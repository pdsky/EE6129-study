#!/usr/bin/python3
"""Put the 知识讲解 + 详细解析 box (src/explain/p2a|p2b|p2c.py) into every Part 2 practice question.

Chinese box: inside .sol-zh, just before <!-- PKP:id -->; English box: inside .sol-en, just before its
Key points box. Both between <!-- XPL:id --> and <!-- /XPL:id --> (idempotent).
add_en.py rewrites the English blocks, so run this after it:
add_zh → kp_prac → add_en → add_xpl → add_intent → quiz_marks → build_practice.
"""
import pathlib, re, sys

B = pathlib.Path(__file__).parent
sys.path.insert(0, str(B.parent / 'explain'))
import xpl

X = xpl.load_available('p2')


ZS = '<span class="zhsub xz" lang="zh-CN">'
PATS = (('p', r'<p\b[^>]*>(.*?)</p>'), ('li', r'<li\b[^>]*>(.*?)</li>'),
        ('td', r'<t([dh])\b[^>]*>(.*?)</t\1>'), ('ans', r'<div class="ans">(.*?)</div>'))


def _cells(body):
    """[(kind, inner_start, inner_end)] outside the English exam templates, in document order per kind."""
    tm = [(m.start(), m.end()) for m in re.finditer(r'<div class="tmpl".*?</div>', body, re.S)]
    out = {}
    for k, pat in PATS:
        lst = []
        for m in re.finditer(pat, body, re.S):
            if any(a <= m.start() < b for a, b in tm):
                continue
            g = m.lastindex
            lst.append((m.start(g), m.end(g)))
        out[k] = lst
    return out


def bilingual(en, zh):
    """English body with the matching Chinese under every paragraph / list item / table cell / summary line."""
    ce, cz = _cells(en), _cells(zh)
    ins = []
    for k in ce:
        assert len(ce[k]) == len(cz[k]), (k, len(ce[k]), len(cz[k]))
        for (a, b), (c, d) in zip(ce[k], cz[k]):
            z = re.sub(r'<div class="calc">.*?</div>', '', zh[c:d], flags=re.S).strip()
            if len(re.findall(r'[一-鿿]', z)) < (4 if k == 'td' else 2):
                continue
            inner = en[a:b]
            j = inner.find('<div')
            pos = a + j if j >= 0 else b
            ins.append((pos, ZS + z + '</span>'))
    for pos, frag in sorted(ins, reverse=True):
        en = en[:pos] + frag + en[pos:]
    return en


def wrap(qid, html, ind):
    return f'{ind}<!-- XPL:{qid} -->\n{html}{ind}<!-- /XPL:{qid} -->\n'


def apply():
    n = 0
    seen = set()
    for i in range(1, 9):
        f = B / f'prac_{i}.html'
        s = f.read_text(encoding='utf-8')
        s = re.sub(r'[ \t]*<!-- XPL:(\w+) -->.*?<!-- /XPL:\1 -->\n', '', s, flags=re.S)
        for qid in re.findall(r'<article class="ex" id="(p\dq\d+)">', s):
            if qid not in X:
                continue
            e = X[qid]
            k = s.index(f'      <!-- PKP:{qid} -->')
            s = s[:k] + wrap(qid, xpl.box(e, 'zh', '      '), '      ') + s[k:]
            a = s.index(f'    <!-- EN:{qid} -->')
            k = s.index('      <div class="pkp"><div class="lbl">◆ Key points', a)
            assert k < s.index(f'<!-- /EN:{qid} -->', a)
            be = dict(e, en=bilingual(e['en'], e['zh']),
                      title_en=f'<span>{e["title_en"]}{ZS}{e["title"]}</span></span>')
            s = s[:k] + wrap(qid, xpl.box(be, 'en', '      '), '      ') + s[k:]
            n += 1
            seen.add(qid)
        f.write_text(s, encoding='utf-8')
    missing = set(X) - seen
    assert not missing, missing
    print('explain boxes (zh + en):', n)


apply()
