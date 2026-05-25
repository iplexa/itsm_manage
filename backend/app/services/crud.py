from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Batch, BatchStatus, BatchTask
from app.schemas.batch import BatchCreate, BatchUpdate
from app.schemas.task import TaskCreate, TaskUpdate


class NotFoundError(Exception):
    pass


class BatchIsRunningError(Exception):
    pass


async def list_batches(session: AsyncSession) -> list[tuple[Batch, int]]:
    stmt = (
        select(Batch, func.count(BatchTask.id).label("tasks_count"))
        .outerjoin(BatchTask)
        .group_by(Batch.id)
        .order_by(Batch.created_at.desc(), Batch.id.desc())
    )
    result = await session.execute(stmt)
    return [(batch, tasks_count) for batch, tasks_count in result.all()]


async def create_batch(session: AsyncSession, payload: BatchCreate) -> Batch:
    batch = Batch(name=payload.name)
    session.add(batch)
    await session.commit()
    await session.refresh(batch)
    return batch


async def get_batch(session: AsyncSession, batch_id: int, *, with_tasks: bool = False) -> Batch:
    stmt: Select[tuple[Batch]] = select(Batch).where(Batch.id == batch_id)
    if with_tasks:
        stmt = stmt.options(selectinload(Batch.tasks))

    result = await session.execute(stmt)
    batch = result.scalar_one_or_none()
    if batch is None:
        raise NotFoundError("Батч не найден")
    return batch


async def update_batch(session: AsyncSession, batch_id: int, payload: BatchUpdate) -> Batch:
    batch = await get_batch(session, batch_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(batch, field, value)

    await session.commit()
    await session.refresh(batch)
    return batch


async def delete_batch(session: AsyncSession, batch_id: int) -> None:
    batch = await get_batch(session, batch_id)
    await session.delete(batch)
    await session.commit()


async def list_tasks(session: AsyncSession, batch_id: int) -> list[BatchTask]:
    await get_batch(session, batch_id)
    stmt = (
        select(BatchTask)
        .where(BatchTask.batch_id == batch_id)
        .order_by(BatchTask.sort_order.asc(), BatchTask.id.asc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def create_task(session: AsyncSession, batch_id: int, payload: TaskCreate) -> BatchTask:
    batch = await get_batch(session, batch_id)
    ensure_batch_tasks_editable(batch)

    next_sort_order = await get_next_task_sort_order(session, batch_id)
    task = BatchTask(
        batch_id=batch_id,
        sort_order=next_sort_order,
        **payload.model_dump(),
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task(session: AsyncSession, batch_id: int, task_id: int) -> BatchTask:
    stmt = select(BatchTask).where(BatchTask.batch_id == batch_id, BatchTask.id == task_id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()
    if task is None:
        raise NotFoundError("Задача не найдена")
    return task


async def update_task(
    session: AsyncSession,
    batch_id: int,
    task_id: int,
    payload: TaskUpdate,
) -> BatchTask:
    batch = await get_batch(session, batch_id)
    ensure_batch_tasks_editable(batch)
    task = await get_task(session, batch_id, task_id)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, batch_id: int, task_id: int) -> None:
    batch = await get_batch(session, batch_id)
    ensure_batch_tasks_editable(batch)
    task = await get_task(session, batch_id, task_id)
    await session.delete(task)
    await session.commit()


async def get_next_task_sort_order(session: AsyncSession, batch_id: int) -> int:
    stmt = select(func.coalesce(func.max(BatchTask.sort_order), -1) + 1).where(
        BatchTask.batch_id == batch_id,
    )
    result = await session.execute(stmt)
    return int(result.scalar_one())


def ensure_batch_tasks_editable(batch: Batch) -> None:
    if batch.status == BatchStatus.running:
        raise BatchIsRunningError("Нельзя редактировать задачи батча во время выполнения")
