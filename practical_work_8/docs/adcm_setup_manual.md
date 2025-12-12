# Настройка ADCM - Ручные шаги

> **Note:** Load configuration before starting:
> ```bash
> source practical_work_8/secrets/config.env
> ```

## Предварительно выполнено

✓ Бандлы загружены на VM в `/tmp/`:
- `adcm_host_ssh_v2.11-1_community.tar`
- `adcm_cluster_adpg_v16.3_arenadata4.4_b1-1_community.tar`

✓ Бандлы скопированы в контейнер ADCM:
- `/adcm/data/bundle/adcm_host_ssh_v2.11-1_community.tar`
- `/adcm/data/bundle/adcm_cluster_adpg_v16.3_arenadata4.4_b1-1_community.tar`

## Шаги для настройки через веб-интерфейс

### 1. Открыть ADCM

URL: **`$ADCM_URL`**

Логин: `$ADCM_USERNAME`
Пароль: `$ADCM_PASSWORD`

### 2. Загрузить бандлы

1. Перейти в раздел **Bundles**
2. Нажать **Upload bundle**
3. Выбрать файл на локальной машине:
   - `adcm_host_ssh_v2.11-1_community (1).tar`
4. Дождаться загрузки
5. Повторить для второго бандла:
   - `adcm_cluster_adpg_v16.3_arenadata4.4_b1-1_community (1).tar`

**Альтернатива:** Можно скачать бандлы с VM обратно на локальную машину:
```bash
scp $SSH_USER@$VM_PUBLIC_IP:/tmp/adcm_host_ssh_v2.11-1_community.tar ~/Downloads/
scp $SSH_USER@$VM_PUBLIC_IP:/tmp/adcm_cluster_adpg_v16.3_arenadata4.4_b1-1_community.tar ~/Downloads/
```

### 3. Настроить ADCM URL

1. Settings → Global Options → ADCM's URL
2. Указать: `$ADCM_URL`
3. Нажать **Save**

### 4. Создать Hostprovider

1. Перейти в **Hostproviders**
2. Нажать **Create hostprovider**
3. Параметры:
   - Type: SSH Common
   - Version: 2.11-1
   - Name: ssh1
   - Description: (любое)
4. Нажать **Create**

### 5. Настроить Hostprovider

1. Открыть созданный hostprovider `ssh1`
2. Primary configuration → Metadata
3. Установить:
   - **Username**: `$HOSTPROVIDER_USERNAME`
   - **Password**: `$HOSTPROVIDER_PASSWORD` (дважды)
4. Нажать **Save**

### 6. Создать кластер

1. Перейти в **Clusters**
2. Нажать **Create cluster**
3. Параметры:
   - Product: ADPG
   - Product version: 16.3_arenadata4.4_b1-1 (community)
   - Cluster name: adpg_cluster
   - Description: (любое)
   - ✓ Принять Terms of Agreement
4. Нажать **Create**

### 7. Добавить сервисы

1. Открыть кластер `adpg_cluster`
2. Вкладка **Services**
3. Нажать **Add services**
4. Выбрать:
   - ✓ ADPG
   - ✓ Monitoring
5. Нажать **Add**
6. Нажать **Got it**

### 8. Создать хост

1. Перейти в **Hosts**
2. Нажать **Create host**
3. Параметры:
   - Hostprovider: ssh1
   - Name: host1
   - Cluster: adpg_cluster
4. Нажать **Create**

### 9. Настроить хост

1. Открыть хост `host1`
2. Primary configuration → Configuration
3. Установить:
   - **Username**: `$SSH_USER`
   - **Password**: `$HOSTPROVIDER_PASSWORD`
   - **Connection address**: `$VM_PRIVATE_IP` (внутренний IP VM)
   - **Port**: `22`
4. Нажать **Save**

### 10. Маппинг компонентов

1. Кластер → вкладка **Mapping**
2. Для **Monitoring**:
   - Prometheus Server: host1
   - Grafana: host1
   - Node Exporter: host1
   - ADPG Exporter: host1
3. Для **ADPG**:
   - ADPG: host1
4. Нажать **Save**

### 11. Настроить Monitoring

1. Кластер → Services → Monitoring
2. Primary configuration
3. **Prometheus settings** → Add property:
   - Field name: `Prometheus_admin`
   - Secret: `$ADCM_USERNAME`
   - Confirm: `$ADCM_PASSWORD`
   - Apply
4. **Grafana settings**:
   - Grafana administrator's password: `$GRAFANA_PASSWORD`
5. Нажать **Save**

### 12. Установить statuschecker

1. Hosts → host1
2. Действия → Install statuschecker
3. Raising concerns → Next
4. Confirmation → ✓ Verbose → Run
5. Дождаться завершения (проверить в Jobs)

### 13. Установить кластер

1. Clusters → adpg_cluster
2. Действия → Install
3. Configuration:
   - Reboot cluster servers after installation: false
4. Next → Next
5. Confirmation → ✓ Verbose → Run
6. Дождаться завершения (может занять несколько минут)

### 14. Запустить кластер

1. Clusters → adpg_cluster
2. Действия → Start
3. Raising concerns → Next
4. Confirmation → ✓ Verbose → Run

### 15. Запустить мониторинг

1. Services → Monitoring
2. Действия → Start
3. Raising concerns → Next
4. Confirmation → ✓ Verbose → Run

## После завершения

После успешного запуска всех сервисов:

- **ADCM**: `$ADCM_URL`
- **Grafana**: `$GRAFANA_URL`
  - Login: `$GRAFANA_USERNAME`
  - Password: `$GRAFANA_PASSWORD`

Кластер ADPG должен быть в статусе **Running** со всеми зелеными индикаторами.
