$databaseName = "cozma_miroslav"
$dumpPath = Join-Path $PSScriptRoot "..\\sql\\export_final.sql"
$dumpPath = [System.IO.Path]::GetFullPath($dumpPath)

& "C:\\xampp\\mysql\\bin\\mysqldump.exe" `
    -u root `
    --routines `
    --triggers `
    --databases $databaseName `
    > $dumpPath
