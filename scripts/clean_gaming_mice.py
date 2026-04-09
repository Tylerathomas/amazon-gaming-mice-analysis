"""
Step 2: Data Cleaning & ETL Pipeline
Amazon Gaming Mice Competitive Intelligence
--------------------------------------------
This script:
1. Loads raw JSON scraped from Amazon via Apify
2. Flattens nested fields (price)
3. Filters to gaming mice only
4. Cleans and standardizes data
5. Engineers new features (price tiers, rating buckets, engagement score)
6. Exports a clean CSV for SQL analysis and Tableau
"""

import json
import pandas as pd
import numpy as np
import re
import os

# ── 1. LOAD RAW DATA ──────────────────────────────────────────────────────────
print("📂 Loading raw data...")

# Update this path if your file is in a different location
RAW_FILE = "dataset_Amazon-crawler_2026-03-11_00-45-20-912.json"

with open(RAW_FILE, "r", encoding="latin-1") as f:
    data = json.load(f)

df_raw = pd.DataFrame(data)
print(f"   Raw records loaded: {len(df_raw)}")


# ── 2. FLATTEN NESTED FIELDS ──────────────────────────────────────────────────
print("\n🔧 Flattening nested fields...")

# Price is a dict: {"value": 29.99, "currency": "$"}
df_raw["price_usd"] = df_raw["price"].apply(
    lambda x: x["value"] if isinstance(x, dict) and "value" in x else np.nan
)

# Drop original nested price column
df = df_raw.drop(columns=["price", "thumbnailImage"], errors="ignore")


# ── 3. FILTER TO GAMING MICE ONLY ─────────────────────────────────────────────
print("\n🖱️  Filtering to gaming mice only...")

# Filter by title containing mouse/mice
mice_title = df["title"].str.contains(r"mouse|mice", case=False, na=False)

# Filter by category path containing Mice (excludes pads, cables, keyboards, etc.)
mice_category = df["breadCrumbs"].str.contains(r"Mice", case=False, na=False)

# Both conditions must be true
df = df[mice_title & mice_category].copy()
print(f"   Records after filtering: {len(df)}")


# ── 4. CLEAN & STANDARDIZE ────────────────────────────────────────────────────
print("\n🧹 Cleaning data...")

# Remove duplicates
before = len(df)
df = df.drop_duplicates(subset=["asin"])
print(f"   Duplicates removed: {before - len(df)}")

# Standardize column names
df = df.rename(columns={
    "reviewsCount": "review_count",
    "price_usd":    "price",
    "stars":        "rating",
    "breadCrumbs":  "category_path",
})

# Clean brand: strip whitespace, title case
df["brand"] = df["brand"].str.strip().str.title()

# Clean title
df["title"] = df["title"].str.strip()

# Ensure correct types
df["price"]        = pd.to_numeric(df["price"], errors="coerce")
df["rating"]       = pd.to_numeric(df["rating"], errors="coerce")
df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")

# Handle missing values
df["price"]        = df["price"].fillna(df["price"].median())
df["rating"]       = df["rating"].fillna(df["rating"].median())
df["review_count"] = df["review_count"].fillna(0).astype(int)
df["brand"]        = df["brand"].fillna("Unknown")
df["description"]  = df["description"].fillna("")

print(f"   Missing values handled.")


# ── 5. FEATURE ENGINEERING ────────────────────────────────────────────────────
print("\n⚙️  Engineering new features...")

# Price tiers
def price_tier(price):
    if price < 20:
        return "Budget (<$20)"
    elif price < 40:
        return "Entry ($20–$39)"
    elif price < 70:
        return "Mid-Range ($40–$69)"
    elif price < 100:
        return "Premium ($70–$99)"
    else:
        return "Ultra-Premium ($100+)"

df["price_tier"] = df["price"].apply(price_tier)

# Rating buckets
def rating_bucket(r):
    if r >= 4.5:
        return "Excellent (4.5+)"
    elif r >= 4.0:
        return "Good (4.0–4.4)"
    elif r >= 3.5:
        return "Average (3.5–3.9)"
    else:
        return "Below Average (<3.5)"

df["rating_bucket"] = df["rating"].apply(rating_bucket)

# Engagement score: proxy for product momentum
# High ratings AND high review counts = strong market presence
df["engagement_score"] = round(df["rating"] * np.log1p(df["review_count"]), 2)

# Is it wireless? (from title)
df["is_wireless"] = df["title"].str.contains(
    r"wireless|bluetooth|lightspeed|wifi", case=False, na=False
).astype(int)

# Is RGB mentioned?
df["has_rgb"] = df["title"].str.contains(
    r"rgb|lighting|chroma|lightsync", case=False, na=False
).astype(int)

print(f"   Features created: price_tier, rating_bucket, engagement_score, is_wireless, has_rgb")


# ── 6. FINAL COLUMN SELECTION & ORDER ─────────────────────────────────────────
final_columns = [
    "asin", "title", "brand", "price", "price_tier",
    "rating", "rating_bucket", "review_count", "engagement_score",
    "is_wireless", "has_rgb", "description", "category_path", "url"
]

df = df[final_columns].reset_index(drop=True)


# ── 7. EXPORT CLEAN CSV ───────────────────────────────────────────────────────
print("\n💾 Exporting clean CSV...")

OUTPUT_FILE = "gaming_mice_clean.csv"
df.to_csv(OUTPUT_FILE, index=False)
print(f"   Saved: {OUTPUT_FILE}")


# ── 8. SUMMARY REPORT ─────────────────────────────────────────────────────────
print("\n" + "="*50)
print("✅ CLEANING COMPLETE — SUMMARY")
print("="*50)
print(f"Total products:        {len(df)}")
print(f"Unique brands:         {df['brand'].nunique()}")
print(f"Price range:           ${df['price'].min():.2f} – ${df['price'].max():.2f}")
print(f"Avg price:             ${df['price'].mean():.2f}")
print(f"Avg rating:            {df['rating'].mean():.2f} ⭐")
print(f"Avg review count:      {int(df['review_count'].mean()):,}")
print(f"Wireless products:     {df['is_wireless'].sum()} ({df['is_wireless'].mean()*100:.0f}%)")
print(f"RGB products:          {df['has_rgb'].sum()} ({df['has_rgb'].mean()*100:.0f}%)")
print("\nPrice tier breakdown:")
print(df["price_tier"].value_counts().to_string())
print("\nRating bucket breakdown:")
print(df["rating_bucket"].value_counts().to_string())
print("\nTop 10 brands by product count:")
print(df["brand"].value_counts().head(10).to_string())