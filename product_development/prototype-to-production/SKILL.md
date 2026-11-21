---
name: prototype-to-production
description: Assess and close the gaps between a working prototype and a defined real-use environment, including data safety, integrations, recovery, operating costs and ownership. Not a blanket production certification.
---

# Prototype To Production

Read the [workflow contract](../references/workflow-contract.md). Define the
specific release: users, data sensitivity, deployment environment, expected use,
critical workflows, acceptable failure and operator. Inspect actual code,
configuration, tests and runtime evidence; a PRD alone cannot establish readiness.
Market evidence informs investment, but cannot waive necessary user protections.

## Assess Relevant Gaps

Rank each finding by evidence, consequence, proposed mitigation, effort and owner.
Separate release blockers, accepted limitations and later work. Evaluate only
relevant concerns, explaining why significant areas are not applicable:

- Authentication and server-enforced authorization, including tenant boundaries.
- Data retention, deletion, secrets, consent and sensitive information in logs.
- Backups and tested restoration, migrations, import/export and data ownership.
- Real integration access, permissions, rate limits, retries, idempotency,
  reconciliation and behavior during provider failure.
- Deployment verification, rollback, dependency/security checks and monitoring.
- Critical task usability, accessibility, failure recovery and support routes.
- Measured resource/vendor costs, usage limits and workable operating budgets.
- Who releases, responds to incidents, maintains integrations and pays the bills.

For AI products, include applicable evaluation evidence, source handling,
prompt-injection boundaries, tool permissions, approval enforcement and fallback.
A prompt is not an access-control mechanism. Do not invent regulatory compliance
or certify security; identify where specialized assessment is needed.

## Reuse Engineering Skills Selectively

Use [deployment-management](../../distributed_systems/deployment-management/SKILL.md),
[observability-monitoring](../../distributed_systems/observability-monitoring/SKILL.md),
[third-party-data-integration](../../data_engineering/third-party-data-integration/SKILL.md)
and other relevant skills as needed. Use
[system-performance-scaling-assessment](../../playbooks/system-performance-scaling-assessment/SKILL.md)
only for evidenced or concrete forecast capacity constraints. Five users may need
strong data controls without distributed infrastructure; usage alone does not
justify caches, queues, replicas or multiple regions.

## Close And Verify

Agree bounded remediation before changing the system. Recheck mitigations using
tests or runtime evidence, including restore/rollback exercises where relevant
and authorized. Record unresolved risks and the owner's explicit release decision
for the particular environment. Business risk acceptance cannot waive required
permissions or mandatory protections. Deployment, spending and private-system
access require their own authorization.

Deliver a release-specific readiness record, verification results, remaining
limitations and a short operator handoff. If critical evidence is missing, state
not ready or readiness unknown and the next check; do not replace evidence with
an optimistic readiness score or a promise of production reliability.
