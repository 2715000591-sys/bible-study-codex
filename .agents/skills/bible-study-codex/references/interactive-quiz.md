# Interactive Quiz

## Default

Generate an interactive HTML multiple-choice quiz by default for full study packages.

- Use `templates/互动选择题模板.html` when the repository is available.
- Use 7-10 questions.
- Use only multiple-choice questions.
- Do not default to a Markdown paper. Make a printable/static version only when asked.
- For full study packages, put quiz data in `outputs/<passage-slug>-package.json` and let `scripts/render-package.py` generate the HTML.

## Difficulty

Target: an ordinary group member who seriously read the passage once should score about 70%.

Raise difficulty through:

- structure observation
- textual basis
- relation discernment between close but different claims
- theme understanding
- application discernment
- whole-passage synthesis

Do not raise difficulty through:

- obscure details
- verse-number memorization
- trick wording
- disputed theology as a scored answer
- asking people to recite phrases from memory

Avoid childish questions such as "who created the heavens and earth" when the passage wording gives it away too directly. Prefer questions that ask what the verse establishes, how one verse prepares the next, or which summary best fits the passage.

Learn from public quiz patterns without copying their wording:

- BibleProject-style questions are useful for structure, repeated words, narrative design, and whole-passage movement.
- BibleBridge-style review plus quiz is useful for moving from a short concept review into scored questions.
- Common trivia apps are useful for interface habits: clear score, answer checking, short explanation, and a passage reference after each answer.
- Most simple trivia or flashcard questions are too low-level for this project. Use at most one warm-up fact question, and only when it helps the reader enter the passage.

Hard quality gates:

- Every question must have exactly 4 choices.
- Use at least 4 deeper tiers across the quiz. Preferred tiers: `结构观察`, `经文依据`, `关系辨析`, `主题理解`, `应用分辨`, `整段综合`.
- Use at most 1 simple warm-up/fact question. The default should not start with several giveaway questions.
- Do not use lazy choices such as `以上皆是`, `以上都对`, `以上都不对`, or `无法判断`.
- Distractors must be plausible enough that a rushed reader might choose them, but clearly wrong from the passage.
- Avoid joke options or options from unrelated Bible eras unless the passage itself requires comparison.
- Do not score a question if the correct answer depends on a disputed interpretation or a denominational preference.
- Every explanation must say what the passage basically says and why the correct answer follows.

## Question mix

For 8 questions, use roughly:

- 1-2 structure observation questions
- 1-2 textual-basis questions
- 1-2 relation discernment questions
- 1 theme-understanding question
- 1 application-discernment question
- 1 synthesis question

For shorter passages, keep the same logic but reduce repetition.

## Explanations

After checking answers, each question must show:

- selected answer state
- correct answer
- short explanation
- passage basis
- what the original passage is basically saying

Wrong-answer explanations must not merely say "不符合原文". Explain the passage direction in plain words.

## Scored vs discussion

Only include clear, passage-supported questions in the scored quiz.

If a question depends on denominational tradition, uncertain historical reconstruction, or a disputed interpretation, do not score it. Put it in a separate `讨论题候选` section outside the interactive quiz if useful.
