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
            s = s[:k] + wrap(qid, xpl.box(e, 'en', '      '), '      ') + s[k:]
            n += 1
            seen.add(qid)
        f.write_text(s, encoding='utf-8')
    missing = set(X) - seen
    assert not missing, missing
    print('explain boxes (zh + en):', n)


apply()
