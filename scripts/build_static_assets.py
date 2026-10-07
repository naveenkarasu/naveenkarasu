from pathlib import Path
from base64 import b64encode
from html import escape

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


def pill(x, y, text, accent=None, h=34):
    accent = accent or C['cyan']
    w = max(72, 22 + len(text) * 8.0)
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="9" fill="{C["panel2"]}" stroke="{accent}" stroke-opacity=".50"/>'
            f'<circle cx="{x+15}" cy="{y+h/2}" r="4" fill="{accent}"/>'
            f'<text x="{x+27}" y="{y+h/2+5}" fill="{C["text"]}" font-family="{FONT}" font-size="14">{escape(text)}</text>'), w


def write(name, content):
    (ASSETS / name).write_text(content, encoding='utf-8')

# intro.svg
body = f'''
<rect x="1" y="1" width="678" height="238" rx="16" fill="{C['panel']}" stroke="url(#panelGlow)" stroke-width="2"/>
<text x="24" y="38" fill="{C['green']}" font-family="{FONT}" font-size="17" font-weight="700">naveen@github:~$</text>
<text x="24" y="78" fill="{C['text']}" font-family="{FONT}" font-size="17">I build security-focused tools and automation</text>
<text x="24" y="106" fill="{C['text']}" font-family="{FONT}" font-size="17">for incident investigation, threat detection,</text>
<text x="24" y="134" fill="{C['text']}" font-family="{FONT}" font-size="17">cloud security and secure software delivery.</text>
<text x="24" y="182" fill="{C['cyan']}" font-family="{FONT}" font-size="15">Security Automation • Cloud Security • DevSecOps • AI Security</text>
<rect x="24" y="201" width="11" height="20" rx="2" fill="{C['text']}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>
<path d="M540 28H650V52" fill="none" stroke="{C['green']}" stroke-opacity=".35"/><path d="M650 188V212H540" fill="none" stroke="{C['cyan']}" stroke-opacity=".35"/>
'''
write('intro.svg', svg_wrap(680, 240, body))

# system-status.svg
rows = [('FOCUSED', .96, C['green']), ('LEARNING', .83, C['cyan']), ('BUILDING', .74, C['blue']), ('CONTRIBUTING', .61, C['purple'])]
body = f'<rect x="1" y="1" width="358" height="238" rx="16" fill="{C["panel"]}" stroke="{C["border"]}" stroke-width="2"/>'
body += f'<text x="24" y="38" fill="{C["green"]}" font-family="{FONT}" font-size="17" font-weight="700">SYSTEM STATUS</text>'
body += f'<circle cx="325" cy="32" r="6" fill="{C["green"]}" filter="url(#softGlow)"/><text x="278" y="37" fill="{C["text"]}" font-family="{FONT}" font-size="12">Online</text>'
y = 72
for label, p, col in rows:
    body += f'<text x="24" y="{y+12}" fill="{C["text"]}" font-family="{FONT}" font-size="13">{label}</text>'
    body += f'<rect x="150" y="{y}" width="174" height="13" rx="7" fill="{C["grid"]}"/>'
    body += f'<rect x="150" y="{y}" width="{174*p:.0f}" height="13" rx="7" fill="{col}"/>'
    body += f'<text x="326" y="{y+11}" text-anchor="end" fill="{C["muted"]}" font-family="{FONT}" font-size="11">{int(p*100)}%</text>'
    y += 38
write('system-status.svg', svg_wrap(360, 240, body))

# ascii-profile.svg fallback
lines = [
'         ░▒▓████▓▒░         ',
'      ░▓████████████▓░      ',
'    ░██████▓▒▒▓███████░     ',
'   ▓████▒      ▒████████    ',
'  ▓███▒   ░▒▒░   ▒██████▓   ',
' ▒███▓  ░▓████▓░  ▓██████▒  ',
' ▓███  ▒██▓▒▒▓██▒  ███████  ',
' ████  ██▒    ▒██  ███████  ',
' ████  ███▓▒▒▓███  ███████  ',
' ▓███▒  ▒██████▒  ▒██████▓  ',
' ▒████▓   ▒██▒   ▓███████▒  ',
'  ▓██████▒    ▒██████████▓   ',
'   ▒████████████████████▒    ',
'     ▒████████████████▒      ',
'        ▒▓██████▓▒           ',
]
body = f'<rect x="1" y="1" width="298" height="498" rx="16" fill="{C["panel"]}" stroke="{C["border"]}" stroke-width="2"/>'
y=38
for line in lines:
    body += f'<text x="30" y="{y}" fill="{C["green"]}" font-family="{FONT}" font-size="12" letter-spacing="1">{escape(line)}</text>'
    y += 15
body += f'<text x="24" y="300" fill="{C["text"]}" font-family="{FONT}" font-size="21" font-weight="700">Naveen Karasu</text>'
body += f'<text x="24" y="327" fill="{C["cyan"]}" font-family="{FONT}" font-size="14">Cybersecurity Engineer</text>'
for yy, k, v in [(368, "whoami", "Security automation • detection • AI-assisted tooling"), (414, "focus", "Cloud security • DevSecOps • incident response"), (460, "status", "Building useful security systems")]:
    body += f'<text x="24" y="{yy}" fill="{C["green"]}" font-family="{FONT}" font-size="13">&gt; {k}</text>'
    body += f'<text x="24" y="{yy+20}" fill="{C["muted"]}" font-family="{FONT}" font-size="11">{escape(v)}</text>'
write('ascii-profile.svg', svg_wrap(300, 500, body))

# skills.svg
skills = [
    ('LANGUAGES & SCRIPTING', ['Python','Go','JavaScript','TypeScript','Bash','PowerShell']),
    ('FRAMEWORKS & TOOLS', ['FastAPI','Docker','Kubernetes','Terraform','Ansible','Git','GitHub Actions']),
    ('CLOUD & PLATFORMS', ['AWS','Azure','Linux','Cloud Security']),
    ('SIEM & DETECTION', ['Splunk','Microsoft Sentinel','ELK Stack','QRadar','Sigma','MITRE ATT&CK']),
    ('ANALYSIS & SCANNING', ['Burp Suite','Metasploit','Wireshark','Nmap','Trivy','Semgrep','Checkov']),
    ('SECURITY DOMAINS', ['Incident Response','Threat Detection','Vulnerability Mgmt','Compliance','DevSecOps','AI / LLM Security','Security Automation']),
]
height = 490
body = f'<rect x="1" y="1" width="1198" height="{height-2}" rx="16" fill="{C["panel"]}" stroke="{C["border"]}" stroke-width="2"/>'
body += f'<text x="24" y="38" fill="{C["green"]}" font-family="{FONT}" font-size="18" font-weight="700">SECURITY ARSENAL</text>'
body += f'<text x="233" y="38" fill="{C["muted"]}" font-family="{FONT}" font-size="12">Grouped so a large skill set stays readable</text>'
y = 70
accents=[C['green'],C['cyan'],C['blue'],C['green'],C['cyan'],C['purple']]
for (cat, items), accent in zip(skills, accents):
    body += f'<text x="24" y="{y+22}" fill="{accent}" font-family="{FONT}" font-size="12" font-weight="700">{escape(cat)}</text>'
    x = 220
    yy = y
    for item in items:
        part,w = pill(x, yy, item, accent)
        if x + w > 1170:
            yy += 42
            x = 220
            part,w = pill(x, yy, item, accent)
        body += part
        x += w + 9
    y = max(y+64, yy+52)
write('skills.svg', svg_wrap(1200, height, body))

# Helpers for project cards with embedded thumbnail
def data_uri(path):
    raw = Path(path).read_bytes()
    return 'data:image/png;base64,' + b64encode(raw).decode('ascii')

def project_card(filename, title, repo, tags, desc_lines, thumb, accent):
    uri=data_uri(thumb)
    body = f'<rect x="1" y="1" width="358" height="338" rx="16" fill="{C["panel"]}" stroke="{accent}" stroke-opacity=".55" stroke-width="2"/>'
    body += f'<image href="{uri}" x="14" y="14" width="332" height="86" preserveAspectRatio="xMidYMid slice"/>'
    body += f'<rect x="14" y="14" width="332" height="86" rx="11" fill="none" stroke="{accent}" stroke-opacity=".5"/>'
    body += f'<text x="18" y="128" fill="{C["text"]}" font-family="{FONT}" font-size="18" font-weight="700">{escape(title)}</text>'
    x=18
    for t in tags:
        part,w = pill(x,145,t,accent,h=26)
        body += part.replace('font-size="14"','font-size="11"')
        x += w+6
    yy=205
    for line in desc_lines:
        body += f'<text x="18" y="{yy}" fill="{C["muted"]}" font-family="{FONT}" font-size="12">{escape(line)}</text>'
        yy += 20
    body += f'<rect x="18" y="286" width="153" height="34" rx="9" fill="{C["panel2"]}" stroke="{accent}"/>'
    body += f'<text x="94" y="308" text-anchor="middle" fill="{C["text"]}" font-family="{FONT}" font-size="12">VIEW REPOSITORY →</text>'
    body += f'<text x="342" y="325" text-anchor="end" fill="{C["muted"]}" font-family="{FONT}" font-size="9">{escape(repo)}</text>'
    (PROJECTS/filename).write_text(svg_wrap(360,340,body),encoding='utf-8')

project_card('ai-log-investigator.svg','AI Log Investigator','AI-log-investigator',['Python','FastAPI','Docker','LLM'],['AI-assisted log investigation and','root-cause analysis with offline fallbacks.'],ASSETS/'ai-log-investigator.png',C['cyan'])
project_card('cehv12-study-guide.svg','CEHv12 Study Guide','CEHV12_StudyGuide',['Security','Training','Labs'],['Open-source cybersecurity study guide','with practical exercises and labs.'],ASSETS/'cehv12-study-guide.png',C['pink'])
project_card('portfolio-3d.svg','Portfolio 3D','portfolio-3d',['Three.js','TypeScript','WebGPU'],['Interactive 3D portfolio with physics,','lighting and dynamic environments.'],ASSETS/'portfolio-3d.png',C['blue'])

# stats.svg fallback - workflow overwrites this with live values
body = f'<rect x="1" y="1" width="1198" height="168" rx="16" fill="{C["panel"]}" stroke="{C["border"]}" stroke-width="2"/>'
body += f'<text x="24" y="34" fill="{C["green"]}" font-family="{FONT}" font-size="16" font-weight="700">GITHUB SIGNALS</text>'
for i,(label,val,col) in enumerate([('CONTRIBUTIONS','auto',C['green']),('PUBLIC REPOS','auto',C['cyan']),('FOLLOWERS','auto',C['purple']),('RECENT ACTIVITY','auto',C['pink'])]):
    x=24+i*292
    body += f'<rect x="{x}" y="52" width="268" height="92" rx="12" fill="{C["panel2"]}" stroke="{col}" stroke-opacity=".35"/>'
    body += f'<text x="{x+18}" y="78" fill="{C["muted"]}" font-family="{FONT}" font-size="11">{label}</text>'
    body += f'<text x="{x+18}" y="116" fill="{C["text"]}" font-family="{FONT}" font-size="24" font-weight="700">{val}</text>'
write('stats.svg', svg_wrap(1200,170,body))

# activity.svg fallback
body = f'<rect x="1" y="1" width="598" height="258" rx="16" fill="{C["panel"]}" stroke="{C["border"]}" stroke-width="2"/>'
body += f'<text x="24" y="38" fill="{C["green"]}" font-family="{FONT}" font-size="16" font-weight="700">RECENT ACTIVITY</text>'
for i, line in enumerate(['Generated automatically from public GitHub events','Pushes, pull requests and releases appear here','Run the workflow once after adding these files']):
    yy=82+i*48
    body += f'<circle cx="32" cy="{yy-5}" r="5" fill="{[C["green"],C["cyan"],C["purple"]][i]}"/><text x="50" y="{yy}" fill="{C["text"]}" font-family="{FONT}" font-size="13">{escape(line)}</text>'
write('activity.svg', svg_wrap(600,260,body))

# achievements capsule row
items=[('CEH v12',C['red']),('AWS Cloud',C['amber']),('Azure Security',C['cyan']),('CISSP — in progress',C['green'])]
body = f'<rect x="1" y="1" width="598" height="258" rx="16" fill="{C["panel"]}" stroke="{C["border"]}" stroke-width="2"/>'
body += f'<text x="24" y="38" fill="{C["green"]}" font-family="{FONT}" font-size="16" font-weight="700">CERTIFICATIONS / LEARNING</text>'
y=66
for name,col in items:
    body += f'<rect x="24" y="{y}" width="550" height="36" rx="10" fill="{C["panel2"]}" stroke="{col}" stroke-opacity=".40"/><circle cx="42" cy="{y+18}" r="5" fill="{col}"/><text x="58" y="{y+23}" fill="{C["text"]}" font-family="{FONT}" font-size="13">{escape(name)}</text>'
    y += 44
write('achievements.svg', svg_wrap(600,260,body))

# capsule/aura footer with embedded art
art=data_uri(ASSETS/'footer-art.png')
extra='''<linearGradient id="footerG" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#00131D"/><stop offset=".48" stop-color="#003B32"/><stop offset=".75" stop-color="#10294A"/><stop offset="1" stop-color="#3B1239"/></linearGradient>'''
body = f'''<path d="M0 28 Q180 6 350 30 T700 30 T1050 26 T1200 20 V160 H0Z" fill="url(#footerG)"/>
<path d="M0 30 Q180 8 350 32 T700 32 T1050 28 T1200 22" fill="none" stroke="{C['green']}" stroke-opacity=".55" stroke-width="2"><animate attributeName="stroke-opacity" values=".25;.75;.25" dur="3s" repeatCount="indefinite"/></path>
<text x="42" y="82" fill="{C['green']}" font-family="{FONT}" font-size="21" font-weight="700">LET'S CONNECT</text>
<text x="42" y="109" fill="{C['text']}" font-family="{FONT}" font-size="13">Security automation • Cloud security • DevSecOps • AI security</text>
<text x="42" y="136" fill="{C['muted']}" font-family="{FONT}" font-size="11">Built as a custom GitHub README system UI — terminal, pixel, aura and capsule inspired.</text>
<image href="{art}" x="980" y="53" width="188" height="72" preserveAspectRatio="xMidYMid slice"/>
'''
write('footer.svg', svg_wrap(1200,160,body,extra))

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
    if path.name.endswith('-light.svg') or path.name.startswith('contribution-snake-'):
        return
    text = path.read_text(encoding='utf-8')
    for dark, light in LIGHT_REPLACEMENTS.items():
        text = text.replace(dark, light).replace(dark.lower(), light)
    out = path.with_name(path.stem + '-light.svg')
    out.write_text(text, encoding='utf-8')


for svg_path in sorted(ASSETS.rglob('*.svg')):
    make_light_variant(svg_path)

print('Light-mode SVG variants generated.')
