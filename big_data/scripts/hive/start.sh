#!/bin/bash

killall screen
# shellcheck disable=SC2016
screen -dmS hiveserver2 bash -c 'cd "$HOME"/hive-"$(whoami)"-metastore && hiveserver2 --hiveconf hive.root.logger=OFF'
