# YDB Configuration Template Guide

The `ydb-template.env` file provides a comprehensive template for configuring YDB connections in this project.

## Quick Start

### For localhost development:
```bash
cp ydb-template.env ydb.env
# Template is already configured for localhost - ready to use!
docker compose up -d ydb
```

### For Yandex Cloud:
```bash
cp ydb-template.env ydb.env
# Edit ydb.env with your cloud settings (see comments in the file)
# Place your service account key as authorized_key.json
```

### No configuration (easiest):
```bash
# No setup needed - automatically uses localhost defaults
docker compose run --rm ydb-mcp
```

## Template Features

The template includes:

- ✅ **Localhost configuration** (ready to use)
- ✅ **Yandex Cloud examples** (with placeholder values)
- ✅ **Multiple authentication methods** with examples
- ✅ **Detailed comments** explaining each option
- ✅ **Usage instructions** right in the file

## Authentication Methods Covered

1. **Anonymous** - For local development
2. **Service Account Key File** - For Yandex Cloud production
3. **Access Token** - For temporary access
4. **Metadata Service** - For Yandex Cloud Compute instances

## File Structure

```bash
# Configuration files:
ydb-template.env     # ← Template with examples (tracked in git)
ydb.env             # ← Your actual config (ignored by git)
authorized_key.json # ← Service account key (ignored by git)
```

This approach ensures:
- Examples are always available
- Personal configurations stay private
- Easy to get started
