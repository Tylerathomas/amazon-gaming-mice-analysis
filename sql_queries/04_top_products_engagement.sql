-- Query 4: Top 10 Products by Engagement Score
-- Which individual products have the strongest market presence?
SELECT
    brand,
    title,
    price,
    rating,
    review_count,
    engagement_score
FROM gaming_mice
ORDER BY engagement_score DESC
LIMIT 10;