import os
from pathlib import Path


def charger_env_local() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


charger_env_local()


class Settings:
    def __init__(self) -> None:
        self.db_host = os.getenv("SCHOOL_DB_HOST", "localhost")
        self.db_port = int(os.getenv("SCHOOL_DB_PORT", "3306"))
        self.db_user = os.getenv("SCHOOL_DB_USER", "root")
        self.db_password = os.getenv("SCHOOL_DB_PASSWORD", "")
        self.db_name = os.getenv("SCHOOL_DB_NAME", "equipe_5")


settings = Settings()
