#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI & Interactive Interface for AntigravitySkillsMove
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

from antigravity_skills_move.core import (
    Colors,
    colorize,
    get_antigravity_config_dir,
    ensure_antigravity_dirs,
    list_installed_items,
    export_bundle,
    import_bundle,
    create_new_skill,
    sync_with_folder,
)


BANNER = r"""
   _____          __  .__                               .__  __         
  /  _  \   _____/  |_|__| _______________ ___  ________/  |/  |_ ___.__.
 /  /_\  \ /    \   __\  |/ ___\_  __ \__  \\  \/ /\__  <   __\   __<   |  |
/    |    \   |  \  | |  / /_/  >  | \// __ \\   /  / __ \|  |  |  |  \___  |
\____|__  /___|  /__| |__\___  /|__|  (____  /\_/  (____  /__|  |__|  / ____|
        \/     \/       /_____/            \/           \/            \/     
                🚀 SKILLS MOVE & SYNC MANAGER (v1.0.0)
"""


def print_banner():
    print(colorize(BANNER, Colors.BOLD + Colors.OKCYAN))
    print(colorize("  Seamlessly transport, sync, and organize skills across computers\n", Colors.OKBLUE))


def display_installed():
    """Displays installed skills and plugins in a clean formatted view."""
    skills, plugins, rules = list_installed_items()
    base = get_antigravity_config_dir()

    print("\n" + "=" * 80)
    print(colorize(" 📦 ANTIGRAVITY ENVIRONMENT STATUS", Colors.BOLD + Colors.OKCYAN))
    print(f" Location: {base}")
    print("=" * 80)

    print(colorize(f"\n⚡ INSTALLED SKILLS ({len(skills)}):", Colors.BOLD + Colors.OKGREEN))
    if not skills:
        print("  (No standalone skills installed yet in ~/.gemini/config/skills)")
    else:
        for idx, s in enumerate(skills, 1):
            desc = (s['description'][:75] + '...') if len(s['description']) > 75 else s['description']
            print(f"  {idx:2d}. {colorize(s['folder'], Colors.BOLD)}: {desc}")

    print(colorize(f"\n🔌 INSTALLED PLUGINS ({len(plugins)}):", Colors.BOLD + Colors.OKBLUE))
    if not plugins:
        print("  (No plugins installed yet in ~/.gemini/config/plugins)")
    else:
        for idx, p in enumerate(plugins, 1):
            skills_info = f"({p['skills_count']} sub-skills)" if p['skills_count'] > 0 else ""
            desc = (p['description'][:65] + '...') if len(p['description']) > 65 else p['description']
            print(f"  {idx:2d}. {colorize(p['folder'], Colors.BOLD)} {skills_info}: {desc}")

    if rules:
        print(colorize(f"\n📋 GLOBAL RULES ({len(rules)}):", Colors.BOLD + Colors.WARNING))
        for idx, r in enumerate(rules, 1):
            print(f"  {idx:2d}. {r['name']}")
    print("\n" + "=" * 80)


def interactive_menu():
    """Interactive loop for console users."""
    print_banner()
    while True:
        print("\n" + "=" * 80)
        print(colorize(" 🛰️  MAIN MENU - AntigravitySkillsMove", Colors.BOLD + Colors.HEADER))
        print("=" * 80)
        print("  1. 📋 List installed Skills & Plugins")
        print("  2. 📦 Export / Pack all Skills to a portable ZIP bundle")
        print("  3. 🚀 Import / Install Skills from a ZIP bundle")
        print("  4. 🔄 Auto-Sync with Shared Folder / Cloud Drive / Git")
        print("  5. ➕ Create / Scaffold a new custom Skill")
        print("  6. 📂 Open Antigravity Skills folder in File Explorer")
        print("  0. ❌ Exit")
        print("=" * 80)

        choice = input(colorize("👉 Select an option (0-6): ", Colors.BOLD)).strip()

        if choice == "1":
            display_installed()
        elif choice == "2":
            out_name = input("Destination ZIP path (Leave blank for default timestamped name): ").strip()
            out_file = export_bundle(output_path=out_name if out_name else None)
            size_mb = out_file.stat().st_size / (1024 * 1024)
            print(colorize(f"\n✅ Bundle successfully created at: {out_file.resolve()} ({size_mb:.2f} MB)", Colors.BOLD + Colors.OKGREEN))
            print(colorize("💡 Copy this file to a USB flash drive, Google Drive, or send it to your other PC.", Colors.OKCYAN))
        elif choice == "3":
            zip_in = input("Enter the path to the ZIP bundle to import: ").strip().strip('"').strip("'")
            if zip_in:
                try:
                    import_bundle(zip_in)
                    print(colorize("\n🎉 Installation completed successfully!", Colors.BOLD + Colors.OKGREEN))
                    display_installed()
                except Exception as e:
                    print(colorize(f"❌ Error during import: {e}", Colors.FAIL))
            else:
                print("❌ Path cannot be empty.")
        elif choice == "4":
            sync_path = input("Enter path to shared folder or Git repo (e.g. D:\\Cloud\\AntigravitySkills): ").strip().strip('"').strip("'")
            if sync_path:
                print("\nSync modes:")
                print("  1. Bidirectional (Recommended: syncs changes in both directions)")
                print("  2. Pull (Only download changes from folder to this machine)")
                print("  3. Push (Only upload changes from this machine to folder)")
                sm = input("Select mode (1/2/3) [1]: ").strip()
                mode_map = {"1": "both", "2": "pull", "3": "push"}
                stats = sync_with_folder(sync_path, mode=mode_map.get(sm, "both"))
                print(colorize(f"\n✨ Sync finished! Downloaded: {stats['downloaded']} updates, Uploaded: {stats['uploaded']} updates.", Colors.BOLD + Colors.OKGREEN))
            else:
                print("❌ Path cannot be empty.")
        elif choice == "5":
            name = input("New Skill Name (e.g. Postgres Optimizer): ").strip()
            if name:
                desc = input("Skill Description (When and why should Antigravity use it): ").strip()
                s_dir = create_new_skill(name, desc if desc else f"Custom skill for {name}")
                print(colorize(f"\n✅ Skill scaffolded at: {s_dir}", Colors.BOLD + Colors.OKGREEN))
            else:
                print("❌ Name cannot be empty.")
        elif choice == "6":
            base = ensure_antigravity_dirs()
            skills_p = base / "skills"
            print(f"Opening: {skills_p}")
            if sys.platform == "win32":
                os.startfile(str(skills_p))
            elif sys.platform == "darwin":
                os.system(f"open '{skills_p}'")
            else:
                os.system(f"xdg-open '{skills_p}'")
        elif choice == "0":
            print("\n👋 Goodbye!")
            break
        else:
            print(colorize("❌ Invalid option. Please try again.", Colors.FAIL))


def main():
    parser = argparse.ArgumentParser(
        prog="antigravity-skills-move",
        description="AntigravitySkillsMove - Export, import, sync, and manage skills across machines for Google Antigravity"
    )
    parser.add_argument("--list", action="store_true", help="List all installed skills, plugins, and rules")
    parser.add_argument("--export", metavar="OUTPUT_ZIP", nargs="?", const="", help="Export all skills to a portable ZIP bundle")
    parser.add_argument("--import-zip", metavar="ZIP_PATH", help="Import and install skills from a ZIP bundle")
    parser.add_argument("--sync-folder", metavar="FOLDER_PATH", help="Sync skills with a cloud folder or Git repo")
    parser.add_argument("--sync-mode", choices=["both", "pull", "push"], default="both", help="Sync direction (both, pull, push)")
    parser.add_argument("--add-skill", metavar="NAME", help="Create a new skill scaffold with given name")
    parser.add_argument("--description", help="Description for the new skill (used with --add-skill)")
    parser.add_argument("--version", action="version", version="AntigravitySkillsMove 1.0.0")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        interactive_menu()
    else:
        if args.list:
            display_installed()
        elif args.export is not None:
            out_file = export_bundle(output_path=args.export if args.export else None)
            size_mb = out_file.stat().st_size / (1024 * 1024)
            print(colorize(f"✅ Bundle exported to: {out_file.resolve()} ({size_mb:.2f} MB)", Colors.BOLD + Colors.OKGREEN))
        elif args.import_zip:
            import_bundle(args.import_zip)
            print(colorize(f"✅ Skills bundle imported from: {args.import_zip}", Colors.BOLD + Colors.OKGREEN))
            display_installed()
        elif args.sync_folder:
            stats = sync_with_folder(args.sync_folder, mode=args.sync_mode)
            print(colorize(f"✅ Sync complete! Downloaded: {stats['downloaded']}, Uploaded: {stats['uploaded']}", Colors.BOLD + Colors.OKGREEN))
        elif args.add_skill:
            desc = args.description or f"Skill for {args.add_skill}"
            s_dir = create_new_skill(args.add_skill, desc)
            print(colorize(f"✅ Created skill at: {s_dir}", Colors.BOLD + Colors.OKGREEN))


if __name__ == "__main__":
    main()
