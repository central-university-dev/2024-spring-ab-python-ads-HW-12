from time import sleep
import json
import random

from river import datasets
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

dataset = datasets.Phishing()

for x, y in dataset:
    print(f"Sending: {x, y}")
    data = {"x": x, "y": y}
    producer.send("ml_training_data", value=data)
    sleep(random.random())