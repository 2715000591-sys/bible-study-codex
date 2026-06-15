#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/.agents/skills/bible-study-codex"
TARGET_ROOT="${CODEX_SKILLS_DIR:-$HOME/.agents/skills}"
TARGET_DIR="$TARGET_ROOT/bible-study-codex"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "找不到 Skill 源目录：$SOURCE_DIR"
  exit 1
fi

mkdir -p "$TARGET_ROOT"

if [[ -d "$TARGET_DIR" ]]; then
  echo "检测到已安装的 bible-study-codex，将更新 Skill 文件。"
  echo "提示：只有项目更新后才需要再次运行本脚本，日常查经提问不用重复安装。"
else
  echo "准备安装 bible-study-codex。"
  echo "提示：这是首次安装。以后日常查经提问不用重复安装，除非项目更新。"
fi

mkdir -p "$TARGET_DIR"
cp -R "$SOURCE_DIR/." "$TARGET_DIR/"

echo "安装完成：$TARGET_DIR"
echo "请重启或刷新 Codex，然后用：Use \$bible-study-codex ..."
