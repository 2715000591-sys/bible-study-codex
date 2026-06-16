# Package Data Contract

Use this contract when generating a full study package. The stable renderer expects one JSON file and handles the HTML layout.

## Render command

In this repository, run:

```bash
python3 scripts/render-package.py --data outputs/<passage-slug>-package.json --out outputs --open
```

If using the installed skill outside the repository, run the bundled renderer relative to the skill folder:

```bash
python3 scripts/render_package.py --data <package-data.json> --out outputs --open
```

Use `--open` for normal user delivery. Omit `--open` only during verification or automated tests.

## Required fields

The JSON object must include:

- `passage`: Chinese passage label, such as `创世记1章到3章`
- `slug`: ASCII file slug, such as `genesis-1-3`
- `summary`: short content-focused summary
- `passage_source`: passage range and translation/source note
- `historical_background`: must be real study content, not a file note
- `context`
- `geography`
- `geography_diagram`: string or object with `label`, `nodes`, and optional `note`
- `sermon_angle`
- `reading_questions`: array of short questions
- `post_summary`
- `cross_references`: array
- `sources`: array of source objects
- `history_summary`: object or array
- `quiz`: 7-10 multiple-choice question objects

## Source object

Each source object should use:

```json
{
  "title": "Source title",
  "url": "https://example.com",
  "note": "What this source supports",
  "verified": true
}
```

If a source is useful but not fully verified, set `verified` to `false` and write the uncertainty in `note`.

## Quiz object

Each quiz item must use:

```json
{
  "tier": "结构观察",
  "ref": "创1-2",
  "question": "Question text",
  "choices": ["A", "B", "C", "D"],
  "answer": 0,
  "explain": "Explain the passage direction in plain words."
}
```

Rules:

- Use 7-10 questions.
- Use exactly 4 choices.
- Use at least 4 tiers across the quiz, such as `结构观察`, `经文依据`, `辨析判断`, `应用分辨`, `综合观察`.
- Do not use lazy choices like `以上皆是`, `以上都对`, `以上都不对`, or `无法判断`.
- Explanations must say what the passage basically says, not only that the selected answer is wrong.

## Output files

The renderer generates:

- `outputs/open.html`
- `outputs/<slug>-study-package.html`
- `outputs/<slug>-quiz.html`
- `outputs/<slug>-sources.html`
- `outputs/<slug>-history-summary.html`

The entry page is always the normal user-facing starting point.
