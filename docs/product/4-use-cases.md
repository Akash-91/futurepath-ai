# FuturePath AI — Use Cases

## 1. Purpose

This document defines the core user use cases for FuturePath AI.

Use cases translate the personas and product vision into concrete user goals. They will later serve as the foundation for:

- Functional requirements
- Non-functional requirements
- API design
- Data modeling
- Architecture decisions
- AI workflow design
- Testing and evaluation

The initial use cases focus on the **Experienced Professional** persona while supporting future expansion toward career exploration and job intelligence.

---

# 2. Use Case Overview

FuturePath's initial product flow is:

```text
Create Career Profile
        ↓
Understand Current Skills
        ↓
Define Target Role
        ↓
Analyze Skill Gaps
        ↓
Prioritize Gaps
        ↓
Receive Recommendations
        ↓
Track Progress
```

Future capabilities will extend this flow with market intelligence and job matching.

---

# 3. UC-01 — Create Career Profile

### Goal

Create a structured representation of the user's professional background from available career information.

### Primary Persona

Experienced Professional

### Trigger

The user provides career information, such as a resume.

### Preconditions

- User has access to FuturePath.
- The user has professional information available for ingestion.

### Main Flow

1. User uploads a resume or provides professional information.
2. FuturePath extracts relevant information.
3. The system identifies:
   - Employment history
   - Roles
   - Skills
   - Technologies
   - Projects
   - Certifications
   - Education
4. Extracted information is converted into a structured career profile.
5. The user reviews the generated profile.
6. The user can correct or update inaccurate information.
7. FuturePath stores the confirmed profile.

### Expected Outcome

The user has a structured career profile that can be used by downstream capabilities.

### Important Considerations

The system should distinguish between:

- Explicit information extracted from the source.
- AI-generated inference.
- User-confirmed information.

### Failure / Edge Cases

- Unsupported document format.
- Poor-quality or scanned resume.
- Missing sections.
- Ambiguous skill names.
- Duplicate information.
- Incorrect extraction.
- Conflicting information across sources.

---

# 4. UC-02 — Understand Current Skills

### Goal

Identify and organize the user's current skills and capabilities.

### Primary Persona

Experienced Professional

### Trigger

A career profile exists.

### Main Flow

1. FuturePath analyzes the user's career profile.
2. The system identifies skills and technologies.
3. Related skills are grouped where appropriate.
4. Experience and evidence are associated with skills.
5. The system estimates capability information where sufficient evidence exists.
6. The user reviews and corrects the results.

### Example

```text
Middleware
├── WebSphere
├── Tomcat
├── IBM HTTP Server
└── Application Server Administration

Cloud / Platform
├── OpenShift
├── Kubernetes
└── Containerization
```

### Expected Outcome

The user has an understandable representation of their current capabilities.

### Failure / Edge Cases

- Skill mentioned without supporting evidence.
- Skill appears only once.
- Different names for the same skill.
- Outdated skills.
- Conflicting proficiency signals.
- AI incorrectly infers a skill.

---

# 5. UC-03 — Define Target Career

### Goal

Allow the user to specify the role or career direction they want to pursue.

### Primary Persona

Experienced Professional

### Secondary Persona

Career Explorer

### Trigger

The user wants to evaluate a future career direction.

### Main Flow

1. User selects or enters a target role.
2. FuturePath identifies the target role.
3. The system determines the capabilities typically associated with that role.
4. The target role becomes part of the user's career plan.

### Example

```text
Current Role
Middleware Engineer

        ↓

Target Role
Solution Architect
```

### Expected Outcome

FuturePath has a defined target state against which the user's current capabilities can be evaluated.

### Failure / Edge Cases

- Ambiguous role name.
- New or uncommon role.
- Role differs significantly between organizations.
- Insufficient market information.
- User has multiple target roles.

---

# 6. UC-04 — Analyze Skill Gap

### Goal

Compare the user's current capabilities with the capabilities required for the target role.

### Primary Persona

Experienced Professional

### Secondary Persona

Career Explorer

### Trigger

The user has both a current career profile and a target role.

### Main Flow

1. FuturePath retrieves the user's current capabilities.
2. FuturePath determines the target role's required capabilities.
3. The system compares the two.
4. Each capability is categorized, for example:
   - Strong alignment
   - Partial alignment
   - Gap
   - Unknown
5. FuturePath explains the basis for the assessment.
6. The user reviews the result.

### Example

| Capability | Current State | Target Requirement | Assessment |
|---|---|---|---|
| Middleware | Strong | Strong | Aligned |
| System Design | Medium | Strong | Partial |
| Distributed Systems | Basic | Strong | Gap |
| Database Architecture | Basic | Strong | Gap |
| Networking | Medium | Strong | Partial |

### Expected Outcome

The user understands where their current capabilities differ from the target role.

### Failure / Edge Cases

- Target requirements are incomplete.
- User profile contains insufficient evidence.
- Proficiency cannot be determined reliably.
- Job-market data conflicts with generic role definitions.
- AI produces an unsupported assessment.

---

# 7. UC-05 — Prioritize Skill Gaps

### Goal

Determine which skill gaps are most important to address first.

### Primary Persona

Experienced Professional

### Trigger

A skill-gap analysis exists.

### Main Flow

1. FuturePath identifies the user's gaps.
2. The system evaluates factors such as:
   - Importance to target role
   - Market demand
   - Current proficiency
   - Dependency on other skills
   - Frequency of requirement
   - Potential career impact
3. Gaps are prioritized.
4. FuturePath explains why each gap has its priority.
5. The user can review and adjust priorities.

### Example

```text
Priority 1
Distributed Systems
Why:
- High relevance to target role
- Significant current gap
- Foundation for multiple architecture capabilities

Priority 2
Database Architecture

Priority 3
Advanced Networking
```

### Expected Outcome

The user knows which gaps deserve attention first.

### Failure / Edge Cases

- Insufficient market evidence.
- Two gaps have similar priority.
- Priority changes as market conditions change.
- User has personal constraints that are not represented in the model.

---

# 8. UC-06 — Generate Personalized Recommendations

### Goal

Recommend concrete actions based on the user's prioritized gaps.

### Primary Persona

Experienced Professional

### Secondary Persona

Career Explorer

### Trigger

Prioritized skill gaps exist.

### Main Flow

1. FuturePath identifies the highest-priority gaps.
2. The system determines appropriate actions.
3. Actions may include:
   - Learn a concept.
   - Complete a project.
   - Practice system design.
   - Gain practical experience.
   - Study a technology.
   - Work toward a certification.
   - Consider an intermediate role.
4. Recommendations are ordered based on relevance.
5. FuturePath explains why each recommendation was selected.

### Example

```text
Gap:
Distributed Systems

Recommended Actions:

1. Learn distributed-system fundamentals.
2. Study consistency and replication.
3. Design a fault-tolerant service.
4. Build an event-driven prototype.
5. Practice architecture case studies.
```

### Expected Outcome

The user receives a practical next-step plan rather than a generic list of resources.

### Failure / Edge Cases

- Recommendations are too generic.
- Recommendation does not match user's current level.
- Learning resources become unavailable.
- Multiple recommendations conflict.
- AI recommends an action without sufficient evidence.

---

# 9. UC-07 — Understand Job Market

### Goal

Understand which skills and capabilities are currently relevant in the user's target market.

### Primary Persona

Experienced Professional

### Secondary Persona

Career Explorer

### Trigger

The user requests market intelligence for a role or career direction.

### Main Flow

1. User specifies a target role or market.
2. FuturePath collects relevant job-market information.
3. The system extracts recurring skills and requirements.
4. Skills are normalized.
5. Demand patterns are analyzed.
6. FuturePath presents the findings with supporting evidence.

### Example

```text
Solution Architect Market

Frequently observed:
- System Design
- Cloud Architecture
- Distributed Systems
- Security
- Networking
- Databases

Emerging:
- AI Architecture
- GenAI
- Platform Engineering
```

### Expected Outcome

The user understands which capabilities appear important in the current market.

### Failure / Edge Cases

- Job data is stale.
- Duplicate job postings.
- Poor-quality job descriptions.
- Market data is biased toward a particular geography.
- Temporary hiring trends are mistaken for long-term demand.

---

# 10. UC-08 — Match User to Job

### Goal

Identify how well a user's capabilities align with a specific job opportunity.

### Primary Persona

Active Job Seeker

### Trigger

The user provides or selects a job posting.

### Main Flow

1. FuturePath analyzes the job requirements.
2. The system compares requirements against the user's career profile.
3. Requirements are categorized:
   - Strong match
   - Partial match
   - Missing
   - Unknown
4. FuturePath identifies important gaps.
5. The system explains the match.
6. The user can decide whether to prioritize the opportunity.

### Expected Outcome

The user understands whether the opportunity is worth pursuing and why.

### Important Principle

A match score alone is insufficient.

The system should explain:

> **Why does this job match me?**

and:

> **What could prevent me from being successful in this role?**

### Failure / Edge Cases

- Job description is vague.
- Requirements contain ambiguous terminology.
- Required skills are missing from the user's profile.
- User has transferable experience that keyword matching would miss.
- Job posting has expired.

---

# 11. UC-09 — Track Career Progress

### Goal

Track how the user's capabilities evolve over time.

### Primary Persona

Experienced Professional

### Trigger

The user updates their profile, completes learning activities, gains experience, or changes career goals.

### Main Flow

1. User updates career information.
2. FuturePath updates the career profile.
3. Skill evidence is updated.
4. Skill-gap analysis can be recalculated.
5. Recommendations can change.
6. The system records meaningful changes.

### Example

```text
January

System Design
Basic

        ↓

April

System Design
Intermediate

        ↓

August

System Design
Strong
```

### Expected Outcome

The user can understand whether their actions are improving alignment with their target career.

### Failure / Edge Cases

- Skill improvement cannot be objectively verified.
- Old evidence conflicts with new evidence.
- User changes target role.
- Market requirements change.

---

# 12. UC-10 — Review and Correct AI Output

### Goal

Allow users to correct inaccurate AI-generated information and improve the reliability of their career profile.

### Primary Persona

All personas

### Trigger

The user identifies incorrect or incomplete information.

### Main Flow

1. FuturePath presents extracted or inferred information.
2. User identifies an incorrect result.
3. User edits or rejects the information.
4. FuturePath stores the confirmed state.
5. Future processing should respect the user's correction where appropriate.

### Expected Outcome

The user remains in control of their career data and AI-generated interpretations.

### Why This Matters

AI extraction and inference will not always be correct.

FuturePath should therefore be designed around:

```text
AI proposes
     ↓
User reviews
     ↓
User confirms / corrects
     ↓
System learns the confirmed state
```

rather than treating AI output as unquestionable truth.

---

# 13. MVP Use Cases

The initial implementation should focus on a small end-to-end value loop.

### MVP

```text
UC-01 Create Career Profile
        ↓
UC-02 Understand Current Skills
        ↓
UC-03 Define Target Career
        ↓
UC-04 Analyze Skill Gap
        ↓
UC-05 Prioritize Skill Gaps
        ↓
UC-06 Generate Personalized Recommendations
```

These use cases establish the core intelligence loop without requiring the full job-market platform.

### Later Phases

```text
                    MVP
                     │
                     ▼
             Career Intelligence
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   Market Intelligence      Job Matching
          │                     │
          └──────────┬──────────┘
                     ▼
              Progress Tracking
```

---

# 14. Use Case Prioritization

| Use Case | Priority | Initial Phase |
|---|---|---|
| Create Career Profile | P0 | MVP |
| Understand Current Skills | P0 | MVP |
| Define Target Career | P0 | MVP |
| Analyze Skill Gap | P0 | MVP |
| Prioritize Skill Gaps | P0 | MVP |
| Personalized Recommendations | P0 | MVP |
| Understand Job Market | P1 | Later |
| Match User to Job | P1 | Later |
| Track Career Progress | P1 | Later |
| Review and Correct AI Output | P0 | MVP |

---

# 15. Product Boundary

The initial FuturePath product is **not** intended to:

- Automatically apply for jobs.
- Make career decisions on behalf of the user.
- Guarantee employment outcomes.
- Treat AI-generated assessments as objective truth.
- Replace professional career counseling.
- Recommend technologies solely because they are currently popular.

The system should provide **evidence-based career intelligence and recommendations while keeping the user in control of decisions**.

---

# 16. Evolution Principle

FuturePath capabilities should be introduced when a real user or system problem justifies them.

The architecture should evolve according to:

```text
User Need
    ↓
Product Requirement
    ↓
System Constraint
    ↓
Architecture Problem
    ↓
Evaluate Options
    ↓
Choose Solution
    ↓
Measure Result
    ↓
Architecture Evolution
```

Technology should therefore follow demonstrated requirements rather than precede them.