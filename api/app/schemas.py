from datetime import date, datetime

from pydantic import BaseModel, Field


# Modeles utilises pour verifier les donnees recues

class EleveCreate(BaseModel):
    nom: str = Field(min_length=2, max_length=150)
    email: str = Field(min_length=5, max_length=190)
    age: int = Field(ge=15, le=99)
    promotion_id: int


class EleveUpdate(BaseModel):
    nom: str | None = Field(default=None, min_length=2, max_length=150)
    email: str | None = Field(default=None, min_length=5, max_length=190)
    age: int | None = Field(default=None, ge=15, le=99)
    promotion_id: int | None = None


class ProfCreate(BaseModel):
    nom: str = Field(min_length=2, max_length=150)
    email: str = Field(min_length=5, max_length=190)
    age: int = Field(ge=18, le=99)


class ProfUpdate(BaseModel):
    nom: str | None = Field(default=None, min_length=2, max_length=150)
    email: str | None = Field(default=None, min_length=5, max_length=190)
    age: int | None = Field(default=None, ge=18, le=99)


class NoteCreate(BaseModel):
    eleve_id: int
    cours_id: int
    prof_id: int | None = None
    valeur: float = Field(ge=0, le=20)
    commentaire: str | None = Field(default=None, max_length=255)


class NoteUpdate(BaseModel):
    eleve_id: int | None = None
    cours_id: int | None = None
    prof_id: int | None = None
    valeur: float | None = Field(default=None, ge=0, le=20)
    commentaire: str | None = Field(default=None, max_length=255)


class DossierUpdate(BaseModel):
    infos: str | None = Field(default=None, max_length=2550)
    avertissement_travail: bool | None = None
    avertissement_comportement: bool | None = None


class InstanceCoursCreate(BaseModel):
    cours_id: int
    prof_id: int
    date_cours: datetime


class InstanceCoursUpdate(BaseModel):
    cours_id: int | None = None
    prof_id: int | None = None
    date_cours: datetime | None = None


class ClubCreate(BaseModel):
    nom: str = Field(min_length=2, max_length=150)
    categorie: str = Field(min_length=2, max_length=120)
    budget_annuel: float = Field(ge=0)
    responsable_prof_id: int | None = None


class ClubUpdate(BaseModel):
    nom: str | None = Field(default=None, min_length=2, max_length=150)
    categorie: str | None = Field(default=None, min_length=2, max_length=120)
    budget_annuel: float | None = Field(default=None, ge=0)
    responsable_prof_id: int | None = None


class ClubInscriptionCreate(BaseModel):
    club_id: int
    eleve_id: int
    role_membre: str = Field(min_length=2, max_length=120)
    date_inscription: date


class ClubInscriptionUpdate(BaseModel):
    club_id: int | None = None
    eleve_id: int | None = None
    role_membre: str | None = Field(default=None, min_length=2, max_length=120)
    date_inscription: date | None = None


class EntrepriseCreate(BaseModel):
    nom: str = Field(min_length=2, max_length=150)
    secteur: str = Field(min_length=2, max_length=120)
    ville: str = Field(min_length=2, max_length=120)
    email_contact: str | None = Field(default=None, min_length=5, max_length=190)
    telephone: str | None = Field(default=None, max_length=40)


class EntrepriseUpdate(BaseModel):
    nom: str | None = Field(default=None, min_length=2, max_length=150)
    secteur: str | None = Field(default=None, min_length=2, max_length=120)
    ville: str | None = Field(default=None, min_length=2, max_length=120)
    email_contact: str | None = Field(default=None, min_length=5, max_length=190)
    telephone: str | None = Field(default=None, max_length=40)


class AlternanceCreate(BaseModel):
    eleve_id: int
    entreprise_id: int
    type_contrat: str = Field(min_length=2, max_length=80)
    poste: str = Field(min_length=2, max_length=150)
    rythme: str = Field(min_length=2, max_length=120)
    date_debut: date
    date_fin: date | None = None
    salaire_mensuel: float = Field(ge=0)


class AlternanceUpdate(BaseModel):
    eleve_id: int | None = None
    entreprise_id: int | None = None
    type_contrat: str | None = Field(default=None, min_length=2, max_length=80)
    poste: str | None = Field(default=None, min_length=2, max_length=150)
    rythme: str | None = Field(default=None, min_length=2, max_length=120)
    date_debut: date | None = None
    date_fin: date | None = None
    salaire_mensuel: float | None = Field(default=None, ge=0)
