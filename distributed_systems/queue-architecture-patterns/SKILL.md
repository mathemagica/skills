---
name: queue-architecture-patterns
description: Design, evaluate, or debug queue-based architecture in distributed systems, including what queues are, where they fit, asynchronous processing, burst smoothing, write buffering, workers, retries, dead-letter queues, idempotency, ordering, backpressure, and integration with databases, APIs, web apps, pipelines, and third-party services.
---

# Queue Architecture Patterns

Use this skill when a system may benefit from asynchronous processing, buffering, retryable work, or decoupling producers from consumers.

## Core Idea

A queue is a durable or semi-durable place to put work so another component can process it later.

Basic shape:

```text
Producer -> Queue -> Consumer / Worker
```

Examples:

- web server enqueues a job
- worker processes the job
- database records the result
- user sees status later

Queues help systems absorb bursts, isolate slow work, retry failures, and decouple components.

## Where Queues Fit In Distributed Systems

Queues often sit between:

```text
Web/API Server -> Queue -> Worker -> Database
Web/API Server -> Queue -> Worker -> Third-Party API
Ingestion Service -> Queue -> Pipeline Stage -> Storage
Scheduler -> Queue -> Worker
Webhook Receiver -> Queue -> Processor
Database Change/Event -> Queue -> Consumer
```

They are useful when the producer should not wait for all downstream work to finish synchronously.

## What Queues Are Useful For

Queues are useful for:

- background jobs
- email sending
- media processing
- imports and exports
- webhook processing
- retries
- rate-limited third-party APIs
- smoothing bursty traffic
- async side effects after a request
- pipeline stages
- event-driven integrations
- fanout to multiple consumers
- workload isolation
- temporary buffering during dependency slowness

They are not magic scaling dust. Queues move work in time; they do not eliminate work.

## Smoothing Bursty Write Performance

Queues help when incoming writes arrive faster than downstream systems can safely process.

Without a queue:

```text
Burst of requests -> App -> Database/External API overload
```

With a queue:

```text
Burst of requests -> App quickly enqueues -> Workers drain queue at controlled rate
```

This can protect:

- databases
- search indexes
- external APIs
- file processors
- email/SMS providers
- ML inference services
- pipeline stages

Design choices:

- bound worker concurrency
- control dequeue rate
- batch writes
- retry with backoff
- monitor queue depth and age
- shed or reject load when queue grows beyond safe limits

Important tradeoff:

- queueing improves throughput stability but introduces latency and eventual consistency.

## When To Consider Adding A Queue

Consider a queue when:

- request path work is slow but does not need to finish before responding
- writes arrive in bursts
- downstream systems have rate limits
- external APIs fail intermittently
- work needs retries
- work can be processed asynchronously
- processing is CPU-heavy or I/O-heavy
- users can tolerate pending/processing status
- batch processing would be more efficient
- multiple consumers need to react to an event
- producer and consumer should deploy/scale independently

Do not add a queue when:

- the user needs an immediate authoritative result
- the operation is small, fast, and reliable
- ordering must be strict but the queue system cannot guarantee the needed order
- duplicate processing would be unsafe and idempotency is not designed
- the team cannot monitor and operate queue backlog
- the real bottleneck is a bad query, missing index, or inefficient code path

## Queue Concepts

### Producer

The component that sends messages.

Examples:

- API server
- scheduler
- webhook receiver
- pipeline stage
- database change stream

Producer responsibilities:

- create valid message
- include idempotency/correlation IDs
- decide whether enqueue success means user-visible success
- handle enqueue failure
- avoid putting secrets in messages

### Message

The unit of work.

Good messages include:

- message type
- stable IDs
- tenant/user context when needed
- idempotency key
- correlation/request ID
- minimal payload or pointer to durable data
- creation timestamp
- version/schema

Avoid:

- huge payloads
- secrets
- data that can go stale without being checked
- implicit dependencies on producer memory

### Queue / Broker

The infrastructure that stores and delivers messages.

Examples:

- AWS SQS
- RabbitMQ
- Kafka
- Google Pub/Sub
- Azure Service Bus
- Redis queues
- Celery broker
- Sidekiq/Resque
- database-backed job tables

Queue responsibilities:

- buffer messages
- deliver to consumers
- support retries/visibility/acks depending on system
- expose backlog metrics
- sometimes preserve ordering or partitions

### Consumer / Worker

The component that processes messages.

Worker responsibilities:

- validate message
- fetch current durable state if needed
- perform work
- write results
- ack/delete message only after safe completion
- handle retries
- be idempotent
- emit logs/metrics

## Delivery Semantics

Common delivery models:

- at-most-once: may lose messages, does not redeliver
- at-least-once: may redeliver, requires idempotent consumers
- exactly-once: rare and usually limited; still design for uncertainty

Most practical systems use:

```text
at-least-once delivery + idempotent processing
```

## Retries And Dead-Letter Queues

Retries are useful for transient failures.

Use:

- retry limits
- exponential backoff
- jitter
- visibility timeouts or ack deadlines
- dead-letter queue after repeated failure

Dead-letter queues are for messages that need inspection or special handling.

Track:

- failure reason
- original message
- receive count
- first/last failure time
- worker version
- correlation ID

Do not let DLQs become silent graveyards. They need alarms and triage.

## Ordering

Queues may or may not preserve order.

Ask:

- Is order required globally?
- Is order required per tenant/resource/key?
- Can work be partitioned by key?
- What happens if messages arrive out of order?
- Can stale messages be ignored by checking current state?

Often, strict ordering is less important than designing state transitions that tolerate out-of-order delivery.

## Backpressure

A queue gives you a place to observe and control pressure.

Signals:

- queue depth
- oldest message age
- processing rate
- failure rate
- retry rate
- worker concurrency
- downstream latency

Responses:

- scale workers
- reduce producer rate
- batch work
- shed load
- pause non-critical producers
- route to lower-priority queue
- increase downstream capacity
- alert humans

## Integration With Other Components

### Web/API Server

Patterns:

- enqueue job and return `202 Accepted`
- return resource with `status: pending`
- poll status endpoint
- push status via websocket/SSE/notification
- use idempotency key for job creation

### Database

Patterns:

- transactional outbox
- job table
- write source-of-truth record before enqueue
- worker reads current state before processing
- unique constraints for dedupe
- store processing status

Pitfall:

- writing database state and enqueueing message separately can create inconsistency if one succeeds and the other fails.

### External APIs

Patterns:

- queue calls to respect rate limits
- retry transient failures
- use provider idempotency keys
- reconcile uncertain outcomes
- isolate provider outages from request path

### Search Indexes / Read Models

Patterns:

- enqueue reindex/update jobs after source-of-truth writes
- tolerate eventual consistency
- rebuild from source of truth when needed
- dedupe by resource/version

### Data Pipelines

Patterns:

- queue between ingestion and processing stages
- checkpoint by partition or offset
- batch messages for efficiency
- use DLQs for malformed records
- make transforms replay-safe

## Common Queue Patterns

### Background Job

```text
Request -> enqueue job -> return response
Worker -> process job -> update status
```

### Work Queue

Multiple workers process independent tasks from one queue.

Good for:

- image processing
- emails
- imports
- exports

### Pub/Sub Fanout

One event goes to multiple subscribers.

Good for:

- audit event
- notification
- search indexing
- analytics ingestion

### Transactional Outbox

Write business state and an outbox event in the same database transaction. A relay publishes outbox events to a queue.

Good for:

- avoiding lost events
- reliable integration after database writes

### Priority Queues

Separate urgent work from background work.

Good for:

- user-facing jobs before bulk maintenance
- paid tier priority
- operational emergency tasks

## Workflow

1. Identify the workflow.
   - What work is being deferred or buffered?
   - Who produces it?
   - Who consumes it?
2. Decide whether async behavior is acceptable.
   - What does the user see immediately?
   - What state indicates pending/processing/failed?
3. Identify the bottleneck or risk.
   - slow work
   - bursty writes
   - external rate limit
   - transient dependency failures
   - deployment decoupling
4. Define the message contract.
   - type
   - IDs
   - schema version
   - tenant/user context
   - idempotency key
   - correlation ID
   - minimal payload vs durable pointer
5. Define processing semantics.
   - retries
   - timeout
   - ack/delete point
   - idempotency
   - ordering requirements
   - failure status
6. Define integration points.
   - database transaction/outbox
   - status table
   - external API idempotency
   - downstream events
7. Define observability.
   - queue depth
   - oldest message age
   - processing rate
   - failure rate
   - DLQ count
   - worker saturation
8. Define operations.
   - replay
   - purge
   - DLQ triage
   - scaling workers
   - pausing producers
   - backfill behavior

## Output Standard

Start with:

- whether a queue is recommended
- producer
- queue/broker
- consumer/worker
- message contract
- user-visible behavior
- retry/DLQ behavior
- idempotency strategy
- observability requirements
- tradeoffs

When evaluating whether to add a queue, include:

| Benefit | Cost/Risk | Mitigation |
|---|---|---|

## Guardrails

- Do not add a queue just to hide slow code without understanding the bottleneck.
- Do not enqueue work that must complete synchronously for correctness.
- Do not assume exactly-once delivery.
- Do not process messages without idempotency for critical side effects.
- Do not put secrets or huge payloads in messages.
- Do not create queues without alarms on backlog and dead-letter messages.
- Do not let async workflows lack user-visible status when users need feedback.
- Do not split database write and message publish without considering outbox or reconciliation.
