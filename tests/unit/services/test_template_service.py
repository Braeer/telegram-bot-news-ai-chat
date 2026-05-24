from pathlib import Path

from app.services.template_service import TemplateService


def test_load_returns_template_content(tmp_path):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()

    template_file = templates_dir / "test.txt"
    template_file.write_text("Hello", encoding="utf-8")

    service = TemplateService(
        templates_dir=templates_dir,
    )

    assert service.load("test.txt") == "Hello"
