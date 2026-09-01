#!/usr/bin/env python3
import datetime
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "contrib-heatmap.svg")

# GitHub-ish green ramp: empty -> brightest. Level 5 is a brighter neon top end.
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 11
GAP = 3
STEP = CELL + GAP
PAD = 20
LEFT_LABEL_W = 28
TOP_LABEL_H = 22
TITLEBAR_H = 28

BG = "#0d1117"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#e6edf3"
GREEN = "#39d353"

# Reveal timing (one-shot diagonal cascade)
COL_T = 0.015
ROW_T = 0.035
CELL_DUR = 0.35


def level_for(count):
    if count == 0:
        return 0
    if count <= 3:
        return 1
    if count <= 8:
        return 2
    if count <= 18:
        return 3
    if count <= 35:
        return 4
    return 5


def build_grid(days):
    if not days:
        return []
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7  # sunday=0
    grid = []
    col = [None] * lead_pad
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid


def render():
    if not os.path.exists(IN_PATH):
        raise FileNotFoundError(f"{IN_PATH} not found.")

    with open(IN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total = data.get("total", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    daily_avg = data.get("daily_avg", 0)
    best_day = data.get("best_day", {"count": 0, "date": ""})

    grid = build_grid(days)
    n_cols = len(grid)
    art_w = n_cols * STEP
    art_h = 7 * STEP

    month_labels = []
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = datetime.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD
    stats_h = 42
    canvas_h = TITLEBAR_H + TOP_LABEL_H + art_h + stats_h + PAD

    # Day of week labels
    day_labels = [
        (1, "Mon"),
        (3, "Wed"),
        (5, "Fri")
    ]

    rects = []
    for ci, col in enumerate(grid):
        x = PAD + LEFT_LABEL_W + ci * STEP
        for ri, cell in enumerate(col):
            if cell is None:
                continue
            date_str, count, lvl = cell
            y = TITLEBAR_H + TOP_LABEL_H + ri * STEP
            delay = ci * COL_T + ri * ROW_T
            fill = PALETTE[lvl]
            rects.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{fill}" style="animation-delay:{delay:.3f}s;"><title>{date_str}: {count} contributions</title></rect>'
            )

    month_svg = []
    for ci, label in month_labels:
        mx = PAD + LEFT_LABEL_W + ci * STEP
        month_svg.append(f'<text x="{mx}" y="{TITLEBAR_H + TOP_LABEL_H - 8}" class="muted-text" font-size="10">{label}</text>')

    day_svg = []
    for ri, label in day_labels:
        dy = TITLEBAR_H + TOP_LABEL_H + ri * STEP + CELL - 2
        day_svg.append(f'<text x="{PAD}" y="{dy}" class="muted-text" font-size="10">{label}</text>')

    footer_y = TITLEBAR_H + TOP_LABEL_H + art_h + 24

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}" fill="none">
  <style>
    .bg {{ fill: {BG}; stroke: {FRAME}; stroke-width: 1; rx: 8px; }}
    .title-bar {{ fill: #161b22; }}
    .dot-red {{ fill: #ff5f56; }}
    .dot-yellow {{ fill: #ffbd2e; }}
    .dot-green {{ fill: #27c93f; }}
    .term-title {{ fill: {MUTED}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}
    .muted-text {{ fill: {MUTED}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    .stat-text {{ fill: {TEXT}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}
    .stat-val {{ fill: {GREEN}; font-weight: bold; }}
    
    .cell {{
      opacity: 0;
      transform: translateY(4px);
      animation: cellIn {CELL_DUR}s ease forwards;
    }}
    @keyframes cellIn {{
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}
  </style>

  <!-- Background Card -->
  <rect width="{canvas_w}" height="{canvas_h}" class="bg" />

  <!-- Terminal Window Bar -->
  <path d="M 0 8 C 0 3.58 3.58 0 8 0 L {canvas_w-8} 0 C {canvas_w-3.58} 0 {canvas_w} 3.58 {canvas_w} 8 L {canvas_w} {TITLEBAR_H} L 0 {TITLEBAR_H} Z" class="title-bar" />
  <circle cx="16" cy="14" r="5" class="dot-red" />
  <circle cx="32" cy="14" r="5" class="dot-yellow" />
  <circle cx="48" cy="14" r="5" class="dot-green" />
  <text x="{canvas_w // 2}" y="18" text-anchor="middle" class="term-title">161seconds@github: ~ (contributions)</text>

  <!-- Labels -->
  {''.join(month_svg)}
  {''.join(day_svg)}

  <!-- Grid Cells -->
  {''.join(rects)}

  <!-- Footer Stats -->
  <text x="{PAD + LEFT_LABEL_W}" y="{footer_y}" class="stat-text">
    Total: <tspan class="stat-val">{total:,}</tspan> | Current streak: <tspan class="stat-val">{current_streak} days</tspan> | Longest: <tspan class="stat-val">{longest_streak} days</tspan> | Avg: <tspan class="stat-val">{daily_avg}/day</tspan>
  </text>

  <!-- Legend -->
  <g transform="translate({canvas_w - PAD - 155}, {footer_y - 10})">
    <text x="-30" y="9" class="muted-text" font-size="10">Less</text>
    {''.join([f'<rect x="{i*14}" y="0" width="{CELL-1}" height="{CELL-1}" rx="2" fill="{c}" />' for i, c in enumerate(PALETTE)])}
    <text x="{len(PALETTE)*14 + 6}" y="9" class="muted-text" font-size="10">More</text>
  </g>
</svg>'''

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[OK] Successfully rendered {OUT_PATH}")


if __name__ == "__main__":
    render()
