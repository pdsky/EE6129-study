#!/usr/bin/python3
"""Build the bilingual practice hub 「EE6129 Practice (EN + 中文)」.

The Chinese practice pages (EE6129_artifacts/*.html + the SW homework page) are taken as built and prepared by
prep.py (parts that already have an English twin are kept Chinese as they are, e.g. p2-practice question lines and
中文 solutions). Every other Chinese unit found by segments.py is replaced from tr/dict.json (Chinese unit → English);
units of real text (≥ BI_MIN Chinese characters, not headings/buttons/labels) get the Chinese original right under
the English (span.zhsub). A small 中文 button on every page hides/shows all Chinese.

usage:
  build_en.py merge          fold batches/out_N.json (agent translations of batches/in_N.json) into tr/dict.json
  build_en.py missing        write batches/missing.json with the units that have no translation yet
  build_en.py                build EE6129_artifacts/en/*.html and EE6129_artifacts/hub-practice-en.html
Run after the Chinese pages and build_hub.py. When a Chinese page changes, run `missing`, translate the new units,
`merge`, then build and republish hub-practice-en.html by URL (artifact id in src/artifact_ids.json "hub-practice-en").
"""
import json, pathlib, re, sys

E = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(E)); sys.path.insert(0, str(E.parent / 'hub'))
import segments, prep  # noqa: E402

ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')
OUT = ART / 'en'
DICT = E / 'tr' / 'dict.json'
PAGES = {
    'exams': ART / 'exams.html',
    'p2-practice': ART / 'p2-practice.html',
    'examples': ART / 'examples.html',
    'hw1': ART / 'hw1.html',
    'bc-practice': ART / 'bc-practice.html',
    'homework-sw': pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_HW_SW/homework_sw.html'),
    'p2-learn': ART / 'p2-learn.html',
    'quiz-summary': ART / 'quiz-summary.html',
    'partA': ART / 'partA.html',
    'partB': ART / 'partB.html',
    'partC': ART / 'partC.html',
}
LEARN = {'p2-learn', 'quiz-summary', 'partA', 'partB', 'partC'}


def load_dict():
    d = json.loads(DICT.read_text(encoding='utf-8')) if DICT.exists() else {}
    if 'OVERRIDE' in globals():
        d.update(OVERRIDE)
        for pre, old, new in OVERRIDE_SUB:
            hit = 0
            for k in d:
                if k.startswith(pre) and old in d[k]:
                    d[k] = d[k].replace(old, new); hit += 1
            assert hit, (pre, old)
    return d


def save_dict(d):
    d = {k: v for k, v in d.items() if k not in OVERRIDE}
    DICT.parent.mkdir(exist_ok=True)
    DICT.write_text(json.dumps(d, ensure_ascii=False, indent=0, sort_keys=True), encoding='utf-8')


def merge():
    d = load_dict(); n = 0
    for fin in sorted((E / 'batches').glob('in_*.json')) + sorted((E / 'batches' / 'learn').glob('in_*.json')):
        fout = fin.with_name(fin.name.replace('in_', 'out_'))
        if not fout.exists():
            print('no output yet:', fout.name); continue
        src = json.loads(fin.read_text(encoding='utf-8')); tr = json.loads(fout.read_text(encoding='utf-8'))
        for it in src:
            en = tr.get(str(it['id']))
            if en is None:
                print('missing', fout.name, it['id']); continue
            d[it['zh']] = en; n += 1
    save_dict(d); print('merged', n, '→', len(d), 'entries')


def page_text(name):
    return prep.prep(name, PAGES[name].read_text(encoding='utf-8'))[0]


def missing():
    d = load_dict(); items = []; seen = set()
    srcs = [(n, page_text(n)) for n in PAGES] + [('learn-guide', H.GUIDE_LEARN)]
    for name, text in srcs:
        for k, kind in segments.units(text).items():
            if k not in d and k not in seen:
                seen.add(k); items.append({'id': len(items), 'page': name, 'kind': kind, 'zh': k})
    (E / 'batches').mkdir(exist_ok=True)
    (E / 'batches' / 'missing.json').write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding='utf-8')
    print(len(items), 'untranslated units → batches/missing.json')


# wording that must differ from the plain translation because the English hub drops the Chinese twins (see prep.py)
OVERRIDE = {}
OVERRIDE_SUB = [  # (zh unit prefix, old English, new English)
    ('讲义配套的 7 份', 'Solutions are in English by default (you must answer the exam in English); you can switch to Chinese at any time. ',
     'Each solution is given in English first (the exam is answered in English), then in Chinese. '),
]


CSS_LABELS = {'补充\u3000': 'Beyond the notes\u2003', '记忆\u3000': 'Memory aid\u2003', '易错\u3000': 'Watch out\u2003',
              '核对\u3000': 'Check\u2003', '中文题意': 'In plain words · 中文题意'}


BI_MIN = 6   # a unit with at least this many Chinese characters is real text → show the Chinese under it
BI_SKIP_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'button', 'summary', 'label', 'option', 'title', 'th', 'nav',
                'select', 'a', 'text', 'dt'}
BI_SKIP_CLASS = {'chip', 'chips', 'lbl', 'pg', 'badge', 'tab', 'tabs', 'eyebrow', 'orig-lab', 'qref', 'seg-lab', 'jump',
                 'st', 'qhead', 'filters', 'ov'}
HAN = re.compile(r'[\u4e00-\u9fff]')
INL = re.compile(r'<(/?)([a-zA-Z][\w-]*)[^>]*?(/?)>')

BI_CSS = """<style>
.zhsub{display:block;margin:.3em 0 .1em;padding-left:.7em;border-left:2px solid rgba(127,127,127,.45);opacity:.8;font-size:.93em;font-weight:400;font-family:'Noto Sans CJK SC','PingFang SC','Microsoft YaHei',sans-serif}
button .zhsub{display:block;border:0;padding:0;margin-top:.15em}
.sol-en::before,.sol-zh::before{display:block;font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.08em;opacity:.7;margin-bottom:4px}
.sol-en::before{content:'ENGLISH'} .sol-zh::before{content:'中文解答'}
.sol-zh{border-top:1px dashed rgba(127,127,127,.5);margin-top:12px;padding-top:10px;font-family:'Noto Sans CJK SC','PingFang SC','Microsoft YaHei',sans-serif}
body.hide-zh .zhsub,body.hide-zh .orig p.zh,body.hide-zh .orig .zh-th,body.hide-zh .sol-zh{display:none!important}
#zhToggle{position:fixed;right:14px;bottom:14px;z-index:50;font:600 .8rem/1 'IBM Plex Sans','Noto Sans CJK SC',sans-serif;border:1px solid rgba(127,127,127,.5);border-radius:999px;padding:8px 13px;background:rgba(255,255,255,.92);color:#123;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.15)}
@media (prefers-color-scheme: dark){#zhToggle{background:rgba(20,32,30,.92);color:#e6f0ed}}
</style>
"""
BI_JS = """<button type="button" id="zhToggle" aria-pressed="true" title="Show / hide Chinese">中文 ✓</button>
<script>(function(){var b=document.getElementById('zhToggle'),k='ee6129-en:zh';
function set(on){document.body.classList.toggle('hide-zh',!on);b.setAttribute('aria-pressed',String(on));b.textContent=on?'中文 ✓':'中文 ✗';try{localStorage.setItem(k,on?'1':'0');}catch(e){}}
var v='1';try{v=localStorage.getItem(k)||'1';}catch(e){} set(v!=='0');
b.addEventListener('click',function(){set(document.body.classList.contains('hide-zh'));});})();</script>
"""


def balanced(frag):
    st = []
    for m in INL.finditer(frag):
        close, name, selfc = m.group(1), m.group(2).lower(), m.group(3)
        if selfc or name in ('br', 'wbr', 'img'):
            continue
        if close:
            if not st or st.pop() != name:
                return False
        else:
            st.append(name)
    return not st


STEPS_OPEN = re.compile(r'\bsteps\s*:\s*\[')


def js_shown_as_html(ctx):
    """Animation figure strings that core.js puts in with innerHTML: a whole caption (cap: '…') or a whole step text."""
    if not ctx or ctx[0] != 'script':
        return False
    before, nxt = ctx[1].rstrip(), ctx[2]
    if nxt not in (',', ']', '}', ')', ''):
        return False                      # part of a concatenation
    if re.search(r'\bcap\s*:\s*$', before):
        return True
    m = None
    for m in STEPS_OPEN.finditer(before):
        pass
    if m and before[-1:] in ('[', ','):
        tail = before[m.end():]
        return tail.count('[') >= tail.count(']')
    return False


def bilingual(kind, txt, ctx, page):
    if len(HAN.findall(txt)) < BI_MIN:
        return False
    if kind == 'js':
        return page == 'bc-practice' or (page in LEARN and js_shown_as_html(ctx))
    if kind != 'html' or not balanced(txt):
        return False
    if ctx:
        tag, cls = ctx
        if tag in BI_SKIP_TAGS or set(cls.split()) & BI_SKIP_CLASS:
            return False
    return True


def translate(name, d, text=None):
    s, keeps = prep.prep(name, PAGES[name].read_text(encoding='utf-8') if text is None else text); miss = []
    def fn(kind, txt):
        if txt not in d:
            miss.append(txt); return txt
        en = d[txt]
        if bilingual(kind, txt, segments.CTX, name):
            return en + '<span class="zhsub" lang="zh-CN">' + txt + '</span>'
        return en
    s = segments.walk(s, fn)
    for zh, en in CSS_LABELS.items():   # labels drawn by CSS ::before
        s = s.replace(f"content:'{zh}'", f"content:'{en}'")
    s = s.replace('lang="zh-CN"', 'lang="en"').replace('\u3000', '\u2003')
    s = s.replace('<span class="zhsub" lang="en">', '<span class="zhsub" lang="zh-CN">')
    s = prep.restore(s, keeps)
    if name not in ('homework-sw', 'learn-guide'):   # bilingual already / part of the hub page
        s = BI_CSS + s + BI_JS
    return s, miss


# ---------------- hubs ----------------
import build_hub as H  # noqa: E402

HUBS = {
    'practice': {
        'id': 'hub-practice-en', 'out': 'hub-practice-en.html', 'title': 'EE6129 Practice (EN + 中文)', 'brand': 'Practice',
        'tabs': [
            ('guide', 'How to practise', 'Guide', None),
            ('exams', 'Past final exams', 'Exams', 'exams'),
            ('p2prac', 'Part 2 · Practice 1–7 + mock questions', 'Part 2', 'p2-practice'),
            ('Aex', 'Part A · Lecture examples', 'Part A', 'examples'),
            ('hw1', 'Part 1 · HW1', 'HW1', 'hw1'),
            ('bc', 'Part B · C quizzes', 'B·C', 'bc-practice'),
            ('hwsw', 'Part 2 · Homework (SW)', 'HW (SW)', 'homework-sw'),
        ]},
    'learn': {
        'id': 'hub-learn-en', 'out': 'hub-learn-en.html', 'title': 'EE6129 Learn (EN + 中文)', 'brand': 'Learn',
        'tabs': [
            ('guide', 'Exam guide', 'Guide', None),
            ('p2', 'Part 2 · Channel to OFDM', 'Part 2', 'p2-learn'),
            ('ch12', 'Ch. 1b–2 problem types', '1b–2 types', 'quiz-summary'),
            ('A', 'Part A · Cellular networks', 'Part A', 'partA'),
            ('B', 'Part B · Wireless systems', 'Part B', 'partB'),
            ('C', 'Part C · Satellite communications', 'Part C', 'partC'),
        ]},
}


def en_url(hub):
    return H.art_url(HUBS[hub]['id'])


def tl(tab, text):
    return f'<a href="#{tab}" data-tab="{tab}">{text}</a>'


def guide_practice(zh_url, learn_url):
    zh = f'<a href="{zh_url}">Chinese version</a>' if zh_url else 'the Chinese practice hub'
    learn = f'<a href="{learn_url}">learning hub (EN + 中文)</a>' if learn_url else 'the learning hub'
    return f'''
<div class="guide">
  <h1>EE6129 final revision · Practice (EN + 中文)</h1>
  <p class="lede">Bilingual edition of the practice hub: the same questions, worked solutions, key-point boxes and lecturer notes as {zh}. Every question and answer is in English with the Chinese right under it, so you can practise writing answers in English and still check the meaning. The <b>中文 ✓</b> button at the bottom right of each page hides or shows all Chinese (hide it to test your English). Work in this order: past final exams first, then the seven Part 2 practice sheets (the lecturer said final questions come from the practices and lecture examples, often as variations), then the Part A examples and HW1, and finally the Part B·C concept questions.</p>
  <p class="lede">中英对照版：题目和答案都是英文在上、中文在下；每页右下角的「中文 ✓」按钮可以一键隐藏 / 显示全部中文（隐藏后可以检验自己的英文）。做题顺序：先做历年真题，再做 Part 2 的 7 份 Practice（老师说期末题出自 Practice 和讲义例题的变形），然后是 Part A 例题和 HW1，最后是 Part B·C 概念题。</p>

  <div class="cards">
    <a class="card" href="#exams" data-tab="exams"><div class="t">Past final exams</div><div class="d">Four papers, 2023-24 S2 to 2025-26 S2, 16 questions: original text, step-by-step solutions and the pattern of what is asked</div></a>
    <a class="card" href="#p2prac" data-tab="p2prac"><div class="t">Part 2 · Practice 1–7 + mock questions</div><div class="d">21 practice questions solved in detail and checked against the official answers, 12 mock questions on Ch. 1b–2, and a random drill</div></a>
    <a class="card" href="#Aex" data-tab="Aex"><div class="t">Part A · Lecture examples</div><div class="d">15 examples on Erlang B/C, frequency reuse, SIR and cell splitting, with a self-test mode</div></a>
    <a class="card" href="#hw1" data-tab="hw1"><div class="t">Part 1 · HW1</div><div class="d">Explanations and model answers for the three Part A homework questions; two of its parts reappear word for word in past exams</div></a>
    <a class="card" href="#bc" data-tab="bc"><div class="t">Part B · C quizzes</div><div class="d">62 multiple-choice, calculation and short-answer questions on WLAN, ad hoc and sensor networks, LTE, IoT and satellites</div></a>
    <a class="card" href="#hwsw" data-tab="hwsw"><div class="t">Part 2 · Homework (SW)</div><div class="d">MRC output SNR, two transmit antennas vs SISO, and the 4G→5G essay: questions and answers</div></a>
  </div>

  <h2>What to practise for each exam question</h2>
  <div class="tw"><table>
    <thead><tr><th>Exam question</th><th>Do first</th><th>Then</th></tr></thead>
    <tbody>
      <tr><td class="q">Q1 <span class="tag p2">Part 2</span></td><td>Q1 of all four {tl('exams', 'past papers')}</td><td>{tl('p2prac', 'Practice 1–5')} (channel, detection, diversity, MIMO) + the Ch. 1b–2 mock questions</td></tr>
      <tr><td class="q">Q2 <span class="tag p2">Part 2</span></td><td>Q2 of all four {tl('exams', 'past papers')}</td><td>{tl('p2prac', 'Practice 6–7')} (equalisation, OFDM)</td></tr>
      <tr><td class="q">Q3 <span class="tag pa">Part A</span></td><td>Q3 of all four {tl('exams', 'past papers')}</td><td>{tl('Aex', 'Part A examples')}, {tl('hw1', 'HW1')}</td></tr>
      <tr><td class="q">Q4 <span class="tag pa">Part A</span></td><td>Q4 of all four {tl('exams', 'past papers')}</td><td>The short-answer questions in {tl('bc', 'Part B·C quizzes')}</td></tr>
    </tbody>
  </table></div>
  <div class="note">Cover the solution and work the question yourself first. Each question has a "Key points" box and, where the lecturer commented on it, a "Lecturer's emphasis in class" box; read them after checking your answer. Links to the notes open the {learn}.</div>
</div>
'''


def guide_learn(d, miss):
    """The Chinese learn-hub guide (exam facts + exam map), translated with Chinese under each text unit."""
    s, m = translate('learn-guide', d, H.GUIDE_LEARN)
    miss.extend(m)
    zh_url = H.HUB_URL.get('learn', '')
    note = ('<p class="lede">Bilingual edition of the learning hub: every paragraph is in English with the Chinese right '
            'under it; the <b>中文 ✓</b> button at the bottom right of each page hides or shows all Chinese. '
            + (f'<a href="{zh_url}">Chinese version</a>.' if zh_url else '') + '</p>'
            '<p class="lede">中英对照版：每段英文下面是对应的中文；每页右下角的「中文 ✓」按钮可以一键隐藏 / 显示全部中文。</p>')
    i = s.find('</h1>')
    return s[:i + 5] + note + s[i + 5:] if i > 0 else note + s


def build_hub(hub, pages, guide_html):
    cfg = HUBS[hub]; other = 'learn' if hub == 'practice' else 'practice'
    hub_url = {'learn': en_url('learn') or H.HUB_URL['learn'], 'practice': en_url('practice') or H.HUB_URL['practice']}
    route = {}
    for h, c in HUBS.items():
        for tid, _l, _s, key in c['tabs']:
            if key:
                v = H.IDS.get(key, {})
                for k in ('new', 'old'):
                    if v.get(k):
                        route[v[k]] = [h, tid]
                route[pathlib.Path(v.get('file', key + '.html')).name] = [h, tid]
    js = H.JS.replace('lang="zh-CN"', 'lang="en"').replace('正在载入…', 'Loading…')
    buttons = ''.join(
        f'<button type="button" role="tab" data-tab="{tid}" data-label="{label}" aria-selected="false">'
        f'<span class="long">{label}</span><span class="short">{short}</span></button>'
        for tid, label, short, _k in cfg['tabs'])
    zh_url = H.HUB_URL.get(hub, '')
    switch = ((f'<a class="switch" href="{hub_url[other]}">{"Practice →" if hub == "learn" else "← Learn"}</a>') +
              (f'<a class="switch" href="{zh_url}">中文版</a>' if zh_url else ''))
    data = (f'document.body.dataset.hub = "{hub}";\n'
            'var PAGES = {' + ','.join(f'"{k}":{H.embed(H.strip_skeleton(v))}' for k, v in pages.items()) + '};\n'
            f'var ROUTE = {json.dumps(route)};\nvar HUBURL = {json.dumps(hub_url)};\n')
    html = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            f'<title>{cfg["title"]}</title>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">\n'
            f'<style>{H.CSS}\n.guide .zhsub{{display:block;margin:.25em 0 .1em;padding-left:.7em;border-left:2px solid rgba(127,127,127,.45);opacity:.8;font-size:.93em;font-weight:400}}</style>\n'
            f'<header class="top"><div class="row"><div class="brand">EE6129 · <b>{cfg["brand"]}</b> EN + 中文</div>'
            f'<span class="sp"></span>{switch}</div>\n'
            f'<nav class="tabs" role="tablist" aria-label="{cfg["title"]}">{buttons}</nav></header>\n'
            f'<main id="stage"><section class="pane" id="guide">{guide_html}</section></main>\n'
            f'<script>\n{data}</script>\n<script>{js}</script>\n')
    out = ART / cfg['out']
    out.write_text(html, encoding='utf-8')
    print(out.name, f'{out.stat().st_size / 1e6:.2f} MB')


def build(which=('practice', 'learn')):
    d = load_dict(); OUT.mkdir(exist_ok=True); bad = 0
    for hub in which:
        pages = {}
        for tid, _l, _s, key in HUBS[hub]['tabs']:
            if not key:
                continue
            s, miss = translate(key, d)
            (OUT / f'{key}.html').write_text(s, encoding='utf-8')
            pages[tid] = s
            print(f'{key:12s} untranslated units: {len(miss):4d}')
            bad += len(miss)
        if hub == 'practice':
            g = guide_practice(H.HUB_URL.get('practice', ''), en_url('learn') or H.HUB_URL.get('learn'))
        else:
            gm = []; g = guide_learn(d, gm); bad += len(gm)
            print(f'{"learn-guide":12s} untranslated units: {len(gm):4d}')
        build_hub(hub, pages, g)
    if bad:
        print('WARNING: run `build_en.py missing` and translate the rest')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'build'
    if cmd == 'build' and len(sys.argv) > 2:
        build(tuple(sys.argv[2:]))
    else:
        {'merge': merge, 'missing': missing, 'build': build}[cmd]()
