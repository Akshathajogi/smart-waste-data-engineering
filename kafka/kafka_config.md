Kafka Configuration
Project

Smart Waste Management – Real-Time Waste Collection & Data Engineering Pipeline

Apache Kafka is used as the real-time event streaming layer of the project.

Kafka Version
Apache Kafka: 4.3.1
Running Mode: KRaft
Zookeeper: Not required
Kafka Topic

waste_sensor

The topic contains real-time waste sensor events.

Kafka Bootstrap Server

localhost:9092

Event Flow
Waste Sensor Data
       |
       v
Python Kafka Producer
       |
       v
Kafka Topic (waste_sensor)
       |
       v
PySpark Structured Streaming
       |
       v
Parquet Storage
       |
       v
SQL Analytics
       |
       v
Streamlit Dashboard
Start Kafka
C:\kafka_2.13-4.3.1\bin\windows\kafka-server-start.bat C:\kafka_2.13-4.3.1\config\server.properties
Create Kafka Topic
C:\kafka_2.13-4.3.1\bin\windows\kafka-topics.bat --create --topic waste_sensor --bootstrap-server localhost:9092

Check available topics:

C:\kafka_2.13-4.3.1\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
Kafka Producer

File:

producer/waste_sensor_producer.py

Run:

python producer\waste_sensor_producer.py

The producer publishes waste sensor events to the waste_sensor topic.

PySpark Streaming

File:

spark/waste_streaming.py

Run:

python spark\waste_streaming.py

The Spark streaming application consumes events from the waste_sensor Kafka topic and writes processed data to Parquet storage.

Kafka Connectivity

The Kafka broker must be running before starting the producer or PySpark streaming application.

Expected broker:

localhost:9092

Project Architecture
                    +---------------------+
                    |  Waste Sensor Data  |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    |  Kafka Producer     |
                    |  Python             |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    |  Apache Kafka       |
                    |  waste_sensor       |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    | PySpark Structured  |
                    | Streaming           |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    | Parquet Storage     |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    | SQL Analytics       |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    | Streamlit Dashboard |
                    +---------------------+
                    
Important Notes

Kafka is used for local development and demonstration of the real-time streaming architecture.

The Streamlit dashboard reads the processed Parquet analytics datasets and does not directly depend on the Kafka broker being available.

Do not commit passwords, API keys, private credentials, or other secrets to the repository.

Technology Stack
Apache Kafka 4.3.1
PySpark 4.2.0
Python
Pandas
Parquet
SQL
Streamlit
Altair