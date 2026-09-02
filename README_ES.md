<div align="center">

# 🚀 AntigravitySkillsMove

### La Herramienta Definitiva para Transportar, Sincronizar en la Nube y Administrar Skills de Google Antigravity

[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Plataforma](https://img.shields.io/badge/plataforma-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=for-the-badge)]()
[![Google Antigravity](https://img.shields.io/badge/Google%20Antigravity-Compatible-green.svg?style=for-the-badge&logo=google)]()

[English](README.md) • [Español](README_ES.md)

<br/>

```text
   _____          __  .__                               .__  __         
  /  _  \   _____/  |_|__| _______________ ___  ________/  |/  |_ ___.__.
 /  /_\  \ /    \   __\  |/ ___\_  __ \__  \\  \/ /\__  <   __\   __<   |  |
/    |    \   |  \  | |  / /_/  >  | \// __ \\   /  / __ \|  |  |  |  \___  |
\____|__  /___|  /__| |__\___  /|__|  (____  /\_/  (____  /__|  |__|  / ____|
        \/     \/       /_____/            \/           \/            \/     
                  SKILLS MOVE & SYNC MANAGER
```

**Nunca vuelvas a perder o tener que reconfigurar tus Skills de Antigravity.**  
Exporta, traslada, genera y mantén sincronizadas todas tus Skills, Plugins y Reglas personalizadas entre tu laptop, PC de escritorio y estación de trabajo con **un solo comando**.

</div>

---

## 💡 ¿Por qué AntigravitySkillsMove?

**Google Antigravity** es uno de los entornos de desarrollo asistido por IA más avanzados, pero sus configuraciones y skills personalizadas se almacenan localmente en cada equipo (`~/.gemini/config/skills`).

Cuando cambias de computador (por ejemplo, del portátil a la oficina), tus prompts especializados, runbooks y herramientas no están disponibles.

**AntigravitySkillsMove soluciona esto al instante:**
- 🔄 **Sincronización Automática con Nube / Git**: Conecta una carpeta compartida en Google Drive, Dropbox, OneDrive o un repositorio Git privado. Tus skills se sincronizan bidireccionalmente.
- 📦 **Paquetes Portables en 1 Clic**: Empaqueta 50+ skills y plugins en un único `.zip` para llevar en una memoria USB.
- ⚡ **Cero Dependencias**: Escrito en Python estándar puro (funciona directamente en Windows, macOS y Linux).
- 🛡️ **Seguridad Total**: Genera respaldos automáticos con marca de tiempo antes de cualquier importación o actualización.
- 🛠️ **Creador Asistido de Skills**: Genera la estructura oficial `SKILL.md` con frontmatter YAML en segundos.

---

## ⚡ Inicio Rápido

### 1. Ejecución Directa (Sin Instalación)

```bash
# Clonar el repositorio
git clone https://github.com/eduandry/AntigravitySkillsMove.git
cd AntigravitySkillsMove

# Iniciar menú interactivo
python antigravity_skills_move.py
```

> **Usuarios de Windows**: Puedes hacer doble clic directamente en [`sync_skills.bat`](file:///e:/IA/Desarrollos/Traductor/AntigravitySkillsMove/sync_skills.bat).

---

### 2. Instalación con PIP (Comando Global en Terminal)

```bash
pip install .
```

¡Ahora tienes el comando `antigravity-skills-move` disponible en cualquier terminal!

```bash
antigravity-skills-move --list
```

---

## 🎮 Funcionalidades y Uso

### 📋 1. Listar Skills y Plugins Instalados
Consulta qué skills, plugins y reglas están activas en tu Antigravity:

```bash
python antigravity_skills_move.py --list
```

---

### 📦 2. Exportar / Empaquetar Skills a un Archivo ZIP Portable
Crea un paquete de respaldo o transporte:

```bash
# Exportación con nombre automático timestamped
python antigravity_skills_move.py --export

# O especifica una ruta destino
python antigravity_skills_move.py --export "D:\Respaldos\mis_skills_antigravity.zip"
```

---

### 🚀 3. Importar e Instalar en un Nuevo Computador
Lleva tu archivo `.zip` al nuevo equipo e instala todo con un comando:

```bash
python antigravity_skills_move.py --import-zip "mis_skills_antigravity.zip"
```

---

### 🔄 4. Sincronización Automática Bidireccional (Nube / Git)
Mantén tus equipos siempre sincronizados a través de una carpeta en la nube o un repositorio Git:

```bash
# Sincronización bidireccional (descarga novedades y sube cambios locales)
python antigravity_skills_move.py --sync-folder "D:\MiDrive\AntigravitySkills" --sync-mode both

# Solo descargar (Pull)
python antigravity_skills_move.py --sync-folder "D:\MiDrive\AntigravitySkills" --sync-mode pull

# Solo subir (Push)
python antigravity_skills_move.py --sync-folder "D:\MiDrive\AntigravitySkills" --sync-mode push
```

> 💡 **Integración con Git**: Si tu carpeta compartida es un repositorio Git, AntigravitySkillsMove ejecuta automáticamente `git pull`, `git add`, `git commit` y `git push`.

---

### ➕ 5. Crear una Nueva Skill Personalizada
Crea una skill con la estructura oficial:

```bash
python antigravity_skills_move.py --add-skill "Optimizador de Postgres" --description "Usar esta skill al optimizar consultas SQL lentas y reportes EXPLAIN ANALYZE."
```

---

## 🗺️ Dónde Guarda Antigravity las Skills

| Alcance | Sistema Operativo | Ruta Absoluta |
| :--- | :--- | :--- |
| **Global (Skills)** | **Windows** | `C:\Users\<Usuario>\.gemini\config\skills\` |
| **Global (Plugins)** | **Windows** | `C:\Users\<Usuario>\.gemini\config\plugins\` |
| **Global (Reglas)** | **Windows** | `C:\Users\<Usuario>\.gemini\config\rules\` |
| **Global (Todas)** | **macOS / Linux** | `~/.gemini/config/skills/` y `~/.gemini/config/plugins/` |
| **Workspace** | **Todos** | `<RaízProyecto>/.agents/skills/<nombre-skill>/` |

---

## 📄 Licencia

Distribuido bajo la Licencia **MIT**. Consulta [LICENSE](LICENSE) para más detalles.
