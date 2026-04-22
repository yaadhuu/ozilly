# Ozilly | The Cinematic Oracle 🎬

![Ozilly App](https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=1200&q=80)

**Ozilly** is a premium, AI-powered movie recommendation engine built to deliver highly accurate, personalized cinematic suggestions. Designed with a stark, modern, and high-end editorial aesthetic, Ozilly provides users with a fluid, Netflix-style discovery experience.

**🟢 Live Deployment:** [weds2isikahulmykbeldox.streamlit.app](https://weds2isikahulmykbeldox.streamlit.app/)

---

## ✨ Features
- **Intelligent Recommendations**: Uses content-based filtering and cosine similarity matrix processing to accurately recommend 18 movies based on your selection.
- **Concurrent Asset Loading**: Connects to the TMDB API using threaded, concurrent execution to fetch high-resolution posters instantly.
- **Premium UI/UX**: Features a highly customized, Apple/Vercel-inspired stark minimalist design with `Space Grotesk` and `Syne` typography.
- **Smart Data Handling**: Dynamically downloads the massive machine learning model (`similarity.pkl`) from the cloud upon initialization to bypass GitHub storage limits.

---

## 🛠 Tech Stack
- **Frontend Framework**: [Streamlit](https://streamlit.io/)
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Machine Learning**: Scikit-Learn (Cosine Similarity)
- **External API**: [TMDB (The Movie Database) API](https://developer.themoviedb.org/docs)
- **Deployment**: Streamlit Community Cloud
- **Cloud Storage**: Google Drive (via `gdown`) for large binaries

---

## 🚀 Running Locally

### Prerequisites
- Python 3.9+
- A TMDB API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yaadhuu/ozilly.git
   cd ozilly
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run ozilly.py
   ```
   *Note: On first run, the app will automatically download the 184MB recommendation model via `gdown`. This may take a few moments depending on your network speed.*

---

## 📝 License
This project is open-source and available under the MIT License.
