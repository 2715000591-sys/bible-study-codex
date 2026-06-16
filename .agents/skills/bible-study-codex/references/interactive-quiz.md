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
- comparing close but different claims
- application discernment
- whole-passage synthesis

Do not raise difficulty through:

- obscure details
- verse-number memorization
- trick wording
- disputed theology as a scored answer
- asking people to recite phrases from memory

Avoid childish questions such as "who created the heavens and earth" when the passage wording gives it away too directly. Prefer questions that ask what the verse establishes, how one verse prepares the next, or which summary best fits the passage.

Hard quality gates:

- Every question must have exactly 4 choices.
- Use at least 4 tiers across the quiz.
- Do not use lazy choices such as `以上皆是`, `以上都对`, `以上都不对`, or `无法判断`.
- Distractors must be plausible enough to test reading, but clearly wrong from the passage.
- Do not score a question if the correct answer depends on a disputed interpretation or a denominational preference.
- Every explanation must say what the passage basically says and why the correct answer follows.

## Question mix

For 8 questions, use roughly:

- 2 structure or main-idea questions
- 2 textual-basis questions
- 2 comparison/discernment questions
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
