$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "outils.ps1")

Import-ProjectEnv

$projectRoot = Get-ProjectRoot
$python = Get-PythonPath

Push-Location $projectRoot
try {
    & $python .\admin_cli\menu_admin.py
}
finally {
    Pop-Location
}
