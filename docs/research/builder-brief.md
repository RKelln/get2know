# Research: the builder-brief skill

Checked 2026-10-29, at source (GitHub API for licences and files; project pages for the rest). Purpose: reuse what exists for "turn an idea into a brief a coding agent can build from", rather than reinvent it. Result: **reference and adapt ideas; copy no text; depend on nothing.**

## Sources

| Source | Licence (checked at source) | What it is |
|---|---|---|
| mattpocock/skills, commit 59db609 (pushed 2026-10-27): `grilling`, `grill-me`, `to-spec`, `to-tickets`, `tdd`, `implement-spec`, `teach`. https://github.com/mattpocock/skills | MIT (repo licence, GitHub API) | Engineering skills: interview a plan, synthesize a spec, slice tickets, build test-first. |
| GitHub spec-kit, `templates/spec-template.md` and `/specify`, `/clarify`, `/plan`, `/tasks`. https://github.com/github/spec-kit | MIT | Spec-driven development: prioritized user stories with Given/When/Then, `FR-###` "MUST" requirements, `[NEEDS CLARIFICATION]` markers, measurable success criteria. |
| Kiro specs. https://kiro.dev/docs/specs/ | Proprietary product (AWS); docs only | `requirements.md` → `design.md` → `tasks.md`. Its docs page says "structured notation"; community templates say EARS (not confirmed on the official page). |
| EARS, Mavin et al., Rolls-Royce, IEEE RE'09. https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax | Method, not code | Five sentence shapes: ubiquitous (SHALL), WHEN (event), WHILE (state), WHERE (optional feature), IF/THEN (unwanted behaviour). |
| anthropics/skills: `doc-coauthoring` (Reader Testing), `discernment-nudge`, `skill-creator`. https://github.com/anthropics/skills | Mostly Apache-2.0 per skill (`LICENSE.txt`); doc skills source-available; `doc-coauthoring` has no licence file of its own | Skill examples. Reader Testing: a fresh agent with no context reads the doc and answers predicted questions. |
| snarktank/ai-dev-tasks `create-prd.md`. https://github.com/snarktank/ai-dev-tasks | Apache-2.0 | A popular PRD prompt: 3-5 clarifying questions with lettered options, then a PRD with goals, stories, numbered functional requirements, non-goals. |

## What we took (ideas only, in our own words)

- **Describe vs decide split** (DESIGN Framing) holds up: `to-spec` says "Do NOT interview the user; just synthesize" and expects decisions already settled by `grilling`. So builder-brief does **not** settle the build. It writes the owner's problem, limits and tests, and lists unsettled choices as `OPEN:` for a grilling/to-spec-style step in the build folder.
- **Explicit unknowns** (spec-kit `[NEEDS CLARIFICATION]`): our `OPEN:` (a choice) and existing `GAP:` (a fact).
- **Out of scope / non-goals** (to-spec, create-prd): our "What it must never do", extended with every `limits.md` line, and "Later, maybe".
- **Testable, user-visible acceptance criteria** (spec-kit Given/When/Then, `to-tickets` checklists, `tdd`'s "tests verify behaviour through public interfaces" and "expected values from an independent source"): our tests are things the owner can check by looking, with a worked example from the owner's real case. The owner's example is the independent source of truth that `tdd` asks for.
- **EARS shapes, in plain words**: "When I give it..., it...", "It never...", "If..., it says so and does not guess". These are EARS's event-driven, unwanted-behaviour and IF/THEN patterns without SHALL. A builder can translate them one to one.
- **Independent, smallest slice first** (spec-kit "each story independently testable, a viable MVP"; `to-tickets` tracer bullets): our "simplest version", often "no new tool" first.
- **Confirmation gate** (`grilling`: do not act until the user confirms): the owner approves the tests before a builder may start.
- **Teach-back**: from design-considerations §9 (explaining to another is a strong learning strategy; keep one human act that preserves competence). `teach`'s fluency-vs-storage distinction supports asking the owner to explain in their own words rather than reading ours back.

## What we rejected, and why

- **Depending on mattpocock/skills or spec-kit.** Both assume a developer, a repo and an issue tracker (`/setup-matt-pocock-skills`, feature branches). An owner has none. We name them as optional tools for the build step only.
- **Grilling's format for owners**: whole-frontier rounds of numbered questions, each with a recommended answer, worded so "yes" accepts it. That breaks our one-question rule and D4 (no suggested answers). The hand-off asks the build-planner to keep one plain question at a time even if it uses grilling.
- **Grilling's "never ask what you can look up"**: rejected as in D3; reading the profile is fine, the owner's other files need a yes.
- **create-prd's lettered multiple-choice questions**: fast for developers, leading for owners (D4).
- **to-spec's "LONG, extremely extensive" user stories and spec-kit's measurable SC-### metrics**: too long for an owner to approve; invites invented numbers. Capped at 8 tests, no number the owner did not say.
- **SHALL / MUST wording and FR-### ids**: not grade 6. Plain sentences carry the same shapes.
- **Kiro's design.md / tasks.md**: architecture and tasks belong to the build step, in the build folder.
- **Reader Testing with a sub-agent** (doc-coauthoring): useful, but not every harness has sub-agents and it doubles cost. Candidate for a rehearse check instead: give a fresh agent only the brief and limits, ask it what it would build and what it must never do.

## Copying and credit

No text was copied from any source. Ideas are credited here. If a future version copies text from mattpocock/skills, spec-kit (MIT) or anthropics/skills (Apache-2.0), keep their licence notice next to it.
