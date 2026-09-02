#!/usr/bin/env bash
# AntigravitySkillsMove - macOS & Linux Launcher
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python3 "$DIR/antigravity_skills_move.py" "$@"
