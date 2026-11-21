---
name: new-product-from-scratch
description: Coordinate product discovery, reviewed MVP scope and requirements, prototyping, market testing and production readiness. Use for a new product idea or an existing experiment, not ordinary feature implementation.
---

# New Product From Scratch

Help a person turn a product vision into something testable without losing their
intent or mistaking a convincing demo for validated demand. This is the family
entrypoint, not a requirement to run every stage or create every document.

Read the [workflow contract](../references/workflow-contract.md) before starting.
Establish the project workspace, vision owner, current evidence, constraints,
intended users and next decision. Ask a few concrete questions at a time; do not
require technical vocabulary or restart discovery when useful work exists.

## Choose The Starting Point

| Available evidence / need | Read and use |
| --- | --- |
| Conversation, recording, diagrams, a demonstrated workflow or unclear idea | [product-discovery-to-scope](../product-discovery-to-scope/SKILL.md) |
| Reviewed scope that needs behavioral requirements | [product-scope-to-prd](../product-scope-to-prd/SKILL.md) |
| Approved requirements and permission to implement | [product-prototype-build](../product-prototype-build/SKILL.md) |
| Prototype, service concept or risky market assumption to test | [product-market-testing](../product-market-testing/SKILL.md) |
| A proposed release to real users or operational problems | [prototype-to-production](../prototype-to-production/SKILL.md) |

Choose the cheapest useful test, not necessarily software. A manual service,
clickable mockup, desktop app, agent skill or web app may fit. Do not force cloud
hosting, AI, accounts, a database or a subscription business onto the idea.
When demand uncertainty dominates, testing may precede a PRD or code. When data
or harm risk dominates, readiness work may precede any real-user trial.

## Preserve The Two Reviews

1. Present the proposed MVP scope as a plain-language user walkthrough with
   exclusions and assumptions, after a short
   [assumption check](../templates/assumption-check.md). Ask whether this is the
   right first version.
2. Present the resulting PRD, examples and unresolved decisions, with a one-page
   [owner summary](../templates/prd-owner-summary.md). Obtain approval
   of that version before implementation. Scope approval alone is not PRD approval.

Pause at each review in the discovery-to-build path; do not infer signoff from
silence or answer on the owner's behalf. For an existing approved artifact,
confirm its version and applicability rather than requiring a ceremonial repeat.
Return material changes to the owner. Implementation permission and permission
to publish, spend or connect accounts remain separate.

## Continue By Evidence

After each stage, state what is known, what remains uncertain, the current
artifact/version and approval status, and one recommended next step. Preserve
existing canonical documents. Stop, narrow or defer when that is the useful
outcome; do not automatically turn feedback into more features or production work.

## Dependencies

No BMAD dependency. The family uses sibling skills and, where applicable, the
engineering library in this checkout. Resolve the canonical skill path first
when installed through symlinks. Load only the skills relevant to the selected
stage. If a referenced skill is unavailable, disclose that and continue with a
small explicit plan rather than pretending it ran or installing it silently.
For an explicitly chosen BMAD workflow, read the
[optional integration guide](../references/bmad-integration.md).
