# teach-a-job: the step between an idea and a brief

**Status:** built 2026-11-06 as D68, untested with any model. This note keeps the reasoning; `skill/.agents/skills/teach-a-job/` is the source of truth.
**Applied 2026-11-06** to `W07.md` (draft 3) and `decks/W07-run-your-company/talk.md` (outline draft 2), with one change from Ryan: the founder-story screens came out of the room and the turn goes to the access trade instead. The line that matters is that open source fixes trust in the tool, not the file leaving the machine.
**Trigger:** the W07 revision, where the four-pile sorting exercise was replaced by a derivation exercise (agent works one job step by step, then reads back the steps, corrections and questions).
**Revisions:** first written as a separate fifth skill; Ryan read it as a second path through the brief, which is the better shape; then Ryan ruled that the artifact is a **skill**, not a recipe, because that is the mainstream word and it is what actually gets built. The rename is not cosmetic: it changes where the file has to live, below.

## What it is

One job, run once with the agent working, written down as a **skill**: a folder with a `SKILL.md` and, if the run produced one, a script beside it.

The body is the five lines the workshop already teaches:

    When:         the trigger.
    Read:         which files, and nothing else.
    Do:           the steps, in order.
    Stop and ask: the questions the agent had to ask.
    Output:       where the result goes.

What the skill format adds is the frontmatter: a name and a description. That is the part a recipe could not do.

**Why skill beats recipe, and it is not only fashion.** A description is how the harness decides when to load the thing. A recipe sits in a folder until somebody remembers it exists; a skill announces what it is for, so it comes back to the owner next time the job comes up, without them having to remember. For a kit whose claim is that the assistant gets more useful over time, that difference is the feature.

## Why it belongs in this kit

The arc today is: interview → `profile/` → ideas → builder brief → build. Between **ideas** and **brief** there is nothing that turns a recurring job into something the assistant runs again. A brief is for a thing someone builds; a skill is for a job the agent performs. For most owners the second one is the first win, and it needs no coding agent and no install.

**The kit already notices the moment and then walks away from it.** From `skill/.agents/skills/get2know/SKILL.md`, under "Keep it flowing, keep track":

> **Asked to do a task now?** Do one short example in the chat, save what it taught you about how they work in `profile/`, say so in one line, then go back to your next question. Do not make new files for drafts unless they ask.

That is the moment this proposal is about. The "go back to your next question" is why it produces nothing reusable: the procedure exists for one chat scroll and is then gone. The fix is not a new behaviour so much as letting this one finish.

It is also why the design should not be a reference inside the interviewer. The interview's rhythm is one question per message on a budget of about eight answers; a run's rhythm is one question per *stop*, inside a job that may take ten minutes. Sharing a skill would make both worse.

## Where the skill lives, and how it loads

`profile/skills/<name>/` is the master copy: it travels with the profile, and the person can read and fix every line. A skill there does not load by itself, so it gets installed into the harness's skills folder, by the agent, after a yes (Ryan, 2026-11-06: symlinked or copied per the harness). `install_skill.py` checks the frontmatter and refuses the kit's own names.

Copy is the default. With a link, a later edit under `profile/`, which is on the allow list, changes the agent's instructions with no prompt and no new yes. A link suits someone running their own setup across harnesses, and takes `--link` and `--target`. The earlier idea, that the person promotes the file by hand, did not survive contact with the audience: Finder hides `.agents/`.

Say out loud which state it is in. A person who believes an uninstalled skill auto-loads is worse off than one with a plain note.

## A fifth skill, with a link from the brief

The first draft of this note had a fifth skill, the second a fork at the top of `builder-brief`. Ryan settled it as a fifth skill for now, with a link from `builder-brief` (2026-11-06). The fork's case was three shared steps, but W07 shows they are not shared in use: a job path may have no picked idea, cannot spend five gap questions, and needs a run before any writing, where the brief forbids running anything. What does carry over from the brief: the problem, must and must never, what it reads, and questions to settle. What does not: the simplest version, options, acceptance tests, and the builder notes. "Undo" becomes "what happens if this is wrong, and who notices".

## The two paths compose, and that is the best case

Ryan's point, and it deserves its own line: a skill can use a tool that was built. That makes the two paths a sequence rather than alternatives, and it is probably the most useful shape for a solo operator: build the small thing that does the arithmetic, then write the skill that runs it at the right moment and checks the result. Neither half is much use alone. The bill-checker nobody remembers to open, and the folder of advice about checking bills, are both worse than the two together.

The skill should say so, because it changes what the owner makes first: where a job has one step a small script would do perfectly, the honest advice is to build that, then write the skill around it.

## What our own skill practice already says

`skill-builder` is the house method for writing skills, and it has been through enough use to have hard-won rules. Five transfer to the owner's skill; the rest is Hermes machinery and should stay out of a kit a beginner reads.

**Transfers:**

1. **"The description is the skill's trigger mechanism."** It is the only advertisement the skill gets, and a description that summarises instead of naming the moment is the most common adoption failure. The test in `skill-builder` is the right one to teach: would a busy agent scanning a hundred descriptions recognise this one for the message the owner would actually send? Which means the description should carry the owner's own words for the job, not our summary of it.
2. **One skill per capability; a variation in audience or use is a reference file, not a new skill.** That is `skill-builder`'s Phase 0 gate, and it is the same conclusion as the fork-versus-fifth-skill argument above, arrived at from our own practice rather than from the D38 anecdote.
3. **Three parts, three jobs.** Deterministic work goes in a script: cheaper than tokens, faster than a model, and it cannot be talked out of the result. Detail needed on some runs goes in a reference, loaded on demand so the runs that skip it pay nothing. What every run needs stays in the body. The test is not the file count but which of the three a piece of content is. (Both meta-skills used to say "a great skill is a single SKILL.md with no scripts and no references", which contradicted `skill-builder`'s own cron section telling you to move workflows into `references/`. Corrected in both on 2026-11-06, after Ryan pushed back on it here.)
4. **"Ship v1.0.0 with the core procedure, then patch as pitfalls emerge."** This is the best thing to tell an owner: the first version is meant to be thin and wrong in small ways, and it improves by being used. It also removes the pressure to get it perfect in one sitting, which is what makes the exercise finishable in ten minutes.
5. **A copy on someone else's machine stops being updatable.** `skill-builder` states it for a CLI's instruction file and it applies exactly here: the owner's folder gets copied to a home computer, then a new one, then shared with a helper. So the skill carries a date, the procedure, and nothing that will be wrong in three months. **Prices, names, rates and addresses belong in `profile/`, and the skill reads them from there.** The rule in one line: the skill holds how the job is done, the profile holds what is true today.

**Does not transfer:** `SKILL_DIR`, toolset declarations, cron token budgets, version and platform frontmatter, the publish flow. None of it means anything to a piano teacher, and all of it turns the artifact into a configuration exercise.

The overlap is worth saying out loud in the room, because it is the same claim the workshop makes about everything else: the method we teach is the method we use. An owner who sees that their four example skills were written by the same process they are about to follow has learned something a definition cannot teach.

## How it runs

The steps are in the skill: check what is there, pick a job, do one real example step by step, read back the three lists, write the skill, install after a yes, then test in a new chat on a new case.

**The new chat is not optional.** The chat that did the run remembers every correction, so a pass there proves little. **The notes are saved as it goes**, in `drafts/teach-<name>.md`, because a run and its write-up may be split by a break or a closed laptop.

**The questions are the interesting column.** Most of a process was never written down, and putting a competent stranger in the chair is how you find the gaps. An interview gets the process they would describe, which is always tidier than the one they run.

**Rules that bend (Ryan, 2026-11-06).** A sick child, under 24 hours' notice: the policy says charged. Real teachers bend that, or don't, and it changes what kind of business they run. So the same question has to reach the assistant: do you want it to hold you to the rule, at some cost in goodwill, or bring those cases to you, at some cost in your time? The skill asks this directly and writes the answer down. It must not quietly soften the rule, which would be the assistant choosing kindness on the owner's behalf. See also D66, kinds of limit.

**Evidence marks** go on rules and stop lines, not on steps, which the person has already read back.

**Rules from `builder-brief` that had to change:** "one question per message" becomes one per stop, or it produces a questionnaire about the job; "no building" becomes drafts only, because the agent does run the job, inside `drafts/`. `builder-brief` has no Standin rule, and `share-safely`'s usual file sets do not include skills, so an owner sharing a profile with a skill in it should check that by hand.

## The word problem, inverted

The first draft argued against calling this a skill, on the grounds that it invites an owner to think they are configuring a product feature. Ryan's call outweighs that: "skill" is what the thing is, it is the word the owner will meet everywhere, and discovery is worth more than the purity.

What survives is smaller and still worth handling: the owner's folder now holds two kinds of skill, the kit's four and the owner's own. Say which is which once, and note that the kit's own four are the best example the owner has, because they can open one and see the shape.

## Not done yet

- **No model has run it.** Rehearsal cases still to write: a person who names a job; a job that touches a `limits.md` line; a run that produces a script; a run where the agent does the whole job in one message (the failure this design exists to prevent); a vague description that never loads; a named job with an existing profile (must not interview); a bending rule (must ask, must not soften).
- **Not confirmed:** that a copied skill is found by a new session in Claude Code and Codex, and whether the `.claude/skills` link carries it (D23).
- **Chat apps do not get it.** They have no install, so this path would stop at a pasted skill. Part 2 has room if that is wanted.
- **The name `builder-brief`** still fits, now that the job path is separate.
