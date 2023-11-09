#!/usr/bin/env bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

ALGORITHM_PATH="$1"
OUTPUT_PATH=output/"$(basename "$ALGORITHM_PATH")"
FILE=part-00000

echo -e "WORKDIR $SCRIPTDIR"
hdfs dfs -rm -r /user/ivanovnp/output/"$1" &>/dev/null
python -m gen_db -o input -n 500 -rr 4,16

echo -e "ALGORITHM_PATH $ALGORITHM_PATH"
python -m jobs."$ALGORITHM_PATH" input -o "$OUTPUT_PATH" -r hadoop

echo -e "\nFILE $FILE"
hdfs dfs -cat /user/ivanovnp/"$OUTPUT_PATH"/part-00000