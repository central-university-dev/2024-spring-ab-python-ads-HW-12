from fastapi import FastAPI, HTTPException
import numpy as np
from typing import Dict, List

from predict import load_faiss_index
from producer import get_kafka_producer, send_user_interaction
from redis_client import get_redis_client

app = FastAPI()
index = load_faiss_index()
producer = get_kafka_producer()
redis_client = get_redis_client()

@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str) -> Dict[str, List[int]]:
    """
    Fetch top 10 movie recommendations for a user based on their embedding.

    Args:
        user_id (str): The ID of the user for whom to fetch recommendations.

    Returns:
        Dict[str, List[int]]: A dictionary containing the user ID and a list of recommended movie indices.

    Raises:
        HTTPException: If user embedding is not found in Redis.
    """
    user_embedding = redis_client.get(f"user:{user_id}")
    if not user_embedding:
        raise HTTPException(status_code=404, detail="User embedding not found")
    
    user_embedding = np.frombuffer(user_embedding, dtype=np.float32)
    
    # Perform the search
    distances, indices = index.search(user_embedding.reshape(1, -1), 10)
    return {"user_id": user_id, "recommendations": indices.flatten().tolist()}

@app.post("/interact/{user_id}/{movie_id}")
def log_interaction(user_id: str, movie_id: str, embedding: List[float]) -> Dict[str, str]:
    """
    Log user interaction with a movie by sending it to Kafka.

    Args:
        user_id (str): The ID of the user who interacted with the movie.
        movie_id (str): The ID of the movie interacted with.
        embedding (List[float]): The embedding vector of the movie.

    Returns:
        Dict[str, str]: Confirmation message of the logged interaction.
    """
    embedding_np = np.array(embedding, dtype=np.float32)
    # Prepare the message
    message = {
        "user_id": user_id,
        "movie_id": movie_id,
        "embedding": embedding_np.tolist()
    }
    # Send the interaction to Kafka
    producer.send('user_interactions', value=message)
    return {"status": "Interaction logged"}
