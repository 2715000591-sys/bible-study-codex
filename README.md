# Codex 查经项目包

这是一个可以放到 GitHub 分享的 Codex 查经项目包。第一版只服务 Codex：安装后，你可以让 Codex 根据一段经文范围，自动准备读经前背景、上下文、重要地名、必要路线图、David Pawson 讲道角度、读后总结、前后文/新旧约呼应、互动选择题网页和本地短历史摘要。

## 费用

项目本身 0 元。GitHub 公开仓库通常 0 元。使用 Codex、付费圣经资料、服务器、域名或外部 AI API 时，费用按对应平台为准。

## 安装

安装脚本只需要在**第一次使用**或**项目更新后**运行。平时问查经问题时，不要重复安装。

新电脑或新 Codex 从零开始：

```bash
git clone https://github.com/2715000591-sys/bible-study-codex.git
cd bible-study-codex
bash scripts/install.sh
```

如果已经下载过项目，就在这个项目根目录运行：

```bash
bash scripts/install.sh
```

安装完成后，重启 Codex。之后可以这样说：

```text
用 $bible-study-codex 帮我做约翰福音3:16-21的读经前背景。
```

如果你只想在这个项目里试用，也可以直接用 Codex 打开本文件夹。仓库里的 `.agents/skills/bible-study-codex` 已经是可读的 Skill。

## 给新 Codex 的一句话

把下面这句话给一个完全不知道本项目的新 Codex。正常人这样说就可以：

```text
帮我安装并试用这个 Codex 查经 Skill：https://github.com/2715000591-sys/bible-study-codex
请你打开这个 GitHub 链接，按 README 把项目下载到本地，运行安装脚本，然后用它测试“创世记1章到3章”的完整查经包。这个 Skill 只需要第一次安装，平时使用不要重复安装。
```

如果你就是正在执行这句话的 Codex，请按这个顺序做：

```bash
git clone https://github.com/2715000591-sys/bible-study-codex.git
cd bible-study-codex
bash scripts/install.sh
```

安装后重启或刷新 Codex，再测试：

```text
用 $bible-study-codex 帮我做创世记1章到3章的完整查经包。
```

## 常用方式

默认完整查经包：

```text
用 $bible-study-codex 帮我做创世记1章到3章的完整查经包。
```

读经前背景：

```text
用 $bible-study-codex 做马可福音4:35-41的读经前背景，给历史背景、上下文、重要地名和简易路线图。
```

互动选择题：

```text
用 $bible-study-codex 根据罗马书8:1-17生成互动选择题网页，7到10题，只要选择题。
```

David Pawson 讲道角度：

```text
用 $bible-study-codex 查 David Pawson / 大卫鲍森有没有讲过路加福音15章。优先找中文翻译、中文字幕或中文频道；找不到文字稿就给链接，不要硬编总结。
```

小组讨论：

```text
用 $bible-study-codex 总结下面这份Get笔记转写稿，按成员观点和后续问题整理。
```

分享前：

```text
用 $bible-study-codex 帮我把这段经文整理成一个短提纲。先问我几个真实经历问题，再写。
```

## 项目内容

- `.agents/skills/bible-study-codex/`：Codex Skill。
- `scripts/install.sh`：安装脚本。
- `templates/`：读经背景、互动选择题、小组总结、分享提纲、历史记录模板。
- `guides/get-note.md`：Get笔记使用教学。
- `sources/`：偏好牧师名单模板。
- `examples/`：示例提示词。
- `history/`：本地私有历史保存处。

## 重要规则

- 默认经文译本是和合本 CUV。
- 不把整本圣经打包进项目。
- 历史、地理、讲道信息需要联网核对。
- 查不到来源就不要硬说。
- 默认偏好牧师是 David Pawson / 大卫鲍森 / 大卫鲍生。优先找中文翻译、中文字幕或中文频道。
- 找不到讲道文字稿、字幕、简介或讲章笔记时，可以给视频链接，但不要硬编总结。
- 默认生成 HTML 互动选择题，不默认生成 Markdown 试卷。
- 互动题只做选择题，每次 7-10 题。题目不要背书、不要抠字眼，难度目标是认真读一遍能答对约 70%。
- 如果经文本身涉及迁徙、战争、路线或明显地理移动，要主动生成示意图，并标明是示意图。
- `history/` 默认不上传 GitHub，也不自动备份。默认只保存短摘要，不保存完整查经包。

## 历史保存

私人查经记录请放在 `history/`。这个目录默认只保留说明文件，具体查经记录会被 Git 忽略，避免你把小组内容或个人感受误传到公开仓库。

默认只保存短摘要，比如：日期、经文、本次重点、牧师讲道角度、小组错题集中在哪里、下次继续查的问题。完整查经包、完整讲道内容、完整互动题不默认保存。

如果将来想备份历史，可以自己复制到网盘或另建私有仓库。第一版不做自动备份。

## 验证

本地检查项目是否正常：

```bash
bash scripts/verify.sh
```

这个命令会检查安装脚本、Skill 格式和互动题页面脚本。它只使用临时目录测试，不会安装到你的真实 Codex。
