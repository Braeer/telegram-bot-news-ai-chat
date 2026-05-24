from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass(frozen=True)
class EnvConfig:
    telegram_bot_token: str
    log_level: str
    default_model: str
    max_context_messages: int
    main_admin_id: int


def load_env_config() -> EnvConfig:
    load_dotenv()

    token = getenv("TELEGRAM_BOT_TOKEN")
    main_admin_id = getenv("MAIN_ADMIN_ID")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")

    if not main_admin_id:
        raise ValueError("MAIN_ADMIN_ID is not set")

    return EnvConfig(
        telegram_bot_token=token,
        main_admin_id=int(main_admin_id),
        log_level=getenv("LOG_LEVEL", "INFO"),
        default_model=getenv("DEFAULT_MODEL", "gpt-3.5-turbo"),
        max_context_messages=int(getenv("MAX_CONTEXT_MESSAGES", "20")),
    )
