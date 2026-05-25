import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from app.services.template_service import TemplateService


class RateLimitMiddleware(BaseMiddleware):
    def __init__(
        self,
        template_service: TemplateService,
        limit_seconds: float = 2.0,
    ) -> None:
        self.template_service = template_service
        self.limit_seconds = limit_seconds
        self.last_request_by_user: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message) or event.from_user is None:
            return await handler(event, data)

        user_id = event.from_user.id
        now = time.monotonic()
        last_request_at = self.last_request_by_user.get(user_id)

        if last_request_at is not None and now - last_request_at < self.limit_seconds:
            await event.answer(
                self.template_service.load("error/rate_limit.txt"),
            )
            return None

        self.last_request_by_user[user_id] = now

        return await handler(event, data)
