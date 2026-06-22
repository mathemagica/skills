---
name: database-selection
description: Choose an appropriate database for a system or data workload by comparing relational, document-oriented, key-value, wide-column, graph, time-series, search, analytical, object storage, and vector databases; explain tradeoffs, fit, risks, and migration paths.
when_to_use: Use when designing a new system, choosing persistence for a feature, evaluating relational vs document databases, deciding whether a vector database is needed, or explaining database tradeoffs for application, analytics, search, or AI/RAG workloads.
argument-hint: "[system-or-workload]"
---

# Database Selection

Use this skill when deciding what kind of database or persistence layer a system should use and why.

## When To Use

- A new system, feature, service, pipeline, or product workflow needs storage.
- A team is choosing between relational and document-oriented storage.
- A design involves structured records, semi-structured documents, embeddings, search, analytics, or event data.
- A user asks whether they need Postgres, MySQL, MongoDB, DynamoDB, Redis, Elasticsearch/OpenSearch, BigQuery, Snowflake, ClickHouse, Neo4j, InfluxDB, object storage, or a vector database.
- A system needs to support joins, transactions, flexible schemas, full-text search, semantic search, reporting, or high-throughput ingestion.
- A current database feels painful and the team needs to understand whether the problem is database fit, schema design, indexing, access patterns, or operational maturity.

## Goal

Recommend the simplest database architecture that satisfies the workload's correctness, query, scale, latency, durability, and operational requirements.

## First Principle

Choose the database from the access patterns and correctness needs, not from hype or familiarity alone.

Start with:

- What data is stored?
- Who writes it?
- Who reads it?
- What queries must be fast?
- What consistency is required?
- What relationships matter?
- What must be transactional?
- What must be searchable?
- What must be analyzed?
- What must be retained or archived?
- What operational burden is acceptable?

## Core Database Types

### Relational Databases

Use relational databases such as PostgreSQL, MySQL, SQL Server, or SQLite when data has stable entities, relationships, constraints, joins, and transactional requirements.

Good fit for:

- business records
- users, accounts, orders, invoices, permissions
- many-to-one and many-to-many relationships
- data integrity constraints
- transactional workflows
- reporting with SQL
- systems where correctness matters more than schema flexibility

Strengths:

- ACID transactions
- joins
- constraints
- mature indexing
- strong query language
- well-understood operations
- durable source of truth

Tradeoffs:

- schema migrations require discipline
- horizontal scaling can require careful design
- deeply nested or highly variable documents may feel awkward
- complex analytical workloads may need a warehouse or columnar store

### Document-Oriented Databases

Use document databases such as MongoDB, CouchDB, or Firestore when records are naturally document-shaped, frequently read as whole aggregates, and schema variation is useful.

Good fit for:

- content documents
- product catalogs with variable attributes
- user profiles or settings
- event payloads
- JSON-native application data
- workloads where aggregate reads dominate

Strengths:

- flexible schema
- natural JSON document model
- easy storage of nested structures
- often simple horizontal scaling
- fewer joins when documents are self-contained

Tradeoffs:

- cross-document relationships can become awkward
- duplication can create consistency problems
- transactions and joins may be weaker, newer, or less ergonomic than relational systems
- reporting across many document shapes can become hard
- schema flexibility can become schema ambiguity

### Key-Value Stores

Use key-value stores such as Redis, DynamoDB, or FoundationDB-style APIs when lookup by key dominates.

Good fit for:

- caching
- sessions
- feature flags
- counters
- simple high-scale lookup
- queues or ephemeral state, depending on the product

### Wide-Column Databases

Use wide-column stores such as Cassandra, ScyllaDB, or Bigtable when writes are huge, access patterns are known, and distributed scale matters more than ad hoc querying.

Good fit for:

- high-volume event ingestion
- time-bucketed records
- globally distributed write-heavy workloads

### Graph Databases

Use graph databases such as Neo4j, Neptune, or JanusGraph when relationships themselves are the primary object of query.

Good fit for:

- recommendations
- fraud rings
- dependency networks
- knowledge graphs
- path traversal queries

### Time-Series Databases

Use time-series databases such as InfluxDB, TimescaleDB, Prometheus, or ClickHouse-style patterns when data is mostly measurements over time.

Good fit for:

- metrics
- sensor readings
- observability
- telemetry
- time-window aggregation

### Search Engines

Use search engines such as Elasticsearch, OpenSearch, Solr, or Meilisearch when lexical search, ranking, faceting, highlighting, or search-specific indexing is central.

Good fit for:

- full-text search
- filtering and faceting
- relevance ranking
- log search

### Analytical Databases and Warehouses

Use warehouses or analytical stores such as BigQuery, Snowflake, Redshift, DuckDB, ClickHouse, or Databricks when the workload is large-scale analysis rather than operational transactions.

Good fit for:

- BI dashboards
- historical analysis
- batch reporting
- aggregations over large datasets
- ELT/ETL outputs

### Object Storage

Use object storage such as S3, GCS, Azure Blob, or local files when storing large immutable blobs.

Good fit for:

- media
- documents
- backups
- data lake files
- model artifacts
- exports

Object storage is often paired with metadata in a relational database.

### Vector Databases

Use vector databases or vector indexes such as pgvector, Pinecone, Weaviate, Milvus, Qdrant, Chroma, Elasticsearch/OpenSearch vector search, or FAISS when the system needs similarity search over embeddings.

Good fit for:

- semantic search
- retrieval-augmented generation
- recommendation by embedding similarity
- duplicate or near-duplicate detection
- clustering or nearest-neighbor lookup

Strengths:

- approximate nearest-neighbor search
- ranking by vector similarity
- embedding-based retrieval
- metadata filtering in mature systems

Tradeoffs:

- vectors do not replace source-of-truth records
- embeddings can drift when models change
- evaluation requires relevance tests
- metadata filters and permissions need careful design
- exact relational queries still belong elsewhere
- vector databases are often secondary indexes, not primary databases

## Relational vs Document-Oriented

Choose relational when:

- relationships are central
- integrity constraints matter
- transactions span multiple entities
- ad hoc querying and reporting matter
- schemas are stable enough to model explicitly

Choose document-oriented when:

- each record is usually read/written as one aggregate
- nested data mirrors application objects
- schema variation is real and valuable
- cross-document joins are rare
- duplication is acceptable or carefully managed

A common compromise:

- relational database as source of truth
- JSON/JSONB columns for limited flexible attributes
- search/vector/document stores as secondary indexes when access patterns require them

## Relational vs Vector Databases

Relational databases and vector databases solve different problems.

Relational databases answer:

- Which records match exact conditions?
- How are entities related?
- Can this transaction preserve constraints?
- What aggregate does SQL compute from structured data?

Vector databases answer:

- Which items are semantically similar to this query or item?
- What content is nearby in embedding space?
- Which chunks should be retrieved for a language model?

Important distinction:

- A relational database is usually a system of record.
- A vector database is usually a retrieval index over derived embeddings.
- Vector search complements relational storage; it rarely replaces it.

Use relational storage for:

- users
- permissions
- document metadata
- canonical content
- transactions
- audit records

Use vector storage for:

- embeddings of documents, chunks, or items
- similarity lookup
- RAG retrieval
- semantic recommendations

## Workflow

1. Define the workload:
   - operational app
   - analytics/reporting
   - search
   - cache/session
   - event ingestion
   - graph traversal
   - time-series
   - AI/RAG retrieval
   - archival/blob storage
2. Identify data shape:
   - tabular entities
   - nested documents
   - key-value pairs
   - event streams
   - graph edges
   - time-stamped measurements
   - blobs
   - vectors/embeddings
3. Identify access patterns:
   - primary reads
   - primary writes
   - joins
   - filters
   - aggregations
   - full-text search
   - semantic search
   - batch scans
   - retention/deletion
4. Identify correctness requirements:
   - ACID transactions
   - uniqueness
   - foreign keys
   - referential integrity
   - consistency model
   - auditability
   - authorization boundaries
5. Identify scale and latency requirements:
   - expected data volume
   - read/write rate
   - latency target
   - geographic distribution
   - offline or sync behavior
6. Consider operational constraints:
   - team familiarity
   - managed service availability
   - backup/restore
   - migrations
   - observability
   - cost
   - compliance
7. Recommend:
   - primary database
   - secondary indexes or stores if needed
   - what each store owns
   - why simpler options were rejected
   - risks and migration path

## Output Standard

- Start with a direct recommendation.
- Explain the workload fit in plain language.
- Separate source-of-truth storage from secondary indexes.
- Include a tradeoff table when comparing two or more options.
- Call out operational risks.
- Prefer boring, mature databases unless the workload clearly needs specialization.

## Guardrails

- Do not recommend a vector database just because AI is involved.
- Do not recommend a document database only because the API uses JSON.
- Do not recommend microservice-style polyglot persistence for a small system without a clear access-pattern need.
- Do not ignore migrations, backups, observability, or team familiarity.
- Do not treat cache, search index, warehouse, or vector index as the only source of truth unless the system is explicitly designed that way.
- Do not optimize for theoretical scale before understanding correctness and query needs.
