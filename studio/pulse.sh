#!/usr/bin/env bash
# create_journal_post.sh
# Usage:
#   ./journal.sh "Custom"    # Create custom post
#   ./journal.sh -1          # Edit most recent journal post
#   ./journal.sh -2          # Edit second most recent journal post
#   ./journal.sh -3          # Edit third most recent journal post
#   ./journal.sh -4          # Edit fourth most recent journal post
#   ./journal.sh -5          # Edit fifth most recent journal post
#   ./journal.sh -l          # List the 5 most recent journal posts
#   ./journal.sh -h          # Show usage help

JOURNAL_DIR="content/journal"
mkdir -p "$JOURNAL_DIR"

# Metadata
TIMESTAMP=$(date +"%Y%m%d_%H%M")
POST_FILE="$JOURNAL_DIR/${TIMESTAMP}_POST.md"
DATE=$(date +"%Y-%m-%d")
AUTHOR="Michael (Aeonath)"

show_help() {
  echo "Usage:"
  echo "  $0 \"Custom Title\"        # Create custom post with a specific title"
  echo "  $0 -1                   # Edit most recent journal post in vim"
  echo "  $0 -2                   # Edit second most recent journal post in vim"
  echo "  $0 -3                   # Edit third most recent journal post in vim"
  echo "  $0 -4                   # Edit fourth most recent journal post in vim"
  echo "  $0 -5                   # Edit fifth most recent journal post in vim"
  echo "  $0 -l                   # List the 5 most recent journal posts"
  echo "  $0 -h                   # Show this help message"
  exit 0
}

open_recent() {
  local n=$1
  local file
  file=$(ls "$JOURNAL_DIR"/*.md 2>/dev/null | sort -r | sed -n "${n}p")
  if [ -z "$file" ]; then
    echo "Error: No journal post found at position $n"
    exit 1
  fi
  echo "Opening: $file"
  vim "$file"
  exit 0
}

# Parse arguments
case "$1" in
  -h|--help)
    show_help
    ;;
  -1)
    open_recent 1
    ;;
  -2)
    open_recent 2
    ;;
  -3)
    open_recent 3
    ;;
  -4)
    open_recent 4
    ;;
  -5)
    open_recent 5
    ;;
  -l)
    echo "Recent journal posts:"
    ls "$JOURNAL_DIR"/*.md 2>/dev/null | sort -r | head -5 | nl -w1 -s") "
    exit 0
    ;;
  "")
    show_help
    ;;
  *)
    TITLE="$*"
    ;;
esac

# Create the post
cat > "$POST_FILE" <<EOF
---
title: "$TITLE"
date: "$DATE"
author: "$AUTHOR"
---

(Write your post content here.)

*— Michael (Aeonath)*

EOF

echo "Created: ($TITLE) $POST_FILE"
