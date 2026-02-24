 🎥 IMDb 2024 Data Scraping & Visualization 🎬
 
 🌍 Project Overview
This project focuses on extracting, analyzing, and visualizing IMDb movie data for the year **2024**. Using Selenium, movie details such as **Title, Genre, Duration, Rating, and Voting Counts** are collected. The dataset is cleaned using Pandas, stored in a SQL database, and explored through an interactive Streamlit dashboard with dynamic visualizations.

🧰 Technology Stack
* **Programming Language**: Python
* **Web Scraping Tool**: Selenium
* **Data Manipulation & Cleaning**: Pandas, NumPy
* **Database System**: SQL Database
* **Data Visualization**: Plotly
* **Dashboard Framework**: Streamlit

 📌 Key Analytical Objectives

✔ Identify top-performing movies based on ratings and votes

✔ Analyze distribution of movies across genres

✔ Evaluate average movie duration by genre

✔ Examine voting behavior trends

✔ Determine dominant genres in 2024

✔ Study rating patterns across movies

✔ Identify top-rated movies within each genre

✔ Detect shortest and longest movies

✔ Compare average ratings by genre

✔ Analyze correlation between ratings and voting counts

🚀 Dashboard Highlights

✔ Dynamic filtering based on rating, duration, votes, and genre

✔ Interactive visual components including:

* Top 10 Movies by Rating & Votes
* Genre Distribution (Bar Chart)
* Average Duration by Genre (Horizontal Bar Chart)
* Voting Trends Across Genres
* Rating Distribution (Histogram / Boxplot)
* Popular Genres by Total Votes (Pie Chart)
* Rating vs Voting Correlation (Scatter Plot)
* Top Movie in Each Genre (Table View)
* Duration Comparison (Shortest vs Longest)
* Genre-Wise Rating Heatmap

⚙️ Setup & Installation Guide

1️⃣ Repository Setup
git clone [https://github.com/yourusername/imdb-2024-analysis.git](https://github.com/anandhi07-tech/IMDB---2024-Data-Scraping-and-Visualization-.git)

2️⃣ Required Dependencies
Ensure the following are installed:
* Python 3.12+
* pip install pandas streamlit selenium numpy mysql-connector-python plotly

3️⃣ Database Configuration
1. Create a SQL database instance
2. Import the cleaned IMDb dataset
3. Update the database configuration file with connection details

4️⃣ Launch the Dashboard

streamlit run app.py


🌐 Accessing the Application

  *Local URL: http://localhost:8502
  *Network URL: http://192.168.0.106:8502

🖥️ Application Usage

🔎 Search and filter movies using interactive controls
📊 Explore overall market trends
🎯 Perform focused analysis using customized filters

📊 Data Description

The dataset includes IMDb movies from 2024 with the following attributes:

* Movie Name
* Genre
* Rating
* Voting Count
* Duration

🤝 Contribution Guidelines

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Submit a pull request


