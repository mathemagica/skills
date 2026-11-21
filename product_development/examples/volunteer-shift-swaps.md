# Synthetic Example: Volunteer Shift Swaps

Entirely fictional materials and review dialogue, illustrating a common starting
point: an owner demonstrating where existing software falls short. No real
interview, product, approval, implementation, test result or demand is
represented. The example stops at an assumption check and proposed scope.

## Discovery Inputs

A food bank volunteer coordinator uses a commercial scheduling app (unnamed here)
and a spreadsheet. The approved inputs are a transcript and three frames extracted
at timestamps the transcript points to, following
[recording evidence](../references/recording-evidence.md).

| Source | Evidence |
| --- | --- |
| Transcript T1, 03:40 | "Every week a few people can't make their shift and text me. Then I'm calling around for a replacement." |
| Frame F1, 05:10 | Scheduling app week view; Saturday 9am shift shows 6 of 8 slots filled; no visible waitlist or swap control |
| Transcript T1, 05:20 | "See, there's nowhere to put people who'd fill in. So I keep this." |
| Frame F2, 06:05 | Spreadsheet titled "fill-ins"; columns Name, Phone, Usual days, Last asked; 23 rows |
| Transcript T1, 11:45 | "I'd love it to just text the fill-in list automatically and the first yes gets the shift." |
| Transcript T1, 14:30 | "The app has reports and payroll stuff too, but we don't use that." |
| Frame F3, 14:35 | App settings page; several personal phone numbers visible (not transcribed) |

Interpretation:

- **Stated:** last-minute dropouts are weekly; finding replacements is manual.
- **Demonstrated:** the inspected app screen shows open slots and no visible
  fill-in control; a separate spreadsheet contains a fill-in list.
- **Stated, not verified:** the owner says the app cannot store fill-ins. One
  screen does not establish that the entire app lacks the feature; configuration,
  other screens or existing integrations could change the build decision.
- **Inferred:** the core job is "fill a dropped shift quickly," not "replace the
  scheduling app."
- **Unknown:** how long filling a shift takes today; whether volunteers would
  respond to automated texts; whether other coordinators have this problem; who
  would pay.
- **Not scope:** the app's reports, payroll features and screen design. Record the
  gap, not the product. F3 contains personal data and is excluded from records.

## Assumption Check, Revision A1

Sent to the owner using the [assumption check](../templates/assumption-check.md):

| # | You said or showed | So I assumed | Owner answer (fictional) |
| --- | --- | --- | --- |
| A1 | Calling around for replacements (03:40) | The first version should help fill a dropped shift, not replace your scheduling app | Right |
| A2 | "Text the fill-in list automatically" (11:45) | Messages go to everyone on the list at once | Not quite: "Only people whose usual days match, or I'll annoy everyone." |
| A3 | "First yes gets the shift" (11:45) | The shift is then updated in the scheduling app automatically | Not sure: "Can it do that?" |
| A4 | Spreadsheet F2 | Volunteers have agreed to receive texts from this tool | Not sure: "Some have. I'd need to ask." |

Owner's own description (fictional): "When someone drops a shift, I click once,
the right fill-ins get a text, and I see who said yes."

Follow-ups: A3 needs an integration check; the scheduling app's access is
unknown, so the first version should simulate the update and have the coordinator
enter it manually. A4 is a consent requirement, not a detail: messaging only
volunteers who agreed.

## Proposed Scope, Revision S1

First test whether the coordinator can select appropriate fill-ins and understand
the replacement workflow using synthetic data and simulated messages. This cannot
test volunteer response or actual time to fill a shift. One workflow: the
coordinator marks a shift as dropped; the tool
selects fill-ins whose usual days match and who have agreed to texts; it sends a
request (simulated in the first test, real only after separate authorization);
the first "yes" is shown to the coordinator, who updates the scheduling app by
hand. Excluded: replacing the scheduling app, reports, payroll, integration with
the app, volunteer self-service. Synthetic volunteer data in the first test.

Success evidence for the simulated test: can the coordinator complete the
selection/response workflow and correctly distinguish simulated messages from
real delivery, with criteria agreed before observation? No results are assumed.

A later, separately authorized pilot could test whether targeted requests fill
real dropped shifts faster, after recipient consent, real messaging readiness and
operational safeguards are established. Agree an observation window and compare
actual baseline and pilot times; label any baseline estimates as estimates.
Owner satisfaction alone would not establish demand across food banks.

Next: owner approval of S1, then [product-scope-to-prd](../product-scope-to-prd/SKILL.md).
No messages are sent, no accounts connected and no volunteers contacted without
separate authorization.
