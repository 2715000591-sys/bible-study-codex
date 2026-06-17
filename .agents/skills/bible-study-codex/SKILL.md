---
name: bible-study-codex
description: Codex Bible study workflow for concise evangelical study packages. Use when the user gives a spoken Bible passage range and wants CUV lookup, pre-reading background, context, geography or route diagrams, David Pawson or specified-pastor sermon angle research, post-reading summaries, Old/New Testament echoes, interactive HTML multiple-choice quizzes with explanations, Get笔记 transcript summaries, personalized short sharing outlines, or short local history summaries.
---

# Codex Bible Study

## Overview

Guide a Codex session through a short, sourced Bible-study workflow. Keep outputs readable for normal readers, avoid long sermon-style prose, and do not present guesses as facts.

## Reference Map

Load only the reference needed for the current task:

- `references/workflow.md` for the default full study package, transcript, sharing-outline, and short-history workflow.
- `references/source-policy.md` for CUV lookup, web verification, citations, and uncertainty rules.
- `references/pastor-research.md` for handling user-specified pastor names and sermon/video summaries.
- `references/interactive-quiz.md` for HTML quiz generation, difficulty, scoring, and explanations.
- `references/package-data.md` for the required JSON data contract and renderer command.

## Core Rules

- Ask for the passage range if missing. Accept spoken ranges like `创世记1章到3章`, `罗马书8章`, `约翰福音3章16到21节`, `John 3:16-21`, or `创世记12章`.
- Treat a passage range as enough input. Normalize the range, retrieve CUV online by default, and ask for pasted text only when lookup fails or the translation source is unclear.
- When the user gives a passage and no narrower task, produce the default full study package: CUV text reference, pre-reading background, context, key places, needed route/geography diagram, David Pawson or specified-pastor sermon angle, reading focus, post-reading summary, cross-references, interactive HTML quiz, and short history summary.
- For a full study package, first write structured package data to `outputs/<passage-slug>-package.json`, then render the pages with the bundled renderer. In the repository, run `python3 scripts/render-package.py --data outputs/<passage-slug>-package.json --out outputs --open`. Do not hand-write finished HTML when the renderer is available.
- A full study package must include a user-openable HTML entry page. Do not deliver only scattered Markdown/HTML file paths. Create an entry page such as `outputs/open.html` or `outputs/<passage>/index.html` with `<meta charset="utf-8">`, the passage range as the title, and four clickable cards: `读经前`, `讲道角度`, `读经后`, and `互动题`.
- Do not put top action buttons on the entry page. Do not show labels such as `打开完整查经包`, `打开互动选择题`, `查看来源`, or `查看历史摘要` on the entry page. Fold those destinations into the four cards.
- The full study package body must also have an HTML version such as `genesis-1-3-study-package.html`. Markdown may exist as backup, but the entry page cards must link to HTML pages or HTML anchors, not to `.md`.
- All Chinese HTML pages must include `<meta charset="utf-8">` to prevent garbled text in Safari.
- Finished pages should feel like a polished, Apple-inspired reading product: restrained colors, strong hierarchy, subtle light/shadow, tasteful motion, and a clear index. Do not rely on dense prose alone.
- Product pages must be content-first. Put `历史背景` inside the study package body near the top, right after `经文范围与来源`. Do not put historical background only in README, notes, history summary, or external links.
- Do not put technical user instructions in finished pages. Avoid page copy about file paths, Markdown, HTML, encodings, "test product", "how to open", or "computer beginners". Explain opening steps only in the Codex final reply when needed.
- If the environment allows opening local files, open the entry page in the user's browser immediately after generation. On macOS, prefer Safari when available, for example `open -a Safari outputs/open.html`; otherwise use the system browser. In the final reply, say that the entry page has been opened first, then provide a clickable entry link. If opening fails, explain in plain language: `请打开 outputs/open.html，这就是入口页。`
- Verify historical background, geography, travel/war routes, and sermon information online. Provide short source links for claims that depend on external facts.
- Keep every answer concise. Prefer a few clear sections over long commentary.
- For Old/New Testament echoes, cross-references, and later narrative connections, place them mainly in the post-reading output unless the user asks for them before reading.
- Default pastor preference is David Pawson / 大卫鲍森 / 大卫鲍生. Do not randomly recommend other pastors. Use only the default or the pastor names/links the user provides. If same-name or channel confusion is possible, ask for confirmation before summarizing.
- Put the pastor-sermon angle early in the package, after the background/context, so readers know what notable angle to watch for before discussion.
- Generate an interactive HTML multiple-choice quiz by default. Do not default to a Markdown paper unless the user asks for a printable/static version.
- If a source cannot be verified, mark it as `需要人工确认` and keep it out of firm conclusions.
- If the user's interpretation may not fit the passage, gently flag the issue before rewriting.
- Save only a short local history summary by default. Do not save the full package, full sermon content, or full quiz unless the user specifically asks. Use local files under `history/`; never upload private history.

## Output Modes

Choose the closest mode from the user's request:

1. **默认查经内容**: passage range normalization, CUV lookup, background, context, key places, route/geography diagram when needed, David Pawson or specified-pastor angle, reading focus, post-reading summary, cross-references, HTML quiz, short history summary.
2. **读经前背景**: passage text reference, historical setting, context, key people/places, geography or route, questions to watch while reading.
3. **读经后总结与互动题**: plain summary, key observations, misunderstandings to avoid, cross-references, interactive HTML multiple-choice quiz with answer explanations.
4. **指定牧师讲道整理**: verify the pastor identity, find sermons on the same passage, summarize only readable/watchable material, or provide links without inventing.
5. **小组转写稿总结**: process Get笔记 or other transcript text, separate speakers when labels exist, summarize themes, questions, and follow-ups.
6. **分享前短提纲**: ask for the user's real experience or pressure point first, then produce a short outline for natural spoken sharing.
7. **历史短摘要**: create a short local Markdown summary using the repository template and keep private content out of public examples.

## Style

- Use short, direct Chinese by default when the user writes Chinese.
- Explain necessary technical terms in plain language.
- Avoid ornate devotional language and over-polished slogans.
- For sharing outlines, use this shape: what happened in the passage, what it means, where it touches daily pressure, one honest closing reminder.
- Keep quiz questions fair but not childish: test structure, textual basis, comparison, and application. Avoid obscure trivia, verse-by-verse memorization, and disputed questions as scored answers.
