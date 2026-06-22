---
name: separation-of-concerns
description: Design, write, review, or refactor code so responsibilities such as routing, validation, business logic, persistence, formatting, configuration, observability, and external integrations stay separated behind the smallest useful boundaries.
when_to_use: Use when designing new code, writing a feature, reviewing existing code, or refactoring code where responsibilities may be mixed across routing, validation, business logic, persistence, formatting, configuration, observability, or external integrations.
argument-hint: "[feature-or-file-or-module]"
---

# Separation Of Concerns

Use this skill when designing, writing, reviewing, or refactoring code whose responsibilities should evolve independently.

## When To Use

- A new feature needs a clear responsibility split before implementation.
- A new module, route, command, component, job, or service needs boundaries that will stay testable.
- A route, controller, component, command, job, or service does too much.
- Business rules are embedded in UI, API, CLI, database, or integration code.
- Validation, orchestration, persistence, formatting, and side effects are interleaved.
- Tests need broad setup for narrow behavior.
- The same rule appears in multiple layers.
- A bug fix requires touching unrelated responsibilities.

## Goal

Design or separate responsibilities at the smallest useful boundary while preserving behavior and following the codebase's existing architecture.

## Workflow

1. Read the target code, requirements, and nearby examples before proposing structure.
2. Decide whether the task is primarily:
   - new-code design
   - existing-code review
   - behavior-preserving refactor
   - mixed implementation and cleanup
3. List the responsibilities involved. Use categories such as:
   - boundary or transport handling
   - validation
   - domain or business rules
   - orchestration
   - persistence
   - external integration
   - presentation or serialization
   - configuration
   - observability
4. Identify which responsibilities change for different reasons.
5. For new code, sketch the smallest useful shape before implementation. Prefer existing local patterns such as:
   - route or controller delegates workflow to a service
   - service owns orchestration and business rules
   - repository or client owns persistence or external API details
   - schema or validator owns input constraints
   - serializer or formatter owns output shape
   - adapter owns vendor-specific translation
6. For existing code, look for concrete symptoms:
   - mixed abstraction levels
   - duplicated rules
   - hidden side effects
   - hard-to-mock dependencies
   - circular imports
   - overly broad tests
   - framework code owning domain decisions
7. Implement or refactor incrementally. Add a boundary only when the destination has a clearer responsibility.
8. Add or adjust focused tests around the separated behavior.
9. Report the responsibility map, what boundary was chosen, where behavior lives, and what was verified.

## Output Standard

- Start with a short responsibility map for design or review work.
- Name the boundary problem in concrete code terms.
- Recommend or implement a minimal design or refactor, not an architecture rewrite.
- Include tests or verification proportional to the risk.
- Distinguish direct observations from architectural suggestions.

## Guardrails

- Do not split tiny cohesive functions.
- Do not add layers just to satisfy a pattern.
- Do not introduce abstract interfaces unless there are multiple implementations, a real test seam, or a clear volatility boundary.
- Do not rename or move broad surfaces unless the task requires it.
- Preserve public behavior unless the user explicitly asks for a redesign.
- Prefer project-local conventions over generic clean-architecture advice.
