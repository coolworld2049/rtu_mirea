from graphframes import GraphFrame
from loguru import logger
from pyspark.sql import functions as F  # noqa
from pyspark.sql.functions import desc

from pr5_tweets.spark.base import get_spark_session
from pr5_tweets.spark.env import spark_work_dir

spark = get_spark_session()

df = spark.read.csv(
    f"{spark_work_dir}/ira_tweets_csv_hashed.csv",
    header=True,
    inferSchema=True,
).limit(10000)

selected_cols = [
    "tweetid",
    "userid",
    "in_reply_to_tweetid",
    "in_reply_to_userid",
    "retweet_userid",
    "retweet_tweetid",
]
df = df.select(*selected_cols).filter(
    "in_reply_to_tweetid is not null or retweet_tweetid is not null"
)
logger.info("df")
df.show()

# Create vertices DataFrame
vertices = df.selectExpr("userid as id").distinct()

# Create edges DataFrame
edges = df.selectExpr(
    "userid as src",
    "coalesce(in_reply_to_tweetid, retweet_tweetid) as dst",
    "tweetid as edge_id",
).filter("src is not null and dst is not null")

# Create a GraphFrame
g = GraphFrame(vertices, edges)

# Find connected components
connected_components = g.connectedComponents()

# Group connected components by user ID
user_tweet_chains = (
    connected_components.groupBy("component", "id")
    .agg({"component": "count"})
    .orderBy(desc("count(component)"))
)

# Show the result
user_tweet_chains.show()

# Stop the Spark session
spark.stop()
