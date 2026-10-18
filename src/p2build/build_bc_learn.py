#!/usr/bin/python3
"""Assemble EE6129 Part B and Part C lecture pages (Part A style) from fragments.

pb_1..pb_6.html -> partB.html, pc_1..pc_6.html -> partC.html.
Writes the repo pages (standalone HTML) and artifact copies (no html/head/body
wrapper; cross-page links pointed at artifact URLs).
"""
import pathlib, sys

B = pathlib.Path(__file__).parent
REPO = pathlib.Path(__file__).resolve().parents[2]
ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')

css = (B / 'partA_style.css').read_text(encoding='utf-8')
rail_js = (B / 'partA_rail.js').read_text(encoding='utf-8')

EXTRA_CSS = '''
/* Part B/C additions */
.worked .wtext{min-width:0;}
.calc{overflow-x:auto;}
.figwrap svg text{fill:var(--ink);font-family:var(--f-body);}
'''

# repo href -> artifact href
LINKS = {
  'partC.html': 'https://claude.ai/artifact/DLKM7od5QZHLjbgEN6cALD',
  'bc-practice.html': 'https://claude.ai/artifact/Fx13NpGCHaY9ztzpnHKLLf',
}

PAGES = {
  'B': dict(
    out='partB.html', frags=[f'pb_{i}.html' for i in range(1, 7)],
    title='没有信号塔时网络怎么办',
    kicker='EE6129 · Part B 讲解 · 无线网络与 LTE',
    h1='没有信号塔时，网络怎么办',
    lede='从会议室里的 WiFi 讲起：802.11 怎么让一群设备轮流说话（DCF、PCF、退避、RTS/CTS），再到互相当基站的自组织网络和传感器网络，最后是 LTE 的全 IP 架构和物联网。每节标讲义页码，能算的地方都配了例题，假设你零基础。',
    meta=['◆ 对应 Part B 讲义 p.1–114', '◆ 共 7 章', '◆ 每节标讲义页码', '◆ 紫色框 = 课外补充'],
    next=('接下来', 'Part C 讲解：从三万五千公里外看地球', 'partC.html',
          '卫星轨道、仰角与覆盖几何、链路损耗、卫星版的 FDMA/TDMA 和切换。Part B 的题目在 <a href="bc-practice.html">Part B/C 练习页</a>。'),
  ),
  'C': dict(
    out='partC.html', frags=[f'pc_{i}.html' for i in range(1, 7)],
    title='从三万五千公里外看地球',
    kicker='EE6129 · Part C 讲解 · 卫星通信',
    h1='从三万五千公里外看地球',
    lede='把"基站"搬到天上：放多高（LEO、MEO、GEO）、能看到多大一片地球、信号路上损失多少、一颗卫星的容量怎么分给许多地面站，以及卫星飞走时怎么切换。几何和链路部分都用讲义的数字验算了一遍，假设你零基础。',
    meta=['◆ 对应 Part C 讲义 p.1–41', '◆ 共 6 章', '◆ 每节标讲义页码', '◆ 紫色框 = 课外补充'],
    next=('接下来', 'Part B/C 练习：概念题、计算题和随机出题', 'bc-practice.html',
          '每题都链接回本页对应章节，答错了可以直接回来看。'),
  ),
}

def build(spec, standalone):
    frags = ''.join((B / f).read_text(encoding='utf-8') for f in spec['frags'])
    meta = '\n'.join(f'        <span>{m}</span>' for m in spec['meta'])
    lbl, h4, href, p = spec['next']
    body = f'''<div class="mobtoc">
  <select id="mobNav" aria-label="跳转到章节"></select>
</div>

<div class="shell">
  <aside class="rail">
    <div class="rail-inner">
      <div class="rail-kicker">本篇目录</div>
      <ul class="rail-list" id="railList"></ul>
    </div>
  </aside>

  <main class="main">
    <header class="masthead">
      <div class="kicker">{spec['kicker']}</div>
      <h1>{spec['h1']}</h1>
      <p class="lede">{spec['lede']}</p>
      <div class="meta">
{meta}
      </div>
    </header>
{frags}
    <div class="next-up">
      <div class="lbl">{lbl}</div>
      <h4><a href="{href}">{h4}</a></h4>
      <p>{p}</p>
    </div>
  </main>
</div>
'''
    if not standalone:
        for repo, art in LINKS.items():
            body = body.replace(f'href="{repo}', f'href="{art}')
    head = f'<title>{spec["title"]}</title>\n<style>{css}{EXTRA_CSS}</style>\n'
    tail = f'\n<script>{rail_js}</script>\n'
    if standalone:
        return ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
                + head + '</head>\n<body>\n' + body + tail + '</body>\n</html>\n')
    return head + body + tail

ART.mkdir(exist_ok=True)
for spec in PAGES.values():
    (REPO / spec['out']).write_text(build(spec, True), encoding='utf-8')
    (ART / spec['out']).write_text(build(spec, False), encoding='utf-8')
    print('ok', spec['out'], (REPO / spec['out']).stat().st_size)

# re-insert the past exam questions (build_exams.py keeps them between PASTQ markers)
import subprocess
subprocess.run([sys.executable, str(B.parent / 'exams' / 'build_exams.py'), '--inject'], check=True)
