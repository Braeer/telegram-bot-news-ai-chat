import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from app.services.template_service import TemplateService


class ErrorMiddleware(BaseMiddleware):
    def __init__(self, template_service: TemplateService) -> None:
        self.template_service = template_service
        self.logger = logging.getLogger("bot.error")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception:
            self.logger.exception("Unhandled error while processing update")

            if isinstance(event, Message):
                await event.answer(
                    self.template_service.load("error/internal_error.txt"),
                )

            return None
