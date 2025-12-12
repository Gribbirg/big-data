SELECT
    oi.seller_id,
    COUNT(DISTINCT oi.order_id) AS unique_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    COUNT(*) AS total_items,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    ROUND(AVG(oi.freight_value), 2) AS avg_freight_per_item
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
WHERE oi.seller_id IS NOT NULL
GROUP BY oi.seller_id
ORDER BY unique_orders DESC
LIMIT 10;
