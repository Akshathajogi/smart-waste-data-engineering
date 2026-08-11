import os

# ==============================
# Windows Hadoop Configuration
# ==============================

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ["PATH"]


# ==============================
# Imports
# ==============================

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json,
    col,
    when,
    to_timestamp
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType
)


# ==============================
# Create Spark Session
# ==============================

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


# ==============================
# Define Kafka JSON Schema
# ==============================

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


# ==============================
# Read Stream from Kafka
# ==============================

raw_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "waste-sensor-data")
    .option("startingOffsets", "earliest")
    .load()
)

print("Kafka stream connected!")


# ==============================
# Convert Kafka value to String
# ==============================

json_stream = raw_stream.select(
    col("value").cast("string").alias("json_data")
)


# ==============================
# Parse JSON
# ==============================

parsed_stream = json_stream.select(
    from_json(col("json_data"), schema).alias("data")
).select("data.*")


# ==============================
# Convert timestamp
# ==============================

clean_stream = parsed_stream.withColumn(
    "timestamp",
    to_timestamp(col("timestamp"))
)


# ==============================
# Create Collection Priority
# ==============================

final_stream = clean_stream.withColumn(
    "collection_priority",
    when(col("fill_level") >= 90, "Critical")
    .when(col("fill_level") >= 70, "High")
    .when(col("fill_level") >= 50, "Medium")
    .otherwise("Low")
)


# ==============================
# Create Battery Status
# ==============================

final_stream = final_stream.withColumn(
    "battery_status",
    when(col("battery_level") <= 20, "Critical")
    .when(col("battery_level") <= 40, "Low")
    .otherwise("Healthy")
)


# ==============================
# Write Processed Stream to Parquet
# ==============================

output_path = r"D:\certificates\smart-waste-data-engineering\data\processed\waste_sensor"

checkpoint_path = r"C:\temp\smart-waste-parquet-checkpoint"

query = (
    final_stream.writeStream
    .format("parquet")
    .outputMode("append")
    .option("path", output_path)
    .option("checkpointLocation", checkpoint_path)
    .trigger(processingTime="10 seconds")
    .start()
)

print("Smart Waste streaming pipeline started!")
print("Processed data is being saved to:")
print(output_path)

query.awaitTermination()