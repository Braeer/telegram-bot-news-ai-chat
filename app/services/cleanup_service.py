import shutil
from pathlib import Path


class CleanupService:
    def __init__(self, chats_dir: Path = Path("data/chats")) -> None:
        self.chats_dir = chats_dir

    def cleanup_chats(self) -> None:
        if not self.chats_dir.exists():
            return

        for path in self.chats_dir.iterdir():
            if path.is_file() and path.suffix == ".json":
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
