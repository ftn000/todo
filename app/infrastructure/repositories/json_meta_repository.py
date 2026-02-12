import json
from pathlib import Path
from app.domain.repositories.meta_repository import MetaRepository

class JsonMetaRepository(MetaRepository):

    def __init__(self, path: Path):
        self._path = path

    def _read(self) -> dict:
        if not self._path.exists():
            return {}

        with self._path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: dict) -> None:
        with self._path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def get(self, key: str) -> str | None:
        data = self._read()
        return data.get(key)

    def set(self, key: str, value: str | None) -> None:
        data = self._read()
        data[key] = value
        self._write(data)