# Historial de Cambios (CHANGELOG) - AntigravitySkillsMove

Todas las modificaciones notables de este proyecto están registradas en este documento.

---

## [1.3.0] - 2026-09-04
### Soporte Integral de Reglas Globales (GEMINI.md / AGENTS.md) y Clonación de Paquetes
- **Transferencia Integral de Repositorios Remotos (`install_from_url_or_git`)**: Soporte para clonar e instalar de una sola vez skills, reglas (`rules/`), plugins, workflows, `mcp_config.json` y reglas raíz (`GEMINI.md`/`AGENTS.md`).
- **Detección y Sincronización de Reglas Standalone**: Reconocimiento automático de `~/.gemini/GEMINI.md` y `~/.gemini/AGENTS.md` en `--list`, `export_bundle`, `import_bundle` y `sync_with_folder`.
- **Deduplicación de Reglas**: Evita duplicaciones si la regla existe simultáneamente en `~/.gemini/` y `~/.gemini/config/`.
- **Actualización de Menú Interactivo**: Opciones 1, 2, 5 y 9 refinadas para reflejar el soporte integral de reglas y paquetes.

## [1.2.0] - 2026-09-02
### Infraestructura SEO y Descubrimiento para IAs (GitHub Pages & llms.txt)
- **Estándar `llms.txt` y `llms-full.txt`**: Creados según la especificación llmstxt.org para consumo directo y eficiente por modelos de lenguaje (Gemini, Claude, GPT, Perplexity).
- **Portal Estático para GitHub Pages (`docs/index.html`)**: Landing page moderna, accesible y responsive con datos estructurados Schema.org JSON-LD (`SoftwareApplication`), OpenGraph y Twitter Cards.
- **Rastreo y Mapa de Sitio (`docs/robots.txt` y `docs/sitemap.xml`)**: Permisos de acceso total para buscadores y bots de IA (`Google-Extended`, `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Googlebot`, `Bingbot`).
- **Insignias y Accesos Directos**: Integración de badges y enlaces directos a la documentación y archivos RAW en `README.md` y `README_ES.md`.

## [1.1.0] - 2026-09-02
### Lanzadores Bootstrap, Chequeo de Salud y Soporte MCP
- **Instaladores de 1-Línea (`install.ps1` y `install.sh`)**: Ejecución instantánea en cualquier máquina sin necesidad de clonar manualmente el repositorio.
- **Chequeo de Salud y Linter (`--doctor`)**: Diagnóstico automático de metadatos YAML, validación de descripciones y escáner preventivo de credenciales/API keys expuestas.
- **Instalación Remota Directa (`--install-remote <URL>`)**: Descarga e instalación de skills directamente desde URLs de GitHub o archivos ZIP.
- **Sincronización de Servidores MCP**: Soporte completo para replicar y transferir `mcp_config.json` y flujos globales entre computadores.
- **Exportación e Importación Selectiva**: Capacidad de elegir subconjuntos específicos de skills para mover entre dispositivos.

## [1.0.0] - 2026-09-02
### Lanzamiento Inicial
- Motor central `core.py` con descubrimiento y empaquetado ZIP portable.
- Menú interactivo por consola y comandos CLI.
- Sincronización bidireccional de carpetas y repositorios Git.
- Creador asistido de plantillas de skills (`create_new_skill`).
- Documentación completa en inglés y español con licencia MIT.
