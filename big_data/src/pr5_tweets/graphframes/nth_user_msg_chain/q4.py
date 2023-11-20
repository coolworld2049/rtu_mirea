import networkx as nx
from graphframes import GraphFrame
from loguru import logger
from matplotlib import pyplot as plt
from pyspark.sql import functions as F

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
    "in_reply_to_tweetid is null or in_reply_to_tweetid RLIKE '^\\\d{18}$'"
)
logger.info("df")
df.show()

vertices = df.selectExpr("tweetid as id").distinct()
logger.info("vertices")
vertices.show(4)

edges = df.selectExpr(
    "tweetid as src",
    "in_reply_to_tweetid as dst",
    "in_reply_to_userid",
    "userid",
    "reply_count",
)
logger.info("edges")
edges.show(4)

g = GraphFrame(vertices, edges)

user_started_chain = (
    g.inDegrees.filter("inDegree != 0 and id is not null")
    .join(vertices, "id")
    .withColumnRenamed("id", "src")
    .join(edges, "src")
    .filter("dst is not null and in_reply_to_userid is not null")
    .filter("reply_count > 0")
    .filter("in_reply_to_userid != userid")
    .orderBy(F.desc("inDegree"))
)
logger.info("user_started_chain")
user_started_chain.show()

user_started_chain_user_id = user_started_chain.take(1)[0]["userid"]
logger.info(f"user_started_chain_user_id: {user_started_chain_user_id}")

nth_chain = 1
filtered_user_started_chain = user_started_chain.filter(
    F.col("userid") == user_started_chain_user_id
)
filtered_user_started_chain_max = (
    filtered_user_started_chain.groupBy("inDegree", "userid")
    .agg({"inDegree": "max"})
    .orderBy(F.desc("max(inDegree)"))
)
logger.info("filtered_user_started_chain_max")
filtered_user_started_chain_max.show()

filtered_user_started_chain = filtered_user_started_chain.filter(
    F.col("inDegree") == filtered_user_started_chain_max.take(1)[0]["max(inDegree)"]
)
logger.info(
    f"filtered_user_started_chain - count: {filtered_user_started_chain.count()}"
)
filtered_user_started_chain.show()

plt.figure(figsize=(19, 8), dpi=100)

nx_graph = nx.MultiDiGraph()

for row in filtered_user_started_chain.collect():
    nx_graph.add_node(row["src"])
    nx_graph.add_node(row["dst"])
    nx_graph.add_node(row["userid"], color="blue")
    nx_graph.add_node(row["in_reply_to_userid"], color="magenta")

for row in filtered_user_started_chain.collect():
    # dst - in_reply_to_tweet_id src - tweetid
    # in_reply_to_userid -> userid -> tweet_id (src) -> in_reply_to_tweet_id (dst)
    # nx_graph.add_edge(row["in_reply_to_userid"], row["userid"])
    # nx_graph.add_edge(row["userid"], row["src"])
    # nx_graph.add_edge(row["src"], row["dst"])

    # tweet_id (src) -> in_reply_to_tweet_id -> (dst) in_reply_to_userid -> userid
    nx_graph.add_edge(row["src"], row["dst"])
    nx_graph.add_edge(row["dst"], row["in_reply_to_userid"])
    nx_graph.add_edge(row["in_reply_to_userid"], row["userid"])
pos = nx.spring_layout(nx_graph, k=0.5)
nx.draw(
    nx_graph,
    pos=pos,
    with_labels=True,
    node_size=60,
    font_size=8,
    edge_color="gray",
    connectionstyle="arc3,rad=0.2",  # adjust the curvature of edges
)

plt.savefig("graph_bidirectional.jpg", format="jpg")

spark.stop()
