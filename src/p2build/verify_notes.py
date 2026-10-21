#!/usr/bin/python3
"""Numbers used in the extra_notes.py boxes (outage decision table, fade margin, dB line,
least squares, water-filling). Run to re-check."""
from math import log10, log2, sqrt, exp, erfc, pi, log
from statistics import NormalDist

Q = lambda x: 0.5 * erfc(x / sqrt(2))
Qinv = lambda p: NormalDist().inv_cdf(1 - p)
lin = lambda db: 10 ** (db / 10)
dB = lambda x: 10 * log10(x)

print('1 path loss only: Pt 20 dBm, K -31.5 dB, gamma 3.6, threshold -110 dBm')
Pr = 20 - 31.5 - 36 * log10(300)
print(f'  Pr(300 m) = {Pr:.2f} dBm ; max d with Pr >= -110: {10**((20-31.5+110)/36):.1f} m')
print('2 shadowing (P1 Q2 a): mean 15 dBm, threshold 10 dBm, sigma 8 dB')
print(f'  Q({5/8:.3f}) = {Q(5/8):.4f}')
print('3 Rayleigh: gbar 20 dB, g0 10 dB')
print(f'  1 - e^-0.1 = {1-exp(-0.1):.4f}')
print('4 macro-diversity independent, Delta = sigma')
print(f'  single Q(1) = {Q(1):.4f} ; both = {Q(1)**2:.4f}')
print('5 correlated rho = b^2 = 0.5, Delta = sigma (numerical integral)')
a = b = sqrt(0.5); n = 20000; L = 10; h = 2 * L / n
I = sum((0.5 if k in (0, n) else 1) * Q((1 + b * (-L + k * h)) / a) ** 2 * exp(-(-L + k * h) ** 2 / 2) / sqrt(2 * pi) for k in range(n + 1)) * h
print(f'  Pout = {I:.4f}')
print('6 discrete SNR: 4 dB p0.2, 8 dB p0.5, 12 dB p0.3, threshold 6 dB')
vals = [(lin(4), .2), (lin(8), .5), (lin(12), .3)]
m = sum(v * p for v, p in vals)
print(f'  lin = {[round(v,2) for v,_ in vals]} ; Pout = 0.2 ; E[gamma] = {m:.3f} = {dB(m):.2f} dB ; DPSK avg Ps = {sum(0.5*exp(-v)*p for v,p in vals):.3e}')
print('7 rho / LCR / AFD: fm 50 Hz, threshold 10 dB below rms power')
rho = sqrt(0.1); lcr = sqrt(2 * pi) * 50 * rho * exp(-0.1); frac = 1 - exp(-0.1)
print(f'  rho = {rho:.4f} ; fraction below = {frac:.4f} ; LCR = {lcr:.2f}/s ; AFD = {frac/lcr*1e3:.3f} ms')
print('8 Rician K = 6 dB')
print(f'  K linear = {lin(6):.2f}')
print('9 BER-defined outage: BPSK Pb = Q(sqrt(2g)) <= 1e-3, Rayleigh gbar 20 dB')
x = Qinv(1e-3); g0 = x * x / 2
print(f'  Q^-1(1e-3) = {x:.3f} ; g0 = {g0:.3f} = {dB(g0):.2f} dB ; Pout = 1 - e^-(g0/100) = {1-exp(-g0/100):.4f}')
print('10 selection diversity, same g0/gbar')
p1 = 1 - exp(-g0 / 100)
print(f'  M=1 {p1:.4f} ; M=2 {p1**2:.3e} ; M=3 {p1**3:.3e}')
print('fade margin: eps 1%, 0.5%, 0.1%, 10% ; g0 7 dB')
for e in (0.01, 0.005, 0.001, 0.1):
    print(f'  eps {e}: FM exact {dB(1/log(1/(1-e))):.2f} dB ; approx {dB(1/e):.2f} dB')
print(f'  gbar needed for eps 1% = {7+dB(1/log(1/0.99)):.2f} dB')
print('dB line check (mock B.Q2): K -37.01, gamma 3.366, d 100 m')
print(f'  M = {-37.01 - 3.366*20:.2f} dB (measured -105)')
print('water-filling P5 Q1: 80, 40, 40, B 10 MHz')
g = [80, 40, 40]; g0w = 3 / (1 + sum(1 / v for v in g))
print(f'  g0 = {g0w:.3f} ; P/P = {[round(1/g0w-1/v,3) for v in g]} ; C = {10*sum(log2(v/g0w) for v in g):.2f} Mbps')
print('water-filling mock B.Q3: 20, 0.5')
print(f'  both: g0 = {2/(1+1/20+2):.4f} ; one: g0 = {1/1.05:.4f} ; C = {log2(21):.3f} ; equal split {log2(11)+log2(1.25):.3f}')
print('shadowing vs Rayleigh at 8 dB margin (mock B.Q2 c)')
print(f'  shadowing sigma 3.347: Q({8/3.347:.3f}) = {Q(8/3.347):.4f} ; Rayleigh: 1 - e^-{lin(-8):.4f} = {1-exp(-lin(-8)):.4f}')
