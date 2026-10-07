import json
import os
import urllib.request
from html import escape
from pathlib import Path

USERNAME = os.getenv("PROFILE_USERNAME", "naveenkarasu")
TOKEN = os.getenv("GITHUB_TOKEN", "")
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": {
        "bg": "#050B12",
        "panel": "#07131D",
        "panel2": "#091925",
        "border": "#0B5A70",
        "green": "#00F5A0",
        "cyan": "#22D3EE",
        "purple": "#8B5CF6",
        "pink": "#EC4899",
        "text": "#E6F1F5",
        "muted": "#94A3B8",
    },
    "light": {
        "bg": "#F6F8FA",
        "panel": "#FFFFFF",
        "panel2": "#EFF6F8",
        "border": "#7AA7B7",
        "green": "#00875F",
        "cyan": "#007C91",
        "purple": "#6639BA",
        "pink": "#BF3989",
        "text": "#17212B",
        "muted": "#57606A",
    },
}


def request_json(url, data=None):
    headers = {
        "User-Agent": "github-profile-readme-generator",
        "Accept": "application/vnd.github+json",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method="POST" if data else "GET",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


query = """query($login:String!){user(login:$login){repositories(privacy:PUBLIC){totalCount} followers{totalCount} contributionsCollection{contributionCalendar{totalContributions}} starred: repositories(first:100,privacy:PUBLIC,ownerAffiliations:OWNER,orderBy:{field:STARGAZERS,direction:DESC}){nodes{stargazerCount}}}}"""
payload = json.dumps({"query": query, "variables": {"login": USERNAME}}).encode()

try:
    data = request_json("https://api.github.com/graphql", payload)["data"]["user"]
    repos = data["repositories"]["totalCount"]
    followers = data["followers"]["totalCount"]
    contrib = data["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    stars = sum(n["stargazerCount"] for n in data["starred"]["nodes"])
except Exception:
    repos = followers = contrib = stars = "—"

try:
    events = request_json(f"https://api.github.com/users/{USERNAME}/events/public?per_page=8")
except Exception:
    events = []


def summarize(event):
    typ = event.get("type", "Activity").removesuffix("Event")
    repo = event.get("repo", {}).get("name", "").split("/")[-1]
    mapping = {
        "Push": "Pushed commits to",
        "PullRequest": "Updated PR in",
        "Issues": "Updated issue in",
        "Create": "Created in",
        "Release": "Published release in",
        "Fork": "Forked",
    }
    return f"{mapping.get(typ, typ)} {repo}".strip()


def render(theme_name: str, c: dict[str, str]) -> None:
    cards = [
        ("YEAR CONTRIBUTIONS", contrib, c["green"]),
        ("PUBLIC REPOS", repos, c["cyan"]),
        ("FOLLOWERS", followers, c["purple"]),
        ("REPO STARS", stars, c["pink"]),
    ]
    parts = [
        f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="170" viewBox="0 0 1200 170" role="img">
<rect width="1200" height="170" rx="16" fill="{c['bg']}"/>
<rect x="1" y="1" width="1198" height="168" rx="16" fill="{c['panel']}" stroke="{c['border']}" stroke-width="2"/>
<text x="24" y="34" fill="{c['green']}" font-family="{FONT}" font-size="16" font-weight="700">GITHUB SIGNALS</text>'''
    ]
    for i, (label, value, color) in enumerate(cards):
        x = 24 + i * 292
        parts.append(
            f'<rect x="{x}" y="52" width="268" height="92" rx="12" fill="{c["panel2"]}" stroke="{color}" stroke-opacity=".4"/>'
            f'<text x="{x+18}" y="78" fill="{c["muted"]}" font-family="{FONT}" font-size="11">{label}</text>'
            f'<text x="{x+18}" y="118" fill="{c["text"]}" font-family="{FONT}" font-size="26" font-weight="700">{value}</text>'
        )
    parts.append("</svg>")
    stats_name = "stats.svg" if theme_name == "dark" else "stats-light.svg"
    (ASSETS / stats_name).write_text("".join(parts), encoding="utf-8")

    parts = [
        f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="260" viewBox="0 0 600 260" role="img">
<rect width="600" height="260" rx="16" fill="{c['bg']}"/>
<rect x="1" y="1" width="598" height="258" rx="16" fill="{c['panel']}" stroke="{c['border']}" stroke-width="2"/>
<text x="24" y="38" fill="{c['green']}" font-family="{FONT}" font-size="16" font-weight="700">RECENT ACTIVITY</text>'''
    ]
    colors = [c["green"], c["cyan"], c["purple"], c["pink"]]
    for i, event in enumerate(events[:4]):
        y = 82 + i * 42
        line = summarize(event)[:63]
        parts.append(
            f'<circle cx="31" cy="{y-5}" r="5" fill="{colors[i % 4]}"/>'
            f'<text x="49" y="{y}" fill="{c["text"]}" font-family="{FONT}" font-size="12">{escape(line)}</text>'
        )
    if not events:
        parts.append(
            f'<text x="24" y="88" fill="{c["muted"]}" font-family="{FONT}" font-size="12">No public events returned.</text>'
        )
    parts.append("</svg>")
    activity_name = "activity.svg" if theme_name == "dark" else "activity-light.svg"
    (ASSETS / activity_name).write_text("".join(parts), encoding="utf-8")


for name, palette in THEMES.items():
    render(name, palette)

print("Updated dark/light stats and activity panels")
