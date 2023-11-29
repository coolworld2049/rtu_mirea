from graphframes import GraphFrame
from loguru import logger
from pyspark.sql import functions as F  # noqa

from pr5_tweets.spark.base import get_spark_session

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
    "retweet_userid",
    "retweet_tweetid",
    "reply_count",
]
df = df.select(*selected_cols).filter(
    "in_reply_to_tweetid is null or in_reply_to_tweetid RLIKE '^\\\d{18}$'"  # noqa
)
logger.info("df")
df.show()

vertices_df = df.selectExpr("userid as id").distinct().orderBy("reply_count")
logger.info("vertices")
vertices_df.show(5)

edges_df = df.selectExpr(
    "userid as src", "in_reply_to_userid as dst", "tweetid as relationship"
).filter("dst is not null")
logger.info("edges_df")
edges_df.show(5)

g = GraphFrame(vertices_df, edges_df).dropIsolatedVertices()

motif_pattern = f"(a)-[]->(b);(b)-[e]->(a)"
logger.info(f"motif_pattern: {motif_pattern}")

motif_df = g.find(motif_pattern).filter("a.id != b.id")
logger.info(f"motif_df - count: {motif_df.count()}")
motif_df.show()
motif_df.printSchema()

n_th_level_df = motif_df.groupBy("a.id").count().orderBy(F.desc("count"))
logger.info("n_th_level_df")
n_th_level_df.show()

n_th_level = 4
n_th_level_userid = n_th_level_df.select("id").take(n_th_level)[n_th_level - 1]["id"]
logger.info(
    f"The user who started the {n_th_level}-th longest chain is {n_th_level_userid}"
)

spark.stop()
