from pyspark import SparkConf

dataset_path = "hdfs://localhost:9000/user/ivanovnp/tweets"
spark_config = SparkConf().setAll(
    [
        ("spark.executor.memory", "6g"),
        ("spark.executor.cores", "4"),
        ("spark.cores.max", "4"),
        ("spark.driver.memory", "6g"),
        ("spark.debug.maxToStringFields", "100"),
    ]
)
