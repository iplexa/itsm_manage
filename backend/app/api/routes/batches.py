import json

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.db.models import BatchStatus
from app.db.session import get_session
from app.schemas.batch import BatchCreate, BatchDetail, BatchRead, BatchUpdate
from app.schemas.run import BatchRunResponse
from app.services import crud
from app.services.batch_run import start_batch_run
from app.services.redis_pubsub import stream_batch_events
from app.worker.batch_runner import run_batch

router = APIRouter(prefix="/batches", tags=["batches"])

_TERMINAL_STATUSES = {BatchStatus.done, BatchStatus.failed}


@router.get("", response_model=list[BatchRead])
async def list_batches(session: AsyncSession = Depends(get_session)) -> list[BatchRead]:
    batches = await crud.list_batches(session)
    return [to_batch_read(batch, tasks_count) for batch, tasks_count in batches]


@router.post("", response_model=BatchRead, status_code=status.HTTP_201_CREATED)
async def create_batch(
    payload: BatchCreate,
    session: AsyncSession = Depends(get_session),
) -> BatchRead:
    batch = await crud.create_batch(session, payload)
    return to_batch_read(batch)


@router.get("/{batch_id}", response_model=BatchDetail)
async def get_batch(
    batch_id: int,
    session: AsyncSession = Depends(get_session),
) -> BatchDetail:
    try:
        batch = await crud.get_batch(session, batch_id, with_tasks=True)
    except crud.NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    tasks = sorted(batch.tasks, key=lambda task: (task.sort_order, task.id))
    data = BatchDetail.model_validate(batch).model_dump()
    data["tasks"] = tasks
    data["tasks_count"] = len(tasks)
    return BatchDetail.model_validate(data)


@router.patch("/{batch_id}", response_model=BatchRead)
async def update_batch(
    batch_id: int,
    payload: BatchUpdate,
    session: AsyncSession = Depends(get_session),
) -> BatchRead:
    try:
        batch = await crud.update_batch(session, batch_id, payload)
    except crud.NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return to_batch_read(batch)


@router.delete("/{batch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_batch(
    batch_id: int,
    session: AsyncSession = Depends(get_session),
) -> Response:
    try:
        await crud.delete_batch(session, batch_id)
    except crud.NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{batch_id}/run", response_model=BatchRunResponse)
async def run_batch_endpoint(
    batch_id: int,
    session: AsyncSession = Depends(get_session),
) -> BatchRunResponse:
    try:
        batch = await start_batch_run(session, batch_id)
    except crud.NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except crud.BatchIsRunningError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error

    run_batch.delay(batch.id)
    return BatchRunResponse(status="started", batch_id=batch.id)


@router.get("/{batch_id}/stream")
async def stream_batch_progress(
    batch_id: int,
    session: AsyncSession = Depends(get_session),
) -> EventSourceResponse:
    """
    SSE-поток прогресса батча.

    События:
    - init        — начальное состояние батча (BatchDetail JSON)
    - task_update — изменение статуса задачи
    - batch_done  — батч завершён (done или failed)
    - ping        — heartbeat каждые 15 с без событий
    """
    try:
        batch = await crud.get_batch(session, batch_id, with_tasks=True)
    except crud.NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    tasks = sorted(batch.tasks, key=lambda t: (t.sort_order, t.id))
    init_data = BatchDetail.model_validate(batch).model_dump()
    init_data["tasks"] = [t.__dict__ for t in tasks]
    init_data["tasks_count"] = len(tasks)

    already_terminal = batch.status in _TERMINAL_STATUSES

    async def generate():
        yield {
            "event": "init",
            "data": json.dumps(init_data, default=str, ensure_ascii=False),
        }

        if already_terminal:
            return

        async for event in stream_batch_events(batch_id):
            event_type = event.get("type", "message")

            if event_type == "ping":
                yield {"event": "ping", "data": ""}
                continue

            yield {
                "event": event_type,
                "data": json.dumps(event, ensure_ascii=False),
            }

            if event_type == "batch_done":
                break

    return EventSourceResponse(generate())


def to_batch_read(batch: object, tasks_count: int = 0) -> BatchRead:
    data = BatchRead.model_validate(batch).model_dump()
    data["tasks_count"] = tasks_count
    return BatchRead.model_validate(data)
