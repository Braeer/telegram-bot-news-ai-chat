from datetime import UTC, datetime, timedelta
from typing import Any

from app.services.ai_service import AIService
from app.services.analytics_service import AnalyticsService
from app.services.settings_service import SettingsService
from app.storage.chat_storage import ChatStorage


class ChatService:
    def __init__(
        self,
        chat_storage: ChatStorage,
        analytics_service: AnalyticsService,
        settings_service: SettingsService,
        ai_service: AIService,
    ) -> None:
        self.chat_storage = chat_storage
        self.analytics_service = analytics_service
        self.settings_service = settings_service
        self.ai_service = ai_service

    def create_new_chat(self, user_id: int) -> None:
        self.chat_storage.delete_chat(user_id)
        self._create_empty_chat(user_id)

    def reset_chat(self, user_id: int) -> None:
        self.chat_storage.delete_chat(user_id)

    def continue_chat(self, user_id: int, message_text: str) -> str:
        chat = self.chat_storage.read_chat(user_id)
        chat["messages"] = self._remove_expired_messages(chat.get("messages", []))

        config = self.settings_service.build_final_config(user_id)

        answer = self.ai_service.generate_answer(
            user_id=user_id,
            message_text=message_text,
            context=chat["messages"],
            config=config,
        )

        chat["messages"].append(
            self._build_message(
                role="user",
                content=message_text,
            )
        )

        chat["messages"].append(
            self._build_message(
                role="assistant",
                content=answer,
            )
        )

        chat["messages"] = self._trim_context(
            messages=chat["messages"],
        )

        chat["updated_at"] = self._now()

        self.chat_storage.write_chat(user_id, chat)

        self.analytics_service.track_request(
            user_id=user_id,
            input_tokens=0,
            output_tokens=0,
        )

        return answer

    def cleanup_expired_messages(self) -> None:
        for user_id in self.chat_storage.get_chat_user_ids():
            chat = self.chat_storage.read_chat(user_id)
            chat["messages"] = self._remove_expired_messages(chat.get("messages", []))
            chat["updated_at"] = self._now()

            self.chat_storage.write_chat(user_id, chat)

    def _create_empty_chat(self, user_id: int) -> None:
        now = self._now()

        self.chat_storage.write_chat(
            user_id,
            {
                "user_id": user_id,
                "messages": [],
                "created_at": now,
                "updated_at": now,
            },
        )

    def _remove_expired_messages(
        self,
        messages: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        min_created_at = datetime.now(UTC) - timedelta(days=2)

        active_messages = []

        for message in messages:
            created_at = message.get("created_at")

            if not created_at:
                continue

            if datetime.fromisoformat(created_at) >= min_created_at:
                active_messages.append(message)

        return active_messages

    def _trim_context(
        self,
        messages: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        global_settings = self.settings_service.get_global_settings()
        max_context_messages = int(global_settings["max_context_messages"])

        if len(messages) <= max_context_messages:
            return messages

        return messages[-max_context_messages:]

    def _build_message(self, role: str, content: str) -> dict[str, str]:
        return {
            "role": role,
            "content": content,
            "created_at": self._now(),
        }

    def _now(self) -> str:
        return datetime.now(UTC).isoformat()
