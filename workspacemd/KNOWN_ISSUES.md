# Problemas Conocidos y Hallazgos (KNOWN_ISSUES)

## 1. Visibilidad y Detección por IAs Externas (Gemini / Crawlers Web)

### Contexto
Al consultar el repositorio `https://github.com/eduandry/AntigravitySkillsMove` desde modelos de lenguaje externos (como la app web de Gemini o buscadores automatizados), el modelo puede indicar que el repositorio "no es accesible", "no tiene README.md" o "no expone una descripción pública detallada".

### Diagnóstico Técnico Verificado
1. **El repositorio SÍ es público**:
   - Validación contra la API oficial de GitHub (`https://api.github.com/repos/eduandry/AntigravitySkillsMove`):
     - `private: false`
     - El acceso anónimo (modo incógnito) funciona correctamente.
2. **El README.md SÍ existe y está publicado**:
   - Validación contra la API: `name: README.md`, tamaño 8,309 bytes.
   - Disponible públicamente en rama `main`.
3. **Causa 1 - Campo "About / Description" vacío en GitHub**:
   - En los metadatos del repositorio en GitHub, el campo `description` estaba en `null` (`None`).
   - Al no contar con una descripción configurada en la sección "About", GitHub inyecta una etiqueta meta genérica:
     `<meta name="description" content="Contribute to eduandry/AntigravitySkillsMove development by creating an account on GitHub.">`
   - Los rastreadores e IAs que leen los metadatos OpenGraph no encuentran una descripción real del propósito de la herramienta.
4. **Causa 2 - Renderizado dinámico de GitHub (React Island / SPA) vs Rastreadores sin JS**:
   - La interfaz moderna de GitHub requiere ejecución de JavaScript para hidratar el contenido del árbol de archivos y renderizar el Markdown en el navegador.
   - El web crawler o scraper en tiempo real de Gemini no ejecuta el JavaScript completo de GitHub o se detiene ante bloqueos preventivos contra bots, impidiendo leer el DOM del README y generando una respuesta de fallo genérica (alucinación de "no tiene README").

### Soluciones Implementadas y Recomendadas
1. **Configurar el campo "About" en GitHub**:
   - Agregar descripción pública en la sección de configuración del repositorio:
     `The complete CLI & GUI toolkit to export, migrate, audit, and sync Google Antigravity skills, plugins, rules, and MCP servers across machines.`
   - Agregar topics (etiquetas): `antigravity`, `gemini`, `skills`, `mcp`, `automation`, `sync`.
2. **Uso de URL Raw para análisis por IAs**:
   - Cuando se consulte a modelos de lenguaje o analizadores de código externos, suministrar la URL sin procesar (RAW) que entrega texto plano directo sin capas de JavaScript de GitHub:
     - `https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/README.md`
     - `https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/README_ES.md`

---

## 2. Omisión de Reglas (`rules/` y `GEMINI.md`) en Clonación y Sincronización

### Contexto
Al utilizar `AntigravitySkillsMove` para clonar o transferir un repositorio remoto (ej. `MyAntigravitySkills`), las reglas no se transferían a la máquina de destino.

### Diagnóstico Técnico Verificado
1. **`install_from_url_or_git()` solo copiaba `skills/`**:
   - En `core.py`, la función clonaba el repositorio pero su lógica solo evaluaba si existía `clone_dest / "skills"`, copiando exclusivamente las subcarpetas de skills e ignorando completamente las carpetas `rules/`, `plugins/`, `global_workflows/` y el archivo `mcp_config.json`.
2. **Ubicación de Reglas Globales en Antigravity**:
   - Las reglas globales activas del usuario se encuentran en `~/.gemini/GEMINI.md` (o `~/.gemini/AGENTS.md`), además de `~/.gemini/config/rules/*.md`.
   - `core.py` (`list_installed_items`, `export_bundle`, `sync_with_folder`) únicamente buscaba en `~/.gemini/config/rules/`.
   - Como la carpeta `~/.gemini/config/rules/` estaba vacía, el sistema reportaba 0 reglas y no exportaba ni sincronizaba `~/.gemini/GEMINI.md`.
   - Por esta razón, el repositorio remoto `MyAntigravitySkills` tenía su carpeta `rules/` vacía y carecía de `GEMINI.md`.

### Solución Requerida
1. Extender `core.py` para detectar, listar, exportar y sincronizar tanto `~/.gemini/config/rules/` como `~/.gemini/GEMINI.md` y `~/.gemini/AGENTS.md`.
2. Actualizar `install_from_url_or_git()` para que clone y transfiera de forma integral: `skills/`, `rules/`, `plugins/`, `mcp_config.json`, `global_workflows/` y archivos de reglas raíz (`GEMINI.md`/`AGENTS.md`).
3. Sincronizar la regla actual `~/.gemini/GEMINI.md` hacia `MyAntigravitySkills` y el repositorio remoto para que esté disponible en la nube.
