from typing import Any

from pydantic import BaseModel, Field

from app.schemas.task import TaskCreate


class TemplateImportRequest(BaseModel):
    template: str = Field(min_length=1)
    params: dict[str, Any] = Field(default_factory=dict)


class TemplateImportResponse(BaseModel):
    tasks: list[TaskCreate]
