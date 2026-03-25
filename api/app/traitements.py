from fastapi import HTTPException

from .bdd import execute, fetch_all
from .requetes import (
    ABSENCE_SELECT,
    ALTERNANCE_SELECT,
    CLUB_INSCRIPTION_SELECT,
    CLUB_SELECT,
    COURSE_SELECT,
    DOSSIER_SELECT,
    ENTREPRISE_SELECT,
    INSTANCE_SELECT,
    NOTE_SELECT,
    PROF_SELECT,
    PROMOTION_SELECT,
    STUDENT_SELECT,
)


def format_eleve_admin(row: dict) -> dict:
    return {
        "id": row["id"],
        "nom": row["nom"],
        "email": row["email"],
        "age": row["age"],
        "promotion": {
            "id": row["promotion_id"],
            "nom": row["promotion_nom"],
            "annee": row["promotion_annee"],
        },
        "specialite": {
            "id": row["specialite_id"],
            "nom": row["specialite_nom"],
        },
        "dossier": {
            "infos": row["dossier_infos"] or "",
            "avertissement_travail": bool(row["avertissement_travail"]),
            "avertissement_comportement": bool(row["avertissement_comportement"]),
        },
    }


def format_eleve_simple(row: dict) -> dict:
    return {
        "nom": row["nom"],
        "age": row["age"],
    }


def format_note_api(row: dict) -> dict:
    return {
        "note": float(row["valeur"]),
        "matiere": row["cours_nom"],
        "nom_eleve": row["eleve_nom"],
    }


def format_note_admin(row: dict) -> dict:
    row["valeur"] = float(row["valeur"])
    return row


def format_alternance(row: dict) -> dict:
    row["salaire_mensuel"] = float(row["salaire_mensuel"])
    return row


def verifier(item: dict | None, message: str) -> dict:
    if item is None:
        raise HTTPException(status_code=404, detail=message)
    return item


def trouver_par_id(rows: list[dict], item_id: int, message: str) -> dict:
    for row in rows:
        if row["id"] == item_id:
            return row
    raise HTTPException(status_code=404, detail=message)


def preparer_update(payload: dict) -> tuple[str, tuple]:
    values = {}
    for key, value in payload.items():
        if value is not None:
            values[key] = value

    if not values:
        raise HTTPException(status_code=400, detail="Aucune valeur a modifier.")

    sql = ", ".join(f"{key} = %s" for key in values)
    params = tuple(values.values())
    return sql, params


def list_eleves() -> list[dict]:
    result = []
    for row in fetch_all(STUDENT_SELECT):
        result.append(format_eleve_simple(row))
    return result


def list_eleves_admin() -> list[dict]:
    result = []
    for row in fetch_all(STUDENT_SELECT):
        result.append(format_eleve_admin(row))
    return result


def get_eleve(eleve_id: int) -> dict:
    for eleve in list_eleves_admin():
        if eleve["id"] == eleve_id:
            return eleve
    raise HTTPException(status_code=404, detail="Eleve introuvable.")


def list_promotions() -> list[dict]:
    return fetch_all(PROMOTION_SELECT)


def list_specialite_cours(specialite_id: int) -> list[dict]:
    result = []
    for row in fetch_all(COURSE_SELECT):
        if row["specialite_id"] == specialite_id:
            result.append(
                {
                    "id": row["id"],
                    "nom": row["nom"],
                    "niveau": row["niveau"],
                }
            )
    return result


def list_specialite_promotions(specialite_id: int) -> list[dict]:
    result = []
    for row in fetch_all(PROMOTION_SELECT):
        if row["specialite_id"] == specialite_id:
            result.append(
                {
                    "id": row["id"],
                    "nom": row["nom"],
                    "annee": row["annee"],
                }
            )
    return result


def list_notes_admin() -> list[dict]:
    result = []
    for row in fetch_all(NOTE_SELECT):
        result.append(format_note_admin(row))
    return result


def list_notes_for_eleve(eleve_id: int) -> list[dict]:
    get_eleve(eleve_id)
    result = []
    for row in list_notes_admin():
        if row["eleve_id"] == eleve_id:
            result.append(format_note_api(row))
    return result


def list_eleves_avertis() -> list[dict]:
    result = []
    for eleve in list_eleves_admin():
        dossier = eleve["dossier"]
        if dossier["avertissement_travail"] or dossier["avertissement_comportement"]:
            result.append(
                {
                    "nom": eleve["nom"],
                    "age": eleve["age"],
                    "avertissement_travail": dossier["avertissement_travail"],
                    "avertissement_comportement": dossier["avertissement_comportement"],
                }
            )
    return result


def list_eleves_bonne_notes() -> list[dict]:
    grouped = {}

    for row in list_notes_admin():
        eleve_id = row["eleve_id"]
        if eleve_id not in grouped:
            grouped[eleve_id] = {"nom": row["eleve_nom"], "notes": []}
        grouped[eleve_id]["notes"].append(row["valeur"])

    result = []
    for values in grouped.values():
        moyenne = round(sum(values["notes"]) / len(values["notes"]), 2)
        if moyenne > 12:
            result.append({"nom": values["nom"], "moyenne_generale": moyenne})

    result = sorted(result, key=lambda item: item["moyenne_generale"], reverse=True)
    return result


def list_profs() -> list[dict]:
    return fetch_all(PROF_SELECT)


def list_profs_severes() -> list[dict]:
    grouped = {}

    for row in list_notes_admin():
        prof_id = row["prof_id"]
        if prof_id is None:
            continue
        if prof_id not in grouped:
            grouped[prof_id] = {"nom": row["prof_nom"], "notes": []}
        grouped[prof_id]["notes"].append(row["valeur"])

    result = []
    for values in grouped.values():
        moyenne = round(sum(values["notes"]) / len(values["notes"]), 2)
        if moyenne < 8:
            result.append(
                {
                    "nom": values["nom"],
                    "moyenne_des_notes_donnees": moyenne,
                }
            )

    result = sorted(result, key=lambda item: item["moyenne_des_notes_donnees"])
    return result


def get_absence_hours_for_eleve(eleve_id: int) -> dict:
    eleve = get_eleve(eleve_id)
    minutes = 0
    for row in fetch_all(ABSENCE_SELECT):
        if row["eleve_id"] == eleve_id:
            minutes += row["duree_minutes"]

    return {
        "nom_eleve": eleve["nom"],
        "heures_absence": round(minutes / 60, 2),
    }


def group_notes_by(par: str) -> dict:
    choices = {
        "eleve": "eleve_nom",
        "prof": "prof_nom",
        "cours": "cours_nom",
        "promotion": "promotion_nom",
    }

    if par not in choices:
        raise HTTPException(status_code=400, detail="Le parametre 'par' est invalide.")

    key_name = choices[par]
    result = {}

    for row in list_notes_admin():
        label = row[key_name] or "Non renseigne"
        if label not in result:
            result[label] = []
        result[label].append(format_note_api(row))

    return result


def list_instances() -> list[dict]:
    return fetch_all(INSTANCE_SELECT)


def list_dossiers() -> list[dict]:
    rows = fetch_all(DOSSIER_SELECT)
    for row in rows:
        row["avertissement_travail"] = bool(row["avertissement_travail"])
        row["avertissement_comportement"] = bool(row["avertissement_comportement"])
    return rows


def list_clubs() -> list[dict]:
    clubs = fetch_all(CLUB_SELECT)
    inscriptions = fetch_all(CLUB_INSCRIPTION_SELECT)
    member_count_by_club = {}

    for inscription in inscriptions:
        club_id = inscription["club_id"]
        if club_id not in member_count_by_club:
            member_count_by_club[club_id] = 0
        member_count_by_club[club_id] += 1

    for club in clubs:
        club["budget_annuel"] = float(club["budget_annuel"])
        club["nombre_membres"] = member_count_by_club.get(club["id"], 0)

    return clubs


def list_club_members(club_id: int) -> list[dict]:
    trouver_par_id(list_clubs(), club_id, "Club introuvable.")
    result = []

    for row in fetch_all(CLUB_INSCRIPTION_SELECT):
        if row["club_id"] == club_id:
            result.append(
                {
                    "eleve_id": row["eleve_id"],
                    "nom_eleve": row["eleve_nom"],
                    "role_membre": row["role_membre"],
                    "date_inscription": row["date_inscription"],
                }
            )

    return result


def list_eleve_clubs(eleve_id: int) -> list[dict]:
    get_eleve(eleve_id)
    result = []

    for row in fetch_all(CLUB_INSCRIPTION_SELECT):
        if row["eleve_id"] == eleve_id:
            result.append(
                {
                    "club_id": row["club_id"],
                    "club_nom": row["club_nom"],
                    "role_membre": row["role_membre"],
                    "date_inscription": row["date_inscription"],
                }
            )

    return result


def list_entreprises() -> list[dict]:
    return fetch_all(ENTREPRISE_SELECT)


def list_alternances() -> list[dict]:
    result = []
    for row in fetch_all(ALTERNANCE_SELECT):
        result.append(format_alternance(row))
    return result


def list_eleve_alternances(eleve_id: int) -> list[dict]:
    get_eleve(eleve_id)
    result = []
    for row in list_alternances():
        if row["eleve_id"] == eleve_id:
            result.append(row)
    return result


def list_courses() -> list[dict]:
    return fetch_all(COURSE_SELECT)


def list_note_records() -> list[dict]:
    return list_notes_admin()


def create_eleve(payload: dict) -> dict:
    result = execute(
        """
        INSERT INTO eleve (nom, email, age, promotion_id)
        VALUES (%s, %s, %s, %s)
        """,
        (payload["nom"], payload["email"], payload["age"], payload["promotion_id"]),
    )
    return get_eleve(result["lastrowid"])


def update_eleve(eleve_id: int, payload: dict) -> dict:
    get_eleve(eleve_id)
    sql, params = preparer_update(payload)
    execute(f"UPDATE eleve SET {sql} WHERE id = %s", params + (eleve_id,))
    return get_eleve(eleve_id)


def delete_eleve(eleve_id: int) -> dict:
    eleve = get_eleve(eleve_id)
    execute("DELETE FROM eleve WHERE id = %s", (eleve_id,))
    return {"message": "Eleve supprime.", "eleve": eleve}


def create_prof(payload: dict) -> dict:
    result = execute(
        """
        INSERT INTO prof (nom, email, age)
        VALUES (%s, %s, %s)
        """,
        (payload["nom"], payload["email"], payload["age"]),
    )
    return trouver_par_id(list_profs(), result["lastrowid"], "Prof introuvable.")


def update_prof(prof_id: int, payload: dict) -> dict:
    trouver_par_id(list_profs(), prof_id, "Prof introuvable.")
    sql, params = preparer_update(payload)
    execute(f"UPDATE prof SET {sql} WHERE id = %s", params + (prof_id,))
    return trouver_par_id(list_profs(), prof_id, "Prof introuvable.")


def delete_prof(prof_id: int) -> dict:
    prof = trouver_par_id(list_profs(), prof_id, "Prof introuvable.")
    execute("DELETE FROM prof WHERE id = %s", (prof_id,))
    return {"message": "Prof supprime.", "prof": prof}


def create_note(payload: dict) -> dict:
    result = execute(
        """
        INSERT INTO note (eleve_id, cours_id, prof_id, valeur, commentaire)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            payload["eleve_id"],
            payload["cours_id"],
            payload.get("prof_id"),
            payload["valeur"],
            payload.get("commentaire"),
        ),
    )
    return trouver_par_id(list_notes_admin(), result["lastrowid"], "Note introuvable.")


def update_note(note_id: int, payload: dict) -> dict:
    trouver_par_id(list_notes_admin(), note_id, "Note introuvable.")
    sql, params = preparer_update(payload)
    execute(f"UPDATE note SET {sql} WHERE id = %s", params + (note_id,))
    return trouver_par_id(list_notes_admin(), note_id, "Note introuvable.")


def update_dossier(eleve_id: int, payload: dict) -> dict:
    dossier = None
    for row in list_dossiers():
        if row["eleve_id"] == eleve_id:
            dossier = row
            break

    verifier(dossier, "Dossier introuvable.")
    sql, params = preparer_update(payload)
    execute(f"UPDATE dossier SET {sql} WHERE eleve_id = %s", params + (eleve_id,))

    dossier = None
    for row in list_dossiers():
        if row["eleve_id"] == eleve_id:
            dossier = row
            break

    return verifier(dossier, "Dossier introuvable.")


def create_instance(payload: dict) -> dict:
    result = execute(
        """
        INSERT INTO instance_cours (cours_id, prof_id, date_cours)
        VALUES (%s, %s, %s)
        """,
        (payload["cours_id"], payload["prof_id"], payload["date_cours"]),
    )
    return trouver_par_id(list_instances(), result["lastrowid"], "Instance de cours introuvable.")


def update_instance(instance_id: int, payload: dict) -> dict:
    trouver_par_id(list_instances(), instance_id, "Instance de cours introuvable.")
    sql, params = preparer_update(payload)
    execute(f"UPDATE instance_cours SET {sql} WHERE id = %s", params + (instance_id,))
    return trouver_par_id(list_instances(), instance_id, "Instance de cours introuvable.")


def delete_instance(instance_id: int) -> dict:
    instance = trouver_par_id(list_instances(), instance_id, "Instance de cours introuvable.")
    execute("DELETE FROM instance_cours WHERE id = %s", (instance_id,))
    return {"message": "Instance de cours supprimee.", "instance": instance}


def create_club(payload: dict) -> dict:
    result = execute(
        """
        INSERT INTO club (nom, categorie, budget_annuel, responsable_prof_id)
        VALUES (%s, %s, %s, %s)
        """,
        (
            payload["nom"],
            payload["categorie"],
            payload["budget_annuel"],
            payload.get("responsable_prof_id"),
        ),
    )
    return trouver_par_id(list_clubs(), result["lastrowid"], "Club introuvable.")


def update_club(club_id: int, payload: dict) -> dict:
    trouver_par_id(list_clubs(), club_id, "Club introuvable.")
    sql, params = preparer_update(payload)
    execute(f"UPDATE club SET {sql} WHERE id = %s", params + (club_id,))
    return trouver_par_id(list_clubs(), club_id, "Club introuvable.")


def delete_club(club_id: int) -> dict:
    club = trouver_par_id(list_clubs(), club_id, "Club introuvable.")
    execute("DELETE FROM club WHERE id = %s", (club_id,))
    return {"message": "Club supprime.", "club": club}


def list_club_inscriptions() -> list[dict]:
    return fetch_all(CLUB_INSCRIPTION_SELECT)


def create_club_inscription(payload: dict) -> dict:
    result = execute(
        """
        INSERT INTO inscription_club (club_id, eleve_id, role_membre, date_inscription)
        VALUES (%s, %s, %s, %s)
        """,
        (
            payload["club_id"],
            payload["eleve_id"],
            payload["role_membre"],
            payload["date_inscription"],
        ),
    )
    return trouver_par_id(list_club_inscriptions(), result["lastrowid"], "Inscription club introuvable.")


def update_club_inscription(inscription_id: int, payload: dict) -> dict:
    trouver_par_id(list_club_inscriptions(), inscription_id, "Inscription club introuvable.")
    sql, params = preparer_update(payload)
    execute(f"UPDATE inscription_club SET {sql} WHERE id = %s", params + (inscription_id,))
    return trouver_par_id(list_club_inscriptions(), inscription_id, "Inscription club introuvable.")


def delete_club_inscription(inscription_id: int) -> dict:
    inscription = trouver_par_id(list_club_inscriptions(), inscription_id, "Inscription club introuvable.")
    execute("DELETE FROM inscription_club WHERE id = %s", (inscription_id,))
    return {"message": "Inscription club supprimee.", "inscription": inscription}


def create_entreprise(payload: dict) -> dict:
    result = execute(
        """
        INSERT INTO entreprise (nom, secteur, ville, email_contact, telephone)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            payload["nom"],
            payload["secteur"],
            payload["ville"],
            payload.get("email_contact"),
            payload.get("telephone"),
        ),
    )
    return trouver_par_id(list_entreprises(), result["lastrowid"], "Entreprise introuvable.")


def update_entreprise(entreprise_id: int, payload: dict) -> dict:
    trouver_par_id(list_entreprises(), entreprise_id, "Entreprise introuvable.")
    sql, params = preparer_update(payload)
    execute(f"UPDATE entreprise SET {sql} WHERE id = %s", params + (entreprise_id,))
    return trouver_par_id(list_entreprises(), entreprise_id, "Entreprise introuvable.")


def delete_entreprise(entreprise_id: int) -> dict:
    entreprise = trouver_par_id(list_entreprises(), entreprise_id, "Entreprise introuvable.")
    execute("DELETE FROM entreprise WHERE id = %s", (entreprise_id,))
    return {"message": "Entreprise supprimee.", "entreprise": entreprise}


def create_alternance(payload: dict) -> dict:
    result = execute(
        """
        INSERT INTO alternance (
            eleve_id,
            entreprise_id,
            type_contrat,
            poste,
            rythme,
            date_debut,
            date_fin,
            salaire_mensuel
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            payload["eleve_id"],
            payload["entreprise_id"],
            payload["type_contrat"],
            payload["poste"],
            payload["rythme"],
            payload["date_debut"],
            payload.get("date_fin"),
            payload["salaire_mensuel"],
        ),
    )
    return trouver_par_id(list_alternances(), result["lastrowid"], "Alternance introuvable.")


def update_alternance(alternance_id: int, payload: dict) -> dict:
    trouver_par_id(list_alternances(), alternance_id, "Alternance introuvable.")
    sql, params = preparer_update(payload)
    execute(f"UPDATE alternance SET {sql} WHERE id = %s", params + (alternance_id,))
    return trouver_par_id(list_alternances(), alternance_id, "Alternance introuvable.")


def delete_alternance(alternance_id: int) -> dict:
    alternance = trouver_par_id(list_alternances(), alternance_id, "Alternance introuvable.")
    execute("DELETE FROM alternance WHERE id = %s", (alternance_id,))
    return {"message": "Alternance supprimee.", "alternance": alternance}
