import logging


class LogService:
    def __init__(self) -> None:
        self.logger = logging.getLogger("bot")

    def info(self, message: str, **extra: object) -> None:
        self.logger.info(message, extra=extra)

    def warning(self, message: str, **extra: object) -> None:
        self.logger.warning(message, extra=extra)

    def error(self, message: str, **extra: object) -> None:
        self.logger.error(message, extra=extra)

    def exception(self, message: str, **extra: object) -> None:
        self.logger.exception(message, extra=extra)
