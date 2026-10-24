import hashlib
import json
from datetime import date
from pathlib import Path
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


def llm_extract(text: str) -> dict[str, Any]:
    if not settings.openai_api_key:
        return {"summary": text[:1000], "experiences": [], "education": [], "skills": [], "projects": [], "certifications": []}
    schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "headline": {"type": "string"},
            "experiences": {"type": "array", "items": {"type": "object"}},
            "education": {"type": "array", "items": {"type": "object"}},
            "skills": {"type": "array", "items": {"type": "object"}},
            "projects": {"type": "array", "items": {"type": "object"}},
            "certifications": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["summary", "experiences", "education", "skills", "projects", "certifications"],
        "additionalProperties": False,
    }
    payload = {
        "model": settings.openai_model,
        "temperature": 0,
        "response_format": {"type": "json_schema", "json_schema": {"name": "career_profile", "strict": True, "schema": schema}},
        "messages": [
            {"role": "system", "content": "Extract career facts from the resume. Never invent facts. Return only facts supported by the resume. Dates may be null. For skills, include name, category, proficiency_level 1-5 only when supported, years_experience only when supported, and evidence_notes with a concise source-backed explanation."},
            {"role": "user", "content": text},
        ],
    }
    with httpx.Client(timeout=90) as client:
        response = client.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": f"Bearer {settings.openai_api_key}"}, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
    return _json_from_response(content)


def _date(value: Any) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def normalize_skill(name: str) -> str:
    return " ".join(name.strip().lower().split())


def persist_extraction(db: Session, resume: Resume, data: dict[str, Any]) -> None:
    user_id = resume.user_id
    profile = db.scalar(select(CareerProfile).where(CareerProfile.user_id == user_id))
    if not profile:
        profile = CareerProfile(user_id=user_id)
        db.add(profile)
        db.flush()
    if data.get("headline"):
        profile.headline = str(data["headline"])[:200]
    if data.get("summary"):
        profile.professional_summary = str(data["summary"])

    for item in data.get("experiences", []):
        company = str(item.get("company_name") or item.get("company") or "").strip()
        title = str(item.get("job_title") or item.get("title") or "").strip()
        if not company or not title:
            continue
        db.add(Experience(user_id=user_id, company_name=company[:200], job_title=title[:200], employment_type=item.get("employment_type"), location=item.get("location"), start_date=_date(item.get("start_date")), end_date=_date(item.get("end_date")), is_current=bool(item.get("is_current", False)), description=item.get("description"), achievements=item.get("achievements"), source_resume_id=resume.id))

    for item in data.get("education", []):
        institution = str(item.get("institution") or "").strip()
        if not institution:
            continue
        db.add(Education(user_id=user_id, institution=institution[:240], qualification=item.get("qualification"), field_of_study=item.get("field_of_study"), start_date=_date(item.get("start_date")), end_date=_date(item.get("end_date")), grade=item.get("grade"), description=item.get("description"), source_resume_id=resume.id))

    for item in data.get("projects", []):
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        db.add(Project(user_id=user_id, name=name[:200], role=item.get("role"), description=item.get("description"), technologies=item.get("technologies"), project_url=item.get("project_url"), start_date=_date(item.get("start_date")), end_date=_date(item.get("end_date")), source_resume_id=resume.id))

    for item in data.get("certifications", []):
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        db.add(Certification(user_id=user_id, name=name[:200], issuing_organization=item.get("issuing_organization"), credential_id=item.get("credential_id"), credential_url=item.get("credential_url"), issue_date=_date(item.get("issue_date")), expiry_date=_date(item.get("expiry_date")), does_not_expire=bool(item.get("does_not_expire", False)), source_resume_id=resume.id))

    for item in data.get("skills", []):
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        normalized = normalize_skill(name)
        skill = db.scalar(select(Skill).where(Skill.normalized_name == normalized))
        if not skill:
            skill = Skill(name=name[:120], normalized_name=normalized[:120], category=item.get("category"))
            db.add(skill)
            db.flush()
        existing = db.scalar(select(UserSkill).where(UserSkill.user_id == user_id, UserSkill.skill_id == skill.id))
        if existing:
            existing.proficiency_level = item.get("proficiency_level")
            existing.years_experience = item.get("years_experience")
            existing.evidence_notes = item.get("evidence_notes")
            existing.source_resume_id = resume.id
        else:
            db.add(UserSkill(user_id=user_id, skill_id=skill.id, proficiency_level=item.get("proficiency_level"), years_experience=item.get("years_experience"), last_used_date=_date(item.get("last_used_date")), evidence_notes=item.get("evidence_notes"), source_resume_id=resume.id))


def process_resume(db: Session, job: ProcessingJob) -> None:
    resume = db.get(Resume, job.resume_id)
    if not resume:
        raise ValueError("Resume not found")
    content = resume_storage.read(resume.storage_key)
    text = extract_pdf_text(content)
    data = llm_extract(text)
    extraction = db.scalar(select(ResumeExtraction).where(ResumeExtraction.resume_id == resume.id, ResumeExtraction.extractor_version == settings.extractor_version))
    if not extraction:
        extraction = ResumeExtraction(resume_id=resume.id, extractor_version=settings.extractor_version)
        db.add(extraction)
    extraction.status = "succeeded"
    extraction.extracted_data = data
    extraction.error_code = None
    extraction.error_message = None
    extraction.completed_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
    persist_extraction(db, resume, data)
