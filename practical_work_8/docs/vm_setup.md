# VM Parameters - Yandex Cloud

> **Note:** Sensitive values are stored in `practical_work_8/secrets/config.env`
> ```bash
> source practical_work_8/secrets/config.env
> ```

## Instance Details
- **Name**: ubuntu-adcm
- **ID**: fhmq982ukc3c2q8jlvvl
- **Zone**: ru-central1-a
- **Status**: RUNNING

## Resources
- **vCPU**: 4 cores
- **RAM**: 4 GB
- **Disk**: 30 GB (boot disk)
- **Platform**: standard-v2

## Network
- **Public IP**: `$VM_PUBLIC_IP`
- **Private IP**: `$VM_PRIVATE_IP`
- **Subnet**: default-ru-central1-a (e9bcdtu2snl87djsn6i9)
- **Network**: default (enpmot2ebi6so6nue3o3)

## Access
- **User**: `$SSH_USER`
- **SSH Key**: ~/.ssh/id_ed25519.pub
- **SSH Command**: `ssh $SSH_USER@$VM_PUBLIC_IP`

## Software Stack
- **OS**: Ubuntu 22.04 LTS
- **Docker**: 29.1.3 ✓
- **Docker Compose**: v5.0.0 ✓
- **PostgreSQL**: 13 (in Docker) ✓
- **ADCM**: 2.7.1 (in Docker) ✓
- **PostgreSQL Client**: 14 ✓
- **Grafana**: (via ADCM Monitoring bundle)
- **Prometheus**: (via ADCM Monitoring bundle)

## Services
- **ADCM Web**: `$ADCM_URL` (credentials in config.env)
- **PostgreSQL**: `$POSTGRES_HOST:$POSTGRES_PORT` (inside adcm-db container)

## Database
- **ecommerce** database created ✓
- **11 tables** created:
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

## Docker Containers
- **adcm-db**: PostgreSQL 13 (network: adcm-net)
- **adcm**: ADCM 2.7.1 (port 8000, network: adcm-net)

## Created
2025-12-12 19:37:00 UTC
