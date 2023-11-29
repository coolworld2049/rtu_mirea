# # Choose a starting vertex for BFS (you can choose any vertex)
# starting_vertex_id = vertices_df.take(1)[0]["id"]
#
# # Run BFS and accumulate the count of users in each level
# bfs_result = g.bfs(
#     fromExpr=f"id = '{starting_vertex_id}'",
#     toExpr=f"id != '{starting_vertex_id}'",
#     maxPathLength=nth,
#     edgeFilter="src != dst"
# )
# """
# root
#  |-- from: struct (nullable = false)
#  |    |-- id: string (nullable = true)
#  |    |-- tweetid: long (nullable = true)
#  |-- e0: struct (nullable = false)
#  |    |-- src: string (nullable = true)
#  |    |-- dst: string (nullable = true)
#  |-- to: struct (nullable = false)
#  |    |-- id: string (nullable = true)
#  |    |-- tweetid: long (nullable = true)
# """
# logger.info("bfs_result")
# bfs_result.show()
#
# n_th_level = (
#     bfs_result.groupBy("from.id")
#     .agg({"from.id": "count"})
#     .withColumnRenamed("count(from.id AS id)", "user_count")
#     .orderBy(F.desc("user_count"))
# )
# logger.info("n_th_level")
# n_th_level.show()
#
# logger.info(f"The user who started the {nth}-th longest chain is")
# n_th_level.limit(1).show()
#
# spark.stop()
