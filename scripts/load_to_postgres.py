"""
Step 2b: Load Clean Data into PostgreSQL
Amazon Gaming Mice Competitive Intelligence
--------------------------------------------
This script:
1. Connects to your local PostgreSQL database
2. Creates the gaming_mice table
3. Loads the clean CSV into the table
"""

import pandas as pd
import psycopg2
from psycopg2 import sql

# ── 1. CONFIGURATION ──────────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "database": "gaming_mice",
    "user":     "postgres",
    "password": "password"  # ← Replace with your PostgreSQL password
}

CSV_FILE = "fixed_gaming_mice_clean.csv"


# ── 2. LOAD CSV ───────────────────────────────────────────────────────────────
print("📂 Loading clean CSV...")
df = pd.read_csv(CSV_FILE, encoding="latin-1")
print(f"   Records to load: {len(df)}")


# ── 3. CONNECT TO POSTGRESQL ──────────────────────────────────────────────────
print("\n🔌 Connecting to PostgreSQL...")
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()
print("   Connected successfully!")


# ── 4. CREATE TABLE ───────────────────────────────────────────────────────────
print("\n🏗️  Creating table...")

cur.execute("DROP TABLE IF EXISTS gaming_mice;")

cur.execute("""
    CREATE TABLE gaming_mice (
        asin            VARCHAR(20) PRIMARY KEY,
        title           TEXT,
        brand           VARCHAR(100),
        price           NUMERIC(10, 2),
        price_tier      VARCHAR(50),
        rating          NUMERIC(3, 1),
        rating_bucket   VARCHAR(50),
        review_count    INTEGER,
        engagement_score NUMERIC(10, 2),
        is_wireless     SMALLINT,
        has_rgb         SMALLINT,
        description     TEXT,
        category_path   TEXT,
        url             TEXT
    );
""")

print("   Table created!")


# ── 5. INSERT DATA ────────────────────────────────────────────────────────────
print("\n📥 Inserting records...")

inserted = 0
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO gaming_mice (
            asin, title, brand, price, price_tier,
            rating, rating_bucket, review_count, engagement_score,
            is_wireless, has_rgb, description, category_path, url
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (asin) DO NOTHING;
    """, (
        row["asin"], row["title"], row["brand"], row["price"], row["price_tier"],
        row["rating"], row["rating_bucket"], row["review_count"], row["engagement_score"],
        row["is_wireless"], row["has_rgb"], row["description"], row["category_path"], row["url"]
    ))
    inserted += 1

conn.commit()
print(f"   Inserted {inserted} records!")


# ── 6. VERIFY ─────────────────────────────────────────────────────────────────
print("\n✅ Verifying load...")
cur.execute("SELECT COUNT(*) FROM gaming_mice;")
count = cur.fetchone()[0]
print(f"   Rows in database: {count}")

cur.execute("SELECT brand, price, rating FROM gaming_mice LIMIT 5;")
rows = cur.fetchall()
print("\n   Sample rows:")
for row in rows:
    print(f"   {row}")


# ── 7. CLOSE CONNECTION ───────────────────────────────────────────────────────
cur.close()
conn.close()
print("\n🔒 Connection closed. Ready for SQL analysis!")
