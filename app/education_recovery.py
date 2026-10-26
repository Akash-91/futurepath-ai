import re
from typing import Any


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\x7f", "")).strip(" -•\t")


def _looks_like_institution(value: str) -> bool:
    return bool(
        re.search(
            r"\b(?:university|college|institute|school|academy|polytechnic)\b",
            value,
            re.I,
        )
    )


def _looks_like_qualification(value: str) -> bool:
    return bool(
        re.search(
            r"\b(?:B\.?Tech|M\.?Tech|B\.?E\.?|M\.?E\.?|B\.?Sc|M\.?Sc|B\.?A\.?|M\.?A\.?|MBA|MCA|BCA|Ph\.?D|Bachelor|Master|Doctor|Diploma|Associate)\b",
            value,
            re.I,
        )
    )


def recover_education_from_text(text: str) -> list[dict[str, Any]]:
    """Recover education records from plain resume text without inventing facts."""
    lines = [_clean(line) for line in text.splitlines() if _clean(line)]
    upper = [line.upper().strip(":") for line in lines]
    section_names = {
        "TECHNICAL SKILLS",
        "PROFESSIONAL EXPERIENCE",
        "EDUCATION",
        "PROJECTS",
        "CERTIFICATIONS",
        "ACHIEVEMENTS",
        "PROFESSIONAL SUMMARY",
    }
    if "EDUCATION" not in upper:
        return []

    start = upper.index("EDUCATION") + 1
    end = len(lines)
    for index in range(start, len(lines)):
        if upper[index] in section_names - {"EDUCATION"}:
            end = index
            break

    year_range = re.compile(
        r"(?P<start>\d{4})\s*[–—-]\s*(?P<end>\d{4}|Present|Current)", re.I
    )
    month_range = re.compile(
        r"(?P<start>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})"
        r"\s*[–—-]\s*(?P<end>Present|Current|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})",
        re.I,
    )

    records: list[dict[str, Any]] = []
    for line in lines[start:end]:
        match = year_range.search(line) or month_range.search(line)
        content = line[: match.start()].strip(" -—–|,") if match else line
        if not content:
            continue

        institution = None
        qualification = None
        field = None

        parts = [part.strip() for part in re.split(r"\s*\|\s*", content) if part.strip()]
        if len(parts) >= 2:
            institution_candidates = [part for part in parts if _looks_like_institution(part)]
            if institution_candidates:
                institution = institution_candidates[0]
                others = [part for part in parts if part != institution]
                qualification = next(
                    (part for part in others if _looks_like_qualification(part)),
                    others[0] if others else None,
                )
                field = next(
                    (part for part in others if part != qualification and not _looks_like_qualification(part)),
                    None,
                )
            elif _looks_like_qualification(parts[0]) and not _looks_like_qualification(parts[-1]):
                qualification, institution = parts[0], parts[-1]
            elif _looks_like_institution(parts[0]):
                institution, qualification = parts[0], parts[1]

        if not institution:
            dash_parts = [
                part.strip()
                for part in re.split(r"\s+[—–-]\s+", content, maxsplit=1)
                if part.strip()
            ]
            if len(dash_parts) == 2:
                left, right = dash_parts
                if _looks_like_institution(right) or _looks_like_qualification(left):
                    institution = right
                    qualification = left if _looks_like_qualification(left) else None
                elif _looks_like_institution(left):
                    institution = left
                    qualification = right if _looks_like_qualification(right) else None

        if not institution:
            comma_parts = [part.strip() for part in content.split(",", 1) if part.strip()]
            if len(comma_parts) == 2:
                left, right = comma_parts
                if _looks_like_institution(right) or _looks_like_qualification(left):
                    institution = right
                    qualification = left if _looks_like_qualification(left) else None
                elif _looks_like_institution(left):
                    institution = left
                    qualification = right if _looks_like_qualification(right) else None

        if not institution:
            at_match = re.search(r"\s+at\s+(?P<institution>.+)$", content, re.I)
            if at_match:
                institution = at_match.group("institution").strip()
                qualification = content[: at_match.start()].strip() or None

        if not institution and _looks_like_institution(content):
            institution = content

        if institution:
            record: dict[str, Any] = {"institution": institution[:240]}
            if qualification:
                record["qualification"] = qualification[:160]
            if field:
                record["field_of_study"] = field[:160]
            if match and match.group("start").isdigit():
                record["start_date"] = f"{match.group('start')}-01-01"
                end_value = match.group("end")
                record["end_date"] = (
                    None
                    if end_value.lower() in {"present", "current"}
                    else f"{end_value}-01-01"
                )
            records.append(record)

    return records
