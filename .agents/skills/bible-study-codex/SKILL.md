---
name: bible-study-codex
description: Codex Bible study workflow for preparing concise evangelical Bible-study help. Use when the user asks for pre-reading historical and geographical background, passage context, CUV Bible passage lookup, post-reading summaries, Markdown quiz papers, specified-pastor sermon research and summaries, Get笔记 transcript summaries, personalized short sharing outlines, or local Bible-study history records.
---

# Codex Bible Study

## Overview

Guide a Codex session through a short, sourced Bible-study workflow. Keep outputs readable for normal readers, avoid long sermon-style prose, and do not present guesses as facts.

## Reference Map

Load only the reference needed for the current task:

- `references/workflow.md` for the full read-before, read-after, transcript, and sharing-outline workflow.
- `references/source-policy.md` for CUV lookup, web verification, citations, and uncertainty rules.
- `references/pastor-research.md` for handling user-specified pastor names and sermon/video summaries.

## Core Rules

- Ask for the passage if missing. Accept formats like `约翰福音3:16-21`, `John 3:16-21`, or `创世记12章`.
- If the user only gives a passage reference, retrieve the text online with CUV as the default. If retrieval fails or the translation source is unclear, ask the user to paste the passage.
- Verify historical background, geography, travel/war routes, and sermon information online. Provide short source links for claims that depend on external facts.
- Keep every answer concise. Prefer a few clear sections over long commentary.
- For Old/New Testament echoes, cross-references, and later narrative connections, place them mainly in the post-reading output unless the user asks for them before reading.
- Do not auto-recommend pastors. Use only the pastor names or links the user provides. If same-name confusion is possible, ask for confirmation before summarizing.
- If a source cannot be verified, mark it as `需要人工确认` and keep it out of firm conclusions.
- If the user's interpretation may not fit the passage, gently flag the issue before rewriting.
- Save history only when the user asks, or when the current project workflow clearly requests a history record. Use local files under `history/`; never upload private history.

## Output Modes

Choose the closest mode from the user's request:

1. **读经前背景**: passage text, historical setting, context, key people/places, geography or route, questions to watch while reading.
2. **读经后总结与试卷**: plain summary, key observations, misunderstandings to avoid, cross-references, Markdown quiz paper with answer key.
3. **指定牧师讲道整理**: verify the pastor identity, find sermons on the same passage, summarize only readable/watchable material.
4. **小组转写稿总结**: process Get笔记 or other transcript text, separate speakers when labels exist, summarize themes, questions, and follow-ups.
5. **分享前短提纲**: ask for the user's real experience or pressure point first, then produce a short outline for natural spoken sharing.
6. **历史记录**: create a local Markdown record using the repository template and keep private content out of public examples.

## Style

- Use short, direct Chinese by default when the user writes Chinese.
- Explain necessary technical terms in plain language.
- Avoid ornate devotional language and over-polished slogans.
- For sharing outlines, use this shape: what happened in the passage, what it means, where it touches daily pressure, one honest closing reminder.
- Keep quiz questions fair: test main meaning and attention to the passage, not obscure trivia.
