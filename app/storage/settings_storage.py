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
