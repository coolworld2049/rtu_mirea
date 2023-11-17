from pyspark.sql import SparkSession

from pr5_rdd_sparksql.queries.v1.const import politicians_tuple

dataset_path = "hdfs://localhost:9000/user/ivanovnp/tweets"

with SparkSession.builder.getOrCreate() as spark:
    df = spark.read.csv(
        f"{dataset_path}/ira_tweets_csv_hashed.csv",
        header=True,
        inferSchema=True,
    )
    df.createOrReplaceTempView("tweets")
    politicians = tuple(
        map(lambda c: [f"'%{str(x).lower()}%'" for x in c], politicians_tuple)
    )
    politicians_flat = {x for p in politicians for x in p}
    query = f"""
        SELECT userid, COUNT(*) AS mention_count
        FROM tweets
        WHERE account_language = 'ru' AND tweet_language = 'ru'
        AND LOWER(tweet_text) LIKE ANY ({', '.join(politicians_flat)})
        GROUP BY userid
        ORDER BY mention_count DESC
        LIMIT 1
    """
    result = spark.sql(query)
    result.show(truncate=False)
    result.write.csv(f"{dataset_path}/output/v1_sparksql_result", header=True)
    spark.stop()
