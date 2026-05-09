from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    amd_api_endpoint: str = "https://api.amd.com/v1"
    amd_api_key: Optional[str] = None
    model_name: str = "meta-llama/Llama-3.1-70B-Instruct"

    inmet_api_key: Optional[str] = None
    cepea_api_key: Optional[str] = None

    telegram_bot_token: Optional[str] = None
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_webhook_auth: Optional[str] = None

    redis_url: str = "redis://localhost:6379"
    chroma_persist_dir: str = "./knowledge/vectorstore"

    app_debug: bool = False
    log_level: str = "INFO"
    max_tokens: int = 2048
    temperature: float = 0.7

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()