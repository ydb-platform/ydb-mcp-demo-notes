# Унифицированная конфигурация YDB

Этот проект настроен для использования единых параметров подключения к YDB как для основного приложения `notes.py`, так и для MCP-сервера.

## Структура конфигурации

### Файл `ydb.env`

Центральный файл конфигурации, содержащий все параметры подключения к YDB:

```bash
# YDB Connection Parameters
YDB_ENDPOINT=grpc://localhost:2136
YDB_DATABASE=/local

# Authentication Configuration
# По умолчанию используется анонимная аутентификация для локальной разработки
# Для продакшена установите одну из следующих переменных:

# YDB_ACCESS_TOKEN_CREDENTIALS=your-access-token
# YDB_SERVICE_ACCOUNT_KEY_FILE_CREDENTIALS=/path/to/key/file.json
# YDB_ANONYMOUS_CREDENTIALS=1
# YDB_METADATA_CREDENTIALS=1

# Дополнительные настройки
# AUTH_MODE определяет режим аутентификации для notes.py
# anonymous - анонимная аутентификация (по умолчанию)
# env - аутентификация из переменных окружения
AUTH_MODE=anonymous
```

## Использование конфигурации

### 1. Приложение notes.py

Автоматически загружает конфигурацию из `ydb.env` при запуске:

```bash
# Использует настройки из ydb.env
python notes.py list

# Переопределить режим аутентификации
python notes.py --auth=env list

# Переопределить переменные окружения
YDB_ENDPOINT=grpc://remote-host:2136 python notes.py list
```

### 2. Docker Compose

Все сервисы используют `ydb.env` через директиву `env_file`:

```yaml
services:
  ydb-mcp:
    env_file:
      - ydb.env
  
  notes-app:
    env_file:
      - ydb.env
```

Запуск:

```bash
# Запуск с общей конфигурацией
docker-compose up -d ydb ydb-mcp

# Использование приложения
docker-compose run --rm notes-app list
```

### 3. MCP-сервер

Конфигурация MCP в `.cursor/mcp.json` использует переменные окружения:

```json
{
    "mcpServers": {
      "ydb": {
        "command": "docker",
        "args": ["exec", "-i", "ydb-mcp", "python", "-m", "ydb_mcp"],
        "env": {
          "YDB_ENDPOINT": "grpc://localhost:2136",
          "YDB_DATABASE": "/local"
        }
      }
    }
}
```

## Настройка для различных сред

### Локальная разработка

По умолчанию (файл `ydb.env`):
- YDB_ENDPOINT=grpc://localhost:2136
- YDB_DATABASE=/local
- AUTH_MODE=anonymous

### Продакшн с токен-аутентификацией

Обновите `ydb.env`:

```bash
YDB_ENDPOINT=grpc://prod-ydb-host:2136
YDB_DATABASE=/production/database
AUTH_MODE=env
YDB_ACCESS_TOKEN_CREDENTIALS=your-production-token
```

### Продакшн с Service Account

Обновите `ydb.env`:

```bash
YDB_ENDPOINT=grpc://prod-ydb-host:2136
YDB_DATABASE=/production/database  
AUTH_MODE=env
YDB_SERVICE_ACCOUNT_KEY_FILE_CREDENTIALS=/path/to/sa-key.json
```

## Загрузка переменных из файла

### Скрипт load_ydb_env.sh

Для ручной загрузки переменных:

```bash
# Загрузить переменные в текущую сессию
source load_ydb_env.sh

# Проверить загруженные переменные
echo $YDB_ENDPOINT
echo $YDB_DATABASE
```

### Автоматическая загрузка в notes.py

Приложение автоматически загружает `ydb.env` при старте. Приоритет переменных:

1. Переменные окружения (высший приоритет)
2. Переменные из `ydb.env`
3. Значения по умолчанию

## Переопределение параметров

### Временное переопределение

```bash
# Переопределить endpoint для одной команды
YDB_ENDPOINT=grpc://test-server:2136 python notes.py list

# Переопределить несколько параметров
YDB_ENDPOINT=grpc://test-server:2136 YDB_DATABASE=/test python notes.py init
```

### Использование альтернативного файла конфигурации

```bash
# Использовать другой файл конфигурации
YDB_ENV_FILE=ydb-production.env python notes.py list

# Скопировать и модифицировать конфигурацию
cp ydb.env ydb-test.env
# ... отредактировать ydb-test.env ...
YDB_ENV_FILE=ydb-test.env python notes.py list
```

## Проверка конфигурации

### Проверка загруженных параметров

```bash
# Приложение покажет используемые параметры
python notes.py list

# Вывод будет включать:
# 📂 Loading YDB configuration from ydb.env
# ✅ Connected to YDB at grpc://localhost:2136
# ℹ️  Using authentication mode: anonymous
```

### Проверка MCP сервера

```bash
# Проверить статус контейнера MCP
docker-compose ps ydb-mcp

# Проверить логи MCP сервера
docker-compose logs ydb-mcp
```

## Устранение проблем

### MCP-сервер не подключается

1. Проверьте статус контейнеров:
   ```bash
   docker-compose ps
   ```

2. Пересоберите MCP контейнер:
   ```bash
   docker-compose build ydb-mcp
   docker-compose up -d ydb-mcp
   ```

3. Проверьте логи:
   ```bash
   docker-compose logs ydb-mcp
   ```

### Приложение не видит конфигурацию

1. Убедитесь, что файл `ydb.env` существует в корне проекта
2. Проверьте права доступа к файлу
3. Убедитесь, что переменные не переопределены в окружении

### Ошибки аутентификации

1. Проверьте правильность AUTH_MODE в `ydb.env`
2. Убедитесь, что переменные аутентификации установлены корректно
3. Для продакшена используйте `AUTH_MODE=env` и соответствующие YDB_*_CREDENTIALS переменные

## Миграция с жёстко заданных параметров

Если у вас есть жёстко заданные параметры в коде или конфигурациях:

1. Создайте файл `ydb.env` с текущими параметрами
2. Обновите docker-compose.yml для использования `env_file: - ydb.env`
3. Обновите `.cursor/mcp.json` для использования переменных окружения
4. Протестируйте работу всех компонентов

После этого все компоненты будут использовать единую конфигурацию из `ydb.env`.
