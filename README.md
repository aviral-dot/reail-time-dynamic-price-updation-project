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
































