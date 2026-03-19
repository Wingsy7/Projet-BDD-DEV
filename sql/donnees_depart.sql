USE cozma_miroslav;

INSERT INTO specialite (id, nom) VALUES
    (1, 'Developpement'),
    (2, 'Cybersecurite'),
    (3, 'Data IA');

INSERT INTO promotion (id, nom, annee, specialite_id) VALUES
    (1, 'DEV2026', 2026, 1),
    (2, 'CYB2026', 2026, 2),
    (3, 'DATA2026', 2026, 3),
    (4, 'DEV2027', 2027, 1);

INSERT INTO cours (id, nom, niveau, specialite_id) VALUES
    (1, 'Python 1', 1, 1),
    (2, 'API REST', 2, 1),
    (3, 'Reseau securise', 2, 2),
    (4, 'SQL avance', 2, NULL),
    (5, 'Analyse de donnees', 3, 3),
    (6, 'Communication pro', 1, NULL);

INSERT INTO prof (id, nom, email, age) VALUES
    (1, 'Alice Martin', 'alice.martin@ecole.local', 38),
    (2, 'Bernard Leroy', 'bernard.leroy@ecole.local', 45),
    (3, 'Clara Petit', 'clara.petit@ecole.local', 34),
    (4, 'David Morel', 'david.morel@ecole.local', 51);

INSERT INTO prof_cours (prof_id, cours_id) VALUES
    (1, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (4, 6),
    (3, 4);

INSERT INTO club (id, nom, categorie, budget_annuel, responsable_prof_id) VALUES
    (1, 'Club Robotique', 'Technique', 2500.00, 1),
    (2, 'Club Basket', 'Sport', 1800.00, 4),
    (3, 'Club CTF', 'Cyber', 2200.00, 2);

INSERT INTO eleve (id, nom, email, age, promotion_id) VALUES
    (1, 'Julie Bernard', 'julie.bernard@ecole.local', 19, 1),
    (2, 'Karim Haddad', 'karim.haddad@ecole.local', 17, 1),
    (3, 'Lea Dubois', 'lea.dubois@ecole.local', 21, 2),
    (4, 'Martin Lopez', 'martin.lopez@ecole.local', 20, 2),
    (5, 'Nora Simon', 'nora.simon@ecole.local', 18, 3),
    (6, 'Paul Renard', 'paul.renard@ecole.local', 22, 3),
    (7, 'Ines Petit', 'ines.petit@ecole.local', 16, 4),
    (8, 'Sami Laurent', 'sami.laurent@ecole.local', 23, 1);

UPDATE dossier
SET infos = 'eleve reguliere, dossier a jour'
WHERE eleve_id = 1;

UPDATE dossier
SET infos = 'mineur - suivi mensuel', avertissement_travail = 1
WHERE eleve_id = 2;

UPDATE dossier
SET infos = 'bonne progression'
WHERE eleve_id = 3;

UPDATE dossier
SET infos = 'suivi comportement', avertissement_comportement = 1
WHERE eleve_id = 4;

UPDATE dossier
SET infos = 'tres bon niveau'
WHERE eleve_id = 5;

UPDATE dossier
SET infos = 'besoin de regularite'
WHERE eleve_id = 6;

UPDATE dossier
SET infos = 'mineur - accompagnement pedagogique'
WHERE eleve_id = 7;

UPDATE dossier
SET infos = 'excellent investissement'
WHERE eleve_id = 8;

INSERT INTO eleve_cours (eleve_id, cours_id) VALUES
    (1, 1), (1, 2), (1, 4), (1, 6),
    (2, 1), (2, 2), (2, 6),
    (3, 3), (3, 4), (3, 6),
    (4, 3), (4, 4), (4, 6),
    (5, 4), (5, 5), (5, 6),
    (6, 4), (6, 5), (6, 6),
    (7, 1), (7, 6),
    (8, 1), (8, 2), (8, 4), (8, 6);

INSERT INTO instance_cours (id, cours_id, prof_id, date_cours) VALUES
    (1, 1, 1, '2026-02-02 09:00:00'),
    (2, 2, 1, '2026-02-04 14:00:00'),
    (3, 3, 2, '2026-02-03 10:00:00'),
    (4, 4, 2, '2026-02-05 11:00:00'),
    (5, 5, 3, '2026-02-06 13:30:00'),
    (6, 6, 4, '2026-02-07 16:00:00'),
    (7, 4, 3, '2026-02-10 11:00:00'),
    (8, 2, 1, '2026-02-12 14:00:00');

INSERT INTO absence (id, eleve_id, instance_cours_id, duree_minutes, justificatif) VALUES
    (1, 2, 1, 45, 1),
    (2, 2, 2, 120, 0),
    (3, 3, 3, 60, 1),
    (4, 4, 4, 180, 0),
    (5, 6, 5, 90, 1),
    (6, 7, 1, 240, 0),
    (7, 8, 8, 30, 1);

INSERT INTO note (id, eleve_id, cours_id, prof_id, valeur, commentaire) VALUES
    (1, 1, 1, 1, 14.50, 'bon demarrage'),
    (2, 1, 2, 1, 15.00, 'application serieuse'),
    (3, 1, 4, 2, 13.00, 'requetes propres'),
    (4, 2, 1, 1, 9.50, 'bases fragiles'),
    (5, 2, 2, 1, 11.00, 'progression visible'),
    (6, 3, 3, 2, 12.50, 'bonne maitrise'),
    (7, 3, 4, 2, 8.00, 'a consolider'),
    (8, 4, 3, 2, 6.50, 'travail insuffisant'),
    (9, 4, 4, 3, 7.00, 'revoir les jointures'),
    (10, 5, 5, 3, 16.50, 'excellent'),
    (11, 5, 4, 3, 14.00, 'serieux'),
    (12, 6, 5, 3, 10.50, 'correct'),
    (13, 6, 4, 2, 9.00, 'manque de precision'),
    (14, 7, 1, 1, 12.00, 'bonne implication'),
    (15, 8, 1, 1, 17.00, 'tres bon niveau'),
    (16, 8, 2, 1, 16.00, 'autonome'),
    (17, 8, 4, 3, 15.50, 'maitrise solide');

INSERT INTO inscription_club (id, club_id, eleve_id, role_membre, date_inscription) VALUES
    (1, 1, 1, 'presidente', '2026-01-10'),
    (2, 1, 8, 'membre', '2026-01-12'),
    (3, 2, 6, 'capitaine', '2026-01-08'),
    (4, 2, 4, 'membre', '2026-01-09'),
    (5, 3, 3, 'membre', '2026-01-15'),
    (6, 3, 4, 'membre', '2026-01-16'),
    (7, 3, 2, 'membre', '2026-01-20');

CALL sp_recalculer_classement_eleves();
