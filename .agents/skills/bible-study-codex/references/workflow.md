# Workflow

## 1. Passage intake

- Accept a passage reference, pasted Bible text, sermon links, or transcript text.
- If the user gives only a reference, retrieve CUV online. If retrieval is not reliable, ask for pasted text.
- Confirm the passage range when the reference is ambiguous.

## 2. Pre-reading background

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

For routes, prefer a simple text route or Mermaid diagram:

```mermaid
flowchart LR
  A["地点A"] --> B["地点B"] --> C["地点C"]
```

Only include route arrows that are supported by the passage or a cited source.

## 3. Post-reading summary and paper

Output:

- 短总结
- 关键观察
- 容易误解的地方
- 与前后文、旧约或新约的呼应
- Markdown 试卷
- 答案区
- 来源

Use 6-10 questions total. Mix choice, short answer, passage understanding, and application questions. Avoid obscure trivia.

## 4. Group transcript summary

Input is usually exported from Get笔记 or another transcription tool.

Output:

- 讨论主题
- 每位成员的主要观点
- 共同看见
- 分歧或还没想清楚的问题
- 下次可以继续追问的问题
- 可保存的历史摘要

If speaker labels are missing, do not pretend to identify voices. Say that the transcript does not provide reliable speaker separation.

## 5. Personalized short sharing outline

Before drafting, ask for 2-4 short user inputs when missing:

- 这段经文哪里打到你
- 最近一个真实压力
- 有没有一个具体场景
- 分享对象是谁

Then output 3-5 points. Each point should be easy to remember and speak naturally.

## 6. Local history

Use `templates/查经历史记录.md` when the repository is available. Save private history under `history/` only when asked.

Never include private group transcript content in public examples.
