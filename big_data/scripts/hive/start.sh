#!/bin/bash

screen -dmS hiveserver2 \
bash -c 'cd ~/metastore && hiveserver2 --hiveconf hive.root.logger=INFO,console'
