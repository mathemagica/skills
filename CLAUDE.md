# Software Architecture Judgment Library

This directory is a reusable product-development and software architecture judgment library for AI coding agents. The skills help an agent discover and test product ideas, then plan, build, review, debug, integrate, deploy, operate, and reason about software systems with durable engineering judgment.

Each skill lives in its own folder with a `SKILL.md` file containing minimal YAML frontmatter and workflow instructions. Keep `SKILL.md` frontmatter portable: use `name` and `description` for discovery, and put platform-specific invocation hints in this index or tool-specific metadata files.

## Structure

```
skills/
  playbooks/          # Meta-skills that sequence other skills for large scenarios
  software_engineering/
  data_engineering/
  distributed_systems/
  product_development/ # Idea, discovery, scope, PRD, prototype, testing, production
```

## How To Use Skills

When asked to help with an engineering task, read the relevant `SKILL.md` file(s) and follow their workflow. Prefer explicit skill invocation or playbook selection over guessing.

To use a skill, read its `SKILL.md` and apply it to the task at hand:

```
Read skills/distributed_systems/caching-patterns/SKILL.md and apply it to this design.
```

To use a playbook (which coordinates multiple skills):

```
Read skills/playbooks/new-web-app-from-scratch/SKILL.md and follow it for this product.
```

## Skill Selection Guide

| If you are... | Start with... | Add when needed... |
| --- | --- | --- |
| Taking a product idea or recorded demo to a prototype | `product_development/new-product-from-scratch/SKILL.md` | owner-reviewed discovery/scope and PRD, then appropriate implementation |
| Testing demand or usability | `product_development/product-market-testing/SKILL.md` | evidence and bounded experiments, not automatic feature work |
| Moving a prototype into real use | `product_development/prototype-to-production/SKILL.md` | release-specific safety, integrations and operations |
| Building a new web app | `playbooks/new-web-app-from-scratch/SKILL.md` | data modeling, database selection, client/server architecture, API design |
| Assessing an existing app | `playbooks/existing-system-refactoring-assessment/SKILL.md` | request tracing, separation of concerns, server organization, observability |
| Diagnosing slowness | `playbooks/system-performance-scaling-assessment/SKILL.md` | query optimization, caching, queues, sync/async processing |
| Designing an integration | `data_engineering/third-party-data-integration/SKILL.md` | idempotency, sync/async processing, queues, observability |
| Choosing storage | `data_engineering/database-selection/SKILL.md` | data modeling, query optimization, primary/secondary database architecture |
| Planning deployment | `distributed_systems/environment-management/SKILL.md` | deployment management, AWS defaults, observability |
| Reviewing architecture tradeoffs | `software_engineering/client-server-architecture/SKILL.md` | API design, CAP tradeoffs, multitenancy |

## Available Skills

### Product Development

| Skill | Path | When To Use |
|-------|------|-------------|
| new-product-from-scratch | `product_development/new-product-from-scratch/SKILL.md` | Choose the lifecycle starting point and next stage |
| product-discovery-to-scope | `product_development/product-discovery-to-scope/SKILL.md` | Interpret recordings/interviews/demos and review MVP scope |
| product-scope-to-prd | `product_development/product-scope-to-prd/SKILL.md` | Turn approved scope into owner-reviewed requirements |
| product-prototype-build | `product_development/product-prototype-build/SKILL.md` | Build and verify approved requirements on the right platform |
| product-market-testing | `product_development/product-market-testing/SKILL.md` | Test problem, usability, value, adoption or buying assumptions |
| prototype-to-production | `product_development/prototype-to-production/SKILL.md` | Assess and close real-use readiness gaps |

Read the family's [workflow contract](product_development/references/workflow-contract.md)
for evidence and approval boundaries. Keep scope and PRD reviews separate; do not
infer approval from silence. Resolve an installed skill's canonical path before
relative references. The [installation guide](product_development/README.md)
preserves sibling dependencies. BMAD is optional, installed separately only with
permission; see the [handoff guide](product_development/references/bmad-integration.md).

### Playbooks

| Skill | Path | When To Use |
|-------|------|-------------|
| new-web-app-from-scratch | `playbooks/new-web-app-from-scratch/SKILL.md` | Starting a new web app, SaaS, internal tool, or full-stack product |
| existing-system-refactoring-assessment | `playbooks/existing-system-refactoring-assessment/SKILL.md` | Assessing an existing app for cleanup, refactoring, or modernization |
| system-performance-scaling-assessment | `playbooks/system-performance-scaling-assessment/SKILL.md` | Diagnosing a slow system and creating a scaling plan |

### Software Engineering

| Skill | Path | When To Use |
|-------|------|-------------|
| separation-of-concerns | `software_engineering/separation-of-concerns/SKILL.md` | Designing or refactoring code boundaries |
| client-server-architecture | `software_engineering/client-server-architecture/SKILL.md` | Defining client/server/API boundaries |
| frontend-framework-selection | `software_engineering/frontend-framework-selection/SKILL.md` | Choosing a frontend framework and rendering model |
| backend-framework-selection | `software_engineering/backend-framework-selection/SKILL.md` | Choosing a backend framework and server architecture |
| full-stack-server-organization | `software_engineering/full-stack-server-organization/SKILL.md` | Organizing server-side code with framework conventions |
| api-design-best-practices | `software_engineering/api-design-best-practices/SKILL.md` | Designing safe, evolvable API contracts |
| frontend-debugging | `software_engineering/frontend-debugging/SKILL.md` | Debugging browser UI behavior |
| backend-debugging | `software_engineering/backend-debugging/SKILL.md` | Debugging server-side code |

### Data Engineering

| Skill | Path | When To Use |
|-------|------|-------------|
| data-modeling-first | `data_engineering/data-modeling-first/SKILL.md` | Starting from business use cases and domain entities |
| database-selection | `data_engineering/database-selection/SKILL.md` | Choosing database technology for a workload |
| query-optimization | `data_engineering/query-optimization/SKILL.md` | Diagnosing slow database-backed operations |
| primary-secondary-database-architecture | `data_engineering/primary-secondary-database-architecture/SKILL.md` | Designing read replica and primary/secondary patterns |
| third-party-data-integration | `data_engineering/third-party-data-integration/SKILL.md` | Integrating external data sources safely |

### Distributed Systems

| Skill | Path | When To Use |
|-------|------|-------------|
| request-flow-tracing | `distributed_systems/request-flow-tracing/SKILL.md` | Tracing requests end-to-end through a system |
| system-scaling-performance | `distributed_systems/system-scaling-performance/SKILL.md` | Analyzing bottlenecks and scaling limits |
| sync-async-processing | `distributed_systems/sync-async-processing/SKILL.md` | Deciding what belongs in request path vs workers |
| queue-architecture-patterns | `distributed_systems/queue-architecture-patterns/SKILL.md` | Designing queue-based workflows and retries |
| caching-patterns | `distributed_systems/caching-patterns/SKILL.md` | Designing safe caching across layers |
| idempotency-patterns | `distributed_systems/idempotency-patterns/SKILL.md` | Making retries and duplicate delivery safe |
| cap-theorem-practical-design | `distributed_systems/cap-theorem-practical-design/SKILL.md` | Applying consistency/availability tradeoffs |
| multitenancy-architecture | `distributed_systems/multitenancy-architecture/SKILL.md` | Designing tenant-aware products and data models |
| environment-management | `distributed_systems/environment-management/SKILL.md` | Managing local, staging, and production environments |
| deployment-management | `distributed_systems/deployment-management/SKILL.md` | Deploying safely with rollout and rollback |
| aws-web-app-deployment-defaults | `distributed_systems/aws-web-app-deployment-defaults/SKILL.md` | Choosing secure AWS defaults for web apps |
| observability-monitoring | `distributed_systems/observability-monitoring/SKILL.md` | Designing logs, metrics, traces, and alerts |

### Related Project

AI Tech Morning Brief is maintained separately at
[mathemagica/ai-tech-morning-brief](https://github.com/mathemagica/ai-tech-morning-brief).
It is not available as a bundled skill here. Follow that repository's migration
instructions for existing installations and schedules; do not use the old local
path or install/create duplicates.

## Skill Composition

Playbook `SKILL.md` files reference individual skills with relative links. When following a playbook step that says to read a skill, open that file and apply its workflow before continuing.

Common pairings:
- `data-modeling-first` before `database-selection`
- `client-server-architecture` before `api-design-best-practices`
- `sync-async-processing` before `queue-architecture-patterns`
- `queue-architecture-patterns` with `idempotency-patterns`
- `environment-management` before `deployment-management`
- `deployment-management` with `observability-monitoring`
