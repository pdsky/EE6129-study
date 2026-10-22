#!/usr/bin/python3
"""Independent adversarial check of quizsum/frag_lcr.html (topic t10: LCR and AFD).

Written by the checker, not the writer; nothing is imported from check_lcr.py. Layers:
  1. sources: the cited past-final / Practice / mock questions really say what the page quotes,
     labels map correctly (p8q3 = 模拟 A·Q3, p8q8 = 模拟 C·Q2), lecturer claims exist in notes.py,
     status badges match quiz_marks.py / notes.py;
  2. numbers: every displayed number recomputed from first principles (AFD as P(z<Z)/LCR, f_m as v/λ,
     ρ from 10^(-X/20), Monte Carlo of the Rayleigh envelope with statistics.NormalDist), compared at
     the displayed precision; where the page shows a chain of rounded operands, the literal arithmetic
     of those operands must also round to the shown result;
  3. a generic scan that evaluates every unit-free "a × b ÷ c = d" chain on the page literally, and
     lists every numeric token on the page that layer 2 did not account for;
  4. HTML / format: html.parser balance, TeX hygiene (no raw < > or CJK in math), required structure.
Stdlib only:  /usr/bin/python3 _verify_lcr.py
"""
import html
import math
import re
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from html.parser import HTMLParser
from pathlib import Path
from statistics import NormalDist

HERE = Path(__file__).resolve().parent
SRC = HERE.parent
RAW = (HERE / 'frag_lcr.html').read_text(encoding='utf-8')


def norm_text(s):
    s = re.sub(r'</(td|th|li|p|div|h[1-6]|tr)>', ' | ', s)
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    return re.sub(r'\s+', ' ', s)


TEXT = norm_text(RAW)
FAIL, SHOWN = [], set()
NCHK = 0


def rnd(x, shown):
    s = shown.replace('−', '-')
    dec = len(s.split('.')[1]) if '.' in s else 0
    return str(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-dec), rounding=ROUND_HALF_UP))


def chk(label, exact, shown, lit=None, snip=None):
    """exact: first-principles value in the displayed unit; lit: value of the displayed rounded operands."""
    global NCHK
    NCHK += 1
    want = shown.replace('−', '-')
    ok_e = rnd(exact, want) == want
    ok_l = lit is None or rnd(lit, want) == want
    ok_s = snip is None or snip in TEXT
    good = ok_e and ok_l and ok_s
    msg = f'[{"OK " if good else "BAD"}] {label}: shown {shown} | exact {exact:.7g}'
    if not ok_e:
        msg += f' (rounds to {rnd(exact, want)})'
    if lit is not None:
        msg += f' | literal {lit:.7g}' + ('' if ok_l else f' (rounds to {rnd(lit, want)})')
    if not ok_s:
        msg += f' | NOT ON PAGE: {snip!r}'
    print(msg)
    if not good:
        FAIL.append(label)
    SHOWN.add(want.lstrip('-'))


def given(label, shown, snip):
    """A given (input) number: must appear on the page in the quoted context."""
    global NCHK
    NCHK += 1
    ok = snip in TEXT
    print(f'[{"OK " if ok else "BAD"}] given {label}: {shown}' + ('' if ok else f' | NOT ON PAGE: {snip!r}'))
    if not ok:
        FAIL.append('given ' + label)
    for t in re.findall(r'\d+(?:\.\d+)?', shown):
        SHOWN.add(t)


def on_page(label, snip, want=True):
    ok = (snip in TEXT) == want
    print(f'[{"OK " if ok else "BAD"}] text {label}: {"present" if want else "absent"} {snip!r}')
    if not ok:
        FAIL.append('text ' + label)


def in_file(label, path, *subs):
    s = (SRC / path).read_text(encoding='utf-8')
    for sub in subs:
        ok = sub in s
        print(f'[{"OK " if ok else "BAD"}] source {label}: {path} contains {sub!r}')
        if not ok:
            FAIL.append(f'source {label}: {sub}')
    return s


def head(t):
    print(f'\n==== {t}')


# ------------------------------------------------------------------ physics, written independently
S2P = math.sqrt(2 * math.pi)
C = 3e8


def p_below(rho):
    """Rayleigh P(z < rho * Z_rms) by Simpson integration of p(z) = 2z e^{-z^2} (Z_rms = 1)."""
    n = 4000
    h = rho / n
    f = lambda z: 2 * z * math.exp(-z * z)
    s = f(0) + f(rho) + sum((4 if k % 2 else 2) * f(k * h) for k in range(1, n))
    return s * h / 3


def lcr(fm, rho):
    return S2P * fm * rho * math.exp(-rho * rho)


def afd(fm, rho):
    """Slide derivation: AFD = (fraction of time below threshold) / LCR; not the closed form."""
    return p_below(rho) / lcr(fm, rho)


def afd_closed(fm, rho):
    return (math.exp(rho * rho) - 1) / (S2P * fm * rho)


def fm_of(v_kmh, fc):
    lam = C / fc
    return (v_kmh / 3.6) / lam


def dB(x):
    return 10 * math.log10(x)


# ================================================================== 1. sources
head('1. sources: cited questions, labels, lecturer claims, status badges')
in_file('2025-26 S2 Q1(a)(ii)', 'exams/data_2526s2.py',
        "id='y2526s2-q1a'", 'symbol duration of 5 ms', 'average fade duration has been estimated to be 20 ms',
        'For a period of 10 seconds, deep fades have been observed to have occurred 40 times',
        'the affected symbol will be in error', 'average number of consecutive symbol errors per second',
        '# EE6129 Semester 2 Examination 2025-2026')
in_file('2024-25 S2 Q1(a)(ii)', 'exams/data_2425.py',
        '# EE6129 Semester 2 Examination 2024-2025', '6 × 10<sup>−6</sup> second', 'level crossing rate of 5',
        'covers exactly three (3) consecutive symbols', 'more than half of the symbol lies within a deep fade')
for f in ('exams/data_2324.py', 'exams/data_2526s1.py'):
    s = (SRC / f).read_text(encoding='utf-8').lower()
    ok = not any(k in s for k in ('level crossing', 'fade duration', 'lcr'))
    print(f'[{"OK " if ok else "BAD"}] source "期末 2/4 套": {f} has no LCR/AFD question')
    if not ok:
        FAIL.append('2/4 claim ' + f)
in_file('Practice 2 Q1', 'p2build/prac_2.html', 'id="p2q1"', '<span class="pg">P2 · Q1</span>',
        'The maximum Doppler shift is 50 Hz', '0.1 of the rms value of the signal strength',
        '<b>官方答案：</b>0.8 ms')
p8 = (SRC / 'p2build/prac_8.html').read_text(encoding='utf-8')
for qid, lab, subs in (
        ('p8q3', '模拟 A · Q3', ['transmits 50 k symbols/s on a 1.8 GHz carrier', 'moves at 72 km/h',
                                'must not fall more than 10 dB below its rms value',
                                'find the average fade duration and the average number of symbols affected by one fade']),
        ('p8q8', '模拟 C · Q2', ['transmits 50 k symbols/s', 'deep fades are observed 300 times',
                                'estimated to be 0.5 ms', 'Over a period of 10 seconds',
                                'how far (in dB) below the rms power is the deep-fade threshold',
                                'the fraction of time the signal spends in deep fades'])):
    a = p8.index(f'id="{qid}"')
    art = p8[a:p8.index('</article>', a)]
    for sub in [f'<span class="pg">{lab}</span>'] + subs:
        ok = sub in art
        print(f'[{"OK " if ok else "BAD"}] source {qid}: contains {sub!r}')
        if not ok:
            FAIL.append(f'{qid}: {sub}')
in_file('learn_02 page refs and errata', 'p2build/learn_02.html',
        '瑞利衰落的 LCR 与 AFD（p.41–43）', 'AFD 公式是怎么来的（p.42–43）', '一次衰落会连错几个符号（第 2 章 p.45–47）',
        '多普勒频移与相干时间（p.34–36）', '瑞利衰落的衰落余量（p.51）', 'AFD = 71.17 µs、每秒 9812 个错误',
        '<b>72.17 µs</b>，每秒 <b>9950</b>', '符号只要有一部分落在衰落里就算错', '0.1% → 30 dB')
notes = (SRC / 'teacher/notes.py').read_text(encoding='utf-8')
CLAIMS = [  # (text on the page, supporting text in teacher/notes.py)
    ('老师说这类题数据多，先把已知量逐个写下来再算', '这类题数据多，老师建议先读题、把已知量逐个写下来'),
    ('老师课上讲的做法：一次衰落里错的符号数 = AFD ÷ Ts；题目给的是符号速率就取倒数，即 AFD × Rs',
     '一次衰落里错的符号数 = AFD ÷ T<sub>s</sub>；题目给的是符号<b>速率</b>时取倒数，即 AFD × R<sub>s</sub>'),
    ('老师要求会说出 ρ = Zmin/Zrms、fm 是最大多普勒频移', '要会说出 <b>ρ = Z<sub>min</sub>/Z<sub>rms</sub></b>，f<sub>m</sub> 是最大多普勒频移'),
    ('老师特别提过：看到“rms 值的 10%”立刻想到 ρ = 0.1', '题目说"最小信号强度是 rms 值的 10%" → 立刻想到 ρ = 0.1'),
    ('老师说漏写会扣分', '没做 dB ↔ 线性换算会扣分'),
    ('Quiz 题型接近期末、但更简单（老师说）', 'Quiz 题型接近期末但更简单'),
]
covered = 0
for page, src in CLAIMS:
    ok = page in TEXT and src in notes
    covered += TEXT.count(page) if page in TEXT else 0
    print(f'[{"OK " if ok else "BAD"}] lecturer claim: page {page in TEXT}, notes.py {src in notes}: {page}')
    if not ok:
        FAIL.append('lecturer claim ' + page)
n_teacher = TEXT.count('老师')
print(f'[{"OK " if n_teacher == covered else "BAD"}] every "老师" on the page is a verified claim ({n_teacher} on page, {covered} verified)')
if n_teacher != covered:
    for m in re.finditer('老师', TEXT):
        print('      ...' + TEXT[max(0, m.start() - 30):m.start() + 50])
    FAIL.append('unverified 老师 claim')
qm = (SRC / 'p2build/quiz_marks.py').read_text(encoding='utf-8')
for card, kind in (("'瑞利衰落的 LCR 与 AFD', 'give'", 'LCR/AFD = 考试给'),
                   ("'瑞利衰落（p.25–26）', 'must'", 'Rayleigh outage 1-e^(-g0/gbar) = 背'),
                   ("'瑞利衰落的衰落余量', 'try'", 'fade margin = 尽量记')):
    ok = card in qm
    print(f'[{"OK " if ok else "BAD"}] quiz_marks.py: {kind}')
    if not ok:
        FAIL.append('quiz_marks ' + kind)
ok = '瑞利中断 1 − e<sup>−γ₀/γ̄</sup>' in notes and 'LCR、AFD 公式（但要会解释 ρ 和 f<sub>m</sub>）' in notes
print(f'[{"OK " if ok else "BAD"}] notes.py: Rayleigh outage listed under 要背, LCR/AFD under 考试会给')

# ================================================================== 2. numbers
head('2a. constants used in the chains')
chk('sqrt(2 pi)', S2P, '2.5066', snip='√(2π) = 2.5066')
chk('e^-0.01', math.exp(-0.01), '0.99005', snip='12.53 × 0.99005 = 12.41')
chk('e^0.01 - 1', math.exp(0.01) - 1, '0.01005', snip='0.01005 / 12.53 = 0.802 ms')
chk('e^-0.1', math.exp(-0.1), '0.90484', snip='95.12 × 0.90484 = 86.07')
chk('e^0.1 - 1', math.exp(0.1) - 1, '0.1052', snip='0.1052 / 95.12 = 1.106 ms')
chk('e^-0.01 to 3 s.f.', math.exp(-0.01), '0.990', snip='(2.5066 × 0.1 × 0.990)')
chk('Rayleigh P(z<0.1 Zrms) by integration = 1-e^-0.01', p_below(0.1), '0.00995', snip='1 − e−0.01 = 0.00995')
# Monte Carlo: envelope of two independent Gaussians with E[z^2] = 1, i.e. rho is relative to Z_rms, not sigma
N = 200000
xs = NormalDist(0, math.sqrt(0.5)).samples(N, seed=11)
ys = NormalDist(0, math.sqrt(0.5)).samples(N, seed=29)
for rho in (0.1, math.sqrt(0.1), 1 / math.sqrt(2)):
    p_hat = sum(1 for x, y in zip(xs, ys) if x * x + y * y < rho * rho) / N
    p = 1 - math.exp(-rho * rho)
    se = math.sqrt(p * (1 - p) / N)
    ok = abs(p_hat - p) < 4 * se
    print(f'[{"OK " if ok else "BAD"}] Monte Carlo P(z < {rho:.4f} Zrms): {p_hat:.5f} vs 1-e^-rho^2 = {p:.5f} (4 SE = {4*se:.5f})')
    if not ok:
        FAIL.append('Monte Carlo')
for rho in (0.1, 0.31623, 0.5):
    assert abs(afd(50, rho) - afd_closed(50, rho)) < 1e-9 * afd(50, rho), rho
print('[OK ] AFD = P(z<Z)/LCR equals the closed form (e^rho^2 - 1)/(sqrt(2pi) fm rho) for rho 0.1, 0.316, 0.5')

head('2b. symbol table and formula cards')
chk('Rs 50 ksps -> Ts (us)', 1 / 50e3 * 1e6, '20', snip='50 k 符号/s → Ts = 20 µs')
chk('"rms 值的 10%" rho', 0.1, '0.1', snip='“rms 值的 10%” → ρ = 0.1')
chk('rho^2 for 10%', 0.1 ** 2, '0.01', snip='rms 值的 10% → ρ = 0.1、ρ² = 0.01（−20 dB）')
chk('10log10(0.01)', dB(0.01), '-20', snip='ρ² = 0.01（−20 dB）')
chk('power 10 dB below: rho^2', 10 ** (-10 / 10), '0.1', snip='功率低 10 dB → ρ² = 0.1、ρ = 0.3162')
chk('power 10 dB below: rho = 10^(-10/20)', 10 ** (-10 / 20), '0.3162', snip='功率低 10 dB → ρ² = 0.1、ρ = 0.3162')
chk('threshold power 1% of mean -> rho', math.sqrt(0.01), '0.1', snip='门限功率是平均功率的 1% → ρ = 0.1')
chk('72 km/h in m/s', 72 / 3.6, '20', snip='72 km/h = 20 m/s')
given('c', '3×10⁸', 'c = 3×10⁸ m/s')
given('km/h divisor', '3.6', 'km/h ÷ 3.6')
chk('card: 10 s, 40 fades -> LCR', 40 / 10, '4', lit=40 / 10, snip='“10 秒里 40 次” → 40/10 = 4 次/s')
chk('card: 2025-26 bursts per s / symbols per burst', 40 / 10, '4', snip='2025-26 S2 那题是每秒 4 串、每串 4 个')

head('2c. table (A) counting: 2025-26 S2 Q1(a)(ii)')
Ts, A, Nf, T = 5e-3, 20e-3, 40, 10
given('2025-26 knowns', '5 20 10 40', 'Ts = 5 ms，AFD = 20 ms，10 s 内 40 次')
L = Nf / T
chk('(1) LCR', L, '4', lit=40 / 10, snip='40/10 = 4 次/s')
chk('(2) per fade', A / Ts, '4', snip='20 ms / 5 ms = 4 个')
chk('(3) errors/s', L * A / Ts, '16', lit=4 * 4, snip='4 × 4 = 16 个/s')
chk('(4) fraction', L * A, '0.08', snip='（原题没问）4 × 20 ms = 0.08')
chk('(5) Rs = 1/Ts', 1 / Ts, '200', snip='Rs = 1/5 ms = 200 个/s')
chk('(5) SER = errors / Rs', (L * A / Ts) / (1 / Ts), '0.08', lit=16 / 200, snip='16 ÷ 200 = 0.08 ✓')

head('2d. table (A) counting: mock C Q2(b)')
Rs, A, Nf, T = 50e3, 0.5e-3, 300, 10
given('mock C knowns', '50 20 0.5 10 300', 'Rs = 50 k 符号/s（Ts = 20 µs），AFD = 0.5 ms，10 s 内 300 次')
L = Nf / T
chk('(1) LCR', L, '30', lit=300 / 10, snip='300/10 = 30 次/s')
chk('(2) per fade', A * Rs, '25', lit=0.5e-3 / 20e-6, snip='0.5 ms / 20 µs = 25 个')
chk('(3) errors/s', L * A * Rs, '750', lit=30 * 25, snip='30 × 25 = 750 个/s')
chk('(4) fraction', L * A, '0.015', lit=30 * 0.5e-3, snip='30 × 0.5 ms = 0.015（1.5%）')
chk('(4) fraction in %', L * A * 100, '1.5', snip='（1.5%）')
chk('(5) SER', L * A * Rs / Rs, '0.015', lit=750 / 50000, snip='750 ÷ 50 000 = 0.015 ✓')
chk('(5) Rs written out', Rs, '50000', snip='750 ÷ 50 000')

head('2e. 2024-25 S2 Q1(a)(ii) worked block')
given('2024-25 knowns', '6 5 3', 'AFD = 6 × 10⁻⁶ s，LCR = 5（题目没写单位，按 次/s）。一次平均衰落正好盖住 3 个连续符号')
chk('Ts (us)', 6e-6 / 3 * 1e6, '2', snip='Ts = 6 µs ÷ 3 = 2 µs')
chk('Rs (k/s)', 1 / (6e-6 / 3) / 1e3, '500', snip='Rs = 500 k 符号/s')
# brute force the "more than half" rule: fade [s, s+3) over symbols [k, k+1), Ts = 1, exact fractions
counts = {}
for i in range(0, 1000):
    s = Fraction(i, 1000)
    cnt = sum(1 for k in range(0, 5) if max(Fraction(0), min(k + 1, s + 3) - max(k, s)) > Fraction(1, 2))
    counts.setdefault(cnt, []).append(s)
only_two = counts.get(2, [])
ok = set(counts) <= {2, 3} and only_two == [Fraction(1, 2)]
print(f'[{"OK " if ok else "BAD"}] "more than half" rule: 3 symbols in error for every offset except exactly Ts/2 '
      f'(counts {sorted((k, len(v)) for k, v in counts.items())})')
if not ok:
    FAIL.append('more-than-half reasoning')
anypart = [sum(1 for k in range(0, 5) if min(k + 1, s + 3) - max(k, s) > 0) for s in (Fraction(0), Fraction(1, 4))]
print(f'      (info) "any part counts" rule: aligned {anypart[0]}, misaligned {anypart[1]} -> slide uses AFD/Ts without +1')
chk('errors/s', 5 * 3, '15', lit=5 * 3, snip='LCR × 3 = 5 × 3 = 15 个/s')

head('2f. table (B) formula: Practice 2 Q1  [fD 50 Hz, rho 0.1]')
fm, rho = 50, 0.1
given('P2Q1 knowns', '50 0.1', 'fD = 50 Hz，最低信号强度 = rms 值的 0.1')
on_page('P2Q1 rho reading', '信号强度（幅度）的 0.1 → ρ = 0.1，ρ² = 0.01（−20 dB）')
den = S2P * fm * rho
chk('denominator', den, '12.53', lit=2.5066 * 50 * 0.1, snip='2.5066 × 50 × 0.1 = 12.53')
chk('AFD (ms)', afd(fm, rho) * 1e3, '0.802', lit=0.01005 / 12.53 * 1e3, snip='0.01005 / 12.53 = 0.802 ms')
chk('LCR', lcr(fm, rho), '12.41', lit=12.53 * 0.99005, snip='12.53 × 0.99005 = 12.41 次/s（原题没问）')
chk('LCR x AFD', lcr(fm, rho) * afd(fm, rho), '0.00995', lit=12.41 * 0.802e-3, snip='12.41 × 0.802 ms = 0.00995 ✓')
chk('official answer 0.8 ms', afd(fm, rho) * 1e3, '0.8', snip='官方答案 0.8 ms')
P2_L, P2_A = lcr(fm, rho), afd(fm, rho)

head('2g. table (B) formula: mock A Q3(c)  [1.8 GHz, 72 km/h, 50 ksps, power 10 dB below rms]')
given('mock A knowns', '1.8 72 50 10', 'fc = 1.8 GHz，72 km/h，50 k 符号/s，功率不能比 rms 低 10 dB 以上')
rho = 10 ** (-10 / 20)
fm = fm_of(72, 1.8e9)
chk('rho^2', rho ** 2, '0.1', snip='功率低 10 dB → ρ² = 10−1 = 0.1，ρ = √0.1 = 0.31623')
chk('rho', rho, '0.31623', snip='ρ = √0.1 = 0.31623')
chk('v (m/s)', 72 / 3.6, '20', lit=72 / 3.6, snip='72 ÷ 3.6 = 20 m/s')
chk('fm = v/lambda', fm, '120', lit=20 * 1.8e9 / 3e8, snip='20 × 1.8×10⁹ / 3×10⁸ = 120 Hz')
den = S2P * fm * rho
chk('denominator', den, '95.12', lit=2.5066 * 120 * 0.31623, snip='2.5066 × 120 × 0.31623 = 95.12')
chk('AFD (ms)', afd(fm, rho) * 1e3, '1.106', lit=0.1052 / 95.12 * 1e3, snip='0.1052 / 95.12 = 1.106 ms')
chk('LCR', lcr(fm, rho), '86.07', lit=95.12 * 0.90484, snip='95.12 × 0.90484 = 86.07 次/s（原题没问）')
chk('LCR x AFD', lcr(fm, rho) * afd(fm, rho), '0.0952', lit=86.07 * 1.106e-3, snip='86.07 × 1.106 ms = 0.0952 ✓')
chk('symbols per fade', afd(fm, rho) * 50e3, '55.3', lit=1.106e-3 / 20e-6, snip='1.106 ms / 20 µs = 55.3 ≈ 55 个')
chk('symbols per fade (integer)', afd(fm, rho) * 50e3, '55', snip='≈ 55 个')
A_mockA = afd(fm, rho)
A_wrong = afd(fm, 0.1)

head('2h. table (C) reverse: Practice 2 Q1 back-check')
fr = P2_L * P2_A
chk('(1) fraction', fr, '0.00995', lit=12.41 * 0.802e-3, snip='12.41 × 0.802 ms = 0.00995 |')
chk('1 - fraction', 1 - fr, '0.99005', snip='ln(1/0.99005) = 0.0100')
r2 = math.log(1 / (1 - fr))
chk('(2) rho^2', r2, '0.0100', lit=math.log(1 / 0.99005), snip='ln(1/0.99005) = 0.0100')
chk('(3) dB', dB(r2), '-20.0', lit=dB(0.0100), snip='−20.0 dB，ρ = 0.100 ✓')
chk('(3) rho', math.sqrt(r2), '0.100', lit=math.sqrt(0.0100), snip='ρ = 0.100 ✓')
chk('(4) fm back', P2_L / (S2P * math.sqrt(r2) * math.exp(-r2)), '50.0', lit=12.41 / (2.5066 * 0.1 * 0.990),
    snip='12.41 / (2.5066 × 0.1 × 0.990) = 50.0 Hz ✓')

head('2i. table (C) reverse: mock C Q2(c)')
fr = 30 * 0.5e-3
chk('(1) fraction', fr, '0.015', lit=30 * 0.5e-3, snip='30 × 0.5 ms = 0.015 |')
chk('1 - fraction', 1 - fr, '0.985', snip='ln(1/0.985) = 0.01511')
r2 = math.log(1 / (1 - fr))
rho = math.sqrt(r2)
chk('(2) rho^2', r2, '0.01511', lit=math.log(1 / 0.985), snip='ln(1/0.985) = 0.01511')
chk('(3) 10log10 rho^2', dB(r2), '-18.21', lit=dB(0.01511), snip='−18.21 dB，ρ = 0.1229')
chk('(3) 20log10 rho (same)', 20 * math.log10(rho), '-18.21', snip='（模拟 C：−18.21 dB）')
chk('(3) rho', rho, '0.1229', lit=math.sqrt(0.01511), snip='ρ = 0.1229')
chk('(4) e^-rho^2', math.exp(-r2), '0.985', snip='0.1229 × 0.985)')
chk('(4) fm back', 30 / (S2P * rho * math.exp(-r2)), '99', lit=30 / (2.5066 * 0.1229 * 0.985),
    snip='30 / (2.5066 × 0.1229 × 0.985) ≈ 99 Hz（题目给 100 Hz）✓')
given('mock C given fm', '100', '题目给 100 Hz')

head('2j. example 1  [Rs 25 ksps, 150 fades in 10 s, AFD 0.8 ms]')
given('ex1 knowns', '25 10 150 0.8 100', '符号速率 Rs = 25 k 符号/s。记录 10 秒，共出现 150 次深衰落，平均衰落时长 0.8 ms')
on_page('ex1 rate raise', '符号速率提高到 100 k 符号/s')
Rs, A, L = 25e3, 0.8e-3, 150 / 10
chk('(a) LCR', L, '15', snip='LCR = 150 ÷ 10 s = 15 次/s')
chk('Rs written out', Rs, '25000', snip='Ts = 1/25 000 = 40 µs')
chk('(b) Ts (us)', 1 / Rs * 1e6, '40', lit=1 / 25000 * 1e6, snip='Ts = 1/25 000 = 40 µs')
chk('(b) per fade', A * Rs, '20', lit=0.8e-3 / 40e-6, snip='0.8 ms ÷ 40 µs = 20 个')
chk('(b) AFD x Rs', A * Rs, '20', lit=0.8e-3 * 25e3, snip='0.8×10⁻³ × 25×10³ = 20')
chk('(c) errors/s', L * A * Rs, '300', lit=15 * 20, snip='15 × 20 = 300 个/s')
chk('(d) SER', L * A, '0.012', lit=300 / 25000, snip='SER = 300 ÷ 25 000 = 0.012')
chk('(d) LCR x AFD', L * A, '0.012', lit=15 * 0.8e-3, snip='15 × 0.8 ms = 0.012 ✓')
chk('(d) percent', L * A * 100, '1.2', snip='信号 1.2% 的时间')
chk('(e) per fade at 100 ksps', A * 100e3, '80', lit=0.8e-3 * 100e3, snip='0.8 ms × 100 k = 80 个')
chk('(e) errors/s at 100 ksps', L * A * 100e3, '1200', lit=15 * 80, snip='15 × 80 = 1200 个')
chk('(e) SER unchanged', L * A, '0.012', snip='SER 仍是 0.012')

head('2k. example 2  [10% of rms, 900 MHz, 60 km/h, 100 ksps]')
given('ex2 knowns', '900 60 10 100', '载频 900 MHz，车速 60 km/h，瑞利衰落；能正常工作的最低信号强度是 rms 值的 10%；符号速率 100 k 符号/s')
rho, fc, Rs = 0.1, 900e6, 100e3
fm = fm_of(60, fc)
chk('(a) rho^2', rho ** 2, '0.01', snip='ρ = 0.1，ρ² = 0.01（门限比平均功率低 20 dB）')
chk('(a) dB below', -dB(rho ** 2), '20', snip='门限比平均功率低 20 dB')
chk('(a) v (m/s)', 60 / 3.6, '16.67', lit=60 / 3.6, snip='v = 60 ÷ 3.6 = 16.67 m/s')
chk('(a) fm = v fc / c', fm, '50.0', lit=16.67 * 9e8 / 3e8, snip='16.67 × 9×10⁸ / 3×10⁸ = 50.0 Hz')
chk('(a) lambda (m)', C / fc, '0.3333', snip='λ = c/fc = 0.3333 m')
chk('(a) v / lambda', fm, '50.0', lit=16.67 / 0.3333, snip='v/λ = 50.0 Hz')
chk('(b) denominator', S2P * fm * rho, '12.53', snip='√(2π) × 50 × 0.1 = 12.53')
chk('(b) LCR', lcr(fm, rho), '12.41', lit=12.53 * math.exp(-0.01), snip='12.53 × e−0.01 = 12.41 次/s')
chk('(b) AFD (ms)', afd(fm, rho) * 1e3, '0.802', lit=0.01005 / 12.53 * 1e3, snip='0.01005/12.53 = 0.802 ms')
chk('(c) per fade', afd(fm, rho) * Rs, '80.2', lit=0.802e-3 * 100e3, snip='0.802 ms × 100 k = 80.2 ≈ 80 个')
chk('(c) per fade integer', afd(fm, rho) * Rs, '80', snip='每次约 80 个')
chk('(c) errors/s', lcr(fm, rho) * afd(fm, rho) * Rs, '995', lit=12.41 * 80.2, snip='12.41 × 80.2 = 995 个')
chk('(c) check (1-e^-0.01) x 1e5', (1 - math.exp(-0.01)) * 1e5, '995', snip='(1 − e−0.01) × 10⁵ = 995 ✓')
chk('(c) fades in 10 s', lcr(fm, rho) * 10, '124', lit=12.41 * 10, snip='12.41 × 10 = 124 次深衰落')
fm2 = fm_of(120, fc)
chk('(d) fm at 120 km/h', fm2, '100', snip='120 km/h → fm = 100 Hz')
chk('(d) LCR', lcr(fm2, rho), '24.82', lit=12.41 * 2, snip='LCR 翻倍为 24.82 次/s')
chk('(d) AFD (ms)', afd(fm2, rho) * 1e3, '0.401', lit=0.802 / 2, snip='AFD 减半为 0.401 ms')
chk('(d) per fade', afd(fm2, rho) * Rs, '40.1', snip='每次只错 40.1 个')
chk('(d) fraction', lcr(fm2, rho) * afd(fm2, rho), '0.00995', snip='LCR × AFD = 1 − e−0.01 = 0.00995 不变')
chk('(d) errors/s', lcr(fm2, rho) * afd(fm2, rho) * Rs, '995', snip='每秒仍错 995 个')

head('2l. example 3  [threshold 15 dB below rms power, fm 80 Hz, Rs 40 ksps]')
given('ex3 knowns', '15 80 40', '低 15 dB，fm = 80 Hz，符号速率 40 k 符号/s')
given('ex3 SER target', '10 3', '要求 SER ≤ 10⁻³')
X, fm, Rs = 15, 80, 40e3
r2 = 10 ** (-X / 10)
rho = 10 ** (-X / 20)
chk('(a) rho^2', r2, '0.03162', snip='ρ² = 10−15/10 = 10−1.5 = 0.03162')
chk('(a) rho', rho, '0.17783', lit=math.sqrt(10 ** -1.5), snip='ρ = √ρ² = 10−15/20 = 0.17783')
ser = p_below(rho)
chk('(a) SER = 1-e^-rho^2', ser, '0.03113', lit=1 - math.exp(-0.03162), snip='1 − e−0.03162 = 0.03113（约 3.1%）')
chk('(a) SER %', ser * 100, '3.1', snip='约 3.1%')
den = S2P * fm * rho
chk('(b) denominator', den, '35.66', lit=2.5066 * 80 * 0.17783, snip='2.5066 × 80 × 0.17783 = 35.66')
chk('(b) e^-rho^2', math.exp(-r2), '0.9689', snip='35.66 × 0.9689 = 34.55')
chk('(b) LCR', lcr(fm, rho), '34.55', lit=35.66 * 0.9689, snip='35.66 × 0.9689 = 34.55 次/s')
chk('(b) e^rho^2 - 1', math.exp(r2) - 1, '0.03213', lit=math.exp(0.03162) - 1, snip='0.03213/35.66 = 0.901 ms')
chk('(b) AFD (ms)', afd(fm, rho) * 1e3, '0.901', lit=0.03213 / 35.66 * 1e3, snip='= 0.03213/35.66 = 0.901 ms')
chk('(b) per fade', afd(fm, rho) * Rs, '36.04', lit=0.901e-3 * 40e3, snip='0.901 ms × 40 k = 36.04 个')
chk('(b) errors/s', lcr(fm, rho) * afd(fm, rho) * Rs, '1245', lit=34.55 * 36.04, snip='34.55 × 36.04 = 1245 个')
chk('(b) SER x Rs', ser * Rs, '1245', lit=0.03113 * 40000, snip='0.03113 × 40 000 = 1245 ✓')
chk('Rs written out', Rs, '40000', snip='× 40 000 = 1245')
eps = 1e-3
r2max = math.log(1 / (1 - eps))
chk('(c) rho^2 max (x1e-3)', r2max * 1e3, '1.0005', snip='ln[1/(1 − 0.001)] = 1.0005×10⁻³')
chk('(c) margin dB (4 s.f.)', dB(1 / r2max), '30.00', snip='10 log₁₀(1/ρ²) ≥ 30.00 dB')
chk('(c) margin dB (3 s.f.)', dB(1 / r2max), '30.0', snip='平均功率至少比门限高 30.0 dB')
chk('(c) = fade margin formula at eps 0.1%', 10 * math.log10(1 / math.log(1 / (1 - 0.001))), '30.0', snip='ε = 0.1% 时的瑞利衰落余量')
chk('answer SER', ser, '0.0311', snip='SER ≈ 0.0311')

head('2m. traps, slide example, exam English')
chk('trap: rho = 0.1 by mistake, AFD (ms)', A_wrong * 1e3, '0.334', snip='AFD 会算成 0.334 ms，真值 1.106 ms')
ratio = A_mockA / A_wrong
ok = 3 < ratio < 4
print(f'[{"OK " if ok else "BAD"}] trap: "差 3 倍多": ratio {ratio:.3f}')
if not ok:
    FAIL.append('ratio 3 倍多')
chk('trap: 0.5 ms / 20 us', 0.5e-3 / 20e-6, '25', snip='0.5 ms ÷ 20 µs = 25（不是 0.025）')
chk('trap: unit slip 0.5/20', 0.5 / 20, '0.025', snip='（不是 0.025）')
chk('trap: LCR 30 vs 750 errors', 300 / 10, '30', snip='模拟 C 是 30 次/s，却是 750 个/s')
fm = fm_of(120, 5e9)
chk('slide example LCR', lcr(fm, 0.1), '137.87', snip='9812 = 137.87 × 71.17')
chk('slide example AFD (us)', afd(fm, 0.1) * 1e6, '72.17', snip='按讲义自己的公式是 72.17 µs、9950 个')
chk('slide example errors/s', lcr(fm, 0.1) * afd(fm, 0.1) * 1e6, '9950', snip='72.17 µs、9950 个')
chk('slide misprint reproduced', 137.87 * 71.17, '9812', lit=lcr(fm, 0.1) * 71.17, snip='9812 = 137.87 × 71.17')
given('slide misprint AFD', '71.17', '例题印的 AFD = 71.17 µs、每秒 9812 个')
chk('English: LCR', 40 / 10, '4', snip='LCR = 40/10 s = 4 fades/s')
chk('English: per fade', 20 / 5, '4', snip='AFD/Ts = 20 ms/5 ms = 4 consecutive symbols')
chk('English: errors/s', 16, '16', lit=4 * 4, snip='4 × 4 = 16 symbols/s')
chk('English: AFD (ms)', afd(50, 0.1) * 1e3, '0.802', lit=0.01005 / 12.53 * 1e3, snip='= 0.01005/12.53 = 0.802 ms. Check')
chk('English: fraction', 1 - math.exp(-0.01), '0.00995', snip='1 − e−ρ² = 0.00995, the fraction of time')

# ================================================================== 3. generic scans
head('3a. every unit-free chain "a op b ... = d" on the page, evaluated literally')
TEX = re.compile(r'\\\(.*?\\\)|\\\[.*?\\\]', re.S)
plain = re.sub(r'(\d) (\d{3})(?!\d)', r'\1\2', TEX.sub(' ', TEXT))
ALLOWED = set('0123456789.×÷/() ')
nchain = 0
for m in re.finditer(r'=\s*(\d+(?:\.\d+)?)', plain):
    res, j = m.group(1), m.start()
    i = j
    while i > 0 and plain[i - 1] in ALLOWED:
        i -= 1
    expr = plain[i:j].strip()
    prev = plain[i - 1] if i > 0 else ''
    if not expr or not re.search(r'[×÷/]', expr) or not re.match(r'[\d(]', expr):
        continue
    if prev in '−-^⁻√' or (expr.startswith('(') and re.match(r'[A-Za-zπ]', prev or ' ')):
        continue
    if expr.count('(') != expr.count(')'):
        continue
    tail = plain[m.end():m.end() + 4].lstrip()
    scale = 1e-3 if tail.startswith('ms') else 1e-6 if tail.startswith('µs') else 1.0
    try:
        val = eval(expr.replace('×', '*').replace('÷', '/'), {'__builtins__': {}}) / scale
    except Exception:
        continue
    nchain += 1
    ok = rnd(val, res) == res
    print(f'[{"OK " if ok else "BAD"}] {expr} = {res}{" (" + tail[:2] + ")" if scale != 1 else ""}: literal {val:.7g}')
    if not ok:
        FAIL.append(f'chain {expr} = {res}')
print(f'      {nchain} chains evaluated')

head('3b. numeric tokens on the page that section 2 did not account for')
LABELS = {  # labels, page numbers, formula constants (not computed values)
    '2024', '25', '2025', '26', '6129', '1', '2', '3', '8', '41', '42', '43', '45', '47', '34', '36', '51',
    '10', '20', '0', '9', '5', '6', '50', '0.5', '0.8', '120', '0.001', '100', '60', '900', '1.8', '72', '80',
    '15', '40', '150', '300', '1.5', '0.1', '3.6'}
unexplained = {}
for m in re.finditer(r'\d+(?:\.\d+)?', plain):
    t = m.group(0)
    if t in SHOWN or t in LABELS:
        continue
    unexplained.setdefault(t, plain[max(0, m.start() - 40):m.end() + 25])
for t, ctx in unexplained.items():
    print(f'[BAD] token {t!r} not verified: ...{ctx}...')
    FAIL.append('token ' + t)
print(f'      {len(unexplained)} unexplained tokens')

# ================================================================== 4. HTML / format
head('4. HTML and format')
VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'wbr', 'col', 'source'}


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.kids, self.text = tag, dict(attrs), parent, [], ''

    def cls(self):
        return self.attrs.get('class', '').split()

    def alltext(self):
        return self.text + ''.join(k.alltext() for k in self.kids)

    def find(self, tag=None, cls=None):
        out = []
        for k in self.kids:
            if (tag is None or k.tag == tag) and (cls is None or cls in k.cls()):
                out.append(k)
            out += k.find(tag, cls)
        return out


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('#root', [], None)
        self.cur, self.errors = self.root, []

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.cur.tag == tag:
            self.cur = self.cur.parent
            return
        self.errors.append(f'</{tag}> closes <{self.cur.tag}> at line {self.getpos()[0]}')
        p = self.cur
        while p is not None and p.tag != tag:
            p = p.parent
        if p is not None:
            self.cur = p.parent

    def handle_data(self, d):
        self.cur.text += d


tb = Tree()
tb.feed(RAW)
tb.close()
unclosed = []
p = tb.cur
while p is not None and p.tag != '#root':
    unclosed.append(p.tag)
    p = p.parent


def rep(label, ok, detail=''):
    global NCHK
    NCHK += 1
    print(f'[{"OK " if ok else "BAD"}] {label}' + (f': {detail}' if detail else ''))
    if not ok:
        FAIL.append(label)


rep('html.parser: no mismatched end tags', not tb.errors, '; '.join(tb.errors))
rep('html.parser: no unclosed tags', not unclosed, ', '.join(unclosed))
rep('no <style>/<script>/<html>/<head>/<body>', not re.search(r'<\s*(style|script|html|head|body)\b', RAW, re.I))
spans = [m.group(0) for m in TEX.finditer(RAW)]
bad = [s for s in spans if re.search(r'[<>]|&lt;|&gt;', s)]
rep(f'TeX: {len(spans)} math spans, none with raw < > or &lt; &gt;', not bad, ' | '.join(bad))
cjk = [s for s in spans if re.search(r'[　-〿一-鿿＀-￯]', s)]
rep('TeX: no CJK inside math', not cjk, ' | '.join(cjk))
unbal = [s for s in spans if s.count('{') != s.count('}')]
rep('TeX: braces balanced in every span', not unbal, ' | '.join(unbal))
rawlt = [m.start() for m in re.finditer(r'<(?![a-zA-Z/!])', RAW)]
rep('no raw < in text outside tags', not rawlt, str(rawlt[:5]))

secs = tb.root.find('section')
rep('exactly one <section class="topic" id="t10">', len(secs) == 1 and secs[0].cls() == ['topic'] and secs[0].attrs.get('id') == 't10')
sec = secs[0]
top = [k for k in sec.kids]
seq = [(k.tag, (k.cls() or [''])[0]) for k in top]
rep('h2 first, with <span class="tn">10</span> and " · "', seq[0][0] == 'h2' and top[0].kids and top[0].kids[0].tag == 'span'
    and top[0].kids[0].cls() == ['tn'] and top[0].kids[0].alltext() == '10' and ' · ' in top[0].alltext())
meta = top[1]
sts = [s for s in meta.kids if 'st' in s.cls()]
rep('div.meta with status spans and span.freq "出现："', meta.tag == 'div' and meta.cls() == ['meta'] and sts
    and all(len(s.cls()) == 2 and s.cls()[1] in ('must', 'try', 'give', 'def') for s in sts)
    and any(s.cls() == ['freq'] and s.alltext().startswith('出现：') for s in meta.kids))
rep('p.why third', top[2].tag == 'p' and top[2].cls() == ['why'])
h3s = [k.alltext() for k in top if k.tag == 'h3']
rep('h3 order', h3s == ['符号与含义 · Symbols', '公式 · Formulas', '解题步骤 · Steps', '中文例子 · 怎么用', '易错 · Traps'], str(h3s))
sym = sec.find('table', 'sym')
ths = [t.alltext() for t in sym[0].find('th')] if sym else []
rows = sym[0].find('tr')[1:] if sym else []
rep('symbol table: 5 headers, every row 5 cells', ths == ['符号', '中文', 'English', '含义（大白话）', '单位']
    and all(len(r.find('td')) == 5 for r in rows), f'{len(rows)} rows')
fms = sec.find('div', 'fm')
okfm = all([k.cls() for k in f.kids][:3] == [['fl'], ['fx'], ['fn']] and f.kids[0].find('span', 'st') for f in fms)
rep(f'{len(fms)} formula cards, each .fl(.st) .fx .fn', okfm and len(fms) >= 3)
EXPECT = [('LCR 的定义', 'def'), ('每次衰落错几个符号', 'def'), ('每秒误符号数', 'def'), ('深衰落时间比例与误符号率', 'def'),
          ('瑞利衰落的 LCR 与 AFD', 'give'), ('两式相乘', 'must'), ('ρ 怎么从题目文字读出来', 'def'), ('最大多普勒频移', 'def')]
got = [(f.kids[0].alltext(), f.kids[0].find('span', 'st')[0].cls()[1]) for f in fms]
okb = len(got) == len(EXPECT) and all(g[0].startswith(e[0]) and g[1] == e[1] for g, e in zip(got, EXPECT))
rep('formula badges match quiz_marks.py / notes.py (两式相乘 = 背 because it is the Rayleigh outage)', okb, str(got))
steps = sec.find('table', 'steps')
oks = True
for t in steps:
    th = [x.alltext() for x in t.find('th')]
    oks &= len(th) == 4 and th[:2] == ['步骤', '做法'] and all(len(r.find('td')) == 4 for r in t.find('tr')[1:])
    tw = t.parent
    idx = top.index(tw)
    oks &= top[idx + 1].tag == 'p' and top[idx + 1].cls() == ['src'] and top[idx + 1].alltext().startswith('来源：')
rep(f'{len(steps)} steps tables: 4 columns, 步骤/做法 headers, followed by p.src 来源：', oks and len(steps) >= 1)
heads = [[x.alltext() for x in t.find('th')][2:] for t in steps]
print('      steps columns:', heads)
first = [x.alltext() for x in steps[0].find('tr')[1:4]]
rep('table (A) keeps the user\'s three rows', [r.find('td')[0].alltext() for r in steps[0].find('tr')[2:5]] == ['① LCR', '② 每次衰落错几个符号', '③ 每秒误符号数'])
ex_i = [i for i, k in enumerate(top) if k.tag == 'h3' and k.alltext() == '中文例子 · 怎么用'][0]
tr_i = [i for i, k in enumerate(top) if k.tag == 'h3' and k.alltext() == '易错 · Traps'][0]
egs = [k for k in top[ex_i + 1:tr_i] if 'eg' in k.cls()]
okeg = all([c.cls()[0] if c.cls() else c.tag for c in e.kids] == ['egh', 'q', 'work', 'ans'] and e.kids[2].tag == 'ol'
           and e.kids[3].alltext().startswith('答案') for e in sec.find('div', 'eg'))
rep(f'examples section has 2-3 .eg ({len(egs)}); every .eg is .egh p.q ol.work p.ans(答案)', 2 <= len(egs) <= 3 and okeg)
trap = sec.find('ul', 'trap')
rep('ul.trap with 3-6 items', len(trap) == 1 and 3 <= len(trap[0].find('li')) <= 6, f'{len(trap[0].find("li"))} items')
en = sec.find('div', 'en')
rep('div.en last, .enl "英文答题模板 · Exam English", >= 1 p', top[-1] is en[0] and en[0].kids[0].cls() == ['enl']
    and en[0].kids[0].alltext() == '英文答题模板 · Exam English' and len(en[0].find('p')) >= 1)
m = re.search(r'<section class="topic" id="(t\d+)">.*?</section>', RAW, re.S)
rep('build_quizsum.py regex extracts the whole section', m is not None and m.group(0) == RAW.strip())

print(f'\n{NCHK} checks, {len(FAIL)} failures')
for f in FAIL:
    print('  FAIL:', f)
