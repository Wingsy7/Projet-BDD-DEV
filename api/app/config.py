from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    db_host: str = os.getenv("SCHOOL_DB_HOST", "localhost")
    db_port: int = int(os.getenv("SCHOOL_DB_PORT", "3306"))
    db_user: str = os.getenv("SCHOOL_DB_USER", "root")
    db_password: str = os.getenv("SCHOOL_DB_PASSWORD", "")
    db_name: str = os.getenv("SCHOOL_DB_NAME", "cozma_miroslav")


settings = Settings()
