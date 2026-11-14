#!/usr/bin/python3
"""Build the two EE6129 hub artifacts: 「EE6129 学习」 and 「EE6129 练习」.

Each hub is one page with a tab bar. The first tab is written here (exam guide / practice guide);
every other tab embeds one of the existing artifact pages (EE6129_artifacts/*.html) in an iframe
(srcdoc, created lazily on first open, so CSS/JS of the pages never clash).
Links inside an embedded page that point to another EE6129 artifact are rerouted: same hub → switch
tab (and scroll to the #anchor), other hub → open that hub at the right tab.

usage: build_hub.py [learn_hub_url practice_hub_url]
  writes EE6129_artifacts/hub-learn.html and hub-practice.html (publish those two files).
  Hub URLs are read from src/artifact_ids.json ("hub-learn", "hub-practice") when not given.
Run after the page builders (quiz_marks → build_learn → build_practice → build_exams …).
"""
import json, pathlib, sys

H = pathlib.Path(__file__).resolve().parent
REPO = H.parents[1]
ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')
HWSW = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_HW_SW/homework_sw.html')
IDS = json.loads((REPO / 'src' / 'artifact_ids.json').read_text(encoding='utf-8'))

def art_url(key):
    v = IDS.get(key, {}).get('new')
    return f'https://claude.ai/artifact/{v}' if v else ''

if len(sys.argv) == 3:
    HUB_URL = {'learn': sys.argv[1], 'practice': sys.argv[2]}
else:
    HUB_URL = {'learn': art_url('hub-learn'), 'practice': art_url('hub-practice')}

# tab id → (hub, label, short, source file, artifact-id key, repo file name)
TABS = [
    ('learn', 'guide', '考试指南', '指南', None, None, None),
    ('learn', 'p2', 'Part 2 · 信道到 OFDM', 'Part 2', ART / 'p2-learn.html', 'p2-learn', 'p2-learn.html'),
    ('learn', 'ch12', '第 1b–2 章题型总结', '1b–2 总结', ART / 'quiz-summary.html', 'quiz-summary', 'quiz-summary.html'),
    ('learn', 'A', 'Part A · 蜂窝网络', 'Part A', ART / 'partA.html', 'partA', 'partA.html'),
    ('learn', 'B', 'Part B · 无线系统', 'Part B', ART / 'partB.html', 'partB', 'partB.html'),
    ('learn', 'C', 'Part C · 卫星通信', 'Part C', ART / 'partC.html', 'partC', 'partC.html'),
    ('practice', 'guide', '怎么练', '指南', None, None, None),
    ('practice', 'exams', '历年期末真题', '真题', ART / 'exams.html', 'exams', 'exams.html'),
    ('practice', 'p2prac', 'Part 2 · Practice 1–7 + 模拟题', 'Part 2 练习', ART / 'p2-practice.html', 'p2-practice', 'p2-practice.html'),
    ('practice', 'Aex', 'Part A · 讲义例题', 'Part A 例题', ART / 'examples.html', 'examples', 'examples.html'),
    ('practice', 'hw1', 'Part 1 · HW1', 'HW1', ART / 'hw1.html', 'hw1', 'hw1.html'),
    ('practice', 'bc', 'Part B · C 练习', 'B·C 练习', ART / 'bc-practice.html', 'bc-practice', 'bc-practice.html'),
    ('practice', 'hwsw', 'Part 2 · 作业 (SW)', 'Part 2 作业', HWSW, 'homework-sw', 'homework_sw.html'),
]

# where every known artifact / file lives: id-or-filename → [hub, tab]
ROUTE = {}
for hub, tid, _l, _s, _src, key, fname in TABS:
    if key:
        v = IDS.get(key, {})
        for k in ('new', 'old'):
            if v.get(k):
                ROUTE[v[k]] = [hub, tid]
        ROUTE[fname] = [hub, tid]

CSS = r'''
:root{
  --bg:#eceff0; --surface:#fff; --surface-2:#e3e9e9; --border:#cbd6d7;
  --text:#13201f; --muted:#4e615f;
  --accent:#0f766e; --accent-strong:#0a5a53; --accent-soft:#d7eeeb; --on-accent:#fff;
  --p2:#2f4fc4; --pa:#b4790f; --warn-soft:#f7e8d2;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){color-scheme:dark;
    --bg:#0b1413; --surface:#111e1c; --surface-2:#182825; --border:#273a36;
    --text:#e6f0ed; --muted:#9ab3ad;
    --accent:#33d1bf; --accent-strong:#7ceede; --accent-soft:#113330; --on-accent:#08100e;
    --p2:#8fa6f5; --pa:#e0ac4b; --warn-soft:#2f2210;}
}
:root[data-theme="dark"]{color-scheme:dark;
  --bg:#0b1413; --surface:#111e1c; --surface-2:#182825; --border:#273a36;
  --text:#e6f0ed; --muted:#9ab3ad;
  --accent:#33d1bf; --accent-strong:#7ceede; --accent-soft:#113330; --on-accent:#08100e;
  --p2:#8fa6f5; --pa:#e0ac4b; --warn-soft:#2f2210;}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--text);font-family:'IBM Plex Sans','Noto Sans CJK SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif;display:flex;flex-direction:column;-webkit-font-smoothing:antialiased}
header.top{flex:none;background:var(--surface);border-bottom:1px solid var(--border);padding:8px 16px 0}
.row{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.brand{font-family:'Barlow Condensed','Noto Sans CJK SC',sans-serif;font-weight:700;font-size:1.35rem;letter-spacing:.01em}
.brand b{color:var(--accent)}
.sp{flex:1}
.switch{font-size:.82rem;font-weight:600;text-decoration:none;color:var(--accent-strong);border:1px solid var(--accent);border-radius:999px;padding:3px 12px;white-space:nowrap}
.switch:hover,.switch:focus-visible{background:var(--accent-soft)}
nav.tabs{display:flex;gap:2px;overflow-x:auto;scrollbar-width:thin;margin-top:6px;-webkit-overflow-scrolling:touch}
nav.tabs button{font:inherit;font-size:.88rem;font-weight:600;color:var(--muted);background:none;border:0;border-bottom:3px solid transparent;padding:8px 12px 7px;cursor:pointer;white-space:nowrap}
nav.tabs button:hover{color:var(--text)}
nav.tabs button[aria-selected="true"]{color:var(--accent-strong);border-bottom-color:var(--accent)}
nav.tabs .short{display:none}
main{flex:1;position:relative;min-height:0}
main > iframe,main > .pane{position:absolute;inset:0;width:100%;height:100%;border:0;background:var(--bg)}
.pane{overflow-y:auto}
.guide{max-width:880px;margin:0 auto;padding:24px 16px 60px;line-height:1.7}
.guide h1{font-family:'Barlow Condensed','Noto Sans CJK SC',sans-serif;font-size:2rem;margin:.1em 0 .2em;text-wrap:balance}
.guide h2{font-family:'Barlow Condensed','Noto Sans CJK SC',sans-serif;font-size:1.35rem;margin:1.6em 0 .4em}
.guide .lede{color:var(--muted);margin:0 0 1em;max-width:70ch}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:12px 0}
.fact{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 14px}
.fact .k{font-size:.75rem;color:var(--muted)}
.fact .v{font-weight:700;font-size:1.05rem}
.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.88rem;background:var(--surface)}
th,td{border:1px solid var(--border);padding:7px 10px;text-align:left;vertical-align:top}
thead th{background:var(--surface-2);white-space:nowrap}
td.q{font-weight:700;white-space:nowrap}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:10px 0}
a.card{display:block;text-decoration:none;color:inherit;background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:14px 16px}
a.card:hover,a.card:focus-visible{border-color:var(--accent)}
a.card .t{font-weight:700;color:var(--accent-strong)}
a.card .d{font-size:.85rem;color:var(--muted);margin-top:2px}
.tag{display:inline-block;font-size:.72rem;font-weight:700;border-radius:999px;padding:0 8px;margin-right:4px;border:1px solid}
.tag.p2{color:var(--p2);border-color:var(--p2)} .tag.pa{color:var(--pa);border-color:var(--pa)}
ol.steps li{margin:.35em 0}
.note{background:var(--warn-soft);border-radius:8px;padding:8px 12px;font-size:.88rem;margin:12px 0}
.loading{position:absolute;inset:0;display:grid;place-items:center;color:var(--muted);font-size:.9rem;pointer-events:none}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.xmap{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:12px;margin:10px 0 4px}
.xq{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:12px 14px 10px}
.xq h3{margin:0 0 2px;font-size:1rem;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.xq h3 .qn{font-family:'Barlow Condensed',sans-serif;font-size:1.35rem;color:var(--accent-strong)}
.xq .sub{font-size:.8rem;color:var(--muted);margin-bottom:6px}
.xr{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:4px 10px;padding:5px 2px;border-top:1px dashed var(--border);font-size:.86rem;line-height:1.4}
.xr a{color:inherit;text-decoration:none}
.xr a:hover,.xr a:focus-visible{color:var(--accent-strong);text-decoration:underline}
.xr .num{font-family:'Barlow Condensed',sans-serif;font-weight:700;color:var(--muted);margin-right:4px}
.xr .dots{display:inline-flex;gap:3px}
.xr .dots i{width:10px;height:10px;border-radius:50%;border:1.6px solid var(--hc);opacity:.45}
.xr .dots i.on{background:var(--hc);opacity:1}
.xr .cnt{font-size:.75rem;font-weight:700;color:var(--hc);white-space:nowrap}
.xr .qs{grid-column:2 / 4;font-size:.74rem;color:var(--muted)}
.h4{--hc:#c23a32} .h3,.h2{--hc:var(--pa)} .h1{--hc:var(--p2)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .h4{--hc:#f08a7e}}
:root[data-theme="dark"] .h4{--hc:#f08a7e}
.xleg{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:.8rem;color:var(--muted);margin:4px 0}
.xleg span{display:inline-flex;align-items:center;gap:5px}
.xleg i{width:10px;height:10px;border-radius:50%;background:var(--hc);display:inline-block}
@media (max-width:440px){.xmap{grid-template-columns:1fr}}
@media (max-width:640px){nav.tabs .long{display:none} nav.tabs .short{display:inline} .brand{font-size:1.15rem}}
'''

def tab_link(t, text):
    return f'<a href="#{t}" data-tab="{t}">{text}</a>'

def exam_map():
    """考试重点图: for each final-exam question, the lecture sections it tested in the 4 past papers."""
    sys.path.insert(0, str(REPO / 'src' / 'anim'))
    import re as _re
    from exam_hits import HITS, PAPERS, SHORT, load_questions
    from inject_anim import sections_of, strip, PAGES
    qs = load_questions()
    titles, has_anim = {}, set()
    for pg, fn in PAGES.items():
        src = (ART / fn).read_text(encoding='utf-8')
        has_anim |= {pg + ':' + m.replace('_', '.') for m in _re.findall(rf'id="asec-{pg}-([\d_]+)"', src)}
        st = strip(src)
        for sec, (a, b, e) in sections_of(st).items():
            h = st[a:b]
            h = _re.sub(r'<span class="zh-num">.*?</span>|<span class="imp[^"]*">.*?</span>', '', h)
            titles[pg + ':' + sec] = _re.sub(r'<[^>]+>', '', h).strip()
    groups = [('Q1', 'Part 2 · 信道、检测、分集、MIMO', '第 2–5 章'), ('Q2', 'Part 2 · 均衡 + OFDM', '第 6–7 章'),
              ('Q3', 'Part A · 蜂窝计算', 'Erlang、复用、SIR、扇区'), ('Q4', 'Part A/B/C · 简答', 'IoT 几乎每年')]
    tab = {'p2': 'p2', 'A': 'A', 'B': 'B', 'C': 'C'}
    pname = {'p2': 'Part 2', 'A': 'Part A', 'B': 'Part B', 'C': 'Part C'}
    order = [p for p, _ in PAPERS]
    cards = []
    for g, name, sub in groups:
        rows = {}
        for qid, secs in HITS.items():
            q = qs[qid]
            if not q['q'].startswith(g):
                continue
            for sec in secs:
                rows.setdefault(sec, []).append(q)
        def key(sec):
            pg, n = sec.split(':')
            return (-len({q['paper'] for q in rows[sec]}), list(tab).index(pg), [int(x) for x in n.split('.')])
        out = []
        for sec in sorted(rows, key=key):
            pg, n = sec.split(':')
            hit = {q['paper'] for q in rows[sec]}
            y = len(hit)
            dots = ''.join(f'<i class="{"on" if p in hit else ""}" title="{nm}"></i>' for p, nm in PAPERS)
            cnt = '4 年都考' if y == 4 else f'{y} / 4 年'
            anchor = f'asec-{pg}-{n.replace(".", "_")}' if sec in has_anim else ''
            ql = ' · '.join(f'{SHORT[q["paper"]]} {q["q"]}' for q in sorted(rows[sec], key=lambda q: order.index(q['paper'])))
            out.append(f'<div class="xr h{y}"><span class="dots">{dots}</span>'
                       f'<a href="#{tab[pg]}" data-tab="{tab[pg]}" data-anchor="{anchor}"><span class="num">{pname[pg] if pg != "p2" else ""} {n}</span>{titles[sec]}</a>'
                       f'<span class="cnt">{cnt}</span><span class="qs">{ql}</span></div>')
        cards.append(f'<div class="xq"><h3><span class="qn">{g}</span>{name}</h3><div class="sub">{sub} · 点小节名直接跳到讲解</div>{"".join(out)}</div>')
    legend = ('<div class="xleg"><span>四个圆点 = 2023-24 S2 · 2024-25 S2 · 2025-26 S1 · 2025-26 S2，实心 = 那份卷考了</span>'
              '<span class="h4"><i></i>4 年都考</span><span class="h3"><i></i>考过 2–3 年</span><span class="h1"><i></i>考过 1 次</span></div>')
    return legend + '<div class="xmap">' + ''.join(cards) + '</div>'


XMAP = exam_map()

GUIDE_LEARN = f'''
<div class="guide">
  <h1>EE6129 期末复习 · 学习</h1>
  <p class="lede">讲解按课程分成两部分：Part 2（Ser Wee，第 7–13 周，信道、检测、分集、MIMO、均衡、OFDM），以及 Part 1 的 A/B/C 三块（蜂窝网络、无线系统、卫星）。上面每个标签是一份完整的讲解页；做题请切到右上角的「练习」。</p>
  <div class="facts">
    <div class="fact"><div class="k">考试时间</div><div class="v">11 月 27 日（周五）2:30 pm</div></div>
    <div class="fact"><div class="k">时长 · 地点</div><div class="v">3 小时 · HALL N</div></div>
    <div class="fact"><div class="k">题量</div><div class="v">4 大题，Part 2 两题 + Part A 老师两题</div></div>
  </div>

  <h2>四道大题考什么（按 4 份历年卷）</h2>
  <div class="tw"><table>
    <thead><tr><th>题</th><th>出题人</th><th>历年固定内容</th><th>先看</th></tr></thead>
    <tbody>
      <tr><td class="q">Q1</td><td><span class="tag p2">Part 2</span></td><td>(a) 第 2 章信道：路径损耗、阴影中断、衰落类型、LCR/AFD、衰落余量、注水（2025-26 S1 换成第 3 章二进制检测）；(b) 第 4 章分集：选择分集 / MRC 的 SNR 与误码率；(c) 第 5 章 MIMO：空间复用、Alamouti、MIMO 容量</td><td>{tab_link('p2', 'Part 2 第 2–5 章')}、{tab_link('ch12', '1b–2 题型总结')}</td></tr>
      <tr><td class="q">Q2</td><td><span class="tag p2">Part 2</span></td><td>(a) 第 6 章均衡：离散 ISI 模型、迫零均衡、<b>残余 ISI 下的误码率（每年都考）</b>；(b) 第 7 章 OFDM：子载波数、循环前缀、功率损失（<b>每年都考</b>）</td><td>{tab_link('p2', 'Part 2 第 6–7 章')}</td></tr>
      <tr><td class="q">Q3</td><td><span class="tag pa">Part A</span></td><td>蜂窝计算：Erlang B / Erlang C、信道数与簇大小、SIR 选簇、小区分裂与扇区化、系统容量</td><td>{tab_link('A', 'Part A')}</td></tr>
      <tr><td class="q">Q4</td><td><span class="tag pa">Part A</span></td><td>简答：多址方式、HLR/VLR、信道分配、切换、AP 接入、卫星切换、传感器网络；<b>IoT 几乎每年都有</b></td><td>{tab_link('B', 'Part B')}、{tab_link('C', 'Part C')}、{tab_link('A', 'Part A')}</td></tr>
    </tbody>
  </table></div>

  <h2>考试重点图（按 4 份历年卷，哪一节考过几次）</h2>
  <p class="lede">每道大题下面列出历年真题实际考到的讲义小节，考的次数越多排越前。讲解页里这些小节的标题下面也有同样的「🎯 期末考点」标记，点上面的题号可以跳到章末那道真题。</p>
  {XMAP}

  <h2>老师说过的期末规则</h2>
  <ul>
    <li>Part 2：讲义里<b>蓝框公式要背</b>，没框的公式考试会给但要懂符号含义；不考积分；按步骤给分，dB ↔ 线性换算不写会扣分。</li>
    <li>Part 2 期末题出自 <b>Practice 题或讲义例题，或它们的变形</b>；把讲义和 7 份 Practice 吃透就够，不用看课外材料。老师说他出的两题比 Quiz 难。</li>
    <li>每份讲解页里粉色的「▶ 老师课上强调」框，是按上课录音整理的重点；章末附了对应的历年真题。</li>
    <li>每一小节都配了「▶ 动画示意」：窗口够宽时在正文右边，跟着你往下滚；手机或窄窗口时在小节标题下面。分步的点「下一步 ▶」一步步看，带滑块的可以拖动改参数，看结果怎么变。</li>
  </ul>

  <h2>建议的复习顺序</h2>
  <ol class="steps">
    <li>{tab_link('p2', 'Part 2')}：第 6 章均衡和第 7 章 OFDM 每年必考，先看；再看第 4 章分集、第 5 章 MIMO，最后回顾第 2–3 章。</li>
    <li>{tab_link('ch12', '第 1b–2 章题型总结')}：信道部分的 13 类计算题，每类有符号表、公式和步骤表，适合快速过一遍。</li>
    <li>{tab_link('A', 'Part A')}：重点在 Erlang B/C 查表、频率复用和 SIR、小区分裂与扇区化。</li>
    <li>{tab_link('B', 'Part B')} 和 {tab_link('C', 'Part C')}：Q4 简答的素材，背要点即可。</li>
    <li>每学完一块，到「练习」做对应的 Practice 和历年真题。</li>
  </ol>
  <div class="note">原来分开的 11 个页面都还在，链接没变；这两个总入口只是把它们按「学习 / 练习」归到一起。</div>
</div>
'''

GUIDE_PRACTICE = f'''
<div class="guide">
  <h1>EE6129 期末复习 · 练习</h1>
  <p class="lede">做题按优先级排：先做历年期末真题，再做 Part 2 的 7 份 Practice（老师说期末题出自 Practice 和讲义例题的变形），然后是 Part A 例题和 HW1，最后是 Part B·C 的概念题。讲解在右上角的「学习」。</p>

  <div class="cards">
    <a class="card" href="#exams" data-tab="exams"><div class="t">历年期末真题</div><div class="d">2023-24 S2 到 2025-26 S2 四份卷、16 道大题：原题、分步解答、出题规律</div></a>
    <a class="card" href="#p2prac" data-tab="p2prac"><div class="t">Part 2 · Practice 1–7 + 模拟题</div><div class="d">21 道 Practice 逐题详解（中英对照、官方答案核对）+ 第 1b–2 章自编模拟题 12 道 + 随机练习</div></a>
    <a class="card" href="#Aex" data-tab="Aex"><div class="t">Part A · 讲义例题</div><div class="d">Erlang B/C、频率复用、SIR、小区分裂等 15 道例题，带自测模式</div></a>
    <a class="card" href="#hw1" data-tab="hw1"><div class="t">Part 1 · HW1</div><div class="d">Part A 作业 3 道大题讲解和参考答案；其中两小题和期末真题完全相同</div></a>
    <a class="card" href="#bc" data-tab="bc"><div class="t">Part B · C 练习</div><div class="d">WLAN、自组网、传感器网络、LTE、IoT、卫星的 62 道选择 / 计算 / 简答题</div></a>
    <a class="card" href="#hwsw" data-tab="hwsw"><div class="t">Part 2 · 作业 (SW)</div><div class="d">MRC 输出 SNR、双发单收 vs SISO、4G→5G 论文：题目、英文答案、中文讲解</div></a>
  </div>

  <h2>每道大题对应练什么</h2>
  <div class="tw"><table>
    <thead><tr><th>期末题</th><th>先做</th><th>再做</th></tr></thead>
    <tbody>
      <tr><td class="q">Q1 <span class="tag p2">Part 2</span></td><td>{tab_link('exams', '真题')} 四年的 Q1</td><td>{tab_link('p2prac', 'Practice 1–5')}（信道、检测、分集、MIMO）+ 第 1b–2 章模拟题</td></tr>
      <tr><td class="q">Q2 <span class="tag p2">Part 2</span></td><td>{tab_link('exams', '真题')} 四年的 Q2</td><td>{tab_link('p2prac', 'Practice 6–7')}（均衡、OFDM）</td></tr>
      <tr><td class="q">Q3 <span class="tag pa">Part A</span></td><td>{tab_link('exams', '真题')} 四年的 Q3</td><td>{tab_link('Aex', 'Part A 例题')}、{tab_link('hw1', 'HW1')}</td></tr>
      <tr><td class="q">Q4 <span class="tag pa">Part A</span></td><td>{tab_link('exams', '真题')} 四年的 Q4</td><td>{tab_link('bc', 'Part B·C 练习')}的简答题</td></tr>
    </tbody>
  </table></div>
  <div class="note">做题时先盖住解答自己算；每道题都有「本题知识点」和「老师课上强调」框，对完答案再看。</div>
</div>
'''

JS = r'''
(function(){
  var HUB = document.body.dataset.hub;
  var stage = document.getElementById('stage');
  var frames = {}, pending = {};
  var tabs = Array.prototype.slice.call(document.querySelectorAll('nav.tabs button'));
  function wrap(html){
    return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">' +
      '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>' + html + '</body></html>';
  }
  function openOut(href){
    var a = document.createElement('a'); a.href = href; a.target = '_blank'; a.rel = 'noopener';
    document.body.appendChild(a); a.click(); a.remove();
  }
  function scrollInside(doc, id){
    if (!id) return;
    var el = null; try { el = doc.getElementById(decodeURIComponent(id)); } catch(e){}
    if (!el) { try { el = doc.querySelector('[name="' + id + '"]'); } catch(e){} }
    if (el) el.scrollIntoView({block:'start'});
  }
  function route(href){
    // returns [hub, tab, anchor] for links to EE6129 pages, else null
    var m = href.match(/artifact\/([A-Za-z0-9]{16,})(?:[^#]*)(?:#(.*))?$/);
    var key = null, anchor = null;
    if (m) { key = m[1]; anchor = m[2] || null; }
    else {
      var f = href.match(/^([\w.-]+\.html)(?:#(.*))?$/);
      if (f) { key = f[1]; anchor = f[2] || null; }
    }
    if (!key || !ROUTE[key]) return null;
    return [ROUTE[key][0], ROUTE[key][1], anchor];
  }
  function hook(doc){
    doc.addEventListener('click', function(e){
      if (e.defaultPrevented || e.button !== 0) return;
      var a = e.target.closest && e.target.closest('a[href]');
      if (!a) return;
      var href = a.getAttribute('href');
      if (!href) return;
      if (href.charAt(0) === '#') {           // in-page anchor: srcdoc would otherwise reload the hub
        e.preventDefault(); scrollInside(doc, href.slice(1)); return;
      }
      var r = route(href);
      if (r) {
        e.preventDefault();
        if (r[0] === HUB) show(r[1], r[2]);
        else if (HUBURL[r[0]]) openOut(HUBURL[r[0]] + '#' + r[1]);
        return;
      }
      if (/^(https?:|mailto:)/.test(href)) { e.preventDefault(); openOut(href); }
    });
  }
  function frameFor(id){
    if (frames[id]) return frames[id];
    var f = document.createElement('iframe');
    f.title = document.querySelector('nav.tabs button[data-tab="' + id + '"]').dataset.label;
    var ld = document.createElement('div'); ld.className = 'loading'; ld.textContent = '正在载入…';
    stage.appendChild(ld);
    f.addEventListener('load', function(){
      ld.remove();
      try { hook(f.contentDocument); } catch(e){}
      if (pending[id]) { var a = pending[id]; pending[id] = null; setTimeout(function(){ try { scrollInside(f.contentDocument, a); } catch(e){} }, 400); }
    });
    f.srcdoc = wrap(PAGES[id]);
    stage.appendChild(f);
    frames[id] = f;
    return f;
  }
  function show(id, anchor){
    if (!document.querySelector('nav.tabs button[data-tab="' + id + '"]')) id = 'guide';
    tabs.forEach(function(b){ b.setAttribute('aria-selected', b.dataset.tab === id ? 'true' : 'false'); });
    var guide = document.getElementById('guide');
    guide.hidden = id !== 'guide';
    Object.keys(frames).forEach(function(k){ frames[k].hidden = k !== id; });
    if (id !== 'guide') {
      var had = !!frames[id];
      if (anchor) pending[id] = anchor;
      var f = frameFor(id); f.hidden = false;
      if (had && anchor) { pending[id] = null; try { scrollInside(f.contentDocument, anchor); } catch(e){} }
    }
    var btn = document.querySelector('nav.tabs button[aria-selected="true"]');
    if (btn && btn.scrollIntoView) btn.scrollIntoView({block:'nearest', inline:'nearest'});
    if (location.hash.slice(1) !== id) { try { history.replaceState(null, '', '#' + id); } catch(e){ location.hash = id; } }
  }
  tabs.forEach(function(b){ b.addEventListener('click', function(){ show(b.dataset.tab); }); });
  document.getElementById('guide').addEventListener('click', function(e){
    var a = e.target.closest('a[data-tab]'); if (!a) return;
    e.preventDefault(); show(a.dataset.tab, a.dataset.anchor || null);
  });
  window.addEventListener('hashchange', function(){ show(location.hash.slice(1) || 'guide'); });
  show(location.hash.slice(1) || 'guide');
})();
'''


def embed(s):
    """Page HTML → a JS string literal that is safe inside <script>."""
    return json.dumps(s, ensure_ascii=False).replace('</', '<\\/').replace('<!--', '<\\u0021--')


def strip_skeleton(s):
    # the artifact copies carry no doctype; repo/full pages may — keep only what is inside <body> if present
    lo = s.lower()
    if '<body' in lo:
        i = lo.find('<body'); i = lo.find('>', i) + 1
        j = lo.rfind('</body>')
        head = ''
        if '<head' in lo:
            h1 = lo.find('<head'); h1 = lo.find('>', h1) + 1; h2 = lo.find('</head>')
            head = s[h1:h2]
        return head + s[i:j if j > 0 else len(s)]
    return s


def build(hub):
    tabs = [t for t in TABS if t[0] == hub]
    other = 'practice' if hub == 'learn' else 'learn'
    title = 'EE6129 学习' if hub == 'learn' else 'EE6129 练习'
    pages = {}
    for _h, tid, label, short, src, key, fname in tabs:
        if src is None:
            continue
        pages[tid] = strip_skeleton(src.read_text(encoding='utf-8'))
    buttons = ''.join(
        f'<button type="button" role="tab" data-tab="{tid}" data-label="{label}" aria-selected="false">'
        f'<span class="long">{label}</span><span class="short">{short}</span></button>'
        for _h, tid, label, short, *_ in tabs)
    other_url = HUB_URL.get(other) or ''
    switch = (f'<a class="switch" href="{other_url}">{"去练习 →" if hub == "learn" else "← 去学习"}</a>'
              if other_url else '')
    if art_url(f'hub-{hub}-en'):   # bilingual edition, built by src/en/build_en.py
        switch += f'<a class="switch" href="{art_url(f"hub-{hub}-en")}">中英对照版</a>'

    guide = GUIDE_LEARN if hub == 'learn' else GUIDE_PRACTICE
    data = ('var PAGES = {' + ','.join(f'"{k}":{embed(v)}' for k, v in pages.items()) + '};\n'
            f'var ROUTE = {json.dumps(ROUTE)};\nvar HUBURL = {json.dumps(HUB_URL)};\n')
    html = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n' f'<title>{title}</title>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">\n'
            f'<style>{CSS}</style>\n'
            f'<header class="top"><div class="row"><div class="brand">EE6129 · <b>{"学习" if hub == "learn" else "练习"}</b></div>'
            f'<span class="sp"></span>{switch}</div>\n'
            f'<nav class="tabs" role="tablist" aria-label="{title}">{buttons}</nav></header>\n'
            f'<main id="stage"><section class="pane" id="guide">{guide}</section></main>\n'
            f'<script>\n{data}</script>\n<script>{JS}</script>\n')
    html = html.replace('<body', '<body', 1)
    out = ART / f'hub-{hub}.html'
    # data-hub on body: the artifact skeleton supplies <body>, so set it from script instead
    html = html.replace('<script>{JS}', '')
    html = html.replace('var PAGES = {', f'document.body.dataset.hub = "{hub}";\nvar PAGES = {{', 1)
    out.write_text(html, encoding='utf-8')
    print(out.name, f'{out.stat().st_size/1e6:.2f} MB', 'tabs:', ', '.join(t[1] for t in tabs))


if __name__ == '__main__':
    build('learn')
    build('practice')
