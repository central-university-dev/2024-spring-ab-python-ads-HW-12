import pandas as pd
import streamlit as st
import requests

st.title('Netflix RecSys')

df = pd.read_csv('/data/netflix_titles.csv').loc[:, ["title"]]

app_mode = st.sidebar.selectbox('Mode', ['Random Films', 'Recommendations'])

def onclick():
    pass

def get_recommended_films(user_id):
    response = requests.post("http://localhost:8000/recommend", json={"user_id": user_id})
    return response.json()["recommendations"]

if app_mode == "Random Films":
    for _, row in df.sample(100).iterrows():
        st.button(row["title"], on_click=onclick)

if app_mode == "Recommendations":
    user_id = st.sidebar.number_input("User ID", value=1)
    recommended_films = get_recommended_films(user_id)
    for film in recommended_films:
        st.button(df.at[film, 'title'], on_click=onclick)