import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.services.templates import TemplateError, generate_tasks


class TemplatesServiceTest(unittest.TestCase):
    def test_vks_template_generates_three_tasks(self) -> None:
        tasks = generate_tasks(
            "vks",
            {
                "audience": "П/2 305",
                "date_start": "2026-03-05T19:00:00",
                "date_end": "2026-03-05T22:00:00",
            },
        )

        assert len(tasks) == 3
        assert tasks[0].service == "VKS_SERVICE"
        assert tasks[1].time_minutes == 180
        assert tasks[2].closure_text == "Оборудование демонтировано."

    def test_rooms_template_defaults_to_dismount_only(self) -> None:
        tasks = generate_tasks(
            "rooms1",
            {
                "audience": "П/2 305",
                "date_start": "2026-03-05T19:00:00",
                "date_end": "2026-03-05T22:00:00",
            },
        )

        assert len(tasks) == 1
        assert "Демонтаж" in tasks[0].name

    def test_unknown_template_raises_error(self) -> None:
        with self.assertRaises(TemplateError):
            generate_tasks("unknown", {})


class TemplatesRouteTest(unittest.TestCase):
    def test_import_template_endpoint(self) -> None:
        client = TestClient(app)
        response = client.post(
            "/api/import/template",
            json={
                "template": "mount",
                "params": {
                    "audience": "П/2 305",
                    "date_start": "2026-03-05T19:00:00",
                    "date_end": "2026-03-05T22:00:00",
                },
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert len(body["tasks"]) == 1
        assert body["tasks"][0]["service"] == "MOUNT_SERVICE"

    def test_import_template_validation_error(self) -> None:
        client = TestClient(app)
        response = client.post(
            "/api/import/template",
            json={"template": "unknown", "params": {}},
        )

        assert response.status_code == 400
