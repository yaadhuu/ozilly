import streamlit as st
import pickle
import pandas as pd
import random
import requests
import os
import gdown

# Download large similarity.pkl from Google Drive
def download_similarity():
    file_path = "similarity.pkl"
    if not os.path.exists(file_path):
        url = "https://drive.google.com/uc?id=1Y2rRA4DGpNXRCJ09J1lOx-JlnV6OBtl6"
        gdown.download(url, file_path, quiet=False)

download_similarity()

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.set_page_config(page_title="Ozilly - Movie Recommender", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');

    html, body {
        background-color: #111;
        color: white;
        font-family: 'Roboto', sans-serif;
    }

    .ozilly-brand {
        font-size: 80px;
        font-weight: 700;
        letter-spacing: 3px;
        background: linear-gradient(90deg, #E50914, #ff4b2b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 40px;
        font-family: 'Roboto', sans-serif;
    }

    .ozilly-slogan {
        text-align: center;
        font-size: 20px;
        color: #cccccc;
        margin-top: -12px;
        font-style: italic;
        letter-spacing: 0.5px;
    }

    .recommend-box {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin-top: 40px;
    }

    .movie-title {
        text-align: center;
        font-size: 16px;
        margin-top: 10px;
        color: #fff;
    }

    img:hover {
        transform: scale(1.05);
        transition: transform 0.3s ease;
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.2);
    }

    .stButton > button {
        background-color: #E50914;
        color: white;
        font-size: 16px;
        padding: 12px 40px;
        border-radius: 10px;
        border: none;
        margin-top: 10px;
    }

    .stButton > button:hover {
        background-color: #b20710;
    }

    .stSelectbox > div {
        background-color: #1e1e1e !important;
        border-radius: 10px;
        padding: 8px;
        font-size: 16px;
        border: 1px solid #333 !important;
        box-shadow: inset 0 0 5px #00000033;
    }
    </style>

    <div class='ozilly-brand'>Ozilly</div>
    <div class='ozilly-slogan'>Your Personal Movie Recommender</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='recommend-box'>", unsafe_allow_html=True)
    selected_movie_name = st.selectbox("🎞️ Search for a movie", movies['title'].values, key="movie_selector", index=None, placeholder="Type or select a movie...")
    recommend_button = st.button("Recommend", key="recommend_button")
    st.markdown("</div>", unsafe_allow_html=True)

# Fetch poster from TMDB
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=e751b9b29910a0685e127c23f664a451&language=en-US'
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image", data
    except:
        return "https://via.placeholder.com/500x750?text=No+Image", {}

# Recommend function
def recommend(movie):
    movie = movie.strip().lower()
    if not any(movies['title'].str.lower() == movie):
        return [], [], []
    idx = movies[movies['title'].str.lower() == movie].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:19]
    titles, posters, movie_details = [], [], []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        poster, details = fetch_poster(movie_id)
        titles.append(movies.iloc[i[0]].title)
        posters.append(poster)
        movie_details.append(details)
    return titles, posters, movie_details

# Display movies in a 6-column grid
def display_movies(titles, posters, movie_details):
    num_per_row = 6
    for i in range(0, len(titles), num_per_row):
        cols = st.columns(num_per_row)
        for idx, col in enumerate(cols):
            if i + idx < len(titles):
                with col:
                    st.image(posters[i + idx], use_container_width=True)
                    st.markdown(f"<div class='movie-title'>{titles[i + idx]}</div>", unsafe_allow_html=True)

                    with st.expander(f"More about {titles[i + idx]}"):
                        details = movie_details[i + idx]
                        st.write(f"**Release Date**: {details.get('release_date', 'N/A')}")
                        st.write(f"**Overview**: {details.get('overview', 'No description available.')}")
                        st.write(f"**Rating**: {details.get('vote_average', 'N/A')}/10")

# App logic
if recommend_button and selected_movie_name:
    titles, posters, movie_details = recommend(selected_movie_name)
    if titles:
        st.subheader("🎯 Recommended for you")
        display_movies(titles, posters, movie_details)
    else:
        st.warning("Movie not found. Try another title.")
else:
    st.subheader("🎬 Explore Movies")
    sample = random.sample(list(movies['title']), 18)
    titles, posters, movie_details = [], [], []
    for title in sample:
        movie_id = movies[movies['title'] == title].iloc[0].movie_id
        poster, details = fetch_poster(movie_id)
        titles.append(title)
        posters.append(poster)
        movie_details.append(details)
    display_movies(titles, posters, movie_details)

if st.button("Load More"):
    st.rerun()
