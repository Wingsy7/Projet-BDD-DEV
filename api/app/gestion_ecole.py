from collections import defaultdict

from fastapi import HTTPException

from .connexion_bdd import execute, fetch_all
from .requetes_sql import (
    ABSENCE_SELECT,
    CLUB_INSCRIPTION_SELECT,
    CLUB_SELECT,
    COURSE_SELECT,
    DOSSIER_SELECT,
    INSTANCE_SELECT,
    NOTE_SELECT,
    PROF_SELECT,
    PROMOTION_SELECT,
    STUDENT_SELECT,
)


class GestionEcole:
    def _format_eleve_admin(self, row: dict) -> dict:
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

    def _format_eleve_simple(self, row: dict) -> dict:
        return {
            "nom": row["nom"],
            "age": row["age"],
        }

    def _format_note_api(self, row: dict) -> dict:
        return {
            "note": float(row["valeur"]),
            "matiere": row["cours_nom"],
            "nom_eleve": row["eleve_nom"],
        }

    def _format_note_admin(self, row: dict) -> dict:
        row["valeur"] = float(row["valeur"])
        return row

    def _verifier(self, item: dict | None, message: str) -> dict:
        if item is None:
            raise HTTPException(status_code=404, detail=message)
        return item

    def _trouver_par_id(self, rows: list[dict], item_id: int, message: str) -> dict:
        for row in rows:
            if row["id"] == item_id:
                return row
        raise HTTPException(status_code=404, detail=message)

    def _preparer_update(self, payload: dict) -> tuple[str, tuple]:
        values = {key: value for key, value in payload.items() if value is not None}
        if not values:
            raise HTTPException(status_code=400, detail="Aucune valeur a modifier.")
        sql = ", ".join(f"{key} = %s" for key in values)
        params = tuple(values.values())
        return sql, params

    def list_eleves(self) -> list[dict]:
        return [self._format_eleve_simple(row) for row in fetch_all(STUDENT_SELECT)]

    def list_eleves_admin(self) -> list[dict]:
        return [self._format_eleve_admin(row) for row in fetch_all(STUDENT_SELECT)]

    def get_eleve(self, eleve_id: int) -> dict:
        eleve = next(
            (row for row in self.list_eleves_admin() if row["id"] == eleve_id),
            None,
        )
        return self._verifier(eleve, "Eleve introuvable.")

    def list_promotions(self) -> list[dict]:
        return fetch_all(PROMOTION_SELECT)

    def list_specialite_cours(self, specialite_id: int) -> list[dict]:
        rows = fetch_all(COURSE_SELECT)
        return [
            {"id": row["id"], "nom": row["nom"], "niveau": row["niveau"]}
            for row in rows
            if row["specialite_id"] == specialite_id
        ]

    def list_specialite_promotions(self, specialite_id: int) -> list[dict]:
        rows = fetch_all(PROMOTION_SELECT)
        return [
            {"id": row["id"], "nom": row["nom"], "annee": row["annee"]}
            for row in rows
            if row["specialite_id"] == specialite_id
        ]

    def list_notes_admin(self) -> list[dict]:
        return [self._format_note_admin(row) for row in fetch_all(NOTE_SELECT)]

    def list_notes_for_eleve(self, eleve_id: int) -> list[dict]:
        self.get_eleve(eleve_id)
        return [
            self._format_note_api(row)
            for row in self.list_notes_admin()
            if row["eleve_id"] == eleve_id
        ]

    def list_eleves_avertis(self) -> list[dict]:
        return [
            {
                "nom": eleve["nom"],
                "age": eleve["age"],
                "avertissement_travail": eleve["dossier"]["avertissement_travail"],
                "avertissement_comportement": eleve["dossier"]["avertissement_comportement"],
            }
            for eleve in self.list_eleves_admin()
            if eleve["dossier"]["avertissement_travail"]
            or eleve["dossier"]["avertissement_comportement"]
        ]

    def list_eleves_bonne_notes(self) -> list[dict]:
        grouped: dict[int, dict] = {}
        for row in self.list_notes_admin():
            current = grouped.setdefault(
                row["eleve_id"],
                {
                    "nom": row["eleve_nom"],
                    "notes": [],
                },
            )
            current["notes"].append(row["valeur"])

        results = []
        for values in grouped.values():
            moyenne = round(sum(values["notes"]) / len(values["notes"]), 2)
            if moyenne > 12:
                results.append(
                    {
                        "nom": values["nom"],
                        "moyenne_generale": moyenne,
                    }
                )

        results.sort(key=lambda item: item["moyenne_generale"], reverse=True)
        return results

    def list_profs(self) -> list[dict]:
        return fetch_all(PROF_SELECT)

    def list_profs_severes(self) -> list[dict]:
        grouped: dict[int, dict] = {}
        for row in self.list_notes_admin():
            prof_id = row["prof_id"]
            if prof_id is None:
                continue
            current = grouped.setdefault(
                prof_id,
                {
                    "nom": row["prof_nom"],
                    "notes": [],
                },
            )
            current["notes"].append(row["valeur"])

        results = []
        for values in grouped.values():
            moyenne = round(sum(values["notes"]) / len(values["notes"]), 2)
            if moyenne < 8:
                results.append(
                    {
                        "nom": values["nom"],
                        "moyenne_des_notes_donnees": moyenne,
                    }
                )

        results.sort(key=lambda item: item["moyenne_des_notes_donnees"])
        return results

    def get_absence_hours_for_eleve(self, eleve_id: int) -> dict:
        eleve = self.get_eleve(eleve_id)
        rows = [row for row in fetch_all(ABSENCE_SELECT) if row["eleve_id"] == eleve_id]
        minutes = sum(row["duree_minutes"] for row in rows)
        return {
            "nom_eleve": eleve["nom"],
            "heures_absence": round(minutes / 60, 2),
        }

    def group_notes_by(self, par: str) -> dict:
        choices = {
            "eleve": "eleve_nom",
            "prof": "prof_nom",
            "cours": "cours_nom",
            "promotion": "promotion_nom",
        }
        if par not in choices:
            raise HTTPException(status_code=400, detail="Le parametre 'par' est invalide.")

        key_name = choices[par]
        grouped: dict[str, list[dict]] = defaultdict(list)

        for row in self.list_notes_admin():
            label = row[key_name] or "Non renseigne"
            grouped[label].append(self._format_note_api(row))

        return dict(grouped)

    def list_instances(self) -> list[dict]:
        return fetch_all(INSTANCE_SELECT)

    def list_dossiers(self) -> list[dict]:
        rows = fetch_all(DOSSIER_SELECT)
        for row in rows:
            row["avertissement_travail"] = bool(row["avertissement_travail"])
            row["avertissement_comportement"] = bool(row["avertissement_comportement"])
        return rows

    def list_clubs(self) -> list[dict]:
        clubs = fetch_all(CLUB_SELECT)
        inscriptions = fetch_all(CLUB_INSCRIPTION_SELECT)
        member_count_by_club: dict[int, int] = defaultdict(int)
        for inscription in inscriptions:
            member_count_by_club[inscription["club_id"]] += 1
        for club in clubs:
            club["budget_annuel"] = float(club["budget_annuel"])
            club["nombre_membres"] = member_count_by_club[club["id"]]
        return clubs

    def list_club_members(self, club_id: int) -> list[dict]:
        self._trouver_par_id(self.list_clubs(), club_id, "Club introuvable.")
        return [
            {
                "eleve_id": row["eleve_id"],
                "nom_eleve": row["eleve_nom"],
                "role_membre": row["role_membre"],
                "date_inscription": row["date_inscription"],
            }
            for row in fetch_all(CLUB_INSCRIPTION_SELECT)
            if row["club_id"] == club_id
        ]

    def list_eleve_clubs(self, eleve_id: int) -> list[dict]:
        self.get_eleve(eleve_id)
        return [
            {
                "club_id": row["club_id"],
                "club_nom": row["club_nom"],
                "role_membre": row["role_membre"],
                "date_inscription": row["date_inscription"],
            }
            for row in fetch_all(CLUB_INSCRIPTION_SELECT)
            if row["eleve_id"] == eleve_id
        ]

    def list_courses(self) -> list[dict]:
        return fetch_all(COURSE_SELECT)

    def create_eleve(self, payload: dict) -> dict:
        result = execute(
            """
            INSERT INTO eleve (nom, email, age, promotion_id)
            VALUES (%s, %s, %s, %s)
            """,
            (
                payload["nom"],
                payload["email"],
                payload["age"],
                payload["promotion_id"],
            ),
        )
        return self.get_eleve(result["lastrowid"])

    def update_eleve(self, eleve_id: int, payload: dict) -> dict:
        self.get_eleve(eleve_id)
        sql, params = self._preparer_update(payload)
        execute(f"UPDATE eleve SET {sql} WHERE id = %s", params + (eleve_id,))
        return self.get_eleve(eleve_id)

    def delete_eleve(self, eleve_id: int) -> dict:
        eleve = self.get_eleve(eleve_id)
        execute("DELETE FROM eleve WHERE id = %s", (eleve_id,))
        return {"message": "Eleve supprime.", "eleve": eleve}

    def create_prof(self, payload: dict) -> dict:
        result = execute(
            """
            INSERT INTO prof (nom, email, age)
            VALUES (%s, %s, %s)
            """,
            (payload["nom"], payload["email"], payload["age"]),
        )
        return self._trouver_par_id(self.list_profs(), result["lastrowid"], "Prof introuvable.")

    def update_prof(self, prof_id: int, payload: dict) -> dict:
        self._trouver_par_id(self.list_profs(), prof_id, "Prof introuvable.")
        sql, params = self._preparer_update(payload)
        execute(f"UPDATE prof SET {sql} WHERE id = %s", params + (prof_id,))
        return self._trouver_par_id(self.list_profs(), prof_id, "Prof introuvable.")

    def delete_prof(self, prof_id: int) -> dict:
        prof = self._trouver_par_id(self.list_profs(), prof_id, "Prof introuvable.")
        execute("DELETE FROM prof WHERE id = %s", (prof_id,))
        return {"message": "Prof supprime.", "prof": prof}

    def create_note(self, payload: dict) -> dict:
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
        return self._trouver_par_id(self.list_notes_admin(), result["lastrowid"], "Note introuvable.")

    def update_note(self, note_id: int, payload: dict) -> dict:
        self._trouver_par_id(self.list_notes_admin(), note_id, "Note introuvable.")
        sql, params = self._preparer_update(payload)
        execute(f"UPDATE note SET {sql} WHERE id = %s", params + (note_id,))
        return self._trouver_par_id(self.list_notes_admin(), note_id, "Note introuvable.")

    def list_note_records(self) -> list[dict]:
        return self.list_notes_admin()

    def update_dossier(self, eleve_id: int, payload: dict) -> dict:
        dossier = next((row for row in self.list_dossiers() if row["eleve_id"] == eleve_id), None)
        self._verifier(dossier, "Dossier introuvable.")
        sql, params = self._preparer_update(payload)
        execute(f"UPDATE dossier SET {sql} WHERE eleve_id = %s", params + (eleve_id,))
        dossier = next((row for row in self.list_dossiers() if row["eleve_id"] == eleve_id), None)
        return self._verifier(dossier, "Dossier introuvable.")

    def create_instance(self, payload: dict) -> dict:
        result = execute(
            """
            INSERT INTO instance_cours (cours_id, prof_id, date_cours)
            VALUES (%s, %s, %s)
            """,
            (payload["cours_id"], payload["prof_id"], payload["date_cours"]),
        )
        return self._trouver_par_id(
            self.list_instances(),
            result["lastrowid"],
            "Instance de cours introuvable.",
        )

    def update_instance(self, instance_id: int, payload: dict) -> dict:
        self._trouver_par_id(self.list_instances(), instance_id, "Instance de cours introuvable.")
        sql, params = self._preparer_update(payload)
        execute(f"UPDATE instance_cours SET {sql} WHERE id = %s", params + (instance_id,))
        return self._trouver_par_id(
            self.list_instances(),
            instance_id,
            "Instance de cours introuvable.",
        )

    def delete_instance(self, instance_id: int) -> dict:
        instance = self._trouver_par_id(
            self.list_instances(),
            instance_id,
            "Instance de cours introuvable.",
        )
        execute("DELETE FROM instance_cours WHERE id = %s", (instance_id,))
        return {"message": "Instance de cours supprimee.", "instance": instance}

    def create_club(self, payload: dict) -> dict:
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
        return self._trouver_par_id(self.list_clubs(), result["lastrowid"], "Club introuvable.")

    def update_club(self, club_id: int, payload: dict) -> dict:
        self._trouver_par_id(self.list_clubs(), club_id, "Club introuvable.")
        sql, params = self._preparer_update(payload)
        execute(f"UPDATE club SET {sql} WHERE id = %s", params + (club_id,))
        return self._trouver_par_id(self.list_clubs(), club_id, "Club introuvable.")

    def delete_club(self, club_id: int) -> dict:
        club = self._trouver_par_id(self.list_clubs(), club_id, "Club introuvable.")
        execute("DELETE FROM club WHERE id = %s", (club_id,))
        return {"message": "Club supprime.", "club": club}

    def list_club_inscriptions(self) -> list[dict]:
        return fetch_all(CLUB_INSCRIPTION_SELECT)

    def create_club_inscription(self, payload: dict) -> dict:
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
        return self._trouver_par_id(
            self.list_club_inscriptions(),
            result["lastrowid"],
            "Inscription club introuvable.",
        )

    def update_club_inscription(self, inscription_id: int, payload: dict) -> dict:
        self._trouver_par_id(
            self.list_club_inscriptions(),
            inscription_id,
            "Inscription club introuvable.",
        )
        sql, params = self._preparer_update(payload)
        execute(
            f"UPDATE inscription_club SET {sql} WHERE id = %s",
            params + (inscription_id,),
        )
        return self._trouver_par_id(
            self.list_club_inscriptions(),
            inscription_id,
            "Inscription club introuvable.",
        )

    def delete_club_inscription(self, inscription_id: int) -> dict:
        inscription = self._trouver_par_id(
            self.list_club_inscriptions(),
            inscription_id,
            "Inscription club introuvable.",
        )
        execute("DELETE FROM inscription_club WHERE id = %s", (inscription_id,))
        return {
            "message": "Inscription club supprimee.",
            "inscription": inscription,
        }
