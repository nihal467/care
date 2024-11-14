#!/bin/bash
printf "api" > /tmp/container-role

set -euo pipefail

postgres_ready() {
python << END
import sys

import psycopg

try:
    psycopg.connect(conninfo="${DATABASE_URL}")
except psycopg.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

python manage.py collectstatic --noinput
python manage.py compilemessages -v 0

export NEW_RELIC_CONFIG_FILE=/etc/newrelic.ini
if [[ -f "$NEW_RELIC_CONFIG_FILE" ]]; then
  newrelic-admin run-program gunicorn config.wsgi:application --bind 0.0.0.0:9000 --chdir=/app
else
  gunicorn config.wsgi:application --bind 0.0.0.0:9000 --chdir=/app --workers 2
fi
