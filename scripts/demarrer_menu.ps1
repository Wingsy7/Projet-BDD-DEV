$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "commun.ps1")

Import-ProjectEnv

$projectRoot = Get-ProjectRoot
$python = Get-PythonPath

Push-Location $projectRoot
try {
    & $python .\admin_cli\menu.py
}
finally {
    Pop-Location
}
