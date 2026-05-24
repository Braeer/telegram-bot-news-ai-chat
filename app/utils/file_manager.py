import json
from pathlib import Path


def ensure_project_structure(data_dir: str, main_admin_id: int) -> None:
    root = Path(data_dir)

    directories = [
        root,
        root / "chats",
        root / "settings",
        root / "settings" / "users",
        root / "analytics",
        root / "analytics" / "users",
        root / "errors",
        root / "logs",
        root / "time-data",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    _ensure_json_file(
        root / "settings" / "access.json",
        {
            "admins": [main_admin_id],
            "users": [main_admin_id],
        },
    )

    _ensure_json_file(
        root / "settings" / "global.json",
        {
            "default_model": "mock",
        },
    )

    _ensure_json_file(
        root / "analytics" / "global.json",
        {
            "total_requests": 0,
            "total_tokens": 0,
        },
    )


def _ensure_json_file(path: Path, default_data: dict) -> None:
    if path.exists():
        return

    path.write_text(
        json.dumps(default_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
