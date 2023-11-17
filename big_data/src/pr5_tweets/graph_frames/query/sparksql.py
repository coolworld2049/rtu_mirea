from pyspark.sql import SparkSession

from pr5_tweets.env import dataset_path

with SparkSession.builder.getOrCreate() as spark:
    df = spark.read.csv(
        f"{dataset_path}/ira_tweets_csv_hashed.csv",
        header=True,
        inferSchema=True,
    )
    ...
