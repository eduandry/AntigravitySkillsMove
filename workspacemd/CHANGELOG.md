# Historial de Cambios (CHANGELOG) - AntigravitySkillsMove

Todas las modificaciones notables de este proyecto están registradas en este documento.

---

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
