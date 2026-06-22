---
name: deployment-management
description: Plan, review, or debug deployment management for applications, including release promotion, build artifacts, environment variables, secrets, config, migrations, rollout strategies, rollback, CI/CD pipelines, deployment verification, monitoring, and production change safety.
when_to_use: Use when deploying an application, designing CI/CD, managing environment variables or secrets, planning release promotion, debugging deployment failures, coordinating database migrations, choosing rollout/rollback strategy, or reviewing production deployment safety.
argument-hint: "[app-or-release]"
---

# Deployment Management

Use this skill when planning, executing, reviewing, or debugging how application changes move safely into running environments.

## Relationship To Environment Management

Use `environment-management` to decide what environments exist and what each is for.

Use this skill to decide how code, config, secrets, migrations, and infrastructure changes are deployed into those environments.

## Core Idea

A deployment is a controlled change to a running system.

Deployments may include:

- application code
- container images
- static assets
- environment variables
- secrets references
- database migrations
- infrastructure changes
- feature flags
- background workers
- scheduled jobs
- queue consumers
- CDN invalidations
- config changes

Good deployment management makes changes repeatable, observable, reversible, and safe.

## Simple Starting Point For New Web Apps

For most new web apps, start with this flow:

```text
main branch
  -> CI tests
  -> build immutable artifact
  -> deploy same artifact to staging
  -> run smoke tests
  -> promote same artifact to production
  -> monitor production
  -> rollback if needed
```

Good defaults:

- build once, promote the same artifact
- keep staging and production deploy processes similar
- use tagged container images or immutable build artifacts
- store secrets outside source code
- validate required config at startup
- run migrations deliberately
- smoke test after deploy
- have a rollback path
- record what version is deployed where

Avoid:

- building one artifact for staging and a different one for production
- changing production config manually without review
- deploying code and secret/config changes with no coordination
- running migrations without rollback/compatibility thought
- assuming deploy success means app health

## Build Artifacts

A build artifact is what gets deployed.

Examples:

- container image
- static frontend bundle
- serverless package
- compiled binary
- wheel/gem/npm package
- infrastructure plan

Best practices:

- build once
- tag with commit SHA and release version
- scan/test before promotion
- store in artifact registry
- deploy the same artifact across environments
- keep provenance: who built it, from which commit, when

## Environment Variables And Config

Environment variables are runtime configuration values.

Examples:

- `APP_ENV`
- `DATABASE_URL`
- `API_BASE_URL`
- `REDIS_URL`
- `LOG_LEVEL`
- `FEATURE_X_ENABLED`
- `ALLOWED_ORIGINS`
- `COOKIE_DOMAIN`
- `QUEUE_NAME`
- `S3_BUCKET`
- `OAUTH_REDIRECT_URI`

Best practices:

- keep variable names consistent across environments
- treat environment variables as config, not code
- validate required variables at startup
- fail fast on missing critical config
- document intentional environment differences
- keep non-secret config reviewable, preferably in infrastructure or deployment code
- avoid one-off console edits
- show deployed config version or checksum where useful
- make environment name visible in logs/metrics

Pitfalls:

- staging points to production services
- production points to sandbox services
- mismatched variable names across envs
- feature flags differ silently
- runtime config changes bypass deployment review
- config is changed but app processes are not restarted/reloaded

## Secrets

Secrets are sensitive values used by the app.

Examples:

- database passwords
- API keys
- OAuth client secrets
- signing keys
- encryption keys
- webhook signing secrets
- private certificates
- payment provider secrets

Best practices:

- store secrets in a secrets manager
- never commit secrets to source code
- never bake secrets into Docker images or frontend bundles
- do not print secrets in logs
- scope secrets per environment
- restrict secret access by runtime role
- rotate important secrets
- support dual-read or staged rotation when needed
- separate deploy permission from secret-read permission where possible
- use sandbox secrets outside production

Pitfalls:

- leaking secrets through build logs
- exposing secrets to frontend code
- reusing production secrets in staging
- long-lived personal credentials in CI
- broad secret access for every service
- breaking deploys by rotating secrets without app support

## Config vs Secret

Use this distinction:

- Config: non-sensitive value that changes behavior.
- Secret: sensitive value that grants access or trust.

Examples:

- `S3_BUCKET=my-app-prod-uploads`: config
- `AWS_SECRET_ACCESS_KEY=...`: secret
- `STRIPE_MODE=live`: config
- `STRIPE_SECRET_KEY=...`: secret

Both need management. Secrets need stronger storage, access control, logging discipline, and rotation.

## Deployment Strategies

### Rolling Deploy

Replace instances gradually.

Good for:

- most stateless web services
- simple container services

Tradeoffs:

- old and new versions run together
- migrations must be backward compatible
- rollback may still need data compatibility

### Blue/Green Deploy

Run old and new environments side by side, then switch traffic.

Good for:

- lower downtime
- quick rollback
- high-risk releases

Tradeoffs:

- more infrastructure cost
- data/migration coordination
- traffic cutover complexity

### Canary Deploy

Send a small percentage of traffic to the new version first.

Good for:

- risk reduction
- measuring real production behavior

Tradeoffs:

- requires metrics and routing support
- can be complex with stateful changes

### Feature Flags

Deploy code separately from enabling behavior.

Good for:

- gradual rollout
- tenant/user-specific rollout
- quick disable
- testing in production safely

Tradeoffs:

- flag lifecycle management
- hidden code paths
- config drift
- combinatorial testing

## Database Migrations

Migrations are often the riskiest part of deployment.

Best practices:

- make schema changes backward compatible when possible
- use expand/contract pattern
- deploy code that tolerates old and new schema during rolling deploys
- avoid long locks on large tables
- test migrations on staging-like data
- have a rollback or forward-fix plan
- separate irreversible data migrations from routine deploy when needed
- monitor migration duration and errors

Expand/contract example:

```text
1. Add nullable new column.
2. Deploy code that writes old and new column.
3. Backfill data.
4. Deploy code that reads new column.
5. Remove old column later.
```

Avoid:

- dropping columns used by old code during rolling deploy
- renaming columns without compatibility layer
- long blocking migrations during peak traffic
- assuming database rollback is as easy as code rollback

## Workers, Queues, And Scheduled Jobs

Deploying async components needs care.

Check:

- are old and new workers compatible with queued messages?
- did message schema change?
- are scheduled jobs duplicated during deployment?
- are workers paused during migrations if needed?
- can failed jobs be retried safely?
- are idempotency keys preserved?

Best practices:

- version message schemas
- keep consumers backward compatible
- drain or pause queues only when necessary
- monitor queue depth and DLQs
- deploy workers deliberately when message handling changes

## Static Assets And CDN

For frontend/static assets:

Best practices:

- fingerprint filenames
- cache immutable assets long-term
- serve HTML with shorter/no cache if it references latest assets
- invalidate CDN only when necessary
- avoid deleting old assets immediately if old HTML may reference them
- verify asset URLs after deploy

Pitfalls:

- stale HTML references missing JS files
- CDN serves old app shell
- service worker caches old bundle
- environment-specific frontend config baked into wrong bundle

## Deployment Verification

A deploy is not complete when the command exits. Verify behavior.

Checks:

- health endpoint
- smoke test critical flows
- app logs
- error rate
- latency
- background worker health
- queue depth
- database migration status
- external integration sanity
- CDN/static asset availability

Production post-deploy monitoring:

- watch for 5xx
- watch p95/p99 latency
- watch frontend errors
- watch job failures
- watch database connections/CPU
- watch business metrics where relevant

## Rollback

Have a rollback strategy before deploying.

Rollback can mean:

- redeploy previous artifact
- disable feature flag
- revert config
- fail traffic back to blue environment
- pause worker
- run forward-fix migration
- restore data only in severe cases

Know:

- what is safe to roll back
- whether migrations are backward compatible
- whether queued messages changed
- whether external side effects already happened
- who can approve rollback
- how to communicate incident status

## Workflow

1. Identify deployment scope.
   - code
   - config
   - secrets
   - database
   - infrastructure
   - workers/jobs
   - static assets/CDN
2. Identify target environment.
3. Confirm artifact and version.
4. Confirm config and secrets.
   - required variables present
   - environment-specific values correct
   - secrets accessible by runtime role
   - no secrets exposed to client/build logs
5. Plan migration steps.
6. Choose rollout strategy.
7. Define verification checks.
8. Define rollback/forward-fix path.
9. Deploy.
10. Monitor.
11. Record outcome.

## Output Standard

Start with:

- deployment scope
- target environment
- artifact/version
- config/secrets changes
- migration risk
- rollout strategy
- verification plan
- rollback plan

When reviewing a deployment plan, include:

| Area | Check | Risk | Action |
|---|---|---|---|

## Guardrails

- Do not deploy without knowing what artifact/version is being deployed.
- Do not store secrets in code, images, frontend bundles, or logs.
- Do not make unreviewed production config changes.
- Do not assume staging passed if production uses a different build artifact.
- Do not run risky migrations without compatibility and rollback/forward-fix plan.
- Do not deploy worker/message schema changes without queue compatibility review.
- Do not treat deploy completion as health verification.
- Prefer repeatable deployment pipelines over manual console changes.
