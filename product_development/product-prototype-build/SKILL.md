---
name: product-prototype-build
description: Implement and verify a small product prototype from approved requirements, choosing the appropriate platform and exposing shortcuts before user testing. Not production release authorization.
---

# Product Prototype Build

Read the [workflow contract](../references/workflow-contract.md). Confirm the
approved PRD version, authorization to implement, workspace and constraints.
Without approval, use [product-scope-to-prd](../product-scope-to-prd/SKILL.md) and
pause. Inspect existing code and preserve unrelated changes before modifying it.

## Choose The Smallest Honest Implementation

Determine whether the agreed test needs a web app, desktop app, mobile interface,
CLI, agent skill, mockup or manually delivered service. Use native platform
conventions and proven domain libraries. Do not silently substitute a web app
for local files, offline operation or desktop integration requirements.

For a web implementation, use the maturity-aware
[new-web-app-from-scratch](../../playbooks/new-web-app-from-scratch/SKILL.md)
engineering branch. Select other library skills only when relevant, such as
[data modeling](../../data_engineering/data-modeling-first/SKILL.md),
[integrations](../../data_engineering/third-party-data-integration/SKILL.md) or
[idempotency](../../distributed_systems/idempotency-patterns/SKILL.md).
Do not require every engineering skill or a particular cloud provider.

Build one end-to-end path before broadening coverage. Keep mocks and synthetic
data visibly distinct from working integrations. Track shortcuts and what they
prevent the experiment from proving. If access is unavailable, agree a simulation
or report the blocker; never imply a mock proves a live integration works.

## Verify Against The Approved Behavior

Map acceptance requirements to actual checks and results. Run focused automated
tests and inspect the real interface or output where applicable. Cover relevant
failure/recovery paths, not just the happy-path screenshot. Report checks not run,
environment limits and deviations. Never claim a prototype is production-ready
because a build or unit test passed.

Return material product changes for owner review before implementing them.
Technical implementation choices within approved behavior do not require a
fresh product approval at every step. Enforce authorization and other critical
boundaries in software, not solely in prompts or instructions.

## Handoff

Provide the runnable artifact, startup instructions, verified behavior, known
limitations, mocks, rough operating costs if measured and the next useful test.
Include a short [demo script](../templates/demo-script.md) the owner can use to
show the prototype, limited to behavior that was actually verified.
Do not publish, spend, connect private accounts or recruit users without separate
authorization. Use [product-market-testing](../product-market-testing/SKILL.md)
to prepare learning, and [prototype-to-production](../prototype-to-production/SKILL.md)
before a real-use release when its risk requires readiness work. These stages
may interleave; do not expose sensitive data merely to accelerate testing.
