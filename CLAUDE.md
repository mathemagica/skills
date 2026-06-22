# Skills Library

This directory is a library of reusable engineering skills. Each skill lives in its own folder with a `SKILL.md` file containing YAML frontmatter and workflow instructions.

## Structure

```
skills/
  playbooks/          # Meta-skills that sequence other skills for large scenarios
  software_engineering/
  data_engineering/
  distributed_systems/
```

## How To Use Skills

When asked to help with an engineering task, read the relevant `SKILL.md` file(s) and follow their workflow. Prefer explicit skill invocation over guessing.

To use a skill, read its `SKILL.md` and apply it to the task at hand:

```
Read skills/distributed_systems/caching-patterns/SKILL.md and apply it to this design.
```

To use a playbook (which coordinates multiple skills):

```
Read skills/playbooks/new-web-app-from-scratch/SKILL.md and follow it for this product.
```

## Available Skills

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

## Skill Composition

Playbook `SKILL.md` files reference individual skills with relative links. When following a playbook step that says to read a skill, open that file and apply its workflow before continuing.

Common pairings:
- `data-modeling-first` before `database-selection`
- `client-server-architecture` before `api-design-best-practices`
- `sync-async-processing` before `queue-architecture-patterns`
- `queue-architecture-patterns` with `idempotency-patterns`
- `environment-management` before `deployment-management`
- `deployment-management` with `observability-monitoring`
