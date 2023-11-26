from pyspark.sql import SparkSession

from pr5_tweets.spark.env import spark_conf


def get_spark_session():
    spark = (
        SparkSession.builder.appName("GraphFramesApp")
        .config(map=spark_conf)
        .getOrCreate()
    )
    spark.sparkContext.setCheckpointDir(f"/tmp")
    # spark.sparkContext.setLogLevel("INFO")
    return spark
