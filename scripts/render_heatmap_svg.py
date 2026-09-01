import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_svg():
    data_file = "data/contributions.json"
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"{data_file} not found. Run fetch_contributions.py first.")

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total = data.get("total_contributions", 0)
    streak = data.get("current_streak", 0)
    longest = data.get("longest_streak", 0)

    # 53 weeks * 7 days = 371 days maximum
    days = days[-371:] if len(days) >= 371 else days

    cell_size = 11
    cell_gap = 3
    start_x = 35
    start_y = 35

    svg_width = 860
    svg_height = 175

    rects = []
    weeks = [days[i:i+7] for i in range(0, len(days), 7)]

    for col_idx, week in enumerate(weeks):
        x = start_x + col_idx * (cell_size + cell_gap)
        for row_idx, day in enumerate(week):
            y = start_y + row_idx * (cell_size + cell_gap)
            level = min(day.get("level", 0), len(PALETTE) - 1)
            color = PALETTE[level]
            
            # Diagonal reveal delay
            delay = (col_idx * 0.015) + (row_idx * 0.025)
            
            rect = f'''<rect class="cell" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}" style="animation-delay: {delay:.3f}s;"><title>{day.get('date', '')}: {day.get('count', 0)} contributions</title></rect>'''
            rects.append(rect)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_labels = []
    num_weeks = max(len(weeks), 1)
    for i, m in enumerate(months):
        mx = start_x + int(i * (num_weeks / 12) * (cell_size + cell_gap))
        month_labels.append(f'<text x="{mx}" y="24" class="label">{m}</text>')

    day_labels = [
        f'<text x="10" y="{start_y + 1 * (cell_size + cell_gap) + 9}" class="label">Mon</text>',
        f'<text x="10" y="{start_y + 3 * (cell_size + cell_gap) + 9}" class="label">Wed</text>',
        f'<text x="10" y="{start_y + 5 * (cell_size + cell_gap) + 9}" class="label">Fri</text>',
    ]

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}" fill="none">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; rx: 8px; }}
    .label {{ fill: #7d8590; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 10px; }}
    .footer-stat {{ fill: #8b949e; font-family: "JetBrains Mono", "Courier New", monospace; font-size: 11px; }}
    .footer-highlight {{ fill: #39d353; font-weight: bold; }}
    .cell {{
      opacity: 0;
      transform: translateY(5px);
      animation: cellReveal 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    @keyframes cellReveal {{
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}
  </style>

  <!-- Background Card -->
  <rect width="{svg_width}" height="{svg_height}" class="bg" />

  <!-- Month Labels -->
  {''.join(month_labels)}

  <!-- Day Labels -->
  {''.join(day_labels)}

  <!-- Heatmap Grid -->
  {''.join(rects)}

  <!-- Footer Stats -->
  <text x="35" y="155" class="footer-stat">
    Total: <tspan class="footer-highlight">{total:,}</tspan> contributions in the last year | Current streak: <tspan class="footer-highlight">{streak} days</tspan> | Longest: <tspan class="footer-highlight">{longest} days</tspan>
  </text>

  <!-- Legend -->
  <g transform="translate({svg_width - 165}, 145)">
    <text x="-32" y="9" class="label">Less</text>
    {''.join([f'<rect x="{i*14}" y="0" width="10" height="10" rx="2" fill="{c}" />' for i, c in enumerate(PALETTE)])}
    <text x="{len(PALETTE)*14 + 6}" y="9" class="label">More</text>
  </g>
</svg>'''

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

    print("[OK] Successfully generated contrib-heatmap.svg")

if __name__ == "__main__":
    render_svg()
