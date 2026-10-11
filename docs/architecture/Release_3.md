
# FuturePath AI — Release 3
## Market & Learning Intelligence

**Release:** R3  
**Primary Goal:** Move from static career analysis to market-aware intelligence.

---

# 1. R3 Objective

R1:

> Understand me.

R2:

> Understand where I want to go.

R3:

> **Understand what the market is demanding and what I should do about it.**

---

# 2. New Capabilities

R3 introduces:

- Job-description ingestion
- Market requirements
- Market skill taxonomy
- Job/role clustering
- Market trends
- RAG
- Learning-resource ingestion
- Educational RAG
- Market-aware recommendations
- Personalized learning paths
- Better recommendation explanations

---

# 3. Market Intelligence

```text
External Job Sources
        │
        ▼
Job Descriptions
        │
        ▼
Requirement Extraction
        │
        ▼
Skill Normalization
        │
        ▼
Embeddings
        │
        ▼
PostgreSQL + pgvector
```

The system can now answer:

> "What skills are becoming more important for Solution Architects?"

rather than only:

> "What skills are required by this one target role?"

---

# 4. RAG Architecture

The supplied comprehensive HLD proposes multi-domain filtered RAG rather than blindly searching all vectors.

Conceptually:

```text
                 User Profile
                     │
                     ▼
              RAG Orchestrator
              /       |       \
             /        |        \
            ▼         ▼         ▼
         Skills     Market    Historical
        Knowledge   Context     Paths
            \         |         /
             \        |        /
              └───────┼────────┘
                      ▼
                  LLM Context
                      │
                      ▼
                Recommendation
```

---

# 5. RAG Alternatives

## Option A — No RAG

Use structured database queries only.

### Advantage

Simple and deterministic.

### Disadvantage

Cannot provide rich contextual reasoning over large knowledge collections.

---

## Option B — Naive Top-K RAG

```text
Question
   ↓
Vector Search
   ↓
Top K
   ↓
LLM
```

### Advantage

Simple.

### Disadvantage

May retrieve irrelevant information across different domains.

---

## Option C — Multi-Domain Filtered RAG

```text
User context
    │
    ├── Skill knowledge
    ├── Market requirements
    └── Historical career paths
              │
              ▼
         Filtered retrieval
              │
              ▼
             LLM
```

### Decision

**Choose Option C for mature R3 RAG.**

But importantly:

> RAG is introduced because R3 creates a real retrieval problem — not simply because "AI applications should use RAG."

---

# 6. Learning Intelligence

R3 adds educational recommendations.

Instead of:

> Learn Kubernetes.

The system can eventually provide:

```text
Gap
 ↓
Kubernetes Pod Lifecycle
 ↓
Relevant learning resource
 ↓
Specific content chunk
 ↓
Practice recommendation
```

This follows the educational-RAG direction in the supplied comprehensive HLD.

---

# 7. Market Clustering

A later R3 capability can identify emerging role clusters.

For example:

```text
500 Job Descriptions
       │
       ▼
Skill vectors
       │
       ▼
Clustering
       │
       ▼
Emerging capability pattern
       │
       ▼
Potential new role
```

The supplied document gives an example of discovering an AI Engineer-type cluster from repeated requirements.

This should initially be treated as **discovery**, not unquestionable truth.

---

# 8. Semantic Caching

R3 is also where Redis can evolve from primarily queue infrastructure toward caching.

Example:

```text
Question
   │
   ▼
Semantic Cache
   │
   ├── HIT → return
   │
   └── MISS
          │
          ▼
         LLM
```

The supplied document proposes semantic similarity caching to reduce repeated LLM cost and latency.

This should be introduced only after actual traffic patterns demonstrate repetition.

---

# 9. R3 Alternatives — Vector Database

At this stage we reassess:

### Option A

PostgreSQL + pgvector

### Option B

PostgreSQL + dedicated vector DB

### Option C

Search platform such as OpenSearch/Elasticsearch

The initial choice remains pgvector.

But R3 introduces a **review trigger**:

> If vector workload becomes the dominant database workload or requires capabilities PostgreSQL cannot economically provide, reconsider dedicated vector infrastructure.

This is the correct architectural behavior:

**Decision ≠ permanent commitment.**

---

# 10. R3 Success Criteria

FuturePath should now answer:

> "Given my current profile, target role, and current market demand, what should I focus on next?"

The answer should combine:

```text
My profile
+
Target role
+
Market requirements
+
Skill gap
+
Learning resources
=
Personalized career action plan
```

---

# 11. R3 Interview Defense

### Why introduce RAG now?

Because the product now contains multiple knowledge domains and requires contextual retrieval.

### Why not RAG in R1?

Because R1 has a small, structured data problem. Adding RAG would increase complexity without solving a demonstrated problem.

### Why semantic caching?

Only when repeated expensive requests justify it.

### Why market clustering?

Because R3 introduces enough market data for discovery algorithms to become useful.

---

**Release 3 principle:**

> Move from deterministic career analysis to context-aware, market-aware intelligence.