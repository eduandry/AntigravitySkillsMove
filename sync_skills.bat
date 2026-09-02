@echo off
chcp 65001 >nul
title AntigravitySkillsMove - Skills Manager
python "%~dp0antigravity_skills_move.py"
if %errorlevel% neq 0 (
    echo.
    echo [Error] Python no se pudo ejecutar. Asegúrate de tener Python instalado y en tu PATH.
    pause
)
