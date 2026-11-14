#!/usr/bin/python3
"""Put the 知识讲解 + 详细解析 box (src/explain/exm.py) at the end of each Part A example's solution
in examples.html, between <!-- XPL:id --> and <!-- /XPL:id -->, plus the box CSS (style#xpl-css).
Idempotent. Then run build_artifacts.py for the artifact copy."""
import pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'src' / 'explain'))
import xpl

X = xpl.load_available('examples')
f = REPO / 'examples.html'
s = f.read_text(encoding='utf-8')
s = re.sub(r'[ \t]*<!-- XPL:(\w+) -->.*?<!-- /XPL:\1 -->\n', '', s, flags=re.S)
s = re.sub(r'<style id="xpl-css">.*?</style>\n', '', s, flags=re.S)
n = 0
for qid in re.findall(r'<article class="ex"[^>]*id="(p\d+)"', s):
    if qid not in X:
        continue
    a = s.index(f'id="{qid}"')
    d = s.index('    <div class="done">', a)
    k = s.rindex('    </div>\n', a, d)          # end of the .sol block
    s = s[:k] + f'      <!-- XPL:{qid} -->\n{xpl.box(X[qid], "zh", "      ")}      <!-- /XPL:{qid} -->\n' + s[k:]
    n += 1
i = s.index('</style>') + len('</style>\n')
s = s[:i] + f'<style id="xpl-css">{xpl.CSS}</style>\n' + s[i:]
f.write_text(s, encoding='utf-8')
print('examples explain boxes:', n, 'of', len(X))
