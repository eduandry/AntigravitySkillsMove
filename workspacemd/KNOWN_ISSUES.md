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
