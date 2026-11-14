# Mortgager: plan

This is the plan's entry point. It holds the repository's tickets and its
parked ideas. The app's feature ideas are the [Dev Plan](../README.md#dev-plan)
list in the README, which stays where it is. Its items have no ids, so they
aren't tickets yet. The only tickets so far are the ecosystem onboarding,
EO1–EO8.

## How this plan works

- **Tickets.** Every ticket has an id: a lane prefix and a number, which is
  never reused or renumbered. A split ticket keeps its number and adds a letter
  (EO6a, EO6b). Each ticket has a stable anchor above its heading, its id in
  lowercase (`#eo4`), which doesn't change when the heading does.
- **Lanes.**

  | prefix | lane |
  | --- | --- |
  | EO | ecosystem onboarding |

- **Each ticket** says what to do, what it needs, and when it is done. Its
  "done when" is its acceptance criteria. Size is a rough guess: S is small,
  M is medium.
- **Issues.** Every open ticket gets one GitHub issue in this repository. The
  issue's title starts with the ticket's id, and its body links the ticket's
  anchor here without copying it. The ticket holds the scope and history, and
  the issue holds status, priority and blockers ([EO8](#eo8)).
- **Adding work.** New work goes here as a ticket in a lane, with a new lane
  when none fits. An idea from the README's Dev Plan that becomes a ticket
  moves here with an id and leaves that list. An idea without an id stays in
  the Dev Plan or under [Parked](#parked), and has no issue. This repository is
  public, so confidential work never goes in this file. The ecosystem's shared
  rules, which `CLAUDE.md` imports, say where it goes.
- **When work ships,** update the ticket's status in the index, add a result
  with the commit to the ticket, and add a line to the [log](#log).

## Index

| ticket | title | size | needs | status |
| --- | --- | --- | --- | --- |
| [EO1](#eo1) | `project.yaml` | S | none | done |
| [EO2](#eo2) | `CLAUDE.md` with the shared rules | S | none | done |
| [EO3](#eo3) | the plan in this repository | S | none | done |
| [EO4](#eo4) | standing approval for commits | S | the owner's decision | todo |
| [EO5](#eo5) | what covers Linux | S | the owner's decision | todo |
| [EO6](#eo6) | a fresh install on Windows | S | none | todo |
| [EO7](#eo7) | Docker on Windows | S | none | todo |
| [EO8](#eo8) | an issue for every open ticket | S | the owner's approval | todo |

## Ecosystem onboarding

Mortgager is one of the eigenomar ecosystem's repositories, which share a
contract: a `project.yaml` manifest, shared Claude rules that `CLAUDE.md`
imports, and one issue per open ticket on the ecosystem's GitHub Project.

**Goal.** Make mortgager discoverable and coordinated in the ecosystem without
changing how it is built or delivered.

**Stays as it is.**

- **build:** `python build_static.py` builds the static page into `dist/`.
  The Flask app needs no build.
- **tests:** none, and no linter.
- **CI:** none.
- **branching:** feature and bugfix branches (`feature/…`, `bugfix/…`) merged
  into `main`, and small changes committed straight to `main`.
- **releases:** none: no tags or GitHub Releases.
- **deployment:** Cloudflare's build deploys every push to `main`. It runs
  `python3 build_static.py`, then `npx wrangler deploy`, and serves `dist/` as
  a Worker at mortgager.eigenomar.com. It serves only `dist/`, so
  `project.yaml`, `CLAUDE.md` and this plan aren't part of it.
- **documents:** the README's Run, Deploy and Dev Plan sections, where they
  are.

**Portability, checked on 2026-11-14.** The checks ran on Windows, with the
machine's Python 3.11 and Flask 2.3.3, started once from `c:\` and once from
`C:\`. Every check passed both times:

- `python -m flask run` serves the page, its stylesheet and a calculation.
- Flask's test client gets the same results, and rejects a price that isn't a
  number.
- `python build_static.py` builds the same `dist/` from both spellings, with
  LF only.
- `dist/src/api.py` returns the same calculation when it's called the way the
  browser calls it.

No script is shell-only, no path is absolute, and the only dependency, Flask,
is pure Python. All 18 tracked files are LF in the index, under
`.gitattributes`. Not checked: a fresh install from `requirements.txt` and the
static page in a browser (EO6), and Docker (EO7).

There is no CI. Linux is covered by Cloudflare's build, which runs
`build_static.py` on Linux for every push to `main`, and by the Docker image,
which runs the server on Linux. No test checks a calculation on either system
(EO5).

### Steps

Each step is small and independent, and can be done between other work.

<a id="eo1"></a>

#### EO1 · `project.yaml` · done

- **done when:** a manifest at the root points at the documents that exist,
  and the ecosystem's validator passes it.
- **result:** done 2026-11-14. It points at this plan and the README's Dev
  Plan, at `CLAUDE.md`'s design section, and at the README's Run and Deploy
  sections. It records no CI and no releases, and Cloudflare deploying every
  push to `main`. Its status is `active`. Update it in the same change that
  moves or adds a document it names.

<a id="eo2"></a>

#### EO2 · `CLAUDE.md` with the shared rules · done

- **done when:** the first line of `CLAUDE.md` imports the ecosystem's shared
  rules. Without that import, the file and the files it names are still enough
  to set up, run, build and deploy the project.
- **result:** done 2026-11-14. It was created from the ecosystem's template,
  with the commands, the plan, the design and the delivery. It grants no
  standing approval for commits ([EO4](#eo4)).

<a id="eo3"></a>

#### EO3 · the plan in this repository · done

- **done when:** this file exists with the onboarding steps, `project.yaml`
  names it, and [how this plan works](#how-this-plan-works) says that
  confidential work never goes in this file.
- **result:** done 2026-11-14. The README's Dev Plan stays where it is, as the
  owner chose. Nothing in the repository is confidential (the owner,
  2026-11-14), so nothing moved. [Parked](#parked) holds one idea, the
  calculation's visualizations.

<a id="eo4"></a>

#### EO4 · standing approval for commits · todo

- **do:** the owner decides whether Claude sessions started in this repository
  may commit on a working branch once their work is verified. Sessions have
  committed here before: the static build and its merge, on 2026-10-04. A
  grant is never inferred from that. If the owner grants it, add a "commits"
  section to `CLAUDE.md` with the ecosystem template's wording. That wording
  never covers `main`, or a push, merge, release or deployment. See
  [open question 1](#open-questions).
- **needs:** the owner's decision.
- **done when:** `CLAUDE.md` states the grant, or this ticket's result records
  that there is none.

<a id="eo5"></a>

#### EO5 · what covers Linux · todo

- **do:** there is no CI. Cloudflare's build runs `build_static.py` on Linux
  for every push to `main`, and the Docker image runs the server on Linux. But
  nothing checks a calculation on either system. Decide whether this plan
  accepts that gap, or whether a ticket adds a check, such as a test of
  `src/api.py` that CI runs on Linux. Adding CI changes the delivery, so it
  would be its own ticket. See [open question 2](#open-questions).
- **needs:** the owner's decision.
- **done when:** this plan says what covers Linux and which gap it accepts, or
  names the ticket that closes the gap.

<a id="eo6"></a>

#### EO6 · a fresh install on Windows · todo

- **do:** the onboarding run checked the code with the Flask 2.3.3 already on
  the machine, and installed nothing. `requirements.txt` pins Flask 2.3.2 and
  nothing else. So a fresh install also takes the newest Werkzeug, Jinja and
  click releases that Flask 2.3.2 allows. On Windows, follow the README's
  virtual environment section into a new `.venv`, then its static section.
  Do it once from `c:\` and once from `C:\`, as the ecosystem's portability
  conventions describe. If something fails, the fix is its own change, such as
  pinning the dependency that broke.
- **needs:** nothing.
- **done when:** in a new virtual environment on Windows, started from `c:\`
  and from `C:\`:
    - `python -m flask run` serves the page and a calculation at
      http://127.0.0.1:5000.
    - the static build's preview at http://localhost:8000 calculates in a
      browser.

<a id="eo7"></a>

#### EO7 · Docker on Windows · todo

- **do:** Docker Desktop is installed with its WSL 2 backend, and
  `docker compose config` reads `compose.yaml` on Windows. But Docker Desktop
  wasn't running during the onboarding run, so the image wasn't built. Start
  Docker Desktop and run `docker compose up --build`, as the README says.
- **needs:** nothing.
- **done when:** on Windows, `docker compose up --build` builds the image and
  serves the page and a calculation at http://127.0.0.1:5000.

<a id="eo8"></a>

#### EO8 · an issue for every open ticket · todo

- **do:** open one issue in this repository for every open ticket (EO4–EO7 on
  2026-11-14), and add each one to the ecosystem's GitHub Project. The title is
  `<id>: <title>`, as in `EO6: a fresh install on Windows`. The body's first
  line links the ticket's anchor on `main` and copies nothing. None of them
  needs another, so there are no blocked-by links. EO4 and EO5 wait on
  decisions, so their issues stay `backlog` until those are made. The proposed
  priority is P2 for each ([open question 3](#open-questions)).
- **needs:** the owner's approval. This repository is public, so the owner
  sees each issue's text before it is written.
- **done when:** every open ticket has exactly one issue in the Project, with
  its status, priority and work type set.

### Open questions

1. **EO4, standing approval for commits:** grant it or not? Recommended: grant
   it. Work here already goes through feature branches, and merging into
   `main`, which deploys, stays the owner's step.
2. **EO5, Linux:** accept the gap, or add a test? Recommended: accept it for
   now. Cloudflare's Linux build runs on every push. Add a test of
   `src/api.py` with the next ticket that changes the calculation.
3. **EO8's priorities:** P2 for each of EO4–EO7? Recommended: yes.
4. **status:** `project.yaml` says `active`, because the Dev Plan holds
   features still to build. Should it be `maintenance` instead, which means
   fixes and small changes only? Recommended: `active`.
5. **GitHub's description:** it reads "a program to calculate mortgage", with
   no homepage. Should it take `project.yaml`'s description, with
   https://mortgager.eigenomar.com as the homepage? Recommended: yes.

## Parked

Ideas without an id. Each one becomes a ticket, with an id, when it's picked
up.

- **Visualizations of the calculation:** amortization, equity, rent vs buy,
  and rate sensitivity. They reuse the calculation in `src/`, and keep its
  assumptions visible.

## Log

- 2026-11-14 · plan · Created by the ecosystem onboarding run, with EO1–EO8.
  EO1–EO3 are done: `project.yaml`, which validates, `CLAUDE.md` with the
  shared rules, and this plan, which links the README's Dev Plan and parks
  the visualizations idea. EO4 and EO5 wait on the owner's decisions. EO6 and
  EO7 are the Windows checks the run couldn't do without installing or
  starting anything, and EO8 opens their issues. Nothing else in the
  repository changed.
