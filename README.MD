# Tagged Image Manager Challenge

Read about [the requirements, design and API](<design-docs/REQUIREMENTS AND DESIGN.md>).

## Getting Started

Prerequisites:

* [awscli v2](https://aws.amazon.com/cli/)
* [direnv](https://direnv.net/)
* [pyenv](https://github.com/pyenv/pyenv)
* [Poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions)

Create your virtualenv, activate and install dependencies:

```
pyenv install
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
pyenv rehash
python -m venv .venv
source .venv/bin/activate
poetry install
```

Run the tests:

```
make tests
```

Deploy Infra:

```
make deploy-infra
```

Deploy App:
```
make deploy
```