from pyspark import SparkContext

from pr5_tweets.env import dataset_path

with SparkContext() as sc:
    rdd = sc.textFile(f"{dataset_path}/ira_tweets_csv_hashed.csv").map(
        lambda line: line.split(",")
    )
    ...
