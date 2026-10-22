#!/usr/bin/python3
"""Independent re-check of quizsum/frag_prob_db.html (t1 probability basics, t2 dB conversion and SNR).

Written by the adversarial checker, separately from the writer's check_prob_db.py. Stdlib only.
Run:  /usr/bin/python3 _verify_prob_db.py        (exit code 1 if any check fails)

  A  recompute every number in the fragment from the question data (labelled lines)
  B  the question data and quoted answers exist in the source files (finals, Practice 1-2, mock, learn pages)
  C  every lecturer claim ("老师…") is backed by src/teacher/notes.py; formula badges follow quiz_marks.py
  D  format: tag balance (html.parser), no raw < > inside TeX, no style/script, section skeleton, badges
  E  key result strings built from part A appear verbatim in the fragment, and every multi-digit,
     decimal or scientific number in the fragment appears in the part A output
"""
import html
import math
import pathlib
import re
import sys
from fractions import Fraction
from html.parser import HTMLParser
from statistics import NormalDist

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent
FRAG = HERE / 'frag_prob_db.html'
RAW = FRAG.read_text(encoding='utf-8')

OUT, FAIL = [], []


def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    OUT.append(s)


def bad(msg):
    FAIL.append(msg)
    print('  !! FAIL:', msg)


def head(t):
    say('\n## ' + t)


N01 = NormalDist()


def Q(x):                       # Gaussian right tail P(Z > x)
    return 1 - N01.cdf(x)


def to_db(x):                   # power ratio -> dB
    return 10 * math.log10(x)


def from_db(d):                 # dB -> power ratio
    return 10 ** (d / 10)


def amp_db(a):                  # amplitude ratio -> dB
    return 20 * math.log10(a)


def dbm(p_mw):                  # power in mW -> dBm
    return 10 * math.log10(p_mw / 1.0)


SUPD = str.maketrans('0123456789-+', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺')


def usci(x, d):                 # 2.08e-03 -> '2.08×10⁻³' (fragment style)
    m, e = f'{x:.{d}e}'.split('e')
    return f'{m}×10{str(int(e)).translate(SUPD)}'


def mn(x, fmt):                 # number with a typographic minus, as the fragment writes it
    return format(x, fmt).replace('-', '−')


V = {}                          # values used by the claim checks in part E

# =====================================================================================  A  numbers
head('A1  t1 formula notes')
p_br = Fraction(4, 7) * Fraction(3, 6)
say(f'marbles (Ch1b p.3-4), bag of 3 red + 4 blue: P(blue first) = 4/7, P(red | blue first) = 3/6, '
    f'P(blue then red) = 4/7 x 3/6 = {p_br} (equals 2/7: {p_br == Fraction(2, 7)})')
say(f'two independent links, each in outage 10% of the time: both at once = 0.1 x 0.1 = {0.1 * 0.1:.2f}')
say('Practice 2 Q2(b): independent shadowing -> P_out = Q(Delta/sigma) * Q(Delta/sigma) = [Q(Delta/sigma)]^2')
say('2025-26 S1 Q1(a)(ii): y = s + w, s = +1 fixed, E[w] = 0, Var(w) = 0.25 -> E[y] = 1 + 0 = 1, '
    'Var[y] = 0.25 (adding a constant does not change the variance)')
say('mock A.Q1(b): prior of the bad state 0.3 -> posterior 0.977 (below)')

head('A2  t1 steps table 1: state table -> total probability -> Bayes')


def two_state(pg, eg, pb, eb):
    rg, rb = pg * eg, pb * eb
    pe = rg + rb
    return rg, rb, pe, rb / pe, rg / pe


for key, lab, (pg, eg, pb, eb) in [
        ('L', 'learn_01 section 1.2 worked example (self-written): good 80% / 1e-04, deep fade 20% / 1e-02',
         (0.8, 1e-4, 0.2, 1e-2)),
        ('M', 'mock A.Q1 (a)(b): good 0.7 / 1e-04, bad 0.3 / 1e-02', (0.7, 1e-4, 0.3, 1e-2))]:
    rg, rb, pe, pb_post, pg_post = two_state(pg, eg, pb, eb)
    V[key] = dict(rg=rg, rb=rb, pe=pe, post=pb_post, postg=pg_post)
    say(lab)
    say(f'   priors {pg} + {pb} = {pg + pb:.1f}')
    say(f'   rows: {pg} x 1e-04 = {rg:.0e} ; {pb} x 1e-02 = {rb:.0e} ; total P_e = {pe:.2e}')
    say(f'   Bayes: {rb:.0e} / {pe:.2e} = {pb_post:.4f} (3 s.f. {pb_post:.3f}) ; other state {pg_post:.4f} ; '
        f'sum {pb_post + pg_post:.1f}')

head('A3  t1 table 1 source line: 2023-24 Q1(b)(i) second half (Ch4 selection diversity), probability part')
g10, g12 = from_db(10), from_db(12)
p10 = 0.2 * 0.2
p12 = 1 - p10
t10 = p10 * 0.5 * math.exp(-g10)
t12 = p12 * 0.5 * math.exp(-g12)
V['sd'] = dict(p10=p10, p12=p12, tot=t10 + t12)
say(f'P(SD output = 10 dB) = 0.2 x 0.2 = {p10:.2f} (independent branches) ; P(12 dB) = 1 - 0.04 = {p12:.2f}')
say(f'DPSK 1/2 e^-gamma: 1/2 e^-10 = {0.5 * math.exp(-10):.3e} ; 1/2 e^-15.85 = {0.5 * math.exp(-15.85):.3e} '
    f'(10^1.2 = {g12:.4f})')
say(f'average SEP = {t10:.3e} + {t12:.3e} = {t10 + t12:.3e} -> {t10 + t12:.1e} '
    f'(data_2324.py shows the second term as 6.2e-08; exact {t12:.2e})')

head('A4  t1 steps table 2: discrete SNR in dB -> mean, variance')


def moments(dbs, ps):
    g = [from_db(d) for d in dbs]
    m1 = sum(p * x for p, x in zip(ps, g))
    m2 = sum(p * x * x for p, x in zip(ps, g))
    return g, m1, m2, m2 - m1 * m1


g, m1, m2, var = moments([10, 12], [0.2, 0.8])
V['y2324'] = dict(g12=g[1], m1=m1, m2=m2, var=var)
say(f'2023-24 Q1(b)(i): 10 dB -> {g[0]:.0f} ; 12 dB -> {g[1]:.2f} (10^1.2 = {g[1]:.4f})')
say(f'   E = 0.2 x 10 + 0.8 x 15.85 = {m1:.2f} (more digits {m1:.3f}) -> {to_db(m1):.2f} dB')
say(f'   wrong: 0.2 x 10 + 0.8 x 12 = {0.2 * 10 + 0.8 * 12:.1f} dB ; gap {to_db(m1) - 11.6:.2f} dB')
say(f'   practice (not asked): 15.85^2 = {g[1] ** 2:.2f} ; E[g^2] = 0.2 x 100 + 0.8 x {g[1] ** 2:.2f} = {m2:.2f}')
say(f'   (E)^2 = {m1:.3f}^2 = {m1 * m1:.2f} ; Var = {m2:.2f} - {m1 * m1:.2f} = {var:.2f}')
say(f'   rounding trap: 14.68^2 = {14.68 ** 2:.2f} -> {m2:.2f} - {14.68 ** 2:.2f} = {m2 - 14.68 ** 2:.2f} '
    f'instead of {var:.2f}')
g, m1, m2, var = moments([11, 12, 13], [0.2, 0.5, 0.3])
V['s1'] = dict(g=g, m1=m1)
say(f'2025-26 S1 Q1(b)(i): 11/12/13 dB (p 0.2/0.5/0.3) -> {g[0]:.2f} / {g[1]:.2f} / {g[2]:.2f} ; mean {m1:.2f} '
    f'-> {to_db(m1):.2f} dB ; wrong dB average {0.2 * 11 + 0.5 * 12 + 0.3 * 13:.1f} dB')
say(f'   MRC, 2 branches: E[X+Y] = 2 x {m1:.2f} = {2 * m1:.2f} -> {to_db(2 * m1):.2f} dB')
g, m1, m2, var = moments([10, 0], [0.7, 0.3])
V['mockc'] = dict(m1=m1, m2=m2, var=var)
say(f'mock A.Q1(c): 10 dB -> {g[0]:.0f}, 0 dB -> {g[1]:.0f} ; E = 0.7 x 10 + 0.3 x 1 = {m1:.1f} -> {to_db(m1):.2f} dB ; '
    f'E[g^2] = 0.7 x 100 + 0.3 x 1 = {m2:.1f} ; 7.3^2 = {m1 * m1:.2f} ; Var = {var:.2f} ; sigma = {math.sqrt(var):.2f}')
say(f'   wrong: 0.7 x 10 + 0.3 x 0 = {0.7 * 10:.0f} dB ; gap {to_db(m1) - 7:.2f} dB')

head('A5  t1 example 1: three states')
ps, es = [0.6, 0.3, 0.1], [1e-4, 1e-3, 1e-2]
rows = [p * e for p, e in zip(ps, es)]
pe = sum(rows)
post = [r / pe for r in rows]
V['ex1'] = dict(rows=rows, pe=pe, post=post)
say(f'priors 0.6 + 0.3 + 0.1 = {sum(ps):.1f} ; rows {rows[0]:.0e}, {rows[1]:.0e}, {rows[2]:.0e} ; P_e = {pe:.2e}')
say(f'P(good|e) = {post[0]:.4f} ({post[0]:.3f}) ; P(medium|e) = {post[1]:.4f} ; P(deep|e) = {post[2]:.4f} '
    f'({post[2]:.3f}) ; sum = {sum(post):.4f}')
say(f'deep fade: {ps[2] * 100:.0f}% of the time, {post[2] * 100:.1f}% of the errors')

head('A6  t1 example 2: backwards, the share of the bad state from the average error rate')
eg, eb, pe = 1e-4, 1e-2, 2e-3
num, den = pe - eg, eb - eg
p = num / den
V['ex2'] = dict(num=num, den=den, p=p, bayes=p * eb / pe)
say(f'2e-03 = (1 - p) x 1e-04 + p x 1e-02 -> p = {num:.1e} / {den:.1e} = {p:.4f} ({p:.3f}, about {round(p * 100)}%)')
say(f'check: (1 - 0.1919) x 1e-04 + 0.1919 x 1e-02 = {(1 - 0.1919) * eg + 0.1919 * eb:.1e}')
say(f'Bayes: P(bad | e) = {p:.4f} x 1e-02 / 2e-03 = {p * eb / pe:.4f} ({p * eb / pe:.3f})')

head('A7  t1 example 3: SNR 3 / 10 / 15 dB with probability 0.25 / 0.5 / 0.25')
dbs, ps = [3, 10, 15], [0.25, 0.5, 0.25]
g, m1, m2, var = moments(dbs, ps)
V['ex3'] = dict(g=g, m1=m1, m2=m2, var=var)
say(f'linear: 10^0.3 = {g[0]:.3f} ; 10 ; 10^1.5 = {g[2]:.3f}')
say(f'(a) 0.25 x 1.995 = {0.25 * 1.995:.3f} ; 0.5 x 10 = 5 ; 0.25 x 31.623 = {0.25 * 31.623:.3f} ; '
    f'shown sum 0.499 + 5 + 7.906 = {0.499 + 5 + 7.906:.3f} ; exact E = {m1:.4f} ({m1:.3f}, 3 s.f. {m1:.1f})')
say(f'    10log10(13.405) = {to_db(13.405):.2f} dB (exact {to_db(m1):.2f})')
wrong = sum(p * d for p, d in zip(ps, dbs))
say(f'    wrong dB average 0.25 x 3 + 0.5 x 10 + 0.25 x 15 = {wrong:.1f} dB ; gap {to_db(m1) - wrong:.2f} dB')
say(f'(b) squares: 10^0.6 = {g[0] ** 2:.3f} ; 10^2 = 1e+02 = 100 ; (10^1.5)^2 = 10^3 = {g[2] ** 2:.0f}')
say(f'    0.25 x 3.981 = {0.25 * 3.981:.3f} ; 0.5 x 100 = 50 ; 0.25 x 1000 = 250 ; E[g^2] = {m2:.3f} -> {m2:.1f}')
say(f'    13.405^2 = {13.405 ** 2:.2f} -> {13.405 ** 2:.1f} ; Var = 301.0 - 179.7 = {301.0 - 179.7:.1f} '
    f'(exact {var:.3f}) ; sigma = sqrt(121.3) = {math.sqrt(121.3):.2f} (exact {math.sqrt(var):.2f})')
say(f'    rounding check: 13.40^2 = {13.40 ** 2:.2f} would give Var {m2 - 13.40 ** 2:.1f}')
say(f'(c) threshold 6 dB: only the 3 dB value lies below -> P_out = {ps[0]:.2f}')
say(f'(d) Y = 2 gamma: each dB value +{to_db(2):.2f} dB ; E[Y] = 2 x 13.405 = {2 * 13.405:.2f} -> {to_db(2 * m1):.2f} dB '
    f'(= 11.27 + 3.01 = {11.27 + 3.01:.2f})')
say(f'    Var(Y) = 2^2 x 121.3 = {4 * 121.3:.1f} ~ {4 * var:.0f} (exact {4 * var:.2f}) ; '
    f'std = 2 x 11.01 = {2 * 11.01:.2f} ~ {2 * math.sqrt(var):.1f} (exact {2 * math.sqrt(var):.3f})')

head('A8  t2 formula notes, quick table, finals list')
say(f'1 W = 1000 mW -> {dbm(1000):.0f} dBm = {dbm(1000) - 30:.0f} dBW ; 1 mW -> {dbm(1):.0f} dBm (slides Ch2 p.10, first step)')
for r in (2, 4, 10, 100, 1000, 0.5, 0.1, 0.01):
    say(f'power x{r}: {to_db(r):+.2f} dB')
for name, mw in (('1 mW', 1), ('100 mW', 100), ('0.5 W', 500), ('1 W', 1000), ('10 W', 1e4),
                 ('1 uW', 1e-3), ('1 pW', 1e-9)):
    say(f'{name} = {dbm(mw):.2f} dBm')
for a in (2, 10, 0.5, math.sqrt(0.1), 0.1):
    say(f'amplitude x{a:.3f}: {amp_db(a):+.2f} dB')
say('finals, dB -> linear: ' + ' ; '.join(f'{d} dB -> {from_db(d):.2f} ({from_db(d):.1f})' for d in (3, 10, 11, 12, 13, 18, 25)))
say(f'2025-26 S2 Q1(b)(i): 15 - 12 = 3 dB -> 10^0.3 = {from_db(3):.3f} (about 2)')
say(f'Practice 1 Q2(a): margin 15 - 10 = 5 dB = x10^0.5 = {from_db(5):.2f} ; 5/8 = {5 / 8:.3f} ; '
    f'Q(0.625) = {Q(0.625):.3f} (right tail ; Q(0) = {Q(0):.1f})')
kT = 1.380649e-23 * 290
say(f'thermal noise kT at 290 K = {10 * math.log10(kT / 1e-3):.2f} dBm/Hz (the usual -174 dBm/Hz)')
say(f'5 MHz: 10log10(5e+06) = {to_db(5e6):.2f} ; bandwidth x2 -> noise +{to_db(2):.2f} dB, SNR -{to_db(2):.2f} dB')
say(f'rho: "0.1 of the rms" (amplitude) -> rho = 0.1, rho^2 = {0.1 ** 2:.2f}, {amp_db(0.1):.0f} dB ; '
    f'"power 10 dB below rms" -> rho^2 = {from_db(-10):.1f}, rho = {math.sqrt(from_db(-10)):.3f} '
    f'({amp_db(math.sqrt(from_db(-10))):.2f} dB)')
say(f'lecturer example: 8.5 dB -> 10^0.85 = {from_db(8.5):.2f}')

head('A9  t2 steps table 1: SNR from powers, then Shannon')
S, I, N, B = 10, 10, 0.1, 20e6
snr, sinr = S / N, S / (I + N)
V['p2q3'] = dict(snr=snr, sinr=sinr, c2=B * math.log2(1 + snr), c1=B * math.log2(1 + sinr))
say(f'Practice 2 Q3: S = 10 mW, I = 10 mW, N = 0.1 mW, B = 20 MHz')
say(f'   (b) SNR = 10 / 0.1 = {snr:.0f} -> {to_db(snr):.0f} dB ; log2(101) = {math.log2(101):.4f} ; '
    f'C2 = {B * math.log2(1 + snr) / 1e6:.2f} Mbps')
say(f'   (a) SINR = 10 / (10 + 0.1) = {sinr:.3f} -> {to_db(sinr):.2f} dB ; log2(1.990) = {math.log2(1 + sinr):.4f} ; '
    f'C1 = {B * math.log2(1 + sinr) / 1e6:.2f} Mbps')
Sm, N0, Bm = -90, -174, 5e6
Nn = N0 + to_db(Bm)
sdb = Sm - Nn
sl = from_db(sdb)
c_a = Bm * math.log2(1 + sl)
V['b3'] = dict(N=Nn, sdb=sdb, sl=sl, c=c_a)
say(f'mock B.Q3(a): N = -174 + {to_db(Bm):.2f} = {Nn:.2f} dBm ; SNR = -90 - ({Nn:.2f}) = {sdb:.2f} dB '
    f'-> 10^{sdb / 10:.3f} = {sl:.1f} ; log2({1 + sl:.1f}) = {math.log2(1 + sl):.3f} ; C = {c_a / 1e6:.1f} Mbps')
Nn2 = N0 + to_db(2 * Bm)
s2 = from_db(Sm - Nn2)
c_b = 2 * Bm * math.log2(1 + s2)
say(f'mock B.Q3(b): 10 MHz: N = {Nn2:.2f} dBm ; SNR = {Sm - Nn2:.2f} dB = {s2:.1f} ; C = {c_b / 1e6:.1f} Mbps ; '
    f'ratio {c_b / c_a:.2f}')

head('A10  t2 steps table 2: power chain W -> dBm -> dB sums -> SNR')
dist = 10 * 3.97 * math.log10(150)
say(f'slides Ch2 p.10: P_t = 1 mW -> {dbm(1):.0f} dBm ; K_dB = -26.67 ; log10(150) = {math.log10(150):.3f} ; '
    f'10 x 3.97 x log10 150 = {dist:.2f} dB ; P_r = 0 - 26.67 - 86.39 = {0 - 26.67 - dist:.2f} dBm (150 m)')
say(f'focused Q3(a): P_t = 1 W = 1000 mW -> {dbm(1000):.0f} dBm ; d = 1 km = 1000 m ; '
    f'10 x 3 x log10 1000 = {30 * math.log10(1000):.0f} dB ; P_r = 30 - 40 - 90 = {30 - 40 - 90} dBm ; '
    f'SNR = -100 - (-120) = {-100 + 120} dB -> 10^(20/10) = {from_db(20):.0f} ; (c) 10/100 = {from_db(10) / from_db(20):.1f}')

head('A11  t2 steps table 3: amplitude ratio or power ratio (10 log / 20 log)')
rho, fD = 0.1, 50
afd1 = (math.exp(rho ** 2) - 1) / (math.sqrt(2 * math.pi) * fD * rho)
say(f'Practice 2 Q1: rho = 0.1 (signal strength = amplitude) ; rho^2 = {rho ** 2:.2f} ; 20log10(0.1) = {amp_db(0.1):.0f} dB ; '
    f'f_D = 50 Hz ; AFD = {afd1 * 1e3:.2f} ms (official 0.8 ms)')
v, fc = 72 / 3.6, 1.8e9
fm = v * fc / 3e8
rho2 = from_db(-10)
rho = math.sqrt(rho2)
afd2 = (math.exp(rho2) - 1) / (math.sqrt(2 * math.pi) * fm * rho)
afdw = (math.exp(0.01) - 1) / (math.sqrt(2 * math.pi) * fm * 0.1)
V['afd'] = dict(a1=afd1, a2=afd2, aw=afdw, fm=fm, rho=rho)
say(f'mock A.Q3(c): 72 km/h / 3.6 = {v:.0f} m/s ; 1.8 GHz ; f_m = v f_c / c = {fm:.0f} Hz ; '
    f'10^(-10/10) = {rho2:.1f} = rho^2 -> rho = sqrt(0.1) = {rho:.3f} ; 10log10(0.1) = {to_db(rho2):.0f} dB = '
    f'20log10({rho:.3f}) = {amp_db(rho):.0f} dB')
say(f'   AFD = {afd2 * 1e3:.3f} ms ; wrong rho = 0.1 -> {afdw * 1e3:.3f} ms')

head('A12  t2 example 1: 0.5 W, 110 dB, 200 kHz, -174 dBm/Hz')
Pt = dbm(500)
Pr = Pt - 110
Bw = 200e3
Nn = -174 + to_db(Bw)
sdb = Pr - Nn
sl = from_db(sdb)
C = Bw * math.log2(1 + sl)
V['e1'] = dict(Pt=Pt, Pr=Pr, N=Nn, sdb=sdb, sl=sl, C=C)
say(f'0.5 W = 500 mW -> {Pt:.2f} dBm (= 30 - {to_db(2):.2f}) ; P_r = {Pt:.2f} - 110 = {Pr:.2f} dBm')
say(f'10log10(2e+05) = {to_db(Bw):.2f} ; N = {Nn:.2f} dBm ; SNR = {sdb:.2f} dB -> 10^{sdb / 10:.3f} = {sl:.0f} = {sl:.2e}')
say(f'C = 2e+05 x log2(1 + {sl:.0f}) = 2e+05 x {math.log2(1 + sl):.2f} = {C / 1e6:.2f} Mbps')

head('A13  t2 example 2: backwards, minimum transmit power')
Nn = -174 + to_db(1e6)
Prm = Nn + 15
Ptm = Prm + 125
say(f'10log10(1e+06) = {to_db(1e6):.0f} ; N = {Nn:.0f} dBm ; P_r,min = {Nn:.0f} + 15 = {Prm:.0f} dBm ; '
    f'P_t,min = {Prm:.0f} + 125 = {Ptm:.0f} dBm = 10^(26/10) mW = {from_db(Ptm):.0f} mW = {from_db(Ptm) / 1000:.2f} W')

head('A14  t2 example 3: S -80 dBm, I -85 dBm, N -90 dBm')
S, I, N = -80, -85, -90
Imw, Nmw = from_db(I), from_db(N)
IN = Imw + Nmw
sinr_db = S - to_db(IN)
V['e3'] = dict(Imw=Imw, IN=IN, INdb=to_db(IN), sinr_db=sinr_db)
say(f'SNR = {S - N} dB ; SIR = {S - I} dB')
say(f'I = 10^-8.5 = {Imw:.3e} mW ; N = 10^-9 = {Nmw:.0e} mW ; I + N = {IN:.3e} mW -> {to_db(IN):.2f} dBm')
say(f'SINR = -80 - ({to_db(IN):.2f}) = {sinr_db:.2f} dB -> 10^{sinr_db / 10:.3f} = {from_db(sinr_db):.2f} ; '
    f'check 1/(1/{from_db(5):.3f} + 1/10) = 1/({1 / from_db(5):.4f} + 0.1) = {1 / (1 / from_db(5) + 0.1):.2f}')
say(f'wrong: -85 + (-90) = {I + N} "dBm" ; 5e+06 Hz used in the traps')

# =====================================================================================  B  sources
head('B  question data and quoted answers in the source files')
_cache = {}


def text(rel):
    if rel not in _cache:
        _cache[rel] = (SRC / rel).read_text(encoding='utf-8')
    return _cache[rel]


def need(rel, sub, why, src=None):
    s = text(rel) if src is None else src
    if sub in s:
        say(f'   ok  {rel}: {why}')
    else:
        bad(f'{rel}: not found [{sub}] ({why})')


def article(rel, aid):
    m = re.search(rf'<article class="ex" id="{aid}">(.*?)</article>', text(rel), re.S)
    return m.group(1) if m else ''


D24, D25, D26a, D26b = 'exams/data_2324.py', 'exams/data_2425.py', 'exams/data_2526s1.py', 'exams/data_2526s2.py'
need(D24, "id='y2324s2-q1b1', paper=P, q='Q1(b)(i)'", '2023-24 Q1(b)(i) exists')
need(D24, "page='p2', ch='ch4'", 'it is a Ch4 question')
need(D24, '10 dB with a probability of 0.2', '10 dB w.p. 0.2')
need(D24, '12 dB with a probability of 0.8', '12 dB w.p. 0.8')
need(D24, 'Determine the average SNR in dB of the received signals', 'asks the average SNR in dB')
need(D24, '0.2 × 10 + 0.8 × 15.85 = 14.68 → 11.67 dB', 'answer 14.68 = 11.67 dB')
need(D24, '0.2×10 + 0.8×12 = 11.6 dB', 'wrong dB average 11.6 dB')
need(D24, '0.04 × ½e<sup>−10</sup> + 0.96 × ½e<sup>−15.85</sup>', 'SD average SEP = total probability')
need(D24, '≈ 9.7×10⁻⁷', 'SD average SEP 9.7e-07')
need(D25, '18dB, 10dB, and 3dB', '2024-25 Q1(a)(iii) sub-band SNRs')
need(D25, 'γ = 63.1、10、2.0', '18/10/3 dB -> 63.1/10/2.0')
need(D26a, "id='y2526s1-q1a', paper=P, q='Q1(a)', marks=12, page='p2', ch='ch3'", '2025-26 S1 Q1(a) is a Ch3 question')
need(D26a, 'zero mean and a variance of 0.25', 'noise variance 0.25')
need(D26a, 'y = s + w', 'y = s + w')
need(D26a, 'Determine the expected values and variances of y when s = 1', 'Q1(a)(ii) asks E and Var of y')
need(D26a, '11 dB with a probability of 0.2', '11 dB w.p. 0.2')
need(D26a, '12 dB with a probability of 0.5', '12 dB w.p. 0.5')
need(D26a, '13 dB with a probability of 0.3', '13 dB w.p. 0.3')
need(D26a, '= 16.43 → 12.16 dB', 'mean 16.43 = 12.16 dB')
need(D26a, '2 × 16.43 = 32.86 → 15.17 dB', 'MRC 32.86 = 15.17 dB')
need(D26b, 'γ̄<sub>R</sub> = 25dB', '2025-26 S2 Q1(a)(iii) 25 dB')
need(D26b, '316.2', '25 dB -> 316.2')
need(D26b, 'average input Signal-to-Noise Ratio (SNR) is 12dB, the average combiner output SNR is 15dB', 'Q1(b)(i) 12/15 dB')
need(D26b, '15 − 12 = 3 dB → 10<sup>0.3</sup> ≈ 2', 'array gain 3 dB -> about 2')
P1, P2, P8 = 'p2build/prac_1.html', 'p2build/prac_2.html', 'p2build/prac_8.html'
q = article(P1, 'p1q2')
need(P1, 'mean \\(\\mu_\\psi\\) dBm and standard deviation \\(\\sigma_\\psi\\) dBm', 'P1 Q2 writes sigma in dBm', q)
need(P1, 'required to be above 10 dBm', 'threshold 10 dBm', q)
need(P1, '\\(\\mu_\\psi\\) = 15 dBm and \\(\\sigma_\\psi\\) = 8 dBm', 'mean 15 dBm, sigma 8', q)
need(P1, 'Q(0.625)=0.266', 'Q(0.625) = 0.266', q)
q = article(P2, 'p2q1')
need(P2, 'The maximum Doppler shift is 50 Hz', 'P2 Q1 f_D = 50 Hz', q)
need(P2, '0.1 of the rms value of the signal strength', 'P2 Q1 amplitude 0.1', q)
need(P2, '官方答案：</b>0.8 ms', 'P2 Q1 official 0.8 ms', q)
q = article(P2, 'p2q2')
need(P2, 'P_{out}=[Q(\\Delta/\\sigma)]^2', 'P2 Q2(b) independent -> square', q)
need(P2, '\\int_{-\\infty}^{\\infty}', 'P2 Q2(c) is an integral', q)
q = article(P2, 'p2q3')
need(P2, 'The power received from each transmitter is 10mW. The total received noise power is 0.1mW. '
         'The channel bandwidth for each user is 20MHz.', 'P2 Q3 data', q)
need(P2, '官方答案：</b>19.86 Mbps；133.16 Mbps', 'P2 Q3 official answers', q)
for aid, label, subs in [
        ('p8q1', '模拟 A · Q1', ['which occurs with probability 0.7, the bit error probability is \\(10^{-4}\\)',
                                'which occurs with probability 0.3, the bit error probability is \\(10^{-2}\\)',
                                'The received SNR is 10 dB in the good state and 0 dB in the bad state']),
        ('p8q3', '模拟 A · Q3', ['transmits 50 k symbols/s on a 1.8 GHz carrier, and the mobile moves at 72 km/h',
                                'the received power must not fall more than 10 dB below its rms value']),
        ('p8q6', '模拟 B · Q3', ['A receiver gets a signal power of −90 dBm over a bandwidth of 5 MHz. '
                                'The noise power spectral density is −174 dBm/Hz.', 'The bandwidth is doubled to 10 MHz']),
        ('p8q12', '专项 · Q3', ['A mobile station is 1 km from a base station that transmits 1 W', 'K_{dB}=-40',
                               'γ = 3', 'The noise power at the receiver is −120 dBm',
                               'instantaneous SNR of at least 10 dB'])]:
    q = article(P8, aid)
    need(P8, f'<span class="pg">{label}</span>', f'{aid} is labelled {label}', q)
    for sub in subs:
        need(P8, sub, f'{aid} data', q)
L1, L2 = 'p2build/learn_01.html', 'p2build/learn_02.html'
s12 = text(L1).split('<span class="zh-num">1.2</span>')[1].split('<span class="zh-num">1.3</span>')[0]
need(L1, '全概率与贝叶斯：信道好坏与误码（自编）', 'learn_01 section 1.2 example is self-written', s12)
need(L1, '信道有 80% 的时间是"好"状态，误码率 10⁻⁴；20% 的时间是"深衰落"状态，误码率 10⁻²', '80% / 20% data', s12)
need(L1, '掷骰子与摸弹珠（第 1b 章 p.3–4）', 'marbles on Ch1b p.3-4')
need(L1, '袋里 3 红 4 蓝', '3 red 4 blue')
need(L1, 'P(先蓝后红) = 4/7 × 3/6 = 2/7', '4/7 x 3/6 = 2/7')
need(L1, '四条规则（第 1b 章 p.5–9）', 'rules on p.5-9')
need(L1, '定义（第 1b 章 p.10–11）', 'E and Var on p.10-11')
need(L1, '必须记住的五条性质（p.10–11、p.14）', 'aX+b properties on p.10-11, p.14')
need(L2, '简化路径损耗模型（p.8）', 'path loss model on Ch2 p.8')
need(L2, '150 m 处收到多少功率（第 2 章 p.10）', 'Ch2 p.10 example')
need(L2, '\\(K_{\\mathrm{dB}}=-26.67\\) dB，γ = 3.97，发射功率 1 mW，求 150 m 处的接收功率', 'p.10 data')
need(L2, '1 mW = 10 log₁₀(1 mW / 1 mW) = 0 dBm', 'p.10 first step 1 mW -> 0 dBm')
need(L2, 'P_r = 0 − 26.67 − 86.39 = −113.06 dBm', 'p.10 answer')
need(L2, '瑞利衰落的 LCR 与 AFD（p.41–43）', 'LCR/AFD on p.41-43')
need(L2, 'AWGN 信道的香农容量（p.48）', 'Shannon on p.48')
need(L2, '\\gamma=\\dfrac{P}{N_0B}', 'gamma = P/(N0 B) on p.48')
need(L2, 'Practice 1 第 2 题原文把 σ 写成 "dBm"，严格说应该是 dB', 'P1 Q2 sigma unit remark')
NOISE174 = re.compile(r'(?:−|-)\s?174(?![\d.])|174\s?dBm')     # not SVG path coordinates such as L174.7
for rel in (L1, L2):
    if NOISE174.search(text(rel)):
        bad(f'{rel} mentions −174 dBm/Hz, so the fragment\'s "outside knowledge" remark needs rewording')
    else:
        say(f'   ok  {rel}: no −174 dBm/Hz (the fragment calls it outside knowledge)')

# =====================================================================================  C  lecturer claims, badges
head('C  lecturer claims (src/teacher/notes.py) and formula status (quiz_marks.py)')
NOTES, MARKS = 'teacher/notes.py', 'p2build/quiz_marks.py'
CLAIMS = [  # (phrase in the fragment, phrase in notes.py)
    ('老师说不考积分，但离散分布的求和会考', '<b>不会考积分</b>，但离散分布的求和会考'),
    ('老师强调的记号', '<b>大写字母（X、Y、Z）是随机变量，小写字母是它的取值</b>'),
    ('老师点名的往年错误：只写一项 P(A₁)P(B | A₁)', '把 P(B) 写成 P(A₁)P(B | A₁)'),
    ('<b>必须对所有 A<sub>i</sub> 求和</b>（第 8 周录音）', "n('p2', ('h3', '1.2'), W8, [\n  '往年学生常犯的错"),
    ('这是老师点名的往年错误', '全概率必须对所有 A<sub>i</sub> 求和</mark>，老师说考试遇到类似题别再犯'),
    ('蓝框，要背（讲义第 1b 章 p.5–9）', '贝叶斯公式是<b>蓝框，要背</b>'),
    ('E[X] = Σx·P(x) 是老师点名要背的', '<b>要背（录音里明确说过）</b>：贝叶斯公式；期望 E[X] = Σx·p(x)'),
    ('E[g(X)] 的一般式考试会给', '<b>考试会给，只要懂含义</b>：高斯 PDF；E[g(X)] 的一般式'),
    ('老师说这是往年常见错误', 'E[g(X)] ≠ g(E[X])。这两点都是往年常见错误'),
    ('老师课上的说法：方差 = 平方的均值 − 均值的平方', '方差 = 平方的均值 − 均值的平方'),
    ('老师说没写 dB ↔ 线性换算会扣分', '没做 dB ↔ 线性换算会扣分'),
    ('老师说漏写 dB ↔ 线性换算会扣分，mW 没换成 dBm 也会扣分', 'mW 没换成 dBm 会扣分'),
    ('老师说 mW 没换成 dBm 会扣分', 'mW 没换成 dBm 会扣分'),
    ('老师讲例题时说 8.5 dB 要先换成 10<sup>0.85</sup>，每年都强调还是有人不换',
     '例题里的 8.5 dB 要先换成 10<sup>0.85</sup>，老师每年都强调还是有人不换'),
    ('老师讲 Practice 1 Q1 时特别提醒："10 dB above"的 10 是 dB，不要换成线性',
     '他特别提醒："10 dB above"里的 10 是 dB，这个公式是 dB 形式推出来的，不要换成线性'),
    ('老师点名要背的公式里没有它', '香农容量 C = B log₂(1 + SNR)'),
]
frag_plain = html.unescape(RAW)
for fphrase, nphrase in CLAIMS:
    if fphrase not in RAW and fphrase not in frag_plain:
        bad(f'claim phrase not in fragment: {fphrase}')
    elif nphrase not in text(NOTES):
        bad(f'notes.py does not back: {fphrase}')
    else:
        say(f'   ok  {fphrase}')
if NOISE174.search(text(NOTES)):
    bad('notes.py mentions −174 dBm/Hz')
# every sentence of the fragment that mentions the lecturer must contain a checked phrase
sentences = re.split(r'[。；\n]', re.sub(r'<[^>]+>', '', RAW))
keys = [re.sub(r'<[^>]+>', '', f) for f, _ in CLAIMS]
for snt in sentences:
    if '老师' in snt and not any(k in snt or snt.strip() in k for k in keys):
        bad(f'unchecked lecturer sentence: {snt.strip()[:90]}')
need(MARKS, "'贝叶斯公式是蓝框，要背。加法、乘法、全概率要会用", 'Bayes = must, total probability = 要会用')
need(MARKS, "'期望 E[X] = Σx·P(x) 要背，离散分布的求和会考。方差公式要会用。'", 'E[X] = must, variance = 要会用')
need(MARKS, "('learn_02.html', '瑞利衰落的 LCR 与 AFD', 'give'", 'LCR/AFD = given')
need(MARKS, "('learn_02.html', 'AWGN 信道的香农容量', 'must'", 'Shannon = must')
need(MARKS, "('learn_02.html', '简化路径损耗模型（p.8）', 'must'", 'path loss model = must')

# =====================================================================================  D  format
head('D  format checks')
VOID = {'br', 'img', 'hr', 'input', 'meta', 'link', 'wbr', 'col', 'area', 'base', 'embed', 'source', 'track', 'param'}


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.kids = tag, dict(attrs), parent, []

    def cls(self):
        return (self.attrs.get('class') or '').split()

    def walk(self):
        yield self
        for k in self.kids:
            if isinstance(k, Node):
                yield from k.walk()

    def text(self):
        return ''.join(k.text() if isinstance(k, Node) else k for k in self.kids)

    def elems(self):
        return [k for k in self.kids if isinstance(k, Node)]


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

    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.cur.tag == tag:
            self.cur = self.cur.parent
            return
        self.errors.append(f'</{tag}> closes while <{self.cur.tag}> is open (line {self.getpos()[0]})')
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.kids.append(data)


t = Tree()
t.feed(RAW)
t.close()
for e in t.errors:
    bad('tag nesting: ' + e)
if t.cur is not t.root:
    chain = []
    n = t.cur
    while n is not t.root:
        chain.append(n.tag)
        n = n.parent
    bad('unclosed tags at end: ' + ' > '.join(reversed(chain)))
if not t.errors and t.cur is t.root:
    say('   ok  html.parser: every tag closed and properly nested')
for tag in ('style', 'script', 'html', 'head', 'body'):
    if re.search(rf'<{tag}\b', RAW, re.I):
        bad(f'<{tag}> present')
say('   ok  no <style>/<script>/<html>/<head>/<body>' if not any(
    re.search(rf'<{x}\b', RAW, re.I) for x in ('style', 'script', 'html', 'head', 'body')) else '')
tex = re.findall(r'\\\((.*?)\\\)', RAW, re.S) + re.findall(r'\\\[(.*?)\\\]', RAW, re.S)
nonascii = set()
for seg in tex:
    if '<' in seg or '>' in seg:
        bad(f'raw < or > inside TeX: {seg[:70]}')
    if '&lt;' in seg or '&gt;' in seg:
        bad(f'&lt;/&gt; inside TeX (use \\lt / \\gt): {seg[:70]}')
    if seg.count('{') != seg.count('}'):
        bad(f'unbalanced braces in TeX: {seg[:70]}')
    nonascii |= {ch for ch in seg if ord(ch) > 127}
if RAW.count('\\(') != RAW.count('\\)') or RAW.count('\\[') != RAW.count('\\]'):
    bad('unbalanced \\( \\) or \\[ \\] delimiters')
say(f'   ok  {len(tex)} TeX segments: no raw < >, braces balanced' + (
    f' ; non-ASCII inside TeX: {sorted(nonascii)}' if nonascii else ' ; all ASCII'))
if nonascii:
    bad(f'non-ASCII characters inside TeX: {sorted(nonascii)}')
BADGE = {'must': '背', 'try': '尽量记', 'give': '考试给', 'def': '定义·必会'}
H3 = ['符号与含义 · Symbols', '公式 · Formulas', '解题步骤 · Steps', '中文例子 · 怎么用', '易错 · Traps']
SYM_HEAD = ['符号', '中文', 'English', '含义（大白话）', '单位']
EXPECT_FM = {  # formula-card label prefix -> expected status (quiz_marks.py / notes.py / task rules)
    '加法与乘法规则': ['def'], '全概率公式': ['def'], '贝叶斯公式': ['must'], '期望': ['must'],
    '方差': ['def'], '线性变换与求和': ['def'], 'dB 值求平均': ['def'],
    '功率 ↔ dBm': ['def'], '比值 ↔ dB': ['def'], 'dB 加减的含义': ['def'], '信噪比': ['def'],
    '噪声功率': ['def'], '10 log 还是 20 log': ['def']}
sections = [n for n in t.root.walk() if n.tag == 'section']
if [s.attrs.get('id') for s in sections] != ['t1', 't2']:
    bad(f'section ids {[s.attrs.get("id") for s in sections]} != [t1, t2]')
for sec in sections:
    sid = sec.attrs.get('id')
    if 'topic' not in sec.cls():
        bad(f'{sid}: section lacks class topic')
    h2 = [n for n in sec.walk() if n.tag == 'h2']
    tn = [n for n in h2[0].walk() if 'tn' in n.cls()] if h2 else []
    if not tn or tn[0].text() != sid[1:] or ' · ' not in h2[0].text():
        bad(f'{sid}: h2 / span.tn / "中文 · English" title')
    meta = [n for n in sec.walk() if 'meta' in n.cls()]
    if not meta or not [n for n in meta[0].walk() if 'st' in n.cls()] or \
            not [n for n in meta[0].walk() if 'freq' in n.cls() and n.text().startswith('出现：')]:
        bad(f'{sid}: div.meta needs badges and span.freq starting with 出现：')
    if not [n for n in sec.walk() if n.tag == 'p' and 'why' in n.cls()]:
        bad(f'{sid}: p.why missing')
    h3s = [n.text() for n in sec.walk() if n.tag == 'h3']
    if h3s != H3:
        bad(f'{sid}: h3 order {h3s}')
    syms = [n for n in sec.walk() if n.tag == 'table' and 'sym' in n.cls()]
    if not any([th.text() for th in tb.walk() if th.tag == 'th'] == SYM_HEAD for tb in syms):
        bad(f'{sid}: no symbols table with header {SYM_HEAD}')
    for tb in syms:
        if tb.parent.tag != 'div' or 'tw' not in tb.parent.cls():
            bad(f'{sid}: a table.sym is not wrapped in div.tw')
    fms = [n for n in sec.walk() if 'fm' in n.cls()]
    for fm in fms:
        kinds = [k.cls()[0] for k in fm.elems()]
        if kinds != ['fl', 'fx', 'fn']:
            bad(f'{sid}: .fm children {kinds}')
            continue
        fl = fm.elems()[0]
        st = [n for n in fl.walk() if 'st' in n.cls()]
        status = [c for n in st for c in n.cls() if c in BADGE]
        label = fl.text()
        exp = next((v for k, v in EXPECT_FM.items() if label.startswith(k)), None)
        if exp is None:
            bad(f'{sid}: unexpected formula card {label[:30]}')
        elif status != exp:
            bad(f'{sid}: card "{label[:20]}" status {status} expected {exp}')
        else:
            say(f'   ok  {sid} card "{label.split(" ")[0]}" status {status[0]} ({BADGE[status[0]]})')
        if '\\[' not in ''.join(k if isinstance(k, str) else k.text() for k in fm.elems()[1].kids):
            bad(f'{sid}: .fx of "{label[:20]}" has no display math')
    steps = [n for n in sec.walk() if n.tag == 'table' and 'steps' in n.cls()]
    if not steps:
        bad(f'{sid}: no steps table')
    for tb in steps:
        ths = [th.text() for th in tb.walk() if th.tag == 'th']
        if len(ths) != 4 or ths[:2] != ['步骤', '做法']:
            bad(f'{sid}: steps header {ths}')
        wrap = tb.parent
        sib = wrap.parent.elems()
        i = sib.index(wrap)
        if i + 1 >= len(sib) or sib[i + 1].tag != 'p' or 'src' not in sib[i + 1].cls() \
                or not sib[i + 1].text().startswith('来源：'):
            bad(f'{sid}: steps table "{ths[2]}" not followed by p.src 来源：')
        if i == 0 or sib[i - 1].tag != 'h4':
            bad(f'{sid}: steps table "{ths[2]}" has no h4 before it')
        rows = [r for r in tb.walk() if r.tag == 'tr'][1:]
        for r in rows:
            if len([c for c in r.elems() if c.tag == 'td']) != 4:
                bad(f'{sid}: a steps row does not have 4 cells')
        say(f'   ok  {sid} steps table [{ths[2]} | {ths[3]}] {len(rows)} rows + p.src')
    egs = [n for n in sec.walk() if 'eg' in n.cls()]
    if not 2 <= len(egs) <= 3:
        bad(f'{sid}: {len(egs)} examples')
    for eg in egs:
        kinds = [(k.tag, (k.cls() or [''])[0]) for k in eg.elems()]
        if kinds != [('div', 'egh'), ('p', 'q'), ('ol', 'work'), ('p', 'ans')]:
            bad(f'{sid}: example structure {kinds}')
    traps = [n for n in sec.walk() if n.tag == 'ul' and 'trap' in n.cls()]
    nli = len([n for n in traps[0].elems() if n.tag == 'li']) if traps else 0
    if not 3 <= nli <= 6:
        bad(f'{sid}: {nli} traps')
    en = [n for n in sec.walk() if 'en' in n.cls()]
    if not en or [k.tag for k in en[0].elems()][:2] != ['div', 'p'] or 'enl' not in en[0].elems()[0].cls():
        bad(f'{sid}: div.en > div.enl + p')
    say(f'   ok  {sid}: {len(fms)} formula cards, {len(steps)} steps tables, {len(egs)} examples, {nli} traps, '
        f'English template present')
for n in t.root.walk():
    if 'st' in n.cls():
        kind = [c for c in n.cls() if c in BADGE]
        if len(kind) != 1 or n.text() != BADGE[kind[0]]:
            bad(f'badge {n.cls()} text {n.text()}')

# =====================================================================================  E  claims + coverage
head('E1  key results (built from part A) appear verbatim in the fragment')
L, M, y24, ex1, ex2, ex3 = V['L'], V['M'], V['y2324'], V['ex1'], V['ex2'], V['ex3']
b3, e1, e3, af, p3 = V['b3'], V['e1'], V['e3'], V['afd'], V['p2q3']
must_have = [
    f'0.8 × 10⁻⁴ = {usci(L["rg"], 0)}；0.2 × 10⁻² = {usci(L["rb"], 0)}',
    f'0.7 × 10⁻⁴ = {usci(M["rg"], 0)}；0.3 × 10⁻² = {usci(M["rb"], 0)}',
    f'8×10⁻⁵ + 2×10⁻³ = {usci(L["pe"], 2)}', f'7×10⁻⁵ + 3×10⁻³ = {usci(M["pe"], 2)}',
    f'2×10⁻³ / 2.08×10⁻³ = {L["post"]:.4f}', f'3×10⁻³ / 3.07×10⁻³ = {M["post"]:.3f}',
    f'{L["postg"]:.4f} + {L["post"]:.4f} = 1', f'{M["postg"]:.4f} + {M["post"]:.4f} = 1',
    f'0.2 × 0.2 = {V["sd"]["p10"]:.2f}', f'1 − 0.04 = {V["sd"]["p12"]:.2f}', f'≈ {usci(V["sd"]["tot"], 1)}（全概率）',
    f'12 dB → {y24["g12"]:.2f}', f'0.8 × 15.85 = {y24["m1"]:.2f}', f'10 log₁₀ 14.68 = {to_db(y24["m1"]):.2f} dB',
    f'0.2 × 100 + 0.8 × {y24["g12"] ** 2:.2f} = {y24["m2"]:.2f}',
    f'220.95 − 14.679² = 220.95 − {y24["m1"] ** 2:.2f} = {y24["var"]:.2f}',
    f'14.679² = {y24["m1"] ** 2:.2f}，方差 {y24["var"]:.2f}；若用 14.68² = {14.68 ** 2:.2f}，会得 {y24["m2"] - 14.68 ** 2:.2f}',
    f'0.7 × 10 + 0.3 × 1 = {V["mockc"]["m1"]:.1f}', f'10 log₁₀ 7.3 = {to_db(7.3):.2f} dB',
    f'0.7 × 100 + 0.3 × 1 = {V["mockc"]["m2"]:.1f}',
    f'70.3 − 7.3² = 70.3 − {7.3 ** 2:.2f} = {V["mockc"]["var"]:.2f}，σ = {math.sqrt(V["mockc"]["var"]):.2f}',
    f'0.2 × 10 + 0.8 × 12 = {11.6:.1f} dB ✗', '0.7 × 10 + 0.3 × 0 = 7 dB ✗',
    f'错算 11.6 dB、正确 {to_db(y24["m1"]):.2f} dB（差 {to_db(y24["m1"]) - 11.6:.2f} dB）',
    f'错算 7 dB、正确 {to_db(7.3):.2f} dB（差 {to_db(7.3) - 7:.2f} dB）',
    ' / '.join(f'{x:.2f}' for x in V['s1']['g']) + f' → 均值 {V["s1"]["m1"]:.2f} → {to_db(V["s1"]["m1"]):.2f} dB'
    f'（直接平均 dB 得 {0.2 * 11 + 0.5 * 12 + 0.3 * 13:.1f} dB）',
    f'2 × 16.43 = {2 * V["s1"]["m1"]:.2f}（{to_db(2 * V["s1"]["m1"]):.2f} dB）',
    '4/7 × 3/6 = 2/7', '0.1 × 0.1 = 0.01', '先验 0.3，知道出错后变成 0.977',
    f'E[γ²] = {V["mockc"]["m2"]:.1f}，而 7.3² = {7.3 ** 2:.2f}，两者之差 {V["mockc"]["var"]:.2f}',
    f'=1.36\\times10^{{-3}}', f'1×10⁻³ / 1.36×10⁻³ = {ex1["post"][2]:.4f}', f'6×10⁻⁵ / 1.36×10⁻³ = {ex1["post"][0]:.4f}',
    f'3×10⁻⁴ / 1.36×10⁻³ = {ex1["post"][1]:.4f}',
    f'P(深衰落 | 错) ≈ {ex1["post"][2]:.3f}，P(好 | 错) ≈ {ex1["post"][0]:.3f}', f'{ex1["post"][2] * 100:.1f}% 的错误',
    f'p=\\dfrac{{1.9\\times10^{{-3}}}}{{9.9\\times10^{{-3}}}}={ex2["p"]:.4f}',
    f'(1 − 0.1919) × 10⁻⁴ + 0.1919 × 10⁻² = {usci((1 - 0.1919) * 1e-4 + 0.1919 * 1e-2, 1)}',
    f'0.1919 × 10⁻² / (2×10⁻³) = {ex2["bayes"]:.4f}', f'p ≈ {ex2["p"]:.3f}', f'P(坏 | 错) ≈ {ex2["bayes"]:.3f}',
    f'10<sup>0.3</sup> = {ex3["g"][0]:.3f}', f'10<sup>1.5</sup> = {ex3["g"][2]:.3f}',
    f'=0.499+5+7.906={ex3["m1"]:.3f}', f'10 log₁₀13.405 = {to_db(ex3["m1"]):.2f} dB',
    f'= {sum(p * d for p, d in zip([0.25, 0.5, 0.25], [3, 10, 15])):.1f} dB，低了 {to_db(ex3["m1"]) - 9.5:.2f} dB',
    f'10<sup>0.6</sup> = {ex3["g"][0] ** 2:.3f}', f'=0.995+50+250={ex3["m2"]:.1f}',
    f'301.0-13.405^2=301.0-{13.405 ** 2:.1f}={ex3["var"]:.1f}', f'σ = √121.3 = {math.sqrt(ex3["var"]):.2f}',
    f'P<sub>out</sub> = 0.25', f'2 × 13.405 = {2 * 13.405:.2f}', f'11.27 + 3.01 = {to_db(2 * ex3["m1"]):.2f} dB',
    f'2² × 121.3 ≈ {4 * ex3["var"]:.0f}', f'2 × 11.01 ≈ {2 * math.sqrt(ex3["var"]):.1f}',
    f'=0.7\\times10^{{-4}}+0.3\\times10^{{-2}}={M["pe"] * 1e3:.2f}\\times10^{{-3}}',
    f'=(3\\times10^{{-3}})/(3.07\\times10^{{-3}})={M["post"]:.3f}', f'10\\log_{{10}}7.3={to_db(7.3):.2f}',
    f'70.3-7.3^2={V["mockc"]["var"]:.2f}',
    # t2
    f'平均功率是门限的 {from_db(5):.2f} 倍', f'5/8 = {5 / 8:.3f} → Q(0.625) = {Q(0.625):.3f}',
    f'18 / 10 / 3 dB → {from_db(18):.1f} / 10 / {from_db(3):.1f}', f'25 dB → {from_db(25):.1f}',
    '15 dB − 12 dB = 3 dB → 10<sup>0.3</sup> ≈ 2', f'10 log₁₀(5×10⁶) = {to_db(5e6):.2f} dB',
    f'噪声 +{to_db(2):.2f} dB → SNR −{to_db(2):.2f} dB', f'ρ² = 0.1，ρ = {math.sqrt(0.1):.3f}',
    f'<td>×2</td><td>+{to_db(2):.2f}（≈ +3）</td><td>1 mW</td><td>{dbm(1):.0f}</td><td>×2</td><td>+{amp_db(2):.2f}</td>',
    f'<td>×4</td><td>+{to_db(4):.2f}</td><td>100 mW</td><td>{dbm(100):.0f}</td><td>×10</td><td>+{amp_db(10):.0f}</td>',
    f'<td>×10</td><td>+{to_db(10):.0f}</td><td>0.5 W</td><td>{dbm(500):.2f}</td><td>×0.5</td><td>{mn(amp_db(0.5), ".2f")}</td>',
    f'<td>×100</td><td>+{to_db(100):.0f}</td><td>1 W</td><td>{dbm(1000):.0f}</td><td>×{math.sqrt(0.1):.3f}（√0.1）</td>'
    f'<td>{mn(amp_db(math.sqrt(0.1)), ".0f")}</td>',
    f'<td>×1000</td><td>+{to_db(1000):.0f}</td><td>10 W</td><td>{dbm(1e4):.0f}</td><td>×0.1</td><td>{mn(amp_db(0.1), ".0f")}</td>',
    f'<td>×0.5</td><td>{mn(to_db(0.5), ".2f")}（≈ −3）</td><td>1 µW</td><td>{mn(dbm(1e-3), ".0f")}</td>',
    f'<td>×0.1</td><td>{mn(to_db(0.1), ".0f")}</td><td>1 pW</td><td>{mn(dbm(1e-9), ".0f")}</td>',
    f'<td>×0.01</td><td>{mn(to_db(0.01), ".0f")}</td>',
    f'3 dB → {from_db(3):.1f}，10 dB → 10，18 dB → {from_db(18):.1f}', f'12 dB → {from_db(12):.2f}',
    f'11 dB → {from_db(11):.2f}，13 dB → {from_db(13):.2f}', f'25 dB → {from_db(25):.1f}（2025-26 S2 Q1(a)(iii)）',
    f'−174 + 10 log₁₀(5×10⁶) = −174 + {to_db(5e6):.2f} = {mn(b3["N"], ".2f")} dBm',
    f'−90 − ({mn(b3["N"], ".2f")}) = {b3["sdb"]:.2f} dB', f'10<sup>{b3["sdb"] / 10:.3f}</sup> = {b3["sl"]:.1f}',
    f'(b) SNR = 10 / 0.1 = {p3["snr"]:.0f}', f'SINR = 10 / (10 + 0.1) = {p3["sinr"]:.3f}',
    f'100 → {to_db(100):.0f} dB；0.990 → {mn(to_db(p3["sinr"]), ".2f")} dB',
    f'20 MHz × log₂101 = {p3["c2"] / 1e6:.2f} Mbps', f'20 MHz × log₂1.990 = {p3["c1"] / 1e6:.2f} Mbps',
    f'5 MHz × log₂{1 + b3["sl"]:.1f} = {b3["c"] / 1e6:.1f} Mbps',
    f'10 × 3.97 × log₁₀150 = {10 * 3.97 * math.log10(150):.2f} dB',
    f'0 − 26.67 − 86.39 = {mn(-26.67 - 10 * 3.97 * math.log10(150), ".2f")} dBm',
    f'10 × 3 × log₁₀1000 = {30 * math.log10(1000):.0f} dB', '30 − 40 − 90 = −100 dBm', '−100 − (−120) = 20 dB',
    f'10<sup>20/10</sup> = {from_db(20):.0f}', 'γ₀/γ̄ = 10/100 = 0.1',
    f'功率比 10<sup>−10/10</sup> = {from_db(-10):.1f} = ρ² → ρ = √0.1 = {af["rho"]:.3f}',
    f'20 log₁₀0.1 = {mn(amp_db(0.1), ".0f")} dB（功率比 ρ² = {0.1 ** 2:.2f}）',
    f'10 log₁₀0.1 = −10 dB = 20 log₁₀{af["rho"]:.3f}', f'f<sub>D</sub> = 50 Hz：AFD = {af["a1"] * 1e3:.2f} ms',
    f'f<sub>m</sub> = {af["fm"]:.0f} Hz：AFD = {af["a2"] * 1e3:.3f} ms（误用 ρ = 0.1 得 {af["aw"] * 1e3:.3f} ms ✗）',
    f'10 log₁₀500 = {e1["Pt"]:.2f} dBm', f'P<sub>r</sub> = 26.99 − 110 = {mn(e1["Pr"], ".2f")} dBm',
    f'−174 + 10 log₁₀(2×10⁵) = −174 + {to_db(2e5):.2f} = {mn(e1["N"], ".2f")} dBm',
    f'SNR = −83.01 − (−120.99) = {e1["sdb"]:.2f} dB → 10<sup>{e1["sdb"] / 10:.3f}</sup> ≈ {usci(e1["sl"], 2)}',
    f'log₂(1 + {e1["sl"]:.0f}) = 2×10⁵ × {math.log2(1 + e1["sl"]):.2f} = {e1["C"] / 1e6:.2f} Mbps',
    f'−174 + 10 log₁₀10⁶ = −174 + {to_db(1e6):.0f} = −114 dBm', '−114 + 15 = −99 dBm', '−99 + 125 = 26 dBm',
    f'10<sup>26/10</sup> mW = {from_db(26):.0f} mW ≈ {from_db(26) / 1000:.2f} W',
    'SNR = −80 − (−90) = 10 dB；SIR = −80 − (−85) = 5 dB',
    f'I = 10<sup>−8.5</sup> = {usci(e3["Imw"], 3)} mW，N = 10<sup>−9</sup> = 1×10⁻⁹ mW，I + N = {usci(e3["IN"], 3)} mW → '
    f'10 log₁₀({usci(e3["IN"], 3)}) = {mn(e3["INdb"], ".2f")} dBm',
    f'SINR = −80 − (−83.81) = {e3["sinr_db"]:.2f} dB → 10<sup>{e3["sinr_db"] / 10:.3f}</sup> = {from_db(e3["sinr_db"]):.2f}',
    f'1/(0.3162 + 0.1) = {1 / (1 / from_db(5) + 0.1):.2f}', '−85 + (−90) = −175',
    f'10 log₁₀(5×10⁶) = {to_db(5e6):.2f}，不是 10 log₁₀5', f'28.4 涨到 47.1 Mbps（1.66 倍）',
    f'10\\log_{{10}}(1000\\ \\text{{mW}}/1\\ \\text{{mW}})={dbm(1000):.0f}', '=30-40-30\\log_{10}1000=-100',
    f'N=-174+10\\log_{{10}}(5\\times10^6)={b3["N"]:.2f}', '20\\log_{10}0.1=-20', '\\rho^2=0.01',
]
for s in must_have:
    if s in RAW:
        say(f'   ok  {s[:110]}')
    else:
        bad(f'not in fragment: {s}')

head('E2  number coverage: every multi-digit / decimal / scientific number in the fragment is printed above')
SUPMAP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺', '0123456789-+')
SUBS = {c: f'_{i} ' for i, c in enumerate('₀₁₂₃₄₅₆₇₈₉')}           # x₁₀ -> x_1 _0 (never glued to a number)
SUBS.update({c: f'^{i} ' for i, c in enumerate('⁰¹²³⁴⁵⁶⁷⁸⁹')})     # 7.3² -> 7.3^2, not 7.32
SUBS.update({'⁻': '^-', '⁺': '^+'})


def sci_or_not(a, e, raw):
    x = float(a)
    if 1 <= x < 10:
        return f' {a}e{int(e):+03d} '
    return raw


def numbers(src):
    s = re.sub(r'<sup>(.*?)</sup>', lambda m: '^(' + m.group(1) + ')', src, flags=re.S)
    s = re.sub(r'<sub>(.*?)</sub>', lambda m: '_(' + m.group(1) + ')', s, flags=re.S)
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    s = re.sub(r'20\d\d-\d\d', ' ', s)                                  # paper years
    s = re.sub(r'p\.\s?\d+(?:\s?[–-]\s?\d+)?', ' ', s)                   # slide pages
    s = re.sub(r'(\d+(?:\.\d+)?)\\times\s*10\^\{?(-?\d+)\}?',
               lambda m: sci_or_not(m.group(1), m.group(2), m.group(0).replace('\\times', ' × ')), s)
    s = re.sub(r'(?<![\d.])10\^\{(-?\d+)\}', lambda m: f' 1e{int(m.group(1)):+03d} ', s)
    s = re.sub(r'(\d+(?:\.\d+)?)\s*×\s*10([⁻⁺]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)',
               lambda m: sci_or_not(m.group(1), m.group(2).translate(SUPMAP), m.group(1) + ' × 10' + m.group(2)), s)
    s = re.sub(r'(?<![\d.])10([⁻⁺]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)', lambda m: f' 1e{int(m.group(1).translate(SUPMAP)):+03d} ', s)
    s = ''.join(SUBS.get(c, c) for c in s)
    return re.findall(r'(?<![\w.])(\d+(?:\.\d+)?(?:e[-+]\d+)?)(?![\d])', s)


ALLOWED = {'1.2': 'learn page section number (讲解页 1.2 节)'}


def coverage(out_text, who):
    checked, missing = set(), []
    for tok in numbers(RAW):
        if tok in checked:
            continue
        checked.add(tok)
        if len(tok) < 2 and '.' not in tok and 'e' not in tok:
            continue                                                  # single digits
        pat = r'(?<![\d.])' + re.escape(tok) + r'(?![\d]|\.\d)'
        if not re.search(pat, out_text):
            missing.append(tok)
    for tok in missing:
        if tok in ALLOWED:
            say(f'   skip {tok}: {ALLOWED[tok]}')
        else:
            bad(f'number {tok} in the fragment is not printed by {who}')
    say(f'   {who}: {len(checked)} distinct number tokens in the fragment, '
        f'{len([x for x in missing if x not in ALLOWED])} not covered')


coverage('\n'.join(OUT), 'this script')

head('F  the writer\'s check_prob_db.py runs and its output also covers every number')
import subprocess
run = subprocess.run([sys.executable, str(HERE / 'check_prob_db.py')], capture_output=True, text=True)
if run.returncode != 0:
    bad('check_prob_db.py exited with ' + str(run.returncode) + ': ' + run.stderr[-300:])
else:
    coverage(run.stdout, 'check_prob_db.py')

print('\n' + ('ALL CHECKS PASSED' if not FAIL else f'{len(FAIL)} FAILED CHECK(S):\n  - ' + '\n  - '.join(FAIL)))
sys.exit(1 if FAIL else 0)
