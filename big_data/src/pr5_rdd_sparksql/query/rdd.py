from pyspark import SparkContext

from pr5_rdd_sparksql.query.const import politicians, russia_country_names
from pr5_rdd_sparksql.query.env import dataset_path

with SparkContext() as sc:
    rdd = sc.textFile(f"{dataset_path}/ira_tweets_csv_hashed.csv").map(
        lambda line: line.split(",")
    )
    query = (
        rdd.filter(
            lambda row: row[10] == '"ru"'
            and row[11] == '"ru"'
            or row[4] in russia_country_names
            and any(p_lower in row[12].lower() for p_lower in politicians)
        )
        .map(lambda row: (row[1], 1))
        .reduceByKey(lambda a, b: a + b)
    )
    q_collect = query.collect()
    result = sc.parallelize(q_collect).sortBy(lambda x: x[1], ascending=False)
    print(f"result: {result.take(1)}")
