# FuturePath AI — Release 1 Implementation Status

## Goal

Release 1 answers: **What do we understand about my career today?**

## Implemented

- Password and Google authentication backed by the PostgreSQL `users` table.
- Stable UUID application identity and provider/subject uniqueness.
- Career profile read/update APIs with authenticated-user ownership checks.
- PDF-only resume upload with a 10 MB default limit.
- SHA-256 fingerprinting and same-user duplicate upload suppression.
- Private local Docker-mounted resume storage using server-generated storage keys.
- Durable `processing_jobs` records with queued/running/succeeded/failed/cancelled states.
- Redis broker and Celery worker service in Docker Compose.
- Retry endpoint for failed/cancelled processing jobs.
- PDF text extraction with pypdf.
- Structured career extraction through an optional OpenAI-compatible structured JSON call.
- Deterministic fallback when no AI API key is configured; this preserves the ingestion/job path but does not claim full semantic extraction.
- Pydantic-compatible validation at the API boundary and deterministic skill normalization.
- Persistence of extracted summary, experiences, education, projects, certifications, skills and skill evidence into PostgreSQL.
- Resume provenance through `source_resume_id` and skill `evidence_notes`.
- Career profile UI for upload, processing status, retry, and manual review/correction.

## Deliberately deferred

### Embeddings / pgvector

The architecture calls for embeddings in R1, but the database LLD deliberately requires the embedding model and vector dimension to be finalized before creating a production vector column/index. The current implementation therefore does not invent a vector dimension. Add pgvector storage once the selected embedding model, dimensions, similarity metric and active-version semantics are approved.

### OCR

OCR remains deferred until real resume samples demonstrate that image-only/scanned PDFs materially affect extraction quality.

### Object storage

Local private storage is used behind a storage abstraction for development. Production object storage can replace it without changing the API contract.

## Local services

```text
Frontend :3000
API      :8000
Postgres :5432 (localhost only)
Redis    internal Docker network
Worker   Celery
```

## Required local environment

Copy `.env.example` to `.env`. Set a strong `JWT_SECRET`, PostgreSQL password, Google OAuth credentials, and optionally `OPENAI_API_KEY` plus `OPENAI_MODEL` for semantic resume extraction.

Never commit `.env`, Google secrets, OpenAI keys, uploaded resumes, or local database files.

## Acceptance flow

1. Sign in with password or Google.
2. Open the career page.
3. Upload a PDF under 10 MB.
4. Confirm a `resumes` row and a `processing_jobs` row exist.
5. Confirm the job transitions through queued/running/succeeded or failed.
6. With `OPENAI_API_KEY` configured, confirm extracted profile entities are persisted and linked to the source resume.
7. Edit the career profile and verify the authenticated user can read/write only their own profile.
8. Upload the same PDF again and verify no second resume is created for that user.
9. Retry a failed job and verify the existing job is reused rather than creating an unowned duplicate.
