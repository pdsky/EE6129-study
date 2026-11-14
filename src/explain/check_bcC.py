# -*- coding: utf-8 -*-
# Check bcC.py: structure, HTML, and every number used in the boxes.  Run with /usr/bin/python3.
import importlib.util, math, re, sys, os
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('bcC', os.path.join(HERE, 'bcC.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
XPL = m.XPL
ok = True
def bad(msg):
    global ok; ok = False; print('FAIL', msg)

# ---- ids / structure
ids = ['c%d' % i for i in range(1, 24)]
for i in ids:
    if i not in XPL: bad('missing ' + i)
extra = set(XPL) - set(ids)
if extra: bad('extra ids %s' % extra)

ALLOWED = {'h4', 'span', 'p', 'ul', 'ol', 'li', 'b', 'i', 'sub', 'sup', 'br', 'div', 'table', 'thead', 'tbody', 'tr', 'th', 'td'}
VOID = {'br'}
class Chk(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack = []; s.err = []
    def handle_starttag(s, t, a):
        a = dict(a)
        if t not in ALLOWED: s.err.append('tag ' + t)
        if 'style' in a: s.err.append('inline style')
        if t == 'span' and a.get('class') != 'st': s.err.append('span class')
        if t == 'div' and a.get('class') not in ('calc', 'tw', 'ans', 'tmpl'): s.err.append('div class %s' % a.get('class'))
        if t == 'div' and a.get('class') == 'tmpl' and a.get('lang') != 'en': s.err.append('tmpl lang')
        if t == 'table' and a.get('class') != 'mini': s.err.append('table class')
        if t not in VOID: s.stack.append(t)
    def handle_endtag(s, t):
        if t in VOID: return
        if not s.stack or s.stack[-1] != t: s.err.append('unbalanced /%s (stack %s)' % (t, s.stack[-3:]))
        else: s.stack.pop()

MCQ = {'c1', 'c6', 'c8', 'c9', 'c12', 'c14', 'c15', 'c19', 'c22'}
for k in ids:
    v = XPL.get(k)
    if not v: continue
    t, z = v['title'], v['zh']
    if not t.startswith('知识讲解 + 详细解析：'): bad(k + ' title prefix')
    if len(t) > 30: bad('%s title too long (%d)' % (k, len(t)))
    for need in ('知识讲解', '一句话', 'class="ans"'):
        if need not in z: bad('%s lacks %s' % (k, need))
    if k in MCQ and '逐项分析' not in z: bad(k + ' MCQ lacks 逐项分析')
    if k not in MCQ and 'class="tmpl" lang="en"' not in z: bad(k + ' lacks English template')
    if '$' in z or '\\(' in z or '<script' in z or '<img' in z or '<a ' in z: bad(k + ' forbidden content')
    c = Chk(); c.feed(z); c.close()
    if c.err: bad('%s html: %s' % (k, c.err))
    if c.stack: bad('%s unclosed %s' % (k, c.stack))
    # stray < or > in text
    txt = re.sub(r'<[^<>]+>', '', z)
    if '<' in txt or '>' in txt: bad(k + ' raw < or > in text')
    n = len(re.sub(r'\s', '', re.sub(r'<[^>]+>', '', z)))
    print('%-4s %5d chars  %s' % (k, n, t))

# ---- numbers
def eq(name, got, want, tol):
    if abs(got - want) > tol: bad('%s: computed %.6g, box says %s' % (name, got, want))
R, h, c = 6370.0, 35863.0, 3e5
mu = 398600.0
lg = math.log10
# c1
eq('c1 GEO radius', R + h, 42233, 0)
# c4
eq('c4 path', 2 * h, 71726, 0)
eq('c4 delay', 2 * h / c, 0.239, 0.0005)
b10 = math.degrees(math.acos(R * math.cos(math.radians(10)) / (R + h))) - 10
d10 = math.sqrt(R**2 + (R + h)**2 - 2 * R * (R + h) * math.cos(math.radians(b10)))
eq('c4 slant 10deg', d10, 40660, 5)
eq('c4 delay edge', 2 * d10 / c, 0.27, 0.005)
eq('c4 two hops', 4 * h / c, 0.48, 0.005)
eq('c4 one-way only', h / c, 0.12, 0.005)
# c5 / c3
cb = R / (R + h)
eq('c5 cos', cb, 0.1508, 0.00005)
b0 = math.degrees(math.acos(cb))
eq('c5 beta', b0, 81.3, 0.05)
eq('c5 beta rad', math.radians(b0), 1.419, 0.0005)
eq('c5 diam', 2 * math.radians(b0) * R, 18000, 100)
eq('c3 cos10', R * math.cos(math.radians(10)) / (R + h), 0.1485, 0.00005)
eq('c3 cos 10 deg', math.cos(math.radians(10)), 0.9848, 0.00005)
eq('c3 theta+beta', b10 + 10, 81.46, 0.005)
eq('c3 beta10', b10, 71.46, 0.005)
eq('c3 diam10', 2 * math.radians(b10) * R, 15900, 20)
eq('c5 cap 0deg %', (1 - cb) / 2 * 100, 42, 0.6)
eq('c5 cap 10deg %', (1 - math.cos(math.radians(b10))) / 2 * 100, 34, 0.6)
eq('c5 wrong R/h', R / h, 0.178, 0.0005)
# c7 / c9 Kepler, Doppler, LEO-GEO difference
eq('c9 T 500', 2 * math.pi * math.sqrt((R + 500)**3 / mu) / 3600, 1.57, 0.005)
eq('c9 v 500', math.sqrt(mu / (R + 500)), 7.6, 0.05)
eq('c7 v 1000', math.sqrt(mu / (R + 1000)), 7.35, 0.005)
eq('c7 doppler kHz', 2e9 * 7.35 / 3e5 / 1e3, 49, 0.1)
eq('c7 LEO-GEO dB', 20 * lg(h / 1000), 31.1, 0.05)
# c10 / c12
eq('c10 Ku-C dB', 20 * lg(12 / 4), 9.5, 0.05)
eq('c12 sin5', math.sin(math.radians(5)), 0.0872, 0.00005)
eq('c12 ratio', math.sin(math.radians(30)) / math.sin(math.radians(5)), 5.7, 0.05)
# c11
eq('c11 log4000', lg(4000), 3.602, 0.0005)
eq('c11 log35863', lg(h), 4.555, 0.0005)
eq('c11 f term', 20 * lg(4000), 72.04, 0.005)
eq('c11 d term', 20 * lg(h), 91.09, 0.005)
L = 32.44 + 20 * lg(4000) + 20 * lg(h)
eq('c11 L', L, 195.6, 0.05)
eq('c11 L const32', 32 + 20 * lg(4000) + 20 * lg(h), 195.1, 0.05)
eq('c11 1GHz', 32.44 + 20 * lg(1000) + 20 * lg(h), 183.5, 0.05)
eq('c11 LEO', 32.44 + 20 * lg(4000) + 20 * lg(1000), 164.5, 0.05)
eq('c11 GHz mistake', 20 * lg(4), 12.04, 0.005)
# c14 antenna gain
eq('c14 10x diameter dB', 10 * lg(10**2), 20, 0)
# c15 wavelength
eq('c15 lambda 12.5', 3e8 / 12.5e9 * 100, 2.4, 0.005)
eq('c15 lambda 18', 3e8 / 18e9 * 100, 1.7, 0.05)
# c16
eq('c16 usable', 40 - 4, 36, 0)
eq('c16 guard %', 4 / 40 * 100, 10, 0)
eq('c16 total', 24 * 40, 960, 0)
eq('c16 ratio', 960 / 500, 1.9, 0.05)
eq('c16 12ch', 12 * 40, 480, 0)
eq('c16 wrong split', 500 / 24, 20.8, 0.05)
# c18
eq('c18', 50 - 1, 49, 0)
# c19
ov = 20 + 10 * (10 + 2)
eq('c19 overhead', ov, 140, 0)
eq('c19 TDMA eff %', (1 - ov / 2000) * 100, 93, 0)
eq('c19 FDMA eff %', 36 / 40 * 100, 90, 0)
# c20
eq('c20 3!', math.factorial(3), 6, 0)
eq('c20 4!', math.factorial(4), 24, 0)
eq('c20 5!', math.factorial(5), 120, 0)
eq('c20 N^2', 5**2, 25, 0)
eq('c20 N(N-1)', 5 * 4, 20, 0)

print('ALL OK' if ok else 'ERRORS FOUND')
sys.exit(0 if ok else 1)
