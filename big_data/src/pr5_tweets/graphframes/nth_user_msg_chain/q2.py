from loguru import logger
from pyspark.sql.functions import col, desc

from pr5_tweets.spark.base import get_spark_session
from pr5_tweets.spark.env import spark_work_dir

spark = get_spark_session()

df = spark.read.csv(f"{spark_work_dir}/ira_tweets_csv_hashed.csv", header=True)
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
df = df.select(*selected_cols)
parquet_path = "ira_tweets_parquet"
df.write.parquet(parquet_path, mode="ignore")
df = spark.read.parquet(parquet_path)

df.filter("in_reply_to_tweetid is not null and is_retweet is false").show()
df.filter(
    "in_reply_to_userid is not null and in_reply_to_tweetid is not null and is_retweet is false"
).show()

tweet_messages = df.filter("is_retweet is null")
logger.info("tweet_messages")
tweet_messages.show()

retweet_messages = df.filter("is_retweet is not null")
logger.info("retweet_messages")
retweet_messages.show()

retweet_count = 2
nth_user = tweet_messages.select(*selected_cols).orderBy(desc("retweet_count"))
logger.info("nth_user")
nth_user.show(4)

nth_user = nth_user.collect()[retweet_count - 1][0]
logger.info(f"nth_user: {nth_user}")

nth_user_retweet_thread = retweet_messages.select(
    "userid",
    "tweetid",
    "retweet_userid",
    "retweet_tweetid",
).filter(col("retweet_userid") == nth_user)
logger.info(f"nth_user_retweet_thread: {nth_user_retweet_thread.count()}")
nth_user_retweet_thread.show()
