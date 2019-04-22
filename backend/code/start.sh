#!/bin/bash
RABBIT_MANAGMENT_PORT=${RABBIT_MANAGMENT_PORT:-15672}
ER=1
echo "Waiting for rabbit to start..."
while [ "$ER" != "0" ] ; do
  echo "Trying..."
  curl -f http://${RABBIT_HOST}:${RABBIT_MANAGMENT_PORT} &>/dev/null
  ER=$?
  sleep 1
done
echo "Starting application..."
pipenv run python start.py
