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
