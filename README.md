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

## Dev Plan

- Split the initial costs
  - Resources include and not exclusive to:
    - [resource1](https://www.hanno.nl/expat-mortgages/tax-return-and-homeownership-in-the-netherlands/)
    - [resource2](https://www.iamexpat.nl/housing/buy-house-netherlands/taxes-costs-fees)
    - [resource3](https://www.iamexpat.nl/housing/dutch-mortgages/fees-costs-tax-relief-netherlands)
- Add monthly charges (e.g., [for an actual property](https://huispedia.nl/eindhoven/5615pa/hoogstraat/39-03#finance))
- Add huispedia API integration
