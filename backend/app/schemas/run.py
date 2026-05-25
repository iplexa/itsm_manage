from pydantic import BaseModel


class BatchRunRequest(BaseModel):
    dry_run: bool = False
    stop_on_error: bool = True


class BatchRunResponse(BaseModel):
    status: str
    batch_id: int
