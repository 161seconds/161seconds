import os
import sys

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense)

DEFAULT_ASCII_ART = [
    "                ....................                ",
    "            .:+shddddddddddddddddhs+:.            ",
    "          -+ydmmmmmmmmmmmmmmmmmmmmmmdy+-          ",
    "        -sdmmmmmmmmmmmmmmmmmmmmmmmmmmmmds-        ",
    "       +dmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmd+       ",
    "      +dmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmd+      ",
    "     +dmmmmmmmmmmmmmNNNNNNNNmmmmmmmmmmmmmmmd+     ",
    "    :dmmmmmmmmmmNNNNNNNNNNNNNNNNmmmmmmmmmmmmd:    ",
    "    smmmmmmmmmNNNNNNNNNNNNNNNNNNNNmmmmmmmmmmms    ",
    "   .dmmmmmmmmNNNNNNNNNNNNNNNNNNNNNNmmmmmmmmmmd.   ",
    "   :mmmmmmmNNNNNNNNNNNNNNNNNNNNNNNNNNmmmmmmmm:   ",
    "   +mmmmmmNNNNNNNNNNNNNNNNNNNNNNNNNNNNmmmmmmm+   ",
    "   +mmmmmmNNNNNNNmdhysooosyhdmNNNNNNNNmmmmmmm+   ",
    "   :mmmmmmNNNNmy+:.          .:+ymNNNNmmmmmmm:   ",
    "   .dmmmmmNNNs.                  .sNNNmmmmmmd.   ",
    "    smmmmmNNy                      yNNmmmmmmms    ",
    "    :dmmmmNN:   .://.      .://.   :NNmmmmmmd:    ",
    "     +dmmmNN-  -s++os-    -s++os-  -NNmmmmmd+     ",
    "      +dmmNN:  :s--+s:    :s--+s:  :NNmmmmd+      ",
    "       +dmNNs   .::.        .::.   sNNmmd+       ",
    "        -sdNNy.                  .yNNds-        ",
    "          -+ydmds/-          -/sdmdy+-          ",
    "            .:+shddddo:--:oddddhs+:.            ",
    "                ..:+shdmmdhso+..                ",
    "             -/oydmNNNNNNNNNNmdyo/-             ",
    "         ./sdmNNNNNNNNNNNNNNNNNNNNmds/.         ",
    "       :sdmNNNNNNNNNNNNNNNNNNNNNNNNNNmds:       ",
    "     :hNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNh:     ",
    "   .yNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNy.   ",
    "  -dNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNd-  ",
    " +NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN+ "
]

def make_ascii_svg(image_path="source-prepped.png", output_path="ascii-portrait.svg", target_width=52):
    rows = []
    
    if os.path.exists(image_path):
        try:
            from PIL import Image
            img = Image.open(image_path).convert("L")
            w, h = img.size
            aspect_ratio = h / w
            target_height = int(target_width * aspect_ratio * 0.55)
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

            for y in range(target_height):
                row_str = ""
                for x in range(target_width):
                    pixel = img.getpixel((x, y))
                    idx = int((255 - pixel) / 255 * (len(RAMP) - 1))
                    char = RAMP[idx]
                    if char == "&": char = "&amp;"
                    elif char == "<": char = "&lt;"
                    elif char == ">": char = "&gt;"
                    row_str += char
                rows.append(row_str)
        except Exception as e:
            print(f"[WARN] Error reading image ({e}), falling back to default avatar art.")
            rows = DEFAULT_ASCII_ART
    else:
        print(f"[INFO] '{image_path}' not found. Using default terminal avatar art.")
        rows = DEFAULT_ASCII_ART

    svg_width = 370
    svg_height = 320
    font_size = 7.5
    line_height = 8.5

    text_elements = []
    for idx, row in enumerate(rows):
        y_pos = 42 + (idx * line_height)
        delay = idx * 0.035
        text_elements.append(f'''
    <g class="row" style="animation-delay: {delay:.3f}s;">
      <text x="18" y="{y_pos}">{row}</text>
    </g>''')

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}" fill="none">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; rx: 8px; }}
    .title-bar {{ fill: #161b22; }}
    .dot-red {{ fill: #ff5f56; }}
    .dot-yellow {{ fill: #ffbd2e; }}
    .dot-green {{ fill: #27c93f; }}
    .term-title {{ fill: #8b949e; font-family: "JetBrains Mono", "Courier New", monospace; font-size: 11px; }}
    
    text {{
      fill: #58a6ff;
      font-family: "JetBrains Mono", "Courier New", monospace;
      font-size: {font_size}px;
      letter-spacing: 1px;
      white-space: pre;
    }}
    .row {{
      opacity: 0;
      animation: typeRow 0.05s forwards;
    }}
    @keyframes typeRow {{
      to {{ opacity: 1; }}
    }}
  </style>

  <!-- Background -->
  <rect width="{svg_width}" height="{svg_height}" class="bg" />

  <!-- Window Header -->
  <path d="M 0 8 C 0 3.58 3.58 0 8 0 L {svg_width-8} 0 C {svg_width-3.58} 0 {svg_width} 3.58 {svg_width} 8 L {svg_width} 28 L 0 28 Z" class="title-bar" />
  <circle cx="16" cy="14" r="5" class="dot-red" />
  <circle cx="32" cy="14" r="5" class="dot-yellow" />
  <circle cx="48" cy="14" r="5" class="dot-green" />
  <text x="{svg_width // 2}" y="18" text-anchor="middle" class="term-title">portrait.ascii</text>

  <!-- Animated Rows -->
  {''.join(text_elements)}
</svg>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[OK] Successfully generated {output_path}")

if __name__ == "__main__":
    img_arg = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
    make_ascii_svg(img_arg)
