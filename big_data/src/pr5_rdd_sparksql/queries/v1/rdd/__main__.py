from py4j.protocol import Py4JJavaError
from pyspark import SparkContext

from pr5_rdd_sparksql.queries.v1.const import politicians

dataset_path = "hdfs://localhost:9000/user/ivanovnp/tweets"

with SparkContext() as sc:
    rdd = (
        sc.textFile(f"{dataset_path}/ira_tweets_csv_hashed.csv")
        .map(lambda line: line.split(","))
        .map(lambda line: tuple(map(lambda c: str(c).rstrip('"').lstrip('"'), line)))
    )
    result = (
        rdd.filter(
            lambda row: all(
                (
                    row[10] == "ru",
                    row[11] == "ru",
                )
            )
            and any(p_lower in row[12].lower() for p_lower in politicians)
        )
        .map(lambda row: (row[3], 1))
        .reduceByKey(lambda a, b: a + b)
        .sortBy(lambda x: x[1], ascending=False)
        .take(1)
    )
    print(f"result: {result}")
    if len(result) > 0:
        try:
            sc.parallelize(result).saveAsTextFile(
                f"{dataset_path}/output/v1_rdd_result"
            )
        except Py4JJavaError as e:
            pass
    sc.stop()
