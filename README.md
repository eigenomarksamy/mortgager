# Mortgager

A program to calculate mortgage

## Run

Whatever build path you're choosing, you'll go to [`127.0.0.1:5000`](http://127.0.0.1:5000/)

### Native

Use your favourite OS to run python3 natively.

```Shell
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ python3 -m flask run
```

### Virtual environment

Use your favourite OS to run virtual environment.

```Shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ python3 -m flask run
```

### Docker (Windows - WSL)

Make sure the Docker windows up is running.

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

Every push to `main` then redeploys. To deploy from your machine instead: `python3 build_static.py && npx wrangler deploy`.

## Dev Plan

- Split the initial costs
  - Resources include and not exclusive to:
    - [resource1](https://www.hanno.nl/expat-mortgages/tax-return-and-homeownership-in-the-netherlands/)
    - [resource2](https://www.iamexpat.nl/housing/buy-house-netherlands/taxes-costs-fees)
    - [resource3](https://www.iamexpat.nl/housing/dutch-mortgages/fees-costs-tax-relief-netherlands)
- Add monthly charges (e.g., [for an actual property](https://huispedia.nl/eindhoven/5615pa/hoogstraat/39-03#finance))
- Add huispedia API integration
