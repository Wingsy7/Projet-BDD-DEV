"""Requetes SQL simples utilisees par l'API.

Le principe du projet est de garder ici des SELECT assez simples,
puis de faire les calculs, tris et regroupements dans traitements.py.
"""

STUDENT_SELECT = """
SELECT
    e.id,
    e.nom,
    e.email,
    e.age,
    e.promotion_id,
    p.nom AS promotion_nom,
    p.annee AS promotion_annee,
    s.id AS specialite_id,
    s.nom AS specialite_nom,
    d.infos AS dossier_infos,
    d.avertissement_travail,
    d.avertissement_comportement
FROM eleve e
JOIN promotion p ON p.id = e.promotion_id
JOIN specialite s ON s.id = p.specialite_id
LEFT JOIN dossier d ON d.eleve_id = e.id
"""

PROMOTION_SELECT = """
SELECT
    p.id,
    p.nom,
    p.annee,
    p.specialite_id,
    s.nom AS specialite_nom
FROM promotion p
JOIN specialite s ON s.id = p.specialite_id
"""

COURSE_SELECT = """
SELECT
    c.id,
    c.nom,
    c.niveau,
    c.specialite_id,
    s.nom AS specialite_nom
FROM cours c
LEFT JOIN specialite s ON s.id = c.specialite_id
"""

PROF_SELECT = """
SELECT
    p.id,
    p.nom,
    p.email,
    p.age
FROM prof p
"""

NOTE_SELECT = """
SELECT
    n.id,
    n.valeur,
    n.commentaire,
    n.eleve_id,
    e.nom AS eleve_nom,
    n.cours_id,
    c.nom AS cours_nom,
    n.prof_id,
    p.nom AS prof_nom,
    pr.id AS promotion_id,
    pr.nom AS promotion_nom,
    s.id AS specialite_id,
    s.nom AS specialite_nom
FROM note n
JOIN eleve e ON e.id = n.eleve_id
JOIN cours c ON c.id = n.cours_id
LEFT JOIN prof p ON p.id = n.prof_id
JOIN promotion pr ON pr.id = e.promotion_id
JOIN specialite s ON s.id = pr.specialite_id
"""

ABSENCE_SELECT = """
SELECT
    a.id,
    a.eleve_id,
    e.nom AS eleve_nom,
    a.instance_cours_id,
    a.duree_minutes,
    a.justificatif,
    ic.cours_id,
    c.nom AS cours_nom,
    ic.prof_id,
    p.nom AS prof_nom,
    ic.date_cours
FROM absence a
JOIN eleve e ON e.id = a.eleve_id
JOIN instance_cours ic ON ic.id = a.instance_cours_id
JOIN cours c ON c.id = ic.cours_id
JOIN prof p ON p.id = ic.prof_id
"""

DOSSIER_SELECT = """
SELECT
    d.id,
    d.eleve_id,
    e.nom AS eleve_nom,
    d.infos,
    d.avertissement_travail,
    d.avertissement_comportement
FROM dossier d
JOIN eleve e ON e.id = d.eleve_id
"""

INSTANCE_SELECT = """
SELECT
    ic.id,
    ic.cours_id,
    c.nom AS cours_nom,
    ic.prof_id,
    p.nom AS prof_nom,
    ic.date_cours
FROM instance_cours ic
JOIN cours c ON c.id = ic.cours_id
JOIN prof p ON p.id = ic.prof_id
"""

CLUB_SELECT = """
SELECT
    c.id,
    c.nom,
    c.categorie,
    c.budget_annuel,
    c.responsable_prof_id,
    p.nom AS responsable_prof_nom
FROM club c
LEFT JOIN prof p ON p.id = c.responsable_prof_id
"""

CLUB_INSCRIPTION_SELECT = """
SELECT
    ic.id,
    ic.club_id,
    c.nom AS club_nom,
    ic.eleve_id,
    e.nom AS eleve_nom,
    ic.role_membre,
    ic.date_inscription
FROM inscription_club ic
JOIN club c ON c.id = ic.club_id
JOIN eleve e ON e.id = ic.eleve_id
"""

ENTREPRISE_SELECT = """
SELECT
    e.id,
    e.nom,
    e.secteur,
    e.ville,
    e.email_contact,
    e.telephone
FROM entreprise e
"""

ALTERNANCE_SELECT = """
SELECT
    a.id,
    a.eleve_id,
    el.nom AS eleve_nom,
    a.entreprise_id,
    en.nom AS entreprise_nom,
    en.secteur AS entreprise_secteur,
    en.ville AS entreprise_ville,
    a.type_contrat,
    a.poste,
    a.rythme,
    a.date_debut,
    a.date_fin,
    a.salaire_mensuel
FROM alternance a
JOIN eleve el ON el.id = a.eleve_id
JOIN entreprise en ON en.id = a.entreprise_id
"""
