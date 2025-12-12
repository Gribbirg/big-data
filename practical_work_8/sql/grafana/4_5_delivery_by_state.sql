-- 4.5.1. Статистика доставки по штатам
SELECT
    c.customer_state AS state,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(AVG(EXTRACT(DAY FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))::numeric), 1) AS avg_delivery_days,
    ROUND(AVG(r.review_score)::numeric, 2) AS avg_rating
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_delivered_customer_date IS NOT NULL
    AND o.order_purchase_timestamp IS NOT NULL
GROUP BY c.customer_state
ORDER BY order_count DESC
LIMIT 15;
