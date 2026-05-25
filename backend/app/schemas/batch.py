from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.db.models import BatchStatus
from app.schemas.task import TaskRead


class BatchBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class BatchCreate(BatchBase):
    pass


class BatchUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    status: BatchStatus | None = None
    error: str | None = None


class BatchRead(BatchBase):
    id: int
    status: BatchStatus
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    error: str | None
    tasks_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class BatchDetail(BatchRead):
    tasks: list[TaskRead] = Field(default_factory=list)
