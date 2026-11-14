#!/usr/bin/python3
"""「EE6129 练习」as ONE page (no tabs): every practice question, lecture example, B·C quiz question and
past-exam part, ordered by chapter (Part 2 → Part A → Part B → Part C), practice first and the past-exam
parts of that chapter after it. The user asked (2026-11-14) for all worked examples in one part instead of
several tabs.

The blocks are cut out of the built pages (EE6129_artifacts/*.html, or the translated en/*.html for the
bilingual edition), each wrapped in <div class="mp-item src-…">. Every source page's own CSS is scoped to
its .src-… class (scope_css), so blocks look exactly as on their own page and nothing clashes. HW1 and the
SW homework stay whole pages, embedded in an iframe that opens with its <details>.

build(pages, lang, out, urls): pages = {'exams','p2-practice','examples','hw1','bc-practice','homework-sw': html}
"""
import json, re, pathlib

H = pathlib.Path(__file__).resolve().parent
REPO = H.parents[1]
IDS = json.loads((REPO / 'src' / 'artifact_ids.json').read_text(encoding='utf-8'))
ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')

SRC = {'p2-practice': 'src-p2', 'examples': 'src-exm', 'exams': 'src-ex', 'bc-practice': 'src-bc'}
STATES = ('exam', 'no-zh', 'lang-en', 'lang-zh', 'hide-zh')

# ---------------------------------------------------------------- chapter plan
# practice items per chapter (exam parts are added automatically from their "back to the notes" link)
P2 = {'ch1': ['p8q1'],
      'ch2': ['p1q1', 'p1q2', 'p1q3', 'p2q1', 'p2q2', 'p2q3'] + [f'p8q{i}' for i in range(2, 13)],
      'ch3': ['p3q1', 'p3q2', 'p3q3'], 'ch4': ['p4q1', 'p4q2', 'p4q3'], 'ch5': ['p5q1', 'p5q2', 'p5q3'],
      'ch6': ['p6q1', 'p6q2', 'p6q3'], 'ch7': ['p7q1', 'p7q2', 'p7q3']}
PA = {'ch4': ['p44', 'p47'], 'ch5': ['p65'], 'ch6': ['p82', 'p89'], 'ch7': ['p91', 'p93'],
      'ch8': ['p121', 'p123', 'p130', 'p133'], 'ch9': ['p136', 'p140', 'p145', 'p148']}
PB = {'ch1': [f'b{i}' for i in range(1, 6)], 'ch2': [f'b{i}' for i in range(6, 12)],
      'ch3': [f'b{i}' for i in range(12, 17)], 'ch4': [f'b{i}' for i in range(17, 21)],
      'ch5': ['b21', 'b22'], 'ch6': [f'b{i}' for i in range(23, 32)], 'ch7': [f'b{i}' for i in range(32, 40)]}
PC = {'ch1': ['c1', 'c2'], 'ch2': ['c3', 'c5', 'c9'], 'ch3': ['c4', 'c6', 'c7', 'c8'],
      'ch4': [f'c{i}' for i in range(10, 16)], 'ch5': [f'c{i}' for i in range(16, 22)], 'ch6': ['c22', 'c23']}
PARTS = [('p2', 'p2-learn', P2, 'p2'), ('A', 'partA', PA, 'A'), ('B', 'partB', PB, 'B'), ('C', 'partC', PC, 'C')]

L = {
 'zh': dict(title='EE6129 练习', brand='练习', exam='自测模式（先藏解答）', zhq='题目中文对照', sol='解答', mastered='已掌握',
            learn='看讲解 →', src={'p2': 'Part 2 练习', 'exm': '讲义例题', 'ex': '历年真题', 'bc': 'B·C 练习'},
            part={'p2': 'Part 2 · 信道到 OFDM（期末 Q1–Q2）', 'A': 'Part A · 蜂窝网络（期末 Q3–Q4）',
                  'B': 'Part B · 无线系统（期末 Q4）', 'C': 'Part C · 卫星通信（期末 Q4）'},
            drill='随机练习（数字随机生成）', sw='Part 2 作业（SW）：题目、英文答案、中文讲解', sheet='Part A 考前速记页',
            hw1='HW1（Part A 作业）：讲解和参考答案', quiz='B·C 随机小测（每次 10 题）', overview='历年真题：出题规律和四份卷对照',
            open='点开查看', loading='正在载入…', toc='目录', counts='练习 {p} 题 · 真题 {e} 题',
            other='中英对照版', to_learn='← 去学习', ch='第 {n} 章'),
 'en': dict(title='EE6129 Practice (EN + 中文)', brand='Practice', exam='Self-test (hide solutions)', zhq='Show 中文 question',
            sol='Solution', mastered='Mastered', learn='Notes →',
            src={'p2': 'Part 2 practice', 'exm': 'Lecture example', 'ex': 'Past final exam', 'bc': 'B·C quiz'},
            part={'p2': 'Part 2 · Channel to OFDM (final Q1–Q2)', 'A': 'Part A · Cellular networks (final Q3–Q4)',
                  'B': 'Part B · Wireless systems (final Q4)', 'C': 'Part C · Satellite communications (final Q4)'},
            drill='Random drill (new numbers each time)', sw='Part 2 homework (SW): questions, English answers, Chinese notes',
            sheet='Part A one-page summary', hw1='HW1 (Part A homework): explanations and model answers',
            quiz='B·C random quiz (10 questions)', overview='Past finals: what is asked, four papers side by side',
            open='open', loading='Loading…', toc='Contents', counts='{p} practice · {e} past-exam',
            other='中文版', to_learn='← Learn', ch='Ch. {n}'),
}


# ---------------------------------------------------------------- helpers
def block_end(s, i, tag):
    depth = 0
    for m in re.compile(rf'<{tag}\b|</{tag}>').finditer(s, i):
        depth += 1 if m.group(0) != f'</{tag}>' else -1
        if depth == 0:
            return m.end()
    raise ValueError(f'unbalanced <{tag}> at {s[i:i + 80]!r}')


def block(s, pat, tag):
    m = re.search(pat, s)
    if not m:
        raise SystemExit(f'not found: {pat}')
    return s[m.start():block_end(s, m.start(), tag)]


def blocks(s, pat, tag):
    out = {}
    for m in re.finditer(pat, s):
        out[m.group(1)] = s[m.start():block_end(s, m.start(), tag)]
    return out


def split_sel(sel):
    out, depth, cur = [], 0, ''
    for ch in sel:
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        if ch == ',' and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def scope_sel(sel, S):
    m = re.match(r'^(:root|html|body)((?:[.\[:#][^\s>+~]*)?)(.*)$', sel, re.S)
    if m:
        base, qual, rest = m.groups()
        return f'{base}{qual} {S}{rest}' if qual else f'{S}{rest}'
    m = re.match(r'^(\.(?:' + '|'.join(STATES) + r')(?![\w-])[^\s>+~]*)(.*)$', sel, re.S)
    if m:
        return f'body{m.group(1)} {S}{m.group(2)}'
    return f'{S} {sel}'


def scope_css(css, S):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0:
            break
        head = css[i:j].strip()
        depth, k = 1, j + 1
        while depth and k < n:
            depth += {'{': 1, '}': -1}.get(css[k], 0); k += 1
        body = css[j + 1:k - 1]
        if head.startswith('@media') or head.startswith('@supports'):
            out.append(f'{head}{{{scope_css(body, S)}}}')
        elif head.startswith('@'):
            semi = [x for x in head.split(';')]      # stray @import/@charset before the block
            out.append(f'{semi[-1].strip()}{{{body}}}')
        else:
            head = head.split(';')[-1].strip()       # drop junk like a stray "@charset …;"
            if head:
                out.append(','.join(scope_sel(x, S) for x in split_sel(head)) + '{' + body + '}')
        i = k
    return '\n'.join(out)


def styles(s):
    return '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', s, re.S))


def links(s):
    return re.findall(r'<link rel="stylesheet"[^>]*>', s)


def learn_ref(blk):
    """(page key, chapter id) from an exam block's 'back to the notes' link."""
    for aid, ch in re.findall(r'claude\.ai/artifact/([A-Za-z0-9]{16,})#(ch\d+)', blk):
        for key, page in (('p2-learn', 'p2'), ('partA', 'A'), ('partB', 'B'), ('partC', 'C')):
            if IDS.get(key, {}).get('new') == aid or IDS.get(key, {}).get('old') == aid:
                return page, ch
    for f, ch in re.findall(r'(p2-learn|partA|partB|partC)\.html#(ch\d+)', blk):
        return {'p2-learn': 'p2', 'partA': 'A', 'partB': 'B', 'partC': 'C'}[f], ch
    raise SystemExit('exam block without a notes link: ' + blk[:120])


def chapter_titles(lang):
    out = {}
    d = ART / 'en' if lang == 'en' else ART
    for page, f in (('p2', 'p2-learn'), ('A', 'partA'), ('B', 'partB'), ('C', 'partC')):
        s = (d / f'{f}.html').read_text(encoding='utf-8')
        for m in re.finditer(r'<section class="chapter" id="(ch\d+)".*?<h2>(.*?)</h2>', s, re.S):
            t = re.sub(r'<span class="zhsub".*?</span>', '', m.group(2), flags=re.S)
            out[(page, m.group(1))] = re.sub(r'<[^>]+>', '', t).strip()
    return out


def art_url(key):
    v = IDS.get(key, {}).get('new')
    return f'https://claude.ai/artifact/{v}' if v else ''


def route_table():
    """artifact id / file name → [hub, tab] for every EE6129 page (same tabs as the learn hub uses)."""
    tabs = {'learn': [('p2', 'p2-learn', 'p2-learn.html'), ('ch12', 'quiz-summary', 'quiz-summary.html'),
                      ('A', 'partA', 'partA.html'), ('B', 'partB', 'partB.html'), ('C', 'partC', 'partC.html')],
            'practice': [('exams', 'exams', 'exams.html'), ('p2prac', 'p2-practice', 'p2-practice.html'),
                         ('Aex', 'examples', 'examples.html'), ('hw1', 'hw1', 'hw1.html'),
                         ('bc', 'bc-practice', 'bc-practice.html'), ('hwsw', 'homework-sw', 'homework_sw.html')]}
    r = {}
    for hub, lst in tabs.items():
        for tid, key, fname in lst:
            v = IDS.get(key, {})
            for k in ('new', 'old'):
                if v.get(k):
                    r[v[k]] = [hub, tid]
            r[fname] = [hub, tid]
    return r


def embed(s):
    return json.dumps(s, ensure_ascii=False).replace('</', '<\\/').replace('<!--', '<\\u0021--')


def strip_skeleton(s):
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


# ---------------------------------------------------------------- page CSS / JS
CSS = r'''
:root{--mp-bg:#eceff0;--mp-surface:#fff;--mp-surface2:#e3e9e9;--mp-border:#cbd6d7;--mp-text:#13201f;--mp-muted:#4e615f;
  --mp-accent:#0f766e;--mp-accent-strong:#0a5a53;--mp-accent-soft:#d7eeeb;--mp-on:#fff;--mp-p2:#2f4fc4;--mp-pa:#b4790f;--mp-pb:#7a4fc4;--mp-pc:#b03a5b}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;--mp-bg:#0b1413;--mp-surface:#111e1c;--mp-surface2:#182825;--mp-border:#273a36;
  --mp-text:#e6f0ed;--mp-muted:#9ab3ad;--mp-accent:#33d1bf;--mp-accent-strong:#7ceede;--mp-accent-soft:#113330;--mp-on:#08100e;--mp-p2:#8fa6f5;--mp-pa:#e0ac4b;--mp-pb:#b79cf0;--mp-pc:#f08aa6}}
:root[data-theme="dark"]{color-scheme:dark;--mp-bg:#0b1413;--mp-surface:#111e1c;--mp-surface2:#182825;--mp-border:#273a36;
  --mp-text:#e6f0ed;--mp-muted:#9ab3ad;--mp-accent:#33d1bf;--mp-accent-strong:#7ceede;--mp-accent-soft:#113330;--mp-on:#08100e;--mp-p2:#8fa6f5;--mp-pa:#e0ac4b;--mp-pb:#b79cf0;--mp-pc:#f08aa6}
*{box-sizing:border-box}
html{scroll-padding-top:64px}
body{margin:0;background:var(--mp-bg);color:var(--mp-text);font-family:'IBM Plex Sans','Noto Sans CJK SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased}
[hidden]{display:none!important}
.mp-top{position:sticky;top:0;z-index:40;background:var(--mp-bg);border-bottom:1px solid var(--mp-border)}
.mp-row{max-width:1320px;margin:0 auto;padding:8px 16px;display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center}
.mp-brand{font-family:'Barlow Condensed','Noto Sans CJK SC',sans-serif;font-size:1.25rem;font-weight:700;letter-spacing:.01em;margin-right:4px;white-space:nowrap}
.mp-brand b{color:var(--mp-accent-strong)}
.mp-sp{flex:1}
.mp-tg{display:flex;align-items:center;gap:6px;font-size:.82rem;color:var(--mp-muted);cursor:pointer;white-space:nowrap}
.mp-tg input{accent-color:var(--mp-accent);width:16px;height:16px}
.mp-seg{display:inline-flex;align-items:center;border:1px solid var(--mp-border);border-radius:999px;overflow:hidden;font-size:.8rem;background:var(--mp-surface)}
.mp-seg span{padding:0 8px 0 10px;color:var(--mp-muted)}
.mp-seg button{font:inherit;border:none;border-left:1px solid var(--mp-border);background:transparent;color:var(--mp-muted);padding:4px 11px;cursor:pointer}
.mp-seg button[aria-pressed="true"]{background:var(--mp-accent);color:var(--mp-on);font-weight:600}
.mp-count{font-family:'IBM Plex Mono',monospace;font-size:.75rem;color:var(--mp-muted);white-space:nowrap}
.mp-switch{font-size:.8rem;font-weight:600;text-decoration:none;color:var(--mp-accent-strong);border:1px solid var(--mp-border);border-radius:999px;padding:4px 12px;background:var(--mp-surface);white-space:nowrap}
.mp-jump{display:none;font:inherit;font-size:.85rem;padding:5px 8px;border:1px solid var(--mp-border);border-radius:8px;background:var(--mp-surface);color:var(--mp-text);max-width:100%}
.mp-layout{max-width:1320px;margin:0 auto;padding:0 16px 80px;display:grid;grid-template-columns:250px minmax(0,1fr);gap:28px}
.mp-rail{position:sticky;top:64px;align-self:start;max-height:calc(100vh - 76px);overflow:auto;padding:18px 0 30px;font-size:.84rem}
.mp-rail .pt{font-weight:700;margin:14px 0 4px;font-size:.8rem;letter-spacing:.02em}
.mp-rail ol{list-style:none;margin:0;padding:0}
.mp-rail a{display:block;padding:3px 8px;border-left:2px solid transparent;color:var(--mp-muted);text-decoration:none;line-height:1.45}
.mp-rail a:hover{color:var(--mp-text)}
.mp-rail a.on{border-left-color:var(--mp-accent);color:var(--mp-accent-strong);font-weight:600;background:var(--mp-accent-soft)}
.mp-rail a .n{font-family:'IBM Plex Mono',monospace;font-size:.7rem;opacity:.8}
.mp-main{min-width:0;padding-top:12px}
.mp-intro{background:var(--mp-surface);border:1px solid var(--mp-border);border-radius:14px;padding:18px 22px;margin:14px 0 6px}
.mp-intro h1{font-family:'Barlow Condensed','Noto Sans CJK SC',sans-serif;font-size:2rem;line-height:1.15;margin:0 0 .3em}
.mp-intro p,.mp-intro li{max-width:80ch;font-size:.93rem}
.mp-intro table{border-collapse:collapse;font-size:.86rem;margin:8px 0}
.mp-intro th,.mp-intro td{padding:5px 10px;border-bottom:1px solid var(--mp-border);text-align:left;vertical-align:top}
.mp-intro a{color:var(--mp-accent-strong)}
.mp-part{margin:46px 0 4px;padding:10px 0 4px;border-bottom:3px solid var(--mp-p2);font-family:'Barlow Condensed','Noto Sans CJK SC',sans-serif;font-size:1.7rem;font-weight:700;line-height:1.2}
.mp-part.A{border-color:var(--mp-pa)} .mp-part.B{border-color:var(--mp-pb)} .mp-part.C{border-color:var(--mp-pc)}
.mp-ch{margin:26px 0 0}
.mp-chh{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;margin:0 0 6px;padding:10px 0 6px;border-bottom:1px solid var(--mp-border)}
.mp-chh h2{font-family:'Barlow Condensed','Noto Sans CJK SC',sans-serif;font-size:1.4rem;line-height:1.2;margin:0;flex:1 1 320px}
.mp-chh .meta{font-size:.78rem;color:var(--mp-muted)}
.mp-chh a{font-size:.8rem;font-weight:600;color:var(--mp-accent-strong);text-decoration:none;white-space:nowrap}
.mp-item{margin:14px 0 0;scroll-margin-top:70px}
.mp-tag{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:.66rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border-radius:6px;padding:1px 8px;margin:0 0 4px;background:var(--mp-accent-soft);color:var(--mp-accent-strong)}
.mp-tag.mp-x{background:#f7e8d2;color:#7a4a0c}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .mp-tag.mp-x{background:#2f2210;color:#f0b56a}}
.mp-item .pastq{margin-top:2px}
.mp-item > .ex,.mp-item > .qcard{margin-bottom:0}
details.mp-embed{border:1px solid var(--mp-border);border-radius:14px;background:var(--mp-surface);margin:14px 0 0}
details.mp-embed > summary{cursor:pointer;padding:12px 18px;font-weight:700;list-style:none}
details.mp-embed > summary::before{content:'▸ ';color:var(--mp-accent)}
details.mp-embed[open] > summary::before{content:'▾ '}
details.mp-embed iframe{display:block;width:100%;border:0;border-top:1px solid var(--mp-border);min-height:420px;background:var(--mp-surface)}
[class^="src-"],[class*=" src-"]{background:none!important;margin:0;padding:0;min-height:0!important}
@media (max-width:980px){.mp-layout{grid-template-columns:minmax(0,1fr)}.mp-rail{display:none}.mp-jump{display:block}}
@media (max-width:560px){.mp-top{position:static}html{scroll-padding-top:8px}.mp-item,[id]{scroll-margin-top:8px}.mp-brand{font-size:1.1rem}.mp-intro{padding:14px}}
'''

JS = r'''
(function(){
  var store={get:function(k){try{return localStorage.getItem(k);}catch(e){return null;}},set:function(k,v){try{localStorage.setItem(k,v);}catch(e){}}};
  var B=document.body;
  /* ---- toolbar: self-test, Chinese question lines, solution language ---- */
  var exam=document.getElementById('mpExam'), zh=document.getElementById('mpZh');
  var exs=[].slice.call(document.querySelectorAll('.mp-item .ex'));
  exam.addEventListener('change',function(){ B.classList.toggle('exam',exam.checked); exs.forEach(function(e){e.classList.remove('open');}); });
  if (store.get('ee6129-p2:zh')==='0'){ zh.checked=false; B.classList.add('no-zh'); }
  zh.addEventListener('change',function(){ B.classList.toggle('no-zh',!zh.checked); store.set('ee6129-p2:zh',zh.checked?'1':'0'); });
  var lb=[].slice.call(document.querySelectorAll('#mpLang button'));
  function setLang(l){ B.classList.toggle('lang-en',l==='en'); B.classList.toggle('lang-zh',l==='zh'); lb.forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.lang===l));}); store.set('ee6129-p2:sollang',l); }
  if (lb.length){ setLang(store.get('ee6129-p2:sollang')==='zh'?'zh':'en'); lb.forEach(function(b){ b.addEventListener('click',function(){ setLang(b.dataset.lang); }); }); }
  /* ---- reveal + mastered (same storage keys as the old pages) ---- */
  var cnt=document.getElementById('mpCount');
  function count(){ var d=exs.filter(function(e){return e.classList.contains('mastered');}).length; cnt.textContent=cnt.dataset.l+' '+d+' / '+exs.length; }
  exs.forEach(function(e){
    var r=e.querySelector('.reveal'); if(r) r.addEventListener('click',function(){ e.classList.add('open'); });
    var cb=e.querySelector('.done input'); if(!cb) return;
    var key=(e.closest('.src-exm')?'ee6129-ex:':'ee6129-p2:')+e.id;
    if (store.get(key)==='1'){ cb.checked=true; e.classList.add('mastered'); }
    cb.addEventListener('change',function(){ e.classList.toggle('mastered',cb.checked); store.set(key,cb.checked?'1':'0'); count(); });
  });
  count();
  /* ---- embedded whole pages (HW1, SW homework) ---- */
  function wrap(html){ return '<!doctype html><html lang="'+document.documentElement.lang+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>'; }
  function fit(f){ try{ var d=f.contentDocument; f.style.height=Math.max(420,d.documentElement.scrollHeight,d.body.scrollHeight)+'px'; }catch(e){} }
  function openEmbed(det, anchor){
    det.open=true;
    var f=det.querySelector('iframe');
    if(!f){ f=document.createElement('iframe'); f.title=det.querySelector('summary').textContent;
      f.addEventListener('load',function(){ try{ hook(f.contentDocument); var ro=new ResizeObserver(function(){fit(f);}); ro.observe(f.contentDocument.body); }catch(e){} fit(f); setTimeout(function(){fit(f);},600);
        if(anchor){ setTimeout(function(){ try{ var el=f.contentDocument.getElementById(anchor); if(el){ var y=f.getBoundingClientRect().top+window.scrollY+el.getBoundingClientRect().top-70; window.scrollTo(0,y);} }catch(e){} },500); } });
      f.srcdoc=wrap(EMBED[det.dataset.page]); det.appendChild(f); }
    else if (anchor){ try{ var el=f.contentDocument.getElementById(anchor); if(el){ var y=f.getBoundingClientRect().top+window.scrollY+el.getBoundingClientRect().top-70; window.scrollTo(0,y);} }catch(e){} }
  }
  [].forEach.call(document.querySelectorAll('details.mp-embed'),function(det){ det.addEventListener('toggle',function(){ if(det.open) openEmbed(det); }); });
  /* ---- links: in-page, to the learning hub, outside ---- */
  function openOut(href){ var a=document.createElement('a'); a.href=href; a.target='_blank'; a.rel='noopener'; document.body.appendChild(a); a.click(); a.remove(); }
  function reveal(el){ var d=el.closest('details'); while(d){ d.open=true; d=d.parentElement&&d.parentElement.closest('details'); } }
  function goto(id){
    if(!id) return false;
    var el=document.getElementById(id) || document.getElementById('q-'+id);
    if(!el && LEGACY[id]) el=document.getElementById(LEGACY[id]);
    if(!el) return false;
    if(el.matches('details.mp-embed')){ openEmbed(el); }
    reveal(el); el.scrollIntoView({block:'start'});
    try{ history.replaceState(null,'','#'+id); }catch(e){}
    return true;
  }
  function route(href){
    var m=href.match(/artifact\/([A-Za-z0-9]{16,})(?:[^#]*)(?:#(.*))?$/), key=null, anchor=null;
    if(m){ key=m[1]; anchor=m[2]||null; } else { var f=href.match(/^([\w.-]+\.html)(?:#(.*))?$/); if(f){ key=f[1]; anchor=f[2]||null; } }
    if(!key||!ROUTE[key]) return null;
    return [ROUTE[key][0],ROUTE[key][1],anchor];
  }
  function follow(href){
    if(href.charAt(0)==='#'){ return goto(decodeURIComponent(href.slice(1))); }
    var r=route(href);
    if(r){
      if(r[0]==='practice'){
        if(r[1]==='hw1'||r[1]==='hwsw'){ var det=document.getElementById(r[1]); if(det){ det.scrollIntoView({block:'start'}); openEmbed(det,r[2]); } return true; }
        return goto(r[2]||r[1]) || true;
      }
      if(LEARN) openOut(LEARN+'#'+r[1]+(r[2]?'~'+r[2]:'')); return true;
    }
    if(/^(https?:|mailto:)/.test(href)){ openOut(href); return true; }
    return false;
  }
  function hook(doc){
    doc.addEventListener('click',function(e){
      if(e.defaultPrevented||e.button!==0) return;
      var a=e.target.closest&&e.target.closest('a[href]'); if(!a) return;
      var href=a.getAttribute('href'); if(!href) return;
      if(doc!==document && href.charAt(0)==='#'){ return; }
      if(follow(href)) e.preventDefault();
    });
  }
  hook(document);
  /* ---- contents rail + phone jump list ---- */
  var rl=[].slice.call(document.querySelectorAll('.mp-rail a')), jump=document.getElementById('mpJump');
  jump.addEventListener('change',function(){ goto(jump.value); });
  var secs=rl.map(function(a){ return document.getElementById(a.getAttribute('href').slice(1)); }).filter(Boolean);
  var io=new IntersectionObserver(function(es){ es.forEach(function(en){ if(!en.isIntersecting) return; var id=en.target.id;
    rl.forEach(function(a){ var on=a.getAttribute('href')==='#'+id; a.classList.toggle('on',on); if(on&&a.scrollIntoView) a.scrollIntoView({block:'nearest'}); }); jump.value=id; }); },{rootMargin:'-12% 0px -78% 0px'});
  secs.forEach(function(s){ io.observe(s); });
  if(location.hash.length>1){ var h=decodeURIComponent(location.hash.slice(1)); setTimeout(function(){ if(!goto(h) && LEGACY[h]) goto(LEGACY[h]); },300); }
})();
'''

INTRO = {
 'zh': '''<h1>EE6129 期末复习 · 练习</h1>
<p>所有练习都在这一页：Part 2 的 7 份 Practice 和自编模拟题、Part A 讲义例题、Part B·C 练习题，以及四份历年期末卷的每一小题，<b>按章节排在一起</b>。每章先放练习 / 例题，再放这一章考过的真题（橙色「历年真题」标签）。左边是目录（手机上在顶部下拉框）。</p>
<ul>
<li>每道题下面都有<b>「📘 知识讲解 + 详细解析」</b>：从零讲这道题用到的知识，再一步一步讲怎么做、为什么这样做、易错点和考试英文写法。</li>
<li>顶部的<b>自测模式</b>会先把 Practice 和例题的解答藏起来，自己做完再点「显示解答」；真题的解答本来就收在「看解答和知识点」里。</li>
<li><b>题目中文对照</b>控制 Part 2 题目下面的中文；<b>解答 EN / 中文</b>切换 Part 2 解答的语言（考试用英文答，默认英文）。</li>
<li>期末 4 道大题：Q1–Q2 出自 Part 2（Q2(a) 每年都是残余 ISI 误码率，Q2(b) 每年都是 OFDM），Q3 是 Part A 话务 / 复用计算，Q4 是简答（每年都有 IoT）。</li>
</ul>''',
 'en': '''<h1>EE6129 final revision · Practice (EN + 中文)</h1>
<p>All practice is on this one page: the seven Part 2 practice sheets and the mock questions, the Part A lecture examples, the Part B·C quiz questions, and every part of the four past final papers, <b>ordered by chapter</b>. Each chapter starts with the practice / example questions, followed by the past-exam parts on that chapter (orange "Past final exam" tag). The contents list is on the left (on a phone, use the drop-down at the top).</p>
<p class="zhp">所有练习都在这一页，按章节排：每章先放练习 / 例题，再放这一章考过的真题。英文在上、中文在下；右下角「中文 ✓」可以隐藏全部中文。</p>
<ul>
<li>Every question has a <b>"📘 Concept + Step by step"</b> box: the knowledge behind the question explained from scratch, then every step with the reason for it, the pitfalls and how to write the answer in the exam.</li>
<li><b>Self-test</b> (top bar) hides the solutions of the practice sheets and examples until you click "Show solution"; past-exam solutions are always folded under their own button.</li>
<li>Final paper: Q1–Q2 are Part 2 (Q2(a) is residual-ISI error probability every year, Q2(b) is always OFDM), Q3 is Part A traffic / reuse calculation, Q4 is short answers (IoT every year).</li>
</ul>''',
}


# ---------------------------------------------------------------- build
def build(pages, lang, out, urls):
    T = L[lang]
    p2, exm, exs, bc = pages['p2-practice'], pages['examples'], pages['exams'], pages['bc-practice']
    it_p2 = blocks(p2, r'<article class="ex" id="(p\dq\d+)">', 'article')
    it_exm = blocks(exm, r'<article class="ex"[^>]*id="(p\d+)"', 'article')
    it_ex = blocks(exs, r'<div class="pastq" id="([\w-]+)">', 'div')
    bcQ = re.findall(r'"id": "([bc]\d+)"', bc)
    overview = block(exs, r'<section class="chapter" id="overview"', 'section').replace('id="overview"', 'id="ex-overview"', 1)
    gi = exm.index('<div class="group" id="sheet">')
    sheet = '\n'.join(exm[gi + m.start():block_end(exm, gi + m.start(), 'div')]
                      for m in re.finditer(r'<div class="sheet"', exm[gi:])).replace('id="bc"', 'id="exm-sheet-bc"', 1)
    drill = block(p2, r'<section id="drill"', 'section').replace(' hidden>', '>', 1)
    quiz = block(bc, r'<section id="quiz"', 'section').replace(' hidden>', '>', 1)
    xplt = block(bc, r'<div id="xplt" hidden>', 'div')

    # exam parts → chapters
    ex_at = {}
    for qid, blk in it_ex.items():
        ex_at.setdefault(learn_ref(blk), []).append(qid)
    titles = chapter_titles(lang)

    used = {'p2': set(), 'exm': set(), 'ex': set(), 'bc': set()}

    def item(kind, qid):
        used[kind].add(qid)
        tag = f'<span class="mp-tag{" mp-x" if kind == "ex" else ""}">{T["src"][kind]}</span>'
        if kind == 'p2':
            return f'<div class="mp-item src-p2">{tag}{it_p2[qid]}</div>'
        if kind == 'exm':
            return f'<div class="mp-item src-exm">{tag}{it_exm[qid]}</div>'
        if kind == 'ex':
            return f'<div class="mp-item src-ex">{tag}{it_ex[qid]}</div>'
        return f'<div class="mp-item src-bc" id="bcq-{qid}">{tag}<div class="bcq" data-q="{qid}"></div></div>'

    body, rail, opts = [], [], []
    for page, learnkey, plan, cls in PARTS:
        pid = f'part-{page}'
        body.append(f'<h1 class="mp-part {cls}" id="{pid}">{T["part"][page]}</h1>')
        rail.append(f'<div class="pt">{T["part"][page]}</div><ol>')
        opts.append(f'<optgroup label="{T["part"][page]}">')
        chs = sorted(set(plan) | {c for (p, c) in ex_at if p == page}, key=lambda c: int(c[2:]))
        for ch in chs:
            kind = 'p2' if page == 'p2' else ('exm' if page == 'A' else 'bc')
            prac = plan.get(ch, [])
            exq = ex_at.get((page, ch), [])
            sid = f'{page}-{ch}'
            n = ch[2:]
            title = titles.get((page, ch), ch)
            learn = urls.get('learn', '')
            ll = f'<a href="{learn}#{page}~{ch}" data-learn="1">{T["learn"]}</a>' if learn else ''
            body.append(f'<section class="mp-ch" id="{sid}"><div class="mp-chh"><h2>{T["ch"].format(n=n)} · {title}</h2>'
                        f'<span class="meta">{T["counts"].format(p=len(prac), e=len(exq))}</span>{ll}</div>')
            body += [item(kind, q) for q in prac] + [item('ex', q) for q in exq]
            body.append('</section>')
            short = title if len(title) <= 26 else title[:25] + '…'
            rail.append(f'<li><a href="#{sid}"><span class="n">{T["ch"].format(n=n)}</span> {short}</a></li>')
            opts.append(f'<option value="{sid}">{T["ch"].format(n=n)} · {short}</option>')
        # extras at the end of each part
        extra = []
        if page == 'p2':
            extra.append(('p2-drill', T['drill'], f'<section class="mp-ch" id="p2-drill"><div class="mp-chh"><h2>{T["drill"]}</h2></div><div class="mp-item src-p2">{drill}</div></section>'))
            extra.append(('hwsw', T['sw'], f'<details class="mp-embed" id="hwsw" data-page="hwsw"><summary>{T["sw"]}</summary></details>'))
        if page == 'A':
            extra.append(('exm-sheet', T['sheet'], f'<section class="mp-ch" id="exm-sheet"><div class="mp-chh"><h2>{T["sheet"]}</h2></div><div class="mp-item src-exm">{sheet}</div></section>'))
            extra.append(('hw1', T['hw1'], f'<details class="mp-embed" id="hw1" data-page="hw1"><summary>{T["hw1"]}</summary></details>'))
        if page == 'C':
            extra.append(('bc-quiz', T['quiz'], f'<section class="mp-ch" id="bc-quiz"><div class="mp-chh"><h2>{T["quiz"]}</h2></div><div class="mp-item src-bc">{quiz}<span id="stat" hidden></span>{xplt}</div></section>'))
        for sid, label, html in extra:
            body.append(html)
            rail.append(f'<li><a href="#{sid}">{label}</a></li>')
            opts.append(f'<option value="{sid}">{label}</option>')
        rail.append('</ol>')
        opts.append('</optgroup>')

    # everything placed exactly once?
    miss = {'p2': set(it_p2) - used['p2'], 'exm': set(it_exm) - used['exm'], 'ex': set(it_ex) - used['ex'], 'bc': set(bcQ) - used['bc']}
    assert not any(miss.values()), miss

    # scoped CSS of every source page
    css = [scope_css(styles(pages[k]), '.' + S) for k, S in SRC.items()]
    head_links = []
    for k in SRC:
        for l in links(pages[k]):
            if l not in head_links:
                head_links.append(l)
    # scripts: MathJax (Part 2), the p2 drill, the B·C quiz/cards
    mj_cfg = re.search(r'<script>\s*(window\.MathJax\s*=.*?)</script>', p2, re.S)
    mj_src = re.findall(r'<script[^>]*src="[^"]*mathjax[^"]*"[^>]*></script>', p2)
    p2js = [x for x in re.findall(r'<script>(.*?)</script>', p2, re.S) if 'drill generators' in x][0]
    i = p2js.index('/* ---------- math helpers'); j = p2js.rindex('})();')
    drill_js = ('(function(){\n var store={get:function(k){try{return localStorage.getItem(k);}catch(e){return null;}},'
                'set:function(k,v){try{localStorage.setItem(k,v);}catch(e){}}};\n' + p2js[i:j] + '})();')
    bcjs = [x for x in re.findall(r'<script>(.*?)</script>', bc, re.S) if 'var Q=' in x][0]
    a = bcjs.index('  // bank'); b = bcjs.index('  // quiz')
    bcjs = (bcjs[:a] + "  document.querySelectorAll('.bcq[data-q]').forEach(function(ph){ var q=Q.filter(function(x){return x.id===ph.dataset.q;})[0];"
            " if(q) ph.appendChild(card(q,function(ok){ if(ok){ store.set('ee6129-bc:'+q.id,'1'); stat(); } })); });\n  stat();\n" + bcjs[b:])

    route = route_table()
    legacy = {'guide': 'mp-top', 'exams': 'ex-overview', 'p2prac': 'part-p2', 'Aex': 'part-A', 'bc': 'part-B',
              'hw1': 'hw1', 'hwsw': 'hwsw', 'overview': 'ex-overview', 'sheet': 'exm-sheet', 'drill': 'p2-drill', 'quiz': 'bc-quiz'}
    embedp = {'hw1': strip_skeleton(pages['hw1']), 'hwsw': strip_skeleton(pages['homework-sw'])}
    data = (f'var ROUTE={json.dumps(route)};\nvar LEGACY={json.dumps(legacy)};\nvar LEARN={json.dumps(urls.get("learn", ""))};\n'
            'var EMBED={' + ','.join(f'"{k}":{embed(v)}' for k, v in embedp.items()) + '};\n')

    lang_seg = ('' if lang == 'en' else
                f'<span class="mp-seg" id="mpLang"><span>{T["sol"]}</span><button type="button" data-lang="en" aria-pressed="true">EN</button>'
                f'<button type="button" data-lang="zh" aria-pressed="false">中文</button></span>')
    sw = ''
    if urls.get('to_learn'):
        sw += f'<a class="mp-switch" href="{urls["to_learn"]}">{T["to_learn"]}</a>'
    if urls.get('other'):
        sw += f'<a class="mp-switch" href="{urls["other"]}">{T["other"]}</a>'
    extra_head = ''
    extra_tail = ''
    if lang == 'en':
        import sys
        sys.path.insert(0, str(REPO / 'src' / 'en'))
        from build_en import BI_CSS, BI_JS
        extra_head, extra_tail = BI_CSS, BI_JS
    overview_html = (f'<details class="mp-embed" id="ex-overview-wrap"><summary>{T["overview"]}</summary>'
                     f'<div class="mp-item src-ex" style="padding:0 16px 12px">{overview}</div></details>')
    html = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            f'<title>{T["title"]}</title>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">\n'
            + '\n'.join(head_links) + '\n'
            + f'<style>{CSS}</style>\n<style>\n' + '\n'.join(css) + '\n</style>\n' + extra_head
            + (f'<script>{mj_cfg.group(1)}</script>\n' if mj_cfg else '') + '\n'.join(mj_src) + '\n'
            + f'<header class="mp-top" id="mp-top"><div class="mp-row"><div class="mp-brand">EE6129 · <b>{T["brand"]}</b></div>'
            f'<label class="mp-tg"><input type="checkbox" id="mpExam"> {T["exam"]}</label>'
            f'<label class="mp-tg"><input type="checkbox" id="mpZh" checked> {T["zhq"]}</label>{lang_seg}'
            f'<span class="mp-count" id="mpCount" data-l="{T["mastered"]}"></span><span class="mp-sp"></span>{sw}'
            f'<select class="mp-jump" id="mpJump" aria-label="{T["toc"]}">{"".join(opts)}</select></div></header>\n'
            f'<div class="mp-layout"><nav class="mp-rail" aria-label="{T["toc"]}">{"".join(rail)}</nav>\n'
            f'<main class="mp-main"><div class="mp-intro">{INTRO[lang]}</div>{overview_html}\n' + '\n'.join(body) + '</main></div>\n'
            + f'<script>\n{data}</script>\n<script>{bcjs}</script>\n<script>{drill_js}</script>\n<script>{JS}</script>\n' + extra_tail)
    if lang == 'en':
        html = html.replace('<span class="mp-tag', '<span class="mp-tag', 1)
    out.write_text(html, encoding='utf-8')
    n = {k: len(v) for k, v in used.items()}
    print(out.name, f'{out.stat().st_size / 1e6:.2f} MB', 'items:', n)


def load_pages(lang):
    d = ART / 'en' if lang == 'en' else ART
    hwsw = (d / 'homework-sw.html') if lang == 'en' else pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_HW_SW/homework_sw.html')
    return {'exams': (d / 'exams.html').read_text(encoding='utf-8'),
            'p2-practice': (d / 'p2-practice.html').read_text(encoding='utf-8'),
            'examples': (d / 'examples.html').read_text(encoding='utf-8'),
            'hw1': (d / 'hw1.html').read_text(encoding='utf-8'),
            'bc-practice': (d / 'bc-practice.html').read_text(encoding='utf-8'),
            'homework-sw': hwsw.read_text(encoding='utf-8')}


if __name__ == '__main__':
    import sys
    lang = sys.argv[1] if len(sys.argv) > 1 else 'zh'
    learn = art_url('hub-learn-en' if lang == 'en' else 'hub-learn')
    urls = {'learn': learn, 'to_learn': learn,
            'other': art_url('hub-practice' if lang == 'en' else 'hub-practice-en')}
    build(load_pages(lang), lang, ART / ('hub-practice-en.html' if lang == 'en' else 'hub-practice.html'), urls)
