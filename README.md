# Заключительное задание первого модуля

Ваша задача в этом уроке — загрузить данные в Elasticsearch из PostgreSQL. Подробности задания в папке `etl`.

**Запуск**

````
    docker-compose up -d
````

**Миграции**

````
    docker-compose exec app make migrate
````

**Создать админа**

````
    docker-compose exec app make createsuperuser
````