param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Payload = Join-Path $RepoRoot "translation"
$Script = Join-Path $PSScriptRoot "star_citizen_it_installer.py"
$VersionInfo = Join-Path $PSScriptRoot "version_info.txt"
$Icon = Join-Path $RepoRoot "assets\icon\star_citizen_installer_italia.ico"
$StarBreaker = Join-Path $PSScriptRoot "vendor\starbreaker\0.3.2\starbreaker.exe"
$StarBreakerNotice = Join-Path $PSScriptRoot "vendor\starbreaker\0.3.2\NOTICE.md"
$Build = Join-Path $RepoRoot "build\4.10-r1"
$Work = Join-Path $Build "work"
$Spec = Join-Path $Build "spec"
$Dist = Join-Path $Build "dist"

if (-not (Test-Path -LiteralPath (Join-Path $Payload "Data\Localization\italian_(italy)\global.ini"))) {
    throw "Payload italiano non trovato: $Payload"
}
if (-not (Test-Path -LiteralPath $Icon)) {
    throw "Icona installer non trovata: $Icon"
}
if (-not (Test-Path -LiteralPath $StarBreaker)) {
    throw "Modulo di verifica StarBreaker non trovato: $StarBreaker"
}

& $Python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --console `
    --name "StarCitizen_Traduzione_Italiana_4.10_R1" `
    --icon $Icon `
    --version-file $VersionInfo `
    --add-data "$Payload;payload" `
    --add-data "$StarBreakerNotice;vendor" `
    --add-binary "$StarBreaker;vendor" `
    --workpath $Work `
    --specpath $Spec `
    --distpath $Dist `
    $Script

if ($LASTEXITCODE -ne 0) {
    throw "Creazione installer non riuscita."
}

$Exe = Join-Path $Dist "StarCitizen_Traduzione_Italiana_4.10_R1.exe"
if (-not (Test-Path -LiteralPath $Exe)) {
    throw "L'eseguibile finale non è stato creato."
}

$Item = Get-Item -LiteralPath $Exe
$Hash = (Get-FileHash -LiteralPath $Exe -Algorithm SHA256).Hash
Write-Output "FILE=$($Item.FullName)"
Write-Output "SIZE=$($Item.Length)"
Write-Output "SHA256=$Hash"
