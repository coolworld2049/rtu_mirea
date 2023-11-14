#!/usr/bin/env bash

set -eou pipefail

cd install || exit
source "$HOME"/.bashrc
. hadoop.sh
source "$HOME"/.bashrc
. hive.sh
source "$HOME"/.bashrc
. pig.sh
source "$HOME"/.bashrc
cd ..