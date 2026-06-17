#!/usr/bin/env python3
"""Render a Bible study package from structured JSON into stable HTML pages."""

from __future__ import annotations

import argparse
import html
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


FORBIDDEN_PAGE_TEXT = [
    "这是给不会电脑的人用的",
    "请打开 outputs/open.html",
    "如果你不知道怎么打开",
    "这是测试产品",
    "使用提示",
    "Markdown 文件",
    "编码问题",
    "电脑小白",
]

FORBIDDEN_QUIZ_CHOICES = ["以上皆是", "以上都对", "以上都不对", "无法判断"]
PREFERRED_QUIZ_TIERS = {
    "结构观察",
    "经文依据",
    "关系辨析",
    "主题理解",
    "应用分辨",
    "整段综合",
}
QUIZ_TIER_ALIASES = {
    "辨析判断": "关系辨析",
    "综合观察": "整段综合",
}
SIMPLE_QUIZ_TIERS = {"基础理解", "热身事实", "事实回忆", "记忆题"}


class PackageError(Exception):
    pass


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("：", "-").replace(":", "-").replace("章", "").replace("节", "")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "study-package"


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def paragraphs(value: Any) -> str:
    parts: list[str] = []
    for item in as_list(value):
        if isinstance(item, dict):
            title = item.get("title")
            text = item.get("text") or item.get("body") or item.get("content") or ""
            if title:
                parts.append(f"<p><strong>{esc(title)}</strong> {esc(text)}</p>")
            elif text:
                parts.append(f"<p>{esc(text)}</p>")
        else:
            chunks = [chunk.strip() for chunk in str(item).split("\n\n") if chunk.strip()]
            parts.extend(f"<p>{esc(chunk)}</p>" for chunk in chunks)
    return "\n".join(parts) or "<p>需要补充。</p>"


def list_block(items: Any, ordered: bool = False) -> str:
    values = [item for item in as_list(items) if str(item).strip()]
    tag = "ol" if ordered else "ul"
    if not values:
        return "<p>需要补充。</p>"
    body = "\n".join(f"<li>{esc(item)}</li>" for item in values)
    return f"<{tag}>\n{body}\n</{tag}>"


def source_link(source: dict[str, Any]) -> str:
    title = source.get("title") or source.get("name") or source.get("url") or "来源"
    url = source.get("url")
    note = source.get("note")
    status = "已核对" if source.get("verified") else "需要人工确认"
    if url:
        link = f'<a href="{esc(url)}">{esc(title)}</a>'
    else:
        link = esc(title)
    extra = f"：{esc(note)}" if note else ""
    return f"{link}<span class=\"source-status\">{esc(status)}</span>{extra}"


def sources_block(sources: Any) -> str:
    values = [item for item in as_list(sources) if isinstance(item, dict)]
    if not values:
        return "<p>需要人工确认。</p>"
    return "<ul>\n" + "\n".join(f"<li>{source_link(item)}</li>" for item in values) + "\n</ul>"


def diagram_block(diagram: Any) -> str:
    if not diagram:
        return '<div class="note">本段没有必须绘制的路线图。</div>'
    if isinstance(diagram, str):
        return f'<div class="note">{esc(diagram)}</div>'
    if not isinstance(diagram, dict):
        return '<div class="note">本段没有必须绘制的路线图。</div>'

    label = diagram.get("label") or "示意图"
    nodes = [str(item) for item in as_list(diagram.get("nodes")) if str(item).strip()]
    note = diagram.get("note")
    if nodes:
        route = "\n".join(f"<span>{esc(node)}</span>" for node in nodes)
        note_html = f"<p>{esc(note)}</p>" if note else ""
        return f"""
        <div class="diagram" aria-label="{esc(label)}">
          <strong>{esc(label)}</strong>
          <div class="route">{route}</div>
          {note_html}
        </div>
        """
    return f'<div class="note">{esc(note or label)}</div>'


def history_block(history: Any) -> str:
    if isinstance(history, dict):
        items = []
        if history.get("date"):
            items.append(f"日期：{history['date']}")
        if history.get("passage"):
            items.append(f"经文：{history['passage']}")
        items.extend(str(item) for item in as_list(history.get("items")))
        return list_block(items)
    return list_block(history)


def normalize_quiz(data: dict[str, Any]) -> list[dict[str, Any]]:
    quiz = data.get("quiz") or data.get("quiz_questions") or []
    normalized: list[dict[str, Any]] = []
    for raw in quiz:
        if not isinstance(raw, dict):
            raise PackageError("quiz 中每一道题都必须是对象。")
        answer = raw.get("answer")
        if answer is None:
            answer = raw.get("answer_index")
        normalized.append(
            {
                "tier": raw.get("tier") or "经文理解",
                "ref": raw.get("ref") or data.get("passage") or "",
                "question": raw.get("question") or "",
                "choices": raw.get("choices") or [],
                "answer": answer,
                "explain": raw.get("explain") or raw.get("explanation") or "",
            }
        )
    return normalized


def validate_package(data: dict[str, Any]) -> None:
    required = {
        "passage": data.get("passage"),
        "summary": data.get("summary"),
        "passage_source": data.get("passage_source"),
        "historical_background": data.get("historical_background") or data.get("sections", {}).get("historical_background"),
        "context": data.get("context") or data.get("sections", {}).get("context"),
        "post_summary": data.get("post_summary") or data.get("sections", {}).get("post_summary"),
    }
    missing = [name for name, value in required.items() if not str(value or "").strip()]
    if missing:
        raise PackageError("缺少必要字段：" + ", ".join(missing))

    sources = [item for item in as_list(data.get("sources")) if isinstance(item, dict)]
    if not sources:
        raise PackageError("查经内容至少需要一个来源。")
    for idx, source in enumerate(sources, start=1):
        if not source.get("title") and not source.get("url"):
            raise PackageError(f"第 {idx} 个来源缺少标题或链接。")
        if not source.get("url"):
            source["verified"] = False

    quiz = normalize_quiz(data)
    if not (7 <= len(quiz) <= 10):
        raise PackageError("互动选择题必须是 7 到 10 题。")
    tiers = set()
    simple_tier_count = 0
    for item in quiz:
        raw_tier = str(item.get("tier", "")).strip()
        tier = QUIZ_TIER_ALIASES.get(raw_tier, raw_tier)
        item["tier"] = tier
        tiers.add(tier)
        if tier in SIMPLE_QUIZ_TIERS:
            simple_tier_count += 1
    deep_tiers = tiers & PREFERRED_QUIZ_TIERS
    if len(deep_tiers) < 4:
        raise PackageError("互动题至少需要 4 种较深层级，例如结构观察、经文依据、关系辨析、主题理解、应用分辨、整段综合。")
    if simple_tier_count > 1:
        raise PackageError("互动题最多只能有 1 题简单热身或事实回忆，不能连续出送分题。")
    for index, item in enumerate(quiz, start=1):
        choices = item["choices"]
        if len(choices) != 4:
            raise PackageError(f"第 {index} 题必须有 4 个选项。")
        if len(set(map(str, choices))) != 4:
            raise PackageError(f"第 {index} 题有重复选项。")
        if any(bad in str(choice) for choice in choices for bad in FORBIDDEN_QUIZ_CHOICES):
            raise PackageError(f"第 {index} 题含有偷懒选项。")
        if not isinstance(item["answer"], int) or not (0 <= item["answer"] < 4):
            raise PackageError(f"第 {index} 题答案索引不正确。")
        if len(str(item["question"]).strip()) < 18:
            raise PackageError(f"第 {index} 题题干太短。")
        if min(len(str(choice).strip()) for choice in choices) < 8:
            raise PackageError(f"第 {index} 题存在过短选项，容易显得幼稚。")
        if len(str(item["explain"]).strip()) < 36:
            raise PackageError(f"第 {index} 题解析太短，必须说明经文大意。")

    data["quiz"] = quiz


def page_shell(title: str, body: str, extra_script: str = "") -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>
    :root {{
      --bg: #f7f8fb;
      --panel: rgba(255, 255, 255, 0.86);
      --panel-strong: #ffffff;
      --ink: #111827;
      --muted: #5f6b7a;
      --line: rgba(17, 24, 39, 0.12);
      --teal: #176b6b;
      --blue: #3457d5;
      --amber: #a86612;
      --ok: #1f7a4d;
      --ok-soft: #e7f7ef;
      --bad: #b42318;
      --bad-soft: #fff0ed;
      --gold: #a15c07;
      --gold-soft: #fff7e6;
      --green-soft: rgba(23, 107, 107, 0.10);
      --blue-soft: rgba(52, 87, 213, 0.10);
      --amber-soft: rgba(168, 102, 18, 0.12);
      --shadow: 0 22px 64px rgba(20, 30, 48, 0.11);
      --soft-shadow: 0 12px 34px rgba(20, 30, 48, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background:
        linear-gradient(140deg, rgba(52, 87, 213, 0.10), transparent 36%),
        linear-gradient(230deg, rgba(23, 107, 107, 0.12), transparent 42%),
        linear-gradient(180deg, #fbfcff 0%, var(--bg) 58%, #fffaf1 100%);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
      line-height: 1.66;
    }}
    a {{ color: inherit; }}
    .page {{ width: min(1180px, calc(100% - 32px)); margin: 0 auto; padding: 34px 0 64px; }}
    .hero {{
      position: relative;
      overflow: hidden;
      margin-bottom: 18px;
      padding: clamp(28px, 5vw, 52px);
      border: 1px solid var(--line);
      border-radius: 8px;
      background:
        linear-gradient(145deg, rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.72)),
        linear-gradient(125deg, var(--green-soft), var(--blue-soft), var(--amber-soft));
      box-shadow: var(--shadow);
      backdrop-filter: blur(18px);
    }}
    .hero::after {{
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(110deg, transparent 0%, rgba(255, 255, 255, 0.68) 44%, transparent 68%);
      transform: translateX(-120%);
      animation: light-sweep 7s ease-in-out infinite;
      pointer-events: none;
    }}
    .eyebrow {{
      display: inline-flex;
      min-height: 28px;
      margin: 0 0 14px;
      padding: 3px 10px;
      border: 1px solid rgba(23, 107, 107, 0.24);
      border-radius: 999px;
      color: var(--teal);
      background: rgba(23, 107, 107, 0.08);
      font-size: 13px;
      font-weight: 850;
    }}
    h1 {{ position: relative; margin: 0; max-width: 840px; font-size: clamp(34px, 6vw, 68px); line-height: 1.04; letter-spacing: 0; }}
    h2 {{ margin: 0 0 10px; font-size: clamp(22px, 3vw, 30px); line-height: 1.2; letter-spacing: 0; }}
    h3 {{ margin: 0 0 8px; font-size: 18px; letter-spacing: 0; }}
    p {{ margin: 8px 0; }}
    ul, ol {{ margin: 8px 0; padding-left: 22px; }}
    li + li {{ margin-top: 6px; }}
    .lead {{ position: relative; max-width: 780px; margin: 18px 0 0; color: var(--muted); font-size: clamp(16px, 2vw, 20px); }}
    .actions {{ position: relative; display: flex; flex-wrap: wrap; gap: 10px; margin-top: 26px; }}
    .button, button {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 46px;
      padding: 0 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.78);
      box-shadow: 0 8px 24px rgba(20, 30, 48, 0.07);
      color: var(--ink);
      text-decoration: none;
      font: inherit;
      font-weight: 850;
      cursor: pointer;
      transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }}
    .button.primary, button.primary {{ border-color: rgba(23, 107, 107, 0.42); background: linear-gradient(135deg, #176b6b, #244ea8); color: #fff; }}
    .button:hover, button:hover {{ transform: translateY(-2px); border-color: rgba(52, 87, 213, 0.40); box-shadow: var(--soft-shadow); }}
    .flow {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-top: 18px; }}
    .step {{ display: block; color: var(--ink); text-decoration: none; transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease; }}
    .step:hover {{ transform: translateY(-3px); border-color: rgba(52, 87, 213, 0.30); box-shadow: 0 18px 46px rgba(20, 30, 48, 0.11); }}
    .layout {{ display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 18px; align-items: start; }}
    .index {{
      position: sticky;
      top: 16px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.76);
      box-shadow: var(--soft-shadow);
      backdrop-filter: blur(16px);
    }}
    .index h2 {{ margin: 0 0 12px; font-size: 15px; }}
    .index a {{ display: grid; gap: 2px; padding: 10px; border-radius: 8px; color: var(--muted); text-decoration: none; transition: background 160ms ease, color 160ms ease, transform 160ms ease; }}
    .index a + a {{ margin-top: 4px; }}
    .index a:hover, .index a.active {{ background: rgba(23, 107, 107, 0.08); color: var(--ink); transform: translateX(2px); }}
    .index small {{ color: var(--teal); font-weight: 850; }}
    .content, .questions {{ display: grid; gap: 14px; }}
    .card, .step, .question, .summary {{
      position: relative;
      overflow: hidden;
      padding: clamp(18px, 3vw, 28px);
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: var(--soft-shadow);
      backdrop-filter: blur(16px);
    }}
    .card {{ opacity: 0; transform: translateY(14px); transition: opacity 420ms ease, transform 420ms ease, border-color 220ms ease, box-shadow 220ms ease; }}
    .card.visible {{ opacity: 1; transform: translateY(0); }}
    .card:hover, .question:hover {{ border-color: rgba(52, 87, 213, 0.24); box-shadow: 0 18px 46px rgba(20, 30, 48, 0.11); }}
    .card::before, .step::before {{ content: ""; position: absolute; inset: 0 0 auto; height: 3px; background: linear-gradient(90deg, var(--teal), var(--blue), var(--amber)); }}
    .stage, .pill, .source-status {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      margin: 0 6px 6px 0;
      padding: 2px 8px;
      border-radius: 999px;
      background: var(--blue-soft);
      color: var(--blue);
      font-size: 12px;
      font-weight: 850;
    }}
    .source-status {{ margin-left: 8px; color: var(--teal); background: var(--green-soft); }}
    .note, .diagram {{
      margin-top: 12px;
      padding: 14px;
      border: 1px solid rgba(23, 107, 107, 0.18);
      border-radius: 8px;
      background: rgba(23, 107, 107, 0.08);
      color: #124f50;
      font-weight: 750;
    }}
    .diagram {{ display: grid; gap: 10px; color: var(--ink); font-weight: 700; }}
    .route {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 8px; align-items: stretch; }}
    .route span {{ display: grid; place-items: center; min-height: 58px; padding: 8px; border: 1px solid var(--line); border-radius: 8px; background: var(--panel-strong); text-align: center; font-size: 14px; }}
    .route span:not(:last-child)::after {{ content: "→"; margin-left: 8px; color: var(--teal); }}
    .toolbar {{ position: sticky; top: 0; z-index: 2; display: grid; grid-template-columns: 1fr auto auto; gap: 10px; align-items: center; padding: 14px 0; background: color-mix(in srgb, var(--bg) 92%, transparent); backdrop-filter: blur(10px); border-bottom: 1px solid var(--line); }}
    .progress-label {{ display: flex; justify-content: space-between; gap: 12px; color: var(--muted); font-size: 13px; margin-bottom: 6px; }}
    .progress {{ height: 8px; overflow: hidden; border-radius: 999px; background: #e4e7ec; }}
    .progress span {{ display: block; width: 0; height: 100%; background: var(--teal); transition: width 180ms ease; }}
    .choices {{ display: grid; gap: 8px; margin-top: 12px; }}
    label {{ display: grid; grid-template-columns: 32px 1fr; gap: 10px; align-items: start; min-height: 48px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: rgba(255, 255, 255, 0.86); cursor: pointer; transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease; }}
    label:hover {{ transform: translateY(-1px); border-color: rgba(23, 107, 107, 0.28); box-shadow: 0 8px 22px rgba(20, 30, 48, 0.07); }}
    input {{ width: 18px; height: 18px; margin: 3px 0 0 4px; accent-color: var(--teal); }}
    .feedback {{ display: none; margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--line); }}
    .checked .feedback {{ display: block; }}
    .answer {{ font-weight: 850; }}
    .summary {{ display: none; margin: 20px 0 10px; }}
    .summary.visible {{ display: grid; gap: 6px; }}
    .question.correct {{ border-color: color-mix(in srgb, var(--ok) 48%, var(--line)); background: var(--ok-soft); }}
    .question.wrong {{ border-color: color-mix(in srgb, var(--bad) 48%, var(--line)); background: var(--bad-soft); }}
    .question.unanswered {{ border-color: color-mix(in srgb, var(--gold) 50%, var(--line)); background: var(--gold-soft); }}
    @keyframes light-sweep {{ 0%, 55% {{ transform: translateX(-120%); opacity: 0; }} 68% {{ opacity: 0.75; }} 100% {{ transform: translateX(120%); opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      *, *::before, *::after {{ animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; }}
      .card {{ opacity: 1; transform: none; }}
    }}
    @media (max-width: 900px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .index {{ position: static; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px; }}
      .index h2 {{ grid-column: 1 / -1; }}
      .flow {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 640px) {{
      .page {{ width: min(100% - 20px, 1180px); padding-top: 18px; }}
      .hero {{ padding: 24px; }}
      .actions, .toolbar, .index, .flow, .route {{ display: grid; grid-template-columns: 1fr; }}
      .button, button {{ width: 100%; }}
      .route span:not(:last-child)::after {{ content: "↓"; display: block; margin: 5px 0 0; }}
    }}
  </style>
</head>
<body>
{body}
{extra_script}
</body>
</html>
"""


def render_entry(data: dict[str, Any], files: dict[str, str]) -> str:
    steps = [
        ("01", "读经前", "历史背景、上下文、重要人物与地理关系。", f'{files["study"]}#source'),
        ("02", "讲道角度", "David Pawson 或指定牧师可核对的讲道方向。", f'{files["study"]}#sermon'),
        ("03", "读经后", "短总结、前后文呼应、旧约或新约线索。", f'{files["study"]}#summary'),
        ("04", "互动题", "选择题、自动检查、错题解释经文大意。", files["quiz"]),
    ]
    flow = "\n".join(
        f'<a class="step" href="{esc(href)}"><span class="stage">{num}</span><h2>{esc(title)}</h2><p>{esc(text)}</p></a>'
        for num, title, text, href in steps
    )
    body = f"""
  <main class="page">
    <section class="hero" aria-label="查经入口">
      <p class="eyebrow">阅读流程</p>
      <h1>{esc(data["passage"])}</h1>
      <p class="lead">{esc(data["summary"])}</p>
    </section>
    <section class="flow" aria-label="四个查经入口">{flow}</section>
  </main>
"""
    return page_shell(data["passage"], body)


def section_value(data: dict[str, Any], name: str) -> Any:
    return data.get(name) or data.get("sections", {}).get(name)


def render_study(data: dict[str, Any], files: dict[str, str]) -> str:
    sections = [
        ("source", "读经前", "经文范围与来源", paragraphs(data.get("passage_source"))),
        ("background", "读经前", "历史背景", paragraphs(section_value(data, "historical_background"))),
        ("context", "读经前", "上下文", paragraphs(section_value(data, "context"))),
        (
            "geography",
            "读经前",
            "重要人物、地名与地理关系",
            paragraphs(section_value(data, "geography")) + diagram_block(data.get("geography_diagram")),
        ),
        ("sermon", "讲道角度", "David Pawson / 指定牧师讲道角度", paragraphs(section_value(data, "sermon_angle"))),
        ("watch", "阅读中", "阅读时留意的问题", list_block(data.get("reading_questions"), ordered=True)),
        ("summary", "读经后", "读后短总结", paragraphs(section_value(data, "post_summary"))),
        ("echoes", "读经后", "前后文、旧约或新约呼应", list_block(data.get("cross_references"))),
        (
            "quiz",
            "练习",
            "互动题",
            f'<p>{esc(data.get("quiz_intro") or "题目围绕经文大意、结构、关系和应用判断。")}</p><p><a class="button primary" href="{esc(files["quiz"])}">开始互动题</a></p>',
        ),
        ("sources", "核对", "来源", sources_block(data.get("sources"))),
        ("history", "留存", "历史短摘要", history_block(data.get("history_summary"))),
    ]
    index = "\n".join(
        f'<a href="#{sid}"><small>{str(i).zfill(2)} {esc(stage)}</small><span>{esc(title)}</span></a>'
        for i, (sid, stage, title, _) in enumerate(sections, start=1)
    )
    cards = "\n".join(
        f'<section class="card" id="{sid}"><span class="stage">{esc(stage)}</span><h2>{esc(title)}</h2>{content}</section>'
        for sid, stage, title, content in sections
    )
    body = f"""
  <main class="page">
    <header class="hero">
      <p class="eyebrow">查经内容</p>
      <h1>{esc(data["passage"])}</h1>
      <p class="lead">{esc(data["summary"])}</p>
      <nav class="actions" aria-label="查经包主要入口">
        <a class="button" href="{esc(files["entry"])}">返回入口页</a>
      </nav>
    </header>
    <div class="layout">
      <nav class="index" aria-label="内容索引"><h2>内容索引</h2>{index}</nav>
      <div class="content">{cards}</div>
    </div>
  </main>
"""
    script = """
  <script>
    const cards = Array.from(document.querySelectorAll('.card'));
    const links = Array.from(document.querySelectorAll('.index a'));
    const linkById = new Map(links.map((link) => [link.getAttribute('href').slice(1), link]));
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('visible');
      });
    }, { threshold: 0.12 });
    const activeObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((link) => link.classList.remove('active'));
        const active = linkById.get(entry.target.id);
        if (active) active.classList.add('active');
      });
    }, { rootMargin: '-30% 0px -55% 0px', threshold: 0.01 });
    cards.forEach((card) => {
      revealObserver.observe(card);
      activeObserver.observe(card);
    });
  </script>
"""
    return page_shell(f'{data["passage"]} 查经内容', body, script)


def render_quiz(data: dict[str, Any], files: dict[str, str]) -> str:
    quiz_json = json.dumps(data["quiz"], ensure_ascii=False).replace("</", "<\\/")
    body = f"""
  <main class="page">
    <header class="hero">
      <p class="eyebrow">互动选择题</p>
      <h1>{esc(data["passage"])} 互动选择题</h1>
      <p class="lead">只做选择题，不考背诵。点“检查答案”后会显示得分、错题、正确答案和经文大意解析。</p>
      <nav class="actions" aria-label="返回查经包">
        <a class="button" href="{esc(files["entry"])}">返回入口页</a>
        <a class="button" href="{esc(files["study"])}">查看查经内容</a>
      </nav>
    </header>
    <section class="toolbar" aria-label="测验工具栏">
      <div>
        <div class="progress-label">
          <span id="answeredText">已答 0 / 0</span>
          <span id="scoreText">未检查</span>
        </div>
        <div class="progress" aria-hidden="true"><span id="progressBar"></span></div>
      </div>
      <button class="primary" id="checkButton" type="button">检查答案</button>
      <button id="resetButton" type="button">重做</button>
    </section>
    <section class="summary" id="summary" aria-live="polite"></section>
    <section class="questions" id="questions"></section>
  </main>
"""
    script = f"""
  <script>
    const quiz = {quiz_json};
    const questionsEl = document.querySelector("#questions");
    const summaryEl = document.querySelector("#summary");
    const progressBar = document.querySelector("#progressBar");
    const answeredText = document.querySelector("#answeredText");
    const scoreText = document.querySelector("#scoreText");
    function renderQuiz() {{
      questionsEl.innerHTML = quiz.map((item, index) => {{
        const choices = item.choices.map((choice, choiceIndex) => `
          <label>
            <input type="radio" name="q${{index}}" value="${{choiceIndex}}">
            <span>${{String.fromCharCode(65 + choiceIndex)}}. ${{choice}}</span>
          </label>
        `).join("");
        return `
          <article class="question" id="q${{index}}">
            <div>
              <span class="pill">${{item.tier}}</span>
              <span class="pill">${{item.ref}}</span>
              <span class="pill">第 ${{index + 1}} 题</span>
            </div>
            <h2>${{item.question}}</h2>
            <div class="choices">${{choices}}</div>
            <div class="feedback" id="f${{index}}"></div>
          </article>
        `;
      }}).join("");
      updateProgress();
    }}
    function getSelected(index) {{
      const selected = document.querySelector(`input[name="q${{index}}"]:checked`);
      return selected ? Number(selected.value) : null;
    }}
    function updateProgress() {{
      const answered = quiz.filter((_, index) => getSelected(index) !== null).length;
      answeredText.textContent = `已答 ${{answered}} / ${{quiz.length}}`;
      progressBar.style.width = `${{Math.round((answered / quiz.length) * 100)}}%`;
    }}
    function checkAnswers() {{
      let score = 0;
      let unanswered = 0;
      quiz.forEach((item, index) => {{
        const selected = getSelected(index);
        const card = document.querySelector(`#q${{index}}`);
        const feedback = document.querySelector(`#f${{index}}`);
        card.classList.remove("correct", "wrong", "unanswered");
        card.classList.add("checked");
        if (selected === null) {{
          unanswered += 1;
          card.classList.add("unanswered");
          feedback.innerHTML = `<p class="answer">还没作答。正确答案：${{String.fromCharCode(65 + item.answer)}}</p><p>${{item.explain}}</p>`;
          return;
        }}
        if (selected === item.answer) {{
          score += 1;
          card.classList.add("correct");
          feedback.innerHTML = `<p class="answer">答对了。正确答案：${{String.fromCharCode(65 + item.answer)}}</p><p>${{item.explain}}</p>`;
        }} else {{
          card.classList.add("wrong");
          feedback.innerHTML = `<p class="answer">这题错了。你选了 ${{String.fromCharCode(65 + selected)}}，正确答案是 ${{String.fromCharCode(65 + item.answer)}}。</p><p>${{item.explain}}</p>`;
        }}
      }});
      scoreText.textContent = `得分 ${{score}} / ${{quiz.length}}`;
      summaryEl.classList.add("visible");
      summaryEl.innerHTML = `<strong>得分：${{score}} / ${{quiz.length}}</strong><span>未作答：${{unanswered}} 题。错题和解析已经显示在对应题目下方。</span>`;
      summaryEl.scrollIntoView({{ behavior: "smooth", block: "nearest" }});
    }}
    function resetQuiz() {{
      document.querySelectorAll("input[type='radio']").forEach((input) => {{ input.checked = false; }});
      document.querySelectorAll(".question").forEach((card) => {{ card.classList.remove("checked", "correct", "wrong", "unanswered"); }});
      document.querySelectorAll(".feedback").forEach((feedback) => {{ feedback.innerHTML = ""; }});
      summaryEl.classList.remove("visible");
      summaryEl.innerHTML = "";
      scoreText.textContent = "未检查";
      updateProgress();
      window.scrollTo({{ top: 0, behavior: "smooth" }});
    }}
    document.addEventListener("change", (event) => {{
      if (event.target.matches("input[type='radio']")) updateProgress();
    }});
    document.querySelector("#checkButton").addEventListener("click", checkAnswers);
    document.querySelector("#resetButton").addEventListener("click", resetQuiz);
    renderQuiz();
  </script>
"""
    return page_shell(f'{data["passage"]} 互动选择题', body, script)


def render_sources(data: dict[str, Any], files: dict[str, str]) -> str:
    body = f"""
  <main class="page">
    <header class="hero">
      <p class="eyebrow">来源</p>
      <h1>{esc(data["passage"])} 来源</h1>
      <nav class="actions" aria-label="辅助页面导航">
        <a class="button" href="{esc(files["entry"])}">返回入口页</a>
        <a class="button" href="{esc(files["study"])}">查看查经内容</a>
        <a class="button" href="{esc(files["quiz"])}">开始互动题</a>
      </nav>
    </header>
    <section class="card visible"><h2>来源</h2>{sources_block(data.get("sources"))}</section>
  </main>
"""
    return page_shell(f'{data["passage"]} 来源', body)


def render_history(data: dict[str, Any], files: dict[str, str]) -> str:
    body = f"""
  <main class="page">
    <header class="hero">
      <p class="eyebrow">历史短摘要</p>
      <h1>{esc(data["passage"])} 历史短摘要</h1>
      <nav class="actions" aria-label="辅助页面导航">
        <a class="button" href="{esc(files["entry"])}">返回入口页</a>
        <a class="button" href="{esc(files["study"])}">查看查经内容</a>
        <a class="button" href="{esc(files["quiz"])}">开始互动题</a>
      </nav>
    </header>
    <section class="card visible">{history_block(data.get("history_summary"))}</section>
  </main>
"""
    return page_shell(f'{data["passage"]} 历史短摘要', body)


def assert_no_forbidden_text(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_PAGE_TEXT:
            if forbidden in text:
                raise PackageError(f"{path} 包含不该出现在成品页里的文字：{forbidden}")


def write_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def open_entry(path: Path) -> None:
    system = platform.system()
    try:
        if system == "Darwin":
            try:
                subprocess.run(["open", "-a", "Safari", str(path)], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["open", str(path)], check=True)
        elif system == "Windows":
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            subprocess.run(["xdg-open", str(path)], check=True)
        print(f"已打开入口页：{path}")
    except Exception as exc:  # pragma: no cover - depends on user OS
        print(f"浏览器没有自动打开。请打开 {path}，这就是入口页。原因：{exc}")


def render(data: dict[str, Any], out_dir: Path) -> dict[str, Path]:
    validate_package(data)
    slug = data.get("slug") or slugify(data["passage"])
    files = {
        "entry": "open.html",
        "study": f"{slug}-study-package.html",
        "quiz": f"{slug}-quiz.html",
        "sources": f"{slug}-sources.html",
        "history": f"{slug}-history-summary.html",
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "data": out_dir / f"{slug}-package.json",
        "entry": out_dir / files["entry"],
        "study": out_dir / files["study"],
        "quiz": out_dir / files["quiz"],
        "sources": out_dir / files["sources"],
        "history": out_dir / files["history"],
    }
    write_file(paths["data"], json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    write_file(paths["entry"], render_entry(data, files))
    write_file(paths["study"], render_study(data, files))
    write_file(paths["quiz"], render_quiz(data, files))
    write_file(paths["sources"], render_sources(data, files))
    write_file(paths["history"], render_history(data, files))
    assert_no_forbidden_text([path for name, path in paths.items() if name != "data"])
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Bible study package from JSON.")
    parser.add_argument("--data", required=True, help="Path to package JSON data.")
    parser.add_argument("--out", default="outputs", help="Output directory.")
    parser.add_argument("--open", action="store_true", help="Open the generated entry page.")
    args = parser.parse_args()

    data_path = Path(args.data)
    out_dir = Path(args.out)
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise PackageError("数据文件根节点必须是对象。")
        paths = render(data, out_dir)
        print("生成完成：")
        for name, path in paths.items():
            print(f"- {name}: {path}")
        if args.open:
            open_entry(paths["entry"])
        return 0
    except (OSError, json.JSONDecodeError, PackageError) as exc:
        print(f"生成失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
