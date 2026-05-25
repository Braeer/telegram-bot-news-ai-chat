import json
from pathlib import Path
from typing import Any


class ChatStorage:
    def __init__(self, data_dir: Path = Path("data")) -> None:
        self.data_dir = data_dir

    def read_chat(self, user_id: int) -> dict[str, Any]:
        path = self.data_dir / "chats" / f"{user_id}.json"

        if not path.exists():
            return {
                "user_id": user_id,
                "messages": [],
            }

        with path.open(encoding="utf-8") as file:
            return json.load(file)

    def write_chat(self, user_id: int, data: dict[str, Any]) -> None:
        path = self.data_dir / "chats" / f"{user_id}.json"

        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def delete_chat(self, user_id: int) -> None:
        path = self.data_dir / "chats" / f"{user_id}.json"

        if path.exists():
            path.unlink()

    def get_chat_user_ids(self) -> list[int]:
        chats_dir = self.data_dir / "chats"

        if not chats_dir.exists():
            return []

        return [int(path.stem) for path in chats_dir.glob("*.json") if path.stem.isdigit()]
