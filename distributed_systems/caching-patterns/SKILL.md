---
name: caching-patterns
description: Design, evaluate, or debug caching across an application stack, including simple web-app defaults, browser caching, CDN/edge caching, API caching, application memory, distributed cache, database/query caching, read models, search/vector indexes, data pipeline caches, cache keys, TTLs, freshness, security, observability, and common pitfalls.
when_to_use: Use when deciding whether to add caching, choosing simple web-app caching defaults, improving latency or cost, reducing repeated reads/computation, protecting downstream systems, debugging stale data, designing cache keys, choosing TTLs, or reviewing caching at any layer of a web app, backend service, data pipeline, or distributed system.
argument-hint: "[workflow-or-system-component]"
---

# Caching Patterns

Use this skill when a system may benefit from reusing previously computed, fetched, or rendered data.

## Core Idea

A cache stores a copy of data or computation results so future requests can be served faster or with less load.

Basic shape:

```text
Request -> Check cache
  -> cache hit: return cached value
  -> cache miss: compute/fetch value, store in cache, return value
```

Caching helps when the same data is read repeatedly and perfect freshness is not always required.

## Simple Starting Points For Web Apps

For most standard web apps, start simple:

```text
1. Cache static assets aggressively.
2. Do not cache authenticated HTML/API responses by default.
3. Use database indexes and query fixes before application caching.
4. Add CDN caching for public content.
5. Add app/distributed caching only for proven hot or expensive reads.
```

### Static Assets

Best default:

- fingerprint asset filenames, such as `app.abc123.js`
- serve with long cache TTL
- deploy new filenames when content changes

Typical headers:

```text
Cache-Control: public, max-age=31536000, immutable
```

Good for:

- JS bundles
- CSS
- fonts
- images with content hashes

### HTML Pages

Default:

- avoid long-lived caching for authenticated or personalized HTML
- use short caching or no-store for dynamic user-specific pages

Typical private/authenticated default:

```text
Cache-Control: private, no-store
```

Public marketing/content pages may be cached if they do not contain user-specific data.

### API Responses

Default:

- do not cache authenticated API responses until cache keys and permissions are designed
- consider short TTLs for public read-only APIs
- use ETags or conditional requests when clients repeatedly fetch the same resource

Good early API cache candidates:

- public configuration
- public catalog data
- reference data
- read-heavy anonymous endpoints

Avoid early API caching for:

- permissions
- billing
- account state
- checkout
- admin data
- tenant-specific private data without tenant-aware keys

### Database And Query Performance

Before adding an application cache:

- inspect slow queries
- add appropriate indexes
- avoid N+1 queries
- paginate large lists
- select only needed fields

Caching is often the second step after making the underlying access pattern sane.

### In-Process Memoization

Use for:

- repeated computation within a single request
- small stable lookups
- pure functions with bounded input space

Avoid:

- unbounded global memoization
- user-specific values without scope
- using process memory as durable state

### Distributed Cache

Add Redis/Memcached only when:

- multiple app instances need shared cache
- cache hit rate is expected to be meaningful
- the data is expensive or hot enough to justify operational complexity
- invalidation/TTL and observability are defined

## Web App Best Practices

- Cache static assets first; it is the safest and highest-leverage default.
- Prefer versioned asset filenames over manual asset invalidation.
- Keep user-specific pages and API responses private or uncached unless designed carefully.
- Include tenant/user/role dimensions in cache keys for private data.
- Use short TTLs before building complex invalidation.
- Add jitter to TTLs for hot keys.
- Use stale-while-revalidate for public content when slightly stale responses are acceptable.
- Treat cache as disposable unless explicitly designed otherwise.
- Make cache behavior visible with headers, metrics, and logs.
- Provide a manual purge path for CDN or public content caches.
- Test that user A cannot receive user B's cached data.
- Document which layer owns each cache.

## What Caching Helps With

Caching can help:

- reduce latency
- reduce database load
- reduce external API calls
- reduce CPU-heavy recomputation
- absorb read bursts
- improve frontend responsiveness
- reduce cloud cost
- protect rate-limited dependencies
- serve static assets efficiently
- support offline or degraded behavior
- reduce repeated pipeline work

Caching does not remove complexity. It trades freshness and invalidation complexity for speed, scale, or cost reduction.

## When To Use Caching

Consider caching when:

- reads are repeated
- data is expensive to compute or fetch
- data changes less often than it is read
- downstream systems are slow, costly, or rate-limited
- users can tolerate bounded staleness
- a cache key can be designed safely
- invalidation or TTL behavior can be explained
- the system has observability for hit/miss and staleness

Do not cache first when:

- the result must always be strongly fresh
- the access pattern is not understood
- the underlying query or algorithm is obviously inefficient
- security/authorization boundaries are unclear
- cache invalidation cannot be reasoned about
- the cached data is rarely reused
- stale data would create serious business harm

## Layers Of Caching

### Browser Cache

Stores assets or responses in the user's browser.

Good for:

- static assets
- images
- fonts
- JS/CSS bundles
- public cacheable responses

Mechanisms:

- `Cache-Control`
- `ETag`
- `Last-Modified`
- service workers
- localStorage/sessionStorage/IndexedDB for app-managed data

Pitfalls:

- stale frontend bundles
- caching user-specific responses accidentally
- hard refresh/debug confusion
- service worker serving old assets

### CDN / Edge Cache

Stores content close to users.

Good for:

- static assets
- images
- public pages
- anonymous GET responses
- expensive public API reads with safe cache keys

Helps with:

- global latency
- origin load reduction
- traffic bursts

Pitfalls:

- caching private data
- missing `Vary`/header/query/cookie key dimensions
- stale deployments
- over-forwarding headers, reducing cache hit rate
- under-forwarding headers, serving wrong content

### Reverse Proxy / Gateway Cache

Caches at Nginx, API gateway, Varnish, or similar layer.

Good for:

- public or semi-public API responses
- route-level caching
- shielding app servers

Pitfalls:

- confusing application cache and proxy cache behavior
- auth-aware cache keys
- invalidation across deployments

### Application In-Memory Cache

Stores data inside one app process.

Good for:

- small reference data
- config lookup
- per-process computed values
- short-lived hot values

Pitfalls:

- not shared across instances
- disappears on restart
- memory growth
- inconsistent values across servers
- unsafe for durable dedupe or critical coordination

### Distributed Cache

Stores values in shared infrastructure such as Redis or Memcached.

Good for:

- shared hot reads
- session data when appropriate
- rate limiting counters
- feature/config lookups
- expensive computed results
- cross-instance cache consistency

Pitfalls:

- cache outage becomes app outage
- hot keys
- stampedes
- missing tenant/user scoping
- memory pressure and eviction surprises
- treating cache as source of truth

### Database / Query Cache

Caches query plans, pages, materialized results, or repeated expensive query outputs.

Good for:

- repeated analytical queries
- materialized views
- summary tables
- database buffer/page cache

Pitfalls:

- hiding bad query design
- stale materialized views
- write amplification
- unclear refresh semantics

### Read Models And Materialized Views

Precomputed views optimized for reads.

Good for:

- dashboards
- list pages
- denormalized views
- reporting
- search/filter-heavy workflows

Pitfalls:

- eventual consistency
- rebuild strategy
- backfill complexity
- bugs from stale derived data

### Search / Vector Indexes As Caches

Search and vector indexes are often derived retrieval structures, not source-of-truth storage.

Good for:

- full-text search
- faceted search
- semantic retrieval
- recommendation candidates

Pitfalls:

- index lag
- permission filtering
- stale embeddings
- needing rebuilds after schema/model changes
- treating derived index data as canonical

### Data Pipeline Caches

Used to avoid recomputing pipeline stages.

Good for:

- expensive transformations
- downloads
- model inference outputs
- intermediate datasets
- checkpointed processing

Pitfalls:

- cache invalidation when source data changes
- stale intermediate artifacts
- poor lineage tracking
- non-reproducible runs

## Cache Strategy Patterns

### Cache-Aside / Lazy Loading

Application checks cache first. On miss, reads from source and writes cache.

Good for:

- common application caches
- simple read-heavy workflows

Tradeoffs:

- first request is slow
- stale data possible
- stampede risk on hot misses

### Write-Through

Writes go to cache and source of truth together.

Good for:

- keeping cache warm after writes

Tradeoffs:

- write latency increases
- failure handling is harder

### Write-Behind / Write-Back

Writes go to cache first and are persisted later.

Good for:

- very high write throughput when eventual persistence is acceptable

Tradeoffs:

- data loss risk
- complex failure handling
- rarely appropriate for critical business records

### Read-Through

Cache layer knows how to load missing values.

Good for:

- standardized cache infrastructure

Tradeoffs:

- cache layer becomes more complex

### Refresh-Ahead

Cache refreshes before expiry.

Good for:

- hot keys
- predictable expensive reads

Tradeoffs:

- extra background complexity
- may refresh unused data

## Cache Key Design

A good cache key includes every dimension that changes the result.

Consider:

- resource ID
- tenant/workspace
- user/role/permissions
- locale
- feature flags
- query params
- filters/sort/pagination
- API version
- data version
- model version for embeddings/ML outputs

Bad cache keys:

- omit tenant/user for private data
- omit filters or pagination
- include noisy irrelevant values that destroy hit rate
- use unstable serialized objects without normalization
- rely on hidden global state

## Freshness And Invalidation

Every cache needs a freshness story.

Options:

- TTL expiration
- explicit invalidation on write
- versioned keys
- event-driven invalidation
- manual purge
- stale-while-revalidate
- rebuild/reindex
- cache busting with asset hashes

Ask:

- How stale can this data be?
- Who can see stale data?
- What business harm can staleness cause?
- What write should invalidate the cache?
- Can stale data be served during dependency outages?
- How do we observe stale or wrong cache entries?

## Common Pitfalls

### Cache Stampede

Many requests miss at once and all recompute the same value.

Mitigations:

- request coalescing
- locks
- jittered TTLs
- stale-while-revalidate
- refresh-ahead
- rate limits

### Hot Keys

One key receives too much traffic.

Mitigations:

- shard/split keys
- local near-cache
- request coalescing
- precompute
- adjust data model

### Stale Or Wrong Data

Cache serves outdated or incorrect values.

Mitigations:

- TTLs
- versioned keys
- invalidation events
- source-of-truth checks for critical paths
- observability

### Security Leaks

Private data is cached under a public or underspecified key.

Mitigations:

- include tenant/user/permission dimensions
- avoid shared caching for private responses unless designed carefully
- use `Cache-Control: private` or `no-store` where appropriate
- test cross-user access

### Cache As Source Of Truth

System loses data because important state only lived in cache.

Mitigations:

- keep durable data in database/object storage
- treat cache as rebuildable
- document exceptions explicitly

### Hidden Cache Layers

Multiple caches interact unpredictably.

Mitigations:

- map all cache layers
- expose cache headers/metrics
- document invalidation path

## Workflow

1. Identify the symptom or goal.
   - latency
   - cost
   - repeated computation
   - downstream overload
   - rate limit
   - offline/degraded behavior
2. Identify the source of truth.
3. Identify read/write pattern.
   - read frequency
   - write frequency
   - acceptable staleness
   - user/tenant sensitivity
4. Start with simple web-app defaults when applicable.
   - static asset caching
   - no-store/private for authenticated dynamic pages
   - query/index fixes before app cache
   - CDN for public content
5. Choose cache layer.
   - browser
   - CDN
   - proxy/gateway
   - app memory
   - distributed cache
   - database/materialized view
   - search/vector index
   - pipeline artifact
6. Define key and scope.
7. Define freshness/invalidation.
8. Define failure behavior.
   - cache miss
   - cache outage
   - stale value
   - source unavailable
9. Define observability.
   - hit rate
   - miss rate
   - latency
   - evictions
   - memory
   - stale serves
   - invalidation events
10. Test correctness, staleness, and security boundaries.

## Output Standard

Start with:

- whether caching is recommended
- simplest safe starting point
- what is being cached
- source of truth
- cache layer
- cache key
- freshness/invalidation plan
- expected benefit
- tradeoffs and risks
- observability

When comparing options, include:

| Cache Layer | Helps With | Tradeoff | When To Choose |
|---|---|---|---|

## Guardrails

- Cache static assets first; be much more cautious with dynamic private data.
- Do not cache private data without tenant/user/permission-aware keys.
- Do not cache before understanding the read/write pattern.
- Do not use caching to hide obviously broken queries or algorithms.
- Do not treat cache as source of truth unless explicitly designed as durable storage.
- Do not add a cache without invalidation or TTL semantics.
- Do not add a cache without hit/miss/staleness observability.
- Do not memoize unbounded inputs without memory limits.
- Prefer the lowest layer that safely solves the problem with the least complexity.
