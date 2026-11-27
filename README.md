# Mortgager

A program to calculate mortgage

## Run

Whatever build path you're choosing, you'll go to [`127.0.0.1:5000`](http://127.0.0.1:5000/)

The commands are written for macOS, Linux and WSL. On Windows, type `python` (or `py`) wherever they say `python3`, since `python3` there only opens the Microsoft Store.

### Native

Use your favourite OS to run Python natively.

```Shell
$ python3 -m pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
$ python3 -m flask run
```

### Virtual environment

```Shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python -m pip install --upgrade pip
$ python -m pip install -r requirements.txt
$ python -m flask run
```

On Windows, call the environment's Python directly instead of activating it, because PowerShell blocks `Activate.ps1` by default:

```PowerShell
> python -m venv .venv
> .venv\Scripts\python -m pip install --upgrade pip
> .venv\Scripts\python -m pip install -r requirements.txt
> .venv\Scripts\python -m flask run
```

### Docker

Make sure Docker is running (Docker Desktop on Windows and macOS).

```Shell
$ docker compose up --build
```

### Static (no server)

The same page, with the Python in `src/` running in the browser through [Pyodide](https://pyodide.org) instead of Flask. This is what's deployed at [mortgager.eigenomar.com](https://mortgager.eigenomar.com).

```Shell
$ python3 build_static.py
$ python3 -m http.server -d dist
```

Then go to [`localhost:8000`](http://localhost:8000/). The first calculation downloads the Python runtime, so it takes a few seconds.

## Deploy

The static build is served by Cloudflare Workers (see `wrangler.jsonc`). In the Cloudflare dashboard, import this repository under *Workers & Pages → Create → Import a repository* with:

- Build command: `python3 build_static.py`
- Deploy command: `npx wrangler deploy`

Every push to `main` then redeploys. To deploy from your machine instead, run `python3 build_static.py`, then `npx wrangler deploy` (`npx.cmd wrangler deploy` in Windows PowerShell, which blocks the `npx.ps1` script by default).

## Dev Plan

- Split the initial costs
  - Resources include and not exclusive to:
    - [resource1](https://www.hanno.nl/expat-mortgages/tax-return-and-homeownership-in-the-netherlands/)
    - [resource2](https://www.iamexpat.nl/housing/buy-house-netherlands/taxes-costs-fees)
    - [resource3](https://www.iamexpat.nl/housing/dutch-mortgages/fees-costs-tax-relief-netherlands)
- Add monthly charges (e.g., [for an actual property](https://huispedia.nl/eindhoven/5615pa/hoogstraat/39-03#finance))
- Add huispedia API integration
