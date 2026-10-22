#!/usr/bin/python3
"""Numbers used in frag_rayleigh.html: t6 Rayleigh outage / fade margin, t7 Rician K-factor.

stdlib only (math, statistics.NormalDist). Every number printed in the fragment comes from here.
Run: /usr/bin/python3 check_rayleigh.py
"""
from math import log10, log, exp, sqrt
from statistics import NormalDist

ND = NormalDist()
Q = lambda x: 1 - ND.cdf(x)
Qinv = lambda p: ND.inv_cdf(1 - p)
lin = lambda db: 10 ** (db / 10)
dB = lambda x: 10 * log10(x)
ray = lambda g0, gb: 1 - exp(-g0 / gb)            # Rayleigh outage, linear inputs
L = lambda e: log(1 / (1 - e))                    # ln(1/(1-eps))
FM = lambda e: dB(1 / L(e))                       # Rayleigh fade margin in dB


def I0(x):
    s = t = 1.0
    k = 1
    while t > 1e-17 * s:
        t *= (x / 2) ** 2 / (k * k)
        s += t
        k += 1
    return s


def rice_cdf(x, K, n=40000):
    """P(gamma < x*gbar) for Rician fading with factor K (x = gamma0/gbar); trapezoid rule on the SNR pdf
    p(u) = (1+K) e^{-K-(1+K)u} I0(2 sqrt(K(1+K)u)), u = gamma/gbar.  Beyond the slides; reference only."""
    h = x / n
    tot = 0.0
    for i in range(n + 1):
        u = i * h
        w = 0.5 if i in (0, n) else 1.0
        tot += w * (1 + K) * exp(-K - (1 + K) * u) * I0(2 * sqrt(K * (1 + K) * u))
    return tot * h


print('================ t6  Rayleigh fading: outage and fade margin')
print('-- formula cards')
for e in (0.10, 0.05, 0.02, 0.01, 0.005, 0.001):
    print(f'  FM eps={e:<6}: ln(1/(1-eps)) = {L(e):.6f} ; exact FM = {FM(e):.2f} dB ; approx 10log10(1/eps) = {dB(1/e):.2f} dB')
for x in (0.05012, 0.1, 0.5):
    ex = 1 - exp(-x)
    print(f'  1-e^-x, x={x}: exact {ex:.4f} ; approx x = {x} ; approx too high by {(x-ex)/ex*100:.1f}%')
print(f'  P(gamma > gbar) = e^-1 = {exp(-1):.4f} ; P(gamma < gbar) = 1-e^-1 = {1-exp(-1):.4f} = {(1-exp(-1))*100:.1f}%')
print(f'  dB rule: 10 dB below mean -> x = {lin(-10):.2f} -> {ray(lin(-10),1):.4f} ; 20 dB -> {ray(lin(-20),1):.5f} ; 30 dB -> {ray(lin(-30),1):.6f}')
print(f'  envelope threshold rho = 0.1 (Practice 2 Q1): rho^2 = {0.1**2:.2f} ; 1-e^-rho^2 = {1-exp(-0.01):.5f} ; power {dB(0.01):.0f} dB below rms')

print('-- table A (forward): final 2024-25 Q1(b)(i) first step | mock B.Q1(a) ; focused Q3(c) in the source line')
gb, g0 = lin(20), lin(7)
x = g0 / gb
print(f'  mock B.Q1(a): gbar 20 dB = 10^2 = {gb:.0f} ; g0 7 dB = 10^0.7 = {g0:.3f} ; Pout = {ray(g0, gb)*100:.2f}% ; x = {x:.5f} ; Pout = 1-e^-x = {ray(g0, gb):.4f} ; approx x = {x:.4f} (+{(x-ray(g0,gb))/ray(g0,gb)*100:.1f}%)')
Pr = 30 + (-40) - 10 * 3 * log10(1000)
gb2, g02 = lin(Pr - (-120)), lin(10)
x2 = g02 / gb2
print(f'  focused Q3(c): Pout = {ray(g02, gb2)*100:.2f}% ; Pr = 30-40-90 = {Pr:.0f} dBm ; gbar = {Pr+120:.0f} dB = {gb2:.0f} ; g0 10 dB = {g02:.0f} ; x = {x2:.3f} ; Pout = {ray(g02, gb2):.4f} ; approx {x2:.3f} (+{(x2-ray(g02,gb2))/ray(g02,gb2)*100:.1f}%)')
print(f'  final 2024-25 Q1(b)(i) (Ch4) single branch: 1-e^-(4.5/30) = 1-e^-{4.5/30:.2f} = {ray(4.5, 30):.4f}')
gb_ = 3.0 ** 2 / 2
print(f'    threshold from BER: Q(3.0) = {Q(3.0):.3e} (paper 1.35e-3) -> sqrt(2 gb) = 3.0 -> gb = {gb_} ; x = {gb_}/30 = {gb_/30:.2f}'
      f' ; Pout = {ray(gb_, 30):.3f} = {ray(gb_, 30)*100:.1f}% ; approx x too high by {(gb_/30-ray(gb_,30))/ray(gb_,30)*100:.1f}%'
      f' ; (Ch4 rest) M = ln0.02/ln{ray(gb_,30):.3f} = {log(0.02)/log(ray(gb_,30)):.2f} -> M = 2')

print('-- table B (backward): final 2025-26 S2 Q1(a)(iii) | mock B.Q1(b)')
gR, e = lin(25), 0.005
gmin = gR * L(e)
print(f'  2025-26 S2: gbar_R 25 dB = 10^2.5 = {gR:.1f} ; ln(1/0.995) = {L(e):.6f} ; gmin = {gR:.1f} x {L(e):.6f} = {gmin:.4f} = {dB(gmin):.2f} dB ; FM = 25 - {dB(gmin):.2f} = {25-dB(gmin):.2f} dB ; formula {FM(e):.2f} dB')
g0, e = lin(7), 0.01
gneed = g0 / L(e)
print(f'  mock B.Q1(b): g0 7 dB = {g0:.3f} ; ln(1/0.99) = {L(e):.6f} ; gbar = {g0:.3f} / {L(e):.5f} = {gneed:.1f} = {dB(gneed):.2f} dB ; FM = {dB(gneed):.2f} - 7 = {dB(gneed)-7:.2f} dB ; formula {FM(e):.2f} dB')
print(f'  check: Pout at gbar {gneed:.1f}: {ray(g0, gneed):.4f}')
print(f'  final 2023-24 Q1(a)(iv): ln(1/0.999) = {L(0.001):.7f} ; FM = 10log10(1/{L(0.001):.7f}) = {FM(0.001):.2f} dB')

print('-- t6 example 1: dBm -> gbar, forward outage, complement')
gbdB = -92 - (-110)
gb, g0 = lin(gbdB), lin(6)
x = g0 / gb
print(f'  gbar = -92-(-110) = {gbdB} dB = 10^1.8 = {gb:.2f} ; g0 6 dB = 10^0.6 = {g0:.3f} ; Pout = {ray(g0, gb)*100:.2f}% ; x = {x:.5f} (= 10^-1.2 = {lin(-12):.5f}, threshold {gbdB-6} dB below mean)')
print(f'  Pout = 1-e^-{x:.5f} = {ray(g0, gb):.6f} (3 s.f. {ray(g0, gb):.3g}) ; approx x = {x:.4f}')
xb = lin(gbdB + 3)
print(f'  (b) 21 dB = {xb:.1f} ; ratio {xb:.1f}/{gb:.2f} = {xb/gb:.3f} (= 10^0.3 = {lin(3):.3f}) ; P(gamma>21 dB) = e^-{xb/gb:.3f} = {exp(-xb/gb):.4f}')

print('-- t6 example 2: eps 2 %, threshold 8 dB -> gbar, FM, max distance')
g0, e = lin(8), 0.02
gneed = g0 / L(e)
print(f'  g0 8 dB = 10^0.8 = {g0:.3f} ; ln(1/0.98) = {L(e):.6f} ; gbar = {g0:.3f}/{L(e):.6f} = {gneed:.1f} = {dB(gneed):.2f} dB')
print(f'  FM = {dB(gneed):.2f} - 8 = {dB(gneed)-8:.2f} dB ; formula {FM(e):.2f} dB ; approx 10log10(50) = {dB(50):.2f} dB')
Pt, Kdb, gam, Nn = dB(1000), -40, 3.5, -115
print(f'  Pt = 1 W = 1000 mW = {Pt:.0f} dBm ; K_dB = {Kdb} dB ; gamma = {gam} ; N = {Nn} dBm')
Prmin = Nn + dB(gneed)
rhs = Pt + Kdb - Prmin
logd = rhs / (10 * gam)
print(f'  Pr,min = {Nn} + {dB(gneed):.2f} = {Prmin:.2f} dBm ; 30 - 40 - 35log10 d >= {Prmin:.2f} -> 35 log10 d <= {rhs:.2f} -> log10 d <= {logd:.4f} -> d <= {10**logd:.1f} m')
print(f'  check at d = 193 m: Pr = {Pt+Kdb-35*log10(193):.2f} dBm, SNR = {Pt+Kdb-35*log10(193)-Nn:.2f} dB, Pout = {ray(g0, lin(Pt+Kdb-35*log10(193)-Nn)):.4f}')

print('-- t6 example 3: same margin, shadowing vs Rayleigh')
M, s = 15, 6
print(f'  shadowing: Q({M}/{s}) = Q({M/s:.2f}) = {Q(M/s):.5f}')
xr = lin(-M)
print(f'  Rayleigh: g0/gbar = 10^-1.5 = {xr:.5f} ; Pout = {ray(xr, 1):.5f} ; ratio Rayleigh/shadow = {ray(xr,1)/Q(M/s):.2f} ; as % : Rayleigh {ray(xr,1)*100:.2f}% vs shadow {Q(2.5)*100:.3f}%')
print(f'  focused Q3: margin 10 dB, sigma 8 dB: shadowing Q(1.25) = {Q(1.25):.4f} ; Rayleigh 1-e^-0.1 = {ray(0.1,1):.4f}')
print('  same margin, sigma 8 dB, for orientation:')
for M in (10, 15, 20):
    print(f'    margin {M} dB: shadow Q({M/8:.3f}) = {Q(M/8):.5f} ; Rayleigh {ray(lin(-M),1):.5f}')

print('-- t6 traps')
print('  lecturer example (Ch3): 8.5 dB -> 10^0.85 = %.3f' % lin(8.5))
print(f'  dB put into exponent: 1-e^-(7/20) = {1-exp(-0.35):.3f} (correct {ray(lin(7), lin(20)):.4f})')
print(f'  log10 instead of ln, eps 1%: log10(1/0.99) = {log10(1/0.99):.6f} -> {dB(1/log10(1/0.99)):.2f} dB (correct {FM(0.01):.2f} dB)')
print(f'  linear subtraction: {lin(7)/L(0.01):.1f} - {lin(7):.3f} = {lin(7)/L(0.01)-lin(7):.1f} (meaningless)')
print(f'  rho not squared, rho = 0.1: wrong 1-e^-0.1 = {1-exp(-0.1):.4f} ; right 1-e^-0.01 = {1-exp(-0.01):.5f}')

print()
print('================ t7  Rician fading and K-factor')
K = 4.0
print(f'-- focused Q3(d): K = 4 -> {dB(K):.2f} dB ; direct share K/(K+1) = {K/(K+1)*100:.0f}% ; scattered {1/(K+1)*100:.0f}%')
x = 0.1
for Kk in (0, 1, 4, 10):
    print(f'   Rician outage (beyond slides) gbar 20 dB, g0 10 dB, K = {Kk:>2} ({"-inf" if Kk == 0 else f"{dB(Kk):.1f}"} dB): {rice_cdf(x, Kk):.5f}')
Kp = lin(6)
print(f'-- slide p.28 curve K = 6 dB: K = 10^0.6 = {Kp:.3f} ; K+1 = {Kp+1:.3f} ; direct share {Kp:.3f}/{Kp+1:.3f} = {Kp/(Kp+1)*100:.1f}% ; scattered {1/(Kp+1)*100:.1f}%')
print(f'-- Rician pdf with s = 0: I0(0) = {I0(0):.0f} -> Rayleigh')

print('-- t7 example 1: direct -80 dBm, scattered -90, -92, -95 dBm')
d = lin(-80)
sc = [lin(v) for v in (-90, -92, -95)]
S = sum(sc)
Kx = d / S
print(f'  direct = {d:.3e} mW ; scattered = {[f"{v:.3e}" for v in sc]} mW ; sum = {S:.3e} mW = {dB(S):.2f} dBm')
print(f'  K = {d:.3e}/{S:.3e} = {Kx:.3f} ; K_dB = {dB(Kx):.2f} dB (= -80 - ({dB(S):.2f})) ; K+1 = {Kx+1:.3f} ; direct share {Kx:.3f}/{Kx+1:.3f} = {Kx/(Kx+1)*100:.1f}%')
print(f'  wrong: strongest scattered path only -> K_dB = -80 - (-90) = {-80-(-90)} dB (correct {dB(Kx):.2f} dB)')

print('-- t7 example 2: K_dB = -3 dB ; LOS blocked (K 10 dB -> 0)')
Km = lin(-3)
print(f'  K = 10^-0.3 = {Km:.4f} ; K+1 = {Km+1:.4f} ; direct share {Km:.4f}/{Km+1:.4f} = {Km/(Km+1)*100:.1f}% ; scattered {1/(Km+1)*100:.1f}%')
print(f'  K = 10 dB -> K = {lin(10):.0f} ; outage (gbar 20 dB, g0 10 dB): K=10 {rice_cdf(x, 10):.2e} = {rice_cdf(x,10)*100:.3f}% ; K=1 (0 dB) {rice_cdf(x,1)*100:.2f}% ; K=4 {rice_cdf(x,4)*100:.2f}% ; K=0 {rice_cdf(x, 0):.4f} = {ray(0.1,1)*100:.2f}% ; ratio K0/K10 {ray(0.1,1)/rice_cdf(x,10):.0f}')

print('-- why the K-trend claim is qualified "threshold below the mean": outage vs K = 0, 1, 4, 10, 30')
for xx in (0.1, 0.5, 0.9, 1.5):
    vals = [rice_cdf(xx, Kk, n=8000) for Kk in (0, 1, 4, 10, 30)]
    mono = all(a > b for a, b in zip(vals, vals[1:]))
    print(f'  gamma0/gbar = {xx}: ' + ' '.join(f'{v:.4f}' for v in vals) + ('  decreasing in K' if mono else '  NOT decreasing (threshold above mean)'))

print('-- t7 traps')
print(f'  20log10(4) = {20*log10(4):.2f} dB (wrong) vs 10log10(4) = {dB(4):.2f} dB')
print(f'  amplitude ratio 2 -> K = 2^2 = 4 = {dB(4):.2f} dB ; not 2 = {dB(2):.2f} dB')
print(f'  K = 0 dB -> K = {lin(0):.0f} -> direct {lin(0)/(lin(0)+1)*100:.0f}% / scattered {1/(lin(0)+1)*100:.0f}%')
