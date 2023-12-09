# Mortgager

A program to calculate mortgage

## Run

### Native

Use your favourite OS to run python3 natively.

```Shell
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ python3 -m flask run
```

Go to `http://127.0.0.1:5000/`

### Virtual environment

Use your favourite OS to run virtual environment.

```Shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ python3 -m flask run
```

Go to `http://127.0.0.1:5000/`

### Docker (Windows - WSL)

Make sure the Docker windows up is running.

```Shell
$ docker compose up --build
```

Go to `http://127.0.0.1:5000/`
