from graphframes import GraphFrame
from pyspark.sql import functions as F  # noqa

from pr5_tweets.spark.base import get_spark_session
from pr5_tweets.spark.env import spark_work_dir

spark = get_spark_session()

df = spark.read.csv(
    f"{spark_work_dir}/ira_tweets_csv_hashed.csv",
    header=True,
    inferSchema=True,
).cache()

selected_cols = [
    "tweetid",
    "userid",
    "is_retweet",
    "in_reply_to_tweetid",
    "in_reply_to_userid",
    "retweet_userid",
    "retweet_tweetid",
    "retweet_count",
]
df = df.select(*selected_cols).filter(
    "in_reply_to_tweetid is null or in_reply_to_tweetid RLIKE '^\\d{18}$'"
)
df.show()

v = df.select("tweetid").withColumnRenamed("tweetid", "id")
e = (
    df.select("tweetid", "in_reply_to_tweetid")
    .withColumnRenamed("tweetid", "src")
    .withColumnRenamed("in_reply_to_tweetid", "dst")
)
g = GraphFrame(v, e)
g.connectedComponents().show()
g.inDegrees.show()
g.inDegrees.orderBy("inDegree", ascending=False).show()

# filteredInDegrees =
# filteredInDegrees = spark.sql(
#     "select * from inDegrees "
#     "where exists (select vertices.id from vertices where vertices.id = inDegrees.id) "
#     "order by inDegree desc"
# )


# tweet_messages = df.filter("is_retweet is null")
# logger.info("tweet_messages")
# tweet_messages.show()
#
# retweet_messages = df.filter("is_retweet is not null")
# logger.info("retweet_messages")
# retweet_messages.show()
#
# retweet_count = 2
# nth_user = tweet_messages.select(*selected_cols).orderBy(desc("retweet_count"))
# logger.info("nth_user")
# nth_user.show(4)
#
# nth_user = nth_user.collect()[retweet_count - 1][0]
# logger.info(f"nth_user: {nth_user}")
#
# nth_user_retweet_thread = retweet_messages.select(
#     "userid",
#     "tweetid",
#     "retweet_userid",
#     "retweet_tweetid",
# ).filter(col("retweet_userid") == nth_user)
# logger.info(f"nth_user_retweet_thread: {nth_user_retweet_thread.count()}")
# nth_user_retweet_thread.show()
