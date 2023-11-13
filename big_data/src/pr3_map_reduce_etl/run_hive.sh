#!/usr/bin/env bash

set -eou pipefail

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

bash ~/rtu_mirea/big_data/scripts/hive/exec.sh -f "$PWD"/hive/ddl.hql
bash ~/rtu_mirea/big_data/scripts/hive/exec.sh -f "$PWD"/hive/dml.hql
bash ~/rtu_mirea/big_data/scripts/hive/exec.sh -f "$PWD"/hive/dql.hql