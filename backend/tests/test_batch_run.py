import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.crud import BatchIsRunningError, NotFoundError


class BatchRunRouteTest(unittest.TestCase):
    def test_run_batch_endpoint_starts_celery_task(self) -> None:
        client = TestClient(app)

        with (
            patch(
                "app.api.routes.batches.start_batch_run",
                new=AsyncMock(return_value=SimpleNamespace(id=42)),
            ) as start_batch_run,
            patch("app.api.routes.batches.run_batch.delay") as delay,
        ):
            response = client.post("/api/batches/42/run")

        assert response.status_code == 200
        assert response.json() == {"status": "started", "batch_id": 42}
        start_batch_run.assert_awaited_once()
        delay.assert_called_once_with(42)

    def test_run_batch_endpoint_returns_404(self) -> None:
        client = TestClient(app)

        with patch(
            "app.api.routes.batches.start_batch_run",
            new=AsyncMock(side_effect=NotFoundError("Батч не найден")),
        ):
            response = client.post("/api/batches/404/run")

        assert response.status_code == 404

    def test_run_batch_endpoint_returns_409_for_running_batch(self) -> None:
        client = TestClient(app)

        with patch(
            "app.api.routes.batches.start_batch_run",
            new=AsyncMock(side_effect=BatchIsRunningError("Батч уже выполняется")),
        ):
            response = client.post("/api/batches/42/run")

        assert response.status_code == 409
