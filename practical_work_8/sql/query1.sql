SELECT
    p.product_category_name AS category_name,
    pcnt.product_category_name_english AS category_name_english,
    SUM(oi.price) AS total_revenue,
    COUNT(DISTINCT oi.order_id) AS unique_orders,
    COUNT(*) AS total_items
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation pcnt
    ON p.product_category_name = pcnt.product_category_name
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name, pcnt.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;
