from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass(frozen=True)
class EnvConfig:
    telegram_bot_token: str
    data_dir: str
    log_level: str
    default_model: str
    max_context_messages: int

def load_env_config() -> EnvConfig:
    load_dotenv()
    
    token = getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    
    return EnvConfig(
        telegram_bot_token=token,
        data_dir=getenv("DATA_DIR", "data"),
        log_level=getenv("LOG_LEVEL", "INFO"),
        default_model=getenv("DEFAULT_MODEL", "gpt-3.5-turbo"),
        max_context_messages=int(getenv("MAX_CONTEXT_MESSAGES", "20")),
    )