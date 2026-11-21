# Synthetic Example: Offline Session Planner

Entirely fictional materials and review dialogue for illustrating the workflow.
No real interview, owner approval, implementation, test result or market demand
is represented here. The example deliberately stops at a verification handoff.

## Discovery Inputs

An instructor wants to arrange workshop activities while sharing their screen.
The approved input for this example is a transcript plus two screenshot
descriptions, not actual audio/video. A run using these inputs must not claim
it watched a recording.

| Source | Evidence |
| --- | --- |
| Transcript T1, 04:10 | "I want to drag activities around and see whether they fit in ninety minutes." |
| Transcript T1, 07:30 | "It needs to work without internet. I use my laptop at the venue." |
| Screenshot description S1 | Spreadsheet has activity name, duration and notes; a total of 105 minutes is highlighted |
| Transcript T1, 12:00 | "Maybe I could share templates with other instructors later." |
| Screenshot description S2 | A diagram has a cloud-shaped box labeled "future sharing?" |

Interpretation: stated need is local planning and duration feedback. Dragging is
a requested interaction. Cloud sharing is a future idea, not approved scope.
Whether others face the same problem or would pay remains unknown. The instructor
is vision owner and initial user, not evidence of a broader buying market.

## Proposed Scope, Revision S1

Build a local/offline prototype to test planning a session, not a hosted SaaS.
Enter activity names and durations, reorder them, see the total versus a session
limit, and save/reopen a plan locally. No accounts, collaboration, payments or
cloud integration. Use synthetic activities in the first test. The platform
choice must preserve offline operation and local persistence, not default to a
hosted web application.

Owner review question: "Walk me through planning your next workshop with this.
Would this version answer whether the planner is useful without template sharing?"

Illustrative owner answer: "Yes, approve scope S1. Sharing can wait. I need to be
able to reopen the plan after closing the application."

This fictional answer approves scope S1 only. It does not approve a PRD or build.

## PRD, Revision P1, Based On S1

| ID | Behavior / acceptance example | Source |
| --- | --- | --- |
| R1 | Create a named activity with a positive duration; invalid duration produces an understandable error | T1 04:10; clarification needed for validation policy |
| R2 | Reorder activities without changing their durations or total | T1 04:10 |
| R3 | A plan totaling 105 minutes against a 90-minute limit clearly shows a 15-minute overrun | S1; T1 04:10 |
| R4 | Save locally, close the application and reopen the same ordered plan without network access | T1 07:30; scope review |

Open decision: should zero-minute activities be allowed? Resolve this before
implementing validation; do not let the agent silently choose a product rule.
Illustrative owner answer: "Positive durations only. Approve P1 with that rule.
You may build it locally with synthetic data. Do not publish it."

Record P1 as approved in the fictional project. These are two distinct reviews,
with separate local implementation permission, not an approval transcript for
any actual project. A later request for online sharing would reopen scope/PRD.

## Prototype And Test Handoff

Choose a lightweight implementation supporting offline persistence. Read relevant
engineering skills, not every cloud or scaling skill. Verification must cover
R1-R4, including closing/reopening and disconnected operation. A static screenshot
does not verify persistence. Mark results pending until the checks actually run.

Propose a task-based session: plan a real-length workshop using synthetic content,
reorder an activity, notice an overrun and reopen the plan. Observe completion and
where help is needed. Agree success criteria before the session; do not invent a
successful result. First-owner satisfaction would support usefulness for that
person, not willingness to pay or repeat adoption across instructors.

Do not recruit participants, publish a download or begin cloud productization
without permission. A production review might next address packaging, local data
recovery and support ownership rather than servers, tenant isolation or replicas.
