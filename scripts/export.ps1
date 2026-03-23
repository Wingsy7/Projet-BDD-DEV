. (Join-Path $PSScriptRoot "commun.ps1")

Import-ProjectEnv

$databaseName = Get-EnvValue "SCHOOL_DB_NAME" "cozma_miroslav"
$dumpPath = Join-Path (Get-ProjectRoot) "sql\\export.sql"
$dumpPath = [System.IO.Path]::GetFullPath($dumpPath)
$mysqldump = Get-MySqlDumpPath
$args = Get-DbCliArgs

$args += "--routines"
$args += "--triggers"
$args += "--databases"
$args += $databaseName

& $mysqldump @args > $dumpPath
Write-Host "Export cree : $dumpPath"
