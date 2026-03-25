import mysql.connector
from fastapi import HTTPException

from .config import db_host, db_name, db_password, db_port, db_user


def ouvrir_connexion():
    try:
        return mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name,
        )
    except mysql.connector.Error:
        raise HTTPException(
            status_code=503,
            detail="Impossible de se connecter a la base de donnees.",
        )


def fetch_all(query: str, params: tuple | None = None) -> list[dict[str, object]]:
    connexion = ouvrir_connexion()
    cursor = connexion.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        return list(cursor.fetchall())
    except HTTPException:
        raise
    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail="Erreur lors de la lecture en base.")
    finally:
        cursor.close()
        connexion.close()


def execute(query: str, params: tuple | None = None) -> dict[str, object]:
    connexion = ouvrir_connexion()
    cursor = connexion.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        connexion.commit()
        return {
            "lastrowid": cursor.lastrowid,
            "rowcount": cursor.rowcount,
        }
    except HTTPException:
        raise
    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail="Erreur lors de l'ecriture en base.")
    finally:
        cursor.close()
        connexion.close()
