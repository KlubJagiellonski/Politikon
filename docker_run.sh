#!/usr/bin/env bash

NAME='politikon'
DB_NAME='politikon_db'
PSQL_VER='postgres:latest'
ES_NAME='politikon_es'
ES_VER='docker.elastic.co/elasticsearch/elasticsearch:5.4.0'
NODE_NAME='politikon_instance'
RUN_AS_DEAMON=false

function pri {
    echo " [${1}] $2"
}

# > > DB  < <
if   ! docker ps -a | grep $DB_NAME >/dev/null; then
    pri 'db' "$DB_NAME creating and running"
    docker run -d --name $DB_NAME $PSQL_VER
elif ! docker ps -a | grep $DB_NAME | grep Up >/dev/null; then
    pri 'db' "existing $DB_NAME starting..."
    docker start $DB_NAME
else
    pri 'db' "nothing to do - $DB_NAME is running..."
fi

if ! docker ps -a | grep $DB_NAME | grep Up >/dev/null; then
    pri '!!' "cannot start $DB_NAME - exiting"
    exit 1
fi

# > > ES  < <
if   ! docker ps -a | grep $ES_NAME >/dev/null; then
    pri 'es' "$ES_NAME creating and running"
    docker run -d --name $ES_NAME -p 9200:9200 -e "http.host=0.0.0.0" -e "transport.host=127.0.0.1" $ES_VER
elif ! docker ps -a | grep $ES_NAME | grep Up >/dev/null; then
    pri 'es' "existing $ES_NAME starting..."
    docker start $ES_NAME
else
    pri 'es' "nothing to do - $ES_NAME is running..."
fi

if ! docker ps -a | grep $ES_NAME | grep Up >/dev/null; then
    pri '!!' "cannot start $ES_NAME - exiting"
    exit 1
fi

# > > BUILD < <
if [[ $1 =~ ^--?build$ ]]; then
    val='yes'
elif [[ $1 =~ ^--?no-build$ ]]; then
    val='no'
elif [[ $1 =~ '-d' ]]; then
    RUN_AS_DEAMON=true
else
    pri 'vm' "$NODE_NAME CONTAINER BUILD"
    pri '  ' " It should NOT harm your env if it NOT CHANGED"
    read -p " Do you want to run it (you should)? [y/N] " val
fi
if [[ $val =~ [yY](es)* ]]; then
    docker stop $NODE_NAME
    if [[ $1 =~ ^--clean$ ]] || [[ $2 =~ ^--clean$ ]]; then
        ./docker_rebuild.sh --clean || exit 1
    else
        ./docker_rebuild.sh || exit 1
    fi
fi

# > > NODE < <
if   ! docker ps -a | grep $NODE_NAME >/dev/null; then
    pri 'vm' "$NODE_NAME creating and starting..."
    docker run -d --dns 8.8.8.8 --dns 8.8.4.4 -t -v `pwd`:/app -p 2233:22 -p 8000:8000 --name $NODE_NAME --link ${DB_NAME}:postgres $NAME /bin/bash
elif ! docker ps -a | grep $NODE_NAME | grep Up >/dev/null; then
    pri 'vm' "existing $NODE_NAME starting..."
    docker start $NODE_NAME
fi


if ! $RUN_AS_DEAMON; then
    pri 'vm' "getting into $NODE_NAME"
    docker exec -it $NODE_NAME bash
else
    pri 'vm' "running $NODE_NAME as deamon"
    docker exec -dit $NODE_NAME bash
fi

true


echo " tip: after work you could use ./docker_bye.sh"

