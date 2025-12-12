# Практическая работа №8 - SQL Запросы

## 3.1. ТОП-10 категорий по выручке, с переводом (0.5 балла)

**Задача:** Определить десять товарных категорий с наибольшим оборотом продаж. Для каждой категории требуется посчитать сумму цен всех проданных позиций (выручка/GMV категории), количество уникальных заказов, в которых встречались товары этой категории, и общее число товарных позиций. Дополнительно к исходному названию категории нужно вывести её англоязычный перевод из словаря переводов.

### SQL Запрос:

```sql
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
```

### Результат:

| **category_name** | **category_name_english** | **total_revenue** | **unique_orders** | **total_items** |
|---|---|---|---|---|
| beleza_saude | health_beauty | 1258681.34 | 8836 | 9670 |
| relogios_presentes | watches_gifts | 1205005.68 | 5624 | 5991 |
| cama_mesa_banho | bed_bath_table | 1036988.68 | 9417 | 11115 |
| esporte_lazer | sports_leisure | 988048.97 | 7720 | 8641 |
| informatica_acessorios | computers_accessories | 911954.32 | 6689 | 7827 |
| moveis_decoracao | furniture_decor | 729762.49 | 6449 | 8334 |
| cool_stuff | cool_stuff | 635290.85 | 3632 | 3796 |
| utilidades_domesticas | housewares | 632248.66 | 5884 | 6964 |
| automotivo | auto | 592720.11 | 3897 | 4235 |
| ferramentas_jardim | garden_tools | 485256.46 | 3518 | 4347 |

---

## 3.2. Платежное поведение (0.5 балла)

**Задача:** Сравнить используемые способы оплаты. По каждому типу оплаты требуется вывести количество зарегистрированных платежей, среднее число рассрочек (если применимо), средний размер платежа и долю заказов, в которых встречается данный способ оплаты.

### SQL Запрос:

```sql
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
```

### Результат:

| **payment_type** | **payment_count** | **avg_installments** | **avg_payment_value** | **order_share_percent** |
|---|---|---|---|---|
| credit_card | 76795 | 3.51 | 163.32 | 76.94 |
| boleto | 19784 | 1.00 | 145.03 | 19.90 |
| voucher | 5775 | 1.00 | 65.70 | 3.89 |
| debit_card | 1529 | 1.00 | 142.57 | 1.54 |
| not_defined | 3 | 1.00 | 0.00 | 0.00 |

---

## 3.3. Зависимость оценки от скорости доставки (0.5 балла)

**Задача:** Изучить, как длительность доставки коррелирует с оценками в отзывах. Для каждого заказа с отзывом и известной фактической датой доставки рассчитывается длительность доставки в днях. Каждый заказ попадает в один из трёх интервалов: до пяти дней включительно, от шести до десяти дней включительно, более десяти дней.

### SQL Запрос:

```sql
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
```

### Результат:

| **delivery_interval** | **order_count** | **avg_review_score** |
|---|---|---|
| До 5 дней включительно | 19008 | 4.43 |
| От 6 до 10 дней включительно | 32408 | 4.35 |
| Более 10 дней | 43451 | 3.90 |

---

## 3.4. Эффективность продавцов (0.5 балла)

**Задача:** Получить рейтинг продавцов по активности и базовым бизнес-показателям. Для каждого продавца считается количество уникальных заказов, число уникальных клиентов, общее число проданных товарных позиций, совокупный оборот по этим позициям и средняя стоимость доставки на позицию. Топ-10 продавцов, отсортированный по числу заказов по убыванию.

### SQL Запрос:

```sql
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
```

### Результат:

| **seller_id** | **unique_orders** | **unique_customers** | **total_items** | **total_revenue** | **avg_freight_per_item** |
|---|---|---|---|---|---|
| 6560211a19b47992c3666cc44a7e94c0 | 1854 | 1854 | 2033 | 123304.83 | 13.75 |
| 4a3ca9315b744ce9f8e9374361493884 | 1806 | 1806 | 1987 | 200472.92 | 17.65 |
| cc419e0650a3c5ba77189a1882b7556a | 1706 | 1706 | 1775 | 104288.42 | 14.46 |
| 1f50f920176fa81dab994f9023523100 | 1404 | 1404 | 1931 | 106939.21 | 18.21 |
| da8622b14eb17ae2831f4ac5b9dab84a | 1314 | 1314 | 1551 | 160236.57 | 16.09 |
| 955fee9216a65b617aa5c0531780ce60 | 1287 | 1287 | 1499 | 135171.70 | 16.97 |
| 7a67c85e85bb2ce8582c35f2203ad736 | 1160 | 1160 | 1171 | 141745.53 | 17.85 |
| ea8482cd71df3c1969d7b9473ff13abc | 1146 | 1146 | 1203 | 37177.52 | 14.58 |
| 4869f7a5dfa277a7dca6462dcf3b52b2 | 1132 | 1132 | 1156 | 229472.63 | 17.45 |
| 3d871de0142ce09b7081e2b9d1733cb1 | 1080 | 1080 | 1147 | 94914.20 | 19.56 |
