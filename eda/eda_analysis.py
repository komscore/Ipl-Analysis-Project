# ============================================================
#   IPL EDA - EXPLORATORY DATA ANALYSIS
#   We ask questions, data gives answers, charts show them
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import os

# ============================================================
# SECTION 1: CONNECT TO MYSQL & LOAD DATA
# We read directly from our database — not CSV anymore!
# ============================================================

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="Stock@123",   # ← your MySQL password
    host="127.0.0.1",
    database="ipl_db",
    port=3306
)

engine = create_engine(connection_url)

os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts"), exist_ok=True)
CHARTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")

# Read both tables from MySQL into pandas dataframes
matches = pd.read_sql("SELECT * FROM matches", engine)
deliveries = pd.read_sql("SELECT * FROM deliveries", engine)

print("✅ Data loaded from MySQL")
print(f"   matches: {matches.shape}")
print(f"   deliveries: {deliveries.shape}")

# Global chart style — makes all charts look clean and professional
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.titleweight"] = "bold"


# ============================================================
# ANALYSIS 1: Which team has won the most matches?
# ============================================================

# Count wins per team, exclude 'No Result' matches
wins = (
    matches[matches["winner"] != "No Result"]
    .groupby("winner")["match_id"]
    .count()
    .sort_values(ascending=False)
    .reset_index()
)
wins.columns = ["team", "wins"]

plt.figure()
sns.barplot(data=wins, x="wins", y="team", hue="team", palette="Blues_r", legend=False)
plt.title("Total Wins by Team — All IPL Seasons")
plt.xlabel("Number of Wins")
plt.ylabel("Team")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "01_total_wins_by_team.png"), dpi=150)
plt.show()
print("✅ Chart 1 saved: Total wins by team")


# ============================================================
# ANALYSIS 2: Does winning the toss help win the match?
# ============================================================

toss_impact = (
    matches.groupby("toss_match_winner")["match_id"]
    .count()
    .reset_index()
)
toss_impact.columns = ["toss_won_match", "count"]
toss_impact["toss_won_match"] = toss_impact["toss_won_match"].map(
    {1: "Yes — Toss & Match Won", 0: "No — Toss Won, Match Lost"}
)

plt.figure(figsize=(7, 7))
plt.pie(
    toss_impact["count"],
    labels=toss_impact["toss_won_match"],
    autopct="%1.1f%%",
    colors=["#4C72B0", "#DD8452"],
    startangle=90
)
plt.title("Does Winning the Toss Help Win the Match?")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR,"02_toss_impact.png"), dpi=150)
plt.show()
print("✅ Chart 2 saved: Toss impact")


# ============================================================
# ANALYSIS 3: Toss decision — bat or field first?
# ============================================================

toss_decision = (
    matches.groupby(["season", "toss_decision"])["match_id"]
    .count()
    .reset_index()
)
toss_decision.columns = ["season", "decision", "count"]

plt.figure()
sns.lineplot(
    data=toss_decision,
    x="season", y="count",
    hue="decision", marker="o"
)
plt.title("Toss Decision Trend — Bat vs Field Across Seasons")
plt.xlabel("Season")
plt.ylabel("Number of Times Chosen")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "03_toss_decision_trend.png"), dpi=150)
plt.show()
print("✅ Chart 3 saved: Toss decision trend")


# ============================================================
# ANALYSIS 4: Top 10 venues by number of matches hosted
# ============================================================

venue_counts = (
    matches.groupby("venue")["match_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
venue_counts.columns = ["venue", "matches"]

plt.figure()
sns.barplot(data=venue_counts, x="matches", y="venue", hue="venue", palette="Greens_r", legend=False)
plt.title("Top 10 Venues by Matches Hosted")
plt.xlabel("Number of Matches")
plt.ylabel("Venue")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "04_top_venues.png"), dpi=150)
plt.show()
print("✅ Chart 4 saved: Top venues")


# ============================================================
# ANALYSIS 5: Top 10 batsmen by total runs scored
# ============================================================

top_batsmen = (
    deliveries.groupby("batsman")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
top_batsmen.columns = ["batsman", "total_runs"]

plt.figure()
sns.barplot(data=top_batsmen, x="total_runs", y="batsman", hue="batsman", palette="Oranges_r", legend=False)
plt.title("Top 10 Batsmen by Total Runs — All IPL Seasons")
plt.xlabel("Total Runs")
plt.ylabel("Batsman")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "05_top_batsmen.png"), dpi=150)
plt.show()
print("✅ Chart 5 saved: Top batsmen")


# ============================================================
# ANALYSIS 6: Top 10 bowlers by total wickets taken
# ============================================================

top_bowlers = (
    deliveries[deliveries["is_wicket"] == 1]
    .groupby("bowler")["is_wicket"]
    .count()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
top_bowlers.columns = ["bowler", "wickets"]

plt.figure()
sns.barplot(data=top_bowlers, x="wickets", y="bowler", hue="bowler", palette="Purples_r", legend=False)
plt.title("Top 10 Bowlers by Total Wickets — All IPL Seasons")
plt.xlabel("Total Wickets")
plt.ylabel("Bowler")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "06_top_bowlers.png"), dpi=150)
plt.show()
print("✅ Chart 6 saved: Top bowlers")


# ============================================================
# ANALYSIS 7: Season-wise total runs scored (batting trends)
# ============================================================

# First merge deliveries with matches to get season info
deliveries_with_season = deliveries.merge(
    matches[["match_id", "season"]], on="match_id", how="left"
)

season_runs = (
    deliveries_with_season.groupby("season")["total_runs"]
    .sum()
    .reset_index()
)
season_runs.columns = ["season", "total_runs"]

plt.figure()
sns.lineplot(data=season_runs, x="season", y="total_runs", marker="o", color="#4C72B0")
plt.title("Total Runs Scored Per Season")
plt.xlabel("Season")
plt.ylabel("Total Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "07_season_runs.png"), dpi=150)
plt.show()
print("✅ Chart 7 saved: Season-wise runs")


# ============================================================
# ANALYSIS 8: Win by runs vs win by wickets distribution
# =============================================