import json
from pathlib import Path

DATA_DIR = Path("data")


def ensure_project_structure(main_admin_id: int) -> None:

    directories = [
        DATA_DIR,
        DATA_DIR / "chats",
        DATA_DIR / "settings",
        DATA_DIR / "settings" / "users",
        DATA_DIR / "analytics",
        DATA_DIR / "analytics" / "users",
        DATA_DIR / "errors",
        DATA_DIR / "logs",
        DATA_DIR / "time-data",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    _ensure_json_file(
        DATA_DIR / "settings" / "access.json",
        {
            "admins": [main_admin_id],
            "users": [main_admin_id],
        },
    )

    _ensure_json_file(
        DATA_DIR / "settings" / "global.json",
        {
            "default_model": "mock",
        },
    )

    _ensure_json_file(
        DATA_DIR / "analytics" / "global.json",
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
