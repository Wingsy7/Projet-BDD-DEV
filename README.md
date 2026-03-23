# Projet Ecole Avance

Ce dossier contient mon rendu pour les 2 sujets :

- `BDD & SQL - Projet Ecole (avance)`
- `Dev BDD - API Projet Ecole (avance)`

Le projet est separe en 2 parties :

- la base de donnees MySQL
- l'API + le menu admin en Python


## Contenu du dossier

- `sql/creation_bdd.sql` : script de creation de la base
- `sql/donnees_depart.sql` : les donnees que j'ai mises pour tester
- `sql/requetes_du_tp.sql` : les requetes demandees dans le sujet SQL
- `sql/procedure_et_triggers.sql` : la procedure stockee et les triggers
- `sql/export_final.sql` : l'export final de la base
- `api/app/api.py` : les routes de l'API
- `api/app/gestion_ecole.py` : la partie ou je fais les traitements en Python
- `api/app/requetes_sql.py` : les requetes SQL simples utilisees par l'API
- `admin_cli/menu_admin.py` : le menu en ligne de commande
- `admin_cli/client_api.py` : les requetes HTTP avec `requests`
- `livrables/schema_bdd_ecole.png` : le schema de la base
- `scripts/installer_dependances.ps1` : script d'installation Python
- `scripts/recreer_bdd.ps1` : script pour recreer la base
- `scripts/lancer_api.ps1` : script pour lancer l'API
- `scripts/lancer_menu.ps1` : script pour lancer le menu admin
- `scripts/verifier_projet.ps1` : un script pour verifier vite le projet

## Fonctionnalite supplementaire : Clubs de l'ecole

On a choisi d'ajouter la gestion des clubs de l'ecole.

### Tables ajoutees

- `club` : stocke les clubs de l'ecole
  - `nom` : nom du club
  - `categorie` : type de club (sport, culture, informatique...)
  - `budget_annuel` : budget du club en euros
  - `responsable_prof_id` : prof responsable du club (optionnel)

- `inscription_club` : table de liaison entre les eleves et les clubs
  - `club_id` : club concerne
  - `eleve_id` : eleve inscrit
  - `role_membre` : role de l'eleve dans le club (membre, president, tresorier...)
  - `date_inscription` : date d'entree dans le club
  - Contrainte UNIQUE sur (club_id, eleve_id) : un eleve ne peut pas etre inscrit deux fois au meme club

### Relations

- Un club peut avoir plusieurs eleves, un eleve peut rejoindre plusieurs clubs
- Un prof peut etre responsable de plusieurs clubs
- Si un prof est supprime, le champ responsable_prof_id passe a NULL (ON DELETE SET NULL)
- Si un eleve est supprime, ses inscriptions aux clubs sont supprimees (ON DELETE CASCADE)

### Routes API ajoutees

- `GET /clubs` : liste tous les clubs avec le nombre de membres
- `GET /clubs/{club_id}/membres` : liste les membres d'un club
- `GET /eleve/{eleve_id}/clubs` : liste les clubs d'un eleve
- `POST /clubs` : creer un club
- `PUT /clubs/{club_id}` : modifier un club
- `DELETE /clubs/{club_id}` : supprimer un club
- `GET /club-inscriptions` : liste toutes les inscriptions
- `POST /club-inscriptions` : inscrire un eleve a un club
- `PUT /club-inscriptions/{id}` : modifier une inscription
- `DELETE /club-inscriptions/{id}` : supprimer une inscription

### Menu admin

Le menu admin permet de gerer les clubs et les inscriptions via l'API :
- Lister les clubs et leurs membres
- Creer, modifier, supprimer un club
- Inscrire un eleve a un club, modifier ou supprimer une inscription

## Installation

Depuis le dossier `projet-ecole-avance` :
```powershell
.\scripts\installer_dependances.ps1
```

Si besoin, on peut forcer un interpreteur Python avec une variable d'environnement :
```powershell
$env:SCHOOL_PYTHON = "C:\chemin\vers\python.exe"
.\scripts\installer_dependances.ps1
```

## Mise en place de la base

Le plus simple :
```powershell
.\scripts\recreer_bdd.ps1
```

On peut aussi lancer les fichiers SQL a la main dans cet ordre :

1. `sql/creation_bdd.sql`
2. `sql/procedure_et_triggers.sql`
3. `sql/donnees_depart.sql`
4. `sql/requetes_du_tp.sql` si on veut montrer les requetes

La base s'appelle actuellement `cozma_miroslav`.
Si besoin, il faut juste changer ce nom pour mettre exactement le nom du groupe demande.

## Variables utiles

- `SCHOOL_DB_HOST`
- `SCHOOL_DB_PORT`
- `SCHOOL_DB_USER`
- `SCHOOL_DB_PASSWORD`
- `SCHOOL_DB_NAME`
- `SCHOOL_API_URL`
- `SCHOOL_PYTHON`
- `SCHOOL_MYSQL_EXE`
- `SCHOOL_MYSQLDUMP_EXE`

Valeur actuelle :
```text
SCHOOL_DB_NAME=cozma_miroslav
```

Le projet peut aussi lire un fichier `.env` a la racine.
Le plus simple est de partir de `.env.example`.

## Lancer l'API
```powershell
.\scripts\lancer_api.ps1
```

Ensuite on peut ouvrir Swagger ici :
```text
http://127.0.0.1:8000/docs
```

## Lancer le menu admin
```powershell
.\scripts\lancer_menu.ps1
```

## Verifier vite fait
```powershell
& ".\scripts\verifier_projet.ps1"
```

Je l'ai surtout garde pour verifier rapidement que la base, l'API et le menu tournent encore ensemble.

## Portabilite

J'ai essaye de faire en sorte que le projet demande le moins d'adaptation possible :

- les scripts PowerShell detectent Python et MySQL automatiquement si c'est dans le PATH
- sinon on peut donner les chemins avec `SCHOOL_PYTHON`, `SCHOOL_MYSQL_EXE` et `SCHOOL_MYSQLDUMP_EXE`
- les variables de base de donnees peuvent etre lues depuis l'environnement ou depuis un fichier `.env`
- le script de verification choisit maintenant un port API libre automatiquement

## Points importants

- `GET /eleve` renvoie seulement `nom` et `age`
- `GET /notes/{eleve_id}` renvoie `note`, `matiere`, `nom_eleve`
- les tris, filtres et calculs de l'API sont faits en Python
- le menu admin passe par l'API, il ne se connecte pas directement a MySQL

## Livrables presents

- le schema PNG
- l'export SQL final
- les scripts SQL
- l'API Python
- le menu admin Python

Normalement tout ce qu'il faut pour le rendu est dans ce dossier.
