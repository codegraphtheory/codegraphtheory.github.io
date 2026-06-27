#!/usr/bin/env bash
# Copy README demo GIFs from sibling GraphTheory repos into site assets.
set -euo pipefail
SITE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECTS_ROOT="$(cd "$SITE_ROOT/.." && pwd)"
DEST="$SITE_ROOT/assets/demos"
mkdir -p "$DEST"
REPOS=(
  hermes-profile-template
  heavy-coder
  context-forge-rag
  chainforge
  solana-rug
)
for name in "${REPOS[@]}"; do
  src="$PROJECTS_ROOT/$name/demos/demo.gif"
  if [[ ! -f "$src" ]]; then
    echo "missing: $src (run ./demos/vhs/render_demo_gif.sh in that repo first)" >&2
    exit 1
  fi
  cp "$src" "$DEST/$name.gif"
  echo "synced $name.gif"
done
ls -lh "$DEST"/*.gif