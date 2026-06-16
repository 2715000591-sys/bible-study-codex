#!/usr/bin/env python3
"""Repository wrapper for the bible-study-codex package renderer."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RENDERER = REPO_ROOT / ".agents" / "skills" / "bible-study-codex" / "scripts" / "render_package.py"

if not RENDERER.exists():
    raise SystemExit(f"找不到生成器：{RENDERER}")

sys.argv[0] = str(RENDERER)
runpy.run_path(str(RENDERER), run_name="__main__")
