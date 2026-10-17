#!/usr/bin/python3
"""Assemble EE6129 Part 2 practice page (Practice 1-7 solutions + random drills).
usage: build_practice.py [learn_artifact_url]"""
import pathlib, sys

B = pathlib.Path(__file__).parent
REPO = pathlib.Path(__file__).resolve().parents[2]
ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')
learn_url = sys.argv[1] if len(sys.argv) > 1 else None
frags = ''.join((B / f'prac_{i}.html').read_text(encoding='utf-8') for i in range(1, 8))

CSS = r'''
:root{
  --bg:#eceff0; --surface:#fff; --surface-2:#e3e9e9; --border:#cbd6d7;
  --text:#13201f; --muted:#4e615f;
  --accent:#0f766e; --accent-strong:#0a5a53; --accent-soft:#d7eeeb; --on-accent:#fff;
  --warn:#7a4a0c; --warn-soft:#f7e8d2; --bad:#a3261e; --bad-soft:#fbe3e0; --ok:#137a3f; --ok-soft:#dcf1e3;
  --extra:#7a4fc4; --extra-soft:#f2ecfb;
  --shadow:0 1px 2px rgba(19,32,31,.06),0 8px 22px rgba(19,32,31,.07);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --bg:#0b1413; --surface:#111e1c; --surface-2:#182825; --border:#273a36;
    --text:#e6f0ed; --muted:#9ab3ad;
    --accent:#33d1bf; --accent-strong:#7ceede; --accent-soft:#113330; --on-accent:#08100e;
    --warn:#f0b56a; --warn-soft:#2f2210; --bad:#f2857c; --bad-soft:#351816; --ok:#4fd087; --ok-soft:#12301f;
    --extra:#b79cf0; --extra-soft:rgba(183,156,240,.12);
    --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 22px rgba(0,0,0,.4);
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --bg:#0b1413; --surface:#111e1c; --surface-2:#182825; --border:#273a36;
  --text:#e6f0ed; --muted:#9ab3ad;
  --accent:#33d1bf; --accent-strong:#7ceede; --accent-soft:#113330; --on-accent:#08100e;
  --warn:#f0b56a; --warn-soft:#2f2210; --bad:#f2857c; --bad-soft:#351816; --ok:#4fd087; --ok-soft:#12301f;
  --extra:#b79cf0; --extra-soft:rgba(183,156,240,.12);
  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 22px rgba(0,0,0,.4);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:'IBM Plex Sans','Noto Sans CJK SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:900px;margin:0 auto;padding:28px 18px 90px}
h1,h2,h3{font-family:'Barlow Condensed','Noto Sans CJK SC','Microsoft YaHei',sans-serif;font-weight:700;margin:0 0 .3em;text-wrap:balance;line-height:1.15;letter-spacing:.01em}
h1{font-size:2.4rem} h2{font-size:1.55rem} h3{font-size:1.18rem}
a{color:var(--accent-strong)}
.back{font-size:.82rem;text-decoration:none;color:var(--muted)}
.eyebrow{font-family:'IBM Plex Mono',monospace;font-size:.7rem;letter-spacing:.09em;text-transform:uppercase;color:var(--accent-strong);margin:14px 0 6px}
.lede{color:var(--muted);max-width:66ch;margin:.2em 0 .8em}
.notice{border:1px solid var(--border);border-radius:10px;padding:9px 14px;font-size:.86rem;color:var(--muted);max-width:72ch}
.notice b{color:var(--text)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.tabs{position:sticky;top:env(safe-area-inset-top,0px);z-index:10;background:var(--bg);display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:12px 0 10px;margin:20px 0 6px;border-bottom:1px solid var(--border)}
.tab{font:inherit;font-size:.9rem;font-weight:600;padding:6px 16px;border-radius:999px;border:1px solid var(--border);background:var(--surface);color:var(--muted);cursor:pointer}
.tab[aria-selected="true"]{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}
.tabs .spacer{flex:1}
.toggle{display:flex;align-items:center;gap:6px;font-size:.82rem;color:var(--muted);cursor:pointer}
.toggle input{accent-color:var(--accent);width:16px;height:16px}
.count{font-family:'IBM Plex Mono',monospace;font-size:.75rem;color:var(--muted)}
.filters{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.chipbtn{font:inherit;font-size:.78rem;border:1px solid var(--border);background:var(--surface);color:var(--muted);border-radius:999px;padding:3px 11px;cursor:pointer}
.chipbtn.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent-strong);font-weight:600}
.tw{overflow-x:auto;margin:8px 0}
table{border-collapse:collapse;width:100%;font-size:.86rem}
th,td{padding:6px 10px;border-bottom:1px solid var(--border);text-align:left;vertical-align:top}
th{font-family:'IBM Plex Mono',monospace;font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:600}
table.mini{width:auto;min-width:240px}
.ov{min-width:620px}
.group{margin:38px 0 10px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;scroll-margin-top:70px}
.group h2{margin:0}
.group span{font-size:.8rem;color:var(--muted)}
.ex{background:var(--surface);border:1px solid var(--border);border-radius:14px;box-shadow:var(--shadow);padding:18px 20px;margin-bottom:14px;scroll-margin-top:70px}
.ex header{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 12px;margin-bottom:8px}
.ex h3{margin:0;flex:1 1 260px}
.pg{font-family:'IBM Plex Mono',monospace;font-size:.72rem;font-weight:600;background:var(--accent-soft);color:var(--accent-strong);border-radius:6px;padding:2px 8px;white-space:nowrap}
.orig{border:1px solid var(--border);border-radius:10px;padding:10px 14px 8px;font-size:.92rem;line-height:1.65}
.orig-lab{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 10px;font-family:'IBM Plex Mono',monospace;font-size:.66rem;letter-spacing:.06em;text-transform:uppercase;color:var(--accent-strong);margin-bottom:4px}
.orig-lab span:last-child{color:var(--muted)}
.orig p{margin:.4em 0}
.orig .eq{text-align:center;margin:.6em 0;overflow-x:auto;overflow-y:hidden;padding:2px 0}
.orig p.zh{margin:-.15em 0 .75em;padding:2px 0 2px 10px;border-left:3px solid var(--accent);background:var(--accent-soft);border-radius:0 6px 6px 0;color:var(--text);font-size:.9rem;line-height:1.7}
.orig .zh-th{font-weight:400;font-size:.85em;color:var(--muted)}
.no-zh .orig p.zh,.no-zh .orig .zh-th{display:none}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 2px}
.chip{font-size:.74rem;border-radius:999px;padding:2px 10px;background:var(--accent-soft);color:var(--accent-strong);font-weight:500}
.chip.src{background:transparent;border:1px solid var(--border);color:var(--muted)}
.reveal{margin-top:10px;background:none;border:1px dashed var(--accent);color:var(--accent-strong);border-radius:8px;padding:6px 12px;font-size:.82rem;cursor:pointer;font-family:inherit;display:none}
.exam .reveal{display:inline-block}
.exam .sol{display:none}
.exam .ex.open .sol{display:block}
.exam .ex.open .reveal{display:none}
.sol{margin-top:10px}
.idea{font-size:.9rem;margin:.3em 0 .6em;max-width:74ch}
ol.steps{margin:0;padding-left:0;list-style:none;counter-reset:s}
ol.steps>li{counter-increment:s;position:relative;padding:6px 0 6px 34px;font-size:.92rem;border-bottom:1px dotted var(--border)}
ol.steps>li:last-child{border-bottom:none}
ol.steps>li::before{content:counter(s);position:absolute;left:0;top:8px;width:22px;height:22px;border-radius:50%;background:var(--accent-soft);color:var(--accent-strong);font-family:'IBM Plex Mono',monospace;font-size:.72rem;font-weight:600;display:flex;align-items:center;justify-content:center}
.calc{font-family:'IBM Plex Mono',monospace;font-size:.85rem;background:var(--surface-2);border-radius:6px;padding:5px 10px;margin:5px 0;overflow-x:auto}
.ans{margin-top:10px;border:1.5px solid var(--accent);border-radius:10px;padding:8px 14px;font-size:.92rem;background:var(--accent-soft)}
.official{margin-top:8px;border-radius:10px;padding:7px 14px;font-size:.88rem;background:var(--ok-soft)}
.official b{color:var(--ok)}
.note{margin-top:8px;border-radius:10px;padding:8px 14px;font-size:.86rem;background:var(--extra-soft);border:1px solid var(--extra)}
.note::before{content:'补充　';font-weight:700;color:var(--extra)}
.pkp{margin-top:12px;border:1px solid var(--accent);border-left-width:5px;border-radius:10px;background:var(--surface);padding:10px 16px 8px}
.pkp > .lbl{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.08em;color:var(--accent-strong);font-weight:700;margin-bottom:4px}
.pkp dl{margin:0;display:grid;grid-template-columns:max-content 1fr;gap:5px 14px}
.pkp dt{font-weight:700;font-size:.84rem;color:var(--accent-strong);padding-top:1px}
.pkp dd{margin:0;font-size:.88rem;line-height:1.65}
@media (max-width:560px){.pkp dl{grid-template-columns:1fr;gap:0}.pkp dt{margin-top:6px}}
.done{display:flex;justify-content:flex-end;margin-top:10px}
.done label{font-size:.8rem;color:var(--muted);display:flex;gap:6px;align-items:center;cursor:pointer}
.done input{accent-color:var(--ok)}
.ex.mastered{border-color:var(--ok)}
.ex.mastered .pg::after{content:' ✓';color:var(--ok)}
.hide{display:none!important}
/* drill */
.drill{background:var(--surface);border:1px solid var(--accent);border-radius:14px;box-shadow:var(--shadow);padding:18px 20px;margin-top:14px}
.drow{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.drow select,.drow input{font:inherit;font-size:.9rem;padding:6px 10px;border:1px solid var(--border);border-radius:8px;background:var(--surface-2);color:var(--text)}
.drow input{font-family:'IBM Plex Mono',monospace;width:11em}
.btn{font:inherit;font-size:.86rem;font-weight:600;border:1px solid var(--accent);background:var(--accent);color:var(--on-accent);border-radius:8px;padding:6px 14px;cursor:pointer}
.btn.ghost{background:transparent;color:var(--accent-strong)}
.dq{margin:14px 0 10px;font-size:.96rem;max-width:74ch}
.dq .tag{font-family:'IBM Plex Mono',monospace;font-size:.7rem;color:var(--accent-strong);letter-spacing:.06em;text-transform:uppercase;display:block;margin-bottom:4px}
.verdict{margin-top:10px;border-radius:10px;padding:8px 14px;font-size:.9rem}
.verdict.good{background:var(--ok-soft);color:var(--ok)}
.verdict.bad{background:var(--bad-soft);color:var(--bad)}
.dsteps{margin-top:10px}
.score{font-family:'IBM Plex Mono',monospace;font-size:.8rem;color:var(--muted)}
mjx-container[display="true"]{overflow-x:auto;overflow-y:hidden;max-width:100%}
footer{margin-top:40px;font-size:.78rem;color:var(--muted);max-width:72ch}
@media (max-width:640px){h1{font-size:1.9rem}.ex{padding:15px}}
'''

MATHJAX = '''<script>
window.MathJax = {
  tex: { inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']] },
  svg: { fontCache: 'global' },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js" async></script>'''

learn_href = learn_url if learn_url else 'p2-learn.html'

OVERVIEW = f'''
  <div class="tw"><table class="ov">
    <thead><tr><th>练习</th><th>周</th><th>考点</th><th>讲解页</th></tr></thead>
    <tbody>
      <tr><td><a href="#P1">Practice 1</a></td><td>8</td><td>路径损耗拟合、阴影中断概率、时延扩展</td><td><a href="{learn_href}#ch2">第二章 2.1–2.4</a></td></tr>
      <tr><td><a href="#P2">Practice 2</a></td><td>9</td><td>平均衰落时长、宏分集、香农容量与 MUD</td><td><a href="{learn_href}#ch2">第二章 2.6–2.7</a></td></tr>
      <tr><td><a href="#P3">Practice 3</a></td><td>10</td><td>正交基、ML 判决门限、误码平台</td><td><a href="{learn_href}#ch3">第三章</a></td></tr>
      <tr><td><a href="#P4">Practice 4</a></td><td>11</td><td>宏分集、MRC、阵列增益与分集增益、等增益合并</td><td><a href="{learn_href}#ch4">第四章</a></td></tr>
      <tr><td><a href="#P5">Practice 5</a></td><td>12</td><td>注水、Alamouti 判决变量、分集-复用折中</td><td><a href="{learn_href}#ch5">第五章</a>、<a href="{learn_href}#ch4">4.4</a></td></tr>
      <tr><td><a href="#P6">Practice 6</a></td><td>13</td><td>ISI 误码率、迫零、MMSE 与 DFE</td><td><a href="{learn_href}#ch6">第六章</a></td></tr>
      <tr><td><a href="#P7">Practice 7</a></td><td>13</td><td>OFDM 子载波数、H_k、等容量 vs 注水、CP</td><td><a href="{learn_href}#ch7">第七章</a></td></tr>
    </tbody>
  </table></div>'''

BODY = f'''<div class="wrap" id="root">
  <a class="back" href="index.html">← 学习站目录</a>
  <div class="eyebrow">EE6129 · Part 2 · Practice 1–7</div>
  <h1>Part 2 练习</h1>
  <p class="lede">讲义配套的 7 份 Practice 共 21 道题，逐题给出英文原题、考点、思路和分步解答，并和官方答案逐一核对。「随机练习」按同样的题型随机出数字，自动判分。</p>
  <div class="notice">所有数字都用程序验算过。<b>20 道题与官方答案一致</b>（其中 P4 Q1 是论述题）；Practice 1 第 1 题按题目数据算不出官方的数字，题下写了原因和标准做法。紫色"补充"框是课外内容。配套讲解见 <a href="{learn_href}">Part 2 讲解页</a>。</div>

  <div class="tabs" role="tablist" aria-label="页面视图">
    <button class="tab" role="tab" id="tab-sol" aria-controls="sol" aria-selected="true" data-tab="sol">逐题详解</button>
    <button class="tab" role="tab" id="tab-drill" aria-controls="drill" aria-selected="false" data-tab="drill">随机练习</button>
    <span class="spacer"></span>
    <label class="toggle" id="examWrap"><input type="checkbox" id="examMode"> 自测模式（先藏解答）</label>
    <label class="toggle"><input type="checkbox" id="zhMode" checked> 题目中文对照</label>
    <span class="count" id="count"></span>
  </div>

  <section id="sol" role="tabpanel" aria-labelledby="tab-sol">
{OVERVIEW}
    <div class="filters" id="filters">
      <button class="chipbtn on" type="button" data-f="all">全部</button>
      <button class="chipbtn" type="button" data-f="p1">P1</button><button class="chipbtn" type="button" data-f="p2">P2</button>
      <button class="chipbtn" type="button" data-f="p3">P3</button><button class="chipbtn" type="button" data-f="p4">P4</button>
      <button class="chipbtn" type="button" data-f="p5">P5</button><button class="chipbtn" type="button" data-f="p6">P6</button>
      <button class="chipbtn" type="button" data-f="p7">P7</button>
    </div>
{frags}
  </section>

  <section id="drill" role="tabpanel" aria-labelledby="tab-drill" hidden>
    <div class="drill">
      <div class="drow">
        <label for="d-type" class="score">题型</label>
        <select id="d-type"></select>
        <button class="btn" type="button" id="d-new">出一道新题</button>
        <span class="spacer" style="flex:1"></span>
        <span class="score" id="d-score">已答 0 · 答对 0</span>
      </div>
      <div class="dq" id="d-q"></div>
      <div class="drow">
        <label for="d-ans" class="score">你的答案</label>
        <input id="d-ans" type="text" inputmode="decimal" autocomplete="off" placeholder="输入数字">
        <span class="score" id="d-unit"></span>
        <button class="btn" type="button" id="d-check">核对</button>
        <button class="btn ghost" type="button" id="d-show">看解答</button>
      </div>
      <div id="d-verdict"></div>
      <div class="dsteps" id="d-steps" hidden></div>
    </div>
    <p class="score" style="margin-top:12px">允许约 2% 的误差（查 Q 表、取整造成的偏差都算对）。概率可以写成 0.0036 或 3.6e-3。</p>
  </section>

  <footer>答案按讲义公式计算；Q 函数用数值方法精确计算，和查表可能差在第三位有效数字。题目原文版权归课程讲师所有，仅供个人学习。</footer>
</div>
'''

JS = r'''
(function(){
  /* ---------- solutions: filter, exam mode, mastered ---------- */
  var root=document.getElementById('root'), exs=[].slice.call(document.querySelectorAll('.ex')), groups=[].slice.call(document.querySelectorAll('.group'));
  var store={get:function(k){try{return localStorage.getItem(k);}catch(e){return null;}},set:function(k,v){try{localStorage.setItem(k,v);}catch(e){}}};
  function count(){ var vis=exs.filter(function(e){return !e.classList.contains('hide');}); var d=vis.filter(function(e){return e.classList.contains('mastered');}).length; document.getElementById('count').textContent='已掌握 '+d+' / '+vis.length; }
  document.querySelectorAll('#filters .chipbtn').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('#filters .chipbtn').forEach(function(x){x.classList.remove('on');}); b.classList.add('on');
      var f=b.dataset.f;
      exs.forEach(function(e){ e.classList.toggle('hide', f!=='all' && e.id.indexOf(f+'q')!==0); });
      groups.forEach(function(g){ g.classList.toggle('hide', f!=='all' && g.id.toLowerCase()!==f); });
      count();
    });
  });
  var zh=document.getElementById('zhMode');
  if (store.get('ee6129-p2:zh')==='0'){ zh.checked=false; root.classList.add('no-zh'); }
  zh.addEventListener('change',function(){ root.classList.toggle('no-zh',!zh.checked); store.set('ee6129-p2:zh',zh.checked?'1':'0'); });
  var exam=document.getElementById('examMode');
  exam.addEventListener('change',function(){ root.classList.toggle('exam',exam.checked); exs.forEach(function(e){e.classList.remove('open');}); });
  exs.forEach(function(e){
    e.querySelector('.reveal').addEventListener('click',function(){ e.classList.add('open'); });
    var cb=e.querySelector('.done input'), key='ee6129-p2:'+e.id;
    if (store.get(key)==='1'){ cb.checked=true; e.classList.add('mastered'); }
    cb.addEventListener('change',function(){ e.classList.toggle('mastered',cb.checked); store.set(key,cb.checked?'1':'0'); count(); });
  });
  count();

  /* ---------- tabs ---------- */
  var tabs=[].slice.call(document.querySelectorAll('[data-tab]'));
  function show(id){ tabs.forEach(function(t){ var on=t.dataset.tab===id; t.setAttribute('aria-selected',String(on)); document.getElementById(t.dataset.tab).hidden=!on; });
    document.getElementById('examWrap').style.visibility = id==='sol'?'visible':'hidden'; document.getElementById('count').style.visibility = id==='sol'?'visible':'hidden'; }
  tabs.forEach(function(t){ t.addEventListener('click',function(){ show(t.dataset.tab); try{history.replaceState(null,'','#'+t.dataset.tab);}catch(e){} }); });
  if ((location.hash||'')==='#drill') show('drill');

  /* ---------- math helpers ---------- */
  function erfc(x){ var z=Math.abs(x), t=1/(1+0.5*z);
    var r=t*Math.exp(-z*z-1.26551223+t*(1.00002368+t*(0.37409196+t*(0.09678418+t*(-0.18628806+t*(0.27886807+t*(-1.13520398+t*(1.48851587+t*(-0.82215223+t*0.17087277)))))))));
    return x>=0?r:2-r; }
  function Q(x){ return 0.5*erfc(x/Math.SQRT2); }
  function Qinv(p){ var lo=-10,hi=40; for(var i=0;i<200;i++){ var m=(lo+hi)/2; if(Q(m)>p) lo=m; else hi=m; } return lo; }
  function pick(a){ return a[Math.floor(Math.random()*a.length)]; }
  function rnd(lo,hi,step){ var n=Math.round((hi-lo)/step); return +(lo+step*Math.floor(Math.random()*(n+1))).toFixed(6); }
  function f(x,d){ if(!isFinite(x)) return '—'; var a=Math.abs(x); if(a!==0&&(a<1e-3||a>=1e6)) return x.toExponential(d===undefined?3:d-1); return (+x.toPrecision(d||4)).toString(); }
  function log2(x){ return Math.log(x)/Math.LN2; }

  /* ---------- drill generators ---------- */
  var G=[
    {id:'out', name:'阴影中断概率（P1 Q2a）', make:function(){
      var mu=rnd(12,22,1), s=pick([4,5,6,8]), T=mu-rnd(3,12,1); var k=(mu-T)/s, a=Q(k);
      return {q:'接收功率（dBm）服从对数正态分布，均值 '+mu+' dBm，标准差 '+s+' dB。低于 '+T+' dBm 即中断，求中断概率。', a:a, rel:0.03, unit:'',
        s:['门限比均值低 '+(mu-T)+' dB = '+f(k)+' 个标准差','P_out = Q('+f(k)+') = '+f(a)]}; }},
    {id:'mu', name:'达到中断要求所需的均值（P1 Q2b）', make:function(){
      var s=pick([3,4,5,6,8]), p=pick([0.01,0.05,0.02,0.001]), T=rnd(-100,10,5); var k=Qinv(p), m=T+s*k;
      return {q:'阴影标准差 '+s+' dB，门限 '+T+' dBm，要求中断概率小于 '+p+'。平均接收功率至少要多少 dBm？', a:m, abs:0.15, unit:'dBm',
        s:['Q(k) = '+p+' → k = '+f(k),'μ &gt; '+T+' + '+s+' × '+f(k)+' = '+f(m,5)+' dBm']}; }},
    {id:'rms', name:'离散功率时延分布的 rms 时延扩展', make:function(){
      var t=[0,rnd(1,4,1),rnd(5,10,1)], pdB=[0,-pick([0,3,6,10]),-pick([3,6,10,20])], P=pdB.map(function(x){return Math.pow(10,x/10);});
      var S=P[0]+P[1]+P[2], m=(P[0]*t[0]+P[1]*t[1]+P[2]*t[2])/S, m2=(P[0]*t[0]*t[0]+P[1]*t[1]*t[1]+P[2]*t[2]*t[2])/S, s=Math.sqrt(m2-m*m);
      return {q:'三条路径的时延分别为 0、'+t[1]+'、'+t[2]+' µs，功率分别为 0、'+pdB[1]+'、'+pdB[2]+' dB（相对）。求 rms 时延扩展（µs）。', a:s, rel:0.02, unit:'µs',
        s:['换成线性功率：'+P.map(function(x){return f(x,3);}).join('、')+'，总和 '+f(S),'平均时延 μ = Σ τP / ΣP = '+f(m)+' µs','E[τ²] = '+f(m2)+'，σ = √(E[τ²] − μ²) = '+f(s)+' µs']}; }},
    {id:'dop', name:'最大多普勒频移与相干时间', make:function(){
      var v=pick([36,54,72,90,108,120]), fc=pick([0.9,1.8,2.4,3.5,5]); var fm=v/3.6*fc*1e9/3e8;
      return {q:'车速 '+v+' km/h，载频 '+fc+' GHz，求最大多普勒频移 f_m（Hz）。', a:fm, rel:0.01, unit:'Hz',
        s:['v = '+v+'/3.6 = '+f(v/3.6)+' m/s','f_m = v·f_c/c = '+f(v/3.6)+' × '+fc+'×10⁹ / 3×10⁸ = '+f(fm)+' Hz','相干时间 T_C ≈ 1/f_m = '+f(1000/fm)+' ms']}; }},
    {id:'afd', name:'瑞利衰落的平均衰落时长（P2 Q1）', make:function(){
      var fd=pick([20,50,80,100,150,200]), r=pick([0.1,0.2,0.3,0.5]); var A=(Math.exp(r*r)-1)/(Math.sqrt(2*Math.PI)*fd*r);
      return {q:'瑞利衰落，最大多普勒频移 '+fd+' Hz，门限是 rms 值的 '+r+' 倍（ρ = '+r+'）。求平均衰落时长（ms）。', a:A*1e3, rel:0.02, unit:'ms',
        s:['AFD = (e^{ρ²} − 1)/(√(2π) f_D ρ)','e^{'+f(r*r)+'} − 1 = '+f(Math.exp(r*r)-1)+'；分母 = 2.5066 × '+fd+' × '+r+' = '+f(Math.sqrt(2*Math.PI)*fd*r),'AFD = '+f(A*1e3)+' ms']}; }},
    {id:'cap', name:'干扰当噪声时的容量（P2 Q3）', make:function(){
      var P=pick([5,10,20]), I=pick([1,2,5,10]), N=pick([0.1,0.2,0.5,1]), B=pick([5,10,20]); var g=P/(I+N), C=B*log2(1+g);
      return {q:'用户 1 收到 '+P+' mW，用户 2 的干扰 '+I+' mW（当高斯噪声处理），噪声 '+N+' mW，带宽 '+B+' MHz。求用户 1 的容量（Mbps）。', a:C, rel:0.01, unit:'Mbps',
        s:['SINR = '+P+' / ('+I+' + '+N+') = '+f(g),'C = '+B+' × log₂(1 + '+f(g)+') = '+f(C)+' Mbps']}; }},
    {id:'ray', name:'瑞利衰落下所需平均 SNR（第 3 章 p.33）', make:function(){
      var g0=rnd(5,12,0.5), cov=pick([90,95,99]); var Po=1-cov/100, gb=Math.pow(10,g0/10)/(-Math.log(1-Po)), dB=10*Math.log10(gb);
      return {q:'瑞利衰落，最低 SNR '+g0+' dB，要求 '+cov+'% 的时间 SNR 高于最低值。平均 SNR 至少多少 dB？', a:dB, abs:0.15, unit:'dB',
        s:['P_out = 1 − '+cov+'% = '+f(Po),'γ̄ = γ₀ / (−ln(1 − P_out)) = '+f(Math.pow(10,g0/10))+' / '+f(-Math.log(1-Po))+' = '+f(gb),'= '+f(dB,4)+' dB（衰落余量 '+f(dB-g0,3)+' dB）']}; }},
    {id:'sd', name:'选择分集的中断概率（第 4 章 p.13）', make:function(){
      var gb=rnd(10,20,1), g0=rnd(3,9,0.5), M=pick([2,3,4]); var x=Math.pow(10,(g0-gb)/10), p1=1-Math.exp(-x), p=Math.pow(p1,M);
      return {q:'瑞利衰落，每路平均 SNR '+gb+' dB，最低 SNR '+g0+' dB，'+M+' 路选择分集。求中断概率。', a:p, rel:0.03, unit:'',
        s:['γ₀/γ̄ = 10^{('+g0+' − '+gb+')/10} = '+f(x),'单路中断 1 − e^{−'+f(x)+'} = '+f(p1),M+' 路：'+f(p1)+'^'+M+' = '+f(p)]}; }},
    {id:'wf', name:'注水法求容量（P5 Q1）', make:function(){
      var g=[rnd(10,100,5),rnd(2,40,1),rnd(0.2,20,0.1)].sort(function(a,b){return b-a;}), k, g0, s;
      for(k=3;k>=1;k--){ s=1; for(var i=0;i<k;i++) s+=1/g[i]; g0=k/s; if(g[k-1]>=g0) break; }
      var C=0; for(var j=0;j<k;j++) C+=log2(g[j]/g0);
      return {q:'三个子信道的 SNR 为 '+g.join('、')+'，发射端知道信道，用注水法。求容量（bit/s/Hz）。', a:C, rel:0.01, unit:'bit/s/Hz',
        s:['先假设全部分功率，算 γ₀；若有 γ &lt; γ₀ 就去掉最差的重算','最终用 '+k+' 个子信道：'+k+'/γ₀ = '+f(s)+' → γ₀ = '+f(g0),'C = Σ log₂(γ_j/γ₀) = '+f(C)+' bit/s/Hz']}; }},
    {id:'dmt', name:'分集-复用折中的最高速率（P5 Q3）', make:function(){
      var N,M,snr,e,g,dneed,r,best=0;
      do { N=pick([2,3,4,6,8]); M=pick([2,3,4]); snr=pick([10,15,20]); e=pick([2,3,4,5,6]); g=Math.pow(10,snr/10); dneed=e*Math.log(10)/Math.log(g); } while (N*M < dneed);
      for(r=0;r<=Math.min(N,M);r++){ if((N-r)*(M-r)>=dneed-1e-9) best=r; }
      var R=best*log2(g);
      return {q:N+' × '+M+' MIMO，d(r) = (N − r)(M − r)，r、d 取整数。SNR = '+snr+' dB，要求 Pe = γ^{−d} ≤ 10^{−'+e+'}。最高速率（bit/s/Hz）？', a:R, rel:0.01, unit:'bit/s/Hz',
        s:['γ = '+f(g)+'，需要 d ≥ '+f(dneed),'d(r)：'+[0,1,2,3,4,5,6,7,8].filter(function(x){return x<=Math.min(N,M);}).map(function(x){return 'r='+x+'→'+(N-x)*(M-x);}).join('，'),'最大 r = '+best+'，R = r·log₂γ = '+f(R)+' bit/s/Hz']}; }},
    {id:'ofdm', name:'OFDM 数据速率（P7 Q2 反过来）', make:function(){
      var N=pick([32,48,60,64,80,100,128]), df=pick([5,10,12.5,15]), Tg=pick([5,10,20]), b=pick([2,4,6]); var T=1e3/df, R=b*N/((T+Tg)*1e-6)/1e6;
      return {q:'OFDM 系统：'+N+' 个子载波，子载波间隔 '+df+' kHz，循环前缀 '+Tg+' µs，每个子载波用每符号 '+b+' bit 的调制。求数据速率（Mbps）。', a:R, rel:0.01, unit:'Mbps',
        s:['有用符号时长 T = 1/Δf = '+f(T)+' µs，加 CP 后 '+f(T+Tg)+' µs','每个 OFDM 符号携带 '+N+' × '+b+' = '+N*b+' bit','R = '+N*b+' / '+f(T+Tg)+' µs = '+f(R)+' Mbps']}; }},
    {id:'zf', name:'迫零均衡器系数（第 6 章 p.24）', make:function(){
      var a=rnd(0.1,0.6,0.1), b=rnd(0.05,0.3,0.05); var c2=a*a-b;
      return {q:'信道 H(z) = 1 + '+a+'z⁻¹ + '+b+'z⁻²。迫零均衡器 C(z) = 1/H(z) = 1 + c₁z⁻¹ + c₂z⁻² + …，求 c₂。', a:c2, abs:0.002, unit:'',
        s:['长除法：第一项 1，余数 −'+a+'z⁻¹ − '+b+'z⁻²','第二项 c₁ = −'+a+'，乘回去余数为 ('+f(a*a)+' − '+b+')z⁻² + …','c₂ = a² − b = '+f(c2)]}; }}
  ];
  var sel=document.getElementById('d-type');
  G.forEach(function(g,i){ var o=document.createElement('option'); o.value=i; o.textContent=g.name; sel.appendChild(o); });
  var o=document.createElement('option'); o.value='mix'; o.textContent='混合（随机题型）'; sel.insertBefore(o, sel.firstChild); sel.value='mix';
  var cur=null, tried=0, right=0, answered=false;
  function render(){
    var g = sel.value==='mix' ? pick(G) : G[+sel.value];
    cur=g.make(); answered=false;
    document.getElementById('d-q').innerHTML='<span class="tag">'+g.name+'</span>'+cur.q;
    document.getElementById('d-unit').textContent=cur.unit;
    document.getElementById('d-ans').value=''; document.getElementById('d-verdict').innerHTML='';
    var st=document.getElementById('d-steps'); st.hidden=true;
    st.innerHTML='<ol class="steps">'+cur.s.map(function(x){return '<li>'+x+'</li>';}).join('')+'</ol><div class="ans">答案：'+f(cur.a,4)+' '+cur.unit+'</div>';
  }
  function parse(v){ v=String(v).trim().replace(/×\s*10\^?/,'e').replace(/\s/g,''); var m=v.match(/^(-?[\d.]+)%$/); if(m) return +m[1]/100; return parseFloat(v); }
  document.getElementById('d-new').addEventListener('click',render);
  sel.addEventListener('change',render);
  document.getElementById('d-show').addEventListener('click',function(){ document.getElementById('d-steps').hidden=false; });
  function check(){
    var x=parse(document.getElementById('d-ans').value); if(isNaN(x)){ document.getElementById('d-verdict').innerHTML='<div class="verdict bad">请输入一个数字。</div>'; return; }
    var ok = cur.abs!==undefined ? Math.abs(x-cur.a)<=cur.abs : Math.abs(x-cur.a)<=Math.abs(cur.a)*cur.rel;
    if(!answered){ tried++; if(ok) right++; answered=true; }
    document.getElementById('d-score').textContent='已答 '+tried+' · 答对 '+right;
    document.getElementById('d-verdict').innerHTML = ok ? '<div class="verdict good">答对了：'+f(cur.a,4)+' '+cur.unit+'</div>' : '<div class="verdict bad">不对，正确答案是 '+f(cur.a,4)+' '+cur.unit+'。看看下面的步骤。</div>';
    if(!ok) document.getElementById('d-steps').hidden=false;
  }
  document.getElementById('d-check').addEventListener('click',check);
  document.getElementById('d-ans').addEventListener('keydown',function(e){ if(e.key==='Enter') check(); });
  render();
})();
'''

def page(standalone):
    head = ('<title>EE6129 Part 2 练习</title>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">\n'
            f'<style>{CSS}</style>\n{MATHJAX}\n')
    body = BODY + f'<script>{JS}</script>\n'
    if not standalone:
        body = body.replace('  <a class="back" href="index.html">← 学习站目录</a>\n', '')
        return head + body
    return ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + body + '</body>\n</html>\n')

std = page(True)
if learn_url:
    std = std.replace(learn_url, 'p2-learn.html')
(REPO / 'p2-practice.html').write_text(std, encoding='utf-8')
ART.mkdir(exist_ok=True)
(ART / 'p2-practice.html').write_text(page(False), encoding='utf-8')
print('ok', (REPO / 'p2-practice.html').stat().st_size)
