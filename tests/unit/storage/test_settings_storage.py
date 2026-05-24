import json
from pathlib import Path

from app.storage.settings_storage import SettingsStorage


def test_read_access_config_returns_access_data(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    access_path = Path("data/settings/access.json")
    access_path.parent.mkdir(parents=True)

    access_path.write_text(
        json.dumps(
            {
                "admins": [123],
                "users": [123, 456],
            }
        ),
        encoding="utf-8",
    )

    storage = SettingsStorage()

    assert storage.read_access_config() == {
        "admins": [123],
        "users": [123, 456],
    }
