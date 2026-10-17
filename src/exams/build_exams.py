#!/usr/bin/python3
"""EE6129 past exam papers: build the overview page and inject questions into the lecture pages.

usage: build_exams.py            build exams.html (repo + artifact copy) and inject into all lecture pages
       build_exams.py --inject   only (re)inject into the lecture pages (called by the lecture builders)

Question data: data_2324.py, data_2425.py, data_2526s1.py, data_2526s2.py (verified by verify.py).
Injected blocks sit between <!-- PASTQ:begin --> and <!-- PASTQ:end --> so re-running is idempotent.
"""
import json, pathlib, re, sys

E = pathlib.Path(__file__).parent
B = E.parent / 'p2build'
REPO = pathlib.Path(__file__).resolve().parents[2]
ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')
URLS = json.loads((E / 'urls.json').read_text(encoding='utf-8')) if (E / 'urls.json').exists() else {}
AURL = lambda key: 'https://claude.ai/artifact/' + key

sys.path.insert(0, str(E))
import data_2324, data_2425, data_2526s1, data_2526s2
QS = data_2324.QS + data_2425.QS + data_2526s1.QS + data_2526s2.QS
BYID = {q['id']: q for q in QS}
from kp_exams import KP
missing = [q['id'] for q in QS if q['id'] not in KP]
if missing:
    raise SystemExit(f'kp_exams.py has no knowledge points for: {missing}')

PAPERS = {
  'y2324s2': ('2023-24 S2', 'Semester 2 Examination 2023-2024', 'April / May 2024', 14),
  'y2425s2': ('2024-25 S2', 'Semester 2 Examination 2024-2025', 'April / May 2025', 15),
  'y2526s1': ('2025-26 S1', 'Semester 1 Examination 2025-2026', 'November / December 2025', 14),
  'y2526s2': ('2025-26 S2', 'Semester 2 Examination 2025-2026', 'April / May 2026', 11),
}
# lecture pages: key -> (repo file, artifact file, artifact id, short name)
PAGES = {
  'A':  ('partA.html', 'partA.html', '6Vp1fcfRZ4o2cfmUtFQtpG', 'Part A'),
  'B':  ('partB.html', 'partB.html', 'Rq8eSjXVaeEVwoUvRE411c', 'Part B'),
  'C':  ('partC.html', 'partC.html', '9gXNBydjgxgVdZQwSYLKfh', 'Part C'),
  'p2': ('p2-learn.html', 'p2-learn.html', 'G7A1bCLeHLqk5ywkZeTtwT', 'Part 2'),
}
HW1 = ('hw1.html', 'McfNsRbbazKMbWfp3FeM4B')
EXAMS = ('exams.html', URLS.get('exams'))
ZH = ['开篇', '第一章', '第二章', '第三章', '第四章', '第五章', '第六章', '第七章', '第八章', '第九章', '第十章']

def chapter_titles():
    out = {}
    for key, (repo, _, _, _) in PAGES.items():
        s = (REPO / repo).read_text(encoding='utf-8')
        for m in re.finditer(r'<section class="chapter" id="(ch\d+)".*?<h2>(.*?)</h2>', s, re.S):
            out[(key, m.group(1))] = re.sub(r'<[^>]+>', '', m.group(2))
    return out

CSS = '''
.pastq-block{margin:46px 0 10px;padding-top:26px;border-top:2px dashed var(--line-strong);}
.pastq-block > h3 .zh-num{background:var(--ink);color:var(--paper);padding:1px 7px;border-radius:5px;font-size:12.5px;}
.pq-intro{font-size:14.5px;color:var(--ink-soft);}
.pastq{border:1px solid var(--line-strong);border-radius:12px;background:var(--card);padding:16px 18px 10px;margin:18px 0 22px;box-shadow:var(--shadow);scroll-margin-top:60px;}
.pq-head{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;font-family:var(--f-mono);font-size:12px;}
.pq-head span{padding:2px 8px;border-radius:5px;border:1px solid var(--line-strong);color:var(--ink-soft);}
.pq-head .pq-paper{background:var(--ink);color:var(--paper);border-color:var(--ink);font-weight:600;}
.pq-head .pq-q{color:var(--accent-ink);border-color:var(--accent);font-weight:700;}
.pq-head .pq-quiz{background:var(--good-soft);color:var(--good);border-color:var(--good);font-weight:700;}
.pq-head .pq-hw{background:var(--gold-soft);color:var(--gold);border-color:var(--gold);}
.pq-head a{color:inherit;text-decoration:none;}
.pq-topic{font-size:14px;color:var(--ink-soft);margin:9px 0 4px;}
.pq-topic b{color:var(--ink);background:none;}
.pastq details > summary{cursor:pointer;font-weight:600;font-size:14px;color:var(--accent-ink);padding:6px 0;list-style:none;}
.pastq details > summary::-webkit-details-marker{display:none;}
.pastq details > summary::before{content:"▸ ";}
.pastq details[open] > summary::before{content:"▾ ";}
.pq-en{font-family:"Times New Roman",Georgia,'Literata',serif;font-size:15.5px;line-height:1.6;background:var(--paper-2);border-left:3px solid var(--ink-faint);border-radius:4px;padding:12px 16px;margin:4px 0 8px;overflow-x:auto;}
.pq-en p{margin:0 0 .7em;}
.pq-en .eq{display:block;text-align:center;margin:.45em 0;font-style:italic;white-space:normal;}
.pq-en .marks{text-align:right;font-size:13.5px;color:var(--ink-soft);}
.pq-en span.marks{display:inline;float:right;}
.pq-en .figwrap{background:var(--card);border-radius:6px;margin:8px 0;}
.pastq .worked{margin:6px 0 10px;}
.pastq .worked .wbody{font-size:15px;}
.pq-note{font-size:13.5px;background:var(--gold-soft);border-left:3px solid var(--gold);border-radius:4px;padding:8px 12px;margin:10px 0 2px;}
.pq-links{font-size:13px;font-family:var(--f-mono);margin:8px 0 4px;display:flex;flex-wrap:wrap;gap:4px 16px;}
.pq-links a{text-decoration:none;}
.pastq .figwrap svg{max-width:100%;height:auto;}
.pq-kp{border:1px solid var(--accent);border-left-width:5px;border-radius:10px;background:var(--accent-soft);padding:12px 16px 8px;margin:4px 0 10px;}
.pq-kp > .lbl{font-family:var(--f-mono);font-size:11px;letter-spacing:.08em;color:var(--accent-ink);font-weight:700;margin-bottom:4px;}
.pq-kp dl{margin:0;display:grid;grid-template-columns:max-content 1fr;gap:4px 14px;}
.pq-kp dt{font-weight:700;font-size:14px;color:var(--accent-ink);}
.pq-kp dd{margin:0;font-size:14.5px;color:var(--ink);line-height:1.65;}
@media (max-width:560px){.pq-kp dl{grid-template-columns:1fr;gap:0;}.pq-kp dt{margin-top:6px;}}
.pq-table td{font-family:var(--f-body);font-size:13.5px;line-height:1.55;vertical-align:top;}
'''

def chname(titles, page, ch):
    n = int(ch[2:])
    return f'{PAGES[page][3]} {ZH[n]}', titles.get((page, ch), '')

def link_page(page, ch, art):
    return (AURL(PAGES[page][2]) if art else PAGES[page][0]) + '#' + ch

def link_exams(qid, art):
    if art:
        return (AURL(EXAMS[1]) + '#' + qid) if EXAMS[1] else None
    return 'exams.html#' + qid

def render(q, ctx, art, titles):
    """ctx: 'lecture' (inside a lecture chapter) or 'exams' (overview page)."""
    pshort = PAPERS[q['paper']][0]
    marks = q.get('marks')
    marks_s = f'{marks} 分' if isinstance(marks, int) else (marks + ' 分' if marks else '')
    tags = [f'<span class="pq-paper">{pshort}</span>', f'<span class="pq-q">{q["q"]}</span>']
    if marks_s: tags.append(f'<span>{marks_s}</span>')
    if q.get('quiz'): tags.append('<span class="pq-quiz">Quiz 范围</span>')
    if q.get('hw'):
        href = AURL(HW1[1]) if art else HW1[0]
        tags.append(f'<span class="pq-hw"><a href="{href}">≡ {q["hw"]}</a></span>')
    cn, ct = chname(titles, q['page'], q['ch'])
    links = []
    if ctx == 'lecture':
        le = link_exams(q['id'], art)
        if le: links.append(f'<a href="{le}">→ 在「历年真题」页看整份 {pshort} 试卷</a>')
    else:
        links.append(f'<a href="{link_page(q["page"], q["ch"], art)}">→ 回到讲解：{cn} {ct}</a>')
    if q.get('same'):
        s = BYID[q['same']]
        anchor = ('#pq-' + s['id']) if ctx == 'lecture' and (s['page'], s['ch']) == (q['page'], q['ch']) else (
                 ('#' + s['id']) if ctx == 'exams' else None)
        if anchor: links.append(f'<a href="{anchor}">→ 同一道题：{PAPERS[s["paper"]][0]} {s["q"]}</a>')
    note = f'<div class="pq-note">注：{q["note"]}</div>' if q.get('note') else ''
    kp = '<div class="pq-kp"><div class="lbl">◆ 本题知识点</div><dl>' + ''.join(
        f'<dt>{lab}</dt><dd>{html}</dd>' for lab, html in KP[q['id']]) + '</dl></div>'
    qid = ('pq-' + q['id']) if ctx == 'lecture' else q['id']
    return f'''<div class="pastq" id="{qid}">
  <div class="pq-head">{''.join(tags)}</div>
  <div class="pq-topic"><b>考点</b>：{q['topic']}</div>
  <details class="pq-orig" open><summary>英文原题（逐字转录）</summary><div class="pq-en" lang="en">{q['en']}</div></details>
  <details class="pq-sol"><summary>看解答和知识点（建议先自己做一遍）</summary><div class="worked"><div class="wbody">{q['sol']}{note}</div></div>{kp}</details>
  <div class="pq-links">{''.join(links)}</div>
</div>
'''

# ---------------------------------------------------------------- injection
def inject_file(path, page, art, titles):
    if not path.exists():
        return 0
    s = path.read_text(encoding='utf-8')
    s = re.sub(r'\s*<!-- PASTQ:begin -->.*?<!-- PASTQ:end -->', '', s, flags=re.S)
    items = [q for q in QS if q['page'] == page]
    chs = []
    for q in items:
        if q['ch'] not in chs: chs.append(q['ch'])
    first = True
    for ch in chs:
        qs = [q for q in items if q['ch'] == ch]
        m = re.search(rf'<section class="chapter" id="{ch}"', s)
        if not m:
            raise SystemExit(f'{path.name}: chapter {ch} not found')
        end = s.index('</section>', m.end())
        papers = sorted({PAPERS[q['paper']][0] for q in qs})
        css = f'<style id="pastq-css">{CSS}</style>' if first else ''
        first = False
        block = (f'\n<!-- PASTQ:begin -->{css}<div class="pastq-block">'
                 f'<h3><span class="zh-num">真题</span>本章的历年期末考题（{len(qs)} 题）</h3>'
                 f'<p class="pq-intro">来自 {"、".join(papers)} 期末卷。原题照试卷逐字转录，先自己做，再展开解答。</p>'
                 + ''.join(render(q, 'lecture', art, titles) for q in qs)
                 + '</div><!-- PASTQ:end -->\n    ')
        s = s[:end] + block + s[end:]
    path.write_text(s, encoding='utf-8')
    return len(items)

def inject_all():
    titles = chapter_titles()
    for page, (repo, artf, _, _) in PAGES.items():
        n1 = inject_file(REPO / repo, page, False, titles)
        n2 = inject_file(ART / artf, page, True, titles)
        print(f'inject {page}: repo {n1}, artifact {n2}')
    # lecturer's in-class emphasis boxes (src/teacher) go in after the exam questions
    import subprocess
    subprocess.run([sys.executable, str(E.parent / 'teacher' / 'inject_teacher.py')], check=True)

# ---------------------------------------------------------------- overview page
MATRIX = {
 'y2324s2': ['信道（路径损耗、阴影中断、衰落类型、衰落余量）＋ SD 分集 ＋ 空间复用、Alamouti',
             'ISI 与线性均衡 ＋ OFDM（H<sub>k</sub>、保护间隔损失）',
             'Erlang B 反推小区半径、集群增益、扇区化 ＋ 三种多址',
             'IoT 两个栈、雾计算 ＋ 推导 SIR = 1.76 + 20 log N'],
 'y2425s2': ['信道（路径损耗图、AFD/LCR、注水）＋ SD 支路数 ＋ 分集复用折中、MIMO 容量',
             '迫零均衡、残余 ISI ＋ OFDM（速率、CP 表达式、等容量功率）',
             'FDD-TDMA 选簇、Erlang B、小区分裂、三扇区',
             'HLR/VLR ＋ IoT 四子层 ＋ Erlang B 中继效率'],
 'y2526s1': ['二进制检测（星座、高斯、Q(2)）＋ MRC 分集增益 ＋ SIMO、并行信道容量',
             'ISI 误码率、均衡器噪声增强 ＋ OFDM（子载波数、速率、相关器）',
             '小区数、信道数、频谱效率 ＋ Erlang C ＋ FCA/DCA',
             'WLAN 入网过程 ＋ IoT 五难点 ＋ 雾计算特征'],
 'y2526s2': ['衰落类型、LCR、衰落余量 ＋ 阵列增益 ＋ MIMO 模型、Alamouti 检测方差',
             'Nyquist 准则、均衡器噪声、残余 ISI ＋ OFDM（H<sub>k</sub>、IDFT、CP 损失）',
             '簇与系统容量 ＋ Erlang C ＋ M/M/m 推导',
             '硬/软切换 ＋ 卫星四种切换 ＋ WSN 架构 ＋ IoT 四子层'],
}

def first_id(paper, qn):
    for q in QS:
        if q['paper'] == paper and q['q'].startswith(f'Q{qn}'):
            return q['id']

def exams_page(art, titles):
    css = (B / 'partA_style.css').read_text(encoding='utf-8')
    rail = (B / 'partA_rail.js').read_text(encoding='utf-8')
    rows = ''
    for p, (short, _, date, _) in PAPERS.items():
        cells = ''.join(f'<td><a href="#{first_id(p, i + 1)}">Q{i + 1}</a> {t}</td>' for i, t in enumerate(MATRIX[p]))
        rows += f'<tr><td><a href="#{p}"><b>{short}</b></a><br><span style="font-size:11px">{date}</span></td>{cells}</tr>'
    quiz = [q for q in QS if q.get('quiz')] + [BYID['y2526s1-q1a']]
    quiz_li = ''.join(f'<li><a href="#{q["id"]}">{PAPERS[q["paper"]][0]} {q["q"]}</a>：{q["topic"]}</li>' for q in quiz)
    # where each question is explained
    by_ch = {}
    for q in QS:
        by_ch.setdefault((q['page'], q['ch']), []).append(q)
    order = ['p2', 'A', 'B', 'C']
    map_rows = ''
    for key in sorted(by_ch, key=lambda k: (order.index(k[0]), int(k[1][2:]))):
        cn, ct = chname(titles, *key)
        qs = ' · '.join(f'<a href="#{q["id"]}">{PAPERS[q["paper"]][0]} {q["q"]}</a>' for q in by_ch[key])
        map_rows += f'<tr><td><a href="{link_page(key[0], key[1], art)}">{cn}</a><br><span style="font-size:12px">{ct}</span></td><td>{len(by_ch[key])}</td><td>{qs}</td></tr>'
    hw_href = AURL(HW1[1]) if art else HW1[0]

    sections = ''
    for p, (short, title, date, pages) in PAPERS.items():
        qs = [q for q in QS if q['paper'] == p]
        sections += f'''
    <section class="chapter" id="{p}">
      <div class="chapter-head"><span class="chapter-num">{short}</span><h2>{date}</h2></div>
      <p class="pq-intro">{title} · 3 小时 · 闭卷 · 4 题全做、每题 25 分 · 试卷 {pages} 页（含附录）</p>
      {''.join(render(q, 'exams', art, titles) for q in qs)}
    </section>'''

    body = f'''<div class="mobtoc">
  <select id="mobNav" aria-label="跳转到章节"></select>
</div>
<div class="shell">
  <aside class="rail"><div class="rail-inner"><div class="rail-kicker">本页目录</div><ul class="rail-list" id="railList"></ul></div></aside>
  <main class="main">
    <header class="masthead">
      <div class="kicker">EE6129 · 历年期末真题 · 2024–2026</div>
      <h1>四份期末卷，逐题讲透</h1>
      <p class="lede">2023-24 S2、2024-25 S2、2025-26 S1、2025-26 S2 四份期末卷，16 道大题全部逐字转录英文原题，配中文分步解答。每道题也插进了对应讲解页的章节末尾，学完一章就能做那一章的真题。</p>
      <div class="meta"><span>◆ 4 份试卷 · 16 道大题</span><span>◆ 计算全部用脚本核对</span><span>◆ 标出 Quiz 范围</span><span>◆ 原题笔误已注明</span></div>
    </header>

    <section class="chapter" id="overview">
      <div class="chapter-head"><span class="chapter-num">总览</span><h2>先看出题规律</h2></div>
      <p>四份卷子的结构完全一样：3 小时、闭卷、4 道题全做、每题 25 分。附录给了傅里叶变换表、常用公式（高斯概率密度、Q 函数、SIR 与扇区化 SIR、Erlang B/C 公式、线性插值）、Erlang B 表、Erlang C 表和 Q 函数表，所以<b>这些公式不用背，但要会用、会查表</b>。</p>
      <div class="tblwrap"><table class="pq-table"><thead><tr><th>试卷</th><th>Q1 · Part 2</th><th>Q2 · Part 2</th><th>Q3 · Part A 计算</th><th>Q4 · 论述</th></tr></thead><tbody>{rows}</tbody></table></div>
      <h3><span class="zh-num">1</span>每年都考的固定套路</h3>
      <ul>
        <li><b>Q1、Q2 固定是 Part 2（Ser Wee），共 50 分。</b>Q1(a) 几乎每年都是第二章无线信道；Q1(b) 是分集加 MIMO。</li>
        <li><b>Q2(a) 4 年都考"有残余 ISI 时的误码率"</b>：P<sub>e</sub> = ½[Q((1−a)/σ) + Q((1+a)/σ)]，a 是残余 ISI 系数。这是最稳的送分题。</li>
        <li><b>Q2(b) 4 年都考 OFDM</b>：子信道增益 H<sub>k</sub>、保护间隔/循环前缀的功率损失 10 log[(NT<sub>s</sub>+T<sub>G</sub>)/NT<sub>s</sub>] 各考了 2 次。</li>
        <li><b>Q3 每年都是 Part A 的话务计算</b>：Erlang B（前两年）、Erlang C（后两年），配合簇大小、小区数、扇区化。</li>
        <li><b>Q4 每年都有 IoT</b>：通信网络层四个子层考了 2 次，雾计算考了 2 次。其余是 Part A/B/C 的概念题（HLR/VLR、WLAN 入网、切换、WSN）。</li>
        <li><b>HW1 的两道题原样出现过</b>：<a href="{hw_href}">HW1</a> Q1(b) ≡ 2024-25 Q4(c)，Q2(b) ≡ 2023-24 Q4(c)；HW1 Q1(a) 的系统组成也和 2024-25 Q4(a) 同源。</li>
      </ul>
      <h3><span class="zh-num">2</span>10 月 23 日 Quiz 相关的真题</h3>
      <p>Quiz 范围是 Ch1b、Ch2 和 Practice 1–2。下面这些真题（或其中的小问）落在范围内，可以当模拟题做，每题限时 10 分钟左右：</p>
      <ul>{quiz_li}</ul>
      <h3><span class="zh-num">3</span>每道题插在哪一章</h3>
      <div class="tblwrap"><table class="pq-table"><thead><tr><th>讲解章节</th><th>题数</th><th>真题</th></tr></thead><tbody>{map_rows}</tbody></table></div>
      <p class="pq-intro">说明：题目逐字转录自 NTU 图书馆提供的扫描版试卷，仅供个人复习，仓库保持私有。官方没有给答案，这里的解答是按讲义的定义和公式推出来的，所有数值都用脚本复核过；题意有歧义的地方在"注"里写明了另一种理解。</p>
    </section>
{sections}
  </main>
</div>
'''
    head = f'<title>EE6129 历年期末真题</title>\n<style>{css}{CSS}</style>\n'
    tail = f'<script>{rail}</script>\n'
    if not art:
        return ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
                + head + '</head>\n<body>\n' + body + tail + '</body>\n</html>\n')
    return head + body + tail

if __name__ == '__main__':
    if '--inject' not in sys.argv:
        titles = chapter_titles()
        (REPO / 'exams.html').write_text(exams_page(False, titles), encoding='utf-8')
        (ART / 'exams.html').write_text(exams_page(True, titles), encoding='utf-8')
        print('exams.html', (REPO / 'exams.html').stat().st_size, 'questions', len(QS))
    inject_all()
