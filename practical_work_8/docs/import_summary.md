# Импорт данных - Итоги

> **Note:** Load configuration for database access:
> ```bash
> source practical_work_8/secrets/config.env
> ```

## Статус: ✓ Завершено успешно

Все CSV файлы успешно импортированы в базу данных `ecommerce`.

## Статистика импорта

| Таблица | Записей | Размер файла |
|---------|---------|--------------|
| geolocation | 1,000,163 | 63 MB |
| customers | 99,441 | 8.5 MB |
| orders | 99,441 | 19 MB |
| order_items | 111,023 | 15 MB |
| order_payments | 103,886 | 5.6 MB |
| order_reviews | 97,621 | 15 MB |
| products | 32,328 | 2.3 MB |
| sellers | 3,095 | 167 KB |
| leads_qualified | 8,000 | 816 KB |
| leads_closed | 380 | 85 KB |
| product_category_name_translation | 71 | 2.6 KB |
| **ВСЕГО** | **1,555,449** | **~130 MB** |

## Порядок импорта (по зависимостям)

1. ✓ geolocation
2. ✓ leads_qualified
3. ✓ product_category_name_translation
4. ✓ sellers
5. ✓ customers
6. ✓ leads_closed
7. ✓ products
8. ✓ orders
9. ✓ order_items
10. ✓ order_reviews
11. ✓ order_payments

## Параметры импорта

- **Формат**: CSV
- **Разделитель**: TAB (`\t`)
- **Заголовки**: Присутствуют (HEADER true)
- **NULL значения**: 'NULL'
- **Кодировка**: UTF-8

## Проверка данных

**Команда для проверки:**
```sql
SELECT schemaname, relname as tablename, n_live_tup as row_count
FROM pg_stat_user_tables
ORDER BY relname;
```

**Результат:** Все таблицы содержат данные, foreign key ограничения соблюдены.

## Доступ к БД

**Через Docker контейнер:**
```bash
ssh $SSH_USER@$VM_PUBLIC_IP
sudo docker exec -it adcm-db psql -U $POSTGRES_USER -d $POSTGRES_DB
```

**Внутри VM (после настройки ADPG через ADCM):**
```bash
psql -U postgres -d $POSTGRES_DB -h $POSTGRES_HOST -p $POSTGRES_PORT
```

## Следующие шаги

1. Завершить настройку ADCM кластера (см. `adcm_setup_manual.md`)
2. Настроить подключение PostgreSQL для внешнего доступа
3. Настроить Grafana data source
4. Выполнить SQL запросы из задания
5. Создать дашборды в Grafana
