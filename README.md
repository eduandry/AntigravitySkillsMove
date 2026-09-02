<div align="center">

# 🚀 AntigravitySkillsMove

### The Ultimate Cross-Platform Skill Transporter, Cloud Sync & Manager for Google Antigravity

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=for-the-badge)]()
[![Google Antigravity](https://img.shields.io/badge/Google%20Antigravity-Compatible-green.svg?style=for-the-badge&logo=google)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](https://github.com/eduandry/AntigravitySkillsMove/pulls)

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

**Never lose or manually re-create your Antigravity skills again.**  
Export, transport, scaffold, and seamlessly keep your custom Skills, Plugins, and Rules synchronized across your laptop, desktop, and work workstations with **a single command**.

</div>

---

## 💡 Why AntigravitySkillsMove?

**Google Antigravity** is one of the most powerful agentic coding environments, but its custom skills and configurations are stored locally on each computer (`~/.gemini/config/skills`).

When you switch between computers (e.g. Work PC ⇄ Home Laptop), your custom runbooks, prompt optimizations, and plugins are left behind.

**AntigravitySkillsMove solves this instantly:**
- 🔄 **Effortless Cloud / Git Sync**: Connect to a Git repo, Google Drive, Dropbox, or OneDrive. Your skills update in both directions automatically.
- 📦 **1-Click Portable Bundles**: Package 50+ skills and plugins into a single, clean `.zip` to carry on a USB drive or email.
- ⚡ **Zero Dependencies**: Pure standard Python (works out-of-the-box on Windows, macOS, and Linux).
- 🛡️ **Safe by Default**: Automatically creates timestamped backups before applying any updates.
- 🛠️ **Built-in Skill Scaffolder**: Generate compliant `SKILL.md` files with correct YAML frontmatter and folder architecture in seconds.

---

## ⚡ 1-Line Instant Run (No Clone Needed!)

Run this command directly in your terminal on ANY computer to immediately launch AntigravitySkillsMove:

#### 🪟 Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/install.ps1 | iex
```

#### 🍎 macOS / 🐧 Linux (Bash):
```bash
curl -sSL https://raw.githubusercontent.com/eduandry/AntigravitySkillsMove/main/install.sh | bash
```

---

## ⚡ Quickstart (Clone or PIP)

### Option A: Clone the Repository
```bash
git clone https://github.com/eduandry/AntigravitySkillsMove.git
cd AntigravitySkillsMove
python antigravity_skills_move.py
```

> **Windows Users**: You can also simply double-click [`sync_skills.bat`](sync_skills.bat).

### Option B: Install via PIP (Global CLI)
```bash
pip install .
antigravity-skills-move --list
```

---

## 🎮 Features & Usage

### 🩺 1. Health Audit & Security Doctor (`--doctor`)
Audit all installed skills for Antigravity compliance (valid YAML frontmatter, optimal description length, executable scripts, and **automatic credential / API key scanning**):

```bash
python antigravity_skills_move.py --doctor
```

---

### 🌐 2. Install Skills Directly from GitHub / URLs (`--install-remote`)
Install any standalone skill or repo package from GitHub or direct ZIP with 1 command:

```bash
python antigravity_skills_move.py --install-remote "https://github.com/user/custom-antigravity-skill"
```

---

### 📋 3. List All Installed Skills & Plugins
Inspect what skills, sub-skills, and rules are currently active in your Antigravity environment:

```bash
python antigravity_skills_move.py --list
```


---

### 📦 2. Export / Pack Skills into a Portable Bundle
Export your entire skill library into a clean `.zip` file:

```bash
# Exports to auto-named antigravity_skills_bundle_<timestamp>.zip
python antigravity_skills_move.py --export

# Or specify a custom output path
python antigravity_skills_move.py --export "D:\Backups\my_antigravity_skills.zip"
```

---

### 🚀 3. Import & Install on a New Computer
Take your `.zip` bundle to your other PC and install everything in 1 step:

```bash
python antigravity_skills_move.py --import-zip "my_antigravity_skills.zip"
```
*AntigravitySkillsMove automatically locates `~/.gemini/config/skills` and installs all skills safely.*

---

### 🔄 4. Bidirectional Auto-Sync (Cloud / Git)
Keep your work PC and home laptop in continuous harmony using a shared folder (Dropbox, Google Drive, OneDrive, or a Git repo):

```bash
# Bidirectional sync (downloads new skills & uploads local changes)
python antigravity_skills_move.py --sync-folder "D:\CloudDrive\AntigravitySkills" --sync-mode both

# Download only (Pull)
python antigravity_skills_move.py --sync-folder "D:\CloudDrive\AntigravitySkills" --sync-mode pull

# Upload only (Push)
python antigravity_skills_move.py --sync-folder "D:\CloudDrive\AntigravitySkills" --sync-mode push
```

> 💡 **Git Superpower**: If your sync folder is a Git repository, AntigravitySkillsMove automatically executes `git pull`, `git add`, `git commit`, and `git push` for you!

---

### ➕ 5. Scaffold a New Custom Skill
Create a production-ready skill scaffold compliant with Antigravity specifications:

```bash
python antigravity_skills_move.py --add-skill "Postgres Query Tuner" --description "Use this skill when optimizing slow SQL queries and EXPLAIN ANALYZE reports."
```

Generated structure:
```text
skills/postgres-query-tuner/
├── SKILL.md          # YAML frontmatter + prompt guidelines
├── scripts/          # Executable helper scripts
├── references/       # In-depth documentation & manuals
└── examples/         # Reference implementations
```

---

## 🖥️ Interactive Console Menu

Prefer a visual experience? Just run without flags:

```text
================================================================================
 🛰️  MAIN MENU - AntigravitySkillsMove
================================================================================
  1. 📋 List installed Skills & Plugins
  2. 📦 Export / Pack all Skills to a portable ZIP bundle
  3. 🚀 Import / Install Skills from a ZIP bundle
  4. 🔄 Auto-Sync with Shared Folder / Cloud Drive / Git
  5. ➕ Create / Scaffold a new custom Skill
  6. 📂 Open Antigravity Skills folder in File Explorer
  0. ❌ Exit
================================================================================
👉 Select an option (0-6):
```

---

## 🗺️ Where Antigravity Saves Skills

| Scope | OS | Absolute Path |
| :--- | :--- | :--- |
| **Global Skills** | **Windows** | `C:\Users\<User>\.gemini\config\skills\` |
| **Global Plugins** | **Windows** | `C:\Users\<User>\.gemini\config\plugins\` |
| **Global Rules** | **Windows** | `C:\Users\<User>\.gemini\config\rules\` |
| **Global All** | **macOS / Linux** | `~/.gemini/config/skills/` and `~/.gemini/config/plugins/` |
| **Workspace** | **All Platforms** | `<ProjectRoot>/.agents/skills/<skill-name>/` |

---

## 🤝 Contributing

Contributions are welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

<div align="center">
Made with ❤️ for the <strong>Google Antigravity & AI Developer Community</strong>.
</div>
