from graphframes import GraphFrame
from pyspark.sql import Row
from pyspark.sql import SparkSession

from pr5_tweets.env import dataset_path, spark_configurations


def create_graphframe(spark, user_rdd, messages_rdd):
    user_df = spark.createDataFrame(user_rdd.map(lambda x: Row(id=x[1])))
    message_df = spark.createDataFrame(
        messages_rdd.map(lambda x: Row(src=x[1], dst=x[2]))
    )
    graph = GraphFrame(user_df, message_df)
    return graph


def main():
    with SparkSession.builder.appName("GraphFramesExample").config(
        map={
            "spark.jars.packages": "graphframes:graphframes:0.8.2-spark3.0-s_2.12",
            "spark.checkpoint.auto": "true",
            **spark_configurations,
        }
    ).getOrCreate() as spark:
        spark.sparkContext.setCheckpointDir(f"{dataset_path}/rdd_checkpoint")
        rdd = spark.read.csv(
            f"{dataset_path}/ira_tweets_csv_hashed.csv", header=True, inferSchema=True
        )
        data_rdd = rdd.rdd.map(tuple)
        print(f"data_rdd: {data_rdd.take(1)}")
        n = 5
        target_user = (
            data_rdd.map(lambda x: (x[1], 1))
            .reduceByKey(lambda a, b: a + b)
            .sortBy(lambda x: x[1], ascending=False)
            .take(n)[-1][0]
        )
        print(f"target_user: {target_user}")

        # Find continuous chain of messages for the target user
        selected_user_messages = data_rdd.filter(lambda x: x[1] == target_user)
        print(f"selected_user_messages: {selected_user_messages.take(1)}")

        # Create GraphFrame
        graph = create_graphframe(spark, data_rdd, selected_user_messages)

        # Find connected components
        connected_components = graph.connectedComponents()

        # Visualize or perform further analysis on connected components
        connected_components.show()


if __name__ == "__main__":
    main()
