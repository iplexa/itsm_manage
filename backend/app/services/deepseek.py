import json
import logging
from typing import Any

import httpx

from app.core.config import settings
from app.schemas.task import TaskCreate

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Ты — система обработки ITSM-заявок РАНХИГС.
Получаешь данные заявок из helpdesk. Задача — преобразовать их в список задач для учёта трудозатрат.

Доступные коды сервисов:
- EDU_SERVICE — сопровождение учебного процесса
- IU_SERVICE — сопровождение учебного процесса (ИУ: монтаж + сопровождение + демонтаж)
- VKS_SERVICE — ВКС (видеоконференцсвязь)
- MOUNT_SERVICE — монтаж/демонтаж оборудования
- MODPC_SERVICE — модернизация ПК
- REGWORKS_SERVICE — регламентные работы

Правила:
- Сопровождение мероприятий с оборудованием (ИУ) → 3 задачи: подготовка 30 мин + сопровождение (длительность) + демонтаж 30 мин, service=IU_SERVICE
- ВКС → 1–3 задачи по ситуации, service=VKS_SERVICE
- Регламентные работы → 1 задача 60 мин, service=REGWORKS_SERVICE
- Монтаж/демонтаж → 1–2 задачи по 30 мин, service=MOUNT_SERVICE
- closure_date — ISO datetime даты закрытия (если нет — null)
- closure_text — краткий текст в прошедшем времени («Оборудование подготовлено.»)

Верни строго JSON:
{"tasks": [{"name": "...", "desc": "...", "service": "...", "time_minutes": N, "closure_text": "...", "closure_date": "YYYY-MM-DDTHH:MM:SS или null"}]}"""


class DeepSeekError(Exception):
    pass


async def generate_tasks_from_requests(request_data_list: list[dict[str, Any]]) -> list[TaskCreate]:
    api_key = settings.deepseek_api_key
    if not api_key:
        raise DeepSeekError("DEEPSEEK_API_KEY не задан в конфигурации")

    user_content = "Данные заявок:\n" + json.dumps(request_data_list, ensure_ascii=False, indent=2)

    payload = {
        "model": settings.deepseek_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1,
    }

    logger.info("DeepSeek запрос для %d заявок", len(request_data_list))

    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(
                f"{settings.deepseek_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
        except httpx.RequestError as error:
            raise DeepSeekError(f"Ошибка соединения с DeepSeek API: {error}") from error
        except httpx.HTTPStatusError as error:
            raise DeepSeekError(f"DeepSeek API вернул HTTP {response.status_code}") from error

    result = response.json()
    content = result["choices"][0]["message"]["content"]

    try:
        data = json.loads(content)
        raw_tasks: list[dict[str, Any]] = data.get("tasks", [])
    except (json.JSONDecodeError, KeyError) as error:
        logger.error("Невалидный ответ DeepSeek: %s", content[:500])
        raise DeepSeekError(f"DeepSeek вернул невалидный JSON: {error}") from error

    tasks: list[TaskCreate] = []
    for raw in raw_tasks:
        try:
            closure_date = raw.get("closure_date")
            if not closure_date or closure_date == "null":
                closure_date = None
            tasks.append(
                TaskCreate(
                    name=str(raw["name"]),
                    desc=str(raw["desc"]),
                    service=str(raw["service"]),
                    time_minutes=int(raw["time_minutes"]),
                    closure_text=str(raw["closure_text"]),
                    closure_date=closure_date,
                )
            )
        except (KeyError, ValueError, TypeError) as error:
            logger.warning("Пропущена задача из ответа DeepSeek: %s — %s", raw, error)

    logger.info("DeepSeek сгенерировал %d задач", len(tasks))
    return tasks
