#!/usr/bin/env python3
"""将 M4A/AAC 音频转为 MP3。"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_INPUT = Path(
    "/home/ubuntu/stephen/01-code/UI4Bot/audio/机器狗的作战屏幕.m4a"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将 M4A 转为 MP3")
    parser.add_argument(
        "input",
        nargs="?",
        default=str(DEFAULT_INPUT),
        help=f"输入 M4A 文件（默认: {DEFAULT_INPUT}）",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="输出 MP3 文件（默认: 与输入同名的 .mp3）",
    )
    parser.add_argument(
        "-b",
        "--bitrate",
        default="192k",
        help="MP3 码率，默认 192k",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = (
        Path(args.output).resolve()
        if args.output
        else input_path.with_suffix(".mp3")
    )

    if not input_path.is_file():
        print(f"错误: 输入文件不存在: {input_path}", file=sys.stderr)
        return 1

    if shutil.which("ffmpeg") is None:
        print("错误: 未找到 ffmpeg，请先安装: sudo apt install ffmpeg", file=sys.stderr)
        return 1

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-codec:a",
        "libmp3lame",
        "-b:a",
        args.bitrate,
        str(output_path),
    ]

    print(f"输入: {input_path}")
    print(f"输出: {output_path}")
    print("开始转换...")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"错误: ffmpeg 转换失败，退出码 {exc.returncode}", file=sys.stderr)
        return exc.returncode

    print(f"完成: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
