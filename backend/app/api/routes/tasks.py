from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services import crud

router = APIRouter(prefix="/batches/{batch_id}/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
async def list_tasks(
    batch_id: int,
    session: AsyncSession = Depends(get_session),
) -> list[TaskRead]:
    try:
        return await crud.list_tasks(session, batch_id)
    except crud.NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    batch_id: int,
    payload: TaskCreate,
    session: AsyncSession = Depends(get_session),
) -> TaskRead:
    try:
        return await crud.create_task(session, batch_id, payload)
    except crud.NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except crud.BatchIsRunningError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    batch_id: int,
    task_id: int,
    payload: TaskUpdate,
    session: AsyncSession = Depends(get_session),
) -> TaskRead:
    try:
        return await crud.update_task(session, batch_id, task_id, payload)
    except crud.NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except crud.BatchIsRunningError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    batch_id: int,
    task_id: int,
    session: AsyncSession = Depends(get_session),
) -> Response:
    try:
        await crud.delete_task(session, batch_id, task_id)
    except crud.NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except crud.BatchIsRunningError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{task_id}/retry", response_model=TaskRead)
async def retry_task(
    batch_id: int,
    task_id: int,
    session: AsyncSession = Depends(get_session),
) -> TaskRead:
    try:
        return await crud.retry_task(session, batch_id, task_id)
    except crud.NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.post("/{task_id}/skip", response_model=TaskRead)
async def skip_task(
    batch_id: int,
    task_id: int,
    session: AsyncSession = Depends(get_session),
) -> TaskRead:
    try:
        return await crud.skip_task(session, batch_id, task_id)
    except crud.NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
