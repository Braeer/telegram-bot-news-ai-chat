import json
from pathlib import Path
from typing import Any


class AnalyticsStorage:
    def __init__(self, data_dir: Path = Path("data")) -> None:
        self.data_dir = data_dir

    def read_user_analytics(self, user_id: int) -> dict[str, Any]:
        path = self.data_dir / "analytics" / "users" / f"{user_id}.json"

        if not path.exists():
            return {
                "user_id": user_id,
                "total_requests": 0,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_tokens": 0,
                "last_request_at": None,
            }

        with path.open(encoding="utf-8") as file:
            return json.load(file)

    def read_global_analytics(self) -> dict:
        path = self.data_dir / "analytics" / "global.json"

        if not path.exists():
            return {
                "total_requests": 0,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_tokens": 0,
                "errors_today": 0,
                "last_request_at": None,
            }

        with path.open(encoding="utf-8") as file:
            return json.load(file)
