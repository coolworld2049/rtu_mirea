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

vertices_df = df.selectExpr("tweetid as id").distinct().orderBy("reply_count")
logger.info("vertices")
vertices_df.show(5)

edges_df = df.selectExpr(
    "tweetid as src", "in_reply_to_tweetid as dst", "userid"
).filter("dst is not null")
logger.info("edges_df")
edges_df.show(5)

G = GraphFrame(vertices_df, edges_df).dropIsolatedVertices()

negative_motif_df = G.find(f"(a)-[e]->(b);!(b)-[]->(a)")
logger.info(f"negative_motif_df")
negative_motif_df.printSchema()
negative_motif_df.show()

motif_edges_df = (
    edges_df.join(
        negative_motif_df,
        [
            negative_motif_df.e["src"] != edges_df.src,
            negative_motif_df.e["dst"] != edges_df.dst,
        ],
        "leftouter",
    )
    .where("src is not null and dst is not null")
    .select("src", "dst", "userid")
)
logger.info(f"motif_edges_df")
motif_edges_df.printSchema()
motif_edges_df.show()

n_th_level_df = motif_edges_df.groupBy("userid").count().orderBy(F.desc("count"))
logger.info("n_th_level_df")
n_th_level_df.show()

n_th_level = 4
n_th_level_userid = n_th_level_df.select("userid").take(n_th_level)[n_th_level - 1]
logger.info(
    f"The user who started the {n_th_level}-th longest chain is {n_th_level_userid}"
)

spark.stop()
