---
name: environment-management
description: Design, manage, review, or debug software deployment environments such as local, staging, production, preview, QA, pre-production, sandbox, and disaster recovery; define the simplest starting setup, when to add environments, promotion flow, environment-specific config, data, access, testing, release gates, and operational tradeoffs.
when_to_use: Use when planning or reviewing deployment environments, deciding how many environments a web app needs, managing environment-specific config, deciding whether staging/pre-production/QA/preview environments are needed, debugging environment-specific bugs, or explaining how production-like environments should work.
argument-hint: "[system-or-release-process]"
---

# Environment Management

Use this skill when designing or managing the environments a system moves through from development to production.

## Core Idea

An environment is a running instance or context of a system with its own configuration, infrastructure, data, credentials, access rules, and operational expectations.

Good environment management helps teams:

- test safely before production
- catch integration and configuration problems
- control releases
- separate real customer data from test data
- reduce production risk
- debug environment-specific issues
- support demos, QA, previews, and enterprise validation

## Simplest Good Starting Point For A Standard Web App

For most small or early web apps, start with:

```text
Local -> Staging -> Production
```

### Local

For fast development and debugging on a developer machine.

Use:

- local app server
- local or shared dev database
- fake/sandbox external services
- fast unit and integration tests

### Staging

For final checks before production.

Use:

- same deployment process as production
- same app/runtime shape as production where practical
- separate staging database
- sandbox credentials for payments/email/third-party APIs
- production-like config names
- smoke tests after deploy

### Production

For real users and real data.

Use:

- real credentials
- strict access controls
- backups
- monitoring and alerts
- rollback plan
- incident response expectations

This simple setup is enough when:

- the team is small
- release frequency is manageable
- there are no formal QA gates
- there are no enterprise acceptance requirements
- production risk is moderate
- staging can stay stable enough to be trusted

Do not start with many environments unless there is a real workflow, compliance, or scale reason. Every environment adds cost, configuration, data management, access control, and drift risk.

## When To Add More Environments

Add environments when a real pain or risk appears.

### Add Preview / Ephemeral Environments When

- UI/product review needs deployed branches
- PRs need isolated acceptance testing
- multiple features are being reviewed at once
- staging is blocked by in-progress work
- designers, PMs, QA, or customers need branch-specific demos

### Add Shared Dev When

- developers need an always-on integration target
- local setup is expensive or incomplete
- multiple services need to talk before staging
- unstable work should not pollute staging

### Add QA / Test When

- QA needs a dedicated place for regression passes
- automated end-to-end tests need isolation
- staging is reserved for release candidates
- test data needs repeatable reset/seed flows

### Add Pre-Production When

- staging is used for ongoing QA and is too noisy for final release gates
- release candidates need a quiet, production-like validation target
- enterprise customers require acceptance testing
- load/performance testing would disrupt staging
- production-like migrations need rehearsal
- regulated workflows need signoff evidence
- blue/green or canary rollout needs an isolated validation target
- production data snapshots require stricter controls than staging

### Add Sandbox When

- external developers, partners, or customers need to test integrations
- public APIs need a safe testing environment
- demos and training should not touch production data

### Add Disaster Recovery When

- business continuity requires defined recovery
- RPO/RTO commitments exist
- downtime or data loss has significant business impact

## Common Environments

### Local

Runs on a developer machine.

Used for:

- fast development
- unit tests
- local debugging
- isolated experimentation

Tradeoffs:

- often least production-like
- may use fake services or local containers
- fast feedback matters more than perfect fidelity

### Development / Dev

Shared or personal environment for in-progress work.

Used for:

- early integration
- unstable feature testing
- developer collaboration
- quick deployed checks

Tradeoffs:

- may be noisy or broken
- should not gate production quality by itself
- often uses synthetic or disposable data

### Preview / Ephemeral

Temporary environment created per branch, PR, or feature.

Used for:

- reviewing UI changes
- testing isolated feature branches
- stakeholder feedback
- automated acceptance checks

Tradeoffs:

- cost and cleanup must be managed
- data should be seeded or synthetic
- third-party integrations may need sandbox credentials

### QA / Test

Environment dedicated to manual or automated test passes.

Used for:

- regression testing
- exploratory QA
- automated end-to-end suites
- release validation

Tradeoffs:

- can become stale or artificial
- needs test data management
- may not match production scale

### Staging

A stable, production-like environment used before production release.

Used for:

- final integration testing
- smoke testing
- release candidate validation
- migration rehearsal
- environment/config verification
- production-like deployment testing

Staging should be similar to production in:

- infrastructure shape
- app configuration
- deployed artifact
- database engine/version
- key integrations, using sandbox credentials where needed
- observability and logging

Staging does not need to match production in:

- full scale
- full data volume
- production secrets
- live customer traffic

### Pre-Production

A very production-like environment used when staging is not enough.

Use pre-production when:

- regulated or enterprise workflows need formal validation
- staging is shared/noisy and cannot be a release gate
- migrations require realistic rehearsals
- performance/load testing needs production-like topology
- customer acceptance testing needs a stable environment
- blue/green or release-candidate validation requires isolation
- production data snapshots are used under controlled policies

Tradeoffs:

- higher cost
- more operational overhead
- stricter access and data controls
- risk of becoming a second production

### Production

The live customer-facing environment.

Used for:

- real users
- real data
- real billing
- real operational commitments
- monitored SLAs/SLOs

Production requires:

- strict access controls
- backup and recovery
- monitoring and alerts
- rollback strategy
- audit logging
- change control
- incident response

### Sandbox

Safe environment for customers, partners, or integrations.

Used for:

- API testing
- partner development
- demos
- integration validation
- training

Tradeoffs:

- must be clearly separate from production
- may need realistic but fake data
- API behavior should match production where possible

### Disaster Recovery / DR

Environment or capability for recovering from major failure.

Used for:

- regional failover
- backup restore
- business continuity

Tradeoffs:

- cost depends on warm/hot/cold standby model
- must be tested, not just documented

## Environment-Specific Config Values

Each environment needs its own configuration values.

Examples:

- database URL
- API base URL
- OAuth redirect URI
- email provider credentials
- payment provider mode
- object storage bucket
- CDN domain
- logging level
- feature flags
- rate limits
- allowed origins/CORS
- cookie domain
- secret keys
- third-party webhook URLs
- queue names
- environment name

Good practices:

- keep config names consistent across environments
- store secrets in a secrets manager, not code
- keep non-secret config in versioned config or infrastructure code where possible
- validate required config at startup
- fail fast when critical config is missing
- document intentional differences between environments
- use sandbox credentials outside production
- make environment visible in logs, metrics, and UI admin surfaces
- avoid manual console-only config changes
- keep config changes reviewable
- do not let staging accidentally point at production services

Bad examples:

- `STAGING_DATABASE_URL` in staging but `DB_CONN` in production
- staging using production Stripe keys
- dev sending real customer emails
- preview environments sharing one mutable production-like secret
- feature flag defaults differing silently between staging and production

Environment-specific config is normal. Hidden config drift is the danger.

## Workflow

1. Start with the simplest environment set that supports the release risk.
   - Usually `local -> staging -> production` for standard web apps.
2. Identify system risk and release needs.
   - Who uses production?
   - What happens if a release fails?
   - Are there compliance, enterprise, or customer validation needs?
3. Define required environments.
   - local
   - staging
   - production
   - preview/dev/QA/pre-production/sandbox/DR only when justified
4. Assign purpose to each environment.
   - development
   - automated tests
   - manual QA
   - release validation
   - performance testing
   - customer acceptance
   - integration sandbox
   - live traffic
5. Define promotion flow.
   - source branch
   - build artifact
   - preview/dev if used
   - staging
   - pre-production if needed
   - production
6. Decide artifact policy.
   - build once, promote the same artifact
   - avoid rebuilding separately for production
   - tag versions/releases
   - track deploy provenance
7. Define configuration and secrets.
   - environment-specific variables
   - secrets manager paths
   - sandbox vs production credentials
   - feature flags
   - safe defaults
   - startup validation
8. Define data policy.
   - synthetic data
   - seeded fixtures
   - anonymized production snapshots
   - production data restrictions
   - reset/refresh process
   - retention
9. Define access controls.
   - who can deploy
   - who can view logs
   - who can access databases
   - who can use customer data
   - who can approve production changes
10. Define release gates.
   - tests
   - migrations
   - smoke checks
   - security checks
   - manual approval
   - monitoring after deploy
11. Define observability.
   - logs
   - metrics
   - traces
   - alerts
   - dashboards
   - environment labels
12. Define drift management.
   - infrastructure as code
   - config comparison
   - dependency/version tracking
   - scheduled review
   - automated checks where possible

## Staging vs Pre-Production

Staging:

- production-like
- shared release validation
- often used continuously by engineering/QA
- may contain synthetic or seeded data
- may be somewhat smaller than production

Pre-production:

- closer to production topology and controls
- quieter and release-candidate focused
- may use sanitized production-like data
- often has stricter access
- used as final release gate or formal validation

## Data Management

Data policy matters as much as infrastructure.

Questions:

- Can lower environments use production data?
- Must data be anonymized?
- How is test data seeded?
- How are environments reset?
- How do migrations get rehearsed?
- How are long-lived test accounts managed?
- Are emails/payments/webhooks disabled or sandboxed?

Guardrails:

- do not send real emails from staging unless intentional
- do not charge real payments outside production
- do not trigger real customer webhooks from test environments
- do not expose production data in low-trust environments
- label non-production data clearly

## Release Promotion

Prefer:

```text
Build once -> test artifact -> deploy same artifact to staging -> promote same artifact to production
```

This reduces "worked in staging, failed in production because it was a different build."

Track:

- commit SHA
- build ID
- artifact/image tag
- migration version
- deployment time
- approver
- rollback target

## Environment Drift

Drift happens when environments differ unintentionally.

Common causes:

- manual console changes
- missing config variables
- different dependency versions
- different database versions
- stale seed data
- disabled integrations
- different IAM/security group rules
- different feature flags

Detect with:

- infrastructure as code
- config diffing
- smoke tests
- deployment checks
- scheduled environment audits
- startup config validation

## Output Standard

Start with:

- recommended environment set
- simplest starting point
- purpose of each environment
- when to add more environments
- promotion flow
- data policy
- config/secrets policy
- access controls
- release gates
- when pre-production is or is not justified

When comparing environments, include:

| Environment | Purpose | Data | Access | Production Similarity | Release Role |
|---|---|---|---|---|---|

## Guardrails

- Do not start with many environments without a real need.
- Do not let staging become an untrusted dumping ground if it is a production release gate.
- Do not use production secrets in lower environments.
- Do not use real customer data without policy, anonymization, and access controls.
- Do not rebuild artifacts separately for production if promotion is feasible.
- Do not add environments without owning their cost, data, access, and drift.
- Do not assume passing in dev means production is safe.
- Do not let environment-specific config become hidden, inconsistent, or manually managed drift.
- Prefer fewer well-managed environments over many neglected ones.
