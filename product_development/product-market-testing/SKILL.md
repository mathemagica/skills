---
name: product-market-testing
description: Design bounded tests of product usability, value, adoption and buying assumptions, interpret actual evidence, and choose whether to iterate, continue or stop. Can precede software implementation.
---

# Product Market Testing

Read the [workflow contract](../references/workflow-contract.md). Establish the
current artifact, intended users versus buyers, available evidence, test budget
and the decision the owner needs to make. A vision owner's approval, a working
demo and positive interview comments are not proof of market demand.

## Choose The Test For The Uncertainty

Distinguish:

- Problem evidence: recent behavior, frequency, workarounds and consequences.
- Usability: whether someone can complete the intended task without coaching.
- Value: whether the outcome improves their real work enough to matter.
- Adoption: whether people return or incorporate it into their workflow.
- Buying: budget, decision authority, alternatives and an actual purchasing step.

When alternatives exist, include a competitive question: what participants use
now, and where practical a side-by-side check against the main alternatives on
the same material. When the product claims to save time or money, plan a measured
comparison with the participant's current method, not only their estimate.
Start with checks the team can run without outside participants, such as
confirming the artifact installs and works on a second machine.

Before choosing tests, look at comparable products for channel, pricing-model and
team-size patterns: competitor pricing pages, founder case-study collections and
public revenue databases. Record each comparable's source, whether its figures are
founder-reported or researched, and how old they are. Use comparables to set
hypotheses and to pick which channel or price to test first. They are never
evidence of demand for this product; collections of businesses that made money
overstate how often a model works, and they rarely record how founders validated
demand.

Propose the cheapest credible experiment: a neutral interview, task-based test,
manual service trial, prototype session or explicitly authorized paid pilot.
Do not force a build when a conversation can resolve the key uncertainty.
Set a bounded cohort/time/cost and success, failure and inconclusive criteria
before observing results. Agree thresholds appropriate to the situation; do not
invent universal conversion rates or statistical certainty from a few interviews.
Propose specific thresholds as clearly labeled proposals for the owners to
confirm, change or reject, with the reasoning behind each; once confirmed, freeze
them and log any later change. Map each pattern of results to the owner's own
decision options (for example go, narrow, pause, stop), plus retest when results
are mostly inconclusive. State sample sizes and quotas honestly: with a handful
of participants, report counts, not rates or preferences between variants.

Use non-leading prompts and realistic tasks. Record participant relationship and
recruitment bias; friendly collaborators are useful but not representative by
default. A co-owner or design partner shaped the product: count their evidence
separately and never as a market signal. Prefer a moderator who did not build the
product and is not close to the participant, and keep builders as silent
observers. If participants receive incentives, record them; incentives can
inflate stated interest and willingness to pay, so weigh buying signals from
incentivized participants accordingly. Define data consent, permitted observation and deletion expectations.
Use synthetic data or readiness work when a real task would expose sensitive data
or cause harm. Clearly disclose mocks and any limitations affecting the test.

## Execute Only Within Authorization

Use the [test plan](../templates/market-test-plan.md),
[session guide and observation sheet](../templates/test-session-guide.md) and
[learning record](../templates/learning-record.md) templates as starting points.
When asked only to plan, deliver the plan, drafts and an empty learning record
marked pending; skip interpretation until results exist.

Draft invitations or session guides in the project workspace. Do not send them,
publish landing pages, buy ads, take payments or promise functionality without
specific authorization. Do not infer that a scheduled test or an invitation means
participation occurred. If unable to run the experiment, provide the plan and mark
results as pending rather than creating hypothetical findings.

## Interpret And Decide

Separate observed behavior, participant statements, measurements, inference and
unknowns. Report the denominator, observation period, missing data and alternative
explanations for any metric. Distinguish stated willingness to pay, a pilot
agreement, a payment and repeat revenue. Before any real payment, confirm with the
owners who receives the money (person or entity), refund terms, taxes and the
payment provider; those are owner decisions, often needing professional advice.
Without usage telemetry, label reuse as self-reported unless the participant
shares evidence such as an exported file or a log. Preserve negative and inconclusive results.

Update the learning record with evidence, criterion outcomes and a recommendation
to continue, change, retest, pause or stop. Choose the next assumption, not an
automatic feature backlog. Material scope changes return through
[product-scope-to-prd](../product-scope-to-prd/SKILL.md); real-use readiness uses
[prototype-to-production](../prototype-to-production/SKILL.md). The owner chooses
the next investment; do not treat a recommendation as a business commitment.
