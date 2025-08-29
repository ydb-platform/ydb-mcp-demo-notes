# Быстрый старт с унифицированной конфигурацией

## 🎯 Проблема решена

Теперь все компоненты (приложение `notes.py`, Docker-сервисы, MCP-сервер) используют **единую конфигурацию** из файла `ydb.env`.

## 📂 Что изменилось

### Создан центральный файл конфигурации `ydb.env`:
```bash
YDB_ENDPOINT=grpc://localhost:2136
YDB_DATABASE=/local
AUTH_MODE=anonymous
```

### Обновлены все компоненты:
- ✅ `notes.py` - автоматически загружает `ydb.env`
- ✅ `docker-compose.yml` - использует `env_file: ydb.env`
- ✅ `.cursor/mcp.json` - использует переменные окружения
- ✅ `Dockerfile.ydb-mcp` - принимает переменные из Docker Compose

## 🚀 Как использовать

### 1. Для локальной разработки (по умолчанию)
Просто запускайте как обычно - все компоненты подхватят настройки из `ydb.env`:

```bash
# Приложение
./venv/bin/python notes.py list

# Docker
docker-compose up -d ydb ydb-mcp
docker-compose run --rm notes-app list

# MCP в Cursor - работает автоматически
```

### 2. Для изменения конфигурации
Отредактируйте файл `ydb.env`:

```bash
# Для другого сервера
YDB_ENDPOINT=grpc://test-server:2136
YDB_DATABASE=/test

# Для аутентификации
AUTH_MODE=env
YDB_ACCESS_TOKEN_CREDENTIALS=your-token
```

### 3. Для временного переопределения
```bash
# Переопределить только endpoint
YDB_ENDPOINT=grpc://another-server:2136 ./venv/bin/python notes.py list

# Использовать другой файл конфигурации
YDB_ENV_FILE=ydb-prod.env ./venv/bin/python notes.py list
```

## 📋 Проверка конфигурации

### Проверить загруженные переменные:
```bash
source load_ydb_env.sh
```

### Проверить Docker Compose:
```bash
docker-compose config
```

### Проверить приложение:
```bash
./venv/bin/python notes.py list
# Выведет: "📂 Loading YDB configuration from ydb.env"
```

## 🔧 Файлы конфигурации

| Файл | Назначение |
|------|------------|
| `ydb.env` | Основная конфигурация (все параметры) |
| `README-CONFIG.md` | Подробное описание |
| `load_ydb_env.sh` | Скрипт для ручной загрузки переменных |
| `.cursor/mcp.json` | Конфигурация MCP для Cursor |

## ✅ Результат

Теперь достаточно изменить один файл `ydb.env`, и все компоненты системы (CLI приложение, Docker-контейнеры, MCP-сервер) будут использовать новые параметры подключения и аутентификации.

**Больше никакого дублирования конфигурации в разных местах!** 🎉
