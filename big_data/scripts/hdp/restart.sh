#!/bin/bash

cd hdp || exit

. stop.sh
. clean.sh
. format.sh
. start.sh