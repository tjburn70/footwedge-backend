#!/usr/bin/env bash

set -e pipefail

python -m venv .venv

.venv/bin/pip install -r src/requirements.txt
.venv/bin/pip install -r src/requirements-dev.txt
