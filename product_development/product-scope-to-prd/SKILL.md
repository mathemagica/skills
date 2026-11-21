---
name: product-scope-to-prd
description: Convert an owner-approved product scope into concise behavioral requirements and acceptance criteria, then obtain version-specific review before building.
---

# Product Scope To PRD

Read the [workflow contract](../references/workflow-contract.md). Locate the
canonical scope, evidence and owner review. If scope approval is missing, draft
or clarify it with [product-discovery-to-scope](../product-discovery-to-scope/SKILL.md)
and pause for review. Do not treat an agent's scope recommendation as approval.

## Specify Behavior Without Expanding The Product

Reuse an existing PRD if one exists. Make the document understandable to the
vision owner and precise enough to implement:

- User/problem, intended test or outcome, approved scope version and exclusions.
- Main workflow and meaningful empty, error, cancellation and recovery states.
- Observable requirements with stable identifiers and concrete acceptance examples.
- Relevant roles, permissions, data lifecycle, accessibility and platform needs.
- Integration contracts, unavailable access and clearly marked simulations.
- Test constraints, safety boundaries, cost/latency expectations when meaningful,
  and deferred production concerns with revisit triggers.
- Open decisions, their owners and what they block.

Link requirements to discovery evidence or an explicitly approved decision. Do
not invent numerical targets, legal obligations, supported platforms, billing or
sharing features just to fill a template. Record technical recommendations as
recommendations until they change approved product behavior. Keep a tiny product's
PRD tiny; supporting architecture documents are not mandatory.

## Owner Review

Present a plain-language walkthrough and the decisions most likely to surprise
the owner, using a one-page [owner summary](../templates/prd-owner-summary.md)
alongside the full PRD. Ask for corrections and approval of the identified PRD version. A
technical feasibility question may remain open, but a blocking product decision
must be resolved or removed from the build scope. Do not start implementation
while approval is pending. When the owner changes the scope, update its decision
record before approving the corresponding PRD change.

## Handoff

Give [product-prototype-build](../product-prototype-build/SKILL.md) the approved
PRD/version, approval evidence, unresolved nonblocking assumptions, acceptance
criteria and permitted implementation environment. Confirm authorization to build;
PRD approval does not authorize account connections, spending or publication.

BMAD is optional, not required. If explicitly selected, use the
[integration guide](../references/bmad-integration.md) to keep one canonical PRD
and one approval record rather than creating a competing requirements process.
