-- 4.5.2. Динамика средней стоимости заказа
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS time,
    ROUND(AVG(oi.price), 2) AS avg_order_value,
    COUNT(DISTINCT o.order_id) AS order_count
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_purchase_timestamp IS NOT NULL
GROUP BY time
ORDER BY time;
