import logging
from datetime import date, datetime, time
from http.cookies import SimpleCookie
from typing import Any
from urllib.parse import urlparse

import httpx

from app.core.config import Settings, settings
from app.db.models import BatchTask
from app.services.service_codes import get_itsm_service_mapping

logger = logging.getLogger(__name__)

DEFAULT_ASSIGNMENT_GROUP = "173822703391995789"
DEFAULT_CALLER = "173148413796748031"
DEFAULT_COMPANY = "170853763708902887"
DEFAULT_TYPE_WORK = "173865532591825881"
DEFAULT_CLOSURE_CODE = "2"
DEFAULT_CREATE_STATE = "2"
DEFAULT_CLOSED_STATE = "7"


class ITSMClientError(Exception):
    pass


class ITSMConfigurationError(ITSMClientError):
    pass


class ITSMRequestError(ITSMClientError):
    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class ITSMResponseError(ITSMClientError):
    pass


class ITSMClient:
    def __init__(
        self,
        app_settings: Settings = settings,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = app_settings
        self.base_url = app_settings.itsm_base_url.rstrip("/")
        self._provided_http_client = http_client

    async def create_request(self, task: BatchTask) -> str:
        mapping = get_itsm_service_mapping(task.service)
        assigned_user = self._assigned_user()
        logger.info("Создание ITSM-заявки для task_id=%s service=%s", task.id, task.service)

        payload = {
            "record": {
                "state": DEFAULT_CREATE_STATE,
                "priority": "1",
                "resubmission": "",
                "external_company": "",
                "external_task": "",
                "assignment_group": DEFAULT_ASSIGNMENT_GROUP,
                "assigned_user": assigned_user,
                "subject": task.name,
                "description": task.desc,
                "related_cis": "",
                "caller": DEFAULT_CALLER,
                "company": DEFAULT_COMPANY,
                "contact_type": "30",
                "tag": "",
                "service": mapping.service,
                "service_2nd_level": mapping.service_2nd_level,
                "service_3rd_level": mapping.service_3rd_level,
                "service_4th_level": mapping.service_4th_level,
                "link_task": "https://tracker.yandex.ru/",
                "admissions_committee": 0,
                "attention_required": 0,
                "task_confidentiality": 0,
                "first_line_task": 0,
                "processed_ai_cb": 0,
                "faq_article": "",
                "additional_comments": "",
                "work_notes": "",
                "basic_service": mapping.basic_service,
                "followers_list": "",
                "admin_closure": None,
                "related_request_model": "",
                "request_template": "",
                "slave_request": "",
                "solved_by_changes": "",
                "related_problems": "",
                "level_of_dependency": None,
                "master_request": "",
                "related_inquiry": "",
                "related_incident": "",
                "glpi_link": "",
                "closure_code": None,
                "closure_notes": "",
                "performer_note": "",
                "manager_note": "",
                "service_manager_satisfaction": None,
                "service_satisfaction": None,
                "resolved_by": "",
                "resolved_at": "",
                "predicted_group": "",
                "predicted_service": "",
                "predicted_group_icl": "",
                "predicted_service_icl": "",
            },
            "attachments": [],
            "rem_attributes": [],
        }

        response_data = await self._request_json("PUT", "record/itsm_request", json=payload)
        request_id = extract_request_id(response_data)
        if request_id is None:
            raise ITSMResponseError("ITSM API не вернул record_id при создании заявки")

        logger.info("ITSM-заявка создана request_id=%s task_id=%s", request_id, task.id)
        return request_id

    async def assign_request(self, request_id: str, assigned_user: str | None = None) -> None:
        user_id = assigned_user or self._assigned_user()
        logger.info("Назначение ITSM-заявки request_id=%s", request_id)
        await self._request_json(
            "POST",
            self._record_endpoint(request_id),
            json={
                "record": {
                    "state": DEFAULT_CREATE_STATE,
                    "assigned_user": user_id,
                },
                "rem_attributes": [],
            },
        )

    async def log_time(self, request_id: str, minutes: int, comment: str) -> None:
        if minutes <= 0:
            raise ValueError("minutes должен быть больше 0")

        logger.info("Списание времени ITSM-заявки request_id=%s minutes=%s", request_id, minutes)
        await self._request_json(
            "POST",
            "widget/run-server-script/172682807793900660",
            json=build_log_time_payload(
                request_id=request_id,
                minutes=minutes,
                comment=comment,
                user_id=self._assigned_user(),
            ),
        )

    async def close_request(
        self,
        request_id: str,
        closure_text: str,
        closure_date: datetime | None = None,
    ) -> None:
        logger.info("Закрытие ITSM-заявки request_id=%s", request_id)
        payload: dict[str, Any] = {
            "record": {
                "state": DEFAULT_CLOSED_STATE,
                "closure_code": DEFAULT_CLOSURE_CODE,
                "closure_notes": closure_text,
            },
            "rem_attributes": [],
        }
        if closure_date is not None:
            payload["record"]["resolved_at"] = closure_date.strftime("%Y-%m-%d %H:%M:%S")

        await self._request_json("POST", self._record_endpoint(request_id), json=payload)

    async def fetch_request_by_link(self, link: str) -> dict[str, Any]:
        request_id = extract_request_id_from_link(link)
        if request_id is None:
            raise ITSMResponseError("Не удалось извлечь ID заявки из ссылки")

        logger.info("Получение ITSM-заявки по ссылке request_id=%s", request_id)
        response_data = await self._request_json("GET", f"record/itsm_request/{request_id}")
        if not isinstance(response_data, dict):
            raise ITSMResponseError("ITSM API вернул неожиданный формат заявки")
        return response_data

    async def _request_json(self, method: str, endpoint: str, **kwargs: Any) -> Any:
        kwargs.setdefault("headers", self._headers())
        client = self._provided_http_client
        if client is not None:
            try:
                response = await client.request(method, self._url(endpoint), **kwargs)
            except httpx.RequestError as error:
                raise ITSMRequestError("Ошибка соединения с ITSM API") from error
            return self._handle_response(response)

        async with httpx.AsyncClient(timeout=30) as session:
            try:
                response = await session.request(method, self._url(endpoint), **kwargs)
            except httpx.RequestError as error:
                raise ITSMRequestError("Ошибка соединения с ITSM API") from error
            return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> Any:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            raise ITSMRequestError(
                f"ITSM API вернул HTTP {response.status_code}",
                status_code=response.status_code,
            ) from error

        if not response.content:
            return {}

        try:
            return response.json()
        except ValueError as error:
            raise ITSMResponseError("ITSM API вернул невалидный JSON") from error

    def _headers(self) -> dict[str, str]:
        bearer_token = self.settings.bearer_token
        if not bearer_token:
            raise ITSMConfigurationError("BEARER_TOKEN не задан")

        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        }
        cookies = parse_cookies(self.settings.cookies)
        if cookies:
            headers["Cookie"] = "; ".join(f"{key}={value}" for key, value in cookies.items())
        return headers

    def _assigned_user(self) -> str:
        if not self.settings.assigned_user:
            raise ITSMConfigurationError("ASSIGNED_USER не задан")
        return self.settings.assigned_user

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    @staticmethod
    def _record_endpoint(request_id: str) -> str:
        return (
            f"record/itsm_request/{request_id}"
            "?form_id=&form_view=Default&open_first_rel_list=0&is_service_portal=0"
        )


def parse_cookies(raw_cookies: str | None) -> dict[str, str]:
    if not raw_cookies:
        return {}

    cookie = SimpleCookie()
    cookie.load(raw_cookies)
    return {key: morsel.value for key, morsel in cookie.items()}


def extract_request_id(response_data: Any) -> str | None:
    if not isinstance(response_data, dict):
        return None

    data = response_data.get("data")
    if isinstance(data, dict) and data.get("record_id"):
        return str(data["record_id"])

    for key in ("id", "record_id", "sys_id"):
        value = response_data.get(key)
        if value:
            return str(value)

    record = response_data.get("record")
    if isinstance(record, dict):
        for key in ("id", "record_id", "sys_id"):
            value = record.get(key)
            if value:
                return str(value)

    if isinstance(record, list) and record:
        first_record = record[0]
        if isinstance(first_record, dict):
            for key in ("id", "record_id", "sys_id"):
                value = first_record.get(key)
                if value:
                    return str(value)

    return None


def extract_request_id_from_link(link: str) -> str | None:
    parsed = urlparse(link)
    parts = [part for part in parsed.path.split("/") if part]
    if parts:
        candidate = parts[-1]
        if candidate.isdigit():
            return candidate

    return None


def build_log_time_payload(
    *,
    request_id: str,
    minutes: int,
    comment: str,
    user_id: str,
    work_date: date | None = None,
    type_work: str = DEFAULT_TYPE_WORK,
) -> dict[str, Any]:
    time_spent_ms = minutes * 60 * 1000
    time_spent_hours = minutes / 60
    current_datetime = format_work_datetime(work_date)

    return {
        "description": comment,
        "closure_code": DEFAULT_CLOSURE_CODE,
        "quick-type": "default",
        "tableName": "itsm_request",
        "recordId": request_id,
        "isVisible": True,
        "isShowModal": True,
        "userId": user_id,
        "taskId": request_id,
        "status": DEFAULT_CLOSED_STATE,
        "action": "saveAndClose",
        "isLocked": False,
        "isLockedButton": False,
        "translations": {
            "specifyingTimeSpent": "Списание трудозатрат",
            "specifyingTimeSpentText": "Укажите время, затраченное на выполнение задачи за текущий день",
            "timeSpentIsSaved": "Трудозатраты списаны",
            "comment": "Комментарий",
            "save": "Сохранить",
            "cancel": "Отменить",
            "time": "Время",
        },
        "condition_work": (
            "((groups_idsHAS171034687395428925^ORgroups_idsHAS173822703391995789"
            "^ORgroups_idsISEMPTY)^category=type^nameNOTLIKEАРХИВ^state=active)"
        ),
        "currentAllTimeSpentInit": 0,
        "datetime": current_datetime,
        "one_typework": type_work,
        "display_name_typework": "По умолчанию",
        "headerTitle": "Быстрые ответы",
        "searchStringLabel": "Поиск",
        "favoriteHeaderTitle": "Избранное",
        "categoriesHeaderTitle": "Категории",
        "emptySearchResult": "Ничего не найдено",
        "tableID": "156950616617772294",
        "userID": user_id,
        "isVisibleMainButton": True,
        "default_store": {
            "quickResponses": [],
            "categories": [],
            "favoriteIds": [],
        },
        "closure_notes_store": {
            "quickResponses": [],
            "categories": [],
            "favoriteIds": [],
        },
        "isShow": True,
        "type_work": {
            "database_value": type_work,
            "display_value": "По умолчанию",
        },
        "isVisibleBackButton": False,
        "areVisibleFavorites": False,
        "condition_typework": (
            "((groups_idsHAS171034687395428925^ORgroups_idsHAS173822703391995789"
            "^ORgroups_idsISEMPTY)^category=view^parentHAS173865532591825881^state=active)"
        ),
        "typework_count": 0,
        "open_typework": False,
        "view_work": {
            "database_value": "",
            "display_value": "",
        },
        "currentTimeSpent": time_spent_ms,
        "timeInt": str(time_spent_hours),
        "closingInfo": comment,
    }


def format_work_datetime(work_date: date | None = None) -> str:
    if work_date is not None:
        return datetime.combine(work_date, time(hour=13)).strftime("%Y-%m-%d %H:%M:%S")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
