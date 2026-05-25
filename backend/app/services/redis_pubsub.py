import asyncio
import json
import logging
from typing import Any, AsyncIterator

import redis.asyncio as aioredis

from app.core.config import settings

logger = logging.getLogger(__name__)

HEARTBEAT_INTERVAL = 15.0


def channel_name(batch_id: int) -> str:
    return f"batch:{batch_id}:events"


async def publish(batch_id: int, event: dict[str, Any]) -> None:
    """Публикует событие в канал батча. Вызывается из Celery-воркера."""
    client = aioredis.from_url(settings.redis_url)
    try:
        await client.publish(channel_name(batch_id), json.dumps(event, ensure_ascii=False))
    except Exception:
        logger.exception("Ошибка публикации события batch_id=%s event=%s", batch_id, event)
    finally:
        await client.aclose()


async def stream_batch_events(batch_id: int) -> AsyncIterator[dict[str, Any]]:
    """
    Подписывается на канал батча и возвращает события.
    Завершается при получении события типа 'batch_done' или при отмене задачи.
    Каждые HEARTBEAT_INTERVAL секунд без событий возвращает {'type': 'ping'}.
    """
    client = aioredis.from_url(settings.redis_url)
    pubsub = client.pubsub()
    await pubsub.subscribe(channel_name(batch_id))
    try:
        while True:
            try:
                message = await asyncio.wait_for(
                    pubsub.get_message(ignore_subscribe_messages=True),
                    timeout=HEARTBEAT_INTERVAL,
                )
            except asyncio.TimeoutError:
                yield {"type": "ping"}
                continue

            if message is None:
                await asyncio.sleep(0.05)
                continue

            event: dict[str, Any] = json.loads(message["data"])
            yield event

            if event.get("type") == "batch_done":
                break
    finally:
        await pubsub.unsubscribe(channel_name(batch_id))
        await client.aclose()
