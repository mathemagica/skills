---
name: new-web-app-from-scratch
description: Coordinate the skills library to plan and build a new web application from scratch, moving from product concept through data modeling, datastore choice, frontend and backend framework selection, client-server architecture, API design, server organization, deployment, observability, and selective use of distributed systems patterns.
when_to_use: Use when starting a new web app, SaaS app, internal tool, dashboard, portal, marketplace, or full-stack product, especially when the user wants the agent to find and use all relevant engineering skills in the right order before or during implementation.
argument-hint: "[product-idea-or-web-app]"
---

# New Web App From Scratch

Use this playbook when planning, designing, or starting implementation of a new web application. This is a meta-skill: its job is to select, sequence, and coordinate other skills from the library.

The goal is to start simple without skipping the decisions that make a system understandable, changeable, deployable, and operable.

## Core Principle

Start with product workflows and data ownership, then move outward to storage, frontend shape, backend shape, architecture, APIs, code organization, deployment, and operations. Add queues, caches, replicas, multitenancy, or advanced distributed systems patterns only when the product shape or evidence justifies them.

## Workflow

### 1. Frame The Product

Clarify:

- target users and primary use cases
- core workflows and user interactions
- business goal and success criteria
- permissions, roles, tenants, or customer boundaries
- data sensitivity, compliance, and audit expectations
- launch constraints, expected traffic, and operational tolerance

Output a short product brief, assumptions, and open questions.

### 2. Start With The Data Model

Use `$data-modeling-first`.

Identify:

- business concepts and domain entities
- relationships and cardinality
- lifecycle states and state transitions
- source-of-truth records
- user interactions that create, update, or read data
- access patterns, reporting needs, and audit needs

Output an initial conceptual data model and major domain objects.

### 3. Choose Storage

Use `$database-selection`.

Default to a relational database for standard transactional web apps unless the data shape, scale, latency, query pattern, or product requirement points elsewhere.

Consider document stores, vector databases, search indexes, caches, warehouses, or mixed storage only when the workload needs them.

Output a datastore recommendation with tradeoffs and deferred storage decisions.

### 4. Choose Frontend Framework And Rendering Shape

Use `$frontend-framework-selection`.

Decide:

- whether the app is mostly content, CRUD, dashboard, workflow, collaboration, or rich interaction
- whether it needs static generation, server rendering, server templates, client-side rendering, islands, or progressive enhancement
- which framework best fits team experience, ecosystem needs, backend integration, deployment constraints, and maintenance expectations

Output a frontend framework and rendering model recommendation with one reasonable alternative.

### 5. Choose Backend Framework And Server Shape

Use `$backend-framework-selection`.

Decide:

- whether the backend should be a full-stack monolith, modular monolith, API-first backend, server-rendered app, backend-for-frontend, serverless function set, or separate service
- which backend framework best fits the data model, API style, team experience, language ecosystem, deployment target, background work, integrations, and operational needs
- whether framework conventions support migrations, auth, validation, serialization, admin workflows, jobs, testing, and observability

Output a backend framework and server architecture recommendation with one reasonable alternative.

### 6. Define Client/Server Boundaries

Use `$client-server-architecture`.

Decide what belongs in:

- browser or mobile client
- backend request handlers
- API contract
- durable storage
- background workers
- external services
- shared types or schemas

Output a first system architecture sketch and responsibility map.

### 7. Design APIs

Use `$api-design-best-practices`.

Define:

- resources, commands, or operations
- request and response shapes
- authentication and authorization model
- validation and error behavior
- pagination, filtering, sorting, and search behavior
- compatibility and versioning expectations
- idempotency requirements for retry-prone operations

Output an API contract outline.

### 8. Organize Server Code

Use `$full-stack-server-organization`.

Choose framework-native organization for:

- routes or URL dispatch
- controllers, views, handlers, or endpoints
- models and persistence
- services or use cases
- serializers, schemas, or presenters
- validators and policies
- background jobs
- integration clients
- tests

Output the recommended backend structure and module boundaries.

### 9. Separate Responsibilities Early

Use `$separation-of-concerns`.

Keep UI, API handling, business rules, persistence, background work, integrations, and infrastructure concerns distinct enough that each can be tested and changed independently.

Output a responsibility map and the first boundaries worth preserving.

### 10. Decide Sync vs Async

Use `$sync-async-processing`.

Keep simple reads and writes in the request path. Consider async workers, task schedulers, or queues for work that is slow, retry-prone, bursty, scheduled, dependency-heavy, or not required for the immediate user response.

Output a request-path versus worker-path decision list.

### 11. Add Queues Only When Needed

Use `$queue-architecture-patterns` when the app needs background jobs, webhook handling, imports, email, media processing, rate-limit management, retries, delayed processing, or burst smoothing.

If no queue is needed yet, say so explicitly and name the trigger that would change the decision.

Output a queue recommendation or a clear "not yet."

### 12. Make Risky Operations Idempotent

Use `$idempotency-patterns`.

Apply idempotency to:

- creates with client retries
- payments or billing
- webhooks
- imports and syncs
- queue jobs
- third-party integrations
- scheduled processing

Output an idempotency key and retry-safety plan for relevant workflows.

### 13. Plan Caching Conservatively

Use `$caching-patterns`.

Start with browser, CDN, static asset caching, and database indexes before adding application-level or distributed caches.

Only cache after naming:

- source of truth
- freshness requirements
- invalidation strategy
- failure behavior
- observability signals

Output a cache plan or an explicit "not yet."

### 14. Plan Environments

Use `$environment-management`.

Start with:

- local
- staging
- production

Add preview, QA, pre-production, sandbox, demo, or disaster recovery environments only when the team workflow, risk profile, or business requirements justify them.

Output an environment map and promotion expectations.

### 15. Plan Deployment

Use `$deployment-management`.

Define:

- build artifacts
- environment variables and secrets
- database migrations
- rollout strategy
- verification steps
- rollback path
- ownership and release process

Output a deployment checklist suitable for the first production release.

### 16. Pick Cloud Defaults

Use `$aws-web-app-deployment-defaults` if AWS is the target platform.

Choose conservative defaults for DNS, TLS, CDN, compute, database, IAM, secrets, logging, monitoring, backups, and least-privilege access.

Output an AWS baseline architecture when relevant.

### 17. Add Observability

Use `$observability-monitoring`.

Define the minimum useful:

- structured logs
- metrics
- traces
- health checks
- dashboards
- deploy markers
- alerts
- runbook notes

Output a minimum viable observability plan.

### 18. Consider Advanced Concerns Only When The Product Calls For Them

Use these selectively:

- `$multitenancy-architecture` for SaaS, B2B apps, tenant isolation, billing, or customer-specific permissions.
- `$third-party-data-integration` for vendor APIs, CRMs, payments, calendars, warehouses, imported datasets, or external systems of record.
- `$primary-secondary-database-architecture` for read scaling or high availability after query and index tuning.
- `$cap-theorem-practical-design` when introducing distributed state, replicas, queues, caches, regions, offline behavior, or availability/consistency tradeoffs.
- `$system-scaling-performance` when projecting or diagnosing throughput, CPU, memory, I/O, database pressure, queue depth, or request rate.
- `$frontend-debugging` and `$backend-debugging` once implementation has behavior to inspect.

## Expected Output

When invoked, produce:

1. Product and user workflow summary
2. Relevant skills selected and why
3. Recommended skill execution order
4. Initial data model
5. Frontend framework and rendering model recommendation
6. Backend framework and server architecture recommendation
7. Architecture outline
8. API and backend organization plan
9. Environment and deployment plan
10. Observability baseline
11. Explicit deferred decisions
12. Implementation checklist

## Default Stance

A new web app usually needs a clear data model, a transactional datastore, appropriate frontend and backend framework choices, a well-defined client/server/API boundary, framework-native server organization, local/staging/production environments, basic deployment safety, and useful observability before it needs queues, distributed caching, read replicas, or multi-region architecture.

When the user asks to start building immediately, still do the smallest useful pass through this playbook before writing code.
