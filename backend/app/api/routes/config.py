from fastapi import APIRouter

from app.core.config import settings
from app.schemas.config import ConfigStatus

router = APIRouter(prefix="/config", tags=["config"])


@router.get("", response_model=ConfigStatus)
async def get_config() -> ConfigStatus:
    """Возвращает статус конфигурации без раскрытия значений секретов."""
    return ConfigStatus(
        itsm_base_url_set=bool(settings.itsm_base_url),
        bearer_token_set=bool(settings.bearer_token),
        cookies_set=bool(settings.cookies),
        assigned_user_set=bool(settings.assigned_user),
        deepseek_api_key_set=bool(settings.deepseek_api_key),
        database_url_set=bool(settings.database_url),
        redis_url_set=bool(settings.redis_url),
    )
