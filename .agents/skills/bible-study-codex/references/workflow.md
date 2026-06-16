# Workflow

## 1. Passage intake

- Accept a passage reference, pasted Bible text, sermon links, or transcript text.
- Expect spoken Chinese ranges such as `创世记1章到3章`, `罗马书8章`, or `约翰福音3章16到21节`.
- Normalize the spoken range into a clear Bible reference before searching.
- If the user gives only a reference, retrieve CUV online. If retrieval is not reliable, ask for pasted text.
- Confirm the passage range only when the range is ambiguous or too broad to handle responsibly.

## 2. Default full study package

When the user gives a passage range without a narrower task, produce this package in order:

1. 经文范围与 CUV 来源
2. 读经前背景
3. 上下文
4. 重要人物、地名、地理关系
5. 必要路线、迁徙、战争或地理示意图
6. David Pawson / 大卫鲍森或用户指定牧师的讲道角度
7. 阅读时留意的问题
8. 读后短总结
9. 前后文、旧约或新约呼应
10. HTML 互动选择题
11. 本次历史短摘要

Keep it concise. The goal is a usable study packet, not a long commentary.

Implementation order:

1. Search and verify sources for Bible text, historical/geographic claims, and preferred-pastor material.
2. Write `outputs/<passage-slug>-package.json` using `references/package-data.md`.
3. Run `python3 scripts/render-package.py --data outputs/<passage-slug>-package.json --out outputs --open`.
4. Run `bash scripts/verify.sh` when the repository is available.
5. Final reply starts with the opened entry page, then a short note about files and verification.

Do not hand-write the final HTML when the renderer is available. The renderer is the stable product surface.

## 3. User-openable delivery

A full study package must feel like a product the user can open, not a list of engineering files. The default open target is an HTML entry page.

Default output structure:

- `outputs/open.html` or `outputs/<passage-slug>/index.html` as the entry page
- `outputs/<passage-slug>-study-package.html` for the full study package body
- `outputs/<passage-slug>-quiz.html` for the interactive multiple-choice quiz
- `outputs/<passage-slug>-sources.html` when sources exist
- `outputs/<passage-slug>-history-summary.html` when a short history summary exists
- optional `.md` backups for people who know how to use them

The entry page must include:

- `<meta charset="utf-8">`
- a clear title with the passage range
- a short content-focused sentence about the passage
- a logical reading-flow index, usually `读经前 -> 讲道角度 -> 读经后 -> 互动题`
- a button or prominent link: `打开完整查经包`, linking to the HTML study package, not `.md`
- a button or prominent link: `打开互动选择题`
- a button or prominent link: `查看来源` when a separate sources page exists
- a button or prominent link: `查看历史摘要` when a separate history summary page exists

All Chinese HTML pages must include `<meta charset="utf-8">`, including entry pages, study package pages, quiz pages, sources pages, and history-summary pages. This prevents Safari from opening Chinese as garbled text.

Finished product pages must be content-first:

- Do not write computer-use teaching into product pages.
- Do not explain file paths, encodings, Markdown, HTML, or how to open files inside the product pages.
- Do not write phrases like `这是测试产品`, `请打开 outputs/open.html`, `如果你不知道怎么打开`, or `适合电脑小白`.
- If opening guidance is needed, put it only in the Codex final reply.
- Use a polished, Apple-inspired visual style: quiet colors, strong hierarchy, subtle shadows, light effects, tasteful motion, and generous spacing.
- The package must not be pure prose. Add a clear content index, section anchors, and lightweight interaction such as scroll reveal or active-section highlighting when practical.

The study package HTML body must use this content order:

1. 标题：经文范围 + 完整查经包
2. 经文范围与来源
3. 历史背景
4. 上下文
5. 重要人物、地名、地理关系
6. 地理示意图, when needed
7. David Pawson / 指定牧师讲道角度
8. 阅读时留意的问题
9. 读后短总结
10. 前后文、旧约或新约呼应
11. 互动选择题入口
12. 来源
13. 历史短摘要

`历史背景` must appear inside the study package body near the top. It is not enough to put it in README, a history file, a source note, or an external link.

After generating the entry page:

1. Open it in the user's browser immediately when the local environment allows it. On macOS, prefer Safari when available, for example `open -a Safari outputs/open.html`; otherwise use the system default browser.
2. In the final reply, do not lead with scattered file paths. Start by saying the entry page has been opened. If Safari opened it, say `我已经用 Safari 打开入口页。`
3. Then provide one clickable entry link to `index.html` or `open.html`.
4. If the browser cannot open it, say plainly: `请打开 outputs/open.html，这就是入口页。`
5. Mention extra file paths only after the entry link, and only if useful.

## 4. Pre-reading background

Output:

- 经文范围
- 一句话背景
- 历史处境
- 上下文
- 重要人物和地名
- 地理或路线
- 阅读时留意的问题
- 来源

Keep Old/New Testament echoes light here. Save fuller cross-reference work for the post-reading mode.

For routes, migrations, war movements, or major geography, proactively include a simple diagram when the passage naturally needs it:

```mermaid
flowchart LR
  A["地点A"] --> B["地点B"] --> C["地点C"]
```

Only include route arrows that are supported by the passage or a cited source. Label generated maps as `示意图`.

## 5. Pastor angle

Place the pastor angle before the post-reading summary when a preferred pastor is available. Default preference is David Pawson / 大卫鲍森 / 大卫鲍生.

Output:

- 搜索到的讲道或视频
- 是否确认讲的是当前经文
- 可读取内容类型：文字稿 / 字幕 / 简介 / 讲章笔记 / 只有视频链接
- 主要角度
- 这对读经有什么帮助
- 需要人工确认的地方

If no readable text, subtitles, notes, or reliable summary is available, provide the link and say it cannot be responsibly summarized.

## 6. Post-reading summary and interactive quiz

Output:

- 短总结
- 关键观察
- 容易误解的地方
- 与前后文、旧约或新约的呼应
- HTML 互动选择题文件, linked from the entry page as a button
- 错题解析规则
- 来源

Do not default to a Markdown paper. Generate a printable/static version only when the user asks.

## 7. Group transcript summary

Input is usually exported from Get笔记 or another transcription tool.

Output:

- 讨论主题
- 每位成员的主要观点
- 共同看见
- 分歧或还没想清楚的问题
- 下次可以继续追问的问题
- 可保存的历史摘要

If speaker labels are missing, do not pretend to identify voices. Say that the transcript does not provide reliable speaker separation.

## 8. Personalized short sharing outline

Before drafting, ask for 2-4 short user inputs when missing:

- 这段经文哪里打到你
- 最近一个真实压力
- 有没有一个具体场景
- 分享对象是谁

Then output 3-5 points. Each point should be easy to remember and speak naturally.

## 9. Local history

Use `templates/查经历史记录.md` when the repository is available. Save a short private summary under `history/` by default when the workflow requests history.

Save only:

- 日期
- 经文
- 本次重点
- 牧师讲道角度
- 小组错题集中在哪里
- 下次继续查的问题

Do not save full study packets, full sermon content, full quiz HTML, or raw transcripts unless the user specifically asks. Never include private group transcript content in public examples.
