from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.settings_service import SettingsService
from app.services.template_service import TemplateService


def build_settings_router(
    settings_service: SettingsService,
    template_service: TemplateService,
) -> Router:
    router = Router()

    @router.message(Command("settings"))
    async def settings_handler(message: Message, user_id: int) -> None:
        config = settings_service.build_final_config(user_id)

        await message.answer(
            template_service.load("user/settings.txt").format(
                model=config["model"],
                temperature=config["temperature"],
                max_tokens=config["max_tokens"],
                system_prompt=config["system_prompt"] or "не задан",
            )
        )

    @router.message(Command("prompt"))
    async def prompt_handler(message: Message, user_id: int) -> None:
        prompt = _get_command_value(message.text)

        if not prompt:
            await message.answer(template_service.load("error/empty_prompt.txt"))
            return

        settings_service.update_user_prompt(user_id, prompt)
        await message.answer(template_service.load("user/prompt_updated.txt"))

    @router.message(Command("set-model"))
    async def set_model_handler(message: Message, user_id: int) -> None:
        model = _get_command_value(message.text)

        if not model:
            await message.answer(template_service.load("error/invalid_setting_value.txt"))
            return

        try:
            settings_service.update_user_model(user_id, model)
        except ValueError as error:
            await message.answer(str(error))
            return

        await message.answer(template_service.load("user/settings_updated.txt"))

    @router.message(Command("set-temperature"))
    async def set_temperature_handler(message: Message, user_id: int) -> None:
        value = _get_command_value(message.text)

        try:
            temperature = float(value) if value is not None else None
        except ValueError:
            temperature = None

        if temperature is None:
            await message.answer(template_service.load("error/invalid_setting_value.txt"))
            return

        try:
            settings_service.update_user_temperature(user_id, temperature)
        except ValueError as error:
            await message.answer(str(error))
            return

        await message.answer(template_service.load("user/settings_updated.txt"))

    @router.message(Command("set-max-tokens"))
    async def set_max_tokens_handler(message: Message, user_id: int) -> None:
        value = _get_command_value(message.text)

        if not value or not value.isdigit():
            await message.answer(template_service.load("error/invalid_setting_value.txt"))
            return

        try:
            settings_service.update_user_max_tokens(user_id, int(value))
        except ValueError as error:
            await message.answer(str(error))
            return

        await message.answer(template_service.load("user/settings_updated.txt"))

    return router


def _get_command_value(text: str | None) -> str | None:
    if not text:
        return None

    parts = text.split(maxsplit=1)

    if len(parts) != 2:
        return None

    return parts[1].strip()
