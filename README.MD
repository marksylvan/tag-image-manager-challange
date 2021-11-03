# Tagged Image Manager Challenge

Read about [the requirements, design and API](<design-docs/REQUIREMENTS AND DESIGN.md>).

OpenAPI [definition](design-docs/openapi/tagged-image-manager.yml) and [readme](design-docs/openapi/generated-tagged-image-manager.md).

## Getting Started

Prerequisites:

* [awscli v2](https://aws.amazon.com/cli/)
* [direnv](https://direnv.net/)
* [pyenv](https://github.com/pyenv/pyenv)
* [Poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions)

Create your virtualenv, activate and install dependencies:

```shell
pyenv install
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
pyenv rehash
python -m venv .venv
source .venv/bin/activate
poetry install
```

Run the tests:

```shell
make tests
```

Run locally (no auth required):

```shell
# use direnv + .envrc to ensure your BUCKET_NAME and DB_URL are set
# ensure you have AWS credentials in your environment allowing you to write to BUCKET_NAME
make run
```

In another shell:

```shell
make tables # if the database is new
curl localhost:8000/v1/tags | jq
```

## Deploy

Deploy Infra:

```shell
make deploy-infra
```

Deploy App:

```shell
# edit .envrc or set following variables when you run the command: BUCKET_NAME, DB_URL, COGNITO_POOL_ARN
make deploy
```

To do a staging or production deployment, set the `STAGE` variable to `staging` or `prod`.
