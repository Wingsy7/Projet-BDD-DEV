# Projet Ecole Avance

Ce dossier correspond aux 2 sujets du TP :

- `BDD & SQL - Projet Ecole (avance)`
- `Dev BDD - API Projet Ecole (avance)`

J'ai garde une organisation simple pour m'y retrouver :

- `sql/creation_bdd.sql` : creation de la base et des tables
- `sql/donnees_depart.sql` : jeu de donnees de depart
- `sql/requetes_du_tp.sql` : requetes a montrer pour la partie BDD
- `sql/procedure_et_triggers.sql` : procedure stockee + triggers
- `sql/export_final.sql` : export final de la base
- `api/app/api.py` : routes FastAPI
- `api/app/gestion_ecole.py` : traitements Python
- `api/app/requetes_sql.py` : `SELECT` simples
- `admin_cli/menu_admin.py` : menu admin en ligne de commande
- `admin_cli/client_api.py` : appels HTTP avec `requests`
- `livrables/schema_bdd_ecole.png` : schema PNG
- `scripts/verifier_projet.ps1` : script de verification

## Fonctionnalite supplementaire

J'ai choisi la gestion des clubs :

- table `club`
- table `inscription_club`
- lecture + CRUD dans l'API
- lecture + CRUD dans le menu admin

## Installation

Depuis `projet-ecole-avance` :

```powershell
& 'C:\Users\cozma\AppData\Local\Python\pythoncore-3.14-64\python.exe' -m pip install -r requirements.txt
```

## Ordre pour la base

1. lancer `sql/creation_bdd.sql`
2. lancer `sql/procedure_et_triggers.sql`
3. lancer `sql/donnees_depart.sql`
4. lancer `sql/requetes_du_tp.sql` si on veut montrer les requetes

Le nom de base actuel est `cozma_miroslav`.
Si le prof veut absolument le nom exact du groupe, il faudra juste l'adapter avant le rendu.

## Variables utiles

- `SCHOOL_DB_HOST`
- `SCHOOL_DB_PORT`
- `SCHOOL_DB_USER`
- `SCHOOL_DB_PASSWORD`
- `SCHOOL_DB_NAME`
- `SCHOOL_API_URL`

Valeur actuelle :

```text
SCHOOL_DB_NAME=cozma_miroslav
```

## Lancer l'API

```powershell
& 'C:\Users\cozma\AppData\Local\Python\pythoncore-3.14-64\python.exe' -m uvicorn app.api:app --reload --app-dir api
```

Swagger :

```text
http://127.0.0.1:8000/docs
```

## Lancer le menu admin

```powershell
& 'C:\Users\cozma\AppData\Local\Python\pythoncore-3.14-64\python.exe' admin_cli/menu_admin.py
```

## Verifier rapidement le projet

```powershell
& ".\scripts\verifier_projet.ps1"
```

## Quelques points importants

- `GET /eleve` renvoie seulement `nom` et `age`
- `GET /notes/{eleve_id}` renvoie `note`, `matiere`, `nom_eleve`
- les tris, filtres et calculs demandes par le sujet API sont faits en Python
- le menu admin passe par l'API, pas par une connexion directe a MySQL

## Livrables

- schema PNG
- export SQL final
- scripts SQL
- API Python
- menu admin Python
