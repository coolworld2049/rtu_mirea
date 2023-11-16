#!/usr/bin/env bash

set +e

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

hdfs_path=warehouse/mapred/output
local_path=mapred/output

hdfs dfs -rm -r $hdfs_path

merged_file_path=merged_file.txt
awk 'FNR > 1' data/customers.csv data/products.csv data/orders.csv > "$merged_file_path"

[ -d $local_path ] || mkdir -p $local_path

blue=$(tput setaf 4)
normal=$(tput sgr0)

for i in {3..4}; do
  module_name=mapred.q"$i"
  printf '\n\e[1;34m%-6s\e[m' "RUN $module_name"
  printf "\n${blue}"
  python -m "$module_name" -r hadoop -o $hdfs_path/q"$i" "$merged_file_path" "$@"
  printf "${normal}"
  remote=$hdfs_path/q"$i"/part-00000
  loc=$local_path/"$i".txt
  [ ! -f $loc ] || rm $loc
  printf "COPY from %s to %s\n" "$remote" $loc
  hdfs dfs -copyToLocal "$remote" $loc
  hdfs dfs -copyToLocal $hdfs_path/q"$i"/part-00001 $local_path/"$i"-00001.txt
done;
