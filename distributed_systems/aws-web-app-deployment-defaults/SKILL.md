---
name: aws-web-app-deployment-defaults
description: Design, review, or implement default AWS deployment architecture for web apps using secure, scalable, observable, cost-aware patterns across DNS, CDN, TLS, load balancing, compute, databases, storage, secrets, IAM, CI/CD, monitoring, and rollback.
---

# AWS Web App Deployment Defaults

Use this skill when planning, reviewing, or implementing a default AWS deployment for a web application.

## Goal

Choose boring, secure, scalable AWS defaults that fit the app's current needs without overbuilding.

## Default Architecture

For many production web apps, start with:

```text
Route 53
  -> CloudFront
  -> AWS WAF optional
  -> ALB or API Gateway
  -> ECS/Fargate, Lambda, Elastic Beanstalk, or EC2
  -> RDS / DynamoDB / ElastiCache / S3 as needed
  -> CloudWatch / X-Ray / alarms
```

Static frontend default:

```text
Route 53 -> CloudFront -> S3 static assets
```

Full-stack/API default:

```text
Route 53 -> CloudFront -> ALB/API Gateway -> App compute -> Database/cache/storage
```

## Core Defaults

### DNS

Use Route 53 or the existing DNS provider.

Default choices:

- stable domain names per environment
- `staging.example.com` and `app.example.com`
- low-risk TTLs during migration
- clear ownership of hosted zones

### TLS

Use ACM certificates.

Default choices:

- HTTPS everywhere
- redirect HTTP to HTTPS
- certificates managed by ACM
- TLS termination at CloudFront, ALB, or API Gateway
- secure cookies when auth is browser-based

### CDN / Edge

Use CloudFront for public web apps unless there is a clear reason not to.

Use for:

- static assets
- frontend bundles
- compression
- edge caching
- TLS termination
- optional WAF integration

Be careful with:

- caching authenticated or user-specific responses
- stale deployments
- cache invalidation strategy
- forwarding headers/cookies/query params only when needed

### Compute

Choose the simplest managed compute that fits the app.

Common defaults:

- S3 + CloudFront for static sites
- ECS Fargate for containerized web apps and APIs
- Lambda + API Gateway for event-driven or low/variable traffic APIs
- Elastic Beanstalk only when the team already uses it
- EC2 only when lower-level control is truly needed

Prefer managed services over hand-managed servers for new projects.

### Load Balancing

Use ALB for container/EC2 web services.

Default choices:

- health checks
- multiple availability zones
- target groups per service
- path/host routing when needed
- no instance-local session dependency

### Database

Use managed databases.

Common defaults:

- RDS PostgreSQL for relational app data
- DynamoDB for key-value/access-pattern-first workloads
- ElastiCache Redis for cache/session/rate-limit style workloads
- S3 for large files/blobs
- OpenSearch only when search requirements justify it

Default RDS production expectations:

- private subnets
- encryption at rest
- automated backups
- point-in-time recovery
- minor version upgrade plan
- migration strategy
- connection pooling where needed

### Networking

Use a VPC with public and private subnets.

Default split:

- public subnets: load balancers, NAT gateways if needed
- private subnets: app tasks, databases, internal services
- databases not publicly accessible
- least-open security groups

Avoid:

- public RDS
- broad `0.0.0.0/0` inbound rules except public HTTP/HTTPS entrypoints
- hardcoded IP assumptions

### IAM

Use least privilege IAM.

Default choices:

- task roles or function roles
- no long-lived AWS keys in app config
- separate deploy roles from runtime roles
- narrow S3, SQS, Secrets Manager, and database permissions
- avoid `AdministratorAccess` for app runtime

### Secrets And Configuration

Use Secrets Manager or SSM Parameter Store.

Default choices:

- no secrets in source code
- no secrets in Docker images
- environment-specific config
- rotation plan for important credentials
- safe logging that never prints secrets

### CI/CD

Use a repeatable deployment pipeline.

Default expectations:

- build artifacts once
- deploy promoted artifacts between environments
- run tests before deploy
- run migrations deliberately
- support rollback
- tag images/releases
- keep staging close to production

Deployment strategies:

- rolling deploy for simple services
- blue/green or canary when downtime or regression risk is high
- CloudFront invalidation/versioned assets for frontend releases

### Observability

Use CloudWatch by default, plus X-Ray/OpenTelemetry when tracing matters.

Track:

- request rate
- error rate
- p50/p95/p99 latency
- CPU/memory
- task restarts
- ALB 4xx/5xx
- database CPU/connections/storage/replica lag
- queue depth
- cache hit rate
- deployment events

Default alarms:

- elevated 5xx
- high latency
- unhealthy targets
- task crash loops
- database storage low
- database CPU/connections high
- queue backlog
- certificate expiration where not ACM-managed

### Backups And Recovery

For production, define recovery expectations.

Include:

- database backups
- restore testing
- S3 versioning where useful
- retention policy
- RPO/RTO expectations
- disaster recovery tier appropriate to business risk

### Security

Baseline:

- HTTPS only
- private databases
- least privilege IAM
- encrypted storage
- security groups scoped tightly
- WAF for public/high-risk apps
- dependency/container scanning where available
- audit logs for sensitive admin actions
- no secrets in logs

### Cost

Use cost-aware defaults.

Watch:

- NAT Gateway costs
- CloudWatch log retention
- overprovisioned RDS
- idle load balancers
- excessive CloudFront invalidations
- data transfer between AZs/regions
- oversized ECS tasks
- unused EBS snapshots

Set:

- budgets
- log retention
- right-sized dev/staging resources
- autoscaling policies where helpful

## Workflow

1. Identify app type:
   - static frontend
   - SSR/full-stack app
   - API service
   - background worker
   - real-time/websocket app
   - internal admin app
2. Identify environments:
   - local
   - preview
   - staging
   - production
3. Choose entrypoint:
   - CloudFront
   - ALB
   - API Gateway
4. Choose compute:
   - S3/CloudFront
   - ECS Fargate
   - Lambda
   - EC2
5. Choose storage:
   - RDS
   - DynamoDB
   - S3
   - ElastiCache
   - OpenSearch
6. Design networking:
   - VPC
   - public/private subnets
   - security groups
   - NAT needs
7. Define secrets/config.
8. Define deploy pipeline and rollback.
9. Define observability and alarms.
10. Review security, backup, and cost defaults.

## Output Standard

Start with a compact architecture recommendation:

```text
Route 53 -> CloudFront -> ALB -> ECS Fargate -> RDS PostgreSQL
                         -> S3 for uploads
                         -> CloudWatch alarms/logs
```

Then include:

- why this architecture fits
- which services are required now
- which services are optional later
- security defaults
- scaling path
- deployment/rollback plan
- observability plan
- cost risks

## Guardrails

- Do not make databases public.
- Do not store secrets in code, images, or frontend bundles.
- Do not add Kubernetes/EKS unless the team has a real orchestration need.
- Do not add microservices before a monolith/service boundary is justified.
- Do not use CloudFront caching for user-specific data without strict cache keys.
- Do not skip rollback and migration planning.
- Do not optimize for theoretical scale before understanding traffic and business risk.
- Prefer managed AWS services and simple defaults for new apps.
