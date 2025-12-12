-- 4.1. Динамика числа заказов по месяцам
SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS time,
    COUNT(DISTINCT order_id) AS order_count
FROM orders
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY time
ORDER BY time;
