#!/usr/bin/python3
"""Numbers for quizsum/frag_fadetype.html (topic t8: delay spread, flat vs frequency-selective;
topic t9: Doppler, fast vs slow, combined fading type).

Every number printed in the fragment comes from a line below (formula notes, steps tables,
examples, traps, exam English). Each block prints the precise value and then a 'shown:' line
with the exact rounded strings used in the fragment. Stdlib only.
Run: /usr/bin/python3 check_fadetype.py

Sources: Practice 1 Q3 (prac_1.html p1q3); mock A Q3 (prac_8.html p8q3); mock C Q2(a) (p8q8);
focused Q3(e)(f) (p8q12); 2023-24 S2 Q1(a)(iii) and Q2(b)(i) (src/exams/data_2324.py);
2025-26 S1 Q2(b)(i) (data_2526s1.py); 2025-26 S2 Q1(a)(i) (data_2526s2.py, explain question, no numbers).
Slide pages (Ch2, printed page numbers): p.30 mu/sigma, p.31-32 B_C and flat/selective, p.33 the 0.1 rule,
p.34 Doppler shift, p.35 Doppler spread, p.36 coherence time, p.37 slow/fast, p.38-39 the two figures.
Lecturer remarks quoted in the fragment (src/teacher/notes.py): 2.4 ratio "slightly above 0.1 (e.g. 0.15)"
-> no conclusion; 2.5 "signal bandwidth within the coherence bandwidth -> flat" (so B_s < B_C is written as flat,
with no extra "borderline" label; B_C ~ 1/sigma is order-of-magnitude only and is not used to convert B_s/B_C
into sigma/Ts).
"""
from math import sqrt, ceil

C = 3e8                      # speed of light, m/s


def lin(db):                 # dB -> linear power ratio (also dBm -> mW)
    return 10 ** (db / 10)


def pdp(taus, p):            # power-weighted mean, second moment, variance, rms spread
    s = sum(p)
    m1 = sum(t * w for t, w in zip(taus, p))
    m2 = sum(t * t * w for t, w in zip(taus, p))
    mu, e2 = m1 / s, m2 / s
    return s, m1, m2, mu, e2, e2 - mu * mu, sqrt(e2 - mu * mu)


def head(t):
    print(f'\n=== {t}')


def shown(*items):
    print('   shown:', ' | '.join(str(x) for x in items))


# ======================================================================= t8 formula notes
head('t8 formula notes')
for d in (0, -3, -6, -10):
    print(f'{d:>4} dB -> {lin(d):.4f}')
shown('1', f'{lin(-3):.4f}', f'{lin(-6):.4f}', f'{lin(-10):.1f}')
print(f'sqrt(12) = {sqrt(12):.3f}  (uniform on [0,a]: mu = a/2, E[tau^2] = a^2/3, sigma = a/sqrt(12))')
print('lecturer example of a ratio slightly above 0.1: 0.15 (notes.py 2.4)')
# 2025-26 S1 Q2(b): B_C given 30 kHz, maximum delay spread 10 us, available bandwidth 500 kHz.
# Use the given B_C directly (slide p.31: B_s < B_C -> flat). 10 us is the MAXIMUM delay spread (guard interval
# in (ii)), not sigma, so it is not turned into 1/sigma or compared with 0.1.
print(f'2025-26 S1 Q2(b)(i): N > 500/30 = {500/30:.2f} -> N_min = {ceil(500/30)} ; '
      f'500/{ceil(500/30)} = {500/ceil(500/30):.1f} kHz < 30 kHz -> flat')
print(f'2023-24 Q2(b)(i) (cited only): subcarrier = 500/2 = {500/2:.0f} kHz -> N = 1000/250 = {1000/250:.0f}')

# ======================================================================= t8 table 1
head('t8 table 1, Practice 1 Q3: uniform PDP P_r = 1 on 0-10 us')
a = 10.0
mu, e2 = a / 2, a * a / 3
var = e2 - mu * mu
sg = sqrt(var)
print(f'mu = a/2 = 10/2 = {mu:g} us ; E[tau^2] = a^2/3 = 100/3 = {e2:.4f} ; var = {e2:.2f} - 5^2 = {var:.4f} ; sigma = {sg:.4f} us')
print(f'flat: Ts > 10 sigma = {10*sg:.3f} us -> Rs < {1/(10*sg*1e-6)/1e3:.3f} ksps  (official 2.89 us, 34.6 ksps)')
shown(f'{mu:g}', f'{e2:.2f}', f'{var:.2f}', f'{sg:.2f}', f'{10*sg:.1f}', f'{1/(10*sg*1e-6)/1e3:.1f}')

head('t8 table 1, mock A Q3: taus 0/1/3 us, 0/-3/-6 dB, 50 ksps (1.8 GHz, 72 km/h)')
taus = [0, 1, 3]
P = [lin(d) for d in (0, -3, -6)]
s, m1, m2, mu, e2, var, sg = pdp(taus, P)
print(f'linear = {[round(x, 4) for x in P]} ; sum = {s:.4f}')
print(f'tau^2 = {[t*t for t in taus]}')
print(f'sum tau*P = 0x1 + 1x0.5012 + 3x0.2512 = {m1:.4f} ; mu = {mu:.4f} us')
print(f'sum tau^2*P = 0 + 1x0.5012 + 9x0.2512 = {m2:.4f} ; E[tau^2] = {e2:.4f} us^2')
print(f'mu^2 = {mu*mu:.4f} ; var = {var:.4f} ; sigma = {sg:.4f} us')
Ts = 1 / 50e3
print(f'Ts = {Ts*1e6:g} us ; sigma/Ts = {sg*1e-6/Ts:.4f} ; Rs max for flat = 0.1/sigma = {0.1/(sg*1e-6)/1e3:.2f} ksps')
shown(f'{s:.3f}', f'{m1:.3f}', f'{mu:.3f}', f'{m2:.3f}', f'{e2:.3f}', f'{var:.3f}', f'{sg:.2f}',
      f'{sg*1e-6/Ts:.3f}', f'{0.1/(sg*1e-6)/1e3:.1f}')
print(f'(trap) delay span 3 us vs sigma {sg:.2f} us')

# ======================================================================= t8 table 2
head('t8 table 2, 2023-24 Q1(a)(iii): sigma 0.01 ms, Ts 1 ms, time-invariant channel')
print(f'sigma/Ts = 0.01/1 = {0.01/1:.2f}')

head('t8 table 2 and t9 table 2, mock C Q2(a): 50 ksps (Bs ~ 50 kHz), B_C 200 kHz, f_m 100 Hz')
Bs, Bc, fm = 50e3, 200e3, 100
Ts = 1 / Bs
print(f'Bs/Bc = 50/200 = {Bs/Bc:.2f} -> Bs < Bc -> flat (slide p.31; practice page and verify_mock.py: flat, slow)')
print(f'Ts = {Ts*1e6:.0f} us ; B_D = f_m = {fm} Hz ; Bs/B_D = {Bs/fm:.0f} ; Tc ~ 1/fm = {1/fm*1e3:.0f} ms ; Tc/Ts = {(1/fm)/Ts:.0f}')

# ======================================================================= t8 examples
head('t8 example 1: taus 0/2/5 us, -80/-84/-90 dBm, then 100 ksps')
taus = [0, 2, 5]
dbm = [-80, -84, -90]
mw = [lin(d) for d in dbm]
print('mW =', [f'{x:.3e}' for x in mw])
P = [x / mw[0] for x in mw]
print('relative dB =', [d - dbm[0] for d in dbm], ' normalised =', [round(x, 4) for x in P])
print(f'tau^2 = {[t*t for t in taus]}')
s, m1, m2, mu, e2, var, sg = pdp(taus, P)
print(f'sum = {s:.4f} ; sum tau*P = {m1:.4f} ; mu = {mu:.4f} us')
print(f'sum tau^2*P = {m2:.4f} ; E[tau^2] = {e2:.4f} ; mu^2 = {mu*mu:.4f} ; var = {var:.4f} ; sigma = {sg:.4f} us')
print(f'flat: Ts > 10 sigma = {10*sg:.3f} us -> Rs < {1/(10*sg*1e-6)/1e3:.2f} ksps')
Ts = 1 / 100e3
print(f'100 ksps: Ts = {Ts*1e6:g} us ; sigma/Ts = {sg*1e-6/Ts:.4f}')
# mu is carried to 4 s.f. (0.8652) before squaring: 0.8652^2 = 0.7486 and 2.732 - 0.7486 = 1.983
# (0.865^2 would be 0.7482, so "0.865^2 = 0.749" must not be printed)
mu4 = round(mu, 4)
shown(f'{s:.3f}', f'{m1:.3f}', f'{mu:.4f}', f'{mu:.3f}', f'{m2:.3f}', f'{e2:.3f}', f'{mu4*mu4:.4f}', f'{var:.3f}',
      f'{sg:.2f}', f'{10*sg:.1f}', f'{10*sg:.2f}', f'{1/(10*sg*1e-6)/1e3:.1f}', f'{sg*1e-6/Ts:.3f}')
s2, _, _, mu2, _, _, sg2 = pdp(taus, mw)
print(f'(check) absolute mW weights give the same mu = {mu2:.4f} us, sigma = {sg2:.4f} us')

head('t8 example 2: P_r(tau) = 2 on 0-4 us, 50 ksps')
a, h = 4.0, 2.0
area = h * a
mu, e2 = a / 2, a * a / 3
var = e2 - mu * mu
sg = sqrt(var)
print(f'area = 2x4 = {area:g} (height cancels) ; mu = a/2 = {mu:g} us ; E[tau^2] = 16/3 = {e2:.4f} ; var = {var:.4f} ; sigma = {sg:.4f} us (4/sqrt12)')
Ts = 1 / 50e3
print(f'Ts = {Ts*1e6:g} us ; sigma/Ts = {sg*1e-6/Ts:.4f} ; Rs max = 0.1/sigma = {0.1/(sg*1e-6)/1e3:.2f} ksps')
print(f'B_C ~ 1/sigma = {1/(sg*1e-6)/1e3:.1f} kHz ; Bs/B_C ~ {50e3*sg*1e-6:.4f} (= sigma/Ts)')
shown(f'{e2:.3f}', f'{var:.3f}', f'{sg:.3f}', f'{sg*1e-6/Ts:.4f}', f'{0.1/(sg*1e-6)/1e3:.1f}', f'{1/(sg*1e-6)/1e3:.0f}')

head('t8 example 3: B_C = 150 kHz given')
Bc = 150e3
print(f'(a) Rs = 10 ksps -> Bs ~ 10 kHz ; Bs/Bc = 10/150 = {10e3/Bc:.4f} ; Bc/Bs = {Bc/10e3:g}')
print(f'(b) Rs = 1 Msps -> Bs ~ 1 MHz ; Bs/Bc = {1e6/Bc:.4f}')
print(f'(c) Bs < Bc -> Rs < {Bc/1e3:g} ksps (upper limit)')
shown(f'{10e3/Bc:.4f}', f'{1e6/Bc:.2f}')

head('t8 traps')
print(f'4-QAM 200 kbit/s -> Rs = 200/log2(4) = {200/2:g} ksps')

# ======================================================================= t9
head('t9 table 1, 2023-24 Q1(a)(iii): time-invariant channel, Ts 1 ms, sigma 0.01 ms')
print('f_m = 0 (no Doppler) ; Tc -> infinity ; sigma/Ts = 0.01 -> flat, slow')

head('t9 table 1, focused Q3(e)(f): 10 ksps, 2 GHz, sigma 2 us, 54 km/h')
Rs, fc, sg, kmh = 10e3, 2e9, 2e-6, 54
Ts = 1 / Rs
v = kmh / 3.6
fm = v * fc / C
Tc = 1 / fm
print(f'Ts = {Ts*1e6:g} us ; sigma/Ts = 2/100 = {sg/Ts:.2f}')
print(f'v = 54/3.6 = {v:g} m/s ; f_m = 15 x 2e9 / 3e8 = {fm:.0f} Hz ; Tc = {Tc*1e3:.0f} ms ; Tc/Ts = {Tc/Ts:.0f} ; '
      f'Bs ~ {Rs/1e3:g} kHz ; Bs/B_D = {Rs/fm:.0f}')
print(f'(trap) 54 km/h used as 54 m/s: f_m = {54*fc/C:.0f} Hz (x{(54*fc/C)/fm:.1f}) ; 72 km/h = {72/3.6:g} m/s')

head('t9 example 1: 360 km/h, lambda 5 cm, 1 ksps, sigma 1 us')
v = 360 / 3.6
lam = 0.05
fm = v / lam
Tc = 1 / fm
Ts = 1 / 1e3
print(f'v = {v:g} m/s ; lambda = {lam:g} m ; f_m = v/lambda = {fm:.0f} Hz ; f_c = c/lambda = {C/lam/1e9:g} GHz ; '
      f'v f_c/c = {v*(C/lam)/C:.0f} Hz')
print(f'Tc = {Tc*1e3:g} ms ; Ts = {Ts*1e3:g} ms ; Ts/Tc = {Ts/Tc:g} ; sigma/Ts = {1e-6/Ts:g} ; '
      f'Bs ~ {1e3/1e3:g} kHz vs B_D = {fm/1e3:g} kHz')

head('t9 example 2: Tc 5 ms measured at 900 MHz, then 100 ksps')
Tc, fc = 5e-3, 900e6
fm = 1 / Tc
lam = C / fc
v = fm * C / fc
print(f'f_m = 1/Tc = {fm:.0f} Hz ; lambda = {lam:.4f} m ; v = f_m c/f_c = f_m lambda = {v:.2f} m/s = {v*3.6:.0f} km/h')
Ts = 1 / 100e3
print(f'Ts = {Ts*1e6:g} us ; Tc/Ts = {Tc/Ts:.0f}')

head('t9 example 3: same channel sigma 2 us, f_m 500 Hz; three symbol rates')
sg, fm = 2e-6, 500
Tc = 1 / fm
print(f'Tc = {Tc*1e3:g} ms')
for Rs in (250, 20e3, 5e6):
    Ts = 1 / Rs
    print(f'Rs = {Rs:g} sps: Ts = {Ts*1e6:g} us = {Ts*1e3:g} ms ; sigma/Ts = {sg/Ts:g} ; Ts/Tc = {Ts/Tc:g} ; Tc/Ts = {Tc/Ts:g}')
