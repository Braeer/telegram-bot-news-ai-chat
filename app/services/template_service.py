from pathlib import Path


class TemplateService:
    def __init__(self, templates_dir: Path = Path("app/templates")) -> None:
        self.templates_dir = templates_dir

    def load(self, template_path: str) -> str:
        path = self.templates_dir / template_path

        return path.read_text(encoding="utf-8").strip()
