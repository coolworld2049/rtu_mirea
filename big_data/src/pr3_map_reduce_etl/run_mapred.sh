#!/usr/bin/env bash

set +e

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

hdfs_path=warehouse/mapred/output
local_path=mapred/query_result

[ -d $local_path ] || mkdir -p $local_path

hdfs dfs -rm -r $hdfs_path
hdfs dfs -mkdir -p $hdfs_path

input_path=hdfs:///user/ivanovnp/warehouse

python -m mapred.job --customers $input_path/customers/customers.csv --products $input_path/products/products.csv --orders $input_path/orders/orders.csv \
  -o $hdfs_path \
  -r hadoop "$@"

for i in {1..7}; do
  remote="$hdfs_path/q$i/part*"
  loc=$local_path/"$i".csv
  echo "$remote" to $loc
  hdfs dfs -copyToLocal "$remote" $loc
done;
