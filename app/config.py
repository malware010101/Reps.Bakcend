# app/config.py
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / "venv" / ".env"

if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()
