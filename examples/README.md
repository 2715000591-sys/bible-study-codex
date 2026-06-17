# 示例提示词

这些示例只演示怎么使用，不包含私人查经历史。

## 给新 Codex 安装和试用

最短版：

```text
请帮我安装并试用这个 Codex 查经 Skill：https://github.com/2715000591-sys/bible-study-codex
安装后先用项目自带的创世记1章到3章示例跑固定生成器，并打开入口页让我看效果。以后我给你经文范围时，请用 $bible-study-codex 生成完整查经包。
```

严格版：

```text
请按顺序做：
1. 下载项目：https://github.com/2715000591-sys/bible-study-codex
2. 进入项目文件夹，运行 bash scripts/install.sh
3. 先运行 python3 scripts/render-package.py --data examples/genesis-1-3-package.json --out outputs --open
4. 确认浏览器打开 outputs/open.html
5. 再用 $bible-study-codex 测试“创世记1章到3章”的完整查经包
注意：安装脚本只在首次安装或项目更新后运行，平时查经不要重复安装。
```

## 默认完整查经包

```text
用 $bible-study-codex 帮我做创世记1章到3章的完整查经包。
```

更严格一点：

```text
用 $bible-study-codex 帮我做创世记1章到3章的完整查经包。请自动查 CUV，联网核对历史、地理和 David Pawson 中文讲道资源。生成后请用固定生成器打开入口页，不要只给我文件路径。
```

## 读经前

```text
用 $bible-study-codex 做马可福音4:35-41的读经前背景。请给历史背景、上下文、重要地名和简易路线图。要简洁，并附来源。
```

## 互动选择题

```text
用 $bible-study-codex 根据罗马书8:1-17生成互动选择题网页。只出选择题，7到10题，难度目标是认真读一遍能答对约70%，错题解析要讲原文大概意思。
```

## David Pawson 讲道角度

```text
用 $bible-study-codex 查 David Pawson / 大卫鲍森 有没有讲过路加福音15章。优先找中文翻译、中文字幕或中文频道；找不到文字稿就给链接，不要硬编总结。
```

## Get笔记转写稿

```text
用 $bible-study-codex 总结下面这份Get笔记转写稿。请不要猜没有标注的说话人。
```

## 分享前

```text
用 $bible-study-codex 帮我准备约翰福音3:16-21的短提纲。先问我几个真实经历问题，再写3个方向让我选。
```
