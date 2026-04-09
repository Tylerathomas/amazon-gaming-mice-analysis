-- Query 3: Wireless vs Wired Performance
-- Do wireless mice rate higher and get more reviews?
SELECT
    CASE WHEN is_wireless = 1 THEN 'Wireless' ELSE 'Wired' END AS connectivity,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(AVG(review_count), 0) AS avg_reviews,
    ROUND(AVG(engagement_score), 2) AS avg_engagement
FROM gaming_mice
GROUP BY is_wireless;