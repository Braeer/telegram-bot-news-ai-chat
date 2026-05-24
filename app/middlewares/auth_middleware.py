from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from app.services.auth_service import AuthService
from app.services.template_service import TemplateService


class AuthMiddleware(BaseMiddleware):
    def __init__(
        self,
        auth_service: AuthService,
        template_service: TemplateService,
    ) -> None:
        self.auth_service = auth_service
        self.template_service = template_service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        user = event.from_user
        if user is None:
            return

        if not self.auth_service.is_allowed_user(user.id):
            await event.answer(
                self.template_service.load("error/access_denied.txt"),
            )
            return

        data["user_id"] = user.id

        return await handler(event, data)
