---
name: sync-async-processing
description: Design, evaluate, or debug synchronous vs asynchronous processing in web apps and distributed systems, including what sync/async mean, when work belongs in the web request path versus background workers, task schedulers, queues, cron jobs, event handlers, webhooks, and simple starting advice for new web apps.
---

# Sync Async Processing

Use this skill when deciding where work should run: directly in the request path or asynchronously in a worker, scheduler, queue, or background process.

## Core Idea

Synchronous processing means the caller waits for the work to complete before receiving a result.

```text
Browser -> Web Server -> Do work now -> Response
```

Asynchronous processing means the caller does not wait for all work to complete. The system records or enqueues work, responds, and another process finishes the work later.

```text
Browser -> Web Server -> Record/enqueue work -> Response
                         Queue -> Worker -> Finish work
```

The design question is:

```text
What must be true before we can safely respond to the user?
```

## Simple Starting Advice For New Web Apps

For a new standard web app, start simple:

1. Keep user-critical validation and small database writes synchronous.
2. Move slow, retryable, or non-user-blocking side effects asynchronous.
3. Use the database as source of truth for status.
4. Add a background job system only when there is real work that should outlive the request.
5. Add a scheduler only when work must run at a time or interval.
6. Add queues when you need retries, burst smoothing, or worker scaling.
7. Always make async work observable and idempotent.

Good initial split:

Synchronous:

- validate request
- authenticate/authorize
- write core business record
- return resource/status to user

Asynchronous:

- send email
- resize image
- call slow third-party API
- generate report
- sync CRM
- index search document
- process uploaded media
- run long import/export
- perform non-critical notification

Do not create a complex async architecture before the workflow needs it. A simple web request plus a small background job queue is often enough.

## When To Keep Work Synchronous

Keep work synchronous when:

- the user needs the result immediately
- correctness depends on the result before responding
- the work is fast and reliable
- the operation is part of the core transaction
- failure should prevent success
- the response must include the computed value
- authorization or validation must complete before proceeding
- the write must be visible immediately

Examples:

- login/auth check
- permission check
- form validation
- create order record
- reserve inventory if required before checkout success
- update account settings
- return search results for an interactive query
- submit payment only if the response must confirm charge result

Synchronous work should be bounded. A web request should not wait indefinitely for slow or unreliable dependencies.

## When To Use Asynchronous Processing

Use async processing when:

- work is slow
- work is retryable
- work is not required for the initial response
- work may fail independently
- work is CPU-heavy or I/O-heavy
- work can be represented as pending/processing/complete/failed
- downstream systems are rate-limited
- bursts need smoothing
- the user can be notified later
- worker scaling should be independent from web server scaling

Examples:

- sending email/SMS
- file processing
- media transcoding
- report generation
- data imports/exports
- webhook processing
- search indexing
- cache warming
- batch enrichment
- billing reconciliation
- analytics aggregation
- CRM or third-party sync

## Web Server Process vs Worker Process

### Web Server Process

Best for:

- request parsing
- auth and authorization
- quick validation
- small transactional writes
- fast reads
- response construction

Optimize for:

- low latency
- predictable execution time
- low memory per request
- avoiding long blocking work
- protecting request concurrency

Avoid:

- long-running CPU tasks
- large file processing
- unbounded loops
- waiting on slow third-party APIs when not required
- heavy batch work
- retry loops inside request handlers

### Worker Process

Best for:

- long-running jobs
- retryable side effects
- CPU-heavy work
- I/O-heavy downstream calls
- scheduled tasks
- queue consumers
- pipeline stages

Optimize for:

- retries
- idempotency
- checkpointing
- concurrency control
- observability
- failure handling
- safe replay

Workers can run slower than web requests, but they must be easier to observe and recover.

## Task Schedulers And Timed Work

Use task schedulers when work should happen on a clock or recurring cadence.

Examples:

- nightly cleanup
- daily report generation
- hourly sync
- expired session cleanup
- invoice generation
- reminder emails
- data freshness checks
- retry reconciliation
- periodic cache warming

Scheduler patterns:

- cron
- cloud scheduled jobs
- Celery beat
- Sidekiq cron
- Kubernetes CronJob
- EventBridge Scheduler
- GitHub Actions scheduled workflows
- managed workflow orchestrators

Design questions:

- What happens if a scheduled run overlaps the previous run?
- Is the task idempotent?
- Can missed runs be caught up?
- How are failures alerted?
- Does it need a lock to prevent duplicate execution?
- What data range does each run own?

## Architectural Components

### Background Job Queue

Use when async work is triggered by user or system events.

```text
Request/Event -> Queue -> Worker
```

Good for:

- emails
- uploads
- reports
- retries
- third-party calls

### Scheduler

Use when work starts from time.

```text
Clock -> Scheduled Job -> Work
```

Good for:

- nightly jobs
- periodic syncs
- cleanup
- batch reports

### Event Bus / Pub/Sub

Use when multiple consumers need to react to a domain event.

```text
OrderCreated -> Event Bus -> Email Consumer
                          -> Analytics Consumer
                          -> Fulfillment Consumer
```

Good for:

- decoupled integrations
- fanout
- domain events

Tradeoff:

- more moving parts
- harder tracing
- eventual consistency

### Workflow Orchestrator

Use when a multi-step async process needs state, retries, branching, and visibility.

Good for:

- long-running business workflows
- human approval steps
- multi-system transactions
- complex data pipelines

Examples:

- Temporal
- AWS Step Functions
- Airflow
- Dagster
- Prefect

Do not start here for simple background jobs.

### Webhook Receiver + Async Processor

Use when receiving events from third parties.

```text
Webhook -> Verify + Store -> Queue -> Processor
```

Good default:

- respond quickly to provider
- process later
- dedupe by event ID
- retry safely

## User Experience Patterns

Async work needs a UX.

Common patterns:

- `202 Accepted`
- pending/processing/complete/failed status
- status polling endpoint
- progress bar
- email/notification on completion
- websocket/SSE updates
- downloadable result when ready
- retry or cancel button
- admin repair tools

Avoid:

- returning success when only enqueue succeeded unless the UI explains pending state
- making users wait silently
- hiding failed async work

## Consistency And Correctness

Async processing creates eventual consistency.

Ask:

- What can the user see immediately?
- What may be stale?
- What must be transactional?
- What happens if the worker fails?
- Can the operation run twice?
- What is the source of truth?
- How is status represented?
- How are partial failures repaired?

Use:

- idempotency keys
- status fields
- job records
- outbox pattern
- retries with backoff
- dead-letter queues
- reconciliation jobs
- audit logs

## Workflow

1. Identify the operation.
2. List required steps and side effects.
3. Classify each step:
   - required before response
   - can happen after response
   - must happen on schedule
   - should react to an event
4. Decide sync vs async.
5. Define source-of-truth state.
   - pending
   - processing
   - completed
   - failed
   - cancelled
6. Define user-visible behavior.
7. Define worker/scheduler/queue behavior.
8. Define retries, idempotency, and failure handling.
9. Define observability.
   - job count
   - queue depth
   - oldest job age
   - success/failure rate
   - duration
   - retries
   - DLQ
10. Test success, retry, duplicate, timeout, and failure paths.

## Output Standard

Start with:

- recommended sync/async split
- what must complete before response
- what can move to background work
- user-visible status behavior
- required architectural component, if any
- idempotency/retry plan
- observability plan

When comparing options, include:

| Work Item | Sync or Async | Why | Failure Handling |
|---|---|---|---|

## Guardrails

- Do not move work async if the user needs the result to determine success.
- Do not keep slow non-critical side effects in the request path.
- Do not add queues/schedulers/workflow engines before the workflow needs them.
- Do not enqueue work without durable status when users need to track it.
- Do not process async work without idempotency.
- Do not hide async failures from users or operators.
- Do not let scheduled jobs overlap unless safe.
- Prefer the simplest architecture that makes latency, correctness, and recovery clear.
