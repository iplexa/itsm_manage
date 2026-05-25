import unittest
from datetime import date, datetime, timezone

import httpx

from app.core.config import Settings
from app.db.models import BatchTask
from app.services.itsm_client import (
    ITSMClient,
    build_log_time_payload,
    extract_request_id,
    extract_request_id_from_link,
    parse_cookies,
)


class ITSMClientHelpersTest(unittest.TestCase):
    def test_parse_cookies(self) -> None:
        assert parse_cookies("sid=abc; session=xyz") == {
            "sid": "abc",
            "session": "xyz",
        }

    def test_extract_request_id(self) -> None:
        assert extract_request_id({"data": {"record_id": "177"}}) == "177"
        assert extract_request_id({"record": {"id": "178"}}) == "178"
        assert extract_request_id({"record": [{"sys_id": "179"}]}) == "179"

    def test_extract_request_id_from_link(self) -> None:
        link = "https://help.ranepa.ru/record/itsm_request/177123?foo=bar"
        assert extract_request_id_from_link(link) == "177123"

    def test_build_log_time_payload(self) -> None:
        payload = build_log_time_payload(
            request_id="177",
            minutes=90,
            comment="Работы выполнены",
            user_id="user-1",
            work_date=date(2026, 3, 5),
        )

        assert payload["recordId"] == "177"
        assert payload["currentTimeSpent"] == 5_400_000
        assert payload["timeInt"] == "1.5"
        assert payload["datetime"] == "2026-03-05 13:00:00"
        assert payload["closingInfo"] == "Работы выполнены"


class ITSMClientAsyncTest(unittest.IsolatedAsyncioTestCase):
    async def test_create_assign_log_and_close(self) -> None:
        seen_requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen_requests.append(request)
            if request.method == "PUT" and request.url.path == "/record/itsm_request":
                return httpx.Response(200, json={"data": {"record_id": "177"}})
            if request.method == "POST" and request.url.path == "/record/itsm_request/177":
                return httpx.Response(200, json={"ok": True})
            if request.method == "POST" and request.url.path == "/widget/run-server-script/172682807793900660":
                return httpx.Response(200, json={"ok": True})
            return httpx.Response(404, json={"error": "not found"})

        settings = Settings(
            itsm_base_url="https://help.example.test",
            bearer_token="token",
            cookies="sid=abc",
            assigned_user="user-1",
        )
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
            client = ITSMClient(settings, http_client)
            task = BatchTask(
                id=10,
                name="Тестовая задача",
                desc="Описание",
                service="EDU_SERVICE",
                time_minutes=30,
                closure_text="Готово",
                closure_date=datetime(2026, 3, 5, 22, 0, tzinfo=timezone.utc),
                sort_order=0,
            )

            request_id = await client.create_request(task)
            await client.assign_request(request_id)
            await client.log_time(request_id, task.time_minutes, task.closure_text)
            await client.close_request(request_id, task.closure_text, task.closure_date)

        assert request_id == "177"
        assert [request.method for request in seen_requests] == ["PUT", "POST", "POST", "POST"]
        assert seen_requests[0].headers["authorization"] == "Bearer token"
        assert seen_requests[0].headers["cookie"] == "sid=abc"
