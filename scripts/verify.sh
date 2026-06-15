#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_DIR="$REPO_ROOT/.agents/skills/bible-study-codex"
VALIDATOR="$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py"

cd "$REPO_ROOT"

echo "1/4 检查安装脚本语法"
bash -n scripts/install.sh

echo "2/4 临时目录试装 Skill"
tmp_install="$(mktemp -d)"
CODEX_SKILLS_DIR="$tmp_install/skills" bash scripts/install.sh >/tmp/bible-study-install-test.out
test -f "$tmp_install/skills/bible-study-codex/SKILL.md"

echo "3/4 检查 HTML 互动题脚本"
for html in templates/互动选择题模板.html examples/interactive-quiz-demo.html; do
  if [[ -f "$html" ]]; then
    script_tmp="$(mktemp).js"
    sed -n '/<script>/,/<\/script>/p' "$html" | sed '1d;$d' > "$script_tmp"
    node --check "$script_tmp" >/dev/null
  fi
done

echo "4/4 检查 Skill 格式"
if [[ -f "$VALIDATOR" ]]; then
  venv_dir="$(mktemp -d)/venv"
  python3 -m venv "$venv_dir"
  "$venv_dir/bin/python" -m pip install --quiet PyYAML
  "$venv_dir/bin/python" "$VALIDATOR" "$SKILL_DIR"
else
  echo "找不到 Skill 校验脚本，跳过：$VALIDATOR"
fi

echo "验证完成"
