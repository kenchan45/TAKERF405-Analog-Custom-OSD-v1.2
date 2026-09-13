#!/usr/bin/env bash
set -euo pipefail
BF_DIR=${1:-betaflight}
THIS_DIR="$(cd "$(dirname "$0")" && pwd)"
COMMIT=11910a0912b9462e15e700be091a40a04181d190

if [ ! -d "$BF_DIR/.git" ]; then
  echo "Betaflight source tree not found at: $BF_DIR" >&2
  echo "Clone betaflight/betaflight and checkout $COMMIT first." >&2
  exit 1
fi

git -C "$BF_DIR" checkout "$COMMIT"
python3 "$THIS_DIR/patch_betaflight_kiss_sticks.py" "$BF_DIR"
rm -rf "$BF_DIR/src/config/configs/TAKERF405"
mkdir -p "$BF_DIR/src/config/configs"
cp -r "$THIS_DIR/custom_config/configs/TAKERF405" "$BF_DIR/src/config/configs/"
make -C "$BF_DIR" arm_sdk_install
make -C "$BF_DIR" TAKERF405 CONFIG_DIR="$BF_DIR/src/config"

echo "Build complete. HEX files:"
find "$BF_DIR/obj" -type f -name '*.hex' -print 2>/dev/null || true
