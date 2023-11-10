import argparse
import ast
import json
import pathlib
from contextlib import suppress

import pyhdfs
from loguru import logger


class Adviser:
    def __init__(self, host, port, username):
        self.username = username
        self.hdfs_client = pyhdfs.HdfsClient(hosts=f"{host}:{port}", user_name=username)

    @staticmethod
    def pairs(key, value, target_key):
        key: list[str] = ast.literal_eval(key)
        with suppress(ValueError):
            key.index(target_key)
            return key, int(value)

    @staticmethod
    def stripes(key, value, target_key):
        value: dict[str, int] = json.loads(value)
        if value.get(target_key):
            sorted_value = sorted(value.items(), key=lambda c: -c[1])
            return key, sorted_value

    def advise(self, file_path: pathlib.Path | str, product: str, advise_count=10):
        file_path = pathlib.Path(file_path)
        logger.info(
            f"part_path {file_path} product '{product}' advise_count '{advise_count}'"
        )
        result = []
        filtered_result = []
        with self.hdfs_client.open(file_path.__str__()) as rf:
            file = rf.read().decode("UTF-8")
            lines = file.split("\n")
            for i in range(len(lines) - 1):
                key, value = lines[i].strip().split("\t")
                if "pairs" in file_path.__str__():
                    local_result = self.pairs(key, value, product)
                elif "stripes" in file_path.__str__():
                    local_result = self.stripes(key, value, product)
                if local_result:
                    result.append(local_result)
        if "pairs" in file_path.__str__():
            sorted_result = sorted(result, key=lambda c: -c[1])
            logger.debug(
                f"algorithm 'pairs' - sorted result: {sorted_result[:advise_count]}"
            )
            filtered_result = list(map(lambda c: c[0][1], sorted_result))
        elif "stripes" in file_path.__str__():
            logger.debug(
                f"algorithm 'stripes' - sorted result: {result[:advise_count]}"
            )
            filtered_result = list(map(lambda c: c[1][0][0], result))
        advices = filtered_result[:advise_count]
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
