import json
import numpy as np
from kafka import KafkaConsumer
from api.app import redis_client

consumer = KafkaConsumer(
    "ml_training_data",
    bootstrap_servers=["kafka:9092"],
    auto_offset_reset="earliest",
    group_id="my_group_id",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

for event in consumer:
    event_data = event.value
    user_id = event_data["user_id"]
    film_embedding = np.array(event_data["embedding"], dtype='float32')

    user_embedding = redis_client.get(f"user:{user_id}:embedding")
    if user_embedding:
        user_embedding = np.array(json.loads(user_embedding), dtype='float32')
        updated_embedding = (user_embedding + film_embedding) / 2
    else:
        updated_embedding = film_embedding

    redis_client.set(f"user:{user_id}:embedding", json.dumps(updated_embedding.tolist()))
