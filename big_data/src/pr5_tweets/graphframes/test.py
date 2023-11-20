from pyspark.sql import SparkSession
from graphframes import GraphFrame
import pandas as pd

from pr5_tweets.spark.env import spark_conf, spark_work_dir

# Initialize Spark session
spark = (
    SparkSession.builder.appName("GraphFramesDemo").config(map=spark_conf).getOrCreate()
)
spark.sparkContext.setCheckpointDir(f"{spark_work_dir}/rdd_checkpoint")
spark.sparkContext.setLogLevel("INFO")

# Sample data for vertices (nodes)
vertices_data = [("A", "Alice"), ("B", "Bob"), ("C", "Charlie"), ("D", "David")]
vertices_df = pd.DataFrame(vertices_data, columns=["id", "name"])
vertices = spark.createDataFrame(vertices_df)

# Sample data for edges
edges_data = [("A", "B"), ("B", "C"), ("C", "A"), ("D", "A")]
edges_df = pd.DataFrame(edges_data, columns=["src", "dst"])
edges = spark.createDataFrame(edges_df)

# Create a GraphFrame
graph = GraphFrame(vertices, edges)

# Display the vertices and edges
print("Vertices:")
graph.vertices.show()

print("Edges:")
graph.edges.show()

# Perform a simple query to find connected components
connected_components = graph.connectedComponents()
print("Connected Components:")
connected_components.show()

# Visualize the graph (requires networkx and matplotlib for visualization)
try:
    import networkx as nx
    import matplotlib.pyplot as plt

    nx_graph = nx.from_pandas_edgelist(edges_df, "src", "dst")
    nx.draw(
        nx_graph,
        with_labels=True,
        font_weight="bold",
        node_color="skyblue",
        edge_color="gray",
    )
    plt.show()
except ImportError:
    print("NetworkX and Matplotlib not installed. Visualization will be skipped.")

# Stop the Spark session
spark.stop()
