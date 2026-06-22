# Skills

## What These Skills Are For

This repository is a reusable engineering skill library for AI coding agents such as Codex and Claude Code. The skills give an agent durable, task-specific engineering judgment it can apply while planning, building, reviewing, debugging, integrating, deploying, or operating software systems.

Each skill is a small, portable instruction package built around a `SKILL.md` file, with optional platform metadata in files such as `agents/openai.yaml`. A skill tells the agent when to use a pattern, what questions to ask, what tradeoffs to consider, what evidence to gather, and what kind of output to produce. Playbooks combine multiple skills into larger workflows, such as building a new web app, assessing an existing system for refactoring, or diagnosing performance bottlenecks.

These skills are not application code, templates, or rigid checklists. They are reusable engineering guidance for recurring software decisions: how to separate concerns, choose frameworks and databases, design APIs, model data, reason about caching and queues, manage environments and deployments, instrument systems, and evaluate architecture before changing it.

Use them when you want an agent to work more like a senior engineering collaborator: grounding recommendations in the codebase, naming tradeoffs, choosing simple defaults, sequencing work, and producing plans or code changes that can be reviewed.

## Contents

### Playbooks

- `new-web-app-from-scratch`: coordinate the skills library to plan and build a new web application from product concept through data model, architecture, APIs, deployment, and observability.
- `existing-system-refactoring-assessment`: coordinate the skills library to assess an existing application for cleanup, refactoring, modernization, rearchitecture, and operational risk before recommending changes.
- `system-performance-scaling-assessment`: coordinate the skills library to diagnose slow systems, identify bottlenecks with evidence, and create a practical scaling plan.

### Software Engineering

- `separation-of-concerns`: design or refactor code so responsibilities stay clear.
- `client-server-architecture`: define client/server/API boundaries for new systems.
- `frontend-framework-selection`: choose a frontend framework and rendering model based on product needs, backend fit, team experience, ecosystem, deployment, and maintainability.
- `backend-framework-selection`: choose a backend framework and server architecture based on product workflows, data model, API style, team experience, ecosystem, deployment, operations, and maintainability.
- `full-stack-server-organization`: organize server-side web framework code around MVC, MTV, CRUD APIs, services, serializers, and framework conventions.
- `api-design-best-practices`: design safe, evolvable API contracts.
- `frontend-debugging`: debug browser UI behavior with DevTools, runtime state, network, DOM, CSS, and framework tooling.
- `backend-debugging`: debug server-side code with one-variable experiments, logs, traces, tests, and debuggers.

### Data Engineering

- `data-modeling-first`: start new projects from business use cases, user interactions, entities, relationships, states, and access patterns.
- `database-selection`: choose database technology based on workload, data shape, correctness, and operational needs.
- `query-optimization`: diagnose slow database-backed operations across database types.
- `primary-secondary-database-architecture`: design safe database read replica and primary/secondary patterns.
- `third-party-data-integration`: integrate external data with source-of-record ownership, external ID mapping, reconciliation, and safeguards.

### Distributed Systems

- `request-flow-tracing`: trace web requests from browser through DNS, CDN, load balancer, app servers, databases, and back.
- `system-scaling-performance`: analyze CPU, memory, I/O, database, and request-rate bottlenecks.
- `sync-async-processing`: decide what belongs in the request path versus workers, schedulers, or queues.
- `queue-architecture-patterns`: design queue-based workflows, workers, retries, DLQs, and backpressure.
- `caching-patterns`: design safe caching across browser, CDN, app, distributed cache, database, read model, search, and pipeline layers.
- `idempotency-patterns`: make retries, duplicate delivery, and partial failure safe.
- `cap-theorem-practical-design`: apply consistency, availability, and partition-tolerance tradeoffs per workflow.
- `multitenancy-architecture`: design tenant-aware product, data, auth, and operational boundaries.
- `environment-management`: choose and manage local, staging, production, preview, QA, pre-production, sandbox, and DR environments.
- `deployment-management`: deploy safely with artifacts, config, secrets, migrations, rollout, verification, and rollback.
- `aws-web-app-deployment-defaults`: choose secure, scalable AWS defaults for web apps.
- `observability-monitoring`: design useful logs, metrics, traces, dashboards, health checks, and alerts.

## How To Use These Skills

Use skills by naming them explicitly in your prompt, usually with `$skill-name`.

Use playbooks when you want the agent to select and sequence multiple skills for a larger engineering scenario.

Example:

```text
Use $data-modeling-first and $client-server-architecture to plan this new web app before writing code.
```

```text
Use $new-web-app-from-scratch with the skills library at /Users/annlewis/projects/skills to plan this product before implementation.
```

```text
Use $existing-system-refactoring-assessment with the skills library at /Users/annlewis/projects/skills to assess this application before refactoring.
```

```text
Use $system-performance-scaling-assessment with the skills library at /Users/annlewis/projects/skills to diagnose why this system is slow and create a scaling plan.
```

You can combine skills when the task spans multiple layers. Prefer starting with the smallest set that matches the decision you are making.

## Scenario Guides

### Building A New Web App From Scratch

Start with product and data shape before code:

1. `$data-modeling-first`: identify business concepts, user interactions, entities, relationships, lifecycle states, and access patterns.
2. `$database-selection`: choose the primary datastore and any secondary indexes or stores.
3. `$frontend-framework-selection`: choose the frontend framework and rendering model.
4. `$backend-framework-selection`: choose the backend framework and server architecture.
5. `$client-server-architecture`: decide what belongs on the client, server, API boundary, and durable storage.
6. `$api-design-best-practices`: define endpoint contracts, auth, errors, pagination, idempotency, and compatibility.
7. `$full-stack-server-organization`: organize server routes, controllers/views, models, services, serializers, validators, and jobs.
8. `$environment-management`: start with `Local -> Staging -> Production`, then add other environments only when justified.
9. `$deployment-management`: define artifact promotion, env vars, secrets, migrations, verification, and rollback.
10. `$observability-monitoring`: add minimum useful logs, metrics, health checks, deploy markers, and alerts.
11. `$aws-web-app-deployment-defaults`: if deploying on AWS, choose default DNS, CDN, TLS, compute, database, IAM, secrets, and monitoring.

Common follow-ons:

- Use `$sync-async-processing` when deciding what stays in the request path.
- Use `$queue-architecture-patterns` for background jobs or burst smoothing.
- Use `$caching-patterns` only after the read/write pattern and source of truth are clear.
- Use `$idempotency-patterns` for any retry-prone create, payment, import, webhook, or job flow.

### Rearchitecting An Existing System

First understand the current system, then change the smallest useful boundary:

1. `$request-flow-tracing`: map how requests move through browser, edge, load balancers, services, caches, queues, and databases.
2. `$separation-of-concerns`: identify mixed responsibilities in code and propose clearer boundaries.
3. `$system-scaling-performance`: determine whether the system is CPU, memory, I/O, database, network, or queue-bound.
4. `$query-optimization`: investigate slow database-backed paths before adding replicas, caches, or queues.
5. `$caching-patterns`, `$queue-architecture-patterns`, or `$primary-secondary-database-architecture`: add scaling components only when they target the measured bottleneck.
6. `$cap-theorem-practical-design`: name the consistency/availability tradeoff introduced by caches, queues, replicas, or regions.
7. `$deployment-management` and `$observability-monitoring`: make the new architecture deployable, observable, and reversible.

For SaaS or B2B systems, add:

- `$multitenancy-architecture`: tenant model, isolation, authorization, billing, support, and operational tradeoffs.

### Considering A System Integration Issue

Use this path when integrating with a vendor, SaaS tool, partner API, payment provider, CRM, calendar, warehouse, or data feed:

1. `$third-party-data-integration`: decide system of record, integration mode, external ID mapping, raw vs normalized data, reconciliation, safeguards, and observability.
2. `$idempotency-patterns`: make webhook, import, retry, and sync behavior duplicate-safe.
3. `$sync-async-processing`: decide whether calls happen in the request path, worker, scheduler, or queue.
4. `$queue-architecture-patterns`: add queues for rate limits, retries, burst smoothing, or delayed processing.
5. `$api-design-best-practices`: define internal or external API contracts.
6. `$observability-monitoring`: track freshness, failures, retries, sync duration, and reconciliation drift.

Useful rule: decide the system of record before designing the sync. Most integration trouble starts when two systems silently believe they own the same field.

### Assessing A System For Refactoring Or Cleanup

Use this path when the system feels hard to change, debug, or operate:

For a full assessment, start with `$existing-system-refactoring-assessment`. Use the individual skills below when you already know the area you want to inspect.

1. `$request-flow-tracing`: map the actual runtime path and system components.
2. `$backend-debugging` or `$frontend-debugging`: reproduce current failures with runtime evidence.
3. `$separation-of-concerns`: identify tangled responsibilities and the smallest boundary worth introducing.
4. `$full-stack-server-organization`: clean up server code using framework-native conventions.
5. `$api-design-best-practices`: review API consistency, compatibility, errors, auth, and pagination.
6. `$data-modeling-first`: revisit domain entities, relationships, states, constraints, and source-of-truth records.
7. `$query-optimization`: find query and access-pattern problems before changing storage or architecture.
8. `$observability-monitoring`: add signals so future cleanup work is guided by evidence.

## Using With Codex

In Codex, these skills can be invoked by name when they are installed or available in the active skill search path.

Use explicit prompts like:

```text
Use $api-design-best-practices to review this endpoint contract.
```

```text
Use $system-scaling-performance and $query-optimization to diagnose this slow dashboard.
```

If the skills are not installed globally, point Codex at this repository or the specific `SKILL.md` file:

```text
Use the skill in /Users/annlewis/projects/skills/distributed_systems/caching-patterns/SKILL.md to review this caching plan.
```

Each skill also has `agents/openai.yaml` metadata for OpenAI/Codex-facing display names, descriptions, and default prompts.

## Using With Claude Code

Claude Code can use skills that follow the `SKILL.md` format with YAML frontmatter. These skills include Claude-friendly metadata such as:

- `name`
- `description`
- `when_to_use`
- `argument-hint`

To use them with Claude Code, copy or symlink skill folders into a Claude skills directory, such as:

```text
~/.claude/skills/
```

or a project-local directory such as:

```text
.claude/skills/
```

Then invoke them explicitly:

```text
Use $deployment-management to plan this release.
```

```text
Use $third-party-data-integration to design the HubSpot sync.
```

Claude can also discover skills by their `description` and `when_to_use` metadata, but explicit invocation is best when you want a specific workflow.

## Skill Composition

Some skills are conceptual companions:

- `data-modeling-first` before `database-selection`
- `frontend-framework-selection` before `client-server-architecture`
- `backend-framework-selection` before `client-server-architecture`
- `client-server-architecture` before `api-design-best-practices`
- `sync-async-processing` before `queue-architecture-patterns`
- `queue-architecture-patterns` with `idempotency-patterns`
- `caching-patterns` with `cap-theorem-practical-design`
- `environment-management` before `deployment-management`
- `deployment-management` with `observability-monitoring`
- `third-party-data-integration` with `idempotency-patterns`

When in doubt, start with the skill that defines ownership and boundaries. Most durable engineering decisions start there.
