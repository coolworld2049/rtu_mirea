dataset_path = "hdfs://localhost:9000/user/ivanovnp/tweets"
spark_configurations = {
    "spark.executor.memory": "10g",  # Adjust based on available memory
    "spark.executor.cores": "4",  # Adjust based on available cores
    "spark.executor.instances": "3",  # Adjust based on the number of executors you want
    "spark.driver.memory": "6g",  # Adjust based on available memory
    "spark.driver.cores": "2",  # Adjust based on available cores
    "spark.default.parallelism": "12",  # Adjust based on the total number of cores
    "spark.sql.shuffle.partitions": "12",  # Adjust based on the total number of cores
    "spark.sql.autoBroadcastJoinThreshold": "52428800",  # Adjust based on the size of your data
    "spark.memory.fraction": "0.8",  # Adjust based on available memory
    "spark.memory.storageFraction": "0.2",  # Adjust based on available memory
    "spark.locality.wait": "0s",  # Reduce locality wait time
    "spark.network.timeout": "600s",  # Increase network timeout if needed
    "spark.streaming.kafka.maxRatePerPartition": "1000",  # Adjust based on your streaming workload
    "spark.streaming.backpressure.enabled": "true",  # Enable backpressure for streaming
    "spark.streaming.receiver.maxRate": "1000",  # Adjust based on your streaming workload
    "spark.task.cpus": "1",  # Set the number of CPU cores to use per task
    "spark.task.maxFailures": "3",  # Maximum number of failures before giving up on a task
    "spark.task.resource.gpu.amount": "0",  # Set the number of GPUs to use per task (if applicable)
    "spark.reducer.maxSizeInFlight": "128m",  # Control the size of map output data in flight
    "spark.shuffle.file.buffer": "1m",  # Buffer size for reading map output files
    "spark.reducer.maxReqsInFlight": "1",  # Control the maximum number of reduce tasks to fetch simultaneously
    "spark.executor.heartbeatInterval": "10s",  # Set executor heartbeat interval
    "spark.speculation": "false",  # Disable speculation to improve performance
}
