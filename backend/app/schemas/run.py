from pydantic import BaseModel


class BatchRunResponse(BaseModel):
    status: str
    batch_id: int
