# 🛰️ Guía de Gestión y Sincronización de Skills en Antigravity

Esta guía explica en detalle **dónde se almacenan las Skills en Google Antigravity** y cómo utilizar la herramienta multiplataforma [`antigravity_skill_sync.py`](file:///e:/IA/Desarrollos/Traductor/antigravity_skill_sync.py) para transferir, respaldar, agregar y sincronizar automáticamente todas tus skills entre diferentes computadores.

---

## 1. ¿Dónde se guardan las Skills de Antigravity?

Antigravity organiza las skills y customizaciones en tres niveles con diferente alcance y prioridad:

```
┌───────────────────────────────────────────────────────────────────────┐
│ 1. Globales (Máquina Local - Disponibles en TODOS tus proyectos)       │
│    📂 ~/.gemini/config/skills/                                        │
│    📂 ~/.gemini/config/plugins/                                       │
├───────────────────────────────────────────────────────────────────────┤
│ 2. De Proyecto / Workspace (Específicas de un repositorio)             │
│    📂 <carpeta-del-proyecto>/.agents/skills/                          │
│    📂 <carpeta-del-proyecto>/.agents/plugins/                         │
├───────────────────────────────────────────────────────────────────────┤
│ 3. Integradas del IDE (Skills por defecto incluidas con Antigravity)  │
│    📂 ~/.gemini/antigravity-ide/builtin/skills/                       │
└───────────────────────────────────────────────────────────────────────┘
```

### Rutas Absolutas por Sistema Operativo:

| Nivel | Sistema Operativo | Ruta en el Sistema de Archivos |
| :--- | :--- | :--- |
| **Global (Skills)** | **Windows** | `C:\Users\<TuUsuario>\.gemini\config\skills\` |
| **Global (Plugins)**| **Windows** | `C:\Users\<TuUsuario>\.gemini\config\plugins\` |
| **Global (Reglas)** | **Windows** | `C:\Users\<TuUsuario>\.gemini\config\rules\` |
| **Global (Todas)**  | **macOS / Linux** | `~/.gemini/config/skills/` y `~/.gemini/config/plugins/` |
| **Workspace**       | **Cualquiera** | `<RaízDelProyecto>/.agents/skills/<nombre-skill>/` |
| **Built-in IDE**    | **Windows** | `C:\Users\<TuUsuario>\.gemini\antigravity-ide\builtin\skills\` |

---

## 2. Herramienta de Sincronización y Transporte: `antigravity_skill_sync.py`

Se ha creado la herramienta automatizada [`antigravity_skill_sync.py`](file:///e:/IA/Desarrollos/Traductor/antigravity_skill_sync.py) y su lanzador Windows [`sync_skills.bat`](file:///e:/IA/Desarrollos/Traductor/sync_skills.bat).

### Métodos de Transporte Disponibles

### Opción A: Sincronización Automática en la Nube / Git (Recomendado)
Puedes apuntar a una carpeta compartida en **Google Drive, Dropbox, OneDrive** o un **Repositorio Git privado** donde tengas tu colección de skills.

1. **Desde la consola o menú interactivo**:
   ```bash
   python antigravity_skill_sync.py --sync-folder "D:\MiDrive\AntigravitySkills" --sync-mode both
   ```
2. **Qué hace automáticamente**:
   - **Descarga (Pull)**: Detecta skills nuevas o modificadas en otros equipos y las instala en el Antigravity de este equipo.
   - **Sube (Push)**: Detecta skills nuevas o modificadas en este equipo y las envía a la carpeta compartida/repo para que tus demás equipos las reciban.

### Opción B: Exportar e Importar mediante Paquete ZIP Portable
Ideal para mover todo en una memoria USB o enviar por correo/mensajería:

1. **En tu equipo actual (Exportar)**:
   ```bash
   python antigravity_skill_sync.py --export "mis_skills_antigravity.zip"
   ```
   *Genera un archivo `.zip` que contiene tus 41+ skills, plugins y reglas.*

2. **En tu nuevo equipo (Importar e Instalar)**:
   - Copias el script `antigravity_skill_sync.py` y tu archivo `.zip` al nuevo equipo.
   - Ejecutas:
     ```bash
     python antigravity_skill_sync.py --import-zip "mis_skills_antigravity.zip"
     ```
   *El script detecta la carpeta `~/.gemini/config/` del nuevo equipo, crea un respaldo preventivo y extrae todas las skills en su ubicación exacta.*

---

## 3. Menú Interactivo Visual

Si ejecutas el script sin parámetros o haces doble clic en [`sync_skills.bat`](file:///e:/IA/Desarrollos/Traductor/sync_skills.bat):

```text
================================================================================
 🛰️  ANTIGRAVITY SKILL SYNC & MANAGER (Transportador de Skills)
================================================================================
  1. 📋 Listar todas las Skills y Plugins instalados en este equipo
  2. 📦 Exportar / Empaquetar todas mis Skills en un archivo ZIP portable
  3. 🚀 Importar / Instalar Skills desde un archivo ZIP
  4. 🔄 Sincronizar automáticamente con Carpeta Compartida / Drive / Git
  5. ➕ Crear / Agregar una nueva Skill personalizada
  6. 📂 Abrir carpeta de Skills de Antigravity en el Explorador de Archivos
  0. ❌ Salir
================================================================================
```

---

## 4. Estructura Requerida de una Skill

Cada skill dentro de `skills/<nombre-de-la-skill>/` debe tener como mínimo un archivo `SKILL.md` con su bloque YAML:

```markdown
---
name: mi-skill-personalizada
description: >-
  Explica detalladamente cuándo y por qué Antigravity debe activar esta skill.
---

# Título de la Skill

Instrucciones y pasos detallados para el agente.
```

Subcarpetas opcionales recomendadas:
- `scripts/`: Scripts ejecutables auxiliares (Python, JS, Bash, PowerShell).
- `references/`: Documentación extensa o manuales de referencia.
- `examples/`: Ejemplos prácticos de código o configuraciones.
