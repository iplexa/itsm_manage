import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.celery import celery_app
from app.db.models import Batch, BatchStatus, BatchTask, BatchTaskStatus
from app.db.session import async_session_maker
from app.services.itsm_client import ITSMClient
from app.services.redis_pubsub import publish

logger = logging.getLogger(__name__)


@celery_app.task(name="app.worker.batch_runner.ping")
def ping() -> str:
    return "pong"


@celery_app.task(name="app.worker.batch_runner.run_batch")
def run_batch(batch_id: int, stop_on_error: bool = True) -> dict[str, Any]:
    return asyncio.run(run_batch_async(batch_id, stop_on_error=stop_on_error))


async def run_batch_async(batch_id: int, *, stop_on_error: bool = True) -> dict[str, Any]:
    async with async_session_maker() as session:
        batch = await get_batch(session, batch_id)
        if batch is None:
            logger.warning("Батч не найден batch_id=%s", batch_id)
            return {"status": "not_found", "batch_id": batch_id}

        tasks = await get_batch_tasks(session, batch_id)
        if not tasks:
            batch.status = BatchStatus.done
            batch.finished_at = datetime.now(UTC)
            await session.commit()
            await publish(batch_id, {"type": "batch_done", "status": "done", "error": None})
            return {"status": "done", "batch_id": batch_id, "tasks": 0}

        client = ITSMClient()
        failed_count = 0

        for task in tasks:
            if task.status == BatchTaskStatus.skipped:
                continue

            await _set_task_status(session, task, BatchTaskStatus.running, error=None)
            await publish(batch_id, _task_event(task, BatchTaskStatus.running))

            try:
                request_id = await client.create_request(task)
                task.itsm_request_id = request_id
                await session.commit()

                await client.assign_request(request_id)
                await client.log_time(request_id, task.time_minutes, task.closure_text)
                await client.close_request(request_id, task.closure_text, task.closure_date)

                await _set_task_status(session, task, BatchTaskStatus.done, error=None)
                await publish(batch_id, _task_event(task, BatchTaskStatus.done))

            except Exception as error:  # noqa: BLE001
                failed_count += 1
                logger.exception("Ошибка выполнения task_id=%s batch_id=%s", task.id, batch_id)
                await _set_task_status(session, task, BatchTaskStatus.failed, error=str(error))
                await publish(batch_id, _task_event(task, BatchTaskStatus.failed, error=str(error)))

                if stop_on_error:
                    batch.status = BatchStatus.failed
                    batch.error = str(error)
                    batch.finished_at = datetime.now(UTC)
                    await session.commit()
                    await publish(batch_id, {"type": "batch_done", "status": "failed", "error": str(error)})
                    return {
                        "status": "failed",
                        "batch_id": batch_id,
                        "failed_tasks": failed_count,
                    }

        batch.status = BatchStatus.failed if failed_count else BatchStatus.done
        batch.error = "Часть задач завершилась с ошибками" if failed_count else None
        batch.finished_at = datetime.now(UTC)
        await session.commit()

        await publish(batch_id, {
            "type": "batch_done",
            "status": batch.status.value,
            "error": batch.error,
        })

        return {
            "status": batch.status.value,
            "batch_id": batch_id,
            "failed_tasks": failed_count,
        }


def _task_event(
    task: BatchTask,
    status: BatchTaskStatus,
    *,
    error: str | None = None,
) -> dict[str, Any]:
    return {
        "type": "task_update",
        "task_id": task.id,
        "name": task.name,
        "status": status.value,
        "itsm_request_id": task.itsm_request_id,
        "error": error,
    }


async def get_batch(session: AsyncSession, batch_id: int) -> Batch | None:
    result = await session.execute(select(Batch).where(Batch.id == batch_id))
    return result.scalar_one_or_none()


async def get_batch_tasks(session: AsyncSession, batch_id: int) -> list[BatchTask]:
    result = await session.execute(
        select(BatchTask)
        .where(BatchTask.batch_id == batch_id)
        .order_by(BatchTask.sort_order.asc(), BatchTask.id.asc()),
    )
    return list(result.scalars().all())


async def _set_task_status(
    session: AsyncSession,
    task: BatchTask,
    status: BatchTaskStatus,
    *,
    error: str | None,
) -> None:
    task.status = status
    task.error = error
    await session.commit()
