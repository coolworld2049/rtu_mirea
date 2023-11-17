from pyspark.sql import SparkSession

from pr5_rdd_sparksql.query.env import dataset_path
from pr5_rdd_sparksql.query.const import politicians, russia_country_names

with SparkSession.builder.getOrCreate() as spark:
    df = spark.read.csv(
        f"{dataset_path}/ira_tweets_csv_hashed.csv",
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
