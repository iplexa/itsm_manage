from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.schemas.import_ import (
    LinksImportRequest,
    LinksImportResponse,
    TemplateImportRequest,
    TemplateImportResponse,
)
from app.services.deepseek import DeepSeekError, generate_tasks_from_requests
from app.services.itsm_client import ITSMClient, ITSMClientError
from app.services.templates import TemplateError, generate_tasks

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/template", response_model=TemplateImportResponse)
async def import_template(payload: TemplateImportRequest) -> TemplateImportResponse:
    try:
        tasks = generate_tasks(payload.template, payload.params)
    except TemplateError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    return TemplateImportResponse(tasks=tasks)


@router.post("/links", response_model=LinksImportResponse)
async def import_links(payload: LinksImportRequest) -> LinksImportResponse:
    """
    Получает данные ITSM-заявок по ссылкам, отправляет в DeepSeek и возвращает список задач.
    """
    if not payload.links:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Список ссылок пуст")

    client = ITSMClient()
    request_data_list: list[dict[str, Any]] = []

    for link in payload.links:
        try:
            raw = await client.fetch_request_by_link(link)
            request_data_list.append(_parse_itsm_response(raw, link))
        except ITSMClientError as error:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Ошибка получения заявки {link}: {error}",
            ) from error

    try:
        tasks = await generate_tasks_from_requests(request_data_list)
    except DeepSeekError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(error)) from error

    return LinksImportResponse(tasks=tasks)


def _parse_itsm_response(data: dict[str, Any], link: str) -> dict[str, Any]:
    try:
        record = data.get("data") or {}
        return {
            "link": link,
            "record_id": record.get("record_id"),
            "subject": _display(record.get("subject")),
            "description": _display(record.get("description")),
            "caller": _display(record.get("caller")),
            "state": _display(record.get("state")),
            "service": _display(record.get("service")),
        }
    except Exception:
        return {"link": link, "raw": str(data)[:500]}


def _display(field: Any) -> str | None:
    if field is None:
        return None
    if isinstance(field, str):
        return field
    if isinstance(field, dict):
        return field.get("display_value") or field.get("value")
    return str(field)
