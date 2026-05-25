from fastapi import APIRouter, HTTPException, status

from app.schemas.import_ import TemplateImportRequest, TemplateImportResponse
from app.services.templates import TemplateError, generate_tasks

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/template", response_model=TemplateImportResponse)
async def import_template(payload: TemplateImportRequest) -> TemplateImportResponse:
    try:
        tasks = generate_tasks(payload.template, payload.params)
    except TemplateError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    return TemplateImportResponse(tasks=tasks)
