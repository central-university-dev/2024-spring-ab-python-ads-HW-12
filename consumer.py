import json
from kafka import KafkaConsumer
import numpy as np
import redis

r = redis.Redis(host="localhost", port=6379, db=0)

consumer = KafkaConsumer(
    "ml_training_data",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    group_id="my_group_id",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

for event in consumer:
    event_data = event.value
    try:
        user_id = event_data["user_id"]
        movie_embedding = np.array(event_data["embedding"], dtype="float32")
        existing_embedding = r.get(user_id)
        if existing_embedding:
            existing_embedding = np.frombuffer(existing_embedding, dtype="float32")
            updated_embedding = (existing_embedding + movie_embedding) / 2
        else:
            updated_embedding = movie_embedding
        r.set(user_id, updated_embedding.tobytes())
    except Exception as e:
        print(f"Error: {e}")
