-- Query 6: Brand Positioning Map
-- Where does each brand sit in price vs rating space?
SELECT
    brand,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(AVG(engagement_score), 2) AS avg_engagement,
    SUM(review_count) AS total_reviews
FROM gaming_mice
GROUP BY brand
HAVING COUNT(*) >= 2
ORDER BY avg_price DESC;