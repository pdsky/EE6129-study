#!/usr/bin/python3
"""Independent re-check of quizsum/frag_fadetype.html (t8: delay spread, flat vs frequency-selective;
t9: Doppler, fast vs slow, combined fading type). Written separately from check_fadetype.py.

Part A recomputes every number from the question data by other routes than the writer's script:
  * discrete delay profiles: central moments sum (tau-mu)^2 P / sum P, cross-checked against E[tau^2]-mu^2;
  * continuous profiles: midpoint-rule integration (no closed form), compared with a/2 and a/sqrt(12);
  * Doppler: both v/lambda and v f_c / c; speeds converted with /3.6 and back with *3.6.
Every display string used in the fragment is printed with a label (section · place · quantity).

Part B checks the fragment itself:
  1. every numeric token in the fragment text is explained (computed in part A, a question input, or a
     structural label such as a year, question number or slide page) -> list of UNEXPLAINED tokens;
  2. every display string from part A appears in the fragment;
  3. HTML: balanced tags (html.parser), no <style>/<script>/<html>/<head>/<body>, section/class structure;
  4. TeX: no raw < or > (and no &lt; / &gt;) inside \\( \\) or \\[ \\];
  5. sources: mock/practice labels and their numbers (prac_8.html, prac_1.html), past-final numbers
     (src/exams/data_*.py), lecturer claims (src/teacher/notes.py), formula status badges (quiz_marks.py).
stdlib only (Q via statistics.NormalDist is not needed for t8/t9). Run: /usr/bin/python3 _verify_fadetype.py
"""
import math
import pathlib
import re
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent
FRAG = HERE / 'frag_fadetype.html'
C = 3.0e8

PROBLEMS = []
D = {}          # label -> display string that must appear in the fragment
ALLOWED = {}    # numeric token -> reasons


def bad(msg):
    PROBLEMS.append(msg)
    print('  !! ' + msg)


def allow(tok, why):
    ALLOWED.setdefault(tok, set()).add(why)


def put(label, s):
    """record a display string produced here; it must appear in the fragment and explains its tokens"""
    D[label] = s
    print(f'  {label:<62} {s}')
    for t in re.findall(r'\d+(?:\.\d+)?(?:×10\^-?\d+)?', s):
        allow(t, label)


def inp(label, *toks):
    """question inputs (given data, not computed)"""
    print(f'  [input] {label:<54} {" | ".join(toks)}')
    for t in toks:
        allow(t, 'input: ' + label)


def lin(db):
    return 10.0 ** (db / 10.0)


def moments(taus, w):
    """weighted mean, second moment and CENTRAL variance (independent of E[t^2]-mu^2)"""
    s = math.fsum(w)
    mu = math.fsum(t * x for t, x in zip(taus, w)) / s
    e2 = math.fsum(t * t * x for t, x in zip(taus, w)) / s
    var = math.fsum((t - mu) ** 2 * x for t, x in zip(taus, w)) / s
    assert abs(var - (e2 - mu * mu)) < 1e-12, (var, e2 - mu * mu)
    return s, mu, e2, var, math.sqrt(var)


def cont_moments(h, a, n=200000):
    """midpoint-rule integration of a flat profile of height h on [0, a]"""
    dt = a / n
    ts = [(i + 0.5) * dt for i in range(n)]
    area = math.fsum(h * dt for _ in ts)
    mu = math.fsum(h * t * dt for t in ts) / area
    e2 = math.fsum(h * t * t * dt for t in ts) / area
    var = math.fsum(h * (t - mu) ** 2 * dt for t in ts) / area
    return area, mu, e2, var, math.sqrt(var)


def sci(x, nd=3):
    m, e = f'{x:.{nd}e}'.split('e')
    return f'{m}×10^{int(e)}'


print('=' * 100)
print('PART A  independent recomputation')
print('=' * 100)

# ---------------------------------------------------------------- t8 formula cards
print('\n--- t8 formula cards')
for d in (0, -3, -6, -10):
    print(f'  {d:>4} dB -> {lin(d):.6f}')
put('t8 dB card: 0 dB', f'{lin(0):g}')
put('t8 dB card: -3 dB', f'{lin(-3):.4f}')
put('t8 dB card: -6 dB', f'{lin(-6):.4f}')
put('t8 dB card: -10 dB', f'{lin(-10):g}')
put('t8 rms card: sqrt(12)', f'{math.sqrt(12):.3f}')
allow('12', 'sqrt(12) in sigma = a/sqrt(12)')
put('t8 flat card: lecturer example ratio (notes.py 2.4)', '0.15')
# 2025-26 S1 Q2(b)(i): subcarrier bandwidth 500/N < B_C = 30 kHz
Bav, Bc_s1 = 500.0, 30.0
N_real = Bav / Bc_s1
N_min = next(n for n in range(1, 1000) if Bav / n < Bc_s1)
put('t8 B_C card: 2025-26 S1 Q2(b)(i) 500/30', f'{N_real:.2f}')
put('t8 B_C card: N_min (first N with 500/N < 30)', f'{N_min}')
put('t8 B_C card: subcarrier bandwidth 500/N_min (kHz)', f'{Bav / N_min:.1f}')
assert Bav / N_min < Bc_s1 and Bav / (N_min - 1) >= Bc_s1
inp('2025-26 S1 Q2(b): bandwidth 500 kHz, B_C 30 kHz, max delay 10 us', '500', '30', '10')

# ---------------------------------------------------------------- t8 table 1 : Practice 1 Q3
print('\n--- t8 table 1 · Practice 1 Q3 (P_r = 1 on 0..10 us)')
area, mu, e2, var, sg = cont_moments(1.0, 10.0)
print(f'  numeric: area {area:.6f} mu {mu:.6f} E2 {e2:.6f} var {var:.6f} sigma {sg:.6f}')
assert abs(mu - 5) < 1e-9 and abs(sg - 10 / math.sqrt(12)) < 1e-6
inp('P1Q3: profile height 1 on 0..10 us; a/2, a^2/3', '1', '0', '10', '2', '3', '100')
put('t8 T1 P1Q3 mu (us)', f'{mu:.0f}')
put('t8 T1 P1Q3 E[tau^2] (us^2)', f'{e2:.2f}')
put('t8 T1 P1Q3 var (us^2)', f'{var:.2f}')
put('t8 T1 P1Q3 sigma (us)', f'{sg:.2f}')
put('t8 T1 P1Q3 10 sigma (us)', f'{10 * sg:.1f}')
put('t8 T1 P1Q3 Rs max = 1/(10 sigma) (ksps)', f'{1 / (10 * sg * 1e-6) / 1e3:.1f}')
put('t8 trap: P1Q3 denominator (area)', f'{area:.0f}')
print('  official answer (prac_1.html / Practice Answers pdf): 5 us, 2.89 us, 34.6 ksps')

# ---------------------------------------------------------------- t8 table 1 : mock A Q3
print('\n--- t8 table 1 · 模拟 A·Q3 (0/1/3 us, 0/-3/-6 dB, 50 ksps, 1.8 GHz, 72 km/h)')
taus = [0.0, 1.0, 3.0]
w = [lin(0), lin(-3), lin(-6)]
s, mu, e2, var, sg = moments(taus, w)
m1, m2 = mu * s, e2 * s
print(f'  weights {[round(x, 6) for x in w]} sum {s:.6f}; sum tP {m1:.6f}; sum t2P {m2:.6f}')
print(f'  mu {mu:.6f} E2 {e2:.6f} central var {var:.6f} sigma {sg:.6f}')
inp('mock A Q3: delays 0/1/3 us, 0/-3/-6 dB, 50 ksps, 1.8 GHz, 72 km/h', '0', '1', '3', '6', '50', '1.8', '72')
put('t8 T1 mockA sum of weights', f'{s:.3f}')
put('t8 T1 mockA sum tau P', f'{m1:.3f}')
put('t8 T1 mockA mu (us)', f'{mu:.3f}')
put('t8 T1 mockA tau^2 of 3 us', f'{3 * 3:g}')
put('t8 T1 mockA sum tau^2 P', f'{m2:.3f}')
put('t8 T1 mockA E[tau^2]', f'{e2:.3f}')
put('t8 T1 mockA var (shown sqrt argument)', f'{e2 - round(mu, 3) ** 2:.3f}')
assert f'{var:.3f}' == f'{e2 - round(mu, 3) ** 2:.3f}'
put('t8 T1 mockA sigma (us)', f'{sg:.2f}')
Ts = 1 / 50e3
put('t8 T1 mockA Ts (us)', f'{Ts * 1e6:.0f}')
put('t8 T1 mockA sigma/Ts', f'{sg * 1e-6 / Ts:.3f}')
put('t8 T1 mockA Rs max 0.1/sigma (ksps)', f'{0.1 / (sg * 1e-6) / 1e3:.1f}')
put('t8 trap: mockA delay span (us)', f'{max(taus) - min(taus):g}')

# ---------------------------------------------------------------- t8 table 2
print('\n--- t8 table 2 · 2023-24 S2 Q1(a)(iii) (Ts 1 ms, sigma 0.01 ms, time-invariant)')
inp('2023-24 Q1(a)(iii): Ts 1 ms, sigma 0.01 ms', '1', '0.01')
put('t8 T2 2324 sigma/Ts', f'{0.01 / 1:.2f}')
print('\n--- t8 table 2 / t9 table 2 · 模拟 C·Q2(a) (50 ksps, B_s ~ 50 kHz, B_C 200 kHz, f_m 100 Hz)')
inp('mock C Q2(a): 50 ksps, B_C 200 kHz, f_m 100 Hz', '50', '200', '100')
Bs, Bc, fm = 50e3, 200e3, 100.0
put('t8 T2 mockC Bs/Bc', f'{Bs / Bc:.2f}')
put('t9 T2 mockC Bs/B_D', f'{Bs / fm:.0f}')
put('t9 T2 mockC Tc = 1/fm (ms)', f'{1 / fm * 1e3:.0f}')
put('t9 T2 mockC Ts (us)', f'{1 / Bs * 1e6:.0f}')
print(f'  Tc/Ts = {(1 / fm) / (1 / Bs):.0f} (not shown)')
print('  practice page + verify_mock.py: Bs < Bc -> flat; B_D << Bs -> slow  => flat, slow (no "borderline")')

# ---------------------------------------------------------------- t8 example 1
print('\n--- t8 例1 (0/2/5 us, -80/-84/-90 dBm; 100 ksps)')
taus = [0.0, 2.0, 5.0]
dbm = [-80.0, -84.0, -90.0]
mw = [lin(x) for x in dbm]
inp('t8 ex1: delays 0/2/5 us, -80/-84/-90 dBm, 100 ksps; relative 0/-4/-10 dB',
    '0', '2', '5', '80', '84', '90', '100', '4', '10')
for x, lab in zip(mw, ('-80', '-84', '-90')):
    put(f't8 ex1 {lab} dBm in mW', sci(x, 3))
rel = [x / mw[0] for x in mw]
put('t8 ex1 weight -4 dB', f'{rel[1]:.4f}')
put('t8 ex1 weight -10 dB', f'{rel[2]:.1f}')
s, mu, e2, var, sg = moments(taus, rel)
s_abs, mu_abs, _, _, sg_abs = moments(taus, mw)
assert abs(mu - mu_abs) < 1e-12 and abs(sg - sg_abs) < 1e-12      # absolute mW weights give the same answer
put('t8 ex1 sum of weights', f'{s:.3f}')
put('t8 ex1 sum tau P', f'{mu * s:.3f}')
put('t8 ex1 mu (us, 4 s.f. kept for squaring)', f'{mu:.4f}')
put('t8 ex1 mu (us)', f'{mu:.3f}')
assert f'{round(mu * s, 3) / round(s, 3):.4f}' == f'{mu:.4f}'          # 1.296/1.498 also gives 0.8652
put('t8 ex1 tau^2 of 2 us and 5 us', f'{2 * 2:g}, {5 * 5:g}')
put('t8 ex1 sum tau^2 P', f'{e2 * s:.3f}')
put('t8 ex1 E[tau^2]', f'{e2:.3f}')
mu4 = round(mu, 4)
put('t8 ex1 mu^2 from mu = 0.8652', f'{mu4 ** 2:.4f}')
put('t8 ex1 var', f'{var:.3f}')
assert f'{round(e2, 3) - round(mu4 ** 2, 4):.3f}' == f'{var:.3f}'        # 2.732 - 0.7486 = 1.983 (shown chain)
print(f'  (0.865^2 = {0.865 ** 2:.4f} -> the old text "0.865^2 = 0.749" was inconsistent)')
put('t8 ex1 sigma (us)', f'{sg:.2f}')
put('t8 ex1 10 sigma (us, 3 s.f.)', f'{10 * sg:.1f}')
put('t8 ex1 10 sigma (us, 4 s.f.)', f'{10 * sg:.2f}')
put('t8 ex1 Rs max (ksps)', f'{1 / (10 * sg * 1e-6) / 1e3:.1f}')
Ts = 1 / 100e3
put('t8 ex1 Ts at 100 ksps (us)', f'{Ts * 1e6:.0f}')
put('t8 ex1 sigma/Ts at 100 ksps', f'{sg * 1e-6 / Ts:.3f}')
r = sg * 1e-6 / Ts
print(f'  0.1 < {r:.3f} << 1 -> grey zone: "cannot be taken as flat" (notes.py 2.4)')
assert 0.1 < r < 0.2

# ---------------------------------------------------------------- t8 example 2
print('\n--- t8 例2 (P_r = 2 on 0..4 us; 50 ksps)')
area, mu, e2, var, sg = cont_moments(2.0, 4.0)
print(f'  numeric: area {area:.6f} mu {mu:.6f} E2 {e2:.6f} var {var:.6f} sigma {sg:.6f}')
assert abs(sg - 4 / math.sqrt(12)) < 1e-6
inp('t8 ex2: height 2 on 0..4 us, 50 ksps; a/2, a^2/3 = 16/3', '2', '0', '4', '50', '16', '3')
put('t8 ex2 area (denominator)', f'{area:.0f}')
put('t8 ex2 mu (us)', f'{mu:.0f}')
put('t8 ex2 E[tau^2]', f'{e2:.3f}')
put('t8 ex2 var', f'{var:.3f}')
put('t8 ex2 sigma (us)', f'{sg:.3f}')
Ts = 1 / 50e3
put('t8 ex2 Ts (us)', f'{Ts * 1e6:.0f}')
put('t8 ex2 sigma/Ts', f'{sg * 1e-6 / Ts:.4f}')
put('t8 ex2 Rs max 0.1/sigma (ksps)', f'{0.1 / (sg * 1e-6) / 1e3:.1f}')
put('t8 ex2 B_C ~ 1/sigma (kHz)', f'{1 / (sg * 1e-6) / 1e3:.0f}')
assert f'{50e3 / (1 / (sg * 1e-6)):.4f}' == f'{sg * 1e-6 / Ts:.4f}'

# ---------------------------------------------------------------- t8 example 3
print('\n--- t8 例3 (B_C = 150 kHz given; 10 ksps, 1 Msps)')
inp('t8 ex3: B_C 150 kHz, 10 ksps, 1 Msps', '150', '10', '1')
put('t8 ex3 (a) Bs/Bc', f'{10 / 150:.4f}')
put('t8 ex3 (a) Bc/Bs', f'{150 / 10:.0f}')
put('t8 ex3 (b) Bs/Bc', f'{1000 / 150:.2f}')
put('t8 ex3 (c) Rs max (ksps)', f'{150:.0f}')

# ---------------------------------------------------------------- t8 traps
print('\n--- t8 traps')
inp('t8 trap: 4-QAM, 200 kbit/s', '200')
put('t8 trap: 200 kbit/s / log2(4) (ksps)', f'{200 / math.log2(4):.0f}')

# ---------------------------------------------------------------- t9 table 1
print('\n--- t9 table 1 · 专项·Q3(e)(f) (10 ksps, 2 GHz, sigma 2 us, 54 km/h)')
inp('专项 Q3: 10 ksps, 2 GHz, sigma 2 us, 54 km/h, c = 3x10^8', '10', '2', '54', '3.6', '2×10^9', '3×10^8')
Rs, fc, sgm, v = 10e3, 2e9, 2e-6, 54 / 3.6
Ts = 1 / Rs
lam = C / fc
fm = v / lam
assert abs(fm - v * fc / C) < 1e-9
put('t9 T1 focused Ts (us)', f'{Ts * 1e6:.0f}')
put('t9 T1 focused sigma/Ts', f'{sgm / Ts:.2f}')
put('t9 T1 focused v (m/s)', f'{v:.0f}')
put('t9 T1 focused f_m (Hz)', f'{fm:.0f}')
put('t9 T1 focused Tc (ms)', f'{1 / fm * 1e3:.0f}')
put('t9 T1 focused Tc/Ts', f'{(1 / fm) / Ts:.0f}')
put('t9 trap: 54 used as m/s -> f_m (Hz)', f'{54 * fc / C:.0f}')
put('t9 trap: factor', f'{(54 * fc / C) / fm:.1f}')
put('t9 trap: 72 km/h in m/s', f'{72 / 3.6:.0f}')
print('\n--- t9 table 1 · 2023-24 Q1(a)(iii): time-invariant -> f_m = 0, Tc -> inf; 0.01 < 0.1 -> flat, slow')
allow('0', 'f_m = 0 / theta = 0 / tau = 0')

# ---------------------------------------------------------------- t9 example 1
print('\n--- t9 例1 (360 km/h, lambda 5 cm, 1 ksps, sigma 1 us)')
inp('t9 ex1: 360 km/h, lambda 5 cm, 1 ksps, sigma 1 us', '360', '5', '1')
v = 360 / 3.6
lam = 0.05
fm = v / lam
fc = C / lam
assert abs(v * fc / C - fm) < 1e-9
Tc, Ts = 1 / fm, 1 / 1e3
put('t9 ex1 v (m/s)', f'{v:.0f}')
put('t9 ex1 lambda (m)', f'{lam:.2f}')
put('t9 ex1 f_m (Hz)', f'{fm:.0f}')
put('t9 ex1 f_c = c/lambda (GHz)', f'{fc / 1e9:.0f}')
put('t9 ex1 Tc (ms)', f'{Tc * 1e3:.1f}')
put('t9 ex1 Ts (ms)', f'{Ts * 1e3:.0f}')
put('t9 ex1 Ts/Tc', f'{Ts / Tc:.0f}')
put('t9 ex1 sigma/Ts', f'{1e-6 / Ts:.3f}')
put('t9 ex1 Bs (kHz)', f'{1 / Ts / 1e3:.0f}')
put('t9 ex1 B_D (kHz)', f'{fm / 1e3:.0f}')
assert Ts > Tc          # symbol longer than coherence time -> fast

# ---------------------------------------------------------------- t9 example 2
print('\n--- t9 例2 (Tc 5 ms at 900 MHz; 100 ksps)')
inp('t9 ex2: Tc 5 ms, 900 MHz = 9x10^8 Hz, 100 ksps', '5', '900', '9×10^8', '100')
Tc, fc = 5e-3, 900e6
fm = 1 / Tc
lam = C / fc
v1 = fm * C / fc
v2 = fm * lam
assert abs(v1 - v2) < 1e-9
put('t9 ex2 f_m (Hz)', f'{fm:.0f}')
put('t9 ex2 v (m/s)', f'{v1:.2f}')
put('t9 ex2 lambda (m)', f'{lam:.4f}')
put('t9 ex2 v (km/h)', f'{v1 * 3.6:.0f}')
Ts = 1 / 100e3
put('t9 ex2 Ts (us)', f'{Ts * 1e6:.0f}')
put('t9 ex2 Tc/Ts', f'{Tc / Ts:.0f}')

# ---------------------------------------------------------------- t9 example 3
print('\n--- t9 例3 (sigma 2 us, f_m 500 Hz; 250 sps, 20 ksps, 5 Msps)')
inp('t9 ex3: sigma 2 us, f_m 500 Hz, 250 sps, 20 ksps, 5 Msps', '2', '500', '250', '20', '5')
sgm, fm = 2e-6, 500.0
Tc = 1 / fm
put('t9 ex3 Tc (ms)', f'{Tc * 1e3:.0f}')
rows = {250: ('ms', 1e3), 20e3: ('us', 1e6), 5e6: ('us', 1e6)}
for R, (unit, k) in rows.items():
    Ts = 1 / R
    put(f't9 ex3 Rs={R:g}: Ts ({unit})', f'{Ts * k:g}')
    put(f't9 ex3 Rs={R:g}: sigma/Ts', f'{sgm / Ts:g}')
    if Ts > Tc:
        put(f't9 ex3 Rs={R:g}: Ts/Tc', f'{Ts / Tc:g}')
    else:
        put(f't9 ex3 Rs={R:g}: Tc/Ts', f'{Tc / Ts:g}')
    flat = 'flat' if sgm / Ts < 0.1 else ('selective' if sgm / Ts >= 10 else 'grey')
    speed = 'fast' if Ts > Tc else 'slow'
    print(f'      -> {flat}, {speed}')

# ---------------------------------------------------------------- structural / constant tokens
print('\n--- structural / formula constants allowed in the text')
for tok, why in [('1', 'constant (1/T_s, B_D = f_m etc.)'), ('2', 'constant (a/2, half marks, squares)'),
                 ('10', 'constant (10 sigma, 10 log, 10^(dB/10))'), ('0.1', 'flat rule 0.1'),
                 ('90', 'angle 90 deg'), ('3.6', 'km/h / 3.6'), ('3', 'constant a^2/3')]:
    allow(tok, why)
    print(f'  {tok:<6} {why}')


# ======================================================================================== PART B
print('\n' + '=' * 100)
print('PART B  checks on the fragment')
print('=' * 100)
raw = FRAG.read_text(encoding='utf-8')

VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'wbr', 'col', 'source', 'area', 'base', 'embed', 'param', 'track'}


class Node:
    def __init__(self, tag, attrs, parent, line):
        self.tag, self.attrs, self.parent, self.line = tag, dict(attrs), parent, line
        self.kids = []

    @property
    def cls(self):
        return set((self.attrs.get('class') or '').split())

    def text(self):
        return ''.join(k if isinstance(k, str) else k.text() for k in self.kids)

    def elems(self):
        return [k for k in self.kids if isinstance(k, Node)]

    def walk(self):
        for k in self.elems():
            yield k
            yield from k.walk()

    def find(self, tag=None, cls=None):
        return [n for n in self.walk() if (tag is None or n.tag == tag) and (cls is None or cls in n.cls)]


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('#root', [], None, 0)
        self.cur = self.root
        self.errors = []

    BLOCK = {'td', 'th', 'tr', 'li', 'p', 'div', 'h2', 'h3', 'h4', 'table', 'thead', 'tbody', 'ol', 'ul', 'section'}

    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCK:
            self.cur.kids.append(' ')        # keep adjacent cells apart in the extracted text
        n = Node(tag, attrs, self.cur, self.getpos()[0])
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(Node(tag, attrs, self.cur, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.cur.tag == tag:
            self.cur = self.cur.parent
            if tag in self.BLOCK:
                self.cur.kids.append(' ')
            return
        self.errors.append(f'</{tag}> at line {self.getpos()[0]} while <{self.cur.tag}> (line {self.cur.line}) is open')
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.kids.append(data)


tp = Tree()
tp.feed(raw)
tp.close()

print('\n--- 1. tags')
for e in tp.errors:
    bad('tag mismatch: ' + e)
n = tp.cur
while n is not tp.root:
    bad(f'unclosed <{n.tag}> opened at line {n.line}')
    n = n.parent
for t in ('style', 'script', 'html', 'head', 'body'):
    if tp.root.find(t):
        bad(f'forbidden <{t}>')
print(f'  tag errors: {len(tp.errors)}; forbidden tags: none' if not tp.errors else '  see !! above')

print('\n--- 2. build regex (build_quizsum.py) finds the sections')
ids = [m.group(1) for m in re.finditer(r'<section class="topic" id="(t\d+)">.*?</section>', raw, re.S)]
print('  sections:', ids)
if ids != ['t8', 't9']:
    bad(f'sections found {ids}, expected t8, t9')

print('\n--- 3. TeX spans')
spans = re.findall(r'\\\((.*?)\\\)', raw, re.S) + re.findall(r'\\\[(.*?)\\\]', raw, re.S)
for sp in spans:
    if re.search(r'[<>]|&lt;|&gt;', sp):
        bad('raw < or > inside TeX: ' + sp[:80])
    if sp.count('{') != sp.count('}'):
        bad('unbalanced braces in TeX: ' + sp[:80])
if raw.count('\\(') != raw.count('\\)') or raw.count('\\[') != raw.count('\\]'):
    bad('unbalanced TeX delimiters')
if '$' in raw:
    bad('$ delimiter found')
print(f'  {len(spans)} TeX spans checked')

print('\n--- 4. section structure')
SYM_HEAD = ['符号', '中文', 'English', '含义（大白话）', '单位']
H3 = ['符号与含义 · Symbols', '公式 · Formulas', '解题步骤 · Steps', '中文例子 · 怎么用', '易错 · Traps']
for sec in tp.root.find('section', 'topic'):
    sid = sec.attrs.get('id')
    h2 = sec.find('h2')
    tn = h2[0].find('span', 'tn') if h2 else []
    ok_h2 = bool(tn) and tn[0].text() == sid[1:] and ' · ' in h2[0].text()
    meta = sec.find('div', 'meta')
    sts = [s for s in meta[0].find('span', 'st')] if meta else []
    freq = meta[0].find('span', 'freq') if meta else []
    why = sec.find('p', 'why')
    h3s = [h.text().strip() for h in sec.find('h3')]
    sym = sec.find('table', 'sym')
    steps = sec.find('table', 'steps')
    fms = sec.find('div', 'fm')
    egs = sec.find('div', 'eg')
    traps = sec.find('ul', 'trap')
    en = sec.find('div', 'en')
    print(f'  {sid}: h2 {ok_h2}; meta badges {[next(iter(s.cls - {"st"})) for s in sts]}; freq {bool(freq)}; why {bool(why)}; '
          f'h3 {h3s == H3}; sym {len(sym)}; fm {len(fms)}; steps {len(steps)}; eg {len(egs)}; trap li '
          f'{len(traps[0].find("li")) if traps else 0}; en {bool(en)}')
    if not ok_h2:
        bad(f'{sid}: h2 / span.tn wrong')
    if not sts or not freq or not freq[0].text().startswith('出现：'):
        bad(f'{sid}: meta badges / freq missing')
    if not why:
        bad(f'{sid}: p.why missing')
    if h3s != H3:
        bad(f'{sid}: h3 order {h3s}')
    for tb in sym:
        head = [th.text().strip() for th in tb.find('th')]
        if head != SYM_HEAD:
            bad(f'{sid}: sym header {head}')
        for tr in tb.find('tbody')[0].find('tr'):
            if len(tr.find('td')) != 5:
                bad(f'{sid}: sym row with {len(tr.find("td"))} cells: {tr.text()[:40]}')
    for fm in fms:
        fl, fx, fn = fm.find('div', 'fl'), fm.find('div', 'fx'), fm.find('div', 'fn')
        if not (fl and fx and fn and fl[0].find('span', 'st')):
            bad(f'{sid}: .fm incomplete: {fm.text()[:40]}')
    for tb in steps:
        head = [th.text().strip() for th in tb.find('th')]
        if len(head) != 4 or head[:2] != ['步骤', '做法']:
            bad(f'{sid}: steps header {head}')
        print(f'      steps columns: {head[2]} | {head[3]}')
        for tr in tb.find('tbody')[0].find('tr'):
            if len(tr.find('td')) != 4:
                bad(f'{sid}: steps row with {len(tr.find("td"))} cells')
        tw = tb.parent
        sib = tw.parent.elems()
        i = sib.index(tw)
        nxt = sib[i + 1] if i + 1 < len(sib) else None
        prv = sib[i - 1] if i > 0 else None
        if not (nxt is not None and nxt.tag == 'p' and 'src' in nxt.cls and nxt.text().startswith('来源：')):
            bad(f'{sid}: steps table not followed by p.src')
        if len(steps) > 1 and not (prv is not None and prv.tag == 'h4'):
            bad(f'{sid}: steps table without h4 before it')
    if not 2 <= len(egs) <= 3:
        bad(f'{sid}: {len(egs)} examples')
    for eg in egs:
        if not (eg.find('div', 'egh') and eg.find('p', 'q') and eg.find('ol', 'work') and eg.find('p', 'ans')):
            bad(f'{sid}: example incomplete')
    if not traps or not 3 <= len(traps[0].find('li')) <= 6:
        bad(f'{sid}: traps count')
    if not en or not en[0].find('div', 'enl') or not en[0].find('p'):
        bad(f'{sid}: exam English block incomplete')

print('\n--- 5. formula status badges (quiz_marks.py / notes.py)')
EXPECT = {'平均时延 Mean delay': {'give'}, 'rms 时延扩展': {'give'}, 'dB → 线性': {'def'},
          '平坦衰落判据': {'must'}, '相干带宽与信号带宽': {'def'}, '多普勒频移 Doppler shift': {'def'},
          '最大多普勒频移、多普勒扩展': {'def'}, '相干时间': {'def'}, '快/慢衰落判据': {'def'}, '两个维度合起来': {'def'}}
for fm in tp.root.find('div', 'fm'):
    fl = fm.find('div', 'fl')[0]
    got = {next(iter(s.cls - {'st'})) for s in fl.find('span', 'st')}
    key = next((k for k in EXPECT if fl.text().startswith(k)), None)
    print(f'  {fl.text():<60} {sorted(got)}  expected {sorted(EXPECT.get(key, {"?"}))}')
    if key is None or got != EXPECT[key]:
        bad(f'badge mismatch: {fl.text()}')
qm = (SRC / 'p2build' / 'quiz_marks.py').read_text(encoding='utf-8')
if "('learn_02.html', '平均时延与 rms 时延扩展', 'give'" not in qm:
    bad('quiz_marks.py no longer marks mean/rms delay as give')
if '\\\\(\\\\sigma_{T_m}/T_s<0.1\\\\)：平坦衰落' not in qm:
    bad('quiz_marks.py no longer carries the inline 背 badge for sigma/Ts < 0.1')
notes = (SRC / 'teacher' / 'notes.py').read_text(encoding='utf-8')
if '平坦衰落判据 σ<sub>τ</sub>/T<sub>s</sub> &lt; 0.1' not in notes:
    bad('notes.py: 0.1 rule not in the must-memorise list')
if '平均时延和 rms 时延扩展公式' not in notes:
    bad('notes.py: mean/rms delay not in the given list')

print('\n--- 6. lecturer claims (every 老师 in the fragment must map to notes.py)')
CLAIMS = [
    ('老师说没写 dB ↔ 线性换算会扣分', '没做 dB ↔ 线性换算会扣分'),
    ('老师说这是蓝框公式，要背', 'σ<sub>τ</sub>/T<sub>s</sub> &lt; 0.1 是<b>蓝框，要背</b>'),
    ('老师课上说比值只稍大于 0.1（如 0.15）时不能下结论，要远大于 0.1 才能说是频率选择性',
     '比值稍大于 0.1（如 0.15）时<b>不能下结论</b>，要远大于 0.1 才能说是频率选择性'),
    ('老师说稍大于 0.1 时不能下结论', '比值稍大于 0.1（如 0.15）时<b>不能下结论</b>'),
    ('老师也说要远大于 0.1', '要远大于 0.1 才能说是频率选择性'),
    ('老师的简单记法：信号带宽在相干带宽以内就是平坦', '简单记法：信号带宽在相干带宽以内就是平坦'),
    ('老师说问衰落类型只答一个维度只给一半分', '只答一个维度只给一半分'),
    ('老师说只给一半分', '只答一个维度只给一半分'),
    ('老师说多普勒<b>频移</b>本身不算失真，多普勒<b>扩展</b>才是（频率色散）',
     '多普勒<b>频移</b>不算失真；多普勒<b>扩展</b>才是严重的失真（频率色散）'),
    ('老师要求会说出它是最大多普勒频移', '要会说出 <b>ρ = Z<sub>min</sub>/Z<sub>rms</sub></b>，f<sub>m</sub> 是最大多普勒频移'),
    ('老师的简单记法：符号时长在相干时间以内就是慢衰落', '符号时长在相干时间以内就是慢衰落'),
    ('老师说时延扩展（时间色散）和多普勒扩展（频率色散）分开判断', '时延扩展是时间色散，多普勒扩展是频率色散，两种效应分开判断'),
]
covered = set()
for frag_s, note_s in CLAIMS:
    pos = [m.start() for m in re.finditer(re.escape(frag_s), raw)]
    in_notes = note_s in notes
    print(f'  {"OK " if pos and in_notes else "BAD"} x{len(pos)} {frag_s[:44]}')
    if not pos:
        bad('claim text not in fragment: ' + frag_s)
    if not in_notes:
        bad('claim not supported by notes.py: ' + note_s)
    covered.update(pos)
for m in re.finditer('老师', raw):
    if m.start() not in covered:
        ctx = re.sub(r'<[^>]+>', '', raw[m.start():m.start() + 60])
        bad('uncovered lecturer attribution: ' + ctx)

print('\n--- 7. sources (labels and numbers)')
p8 = (SRC / 'p2build' / 'prac_8.html').read_text(encoding='utf-8')
arts = {m.group(1): m.group(0) for m in re.finditer(r'<article class="ex" id="(p8q\d+)">.*?</article>', p8, re.S)}
lab = {k: re.search(r'<span class="pg">([^<]*)</span>', v).group(1) for k, v in arts.items()}
txt = {k: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', v)) for k, v in arts.items()}
WANT = {'p8q3': ('模拟 A · Q3', ['50 k symbols/s on a 1.8 GHz carrier', 'moves at 72 km/h', '0 0 1 −3 3 −6',
                                '平坦慢衰落', '1.255 / 1.752 = 0.716 µs', '√1.063 = 1.03 µs']),
        'p8q8': ('模拟 C · Q2', ['50 k symbols/s', 'coherence bandwidth of 200 kHz', 'maximum Doppler shift of 100 Hz',
                                '平坦慢衰落']),
        'p8q12': ('专项 · Q3', ['10 k symbols/s on a 2 GHz carrier', 'rms delay spread of the channel is 2 µs',
                               'moves at 54 km/h', 'Is the fading flat or frequency-selective', 'Is the fading fast or slow'])}
for k, (want_lab, needles) in WANT.items():
    ok = lab.get(k) == want_lab
    miss = [nd for nd in needles if nd not in txt.get(k, '')]
    print(f'  {k}: label "{lab.get(k)}" {"OK" if ok else "!="} {want_lab}; missing {miss}')
    if not ok or miss:
        bad(f'{k}: label/number mismatch {miss}')
for k, v in lab.items():
    print(f'      {k} = {v}')
p1 = (SRC / 'p2build' / 'prac_1.html').read_text(encoding='utf-8')
a = re.search(r'<article class="ex" id="p1q3">.*?</article>', p1, re.S).group(0)
for nd in ('<span class="pg">P1 · Q3</span>', r'0\le\tau\le10\,\mu s', '官方答案：</b>5 µs，2.89 µs；34.6 ksps'):
    print(f'  p1q3 has {nd!r}: {nd in a}')
    if nd not in a:
        bad('p1q3 missing ' + nd)
ex = {y: (SRC / 'exams' / f'data_{y}.py').read_text(encoding='utf-8') for y in ('2324', '2425', '2526s1', '2526s2')}
EXAM = [('2324', 'symbol duration of 1 ms'), ('2324', 'time invariant channel impulse response'),
        ('2324', 'rms delay spread of 0.01ms'), ('2324', 'coherence bandwidth of 500 kHz'),
        ('2324', 'half of the coherence bandwidth'),
        ('2526s1', 'available bandwidth of 500 kHz'), ('2526s1', 'measured to be 30 kHz and 10 microseconds'),
        ('2526s1', 'minimum number of carriers the OFDM system should use for its signal to experience flat fading'),
        ('2526s1', 'N<sub>min</sub> = 17'), ('2526s1', '保护间隔 T<sub>G</sub> ≥ 10 µs'),
        ('2526s2', 'Explain how coherence bandwidth, doppler spread, and signal bandwidth can be used to determine the type of fading'),
        ('2425', 'What would you observe on the value of h for fast-fading channels')]
for y, nd in EXAM:
    print(f'  data_{y}.py has {nd[:70]!r}: {nd in ex[y]}')
    if nd not in ex[y]:
        bad(f'data_{y}.py missing {nd}')
cls = sum(bool(re.search(r'fading type|type of fading', re.sub(r'<[^>]+>', '', v), re.I)) for v in ex.values())
print(f'  papers with a fading-type question: {cls}/4')
put('meta: papers with a fading-type question', f'{cls}/4')
for tok in str(cls), '4':
    allow(tok, 'meta 2/4 papers')

print('\n--- 8. wording checks (no "borderline / approximately flat" verdict for B_s < B_C)')
for m in re.finditer(r'borderline|approximately flat|近似）平坦|（近似）', raw):
    ctx = re.sub(r'<[^>]+>', '', raw[max(0, m.start() - 70):m.end() + 30])
    print('  found:', ctx.replace('\n', ' '))
    if '不要自己再加' not in ctx:
        bad('borderline wording outside the warning trap: ' + ctx)

print('\n--- 9. numeric tokens in the fragment text')
text = tp.root.text()
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻', '0123456789-')
t = re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+', lambda m: '^' + m.group(0).translate(SUP), text)
t = t.replace('−', '-')
STRUCT = [r'20\d\d-\d\d', r'\bS[12]\b', r'Q\d+(?:\([a-z]+\))*', r'p\.\s?\d+(?:\s?[–-]\s?\d+)?', r'第 \d+[ab]? 章',
          r'Practice \d', r'\bt\d+\b', r'\d+-QAM', r'例 \d', r'题型 \d', r'期末 \d/\d 套']
for pat in STRUCT:
    t = re.sub(pat, ' ', t)
found = {}
for m in re.finditer(r'(\d+(?:\.\d+)?)\s*×\s*10\^(-?\d+)', t):
    found.setdefault(f'{m.group(1)}×10^{m.group(2)}', []).append(m.start())
t = re.sub(r'(\d+(?:\.\d+)?)\s*×\s*10\^(-?\d+)', ' ', t)
t = re.sub(r'\^-?\d+', ' ', t)                       # squares and other exponents (tau^2, mu^2, us^2)
for m in re.finditer(r'(?<![\w.])\d+(?:\.\d+)?', t):
    found.setdefault(m.group(0), []).append(m.start())
unexpl = []
for tok in sorted(found, key=lambda x: (float(x.split('×')[0]) if '×' not in x else 1e9, x)):
    why = ALLOWED.get(tok)
    print(f'  {tok:<14} x{len(found[tok]):<3} {"; ".join(sorted(why))[:110] if why else "UNEXPLAINED"}')
    if not why:
        unexpl.append(tok)
for tok in unexpl:
    for p in found[tok][:3]:
        bad(f'unexplained number {tok}: ...{t[max(0, p - 40):p + 30]}...')

print('\n--- 10. every display string of part A appears in the fragment')
plain = t2 = re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+', lambda m: '^' + m.group(0).translate(SUP), text).replace('−', '-')
for label, s in D.items():
    if label.startswith('meta:'):
        s_check = s.replace('/4', '/4 套')
    else:
        s_check = s
    hit = all(re.search(r'(?<![\d.])' + re.escape(part.strip()) + r'(?![\d])', plain) for part in s_check.split(','))
    if not hit:
        bad(f'display string not found in fragment: {label} = {s}')
print(f'  {len(D)} display strings checked')

print('\n' + '=' * 100)
print(f'RESULT: {len(PROBLEMS)} problem(s)')
for p in PROBLEMS:
    print('  - ' + p)
