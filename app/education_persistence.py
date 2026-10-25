from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from .models.career import Education, ResumeExtraction
from .models.core import Resume


def _value(item: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = item.get(key)
        if value is None:
            continue
        if isinstance(value, dict):
            value = value.get("name") or value.get("value") or value.get("text")
        if value is not None and str(value).strip():
            return value
    return None


def _date(value: Any) -> date | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        text = str(value).strip()
        if len(text) == 4 and text.isdigit():
            return date(int(text), 1, 1)
        return date.fromisoformat(text[:10])
    except (TypeError, ValueError):
        return None


def _normalize(item: Any) -> dict[str, Any] | None:
    if isinstance(item, str):
        value = item.strip()
        return {"institution": value} if value else None
    if not isinstance(item, dict):
        return None

    institution = _value(
        item,
        "institution",
        "institution_name",
        "school",
        "school_name",
        "university",
        "university_name",
        "college",
        "college_name",
    )
    qualification = _value(item, "qualification", "degree", "degree_name", "program", "program_name")
    field = _value(item, "field_of_study", "field", "major", "specialization", "subject")

    # Some extractors return a single `name` field for the institution.
    if not institution:
        name = _value(item, "name")
        if name and (qualification or field):
            institution = name

    if not institution:
        return None

    return {
        "institution": str(institution).strip()[:240],
        "qualification": str(qualification).strip()[:160] if qualification else None,
        "field_of_study": str(field).strip()[:160] if field else None,
        "start_date": _date(_value(item, "start_date", "start_year")),
        "end_date": _date(_value(item, "end_date", "end_year")),
        "grade": _value(item, "grade", "gpa", "score"),
        "description": _value(item, "description", "details"),
    }


def ensure_education_persisted(db: Session, resume: Resume, data: dict[str, Any]) -> int:
    """Persist R1 education data and enforce the DB postcondition.

    This is intentionally idempotent for one resume: existing rows sourced from
    this resume are replaced with the normalized extraction result.
    """
    raw_items = data.get("education") or []
    if not isinstance(raw_items, list):
        raw_items = [raw_items]

    normalized = [item for raw in raw_items if (item := _normalize(raw)) is not None]

    db.execute(delete(Education).where(Education.source_resume_id == resume.id))
    for item in normalized:
        db.add(
            Education(
                user_id=resume.user_id,
                institution=item["institution"],
                qualification=item["qualification"],
                field_of_study=item["field_of_study"],
                start_date=item["start_date"],
                end_date=item["end_date"],
                grade=item["grade"],
                description=item["description"],
                source_resume_id=resume.id,
            )
        )

    db.flush()

    persisted = db.scalar(
        select(Education.id)
        .where(Education.source_resume_id == resume.id)
        .limit(1)
    )
    if normalized and persisted is None:
        keys = sorted({key for raw in raw_items if isinstance(raw, dict) for key in raw})
        raise RuntimeError(
            "R1 education persistence invariant failed: extraction contained "
            f"{len(normalized)} education item(s), but no education row was persisted; "
            f"received keys: {keys}"
        )
    return len(normalized)
