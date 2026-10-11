
# FuturePath AI — Release 2
## Career Gap & Target Role Intelligence

**Release:** R2  
**Primary Goal:** Move from "understanding me" to "understanding where I want to go."

---

# 1. R2 Objective

R1 answers:

> What do we know about this person's career?

R2 answers:

> **Given a target role, what am I missing and how significant is the gap?**

---

# 2. New Capabilities

R2 introduces:

- Target role
- Target capability model
- Job-description ingestion
- Requirement extraction
- Skill normalization
- Exact skill matching
- Semantic skill matching
- Gap scoring
- Evidence-backed explanations
- Prioritized recommendations
- Target-role comparison

---

# 3. R2 User Journey

```text
Career Profile
      │
      ▼
Select Target Role
      │
      ▼
Target Role Requirements
      │
      ▼
Normalize Skills
      │
      ├──────────────┐
      ▼              ▼
Exact Match     Semantic Match
      │              │
      └───────┬──────┘
              ▼
         Gap Engine
              │
              ▼
      Priority Calculation
              │
              ▼
       Recommendations
```

---

# 4. Matching Architecture

The supplied architecture recommends a deterministic + semantic approach.

We will therefore use:

```text
              Candidate Skill
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
    Exact Matching      Vector Similarity
          │                   │
          └─────────┬─────────┘
                    ▼
              Gap Scoring
```

---

# 5. Why Not Pure LLM Matching?

### Option A — LLM does everything

```text
Profile + JD
     │
     ▼
    LLM
     │
     ▼
"You're 72% ready"
```

Problem:

- difficult to reproduce
- difficult to audit
- potentially inconsistent
- expensive
- difficult to explain

---

### Option B — Exact matching only

```text
Java == Java
Kubernetes == Kubernetes
```

Problem:

```text
K8s ≠ Kubernetes
Postgres ≠ PostgreSQL
```

and semantically related skills may be missed.

---

### Option C — Hybrid matching

```text
Exact identity
       +
Semantic similarity
       +
Deterministic scoring
       +
Evidence
```

### Decision

**Choose Option C.**

The LLM can explain or assist, but the core score should remain deterministic.

---

# 6. Skill-Gap Model

Example:

| Requirement | User | Match |
|---|---|---|
| Python | Strong | High |
| PostgreSQL | Strong | High |
| Kubernetes | Evidence | Medium |
| Kafka | None | Gap |
| System Design | Partial evidence | Medium |
| AWS | None | Gap |

The system produces:

```text
Skill Gap
 ├── Missing
 ├── Weak
 ├── Partial
 ├── Matched
 └── Strong
```

---

# 7. Recommendation Engine

Recommendations should answer:

```text
WHAT?
WHY?
PRIORITY?
EVIDENCE?
```

Example:

> Kafka — High Priority  
> Your target role requires distributed messaging experience. Your current profile shows related event-driven architecture experience but no direct Kafka evidence.

This is substantially stronger than:

> "Learn Kafka."

---

# 8. R2 Architecture Choices

### Matching execution

#### Option A — API synchronous

Suitable for small deterministic calculations.

#### Option B — Background job

Suitable when matching expands into expensive multi-stage processing.

#### Decision

Use synchronous processing for lightweight deterministic gap calculations initially.

Move to asynchronous execution when the workload becomes materially expensive.

This demonstrates an important architecture principle:

> **Not everything needs to become a background job simply because we have a queue.**

---

# 9. R2 Vector Usage

pgvector is used for:

```text
User Skill
      │
      ▼
Embedding
      │
      ▼
Nearest Target Capability
```

Example:

```text
"Kubernetes"
      │
      ▼
0.94
      │
      ▼
"K8s container orchestration"
```

The similarity result is only one input.

It does not automatically mean the user possesses the capability.

Evidence remains necessary.

---

# 10. R2 Scope Boundary

R2 still does **not** attempt to become the complete career marketplace.

Not yet:

- real-time job market
- millions of jobs
- educational RAG
- continuous market monitoring
- autonomous career agent

The focus remains:

> **Profile → Target → Gap → Action**

---

# 11. R2 Success Criteria

A user should be able to say:

> "I want to become a Solution Architect."

And FuturePath should answer:

```text
Current capabilities
       ↓
Target capabilities
       ↓
Matched capabilities
       ↓
Partial capabilities
       ↓
Missing capabilities
       ↓
Priority
       ↓
Recommended next actions
```

---

# 12. R2 Architectural Exit Criteria

Before R3:

- Target-role model is stable
- Skill taxonomy is sufficiently useful
- Matching quality has evaluation data
- False-positive semantic matches are understood
- Gap scoring is reproducible
- Recommendations have traceable rationale
- User corrections are persisted
- PostgreSQL/pgvector performance is measured

---

# 13. R2 Interview Defense

### Why hybrid matching?

Because deterministic logic provides explainability and semantic search handles vocabulary differences.

### Why not LLM-only?

Because the scoring mechanism must be reproducible and auditable.

### Why pgvector?

Because the vector workload remains tightly coupled to career entities and does not yet justify a separate vector platform.

---

**Release 2 principle:**

> Turn career information into a measurable capability gap.