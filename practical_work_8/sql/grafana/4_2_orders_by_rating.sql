-- 4.2. Количество заказов по оценкам
SELECT
    review_score::text AS score,
    COUNT(order_id) AS order_count
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;
