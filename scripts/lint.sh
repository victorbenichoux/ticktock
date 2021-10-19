#!/bin/bash
set -e

black ticktock tests --check
isort ticktock tests --check-only
flake8 ticktock tests 
mypy ticktock

