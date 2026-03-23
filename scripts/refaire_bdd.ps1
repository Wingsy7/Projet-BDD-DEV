$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "commun.ps1")

Import-ProjectEnv

$projectRoot = Get-ProjectRoot

Write-Host ""
Write-Host "== Recreation de la base =="
Invoke-SqlFile (Join-Path $projectRoot "sql\base.sql")
Invoke-SqlFile (Join-Path $projectRoot "sql\automatismes.sql")
Invoke-SqlFile (Join-Path $projectRoot "sql\donnees.sql")
Write-Host ""
Write-Host "== Base prete =="
