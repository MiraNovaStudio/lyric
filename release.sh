#!/bin/bash
# ============================================================
# MiraNova Studios – Lyric Package Release Script
# ------------------------------------------------------------
# Cleans old build artifacts, bumps version (if provided),
# builds a fresh distribution, and uploads to PyPI.
# Usage:
#   ./release.sh [new_version]
# Example:
#   ./release.sh 0.1.0
# ============================================================

set -e  # exit immediately on error
PROJECT="lyric-lang"

echo "🚀 Starting release process for $PROJECT..."

# Step 1. Optional version bump
if [ -n "$1" ]; then
  NEW_VERSION="$1"
  echo "🔧 Updating version to $NEW_VERSION..."
  # Replace version in pyproject.toml
  sed -i.bak -E "s/^version = .*/version = \"$NEW_VERSION\"/" pyproject.toml
  rm -f pyproject.toml.bak
else
  echo "ℹ️  No version specified — using existing version."
fi

# Step 2. Clean previous builds
echo "🧹 Cleaning old build artifacts..."
rm -rf build dist *.egg-info

# Step 3. Build new package
echo "🏗️  Building distribution..."
python -m build

# Step 4. Upload to PyPI
echo "📦 Uploading to PyPI..."
twine upload dist/* -u __token__ -p "$TWINE_PASSWORD"

# Step 5. Completion
echo "✅ Release complete!"
echo "🎉 Check it out: https://pypi.org/project/$PROJECT/"
