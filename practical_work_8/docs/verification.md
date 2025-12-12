# Проверка работоспособности

> **Note:** Load configuration first:
> ```bash
> source practical_work_8/secrets/config.env
> ```

## 1. Docker контейнеры

**Команда:**
```bash
ssh $SSH_USER@$VM_PUBLIC_IP "sudo docker ps"
```

**Результат:** 2 контейнера работают (RUNNING):
- **adcm** - порт 8000
- **adcm-db** - PostgreSQL 13

## 2. ADCM веб-интерфейс

**URL:** `$ADCM_URL`

**Доступ:**
- Login: `$ADCM_USERNAME`
- Password: `$ADCM_PASSWORD`

**Статус:** Интерфейс загружается, показывает HTML-страницу ADCM

## 3. PostgreSQL база данных

**Подключение через Docker:**
```bash
ssh $SSH_USER@$VM_PUBLIC_IP "sudo docker exec -i adcm-db psql -U $POSTGRES_USER -d $POSTGRES_DB"
```

**Проверка таблиц:**
```bash
ssh $SSH_USER@$VM_PUBLIC_IP "sudo docker exec -i adcm-db psql -U $POSTGRES_USER -d $POSTGRES_DB -c '\dt'"
```

**Результат:** 11 таблиц созданы:
- customers
- geolocation
- leads_closed
- leads_qualified
- order_items
- order_payments
- order_reviews
- orders
- product_category_name_translation
- products
- sellers

**Статус данных:** Таблицы пустые, ждут импорта CSV

## 4. Сетевое подключение

**Проверка порта ADCM:**
```bash
curl -s $ADCM_URL | head -5
```

**Результат:** HTTP 200, возвращается HTML

## Что работает:
✓ VM доступна по SSH
✓ Docker контейнеры запущены
✓ ADCM веб-интерфейс доступен
✓ PostgreSQL работает
✓ База ecommerce создана
✓ Структура таблиц готова

## Что осталось:
- Загрузить бандлы в ADCM
- Настроить ADCM кластер
- Импортировать CSV данные
- Настроить Grafana
