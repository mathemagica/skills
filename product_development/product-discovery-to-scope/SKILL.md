---
name: product-discovery-to-scope
description: Turn product interviews, recordings, demonstrations, diagrams or existing prototypes into an evidence-backed MVP scope for owner review. Use before requirements or when product intent is unclear.
---

# Product Discovery To Scope

Read the [workflow contract](../references/workflow-contract.md). Accept the
inputs available; a 30-45 minute recorded conversation and demonstration can
be useful but is not a prerequisite or a prescribed interview duration.

## Gather And Interpret Evidence

For a planned session, use the [interview guide](../references/interview-guide.md)
and draft the [owner prep note](../templates/owner-prep-note.md) beforehand for
the facilitator to send. Do not send it without specific authorization. For
transcripts, screen content and frames, follow
[recording evidence](../references/recording-evidence.md).

Establish consent, material ownership, approved processing location and handling
expectations before reading recordings. Check which tools actually support the
audio and video formats. Transcribe only with available authorized tools; retain
source timestamps and speaker uncertainty where supported. A transcript does
not establish what appeared on screen. Request screenshots, a walkthrough or
clarification when visual evidence is needed. Do not fabricate inaccessible
media, timestamps, quotations or transcription accuracy.

For a live interview, ask for a recent concrete example: what triggered the work,
what they did, tools and handoffs, where it failed, and what a better outcome
would mean. Invite demonstrations of a prototype, existing software or diagrams.
Clarify who uses it, who pays, who operates it and who owns the vision; these may
be different people. Separate frequent pain from an appealing feature idea.

Capture material observations with source references. Label them as stated,
demonstrated, inferred or unknown. Preserve the person's terminology alongside
your interpretation. If audio, screens and diagrams conflict, surface the
conflict rather than choosing the most convenient interpretation. A demonstrated
workaround may suggest a need, but does not prove other users have it.

## Propose A Small Testable Scope

Summarize the intended user, problem, current workflow and desired outcome. Name
the riskiest assumption and propose the smallest artifact that could test it,
including a non-software alternative where useful. Distinguish a learning
prototype from an MVP intended to deliver ongoing value; agree what this version
means here rather than relying on the acronym.

Include:

- One end-to-end workflow, with concrete input and expected result.
- Included capabilities and explicit exclusions; do not reproduce every feature
  visible in demonstrated third-party software.
- Data needs, platform/accessibility constraints, important risks and dependencies.
- Which integrations will be real, simulated or manual, with implications for
  what the test can establish.
- Success evidence, a bounded effort/cost hypothesis, and reasons to stop or narrow.
- Assumptions that need owner confirmation versus external user/buyer testing.

Before asking for scope approval, present a plain-language
[assumption check](../templates/assumption-check.md): what you heard, each
assumption that changes what gets built, terms the owner may not know, and a
request to describe the first version in their own words. Treat agreement without
that description as not yet understood. Then ask the vision owner to walk through
this scope in their own words. Resolve
material misunderstandings, record approval of the specific scope version, and
pause before the [PRD stage](../product-scope-to-prd/SKILL.md). If the next useful
step is market discovery rather than building, suggest
[product-market-testing](../product-market-testing/SKILL.md).

## Output

Use or update a concise discovery brief and proposed MVP scope in the agreed
workspace. Link important claims to source evidence and identify remaining
questions. Do not include raw private media in a public repository. Scope
alignment is not market validation, engineering feasibility or build approval.
