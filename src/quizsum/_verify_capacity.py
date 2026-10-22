#!/usr/bin/python3
"""Independent re-check of frag_capacity.html (t11 Shannon / SNR-SIR-SINR, t12 Rayleigh outage capacity and
fade margin, t13 water-filling). Written from scratch: it does not import or copy check_capacity.py.

Part 1 recomputes every number in the fragment, labelled by where it appears (table column / example / trap).
Part 2 independent cross-checks of the methods:
  * Rayleigh CDF: numerical integration of the exponential SNR pdf must give 1 - e^(-g0/gbar) = eps;
  * water-filling: (i) lecture loop "assume all on, drop the worst, recompute", (ii) bisection on the water
    level, (iii) brute-force search over power splits -> the water-filling capacity must be the maximum;
  * Shannon inverse: B log2(1 + (2^(R/B) - 1)) must give R back.
Part 3 scans the fragment: every number token outside TeX must equal (after rounding to the precision shown)
a value computed here or a given input. Unmatched tokens are printed for manual review.
stdlib only (Q via statistics.NormalDist is not needed for t11-t13).   usage: /usr/bin/python3 _verify_capacity.py
"""
import html
import math
import pathlib
import random
import re

HERE = pathlib.Path(__file__).parent
FRAG = HERE / 'frag_capacity.html'

V = []                                     # (label, value); everything printed is registered for Part 3


def reg(label, x):
    V.append((label, x))
    return x


def show(label, x, fmt='.6g'):
    reg(label, x)
    print(f'  {label:<66s} {x:{fmt}}')
    return x


def head(s):
    print(f'\n### {s}')


def db(x):                                 # power ratio -> dB
    return 10.0 * math.log10(x)


def undb(d):                               # dB -> power ratio
    return 10.0 ** (d / 10.0)


def lg2(x):                                # log base 2 via natural log (independent of math.log2)
    return math.log(x) / math.log(2.0)


def lnterm(eps):                           # ln(1/(1-eps)) written as -ln(1-eps)
    return -math.log1p(-eps)


# given inputs that appear in the fragment text (question data, eps in %, etc.)
GIVEN = [10, 0.1, 20, 2, 0.5, 0.05, 10, -90, -174, 5, 25, 0.005, 0.5, 20, 0.01, 1, 7, 0.001, 0.1, 30, 0.02,
         1, 1000, 2, 0.05, 15, 18, 3, 1, 12, 6, -3, 0, -5, 17.77, 2.63, 0.087, 8, 0.2, 1e-9, -9, 6, 100, 4,
         40, 50, 2.5, 0.995, 0.99, 0.999, 0.98, 0.95, 1.0, 0.3010, 0.6931, -100,
         101, 41, 201, 11, 51, 21]                  # 1 + SNR arguments of log2 written as integers
for i, g in enumerate(GIVEN):
    reg(f'given[{i}]', g)

print('PART 1 - every number in frag_capacity.html, recomputed')

# =========================================================================================== t11
head('t11 symbols: log2 via a calculator')
show('log10(2)  (log2 x = log10 x / 0.3010)', math.log10(2))
show('ln(2)     (log2 x = ln x / 0.6931)', math.log(2))
show('10 log10 2 (B doubled -> N +3.01 dB)', db(2))

head('t11 table 1, col 3: Practice 2 Q3 (S = I = 10 mW, N = 0.1 mW, B = 20 MHz)')
S, I, N, B = 10.0, 10.0, 0.1, 20e6
x = show('SINR1 = 10/(10 + 0.1)', S / (I + N))
show('SINR1 in dB', db(x))
show('1 + SINR1', 1 + x)
show('log2(1 + SINR1)', lg2(1 + x))
C1 = show('C1 (Mbps) = 20 x log2(1.990)', B * lg2(1 + x) / 1e6)
y = show('SNR2 = 10/0.1 (after MUD)', S / N)
show('SNR2 in dB', db(y))
show('log2(101)', lg2(101))
C2 = show('C2 (Mbps) = 20 x log2(101)', B * lg2(1 + y) / 1e6)
show('C1 + C2 (Mbps)', C1 + C2)
show('log2(201)', lg2(201))
show('sum-rate check 20 x log2(1 + 20/0.1) (Mbps)', 20 * lg2(1 + (S + I) / N))

head('t11 table 1, col 4: mock C Q3 (a)(b) (S = 2 mW, I = 0.5 mW, N = 0.05 mW, B = 10 MHz)')
S, I, N, B = 2.0, 0.5, 0.05, 10e6
snr = show('SNR = 2/0.05', S / N)
show('SNR dB', db(snr))
sir = show('SIR = 2/0.5', S / I)
show('SIR dB', db(sir))
sinr = show('SINR = 2/(0.5 + 0.05)', S / (I + N))
show('SINR dB', db(sinr))
show('1 + SINR', 1 + sinr)
show('log2(1 + SINR)', lg2(1 + sinr))
Ca = show('C (a) Mbps', B * lg2(1 + sinr) / 1e6)
show('log2(41)', lg2(41))
Cb = show('C (b) Mbps (I removed)', B * lg2(1 + snr) / 1e6)
show('ratio C(b)/C(a)', Cb / Ca)
show('I/N', I / N)

head('t11 table 2: mock B Q3 (a)(b) (S = -90 dBm, N0 = -174 dBm/Hz, B = 5 MHz then 10 MHz)')
caps = {}
for Bw, tag in ((5e6, '5 MHz'), (10e6, '10 MHz')):
    tenlogB = show(f'[{tag}] 10 log10 B', db(Bw))
    NdBm = show(f'[{tag}] N = -174 + 10 log10 B (dBm)', -174 + tenlogB)
    sdb = show(f'[{tag}] SNR = -90 - N (dB)', -90 - NdBm)
    show(f'[{tag}] exponent SNR_dB/10', sdb / 10)
    s = show(f'[{tag}] SNR linear', undb(sdb))
    show(f'[{tag}] 1 + SNR', 1 + s)
    show(f'[{tag}] log2(1 + SNR)', lg2(1 + s))
    caps[tag] = show(f'[{tag}] C (Mbps)', Bw * lg2(1 + s) / 1e6)
show('ratio C(10 MHz)/C(5 MHz)', caps['10 MHz'] / caps['5 MHz'])

head('t11 example 1: S = 10 mW, N0 = 1e-9 W/Hz, B = 1 MHz -> 2 MHz')
S, N0 = 10e-3, 1e-9
ex1 = {}
for Bw, tag in ((1e6, '1 MHz'), (2e6, '2 MHz')):
    Nw = show(f'[{tag}] N = N0 B (W)', N0 * Bw)
    show(f'[{tag}] N (dBm)', db(Nw / 1e-3))
    s = show(f'[{tag}] SNR', S / Nw)
    show(f'[{tag}] SNR dB', db(s))
    show(f'[{tag}] log2(1 + SNR)', lg2(1 + s))
    ex1[tag] = show(f'[{tag}] C (Mbps)', Bw * lg2(1 + s) / 1e6)
show('ratio 2 MHz / 1 MHz', ex1['2 MHz'] / ex1['1 MHz'])
show('power doubled to 20 mW, SNR stays 10: 2 MHz x log2 11 (Mbps)', 2 * lg2(11))

head('t11 example 2: B = 5 MHz, R = 20 Mbps, N = -100 dBm')
show('R/B', 20 / 5)
smin = show('SNR_min = 2^4 - 1', 2 ** (20 / 5) - 1)
show('SNR_min dB', db(smin))
show('S_min = -100 + SNR_min,dB (dBm)', -100 + db(smin))
show('(c) 10 dB linear', undb(10))
show('(c) C = 5 x log2(11) (Mbps)', 5 * lg2(1 + undb(10)))

head('t11 example 3: P1 = 8 mW, P2 = 2 mW, N = 0.2 mW, B = 10 MHz each')
P1, P2, N, B = 8.0, 2.0, 0.2, 10.0      # B in MHz -> C in Mbps
a1 = show('(a) SINR1 = 8/(2 + 0.2)', P1 / (P2 + N))
show('(a) SINR1 dB', db(a1))
show('(a) 1 + SINR1', 1 + a1)
show('(a) log2(1 + SINR1)', lg2(1 + a1))
c1 = show('(a) C1 (Mbps)', B * lg2(1 + a1))
a2 = show('(a) SNR2 = 2/0.2', P2 / N)
show('(a) SNR2 dB', db(a2))
show('(a) log2(11)', lg2(11))
c2 = show('(a) C2 (Mbps)', B * lg2(1 + a2))
show('(a) C1 + C2 (Mbps)', c1 + c2)
b2 = show('(b) SINR2 = 2/(8 + 0.2)', P2 / (P1 + N))
show('(b) SINR2 dB', db(b2))
show('(b) 1 + SINR2', 1 + b2)
show('(b) log2(1 + SINR2)', lg2(1 + b2))
d2 = show('(b) C2 (Mbps)', B * lg2(1 + b2))
b1 = show('(b) SNR1 = 8/0.2', P1 / N)
show('(b) SNR1 dB', db(b1))
d1 = show('(b) C1 (Mbps)', B * lg2(1 + b1))
show('(b) C2 + C1 (Mbps)', d1 + d2)
show('check 10 log2(1 + 10/0.2) = 10 log2 51 (Mbps)', B * lg2(1 + (P1 + P2) / N))
show('(c) no MUD: C1(a) + C2(b) (Mbps)', c1 + d2)
show('(c) fraction of the MUD sum', (c1 + d2) / (c1 + c2))

head('t11 traps')
show('wrong: log2(1 + 17.01)', lg2(1 + 17.01))
show('right: log2(1 + 10^1.701)', lg2(1 + undb(-90 + 174 - db(5e6))))

# =========================================================================================== t12
head('t12 formula card: Rayleigh fade margin for eps = 1%, 0.5%, 0.1%, 10% (exact and 10log10(1/eps))')
for e in (0.01, 0.005, 0.001, 0.1):
    show(f'eps {e}: ln(1/(1-eps))', lnterm(e))
    show(f'eps {e}: 1/ln(1/(1-eps))', 1 / lnterm(e))
    show(f'eps {e}: FM exact dB', -db(lnterm(e)))
    show(f'eps {e}: FM approx 10log10(1/eps) dB', db(1 / e))
    show(f'eps {e} in %', 100 * e)

head('t12 table 1, col 3: final 2025-26 S2 Q1(a)(iii) (gbar_R = 25 dB, eps = 0.005)')
gb = show('gbar = 10^2.5', undb(25))
L = show('ln(1/0.995)', lnterm(0.005))
gm = show('g_min = gbar x ln-term', gb * L)
show('g_min dB', db(gm))
show('FM = 25 - g_min,dB', 25 - db(gm))
show('1 + g_min', 1 + gm)
show('(not asked) C_eps/B = log2(1 + g_min) bit/s/Hz', lg2(1 + gm))
show('check 1 - exp(-g_min/gbar) (must be 0.005)', 1 - math.exp(-gm / gb))
w = show('trap: log10(1/0.995) used instead of ln', math.log10(1 / 0.995))
show('trap: wrong g_min', gb * w)
show('trap: wrong g_min dB', db(gb * w))
show('trap: wrong FM', 25 - db(gb * w))

head('t12 table 1, col 4: mock C Q3 (c) (gbar = 20 dB, eps = 1%, B = 10 MHz)')
gb = show('gbar = 10^2', undb(20))
L = show('ln(1/0.99)', lnterm(0.01))
gm = show('g_min', gb * L)
show('g_min dB', db(gm))
show('FM = 20 - g_min,dB', 20 - db(gm))
show('1 + g_min', 1 + gm)
show('log2(1 + g_min)', lg2(1 + gm))
ce = show('C_eps = 10 x log2(1 + g_min) (Mbps)', 10 * lg2(1 + gm))
cawgn = show('AWGN 10 x log2(101) (Mbps)', 10 * lg2(1 + gb))
show('ratio AWGN / C_eps', cawgn / ce)

head('t12 table 2, col 3: final 2023-24 Q1(a)(iv) (eps = 0.1%)')
show('ln(1/0.999)', lnterm(0.001))
show('1/ln-term', 1 / lnterm(0.001))
show('FM dB', -db(lnterm(0.001)))

head('t12 table 2, col 4: mock B Q1 (b) (threshold 7 dB, eps = 1%)')
g0 = show('g0 = 10^0.7', undb(7))
L = show('ln(1/0.99)', lnterm(0.01))
show('1/ln-term', 1 / L)
fm1 = show('FM dB', -db(L))
gbn = show('gbar needed = g0 / ln-term', g0 / L)
show('gbar needed dB', db(gbn))
show('7 + FM', 7 + fm1)

head('t12 example 1: gbar = 30 dB, eps = 2%, B = 1 MHz')
gb = show('gbar = 10^3', undb(30))
L = show('ln(1/0.98)', lnterm(0.02))
gm = show('g_min', gb * L)
show('g_min dB', db(gm))
show('FM = 30 - g_min,dB', 30 - db(gm))
show('FM by formula', -db(L))
show('1 + g_min', 1 + gm)
ce = show('C_eps = 1 MHz x log2(1 + g_min) (Mbps)', lg2(1 + gm))
show('(1 - eps) C_eps (Mbps)', 0.98 * ce)
show('0.98 x 4.406 (as written)', 0.98 * 4.406)
show('AWGN log2(1001) (Mbps)', lg2(1 + gb))
show('C_eps / AWGN', ce / lg2(1 + gb))
show('exponent -g_min/gbar', -gm / gb)
show('exponent -g_min (numerator as written, e^(-20.20/1000))', -gm)
show('check 1 - exp(-g_min/gbar)', 1 - math.exp(-gm / gb))

head('t12 example 2: eps = 1%, guarantee C_eps/B = 2 bit/s/Hz')
gm = show('g_min = 2^2 - 1', 2 ** 2 - 1)
show('g_min dB', db(gm))
L = show('ln(1/0.99)', lnterm(0.01))
gbn = show('gbar = 3 / ln-term', gm / L)
show('gbar dB', db(gbn))
show('FM = gbar,dB - g_min,dB', db(gbn) - db(gm))

head('t12 example 3: eps = 5% with gbar = 15 dB and 25 dB; then eps = 0.5%')
L = show('ln(1/0.95)', lnterm(0.05))
fm5 = show('FM(5%) dB', -db(L))
for gdb in (15, 25):
    gb = show(f'[{gdb} dB] gbar linear', undb(gdb))
    show(f'[{gdb} dB] exponent', gdb / 10)
    gm = show(f'[{gdb} dB] g_min', gb * L)
    show(f'[{gdb} dB] g_min dB', db(gm))
    show(f'[{gdb} dB] FM = gbar,dB - g_min,dB', gdb - db(gm))
ap = show('approx 10 log10(1/0.05)', db(1 / 0.05))
show('approx - exact', ap - fm5)
fm05 = show('FM(0.5%) dB', -db(lnterm(0.005)))
show('extra margin FM(0.5%) - FM(5%)', fm05 - fm5)

head('t12 traps: eps = 10%')
show('FM exact (10%)', -db(lnterm(0.1)))
show('FM approx (10%)', db(1 / 0.1))


# =========================================================================================== t13
def wf_lecture(g, label):
    """Lecture loop: all on -> 1/g0 = (1 + sum 1/g_i)/n -> drop the worst if any g_i < g0 -> repeat."""
    on = sorted(range(len(g)), key=lambda i: -g[i])
    rnd = 0
    while True:
        rnd += 1
        s = 1 + sum(1 / g[i] for i in on)
        inv0 = s / len(on)
        g0 = 1 / inv0
        show(f'{label} round {rnd} (n = {len(on)}): 1 + sum 1/g', s)
        show(f'{label} round {rnd}: 1/g0 (water level)', inv0)
        show(f'{label} round {rnd}: g0', g0)
        show(f'{label} round {rnd}: g0 dB', db(g0))
        bad = [i for i in on if g[i] < g0]
        for i in bad:
            show(f'{label} round {rnd}: would-be P_{i + 1}/P (negative)', inv0 - 1 / g[i])
        print(f'    {label} round {rnd}: on = {[i + 1 for i in on]}, failing g_i < g0: {[i + 1 for i in bad]}')
        if not bad:
            return on, inv0, g0
        on.remove(min(on, key=lambda i: g[i]))


def wf_bisect(g):
    """Water level mu with sum max(0, mu - 1/g_i) = 1, found by bisection (independent of the loop)."""
    lo, hi = 0.0, 1 + sum(1 / x for x in g)
    for _ in range(200):
        mu = (lo + hi) / 2
        if sum(max(0.0, mu - 1 / x) for x in g) > 1:
            hi = mu
        else:
            lo = mu
    return (lo + hi) / 2


def cap(g, p):                             # sum log2(1 + g_i p_i), p_i = P_i/P
    return sum(lg2(1 + gi * pi) for gi, pi in zip(g, p))


def brute(g, trials=200000, seed=1):
    """Best capacity over random splits (Dirichlet) and a fine grid for 2 channels."""
    rng = random.Random(seed)
    best = 0.0
    if len(g) == 2:
        for k in range(100001):
            p = k / 100000
            best = max(best, cap(g, (p, 1 - p)))
    for _ in range(trials):
        w = [rng.expovariate(1.0) for _ in g]
        t = sum(w)
        best = max(best, cap(g, [x / t for x in w]))
    return best


def wf_all(gdb, P, label, linear=False, dbshow=True):
    g = list(gdb) if linear else [undb(d) for d in gdb]
    for i, (d, x) in enumerate(zip(gdb, g), 1):
        if not linear:
            show(f'{label} g{i}: {d} dB -> 10^{d / 10:g}', x)
            show(f'{label} g{i} exponent', d / 10)
        show(f'{label} 1/g{i}', 1 / x)
    on, inv0, g0 = wf_lecture(g, label)
    mu = wf_bisect(g)
    assert abs(mu - inv0) < 1e-9, (label, mu, inv0)
    p = [inv0 - 1 / g[i] if i in on else 0.0 for i in range(len(g))]
    for i, pi in enumerate(p, 1):
        show(f'{label} P{i} (W, P = {P} W)', P * pi)
    show(f'{label} sum P_i (W)', P * sum(p))
    terms = []
    for i in on:
        r = show(f'{label} g{i + 1} x (1/g0) = g{i + 1}/g0', g[i] * inv0)
        terms.append(show(f'{label} log2(g{i + 1}/g0)', lg2(r)))
    C = show(f'{label} C = sum log2(g_i/g0) (per 1 MHz sub-band -> Mbps)', sum(terms))
    assert abs(C - cap(g, p)) < 1e-9                          # log2(g/g0) == log2(1 + g P_i/P)
    b = brute(g)
    print(f'    {label} brute-force best capacity {b:.6f} <= water-filling {C:.6f}: {b <= C + 1e-9}')
    assert b <= C + 1e-9, (label, b, C)
    return g, on, inv0, g0, p, C


head('t13 table, col 3: final 2024-25 Q1(a)(iii) (18, 10, 3 dB; P = 1 W)')
wf_all([18, 10, 3], 1, '[2024-25]')

head('t13 table, col 4: mock B Q3 (c) (SNR 20 and 0.5 linear; 1 MHz each)')
g, on, inv0, g0, p, C = wf_all([20, 0.5], 1, '[mock B Q3c]', linear=True)
show('[mock B Q3c] 20/0.952 (as written)', 20 / 0.952)
show('[mock B Q3c] log2(21)', lg2(21))
eq = show('[mock B Q3c] equal split log2(1 + 10) + log2(1 + 0.25) (Mbps)', lg2(11) + lg2(1.25))
show('[mock B Q3c] water-filling gain over equal split (Mbps)', C - eq)

head('t13 lecture example Ch2 p.56-57 (17.77, 2.63, 0.087): third sub-channel dropped')
wf_all([17.77, 2.63, 0.087], 1, '[slides]', linear=True)

head('t13 example 1: 12 dB and 6 dB, P = 2 W, 1 MHz each')
g, on, inv0, g0, p, C = wf_all([12, 6], 2, '[ex1]')
h = [x / 2 for x in g]                     # equal split: each sub-band gets P/2 -> SNR halves
show('[ex1] equal split SNR1 = g1/2', h[0])
show('[ex1] equal split SNR2 = g2/2', h[1])
show('[ex1] 1 + SNR1', 1 + h[0])
show('[ex1] 1 + SNR2', 1 + h[1])
show('[ex1] log2(1 + SNR1)', lg2(1 + h[0]))
show('[ex1] log2(1 + SNR2)', lg2(1 + h[1]))
show('[ex1] log2(8.924) (as written)', lg2(8.924))
show('[ex1] log2(2.991) (as written)', lg2(2.991))
show('[ex1] equal split C (Mbps)', lg2(1 + h[0]) + lg2(1 + h[1]))
show('[ex1] log2(10.42) (as written)', lg2(10.42))
show('[ex1] log2(2.616) (as written)', lg2(2.616))

head('t13 example 2: 15, 6, -3 dB, P = 1 W, 1 MHz each (third sub-band dropped)')
wf_all([15, 6, -3], 1, '[ex2]')
show('[ex2] 1.0927 - 1.9953 (as written)', 1.0927 - 1.9953)

head('t13 example 3: 20, 10, 0, -5 dB, P = 1 W, 1 MHz each (dropped twice)')
wf_all([20, 10, 0, -5], 1, '[ex3]')
show('[ex3] log2(55.5)', lg2(55.5))
show('[ex3] log2(5.55)', lg2(5.55))

# =========================================================================================== Part 2
print('\nPART 2 - independent method checks')
for gbar_db, g0_db in ((20, 7), (25, 2.0006), (30, 13.054)):
    gbar, g0 = undb(gbar_db), undb(g0_db)
    n = 20000                               # Simpson integration of p(g) = (1/gbar) e^(-g/gbar) on [0, g0]
    hstep = g0 / n
    acc = sum((1 if k in (0, n) else 4 if k % 2 else 2) * math.exp(-(k * hstep) / gbar) / gbar for k in range(n + 1))
    integ = acc * hstep / 3
    print(f'  Rayleigh CDF gbar {gbar_db} dB, g0 {g0_db} dB: integral {integ:.8f} vs 1 - e^(-g0/gbar) {1 - math.exp(-g0 / gbar):.8f}')
    assert abs(integ - (1 - math.exp(-g0 / gbar))) < 1e-9
for R, Bw in ((20, 5), (2, 1)):
    s = 2 ** (R / Bw) - 1
    assert abs(Bw * lg2(1 + s) - R) < 1e-12
print('  Shannon inverse SNR = 2^(R/B) - 1 reproduces R: ok')
for e in (0.001, 0.005, 0.01, 0.02, 0.05, 0.1):  # FM from the ratio equals FM from the closed form
    gbar = 123.4
    gmin = gbar * lnterm(e)
    assert abs((db(gbar) - db(gmin)) - (-db(lnterm(e)))) < 1e-12
print('  FM = gbar_dB - gmin_dB = 10log10(1/ln(1/(1-eps))) for any gbar: ok')

# =========================================================================================== Part 3
print('\nPART 3 - every number token in the fragment (outside TeX) must match a value above')
raw = FRAG.read_text(encoding='utf-8')
tex = re.findall(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', raw, flags=re.S)
txt = re.sub(r'\\\(.*?\\\)|\\\[.*?\\\]', ' ', raw, flags=re.S)
txt = re.sub(r'<[^>]+>', ' ', txt)
txt = html.unescape(txt)
txt = txt.replace('log₂', 'log_2 ').replace('log₁₀', 'log_10 ')
tok = re.compile(r'(?<![A-Za-z0-9_.])(−?)(\d+(?:\.\d+)?)')
vals = list(V)
verbose = '-v' in __import__('sys').argv
unmatched, signonly, n = [], [], 0
for m in tok.finditer(txt):
    sgn, num = m.group(1), m.group(2)
    t = float(num) * (-1 if sgn else 1)
    dec = len(num.split('.')[1]) if '.' in num else 0
    tol = 0.5 * 10 ** (-dec) * (1 + 1e-9) + 1e-12
    n += 1
    hit = [lab for lab, v in vals if abs(v - t) <= tol]
    if hit:
        if verbose:
            print(f'  ok {sgn + num:>10s}  <- {hit[0]}')
        continue
    ctx = txt[max(0, m.start() - 40):m.end() + 25].replace('\n', ' ')
    ctx = re.sub(r'\s+', ' ', ctx)
    if any(abs(abs(v) - abs(t)) <= tol for _, v in vals):
        signonly.append((sgn + num, ctx))
    else:
        unmatched.append((sgn + num, ctx))
print(f'  tokens checked: {n}; unmatched: {len(unmatched)}; sign-only matches: {len(signonly)}')
for s, c in signonly:
    print(f'  SIGN?     {s:>10s}   ...{c}...')
for s, c in unmatched:
    print(f'  UNMATCHED {s:>10s}   ...{c}...')
nums_in_tex = sorted({x for a, b in tex for x in re.findall(r'\d+(?:\.\d+)?', a + b)}, key=float)
print(f'  TeX segments: {len(tex)}; numbers inside TeX (symbolic formulas only): {nums_in_tex}')

# =========================================================================================== Part 4
print('\nPART 4 - format: balanced tags, TeX hygiene, required blocks per topic')
from html.parser import HTMLParser

VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'wbr', 'col', 'source', 'area', 'base', 'embed', 'param', 'track'}


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.root = [], [], {'tag': 'root', 'attrs': {}, 'kids': [], 'text': ''}
        self.cur = [self.root]

    def handle_starttag(self, tag, attrs):
        node = {'tag': tag, 'attrs': dict(attrs), 'kids': [], 'text': '', 'line': self.getpos()[0]}
        self.cur[-1]['kids'].append(node)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))
            self.cur.append(node)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.errors.append(f'line {self.getpos()[0]}: </{tag}> does not close <{self.stack[-1][0] if self.stack else None}>')
            return
        self.stack.pop()
        self.cur.pop()

    def handle_data(self, data):
        for n in self.cur:
            n['text'] += data


def find(node, tag=None, cls=None):
    out = []
    for k in node['kids']:
        if (tag is None or k['tag'] == tag) and (cls is None or cls in k['attrs'].get('class', '').split()):
            out.append(k)
        out += find(k, tag, cls)
    return out


t = Tree()
t.feed(raw)
t.close()
print(f'  tag errors: {t.errors or "none"}; unclosed at end: {t.stack or "none"}')
print(f'  <style>/<script>/<html>/<head>/<body> present: {bool(re.search(r"<(style|script|html|head|body)\b", raw))}')
bad_tex = [seg for a, b in tex for seg in (a + b,) if '<' in seg or '>' in seg or '&lt;' in seg or '&gt;' in seg]
print(f'  raw < or > (or &lt;/&gt;) inside TeX: {bad_tex or "none"}')
txt_only = re.sub(r'\\\(.*?\\\)|\\\[.*?\\\]', ' ', raw, flags=re.S)
stray = [m.start() for m in re.finditer(r'<(?![a-zA-Z/!])', txt_only)]
print(f'  stray "<" in text (not a tag): {stray or "none"}')
STATUS = {'must': '背', 'try': '尽量记', 'give': '考试给', 'def': '定义·必会'}
for sec in find(t.root, 'section', 'topic'):
    sid = sec['attrs'].get('id')
    h2 = find(sec, 'h2')
    h3 = [re.sub(r'\s+', ' ', x['text']).strip() for x in find(sec, 'h3')]
    meta = find(sec, 'div', 'meta')
    sts = find(meta[0], 'span', 'st') if meta else []
    st_ok = all(STATUS.get(next((c for c in s['attrs']['class'].split() if c != 'st'), ''), None) == s['text'].strip()
                for s in find(sec, 'span', 'st'))
    sym = find(sec, 'table', 'sym')
    symhead = [x['text'].strip() for x in find(sym[0], 'th')] if sym else []
    steps = find(sec, 'table', 'steps')
    stepcols = [len(find(s, 'th')) for s in steps]
    rows_ok = all(len(find(r, 'td')) == 4 for s in steps for r in find(s, 'tr') if find(r, 'td'))
    srcs = find(sec, 'p', 'src')
    egs = find(sec, 'div', 'eg')
    eg_ok = all(find(e, 'div', 'egh') and find(e, 'p', 'q') and find(e, 'ol', 'work') and find(e, 'p', 'ans') for e in egs)
    traps = find(sec, 'ul', 'trap')
    ntrap = len(find(traps[0], 'li')) if traps else 0
    en = find(sec, 'div', 'en')
    en_ok = bool(en) and bool(find(en[0], 'div', 'enl')) and bool(find(en[0], 'p'))
    fms = find(sec, 'div', 'fm')
    fm_ok = all(find(f, 'div', 'fl') and find(f, 'div', 'fx') and find(f, 'div', 'fn') for f in fms)
    print(f'  [{sid}] h2+tn: {bool(h2 and find(h2[0], "span", "tn"))}; meta badges {[s["text"] for s in sts]} freq: {bool(meta and find(meta[0], "span", "freq"))};'
          f' why: {bool(find(sec, "p", "why"))}; status text matches class: {st_ok}')
    print(f'         h3: {h3}')
    print(f'         sym header: {symhead}; sym rows: {len(find(sym[0], "tr")) - 1 if sym else 0}; formulas: {len(fms)} complete={fm_ok}')
    print(f'         steps tables: {len(steps)} cols={stepcols} all rows 4 cells={rows_ok}; p.src: {len(srcs)}; examples: {len(egs)} complete={eg_ok};'
          f' traps: {ntrap}; english: {en_ok}')
