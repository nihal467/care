#!/usr/bin/env bash
printf "api" > /tmp/container-role

set -euo pipefail

./scripts/wait_for_db.sh
./scripts/wait_for_redis.sh

echo "running collectstatic..."
python manage.py collectstatic --noinput
python manage.py compilemessages -v 0

echo "starting server..."
if [[ "${DJANGO_DEBUG,,}" == "true" ]]; then
  echo "waiting for debugger..."
  python -m debugpy --wait-for-client --listen 0.0.0.0:9876 manage.py runserver_plus 0.0.0.0:9000
else
  python manage.py runserver 0.0.0.0:9000
fi
