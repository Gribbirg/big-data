SELECT
    payment_type,
    COUNT(*) AS payment_count,
    ROUND(AVG(payment_installments), 2) AS avg_installments,
    ROUND(AVG(payment_value), 2) AS avg_payment_value,
    ROUND(
        COUNT(DISTINCT order_id)::decimal /
        (SELECT COUNT(DISTINCT order_id) FROM order_payments) * 100,
        2
    ) AS order_share_percent
FROM order_payments
GROUP BY payment_type
ORDER BY payment_count DESC;
