# ITSM Manage

Веб-приложение для пакетного создания, назначения, логирования времени и закрытия задач в ITSM.

Сейчас реализована Фаза 1: инфраструктурный каркас, FastAPI endpoint `/health`, SQLAlchemy async, Alembic, модели `Batch` и `BatchTask`, PostgreSQL, Redis, Celery worker и минимальный frontend на Vite.

Фаза 2 добавляет CRUD API для батчей и задач.

Фаза 3 добавляет async ITSM client service для создания, назначения, списания времени, закрытия и получения заявок из ITSM.

Фаза 4 добавляет генерацию задач из шаблонов через endpoint `POST /api/import/template`.

Фаза 5 добавляет запуск батча через Celery: `POST /api/batches/{batch_id}/run`.

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

## CRUD API

Батчи:

```http
GET /api/batches
POST /api/batches
GET /api/batches/{batch_id}
PATCH /api/batches/{batch_id}
DELETE /api/batches/{batch_id}
```

Задачи батча:

```http
GET /api/batches/{batch_id}/tasks
POST /api/batches/{batch_id}/tasks
PATCH /api/batches/{batch_id}/tasks/{task_id}
DELETE /api/batches/{batch_id}/tasks/{task_id}
```

Если батч находится в статусе `running`, изменение задач возвращает `409 Conflict`.

Запуск батча:

```http
POST /api/batches/{batch_id}/run
```

Ответ:

```json
{"status":"started","batch_id":1}
```

Endpoint переводит батч в `running`, задачи в `pending` и ставит Celery-задачу `run_batch`.

## Template import

```http
POST /api/import/template
```

Пример:

```json
{
  "template": "vks",
  "params": {
    "audience": "П/2 305",
    "date_start": "2026-03-05T19:00:00",
    "date_end": "2026-03-05T22:00:00"
  }
}
```

Поддерживаемые шаблоны: `rooms1`, `rooms2`, `iu_tasks`, `vks`, `mount`, `modpc`, `regworks`.

## Backend tests

```bash
docker compose run --rm --no-deps backend python -m unittest discover tests
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

Для сервера можно переопределить внешние порты контейнеров:

```env
BACKEND_PORT=18000
FRONTEND_PORT=15173
POSTGRES_PORT=15432
REDIS_PORT=16379
```

На сервере `mskvpn.ru` приложение разворачивается в `/opt/itsm_manage`.

Caddy настроен в `/opt/caddy-remnawave/Caddyfile`:

- `https://itsm.plxa.ru/` проксируется во frontend на `host.docker.internal:15173`;
- `https://itsm.plxa.ru/health`, `/api/*`, `/docs*`, `/openapi.json` проксируются в backend на `host.docker.internal:18000`.

## CI/CD

GitHub Actions workflow находится в `.github/workflows/ci-cd.yml`.

Для deploy на сервер нужны repository secrets:

- `DEPLOY_HOST` — хост сервера, например `mskvpn.ru`;
- `DEPLOY_USER` — пользователь SSH, например `root`;
- `DEPLOY_SSH_PRIVATE_KEY` — приватный SSH-ключ для подключения.

Опционально можно задать repository variable:

- `DEPLOY_PATH` — путь деплоя, по умолчанию `/opt/itsm_manage`.

## Следующий этап

Фаза 2: CRUD API для батчей и задач.
