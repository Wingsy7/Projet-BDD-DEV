$script:ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))

function Get-ProjectRoot {
    return $script:ProjectRoot
}

function Get-EnvValue {
    param(
        [string] $Name,
        [string] $Default = ""
    )

    $value = [Environment]::GetEnvironmentVariable($Name, "Process")
    if ([string]::IsNullOrWhiteSpace($value)) {
        return $Default
    }
    return $value
}

function Set-ProcessEnvIfMissing {
    param(
        [string] $Name,
        [string] $Value
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return
    }

    $current = [Environment]::GetEnvironmentVariable($Name, "Process")
    if ([string]::IsNullOrWhiteSpace($current)) {
        [Environment]::SetEnvironmentVariable($Name, $Value, "Process")
    }
}

function Import-ProjectEnv {
    $envPath = Join-Path $script:ProjectRoot ".env"
    if (Test-Path $envPath) {
        foreach ($rawLine in Get-Content $envPath) {
            $line = $rawLine.Trim()
            if ($line -eq "" -or $line.StartsWith("#") -or -not $line.Contains("=")) {
                continue
            }

            $parts = $line.Split("=", 2)
            $name = $parts[0].Trim()
            $value = $parts[1].Trim().Trim('"').Trim("'")
            Set-ProcessEnvIfMissing -Name $name -Value $value
        }
    }

    $defaults = @{
        "SCHOOL_DB_HOST" = "localhost"
        "SCHOOL_DB_PORT" = "3306"
        "SCHOOL_DB_USER" = "root"
        "SCHOOL_DB_NAME" = "cozma_miroslav"
        "SCHOOL_API_URL" = "http://127.0.0.1:8000"
    }

    foreach ($name in $defaults.Keys) {
        Set-ProcessEnvIfMissing -Name $name -Value $defaults[$name]
    }
}

function Find-ExistingPath {
    param([string[]] $Candidates)

    foreach ($candidate in $Candidates) {
        if (-not [string]::IsNullOrWhiteSpace($candidate) -and (Test-Path $candidate)) {
            return $candidate
        }
    }

    return $null
}

function Test-ExecutableWorks {
    param(
        [string] $Path,
        [string[]] $Arguments
    )

    if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path $Path)) {
        return $false
    }

    try {
        & $Path @Arguments > $null 2> $null
        return ($LASTEXITCODE -eq 0)
    }
    catch {
        return $false
    }
}

function Assert-LastExitCode {
    param(
        [string] $Message
    )

    if ($LASTEXITCODE -ne 0) {
        throw "$Message (code $LASTEXITCODE)."
    }
}

function Get-PythonPath {
    Import-ProjectEnv

    $envPython = Get-EnvValue "SCHOOL_PYTHON"
    if (Test-ExecutableWorks -Path $envPython -Arguments @("-V")) {
        return $envPython
    }

    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand -and (Test-ExecutableWorks -Path $pythonCommand.Source -Arguments @("-V"))) {
        return $pythonCommand.Source
    }

    $candidate = Find-ExistingPath @(
        "C:\Users\$env:USERNAME\AppData\Local\Python\pythoncore-3.14-64\python.exe",
        "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python314\python.exe",
        "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python313\python.exe",
        "C:\Python314\python.exe",
        "C:\Python313\python.exe"
    )

    if ($candidate -and (Test-ExecutableWorks -Path $candidate -Arguments @("-V"))) {
        return $candidate
    }

    throw "Python introuvable. Ajoute-le au PATH ou renseigne SCHOOL_PYTHON."
}

function Get-MySqlCliPath {
    Import-ProjectEnv

    $envMysql = Get-EnvValue "SCHOOL_MYSQL_EXE"
    if (Test-ExecutableWorks -Path $envMysql -Arguments @("--version")) {
        return $envMysql
    }

    $mysqlCommand = Get-Command mysql -ErrorAction SilentlyContinue
    if ($mysqlCommand -and (Test-ExecutableWorks -Path $mysqlCommand.Source -Arguments @("--version"))) {
        return $mysqlCommand.Source
    }

    $candidate = Find-ExistingPath @(
        "C:\xampp\mysql\bin\mysql.exe",
        "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
        "C:\Program Files\MariaDB 11.0\bin\mysql.exe",
        "C:\Program Files\MariaDB 10.11\bin\mysql.exe"
    )

    if ($candidate -and (Test-ExecutableWorks -Path $candidate -Arguments @("--version"))) {
        return $candidate
    }

    throw "Client MySQL introuvable. Ajoute-le au PATH ou renseigne SCHOOL_MYSQL_EXE."
}

function Get-MySqlDumpPath {
    Import-ProjectEnv

    $envDump = Get-EnvValue "SCHOOL_MYSQLDUMP_EXE"
    if (Test-ExecutableWorks -Path $envDump -Arguments @("--version")) {
        return $envDump
    }

    $mysqldumpCommand = Get-Command mysqldump -ErrorAction SilentlyContinue
    if ($mysqldumpCommand -and (Test-ExecutableWorks -Path $mysqldumpCommand.Source -Arguments @("--version"))) {
        return $mysqldumpCommand.Source
    }

    $candidate = Find-ExistingPath @(
        "C:\xampp\mysql\bin\mysqldump.exe",
        "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
        "C:\Program Files\MariaDB 11.0\bin\mysqldump.exe",
        "C:\Program Files\MariaDB 10.11\bin\mysqldump.exe"
    )

    if ($candidate -and (Test-ExecutableWorks -Path $candidate -Arguments @("--version"))) {
        return $candidate
    }

    throw "mysqldump introuvable. Ajoute-le au PATH ou renseigne SCHOOL_MYSQLDUMP_EXE."
}

function Get-DbCliArgs {
    Import-ProjectEnv

    $args = @(
        "-h", (Get-EnvValue "SCHOOL_DB_HOST" "localhost"),
        "-P", (Get-EnvValue "SCHOOL_DB_PORT" "3306"),
        "-u", (Get-EnvValue "SCHOOL_DB_USER" "root")
    )

    $password = Get-EnvValue "SCHOOL_DB_PASSWORD"
    if (-not [string]::IsNullOrEmpty($password)) {
        $args += "-p$password"
    }

    return $args
}

function Invoke-SqlFile {
    param([string] $Path)

    $mysql = Get-MySqlCliPath
    $fullPath = [System.IO.Path]::GetFullPath($Path)
    $args = Get-DbCliArgs
    $args += "--execute=source $($fullPath -replace '\\', '/')"
    & $mysql @args | Out-Host
    Assert-LastExitCode "Erreur pendant l'execution du fichier SQL $fullPath"
}

function Invoke-SqlQuery {
    param([string] $Query)

    $mysql = Get-MySqlCliPath
    $args = Get-DbCliArgs
    $args += "--table"
    $args += "--execute=$Query"
    & $mysql @args | Out-Host
    Assert-LastExitCode "Erreur pendant l'execution d'une requete SQL"
}

function Get-FreeTcpPort {
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
    $listener.Start()
    $port = $listener.LocalEndpoint.Port
    $listener.Stop()
    return $port
}
