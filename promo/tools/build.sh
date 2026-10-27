#!/usr/bin/env bash
# Render the promo end to end: subframes -> motion-blurred 60 fps video -> mux the motion-sound soundtrack.
# Usage: promo/tools/build.sh <work_dir> <output.mp4>
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
work="$1"; out="$2"
python3 -I "$here/make_sfx.py" > /dev/null
rm -rf "$work/frames"
node "$here/render.cjs" "$work/frames" 4
# tmix at frame n averages n-2..n, so every third output (n mod 3 == 2) is one centred (t-, t, t+) triplet.
ffmpeg -v error -y -framerate 180 -i "$work/frames/%05d.jpg" -i "$here/../sfx/soundtrack.m4a" \
  -vf "tmix=frames=3,select='eq(mod(n\,3)\,2)',setpts=N/60/TB,format=yuv420p" -r 60 \
  -c:v libx264 -preset slow -crf 16 -profile:v high -movflags +faststart \
  -c:a copy -shortest "$out"
