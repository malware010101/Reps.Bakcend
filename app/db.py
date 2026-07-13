import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / "venv" / ".env"

if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()


TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("db_url")
    },
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "default",
        },
    },
}
