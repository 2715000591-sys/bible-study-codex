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
  echo "检测到已安装的 bible-study-codex，将更新文件。不会删除你的其他 Skill。"
else
  echo "准备安装 bible-study-codex。"
fi

mkdir -p "$TARGET_DIR"
cp -R "$SOURCE_DIR/." "$TARGET_DIR/"

echo "安装完成：$TARGET_DIR"
echo "请重启 Codex，然后用：Use \$bible-study-codex ..."
