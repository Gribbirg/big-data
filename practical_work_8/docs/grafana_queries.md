# Grafana Dashboard - SQL Запросы для визуализаций

> **Note:** Load configuration for access:
> ```bash
> source practical_work_8/secrets/config.env
> ```

## Доступ к Grafana

**URL:** `$GRAFANA_URL`
**Login:** `$GRAFANA_USERNAME`
**Password:** `$GRAFANA_PASSWORD`

---

## 4.1. Динамика числа заказов по месяцам (линейный график)

**Тип визуализации:** Time series (линейный график)

### SQL Запрос:

```sql
SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS time,
    COUNT(DISTINCT order_id) AS order_count
FROM orders
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY time
ORDER BY time;
```

### Настройки в Grafana:
1. **Query:**
   - Format: Time series
   - Column `time` должен быть типа Timestamp
   - Column `order_count` - Numeric
2. **Visualization:** Time series
3. **Panel options:**
   - Title: "Динамика числа заказов по месяцам"
   - Description: "Временной ряд, показывающий рост или падения количества заказов"

### Выводы:
- Видна сезонность и тренд роста/падения заказов
- Пиковые месяцы продаж
- Общая динамика бизнеса

---

## 4.2. Количество заказов по оценкам (столбчатая диаграмма)

**Тип визуализации:** Bar chart (вертикальные столбцы)

### SQL Запрос:

```sql
SELECT
    review_score::text AS score,
    COUNT(order_id) AS order_count
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;
```

### Настройки в Grafana:
1. **Query:**
   - Format: Table
   - Преобразовать review_score в текст для категориальной оси
2. **Visualization:** Bar chart
3. **Panel options:**
   - Title: "Распределение заказов по оценкам"
   - X-axis: score (категориальная)
   - Y-axis: order_count
4. **Bar chart options:**
   - Orientation: Vertical
   - Show values: On

### Выводы:
- Распределение удовлетворенности клиентов
- Процент негативных/позитивных отзывов
- Качество сервиса

---

## 4.3. Распределение способов оплаты (круговая диаграмма)

**Тип визуализации:** Pie chart

### SQL Запрос:

```sql
SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS order_count
FROM order_payments
WHERE payment_type != 'not_defined'
GROUP BY payment_type
ORDER BY order_count DESC;
```

### Настройки в Grafana:
1. **Query:**
   - Format: Table
2. **Visualization:** Pie chart
3. **Panel options:**
   - Title: "Распределение способов оплаты"
   - Legend: Show percentages
4. **Pie chart options:**
   - Display labels: Name and percent
   - Legend placement: Right

### Выводы:
- Кредитные карты - доминирующий способ оплаты
- Разнообразие платежных методов
- Предпочтения клиентов

---

## 4.4. Топ-10 категорий по объему продаж (горизонтальные столбцы)

**Тип визуализации:** Bar chart (горизонтальные столбцы)

### SQL Запрос:

```sql
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
```

### Настройки в Grafana:
1. **Query:**
   - Format: Table
2. **Visualization:** Bar chart
3. **Panel options:**
   - Title: "ТОП-10 категорий по выручке"
4. **Bar chart options:**
   - Orientation: Horizontal
   - Show values: On
   - Sort: Descending

### Выводы:
- Самые прибыльные категории товаров
- Приоритеты для закупок и маркетинга
- Структура ассортимента

---

## 4.5. Дополнительная визуализация 1: Среднее время доставки по штатам (карта/таблица)

**Тип визуализации:** Table

### SQL Запрос:

```sql
SELECT
    c.customer_state AS state,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(AVG(EXTRACT(DAY FROM (o.order_delivered_customer_date - o.order_purchase_timestamp))), 1) AS avg_delivery_days,
    ROUND(AVG(r.review_score), 2) AS avg_rating
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_delivered_customer_date IS NOT NULL
    AND o.order_purchase_timestamp IS NOT NULL
GROUP BY c.customer_state
ORDER BY order_count DESC
LIMIT 15;
```

### Настройки в Grafana:
1. **Visualization:** Table
2. **Panel options:**
   - Title: "Статистика доставки по штатам"
3. **Table options:**
   - Show header: Yes
   - Column alignment: Auto

### Выводы:
- География заказов
- Влияние региона на скорость доставки
- Региональная удовлетворенность

---

## 4.5. Дополнительная визуализация 2: Динамика средней стоимости заказа

**Тип визуализации:** Time series (area chart)

### SQL Запрос:

```sql
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS time,
    ROUND(AVG(oi.price), 2) AS avg_order_value,
    COUNT(DISTINCT o.order_id) AS order_count
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_purchase_timestamp IS NOT NULL
GROUP BY time
ORDER BY time;
```

### Настройки в Grafana:
1. **Query:**
   - Format: Time series
2. **Visualization:** Time series
3. **Panel options:**
   - Title: "Средняя стоимость заказа по месяцам"
4. **Graph styles:**
   - Line interpolation: Smooth
   - Fill opacity: 30%
   - Show points: Auto

### Выводы:
- Изменение среднего чека
- Влияние маркетинговых акций
- Тренды потребительского поведения

---

## Инструкция по созданию дашборда

### 1. Создать новый дашборд
1. Dashboards → New dashboard
2. Add visualization
3. Выбрать источник: **Ecom-ADPG** (или ваш PostgreSQL data source)

### 2. Добавить панель
1. В Query editor переключиться на **Code** (не Builder)
2. Вставить SQL запрос
3. Выбрать тип визуализации справа
4. Настроить параметры панели
5. Нажать **Apply**

### 3. Расположить панели
1. Drag & drop для изменения размера и положения
2. Рекомендуемая раскладка:
   - Верх: 2 больших графика (4.1 и 4.5.2)
   - Середина: 3 средних (4.2, 4.3, 4.4)
   - Низ: таблица (4.5.1)

### 4. Сохранить дашборд
1. Save dashboard (иконка дискеты)
2. Название: "Ecommerce Analytics"
3. Folder: General
4. Save

### 5. Экспорт дашборда
1. Share dashboard → Export → Save to file
2. Сохранить как `ecommerce_dashboard.json`

---

## Команды для проверки запросов локально

```bash
# Подключение к БД
ssh $SSH_USER@$VM_PUBLIC_IP "sudo docker exec -it adcm-db psql -U $POSTGRES_USER -d $POSTGRES_DB"

# Или через файл
ssh $SSH_USER@$VM_PUBLIC_IP "cat /tmp/query.sql | sudo docker exec -i adcm-db psql -U $POSTGRES_USER -d $POSTGRES_DB"
```

---

## Скриншоты для отчета

Для каждой визуализации нужно сделать:
1. Скриншот графика/диаграммы
2. Краткий текстовый вывод (3-5 предложений)

**Финальный скриншот:**
- Весь дашборд целиком (все панели на одном экране)
