<div align="center">

# 🚀 AntigravitySkillsMove

### La Herramienta Definitiva para Transportar, Sincronizar en la Nube y Administrar Skills de Google Antigravity

[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Plataforma](https://img.shields.io/badge/plataforma-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=for-the-badge)]()
[![Google Antigravity](https://img.shields.io/badge/Google%20Antigravity-Compatible-green.svg?style=for-the-badge&logo=google)]()
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-2ea44f?style=for-the-badge)](https://eduandry.github.io/AntigravitySkillsMove/)
[![llms.txt](https://img.shields.io/badge/llms.txt-estándar-blueviolet?style=for-the-badge)](https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/llms.txt)

[English](README.md) • [Español](README_ES.md) • [🌐 Documentación Online](https://eduandry.github.io/AntigravitySkillsMove/) • [🤖 Contexto IA (llms.txt)](https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/llms.txt)

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

## ⚡ Ejecución Instantánea en 1 Línea (¡Sin Clonar el Repo!)

Ejecuta este comando directamente en tu terminal en CUALQUIER computador para iniciar AntigravitySkillsMove al instante:

#### 🪟 Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/install.ps1 | iex
```

#### 🍎 macOS / 🐧 Linux (Bash):
```bash
curl -sSL https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/install.sh | bash
```

---

## ⚡ Inicio Rápido (Clonar o PIP)

### Opción A: Clonar el Repositorio
```bash
git clone https://github.com/eduandry/AntigravitySkillsMove.git
cd AntigravitySkillsMove
python antigravity_skills_move.py
```

> **Usuarios de Windows**: Puedes hacer doble clic directamente en [`sync_skills.bat`](sync_skills.bat).

### Opción B: Instalación con PIP (Comando Global)
```bash
pip install .
antigravity-skills-move --list
```

---

## 🎮 Funcionalidades y Uso

### 🩺 1. Auditoría de Salud y Seguridad (`--doctor`)
Analiza la calidad de todas tus skills (valida frontmatter YAML, longitud óptima de descripción y **escanea preventivamente posibles API keys o contraseñas expuestas**):

```bash
python antigravity_skills_move.py --doctor
```

---

### 🌐 2. Instalar Skills Directamente desde GitHub o URL (`--install-remote`)
Descarga e instala cualquier skill individual o colección desde GitHub o archivo ZIP con un solo comando:

```bash
python antigravity_skills_move.py --install-remote "https://github.com/usuario/mi-skill-antigravity"
```

---

### 📋 3. Listar Skills y Plugins Instalados
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
