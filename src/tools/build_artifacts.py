#!/usr/bin/python3
"""Make artifact copies of repo pages: drop the html/head/body wrapper and the
back link, and point links between pages at the published artifact URLs."""
import pathlib, re

REPO = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129-study')
OUT = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')
OUT.mkdir(exist_ok=True)
EXAMPLES_URL = 'https://claude.ai/artifact/DVPDZGHpQJVjBLP8XZAraG'

WRAPPER = re.compile(r'^\s*(<!doctype html>|<html[^>]*>|<head>|<meta charset[^>]*>|<meta name="viewport"[^>]*>|</head>|<body>|</body>|</html>)\s*$', re.I)

for name in ('hw1.html', 'examples.html'):
    lines = (REPO / name).read_text(encoding='utf-8').splitlines()
    lines = [l for l in lines if not WRAPPER.match(l) and '<a class="back"' not in l]
    html = '\n'.join(lines) + '\n'
    html = html.replace('href="examples.html#', f'href="{EXAMPLES_URL}#')
    (OUT / name).write_text(html, encoding='utf-8')
    print(name, len(html))
