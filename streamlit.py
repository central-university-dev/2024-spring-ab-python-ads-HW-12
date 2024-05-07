import streamlit as st
import requests
import pandas as pd

st.title('Netflix Recommendation System')

API_URL = "http://localhost:8000"  # Ensure this matches the FastAPI application URL

def fetch_recommendations(user_id: str) -> pd.DataFrame:
    """
    Fetch movie recommendations for a given user ID by querying the FastAPI server.
    
    Args:
        user_id (str): The ID of the user for whom to fetch recommendations.

    Returns:
        pd.DataFrame: Data frame of recommended movie titles.
    """
    response = requests.get(f"{API_URL}/recommendations/{user_id}")
    if response.status_code == 200:
        recommendations = response.json()['recommendations']
        df = pd.read_csv("netflix_titles.csv")
        recommended_titles = df[df.index.isin(recommendations)]['title']
        return recommended_titles
    else:
        st.error('Failed to retrieve recommendations: ' + response.text)
        return pd.DataFrame()

def log_interaction(user_id: str, movie_id: str, embedding: list):
    """
    Log a user's interaction with a movie by sending a POST request to the FastAPI server.

    Args:
        user_id (str): The ID of the user who interacted with the movie.
        movie_id (str): The ID of the movie interacted with.
        embedding (list): The embedding vector of the movie.
    """
    response = requests.post(f"{API_URL}/interact/{user_id}/{movie_id}", json={"embedding": embedding})
    if response.status_code == 200:
        st.success("Interaction logged successfully.")
    else:
        st.error("Failed to log interaction: " + response.text)

# User interaction
user_id_input = st.text_input('Enter your user ID to get recommendations:')
if user_id_input:
    recommended_titles = fetch_recommendations(user_id_input)
    if not recommended_titles.empty:
        st.subheader('Your Recommendations:')
        st.table(recommended_titles)

        # Option to log interaction with any of the recommended movies
        movie_id_input = st.text_input('Enter movie ID to log interaction:')
        embedding_input = st.text_area('Enter embedding vector:', value='[]')
        if st.button('Log Interaction'):
            embedding = eval(embedding_input)
            log_interaction(user_id_input, movie_id_input, embedding)
