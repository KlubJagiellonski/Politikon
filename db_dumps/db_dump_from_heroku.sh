#!/bin/sh

#dumps politikon db from heroku

DUMP=`heroku pg:backups --app politikon | grep '^[a|b]' | head -1 | cut -f1 -d' '`
FILENAME=`heroku pg:backups --app politikon | grep '^[a|b]' | head -1 | cut -f3,4 -d' '`
FILENAME=`echo "politikon_NON-anonymized_db_${FILENAME// /_}.dump"`

curl -o $FILENAME `heroku pg:backups public-url $DUMP --app politikon`

