param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Payload = Join-Path $RepoRoot "translation"
$Script = Join-Path $PSScriptRoot "star_citizen_it_installer.py"
$VersionInfo = Join-Path $PSScriptRoot "version_info.txt"
$Build = Join-Path $RepoRoot "build"
$Work = Join-Path $Build "work"
$Spec = Join-Path $Build "spec"
$Dist = Join-Path $Build "dist"

if (-not (Test-Path -LiteralPath (Join-Path $Payload "Data\Localization\italian_(italy)\global.ini"))) {
    throw "Payload italiano non trovato: $Payload"
}

& $Python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --console `
    --name "StarCitizen_Traduzione_Italiana_4.9_R1" `
    --version-file $VersionInfo `
    --add-data "$Payload;payload" `
    --workpath $Work `
    --specpath $Spec `
    --distpath $Dist `
    $Script

if ($LASTEXITCODE -ne 0) {
    throw "Creazione installer non riuscita."
}

$Exe = Join-Path $Dist "StarCitizen_Traduzione_Italiana_4.9_R1.exe"
if (-not (Test-Path -LiteralPath $Exe)) {
    throw "L'eseguibile finale non è stato creato."
}

$Item = Get-Item -LiteralPath $Exe
$Hash = (Get-FileHash -LiteralPath $Exe -Algorithm SHA256).Hash
Write-Output "FILE=$($Item.FullName)"
Write-Output "SIZE=$($Item.Length)"
Write-Output "SHA256=$Hash"
