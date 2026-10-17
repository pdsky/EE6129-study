#!/usr/bin/python3
"""Add an English solution (from sol_en.py) next to each Chinese solution in prac_1..7.html.

The Chinese block becomes <div class="sol sol-zh">, the English one <div class="sol sol-en" lang="en">,
placed right after it between <!-- EN:id --> and <!-- /EN:id -->. The page toggle (解答 EN / 中文)
shows one of them. Idempotent. Run after kp_prac.py and before build_practice.py.
"""
import pathlib, re, sys

B = pathlib.Path(__file__).parent
sys.path.insert(0, str(B))
from sol_en import EN


def render(qid, d):
    out = ['    <div class="sol sol-en" lang="en">']
    if d.get('idea'):
        out.append(f'      <p class="idea"><b>Approach:</b> {d["idea"]}</p>')
    out.append('      <ol class="steps">')
    out += [f'        <li>{s}</li>' for s in d['steps']]
    out.append('      </ol>')
    out.append(f'      <div class="ans">{d["ans"]}</div>')
    out.append(f'      <div class="official"><b>Official answer:</b> {d["official"]}</div>')
    if d.get('note'):
        out.append(f'      <div class="note">{d["note"]}</div>')
    rows = ''.join(f'<dt>{lab}</dt><dd>{html}</dd>' for lab, html in d['kp'])
    out.append(f'      <div class="pkp"><div class="lbl">◆ Key points</div><dl>{rows}</dl></div>')
    out.append('    </div>')
    return f'    <!-- EN:{qid} -->\n' + '\n'.join(out) + f'\n    <!-- /EN:{qid} -->\n'


def apply():
    n = 0
    for i in range(1, 8):
        f = B / f'prac_{i}.html'
        s = f.read_text(encoding='utf-8')
        s = re.sub(r'    <!-- EN:(\w+) -->.*?<!-- /EN:\1 -->\n', '', s, flags=re.S)
        s = s.replace('<div class="sol">', '<div class="sol sol-zh">')
        for qid in re.findall(r'<article class="ex" id="(p\dq\d)">', s):
            a = s.find(f'<article class="ex" id="{qid}">')
            d = s.find('    <div class="done">', a)
            s = s[:d] + render(qid, EN[qid]) + s[d:]
            n += 1
        f.write_text(s, encoding='utf-8')
    print('english solutions:', n)

apply()
