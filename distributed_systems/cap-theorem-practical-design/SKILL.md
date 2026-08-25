---
name: cap-theorem-practical-design
description: Apply the CAP theorem practically when designing, implementing, scaling, operating, or recovering distributed systems; reason about consistency, availability, partition tolerance, failure modes, data replication, queues, caches, databases, read replicas, conflict resolution, viral traffic events, and user/business tradeoffs.
---

# CAP Theorem Practical Design

Use this skill when a distributed system design or incident requires reasoning about consistency, availability, and partition tolerance.

## Core Idea

The CAP theorem says that when a network partition occurs, a distributed system must choose between:

- consistency: every read sees the latest successful write, or an error
- availability: every request receives a non-error response, though it may be stale or conflicting
- partition tolerance: the system continues operating despite network communication failures between nodes

In real distributed systems, partitions and partial failures happen. So the practical question is usually not "CP or AP forever?" but:

```text
During a partition or partial failure, which operations must preserve consistency, and which operations may remain available with stale or eventually reconciled data?
```

## Practical Translation

CAP is about behavior under failure.

Normal operation may look consistent and available. The design choice becomes visible when:

- replicas cannot communicate
- one region loses connectivity
- one service times out while another keeps running
- a cache is stale
- a database replica lags
- a queue redelivers messages
- a leader election is uncertain
- a write succeeds in one component but not another
- a service times out but may have completed work

## What New Web Apps Usually Experience

A new standard web app may not experience dramatic textbook CAP scenarios at first, especially if it uses:

```text
single primary database
single region
one web app deployment
no read replicas
minimal caching
few async workflows
```

In that setup, the first CAP-like issues usually appear as smaller consistency and availability tradeoffs around:

- browser/CDN caching
- database transactions
- background jobs
- queues
- third-party API timeouts
- webhooks
- email/payment side effects
- stale UI state after writes
- search indexes or denormalized read models
- deployment rollouts with old and new code running at once

For a simple new app, focus on:

- keep source-of-truth data in one primary database
- use database constraints for critical correctness
- keep permission checks and payment/order state strongly consistent
- treat caches, search indexes, and async jobs as derived state
- make background jobs idempotent
- avoid multi-region writes until business needs justify them
- have clear behavior when third-party services fail
- show pending/processing states for async workflows
- do not introduce read replicas until read load actually requires them

## What Changes As The App Scales

As users, throughput, data volume, and operational complexity grow, CAP tradeoffs become more visible.

### More Users

Watch for:

- higher read pressure
- higher write contention
- more concurrent updates
- more cache pressure
- more permission-sensitive access paths

Likely additions:

- caching
- query optimization
- pagination
- background jobs
- read replicas

New tradeoffs:

- stale cache data
- read-after-write issues on replicas
- async processing delays

### More Throughput

Watch for:

- database saturation
- queue backlogs
- lock contention
- external API rate limits
- retries increasing load

Likely additions:

- queues
- rate limits
- backpressure
- worker pools
- batched writes
- circuit breakers

New tradeoffs:

- eventually consistent processing
- duplicate delivery
- delayed visibility
- partial failure recovery

### More Data

Watch for:

- slow queries
- expensive reports
- large table migrations
- index bloat
- full scans
- stale materialized views

Likely additions:

- read models
- materialized views
- search indexes
- partitioning
- warehouses

New tradeoffs:

- source-of-truth vs derived data
- rebuild/replay requirements
- stale reporting/search results

### More Regions Or Global Users

Watch for:

- cross-region latency
- failover behavior
- data residency requirements
- regional outages
- split-brain risk

Likely additions:

- CDN
- regional read replicas
- active/passive failover
- eventually active/active designs

New tradeoffs:

- stale regional reads
- failover data loss windows
- conflict resolution
- regional ownership models

## Organic Scaling Events And Viral Traffic

When an app goes viral, the first failures are often not exotic distributed-consensus failures. They are usually pressure on simple shared resources.

Common failure points:

- database connection pool exhaustion
- slow database queries amplified by traffic
- cache stampedes
- CDN/cache misconfiguration
- too many synchronous third-party API calls
- queue backlogs
- worker saturation
- rate limits
- memory exhaustion
- hot rows or hot keys
- signup/email/payment providers throttling

CAP-related decisions during a viral event:

- Can public pages be served stale from CDN?
- Can non-critical features be degraded or disabled?
- Can writes be queued instead of processed immediately?
- Can read-heavy traffic use cached or replicated data?
- Which operations must fail closed for correctness?
- Which operations may return "processing" or "try again later"?
- Which data must remain strongly consistent even under load?

Practical emergency posture:

- protect the primary database
- cache public/static content aggressively
- shed or rate-limit non-critical traffic
- move slow side effects out of request path
- keep payments, auth, permissions, and critical writes consistent
- accept staleness for dashboards, feeds, search, counts, recommendations, and public content
- monitor queue lag, replication lag, cache hit rate, error rate, and latency
- prefer explicit degraded mode over accidental inconsistency

## Key Terms

### Consistency

Clients see a coherent view of data.

Strong consistency examples:

- account balance after a transfer
- uniqueness of username/email
- inventory reservation
- permissions and access checks
- payment/order state transitions

Eventual consistency examples:

- search indexes
- analytics dashboards
- notification counts
- recommendation feeds
- cached public content
- asynchronously updated read models

### Availability

The system responds to requests.

Availability does not mean "correct latest data." It means the system can return some valid response under failure.

Examples:

- serve stale cached content
- accept writes into a local queue
- show last-known status
- allow offline edits for later sync
- return degraded results

### Partition Tolerance

The system tolerates communication failure between components.

In distributed systems, partition tolerance is not optional. Networks fail, time out, drop packets, and split regions.

## How CAP Applies To Design

For each operation, decide:

- Does this operation require latest data?
- Can this operation return stale data?
- Can writes be accepted during partition?
- What happens if two sides accept conflicting writes?
- How are conflicts detected and resolved?
- What is the user/business impact of rejecting the request?
- What is the user/business impact of accepting a stale/conflicting request?

Do this per workflow, not just per database.

Example:

| Operation | Preferred Behavior Under Partition | Why |
|---|---|---|
| Login permission check | Consistent or fail closed | Security |
| Product browsing | Available with stale data | UX |
| Checkout inventory reservation | Consistent | Avoid oversell |
| Search results | Available with stale index | Acceptable freshness lag |
| Analytics dashboard | Available with stale label | Better than outage |
| Bank transfer | Consistent or reject | Financial correctness |

## CP, AP, And CA In Practice

### CP: Consistency + Partition Tolerance

During partition, the system may reject or block some requests to preserve correctness.

Good fit:

- money movement
- permissions
- inventory reservation
- uniqueness constraints
- critical workflow state
- compliance-sensitive writes

Tradeoff:

- lower availability during failure
- users may see errors or delays

### AP: Availability + Partition Tolerance

During partition, the system continues responding, accepting stale reads or conflicting writes that must be reconciled later.

Good fit:

- feeds
- likes/views
- comments in some products
- collaborative/offline edits with merge rules
- shopping cart drafts
- analytics events
- metrics ingestion
- search indexes

Tradeoff:

- conflict resolution required
- users may see stale or temporarily inconsistent data

### CA: Consistency + Availability

Only realistic when there is no partition or no distributed boundary.

In real distributed systems, do not rely on CA under failure. If network partitions are possible, the design still needs a partition behavior.

## Implementation Patterns

### Strongly Consistent Source Of Truth

Use a primary database, transactions, constraints, or consensus-backed storage for data that must be correct.

Patterns:

- ACID transactions
- unique constraints
- row locks / compare-and-swap
- leader-based writes
- quorum reads/writes where appropriate
- fail closed on permission checks

### Eventually Consistent Read Models

Use derived views for performance or availability.

Patterns:

- event-driven projections
- search indexes
- caches
- materialized views
- async denormalized tables
- vector indexes

Need:

- freshness expectations
- rebuild/replay path
- stale data labeling if user-visible
- source-of-truth fallback for critical actions

### Queues And Async Processing

Queues often create eventual consistency.

Patterns:

- at-least-once delivery
- idempotent consumers
- retries
- dead-letter queues
- reconciliation jobs
- status fields

CAP lens:

- enqueueing may allow request availability
- downstream state updates happen later
- duplicates and partial failures must be safe

### Caches

Caches often trade consistency for latency and availability.

Patterns:

- TTL
- explicit invalidation
- stale-while-revalidate
- cache busting
- tenant/user-safe keys

CAP lens:

- cache can serve during origin failure
- data may be stale
- sensitive operations should bypass or validate against source of truth

### Read Replicas

Read replicas can improve read availability and scale but may be stale.

Patterns:

- route read-after-write to primary
- route stale-tolerant reads to replicas
- monitor replication lag
- fail over carefully

CAP lens:

- during lag/partition, secondary reads may violate latest-write consistency
- choose which reads may be stale

### Multi-Region Systems

Multi-region design forces explicit tradeoffs.

Options:

- active/passive: simpler consistency, slower failover
- active/active: higher availability, conflict resolution needed
- regional read replicas: faster local reads, staleness risk
- global tables: available writes, conflict semantics matter

Questions:

- Can users write in multiple regions?
- What happens if regions disconnect?
- Which region owns which tenant/resource?
- How do you prevent split-brain?
- How do you reconcile conflicts?

## Failure And Recovery

CAP matters most during incidents.

Failure questions:

- Which components are partitioned?
- Which side can accept writes?
- Are reads stale?
- Is there split-brain risk?
- Did both sides accept conflicting state?
- What was acknowledged to users?
- Which system is source of truth?
- What must be reconciled?

Recovery steps:

1. Stop additional damage if consistency is at risk.
2. Identify authoritative source of truth.
3. Measure divergence.
4. Reconcile conflicts.
5. Replay or rebuild derived state.
6. Restore traffic gradually.
7. Add guardrails, tests, or alerts for next time.

## Maintenance And Scaling

As systems scale, CAP tradeoffs often appear in ordinary choices:

- adding read replicas creates stale-read decisions
- adding caches creates invalidation/freshness decisions
- adding queues creates eventual-processing decisions
- adding regions creates conflict/failover decisions
- adding sharding creates cross-shard transaction decisions
- adding search indexes creates source-of-truth vs derived-data decisions

Each scaling component should state:

- what it improves
- what consistency it weakens
- what failure mode it introduces
- how operators detect and recover from that failure

## Workflow

1. Identify the distributed boundary.
   - database replica
   - cache
   - queue
   - service call
   - region
   - browser/client
   - third-party integration
2. Identify the operation.
   - read
   - write
   - transaction
   - side effect
   - derived update
3. Classify consistency need.
   - strong
   - read-your-writes
   - monotonic reads
   - eventual
   - best effort
4. Define partition behavior.
   - reject request
   - serve stale data
   - accept and reconcile later
   - queue for later
   - degrade feature
5. Define conflict behavior.
   - impossible by design
   - last-write-wins
   - merge
   - human review
   - source-of-truth wins
   - reject conflicting write
6. Define observability.
   - replication lag
   - queue lag
   - cache age
   - conflict count
   - failed writes
   - stale-read rate
   - failover events
7. Define recovery plan.
   - source of truth
   - replay/rebuild path
   - reconciliation process
   - user communication if needed

## Output Standard

Start with:

- distributed boundary
- operation/workflow
- consistency requirement
- availability requirement
- partition behavior
- chosen tradeoff
- user/business impact
- recovery strategy

When comparing options, include:

| Option | Consistency | Availability | Failure Mode | Recovery |
|---|---|---|---|---|

For new or scaling web apps, include:

- which CAP-like tradeoffs are relevant now
- which can wait
- what to watch as users/throughput/data scale
- what to do during organic scaling or viral traffic

## Guardrails

- Do not discuss CAP only at the database-brand level; apply it per operation.
- Do not claim a distributed system is simply CA under real network failure.
- Do not add caches, queues, replicas, or regions without naming the consistency tradeoff.
- Do not serve stale data for permissions, payments, or critical state transitions unless explicitly safe.
- Do not accept writes on both sides of a partition without conflict resolution.
- Do not design failover without split-brain prevention.
- Do not treat derived indexes or caches as source of truth unless explicitly designed that way.
- Prefer explicit degradation over accidental inconsistency.
