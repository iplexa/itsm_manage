from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Batch, BatchStatus, BatchTask, BatchTaskStatus
from app.services.crud import BatchIsRunningError, NotFoundError


async def start_batch_run(session: AsyncSession, batch_id: int) -> Batch:
    batch = await get_batch_for_run(session, batch_id)
    if batch.status == BatchStatus.running:
        raise BatchIsRunningError("Батч уже выполняется")

    batch.status = BatchStatus.running
    batch.started_at = datetime.now(UTC)
    batch.finished_at = None
    batch.error = None

    tasks = await get_batch_tasks_for_run(session, batch_id)
    for task in tasks:
        task.status = BatchTaskStatus.pending
        task.error = None
        task.itsm_request_id = None

    await session.commit()
    await session.refresh(batch)
    return batch


async def get_batch_for_run(session: AsyncSession, batch_id: int) -> Batch:
    result = await session.execute(select(Batch).where(Batch.id == batch_id))
    batch = result.scalar_one_or_none()
    if batch is None:
        raise NotFoundError("Батч не найден")
    return batch


async def get_batch_tasks_for_run(session: AsyncSession, batch_id: int) -> list[BatchTask]:
    result = await session.execute(
        select(BatchTask)
        .where(BatchTask.batch_id == batch_id)
        .order_by(BatchTask.sort_order.asc(), BatchTask.id.asc()),
    )
    return list(result.scalars().all())
