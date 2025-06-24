# Real-Time-Dynamic-Price-Updation-Project

![image_alt](https://github.com/aviral-dot/real-time-dynamic-price-updation-project/blob/main/real-time-dynamic-price.drawio.png?raw=true)


📈 Real-Time Dynamic Price Updation System — Dockerized End-to-End Pipeline
This project implements a real-time dynamic pricing system that emulates Uber-like ride price prediction and visualization. It is built using a modern big data and machine learning stack, fully containerized using Docker to ensure easy deployment, scalability, and modularity.

The core idea is to simulate incoming Uber ride data, process it in real time using Apache Kafka and Apache Spark, apply machine learning models for price prediction (XGBoost), and reflect these dynamic changes instantly in a responsive UI. The entire flow is monitored using Prometheus and visualized using Grafana dashboards.

🧩 System Architecture Overview
The architecture is composed of several interconnected services working together in real time:

🚖 Uber API Simulation: A mock service continuously generates real-time ride events (e.g., location, distance, time) and streams them into Kafka topics.

🧵 Apache Kafka: Acts as the event streaming platform, decoupling the producers (data generators) and consumers (Spark) for scalable and reliable data ingestion.

📦 Schema Registry: Maintains Avro schemas for Kafka topics to ensure schema consistency and compatibility between producers and consumers.

📊 Kafka Control Center: A web-based UI to manage and monitor Kafka topics, consumer groups, schema validations, and streaming health.

⚡ Apache Spark (Structured Streaming): Reads real-time ride data from Kafka, performs transformations and feature engineering, and applies a trained XGBoost machine learning model to predict updated ride prices dynamically.

🤖 XGBoost Model: A powerful gradient boosting model that uses multiple features from ride data to predict surge or drop in pricing per region.

🗃️ MongoDB (Replica Set): Stores the latest predicted price for each region (NY, CA, TX, etc.) in a centralized price_history collection. The same document is updated for each new prediction using the region as _id.

🌐 Real-Time Web UI:

Backend (Node.js): Subscribes to MongoDB Change Streams and broadcasts updates to the frontend via WebSocket.

Frontend (React): Dynamically displays updated regional prices as soon as they change in MongoDB.

📈 Prometheus & Grafana: Monitors the health and performance of various services (Kafka, Spark, MongoDB, etc.), collects metrics, and visualizes them through custom Grafana dashboards.

🐳 Dockerized Setup: Every service (Kafka, Spark, MongoDB, frontend, backend, monitoring) runs in isolated Docker containers, orchestrated via docker-compose for easy local development and reproducibility.

🔄 End-to-End Data Flow
Real-time ride data is pushed from the simulated Uber API to Kafka.

Kafka streams the data into a topic defined with a schema registered in Schema Registry.

Apache Spark reads data from Kafka, applies preprocessing and XGBoost model predictions.

Predicted prices are written to MongoDB, updating the same documents by region.

Backend service listens to MongoDB’s Change Streams and sends real-time updates to connected clients via WebSocket.

Frontend UI instantly reflects updated pricing per region.

Prometheus scrapes metrics and Grafana visualizes them for system observability.

✅ Features
🚀 Real-time data streaming & processing

🧠 Machine learning-based price prediction (XGBoost)

🖥️ Live frontend with real-time price updates

📡 MongoDB Change Streams + WebSocket integration

📊 Monitoring & dashboarding with Prometheus + Grafana

🐳 Fully Dockerized and reproducible setup

📦 Schema evolution managed via Confluent Schema Registry

































