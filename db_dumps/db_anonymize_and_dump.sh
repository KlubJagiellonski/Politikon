#!/bin/sh

DUMP=$1

./db_restore_dump.sh ./$DUMP

DB_HOST=$(echo "postgres://postgres:postgres@$POSTGRES_PORT_5432_TCP_ADDR:$POSTGRES_PORT_5432_TCP_PORT/politikon")

psql -d $DB_HOST -f db_anonymize.sql

OUTPUT_DUMP=$2

/usr/lib/postgresql/9.4/bin/pg_dump -Fc -d $DB_HOST > $OUTPUT_DUMP
