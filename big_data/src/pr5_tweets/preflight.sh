#!/bin/bash


SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

HDFS_DIR=tweets
LOCAL_DIR=$HOME/tweets
CUR_DIR="$SCRIPTDIR"/"$HDFS_DIR"

cat "$LOCAL_DIR"/ira_tweets_csv_hashed.csv | head -n 10 \
  > "$LOCAL_DIR"/ira_tweets_csv_hashed-10.csv

cat "$LOCAL_DIR"/ira_tweets_csv_hashed.csv | head -n 50 \
  > "$LOCAL_DIR"/ira_tweets_csv_hashed-50.csv

mv "$LOCAL_DIR"/Twitter_Elections_Integrity_Datasets_hashed_README.txt \
  "$LOCAL_DIR"/Twitter_Elections_Integrity_Datasets_hashed_README.md &> /dev/null

[ -d "$CUR_DIR" ] || sudo ln -s "$LOCAL_DIR" "$CUR_DIR"

#hdfs dfs -mkdir $HDFS_DIR
#hdfs dfs -mkdir "$HDFS_DIR"/rdd_checkpoint
#
#for file in "$LOCAL_DIR"/*.csv; do
#  file_name="$(basename "$file")"
#  echo copy "$file" to "$HDFS_DIR"/"$file_name"
#  hdfs dfs -copyFromLocal "$file" $HDFS_DIR
#done;