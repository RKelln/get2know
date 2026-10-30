# Governance

How Get2Know and the capability commons are run, who decides what, and how the work of the maintenance agents is checked. **Status: proposed, 2026-10-29.** Decided so far (with Ryan, 2026-10-29): the project is hosted under a non-profit, and commons records are CC0. Everything else here is a proposal for Ryan to accept or change.

## The host

A **non-profit organization** holds the project: the code repository, the commons, any money (grants, donations, sponsors), the accounts the scheduled agents run under, and the trademark if there is one. Which non-profit is still to be named. Its job is to keep the project open and independent of any one company, including AI companies and the makers of tools listed in the commons.

## Roles

| Role | Who | Does |
|---|---|---|
| **Lead** | Ryan, to start | sets direction; final say when the steering group cannot agree; names the first maintainers and approvers |
| **Steering group** | the lead plus 2 to 4 maintainers, when there are enough people | sets priorities, ranks gaps monthly, adds and removes maintainers and approvers |
| **Maintainers** | named in this file | review and merge pull requests in their area (code, skill text, commons) |
| **Reviewers** | anyone with a few accepted contributions, invited by a maintainer | skim the daily commons digest and review level 0 to 2 records |
| **Level-3 approvers** | short list, below | approve the first listing of a vetted tool |
| **Contributors** | anyone | send code, words, records, stories and gaps |
| **Code of conduct contacts** | at least two people, named by the lead | receive and act on reports (see `CODE_OF_CONDUCT.md`) |

Current lists *(proposed: Ryan to confirm)*:
- Lead: Ryan Kelln *(proposed)*.
- Maintainers: Ryan Kelln *(proposed)*.
- Level-3 approvers: Ryan Kelln *(proposed)*.
- Code of conduct contacts: to be named.

## How decisions are made

1. **Small changes** (fixes, records, wording): one maintainer reviews and merges.
2. **Design changes** (how the interview works, the record format, the ladder): written up in `docs/DESIGN.md` with the reason, open for comment for at least a week, then the lead or the steering group decides. "We tried it in rehearse and here is what happened" counts for more than opinions.
3. **People** (adding or removing maintainers and approvers): the steering group, by agreement; if it cannot agree, the lead decides.
4. **Safety removals** (a tool turns out unsafe, a record leaks something private): any maintainer or approver acts at once, then explains in the issue.

Decisions and their reasons are public, in issues and `docs/DESIGN.md`, except for code of conduct reports and anything about a private person.

## How the agents' work is reviewed

The commons is tended by scheduled agents (scout, triage, prover, vetter, describer, gardener; see `docs/capability-commons.md`). Their output is treated like any contributor's, with more limits:

- **Agents never merge to the main branch on their own**, except for fact refreshes (dates, release numbers, the archived flag) that pass `commons/check.py`. Everything else is a pull request a person reviews.
- **Each run leaves a log**: what it looked at, what it changed, what it cost. Logs are kept so a reviewer can see why a record says what it says.
- **A daily digest** lists the agents' pull requests, grouped by how much review each needs (see the table in `CONTRIBUTING.md`). Reviewers work through it; anything nobody reviews stays `found` and is never shown to an owner.
- **The queue has a cap.** The agents only open as many pull requests as reviewers can read in a week. If the queue is full, they stop and wait. Review time is the limit by design.
- **Spending has a cap.** Each agent has a monthly budget set by the steering group; it stops when the budget is spent.
- **Agents' text is checked like untrusted text.** An agent that read a third-party README may have been misled by it. Reviewers check that a record is in plain words of our own and contains no instructions aimed at an AI.
- **Decision models** (narrow yes/no answers, see the proposal) are trusted for a question only after they are scored on a hand-labelled test set for that question. Low-confidence answers go to a person.
- **Vetting reports from owners' AIs** *(proposed, see "Distributed vetting" in `docs/capability-commons.md`)* are untrusted contributions. One report never vets a tool; reports from the tool's submitter or makers do not count; a level-3 approver still approves the first listing. How to resist fake or colluding vetters is an open problem.
- **Quarterly check:** the steering group samples some agent-merged and agent-proposed records, checks them by hand, and publishes the error rate. If it rises, the agents get more review, not less.

## Money and conflicts of interest

- Money goes through the host non-profit, and what it pays for is published.
- Anyone who makes, sells, or is paid by a tool says so before reviewing or approving that tool's record, and steps aside.
- Sponsors cannot buy a listing, a better place in matching, or a say over records.

## Changing this document

By the design-change process above. Until the steering group exists, the lead decides, and records the reason in `docs/DESIGN.md`.
