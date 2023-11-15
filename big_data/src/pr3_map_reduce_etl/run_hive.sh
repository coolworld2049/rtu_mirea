#!/usr/bin/env bash

set +e

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

bash ~/rtu_mirea/big_data/scripts/hive/exec.sh --outputformat=csv2 -f hive/ddl.hql
bash ~/rtu_mirea/big_data/scripts/hive/exec.sh --outputformat=csv2 -f hive/dql.hql > hive/query_result.csv
