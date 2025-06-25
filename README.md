# Real-Time-Dynamic-Price-Updation-Project<br><br>

![image_alt](https://github.com/aviral-dot/real-time-dynamic-price-updation-project/blob/main/real-time-dynamic-price.drawio.png?raw=true)<br><br>




**📈 Real-Time Dynamic Price Updation System — Dockerized End-to-End Pipeline**<br>
This project implements a real-time dynamic pricing system that emulates Uber-like ride price prediction and visualization. It is built using a modern big data and machine learning stack, fully containerized using Docker to ensure easy deployment, scalability, and modularity.

The core idea is to simulate incoming Uber ride data, process it in real time using Apache Kafka and Apache Spark, apply machine learning models for price prediction (XGBoost), and reflect these dynamic changes instantly in a responsive UI. The entire flow is monitored using Prometheus and visualized using Grafana dashboards.




**🧩 System Architecture Overview**<br>
The architecture is composed of several interconnected services working together in real time:

🚖 Uber API Simulation: A mock service continuously generates real-time ride events (e.g., location, distance, time) and streams them into Kafka topics.

🧵 Apache Kafka: Acts as the event streaming platform, decoupling the producers (data generators) and consumers (Spark) for scalable and reliable data ingestion.

📦 Schema Registry: Maintains Avro schemas for Kafka topics to ensure schema consistency and compatibility between producers and consumers.

📊 Kafka Control Center: A web-based UI to manage and monitor Kafka topics, consumer groups, schema validations, and streaming health.

⚡ Apache Spark (Structured Streaming): Reads real-time ride data from Kafka, performs transformations and feature engineering, and applies a trained XGBoost machine learning model to predict updated ride prices dynamically.

🤖 XGBoost Model: A powerful gradient boosting model that uses multiple features from ride data to predict surge or drop in pricing per region.

🗃️ MongoDB (Replica Set): Stores the latest predicted price for each region (NY, CA, TX, etc.) in a centralized price_history collection. The same document is updated for each new prediction using the region as _id.
<br>

🌐 Real-Time Web UI:<br>

Backend (Node.js): Subscribes to MongoDB Change Streams and broadcasts updates to the frontend via WebSocket.

Frontend (React): Dynamically displays updated regional prices as soon as they change in MongoDB.

📈 Prometheus & Grafana: Monitors the health and performance of various services (Kafka, Spark, MongoDB, etc.), collects metrics, and visualizes them through custom Grafana dashboards.

🐳 Dockerized Setup: Every service (Kafka, Spark, MongoDB, frontend, backend, monitoring) runs in isolated Docker containers, orchestrated via docker-compose for easy local development and reproducibility.



**🔄 End-to-End Data Flow**<br>

Real-time ride data is pushed from the simulated Uber API to Kafka.

Kafka streams the data into a topic defined with a schema registered in Schema Registry.

Apache Spark reads data from Kafka, applies preprocessing and XGBoost model predictions.

Predicted prices are written to MongoDB, updating the same documents by region.

Backend service listens to MongoDB’s Change Streams and sends real-time updates to connected clients via WebSocket.

Frontend UI instantly reflects updated pricing per region.

Prometheus scrapes metrics and Grafana visualizes them for system observability.


✅ Features<br>
🚀 Real-time data streaming & processing

🧠 Machine learning-based price prediction (XGBoost)

🖥️ Live frontend with real-time price updates

📡 MongoDB Change Streams + WebSocket integration

📊 Monitoring & dashboarding with Prometheus + Grafana

🐳 Fully Dockerized and reproducible setup

📦 Schema evolution managed via Confluent Schema Registry<br><br>




![Screenshot 2025-06-23 004757](https://github.com/user-attachments/assets/2e966768-1d38-4c86-babf-3ef6db8041f2)<br><br>

![Screenshot 2025-06-23 004815](https://github.com/user-attachments/assets/fa59dd6e-70c7-4ad8-9186-83014a3cb135)<br><br>

🐳 Dockerized Setup — Containerized Microservices Architecture<br>
This project leverages a fully Dockerized microservices architecture to orchestrate and manage each component of the real-time price prediction pipeline. Docker ensures a consistent, reproducible environment for both local development and production deployments. Each major service—Kafka, Spark, MongoDB, frontend/backend UI, monitoring stack—is encapsulated within its own container and coordinated using docker-compose.

You can bring the entire system up with a single command:

bash
Copy
Edit
docker-compose up --build
This command builds all necessary images (if not already built) and spins up containers with the predefined configuration—including memory/CPU limits, custom networks, mounted volumes, and exposed ports. Each service is linked to the others internally via Docker’s network bridge, ensuring seamless service-to-service communication.

📷 Container Initialization Snapshot
Below is a snapshot showing the live Docker container startup process during system initialization:


📌 As shown above, all core services initialize in sequence:

Kafka brokers and Schema Registry come online to handle incoming event streams.

Spark Master and Workers register and prepare for distributed streaming jobs.

MongoDB Replica Set is initialized with keyfile-based internal authentication.

Node.js Backend connects to MongoDB and opens a WebSocket server.

React Frontend launches the real-time UI dashboard.

Prometheus and Grafana come online for system observability and performance monitoring.

🧱 Microservices in Docker Compose<br>
Service	Role
Kafka	Real-time messaging layer for ingesting Uber ride events
Schema Registry	Ensures schema consistency for Kafka messages
Apache Spark	Distributed data processing and ML model execution
MongoDB Replica Set	Stores regional price predictions in a fault-tolerant way
Node.js Backend	Bridges MongoDB change streams to frontend via WebSocket
React Frontend	Live interface showing real-time price changes per region
Prometheus	Collects metrics from all services
Grafana	Dashboards for real-time system monitoring and alerting

Each container is provisioned with:

Health checks to verify readiness before linking with dependent services

Named volumes to persist important data (MongoDB state, Grafana dashboards, etc.)

Custom Docker networks (kafka-net, spark-net) for logical separation and efficiency

Resource constraints to control memory/CPU usage per container

<br>
<br>


![image](https://github.com/user-attachments/assets/4ced7e10-6dc0-426b-a9e8-45ea566d3ec2)<br><br>


THE PROJECT BEGINS WITH SENDING THE REAL TIME PRICE UPDATION DATA OF THE COMPETITORS OF  VARIOUS DIFFERENT PLACE IN ORDER TO COMPETE WITH THE PRICE AND CAPTURE THE CUSTOMERS. 
THE DATA IS SENT TO THE KAFKA IN KAFKA TOPICS.

This project includes a custom Python script that streams real-time Uber-like pricing data to Kafka. The script reads records in CSV format and emits structured events to a Kafka topic at a steady interval (e.g., 1 message per second per region). This simulated feed powers the real-time ML prediction and pricing pipeline.

🧪 Purpose
Simulate real-world Uber ride events with regional and environmental factors.

Push live updates to Kafka, triggering real-time predictions by Apache Spark.

Enable end-to-end testing of data ingestion, transformation, and model scoring.

Mimic fluctuating pricing dynamics under various weather, traffic, and demand conditions.

**📄 Sample Raw Data Format (CSV)**
yaml
Copy
Edit
2024-01-05 13:00:00,13,4,CA,Sunny,9,39,28.16,28.65
<br>
<br>

![Screenshot 2025-06-25 045706](https://github.com/user-attachments/assets/ace586ea-77b2-4e86-9d47-e0918f424ec8)<br><br>

**📡 Kafka Control Center — Real-Time Message Monitoring**
Apache Kafka is at the heart of this project, enabling real-time data flow from producers (e.g., dynamic pricing event generator) to downstream consumers like Spark.

To visualize and monitor the live Kafka topics, this project integrates the Confluent Control Center — a powerful GUI for Kafka operations.

📷 Kafka Message Flow Example

✅ The image above shows the Control Center UI displaying real-time messages published to the Kafka topic uber-ride-events. Each message represents a simulated ride event containing data like region, timestamp, weather, traffic level, and pricing.

🧭 What You Can Monitor in the Control Center:
Active topics and partitions (e.g., uber-ride-events)

Message throughput and retention

Real-time message content (in JSON or Avro)

Producer/consumer performance

Schema versioning via Schema Registry (if integrated)

🔌 How to Access It
Once the stack is running, you can access the Control Center at:

arduino
Copy
Edit
http://localhost:9021
Login is not required by default (unless configured).

THE MESSAGE IN THE IMAGE ARE THE MESSAGE OF REAL TIME DATA ARRIVING IN KAFKA TOPIC WHICH IS SHOWN BY CONTROL CENTER.<br><br>

![Screenshot 2025-06-25 045840](https://github.com/user-attachments/assets/2d553057-a215-4c28-9a51-6e5a081622bc)<br><br>

🧾 Schema Registry — Enforcing Data Contracts for Kafka
To ensure consistent structure and backward-compatible data evolution, this project uses Confluent Schema Registry. It provides a centralized service for managing Avro schemas used when producing and consuming Kafka messages.

Using Schema Registry avoids common issues like:

Inconsistent field names or types

Breaking changes in data formats

Consumers failing due to unknown schemas

🧬 How It Works
The producer registers an Avro schema before sending messages

The consumer retrieves and validates against the latest schema

Schemas are versioned, allowing safe updates over time

📷 Schema Registry in Action

🧩 Above: The Schema Registry UI shows registered schemas for Kafka topics like uber-ride-events-value. Each schema describes the structure of data being sent, including fields such as region, timestamp, traffic_level, and final_price.

THE SCHEMA REGISTRY REGISTER THE AVRO SCHEMA 

![image](https://github.com/user-attachments/assets/1df82a58-39ec-4e1f-ab0e-b39fa14a5473)


the image is of the avro schema of the data.<br><br>

![Screenshot 2025-06-25 025509](https://github.com/user-attachments/assets/9a803424-d525-4e62-a55c-cf9af8bbec9b)<br><br>

**🏢 Kafka Broker — The Core of Real-Time Messaging**
In this project, the Kafka broker is the central component responsible for receiving, storing, and distributing messages between producers (like the pricing data generator) and consumers (like Apache Spark).

Each broker handles Kafka topics (like uber-ride-events) and partitions, ensuring high throughput and durability for real-time event streams.

**⚙️ Role of the Kafka Broker**
Receives messages from producers (e.g., ride events, pricing updates)

Stores messages in topic-partitions for a configurable retention period

Serves messages to multiple consumers, including:

Spark (for prediction)

WebSocket backend (for real-time UI)

Control Center or CLI tools (for debugging)

**🧭 Architecture View**
text
Copy
Edit
Producer --> [ Kafka Broker ] --> Consumer(s)
                        |
              +----------------------+
              | Topics:              |
              |  - uber-ride-events  |
              |  - prediction-logs   |
              +----------------------+
              
**🧾 Example Message Stored in the Broker**
json
Copy
Edit
{
  "timestamp": "2024-01-05 13:00:00",
  "region": "CA",
  "weather_condition": "Sunny",
  "traffic_index": 9,
  "base_fare": 28.16,
  "final_price": 28.65
}

**📷 Kafka Broker Message Snapshot**

📌 Above: The screenshot shows a message stored inside the uber-ride-events topic on the Kafka broker. Each message represents a ride pricing event including location, weather, and traffic-based pricing adjustments.
<br>
<br>

![Screenshot 2025-06-25 025716](https://github.com/user-attachments/assets/14dfce64-cbfa-496b-9d43-4ed479603655)<br><br>

🐘 Apache Zookeeper — Kafka Cluster Coordination Backbone
Apache Zookeeper plays a critical role in this project by managing and coordinating the Kafka broker. It handles the internal bookkeeping required for:

Broker discovery

Leader election

Configuration synchronization

Topic partition assignment

Without Zookeeper, the Kafka broker would not be able to start up, maintain consistency, or recover from failures (in older versions of Kafka, before KRaft mode).

🔧 Why Zookeeper is Required (in this project)
Kafka (v7.4 and earlier in this setup) depends on Zookeeper to:

Register and discover broker nodes

Track partition leader assignments

Store cluster metadata

Zookeeper provides a consistent and fault-tolerant metadata store used by Kafka for all coordination logic

📷 Zookeeper Process View

📌 Above: The screenshot shows the Zookeeper process running inside its container. This confirms that the service is active and reachable by the Kafka broker for cluster operations and leadership elections.<br>

![Screenshot 2025-06-25 030031](https://github.com/user-attachments/assets/dfa98cd3-a26b-4531-b3e7-d66698808a59)<br><br>
![Screenshot 2025-06-25 034613](https://github.com/user-attachments/assets/6a95ca7d-d507-4c4d-833a-0c247f8bf531)<br><br>


**⚡ Apache Spark Master — Distributed Processing Engine**
Apache Spark is used in this project for real-time stream processing and machine learning-based price prediction. The Spark Master node is the central coordinator in the Spark cluster. It schedules jobs, assigns tasks to workers, and manages resources across the cluster.

🔧 Role of the Spark Master
Coordinates all executors (worker nodes)

Manages job scheduling and DAG execution

Maintains cluster metadata, including active workers and running stages

In this project, it:

Consumes messages from Kafka topics like uber-ride-events

Applies transformations and ML inference (e.g., XGBoost model)

Sends the predicted price to MongoDB for real-time UI updates

**📷 Spark Master UI**

🖥 Above: The Spark Master Web UI shows active workers, submitted jobs, and driver information. This dashboard helps monitor the state of the cluster, executors, memory usage, and job performance in real time.


**🎯 Use of Spark Master in This Project**
The Spark Master serves as the central coordinator in your real-time data processing pipeline. Its role is to orchestrate distributed computation over streaming data received from Kafka, enabling scalable price prediction for different regions using a machine learning model.

**🚀 Responsibilities of Spark Master in This Project**
Consumes Kafka Streams

Reads real-time event data (e.g., timestamp, region, weather, traffic) from the Kafka topic uber-ride-events.

This data is generated every second by a producer script simulating dynamic ride conditions.

Distributes Processing Tasks

The Spark Master schedules and distributes the workload (data batches or micro-batches) to Spark workers.

It uses Spark Streaming (or Structured Streaming) to handle continuous data ingestion from Kafka.

Applies ML Model for Price Prediction

Once the data is ingested, Spark applies a pre-trained XGBoost machine learning model and a scaler to predict the final ride price.

The model is cached in the driver/executor memory for efficient access and inference.

Writes Results to MongoDB

After processing, the predicted price (along with region and timestamp) is written to MongoDB into the pricing.price_history collection.

Spark uses a unique _id per region to keep updating the same document in real time.

Enables Real-Time UI Updates

MongoDB’s Change Streams detect updates made by Spark and trigger WebSocket messages to the UI.

This allows the frontend to instantly reflect updated prices without polling or refresh.
<br>
<br>

![Screenshot 2025-06-25 025950](https://github.com/user-attachments/assets/c8b66ef6-6c34-47ae-928f-948b1934fed5)

**🔧 Apache Spark Worker — Task Executor in the Cluster**
In this project, the Spark Worker is responsible for executing distributed tasks assigned by the Spark Master. It is where the actual computation happens — from reading Kafka data to applying machine learning and writing results to MongoDB.

🛠️ Role of Spark Worker in This Project
Connects to the Spark Master and registers as an executor

Receives tasks like reading Kafka streams, processing event data, and making predictions

Loads ML components (scaler + XGBoost model) into memory from S3 or /tmp

Writes prediction results (region-based pricing) into MongoDB for UI consumption

**🔁 Real-Time Processing Flow**
text
Copy
Edit
[Kafka] --> [Spark Worker] --> [Model Prediction] --> [MongoDB]
                           ↘
                      Managed by Spark Master
Each Spark Worker:

Pulls event batches from Kafka

Applies preprocessing (e.g., scaling traffic/weather/base_fare)

Runs inference using XGBoost

Sends output to MongoDB’s price_history collection

📷 Spark Worker in Action

📌 The screenshot above shows the Spark Worker registered with the Spark Master. It provides information like executor ID, memory usage, and active tasks.

You can access this via the Spark Master UI at http://localhost:8080, where Spark Workers are listed under “Workers” and “Executors”.<br><br>

![Screenshot 2025-06-23 005419](https://github.com/user-attachments/assets/66e04594-48bc-46e2-afec-dfc9c38291ba)<br>

THE ABOVE SPARK-SUBMIT WHICH IS SUBMITTED TO SPARK MASTER WHOSE WORK IS TO ALLOCATE RESOURCES TO SPARK WORKERS<br>

![Screenshot 2025-06-23 005532](https://github.com/user-attachments/assets/5639d991-2f92-4ab2-b84b-fc974695788a)<br>
![Screenshot 2025-06-23 005631](https://github.com/user-attachments/assets/63dbfbc7-14df-4a55-9726-80e7f5fdb46c)<br>
![Screenshot 2025-06-23 005656](https://github.com/user-attachments/assets/6cfc0d06-7d70-475b-abad-49696a93c6c0)<br>
![Screenshot 2025-06-23 010003](https://github.com/user-attachments/assets/71223b0e-db54-4721-a986-62a34973a928)<br>
![Screenshot 2025-06-23 010011](https://github.com/user-attachments/assets/d52f648e-ad01-4994-a926-ab1c249e8c97)<br>
![Screenshot 2025-06-23 010051](https://github.com/user-attachments/assets/772302e2-9de7-49cb-b0dd-72c019bcc3c1)<br>
![Screenshot 2025-06-23 010213](https://github.com/user-attachments/assets/4a7c7d93-4ccd-4ca2-80cc-3ce8544fcfd5)<br>
![Screenshot 2025-06-23 010221](https://github.com/user-attachments/assets/f3324db3-1b32-4597-9dd3-096b67a4601a)<br>
![Screenshot 2025-06-23 010231](https://github.com/user-attachments/assets/e7a149e9-e8f8-4bf4-a894-1ccfa44e2c23)<br>
![Screenshot 2025-06-23 010241](https://github.com/user-attachments/assets/8d97ab24-9b6b-47e0-9204-fd3bb829e151)<br>


THE ABOVE ARE THE IMAGES OF THE SPARK JOB RUNNING IN APACHE SPARK. IT GIVE DETAILS ABOUT THE BROADCASTING OF THE FILES AND PACKAGES TO SPARK WORKERS.
IT ALSO SHOWS THAT READING,CLEANING,PROCESSING AND WRITING OF THE TO THE MONGODB DATABASE.<br><br>

![Screenshot 2025-06-25 025052](https://github.com/user-attachments/assets/5004071d-76a6-47e6-b641-2843d56576c4)<br><br>

![Screenshot 2025-06-25 025136](https://github.com/user-attachments/assets/2912c5b6-4419-4b20-a17c-62d7eba9168d)<br>


**🍃 MongoDB — Real-Time Storage for Price Predictions**
MongoDB is used in this project as the primary data store for the predicted ride prices. After Apache Spark processes Kafka events and applies the machine learning model, the prediction results are stored in MongoDB in real time.

This enables the frontend UI to instantly reflect updated prices through MongoDB Change Streams and WebSockets.

💾 What MongoDB Stores
Each document in the pricing.price_history collection contains the latest predicted price for a region, along with metadata such as:

region: e.g., "CA", "NY", "TX"

timestamp: time of prediction

weather_condition, traffic_index, base_fare, etc.

final_price: predicted output from ML model

🧾 Example Document
json
Copy
Edit
{
  "_id": "CA",
  "timestamp": "2024-01-05 13:00:00",
  "weather_condition": "Sunny",
  "traffic_index": 9,
  "base_fare": 28.16,
  "final_price": 28.65
}
Each region is stored using its name as _id to continuously update a single document per region, making it easy to track the latest price for display.

📷 MongoDB Shell Snapshot

🟢 The image above shows the output from db.price_history.find().pretty() in the MongoDB shell. It confirms that the predicted pricing data is being written correctly, with updated values for each region.

WE HAVE TWO MONGO IN DOCKER MONGO 1st one WHICH IS THE PRIMARY AND THE SECOND ONE IS THE REPLICA MONGO.<br>

![Screenshot 2025-06-25 025433](https://github.com/user-attachments/assets/38fa71e0-dae7-4531-b07c-e1476ee0f6e6)<br>


![Screenshot 2025-06-25 025344](https://github.com/user-attachments/assets/b1d55305-a2f9-45c7-bfc7-ad460d7a31ff)<br>

THE ABOVE IS THE IMAGE OF THE DOCKER SETUP FOR THE UI-FRONTEND THAT CONSTANTLY SHOWS THE CHAGNES IN THE PRICE PER REGION.<br><br>

![Screenshot 2025-06-25 014834](https://github.com/user-attachments/assets/40848de1-61b3-488f-bf9a-5677c4cdbb86)<br>

![Screenshot 2025-06-25 024741](https://github.com/user-attachments/assets/bc9300e3-ef08-4e31-ba87-0cbe722531a8)<br>


![Screenshot 2025-05-25 132007](https://github.com/user-attachments/assets/1efecd89-c74a-47aa-9d69-d2d0d80cbf85)<br>

![Screenshot 2025-05-25 105025](https://github.com/user-attachments/assets/27ece836-7e98-4a99-a490-c933817c389a)<br>

**📊 Monitoring with Prometheus & Grafana**
To ensure the health and performance of this real-time data pipeline, this project integrates Prometheus and Grafana for observability and monitoring.

Prometheus collects time-series metrics from various services (like Kafka, Docker, and node exporters), while Grafana visualizes those metrics in interactive dashboards.

🛠️ Why Monitoring is Essential
Detects bottlenecks in Kafka message throughput

Tracks Spark executor performance

Monitors MongoDB write latency

Shows Docker container resource usage

Helps debug issues in real time with alerting (if enabled)

🔍 Prometheus — Time-Series Metrics Collector
Prometheus scrapes metrics from services like:

Kafka (via JMX Exporter)

Docker (via cAdvisor or node-exporter)

Spark (if configured with Prometheus metrics)

System metrics (CPU, memory, disk I/O)

Prometheus setup in docker-compose.yml:

yaml
Copy
Edit
prometheus:
  image: prom/prometheus:latest
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
  networks:
    - kafka-net
Access Prometheus at:

arduino
Copy
Edit
http://localhost:9090
📊 Grafana — Real-Time Dashboard Visualizer
Grafana connects to Prometheus and displays visual dashboards of your system. In this project, it includes panels for:

Kafka topic throughput and partition lag

Docker container CPU/memory usage

MongoDB writes per second

Spark master/worker status (if Prometheus exporter is set)

Custom app-level metrics (optional)

Grafana setup in docker-compose.yml:

yaml
Copy
Edit
grafana:
  image: grafana/grafana:latest
  ports:
    - "3001:3000"
  networks:
    - kafka-net
Access Grafana at:

arduino
Copy
Edit
http://localhost:3001
📷 Dashboard Screenshots
🔧 Prometheus Dashboard

🧩 Prometheus collects time-series metrics from Kafka, Docker, and optionally Spark. You can query metrics using PromQL to explore system behavior in real time.

📈 Grafana Dashboards

📊 Grafana shows real-time visualizations like Kafka topic lag, Spark memory usage, and MongoDB activity. Dashboards help track performance trends and debug issues faster.



















































