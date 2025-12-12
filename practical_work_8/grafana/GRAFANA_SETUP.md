# Быстрый старт - Grafana Dashboard

> **Note:** Before starting, load the configuration:
> ```bash
> source practical_work_8/secrets/config.env
> ```

## 1. Открой Grafana

**URL:** `$GRAFANA_URL`

**Логин:**
- Username: `$GRAFANA_USERNAME`
- Password: `$GRAFANA_PASSWORD`

---

## 2. Проверь подключение к PostgreSQL

1. Перейди в **Connections → Data sources**
2. Найди источник с PostgreSQL (например, `Ecom-ADPG`)
3. Нажми **Test** - должно быть "Database Connection OK"

**Если источника нет, создай:**
1. Connections → Add data source → PostgreSQL
2. Настройки:
   - Host: `$POSTGRES_HOST:$POSTGRES_PORT`
   - Database: `$POSTGRES_DB`
   - User: `$POSTGRES_USER`
   - Password: (check container or config)
   - TLS/SSL Mode: `disable`
3. Save & test

---

## 3. Создай дашборд

### Шаг 1: Создание
1. Dashboards → New dashboard
2. Add visualization
3. Выбери PostgreSQL data source

### Шаг 2: Добавь первую панель (4.1 - График по месяцам)

1. В Query editor переключись на **Code** (правый верхний угол)
2. Скопируй и вставь SQL из файла: `sql/grafana/4_1_orders_by_month.sql`
3. Справа выбери визуализацию: **Time series**
4. В **Panel options** установи:
   - Title: "Динамика числа заказов по месяцам"
5. Нажми **Apply**

### Шаг 3: Добавь остальные панели

Повтори для каждого запроса:
- `4_2_orders_by_rating.sql` → **Bar chart** (вертикальные столбцы)
- `4_3_payment_distribution.sql` → **Pie chart**
- `4_4_top_categories.sql` → **Bar chart** (horizontal)
- `4_5_delivery_by_state.sql` → **Table**
- `4_5_avg_order_value.sql` → **Time series**

### Шаг 4: Расположи панели

Drag & drop для изменения размера и положения.

**Рекомендуемая раскладка:**
```
┌─────────────────────────┬─────────────────────────┐
│  4.1 Orders by Month    │  4.5.2 Avg Order Value  │
│  (Time series)          │  (Time series)          │
├─────────────┬───────────┼─────────────────────────┤
│ 4.2 Ratings │ 4.3 Pay   │  4.4 Top Categories     │
│ (Bar chart) │ (Pie)     │  (Horizontal bars)      │
├─────────────┴───────────┴─────────────────────────┤
│  4.5.1 Delivery by State (Table)                  │
└───────────────────────────────────────────────────┘
```

### Шаг 5: Сохрани дашборд
1. Иконка дискеты (Save dashboard)
2. Title: "Ecommerce Analytics"
3. Folder: General
4. **Save**

---

## 4. Сделай скриншоты

### Для отчета нужно:

1. **Скриншот каждой визуализации** (6 штук)
   - Открой панель на полный экран (три точки → View)
   - Скриншот

2. **Скриншот всего дашборда** (1 штук)
   - Уменьши масштаб браузера (Cmd + "-") чтобы влезло все
   - Скриншот

3. **Текстовые выводы** по каждой визуализации:
   - Что видно на графике
   - Какие тренды/паттерны
   - Какие выводы для бизнеса

---

## 5. Экспорт дашборда (опционально)

1. Share dashboard → Export → Save to file
2. Сохрани как `ecommerce_dashboard.json`
3. Можно будет импортировать на другом сервере

---

## Полезные ссылки

- **Документация SQL запросов:** `docs/grafana_queries.md`
- **SQL файлы:** `sql/grafana/`
- **Результаты SQL запросов:** `report/results/sql_queries.md`

---

## Проблемы?

### Grafana не открывается
```bash
ssh $SSH_USER@$VM_PUBLIC_IP
sudo docker ps | grep adcm
# Проверь что контейнер adcm запущен
```

### PostgreSQL не подключается
```bash
ssh $SSH_USER@$VM_PUBLIC_IP "sudo docker exec -i adcm-db psql -U $POSTGRES_USER -d $POSTGRES_DB -c 'SELECT 1'"
# Должно вернуть: 1
```

### Запрос не работает
Проверь SQL локально:
```bash
ssh $SSH_USER@$VM_PUBLIC_IP "cat /path/to/query.sql | sudo docker exec -i adcm-db psql -U $POSTGRES_USER -d $POSTGRES_DB"
```
