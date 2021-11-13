#!/bin/bash
set -e

if [[ $1 == apply ]] ; then
    black ticktock tests
    isort ticktock tests
fi

black ticktock tests --check
isort ticktock tests --check-only
flake8 ticktock tests 
mypy ticktock

