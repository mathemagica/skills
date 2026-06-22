---
name: third-party-data-integration
description: Design, review, or debug third-party data integrations, including API pulls, webhooks, batch imports, data pipelines, sync jobs, source-of-truth ownership, external ID mapping, reconciliation, idempotency, freshness, validation, rate limits, retries, observability, and safe integration with key domain tables.
when_to_use: Use when integrating data from external APIs, partner systems, SaaS tools, vendors, data feeds, files, warehouses, CRMs, payment providers, calendars, product catalogs, identity providers, or other third-party systems into an application or data platform.
argument-hint: "[integration-or-source-system]"
---

# Third Party Data Integration

Use this skill when a system needs to ingest, sync, reconcile, or depend on data from an external system.

## Core Idea

Third-party data integration is the process of bringing external data into your system while preserving clarity about ownership, identity, freshness, correctness, and failure behavior.

The most important question is:

```text
Which system is the system of record for each domain concept?
```

Without a clear system of record, integrations create duplicate truth, conflicting updates, broken permissions, and unreliable reporting.

## Integration Modes

### Pull From API

Your system periodically calls a third-party API.

Good for:

- scheduled syncs
- systems without webhooks
- backfills
- incremental imports
- reconciliation jobs

Design concerns:

- pagination
- rate limits
- auth/token refresh
- partial failures
- checkpoint/cursor
- deleted records
- API version changes
- vendor downtime

### Webhooks / Push Events

Third party sends events to your system.

Good for:

- near-real-time updates
- lifecycle events
- payment status
- calendar changes
- CRM updates
- document signing
- fulfillment status

Design concerns:

- signature verification
- event ID dedupe
- out-of-order delivery
- retries
- replay attacks
- fast acknowledgement
- async processing
- reconciliation with API pull

### Batch Files / Data Feeds

Third party provides CSV, JSON, XML, Parquet, SFTP, object storage, or warehouse exports.

Good for:

- large datasets
- nightly updates
- legacy vendors
- data warehouse integration
- partner feeds

Design concerns:

- file arrival detection
- schema validation
- idempotent loading
- partitioning
- bad row handling
- checksums
- duplicates
- late or missing files

### Direct Database / Warehouse Sharing

Third party exposes data through a warehouse, shared database, or marketplace.

Good for:

- analytics
- large-scale reporting
- low-latency internal data sharing

Design concerns:

- read-only access
- schema drift
- ownership boundaries
- privacy/security
- freshness expectations
- lineage

## System Of Record

A system of record is the authoritative place where a piece of data is created, owned, and corrected.

For each domain concept, decide:

- Is our system the source of truth?
- Is the third party the source of truth?
- Is ownership split by field?
- Is the third party only a derived source?
- Can users edit this locally?
- If both systems update it, which wins?
- How are conflicts resolved?

Examples:

| Domain Concept | System Of Record | Local Role |
|---|---|---|
| Customer profile | CRM | cached copy for display |
| Payment status | Payment provider | synced status for app workflows |
| User permissions | Our app | never overwritten by CRM |
| Product catalog | Vendor feed | imported canonical catalog |
| Analytics events | Our app | emitted to warehouse |
| Calendar event | Google Calendar | mirrored with external ID |

Avoid having two systems silently believe they both own the same field.

## External ID Mapping

Most integrations require mapping external identities to local domain records.

Use explicit mapping fields or tables.

Examples:

- `stripe_customer_id` on `customers`
- `hubspot_contact_id` on `contacts`
- `external_source + external_id`
- `provider + account_id + external_object_id`
- `source_system_record_mappings`

For key domain tables, decide:

- local primary key
- external provider key
- natural key if any
- tenant/workspace scope
- uniqueness constraints
- merge/deduplication policy

Example mapping table:

```text
external_mappings
- id
- tenant_id
- provider
- external_object_type
- external_object_id
- local_object_type
- local_object_id
- first_seen_at
- last_seen_at
- external_updated_at
```

Recommended uniqueness:

```text
UNIQUE(tenant_id, provider, external_object_type, external_object_id)
```

## Reconciliation

Reconciliation compares local state against external state to detect drift.

Use reconciliation when:

- webhooks may be missed
- API pulls are incremental
- third-party status matters for correctness
- payments, fulfillment, or account state can change externally
- imports can partially fail
- duplicate or merged records are possible

Reconciliation can:

- detect missing records
- detect deleted records
- fix stale statuses
- resolve duplicate mappings
- identify conflicts
- backfill failed updates
- produce audit reports

Common pattern:

```text
Webhook -> fast event capture -> async processing
Scheduled reconciliation -> API pull -> compare external vs local -> repair/report
```

## Data Modeling

For imported data, model:

- raw external payload when useful
- normalized local record
- mapping to external ID
- sync status
- last synced timestamp
- external updated timestamp
- source system
- error state
- conflict state
- audit trail

Keep raw payloads when:

- debugging vendor issues
- auditability matters
- schemas change often
- reprocessing may be useful

Do not let raw vendor shape leak everywhere into the domain model. Normalize at the boundary.

## Safeguards

### Validation

Validate:

- schema shape
- required fields
- enum values
- date/time format
- IDs
- tenant scope
- referential integrity
- record counts
- checksums for files
- unexpected nulls

### Idempotency

Every import, webhook, or sync should tolerate duplicates.

Use:

- external event IDs
- unique constraints
- upserts
- mapping tables
- processed-event tables
- deterministic file/batch IDs

### Rate Limits And Backoff

Respect third-party limits.

Use:

- pagination
- request throttling
- exponential backoff
- retry-after headers
- circuit breakers
- queued sync jobs
- provider-specific quotas

### Partial Failure Handling

Plan for:

- some records fail validation
- API page fails halfway
- token expires mid-sync
- webhook processing fails after ack
- local write succeeds but downstream publish fails
- vendor returns inconsistent data

Use:

- checkpoints
- resumable syncs
- dead-letter queues
- error tables
- retry jobs
- reconciliation reports

### Security

Protect:

- API tokens
- webhook signing secrets
- OAuth refresh tokens
- vendor payloads with PII
- logs
- file drops
- object storage paths

Use:

- least privilege scopes
- secrets manager
- signature verification
- encrypted storage
- audit logs
- tenant isolation

## Freshness And Latency

Define freshness expectations.

Examples:

- payment status within 1 minute
- CRM contact sync nightly
- product catalog daily
- analytics events hourly
- calendar updates near-real-time

Freshness choices affect:

- polling frequency
- webhook need
- queue sizing
- rate-limit pressure
- UI expectations
- reconciliation cadence

Expose stale data clearly when users depend on it.

## Integration Architecture Patterns

### Direct Request-Time Call

```text
User Request -> Our App -> Third-Party API -> Response
```

Use only when:

- the response truly needs live external data
- third-party latency is acceptable
- failure behavior is clear

Risks:

- slow user requests
- third-party outage affects app
- rate limits in request path

### Cached External Data

```text
Sync Job -> Local Database
User Request -> Local Database
```

Good default for most app workflows.

Benefits:

- faster reads
- stable app behavior
- better control over data model
- easier authorization and reporting

Tradeoff:

- data may be stale

### Webhook + Reconciliation

```text
Webhook -> Queue -> Processor -> Local Database
Scheduled Pull -> Compare/Repair
```

Good for:

- payment providers
- CRMs
- calendars
- fulfillment status

### Batch Pipeline

```text
File/API Extract -> Raw Storage -> Validate -> Normalize -> Merge -> Report
```

Good for:

- large feeds
- nightly imports
- partner datasets
- analytics sources

## Workflow

1. Identify the integration source and business purpose.
2. Define system of record per domain concept and field.
3. Choose integration mode.
   - API pull
   - webhook
   - batch file
   - warehouse share
   - hybrid
4. Design identity mapping.
   - local IDs
   - external IDs
   - tenant scope
   - uniqueness constraints
5. Define data model.
   - raw payload
   - normalized record
   - mapping table
   - sync metadata
   - errors/conflicts
6. Define sync behavior.
   - full sync
   - incremental sync
   - cursor/checkpoint
   - deletion handling
   - conflict resolution
7. Define safeguards.
   - validation
   - idempotency
   - retries
   - rate limits
   - DLQ/error table
   - reconciliation
8. Define security.
   - auth
   - secrets
   - webhook signatures
   - PII handling
   - tenant isolation
9. Define observability.
   - records processed
   - records failed
   - sync duration
   - sync freshness
   - API error/rate-limit counts
   - drift/reconciliation results
10. Test with duplicates, missing records, schema changes, rate limits, and partial failures.

## Output Standard

Start with:

- source system
- business purpose
- system of record decision
- integration mode
- ID mapping strategy
- local data model
- sync/freshness expectations
- safeguards
- reconciliation plan
- observability

When comparing options, include:

| Option | Benefits | Risks | When To Choose |
|---|---|---|---|

## Guardrails

- Do not integrate data before deciding system of record.
- Do not rely only on names/emails for identity mapping when stable external IDs exist.
- Do not treat webhooks as perfectly reliable.
- Do not skip reconciliation for critical external state.
- Do not let vendor payload shape leak across the whole app.
- Do not perform slow third-party calls in request path unless truly required.
- Do not store third-party secrets in code or logs.
- Do not ignore tenant boundaries in external ID mappings.
- Prefer local normalized models plus explicit external mappings for important domain tables.
