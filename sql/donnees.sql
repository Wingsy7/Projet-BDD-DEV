USE cozma_miroslav;

-- 1. Specialites, promotions, cours et profs

INSERT INTO specialite (id, nom) VALUES
    (1, 'Developpement'),
    (2, 'Cybersecurite'),
    (3, 'Data IA');

INSERT INTO promotion (id, nom, annee, specialite_id) VALUES
    (1, 'DEV2026', 2026, 1),
    (2, 'CYB2026', 2026, 2),
    (3, 'DATA2026', 2026, 3),
    (4, 'DEV2027', 2027, 1),
    (5, 'CYB2027', 2027, 2),
    (6, 'DATA2027', 2027, 3);

INSERT INTO cours (id, nom, niveau, specialite_id) VALUES
    (1, 'Python 1', 1, 1),
    (2, 'API REST', 2, 1),
    (3, 'Reseau securise', 2, 2),
    (4, 'SQL avance', 2, NULL),
    (5, 'Analyse de donnees', 3, 3),
    (6, 'Communication pro', 1, NULL),
    (7, 'Forensic reseau', 3, 2),
    (8, 'Machine learning applique', 3, 3),
    (9, 'Docker et CI', 2, 1);

INSERT INTO prof (id, nom, email, age) VALUES
    (1, 'Alice Martin', 'alice.martin@ecole.local', 38),
    (2, 'Bernard Leroy', 'bernard.leroy@ecole.local', 45),
    (3, 'Clara Petit', 'clara.petit@ecole.local', 34),
    (4, 'David Morel', 'david.morel@ecole.local', 51),
    (5, 'Elodie Garnier', 'elodie.garnier@ecole.local', 39),
    (6, 'Farid Benali', 'farid.benali@ecole.local', 42),
    (7, 'Gaelle Renaud', 'gaelle.renaud@ecole.local', 36);

INSERT INTO prof_cours (prof_id, cours_id) VALUES
    (1, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (4, 6),
    (3, 4),
    (5, 3),
    (5, 7),
    (6, 5),
    (6, 8),
    (7, 6),
    (7, 9);

INSERT INTO club (id, nom, categorie, budget_annuel, responsable_prof_id) VALUES
    (1, 'Club Robotique', 'Technique', 2500.00, 1),
    (2, 'Club Basket', 'Sport', 1800.00, 4),
    (3, 'Club CTF', 'Cyber', 2200.00, 2),
    (4, 'Club Debat', 'Culture', 1200.00, 7),
    (5, 'Club Open Source', 'Informatique', 1600.00, 1);

INSERT INTO entreprise (id, nom, secteur, ville, email_contact, telephone) VALUES
    (1, 'NovaTech Solutions', 'Developpement logiciel', 'Paris', 'contact@novatech.local', '01 45 22 10 10'),
    (2, 'CyberWall', 'Cybersecurite', 'Lille', 'recrutement@cyberwall.local', '03 20 11 54 20'),
    (3, 'DataPulse', 'Data et IA', 'Lyon', 'talents@datapulse.local', '04 78 33 41 90'),
    (4, 'SecureOps', 'Audit securite', 'Bordeaux', 'jobs@secureops.local', '05 56 40 88 70'),
    (5, 'CloudForge', 'DevOps', 'Nantes', 'contact@cloudforge.local', '02 40 77 60 30'),
    (6, 'GreenData Lab', 'Data durable', 'Grenoble', 'talent@greendata.local', '04 76 52 10 90'),
    (7, 'HexaSecure', 'Cyberdefense', 'Toulouse', 'contact@hexasecure.local', '05 61 77 45 10'),
    (8, 'PixelRiver Studio', 'Applications web', 'Rennes', 'recrutement@pixelriver.local', '02 99 32 19 88'),
    (9, 'BlueKernel Cloud', 'Cloud et automatisation', 'Montpellier', 'jobs@bluekernel.local', '04 67 80 22 14'),
    (10, 'NexaAudit', 'Conseil data', 'Strasbourg', 'talent@nexaaudit.local', '03 88 19 74 50');

-- 2. Eleves

INSERT INTO eleve (id, nom, email, age, promotion_id) VALUES
    (1, 'Julie Bernard', 'julie.bernard@ecole.local', 19, 1),
    (2, 'Karim Haddad', 'karim.haddad@ecole.local', 17, 1),
    (3, 'Lea Dubois', 'lea.dubois@ecole.local', 21, 2),
    (4, 'Martin Lopez', 'martin.lopez@ecole.local', 20, 2),
    (5, 'Nora Simon', 'nora.simon@ecole.local', 18, 3),
    (6, 'Paul Renard', 'paul.renard@ecole.local', 22, 3),
    (7, 'Ines Petit', 'ines.petit@ecole.local', 16, 4),
    (8, 'Sami Laurent', 'sami.laurent@ecole.local', 23, 1),
    (9, 'Amine Bensaid', 'amine.bensaid@ecole.local', 19, 5),
    (10, 'Chloe Mercier', 'chloe.mercier@ecole.local', 20, 6),
    (11, 'Yanis Fontaine', 'yanis.fontaine@ecole.local', 18, 4),
    (12, 'Salome Robert', 'salome.robert@ecole.local', 21, 1),
    (13, 'Mehdi Ouali', 'mehdi.ouali@ecole.local', 19, 2),
    (14, 'Camille Torres', 'camille.torres@ecole.local', 17, 6),
    (15, 'Lucas Perrin', 'lucas.perrin@ecole.local', 22, 3);

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

UPDATE dossier
SET infos = 'profil regulier en cyber'
WHERE eleve_id = 9;

UPDATE dossier
SET infos = 'bonne autonomie sur les projets data'
WHERE eleve_id = 10;

UPDATE dossier
SET infos = 'debuts serieux en developpement'
WHERE eleve_id = 11;

UPDATE dossier
SET infos = 'tres bonne participation en cours'
WHERE eleve_id = 12;

UPDATE dossier
SET infos = 'suivi travail a renforcer', avertissement_travail = 1
WHERE eleve_id = 13;

UPDATE dossier
SET infos = 'mineure - suivi alternance a preparer'
WHERE eleve_id = 14;

UPDATE dossier
SET infos = 'niveau stable, bon esprit d equipe'
WHERE eleve_id = 15;

-- 3. Cours suivis par les eleves

INSERT INTO eleve_cours (eleve_id, cours_id) VALUES
    (1, 1), (1, 2), (1, 4), (1, 6),
    (2, 1), (2, 2), (2, 6),
    (3, 3), (3, 4), (3, 6),
    (4, 3), (4, 4), (4, 6),
    (5, 4), (5, 5), (5, 6),
    (6, 4), (6, 5), (6, 6),
    (7, 1), (7, 6),
    (8, 1), (8, 2), (8, 4), (8, 6),
    (9, 3), (9, 4), (9, 6), (9, 7),
    (10, 4), (10, 5), (10, 6), (10, 8),
    (11, 1), (11, 2), (11, 6), (11, 9),
    (12, 1), (12, 2), (12, 4), (12, 6), (12, 9),
    (13, 3), (13, 4), (13, 6), (13, 7),
    (14, 4), (14, 5), (14, 6), (14, 8),
    (15, 4), (15, 5), (15, 6), (15, 8);

-- 4. Seances, absences et notes

INSERT INTO instance_cours (id, cours_id, prof_id, date_cours) VALUES
    (1, 1, 1, '2026-02-02 09:00:00'),
    (2, 2, 1, '2026-02-04 14:00:00'),
    (3, 3, 2, '2026-02-03 10:00:00'),
    (4, 4, 2, '2026-02-05 11:00:00'),
    (5, 5, 3, '2026-02-06 13:30:00'),
    (6, 6, 4, '2026-02-07 16:00:00'),
    (7, 4, 3, '2026-02-10 11:00:00'),
    (8, 2, 1, '2026-02-12 14:00:00'),
    (9, 7, 5, '2026-02-14 10:00:00'),
    (10, 8, 6, '2026-02-16 09:30:00'),
    (11, 9, 7, '2026-02-17 15:00:00'),
    (12, 5, 6, '2026-02-18 13:30:00'),
    (13, 3, 5, '2026-02-19 10:00:00'),
    (14, 9, 7, '2026-02-20 15:00:00'),
    (15, 8, 6, '2026-02-21 09:30:00');

INSERT INTO absence (id, eleve_id, instance_cours_id, duree_minutes, justificatif) VALUES
    (1, 2, 1, 45, 1),
    (2, 2, 2, 120, 0),
    (3, 3, 3, 60, 1),
    (4, 4, 4, 180, 0),
    (5, 6, 5, 90, 1),
    (6, 7, 1, 240, 0),
    (7, 8, 8, 30, 1),
    (8, 9, 9, 60, 1),
    (9, 10, 10, 30, 1),
    (10, 11, 11, 90, 0),
    (11, 12, 14, 45, 1),
    (12, 13, 13, 120, 0),
    (13, 14, 15, 180, 0),
    (14, 15, 12, 60, 1),
    (15, 5, 10, 30, 1);

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
    (17, 8, 4, 3, 15.50, 'maitrise solide'),
    (18, 9, 3, 2, 13.50, 'bonne vigilance'),
    (19, 9, 4, 2, 12.00, 'sql propre'),
    (20, 9, 7, 5, 14.00, 'analyse correcte'),
    (21, 10, 5, 3, 15.50, 'bon niveau'),
    (22, 10, 8, 6, 16.00, 'tres bon projet'),
    (23, 10, 4, 3, 13.50, 'serieuse'),
    (24, 11, 1, 1, 11.50, 'bases acquises'),
    (25, 11, 2, 1, 12.50, 'application correcte'),
    (26, 11, 9, 7, 14.00, 'deploiement propre'),
    (27, 12, 1, 1, 15.00, 'bon rythme'),
    (28, 12, 2, 1, 14.50, 'a l aise'),
    (29, 12, 4, 3, 13.00, 'bon raisonnement'),
    (30, 12, 9, 7, 15.50, 'pipeline propre'),
    (31, 13, 3, 2, 7.50, 'lacunes reseau'),
    (32, 13, 4, 2, 8.50, 'jointures a revoir'),
    (33, 13, 7, 5, 9.00, 'analyse moyenne'),
    (34, 14, 5, 3, 14.00, 'bonne curiosite'),
    (35, 14, 8, 6, 12.50, 'effort regulier'),
    (36, 14, 4, 3, 11.00, 'correct'),
    (37, 15, 5, 6, 17.50, 'excellent rendu'),
    (38, 15, 8, 6, 16.50, 'bonne autonomie'),
    (39, 15, 4, 3, 15.00, 'tres propre');

-- 5. Clubs et alternance

INSERT INTO inscription_club (id, club_id, eleve_id, role_membre, date_inscription) VALUES
    (1, 1, 1, 'presidente', '2026-01-10'),
    (2, 1, 8, 'membre', '2026-01-12'),
    (3, 2, 6, 'capitaine', '2026-01-08'),
    (4, 2, 4, 'membre', '2026-01-09'),
    (5, 3, 3, 'membre', '2026-01-15'),
    (6, 3, 4, 'membre', '2026-01-16'),
    (7, 3, 2, 'membre', '2026-01-20'),
    (8, 4, 10, 'membre', '2026-01-18'),
    (9, 4, 12, 'membre', '2026-01-19'),
    (10, 5, 1, 'membre', '2026-01-22'),
    (11, 5, 11, 'mainteneur', '2026-01-25'),
    (12, 5, 12, 'membre', '2026-01-28'),
    (13, 3, 9, 'membre', '2026-01-27'),
    (14, 1, 10, 'membre', '2026-01-30'),
    (15, 2, 15, 'membre', '2026-01-18'),
    (16, 4, 14, 'vice-presidente', '2026-02-01');

INSERT INTO alternance (
    id,
    eleve_id,
    entreprise_id,
    type_contrat,
    poste,
    rythme,
    date_debut,
    date_fin,
    salaire_mensuel
) VALUES
    (1, 1, 1, 'Apprentissage', 'Developpeuse API junior', '3 semaines entreprise / 1 semaine ecole', '2026-09-01', '2027-08-31', 1280.00),
    (2, 3, 2, 'Professionnalisation', 'Analyste SOC junior', '2 semaines entreprise / 1 semaine ecole', '2026-09-15', '2027-09-14', 1400.00),
    (3, 5, 3, 'Apprentissage', 'Data analyst junior', '4 jours entreprise / 1 jour ecole', '2026-10-01', '2027-09-30', 1350.00),
    (4, 8, 1, 'Apprentissage', 'Developpeur backend junior', '3 semaines entreprise / 1 semaine ecole', '2026-09-01', '2027-08-31', 1450.00),
    (5, 10, 3, 'Apprentissage', 'Data analyst junior', '4 jours entreprise / 1 jour ecole', '2026-09-01', '2027-08-31', 1420.00),
    (6, 12, 5, 'Apprentissage', 'DevOps junior', '3 semaines entreprise / 1 semaine ecole', '2026-09-01', '2027-08-31', 1380.00),
    (7, 13, 4, 'Professionnalisation', 'Technicien cyber junior', '2 semaines entreprise / 1 semaine ecole', '2026-10-01', '2027-09-30', 1330.00),
    (8, 15, 6, 'Apprentissage', 'Analyste data junior', '4 jours entreprise / 1 jour ecole', '2026-09-15', '2027-09-14', 1410.00),
    (9, 9, 7, 'Professionnalisation', 'Analyste cyber junior', '2 semaines entreprise / 1 semaine ecole', '2026-09-10', '2027-09-09', 1360.00),
    (10, 11, 9, 'Apprentissage', 'Integrateur cloud junior', '3 semaines entreprise / 1 semaine ecole', '2026-09-20', '2027-09-19', 1320.00),
    (11, 6, 10, 'Professionnalisation', 'Consultant data junior', '4 jours entreprise / 1 jour ecole', '2026-10-05', '2027-10-04', 1390.00);

-- On remplit la table de classement a la fin

CALL sp_recalculer_classement_eleves();
