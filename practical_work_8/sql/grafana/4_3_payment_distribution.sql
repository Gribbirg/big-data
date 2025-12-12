-- 4.3. Распределение способов оплаты (Pie Chart)
SELECT
    payment_type AS metric,
    COUNT(DISTINCT order_id)::numeric AS value
FROM order_payments
WHERE payment_type <> 'not_defined'
GROUP BY payment_type
ORDER BY value DESC;
