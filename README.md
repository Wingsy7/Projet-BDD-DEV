# Projet Ecole Avance

Ce dossier contient mon rendu pour les 2 sujets :

- `BDD & SQL - Projet Ecole (avance)`
- `Dev BDD - API Projet Ecole (avance)`

Le projet est separe en 2 parties :

- la base de donnees MySQL
- l'API + le menu admin en Python

J'ai essaye de garder une structure assez simple pour pouvoir la relire facilement.
Si on veut comprendre le projet dans l'ordre, le plus simple est de lire :

1. `sql/base.sql`
2. `sql/donnees.sql`
3. `sql/requetes.sql`
4. `api/app/requetes.py`
5. `api/app/bdd.py`
6. `api/app/traitements.py`
7. `api/app/routes.py`
8. `admin_cli/menu.py`


## Contenu du dossier

- `sql/base.sql` : script de creation de la base
- `sql/donnees.sql` : les donnees que j'ai mises pour tester
- `sql/requetes.sql` : les requetes demandees dans le sujet SQL
- `sql/automatismes.sql` : la procedure stockee et les triggers
- `sql/export.sql` : l'export final de la base
- `api/app/routes.py` : les routes de l'API
- `api/app/traitements.py` : la partie ou je fais les traitements en Python
- `api/app/requetes.py` : les requetes SQL simples utilisees par l'API
- `admin_cli/menu.py` : le menu en ligne de commande
- `admin_cli/client.py` : les requetes HTTP avec `requests`
- `livrables/schema_ecole.png` : le schema de la base
- `scripts/installer.ps1` : script d'installation Python
- `scripts/refaire_bdd.ps1` : script pour recreer la base
- `scripts/demarrer_api.ps1` : script pour lancer l'API
- `scripts/demarrer_menu.ps1` : script pour lancer le menu admin
- `scripts/verifier.ps1` : un script pour verifier vite le projet

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

## Ajout en plus : Alternance

J'ai aussi ajoute un petit suivi d'alternance avec les entreprises.

### Tables ajoutees

- `entreprise` : stocke les entreprises partenaires
  - `nom`
  - `secteur`
  - `ville`
  - `email_contact`
  - `telephone`

- `alternance` : lie un eleve a une entreprise avec les infos du contrat
  - `eleve_id`
  - `entreprise_id`
  - `type_contrat`
  - `poste`
  - `rythme`
  - `date_debut`
  - `date_fin`
  - `salaire_mensuel`

### Routes API ajoutees

- `GET /entreprises`
- `POST /entreprises`
- `PUT /entreprises/{entreprise_id}`
- `DELETE /entreprises/{entreprise_id}`
- `GET /alternances`
- `GET /eleve/{eleve_id}/alternance`
- `POST /alternances`
- `PUT /alternances/{alternance_id}`
- `DELETE /alternances/{alternance_id}`

### Menu admin

Le menu permet maintenant aussi de :
- lister les entreprises
- creer, modifier, supprimer une entreprise
- lister les contrats d'alternance
- creer, modifier, supprimer une alternance

## Installation

Depuis le dossier `projet-ecole-avance` :
```powershell
.\scripts\installer.ps1
```

Si besoin, on peut forcer un interpreteur Python avec une variable d'environnement :
```powershell
$env:SCHOOL_PYTHON = "C:\chemin\vers\python.exe"
.\scripts\installer.ps1
```

## Mise en place de la base

Le plus simple :
```powershell
.\scripts\refaire_bdd.ps1
```

On peut aussi lancer les fichiers SQL a la main dans cet ordre :

1. `sql/base.sql`
2. `sql/automatismes.sql`
3. `sql/donnees.sql`
4. `sql/requetes.sql` si on veut montrer les requetes

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
.\scripts\demarrer_api.ps1
```

Ensuite on peut ouvrir Swagger ici :
```text
http://127.0.0.1:8000/docs
```

## Lancer le menu admin
```powershell
.\scripts\demarrer_menu.ps1
```

## Verifier vite fait
```powershell
& ".\scripts\verifier.ps1"
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
