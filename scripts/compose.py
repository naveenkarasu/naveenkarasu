"""Compose multi-panel rows into single images.

GitHub always draws gray borders around README table cells, so rows that need panels
side by side or stacked (and no per-panel links) are composed here into one SVG that
spans the 1200px page grid. Run after the other generators: it embeds their output.
"""
import re
from base64 import b64encode
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
W, G = 1200, 20  # page grid width and gutter, shared by every row


def size(name):
    head = (ASSETS / name).read_text(encoding='utf-8')[:400]
    w, h = re.search(r'width="([\d.]+)" height="([\d.]+)"', head).groups()
    return float(w), float(h)


def img(name, x, y, w, h):
    uri = 'data:image/svg+xml;base64,' + b64encode((ASSETS / name).read_bytes()).decode('ascii')
    return f'<image href="{uri}" x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"/>'


def svg(h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h:.0f}" '
            f'viewBox="0 0 {W} {h:.0f}" role="img">{body}</svg>')


def hero(sfx):
    """Avatar card on the left; intro + status (equal height) stacked over skills on the right."""
    avatar, intro, status, skills = (f'{n}{sfx}.svg' for n in ('ascii-profile', 'intro', 'system-status', 'skills'))
    (aw, ah), (iw, ih), (sw, sh), (kw, kh) = map(size, (avatar, intro, status, skills))

    def layout(wr):
        wi = (wr - G) / (1 + ih * sw / (iw * sh))  # intro width so intro and status share one height
        h1 = wi * ih / iw
        return wi, h1, (wr - G - wi), h1 + G + wr * kh / kw, (W - G - wr) * ah / aw

    # left height falls and right height rises linearly with wr: solve left == right
    f = lambda wr: layout(wr)[4] - layout(wr)[3]  # noqa: E731
    a, b = 600.0, 1000.0
    wr = a - f(a) * (b - a) / (f(b) - f(a))
    wi, h1, ws, right_h, left_h = layout(wr)
    wl = W - G - wr
    body = (img(avatar, 0, 0, wl, left_h)
            + img(intro, wl + G, 0, wi, h1)
            + img(status, wl + G + wi + G, 0, ws, h1)
            + img(skills, wl + G, h1 + G, wr, wr * kh / kw))
    return svg(max(left_h, right_h), body)


def pair(left, right, sfx):
    """Two equal panels side by side with one gutter."""
    l, r = f'{left}{sfx}.svg', f'{right}{sfx}.svg'
    cw = (W - G) / 2
    (lw, lh), (rw, rh) = size(l), size(r)
    return svg(max(cw * lh / lw, cw * rh / rw), img(l, 0, 0, cw, cw * lh / lw) + img(r, cw + G, 0, cw, cw * rh / rw))


for sfx in ('', '-light'):
    (ASSETS / f'hero{sfx}.svg').write_text(hero(sfx), encoding='utf-8')
    (ASSETS / f'activity-row{sfx}.svg').write_text(pair('activity', 'achievements', sfx), encoding='utf-8')
print('Composed hero and activity rows')
