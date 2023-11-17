#!/bin/bash

cd hdp || exit

. stop.sh
. format.sh
. start.sh