from pyspark.sql import SparkSession, Row
from pyspark.context import SparkContext
import os
import time


def main():
    spark = SparkSession \
    .builder \
    .appName("Streaming from Kafka") \
    .config("spark.streaming.stopGracefullyOnShutdown", True) \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
    .master("local[*]") \
    .getOrCreate()

    df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka_container:9093") \
    .option("subscribe", "RandomNumber") \
    .option("startingOffsets", "latest") \
    .option("maxOffsetsPerTrigger", 100) \
    .load()

    print(str(df.isStreaming))
    df.printSchema()

    execution_counter = 0
    while execution_counter <= 50:
        query = df.selectExpr("*") \
        .writeStream \
        .format("console") \
        .outputMode("append") \
        .start() \
        .awaitTermination(7)
    
        execution_counter +=1
        print("Execution counter: " + str(execution_counter))

    

if __name__ == "__main__":
    main()