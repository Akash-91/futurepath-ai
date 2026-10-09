# FuturePath AI — Personas

## 1. Purpose

This document defines the primary user personas for FuturePath AI.

Personas are used to:

- Establish who FuturePath is designed to help.
- Understand user goals, motivations, and pain points.
- Guide product requirements and use-case definition.
- Prevent architecture and feature decisions from being driven by technology rather than user needs.

FuturePath will initially focus on professionals who want to understand their current career position, identify meaningful gaps, and make better career decisions.

---

# 2. Primary Persona — Experienced Professional

## Overview

An experienced professional with several years of work experience who wants to understand their current capabilities, evaluate their readiness for a target role, and determine what they should focus on next.

### Example

A middleware engineer with 8–12 years of experience who wants to transition into a Solution Architect role.

### Goals

- Understand their current professional capabilities.
- Identify transferable skills.
- Determine readiness for a target role.
- Identify meaningful skill gaps.
- Understand which gaps matter most.
- Discover relevant career opportunities.
- Create a practical learning and development plan.
- Track progress over time.

### Pain Points

- Professional information is spread across resumes, job profiles, projects, certifications, and personal knowledge.
- They may know many technologies but struggle to understand their overall capability profile.
- Job descriptions contain large numbers of requirements with no clear prioritization.
- Learning resources are abundant but difficult to prioritize.
- Generic career advice does not account for existing experience.
- It is difficult to distinguish between a genuinely important skill gap and a minor missing keyword.
- They may not know whether their current experience is aligned with market demand.

### Key Questions

> What am I actually good at?

> Where am I weak?

> What does my target role require?

> Which gaps matter most?

> What should I learn next?

> Am I becoming more competitive in the market?

### FuturePath Value

FuturePath should transform fragmented professional information into an evolving career profile and connect that profile with market requirements and actionable recommendations.

---

# 3. Secondary Persona — Career Explorer

## Overview

A professional considering a transition into a different role, specialization, or career direction.

The transition may be within the same broad domain or into a substantially different one.

### Examples

- Middleware Engineer → Solution Architect
- System Administrator → Cloud Engineer
- Software Engineer → AI Engineer
- Developer → Platform Engineer

### Goals

- Understand what the target career actually requires.
- Determine which existing skills are transferable.
- Identify missing capabilities.
- Understand the difficulty and scope of the transition.
- Prioritize learning.
- Identify realistic intermediate steps.

### Pain Points

- Career paths are often presented as generic lists of technologies.
- Existing experience is rarely considered when recommending a new path.
- It is difficult to understand which skills are foundational versus optional.
- Users may spend significant time learning skills that have limited relevance to their intended role.
- There is uncertainty about whether a career transition is realistic.

### Key Questions

> Can I realistically move into this role?

> Which of my existing skills are useful?

> What am I missing?

> What should I learn first?

> What intermediate role could help me get there?

### FuturePath Value

FuturePath should provide a personalized transition path based on the user's existing capabilities, target role, market demand, and identified gaps.

---

# 4. Secondary Persona — Active Job Seeker

## Overview

A professional who is actively searching for new employment opportunities and wants to identify roles where their capabilities are genuinely relevant.

### Goals

- Find relevant job opportunities.
- Understand why a job matches their profile.
- Identify missing requirements.
- Prioritize applications.
- Improve their readiness for target roles.
- Understand how their profile compares with current market requirements.

### Pain Points

- Job boards return large numbers of potentially irrelevant positions.
- Keyword-based matching does not capture transferable skills or experience.
- Job descriptions often contain long lists of requirements without prioritization.
- Users may apply to jobs without understanding their actual gaps.
- A simple match percentage does not explain *why* the match exists.

### Key Questions

> Which jobs are actually relevant to me?

> Why am I a good or poor match?

> What am I missing?

> Is the missing requirement critical or optional?

> Which opportunities should I prioritize?

### FuturePath Value

FuturePath should provide explainable job matching that connects the user's capabilities with job requirements and clearly identifies strengths, gaps, and potential risks.

---

# 5. Persona Comparison

| Attribute | Experienced Professional | Career Explorer | Active Job Seeker |
|---|---|---|---|
| Primary objective | Career development | Career transition | Find relevant opportunities |
| Main question | "Where should I improve?" | "Can I move into this role?" | "Which jobs fit me?" |
| Current experience | Significant | Usually significant | Usually significant |
| Target role | Often defined | May be exploratory | Usually defined |
| Key capability | Career intelligence | Skill-gap analysis | Job matching |
| Major pain point | Lack of direction | Unclear transition path | Too many / poor-quality matches |
| FuturePath value | Personalized career intelligence | Personalized transition path | Explainable opportunity matching |

---

# 6. Common User Needs

Although the personas have different objectives, they share several underlying needs.

### 6.1 Understand the Current State

Users need an accurate representation of:

- Experience
- Skills
- Technologies
- Roles
- Projects
- Certifications
- Areas of expertise
- Evidence supporting those capabilities

### 6.2 Understand the Target State

Users need to understand:

- Target roles
- Required capabilities
- Expected proficiency
- Market demand
- Relevant experience
- Role-specific expectations

### 6.3 Understand the Gap

Users need more than a list of missing skills.

FuturePath should eventually explain:

- What is missing?
- How significant is the gap?
- Why does it matter?
- How frequently is it required?
- Is it foundational or optional?
- What evidence would demonstrate competency?

### 6.4 Decide What to Do Next

Users need actionable recommendations rather than information overload.

Examples:

- Learn a specific concept.
- Complete a project.
- Gain practical experience.
- Improve a specific skill.
- Apply for an intermediate role.
- Consider a particular opportunity.

---

# 7. Persona Design Principles

FuturePath should follow these principles when designing user experiences and intelligence.

## Evidence Over Assumption

The system should distinguish between information explicitly provided by the user and conclusions inferred by AI.

For example:

**Fact**

> User has 5 years of WebSphere experience.

**Inference**

> User may have strong middleware administration capability.

**Recommendation**

> Distributed systems should be prioritized for the user's target Solution Architect role.

These should not be treated as equivalent levels of certainty.

---

## Explainability Over Scores

FuturePath should avoid presenting unexplained scores as authoritative.

Instead of:

> "Your career match is 78%."

Prefer:

> "You have strong alignment in middleware, production operations, and migration. The largest gaps are distributed systems and database architecture, which are frequently required for the target role."

Scores may eventually be useful, but they should be supported by understandable evidence.

---

## Personalization Over Generic Advice

Recommendations should consider:

- Current capabilities
- Experience
- Target role
- Existing knowledge
- Market requirements
- User goals
- Previous progress

The system should not recommend the same generic career path to every user.

---

## Actionability Over Information Volume

FuturePath should help users answer:

> **"What should I do next?"**

rather than simply providing more information.

---

# 8. Initial Target Persona

For the first product iteration, FuturePath will prioritize the **Experienced Professional** persona.

The initial product scenario will focus on a professional who:

1. Has an existing professional background.
2. Provides career information such as a resume.
3. Wants to pursue a target role.
4. Needs to understand their current capabilities.
5. Wants to identify and prioritize skill gaps.
6. Wants actionable recommendations.

This persona provides a strong foundation for the initial vertical slice:

```text
Resume
   ↓
Career Profile
   ↓
Skills & Experience
   ↓
Target Role
   ↓
Skill Gap Analysis
   ↓
Prioritized Recommendations
```

The Career Explorer and Active Job Seeker personas will influence future capabilities without unnecessarily expanding the initial MVP scope.