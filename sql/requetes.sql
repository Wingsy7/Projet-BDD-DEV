USE equipe_6;

-- 1. Requetes simples
-- Liste de tous les eleves (nom et age)
SELECT nom, age
FROM eleve;

-- Liste de tous les eleves (nom et age) de plus de 18 ans
SELECT nom, age
FROM eleve
WHERE age > 18;

-- Liste des notes d'un cours precis inferieures a 10
SELECT n.id, n.valeur, e.nom AS eleve_nom
FROM note n
JOIN eleve e ON e.id = n.eleve_id
WHERE n.cours_id = 4
  AND n.valeur < 10;

-- Liste des eleves avec leur dossier
SELECT e.nom, d.infos, d.avertissement_travail, d.avertissement_comportement
FROM eleve e
JOIN dossier d ON d.eleve_id = e.id;

-- Liste de toutes les absences avec eleve et cours
SELECT
    a.duree_minutes,
    a.justificatif,
    e.nom AS eleve_nom,
    c.nom AS cours_nom
FROM absence a
JOIN eleve e ON e.id = a.eleve_id
JOIN instance_cours ic ON ic.id = a.instance_cours_id
JOIN cours c ON c.id = ic.cours_id;

-- Liste des notes d'un seul eleve avec cours et prof
SELECT
    e.nom AS eleve_nom,
    c.nom AS cours_nom,
    p.nom AS prof_nom,
    n.valeur
FROM note n
JOIN eleve e ON e.id = n.eleve_id
JOIN cours c ON c.id = n.cours_id
LEFT JOIN prof p ON p.id = n.prof_id
WHERE e.nom = 'Julie Bernard';

-- 2. Requetes avec calculs
-- Duree moyenne des absences
SELECT AVG(duree_minutes) AS duree_moyenne_absence
FROM absence;

-- Duree moyenne des absences avec et sans justificatif
SELECT justificatif, AVG(duree_minutes) AS duree_moyenne
FROM absence
GROUP BY justificatif;

-- Duree totale des absences de chaque eleve, ordre croissant
SELECT e.nom, COALESCE(SUM(a.duree_minutes), 0) AS duree_totale
FROM eleve e
LEFT JOIN absence a ON a.eleve_id = e.id
GROUP BY e.id, e.nom
ORDER BY duree_totale ASC;

-- Moyenne des notes de chaque cours, NULL si pas de note
SELECT c.nom, AVG(n.valeur) AS moyenne_cours
FROM cours c
LEFT JOIN note n ON n.cours_id = c.id
GROUP BY c.id, c.nom;

-- Moyenne de chaque eleve dans chaque cours
SELECT e.nom AS eleve_nom, c.nom AS cours_nom, AVG(n.valeur) AS moyenne_eleve_cours
FROM note n
JOIN eleve e ON e.id = n.eleve_id
JOIN cours c ON c.id = n.cours_id
GROUP BY e.id, e.nom, c.id, c.nom;

-- Moyennes superieures a 10 par eleve et cours, ordre decroissant
SELECT e.nom AS eleve_nom, c.nom AS cours_nom, AVG(n.valeur) AS moyenne_eleve_cours
FROM note n
JOIN eleve e ON e.id = n.eleve_id
JOIN cours c ON c.id = n.cours_id
GROUP BY e.id, e.nom, c.id, c.nom
HAVING AVG(n.valeur) > 10
ORDER BY moyenne_eleve_cours DESC;

-- 3. Sous-requetes
-- Sous requete : nombre d'eleves ayant plus de 60 minutes d'absence
SELECT COUNT(*) AS nb_eleves_plus_60_minutes
FROM (
    SELECT eleve_id, SUM(duree_minutes) AS total_absence
    FROM absence
    GROUP BY eleve_id
    HAVING SUM(duree_minutes) > 60
) AS absences_longues;

-- Sous requete : matieres dont la moyenne est superieure a la moyenne globale
SELECT moyenne_par_cours.cours_nom, moyenne_par_cours.moyenne_cours
FROM (
    SELECT c.id, c.nom AS cours_nom, AVG(n.valeur) AS moyenne_cours
    FROM cours c
    JOIN note n ON n.cours_id = c.id
    GROUP BY c.id, c.nom
) AS moyenne_par_cours
WHERE moyenne_par_cours.moyenne_cours > (
    SELECT AVG(valeur)
    FROM note
);

-- Sous requete : repartition des etudiants par specialite en pourcentage
SELECT
    s.nom AS specialite_nom,
    CONCAT(
        ROUND(
            COUNT(e.id) * 100 / (
                SELECT COUNT(*)
                FROM eleve
            ),
            2
        ),
        '%'
    ) AS repartition
FROM specialite s
LEFT JOIN promotion p ON p.specialite_id = s.id
LEFT JOIN eleve e ON e.promotion_id = p.id
GROUP BY s.id, s.nom;

-- 4. Ajouter des donnees
INSERT INTO prof (nom, email, age)
VALUES ('Emma Rossi', 'emma.rossi@ecole.local', 33);

INSERT INTO cours (nom, niveau, specialite_id)
VALUES ('Docker fondamental', 2, 1);

INSERT INTO eleve (nom, email, age, promotion_id)
VALUES ('Hugo Caron', 'hugo.caron@ecole.local', 20, 1);

UPDATE dossier
SET infos = 'dossier cree apres insertion'
WHERE eleve_id = (
    SELECT id
    FROM eleve
    WHERE email = 'hugo.caron@ecole.local'
);

INSERT INTO eleve_cours (eleve_id, cours_id)
VALUES (
    (SELECT id FROM eleve WHERE email = 'hugo.caron@ecole.local'),
    (SELECT id FROM cours WHERE nom = 'Docker fondamental')
);

INSERT INTO prof_cours (prof_id, cours_id)
VALUES (
    (SELECT id FROM prof WHERE email = 'emma.rossi@ecole.local'),
    (SELECT id FROM cours WHERE nom = 'Docker fondamental')
);

-- 5. Modifier des donnees
UPDATE prof
SET age = 34
WHERE email = 'emma.rossi@ecole.local';

UPDATE cours
SET specialite_id = 3
WHERE nom = 'Docker fondamental';

-- 6. Supprimer des donnees
DELETE FROM note
WHERE id = 4;

DELETE FROM prof
WHERE email = 'emma.rossi@ecole.local';

DELETE a
FROM absence a
JOIN eleve e ON e.id = a.eleve_id
WHERE e.nom = 'Martin Lopez';

-- 7. Bonus clubs
-- Membres de chaque club
SELECT
    c.nom AS club,
    e.nom AS eleve,
    ic.role_membre
FROM inscription_club ic
JOIN club c ON c.id = ic.club_id
JOIN eleve e ON e.id = ic.eleve_id
ORDER BY c.nom, e.nom;

-- Nombre de membres par club
SELECT
    c.nom AS club,
    COUNT(ic.id) AS nb_membres
FROM club c
LEFT JOIN inscription_club ic ON ic.club_id = c.id
GROUP BY c.id, c.nom
ORDER BY nb_membres DESC, c.nom ASC;

-- 8. Bonus alternance
-- Contrats eleves / entreprises
SELECT
    e.nom AS eleve,
    en.nom AS entreprise,
    a.type_contrat,
    a.poste,
    a.rythme
FROM alternance a
JOIN eleve e ON e.id = a.eleve_id
JOIN entreprise en ON en.id = a.entreprise_id
ORDER BY en.nom, e.nom;

SELECT
    en.nom AS entreprise,
    COUNT(a.id) AS nb_alternants
FROM entreprise en
LEFT JOIN alternance a ON a.entreprise_id = en.id
GROUP BY en.id, en.nom
ORDER BY nb_alternants DESC, en.nom ASC;
