#!/usr/bin/env bash
# Copia la skill de este repo a Claude Code y Codex.
# Vuelve a ejecutarlo cada vez que edites algo en skills/marca.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/skills/marca"

if [ ! -f "$SRC/SKILL.md" ]; then
  echo "✗ no se encontró la skill en $SRC (falta SKILL.md)" >&2
  exit 1
fi

for dest in "$HOME/.claude/skills" "$HOME/.codex/skills"; do
  mkdir -p "$dest"
  # Migración: la skill antes se llamaba logo-design. Borra esa copia para no tener dos skills iguales.
  if [ -d "$dest/logo-design" ]; then
    rm -rf "$dest/logo-design"
    echo "• se borró la versión anterior en $dest/logo-design"
  fi
  rm -rf "$dest/marca"
  cp -R "$SRC" "$dest/marca"
  find "$dest/marca" -name "__pycache__" -type d -prune -exec rm -rf {} +
  echo "✓ instalada en $dest/marca"
done
