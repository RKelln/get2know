# Get2Know

**Open-source onboarding for small organizations, at scale.** An AI interviewer gets to know a small business or non-profit well enough to write down how it actually works. Then it helps the owner find what AI can do for them, preferring open tools they can own, change and share. What the organization learns stays in its own plain-text folder; what the community learns flows into a shared, open commons.

**Status (2026-11-14, version 0.2.4): early and working. Used in a library workshop (participants played a made-up owner), which went well; not yet used by an owner on their own business.**
- **Built:** skills in `skill/` for the interview (first interview, follow-up from notes, resume, re-check, outcome check, helper mode, other languages, more than one voice; owner-editable settings), "did you know" cards, a builder brief, and share-safely, and an experimental `teach-a-job` (show it one job and it writes the job down as a skill). A one-prompt version for any chat app, an experimental three-part version, and a versioned zip with safe updates.
- **Tested in simulation** with `rehearse` (one model plays the owner, another interviews, a third judges, plus code checks): a made-up bike shop (cooperative, vague, guarded, hostile, hurried and low-literacy owners; clean and messy notes) and a made-up non-profit (first interview, resume, a planted instruction in an email). Recent rounds pass most checks; the open problems are listed in `docs/DESIGN.md`.
- **Not yet tested with any model:** `teach-a-job`, the builder brief, share-safely, the chat prompts, the re-check, outcome, helper, language and more-than-one-voice modes.
- **Planned:** kinds of limit (a rule, theirs to keep, a trust call) and how trust is earned (`docs/DESIGN.md` D66, `docs/research/limits-and-trust.md`).
- **First use:** a library workshop on 2026-11-02, with a repeat planned for 2026-11-30.
- **The commons** is a proposal (`docs/capability-commons.md`) with 43 seed records in `commons/`, none vetted yet.

## The idea

1. **Get to know.** An agent interviews the owner, one plain question at a time, about the real work: people, tools, money, customers, the week, and what must stay human. It writes a `profile/` folder of plain-text files: how we work, our limits, ideas, notes, a log. Every line says where it came from. The owner can read and fix all of it.
2. **Discover.** From the profile, the agent proposes three to five honest ideas, each tied to something the owner said, with at least one "not for AI". "Did you know I can...?" cards show uses people would not think to ask for.
3. **Hand off.** The profile is the starting context for every later agent: one that builds a small tool, drafts replies, or checks the books. It knows the business, its words and its limits instead of guessing.
4. **Share (the commons, proposed).** A public, CC0 index of what AI can do for small organizations and which open-source tools do it, tended daily by cheap agents and reviewed by people. Knowledge comes first ("this is possible, and here it is shown on made-up data"), so the owner's own AI can build a safe version; vetted open tools are preferred once they pass safety checks. Unvetted tools may be named with a warning, for use only by owners who help check them. Organizations search it locally against their profile, so the profile never leaves home. With consent, they send back stories and **gaps** (needs nobody meets yet), which become a shared to-do list for open-source builders.

## Why

Most people trying AI start with "what can it do?" The useful question is "what does my organization actually need?", and most owners cannot answer that cold. A good interviewer can. The result is specific to the organization, and it outlasts any one tool or model.

Why open source: an agent can only fix what it can read. Open tools are the ones a small organization's own helper can maintain, adapt and improve, and the costs of maintenance become visible and shareable. Get2Know's job is to make that path the easy one: find the need, show what is possible, prefer what is open, and turn shared gaps into shared work.

## Try it

Copy `skill/` into a folder, open that folder in Claude Code or Codex, and type "hi". It works from scratch, from notes you already have, or picks up a previous session from `profile/`. `skill/FACILITATOR.md` is for whoever runs a session.

No Claude Code or Codex? Paste `dist/get2know-prompt.md` into a new chat in any AI chat app and answer its questions. It gives you your profile files as text to save. To carry on later, paste the prompt and your files into a new chat.

*Experimental:* chat apps that limit pasting, or small models, can use the three-part version in `dist/chat/`: paste `get2know-1-interview.md` first; it asks for the other parts when it needs them.

One download: the zip on the project's Releases page (`get2know-<version>.zip`; the first is 0.1.0). To update, see `UPDATE.md` inside; updating never touches your `profile/`.

## What is here

- `skill/`: the skill folder people use. `AGENTS.md` at the top; skills in `.agents/skills/` (`get2know`, `did-you-know`, `builder-brief`, `share-safely`, `teach-a-job`), linked as `.claude/skills/`. `VERSION`, `CHANGELOG.md`, `UPDATE.md`.
- `tools/`: builds the chat prompts (`dist/get2know-prompt.md`, `dist/chat/`), the manifest and the release zip (`python3 tools/build_all.py`; releasing: `docs/RELEASING.md`), and `update.py`.
- `commons/`: seed records for the capability commons (CC0) and their checker.
- `tests/rehearse/`: simulated interviews (a made-up bike shop, with clean and messy drafts, and a made-up non-profit), code checks and a judge rubric, using [`rehearse`](https://github.com/RKelln/rehearse). Everything needed to run them is in this repo.
- `docs/DESIGN.md`: every decision and why (start here). `docs/design-builder-side.md`: the builder side, from an approved brief to a tool the owner keeps. `docs/capability-commons.md`: the commons proposal. `docs/research/`: sources checked.
- `docs/REQUIREMENTS.md`, `docs/MVP-first-deployment.md`: the starting requirements and the first deployment.
- `docs/prior-art-*.md`, `docs/design-considerations.md`: research memos, not specs.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `docs/GOVERNANCE.md`: proposals, not yet decided; who hosts and stewards the project is open.
- `HANDOFF.md`: what is in flight. `AGENTS.md`: instructions for agents working on this repo.

## Licence

Code: MIT. Prompts and skill text: CC BY 4.0. Commons records: CC0. See `LICENSE` and `skill/LICENSE.md`.
