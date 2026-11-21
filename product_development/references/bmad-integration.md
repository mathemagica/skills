# Optional BMAD Integration

**BMAD is not a dependency.** These skills run with this library and an agent
that can read files; media processing, building and deployment require the
corresponding tools and permissions. All product stages have a standalone path.

BMAD can provide requirements, architecture and delivery workflows when the user
already uses it or explicitly chooses it. No BMAD code is bundled, no particular
version is required and compatibility across releases is not assumed or certified.
See the [official project](https://github.com/bmad-code-org/BMAD-METHOD) for its
current installation instructions and prerequisites. Review and obtain permission
before installing; the library installer does not install BMAD.

## Handoff Instead Of Competing Orchestrators

1. Inspect the installed BMAD version, skills and project configuration. Use its
   own help/catalog to find available workflows; do not assume a command name
   from another release is present. If absent, offer standalone operation.
2. Agree which workflow owns the current stage. Stop autonomous lifecycle routing
   while BMAD owns execution. Do not have both systems independently advance it.
3. Map the discovery brief, scope and PRD to the project's canonical BMAD artifacts.
   Preserve source references, exclusions, requirement IDs and approval records.
   Reuse documents rather than generating parallel conflicting PRDs.
4. Give the selected workflow a small handoff: approved artifact/version, evidence,
   acceptance criteria, unresolved decisions, constraints, mocks and authorization.
5. After its output, reconcile actual changes and verification into the same
   records. Reopen owner review if behavior or scope materially changed.

Typical mappings (verify availability locally): discovery may use a product brief;
requirements may use PRD creation/editing; implementation may use architecture,
story execution and review. Neither a BMAD artifact nor a passing workflow
substitutes for the owner's scope/PRD approvals or actual runtime verification.

Do not copy BMAD's implementation into this family or impose its roles, documents
or installation on a user who only wants the standalone skills.
