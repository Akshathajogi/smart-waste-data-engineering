from pyspark.sql import SparkSession

# ==========================================
# Create Spark Session
# ==========================================

spark = (
    SparkSession.builder
    .appName("Smart Waste SQL Analytics")
    .master("local[*]")
    .config(
        "spark.sql.warehouse.dir",
        "file:///D:/certificates/smart-waste-data-engineering/spark-warehouse"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("======================================")
print("Smart Waste SQL Analytics")
print("======================================")

# ==========================================
# Base path
# ==========================================

base_path = (
    r"D:\certificates\smart-waste-data-engineering"
    r"\data\processed\analytics"
)

# ==========================================
# Load Parquet datasets
# ==========================================

datasets = {
    "overall_summary": "overall_summary",
    "collection_priority": "collection_priority",
    "battery_status": "battery_status",
    "location_analysis": "location_analysis",
    "critical_bins": "critical_bins",
    "bin_analysis": "bin_analysis",
}

for table_name, folder_name in datasets.items():

    path = f"{base_path}\\{folder_name}"

    df = spark.read.parquet(path)

    df.createOrReplaceTempView(table_name)

    print(f"Loaded SQL view: {table_name}")


# ==========================================
# 1. Overall Summary
# ==========================================

print("\n======================================")
print("1. OVERALL SUMMARY")
print("======================================")

spark.sql("""
SELECT *
FROM overall_summary
""").show(truncate=False)


# ==========================================
# 2. Collection Priority
# ==========================================

print("\n======================================")
print("2. COLLECTION PRIORITY")
print("======================================")

spark.sql("""
SELECT
    collection_priority,
    count
FROM collection_priority
ORDER BY count DESC
""").show(truncate=False)


# ==========================================
# 3. Battery Status
# ==========================================

print("\n======================================")
print("3. BATTERY STATUS")
print("======================================")

spark.sql("""
SELECT
    battery_status,
    count
FROM battery_status
ORDER BY count DESC
""").show(truncate=False)


# ==========================================
# 4. Location Analysis
# ==========================================

print("\n======================================")
print("4. LOCATION ANALYSIS")
print("======================================")

spark.sql("""
SELECT
    location,
    sensor_readings,
    avg_fill_level,
    total_waste_kg,
    avg_battery_level
FROM location_analysis
ORDER BY avg_fill_level DESC
""").show(truncate=False)


# ==========================================
# 5. Critical Bins
# ==========================================

print("\n======================================")
print("5. CRITICAL BINS")
print("======================================")

spark.sql("""
SELECT
    bin_id,
    location,
    fill_level,
    weight_kg,
    battery_level,
    collection_priority
FROM critical_bins
ORDER BY fill_level DESC
""").show(20, truncate=False)


# ==========================================
# 6. Bin Analysis
# ==========================================

print("\n======================================")
print("6. BIN ANALYSIS")
print("======================================")

spark.sql("""
SELECT
    bin_id,
    location,
    readings,
    avg_fill_level,
    max_fill_level,
    total_waste_kg,
    avg_battery_level
FROM bin_analysis
ORDER BY avg_fill_level DESC
""").show(20, truncate=False)


print("\n======================================")
print("SQL ANALYTICS COMPLETED SUCCESSFULLY!")
print("======================================")

spark.stop()