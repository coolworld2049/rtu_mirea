import time
from pprint import pprint

from pr5_tweets.rdd_sparksql.rf_user_who_often_mentions.const import (
    politicians,
    russia_country_names,
)
from pr5_tweets.spark.env import spark_work_dir, get_spark_session

spark = get_spark_session()

start_time = time.time()
rdd = spark.sparkContext.textFile(f"{spark_work_dir}/ira_tweets_csv_hashed.csv").map(
    lambda line: line.split(",")
)

filtered_rdd = rdd.filter(
    lambda row: row[10] == '"ru"'
    and row[11] == '"ru"'
    or row[4] in russia_country_names
    and any(p_lower in row[12].lower() for p_lower in politicians)
)

mapped_rdd = filtered_rdd.map(lambda row: (row[1], 1))
reduced_rdd = mapped_rdd.reduceByKey(lambda a, b: a + b)

mapped_data = mapped_rdd.collect()
print("Data after map:")
pprint(mapped_data[:10])

reduced_data = reduced_rdd.collect()
print("Data after reduceByKey:")
pprint(reduced_data[:10])

result = spark.sparkContext.parallelize(reduced_data, numSlices=5).sortBy(
    lambda x: x[1], ascending=False
)
print(f"Result: {result.take(1)}")
spark.stop()
stop_time = time.time()
print(f"Elapsed time: {stop_time - start_time:.2f} sec")