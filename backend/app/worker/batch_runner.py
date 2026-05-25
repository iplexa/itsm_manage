from app.core.celery import celery_app


@celery_app.task(name="app.worker.batch_runner.ping")
def ping() -> str:
    return "pong"
