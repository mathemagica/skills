# Harness Engineering

Harness engineering is the practice of making a software project legible,
operable, and correctable by coding agents and humans working together.

OpenAI described this pattern in
[Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/).
That article focuses on Codex, but the paradigm is platform independent. The
same ideas apply to Codex, Claude Code, other coding agents, human engineers,
and mixed teams: put durable project knowledge where the worker can find it,
encode recurring judgment into contracts and tools, and improve the harness
whenever the agent fails in a predictable way.

Harness engineering is not "write more docs." It is building the operating
environment that lets an agent do reliable work without depending on chat
history, private memory, or a human repeatedly re-explaining the same rule.

## Core Idea

A repo should contain enough durable context for a future agent or engineer to
answer:

- What is this project for?
- Where are the authoritative sources of truth?
- What boundaries must not be crossed?
- Which decisions require human judgment?
- How do I test, validate, deploy, or safely stop?
- What should I do when existing instructions are wrong or incomplete?

The goal is to make the repo itself the operating manual.

## Minimum Harness Shape

For most repos, start with these files:

```text
README.md
AGENTS.md
HUMAN_INPUT.md
docs/
docs/contracts/
docs/workflows/
```

Add repo-local skills only when a workflow repeats often enough to deserve a
dedicated reusable procedure:

```text
.codex/skills/
.claude/skills/
```

The exact directory names can vary by platform. The principle is stable: keep a
small agent entrypoint, keep durable knowledge in versioned docs, and keep
open human decisions separate from executable instructions.

## What To Put In `AGENTS.md`

`AGENTS.md` should be short. Treat it as a map, not an encyclopedia.

Include:

- Project mission in one or two bullets.
- Scope boundaries: what this repo owns and does not own.
- Required reading order for common work.
- Hard safety rules.
- Pointers to source-of-truth docs, contracts, tests, runbooks, and skills.
- Escalation rules for decisions the agent must not invent.

Avoid:

- Long architecture essays.
- Large troubleshooting guides.
- Stale release notes.
- Every preference anyone has ever expressed.
- Duplicating docs that live elsewhere.

Example:

```md
# AGENTS.md

Keep this file short. Durable project knowledge lives in `docs/`.
Unresolved human decisions live in `HUMAN_INPUT.md`.
Repeatable workflows live in repo-local skills.

## Mission

- Maintain the API service for the product.
- Keep public API contracts, schema changes, and deployment behavior explicit.

## Working Rules

- Read `docs/contracts/api-contract.md` before changing API behavior.
- Read `docs/workflows/change-process.md` before making cross-module changes.
- Update code, tests, and contracts together when a stable surface changes.
- Do not invent product, legal, pricing, or security-policy decisions.

## Source Of Truth

- Architecture: `docs/architecture.md`
- API contract: `docs/contracts/api-contract.md`
- Deployment contract: `docs/contracts/deployment-contract.md`
- Human decisions: `HUMAN_INPUT.md`
```

## What To Put In `HUMAN_INPUT.md`

`HUMAN_INPUT.md` is for decisions agents should not make on their own.

Use it for:

- Product positioning.
- Legal or policy language.
- Security posture choices.
- Pricing, packaging, or business decisions.
- Naming decisions with external consequences.
- Conflicting repo conventions.
- Cost, scaling, or operational tradeoffs without enough data.
- Ambiguous behavior where multiple answers are reasonable.

Do not use it as a dumping ground for ordinary TODOs. If the agent can safely
resolve the issue with code, tests, docs, or repo inspection, it does not
belong in `HUMAN_INPUT.md`.

Useful template:

```md
# HUMAN_INPUT.md

Use this file for decisions agents should not invent.

## Open

## 2026-06-24 - Short decision title
- Status: open
- Area: product | legal | security | architecture | operations | naming
- Owner: unassigned
- Needed: one sentence describing the decision.
- Why blocked: one sentence explaining what cannot be inferred safely.
- Unblocks: files, workflows, or release paths affected by the decision.

## Resolved

## 2026-06-20 - Example resolved decision
- Status: resolved
- Decision: the chosen answer
- Notes: any useful rationale or follow-up
```

## What To Put In `docs/contracts/`

A contract is a stable surface that other code, people, agents, or systems rely
on.

Good contract candidates:

- API request/response shapes.
- Database schema and migration rules.
- Queue payloads and retry behavior.
- Event or webhook formats.
- File and artifact paths.
- Generated-code update rules.
- Deployment triggers and environment wiring.
- Authentication and authorization boundaries.
- Prompt, model, or evaluation assets.
- Public UI behavior that other teams build against.

Each contract should answer:

- What surface does this define?
- Who produces it?
- Who consumes it?
- What invariants must hold?
- What is allowed to change additively?
- What requires coordinated migration?
- How should changes be tested?
- What logs or observability signals prove it is working?

Keep contracts narrow enough to be actionable. A contract that tries to explain
everything becomes another stale manual.

## Workflows Worth Encoding

Create a workflow doc or local skill when the same work recurs.

Good candidates:

- Starting an issue branch and draft PR.
- Debugging production or staging APIs.
- Running a replay fixture.
- Updating generated clients after OpenAPI changes.
- Promoting a prompt or model change.
- Performing a full reindex or backfill.
- Reviewing contract drift across repos.
- Logging a bug in the canonical issue format.

The test is simple: if a human has explained the same process twice, encode it.

## The Correction Loop

The most important harness-engineering habit is how you respond when an agent
makes a mistake.

Do not only correct the agent in chat.

If the mistake reveals a missing durable rule, update the harness first:

1. Identify the missing rule, contract, test, or workflow.
2. Patch the relevant harness file:
   - `AGENTS.md` for a short routing or safety rule.
   - `HUMAN_INPUT.md` for a judgment call the agent should not invent.
   - `docs/contracts/*` for a stable system boundary.
   - `docs/workflows/*` or a local skill for repeatable process.
   - tests or linters for rules that can be enforced mechanically.
3. Tell the agent to reload the relevant contracts or instructions.
4. Then ask the agent to redo the work under the updated harness.

Example prompt:

```text
You crossed an API boundary that should have been explicit.
First update `docs/contracts/api-contract.md` to state the boundary and add
the regression test that would have caught this. Then reload `AGENTS.md` and
the API contract before re-implementing the fix.
```

This turns one failure into a reusable improvement. The agent learns through
the repository, not through an ephemeral scolding that disappears after the
conversation ends.

## When To Use Docs Versus Tests

Use docs when the rule requires judgment or context.

Use tests or linters when the rule can be checked mechanically.

Examples:

- "All user-visible API errors must use this response shape" should become a
  test or schema check.
- "Do not decide pricing tiers without a human" belongs in `HUMAN_INPUT.md` or
  `AGENTS.md`.
- "This queue message must be emitted only after the database write succeeds"
  belongs in a contract and a regression test.
- "Generated clients must be updated after OpenAPI changes" belongs in a
  workflow and CI check if possible.

Documentation guides the agent. Tests and tools constrain it.

## Signs A Repo Needs More Harness

Add harness structure when you see:

- Agents repeatedly ask the same setup questions.
- Agents make the same wrong architectural move.
- API or schema changes break downstream code.
- Deployment steps are known only to one person.
- Debugging requires chat history.
- Prompt or model changes lack rationale.
- Generated files are updated inconsistently.
- Review comments repeat the same style or boundary rule.
- A repo has important behavior but no obvious source of truth.

These are not just documentation problems. They are missing operating
surfaces.

## Signs A Repo Has Too Much Harness

Harness can also become clutter.

Trim it when:

- `AGENTS.md` becomes a long manual.
- Multiple docs repeat the same rule.
- Old plans are indistinguishable from current contracts.
- Docs describe behavior that tests could enforce.
- Instructions mention tools or paths that no longer exist.
- Agents cannot tell which document is authoritative.

Good harness design uses progressive disclosure: a small map first, then
deeper contracts only when relevant.

## Applying Harness Engineering To Any Repo

For a new or existing repo:

1. Add a short `AGENTS.md`.
2. Add `HUMAN_INPUT.md`.
3. Create `docs/architecture.md` with the system map.
4. Create one contract for the most important boundary.
5. Add a change-process workflow.
6. Add tests for the highest-risk contract rule.
7. Add a local skill only after a workflow repeats.
8. When the agent makes a mistake, patch the harness before retrying.

Start small. The point is not to create a bureaucracy. The point is to make the
project easier to operate the next time.

## Platform Independence

This pattern does not depend on any one agent runtime.

Codex, Claude Code, other coding agents, and human engineers all benefit from:

- short entrypoint instructions
- versioned source-of-truth docs
- explicit contracts
- repeatable workflows
- human-decision logs
- tests and linters that enforce boundaries
- feedback loops that improve the harness after mistakes

The platform may change. The durable repo-local operating system remains.
