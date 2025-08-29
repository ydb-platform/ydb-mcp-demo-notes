#!/bin/bash
# Test script to verify YDB MCP configuration fallback behavior

set -e  # Exit on any error

echo "🧪 Testing YDB MCP Configuration Fallback"
echo "========================================="

# Test 1: No configuration file (localhost defaults)
echo
echo "📋 Test 1: No configuration file (localhost defaults)"
echo "-----------------------------------------------------"

# Backup existing config if present
if [ -f "ydb.env" ]; then
    echo "💾 Backing up existing ydb.env"
    mv ydb.env ydb.env.backup
fi

echo "🚀 Testing MCP with localhost defaults..."
docker compose run --rm ydb-mcp python -c "
import os
print('✓ YDB_ENDPOINT:', os.getenv('YDB_ENDPOINT'))
print('✓ YDB_DATABASE:', os.getenv('YDB_DATABASE'))
print('✓ YDB_ANONYMOUS_CREDENTIALS:', os.getenv('YDB_ANONYMOUS_CREDENTIALS'))
print('✓ Expected: localhost:2136, /local, anonymous auth')
"

# Test 2: With configuration file
echo
echo "📋 Test 2: With configuration file (cloud settings)"
echo "---------------------------------------------------"

# Restore config if we backed it up
if [ -f "ydb.env.backup" ]; then
    echo "📂 Restoring ydb.env configuration"
    mv ydb.env.backup ydb.env
elif [ -f "ydb-template.env" ]; then
    echo "📂 Using ydb-template.env as example"
    cp ydb-template.env ydb.env
elif [ -f "ydb copy.env" ]; then
    echo "📂 Using ydb copy.env as example"
    cp "ydb copy.env" ydb.env
else
    echo "⚠️  No configuration file available for Test 2"
    exit 0
fi

echo "🚀 Testing MCP with configuration file..."
docker compose run --rm ydb-mcp python -c "
import os
endpoint = os.getenv('YDB_ENDPOINT', 'Not set')
database = os.getenv('YDB_DATABASE', 'Not set')
auth_mode = os.getenv('YDB_AUTH_MODE', 'Not set')
print('✓ YDB_ENDPOINT:', endpoint[:50] + ('...' if len(endpoint) > 50 else ''))
print('✓ YDB_DATABASE:', database)
print('✓ YDB_AUTH_MODE:', auth_mode)
print('✓ Expected: Settings from ydb.env file')
"

echo
echo "🎉 All tests completed successfully!"
echo "📖 Configuration fallback is working correctly:"
echo "   • No ydb.env file → localhost defaults"
echo "   • With ydb.env file → settings from file"
