#!/bin/bash
# Скрипт для загрузки переменных окружения YDB из ydb.env файла
# Использование: source load_ydb_env.sh

# Путь к файлу конфигурации
YDB_ENV_FILE="${YDB_ENV_FILE:-ydb.env}"

if [ -f "$YDB_ENV_FILE" ]; then
    echo "Загружаем конфигурацию YDB из $YDB_ENV_FILE..."
    
    # Загружаем переменные, игнорируя комментарии и пустые строки
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Пропускаем комментарии и пустые строки
        if [[ ! "$line" =~ ^[[:space:]]*# ]] && [[ -n "$line" ]]; then
            # Убираем пробелы в начале и конце
            line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            # Экспортируем переменную
            if [[ "$line" =~ ^[A-Za-z_][A-Za-z0-9_]*= ]]; then
                export "$line"
                echo "  ✓ $(echo "$line" | cut -d= -f1)"
            fi
        fi
    done < "$YDB_ENV_FILE"
    
    echo "Конфигурация YDB загружена успешно!"
    echo "YDB_ENDPOINT: $YDB_ENDPOINT"
    echo "YDB_DATABASE: $YDB_DATABASE"
    echo "AUTH_MODE: $AUTH_MODE"
else
    echo "⚠️  Файл конфигурации $YDB_ENV_FILE не найден"
    echo "Используются значения по умолчанию:"
    export YDB_ENDPOINT="${YDB_ENDPOINT:-grpc://localhost:2136}"
    export YDB_DATABASE="${YDB_DATABASE:-/local}"
    export AUTH_MODE="${AUTH_MODE:-anonymous}"
fi
