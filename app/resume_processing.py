import hashlib
import json
import re
from datetime import date
from typing import Any

import httpx
from pypdf import PdfReader
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from .config import settings
from .models.career import CareerProfile, Education, Experience, Project, Certification, Skill, UserSkill, ResumeExtraction
from .models.core import ProcessingJob, Resume
from .storage import resume_storage


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_pdf_text(content: bytes) -> str:
    import io
    reader = PdfReader(io.BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages).strip()
    if not text:
        raise ValueError("PDF contains no extractable text")
    return text[:120000]


def _json_from_response(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def _clean_line(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\x7f", "")).strip(" -•\t")


def _parse_date_range(value: str) -> tuple[date | None, date | None, bool]:
    normalized = value.replace("–", "-").replace("—", "-")
    match = re.search(r"(?P<start>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\s*-\s*(?P<end>(?:Present|Current|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}))", normalized, re.I)
    if not match:
        return None, None, False
    from datetime import datetime
    def parse_month(value: str) -> date | None:
        if value.lower() in {"present", "current"}:
            return None
        for fmt in ("%b %Y", "%B %Y"):
            try:
                return datetime.strptime(value.title(), fmt).date()
            except ValueError:
                pass
        return None
    end_text = match.group("end")
    return parse_month(match.group("start")), parse_month(end_text), end_text.lower() in {"present", "current"}


def deterministic_extract(text: str) -> dict[str, Any]:
    """Conservative local R1 parser for text-based resumes when no LLM is configured."""
    lines = [_clean_line(line) for line in text.splitlines() if _clean_line(line)]
    upper = [line.upper().strip(":") for line in lines]
    sections = {"TECHNICAL SKILLS", "PROFESSIONAL EXPERIENCE", "EDUCATION", "PROJECTS", "CERTIFICATIONS", "ACHIEVEMENTS"}

    summary = ""
    if "PROFESSIONAL SUMMARY" in upper:
        i = upper.index("PROFESSIONAL SUMMARY") + 1
        chunks = []
        while i < len(lines) and upper[i] not in sections:
            chunks.append(lines[i]); i += 1
        summary = " ".join(chunks).strip()

    headline = ""
    if "PROFESSIONAL SUMMARY" in upper:
        i = upper.index("PROFESSIONAL SUMMARY")
        if i > 0 and "|" in lines[i - 1]:
            headline = " | ".join(p.strip() for p in lines[i - 1].split("|")[:2])

    skills: list[dict[str, Any]] = []
    if "TECHNICAL SKILLS" in upper:
        i = upper.index("TECHNICAL SKILLS") + 1
        while i < len(lines) and upper[i] not in {"PROFESSIONAL EXPERIENCE", "EDUCATION", "PROJECTS", "CERTIFICATIONS", "ACHIEVEMENTS"}:
            if ":" in lines[i]:
                category, values = lines[i].split(":", 1)
                for value in re.split(r",|;", values):
                    name = _clean_line(value)
                    if name:
                        skills.append({"name": name, "category": category.strip()})
            i += 1

    experiences: list[dict[str, Any]] = []
    if "PROFESSIONAL EXPERIENCE" in upper:
        i = upper.index("PROFESSIONAL EXPERIENCE") + 1
        while i < len(lines) and upper[i] not in {"EDUCATION", "PROJECTS", "CERTIFICATIONS", "ACHIEVEMENTS"}:
            line = lines[i]
            m = re.search(r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*[–—-]\s*(?:Present|Current|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}))", line, re.I)
            if m:
                prefix = line[:m.start()].strip(" -—–")
                title, company = prefix, ""
                if "—" in prefix: title, company = [p.strip() for p in prefix.split("—", 1)]
                elif "–" in prefix: title, company = [p.strip() for p in prefix.split("–", 1)]
                elif "-" in prefix: title, company = [p.strip() for p in prefix.split("-", 1)]
                if "|" in company: company, location = [p.strip() for p in company.split("|", 1)]
                else: location = None
                start_date, end_date, is_current = _parse_date_range(m.group(1))
                i += 1; description = []
                while i < len(lines) and upper[i] not in {"EDUCATION", "PROJECTS", "CERTIFICATIONS", "ACHIEVEMENTS"}:
                    if re.search(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*[–—-]\s*", lines[i], re.I): break
                    description.append(lines[i]); i += 1
                if company and title:
                    experiences.append({"company_name": company, "job_title": title, "location": location, "start_date": start_date.isoformat() if start_date else None, "end_date": end_date.isoformat() if end_date else None, "is_current": is_current, "description": " ".join(description) or None})
                continue
            i += 1

    education: list[dict[str, Any]] = []
    if "EDUCATION" in upper:
        i = upper.index("EDUCATION") + 1
        while i < len(lines) and upper[i] not in {"PROJECTS", "CERTIFICATIONS", "ACHIEVEMENTS"}:
            m = re.search(r"(\d{4})\s*[–—-]\s*(\d{4}|Present|Current)", lines[i], re.I)
            if m:
                prefix = lines[i][:m.start()].strip(" -—–")
                qualification = None; institution = prefix
                if "|" in prefix:
                    qualification, institution = [p.strip() for p in prefix.split("|", 1)]
                elif "," in prefix:
                    qualification, institution = [p.strip() for p in prefix.split(",", 1)]
                education.append({"institution": institution, "qualification": qualification, "start_date": f"{m.group(1)}-01-01", "end_date": None if m.group(2).lower() in {"present", "current"} else f"{m.group(2)}-01-01"})
            i += 1

    projects: list[dict[str, Any]] = []
    if "PROJECTS" in upper:
        i = upper.index("PROJECTS") + 1
        while i < len(lines) and upper[i] not in {"CERTIFICATIONS", "ACHIEVEMENTS"}:
            line = lines[i]
            if line and not line.startswith(("-", "•")):
                projects.append({"name": re.split(r"\s+[|:-]\s+", line, maxsplit=1)[0].strip(), "description": lines[i + 1] if i + 1 < len(lines) else None})
            i += 1

    certifications: list[dict[str, Any]] = []
    if "CERTIFICATIONS" in upper:
        i = upper.index("CERTIFICATIONS") + 1
        while i < len(lines) and upper[i] not in {"ACHIEVEMENTS"}:
            if lines[i]: certifications.append({"name": lines[i]})
            i += 1

    return {"summary": summary or text[:1000], "headline": headline, "experiences": experiences, "education": education, "skills": skills, "projects": projects, "certifications": certifications}


def llm_extract(text: str) -> dict[str, Any]:
    if not settings.openai_api_key:
        return deterministic_extract(text)
    schema = {
        "type": "object",
        "properties": {"summary": {"type": "string"}, "headline": {"type": "string"}, "experiences": {"type": "array", "items": {"type": "object"}}, "education": {"type": "array", "items": {"type": "object"}}, "skills": {"type": "array", "items": {"type": "object"}}, "projects": {"type": "array", "items": {"type": "object"}}, "certifications": {"type": "array", "items": {"type": "object"}}},
        "required": ["summary", "experiences", "education", "skills", "projects", "certifications"], "additionalProperties": False,
    }
    payload = {"model": settings.openai_model, "temperature": 0, "response_format": {"type": "json_schema", "json_schema": {"name": "career_profile", "strict": True, "schema": schema}}, "messages": [{"role": "system", "content": "Extract career facts from the resume. Never invent facts. Return only facts supported by the resume. Dates may be null. For skills, include name, category, proficiency_level 1-5 only when supported, years_experience only when supported, and evidence_notes with a concise source-backed explanation."}, {"role": "user", "content": text}]}
    with httpx.Client(timeout=90) as client:
        response = client.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": f"Bearer {settings.openai_api_key}"}, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
    return _json_from_response(content)


def _date(value: Any) -> date | None:
    if not value: return None
    try: return date.fromisoformat(str(value)[:10])
    except ValueError: return None


def normalize_skill(name: str) -> str:
    return " ".join(name.strip().lower().split())


def _first_value(item: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = item.get(key)
        if value is not None and str(value).strip():
            return value
    return None


def persist_extraction(db: Session, resume: Resume, data: dict[str, Any]) -> None:
    user_id = resume.user_id
    profile = db.scalar(select(CareerProfile).where(CareerProfile.user_id == user_id))
    if not profile:
        profile = CareerProfile(user_id=user_id); db.add(profile); db.flush()
    if data.get("headline"): profile.headline = str(data["headline"])[:200]
    if data.get("summary"): profile.professional_summary = str(data["summary"])

    db.execute(delete(Experience).where(Experience.source_resume_id == resume.id))
    db.execute(delete(Education).where(Education.source_resume_id == resume.id))
    db.execute(delete(Project).where(Project.source_resume_id == resume.id))
    db.execute(delete(Certification).where(Certification.source_resume_id == resume.id))
    db.execute(delete(UserSkill).where(UserSkill.source_resume_id == resume.id))

    for item in data.get("experiences", []):
        company = str(item.get("company_name") or item.get("company") or "").strip(); title = str(item.get("job_title") or item.get("title") or "").strip()
        if company and title: db.add(Experience(user_id=user_id, company_name=company[:200], job_title=title[:200], employment_type=item.get("employment_type"), location=item.get("location"), start_date=_date(item.get("start_date")), end_date=_date(item.get("end_date")), is_current=bool(item.get("is_current", False)), description=item.get("description"), achievements=item.get("achievements"), source_resume_id=resume.id))
    for item in data.get("education", []):
        # Accept the canonical R1 fields as well as common provider/LLM aliases.
        # The normalized table requires only institution, so do not silently drop
        # a valid education item when a model calls it school/university/college.
        institution = _first_value(item, "institution", "institution_name", "school", "school_name", "university", "university_name", "college", "college_name")
        qualification = _first_value(item, "qualification", "degree", "degree_name")
        field_of_study = _first_value(item, "field_of_study", "field", "major", "specialization")
        if institution:
            db.add(Education(user_id=user_id, institution=str(institution)[:240], qualification=str(qualification)[:160] if qualification else None, field_of_study=str(field_of_study)[:160] if field_of_study else None, start_date=_date(item.get("start_date") or item.get("start_year")), end_date=_date(item.get("end_date") or item.get("end_year")), grade=item.get("grade"), description=item.get("description"), source_resume_id=resume.id))
    for item in data.get("projects", []):
        name = str(item.get("name") or "").strip()
        if name: db.add(Project(user_id=user_id, name=name[:200], role=item.get("role"), description=item.get("description"), technologies=item.get("technologies"), project_url=item.get("project_url"), start_date=_date(item.get("start_date")), end_date=_date(item.get("end_date")), source_resume_id=resume.id))
    for item in data.get("certifications", []):
        name = str(item.get("name") or "").strip()
        if name: db.add(Certification(user_id=user_id, name=name[:200], issuing_organization=item.get("issuing_organization"), credential_id=item.get("credential_id"), credential_url=item.get("credential_url"), issue_date=_date(item.get("issue_date")), expiry_date=_date(item.get("expiry_date")), does_not_expire=bool(item.get("does_not_expire", False)), source_resume_id=resume.id))
    for item in data.get("skills", []):
        name = str(item.get("name") or "").strip()
        if not name: continue
        normalized = normalize_skill(name)
        skill = db.scalar(select(Skill).where(Skill.normalized_name == normalized))
        if not skill:
            skill = Skill(name=name[:120], normalized_name=normalized[:120], category=item.get("category")); db.add(skill); db.flush()
        existing = db.scalar(select(UserSkill).where(UserSkill.user_id == user_id, UserSkill.skill_id == skill.id))
        if existing:
            existing.proficiency_level = item.get("proficiency_level"); existing.years_experience = item.get("years_experience"); existing.evidence_notes = item.get("evidence_notes"); existing.source_resume_id = resume.id
        else:
            db.add(UserSkill(user_id=user_id, skill_id=skill.id, proficiency_level=item.get("proficiency_level"), years_experience=item.get("years_experience"), last_used_date=_date(item.get("last_used_date")), evidence_notes=item.get("evidence_notes"), source_resume_id=resume.id))


def process_resume(db: Session, job: ProcessingJob) -> None:
    resume = db.get(Resume, job.resume_id)
    if not resume: raise ValueError("Resume not found")
    content = resume_storage.read(resume.storage_key)
    text = extract_pdf_text(content)
    data = llm_extract(text)
    extraction = db.scalar(select(ResumeExtraction).where(ResumeExtraction.resume_id == resume.id, ResumeExtraction.extractor_version == settings.extractor_version))
    if not extraction:
        extraction = ResumeExtraction(resume_id=resume.id, extractor_version=settings.extractor_version); db.add(extraction)
    extraction.status = "succeeded"; extraction.extracted_data = data; extraction.error_code = None; extraction.error_message = None
    from datetime import datetime, timezone
    extraction.completed_at = datetime.now(timezone.utc)
    persist_extraction(db, resume, data)
