-- Query 2: Price Tier Performance
-- Which price tiers have the best ratings and engagement?
SELECT
    price_tier,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(AVG(review_count), 0) AS avg_reviews,
    ROUND(AVG(engagement_score), 2) AS avg_engagement
FROM gaming_mice
GROUP BY price_tier
ORDER BY avg_price ASC;