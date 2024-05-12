from fastapi import FastAPI, HTTPException
import faiss
import numpy as np
import pandas as pd
import redis

netflix_df = pd.read_csv("netflix_titles.csv")
index = faiss.read_index("faiss_index.index")

r = redis.Redis(host="localhost", port=6379, db=0)

app = FastAPI()


def get_recommendations(vector, k=10):
    faiss.normalize_L2(vector)
    distances, indices = index.search(vector, k)
    return indices


@app.post("/recommend/")
def recommend(user_id: str):
    user_embedding = r.get(user_id)
    if user_embedding is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_embedding = np.frombuffer(user_embedding, dtype="float32")
    recommendations = get_recommendations(user_embedding.reshape(1, -1))
    recommended_titles = netflix_df.iloc[recommendations[0]]["title"].tolist()
    return {"recommendations": recommended_titles}
