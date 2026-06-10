# 🎬 Ozilly

> **Your personal movie recommender. Netflix vibes, cosine similarity under the hood.**  
> Type a movie. Hit recommend. Get 18 handpicked suggestions instantly — pulled from a pre-computed ML similarity matrix and enriched with live TMDB posters and metadata.

<p align="center">
  <a href="https://weds2isikahulmykbeldox.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/🚀 Live Demo-Streamlit Cloud-E50914?style=for-the-badge" alt="Live Demo"/>
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
  <img src="https://img.shields.io/badge/TMDB_API-01D277?style=for-the-badge&logo=themoviedatabase&logoColor=white"/>
  <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
</p>

---

## ⚙️ How It Works

Ozilly is a **content-based filtering** recommendation engine. It doesn't need ratings or user history — it understands movies by their content.

```
Movie Input
    │
    ▼
NLP Feature Engineering
(genres + keywords + cast + crew → CountVectorizer / TfidfVectorizer)
    │
    ▼
184MB Cosine Similarity Matrix  ←── pre-computed & stored as similarity.pkl
    │
    ▼
O(1) Index Lookup → Top 18 most similar movies
    │
    ▼
Parallel TMDB API calls (ThreadPoolExecutor) → Posters + Metadata
    │
    ▼
Streamlit UI renders a 6-column movie grid
```

### Key Engineering Decisions

**Parallel API fetching** — Instead of firing TMDB requests one by one (~8s), `ThreadPoolExecutor` fires them all concurrently, bringing fetch time down to under 1 second.

**Cloud model streaming** — The 184MB `similarity.pkl` is too large for GitHub. On first run, `gdown` streams it directly from Google Drive into the app runtime. Repo stays lightweight; model is always available.

**`st.cache_data` / `st.cache_resource`** — Streamlit memoization ensures the model and movie dataframe are loaded once into memory. No redundant disk reads on re-renders.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎯 Content-Based Recommendations | 18 results per search, ranked by cosine similarity score |
| 🎞️ Searchable Dropdown | Type-ahead select across the full movie dataset |
| 🖼️ Live Poster Fetching | High-res posters pulled from TMDB API in real time |
| 📋 Movie Detail Expanders | Release date, overview, and rating per recommendation |
| 🎲 Explore Mode | Random 18-movie grid on load + "Load More" to reshuffle |
| 🎨 Custom Netflix-Style UI | CSS-injected dark theme with Roboto typography and red gradient branding |

---

## 🗂️ Project Structure

```
ozilly/
├── ozilly.py          # Main Streamlit app — UI, recommendation logic, API calls
├── movie_dict.pkl     # Pickled movie DataFrame (titles + movie IDs)
├── model/             # ML model artifacts (notebook + preprocessing scripts)
├── requirements.txt   # Python dependencies
├── setup.sh           # Streamlit Cloud deployment config (headless server setup)
└── .gitignore         # Excludes similarity.pkl (184MB — streamed from Drive at runtime)
```

> `similarity.pkl` is **not in the repo** — it's auto-downloaded from Google Drive on first run via `gdown`. This is by design to keep the repo under GitHub's file size limits.

---

## 🚀 Running Locally

**Prerequisites:** Python 3.9+, a TMDB API key

```bash
# 1. Clone
git clone https://github.com/yaadhuu/ozilly.git
cd ozilly

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Run
streamlit run ozilly.py
```

> On first launch, the app will automatically download `similarity.pkl` (~184MB) from Google Drive. This only happens once — subsequent runs load from disk.

---

## 📦 Dependencies

```
streamlit       # Frontend framework
pandas          # Dataset handling
numpy           # Matrix operations
scikit-learn    # TF-IDF vectorization + cosine similarity
requests        # TMDB API calls
gdown           # Google Drive model download
```

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| ML / NLP | scikit-learn — CountVectorizer / TfidfVectorizer, Cosine Similarity |
| Data Processing | pandas, NumPy |
| Frontend | Streamlit + custom CSS/HTML injection |
| Movie Metadata | TMDB REST API |
| Model Distribution | Google Drive + gdown |
| Concurrency | Python `concurrent.futures.ThreadPoolExecutor` |
| Deployment | Streamlit Community Cloud (CI/CD via GitHub) |

---

## 📌 About

Built by **Yeadhu Krishna** — [github.com/yaadhuu](https://github.com/yaadhuu)  
📧 yeadhukrishna.p@gmail.com  
📄 MIT License

---

<p align="center">Find your next favorite film. 🎬</p>
