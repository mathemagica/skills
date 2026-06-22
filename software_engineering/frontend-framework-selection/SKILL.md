---
name: frontend-framework-selection
description: Choose an appropriate frontend framework or rendering approach for a web application based on product requirements, interactivity, routing, data fetching, rendering model, team experience, ecosystem maturity, deployment constraints, performance, accessibility, and long-term maintainability.
when_to_use: Use when starting a new web app, dashboard, internal tool, marketing site, SaaS app, admin UI, customer portal, or when deciding between React, Next.js, Vue, Nuxt, Svelte, SvelteKit, Angular, Remix, Astro, HTMX, server-rendered templates, a single-page app, or another frontend approach.
argument-hint: "[web-app-or-frontend-decision]"
---

# Frontend Framework Selection

Use this skill when choosing a frontend framework, rendering model, or client-side architecture for a web application.

Start from the product's interaction model, not framework popularity.

## Goal

Choose a frontend approach that fits the product, backend architecture, team, deployment environment, and long-term maintenance needs.

## Decision Inputs

Clarify:

- product type: content site, CRUD app, dashboard, internal tool, SaaS app, portal, marketplace, e-commerce, collaboration app, or custom interactive tool
- interaction model: simple forms, complex workflows, data visualization, real-time updates, offline support, drag/drop, rich editing, or mostly reading content
- rendering needs: static generation, server-side rendering, server-rendered templates, client-side rendering, streaming, islands, progressive enhancement, or hybrid rendering
- SEO and sharing requirements
- authentication and authorization shape
- data fetching, cache, and mutation patterns
- backend relationship: monolith, API-first backend, backend-for-frontend, GraphQL, REST, RPC, or full-stack framework
- team expertise, hiring market, testing comfort, and maintenance capacity
- deployment constraints: edge, serverless, containers, CDN, static hosting, long-running server, or platform-specific runtime
- accessibility, internationalization, design system, and component library needs

## Workflow

1. Classify the product and interaction model.
2. Choose the rendering shape.
3. Match the framework to the backend architecture.
4. Evaluate team and ecosystem fit.
5. Evaluate operational cost.
6. Recommend one primary option and one reasonable alternative.
7. Name the evidence that would change the decision.

## Rendering Shape Guidance

- Use server-rendered templates or HTMX-style progressive enhancement for simple CRUD apps where the backend owns most behavior and rich client state is not central.
- Use static generation or islands architecture for content-heavy sites with limited interactivity.
- Use full-stack SSR frameworks such as Next.js, Remix, Nuxt, or SvelteKit for apps needing routing, auth, data loading, SEO, and rich interaction.
- Use a client-heavy SPA when the app behaves more like a desktop application and SEO or first-load constraints are manageable.
- Use an enterprise-structured framework such as Angular when the team values strong conventions, integrated tooling, and consistency across many contributors.
- Use the team's existing framework when it is adequate; switching ecosystems should solve a real product, operational, or maintainability problem.

## Backend Architecture Fit

Pair this skill with `$client-server-architecture`.

Check:

- whether the frontend framework expects server runtime, static hosting, or both
- whether API clients, generated types, schemas, or shared validation are easy to maintain
- how authentication cookies, sessions, tokens, CSRF, and CORS work in the chosen shape
- how server-rendered data, client cache, optimistic updates, and invalidation are handled
- whether the deployment platform supports the framework's SSR, streaming, server components, edge runtime, or build output
- whether the framework makes the desired client/server boundary clearer or more confusing

## Useful Defaults

- Standard SaaS app with rich UI and React experience: consider Next.js or Remix.
- Internal CRUD tool where backend simplicity matters most: consider server-rendered templates with progressive enhancement.
- Content-heavy site: consider Astro, Next.js static/SSR, Nuxt, or another content-friendly framework.
- Highly interactive browser app: consider React, Vue, Svelte, or Angular with an architecture suited to the team.
- Enterprise app with many contributors and a need for strong conventions: Angular can be a strong fit.
- Smaller team valuing simplicity and compiler-driven ergonomics: SvelteKit can be a strong fit.
- Team already strong in Vue: Vue or Nuxt are usually better than switching ecosystems without a clear reason.

## Tradeoffs

- SPA vs SSR: client flexibility and rich local interaction versus first load, SEO, server complexity, and hydration failure modes.
- Full-stack framework vs separate frontend/backend: integrated productivity versus deployment and runtime coupling.
- Popular ecosystem vs smaller ecosystem: hiring and library depth versus simplicity and lower conceptual overhead.
- Server-rendered templates vs client-heavy UI: simpler backend-owned workflows versus richer client interaction.
- Framework convention vs flexibility: speed and consistency versus architectural control.
- Static hosting vs server runtime: operational simplicity versus dynamic rendering and request-time personalization.

## Operational Checks

Before finalizing, consider:

- build pipeline complexity
- bundle size and performance budgets
- SSR and hydration failure modes
- cache behavior and invalidation
- error reporting and frontend observability
- testing strategy
- accessibility tooling
- dependency churn and upgrade cadence
- local development experience

## Expected Output

When invoked, produce:

1. Product interaction profile
2. Rendering model recommendation
3. Frontend framework recommendation
4. Backend integration model
5. Operational implications
6. Risks and tradeoffs
7. Reasonable alternative
8. Decision summary

