$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "outils.ps1")

Import-ProjectEnv

$projectRoot = Get-ProjectRoot
$python = Get-PythonPath
$apiUrl = Get-EnvValue "SCHOOL_API_URL" "http://127.0.0.1:8000"
$uri = [System.Uri] $apiUrl
$hostName = $uri.Host
$port = $uri.Port

Push-Location $projectRoot
try {
    & $python -m uvicorn app.api:app --host $hostName --port $port --app-dir api --reload
}
finally {
    Pop-Location
}
