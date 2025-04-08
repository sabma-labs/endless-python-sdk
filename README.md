# Endless Python SDK
[![Discord][discord-image]][discord-url]
[![PyPI Package Version][pypi-image-version]][pypi-url]
[![PyPI Package Downloads][pypi-image-downloads]][pypi-url]

This provides basic functionalities to interact with [Endless](https://github.com/endless-labs). Get started [here](https://docs.endless.link/endless/devbuild/start).

Currently, this is still in development and may not be suitable for production purposes.

Note: The sync client is deprecated, please only start new projects using the async client. Feature contributions to the sync client will be rejected.

## Requirements
This SDK uses [Poetry](https://python-poetry.org/docs/#installation) for packaging and dependency management:

```
curl -sSL https://install.python-poetry.org | python3 -
poetry install
```

## Unit testing
```bash
make test
```

## E2E testing and Using the Endless CLI

* Download and install the [Endless CLI](https://docs.endless.link/endless/devbuild/build/endless-cli).
* Set the environment variable `ENDLESS_CLI_PATH` to the full path of the CLI.
* Retrieve the [Endless Core Github Repo](https://github.com/endless-labs/endless-move-framework) (git clone https://github.com/endless-labs/endless-move-framework.git)
* Set the environment variable `ENDLESS_CORE_REPO` to the full path of the Repository.
* `make integration_test`

You can do this a bit more manually by:

First, run a local testnet (run this from the root of endless-framework):

```bash
endless node run-local-testnet --force-restart --assume-yes --with-indexer-api
```

Next, tell the end-to-end tests to talk to this locally running testnet:

```bash
export ENDLESS_CORE_REPO="/path/to/repo"
export ENDLESS_FAUCET_URL="http://127.0.0.1:8081"
export ENDLESS_INDEXER_URL="https://idx-test.endless.link/api/v1"
export ENDLESS_NODE_URL="https://rpc-test.endless.link/v1"
```

Finally run the tests:

```bash
make examples
```

Integration Testing Using the Endless CLI:

```bash
make integration_test
```

> [!NOTE]
> The Python SDK does not require the Indexer, if you would prefer to test without it, unset or do not set the environmental variable `ENDLESS_INDEXER_URL` and exclude `--with-indexer-api` from running the endless node software.

## Autoformatting
```bash
make fmt
```

## Autolinting
```bash
make lint
```

## Package Publishing

* Download the [ENDLESS CLI](https://docs.endless.link/endless/devbuild/build/endless-cli).
* Set the environment variable `ENDLESS_CLI_PATH` to the full path of the CLI.
* `poetry run python -m endless_sdk.cli` and set the appropriate command-line parameters

## Semantic versioning
This project follows [semver](https://semver.org/) as closely as possible

[repo]: https://github.com/endless-labs/endless-move-framework
[pypi-image-version]: https://img.shields.io/pypi/v/endless-sdk.svg
[pypi-image-downloads]: https://img.shields.io/pypi/dm/endless-sdk.svg
[pypi-url]: https://pypi.org/project/endless-sdk
[discord-image]: https://img.shields.io/discord/945856774056083548?label=Discord&logo=discord&style=flat~~~~
[discord-url]: https://discord.gg/endlessnetwork
