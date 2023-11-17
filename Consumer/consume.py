from pyspark.sql import SparkSession, Row
from pyspark.context import SparkContext
import os
#from IPython.display import display, clear_output
import time


def main_jupyter_code():
    """
    deprecated function used solely to document code that worked on the jupyter notebook version
    """
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars /home/jovyan/spark-streaming-kafka-assembly_2.10-1.6.1.jar pyspark-shell'

    spark = SparkSession.builder \
    .master("spark://172.18.0.2:7077") \
    .appName("spark_on_docker") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
    .getOrCreate()
#-------------New Notebook Cell----------------#
    df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "kafka_container:9093").option("subscribe", "LazerScan").option("startingOffsets", "earliest").option("maxOffsetsPerTrigger", 100).load()
    print(str(df.isStreaming))
    df.printSchema()
#-------------New Notebook Cell----------------#
    query = df.withWatermark("timestamp", "3 minutes") \
        .writeStream \
        .outputMode("append") \
        .format("memory") \
        .queryName("LazerScanQuery1") \
        .start()
#-------------New Notebook Cell----------------#
    while True:
        # clear_output(wait=True)
        # display(query.status)
        # display(spark.sql('SELECT CAST(value AS STRING) FROM LazerScanQuery1').show(200,truncate=False))
        # display(query.lastProgress)
        # display(query.status)
        # display(query.isActive)
        time.sleep(1)

def main():
    # os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars /home/jovyan/spark-streaming-kafka-assembly_2.10-1.6.1.jar pyspark-shell'
    # os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0, org.apache.spark:spark-streaming-kafka-0-10_2.13:3.5.0 pyspark-shell'
    # .config('spark.jars.packages', 'org.apache.spark:spark-streaming-kafka-0-10_2.13:3.5.0') \

    # spark = SparkSession.builder \
    # .master("local[*]") \
    # .appName("spark_on_docker") \
    # .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0') \
    # .config('spark.jars.packages', 'org.apache.spark:spark-streaming-kafka-0-10-assembly_2.12:3.5.0') \
    # .getOrCreate()

    # os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10-assembly_2.12:3.5.0,  pyspark-shell'

    spark = SparkSession \
    .builder \
    .appName("Streaming from Kafka") \
    .config("spark.streaming.stopGracefullyOnShutdown", True) \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0') \
    .master("local[*]") \
    .getOrCreate()

    df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka_container:9093") \
    .option("subscribe", "LazerScan") \
    .option("startingOffsets", "earliest") \
    .option("maxOffsetsPerTrigger", 100) \
    .load()

    print(str(df.isStreaming))
    df.printSchema()

    query = df.selectExpr("*") \
    .writeStream \
    .format("console") \
    .start()

    query.awaitTermination()


    # query = df \
    #     .writeStream \
    #     .outputMode("append") \
    #     .format("memory") \
    #     .queryName("LazerScanQuery1") \
    #     .start()

    # while True:
    #     # print(spark.sql("""SELECT * FROM LazerScanQuery1""").show(200,truncate=False))
    #     print(spark.sql("SELECT * FROM range(10) where id > 7").show())
    #     time.sleep(1)


if __name__ == "__main__":
    main()