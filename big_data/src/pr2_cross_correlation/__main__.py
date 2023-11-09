import argparse
import os
import pathlib
import random

import pyhdfs
from loguru import logger
from mimesis import Generic

HADOOP_HOME = "/home/ivanovnp/hadoop-2.9.2"
PWD = pathlib.Path(__file__).parent


class CrossCorrelation:
    def __init__(
        self,
        host,
        port,
        username,
        algorithm_name,
        db_file,
    ):
        self.username = username
        self.algorithm_name = algorithm_name
        self.db_file = db_file
        self.mapper_file_path = PWD.joinpath(f"{algorithm_name}/map.py")
        self.reducer_file_path = PWD.joinpath(f"{algorithm_name}/reduce.py")
        self.hdfs_project_dir = PWD
        self.hdfs_client = pyhdfs.HdfsClient(hosts=f"{host}:{port}", user_name=username)

    def create_db(self):
        generic = Generic()
        fake_products = [generic.text.word().replace(" ", "") for _ in range(100)]
        product_names = ""
        product_number = 200
        for a in range(product_number):
            _product_names = " ".join(set(random.choices(fake_products, k=random.randint(4, 12))))
            if a != product_number - 1:
                _product_names += "\n"
            product_names += _product_names
        pathlib.Path(self.db_file).write_text(product_names)
        logger.debug(f"Created db {self.db_file}")

    def upload_db(self):
        self.hdfs_client.delete(
            f"{self.hdfs_project_dir}/input", recursive=True
        )
        self.hdfs_client.create(
            f"{self.hdfs_project_dir}/input",
            pathlib.Path(self.db_file).read_bytes(),
        )
        logger.debug(f"Uploaded db {self.db_file} to HDFS")

    def run_hadoop_job(self):
        _output_path = f"{self.hdfs_project_dir}/output/{self.algorithm_name}/"
        self.hdfs_client.delete(_output_path, recursive=True)
        cmd = (
            f"{HADOOP_HOME}/bin/yarn jar {HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-*.jar"
            f" -files {self.mapper_file_path},{self.reducer_file_path}"
            f" -input {self.hdfs_project_dir}/input"
            f" -output {self.hdfs_project_dir}/output/{self.algorithm_name}"
            f" -mapper {self.mapper_file_path}"
            f" -reducer {self.reducer_file_path}"
        )
        print(cmd)
        res = os.system(cmd)
        if res != 0:
            raise Exception(f"cmd output {res}")
        logger.info("Hadoop job completed")

    def get_adviser(self, product: str = lambda: input("Enter product name: ")):
        advise_count = 10
        result = {}
        with self.hdfs_client.open(
            f"{self.hdfs_project_dir}/output/{self.algorithm_name}/part-00000"
        ) as res:
            lines = res.read().decode("utf-8").split("\n")

            for i in range(len(lines) - 1):
                products, count = lines[i].strip().split("\t")
                products = products.split(" ")
                if product == products[0]:
                    result[products[1]] = int(count)
                elif product == products[1]:
                    result[products[0]] = int(count)

        sorted_result = sorted(result.items(), key=lambda item: (-item[1], item[0]))
        for index, (product, count) in enumerate(sorted_result[:advise_count], start=1):
            logger.info(f"{index}) {product} ({count})")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=50070)
    parser.add_argument("--username", default="ivanovnp")
    parser.add_argument(
        "--algorithm_name", choices=["pairs", "stripes"], default="pairs"
    )
    parser.add_argument("--db_file", default=f"{PWD}/product_database.txt")

    args = parser.parse_args()
    correlation = CrossCorrelation(
        host=args.host,
        port=args.port,
        username=args.username,
        algorithm_name=args.algorithm_name,
        db_file=args.db_file,
    )
    correlation.create_db()
    correlation.upload_db()
    correlation.run_hadoop_job()
    correlation.get_adviser()


if __name__ == "__main__":
    main()
