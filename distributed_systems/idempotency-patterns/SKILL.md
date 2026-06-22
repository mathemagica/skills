---
name: idempotency-patterns
description: Design, review, or debug idempotent behavior in distributed systems, including web apps, APIs, data pipelines, backend jobs, queues, retries, webhooks, payments, imports, exports, and third-party integrations.
when_to_use: Use when a system operation may be retried, duplicated, replayed, timed out, partially completed, delivered more than once, or called by unreliable clients, queues, workers, schedulers, webhooks, or third-party APIs.
argument-hint: "[operation-or-workflow]"
---

# Idempotency Patterns

Use this skill when designing or debugging a system operation that might run more than once.

## Core Idea

An operation is idempotent when applying it multiple times has the same intended effect as applying it once.

Example:

```text
Set order status to "cancelled"   -> idempotent
Increment account balance by $10  -> not idempotent unless guarded
Create invoice with random ID     -> not idempotent unless keyed
Create invoice for order #123     -> can be idempotent with uniqueness
```

Distributed systems need idempotency because retries, duplicate delivery, timeouts, network failures, and partial success are normal.

## Why Idempotency Matters

Without idempotency, retries can cause:

- duplicate payments
- duplicate emails
- duplicate imported records
- duplicate jobs
- double-counted metrics
- repeated side effects
- corrupted state
- inconsistent downstream systems
- support incidents that are hard to unwind

Idempotency lets systems safely retry after uncertainty.

The key uncertainty is:

```text
Did the operation fail before doing the work, after doing the work, or after doing the work but before the caller saw the response?
```

Idempotency makes that ambiguity survivable.

## Where This Pattern Shows Up

### Web Apps And APIs

Common uses:

- form submission
- checkout/payment
- account creation
- file upload
- password reset
- order cancellation
- booking/reservation
- API `POST` requests
- retrying failed requests from clients

Patterns:

- idempotency keys
- unique constraints
- client-generated request IDs
- upsert by natural key
- safe retries for `PUT`/`PATCH`
- deduplicated command records
- redirect-after-post for browser forms

### Backend Jobs And Queues

Queues commonly provide at-least-once delivery, meaning a job may run more than once.

Common causes:

- worker crash after processing but before ack
- visibility timeout expires
- retry policy re-enqueues job
- dead-letter replay
- scheduler runs overlapping jobs

Patterns:

- job idempotency key
- processed-message table
- unique output constraints
- checkpointing
- state-machine transitions
- compare-and-set updates
- idempotent external calls
- safe retry and backoff

### Data Pipelines

Pipelines often rerun batches, replay events, or process late-arriving data.

Common uses:

- ingestion
- ETL/ELT
- stream processing
- backfills
- deduplication
- snapshot imports
- incremental syncs
- materialized view rebuilds

Patterns:

- deterministic record keys
- merge/upsert instead of blind append
- partition replacement
- watermark/checkpoint tracking
- exactly-once-like semantics built from idempotent writes
- replay-safe transforms
- immutable raw data plus derived rebuilds

### Third-Party Integrations

Third-party APIs and webhooks often retry deliveries or return uncertain errors.

Common uses:

- payment processors
- email providers
- CRM syncs
- calendar integrations
- shipping/fulfillment
- OAuth callbacks
- webhooks

Patterns:

- provider idempotency keys
- webhook event ID deduplication
- natural-key upserts
- external ID mapping tables
- sync cursors
- retry-safe outbound calls
- reconciliation jobs

## Workflow

1. Identify the operation.
   - What is the requested business action?
   - What state changes?
   - What side effects occur?
2. Identify duplicate sources.
   - client retry
   - server timeout
   - load balancer retry
   - queue redelivery
   - worker crash
   - scheduler overlap
   - webhook replay
   - manual replay/backfill
   - third-party retry
3. Identify the idempotency scope.
   - per user
   - per tenant
   - per resource
   - per external event
   - per batch partition
   - per workflow step
4. Choose the idempotency key.
   - client-provided key
   - provider event ID
   - natural business key
   - generated command ID
   - deterministic batch/partition key
5. Decide where to enforce it.
   - database unique constraint
   - idempotency-key table
   - processed-events table
   - job state table
   - external ID mapping table
   - object storage path
   - cache with durable fallback
6. Define replay behavior.
   - return original success response
   - no-op if already complete
   - resume from checkpoint
   - reject conflicting duplicate
   - update existing record
   - reconcile downstream state
7. Make side effects safe.
   - send email once
   - charge payment once
   - create external object once
   - publish event once or make consumers idempotent
8. Test duplicates and partial failures.

## Idempotency Key Design

A good idempotency key is:

- stable across retries of the same operation
- different for distinct operations
- scoped to avoid cross-user or cross-tenant collisions
- stored durably enough to survive retry windows
- tied to request parameters so conflicting reuse can be detected

Examples:

```text
tenant_id + idempotency_key
provider + webhook_event_id
source_system + external_object_id
pipeline_name + partition_date + source_file_hash
order_id + "cancel"
user_id + form_submission_uuid
```

Avoid:

- random server-generated IDs after the retry boundary
- timestamps alone
- keys without tenant/user scope
- cache-only dedupe for operations that must survive process restart
- treating every repeated request as safe without checking payload consistency

## Common Implementation Patterns

### Unique Constraint

Use when the operation creates a resource with a natural unique identity.

Example:

```text
UNIQUE(tenant_id, external_invoice_id)
```

Good for:

- imports
- syncs
- external objects
- create-if-not-exists workflows

### Idempotency Key Table

Use when clients submit commands that may be retried.

Stores:

- key
- request hash
- status: started/succeeded/failed
- response or resource reference
- expiration
- created_by/tenant

Good for:

- payments
- checkout
- API POSTs
- expensive workflows

### Processed Event Table

Use for webhook/event consumers.

Stores:

- provider/source
- event ID
- received timestamp
- processing status
- error/retry info

Good for:

- webhooks
- event streams
- queue consumers

### State Machine Transitions

Use when an entity has lifecycle states.

Example:

- only transition `pending -> processed`
- ignore duplicate `processed -> processed`
- reject invalid `cancelled -> shipped`

Good for:

- orders
- jobs
- approvals
- document processing

### Checkpointing

Use when processing a batch or stream.

Stores:

- last processed offset
- watermark
- partition
- source file hash
- batch run ID

Good for:

- pipelines
- stream processors
- backfills
- incremental syncs

## Idempotency vs Exactly Once

Exactly-once delivery is rare in real distributed systems.

Most reliable systems use:

```text
at-least-once delivery + idempotent processing
```

This means the system may deliver or execute work more than once, but repeated processing does not corrupt state.

Do not rely on "this queue only sends once" unless the provider explicitly guarantees it and the surrounding code still handles uncertainty.

## Testing Idempotency

Test:

- same request sent twice
- same request sent concurrently
- retry after timeout
- worker crash after side effect but before ack
- webhook replay
- duplicate batch file
- partial failure after database write but before external call
- partial failure after external call but before local write
- idempotency key reused with different payload
- expired idempotency key behavior

## Output Standard

Start with:

- operation being protected
- duplicate/retry sources
- idempotency key
- enforcement point
- replay behavior
- side effects that must be guarded

Then include:

- failure scenarios
- recommended storage/constraint
- tradeoffs
- tests to prove duplicate safety

## Guardrails

- Do not assume retries are rare.
- Do not use in-memory-only dedupe for durable side effects.
- Do not rely on queue delivery being exactly once.
- Do not create side effects before recording enough state to dedupe or reconcile.
- Do not let the same idempotency key mean different payloads.
- Do not ignore tenant/user scoping.
- Do not claim an operation is idempotent just because it usually succeeds.
- Prefer durable constraints over best-effort duplicate checks for critical workflows.
