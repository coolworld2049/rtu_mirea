import ast
from collections import defaultdict

import pyhdfs
from loguru import logger

hdfs_client = pyhdfs.HdfsClient(hosts=f"localhost:50070", user_name="username")


def process_hdfs_file(file_path: str, product: str, max_count: int = 5):
    logger.info(f"file_path '{file_path}' product 'product'")
    mapping = defaultdict(lambda: {})
    with hdfs_client.open(file_path) as rf:
        file = rf.read().decode("UTF-8")
        lines = list(filter(lambda c: c != "", file.split("\n")))
        data = [tuple(map(lambda c: ast.literal_eval(c), x.split("\t"))) for x in lines]
        for k, v in data:
            if "pairs" in file_path:
                if k[0] == product:
                    mapping[k[0]].update({k[1]: v})
            elif "stripes" in file_path:
                if k == product:
                    mapping[k] = v
    sorted_mapping_by_value = sorted(
        mapping[product].items(), key=lambda c: c[1], reverse=True
    )
    logger.debug(sorted_mapping_by_value)
    return sorted_mapping_by_value


def advise(items, max_count):
    sorted_mapping_by_key = list(map(lambda c: c[0], sorted(items, key=lambda c: c[0])))
    result = sorted_mapping_by_key[:max_count]
    logger.info(result)
    return result


MAX_COUNT = 10
PRODUCT = "agreements"
pairs = process_hdfs_file("/user/ivanovnp/output/pairs/part-00000", PRODUCT, MAX_COUNT)
advise(pairs, MAX_COUNT)

stripes = process_hdfs_file(
    "/user/ivanovnp/output/stripes/part-00000", PRODUCT, MAX_COUNT
)
advise(stripes, MAX_COUNT)
