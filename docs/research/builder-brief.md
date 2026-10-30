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

## Added 2026-10-30: Elephant-Goldfish Model (EGM)

google/elephant-goldfish-model, commit 403d888 (2026-10-30), version 0.1.0, Apache-2.0. https://github.com/google/elephant-goldfish-model. Read at source: README, `docs/harnesses.md`, `docs/codex.md`, `TESTING.md`, the manifests, `egm-brainstorm`, `egm-review-loop`, `egm-resolve` and the comprehension persona. Its README says thousands of Google engineers use it. We have not run it.

**What it is.** A plugin of skills for engineers designing a feature before coding. The "elephant" (the main agent, holding the project and the conversation) drafts a spec. The "goldfish" (fresh subagents that see only the document and the sources they are given, never the conversation) review it from several angles. The person resolves trade-offs, approves the design and decides what to build.

**What is automatic and what is not.** Goldfish find problems; they do not fix them. In `egm-resolve` the elephant marks each finding PROPOSE FIX (the person accepts or rejects), CONTEST (the elephant thinks the reviewer is wrong) or ESCALATE (it "needs the user's knowledge, not only approval"), and stops for the person. There is an "accept all" option. Its README: "A review does not replace tests or human judgment."

**Why it is not owner-ready as it stands.** The person in the loop is assumed to be an engineer: escalations come out in engineering terms, the brainstorm lenses are load, migration, on-call and tech debt, and two reviewers (codebase details, drift report) assume existing code. An owner's first tool usually has none. Its brainstorm rules ("never agree by default", "critique first") are the wrong tone for a nervous beginner.

**Why it is still a good example.** `egm-review-loop` takes its reviewers and standards as file paths, so a project can supply its own. That allows an owner-facing set: "Does this break a line in `limits.md`?", "Could a spreadsheet do it?", "What does it cost each month, in dollars?", "What happens when it is wrong, and can the owner undo it?". The elephant settles the engineering findings and asks the owner only what the owner can judge, as plain trade-offs (cost vs speed, more work for the owner vs more for the tool). Our brief is its input, and the owner-approved tests are its exam.

**Packaging practices worth copying** (see D56):
- One copy of the skill text, with a thin manifest per harness (`.claude-plugin/`, `.codex-plugin/`, a root `plugin.json`). Users install with `claude plugin marketplace add <owner>/<repo>`. That needs a public repo.
- Unit tests that fail when the manifests' name, version or description drift apart.
- "Install the whole plugin": skills that read files outside their own folder break if only `skills/` is copied. We have one such read: `builder-brief/SKILL.md` reads `get2know/references/profile-folder.md`. A plugin moves that path (EGM uses `${CLAUDE_PLUGIN_ROOT}` on Claude, and "three folders above SKILL.md" on Codex).
- A test that keeps each skill body under 24,000 bytes (Antigravity's limit). Ours: largest 12,441.
- A per-skill `agents/openai.yaml` with a display name and icon for Codex.
- A record of what has actually run end to end on each harness, kept apart from what is merely configured.
- One-turn scenario files with regex pass/fail patterns (`test_scenarios.yaml`): far cheaper than a simulated interview.

**Delegation lessons, if we use subagents.** Subagent tools differ by harness and version; EGM checks the tool's options at run time (on Codex it sets `fork_context: false`). It treats a missing read or a timed-out reviewer as an incomplete review, not a clean one. EGM stops when it cannot spawn a subagent; an interview must carry on without one.

## Copying and credit

No text was copied from any source. Ideas are credited here. If a future version copies text from mattpocock/skills, spec-kit (MIT) or anthropics/skills (Apache-2.0), keep their licence notice next to it.
