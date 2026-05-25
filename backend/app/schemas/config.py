from pydantic import BaseModel


class ConfigStatus(BaseModel):
    itsm_base_url_set: bool
    bearer_token_set: bool
    cookies_set: bool
    assigned_user_set: bool
    deepseek_api_key_set: bool
    database_url_set: bool
    redis_url_set: bool
