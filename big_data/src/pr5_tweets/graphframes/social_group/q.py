from graphframes import GraphFrame

from pr5_tweets.spark.base import get_spark_session
from pr5_tweets.spark.env import spark_work_dir
from pyspark.sql import functions as F

# Create Spark session
spark = get_spark_session()

# Load data from CSV file
df = spark.read.csv(f"{spark_work_dir}/ira_tweets_csv_hashed.csv", header=True, inferSchema=True).limit(1000)

# Create GraphFrame
vertices = (
    df.select("user_screen_name", "user_reported_location")
    .distinct()
    .withColumnRenamed("user_screen_name", "id")
)
edges = (
    df.select("user_screen_name", "retweet_userid")
    .withColumnRenamed("user_screen_name", "src")
    .withColumnRenamed("retweet_userid", "dst")
)

g = GraphFrame(vertices, edges)
g

spark.stop()