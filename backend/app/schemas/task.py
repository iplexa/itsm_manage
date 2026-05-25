from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.db.models import BatchTaskStatus


class TaskBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    desc: str = Field(min_length=1)
    service: str = Field(min_length=1, max_length=100)
    time_minutes: int = Field(ge=1)
    closure_text: str = Field(min_length=1)
    closure_date: datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    desc: str | None = Field(default=None, min_length=1)
    service: str | None = Field(default=None, min_length=1, max_length=100)
    time_minutes: int | None = Field(default=None, ge=1)
    closure_text: str | None = Field(default=None, min_length=1)
    closure_date: datetime | None = None
    status: BatchTaskStatus | None = None
    itsm_request_id: str | None = Field(default=None, max_length=100)
    error: str | None = None
    sort_order: int | None = Field(default=None, ge=0)


class TaskRead(TaskBase):
    id: int
    batch_id: int
    status: BatchTaskStatus
    itsm_request_id: str | None
    error: str | None
    sort_order: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
