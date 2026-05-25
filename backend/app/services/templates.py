from collections.abc import Callable
from datetime import datetime
from typing import Any

from app.schemas.task import TaskCreate
from app.services.service_codes import (
    EDU_SERVICE,
    IU_SERVICE,
    MODPC_SERVICE,
    MOUNT_SERVICE,
    REGWORKS_SERVICE,
    VKS_SERVICE,
)


class TemplateError(Exception):
    pass


TemplateFactory = Callable[[dict[str, Any]], list[TaskCreate]]


def generate_tasks(template: str, params: dict[str, Any]) -> list[TaskCreate]:
    factory = TEMPLATE_FACTORIES.get(template)
    if factory is None:
        raise TemplateError(f"Неизвестный шаблон: {template}")
    return factory(params)


def make_edu_support_tasks(
    audience: str,
    date_start: datetime,
    date_end: datetime,
    *,
    need_mount: bool = True,
    need_support: bool = False,
    need_dismount: bool = True,
    service: str = EDU_SERVICE,
) -> list[TaskCreate]:
    tasks: list[TaskCreate] = []

    if need_mount:
        tasks.append(
            TaskCreate(
                name=f"Подготовка оборудования в аудитории {audience}",
                desc=f"Подготовить оборудование для мероприятия в аудитории {audience}.",
                service=service,
                time_minutes=30,
                closure_text="Оборудование подготовлено.",
                closure_date=date_start,
            ),
        )

    if need_support:
        tasks.append(
            TaskCreate(
                name=f"Сопровождение мероприятия в аудитории {audience}",
                desc=f"Выполнить сопровождение мероприятия в аудитории {audience}.",
                service=service,
                time_minutes=max(30, int((date_end - date_start).total_seconds() // 60)),
                closure_text="Сопровождение проведено.",
                closure_date=date_end,
            ),
        )

    if need_dismount:
        tasks.append(
            TaskCreate(
                name=f"Демонтаж оборудования в аудитории {audience}",
                desc=f"Отключить и убрать оборудование после мероприятия в аудитории {audience}.",
                service=service,
                time_minutes=30,
                closure_text="Оборудование демонтировано.",
                closure_date=date_end,
            ),
        )

    return tasks


def make_vks_tasks(params: dict[str, Any]) -> list[TaskCreate]:
    audience, date_start, date_end = get_common_params(params)
    return make_edu_support_tasks(
        audience,
        date_start,
        date_end,
        need_mount=get_bool(params, "need_mount", True),
        need_support=get_bool(params, "need_support", True),
        need_dismount=get_bool(params, "need_dismount", True),
        service=VKS_SERVICE,
    )


def make_rooms_tasks(params: dict[str, Any]) -> list[TaskCreate]:
    audience, date_start, date_end = get_common_params(params)
    # TODO: перенести точную логику старых rooms1/rooms2 из tasks.py.
    # По правилу сопровождения по умолчанию создаём только финальный демонтаж.
    return make_edu_support_tasks(
        audience,
        date_start,
        date_end,
        need_mount=get_bool(params, "need_mount", False),
        need_support=get_bool(params, "need_support", False),
        need_dismount=get_bool(params, "need_dismount", True),
        service=EDU_SERVICE,
    )


def make_mount_tasks(params: dict[str, Any]) -> list[TaskCreate]:
    audience, date_start, _ = get_common_params(params)
    return [
        TaskCreate(
            name=f"Монтаж оборудования в аудитории {audience}",
            desc=f"Выполнить монтаж оборудования в аудитории {audience}.",
            service=MOUNT_SERVICE,
            time_minutes=get_int(params, "time_minutes", 30),
            closure_text="Монтаж оборудования выполнен.",
            closure_date=date_start,
        ),
    ]


def make_modpc_tasks(params: dict[str, Any]) -> list[TaskCreate]:
    audience, date_start, _ = get_common_params(params)
    return [
        TaskCreate(
            name=f"Модернизация ПК в аудитории {audience}",
            desc=f"Выполнить работы по модернизации ПК в аудитории {audience}.",
            service=MODPC_SERVICE,
            time_minutes=get_int(params, "time_minutes", 60),
            closure_text="Работы по модернизации ПК выполнены.",
            closure_date=date_start,
        ),
    ]


def make_regworks_tasks(params: dict[str, Any]) -> list[TaskCreate]:
    audience, date_start, _ = get_common_params(params)
    return [
        TaskCreate(
            name=f"Регламентные работы в аудитории {audience}",
            desc=f"Выполнить регламентные работы в аудитории {audience}.",
            service=REGWORKS_SERVICE,
            time_minutes=get_int(params, "time_minutes", 60),
            closure_text="Регламентные работы выполнены.",
            closure_date=date_start,
        ),
    ]


def make_iu_tasks(params: dict[str, Any]) -> list[TaskCreate]:
    audience, date_start, date_end = get_common_params(params)
    # TODO: уточнить реальный состав IU-шаблона и заменить базовую структуру.
    return make_edu_support_tasks(
        audience,
        date_start,
        date_end,
        need_mount=get_bool(params, "need_mount", True),
        need_support=get_bool(params, "need_support", True),
        need_dismount=get_bool(params, "need_dismount", True),
        service=IU_SERVICE,
    )


def get_common_params(params: dict[str, Any]) -> tuple[str, datetime, datetime]:
    audience = get_str(params, "audience")
    date_start = get_datetime(params, "date_start")
    date_end = get_datetime(params, "date_end")
    if date_end < date_start:
        raise TemplateError("date_end не может быть раньше date_start")
    return audience, date_start, date_end


def get_str(params: dict[str, Any], key: str) -> str:
    value = params.get(key)
    if not isinstance(value, str) or not value.strip():
        raise TemplateError(f"Параметр {key} обязателен")
    return value.strip()


def get_datetime(params: dict[str, Any], key: str) -> datetime:
    value = params.get(key)
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as error:
            raise TemplateError(f"Параметр {key} должен быть ISO datetime") from error
    raise TemplateError(f"Параметр {key} обязателен")


def get_bool(params: dict[str, Any], key: str, default: bool) -> bool:
    value = params.get(key, default)
    if isinstance(value, bool):
        return value
    raise TemplateError(f"Параметр {key} должен быть boolean")


def get_int(params: dict[str, Any], key: str, default: int) -> int:
    value = params.get(key, default)
    if isinstance(value, int) and value > 0:
        return value
    raise TemplateError(f"Параметр {key} должен быть положительным числом")


TEMPLATE_FACTORIES: dict[str, TemplateFactory] = {
    "rooms1": make_rooms_tasks,
    "rooms2": make_rooms_tasks,
    "iu_tasks": make_iu_tasks,
    "vks": make_vks_tasks,
    "mount": make_mount_tasks,
    "modpc": make_modpc_tasks,
    "regworks": make_regworks_tasks,
}
