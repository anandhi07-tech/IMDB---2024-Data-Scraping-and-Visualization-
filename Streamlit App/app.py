import streamlit as st
import pandas as pd
import mysql.connector
import re
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import statsmodels.api as sm


# Database Configuration
# -----------------------------
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Mysql@123",
    "database": "movies_database",
}

def convert_duration(duration_str):
    if pd.isna(duration_str) or duration_str == "None":
          return np.nan

    duration_str = str(duration_str).lower().strip()

    hours = 0
    minutes = 0

    # Match hours
    h_match = re.search(r'(\d+)\s*h', duration_str)
    if h_match:
        hours = int(h_match.group(1))

    # Match minutes
    m_match = re.search(r'(\d+)\s*m', duration_str)
    if m_match:
        minutes = int(m_match.group(1))

    # If pure number like "95"
    if hours == 0 and minutes == 0:
        if duration_str.isdigit():
            return int(duration_str)

    total_minutes = hours * 60 + minutes

    if total_minutes == 0:
        return np.nan

    return total_minutes


def convert_voting(vote_str):
    if pd.isna(vote_str) or vote_str in ["None", "", "nan", None]:
        return np.nan
    try:
        if "K" in vote_str:
            return float(vote_str.replace("K", "")) * 1000
        return float(vote_str)
    except ValueError:
        return np.nan
# Fetching data from Mysql
@st.cache_data
def fetch_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT Title,Genre,Duration,Rating,voting FROM movies;"
    df = pd.read_sql(query, conn)
    conn.close()

    df["Duration"] = df["Duration"].astype(str).apply(convert_duration).fillna(0)
    df["voting"] = df["voting"].astype(str).apply(convert_voting).fillna(0)
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").fillna(0)

    return df
movies_df = fetch_data()
# Sidebar Navigation
st.sidebar.title("Movie Arena")
page = st.sidebar.radio("Go to", ["Movie Market Analysis - 2024", "Discover Your Movie"])
# Custom styling
st.markdown(
    """
    <style>
        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #2b2b2b;
        }
         /* Sidebar labels white */
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] p {
            color: white !important;
        }

        /* Input box text black */
        section[data-testid="stSidebar"] input {
            color: black !important;
        }

        /* Dropdown text black */
        section[data-testid="stSidebar"] div[data-baseweb="select"] input {
            color: black !important;
             /* Sidebar title only */
        section[data-testid="stSidebar"] h1 {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
if page == "Movie Market Analysis - 2024":
    st.title("🎬 IMDb 2024 Movies Analysis - Overall")
# ---------------------------------------------
# Top 10 Movies by Rating & voting
# ---------------------------------------------
    st.markdown("### 📊 Top 10 Movies by Rating & voting")
    top_movies = (movies_df.sort_values(by=["Rating", "voting"], 
             ascending=[False, False]).head(10).reset_index(drop=True))

    col1, col2 = st.columns([3, 1])

    with col1:
     st.dataframe(
        top_movies,
        width='stretch',
        hide_index=True
    )

    with col2:
     st.metric(
        label="Highest Rating",
        value=round(top_movies["Rating"].max(), 2)
    )
     st.metric(
        label="Highest Votes",
        value=float(top_movies["voting"].max())
    )
# ---------------------------------------------
# Genre Distribution
# ---------------------------------------------

    st.markdown("### 🎭 Genre Distribution")

    genre_counts = (
    movies_df["Genre"]
    .value_counts()
    .reset_index()
   )

    genre_counts.columns = ["Genre", "Count"]

    fig = px.bar(
    genre_counts,
    x="Genre",
    y="Count",
    title="Number of Movies per Genre",
    text="Count"
   )

    fig.update_layout(
    xaxis_title="Genre",
    yaxis_title="Number of Movies",
    xaxis_tickangle=-45
   )

    st.plotly_chart(fig, width='stretch')

 # ---------------------------------------------
# Average Duration by Genre
# ---------------------------------------------

    st.markdown("### ⏳ Average Duration by Genre")

    avg_duration = (
    movies_df
    .groupby("Genre")["Duration"]
    .mean()
    .reset_index()
    )

    fig = px.bar(
    avg_duration,
    x="Duration",
    y="Genre",
    orientation="h",
    title="Average Movie Duration per Genre (Minutes)",
    text="Duration"
    )

    fig.update_layout(
    xaxis_title="Average Duration (Minutes)",
    yaxis_title="Genre"
    )

    st.plotly_chart(fig, width='stretch')
# ---------------------------------------------
# voting Trends by Genre
# ---------------------------------------------

    st.markdown("### 📈 voting Trends by Genre")

    avg_voting = (
    movies_df
    .groupby("Genre")["voting"]
    .mean()
    .reset_index()
    )

    fig = px.bar(
    avg_voting,
    x="Genre",
    y="voting",
    title="Average voting Count per Genre",
    text="voting"
    )

    fig.update_layout(
    xaxis_tickangle=-45,
    yaxis_title="Average Votes"
    )

    st.plotly_chart(fig, width='stretch')
# ---------------------------------------------
# Rating Distribution
# ---------------------------------------------

    st.markdown("### ⭐ Rating Distribution")

    fig = px.histogram(
    movies_df,
    x="Rating",
    nbins=20,
    title="Distribution of Movie Ratings"
    )

    st.plotly_chart(fig, width='stretch')
# ---------------------------------------------
# Top Rated Movie in Each Genre
# ---------------------------------------------

    st.markdown("### 🏆 Top Rated Movie per Genre")

    top_per_genre = movies_df.loc[
    movies_df.groupby("Genre")["Rating"].idxmax()
    ]

    st.dataframe(
    top_per_genre[["Genre", "Title", "Rating", "voting"]],
    width='stretch',
    hide_index=True
    ) 
# ---------------------------------------------
# Most Popular Genres by voting
# ---------------------------------------------

    st.markdown("### 🔥 Most Popular Genres by Total voting")

    total_votes = (
    movies_df
    .groupby("Genre")["voting"]
    .sum()
    .reset_index()
    )

    fig = px.pie(
    total_votes,
    names="Genre",
    values="voting",
    title="Total voting Distribution by Genre"
    )

    st.plotly_chart(fig, width='stretch')
# ---------------------------------------------
# Duration Extremes
# ---------------------------------------------

    st.markdown("### 🎬 Shortest & Longest Movies")

    shortest_movie = movies_df.loc[movies_df["Duration"].idxmin()]
    longest_movie = movies_df.loc[movies_df["Duration"].idxmax()]

    col1, col2 = st.columns(2)

    with col1:
     st.markdown("#### 🎥 Shortest Movie")
     st.write(shortest_movie)

    with col2:
     st.markdown("#### 🎥 Longest Movie")
     st.write(longest_movie)
    # ---------------------------------------------
# Average Ratings by Genre (Heatmap)
# ---------------------------------------------

    st.markdown("### 🎨 Average Ratings by Genre")

    heatmap_data = (
    movies_df
    .groupby("Genre")["Rating"]
    .mean()
    .reset_index()
    )

    fig = px.imshow(
    [heatmap_data["Rating"]],
    x=heatmap_data["Genre"],
    labels=dict(x="Genre", y="Average Rating"),
    title="Average Rating per Genre"
   )

    st.plotly_chart(fig, width='stretch')
# ---------------------------------------------
# Correlation: Rating vs voting
# ---------------------------------------------

    st.markdown("### 📊 Correlation: Rating vs voting")

    fig = px.scatter(
    movies_df,
    x="voting",
    y="Rating",
    title="Relationship Between Ratings and voting",
    trendline="ols"
    )
    st.plotly_chart(fig, width='stretch')
#if page =="Movie Market Analysis - 2024":
#st.title("📊 Movie Market Analysis - 2024")
#st.plotly_chart(fig, width='stretch')
elif page == "Discover Your Movie":
   st.title("🎬 Find Your Favorite Movies, Discover the Best! ")
   st.sidebar.header("Filters")
   selected_genre = st.sidebar.multiselect(
        "Select Genre", movies_df["Genre"].unique()
   )
   min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0, 0.1)
   max_rating = st.sidebar.slider("Maximum Rating", 0.0, 10.0, 10.0, 0.1)
   min_votes = st.sidebar.slider(
        "Minimum Votes", 0, 
        int(movies_df["voting"].max()), 1000, 100
   )
   movie_search = st.sidebar.text_input("Search Movie Name")
   duration_filter = st.sidebar.radio(
        "⏳ Select Duration:", 
        ["All", "< 2 hrs", "2-3 hrs", "> 3 hrs"]
   )
   filtered_df = movies_df [
    (movies_df["Rating"] >= min_rating) &
    (movies_df["Rating"] <= max_rating) &
    (movies_df["voting"] >= min_votes)
    ] 
   if duration_filter == "< 2 hrs":
        filtered_df = filtered_df[filtered_df["Duration"] < 120]
   elif duration_filter == "2-3 hrs":
        filtered_df = filtered_df[(filtered_df["Duration"] >= 120) & (filtered_df["Duration"] <= 180)]
   elif duration_filter == "> 3 hrs":
        filtered_df = filtered_df[filtered_df["Duration"] > 180]
   if selected_genre:
        filtered_df = filtered_df[filtered_df["Genre"].isin(selected_genre)]
   if movie_search:
        filtered_df = filtered_df[filtered_df["Title"].str.contains(movie_search, case=False, na=False)]
    
        st.dataframe(filtered_df.reset_index(drop=True))

   if not filtered_df.empty:
        # Top 10 Movies by Rating & Votes
        st.subheader("📊 Top 10 Movies by Rating & Votes")
        top_movies = filtered_df.sort_values(["Rating", "voting"], ascending=[False, False]).head(10)
        st.dataframe(top_movies)

        # Genre Distribution
        st.subheader("🎭 Genre Distribution ")
        genre_counts = filtered_df["Genre"].value_counts().reset_index()
        genre_counts.columns = ["Genre", "Count"]
        st.plotly_chart(px.bar(genre_counts, x="Genre", y="Count", title="Number of Movies per Genre "))

        # Average Duration by Genre
        st.subheader("⏳ Average Duration by Genre ")
        avg_duration = filtered_df.groupby("Genre")["Duration"].mean().reset_index()
        st.plotly_chart(px.bar(avg_duration, x="Duration", y="Genre", orientation="h", title="Average Duration per Genre "))

        # voting Trends by Genre
        st.subheader("📈 voting Trends ")
        avg_voting = filtered_df.groupby("Genre")["voting"].mean().reset_index()
        st.plotly_chart(px.bar(avg_voting, x="Genre", y="voting", title="Average voting Counts per Genre "))

        # Rating Distribution
        st.subheader("⭐ Rating Distribution ")
        st.plotly_chart(px.histogram(filtered_df, x="Rating", nbins=20, title="Rating Distribution of Movies"))

        # Top Rated Movie per Genre
        st.subheader("🏆 Top Rated Movie in Each Genre")
        top_per_genre = filtered_df.loc[filtered_df.groupby("Genre")["Rating"].idxmax()]
        st.dataframe(top_per_genre[["Genre", "Title", "Rating"]])

        # Most Popular Genres by voting
        st.subheader("🔥 Most Popular Genres by voting ")
        total_votes_by_genre = filtered_df.groupby("Genre")["voting"].sum().reset_index()
        st.plotly_chart(px.pie(total_votes_by_genre, names="Genre", values="voting", title="Most Popular Genres by voting "))

        # Shortest & Longest Movies
        valid_movies = filtered_df[filtered_df["Duration"] > 0]
        if not valid_movies.empty:
            shortest_movie = valid_movies.loc[valid_movies["Duration"].idxmin()]
            longest_movie = valid_movies.loc[valid_movies["Duration"].idxmax()]

            st.subheader("🎥 Shortest & Longest Movies")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🎬 Shortest Movie")
                st.markdown(f"**Title:** {shortest_movie['Title']}")
                st.markdown(f"**Duration:** ⏳ {shortest_movie['Duration']} mins")
                st.markdown(f"**Rating:** ⭐ {shortest_movie['Rating']}")
                st.markdown(f"**Genre:** 🎭 {shortest_movie['Genre']}")
                st.markdown("---")

            with col2:
                st.markdown("### 🎬 Longest Movie")
                st.markdown(f"**Title:** {longest_movie['Title']}")
                st.markdown(f"**Duration:** ⏳ {longest_movie['Duration']} mins")
                st.markdown(f"**Rating:** ⭐ {longest_movie['Rating']}")
                st.markdown(f"**Genre:** 🎭 {longest_movie['Genre']}")
                st.markdown("---")

        # Ratings by Genre (Heatmap)
        st.subheader("🎨 Ratings by Genre ")
        heatmap_data = filtered_df.pivot_table(index="Genre", values="Rating", aggfunc="mean").reset_index()
        st.plotly_chart(px.imshow([heatmap_data["Rating"]], labels=dict(x="Genre", y="Average Rating"), x=heatmap_data["Genre"]))

        # Correlation Analysis
        st.subheader("📊 Correlation: Ratings vs Voting ")
        st.plotly_chart(px.scatter(filtered_df, x="voting", y="Rating", title="Correlation Between Ratings & Voting Counts "))
else:
        st.warning("No movies match your filters. Try adjusting the filters.")