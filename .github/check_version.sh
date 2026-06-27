#!/bin/bash

version=$(python3 -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")
result=$(curl -s https://pypi.org/pypi/pyIntradel/json | jq -r '.releases | keys[]' | grep -w "$version")

if [ -z "$result" ]
then
  echo Version "$version" not found in pypi, all good
  exit 0
else
  echo Version "$version" already exist in pypi
  exit 1
fi
