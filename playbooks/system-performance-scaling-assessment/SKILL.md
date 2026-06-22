---
name: system-performance-scaling-assessment
description: Coordinate the skills library to assess an existing application or system that is slow, identify bottlenecks with evidence, and create a practical scaling plan across request tracing, debugging, query optimization, resource analysis, caching, queues, async processing, database architecture, deployment, observability, and distributed systems tradeoffs.
when_to_use: Use when diagnosing a slow application, API, dashboard, background job, integration, or user workflow; when identifying CPU, memory, I/O, database, network, queue, cache, dependency, concurrency, or request-rate bottlenecks; or when creating a scaling plan for growth, burst traffic, larger datasets, or an organic scaling event.
argument-hint: "[slow-system-or-workflow]"
---

# System Performance Scaling Assessment

Use this playbook when an existing application or system is slow and the user wants to understand why, identify the bottlenecks, and create a scaling plan. This is a meta-skill: its job is to select, sequence, and coordinate other skills from the library.

Do not scale from guesses. First measure where time and resources are spent, then improve the narrowest bottleneck that affects the user workflow or system constraint.

## Core Principle

Start with measurement, query plans, resource usage, and request-path timing before adding architecture. The cheapest scaling fix is often an index, pagination, batching, removing N+1 requests, moving one slow task async, or adding one missing metric.

## Workflow

### 1. Frame The Performance Problem

Clarify:

- slow workflow, endpoint, page, job, dashboard, integration, or user action
- user impact and business urgency
- expected latency, current latency, throughput, error rate, and success criteria
- affected environments, tenants, users, browsers, regions, or time windows
- recent deployments, data growth, traffic changes, incidents, or dependency changes
- current dataset size, request rate, read/write volume, and concurrency

Output a performance problem statement and target latency, throughput, or reliability goal.

### 2. Trace The Request Path

Use `$request-flow-tracing`.

Map browser, DNS, CDN, load balancer, app servers, APIs, workers, queues, caches, databases, and third-party calls for the slow workflow.

Output an end-to-end request and runtime flow.

### 3. Establish Runtime Evidence

Use `$frontend-debugging` and `$backend-debugging`.

Reproduce the slow path and collect:

- browser network waterfall
- frontend render or hydration timing when relevant
- backend logs and request timings
- traces and spans
- profiles
- resource usage
- queue timing
- dependency timing
- database timing

Output an evidence log and timing breakdown.

### 4. Identify System Resource Bottlenecks

Use `$system-scaling-performance`.

Determine whether the system is:

- CPU-bound
- memory-bound
- I/O-bound
- database-bound
- network-bound
- queue-bound
- cache-bound
- dependency-bound
- concurrency-bound
- request-rate-bound

Consider Big-O behavior, request rate, read/write volume, memory growth, and per-request resource cost.

Output bottleneck hypotheses ranked by evidence.

### 5. Analyze Database And Query Performance

Use `$query-optimization`.

Review slow queries, explain plans, indexes, joins, scans, cardinality, fan-out, N+1 patterns, document access patterns, vector search behavior, write amplification, and transaction contention.

Use `$database-selection` if the current storage technology no longer fits the workload.

Output query and datastore findings.

### 6. Review Data Model Fit

Use `$data-modeling-first`.

Check whether the data model matches current access patterns, lifecycle states, relationships, reporting needs, and source-of-truth boundaries.

Output data model bottlenecks or confirmation that the model is not the main issue.

### 7. Review Client/Server And API Efficiency

Use `$client-server-architecture` and `$api-design-best-practices`.

Look for:

- overfetching
- underfetching
- chatty APIs
- missing pagination
- expensive filters or sorts
- synchronous dependency chains
- poor retry behavior
- unclear state ownership
- response shapes that force expensive server work or client work

Output API and boundary performance findings.

### 8. Assess Framework Or Runtime Constraints

Use `$frontend-framework-selection` and `$backend-framework-selection` only if the framework, runtime, rendering model, or deployment shape appears to contribute to the bottleneck.

Distinguish framework misuse from framework mismatch.

Output keep, tune, or revisit recommendations for framework choices.

### 9. Review Sync vs Async Processing

Use `$sync-async-processing`.

Identify work that should leave the request path, such as:

- slow third-party calls
- heavy computation
- imports and exports
- email and notifications
- media processing
- reconciliation
- scheduled work
- analytics or reporting updates

Output a request-path reduction plan.

### 10. Consider Queues For Burst Smoothing

Use `$queue-architecture-patterns`.

Consider queues when write traffic is bursty, processing is retry-prone, third-party rate limits apply, work can complete after the user response, or workers can process at a controlled rate.

Output a queue recommendation, worker model, retry/dead-letter plan, or explicit "not yet."

### 11. Make Retries Safe

Use `$idempotency-patterns`.

Ensure retries, queue jobs, imports, webhooks, scheduled tasks, and third-party calls are duplicate-safe.

Output an idempotency plan for scaling changes.

### 12. Evaluate Caching

Use `$caching-patterns`.

Consider browser, CDN, app, distributed cache, database cache, read model, search index, materialized view, or pipeline cache layers.

Before adding a cache, name:

- source of truth
- freshness requirement
- invalidation strategy
- failure behavior
- observability signals

Output a cache plan or explicit "not yet."

### 13. Evaluate Database Scaling Patterns

Use `$primary-secondary-database-architecture`.

Consider read replicas only after query, index, and data-model improvements are understood.

Review replica lag, read-after-write behavior, failover, reporting load, read routing, and consistency expectations.

Output a primary/secondary recommendation or deferral.

### 14. Name Distributed Systems Tradeoffs

Use `$cap-theorem-practical-design`.

For queues, caches, replicas, regions, async workflows, offline behavior, or third-party dependencies, identify consistency, availability, partition, freshness, and recovery tradeoffs.

Output failure-mode and consistency notes.

### 15. Review Deployment And Infrastructure Limits

Use `$environment-management`, `$deployment-management`, and `$aws-web-app-deployment-defaults` if AWS is used.

Assess:

- instance, container, or function sizing
- autoscaling policy
- concurrency settings
- connection pools
- load balancer behavior
- CDN use
- database capacity
- worker capacity
- environment parity
- migration and rollout safety

Output infrastructure scaling findings.

### 16. Review Observability

Use `$observability-monitoring`.

Check whether logs, metrics, traces, dashboards, health checks, deploy markers, and alerts can prove where time and resources go.

If not, instrument first.

Output observability gaps and required instrumentation.

### 17. Create The Scaling Plan

Prioritize fixes by:

- user impact
- bottleneck evidence
- confidence
- cost
- implementation risk
- reversibility
- operational complexity

Classify recommendations as:

- tune now
- instrument first
- optimize queries or data access
- move async
- cache selectively
- scale infrastructure
- redesign later
- leave alone

Output a staged scaling roadmap and verification plan.

## Expected Output

When invoked, produce:

1. Performance problem statement and target latency, throughput, or reliability goal
2. Relevant skills selected and why
3. End-to-end request/runtime flow
4. Evidence and timing breakdown
5. Bottleneck hypotheses ranked by evidence
6. Query, datastore, and data model findings
7. API, frontend, backend, and request-path findings
8. Resource profile: CPU, memory, I/O, database, network, queue, cache, dependency, and concurrency
9. Caching, queue, async, replica, and infrastructure recommendations
10. Observability gaps
11. Risk-ranked scaling plan
12. Quick wins
13. Instrumentation-first tasks
14. Deferred architecture changes
15. Verification plan

## Default Stance

Fix the measured bottleneck before adding a new architectural component. If the system cannot prove where time or resources are going, add the missing instrumentation before changing architecture.

