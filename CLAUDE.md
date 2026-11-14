@../meta-eigenomar/standards/claude-ecosystem.md

# mortgager: Claude instructions

mortgager is a rent-or-buy calculator for the Dutch housing market. From a
price, a loan, rent and upfront costs, it builds an annuity mortgage's monthly
schedule and finds the months when buying beats renting, when selling turns a
profit, and when renting the home out pays off. It runs as a Flask app. It
also runs as a static page that executes the same Python in the browser with
Pyodide, and that page is deployed at mortgager.eigenomar.com.

## commands

Run them from the repository root. On Windows, type `python` where Linux uses
`python3`, since `python3` there is the Microsoft Store stub. In Windows
PowerShell, call a virtual environment's Python directly
(`.venv\Scripts\python`) instead of activating it, and type `npx.cmd` for
`npx`. Both `Activate.ps1` and `npx.ps1` are blocked by default.

- **setup:** `python -m venv .venv`, then
  `.venv\Scripts\python -m pip install -r requirements.txt` on Windows, or
  `.venv/bin/python -m pip install -r requirements.txt` on Linux.
- **run the server:** `python -m flask run`, with the environment's Python,
  then open http://127.0.0.1:5000. Or, with Docker running (Docker Desktop on
  Windows), run `docker compose up --build`.
- **build the static page:** `python build_static.py` writes `dist/`. Preview
  it with `python -m http.server -d dist` at http://localhost:8000. The first
  calculation downloads Pyodide from its CDN.
- **test:** there are no tests and no linter. A push to `main` deploys. So
  before pushing, check that `python build_static.py` succeeds, since
  Cloudflare's build runs it. Also check a calculation on the Flask app and on
  the static build's preview.

## plan

[docs/plan.md](docs/plan.md) is the plan's entry point. It holds the tickets
and the parked ideas. The app's feature ideas are the README's
[Dev Plan](README.md#dev-plan) list, which has no ids. An idea that becomes a
ticket moves into `docs/plan.md` with an id. Ticket ids are a lane prefix and
a number (EO1), and are never reused or renumbered. Each ticket has a stable
anchor above its heading: its id in lowercase. When work ships, update the
ticket's status in the index, add a result with the commit, and add a line to
the log. This repository is public, so confidential work never goes in the
plan or anywhere else here.

## design

- `src/` is the calculation. `mortgage.py` builds the schedule and the
  breakeven months. `conf.py` holds the Dutch rules' constants: the price limit
  for a first home, the transfer tax and the rental terms. `utils.py` holds the
  helpers. `api.py` parses the form and returns the response. Flask's
  `/calculate` calls `calculate()`, and the static page calls
  `calculate_json()` through Pyodide, so parsing and calculating live only
  there.
- `src/` uses only Python's standard library. The static build loads no
  packages into Pyodide, and `build_static.py` copies every `src/*.py` into
  `dist/`.
- `templates/index.html`, `static/styles.css` and `static/js/script.js` are
  the one page both ways use. `app.py` serves them through Flask.
  `build_static.py` copies them into `dist/` and injects a config and Pyodide's
  script before `script.js`. `script.js` then calculates in the browser instead
  of posting to `/calculate`. A change to the page must work both ways.
  `build_static.py` stops if it can't find
  `<script src="static/js/script.js"` in the template.
- `dist/` is generated and ignored. Change the sources and rebuild, never
  `dist/` itself. The Pyodide version is pinned in `build_static.py`
  (`PYODIDE_VERSION`).
- text files are LF in every checkout (`.gitattributes`, `.editorconfig`).

## delivery

- **CI:** none.
- **releases:** none: no tags or GitHub Releases.
- **deployment:** Cloudflare's build deploys every push to `main`. It runs
  `python3 build_static.py`, then `npx wrangler deploy`, which serves `dist/`
  as a Worker at mortgager.eigenomar.com (`wrangler.jsonc`). So pushing or
  merging to `main` is deploying. Only `dist/` is served, never the
  repository's other files. To deploy by hand, run `python build_static.py`,
  then `npx wrangler deploy`.
- the Docker image runs the Flask server locally. It isn't deployed.

## commits

You may commit on a working branch (`feature/…` or `bugfix/…`) once the work
is verified, and show the changed files, the checks' results and the commit
message with the commit. Never commit on `main`, and never push, merge,
release or deploy without the owner's approval: a push or merge to `main`
deploys. This grant covers only sessions started in this repository.
