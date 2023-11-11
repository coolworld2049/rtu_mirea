import ast

import pyhdfs

hdfs_client = pyhdfs.HdfsClient(hosts=f"localhost:50070", user_name="username")


def process_hdfs_file(file_path: str, product: str):
    lines = []

    with hdfs_client.open(file_path) as rf:
        file = rf.read().decode("UTF-8")
        if "pairs" in file_path:
            lines.extend(
                [
                    (ast.literal_eval(x.split("\t")[0])[1], x.split("\t")[1])
                    for x in file.split("\n")
                    if x.split("\t")[0]
                    and ast.literal_eval(x.split("\t")[0])[0] == product
                ]
            )
        elif "stripes" in file_path:
            for x in file.split("\n"):
                key = x.split("\t")[0].replace('"', "")
                if key == product:
                    lines = list(ast.literal_eval(x.split("\t")[1]).items())
    lines = sorted(lines, key=lambda c: c[1], reverse=True)
    lines = sorted(lines)
    return lines[:10]


pairs = process_hdfs_file("/user/ivanovnp/output/pairs/part-00000", "loan")
stripes = process_hdfs_file("/user/ivanovnp/output/stripes/part-00000", "loan")
print(f"pairs {pairs}")
print(f"stripes {stripes}")
