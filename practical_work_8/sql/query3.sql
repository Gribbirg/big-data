WITH delivery_data AS (
    SELECT
        o.order_id,
        r.review_score,
        EXTRACT(DAY FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) AS delivery_days
    FROM orders o
    JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_delivered_customer_date IS NOT NULL
        AND o.order_purchase_timestamp IS NOT NULL
)
SELECT
    CASE
        WHEN delivery_days <= 5 THEN 'До 5 дней включительно'
        WHEN delivery_days BETWEEN 6 AND 10 THEN 'От 6 до 10 дней включительно'
        ELSE 'Более 10 дней'
    END AS delivery_interval,
    COUNT(order_id) AS order_count,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM delivery_data
GROUP BY
    CASE
        WHEN delivery_days <= 5 THEN 'До 5 дней включительно'
        WHEN delivery_days BETWEEN 6 AND 10 THEN 'От 6 до 10 дней включительно'
        ELSE 'Более 10 дней'
    END
ORDER BY
    MIN(CASE
        WHEN delivery_days <= 5 THEN 1
        WHEN delivery_days BETWEEN 6 AND 10 THEN 2
        ELSE 3
    END);
