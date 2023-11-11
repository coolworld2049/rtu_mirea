#!/usr/bin/env bash

set -eou pipefail

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

bash exec_hive.sh -f hive/ddl.hql
bash exec_hive.sh -f hive/dml.hql
bash exec_hive.sh -f hive/dql.hql