import json
from pathlib import Path
from typing import Any


class SettingsStorage:
    def __init__(self, data_dir: Path = Path("data")) -> None:
        self.data_dir = data_dir

    def read_access_config(self) -> dict[str, Any]:
        path = self.data_dir / "settings" / "access.json"

        with path.open(encoding="utf-8") as file:
            return json.load(file)

    def write_access_config(self, data: dict) -> None:
        path = self.data_dir / "settings" / "access.json"

        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def add_user(self, user_id: int) -> None:
        access_config = self.read_access_config()

        if user_id not in access_config["users"]:
            access_config["users"].append(user_id)

        self.write_access_config(access_config)

    def add_admin(self, user_id: int) -> None:
        access_config = self.read_access_config()

        if user_id not in access_config["admins"]:
            access_config["admins"].append(user_id)

        if user_id not in access_config["users"]:
            access_config["users"].append(user_id)

        self.write_access_config(access_config)
