---
name: full-stack-server-organization
description: Design, write, review, or refactor server-side code in full-stack web frameworks using MVC, MVW, MTV, CRUD/resource APIs, service layers, repositories, serializers, validators, middleware, and framework-native organization patterns.
when_to_use: Use when creating or reorganizing server code in Rails, Django, Laravel, Spring, ASP.NET, Express, FastAPI, Flask, Phoenix, NestJS, or similar full-stack/backend web frameworks.
argument-hint: "[framework-or-feature-or-module]"
---

# Full Stack Server Organization

Use this skill when designing, writing, reviewing, or refactoring server-side web framework code so routes, controllers, views/templates, models, services, persistence, validation, and API contracts stay organized.

## When To Use

- A new web feature needs server-side structure.
- A backend module is becoming hard to navigate.
- Route handlers, controllers, models, views, serializers, or templates are taking on too many responsibilities.
- CRUD endpoints need a consistent resource shape.
- A project uses MVC, MVW, MTV, resource controllers, service objects, repositories, middleware, or serializers.
- Business logic is leaking into controllers, templates, models, or ORM callbacks.
- Server-side rendering and JSON APIs need to coexist cleanly.
- A framework offers strong conventions, but the codebase is drifting away from them.

## Goal

Keep server-side code organized around the framework's native architecture while making responsibility boundaries explicit, testable, and durable.

## Pattern Vocabulary

Use the project's framework vocabulary first:

- MVC: model owns domain/persistence behavior, view owns presentation, controller coordinates request handling.
- MTV: model owns data/domain behavior, template owns presentation, view function/class coordinates request handling.
- MVW: "model-view-whatever" patterns vary by framework; identify what the local "whatever" layer actually owns.
- CRUD/resource API: expose resources through consistent create, read, update, delete, list, filter, and pagination operations.
- Service layer: owns business workflows that do not belong in controllers, models, templates, or serializers.
- Repository/data access layer: isolates query or persistence details when the framework or codebase benefits from it.
- Serializer/schema layer: owns request/response shape, transformation, and validation when the framework supports it.
- Middleware/filter/interceptor: owns cross-cutting request behavior such as auth, sessions, logging, metrics, CORS, or request context.

## Default Responsibility Split

Prefer the local framework's conventions unless there is a clear reason to introduce a new layer.

- Routes map URLs or operations to handlers.
- Controllers/views/handlers coordinate request lifecycle, auth checks, parameter parsing, service calls, and response selection.
- Models/entities own domain invariants and persistence-adjacent behavior, but should not become broad workflow coordinators.
- Services/use cases own multi-step business workflows and interactions across models, external APIs, or background jobs.
- Repositories/query objects own complex data access when queries become reusable, hard to test, or too large for handlers/models.
- Serializers/schemas/forms own input validation, output shape, and framework-native error formatting.
- Templates/views own presentation only.
- Middleware owns request-wide concerns, not feature-specific business logic.
- Jobs/tasks own asynchronous execution, retries, and background side effects.

## Workflow

1. Identify the framework and its native organization style.
2. Read nearby feature code before proposing structure.
3. Name the server-side workflow:
   - request path or operation
   - authenticated actor
   - target resource
   - business action
   - response type: HTML, JSON, redirect, stream, file, or background job
4. Classify responsibilities:
   - routing
   - request parsing
   - authentication and authorization
   - validation
   - orchestration
   - domain rules
   - persistence/querying
   - serialization
   - presentation/template rendering
   - background work
   - observability
5. Choose the organizing pattern:
   - simple framework-native handler/controller for narrow behavior
   - resource controller or CRUD endpoint for standard resource operations
   - service/use-case object for multi-step workflows
   - query object/repository for complex data access
   - serializer/schema/form object for input/output shape
   - middleware/filter/interceptor for cross-cutting request behavior
6. Define the contract:
   - route or endpoint
   - request params/body
   - success response
   - validation errors
   - auth/permission behavior
   - not-found/stale-resource behavior
   - side effects and background jobs
7. Implement or refactor in small steps.
8. Keep tests at the right layer:
   - route/controller/request tests for HTTP behavior
   - service/use-case tests for business workflows
   - model/entity tests for invariants
   - serializer/schema/form tests for shape and validation
   - integration tests for critical end-to-end flows
9. Report where each responsibility lives and what was verified.

## CRUD/API Guidance

For CRUD/resource APIs:

- Use resource names and HTTP verbs consistently when the framework supports REST conventions.
- Keep list endpoints explicit about filtering, sorting, pagination, and default ordering.
- Keep create/update validation errors structured and predictable.
- Treat delete semantics deliberately: hard delete, soft delete, archive, deactivate, or detach.
- Use idempotency for retry-prone create/update operations when duplicate side effects matter.
- Avoid hiding business workflows behind misleading CRUD names; use action-specific endpoints or service methods when the operation is not really CRUD.

## Server-Side Rendering Guidance

For HTML/template features:

- Keep templates focused on rendering, not querying or business decisions.
- Prepare view models, context objects, or presenter data before rendering when pages become complex.
- Keep redirects, flash messages, and form errors consistent with local framework conventions.
- Avoid duplicating business rules between HTML forms and JSON APIs.

## Guardrails

- Do not add a service/repository layer just because a pattern exists.
- Do not move simple framework-native code into abstractions that make it harder to read.
- Do not put secrets, authorization, or trusted business rules in templates or client-side code.
- Do not bury business workflows in ORM callbacks unless the project already relies on that pattern and the behavior is truly model-local.
- Do not duplicate validation across controller, serializer, model, and client without naming the authoritative layer.
- Prefer framework conventions over generic architecture advice.
- Preserve existing public routes, API contracts, and behavior unless the user explicitly asks for redesign.
