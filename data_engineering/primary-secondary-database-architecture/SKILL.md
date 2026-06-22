---
name: primary-secondary-database-architecture
description: Design, evaluate, or debug primary/secondary database architectures, including primary writes, secondary reads, replication lag, failover, read scaling, consistency tradeoffs, read replicas, follower nodes, standby databases, and operational risks.
when_to_use: Use when deciding whether to add read replicas, scale database reads, separate read/write traffic, improve availability, design failover, or explain primary/secondary replication patterns in relational, document, search, cache, or distributed data systems.
argument-hint: "[database-or-workload]"
---

# Primary Secondary Database Architecture

Use this skill when a system needs to scale database reads, improve availability, separate read/write traffic, or reason about replicated database topology.

## Core Idea

In a primary/secondary architecture, one database node is the authoritative writer, and one or more secondary nodes replicate data from it.

Common names:

- primary / secondary
- leader / follower
- master / replica
- writer / read replica
- source / replica
- active / standby

Prefer `primary/secondary` or `leader/follower` in new writing.

## What It Is Useful For

Primary/secondary replication is useful for:

- scaling read-heavy workloads
- reducing load on the primary database
- isolating expensive reporting queries
- improving availability with standby nodes
- supporting disaster recovery
- enabling backups from replicas
- serving geographically closer reads in some systems
- separating operational traffic from analytics or admin traffic

The core pattern:

```text
Writes -> Primary
Reads  -> Primary or Secondary replicas
Replication: Primary -> Secondaries
```

## How It Helps Scale

The primary handles writes and authoritative consistency. Secondary replicas handle eligible reads.

This helps when:

- reads greatly outnumber writes
- read queries are expensive enough to affect writes
- dashboards or admin tools compete with user-facing traffic
- application servers can route stale-tolerant reads to replicas
- the primary database is CPU, I/O, or connection-bound due to read load

It does not automatically help when:

- the workload is write-heavy
- reads must always see the latest write
- replication lag is unacceptable
- the bottleneck is bad queries or missing indexes
- the application cannot distinguish read-after-write paths
- all traffic still goes to the primary

## Systems That Use This Pattern

Common examples:

- PostgreSQL read replicas / streaming replication
- MySQL replicas
- SQL Server Always On readable secondaries
- MongoDB replica sets
- Redis primary-replica setups
- Elasticsearch/OpenSearch primary and replica shards, though query routing differs from classic SQL read replicas
- Cassandra/Scylla/Dynamo-style systems have replication, but not always a single-primary model
- Cloud-managed databases like Amazon RDS/Aurora, Cloud SQL, AlloyDB, Azure SQL, and MongoDB Atlas
- Search, cache, and analytical systems may use related replica patterns for availability and read distribution

Be precise: not every replicated system is a primary/secondary system. Some systems are multi-leader, leaderless, consensus-based, or shard-replicated.

## Workflow

1. Identify the workload.
   - read-heavy
   - write-heavy
   - mixed
   - reporting/dashboard
   - request-path reads
   - background jobs
2. Identify the current database system and replication model.
3. Classify reads.
   - must be strongly consistent
   - can tolerate stale data
   - read-after-write required
   - admin/reporting only
   - cacheable
4. Identify the bottleneck.
   - primary CPU
   - primary I/O
   - connection pool
   - slow queries
   - locks
   - analytics load
   - network latency
5. Decide whether replicas address the actual bottleneck.
6. Design read routing.
   - writes go to primary
   - read-after-write goes to primary
   - stale-tolerant reads may go to secondary
   - heavy reports may go to dedicated replica
7. Account for replication lag.
   - measure lag
   - expose lag metrics
   - define acceptable staleness
   - route consistency-sensitive reads to primary
8. Plan failover.
   - automatic or manual promotion
   - application reconnection behavior
   - DNS/proxy/load balancer behavior
   - split-brain prevention
   - recovery of old primary
9. Verify with load tests and failure tests.
10. Document routing, consistency, lag expectations, and operational runbooks.

## Consistency Tradeoffs

Primary reads usually provide the freshest data.

Secondary reads may be stale because replication is often asynchronous.

Common failure modes:

- user creates a record, then cannot see it immediately
- permission update is not visible on a replica yet
- dashboards show old values
- background worker reads stale state and takes the wrong action
- failover promotes a replica that has not received the latest writes

Use primary reads for:

- read-after-write flows
- auth and permission checks
- payment/order state transitions
- critical workflow decisions
- uniqueness or constraint-sensitive logic

Use secondary reads for:

- browsing/list pages that tolerate slight staleness
- reports
- search-like exploration
- dashboards
- exports
- admin tools
- background analysis

## Read Routing Patterns

Common patterns:

- all writes to primary, all reads to primary: simplest, no read scaling
- writes to primary, selected reads to replicas: common read-scaling setup
- dedicated reporting replica: protects primary from expensive queries
- region-local read replicas: improves read latency but increases staleness risk
- primary fallback: if replica lag is too high, route to primary
- sticky primary reads after write: user reads from primary briefly after writing

## Operational Concerns

Track:

- replication lag
- replica health
- failover events
- replication slot/binlog/WAL growth
- primary write load
- read distribution
- connection pool usage by primary versus replicas
- query load on each replica
- backup and restore status

Risks:

- replica lag hides fresh data
- replicas amplify cost
- bad queries copied to replicas are still bad queries
- failover can break clients if connection routing is brittle
- split-brain can corrupt data in poorly managed systems
- schema migrations must be replication-aware
- replicas may not support every query mode or isolation level

## When Not To Use This Pattern

Do not reach for primary/secondary first when:

- the workload is small
- query optimization would solve the issue
- writes are the bottleneck
- strict consistency is required for most reads
- operational capacity is limited
- the database already has unused headroom
- caching or materialized views are a better fit
- analytics should be moved to a warehouse instead

## Output Standard

Start with:

- current database system
- workload shape
- bottleneck
- whether primary/secondary helps
- consistency risk
- recommended topology

When recommending replicas, include:

- which reads move to secondaries
- which reads must stay on primary
- expected scaling benefit
- replication lag tolerance
- failover plan
- monitoring requirements
- tradeoffs and risks

## Guardrails

- Do not use replicas as a substitute for query optimization.
- Do not route authorization or critical read-after-write checks to stale replicas.
- Do not assume replication is synchronous unless verified.
- Do not call every replicated database primary/secondary.
- Do not add replicas without observability for lag and health.
- Do not design failover without considering split-brain and client reconnection.
- Prefer the simplest topology that solves the measured bottleneck.
