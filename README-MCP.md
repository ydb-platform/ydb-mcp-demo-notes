# YDB MCP Server Configuration

Этот проект настроен для использования YDB MCP сервера через Docker Compose с интеграцией в Cursor.

## Компоненты

### Docker Compose Services

1. **ydb** - YDB сервер
   - Порт gRPC: 2136
   - Порт Web UI: 8765
   - База данных: `/local`

2. **ydb-mcp** - MCP сервер для работы с YDB
   - Собирается из `Dockerfile.ydb-mcp`
   - Использует host network для подключения к YDB
   - Предустановленный пакет `ydb-mcp`

3. **notes-app** - Ваше приложение (опционально)

## Запуск

1. Первый запуск (сборка образа YDB MCP):
   ```bash
   docker-compose build ydb-mcp
   docker-compose up -d ydb ydb-mcp
   ```

2. Последующие запуски (используется кешированный образ):
   ```bash
   docker-compose up -d ydb ydb-mcp
   ```

3. Проверьте статус:
   ```bash
   docker-compose ps
   ```

4. Проверьте логи MCP сервера:
   ```bash
   docker-compose logs ydb-mcp
   ```

## Конфигурация Cursor

Файл `.cursor-settings` уже настроен для работы с MCP сервером. Cursor будет автоматически подключаться к YDB через MCP интерфейс.

### Возможности MCP сервера

- Выполнение SQL запросов к YDB
- Управление схемой базы данных
- Просмотр и изменение данных
- Получение метаинформации о таблицах

## Полезные команды

### Подключение к YDB напрямую
```bash
# Подключение к контейнеру YDB
docker exec -it ydb-local bash

# Использование YDB CLI внутри контейнера
ydb -e grpc://localhost:2136 -d /local scheme ls
```

### Подключение к MCP серверу
```bash
# Просмотр логов MCP сервера
docker-compose logs -f ydb-mcp

# Перезапуск MCP сервера
docker-compose restart ydb-mcp
```

## Web UI

YDB Web UI доступен по адресу: http://localhost:8765

## Переменные окружения

Основные переменные окружения настроены в `docker-compose.yml`:

- `YDB_ENDPOINT=grpc://localhost:2136` - Адрес YDB сервера (через host network)
- `YDB_DATABASE=/local` - Имя базы данных

## Особенности конфигурации

### Host Network
YDB MCP сервис использует `network_mode: host`, что позволяет:
- Подключаться к YDB по `localhost:2136`
- Избежать проблем с сетевой изоляцией Docker
- Упростить конфигурацию

### Кеширование образа
YDB MCP собирается из `Dockerfile.ydb-mcp`, который:
- Устанавливает `ydb-mcp` через pip
- Кеширует установку для быстрых последующих запусков
- Не требует переустановки при каждом запуске контейнера

## Troubleshooting

1. **MCP сервер не запускается**:
   - Проверьте, что YDB сервер запущен и доступен
   - Проверьте логи: `docker-compose logs ydb-mcp`

2. **Cursor не подключается к MCP**:
   - Убедитесь, что MCP сервер запущен
   - Проверьте конфигурацию в `.cursor-settings`
   - Перезапустите Cursor

3. **Проблемы с подключением к YDB**:
   - Проверьте, что порты не заняты другими процессами
   - Убедитесь, что база данных `/local` создана
