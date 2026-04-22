import streamlit as st
import pickle
import pandas as pd
import random
import requests
import os
import gdown
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(page_title="Ozilly | Premium Cinematic Discovery", layout="wide", initial_sidebar_state="collapsed")

# --- Custom CSS for Award-Winning UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Reset & Dark Theme */
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Hide Streamlit elements */
    header, [data-testid="stToolbar"], footer { display: none !important; }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .hero-title {
        font-size: 4.5rem;
        color: #ffffff;
        margin-bottom: 0.5rem;
        text-align: center;
        letter-spacing: -0.04em;
        font-weight: 800;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #a1a1aa;
        font-size: 1.1rem;
        font-weight: 400;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 4rem;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    /* Search Bar */
    [data-baseweb="select"] {
        background-color: #0a0a0a !important;
        border: 1px solid #333333 !important;
        border-radius: 8px;
        transition: border-color 0.2s ease;
    }
    [data-baseweb="select"]:hover, [data-baseweb="select"]:focus-within {
        border-color: #ffffff !important;
    }
    
    /* Buttons */
    div.stButton > button {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #ffffff;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #e5e5e5;
        border-color: #e5e5e5;
        color: #000000;
        transform: translateY(-1px);
    }
    
    /* Movie Cards */
    [data-testid="stImage"] {
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        cursor: pointer;
        object-fit: cover;
        aspect-ratio: 2/3;
        border: 1px solid rgba(255,255,255,0.05);
    }
    [data-testid="stImage"]:hover {
        transform: scale(1.03) translateY(-4px);
        box-shadow: 0 12px 30px rgba(255,255,255,0.05);
        border-color: rgba(255,255,255,0.15);
        z-index: 10;
    }
    
    .movie-card-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        color: #e4e4e7;
        margin-top: 10px;
        text-align: center;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
    }
    
    /* Expanders */
    [data-testid="stExpander"] {
        border: 1px solid #27272a !important;
        background: #09090b !important;
        border-radius: 8px !important;
        margin-top: -8px;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 3.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #27272a;
        padding-bottom: 0.75rem;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_resource(show_spinner="Initializing Cinematic Engine...")
def download_similarity():
    file_path = "similarity.pkl"
    if not os.path.exists(file_path):
        url = "https://drive.google.com/uc?id=1Y2rRA4DGpNXRCJ09J1lOx-JlnV6OBtl6"
        gdown.download(url, file_path, quiet=False)

download_similarity()

@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

# --- TMDB API ---
API_KEY = "e751b9b29910a0685e127c23f664a451"
FALLBACK_POSTER = "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"

@st.cache_data(show_spinner=False, ttl=86400)
def fetch_poster(movie_id):
    try:
        # Some datasets contain string IDs or invalid formats, ensuring it's an int/string
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else FALLBACK_POSTER
            return poster_url, data
    except Exception:
        pass
    return FALLBACK_POSTER, {}

def fetch_posters_concurrently(movie_ids):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_poster, movie_ids))
    return results

# --- Recommendation Logic ---
def recommend(movie):
    movie = movie.strip().lower()
    matches = movies[movies['title'].str.lower() == movie]
    if matches.empty:
        return [], [], []
    
    idx = matches.index[0]
    distances = similarity[idx]
    # Get top 18 recommendations
    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:19]
    
    rec_indices = [i[0] for i in movie_list]
    rec_movies = movies.iloc[rec_indices]
    
    titles = rec_movies['title'].tolist()
    movie_ids = rec_movies['movie_id'].tolist()
    
    fetched_data = fetch_posters_concurrently(movie_ids)
    posters = [data[0] for data in fetched_data]
    details = [data[1] for data in fetched_data]
    
    return titles, posters, details

# --- UI Components ---
def display_movie_grid(titles, posters, movie_details):
    cols_per_row = 6
    for i in range(0, len(titles), cols_per_row):
        cols = st.columns(cols_per_row)
        for idx, col in enumerate(cols):
            if i + idx < len(titles):
                with col:
                    title = titles[i + idx]
                    poster = posters[i + idx]
                    details = movie_details[i + idx]
                    
                    st.image(poster, width='stretch')
                    st.markdown(f"<div class='movie-card-title'>{title}</div>", unsafe_allow_html=True)
                    
                    # Expandable details
                    with st.expander("View Details"):
                        st.markdown(f"**Released:** {details.get('release_date', 'N/A')}")
                        st.markdown(f"**Rating:** ⭐ {details.get('vote_average', 'N/A')}/10")
                        overview = details.get('overview', 'No synopsis available.')
                        # Truncate overview if too long
                        if len(overview) > 150: overview = overview[:147] + "..."
                        st.caption(overview)
        st.write("") # Spacer between rows

# --- Main App Layout ---
st.markdown("<h1 class='hero-title'>Ozilly</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>The Cinematic Oracle</p>", unsafe_allow_html=True)

# Search Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie = st.selectbox(
        "Search the cinematic universe...",
        movies['title'].values,
        index=None,
        placeholder="E.g. Inception, The Dark Knight, Interstellar..."
    )
    search_btn = st.button("Discover Recommendations")

st.markdown("<br><br>", unsafe_allow_html=True)

if search_btn and selected_movie:
    with st.spinner(f"Consulting the oracle for '{selected_movie}'..."):
        titles, posters, details = recommend(selected_movie)
    
    if titles:
        st.markdown(f"<h2 class='section-title'>Because you watched <i>{selected_movie}</i></h2>", unsafe_allow_html=True)
        display_movie_grid(titles, posters, details)
    else:
        st.error("Movie not found in the oracle's database.")
else:
    # Display Trending/Discover section
    st.markdown("<h2 class='section-title'>Discover Masterpieces</h2>", unsafe_allow_html=True)
    
    # Select random 18 movies for the discover section
    # Using a fixed seed based on the hour to keep it stable but changing occasionally
    import datetime
    random.seed(datetime.datetime.now().hour)
    sample_indices = random.sample(range(len(movies)), 18)
    sample_movies = movies.iloc[sample_indices]
    
    titles = sample_movies['title'].tolist()
    movie_ids = sample_movies['movie_id'].tolist()
    
    fetched_data = fetch_posters_concurrently(movie_ids)
    posters = [data[0] for data in fetched_data]
    details = [data[1] for data in fetched_data]
    
    display_movie_grid(titles, posters, details)
