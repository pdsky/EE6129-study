#!/usr/bin/python3
"""EE6129 Part B + C practice page (question bank + random quiz), data-driven.
usage: build_bc.py  (writes repo bc-practice.html and artifact copy)"""
import json, pathlib, re, runpy

B = pathlib.Path(__file__).parent
REPO = pathlib.Path(__file__).resolve().parents[2]
ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')
Qs = runpy.run_path(str(B / 'bc_questions.py'))['Q']
CSS = re.search(r"CSS = r'''(.*?)'''", (B / 'build_practice.py').read_text(encoding='utf-8'), re.S).group(1)

# where each topic is explained (repo page, artifact page)
LEARN = {
  'B': ('partB.html', 'https://claude.ai/artifact/Rq8eSjXVaeEVwoUvRE411c'),
  'C': ('partC.html', 'https://claude.ai/artifact/9gXNBydjgxgVdZQwSYLKfh'),
}
ANCHOR = {'WLAN':'ch1','MAC':'ch2','MANET/WSN':'ch4','LTE':'ch6','IoT':'ch7','轨道':'ch1','链路':'ch4','多址':'ch5','网络':'ch6'}

EXTRA_CSS = '''
.qcard{background:var(--surface);border:1px solid var(--border);border-radius:14px;box-shadow:var(--shadow);padding:16px 18px;margin-bottom:12px}
.qhead{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;margin-bottom:6px}
.badge{font-family:'IBM Plex Mono',monospace;font-size:.68rem;font-weight:600;border-radius:6px;padding:2px 8px;background:var(--accent-soft);color:var(--accent-strong)}
.badge.t-num{background:var(--warn-soft);color:var(--warn)}
.badge.t-short{background:var(--extra-soft);color:var(--extra)}
.qref{font-size:.74rem;color:var(--muted);margin-left:auto}
.qtext{font-size:.96rem;margin:.2em 0 .5em;max-width:76ch}
.opts{display:grid;gap:6px}
.opt{font:inherit;text-align:left;font-size:.9rem;border:1px solid var(--border);background:var(--surface-2);color:var(--text);border-radius:10px;padding:7px 12px;cursor:pointer}
.opt:hover{border-color:var(--accent)}
.opt.right{border-color:var(--ok);background:var(--ok-soft);color:var(--ok);font-weight:600}
.opt.wrong{border-color:var(--bad);background:var(--bad-soft);color:var(--bad)}
.opt[disabled]{cursor:default}
.numrow{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.numrow input{font:inherit;font-family:'IBM Plex Mono',monospace;font-size:.9rem;padding:6px 10px;border:1px solid var(--border);border-radius:8px;background:var(--surface-2);color:var(--text);width:10em}
.expl{margin-top:10px;border-radius:10px;padding:8px 14px;font-size:.88rem;background:var(--accent-soft)}
.expl .lk{display:block;margin-top:4px;font-size:.8rem}
.sum{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}
.sum div{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:6px 12px;font-size:.82rem}
.sum b{font-family:'IBM Plex Mono',monospace;font-size:1rem}
.quizbar{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin:10px 0}
'''

BODY = '''<div class="wrap" id="root">
  <a class="back" href="index.html">← 学习站目录</a>
  <div class="eyebrow">EE6129 · Part B 无线系统 · Part C 卫星通信</div>
  <h1>Part B · C 练习</h1>
  <p class="lede">讲义没有给这两部分配练习，这里按讲义逐页出了 __N__ 道题：选择题点选项即判对错，计算题输入数字自动核对，简答题点开看参考答案。每题都标了讲义页码，并链接到对应的讲解章节。</p>
  <div class="notice">题目全部出自 Part B（114 页）和 Part C（41 页）讲义；标"课外补充"的两道计算题用到讲义图上的几何关系和 Part A 的公式。「小测」每次随机抽 10 道选择题和计算题。</div>

  <div class="tabs" role="tablist" aria-label="页面视图">
    <button class="tab" role="tab" id="tab-bank" aria-controls="bank" aria-selected="true" data-tab="bank">题库</button>
    <button class="tab" role="tab" id="tab-quiz" aria-controls="quiz" aria-selected="false" data-tab="quiz">小测（随机 10 题）</button>
    <span class="spacer"></span>
    <span class="count" id="stat"></span>
  </div>

  <section id="bank" role="tabpanel" aria-labelledby="tab-bank">
    <div class="filters" id="filters"></div>
    <div id="list"></div>
  </section>

  <section id="quiz" role="tabpanel" aria-labelledby="tab-quiz" hidden>
    <div class="quizbar"><span class="score" id="qprog"></span><button class="btn" type="button" id="qnew">重新抽 10 题</button></div>
    <div id="qbox"></div>
    <div class="quizbar"><span></span><button class="btn ghost" type="button" id="qnext">下一题 →</button></div>
  </section>

  <footer>题目根据 EE6129 Part B、Part C 讲义整理，仅供个人复习。</footer>
</div>
'''

JS = r'''
(function(){
  var Q=__DATA__, LEARN=__LEARN__, ANCHOR=__ANCHOR__;
  var store={get:function(k){try{return localStorage.getItem(k);}catch(e){return null;}},set:function(k,v){try{localStorage.setItem(k,v);}catch(e){}}};
  var TYPE={mcq:'选择',num:'计算',short:'简答'};
  function esc(s){ return String(s); }
  function learnLink(q){ var a=ANCHOR[q.topic]||''; return '<a class="lk" href="'+LEARN[q.part]+(a?'#'+a:'')+'">去 Part '+q.part+' 讲解页看「'+q.topic+'」→</a>'; }
  function parse(v){ v=String(v).trim().replace(/×\s*10\^?/,'e').replace(/\s/g,''); return parseFloat(v); }
  function okNum(q,x){ if(isNaN(x)) return false; if(q.abs!==null&&q.abs!==undefined) return Math.abs(x-q.ans)<=q.abs+1e-9; return Math.abs(x-q.ans)<=Math.abs(q.ans)*(q.rel||0.02); }
  function stat(){ var done=Q.filter(function(q){return store.get('ee6129-bc:'+q.id)==='1';}).length; document.getElementById('stat').textContent='已答对 '+done+' / '+Q.length; }

  function card(q, onResult){
    var el=document.createElement('article'); el.className='qcard'; el.id='q-'+q.id;
    var h='<div class="qhead"><span class="badge t-'+q.type+'">Part '+q.part+' · '+q.topic+' · '+TYPE[q.type]+'</span><span class="qref">'+q.ref+'</span></div><div class="qtext">'+q.q+'</div>';
    if(q.type==='mcq'){ h+='<div class="opts">'+q.opts.map(function(o,i){return '<button type="button" class="opt" data-i="'+i+'">'+String.fromCharCode(65+i)+'. '+o+'</button>';}).join('')+'</div>'; }
    else if(q.type==='num'){ h+='<div class="numrow"><input type="text" inputmode="decimal" aria-label="答案"><span class="score">'+(q.unit||'')+'</span><button class="btn" type="button" data-act="check">核对</button><button class="btn ghost" type="button" data-act="show">看解析</button></div>'; }
    else { h+='<button class="reveal" style="display:inline-block" type="button" data-act="show">显示参考答案</button>'; }
    h+='<div class="expl" hidden></div>';
    el.innerHTML=h;
    var ex=el.querySelector('.expl');
    function showExp(prefix){ ex.innerHTML=(prefix||'')+(q.type==='short'?q.model:q.exp)+learnLink(q); ex.hidden=false; }
    if(q.type==='mcq'){
      var bs=[].slice.call(el.querySelectorAll('.opt'));
      bs.forEach(function(b){ b.addEventListener('click',function(){
        var i=+b.dataset.i, ok=i===q.ans;
        bs.forEach(function(x){ x.disabled=true; if(+x.dataset.i===q.ans) x.classList.add('right'); });
        if(!ok) b.classList.add('wrong');
        showExp(ok?'<b>答对了。</b>':'<b>正确答案是 '+String.fromCharCode(65+q.ans)+'。</b>');
        if(onResult) onResult(ok);
      }); });
    } else if(q.type==='num'){
      var inp=el.querySelector('input');
      function chk(){ var ok=okNum(q,parse(inp.value)); showExp((ok?'<b>答对了：</b>':'<b>答案是 ')+q.ans+' '+(q.unit||'')+(ok?'。':'。</b>')+' '); if(onResult){ onResult(ok); onResult=null; } }
      el.querySelector('[data-act="check"]').addEventListener('click',chk);
      inp.addEventListener('keydown',function(e){ if(e.key==='Enter') chk(); });
      el.querySelector('[data-act="show"]').addEventListener('click',function(){ showExp('<b>答案：'+q.ans+' '+(q.unit||'')+'。</b>'); });
    } else {
      el.querySelector('[data-act="show"]').addEventListener('click',function(e){ e.target.style.display='none'; showExp('<b>参考答案：</b>'); });
    }
    return el;
  }

  // bank
  var topics=[]; Q.forEach(function(q){ var k=q.part+'|'+q.topic; if(topics.indexOf(k)<0) topics.push(k); });
  var fbar=document.getElementById('filters'), list=document.getElementById('list');
  function fbtn(label,key){ var b=document.createElement('button'); b.type='button'; b.className='chipbtn'; b.textContent=label; b.dataset.k=key; fbar.appendChild(b); return b; }
  fbtn('全部','all').classList.add('on'); fbtn('Part B','B'); fbtn('Part C','C');
  topics.forEach(function(k){ var p=k.split('|'); fbtn(p[0]+' · '+p[1],k); });
  ['mcq','num','short'].forEach(function(t){ fbtn('只看'+TYPE[t]+'题','t:'+t); });
  Q.forEach(function(q){ list.appendChild(card(q,function(ok){ if(ok){ store.set('ee6129-bc:'+q.id,'1'); stat(); } })); });
  fbar.addEventListener('click',function(e){
    var b=e.target.closest('.chipbtn'); if(!b) return;
    [].forEach.call(fbar.children,function(x){x.classList.remove('on');}); b.classList.add('on');
    var k=b.dataset.k;
    Q.forEach(function(q){ var show = k==='all' || k===q.part || k===q.part+'|'+q.topic || k==='t:'+q.type; document.getElementById('q-'+q.id).classList.toggle('hide',!show); });
  });
  stat();

  // quiz
  var pool=Q.filter(function(q){return q.type!=='short';}), set=[], idx=0, score=0;
  function newQuiz(){ set=pool.slice().sort(function(){return Math.random()-0.5;}).slice(0,10); idx=0; score=0; showQ(); }
  function showQ(){
    var box=document.getElementById('qbox'); box.innerHTML='';
    if(idx>=set.length){ box.innerHTML='<div class="qcard"><h3>完成：答对 '+score+' / '+set.length+'</h3><p class="score">点"重新抽 10 题"再来一轮；没答对的题可以回题库按主题复习。</p></div>'; document.getElementById('qprog').textContent=''; document.getElementById('qnext').style.visibility='hidden'; return; }
    document.getElementById('qnext').style.visibility='visible';
    document.getElementById('qprog').textContent='第 '+(idx+1)+' / '+set.length+' 题 · 已答对 '+score;
    var answered=false;
    box.appendChild(card(set[idx],function(ok){ if(answered) return; answered=true; if(ok){ score++; store.set('ee6129-bc:'+set[idx].id,'1'); stat(); } document.getElementById('qprog').textContent='第 '+(idx+1)+' / '+set.length+' 题 · 已答对 '+score; }));
  }
  document.getElementById('qnew').addEventListener('click',newQuiz);
  document.getElementById('qnext').addEventListener('click',function(){ idx++; showQ(); });
  newQuiz();

  // tabs
  var tabs=[].slice.call(document.querySelectorAll('[data-tab]'));
  function show(id){ tabs.forEach(function(t){ var on=t.dataset.tab===id; t.setAttribute('aria-selected',String(on)); document.getElementById(t.dataset.tab).hidden=!on; }); }
  tabs.forEach(function(t){ t.addEventListener('click',function(){ show(t.dataset.tab); try{history.replaceState(null,'','#'+t.dataset.tab);}catch(e){} }); });
  if((location.hash||'')==='#quiz') show('quiz');
})();
'''

def page(standalone):
    learn = {k: (v[0] if standalone else v[1]) for k, v in LEARN.items()}
    js = (JS.replace('__DATA__', json.dumps(Qs, ensure_ascii=False))
            .replace('__LEARN__', json.dumps(learn, ensure_ascii=False))
            .replace('__ANCHOR__', json.dumps(ANCHOR, ensure_ascii=False)))
    body = BODY.replace('__N__', str(len(Qs)))
    head = ('<title>EE6129 Part B·C 练习</title>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">\n'
            f'<style>{CSS}{EXTRA_CSS}</style>\n')
    if not standalone:
        body = body.replace('  <a class="back" href="index.html">← 学习站目录</a>\n', '')
        return head + body + f'<script>{js}</script>\n'
    return ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + body + f'<script>{js}</script>\n</body>\n</html>\n')

(REPO / 'bc-practice.html').write_text(page(True), encoding='utf-8')
ART.mkdir(exist_ok=True)
(ART / 'bc-practice.html').write_text(page(False), encoding='utf-8')
print('ok', len(Qs), 'questions', (REPO / 'bc-practice.html').stat().st_size)
