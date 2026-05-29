# ============================================================
#   IPL ETL PIPELINE
#   Extract → Transform → Load
# ============================================================

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import os

# ============================================================
# SECTION 1: EXTRACT
# Reading raw CSV files into Python
# Like opening Excel files but inside Python
# ============================================================

print("📥 Extracting data...")

# This finds the project root folder automatically
# No matter where you run the file from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

matches = pd.read_csv(os.path.join(BASE_DIR, "data", "matches.csv"))
deliveries = pd.read_csv(os.path.join(BASE_DIR, "data", "deliveries.csv"))

print(f"   matches.csv    → {matches.shape[0]} rows, {matches.shape[1]} columns")
print(f"   deliveries.csv → {deliveries.shape[0]} rows, {deliveries.shape[1]} columns")


# ============================================================
# SECTION 2: TRANSFORM — MATCHES
# Cleaning and fixing the matches data
# ============================================================

print("\n🔄 Transforming matches data...")

# umpire3 is fully empty → useless, drop it
# dl_applied = rain rule column → not needed for our analysis
matches.drop(columns=["umpire3", "dl_applied"], inplace=True)
print("   ✅ Dropped umpire3 and dl_applied")

# 'id' is too vague → rename to 'match_id' for clarity
matches.rename(columns={"id": "match_id"}, inplace=True)
print("   ✅ Renamed 'id' to 'match_id'")

# Convert date from plain text → real date format
# So we can later sort and filter by date properly
matches["date"] = pd.to_datetime(matches["date"])
print("   ✅ Converted date column to datetime")

# Fill missing values with meaningful labels
matches["city"] = matches["city"].fillna("Unknown")
matches["winner"] = matches["winner"].fillna("No Result")
matches["player_of_match"] = matches["player_of_match"].fillna("N/A")
print("   ✅ Filled missing values")

# Some teams changed names over the years in the data
# We standardize them so analysis stays consistent
team_name_fixes = {
    "Rising Pune Supergiant": "Rising Pune Supergiants",
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
}
for col in ["team1", "team2", "toss_winner", "winner"]:
    matches[col] = matches[col].replace(team_name_fixes)
print("   ✅ Standardized team names")

# New column: did the toss winner also win the match?
# 1 = Yes, 0 = No
# Useful for toss impact analysis later
matches["toss_match_winner"] = np.where(
    matches["toss_winner"] == matches["winner"], 1, 0
)
print("   ✅ Added toss_match_winner column")

print(f"\n   matches final shape: {matches.shape}")


# ============================================================
# SECTION 3: TRANSFORM — DELIVERIES
# Cleaning the ball-by-ball data
# ============================================================

print("\n🔄 Transforming deliveries data...")

# When no wicket falls, these columns are empty
# Fill with 'None' so database doesn't have blank cells
deliveries["player_dismissed"] = deliveries["player_dismissed"].fillna("None")
deliveries["dismissal_kind"] = deliveries["dismissal_kind"].fillna("None")
deliveries["fielder"] = deliveries["fielder"].fillna("None")
print("   ✅ Filled missing dismissal columns")

# New column: did a wicket fall on this ball?
# 1 = yes a wicket fell, 0 = no wicket
deliveries["is_wicket"] = np.where(
    deliveries["player_dismissed"] != "None", 1, 0
)
print("   ✅ Added is_wicket column")

# Super overs are tie-breakers, not regular match play
# We remove them to keep analysis clean
deliveries = deliveries[deliveries["is_super_over"] == 0]
deliveries = deliveries.drop(columns=["is_super_over"])
print("   ✅ Removed super over deliveries")

print(f"\n   deliveries final shape: {deliveries.shape}")


# ============================================================
# SECTION 4: LOAD — Push cleaned data into MySQL
# ============================================================

print("\n📤 Loading into MySQL...")

# This is your MySQL connection string
# FORMAT: mysql+pymysql://username:password@host/database_name
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

DB_USER = "root"
DB_PASSWORD = "Stock@123"   # ← put your password here
DB_HOST = "127.0.0.1"                  # ← use IP instead of 'localhost'
DB_NAME = "ipl_db"

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,      # SQLAlchemy handles special characters safely
    host=DB_HOST,
    database=DB_NAME,
    port=3306
)

engine = create_engine(connection_url)

# Load matches table into MySQL
# if_exists="replace" → if table already exists, recreate it fresh
# index=False → don't write pandas row numbers as a column
matches.to_sql("matches", con=engine, if_exists="replace", index=False)
print("   ✅ 'matches' table created in MySQL")

# chunksize=1000 → inserts 1000 rows at a time (faster for big data)
deliveries.to_sql("deliveries", con=engine, if_exists="replace", index=False, chunksize=1000)
print("   ✅ 'deliveries' table created in MySQL")

print("\n🎉 ETL Pipeline Complete!")
print("   MySQL now has 2 tables → matches + deliveries")