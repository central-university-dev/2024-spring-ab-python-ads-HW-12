from time import sleep
import json
import random
from kafka import KafkaProducer
from river import datasets


producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

dataset = datasets.Phishing()

for x, y in dataset:
    data = {"user_id": random.randint(1, 10), "embedding": list(x.values())}  # Simulate user IDs
    producer.send("ml_training_data", value=data)



