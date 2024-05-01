from time import sleep
import json
from kafka import KafkaProducer
import logging

logging.basicConfig(level=logging.INFO)

def get_kafka_producer(bootstrap_servers: str = 'localhost:9092') -> KafkaProducer:
    """
    Configure and return a Kafka producer.

    Args:
        bootstrap_servers (str): The server for Kafka connection.

    Returns:
        KafkaProducer: Configured Kafka producer.
    """
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

def send_user_interaction(producer: KafkaProducer, topic: str, user_id: str, movie_id: str, embedding: list) -> None:
    """
    Send a user interaction message to Kafka.

    Args:
        producer (KafkaProducer): The Kafka producer.
        topic (str): The Kafka topic to send messages to.
        user_id (str): The user's ID.
        movie_id (str): The movie's ID.
        embedding (list): The embedding vector of the movie.

    Returns:
        None
    """
    message = {'user_id': user_id, 'movie_id': movie_id, 'embedding': embedding}
    try:
        producer.send(topic, value=message)
        logging.info("Message sent successfully")
