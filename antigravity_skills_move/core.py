#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core Engine for AntigravitySkillsMove
Handles discovery, packaging, unbundling, remote installation, health audits,
credential scanning, selective synchronization, and scaffolding.
"""

import os
import sys
import shutil
import zipfile
import json
import re
import urllib.request
import tempfile
import datetime
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colorize(text: str, color: str) -> str:
    """Wraps text in ANSI color codes if terminal supports them."""
    return f"{color}{text}{Colors.ENDC}"


def get_antigravity_config_dir() -> Path:
    """Returns the absolute path to Antigravity's global config directory (~/.gemini/config)."""
    return Path.home() / ".gemini" / "config"


def ensure_antigravity_dirs() -> Path:
    """Ensures that all standard Antigravity configuration subdirectories exist."""
    base = get_antigravity_config_dir()
    for sub in ["skills", "plugins", "rules", "global_workflows"]:
        (base / sub).mkdir(parents=True, exist_ok=True)
    return base


def parse_skill_md(skill_md_path: Path) -> Dict[str, str]:
    """Parses frontmatter metadata (name and description) from a SKILL.md file."""
    info = {"name": skill_md_path.parent.name, "description": "No description provided."}
    if not skill_md_path.exists():
        return info

    try:
        content = skill_md_path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        in_yaml = False
        yaml_lines = []
        for line in lines:
            if line.strip() == "---":
                if not in_yaml:
                    in_yaml = True
                    continue
                else:
                    break
            if in_yaml:
                yaml_lines.append(line)

        desc_collecting = False
        desc_lines = []
        for yline in yaml_lines:
            if yline.startswith("name:"):
                info["name"] = yline.split("name:", 1)[1].strip().strip('"').strip("'")
                desc_collecting = False
            elif yline.startswith("description:"):
                val = yline.split("description:", 1)[1].strip()
                if val.startswith(">-") or val.startswith(">") or val.startswith("|") or not val:
                    desc_collecting = True
                else:
                    info["description"] = val.strip('"').strip("'")
                    desc_collecting = False
            elif desc_collecting:
                if yline.startswith("  ") or yline.startswith("\t"):
                    desc_lines.append(yline.strip().strip('"').strip("'"))
                else:
                    desc_collecting = False
        if desc_lines:
            info["description"] = " ".join(desc_lines)
    except Exception as e:
        info["description"] = f"Error reading SKILL.md: {e}"
    return info


def list_installed_items() -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """Returns lists of installed skills, plugins, and rules."""
    base = get_antigravity_config_dir()
    skills_dir = base / "skills"
    plugins_dir = base / "plugins"
    rules_dir = base / "rules"

    skills = []
    if skills_dir.exists():
        for item in sorted(skills_dir.iterdir()):
            if item.is_dir():
                skill_md = item / "SKILL.md"
                info = parse_skill_md(skill_md)
                info["folder"] = item.name
                info["path"] = str(item)
                info["has_skill_md"] = skill_md.exists()
                skills.append(info)

    plugins = []
    if plugins_dir.exists():
        for item in sorted(plugins_dir.iterdir()):
            if item.is_dir():
                plugin_json = item / "plugin.json"
                p_name = item.name
                p_desc = "No plugin metadata"
                if plugin_json.exists():
                    try:
                        p_data = json.loads(plugin_json.read_text(encoding="utf-8", errors="replace"))
                        p_name = p_data.get("name", p_name)
                        p_desc = p_data.get("description", p_desc)
                    except Exception:
                        pass
                
                plugin_skills = []
                p_skills_dir = item / "skills"
                if p_skills_dir.exists():
                    for ps in p_skills_dir.iterdir():
                        if ps.is_dir():
                            plugin_skills.append(ps.name)

                plugins.append({
                    "name": p_name,
                    "folder": item.name,
                    "description": p_desc,
                    "skills_count": len(plugin_skills),
                    "skills": plugin_skills,
                    "path": str(item)
                })

    rules = []
    if rules_dir.exists():
        for item in sorted(rules_dir.iterdir()):
            if item.is_file() and item.suffix == ".md":
                rules.append({"name": item.name, "path": str(item)})

    return skills, plugins, rules


# Patrones de detección de credenciales y secretos accidentales
SECRET_PATTERNS = [
    (re.compile(r"sk-[a-zA-Z0-9]{32,}", re.IGNORECASE), "OpenAI API Key"),
    (re.compile(r"AIzaSy[a-zA-Z0-9_-]{33}", re.IGNORECASE), "Google Cloud / Gemini API Key"),
    (re.compile(r"ghp_[a-zA-Z0-9]{36}", re.IGNORECASE), "GitHub Personal Access Token"),
    (re.compile(r"gho_[a-zA-Z0-9]{36}", re.IGNORECASE), "GitHub OAuth Token"),
    (re.compile(r"xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,32}", re.IGNORECASE), "Slack Token"),
    (re.compile(r"BEGIN\s+(RSA|OPENSSH|EC|DSA)?\s*PRIVATE KEY", re.IGNORECASE), "Private Key"),
]


def scan_for_secrets(directory: Path) -> List[Dict[str, str]]:
    """Escanea una carpeta en busca de posibles API Keys o credenciales expuestas."""
    findings = []
    for root, _, files in os.walk(directory):
        for f in files:
            file_p = Path(root) / f
            # Ignorar binarios grandes o extensiones pesadas
            if file_p.suffix.lower() in [".png", ".jpg", ".jpeg", ".zip", ".exe", ".pdf", ".pyc"]:
                continue
            try:
                text = file_p.read_text(encoding="utf-8", errors="ignore")
                for pattern, secret_type in SECRET_PATTERNS:
                    if pattern.search(text):
                        findings.append({
                            "file": str(file_p.relative_to(directory)),
                            "type": secret_type
                        })
            except Exception:
                pass
    return findings


def audit_skills() -> List[Dict]:
    """Realiza un chequeo de salud / diagnóstico ('doctor') de todas las skills instaladas."""
    skills, _, _ = list_installed_items()
    report = []
    
    for s in skills:
        p = Path(s["path"])
        skill_md = p / "SKILL.md"
        issues = []
        
        # 1. Existencia de SKILL.md
        if not skill_md.exists():
            issues.append("Falta archivo principal SKILL.md")
        else:
            desc = s.get("description", "")
            if len(desc) < 25:
                issues.append("Descripción YAML demasiado corta (dificulta que Antigravity sepa cuándo activarla)")
            if not s.get("name"):
                issues.append("Falta campo 'name' en YAML frontmatter")

        # 2. Escaneo de secretos
        secrets = scan_for_secrets(p)
        if secrets:
            for sec in secrets:
                issues.append(f"Posible credencial expuesta ({sec['type']}) en: {sec['file']}")

        # 3. Subcarpetas
        has_scripts = (p / "scripts").exists()
        has_refs = (p / "references").exists()

        status = "HEALTHY" if not issues else ("WARNING" if len(issues) == 1 and "corta" in issues[0] else "ERROR")
        report.append({
            "name": s["folder"],
            "status": status,
            "issues": issues,
            "has_scripts": has_scripts,
            "has_refs": has_refs
        })
    return report


def export_bundle(
    output_path: Optional[str] = None,
    export_mcp: bool = True,
    selected_skills: Optional[Set[str]] = None,
    sanitize_secrets: bool = True
) -> Path:
    """
    Empaqueta todas o una selección de skills, plugins y reglas en un archivo ZIP portable.
    """
    base = get_antigravity_config_dir()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if not output_path:
        output_file = Path.cwd() / f"antigravity_skills_bundle_{timestamp}.zip"
    else:
        output_file = Path(output_path)
        if output_file.is_dir():
            output_file = output_file / f"antigravity_skills_bundle_{timestamp}.zip"

    ensure_antigravity_dirs()
    skills_dir = base / "skills"
    plugins_dir = base / "plugins"
    rules_dir = base / "rules"
    workflows_dir = base / "global_workflows"

    manifest = {
        "generator": "AntigravitySkillsMove",
        "version": "1.1.0",
        "created_at": datetime.datetime.now().isoformat(),
        "source_platform": sys.platform,
        "included": []
    }

    count_skills = 0
    count_plugins = 0
    count_rules = 0

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if skills_dir.exists():
            for item in skills_dir.iterdir():
                if item.is_dir():
                    if selected_skills is not None and item.name not in selected_skills:
                        continue
                    
                    # Chequeo preventivo de secretos si está activado
                    if sanitize_secrets:
                        secs = scan_for_secrets(item)
                        if secs:
                            print(colorize(f"⚠️ Advertencia de seguridad: Se detectaron credenciales en la skill '{item.name}'", Colors.WARNING))

                    for root, _, files in os.walk(item):
                        for f in files:
                            full_p = Path(root) / f
                            rel_p = full_p.relative_to(base)
                            zipf.write(full_p, arcname=str(rel_p))
                    count_skills += 1
            manifest["included"].append(f"skills ({count_skills})")

        # Plugins (siempre incluidos o exportados completos)
        if plugins_dir.exists() and (selected_skills is None):
            for root, _, files in os.walk(plugins_dir):
                for f in files:
                    full_p = Path(root) / f
                    rel_p = full_p.relative_to(base)
                    zipf.write(full_p, arcname=str(rel_p))
            count_plugins = len([d for d in plugins_dir.iterdir() if d.is_dir()])
            manifest["included"].append(f"plugins ({count_plugins})")

        if rules_dir.exists() and (selected_skills is None):
            for root, _, files in os.walk(rules_dir):
                for f in files:
                    full_p = Path(root) / f
                    rel_p = full_p.relative_to(base)
                    zipf.write(full_p, arcname=str(rel_p))
            count_rules = len([d for d in rules_dir.iterdir() if d.is_file()])
            manifest["included"].append(f"rules ({count_rules})")

        if workflows_dir.exists() and (selected_skills is None):
            for root, _, files in os.walk(workflows_dir):
                for f in files:
                    full_p = Path(root) / f
                    rel_p = full_p.relative_to(base)
                    zipf.write(full_p, arcname=str(rel_p))

        mcp_file = base / "mcp_config.json"
        if export_mcp and mcp_file.exists():
            zipf.write(mcp_file, arcname="mcp_config.json")
            manifest["included"].append("mcp_config.json")

        zipf.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))

    return output_file


def import_bundle(
    zip_path: str,
    overwrite: bool = True,
    backup_first: bool = True,
    selected_items: Optional[Set[str]] = None
) -> bool:
    """Importa e instala un paquete ZIP de skills en el directorio global de Antigravity."""
    zip_file = Path(zip_path)
    if not zip_file.exists():
        raise FileNotFoundError(f"Archivo de paquete '{zip_path}' no encontrado.")

    base = ensure_antigravity_dirs()

    if backup_first:
        backup_dir = base.parent / "config_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"backup_before_import_{ts}.zip"
        export_bundle(output_path=str(backup_file), sanitize_secrets=False)

    with zipfile.ZipFile(zip_file, 'r') as zipf:
        file_list = zipf.namelist()
        for member in file_list:
            if member == "manifest.json":
                continue

            # Filtro selectivo si se especificó
            if selected_items is not None:
                parts = member.split("/")
                if len(parts) >= 2 and parts[1] not in selected_items:
                    continue

            target_path = (base / member).resolve()
            if not str(target_path).startswith(str(base.resolve())):
                continue

            if member.endswith("/"):
                target_path.mkdir(parents=True, exist_ok=True)
                continue

            target_path.parent.mkdir(parents=True, exist_ok=True)

            if target_path.exists() and not overwrite:
                continue

            with zipf.open(member) as source, open(target_path, "wb") as target:
                shutil.copyfileobj(source, target)

    return True


def install_from_url_or_git(remote_url: str) -> Path:
    """
    Descarga e instala una skill directamente desde un repositorio GitHub o URL de archivo ZIP.
    Ejemplos:
      - https://github.com/usuario/mi-skill
      - https://github.com/usuario/mi-skill.git
      - https://ejemplo.com/skills/mi-skill.zip
    """
    base = ensure_antigravity_dirs() / "skills"
    url = remote_url.strip()

    print(f"\n🌐 Descargando skill desde: {url}")
    
    # Caso 1: Archivo ZIP directo
    if url.endswith(".zip"):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_zip = Path(tmpdir) / "downloaded_skill.zip"
            urllib.request.urlretrieve(url, tmp_zip)
            import_bundle(str(tmp_zip), backup_first=True)
            return base

    # Caso 2: Repositorio Git / GitHub
    skill_name = url.rstrip("/").split("/")[-1].replace(".git", "").lower()
    target_skill_dir = base / skill_name

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dest = Path(tmpdir) / "cloned_repo"
        try:
            subprocess.run(["git", "clone", "--depth", "1", url, str(clone_dest)], check=True, capture_output=True, text=True)
        except Exception as e:
            raise RuntimeError(f"Error al clonar repositorio: {e}")

        # Comprobar si el repo es una skill en sí (tiene SKILL.md) o contiene carpeta skills/
        if (clone_dest / "SKILL.md").exists():
            if target_skill_dir.exists():
                shutil.rmtree(target_skill_dir)
            shutil.copytree(clone_dest, target_skill_dir, ignore=shutil.ignore_patterns(".git", ".github"))
            return target_skill_dir
        elif (clone_dest / "skills").exists():
            for sk in (clone_dest / "skills").iterdir():
                if sk.is_dir():
                    dst = base / sk.name
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(sk, dst)
            return base
        else:
            # Instalar la carpeta completa y crear scaffolding si falta
            if target_skill_dir.exists():
                shutil.rmtree(target_skill_dir)
            shutil.copytree(clone_dest, target_skill_dir, ignore=shutil.ignore_patterns(".git", ".github"))
            if not (target_skill_dir / "SKILL.md").exists():
                create_new_skill(skill_name, f"Skill importada desde {url}", target_dir=base)
            return target_skill_dir


def create_new_skill(skill_name: str, skill_description: str, target_dir: Optional[Path] = None) -> Path:
    """Crea una nueva skill con estructura estándar SKILL.md y subcarpetas."""
    base = target_dir if target_dir else (ensure_antigravity_dirs() / "skills")
    skill_slug = skill_name.strip().lower().replace(" ", "-").replace("_", "-")
    skill_dir = base / skill_slug

    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "examples").mkdir(exist_ok=True)

    skill_md_content = f"""---
name: {skill_slug}
description: >-
  {skill_description.strip()}
---

# {skill_name}

{skill_description.strip()}

## Cuándo Activar esta Skill
Describe detalladamente los términos, disparadores y escenarios en los que Antigravity debe usar esta skill.

## Procedimiento Paso a Paso
1. **Paso 1**: Describir la preparación inicial o ejecución de scripts auxiliares.
2. **Paso 2**: Describir el flujo de trabajo o comando principal.
3. **Paso 3**: Validar los resultados y entregar el informe en formato Markdown (.md).

## Recursos y Herramientas
- Scripts ejecutables: `./scripts/`
- Manuales y referencias: `./references/`
- Ejemplos de uso: `./examples/`
"""
    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_md_content, encoding="utf-8")
    return skill_dir


def sync_with_folder(sync_folder_path: str, mode: str = "both", auto_git: bool = True) -> Dict[str, int]:
    """Sincroniza skills con un directorio local, carpeta de nube o repositorio Git."""
    sync_folder = Path(sync_folder_path).resolve()
    base = ensure_antigravity_dirs()

    sync_skills = sync_folder / "skills"
    sync_plugins = sync_folder / "plugins"
    sync_rules = sync_folder / "rules"
    sync_workflows = sync_folder / "global_workflows"

    sync_skills.mkdir(parents=True, exist_ok=True)
    sync_plugins.mkdir(parents=True, exist_ok=True)
    sync_rules.mkdir(parents=True, exist_ok=True)
    sync_workflows.mkdir(parents=True, exist_ok=True)

    stats = {"downloaded": 0, "uploaded": 0}

    is_git_repo = (sync_folder / ".git").exists()
    if is_git_repo and auto_git and mode in ["pull", "both"]:
        try:
            subprocess.run(["git", "-C", str(sync_folder), "pull"], capture_output=True, text=True, timeout=15)
        except Exception:
            pass

    def copy_sync(src: Path, dst: Path) -> int:
        count = 0
        if not src.exists():
            return count
        for item in src.iterdir():
            target = dst / item.name
            if item.is_dir():
                if not target.exists() or item.stat().st_mtime > target.stat().st_mtime:
                    shutil.copytree(item, target, dirs_exist_ok=True)
                    count += 1
            elif item.is_file():
                if not target.exists() or item.stat().st_mtime > target.stat().st_mtime:
                    shutil.copy2(item, target)
                    count += 1
        return count

    def copy_file_if_newer(src_file: Path, dst_file: Path) -> int:
        if src_file.exists():
            if not dst_file.exists() or src_file.stat().st_mtime > dst_file.stat().st_mtime:
                shutil.copy2(src_file, dst_file)
                return 1
        return 0

    # 1. Pull (Desde carpeta compartida / Git -> Antigravity Local)
    if mode in ["pull", "both"]:
        stats["downloaded"] += copy_sync(sync_skills, base / "skills")
        stats["downloaded"] += copy_sync(sync_plugins, base / "plugins")
        stats["downloaded"] += copy_sync(sync_rules, base / "rules")
        stats["downloaded"] += copy_sync(sync_workflows, base / "global_workflows")
        # Sincronizar MCP Config
        stats["downloaded"] += copy_file_if_newer(sync_folder / "mcp_config.json", base / "mcp_config.json")

    # 2. Push (Desde Antigravity Local -> Carpeta compartida / Git)
    if mode in ["push", "both"]:
        stats["uploaded"] += copy_sync(base / "skills", sync_skills)
        stats["uploaded"] += copy_sync(base / "plugins", sync_plugins)
        stats["uploaded"] += copy_sync(base / "rules", sync_rules)
        stats["uploaded"] += copy_sync(base / "global_workflows", sync_workflows)
        # Sincronizar MCP Config
        stats["uploaded"] += copy_file_if_newer(base / "mcp_config.json", sync_folder / "mcp_config.json")

        if is_git_repo and auto_git and stats["uploaded"] > 0:
            try:
                subprocess.run(["git", "-C", str(sync_folder), "add", "."], capture_output=True, timeout=10)
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                subprocess.run(["git", "-C", str(sync_folder), "commit", "-m", f"Auto-sync skills & MCP: {ts}"], capture_output=True, timeout=10)
                subprocess.run(["git", "-C", str(sync_folder), "push"], capture_output=True, timeout=20)
            except Exception:
                pass

    return stats

