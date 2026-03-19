from contextlib import contextmanager

import mysql.connector

from .config import settings


@contextmanager
def get_connection():
    connection = mysql.connector.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
    )
    try:
        yield connection
    finally:
        connection.close()


def fetch_all(query: str, params: tuple | None = None) -> list[dict]:
    with get_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        cursor.close()
        return rows


def execute(query: str, params: tuple | None = None) -> dict:
    with get_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        connection.commit()
        result = {
            "lastrowid": cursor.lastrowid,
            "rowcount": cursor.rowcount,
        }
        cursor.close()
        return result
