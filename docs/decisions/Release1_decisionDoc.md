
# FuturePath AI
## MVP1 / Release 1 — Architecture Decision Record

**Status:** Accepted  
**Release:** R1 — Career Profile Intelligence

---

# 1. Purpose

This document records the architecture decisions made for FuturePath AI Release 1.

It deliberately captures:

- alternatives considered
- advantages
- disadvantages
- trade-offs
- selected option
- rejected options
- failure modes
- security considerations
- scalability considerations
- future change triggers

The goal is to prevent technology choices from becoming arbitrary or fashion-driven.

---

# 2. Source Documents Reviewed

Three attached architecture documents were reviewed:

### Document A — CompleteSoftwareStack

Primarily a technology-stack and implementation blueprint.

It proposes:

- Next.js / React
- FastAPI
- Pydantic
- Redis
- Celery/ARQ
- pypdf/pdfplumber
- structured LLM extraction
- embeddings
- PostgreSQL
- pgvector
- SQLAlchemy
- Alembic
- Docker Compose
- Pytest
- GitHub Actions

It presents the baseline:

```text
Browser
  ↓
Next.js
  ↓
FastAPI
  ↓
Redis
  ↓
Celery
  ↓
PostgreSQL + pgvector
```

 

---

### Document B — Comprehensive HLD v0.2

This document expands the architecture into:

- modular monolith
- Redis + Celery
- PostgreSQL + pgvector
- RAG
- market vectors
- historical career paths
- feedback/self-learning
- semantic caching
- market clustering
- adaptive parsing
- educational RAG

It also gives larger-scale planning assumptions and explicit ADRs.

---

### Document C — HLD v0.1

This document gives the strongest detailed architecture/ADR treatment around:

- quantitative traffic modelling
- modular monolith
- async execution
- Redis + Celery/ARQ
- PostgreSQL + pgvector
- deterministic vs generative responsibilities
- failure handling
- evolution triggers

It explicitly describes microservices, modular monolith and serverless alternatives, and the async alternatives of BackgroundTasks, Redis/Celery and Kafka.

---

# 3. Important Observation

The three documents are **not three competing architectures**.

They represent different levels of maturity:

```text
CompleteSoftwareStack
        │
        │ implementation baseline
        ▼
HLD v0.1
        │
        │ architecture + quantitative reasoning
        ▼
HLD v0.2
        │
        │ future intelligence capabilities
        ▼
FuturePath R1 → R4
```

Therefore:

> We should use the documents as evidence and design input, but not automatically import every future-state capability into R1.

---

# 4. ADR-01 — Backend Architecture

## Problem

FuturePath needs:

- REST APIs
- authentication
- resume processing
- profile management
- skill management
- deterministic business logic
- AI orchestration

We need an architecture that supports R1 without creating unnecessary distributed-system complexity.

---

## Option A — Microservices

```text
Auth Service
     ↓
Resume Service
     ↓
Extraction Service
     ↓
Profile Service
     ↓
Skill Service
```

### Pros

- Independent deployment
- Independent scaling
- Strong service boundaries
- Failure isolation
- Team ownership separation

### Cons

- Network calls
- Distributed tracing
- Multiple deployments
- More CI/CD pipelines
- More operational complexity
- Data consistency complexity
- Harder local development

---

## Option B — Modular Monolith

```text
             FastAPI
                │
    ┌───────────┼────────────┐
    │           │            │
   Auth      Resume       Profile
    │           │            │
    └───────────┼────────────┘
                │
             Skills
```

### Pros

- Simple deployment
- Low latency internal calls
- Shared transaction boundary
- Easy development
- Easy debugging
- Logical domain separation
- Can evolve into services later

### Cons

- Failure can affect the application process
- Modules share runtime
- Independent scaling is limited

---

## Option C — Serverless

### Pros

- Automatic scaling
- Pay-per-use
- Reduced server management

### Cons

- Cold starts
- Execution constraints
- More complex state management
- AI workloads may be awkward
- Local development becomes more complex

---

## Decision

### **Modular Monolith — FastAPI**

---

## Why?

R1 domain boundaries are still evolving.

We want:

```text
clean internal boundaries
+
simple deployment
+
low operational overhead
```

The attached HLDs also select the modular monolith direction. 

---

## Why not microservices?

Because we currently have no demonstrated need for:

- independent service deployment
- separate teams
- dramatically different scaling patterns
- service-level failure isolation

---

## Failure mode

Large PDF parsing could cause memory pressure.

### Defense

Do not execute heavy processing inside the API process.

Move it to workers.

---

## Change trigger

Consider service extraction when one or more becomes true:

```text
Independent deployment required
OR
Independent scaling required
OR
Different ownership
OR
Failure isolation required
OR
Different runtime required
```

---

# 5. ADR-02 — Asynchronous Processing

## Problem

PDF parsing and LLM processing are long-running.

The attached sources describe processing durations in the seconds range and therefore recommend decoupling ingestion from processing. 

---

## Option A — Synchronous

### Pros

- Very simple
- Easy request/response model

### Cons

- HTTP timeout
- Connection starvation
- Poor burst handling
- User waits for AI processing

---

## Option B — FastAPI BackgroundTasks

### Pros

- Very simple
- No separate queue

### Cons

- Same application process
- Process restart can lose work
- Weak isolation
- Limited operational control

---

## Option C — Redis + Celery/ARQ

### Pros

- Queue buffering
- Retries
- Independent workers
- Horizontal scaling
- Job lifecycle

### Cons

- Redis dependency
- Worker infrastructure
- Additional monitoring

---

## Option D — Kafka

### Pros

- Durable event stream
- Replay
- Partitioning
- Multiple consumers
- High throughput

### Cons

- Operational complexity
- More infrastructure
- More configuration
- Unnecessary for R1 workload

The detailed HLD explicitly contrasts these choices and selects Redis + Celery/ARQ.

---

## Decision

### **Redis + Celery**

---

## R1 HLD

```text
Client
  │
  ▼
FastAPI
  │
  │ enqueue
  ▼
Redis
  │
  ▼
Celery Worker
  │
  ├── PDF
  ├── LLM
  ├── validation
  └── embeddings
  │
  ▼
PostgreSQL
```

---

## Why not Kafka?

Kafka is a **valid future option**, not a bad technology.

It becomes justified when we need:

- durable event history
- replay
- many independent consumers
- event-driven architecture across multiple domains
- high event throughput

---

# 6. ADR-03 — Primary Data Store

## Problem

FuturePath needs:

- users
- profiles
- experiences
- skills
- evidence
- jobs
- relationships
- vector similarity

---

## Option A — PostgreSQL + dedicated vector DB

Example:

```text
PostgreSQL
     +
Pinecone/Qdrant
```

### Pros

- Specialized vector capabilities
- Independent vector scaling

### Cons

- Two persistence systems
- Synchronization
- More infrastructure
- More operational cost
- Potential consistency problems

---

## Option B — MongoDB + Qdrant

### Pros

- Flexible documents
- Dedicated vector database

### Cons

- Less natural relational modelling
- More infrastructure
- Two persistence systems

---

## Option C — PostgreSQL + pgvector

### Pros

- Relational integrity
- ACID transactions
- Vector search
- One primary persistence system
- Simple local development
- Easy joins between profile and skills

### Cons

- Vector workload shares database resources
- Dedicated vector DB may eventually scale better for very large workloads

The three documents consistently support PostgreSQL + pgvector as the baseline. 

---

## Decision

### **PostgreSQL + pgvector**

---

## Why?

The core domain is relational.

```text
User
 ↓
Profile
 ↓
Experience
 ↓
Skill
 ↓
Evidence
```

Vectors are an extension of the career data rather than a completely separate domain in R1.

---

## Change trigger

Move to a dedicated vector database when:

- vector workload dominates DB capacity
- vector latency becomes unacceptable
- dataset size materially exceeds practical PostgreSQL capacity
- specialized vector capabilities become necessary

---

# 7. ADR-04 — PDF Processing

## Option A — Direct PDF → LLM

### Pros

- Simple
- Less parsing code

### Cons

- Cost
- Less deterministic
- Vendor dependency
- Harder validation

---

## Option B — pypdf

### Pros

- Lightweight
- Fast
- Local

### Cons

- Layout limitations

---

## Option C — pdfplumber

### Pros

- Better layout extraction

### Cons

- More processing

---

## Option D — OCR

### Pros

- Scanned PDF support

### Cons

- Additional infrastructure
- Cost
- OCR errors

---

## Decision

### **pypdf + pdfplumber**

OCR only when real input data demonstrates the need.

---

# 8. ADR-05 — Structured LLM Output

## Option A — Free-form LLM

### Pros

- Simple

### Cons

- Unreliable structure
- Hard to validate
- Difficult persistence

---

## Option B — JSON mode

### Pros

- Structured output

### Cons

- Schema guarantees can still be insufficient

---

## Option C — Schema-constrained structured output

### Pros

- Strong validation
- Predictable structure
- Easier persistence
- Easier testing

### Cons

- More schema design
- Model/provider capabilities matter

---

## Decision

### **Schema-constrained structured output + Pydantic**

---

# 9. ADR-06 — RAG

## Option A — No RAG

### Pros

- Simple
- Low cost
- Easy to debug

### Cons

- Cannot effectively retrieve external knowledge

---

## Option B — Naive Top-K RAG

```text
Query
 ↓
Vector Search
 ↓
Top K
 ↓
LLM
```

### Pros

- Easy to implement

### Cons

- No domain separation
- Potentially noisy context
- Generic answers

---

## Option C — Multi-domain filtered RAG

```text
User Profile
      │
      ├── Skill Knowledge
      ├── Market Requirements
      └── Historical Paths
              │
              ▼
        RAG Assembly
              │
              ▼
             LLM
```

### Pros

- More relevant context
- Domain-aware retrieval
- Better future intelligence

### Cons

- More complex
- Requires multiple knowledge domains
- Requires retrieval evaluation

The broader HLD selects multi-domain filtered RAG for the mature system.

---

## R1 Decision

### **No RAG**

Why?

R1 does not yet have enough external knowledge domains to justify it.

---

## R3 Decision

Introduce RAG when:

```text
Market knowledge
+
Learning resources
+
Career paths
+
Role requirements
```

become real knowledge domains.

---

# 10. ADR-07 — Agents

## Option A — Deterministic workflows

### Pros

- Predictable
- Testable
- Easy to debug
- Lower cost

### Cons

- Less autonomous

---

## Option B — Agents

### Pros

- Dynamic planning
- Tool selection
- Multi-step investigation

### Cons

- Non-determinism
- Higher cost
- More complex failure handling
- Harder testing

---

## Decision

### **No agents in R1**

Use deterministic workflows.

Agents become candidates in R4.

---

# 11. ADR-08 — Semantic Caching

The broader HLD proposes semantic caching to reduce repeated LLM work and latency.

## Options

### No cache

Simple but every request reaches AI services.

### Exact cache

Fast but only helps identical requests.

### Semantic cache

Similar queries can reuse results.

### R1 decision

**No semantic cache.**

First measure:

```text
request repetition
LLM cost
LLM latency
cache hit opportunity
```

Then introduce it.

---

# 12. ADR-09 — Self-Learning / Feedback

The broader HLD proposes a feedback loop involving career progression and user ratings.

## R1

Do not implement autonomous learning.

Capture the data required for future learning:

```text
user correction
recommendation feedback
profile changes
career progression
```

---

## Important terminology decision

Do not call R4 automatically **RLHF**.

Use:

> **Feedback-driven recommendation learning**

unless we actually implement a true reinforcement-learning/human-feedback training architecture.

---

# 13. ADR-10 — Deployment

## Option A — Docker Compose

### Pros

- Simple
- Reproducible
- Excellent local development
- Low operational overhead

### Cons

- Not a production orchestration platform

---

## Option B — Kubernetes

### Pros

- Autoscaling
- Self-healing
- Container orchestration
- Strong production capabilities

### Cons

- Operational complexity
- More infrastructure
- More learning/maintenance

---

## Decision

### R1 — Docker Compose

Kubernetes/OpenShift becomes a later deployment decision.

---

# 14. ADR-11 — Vector Database

## Options

### pgvector

Selected.

### Pinecone

Specialized managed vector platform.

### Qdrant

Specialized vector search platform.

---

## R1 decision

**pgvector**

because:

```text
Career data
+
metadata
+
relationships
+
vectors
```

can remain within one primary persistence boundary.

---

# 15. What We Deliberately Rejected

| Technology / Pattern | R1 decision |
|---|---|
| Microservices | ❌ Deferred |
| Kafka | ❌ Deferred |
| Kubernetes | ❌ Deferred |
| Dedicated vector DB | ❌ Deferred |
| RAG | ❌ Deferred |
| Agents | ❌ Deferred |
| MCP | ❌ Deferred |
| OCR | ❌ Unless needed |
| Semantic caching | ❌ Deferred |
| Market clustering | ❌ Deferred |
| Autonomous learning | ❌ Deferred |

This is intentional architectural restraint.

---

# 16. Final R1 Technology Decision

```text
Frontend
   ↓
Next.js / React
   ↓
FastAPI Modular Monolith
   ↓
Redis + Celery
   ↓
Workers
   ├── pypdf/pdfplumber
   ├── Structured LLM
   ├── Pydantic validation
   └── Embeddings
   ↓
PostgreSQL + pgvector
```

---

# 17. Why This Architecture Is Defensible

The architecture is not:

> “I like FastAPI.”

It is:

```text
Long-running AI workload
        ↓
Need async processing
        ↓
Redis + Celery

Relational career domain
        ↓
Need transactional DB
        ↓
PostgreSQL

Semantic skill matching
        ↓
Need vector search
        ↓
pgvector

Evolving domain
        ↓
Avoid premature service boundaries
        ↓
Modular monolith

No mature knowledge retrieval requirement
        ↓
Defer RAG

No autonomous planning requirement
        ↓
Defer agents

No event-stream requirement
        ↓
Defer Kafka

No orchestration requirement
        ↓
Defer Kubernetes
```

---

# 18. Architecture Change Triggers

This is critical.

We don't say:

> “One day we will move to microservices.”

We define the trigger.

### Microservices

Trigger:

```text
Independent deployment/scaling/ownership becomes necessary.
```

### Kafka

Trigger:

```text
Multiple independent event consumers
+
replay
+
durable event history
+
higher event volume
```

### Dedicated vector DB

Trigger:

```text
Vector workload becomes the database bottleneck
```

### Kubernetes

Trigger:

```text
Production container orchestration complexity justifies it.
```

### RAG

Trigger:

```text
Multiple external knowledge domains need retrieval.
```

### Agents

Trigger:

```text
Multi-step autonomous planning becomes a real product requirement.
```

---

# 19. Final Architecture Principle

> **Complexity must be earned by requirements.**

FuturePath R1 should therefore be:

```text
Simple enough to build
Reliable enough to trust
Structured enough to extend
Observable enough to operate
Evolvable enough to become R4
```

---

# 20. Solution Architect Interview Closing Answer

If an interviewer asks:

### “Explain your architecture and major decisions.”

Answer:

> “FuturePath AI starts with a modular FastAPI monolith because the domain is still evolving and there is no demonstrated need for independent service deployment. Resume ingestion is asynchronous because PDF parsing and LLM inference are long-running, so the API places work onto Redis and Celery workers. PostgreSQL is the transactional source of truth because the career domain is relational, while pgvector provides semantic skill matching without introducing another persistence system. We use structured LLM outputs with schema validation because LLMs are probabilistic and should not directly control system state. We deliberately defer Kafka, microservices, Kubernetes, RAG, agents and a dedicated vector database until measurable requirements justify them. The architecture is therefore intentionally simple in R1 but has clear evolution triggers for R2 through R4.”