# -*- coding: utf-8 -*-
"""Check src/explain/p2b.py: structure, allowed HTML, zh/en parity, and every number.
Run:  /usr/bin/python3 check_p2b.py
"""
import cmath, importlib.util, os, re, sys
from html.parser import HTMLParser
from math import erfc, log2, log10, sqrt, pi

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('p2b', os.path.join(HERE, 'p2b.py'))
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
XPL, NOTES = M.XPL, M.NOTES
IDS = ['p5q1', 'p5q2', 'p5q3', 'p6q1', 'p6q2', 'p6q3', 'p7q1', 'p7q2', 'p7q3']
ERR = []
def err(m): ERR.append(m)

# ------------------------------------------------------------------ structure / HTML
ALLOWED = {'h4', 'span', 'p', 'ul', 'ol', 'li', 'b', 'i', 'sub', 'sup', 'br', 'div',
           'table', 'thead', 'tbody', 'tr', 'th', 'td'}
DIV_CLS = {'calc', 'tw', 'ans', 'tmpl'}

class V(HTMLParser):
    def __init__(s, where):
        super().__init__(convert_charrefs=False); s.w = where; s.stack = []; s.seq = []; s.text = []
    def handle_starttag(s, t, a):
        a = dict(a)
        if t not in ALLOWED: err(f'{s.w}: tag <{t}> not allowed')
        bad = set(a) - {'class', 'lang'}
        if bad: err(f'{s.w}: attributes {bad} on <{t}>')
        if 'style' in a: err(f'{s.w}: inline style')
        c = a.get('class')
        if t == 'span' and (c != 'st' or not s.stack or s.stack[-1][0] != 'h4'): err(f'{s.w}: span must be h4 > span.st')
        if t == 'div':
            if c not in DIV_CLS: err(f'{s.w}: div class {c!r}')
            if c == 'tmpl' and a.get('lang') != 'en': err(f'{s.w}: div.tmpl needs lang=en')
        if t == 'table' and (c != 'mini' or not s.stack or s.stack[-1][1] != 'tw'): err(f'{s.w}: table must be div.tw > table.mini')
        if s.stack and s.stack[-1][1] == 'tmpl' and t != 'p': err(f'{s.w}: div.tmpl child must be p, got {t}')
        if t in ('div', 'p', 'h4', 'ul', 'ol', 'table') and c not in (None, 'st'):
            pass
        s.seq.append((t, c))
        if t != 'br': s.stack.append((t, c))
    def handle_endtag(s, t):
        if t == 'br': return
        if not s.stack or s.stack[-1][0] != t: err(f'{s.w}: unbalanced </{t}> (stack {[x[0] for x in s.stack][-3:]})'); return
        s.stack.pop()
    def handle_data(s, d):
        if '<' in d or '>' in d: err(f'{s.w}: raw < or > in text: {d[:60]!r}')
        s.text.append(d)
    def close(s):
        super().close()
        if s.stack: err(f'{s.w}: unclosed {s.stack}')

def check_body(qid, lang, body):
    w = f'{qid}.{lang}'
    # every '<' must start an allowed tag
    for m in re.finditer(r'<(/?)([a-zA-Z0-9]*)', body):
        if m.group(2).lower() not in ALLOWED: err(f'{w}: stray "<" near {body[m.start():m.start()+20]!r}')
    v = V(w); v.feed(body); v.close()
    # TeX: only inline \( \)
    if '\\[' in body or '$' in body: err(f'{w}: display TeX or $ found')
    if body.count('\\(') != body.count('\\)'): err(f'{w}: unbalanced \\( \\)')
    for seg in re.findall(r'\\\((.*?)\\\)', body, flags=re.S):
        if '<' in seg or '>' in seg: err(f'{w}: < or > inside TeX: {seg[:40]!r}')
    return v

for q in IDS:
    if q not in XPL: err(f'missing id {q}'); continue
    e = XPL[q]
    for k in ('title', 'zh', 'title_en', 'en'):
        if not e.get(k): err(f'{q}: missing {k}')
    if len(e['title']) > 30: err(f'{q}: title {len(e["title"])} chars > 30')
    if not e['title'].startswith('知识讲解 + 详细解析：'): err(f'{q}: title prefix')
    vz = check_body(q, 'zh', e['zh']); ve = check_body(q, 'en', e['en'])
    for s_ in ('<span class="st">知识讲解</span>', '<span class="st">详细解析</span>', '<span class="st">易错</span>',
               '<span class="st">考试</span>', '<div class="tmpl" lang="en">', '<div class="ans">一句话：'):
        if s_ not in e['zh']: err(f'{q}.zh: missing {s_}')
    for s_ in ('<span class="st">Concept</span>', '<span class="st">Step by step</span>', '<span class="st">Pitfalls</span>',
               '<span class="st">Exam</span>', '<div class="tmpl" lang="en">', '<div class="ans">In one line:'):
        if s_ not in e['en']: err(f'{q}.en: missing {s_}')
    if vz.seq != ve.seq: err(f'{q}: zh/en tag structure differs ({len(vz.seq)} vs {len(ve.seq)} tags)')
    # exam template identical in both languages
    tz = re.search(r'<div class="tmpl" lang="en">(.*?)</div>', e['zh'], re.S).group(1)
    te = re.search(r'<div class="tmpl" lang="en">(.*?)</div>', e['en'], re.S).group(1)
    if tz != te: err(f'{q}: exam template differs between zh and en')
    # Chinese body length (characters of CJK only) for info
    cjk = len(re.findall(r'[一-鿿]', e['zh']))
    print(f'{q}: zh CJK chars {cjk:5d}, zh len {len(e["zh"]):5d}, en len {len(e["en"]):5d}, tags {len(vz.seq)}')
extra = set(XPL) - set(IDS)
if extra: err(f'unexpected ids {extra}')

# ------------------------------------------------------------------ numbers
Q = lambda x: 0.5 * erfc(x / sqrt(2))
def both(q, *ss):
    for s_ in ss:
        for lang in ('zh', 'en'):
            if s_ not in XPL[q][lang]: err(f'{q}.{lang}: expected text {s_!r} not found')
def near(name, val, want, tol):
    if abs(val - want) > tol: err(f'{name}: computed {val:.6g}, text says {want}')

# P5 Q1 water-filling 80, 40, 40, B = 10 MHz
g = [80, 40, 40]; s3 = 1 + sum(1 / x for x in g); g0 = 3 / s3
near('p5q1 3/g0', s3, 1.0625, 1e-12); near('p5q1 g0', g0, 2.82, 0.005); near('p5q1 1/g0', 1 / g0, 0.354, 0.0005)
P = [1 / g0 - 1 / x for x in g]; near('p5q1 P1', P[0], 0.342, 0.0005); near('p5q1 P2', P[1], 0.329, 0.0005)
near('p5q1 sum P', sum(P), 1, 1e-12)
near('p5q1 g1/g0', 80 / g0, 28.33, 0.005); near('p5q1 g2/g0', 40 / g0, 14.17, 0.005)
near('p5q1 log10 28.33', log10(28.33), 1.452, 0.0005); near('p5q1 log10 14.17', log10(14.17), 1.151, 0.0005)
near('p5q1 1.452/0.301', 1.452 / 0.301, 4.82, 0.006); near('p5q1 1.151/0.301', 1.151 / 0.301, 3.82, 0.006)
Cwf = 10 * sum(log2(x / g0) for x in g); near('p5q1 C/B', Cwf / 10, 12.47, 0.005); near('p5q1 C', Cwf, 124.7, 0.05)
near('p5q1 log2 g1/g0', log2(80 / g0), 4.82, 0.005); near('p5q1 2log2 g2/g0', 2 * log2(40 / g0), 7.65, 0.005)
Ceq = 10 * sum(log2(1 + x / 3) for x in g); near('p5q1 Ceq', Ceq, 124.7, 0.05)
near('p5q1 eq term1', log2(1 + 80 / 3), 4.79, 0.005); near('p5q1 eq term2', log2(1 + 40 / 3), 3.84, 0.005)
near('p5q1 80/3', 80 / 3, 26.7, 0.05); near('p5q1 40/3', 40 / 3, 13.3, 0.05)
near('p5q1 diff', Cwf - Ceq, 0.006, 0.0005)
near('p5q1 wrong eq', 10 * sum(log2(x / 3) for x in g), 122.1, 0.05)
# low-SNR comparison quoted from the key-points box: 0.8, 0.4, 0.4 → WF 0.85, equal 0.70, 21 %
wf_low = log2(0.8 / (1 / (1 + 1 / 0.8))); eq_low = log2(1 + 0.8 / 3) + 2 * log2(1 + 0.4 / 3)
near('p5q1 lowSNR wf', wf_low, 0.85, 0.005); near('p5q1 lowSNR eq', eq_low, 0.70, 0.005)
near('p5q1 lowSNR gain %', (wf_low / eq_low - 1) * 100, 21, 0.6); near('p5q1 lowSNR loss %', (1 - eq_low / wf_low) * 100, 17, 0.6)
both('p5q1', '1.0625', '2.82', '0.354', '0.342', '0.329', '28.33', '14.17', '124.7', '122.1', '0.006', '12.47')

# P5 Q2 Alamouti algebra (random check + the worked example)
import random
random.seed(1)
for _ in range(200):
    hA, hB, u1, u2, w1, w2 = [complex(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(6)]
    y1 = hA * u1 + hB * u2 + w1; y2 = -hA * u2.conjugate() + hB * u1.conjugate() + w2
    n2 = abs(hA) ** 2 + abs(hB) ** 2
    z1 = hA.conjugate() * y1 + hB * y2.conjugate(); z2 = hB.conjugate() * y1 - hA * y2.conjugate()
    if abs(z1 - (n2 * u1 + hA.conjugate() * w1 + hB * w2.conjugate())) > 1e-9: err('p5q2 z1 algebra')
    if abs(z2 - (n2 * u2 + hB.conjugate() * w1 - hA * w2.conjugate())) > 1e-9: err('p5q2 z2 algebra')
    F = [[hA, hB], [hB.conjugate(), -hA.conjugate()]]
    FH = [[F[j][i].conjugate() for j in range(2)] for i in range(2)]
    G = [[sum(FH[i][k] * F[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    if abs(G[0][0] - n2) > 1e-9 or abs(G[1][1] - n2) > 1e-9 or abs(G[0][1]) > 1e-9 or abs(G[1][0]) > 1e-9: err('p5q2 F^H F')
# noise of z1 / ||h|| has variance N0, and the two noises are uncorrelated (Monte Carlo, N0 = 1)
hA, hB = 0.7 + 0.2j, -0.4 + 1.1j; n = sqrt(abs(hA) ** 2 + abs(hB) ** 2); acc = acc12 = 0; K = 200000
cw = lambda: complex(random.gauss(0, sqrt(.5)), random.gauss(0, sqrt(.5)))
for _ in range(K):
    w1, w2 = cw(), cw(); a = (hA.conjugate() * w1 + hB * w2.conjugate()) / n; b = (hB.conjugate() * w1 - hA * w2.conjugate()) / n
    acc += abs(a) ** 2; acc12 += a * b.conjugate()
near('p5q2 normalised noise var', acc / K, 1.0, 0.02); near('p5q2 noise corr', abs(acc12 / K), 0.0, 0.02)
hA, hB, u1, u2 = 1, 1j, 1, -1
y1 = hA * u1 + hB * u2; y2 = -hA * u2 + hB * u1        # u real → u* = u
z1 = hA * y1 + hB * y2.conjugate(); z2 = (-1j) * y1 - hA * y2.conjugate()
if y1 != 1 - 1j or y2 != 1 + 1j or abs(z1 - 2) > 1e-12 or abs(z2 + 2) > 1e-12: err(f'p5q2 example y1={y1} y2={y2} z1={z1} z2={z2}')
both('p5q2', '−u₂*', 'N(0, N₀)', '= 2 = ‖h‖²u₁', '= −2 = ‖h‖²u₂', '3 dB')

# P5 Q3 DMT 8 x 4, 10 dB, Pe <= 1e-3
gam = 10 ** (10 / 10); dmin = 3 / log10(gam); near('p5q3 dmin', dmin, 3, 1e-12)
d = [(8 - r) * (4 - r) for r in range(5)]
if d != [32, 21, 12, 5, 0]: err(f'p5q3 d table {d}')
rmax = max(r for r in range(5) if d[r] >= dmin)
if rmax != 3: err('p5q3 r')
r1, r2 = 6 - sqrt(7), 6 + sqrt(7); near('p5q3 root1', r1, 3.35, 0.005); near('p5q3 root2', r2, 8.65, 0.005)
if abs((8 - r1) * (4 - r1) - 3) > 1e-9: err('p5q3 quadratic')
near('p5q3 log2 10', log2(10), 3.32, 0.002); near('p5q3 R', 3 * log2(10), 9.97, 0.005); near('p5q3 R exact', 3 * log2(10), 9.966, 0.0005)
near('p5q3 R r=4', 4 * log2(10), 13.3, 0.05); near('p5q3 R r=2', 2 * log2(10), 6.64, 0.005)
if d[3] != 5 or d[2] != 12: err('p5q3 d(3), d(2)')
both('p5q3', '9.97', '9.96', '3.35', '8.65', '6 ± √7', 'r² − 12r + 29 = 0', '13.3', '6.64', '10<sup>−5</sup>', '10<sup>−12</sup>')

# P6 Q1 binary PAM with H = 1 + a z^-1, U = 1 - a z^-1
a = 0.4
ne = lambda A: 0.5 * Q((1 - a) * A) + 0.5 * Q((1 + a) * A)
eq = lambda A: 0.5 * Q((1 - a * a) / sqrt(1 + a * a) * A) + 0.5 * Q((1 + a * a) / sqrt(1 + a * a) * A)
near('p6q1 worst eq arg', (1 - a * a) / sqrt(1 + a * a), 0.78, 0.005); near('p6q1 sqrt(1.16)', sqrt(1 + a * a), 1.077, 0.0005)
near('p6q1 ne A=2', ne(2), 0.0588, 0.00005); near('p6q1 ne A=3', ne(3), 0.0180, 0.00005)
near('p6q1 eq A=2', eq(2), 0.0375, 0.00005); near('p6q1 eq A=3', eq(3), 0.0051, 0.00005)
near('p6q1 ½Q(1.8)', 0.5 * Q(1.8), 0.0180, 0.00005); near('p6q1 ½Q(4.2)', 0.5 * Q(4.2) * 1e6, 7, 0.5)
near('p6q1 ne A=1', ne(1), 0.1775, 0.00005); near('p6q1 eq A=1', eq(1), 0.1792, 0.00005)
lo, hi = 0.5, 2.0
for _ in range(80):
    m = (lo + hi) / 2
    if ne(m) < eq(m): lo = m
    else: hi = m
near('p6q1 crossover A', lo, 1.06, 0.005); near('p6q1 crossover Eb/N0 dB', 10 * log10(lo * lo / 2), -2.5, 0.06)
for al in [0.01, 0.1, 0.25, 0.49, 0.7, 0.99]:
    if not (1 - al * al) / sqrt(1 + al * al) > 1 - al: err(f'p6q1 inequality fails at {al}')
# signal / noise response of the cascade
hu = [1, 0, -a * a]  # (1 + a z^-1)(1 - a z^-1)
if [round(x, 12) for x in [1, a - a, -a * a]] != [round(x, 12) for x in hu]: err('p6q1 cascade')
both('p6q1', '0.78A', '0.0588', '0.0180', '0.0375', '0.0051', '1.06', '−2.5 dB', '0.1775', '0.1792', '1.077', '7 × 10⁻⁶')

# P6 Q2 ZF, noise variance 0.1
def zf_taps(a, n=8):  # long division of 1 by (1 + a z^-1)
    rem = [1.0] + [0.0] * n; q = []
    for k in range(n):
        c = rem[k]; q.append(c); rem[k] -= c; rem[k + 1] -= c * a
    return q
t = zf_taps(0.5)
if any(abs(t[k] - (-0.5) ** k) > 1e-12 for k in range(8)): err('p6q2 long division')
for a_ in (0.5, 0.9):
    s = sqrt(0.1)
    pa = 0.5 * Q((1 + a_) / s) + 0.5 * Q((1 - a_) / s); pb = Q(sqrt((1 - a_ ** 2) / 0.1))
    if a_ == 0.5:
        near('p6q2 a=.5 args', (1 + a_) / s, 4.74, 0.005); near('p6q2 a=.5 arg2', (1 - a_) / s, 1.58, 0.005)
        near('p6q2 a=.5 pa', pa, 0.0285, 0.00005); near('p6q2 a=.5 zf arg', sqrt(7.5), 2.74, 0.005)
        near('p6q2 a=.5 pb', pb, 0.0031, 0.00005); near('p6q2 ratio', pa / pb, 9, 0.5); near('p6q2 enh', 1 / (1 - a_ ** 2), 1.33, 0.005)
    else:
        near('p6q2 a=.9 arg1', (1 + a_) / s, 6.01, 0.005); near('p6q2 a=.9 arg2', (1 - a_) / s, 0.316, 0.0005)
        near('p6q2 a=.9 pa', pa, 0.188, 0.0005); near('p6q2 a=.9 zf arg', sqrt((1 - a_ ** 2) / 0.1), 1.38, 0.005)
        near('p6q2 a=.9 pb', pb, 0.084, 0.0005); near('p6q2 a=.9 enh', 1 / (1 - a_ ** 2), 5.26, 0.005)
near('p6q2 sqrt0.1', sqrt(0.1), 0.316, 0.0005)
near('p6q2 geometric', sum(0.25 ** k for k in range(200)), 1 / (1 - 0.25), 1e-12)
both('p6q2', '0.0285', '0.0031', '4.74', '1.58', '2.74', '0.188', '0.084', '6.01', '1.33', '5.26', '0.316')

# P6 Q3 MMSE linear + DFE, x0 = 1, x1 = 1/2, sigma^2 = 1
mse = lambda q: q * q / 4 + 0.25 + q * q + 1 + q * q
near('p6q3 mse(0)', mse(0), 1.25, 1e-12); near('p6q3 mse coeff', mse(1) - mse(0), 2.25, 1e-12)
# Monte Carlo check of the MSE expression at q = 0.3
random.seed(2); qq = 0.3; acc = 0; K = 200000
for _ in range(K):
    Am1, A0, Ap1 = [random.choice((-1, 1)) for _ in range(3)]; z0, z1 = random.gauss(0, 1), random.gauss(0, 1)
    yn = A0 + 0.5 * Am1 + z0; yn1 = Ap1 + 0.5 * A0 + z1; acc += (yn + qq * yn1 - A0) ** 2
near('p6q3 MSE MC', acc / K, mse(qq), 0.02)
pa = 0.5 * Q(1.5) + 0.5 * Q(0.5)
near('p6q3 Q1.5', Q(1.5), 0.0668, 0.00005); near('p6q3 Q0.5', Q(0.5), 0.3085, 0.00005); near('p6q3 pa', pa, 0.188, 0.0005)
pc, pw = Q(1), 0.5 * Q(2) + 0.25
near('p6q3 Q1', pc, 0.159, 0.0005); near('p6q3 Q2', Q(2), 0.0228, 0.00005); near('p6q3 ½Q2', 0.5 * Q(2), 0.0114, 0.00005)
near('p6q3 pw', pw, 0.261, 0.0005)
p = pc / (1 - pw + pc); near('p6q3 p', p, 0.177, 0.0005); near('p6q3 denom', 1 - 0.261 + 0.159, 0.898, 1e-12); near('p6q3 0.159/0.898', 0.159 / 0.898, 0.177, 0.0005)
seq = [pc]
for _ in range(3): seq.append(pc * (1 - seq[-1]) + pw * seq[-1])
near('p6q3 p2', seq[1], 0.175, 0.0005); near('p6q3 p3', seq[2], 0.1766, 0.00005); near('p6q3 p4', seq[3], 0.1768, 0.00005)
# Monte Carlo of the DFE itself (A0 = 0, n large)
random.seed(3); errs = 0; prevA = 0; prevhat = 0; K = 400000
for n_ in range(K):
    A = random.choice((-1, 1)); y = A + 0.5 * prevA + random.gauss(0, 1); u = y - 0.5 * prevhat
    ah = 1 if u >= 0 else -1
    if n_ > 1000 and ah != A: errs += 1
    prevA, prevhat = A, ah
near('p6q3 DFE MC', errs / (K - 1001), 0.177, 0.003)
both('p6q3', '1.25 + 2.25q²', '0.0668', '0.3085', '0.188', '0.159', '0.261', '0.0114', '0.177', '0.898', '0.175', '0.1766', '0.1768', '0.0228')

# P7 Q1 OFDM N = 4, h = [0.8, 0.6], total power 10, sigma^2 = 1
N = 4; h = [0.8, 0.6]
H = [sum(h[i] * cmath.exp(-2j * pi * i * k / N) for i in range(2)) for k in range(N)]
for k, want in enumerate([1.4, 0.8 - 0.6j, 0.2, 0.8 + 0.6j]):
    if abs(H[k] - want) > 1e-12: err(f'p7q1 H{k}')
G = [abs(H[k % N]) ** 2 for k in (1, 2, 3, 4)]
if any(abs(x - y) > 1e-12 for x, y in zip(G, [1, 0.04, 1, 1.96])): err('p7q1 |H|^2')
near('p7q1 Parseval', sum(G), 4, 1e-12)
S = sum(1 / x for x in G); near('p7q1 S', S, 27.51, 0.005); c = 10 / S; near('p7q1 c', c, 0.3635, 0.00005)
Pc = [c / x for x in G]
for x, w in zip(Pc, [0.36, 9.09, 0.36, 0.19]): near('p7q1 Pc', x, w, 0.005)
near('p7q1 Pc sum', sum(Pc), 10, 1e-9); near('p7q1 91%', Pc[1] / 10 * 100, 91, 0.5)
near('p7q1 1/1.96', 1 / 1.96, 0.51, 0.005)
mu4 = (10 + S) / 4; near('p7q1 mu4', mu4, 9.38, 0.005); near('p7q1 37.51', 10 + S, 37.51, 0.005)
mu = (10 + 1 + 1 + 1 / 1.96) / 3; near('p7q1 mu', mu, 4.17, 0.005); near('p7q1 12.51', 10 + 1 + 1 + 1 / 1.96, 12.51, 0.005)
Pw = [mu - 1, mu - 1, mu - 1 / 1.96]
for x, w in zip(Pw, [3.17, 3.17, 3.66]): near('p7q1 Pw', x, w, 0.005)
near('p7q1 Pw sum', sum(Pw), 10, 1e-9)
C = 2 * log2(mu) + log2(mu * 1.96); near('p7q1 C', C, 7.15, 0.005); near('p7q1 C/4', C / 4, 1.79, 0.005)
near('p7q1 log2 mu', log2(mu), 2.06, 0.005); near('p7q1 log2 mu*1.96', log2(mu * 1.96), 3.03, 0.005)
gk = [10 * x for x in G]; g0 = 10 / mu; near('p7q1 g0', g0, 2.40, 0.005)
s_ = 1 + sum(1 / x for x in gk if x >= g0); near('p7q1 g0 from slide formula', 3 / s_, g0, 1e-9)
near('p7q1 C via g0', sum(log2(x / g0) for x in gk if x >= g0), C, 1e-9)
ceq_sub = log2(1 + c); near('p7q1 eqcap per sub', ceq_sub, 0.447, 0.0005); near('p7q1 eqcap total', 4 * ceq_sub, 1.79, 0.005)
Cpow = sum(log2(1 + 2.5 * x) for x in G); near('p7q1 equal power', Cpow, 6.31, 0.005); near('p7q1 equal power/4', Cpow / 4, 1.58, 0.005)
both('p7q1', '27.51', '0.3635', '9.09', '9.38', '4.17', '3.17', '3.66', '7.15', '1.79', '2.40', '0.447', '6.31', '1.58', '91%', '2.06', '3.03', '12.51', '37.51')

# P7 Q2 OFDM design
B, TG, Rb, k = 600e3, 20e-6, 2e6, 4
Rs = Rb / k; near('p7q2 Rs', Rs, 500e3, 1e-6)
Nn = Rs * TG / (1 - Rs / B); near('p7q2 N', Nn, 60, 1e-9); near('p7q2 coef', Rs / B, 0.8333, 0.00005); near('p7q2 const', Rs * TG, 10, 1e-9)
T = 60 / B; near('p7q2 T us', T * 1e6, 100, 1e-9); near('p7q2 total us', (T + TG) * 1e6, 120, 1e-9)
near('p7q2 df', B / 60, 10e3, 1e-9); near('p7q2 rate', 60 * 4 / (T + TG), 2e6, 1e-3)
near('p7q2 per-sub rate', 1 / (T + TG), 8.33e3, 5); near('p7q2 Bc', 1 / TG, 50e3, 1e-6)
near('p7q2 loss dB', 10 * log10(120 / 100), 0.79, 0.005)
near('p7q2 quick T', 5 * 20, 100, 0); near('p7q2 5/6', 500 / 600, 5 / 6, 1e-12)
both('p7q2', '500 k', 'N = 60', '100 µs', '120 µs', '0.12 ms', '0.8333N + 10', '10 kHz', '50 kHz', '0.79 dB', '8.33 k')

# P7 Q3 CP with h = [1, 0.9], N = 4: CP of 1 sample gives circular convolution → R_k = H_k S_k
import random as R_
R_.seed(4); hh = [1, 0.9]; N = 4
def dft(x): return [sum(x[n] * cmath.exp(-2j * pi * n * k / N) for n in range(N)) for k in range(N)]
prev = [complex(R_.gauss(0, 1), R_.gauss(0, 1)) for _ in range(N)]
x = [complex(R_.gauss(0, 1), R_.gauss(0, 1)) for _ in range(N)]
for G_, expect_ok in ((1, True), (0, False)):
    tx = prev[N - G_:] + prev + x[N - G_:] + x if G_ else prev + x
    rx = [tx[i] + (0.9 * tx[i - 1] if i else 0) for i in range(len(tx))]
    kept = rx[-N:]
    Hk = dft(hh + [0] * (N - 2)); Xk = dft(x); Rk = dft(kept)
    ok = all(abs(Rk[k] - Hk[k] * Xk[k]) < 1e-9 for k in range(N))
    if ok != expect_ok: err(f'p7q3 CP={G_} circular check gave {ok}')
for k, want in enumerate([1.9, 1 - 0.9j, 0.1, 1 + 0.9j]):
    if abs(Hk[k] - want) > 1e-12: err(f'p7q3 H{k}')
both('p7q3', 'L − 1 = 1', '1.9', '1 − 0.9j', '0.1', '1 + 0.9j', 'N/(N + G)')

# ------------------------------------------------------------------ report
print()
if ERR:
    print(f'{len(ERR)} problem(s):'); [print(' -', e) for e in ERR]; sys.exit(1)
print(f'OK: {len(IDS)} ids, structure + zh/en parity + all numbers checked.')
print('NOTES:'); print(NOTES)
