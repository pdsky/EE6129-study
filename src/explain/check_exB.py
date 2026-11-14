#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Checks for exB.py: structure, allowed HTML, and every number used in the boxes."""
import importlib.util, os, re, sys, cmath
from math import *
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('exB', os.path.join(HERE, 'exB.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
XPL, NOTES = m.XPL, m.NOTES

IDS = ['y2526s1-q1a', 'y2526s1-q1b1', 'y2526s1-q1b2', 'y2526s1-q2a', 'y2526s1-q2b', 'y2526s1-q3a',
       'y2526s1-q3b', 'y2526s1-q3c', 'y2526s1-q4a', 'y2526s1-q4bc', 'y2526s2-q1a', 'y2526s2-q1b1',
       'y2526s2-q1b2', 'y2526s2-q2a', 'y2526s2-q2b', 'y2526s2-q3a', 'y2526s2-q3bc', 'y2526s2-q4a',
       'y2526s2-q4b', 'y2526s2-q4c', 'y2526s2-q4d']
err = []
def bad(msg): err.append(msg)

# ---------------------------------------------------------------- structure
for q in IDS:
    if q not in XPL: bad(f'missing id {q}')
for q in XPL:
    if q not in IDS: bad(f'unexpected id {q}')

ALLOWED = {'h4': set(), 'span': {'st'}, 'p': set(), 'ul': set(), 'ol': set(), 'li': set(), 'b': set(),
           'i': set(), 'sub': set(), 'sup': set(), 'br': set(), 'div': {'calc', 'tw', 'ans', 'tmpl'},
           'table': {'mini'}, 'thead': set(), 'tbody': set(), 'tr': set(), 'th': set(), 'td': set()}
VOID = {'br'}

class P(HTMLParser):
    def __init__(s, qid):
        super().__init__(convert_charrefs=True); s.q = qid; s.stack = []
    def handle_starttag(s, tag, attrs):
        a = dict(attrs)
        if tag not in ALLOWED: bad(f'{s.q}: tag {tag} not allowed'); return
        for k, v in a.items():
            if k == 'class':
                if v not in ALLOWED[tag]: bad(f'{s.q}: class {v} on {tag}')
            elif k == 'lang' and tag == 'div' and a.get('class') == 'tmpl' and v == 'en': pass
            else: bad(f'{s.q}: attribute {k} on {tag}')
        if tag == 'div' and a.get('class') == 'tmpl' and a.get('lang') != 'en': bad(f'{s.q}: tmpl without lang=en')
        if tag == 'span' and (not s.stack or s.stack[-1] != 'h4'): bad(f'{s.q}: span.st outside h4')
        if tag == 'table' and (not s.stack or s.stack[-1] != 'div'): bad(f'{s.q}: table not in div.tw')
        if tag not in VOID: s.stack.append(tag)
    def handle_endtag(s, tag):
        if tag in VOID: return
        if not s.stack or s.stack[-1] != tag: bad(f'{s.q}: unbalanced /{tag}, stack {s.stack[-3:]}'); return
        s.stack.pop()

for q, d in XPL.items():
    t, z = d.get('title', ''), d.get('zh', '')
    if not t.startswith('知识讲解 + 详细解析：'): bad(f'{q}: title prefix')
    if len(t) > 30: bad(f'{q}: title too long ({len(t)})')
    if '<span class="st">知识讲解</span>' not in z: bad(f'{q}: no 知识讲解')
    if '一句话' not in z or '<div class="ans">一句话' not in z: bad(f'{q}: no 一句话')
    if '<div class="tmpl" lang="en">' not in z: bad(f'{q}: no English template')
    for bad_s in ('style=', '<script', '<img', '<a ', 'href', '\\(', '$$', 'MathJax'):
        if bad_s in z: bad(f'{q}: forbidden {bad_s}')
    # every "<" must start a tag
    for mm in re.finditer(r'<', z):
        if not re.match(r'</?[a-z0-9]+[ >/]', z[mm.start():mm.start() + 12]): bad(f'{q}: raw < at {z[mm.start():mm.start()+20]!r}')
    if re.search(r'(?<![a-z0-9"\'/])>', re.sub(r'<[^<>]*>', '', z)): bad(f'{q}: raw > in text')
    if re.search(r'&(?![a-z]+;|#\d+;)', z): bad(f'{q}: raw & in text')
    p = P(q); p.feed(z); p.close()
    if p.stack: bad(f'{q}: unclosed {p.stack}')
    # tmpl may only contain p (and inline)
    for blk in re.findall(r'<div class="tmpl" lang="en">(.*?)</div>', z, re.S):
        if re.search(r'<(div|ul|ol|table|h4)', blk): bad(f'{q}: block element inside tmpl')
    cn = len(re.findall(r'[一-鿿]', z))
    print(f'{q:14s} 汉字 {cn:5d}  chars {len(z):6d}')
if '<' in NOTES or '>' in NOTES: bad('NOTES contains < or >')

# ---------------------------------------------------------------- numbers
def Q(x): return 0.5 * erfc(x / sqrt(2))
def erlB(A, M):
    b = 1.0
    for k in range(1, M + 1): b = A * b / (k + A * b)
    return b
def erlC(A, M):
    B = erlB(A, M); r = A / M
    return B / (1 - r + r * B)
def solve(f, M, p):
    lo, hi = 1e-6, M * 1.5
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid, M) < p: lo = mid
        else: hi = mid
    return lo
lin = lambda d: 10 ** (d / 10); dB = lambda x: 10 * log10(x)

def near(name, val, ref, tol):
    if abs(val - ref) > tol: bad(f'NUM {name}: computed {val:.6g}, text {ref}')
def has(q, s):
    if s not in XPL[q]['zh']: bad(f'TEXT {q}: expected "{s}"')

# s1-q1a
near('Q(2)', Q(2), 0.0228, 5e-5); near('1/sqrt(0.5pi)', 1 / sqrt(0.5 * pi), 0.798, 5e-4)
near('Q(2) table', Q(2), 0.02275, 5e-6); near('gamma_b', 1 / (2 * 0.25), 2, 1e-12)
has('y2526s1-q1a', 'Q(2) ≈ 0.0228'); has('y2526s1-q1a', '0.798')
# s1-q1b1
g = [lin(11), lin(12), lin(13)]; p = [0.2, 0.5, 0.3]
near('12.59', g[0], 12.59, 5e-3); near('15.85', g[1], 15.85, 5e-3); near('19.95', g[2], 19.95, 5e-3)
near('2.518', 0.2 * g[0], 2.518, 5e-4); near('7.924', 0.5 * g[1], 7.924, 5e-4); near('5.986', 0.3 * g[2], 5.986, 5e-4)
gin = sum(a * b for a, b in zip(g, p)); near('gin', gin, 16.43, 5e-3); near('gin dB', dB(gin), 12.16, 5e-3)
near('dB avg', 0.2 * 11 + 0.5 * 12 + 0.3 * 13, 12.1, 1e-9)
near('out', 2 * gin, 32.86, 5e-3); near('out dB', dB(2 * gin), 15.17, 5e-3)
near('log 2e-4', -log10(2e-4), 3.699, 5e-4); near('log gin', log10(gin), 1.216, 5e-4)
d = -log10(2e-4) / log10(gin); near('d', d, 3.04, 5e-3)
near('log out', log10(2 * gin), 1.517, 5e-4); near('d out', -log10(2e-4) / log10(2 * gin), 2.44, 5e-3)
# s1-q1b2
near('det', (1 + 3) * (1 + 1), 8, 0); near('cap', log2(8), log2(4) + log2(2), 1e-12)
# s1-q2a
near('Q(2.17)', Q(1.3 / 0.6), 0.0151, 5e-5); near('Q(1.17)', Q(0.7 / 0.6), 0.1217, 5e-5)
near('1.3/0.6', 1.3 / 0.6, 2.17, 5e-3); near('0.7/0.6', 0.7 / 0.6, 1.17, 5e-3)
pe = 0.5 * (Q(1.3 / 0.6) + Q(0.7 / 0.6)); near('Pe s1q2a', pe, 0.0684, 5e-5)
near('noISI', Q(1 / 0.6), 0.0478, 5e-5)
# ZF example: (1+0.3z)(1-0.3z+0.09z^2) = 1 + 0.027 z^3
prod = [0] * 4
for i, a in enumerate([1, 0.3]):
    for j, b in enumerate([1, -0.3, 0.09]): prod[i + j] += a * b
near('ZF z1', prod[1], 0, 1e-12); near('ZF z2', prod[2], 0, 1e-12); near('ZF z3', prod[3], 0.027, 1e-12)
near('1.0981', 1 + 0.3 ** 2 + 0.09 ** 2, 1.0981, 1e-9); near('0.395', 0.36 * 1.0981, 0.395, 5e-4)
# s1-q2b
near('500/30', 500 / 30, 16.7, 0.05); near('500/17', 500 / 17, 29.4, 0.05); near('500/16', 500 / 16, 31.25, 1e-9)
near('R_eff', 100 / 110e-6 / 1e3, 909, 0.5); near('raw', 100 / 100e-6, 1e6, 1e-6)
near('eff%', 100 / 110 * 100, 90.9, 0.05); near('GI loss', dB(110 / 100), 0.41, 5e-3)
# orthogonality integral numerically
T = 1.0
for k in range(4):
    s = sum(cmath.exp(2j * pi * (k - 1) * (t + 0.5) / 4000) for t in range(4000)) / 4000
    near(f'orth k={k}', abs(s), 1.0 if k == 1 else 0.0, 1e-9)
# s1-q3a
Ac = 3 * sqrt(3) / 2 * 4; near('Ac', Ac, 10.39, 5e-3); near('2.598', 3 * sqrt(3) / 2, 2.598, 5e-4)
near('cells', 1500 / Ac, 144.3, 0.05); near('ceil', ceil(1500 / Ac), 145, 0)
ch = (25000 - 40) / 30; near('ch', ch, 832, 1e-9); near('814/9', 814 / 9, 90.4, 0.05); near('832/9', ch / 9, 92.44, 5e-3)
near('den', 0.03 * Ac * 9, 2.806, 5e-4); near('eta', 1 / (0.03 * Ac * 9), 0.356, 5e-4)
tot = ch / 9 * 1500 / Ac; near('tot ch', tot, 13344, 1); near('eta alt', tot / (25 * 1500), 0.356, 5e-4)
near('eta slide', (25 / 0.03) / (25 * Ac * 9), 0.356, 5e-4)
# s1-q3b
near('1001/9', 1001 / 9, 111.2, 0.05)
a110, a115, a111 = solve(erlC, 110, .05), solve(erlC, 115, .05), solve(erlC, 111, .05)
near('A110', a110, 92.5, 0.05); near('A115', a115, 97.1, 0.05)
near('interp111', 92.5 + (97.1 - 92.5) / 5, 93.42, 1e-9); near('A111 exact', a111, 93.4, 0.05)
near('users', a111 / 0.03, 3114, 1); near('per km2', a111 / 0.03 / 4, 779, 0.5)
near('users 93.4', 93.4 / 0.03, 3114, 1.5)
near('H', 0.03 / 1.5 * 3600, 72, 1e-9); near('108 s', 1.5 * 72, 108, 1e-9); near('108/3600', 108 / 3600, 0.03, 1e-12)
near('875', 3500 / 4, 875, 0); near('2.72M', 3114 * 875 / 1e6, 2.72, 0.005)
# s1-q3c
near('210/7', 210 / 7, 30, 0)
# s2-q1a
near('LCR', 40 / 10, 4, 0); near('per fade', 20 / 5, 4, 0); near('err/s', 16, 4 * 4, 0)
near('frac', 4 * 0.02, 0.08, 1e-12); near('sym/s', 1 / 5e-3, 200, 1e-9); near('200*0.08', 200 * 0.08, 16, 1e-9)
gR = lin(25); near('316.2', gR, 316.2, 0.05); near('ln', -log(1 - 0.005), 0.005013, 5e-7)
gm = gR * -log(1 - 0.005); near('gmin', gm, 1.585, 5e-4); near('gmin dB', dB(gm), 2.0, 5e-3)
near('FM', 25 - dB(gm), 23.0, 5e-3); near('FM2', dB(1 / -log(1 - 0.005)), 23.0, 5e-3)
near('C/B', log2(1 + gm), 1.37, 5e-3)
# s2-q1b1
near('g', 10 ** 0.3, 1.995, 5e-4); near('Pe', lin(12) ** -3.7, 3.63e-5, 5e-8)
near('-4.44', -1.2 * 3.7, -4.44, 1e-12); near('10^0.56', 10 ** 0.56, 3.63, 5e-3)
near('Pe out', lin(15) ** -3.7, 2.8e-6, 5e-8); near('31.62', lin(15), 31.62, 5e-3)
near('d=2', lin(12) ** -2, 4e-3, 5e-5); near('SD g M=4', 1 + 1 / 2 + 1 / 3 + 1 / 4, 2.08, 5e-3)
near('SD g dB', dB(1 + 1 / 2 + 1 / 3 + 1 / 4), 3.2, 0.05)
# s2-q1b2
near('24 gains', 6 * 4, 24, 0); near('norm', 0.5 + 1.5, 2, 0)
# s2-q2a
near('noise', 0.25 * 2.56, 0.64, 1e-12); near('sigma', sqrt(0.64), 0.8, 1e-12)
near('Q1.5', Q(1.5), 0.0668, 5e-5); near('Q1', Q(1), 0.1587, 5e-5)
near('Pe s2q2a', 0.5 * (Q(1.5) + Q(1)), 0.1127, 5e-5); near('Q1.25', Q(1.25), 0.106, 5e-4); near('Q2', Q(2), 0.023, 5e-4)
# s2-q2b
H = [1 + 0.3 * cmath.exp(-2j * pi * k / 4) for k in range(1, 5)]
for hk, ref in zip(H, [1 - 0.3j, 0.7, 1 + 0.3j, 1.3]): near(f'H {ref}', abs(hk - ref), 0, 1e-12)
near('|H1|', abs(H[0]), 1.044, 5e-4); near('conj', abs(H[2] - H[0].conjugate()), 0, 1e-12)
near('8us', 4 * 2, 8, 0); near('28', 8 + 20, 28, 0); near('log3.5', log10(3.5), 0.544, 5e-4)
near('loss', dB(28 / 8), 5.44, 5e-3); near('71%', 20 / 28 * 100, 71, 0.5); near('wrong', dB(22 / 2), dB(11), 1e-12)
# s2-q3a
near('153', 1071 / 7, 153, 0); near('42', 7 * 6, 42, 0); near('50', 2100 / 42, 50, 0); near('350', 50 * 7, 350, 0)
near('cap', 1071 * 50, 53550, 0); near('cap2', 153 * 350, 53550, 0); near('2100/6', 2100 / 6, 350, 0)
# s2-q3bc
a150, a155, a153 = solve(erlC, 150, .05), solve(erlC, 155, .05), solve(erlC, 153, .05)
near('A150', a150, 129.5, 0.05); near('A155', a155, 134.1, 0.05)
near('interp153', 129.5 + 3 / 5 * (134.1 - 129.5), 132.26, 1e-9); near('2.76', 3 / 5 * 4.6, 2.76, 1e-9)
near('A153', a153, 132.2, 0.05); near('users', a153 / 0.03, 4408, 1); near('per km2 s2', a153 / 0.03 / 6, 735, 0.5)
near('132.2/0.03', 132.2 / 0.03, 4408, 2); near('H s2', 0.03 / 1.2 * 3600, 90, 1e-9); near('0.025', 0.03 / 1.2, 0.025, 1e-12)
mm_, r = 3, 2.0
P0 = 1 / (sum(r ** k / factorial(k) for k in range(mm_)) + r ** mm_ / factorial(mm_) / (1 - r / mm_))
near('P0', P0, 1 / 9, 1e-12); near('P0 terms', 1 + 2 + 2 + (8 / 6) * 3, 9, 1e-12)
Pk = [P0 * r ** k / factorial(k) if k <= mm_ else P0 * r ** k / (factorial(mm_) * mm_ ** (k - mm_)) for k in range(500)]
near('sum Pk', sum(Pk), 1, 1e-9); near('Pwait', sum(Pk[mm_:]), 4 / 9, 1e-9); near('erlC(2,3)', erlC(2, 3), 4 / 9, 1e-9)
near('0.444', 4 / 9, 0.444, 5e-4)
# recursion check P_k = (rho/k)P_{k-1} (k<=m) and (rho/m)P_{k-1} (k>=m)
for k in range(1, 20):
    f = r / k if k <= mm_ else r / mm_
    near(f'rec {k}', Pk[k], f * Pk[k - 1], 1e-12)

# text spot checks: key results appear in the boxes
for q, s in [('y2526s1-q1b1', '16.43'), ('y2526s1-q1b1', '32.86'), ('y2526s1-q1b1', '3.04'),
             ('y2526s1-q2a', '0.0684'), ('y2526s1-q2a', '0.0151'), ('y2526s1-q2a', '0.1217'), ('y2526s1-q2a', '0.395'),
             ('y2526s1-q2b', 'N<sub>min</sub> = 17'), ('y2526s1-q2b', '909 kbit/s'), ('y2526s1-q2b', '0.41 dB'),
             ('y2526s1-q3a', '832'), ('y2526s1-q3a', '0.356'), ('y2526s1-q3a', '145'), ('y2526s1-q3a', '13 344'),
             ('y2526s1-q3b', '93.4'), ('y2526s1-q3b', '779'), ('y2526s1-q3b', '72 秒'),
             ('y2526s2-q1a', '16 个/秒'), ('y2526s2-q1a', '1.585'), ('y2526s2-q1a', '23.0 dB'), ('y2526s2-q1a', '1.37'),
             ('y2526s2-q1b1', '3.6×10⁻⁵'), ('y2526s2-q1b1', '2.8×10⁻⁶'), ('y2526s2-q1b1', '2.08'),
             ('y2526s2-q1b2', '6×4'), ('y2526s2-q2a', '0.64'), ('y2526s2-q2a', '0.1127'), ('y2526s2-q2a', '0.106'),
             ('y2526s2-q2b', '1.044'), ('y2526s2-q2b', '5.44 dB'), ('y2526s2-q2b', '28 µs'),
             ('y2526s2-q3a', '53 550'), ('y2526s2-q3bc', '132.2'), ('y2526s2-q3bc', '735'), ('y2526s2-q3bc', '90 s'),
             ('y2526s2-q3bc', '4/9')]:
    has(q, s)

print()
if err:
    print('FAILED:'); [print('  ' + e) for e in err]; sys.exit(1)
print(f'OK: {len(XPL)} ids, structure + HTML + numbers all checked.')
