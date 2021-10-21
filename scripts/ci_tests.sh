#!/bin/bash

set -ux

if [[ $OS_NAME == "ubuntu-latest" ]]; then
    nox --error-on-missing-interpreters -s "coverage-${PYTHON_VERSION}"
else
    nox --error-on-missing-interpreters -s "test-${PYTHON_VERSION}"
fi
