# Projet Ecole Avance

Projet realise pour les 2 sujets :

- `BDD & SQL - Projet Ecole (avance)`
- `Dev BDD - API Projet Ecole (avance)`

Le projet contient 3 parties :

- une base MySQL
- une API en Python avec FastAPI
- un menu admin en ligne de commande

## Fichiers utiles

- `sql/base.sql` : creation de la base et des tables
- `sql/donnees.sql` : jeu de donnees de depart
- `sql/requetes.sql` : requetes SQL du sujet
- `sql/automatismes.sql` : procedure et triggers
- `sql/export.sql` : export final de la base
- `api/app/routes.py` : routes de l'API
- `api/app/traitements.py` : traitements Python
- `api/app/requetes.py` : SELECT simples pour l'API
- `api/app/bdd.py` : connexion a MySQL
- `admin_cli/menu.py` : menu admin
- `admin_cli/client.py` : appels HTTP avec `requests`

## Ordre de lecture

Si on veut relire le projet rapidement, le plus simple est :

1. `sql/base.sql`
2. `sql/donnees.sql`
3. `sql/requetes.sql`
4. `sql/automatismes.sql`
5. `api/app/requetes.py`
6. `api/app/bdd.py`
7. `api/app/traitements.py`
8. `api/app/routes.py`
9. `admin_cli/menu.py`

## Ce qu'on a mis en plus

En plus du sujet de base, on a garde 2 parties :

- les clubs de l'ecole
- l'alternance avec les entreprises

### Clubs

Tables ajoutees :

- `club`
- `inscription_club`

Routes principales :

- `GET /clubs`
- `GET /clubs/{club_id}/membres`
- `GET /eleve/{eleve_id}/clubs`
- `POST /clubs`
- `PUT /clubs/{club_id}`
- `DELETE /clubs/{club_id}`

### Alternance

Tables ajoutees :

- `entreprise`
- `alternance`

Routes principales :

- `GET /entreprises`
- `GET /alternances`
- `GET /eleve/{eleve_id}/alternance`
- `POST /entreprises`
- `POST /alternances`

## Base de donnees

Le nom de base actuel est :

```text
equipe_6
```

Si besoin, on peut le changer avec :

- `SCHOOL_DB_NAME`

## Installation

Depuis le dossier `projet-ecole-avance` :

```powershell
.\scripts\installer.ps1
```

Si Python n'est pas detecte automatiquement :

```powershell
$env:SCHOOL_PYTHON = "C:\chemin\vers\python.exe"
.\scripts\installer.ps1
```

## Mise en place

Le plus simple :

```powershell
.\scripts\refaire_bdd.ps1
```

Ordre manuel si on veut lancer les fichiers un par un :

1. `sql/base.sql`
2. `sql/automatismes.sql`
3. `sql/donnees.sql`
4. `sql/requetes.sql`

## Lancer le projet

API :

```powershell
.\scripts\demarrer_api.ps1
```

Menu admin :

```powershell
.\scripts\demarrer_menu.ps1
```

Swagger :

```text
http://127.0.0.1:8000/docs
```

## Verifier rapidement

```powershell
.\scripts\verifier.ps1
```

Ce script refait la base puis teste :

- le SQL
- les triggers
- l'API
- le menu admin

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

Le projet peut lire un fichier `.env`.
On peut partir de `.env.example`.

## Points a montrer

- `GET /eleve` renvoie seulement `nom` et `age`
- `GET /notes/{eleve_id}` renvoie `note`, `matiere`, `nom_eleve`
- les calculs et tris de l'API sont faits en Python
- le menu admin passe par l'API
- la base contient aussi une procedure stockee et des triggers

## Livrables

- schema PNG
- export SQL
- scripts SQL
- API Python
- menu admin
