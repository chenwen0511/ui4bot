#!/usr/bin/env bash
# 将 WebM 转为 MP4（H.264 + AAC），兼容主流播放器与浏览器。
#
# 用法:
#   ./scripts/webm_to_mp4.sh
#   ./scripts/webm_to_mp4.sh /path/to/input.webm
#   ./scripts/webm_to_mp4.sh /path/to/input.webm /path/to/output.mp4

set -euo pipefail

INPUT="${1:-/home/ubuntu/stephen/01-code/UI4Bot/video/traybot.webm}"

if [[ ! -f "$INPUT" ]]; then
  echo "错误: 输入文件不存在: $INPUT" >&2
  exit 1
fi

if [[ -n "${2:-}" ]]; then
  OUTPUT="$2"
else
  OUTPUT="${INPUT%.*}.mp4"
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "错误: 未找到 ffmpeg，请先安装: sudo apt install ffmpeg" >&2
  exit 1
fi

echo "输入: $INPUT"
echo "输出: $OUTPUT"
echo "开始转换..."

ffmpeg -y -i "$INPUT" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "$OUTPUT"

echo "完成: $OUTPUT"
