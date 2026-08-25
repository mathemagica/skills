---
name: data-modeling-first
description: Design new projects from the data model first by identifying business use cases, user interactions, core entities, relationships, events, constraints, lifecycle states, ownership, and access patterns before implementation.
---

# Data Modeling First

Use this skill when planning a new project or system component whose behavior depends on shared business concepts, durable records, user interactions, events, or reporting needs.

## Why Data Modeling Comes First

A data model is the shared map of what the system knows, what it remembers, and what it treats as true.

Start with the data model before implementation because it clarifies:

- what the business actually needs to track
- what users create, view, change, approve, delete, or search
- which concepts are real entities versus temporary UI state
- which relationships matter
- which rules protect correctness
- which lifecycle states exist
- which workflows need history or auditability
- which queries must be fast or reliable
- which data belongs in source-of-truth storage versus derived views, caches, indexes, or analytics outputs

Starting with screens or code alone often hides ambiguity. Starting with the data model reveals the nouns, relationships, constraints, and state transitions that every interface, API, workflow, and report will depend on.

## Relationship To Business Use Cases

Business use cases explain why the data exists.

For each use case, identify:

- actor: who performs the action
- goal: what outcome they need
- object: what business entity they act on
- action: create, review, approve, update, search, export, reconcile, archive, delete
- decision: what rule or status changes
- evidence: what must be retained for trust, audit, reporting, or debugging
- reporting need: what the business later needs to measure

A good data model should make business questions answerable without reverse-engineering application behavior.

Examples:

- If users approve applications, the model probably needs `Application`, `Applicant`, `Review`, `ApprovalDecision`, status history, timestamps, and reviewer identity.
- If users compare policies, the model probably needs `Policy`, `Jurisdiction`, `Topic`, `Version`, extracted sections, citations, and search/index metadata.
- If users upload media, the model probably needs `File`, `Owner`, `StorageObject`, `ProcessingJob`, `DerivedArtifact`, permissions, and lifecycle state.

## Relationship To User Interactions

User interactions reveal how data changes over time.

For each interaction, ask:

- What record is created?
- What field or relationship changes?
- What must be validated?
- What permissions apply?
- What happens if the user cancels, retries, edits, or deletes?
- What state does the user expect to see later?
- What history must be preserved?
- What derived data, notifications, jobs, or indexes are triggered?

UI state is often temporary. Domain state is durable. The data model helps separate the two.

## Core Concepts

### Entity

A durable thing the business recognizes.

Examples:

- user
- organization
- account
- order
- document
- meeting
- policy
- task
- job
- invoice

### Attribute

A property of an entity.

Examples:

- title
- status
- created_at
- amount
- email
- source_url

### Relationship

How entities connect.

Examples:

- user belongs to organization
- order has many line items
- document has many versions
- policy applies to jurisdiction
- task is assigned to user

### Event

Something that happened and may need history.

Examples:

- submitted
- approved
- exported
- imported
- synced
- failed
- retried

### State

A durable condition that affects behavior.

Examples:

- draft
- pending_review
- approved
- rejected
- archived
- failed
- processing

### Constraint

A rule that must remain true.

Examples:

- email is unique
- invoice total equals sum of lines
- only approved policies can publish
- archived records cannot be edited
- one active subscription per account

### Derived Data

Data computed from source-of-truth records.

Examples:

- search indexes
- vector embeddings
- dashboard aggregates
- denormalized read models
- cached counts
- materialized views

Derived data must have a refresh or invalidation plan.

## Workflow

1. Identify the business goal.
   - What problem is this system solving?
   - What decision, workflow, or user outcome does it support?
2. List actors and user interactions.
   - Who uses the system?
   - What do they create, view, edit, approve, search, export, or delete?
3. Extract candidate entities.
   - Pull out the durable nouns from use cases and interactions.
   - Separate true business entities from UI-only concepts and derived artifacts.
4. Define relationships.
   - one-to-one
   - one-to-many
   - many-to-many
   - ownership
   - containment
   - versioning
   - dependency
   - lineage
5. Define lifecycle states and events.
   - What statuses exist?
   - What transitions are allowed?
   - What events need history?
   - Who or what causes each transition?
6. Define constraints and invariants.
   - What must always be true?
   - What must be unique?
   - What requires authorization?
   - What must be auditable?
7. Identify access patterns.
   - What does the UI need to load?
   - What does the API need to expose?
   - What reports need to aggregate?
   - What search or filter operations matter?
   - What writes must be transactional?
8. Decide source-of-truth versus derived data.
   - What is canonical?
   - What is cached?
   - What is indexed?
   - What is generated?
   - What can be rebuilt?
9. Sketch the model.
   - Entities
   - Attributes
   - Relationships
   - States
   - Events
   - Constraints
   - Derived views/indexes
10. Validate against use cases.
   - Can each user interaction be represented?
   - Can each business question be answered?
   - Are permissions and ownership clear?
   - Are lifecycle transitions explicit?
   - Are reporting and audit needs supported?
11. Translate into implementation shape.
   - database tables or collections
   - schema definitions
   - API resources
   - domain services
   - event logs
   - read models
   - analytics outputs

## Output Standard

Start with a compact data model summary:

- business goal
- actors
- core entities
- key relationships
- lifecycle states
- important constraints
- source-of-truth records
- derived data/indexes
- access patterns
- open questions

When useful, include a simple ER-style sketch:

```text
Organization 1--* User
User 1--* Project
Project 1--* Task
Task *--1 Status
Task 1--* Comment
```

Then explain how the model supports the business use cases and user interactions.

## Why This Matters

A good data model reduces downstream confusion because it becomes the contract between:

- product requirements
- user experience
- API design
- database design
- permissions
- workflows
- analytics
- search
- integrations
- tests

When the data model is weak, every layer compensates with special cases. When it is clear, the rest of the system has something stable to build around.

## Guardrails

- Do not start with tables before understanding business concepts.
- Do not start with screens before identifying durable domain state.
- Do not confuse UI state with source-of-truth data.
- Do not treat derived data as canonical unless explicitly designed that way.
- Do not over-normalize or denormalize before identifying access patterns.
- Do not introduce events, audit logs, or versioning without a clear business or operational need.
- Do not ignore permissions, lifecycle states, or deletion/retention rules.
- Prefer a simple model that explains the business over a clever schema that only explains the implementation.
