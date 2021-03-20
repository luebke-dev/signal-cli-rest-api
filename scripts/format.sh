#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place signal_cli_rest_api --exclude=__init__.py
black signal_cli_rest_api
isort --recursive --apply signal_cli_rest_api
