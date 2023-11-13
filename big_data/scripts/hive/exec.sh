#!/usr/bin/env bash

beeline -u jdbc:hive2://localhost:10000 -n "$USER" --color=true "$@"
