-- Query 1: Brand Dominance
-- Which brands have the most products and highest avg rating?
SELECT 
    brand,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(rating), 2) AS avg_rating,
    SUM(review_count) AS total_reviews
FROM gaming_mice
GROUP BY brand
ORDER BY product_count DESC;