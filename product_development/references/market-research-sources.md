# Market Research Sources

Use this when building the Comparables section of a market test plan or looking
for problem evidence before a test. Sources are grouped by what they can tell you.
None of them is evidence that people want this product. They help you choose
which assumptions to test first and set reasonable thresholds.

Specific services change often. The names below were checked in November 2026;
confirm a service still exists and still works the same way before relying on it.

## How strong is each kind of evidence

| Kind of source | What it can support | Main bias |
|---|---|---|
| Payment-provider-verified revenue | Pricing and revenue ranges for similar products | Listed by founders proud of their numbers or trying to sell |
| Business-for-sale marketplaces | What similar businesses are worth (useful at a grow, sell or stop decision) | Asking prices are not sale prices; stalled businesses get listed |
| Founder case-study collections | Channels and first-customer tactics | Self-reported, success-only, rarely say how demand was validated |
| Failure and postmortem databases | Reasons similar products died, to turn into assumptions | Small, uneven coverage; causes are founders' own accounts |
| Public posts and complaints | That the problem exists and how people describe it | Shows pain, not willingness to pay; loud users over-represented |
| Competitor reviews | Gaps and frustrations with existing options | Unhappy and very happy reviewers over-represented |
| Launch platforms | How similar products are pitched and received | Attention is not purchase intent |
| Search trends and traffic estimates | Direction of interest, rough competitor size | Relative or estimated, weakest for niche products |

Record for each comparable: the source, whether figures are verified,
founder-reported or estimated, and the date.

## Verified revenue and marketplaces

- TrustMRR and StartuPage read revenue from payment providers such as Stripe.
  OpenRevenue is an open-source alternative using cryptographic proof.
- Acquire.com and Flippa list businesses for sale with vetted figures. IndieMaker
  and similar listings are often self-reported; treat them like case studies.
- Coverage is strongest for web SaaS and AI tools. Desktop, professional and
  niche tools are often missing; say so rather than stretching weak matches.

## Founder case studies

Starter Story, Indie Hackers and similar collections. Use them for channel and
pricing-model patterns and for how founders found their first customers.
Revenue figures are founder-reported and rank lowest.

## Failure databases

Successful-business collections overstate how often a model works. Before
testing, search for dead products that tried the same idea and turn each stated
cause of failure into an assumption to check.

- Failory's Startup Cemetery (failures grouped by cause)
- CB Insights' collected founder postmortems
- Startups.RIP (shut-down Y Combinator companies)
- Loot Drop (a larger list of dead startups)

Also search the web for "[product category] shut down" and "[competitor]
discontinued"; small tools rarely appear in these databases.

## Problem evidence from public posts

Public complaints are stated by strangers who were not asked, which makes them
useful for problem assumptions. They do not show anyone would pay.

- F5Bot (free email alerts for keywords on Reddit, Hacker News and Lobsters)
- Paid monitors such as Syften and Octolens
- A manual web search restricted to a site, for example `site:reddit.com`
- GummySearch closed in late 2025 after losing Reddit API access; older guides
  that recommend it are out of date.

Quote posts by link and date, do not collect personal details, and use what you
find to shape interview questions rather than as a result.

## Competitor reviews

Read low and middle ratings on G2, Capterra, the Mac App Store, Google Play or
similar sites for direct competitors and the workaround people use today. Look
for the same complaint repeated in specific words by different reviewers; one
complaint is noise. Useful for choosing which comparison to run in a test and
for positioning, not for sizing demand.

## Launch platforms

Product Hunt and similar launch pages show how comparable products were pitched
and which objections commenters raised. Upvotes and signups from a launch are
weak signals of purchase: founders commonly report hundreds of signups and very
few paying customers. If a launch is used as a channel test, set the threshold on
paid conversions or qualified waitlist signups, not upvotes.

## Search trends and traffic estimates

- Google Trends shows relative interest on a 0-100 scale, not search counts.
  Niche terms often show zero even when customers exist, and small changes near
  the floor look like large swings. Use it for direction and seasonality, and
  check that the searched phrase is the buyers' wording, not the team's.
- Traffic estimators (Similarweb, Semrush, Ahrefs and others) give ranges that
  are least accurate for small sites; published comparisons show median errors
  around half of actual traffic or worse. Free tiers are limited. Use rank order
  among competitors, not absolute numbers.
