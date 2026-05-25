# ITSM Manage

Веб-приложение для пакетного создания, назначения, логирования времени и закрытия задач в ITSM.

Сейчас реализована Фаза 1: инфраструктурный каркас, FastAPI endpoint `/health`, SQLAlchemy async, Alembic, модели `Batch` и `BatchTask`, PostgreSQL, Redis, Celery worker и минимальный frontend на Vite.

## Требования

- Docker
- Docker Compose

## Быстрый старт

```bash
cp .env.example .env
docker compose up --build
```

Backend будет доступен на `http://localhost:8000`.

Frontend будет доступен на `http://localhost:5173`.

PostgreSQL будет доступен на `localhost:5432`.

Redis будет доступен на `localhost:6379`.

## Проверка health endpoint

```bash
curl http://localhost:8000/health
```

Ожидаемый ответ:

```json
{"status":"ok"}
```

## Миграции

Миграции применяются автоматически при запуске backend-контейнера.

Ручной запуск миграций внутри backend-контейнера:

```bash
docker compose exec backend alembic upgrade head
```

## Переменные окружения

Пример конфигурации находится в `.env.example`.

Секреты, токены, cookies и API-ключи нужно хранить в локальном `.env`. Этот файл не должен попадать в git.

## Следующий этап

Фаза 2: CRUD API для батчей и задач.
