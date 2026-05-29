# ============================================================
#   EXPORT MySQL DATA TO CSV
#   For uploading into Power BI Service
# ============================================================

import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# ============================================================
# CONNECT TO MYSQL
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

# Output folder — saves CSVs inside sql/exports/
EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

print("📤 Exporting tables from MySQL to CSV...\n")

# ============================================================
# EXPORT 1: matches table (straightforward)
# ============================================================

matches = pd.read_sql("SELECT * FROM matches", engine)
matches.to_csv(os.path.join(EXPORT_DIR, "matches.csv"), index=False)
print(f"   ✅ matches.csv exported → {len(matches)} rows")

# ============================================================
# EXPORT 2: deliveries table (straightforward)
# ============================================================

deliveries = pd.read_sql("SELECT * FROM deliveries", engine)
deliveries.to_csv(os.path.join(EXPORT_DIR, "deliveries.csv"), index=False)
print(f"   ✅ deliveries.csv exported → {len(deliveries)} rows")

# ============================================================
# EXPORT 3: team wins summary (pre-aggregated for Power BI)
# ============================================================

team_wins = pd.read_sql("""
    SELECT winner AS team, COUNT(*) AS total_wins
    FROM matches
    WHERE winner != 'No Result'
    GROUP BY winner
    ORDER BY total_wins DESC
""", engine)
team_wins.to_csv(os.path.join(EXPORT_DIR, "team_wins.csv"), index=False)
print(f"   ✅ team_wins.csv exported → {len(team_wins)} rows")

# ============================================================
# EXPORT 4: season summary (matches & runs per season)
# ============================================================

season_summary = pd.read_sql("""
    SELECT 
        m.season,
        COUNT(DISTINCT m.match_id) AS total_matches,
        SUM(d.total_runs) AS total_runs,
        AVG(d.total_runs) AS avg_runs_per_ball
    FROM matches m
    JOIN deliveries d ON m.match_id = d.match_id
    GROUP BY m.season
    ORDER BY m.season
""", engine)
season_summary.to_csv(os.path.join(EXPORT_DIR, "season_summary.csv"), index=False)
print(f"   ✅ season_summary.csv exported → {len(season_summary)} rows")

# ============================================================
# EXPORT 5: top batsmen (runs per player)
# ============================================================

top_batsmen = pd.read_sql("""
    SELECT 
        batsman,
        SUM(batsman_runs) AS total_runs,
        COUNT(*) AS balls_faced,
        ROUND(SUM(batsman_runs) / COUNT(*) * 100, 2) AS strike_rate
    FROM deliveries
    GROUP BY batsman
    ORDER BY total_runs DESC
    LIMIT 50
""", engine)
top_batsmen.to_csv(os.path.join(EXPORT_DIR, "top_batsmen.csv"), index=False)
print(f"   ✅ top_batsmen.csv exported → {len(top_batsmen)} rows")

# ============================================================
# EXPORT 6: top bowlers (wickets per player)
# ============================================================

top_bowlers = pd.read_sql("""
    SELECT 
        bowler,
        COUNT(*) AS total_wickets,
        COUNT(DISTINCT match_id) AS matches_played
    FROM deliveries
    WHERE is_wicket = 1
    GROUP BY bowler
    ORDER BY total_wickets DESC
    LIMIT 50
""", engine)
top_bowlers.to_csv(os.path.join(EXPORT_DIR, "top_bowlers.csv"), index=False)
print(f"   ✅ top_bowlers.csv exported → {len(top_bowlers)} rows")

# ============================================================
# EXPORT 7: toss analysis
# ============================================================

toss_analysis = pd.read_sql("""
    SELECT
        toss_decision,
        toss_match_winner,
        COUNT(*) AS matches
    FROM matches
    GROUP BY toss_decision, toss_match_winner
""", engine)
toss_analysis.to_csv(os.path.join(EXPORT_DIR, "toss_analysis.csv"), index=False)
print(f"   ✅ toss_analysis.csv exported → {len(toss_analysis)} rows")

# ============================================================
# EXPORT 8: venue analysis
# ============================================================

venue_analysis = pd.read_sql("""
    SELECT
        venue,
        city,
        COUNT(*) AS total_matches,
        SUM(CASE WHEN toss_decision = 'bat' THEN 1 ELSE 0 END) AS chose_bat,
        SUM(CASE WHEN toss_decision = 'field' THEN 1 ELSE 0 END) AS chose_field
    FROM matches
    GROUP BY venue, city
    ORDER BY total_matches DESC
""", engine)
venue_analysis.to_csv(os.path.join(EXPORT_DIR, "venue_analysis.csv"), index=False)
print(f"   ✅ venue_analysis.csv exported → {len(venue_analysis)} rows")

print("\n🎉 All exports complete!")
print(f"   Files saved in: sql/exports/")