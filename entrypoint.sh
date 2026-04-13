#!/bin/sh
set -e

flask db upgrade

exec gunicorn -w "${WORKERS:-2}" -b "0.0.0.0:${PORT:-5000}" \
    --timeout "${TIMEOUT:-120}" \
    --capture-output --enable-stdio-inheritance \
    main:app
