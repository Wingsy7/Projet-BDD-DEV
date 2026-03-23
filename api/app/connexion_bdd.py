from contextlib import contextmanager
from typing import cast

import mysql.connector
from fastapi import HTTPException

from .config import settings


@contextmanager
def get_connection():
    try:
        connection = mysql.connector.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name,
        )
    except mysql.connector.Error as e:
        raise HTTPException(status_code=503, detail=f"Impossible de se connecter a la base de donnees : {e}")
    try:
        yield connection
    finally:
        connection.close()


def fetch_all(query: str, params: tuple | None = None) -> list[dict[str, object]]:
    try:
        with get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            rows = cast(list[dict[str, object]], cursor.fetchall())
            cursor.close()
            return rows
    except HTTPException:
        raise
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture : {e}")


def execute(query: str, params: tuple | None = None) -> dict[str, object]:
    try:
        with get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            connection.commit()
            result: dict[str, object] = {
                "lastrowid": cursor.lastrowid,
                "rowcount": cursor.rowcount,
            }
            cursor.close()
            return result
    except HTTPException:
        raise
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'ecriture : {e}")