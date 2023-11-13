#!/usr/bin/env bash

. install/hadoop.sh
. install/hive.sh

. hdp/clean.sh
. hdp/format.sh
. hdp/start.sh

. hive/metastore.sh
. hive/start.sh