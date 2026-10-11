
# FuturePath AI
## Master Architecture Decisions & Solution Architect Interview Runbook

**Scope:** Release 1 → Release 4  
**Purpose:** Architecture reasoning, decision history, trade-offs and interview preparation

---

# 1. How to Read This Document

Every decision follows:

```text
WHAT?
↓
WHY?
↓
ALTERNATIVES
↓
PROS / CONS
↓
TRADE-OFF
↓
DECISION
↓
WHY THIS?
↓
WHY NOT THE OTHERS?
↓
FAILURE MODES
↓
SECURITY
↓
SCALING
↓
CHANGE TRIGGER
↓
INTERVIEW DEFENSE
```

This is more important than memorizing technology names.

---

# 2. MASTER DECISION TABLE

| Area | Our Choice | Deferred / Rejected |
|---|---|---|
| Backend | FastAPI modular monolith | Microservices |
| Frontend | Next.js / React | — |
| Async processing | Redis + Celery | BackgroundTasks, Kafka |
| Transactional DB | PostgreSQL | MongoDB |
| Vector | pgvector | Pinecone/Qdrant initially |
| PDF | pypdf + pdfplumber | OCR initially |
| LLM output | Structured schema + Pydantic | Free-form |
| RAG | R3 | R1/R2 |
| Matching | Hybrid deterministic + semantic | LLM-only |
| Agents | R4 candidate | R1–R3 |
| MCP | R4 candidate | R1–R3 |
| Cache | Introduce when measured | Semantic cache initially |
| Market clustering | R3/R4 | R1/R2 |
| Deployment | Docker Compose initially | Kubernetes |
| Event streaming | R4 candidate | Kafka initially |
| Self-learning | R4 feedback loop | R1–R3 autonomous learning |
| Vector DB | pgvector initially | Dedicated vector DB |
| OCR | Demand-driven | Default OCR |
| Microservices | Trigger-driven | Premature R1 distribution |

---

# 3. SOURCE DOCUMENT COMPARISON

We reviewed three architecture sources.

## Document A — CompleteSoftwareStack

Strongest contribution:

> **Concrete technology implementation stack.**

It provides the detailed technology mapping:

```text
Next.js
FastAPI
Pydantic
Redis
Celery/ARQ
pypdf/pdfplumber
LLM
Embeddings
PostgreSQL
pgvector
SQLAlchemy
Alembic
Docker Compose
Pytest
GitHub Actions
```

It is especially useful as the implementation baseline.

---

## Document B — Comprehensive HLD v0.2

Strongest contribution:

> **Future-state intelligence architecture.**

It expands into:

- RAG
- market intelligence
- historical career paths
- semantic caching
- market clustering
- adaptive parsing
- educational RAG
- feedback/self-learning

It also provides explicit ADRs for modular monolith, Redis/Celery, PostgreSQL/pgvector and filtered RAG. 

---

## Document C — HLD v0.1

Strongest contribution:

> **Architecture reasoning and progressive evolution.**

It emphasizes:

- justified complexity
- deterministic over generative
- stateless compute
- resilience
- quantitative sizing
- ADRs
- phased architecture
- trigger-based distributed evolution
- interview defense

It explicitly proposes the evolution:

```text
Phase 1
Vertical Slice

Phase 2
Target Analysis

Phase 3
Cost Optimization

Phase 4
Distributed Evolution
```

 

---

# 4. MASTER CONCLUSION FROM THE THREE DOCUMENTS

The documents are complementary.

```text
Document A
Implementation Stack

        +

Document B
Future Intelligence

        +

Document C
Architecture Reasoning

        ↓

FuturePath AI Final Architecture
```

We should not copy every technology from the future-state architecture into R1.

---

# 5. ADR-01 — MODULAR MONOLITH VS MICROSERVICES

## What?

Choose the initial application architecture.

---

## Alternatives

### Microservices

Pros:

- independent deployment
- independent scaling
- failure isolation
- team ownership

Cons:

- network communication
- distributed tracing
- deployment complexity
- data consistency
- more infrastructure

---

### Modular Monolith

Pros:

- simple deployment
- low internal latency
- shared transactions
- fast development
- easier debugging
- clean logical boundaries

Cons:

- shared runtime
- less independent scaling
- possible larger deployment unit

---

### Serverless

Pros:

- automatic scaling
- low infrastructure management

Cons:

- execution constraints
- cold starts
- more complicated AI orchestration
- vendor/platform coupling

---

## Decision

### **FastAPI Modular Monolith**

---

## Why?

R1 domain boundaries are not proven yet.

We prefer:

```text
Logical separation
+
Operational simplicity
```

---

## Why not microservices?

Because we do not yet need:

- independent service deployment
- independent scaling
- organizational service ownership
- failure isolation between domains

---

## Failure mode

One process can affect multiple modules.

### Mitigation

Heavy workloads run outside the API process.

---

## Change trigger

Extract a service when:

> **Independent deployment, scaling, ownership, runtime or failure isolation becomes a measurable requirement.**

The attached HLDs independently arrive at the modular-monolith decision. 

---

# 6. ADR-02 — SYNCHRONOUS VS ASYNCHRONOUS PROCESSING

## Problem

AI/PDF workloads are long-running.

The source documents cite extraction/AI processing in the seconds range and use asynchronous processing to protect the API layer.

---

## Alternatives

| Option | Pros | Cons |
|---|---|---|
| Synchronous | Simple | Timeouts, blocked workers |
| BackgroundTasks | Simple | Same process |
| Redis + Celery | Queue, retries, scaling | Infrastructure |
| Kafka | Durable events/replay | High complexity |

---

## Decision

### Redis + Celery

---

## Why?

Because we need:

- buffering
- retries
- independent workers
- controlled concurrency
- horizontal scaling

---

## Why not BackgroundTasks?

A process restart can interrupt work.

---

## Why not Kafka?

Kafka solves a broader event-streaming problem than R1 currently has.

---

## Change trigger

Kafka becomes attractive when:

```text
Multiple consumers
+
Durable events
+
Replay
+
High event volume
```

---

# 7. ADR-03 — POSTGRESQL VS NOSQL

## Problem

Career information has relationships.

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

---

## Alternatives

### PostgreSQL

Pros:

- ACID
- relationships
- constraints
- transactions
- mature SQL
- vector extension

Cons:

- schema evolution needs discipline
- very large specialized workloads may need additional systems

### MongoDB

Pros:

- flexible documents
- easy document modelling

Cons:

- less natural for highly relational career analytics
- still need vector capability

---

## Decision

### PostgreSQL

---

## Why?

Career data is relational first.

---

# 8. ADR-04 — PGVECTOR VS DEDICATED VECTOR DB

## Alternatives

### PostgreSQL + pgvector

Pros:

- one primary data boundary
- joins between vectors and metadata
- transactional consistency
- simpler operations

Cons:

- vector and relational workload share resources

### PostgreSQL + Pinecone

Pros:

- specialized vector infrastructure
- independent scaling

Cons:

- two systems
- synchronization
- dual-write concerns

### MongoDB + Qdrant

Pros:

- flexible documents + specialized vector search

Cons:

- more infrastructure
- two persistence systems

---

## Decision

### PostgreSQL + pgvector

---

## Why?

R1/R2 vector workload is part of the career-data domain.

The attached HLDs explicitly choose PostgreSQL + pgvector over separate vector infrastructure. 

---

## Change trigger

Introduce dedicated vector infrastructure when:

- vector workload dominates DB
- vector latency becomes unacceptable
- scale exceeds practical PostgreSQL capacity
- required vector functionality is missing

---

# 9. ADR-05 — PDF EXTRACTION

## Alternatives

| Technology | Strength | Weakness |
|---|---|---|
| Direct LLM PDF | Simple | Cost/less deterministic |
| pypdf | Lightweight | Layout limitations |
| pdfplumber | Better layout | More processing |
| OCR | Scanned PDF | Cost/complexity |

---

## Decision

### pypdf + pdfplumber

---

## Why?

Good R1 balance.

---

## OCR trigger

Introduce OCR when real resume samples show a meaningful percentage of scanned/image-only documents.

---

# 10. ADR-06 — FREE-FORM LLM VS STRUCTURED OUTPUT

## Free-form

Pros:

- easy

Cons:

- unpredictable
- difficult validation
- difficult persistence

---

## JSON mode

Better, but still requires validation.

---

## Schema-constrained output

Pros:

- predictable
- testable
- validated
- easier persistence

Cons:

- requires schema design

---

## Decision

### Structured output + Pydantic validation

---

## Core principle

> The LLM can propose data. The application decides whether that data becomes system state.

---

# 11. ADR-07 — LLM VS DETERMINISTIC MATCHING

This is especially important for R2.

## Option A — LLM-only matching

Pros:

- flexible
- natural language reasoning

Cons:

- inconsistent
- difficult to reproduce
- expensive
- difficult to test

---

## Option B — Deterministic only

Pros:

- predictable
- cheap
- testable

Cons:

- misses semantic relationships

---

## Decision

### Hybrid

```text
Exact Match
      +
Semantic Similarity
      +
Deterministic Score
      +
LLM Explanation
```

The attached HLD v0.1 explicitly emphasizes deterministic matching coupled with targeted LLM reasoning.

---

# 12. ADR-08 — RAG

## When?

R3.

---

## Why not R1?

R1 has no substantial external knowledge-retrieval problem.

It is primarily:

```text
Resume
 ↓
Structured Career Profile
```

---

## Why not R2?

R2 is primarily:

```text
Profile
+
Target Role
 ↓
Gap Analysis
```

Retrieval can remain limited.

---

## Why R3?

Now we have:

```text
Market
+
Roles
+
Learning
+
Career
+
Historical knowledge
```

RAG becomes genuinely valuable.

---

# 13. ADR-09 — NAIVE RAG VS FILTERED RAG

## Naive Top-K

```text
Query
 ↓
Top-K vectors
 ↓
LLM
```

### Pros

- simple
- fast to build

### Cons

- noisy
- generic
- domain mixing

---

## Multi-domain filtered RAG

```text
User
 │
 ├── Career
 ├── Market
 ├── Role
 └── Learning
       ↓
Filtered Retrieval
       ↓
Context Assembly
       ↓
LLM
```

### Pros

- more relevant
- explainable retrieval domains
- better context control

### Cons

- more complexity
- retrieval evaluation required

---

## Decision

### R3 — Multi-domain filtered RAG

This is consistent with the broader HLD's RAG design.

---

# 14. ADR-10 — AGENTS

## Alternatives

### Deterministic workflows

Pros:

- predictable
- testable
- cheap

Cons:

- limited autonomy

### Agents

Pros:

- dynamic planning
- tool selection
- multi-step execution

Cons:

- non-determinism
- cost
- complex failure handling
- difficult evaluation

---

## Decision

### R1–R3: No agents

### R4: Candidate

---

## Trigger

Use agents when the product genuinely needs:

> autonomous multi-step planning and tool use.

---

# 15. ADR-11 — MCP

## Why not R1?

No external tool ecosystem requirement.

---

## Why R4?

R4 may need standardized connections to:

- job sources
- learning systems
- external knowledge
- productivity systems
- career tools

---

## Decision

### R4 candidate

---

# 16. ADR-12 — SEMANTIC CACHE

The broader HLD proposes semantic caching to reduce repeated LLM work and latency.

---

## Alternatives

### No cache

Simple.

### Exact cache

Useful for identical queries.

### Semantic cache

Useful for semantically similar queries.

---

## Decision

Do not introduce semantic caching until we measure:

- repeated query rate
- LLM cost
- latency
- cache hit opportunity

---

## Trigger

If repeated semantic requests become a material cost/latency driver:

```text
Redis
+
semantic similarity
```

can be introduced.

---

# 17. ADR-13 — MARKET CLUSTERING

## Problem

The market may evolve faster than manually defined roles.

---

## Option

Use embeddings + clustering to identify emerging role patterns.

Example:

```text
500 JDs
 ↓
Embeddings
 ↓
Cluster
 ↓
LLM interpretation
 ↓
Potential new role
```

The broader HLD specifically proposes DBSCAN-style clustering of market JDs as an expansion capability.

---

## Decision

### R3/R4

Not R1.

---

# 18. ADR-14 — SELF-LEARNING

## R1

Capture:

- user corrections
- profile changes
- feedback

but do not automatically alter the intelligence model.

---

## R4

Use:

```text
Recommendation
 ↓
User feedback
 ↓
Career outcome
 ↓
Evaluation
 ↓
Improved recommendation
```

---

## Terminology

Use:

> Feedback-driven recommendation learning

rather than automatically calling it RLHF.

---

# 19. ADR-15 — DOCKER COMPOSE VS KUBERNETES

## Docker Compose

Pros:

- simple
- reproducible
- ideal local environment
- low operational overhead

Cons:

- limited orchestration

---

## Kubernetes

Pros:

- autoscaling
- self-healing
- production orchestration
- service discovery

Cons:

- operational complexity

---

## Decision

### R1 — Docker Compose

---

## Trigger

Move to Kubernetes/OpenShift when:

- production container count grows
- autoscaling becomes important
- self-healing becomes necessary
- platform standards require it
- operational complexity justifies orchestration

---

# 20. ADR-16 — KAFKA

## Why not R1?

No requirement for a durable enterprise event stream.

---

## Redis is enough for:

```text
Job queue
Retry
Worker coordination
```

---

## Kafka becomes useful for:

```text
Career events
Market events
Learning events
Recommendation events
Feedback events
```

with:

- multiple consumers
- replay
- durable history
- high throughput

---

# 21. ADR-17 — MICROSERVICE EVOLUTION

The transition should never be:

```text
R4 arrived
↓
Let's use microservices
```

Instead:

```text
Measure architectural pressure
          ↓
Identify bounded context
          ↓
Prove independent deployment/scaling need
          ↓
Extract service
```

---

# 22. ADR-18 — OBJECT STORAGE

The source documents discuss resume intake/file handling, but they do not establish a definitive R1 object-storage product.

Therefore:

### Decision

Keep the abstraction:

```text
Object/File Storage
```

until the implementation requirements are finalized.

Do not prematurely claim:

```text
S3
```

as a locked architectural choice.

---

# 23. ADR-19 — EMBEDDING MODEL

The attached software-stack document proposes OpenAI `text-embedding-3-small` with 1536-dimensional vectors.

Our architecture decision should be:

> The embedding model is a configurable provider/model decision; pgvector dimensionality must match the selected model.

Do not hard-code the vector dimension as a universal architecture truth.

---

# 24. ADR-20 — FAILURE HANDLING

## Failure principle

> **Fail the operation, not the entire application.**

---

## LLM failure

```text
LLM unavailable
 ↓
Job delayed
 ↓
Retry
 ↓
Profile remains accessible
```

---

## Worker failure

```text
Worker crash
 ↓
Retry
```

---

## Database failure

```text
Persistence failure
 ↓
Controlled error
 ↓
Retry where safe
```

---

## Invalid LLM output

```text
LLM
 ↓
Schema validation
 ↓
Reject
 ↓
Retry / fail
```

---

# 25. ADR-21 — SECURITY

Security architecture evolves with the product.

## R1

- authentication
- authorization
- TLS
- encryption
- secret management
- safe logging
- file validation

## R2

- role/JD isolation
- stronger access controls

## R3

- prompt injection defense
- source trust
- retrieval controls
- content filtering

## R4

- agent permissions
- external-tool authorization
- audit trails
- fine-grained policies

---

# 26. ADR-22 — OBSERVABILITY

## R1

```text
Logs
Metrics
Traces
```

## R2

Add:

```text
Matching quality
Gap-analysis latency
```

## R3

Add:

```text
Retrieval quality
RAG latency
Token cost
Recommendation acceptance
```

## R4

Add:

```text
Career outcomes
Recommendation usefulness
Agent success
Tool success
Feedback quality
```

---

# 27. ADR-23 — SCALABILITY

## R1

Scale:

```text
API independently
Workers independently
```

Example:

```text
Traffic
 ↓
API x N
 ↓
Redis
 ↓
Worker x N
 ↓
PostgreSQL
```

---

## R2

Scale:

- JD ingestion
- matching
- vector search

---

## R3

Scale:

- market ingestion
- RAG
- learning ingestion
- retrieval
- caching

---

## R4

Potentially:

- Kubernetes
- Kafka
- microservices
- dedicated vector DB
- distributed caches

---

# 28. ARCHITECTURE CONTRAST — WHAT WE CHOSE

This is the section to memorize.

| Question | Chosen | Alternative | Why chosen |
|---|---|---|---|
| Application architecture | Modular monolith | Microservices | Boundaries not proven |
| Async | Redis + Celery | Kafka | Simpler and sufficient |
| DB | PostgreSQL | MongoDB | Relational domain |
| Vector | pgvector | Pinecone/Qdrant | One persistence boundary |
| PDF | pypdf/pdfplumber | OCR | Simpler initial requirement |
| AI output | Structured | Free-form | Reliability |
| Matching | Hybrid | LLM-only | Deterministic/testable |
| RAG | R3 | R1 | Knowledge retrieval not yet needed |
| RAG strategy | Filtered multi-domain | Naive Top-K | Better relevance |
| Agents | R4 candidate | R1 | Too much non-determinism |
| MCP | R4 candidate | R1 | No integration requirement |
| Deployment | Docker Compose | Kubernetes | Lower R1 complexity |
| Events | Redis queue | Kafka | No event-stream requirement |
| Learning | Feedback-driven | RLHF | More accurate architectural terminology |
| Vector DB | pgvector | Dedicated DB | Current scale/domain |
| Cache | Demand-driven | Immediate semantic cache | Avoid premature complexity |

---

# 29. THE MOST IMPORTANT TRADE-OFFS

## Simplicity vs scalability

We choose simplicity initially.

But:

```text
Modular Monolith
+
Async workers
+
Stateless API
```

gives meaningful horizontal scalability without immediately distributing the whole system.

---

## Consistency vs specialized infrastructure

PostgreSQL + pgvector sacrifices some specialized vector-database flexibility in exchange for:

> simpler consistency and operations.

---

## Determinism vs intelligence

We do not ask the LLM to control everything.

Instead:

```text
LLM
=
semantic intelligence

Code
=
system control
```

---

## Immediate capability vs future flexibility

We deliberately defer:

- Kafka
- Kubernetes
- microservices
- agents
- MCP
- RAG

but keep the architecture capable of introducing them later.

---

# 30. ARCHITECTURE CHANGE TRIGGER TABLE

| Technology | Introduce when... |
|---|---|
| Microservices | Independent deployment/scaling/ownership required |
| Kafka | Durable event streaming/replay/multiple consumers required |
| Kubernetes | Container orchestration complexity becomes material |
| Dedicated vector DB | pgvector becomes vector bottleneck |
| RAG | Multiple knowledge domains require retrieval |
| Agents | Autonomous multi-step planning becomes necessary |
| MCP | Standardized external tool integration becomes necessary |
| Semantic cache | Repeated semantic requests materially affect cost/latency |
| OCR | Real resumes require scanned-document processing |
| Read replicas | Read workload materially exceeds primary capacity |
| Partitioning | Data size/query patterns justify it |
| Multi-region | Availability/latency/business requirements justify it |

---

# 31. SOLUTION ARCHITECT INTERVIEW RUNBOOK

## Q1. Why didn't you start with microservices?

### Answer

> “Because our domain boundaries were still evolving. Starting with microservices would introduce distributed failure, network communication and deployment complexity before we had evidence that independent deployment or scaling was necessary. I chose a modular monolith with explicit domain boundaries and kept service extraction as a trigger-based evolution.”

---

## Q2. Why Redis?

> “Resume processing involves long-running PDF and LLM operations. I needed asynchronous buffering, retries and independent worker scaling. Redis with Celery provides those capabilities with less operational complexity than Kafka.”

---

## Q3. Why not Kafka?

> “Kafka is a strong event-streaming platform, but R1 has a job-processing problem rather than a durable event-streaming problem. If we later require replay, multiple independent consumers, durable event history or high event throughput, Kafka becomes a candidate.”

---

## Q4. Why PostgreSQL?

> “The core domain is relational: users, profiles, experiences, skills, evidence and roles. We need transactions, constraints and relationships.”

---

## Q5. Why pgvector?

> “We need semantic similarity, but the vector data is closely associated with relational career data. pgvector lets us keep the initial persistence boundary simple.”

---

## Q6. Why not Pinecone or Qdrant?

> “They are valid alternatives. I rejected them initially because they introduce another persistence system and synchronization boundary. I would revisit the decision if vector workload becomes a bottleneck or specialized capabilities justify the operational cost.”

---

## Q7. Why no RAG in R1?

> “R1 is primarily a structured extraction problem. RAG becomes valuable once we have multiple knowledge domains such as market data, role requirements and learning resources, which is why it enters in R3.”

---

## Q8. Why not use an agent?

> “The early workflows are deterministic. Agents introduce planning and non-determinism before there is a genuine autonomous workflow requirement.”

---

## Q9. What if the LLM goes down?

> “Because processing is asynchronous, the API remains available. The job remains pending or retryable, while existing career profiles remain accessible.”

---

## Q10. What if 1,000 resumes arrive simultaneously?

> “The API accepts and queues them rather than processing synchronously. Redis buffers the workload, workers process it at controlled concurrency and LLM rate limits are respected.”

---

## Q11. How do you prevent duplicate processing?

> “I use document fingerprints, idempotency keys, uniqueness constraints and transactional state transitions.”

---

## Q12. How would you scale the system?

> “First horizontally scale stateless API instances and workers independently. Then optimize PostgreSQL with indexes, connection pooling and query optimization. Only after measuring actual bottlenecks would I consider replicas, partitioning, dedicated vector infrastructure or microservices.”

---

## Q13. How do you secure an AI application?

> “I treat both user documents and AI outputs as untrusted inputs. Authentication and authorization are enforced before access, sensitive data is minimized, prompts and outputs are validated, secrets are externalized, and sensitive content is excluded from logs.”

---

## Q14. How do you make LLM output reliable?

> “I don't allow free-form model output to directly become system state. I use structured schemas, Pydantic validation, evidence checks and deterministic persistence logic.”

---

## Q15. How do you distinguish AI inference from facts?

> “I store evidence separately. The system distinguishes source facts, inferred information and recommendations so that users can understand what came from their resume versus what the model inferred.”

---

# 32. THE ARCHITECTURE STORY IN 60 SECONDS

Memorize this.

> “FuturePath AI starts with a modular FastAPI monolith because the domain is evolving and we don't yet need independent service boundaries. Resume ingestion is asynchronous because PDF parsing and LLM inference are long-running, so Redis and Celery decouple the API from workers. PostgreSQL is the transactional source of truth because the career domain is relational, while pgvector adds semantic similarity without introducing another persistence system. R1 focuses on trustworthy career-profile extraction. R2 adds deterministic plus semantic target-role gap analysis. R3 introduces market intelligence and multi-domain RAG when external knowledge becomes meaningful. R4 adds feedback-driven continuous intelligence and may introduce agents, MCP, Kafka, microservices and Kubernetes only where measurable requirements justify them.”

---

# 33. THE ARCHITECTURE STORY IN ONE DIAGRAM

```text
                    ┌─────────────────────┐
                    │        USER         │
                    └──────────┬──────────┘
                               │
                               ▼
                       ┌──────────────┐
                       │   Next.js    │
                       └──────┬───────┘
                              │
                              ▼
                ┌───────────────────────────┐
                │     FastAPI Monolith      │
                │                           │
                │ Career │ Role │ Market    │
                │ Gap    │ Learning         │
                └───────┬───────────┬───────┘
                        │           │
                        ▼           ▼
                    ┌───────┐ ┌──────────────┐
                    │ Redis │ │ PostgreSQL   │
                    └───┬───┘ │ + pgvector   │
                        │      └──────▲───────┘
                        ▼             │
                    ┌─────────┐      │
                    │ Workers │──────┘
                    └────┬────┘
                         │
             ┌───────────┼────────────┐
             ▼           ▼            ▼
            PDF         LLM       Embeddings
                         │
                         ▼
                    RAG in R3
                         │
                         ▼
                 Recommendations
                         │
                         ▼
                      Feedback
                         │
                         ▼
              Continuous Intelligence
                         │
                         ▼
          Future Distributed Architecture
```

---

# 34. FINAL ARCHITECTURE PRINCIPLE

The most important sentence in this entire document is:

> **We don't choose architecture based on what technology is popular; we choose it based on the problem, constraints and measurable architectural pressure.**

Therefore:

```text
R1
Simple + Reliable

R2
Analytical + Deterministic

R3
Context-Aware + Retrieval-Driven

R4
Continuous + Adaptive + Potentially Distributed
```

---

# 35. FINAL DECISION

The current baseline is:

```text
                 FUTUREPATH AI
                       │
                       ▼
                Next.js / React
                       │
                       ▼
             FastAPI Modular Monolith
                       │
             ┌─────────┴──────────┐
             ▼                    ▼
           Redis              PostgreSQL
             │                 + pgvector
             ▼
        Celery Workers
             │
      ┌──────┼─────────┐
      ▼      ▼         ▼
     PDF     LLM    Embeddings
             │
             ▼
           RAG
          (R3)
             │
             ▼
      Recommendations
             │
             ▼
          Feedback
             │
             ▼
     Continuous Intelligence
             │
             ▼
   Distributed evolution
   only when justified
```

This is the **architecture baseline**.

Any future change must be based on evidence, documented here, and accompanied by a clear explanation of:

**what changed → why it changed → what we considered → what we chose → what trade-off we accepted.**