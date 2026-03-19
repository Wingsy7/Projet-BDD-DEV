$ErrorActionPreference = "Stop"

$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$python = "C:\Users\cozma\AppData\Local\Python\pythoncore-3.14-64\python.exe"
$mysql = "C:\xampp\mysql\bin\mysql.exe"
$dbName = "cozma_miroslav"

function Lance-FichierSql {
    param([string] $Path)

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    & $mysql -u root --execute="source $($fullPath -replace '\\', '/')" | Out-Host
}

function Lance-RequeteSql {
    param([string] $Query)

    & $mysql -u root --table --execute=$Query | Out-Host
}

Write-Host ""
Write-Host "== Reset base =="
Lance-FichierSql (Join-Path $projectRoot "sql\creation_bdd.sql")
Lance-FichierSql (Join-Path $projectRoot "sql\procedure_et_triggers.sql")
Lance-FichierSql (Join-Path $projectRoot "sql\donnees_depart.sql")

Write-Host ""
Write-Host "== SQL smoke =="
$sqlSmoke = @"
USE $dbName;
SELECT COUNT(*) AS nb_eleves FROM eleve;
SELECT COUNT(*) AS nb_notes FROM note;
SELECT COUNT(*) AS nb_clubs FROM club;
SELECT e.nom, c.score, c.moyenne_generale
FROM classement_eleve c
JOIN eleve e ON e.id = c.eleve_id
ORDER BY c.score DESC, c.moyenne_generale DESC, e.nom ASC
LIMIT 3;
"@
Lance-RequeteSql $sqlSmoke

Write-Host ""
Write-Host "== Trigger smoke =="
$triggerSmoke = @"
USE $dbName;
INSERT INTO eleve (nom, email, age, promotion_id)
VALUES ('Test Mineur Script', 'test.mineur.script@ecole.local', 16, 1);
SELECT e.nom, d.infos
FROM eleve e
JOIN dossier d ON d.eleve_id = e.id
WHERE e.email = 'test.mineur.script@ecole.local';
DELETE FROM eleve WHERE email = 'test.mineur.script@ecole.local';

INSERT INTO note (eleve_id, cours_id, prof_id, valeur, commentaire)
VALUES (1, 1, 1, 14.00, 'test_all_keep_best');
SET @keep_best_id = LAST_INSERT_ID();
UPDATE note SET valeur = 8.00 WHERE id = @keep_best_id;
SELECT id, valeur FROM note WHERE id = @keep_best_id;
DELETE FROM note WHERE id = @keep_best_id;

INSERT INTO prof (nom, email, age)
VALUES ('Prof Temp Script', 'prof.temp.script@ecole.local', 40);
SET @temp_prof_id = LAST_INSERT_ID();
INSERT INTO note (eleve_id, cours_id, prof_id, valeur, commentaire)
VALUES (1, 1, @temp_prof_id, 18.00, 'test_all_delete_prof');
SET @temp_note_id = LAST_INSERT_ID();
DELETE FROM prof WHERE id = @temp_prof_id;
SELECT id, valeur, prof_id FROM note WHERE id = @temp_note_id;
DELETE FROM note WHERE id = @temp_note_id;
"@
Lance-RequeteSql $triggerSmoke

Write-Host ""
Write-Host "== API smoke =="
$stdoutLog = Join-Path $projectRoot "uvicorn-test.out.log"
$stderrLog = Join-Path $projectRoot "uvicorn-test.err.log"
if (Test-Path $stdoutLog) { Remove-Item $stdoutLog -Force }
if (Test-Path $stderrLog) { Remove-Item $stderrLog -Force }

$proc = Start-Process `
    -FilePath $python `
    -ArgumentList "-m", "uvicorn", "app.api:app", "--host", "127.0.0.1", "--port", "8000", "--app-dir", "api" `
    -WorkingDirectory $projectRoot `
    -RedirectStandardOutput $stdoutLog `
    -RedirectStandardError $stderrLog `
    -PassThru

try {
    Start-Sleep -Seconds 4
    if ($proc.HasExited) {
        Write-Host "Echec du lancement uvicorn"
        if (Test-Path $stdoutLog) { Get-Content $stdoutLog | Out-Host }
        if (Test-Path $stderrLog) { Get-Content $stderrLog | Out-Host }
        throw "Uvicorn a quitte trop tot."
    }

    $apiSmoke = @'
import json
import requests

base = "http://127.0.0.1:8000"

def req(path):
    response = requests.get(base + path, timeout=30)
    response.raise_for_status()
    return response.json()

summary = {
    "health": req("/health"),
    "eleves_count": len(req("/eleve")),
    "notes_eleve_1": len(req("/notes/1")),
    "bonne_notes_top3": [item["nom"] for item in req("/eleve/bonne_notes")[:3]],
    "absence_eleve_2": req("/eleve/2/absence"),
}
print(json.dumps(summary, indent=2, ensure_ascii=True))
'@
    $apiSmoke | & $python - | Out-Host

    Write-Host ""
    Write-Host "== CLI smoke =="
    @("1", "25", "1", "0") | & $python ".\admin_cli\menu_admin.py" | Select-Object -First 35 | Out-Host
}
finally {
    if (-not $proc.HasExited) {
        Stop-Process -Id $proc.Id -Force
    }
}

Write-Host ""
Write-Host "== Reset final =="
Lance-FichierSql (Join-Path $projectRoot "sql\creation_bdd.sql")
Lance-FichierSql (Join-Path $projectRoot "sql\procedure_et_triggers.sql")
Lance-FichierSql (Join-Path $projectRoot "sql\donnees_depart.sql")

Write-Host ""
Write-Host "== OK =="
