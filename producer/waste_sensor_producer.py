
import pandas as pd
import random
import json
from datetime import datetime, timedelta
from kafka import KafkaProducer

# ---------------------------------------
# Configuration
# ---------------------------------------

NUM_BINS = 20
NUM_RECORDS = 1000

KAFKA_TOPIC = "waste-sensor-data"
KAFKA_SERVER = "localhost:9092"

# ---------------------------------------
# Locations for smart bins
# ---------------------------------------

locations = [
    "Udupi",
    "Manipal",
    "Kundapura",
    "Brahmagiri",
    "Malpe"
]

# ---------------------------------------
# Connect to Kafka
# ---------------------------------------

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

print("Connected to Kafka successfully!")

# ---------------------------------------
# Create bin information
# ---------------------------------------

bins = []

for i in range(1, NUM_BINS + 1):

    bins.append({
        "bin_id": f"BIN_{i:03d}",
        "location": random.choice(locations),
        "latitude": round(random.uniform(13.30, 13.40), 6),
        "longitude": round(random.uniform(74.70, 74.80), 6)
    })

# ---------------------------------------
# Generate sensor readings
# ---------------------------------------

records = []

start_time = datetime.now() - timedelta(hours=24)

for i in range(NUM_RECORDS):

    bin_info = random.choice(bins)

    timestamp = start_time + timedelta(minutes=i)

    fill_level = random.randint(10, 100)

    weight_kg = round(
        fill_level * random.uniform(0.4, 0.8),
        2
    )

    temperature = round(
        random.uniform(25, 40),
        2
    )

    battery_level = random.randint(20, 100)

    if fill_level >= 90:
        status = "Overflow Risk"

    elif fill_level >= 70:
        status = "Warning"

    else:
        status = "Normal"

    record = {
        "timestamp": timestamp.isoformat(),
        "bin_id": bin_info["bin_id"],
        "location": bin_info["location"],
        "fill_level": fill_level,
        "weight_kg": weight_kg,
        "temperature": temperature,
        "battery_level": battery_level,
        "latitude": bin_info["latitude"],
        "longitude": bin_info["longitude"],
        "status": status
    }

    records.append(record)

    # ---------------------------------------
    # Send record to Kafka
    # ---------------------------------------

    producer.send(
        KAFKA_TOPIC,
        value=record
    )

# ---------------------------------------
# Make sure all messages are delivered
# ---------------------------------------

producer.flush()

# ---------------------------------------
# Convert records to DataFrame
# ---------------------------------------

df = pd.DataFrame(records)

# ---------------------------------------
# Save dataset
# ---------------------------------------

output_file = "data/raw/waste_sensor_data.csv"

df.to_csv(
    output_file,
    index=False
)

print("---------------------------------------")
print("Dataset generated successfully!")
print(f"Total records: {len(df)}")
print(f"CSV file: {output_file}")
print("All records sent to Kafka successfully!")
print("---------------------------------------")

print("\nFirst 5 records:")
print(df.head())

# ---------------------------------------
# Close Kafka producer
# ---------------------------------------

producer.close()

