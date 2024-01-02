from pyspark.sql import SparkSession


spark_work_dir = "file:///home/ivanovnp/tweets"
spark_conf = {
    "spark.jars.packages": "graphframes:graphframes:0.8.3-spark3.5-s_2.12",
    "spark.checkpoint.auto": "true",
    "spark.sql.debug.maxToStringFields": "100",
    "spark.executor.memory": "10g",
    "spark.driver.memory": "10g",
}


def get_spark_session():
    spark = (
        SparkSession.builder.appName("GraphFramesApp")
        .config(map=spark_conf)
        .getOrCreate()
    )
    spark.sparkContext.setCheckpointDir(f"/tmp")
    return spark
