from graphframes import GraphFrame
from loguru import logger
from pyspark.sql.functions import col

from pr5_tweets.spark.base import get_spark_session
from pr5_tweets.spark.env import spark_work_dir

spark = get_spark_session()

selected_cols = ["tweetid", "userid", "retweet_userid"]
df = (
    spark.read.csv(f"{spark_work_dir}/ira_tweets_csv_hashed.csv", header=True)
    .select(*selected_cols)
    .limit(1000)
)

parquet_path = "ira_tweets_parquet"
df.write.parquet(parquet_path, mode="overwrite")
df = spark.read.parquet(parquet_path)

logger.info("df")
df.show()


vertices = (
    df.filter(col("userid").isNotNull())
    .select("userid")
    .withColumnRenamed("userid", "id")
)
logger.info("vertices")
vertices.show(40)

edges = (
    df.select("userid", "retweet_userid")
    .where(~col("retweet_userid").like("NULL|true|false"))
    .withColumnRenamed("userid", "src")
    .withColumnRenamed("retweet_userid", "dst")
)
logger.info("edges")
edges.show(40)

g = GraphFrame(vertices, edges)

connected_components = g.connectedComponents()
logger.info("connected_components")
connected_components.show(40)

n = 2
user_count = df.groupBy("userid").count()
nth_user = (
    user_count.orderBy("count", ascending=False).select("userid").collect()[n - 1][0]
)
logger.info(f"nth_user: {nth_user}")
user_id_comp = g.vertices.filter(col("id") == nth_user).select("id").first()[0]
continuous_chain = connected_components.filter(col("component") == user_id_comp)

logger.info("continuous_chain")
continuous_chain.show(40)
spark.stop()
