"""
Step 4: AI-Powered Insights using Anthropic API
Amazon Gaming Mice Competitive Intelligence
--------------------------------------------
This script:
1. Extracts structured features from product descriptions (DPI, sensor, battery, etc.)
2. Generates competitive summaries per price tier
3. Saves results to CSV files for Tableau and further analysis
"""

import anthropic
import pandas as pd
import json
import time

# ── 1. CONFIGURATION ──────────────────────────────────────────────────────────
API_KEY  = "****"  
CSV_FILE = "gaming_mice_clean.csv"

client = anthropic.Anthropic(api_key=API_KEY)


# ── 2. LOAD DATA ──────────────────────────────────────────────────────────────
print("📂 Loading clean data...")
df = pd.read_csv(CSV_FILE, encoding="latin-1")
print(f"   Records loaded: {len(df)}")


# ── 3. FEATURE EXTRACTION ─────────────────────────────────────────────────────
print("\n🤖 Extracting features from product descriptions...")
print("   (This may take a few minutes due to API rate limits)\n")

def extract_features(title, description):
    """Use Claude to extract structured features from a product title/description."""
    
    prompt = f"""You are a product data analyst. Extract key technical features from this gaming mouse product.

Product Title: {title}
Product Description: {description}

Extract the following features. If a feature is not mentioned, return null.
Respond ONLY with a JSON object, no other text or markdown:

{{
    "dpi_max": <maximum DPI as integer or null>,
    "is_gaming": <true if marketed as a gaming mouse, false if office/general use>,
    "form_factor": <"ergonomic", "ambidextrous", or "vertical" or null>,
    "key_selling_point": <single most emphasized selling point in 5 words or less>,
    "target_audience": <"gamer", "office worker", "traveler", or "general">
}}"""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        raw = message.content[0].text.strip()
        # Clean any accidental markdown
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    
    except Exception as e:
        print(f"   ⚠️  Error extracting features: {e}")
        return {
            "dpi_max": None,
            "is_gaming": None,
            "form_factor": None,
            "key_selling_point": None,
            "target_audience": None
        }


# Run feature extraction on all products
features_list = []

for i, row in df.iterrows():
    print(f"   Processing {i+1}/{len(df)}: {row['brand']} - {row['title'][:50]}...")
    
    features = extract_features(row["title"], row["description"])
    features["asin"] = row["asin"]
    features["brand"] = row["brand"]
    features["price"] = row["price"]
    features["price_tier"] = row["price_tier"]
    features["rating"] = row["rating"]
    features_list.append(features)
    
    # Small delay to avoid rate limiting
    time.sleep(0.5)

# Save features to CSV
features_df = pd.DataFrame(features_list)
features_df.to_csv("ai_features.csv", index=False)
print(f"\n✅ Features saved to ai_features.csv")


# ── 4. COMPETITIVE SUMMARIES BY PRICE TIER ────────────────────────────────────
print("\n📝 Generating competitive summaries by price tier...")

def generate_summary(price_tier, products):
    """Generate a competitive summary for a price tier."""
    
    # Build a product list string
    product_lines = []
    for _, p in products.iterrows():
        product_lines.append(
            f"- {p['brand']} | ${p['price']} | {p['rating']}★ | {p['review_count']:,} reviews | {p['title'][:80]}"
        )
    product_text = "\n".join(product_lines)
    
    prompt = f"""You are a competitive intelligence analyst specializing in consumer electronics.

Analyze these Amazon gaming mice in the {price_tier} price tier:

{product_text}

Write a 3-4 sentence competitive summary covering:
1. What brands dominate this tier and why
2. What features or selling points are most common
3. What a new brand would need to compete successfully here

Be specific and data-driven. Write in a professional business analyst tone."""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    
    except Exception as e:
        print(f"   ⚠️  Error generating summary: {e}")
        return "Summary unavailable."


# Generate summary for each price tier
summaries_list = []
price_tiers = df["price_tier"].unique()

for tier in price_tiers:
    print(f"   Generating summary for: {tier}...")
    tier_products = df[df["price_tier"] == tier]
    summary = generate_summary(tier, tier_products)
    
    summaries_list.append({
        "price_tier": tier,
        "product_count": len(tier_products),
        "avg_price": round(tier_products["price"].mean(), 2),
        "avg_rating": round(tier_products["rating"].mean(), 2),
        "competitive_summary": summary
    })
    
    time.sleep(1)

# Save summaries to CSV
summaries_df = pd.DataFrame(summaries_list)
summaries_df.to_csv("ai_summaries.csv", index=False)
print(f"\n✅ Summaries saved to ai_summaries.csv")


# ── 5. PRINT SUMMARY REPORT ───────────────────────────────────────────────────
print("\n" + "="*60)
print("✅ AI INSIGHTS COMPLETE")
print("="*60)
print(f"   Features extracted: {len(features_df)} products → ai_features.csv")
print(f"   Summaries generated: {len(summaries_df)} price tiers → ai_summaries.csv")
print("\n📊 Sample Competitive Summaries:")
print("-"*60)

for _, row in summaries_df.iterrows():
    print(f"\n{row['price_tier']} ({row['product_count']} products, avg ${row['avg_price']}):")
    print(row["competitive_summary"])
    print()
