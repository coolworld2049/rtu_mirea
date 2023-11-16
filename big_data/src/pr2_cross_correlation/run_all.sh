#!/usr/bin/env bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

bash run.sh pairs "$1"
bash run.sh stripes "$1"