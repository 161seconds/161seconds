import os

def generate_info_card():
    width = 490
    height = 320

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" fill="none">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; rx: 8px; }}
    .title-bar {{ fill: #161b22; }}
    .dot-red {{ fill: #ff5f56; }}
    .dot-yellow {{ fill: #ffbd2e; }}
    .dot-green {{ fill: #27c93f; }}
    .term-title {{ fill: #8b949e; font-family: "JetBrains Mono", "Courier New", monospace; font-size: 11px; }}
    
    .code-text {{
      font-family: "JetBrains Mono", "Courier New", monospace;
      font-size: 12px;
      dominant-baseline: middle;
    }}
    .key {{ fill: #58a6ff; font-weight: bold; }}
    .val {{ fill: #c9d1d9; }}
    .accent {{ fill: #39d353; font-weight: bold; }}
    .sub {{ fill: #8b949e; }}
    .prompt {{ fill: #ff7b72; font-weight: bold; }}
    .user {{ fill: #79c0ff; font-weight: bold; }}

    .line {{
      opacity: 0;
      animation: lineIn 0.35s ease forwards;
    }}
    @keyframes lineIn {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}
  </style>

  <!-- Card Background -->
  <rect width="{width}" height="{height}" class="bg" />

  <!-- Terminal Window Bar -->
  <path d="M 0 8 C 0 3.58 3.58 0 8 0 L {width-8} 0 C {width-3.58} 0 {width} 3.58 {width} 8 L {width} 28 L 0 28 Z" class="title-bar" />
  <circle cx="16" cy="14" r="5" class="dot-red" />
  <circle cx="32" cy="14" r="5" class="dot-yellow" />
  <circle cx="48" cy="14" r="5" class="dot-green" />
  <text x="{width // 2}" y="18" text-anchor="middle" class="term-title">161seconds@github: ~ (neofetch)</text>

  <!-- Terminal Content Lines with explicit X and Y coordinates -->
  <g class="code-text">
    <g class="line" style="animation-delay: 0.08s;">
      <text x="24" y="56"><tspan class="prompt">➜</tspan> <tspan class="user">161seconds</tspan><tspan class="sub">@github</tspan></text>
      <text x="24" y="74" class="sub">---------------------------------------</text>
    </g>

    <g class="line" style="animation-delay: 0.16s;">
      <text x="24" y="98"><tspan class="key">Name      :</tspan> <tspan class="val">Nguyen Van Quoc Bao</tspan></text>
    </g>

    <g class="line" style="animation-delay: 0.24s;">
      <text x="24" y="120"><tspan class="key">Role      :</tspan> <tspan class="accent">Backend Developer in Progress</tspan></text>
    </g>

    <g class="line" style="animation-delay: 0.32s;">
      <text x="24" y="142"><tspan class="key">Education :</tspan> <tspan class="val">FPT University (Year 3)</tspan></text>
    </g>

    <g class="line" style="animation-delay: 0.40s;">
      <text x="24" y="164"><tspan class="key">Stack     :</tspan> <tspan class="val">C#, .NET Core, SQL Server, MongoDB</tspan></text>
    </g>

    <g class="line" style="animation-delay: 0.48s;">
      <text x="24" y="186"><tspan class="key">Interests :</tspan> <tspan class="val">APIs, System Design, Architecture</tspan></text>
    </g>

    <g class="line" style="animation-delay: 0.56s;">
      <text x="24" y="208"><tspan class="key">Motto     :</tspan> <tspan class="accent">Consistency &gt; Motivation</tspan></text>
    </g>

    <g class="line" style="animation-delay: 0.64s;">
      <text x="24" y="230"><tspan class="key">Status    :</tspan> <tspan class="val">Building cool stuff everyday 🚀</tspan></text>
    </g>

    <!-- Color Palette Blocks -->
    <g class="line" style="animation-delay: 0.72s;">
      <rect x="24"  y="256" width="24" height="12" rx="2" fill="#ff7b72" />
      <rect x="54"  y="256" width="24" height="12" rx="2" fill="#ffa657" />
      <rect x="84"  y="256" width="24" height="12" rx="2" fill="#d2a8ff" />
      <rect x="114" y="256" width="24" height="12" rx="2" fill="#79c0ff" />
      <rect x="144" y="256" width="24" height="12" rx="2" fill="#58a6ff" />
      <rect x="174" y="256" width="24" height="12" rx="2" fill="#39d353" />
      <rect x="204" y="256" width="24" height="12" rx="2" fill="#f0f6fc" />
    </g>
  </g>
</svg>'''

    with open("info-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("[OK] Successfully generated info-card.svg")

if __name__ == "__main__":
    generate_info_card()
