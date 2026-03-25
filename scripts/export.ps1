. (Join-Path $PSScriptRoot "commun.ps1")

Import-ProjectEnv

$databaseName = Get-EnvValue "SCHOOL_DB_NAME" "equipe_6"
$dumpPath = Join-Path (Get-ProjectRoot) "sql\\export.sql"
$dumpPath = [System.IO.Path]::GetFullPath($dumpPath)
$mysqldump = Get-MySqlDumpPath
$args = Get-DbCliArgs

$args += "--routines"
$args += "--triggers"
$args += "--databases"
$args += $databaseName

& $mysqldump @args > $dumpPath
Assert-LastExitCode "Erreur pendant la creation de l'export SQL"
Write-Host "Export cree : $dumpPath"
