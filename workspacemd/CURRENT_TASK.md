# Tarea Actual: Diagnóstico y Soporte Integral para Clonación y Transferencia de Reglas (rules/ y GEMINI.md)

**Estado:** Completado exitosamente.

---

## 🔍 Diagnóstico Realizado:
- **Causa 1 (Clonación remota)**: La función `install_from_url_or_git()` clonaba los repositorios pero únicamente copiaba carpetas dentro de `skills/`, ignorando completamente `rules/`, `plugins/`, `mcp_config.json`, `global_workflows/` y archivos de reglas raíz.
- **Causa 2 (Ubicación de Reglas)**: Las reglas activas del usuario residen en `~/.gemini/GEMINI.md` (o `~/.gemini/AGENTS.md`), pero `AntigravitySkillsMove` solo inspeccionaba `~/.gemini/config/rules/`. Al estar esta última carpeta vacía, el sistema reportaba 0 reglas y no las transfería ni las exportaba.

---

## ✅ Mejoras Implementadas:
- [x] **Detección Ampliada de Reglas**: `list_installed_items()` ahora detecta reglas en `~/.gemini/config/rules/*.md` y reglas raíz `GEMINI.md` y `AGENTS.md` (tanto en `~/.gemini` como en `~/.gemini/config`), deduplicando por nombre.
- [x] **Clonación Integral de Paquetes Remotos**: `install_from_url_or_git()` ahora detecta si el repositorio remoto contiene `skills/`, `rules/`, `plugins/`, `mcp_config.json`, `global_workflows/` o `GEMINI.md`, e instala todo el ecosistema de forma completa.
- [x] **Exportación e Importación de Reglas Globales**: `export_bundle()` y `import_bundle()` empaquetan y restauran `GEMINI.md` y `AGENTS.md`.
- [x] **Sincronización Bidireccional de Reglas**: `sync_with_folder()` ahora sincroniza `GEMINI.md` y `AGENTS.md` además de la carpeta `rules/`.
- [x] **Pruebas de Validación**: Verificado el listado, exportación a ZIP, sincronización con carpetas y clonación de repositorios mock con reglas.
