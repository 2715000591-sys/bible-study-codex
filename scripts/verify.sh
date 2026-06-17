#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_DIR="$REPO_ROOT/.agents/skills/bible-study-codex"
VALIDATOR="$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py"

cd "$REPO_ROOT"

echo "1/5 检查安装脚本语法"
bash -n scripts/install.sh

echo "2/5 临时目录试装 Skill"
tmp_install="$(mktemp -d)"
CODEX_SKILLS_DIR="$tmp_install/skills" bash scripts/install.sh >/tmp/bible-study-install-test.out
test -f "$tmp_install/skills/bible-study-codex/SKILL.md"
test -f "$tmp_install/skills/bible-study-codex/scripts/render_package.py"

echo "3/5 运行固定生成器"
tmp_render="$(mktemp -d)"
python3 scripts/render-package.py --data examples/genesis-1-3-package.json --out "$tmp_render" >/tmp/bible-study-render-test.out
test -f "$tmp_render/open.html"
test -f "$tmp_render/genesis-1-3-package.json"
test -f "$tmp_render/genesis-1-3-study-package.html"
test -f "$tmp_render/genesis-1-3-quiz.html"
if grep -Eq 'href="[^"]+\.md"' "$tmp_render/open.html"; then
  echo "生成器入口页不能默认链接到 Markdown"
  exit 1
fi
if grep -Eq '打开完整查经包|打开互动选择题|查看来源|查看历史摘要|完整查经包' "$tmp_render/open.html"; then
  echo "生成器入口页仍包含旧按钮或旧标题"
  exit 1
fi
for target in 'genesis-1-3-study-package.html#source' 'genesis-1-3-study-package.html#sermon' 'genesis-1-3-study-package.html#summary' 'genesis-1-3-quiz.html'; do
  if ! grep -q "$target" "$tmp_render/open.html"; then
    echo "生成器入口页缺少四卡片入口：$target"
    exit 1
  fi
done
if ! grep -q '内容索引' "$tmp_render/genesis-1-3-study-package.html"; then
  echo "生成器输出缺少内容索引"
  exit 1
fi
if ! grep -q '<h2>历史背景</h2>' "$tmp_render/genesis-1-3-study-package.html"; then
  echo "生成器输出缺少历史背景"
  exit 1
fi

echo "4/5 检查 HTML 页面"
while IFS= read -r html; do
  if [[ -f "$html" ]]; then
    if ! grep -Eiq '<meta[[:space:]][^>]*charset=["'\'']?utf-8' "$html"; then
      echo "缺少 UTF-8 声明：$html"
      exit 1
    fi
    script_tmp="$(mktemp).js"
    sed -n '/<script>/,/<\/script>/p' "$html" | sed '1d;$d' > "$script_tmp"
    if [[ -s "$script_tmp" ]]; then
      node --check "$script_tmp" >/dev/null
    fi
    if [[ "$html" == outputs/* ]]; then
      if grep -Eq '这是给不会电脑的人用的|请打开 outputs/open.html|如果你不知道怎么打开|这是测试产品|使用提示|Markdown 文件|编码问题|电脑小白' "$html"; then
        echo "成品页面包含多余使用说明或技术说明：$html"
        exit 1
      fi
    fi
  fi
done < <(find templates examples outputs "$tmp_render" -type f -name '*.html' 2>/dev/null | sort)

if [[ -f outputs/open.html ]]; then
  if grep -Eq '打开完整查经包|打开互动选择题|查看来源|查看历史摘要|完整查经包' outputs/open.html; then
    echo "入口页仍包含旧按钮或旧标题：outputs/open.html"
    exit 1
  fi
  for target in 'genesis-1-3-study-package.html#source' 'genesis-1-3-study-package.html#sermon' 'genesis-1-3-study-package.html#summary' 'genesis-1-3-quiz.html'; do
    if ! grep -q "$target" outputs/open.html; then
      echo "入口页缺少四卡片入口：$target"
      exit 1
    fi
  done
  if grep -Eq 'href="[^"]+\.md"' outputs/open.html; then
    echo "入口页不能默认链接到 Markdown：outputs/open.html"
    exit 1
  fi
fi

if [[ -f outputs/genesis-1-3-study-package.html ]]; then
  if ! grep -q '内容索引' outputs/genesis-1-3-study-package.html; then
    echo "查经内容页缺少内容索引：outputs/genesis-1-3-study-package.html"
    exit 1
  fi
  source_line="$(grep -n '<h2>经文范围与来源</h2>' outputs/genesis-1-3-study-package.html | head -n 1 | cut -d: -f1 || true)"
  background_line="$(grep -n '<h2>历史背景</h2>' outputs/genesis-1-3-study-package.html | head -n 1 | cut -d: -f1 || true)"
  if [[ -z "$source_line" || -z "$background_line" || "$background_line" -le "$source_line" || $((background_line - source_line)) -gt 80 ]]; then
    echo "历史背景必须在查经内容正文靠前位置"
    exit 1
  fi
fi

if find outputs -type f -name '*.html' -print0 2>/dev/null | xargs -0 grep -q '完整查经包'; then
  echo "成品页面不应再显示“完整查经包”"
  exit 1
fi

echo "5/5 检查 Skill 格式"
if [[ -f "$VALIDATOR" ]]; then
  venv_dir="$(mktemp -d)/venv"
  python3 -m venv "$venv_dir"
  "$venv_dir/bin/python" -m pip install --quiet PyYAML
  "$venv_dir/bin/python" "$VALIDATOR" "$SKILL_DIR"
else
  echo "找不到 Skill 校验脚本，跳过：$VALIDATOR"
fi

echo "验证完成"
