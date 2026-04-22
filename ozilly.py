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
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    /* Global */
    .stApp {
        background: radial-gradient(circle at top, #1a1a24 0%, #0d0d12 100%);
        font-family: 'Outfit', sans-serif;
        color: #e2e8f0;
    }
    
    header {visibility: hidden;}

    /* Branding Header */
    .hero-container {
        padding: 4rem 1rem 1rem 1rem;
        animation: fadeIn 1.2s ease-out;
        text-align: center;
    }
    
    .ozilly-brand {
        font-size: 6rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        background: linear-gradient(135deg, #ff0055 0%, #ff5e62 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 10px 40px rgba(255, 0, 85, 0.4);
        margin-bottom: 0.2rem;
    }

    .ozilly-slogan {
        font-size: 1.2rem;
        font-weight: 300;
        color: #94a3b8;
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }

    /* Search Box Container */
    .recommend-box {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 2.5rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.6);
        max-width: 750px;
        margin: 3rem auto;
        animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        opacity: 0;
        transform: translateY(30px);
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #ff0055 0%, #ff5e62 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        border-radius: 14px;
        padding: 0.8rem 2rem;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 20px -5px rgba(255, 0, 85, 0.4);
        margin-top: 15px;
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px -5px rgba(255, 0, 85, 0.6);
        color: white;
        border-color: transparent;
    }
    
    div.stButton > button:active {
        transform: translateY(1px);
    }

    /* Selectbox Styling */
    .stSelectbox > div > div {
        background-color: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px;
        color: white !important;
        padding: 0.2rem;
    }

    /* Movie Cards */
    [data-testid="stImage"] {
        border-radius: 18px;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        cursor: pointer;
    }
    
    [data-testid="stImage"]:hover {
        transform: translateY(-12px) scale(1.04);
        box-shadow: 0 25px 45px rgba(255, 0, 85, 0.25);
    }

    .movie-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.15rem;
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        color: #f8fafc;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }

    /* Details Expander */
    .st-emotion-cache-1zqwqct, [data-testid="stExpander"] {
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        background: rgba(255,255,255,0.02) !important;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Subheaders */
    h3 {
        font-weight: 800 !important;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 3rem !important;
        margin-bottom: 2.5rem !important;
        font-size: 2rem !important;
    }
    
    /* Markdown Text */
    p {
        color: #cbd5e1;
    }
    </style>

    <div class='hero-container'>
        <div class='ozilly-brand'>Ozilly</div>
        <div class='ozilly-slogan'>The Cinematic Oracle</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='recommend-box'>", unsafe_allow_html=True)
selected_movie_name = st.selectbox("Search the ultimate movie database", movies['title'].values, key="movie_selector", index=None, placeholder="Type or select your next obsession...")
recommend_button = st.button("Discover Recommendations", key="recommend_button")
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
