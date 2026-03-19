from pydantic import BaseModel, Field


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
    date_cours: str


class InstanceCoursUpdate(BaseModel):
    cours_id: int | None = None
    prof_id: int | None = None
    date_cours: str | None = None


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
    date_inscription: str


class ClubInscriptionUpdate(BaseModel):
    club_id: int | None = None
    eleve_id: int | None = None
    role_membre: str | None = Field(default=None, min_length=2, max_length=120)
    date_inscription: str | None = None
