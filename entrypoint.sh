#!/bin/sh
set -e

DB_PATH="${SQLALCHEMY_DATABASE_URI#sqlite:///}"

# Si la BD existe pero no tiene alembic_version, hacer stamp head
# para que Alembic no intente crear tablas que ya existen
if [ -f "$DB_PATH" ]; then
    HAS_ALEMBIC=$(sqlite3 "$DB_PATH" "SELECT name FROM sqlite_master WHERE type='table' AND name='alembic_version';" 2>/dev/null || echo "")
    if [ -z "$HAS_ALEMBIC" ]; then
        echo "BD existente sin historial Alembic. Ejecutando stamp head..."
        flask db stamp head
    fi
fi

flask db upgrade

exec gunicorn -w "${WORKERS:-2}" -b "0.0.0.0:${PORT:-5000}" \
    --timeout "${TIMEOUT:-120}" \
    --capture-output --enable-stdio-inheritance \
    main:app
