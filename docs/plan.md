# Mortgager: plan

This is the plan's entry point. It holds the repository's tickets and its
parked ideas. The app's feature ideas are the [Dev Plan](../README.md#dev-plan)
list in the README, which stays where it is. Its items have no ids, so they
aren't tickets yet. The ecosystem onboarding, EO1–EO8, was done on
2026-11-14, and [UI1](#ui1), a modern look for the calculator, and
[UI2](#ui2), the ecosystem's tab icon, on 2026-11-24, and [UI3](#ui3), the
footer's link to eigenomar.com, and [UI4](#ui4), the lowercase page, on
2026-11-27. The open tickets are
[DOC5](#doc5) and [SCM5](#scm5), which adopt the ecosystem's standards, and
[MIG5](#mig5), which moves this plan's tickets into their GitHub issues.

## How this plan works

- **Tickets.** Every ticket has an id: a lane prefix and a number, which is
  never reused or renumbered. A split ticket keeps its number and adds a letter
  (EO6a, EO6b). Each ticket has a stable anchor above its heading, its id in
  lowercase (`#eo4`), which doesn't change when the heading does.
- **Lanes.**

  | prefix | lane |
  | --- | --- |
  | EO | ecosystem onboarding |
  | UI | the page: how it looks and how it's used |
  | DOC | the product's documents: vision, architecture, design, testing strategy, and verification and validation |
  | SCM | source control and delivery: CI, branching, protection, releases and versioning |
  | MIG | the backlog moves into GitHub issues: the cutover to GitHub as its home |

- **Each ticket** says what to do, what it needs, and when it is done. Its
  "done when" is its acceptance criteria. Its size is on the ecosystem's
  scale, the same value as its issue's `Size` in the ecosystem's GitHub
  Project: xxs takes minutes, xs under an hour, s an hour or two, m about a
  session, l two or three, xl four to six and xxl more. tbd means an open
  decision or work not yet planned decides it. A change to one is made to the
  other in the same session.
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
| [EO1](#eo1) | `project.yaml` | s | none | done |
| [EO2](#eo2) | `CLAUDE.md` with the shared rules | s | none | done |
| [EO3](#eo3) | the plan in this repository | s | none | done |
| [EO4](#eo4) | standing approval for commits | s | the owner's decision | done |
| [EO5](#eo5) | what covers Linux | s | the owner's decision | done |
| [EO6](#eo6) | a fresh install on Windows | s | none | done |
| [EO7](#eo7) | Docker on Windows | s | none | done |
| [EO8](#eo8) | an issue for every open ticket | s | the owner's approval | done |
| [UI1](#ui1) | a modern look for the calculator | m | none | done |
| [UI2](#ui2) | the ecosystem's tab icon | xs | none | done |
| [UI3](#ui3) | a footer link to eigenomar.com | xs | none | done |
| [UI4](#ui4) | the page in lowercase | xs | none | done |
| [DOC5](#doc5) | the product's documents | tbd | `meta-eigenomar` ST1 | open |
| [SCM5](#scm5) | the ecosystem's SCM strategy | tbd | `meta-eigenomar` ST2 | open |
| [MIG5](#mig5) | the backlog moves into GitHub issues | xs | `meta-eigenomar` ST3 | open |

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
`.gitattributes`. A fresh install from `requirements.txt`, the static page in a
browser (EO6) and Docker (EO7) were checked the same day, from both
spellings, and pass.

There is no CI. Linux is covered by Cloudflare's build, which runs
`build_static.py` on Linux for every push to `main`, and by the Docker image,
which runs the server on Linux. No test checks a calculation on either system,
a gap the owner accepts for now (EO5).

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
  moves or adds a document it names. `68a3549`.

<a id="eo2"></a>

#### EO2 · `CLAUDE.md` with the shared rules · done

- **done when:** the first line of `CLAUDE.md` imports the ecosystem's shared
  rules. Without that import, the file and the files it names are still enough
  to set up, run, build and deploy the project.
- **result:** done 2026-11-14. It was created from the ecosystem's template,
  with the commands, the plan, the design and the delivery. It granted no
  standing approval for commits until [EO4](#eo4). `68a3549`.

<a id="eo3"></a>

#### EO3 · the plan in this repository · done

- **done when:** this file exists with the onboarding steps, `project.yaml`
  names it, and [how this plan works](#how-this-plan-works) says that
  confidential work never goes in this file.
- **result:** done 2026-11-14. The README's Dev Plan stays where it is, as the
  owner chose. Nothing in the repository is confidential (the owner,
  2026-11-14), so nothing moved. [Parked](#parked) holds one idea, the
  calculation's visualizations. `68a3549`.

<a id="eo4"></a>

#### EO4 · standing approval for commits · done

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
- **result:** done 2026-11-14. The owner granted it: `CLAUDE.md`'s "commits"
  section lets a session started here commit on a working branch once its work
  is verified, and never on `main`. Pushing, merging, releasing and deploying
  stay the owner's, and a push or merge to `main` deploys.

<a id="eo5"></a>

#### EO5 · what covers Linux · done

- **do:** there is no CI. Cloudflare's build runs `build_static.py` on Linux
  for every push to `main`, and the Docker image runs the server on Linux. But
  nothing checks a calculation on either system. Decide whether this plan
  accepts that gap, or whether a ticket adds a check, such as a test of
  `src/api.py` that CI runs on Linux. Adding CI changes the delivery, so it
  would be its own ticket. See [open question 2](#open-questions).
- **needs:** the owner's decision.
- **done when:** this plan says what covers Linux and which gap it accepts, or
  names the ticket that closes the gap.
- **result:** done 2026-11-14. The owner accepts the gap for now: Linux is
  covered by Cloudflare's build, which runs `build_static.py` on every push to
  `main`, and by the Docker image, which runs the server (checked in EO7), but
  nothing checks a calculation there. The next ticket that changes the
  calculation adds a test of `src/api.py`.

<a id="eo6"></a>

#### EO6 · a fresh install on Windows · done

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
- **result:** done 2026-11-14, in a throwaway virtual environment outside the
  repository, made with the README's commands. It took Flask 2.3.2 with
  Werkzeug 3.1.9, Jinja2 3.1.6 and click 8.5.1, the newest the pin allows,
  and nothing broke, so no pin is needed. From `c:\` and from `C:\`, the
  server served the page, its stylesheet and a calculation, and the static
  build's preview calculated in headless Edge through Pyodide. Both gave the
  same breakeven months for the page's default inputs: 53, 22, and none for
  renting out. `dist/` and the environment were deleted afterwards.

<a id="eo7"></a>

#### EO7 · Docker on Windows · done

- **do:** Docker Desktop is installed with its WSL 2 backend, and
  `docker compose config` reads `compose.yaml` on Windows. But Docker Desktop
  wasn't running during the onboarding run, so the image wasn't built. Start
  Docker Desktop and run `docker compose up --build`, as the README says.
- **needs:** nothing.
- **done when:** on Windows, `docker compose up --build` builds the image and
  serves the page and a calculation at http://127.0.0.1:5000.
- **result:** done 2026-11-14 with Docker Desktop's engine 24.0.6. From `c:\`
  and from `C:\`, `docker compose up --build` built the image, and the
  container served the page, its stylesheet and the same calculation as EO6
  (53, 22, none). The container and image were removed afterwards.

<a id="eo8"></a>

#### EO8 · an issue for every open ticket · done

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
- **result:** done 2026-11-14 with no issues: EO4–EO7 were done at once, as
  the owner chose, so no ticket is open. A ticket added later gets its issue
  when it's added.

### Open questions

All answered by the owner on 2026-11-14:

1. **EO4, standing approval for commits:** granted, on working branches
   ([EO4](#eo4)).
2. **EO5, Linux:** the gap is accepted for now, and the next ticket that
   changes the calculation adds a test of `src/api.py` ([EO5](#eo5)).
3. **EO8's priorities:** not needed, since EO4–EO7 were done at once and have
   no issues.
4. **status:** `active`.
5. **GitHub's description:** `project.yaml`'s, with
   https://mortgager.eigenomar.com as the homepage.

## The page

The page works, but it looks like a bare form: inputs in one long column,
three breakeven lines, a 3-decimal table and `alert()` for errors. This lane
makes it look and behave like a tool.

**Stays as it is,** for every ticket in this lane:

- the calculation in `src/`, and what the page sends it: the same field ids,
  values and defaults, which `src/api.py` parses.
- one page for both ways: `templates/index.html`, `static/styles.css` and
  `static/js/script.js`, used by Flask and copied by `build_static.py`, with
  `<script src="static/js/script.js"` still in the template.
- plain HTML, CSS and JavaScript: no framework, no build step, and no new
  dependency or external script, stylesheet or font. Pyodide stays the only
  thing loaded from a CDN.

A ticket here doesn't change the calculation, so it doesn't need the test of
`src/api.py` that [EO5](#eo5) asks of the next ticket that does.

### Tickets

<a id="ui1"></a>

#### UI1 · a modern look for the calculator · done

- **do:** restyle the page as a calculator tool:
    - **inputs** grouped in labelled sections, such as the home and the loan,
      the buyer, renting, upfront costs and renting out, with aligned labels
      and their units (€, %, months) beside each field, and a `<form>` so
      Enter calculates.
    - **results:** the three breakeven months as cards above the schedule,
      each with a short line on what it means, and "none" instead of `NA`
      when a month isn't reached.
    - **the schedule:** euro amounts with thousands separators and two
      decimals, a header that stays in view while it scrolls, and its own
      scroll box, so a narrow screen doesn't scroll the page sideways.
    - **states:** an error shown in the page instead of an `alert()`, and a
      loading state while the static page downloads Python on its first
      calculation.
    - **layout and theme:** inputs beside the results on a wide screen,
      stacked on a phone, and light and dark themes that follow the system
      setting.
- **not in it:** the footer link to eigenomar.com and the other items in the
  README's [Dev Plan](../README.md#dev-plan), the [visualizations](#parked),
  and new inputs. Each stays where it is until it's picked up.
- **needs:** nothing.
- **done when,** on the Flask app and on the static build's preview:
    - the default inputs give the same breakeven months as [EO6](#eo6): 53,
      22, and none for renting out.
    - at 375 px wide, the page doesn't scroll sideways, and the schedule
      scrolls inside its own box.
    - light and dark follow the system setting, and body text in both has a
      contrast of at least 4.5:1 (WCAG AA).
    - every input has a visible label and unit. By keyboard alone, Tab reaches
      every field and the button, focus is visible, and Enter calculates.
    - an empty price shows `src/api.py`'s error in the page, with no dialog.
      The static page's first calculation shows the loading state.
    - the schedule's amounts have thousands separators and two decimals.
    - `python build_static.py` succeeds, and `requirements.txt` and the
      template's external scripts and stylesheets are unchanged.
- **result:** done 2026-11-24, on `feature/ui1-modern-look`, in
  `templates/index.html`, `static/styles.css` and `static/js/script.js`
  only. The inputs are in five fieldsets with their units, inside a
  `<form>`. The breakeven months are cards that also give years and months,
  and "none" when a month isn't reached. The schedule is a table with a
  sticky header and month column, in its own scroll box. Errors and the
  loading state show in the page, and the colours are eigenomar.com's, light
  and dark. When the price is too high for a first home, the schedule area
  says so. Every "done when" was checked in headless Edge, on the Flask app
  and the static build's preview, in light and dark: 53, 22 and none; a
  375 px page that doesn't scroll sideways; 15 controls reached by Tab with
  focus visible; `src/api.py`'s error for an empty price, with no dialog;
  and the loading state on the static page's first calculation. Body and
  muted text measure at least 5.37:1 in both themes. `9bc179e`, merged
  in `84f65db` and deployed the same day, where the same checks pass at
  mortgager.eigenomar.com.

<a id="ui2"></a>

#### UI2 · the ecosystem's tab icon · done

- **do:** every app under eigenomar.com shows the same tab icon:
  eigenomar.com's lambda with its two colors swapped, a light-blue tile and a
  near-black lambda (shared decision SD5). The page has none today. Add it as
  `static/favicon.svg`, and link it from `templates/index.html` with
  `<link rel="icon" type="image/svg+xml" href="static/favicon.svg">`, a
  relative path like the stylesheet's. Flask serves it from `static/`, and
  `build_static.py` already copies that folder into `dist/`, so neither
  changes.
- **needs:** nothing. It touches one line of the template, so it fits before,
  after or inside [UI1](#ui1).
- **done when:** the tab shows the icon on the Flask app, on the static
  build's preview and at mortgager.eigenomar.com, in a light and a dark
  browser theme, and `python build_static.py` succeeds.
- **result:** done 2026-11-24, after [UI1](#ui1): `static/favicon.svg` is
  the SVG of shared decision SD5, byte for byte, and `templates/index.html`
  links it. `python build_static.py` copies it into `dist/` unchanged. In
  headless Edge, in light and dark, the Flask app, the static build's
  preview and mortgager.eigenomar.com all resolve the page's icon link and
  serve it as `image/svg+xml` with the same bytes, and it renders. Headless
  Edge has no tab strip, so the tab itself is left to the eye. `a4a086f`,
  merged in `84f65db`.

<a id="ui3"></a>

#### UI3 · a footer link to eigenomar.com · done

- **do:** add a footer after the page's `<main>` in `templates/index.html`,
  with a button-like link to [eigenomar.com](https://eigenomar.com) that opens in the same
  tab, as the README's Dev Plan item asked. The ecosystem's other apps have
  the same "eigenomar.com" button in their footers.
- **needs:** nothing.
- **done when:** on the Flask app and the static build, the footer's link
  shows below the inputs and results in light and dark, goes to
  eigenomar.com in the same tab, and doesn't make a 375 px page scroll
  sideways. `python build_static.py` succeeds.
- **result:** done 2026-11-27, on `feature/ui3-ui4-footer-lowercase`, in
  `templates/index.html` and `static/styles.css`. The link has the
  Calculate button's shape but is quiet, a surface fill with a border and
  the accent's text, so Calculate stays the page's one filled button. The
  item left the README's Dev Plan. Checked with [UI4](#ui4).

<a id="ui4"></a>

#### UI4 · the page in lowercase · done

- **do:** show the page's text in lowercase, as eigenomar.com does: the
  heading, legends, labels, units, cards, the schedule's headers, the
  button, the rental options, and the status and error messages. The
  schedule's headers and the error come from `src/`, which stays as it is,
  so a CSS rule lowercases them, as eigenomar.com's and selecta's do, and the
  `<title>`, which CSS doesn't reach, is written lowercase. Nothing on the
  page needs its case kept: it has no acronyms, and the inputs are numbers.
- **needs:** nothing.
- **done when:** on the Flask app and the static build, in light and dark,
  every text on the page and the tab's title show in lowercase, the default
  inputs still give 53, 22 and none, and `python build_static.py` succeeds.
- **result:** done 2026-11-27, on `feature/ui3-ui4-footer-lowercase`, in
  `templates/index.html` and `static/styles.css`. `body` has
  `text-transform: lowercase`, and `button`, `select` and `option` take it
  too, since the browser's own stylesheet resets them. The cards' headings
  lost their uppercase. In headless Edge on the Flask app, at 1280 and
  375 px in light and dark: the title, heading, legends, button, rental
  options, cards, schedule headers and status are lowercase; 53, 22 and
  none; an empty price shows "invalid input. please enter valid numbers."
  in the page; the footer's link goes to eigenomar.com with no target; and
  no width scrolls sideways. The static build's stylesheet is the same
  file, and its page differs from the template only by the two script lines
  `build_static.py` injects. The static preview wasn't opened in a browser
  this time.

## Ecosystem standards

The ecosystem's contract, in `meta-eigenomar`, is adding two standards that
every repository adopts: the documents each one keeps, and how each one
manages its source and delivers it. DOC5 and SCM5 adopt them here, each once
its standard is designed. Until then, their issues stay in the backlog.

A third standard, `meta-eigenomar` ST3, makes GitHub's issues the home of
every repository's backlog, and its decisions were made on 2026-11-27. MIG5
moves this plan's tickets there, once ST3 is built.

### Tickets

<a id="doc5"></a>

#### DOC5 · the product's documents · open

- **do:** write this repository's product vision, architecture, design,
  testing strategy, and verification and validation (V&V) documents, in the
  shape the ecosystem's document standard sets. Where a file or section
  already covers one, name it rather than copy it. Today there is no vision
  beyond the README's first line, `CLAUDE.md`'s design section is the
  architecture, and there are no tests: [EO5](#eo5) accepts that gap until the next ticket
  that changes the calculation adds a test of `src/api.py`. [EO6](#eo6)'s
  breakeven months, 53, 22 and none, are the one recorded check of the
  calculation.
- **needs:** the ecosystem's document standard (`meta-eigenomar` ST1).
- **done when:** each of the five documents exists, or names the file or
  section that holds it, and follows the standard's outline. `project.yaml`
  names them under the standard's keys, and the ecosystem's validator passes.
  Nothing in them is confidential, since this repository is public.

<a id="scm5"></a>

#### SCM5 · the ecosystem's SCM strategy · open

- **do:** adopt the ecosystem's SCM strategy through its adoption checklist:
  CI, branching, protection of `main`, versioning and releases, the health
  report and dependency updates. Today there is no CI or release, Cloudflare's
  build deploys every push to `main`, and sessions commit on `feature/…` and
  `bugfix/…` branches under [EO4](#eo4)'s standing approval.
- **needs:** the ecosystem's SCM strategy (`meta-eigenomar` ST2).
- **done when:** every item on the checklist is applied here, or recorded here
  as an exception the strategy allows, with its reason. `project.yaml`'s
  `delivery` and `CLAUDE.md` say what runs, any workflow passes on `main`, and
  the ecosystem's validator passes.

<a id="mig5"></a>

#### MIG5 · the backlog moves into GitHub issues · open

- **do:** move this plan's planning to GitHub all at once, following the
  cutover steps of the ecosystem's standard `meta-eigenomar` ST3. Each open
  ticket's content moves into its issue's body, keeping its id and its issue's
  `<id>: <title>`. [Parked](#parked)'s ideas and the README's [Dev
  Plan](../README.md#dev-plan) list become draft items in the Project with
  status `idea`, hard needs are blocked-by links, and size, status and
  priority live only in the Project. Done, dropped and moved tickets stay here
  as a frozen archive, and each open ticket's anchor stays, linking its issue.
- **needs:** GitHub as the home of the backlog (`meta-eigenomar` ST3), which
  includes the ecosystem's own cutover first and the backlog's backup. DOC5 is
  a planning need: the plan's direction moves into the vision before this plan
  retires.
- **done when:** every open ticket's content is in its issue, and this file
  holds only the archive and the anchors. `project.yaml`'s `documents.plan` is
  `null` and `planning.source` names GitHub, the ecosystem's validator passes,
  nothing confidential is in any issue, since this repository is public, and
  the owner approved the cutover. Bringing tickets up to the ecosystem's
  ticket standard (`meta-eigenomar` ST4) isn't part of it: each ticket follows
  it when it is picked up.

## Parked

Ideas without an id. Each one becomes a ticket, with an id, when it's picked
up.

- **Visualizations of the calculation:** amortization, equity, rent vs buy,
  and rate sensitivity. They reuse the calculation in `src/`, and keep its
  assumptions visible.

## Log

- 2026-11-27 · UI3, UI4 · Added and done at the owner's request, from a
  session in `meta-eigenomar`, on `feature/ui3-ui4-footer-lowercase`: a
  footer link to eigenomar.com, which left the README's Dev Plan, and the
  page's text in lowercase, as eigenomar.com's. Done at once, so neither has
  an issue. Nothing in `src/` changed. Checked on the Flask app.
- 2026-11-27 · MIG5 · Added, in a new lane, at the owner's request: this
  repository's cutover to GitHub as the home of its backlog, the ecosystem's
  standard `meta-eigenomar` ST3, whose decisions were made that day. It needs
  ST3, so its issue waits as `blocked`.
- 2026-11-26 · DOC5, SCM5 · Renamed from `DOC1` and `SCM1`, since the
  ecosystem's lanes are numbered across its repositories. Their anchors,
  headings, index rows and issues changed with them, and the log keeps the ids
  it was written with.
- 2026-11-24 · UI1, UI2 · Merged in `84f65db` and deployed. The UI1 checks
  and the icon pass at mortgager.eigenomar.com, and both issues are closed.
- 2026-11-24 · UI2 · Built on `feature/ui1-modern-look`, `a4a086f`: the
  ecosystem's tab icon (shared decision SD5) as `static/favicon.svg`, linked
  from the template, and served both ways.
- 2026-11-24 · UI1 · Done on `feature/ui1-modern-look`, `9bc179e`: the page restyled
  as a calculator tool, with grouped inputs and units, breakeven cards, a
  formatted schedule in its own scroll box, in-page errors and loading, and
  light and dark themes. Nothing in `src/` changed. Checked on the Flask app
  and the static build.
- 2026-11-20 · UI2 · Added at the owner's request: every app under
  eigenomar.com shares one tab icon, eigenomar.com's lambda with its colors
  swapped (shared decision SD5). The page has none, so UI2 adds it.
- 2026-11-18 · DOC1, SCM1 · Added, in two new lanes, at the owner's request:
  this repository's adoption of the ecosystem's document standard and SCM
  strategy, which are designed in `meta-eigenomar`. Each needs its standard,
  so its issue waits in the backlog.
- 2026-11-15 · UI1 · Added, in a new lane for the page, UI: a modern look for
  the calculator, with the page's layout, results, schedule, errors, loading
  and themes, and nothing in `src/`. It needs nothing.
- 2026-11-14 · EO4–EO8 · Done, as the owner chose. EO4: `CLAUDE.md` grants
  standing approval for commits on working branches. EO5: the plan accepts
  that nothing checks a calculation on Linux, for now. EO6: a fresh install in
  a throwaway environment, with the newest Werkzeug the pin allows, serves and
  calculates from `c:\` and `C:\`, on the server and in a browser. EO7:
  `docker compose up --build` serves the page and a calculation from both
  spellings. EO8 needs no issues, since nothing is open. EO1–EO3's results
  name `68a3549`. The ecosystem onboarding is complete.
- 2026-11-14 · plan · Created by the ecosystem onboarding run, with EO1–EO8.
  EO1–EO3 are done: `project.yaml`, which validates, `CLAUDE.md` with the
  shared rules, and this plan, which links the README's Dev Plan and parks
  the visualizations idea. EO4 and EO5 wait on the owner's decisions. EO6 and
  EO7 are the Windows checks the run couldn't do without installing or
  starting anything, and EO8 opens their issues. Nothing else in the
  repository changed.
