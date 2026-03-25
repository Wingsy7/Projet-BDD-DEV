from fastapi import FastAPI, Query

from . import traitements
from .schemas import (
    AlternanceCreate,
    AlternanceUpdate,
    ClubCreate,
    ClubInscriptionCreate,
    ClubInscriptionUpdate,
    ClubUpdate,
    DossierUpdate,
    EleveCreate,
    EleveUpdate,
    EntrepriseCreate,
    EntrepriseUpdate,
    InstanceCoursCreate,
    InstanceCoursUpdate,
    NoteCreate,
    NoteUpdate,
    ProfCreate,
    ProfUpdate,
)


app = FastAPI(title="API ecole")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# Eleves

@app.get("/eleve")
def list_eleves() -> list[dict]:
    return traitements.list_eleves()


@app.get("/admin/eleves")
def list_eleves_admin() -> list[dict]:
    return traitements.list_eleves_admin()


@app.get("/eleve/avertis")
def list_eleves_avertis() -> list[dict]:
    return traitements.list_eleves_avertis()


@app.get("/eleve/bonne_notes")
def list_eleves_bonne_notes() -> list[dict]:
    return traitements.list_eleves_bonne_notes()


@app.get("/eleve/{eleve_id}/absence")
def get_eleve_absence(eleve_id: int) -> dict:
    return traitements.get_absence_hours_for_eleve(eleve_id)


@app.get("/eleve/{eleve_id}/clubs")
def get_eleve_clubs(eleve_id: int) -> list[dict]:
    return traitements.list_eleve_clubs(eleve_id)


@app.get("/eleve/{eleve_id}/alternance")
def get_eleve_alternance(eleve_id: int) -> list[dict]:
    return traitements.list_eleve_alternances(eleve_id)


@app.get("/eleve/{eleve_id}")
def get_eleve(eleve_id: int) -> dict:
    return traitements.get_eleve(eleve_id)


@app.post("/eleve")
def create_eleve(payload: EleveCreate) -> dict:
    return traitements.create_eleve(payload.model_dump())


@app.put("/eleve/{eleve_id}")
def update_eleve(eleve_id: int, payload: EleveUpdate) -> dict:
    return traitements.update_eleve(eleve_id, payload.model_dump())


@app.delete("/eleve/{eleve_id}")
def delete_eleve(eleve_id: int) -> dict:
    return traitements.delete_eleve(eleve_id)


# Notes

@app.get("/notes/{eleve_id}")
def get_notes_for_eleve(eleve_id: int) -> list[dict]:
    return traitements.list_notes_for_eleve(eleve_id)


@app.get("/note")
def get_notes(
    par: str | None = None,
    type_param: str | None = Query(default=None, alias="type"),
) -> list[dict] | dict:
    group_value = par or type_param
    if group_value:
        return traitements.group_notes_by(group_value)
    return traitements.list_note_records()


@app.post("/note")
def create_note(payload: NoteCreate) -> dict:
    return traitements.create_note(payload.model_dump())


@app.put("/note/{note_id}")
def update_note(note_id: int, payload: NoteUpdate) -> dict:
    return traitements.update_note(note_id, payload.model_dump())


# Profs et dossiers

@app.get("/prof")
def list_profs() -> list[dict]:
    return traitements.list_profs()


@app.get("/prof/severe")
def list_profs_severes() -> list[dict]:
    return traitements.list_profs_severes()


@app.post("/prof")
def create_prof(payload: ProfCreate) -> dict:
    return traitements.create_prof(payload.model_dump())


@app.put("/prof/{prof_id}")
def update_prof(prof_id: int, payload: ProfUpdate) -> dict:
    return traitements.update_prof(prof_id, payload.model_dump())


@app.delete("/prof/{prof_id}")
def delete_prof(prof_id: int) -> dict:
    return traitements.delete_prof(prof_id)


@app.get("/dossier")
def list_dossiers() -> list[dict]:
    return traitements.list_dossiers()


@app.put("/dossier/{eleve_id}")
def update_dossier(eleve_id: int, payload: DossierUpdate) -> dict:
    return traitements.update_dossier(eleve_id, payload.model_dump())


# Instances, promotions et cours

@app.get("/instances")
def list_instances() -> list[dict]:
    return traitements.list_instances()


@app.post("/instances")
def create_instance(payload: InstanceCoursCreate) -> dict:
    return traitements.create_instance(payload.model_dump())


@app.put("/instances/{instance_id}")
def update_instance(instance_id: int, payload: InstanceCoursUpdate) -> dict:
    return traitements.update_instance(instance_id, payload.model_dump())


@app.delete("/instances/{instance_id}")
def delete_instance(instance_id: int) -> dict:
    return traitements.delete_instance(instance_id)


@app.get("/promotion")
def list_promotions() -> list[dict]:
    return traitements.list_promotions()


@app.get("/cours")
def list_cours() -> list[dict]:
    return traitements.list_courses()


@app.get("/specialites/{specialite_id}/cours")
def list_specialite_cours(specialite_id: int) -> list[dict]:
    return traitements.list_specialite_cours(specialite_id)


@app.get("/specialites/{specialite_id}/prom")
def list_specialite_promotions(specialite_id: int) -> list[dict]:
    return traitements.list_specialite_promotions(specialite_id)


# Clubs

@app.get("/clubs")
def list_clubs() -> list[dict]:
    return traitements.list_clubs()


@app.get("/clubs/{club_id}/membres")
def list_club_members(club_id: int) -> list[dict]:
    return traitements.list_club_members(club_id)


@app.post("/clubs")
def create_club(payload: ClubCreate) -> dict:
    return traitements.create_club(payload.model_dump())


@app.put("/clubs/{club_id}")
def update_club(club_id: int, payload: ClubUpdate) -> dict:
    return traitements.update_club(club_id, payload.model_dump())


@app.delete("/clubs/{club_id}")
def delete_club(club_id: int) -> dict:
    return traitements.delete_club(club_id)


@app.get("/club-inscriptions")
def list_club_inscriptions() -> list[dict]:
    return traitements.list_club_inscriptions()


@app.post("/club-inscriptions")
def create_club_inscription(payload: ClubInscriptionCreate) -> dict:
    return traitements.create_club_inscription(payload.model_dump())


@app.put("/club-inscriptions/{inscription_id}")
def update_club_inscription(inscription_id: int, payload: ClubInscriptionUpdate) -> dict:
    return traitements.update_club_inscription(inscription_id, payload.model_dump())


@app.delete("/club-inscriptions/{inscription_id}")
def delete_club_inscription(inscription_id: int) -> dict:
    return traitements.delete_club_inscription(inscription_id)


# Entreprises et alternance

@app.get("/entreprises")
def list_entreprises() -> list[dict]:
    return traitements.list_entreprises()


@app.post("/entreprises")
def create_entreprise(payload: EntrepriseCreate) -> dict:
    return traitements.create_entreprise(payload.model_dump())


@app.put("/entreprises/{entreprise_id}")
def update_entreprise(entreprise_id: int, payload: EntrepriseUpdate) -> dict:
    return traitements.update_entreprise(entreprise_id, payload.model_dump())


@app.delete("/entreprises/{entreprise_id}")
def delete_entreprise(entreprise_id: int) -> dict:
    return traitements.delete_entreprise(entreprise_id)


@app.get("/alternances")
def list_alternances() -> list[dict]:
    return traitements.list_alternances()


@app.post("/alternances")
def create_alternance(payload: AlternanceCreate) -> dict:
    return traitements.create_alternance(payload.model_dump())


@app.put("/alternances/{alternance_id}")
def update_alternance(alternance_id: int, payload: AlternanceUpdate) -> dict:
    return traitements.update_alternance(alternance_id, payload.model_dump())


@app.delete("/alternances/{alternance_id}")
def delete_alternance(alternance_id: int) -> dict:
    return traitements.delete_alternance(alternance_id)
