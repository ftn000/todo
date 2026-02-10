from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"

TASKS_FILE = DATA_DIR / "tasks.json"
META_FILE = DATA_DIR / "meta.json"
