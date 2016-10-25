#!/usr/bin/env bash

NODE_NAME='politikon_instance'
WAS_RUNNING=false

if  docker ps | grep $NODE_NAME >/dev/null; then
    WAS_RUNNING=true
fi

# Set up
if  ! $WAS_RUNNING; then
    ./docker_run.sh -d
fi

# Run tests
docker exec -it $NODE_NAME coverage run --source=politikon,events,accounts manage.py test --settings=politikon.settings.test

# Clean up
if ! $WAS_RUNNING; then
    ./docker_bye.sh
fi