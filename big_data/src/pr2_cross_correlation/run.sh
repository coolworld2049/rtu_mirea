#!/usr/bin/env bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

ALGORITHM_NAME="$1"
OUTPUT_PATH=output/"$(basename "$ALGORITHM_NAME")"
MR_JOB_KWARGS="-o $OUTPUT_PATH -r hadoop $2"
FILE=part-00000

echo -e "\nWORKDIR $SCRIPTDIR"
hdfs dfs -rm -r /user/ivanovnp/output/"$1"

echo -e "ALGORITHM_NAME $ALGORITHM_NAME"
# shellcheck disable=SC2086
python -m jobs."$ALGORITHM_NAME" input $MR_JOB_KWARGS

echo -e "\nFILE $FILE"
[ -d parts ] || mkdir parts
hdfs dfs -cat /user/ivanovnp/"$OUTPUT_PATH"/"$FILE" > parts/"$(basename "$OUTPUT_PATH"_"$FILE")"