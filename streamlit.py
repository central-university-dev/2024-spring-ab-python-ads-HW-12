import pandas as pd

import streamlit as st

st.title('Netflix RecSys')

df = pd.read_csv("netflix_titles.csv").loc[:, ["title"]]

app_mode = st.sidebar.selectbox('Mode', ['Random Films', 'Recommendations'])

def onclick():
    pass

def get_recommended_films():
    return [392, 1358, 3329]

if app_mode == "Random Films":
    for _, row in df.sample(100).iterrows():
        st.button(row["title"], on_click=onclick)

if app_mode == "Recommendations":
    for film in get_recommended_films():
        st.button(df.at[film, "title"], on_click=onclick)
