DROP DATABASE IF EXISTS equipe_5;
CREATE DATABASE equipe_5
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE equipe_5;

-- Partie 1 : ce qui sert a organiser l'ecole

CREATE TABLE specialite (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE promotion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(120) NOT NULL UNIQUE,
    annee INT NOT NULL,
    specialite_id INT NOT NULL,
    CONSTRAINT fk_promotion_specialite
        FOREIGN KEY (specialite_id) REFERENCES specialite(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE cours (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL UNIQUE,
    niveau INT NOT NULL DEFAULT 1,
    specialite_id INT NULL,
    CONSTRAINT fk_cours_specialite
        FOREIGN KEY (specialite_id) REFERENCES specialite(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE prof (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    email VARCHAR(190) NOT NULL UNIQUE,
    age INT NOT NULL
);

CREATE TABLE prof_cours (
    prof_id INT NOT NULL,
    cours_id INT NOT NULL,
    PRIMARY KEY (prof_id, cours_id),
    CONSTRAINT fk_prof_cours_prof
        FOREIGN KEY (prof_id) REFERENCES prof(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_prof_cours_cours
        FOREIGN KEY (cours_id) REFERENCES cours(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Partie 2 : les eleves et leur suivi

CREATE TABLE eleve (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    email VARCHAR(190) NOT NULL UNIQUE,
    age INT NOT NULL,
    promotion_id INT NOT NULL,
    CONSTRAINT fk_eleve_promotion
        FOREIGN KEY (promotion_id) REFERENCES promotion(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE dossier (
    id INT AUTO_INCREMENT PRIMARY KEY,
    eleve_id INT NOT NULL UNIQUE,
    infos VARCHAR(2550) NOT NULL DEFAULT '',
    avertissement_travail TINYINT(1) NOT NULL DEFAULT 0,
    avertissement_comportement TINYINT(1) NOT NULL DEFAULT 0,
    CONSTRAINT fk_dossier_eleve
        FOREIGN KEY (eleve_id) REFERENCES eleve(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE eleve_cours (
    eleve_id INT NOT NULL,
    cours_id INT NOT NULL,
    PRIMARY KEY (eleve_id, cours_id),
    CONSTRAINT fk_eleve_cours_eleve
        FOREIGN KEY (eleve_id) REFERENCES eleve(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_eleve_cours_cours
        FOREIGN KEY (cours_id) REFERENCES cours(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Partie 3 : les seances, les absences et les notes

CREATE TABLE instance_cours (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cours_id INT NOT NULL,
    prof_id INT NOT NULL,
    date_cours DATETIME NOT NULL,
    CONSTRAINT fk_instance_cours_cours
        FOREIGN KEY (cours_id) REFERENCES cours(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_instance_cours_prof
        FOREIGN KEY (prof_id) REFERENCES prof(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE absence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    eleve_id INT NOT NULL,
    instance_cours_id INT NOT NULL,
    duree_minutes INT NOT NULL,
    justificatif TINYINT(1) NOT NULL DEFAULT 0,
    CONSTRAINT fk_absence_eleve
        FOREIGN KEY (eleve_id) REFERENCES eleve(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_absence_instance
        FOREIGN KEY (instance_cours_id) REFERENCES instance_cours(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE note (
    id INT AUTO_INCREMENT PRIMARY KEY,
    eleve_id INT NOT NULL,
    cours_id INT NOT NULL,
    prof_id INT NULL,
    valeur DECIMAL(5, 2) NOT NULL,
    commentaire VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_note_eleve
        FOREIGN KEY (eleve_id) REFERENCES eleve(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_note_cours
        FOREIGN KEY (cours_id) REFERENCES cours(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_note_prof
        FOREIGN KEY (prof_id) REFERENCES prof(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Partie 4 : fonctionnalites en plus

CREATE TABLE club (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL UNIQUE,
    categorie VARCHAR(120) NOT NULL,
    budget_annuel DECIMAL(10, 2) NOT NULL DEFAULT 0,
    responsable_prof_id INT NULL,
    CONSTRAINT fk_club_prof
        FOREIGN KEY (responsable_prof_id) REFERENCES prof(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE inscription_club (
    id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT NOT NULL,
    eleve_id INT NOT NULL,
    role_membre VARCHAR(120) NOT NULL DEFAULT 'membre',
    date_inscription DATE NOT NULL,
    UNIQUE KEY uq_club_eleve (club_id, eleve_id),
    CONSTRAINT fk_inscription_club_club
        FOREIGN KEY (club_id) REFERENCES club(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_inscription_club_eleve
        FOREIGN KEY (eleve_id) REFERENCES eleve(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE entreprise (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL UNIQUE,
    secteur VARCHAR(120) NOT NULL,
    ville VARCHAR(120) NOT NULL,
    email_contact VARCHAR(190) NULL,
    telephone VARCHAR(40) NULL
);

CREATE TABLE alternance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    eleve_id INT NOT NULL,
    entreprise_id INT NOT NULL,
    type_contrat VARCHAR(80) NOT NULL,
    poste VARCHAR(150) NOT NULL,
    rythme VARCHAR(120) NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE NULL,
    salaire_mensuel DECIMAL(10, 2) NOT NULL DEFAULT 0,
    UNIQUE KEY uq_alternance_contrat (eleve_id, entreprise_id, date_debut),
    CONSTRAINT fk_alternance_eleve
        FOREIGN KEY (eleve_id) REFERENCES eleve(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_alternance_entreprise
        FOREIGN KEY (entreprise_id) REFERENCES entreprise(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Partie 5 : table remplie par la procedure de classement

CREATE TABLE classement_eleve (
    eleve_id INT PRIMARY KEY,
    score INT NOT NULL,
    moyenne_generale DECIMAL(5, 2) NOT NULL,
    total_absence_minutes INT NOT NULL,
    a_un_avertissement TINYINT(1) NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_classement_eleve
        FOREIGN KEY (eleve_id) REFERENCES eleve(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
