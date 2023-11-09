import argparse
import os
import pathlib
import random
import time

import pyhdfs
from loguru import logger
from mimesis import Generic

PWD = pathlib.Path(__file__).parent
HADOOP_VERSION = "2.9.2"


class CrossCorrelation:
    def __init__(self, host, port, username, algorithm_name, input_path, output_path):
        self.username = username
        self.algorithm_name = algorithm_name
        self.input_path = pathlib.Path(input_path)
        self.output_path = pathlib.Path(output_path)
        self.mapper_file_path = PWD.joinpath(f"{algorithm_name}/map.py")
        self.reducer_file_path = PWD.joinpath(f"{algorithm_name}/reduce.py")
        self.hdfs_client = pyhdfs.HdfsClient(hosts=f"{host}:{port}", user_name=username)
        self.hadoop_home = f"/home/{self.username}/hadoop-{HADOOP_VERSION}"

        self.output_path.mkdir(exist_ok=True)
        os.system(f"chmod +x {self.mapper_file_path} {self.reducer_file_path}")

    @property
    def get_input_path_str(self):
        return self.input_path.__str__()

    @property
    def get_output_path_str(self):
        return self.output_path.__str__()

    def _create_input(self, product_number: int = 200):
        if self.input_path.exists():
            return True
        generic = Generic()
        fake_products = [generic.text.word().replace(" ", "") for _ in range(100)]
        product_names = ""
        for a in range(product_number):
            _product_names = " ".join(
                set(random.choices(fake_products, k=random.randint(6, 18)))
            )
            if a != product_number - 1:
                _product_names += "\n"
            product_names += _product_names
        self.input_path.write_text(product_names)
        logger.debug(f"Created {self.input_path}")

    def _upload_input(self):
        self.hdfs_client.delete(self.get_input_path_str, recursive=True)
        self.hdfs_client.create(
            self.get_input_path_str,
            pathlib.Path(self.input_path).read_bytes(),
        )
        logger.debug(f"Uploaded {self.input_path} to hdfs")

    def yarn_jar_streaming(self, local_save: bool = True):
        self._create_input()
        self._upload_input()
        self.hdfs_client.delete(self.get_output_path_str, recursive=True)
        cmd = (
            f"{self.hadoop_home}/bin/yarn jar {self.hadoop_home}/share/hadoop/tools/lib/hadoop-streaming-*.jar"
            f" -files {self.mapper_file_path},{self.reducer_file_path}"
            f" -input {self.get_input_path_str}"
            f" -output {self.get_output_path_str}"
            f" -mapper {self.mapper_file_path}"
            f" -reducer {self.reducer_file_path}"
        )
        print(cmd)
        os.system(cmd)
        if local_save:
            file_name = "part-00000"
            path = self.output_path.joinpath(file_name).__str__()
            pathlib.Path(path).write_bytes(self.hdfs_client.open(path).read())
        logger.info("Hadoop job completed")


class Adviser:
    def __init__(self, hdfs_client: pyhdfs.HdfsClient, output_path: pathlib.Path):
        self.hdfs_client: pyhdfs.HdfsClient = hdfs_client
        self.output_path = output_path

    def advise(self, algorithm_name: str, product: str | None = None, advise_count=10):
        logger.info(
            f"algorithm_name '{algorithm_name}' product '{product}' advise_count '{advise_count}'"
        )
        self.output_path.parents[1].joinpath(algorithm_name)
        if not product:
            product = input("Enter product name: ")
        result = {}
        file_name = "part-00000"
        with self.hdfs_client.open(
            self.output_path.joinpath(file_name).__str__()
        ) as rf:
            ln = rf.read().decode("UTF-8").split("\n")
            for i in range(len(ln) - 1):
                products, count = ln[i].strip().split("\t")
                products = products.split(" ")
                if product == products[0]:
                    result[products[1]] = int(count)
                elif product == products[1]:
                    result[products[0]] = int(count)

        sorted_result = sorted(result.items(), key=lambda item: (-item[1], item[0]))
        for index, (product, count) in enumerate(sorted_result[:advise_count], start=1):
            logger.info(f"[{product}] {count}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=50070)
    parser.add_argument("--username", default="ivanovnp")
    parser.add_argument(
        "--algorithm_name", choices=["pairs", "stripes"], default="pairs"
    )
    parser.add_argument("--force", default=False)
    parser.add_argument("--advise", help="--advise [product_name]")
    parser.add_argument(
        "--advise-number",
        default=10,
        help="--advise-number [integer]",
    )

    args = parser.parse_args()
    correlation = CrossCorrelation(
        host=args.host,
        port=args.port,
        username=args.username,
        algorithm_name=args.algorithm_name,
        input_path=f"{PWD}/input",
        output_path=f"{PWD}/output/{args.algorithm_name}",
    )
    if args.force or not correlation.hdfs_client.exists(
        correlation.get_output_path_str
    ):
        correlation.yarn_jar_streaming()

    adviser = Adviser(
        hdfs_client=correlation.hdfs_client, output_path=correlation.output_path
    )
    try:
        adviser.advise(args.algorithm_name, product=args.advise)
    except pyhdfs.HdfsFileNotFoundException as e:
        correlation.yarn_jar_streaming()
        time.sleep(2)
        adviser.advise(args.algorithm_name, product=args.advise)
        logger.error(e)


if __name__ == "__main__":
    main()
