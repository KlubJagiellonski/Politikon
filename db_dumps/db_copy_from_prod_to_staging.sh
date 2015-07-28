#!/bin/sh

heroku pg:copy politikon::DATABASE_URL DATABASE_URL --app politikon-staging
