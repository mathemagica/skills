---
name: multitenancy-architecture
description: Design, evaluate, or review multitenant application architecture, including tenant isolation models, shared vs dedicated infrastructure, data modeling, authorization, onboarding, billing, observability, security, compliance, operational costs, and product/business tradeoffs.
when_to_use: Use when building SaaS, B2B, enterprise, white-label, partner, marketplace, agency, internal platform, or multi-customer systems where one application serves multiple organizations, accounts, customers, workspaces, or environments.
argument-hint: "[product-or-system]"
---

# Multitenancy Architecture

Use this skill when deciding whether and how an application should support multiple tenants.

## Core Idea

A tenant is a customer, organization, workspace, account, partner, environment, or other business boundary that expects its data, configuration, permissions, billing, and operational experience to be separated from others.

Multitenancy means one product or platform serves multiple tenants through shared application code and often shared infrastructure, while preserving the right isolation boundaries.

## When To Consider Multitenancy

Consider multitenancy when:

- the product is SaaS or B2B
- users belong to organizations or workspaces
- customers need separate data, permissions, configuration, branding, or billing
- one deployment should serve many customers
- onboarding a new customer should be mostly self-service or operationally cheap
- support/admin teams need tenant-aware tooling
- tenants may have different plans, limits, integrations, or compliance needs
- enterprise customers may ask for dedicated environments later

Do not assume multitenancy is only a database concern. It affects product design, support, billing, analytics, operations, security, and go-to-market.

## Why It Matters To Product And Business

Multitenancy determines:

- how customers are onboarded
- how pricing and billing are modeled
- how permissions work
- how support investigates issues
- how customer data is exported or deleted
- how features are rolled out by plan or tenant
- how custom configuration is supported
- how compliance promises are made
- how noisy-neighbor risks are handled
- how enterprise customers can receive stronger isolation
- how much it costs to operate each customer

A weak tenant model often becomes expensive later because every feature must retrofit tenant boundaries.

## Tenant Isolation Models

### Shared Everything

All tenants share the same application, database, and infrastructure. Tenant identity is represented in data, often with `tenant_id`.

Good fit:

- early-stage SaaS
- many small tenants
- low per-tenant customization
- strong need for operational simplicity

Benefits:

- lowest operational overhead
- easy fleet-wide deployments
- efficient resource usage
- simple onboarding

Risks:

- data leakage bugs are high impact
- noisy neighbors
- harder enterprise isolation story
- queries must consistently filter by tenant
- tenant-specific restore/export/delete can be harder

### Shared App, Separate Database Or Schema

Tenants share application code but have separate databases or schemas.

Good fit:

- medium/large tenants
- stronger isolation needs
- per-tenant backup/restore requirements
- regional or compliance boundaries
- customer-specific migration windows

Benefits:

- stronger data isolation
- easier tenant-level backup/restore
- easier noisy-neighbor isolation
- clearer enterprise posture

Risks:

- higher operational complexity
- migrations across many tenants
- connection management
- cross-tenant analytics harder
- onboarding/provisioning more complex

### Dedicated Stack Per Tenant

Each tenant has a dedicated deployment, database, and infrastructure.

Good fit:

- large enterprise customers
- strict compliance/security isolation
- custom SLAs
- data residency needs
- highly customized deployments

Benefits:

- strongest isolation
- custom scaling and maintenance windows
- clearer blast-radius control
- easier contractual guarantees

Risks:

- high cost per tenant
- operational sprawl
- slower upgrades
- fragmented observability
- harder product consistency

### Hybrid Model

Most tenants use shared infrastructure; high-value or regulated tenants use dedicated resources.

Good fit:

- SaaS products moving upmarket
- mixed SMB/enterprise customer base
- tiered plans
- compliance-driven segmentation

Benefits:

- balances cost and isolation
- supports enterprise growth path
- avoids overbuilding for all tenants

Risks:

- multiple operating models
- feature behavior can drift
- more complex support and deployment playbooks

## Data Modeling

Tenant identity should be explicit.

Common patterns:

- `tenant_id` on tenant-owned tables
- tenant-scoped unique constraints
- tenant-aware foreign keys where supported
- membership table: users belong to tenants with roles
- tenant settings/configuration table
- tenant plan/limits table
- audit logs scoped by tenant
- data retention/deletion metadata

Example:

```text
Tenant 1--* Membership *--1 User
Tenant 1--* Project
Project 1--* Task
Tenant 1--* IntegrationConfig
Tenant 1--* AuditEvent
```

Tenant-scoped uniqueness:

```text
UNIQUE(tenant_id, slug)
UNIQUE(tenant_id, external_id)
```

Avoid global uniqueness unless the business requires it.

## Authorization And Security

Every tenant-aware access path needs authorization.

Check:

- user belongs to tenant
- user role permits the action
- resource belongs to tenant
- integration credential belongs to tenant
- background job carries tenant context
- admin/support access is audited
- API keys are tenant-scoped
- cache keys include tenant context
- search/vector indexes enforce tenant filtering
- object storage paths and signed URLs are tenant-aware

Common bug:

- route checks that the user is logged in but forgets to verify the resource belongs to the active tenant.

## Product Design Impacts

Multitenancy affects UX:

- tenant switcher
- invitations and membership
- roles and permissions
- workspace settings
- billing owner
- usage limits
- tenant-specific integrations
- branding/custom domains
- audit logs
- data export/delete
- admin/support impersonation
- feature flags by tenant or plan

Decide early:

- Can a user belong to multiple tenants?
- Can resources move between tenants?
- Is there a personal workspace?
- Who owns billing?
- Who can invite users?
- What happens when a tenant is suspended or deleted?

## Operational Impacts

Plan for:

- tenant onboarding/provisioning
- migrations
- backups and restores
- tenant-level exports
- tenant-level deletion
- tenant-specific incident response
- rate limits and quotas
- noisy-neighbor detection
- per-tenant observability
- support tooling
- customer-specific configuration
- feature rollout and rollback by tenant

## Business Tradeoffs

Shared tenancy lowers cost and accelerates onboarding, but increases the importance of correct isolation and observability.

Dedicated tenancy improves enterprise sales and isolation, but increases cost, complexity, and support burden.

Hybrid tenancy gives commercial flexibility, but requires discipline to avoid maintaining several products in disguise.

Questions for business/product:

- What is the expected tenant count?
- What is the expected tenant size distribution?
- Are customers SMB, mid-market, enterprise, internal teams, or partners?
- Do customers require data residency or dedicated environments?
- Is tenant-level billing required?
- Are tenant-level SLAs promised?
- Is per-tenant customization part of the business model?
- How expensive can onboarding be?
- How expensive can offboarding be?

## Workflow

1. Define what a tenant means for this product.
2. Identify tenant-facing product workflows.
   - signup/onboarding
   - invitations
   - switching tenants
   - permissions
   - billing
   - integrations
   - exports/deletion
3. Identify isolation requirements.
   - data
   - compute
   - network
   - secrets
   - observability
   - compliance
4. Choose tenancy model.
   - shared everything
   - shared app/separate schema
   - shared app/separate database
   - dedicated stack
   - hybrid
5. Model tenant data.
   - tenant entity
   - user membership
   - tenant-owned resources
   - tenant-scoped uniqueness
   - tenant settings
   - audit events
6. Design authorization.
   - resource ownership checks
   - tenant context propagation
   - API key scoping
   - admin/support access
7. Design operational controls.
   - quotas
   - rate limits
   - backup/restore
   - observability
   - tenant-level incident handling
8. Identify product/business consequences.
   - pricing
   - plans
   - enterprise commitments
   - onboarding cost
   - support cost
   - customization policy
9. Document risks and migration paths.

## Output Standard

Start with:

- definition of tenant
- recommended tenancy model
- why it fits the business/product
- isolation guarantees
- data model implications
- authorization requirements
- operational costs
- future migration path

When comparing options, include:

| Model | Benefits | Costs/Risks | Best Fit |
|---|---|---|---|

## Guardrails

- Do not treat tenant isolation as only a frontend filter.
- Do not add `tenant_id` without enforcing it in authorization, queries, caches, jobs, and integrations.
- Do not use global admin/support access without audit logs.
- Do not cache tenant-specific data without tenant-scoped cache keys.
- Do not put multiple tenants in one search/vector index without enforceable tenant filters.
- Do not promise dedicated isolation on shared infrastructure without clear boundaries.
- Do not choose dedicated stacks for every tenant unless the business can absorb the operational cost.
- Prefer the simplest tenancy model that supports the business commitments and security requirements.
