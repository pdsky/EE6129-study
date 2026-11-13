#!/usr/bin/python3
"""Print the plain text of one or more sections of a learning page, to read before drawing its animation.
Usage: sec_text.py p2 6.3 [6.4 ...]     (page = p2 | A | B | C)"""
import pathlib, re, sys, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from inject_anim import sections_of, strip, PAGES, REPO

page = sys.argv[1]
s = strip((REPO / PAGES[page]).read_text(encoding='utf-8'))
secs = sections_of(s)
for k in sys.argv[2:]:
    a, b, e = secs[k]
    t = s[a:e]
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', t, flags=re.S)
    t = re.sub(r'<svg.*?</svg>', '[图]', t, flags=re.S)
    t = re.sub(r'<(br|/p|/li|/div|/h3|/tr|/summary|/dt|/dd)[^>]*>', '\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    print(f'===== {page} {k} =====\n{t.strip()}\n')
