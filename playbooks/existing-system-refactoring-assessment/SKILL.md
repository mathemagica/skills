---
name: existing-system-refactoring-assessment
description: Coordinate the skills library to assess an existing application or system for refactoring, cleanup, modernization, or rearchitecture by understanding runtime behavior, request flow, architecture, code organization, data model, APIs, performance, observability, deployment, integrations, and operational risk before recommending changes.
when_to_use: Use when reviewing an existing application for cleanup, refactoring, modernization, rearchitecture, legacy system assessment, developer-velocity issues, scaling problems, operational risk, or when the user wants the agent to find and use all relevant skills before changing production code.
argument-hint: "[application-or-system]"
---

# Existing System Refactoring Assessment

Use this playbook when assessing an existing application or system for potential refactoring, cleanup, modernization, or rearchitecture. This is a meta-skill: its job is to select, sequence, and coordinate other skills from the library.

Do not refactor from vibes. First reconstruct how the system actually behaves, where responsibilities live, which workflows matter, what data is authoritative, where failures occur, and which changes would reduce risk or unlock product work.

## Core Principle

Prefer evidence over rewrite energy. A system that is ugly but stable should not be rewritten unless its current shape blocks important work, creates real operational risk, hides important failure modes, or prevents the team from understanding and safely changing it.

## Workflow

### 1. Frame The Assessment

Clarify:

- goal: cleanup, modernization, performance, reliability, developer velocity, security, scaling, product enablement, migration, or incident prevention
- stakeholders and system owners
- user-facing workflows and business-critical paths
- current pain points and recent incidents
- known constraints, deadlines, compliance concerns, and change tolerance

Output assessment scope, success criteria, assumptions, and open questions.

### 2. Map Request And Runtime Flow

Use [`request-flow-tracing`](../../distributed_systems/request-flow-tracing/SKILL.md).

Trace important workflows from browser or client through DNS, CDN, load balancer, app servers, APIs, queues, caches, databases, and third-party systems.

Output a current runtime map and workflow inventory.

### 3. Establish Debugging Evidence

Use [`backend-debugging`](../../software_engineering/backend-debugging/SKILL.md) and [`frontend-debugging`](../../software_engineering/frontend-debugging/SKILL.md) where relevant.

Reproduce concrete issues, inspect runtime behavior, compare expected versus actual behavior, and separate symptoms from causes.

Output an evidence log for important defects, confusing behaviors, and suspected root causes.

### 4. Assess Responsibility Boundaries

Use [`separation-of-concerns`](../../software_engineering/separation-of-concerns/SKILL.md).

Identify mixed concerns such as:

- UI code owning business rules
- controllers or handlers owning persistence details
- models owning integration workflows
- background jobs hiding core domain behavior
- infrastructure concerns leaking into domain code
- duplicated validation, authorization, or transformation logic

Output a responsibility map and boundary problems.

### 5. Assess Server Organization

Use [`full-stack-server-organization`](../../software_engineering/full-stack-server-organization/SKILL.md).

Review whether server code follows framework-native organization around routes, controllers/views, handlers, models, serializers, services, schemas, validators, jobs, and tests.

Output a server structure assessment and cleanup opportunities.

### 6. Assess Framework Fit

Use [`frontend-framework-selection`](../../software_engineering/frontend-framework-selection/SKILL.md) and [`backend-framework-selection`](../../software_engineering/backend-framework-selection/SKILL.md).

Decide whether existing framework choices are still helping, merely unfamiliar, or actively creating maintenance, product, hiring, performance, or operational problems.

Output keep, change, or revisit recommendations for framework choices.

### 7. Review Client/Server Boundaries

Use [`client-server-architecture`](../../software_engineering/client-server-architecture/SKILL.md).

Check whether state ownership, validation, authorization, caching, errors, retries, background work, secrets, and durable workflows sit on the right side of the boundary.

Output a client/server boundary assessment.

### 8. Review API Design

Use [`api-design-best-practices`](../../software_engineering/api-design-best-practices/SKILL.md).

Assess endpoint consistency, authentication, authorization, validation, pagination, filtering, versioning, idempotency, error shape, compatibility, and consumer coupling.

Output API risks and cleanup opportunities.

### 9. Review Data Model And Source Of Truth

Use [`data-modeling-first`](../../data_engineering/data-modeling-first/SKILL.md).

Identify domain entities, relationships, lifecycle states, overloaded tables, missing constraints, duplicated records, unclear ownership, and mismatch between business workflows and persistence.

Output a data model and source-of-truth assessment.

### 10. Review Database Choice And Query Performance

Use [`database-selection`](../../data_engineering/database-selection/SKILL.md) and [`query-optimization`](../../data_engineering/query-optimization/SKILL.md).

Check whether current storage choices fit the workload. Investigate slow paths with explain plans, indexes, access patterns, cardinality, fan-out, joins, scans, document access patterns, vector search constraints, or cache/search/warehouse misuse.

Output storage fit and query optimization findings.

### 11. Assess Scaling And Bottlenecks

Use [`system-scaling-performance`](../../distributed_systems/system-scaling-performance/SKILL.md).

Determine whether bottlenecks are CPU, memory, I/O, network, database, cache, queue, third-party, or request-rate related.

Output a measured bottleneck model and likely scaling limits.

### 12. Review Async Work, Queues, And Idempotency

Use [`sync-async-processing`](../../distributed_systems/sync-async-processing/SKILL.md), [`queue-architecture-patterns`](../../distributed_systems/queue-architecture-patterns/SKILL.md), and [`idempotency-patterns`](../../distributed_systems/idempotency-patterns/SKILL.md).

Identify work incorrectly happening in the request path, missing retries, unsafe retries, duplicate-processing risk, dead-letter queue gaps, and overcomplicated async flows.

Output an async processing and retry-safety assessment.

### 13. Review Caching

Use [`caching-patterns`](../../distributed_systems/caching-patterns/SKILL.md).

Identify whether caches solve a measured bottleneck, whether invalidation is safe, whether freshness expectations are clear, and whether cached data has an obvious source of truth.

Output cache risks and simplification opportunities.

### 14. Review Database Replication Patterns

Use [`primary-secondary-database-architecture`](../../data_engineering/primary-secondary-database-architecture/SKILL.md) if replicas, failover, read scaling, analytics replicas, or reporting copies exist or are being considered.

Check read-after-write behavior, replica lag, failover runbooks, routing logic, and consistency expectations.

Output a replica safety assessment.

### 15. Review Distributed System Tradeoffs

Use [`cap-theorem-practical-design`](../../distributed_systems/cap-theorem-practical-design/SKILL.md).

Name where consistency, availability, and partition-tolerance tradeoffs appear because of caches, queues, replicas, regions, offline behavior, or third-party dependencies.

Output consistency and failure-mode assessment.

### 16. Review Multitenancy

Use [`multitenancy-architecture`](../../distributed_systems/multitenancy-architecture/SKILL.md) if the product has customers, accounts, organizations, workspaces, teams, regions, or tenant-like boundaries.

Assess tenant isolation, authorization, billing, support tooling, data lifecycle, noisy-neighbor risk, and migration complexity.

Output a tenant model assessment.

### 17. Review Third-Party Integrations

Use [`third-party-data-integration`](../../data_engineering/third-party-data-integration/SKILL.md).

Identify systems of record, external ID mapping, sync direction, reconciliation, freshness, retries, observability, rate limits, and failure handling.

Output integration risk assessment.

### 18. Review Environments And Deployment

Use [`environment-management`](../../distributed_systems/environment-management/SKILL.md), [`deployment-management`](../../distributed_systems/deployment-management/SKILL.md), and [`aws-web-app-deployment-defaults`](../../distributed_systems/aws-web-app-deployment-defaults/SKILL.md) if AWS is used.

Assess local/staging/production parity, environment-specific config, secrets, migrations, rollback, deployment safety, cloud defaults, IAM, network boundaries, backups, and disaster recovery.

Output release and environment risk assessment.

### 19. Review Observability

Use [`observability-monitoring`](../../distributed_systems/observability-monitoring/SKILL.md).

Assess whether logs, metrics, traces, health checks, dashboards, deploy markers, and alerts answer the questions engineers ask during incidents, refactors, releases, and debugging sessions.

Output an observability gap list.

### 20. Prioritize Refactoring Work

Group findings by:

- production risk
- user impact
- business impact
- developer friction
- operational risk
- dependency order
- reversibility

Prefer small, reversible improvements before large rewrites.

Explicitly classify recommendations as:

- fix now
- instrument first
- refactor incrementally
- redesign later
- leave alone

Output a prioritized refactoring roadmap.

## Expected Output

When invoked, produce:

1. Assessment scope and system summary
2. Relevant skills selected and why
3. Current request/runtime flow map
4. Current architecture and responsibility map
5. Data model and source-of-truth assessment
6. API and client/server boundary assessment
7. Framework and code organization assessment
8. Performance, scaling, and query findings
9. Async, queue, cache, and idempotency findings
10. Integration, tenancy, deployment, and observability findings
11. Risk-ranked refactoring opportunities
12. Safe first steps
13. Deferred or explicitly avoided changes
14. Suggested implementation sequence

## Default Stance

Do the smallest useful assessment before changing code. If evidence is missing, recommend instrumentation, tests, traces, or focused debugging before proposing a rewrite.

