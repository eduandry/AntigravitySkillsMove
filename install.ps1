# AntigravitySkillsMove - 1-Line Bootstrap Installer for Windows
# Run via: irm https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/install.ps1 | iex

$ErrorActionPreference = "Stop"

Write-Host "`n🚀 [AntigravitySkillsMove] Inicializando instalación rápida..." -ForegroundColor Cyan

$InstallDir = "$HOME\.antigravity_skills_move"
if (!(Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}

$ScriptUrl = "https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/antigravity_skills_move.py"
$CoreUrl = "https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/antigravity_skills_move/core.py"
$CliUrl = "https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/antigravity_skills_move/cli.py"
$InitUrl = "https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/antigravity_skills_move/__init__.py"

$PkgDir = "$InstallDir\antigravity_skills_move"
if (!(Test-Path $PkgDir)) {
    New-Item -ItemType Directory -Path $PkgDir -Force | Out-Null
}

Write-Host "⬇️ Descargando componentes más recientes..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $ScriptUrl -OutFile "$InstallDir\antigravity_skills_move.py" -UseBasicParsing
Invoke-WebRequest -Uri $CoreUrl -OutFile "$PkgDir\core.py" -UseBasicParsing
Invoke-WebRequest -Uri $CliUrl -OutFile "$PkgDir\cli.py" -UseBasicParsing
Invoke-WebRequest -Uri $InitUrl -OutFile "$PkgDir\__init__.py" -UseBasicParsing

Write-Host "✅ ¡AntigravitySkillsMove instalado exitosamente en $InstallDir!" -ForegroundColor Green
Write-Host "🎮 Iniciando menú interactivo...`n" -ForegroundColor Cyan

python "$InstallDir\antigravity_skills_move.py"
