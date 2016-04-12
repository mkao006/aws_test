#!/bin/bash

echo Starting postgres
exec start-stop-daemon --start --chuid postgres:postgres \
    --exec /usr/lib/postgresql/9.3/bin/postgres -- \
    -D /var/lib/postgresql/9.3/main \
    -c config_file=/etc/postgresql/9.3/main/postgresql.conf &
# psql -c "CREATE USER mk WITH SUPERUSER PASSWORD 'password';"\
# && createdb -O mk random_walker_aws_test

# python commands
# python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn random_walker.wsgi:application \
    --name random_walker \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log \
    "$@"
