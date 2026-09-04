# Estado del Proyecto: AntigravitySkillsMove

**Fecha de última actualización:** 2026-09-04  
**Estado actual:** PRODUCCIÓN Y PUBLICADO (V1.3.0)  
**Versión:** 1.3.0-production  
**Repositorio GitHub:** https://github.com/eduandry/AntigravitySkillsMove.git  

---

## 🎯 Resumen del Proyecto
**AntigravitySkillsMove** es una herramienta de código abierto de nivel empresarial para exportar, trasladar, auditar, generar y sincronizar de forma bidireccional todas las Skills, Plugins, Reglas y Servidores MCP (Model Context Protocol) de Google Antigravity entre diferentes computadores.

---

## 🧩 Componentes Entregados:
1. **Motor Central (`antigravity_skills_move/core.py`)**:
   - Detección automática de la ruta de configuración global `~/.gemini/config` y `~/.gemini/`.
   - Empaquetado y desempaquetado de archivos ZIP portables con manifiesto JSON, incluyendo reglas globales (`rules/` y `GEMINI.md`/`AGENTS.md`).
   - Sincronización bidireccional automática con carpetas de nube (Google Drive, Dropbox, OneDrive) o repositorios Git (auto `git pull/push`).
   - Sincronización integral de Servidores MCP (`mcp_config.json`), reglas y flujos globales (`global_workflows/`).
   - Chequeo de salud (`audit_skills`) con validación de metadatos YAML y escaneo preventivo de credenciales o secretos expuestos.
   - Instalación remota directa de paquetes completos desde URLs de repositorios GitHub o archivos ZIP (`install_from_url_or_git`).
   - Generador asistido de nuevas skills con plantilla oficial y estructura de carpetas (`create_new_skill`).

2. **Interfaz CLI & Menú Interactivo (`antigravity_skills_move/cli.py` & `antigravity_skills_move.py`)**:
   - Menú por consola numerado y a color con ASCII Banner.
   - Argumentos CLI para automatización (`--list`, `--doctor`, `--export`, `--import-zip`, `--install-remote`, `--sync-folder`, `--add-skill`).

3. **Instaladores de 1-Línea y Lanzadores**:
   - Windows PowerShell 1-liner: `install.ps1`
   - macOS / Linux Bash 1-liner: `install.sh`
   - Acceso directo doble-clic: `sync_skills.bat` (Windows) y `sync_skills.sh` (macOS/Linux).

4. **Infraestructura de Código Abierto & CI/CD**:
   - Empaquetado `pyproject.toml` y `setup.py`.
   - GitHub Actions CI en `.github/workflows/ci.yml` (Windows, macOS, Ubuntu).
   - Plantillas de issues en `.github/ISSUE_TEMPLATE/` y guía de contribución `CONTRIBUTING.md`.
   - Licencia MIT y documentación bilingüe (`README.md` y `README_ES.md`).

5. **Infraestructura SEO y Soporte para IAs (GitHub Pages & llms.txt)**:
   - Estándar `llms.txt` y `llms-full.txt` para lectura directa por LLMs (Gemini, ChatGPT, Claude, Perplexity).
   - Portal web estático `docs/index.html` con Schema.org JSON-LD `SoftwareApplication` y diseño moderno responsive.
   - Archivos de rastreo e indexación `docs/robots.txt` y `docs/sitemap.xml`.
