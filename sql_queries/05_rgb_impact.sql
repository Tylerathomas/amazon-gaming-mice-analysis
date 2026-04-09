-- Query 5: RGB Impact on Ratings
-- Does RGB lighting affect ratings or engagement?
SELECT
    CASE WHEN has_rgb = 1 THEN 'Has RGB' ELSE 'No RGB' END AS rgb_status,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(AVG(review_count), 0) AS avg_reviews,
    ROUND(AVG(engagement_score), 2) AS avg_engagement
FROM gaming_mice
GROUP BY has_rgb;