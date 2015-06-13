#!/usr/bin/env bash

set -eu

scripts/configure.py
scripts/reset-db.sh

echo "configuration complete"
