#!/usr/bin/env bash
# AntigravitySkillsMove - 1-Line Bootstrap Installer for macOS & Linux
# Run via: curl -sSL https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/install.sh | bash

set -e

echo -e "\n\033[1;36m🚀 [AntigravitySkillsMove] Inicializando instalación rápida...\033[0m"

INSTALL_DIR="$HOME/.antigravity_skills_move"
PKG_DIR="$INSTALL_DIR/antigravity_skills_move"

mkdir -p "$PKG_DIR"

BASE_URL="https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main"

echo -e "\033[1;33m⬇️ Descargando componentes más recientes...\033[0m"
curl -sSL "$BASE_URL/antigravity_skills_move.py" -o "$INSTALL_DIR/antigravity_skills_move.py"
curl -sSL "$BASE_URL/antigravity_skills_move/core.py" -o "$PKG_DIR/core.py"
curl -sSL "$BASE_URL/antigravity_skills_move/cli.py" -o "$PKG_DIR/cli.py"
curl -sSL "$BASE_URL/antigravity_skills_move/__init__.py" -o "$PKG_DIR/__init__.py"

chmod +x "$INSTALL_DIR/antigravity_skills_move.py"

echo -e "\033[1;32m✅ ¡AntigravitySkillsMove instalado exitosamente en $INSTALL_DIR!\033[0m"
echo -e "\033[1;36m🎮 Iniciando menú interactivo...\033[0m\n"

python3 "$INSTALL_DIR/antigravity_skills_move.py"
