from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import numpy as np
import pytest

from . import app

client = TestClient(app)

def test_get_recommendations_success():
    """Mock Redis client and Faiss index"""
    app.redis_client.get = MagicMock(return_value=np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32).tobytes())
    app.index.search = MagicMock(return_value=(None, np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])))
    
    response = client.get("/recommendations/test_user")
    assert response.status_code == 200
    assert response.json() == {
        "user_id": "test_user",
        "recommendations": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }

def test_get_recommendations_not_found():
    """Mock Redis client to return None"""
    app.redis_client.get = MagicMock(return_value=None)
    
    response = client.get("/recommendations/test_user")
    assert response.status_code == 404
    assert response.json() == {"detail": "User embedding not found"}

def test_log_interaction():
    """Mock Kafka producer"""
    app.producer.send = MagicMock()

    response = client.post("/interact/test_user/123", json={"embedding": [0.1, 0.2, 0.3]})
    assert response.status_code == 200
    assert response.json() == {"status": "Interaction logged"}
    app.producer.send.assert_called_once_with('user_interactions', value={
        "user_id": "test_user",
        "movie_id": "123",
        "embedding": [0.1, 0.2, 0.3]
    })

