import os

# Windows environment
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ["PATH"]

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType
)

# --------------------------------------------------
# 1. Create Spark Session
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("SmartWasteStreaming")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("Spark version:", spark.version)


# --------------------------------------------------
# 2. Define Waste Sensor JSON Schema
# --------------------------------------------------

schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("bin_id", StringType(), True),
    StructField("location", StringType(), True),
    StructField("fill_level", IntegerType(), True),
    StructField("weight_kg", DoubleType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("battery_level", IntegerType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("status", StringType(), True)
])


# --------------------------------------------------
# 3. Read data from Kafka
# --------------------------------------------------

df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "waste-sensor-data")
    .option("startingOffsets", "earliest")
    .load()
)

print("Kafka connection configured successfully!")


# --------------------------------------------------
# 4. Convert Kafka value from binary to JSON string
# --------------------------------------------------

json_df = df.select(
    col("value").cast("string").alias("json_value")
)


# --------------------------------------------------
# 5. Parse JSON into structured columns
# --------------------------------------------------

parsed_df = (
    json_df
    .select(
        from_json(col("json_value"), schema).alias("data")
    )
    .select("data.*")
)


# --------------------------------------------------
# 6. Write streaming data to console
# --------------------------------------------------

query = (
    parsed_df.writeStream
    .format("console")
    .outputMode("append")
    .option(
        "checkpointLocation",
        r"C:\temp\smart-waste-checkpoint"
    )
    .option("truncate", "false")
    .option("numRows", 20)
    .start()
)

print("Streaming query started!")

query.awaitTermination()