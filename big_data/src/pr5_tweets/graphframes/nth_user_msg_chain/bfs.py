from graphframes import GraphFrame
from loguru import logger
from pyspark.sql import functions as F

from pr5_tweets.spark.base import get_spark_session

spark = get_spark_session()

# Load the dataset
df = spark.read.csv(
    "file:///home/ivanovnp/tweets/ira_tweets_csv_hashed.csv",
    header=True,
    inferSchema=True,
)

# Select relevant columns and filter out non-replies
selected_cols = ["tweetid", "userid", "in_reply_to_tweetid", "in_reply_to_userid"]
df = df.select(*selected_cols).filter("in_reply_to_tweetid is not null")

# Create vertices and edges DataFrames
vertices_df = df.selectExpr("tweetid as id", "userid").distinct()
edges_df = df.selectExpr("in_reply_to_tweetid as src", "tweetid as dst")

# Create a GraphFrame
G = GraphFrame(vertices_df, edges_df)

# Perform BFS to find the connected components
random_tweet_id = df.select("tweetid").first()["tweetid"]
bfs_result = G.bfs(f"id = '{random_tweet_id}'", "dst = id")

# Find the largest connected component
largest_cc = bfs_result.groupBy("component").count().sort(F.desc("count")).limit(1)

# Extract the largest connected component's ID
largest_cc_id = largest_cc.select("component").collect()[0][0]

logger.info(f"Largest Connected Component ID: {largest_cc_id}")

# Filter vertices of the largest connected component
largest_cc_vertices_df = vertices_df.filter(vertices_df.id.isin(largest_cc_id))

# Display the vertices of the largest connected component
logger.info("Vertices of the Largest Connected Component:")
largest_cc_vertices_df.show()

# Stop the Spark session
spark.stop()
