#!/usr/bin/env bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

python -m gen_db -o input -n 60 -rr 4,12
bash run.sh pairs "$1"
bash run.sh stripes "$1"