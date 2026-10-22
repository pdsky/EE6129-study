#!/usr/bin/python3
"""Check script for quizsum/frag_prob_db.html (t1 probability basics, t2 dB conversion and SNR).

Every number printed in the fragment (steps tables, formula notes, examples, traps, English
templates, quick-conversion table) is printed here with a label. Stdlib only.
Run:  /usr/bin/python3 check_prob_db.py
Sources of the question data: src/p2build/learn_01.html, learn_02.html, prac_1.html, prac_2.html,
prac_8.html (verify_mock.py), src/exams/data_2324.py, data_2425.py, data_2526s1.py, data_2526s2.py.
"""
from math import log10, log2, sqrt, exp, pi
from statistics import NormalDist

lin = lambda db: 10 ** (db / 10)          # dB -> linear power ratio
dB = lambda x: 10 * log10(x)              # linear power ratio -> dB
Q = lambda x: NormalDist().cdf(-x)        # Gaussian tail


def h(t):
    print('\n=== ' + t)


def mean(vals, probs):
    return sum(v * p for v, p in zip(vals, probs))


# ============================================================ t1 probability
h('t1 table A, left: learn_01 section 1.2 worked example (self-written): good 0.8 / 1e-4, fade 0.2 / 1e-2')
pG, eG, pB, eB = 0.8, 1e-4, 0.2, 1e-2
rG, rB = pG * eG, pB * eB
Pe = rG + rB
print(f'sum of priors = {pG + pB:.1f}')
print(f'inputs: P(err | good) = {eG:.0e}, P(err | fade) = {eB:.0e}')
print(f'row good = {rG:.0e} ; row fade = {rB:.0e} ; total Pe = {Pe:.3e} = {Pe:.2e}')
print(f'P(fade | err) = {rB / Pe:.4f} ; P(good | err) = {rG / Pe:.4f} ; sum = {(rB + rG) / Pe:.1f}')

h('t1 table A, right: mock A.Q1 (a)(b): good 0.7 / 1e-4, bad 0.3 / 1e-2')
pG, eG, pB, eB = 0.7, 1e-4, 0.3, 1e-2
rG, rB = pG * eG, pB * eB
Pe = rG + rB
print(f'sum of priors = {pG + pB:.1f}')
print(f'row good = {rG:.0e} ; row bad = {rB:.0e} ; total Pe = {Pe:.3e} = {Pe:.2e}')
print(f'P(bad | err) = {rB / Pe:.4f} (3 s.f. {rB / Pe:.3f}) ; P(good | err) = {rG / Pe:.4f} ; sum = {(rB + rG) / Pe:.1f}')

h('t1 table A source line: final 2023-24 Q1(b)(i) second half (Ch4 selection diversity), probability part')
p10 = 0.2 * 0.2
sep = p10 * 0.5 * exp(-10) + (1 - p10) * 0.5 * exp(-lin(12))
print(f'P(SD output = 10 dB) = 0.2*0.2 = {p10:.2f} ; P(12 dB) = 1 - 0.04 = {1 - p10:.2f} ; '
      f'average SEP = 0.04*0.5e^-10 + 0.96*0.5e^-{lin(12):.2f} = {sep:.1e}')

h('t1 table B, left: final 2023-24 Q1(b)(i) first step: 10 dB p0.2, 12 dB p0.8')
v = [lin(10), lin(12)]; p = [0.2, 0.8]
m = mean(v, p); m2 = mean([x * x for x in v], p)
print(f'linear = {v[0]:.0f}, {v[1]:.2f}')
print(f'E[g] = 0.2*10 + 0.8*{v[1]:.2f} = {m:.2f} -> {dB(m):.2f} dB')
print(f'wrong: average of dB values = 0.2*10 + 0.8*12 = {0.2 * 10 + 0.8 * 12:.1f} dB ; gap = {dB(m) - 11.6:.2f} dB')
print(f'(not asked, practice) E[g^2] = 0.2*100 + 0.8*{v[1] ** 2:.2f} = {m2:.2f} ; (E[g])^2 = {m:.3f}^2 = {m * m:.2f} ; '
      f'Var = {m2:.2f} - {m * m:.2f} = {m2 - m * m:.2f}')
print(f'rounding trap: 14.68^2 = {14.68 ** 2:.2f} -> {m2:.2f} - {14.68 ** 2:.2f} = {m2 - 14.68 ** 2:.2f} (keep the extra digit)')

h('t1 source line: final 2025-26 S1 Q1(b)(i) first step: 11/12/13 dB with 0.2/0.5/0.3')
v = [lin(11), lin(12), lin(13)]; p = [0.2, 0.5, 0.3]
m = mean(v, p)
print(f'linear = {v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f} ; E[g] = {m:.2f} -> {dB(m):.2f} dB ; wrong dB average = {mean([11, 12, 13], p):.1f} dB')
print(f'MRC (E[X+Y] = E[X]+E[Y]): 2*{m:.2f} = {2 * m:.2f} -> {dB(2 * m):.2f} dB')

h('t1 table B, right: mock A.Q1 (c): 10 dB p0.7, 0 dB p0.3')
v = [lin(10), lin(0)]; p = [0.7, 0.3]
m = mean(v, p); m2 = mean([x * x for x in v], p)
print(f'linear = {v[0]:.0f}, {v[1]:.0f} ; E[g] = {m:.1f} -> {dB(m):.2f} dB')
print(f'E[g^2] = {m2:.1f} ; (E[g])^2 = {m * m:.2f} ; Var = {m2 - m * m:.2f} ; std = {sqrt(m2 - m * m):.2f}')
print(f'wrong dB average = 0.7*10 + 0.3*0 = {0.7 * 10 + 0.3 * 0:.0f} dB ; gap = {dB(m) - 7:.2f} dB')

h('t1 formula notes')
print(f'marbles (Ch1b p.3-4): 3 red 4 blue: P(first blue) = 4/7 = {4 / 7:.4f} ; P(red | blue first) = 3/6 = {3 / 6:.1f} ; P(blue then red) = 4/7*3/6 = 2/7 = {4 / 7 * 3 / 6:.4f}')
print(f'two independent links, 10% each: both = {0.1 * 0.1:.2f}')
print('final 2025-26 S1 Q1(a)(ii): y = s + w, s = +1 fixed, Var(w) = 0.25 -> E[y] = 1, Var[y] = 0.25 (inputs, no computation)')

h('t1 example 1: three states good 0.6/1e-4, medium 0.3/1e-3, deep fade 0.1/1e-2')
ps = [0.6, 0.3, 0.1]; es = [1e-4, 1e-3, 1e-2]
rows = [a * b for a, b in zip(ps, es)]; Pe = sum(rows)
print(f'sum priors = {sum(ps):.1f} ; rows = {rows[0]:.0e}, {rows[1]:.0e}, {rows[2]:.0e} ; Pe = {Pe:.3e} = {Pe:.2e}')
post = [r / Pe for r in rows]
print(f'P(good|err) = {post[0]:.4f} ; P(medium|err) = {post[1]:.4f} ; P(deep|err) = {post[2]:.4f} ; sum = {sum(post):.4f}')
print(f'deep fade share of errors = {100 * post[2]:.1f}% ; answer line (3 s.f.): P(deep|err) = {post[2]:.3f}, P(good|err) = {post[0]:.3f}')

h('t1 example 2: backwards, eG 1e-4, eB 1e-2, measured Pe 2e-3, find p = P(bad)')
eG, eB, Pe = 1e-4, 1e-2, 2e-3
pbad = (Pe - eG) / (eB - eG)
print(f'numerator Pe - eG = {Pe - eG:.1e} ; denominator eB - eG = {eB - eG:.1e} ; p = {pbad:.4f}')
print(f'check: (1-p)*1e-4 + p*1e-2 = {(1 - pbad) * eG + pbad * eB:.1e}')
print(f'P(bad | err) = p*eB/Pe = {pbad * eB / Pe:.4f}')
print(f'answer line (3 s.f.): p = {pbad:.3f} (about {100 * pbad:.0f}% of the time) ; P(bad | err) = {pbad * eB / Pe:.3f}')

h('t1 example 3: SNR 3 dB p0.25, 10 dB p0.5, 15 dB p0.25 ; threshold 6 dB ; power doubled')
dbs = [3, 10, 15]; p = [0.25, 0.5, 0.25]
v = [lin(x) for x in dbs]
m = mean(v, p); m2 = mean([x * x for x in v], p); var = m2 - m * m
print(f'linear = 10^{3 / 10:.1f} = {v[0]:.3f}, {v[1]:.0f}, 10^{15 / 10:.1f} = {v[2]:.3f}')
print(f'terms = {0.25 * v[0]:.3f} + {0.5 * v[1]:.0f} + {0.25 * v[2]:.3f} ; E[g] = {m:.3f} (3 s.f. {m:.1f}) -> {dB(m):.2f} dB')
print(f'wrong dB average = {mean(dbs, p):.1f} dB ; gap = {dB(m) - mean(dbs, p):.2f} dB')
print(f'squares (double the exponent): 10^0.6 = {v[0] ** 2:.3f}, 10^2 = {1e2:.0e} = {v[1] ** 2:.0f}, 10^3 = {v[2] ** 2:.0f} ; '
      f'terms = {0.25 * v[0] ** 2:.3f} + {0.5 * v[1] ** 2:.0f} + {0.25 * v[2] ** 2:.0f}')
print(f'E[g^2] = {m2:.1f} ; (E[g])^2 = {m:.3f}^2 = {m * m:.1f} ; Var = {var:.1f} ; std = {sqrt(var):.2f}')
print(f'outage P(g < 6 dB): only 3 dB value -> {p[0]:.2f}')
print(f'doubled: each +{dB(2):.2f} dB ; E[2g] = 2*{m:.3f} = {2 * m:.2f} -> {dB(2 * m):.2f} dB (= {dB(m):.2f} + {dB(2):.2f}) ; '
      f'Var(2g) = 4*{var:.1f} = {4 * round(var, 1):.1f} ~ {4 * var:.0f} ; std = 2*{sqrt(var):.2f} ~ {2 * sqrt(var):.1f}')

# ============================================================ t2 dB and SNR
h('t2 table A, left: Practice 2 Q3: S = 10 mW each user, noise 0.1 mW, B = 20 MHz')
S, I, N, B = 10, 10, 0.1, 20e6
snr = S / N; sinr = S / (I + N)
print(f'(b) SNR = 10/0.1 = {snr:.0f} -> {dB(snr):.0f} dB ; C2 = 20 MHz * log2({1 + snr:.0f}) = {B * log2(1 + snr) / 1e6:.2f} Mbps')
print(f'(a) SINR = 10/10.1 = {sinr:.3f} -> {dB(sinr):.2f} dB ; C1 = 20 MHz * log2({1 + sinr:.3f}) = {B * log2(1 + sinr) / 1e6:.2f} Mbps')

h('t2 table A, right: mock B.Q3 (a)(b): S = -90 dBm, N0 = -174 dBm/Hz, B = 5 MHz')
S, N0, B = -90, -174, 5e6
Nn = N0 + dB(B); s_db = S - Nn
print(f'10log10({B:.0e}) = {dB(B):.2f} ; N = {Nn:.2f} dBm ; SNR = {s_db:.2f} dB -> 10^{s_db / 10:.3f} = {lin(s_db):.1f} ; C = 5 MHz * log2({1 + lin(s_db):.1f}) = {B * log2(1 + lin(s_db)) / 1e6:.1f} Mbps')
Nn2 = N0 + dB(2 * B); s2 = S - Nn2
print(f'(b) 2B: 10log10(1e7) = {dB(2 * B):.2f} ; N = {Nn2:.2f} dBm (+{dB(2):.2f} dB) ; SNR = {s2:.2f} dB -> {lin(s2):.1f} ; C = {2 * B * log2(1 + lin(s2)) / 1e6:.1f} Mbps ; ratio = {2 * B * log2(1 + lin(s2)) / (B * log2(1 + lin(s_db))):.2f}')

h('t2 table B, left: slides Ch2 p.10 example: Pt 1 mW, K -26.67 dB, gamma 3.97, d 150 m')
Pt = dB(1 / 1)       # 1 mW / 1 mW
dist = 10 * 3.97 * log10(150)
print(f'Pt = {Pt:.0f} dBm ; log10(150) = {log10(150):.3f} ; 10*3.97*log10(150) = {dist:.2f} dB ; Pr = {Pt - 26.67 - dist:.2f} dBm')

h('t2 table B, right: focused Q3 (a): Pt 1 W, K -40 dB, gamma 3, d 1000 m, N -120 dBm')
Pt = dB(1000 / 1)    # 1000 mW
dist = 10 * 3 * log10(1000)
Pr = Pt - 40 - dist
print(f'Pt = {Pt:.0f} dBm ; 10*3*log10(1000) = {dist:.0f} dB ; Pr = {Pr:.0f} dBm ; SNR = {Pr - (-120):.0f} dB -> {lin(Pr + 120):.0f}')
print(f'next part (c): g0/gbar = 10/100 = {lin(10) / lin(Pr + 120):.1f}')

h('t2 table C, left: Practice 2 Q1: rho = 0.1 (signal strength = amplitude), fD = 50 Hz')
rho, fm = 0.1, 50
afd = (exp(rho ** 2) - 1) / (sqrt(2 * pi) * fm * rho)
print(f'rho^2 = {rho ** 2:.2f} ; 20log10(0.1) = {20 * log10(rho):.0f} dB ; AFD = {afd * 1e3:.2f} ms')

h('t2 table C, right: mock A.Q3 (c): power 10 dB below rms, 72 km/h, 1.8 GHz')
pr = lin(-10); rho = sqrt(pr); fm = (72 / 3.6) * 1.8e9 / 3e8
afd = (exp(rho ** 2) - 1) / (sqrt(2 * pi) * fm * rho)
afd_wrong = (exp(0.01) - 1) / (sqrt(2 * pi) * fm * 0.1)
print(f'power ratio = {pr:.1f} = rho^2 ; rho = {rho:.3f} ; 10log10(0.1) = {dB(pr):.0f} dB = 20log10({rho:.3f}) = {20 * log10(rho):.0f} dB')
print(f'fm = {fm:.0f} Hz ; AFD = {afd * 1e3:.3f} ms ; wrong rho = 0.1 -> AFD = {afd_wrong * 1e3:.3f} ms')

h('t2 noise floor check (outside the slides): kT at 290 K')
kT = 1.380649e-23 * 290
print(f'k*T0 with T0 = 290 K: 10log10(kT / 1 mW) = {dB(kT / 1e-3):.2f} dBm/Hz (about -174)')

h('t2 quick-conversion table')
for r in (2, 4, 10, 100, 1000, 0.5, 0.1, 0.01):
    print(f'power x{r}: {dB(r):+.2f} dB')
for mw, name in ((1, '1 mW'), (100, '100 mW'), (500, '0.5 W'), (1000, '1 W'), (1e4, '10 W'), (1e-3, '1 uW'), (1e-9, '1 pW')):
    print(f'{name} = {dB(mw):.2f} dBm')
for a in (2, 10, 0.1, sqrt(0.1), 0.5):
    print(f'amplitude x{a:.3f}: {20 * log10(a):+.2f} dB')
print('dB -> linear seen in finals / Practice:')
for d_ in (3, 10, 11, 12, 13, 18, 25):
    print(f'  {d_} dB -> {lin(d_):.2f} ({lin(d_):.1f})')
print(f'final 2025-26 S2 Q1(b)(i): array gain 15 - 12 = 3 dB -> 10^0.3 = {lin(3):.3f} (about 2)')
print(f'lecturer example (teacher/notes.py, 3.5): 8.5 dB -> 10^0.85 = {lin(8.5):.2f}')
print(f'Practice 1 Q2 (a): margin 15 - 10 = 5 dB ; 5/8 = {5 / 8:.3f} ; Q(0.625) = {Q(0.625):.3f} ; linear 10^0.5 = {lin(5):.2f} times')
print(f'1 W = 0 dBW = {dB(1000):.0f} dBm')

h('t2 example 1: Pt 0.5 W, total loss 110 dB, B 200 kHz, N0 -174 dBm/Hz')
Pt = dB(500); Pr = Pt - 110; Bw = 200e3; Nn = -174 + dB(Bw); s_db = Pr - Nn
print(f'Pt = {Pt:.2f} dBm (= 30 - {dB(2):.2f}) ; Pr = {Pr:.2f} dBm')
print(f'0.5 W = {500} mW ; 10log10({Bw:.0e}) = {dB(Bw):.2f} ; N = {Nn:.2f} dBm ; SNR = {s_db:.2f} dB -> 10^{s_db / 10:.3f} = {lin(s_db):.4g} = {lin(s_db):.2e}')
print(f'C = 2e5 * log2(1 + {lin(s_db):.0f}) = 2e5 * {log2(1 + lin(s_db)):.2f} = {Bw * log2(1 + lin(s_db)) / 1e6:.2f} Mbps')

h('t2 example 2: backwards: B 1 MHz, N0 -174, SNR >= 15 dB, path loss 125 dB -> min Pt')
Nn = -174 + dB(1e6); Prmin = Nn + 15; Ptmin = Prmin + 125
print(f'10log10({1e6:.0e}) = {dB(1e6):.0f} ; N = {Nn:.0f} dBm ; Pr,min = {Prmin:.0f} dBm ; Pt,min = {Ptmin:.0f} dBm = {lin(Ptmin):.0f} mW = {lin(Ptmin) / 1000:.2f} W')

h('t2 example 3: S -80 dBm, I -85 dBm, N -90 dBm')
S, I, N = -80, -85, -90
Imw, Nmw = lin(I), lin(N)
IN = Imw + Nmw
print(f'SNR = {S - N} dB ; SIR = {S - I} dB')
print(f'I = 10^({I}/10) = 10^{I / 10:.1f} = {Imw:.3e} mW ; N = 10^{N / 10:.0f} = {Nmw:.0e} mW ; I+N = {IN:.3e} mW -> {dB(IN):.2f} dBm')
print(f'SINR = {S - dB(IN):.2f} dB -> 10^{(S - dB(IN)) / 10:.3f} = {lin(S - dB(IN)):.2f}')
print(f'check 1/(1/SIR + 1/SNR) = 1/({1 / lin(5):.4f} + {1 / lin(10):.1f}) = {1 / (1 / lin(5) + 1 / lin(10)):.2f}')
print(f'wrong: -85 + (-90) = {I + N} "dBm" (meaningless)')

print('\nall numbers above are the ones printed in frag_prob_db.html')
