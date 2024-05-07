import json
from kafka import KafkaConsumer
from river import compose, preprocessing, linear_model, metrics
import logging

logging.basicConfig(level=logging.INFO)

model: compose.Pipeline = compose.Pipeline(
    preprocessing.StandardScaler(),
    linear_model.LogisticRegression()
)

metric: metrics.ROCAUC = metrics.ROCAUC()

consumer = KafkaConsumer(
    "ml_training_data",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    group_id="my_group_id",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

for event in consumer:
    event_data = event.value
    try:
        x = event_data["x"]
        y = event_data["y"]
        y_pred = model.predict_proba_one(x)
        metric.update(y, y_pred)
        model.learn_one(x, y)
        logging.info(f"Updated metric: {metric}")
    except Exception as e:
        logging.error(f"Error processing event: {e}")
