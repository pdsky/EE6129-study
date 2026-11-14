#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Check src/explain/exA.py: structure, allowed HTML, and every number written in the boxes."""
import importlib.util, os, sys, cmath
from math import *
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('exA', os.path.join(HERE, 'exA.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
XPL, NOTES = m.XPL, m.NOTES

IDS = ['y2324s2-q1a', 'y2324s2-q1b1', 'y2324s2-q1b2', 'y2324s2-q2a', 'y2324s2-q2b', 'y2324s2-q3a',
       'y2324s2-q3b', 'y2324s2-q4ab', 'y2324s2-q4c', 'y2425s2-q1a', 'y2425s2-q1b1', 'y2425s2-q1b2',
       'y2425s2-q2a', 'y2425s2-q2b', 'y2425s2-q3', 'y2425s2-q4a', 'y2425s2-q4b', 'y2425s2-q4c']
err = []
def bad(msg): err.append(msg)

# ---------------------------------------------------------------- structure
ALLOWED = {'h4', 'span', 'p', 'ul', 'ol', 'li', 'b', 'i', 'sub', 'sup', 'br', 'div', 'table',
           'thead', 'tbody', 'tr', 'th', 'td'}
VOID = {'br'}
class P(HTMLParser):
    def __init__(s, qid):
        super().__init__(convert_charrefs=True); s.qid = qid; s.stack = []
    def handle_starttag(s, tag, attrs):
        a = dict(attrs)
        if tag not in ALLOWED: bad(f'{s.qid}: tag <{tag}> not allowed')
        if 'style' in a: bad(f'{s.qid}: inline style')
        if tag == 'span' and a.get('class') != 'st': bad(f'{s.qid}: span without class st')
        if tag == 'div':
            c = a.get('class')
            if c not in ('calc', 'tw', 'ans', 'tmpl'): bad(f'{s.qid}: div class {c}')
            if c == 'tmpl' and a.get('lang') != 'en': bad(f'{s.qid}: tmpl without lang=en')
        if tag == 'table' and a.get('class') != 'mini': bad(f'{s.qid}: table not .mini')
        if tag == 'table' and (not s.stack or s.stack[-1] != ('div', 'tw')): bad(f'{s.qid}: table not inside div.tw')
        if tag == 'p' and s.stack and s.stack[-1][0] == 'div' and s.stack[-1][1] == 'tmpl':
            pass
        if tag not in VOID: s.stack.append((tag, a.get('class')))
    def handle_startendtag(s, tag, attrs):
        if tag not in VOID: bad(f'{s.qid}: self-closing <{tag}/>')
    def handle_endtag(s, tag):
        if tag in VOID: return
        if not s.stack or s.stack[-1][0] != tag:
            bad(f'{s.qid}: unbalanced </{tag}> (stack {[t for t, _ in s.stack[-3:]]})'); return
        s.stack.pop()
    def handle_data(s, d):
        pass

for q in IDS:
    if q not in XPL: bad(f'missing id {q}'); continue
    e = XPL[q]; t, z = e['title'], e['zh']
    if not t.startswith('知识讲解 + 详细解析：'): bad(f'{q}: title prefix')
    if len(t.split('：', 1)[1]) > 30: bad(f'{q}: title too long')
    for need in ('<span class="st">知识讲解</span>', '<div class="ans">一句话：', '<div class="tmpl" lang="en">',
                 '<span class="st">易错</span>', '<span class="st">考试</span>英文写法'):
        if need not in z: bad(f'{q}: missing {need}')
    if '\\(' in z or '$' in z or '<script' in z or '<a ' in z or '<img' in z: bad(f'{q}: forbidden content')
    import re
    txt = re.sub(r'</?[a-z0-9]+(\s+[a-z-]+="[^"]*")*\s*/?>', '', z)
    for ch_ in '<>':
        if ch_ in txt: bad(f'{q}: raw {ch_} in text near {txt[max(0, txt.index(ch_) - 20):txt.index(ch_) + 20]!r}')
    p = P(q); p.feed(z); p.close()
    if p.stack: bad(f'{q}: unclosed {p.stack}')
    zh_chars = sum(1 for c in z if '一' <= c <= '鿿')
    print(f'{q:15s} 中文字数 {zh_chars:5d}  total chars {len(z):6d}')
extra = set(XPL) - set(IDS)
if extra: bad(f'extra ids {extra}')

# ---------------------------------------------------------------- numbers
def Q(x): return 0.5 * erfc(x / sqrt(2))
def Qinv(p):
    lo, hi = -10, 40
    for _ in range(200):
        mm = (lo + hi) / 2
        if Q(mm) > p: lo = mm
        else: hi = mm
    return lo
def erlB(A, M):
    b = 1.0
    for k in range(1, M + 1): b = A * b / (k + A * b)
    return b
def Aof(M, p):
    lo, hi = 1e-6, M * 1.5
    for _ in range(200):
        mm = (lo + hi) / 2
        if erlB(mm, M) < p: lo = mm
        else: hi = mm
    return lo
dB = lambda x: 10 * log10(x); lin = lambda d: 10 ** (d / 10)

C = []   # (qid, literal that must appear in the body, stated value, computed value, tolerance)
def c(q, lit, stated, val, tol=None):
    if tol is None:
        s = repr(stated); dec = len(s.split('.')[1]) if '.' in s and 'e' not in s else 0
        tol = 0.5 * 10 ** (-dec) * 1.0001 + 1e-12
    C.append((q, lit, stated, val, tol))

q = 'y2324s2-q1a'
z = Qinv(0.01)
c(q, 'Q(2.33) = 0.0099', 0.0099, Q(2.33), 5e-5)
c(q, '精确值 2.326', 2.326, z)
c(q, 'σ &lt; 10/2.326 = 4.30 dB', 4.30, 10 / z)
c(q, '4.30² = 18.5 dB²', 18.5, (10 / z) ** 2)
c(q, 'Q(2) = 0.0228', 0.0228, Q(2))
c(q, 'ln(1.001001) = 0.0010005', 0.0010005, -log(1 - 0.001), 5e-8)
c(q, '1/(1 − 0.001)', 1.001001, 1 / 0.999, 5e-7)
c(q, '10 log₁₀(999.5) ≈ 30.0 dB', 30.0, -dB(-log(1 - 0.001)))
c(q, '999.5', 999.5, 1 / -log(0.999), 0.05)
c(q, 'ε = 10⁻² → 20 dB', 20, -dB(-log(0.99)), 0.05)

q = 'y2324s2-q1b1'
g10, g12 = lin(10), lin(12)
c(q, '10<sup>1.2</sup> = 15.85', 15.85, g12)
avg = 0.2 * g10 + 0.8 * g12
c(q, '2 + 12.68 = 14.68', 14.68, avg); c(q, '12.68', 12.68, 0.8 * g12)
c(q, '10 log₁₀14.68 = 11.67 dB', 11.67, dB(avg))
sd = 0.04 * g10 + 0.96 * g12
c(q, '0.96 × 15.85 = 15.61 → 11.94 dB', 15.61, sd); c(q, '11.94 dB', 11.94, dB(sd))
c(q, '½e<sup>−10</sup> = 2.27×10⁻⁵', 2.27e-5, 0.5 * exp(-10), 5e-8)
c(q, '½e<sup>−15.85</sup> = 6.54×10⁻⁸', 6.54e-8, 0.5 * exp(-g12), 5e-11)
c(q, '9.08×10⁻⁷ + 6.28×10⁻⁸', 9.08e-7, 0.04 * 0.5 * exp(-10), 5e-10)
c(q, '6.28×10⁻⁸ ≈', 6.28e-8, 0.96 * 0.5 * exp(-g12), 5e-11)
Pe = 0.04 * 0.5 * exp(-10) + 0.96 * 0.5 * exp(-g12)
c(q, '≈ 9.71×10⁻⁷', 9.71e-7, Pe, 5e-10)
Pe1 = 0.2 * 0.5 * exp(-10) + 0.8 * 0.5 * exp(-g12)
c(q, '≈ 4.59×10⁻⁶', 4.59e-6, Pe1, 5e-9)
c(q, '约小 4.7 倍', 4.7, Pe1 / Pe)
c(q, '占总数约 94%', 0.94, 0.04 * 0.5 * exp(-10) / Pe)
c(q, '½e<sup>−15.61</sup> ≈ 8.3×10⁻⁸', 8.3e-8, 0.5 * exp(-sd), 5e-10)
c(q, '0.2 × 10 + 0.8 × 12 = 11.6 dB', 11.6, 0.2 * 10 + 0.8 * 12)

q = 'y2324s2-q1b2'
s1, s2 = 1 + 1j, 1 - 1j
X = [[s1, -s2.conjugate()], [s2, s1.conjugate()]]
XXH = [[sum(X[i][k] * X[j][k].conjugate() for k in range(2)) for j in range(2)] for i in range(2)]
c(q, '代入得 X X<sup>H</sup> = 4I', 4, XXH[0][0].real, 1e-12)
assert abs(XXH[1][1] - 4) < 1e-12 and abs(XXH[0][1]) < 1e-12 and abs(XXH[1][0]) < 1e-12
# Alamouti combining with random numbers
h1, h2, a, b = 0.3 - 0.7j, -1.1 + 0.4j, 0.6 + 0.2j, -0.5 + 0.9j
y1 = h1 * a + h2 * b; y2 = -h1 * b.conjugate() + h2 * a.conjugate()
comb = h1.conjugate() * y1 + h2 * y2.conjugate()
assert abs(comb - (abs(h1) ** 2 + abs(h2) ** 2) * a) < 1e-12, 'Alamouti combining'
c(q, 'min(3, 5) = 3', 3, min(3, 5), 0)
c(q, '3 × 5 = 15', 15, 3 * 5, 0)
c(q, '少约 3 dB', 3, dB(2), 0.02)

q = 'y2324s2-q2a'
s2v = 0.3 * 1.36; sd2 = sqrt(s2v)
c(q, '0.3 × 1.36 = 0.408', 0.408, s2v); c(q, '√0.408 = 0.639', 0.639, sd2)
c(q, 'Q(1.00)', 1.00, 0.64 / sd2); c(q, 'Q(2.13)', 2.13, 1.36 / sd2)
c(q, '½ × 0.1587', 0.1587, Q(1.0)); c(q, '½ × 0.0166', 0.0166, Q(1.36 / sd2))
c(q, '0.0166 ≈ 0.087', 0.087, 0.5 * (Q(0.64 / sd2) + Q(1.36 / sd2)))
c(q, 'σ = √0.3 = 0.548', 0.548, sqrt(0.3))
c(q, 'P<sub>b</sub> = ½Q(0.4/0.548) + ½Q(1.6/0.548) ≈ 0.117', 0.117, 0.5 * (Q(0.4 / sqrt(0.3)) + Q(1.6 / sqrt(0.3))))
# product check
import itertools
def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] += x * y
    return r
pr = pmul([1, 0, -0.6], [1, 0, 0.6]); assert all(abs(u - v) < 1e-12 for u, v in zip(pr, [1, 0, 0, 0, -0.36]))
c(q, '1 − 0.36Z⁻⁴', 0.36, -pr[4])

q = 'y2324s2-q2b'
h = [1, -0.6, 0.2]; H = [sum(h[i] * cmath.exp(-2j * pi * i * k / 4) for i in range(3)) for k in range(1, 5)]
for k, (re_, im_) in enumerate([(0.8, 0.6), (1.8, 0), (0.8, -0.6), (0.6, 0)]):
    assert abs(H[k] - complex(re_, im_)) < 1e-12, ('H', k + 1)
c(q, '|H<sub>k</sub>|', 1.0, abs(H[0]), 1e-9); c(q, '0.8 − 0.6j', 1.0, abs(H[2]), 1e-9)
c(q, 'N = 1 MHz / 250 kHz = 4', 4, 1e6 / 250e3, 0)
c(q, '4 + 1 = 5 µs', 5, 4 + 1, 0)
c(q, '10 × 0.0969 ≈ 0.97 dB', 0.97, dB(5 / 4)); c(q, '0.0969', 0.0969, log10(1.25))
c(q, '20% 的时间', 0.20, 1 / 5)

q = 'y2324s2-q3a'
Au = 0.9 * 90 / 3600; A57 = Aof(57, 0.01); m1 = A57 / Au; ar1 = floor(m1) / 720
c(q, '= 0.0225 E', 0.0225, Au)
c(q, 'A ≈ 44.2 E/小区', 44.2, A57)
c(q, 'm = 44.2/0.0225 ≈ 1965', 1965, floor(m1), 0)
c(q, '面积 = 1965/720 = 2.73 km²', 2.73, ar1)
c(q, '3√3/2 = 2.598', 2.598, 3 * sqrt(3) / 2)
c(q, '√1.051', 1.051, 2.73 / (3 * sqrt(3) / 2))          # same rounding chain as the solution (area 2.73)
c(q, '≈ 1.03 km', 1.03, sqrt(2.73 / (3 * sqrt(3) / 2)))
c(q, '≈ 1.03 km', 1.03, sqrt(m1 / 720 / (3 * sqrt(3) / 2)), 0.0051)   # unrounded: 1.025 km
c(q, '1965/57 ≈ 34.5', 34.5, 1965 / 57)
A19 = Aof(19, 0.01)
c(q, 'A ≈ 11.2 E/扇区', 11.2, A19); c(q, '3 × 11.23 = 33.7 E', 11.23, A19); c(q, '= 33.7 E', 33.7, 3 * A19)
m2 = 3 * A19 / Au; ar2 = floor(m2) / 720
c(q, 'm = 33.7/0.0225 ≈ 1497', 1497, floor(m2), 0)
c(q, '面积 = 1497/720 = 2.08 km²', 2.08, ar2)
c(q, '≈ 0.89 km', 0.89, sqrt(ar2 / (3 * sqrt(3) / 2)))
c(q, '1497/57 ≈ 26.3', 26.3, 1497 / 57)
c(q, '少约 24%', 0.24, 1 - 3 * A19 / A57)
c(q, 'A/M 从 0.78', 0.78, A57 / 57); c(q, '降到 0.59', 0.59, 3 * A19 / 57)
c(q, '2.73/2.08 ≈ 1.31', 1.31, ar1 / ar2)
c(q, '讲义 p.122 例子：50 条、2% 时为 24.2', 24.2, 1210 / 50)

q = 'y2324s2-q4c'
Qr = sqrt(21); n = log10(600) / log10(Qr)
c(q, '1.76 + 16.90 = 18.66 dB', 18.66, 1.76 + 20 * log10(7)); c(q, '16.90', 16.90, 20 * log10(7))
c(q, '10 log₁₀1.5', 1.76, dB(1.5))
c(q, '18.66 dB（p.89）', 18.66, dB(Qr ** 4 / 6))
c(q, '17.27 dB（p.91）', 17.27, dB(1 / (2 * (Qr - 1) ** -4 + 2 * Qr ** -4 + 2 * (Qr + 1) ** -4)))
c(q, 'Q = √21 = 4.583', 4.583, Qr)
c(q, '2.778/0.661 ≈ 4.20', 2.778, log10(600)); c(q, '0.661', 0.661, log10(Qr)); c(q, '≈ 4.20', 4.20, n)
nn = 4.2
c(q, '3.583<sup>4.2</sup> = 212.6', 212.6, (Qr - 1) ** nn); c(q, 'Q<sup>4.2</sup> = 597.9', 597.9, Qr ** nn)
c(q, '5.583<sup>4.2</sup> = 1370', 1370, (Qr + 1) ** nn, 0.5)
w = 2 / (Qr - 1) ** nn + 2 / Qr ** nn + 2 / (Qr + 1) ** nn
c(q, '= 1/0.0142', 0.0142, w); c(q, '≈ 70.4 → 18.5 dB', 70.4, 1 / w); c(q, '18.5 dB', 18.5, dB(1 / w))
c(q, '5.283<sup>4.2</sup> = 1086', 1086, (Qr + 0.7) ** nn, 0.5)
s120 = 1 / (Qr ** -nn + (Qr + 0.7) ** -nn)
c(q, '≈ 385.7 → 25.9 dB', 385.7, s120); c(q, '25.9 dB', 25.9, dB(s120))
c(q, '高约 7.4 dB', 7.4, dB(s120) - dB(1 / w)); c(q, '还剩约 6 dB', 6, dB(s120) - 20, 0.5)
# with exact n (4.202) the answers round the same
assert round(dB(1 / (2 * (Qr - 1) ** -n + 2 * Qr ** -n + 2 * (Qr + 1) ** -n)), 1) == 18.5
assert round(dB(1 / (Qr ** -n + (Qr + 0.7) ** -n)), 1) == 25.9

q = 'y2425s2-q1a'
c(q, 'B = 88/35 = 2.51', 2.51, 88 / 35); c(q, '10<sup>2.51</sup> ≈ 327 m', 327, 10 ** (88 / 35), 0.5)
c(q, 'T<sub>s</sub> = 6 µs / 3 = 2 µs', 2, 6 / 3, 0)
c(q, '5 × 3 = 15', 15, 5 * 3, 0)
c(q, '15/(5×10⁵) = 3×10⁻⁵', 3e-5, 15 / 5e5, 1e-12); c(q, '5 × 6×10⁻⁶ = 3×10⁻⁵', 3e-5, 5 * 6e-6, 1e-12)
g = [lin(18), lin(10), lin(3)]
c(q, '18 dB → 63.1', 63.1, g[0]); c(q, '3 dB → 2.0', 2.0, g[2])
inv0 = (1 + sum(1 / x for x in g)) / 3
c(q, '1 + 0.0158', 0.0158, 1 / g[0], 5e-5); c(q, '0.501)/3', 0.501, 1 / g[2]); c(q, '1.617/3', 1.617, 1 + sum(1 / x for x in g))
c(q, '= 0.539', 0.539, inv0); c(q, 'γ₀ = 1/0.539 = 1.855', 1.855, 1 / inv0); c(q, '（2.7 dB）', 2.7, dB(1 / inv0))
P = [inv0 - 1 / x for x in g]
c(q, '0.523 W', 0.523, P[0]); c(q, '0.439 W', 0.439, P[1]); c(q, '0.038 W', 0.038, P[2])
c(q, '0.539 − 0.016', 0.016, 1 / g[0]); c(q, '和为 1 W', 1, sum(P), 1e-9)

q = 'y2425s2-q1b1'
gb = Qinv(1.35e-3) ** 2 / 2; base = 1 - exp(-4.5 / 30)
c(q, 'x = 3.00', 3.00, Qinv(1.35e-3)); c(q, '= 4.5（6.53 dB）', 4.5, gb, 1e-3); c(q, '6.53 dB', 6.53, dB(4.5))
c(q, '约 14.8 dB', 14.8, dB(30))
c(q, '1 − 0.861 = 0.139', 0.861, exp(-0.15)); c(q, '= 0.139', 0.139, base)
c(q, '(−3.91)/(−1.97) ≈ 1.98', 1.98, log(0.02) / log(base)); c(q, '(−3.91)', -3.91, log(0.02)); c(q, '(−1.97)', -1.97, log(base))
c(q, '0.139² = 0.0194', 0.0194, base ** 2); c(q, '<td>0.0027</td>', 0.0027, base ** 3)
c(q, '15%（4.5/30）', 0.15, 4.5 / 30); c(q, '概率是 13.9%', 0.139, base)

q = 'y2425s2-q1b2'
c(q, '5 × 3 = 15', 15, 15, 0)
c(q, 'SNR = (10⁻³)<sup>−1/3</sup> = 10', 10, (1e-3) ** (-1 / 3), 1e-9)
c(q, '2 × 3.32 ≈ 6.64', 6.64, 2 * log2(10)); c(q, '= 3.32', 3.32, log2(10))
c(q, 'd(2) = (5 − 2)(3 − 2) = 3', 3, (5 - 2) * (3 - 2), 0)
c(q, 'log₂(1 + 16) = log₂17', 16, 1 * 4 / 0.25, 0)
c(q, '1.230/0.301 ≈ 4.09', 4.09, log2(17)); c(q, '1.230', 1.230, log10(17))
c(q, 'log₂9 ≈ 3.17', 3.17, log2(9))

q = 'y2425s2-q2a'
pr = pmul([1, -0.2, 0.04], [1, 0.2]); assert all(abs(u - v) < 1e-12 for u, v in zip(pr, [1, 0, 0, 0.008]))
c(q, '= 1 + 0.008Z⁻³', 0.008, pr[3])
inv = [(-0.2) ** k for k in range(4)]
assert [round(x, 6) for x in inv] == [1, -0.2, 0.04, -0.008]
c(q, 'σ = √0.64 = 0.8', 0.8, sqrt(0.64))
c(q, 'Q(2) = 0.0228', 0.0228, Q(2)); c(q, 'Q(0.5) = 0.3085', 0.3085, Q(0.5))
c(q, '≈ 0.166', 0.166, 0.5 * (Q(0.5) + Q(2)))
c(q, 'Q(1.25) ≈ 0.106', 0.106, Q(1.25))
c(q, '约 1.6 倍', 1.6, 0.5 * (Q(0.5) + Q(2)) / Q(1.25))

q = 'y2425s2-q2b'
c(q, '5×10⁶ × 2 = 10 Mbit/s', 10, 5 * 2, 0); c(q, '5/4 = 1.25', 1.25, 5 / 4); c(q, '10/4 = 2.5', 2.5, 10 / 4)
c(q, 'T<sub>s</sub> = 1/(5×10⁶) = 0.2 µs', 0.2, 1e6 / 5e6); c(q, '4T<sub>s</sub> = 0.8 µs', 0.8, 4 * 0.2)
Pk = 2 ** 3.6 - 1
c(q, '2<sup>3.6</sup> = 12.126', 12.126, 2 ** 3.6); c(q, '10<sup>1.084</sup>', 1.084, 3.6 * 0.301); c(q, '≈ 12.13', 12.13, 10 ** 1.084, 0.01)
c(q, '= 11.126（≈ 11.13）', 11.126, Pk)
Ps = [Pk / x ** 2 for x in (1, 0.2, 1, 1.4)]
c(q, '11.126/0.04 = 278.1', 278.1, Ps[1]); c(q, '11.126/1.96 = 5.68', 5.68, Ps[3])
c(q, '再除得 278.25', 278.25, 11.13 / 0.04, 1e-9)
c(q, '≈ 306.1', 306.1, sum(Ps))
c(q, '278.1/306.1 ≈ 91%', 0.91, Ps[1] / sum(Ps))

q = 'y2425s2-q3'
ch = (20 - 2) / 0.2 * 8
c(q, '18 MHz / 200 kHz = 90', 90, 18 / 0.2, 1e-9); c(q, '90 × 8 = 720', 720, ch, 0)
c(q, '10<sup>1.8</sup> = 63.1', 63.1, 10 ** 1.8)
c(q, 'Q<sup>3.7</sup> ≥ 378.6', 378.6, 6 * 10 ** 1.8)
Qm = (6 * 10 ** 1.8) ** (1 / 3.7)
c(q, '378.6<sup>1/3.7</sup> = 4.98', 4.98, Qm); c(q, '4.98²/3 = 8.25', 8.25, Qm ** 2 / 3)
sir = lambda N, nn=3.7: dB(sqrt(3 * N) ** nn / 6)
s120f = lambda N, nn=3.7: dB(1 / (sqrt(3 * N) ** -nn + (sqrt(3 * N) + 0.7) ** -nn))
c(q, 'N = 7 只有 16.7 dB', 16.7, sir(7)); c(q, 'N = 9 为 18.7 dB', 18.7, sir(9))
c(q, '720/9 = 80', 80, 720 / 9, 0)
ar = 3 * sqrt(3) / 2
c(q, '2.598 × 1² = 2.598', 2.598, ar)
c(q, '2.598 × 2000 = 5196', 5196, ar * 2000, 0.5); c(q, '5196 × 0.03 = 155.9 E', 155.9, ar * 2000 * 0.03)
A80 = Aof(80, 0.01)
c(q, '能承载 A ≈ 65.4 E', 65.4, A80)
c(q, '阻塞率约 49%', 0.49, erlB(ar * 2000 * 0.03, 80))
area = A80 / 60
c(q, '65.4/(2000 × 0.03) = 1.09 km²', 1.09, area)
c(q, 'R = √(1.09/2.598) ≈ 0.648 km', 0.648, sqrt(area / ar))
c(q, '155.9/1.09 ≈ 144', 144, ceil(60 * ar / area), 0)
c(q, '约 2.4 倍基站', 2.4, ceil(60 * ar / area) / 60)
c(q, 'Q = 3 → 16.0 dB', 16.0, s120f(3)); c(q, 'Q = √12 = 3.46 → 18.2 dB', 18.2, s120f(4)); c(q, '3.46', 3.46, sqrt(12))
c(q, '720/4 = 180', 180, 720 / 4, 0); c(q, '每扇区 60 条', 60, 180 / 3, 0)
c(q, '90/4 = 22.5', 22.5, 90 / 4); c(q, '7.5 × 8 = 60', 60, 7.5 * 8, 0)
A60 = Aof(60, 0.01)
c(q, 'A ≈ 46.9 E/扇区', 46.9, A60); c(q, '3 × 46.95 = 140.8 E', 46.95, A60); c(q, '= 140.8 E', 140.8, 3 * A60)
tot = 60 * ar * 2000 * 0.03
c(q, '60 × 2.598 = 155.9 km²', 155.9, 60 * ar); c(q, '= 9353 E', 9353, tot, 0.5)
c(q, '9353/140.8 = 66.4 → 67', 66.4, tot / (3 * A60)); c(q, '67 个', 67, ceil(tot / (3 * A60)), 0)
c(q, '半径约 0.95 km', 0.95, sqrt(60 * ar / 67 / ar))
c(q, '需要约 178 个小区', 178, ceil(tot / (Aof(26, 0.01) + 2 * Aof(27, 0.01))), 0)

q = 'y2425s2-q4c'
A56 = Aof(56, 0.02); A72 = Aof(72, 0.02)
c(q, '504/9 = 56', 56, 504 / 9, 0)
c(q, 'A ≈ 45.9 E', 45.9, A56); c(q, '45.9 × (1 − 0.02) = 45.0 E', 45.0, A56 * 0.98)
c(q, '45.9/56 ≈ 0.82', 0.82, A56 / 56); c(q, '45.0/56 ≈ 0.80', 0.80, A56 * 0.98 / 56)
c(q, '2 × 15/60 = 0.5', 0.5, 2 * 15 / 60)
c(q, '45.9/0.5 = 91.8 → 91', 91.8, 45.9 / 0.5, 1e-9); c(q, '→ 91 个用户', 91, floor(A56 / 0.5), 0)
c(q, '92 个人会产生 46 E', 46, 92 * 0.5, 0)
c(q, '504/7 = 72', 72, 504 / 7, 0); c(q, 'A ≈ 61.0 E', 61.0, A72)
c(q, '61.0 × 0.98 = 59.8 E', 59.8, A72 * 0.98)
c(q, '61.0/72 ≈ 0.85', 0.85, A72 / 72); c(q, '按承载 0.83', 0.83, A72 * 0.98 / 72)
c(q, '61.0/0.5 = 122', 122, floor(A72 / 0.5), 0)
c(q, '多 29%', 0.29, 72 / 56 - 1); c(q, '多 33%', 0.33, A72 / A56 - 1)
c(q, '20.85 dB（N = 9）', 20.85, dB(27 ** 2 / 6)); c(q, '18.66 dB（N = 7）', 18.66, dB(21 ** 2 / 6))
c(q, '10 条、1% 时 4.46/10 = 44.6%', 4.46, Aof(10, 0.01), 0.005)
c(q, '多承载 60% 的话务', 0.60, Aof(10, 0.01) / (2 * Aof(5, 0.01)) - 1, 0.05)

nbad = 0
for (q, lit, stated, val, tol) in C:
    if lit not in XPL[q]['zh']:
        bad(f'{q}: literal not found in body: {lit!r}'); nbad += 1; continue
    if abs(stated - val) > tol:
        bad(f'{q}: {lit!r} states {stated}, computed {val:.6g} (tol {tol:g})'); nbad += 1
print(f'\nnumber checks: {len(C)}, failed: {nbad}')
print('NOTES:\n' + NOTES)
if err:
    print('\nERRORS:'); [print(' -', e) for e in err]; sys.exit(1)
print('\nALL OK: %d ids' % len(IDS))
