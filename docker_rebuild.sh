#!/usr/bin/env bash

if [[ $1 =~ ^--clean$ ]]; then
  docker build --rm=true -t politikon .
else
  docker build -t politikon .
fi
