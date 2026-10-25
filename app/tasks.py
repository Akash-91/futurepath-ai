from datetime import datetime, timezone

from sqlalchemy import select

from .celery_app import celery_app
from .db.session import SessionLocal
from .education_persistence import ensure_education_persisted
from .models.core import ProcessingJob, Resume
from .models.career import ResumeExtraction
from .resume_processing import process_resume


@celery_app.task(bind=True, name="app.tasks.process_resume_job")
def process_resume_job(self, job_id: str):
    db = SessionLocal()
    try:
        job = db.get(ProcessingJob, job_id)
        if not job or job.status in {"succeeded", "cancelled"}:
            return
        job.status = "running"
        job.attempt_count += 1
        job.started_at = datetime.now(timezone.utc)
        db.commit()
        try:
            process_resume(db, job)

            # R1 postcondition: if extraction contains education, at least one
            # corresponding education row must exist before the job succeeds.
            resume = db.get(Resume, job.resume_id) if job.resume_id else None
            if resume:
                extraction = db.scalar(
                    select(ResumeExtraction).where(
                        ResumeExtraction.resume_id == resume.id,
                        ResumeExtraction.extractor_version == "r1-v1",
                    )
                )
                if extraction and extraction.extracted_data:
                    ensure_education_persisted(db, resume, extraction.extracted_data)

            job.status = "succeeded"
            job.finished_at = datetime.now(timezone.utc)
            job.error_code = None
            job.error_message = None
            db.commit()
        except Exception as exc:
            db.rollback()
            job = db.get(ProcessingJob, job.id)
            job.error_code = "PROCESSING_FAILED"
            job.error_message = str(exc)[:500]
            if job.attempt_count < job.max_attempts:
                job.status = "queued"
                db.commit()
                raise self.retry(exc=exc, countdown=min(60 * (2 ** (job.attempt_count - 1)), 900))
            job.status = "failed"
            job.finished_at = datetime.now(timezone.utc)
            db.commit()
            raise
    finally:
        db.close()
