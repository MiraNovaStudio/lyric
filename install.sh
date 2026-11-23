#!/bin/bash
# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studio
# All rights reserved.
#
# Install Lyric from this source tree into the current Python environment.
# Usage: ./install.sh [-e] [-h]
#   -e    Editable install (pip install -e .)
#   -h    Show this help message

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

EDITABLE=false

while getopts "eh" opt; do
    case "$opt" in
        e) EDITABLE=true ;;
        h)
            echo "Usage: ./install.sh [-e] [-h]"
            echo ""
            echo "Install Lyric from this checkout into the current Python environment."
            echo ""
            echo "Options:"
            echo "  -e    Editable install (pip install -e .)"
            echo "  -h    Show this help message"
            exit 0
            ;;
        *) exit 1 ;;
    esac
done

# Git Bash may expose Python as py, python, or python3.
if py -3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
    PYTHON=(py -3)
elif python -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
    PYTHON=(python)
elif python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
    PYTHON=(python3)
else
    echo "Python 3.10+ is required. Looked for py -3, python, and python3." >&2
    exit 1
fi

if [ "$EDITABLE" = true ]; then
    "${PYTHON[@]}" -m pip install -e .
else
    "${PYTHON[@]}" -m pip install .
fi
