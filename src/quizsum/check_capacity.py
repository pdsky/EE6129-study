#!/usr/bin/python3
"""Numbers for frag_capacity.html: Quiz-summary topics t11 (Shannon, SNR/SIR/SINR), t12 (Rayleigh outage
capacity, fade margin) and t13 (water-filling). Every number printed in the fragment comes from this script.
Sources of the real questions: Practice 2 Q3 (prac_2.html p2q3), mock B Q1/Q3 and C Q3 (prac_8.html p8q4,
p8q6, p8q9), finals 2023-24 Q1(a)(iv), 2024-25 Q1(a)(iii), 2025-26 S2 Q1(a)(iii) (src/exams/data_*.py).
stdlib only.  usage: /usr/bin/python3 check_capacity.py
"""
from math import log10, log2, log, exp

lin = lambda d: 10 ** (d / 10)
dB = lambda x: 10 * log10(x)
lnf = lambda e: log(1 / (1 - e))                     # ln(1/(1-eps))
FM = lambda e: dB(1 / lnf(e))                        # Rayleigh fade margin, dB


def head(s):
    print(f'\n=== {s}')


def wf(gs, P=1.0, B=1.0, label=''):
    """Water-filling, lecture procedure: assume all on, solve 1/g0, drop the worst if any g_i < g0, repeat."""
    on = list(range(len(gs)))
    print(f'  {label} linear SNR = {[round(g, 4) for g in gs]} ; 1/g = {[round(1 / g, 5) for g in gs]}')
    rnd = 1
    while True:
        inv0 = (1 + sum(1 / gs[i] for i in on)) / len(on)
        g0 = 1 / inv0
        bad = [i + 1 for i in on if gs[i] < g0]
        neg = {i + 1: round(inv0 - 1 / gs[i], 4) for i in on if gs[i] < g0}
        print(f'  round {rnd}: on = {[i + 1 for i in on]} n = {len(on)} ; 1 + sum(1/g) = {1 + sum(1 / gs[i] for i in on):.5f}'
              f' ; 1/g0 = {inv0:.5f} ; g0 = {g0:.4f} ({dB(g0):.2f} dB) ; fails g_i < g0: {bad}'
              + (f' ; would-be P_i/P = {neg}' if neg else ''))
        if not bad:
            break
        on.remove(min(on, key=lambda i: gs[i]))
        rnd += 1
    Pi = [P * (inv0 - 1 / gs[i]) if i in on else 0.0 for i in range(len(gs))]
    print(f'  P_i/P = {[round(inv0 - 1 / gs[i], 6) if i in on else 0 for i in range(len(gs))]} ; P_i (W, P = {P}) = {[round(p, 5) for p in Pi]} ; sum = {sum(Pi):.4f}')
    terms = [log2(gs[i] / g0) for i in on]
    print(f'  g_i/g0 = g_i x (1/g0) = {[round(gs[i] / g0, 5) for i in on]} ; log2 terms = {[round(t, 5) for t in terms]} ; C = B*sum = {B * sum(terms):.4f} (B = {B})')
    return on, inv0, g0, Pi, B * sum(terms)


# ============================================================== t11 Shannon / SINR
head('t11 symbols: calculator constants for log2')
print(f'log10(2) = {log10(2):.4f} ; ln(2) = {log(2):.4f} ; 10log10(2) = {dB(2):.2f} dB')

head('t11 table 1, column 3: Practice 2 Q3 (P1 = P2 = 10 mW, N = 0.1 mW, B = 20 MHz)')
S, I, N, B = 10, 10, 0.1, 20e6
sinr = S / (I + N); snr = S / N
C1, C2 = B * log2(1 + sinr) / 1e6, B * log2(1 + snr) / 1e6
print(f'(a) SINR = {sinr:.4f} ({dB(sinr):.4f} dB) ; log2(1+SINR) = log2({1 + sinr:.4f}) = {log2(1 + sinr):.4f} ; C1 = {C1:.2f} Mbps')
print(f'(b) SNR = {snr:.0f} ({dB(snr):.2f} dB) ; log2(101) = {log2(101):.4f} ; C2 = {C2:.2f} Mbps')
print(f'check: C1 + C2 = {C1 + C2:.2f} ; 20 log2(1 + 20/0.1) = 20 log2(201) = {20 * log2(201):.2f} Mbps')
print(f'trap (pretend user 2 absent in (a)): SNR 100 -> {B * log2(101) / 1e6:.2f} Mbps')

head('t11 table 1, column 4: mock C Q3 (a)(b) (S = 2 mW, I = 0.5 mW, N = 0.05 mW, B = 10 MHz)')
S, I, N, B = 2, 0.5, 0.05, 10e6
snr, sir, sinr = S / N, S / I, S / (I + N)
Ca, Cb = B * log2(1 + sinr) / 1e6, B * log2(1 + snr) / 1e6
print(f'(a) SNR = {snr:.1f} ({dB(snr):.2f} dB) ; SIR = {sir:.1f} ({dB(sir):.2f} dB) ; SINR = {sinr:.4f} ({dB(sinr):.2f} dB)')
print(f'    log2(1 + SINR) = log2({1 + sinr:.3f}) = {log2(1 + sinr):.4f} ; C = {Ca:.2f} Mbps')
print(f'(b) log2(41) = {log2(41):.4f} ; C = {Cb:.2f} Mbps ; ratio = {Cb / Ca:.2f} ; I/N = {I / N:.0f}')

head('t11 table 2: mock B Q3 (a)(b) (S = -90 dBm, N0 = -174 dBm/Hz, B = 5 MHz -> 10 MHz)')
for Bw in (5e6, 10e6):
    Nd = -174 + dB(Bw); sd = -90 - Nd; s = lin(sd); C = Bw * log2(1 + s) / 1e6
    print(f'B = {Bw / 1e6:.0f} MHz: 10log10 B = {dB(Bw):.2f} ; N = {Nd:.2f} dBm ; SNR = {sd:.2f} dB = 10^{sd / 10:.4f} = {s:.2f}'
          f' ; log2(1 + SNR) = log2({1 + s:.2f}) = {log2(1 + s):.3f} ; C = {C:.2f} Mbps')
r = (10e6 * log2(1 + lin(-90 + 174 - dB(10e6)))) / (5e6 * log2(1 + lin(-90 + 174 - dB(5e6))))
print(f'ratio = {r:.3f} ; doubling B adds 10log10(2) = {dB(2):.2f} dB of noise')
print(f'trap: SNR in dB into log2: log2(1 + 17.01) = {log2(1 + 17.01):.2f} (vs correct {log2(1 + lin(17.0103)):.2f})')

head('t11 example 1: S = 10 mW, N0 = 1e-9 W/Hz, B = 1 MHz -> 2 MHz')
S = 10e-3; N0 = 1e-9
for Bw in (1e6, 2e6):
    N = N0 * Bw; s = S / N
    print(f'B = {Bw / 1e6:.0f} MHz: N = {N:.0e} W ({dB(N / 1e-3):.2f} dBm) ; SNR = {s:.0f} ({dB(s):.2f} dB) ; log2(1+SNR) = {log2(1 + s):.4f} ; C = {Bw * log2(1 + s) / 1e6:.2f} Mbps')
c1, c2 = 1e6 * log2(11), 2e6 * log2(6)
print(f'ratio = {c2 / c1:.2f} ; power also doubled (SNR stays 10): 2 MHz x log2(11) = {2 * log2(11):.2f} Mbps')

head('t11 example 2: B = 5 MHz, R = 20 Mbps, N = -100 dBm')
smin = 2 ** (20 / 5) - 1
print(f'R/B = {20 / 5:.0f} ; SNR_min = 2^4 - 1 = {smin:.0f} = {dB(smin):.2f} dB ; S_min = {-100 + dB(smin):.2f} dBm')
print(f'(c) SNR 10 dB = {lin(10):.0f} ; C = 5 x log2(11) = {5 * log2(11):.2f} Mbps')

head('t11 example 3: P1 = 8 mW, P2 = 2 mW, N = 0.2 mW, B = 10 MHz each')
P1, P2, N, B = 8, 2, 0.2, 10
s1 = P1 / (P2 + N); s2 = P2 / N
print(f'(a) decode 1 first: SINR1 = {s1:.4f} ({dB(s1):.2f} dB) ; log2({1 + s1:.3f}) = {log2(1 + s1):.4f} ; C1 = {B * log2(1 + s1):.2f}'
      f' ; SNR2 = {s2:.0f} ({dB(s2):.0f} dB) ; log2(11) = {log2(11):.4f} ; C2 = {B * log2(1 + s2):.2f} ; sum = {B * (log2(1 + s1) + log2(1 + s2)):.2f}')
t2 = P2 / (P1 + N); t1 = P1 / N
print(f'(b) decode 2 first: SINR2 = {t2:.4f} ({dB(t2):.2f} dB) ; log2({1 + t2:.4f}) = {log2(1 + t2):.4f} ; C2 = {B * log2(1 + t2):.2f}'
      f' ; SNR1 = {t1:.0f} ({dB(t1):.2f} dB) ; log2(41) = {log2(41):.4f} ; C1 = {B * log2(1 + t1):.2f} ; sum = {B * (log2(1 + t2) + log2(1 + t1)):.2f}')
print(f'check: 10 log2(1 + 10/0.2) = 10 log2(51) = {B * log2(51):.2f} Mbps')
print(f'(c) no MUD: {B * log2(1 + s1):.2f} + {B * log2(1 + t2):.2f} = {B * (log2(1 + s1) + log2(1 + t2)):.2f} Mbps ; fraction of MUD sum = {(log2(1 + s1) + log2(1 + t2)) / log2(51):.3f}')
print(f'    SIR1 if noise ignored = {P1 / P2:.0f} ({dB(P1 / P2):.2f} dB)')

# ============================================================== t12 outage capacity / fade margin
head('t12 formula card: FM for eps = 1%, 0.5%, 0.1%, 10% (exact vs approx 10log10(1/eps))')
for e in (0.01, 0.005, 0.001, 0.1):
    print(f'  eps {e}: ln(1/(1-eps)) = {lnf(e):.6f} ; FM exact = {FM(e):.2f} dB ; approx = {dB(1 / e):.2f} dB')

head('t12 table 1, column 3: final 2025-26 S2 Q1(a)(iii) (gbar_R = 25 dB, eps = 0.005)')
gb, e = lin(25), 0.005
gm = gb * lnf(e)
print(f'gbar = 10^2.5 = {gb:.1f} ; ln(1/0.995) = {lnf(e):.6f} ; g_min = {gm:.4f} = {dB(gm):.2f} dB ; FM = 25 - {dB(gm):.2f} = {25 - dB(gm):.2f} dB ; formula {FM(e):.2f} dB')
print(f'(not asked) C_eps/B = log2(1 + {gm:.3f}) = log2({1 + gm:.3f}) = {log2(1 + gm):.3f} bit/s/Hz')
print(f'check: 1 - e^(-g_min/gbar) = {1 - exp(-gm / gb):.4f}')
wrong = gb * log10(1 / (1 - e))
print(f'trap (log10 instead of ln): log10(1/0.995) = {log10(1 / 0.995):.6f} ; g_min = {wrong:.4f} ({dB(wrong):.2f} dB) ; FM = {25 - dB(wrong):.2f} dB')

head('t12 table 1, column 4: mock C Q3 (c) (gbar = 20 dB, eps = 1%, B = 10 MHz)')
gb, e, B = lin(20), 0.01, 10
gm = gb * lnf(e)
print(f'gbar = {gb:.0f} ; ln(1/0.99) = {lnf(e):.5f} ; g_min = {gm:.4f} = {dB(gm):.2f} dB ; FM = {20 - dB(gm):.2f} dB')
print(f'C_eps = 10 MHz x log2({1 + gm:.3f}) = 10 x {log2(1 + gm):.4f} = {B * log2(1 + gm):.2f} Mbps ; AWGN 20 dB: 10 x log2(101) = {B * log2(101):.2f} Mbps ; ratio {log2(101) / log2(1 + gm):.2f}')

head('t12 table 2, column 3: final 2023-24 Q1(a)(iv) (eps = 0.1%)')
e = 0.001
print(f'ln(1/0.999) = {lnf(e):.7f} ; 1/ln = {1 / lnf(e):.1f} ; FM = {FM(e):.2f} dB')

head('t12 table 2, column 4: mock B Q1 (b) (threshold 7 dB, eps = 1%)')
g0, e = lin(7), 0.01
gbn = g0 / lnf(e)
print(f'g0 = 10^0.7 = {g0:.3f} ; 1/ln(1/0.99) = {1 / lnf(e):.2f} ; FM = {FM(e):.2f} dB ; gbar needed = {g0:.3f}/{lnf(e):.5f} = {gbn:.1f} = {dB(gbn):.2f} dB ; 7 + FM = {7 + FM(e):.2f} dB')

head('t12 example 1: gbar = 30 dB, eps = 2%, B = 1 MHz')
gb, e = lin(30), 0.02
gm = gb * lnf(e)
ce = log2(1 + gm)
print(f'gbar = {gb:.0f} ; ln(1/0.98) = {lnf(e):.5f} ; g_min = {gm:.3f} = {dB(gm):.2f} dB ; FM = 30 - {dB(gm):.2f} = {30 - dB(gm):.2f} ; formula {FM(e):.2f} dB')
print(f'C_eps = 1 MHz x log2({1 + gm:.2f}) = {ce:.3f} Mbps ; (1-eps) C_eps = 0.98 x {ce:.3f} = {0.98 * ce:.3f} Mbps ; AWGN 30 dB: log2(1001) = {log2(1001):.3f} Mbps')
print(f'check: 1 - e^(-{gm / gb:.5f}) = {1 - exp(-gm / gb):.4f}')

head('t12 example 2: eps = 1%, need C_eps/B = 2 bit/s/Hz')
gm = 2 ** 2 - 1; e = 0.01
gbn = gm / lnf(e)
print(f'g_min = 2^2 - 1 = {gm} = {dB(gm):.2f} dB ; gbar = {gm}/{lnf(e):.5f} = {gbn:.1f} = {dB(gbn):.2f} dB ; FM = {dB(gbn) - dB(gm):.2f} dB')

head('t12 example 3: eps = 5%, gbar = 15 dB and 25 dB; tighten to 0.5%')
e = 0.05
print(f'ln(1/0.95) = {lnf(e):.5f} ; FM = {FM(e):.2f} dB ; approx 10log10(20) = {dB(1 / e):.2f} dB ; diff {dB(1 / e) - FM(e):.2f} dB')
for gdb in (15, 25):
    gb = lin(gdb); gm = gb * lnf(e)
    print(f'  gbar {gdb} dB = {gb:.2f} : g_min = {gm:.3f} = {dB(gm):.2f} dB ; FM = {gdb} - {dB(gm):.2f} = {gdb - dB(gm):.2f} dB')
print(f'eps 0.5%: FM = {FM(0.005):.2f} dB ; extra = {FM(0.005):.2f} - {FM(e):.2f} = {FM(0.005) - FM(e):.2f} dB')

# ============================================================== t13 water-filling
head('t13 table, column 3: final 2024-25 Q1(a)(iii) (18, 10, 3 dB, P = 1 W)')
wf([lin(18), lin(10), lin(3)], P=1, B=1, label='2024-25:')
print('  (per-Hz capacity is not asked in the paper; printed only as an extension)')

head('t13 table, column 4: mock B Q3 (c) (SNR 20 and 0.5, 1 MHz each)')
wf([20, 0.5], P=1, B=1, label='mock B Q3c:')
print(f'  equal split (each P/2: SNR 10 and 0.25): log2(11) + log2(1.25) = {log2(11):.4f} + {log2(1.25):.4f} = {log2(11) + log2(1.25):.2f} Mbps')

head('t13 lecture example Ch2 p.56-57 (17.77, 2.63, 0.087) - only cited as "third one dropped"')
wf([17.77, 2.63, 0.087], label='slides:')

head('t13 example 1: 12 dB and 6 dB, P = 2 W, 1 MHz each')
g = [lin(12), lin(6)]
on, inv0, g0, Pi, C = wf(g, P=2, B=1, label='ex1:')
eq = log2(1 + g[0] / 2) + log2(1 + g[1] / 2)
print(f'  equal split 1 W each: SNR {g[0] / 2:.3f}, {g[1] / 2:.3f} ; log2({1 + g[0] / 2:.3f}) + log2({1 + g[1] / 2:.3f}) = {log2(1 + g[0] / 2):.3f} + {log2(1 + g[1] / 2):.3f} = {eq:.2f} Mbps')
print(f'  as written in the fragment (arguments rounded first): log2(10.42) = {log2(10.42):.3f} ; log2(2.616) = {log2(2.616):.3f} ;'
      f' log2(8.924) = {log2(8.924):.3f} ; log2(2.991) = {log2(2.991):.3f} ; 3.158 + 1.581 = {3.158 + 1.581:.2f}')

head('t13 example 2: 15, 6, -3 dB, P = 1 W, 1 MHz each (third dropped)')
wf([lin(15), lin(6), lin(-3)], P=1, B=1, label='ex2:')

head('t13 example 3: 20, 10, 0, -5 dB, P = 1 W, 1 MHz each (dropped twice)')
wf([lin(20), lin(10), lin(0), lin(-5)], P=1, B=1, label='ex3:')
print(f'  log2(55.5) = {log2(55.5):.3f} ; log2(5.55) = {log2(5.55):.3f}')
