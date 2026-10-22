#!/usr/bin/python3
"""Assemble the CA2 Quiz example summary (quiz-summary.html) from the topic fragments in this folder.

Fragments frag_<key>.html each hold one or more <section class="topic" id="tN"> blocks (symbols table,
formulas, steps table with a past-final and a mock column, Chinese worked examples, traps, exam English).
Numbers: check_<key>.py (writer) and _verify_<key>.py (independent re-check).
usage: build_quizsum.py   — writes <repo>/quiz-summary.html and the artifact copy in EE6129_artifacts/
"""
import pathlib, re

B = pathlib.Path(__file__).parent
REPO = pathlib.Path(__file__).resolve().parents[2]
ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')

ARTURL = {'p2-learn.html': 'https://claude.ai/artifact/2oFi3Q2EigxutPVdykK7SQ',
          'p2-practice.html': 'https://claude.ai/artifact/NSSpuGLFTduzmgbBqZ1RSS',
          'exams.html': 'https://claude.ai/artifact/Ui8bXNmbpxttcCYkywnxFD'}

ORDER = ['prob_db', 'pathloss', 'shadow', 'rayleigh', 'fadetype', 'lcr', 'capacity']
PARTS = [('概率与 dB', ['t1', 't2']),
         ('大尺度：路径损耗与阴影', ['t3', 't4', 't5']),
         ('小尺度：多径衰落', ['t6', 't7', 't8', 't9', 't10']),
         ('信道容量', ['t11', 't12', 't13'])]
SHORT = {'t1': '概率', 't2': 'dB / SNR', 't3': '路径损耗', 't4': '最小二乘', 't5': '阴影中断',
         't6': '瑞利', 't7': '莱斯 K', 't8': '时延扩展', 't9': '多普勒·衰落类型', 't10': 'LCR / AFD',
         't11': '香农·SINR', 't12': '中断容量', 't13': '注水'}

CSS = r'''
:root{
  --bg:#eceff0; --surface:#fff; --surface-2:#e3e9e9; --border:#cbd6d7;
  --text:#13201f; --muted:#4e615f;
  --accent:#0f766e; --accent-strong:#0a5a53; --accent-soft:#d7eeeb; --on-accent:#fff;
  --must:#1f4fb8; --must-soft:#e2eafb; --try:#8a5a0b; --try-soft:#f7ead2;
  --give:#4e615f; --give-soft:#e3e9e9; --def:#137a3f; --def-soft:#dcf1e3;
  --bad:#a3261e; --bad-soft:#fbe3e0; --en:#6b46b0; --en-soft:#f2ecfb;
  --shadow:0 1px 2px rgba(19,32,31,.06),0 8px 22px rgba(19,32,31,.07);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --bg:#0b1413; --surface:#111e1c; --surface-2:#182825; --border:#273a36;
    --text:#e6f0ed; --muted:#9ab3ad;
    --accent:#33d1bf; --accent-strong:#7ceede; --accent-soft:#113330; --on-accent:#08100e;
    --must:#8fb0ff; --must-soft:#16233f; --try:#f0b56a; --try-soft:#2f2210;
    --give:#9ab3ad; --give-soft:#182825; --def:#4fd087; --def-soft:#12301f;
    --bad:#f2857c; --bad-soft:#351816; --en:#b79cf0; --en-soft:rgba(183,156,240,.12);
    --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 22px rgba(0,0,0,.4);
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --bg:#0b1413; --surface:#111e1c; --surface-2:#182825; --border:#273a36;
  --text:#e6f0ed; --muted:#9ab3ad;
  --accent:#33d1bf; --accent-strong:#7ceede; --accent-soft:#113330; --on-accent:#08100e;
  --must:#8fb0ff; --must-soft:#16233f; --try:#f0b56a; --try-soft:#2f2210;
  --give:#9ab3ad; --give-soft:#182825; --def:#4fd087; --def-soft:#12301f;
  --bad:#f2857c; --bad-soft:#351816; --en:#b79cf0; --en-soft:rgba(183,156,240,.12);
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 22px rgba(0,0,0,.4);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:'IBM Plex Sans','Noto Sans CJK SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:940px;margin:0 auto;padding-inline:16px;padding-block:28px 90px}
h1,h2,h3,h4{font-family:'Barlow Condensed','Noto Sans CJK SC','Microsoft YaHei',sans-serif;font-weight:700;margin:0 0 .3em;text-wrap:balance;line-height:1.2;letter-spacing:.01em}
h1{font-size:2.4rem} h2{font-size:1.6rem} h3{font-size:1.15rem;margin-top:1.5em;color:var(--accent-strong)} h4{font-size:1.02rem;margin-top:1.1em}
a{color:var(--accent-strong)}
.back{font-size:.82rem;text-decoration:none;color:var(--muted)}
.eyebrow{font-family:'IBM Plex Mono',monospace;font-size:.7rem;letter-spacing:.09em;text-transform:uppercase;color:var(--accent-strong);margin:14px 0 6px}
.lede{color:var(--muted);max-width:68ch;margin:.2em 0 .9em}
.notice{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 16px;font-size:.9rem;max-width:76ch;margin:0 0 12px}
.notice p{margin:.3em 0}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:.84rem;color:var(--muted);margin:8px 0 0}
.st{display:inline-block;vertical-align:middle;font-family:'IBM Plex Mono','Noto Sans CJK SC',monospace;font-size:.72rem;font-weight:700;line-height:1.5;padding:1px 9px;border-radius:999px;border:1px solid;white-space:nowrap;margin-right:4px}
.st.must{color:var(--must);border-color:var(--must);background:var(--must-soft)}
.st.try{color:var(--try);border-color:var(--try);background:var(--try-soft)}
.st.give{color:var(--give);border-color:var(--border);background:var(--give-soft)}
.st.def{color:var(--def);border-color:var(--def);background:var(--def-soft)}
nav.toc{position:sticky;top:env(safe-area-inset-top,0px);z-index:10;background:var(--bg);border-bottom:1px solid var(--border);padding:10px 0 8px;margin:18px 0 8px;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
nav.toc a{font-size:.8rem;font-weight:600;text-decoration:none;color:var(--muted);background:var(--surface);border:1px solid var(--border);border-radius:999px;padding:3px 11px;white-space:nowrap}
nav.toc a:hover,nav.toc a:focus-visible{color:var(--accent-strong);border-color:var(--accent)}
nav.toc .spacer{flex:1}
.toggle{display:flex;align-items:center;gap:6px;font-size:.82rem;color:var(--muted);cursor:pointer}
.toggle input{accent-color:var(--accent);width:16px;height:16px}
.part{font-family:'IBM Plex Mono',monospace;font-size:.74rem;letter-spacing:.09em;text-transform:uppercase;color:var(--accent-strong);margin:44px 0 0;padding-top:10px;border-top:2px solid var(--accent)}
section.topic{background:var(--surface);border:1px solid var(--border);border-radius:14px;box-shadow:var(--shadow);padding:22px 24px 20px;margin:16px 0 26px;scroll-margin-top:70px}
section.topic h2 .tn{display:inline-grid;place-items:center;min-width:1.7em;height:1.7em;margin-right:.45em;border-radius:8px;background:var(--accent);color:var(--on-accent);font-size:.85em;vertical-align:.08em;padding:0 .25em}
.meta{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:4px 0 8px}
.freq{font-size:.8rem;color:var(--muted)}
.why{background:var(--accent-soft);border-radius:8px;padding:8px 12px;margin:6px 0 4px;max-width:none}
.tw{overflow-x:auto;margin:8px 0;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;font-size:.88rem;width:100%;font-variant-numeric:tabular-nums}
th,td{border:1px solid var(--border);padding:6px 9px;text-align:left;vertical-align:top}
thead th{background:var(--surface-2);font-weight:600;white-space:nowrap}
table.sym td:first-child{white-space:nowrap;font-weight:600}
table.steps td:first-child{white-space:nowrap;font-weight:700;color:var(--accent-strong)}
table.steps th:nth-child(3),table.steps th:nth-child(4){color:var(--accent-strong)}
.src{font-size:.8rem;color:var(--muted);margin:4px 0 0}
.fm{border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:8px;padding:8px 14px;margin:10px 0;background:var(--surface)}
.fm .fl{font-weight:600;font-size:.92rem}
.fm .fl .st{margin-left:6px}
.fm .fx{overflow-x:auto;overflow-y:hidden;margin:2px 0}
.fm .fn{font-size:.86rem;color:var(--muted)}
.eg{border:1px solid var(--border);border-radius:10px;padding:10px 16px 8px;margin:12px 0;background:var(--surface)}
.egh{font-weight:700;color:var(--accent-strong)}
.eg .q{margin:.3em 0 .2em}
.eg ol.work{margin:.3em 0;padding-left:1.4em}
.eg ol.work li{margin:.15em 0}
.eg .ans{font-weight:600;background:var(--def-soft);border-radius:6px;padding:4px 10px;margin:.4em 0 .3em;display:inline-block}
.reveal{display:none;font:inherit;font-size:.82rem;font-weight:600;padding:3px 12px;border-radius:999px;border:1px solid var(--accent);background:var(--surface);color:var(--accent-strong);cursor:pointer;margin:4px 0}
body.selftest .eg:not(.open) .work,body.selftest .eg:not(.open) .ans{display:none}
body.selftest .eg .reveal{display:inline-block}
ul.trap{padding-left:0;list-style:none;margin:6px 0}
ul.trap li{position:relative;padding:4px 10px 4px 30px;margin:4px 0;background:var(--bad-soft);border-radius:6px}
ul.trap li::before{content:"✗";position:absolute;left:11px;top:4px;color:var(--bad);font-weight:700}
.en{border:1px solid var(--en);border-radius:10px;background:var(--en-soft);padding:8px 14px;margin:16px 0 4px}
.enl{font-family:'IBM Plex Mono',monospace;font-size:.72rem;letter-spacing:.06em;color:var(--en);font-weight:600}
.en p{margin:.3em 0}
table.cheat td:nth-child(2){white-space:nowrap}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
mjx-container[display="true"]{overflow-x:auto;overflow-y:hidden;max-width:100%}
td mjx-container{overflow:visible!important}
@media (max-width:640px){mjx-container:not([display="true"]){display:inline-block;max-width:100%;overflow-x:auto;overflow-y:hidden;vertical-align:middle}
  h1{font-size:1.9rem} section.topic{padding:16px 14px} nav.toc a{font-size:.75rem;padding:2px 9px}}
footer{margin-top:40px;font-size:.8rem;color:var(--muted);max-width:76ch}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
'''

MATHJAX = '''<script>
window.MathJax = {
  tex: { inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']] },
  svg: { fontCache: 'global' },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js" async></script>'''

JS = r'''
(function(){
  var box = document.getElementById('selftest');
  document.querySelectorAll('.eg').forEach(function(eg){
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'reveal'; b.textContent = '显示步骤和答案';
    b.addEventListener('click', function(){ eg.classList.toggle('open'); b.textContent = eg.classList.contains('open') ? '收起' : '显示步骤和答案'; });
    var at = eg.querySelector('.q') || eg.querySelector('.egh');
    if (at) at.insertAdjacentElement('afterend', b); else eg.prepend(b);
  });
  function set(on){ document.body.classList.toggle('selftest', on); try { localStorage.setItem('qs-selftest', on ? '1' : '0'); } catch(e){} }
  var on = false; try { on = localStorage.getItem('qs-selftest') === '1'; } catch(e){}
  box.checked = on; set(on);
  box.addEventListener('change', function(){ set(box.checked); });
})();
'''

HEAD = '''<div class="wrap">
  <a class="back" href="index.html">← 学习站目录</a>
  <div class="eyebrow">EE6129 Part 2 · CA2 Quiz · Fri 23 Oct 2026</div>
  <h1>Quiz 例题总结</h1>
  <p class="lede">Quiz 范围内的 13 类题，每类都按同一个顺序写：先把符号和含义用中英文列出来，再给公式（标出要背还是考试给），然后用一张“步骤 × 真题 × 模拟题”的对照表走一遍，最后用几个中文例子练变形，附易错点和英文答题句。所有数字都用脚本算过两遍。</p>
  <div class="notice">
    <p><b>时间地点</b>：10 月 23 日（周五）3:00–3:30 pm，LT23，闭卷 30 分钟，3 道短题。带认可的计算器、带照片的证件。</p>
    <p><b>范围</b>：第 1b 章概率、第 2 章无线信道、Practice 1–2。不考第 1a 章、第 3–7 章、积分计算。考卷附 Q 函数表。</p>
    <p><b>答题</b>：dB ↔ 线性的换算要写出来，单位写清楚；中间结果保留 3–4 位有效数字，最后再四舍五入。</p>
    <div class="legend"><span><span class="st must">背</span>讲义蓝框，考试不给</span><span><span class="st try">尽量记</span>老师说试着记</span><span><span class="st give">考试给</span>懂含义、会代数</span><span><span class="st def">定义·必会</span>一行定义，自己要会</span></div>
  </div>
'''

CHEAT = '''
  <div class="part" id="cheat">考前最后看</div>
  <section class="topic">
    <h2>公式状态总表 · Formula checklist</h2>
    <p class="why">进考场前把这张表从上到下默念一遍：“背”的能默写，“考试给”的知道每个字母是什么。</p>
    <div class="tw"><table class="cheat"><thead><tr><th>公式</th><th>状态</th><th>一句话用法</th></tr></thead><tbody>
      <tr><td>贝叶斯 \\(P(A|B)=\\dfrac{P(B|A)P(A)}{P(B)}\\)；全概率 \\(P(B)=\\sum_i P(B|A_i)P(A_i)\\)</td><td><span class="st must">背</span> <span class="st def">全概率会用</span></td><td>先用全概率求分母（对所有 A<sub>i</sub> 求和），再代贝叶斯</td></tr>
      <tr><td>\\(E[X]=\\sum x\\,P(x)\\)，\\(\\mathrm{Var}=E[X^2]-(E[X])^2\\)</td><td><span class="st must">E[X] 背</span> <span class="st def">Var 会用</span></td><td>离散求和，SNR 要先换成线性再平均；平方前 E[X] 多留几位</td></tr>
      <tr><td>\\(P(\\mathrm{dBm})=10\\log_{10}(P/1\\,\\mathrm{mW})\\)；1 W = 30 dBm</td><td><span class="st def">定义·必会</span></td><td>dBm − dBm = dB；SNR = P<sub>r</sub>(dBm) − N(dBm)</td></tr>
      <tr><td>\\(P_r=P_tK(d_0/d)^{\\gamma}\\)；\\(P_{r,\\mathrm{dB}}=P_{t,\\mathrm{dB}}+K_{\\mathrm{dB}}-10\\gamma\\log_{10}(d/d_0)\\)</td><td><span class="st must">背</span></td><td>题目写 simplified path loss model 就用它，别用自由空间</td></tr>
      <tr><td>最小二乘 \\(\\gamma=-\\dfrac{\\sum(x_i-\\bar x)(M_i-\\bar M)}{\\sum(x_i-\\bar x)^2}\\)，\\(K_{\\mathrm{dB}}=\\bar M+\\gamma\\bar x\\)，\\(\\sigma^2=\\) 残差平方平均</td><td><span class="st def">会算</span></td><td>\\(x_i=10\\log_{10}(d_i/d_0)\\)，列表算</td></tr>
      <tr><td>\\(P_{out}=Q\\!\\left(\\dfrac{\\bar P_r-P_{min}}{\\sigma}\\right)\\)</td><td><span class="st must">背</span></td><td>余量 ÷ σ 再查 Q 表；反查得所需余量</td></tr>
      <tr><td>\\(p(\\gamma)=\\dfrac{1}{\\bar\\gamma}e^{-\\gamma/\\bar\\gamma}\\)；\\(P_{out}=1-e^{-\\gamma_0/\\bar\\gamma}\\)</td><td><span class="st must">背</span></td><td>瑞利：γ<sub>0</sub>、γ̄ 都用线性</td></tr>
      <tr><td>\\(FM=10\\log_{10}\\dfrac{1}{\\ln\\frac{1}{1-\\varepsilon}}\\)（\\(\\approx 10\\log_{10}(1/\\varepsilon)\\)）</td><td><span class="st try">尽量记</span></td><td>只和 ε 有关，ε = 1% 时约 20 dB</td></tr>
      <tr><td>莱斯 \\(K=\\) 直射功率 / 散射总功率</td><td><span class="st give">考试给</span></td><td>K = 0 是瑞利，K 越大越接近不衰落</td></tr>
      <tr><td>\\(\\mu_{T_m}=\\dfrac{\\sum P_i\\tau_i}{\\sum P_i}\\)，\\(\\sigma_{T_m}=\\sqrt{E[\\tau^2]-\\mu^2}\\)</td><td><span class="st give">考试给</span></td><td>功率先 dB → 线性再加权</td></tr>
      <tr><td>平坦衰落 \\(\\sigma_{T_m}/T_s\\lt 0.1\\)</td><td><span class="st must">背</span></td><td>满足就是平坦；\\(\\sigma_{T_m}/T_s\\gg 1\\) 是频率选择性（有 ISI），夹在中间别硬判</td></tr>
      <tr><td>\\(f_m=vf_c/c\\)，\\(T_c\\approx 1/f_m\\)，\\(B_c\\approx 1/\\sigma_{T_m}\\)</td><td><span class="st def">定义·必会</span></td><td>km/h ÷ 3.6；\\(T_s\\ll T_c\\) 慢衰落</td></tr>
      <tr><td>瑞利 LCR \\(L_Z=\\sqrt{2\\pi}f_m\\rho e^{-\\rho^2}\\)，AFD \\(\\bar t_Z=\\dfrac{e^{\\rho^2}-1}{\\sqrt{2\\pi}f_m\\rho}\\)</td><td><span class="st give">考试给</span></td><td>会解释 ρ = Z<sub>min</sub>/Z<sub>rms</sub>（幅度比）和 f<sub>m</sub></td></tr>
      <tr><td>时间比例 = LCR × AFD；每秒误符号 = LCR × AFD ÷ T<sub>s</sub></td><td><span class="st def">定义·必会</span></td><td>观测 10 秒要先 ÷ 10 得 LCR</td></tr>
      <tr><td>\\(C=B\\log_2(1+\\mathrm{SNR})\\)；SINR \\(=S/(I+N)\\)</td><td><span class="st must">背</span></td><td>SNR 用线性值</td></tr>
      <tr><td>\\(C_\\varepsilon=B\\log_2\\!\\left(1+\\bar\\gamma\\ln\\frac{1}{1-\\varepsilon}\\right)\\)</td><td><span class="st give">考试给</span></td><td>真题都把它印在题里</td></tr>
      <tr><td>注水 \\(\\dfrac{P_i}{P}=\\dfrac{1}{\\gamma_0}-\\dfrac{1}{\\gamma_i}\\)（\\(\\gamma_i\\ge\\gamma_0\\)，否则 0）</td><td><span class="st try">尽量记</span></td><td>先假设全开解 γ<sub>0</sub>，有 γ<sub>i</sub> &lt; γ<sub>0</sub> 就去掉重算</td></tr>
    </tbody></table></div>
  </section>
'''


def body(standalone):
    frags = {k: (B / f'frag_{k}.html').read_text(encoding='utf-8') for k in ORDER}
    sections = {}
    for k in ORDER:
        for m in re.finditer(r'<section class="topic" id="(t\d+)">.*?</section>', frags[k], re.S):
            sections[m.group(1)] = m.group(0)
    missing = [t for _, ts in PARTS for t in ts if t not in sections]
    assert not missing, f'missing sections: {missing}'
    toc = ''.join(f'<a href="#{t}">{t[1:]} {SHORT[t]}</a>' for _, ts in PARTS for t in ts)
    toc = (f'  <nav class="toc" aria-label="目录">{toc}<a href="#cheat">公式总表</a><span class="spacer"></span>'
           '<label class="toggle"><input type="checkbox" id="selftest">自测模式（遮住例子的步骤）</label></nav>\n')
    out = HEAD + toc
    for i, (name, ts) in enumerate(PARTS, 1):
        out += f'\n  <div class="part">第 {i} 部分 · {name}</div>\n'
        out += '\n'.join(sections[t] for t in ts) + '\n'
    out += CHEAT
    links = ('相关页面：<a href="p2-learn.html">Part 2 讲解</a> · <a href="p2-practice.html">Part 2 练习（Practice 1–2、模拟题 A/B/C、专项）</a> · '
             '<a href="exams.html">历年期末真题</a>。')
    out += (f'\n  <footer>{links}<br>题号对照：模拟 A · Q1–Q3、B · Q1–Q3、C · Q1–Q3、专项 · Q1–Q3 都在练习页的“模拟 Quiz”分组。'
            '数字核对脚本在仓库 src/quizsum/（check_*.py、_verify_*.py）。</footer>\n</div>\n')
    if not standalone:
        out = out.replace('  <a class="back" href="index.html">← 学习站目录</a>\n', '')
        for f, u in ARTURL.items():
            out = out.replace(f'href="{f}"', f'href="{u}"')
    return out + f'<script>{JS}</script>\n'


def page(standalone):
    head = ('<title>EE6129 Quiz 例题总结</title>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">\n'
            f'<style>{CSS}</style>\n{MATHJAX}\n')
    if not standalone:
        return head + body(False)
    return ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + body(True) + '</body>\n</html>\n')


if __name__ == '__main__':
    (REPO / 'quiz-summary.html').write_text(page(True), encoding='utf-8')
    ART.mkdir(exist_ok=True)
    (ART / 'quiz-summary.html').write_text(page(False), encoding='utf-8')
    print('ok', (REPO / 'quiz-summary.html').stat().st_size, (ART / 'quiz-summary.html').stat().st_size)
