
# FuturePath AI
## MVP1 / Release 1 — Career Profile Intelligence
### High-Level Design

**Document Version:** R1.0  
**Status:** Architecture Baseline  
**Scope:** Release 1 only

---

# 1. Executive Summary

FuturePath AI Release 1 establishes the foundational career intelligence platform.

The objective is:

> **“What does FuturePath understand about my career today?”**

The system accepts a user's resume, extracts structured career information, validates it, identifies skills and evidence, generates semantic representations and stores the resulting career profile for later releases.

R1 intentionally does **not** attempt to solve the entire FuturePath vision.

---

# 2. R1 Scope

## In scope

- Authentication
- Resume upload
- PDF validation
- PDF text extraction
- Asynchronous processing
- Job status
- Structured LLM extraction
- Schema validation
- Evidence/provenance
- Skill normalization
- Skill embeddings
- Career profile
- Experience
- Skills
- User corrections
- PostgreSQL
- pgvector
- Redis
- Celery/ARQ
- Retry handling
- Idempotency
- Basic observability
- Docker Compose
- Automated testing

---

# 3. Explicitly Out of Scope

R1 does not implement:

- Market intelligence
- Job ingestion
- Target-role gap analysis
- RAG
- Educational RAG
- Agents
- MCP
- Kafka
- Microservices
- Kubernetes/OpenShift
- Dedicated vector database
- Autonomous self-learning
- RLHF
- Market clustering
- Semantic vector caching
- OCR unless real input data proves it necessary

---

# 4. Architecture Principles

## Principle 1 — Deterministic over generative

LLM:

```text
Extract
Interpret
Summarize
```

Code:

```text
Validate
Store
Compare
Calculate
Control
```

---

## Principle 2 — Async by default for long-running AI work

User-facing APIs must not wait for the complete AI pipeline.

---

## Principle 3 — PostgreSQL is the source of truth

Transactional career information lives in PostgreSQL.

---

## Principle 4 — Evidence-backed intelligence

Every extracted skill should ideally have evidence pointing back to the source resume.

---

## Principle 5 — Start simple, evolve using measurable triggers

Do not introduce distributed architecture merely because the final product may eventually need it.

---

# 5. Context Diagram

```text
                     ┌──────────────────┐
                     │      USER        │
                     └────────┬─────────┘
                              │
                              │ HTTPS
                              ▼
                    ┌──────────────────┐
                    │ Next.js / React  │
                    └────────┬─────────┘
                             │
                             │ REST
                             ▼
                ┌─────────────────────────────┐
                │      FuturePath Backend    │
                │          FastAPI            │
                │                             │
                │ Auth                        │
                │ Resume                     │
                │ Profile                    │
                │ Skills                     │
                │ Jobs/Status                │
                └──────┬───────────┬─────────┘
                       │           │
                       │           │
                    enqueue     DB operations
                       │           │
                       ▼           ▼
                  ┌─────────┐ ┌──────────────┐
                  │  Redis  │ │ PostgreSQL   │
                  │ Broker  │ │ + pgvector   │
                  └────┬────┘ └──────▲───────┘
                       │              │
                       ▼              │
                ┌──────────────┐     │
                │Celery Worker │─────┘
                │              │
                │ PDF parser   │
                │ LLM          │
                │ Validation   │
                │ Embeddings   │
                └──────┬───────┘
                       │
                       ▼
               ┌────────────────┐
               │ External AI    │
               │ LLM/Embedding  │
               └────────────────┘
```

---

# 6. Resume Processing Sequence

```text
User
 │
 │ POST /resume
 ▼
FastAPI
 │
 ├── validate request
 ├── store document metadata
 ├── create processing job
 │
 ▼
Redis
 │
 ▼
Celery Worker
 │
 ├── retrieve document
 ├── extract PDF text
 ├── normalize text
 ├── call structured LLM
 ├── validate schema
 ├── validate evidence
 ├── normalize skills
 ├── generate embeddings
 └── persist profile
 │
 ▼
PostgreSQL + pgvector
 │
 ▼
Job = COMPLETED
```

Client:

```text
GET /jobs/{job_id}
```

returns current state.

---

# 7. Processing State Machine

```text
             ┌──────────┐
             │ PENDING  │
             └────┬─────┘
                  │
                  ▼
            ┌────────────┐
            │ PROCESSING │
            └─────┬──────┘
                  │
          ┌───────┴────────┐
          ▼                ▼
    ┌───────────┐     ┌────────┐
    │ COMPLETED │     │ FAILED │
    └───────────┘     └────────┘
```

Transient failures:

```text
PROCESSING
    ↓
retry
    ↓
PROCESSING
```

Bounded retries prevent infinite loops.

---

# 8. Application Architecture

## Modular monolith

Logical modules:

```text
app/
├── api/
│   ├── auth/
│   ├── resume/
│   ├── profile/
│   └── jobs/
│
├── domain/
│   ├── users/
│   ├── resumes/
│   ├── profiles/
│   ├── skills/
│   └── evidence/
│
├── services/
│   ├── pdf_extractor.py
│   ├── llm_extractor.py
│   ├── skill_normalizer.py
│   └── embedding_service.py
│
├── workers/
│   └── tasks.py
│
└── infrastructure/
    ├── database/
    ├── redis/
    └── external_ai/
```

Logical separation exists even though deployment remains one application.

---

# 9. Data Architecture

## Core entities

### User

```text
user
-----
id
email
created_at
```

### Resume

```text
resume
------
id
user_id
file_reference
content_hash
status
uploaded_at
```

### Processing Job

```text
processing_job
--------------
id
resume_id
status
attempt_count
started_at
completed_at
error_code
```

### Career Profile

```text
career_profile
--------------
id
user_id
summary
total_experience
updated_at
```

### Experience

```text
experience
----------
id
profile_id
company
role
start_date
end_date
description
```

### Skill

```text
skill
-----
id
canonical_name
category
embedding
```

### Profile Skill

```text
profile_skill
-------------
profile_id
skill_id
proficiency
confidence
```

### Skill Evidence

```text
skill_evidence
--------------
id
profile_skill_id
source_resume_id
evidence_text
source_location
```

---

# 10. Vector Architecture

R1 uses:

```text
PostgreSQL
      +
pgvector
```

Vectors are associated with entities such as skills.

Example:

```text
Kubernetes
    │
    ├── canonical_name
    ├── category
    └── embedding
```

Vector dimensionality is determined by the selected embedding model.

Do not hard-code the dimension independently of the model configuration.

The attached software-stack document gives a concrete 1536-dimensional embedding configuration using OpenAI's `text-embedding-3-small`; this should be treated as the selected implementation configuration only if we lock that model for R1.

---

# 11. AI Architecture

```text
Resume
  ↓
Parser
  ↓
Normalized Text
  ↓
LLM
  ↓
Structured JSON
  ↓
Pydantic
  ↓
Evidence Validation
  ↓
Skill Normalization
  ↓
Embeddings
  ↓
PostgreSQL
```

---

# 12. Facts, Inferences and Recommendations

These must not be mixed.

### Fact

> “Worked with Kubernetes.”

### Inference

> “Likely has practical Kubernetes experience.”

### Recommendation

> “Advanced Kubernetes networking may be useful for the target role.”

R1 primarily stores:

**facts + evidence + controlled inference**

Recommendations become more important in R2/R3.

---

# 13. API Design

## Upload resume

```http
POST /api/v1/resumes
```

Response:

```http
202 Accepted
```

```json
{
  "resume_id": "123",
  "job_id": "456",
  "status": "PENDING"
}
```

---

## Job status

```http
GET /api/v1/jobs/{job_id}
```

Example:

```json
{
  "job_id": "456",
  "status": "PROCESSING"
}
```

---

## Career profile

```http
GET /api/v1/profile
```

---

## Update profile

```http
PATCH /api/v1/profile
```

Allows user correction.

---

## Resume details

```http
GET /api/v1/resumes/{resume_id}
```

---

# 14. Idempotency

Resume processing must not blindly create duplicates.

Potential mechanism:

```text
SHA-256(file)
      ↓
content_hash
      ↓
existing?
 ┌────┴────┐
yes        no
 ↓          ↓
reuse     process
```

API requests may additionally use an idempotency key.

---

# 15. Reliability

### LLM failure

```text
API remains available
        ↓
job remains pending/retryable
        ↓
worker retries
```

### Worker failure

```text
worker crash
   ↓
task retry
```

### Database failure

Controlled error + retry where appropriate.

### Malformed AI response

```text
LLM
 ↓
Schema validation
 ↓
INVALID
 ↓
retry/reject
```

Never persist invalid AI output simply because the LLM produced it.

---

# 16. Security

R1 security baseline:

- HTTPS
- authentication
- authorization
- input validation
- file validation
- rate limiting
- secrets management
- encryption
- least privilege
- safe logging
- data deletion
- auditability

Resume contents should not appear in normal application logs.

---

# 17. Observability

### Metrics

```text
API p95/p99
Queue depth
Task age
Processing duration
Retry count
LLM latency
LLM failure rate
Embedding latency
DB latency
Extraction success rate
```

### Correlation

```text
request_id
   ↓
job_id
   ↓
worker task
   ↓
LLM call
   ↓
DB transaction
```

---

# 18. Deployment

## Local

```text
Docker Compose
```

Services:

```text
frontend
api
worker
redis
postgres
```

---

## CI/CD

```text
Git Push
   ↓
Lint
   ↓
Unit Tests
   ↓
Integration Tests
   ↓
Security Checks
   ↓
Docker Build
   ↓
Deploy
```

---

# 19. Technology Baseline

| Layer | R1 Choice |
|---|---|
| Frontend | Next.js / React |
| Styling | Tailwind/shadcn |
| Backend | Python / FastAPI |
| Validation | Pydantic |
| Async | Celery/ARQ |
| Broker | Redis |
| PDF | pypdf + pdfplumber |
| LLM | External structured-output LLM |
| Embeddings | External embedding model |
| Database | PostgreSQL |
| Vector | pgvector |
| ORM | SQLAlchemy |
| Migration | Alembic |
| Container | Docker |
| Local orchestration | Docker Compose |
| Tests | Pytest |
| CI | GitHub Actions |

The attached `CompleteSoftwareStack` document provides essentially this baseline technology map. 

---

# 20. R1 Architecture Summary

```text
                    ┌──────────────┐
                    │     USER     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Next.js    │
                    └──────┬───────┘
                           │
                           ▼
              ┌────────────────────────┐
              │       FastAPI          │
              │    Modular Monolith    │
              └───────┬─────────┬──────┘
                      │         │
                      ▼         ▼
                  ┌───────┐ ┌──────────────┐
                  │ Redis │ │ PostgreSQL   │
                  └───┬───┘ │ + pgvector   │
                      │     └──────▲───────┘
                      ▼            │
                ┌──────────┐      │
                │ Celery   │──────┘
                │ Workers  │
                └────┬─────┘
                     │
                     ▼
               ┌────────────┐
               │ External   │
               │ AI APIs    │
               └────────────┘
```

---

# 21. R1 Definition of Done

R1 is complete when a user can:

1. Register/login
2. Upload a resume
3. Receive a job ID
4. See processing status
5. Resume is parsed asynchronously
6. Structured career information is extracted
7. Skills are identified
8. Evidence is stored
9. Embeddings are generated
10. Career profile is stored
11. User can review it
12. User can correct it
13. Failures are retried safely
14. Duplicate processing is prevented
15. System metrics are visible
16. Automated tests pass

---

# 22. R1 Success Principle

The objective is **not** to prove that FuturePath can do everything.

The objective is to prove:

> **FuturePath can reliably convert a user's unstructured career history into a trustworthy structured career profile.**

That becomes the foundation for R2.