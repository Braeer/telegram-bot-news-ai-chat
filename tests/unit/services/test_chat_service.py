from datetime import UTC, datetime, timedelta

from app.services.chat_service import ChatService


class FakeAIService:
    def generate_answer(
        self,
        user_id: int,
        message_text: str,
        context: list[dict],
        config: dict,
    ) -> str:
        return f"Mock answer: {message_text}"


class FakeChatStorage:
    def __init__(self):
        self.chats = {}
        self.deleted_user_ids = []

    def read_chat(self, user_id: int) -> dict:
        return self.chats.get(
            user_id,
            {
                "user_id": user_id,
                "messages": [],
            },
        )

    def write_chat(self, user_id: int, data: dict) -> None:
        self.chats[user_id] = data

    def delete_chat(self, user_id: int) -> None:
        self.deleted_user_ids.append(user_id)
        self.chats.pop(user_id, None)

    def get_chat_user_ids(self) -> list[int]:
        return list(self.chats.keys())


class FakeAnalyticsService:
    def __init__(self):
        self.requests = []

    def track_request(self, user_id: int, input_tokens: int = 0, output_tokens: int = 0) -> None:
        self.requests.append(
            {
                "user_id": user_id,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            }
        )


class FakeSettingsService:
    def get_global_settings(self) -> dict:
        return {
            "max_context_messages": 4,
        }

    def build_final_config(self, user_id: int) -> dict:
        return {
            "model": "mock",
            "temperature": 0.7,
            "max_tokens": 2000,
            "system_prompt": "",
        }


def build_service() -> tuple[ChatService, FakeChatStorage, FakeAnalyticsService]:
    chat_storage = FakeChatStorage()
    analytics_service = FakeAnalyticsService()
    settings_service = FakeSettingsService()
    ai_service = FakeAIService()

    service = ChatService(
        chat_storage=chat_storage,
        analytics_service=analytics_service,
        settings_service=settings_service,
        ai_service=ai_service,
    )

    return service, chat_storage, analytics_service


def test_create_new_chat_deletes_old_chat_and_creates_empty_chat():
    service, chat_storage, _ = build_service()

    chat_storage.chats[123] = {
        "user_id": 123,
        "messages": [{"role": "user", "content": "old"}],
    }

    service.create_new_chat(123)

    assert 123 in chat_storage.deleted_user_ids
    assert chat_storage.chats[123]["messages"] == []


def test_reset_chat_deletes_chat():
    service, chat_storage, _ = build_service()

    chat_storage.chats[123] = {
        "user_id": 123,
        "messages": [{"role": "user", "content": "old"}],
    }

    service.reset_chat(123)

    assert 123 in chat_storage.deleted_user_ids
    assert 123 not in chat_storage.chats


def test_continue_chat_saves_user_and_assistant_messages():
    service, chat_storage, analytics_service = build_service()

    answer = service.continue_chat(
        user_id=123,
        message_text="Привет",
    )

    messages = chat_storage.chats[123]["messages"]

    assert answer == "Mock answer: Привет"
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Привет"
    assert messages[1]["role"] == "assistant"
    assert messages[1]["content"] == "Mock answer: Привет"

    assert analytics_service.requests == [
        {
            "user_id": 123,
            "input_tokens": 0,
            "output_tokens": 0,
        }
    ]


def test_continue_chat_removes_messages_older_than_two_days():
    service, chat_storage, _ = build_service()

    old_date = (datetime.now(UTC) - timedelta(days=3)).isoformat()
    fresh_date = datetime.now(UTC).isoformat()

    chat_storage.chats[123] = {
        "user_id": 123,
        "messages": [
            {
                "role": "user",
                "content": "old",
                "created_at": old_date,
            },
            {
                "role": "user",
                "content": "fresh",
                "created_at": fresh_date,
            },
        ],
    }

    service.continue_chat(
        user_id=123,
        message_text="new",
    )

    contents = [message["content"] for message in chat_storage.chats[123]["messages"]]

    assert "old" not in contents
    assert "fresh" in contents
    assert "new" in contents


def test_continue_chat_trims_context_by_global_limit():
    service, chat_storage, _ = build_service()

    for index in range(3):
        service.continue_chat(
            user_id=123,
            message_text=f"message-{index}",
        )

    messages = chat_storage.chats[123]["messages"]

    assert len(messages) == 4
    assert messages[0]["content"] == "message-1"
    assert messages[-1]["content"] == "Mock answer: message-2"
