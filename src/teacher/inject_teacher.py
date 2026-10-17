#!/usr/bin/python3
"""Insert the "老师课上强调" boxes (notes.py) into every study page, repo copy and artifact copy.

Idempotent: each box sits between <!-- TEACH:begin id --> and <!-- TEACH:end id -->.
Called at the end of build_exams.py --inject (so build_learn.py / build_bc_learn.py run it) and by build_practice.py.
Can also be run on its own after hand-editing partA.html.
"""
import pathlib, re, sys

T = pathlib.Path(__file__).resolve().parent
REPO = T.parents[1]
ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')
sys.path.insert(0, str(T))
from notes import NOTES

PAGES = {'p2': 'p2-learn.html', 'A': 'partA.html', 'B': 'partB.html', 'C': 'partC.html',
         'ex': 'exams.html', 'prac': 'p2-practice.html'}

CSS = '''<style id="teach-css">
:root{--teach:#a3214f;--teach-soft:#fcebf1;--teach-line:#eba3bd;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--teach:#f58db4;--teach-soft:rgba(245,141,180,.11);--teach-line:rgba(245,141,180,.4);}}
:root[data-theme="dark"]{--teach:#f58db4;--teach-soft:rgba(245,141,180,.11);--teach-line:rgba(245,141,180,.4);}
.teach{border:1px solid var(--teach-line);border-left:5px solid var(--teach);border-radius:10px;background:var(--teach-soft);padding:10px 16px 6px;margin:14px 0 22px;font-size:14.5px;line-height:1.7;}
.teach > .lbl{font-size:12px;font-weight:700;letter-spacing:.04em;color:var(--teach);margin-bottom:4px;}
.teach > .lbl span{font-weight:500;opacity:.8;}
.teach.big > .lbl{font-size:15px;}
.teach ul{margin:0 0 .4em;padding-left:1.25em;}
.teach li{margin-bottom:.35em;}
.teach mark.hl{background:linear-gradient(to bottom,transparent 45%,var(--teach-line) 45%);color:inherit;font-weight:600;}
.exam .ex:not(.open) .teach{display:none;}
</style>'''


def box(i, note, css):
    head = note['title'] or '老师课上强调'
    cls = 'teach big' if note['big'] else 'teach'
    items = ''.join(f'<li>{x}</li>' for x in note['items'])
    return (f'<!-- TEACH:begin {i} -->{css}<div class="{cls}"><div class="lbl">▶ {head}'
            f' <span>· {note["src"]}</span></div><ul>{items}</ul></div><!-- TEACH:end {i} -->\n')


def position(s, at):
    kind, key = at
    if kind == 'chapter':
        m = re.search(rf'<section class="chapter" id="{key}"', s)
        if not m:
            return -1
        j = s.find('class="chapter-head"', m.end())
        j = s.find('</div>', j) + len('</div>')
        return s.find('\n', j) + 1
    if kind == 'h3':
        j = s.find(f'<span class="zh-num">{key}</span>')
        if j < 0:
            return -1
        j = s.find('</h3>', j) + len('</h3>')
        return s.find('\n', j) + 1
    if kind == 'article':
        a = s.find(f'<article class="ex" id="{key}">')
        if a < 0:
            return -1
        d = s.find('<div class="done">', a)
        return s.rfind('\n', a, d) + 1
    raise ValueError(kind)


def inject(path, page):
    if not path.exists():
        return 0
    s = path.read_text(encoding='utf-8')
    s = re.sub(r'<!-- TEACH:begin (\d+) -->.*?<!-- TEACH:end \1 -->\n', '', s, flags=re.S)
    n, first = 0, True
    for i, note in enumerate(NOTES):
        if note['page'] != page:
            continue
        p = position(s, note['at'])
        if p <= 0:
            raise SystemExit(f'{path.name}: anchor {note["at"]} not found')
        s = s[:p] + box(i, note, CSS if first else '') + s[p:]
        first = False
        n += 1
    path.write_text(s, encoding='utf-8')
    return n


if __name__ == '__main__':
    out = []
    for page, fn in PAGES.items():
        a = inject(REPO / fn, page)
        b = inject(ART / fn, page)
        out.append(f'{page} {a}/{b}')
    print('teacher notes:', ', '.join(out))
