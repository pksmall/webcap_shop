
# Запуск локальной разработки

Для разработки понадобиться `pytho3.8` или выше.

Создайте вируатуальную среду:
```bash
virtualenv -m python3 venv
```

Активируйте виратульную среду для разработки:
```bash
. ./venv/bin/activate
```

Скопируйте `.env.example` в `.env`. Отредактируйте на нужные вам параметры

Скопируйте `webcap_shop/local-exeample.py` в `webcap_shop/local.py`. Отредактируете с соотвествии вашему `.env` файлу.

Создайте базу даных, если выбрали `postgres`:
```bash
psql -h localhost -U postgres posgres
# create database webshopdb;
```

Запустите инсталяцию пакетов для запуска:
```bash
pip install -r requirements.txt
```

Запустите миграцию:
```bash
python manage.py migrate
```

Запустие проект:
```bash
python manage.py runserver 8000
```

Загрузите подготовленные данные для проекта:
```bash
python manage.py loaddata data_dump.json
```

Запустите тесты:
```bash
python manage.py test
```

# Продакшен или тест сервер через Docker

Скопируйте `.env.example` в `.env`. Отредактируйте на нужные вам параметры

Скопируйте `webcap_shop/local-exeample.py` в `webcap_shop/local.py`. Отредактируете с соотвествии вашему `.env` файлу.

Запуск проекта:
```bash
docker-compose up -d
```

Загрузка данных для проекта:
```bash
docker-compose exec backend python manage.py loaddata data_dump.json
```

