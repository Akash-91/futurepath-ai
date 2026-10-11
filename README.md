# FuturePath AI

> Personal Career & Future Intelligence Platform

## Vision

Given who I am today, what is happening in the market,
where am I falling short, what should I learn next,
and which opportunities are relevant to me?

## Product

FuturePath AI is built around the idea of connecting a person's
current capabilities, career goals, market intelligence, skill
gaps, and next actions.

- Career Profile
- Skill Intelligence
- Job Market Intelligence
- Skill Gap Analysis
- Personalized Learning
- Career Assistant

### Product Documentation

- [Product Vision](docs/product/1-product-vision.md)
- [Problem Statement](docs/product/2-problem-statement.md)
- [Personas](docs/product/3-personas.md)
- [Use Cases](docs/product/4-use-cases.md)
- [Functional Requirements](docs/product/5-functional-requirements.md)
- [Non Functional Requirements](docs/product/6-non-functional-requirements.md)

## Architecture

Architecture is being developed incrementally based on
real requirements, constraints, experiments, and measurable
system limitations.

### Architecture Documentation

- [Architecture v0.1](docs/architecture/architecture-v0.1.md)
- [HLD Roadmap](docs/architecture/HLD_roadmap.md)
- [Final End-to-End HLD](docs/architecture/Final_HLD.md)

### Architecture Decisions

- [Master Architecture Decisions](docs/decisions/Final_DecisionDoc.md)
- [Release 1 Architecture Decision Record](docs/decisions/Release1_decisionDoc.md)

## Current Status

### Architecture v0.1

- [x] Product Vision
- [x] Problem Statement
- [x] Personas
- [x] Use Cases
- [x] Functional Requirements
- [x] Non-Functional Requirements
- [ ] System Context
- [ ] High-Level Design
- [ ] Data Model
- [ ] Technology Evaluation
- [ ] Architecture Decision Records

## Development Roadmap

## Development Roadmap

FuturePath AI will be built incrementally. Each phase introduces new capabilities only when they provide real product or architectural value.

The initial goal is to build and deploy **Release 1 — Career Profile MVP** as a real, working application. Advanced technologies such as RAG, Agents, MCP, Kafka, Kubernetes, and OpenShift will be introduced progressively as the product evolves.

---

### Phase 0 — Architecture
**Status: 🚧 In Progress**

Finalize the initial architecture, technology choices, system boundaries, data model, API structure, security, reliability, observability, and deployment approach.

**Initial Technology Stack**

| Area | Decision |
|---|---|
| Frontend | Next.js + React |
| Backend | FastAPI + Python |
| Architecture | Modular Monolith |
| Database | PostgreSQL |
| Vector Search | pgvector |
| Cache / Queue | Redis |
| Background Processing | Celery |
| Resume Processing | pypdf / pdfplumber |
| LLM Processing | Structured JSON + Pydantic validation |
| Embeddings | Configurable embedding model |
| Matching | Hybrid matching |
| File Storage | Object Storage abstraction |
| Containerization | Docker |
| Local Deployment | Docker Compose |
| CI/CD | GitHub Actions |
| Observability | Logs + Metrics + Traces |

**Key architectural principle:**

> Start simple, measure real requirements, and introduce distributed technologies only when the system needs them.

---

### Phase 1 — Career Profile MVP
**Status: ⏳ Next**

Build and deploy the first real working release.

**Core capabilities:**

- User authentication
- Resume upload
- Resume validation
- PDF text extraction
- Structured career information extraction
- Skill extraction and normalization
- Experience and education extraction
- Evidence/provenance
- Embedding generation
- Career profile creation
- Profile correction
- Processing status
- Retry and failure handling
- Basic observability

**Core flow:**

```text
User
 ↓
Next.js
 ↓
FastAPI
 ↓
Resume Processing
 ↓
LLM
 ↓
Validation
 ↓
Skill Normalization
 ↓
Embeddings
 ↓
PostgreSQL + pgvector
 ↓
Career Profile
```

**Deployment goal:**

```text
Code
 ↓
Docker
 ↓
Local Testing
 ↓
CI/CD
 ↓
Deployment
 ↓
Real Application
 ↓
Monitoring & Improvement
```

---

### Phase 2 — RAG
**Status: ⏳ Planned**

Introduce Retrieval-Augmented Generation when FuturePath requires multiple knowledge sources.

Build:

- Knowledge ingestion
- Embeddings
- Vector retrieval
- Metadata filtering
- Reranking
- Context assembly
- RAG-based career assistance

```text
User Question
 ↓
Retriever
 ↓
pgvector
 ↓
Relevant Context
 ↓
LLM
 ↓
Answer
```

---

### Phase 3 — Job Intelligence
**Status: ⏳ Planned**

Build intelligence around target roles and job opportunities.

Build:

- Job description ingestion
- Job/role extraction
- Skill taxonomy
- Job embeddings
- Job matching
- Skill-gap analysis
- Match scoring
- Market intelligence

```text
Career Profile
      +
Job Description
      ↓
Hybrid Matching
      ↓
Match Score
      ↓
Skill Gaps
```

**Matching approach:**

```text
Exact Matching
+
Semantic Similarity
+
Deterministic Scoring
+
LLM Explanation
```

---

### Phase 4 — Personalized Learning
**Status: ⏳ Planned**

Convert identified skill gaps into actionable learning plans.

Build:

- Learning resource ingestion
- Skill → learning mapping
- Personalized learning paths
- Learning recommendations
- Progress tracking
- User feedback
- Recommendation improvement

```text
Skill Gap
 ↓
Learning Resources
 ↓
Personalized Learning Path
 ↓
Progress
 ↓
Feedback
```

---

### Phase 5 — Agents
**Status: ⏳ Planned**

Introduce AI agents only when autonomous multi-step workflows provide clear value.

Potential capabilities:

- Understand career goals
- Search opportunities
- Analyze skill gaps
- Find learning resources
- Generate recommendations
- Execute multi-step career workflows

Agents will not be introduced simply for architectural complexity.

---

### Phase 6 — MCP
**Status: ⏳ Planned**

Introduce MCP when FuturePath requires standardized access to external tools and data sources.

Potential integrations:

- Job platforms
- Learning platforms
- External knowledge sources
- Career tools
- Productivity tools

---

### Phase 7 — Event-Driven Architecture
**Status: ⏳ Planned**

Introduce event-driven architecture when multiple independent components need to react to domain events.

Example:

```text
CareerProfileUpdated
        ↓
 ┌──────┼──────────┐
 ↓      ↓          ↓
Analytics Market  Recommendation
```

**Technology evolution:**

```text
Redis + Celery
      ↓
Kafka
```

Kafka will be introduced only when durable event history, replay, multiple consumers, partitioning, or high-throughput event processing justify it.

---

### Phase 8 — Scale & Resilience
**Status: ⏳ Planned**

Improve production scalability and reliability.

Focus areas:

- Horizontal API scaling
- Worker scaling
- Database optimization
- Connection pooling
- Caching
- Read replicas
- Retry and failure handling
- Rate limiting
- Load testing
- High availability
- Disaster recovery
- RPO / RTO
- Performance optimization
- Cost optimization

```text
Load Balancer
 ├── API Instance 1
 ├── API Instance 2
 └── API Instance 3

Redis
 └── Celery Workers
       ├── Worker 1
       ├── Worker 2
       └── Worker 3
```

---

### Phase 9 — Kubernetes
**Status: ⏳ Planned**

Move from Docker Compose to Kubernetes when container orchestration requirements justify the additional complexity.

Potential capabilities:

- Container orchestration
- Horizontal autoscaling
- Self-healing
- Rolling deployments
- Resource management
- Service discovery
- Production workload management

```text
Docker Compose
      ↓
Kubernetes
```

---

### Phase 10 — OpenShift
**Status: ⏳ Planned**

Introduce OpenShift as the enterprise deployment platform when the architecture and operational requirements justify it.

```text
Kubernetes
      ↓
OpenShift
```

This phase will also provide practical experience with enterprise container platforms, security, deployment, scaling, and platform operations.

---

## Technology Evolution

The overall architecture is expected to evolve approximately as follows:

```text
PHASE 0
Architecture
   ↓
PHASE 1
Modular Monolith
+ PostgreSQL
+ pgvector
+ Redis/Celery
+ Docker
   ↓
PHASE 2
RAG
   ↓
PHASE 3
Job Intelligence
   ↓
PHASE 4
Personalized Learning
   ↓
PHASE 5
Agents
   ↓
PHASE 6
MCP
   ↓
PHASE 7
Event-Driven Architecture
+ Kafka when justified
   ↓
PHASE 8
Scale & Resilience
   ↓
PHASE 9
Kubernetes
   ↓
PHASE 10
OpenShift
```

## Architecture Evolution Principle

FuturePath AI will follow a **measure-before-migrate** approach.

Technologies will not be introduced simply because they are popular or expected in modern architectures.

The decision to introduce a new technology will be based on:

- Real functional requirements
- Performance requirements
- Availability requirements
- Reliability requirements
- Scalability requirements
- Security requirements
- Operational complexity
- Measurable system limitations

> **Build the simplest architecture that works today. Measure it in reality. Evolve it when the evidence says it is time.**