# Projet-BDD-DEV

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)

School management project combining a MySQL database, a FastAPI backend and a command-line admin interface.
The goal is to model a realistic school system, expose structured API endpoints and handle business logic in Python.

## Main Components

- MySQL database with schema, seed data, queries, stored procedure and triggers
- FastAPI application exposing read and CRUD endpoints
- Python service layer for filtering, grouping and business calculations
- Command-line admin menu using HTTP calls to the API
- Extra modules for clubs and work-study management

## Tech Stack

| Technology | Usage |
|---|---|
| MySQL | Relational database |
| SQL | Schema, seed data, stored logic and queries |
| Python | Backend logic |
| FastAPI | HTTP API |
| Requests | Admin CLI HTTP client |
| PowerShell | Setup, verification and export scripts |

## Architecture

```text
admin_cli/menu.py
  -> admin_cli/client.py
  -> api/app/routes.py
  -> api/app/traitements.py
  -> api/app/bdd.py
  -> api/app/requetes.py
  -> MySQL
```

## Key Features

- Student, teacher, grade and attendance management
- Grouped note analysis and filtered endpoints
- Stored procedure for student ranking
- Triggers for automatic school rules
- Club and work-study extensions
- End-to-end verification script

## Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Rebuild the database
powershell -ExecutionPolicy Bypass -File .\scripts\refaire_bdd.ps1

# Start the API
powershell -ExecutionPolicy Bypass -File .\scripts\demarrer_api.ps1

# Start the admin menu
powershell -ExecutionPolicy Bypass -File .\scripts\demarrer_menu.ps1
```

Swagger is available at:

```text
http://127.0.0.1:8000/docs
```

## Project Structure

```text
Projet-BDD-DEV/
├── sql/
├── api/app/
├── admin_cli/
├── scripts/
├── livrables/
├── README.md
└── requirements.txt
```

## What This Project Demonstrates

- Database design and business rules in SQL
- Clean API layering with validation and service logic
- Practical Python backend development
- A reproducible workflow with verification and export scripts

## Author

**Miroslav**  
GitHub: [Wingsy7](https://github.com/Wingsy7)
