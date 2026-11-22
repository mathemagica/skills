# Idea To Market

A family of six portable agent skills for moving from a product vision to
reviewed scope, a prototype, market learning and an appropriate real-use release.
Start with a conversation, a recording, a diagram or an existing product artifact.
You do not need technical vocabulary or a fully formed business to begin.

## Start Your First Project

Use this yourself, or as a facilitator helping someone explain their product
vision. The vision owner makes the product decisions; the agent helps interpret,
propose, implement and verify. An interview with that person is a starting point,
not evidence that a broader market wants the product.

1. Choose a separate project folder for briefs, requirements, code and learning.
   Keep private interviews out of this public skills checkout.
2. Choose the starting material: a conversation, a recording you have permission
   to process, a transcript, screenshots, a diagram or an existing prototype.
   You can start without any media tools by explaining the idea in chat.
3. Ask the assistant to use `new-product-from-scratch`. It will find the right
   stage, ask focused questions and show the next decision. You do not need to
   invoke every skill or read every template.

Without installing skills, point the assistant at your checkout:

```text
Read /absolute/path/to/skills/product_development/new-product-from-scratch/SKILL.md
and follow its linked guidance. My project folder is [path]. My idea is [idea].
Help me decide the smallest useful first version; don't build anything yet.
```

After [installation](#installation), use `$new-product-from-scratch` in Codex or
`/new-product-from-scratch` in Claude Code, then describe the project in ordinary
language. For example:

```text
I have a transcript and screenshots from a product interview. Analyze only those
files in [project folder], separate what the person showed from your assumptions,
and propose a first-version scope for me to review. Don't upload them elsewhere.
```

For a session that has not happened yet, ask: "Help me prepare a discovery
interview. Draft a prep note for me to send; don't send it for me." Start with the
[interview guide](references/interview-guide.md). For an existing approved PRD,
provide the version and approval context and ask to start at the prototype stage.

## What Happens Next

| Stage | What you review or receive | Your next decision |
| --- | --- | --- |
| Discovery | What the agent heard, saw and inferred; a short assumption check and proposed scope | Correct misunderstandings and approve the specific scope version |
| Requirements | A concise PRD (product requirements document) and plain-language owner summary | Approve that PRD version, then separately authorize implementation |
| Prototype | Runnable artifact, verification results, known shortcuts and a demo script | Choose what to test, and with whom |
| Market learning | Experiment plan, then actual observations if the test runs | Iterate, retest, continue, pause or stop |
| Production readiness | Release-specific gaps, mitigations, costs and operating ownership | Decide whether the defined release is ready and authorize any deployment |

Reply in the same conversation with corrections or approval, naming the version
you are approving. The assistant should record that decision, not infer it from
silence or check a template's approval boxes itself. The assumption check helps
prepare scope review; it is not a third mandatory approval ceremony. Publication,
spending, private account access and contacting participants need separate
authorization. You can pause and resume from existing artifacts rather than
repeat the whole process.

Use a demo to explain verified behavior. Use an uncoached task when you want to
test usability; showing the solution first changes what that task can establish.
Simulated features can test comprehension and workflow, not actual integrations,
delivery, response rates or sales. Those need a separately authorized real test.

## The Workflow

Conversation / optional recorded demonstration -> evidence and proposed MVP
scope -> owner review -> PRD -> owner signoff -> prototype -> testing and learning.

Testing can happen before building, and readiness work may be necessary before
real-user tests. Not every idea should become software or reach production.

| Skill | Use it for |
| --- | --- |
| [new-product-from-scratch](new-product-from-scratch/SKILL.md) | Choose the starting point and coordinate stages |
| [product-discovery-to-scope](product-discovery-to-scope/SKILL.md) | Interpret interviews/demos and review an MVP scope |
| [product-scope-to-prd](product-scope-to-prd/SKILL.md) | Review observable requirements before building |
| [product-prototype-build](product-prototype-build/SKILL.md) | Implement and verify the appropriate kind of prototype |
| [product-market-testing](product-market-testing/SKILL.md) | Test usability, value, adoption or buying assumptions |
| [prototype-to-production](prototype-to-production/SKILL.md) | Close release-specific operational gaps |

## Installation

**BMAD is not required.** There are no mandatory external framework or media
service dependencies. Keep the complete library checkout: these skills reference
sibling skills, shared guidance and the existing engineering playbooks.
An individual copied skill folder is not a complete installation of this family.

Clone the repository, or use your existing checkout:

```sh
git clone https://github.com/mathemagica/skills.git
cd skills
```

With Python 3.10+ on a filesystem that supports directory symlinks, install links
to the library's skills into your agent's directory. Choose one or both:

```sh
# Codex personal skills
python3 scripts/install_skills.py --target-dir ~/.agents/skills
# Claude Code personal skills
python3 scripts/install_skills.py --target-dir ~/.claude/skills
```

The installer links all skill families so engineering handoffs remain available.
It refuses existing conflicting folders/links rather than replacing them. It
does not change agent settings, install BMAD, connect services or schedule work.
Review any conflict yourself; do not delete a different skill just to proceed.
Keep the checkout at the same path; subsequent reviewed checkout changes become
visible through the links. Restart the agent if discovery needs refreshing.
On Windows, directory symlinks may require Developer Mode or elevated permission;
use the direct-file route below if unavailable, rather than weakening permissions.

No installation is necessary when the agent can read the checkout. Ask:

```text
Read /absolute/path/to/skills/product_development/new-product-from-scratch/SKILL.md
and use it for this product idea. Resolve relative references from that file's
canonical location. Keep project materials in my separate project workspace.
```

After installation, invoke `$new-product-from-scratch` in Codex or
`/new-product-from-scratch` in Claude Code. The skill should orient you, not
automatically start building. Each stage can also be invoked independently.

## Tools And Permissions

The agent must be able to read and write the chosen project workspace. Audio
transcription and video inspection depend on its available tools; the skills do
not include a transcription engine. A transcript-only run must say it did not
inspect the video. Building and verification need the selected platform's tools.
No cloud provider, hosting subscription or external account is required to start.

Get recording/processing consent and agree where private material can go. Local
file storage does not imply offline AI. Never put private interviews in this
public library. Scope review and PRD signoff are separate, and neither authorizes
publication, spending, account connections or recruitment.

## Optional BMAD

Use BMAD only if you choose it. Install it separately using the
[official instructions](https://github.com/bmad-code-org/BMAD-METHOD), including
the prerequisites for the version you select. This library does not bundle or
install it and makes no cross-version compatibility guarantee. See the
[BMAD handoff guide](references/bmad-integration.md) for using installed workflows
without competing PRDs, duplicate orchestration or bypassed owner reviews.

## Interview Kit And Templates

- [Interview guide](references/interview-guide.md) for running a discovery session
- [Owner prep note](templates/owner-prep-note.md) to send before the session
- [Recording evidence](references/recording-evidence.md) for transcripts, screen
  frames, privacy and third-party software shown on screen
- [Assumption check](templates/assumption-check.md), a plain-language review
  before scope approval
- [PRD owner summary](templates/prd-owner-summary.md), a one-page companion for PRD
  approval
- [Demo script](templates/demo-script.md) for the owner to show a verified prototype
- [Market research sources](references/market-research-sources.md) for
  comparables, failure databases and public problem evidence
- [Market test plan](templates/market-test-plan.md), [test session guide and
  observation sheet](templates/test-session-guide.md) and
  [learning record](templates/learning-record.md) for market testing

Templates are starting points; adapt them to the project and the person.

## Examples And Validation

The [offline session planner](examples/offline-session-planner.md) demonstrates the
two owner reviews and an honest prototype/testing handoff without private data.
The [volunteer shift swaps](examples/volunteer-shift-swaps.md) example shows a
feature-gap demonstration, an assumption check that corrects the agent, and a
scope that records the gap without copying the existing product.
The [behavioral scenarios](evaluations/scenarios.md) define realistic forward
tests. They are a test protocol, not a claim those agent runs passed.

Run the repository's structural and installer tests from the checkout:

```sh
python3 -m unittest discover -s tests -v
```

Those tests check packaging and dependency resolution, not product judgment or
market outcomes. Replaying private cases needs participant permission; use
synthetic fixtures for public demonstrations.
