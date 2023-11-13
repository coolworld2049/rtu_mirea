#!/bin/bash

# shellcheck disable=SC2016
screen -dmS hiveserver2 bash -c 'cd /tmp/hive-`whoami`-metastore && hiveserver2 --hiveconf hive.root.logger=INFO,console'