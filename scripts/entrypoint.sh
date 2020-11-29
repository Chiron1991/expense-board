#!/bin/bash

set -e

# check SECRET_KEY
if [ -z "$SECRET_KEY" ]
then
  echo "*** WARNING *** You have not set an explicit SECRET_KEY. Will use a temporary one. This will likely cause trouble at some point."
fi

# if this entrypoint is called from an interactive session (docker run -it), execute the command instead of starting the app
if [ ! -z "$@" ]
then
  exec $@
  exit 0
fi

# prepare log files and output them to stdout
mkdir -p /srv/logs
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &  # todo: check what django logging outputs

# apply schema migrations
echo "Applying schema migrations"
python manage.py migrate

# run the app
if [ ! -z "$HTTP_WORKER_COUNT" ]
then
  NUM_WORKER=$HTTP_WORKER_COUNT
else
  NUM_WORKER=$(nproc)
fi
echo "Running gunicorn with $NUM_WORKER workers"
exec gunicorn expenseboard.wsgi:application \
  --name expenseboard \
  --bind 0.0.0.0:80 \
  --workers $NUM_WORKER \
  --log-level=info \
  --log-file=/srv/logs/gunicorn.log \
  --access-logfile=/srv/logs/access.log
