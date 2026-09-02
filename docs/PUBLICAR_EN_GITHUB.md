# 🚀 Guía de Publicación y Estrategia Viral para `AntigravitySkillsMove`

Esta guía contiene los pasos exactos para publicar el repositorio en GitHub y la estrategia recomendada para darle visibilidad internacional y convertirlo en una herramienta viral en la comunidad de IA y Antigravity.

---

## 📦 1. Estado del Repositorio Local

El proyecto ya está completamente creado, configurado y empaquetado como repositorio Git local en:
`e:\IA\Desarrollos\Traductor\AntigravitySkillsMove`

### Componentes Listos en el Repositorio:
- ✅ **`README.md` y `README_ES.md`**: Documentación bilingüe con badges, arte ASCII, ejemplos de uso y tablas visuales.
- ✅ **`pyproject.toml` y `setup.py`**: Listo para instalación con `pip` y publicación en PyPI (`pip install antigravity-skills-move`).
- ✅ **Paquete modular (`antigravity_skills_move/`)**: Arquitectura limpia con `core.py` y `cli.py`.
- ✅ **Script standalone (`antigravity_skills_move.py`)**: Ejecutable en un solo archivo con cero dependencias externas.
- ✅ **Lanzadores 1-Clic**: `sync_skills.bat` (Windows) y `sync_skills.sh` (macOS/Linux).
- ✅ **GitHub Actions CI (`.github/workflows/ci.yml`)**: Pruebas automáticas en Ubuntu, Windows y macOS.
- ✅ **Plantillas de Issues y Contribución**: `.github/ISSUE_TEMPLATE/` y `CONTRIBUTING.md`.
- ✅ **Licencia MIT** y `.gitignore` optimizado.

---

## 🌐 2. Pasos para Crear y Subir el Repositorio a GitHub

### Paso 1: Crear el Repositorio en GitHub
1. Abre tu navegador e ingresa a [GitHub - New Repository](https://github.com/new).
2. **Repository name**: `AntigravitySkillsMove`
3. **Description**: `🚀 The ultimate cross-platform tool to export, import, sync, and manage Google Antigravity skills across multiple computers.`
4. **Visibility**: Selecciona **Public** (Público).
5. **Initialize this repository with**: Deja todas las casillas **desmarcadas** (NO agregues README, .gitignore ni License porque ya los tenemos listos y configurados).
6. Haz clic en **Create repository**.

---

### Paso 2: Subir tu Código a GitHub (`eduandry/AntigravitySkillsMove`)

El repositorio local ya tiene configurado el remote oficial: `https://github.com/eduandry/AntigravitySkillsMove.git`.

Para subir el código a tu cuenta `eduandry`:

#### Opción A: Usando un Personal Access Token (PAT) de GitHub (Más rápido)
Si tienes un token de acceso personal clásico o fine-grained (con permisos `repo`):
```powershell
cd E:\IA\Desarrollos\Traductor\AntigravitySkillsMove
git push https://<TU_TOKEN_PAT>@github.com/eduandry/AntigravitySkillsMove.git main
```

#### Opción B: Actualizar tus credenciales en Windows
Si Windows tiene guardada otra cuenta de GitHub (ej: `tecnologiamzl`):
1. Presiona `Win + R`, escribe `control /name Microsoft.CredentialManager` y presiona Enter.
2. Ve a **Credenciales de Windows** (Windows Credentials).
3. Busca la entrada `git:https://github.com`.
4. Haz clic en **Editar** y pon tu usuario `eduandry` y tu Token de GitHub como contraseña.
5. Luego ejecuta:
   ```powershell
   cd E:\IA\Desarrollos\Traductor\AntigravitySkillsMove
   git push -u origin main
   ```

#### Opción C: Mediante SSH (si tienes tu clave SSH vinculada a eduandry)
```powershell
cd E:\IA\Desarrollos\Traductor\AntigravitySkillsMove
git remote set-url origin git@github.com:eduandry/AntigravitySkillsMove.git
git push -u origin main
```


---

## 🌟 3. Configuración en GitHub para Maximizar Visibilidad

Una vez subido el repositorio a GitHub:

### A. Temas y Etiquetas (Topics / Tags)
En la página principal de tu repositorio en GitHub, haz clic en el ícono de engranaje ⚙️ junto a **About** y agrega estos tags clave:
- `antigravity`
- `google-antigravity`
- `ai-skills`
- `gemini`
- `developer-tools`
- `productivity`
- `python`
- `cli`
- `prompt-engineering`
- `ai-agent`

### B. Activar GitHub Discussions
En **Settings > General > Features**, activa la casilla **Discussions** para que la comunidad pueda compartir sus propias skills personalizadas.

---

## 📣 4. Estrategia de Lanzamiento Viral (Paso a Paso)

Para que el proyecto se vuelva viral rápidamente, compártelo en los siguientes canales con estas plantillas de texto de alto impacto:

### 1. Publicación en Reddit (r/LocalLLaMA, r/MachineLearning, r/ChatGPTCoding)
**Título:**
> *[Tool] I built an open-source tool to seamlessly sync & move Google Antigravity skills across multiple computers (Zero-deps Python)*

**Cuerpo:**
> Hey everyone!  
> If you're using Google Antigravity for agentic coding, you probably know how painful it is to switch computers and realize all your custom skills, prompt runbooks, and plugins are trapped on your other machine.
> 
> I built **AntigravitySkillsMove** — a lightweight, zero-dependency CLI tool that:
> - 🔄 Auto-syncs skills bidirectionally via Git, Google Drive, Dropbox, or OneDrive.
> - 📦 Exports/imports entire skill suites into portable 1-click ZIP bundles.
> - 🛡️ Creates safety backups before any overwrite.
> - 🛠️ Quickly scaffolds compliant `SKILL.md` files in 3 seconds.
> 
> Works out of the box on Windows, macOS, and Linux.
> 
> GitHub: https://github.com/<TU_USUARIO_GITHUB>/AntigravitySkillsMove  
> Feedback and PRs are super welcome! ⭐

---

### 2. Publicación en X (Twitter / LinkedIn)
> 🚀 Tired of losing your custom Google Antigravity skills when switching computers?
> 
> Introducing **AntigravitySkillsMove** — the ultimate cross-platform utility to export, import, and auto-sync custom skills across your laptop, desktop & work PCs with 1 command.
> 
> ⚡ Zero dependencies  
> 🔄 Bidirectional Git/Cloud sync  
> 📦 1-click portable bundles  
> 
> ⭐ Star on GitHub: https://github.com/<TU_USUARIO_GITHUB>/AntigravitySkillsMove  
> #GoogleAntigravity #AI #AgenticCoding #Python #OpenSource

---

### 3. Publicación en Hacker News (Show HN)
**Título:**
> *Show HN: AntigravitySkillsMove – Sync and transport Google Antigravity skills across machines*

---

## 🚀 5. Publicar en PyPI (Opcional para que cualquiera use `pip install`)

Si deseas que cualquier persona pueda instalarlo con `pip install antigravity-skills-move`:

```powershell
pip install build twine
python -m build
twine upload dist/*
```
