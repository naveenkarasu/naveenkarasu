import io
import os
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

USERNAME = os.getenv("PROFILE_USERNAME", "naveenkarasu")
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

url = f"https://github.com/{USERNAME}.png?size=420"
req = urllib.request.Request(url, headers={"User-Agent": "github-profile-readme-generator"})
with urllib.request.urlopen(req, timeout=30) as response:
    raw = response.read()

img = Image.open(io.BytesIO(raw)).convert("L")
img = ImageOps.fit(img, (42, 42), method=Image.Resampling.LANCZOS)
img = ImageOps.autocontrast(img)

THEMES = {
    "dark": {
        "bg": "#050B12",
        "panel": "#07131D",
        "border": "#0B5A70",
        "green": "#00F5A0",
        "cyan": "#22D3EE",
        "text": "#E6F1F5",
        "muted": "#94A3B8",
    },
    "light": {
        "bg": "#F6F8FA",
        "panel": "#FFFFFF",
        "border": "#7AA7B7",
        "green": "#00875F",
        "cyan": "#007C91",
        "text": "#17212B",
        "muted": "#57606A",
    },
}

W, H = 300, 700
left, top, size = 18, 40, 264
cell = size / 42
px = img.load()


def render(theme_name: str, colors: dict[str, str]) -> None:
    c = colors
    parts = [
        f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal-style pixel portrait of {USERNAME}">
<defs><filter id="g"><feGaussianBlur stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<text x="20" y="29" fill="{c['green']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="13">avatar://{USERNAME}</text>
<text x="252" y="29" text-anchor="end" fill="{c['green']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="13">Online</text>
'''
    ]

    for y in range(42):
        for x in range(42):
            lum = px[x, y] / 255.0
            strength = 1.0 - lum
            if strength < 0.18:
                continue
            radius = 0.6 + strength * 2.3
            opacity = 0.20 + strength * 0.80
            cx = left + (x + 0.5) * cell
            cy = top + (y + 0.5) * cell
            parts.append(
                f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{radius:.2f}" '
                f'fill="{c["green"]}" opacity="{opacity:.2f}"/>'
            )

    parts.append(
        f'''
<line x1="20" y1="318" x2="280" y2="318" stroke="{c['border']}"/>
<text x="20" y="354" fill="{c['text']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="24" font-weight="700">Naveen Karasu</text>
<text x="20" y="380" fill="{c['cyan']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="15">Cybersecurity Engineer</text>
<text x="20" y="420" fill="{c['green']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="15">&gt; whoami</text>
<text x="20" y="442" fill="{c['muted']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="14">Building security automation,</text>
<text x="20" y="462" fill="{c['muted']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="14">detection &amp; AI-assisted tools</text>
<text x="20" y="498" fill="{c['green']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="15">&gt; location</text>
<text x="20" y="520" fill="{c['muted']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="14">Dallas, TX</text>
<text x="20" y="556" fill="{c['green']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="15">&gt; interests</text>
<text x="20" y="578" fill="{c['muted']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="14">Security | AI | Cloud | Labs</text>
<text x="20" y="614" fill="{c['green']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="15">&gt; currently</text>
<text x="20" y="636" fill="{c['muted']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="14">Building cool things...</text>
<text x="20" y="656" fill="{c['muted']}" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="14">Always learning...</text>
<circle cx="270" cy="24" r="5" fill="{c['green']}" filter="url(#g)"/>
</svg>'''
    )

    filename = "ascii-profile.svg" if theme_name == "dark" else "ascii-profile-light.svg"
    out = ASSETS / filename
    out.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {out}")


for name, palette in THEMES.items():
    render(name, palette)
