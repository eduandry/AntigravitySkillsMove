#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core Engine for AntigravitySkillsMove
Handles discovery, packaging, unbundling, synchronization, and scaffolding.
"""

import os
import sys
import shutil
import zipfile
import json
import datetime
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional

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


def export_bundle(output_path: Optional[str] = None, export_mcp: bool = False) -> Path:
    """Exports all skills, plugins, rules, and workflows into a standalone portable ZIP bundle."""
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
        "version": "1.0.0",
        "created_at": datetime.datetime.now().isoformat(),
        "source_platform": sys.platform,
        "included": []
    }

    count_skills = 0
    count_plugins = 0
    count_rules = 0

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if skills_dir.exists():
            for root, _, files in os.walk(skills_dir):
                for f in files:
                    full_p = Path(root) / f
                    rel_p = full_p.relative_to(base)
                    zipf.write(full_p, arcname=str(rel_p))
            count_skills = len([d for d in skills_dir.iterdir() if d.is_dir()])
            manifest["included"].append(f"skills ({count_skills})")

        if plugins_dir.exists():
            for root, _, files in os.walk(plugins_dir):
                for f in files:
                    full_p = Path(root) / f
                    rel_p = full_p.relative_to(base)
                    zipf.write(full_p, arcname=str(rel_p))
            count_plugins = len([d for d in plugins_dir.iterdir() if d.is_dir()])
            manifest["included"].append(f"plugins ({count_plugins})")

        if rules_dir.exists():
            for root, _, files in os.walk(rules_dir):
                for f in files:
                    full_p = Path(root) / f
                    rel_p = full_p.relative_to(base)
                    zipf.write(full_p, arcname=str(rel_p))
            count_rules = len([d for d in rules_dir.iterdir() if d.is_file()])
            manifest["included"].append(f"rules ({count_rules})")

        if workflows_dir.exists():
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


def import_bundle(zip_path: str, overwrite: bool = True, backup_first: bool = True) -> bool:
    """Imports and installs a skills bundle ZIP into Antigravity global config."""
    zip_file = Path(zip_path)
    if not zip_file.exists():
        raise FileNotFoundError(f"Bundle file '{zip_path}' not found.")

    base = ensure_antigravity_dirs()

    if backup_first:
        backup_dir = base.parent / "config_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"backup_before_import_{ts}.zip"
        export_bundle(output_path=str(backup_file))

    with zipfile.ZipFile(zip_file, 'r') as zipf:
        file_list = zipf.namelist()
        for member in file_list:
            if member == "manifest.json":
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


def create_new_skill(skill_name: str, skill_description: str, target_dir: Optional[Path] = None) -> Path:
    """Creates a new skill directory with standard SKILL.md and folder scaffolding."""
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

## When to Activate this Skill
Provide detailed trigger conditions explaining when Antigravity should use this skill.

## Step-by-Step Procedure
1. **Step 1**: Describe the initial preparation or prerequisite scripts.
2. **Step 2**: Describe the main execution command or workflow.
3. **Step 3**: Validate results and summarize findings.

## Resources and Tools
- Helper scripts: `./scripts/`
- Reference manuals: `./references/`
- Code examples: `./examples/`
"""
    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_md_content, encoding="utf-8")
    return skill_dir


def sync_with_folder(sync_folder_path: str, mode: str = "both", auto_git: bool = True) -> Dict[str, int]:
    """Synchronizes skills with a local directory, cloud drive, or Git repository."""
    sync_folder = Path(sync_folder_path).resolve()
    base = ensure_antigravity_dirs()

    sync_skills = sync_folder / "skills"
    sync_plugins = sync_folder / "plugins"
    sync_rules = sync_folder / "rules"

    sync_skills.mkdir(parents=True, exist_ok=True)
    sync_plugins.mkdir(parents=True, exist_ok=True)
    sync_rules.mkdir(parents=True, exist_ok=True)

    stats = {"downloaded": 0, "uploaded": 0}

    # If the folder is a git repo and auto_git is enabled, pull first
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

    if mode in ["pull", "both"]:
        stats["downloaded"] += copy_sync(sync_skills, base / "skills")
        stats["downloaded"] += copy_sync(sync_plugins, base / "plugins")
        stats["downloaded"] += copy_sync(sync_rules, base / "rules")

    if mode in ["push", "both"]:
        stats["uploaded"] += copy_sync(base / "skills", sync_skills)
        stats["uploaded"] += copy_sync(base / "plugins", sync_plugins)
        stats["uploaded"] += copy_sync(base / "rules", sync_rules)

        if is_git_repo and auto_git and stats["uploaded"] > 0:
            try:
                subprocess.run(["git", "-C", str(sync_folder), "add", "."], capture_output=True, timeout=10)
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                subprocess.run(["git", "-C", str(sync_folder), "commit", "-m", f"Auto-sync skills: {ts}"], capture_output=True, timeout=10)
                subprocess.run(["git", "-C", str(sync_folder), "push"], capture_output=True, timeout=20)
            except Exception:
                pass

    return stats
