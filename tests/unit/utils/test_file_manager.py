import json
from pathlib import Path

from app.utils.file_manager import ensure_project_structure


def test_ensure_project_structure_creates_required_directories(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    ensure_project_structure(main_admin_id=123456)

    assert Path("data").exists()
    assert Path("data/chats").exists()
    assert Path("data/settings").exists()
    assert Path("data/settings/users").exists()
    assert Path("data/analytics").exists()
    assert Path("data/analytics/users").exists()
    assert Path("data/errors").exists()
    assert Path("data/logs").exists()
    assert Path("data/time-data").exists()


def test_ensure_project_structure_creates_access_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    ensure_project_structure(main_admin_id=123456)

    access_config = json.loads(Path("data/settings/access.json").read_text())

    assert access_config == {
        "admins": [123456],
        "users": [123456],
    }


def test_ensure_project_structure_does_not_override_existing_access_config(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    access_path = Path("data/settings/access.json")
    access_path.parent.mkdir(parents=True)

    access_path.write_text(
        json.dumps(
            {
                "admins": [111],
                "users": [111, 222],
            }
        ),
        encoding="utf-8",
    )

    ensure_project_structure(main_admin_id=123456)

    access_config = json.loads(access_path.read_text())

    assert access_config == {
        "admins": [111],
        "users": [111, 222],
    }
