-- 4.4. Топ-10 категорий по объему продаж
SELECT
    pcnt.product_category_name_english AS category,
    SUM(oi.price) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation pcnt
    ON p.product_category_name = pcnt.product_category_name
WHERE p.product_category_name IS NOT NULL
GROUP BY pcnt.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;
