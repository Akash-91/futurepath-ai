from pathlib import Path
from uuid import UUID

from .config import settings


class ResumeStorage:
    def __init__(self) -> None:
        self.root = Path(settings.resume_storage_path)
        self.root.mkdir(parents=True, exist_ok=True)

    def key_for(self, user_id: UUID, resume_id: UUID) -> str:
        return f"{user_id}/{resume_id}.pdf"

    def path_for(self, storage_key: str) -> Path:
        path = (self.root / storage_key).resolve()
        if self.root.resolve() not in path.parents:
            raise ValueError("Invalid storage key")
        return path

    def save(self, storage_key: str, content: bytes) -> None:
        path = self.path_for(storage_key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def read(self, storage_key: str) -> bytes:
        return self.path_for(storage_key).read_bytes()

    def delete(self, storage_key: str) -> None:
        path = self.path_for(storage_key)
        if path.exists():
            path.unlink()


resume_storage = ResumeStorage()
