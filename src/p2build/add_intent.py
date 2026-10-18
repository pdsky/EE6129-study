#!/usr/bin/python3
"""Insert the 题意讲解 box (intent.py) into every practice question in prac_1..7.html.

The box goes right after the chips line and before the 显示解答 button, outside <div class="sol">,
so it stays available in 自测模式. Idempotent: each box is between <!-- INTENT:id --> and
<!-- /INTENT:id -->. Run before build_practice.py (any order relative to kp_prac.py / add_en.py).
"""
import pathlib, re, sys

B = pathlib.Path(__file__).parent
sys.path.insert(0, str(B))
from intent import INTENT


def render(qid, d):
    o = ['      <details class="deep intent">',
         '        <summary>题意讲解：这道题到底要干嘛</summary>',
         '        <div class="deep-body">',
         '          <h4><span class="st">场景</span>题目在讲一件什么事</h4>']
    o += [f'          <p>{p}</p>' for p in d['scene']]
    rows = ''.join(f'<tr><td>{s}</td><td>{m}</td></tr>' for s, m in d['symbols'])
    o += ['          <h4><span class="st">符号</span>题目里每个量是什么</h4>',
          f'          <div class="tw"><table class="sym"><tbody>{rows}</tbody></table></div>',
          '          <h4><span class="st">要求</span>每一问在问什么</h4>',
          '          <ul>']
    o += [f'            <li><b>{lab}</b> {txt}</li>' for lab, txt in d['parts']]
    o.append('          </ul>')
    if d['traps']:
        o += ['          <h4><span class="st">注意</span>读题容易误会的地方</h4>', '          <ul>']
        o += [f'            <li>{t}</li>' for t in d['traps']]
        o.append('          </ul>')
    o += ['          <h4><span class="st">目的</span>这道题想让你明白什么</h4>',
          f'          <p>{d["point"]}</p>',
          f'          <div class="ans">一句话：{d["line"]}</div>',
          '        </div>',
          '      </details>']
    return f'    <!-- INTENT:{qid} -->\n' + '\n'.join(o) + f'\n    <!-- /INTENT:{qid} -->\n'


def apply():
    n = 0
    for i in range(1, 8):
        f = B / f'prac_{i}.html'
        s = f.read_text(encoding='utf-8')
        s = re.sub(r'    <!-- INTENT:(\w+) -->.*?<!-- /INTENT:\1 -->\n', '', s, flags=re.S)
        for qid in re.findall(r'<article class="ex" id="(p\dq\d)">', s):
            if qid not in INTENT:
                raise SystemExit(f'intent.py has no 题意讲解 for {qid}')
            a = s.find(f'<article class="ex" id="{qid}">')
            j = s.find('    <button class="reveal"', a)
            s = s[:j] + render(qid, INTENT[qid]) + s[j:]
            n += 1
        f.write_text(s, encoding='utf-8')
    print('intent boxes:', n)

apply()
