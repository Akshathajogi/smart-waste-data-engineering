from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    sum,
    count,
    max,
    round,
    desc
)

# ==========================================
# Create Spark Session
# ==========================================

spark = (
    SparkSession.builder
    .appName("Smart Waste Analytics")
    .master("local[*]")
    .config("spark.hadoop.io.nativeio.enabled", "false")
    .config(
        "spark.sql.warehouse.dir",
        "file:///D:/certificates/smart-waste-data-engineering/spark-warehouse"
    )
    .getOrCreate()
)

print("======================================")
print("Smart Waste Analytics")
print("======================================")

# ==========================================
# Input / Output Paths
# ==========================================

input_path = r"D:\certificates\smart-waste-data-engineering\data\processed\waste_sensor"

output_path = r"D:\certificates\smart-waste-data-engineering\data\processed\analytics"

# ==========================================
# Read Processed Parquet Data
# ==========================================

df = spark.read.parquet(input_path)

print("Data loaded successfully!")

df.printSchema()
df.show(10)

# ==========================================
# 1. Overall Summary
# ==========================================

print("\n======================================")
print("OVERALL SUMMARY")
print("======================================")

overall_summary = df.select(
    count("*").alias("total_records"),
    round(avg("fill_level"), 2).alias("avg_fill_level"),
    round(sum("weight_kg"), 2).alias("total_waste_kg"),
    round(avg("temperature"), 2).alias("avg_temperature"),
    round(avg("battery_level"), 2).alias("avg_battery_level")
)

overall_summary.show(truncate=False)

# Save
overall_summary.write.mode("overwrite").parquet(
    output_path + r"\overall_summary"
)

# ==========================================
# 2. Collection Priority
# ==========================================

print("\n======================================")
print("COLLECTION PRIORITY")
print("======================================")

collection_priority = (
    df.groupBy("collection_priority")
    .count()
    .orderBy(desc("count"))
)

collection_priority.show()

# Save
collection_priority.write.mode("overwrite").parquet(
    output_path + r"\collection_priority"
)

# ==========================================
# 3. Battery Status
# ==========================================

print("\n======================================")
print("BATTERY STATUS")
print("======================================")

battery_status = (
    df.groupBy("battery_status")
    .count()
    .orderBy(desc("count"))
)

battery_status.show()

# Save
battery_status.write.mode("overwrite").parquet(
    output_path + r"\battery_status"
)

# ==========================================
# 4. Location-wise Analysis
# ==========================================

print("\n======================================")
print("LOCATION-WISE ANALYSIS")
print("======================================")

location_analysis = (
    df.groupBy("location")
    .agg(
        count("*").alias("sensor_readings"),
        round(avg("fill_level"), 2).alias("avg_fill_level"),
        round(sum("weight_kg"), 2).alias("total_waste_kg"),
        round(avg("battery_level"), 2).alias("avg_battery_level")
    )
    .orderBy(desc("avg_fill_level"))
)

location_analysis.show(truncate=False)

# Save
location_analysis.write.mode("overwrite").parquet(
    output_path + r"\location_analysis"
)

# ==========================================
# 5. Critical Bins
# ==========================================

print("\n======================================")
print("CRITICAL BINS")
print("======================================")

critical_bins = (
    df.filter(
        df.collection_priority == "Critical"
    )
    .select(
        "bin_id",
        "location",
        "fill_level",
        "weight_kg",
        "battery_level",
        "collection_priority"
    )
    .orderBy(desc("fill_level"))
)

critical_bins.show(20, truncate=False)

# Save
critical_bins.write.mode("overwrite").parquet(
    output_path + r"\critical_bins"
)

# ==========================================
# 6. Bin-wise Performance
# ==========================================

print("\n======================================")
print("BIN-WISE ANALYSIS")
print("======================================")

bin_analysis = (
    df.groupBy("bin_id", "location")
    .agg(
        count("*").alias("readings"),
        round(avg("fill_level"), 2).alias("avg_fill_level"),
        round(max("fill_level"), 2).alias("max_fill_level"),
        round(sum("weight_kg"), 2).alias("total_waste_kg"),
        round(avg("battery_level"), 2).alias("avg_battery_level")
    )
    .orderBy(desc("avg_fill_level"))
)

bin_analysis.show(20, truncate=False)

# Save
bin_analysis.write.mode("overwrite").parquet(
    output_path + r"\bin_analysis"
)

# ==========================================
# Stop Spark
# ==========================================

spark.stop()

print("\n======================================")
print("Analytics completed successfully!")
print("Analytics output saved successfully!")
print("======================================")