from graphframes import GraphFrame
from loguru import logger
from pyspark.sql import functions as F  # noqa

from pr5_tweets.spark.env import get_spark_session

spark = get_spark_session()

df = spark.read.csv(
    "file:///home/ivanovnp/tweets/ira_tweets_csv_hashed.csv",
    header=True,
    inferSchema=True,
)

selected_cols = [
    "tweetid",
    "userid",
    "in_reply_to_tweetid",
    "in_reply_to_userid",
]
df = df.select(*selected_cols).filter(
    "in_reply_to_tweetid is null or in_reply_to_tweetid RLIKE '^\\\d{18}$'"  # noqa
)
logger.info("df")
df.show()

vertices_df = df.selectExpr("tweetid as id", "userid").distinct()
logger.info("vertices")
vertices_df.show(5)

edges_df = df.selectExpr("tweetid as src", "in_reply_to_tweetid as dst")
logger.info("edges_df")
edges_df.show(5)

G = GraphFrame(vertices_df, edges_df)

cc = G.connectedComponents()

cc_df = cc.groupBy("component").count().sort(F.desc("count"))
logger.info("connected_components_df")
cc_df.show()

n_th = 1
n_th_component = cc_df.take(n_th)[0]["component"]
logger.info(f"{n_th} component: {n_th_component}")

cc_vertices_df = cc.filter(F.col("component") == n_th_component)
logger.info("connected_component_vertices")
cc_vertices_df.show()

n_th_level_df = cc_vertices_df.join(
    edges_df,
    cc_vertices_df.id == edges_df.src,
    "leftouter",
)
logger.info("n_th_level_df")
n_th_level_df.show()

spark.stop()
