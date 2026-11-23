#!/bin/bash
# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studio
# All rights reserved.
#
# Build a double-click Windows installer.
# Usage: ./build-win.sh [-u] [-b] [-h]
#   -u    Installer that uses the Python already on the PC
#   -b    Installer that contains its own Python
#   -h    Show this help message
#
# With no options, the unbundled installer is built.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_EMBED_VERSION="3.14.6"
UNBUNDLED=false
BUNDLED=false

while getopts "ubh" opt; do
    case "$opt" in
        u) UNBUNDLED=true ;;
        b) BUNDLED=true ;;
        h)
            echo "Usage: ./build-win.sh [-u] [-b] [-h]"
            echo ""
            echo "Build a double-click Windows installer."
            echo ""
            echo "Options:"
            echo "  -u    Unbundled. Uses Python 3.10+ already installed on the PC."
            echo "        Writes dist/LyricSetup-<version>.exe"
            echo "  -b    Bundled. Contains Python ${PYTHON_EMBED_VERSION} for Lyric."
            echo "        Writes dist/LyricSetup-<version>-bundled.exe"
            echo "  -h    Show this help message"
            echo ""
            echo "With no options, the unbundled installer is built."
            exit 0
            ;;
        *) exit 1 ;;
    esac
done

if [ "$UNBUNDLED" = false ] && [ "$BUNDLED" = false ]; then
    UNBUNDLED=true
fi

if py -3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
    PYTHON=(py -3)
elif python -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
    PYTHON=(python)
elif python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
    PYTHON=(python3)
else
    echo "Python 3.10+ is required to build the installer. Looked for py -3, python, and python3." >&2
    exit 1
fi

CSC="/c/Windows/Microsoft.NET/Framework64/v4.0.30319/csc.exe"
if [ ! -f "$CSC" ]; then
    echo "The .NET Framework C# compiler was not found at $CSC" >&2
    exit 1
fi

VERSION="$(sed -n 's/^__version__ = "\([^"]*\)".*/\1/p' lyric/__init__.py)"
if [ -z "$VERSION" ]; then
    echo "Could not read __version__ from lyric/__init__.py" >&2
    exit 1
fi

FILE_VERSION="${VERSION}"
case "$FILE_VERSION" in
    *.*.*.*) ;;
    *.*.*) FILE_VERSION="${FILE_VERSION}.0" ;;
    *.*) FILE_VERSION="${FILE_VERSION}.0.0" ;;
    *) FILE_VERSION="${FILE_VERSION}.0.0.0" ;;
esac

mkdir -p dist
echo "Building package..."
"${PYTHON[@]}" -m pip wheel . -w dist --no-deps
WHEEL="$(ls -1t dist/lyric_lang-*.whl | head -n 1)"

compile_installer() {
    local out="$1"
    local title="$2"
    local define="$3"
    shift 3

    local info="dist/AssemblyInfo.cs"
    local wheel_name
    wheel_name="$(basename "$WHEEL")"
    cat > "$info" << EOF
using System.Reflection;
[assembly: AssemblyTitle("${title}")]
[assembly: AssemblyProduct("Lyric")]
[assembly: AssemblyVersion("${FILE_VERSION}")]
[assembly: AssemblyFileVersion("${FILE_VERSION}")]

static class WheelInfo
{
    public const string FileName = "${wheel_name}";
}
EOF

    local args=(
        /nologo
        /target:winexe
        /out:"$(cygpath -w "$out")"
        /reference:System.Windows.Forms.dll
        /reference:System.Drawing.dll
        /win32icon:"$(cygpath -w packaging/lyric.ico)"
        /resource:"$(cygpath -w "$WHEEL")",lyric.whl
    )
    if [ -n "$define" ]; then
        args+=(/define:"$define")
    fi
    while [ "$#" -gt 0 ]; do
        args+=("$1")
        shift
    done
    args+=("$(cygpath -w packaging/LyricSetup.cs)" "$(cygpath -w "$info")")

    echo "Building ${out}..."
    MSYS_NO_PATHCONV=1 "$CSC" "${args[@]}"
    echo "Installer: ${out}"
}

if [ "$UNBUNDLED" = true ]; then
    compile_installer "dist/LyricSetup-${VERSION}.exe" "Lyric Setup ${VERSION}" ""
fi

if [ "$BUNDLED" = true ]; then
    CACHE="build/win-bundle"
    mkdir -p "$CACHE"
    EMBED_ZIP="${CACHE}/python-${PYTHON_EMBED_VERSION}-embed-amd64.zip"
    GET_PIP="${CACHE}/get-pip.py"
    if [ ! -f "$EMBED_ZIP" ]; then
        echo "Downloading Python ${PYTHON_EMBED_VERSION}..."
        curl -fL --retry 3 -o "$EMBED_ZIP" \
            "https://www.python.org/ftp/python/${PYTHON_EMBED_VERSION}/python-${PYTHON_EMBED_VERSION}-embed-amd64.zip"
    fi
    if [ ! -f "$GET_PIP" ]; then
        echo "Downloading pip bootstrap..."
        curl -fL --retry 3 -o "$GET_PIP" "https://bootstrap.pypa.io/get-pip.py"
    fi
    compile_installer "dist/LyricSetup-${VERSION}-bundled.exe" "Lyric Setup ${VERSION} bundled" "BUNDLED" \
        /resource:"$(cygpath -w "$EMBED_ZIP")",python.zip \
        /resource:"$(cygpath -w "$GET_PIP")",getpip.py
fi

rm -f dist/LyricSetup.exe
echo ""
echo "Double-click the installer to install."
