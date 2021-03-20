#!/usr/bin/env bash

set -x

black signal_cli_rest_api --check
isort --recursive --check-only signal_cli_rest_api
flake8 signal_cli_rest_api