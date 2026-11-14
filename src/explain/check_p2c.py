#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Check src/explain/p2c.py: structure, allowed HTML, TeX rules, zh/en parity, and every number.
Run:  /usr/bin/python3 src/explain/check_p2c.py"""
import importlib.util, os, re, sys
from html.parser import HTMLParser
from math import log10, log2, log, sqrt, exp, erfc, pi
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('p2c', os.path.join(HERE, 'p2c.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
XPL, NOTES = m.XPL, m.NOTES
IDS = ['p8q1', 'p8q7', 'p8q8', 'p8q9', 'p8q10', 'p8q11']
err = []
def bad(msg): err.append(msg)

# ---------------------------------------------------------------- 1. ids / keys / required words
for i in IDS:
    if i not in XPL: bad(f'{i}: missing'); continue
    e = XPL[i]
    for k in ('title', 'title_en', 'zh', 'en'):
        if not e.get(k): bad(f'{i}: key {k} missing')
    if '知识讲解' not in e['zh'] or '一句话' not in e['zh']: bad(f'{i}: zh lacks 知识讲解 / 一句话')
    if 'Concept' not in e['en'] or 'In one line' not in e['en']: bad(f'{i}: en lacks Concept / In one line')
    if not e['title'].startswith('知识讲解 + 详细解析：'): bad(f'{i}: title prefix')
    if len(e['title'].split('：', 1)[1]) > 30: bad(f'{i}: title too long')
    if re.search(r'[一-鿿]', e['en'] + e['title_en']): bad(f'{i}: Chinese characters in en')
extra = set(XPL) - set(IDS)
if extra: bad(f'unexpected ids {extra}')

# ---------------------------------------------------------------- 2. HTML: allowed tags, balance, nesting
ALLOWED = {'h4', 'span', 'p', 'ul', 'ol', 'li', 'b', 'i', 'sub', 'sup', 'br', 'div', 'table', 'thead', 'tbody', 'tr', 'th', 'td'}
DIVCLS = {'calc', 'tw', 'ans', 'tmpl'}
class P(HTMLParser):
    def __init__(s, tag):
        super().__init__(convert_charrefs=True); s.st = []; s.tag = tag; s.last_h4 = None
    def handle_starttag(s, t, a):
        a = dict(a)
        if t not in ALLOWED: bad(f'{s.tag}: tag <{t}> not allowed')
        if t == 'br': return
        if t == 'span' and a != {'class': 'st'}: bad(f'{s.tag}: span attrs {a}')
        if t == 'span' and (not s.st or s.st[-1][0] != 'h4'): bad(f'{s.tag}: span.st outside h4')
        if t == 'div':
            c = a.get('class')
            if c not in DIVCLS: bad(f'{s.tag}: div class {c}')
            if c == 'tmpl' and a.get('lang') != 'en': bad(f'{s.tag}: tmpl without lang=en')
            if c != 'tmpl' and set(a) != {'class'}: bad(f'{s.tag}: div attrs {a}')
        elif t == 'table':
            if a != {'class': 'mini'} or not s.st or s.st[-1] != ('div', 'tw'): bad(f'{s.tag}: table not mini inside div.tw')
        elif t not in ('span',) and a: bad(f'{s.tag}: attrs on <{t}> {a}')
        if t == 'p' and s.st and s.st[-1][0] == 'p': bad(f'{s.tag}: p inside p')
        if s.st and s.st[-1] == ('div', 'tmpl') and t != 'p': bad(f'{s.tag}: tmpl child <{t}>')
        s.st.append((t, a.get('class')))
        if t == 'h4': s.last_h4 = s.getpos()
    def handle_endtag(s, t):
        if t == 'br': return
        if not s.st or s.st[-1][0] != t: bad(f'{s.tag}: unbalanced </{t}> at {s.getpos()} stack {s.st[-3:]}'); return
        s.st.pop()
    def close(s):
        super().close()
        if s.st: bad(f'{s.tag}: unclosed {s.st}')

def check_h4(tag, body):
    for h in re.findall(r'<h4>(.*?)</h4>', body, flags=re.S):
        if not re.match(r'<span class="st">[^<]+</span>\S', h): bad(f'{tag}: h4 not "span.st + title": {h[:40]}')

for i in IDS:
    for k in ('zh', 'en'):
        b = XPL[i][k]; tag = f'{i}.{k}'
        p = P(tag); p.feed(b); p.close(); check_h4(tag, b)
        bare = re.sub(r'</?(?:%s)(?:\s[^<>]*)?>' % '|'.join(ALLOWED), '', b)
        if '<' in bare or '>' in bare: bad(f'{tag}: raw < or > in text')
        if re.search(r'style=|script|<img|<a\s|\\\[|\$', b): bad(f'{tag}: forbidden content')
        # TeX: inline \( \) only, balanced, no < inside
        opens, closes = b.count('\\('), b.count('\\)')
        if opens != closes: bad(f'{tag}: TeX \\( \\) unbalanced {opens}/{closes}')
        for t in re.findall(r'\\\((.*?)\\\)', b, flags=re.S):
            if '<' in t or '&lt;' in t: bad(f'{tag}: < inside TeX')
        nontex = re.sub(r'\\\(.*?\\\)', '', b, flags=re.S)
        if re.search(r'\\[a-zA-Z]', nontex): bad(f'{tag}: TeX command outside \\( \\)')
    zh, en = XPL[i]['zh'], XPL[i]['en']
    for pat in ('<h4>', 'class="calc"', 'class="mini"', 'class="ans"', 'class="tmpl"', '<li>', '<tr>', '\\('):
        if zh.count(pat) != en.count(pat): bad(f'{i}: zh/en count of {pat} differ {zh.count(pat)}/{en.count(pat)}')
    tz = re.search(r'<div class="tmpl" lang="en">.*?</div>', zh, flags=re.S).group(0)
    te = re.search(r'<div class="tmpl" lang="en">.*?</div>', en, flags=re.S).group(0)
    if tz != te: bad(f'{i}: exam template differs between zh and en')
    # English st labels
    st_en = re.findall(r'<span class="st">([^<]+)</span>', en)
    for s in st_en:
        if re.search(r'[一-鿿]', s): bad(f'{i}: Chinese st label in en')

# ---------------------------------------------------------------- 3. numbers
Q = lambda x: 0.5 * erfc(x / sqrt(2))
Qi = lambda p: NormalDist().inv_cdf(1 - p)
dB = lambda x: 10 * log10(x)
f = lambda v, n: f'{v:.{n}f}'
C = {}   # id -> {token: (computed value, decimals)}
def chk(i, tok, val, n):
    C.setdefault(i, {})[tok] = (val, n)
    if f(val, n) != tok: bad(f'{i}: number {tok} != computed {f(val, n)} ({val})')

# p8q1
Pe = 0.7e-4 + 0.3e-2
chk('p8q1', '3.07', Pe * 1e3, 2); chk('p8q1', '0.00307', Pe, 5)
chk('p8q1', '0.977', 0.3e-2 / Pe, 3); chk('p8q1', '0.023', 0.7e-4 / Pe, 3)
chk('p8q1', '0.298', 0.3 * 0.99 / (1 - Pe), 3)
Eg = 0.7 * 10 + 0.3 * 1; Eg2 = 0.7 * 100 + 0.3 * 1
chk('p8q1', '7.3', Eg, 1); chk('p8q1', '70.3', Eg2, 1); chk('p8q1', '53.29', Eg ** 2, 2)
chk('p8q1', '17.01', Eg2 - Eg ** 2, 2); chk('p8q1', '4.12', sqrt(Eg2 - Eg ** 2), 2)
chk('p8q1', '0.8633', log10(7.3), 4); chk('p8q1', '8.63', dB(7.3), 2)
chk('p8q1', '7.29', (10 - 7.3) ** 2, 2); chk('p8q1', '39.69', (1 - 7.3) ** 2, 2)
chk('p8q1', '5.103', 0.7 * 7.29, 3); chk('p8q1', '11.907', 0.3 * 39.69, 3)
chk('p8q1', '5.01', 10 ** 0.7, 2); chk('p8q1', '3070', 1e6 * Pe, 0); chk('p8q1', '3000', 3e5 * 1e-2, 0)
chk('p8q1', '70', 7e5 * 1e-4, 0)
# p8q7
p1 = Q(1.25); p2 = p1 * p1; x2 = Qi(p2)
chk('p8q7', '0.1056', p1, 4); chk('p8q7', '0.106', p1, 3); chk('p8q7', '10.6', 100 * p1, 1)
chk('p8q7', '0.0112', p2, 4); chk('p8q7', '1.12', p2 * 100, 2)
chk('p8q7', '0.0113', Q(2.28), 4); chk('p8q7', '0.0110', Q(2.29), 4)
chk('p8q7', '2.283', 2.28 + 0.01 * (0.0113 - 0.0112) / (0.0113 - 0.0110), 3)
chk('p8q7', '2.2848', x2, 4); chk('p8q7', '2.285', x2, 3)
chk('p8q7', '18.3', x2 * 8, 1); chk('p8q7', '18.24', 2.28 * 8, 2); chk('p8q7', '18.32', 2.29 * 8, 2)
chk('p8q7', '8.3', x2 * 8 - 10, 1)
chk('p8q7', '0.200', 1 - (1 - p1) ** 2, 3)
p3 = p1 ** 3; x3 = Qi(p3)
chk('p8q7', '1.18', p3 * 1e3, 2); chk('p8q7', '3.04', x3, 2); chk('p8q7', '24.3', x3 * 8, 1)
chk('p8q7', '14.3', x3 * 8 - 10, 1); chk('p8q7', '6.0', (x3 * 8 - 10) - (x2 * 8 - 10), 1)
chk('p8q7', '1.25', 10 / 8, 2); chk('p8q7', '64', 8 ** 2, 0)
# p8q8
lcr = 300 / 10; frac = lcr * 0.5e-3; Ts = 1 / 50e3
chk('p8q8', '30', lcr, 0); chk('p8q8', '0.015', frac, 3); chk('p8q8', '1.5', frac * 100, 1)
chk('p8q8', '20', Ts * 1e6, 0); chk('p8q8', '25', 0.5e-3 / Ts, 0); chk('p8q8', '750', lcr * 0.5e-3 / Ts, 0)
chk('p8q8', '500', 50e3 / 100, 0); chk('p8q8', '4', 200 / 50, 0); chk('p8q8', '15', lcr * 0.5, 0)
r2 = log(1 / (1 - frac))
chk('p8q8', '0.985', 1 - frac, 3); chk('p8q8', '0.01511', r2, 5); chk('p8q8', '0.0151', r2, 4)
chk('p8q8', '18.2', -dB(r2), 1); chk('p8q8', '0.123', sqrt(r2), 3); chk('p8q8', '18.24', -dB(0.015), 2)
chk('p8q8', '98.8', lcr / (sqrt(2 * pi) * sqrt(r2) * exp(-r2)), 1); chk('p8q8', '9.1', -dB(sqrt(r2)), 1)
chk('p8q8', '10', 1e3 / 100, 0)
# p8q9
S, I, N, B = 2.0, 0.5, 0.05, 10
snr, sir, sinr = S / N, S / I, S / (I + N)
chk('p8q9', '40', snr, 0); chk('p8q9', '16.0', dB(snr), 1); chk('p8q9', '4', sir, 0); chk('p8q9', '6.0', dB(sir), 1)
chk('p8q9', '3.64', sinr, 2); chk('p8q9', '5.6', dB(sinr), 1); chk('p8q9', '0.275', 1 / snr + 1 / sir, 3)
chk('p8q9', '4.64', 1 + sinr, 2); chk('p8q9', '2.213', log2(1 + sinr), 3); chk('p8q9', '22.1', B * log2(1 + sinr), 1)
chk('p8q9', '5.358', log2(41), 3); chk('p8q9', '53.6', B * log2(41), 1); chk('p8q9', '2.4', log2(41) / log2(1 + sinr), 1)
chk('p8q9', '22.7', B * log2(1 + S / (I + N / 2)), 1); chk('p8q9', '29.4', B * log2(1 + S / (I / 2 + N)), 1)
gb = 10 ** (20 / 10); L1 = log(1 / 0.99); gmin = gb * L1
chk('p8q9', '100', gb, 0); chk('p8q9', '0.01005', L1, 5); chk('p8q9', '1.005', gmin, 3); chk('p8q9', '2.005', 1 + gmin, 3)
chk('p8q9', '0.02', dB(gmin), 2); chk('p8q9', '1.004', log2(1 + gmin), 3); chk('p8q9', '10.0', B * log2(1 + gmin), 1)
chk('p8q9', '10.04', B * log2(1 + gmin), 2); chk('p8q9', '9.94', 0.99 * B * log2(1 + gmin), 2)
chk('p8q9', '6.658', log2(101), 3); chk('p8q9', '66.6', B * log2(101), 1); chk('p8q9', '6.6', log2(101) / log2(1 + gmin), 1)
chk('p8q9', '19.98', 20 - dB(gmin), 2); chk('p8q9', '0.00436', log10(1 / 0.99), 5)
chk('p8q9', '0.436', gb * log10(1 / 0.99), 3); chk('p8q9', '5.2', B * log2(1 + gb * log10(1 / 0.99)), 1)
chk('p8q9', '0.025', 1 / snr, 3); chk('p8q9', '0.25', 1 / sir, 2); chk('p8q9', '0.55', I + N, 2)
chk('p8q9', '0.525', I + N / 2, 3); chk('p8q9', '0.3', I / 2 + N, 1); chk('p8q9', '41', 1 + snr, 0); chk('p8q9', '101', 1 + gb, 0)
# p8q10
lam = 3e8 / 900e6; Pt = 30
fs = lambda d, l=lam: Pt + 20 * log10(l / (4 * pi * d))
chk('p8q10', '0.3333', lam, 4); chk('p8q10', '0.333', lam, 3); chk('p8q10', '12566', 4 * pi * 1000, 0)
chk('p8q10', '2.65', lam / (4 * pi * 1000) * 1e5, 2); chk('p8q10', '4.576', -log10(lam / (4 * pi * 1000)), 3)
chk('p8q10', '91.5', Pt - fs(1000), 1); chk('p8q10', '61.5', -fs(1000), 1)
chk('p8q10', '59.08', 20 * log10(900), 2); chk('p8q10', '91.5', 32.44 + 20 * log10(900), 1)
chk('p8q10', '6.02', 20 * log10(2), 2); chk('p8q10', '67.55', -fs(2000), 2); chk('p8q10', '67.547', -fs(2000), 3)
chk('p8q10', '67.5', -fs(2000), 1); chk('p8q10', '61.53', -fs(1000), 2); chk('p8q10', '0.05', 67.6 - 67.55, 2); chk('p8q10', '31', 10 ** ((fs(1000) - (Pt - 31.5 - 35 * log10(1000))) / 10) / 1e3, 0); chk('p8q10', '73.6', -fs(2000, 3e8 / 1.8e9), 1)
chk('p8q10', '106.5', -(Pt - 31.5 - 35 * log10(1000)), 1); chk('p8q10', '105', 35 * log10(1000), 0)
chk('p8q10', '45', fs(1000) - (Pt - 31.5 - 35 * log10(1000)), 0)
chk('p8q10', '3.1', 10 ** ((fs(1000) - (Pt - 31.5 - 35 * log10(1000))) / 10) / 1e4, 1)
chk('p8q10', '31.5', -20 * log10(lam / (4 * pi)), 1); chk('p8q10', '60', 20 * 3, 0)
chk('p8q10', '6', 20 * log10(2), 0); chk('p8q10', '30', 10 * log10(1000), 0)
# p8q11
ht, hr = 30, 1.5
dc = 4 * ht * hr / lam; tr = 10 * log10(10 * (ht * hr) ** 2 / 5000 ** 4) + 30
fs5 = 10 * log10(10 * (lam / (4 * pi * 5000)) ** 2) + 30
chk('p8q11', '540', dc, 0); chk('p8q11', '180', 4 * ht * hr, 0); chk('p8q11', '2025', (ht * hr) ** 2, 0)
chk('p8q11', '6.25', 5000 ** 4 / 1e14, 2); chk('p8q11', '3.24', 10 * (ht * hr) ** 2 / 5000 ** 4 * 1e11, 2)
chk('p8q11', '74.9', -tr, 1); chk('p8q11', '33.06', 20 * log10(45), 2); chk('p8q11', '147.96', 40 * log10(5000), 2)
chk('p8q11', '65.5', -fs5, 1); chk('p8q11', '105.5', -20 * log10(lam / (4 * pi * 5000)), 1)
chk('p8q11', '2.81', 10 * (lam / (4 * pi * 5000)) ** 2 * 1e10, 2); chk('p8q11', '9.4', fs5 - tr, 1)
chk('p8q11', '1696', pi * dc, 0); chk('p8q11', '1.7', pi * dc / 1e3, 1)
chk('p8q11', '9.4', 20 * log10(5000 / (pi * dc)), 1)
chk('p8q11', '12.04', 40 * log10(2), 2); chk('p8q11', '12', 40 * log10(2), 0); chk('p8q11', '6.02', 20 * log10(2), 2)
chk('p8q11', '6', 20 * log10(2), 0); chk('p8q11', '3.01', 10 * log10(2), 2)
chk('p8q11', '1080', 4 * ht * hr / (3e8 / 1.8e9), 0); chk('p8q11', '1080', 4 * 2 * ht * hr / lam, 0)
chk('p8q11', '40', 10 * log10(10) + 30, 0); chk('p8q11', '0.3333', lam, 4); chk('p8q11', '0.333', lam, 3)

# givens from the question / slides / rules (page numbers, labels, exponents, small integers)
GIVEN = {
 'p8q1': '30 0.7 0.3 10 0 1 100 0.99 0.003 0.00007 5 4 2 6 7 8 9 11 3 1b 0.023',
 'p8q7': '0.01 7 95 105 8 10 1.2 0.05 2.28 2.29 2 3 4 6 11 12 14 15 1b 1 0 2.2848',
 'p8q8': '50 200 100 300 10 0.5 1 2 3 4 31 33 34 35 36 37 39 40 42 43 45 47 2 0.12 50000',
 'p8q9': '0 99 2 0.5 0.05 10 20 0.01 0.99 1 0.301 1a 16 48 49 50 51 3 7 1 0.02 2 5 6 7',
 'p8q10': '67.6 1 900 3 10 8 9 1000 1.8 32.44 32 2 3.5 0.3333 4 51 5 31.5 1 0 20 35 3.7 6.5 10 2 1.0 4.576',
 'p8q11': '0 30 1.5 10 900 5 4 2 3 1 10 8 9 30 5000 1.5 45 40 20 14 11 1.7',
}
def toks(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'p\.\d+(?:–\d+)?', ' ', s)                    # slide page refs
    s = re.sub(r'(?:Q|P)\d\s?Q\d', ' ', s)                       # P2 Q2 etc.
    s = re.sub(r'(?:Practice|第)\s?\d+', ' ', s)
    s = re.sub(r'\d+[ab]\b', ' ', s)                             # 1a / 1b chapter
    s = re.sub(r'(?:Ch|第)\s?\d+(?:–\d+)?', ' ', s)
    return set(re.findall(r'(?<![\w.])\d+(?:\.\d+)?', s))
for i in IDS:
    allowed = set(C.get(i, {})) | set(GIVEN[i].split())
    for k in ('zh', 'en'):
        unk = sorted(toks(XPL[i][k]) - allowed, key=float)
        if unk: bad(f'{i}.{k}: unchecked numbers {unk}')
    nz, ne = toks(XPL[i]['zh']), toks(XPL[i]['en'])
    if nz ^ ne: print(f'  info {i}: numbers only in zh {sorted(nz - ne)} / only in en {sorted(ne - nz)}')

# ---------------------------------------------------------------- report
for i in IDS:
    zh = XPL[i]['zh']; nzh = len(re.findall(r'[一-鿿]', re.sub(r'<[^>]+>', '', zh)))
    print(f'{i}: zh {len(zh)} chars ({nzh} 汉字), en {len(XPL[i]["en"])} chars, h4 {zh.count("<h4>")}')
print('NOTES:', NOTES.count('\n') + 1 if NOTES.strip() else 0, 'line(s)')
if err:
    print('\n'.join('FAIL ' + e for e in err)); sys.exit(1)
print('ALL OK')
