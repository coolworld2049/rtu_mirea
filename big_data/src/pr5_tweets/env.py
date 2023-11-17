dataset_path = "hdfs://localhost:9000/user/ivanovnp/tweets"
spark_configurations = {
    "spark.executor.memory": "6g",  # Set the memory per executor (adjust based on your total memory)
    "spark.executor.cores": "3",  # Set the number of cores per executor
    "spark.executor.instances": "3",  # Set the number of executor instances
    "spark.driver.memory": "4g",  # Set the memory for the driver
    "spark.driver.cores": "3",  # Set the number of cores for the driver
    "spark.default.parallelism": "12",  # Set the default parallelism (usually equal to the total number of cores)
    "spark.sql.shuffle.partitions": "12",  # Set the number of partitions for shuffling operations
    "spark.memory.fraction": "0.8",  # Fraction of heap space used for Spark's memory
    "spark.memory.storageFraction": "0.2",  # Fraction of heap space used for storage memory
    "spark.network.timeout": "600s",  # Increase network timeout if needed
    "spark.task.cpus": "1",  # Set the number of CPU cores to use per task
    "spark.reducer.maxSizeInFlight": "128m",  # Control the size of map output data in flight
    "spark.shuffle.file.buffer": "1m",  # Buffer size for reading map output files
    "spark.executor.heartbeatInterval": "10s",  # Set executor heartbeat interval
    "spark.speculation": "false",  # Disable speculation to improve performance
}
