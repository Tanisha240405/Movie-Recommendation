import streamlit as st
import pandas as pd
import numpy as np
import requests
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")
st.markdown("Get top movie recommendations using Collaborative & Content-Based Filtering.")

@st.cache_data
def load_data():
    ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])

    genre_cols = ['unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime',
                  'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
                  'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

    raw_movies = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', names=list(range(24)), usecols=list(range(24)))
    raw_movies.columns = ['movie_id', 'title', 'release_date', 'video_release_date', 'IMDb_URL'] + genre_cols

    # Extract IMDb ID from IMDb_URL
    def extract_imdb_id(url):
        match = re.search(r'title/tt(\d+)', url)
        if match:
            return f'tt{match.group(1)}'
        else:
            return None

    raw_movies['imdb_id'] = raw_movies['IMDb_URL'].apply(lambda x: extract_imdb_id(x) if isinstance(x, str) else None)
    raw_movies['genres'] = raw_movies[genre_cols].apply(
        lambda row: ','.join([g for g, val in zip(genre_cols, row) if val == 1]), axis=1
    )

    movies = raw_movies[['movie_id', 'title', 'genres', 'imdb_id']]
    data = pd.merge(ratings, movies[['movie_id', 'title']], on='movie_id')
    user_movie_matrix = data.pivot_table(index='user_id', columns='title', values='rating')
    user_movie_matrix.fillna(0, inplace=True)

    collab_sim = cosine_similarity(user_movie_matrix.T)
    collab_df = pd.DataFrame(collab_sim, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['genres'])
    content_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    content_df = pd.DataFrame(content_sim, index=movies['title'], columns=movies['title'])

    return collab_df, content_df, sorted(user_movie_matrix.columns), movies

# 🔐 Replace this with your actual TMDB API key
TMDB_API_KEY = "your-api-from-tmdb-website"

# 🎬 Poster fetching using IMDb ID first, then title as fallback
def get_movie_poster(title, imdb_id=None):
    try:
        # 1. Try with IMDb ID
        if imdb_id:
            imdb_url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id"
            response = requests.get(imdb_url).json()
            results = response.get('movie_results', [])
            if results and results[0].get('poster_path'):
                return "https://image.tmdb.org/t/p/w500" + results[0]['poster_path']

        # 2. Fallback: title search
        clean_title = re.sub(r"\s*\(\d{4}\)", "", title)
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={clean_title}"
        response = requests.get(search_url).json()
        if response['results']:
            poster_path = response['results'][0].get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
    except:
        pass
    return "https://via.placeholder.com/300x450?text=No+Image"

collab_df, content_df, movie_titles, movies_df = load_data()

tab1, tab2 = st.tabs(["🔁 Collaborative Filtering", "🎭 Content-Based Filtering"])

with tab1:
    st.subheader("Collaborative Filtering")
    movie_name_cf = st.selectbox("Choose a movie:", movie_titles, key="cf")
    top_n_cf = st.slider("How many recommendations?", 1, 10, 5, key="slider_cf")

    if st.button("Get Collaborative Recommendations"):
        if movie_name_cf in collab_df:
            results = collab_df[movie_name_cf].sort_values(ascending=False)[1:top_n_cf+1]
            st.markdown("### 🎯 Top Recommendations:")
            for title, score in results.items():
                imdb_id = movies_df[movies_df['title'] == title]['imdb_id'].values[0]
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(get_movie_poster(title, imdb_id), width=120)
                with col2:
                    st.write(f"**{title}** — Similarity Score: {score:.2f}")
        else:
            st.warning("Movie not found.")

with tab2:
    st.subheader("Content-Based Filtering")
    movie_name_cb = st.selectbox("Choose a movie:", movie_titles, key="cb")
    top_n_cb = st.slider("How many recommendations?", 1, 10, 5, key="slider_cb")

    if st.button("Get Content-Based Recommendations"):
        if movie_name_cb in content_df:
            results = content_df[movie_name_cb].sort_values(ascending=False)[1:top_n_cb+1]
            st.markdown("### 🎯 Top Recommendations:")
            for title, score in results.items():
                imdb_id = movies_df[movies_df['title'] == title]['imdb_id'].values[0]
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(get_movie_poster(title, imdb_id), width=120)
                with col2:
                    st.write(f"**{title}** — Genre Similarity: {score:.2f}")
        else:
            st.warning("Movie not found.")
