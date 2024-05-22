import json

import faiss
import numpy as np
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from predict import get_recommendations

index = faiss.read_index("index.index")
redis_client = redis.Redis(host='redis', port=6379, db=0)

app = FastAPI()


class RecommendationRequest(BaseModel):
    user_id: int


@app.post("/recommend")
async def recommend(request: RecommendationRequest):
    user_embedding = redis_client.get(f"user:{request.user_id}:embedding")
    if not user_embedding:
        raise HTTPException(status_code=404, detail="User embedding not found")

    user_embedding = np.array(json.loads(user_embedding), dtype='float32').reshape(1, -1)
    recommendations = get_recommendations(user_embedding, index, k=10)
    return {"recommendations": recommendations.tolist()}
