#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AntigravitySkillsMove - Standalone Single-File Distribution
Move, sync, and manage your Google Antigravity skills across multiple computers.
"""

import os
import sys

# Add parent directory to sys.path if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from antigravity_skills_move.cli import main
except ImportError:
    # If copied standalone without package folder
    from pathlib import Path
    import zipfile
    import json
    import datetime
    import shutil
    import argparse
    import subprocess

    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    # Import fallback
    from antigravity_skills_move.core import *
    from antigravity_skills_move.cli import main

if __name__ == "__main__":
    main()
