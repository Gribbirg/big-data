# Практическая работа №8. Последовательность развертывания компонент и настройки

## Требуемое ПО

1. Среда виртуализации с поддержкой сетевого моста - **VirtualBox**
2. Образ серверной версии Linux - **Ubuntu Server 22.04 LTS**
3. Бандлы ADPG и SSH common для **ADCM**
4. **DBeaver CE** для подключения к базе данных PostgreSQL

## Часть 1. Установка и настройка виртуальной машины

### 1.1 Создание виртуальной машины в VirtualBox

**Параметры ВМ:**
- CPU: 1
- RAM: 2 ГБ
- Жесткий диск: 25 ГБ (виртуальный)
- Тип сети: **Bridged Adapter** (сетевой мост)
- ОС: Ubuntu Server 22.04 LTS

### 1.2 Установка Ubuntu Server

1. **Выбор языка установщика**: English (рекомендуется для работы с ADCM/ADPG)

2. **Обновление установщика**: Выбрать "Continue without updating" для воспроизводимости шагов

3. **Раскладка клавиатуры**: English (US) для Layout и Variant

4. **Профиль установки**: Ubuntu Server (стандартный)
   - Не включать поиск сторонних драйверов

5. **Сетевая конфигурация**:
   - Интерфейс получит адрес по DHCP (например: 10.0.60.168/24)
   - Сетевой мост работает корректно - ВМ в той же сети, что и хост

6. **Proxy**: Оставить пустым (если нет корпоративного прокси)

7. **Зеркало архивов**: http://ru.archive.ubuntu.com/ubuntu/

8. **Разметка диска**:
   - Use an entire disk
   - Set up this disk as an LVM group
   - Шифрование LUKS не включать

**Итоговая разметка:**
- `/boot` - ext4 (~2 ГБ)
- `/` - LVM ext4 (~11.5 ГБ)
- Физический диск: BIOS-раздел (~1 ГБ) + /boot + LVM-группа ubuntu-vg (~23 ГБ)

9. **Подтверждение**: Continue при предупреждении о форматировании

10. **Профиль пользователя**:
    - Name: user
    - Server name: os
    - Username: user
    - Password: user

11. **Ubuntu Pro**: Skip for now

12. **SSH**: Install OpenSSH server (отметить галочкой)

13. **Featured server snaps**: Не выбирать

14. После установки: **Reboot Now**

### 1.3 Первый вход в систему

После перезагрузки:
- Login: user
- Password: user

**Проверка IP-адреса:**
```bash
ip a
```

**Подключение по SSH** (с хост-машины):
```bash
ssh -o ServerAliveInterval=60 user@10.0.60.168 -y
```

## Часть 2. Установка Docker

### 2.1 Установка зависимостей

```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

### 2.2 Добавление ключа и репозитория Docker

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 2.3 Установка Docker

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin
```

### 2.4 Настройка зеркала Docker

```bash
sudo sh -c 'echo "{ \"registry-mirrors\": [\"https://dockerhub.timeweb.cloud\"] }" >> /etc/docker/daemon.json'
sudo systemctl restart docker
sudo systemctl status docker
```

### 2.5 Тестирование Docker

```bash
sudo docker run hello-world
```

### 2.6 Добавление пользователя в группу docker

```bash
sudo usermod -aG docker $USER
newgrp docker
sudo apt update
```

### 2.7 Установка Docker Compose

```bash
sudo apt install docker-compose-plugin
docker compose version
```

## Часть 3. Развертывание ADCM

### 3.1 Создание сети Docker

```bash
sudo docker network create adcm-net
```

### 3.2 Запуск контейнера PostgreSQL для ADCM

```bash
sudo docker run -d \
--name adcm-db \
--network adcm-net \
-v adcm-db-data:/var/lib/postgresql/data \
-e POSTGRES_PASSWORD=UseAStrongPassword \
-e POSTGRES_USER=adcm_user \
-e POSTGRES_DB=adcm_db \
--restart on-failure \
postgres:13
```

### 3.3 Запуск контейнера ADCM

```bash
sudo docker run -d \
--name adcm \
--network adcm-net \
-p 8000:8000 \
-v /opt/adcm:/adcm/data \
-e DB_HOST=adcm-db \
-e DB_PORT=5432 \
-e DB_NAME=adcm_db \
-e DB_USER=adcm_user \
-e DB_PASS=UseAStrongPassword \
--restart on-failure \
arenadata/adcm:2.7.1
```

### 3.4 Проверка запущенных контейнеров

```bash
sudo docker ps
```

### 3.5 Настройка sudo без пароля

```bash
sudo visudo
```

Добавить в конец файла:
```
user ALL=(ALL) NOPASSWD:ALL
```

Сохранить: Ctrl+O, Enter, Ctrl+X

### 3.6 Доступ к ADCM

**Через сетевой мост:**
```
http://10.0.60.168:8000
```

**Через SSH туннель (для удаленного сервера):**
```bash
ssh -fN -L 8080:0.0.0.0:8000 root@<server_ip>
```
Затем открыть: http://localhost:8080

**Учетные данные:**
- Login: admin
- Password: admin

## Часть 4. Настройка ADCM

### 4.1 Первоначальная настройка

1. Войти в интерфейс ADCM
2. Settings → Global Options → ADCM's URL
   - Указать конкретный URL из адресной строки
   - Сохранить (Save)

### 4.2 Загрузка бандлов

1. Перейти в раздел **Bundles**
2. Нажать **Upload bundle**
3. Загрузить:
   - `adcm_host_ssh_v2.11-1_community.tar`
   - `adcm_cluster_adpg_v16.3_arenadata4.4_b1-1_community.tar`

### 4.3 Создание Hostprovider

1. Перейти в раздел **Hostproviders**
2. Нажать **Create hostprovider**
3. Параметры:
   - Type: SSH Common
   - Version: 2.11-1
   - Name: ssh1
   - Description: (любое)
4. Создать (Create)

### 4.4 Настройка Hostprovider

1. Открыть созданный hostprovider
2. Primary configuration → Metadata
3. Установить параметры:
   - **Username**: user
   - **Password**: user (дважды для подтверждения)
4. Сохранить (Save)

### 4.5 Создание кластера

1. Перейти в **Clusters**
2. Нажать **Create cluster**
3. Параметры:
   - Product: ADPG
   - Product version: 16.3_arenadata4.4_b1-1 (community)
   - Cluster name: adpg_cluster
   - Description: (любое)
   - Принять Terms of Agreement
4. Создать (Create)

### 4.6 Добавление сервисов

1. Открыть созданный кластер
2. Перейти на вкладку **Services**
3. Нажать **Add services**
4. Выбрать:
   - ADPG ✓
   - Monitoring ✓
5. Добавить (Add)
6. Нажать **Got it**

### 4.7 Создание хоста

1. Перейти в раздел **Hosts**
2. Нажать **Create host**
3. Параметры:
   - Hostprovider: ssh1
   - Name: host1
   - Cluster: adpg_cluster
4. Создать (Create)

### 4.8 Настройка хоста

1. Открыть созданный хост
2. Primary configuration → Configuration
3. Установить параметры:
   - **Username**: user
   - **Password**: user
   - **Connection address**: 10.41.80.156 (актуальный IP вашей ВМ)
   - **Port**: 22
4. Сохранить (Save)

### 4.9 Маппинг компонентов

1. Вернуться в кластер → вкладка **Mapping**
2. Для каждого сервиса:

**Monitoring:**
- Prometheus Server: host1
- Grafana: host1
- Node Exporter: host1
- ADPG Exporter: host1

**ADPG:**
- ADPG: host1

3. Сохранить (Save)

### 4.10 Настройка сервиса Monitoring

1. Кластер → Services → Monitoring
2. Primary configuration
3. **Prometheus settings** → Add property:
   - Field name: `Prometheus_admin`
   - Secret: `admin`
   - Confirm: `admin`
   - Apply

4. **Grafana settings**:
   - Grafana administrator's password: `123456Abcadmin?`

5. Сохранить (Save)

### 4.11 Установка статусчекера

1. Hosts → host1
2. Действия → Install statuschecker
3. Raising concerns → Next
4. Confirmation → Verbose ✓ → Run

Дождаться завершения (Jobs)

### 4.12 Установка кластера

1. Clusters → adpg_cluster
2. Действия → Install
3. Configuration:
   - Reboot cluster servers after installation: false
4. Next → Next
5. Confirmation → Verbose ✓ → Run

Дождаться завершения (может занять несколько минут)

### 4.13 Запуск кластера

1. Clusters → adpg_cluster
2. Действия → Start
3. Raising concerns → Next
4. Confirmation → Verbose ✓ → Run

### 4.14 Запуск мониторинга

1. Services → Monitoring
2. Действия → Start
3. Raising concerns → Next
4. Confirmation → Verbose ✓ → Run

## Часть 5. Настройка PostgreSQL

### 5.1 Установка клиента PostgreSQL

```bash
sudo apt install postgresql-client
```

### 5.2 Проверка порта PostgreSQL

```bash
ss -lntp | grep 5432 || true
```

### 5.3 Подключение к PostgreSQL

```bash
sudo -u postgres psql -d postgres
```

### 5.4 Просмотр баз данных

```sql
\l
```

### 5.5 Установка пароля для postgres

```sql
ALTER ROLE postgres WITH PASSWORD 'secret';
```

### 5.6 Создание базы данных

```sql
CREATE DATABASE ecommerce;
```

### 5.7 Подключение к базе

```bash
sudo -u postgres psql -d ecommerce
```

### 5.8 Настройка ADPG для внешних подключений

1. ADCM → Clusters → adpg_cluster → Services → ADPG
2. Primary configuration
3. **ADPG configurations**:
   - `listen_addresses = '*'`
4. **PG_HBA**:
   - Добавить: `host all all 0.0.0.0/0 md5`
5. Сохранить (Save)

### 5.9 Перезапуск ADPG

1. Services → ADPG
2. Действия → Reconfigure & Restart
3. Configuration → Next → Next
4. Confirmation → Verbose ✓ → Run

## Часть 6. Подключение Grafana к PostgreSQL

### 6.1 Доступ к Grafana

```
http://10.41.80.156:11210
```

**Учетные данные:**
- Email or username: admin
- Password: 123456Abcadmin?

### 6.2 Добавление источника данных

1. Connections → Connect data
2. Выбрать PostgreSQL
3. Нажать **Create a PostgreSQL data source**

### 6.3 Настройка подключения

**PostgreSQL Connection:**
- Name: Ecom-ADPG (или любое)
- Host: localhost:5432
- Database: ecommerce
- User: postgres
- Password: secret
- TLS/SSL Mode: disable

**Connection limits:**
- Max open: 100
- Max idle: 100, Auto: On

### 6.4 Сохранение и тестирование

1. Нажать **Save & test**
2. Должно появиться: "Database Connection OK"

## Часть 7. Создание схемы БД ecommerce

### 7.1 Создание таблиц

Выполнить следующий SQL-скрипт в DBeaver или psql:

```sql
-- Таблица sellers
CREATE TABLE IF NOT EXISTS sellers (
 seller_id text PRIMARY KEY,
 seller_zip_code_prefix integer,
 seller_city text,
 seller_state text
);
CREATE INDEX IF NOT EXISTS idx_sellers_zip
 ON sellers (seller_zip_code_prefix);

-- Таблица customers
CREATE TABLE IF NOT EXISTS customers (
 customer_id text PRIMARY KEY,
 customer_unique_id text NOT NULL,
 customer_zip_code_prefix integer,
 customer_city text,
 customer_state text
);
CREATE INDEX IF NOT EXISTS idx_customers_unique_id
 ON customers (customer_unique_id);
CREATE INDEX IF NOT EXISTS idx_customers_zip
 ON customers (customer_zip_code_prefix);

-- Таблица geolocation
CREATE TABLE IF NOT EXISTS geolocation (
 geolocation_id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
 geolocation_zip_code_prefix integer,
 geolocation_lat double precision,
 geolocation_lng double precision,
 geolocation_city text,
 geolocation_state text
);
CREATE INDEX IF NOT EXISTS idx_geolocation_zip
 ON geolocation (geolocation_zip_code_prefix);
CREATE INDEX IF NOT EXISTS idx_geolocation_city_state
 ON geolocation (geolocation_city, geolocation_state);

-- Таблица leads_qualified
CREATE TABLE IF NOT EXISTS leads_qualified (
 mql_id text PRIMARY KEY,
 first_contact_date timestamp,
 landing_page_id text,
 origin text
);
CREATE INDEX IF NOT EXISTS idx_leads_first_contact
 ON leads_qualified (first_contact_date);

-- Таблица product_category_name_translation
CREATE TABLE IF NOT EXISTS product_category_name_translation (
 product_category_name text PRIMARY KEY,
 product_category_name_english text
);

-- Таблица products
CREATE TABLE IF NOT EXISTS products (
 product_id text PRIMARY KEY,
 product_category_name text,
 product_name_lenght integer,
 product_description_lenght integer,
 product_photos_qty integer,
 product_weight_g numeric,
 product_length_cm numeric,
 product_height_cm numeric,
 product_width_cm numeric,
 CONSTRAINT fk_products_category
 FOREIGN KEY (product_category_name)
 REFERENCES product_category_name_translation(product_category_name)
 ON UPDATE CASCADE
 ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_products_category
 ON products (product_category_name);

-- Таблица orders
CREATE TABLE IF NOT EXISTS orders (
 order_id text PRIMARY KEY,
 customer_id text NOT NULL,
 order_status text,
 order_purchase_timestamp timestamp,
 order_approved_at timestamp,
 order_delivered_carrier_date timestamp,
 order_delivered_customer_date timestamp,
 order_estimated_delivery_date timestamp,
 CONSTRAINT fk_orders_customer
 FOREIGN KEY (customer_id)
 REFERENCES customers(customer_id)
 ON UPDATE CASCADE
 ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS idx_orders_customer
 ON orders (customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_purchase_ts
 ON orders (order_purchase_timestamp);
CREATE INDEX IF NOT EXISTS idx_orders_status
 ON orders (order_status);

-- Таблица order_reviews
CREATE TABLE IF NOT EXISTS order_reviews (
 review_id text PRIMARY KEY,
 order_id text NOT NULL,
 review_score integer,
 review_comment_title text,
 review_comment_message text,
 review_creation_date timestamp,
 review_answer_timestamp timestamp,
 CONSTRAINT fk_order_reviews_order
 FOREIGN KEY (order_id)
 REFERENCES orders(order_id)
 ON UPDATE CASCADE
 ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_orderreviews_order
 ON order_reviews (order_id);
CREATE INDEX IF NOT EXISTS idx_orderreviews_score
 ON order_reviews (review_score);

-- Таблица order_payments
CREATE TABLE IF NOT EXISTS order_payments (
 order_id text NOT NULL,
 payment_sequential integer NOT NULL,
 payment_type text,
 payment_installments integer,
 payment_value numeric,
 PRIMARY KEY (order_id, payment_sequential),
 CONSTRAINT fk_order_payments_order
 FOREIGN KEY (order_id)
 REFERENCES orders(order_id)
 ON UPDATE CASCADE
 ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_orderpayments_order
 ON order_payments (order_id);
CREATE INDEX IF NOT EXISTS idx_orderpayments_type
 ON order_payments (payment_type);

-- Таблица leads_closed
CREATE TABLE IF NOT EXISTS leads_closed (
 mql_id text PRIMARY KEY,
 seller_id text,
 sdr_id text,
 sr_id text,
 won_date timestamp,
 business_segment text,
 lead_type text,
 lead_behaviour_profile text,
 has_company boolean,
 has_gtin boolean,
 average_stock numeric,
 business_type text,
 declared_product_catalog_size integer,
 declared_monthly_revenue numeric,
 CONSTRAINT fk_leads_closed_mql
 FOREIGN KEY (mql_id)
 REFERENCES leads_qualified(mql_id)
 ON UPDATE CASCADE
 ON DELETE CASCADE,
 CONSTRAINT fk_leads_closed_seller
 FOREIGN KEY (seller_id)
 REFERENCES sellers(seller_id)
 ON UPDATE CASCADE
 ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_leads_won_date
 ON leads_closed (won_date);
CREATE INDEX IF NOT EXISTS idx_leads_seller
 ON leads_closed (seller_id);

-- Таблица order_items
CREATE TABLE IF NOT EXISTS order_items (
 order_id text NOT NULL,
 order_item_id integer NOT NULL,
 product_id text,
 seller_id text,
 shipping_limit_date timestamp,
 price numeric,
 freight_value numeric,
 PRIMARY KEY (order_id, order_item_id),
 CONSTRAINT fk_order_items_order
 FOREIGN KEY (order_id)
 REFERENCES orders(order_id)
 ON UPDATE CASCADE
 ON DELETE CASCADE,
 CONSTRAINT fk_order_items_product
 FOREIGN KEY (product_id)
 REFERENCES products(product_id)
 ON UPDATE CASCADE
 ON DELETE SET NULL,
 CONSTRAINT fk_order_items_seller
 FOREIGN KEY (seller_id)
 REFERENCES sellers(seller_id)
 ON UPDATE CASCADE
 ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_orderitems_product
 ON order_items (product_id);
CREATE INDEX IF NOT EXISTS idx_orderitems_seller
 ON order_items (seller_id);
CREATE INDEX IF NOT EXISTS idx_orderitems_order
 ON order_items (order_id);
```

### 7.2 Импорт данных через DBeaver

**Порядок импорта (по зависимостям):**

1. geolocation → geolocation.csv
2. leads_qualified → leads_qualified.csv
3. product_category_name_translation → product_category_name_translation.csv
4. sellers → sellers.csv
5. customers → customers.csv
6. leads_closed → leads_closed.csv
7. products → products.csv
8. orders → orders.csv
9. order_items → order_items.csv
10. order_reviews → order_reviews.csv
11. order_payments → order_payments.csv

**Настройки импорта в DBeaver:**
- Разделитель столбцов: `\t`
- Значение NULL: `NULL`

## Часть 8. Создание дашборда в Grafana

### 8.1 Создание нового дашборда

1. Dashboards → New dashboard
2. Add visualization
3. Выбрать источник данных: Ecom-ADPG

### 8.2 Пример запроса

```sql
SELECT review_score, COUNT(review_id) as count
FROM order_reviews
GROUP BY review_score
ORDER BY review_score DESC;
```

### 8.3 Настройка визуализации

1. В Query выбрать:
   - Table: order_reviews
   - Column: review_score
   - Aggregation: COUNT
2. Add column:
   - Column: review_id
   - Aggregation: COUNT
3. Group by: review_score
4. Order by: COUNT(review_id) DESC

### 8.4 Переключение на Transform

1. Convert field type
2. Field: review_score → String
3. Apply

### 8.5 Выбор типа визуализации

Справа выбрать тип графика (например, Bar chart)

### 8.6 Сохранение

1. Apply
2. Save dashboard
3. Указать название

## Часть 9. Управление кластером

### 9.1 Перезапуск Docker-контейнеров

```bash
docker stop adcm
docker stop adcm-db
sudo systemctl restart docker
docker start adcm-db
docker start adcm
```

### 9.2 Проверка статуса контейнеров

```bash
sudo docker ps
```

### 9.3 Остановка и запуск через ADCM

1. Clusters → adpg_cluster
2. Действия:
   - **Check** - проверка состояния
   - **Reinstall** - переустановка
   - **Reinstall statuschecker** - переустановка статусчекера
   - **Start** - запуск
   - **Stop** - остановка

## Примечания

- **IP-адрес может меняться** при смене сетевого адаптера физического устройства
- При изменении IP необходимо обновить:
  - Connection address в ADCM для хоста
  - Host в настройках Grafana (если используется)
- Для продакшена рекомендуется использовать статический IP или резервирование в DHCP

## Полезные команды

**Проверка портов:**
```bash
ss -lntp | grep 5432  # PostgreSQL
ss -lntp | grep 8000  # ADCM
ss -lntp | grep 11210 # Grafana
```

**Логи Docker:**
```bash
docker logs adcm
docker logs adcm-db
```

**Подключение к PostgreSQL из консоли:**
```bash
sudo -u postgres psql -d ecommerce
```

**Просмотр таблиц:**
```sql
\dt
```

**Выход из psql:**
```sql
\q
```
