---
name: query-optimization
description: Diagnose and improve slow queries across relational, document, key-value, search, analytical, graph, time-series, and vector databases by identifying the current database choice, reading the relevant query plan or profiling output, reasoning about complexity and access patterns, and choosing safe optimization paths with clear tradeoffs.
when_to_use: Use when someone reports a slow query, endpoint, report, dashboard, search, retrieval, ORM call, aggregation, or database-backed workflow, especially when the right diagnostic method depends on the database type.
argument-hint: "[query-or-endpoint-or-workload]"
---

# Query Optimization

Use this skill when a database-backed operation is slow and needs diagnosis before changing indexes, schema, query shape, caching, or infrastructure.

## First Principle

Optimize for the database you actually have, the workload you actually run, and the correctness guarantees you actually need.

Do not assume every database optimizes in the same way. Relational, document, search, analytical, graph, time-series, key-value, and vector systems expose different query planners, bottlenecks, and safe optimization paths.

## First Response To A Slow Query Complaint

Start by identifying:

- exact slow query, endpoint, report, search, retrieval, job, or ORM call
- current database or storage system
- database role: source of truth, cache, search index, warehouse, vector index, event store, or derived read model
- current runtime: production, staging, local, batch, dashboard, request path
- baseline latency and expected latency
- whether slowness is constant, intermittent, or a regression
- data volume and result size
- generated query if an ORM/query builder is involved
- whether the bottleneck is database execution, locking, network transfer, application processing, serialization, or rendering

Optimization without a baseline is guesswork.

## Database-Aware Diagnostic Workflow

1. Identify the database type and role.
2. Capture the real query or generated operation.
3. Measure baseline latency, rows/documents/items scanned, rows/documents/items returned, and payload size where possible.
4. Use the database's native diagnostic tool.
5. Identify the dominant cost.
6. Choose the smallest safe optimization path.
7. Re-measure with the same workload.
8. Document the before/after result and tradeoffs.

## Explain Plans And Profiling

An explain plan describes how a database intends to execute a query. In many systems it shows access paths, index use, join strategies, estimated rows, sort/aggregation steps, and estimated cost.

Use explain/profiling tools when:

- a query is unexpectedly slow
- an index exists but does not help
- data growth changed performance
- joins, filters, sorts, aggregations, or search rankings are expensive
- deciding whether to add an index, rewrite the query, change schema, cache, or move the workload

Database-specific examples:

- PostgreSQL/MySQL/SQLite: `EXPLAIN`, `EXPLAIN ANALYZE`
- MongoDB: `explain()`, query profiler, slow query logs
- Elasticsearch/OpenSearch: `_explain`, `_profile`, slow logs
- BigQuery/Snowflake/Redshift/ClickHouse: query profile, execution graph, bytes scanned, partitions read
- DynamoDB: consumed capacity, throttling metrics, access pattern analysis
- Redis: `SLOWLOG`, latency monitor, keyspace analysis
- Neo4j: `EXPLAIN`, `PROFILE`
- InfluxDB/TimescaleDB/Prometheus-like systems: query analyzer, series cardinality, time-range scan size
- Vector databases: query latency, candidate count, index type, recall/precision evals, filter selectivity, embedding/index freshness

Do not treat explain output as the whole truth. It explains database work, not necessarily application latency, network transfer, connection pooling, lock waits, or UI rendering.

## Big-O Thinking For Queries

Use Big-O reasoning to understand how the query scales as data grows.

Common patterns:

- `O(1)`: direct key lookup
- `O(log n)`: indexed lookup, often B-tree-like
- `O(k)`: work proportional to matching result size
- `O(n)`: full table, collection, partition, index, or corpus scan
- `O(n log n)`: large sort, grouping, ranking, or aggregation
- `O(n * m)`: nested loops, cross products, N+1 queries, unbounded graph traversal
- `O(number of network round trips)`: many small queries or remote calls

Use this reasoning differently by database type:

- Relational: joins, indexes, sort/group cost, row estimates, lock contention
- Document: collection scans, unbounded arrays, aggregation pipelines, document size, shard keys
- Key-value: access pattern mismatch, hot keys, over-fetching, missing composite key design
- Search: index size, analyzer mismatch, scoring cost, faceting, high-cardinality filters
- Analytical: bytes scanned, partitions pruned, clustering, shuffle, spill, aggregation scale
- Graph: traversal depth, fanout, path explosion, missing labels/indexes
- Time-series: time range, series cardinality, downsampling, retention, tag selectivity
- Vector: candidate set size, ANN index parameters, metadata filter selectivity, recall/latency tradeoff

## Optimization Paths By Database Type

### Relational Databases

Examples: PostgreSQL, MySQL, SQL Server, SQLite.

Common bottlenecks:

- sequential scans over large tables
- missing or unused indexes
- bad join order or join strategy
- stale statistics
- low-selectivity predicates
- expensive sort/group
- N+1 ORM queries
- lock contention

Optimization paths:

- add or adjust indexes
- use compound, covering, partial, or expression indexes
- rewrite predicates to use indexes
- reduce selected columns and rows
- fix join predicates
- use pagination or keyset pagination
- update statistics or maintenance tasks
- denormalize or add materialized views for stable read-heavy access patterns
- move analytical workloads to a warehouse or read model

Tradeoffs:

- indexes speed reads but slow writes and consume storage
- denormalization improves reads but adds consistency burden
- materialized views improve repeated reads but need refresh strategy

### Document Databases

Examples: MongoDB, Firestore, CouchDB.

Common bottlenecks:

- collection scans
- missing compound indexes
- poor shard/partition key
- large documents
- unbounded nested arrays
- aggregation pipeline stages processing too much data
- cross-document relationship queries

Optimization paths:

- add indexes matching filter/sort patterns
- reshape documents around aggregate read patterns
- avoid unbounded arrays in hot documents
- project only needed fields
- move selective `$match` stages earlier
- denormalize carefully for read-heavy paths
- redesign shard/partition keys if distribution is the problem

Tradeoffs:

- denormalization can create consistency work
- flexible schema can hide data quality problems
- cross-document workflows may need relational modeling or explicit transactions

### Key-Value And Wide-Column Stores

Examples: Redis, DynamoDB, Cassandra, ScyllaDB, Bigtable.

Common bottlenecks:

- querying by non-key attributes
- hot partitions or hot keys
- scan-heavy access
- high fanout reads
- oversized items
- inefficient secondary index use

Optimization paths:

- redesign primary keys around access patterns
- add secondary indexes only when access patterns justify them
- introduce composite keys
- bucket high-volume keys
- precompute read models
- batch gets where supported
- cache stable reference data
- split hot/cold data

Tradeoffs:

- access-pattern-first design is powerful but less flexible
- secondary indexes may add cost, lag, or write amplification
- denormalized read models require update discipline

### Search Engines

Examples: Elasticsearch, OpenSearch, Solr, Meilisearch.

Common bottlenecks:

- expensive scoring
- high-cardinality faceting
- leading wildcard queries
- poor analyzer choice
- too many shards or bad shard sizing
- deep pagination
- large aggregations
- filters not using cached bitsets effectively

Optimization paths:

- tune mappings and analyzers
- use filters instead of scored queries when relevance is not needed
- avoid deep offset pagination; use search-after/cursors
- reduce returned fields
- precompute facets or aggregates
- tune shard count and refresh behavior
- separate search index from source-of-truth database

Tradeoffs:

- search indexes are usually derived, not canonical
- faster indexing/querying can reduce freshness or relevance quality
- analyzer changes may require reindexing

### Analytical Databases And Warehouses

Examples: BigQuery, Snowflake, Redshift, ClickHouse, DuckDB, Databricks.

Common bottlenecks:

- too many bytes scanned
- missing partition pruning
- poor clustering/sort keys
- large shuffles
- high-cardinality joins or groups
- repeated expensive transformations
- dashboard queries over raw detail tables

Optimization paths:

- partition by time or tenant
- cluster/sort by common filters
- pre-aggregate
- materialize intermediate models
- select fewer columns
- filter earlier
- use incremental models
- move repeated dashboard logic into curated tables

Tradeoffs:

- pre-aggregation speeds reads but reduces flexibility
- partitioning helps only if queries filter on partition keys
- materialization improves speed but adds freshness and pipeline complexity

### Graph Databases

Examples: Neo4j, Neptune, JanusGraph.

Common bottlenecks:

- traversal fanout explosion
- unbounded path queries
- missing labels or indexes on starting nodes
- broad relationship scans
- variable-length paths without limits

Optimization paths:

- start from selective indexed nodes
- bound traversal depth
- add labels/indexes for entry points
- constrain relationship types
- precompute common graph projections
- cache expensive graph results when data changes slowly

Tradeoffs:

- graph queries are expressive but can explode combinatorially
- precomputed relationships improve speed but add maintenance burden

### Time-Series Databases

Examples: InfluxDB, TimescaleDB, Prometheus, ClickHouse time-series patterns.

Common bottlenecks:

- overly broad time ranges
- high-cardinality tags
- missing downsampling
- too many series touched
- raw-data dashboards
- retention and compression issues

Optimization paths:

- narrow time windows
- downsample or roll up
- choose tags carefully
- partition/chunk by time
- precompute dashboard aggregates
- apply retention policies
- separate hot recent data from cold historical data

Tradeoffs:

- downsampling loses detail
- high-cardinality tags improve filtering but can harm storage/query performance
- retention saves cost but affects historical analysis

### Vector Databases And Vector Indexes

Examples: pgvector, Pinecone, Weaviate, Milvus, Qdrant, Chroma, FAISS, Elasticsearch/OpenSearch vector search.

Common bottlenecks:

- too many candidate vectors
- expensive metadata filtering
- poor index configuration
- high-dimensional embeddings
- exact search where approximate search is acceptable
- stale or mismatched embeddings
- poor chunking strategy
- retrieval quality issues mistaken for latency issues

Optimization paths:

- tune ANN index type and parameters
- reduce candidate count
- use metadata filters carefully
- improve chunking
- reduce embedding dimensionality if acceptable
- separate canonical content from vector index
- batch embedding/index updates
- evaluate recall/precision alongside latency

Tradeoffs:

- faster approximate search can reduce recall
- stronger filters can reduce candidate quality or increase latency
- vector indexes are usually derived retrieval structures, not systems of record
- embedding model changes may require reindexing

## Cross-Cutting Optimization Levers

### Indexing

Use indexes for common, selective filters, joins, ordering, search, similarity, or uniqueness.

Always consider:

- read improvement
- write penalty
- storage cost
- maintenance cost
- freshness or rebuild requirements
- whether the index matches the actual query shape

### Query Rewrite

Use when the query asks the database to do unnecessary work.

Examples:

- filter earlier
- avoid functions on indexed fields
- select fewer fields
- remove unnecessary joins
- batch N+1 lookups
- avoid deep pagination
- bound graph traversals
- pre-aggregate analytics

### Data Model Change

Use when the current model fights an important, stable access pattern.

Examples:

- denormalized read model
- materialized view
- summary table
- search index
- vector index
- partitioning
- sharding
- hot/cold split

### Caching

Use when reads repeat, freshness requirements allow it, and invalidation is manageable.

Define:

- cache key
- TTL
- invalidation trigger
- permission boundary
- stale data behavior
- stampede protection

### Workload Relocation

Some queries belong somewhere else.

Move to:

- background job
- analytics warehouse
- search index
- materialized read model
- read replica
- vector retrieval index
- precomputed dashboard table

## Output Standard

Start with:

- current database and its role
- observed symptom
- baseline measurement
- likely dominant cost
- recommended next diagnostic or fix

When comparing options, include:

| Option | Helps With | Tradeoff | When To Choose |
|---|---|---|---|

When explain/profile output is available, summarize:

- access method
- indexes or partitions used
- rows/documents/items scanned vs returned
- join/traversal/aggregation/search strategy
- highest-cost step
- suspicious estimate mismatch
- whether the result points to query, index, schema, cache, or workload-placement changes

## Guardrails

- Do not add indexes blindly.
- Do not assume relational optimization strategies apply unchanged to document, search, vector, graph, or analytical systems.
- Do not optimize without knowing the current database and its role.
- Do not treat cache, search, warehouse, or vector index as canonical unless explicitly designed that way.
- Do not use expensive production profiling without understanding execution risk.
- Do not trust ORM or query-builder code without inspecting generated operations.
- Do not assume database time is the whole endpoint latency.
- Do not denormalize or replatform before confirming the access pattern is important and stable.
- Prefer measured, incremental changes over clever rewrites.
