# Registro de Decisiones de Arquitectura (ADRs) - AntigravitySkillsMove

## ADR-001: Arquitectura Multiplataforma con Cero Dependencias Externas
- **Contexto**: Para que la herramienta sea inmediatamente portable y funcione en cualquier computador sin requerir `pip install` previo ni permisos administrativos.
- **Decisión**: Toda la lógica central (`core.py`) está construida utilizando exclusivamente la biblioteca estándar de Python 3.8+ (`zipfile`, `urllib.request`, `shutil`, `json`, `pathlib`, `subprocess`, `argparse`).

## ADR-002: Sincronización Integral de Servidores MCP y Flujos Globales
- **Contexto**: Los servidores MCP (Model Context Protocol) en `~/.gemini/config/mcp_config.json` son esenciales para el funcionamiento de herramientas avanzadas en Antigravity.
- **Decisión**: Se incluye soporte bidireccional y preservación automática de `mcp_config.json` y `global_workflows/` tanto en empaquetado ZIP como en sincronización con Git/nube.

## ADR-003: Auditoría Preventiva de Seguridad y Chequeo de Salud (`--doctor`)
- **Contexto**: Al compartir paquetes o repositorios de skills, los desarrolladores pueden filtrar accidentalmente claves privadas o crear skills con metadatos YAML incompletos.
- **Decisión**: Se implementa un motor de auditoría (`audit_skills`) que analiza frontmatter YAML, longitud de descripciones y ejecuta expresiones regulares de escaneo sobre patrones de API Keys (OpenAI, Gemini, GitHub, Slack, Private Keys).

## ADR-004: Bootstrap de 1-Línea para Windows y Unix
- **Contexto**: Reducir a cero la fricción de instalación en equipos nuevos para maximizar adopción comunitaria.
- **Decisión**: Se crean `install.ps1` (ejecutable vía `irm ... | iex`) e `install.sh` (ejecutable vía `curl ... | bash`) que descargan y ejecutan la versión standalone en un directorio aislado de usuario (`~/.antigravity_skills_move/`).
