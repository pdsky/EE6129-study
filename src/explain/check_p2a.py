# -*- coding: utf-8 -*-
"""Check src/explain/p2a.py: structure, allowed HTML, TeX, bilingual consistency, and every number.
Run: /usr/bin/python3 check_p2a.py"""
import importlib.util, math, os, random, re, sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('p2a', os.path.join(HERE, 'p2a.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
XPL, NOTES = m.XPL, m.NOTES

IDS = ['p1q1', 'p1q2', 'p1q3', 'p2q1', 'p3q1', 'p3q2', 'p3q3', 'p4q1', 'p4q2', 'p4q3']
ERR = []
def bad(msg): ERR.append(msg)

CJK = re.compile(r'[一-鿿]')

# ------------------------------------------------------------------ HTML structure
ALLOWED = {'h4', 'span', 'p', 'ul', 'ol', 'li', 'b', 'i', 'sub', 'sup', 'br', 'div',
           'table', 'thead', 'tbody', 'tr', 'th', 'td'}
DIVCLS = {'calc', 'tw', 'ans', 'tmpl'}

class P(HTMLParser):
    def __init__(s, where):
        super().__init__(convert_charrefs=True); s.w = where; s.stack = []; s.st = []; s.cur_st = None
        s.tmpl = []; s.in_tmpl = 0; s.tmpl_buf = None
    def handle_starttag(s, tag, attrs):
        a = dict(attrs)
        if tag not in ALLOWED: bad(f'{s.w}: tag <{tag}> not allowed')
        if tag == 'span':
            if a != {'class': 'st'}: bad(f'{s.w}: span attrs {a}')
            if not s.stack or s.stack[-1] != 'h4': bad(f'{s.w}: span.st not directly in h4')
            s.cur_st = ''
        elif tag == 'div':
            c = a.get('class')
            if c not in DIVCLS: bad(f'{s.w}: div class {c}')
            if c == 'tmpl':
                if a != {'class': 'tmpl', 'lang': 'en'}: bad(f'{s.w}: tmpl attrs {a}')
                s.in_tmpl += 1
            elif set(a) != {'class'}: bad(f'{s.w}: div extra attrs {a}')
        elif tag == 'table':
            if a != {'class': 'mini'}: bad(f'{s.w}: table attrs {a}')
            if not s.stack or s.stack[-1] != 'div.tw': bad(f'{s.w}: table not in div.tw')
        elif attrs:
            bad(f'{s.w}: <{tag}> has attrs {a}')
        if tag == 'p' and s.in_tmpl and s.stack and s.stack[-1] != 'div.tmpl':
            bad(f'{s.w}: p in tmpl not direct child')
        if tag != 'br':
            s.stack.append('div.' + a['class'] if tag == 'div' and 'class' in a else tag)
    def handle_endtag(s, tag):
        if tag == 'br': return
        if not s.stack: bad(f'{s.w}: stray </{tag}>'); return
        top = s.stack.pop()
        if top.split('.')[0] != tag: bad(f'{s.w}: </{tag}> closes <{top}>')
        if tag == 'span' and s.cur_st is not None: s.st.append(s.cur_st); s.cur_st = None
        if top == 'div.tmpl': s.in_tmpl -= 1
    def handle_startendtag(s, tag, attrs):
        if tag != 'br': bad(f'{s.w}: self-closing <{tag}/>')
    def handle_data(s, d):
        if s.cur_st is not None: s.cur_st += d
        if s.in_tmpl and CJK.search(d): bad(f'{s.w}: Chinese inside English tmpl: {d[:30]}')

def check_html(where, html):
    p = P(where); p.feed(html); p.close()
    if p.stack: bad(f'{where}: unclosed {p.stack}')
    # raw text outside tags: no < or >
    txt = re.sub(r'<[^<>]*>', '', html)
    if '<' in txt or '>' in txt: bad(f'{where}: raw < or > in text: ' + re.findall(r'.{0,20}[<>].{0,20}', txt)[0])
    # TeX: only \( \) inline, balanced, no display math / dollars
    if '\\[' in html or '\\]' in html or '$' in html: bad(f'{where}: display math or $')
    if html.count('\\(') != html.count('\\)'): bad(f'{where}: unbalanced \\( \\)')
    for seg in re.findall(r'\\\((.*?)\\\)', html, flags=re.S):
        if '\\(' in seg: bad(f'{where}: nested TeX')
    # bare TeX commands outside \( \)
    outside = re.sub(r'\\\(.*?\\\)', '', html, flags=re.S)
    if re.search(r'\\[a-zA-Z]', outside): bad(f'{where}: TeX command outside \\( \\): ' + re.search(r'.{0,20}\\[a-zA-Z]+', outside).group(0))
    tm = re.findall(r'<div class="tmpl" lang="en">(.*?)</div>', html, flags=re.S)
    return p.st, tm

stats = []
for i in IDS:
    if i not in XPL: bad(f'missing id {i}'); continue
    e = XPL[i]
    for k in ('title', 'zh', 'title_en', 'en'):
        if k not in e or not e[k].strip(): bad(f'{i}: missing {k}')
    if set(e) - {'title', 'zh', 'title_en', 'en'}: bad(f'{i}: extra keys {set(e)}')
    t = e['title']
    if not t.startswith('知识讲解 + 详细解析：'): bad(f'{i}: title prefix')
    if len(t.replace(' ', '')) > 30: bad(f'{i}: title too long ({len(t.replace(" ", ""))})')
    if CJK.search(e['title_en']): bad(f'{i}: Chinese in title_en')
    st_zh, tm_zh = check_html(i + '.zh', e['zh'])
    st_en, tm_en = check_html(i + '.en', e['en'])
    for need in ('知识讲解', '详细解析' if i != 'p4q1' else '答题要点', '易错', '考试'):
        if need not in st_zh: bad(f'{i}.zh: no st {need}')
    for need in ('Concept', 'Step by step' if i != 'p4q1' else 'Answer points', 'Pitfalls', 'Exam'):
        if need not in st_en: bad(f'{i}.en: no st {need}')
    if any(CJK.search(s) for s in st_en): bad(f'{i}.en: Chinese st label')
    if not all(CJK.search(s) for s in st_zh): bad(f'{i}.zh: non-Chinese st label {st_zh}')
    if len(st_zh) != len(st_en): bad(f'{i}: section count zh {len(st_zh)} vs en {len(st_en)}')
    if '<div class="ans">一句话：' not in e['zh']: bad(f'{i}.zh: no 一句话 ans')
    if '<div class="ans">In one line:' not in e['en']: bad(f'{i}.en: no In one line ans')
    if CJK.search(e['en']): bad(f'{i}.en: contains Chinese: ' + CJK.search(e['en']).group(0))
    if len(tm_zh) != 1 or tm_zh != tm_en: bad(f'{i}: tmpl missing or zh/en differ')
    # structural parity: same number of calc / tables / li
    for tag in ('<div class="calc">', '<table', '<li>', '<h4>'):
        if e['zh'].count(tag) != e['en'].count(tag): bad(f'{i}: count of {tag} zh {e["zh"].count(tag)} en {e["en"].count(tag)}')
    nzh = len(CJK.findall(re.sub(r'<[^>]*>', '', e['zh'])))
    stats.append((i, nzh, len(re.sub(r'<[^>]*>', '', e['en']).split())))

# ------------------------------------------------------------------ numbers
Q = lambda x: 0.5 * math.erfc(x / math.sqrt(2))
def Qinv(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if Q(mid) > p else (lo, mid)
    return lo
def f2(x, n=2): return f'{x:.{n}f}'
def sci(x, n=2):
    s = f'{x:.{n}e}'; a, b = s.split('e'); b = int(b)
    sup = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    return f'{a} × 10' + str(b).translate(sup)
def has(i, s, langs=('zh', 'en')):
    for L in langs:
        if s not in XPL[i][L]: bad(f'{i}.{L}: expected "{s}" not found')
def close(name, got, want, tol):
    if abs(got - want) > tol: bad(f'{name}: computed {got} vs written {want}')

# P1 Q1 -------------------------------------------------------------
d = [5, 25, 65, 110, 400, 1000]; M = [-60, -80, -105, -115, -130, -150]; n = 6
x = [10 * math.log10(v) for v in d]
Sx, Sx2, SM, SxM = sum(x), sum(a * a for a in x), sum(M), sum(a * b for a, b in zip(x, M))
Sxx = Sx2 - Sx ** 2 / n; SxMc = SxM - Sx * SM / n
g = -SxMc / Sxx; xb = Sx / n; Mb = SM / n; K = Mb + g * xb
e = [mm - (K - g * a) for a, mm in zip(x, M)]
mse = sum(v * v for v in e) / n; sig = math.sqrt(mse)
has('p1q1', '6.99、13.98、18.13、20.41、26.02、30.00', ('zh',))
has('p1q1', '6.99, 13.98, 18.13, 20.41, 26.02, 30.00', ('en',))
for s in [f'Σx = {f2(Sx)}', f'Σx² = {f2(Sx2)}', f'ΣM = {SM}'.replace('-', '−'), f'ΣxM = {f2(SxM)}'.replace('-', '−'),
          f'{f2(Sx2)} − {f2(Sx ** 2 / n)} = {f2(Sxx)}', f'{f2(SxM)} + {f2(-Sx * SM / n)} = {f2(SxMc)}'.replace('-', '−'),
          f'γ = {f2(-SxMc)} / {f2(Sxx)} = {f2(g)}', f'−{f2(-Mb)} + {f2(g)} × {f2(xb)} = {K:.1f} dB'.replace('-', '−').replace('−−', '−'),
          f'{f2(sum(v * v for v in e))} / 6 = {f2(mse)}', f'√{f2(mse)} = {f2(sig)}', f'10 / {f2(sig)} = {f2(10 / sig)}']:
    has('p1q1', s)
close('p1q1 Pout', Q(10 / sig), 1.85e-3, 0.005e-3)
close('p1q1 Q(2.90) table', Q(2.90), 1.87e-3, 0.005e-3)
has('p1q1', '1.85 × 10⁻³'); has('p1q1', '1.87 × 10⁻³')
resid = ['−1.67', '+5.88', '−2.77', '−3.77', '+3.32', '−0.99']
for r_, v in zip(resid, e): close('p1q1 resid', v, float(r_.replace('−', '-')), 0.006)
has('p1q1', '、'.join(resid), ('zh',)); has('p1q1', ', '.join(resid), ('en',))
close('p1q1 sum resid', sum(e), 0, 1e-9)
close('p1q1 log10 gamma x10', 10 * g, 39.4, 0.05); has('p1q1', '39.4')
eo = [mm - (-31.4 - 3.86 * a) for a, mm in zip(x, M)]
close('p1q1 official mse', sum(v * v for v in eo) / n, 13.1, 0.05); has('p1q1', '13.1')
close('p1q1 lecturer arg', 10 / math.sqrt(9.656), 3.22, 0.005); close('p1q1 Q(3.23)', Q(3.23), 6.19e-4, 0.005e-4)
has('p1q1', '10/√9.656 = 3.22'); has('p1q1', '6.19 × 10⁻⁴')
close('p1q1 0.19%', Q(10 / sig) * 100, 0.19, 0.005)
close('p1q1 2.33sigma=1%', Q(2.33), 0.01, 0.0002)

# P1 Q2 -------------------------------------------------------------
close('p1q2 Q(.625)', Q(0.625), 0.266, 0.0005); close('p1q2 Q(.62)', Q(0.62), 0.2676, 0.00005); close('p1q2 Q(.63)', Q(0.63), 0.2643, 0.00005)
close('p1q2 0.734', 1 - Q(0.625), 0.734, 0.0005)
for s in ['Q(0.62) = 0.2676', 'Q(0.63) = 0.2643', 'Q(0.625) ≈ 0.266', '26.6%', '0.734', 'Q(2.32) = 0.0102', 'Q(2.33) = 0.0099',
          '2.326 × 4 = 9.31 dB', '10 + 4 × 2.326 = 19.3 dBm', '10 + 8 × 2.326 = 28.6 dBm', '9.3 dB', '0.1587', '1.645', '3.09']:
    has('p1q2', s)
close('Q(2.32)', Q(2.32), 0.0102, 0.00005); close('Q(2.33)', Q(2.33), 0.0099, 0.00005)
qi = Qinv(0.01); close('Qinv .01', qi, 2.326, 0.0005)
close('p1q2 margin', 4 * qi, 9.31, 0.005); close('p1q2 mu', 10 + 4 * qi, 19.3, 0.05); close('p1q2 mu8', 10 + 8 * qi, 28.6, 0.05)
close('p1q2 diff', 4 * qi, 9.3, 0.05); close('Q(1)', Q(1), 0.1587, 0.00005); close('Q(1.645)', Q(1.645), 0.05, 0.0001)
close('Q(3.09)', Q(3.09), 1e-3, 0.00002)

# P1 Q3 -------------------------------------------------------------
N = 200000; h = 10 / N
mu = sum((k + .5) * h * h for k in range(N)) / 10
var = sum(((k + .5) * h - mu) ** 2 * h for k in range(N)) / 10
close('p1q3 mu', mu, 5, 1e-6); close('p1q3 int(t-5)^2', var * 10, 83.33, 0.005); close('p1q3 var', var, 8.33, 0.005)
close('p1q3 E t2', 1000 / 3 / 10, 33.33, 0.005); close('p1q3 sigma', math.sqrt(var), 2.89, 0.005)
close('p1q3 10sigma', 10 * math.sqrt(var), 28.87, 0.005); close('p1q3 Rs', 1 / (10 * math.sqrt(var) * 1e-6), 34641, 0.6)
close('p1q3 a/sqrt12', 10 / math.sqrt(12), 2.89, 0.005); close('sqrt12', math.sqrt(12), 3.46, 0.005)
for s in ['50/10 = 5 µs', '83.33', '8.33 µs²', '33.33', '2.89 µs', '28.87 µs', '34641', '34.6 ksps', '10 × 2.887 = 28.87', '10/3.46']:
    has('p1q3', s)

# P2 Q1 -------------------------------------------------------------
r = 0.1; fD = 50
num = math.exp(r * r) - 1; den = math.sqrt(2 * math.pi) * fD * r; afd = num / den; lcr = den * math.exp(-r * r)
close('p2q1 num', num, 0.01005, 0.000005); close('p2q1 den', den, 12.53, 0.005); close('p2q1 afd', afd, 8.0e-4, 0.05e-4)
close('p2q1 afd 8.02', afd, 8.02e-4, 0.005e-4); close('p2q1 lcr', lcr, 12.41, 0.005)
close('p2q1 product', 8.02e-4 * 12.41, 0.00995, 0.000005); close('p2q1 1-e', 1 - math.exp(-0.01), 0.00995, 0.000005)
close('p2q1 approx', r / (math.sqrt(2 * math.pi) * fD), 7.98e-4, 0.005e-4); close('p2q1 125.3', math.sqrt(2 * math.pi) * fD, 125.3, 0.05)
close('p2q1 sqrt2pi', math.sqrt(2 * math.pi), 2.5066, 0.00005); close('p2q1 dB', 20 * math.log10(0.1), -20, 1e-9)
close('p2q1 symbols', afd * 1e4, 8, 0.05)
rp = math.sqrt(0.1); afdp = (math.exp(0.1) - 1) / (math.sqrt(2 * math.pi) * fD * rp)
close('p2q1 power rho', rp, 0.316, 0.0005); close('p2q1 afd power', afdp * 1e3, 2.65, 0.005); close('p2q1 e0.1-1', math.exp(0.1) - 1, 0.105, 0.0005)
if not 3 < afdp / afd < 4: bad('p2q1: 差 3 倍多 wrong')
for s in ['0.01005', '12.53', '8.0 × 10⁻⁴ s', '0.8 ms', '12.41', '8.02 × 10⁻⁴ × 12.41 = 0.00995', '7.98 × 10⁻⁴', '0.1/125.3',
          '2.5066', '2.65 ms', '0.316', '0.105', '−20 dB']:
    has('p2q1', s)

# P3 Q1 -------------------------------------------------------------
T = 2.0; N = 20000; h = T / N; ts = [(k + .5) * h for k in range(N)]
cs = sum(math.cos(2 * math.pi * t / T) * math.sin(2 * math.pi * t / T) for t in ts) * h
cc = sum(math.cos(2 * math.pi * t / T) ** 2 for t in ts) * h; ss = sum(math.sin(2 * math.pi * t / T) ** 2 for t in ts) * h
close('p3q1 orth', cs, 0, 1e-9); close('p3q1 cos2', cc, T / 2, 1e-9); close('p3q1 sin2', ss, T / 2, 1e-9)
A, ph = 1.7, 0.6
psi1 = lambda t: math.sqrt(2 / T) * math.cos(2 * math.pi * t / T); psi2 = lambda t: math.sqrt(2 / T) * math.sin(2 * math.pi * t / T)
s = lambda t: A * math.cos(2 * math.pi * t / T + ph)
c1 = sum(s(t) * psi1(t) for t in ts) * h; c2 = sum(s(t) * psi2(t) for t in ts) * h
close('p3q1 coord1', c1, A * math.cos(ph) * math.sqrt(T / 2), 1e-6); close('p3q1 coord2', c2, -A * math.sin(ph) * math.sqrt(T / 2), 1e-6)
close('p3q1 energy', c1 ** 2 + c2 ** 2, sum(s(t) ** 2 for t in ts) * h, 1e-6)
has('p3q1', 'T/2'); has('p3q1', '√(2/T)')

# P3 Q2 -------------------------------------------------------------
s0, s1 = 0.1, 0.4; S0, S1 = math.sqrt(s0), math.sqrt(s1)
gfun = lambda y: y * y / (2 * s0) - (y - 1) ** 2 / (2 * s1) + math.log(S0 / S1)
a2, b2, c2_ = 1 / (2 * s0) - 1 / (2 * s1), 1 / s1, -1 / (2 * s1) + math.log(S0 / S1)
close('p3q2 a', a2, 3.75, 1e-9); close('p3q2 b', b2, 2.5, 1e-9); close('p3q2 c', c2_, -1.943, 0.0005)
yt = (-b2 + math.sqrt(b2 * b2 - 4 * a2 * c2_)) / (2 * a2); y2 = (-b2 - math.sqrt(b2 * b2 - 4 * a2 * c2_)) / (2 * a2)
close('p3q2 thr', yt, 0.46, 0.005); close('p3q2 root2', y2, -1.13, 0.005); close('p3q2 g(yt)', gfun(yt), 0, 1e-9)
# closed form written in the box
aa = s1 - s0
ycf = (-s0 + math.sqrt(s0 ** 2 + aa * (s0 + s0 * s1 * math.log(s1 / s0)))) / aa
close('p3q2 closed form', ycf, yt, 1e-9)
# multiplied form: (s1-s0)y^2 + 2 s0 y - s0 - s0 s1 ln(s1/s0) = 2 s0 s1 g(y)
for yy in (-2, 0.3, 0.7, 1.5):
    close('p3q2 quad form', aa * yy * yy + 2 * s0 * yy - s0 - s0 * s1 * math.log(s1 / s0), 2 * s0 * s1 * gfun(yy), 1e-9)
# wrong threshold without 1/sigma
yw = (-s0 + math.sqrt(s0 ** 2 + aa * s0)) / aa; close('p3q2 wrong thr', yw, 0.33, 0.005)
f = lambda y, mu_, s_: math.exp(-(y - mu_) ** 2 / (2 * s_ * s_)) / (math.sqrt(2 * math.pi) * s_)
close('p3q2 f(.5|0)', f(0.5, 0, S0), 0.361, 0.0005); close('p3q2 f(.5|1)', f(0.5, 1, S1), 0.461, 0.0005)
pe = 0.5 * (Q(yt / S0) + Q((1 - yt) / S1)); pm = 0.5 * (Q(0.5 / S0) + Q(0.5 / S1))
close('p3q2 args', 0.460 / 0.3162, 1.455, 0.0005); close('p3q2 args2', 0.540 / 0.6325, 0.854, 0.0005)
close('p3q2 Q1.455', Q(1.455), 0.0728, 0.00005); close('p3q2 Q.854', Q(0.854), 0.1966, 0.00005)
close('p3q2 sum rounded', 0.5 * (0.0728 + 0.1966), 0.135, 0.0005)
close('p3q2 pe', pe, 0.135, 0.0005); close('p3q2 pm', pm, 0.136, 0.0005)
close('p3q2 mid args', 0.5 / S0, 1.581, 0.0005); close('p3q2 mid args2', 0.5 / S1, 0.791, 0.0005)
close('p3q2 sigma', S0, 0.316, 0.0005); close('p3q2 sigma1', S1, 0.632, 0.0005)
if not pe < pm: bad('p3q2: ML not better than midpoint')
p_tail0 = Q(-y2 / S0); close('p3q2 tail', p_tail0, 2e-4, 0.5e-4)
pex = 0.5 * (Q(yt / S0) + Q(-y2 / S0) + Q((1 - yt) / S1) - Q((1 - y2) / S1))
close('p3q2 exact diff', abs(pex - pe), 1e-4, 0.3e-4)
for s in ['3.75y² + 2.5y − 1.943', '0.46', '−1.13', '0.33', '0.361', '0.461', '1.455', '0.854', 'Q(1.455) + Q(0.854)',
          '0.0728 + 0.1966', '= 0.135', 'Q(1.581) + Q(0.791)', '0.136', '0.460/0.3162', '0.540/0.6325']:
    has('p3q2', s)

# P3 Q3 -------------------------------------------------------------
Ts = 3e-6 / math.sqrt(1e-3)
close('p3q3 sqrt', math.sqrt(1e-3), 0.0316, 0.00005); close('p3q3 Ts', Ts * 1e6, 94.87, 0.005)
close('p3q3 Rb', 2 / Ts / 1e3, 21.08, 0.005); close('p3q3 BPSK', 1 / Ts / 1e3, 10.54, 0.005)
close('p3q3 ratio', 3e-6 / Ts, 0.0316, 0.00005)
for s in ['0.0316', '94.87 µs', '21.08 kbps', '10.54 kbps', '10<sup>−1.5</sup>', '0.1² = 10⁻²']:
    has('p3q3', s)

# P4 Q1 -------------------------------------------------------------
close('p4q1 Q1', Q(1), 0.1587, 0.00005); close('p4q1 Q1^2', Q(1) ** 2, 0.0252, 0.00005)
# correlated macro-diversity rho=0.5, Delta = sigma (Practice 2 Q2(c)): numeric integral
b_ = math.sqrt(0.5); a_ = math.sqrt(0.5); Nn = 20000; lo, hi = -10, 10; hh = (hi - lo) / Nn
Pc = sum(Q((1 + b_ * (lo + (k + .5) * hh)) / a_) ** 2 * math.exp(-(lo + (k + .5) * hh) ** 2 / 2) / math.sqrt(2 * math.pi) for k in range(Nn)) * hh
close('p4q1 rho .5', Pc, 0.0625, 0.0005)
for s in ['0.1² = 1%', '0.1³ = 0.1%', 'Q(1) = 0.1587', '[Q(1)]² = 0.0252', '2.5%', '6.3%']:
    has('p4q1', s)

# P4 Q2 -------------------------------------------------------------
E = math.exp
pa = (1 / 3) * 0.5 * E(-8) + (2 / 3) * 0.5 * E(-11)
close('p4q2 gbar', 8 / 3 + 22 / 3, 10, 1e-9); close('p4q2 pa1', (1 / 3) * 0.5 * E(-8), 5.59e-5, 0.005e-5)
close('p4q2 pa2', (2 / 3) * 0.5 * E(-11), 0.56e-5, 0.005e-5); close('p4q2 pa', pa, 6.15e-5, 0.005e-5)
close('p4q2 naive', 0.5 * E(-10), 2.27e-5, 0.005e-5)
pb_terms = [0.5 * E(-16) / 9, 0.5 * E(-19) * 4 / 9, 0.5 * E(-22) * 4 / 9]; pb = sum(pb_terms)
for v, w in zip(pb_terms, [6.25e-9, 1.25e-9, 0.06e-9]): close('p4q2 b term', v, w, 0.005e-9)
close('p4q2 pb', pb, 7.56e-9, 0.005e-9); close('p4q2 d b', -math.log10(pb), 8.12, 0.005)
if not pb_terms[0] / pb > 0.8: bad('p4q2: 八成以上 wrong')
close('p4q2 gsig', (16 + 76 + 88) / 9, 20, 1e-9); close('p4q2 3dB', 10 * math.log10(2), 3.01, 0.005)
close('p4q2 shortcut', 2 * pa, 1.23e-4, 0.005e-4); close('p4q2 shortcut2', 0.5 * (2 * pa) ** 2, 7.56e-9, 0.005e-9)
close('p4q2 d single', -math.log10(pa), 4.2, 0.05)
Er = (1 / 3) * E(-0.6) + (2 / 3) * E(-1.2)
close('p4q2 Er1', (1 / 3) * E(-0.6), 0.1829, 0.00005); close('p4q2 Er2', (2 / 3) * E(-1.2), 0.2008, 0.00005); close('p4q2 Er', Er, 0.3837, 0.00005)
cb7 = 0.5 * Er ** 2 * E(-14); cb10 = 0.5 * Er ** 2 * E(-20)
close('p4q2 cb7', cb7, 6.12e-8, 0.005e-8); close('p4q2 cb10', cb10, 1.52e-10, 0.005e-10)
Eb = (1 / 3) * E(-14) + (2 / 3) * E(-20); close('p4q2 Eb', Eb, 2.786e-7, 0.0005e-7)
pc = (1 / 3) * cb7 + (2 / 3) * cb10; close('p4q2 pc', pc, 2.05e-8, 0.005e-8); close('p4q2 pc2', 0.5 * Er ** 2 * Eb, pc, 1e-20)
enum = 0; meanS = 0
for r1, p1 in [(0.6, 1 / 3), (1.2, 2 / 3)]:
    for r2, p2 in [(0.6, 1 / 3), (1.2, 2 / 3)]:
        for bb, p3 in [(7, 1 / 3), (10, 2 / 3)]:
            enum += p1 * p2 * p3 * 0.5 * E(-(r1 + r2 + 2 * bb)); meanS += p1 * p2 * p3 * (r1 + r2 + 2 * bb)
close('p4q2 enum', enum, pc, 1e-20); close('p4q2 meanS', meanS, 20, 1e-9)
close('p4q2 d c', -math.log10(pc), 7.7, 0.05); close('p4q2 log2.05', math.log10(2.05), 0.31, 0.005)
close('p4q2 ratio', pc / pb, 2.7, 0.05)
close('p4q2 Er mean', 0.6 / 3 + 2.4 / 3, 1, 1e-9); close('p4q2 Eb mean', 7 / 3 + 20 / 3, 9, 1e-9)
for s in ['6.15 × 10⁻⁵', '5.59 × 10⁻⁵ + 0.56 × 10⁻⁵', '2.27 × 10⁻⁵', '6.25 × 10⁻⁹', '1.25 × 10⁻⁹', '0.06 × 10⁻⁹', '7.56 × 10⁻⁹',
          '180/9 = 20', '3.01 dB', '8.12 / 1 = 8.1', '1.23 × 10⁻⁴', '0.1829 + 0.2008 = 0.3837', '6.12 × 10⁻⁸', '1.52 × 10⁻¹⁰',
          '2.05 × 10⁻⁸', '2.786 × 10⁻⁷', '8 − 0.31 = 7.7', '2.7', '4.2']:
    has('p4q2', s)

# P4 Q3 -------------------------------------------------------------
a0, s1q, Ee, s2q = 1.0, 0.1, 1.0, 0.1
args = {Mk: math.sqrt(Mk) * a0 * math.sqrt(Ee) / math.sqrt(s1q * Ee + s2q) for Mk in (1, 2, 4)}
close('p4q3 arg1', args[1], 2.24, 0.005); close('p4q3 arg2', args[2], 3.16, 0.005); close('p4q3 arg4', args[4], 4.47, 0.005)
close('p4q3 P1', Q(args[1]), 0.0127, 0.00005); close('p4q3 P2', Q(args[2]), 7.8e-4, 0.05e-4); close('p4q3 P4', Q(args[4]), 3.9e-6, 0.05e-6)
corr = 4 * a0 / math.sqrt(16 * s1q + 4 * s2q); close('p4q3 corr arg', corr, 2.83, 0.005); close('p4q3 corr P', Q(corr), 2.3e-3, 0.05e-3)
random.seed(1); Nmc = 400000; err = 0
for _ in range(Nmc):
    z = sum(random.gauss(a0, math.sqrt(s1q)) * math.sqrt(Ee) + random.gauss(0, math.sqrt(s2q)) for _ in range(2))
    err += z <= 0
close('p4q3 MC', err / Nmc, 8.0e-4, 0.05e-4)
# general variance check by MC for M=1 formula
for s in ['Q(2.24) = 0.0127', 'Q(3.16) = 7.8 × 10⁻⁴', '8.0 × 10⁻⁴', 'Q(4.47) = 3.9 × 10⁻⁶', 'Q(2.83) = 2.3 × 10⁻³', '1/√0.2',
          'M²σ₁²E + Mσ₂²', 'M(σ₁²E + σ₂²)']:
    has('p4q3', s)

# ------------------------------------------------------------------ report
print('id     zh-CJK  en-words')
for i, a, b in stats: print(f'{i:6s} {a:6d}  {b:6d}')
long_ = [i for i, a, _ in stats if not 500 <= a <= 2200]
if long_: print('note: Chinese length outside 500–2200:', long_)
print('NOTES lines:', len([l for l in NOTES.splitlines() if l.strip()]))
if ERR:
    print(f'\n{len(ERR)} problem(s):'); [print(' -', e_) for e_ in ERR]; sys.exit(1)
print('\nALL OK: 10 ids, HTML/TeX valid, zh/en parity, all numbers verified')
