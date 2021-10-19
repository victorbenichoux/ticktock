#!/usr/bin/env bash

set -e
set -x

black ticktock tests
isort ticktock tests
