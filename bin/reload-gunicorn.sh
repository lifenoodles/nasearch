#!/usr/bin/env bash

set -e

pids=$(ps aux | grep gunicorn | grep -vE "grep|reload" | \
    awk '{printf "%s ", $2}')
if [ -n "${pids}" ]; then
    echo "Killing gunicorn instances with pid/s: ${pids}"
    echo ${pids} | xargs kill
fi

source ~/venv/noagenda-db/bin/activate
gunicorn --error-log ./gunicorn_error \
    --bind localhost:8001 nadb.wsgi:application &

echo "Gunicorn listening on port 8001"
