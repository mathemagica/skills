---
name: api-design-best-practices
description: Design, review, or refactor APIs using clear resource/operation boundaries, request and response contracts, HTTP semantics, validation, authentication, authorization, pagination, filtering, idempotency, versioning, error handling, documentation, testing, and backward compatibility.
when_to_use: Use when creating a new API, changing an existing API contract, designing REST/RPC/GraphQL endpoints, reviewing backend routes, defining client-server contracts, or diagnosing API usability, consistency, compatibility, or security issues.
argument-hint: "[api-or-endpoint-or-feature]"
---

# API Design Best Practices

Use this skill when designing, reviewing, or changing an API contract.

## First Principle

An API is a contract between systems.

Design it around the product workflow, domain model, client needs, security requirements, and long-term compatibility, not just the easiest server function to expose.

## When To Use

- A new endpoint, route, resolver, RPC method, or webhook is being created.
- A frontend and backend need a clear contract.
- An API response shape is changing.
- A public or partner API needs stability.
- An internal API is becoming hard to use or inconsistent.
- API errors, pagination, filtering, auth, or idempotency need standardization.
- A backend route exposes implementation details instead of domain concepts.

## Goal

Create an API that is clear, safe, consistent, testable, evolvable, and pleasant for clients to use.

## API Style Selection

Choose the style that fits the system and existing conventions.

### REST / Resource-Oriented HTTP

Good fit:

- CRUD/resource APIs
- web and mobile clients
- standard HTTP caching/status semantics
- public APIs

Common pattern:

```text
GET    /projects
POST   /projects
GET    /projects/{project_id}
PATCH  /projects/{project_id}
DELETE /projects/{project_id}
```

### RPC / Command APIs

Good fit:

- action-oriented workflows
- internal services
- operations that are not naturally CRUD
- explicit commands

Example:

```text
POST /orders/{order_id}:cancel
POST /invoices/{invoice_id}:send
```

### GraphQL

Good fit:

- clients need flexible selection
- many related resources
- multiple frontend consumers with different data needs

Tradeoffs:

- harder HTTP caching
- authorization and N+1 risks
- schema governance needed

### Webhooks / Event APIs

Good fit:

- notifying external systems
- async lifecycle events
- integrations

Need:

- event IDs
- signing
- replay handling
- idempotent consumers
- versioned payloads

## Workflow

1. Identify the product workflow.
   - Who calls the API?
   - What user/business action does it support?
   - Is it interactive, batch, integration, or background use?
2. Identify the domain concept.
   - resource
   - command
   - event
   - query
   - aggregate
3. Choose API style.
   - REST/resource
   - RPC/command
   - GraphQL
   - webhook/event
4. Define request contract.
   - path
   - method
   - headers
   - query params
   - body shape
   - auth requirements
   - idempotency key when needed
5. Define response contract.
   - success status
   - response body
   - error status codes
   - validation error shape
   - pagination metadata
   - links/cursors when relevant
6. Define authorization.
   - who can call it
   - resource ownership checks
   - tenant boundaries
   - role/scope requirements
7. Define consistency and side effects.
   - read-after-write behavior
   - async job behavior
   - retries
   - idempotency
   - emitted events
8. Define compatibility.
   - what fields are required
   - what fields are optional
   - deprecation/migration path
   - versioning strategy
9. Add tests and documentation.

## HTTP Semantics

Use HTTP deliberately.

Common defaults:

- `GET`: retrieve data, no side effects
- `POST`: create resource or submit command
- `PUT`: replace full resource or idempotent upsert
- `PATCH`: partial update
- `DELETE`: delete, archive, deactivate, or detach explicitly

Status codes:

- `200 OK`: successful read/update with body
- `201 Created`: resource created
- `202 Accepted`: async work accepted
- `204 No Content`: success with no body
- `400 Bad Request`: malformed request
- `401 Unauthorized`: missing/invalid authentication
- `403 Forbidden`: authenticated but not allowed
- `404 Not Found`: resource absent or intentionally hidden
- `409 Conflict`: state/version/idempotency conflict
- `422 Unprocessable Entity`: validation failed where used by convention
- `429 Too Many Requests`: rate limited
- `500+`: server/dependency failure

Avoid:

- using `GET` for mutations
- returning `200` for errors
- leaking authorization details in `404`/`403` inconsistently
- inventing unusual status codes without local convention

## Resource And Operation Design

Use stable domain names, not implementation names.

Prefer:

```text
/projects/{project_id}/tasks
```

Over:

```text
/getTasksForProjectDatabaseQuery
```

For non-CRUD actions, name the command clearly:

```text
POST /orders/{order_id}:cancel
POST /reports/{report_id}:run
POST /uploads/{upload_id}:complete
```

Do not hide complex business workflows behind misleading CRUD endpoints.

## Request Design

Good request contracts:

- accept only fields the client may set
- validate types, required fields, ranges, and enum values
- distinguish omitted fields from explicit null where relevant
- avoid server-controlled fields in client input
- support idempotency keys for retry-prone operations
- keep payloads bounded
- avoid exposing internal IDs unless they are stable API concepts

## Response Design

Good response contracts:

- return stable field names
- include IDs needed for follow-up actions
- omit secrets and internal-only fields
- use predictable date/time formats
- distinguish empty list from null
- represent state explicitly
- include pagination metadata for lists
- avoid response shapes that change based on hidden server state

## Pagination, Filtering, Sorting

For list endpoints, define:

- pagination style: cursor, keyset, offset
- default page size
- max page size
- default ordering
- allowed filters
- allowed sort fields
- behavior for invalid filters
- total count availability, if any

Prefer cursor/keyset pagination for large or changing datasets.

## Error Design

Errors should help clients recover.

Include:

- machine-readable code
- human-readable message
- field-level validation details when relevant
- request/correlation ID when useful
- retryability when useful

Example:

```json
{
  "error": {
    "code": "validation_failed",
    "message": "One or more fields are invalid.",
    "fields": {
      "email": "Must be a valid email address."
    }
  }
}
```

Do not expose:

- stack traces
- secrets
- raw SQL
- internal service credentials
- sensitive auth details

## Authentication And Authorization

Authenticate the caller and authorize the action.

Check:

- identity
- tenant/workspace
- role/scope
- resource ownership
- row/object-level permissions
- admin/support access auditability

Never rely on frontend-only authorization.

## Idempotency And Retries

Use idempotency for operations that may be retried.

Especially:

- payments
- checkout
- order creation
- external API calls
- imports
- uploads
- background job creation

Patterns:

- idempotency key header
- unique business constraint
- command table
- request hash
- replay original response
- reject same key with different payload

## Versioning And Compatibility

Prefer backward-compatible changes:

Safe:

- add optional response fields
- add optional request fields
- add new endpoints
- add enum values only if clients tolerate unknowns

Risky:

- remove fields
- rename fields
- change types
- change semantics
- make optional fields required
- change default ordering
- change error shape

Version when compatibility cannot be preserved.

Strategies:

- URL version: `/v1/...`
- header version
- schema version in event/webhook payload
- feature negotiation

## Documentation

Document:

- purpose
- auth
- request
- response
- errors
- pagination
- filtering
- rate limits
- idempotency
- examples
- compatibility notes

Prefer OpenAPI/JSON Schema/GraphQL schema where the project uses them.

## Testing

Test:

- success path
- validation errors
- auth failures
- permission boundaries
- not found
- conflict/state errors
- idempotency/retry behavior
- pagination/filtering/sorting
- backward compatibility
- generated client/schema validity when relevant

## Output Standard

Start with:

- API purpose
- recommended style
- route/operation
- request shape
- response shape
- auth requirements
- error behavior
- compatibility notes

When reviewing, identify:

- contract ambiguity
- security risks
- compatibility risks
- client usability issues
- missing tests/docs

## Guardrails

- Do not expose server internals as API design.
- Do not rely on frontend validation for correctness or authorization.
- Do not change response contracts without compatibility review.
- Do not add pagination/filtering casually without defining behavior.
- Do not make retry-prone mutations non-idempotent.
- Do not leak secrets, stack traces, or raw implementation errors.
- Prefer consistency with existing API conventions over generic purity.
