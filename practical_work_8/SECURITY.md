# Security Configuration

This document explains the security measures implemented in this project.

## Overview

All sensitive information (passwords, IP addresses, credentials) has been moved to `secrets/config.env` which is excluded from version control.

## Setup

1. **Copy the example configuration:**
   ```bash
   cd practical_work_8
   cp secrets/config.env.example secrets/config.env
   ```

2. **Edit with your actual values:**
   ```bash
   nano secrets/config.env  # or use any text editor
   ```

3. **Load the configuration before running commands:**
   ```bash
   source practical_work_8/secrets/config.env
   ```

## Configuration Variables

The following environment variables are used throughout the documentation:

### VM Configuration
- `VM_PUBLIC_IP` - Public IP address of the VM
- `VM_PRIVATE_IP` - Private IP address of the VM
- `SSH_USER` - SSH username

### ADCM Configuration
- `ADCM_URL` - ADCM web interface URL
- `ADCM_USERNAME` - ADCM admin username
- `ADCM_PASSWORD` - ADCM admin password

### Grafana Configuration
- `GRAFANA_URL` - Grafana web interface URL
- `GRAFANA_USERNAME` - Grafana admin username
- `GRAFANA_PASSWORD` - Grafana admin password

### PostgreSQL Configuration
- `POSTGRES_HOST` - PostgreSQL host
- `POSTGRES_PORT` - PostgreSQL port
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - PostgreSQL username

### Hostprovider Configuration
- `HOSTPROVIDER_USERNAME` - Hostprovider username
- `HOSTPROVIDER_PASSWORD` - Hostprovider password

## Files Updated

The following files have been updated to use environment variables instead of hardcoded values:

- `grafana/GRAFANA_SETUP.md`
- `docs/vm_setup.md`
- `docs/adcm_setup_manual.md`
- `docs/verification.md`
- `docs/import_summary.md`
- `docs/grafana_queries.md`

## Security Best Practices

1. **Never commit `secrets/config.env`** - It's in `.gitignore` for a reason
2. **Rotate passwords regularly** - Especially for production environments
3. **Use strong passwords** - Minimum 12 characters, mix of letters, numbers, symbols
4. **Limit access** - Only share credentials with authorized personnel
5. **Use SSH keys** - Instead of passwords for SSH access when possible

## Troubleshooting

If commands fail with "variable not set" errors:
```bash
# Make sure you loaded the configuration
source practical_work_8/secrets/config.env

# Verify variables are set
echo $VM_PUBLIC_IP
echo $GRAFANA_URL
```

## For Development

When working with this project:
1. Always load config before running any commands
2. Add to your shell profile for automatic loading:
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   alias load-pw8='source ~/path/to/practical_work_8/secrets/config.env'
   ```

## Notes

- The `secrets/config.env.example` file is tracked in git as a template
- Only the actual `secrets/config.env` is excluded from version control
- This approach keeps sensitive data secure while maintaining documentation usability
