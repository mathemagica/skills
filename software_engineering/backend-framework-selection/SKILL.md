---
name: backend-framework-selection
description: Choose an appropriate backend framework or server architecture for a web application based on product requirements, API style, data model, team experience, language ecosystem, performance needs, deployment constraints, operational maturity, integrations, background work, and long-term maintainability.
---

# Backend Framework Selection

Use this skill when choosing a backend framework, server architecture, or backend runtime shape for a web application.

Start from the product's domain model, workflows, and operational needs, not language fashion.

## Goal

Choose a backend approach that fits the product, data model, API needs, team, deployment environment, and long-term ownership model.

## Decision Inputs

Clarify:

- product type: CRUD app, workflow system, public API, internal tool, data product, marketplace, SaaS app, integration-heavy service, real-time app, or server-rendered app
- backend responsibilities: business rules, auth, transactions, source-of-truth records, admin tooling, audit trails, background jobs, schedulers, webhooks, integrations, or reporting
- API style: server-rendered pages, REST, GraphQL, RPC, webhooks, streaming, async events, or hybrid
- data and transaction needs: relational domain model, document-heavy data, event-heavy workflows, search-heavy behavior, analytics-heavy behavior, or mixed persistence
- team expertise, hiring market, debugging comfort, testing maturity, deployment experience, and long-term ownership
- ecosystem needs: ORM, migrations, auth, authorization, validation, serialization, admin UI, background jobs, observability, testing, security, API docs, and deployment support
- runtime and deployment constraints: long-running server, containers, serverless, edge, managed platform, or on-premises

## Workflow

1. Classify the backend job.
2. Choose the backend architecture shape.
3. Match framework capabilities to data, transactions, APIs, and operations.
4. Match the backend to the frontend and API architecture.
5. Evaluate team and ecosystem fit.
6. Evaluate operational cost.
7. Recommend one primary option and one reasonable alternative.
8. Name the evidence that would change the decision.

## Backend Shape Guidance

- Use a conventional full-stack monolith or modular monolith for most new web apps.
- Use an API-first backend when multiple clients, separate frontend teams, mobile apps, or external consumers need stable contracts.
- Use a server-rendered framework when backend-owned workflows and CRUD simplicity matter more than rich client state.
- Use serverless selectively for event-driven, low-operations, spiky, or small independent functions.
- Avoid microservices until there are clear domain-boundary, scaling, deployment, compliance, or team-ownership reasons.
- Keep background workers and scheduled jobs close to the main application until their scale or ownership clearly warrants separation.

## Framework Capability Checks

Evaluate:

- routing and middleware
- ORM, query layer, and migrations
- transaction support and concurrency model
- validation and serialization
- authentication and authorization
- background jobs and scheduling
- admin interface or internal operations support
- API documentation and schema generation
- testing tools
- observability hooks
- security defaults
- deployment and runtime compatibility

## Data And Transaction Fit

Pair this skill with `$data-modeling-first` and `$database-selection`.

Prefer frameworks with strong relational modeling, migrations, and transaction support when the domain is transactional.

Prefer explicit schemas, validation, and API documentation when the backend is external-facing or integration-heavy.

Check:

- transaction boundaries
- consistency requirements
- migration safety
- concurrency behavior
- query and ORM escape hatches
- background job integration
- data access testability

## Frontend And API Fit

Pair this skill with `$frontend-framework-selection`, `$client-server-architecture`, and `$api-design-best-practices`.

Check:

- whether the backend serves pages, APIs, or both
- whether auth uses cookies, sessions, tokens, OAuth, SSO, CSRF, or CORS
- whether typed clients, generated schemas, or shared validation are important
- whether the frontend and backend should deploy together or separately
- whether a full-stack framework's coupling helps the product or limits future flexibility
- whether the framework supports the expected error, pagination, filtering, and versioning patterns

## Useful Defaults

- Many new transactional web apps: Django, Rails, Laravel, Spring Boot, ASP.NET Core, Phoenix, or a comparable batteries-included framework can be a strong default.
- Python API-first service: FastAPI is often a good fit, especially with typed request and response models.
- Python CRUD-heavy app needing admin tooling: Django is often a good fit.
- Node/TypeScript team needing structured backend conventions: NestJS is usually stronger than ad hoc Express.
- Small Node service or prototype: Express or Fastify can work, but add structure deliberately.
- Enterprise Java team: Spring Boot is a strong default.
- Microsoft/.NET team: ASP.NET Core is a strong default.
- Performance-sensitive simple services: Go can be a strong fit when team expertise exists.
- Real-time systems: Phoenix, Node, Go, or framework-specific websocket support may matter.
- Most early-stage products: prefer a modular monolith over microservices.

## Tradeoffs

- Batteries-included framework vs lightweight framework: speed and conventions versus flexibility and smaller surface area.
- Monolith vs microservices: simpler development and deployment versus independent scaling and team ownership.
- API-first vs server-rendered: client flexibility and multi-client support versus backend-owned simplicity.
- ORM vs hand-written SQL: productivity and consistency versus query control.
- Dynamic language vs statically typed language: speed of iteration versus compile-time guarantees and refactoring safety.
- Serverless vs long-running server: lower operations and burst handling versus cold starts, runtime limits, and local development complexity.
- Full-stack framework vs separate backend/frontend: integration speed versus coupling.

## Operational Checks

Before finalizing, consider:

- deployment complexity
- database migration safety
- logging, metrics, tracing, and health checks
- worker and scheduler management
- secrets and environment configuration
- local development experience
- test speed and reliability
- security patch cadence
- framework upgrade cadence and dependency risk

## Expected Output

When invoked, produce:

1. Backend responsibility profile
2. Backend architecture shape recommendation
3. Backend framework recommendation
4. Data and transaction fit
5. Frontend/API integration model
6. Operational implications
7. Risks and tradeoffs
8. Reasonable alternative
9. Decision summary

