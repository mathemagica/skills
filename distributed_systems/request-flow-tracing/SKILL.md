---
name: request-flow-tracing
description: Explain, trace, design, or debug how a user request flows through a distributed web system from browser to DNS, CDN/edge cache, TLS, load balancer, reverse proxy, application servers, caches, queues, databases, external services, and back to the browser.
---

# Request Flow Tracing

Use this skill when a user wants to understand, explain, design, or debug the path a request takes through a web system.

## First Principle

A user request is not one step. It is a chain of network, routing, compute, data, and response-processing steps.

To understand behavior or performance, trace the request across each boundary and ask:

- What component receives the request?
- What does it decide?
- What does it forward, cache, reject, or transform?
- What evidence can prove the request reached that step?
- What response or error comes back?

## Typical Request Flow

A simplified web request often looks like:

```text
Browser
  -> DNS
  -> CDN / Edge Cache
  -> TLS Termination
  -> Load Balancer
  -> Reverse Proxy / API Gateway
  -> Application Server
  -> Cache / Queue / Internal Service
  -> Database / Object Storage / External API
  <- Response assembled by Application Server
  <- Load Balancer / Edge
  <- Browser receives and renders response
```

Not every system has every step. Some systems are static sites, serverless apps, monoliths, multi-service architectures, mobile APIs, or internal-only services.

## Core Components

### Browser / Client

The browser starts the request.

It handles:

- URL parsing
- DNS lookup initiation
- connection reuse
- TLS negotiation
- cookies and auth headers
- request headers and body
- caching rules
- redirects
- CORS enforcement
- rendering the response
- JavaScript-triggered API calls

Evidence:

- browser Network tab
- console logs
- request/response headers
- timing waterfall
- cookies/storage
- CORS/preflight details

### DNS

DNS translates a domain name into an IP address or another name.

Example:

```text
app.example.com -> CDN hostname -> edge IP
```

DNS can involve:

- A records
- AAAA records
- CNAME records
- TTLs
- hosted zones
- split-horizon/private DNS
- geo/latency routing
- failover routing

DNS answers the question: "Where should the client connect for this name?"

DNS does not usually know application paths like `/api/users`.

Evidence:

- `dig`
- `nslookup`
- DNS provider records
- TTL values
- browser/network resolver behavior

### CDN / Edge Cache

A CDN or edge cache sits close to users and may serve cached content without reaching origin servers.

It can handle:

- static asset caching
- HTML caching when configured
- image optimization
- compression
- TLS termination
- edge redirects
- edge functions
- WAF/security checks
- bot protection

Cache outcomes:

- cache hit: served from edge
- cache miss: forwarded to origin
- stale hit: old cached content served under policy
- bypass: request deliberately goes to origin

Evidence:

- response headers such as `cache-control`, `age`, `etag`, `x-cache`, `cf-cache-status`, `x-served-by`
- CDN logs
- origin access logs
- browser Network tab

### TLS / HTTPS

TLS secures the connection and proves server identity with certificates.

TLS may terminate at:

- CDN
- load balancer
- reverse proxy
- application server

Important questions:

- Where does HTTPS terminate?
- Is traffic re-encrypted to the origin?
- Are certificates valid?
- Are redirects forcing HTTPS?
- Are cookies marked `Secure` when required?

Evidence:

- browser security panel
- certificate details
- load balancer/CDN TLS config
- TLS handshake errors

### Load Balancer

A load balancer distributes requests across multiple healthy backend targets.

It can route by:

- host
- path
- port
- protocol
- target group
- health check status
- weighted routing
- sticky sessions

It helps scale by allowing multiple application servers behind one stable entry point.

Example:

```text
Load Balancer
  -> app-server-1
  -> app-server-2
  -> app-server-3
```

If one server fails health checks, the load balancer stops routing traffic to it.

Evidence:

- load balancer access logs
- target health
- target group membership
- status codes
- latency metrics
- health check logs

### Reverse Proxy / API Gateway

A reverse proxy or API gateway sits before app code and handles routing or cross-cutting concerns.

It may handle:

- path routing
- API version routing
- authentication prechecks
- rate limiting
- request size limits
- header normalization
- compression
- WebSocket upgrades
- CORS
- service discovery

Evidence:

- gateway logs
- route config
- upstream response codes
- rate limit headers
- request IDs

### Application Server

The application server runs business code.

It handles:

- routing to handler/controller/resolver
- request parsing
- auth and authorization
- validation
- business logic
- rendering or JSON serialization
- calls to databases, caches, queues, internal services, and external APIs
- response construction

With multiple servers behind a load balancer, each instance should usually be stateless or share state through durable stores such as databases, caches, or object storage.

Evidence:

- app logs
- traces/spans
- request IDs
- metrics
- debugger
- server error stack traces

### Cache

Caches reduce repeated work or repeated reads.

Common locations:

- browser cache
- CDN cache
- reverse proxy cache
- application in-memory cache
- distributed cache such as Redis or Memcached
- database query cache or materialized views

Questions:

- What is cached?
- What is the cache key?
- What is the TTL?
- How is it invalidated?
- Can stale data be served?
- Is cache scoped by user/tenant/permissions?

Evidence:

- cache headers
- cache hit/miss metrics
- Redis/Memcached metrics
- application logs
- CDN headers

### Queue / Background Worker

Some requests enqueue work instead of doing everything synchronously.

Used for:

- email sending
- media processing
- imports/exports
- webhooks
- retries
- long-running jobs
- asynchronous side effects

Flow:

```text
Request -> App Server -> Queue -> Worker -> Database/External API
```

The initial response may return before the work finishes.

Evidence:

- queue depth
- job logs
- retry/dead-letter queues
- worker metrics
- job IDs

### Database

The database stores source-of-truth data or queryable records.

The app may:

- read data
- write data
- run transactions
- enforce constraints
- query indexes
- call stored procedures
- hit read replicas
- experience lock waits or connection pool limits

Questions:

- Is this read or write?
- Which database receives it?
- Is it primary or replica?
- Is a transaction involved?
- Are indexes used?
- Is the data fresh?
- Are permissions enforced before access?

Evidence:

- query logs
- slow query logs
- explain plans
- database metrics
- connection pool stats
- replication lag
- locks/deadlocks

### Object Storage / Files

Large files often live outside the database.

Used for:

- images
- videos
- documents
- exports
- backups
- logs
- model artifacts

Evidence:

- object key/path
- signed URL generation
- storage access logs
- content type
- permissions
- lifecycle/retention rules

### External Services

Requests may call third-party APIs or internal services.

Questions:

- Is the dependency required for the response?
- What timeout applies?
- Are retries safe?
- Is the call idempotent?
- What happens if it fails?

Evidence:

- outbound request logs
- traces
- dependency metrics
- response status/body
- retry logs

## Response Path Back To Browser

The response returns through much of the same path:

```text
Database/Service
  -> Application Server
  -> Proxy/Gateway
  -> Load Balancer
  -> CDN/Edge
  -> Browser
```

At each step, headers or body can be transformed.

Important response concerns:

- status code
- response body
- cookies
- caching headers
- redirects
- compression
- CORS headers
- security headers
- content type
- streaming/chunking
- error wrapping

## Debugging Workflow

1. Start at the browser.
   - What URL?
   - What method?
   - What status?
   - What response?
   - Was it cached?
2. Check DNS and routing when the browser cannot connect or reaches the wrong service.
3. Check CDN/edge headers for cache hit/miss, redirects, WAF blocks, or stale content.
4. Check load balancer health and logs.
5. Check gateway/proxy route matching.
6. Check application logs using request ID or trace ID.
7. Check database/cache/queue/external dependency evidence.
8. Trace the response back to where it changed, failed, or slowed down.
9. Identify the first component whose output differs from expectation.

## Latency Breakdown

Request latency can come from:

- DNS lookup
- TCP/TLS connection setup
- CDN cache miss
- load balancer queueing
- proxy/gateway routing
- application CPU
- database query time
- lock waits
- cache misses
- external API latency
- queueing
- serialization
- response transfer
- browser rendering

Use timing waterfalls, traces, and metrics to locate the largest segment.

## Multiple Servers Behind A Load Balancer

Multiple app servers help scale stateless request handling.

Requirements:

- shared persistent state lives outside the instance
- sessions are stored in cookies, shared cache, or database
- uploaded files go to shared storage, not local disk
- background jobs are coordinated through queues
- deployments and migrations are compatible across versions
- health checks reflect real readiness
- logs/metrics are centralized

Common problems:

- sticky-session assumptions
- one instance has stale config
- local filesystem writes disappear
- cache warmup differs by instance
- rolling deploys run incompatible code versions
- load balancer routes to unhealthy instances

## Output Standard

Start with a request-flow map:

```text
Browser -> DNS -> CDN -> Load Balancer -> App Server -> Database -> App Server -> Browser
```

Then identify:

- where the request is expected to go
- what each component is responsible for
- what evidence confirms or disproves each step
- where the failure or latency likely begins
- the next diagnostic action

For architecture explanations, include:

- which components exist
- which components are optional
- what each component adds
- what complexity each component introduces

## Guardrails

- Do not assume a request reached the backend without checking browser/network and edge evidence.
- Do not assume a backend bug when CDN cache or DNS routing may be serving old content.
- Do not assume load balancing helps if the bottleneck is the database.
- Do not store instance-local state when multiple servers serve the same app.
- Do not cache user-specific content without permission-aware cache keys.
- Do not debug only one layer when the symptom crosses network boundaries.
- Prefer evidence from request IDs, traces, logs, and headers over guesses.
