FuturePath AI — Functional Requirements

1. Purpose

This document defines the functional requirements for FuturePath AI.

Functional requirements describe what the system must do from a user’s and product perspective.

They will provide the foundation for:

* API design
* Domain and data modeling
* AI workflow design
* User interface capabilities
* Validation and testing
* Architecture decisions
* Future non-functional requirements
* Architecture-to-requirement traceability

This document intentionally avoids prescribing specific technologies.

For example, a requirement may state:

“The system shall store and retrieve vector representations of supported career content.”

It should not state:

“The system shall use Pinecone.”

The technology decision belongs later in architecture and technology evaluation.

⸻

2. Product Scope

The initial FuturePath functional scope is:

                CAREER INFORMATION
                        │
                        ▼
                PROFILE CREATION
                        │
                        ▼
                 SKILL ANALYSIS
                        │
                        ▼
                 TARGET ROLE
                        │
                        ▼
                 GAP ANALYSIS
                        │
                        ▼
               GAP PRIORITIZATION
                        │
                        ▼
             RECOMMENDATIONS

Future phases will extend this foundation with:

Career Intelligence
        │
        ├── Market Intelligence
        │
        ├── Job Matching
        │
        ├── Personalized Learning
        │
        └── Progress Tracking

⸻

3. Functional Requirement Classification

Requirements are classified by priority.

Priority	Meaning
P0	Required for the initial MVP
P1	Important for the next product phase
P2	Future capability
P3	Exploratory / optional

⸻

4. FR-001 — User Account

Priority: P0

The system shall allow a user to establish an identifiable FuturePath account.

Requirements

The system shall:

1. Create a unique user identity.
2. Associate career information with the user.
3. Allow the user to access their own career profile.
4. Allow the user to update their profile.
5. Prevent one user from accessing another user’s career information.
6. Maintain the relationship between the user and all career-related data.

Acceptance Criteria

* A new user can create an account.
* A user can retrieve their own profile.
* A user cannot retrieve another user’s profile.
* User-associated career data remains associated with the correct user.

⸻

5. FR-002 — Career Information Ingestion

Priority: P0

The system shall allow users to provide professional information to FuturePath.

Initial Input

The primary initial input will be a resume.

Future versions may support:

* Additional documents
* Professional profiles
* Certifications
* Project descriptions
* Manually entered experience
* Other structured career information

Requirements

The system shall:

1. Accept supported career-information documents.
2. Validate the input.
3. Store the original source.
4. Create an ingestion record.
5. Track ingestion status.
6. Process the source for information extraction.
7. Associate the source with the correct user.
8. Allow the user to identify the source used to generate profile information.

Possible Ingestion States

UPLOADED
   ↓
VALIDATING
   ↓
PROCESSING
   ↓
EXTRACTED
   ↓
REVIEW_REQUIRED
   ↓
CONFIRMED

Failure states shall also be represented.

Acceptance Criteria

Given a valid supported resume:

* The system accepts the document.
* The original document is associated with the user.
* An ingestion process is created.
* The system reports processing status.
* Extracted information becomes available for review.

⸻

6. FR-003 — Document Validation

Priority: P0

The system shall validate uploaded career documents before processing.

Validation Areas

The system should validate:

* Supported format
* File readability
* File integrity
* File size
* Content availability
* Potentially unsupported document characteristics

Requirements

If validation fails:

1. Processing shall not continue.
2. The system shall record the failure.
3. The user shall receive a meaningful error.
4. The original upload shall not be silently discarded.

Example

Instead of:

“Processing failed.”

The system should provide:

“The uploaded document could not be processed because the file format is not currently supported.”

⸻

7. FR-004 — Career Information Extraction

Priority: P0

The system shall extract structured career information from supported sources.

Information Categories

The extraction process should identify, where available:

Career Profile
│
├── Personal / Professional Summary
├── Employment
│   ├── Organization
│   ├── Role
│   ├── Dates
│   └── Responsibilities
│
├── Skills
├── Technologies
├── Projects
├── Education
├── Certifications
├── Achievements
└── Other Career Evidence

Requirements

The system shall:

1. Extract information from the source.
2. Preserve the relationship between extracted information and its source.
3. Identify uncertain or ambiguous information.
4. Avoid inventing information that does not exist in the source.
5. Provide extraction results for user review.

Important Principle

The extraction system must distinguish:

Observed information

“Worked with OpenShift.”

from:

Inferred information

“Likely has container orchestration experience.”

The second statement must not automatically become a confirmed fact.

⸻

8. FR-005 — Career Profile Creation

Priority: P0

The system shall transform extracted and user-confirmed information into a structured career profile.

Career Profile Components

Career Profile
│
├── Employment History
├── Roles
├── Skills
├── Technologies
├── Projects
├── Certifications
├── Education
├── Industries
└── Career Evidence

Requirements

The system shall:

1. Create a structured profile from extracted information.
2. Associate profile information with supporting evidence.
3. Preserve user-confirmed information.
4. Allow profile updates.
5. Maintain profile history where required.
6. Distinguish confirmed information from inferred information.

Acceptance Criteria

A user should be able to answer:

“What does FuturePath currently know about my professional background?”

without having to inspect the original resume.

⸻

9. FR-006 — User Review and Correction

Priority: P0

The system shall allow users to review and correct extracted or inferred information.

Requirements

The user shall be able to:

* Confirm information.
* Edit information.
* Reject information.
* Add missing information.
* Remove incorrect information.
* Provide additional context.

Example

AI extraction:

Skill: Kubernetes
Confidence: Medium
Evidence: Resume project description

User:

Reject

FuturePath should preserve the user’s correction.

Principle

AI output is proposed information, not automatically authoritative information.

⸻

10. FR-007 — Skill Identification

Priority: P0

The system shall identify skills from the user’s career information.

Skill Categories

The system should support categories such as:

* Technical skills
* Architecture skills
* Operational skills
* Management skills
* Communication skills
* Domain skills
* Tools and technologies

Example

Skill
│
├── Category
├── Evidence
├── Source
├── Recency
├── Experience
├── Confidence
└── User Confirmation

Requirements

The system shall:

1. Identify explicit skills.
2. Normalize equivalent skill names where appropriate.
3. Associate skills with evidence.
4. Track confidence for inferred skills.
5. Allow user correction.
6. Avoid treating a technology mention as automatic proof of proficiency.

⸻

11. FR-008 — Skill Evidence

Priority: P0

The system shall maintain evidence supporting career capabilities.

Example

Skill:
OpenShift
Evidence:
"Migrated four applications from traditional middleware
infrastructure to OpenShift."
Source:
Resume
Evidence Type:
Professional Experience

Requirements

Each significant skill assessment should be traceable to one or more pieces of evidence where possible.

Evidence may include:

* Resume statements
* Projects
* Employment history
* Certifications
* User-provided information
* Later, completed learning activities

Why This Matters

FuturePath should eventually be able to answer:

“Why does the system believe I have this skill?”

⸻

12. FR-009 — Skill Proficiency Representation

Priority: P0

The system shall represent a user’s skill state without assuming that proficiency can always be accurately determined.

Possible states include:

UNKNOWN
BEGINNER
INTERMEDIATE
ADVANCED
EXPERT

However, these labels are not sufficient by themselves.

The system should eventually consider:

* Evidence
* Duration
* Recency
* Frequency of use
* Complexity of work
* User confirmation

Important Rule

The system must not assign a precise proficiency level when the available evidence does not support it.

For example:

“Used Python once in a project”

should not automatically become:

“Advanced Python.”

⸻

13. FR-010 — Target Role Definition

Priority: P0

The system shall allow the user to define one or more target career directions.

Examples

Solution Architect
Cloud Architect
AI Engineer
Platform Engineer

Requirements

The user shall be able to:

1. Search for a target role.
2. Select a target role.
3. Enter a target role manually where supported.
4. Set a target role as active.
5. Change the target role.
6. Maintain multiple possible career directions in future versions.

Initial MVP

The MVP may support one active target role at a time.

⸻

14. FR-011 — Target Role Capability Model

Priority: P0

The system shall represent the capabilities associated with a target role.

Example

Solution Architect
│
├── System Design
├── Distributed Systems
├── Databases
├── Networking
├── Security
├── Cloud
├── Resilience
├── Cost Optimization
└── Stakeholder Management

Requirements

The system shall:

1. Associate capabilities with target roles.
2. Represent the importance of capabilities where sufficient evidence exists.
3. Distinguish required capabilities from optional capabilities.
4. Allow role requirements to evolve as market information improves.

⸻

15. FR-012 — Target Role Analysis

Priority: P0

The system shall analyze the user’s selected target role and explain what capabilities are relevant to it.

Output

The system should provide:

* Important capabilities
* Supporting skills
* Typical experience
* Relevant technologies
* Potentially important domain knowledge

Example

For Solution Architect:

High importance
- System Design
- Distributed Systems
- Architecture Principles
Supporting
- Databases
- Networking
- Security
- Cloud
Contextual
- Industry knowledge
- Leadership
- Stakeholder management

The system should avoid presenting every technology associated with the role as equally important.

⸻

16. FR-013 — Skill Gap Analysis

Priority: P0

The system shall compare the user’s current capabilities against the target role’s expected capabilities.

Gap Categories

STRONG_ALIGNMENT
PARTIAL_ALIGNMENT
GAP
UNKNOWN

Requirements

The system shall:

1. Identify capabilities relevant to the target role.
2. Retrieve corresponding user capabilities.
3. Compare current and target states.
4. Identify gaps.
5. Explain the basis of the assessment.
6. Identify insufficient evidence.
7. Allow the user to challenge or correct an assessment.

Example

Target:
Distributed Systems — Advanced
User:
Distributed Systems — Basic
Assessment:
Significant Gap

⸻

17. FR-014 — Gap Explanation

Priority: P0

The system shall explain why a capability has been identified as a gap.

The explanation should reference available evidence.

Example

“Distributed systems appears to be a significant gap because the current profile contains limited evidence of distributed-system design, while the target role requires strong understanding of scalability, consistency, fault tolerance, and distributed communication.”

The system should avoid unsupported statements such as:

“You are bad at distributed systems.”

⸻

18. FR-015 — Gap Prioritization

Priority: P0

The system shall prioritize identified skill gaps.

Potential Factors

Prioritization may consider:

* Target-role importance
* Market demand
* Current proficiency
* Gap magnitude
* Skill dependencies
* Frequency of requirement
* Career impact
* User-defined goals

Example

Priority 1
Distributed Systems
Priority 2
Database Architecture
Priority 3
Advanced Networking

Requirements

The system shall:

1. Produce a prioritized list.
2. Explain why a gap received its priority.
3. Avoid presenting the priority as absolute truth.
4. Allow recalculation when relevant information changes.

⸻

19. FR-016 — Recommendation Generation

Priority: P0

The system shall generate personalized actions based on identified and prioritized gaps.

Recommendation Types

Recommendations may include:

* Learning a concept
* Completing a project
* Practicing architecture
* Gaining practical experience
* Studying a technology
* Reviewing documentation
* Pursuing a certification
* Applying for an intermediate opportunity

Requirements

Recommendations shall consider:

* User’s current capabilities
* Target role
* Gap severity
* Skill dependencies
* Evidence
* Market relevance

Example

Gap:
Distributed Systems
Recommendation:
Build a small service demonstrating replication,
failure handling, and consistency trade-offs.
Reason:
Practical implementation provides stronger evidence
of capability than theoretical study alone.

⸻

20. FR-017 — Recommendation Explanation

Priority: P0

The system shall explain why a recommendation was generated.

Each significant recommendation should answer:

1. What should I do?
2. Why should I do it?
3. Which gap does it address?
4. Why is it relevant to my target role?
5. What evidence supports the recommendation?

This prevents FuturePath from becoming a generic AI advice generator.

⸻

21. FR-018 — Career Intelligence Summary

Priority: P0

The system shall provide a consolidated view of the user’s career position.

The summary should eventually answer:

Where am I today?
        ↓
Where do I want to go?
        ↓
What is missing?
        ↓
What matters most?
        ↓
What should I do next?

Example Output

Current Position
Strong middleware and production experience.
Target
Solution Architect.
Strong Alignment
- Middleware
- Production Operations
- Migration
Important Gaps
- Distributed Systems
- Database Architecture
Recommended Next Step
Focus on distributed-system fundamentals and
architecture case studies.

⸻

22. FR-019 — Job Market Intelligence

Priority: P1

The system shall eventually analyze relevant job-market information.

Requirements

The system should be able to:

1. Identify relevant job postings or market sources.
2. Extract required skills.
3. Normalize skills.
4. Identify recurring requirements.
5. Analyze demand patterns.
6. Associate market observations with roles.
7. Identify emerging requirements where sufficient evidence exists.
8. Identify geographic or market-specific differences.

Important Constraint

Market conclusions should be based on sufficient evidence rather than a small number of job postings.

⸻

23. FR-020 — Job Requirement Extraction

Priority: P1

The system shall extract structured requirements from job descriptions.

Example

Job
│
├── Role
├── Experience
├── Required Skills
├── Preferred Skills
├── Responsibilities
├── Domain
└── Location

The system should distinguish:

Required

Kubernetes experience required.

from:

Preferred

Experience with OpenShift preferred.

This distinction is important for accurate job matching.

⸻

24. FR-021 — Job Matching

Priority: P1

The system shall compare a user’s career profile against a job opportunity.

Match Dimensions

The system should consider:

* Skills
* Experience
* Role history
* Domain experience
* Responsibilities
* Required capabilities
* Preferred capabilities

Output

Strong Matches
Partial Matches
Missing Requirements
Unknown Requirements
Potential Risks

The system should provide explanations rather than relying solely on a numerical score.

⸻

25. FR-022 — Job Match Explanation

Priority: P1

For every significant match assessment, the system shall explain:

* Why the user matches.
* Where the user partially matches.
* What is missing.
* Which gaps are critical.
* Which gaps may be trainable.
* What information is uncertain.

⸻

26. FR-023 — Career Progress Tracking

Priority: P1

The system shall allow meaningful changes to the user’s career profile to be tracked over time.

Changes May Include

* New skills
* Increased proficiency
* New roles
* New projects
* Certifications
* Completed learning
* New target roles
* Updated market requirements

Expected Capability

FuturePath should eventually answer:

“How has my readiness for my target role changed over the last six months?”

⸻

27. FR-024 — Reassessment

Priority: P1

The system shall allow career assessments to be recalculated when relevant information changes.

Reassessment may be triggered by:

* Profile update
* Skill update
* Target-role change
* New market data
* New job requirements
* User-requested reassessment

Example

Profile Change
      ↓
Skill State Changes
      ↓
Gap Analysis Changes
      ↓
Priorities Change
      ↓
Recommendations Change

⸻

28. FR-025 — User Feedback

Priority: P1

The system shall allow users to provide feedback on FuturePath’s output.

Feedback may include:

* Correct
* Incorrect
* Partially correct
* Not relevant
* Useful
* Not useful

The system should associate feedback with the relevant output.

Purpose

Feedback will eventually support:

* Quality evaluation
* Recommendation improvement
* AI evaluation
* Personalization
* Error analysis

⸻

29. FR-026 — Source Traceability

Priority: P0

The system shall maintain traceability between important system outputs and their supporting sources.

For example:

Recommendation
      ↓
Skill Gap
      ↓
Target Requirement
      ↓
User Capability
      ↓
Evidence
      ↓
Original Source

This should allow the system to answer:

“Why did FuturePath reach this conclusion?”

This is a core requirement for trustworthy AI behavior.

⸻

30. FR-027 — Confidence Representation

Priority: P0

The system shall represent uncertainty for AI-generated or inferred information where appropriate.

Possible conceptual states:

HIGH CONFIDENCE
MEDIUM CONFIDENCE
LOW CONFIDENCE
INSUFFICIENT EVIDENCE

Confidence should not be presented as a guarantee of correctness.

It represents the system’s confidence based on available evidence and processing.

⸻

31. FR-028 — Contradiction Handling

Priority: P1

The system shall identify conflicting information.

Example

Resume:

Kubernetes — 5 years

User correction:

I only worked with Kubernetes for 1 year.

The system should not silently choose one value.

It should identify the conflict and allow the user to resolve it.

⸻

32. FR-029 — Profile Versioning

Priority: P1

The system should maintain meaningful versions or history of the user’s career profile.

This allows FuturePath to understand:

Profile V1
     ↓
Profile V2
     ↓
Profile V3

and eventually answer:

“What changed?”

Profile versioning also provides an audit trail for significant career-data changes.

⸻

33. FR-030 — Data Export

Priority: P1

The system should allow users to export their career information.

Potential formats may include:

* Structured JSON
* Human-readable report
* Career profile document

The exported information should represent user-owned career data in a portable form.

⸻

34. FR-031 — Data Deletion

Priority: P0

The system shall allow users to request deletion of their career information.

Deletion should consider:

* Uploaded documents
* Extracted information
* Career profile
* Skill information
* Recommendations
* Feedback
* Associated derived data

The exact retention and deletion policy will be defined separately as part of security and privacy requirements.

⸻

35. FR-032 — Processing Status

Priority: P0

The system shall expose the status of long-running operations.

Examples:

Document Processing
├── Uploaded
├── Validating
├── Extracting
├── Structuring
├── Awaiting Review
└── Complete

For failures:

FAILED

The system should provide enough information for the user to understand what happened.

⸻

36. FR-033 — Retry Failed Processing

Priority: P0

The system shall allow recoverable processing failures to be retried.

Examples:

* Temporary processing failure
* Temporary model/service failure
* Interrupted ingestion
* Transient dependency failure

The system should avoid requiring the user to upload the same document repeatedly when the underlying failure is recoverable.

⸻

37. FR-034 — Idempotent Processing

Priority: P0

Repeated processing of the same request should not unintentionally create duplicate career records.

For example:

Resume uploaded
      ↓
Processing started
      ↓
Network interruption
      ↓
Retry

The retry should not create two independent career profiles unless explicitly requested.

This requirement will become particularly important if FuturePath later introduces asynchronous processing.

⸻

38. FR-035 — AI Output Classification

Priority: P0

FuturePath shall distinguish between different types of system-generated information.

At minimum:

FACT
INFERENCE
ASSESSMENT
RECOMMENDATION

Example

FACT

User worked with WebSphere.

INFERENCE

User likely has application-server administration experience.

ASSESSMENT

Application-server administration is strongly aligned with the target role.

RECOMMENDATION

Focus next on distributed-system design.

This separation is a core product principle.

⸻

39. FR-036 — Human Override

Priority: P0

The user shall be able to override incorrect system interpretations.

Examples:

AI:
Skill = Kubernetes
User:
Reject

or:

AI:
Python proficiency = Intermediate
User:
Change to Beginner

The system shall preserve the user’s explicit correction.

⸻

40. FR-037 — Personalized Context

Priority: P1

FuturePath should maintain relevant user context when generating recommendations.

Context may include:

* Career history
* Target roles
* Existing skills
* Previous recommendations
* Completed learning
* User feedback
* Previous corrections
* Career goals

Recommendations should use relevant context rather than treating every interaction as an isolated question.

⸻

41. FR-038 — Multiple Career Directions

Priority: P2

FuturePath should eventually allow users to maintain multiple possible career directions.

Example:

Current Role
Middleware Engineer
Potential Directions
├── Solution Architect
├── Platform Engineer
└── AI Engineer

The system should allow comparison between possible paths.

⸻

42. FR-039 — Career Path Comparison

Priority: P2

The system should eventually compare multiple target roles.

Example:

Capability	Solution Architect	AI Engineer	Platform Engineer
System Design	High	High	High
Python	Medium	High	Medium
ML/AI	Low	High	Low
Kubernetes	Medium	Medium	High
Networking	High	Medium	High

The user should be able to understand:

* Which path is closest to their current profile.
* Which path requires the largest transition.
* Which skills transfer between paths.
* Which capabilities are unique to each path.

⸻

43. FR-040 — Learning Resource Association

Priority: P1

FuturePath should eventually associate skill gaps with relevant learning resources.

Resources may include:

* Courses
* Documentation
* Books
* Tutorials
* Projects
* Architecture case studies
* Practice exercises

The system should prioritize resources based on the identified gap and user’s current capability rather than simply returning popular resources.

⸻

44. FR-041 — Personalized Learning Plan

Priority: P1

The system should eventually transform prioritized skill gaps into a structured learning plan.

Example:

Target:
Solution Architect
Gap:
Distributed Systems
Learning Plan
Week 1
Consistency & Replication
Week 2
Partitioning & Sharding
Week 3
Fault Tolerance
Week 4
Architecture Case Study
Week 5
Build Practical Project

The learning plan should be adaptable based on user progress.

⸻

45. FR-042 — Career Intelligence Assistant

Priority: P1

FuturePath should eventually provide a conversational interface through which users can ask questions about their career profile.

Examples:

“What are my biggest gaps for Solution Architect?”

“Why did you prioritize distributed systems?”

“Which of my skills transfer to a Platform Engineer role?”

“What should I focus on this month?”

The assistant must use the user’s structured career context and relevant evidence rather than generating generic answers.

⸻

46. FR-043 — Explainability of AI Decisions

Priority: P0

FuturePath shall provide explanations for important AI-generated conclusions.

Important conclusions include:

* Skill identification
* Skill assessment
* Gap identification
* Gap prioritization
* Recommendations
* Job matching

The explanation should identify relevant evidence and assumptions where possible.

⸻

47. FR-044 — Unsupported Conclusion Handling

Priority: P0

The system shall avoid presenting unsupported conclusions as facts.

If evidence is insufficient, the system should communicate uncertainty.

Example:

“There is not enough information in your current profile to determine your database architecture proficiency.”

rather than:

“Your database architecture skill is weak.”

⸻

48. FR-045 — Market-Aware Recommendations

Priority: P1

When market intelligence becomes available, FuturePath should incorporate relevant market information into recommendations.

Example:

Current Skill Gap
       +
Target Role
       +
Market Demand
       ↓
Prioritized Recommendation

However, market demand should be treated as one input rather than the sole determinant.

⸻

49. FR-046 — Recommendation Recalculation

Priority: P1

Recommendations should be recalculated when significant underlying information changes.

Potential triggers:

* New skill
* Skill proficiency change
* Target role change
* Market requirement change
* Completed learning activity
* User feedback

⸻

50. FR-047 — Auditability of Important Decisions

Priority: P0

FuturePath shall retain sufficient information to understand how important assessments were generated.

For example:

Assessment
    ↓
Inputs
    ↓
Evidence
    ↓
Rules / Model Output
    ↓
Decision

The exact implementation will be determined during architecture design.

⸻

51. Core Business Rules

The following rules apply across the functional requirements.

BR-001 — Evidence Before Inference

The system should prefer explicit evidence over unsupported inference.

⸻

BR-002 — User Confirmation Has Higher Authority

When a user explicitly corrects a system-generated interpretation, the confirmed user input should take precedence over the previous inference.

⸻

BR-003 — Unknown Is Valid

The system must be able to represent:

“We don’t know.”

Lack of evidence should not automatically become a negative assessment.

⸻

BR-004 — Missing Skill ≠ Lack of Ability

If a skill is not present in the user’s profile, FuturePath should not automatically conclude that the user lacks that skill.

The correct state may be:

UNKNOWN

rather than:

GAP

⸻

BR-005 — Recommendations Must Have a Reason

Important recommendations should be explainable through the user’s profile, target state, evidence, or market information.

⸻

BR-006 — Scores Must Be Explainable

If FuturePath eventually introduces numerical scores, the system should be able to explain the factors contributing to those scores.

⸻

BR-007 — AI Does Not Own the Truth

AI-generated information is subject to review, correction, and uncertainty.

⸻

BR-008 — Market Demand Is Contextual

A skill’s importance may vary by:

* Role
* Geography
* Industry
* Company
* Seniority
* Time

Therefore, FuturePath should avoid treating market demand as universally applicable.

⸻

BR-009 — Career Decisions Remain With the User

FuturePath provides intelligence and recommendations.

The user remains responsible for career decisions.

⸻

52. End-to-End MVP Functional Flow

The initial MVP should support the following complete journey:

                USER
                  │
                  ▼
           Upload Resume
                  │
                  ▼
          Validate Document
                  │
                  ▼
        Extract Career Data
                  │
                  ▼
        Create Career Profile
                  │
                  ▼
        Identify Current Skills
                  │
                  ▼
         User Reviews Profile
                  │
                  ▼
          Select Target Role
                  │
                  ▼
       Analyze Target Role
                  │
                  ▼
          Analyze Skill Gap
                  │
                  ▼
         Prioritize Skill Gaps
                  │
                  ▼
       Generate Recommendations
                  │
                  ▼
           User Takes Action

This is the first meaningful FuturePath value loop.

⸻

53. MVP Functional Requirement Set

The initial MVP should implement the following P0 capabilities:

FR-001   User Account
FR-002   Career Information Ingestion
FR-003   Document Validation
FR-004   Career Information Extraction
FR-005   Career Profile Creation
FR-006   User Review and Correction
FR-007   Skill Identification
FR-008   Skill Evidence
FR-009   Skill Proficiency Representation
FR-010   Target Role Definition
FR-011   Target Role Capability Model
FR-012   Target Role Analysis
FR-013   Skill Gap Analysis
FR-014   Gap Explanation
FR-015   Gap Prioritization
FR-016   Recommendation Generation
FR-017   Recommendation Explanation
FR-018   Career Intelligence Summary
FR-026   Source Traceability
FR-027   Confidence Representation
FR-030*  Data Export
FR-031   Data Deletion
FR-032   Processing Status
FR-033   Retry Failed Processing
FR-034   Idempotent Processing
FR-035   AI Output Classification
FR-036   Human Override
FR-043   Explainability
FR-044   Unsupported Conclusion Handling
FR-047   Auditability

FR-030 may be deferred if necessary for the first implementation, but the underlying data model should not prevent it.

⸻

54. Traceability to Use Cases

Use Case	Primary Functional Requirements
UC-01 Create Career Profile	FR-002 → FR-006
UC-02 Understand Current Skills	FR-007 → FR-009
UC-03 Define Target Career	FR-010 → FR-012
UC-04 Analyze Skill Gap	FR-013 → FR-014
UC-05 Prioritize Skill Gaps	FR-015
UC-06 Personalized Recommendations	FR-016 → FR-017
UC-07 Understand Job Market	FR-019 → FR-020
UC-08 Match User to Job	FR-021 → FR-022
UC-09 Track Career Progress	FR-023 → FR-024
UC-10 Review and Correct AI Output	FR-006, FR-025, FR-028, FR-036

⸻

55. Requirements That Will Drive Architecture

Several requirements are intentionally included because they will create interesting architectural problems later.

Document ingestion

FR-002 → FR-004

Raises questions around:

* Synchronous vs asynchronous processing
* Large documents
* Processing failures
* Retry behavior
* Idempotency

AI extraction

FR-004 → FR-009

Raises questions around:

* Structured output
* Model reliability
* Validation
* Confidence
* Human review
* Evaluation

Source traceability

FR-008
FR-026
FR-047

Raises questions around:

* Provenance
* Data relationships
* Auditability
* Retrieval

Skill-gap intelligence

FR-013 → FR-015

Raises questions around:

* Skill representation
* Matching
* Ranking
* Evidence
* Rules vs LLM reasoning

Recommendations

FR-016 → FR-017

Raises questions around:

* RAG
* Recommendation quality
* Evaluation
* Personalization
* Hallucination control

Future market intelligence

FR-019 → FR-022

Raises questions around:

* Data ingestion
* Freshness
* Deduplication
* Normalization
* Search
* Ranking

These architectural questions should be solved after we understand the requirements, not before.

⸻

56. Architecture Evolution Principle

Functional requirements are expected to evolve.

The architecture should therefore follow:

Requirement
    ↓
Constraint
    ↓
Architecture Problem
    ↓
Options
    ↓
Decision
    ↓
Implementation
    ↓
Measurement
    ↓
Architecture Evolution

A technology should be introduced only when a requirement creates a problem that the technology solves better than simpler alternatives.

For example:

Need asynchronous processing
        ↓
Evaluate:
- synchronous API
- background worker
- queue
- event streaming
        ↓
Choose based on:
- workload
- latency
- reliability
- complexity
- cost

The requirement does not automatically imply a particular technology.

⸻

57. Out of Scope for Functional Requirements

The following are intentionally not specified as implementation requirements yet:

* Kafka
* Redis
* Kubernetes
* OpenShift
* Dedicated vector database
* MCP
* Autonomous agents
* Multiple LLM providers
* Service mesh
* Microservices
* Specific cloud provider
* Specific LLM
* Specific embedding model

These may become justified later by functional or non-functional constraints.

⸻

58. Next Engineering Artifacts

The functional requirements now provide the foundation for the next design stage.

The recommended sequence is:

Product Vision
       ↓
Problem Statement
       ↓
Personas
       ↓
Use Cases
       ↓
Functional Requirements   ← CURRENT
       ↓
Non-Functional Requirements
       ↓
System Context
       ↓
Domain Model
       ↓
High-Level Architecture
       ↓
Technology Evaluation
       ↓
Architecture Decision Records
       ↓
Implementation

The next document should therefore be:

docs/architecture/non-functional-requirements.md

That is where we define measurable expectations for performance, scalability, availability, reliability, security, privacy, observability, maintainability, cost, AI quality, data freshness, and disaster recovery.

Those NFRs will be especially important because they are what will eventually tell us whether FuturePath actually needs things like asynchronous processing, caching, queues, multiple services, Kubernetes, or other distributed-system components.