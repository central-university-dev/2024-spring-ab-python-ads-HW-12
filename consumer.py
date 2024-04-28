import json

from kafka import KafkaConsumer

from river import linear_model
from river import compose
from river import preprocessing
from river import metrics

metric = metrics.ROCAUC()

model = compose.Pipeline(
    preprocessing.StandardScaler(),
    linear_model.LogisticRegression()
)

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
        print(metric)
        model.learn_one(x, y)
    except:
        print("Error")
