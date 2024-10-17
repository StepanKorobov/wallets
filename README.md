# wallets
REST wallets

####
# ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi)

## Установка

1. Клонируйте или скачайте репозиторий с gitlab/github
2. В случае первого запуска приложения, нужно выполнить команду `docker-compose run --rm postgresql` после появления надписи `database system is ready to accept connections` нажать сочетания клавиш`CTRL + C`, приступить к 3-му пункту
3. Введите команду `docker compose up -d` из папки с проектом

# Настройка

Нужно создать файл .env в корне проекта.

Указать переменные окружения для настройки базы данных.

*Пример:*
```bash
# Настройки для основной базы данных
# Имя пользователя БД
DB_USER = "admin"
# Пароль от БД
DB_PASSWORD = "admin"
# Хост от БД
DB_HOST = database
# Порт от БД
DB_PORT = 5432
# Имя БД
DB_NAME = "twitter"


# Настройки для тестовой базы дынных
# Имя пользователя БД
TEST_DB_USER = "test_user"
# Пароль от БД
TEST_DB_PASSWORD = "test_password"
# Хост от БД
TEST_DB_HOST = 127.0.0.1
# Порт от БД
TEST_DB_PORT = 6000
# Имя БД
TEST_DB_NAME = "test"
```

## Endpoints

**Более подробная документация описана при помощи swagger, её можно посмотреть после запуска проекта: (ip сервера:8000/docs)**
1) Endpoint для получения баланса кошелька:
   - Method: GET 
   - Rout: api/v1/wallets/{WALLET_UUID}
2) Endpoint для операций с кошельком (положить на счёт, снять со счёта).
    - Method: POST
    - Rout: api/v1/wallets/<WALLET_UUID>/operation
    - data:
      - type: JSON
      - { operationType: DEPOSIT or WITHDRAW, amount: 1000 }

## Тестирование
**В проекте содержаться тесты, они нужны для тестирования работоспособности всех Эндпоинтов.**

*Для запуска понадобится:*
1) Установить необходимые библиотеки командой `pip install -r requarements_test.txt`.
2) Запустить тестовую базу данных командой `docker run --name testing_database --rm -e POSTGRES_USER=test_user -e POSTGRES_PASSWORD=test_password -e POSTGRES_DB=test -p 6000:5432 -it postgres`
3) Запустить тесты командой `pytest -v test/`

*Примечание к пункту 2 (в случае применения других настроек в .env):*
   - -e POSTGRES_USER=(нужно указать значение TEST_DB_USER из .env)
   - -e POSTGRES_PASSWORD=(нужно указать значение TEST_DB_PASSWORD из .env)
   - -e POSTGRES_DB=(нужно указать значение TEST_DB_NAME из .env)
   - -p (нужно указать значение TEST_DB_PORT из .env):5432

