import argparse
import ast
import pathlib
from contextlib import suppress

import pyhdfs
from loguru import logger


class Adviser:
    def __init__(self, host, port, username):
        self.username = username
        self.hdfs_client = pyhdfs.HdfsClient(hosts=f"{host}:{port}", user_name=username)

    def advise(self, file_path: pathlib.Path | str, product: str, advise_count=10):
        file_path = pathlib.Path(file_path)
        logger.info(
            f"part_path {file_path} product '{product}' advise_count '{advise_count}'"
        )
        result = []
        with self.hdfs_client.open(file_path.__str__()) as rf:
            file = rf.read().decode("UTF-8")
            # logger.debug(f"file_path {file_path}: \n{file}")
            lines = file.split("\n")
            for i in range(len(lines) - 1):
                _products, _count = lines[i].strip().split("\t")
                products: list[str] = ast.literal_eval(_products)
                with suppress(ValueError):
                    product_index = products.index(product)
                    del products[product_index]
                    result.append((products, int(_count)))

        final_result = list(map(lambda c: c[0][0], sorted(result, key=lambda c: -c[1])))
        advices = final_result[:advise_count]
        logger.info("advices:\n{}".format("\n".join(advices)))
        return advices


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=50070)
    parser.add_argument("--username", default="ivanovnp")
    parser.add_argument(
        "-alg", "--algorithm_name", choices=["pairs", "stripes"], required=True
    )
    parser.add_argument("-p", "--product", required=True)
    parser.add_argument(
        "-ac",
        "--advise_count",
        default=10,
        help="--advise_count [integer]",
    )
    args = parser.parse_args()
    adviser = Adviser(
        host=args.host,
        port=args.port,
        username=args.username,
    )
    part_path = pathlib.Path(
        f"/user/{args.username}/output/{args.algorithm_name}/part-00000"
    )
    adviser.advise(part_path, args.product, args.advise_count)
