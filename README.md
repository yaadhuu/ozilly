# Ozilly | Machine Learning Movie Recommendation Engine


**Ozilly** is a highly optimized, AI-powered content recommendation system. Built to demonstrate proficiency in Machine Learning, Data Engineering, and Full-Stack deployment, this project leverages vectorization and cosine similarity to deliver highly accurate, personalized cinematic suggestions in real-time.

**🟢 Live Deployment:** [weds2isikahulmykbeldox.streamlit.app](https://weds2isikahulmykbeldox.streamlit.app/)

---

## 🧠 Machine Learning & Architecture
The core recommendation engine relies on Natural Language Processing (NLP) and content-based filtering.
- **Feature Engineering & NLP:** Processed metadata (genres, keywords, cast, crew) using `CountVectorizer` / `TfidfVectorizer` to convert text data into a multidimensional vector space.
- **Dimensionality & Similarity Matrix:** Computed the **Cosine Similarity** between movie vectors to mathematically determine content overlap, resulting in a pre-computed `184MB` similarity matrix.
- **O(1) Matrix Lookups:** The Streamlit application loads the pre-computed similarity matrix into memory via `pickle`, allowing for O(1) index lookups and instant recommendation sorting.

---

## 🛠 Complete Tech Stack

### Data Science & Machine Learning
- **Python (3.9+)**: Core programming language.
- **Scikit-Learn**: Used for NLP text vectorization and computing the Cosine Similarity matrix.
- **Pandas**: Utilized for massive dataset cleaning, preprocessing, and DataFrame manipulation.
- **NumPy**: Employed for high-performance array operations and matrix sorting.

### Software Engineering & Backend
- **RESTful API Integration**: Integrated with the **TMDB API** to fetch live metadata and high-resolution posters.
- **Concurrent Execution**: Implemented Python's `ThreadPoolExecutor` to perform asynchronous, parallel HTTP requests, dropping the API fetching time from ~8 seconds to < 1 second.
- **Cloud Data Streaming**: Implemented `gdown` to dynamically stream the massive `184MB` machine learning model from Google Drive directly into the app runtime, bypassing GitHub's strict file size limitations (LFS constraints).

### Frontend & Deployment
- **Streamlit**: Engineered the frontend interface with Python, utilizing `st.cache_data` and `st.cache_resource` for memoization and efficient state management.
- **Custom CSS/HTML Injection**: Overrode default Streamlit styling with advanced CSS to create a premium, minimalist (Space Grotesk & Syne typography) user interface.
- **Streamlit Community Cloud**: Automated CI/CD pipeline for live deployment straight from the GitHub repository.

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
   *Note: On first initialization, the application will automatically download the required ML similarity model via Google Drive. This ensures your local repository remains lightweight.*

---

## 📝 License
This project is open-source and available under the MIT License.
