---
name: system-scaling-performance
description: Analyze and improve system scaling and performance by identifying CPU, memory, I/O, network, database, and request-rate bottlenecks; use Big-O reasoning, resource profiling, request-category read/write rates, caching, memoization, batching, concurrency controls, and architectural scaling options.
---

# System Scaling Performance

Use this skill when a system, service, endpoint, job, or workflow needs to handle more load, reduce latency, reduce cost, or avoid resource exhaustion.

## First Principle

Performance tuning starts with measurement.

Do not guess whether the system is CPU-bound, memory-bound, I/O-bound, network-bound, database-bound, or lock-bound. Identify the limiting resource, then choose the smallest improvement that changes that limit.

## When To Use

- A service slows down under load.
- An endpoint has high latency or unstable tail latency.
- A job takes too long or uses too much memory.
- Servers run out of CPU, memory, disk, network, file handles, workers, or database connections.
- A system needs capacity planning before launch.
- A team is considering caching, memoization, queues, replicas, sharding, batching, streaming, or async workers.
- A code path appears inefficient and needs Big-O analysis.
- Different request types have different data read/write rates and scaling impact.

## Goal

Find the bottleneck, explain why it limits scaling, and recommend measured optimization or architecture changes with clear tradeoffs.

## Core Concepts

### CPU-Bound

A system is CPU-bound when performance is limited by computation.

Signals:

- high CPU utilization
- request latency rises with computation-heavy inputs
- profiling shows expensive functions, parsing, serialization, compression, encryption, sorting, regex, rendering, ML inference, or tight loops

Optimization paths:

- improve algorithmic complexity
- reduce repeated computation
- memoize deterministic expensive calls
- batch work
- parallelize if safe
- move heavy work to background jobs
- use compiled/vectorized/native libraries
- scale out workers if work is parallelizable

Tradeoffs:

- parallelism can increase memory and contention
- memoization uses memory
- background work changes freshness and user feedback

### Memory-Bound

A system is memory-bound when performance or stability is limited by available RAM.

Signals:

- out-of-memory crashes
- swap usage
- garbage collection pauses
- high heap growth
- large object retention
- too many concurrent requests
- loading whole datasets into memory
- unbounded queues, caches, maps, lists, buffers, or result sets

Optimization paths:

- stream data instead of loading all at once
- paginate or chunk large operations
- bound queues and caches
- reduce object duplication
- avoid retaining request-scoped data globally
- use compact data structures
- free references earlier
- tune concurrency limits
- move large blobs to object storage
- use external cache/storage when appropriate

Tradeoffs:

- streaming can complicate code
- smaller concurrency improves stability but may reduce throughput
- external storage adds latency and operational complexity

### I/O-Bound

A system is I/O-bound when waiting on disk, database, file storage, external APIs, or network dominates.

Signals:

- low CPU but high latency
- slow database queries
- high disk read/write wait
- many remote calls per request
- large payload transfers
- external API latency dominates

Optimization paths:

- reduce round trips
- batch calls
- cache repeated reads
- add indexes or read models
- compress or reduce payloads
- parallelize independent I/O with limits
- use queues for slow side effects
- colocate services or data when latency matters

Tradeoffs:

- caching needs invalidation
- batching can increase tail latency if poorly tuned
- parallel I/O can overload dependencies

### Network-Bound

A system is network-bound when bandwidth, latency, connection setup, or cross-region traffic limits performance.

Optimization paths:

- reduce payload size
- avoid chatty APIs
- use pagination and field selection
- compress responses
- cache at edge or client
- colocate services
- reuse connections
- use async/background transfer for large data

### Database-Bound

A system is database-bound when the database is the limiting shared resource.

Signals:

- high query latency
- connection pool exhaustion
- lock waits
- high read/write IOPS
- slow queries
- replication lag
- hot rows or partitions

Optimization paths:

- optimize queries
- add appropriate indexes
- reduce N+1 patterns
- cache stable reads
- add read replicas for read-heavy workloads
- partition or shard when necessary
- move analytics off the primary database
- introduce write queues or event streams for bursty writes

## Big-O Reasoning

Use Big-O notation to predict how work grows as input size, request volume, or data volume grows.

Common patterns:

- `O(1)`: direct lookup or fixed work
- `O(log n)`: indexed lookup or tree search
- `O(k)`: work proportional to returned items
- `O(n)`: scan over all items
- `O(n log n)`: sorting or grouping large inputs
- `O(n^2)`: nested comparison loops, pairwise matching, repeated scans
- `O(n * m)`: joining or comparing two collections naively
- `O(requests * dependencies)`: remote-call fanout
- `O(concurrency * per-request-memory)`: memory pressure from simultaneous requests

Use Big-O to ask:

- What input size controls runtime?
- What data structure is being scanned?
- Does each request do work proportional to all users, all records, or all history?
- Does the system repeat work it could reuse?
- Does concurrency multiply memory usage?
- Does request fanout multiply dependency load?

## Request Category Resource Modeling

For each category of incoming request, estimate:

- request rate: requests per second/minute/hour
- CPU time per request
- memory allocated per request
- peak memory retained per request
- database reads per request
- database writes per request
- cache reads/writes per request
- external API calls per request
- disk/object storage reads/writes per request
- network bytes in/out
- background jobs created
- lock/transaction duration
- expected concurrency
- p50/p95/p99 latency target

Use a table:

| Request Category | Rate | CPU | Memory | DB Reads | DB Writes | External Calls | Bytes Out | Bottleneck Risk |
|---|---:|---:|---:|---:|---:|---:|---:|---|

This makes scaling concrete. A rare admin report and a hot user-facing read endpoint should not be optimized the same way.

## How Code Uses System Memory

Memory is consumed by:

- loaded objects and data structures
- request bodies and response buffers
- database result sets
- ORM entities and identity maps
- JSON parsing and serialization
- file buffers
- caches and memoized values
- queues and worker pools
- thread stacks
- connection pools
- language runtime overhead
- garbage collector metadata
- native libraries and memory outside the managed heap

Common memory traps:

- reading entire files into memory
- loading all rows instead of paginating/streaming
- unbounded in-process caches
- retaining references after request completion
- accumulating logs/events in arrays
- large ORM object graphs
- high concurrency with large per-request allocations
- response buffering for large exports

## Scaling Limits Of System Memory

Memory limits are reached when:

- working set exceeds RAM
- heap grows faster than GC can reclaim
- per-request memory multiplied by concurrency exceeds available memory
- cache grows without bounds
- queues grow faster than workers drain them
- large jobs compete with request handling
- the OS starts swapping
- container memory limits kill the process

Capacity estimate:

```text
safe_concurrency ~= available_memory_for_app / peak_memory_per_request
```

Then reduce this by headroom for runtime, caches, connection pools, background work, fragmentation, and traffic spikes.

## When To Add Architectural Components

### Memoization

Use memoization for expensive deterministic computations within a bounded scope.

Good fit:

- pure function result reuse
- repeated calculation during one request or job
- stable derived values

Avoid when:

- inputs are huge
- results are user-specific without careful keys
- memory cannot be bounded
- data freshness is unclear

### Caching

Use caching when repeated reads are expensive and some staleness is acceptable.

Decide:

- cache key
- TTL
- invalidation
- permission boundaries
- max size
- stampede protection
- stale behavior
- observability

### Queues / Background Jobs

Use queues when work is slow, bursty, retryable, or not required for immediate response.

Tradeoffs:

- eventual consistency
- retry/idempotency requirements
- operational monitoring
- delayed user feedback

### Read Replicas

Use read replicas when read load exceeds the primary database's capacity and slightly stale reads are acceptable.

Tradeoffs:

- replication lag
- read-after-write consistency issues
- routing complexity

### Partitioning / Sharding

Use partitioning or sharding when data size, write throughput, or hot partitions exceed what one logical store handles well.

Tradeoffs:

- operational complexity
- cross-shard queries
- rebalancing
- transaction limitations

### Streaming / Incremental Processing

Use streaming when data is too large to hold in memory or latency matters during long operations.

Tradeoffs:

- more complex control flow
- partial failure handling
- harder testing

## Workflow

1. Define the symptom.
   - latency
   - throughput
   - error rate
   - memory exhaustion
   - CPU saturation
   - cost
2. Capture baseline metrics.
   - p50/p95/p99 latency
   - request rate
   - CPU
   - memory
   - GC
   - DB latency
   - I/O wait
   - network
   - queue depth
3. Categorize request types and read/write rates.
4. Identify the likely bound resource.
5. Profile the hot path.
6. Apply Big-O reasoning to the dominant code or data access path.
7. Pick the smallest optimization:
   - algorithm/data structure
   - query/index
   - memory reduction
   - cache/memoization
   - batching
   - streaming
   - concurrency limit
   - background job
   - architectural component
8. Re-measure under comparable load.
9. Report the bottleneck, fix, before/after metrics, tradeoffs, and remaining capacity risk.

## Output Standard

Start with:

- observed symptom
- likely bottleneck
- evidence needed or available
- request categories affected
- recommended next measurement or fix

When proposing a fix, include:

- why it targets the bottleneck
- expected impact
- tradeoffs
- verification plan
- rollback plan if risky

## Guardrails

- Do not scale infrastructure before identifying the limiting resource.
- Do not add caching without a freshness and invalidation plan.
- Do not increase concurrency when memory or downstream dependencies are already saturated.
- Do not optimize rare paths before hot request categories.
- Do not use averages alone; inspect tail latency.
- Do not assume CPU, memory, database, and network bottlenecks have the same fix.
- Do not ignore per-request read/write rates when estimating scale.
- Prefer measured bottleneck removal over broad rewrites.
