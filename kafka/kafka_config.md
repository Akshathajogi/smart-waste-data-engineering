# Kafka Configuration

## Project

Smart Waste Management – Real-Time Waste Collection & Data Engineering Pipeline

Apache Kafka is used as the real-time event streaming layer of the project.

---

## Kafka Setup

- Apache Kafka: 4.3.1
- Running Mode: KRaft
- Zookeeper: Not required
- Bootstrap Server: `localhost:9092`
- Kafka Topic: `waste_sensor`

---

## Event Flow

```text
Waste Sensor Data
       ↓
Python Kafka Producer
       ↓
Kafka Topic: waste_sensor
       ↓
PySpark Structured Streaming
       ↓
Parquet Storage
       ↓
SQL Analytics
       ↓
Streamlit Dashboard
```

---

## Start Kafka

```powershell
C:\kafka_2.13-4.3.1\bin\windows\kafka-server-start.bat C:\kafka_2.13-4.3.1\config\server.properties
```

---

## Create Kafka Topic

```powershell
C:\kafka_2.13-4.3.1\bin\windows\kafka-topics.bat --create --topic waste_sensor --bootstrap-server localhost:9092
```

Check available topics:

```powershell
C:\kafka_2.13-4.3.1\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

---

## Run Kafka Producer

File:

```text
producer/waste_sensor_producer.py
```

Run:

```powershell
python producer\waste_sensor_producer.py
```

The producer publishes waste sensor events to the `waste_sensor` Kafka topic.

---

## Run PySpark Streaming

File:

```text
spark/waste_streaming.py
```

Run:

```powershell
python spark\waste_streaming.py
```

The PySpark streaming application consumes events from Kafka and writes processed data to Parquet storage.

---

## Kafka Connectivity

The Kafka broker must be running before starting the producer or PySpark streaming application.

```text
Bootstrap Server: localhost:9092
Topic: waste_sensor
```

---

## Technology Stack

- Apache Kafka 4.3.1
- PySpark 4.2.0
- Python
- Parquet
- SQL
- Streamlit
