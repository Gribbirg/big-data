# Secrets Configuration
This directory contains sensitive configuration data that should NOT be committed to version control.

## Files

- `config.env` - Your actual configuration (DO NOT COMMIT)
- `config.env.example` - Template for creating your own config

## Setup

1. Copy the example file:
   ```bash
   cp config.env.example config.env
   ```

2. Edit `config.env` with your actual values

3. Load the configuration in your shell:
   ```bash
   source practical_work_8/secrets/config.env
   ```

## Usage in Documentation

Instead of hardcoding values, documentation now references environment variables:
- `$VM_PUBLIC_IP` instead of actual IP
- `$ADCM_USERNAME` and `$ADCM_PASSWORD` instead of credentials
- etc.

## Security Notes

- Never commit `config.env` to git
- The `secrets/` directory is added to `.gitignore`
- Only `config.env.example` should be in version control
- Rotate passwords regularly
- Use strong, unique passwords for each service
