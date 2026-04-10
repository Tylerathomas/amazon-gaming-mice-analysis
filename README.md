# Amazon Gaming Mice — Competitive Intelligence Pipeline

An end-to-end data analytics pipeline that scrapes Amazon gaming mouse listings, cleans and analyzes the data with Python and SQL, uses AI (Anthropic API) to extract structured product insights, and visualizes findings in Tableau.

**Central Business Question:** *What does it take to win at each price tier?*

---

## Key Findings

- **Budget-tier mice dominate** in review volume — consumers gravitate toward cheap options or go premium, skipping the middle
- **The $40–$69 mid-range is a "dead zone"** with the lowest engagement of any tier
- **Ratings are flat across all tiers** (~4.3–4.5) — stars alone don't separate winners from losers
- **Brand equity overrides price sensitivity** at the premium tier — Logitech G outperforms Razer in reviews despite higher avg price
- **Logitech/Logitech G control ~40% of the market** with 22 of 56 products in the dataset

---

## Pipeline Architecture

| Stage | Tool | Script | Output |
|-------|------|--------|--------|
| 1. Data Collection | Apify | *(cloud scraper)* | `data/raw/dataset_Amazon-crawler_*.json` |
| 2. Data Cleaning & ETL | Python (Pandas) | `scripts/clean_gaming_mice.py` | `data/clean/fixed_gaming_mice_clean.csv` |
| 2b. Database Load | Python (psycopg2) | `scripts/load_to_postgres.py` | PostgreSQL `gaming_mice` table |
| 3. SQL Analysis | PostgreSQL | `sql_queries/01–06_*.sql` | Query results + `Insights.txt` |
| 4. AI Insights | Anthropic API (Claude) | `scripts/ai_insights.py` | `data/ai_outputs/ai_features.csv`, `ai_summaries.csv` |
| 5. Visualization | Tableau Public | — | [Dashboard Link](https://public.tableau.com/app/profile/tyler.thomas5812/viz/AmazonMice/Whatittakestowinateachpricetier-AmazonMiceAnalysis) |

---

## Project Structure

```
amazon-gaming-mice-analysis/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   │   └── dataset_Amazon-crawler_2026-03-11_00-45-20-912.json
│   ├── clean/
│   │   ├── fixed_gaming_mice_clean.csv   # Final clean dataset (56 products)
│   │   └── gaming_mice_clean.csv         # Earlier version (70 products, before exclusion filters)
│   └── ai_outputs/
│       ├── ai_features.csv
│       └── ai_summaries.csv
├── scripts/
│   ├── clean_gaming_mice.py              # V1 ETL: JSON → clean CSV
│   ├── new_clean_gaming_mice.py          # V2 ETL: added exclusion filters (keyboard combos, jigglers, etc.)
│   ├── load_to_postgres.py              # Load CSV into PostgreSQL
│   └── ai_insights.py                   # Anthropic API feature extraction & summaries
├── sql_queries/
│   ├── 01_brand_dominance.sql
│   ├── 02_price_tier_performance.sql
│   ├── 03_wireless_vs_wired.sql
│   ├── 04_top_products_engagement.sql
│   ├── 05_rgb_impact.sql
│   ├── 06_brand_positioning.sql
│   └── Insights.txt
└── docs/
    └── Screenshot_2026-03-11_181723.png
```

> **Why two cleaning scripts?** The first version (`clean_gaming_mice.py`) produced 70 products but included non-gaming items like mouse jigglers and keyboard combos. The second version (`new_clean_gaming_mice.py`) added exclusion filters and brought the dataset down to 56 true gaming mice. Both are included intentionally to show iterative problem-solving.

---

## How to Reproduce

### Prerequisites
- Python 3.8+
- PostgreSQL installed locally
- Apify account (free tier works)
- Anthropic API key

### 1. Scrape Data
Use the **"Free Amazon Product Scraper" by junglee** on [Apify](https://apify.com). Search for gaming mice, export as JSON, and save to `data/raw/`.

### 2. Clean & Transform
```bash
pip install -r requirements.txt
cd scripts
python new_clean_gaming_mice.py
```
Reads the raw JSON, filters to gaming mice only, engineers features (price tiers, rating buckets, engagement score), and outputs the clean CSV.

### 3. Load into PostgreSQL
```bash
# Create a database called "gaming_mice" in pgAdmin first
python load_to_postgres.py
```

### 4. Run SQL Analysis
Open the `.sql` files in pgAdmin and run them against the `gaming_mice` database. Each query is self-contained. Key findings are summarized in `sql_queries/Insights.txt`.

### 5. Generate AI Insights
```bash
export ANTHROPIC_API_KEY="your-key-here"
python ai_insights.py
```
Extracts structured features (DPI, form factor, target audience) and generates competitive summaries per price tier using Claude Haiku.

### 6. Tableau Dashboard
Import `fixed_gaming_mice_clean.csv` into Tableau Public and build the dashboard, or view the published version linked below.

---

## Tableau Dashboard

> [View the Dashboard on Tableau Public](https://public.tableau.com/views/AmazonMice/Whatittakestowinateachpricetier-AmazonMiceAnalysis?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

The dashboard answers **"What does it take to win at each price tier?"** through four charts:
1. **Competitive Landscape** — Product count by price tier
2. **Review Volume by Tier** — Budget mice dominate; mid-range is the dead zone
3. **Price vs. Engagement** — Scatter plot showing inverse relationship
4. **Brand Market Share** — Treemap showing Logitech/Logitech G dominance

---

## Tech Stack

- **Scraping:** Apify (Free Amazon Product Scraper)
- **ETL:** Python 3, Pandas, NumPy
- **Database:** PostgreSQL, psycopg2
- **AI/NLP:** Anthropic API (Claude Haiku)
- **Visualization:** Tableau Public

---

## Dataset Summary

| Metric | Value |
|--------|-------|
| Total products (after cleaning) | 56 |
| Unique brands | 28 |
| Price range | $4.99 – $159.99 |
| Avg rating | 4.43 ⭐ |
| Wireless products | 69% |
| Price tiers | Budget, Entry, Mid-Range, Premium, Ultra-Premium |

---

## License

This project is for portfolio/educational purposes. Amazon product data was scraped in compliance with Apify's terms of service.
