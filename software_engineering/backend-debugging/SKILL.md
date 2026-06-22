---
name: backend-debugging
description: Debug backend code using scientific-method diagnosis, one-variable-at-a-time experiments, server logs, traces, tests, debuggers, breakpoints, runtime state inspection, database/API observation, and clear frontend/backend execution boundaries.
when_to_use: Use when diagnosing backend bugs, API failures, server errors, data bugs, job failures, integration issues, auth problems, concurrency bugs, request handling issues, or uncertainty about whether code executes on the frontend or backend.
argument-hint: "[endpoint-or-service-or-bug]"
---

# Backend Debugging

Use this skill when backend code behaves incorrectly and needs diagnosis before changing implementation.

## First Principle

Debugging is an experiment, not a hunch.

Use the scientific method:

1. Observe the failure.
2. Form a specific hypothesis.
3. Change or inspect one variable at a time.
4. Measure the result.
5. Keep, revise, or reject the hypothesis.
6. Repeat until the smallest responsible cause is identified.

Do not change several things at once unless the goal is temporary isolation and you can unwind each change cleanly.

## When To Use

- An API endpoint returns the wrong status, data, or error.
- A server route, controller, resolver, worker, cron job, or queue consumer fails.
- Logs show exceptions, timeouts, retries, or unexpected branches.
- Data is missing, stale, duplicated, corrupted, or written in the wrong shape.
- Auth, permissions, sessions, or request context behave unexpectedly.
- A backend integration with a database, cache, queue, storage system, or external API fails.
- A bug only appears in one environment, tenant, user role, input, or deployment.
- It is unclear whether the failing code runs in the browser/client or on the server/backend.

## Goal

Find the smallest observable cause of the backend bug, fix it at the right layer, and verify the behavior with tests or runtime evidence.

## Core Debugging Workflow

1. Reproduce or characterize the failure.
   - endpoint/job/service
   - environment
   - input payload or event
   - user/tenant/auth context
   - expected behavior
   - actual behavior
   - frequency and regression window
2. Capture baseline evidence.
   - logs
   - stack traces
   - request IDs or trace IDs
   - status codes
   - response body
   - database records
   - queue messages
   - external API responses
   - relevant configuration
3. Form one hypothesis at a time.
   - "The request body is parsed incorrectly."
   - "The user lacks the expected permission."
   - "The database query returns no rows."
   - "The worker retries because the downstream API times out."
4. Choose the smallest observation or experiment that could disprove the hypothesis.
5. Inspect runtime behavior with logs, tests, debugger breakpoints, traces, or database/API probes.
6. Change only one variable when testing a fix.
7. Verify the fix with the original reproduction and a focused regression test when practical.
8. Remove temporary logs, debug flags, and local-only instrumentation.

## One-Variable-At-A-Time Debugging

When diagnosing, isolate variables such as:

- input payload
- user identity or role
- feature flag
- environment variable
- database row/state
- external dependency response
- cache state
- queue message
- time/date
- concurrency level
- network timeout
- code branch

Examples:

- Change the user role but keep the payload identical.
- Change the payload field but keep the user and database state identical.
- Bypass cache only after recording what cache key and value were used.
- Replace an external API with a fixture only after confirming the outgoing request shape.

This prevents a common failure mode: making the bug disappear without learning which condition mattered.

## What Backend Debuggers Tell You

A debugger shows what the running backend process is doing at a precise point in execution.

Use it to inspect:

- call stack: how execution reached this line
- local variables: parsed inputs, IDs, flags, intermediate values
- request context: headers, auth identity, tenant, correlation ID
- control flow: which branch is taken and why
- object references: whether data is mutated, copied, or shared
- exceptions: where an error originates before framework wrapping
- async flow: where promises, futures, callbacks, goroutines, tasks, or threads resume
- database calls: query text, parameters, transaction state, result shape
- external calls: outgoing URL, method, headers, payload, timeout, response
- locks and concurrency clues: waiting threads/tasks, shared mutable state, race conditions
- configuration: environment-derived values at runtime

A debugger does not tell you what the backend should do. It tells you what it actually did with the real runtime state.

## Debugger Techniques

Use language/framework-native debugging tools when available:

- breakpoints for suspicious lines
- conditional breakpoints for one user, request ID, record ID, or payload shape
- logpoints when pausing is too disruptive
- exception breakpoints to stop where errors originate
- step over/into/out to trace control flow
- watch expressions for changing values
- stack inspection for framework and application boundaries
- thread/task inspection for concurrency issues

Use caution:

- Avoid pausing production processes unless explicitly safe and approved.
- Prefer staging, local reproduction, test fixtures, or non-pausing observability in production.
- Be careful with secrets in debugger views, logs, screenshots, and reports.

## Backend Observability Tools

### Logs

Use for:

- exceptions and stack traces
- request lifecycle events
- branch decisions
- external dependency failures
- job retries
- sanitized inputs and IDs

Good logs include correlation IDs and omit secrets.

### Traces

Use for:

- request path across services
- timing by span
- downstream calls
- retries and timeouts
- locating the slow or failing service boundary

### Metrics

Use for:

- error rate
- request rate
- latency percentiles
- queue depth
- retry counts
- CPU/memory
- database connection pool use
- cache hit rate

### Tests

Use for:

- reproducing a bug deterministically
- locking in the expected behavior
- checking edge cases without changing production state

Prefer the narrowest test that proves the bug and the fix, then add broader integration coverage when the failure crosses boundaries.

## Frontend vs Backend Boundary

In client-server systems, the frontend runs in the user's browser, mobile app, or client runtime. The backend runs on servers, serverless functions, workers, queues, cron jobs, databases, and managed services.

The line is usually the network/API boundary:

- Frontend code prepares user interactions, renders UI, manages local state, and sends requests.
- Backend code receives requests/events, enforces trusted business rules, checks authorization, reads/writes source-of-truth data, calls trusted integrations, and returns responses.

## How To Tell Where Code Executes

Code is likely frontend/client-side if:

- it runs in the browser DevTools console or appears in browser stack traces
- it accesses `window`, `document`, DOM APIs, browser storage, or browser events
- it lives in client components, frontend bundles, static assets, or browser-visible source maps
- it handles clicks, form input, viewport changes, or client routing
- its logs appear in the browser console
- it cannot safely access secrets

Code is likely backend/server-side if:

- it runs in server logs, worker logs, or cloud function logs
- it accesses databases, queues, file/object storage, server environment variables, or secret managers
- it handles HTTP routes, API controllers, resolvers, middleware, server actions, jobs, or cron tasks
- it enforces authorization or trusted business rules
- its stack trace appears in the server process
- it can access private network resources or credentials

Code can be ambiguous in full-stack frameworks. Check:

- file naming conventions such as `.server`, `.client`, server components, API routes, or route handlers
- framework docs for server/client boundaries
- whether the module is imported by browser-bundled code
- whether logs appear in the terminal/server logs or browser console
- whether browser-only globals are available
- whether secrets or database clients are accessible
- whether the code runs during build, server render, hydration, request handling, or client interaction

If unsure, add a temporary, sanitized log in the smallest safe place and observe where it appears. Remove it before finishing.

## Common Backend Bug Categories

### API Contract Bugs

Symptoms:

- wrong status code
- missing field
- wrong response shape
- client/server validation mismatch

Strategy:

- inspect request and response
- compare implementation to API contract
- verify serializer/schema behavior
- add contract or request tests

### Data Bugs

Symptoms:

- wrong records returned
- duplicate writes
- missing updates
- stale reads
- inconsistent derived data

Strategy:

- inspect source-of-truth data
- trace query parameters and transaction boundaries
- check cache/read-model/index freshness
- distinguish canonical data from derived data

### Auth And Permission Bugs

Symptoms:

- unauthorized users gain access
- authorized users are blocked
- tenant or role behavior is wrong

Strategy:

- inspect authenticated principal
- inspect roles/scopes/tenant context
- verify authorization checks happen on the backend
- test allowed and denied paths

### Integration Bugs

Symptoms:

- downstream API errors
- timeouts
- retries
- malformed payloads
- webhook/job failures

Strategy:

- inspect outgoing request shape
- inspect sanitized downstream response
- check retries and idempotency
- reproduce with fixtures or recorded responses when possible

### Concurrency Bugs

Symptoms:

- race conditions
- duplicate processing
- lost updates
- intermittent failures
- lock waits

Strategy:

- inspect transaction boundaries
- check idempotency keys
- look for shared mutable state
- reproduce with controlled concurrency
- add database constraints or locking where appropriate

## Output Standard

Start with:

- reproduction or observed symptom
- expected behavior
- actual behavior
- current hypothesis
- evidence gathered
- next one-variable experiment or fix

When reporting debugger findings, include:

- breakpoint or tool used
- runtime values observed
- call stack or request path if relevant
- why the observation supports or rejects the hypothesis

When fixing, include:

- the smallest responsible code change
- verification performed
- test coverage added or updated
- remaining uncertainty or production follow-up if any

## Guardrails

- Do not make multiple behavioral changes before measuring which one matters.
- Do not debug only from source code when runtime values are available.
- Do not log secrets, tokens, passwords, raw cookies, or credential-bearing URLs.
- Do not trust frontend checks for backend authorization.
- Do not assume the frontend is wrong without inspecting the backend request/response.
- Do not assume the backend is wrong without checking whether the failing code actually runs on the client.
- Do not pause or mutate production systems with a debugger unless explicitly safe and approved.
- Remove temporary logs, debug prints, and debugger statements before finishing.
