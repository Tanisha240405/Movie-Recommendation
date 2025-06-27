# 🎬 Movie Recommendation System

This project is a movie recommender system built with **Streamlit** using the **MovieLens 100k dataset**. It supports two types of filtering:

- 🔁 Collaborative Filtering (based on user ratings)
- 🎭 Content-Based Filtering (based on movie genres)

It also integrates **TMDB API** to show movie posters using **IMDb IDs**.

---

## 📦 Features
- Dual-tab UI: Collaborative + Content-Based recommendations
- Live poster previews using TMDB API
- IMDb ID-based search for better poster accuracy
- Clean Streamlit UI

---

## 📂 Dataset
The app uses the [MovieLens 100k dataset](https://grouplens.org/datasets/movielens/100k/).  
Ensure the folder `ml-100k` is placed in the same directory as `app.py`.

---

## 🚀 How to Run

1. Clone this repo or download the ZIP  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
🔐 TMDB API Key

To use poster preview features, you must add your own TMDB API key.

Create an account and get your key: https://www.themoviedb.org/settings/api
Set the environment variable:
On Linux/macOS (Terminal):

export TMDB_API_KEY=your_key_here
On Windows (CMD):

set TMDB_API_KEY=your_key_here
Then run the app:
streamlit run app.py

## Preview 

![WhatsApp Image 2025-06-27 at 3 00 14 PM](https://github.com/user-attachments/assets/59c218ee-7ba2-47b0-b267-7cb51bfeb473)

![WhatsApp Image 2025-06-27 at 3 00 14 PM (1)](https://github.com/user-attachments/assets/0398e413-0264-4e7e-8adc-9d75a9d91298)

## 📄 Report

Refer to Movie_Recommendation_Report.pdf for technical documentation and summary.

## 👨‍💻 Developed By

Tanisha Bhargava – Internship Project, June 2025
