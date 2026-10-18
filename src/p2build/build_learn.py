#!/usr/bin/python3
"""Assemble EE6129 Part 2 learn page from fragments.

Writes the repo page (standalone HTML) and an artifact copy (no html/head/body
wrapper; cross-page links pointed at artifact URLs passed on the command line).
usage: build_learn.py [practice_artifact_url]
"""
import pathlib, sys

B = pathlib.Path(__file__).parent
REPO = pathlib.Path(__file__).resolve().parents[2]
ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')
practice_url = sys.argv[1] if len(sys.argv) > 1 else None

css = (B / 'partA_style.css').read_text(encoding='utf-8')
rail_js = (B / 'partA_rail.js').read_text(encoding='utf-8')
frags = ''.join((B / f'learn_{i:02d}.html').read_text(encoding='utf-8') for i in range(1, 9))

EXTRA_CSS = '''
/* Part 2 additions */
@media (max-width:680px){.main mjx-container:not([display="true"]){display:inline-block;max-width:100%;overflow-x:auto;overflow-y:hidden;vertical-align:middle;}}
/* key-point marks */
:root{--key:#c2410c;--key-soft:#fff1e6;--key-line:#f5b48a;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--key:#fb923c;--key-soft:rgba(251,146,60,.12);--key-line:rgba(251,146,60,.45);}}
:root[data-theme="dark"]{--key:#fb923c;--key-soft:rgba(251,146,60,.12);--key-line:rgba(251,146,60,.45);}
.imp{display:inline-block;vertical-align:middle;margin-left:10px;font-family:var(--f-mono);font-size:11px;font-weight:700;letter-spacing:.04em;padding:2px 8px;border-radius:999px;border:1px solid var(--key-line);color:var(--key);background:var(--key-soft);white-space:nowrap;}
.imp.i2{opacity:.85}
.imp.i1{color:var(--ink-faint);border-color:var(--line-strong);background:transparent;}
/* quiz scope + formulas to memorise (quiz_marks.py) */
:root{--must:#b42318;--must-soft:#fdecea;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--must:#f97066;--must-soft:rgba(249,112,102,.13);}}
:root[data-theme="dark"]{--must:#f97066;--must-soft:rgba(249,112,102,.13);}
.qz{display:inline-block;vertical-align:middle;margin-left:8px;font-family:var(--f-mono);font-size:11px;font-weight:700;letter-spacing:.03em;line-height:1.5;padding:1px 8px;border-radius:999px;border:1px solid;white-space:nowrap;}
.qz.in,.qz.note{color:var(--good);border-color:var(--good);background:var(--good-soft);}
.qz.out{color:var(--ink-faint);border-color:var(--line-strong);background:transparent;font-weight:600;}
.qz.must{color:var(--must);border-color:var(--must);background:var(--must-soft);}
.qz.try{color:var(--gold);border-color:var(--gold);background:var(--gold-soft);}
.qz.give{color:var(--accent-ink);border-color:var(--accent);background:var(--accent-soft);}
.chapter-head{flex-wrap:wrap;}
.chapter-head .qz{margin-left:0;}
.qzline{margin-top:10px;padding-top:8px;border-top:1px dashed var(--line-strong);font-family:var(--f-body);font-size:14px;line-height:1.7;color:var(--ink);}
.qzline .qz{margin:0 8px 0 0;}
.qzbox{border:1.5px solid var(--good);border-left-width:5px;border-radius:10px;background:var(--good-soft);padding:14px 18px 8px;margin:0 0 28px;}
.qzbox > .lbl{font-family:var(--f-mono);font-size:11px;letter-spacing:.06em;color:var(--good);font-weight:700;margin-bottom:6px;}
.qzbox p{margin:0 0 .6em;font-size:15px;line-height:1.75;}
.qzbox .qz{margin:0 2px;}
.key{border:1.5px solid var(--key);border-left-width:5px;border-radius:10px;background:var(--key-soft);padding:14px 18px 12px;margin:24px 0;}
.key > .lbl{font-family:var(--f-mono);font-size:11px;letter-spacing:.08em;color:var(--key);font-weight:700;margin-bottom:6px;}
.key ul,.key ol{margin:0 0 .4em;padding-left:1.3em;}
.key li{margin-bottom:.35em;font-size:15px;}
.key p{font-size:15px;margin-bottom:.5em;}
.pitfall{border:1.5px dashed var(--key);border-radius:10px;padding:12px 16px;margin:22px 0;background:var(--card);}
.pitfall > .lbl{font-family:var(--f-mono);font-size:11px;letter-spacing:.08em;color:var(--key);font-weight:700;margin-bottom:6px;}
.pitfall ul{margin:0;padding-left:1.3em;}
.pitfall li{font-size:15px;margin-bottom:.35em;}
mark.hl{background:linear-gradient(to bottom,transparent 45%,var(--key-soft) 45%);color:inherit;font-weight:600;padding:0 1px;box-shadow:inset 0 -2px 0 var(--key-line);}
.legend{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;font-size:13px;color:var(--ink-soft);margin:6px 0 18px;}
.steps{counter-reset:st;list-style:none;padding-left:0 !important;}
.steps > li{counter-increment:st;position:relative;padding-left:2.1em;margin-bottom:.6em;}
.steps > li::before{content:counter(st);position:absolute;left:0;top:.15em;width:1.5em;height:1.5em;border-radius:50%;background:var(--accent-soft);color:var(--accent-ink);font-family:var(--f-mono);font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;}

.extra-inline{font-size:14px;color:var(--extra);}
.tool{border:1px solid var(--accent);border-radius:10px;background:var(--card);padding:16px 20px;margin:22px 0;box-shadow:var(--shadow);}
.tool h4{font-family:var(--f-display);font-size:17px;margin:0 0 10px;color:var(--accent-ink);}
.trow{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:flex-end;}
.trow label{display:flex;flex-direction:column;font-size:12.5px;color:var(--ink-soft);gap:4px;}
.trow input{font-family:var(--f-mono);font-size:14px;padding:5px 8px;border:1px solid var(--line-strong);border-radius:6px;background:var(--paper-2);color:var(--ink);width:8em;max-width:100%;}
.tout{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin-top:12px;}
.tout div{background:var(--paper-2);border-radius:8px;padding:6px 10px;}
.tout span{display:block;font-size:11.5px;color:var(--ink-faint);font-family:var(--f-mono);}
.tout b{font-family:var(--f-mono);font-size:15px;word-break:break-word;}
.thint{font-size:13px;color:var(--ink-soft);margin-top:8px;}
.formula-card .fexpr{line-height:2.1;}
mjx-container[display="true"]{overflow-x:auto;overflow-y:hidden;max-width:100%;}
.formula-card .fexpr mjx-container{max-width:100%;}
.worked .wtext{min-width:0;}
/* knowledge-point box under each worked example */
.kp{border:1px solid var(--accent);border-left-width:5px;border-radius:10px;background:var(--accent-soft);padding:12px 18px 8px;margin:-16px 0 30px;}
.kp > .lbl{font-family:var(--f-mono);font-size:11px;letter-spacing:.08em;color:var(--accent-ink);font-weight:700;margin-bottom:4px;}
.kp dl{margin:0;display:grid;grid-template-columns:max-content 1fr;gap:4px 14px;}
.kp dt{font-weight:700;font-size:14px;color:var(--accent-ink);padding-top:1px;}
.kp dd{margin:0;font-size:14.5px;color:var(--ink);line-height:1.65;}
@media (max-width:560px){.kp dl{grid-template-columns:1fr;gap:0;}.kp dt{margin-top:6px;}}
'''

MATHJAX = '''<script>
window.MathJax = {
  tex: { inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']] },
  svg: { fontCache: 'global' },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js" async></script>'''

TOOLS_JS = r'''
(function(){
  function erfc(x){ var z=Math.abs(x), t=1/(1+0.5*z);
    var r=t*Math.exp(-z*z-1.26551223+t*(1.00002368+t*(0.37409196+t*(0.09678418+t*(-0.18628806+t*(0.27886807+t*(-1.13520398+t*(1.48851587+t*(-0.82215223+t*0.17087277)))))))));
    return x>=0?r:2-r; }
  function Q(x){ return 0.5*erfc(x/Math.SQRT2); }
  function Qinv(p){ var lo=-10, hi=40; for (var i=0;i<200;i++){ var m=(lo+hi)/2; if (Q(m)>p) lo=m; else hi=m; } return lo; }
  function fmt(x){ if (!isFinite(x)) return '—'; var a=Math.abs(x); return (a!==0&&(a<1e-3||a>=1e6))?x.toExponential(3):(+x.toPrecision(4)).toString(); }
  function $(id){ return document.getElementById(id); }
  function on(ids, fn){ ids.forEach(function(i){ $(i).addEventListener('input', fn); }); fn(); }

  on(['q-x','q-p'], function(){
    $('q-out').textContent = fmt(Q(+$('q-x').value));
    var p=+$('q-p').value; $('qi-out').textContent = (p>0&&p<1)? fmt(Qinv(p)) : '—';
  });

  on(['wf-g','wf-b'], function(){
    var g=$('wf-g').value.split(/[,\s]+/).map(Number).filter(function(v){ return v>0; });
    var B=+$('wf-b').value;
    if (!g.length){ $('wf-g0').textContent=$('wf-p').textContent=$('wf-c').textContent='—'; return; }
    var idx=g.map(function(v,i){ return i; }).sort(function(a,b){ return g[b]-g[a]; }), g0=NaN, k;
    for (k=idx.length;k>=1;k--){
      var s=1; for (var i=0;i<k;i++) s+=1/g[idx[i]];
      g0=k/s; if (g[idx[k-1]]>=g0) break;
    }
    var P=g.map(function(v){ return v>=g0 ? 1/g0-1/v : 0; });
    var C=0; g.forEach(function(v){ if (v>=g0) C+=Math.log2(v/g0); });
    $('wf-g0').textContent=fmt(g0);
    $('wf-p').textContent=P.map(function(v){ return v.toFixed(3); }).join(' / ');
    $('wf-c').textContent=fmt(C*B)+(B===1?' bit/s/Hz':' Mbps');
  });

  on(['l-v','l-f','l-r','l-rs'], function(){
    var fm=(+$('l-v').value/3.6)*(+$('l-f').value)*1e9/3e8, r=+$('l-r').value, Rs=+$('l-rs').value*1e3;
    var L=Math.sqrt(2*Math.PI)*fm*r*Math.exp(-r*r), A=(Math.exp(r*r)-1)/(Math.sqrt(2*Math.PI)*fm*r);
    $('l-fm').textContent=fmt(fm); $('l-tc').textContent=fmt(1e3/fm)+' ms';
    $('l-lcr').textContent=fmt(L); $('l-afd').textContent=fmt(A*1e6)+' µs'; $('l-n').textContent=fmt(A*Rs);
  });

  on(['o-r','o-b','o-w','o-g'], function(){
    var Rs=(+$('o-r').value*1e6)/(+$('o-b').value), B=+$('o-w').value*1e3, Tg=+$('o-g').value*1e-6;
    if (!(Rs<B)){ ['o-n','o-t','o-tt','o-loss'].forEach(function(i){ $(i).textContent='不可行'; }); return; }
    var N=Rs*Tg/(1-Rs/B), Nn=Math.ceil(N-1e-9), T=Nn/B;
    $('o-n').textContent=fmt(N)+(Math.abs(N-Nn)>1e-6?' → '+Nn:'');
    $('o-t').textContent=fmt(T*1e6)+' µs'; $('o-tt').textContent=fmt((T+Tg)*1e6)+' µs';
    $('o-loss').textContent=fmt(10*Math.log10((T+Tg)/T))+' dB';
  });
})();
'''

practice_href = practice_url if practice_url else 'p2-practice.html'
BODY = f'''<div class="mobtoc">
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
      <div class="kicker">EE6129 · Part 2 讲解 · Ser Wee · 第 7–13 周</div>
      <h1>信号在路上变坏了，怎么救回来</h1>
      <p class="lede">从"无线信道到底怎么折腾信号"出发，一路讲到信号检测、分集、MIMO、均衡和 OFDM。每个公式先讲直觉、再讲推导，讲义例题和 Practice 1–7 的题目都配了完整解答，假设你零基础。</p>
      <div class="meta">
        <span>◆ 对应讲义第 1–7 章</span>
        <span>◆ 每节标讲义页码</span>
        <span>◆ 紫色框 = 课外补充</span>
        <span>◆ ★★★ 必考 · ★★ 常考 · ★ 了解</span>
        <span>◆ 橙框 = 考试重点</span>
        <span>◆ <a href="{practice_href}">配套练习页 →</a></span>
      </div>
    </header>
{frags}
    <div class="next-up">
      <div class="lbl">接下来</div>
      <h4><a href="{practice_href}">Part 2 练习：Practice 1–7 全部题目逐题详解</a></h4>
      <p>每题附英文原题、考点、分步解答和官方答案核对，还有随机出题的练习模式。</p>
    </div>
  </main>
</div>
'''

def page(standalone):
    head = f'<title>EE6129 Part 2 讲解</title>\n<style>{css}{EXTRA_CSS}</style>\n{MATHJAX}\n'
    body = BODY + f'\n<script>{rail_js}</script>\n<script>{TOOLS_JS}</script>\n'
    if standalone:
        return ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
                + head + '</head>\n<body>\n' + body + '</body>\n</html>\n')
    return head + body

(REPO / 'p2-learn.html').write_text(page(True).replace(practice_href, 'p2-practice.html') if practice_url else page(True), encoding='utf-8')
ART.mkdir(exist_ok=True)
(ART / 'p2-learn.html').write_text(page(False), encoding='utf-8')
print('ok', (REPO / 'p2-learn.html').stat().st_size)

# re-insert the past exam questions (build_exams.py keeps them between PASTQ markers)
import subprocess
subprocess.run([sys.executable, str(B.parent / 'exams' / 'build_exams.py'), '--inject'], check=True)
