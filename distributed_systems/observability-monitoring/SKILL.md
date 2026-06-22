---
name: observability-monitoring
description: Design, review, or debug observability for applications and distributed systems, including monitoring, alerting, logging, metrics, traces, instrumentation, dashboards, SLOs, health checks, incident signals, and practical starting defaults for web apps and backend services.
when_to_use: Use when adding monitoring, designing alarms, instrumenting code, improving logs, choosing metrics/traces, debugging production issues, reviewing operational readiness, creating dashboards, or deciding what signals a web app, API, worker, queue, database, or integration should expose.
argument-hint: "[system-or-service]"
---

# Observability Monitoring

Use this skill when a system needs to be understandable in production.

## Core Idea

Observability is the ability to understand what a system is doing from the outside by looking at the signals it emits.

The main signals are:

- logs: discrete events and context
- metrics: numeric measurements over time
- traces: request or workflow paths across components
- events: notable changes such as deploys, failures, failovers, or migrations

Monitoring watches those signals. Alerting notifies humans when action is needed.

## Simple Starting Point For Web Apps

For a standard web app, start with:

1. Structured application logs.
2. Request metrics.
3. Error tracking.
4. Basic infrastructure metrics.
5. Health checks.
6. Deployment markers.
7. A small set of actionable alerts.

Minimum useful signals:

- request rate
- error rate
- p50/p95/p99 latency
- 4xx and 5xx counts
- CPU and memory
- database latency and connection usage
- background job failures
- queue depth and oldest message age
- external API error/timeout rate
- deploy version and timestamp

Minimum useful alerts:

- elevated 5xx rate
- sustained high latency
- app instances unhealthy
- worker failure or queue backlog
- database unavailable or connection pool exhausted
- disk/storage near full where relevant
- critical scheduled job failed
- error budget burn or SLO breach if SLOs exist

Do not start with dozens of noisy alerts. Start with a few alerts that require human action.

## Logs

Logs are timestamped records of things that happened.

Good logs answer:

- what happened?
- where did it happen?
- for which request/job/user/tenant/resource?
- was it expected or an error?
- what should an operator investigate next?

Best practices:

- use structured logs, usually JSON in production
- include request ID / correlation ID
- include tenant/workspace ID when relevant
- include user ID only when safe and useful
- include resource IDs
- include operation name
- include duration for important operations
- include error type and stack trace for exceptions
- avoid secrets, tokens, passwords, raw cookies, and sensitive PII
- log at appropriate levels: debug, info, warn, error
- make logs searchable by request ID, job ID, tenant ID, and deployment version

Avoid:

- noisy logs on hot paths
- logs without context
- logging entire request/response bodies by default
- swallowing exceptions without logging
- logging secrets or credential-bearing URLs
- using logs as the only metric source when metrics are needed

## Metrics

Metrics are numeric values tracked over time.

Good metrics are:

- named consistently
- tagged with useful dimensions
- bounded in cardinality
- tied to user or system outcomes
- useful for dashboards and alerts

Common metric types:

- counter: monotonically increasing count
- gauge: current value
- histogram/distribution: latency or size distribution

Golden signals for services:

- traffic: request rate
- errors: error rate
- latency: p50/p95/p99
- saturation: CPU, memory, connections, queue depth, thread pools

Useful dimensions:

- service
- environment
- route or operation
- status code class
- dependency
- region
- tenant tier, if low cardinality

Avoid high-cardinality labels:

- raw user ID
- request ID
- email
- full URL with arbitrary query params
- unbounded resource IDs

High-cardinality labels can make monitoring expensive or unusable.

## Tracing

Traces show how one request or workflow moves across components.

Useful for:

- distributed systems
- slow requests
- dependency latency
- queue/worker flows
- microservices
- external API calls
- database spans
- debugging where time is spent

A good trace includes:

- request entry span
- route/operation name
- database calls
- cache calls
- queue publish/consume
- external API calls
- errors
- correlation IDs
- selected business attributes with safe cardinality

Trace propagation matters. Pass trace/request IDs across:

- HTTP calls
- queues
- background jobs
- event buses
- worker boundaries

## Instrumentation

Instrumentation is code or configuration that emits observability signals.

Instrument:

- HTTP request start/end
- route/controller/resolver duration
- database query duration or aggregate DB timing
- cache hit/miss
- queue enqueue/dequeue/process duration
- worker success/failure
- external API calls
- scheduled job start/end/failure
- retries
- rate limit decisions
- auth failures
- critical business events
- deployment/version metadata

Prefer:

- framework auto-instrumentation where reliable
- OpenTelemetry-compatible instrumentation when possible
- small manual instrumentation around business-critical flows
- consistent operation names

Do not instrument everything blindly. Instrument what helps answer operational questions.

## Alerts

An alert should mean a human should act.

Good alerts are:

- actionable
- routed to the right owner
- tied to user impact or imminent system risk
- tuned to avoid flapping
- documented with a runbook or next step
- tested occasionally

Bad alerts:

- "CPU is 80% once"
- every single exception
- expected validation errors
- transient dependency blips below user-impact threshold
- alerts no one owns
- alerts with no severity or action

Alert examples:

- 5xx rate > threshold for 5 minutes
- p95 latency > SLO for 10 minutes
- queue oldest message age > acceptable processing delay
- dead-letter queue has messages
- database connection pool exhausted
- scheduled billing job failed
- certificate expires soon
- error budget burn rate too high

Use warning signals for dashboards or tickets. Use paging alerts for urgent human action.

## SLOs And SLIs

An SLI is a measurement of service behavior.

Examples:

- percentage of successful requests
- p95 request latency
- job completion within 10 minutes
- webhook processing success rate
- search freshness within 5 minutes

An SLO is a target for that measurement.

Examples:

- 99.9% of API requests succeed over 30 days
- 95% of page loads complete under 2 seconds
- 99% of import jobs complete within 15 minutes

Use SLOs when:

- the product has reliability expectations
- the team needs to prioritize reliability work
- alerts should be tied to user impact
- incident severity needs consistency

## Dashboards

Dashboards should support operational questions.

Good dashboards answer:

- Is the system healthy?
- Are users impacted?
- What changed recently?
- Which dependency is failing?
- Is this deploy related?
- Are queues backing up?
- Is the database saturated?
- Are errors localized by route, tenant, region, or version?

Useful dashboard sections:

- traffic/errors/latency
- deploy markers
- infrastructure saturation
- database/cache/queue health
- external dependency health
- worker/job health
- business-critical metrics

Avoid wall-of-graphs dashboards that no one uses.

## Health Checks

Health checks tell infrastructure whether a process should receive traffic.

Types:

- liveness: is the process alive?
- readiness: can it serve traffic?
- dependency health: are critical dependencies reachable?
- startup: has initialization completed?

Best practices:

- keep liveness simple
- make readiness reflect real serving ability
- do not make health checks so expensive they cause outages
- distinguish degraded dependency from app death
- expose version/build metadata separately when useful

## Logging And Privacy

Observability must not leak sensitive data.

Never log:

- passwords
- API keys
- bearer tokens
- raw cookies
- private keys
- payment card data
- credential-bearing URLs
- sensitive PII unless policy explicitly allows it

Be careful with:

- emails
- names
- addresses
- IP addresses
- user-generated content
- document text
- health/financial/legal data

Use redaction and allowlists where possible.

## Workflow

1. Identify the system or workflow.
2. Identify user-impacting outcomes.
3. Define the main signals needed.
   - logs
   - metrics
   - traces
   - events
4. Add or review instrumentation.
5. Define dashboards.
6. Define alerts.
7. Define runbooks or first-response notes.
8. Verify signals in staging or production.
9. Review noise and gaps after incidents or deploys.

## Output Standard

Start with:

- service/workflow being observed
- key user outcomes
- logs needed
- metrics needed
- traces needed
- alerts recommended
- dashboards recommended
- privacy/security concerns

When reviewing alerting, include:

| Alert | Signal | Threshold | Owner | Action |
|---|---|---|---|---|

## Guardrails

- Do not create alerts without an owner and action.
- Do not page humans for non-actionable noise.
- Do not log secrets or sensitive payloads.
- Do not use high-cardinality metric labels casually.
- Do not rely only on logs for latency/error monitoring.
- Do not add tracing without propagating context across service/job boundaries.
- Do not treat health checks as full integration tests.
- Prefer a few useful signals over many decorative dashboards.
