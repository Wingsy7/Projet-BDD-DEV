$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "outils.ps1")

Import-ProjectEnv

$projectRoot = Get-ProjectRoot

Write-Host ""
Write-Host "== Recreation de la base =="
Invoke-SqlFile (Join-Path $projectRoot "sql\creation_bdd.sql")
Invoke-SqlFile (Join-Path $projectRoot "sql\procedure_et_triggers.sql")
Invoke-SqlFile (Join-Path $projectRoot "sql\donnees_depart.sql")
Write-Host ""
Write-Host "== Base prete =="
