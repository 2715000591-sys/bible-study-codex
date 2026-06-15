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

## Core Rules

- Ask for the passage range if missing. Accept spoken ranges like `创世记1章到3章`, `罗马书8章`, `约翰福音3章16到21节`, `John 3:16-21`, or `创世记12章`.
- Treat a passage range as enough input. Normalize the range, retrieve CUV online by default, and ask for pasted text only when lookup fails or the translation source is unclear.
- When the user gives a passage and no narrower task, produce the default full study package: CUV text reference, pre-reading background, context, key places, needed route/geography diagram, David Pawson or specified-pastor sermon angle, reading focus, post-reading summary, cross-references, interactive HTML quiz, and short history summary.
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

1. **默认完整查经包**: passage range normalization, CUV lookup, background, context, key places, route/geography diagram when needed, David Pawson or specified-pastor angle, reading focus, post-reading summary, cross-references, HTML quiz, short history summary.
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
