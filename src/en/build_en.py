#!/usr/bin/python3
"""Build the English practice hub 「EE6129 Practice (English)」.

The Chinese practice pages (EE6129_artifacts/*.html + the SW homework page) are taken as built, cleaned by prep.py
(p2-practice drops its Chinese copies, which already have English twins), and every Chinese unit found by
segments.py is replaced from the dictionary tr/dict.json (Chinese unit → English).

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
}


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
    for fin in sorted((E / 'batches').glob('in_*.json')):
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
    return prep.prep(name, PAGES[name].read_text(encoding='utf-8'))


def missing():
    d = load_dict(); items = []; seen = set()
    for name in PAGES:
        for k, kind in segments.units(page_text(name)).items():
            if k not in d and k not in seen:
                seen.add(k); items.append({'id': len(items), 'page': name, 'kind': kind, 'zh': k})
    (E / 'batches').mkdir(exist_ok=True)
    (E / 'batches' / 'missing.json').write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding='utf-8')
    print(len(items), 'untranslated units → batches/missing.json')


# wording that must differ from the plain translation because the English hub drops the Chinese twins (see prep.py)
OVERRIDE = {
    '中文答案': 'Explanation',
    '3 道大题、14 个小问。「讲解」按题拆考点和思路，配图和计算器；「中文答案」和「English answers」是两份完整的参考答案，内容一致。所有 Erlang 值都用课件 Erlang B 表查得，并用公式复核过。':
        '3 questions, 14 sub-parts. The "Walkthrough" tab breaks each question into key points and an approach, with figures and calculators; "English answers" is the complete model answer. All Erlang values are read from the Erlang B table in the slides and checked with the formula.',
}
OVERRIDE_SUB = [  # (zh unit prefix, old English, new English)
    ('每题先给题目原文', 'Each question gives the original text and a Chinese translation, then an English answer (for submission) and a Chinese answer (for understanding).',
     'Each question gives the original text and a plain-language restatement, then the English answer (for submission) and an explanation (for understanding).'),
    ('<span>Original question · 中英对照', 'Original question · bilingual', 'Original question'),
    ('<span>Original question · 中英对照', 'Original question · Chinese and English', 'Original question'),
    ('讲义配套的 7 份', 'the original question in Chinese and English,', 'the original question,'),
    ('讲义配套的 7 份', 'Solutions are in English by default (you must answer the exam in English); you can switch to Chinese at any time. ', ''),
]


CSS_LABELS = {'补充\u3000': 'Beyond the notes\u2003', '记忆\u3000': 'Memory aid\u2003', '易错\u3000': 'Watch out\u2003',
              '核对\u3000': 'Check\u2003', '中文题意': 'In plain words'}


def translate(name, d):
    s = page_text(name); miss = []
    def fn(kind, txt):
        if txt in d:
            return d[txt]
        miss.append(txt); return txt
    s = segments.walk(s, fn)
    for zh, en in CSS_LABELS.items():   # labels drawn by CSS ::before
        s = s.replace(f"content:'{zh}'", f"content:'{en}'")
    s = s.replace('lang="zh-CN"', 'lang="en"').replace('\u3000', '\u2003')
    return s, miss


# ---------------- hub ----------------
import build_hub as H  # noqa: E402

TABS = [
    ('guide', 'How to practise', 'Guide', None),
    ('exams', 'Past final exams', 'Exams', 'exams'),
    ('p2prac', 'Part 2 · Practice 1–7 + mock questions', 'Part 2', 'p2-practice'),
    ('Aex', 'Part A · Lecture examples', 'Part A', 'examples'),
    ('hw1', 'Part 1 · HW1', 'HW1', 'hw1'),
    ('bc', 'Part B · C quizzes', 'B·C', 'bc-practice'),
    ('hwsw', 'Part 2 · Homework (SW)', 'HW (SW)', 'homework-sw'),
]


def tl(tab, text):
    return f'<a href="#{tab}" data-tab="{tab}">{text}</a>'


def guide(zh_url, learn_url):
    zh = f'<a href="{zh_url}">Chinese version</a>' if zh_url else 'the Chinese practice hub'
    learn = f'<a href="{learn_url}">EE6129 学习</a>' if learn_url else 'the learning hub'
    return f'''
<div class="guide">
  <h1>EE6129 final revision · Practice (English)</h1>
  <p class="lede">English edition of the practice hub: the same questions, worked solutions, key-point boxes and lecturer notes as {zh}, translated so you can practise writing answers in English. Work in this order: past final exams first, then the seven Part 2 practice sheets (the lecturer said final questions come from the practices and lecture examples, often as variations), then the Part A examples and HW1, and finally the Part B·C concept questions.</p>

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
  <div class="note">Cover the solution and work the question yourself first. Each question has a "Key points" box and, where the lecturer commented on it, a "Lecturer's emphasis in class" box; read them after checking your answer. Links to the learning pages open {learn}, which is in Chinese.</div>
</div>
'''


def build_hub(pages):
    hub_url = dict(H.HUB_URL)
    route = {}
    for tid, _l, _s, key in TABS:
        if key:
            v = H.IDS.get(key, {})
            for k in ('new', 'old'):
                if v.get(k):
                    route[v[k]] = ['practice', tid]
            route[pathlib.Path(v.get('file', key + '.html')).name] = ['practice', tid]
    for k, v in H.ROUTE.items():          # learn pages → the (Chinese) learn hub
        if v[0] == 'learn':
            route[k] = v
    js = (H.JS.replace('lang="zh-CN"', 'lang="en"').replace('正在载入…', 'Loading…'))
    buttons = ''.join(
        f'<button type="button" role="tab" data-tab="{tid}" data-label="{label}" aria-selected="false">'
        f'<span class="long">{label}</span><span class="short">{short}</span></button>'
        for tid, label, short, _k in TABS)
    zh_url = hub_url.get('practice', '')
    switch = ((f'<a class="switch" href="{hub_url["learn"]}">Learning pages (Chinese)</a>' if hub_url.get('learn') else '') +
              (f'<a class="switch" href="{zh_url}">中文版</a>' if zh_url else ''))
    data = ('document.body.dataset.hub = "practice";\n'
            'var PAGES = {' + ','.join(f'"{k}":{H.embed(H.strip_skeleton(v))}' for k, v in pages.items()) + '};\n'
            f'var ROUTE = {json.dumps(route)};\nvar HUBURL = {json.dumps(hub_url)};\n')
    html = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<title>EE6129 Practice (English)</title>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">\n'
            f'<style>{H.CSS}</style>\n'
            '<header class="top"><div class="row"><div class="brand">EE6129 · <b>Practice</b> (English)</div>'
            f'<span class="sp"></span>{switch}</div>\n'
            f'<nav class="tabs" role="tablist" aria-label="EE6129 Practice">{buttons}</nav></header>\n'
            f'<main id="stage"><section class="pane" id="guide">{guide(zh_url, hub_url.get("learn"))}</section></main>\n'
            f'<script>\n{data}</script>\n<script>{js}</script>\n')
    out = ART / 'hub-practice-en.html'
    out.write_text(html, encoding='utf-8')
    print(out.name, f'{out.stat().st_size / 1e6:.2f} MB')


def build():
    d = load_dict(); OUT.mkdir(exist_ok=True); pages = {}; bad = 0
    for tid, _l, _s, key in TABS:
        if not key:
            continue
        s, miss = translate(key, d)
        left = segments.visible_cjk(s)
        left = [t for t in left if t.strip() != '中文']
        (OUT / f'{key}.html').write_text(s, encoding='utf-8')
        pages[tid] = s
        print(f'{key:12s} untranslated units: {len(miss):4d}   Chinese left: {len(left)}')
        bad += len(miss)
    if bad:
        print('WARNING: run `build_en.py missing` and translate the rest')
    build_hub(pages)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'build'
    {'merge': merge, 'missing': missing, 'build': build}[cmd]()
