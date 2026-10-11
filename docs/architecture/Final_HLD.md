
# FuturePath AI
## Final End-to-End High-Level Design

**Product:** FuturePath AI  
**Architecture Scope:** Release 1 → Release 4  
**Document Type:** Master Product & Architecture HLD  
**Status:** Baseline / Living Architecture  
**Purpose:** Single authoritative end-to-end architecture document

---

# 1. Executive Summary

FuturePath AI is a personal career and future intelligence platform.

Its fundamental question is:

> **“Given who I am today, what is happening in the market, where am I falling short, what should I learn next, and which opportunities are relevant to me?”**

FuturePath AI progressively evolves from understanding a person's current career profile into a continuous career intelligence system.

The architecture deliberately evolves through four releases:

```text
R1
Career Profile Intelligence
        ↓
R2
Career Gap & Target Role Intelligence
        ↓
R3
Market & Learning Intelligence
        ↓
R4
Continuous Personal Career Intelligence
```

The architecture is intentionally **progressive**.

We do not deploy the R4 architecture on Day 1.

Instead:

> **Complexity is introduced only when the product requirements, workload or operational characteristics justify it.**

---

# 2. Product Vision

FuturePath AI combines four dimensions:

```text
┌─────────────────────┐
│       PERSON        │
│ Resume              │
│ Experience          │
│ Skills              │
│ Career history      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    INTELLIGENCE     │
│ Profile analysis    │
│ Gap analysis        │
│ Semantic matching   │
│ Recommendations     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       MARKET        │
│ Jobs                │
│ Roles               │
│ Skills              │
│ Trends              │
│ Requirements        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       ACTION        │
│ Skills to learn     │
│ Learning paths      │
│ Opportunities       │
│ Career progression  │
└─────────────────────┘
```

---

# 3. Architectural Principles

## 3.1 Justified Complexity

Do not introduce technology because it is fashionable.

Every major architectural decision follows:

```text
Problem
   ↓
Constraints
   ↓
Alternatives
   ↓
Pros / Cons
   ↓
Trade-off
   ↓
Decision
   ↓
Change Trigger
```

---

## 3.2 Deterministic Over Generative

LLMs should primarily:

- extract
- interpret
- summarize
- reason

Deterministic application logic should:

- validate
- compare
- calculate
- rank
- persist
- enforce rules

---

## 3.3 Asynchronous by Default

Long-running operations should not block user-facing HTTP requests.

Examples:

- PDF extraction
- LLM inference
- embeddings
- large-scale job ingestion
- market processing
- learning-resource ingestion

---

## 3.4 Evidence Before Intelligence

FuturePath should distinguish:

```text
Fact
↓
Inference
↓
Recommendation
```

Example:

**Fact**

> User worked with Kubernetes.

**Inference**

> User likely has practical Kubernetes experience.

**Recommendation**

> Advanced Kubernetes networking may be useful for the target role.

---

## 3.5 PostgreSQL as the Initial Source of Truth

The career domain is highly relational.

Therefore:

```text
Users
Profiles
Experiences
Skills
Evidence
Roles
Requirements
Gaps
Feedback
```

remain relational data.

Vectors are initially stored alongside this data using pgvector.

---

## 3.6 Evolution Over Premature Distribution

R1 starts with:

```text
Modular Monolith
```

not:

```text
Microservices
```

Distributed architecture is introduced only when measurable architectural pressure appears.

---

# 4. Release Strategy

| Release | Product Question | Main Capability |
|---|---|---|
| R1 | What do we know about me? | Career profile |
| R2 | What am I missing for a target role? | Gap analysis |
| R3 | What does the market demand and what should I learn? | Market + learning intelligence |
| R4 | How can FuturePath continuously guide my career? | Continuous intelligence |

---

# 5. RELEASE 1 — Career Profile Intelligence

## 5.1 Goal

Answer:

> **“What do we understand about my career today?”**

---

## 5.2 User Journey

```text
Upload Resume
      ↓
Validate
      ↓
Store
      ↓
Create Processing Job
      ↓
Async Worker
      ↓
Extract PDF Text
      ↓
Normalize Text
      ↓
Structured LLM Extraction
      ↓
Schema Validation
      ↓
Evidence Validation
      ↓
Skill Normalization
      ↓
Generate Embeddings
      ↓
PostgreSQL + pgvector
      ↓
Career Profile
      ↓
User Review
      ↓
User Correction
```

---

# 6. R1 Functional Scope

### Authentication

Users can securely access their profile.

### Resume ingestion

Users can upload resumes.

### Processing

Resume processing occurs asynchronously.

### Extraction

Extract:

- career summary
- companies
- roles
- dates
- responsibilities
- skills
- education
- evidence

### Skill intelligence

For each skill:

- canonical skill
- evidence
- confidence
- estimated proficiency
- semantic embedding

### User correction

The user can correct extracted information.

### Processing status

```text
PENDING
   ↓
PROCESSING
   ↓
COMPLETED

or

FAILED
```

---

# 7. R1 Architecture

```text
                         ┌───────────────┐
                         │     USER      │
                         └───────┬───────┘
                                 │ HTTPS
                                 ▼
                       ┌──────────────────┐
                       │ Next.js / React  │
                       └────────┬─────────┘
                                │ REST
                                ▼
                  ┌──────────────────────────┐
                  │        FastAPI           │
                  │     Modular Monolith     │
                  │                          │
                  │ Auth                     │
                  │ Resume                   │
                  │ Profile                  │
                  │ Skills                   │
                  │ Jobs                     │
                  └───────┬───────────┬──────┘
                          │           │
                       enqueue      database
                          │           │
                          ▼           ▼
                     ┌────────┐ ┌──────────────┐
                     │ Redis  │ │ PostgreSQL   │
                     │ Broker │ │ + pgvector   │
                     └───┬────┘ └──────▲───────┘
                         │              │
                         ▼              │
                  ┌──────────────┐     │
                  │ Celery       │─────┘
                  │ Worker Pool  │
                  │              │
                  │ PDF Parser   │
                  │ LLM          │
                  │ Validation   │
                  │ Embeddings   │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ External AI  │
                  │ LLM + Embed  │
                  └──────────────┘
```

---

# 8. R1 AI Pipeline

```text
PDF
 ↓
File Validation
 ↓
PDF Extraction
 ↓
Text Normalization
 ↓
Structured LLM
 ↓
Pydantic Validation
 ↓
Evidence / Provenance
 ↓
Skill Normalization
 ↓
Embedding
 ↓
PostgreSQL + pgvector
```

Initial PDF technology:

- pypdf
- pdfplumber

OCR is deferred until actual input data proves it is required.

The attached stack document explicitly uses pypdf/pdfplumber for local extraction and structured LLM output for reliable entity creation.

---

# 9. R1 Data Model

Core entities:

```text
User
 │
 └── CareerProfile
       │
       ├── Experience
       │
       ├── Education
       │
       └── ProfileSkill
              │
              ├── Skill
              │
              └── SkillEvidence

User
 │
 └── Resume
       │
       └── ProcessingJob
```

Important principle:

> Resume binary storage and relational career metadata should be treated as separate concerns.

The exact object-storage technology remains an implementation decision until R1 storage requirements are finalized.

---

# 10. R1 Reliability

The system must tolerate:

- corrupted PDF
- parser failure
- LLM timeout
- LLM unavailable
- malformed LLM response
- embedding failure
- Redis failure
- worker crash
- PostgreSQL failure
- duplicate submission

---

## Retry

Transient failure:

```text
Retry
 ↓
Backoff
 ↓
Bounded Attempts
```

Permanent failure:

```text
FAILED
```

---

## Idempotency

Use:

- document fingerprint
- job identifier
- uniqueness constraints
- transactional persistence
- idempotency key where appropriate

Goal:

> A retry must not create duplicate career data.

---

# 11. R1 Security

Security starts from R1.

Controls include:

- TLS
- authentication
- authorization
- input validation
- file validation
- rate limiting
- least privilege
- encrypted storage
- secure secret handling
- sanitized logs
- deletion capability
- auditability

Never log:

- resume content
- access tokens
- API keys
- passwords
- sensitive LLM prompts

---

# 12. R1 Observability

### Logs

Application events without sensitive content.

### Metrics

- API latency
- p95/p99
- request rate
- error rate
- queue depth
- task age
- retries
- processing time
- LLM latency
- LLM failures
- embedding latency
- DB latency
- extraction success

### Tracing

```text
request_id
   ↓
job_id
   ↓
worker task
   ↓
LLM request
   ↓
database transaction
```

---

# 13. R1 Deployment

Local development:

```text
Docker Compose
```

Services:

```text
Frontend
API
Worker
Redis
PostgreSQL + pgvector
```

CI/CD:

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
Build
 ↓
Deploy
```

---

# 14. RELEASE 2 — Career Gap & Target Role Intelligence

## Goal

Answer:

> **“Given a target role, what am I missing and how significant is the gap?”**

---

# 15. R2 New Capabilities

R2 adds:

- target role
- target capability model
- job description ingestion
- requirement extraction
- skill normalization
- exact matching
- semantic matching
- gap scoring
- evidence-backed explanations
- prioritized recommendations
- role comparison

---

# 16. R2 Architecture

```text
                  R1 Career Profile
                         │
                         ▼
                  ┌──────────────┐
                  │ Target Role  │
                  └──────┬───────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Requirement      │
                │ Extraction       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Skill             │
                │ Normalization     │
                └────────┬─────────┘
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Exact Matching        Semantic Matching
             │                       │
             └───────────┬───────────┘
                         ▼
                 ┌──────────────┐
                 │ Gap Engine   │
                 └──────┬───────┘
                        ▼
                Prioritized Gaps
```

---

# 17. R2 Matching Model

R2 should not rely on an LLM alone.

Use:

```text
Exact Identity
      +
Semantic Similarity
      +
Deterministic Scoring
      +
Evidence
```

Example:

```text
Target: Kubernetes

User:
Kubernetes → exact match

Target:
Distributed Systems

User:
Kafka + Kubernetes + system design
→ semantic adjacency
```

---

# 18. R2 Gap Categories

```text
Strong Match
Partial Match
Adjacent Skill
Missing Skill
Unknown Evidence
```

Important:

> Unknown evidence does not automatically mean the user does not possess the skill.

---

# 19. R2 Output

Example:

```text
Target Role: Solution Architect

Strong:
✓ Kubernetes
✓ Java
✓ Distributed Systems

Partial:
~ Cloud Architecture

Gap:
✗ Event-driven Architecture

Priority:
HIGH
```

---

# 20. RELEASE 3 — Market & Learning Intelligence

## Goal

Answer:

> **“What is the market demanding, where do I stand against it, and what should I learn next?”**

---

# 21. R3 New Capabilities

R3 adds:

- job-description ingestion at scale
- market requirements
- market skill taxonomy
- market trends
- role clustering
- market intelligence
- RAG
- learning-resource ingestion
- educational RAG
- market-aware recommendations
- personalized learning paths
- semantic caching when justified

---

# 22. R3 Architecture

```text
                    ┌──────────────────┐
                    │ Market JDs       │
                    └────────┬─────────┘
                             ▼
                   ┌──────────────────┐
                   │ JD Extraction    │
                   └────────┬─────────┘
                            ▼
                   ┌──────────────────┐
                   │ Skill Taxonomy   │
                   └────────┬─────────┘
                            ▼
                  ┌─────────────────────┐
                  │ Market Intelligence │
                  └─────────┬───────────┘
                            │
                 ┌──────────┼───────────┐
                 ▼          ▼           ▼
              Skills     Market      Role
                        Trends      Clusters
                 │          │           │
                 └──────────┼───────────┘
                            ▼
                      RAG Retrieval
                            │
                            ▼
                  ┌──────────────────┐
                  │ Recommendation   │
                  │ Engine           │
                  └────────┬─────────┘
                           ▼
                  Personalized Plan
```

---

# 23. R3 RAG

RAG is intentionally introduced here rather than R1.

By R3 there are meaningful knowledge domains:

```text
Career Profile
      +
Role Requirements
      +
Market Requirements
      +
Historical Career Paths
      +
Learning Resources
```

---

## Retrieval architecture

Instead of:

```text
Query
 ↓
Top-K vectors
 ↓
LLM
```

use:

```text
User Context
     │
     ├── Career knowledge
     ├── Market knowledge
     ├── Role knowledge
     └── Learning knowledge
              │
              ▼
       Filtered Retrieval
              │
              ▼
        Context Assembly
              │
              ▼
              LLM
```

The comprehensive attached HLD explicitly proposes multi-domain filtered RAG across skills, market requirements and historical paths.

---

# 24. R3 Learning Intelligence

The system should move beyond:

> “Learn Kubernetes.”

toward:

> “You are missing Kubernetes Pod Lifecycle knowledge. Here is the relevant learning material and why it matters for your target role.”

Learning resources may eventually include:

- documentation
- courses
- articles
- transcripts
- educational content

Educational RAG is a future capability identified in the broader HLD.

---

# 25. R3 Market Intelligence

The system can calculate:

```text
Skill frequency
Skill importance
Role demand
Emerging skills
Skill combinations
Role clusters
```

Potential clustering:

```text
Job Descriptions
       ↓
Embeddings
       ↓
Clustering
       ↓
Emerging Role Patterns
```

For example:

```text
LLM
+
RAG
+
LangChain
+
Python
```

may reveal an emerging role pattern.

The broader HLD proposes DBSCAN-style market clustering as a future intelligence capability.

---

# 26. RELEASE 4 — Continuous Personal Career Intelligence

## Goal

Become a continuously improving personal career intelligence system.

Answer:

> **“Based on my current career, market changes, actions and outcomes, what should I do next?”**

---

# 27. R4 Capabilities

R4 may introduce:

- continuous feedback
- user ratings
- career progression tracking
- observed career outcomes
- feedback-driven recommendation learning
- advanced market intelligence
- autonomous workflows where justified
- MCP/tool calling where justified
- agents where justified
- event-driven architecture where justified
- Kafka where justified
- microservices where justified
- Kubernetes/OpenShift where justified
- dedicated vector infrastructure where justified

---

# 28. R4 Feedback Loop

```text
Recommendation
      ↓
User Action
      ↓
Learning / Application / Job Search
      ↓
Career Outcome
      ↓
User Feedback
      ↓
Observed Progress
      ↓
Recommendation Evaluation
      ↓
Improved Recommendation
```

Important terminology:

> **Feedback-driven recommendation learning**

Do not automatically call this RLHF unless a genuine reinforcement-learning/human-feedback training system is implemented.

The broader HLD describes both implicit career progression and explicit user ratings as inputs into a learning loop.

---

# 29. R4 Agents

Agents are not automatically required.

They become useful when FuturePath needs autonomous multi-step workflows such as:

```text
Find target role
 ↓
Research market
 ↓
Analyze user's gap
 ↓
Search learning resources
 ↓
Build learning plan
 ↓
Evaluate progress
 ↓
Reassess
```

Until that complexity exists:

> deterministic workflows are preferred.

---

# 30. R4 MCP

MCP/tool calling becomes useful when FuturePath needs standardized access to external tools/data sources.

Potential examples:

```text
Job platforms
Learning platforms
Career data
Calendars
Productivity tools
External knowledge
```

MCP should be introduced because of an integration requirement, not simply because it is available.

---

# 31. R4 Event Architecture

Potential evolution:

```text
                    Event Bus
                       │
        ┌──────────────┼───────────────┐
        ▼              ▼               ▼
 Career Service   Market Service   Learning Service
```

Kafka becomes a candidate when we have:

- multiple independent consumers
- durable event history
- replay
- high event volume
- independent event-driven services

---

# 32. R4 Microservices Evolution

The modular monolith may eventually evolve into:

```text
                API Gateway
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 Career Service   Market Service  Learning Service
      │              │              │
      └──────────────┼──────────────┘
                     ▼
              Event Infrastructure
```

But this is **trigger-based**, not predetermined.

---

# 33. Complete Architecture Evolution

```text
R1
┌────────────────────────────────────┐
│ Modular Monolith                   │
│ FastAPI                            │
│ Redis + Celery                     │
│ PostgreSQL + pgvector              │
│ Structured AI extraction           │
└────────────────────────────────────┘
                  │
                  ▼
R2
┌────────────────────────────────────┐
│ + Target Roles                     │
│ + JD Processing                    │
│ + Hybrid Matching                  │
│ + Gap Analysis                     │
└────────────────────────────────────┘
                  │
                  ▼
R3
┌────────────────────────────────────┐
│ + Market Intelligence              │
│ + RAG                              │
│ + Learning Knowledge               │
│ + Role Clustering                  │
│ + Personalized Learning            │
└────────────────────────────────────┘
                  │
                  ▼
R4
┌────────────────────────────────────┐
│ + Continuous Feedback              │
│ + Career Outcomes                  │
│ + Advanced Intelligence            │
│ + Agents where justified           │
│ + MCP where justified              │
│ + Events where justified           │
│ + Distributed architecture         │
└────────────────────────────────────┘
```

---

# 34. Cross-Release Data Architecture

The logical evolution is:

```text
                    USER
                     │
                     ▼
              CAREER PROFILE
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      EXPERIENCE   SKILLS    EVIDENCE
                     │
                     ▼
                TARGET ROLE
                     │
                     ▼
              REQUIREMENTS
                     │
                     ▼
                GAP ANALYSIS
                     │
                     ▼
              MARKET CONTEXT
                     │
                     ▼
             LEARNING CONTENT
                     │
                     ▼
             RECOMMENDATIONS
                     │
                     ▼
                USER ACTION
                     │
                     ▼
              CAREER OUTCOME
                     │
                     └──────────────► FEEDBACK
```

---

# 35. Storage Evolution

## R1

```text
PostgreSQL + pgvector
```

## R2

Same primary architecture.

Additional entities:

```text
TargetRole
RoleRequirement
GapAnalysis
```

## R3

Additional knowledge domains:

```text
MarketRequirement
MarketSkill
JobDescription
LearningResource
LearningChunk
```

## R4

Potential supporting systems:

```text
Event Store / Kafka
Dedicated vector infrastructure
Caches
Analytics/feature stores
```

Only when justified.

---

# 36. Scaling Evolution

## R1

```text
API
 ↓
Redis
 ↓
Workers
 ↓
PostgreSQL
```

Scale API and workers independently.

---

## R2

Increase:

- matching workload
- JD ingestion
- vector queries
- database read workload

---

## R3

Introduce:

- worker pools by workload
- market ingestion workers
- RAG retrieval optimization
- caching
- potentially read replicas
- potentially specialized vector infrastructure

---

## R4

Potentially:

- Kubernetes/OpenShift
- autoscaling
- Kafka
- independent services
- specialized databases
- advanced caching
- multi-region architecture if required

---

# 37. Security Evolution

Security remains a cross-release concern.

R1:

```text
Authentication
Authorization
Encryption
Secrets
Safe logging
```

R2:

```text
Role/JD data isolation
```

R3:

```text
External knowledge provenance
Prompt injection defense
Source trust
Content filtering
```

R4:

```text
Tool authorization
Agent permissions
External-system access control
Audit trails
Fine-grained policies
```

---

# 38. Reliability Evolution

R1:

```text
Retry
Idempotency
Failure states
Worker isolation
```

R2:

```text
Matching failure isolation
```

R3:

```text
RAG fallback
Source failure handling
Market ingestion recovery
```

R4:

```text
Event replay
Dead-letter processing
Distributed failure isolation
Disaster recovery
Potential multi-region recovery
```

---

# 39. Observability Evolution

R1:

```text
Logs
Metrics
Traces
```

R2:

```text
Matching quality
Gap-analysis latency
```

R3:

```text
Retrieval quality
RAG latency
Token cost
Recommendation acceptance
```

R4:

```text
Recommendation usefulness
Career outcome metrics
Feedback quality
Agent/tool success
End-to-end business KPIs
```

---

# 40. Complete FuturePath Architecture

```text
                              USER
                                │
                                ▼
                         ┌─────────────┐
                         │  Next.js    │
                         └──────┬──────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │ FuturePath API         │
                    │                        │
                    │ Career                 │
                    │ Roles                  │
                    │ Matching               │
                    │ Market                 │
                    │ Learning               │
                    │ Recommendations        │
                    └───────────┬────────────┘
                                │
                    ┌───────────┴────────────┐
                    ▼                        ▼
               PostgreSQL               Redis
                    │                        │
                    │                   Async Jobs
                    │                        │
                    ▼                        ▼
               pgvector                 Workers
                                             │
                    ┌────────────────────────┼───────────────┐
                    │                        │               │
                    ▼                        ▼               ▼
                  LLM                    Embeddings       RAG
                    │                        │               │
                    └────────────────────────┼───────────────┘
                                             │
                                             ▼
                                    Intelligence Engine
                                             │
                          ┌──────────────────┼──────────────────┐
                          ▼                  ▼                  ▼
                       Career             Market            Learning
                       Gap                 Trends            Paths
                          │                  │                  │
                          └──────────────────┼──────────────────┘
                                             ▼
                                      Recommendations
                                             │
                                             ▼
                                           USER
                                             │
                                             ▼
                                         FEEDBACK
                                             │
                                             ▼
                                  Continuous Intelligence
```

---

# 41. Final Architecture Philosophy

FuturePath AI is not designed as a collection of technologies.

It is designed as an evolving system:

```text
Understand Person
      ↓
Understand Target
      ↓
Understand Gap
      ↓
Understand Market
      ↓
Understand Learning
      ↓
Recommend Action
      ↓
Observe Outcome
      ↓
Learn
      ↓
Repeat
```

The architecture follows the same progression.

---

# 42. Final Design Statement

> **R1 establishes trustworthy career data.**
>
> **R2 turns that data into measurable capability gaps.**
>
> **R3 adds market and learning context through retrieval and intelligence.**
>
> **R4 creates a continuous feedback-driven career intelligence system.**

The architecture deliberately starts simple and becomes distributed only when the product earns that complexity.

---

# 43. Living Architecture Rule

This document is the **architecture baseline**, not an immutable contract.

During implementation, if testing, workload measurements, real user data or operational experience proves that a decision should change:

```text
Observe
 ↓
Measure
 ↓
Challenge decision
 ↓
Document reason
 ↓
Update HLD
 ↓
Update Architecture Decision Runbook
 ↓
Implement
```

No architecture decision should change silently.