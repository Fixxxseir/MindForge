# MindForge

MindForge – это гибкое и масштабируемое решение, которое делает онлайн-обучение доступным, увлекательным и эффективным для всех пользователей.

## Быстрый старт

### Предварительные требования
- Docker (версия 20.10.7+)
- Docker Compose (версия 1.29.2+)

## Запуск через Docker

1. Соберите и запустите контейнеры:
docker-compose up -d --build

*Флаг -d запускает в фоновом режиме*

2. После запуска приложение будет доступно:
- Основной интерфейс: http://localhost:8000
- Админ-панель: http://localhost:8000/admin

## Основные команды

### Управление контейнерами
- Просмотр всех контейнеров:
docker ps


- Вход в контейнер (замените CONTAINER_ID):
docker exec -it CONTAINER_ID bash


- Остановка всех контейнеров:
docker-compose down


### Тестирование
- Запуск тестов внутри контейнера:
docker-compose exec web python manage.py test


## Устранение неполадок

1. Если сервисы не запускаются:
docker-compose logs -f сервис # (web/db/redis/celery)


2. Полная пересборка:
docker-compose down -v && docker-compose up -d --build


# if 'test' in sys.argv:
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": 'django.db.backends.postgresql_psycopg2',
#             "NAME": os.getenv("DB_NAME", 'mindforge_db'),
#             "USER": os.getenv("DB_USER", 'postgres'),
#             "PASSWORD": os.getenv("DB_PASSWORD", 'postgres'),
#             "HOST": os.getenv("DB_HOST", 'localhost'),
#             "PORT": os.getenv("DB_PORT", '5432'),
#         }
#     }