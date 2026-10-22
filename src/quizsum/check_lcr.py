#!/usr/bin/python3
"""Numbers for quizsum/frag_lcr.html (topic t10: level crossing rate and average fade duration).

Every number printed in the fragment comes from a line below (tables A/B/C, the 2024-25 variation,
examples 1-3, traps, exam English). Stdlib only. Run: /usr/bin/python3 check_lcr.py

Sources: 2025-26 S2 Q1(a)(ii) and 2024-25 S2 Q1(a)(ii) (src/exams/data_2526s2.py, data_2425.py),
Practice 2 Q1 (prac_2.html p2q1), mock A Q3(c) and mock C Q2(b)(c) (prac_8.html p8q3, p8q8),
slide example Ch2 p.45-47 (learn_02.html section 2.6).
"""
from math import sqrt, pi, exp, log, log10

S2P = sqrt(2 * pi)            # common factor of the Rayleigh LCR / AFD formulas
C = 3e8                       # speed of light, m/s


def lcr(fm, rho):             # L_Z = sqrt(2 pi) fm rho e^(-rho^2)
    return S2P * fm * rho * exp(-rho ** 2)


def afd(fm, rho):             # AFD = (e^(rho^2) - 1) / (sqrt(2 pi) fm rho)
    return (exp(rho ** 2) - 1) / (S2P * fm * rho)


def dB(x):
    return 10 * log10(x)


def head(t):
    print(f'\n=== {t}')


print(f'sqrt(2*pi) = {S2P:.4f}  (shown as 2.5066; with 2.507 the chains 2.507 x 120 x 0.3162 = {2.507*120*0.3162:.4f} '
      f'and 2.507 x 50 x 0.1 = {2.507*50*0.1:.3f} no longer round to the shown 95.12 / 12.53)')

# ---------------------------------------------------------------- symbol table / formula cards
head('symbol table and formula cards')
print(f'Rs 50 ksps -> Ts = {1/50e3*1e6:g} us')
print(f'72 km/h -> {72/3.6:g} m/s')
print(f'rho wording: "10% of rms" -> rho = 0.1, rho^2 = {0.1**2:.2f}, {dB(0.1**2):.1f} dB')
print(f'rho wording: "power 10 dB below" -> rho^2 = {10**(-10/10):g}, rho = {10**(-10/20):.4f}')
print(f'rho wording: "threshold power = 1% of mean" -> rho^2 = 0.01, rho = {sqrt(0.01):g}')

# ---------------------------------------------------------------- (A) counting method
head('(A) counting: 2025-26 S2 Q1(a)(ii)  [Ts 5 ms, AFD 20 ms, 40 fades in 10 s]')
N, T, A, Ts = 40, 10, 20e-3, 5e-3
L = N / T; ns = A / Ts; ne = L * ns; fr = L * A; Rs = 1 / Ts
print(f'(1) LCR = {N}/{T} = {L:g} /s')
print(f'(2) per fade = {A*1e3:g} ms / {Ts*1e3:g} ms = {ns:g}')
print(f'(3) errors/s = {L:g} x {ns:g} = {ne:g}')
print(f'(4) fraction = {L:g} x {A*1e3:g} ms = {fr:g}')
print(f'(5) Rs = 1/Ts = {Rs:g} /s ; SER = {ne:g} / {Rs:g} = {ne/Rs:g}  (= fraction)')

head('(A) counting: mock C Q2(b)  [Rs 50 ksps, AFD 0.5 ms, 300 fades in 10 s]')
N, T, A, Rs = 300, 10, 0.5e-3, 50e3
Ts = 1 / Rs; L = N / T; ns = A / Ts; ne = L * ns; fr = L * A
print(f'Ts = 1/{Rs:g} = {Ts*1e6:g} us')
print(f'(1) LCR = {N}/{T} = {L:g} /s')
print(f'(2) per fade = {A*1e3:g} ms / {Ts*1e6:g} us = {ns:g}')
print(f'(3) errors/s = {L:g} x {ns:g} = {ne:g}')
print(f'(4) fraction = {L:g} x {A*1e3:g} ms = {fr:g} ({fr*100:g}%)')
print(f'(5) SER = {ne:g} / {Rs:g} = {ne/Rs:g}  (= fraction)')
print(f'trap: units not unified, 0.5 / 20 = {0.5/20:g} (wrong) vs 0.5 ms / 20 us = {ns:g}')
mockC_frac, mockC_L = fr, L

head('variation: 2024-25 S2 Q1(a)(ii)  [AFD 6 us covers exactly 3 symbols, LCR 5]')
A, k, L = 6e-6, 3, 5
Ts = A / k
print(f'Ts = {A*1e6:g} us / {k} = {Ts*1e6:g} us ; Rs = {1/Ts:g} /s = {1/Ts/1e3:g} k/s')
print(f'errors/s = {L} x {k} = {L*k}')

# ---------------------------------------------------------------- (B) Rayleigh formulas
head('(B) formula: Practice 2 Q1  [fD 50 Hz, rho 0.1]')
fm, rho = 50, 0.1
den = S2P * fm * rho
L, A = lcr(fm, rho), afd(fm, rho)
print(f'rho = {rho} ; rho^2 = {rho**2:g} ; {dB(rho**2):.1f} dB')
print(f'denominator sqrt(2pi) fm rho = 2.5066 x {fm} x {rho} = {den:.2f}  (literal {2.5066*fm*rho:.4f})')
print(f'e^(rho^2) - 1 = {exp(rho**2)-1:.5f} ; AFD = {exp(rho**2)-1:.5f} / {den:.2f} = {A*1e3:.3f} ms = {A:.3e} s')
print(f'e^(-rho^2) = {exp(-rho**2):.5f} ; LCR = {den:.2f} x e^-0.01 = {L:.2f} /s')
print(f'check LCR x AFD = {L:.2f} x {A*1e3:.3f} ms = {L*A:.5f} ; 1 - e^-0.01 = {1-exp(-rho**2):.5f}')
p2_L, p2_A = L, A

head('(B) formula: mock A Q3(c)  [1.8 GHz, 72 km/h, 50 ksps, power not more than 10 dB below rms]')
v, fc, Rs = 72 / 3.6, 1.8e9, 50e3
fm = v * fc / C; rho = sqrt(10 ** (-10 / 10))
den = S2P * fm * rho
L, A = lcr(fm, rho), afd(fm, rho)
print(f'rho^2 = 10^-1 = {rho**2:g} ; rho = sqrt(0.1) = {rho:.5f}  (4 s.f. elsewhere: {rho:.4f})')
print(f'v = {v:g} m/s ; fm = {v:g} x {fc:g} / {C:g} = {fm:g} Hz')
print(f'denominator = 2.5066 x {fm:g} x {rho:.5f} = {den:.2f}  (literal {2.5066*fm*0.31623:.4f})')
print(f'e^0.1 - 1 = {exp(0.1)-1:.4f} ; AFD = {exp(0.1)-1:.4f} / {den:.2f} = {A*1e3:.3f} ms')
print(f'e^-0.1 = {exp(-0.1):.5f} ; LCR = {den:.2f} x {exp(-0.1):.5f} = {L:.2f} /s  (literal 95.12 x 0.90484 = {95.12*0.90484:.4f}; '
      f'with 0.9048 it would be {95.12*0.9048:.4f})')
print(f'check LCR x AFD = {L:.2f} x {A*1e3:.3f} ms = {L*A:.4f} ; 1 - e^-0.1 = {1-exp(-0.1):.4f}')
print(f'symbols per fade = {A*1e3:.3f} ms / {1e6/Rs:g} us = {A*Rs:.1f} ~ {round(A*Rs)}')
wrong = afd(fm, 0.1)
print(f'trap: rho taken as 0.1 -> AFD = {wrong*1e3:.3f} ms (true {A*1e3:.3f} ms, ratio {A/wrong:.2f})')

# ---------------------------------------------------------------- (C) back out rho
head('(C) reverse: Practice 2 Q1 back-check')
fr = p2_L * p2_A
r2 = log(1 / (1 - fr)); r = sqrt(r2)
print(f'(1) fraction = {p2_L:.2f} x {p2_A*1e3:.3f} ms = {fr:.5f} ; 1 - fraction = {1-fr:.5f}')
print(f'(2) rho^2 = ln(1/{1-fr:.5f}) = {r2:.4f}')
print(f'(3) 10 log10 rho^2 = {dB(r2):.1f} dB ; rho = {r:.3f}')
print(f'(4) fm = {p2_L:.2f} / (2.5066 x {r:.1f} x {exp(-r2):.3f}) = {p2_L/(S2P*r*exp(-r2)):.1f} Hz  (literal {12.41/(2.5066*0.1*0.990):.3f})')

head('(C) reverse: mock C Q2(c)')
fr = mockC_frac
r2 = log(1 / (1 - fr)); r = sqrt(r2)
print(f'(1) fraction = 30 x 0.5 ms = {fr:g} ; 1 - fraction = {1-fr:g}')
print(f'(2) rho^2 = ln(1/{1-fr:g}) = {r2:.5f}')
print(f'(3) 10 log10 rho^2 = {dB(r2):.2f} dB ; 20 log10 rho = {20*log10(r):.2f} dB ; rho = {r:.4f}')
lit = 30 / (2.5066 * 0.1229 * 0.985)
print(f'(4) e^-rho^2 = {exp(-r2):.3f} ; fm = {mockC_L:g} / (2.5066 x {r:.4f} x {exp(-r2):.3f}) = {mockC_L/(S2P*r*exp(-r2)):.2f} Hz exact, '
      f'{lit:.2f} from the shown operands -> shown as ~ {round(lit)} Hz (given 100 Hz)')

# ---------------------------------------------------------------- examples
head('Example 1: 10 s window, symbol rate given  [Rs 25 ksps, 150 fades in 10 s, AFD 0.8 ms]')
N, T, A, Rs = 150, 10, 0.8e-3, 25e3
Ts = 1 / Rs; L = N / T; ns = A / Ts; ne = L * ns
print(f'(a) LCR = {N}/{T} = {L:g} /s')
print(f'(b) Ts = 1/{Rs:g} = {Ts*1e6:g} us ; per fade = {A*1e3:g} ms / {Ts*1e6:g} us = {ns:g} ; AFD x Rs = {A*Rs:g}')
print(f'(c) errors/s = {L:g} x {ns:g} = {ne:g}')
print(f'(d) SER = {ne:g}/{Rs:g} = {ne/Rs:g} ; LCR x AFD = {L:g} x {A*1e3:g} ms = {L*A:g} ({L*A*100:g}%)')
Rs2 = 100e3
print(f'(e) Rs = {Rs2:g}: per fade = {A*Rs2:g} ; errors/s = {L:g} x {A*Rs2:g} = {L*A*Rs2:g} ; SER = {L*A*Rs2/Rs2:g}')

head('Example 2: formula, 10% of rms, 900 MHz, 60 km/h, Rs 100 ksps')
v, fc, rho, Rs = 60 / 3.6, 900e6, 0.1, 100e3
fm = v * fc / C; lam = C / fc
L, A = lcr(fm, rho), afd(fm, rho)
den = S2P * fm * rho
print(f'(a) rho = {rho} ; rho^2 = {rho**2:g} ; {dB(rho**2):.0f} dB')
print(f'(a) v = 60/3.6 = {v:.2f} m/s ; fm = {v:.2f} x {fc:g} / {C:g} = {fm:.1f} Hz ; lambda = {lam:.4f} m ; v/lambda = {v/lam:.1f} Hz'
      f'  (literal 16.67/0.3333 = {16.67/0.3333:.3f}; with 0.333 it would be {16.67/0.333:.3f})')
print(f'(b) denominator = {den:.2f} ; LCR = {L:.2f} /s ; AFD = {exp(rho**2)-1:.5f}/{den:.2f} = {A*1e3:.3f} ms')
ns = A * Rs; ne = L * ns
print(f'(c) per fade = {A*1e3:.3f} ms x {Rs:g} = {ns:.1f} ~ {round(ns)} ; errors/s = {L:.2f} x {ns:.1f} = {ne:.0f} ; check (1-e^-0.01) x 1e5 = {(1-exp(-rho**2))*Rs:.0f}')
print(f'(c) fades in 10 s = {L:.2f} x 10 = {L*10:.1f} ~ {round(L*10)}')
fm2 = (120 / 3.6) * fc / C
L2, A2 = lcr(fm2, rho), afd(fm2, rho)
print(f'(d) 120 km/h: fm = {fm2:.1f} Hz ; LCR = {L2:.2f} /s ; AFD = {A2*1e3:.3f} ms ; per fade = {A2*Rs:.1f} ; fraction = {L2*A2:.5f} ; errors/s = {L2*A2*Rs:.0f}')

head('Example 3: SER, threshold 15 dB below rms power, fm 80 Hz, Rs 40 ksps')
X, fm, Rs = 15, 80, 40e3
r2 = 10 ** (-X / 10); rho = sqrt(r2)
ser = 1 - exp(-r2)
den = S2P * fm * rho
L, A = lcr(fm, rho), afd(fm, rho)
print(f'(a) rho^2 = 10^-1.5 = {r2:.5f} ; rho = 10^(-15/20) = {rho:.5f}')
print(f'(a) SER = 1 - e^-{r2:.5f} = {ser:.5f} ~ {ser:.3g} ({ser*100:.1f}%)')
print(f'(b) denominator = 2.5066 x {fm} x {rho:.5f} = {den:.2f}  (literal {2.5066*80*0.17783:.4f}) ; e^-rho^2 = {exp(-r2):.4f} ; LCR = {L:.2f} /s')
print(f'(b) e^rho^2 - 1 = {exp(r2)-1:.5f} ; AFD = {exp(r2)-1:.5f}/{den:.2f} = {A*1e3:.3f} ms')
print(f'(b) per fade = {A*1e3:.3f} ms x {Rs:g} = {A*Rs:.2f} ; errors/s = {L:.2f} x {A*Rs:.2f} = {L*A*Rs:.0f} ; SER x Rs = {ser*Rs:.0f}')
eps = 1e-3
r2max = log(1 / (1 - eps))
print(f'(c) rho^2 <= ln(1/(1-0.001)) = {r2max:.4e} ; 10 log10(1/rho^2) = {dB(1/r2max):.2f} dB ~ {dB(1/r2max):.1f} dB')

# ---------------------------------------------------------------- traps: slide example p.45-47
head('trap: slide example Ch2 p.45-47 [rho 0.1, 120 km/h, 5 GHz, 1 Msps]')
v, fc, rho, Rs = 120 / 3.6, 5e9, 0.1, 1e6
fm = v * fc / C
L, A = lcr(fm, rho), afd(fm, rho)
print(f'fm = {fm:.2f} Hz ; LCR = {L:.2f} /s ; AFD = {A*1e6:.2f} us ; errors/s = {L*A*Rs:.0f} ; (1-e^-0.01) x 1e6 = {(1-exp(-0.01))*1e6:.0f}')
print(f'slide printed AFD 71.17 us, 9812 /s: {L:.2f} x 71.17 = {L*71.17:.0f}  (9812 follows from the misprinted AFD)')
