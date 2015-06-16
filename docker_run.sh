#!/usr/bin/env bash

if docker run -d --name politikon_db postgres:9.4.1 ; then
    echo "New database created" ;
else
    echo "Starting existing database" ;
    docker start politikon_db ;
fi

if docker run -it -v `pwd`:/app -p 2233:22 -p 8000:8000 --name politikon_instance --link politikon_db:postgres politikon ; then
    echo "politikon_instance created" ;
else
    echo "Starting existing politikon instance" ;
    docker start politikon_instance ;
fi
