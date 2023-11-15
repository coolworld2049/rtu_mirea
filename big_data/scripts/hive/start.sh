#!/bin/bash

killall screen
screen -dmS hiveserver2 bash -c 'cd "$HOME"/hive-"$(whoami)"-metastore && hiveserver2 --hiveconf hive.root.logger=OFF'