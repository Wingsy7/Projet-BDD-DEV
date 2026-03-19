Add-Type -AssemblyName System.Drawing

$outputPath = Join-Path $PSScriptRoot "..\\livrables\\schema_bdd_ecole.png"
$outputPath = [System.IO.Path]::GetFullPath($outputPath)

$bitmap = New-Object System.Drawing.Bitmap 2400, 1700
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.Clear([System.Drawing.Color]::FromArgb(248, 248, 244))

$titleFont = New-Object System.Drawing.Font("Segoe UI", 24, [System.Drawing.FontStyle]::Bold)
$headerFont = New-Object System.Drawing.Font("Segoe UI", 14, [System.Drawing.FontStyle]::Bold)
$textFont = New-Object System.Drawing.Font("Consolas", 11)
$linePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(68, 68, 68), 2)
$relationPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(26, 115, 232), 2)
$relationPen.EndCap = [System.Drawing.Drawing2D.LineCap]::ArrowAnchor
$headerBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(39, 76, 119))
$fillBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(33, 33, 33))
$headerTextBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)

$graphics.DrawString("Schema BDD Ecole - Projet avance", $titleFont, $textBrush, 40, 20)

$tables = @(
    @{ Name = "specialite"; X = 40; Y = 90; Fields = @("id PK", "nom") },
    @{ Name = "promotion"; X = 40; Y = 300; Fields = @("id PK", "nom", "annee", "specialite_id FK") },
    @{ Name = "cours"; X = 40; Y = 570; Fields = @("id PK", "nom", "niveau", "specialite_id FK?") },
    @{ Name = "prof"; X = 640; Y = 90; Fields = @("id PK", "nom", "email", "age") },
    @{ Name = "prof_cours"; X = 640; Y = 340; Fields = @("prof_id PK/FK", "cours_id PK/FK") },
    @{ Name = "instance_cours"; X = 640; Y = 520; Fields = @("id PK", "cours_id FK", "prof_id FK", "date_cours") },
    @{ Name = "eleve"; X = 1260; Y = 90; Fields = @("id PK", "nom", "email", "age", "promotion_id FK") },
    @{ Name = "dossier"; X = 1260; Y = 380; Fields = @("id PK", "eleve_id FK unique", "infos", "avertissement_travail", "avertissement_comportement") },
    @{ Name = "eleve_cours"; X = 1260; Y = 690; Fields = @("eleve_id PK/FK", "cours_id PK/FK") },
    @{ Name = "note"; X = 1870; Y = 90; Fields = @("id PK", "eleve_id FK", "cours_id FK", "prof_id FK?", "valeur", "commentaire", "created_at") },
    @{ Name = "absence"; X = 1870; Y = 430; Fields = @("id PK", "eleve_id FK", "instance_cours_id FK", "duree_minutes", "justificatif") },
    @{ Name = "club"; X = 640; Y = 920; Fields = @("id PK", "nom", "categorie", "budget_annuel", "responsable_prof_id FK?") },
    @{ Name = "inscription_club"; X = 1260; Y = 980; Fields = @("id PK", "club_id FK", "eleve_id FK", "role_membre", "date_inscription") },
    @{ Name = "classement_eleve"; X = 1870; Y = 760; Fields = @("eleve_id PK/FK", "score", "moyenne_generale", "total_absence_minutes", "a_un_avertissement", "updated_at") }
)

$boxes = @{}

foreach ($table in $tables) {
    $height = 62 + ($table.Fields.Count * 22)
    $rect = New-Object System.Drawing.Rectangle($table.X, $table.Y, 430, $height)
    $headerRect = New-Object System.Drawing.Rectangle($table.X, $table.Y, 430, 40)
    $graphics.FillRectangle($fillBrush, $rect)
    $graphics.DrawRectangle($linePen, $rect)
    $graphics.FillRectangle($headerBrush, $headerRect)
    $graphics.DrawString($table.Name, $headerFont, $headerTextBrush, ($table.X + 12), ($table.Y + 8))

    for ($i = 0; $i -lt $table.Fields.Count; $i++) {
        $graphics.DrawString($table.Fields[$i], $textFont, $textBrush, ($table.X + 12), ($table.Y + 48 + ($i * 22)))
    }

    $boxes[$table.Name] = $rect
}

function Get-CenterRight($rect) {
    return New-Object System.Drawing.Point(($rect.X + $rect.Width), ($rect.Y + [int]($rect.Height / 2)))
}

function Get-CenterLeft($rect) {
    return New-Object System.Drawing.Point($rect.X, ($rect.Y + [int]($rect.Height / 2)))
}

function Get-CenterBottom($rect) {
    return New-Object System.Drawing.Point(($rect.X + [int]($rect.Width / 2)), ($rect.Y + $rect.Height))
}

function Get-CenterTop($rect) {
    return New-Object System.Drawing.Point(($rect.X + [int]($rect.Width / 2)), $rect.Y)
}

$relations = @(
    @{ From = "specialite"; To = "promotion"; Start = "bottom"; End = "top" },
    @{ From = "specialite"; To = "cours"; Start = "bottom"; End = "top" },
    @{ From = "promotion"; To = "eleve"; Start = "right"; End = "left" },
    @{ From = "prof"; To = "prof_cours"; Start = "bottom"; End = "top" },
    @{ From = "cours"; To = "prof_cours"; Start = "right"; End = "left" },
    @{ From = "cours"; To = "instance_cours"; Start = "right"; End = "left" },
    @{ From = "prof"; To = "instance_cours"; Start = "bottom"; End = "top" },
    @{ From = "eleve"; To = "dossier"; Start = "bottom"; End = "top" },
    @{ From = "eleve"; To = "eleve_cours"; Start = "bottom"; End = "top" },
    @{ From = "cours"; To = "eleve_cours"; Start = "right"; End = "left" },
    @{ From = "eleve"; To = "note"; Start = "right"; End = "left" },
    @{ From = "cours"; To = "note"; Start = "right"; End = "left" },
    @{ From = "prof"; To = "note"; Start = "right"; End = "left" },
    @{ From = "eleve"; To = "absence"; Start = "right"; End = "left" },
    @{ From = "instance_cours"; To = "absence"; Start = "right"; End = "left" },
    @{ From = "prof"; To = "club"; Start = "bottom"; End = "top" },
    @{ From = "club"; To = "inscription_club"; Start = "right"; End = "left" },
    @{ From = "eleve"; To = "inscription_club"; Start = "bottom"; End = "top" },
    @{ From = "eleve"; To = "classement_eleve"; Start = "right"; End = "left" }
)

foreach ($relation in $relations) {
    $fromRect = $boxes[$relation.From]
    $toRect = $boxes[$relation.To]

    switch ($relation.Start) {
        "right" { $start = Get-CenterRight $fromRect }
        "left" { $start = Get-CenterLeft $fromRect }
        "top" { $start = Get-CenterTop $fromRect }
        default { $start = Get-CenterBottom $fromRect }
    }

    switch ($relation.End) {
        "right" { $end = Get-CenterRight $toRect }
        "left" { $end = Get-CenterLeft $toRect }
        "top" { $end = Get-CenterTop $toRect }
        default { $end = Get-CenterBottom $toRect }
    }

    $graphics.DrawLine($relationPen, $start, $end)
}

$legendFont = New-Object System.Drawing.Font("Segoe UI", 10)
$graphics.DrawString("PK = cle primaire | FK = cle etrangere | ? = nullable", $legendFont, $textBrush, 40, 1620)

$bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()
