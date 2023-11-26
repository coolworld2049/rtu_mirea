spark_work_dir = "hdfs://localhost:9000/user/ivanovnp/tweets"
spark_conf = {
    "spark.jars.packages": "graphframes:graphframes:0.8.3-spark3.5-s_2.12",
    "spark.checkpoint.auto": "true",
    "spark.sql.debug.maxToStringFields": "100",
    "spark.executor.memory": "10g",
    # "spark.executor.cores": "1",
    # "spark.executor.instances": "4",
    "spark.driver.memory": "10g",
    # "spark.driver.cores": "6",
    # "spark.default.parallelism": "12",
}
