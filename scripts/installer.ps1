$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "commun.ps1")

Import-ProjectEnv

$projectRoot = Get-ProjectRoot
$python = Get-PythonPath

Push-Location $projectRoot
try {
    & $python -m pip install -r requirements.txt
}
finally {
    Pop-Location
}
