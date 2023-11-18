from graphframes import GraphFrame
from pyspark.sql.functions import desc, col

from pr5_tweets.spark.base import get_spark_session
from pr5_tweets.spark.env import spark_work_dir

spark = get_spark_session()

df = spark.read.csv(f"{spark_work_dir}/ira_tweets_csv_hashed.csv", header=True)
selected_cols = [
    "tweetid",
    "userid",
    "user_screen_name",
    "is_retweet",
    "in_reply_to_tweetid",
    "in_reply_to_userid",
    "retweet_userid",
    "retweet_tweetid",
    "retweet_count",
]
df = df.select(*selected_cols).limit(1000)

parquet_path = "ira_tweets_parquet"
df.write.parquet(parquet_path, mode="overwrite")
tweets_df = spark.read.parquet(parquet_path)

vertices = tweets_df.select("userid").withColumnRenamed("userid", "id").distinct()
edges = (
    tweets_df.filter(
        "in_reply_to_tweetid is not null and retweet_userid is not null and is_retweet is false"
    )
    .select("userid", "retweet_userid")
    .withColumnRenamed("userid", "src")
    .withColumnRenamed("retweet_userid", "dst")
)
# Create a GraphFrame
g = GraphFrame(vertices, edges)

# Define the motif pattern for a continuous chain of messages
motif = g.find("(id)-[]->(src)")
motif.show()

# Count the occurrences of the motif for each user
user_counts = motif.groupBy("a").count().orderBy(desc("count"))

# Choose the user who started the nth most frequent continuous chain
n = 2  # Replace with the desired value
nth_user = user_counts.select("a").collect()[n - 1][0]

# Display information about the user
print(f"User who started the {n}-th most frequent continuous chain: {nth_user}")
