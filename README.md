# 🏏 IPL Data Analysis Project
### End-to-End Data Pipeline | ETL · MySQL · EDA · Power BI

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql&logoColor=white)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Project Overview

An end-to-end data analysis project on **15+ seasons of IPL cricket data** covering **636 matches** and **150,000+ ball-by-ball deliveries**.

Built a complete data pipeline that:
- **Extracts** raw CSV data and cleans it using Pandas & NumPy
- **Loads** structured data into a MySQL relational database
- **Analyzes** team performance, player consistency, toss patterns & venue trends
- **Visualizes** insights through an interactive 3-page Power BI dashboard

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| 🐍 Python (Pandas, NumPy) | ETL Pipeline & Data Cleaning |
| 🗄️ MySQL | Structured Relational Data Storage |
| 📊 Matplotlib & Seaborn | Exploratory Data Analysis & Charts |
| 📈 Power BI | Interactive 3-Page Dashboard |
| 🔧 SQLAlchemy & PyMySQL | Python–MySQL Connection |
| 🐙 Git & GitHub | Version Control |

---

## 📁 Project Structure
IPL-Analysis-Project/
│
├── 📂 data/
│   └── matches.csv              # Raw match-level data (636 matches)
│
├── 📂 etl/
│   └── etl_pipeline.py          # Extract → Transform → Load pipeline
│
├── 📂 eda/
│   ├── eda_analysis.py               # EDA script with 8 charts
│   └── 📂 charts/                    # Generated PNG chart outputs
│       ├── 01_total_wins_by_team.png
│       ├── 02_toss_impact.png
│       ├── 03_toss_decision_trend.png
│       ├── 04_top_venues.png
│       ├── 05_top_batsmen.png
│       ├── 06_top_bowlers.png
│       ├── 07_season_runs.png
│       └── 08_win_distribution.png
│
├── 📂 sql/
│   ├── export_to_csv.py              # MySQL → CSV export for Power BI
│   └── 📂 exports/                   # Exported aggregated CSV files
│       ├── matches.csv
│       ├── season_summary.csv
│       ├── team_wins.csv
│       ├── top_batsmen.csv
│       ├── top_bowlers.csv
│       ├── toss_analysis.csv
│       └── venue_analysis.csv
---

## ⚙️ ETL Pipeline

The pipeline processes raw IPL data through 3 stages:

**Extract** → Read raw CSV files into Pandas DataFrames  
**Transform** → Clean, fix, and enrich the data:
- Dropped null columns (`umpire3`, `dl_applied`)
- Standardized team names across seasons
- Filled missing values in `city`, `winner`, `player_of_match`
- Added derived column: `toss_match_winner`
- Added `is_wicket` column to deliveries
- Removed super over deliveries for clean analysis

**Load** → Push cleaned data into MySQL (`ipl_db` database)

```python
matches    → 636 rows,    17 columns
deliveries → 150,379 rows, 21 columns
```

---

## 📊 Exploratory Data Analysis

| # | Chart | Key Insight |
|---|-------|-------------|
| 1 | Total Wins by Team | Mumbai Indians lead with most wins all-time |
| 2 | Toss Impact | 57% chose to field first after winning toss |
| 3 | Toss Decision Trend | Fielding first became dominant post-2012 |
| 4 | Top 10 Venues | M Chinnaswamy Stadium hosted the most matches |
| 5 | Top 10 Batsmen | SK Raina is the all-time leading run scorer |
| 6 | Top 10 Bowlers | SL Malinga leads with the most wickets |
| 7 | Season-wise Runs | Runs peaked around 2013–2014 season |
| 8 | Win Distribution | Most teams win chases by 1–4 wickets |

---

## 📈 Power BI Dashboard

Interactive 3-page dashboard:

**Page 1 — Team Overview**
- Total wins by team · Toss decision breakdown
- Season-wise total runs · Total matches played

**Page 2 — Player Analysis**
- Top 10 batsmen by total runs
- Top 10 bowlers by total wickets

**Page 3 — Venue Analysis**
- Top 10 venues by matches hosted
- Season-wise wins by team

---

## 🔍 Key Insights

- 🏆 **Mumbai Indians** are the most dominant IPL team across all seasons
- 🎲 **57% of toss winners** chose to field first
- 🏏 **SK Raina** scored the most runs across all IPL seasons
- 🎳 **SL Malinga** is the highest wicket-taker across all seasons
- 🏟️ **M Chinnaswamy Stadium** hosted the most IPL matches

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/komscore/IPL-Analysis-Project.git

# 2. Install dependencies
pip install pandas numpy sqlalchemy pymysql matplotlib seaborn cryptography

# 3. Create MySQL database
# Run in MySQL: CREATE DATABASE ipl_db;

# 4. Run ETL pipeline
python etl/etl_pipeline.py

# 5. Run EDA
python eda/eda_analysis.py

# 6. Export for Power BI
python sql/export_to_csv.py
```

---

## 👩‍💻 Author

**Komal Sharma**  
[![GitHub](https://img.shields.io/badge/GitHub-komscore-black?logo=github)](https://github.com/komscore)

---
*Built as a portfolio project to demonstrate end-to-end data engineering and analytics skills.*