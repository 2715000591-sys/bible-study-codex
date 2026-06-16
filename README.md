# Codex 查经项目包

这是一个可以放到 GitHub 分享的 Codex 查经项目包。第一版只服务 Codex：安装后，你可以让 Codex 根据一段经文范围，自动准备读经前背景、上下文、重要地名、必要路线图、David Pawson 讲道角度、读后总结、前后文/新旧约呼应、互动选择题网页和本地短历史摘要。

## 费用

项目本身 0 元。GitHub 公开仓库通常 0 元。

可能额外花钱的地方只有这些：

- 使用 Codex 或其他 AI 产品：按你的账号套餐算。
- 调用付费 AI API：钱花在模型生成文字、图片或转写上。
- 使用付费圣经资料或讲道资料库：钱花在资料版权或会员访问上。
- 部署服务器：钱花在网站运行环境上。
- 购买域名：钱花在网址上。

第一版只是本地 Skill 和文件模板，不需要服务器、域名或 API。

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
请你打开这个 GitHub 链接，按 README 把项目下载到本地，运行安装脚本，然后用固定生成器测试“创世记1章到3章”的完整查经包。测试完整查经包时，要先生成或使用 outputs/<passage-slug>-package.json，再运行 python3 scripts/render-package.py --data outputs/<passage-slug>-package.json --out outputs --open。这个 Skill 只需要第一次安装，平时使用不要重复安装。
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

如果只是先确认固定生成器能正常打开同款页面，可以运行：

```bash
python3 scripts/render-package.py --data examples/genesis-1-3-package.json --out outputs --open
```

正常结果是浏览器自动打开 `outputs/open.html`，里面有“打开完整查经包”和“打开互动选择题”按钮。

## 常用方式

默认完整查经包：

```text
用 $bible-study-codex 帮我做创世记1章到3章的完整查经包。
```

生成完整查经包后，Codex 应该交付一个正常 HTML 入口页，比如 `outputs/open.html` 或 `outputs/index.html`。入口页像普通网页一样打开，里面有清楚的阅读流程和按钮，可以进入完整查经包、互动选择题、来源或历史摘要。

稳定生成方式：先生成结构化数据，再运行固定生成器。新 Codex 应该优先这样做：

```bash
python3 scripts/render-package.py --data outputs/genesis-1-3-package.json --out outputs --open
```

这样页面风格、按钮、互动题和入口页都会由脚本统一生成，不靠 Codex 临场发挥。

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
- 测试产品必须有正常 HTML 入口页。完整查经包不能只交付散落文件、复杂路径或 `.md` 文件。
- 入口页必须写 `<meta charset="utf-8">`，避免 Safari 打开中文时乱码。
- 入口页标题格式：`经文范围 + 完整查经包`。
- 入口页要有清楚按钮：`打开完整查经包`、`打开互动选择题`、`查看来源`，以及有单独历史摘要时的 `查看历史摘要`。
- 入口页和完整查经包要有更像产品的索引：读经前、讲道角度、读经后、互动题、来源和历史摘要要分清楚。
- 成品页面要有克制的苹果风格：清楚层级、舒适留白、光影、阴影和适度动效；不能只靠一大堆文字堆起来。
- 完整查经包优先使用固定生成器：先写 `outputs/<passage-slug>-package.json`，再运行 `python3 scripts/render-package.py --data outputs/<passage-slug>-package.json --out outputs --open`。
- 互动题质量要经过脚本检查：7-10题、每题4个选项、至少4种题型层级、不能用偷懒选项，解析必须讲清经文大意。
- 来源要写进数据文件里的 `sources`，每条来源标明标题、链接、说明和是否已核对。
- `打开完整查经包` 必须链接到 HTML 页面，例如 `genesis-1-3-study-package.html`，不要链接到 `.md`。
- 完整查经包本体也要生成 HTML 版本。Markdown 可以保留作备份或给懂的人看，但不能作为默认打开入口。
- 成品页面只呈现内容价值，不写电脑使用教学，不解释文件路径、Markdown、HTML、编码或“怎么打开文件”。
- 历史背景必须放在完整查经包正文靠前位置，紧跟在“经文范围与来源”之后，不能只放在 README、历史摘要、来源页或外部链接里。
- 如果环境允许，生成后要自动打开入口页。macOS 优先用 Safari：`open -a Safari outputs/open.html`；其他电脑用系统默认浏览器。
- 最终回复先说入口页已经打开，再给可点击入口链接。如果确实用 Safari 打开，就说“我已经用 Safari 打开入口页。”
- 如果浏览器打不开，就用最简单的话告诉用户：`请打开 outputs/open.html，这就是入口页。`

## 交付体验

完整查经包默认应该输出到 `outputs/`，并提供一个入口页：

```text
outputs/
├── open.html                         # 用户先打开这个
├── genesis-1-3-package.json          # 结构化数据
├── genesis-1-3-study-package.html    # 完整查经包 HTML
├── genesis-1-3-quiz.html             # 互动选择题 HTML
├── genesis-1-3-sources.html          # 来源
└── genesis-1-3-history-summary.html  # 历史短摘要
```

用户正常只需要打开 `open.html`。互动题 HTML 是入口页里的一个按钮，不应该成为唯一交付物。

所有中文网页都必须有：

```html
<meta charset="utf-8">
```

完整查经包正文结构固定为：

```text
标题：经文范围 + 完整查经包
经文范围与来源
历史背景
上下文
重要人物、地名、地理关系
地理示意图（需要时）
David Pawson / 指定牧师讲道角度
阅读时留意的问题
读后短总结
前后文、旧约或新约呼应
互动选择题入口
来源
历史短摘要
```

视觉和索引规则：

- 入口页先呈现阅读流程，不做文件目录。
- 完整查经包要有内容索引和锚点，能看出读经前、讲道角度、读经后和练习的顺序。
- 查经包正文必须直接呈现历史背景，而且位置靠前。
- 页面可以有轻微动效、光影和阴影，但不要喧宾夺主。
- 页面里不要写打开文件、编码、Markdown、HTML 这类说明。

## 固定生成器

生成器文件：

```text
scripts/render-package.py
```

输入数据参考：

```text
examples/genesis-1-3-package.json
```

常用命令：

```bash
python3 scripts/render-package.py --data examples/genesis-1-3-package.json --out outputs --open
```

这个生成器会检查题目质量、来源格式、历史背景必填，并生成统一风格的 HTML 页面。

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
