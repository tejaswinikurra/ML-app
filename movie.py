import streamlit as st
import pandas as pd
import ast

# Load data
titles_path = "titles.csv"
credits_path = "credits.csv"

titles_df = pd.read_csv(titles_path)
credits_df = pd.read_csv(credits_path)

# Merge titles and credits on id
movies_df = pd.merge(titles_df, credits_df, on="id", how="left")

# Streamlit App
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🍿",
    layout="wide"
)


# Custom HTML/CSS for better visuals
st.markdown("""
    <style>
        body {
            background-color: #0f1117;
            color: #f0f2f6;
            font-family: 'Segoe UI', sans-serif;
        }
        .stSelectbox label, .stSlider label {
            color: #f0f2f6;
        }
        .title-text {
            font-size: 2.5em;
            font-weight: bold;
            color: #00ffcc;
        }
        .movie-title {
            font-size: 1.2em;
            font-weight: 600;
            color: #66ffcc;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-text">🎬 Movie Recommendation System</p>', unsafe_allow_html=True)
st.write("Find top movies by genre and year!")

# Genre cleaning
def clean_genre(genre_str):
    try:
        genre_list = ast.literal_eval(genre_str)
        if isinstance(genre_list, list):
            return [g.strip() for g in genre_list]
    except:
        pass
    return []

all_genres = titles_df['genres'].dropna().apply(clean_genre).explode().dropna().unique()
selected_genre = st.sidebar.selectbox("🎭 Choose a genre:", sorted(all_genres))

# Year filter
years = titles_df['release_year'].dropna().astype(int)
min_year = years.min()
max_year = years.max()
year_range = st.sidebar.slider("📅 Select release year range:", int(min_year), int(max_year), (2000, 2023))

# Filter logic
filtered_movies = titles_df[
    titles_df['genres'].apply(lambda g: selected_genre in clean_genre(g) if pd.notna(g) else False)
    & titles_df['release_year'].between(year_range[0], year_range[1])
]

# Display top movies
st.subheader(f"Top {min(10, len(filtered_movies))} {selected_genre} Movies ({year_range[0]} - {year_range[1]}):")

col1, col2 = st.columns(2)
for i, (index, row) in enumerate(filtered_movies.head(10).iterrows()):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"<div class='movie-title'>🎥 {row['title']} ({row['release_year']})</div>", unsafe_allow_html=True)
        if pd.notna(row.get("description")):
            st.markdown(f"> {row['description']}")
        st.markdown("---")
