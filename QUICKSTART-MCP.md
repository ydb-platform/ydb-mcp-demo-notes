# YDB MCP Quick Start Guide

This guide shows how to quickly set up and use the YDB MCP (Model Context Protocol) server with Cursor IDE.

## Prerequisites

- Docker and Docker Compose installed
- Cursor IDE with MCP support

## Quick Setup

1. **Clone or download this project**

2. **Choose your YDB configuration:**

   **For local development (localhost):**
   - **Option 1 (Easiest):** No configuration needed! The system automatically uses localhost defaults when no `ydb.env` file is present
   - **Option 2:** Copy the template: `cp ydb-template.env ydb.env` (already configured for localhost)
   - **Option 3:** Use the example: `cp "ydb copy.env" ydb.env`

   **For Yandex Cloud YDB:**
   - Copy the template: `cp ydb-template.env ydb.env`
   - Edit `ydb.env` with your Yandex Cloud settings (see comments in the file)
   - Make sure you have `authorized_key.json` in the project root (for service account auth)

3. **Add MCP server to Cursor:**
   
   Copy the contents of `.cursor/mcp.json` to your Cursor MCP settings, or copy the file to your Cursor configuration directory.

4. **Start using MCP in Cursor:**
   
   The MCP server will automatically start when Cursor connects to it. Configuration is handled automatically:
   - **With `ydb.env` file:** Uses settings from the file
   - **Without `ydb.env` file:** Uses localhost defaults with anonymous authentication

## Configuration Files

- **`ydb.env`** - Main configuration file for YDB connection and authentication
- **`ydb-template.env`** - Template file with examples for both localhost and cloud configurations
- **`.cursor/mcp.json`** - Cursor MCP server configuration
- **`docker-compose.yml`** - Docker services configuration
- **`localhost.env`** - Example configuration for local YDB (same as "ydb copy.env")

## Switching Between Configurations

To switch between different YDB instances:

1. **For localhost (three options):**
   ```bash
   # Option 1: Remove config file (automatic localhost defaults)
   rm ydb.env
   docker compose up -d ydb  # Start local YDB if needed
   
   # Option 2: Use template (recommended)
   cp ydb-template.env ydb.env
   docker compose up -d ydb  # Start local YDB if needed
   
   # Option 3: Use existing example
   cp localhost.env ydb.env
   docker compose up -d ydb  # Start local YDB if needed
   ```

2. **For Yandex Cloud:**
   ```bash
   # Restore your cloud configuration
   # Make sure ydb.env contains your cloud settings
   # Make sure authorized_key.json is available
   ```

3. **Restart MCP in Cursor** (disconnect and reconnect MCP server)

## Simple Command

The MCP command in Cursor is now simplified to:
```
docker compose run --rm ydb-mcp
```

All configuration is handled through:
- Environment variables in `ydb.env`
- Docker Compose configuration
- No manual parameter passing needed

## Troubleshooting

1. **Check YDB connection:**
   ```bash
   docker compose run --rm ydb-mcp python -c "import os; print('YDB_ENDPOINT:', os.getenv('YDB_ENDPOINT'))"
   ```

2. **View MCP logs:**
   ```bash
   docker compose logs ydb-mcp
   ```

3. **Test connection without MCP:**
   ```bash
   docker compose run --rm notes-app python notes.py
   ```

## What's Different Now

✅ **Before (complex):**
- Hard-coded localhost defaults in Dockerfile
- Complex command with multiple parameters in mcp.json
- Manual environment setup required
- Always needed configuration file

✅ **After (simple):**
- **Smart defaults:** Works out-of-the-box with localhost when no config file present
- **Flexible configuration:** Use `ydb.env` file for custom settings
- Simple `docker compose run --rm ydb-mcp` command
- Automatic environment loading and fallback
- Easy switching between configurations

## Default Behavior

| Scenario | YDB Endpoint | Database | Authentication |
|----------|-------------|----------|----------------|
| **No `ydb.env` file** | `grpc://localhost:2136` | `/local` | Anonymous |
| **With `ydb.env` file** | From file | From file | From file |

This means you can start using MCP immediately without any configuration!
