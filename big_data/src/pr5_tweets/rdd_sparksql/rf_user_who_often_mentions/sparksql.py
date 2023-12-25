from pr5_tweets.rdd_sparksql.rf_user_who_often_mentions.const import (
    politicians,
    russia_country_names,
)
from pr5_tweets.spark.env import get_spark_session, spark_work_dir

spark = get_spark_session()

df = spark.read.csv(
    f"{spark_work_dir}/ira_tweets_csv_hashed.csv",
    header=True,
    inferSchema=True,
)
df_filter = df.filter((df.account_language == "ru") & (df.tweet_language == "ru"))
df_filter.createOrReplaceTempView("tweets")
query = f"""
    SELECT userid, COUNT(*) AS mention_count
    FROM tweets
    WHERE account_language = 'ru' 
    OR LOWER(user_reported_location) RLIKE '{'|'.join(russia_country_names)}'
    AND tweet_language = 'ru'
    AND LOWER(tweet_text) RLIKE '{'|'.join(politicians)}'
    GROUP BY userid
    ORDER BY mention_count DESC
    LIMIT 1
"""
result = spark.sql(query)
result.show()
spark.stop()
