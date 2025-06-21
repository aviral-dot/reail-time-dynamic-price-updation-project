import time
import random
import numpy as np
from datetime import datetime
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer
import signal
import sys
import threading

# Schema Registry configuration
schema_registry_conf = {'url': 'http://localhost:8083'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Avro schema
avro_schema_str = """
{
  "namespace": "com.pricing",
  "type": "record",
  "name": "PriceEvent",
  "fields": [
    {"name": "timestamp", "type": "string"},
    {"name": "hour", "type": "int"},
    {"name": "day_of_week", "type": "int"},
    {"name": "region", "type": "string"},
    {"name": "weather", "type": "string"},
    {"name": "demand", "type": "int"},
    {"name": "inventory", "type": "int"},
    {"name": "competitor_price", "type": "float"},
    {"name": "actual_price", "type": "float"}
  ]
}
"""

avro_serializer = AvroSerializer(
    schema_registry_client=schema_registry_client,
    schema_str=avro_schema_str,
    to_dict=lambda obj, ctx: obj
)

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': avro_serializer,
    'linger.ms': 100,
    'batch.num.messages': 1000,
    'enable.idempotence': True,
    'max.in.flight.requests.per.connection': 3,
    'compression.type': 'lz4',
    'retries': 5,
    'acks': 'all'
}

producer = SerializingProducer(producer_conf)

# Constants
regions = ['NY', 'CA', 'TX']
weathers = ['Sunny', 'Rainy', 'Cloudy']
base_competitor_price = {'NY': 30, 'CA': 28, 'TX': 25}
weather_factor = {'Sunny': 1.0, 'Cloudy': 1.02, 'Rainy': 1.05}

def generate_pricing_event(timestamp: datetime, region: str):
    hour = timestamp.hour
    day_of_week = timestamp.weekday()
    weather = random.choice(weathers)

    demand = (
        20 * (7 <= hour <= 9) +
        25 * (17 <= hour <= 19) +
        np.random.poisson(lam=5)
    )

    inventory = max(50 - demand + np.random.randint(-5, 5), 0)
    comp_price = base_competitor_price[region] + np.random.normal(0, 1.5)
    comp_price = round(comp_price, 2)

    base_price = comp_price * (1 + 0.05 * (demand / (inventory + 1)))
    peak_adj = 1.1 if ((7 <= hour <= 9) or (17 <= hour <= 19)) else 1.0
    weather_adj = weather_factor[weather]

    actual_price = round(base_price * peak_adj * weather_adj + np.random.normal(0, 0.5), 2)

    return {
        "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        "hour": hour,
        "day_of_week": day_of_week,
        "region": region,
        "weather": weather,
        "demand": int(demand),
        "inventory": int(inventory),
        "competitor_price": comp_price,
        "actual_price": actual_price
    }

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Failed to deliver message: {err}")
    else:
        print(f"✅ Delivered message to {msg.topic()} [{msg.partition()}] offset {msg.offset()}")

def shutdown(signum, frame):
    print("\n🛑 Shutting down producer gracefully...")
    remaining = producer.flush(timeout=10)
    if remaining == 0:
        print("✅ All messages acknowledged. Shutdown complete.")
    else:
        print(f"⚠️ Shutdown complete but {remaining} message(s) left unacknowledged!")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def background_poll():
    while True:
        producer.poll(0.05)  # Poll every 50 milliseconds
        time.sleep(0.05)

if __name__ == "__main__":
    topic = "my-topic1"
    print("🟢 Producing dynamic pricing events for all regions every second... Press Ctrl+C to stop.")

    # Start the background polling thread
    poll_thread = threading.Thread(target=background_poll, daemon=True)
    poll_thread.start()

    counter = 0
    while True:
        now = datetime.now()
        for region in regions:
            event = generate_pricing_event(now, region)
            producer.produce(topic=topic, key=region, value=event, on_delivery=delivery_report)
            # Removed producer.poll(0) here, background thread handles polling
            counter += 1
        time.sleep(150)  # Every second, produce one message per region
