import streamlit as st
import pandas as pd
import requests

st.title("Netflix RecSys")

app_mode = st.sidebar.selectbox("Mode", ["Random Films", "Recommendations"])


def onclick():
    pass


def get_recommended_films(user_id):
    response = requests.post(
        "http://localhost:8000/recommend/", json={"user_id": user_id}
    )
    if response.status_code == 200:
        return response.json().get("recommendations", [])
    else:
        st.error("Failed to fetch recommendations")


if app_mode == "Random Films":
    df = pd.read_csv("netflix_titles.csv").loc[:, ["title"]]
    for _, row in df.sample(100).iterrows():
        st.button(row["title"], on_click=onclick)

if app_mode == "Recommendations":
    user_id = st.text_input("Enter your user ID:")
    if user_id:
        recommendations = get_recommended_films(user_id)
        for title in recommendations:
            st.button(title, on_click=onclick)
