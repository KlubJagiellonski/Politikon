#!/usr/bin/env bash

if ! docker ps -a | grep politikon_db >/dev/null; then
    docker run -d --name politikon_db postgres:latest
    echo "New database created" ;
else
    docker start politikon_db ;
    echo "Started existing database" ;
fi

if ! docker ps -a | grep politikon_instance >/dev/null; then
    docker run -d --dns 8.8.8.8 --dns 8.8.4.4 -it -v `pwd`:/app -p 2233:22 -p 8000:8000 --name politikon_instance --link politikon_db:postgres politikon /bin/bash;
    echo "politikon_instance created" ;
else
    docker start politikon_instance ;
    echo "Started existing politikon instance" ;
fi
docker attach politikon_instance
