📱**PhonePe Pulse Data Analysis Dashboard** 


📌 Project Overview

This project analyzes digital payment trends in India using the PhonePe Pulse dataset and presents insights through an interactive Streamlit dashboard.

The objective of this project is to understand how digital payments are growing across India and identify patterns in transactions, user engagement, and insurance adoption.

Key Objectives

• Analyze transaction value and volume across Indian states and districts
• Understand user registration growth and app engagement
• Identify regions with high digital payment adoption
• Study insurance usage trends within the PhonePe ecosystem
• Build an interactive dashboard to visualize insights

The project demonstrates a complete data analytics pipeline, including:

Data extraction from GitHub

Data transformation using Python

Data storage using SQL

Data analysis using SQL queries

Data visualization using Streamlit and Python libraries

🛠 Code and Resources Used
Programming Language

Python 3.x

(Update this if you know your exact version. You can check using python --version.)

Libraries Used
Library	Purpose
Pandas	Data manipulation and analysis
Streamlit	Interactive dashboard development
MySQL Connector	Connecting Python with MySQL database
Matplotlib	Creating charts and plots
Plotly	Interactive visualizations
JSON	Parsing raw dataset files

Example installation:

pip install pandas streamlit mysql-connector-python matplotlib plotly
Development Tools

• Python
• Jupyter Notebook
• MySQL Database
• Streamlit
• Git & GitHub

External Resources Used
PhonePe Dataset

Dataset Source:

PhonePe Pulse GitHub Repository

https://github.com/PhonePe/pulse

This repository contains public data about digital payments in India.

India Choropleth Map (GeoJSON)

The India state map used in the dashboard was obtained from:

https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson

This GeoJSON file is used to create the interactive India map visualization in the Streamlit dashboard.

📊 Dataset Description

The dataset used in this project comes from the PhonePe Pulse GitHub repository.

The data is organized in JSON format and contains information about digital transactions across India.

The dataset is categorized into three main sections.

1️⃣ Aggregated Data

Aggregated data provides summarized metrics across different states.

Tables created:

Table Name	Description
aggregated_user	Contains registered users and app opens
aggregated_transaction	Contains transaction value and transaction count
aggregated_insurance	Contains insurance transaction data

This data helps analyze:

• Transaction growth
• User adoption
• Insurance usage

2️⃣ Map Data

Map data provides more granular location-based insights.

Tables created:

Table Name	Description
map_user	User distribution across districts
map_transaction	Transaction mapping across states and districts
map_insurance	Insurance distribution data

This data is useful for geographical analysis.

3️⃣ Top Data

Top data provides the highest performing regions.

Tables created:

Table Name	Description
top_user	Top users by region
top_transaction	Top states, districts and pincodes by transaction
top_insurance	Top regions by insurance usage

This helps identify high-performing regions.

🧹 Data Cleaning and Preprocessing

Before analysis, the dataset required several preprocessing steps.

Data Cleaning Steps

• Extracted data from JSON files
• Converted nested JSON structures into structured tables
• Standardized state names for consistency
• Removed formatting issues such as hyphens in state names
• Converted data types for numerical analysis
• Handled missing values where necessary

Example transformation used in the dashboard:

df["State"] = df["State"].str.replace("-", " ").str.title()

This ensured the state names match the GeoJSON map structure.

🔍 Exploratory Data Analysis (EDA)

Exploratory Data Analysis was performed using SQL queries and Python visualizations.

The analysis focuses on five business case studies.

1️⃣ Transaction Analysis for Market Expansion

This analysis explores:

• Total transaction value by state
• Total transaction count by state
• Year-wise transaction growth
• Quarterly transaction trends
• Average transaction value per state

Purpose:

To identify regions with strong digital payment adoption.

2️⃣ User Engagement and Growth Strategy

Key metrics analyzed:

• Total registered users by state
• Total app opens by state
• User engagement rate
• Year-wise user growth
• Quarterly user growth trends

Purpose:

To understand user activity and engagement patterns.

3️⃣ Insurance Engagement Analysis

Analysis includes:

• Insurance amount by state
• Total insurance policies by state
• District contribution to insurance value
• Year-wise insurance growth
• Average insurance value per district

Purpose:

To identify insurance adoption trends.

4️⃣ Transaction Analysis Across States and Districts

This analysis explores:

• Top districts by transaction value
• Top pincodes by transaction count
• Average transaction value by district
• Transaction growth over time

Purpose:

To identify high-value digital payment regions.

5️⃣ User Registration Analysis

Metrics analyzed:

• State-wise total registrations
• Quarterly registration growth
• Top districts by registration
• Top pincodes by registrations

Purpose:

To understand regional adoption of PhonePe services.

📈 Dashboard Features

An interactive dashboard was built using Streamlit.

Main features include:

India Overview Map

The dashboard displays an interactive map showing:

• Transaction Value
• Registered Users
• Insurance Amount

Users can switch between different metrics using a dropdown.

Business Case Analysis

The dashboard contains five analytical sections.

Each section includes:

• SQL-based data queries
• Visualizations using Matplotlib and Plotly
• Key insights explaining the results

Interactive Filters

Users can interact with the dashboard by selecting:

• Year
• State
• Case study

This allows deeper exploration of the dataset.

📷 Dashboard Preview

(Add screenshots here in GitHub)

Example:

/screenshots/dashboard_home.png
/screenshots/analysis_page.png
🚀 How to Run the Project
Step 1

Clone the repository

git clone https://github.com/yourusername/phonepe-pulse-dashboard.git
Step 2

Install required libraries

pip install -r requirements.txt
Step 3

Run the Streamlit application

streamlit run app.py
📊 Key Insights

Some insights discovered during the analysis:

• Digital payment transactions have grown significantly over the years.
• States like Maharashtra and Karnataka dominate transaction value.
• High user registrations strongly correlate with high app engagement.
• Insurance adoption is increasing steadily across districts.
• Certain districts contribute disproportionately to transaction volume.

🔮 Future Improvements

Possible enhancements for this project include:

• Adding district-level interactive maps
• Implementing real-time data updates
• Adding predictive analytics models
• Creating mobile-friendly dashboard layout
• Deploying the dashboard on Streamlit Cloud or AWS

👨‍💻 Author

Charanraj S

Computer Science Engineering Graduate
Data Analytics & Python Enthusiast# phonepe-pulse-dashboard
Interactive data analytics dashboard analyzing PhonePe digital payment trends across India using Python, SQL, and Streamlit.
