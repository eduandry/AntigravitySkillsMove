#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI & Interactive Interface for AntigravitySkillsMove
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, Set

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
    audit_skills,
    install_from_url_or_git,
)


BANNER = r"""
   _____          __  .__                               .__  __         
  /  _  \   _____/  |_|__| _______________ ___  ________/  |/  |_ ___.__.
 /  /_\  \ /    \   __\  |/ ___\_  __ \__  \\  \/ /\__  <   __\   __<   |  |
/    |    \   |  \  | |  / /_/  >  | \// __ \\   /  / __ \|  |  |  |  \___  |
\____|__  /___|  /__| |__\___  /|__|  (____  /\_/  (____  /__|  |__|  / ____|
        \/     \/       /_____/            \/           \/            \/     
                🚀 SKILLS MOVE & SYNC MANAGER (v1.1.0)
"""


def print_banner():
    print(colorize(BANNER, Colors.BOLD + Colors.OKCYAN))
    print(colorize("  Seamlessly transport, sync, audit, and organize skills across computers\n", Colors.OKBLUE))


def display_installed():
    """Muestra un listado formateado de las skills, plugins y reglas instaladas."""
    skills, plugins, rules = list_installed_items()
    base = get_antigravity_config_dir()

    print("\n" + "=" * 80)
    print(colorize(" 📦 ESTADO DEL ENTORNO ANTIGRAVITY", Colors.BOLD + Colors.OKCYAN))
    print(f" Ubicación: {base}")
    print("=" * 80)

    print(colorize(f"\n⚡ SKILLS INSTALADAS ({len(skills)}):", Colors.BOLD + Colors.OKGREEN))
    if not skills:
        print("  (No hay skills instaladas en ~/.gemini/config/skills)")
    else:
        for idx, s in enumerate(skills, 1):
            desc = (s['description'][:75] + '...') if len(s['description']) > 75 else s['description']
            print(f"  {idx:2d}. {colorize(s['folder'], Colors.BOLD)}: {desc}")

    print(colorize(f"\n🔌 PLUGINS INSTALADOS ({len(plugins)}):", Colors.BOLD + Colors.OKBLUE))
    if not plugins:
        print("  (No hay plugins instalados en ~/.gemini/config/plugins)")
    else:
        for idx, p in enumerate(plugins, 1):
            skills_info = f"({p['skills_count']} sub-skills)" if p['skills_count'] > 0 else ""
            desc = (p['description'][:65] + '...') if len(p['description']) > 65 else p['description']
            print(f"  {idx:2d}. {colorize(p['folder'], Colors.BOLD)} {skills_info}: {desc}")

    if rules:
        print(colorize(f"\n📋 REGLAS GLOBALES ({len(rules)}):", Colors.BOLD + Colors.WARNING))
        for idx, r in enumerate(rules, 1):
            print(f"  {idx:2d}. {r['name']}")
    print("\n" + "=" * 80)


def run_doctor():
    """Ejecuta un diagnóstico exhaustivo de salud y seguridad de todas las skills."""
    print(colorize("\n🩺 Ejecutando Antigravity Doctor (Chequeo de Salud y Seguridad)...", Colors.BOLD + Colors.OKCYAN))
    report = audit_skills()
    if not report:
        print("No hay skills para auditar.")
        return

    healthy_count = sum(1 for r in report if r["status"] == "HEALTHY")
    warning_count = sum(1 for r in report if r["status"] == "WARNING")
    error_count = sum(1 for r in report if r["status"] == "ERROR")

    print("\n" + "=" * 80)
    print(f" RESULTADOS DE LA AUDITORÍA ({len(report)} Skills Analizadas)")
    print("=" * 80)

    for item in report:
        if item["status"] == "HEALTHY":
            icon = colorize("✅ OK", Colors.OKGREEN)
        elif item["status"] == "WARNING":
            icon = colorize("⚠️ AVISO", Colors.WARNING)
        else:
            icon = colorize("❌ ERROR", Colors.FAIL)

        extra = []
        if item["has_scripts"]:
            extra.append("scripts/")
        if item["has_refs"]:
            extra.append("references/")
        tags = f" [{', '.join(extra)}]" if extra else ""

        print(f" {icon} {colorize(item['name'], Colors.BOLD)}{tags}")
        if item["issues"]:
            for iss in item["issues"]:
                print(f"     ↳ {iss}")

    print("=" * 80)
    print(colorize(f"📊 Resumen: {healthy_count} Saludables, {warning_count} con Advertencias, {error_count} con Errores", Colors.BOLD))
    print("=" * 80)


def interactive_menu():
    """Menú interactivo completo por consola."""
    print_banner()
    while True:
        print("\n" + "=" * 80)
        print(colorize(" 🛰️  MENÚ PRINCIPAL - AntigravitySkillsMove", Colors.BOLD + Colors.HEADER))
        print("=" * 80)
        print("  1. 📋 Listar Skills, Plugins y Reglas instaladas")
        print("  2. 📦 Exportar todo (Skills, Reglas, Plugins, MCP) a paquete ZIP portable")
        print("  3. 🎯 Exportación Selectiva (Elegir qué skills empaquetar)")
        print("  4. 🚀 Importar / Instalar desde archivo ZIP")
        print("  5. 🌐 Descargar e Instalar Paquete o Skill desde URL o GitHub Repo")
        print("  6. 🔄 Auto-Sincronizar con Carpeta Compartida / Drive / Git")
        print("  7. 🩺 Diagnóstico de Salud y Seguridad (Doctor / Linter)")
        print("  8. ➕ Crear / Generar nueva Skill con plantilla oficial")
        print("  9. 📂 Abrir carpeta de Configuración en el Explorador de Archivos")
        print("  0. ❌ Salir")
        print("=" * 80)

        choice = input(colorize("👉 Selecciona una opción (0-9): ", Colors.BOLD)).strip()

        if choice == "1":
            display_installed()
        elif choice == "2":
            out_name = input("Ruta o nombre del archivo ZIP destino (Enter para automático): ").strip()
            out_file = export_bundle(output_path=out_name if out_name else None)
            size_mb = out_file.stat().st_size / (1024 * 1024)
            print(colorize(f"\n✅ Paquete creado exitosamente en: {out_file.resolve()} ({size_mb:.2f} MB)", Colors.BOLD + Colors.OKGREEN))
        elif choice == "3":
            skills, _, _ = list_installed_items()
            if not skills:
                print("No hay skills instaladas.")
                continue
            print("\nSelecciona las skills a exportar:")
            for idx, s in enumerate(skills, 1):
                print(f"  {idx:2d}. {s['folder']}")
            selected_str = input("\nIngresa los números separados por coma (ej: 1, 3, 5): ").strip()
            try:
                indexes = [int(x.strip()) for x in selected_str.split(",") if x.strip()]
                chosen = {skills[i - 1]["folder"] for i in indexes if 1 <= i <= len(skills)}
                if chosen:
                    out_file = export_bundle(selected_skills=chosen)
                    size_mb = out_file.stat().st_size / (1024 * 1024)
                    print(colorize(f"\n✅ Paquete selectivo ({len(chosen)} skills) creado en: {out_file.resolve()} ({size_mb:.2f} MB)", Colors.BOLD + Colors.OKGREEN))
                else:
                    print("❌ No se seleccionó ninguna skill válida.")
            except Exception as e:
                print(colorize(f"❌ Selección inválida: {e}", Colors.FAIL))
        elif choice == "4":
            zip_in = input("Ingresa la ruta del archivo ZIP a importar: ").strip().strip('"').strip("'")
            if zip_in:
                try:
                    import_bundle(zip_in)
                    print(colorize("\n🎉 ¡Instalación completada exitosamente!", Colors.BOLD + Colors.OKGREEN))
                    display_installed()
                except Exception as e:
                    print(colorize(f"❌ Error durante la importación: {e}", Colors.FAIL))
            else:
                print("❌ Ruta vacía.")
        elif choice == "5":
            url_in = input("Ingresa la URL del repositorio GitHub o archivo ZIP: ").strip().strip('"').strip("'")
            if url_in:
                try:
                    res_dir = install_from_url_or_git(url_in)
                    print(colorize(f"\n✅ ¡Instalación completada exitosamente desde {url_in}!", Colors.BOLD + Colors.OKGREEN))
                    display_installed()
                except Exception as e:
                    print(colorize(f"❌ Error al descargar o instalar: {e}", Colors.FAIL))
            else:
                print("❌ URL vacía.")
        elif choice == "6":
            sync_path = input("Ingresa la ruta de la carpeta compartida o repositorio Git: ").strip().strip('"').strip("'")
            if sync_path:
                print("\nModos de sincronización:")
                print("  1. Bidireccional (Recomendado: actualiza ambos lados)")
                print("  2. Descargar (Pull: solo trae novedades a este equipo)")
                print("  3. Subir (Push: solo envía novedades de este equipo)")
                sm = input("Selecciona modo (1/2/3) [1]: ").strip()
                mode_map = {"1": "both", "2": "pull", "3": "push"}
                stats = sync_with_folder(sync_path, mode=mode_map.get(sm, "both"))
                print(colorize(f"\n✨ Sincronización finalizada! Descargadas: {stats['downloaded']}, Subidas: {stats['uploaded']}", Colors.BOLD + Colors.OKGREEN))
            else:
                print("❌ Ruta vacía.")
        elif choice == "7":
            run_doctor()
        elif choice == "8":
            name = input("Nombre de la nueva Skill (ej: Analizador Logs AWS): ").strip()
            if name:
                desc = input("Descripción (cuándo y por qué debe usarla Antigravity): ").strip()
                s_dir = create_new_skill(name, desc if desc else f"Skill para {name}")
                print(colorize(f"\n✅ Skill generada exitosamente en: {s_dir}", Colors.BOLD + Colors.OKGREEN))
            else:
                print("❌ El nombre no puede estar vacío.")
        elif choice == "9":
            base = ensure_antigravity_dirs()
            skills_p = base / "skills"
            print(f"Abriendo: {skills_p}")
            if sys.platform == "win32":
                os.startfile(str(skills_p))
            elif sys.platform == "darwin":
                os.system(f"open '{skills_p}'")
            else:
                os.system(f"xdg-open '{skills_p}'")
        elif choice == "0":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print(colorize("❌ Opción inválida. Intenta nuevamente.", Colors.FAIL))


def main():
    parser = argparse.ArgumentParser(
        prog="antigravity-skills-move",
        description="AntigravitySkillsMove - Transport, sync, audit, and manage skills for Google Antigravity"
    )
    parser.add_argument("--list", action="store_true", help="List all installed skills, plugins, and rules")
    parser.add_argument("--doctor", action="store_true", help="Run health check, validation and credential scan on all skills")
    parser.add_argument("--export", metavar="OUTPUT_ZIP", nargs="?", const="", help="Export all skills to a portable ZIP bundle")
    parser.add_argument("--import-zip", metavar="ZIP_PATH", help="Import and install skills from a ZIP bundle")
    parser.add_argument("--install-remote", metavar="URL", help="Download and install a skill directly from a GitHub URL or ZIP")
    parser.add_argument("--sync-folder", metavar="FOLDER_PATH", help="Sync skills with a cloud folder or Git repo")
    parser.add_argument("--sync-mode", choices=["both", "pull", "push"], default="both", help="Sync direction (both, pull, push)")
    parser.add_argument("--add-skill", metavar="NAME", help="Create a new skill scaffold with given name")
    parser.add_argument("--description", help="Description for the new skill (used with --add-skill)")
    parser.add_argument("--version", action="version", version="AntigravitySkillsMove 1.1.0")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        interactive_menu()
    else:
        if args.list:
            display_installed()
        elif args.doctor:
            run_doctor()
        elif args.export is not None:
            out_file = export_bundle(output_path=args.export if args.export else None)
            size_mb = out_file.stat().st_size / (1024 * 1024)
            print(colorize(f"✅ Bundle exported to: {out_file.resolve()} ({size_mb:.2f} MB)", Colors.BOLD + Colors.OKGREEN))
        elif args.import_zip:
            import_bundle(args.import_zip)
            print(colorize(f"✅ Skills bundle imported from: {args.import_zip}", Colors.BOLD + Colors.OKGREEN))
            display_installed()
        elif args.install_remote:
            res_dir = install_from_url_or_git(args.install_remote)
            print(colorize(f"✅ Skill successfully installed in: {res_dir}", Colors.BOLD + Colors.OKGREEN))
        elif args.sync_folder:
            stats = sync_with_folder(args.sync_folder, mode=args.sync_mode)
            print(colorize(f"✅ Sync complete! Downloaded: {stats['downloaded']}, Uploaded: {stats['uploaded']}", Colors.BOLD + Colors.OKGREEN))
        elif args.add_skill:
            desc = args.description or f"Skill for {args.add_skill}"
            s_dir = create_new_skill(args.add_skill, desc)
            print(colorize(f"✅ Created skill at: {s_dir}", Colors.BOLD + Colors.OKGREEN))


if __name__ == "__main__":
    main()
