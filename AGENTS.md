# Get2Know: instructions for the working agent

You are building Get2Know. Read `README.md`, then `docs/REQUIREMENTS.md`, `docs/MVP-first-deployment.md`, `docs/prior-art-to-check.md`, `docs/prior-art-research.md`, `docs/research/agent-lean.md` and `docs/design-considerations.md`.

`docs/design-considerations.md` and `docs/prior-art-research.md` are research memos, not specs. They deliberately leave tensions unresolved. Check their claims at their primary sources before relying on them, and do not treat their suggestions as decisions: decide, and record why in `docs/DESIGN.md`.

## Your remit

- The MVP in `docs/MVP-first-deployment.md` has a hard date. Ship it first, as small as it can be and still pass its success criteria.
- Beyond the MVP, **you own the general design.** `docs/REQUIREMENTS.md` is a rough starting point written by someone who is not an expert in small-business consulting. Check it against prior art, correct it, and extend it. Record what you changed and why in `docs/DESIGN.md`. Ask Ryan when a choice really is his; otherwise decide and note it.
- Nothing in these docs is sacred. Where a requirement conflicts with something you learn, say so and propose the change.

## Working rules

- Plan in writing before building. Short plan, then build.
- Python with `uv` (not bare pip). No heavy dependencies; the interview itself is mostly prompts and plain text.
- Plain-text outputs (Markdown, CSV). A person should be able to read and edit every artifact in a text editor.
- Spoken-style outputs (interview questions) are short and in plain language, near grade 6. Define any business or AI word the first time.
- The interviewer asks **one question at a time** and waits.
- Test with the [`rehearse`](https://github.com/RKelln/rehearse) tool (simulated owner plays one model, the interviewer another; see `tests/rehearse/README.md`). Live runs spend Ryan's subscription: dry-run first, ask before running live, keep runs small.
- Do not copy the fixture's answer key anywhere an interviewer or sim can read it.
- Keep this repo general. Its docs and code should not depend on any one deployment. The first deployment is described only in `docs/MVP-first-deployment.md`.
- Report faithfully: say what is untested.
