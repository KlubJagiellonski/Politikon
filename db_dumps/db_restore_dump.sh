#!/bin/sh

DUMP=$1


OPS_DB_HOST=$(echo "postgres://postgres:postgres@$POSTGRES_PORT_5432_TCP_ADDR:$POSTGRES_PORT_5432_TCP_PORT")
POLITIKON_DB_HOST=$(echo "postgres://postgres:postgres@$POSTGRES_PORT_5432_TCP_ADDR:$POSTGRES_PORT_5432_TCP_PORT/politikon")

echo "Dropping db..."
psql $OPS_DB_HOST -c "DROP DATABASE politikon;"

echo "Creating empty db..."
psql $OPS_DB_HOST -c "CREATE DATABASE politikon;"

echo "Restoring db dump..."
pg_restore --verbose --clean --no-acl --no-owner -d $POLITIKON_DB_HOST $DUMP

echo "Dump $DUMP restoration completed"

