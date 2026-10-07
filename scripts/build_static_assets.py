from pathlib import Path
from base64 import b64encode
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
PROJECTS = ASSETS / 'projects'
PROJECTS.mkdir(parents=True, exist_ok=True)

C = {
    'bg': '#050B12', 'panel': '#07131D', 'panel2': '#091925', 'border': '#0B5A70',
    'green': '#00F5A0', 'cyan': '#22D3EE', 'blue': '#3B82F6', 'purple': '#8B5CF6',
    'pink': '#EC4899', 'text': '#E6F1F5', 'muted': '#94A3B8', 'grid': '#0B2536',
    'amber': '#F59E0B', 'red': '#FB7185'
}
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def svg_wrap(width, height, body, extra_defs=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
<defs>
  <linearGradient id="panelGlow" x1="0" x2="1"><stop stop-color="{C['cyan']}" stop-opacity=".28"/><stop offset=".52" stop-color="{C['green']}" stop-opacity=".10"/><stop offset="1" stop-color="{C['purple']}" stop-opacity=".20"/></linearGradient>
  <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  {extra_defs}
</defs>
<rect width="100%" height="100%" rx="16" fill="{C['bg']}"/>
{body}
</svg>'''


# Brand icons: Simple Icons (CC0). Generic icons: Lucide (ISC). Vendored in scripts/icons.json.
ICONS = json.loads((ROOT / 'scripts' / 'icons.json').read_text(encoding='utf-8'))
SKILL_ICONS = {
    'Python': 'python', 'Go': 'go', 'JavaScript': 'javascript', 'TypeScript': 'typescript', 'Bash': 'gnubash',
    'PowerShell': 'powershell', 'FastAPI': 'fastapi', 'Docker': 'docker', 'Kubernetes': 'kubernetes',
    'Terraform': 'terraform', 'Ansible': 'ansible', 'Git': 'git', 'GitHub Actions': 'githubactions',
    'AWS': 'amazonwebservices', 'Azure': 'microsoftazure', 'Linux': 'linux', 'Cloud Security': 'cloud-cog',
    'Splunk': 'splunk', 'Microsoft Sentinel': 'shield-alert', 'ELK Stack': 'elasticstack', 'QRadar': 'ibm',
    'Sigma': 'scroll-text', 'MITRE ATT&CK': 'target', 'Burp Suite': 'burpsuite', 'Metasploit': 'metasploit',
    'Wireshark': 'wireshark', 'Nmap': 'network', 'Trivy': 'trivy', 'Semgrep': 'scan-search', 'Checkov': 'shield-check',
    'Incident Response': 'siren', 'Threat Detection': 'radar', 'Vulnerability Mgmt': 'bug', 'Compliance': 'file-check',
    'DevSecOps': 'workflow', 'AI / LLM Security': 'brain-circuit', 'Security Automation': 'bot',
}


def icon(name, x, y, size, color):
    i = ICONS[name]
    if 'lucide' in i:
        return (f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
                f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{i["lucide"]}</svg>')
    r, g, b = (int(i['hex'][k:k + 2], 16) for k in (1, 3, 5))
    fill = i['hex'] if (r * .299 + g * .587 + b * .114) > 60 else C['text']  # near-black logos would vanish on dark panels
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24"><path d="{i["d"]}" fill="{fill}"/></svg>'


def pill(x, y, text, accent=None, h=34, fs=14):
    accent = accent or C['cyan']
    ic = SKILL_ICONS.get(text)
    # monospace glyphs are ~0.6em wide; left inset for the icon/dot + 12px right padding
    inset = h * .55 + 14 if ic else 27
    w = inset + 12 + len(text) * fs * 0.62
    mark = icon(ic, x + 9, y + h * .225, h * .55, accent) if ic else f'<circle cx="{x+15}" cy="{y+h/2}" r="4" fill="{accent}"/>'
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="9" fill="{C["panel2"]}" stroke="{accent}" stroke-opacity=".50"/>'
            + mark +
            f'<text x="{x+inset:.0f}" y="{y+h/2+fs*.35:.0f}" fill="{C["text"]}" font-family="{FONT}" font-size="{fs}">{escape(text)}</text>'), w


def data_uri(path):
    mime = 'jpeg' if Path(path).suffix == '.jpg' else 'png'
    return f'data:image/{mime};base64,' + b64encode(Path(path).read_bytes()).decode('ascii')


ART = ASSETS / 'art'


def write(name, content):
    (ASSETS / name).write_text(content, encoding='utf-8')

# header.svg (stays dark in light mode, like the mockup)
extra = f'''<linearGradient id="fadeL" x1="0" x2="1"><stop stop-color="{C['bg']}"/><stop offset=".34" stop-color="{C['bg']}" stop-opacity=".9"/><stop offset=".6" stop-color="{C['bg']}" stop-opacity="0"/></linearGradient>
  <clipPath id="hclip"><rect width="1200" height="340" rx="16"/></clipPath>'''
body = f'''<g clip-path="url(#hclip)"><image href="{data_uri(ART/'header.jpg')}" x="270" y="0" width="1020" height="340" preserveAspectRatio="xMidYMid slice"/><rect width="1200" height="340" fill="url(#fadeL)"/></g>
<rect x="1" y="1" width="1198" height="338" rx="16" fill="none" stroke="{C['border']}" stroke-width="2"/>
<text x="48" y="118" fill="{C['text']}" font-family="{FONT}" font-size="46" font-weight="700" letter-spacing="2">NAVEEN KARASU</text>
<rect x="424" y="80" width="14" height="44" fill="{C['green']}"/>
<text x="48" y="160" fill="{C['cyan']}" font-family="{FONT}" font-size="24">Cybersecurity Engineer</text>
<text x="48" y="200" fill="{C['text']}" font-family="{FONT}" font-size="15">Security Automation • Cloud Security • DevSecOps • AI Security</text>
<text font-family="'Segoe Script','Brush Script MT',cursive" font-size="22" font-style="italic" fill="{C['text']}" text-anchor="middle"><tspan x="1110" y="62">Turning</tspan><tspan x="1110" y="90">Curiosity</tspan><tspan x="1110" y="118">into</tspan><tspan x="1110" y="146">Security</tspan></text>
'''
x = 48
for chip in ['Build', 'Detect', 'Automate', 'Secure', 'Learn']:
    w = 36 + len(chip) * 15 * 0.62
    body += f'<rect x="{x}" y="232" width="{w:.0f}" height="36" rx="18" fill="{C["panel"]}" fill-opacity=".7" stroke="{C["green"]}" stroke-width="2"/>'
    body += f'<text x="{x+w/2:.0f}" y="255" text-anchor="middle" fill="{C["green"]}" font-family="{FONT}" font-size="15">{chip}</text>'
    x += w + 14
write('header.svg', svg_wrap(1200, 340, body, extra))

# intro.svg
body = f'''
<rect x="1" y="1" width="678" height="238" rx="16" fill="{C['panel']}" stroke="url(#panelGlow)" stroke-width="2"/>
<text x="24" y="40" fill="{C['green']}" font-family="{FONT}" font-size="19" font-weight="700">naveen@github:~$</text>
<text font-family="{FONT}" font-size="18" fill="{C['text']}"><tspan x="24" y="76">I build security-focused</tspan><tspan x="24" y="102">tools and automation for</tspan><tspan x="24" y="128">incident investigation,</tspan><tspan x="24" y="154">threat detection, cloud</tspan><tspan x="24" y="180">security &amp; secure delivery.</tspan></text>
<g clip-path="url(#iclip)"><image href="{data_uri(ART/'intro.jpg')}" x="430" y="14" width="236" height="212" preserveAspectRatio="xMidYMid slice"/><rect x="430" y="14" width="80" height="212" fill="url(#ifade)"/></g>
<rect x="556" y="134" width="100" height="80" rx="8" fill="{C['panel']}" fill-opacity=".85" stroke="{C['border']}"/>
<text font-family="{FONT}" font-size="11" fill="{C['text']}"><tspan x="566" y="153">✓ Coffee</tspan><tspan x="566" y="170">✓ Code</tspan><tspan x="566" y="187">✓ Security</tspan><tspan x="566" y="204">✓ Better Systems</tspan></text>
<rect x="24" y="200" width="11" height="20" rx="2" fill="{C['text']}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>
'''
write('intro.svg', svg_wrap(680, 240, body, f'''<clipPath id="iclip"><rect x="430" y="14" width="236" height="212" rx="10"/></clipPath>
  <linearGradient id="ifade" x1="0" x2="1"><stop stop-color="{C['panel']}"/><stop offset="1" stop-color="{C['panel']}" stop-opacity="0"/></linearGradient>'''))

# system-status.svg
rows = [('FOCUSED', .96, C['green']), ('LEARNING', .83, C['cyan']), ('BUILDING', .74, C['blue']), ('CONTRIBUTING', .61, C['purple'])]
body = f'<rect x="1" y="1" width="358" height="238" rx="16" fill="{C["panel"]}" stroke="{C["border"]}" stroke-width="2"/>'
body += f'<text x="24" y="38" fill="{C["green"]}" font-family="{FONT}" font-size="19" font-weight="700">SYSTEM STATUS</text>'
body += f'<circle cx="325" cy="32" r="6" fill="{C["green"]}" filter="url(#softGlow)"/><text x="314" y="38" text-anchor="end" fill="{C["text"]}" font-family="{FONT}" font-size="15">Online</text>'
y = 72
for label, p, col in rows:
    body += f'<text x="24" y="{y+13}" fill="{C["text"]}" font-family="{FONT}" font-size="15">{label}</text>'
    body += f'<rect x="158" y="{y}" width="130" height="14" rx="7" fill="{C["grid"]}"/>'
    body += f'<rect x="158" y="{y}" width="{130*p:.0f}" height="14" rx="7" fill="{col}"/>'
    body += f'<text x="338" y="{y+13}" text-anchor="end" fill="{C["muted"]}" font-family="{FONT}" font-size="14">{int(p*100)}%</text>'
    y += 40
write('system-status.svg', svg_wrap(360, 240, body))

# skills.svg
skills = [
    ('LANGUAGES & SCRIPTING', ['Python','Go','JavaScript','TypeScript','Bash','PowerShell']),
    ('FRAMEWORKS & TOOLS', ['FastAPI','Docker','Kubernetes','Terraform','Ansible','Git','GitHub Actions']),
    ('CLOUD & PLATFORMS', ['AWS','Azure','Linux','Cloud Security']),
    ('SIEM & DETECTION', ['Splunk','Microsoft Sentinel','ELK Stack','QRadar','Sigma','MITRE ATT&CK']),
    ('ANALYSIS & SCANNING', ['Burp Suite','Metasploit','Wireshark','Nmap','Trivy','Semgrep','Checkov']),
    ('SECURITY DOMAINS', ['Incident Response','Threat Detection','Vulnerability Mgmt','Compliance','DevSecOps','AI / LLM Security','Security Automation']),
]
W = 900
body = f'<text x="24" y="40" fill="{C["green"]}" font-family="{FONT}" font-size="19" font-weight="700">SECURITY ARSENAL</text>'
y = 66
accents=[C['green'],C['cyan'],C['blue'],C['green'],C['cyan'],C['purple']]
for (cat, items), accent in zip(skills, accents):
    words = cat.split(' & ')
    body += f'<text fill="{accent}" font-family="{FONT}" font-size="14" font-weight="700"><tspan x="24" y="{y+17}">{escape(words[0])}{" &amp;" if len(words) > 1 else ""}</tspan>' + (f'<tspan x="24" y="{y+35}">{escape(words[1])}</tspan>' if len(words) > 1 else '') + '</text>'
    x, yy = 190, y
    for item in items:
        part, w = pill(x, yy, item, accent, h=38, fs=15)
        if x + w > W - 18:
            yy += 46
            x = 190
            part, w = pill(x, yy, item, accent, h=38, fs=15)
        body += part
        x += w + 9
    y = yy + 58
height = y + 4
body = f'<rect x="1" y="1" width="{W-2}" height="{height-2}" rx="16" fill="{C["panel"]}" stroke="{C["border"]}" stroke-width="2"/>' + body
write('skills.svg', svg_wrap(W, height, body))


def project_card(filename, title, repo, tags, desc_lines, thumb, accent, pos):
    uri=data_uri(thumb)
    body = f'<rect x="1" y="1" width="358" height="338" rx="16" fill="{C["panel"]}" stroke="{accent}" stroke-opacity=".55" stroke-width="2"/>'
    body += f'<image href="{uri}" x="14" y="14" width="332" height="86" preserveAspectRatio="xMidYMid slice"/>'
    body += f'<rect x="14" y="14" width="332" height="86" rx="11" fill="none" stroke="{accent}" stroke-opacity=".5"/>'
    body += f'<text x="18" y="128" fill="{C["text"]}" font-family="{FONT}" font-size="18" font-weight="700">{escape(title)}</text>'
    x=18
    for t in tags:
        part,w = pill(x,145,t,accent,h=28,fs=11)
        body += part
        x += w+6
    yy=205
    for line in desc_lines:
        body += f'<text x="18" y="{yy}" fill="{C["muted"]}" font-family="{FONT}" font-size="13">{escape(line)}</text>'
        yy += 21
    body += f'<rect x="18" y="286" width="153" height="34" rx="9" fill="{C["panel2"]}" stroke="{accent}"/>'
    body += f'<text x="94" y="308" text-anchor="middle" fill="{C["text"]}" font-family="{FONT}" font-size="12">VIEW REPOSITORY →</text>'
    body += f'<text x="342" y="325" text-anchor="end" fill="{C["muted"]}" font-family="{FONT}" font-size="9">{escape(repo)}</text>'
    card = svg_wrap(360, 340, body).replace('<rect width="100%" height="100%" rx="16"', '<rect width="360" height="340" rx="16"')
    inner = card[card.index('>') + 1:card.rindex('</svg>')]
    cw = (1200 - 2 * 20) / 3  # three cards + two 20px gutters span the 1200px page grid
    x = pos * (400 - cw) / 2   # left card flush left, middle centred, right card flush right
    (PROJECTS/filename).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="{340*cw/360:.0f}" viewBox="0 0 400 {340*cw/360:.0f}" role="img">'
        f'<svg x="{x:.2f}" width="{cw:.2f}" height="{340*cw/360:.2f}" viewBox="0 0 360 340">{inner}</svg></svg>', encoding='utf-8')

project_card('ai-log-investigator.svg','AI Log Investigator','AI-log-investigator',['Python','FastAPI','Docker','LLM'],['AI-assisted log investigation and','root-cause analysis with offline fallbacks.'],ART/'ai-log-investigator.jpg',C['cyan'],0)
project_card('cehv12-study-guide.svg','CEHv12 Study Guide','CEHV12_StudyGuide',['Security','Training','Labs'],['Open-source cybersecurity study guide','with practical exercises and labs.'],ART/'cehv12-study-guide.jpg',C['pink'],1)
project_card('portfolio-3d.svg','Portfolio 3D','portfolio-3d',['Three.js','TypeScript','WebGPU'],['Interactive 3D portfolio with physics,','lighting and dynamic environments.'],ART/'portfolio-3d.jpg',C['blue'],2)

# certifications: 2x2 capsules with icons, like the mockup
certs = [('CEH', 'v12', 'target', C['red']), ('AWS', 'Cloud', 'amazonwebservices', C['amber']),
         ('Azure', 'Security', 'microsoftazure', C['cyan']), ('CISSP', 'In progress', 'lock', C['green'])]
body = f'<rect x="1" y="1" width="598" height="258" rx="16" fill="{C["panel"]}" stroke="{C["border"]}" stroke-width="2"/>'
body += f'<text x="24" y="38" fill="{C["green"]}" font-family="{FONT}" font-size="19" font-weight="700">CERTIFICATIONS / LEARNING</text>'
for i, (name, sub, ic, col) in enumerate(certs):
    x, y = 24 + (i % 2) * 284, 62 + (i // 2) * 96
    body += f'<rect x="{x}" y="{y}" width="268" height="84" rx="42" fill="{C["panel2"]}" stroke="{col}" stroke-opacity=".55" stroke-width="1.5"/>'
    body += f'<circle cx="{x+42}" cy="{y+42}" r="26" fill="{C["bg"]}" stroke="{col}" stroke-opacity=".6"/>' + icon(ic, x + 28, y + 28, 28, col)
    body += f'<text x="{x+82}" y="{y+39}" fill="{C["text"]}" font-family="{FONT}" font-size="18" font-weight="700">{escape(name)}</text>'
    body += f'<text x="{x+82}" y="{y+60}" fill="{C["muted"]}" font-family="{FONT}" font-size="13">{escape(sub)}</text>'
write('achievements.svg', svg_wrap(600,260,body))

# quote panel with the moonlit skyline fading in from the right
extra = f'''<linearGradient id="qfade" x1="0" x2="1"><stop offset=".45" stop-color="{C['panel']}"/><stop offset=".7" stop-color="{C['panel']}" stop-opacity="0"/></linearGradient>
  <clipPath id="qclip"><rect width="1200" height="200" rx="16"/></clipPath>'''
body = f'''<g clip-path="url(#qclip)"><rect width="1200" height="200" fill="{C['panel']}"/><image href="{data_uri(ART/'quote.jpg')}" x="560" y="0" width="640" height="200" preserveAspectRatio="xMidYMid slice"/><rect width="1200" height="200" fill="url(#qfade)"/></g>
<rect x="1" y="1" width="1198" height="198" rx="16" fill="none" stroke="{C['border']}" stroke-width="2"/>
<text x="40" y="78" fill="{C['purple']}" font-family="Georgia,serif" font-size="64">“</text>
<text font-family="{FONT}" font-size="20" fill="{C['text']}"><tspan x="84" y="64">Better security tools.</tspan><tspan x="84" y="94">Safer systems.</tspan><tspan x="84" y="124">A more open and secure internet.</tspan></text>
<text x="84" y="162" fill="{C['cyan']}" font-family="{FONT}" font-size="15">— Naveen Karasu</text>
'''
write('quote.svg', svg_wrap(1200, 200, body, extra))

# social buttons: one small SVG each, so every button is its own link in README.md
SOCIAL = ASSETS / 'social'
SOCIAL.mkdir(exist_ok=True)
for name, ic, col in [('LinkedIn', 'linkedin', C['cyan']), ('GitHub', 'github', C['green']), ('X', 'x', C['text']),
                      ('Medium', 'medium', C['text']), ('dev.to', 'devdotto', C['text']), ('Hashnode', 'hashnode', C['blue']),
                      ('Stack Overflow', 'stackoverflow', C['amber']), ('Instagram', 'instagram', C['pink'])]:
    btn = (f'<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48" role="img" aria-label="{escape(name)}">'
           f'<rect x="1" y="1" width="46" height="46" rx="12" fill="{C["panel"]}" stroke="{col}" stroke-opacity=".7" stroke-width="1.5"/>'
           + icon(ic, 13, 13, 22, col) + '</svg>')
    (SOCIAL / f'{ic}.svg').write_text(btn, encoding='utf-8')

# pixel cat mascot (sits at the end of the contribution snake, like the mockup)
CAT = """
..W..........W..
..WW........WW..
..WPW......WPW..
..WWWWWWWWWWWW..
.WWWWWWWWWWWWWW.
.WWGGWWWWWWGGWW.
.WWGKWWWWWWGKWW.
.WWWWWWPPWWWWWW.
.WPPWWWKKWWWPPW.
..WWWWWWWWWWWW..
...WWWWWWWWWW...
..WWWWWWWWWWWW..
..WW.WWWWWW.WW..
..WW.WW..WW.WW..
"""
colors = {'W': C['text'], 'P': C['pink'], 'G': C['green'], 'K': C['border']}
cells = ''.join(f'<rect x="{x*6}" y="{y*6+6}" width="6" height="6" fill="{colors[ch]}"/>'
                for y, row in enumerate(CAT.strip().splitlines()) for x, ch in enumerate(row) if ch in colors)
write('pixel-cat.svg', f'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96" shape-rendering="crispEdges" role="img">{cells}</svg>')

# footer with HQ shrine art fading in from the right
extra = f'''<linearGradient id="ffade" x1="0" x2="1"><stop offset=".5" stop-color="{C['panel']}"/><stop offset=".72" stop-color="{C['panel']}" stop-opacity="0"/></linearGradient>
  <clipPath id="fclip"><rect width="1200" height="240" rx="16"/></clipPath>'''
body = f'''<g clip-path="url(#fclip)"><rect width="1200" height="240" fill="{C['panel']}"/><image href="{data_uri(ART/'footer.jpg')}" x="600" y="0" width="600" height="240" preserveAspectRatio="xMidYMid slice"/><rect width="1200" height="240" fill="url(#ffade)"/></g>
<rect x="1" y="1" width="1198" height="238" rx="16" fill="none" stroke="{C['border']}" stroke-width="2"/>
<text x="42" y="82" fill="{C['green']}" font-family="{FONT}" font-size="24" font-weight="700">LET'S CONNECT</text>
<text x="42" y="120" fill="{C['text']}" font-family="{FONT}" font-size="15">Open to collaboration on security, automation</text>
<text x="42" y="144" fill="{C['text']}" font-family="{FONT}" font-size="15">and interesting projects.</text>
<text x="42" y="192" fill="{C['muted']}" font-family="{FONT}" font-size="15">Thanks for visiting! ⭐ Follow for more security and coding projects.</text>
'''
write('footer.svg', svg_wrap(1200, 240, body, extra))

print('Static assets generated.')

# --- Light-mode asset export -------------------------------------------------
# GitHub profile READMEs cannot run page-level CSS, so we export matching
# light-mode SVGs and select them in README.md with <picture>.
LIGHT_REPLACEMENTS = {
    '#050B12': '#F6F8FA',
    '#07131D': '#FFFFFF',
    '#091925': '#EFF6F8',
    '#0B5A70': '#7AA7B7',
    '#00F5A0': '#00875F',
    '#22D3EE': '#007C91',
    '#3B82F6': '#0969DA',
    '#8B5CF6': '#6639BA',
    '#EC4899': '#BF3989',
    '#E6F1F5': '#17212B',
    '#94A3B8': '#57606A',
    '#0B2536': '#D8E3E7',
    '#F59E0B': '#9A6700',
    '#FB7185': '#CF222E',
    '#00131D': '#F6F8FA',
    '#003B32': '#E4F4EE',
    '#10294A': '#EAF2FF',
    '#3B1239': '#FBEAF5',
}


def make_light_variant(path: Path):
    if path.name.endswith('-light.svg') or path.name.startswith('contribution-snake-') or path.name == 'header.svg':
        return
    text = path.read_text(encoding='utf-8')
    for dark, light in LIGHT_REPLACEMENTS.items():
        text = text.replace(dark, light).replace(dark.lower(), light)
    out = path.with_name(path.stem + '-light.svg')
    out.write_text(text, encoding='utf-8')


for svg_path in sorted(ASSETS.rglob('*.svg')):
    make_light_variant(svg_path)

print('Light-mode SVG variants generated.')
