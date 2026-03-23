import os
from dataclasses import dataclass
from pathlib import Path


def load_local_env() -> None:
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


load_local_env()


@dataclass(frozen=True)
class Settings:
    db_host: str = os.getenv("SCHOOL_DB_HOST", "localhost")
    db_port: int = int(os.getenv("SCHOOL_DB_PORT", "3306"))
    db_user: str = os.getenv("SCHOOL_DB_USER", "root")
    db_password: str = os.getenv("SCHOOL_DB_PASSWORD", "")
    db_name: str = os.getenv("SCHOOL_DB_NAME", "cozma_miroslav")


settings = Settings()
