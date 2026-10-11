# FuturePath AI
## Architecture, Design Decisions & Solution Architect Interview Guide

**Purpose:**  
This document is the central architecture and interview-study reference for FuturePath AI.

It explains:

- High-Level Design
- Architecture principles
- Major components
- Technology choices
- Alternatives
- Pros and cons
- Trade-offs
- Availability
- Reliability
- Scalability
- Consistency
- CAP theorem
- Performance
- Failure handling
- Security
- Observability
- Disaster recovery
- Architecture evolution
- Detailed Solution Architect interview questions

---

# 1. What Is FuturePath AI?

FuturePath AI is a personal career intelligence platform.

Its purpose is to answer:

> **"Given who I am today, what is happening in the market, where am I falling short, what should I learn next, and which opportunities are relevant to me?"**

The architecture evolves progressively:

```text
R1
Career Profile Intelligence
        ↓
R2
Career Gap & Target Role Intelligence
        ↓
R3
Market + Learning Intelligence
        ↓
R4
Continuous Career Intelligence
```

The long-term intelligence loop is:

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

---

# 2. Core Architectural Principles

## 2.1 Justified Complexity

Do not introduce technology simply because it is popular.

The architecture should evolve according to measurable requirements.

```text
Requirement
    ↓
Constraint
    ↓
Problem
    ↓
Options
    ↓
Trade-off
    ↓
Decision
    ↓
Measurement
    ↓
Re-evaluation
```

For example:

```text
Don't say:

"We need microservices because the application is growing."

Instead say:

"Which component requires independent deployment,
independent scaling, ownership or failure isolation?"
```

---

# 2.2 Deterministic Over Generative

Use LLMs where reasoning and language understanding provide value.

Use deterministic application logic where correctness and repeatability matter.

### LLM

```text
Extract
Normalize
Summarize
Explain
Interpret
```

### Application

```text
Validate
Score
Compare
Rank
Persist
Authorize
Apply business rules
```

The key principle is:

> **The LLM proposes; the application decides.**

---

# 2.3 Stateless Application Compute

The API layer should remain stateless.

```text
             Load Balancer
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
    API-1       API-2      API-N
```

State belongs in external systems:

```text
PostgreSQL
Redis
Object/File Storage
```

This allows horizontal scaling.

---

# 2.4 Asynchronous by Default for Heavy AI Work

PDF processing and LLM inference can take seconds.

Therefore:

```text
HTTP Request
     ↓
Accept Job
     ↓
Queue
     ↓
Worker
     ↓
AI Processing
     ↓
Database
```

The API should not wait for the entire AI pipeline.

---

# 3. High-Level Architecture

```text
                         ┌───────────────┐
                         │     USER      │
                         └───────┬───────┘
                                 │
                                 ▼
                     ┌─────────────────────┐
                     │ Next.js / React     │
                     └──────────┬──────────┘
                                │ HTTPS
                                ▼
                     ┌─────────────────────┐
                     │ Load Balancer       │
                     └──────────┬──────────┘
                                │
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
             FastAPI-1      FastAPI-2       FastAPI-N
                 │              │              │
                 └──────────────┼──────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
             PostgreSQL + pgvector       Redis
                                            │
                                            ▼
                                     Celery Workers
                                            │
                              ┌─────────────┼─────────────┐
                              ▼             ▼             ▼
                             PDF           LLM        Embeddings
                              │             │             │
                              └─────────────┼─────────────┘
                                            ▼
                                      PostgreSQL
```

---

# 4. Release Architecture

## R1 — Career Profile Intelligence

Question:

> **What do we understand about the user's career today?**

Capabilities:

- Authentication
- Resume upload
- PDF processing
- Structured extraction
- Skill extraction
- Experience extraction
- Education
- Evidence
- Skill normalization
- Embeddings
- Career profile
- User corrections
- Processing status
- Retry/failure handling

---

## R2 — Career Gap Intelligence

Question:

> **What am I missing for a target role?**

Adds:

- Target roles
- Job description ingestion
- Requirement extraction
- Skill normalization
- Exact matching
- Semantic matching
- Gap scoring
- Evidence-backed explanations
- Prioritized gaps

---

## R3 — Market & Learning Intelligence

Question:

> **What does the market demand and what should I learn next?**

Adds:

- Market job ingestion
- Market skill taxonomy
- Market trends
- Role clustering
- RAG
- Learning resources
- Learning recommendations
- Personalized learning paths
- Semantic caching where justified

---

## R4 — Continuous Career Intelligence

Question:

> **How can FuturePath continuously guide my career?**

Potential additions:

- User feedback
- Career outcomes
- Recommendation evaluation
- Feedback-driven learning
- Advanced market intelligence
- Agents where justified
- MCP where justified
- Kafka where justified
- Microservices where justified
- Kubernetes/OpenShift where justified
- Dedicated vector infrastructure where justified

---

# 5. R1 Resume Processing Architecture

```text
Resume Upload
     ↓
File Validation
     ↓
Store Document
     ↓
Create Processing Job
     ↓
Redis Queue
     ↓
Celery Worker
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

# 6. Technology Decision #1 — Modular Monolith

## Problem

Should FuturePath start with:

1. Microservices
2. Serverless
3. Modular monolith

---

## Option 1 — Microservices

```text
Auth Service
Profile Service
Resume Service
Matching Service
Recommendation Service
```

### Pros

- Independent deployment
- Independent scaling
- Failure isolation
- Independent technology choices
- Clear service ownership

### Cons

- Network communication
- Distributed failures
- Distributed transactions
- Service discovery
- More deployments
- More monitoring
- Distributed tracing
- More complex local development

---

## Option 2 — Serverless

### Pros

- Automatic scaling
- Pay-per-use
- Less infrastructure management

### Cons

- Cold starts
- Execution limits
- Complex long-running workloads
- Vendor coupling
- More complicated state/workflow management

---

## Option 3 — Modular Monolith

```text
FastAPI
│
├── Auth
├── Resume
├── Profile
├── Skills
├── Matching
├── Jobs
└── Recommendations
```

### Pros

- Simple
- Fast
- Easy local development
- Shared transactions
- Easy debugging
- Low operational overhead
- Clear internal boundaries

### Cons

- Shared deployment unit
- Shared process failure boundary
- Less granular scaling

---

## Decision

**Start with a modular monolith.**

The important point is that "monolith" does not mean "poor architecture."

A well-structured modular monolith gives us:

```text
Clear boundaries
+
Low operational complexity
+
Future extraction capability
```

---

# 7. When Should We Introduce Microservices?

Only when measurable pressure appears.

### Trigger 1

A module requires independent scaling.

### Trigger 2

A module needs independent deployment.

### Trigger 3

A different team owns the module.

### Trigger 4

A module has very different runtime requirements.

### Trigger 5

Failure isolation becomes important.

### Trigger 6

The monolith's deployment cycle becomes a bottleneck.

The decision process:

```text
Measure
   ↓
Identify bottleneck
   ↓
Identify bounded context
   ↓
Prove independent need
   ↓
Extract
   ↓
Measure again
```

---

# 8. Technology Decision #2 — Synchronous vs Asynchronous

Resume extraction and LLM inference may take approximately **8–22 seconds**.

If handled synchronously:

```text
Client
  ↓
HTTP Request
  ↓
FastAPI
  ↓
PDF
  ↓
LLM
  ↓
Embedding
  ↓
Database
  ↓
Response
```

This creates long-lived requests.

At higher concurrency, worker threads/connections become occupied waiting on external AI operations.

---

## Option A — Synchronous

### Pros

- Very simple
- Easy to implement

### Cons

- Long HTTP requests
- Connection exhaustion
- Poor spike handling
- Gateway timeouts
- Poor user experience

---

## Option B — FastAPI BackgroundTasks

### Pros

- Very easy
- No extra infrastructure

### Cons

The task remains associated with the application process.

If:

```text
Application crashes
OR
Container restarts
OR
Deployment occurs
```

the task can be lost.

---

## Option C — Redis + Celery

```text
Client
  ↓
FastAPI
  ↓
202 Accepted
  ↓
Redis
  ↓
Celery Worker
  ↓
PDF / LLM / Embedding
  ↓
PostgreSQL
```

### Pros

- Decouples HTTP from processing
- Queue buffering
- Retries
- Backoff
- Worker scaling
- Controlled concurrency
- API and worker tiers scale independently

### Cons

- Redis dependency
- Worker management
- Queue monitoring

---

## Option D — Kafka

### Pros

- Durable event stream
- Replay
- Partitioning
- Consumer groups
- Multiple consumers

### Cons

- Much higher operational complexity
- Event-stream design required
- Partition management
- More infrastructure

---

## Decision

**Redis + Celery initially.**

Kafka becomes a future option if the problem changes from:

> "Execute this background job"

to:

> "Publish durable events that many independent consumers need to process."

---

# 9. Technology Decision #3 — PostgreSQL

FuturePath has a strongly relational domain:

```text
User
 ↓
Career Profile
 ↓
Experience
 ↓
Skills
 ↓
Skill Evidence
 ↓
Target Role
 ↓
Requirements
 ↓
Gap Analysis
```

PostgreSQL provides:

- ACID transactions
- Foreign keys
- Constraints
- Joins
- SQL
- Transactional integrity
- JSON support
- Mature indexing

---

# 10. PostgreSQL vs MongoDB

## PostgreSQL

Best when:

- Relationships matter
- Transactions matter
- Data integrity matters
- Analytical joins matter

## MongoDB

Best when:

- Data is primarily document-oriented
- Schema flexibility is important
- Relationships are less central

### Decision

PostgreSQL is the better initial fit because the core career domain is relational.

---

# 11. Technology Decision #4 — pgvector vs Dedicated Vector DB

FuturePath needs semantic similarity.

Examples:

```text
User Skill
     ↕
Target Skill

Resume
     ↕
Job Description

User Profile
     ↕
Learning Resource
```

---

## Option A — PostgreSQL + Dedicated Vector DB

```text
                ┌── PostgreSQL
Application ────┤
                └── Vector DB
```

Problem:

A write could succeed in PostgreSQL but fail in the vector database.

```text
PostgreSQL = SUCCESS
Vector DB  = FAILURE
```

Now the systems disagree.

---

## Option B — PostgreSQL + pgvector

```text
PostgreSQL
├── Users
├── Profiles
├── Skills
├── Evidence
└── Embeddings
```

This gives a single persistence boundary.

### Advantages

- One database
- Transactional consistency
- SQL + vector search
- Easier development
- Easier operations
- No immediate dual-write problem

### Disadvantages

- Vector workload shares database resources
- Specialized vector features may be more limited
- Very large vector workloads may eventually justify a dedicated system

---

## Decision

**PostgreSQL + pgvector initially.**

---

# 12. Vector Search and HNSW

For semantic search, an approximate nearest-neighbor index such as HNSW can be used.

Conceptually:

```text
Query Embedding
       ↓
HNSW Index
       ↓
Nearest Vectors
       ↓
Relevant Skills / Documents
```

Without an index, searching millions of vectors can require much more computation.

The architecture should measure:

- Query latency
- Index size
- Memory
- Recall
- Write/update cost

before deciding whether a dedicated vector database is necessary.

---

# 13. CAP Theorem

CAP is one of the most important concepts for defending this architecture.

CAP stands for:

```text
C = Consistency
A = Availability
P = Partition Tolerance
```

During a network partition in a distributed system, you cannot guarantee both strong consistency and availability while also tolerating the partition.

The practical trade-off becomes:

```text
CP
or
AP
```

---

# 14. Consistency

Consistency means:

> Every successful read observes data according to the system's defined consistency guarantees.

For critical career-profile updates:

```text
Profile
+
Skills
+
Evidence
+
Embeddings
```

should not casually become contradictory.

This is one reason to keep closely related relational and vector state within PostgreSQL initially.

---

# 15. Partition Tolerance

A distributed system must assume that network communication can fail.

For example:

```text
Application
     │
     X
     │
Database
```

The application may not be able to communicate with the database.

Partition tolerance means the architecture is designed with such failures in mind.

---

# 16. CP vs AP in FuturePath

Do **not** say:

> "FuturePath is a CP system."

That is too simplistic.

Different components can have different consistency requirements.

### Stronger consistency

Useful for:

```text
Career profile
User data
Skill relationships
Transactions
Authorization
```

### Eventual consistency

Acceptable for things such as:

```text
Market statistics
Cached recommendations
Search indexes
Analytics
Derived trend information
```

The correct Solution Architect answer is:

> **"Consistency is chosen per data flow and business requirement, not necessarily for the entire system."**

---

# 17. CAP vs Application Availability

This is an important interview distinction.

### Application availability

Example:

> 99.9% uptime.

This asks:

> Can users access the application?

### CAP availability

This asks:

> During a network partition, does every request receive a response?

They are related concepts but **not the same thing**.

---

# 18. Availability Architecture

A highly available application tier can look like:

```text
                 Load Balancer
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        API-1        API-2        API-3
```

If API-2 fails:

```text
API-1 ✓
API-2 ✗
API-3 ✓
```

traffic can continue through healthy instances.

Statelessness makes this possible.

---

# 19. Queue-Based Availability

Suppose 1,000 users upload resumes simultaneously.

Bad architecture:

```text
1000 requests
     ↓
1000 LLM calls
```

This could overwhelm:

- API workers
- LLM provider
- memory
- network connections

Better:

```text
1000 uploads
      ↓
API
      ↓
Redis Queue
      ↓
Worker Pool
      ↓
Controlled LLM Calls
```

The queue becomes a **shock absorber**.

---

# 20. Reliability

Reliability means:

> The system continues to behave correctly despite failures.

Potential failures:

```text
PDF corrupted
LLM timeout
LLM unavailable
Invalid LLM output
Embedding failure
Worker crash
Redis failure
Database failure
Network timeout
Duplicate upload
External API rate limit
```

---

# 21. Retry Strategy

Not every failure should be retried.

### Retryable

```text
Timeout
Temporary network error
Rate limit
Temporary provider outage
```

### Usually not retryable

```text
Invalid PDF
Invalid user input
Unsupported file type
Permanent authorization failure
```

Use:

```text
Retry
 ↓
Exponential Backoff
 ↓
Maximum Attempts
 ↓
Failed / Dead-Letter State
```

Example:

```text
Attempt 1
   ↓
2 seconds
   ↓
Attempt 2
   ↓
4 seconds
   ↓
Attempt 3
   ↓
8 seconds
   ↓
FAILED
```

---

# 22. Idempotency

Imagine the same resume is submitted twice.

Without idempotency:

```text
Upload
 ↓
Job A

Same Upload
 ↓
Job B
```

Both may create duplicate processing.

Use:

```text
Document Hash
+
Idempotency Key
+
Unique Constraints
+
Processing State
```

Example:

```text
document_hash = SHA256(file)
```

Then determine whether the same document has already been processed.

---

# 23. Structured LLM Output

Bad:

```text
Resume
 ↓
LLM
 ↓
Free-form text
 ↓
Database
```

Better:

```text
Resume
 ↓
LLM
 ↓
Structured JSON
 ↓
Pydantic Validation
 ↓
Evidence Validation
 ↓
Database
```

Example:

```json
{
  "skills": [
    {
      "name": "PostgreSQL",
      "category": "Database",
      "proficiency": "Practitioner",
      "evidence": "..."
    }
  ]
}
```

The application validates this before persistence.

---

# 24. LLM Failure

If the LLM becomes unavailable:

```text
User
 ↓
Upload
 ↓
API
 ↓
202 Accepted
 ↓
Redis
 ↓
Worker
 ↓
LLM unavailable
```

The job becomes:

```text
PENDING
or
RETRYING
```

The API remains available.

The user does not lose their existing career profile.

---

# 25. Transactional Persistence

After extraction:

```text
BEGIN TRANSACTION

Update Profile
Create Skills
Create Evidence
Create Embeddings

COMMIT
```

If something fails:

```text
ROLLBACK
```

This avoids partially persisted profile state.

---

# 26. Scalability

Scalability should happen progressively.

## Stage 1

Scale API horizontally.

```text
API-1
API-2
API-3
```

## Stage 2

Scale workers independently.

```text
Worker-1
Worker-2
...
Worker-N
```

## Stage 3

Optimize PostgreSQL.

```text
Indexes
Connection Pooling
Query Optimization
```

## Stage 4

Read replicas if required.

## Stage 5

Partitioning if justified.

## Stage 6

Dedicated vector infrastructure if pgvector becomes a measurable bottleneck.

---

# 27. Quantitative Thinking

Architecture decisions should be supported by numbers.

Example target model:

```text
Active Users              50,000
Market JDs/month          10,000
Market vectors            ~300,000
Peak RAG requests         ~25 req/sec
LLM processing            ~8–22 sec
```

Another long-term sizing model can consider:

```text
1,000 users
       ↓
50,000 users
       ↓
500,000 users
```

with corresponding increases in:

- ingestion
- reads
- database size
- vector count
- LLM requests
- worker concurrency

The exact numbers are assumptions and should be validated through load testing.

---

# 28. Bottleneck Analysis

Never assume the bottleneck.

Measure:

```text
API latency
Queue depth
Worker utilization
LLM latency
LLM rate limits
Database CPU
Database connections
Vector search latency
Cache hit rate
Network latency
```

A system is scalable only if we understand where its bottleneck moves as load increases.

---

# 29. RAG Architecture

RAG becomes useful when FuturePath has multiple knowledge domains.

For example:

```text
Career Knowledge
Market Knowledge
Role Knowledge
Learning Knowledge
Historical Career Paths
```

Architecture:

```text
User Context
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

---

# 30. Naive RAG vs Filtered RAG

## Naive RAG

```text
Question
   ↓
Top-K vectors
   ↓
LLM
```

Problem:

The retrieved documents may be semantically similar but belong to the wrong domain.

---

## Filtered RAG

```text
Question
   ↓
Determine Knowledge Domain
   ↓
Apply Metadata Filters
   ↓
Retrieve
   ↓
Re-rank
   ↓
Context Assembly
   ↓
LLM
```

This gives better contextual relevance.

---

# 31. Hybrid Matching

Career matching should not rely entirely on an LLM.

Use:

```text
Exact Match
      +
Semantic Similarity
      +
Deterministic Scoring
      +
Evidence
      +
LLM Explanation
```

Example:

```text
User: PostgreSQL
Target: PostgreSQL
→ Exact Match

User: WebSphere
Target: Application Server Administration
→ Semantic / taxonomy relationship

User: Kafka
Target: Kafka
→ Exact Match
```

---

# 32. Gap Categories

A useful gap engine can distinguish:

```text
Strong Match
Partial Match
Adjacent Skill
Missing Skill
Unknown Evidence
```

Important:

> **Unknown evidence does not mean the user does not possess the skill.**

It means the system does not have sufficient evidence.

---

# 33. Semantic Cache

Caching can reduce:

```text
LLM Cost
LLM Latency
Repeated Computation
```

Potential flow:

```text
Request
 ↓
Semantic Cache
 ↓
Hit?
 ├── YES → Return Cached Result
 │
 └── NO
       ↓
      LLM
       ↓
     Cache
```

Do not introduce this blindly.

First measure:

```text
Repeated queries?
High cost?
High latency?
High cacheability?
```

---

# 34. Market Clustering

FuturePath can eventually discover emerging role patterns.

Example:

```text
Job Descriptions
      ↓
Embeddings
      ↓
Clustering
      ↓
Role Patterns
      ↓
Emerging Skill Groups
```

This can help identify emerging combinations such as:

```text
Cloud
+
Kubernetes
+
Platform Engineering
+
AI
```

without requiring every new job title to be manually predefined.

---

# 35. Agents

Agents should be introduced only when autonomous multi-step workflows are genuinely required.

Traditional workflow:

```text
Step 1
 ↓
Step 2
 ↓
Step 3
```

Agentic workflow:

```text
Goal
 ↓
Plan
 ↓
Choose Tool
 ↓
Execute
 ↓
Observe
 ↓
Re-plan
 ↓
Next Tool
```

Agents introduce additional:

- non-determinism
- failure modes
- security concerns
- cost
- observability requirements

Therefore they belong later unless the product requirement demands them earlier.

---

# 36. MCP

MCP becomes valuable when FuturePath needs standardized integration with external tools or data sources.

Potential future integrations:

```text
Job platforms
Learning platforms
Career tools
External knowledge systems
User productivity tools
```

MCP should be introduced because there is an integration requirement, not simply because it is an AI application.

---

# 37. Kafka

Kafka becomes justified when FuturePath develops a true event-driven architecture.

Example:

```text
CareerProfileUpdated
          │
    ┌─────┼─────┬──────────┐
    ▼     ▼     ▼          ▼
Analytics Market Recommendation Notification
```

Kafka is useful when we need:

- durable event history
- replay
- multiple consumers
- partitioning
- high event throughput

Redis/Celery remains better for straightforward background job execution.

---

# 38. Kubernetes / OpenShift

Initially:

```text
Docker Compose
```

Later:

```text
Kubernetes / OpenShift
```

Introduce orchestration when we have meaningful requirements around:

- container count
- autoscaling
- self-healing
- deployment management
- scheduling
- service discovery
- resource isolation

---

# 39. Security Architecture

Security should exist at every layer.

```text
Authentication
      ↓
Authorization
      ↓
Input Validation
      ↓
File Validation
      ↓
Secrets Management
      ↓
Encryption
      ↓
Safe Logging
      ↓
Audit
```

For AI:

```text
Untrusted Document
        ↓
Prompt Injection Defense
        ↓
Controlled Retrieval
        ↓
Output Validation
        ↓
Controlled Tool Access
```

Never log:

- Resume contents
- Access tokens
- API keys
- Passwords
- Sensitive prompts
- Sensitive user information unnecessarily

---

# 40. Observability

Every important operation should be traceable.

```text
request_id
    ↓
job_id
    ↓
worker
    ↓
LLM request
    ↓
embedding request
    ↓
database transaction
```

Monitor:

### Application

- Request rate
- Error rate
- P95/P99 latency

### Queue

- Queue depth
- Queue age
- Failed jobs
- Retry count

### AI

- LLM latency
- LLM errors
- Token usage
- Cost
- Embedding latency

### Database

- Query latency
- CPU
- Memory
- Connections
- Slow queries

### RAG

- Retrieval latency
- Retrieval quality
- Context size
- Recommendation acceptance

---

# 41. Disaster Recovery

A mature production architecture must explicitly define:

## RPO

**Recovery Point Objective**

> How much data can we afford to lose?

Example:

```text
RPO = 15 minutes
```

means the business accepts potentially losing up to 15 minutes of data.

---

## RTO

**Recovery Time Objective**

> How quickly must the system recover?

Example:

```text
RTO = 1 hour
```

means the system should be restored within approximately one hour.

The actual values must come from business requirements.

---

# 42. Backup Strategy

At minimum:

```text
PostgreSQL
     ↓
Automated Backup
     ↓
Durable External Storage
     ↓
Restore Test
```

Important principle:

> **A backup that has never been successfully restored is not a proven recovery strategy.**

---

# 43. Failure Matrix

| Failure | Impact | Protection |
|---|---|---|
| API instance fails | Requests to instance fail | Load balancer + multiple instances |
| Worker fails | Processing delayed | Queue + retry |
| LLM unavailable | Processing delayed | Retry + backoff |
| LLM invalid output | Invalid profile | Schema validation |
| PDF corrupted | Job failure | File validation |
| Duplicate upload | Duplicate processing | Hash + idempotency |
| DB transaction fails | Partial persistence risk | ACID + rollback |
| Embedding fails | Semantic processing incomplete | Retry/reprocess |
| LLM rate limit | Processing slows | Queue + controlled concurrency |
| Redis unavailable | Jobs cannot be queued | HA/recovery strategy |
| Network partition | Dependency unavailable | Explicit consistency/failure policy |

---

# 44. Architecture Evolution

The architecture should evolve like this:

```text
R1
Modular Monolith
+
Redis/Celery
+
PostgreSQL/pgvector
        ↓
R2
+
Hybrid Matching
+
Gap Engine
        ↓
R3
+
Market Intelligence
+
RAG
+
Learning Intelligence
+
Caching
        ↓
R4
+
Feedback Loop
+
Advanced Intelligence
+
Possible Agents
+
Possible MCP
+
Possible Kafka
+
Possible Microservices
+
Possible Kubernetes
```

The word **possible** is intentional.

R4 does not automatically mean every distributed technology must be introduced.

---

# 45. Architecture Decision Framework

For every significant technology decision, use this template:

```text
1. What problem are we solving?

2. What are the constraints?

3. What alternatives exist?

4. What are the pros?

5. What are the cons?

6. What is the trade-off?

7. What are the failure modes?

8. What is the security impact?

9. How does it scale?

10. What consistency model is required?

11. What does it cost operationally?

12. When should we change the decision?

13. How would I defend this in an interview?
```

---

# 46. Master Decision Table

| Area | Initial Choice | Alternative | Main Trade-off |
|---|---|---|---|
| Backend | Modular Monolith | Microservices | Simplicity vs independent scaling |
| Async | Redis + Celery | Kafka | Job execution vs event streaming |
| Database | PostgreSQL | MongoDB | Relational integrity vs flexibility |
| Vector | pgvector | Qdrant/Pinecone | Unified persistence vs specialized scale |
| PDF | pypdf/pdfplumber | OCR | Simplicity vs scanned-document support |
| LLM Output | Structured | Free-form | Reliability vs flexibility |
| Matching | Hybrid | LLM-only | Determinism vs flexibility |
| RAG | R3 onward | Immediate | Complexity vs retrieval value |
| RAG Retrieval | Filtered | Naive Top-K | Relevance vs simplicity |
| Cache | Demand-driven | Immediate semantic cache | Simplicity vs optimization |
| Agents | Later | Immediate | Control vs autonomy |
| MCP | Later | Immediate | Integration value vs abstraction |
| Events | Kafka later | Redis initially | Replayability vs complexity |
| Deployment | Docker Compose initially | Kubernetes | Simplicity vs orchestration |
| Learning | Feedback-driven | RLHF | Practicality vs training complexity |

---

# 47. Architecture Change Triggers

| Technology | Change when... |
|---|---|
| Microservices | Independent deployment/scaling/ownership becomes necessary |
| Kafka | Durable event streaming/replay/multiple consumers become necessary |
| Kubernetes | Container orchestration complexity becomes significant |
| Dedicated Vector DB | pgvector becomes a measurable bottleneck |
| Read Replicas | Read workload exceeds primary capacity |
| Partitioning | Data volume/query patterns justify it |
| RAG | Multiple knowledge domains require retrieval |
| Agents | Autonomous multi-step planning becomes necessary |
| MCP | Standardized external tool integration becomes necessary |
| Semantic Cache | Repeated semantic requests materially affect cost/latency |
| OCR | Real scanned resumes require it |
| Multi-region | Business availability/latency requirements justify it |

---

# 48. Solution Architect Interview Questions

## Architecture Fundamentals

### Q1. Explain the FuturePath architecture in 60 seconds.

**Answer:**

> "FuturePath starts as a stateless FastAPI modular monolith because the domain is evolving and independent service boundaries haven't been proven yet. Resume processing and LLM inference are long-running, so they are moved to Redis and Celery workers. PostgreSQL is the transactional source of truth, with pgvector providing semantic search without introducing another persistence system initially. R2 adds hybrid target-role matching and deterministic gap analysis. R3 introduces market intelligence and filtered RAG when external knowledge becomes important. R4 can evolve toward event-driven architecture, agents, MCP, microservices and Kubernetes only when measurable requirements justify them."

---

### Q2. Why not start with microservices?

**Answer:**

> "Because microservices distribute failure boundaries across networks. At the beginning, the domain is changing rapidly and the operational overhead would not provide enough value. I prefer a modular monolith with explicit boundaries and extract services later when independent scaling, deployment, ownership or failure isolation becomes necessary."

---

### Q3. How can a monolith scale?

**Answer:**

> "If the application is stateless, I can run multiple instances behind a load balancer. Heavy asynchronous work is already separated into workers, so API and worker tiers can scale independently."

---

### Q4. What is the difference between a monolith and a modular monolith?

**Answer:**

> "A traditional monolith may have weak internal boundaries. A modular monolith deliberately separates business capabilities into modules with clear interfaces and responsibilities while keeping them within one deployable application."

---

# 49. Async Processing Questions

### Q5. Why is resume processing asynchronous?

**Answer:**

> "PDF parsing, LLM inference and embedding generation can take seconds. Keeping the HTTP request open wastes server resources and makes spikes dangerous. The API therefore accepts the job and returns a job ID while workers process it asynchronously."

---

### Q6. Why Redis and Celery?

**Answer:**

> "Redis provides the queue/buffering layer and Celery provides worker execution, retries and independent scaling. This separates the user-facing API from long-running AI processing."

---

### Q7. Why not FastAPI BackgroundTasks?

**Answer:**

> "BackgroundTasks still run in the application process. A process crash or deployment can interrupt the task. A distributed queue gives better isolation and retry capabilities."

---

### Q8. Why not Kafka?

**Answer:**

> "Kafka is designed for durable event streaming, replay and multiple independent consumers. Our initial problem is reliable background job execution, so Redis and Celery solve it with less complexity."

---

# 50. Database Questions

### Q9. Why PostgreSQL?

**Answer:**

> "The domain is relational: users, profiles, experiences, skills, evidence, roles and requirements have strong relationships and transactional requirements. PostgreSQL provides ACID transactions, constraints and mature SQL capabilities."

---

### Q10. Why not MongoDB?

**Answer:**

> "MongoDB is useful for document-centric workloads, but FuturePath has significant relational relationships and analytical joins. PostgreSQL is a better initial fit."

---

### Q11. Why pgvector?

**Answer:**

> "We need semantic search, but the vectors are strongly associated with relational career data. pgvector allows us to keep both within PostgreSQL and reduces the need for cross-database consistency."

---

### Q12. Why not Pinecone or Qdrant?

**Answer:**

> "They are valid specialized options. The trade-off is introducing another persistence system and synchronization boundary. I would move to a dedicated vector database when vector scale, latency or required features justify the additional operational complexity."

---

# 51. CAP Questions

### Q13. Explain CAP theorem.

**Answer:**

> "CAP says that when a distributed system experiences a network partition, it cannot simultaneously guarantee strong consistency and availability while also tolerating the partition. The practical choice becomes whether a particular distributed interaction favors consistency or availability."

---

### Q14. What is CP?

**Answer:**

> "Consistency plus partition tolerance. During a partition, the system may reject or delay operations rather than return potentially inconsistent data."

---

### Q15. What is AP?

**Answer:**

> "Availability plus partition tolerance. The system continues responding during the partition, potentially returning stale or temporarily divergent data."

---

### Q16. Is FuturePath CP or AP?

**Best answer:**

> "I wouldn't classify the entire application as simply CP or AP. CAP applies to specific distributed interactions. Critical transactional career data needs stronger consistency, while caches, analytics and some market-derived information can tolerate eventual consistency."

---

### Q17. Why does pgvector help with consistency?

**Answer:**

> "If relational data and vectors were stored in separate systems, a failure between two writes could leave them inconsistent. Keeping them in PostgreSQL initially allows related updates to participate in the same transactional boundary."

---

### Q18. Does PostgreSQL eliminate all distributed-system problems?

**Answer:**

> "No. It reduces one consistency boundary, but the overall system still contains distributed components such as API instances, Redis, workers and external AI providers. We still need explicit failure and consistency strategies."

---

# 52. Availability Questions

### Q19. How do you achieve high availability?

**Answer:**

> "Keep API instances stateless, run multiple instances behind a load balancer, separate long-running workers from the API, use queue buffering, and design the database and external dependencies with appropriate recovery strategies."

---

### Q20. What happens if one API instance crashes?

**Answer:**

> "The load balancer routes traffic to healthy instances. Because the API is stateless, another instance can handle the request."

---

### Q21. What happens if a worker crashes?

**Answer:**

> "The job remains managed by the queue and can be retried according to its processing state and retry policy. Idempotency prevents duplicate side effects."

---

### Q22. What happens if the LLM provider is down?

**Answer:**

> "The API remains available. Processing jobs become pending or retryable, with exponential backoff and bounded retries. Existing user data remains accessible."

---

# 53. Reliability Questions

### Q23. How do you make the system reliable?

**Answer:**

> "I use asynchronous processing, retries, exponential backoff, idempotency, schema validation, transactional persistence, timeouts, controlled concurrency and observability."

---

### Q24. How do you prevent duplicate processing?

**Answer:**

> "Use document fingerprints, idempotency keys, unique constraints and explicit job state transitions."

---

### Q25. What if the LLM returns invalid JSON?

**Answer:**

> "The response is rejected by schema validation. We can retry with a bounded policy, and if validation continues to fail, the job enters a failed state rather than corrupting the database."

---

### Q26. Why should the LLM not directly update the database?

**Answer:**

> "LLM output is probabilistic. The application must validate, normalize and authorize the result before it becomes persistent system state."

---

# 54. Scalability Questions

### Q27. What happens if 1,000 resumes arrive simultaneously?

**Answer:**

```text
1000 uploads
     ↓
Load Balancer
     ↓
API
     ↓
Redis
     ↓
Worker Pool
     ↓
Controlled LLM Calls
```

> "The queue absorbs the burst while workers process jobs at a controlled rate."

---

### Q28. How would you scale the workers?

**Answer:**

> "Based on queue depth, task age, CPU/memory utilization, LLM throughput and external provider rate limits. Worker count should be driven by measurements."

---

### Q29. What could become the bottleneck?

Potential bottlenecks include:

```text
LLM provider
Worker CPU
Redis
PostgreSQL
Vector search
External API rate limits
Network
```

The correct answer is:

> **Measure before optimizing.**

---

# 55. RAG Questions

### Q30. Why not use RAG in R1?

**Answer:**

> "R1 is primarily structured extraction. There isn't enough external knowledge retrieval required to justify RAG complexity."

---

### Q31. Why introduce RAG later?

**Answer:**

> "R3 introduces market data, learning resources, role knowledge and historical career information. Retrieval becomes valuable when the system needs grounded external context."

---

### Q32. Why filtered RAG instead of simple Top-K?

**Answer:**

> "Because semantic similarity alone doesn't guarantee contextual relevance. Filtering by domain lets us retrieve from the correct knowledge space before assembling the final context."

---

# 56. AI Questions

### Q33. Why not let the LLM calculate the entire skill gap?

**Answer:**

> "The gap score should be deterministic, testable and explainable. I use exact matching, semantic similarity and deterministic scoring for the decision, and the LLM can provide the natural-language explanation."

---

### Q34. Why not let the LLM do everything?

**Answer:**

Because of:

```text
Non-determinism
Hallucination
Cost
Latency
Difficult testing
Poor reproducibility
```

---

### Q35. How do you make AI output reliable?

**Answer:**

```text
Structured Output
+
Schema Validation
+
Evidence
+
Deterministic Rules
+
Retry
+
Observability
```

---

# 57. Agent Questions

### Q36. Why not use agents from day one?

**Answer:**

> "The initial workflows are deterministic. Agents introduce additional planning uncertainty and failure modes. I would introduce them when autonomous multi-step tool use provides measurable product value."

---

### Q37. When would you use an agent?

When the system needs:

```text
Goal
 ↓
Plan
 ↓
Select tools
 ↓
Execute
 ↓
Observe
 ↓
Re-plan
```

---

# 58. Kafka Questions

### Q38. When would you introduce Kafka?

**Answer:**

> "When we have multiple independent consumers, durable event history, replay requirements, partitioning and sufficient event throughput to justify Kafka."

---

### Q39. Redis vs Kafka?

| Redis + Celery | Kafka |
|---|---|
| Background jobs | Event streaming |
| Task execution | Durable event log |
| Retries | Replay |
| Simpler | More operationally complex |
| Worker queue | Multiple consumer groups |
| Good for R1 | Useful at later maturity |

---

# 59. Kubernetes Questions

### Q40. Why not Kubernetes immediately?

**Answer:**

> "Docker Compose is enough for early development. Kubernetes becomes valuable when we have meaningful requirements for autoscaling, self-healing, scheduling, deployment management and a larger container footprint."

---

# 60. Security Questions

### Q41. How do you secure an AI application?

**Answer:**

> "I secure identity and authorization first, validate uploaded files and inputs, protect secrets, encrypt sensitive data, avoid sensitive logging, validate LLM output, treat retrieved documents as untrusted and restrict any future agent/tool permissions."

---

### Q42. What is prompt injection?

**Answer:**

> "Prompt injection occurs when untrusted content attempts to manipulate the model's instructions or behavior."

For example, a job description or document could contain malicious instructions.

Therefore:

```text
Retrieved Content ≠ Trusted Instructions
```

---

# 61. Observability Questions

### Q43. What would you monitor?

**Answer:**

```text
API latency
P95/P99
Error rate
Queue depth
Queue age
Worker failures
Retry count
LLM latency
LLM cost
Database latency
Vector search latency
RAG quality
Recommendation acceptance
```

---

### Q44. How do you trace one resume through the system?

Use:

```text
request_id
     ↓
job_id
     ↓
worker
     ↓
LLM request
     ↓
embedding request
     ↓
DB transaction
```

This allows end-to-end debugging.

---

# 62. Disaster Recovery Questions

### Q45. What is RPO?

> "Recovery Point Objective defines how much data loss the business can tolerate."

---

### Q46. What is RTO?

> "Recovery Time Objective defines how quickly the system must be restored."

---

### Q47. How do you validate backups?

> "By performing regular restore tests. A successful backup operation alone doesn't prove that recovery will work."

---

# 63. Design Scenario Questions

## Q48. What if traffic increases 10x?

Answer in this order:

```text
1. Measure bottleneck
2. Scale API horizontally
3. Scale workers
4. Increase queue capacity
5. Control LLM concurrency
6. Optimize DB
7. Add read replicas if required
8. Optimize vector search
9. Add caching if justified
10. Reconsider service boundaries if necessary
```

Do not immediately say:

> "Move to microservices."

---

## Q49. What if PostgreSQL becomes the bottleneck?

Investigate:

```text
Slow queries
Indexes
Connections
CPU
Memory
Locks
Vector queries
Read/write ratio
```

Then consider:

```text
Query optimization
+
Indexes
+
Connection pooling
+
Read replicas
+
Partitioning
+
Vector separation
```

only as justified.

---

## Q50. What if pgvector becomes the bottleneck?

First measure:

```text
Vector count
Query latency
Recall
Index size
Memory
CPU
Concurrent queries
```

Then evaluate:

```text
HNSW optimization
+
Hardware scaling
+
Query optimization
+
Dedicated vector DB
```

---

# 64. The Most Important Interview Framework

Whenever an interviewer challenges a technology choice, answer in this order:

```text
WHAT PROBLEM?

        ↓

WHAT CONSTRAINT?

        ↓

WHAT OPTIONS?

        ↓

PROS / CONS?

        ↓

TRADE-OFF?

        ↓

WHAT DID WE CHOOSE?

        ↓

WHY?

        ↓

WHY NOT THE OTHERS?

        ↓

WHAT CAN FAIL?

        ↓

HOW DOES IT SCALE?

        ↓

HOW IS IT SECURED?

        ↓

WHEN WOULD WE CHANGE IT?
```

This framework is more valuable than memorizing individual technologies.

---

# 65. Final Architecture Story

The complete story of FuturePath AI is:

```text
                 USER
                   │
                   ▼
             Career Data
                   │
                   ▼
        ┌────────────────────┐
        │ Career Profile     │
        │ Intelligence       │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Target Role        │
        │ Gap Intelligence   │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Market Intelligence│
        │ + RAG              │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Learning &         │
        │ Recommendations    │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ User Action        │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Career Outcome     │
        └─────────┬──────────┘
                  │
                  ▼
             Feedback
                  │
                  └──────────────► Intelligence
```

The infrastructure evolves underneath it:

```text
R1
FastAPI
+
Redis/Celery
+
PostgreSQL/pgvector

        ↓

R2
+
Hybrid Matching
+
Gap Engine

        ↓

R3
+
RAG
+
Market Intelligence
+
Learning Intelligence
+
Caching

        ↓

R4
+
Feedback
+
Possible Agents
+
Possible MCP
+
Possible Kafka
+
Possible Microservices
+
Possible Kubernetes
```

---

# 66. Final Principles to Remember

### Principle 1

> **Don't choose technology before understanding the problem.**

### Principle 2

> **Use numbers to justify architecture.**

### Principle 3

> **Keep the API stateless.**

### Principle 4

> **Move long-running AI work out of HTTP requests.**

### Principle 5

> **Keep transactional data in a reliable source of truth.**

### Principle 6

> **Use deterministic logic for decisions that need repeatability.**

### Principle 7

> **Treat LLM output as untrusted until validated.**

### Principle 8

> **CAP is about distributed systems under partition, not simply uptime.**

### Principle 9

> **Availability, reliability and scalability are different architectural properties.**

### Principle 10

> **Do not introduce microservices, Kafka or Kubernetes without measurable reasons.**

### Principle 11

> **A queue absorbs spikes; it does not magically increase total processing capacity.**

### Principle 12

> **Retries require idempotency.**

### Principle 13

> **Backups are useful only if recovery is tested.**

### Principle 14

> **Every architectural decision has a change trigger.**

### Principle 15

> **Architecture should evolve from measured pressure, not technology trends.**

---

# 67. One Sentence to Memorize for Interviews

> **"I choose the simplest architecture that satisfies the current functional, performance, availability, reliability, consistency and scalability requirements, and I define measurable triggers for when that decision should change."**

That is the core architectural philosophy behind FuturePath AI.