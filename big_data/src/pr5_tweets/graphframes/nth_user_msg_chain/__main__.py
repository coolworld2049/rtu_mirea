from pprint import pprint

import networkx as nx  # noqa
from graphframes import GraphFrame
from matplotlib import pyplot as plt  # noqa
from pyspark.sql import functions as F  # noqa

from pr5_tweets.spark.env import get_spark_session, spark_work_dir

spark = get_spark_session()

df = spark.read.csv(
    f"{spark_work_dir}/ira_tweets_csv_hashed.csv",
    header=True,
    inferSchema=True,
)

filtered_df = (
    df.select(
        "tweetid",
        "userid",
        "in_reply_to_tweetid",
        "in_reply_to_userid",
        "reply_count",
    )
    .withColumn("reply_count", F.col("reply_count").cast("int"))
    .filter("in_reply_to_tweetid is null or in_reply_to_tweetid RLIKE '^\\\d{18}$'")
)

vertices_df = filtered_df.selectExpr(
    "tweetid as id", "in_reply_to_userid", "reply_count"
)
edges_df = filtered_df.selectExpr("in_reply_to_tweetid as src", "tweetid as dst")

G = GraphFrame(vertices_df, edges_df)

nth_tweet_chain = 44

bfs_df = G.bfs(
    fromExpr="in_reply_to_userid is null",
    toExpr="in_reply_to_userid is not null and reply_count = 0",
    maxPathLength=nth_tweet_chain,
)
print("bfs_df schema:\n")
bfs_df.printSchema()

bfs_df_dict = bfs_df.limit(20).toPandas().to_dict(orient="records")
print("bfs_df_dict:\n")
pprint(bfs_df_dict)

bfs_df_grouped = (
    bfs_df.groupBy("to.in_reply_to_userid")
    .agg({"to.in_reply_to_userid": "count"})
    .withColumnRenamed(
        "count(to.in_reply_to_userid AS in_reply_to_userid)", "tweet_count"
    )
)
print("bfs_df_grouped:\n")
bfs_df_grouped.show()

bfs_df_filtered = bfs_df_grouped.filter(F.col("tweet_count") == nth_tweet_chain)
print(f"bfs_df_filtered:\n")
bfs_df_filtered.show()

target_userid = bfs_df_filtered.first()["in_reply_to_userid"]
print(f"target_userid: {target_userid}\n")
