# Source Policy

## Bible text

- Default to CUV when the user gives only a passage reference.
- Treat spoken passage ranges as normal input. Normalize the range before lookup.
- Do not bundle a full Bible text inside this project.
- Prefer online lookup sources that clearly identify the translation.
- First try Bible Gateway with `version=CUV` or `version=CUVS` for CUV lookup when browsing is available.
- If a requested translation has unclear copyright status, ask the user to paste the text.

## Verification

Verify these items online before presenting them as facts:

- historical background
- date, author, audience, and setting when disputed
- geography, places, distances, travel routes, and war routes
- sermon title, preacher identity, church/channel, date, and passage covered
- video captions, transcript, or notes before summarizing sermon content

If a claim is plausible but not verified, label it `需要人工确认`.

For full study packages, every external claim group must be represented in `sources` inside the package data JSON. Use source objects with `title`, `url`, `note`, and `verified`. If the URL is missing or the source is uncertain, set `verified` to `false`.

## Diagrams and images

- If the passage naturally involves migration, travel, war routes, or major geographic movement, proactively include a diagram.
- Prefer Mermaid or a simple text route for factual clarity.
- Generate an image only when a visual map or route would genuinely help and the available model/tool can create it.
- Every diagram or generated image must be labeled `示意图`.
- Do not invent route arrows, place locations, battle movement, dates, or distances. If uncertain, mark `需要人工确认`.
- For renderer output, put factual route steps in `geography_diagram.nodes`. If the exact location or route is uncertain, say so in `geography_diagram.note`.

## Citations

- Keep citations short and practical.
- Link to original or near-original sources when possible: Bible text source, church page, official channel, seminary/article source, map/source page.
- Do not cite random reposts when an official church/channel page exists.

## Accuracy behavior

- Do not fill gaps with imagination.
- Do not turn one commentator's opinion into the passage's certain meaning.
- Do not summarize a sermon video from the title alone.
- If sources disagree, say so briefly and keep the output usable.
- If the user requests a statement that may not fit the biblical text, flag it before offering a safer wording.

## Cost and access

Assume the project itself is free. Mention possible costs only when the user needs paid APIs, paid Bible software, paid sermon databases, hosting, or a domain name.
