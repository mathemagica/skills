---
name: client-server-architecture
description: Design new systems or system components using standard client-server architecture patterns, including clear client/server responsibilities, API boundaries, data flow, authentication, state ownership, error handling, caching, and deployment/runtime concerns.
when_to_use: Use when creating a new application, service, feature, API, frontend/backend boundary, integration, or system component that needs a clear client-server architecture.
argument-hint: "[system-or-component]"
---

# Client Server Architecture

Use this skill when designing or implementing a new system or component that has a client, server, API, service, or runtime boundary.

## When To Use

- A new app, service, API, frontend feature, backend module, or integration is being created.
- A system needs a clear split between client-side and server-side responsibilities.
- A component needs API contracts, request/response flows, auth boundaries, or persistence boundaries.
- A frontend needs to coordinate with backend capabilities.
- A backend needs to expose data or behavior safely to one or more clients.
- A system design needs to account for caching, latency, offline behavior, retries, or deployment shape.

## Goal

Design a client-server boundary that is explicit, testable, secure, and aligned with the product workflow and existing codebase conventions.

## Core Responsibility Split

Prefer this default split unless the local architecture gives a stronger pattern:

- Client owns presentation, local interaction state, input collection, optimistic UI, accessibility, and user feedback.
- Server owns trusted business rules, authorization, persistence, durable workflows, secrets, external service credentials, and cross-user consistency.
- API owns the contract between client and server: resource shape, command semantics, validation errors, status codes, pagination, filtering, and compatibility.
- Shared schemas or generated clients may own type consistency, but not business authority unless the project already uses that pattern.

## Workflow

1. Identify the user workflow and the system boundary.
2. Classify each responsibility:
   - presentation
   - client interaction state
   - server business logic
   - persistence
   - authorization
   - validation
   - external integrations
   - background work
   - observability
   - deployment or runtime ownership
3. Choose the interaction model:
   - request/response REST API
   - RPC-style command API
   - GraphQL query or mutation boundary
   - server-rendered pages
   - streaming or websocket updates
   - event-driven or background workflow
4. Define the API contract:
   - endpoint or operation name
   - request shape
   - response shape
   - validation failures
   - auth requirements
   - pagination, filtering, and sorting behavior when relevant
   - idempotency and retry behavior when relevant
5. Decide state ownership:
   - transient UI state stays on the client
   - canonical domain state lives on the server
   - cached server state is invalidated or refreshed deliberately
   - optimistic updates include rollback behavior
6. Design failure behavior:
   - network failure
   - validation failure
   - authorization failure
   - not found or stale resource
   - partial success
   - server or dependency failure
7. Account for non-functional concerns:
   - latency and request count
   - caching and cache invalidation
   - rate limits
   - security and secret handling
   - auditability
   - observability
   - schema or version compatibility
8. Implement using existing project conventions.
9. Add tests at the right boundary:
   - client component or interaction tests
   - API contract tests
   - server unit or service tests
   - integration tests for critical flows
10. Report the chosen boundary, contract, state ownership, and verification.

## Output Standard

- Start with a compact architecture sketch.
- Name what belongs on the client, server, and API boundary.
- Include a request/response or operation contract for new APIs.
- Call out security-sensitive decisions.
- Prefer the smallest architecture that can support the expected workflow.
- Identify follow-up decisions only when they block safe implementation.

## Guardrails

- Do not put secrets, durable authorization, or trusted business rules in the client.
- Do not create an API endpoint before naming the workflow it supports.
- Do not over-split into services unless scale, ownership, deployment, or reliability requires it.
- Do not invent a protocol if the existing codebase already has a standard.
- Do not duplicate validation rules without deciding which layer is authoritative.
- Do not rely on client-only checks for data integrity or access control.
- Preserve existing architecture conventions unless the task explicitly asks for redesign.
