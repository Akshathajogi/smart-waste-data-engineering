-- ============================================================
-- SMART WASTE MANAGEMENT - ANALYTICS SQL
-- ============================================================

-- 1. Overall Summary
SELECT *
FROM overall_summary;


-- 2. Collection Priority Distribution
SELECT
    collection_priority,
    count
FROM collection_priority
ORDER BY count DESC;


-- 3. Battery Status Distribution
SELECT
    battery_status,
    count
FROM battery_status
ORDER BY count DESC;


-- 4. Location-wise Analysis
SELECT
    location,
    sensor_readings,
    avg_fill_level,
    total_waste_kg,
    avg_battery_level
FROM location_analysis
ORDER BY avg_fill_level DESC;


-- 5. Critical Bins
SELECT
    bin_id,
    location,
    fill_level,
    weight_kg,
    battery_level,
    collection_priority
FROM critical_bins
ORDER BY fill_level DESC;


-- 6. Bin-wise Performance
SELECT
    bin_id,
    location,
    readings,
    avg_fill_level,
    max_fill_level,
    total_waste_kg,
    avg_battery_level
FROM bin_analysis
ORDER BY avg_fill_level DESC;