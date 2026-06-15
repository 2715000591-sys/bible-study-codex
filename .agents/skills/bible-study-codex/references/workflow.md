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

## 3. Pre-reading background

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

## 4. Pastor angle

Place the pastor angle before the post-reading summary when a preferred pastor is available. Default preference is David Pawson / 大卫鲍森 / 大卫鲍生.

Output:

- 搜索到的讲道或视频
- 是否确认讲的是当前经文
- 可读取内容类型：文字稿 / 字幕 / 简介 / 讲章笔记 / 只有视频链接
- 主要角度
- 这对读经有什么帮助
- 需要人工确认的地方

If no readable text, subtitles, notes, or reliable summary is available, provide the link and say it cannot be responsibly summarized.

## 5. Post-reading summary and interactive quiz

Output:

- 短总结
- 关键观察
- 容易误解的地方
- 与前后文、旧约或新约的呼应
- HTML 互动选择题文件
- 错题解析规则
- 来源

Do not default to a Markdown paper. Generate a printable/static version only when the user asks.

## 6. Group transcript summary

Input is usually exported from Get笔记 or another transcription tool.

Output:

- 讨论主题
- 每位成员的主要观点
- 共同看见
- 分歧或还没想清楚的问题
- 下次可以继续追问的问题
- 可保存的历史摘要

If speaker labels are missing, do not pretend to identify voices. Say that the transcript does not provide reliable speaker separation.

## 7. Personalized short sharing outline

Before drafting, ask for 2-4 short user inputs when missing:

- 这段经文哪里打到你
- 最近一个真实压力
- 有没有一个具体场景
- 分享对象是谁

Then output 3-5 points. Each point should be easy to remember and speak naturally.

## 8. Local history

Use `templates/查经历史记录.md` when the repository is available. Save a short private summary under `history/` by default when the workflow requests history.

Save only:

- 日期
- 经文
- 本次重点
- 牧师讲道角度
- 小组错题集中在哪里
- 下次继续查的问题

Do not save full study packets, full sermon content, full quiz HTML, or raw transcripts unless the user specifically asks. Never include private group transcript content in public examples.
