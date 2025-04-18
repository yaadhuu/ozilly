import streamlit as st
import pickle
import pandas as pd
import random
import requests

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.set_page_config(page_title="Ozilly - Movie Recommender", layout="wide")

# Branding + Custom Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@600&display=swap');

    html, body {
        background-color: #111;
        color: white;
        font-family: 'Outfit', sans-serif;
    }

    .ozilly-brand {
        font-family: 'Outfit', sans-serif;
        font-size: 38px;
        letter-spacing: 1.5px;
        background: linear-gradient(to right, #e50914, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px 30px 0px 30px;
    }

    .ozilly-slogan {
        font-size: 16px;
        color: #dddddd;
        padding-left: 32px;
        margin-top: -10px;
        font-style: italic;
    }

    .recommend-box {
        text-align: center;
        padding: 20px;
    }

    .movie-title {
        text-align: center;
        font-size: 14px;
        margin-top: 10px;
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
        padding: 8px 24px;
        border-radius: 8px;
        border: none;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #b20710;
        transform: scale(1.05);
    }
    </style>

    <div class='ozilly-brand'>Ozilly</div>
    <div class='ozilly-slogan'>Your Personal Movie Recommender</div>
""", unsafe_allow_html=True)

# Centered recommend section
with st.container():
    st.markdown("<div class='recommend-box'>", unsafe_allow_html=True)
    selected_movie_name = st.selectbox("🎞️ Search for a movie", movies['title'].values, key="movie_selector", index=None, placeholder="Type or select a movie...")
    recommend_button = st.button("🎯 Recommend", key="recommend_button")
    st.markdown("</div>", unsafe_allow_html=True)

# Fetch movie poster
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=e751b9b29910a0685e127c23f664a451&language=en-US'
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommend function
def recommend(movie):
    movie = movie.strip().lower()
    if not any(movies['title'].str.lower() == movie):
        return [], []
    idx = movies[movies['title'].str.lower() == movie].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:18]
    titles, posters = [], []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        titles.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return titles, posters

# Display movies in a 6-column grid
def display_movies(titles, posters):
    num_per_row = 6
    for i in range(0, len(titles), num_per_row):
        cols = st.columns(num_per_row)
        for idx, col in enumerate(cols):
            if i + idx < len(titles):
                with col:
                    st.image(posters[i + idx], use_container_width=True)
                    st.markdown(f"<div class='movie-title'>{titles[i + idx]}</div>", unsafe_allow_html=True)

# Main logic
if recommend_button and selected_movie_name:
    names, posters = recommend(selected_movie_name)
    st.empty()  # Clear everything
    if names:
        st.subheader("🎯 Recommended for you")
        display_movies(names, posters)
    else:
        st.warning("Movie not found. Try another title.")
else:
    st.subheader("🎬 Explore Random Movies")
    sample = random.sample(list(movies['title']), 18)
    titles, posters = [], []
    for title in sample:
        movie_id = movies[movies['title'] == title].iloc[0].movie_id
        titles.append(title)
        posters.append(fetch_poster(movie_id))
    display_movies(titles, posters)








