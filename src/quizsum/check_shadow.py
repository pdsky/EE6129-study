#!/usr/bin/python3
"""Numbers for frag_shadow.html (topic t5: log-normal shadowing outage, inverse Q lookup,
maximum distance / allowed sigma, macro-diversity). Stdlib only; run with /usr/bin/python3.
Every number printed in the fragment is printed here with a label.

Q(x)  = right-tail area of N(0,1) = 1 - Phi(x)      (statistics.NormalDist)
Qinv  = x such that Q(x) = p
Table lookups are done the way a student does it: round the argument to 2 decimals first.
"""
from math import log10, sqrt, exp, pi
from statistics import NormalDist

N = NormalDist()
Q = lambda x: N.cdf(-x)
Phi = N.cdf
Qinv = lambda p: -N.inv_cdf(p)
dBm = lambda mw: 10 * log10(mw)
mW = lambda dbm: 10 ** (dbm / 10)
r2 = lambda x: round(x + 1e-12, 2)          # argument rounded for the Q table


def interp(x0, p):
    """Inverse lookup the way it is done on paper: linear interpolation between table rows x0 and x0 + 0.01."""
    q0, q1 = Q(round(x0, 2)), Q(round(x0 + 0.01, 2))
    return x0 + 0.01 * (q0 - p) / (q0 - q1)


def sec(t):
    print(f'\n=== {t}')


# ------------------------------------------------------------------ formula cards
sec('[F] formula cards')
print(f'100 mW = {dBm(100):.2f} dBm ; 2 W = 2000 mW = {dBm(2000):.2f} dBm ; 1 W = {dBm(1000):.2f} dBm')
for x in (0, 1, 1.282, 1.645, 2, 2.326, 3.09):
    print(f'Q({x}) = {Q(x):.4f}')
for p in (0.1, 0.05, 0.01, 0.001):
    print(f'Qinv({p}) = {Qinv(p):.4f}')
print(f'Phi(1) = {Phi(1):.4f} = 1 - Q(1) = {1 - Q(1):.4f}')
print(f'lecture p.16: P_out < 1% -> M >= {Qinv(0.01):.3f} sigma (slide writes 2.33)')

# ------------------------------------------------------------------ table A (forward)
sec('[TA] forward: Practice 1 Q2(a)')
mu, Pmin, s = 15, 10, 8
M = mu - Pmin
print(f'M = {mu} - {Pmin} = {M} dB ; M/sigma = {M}/{s} = {M/s:.3f}')
print(f'Q(0.625) = {Q(0.625):.4f} ; table Q(0.62) = {Q(0.62):.4f} , Q(0.63) = {Q(0.63):.4f}')

sec('[TA] forward: mock A Q2(a)(b)')
Pt = dBm(100); K, g, Pmin, s, d = -31.5, 3.6, -110, 6, 300
pl = 10 * g * log10(d)
Pr = Pt + K - pl
M = Pr - Pmin
print(f'Pt = 10log10(100) = {Pt:.2f} dBm ; 10*gamma = {10*g:.0f} ; 36 log10 300 = {pl:.2f} dB')
print(f'Pr(300) = {Pt:.0f} - 31.5 - {pl:.2f} = {Pr:.2f} dBm ; M = {Pr:.2f} - ({Pmin}) = {M:.2f} dB')
print(f'M/sigma = {M:.2f}/{s} = {M/s:.3f} -> table arg {r2(M/s)} ; Q({r2(M/s)}) = {Q(r2(M/s)):.4f} ; unrounded Q({M/s:.4f}) = {Q(M/s):.4f}')
print(f'as shown on the page (rounded operands): 9.32/6 = {9.32/6:.3f} -> {r2(9.32/6)} ; Q({9.32/6:.3f}) = {Q(9.32/6):.4f} '
      f'(table interpolation 0.0606 + 0.333 x (0.0594 - 0.0606) = {0.0606 + (9.32/6 - 1.55)/0.01*(0.0594 - 0.0606):.4f})')

sec('[SRC-A] Practice 1 Q1(b) (least squares on the question data) and lecture p.16 example')
dd = [5, 25, 65, 110, 400, 1000]; MM = [-60, -80, -105, -115, -130, -150]
xs = [10 * log10(v) for v in dd]; n = len(dd)
xb, Mb = sum(xs) / n, sum(MM) / n
gam = -sum((x - xb) * (y - Mb) for x, y in zip(xs, MM)) / sum((x - xb) ** 2 for x in xs)
Kdb = Mb + gam * xb
mse = sum((y - (Kdb - gam * x)) ** 2 for x, y in zip(xs, MM)) / n
sig = sqrt(mse)
print(f'P1Q1 LS: gamma = {gam:.3f} ; K_dB = {Kdb:.2f} dB ; MSE = {mse:.2f} dB^2 ; sigma = {sig:.3f} dB')
print(f'P1Q1(b): 10/sigma = {10/sig:.3f} -> Q({r2(10/sig):.2f}) = {Q(r2(10/sig)):.2e} (unrounded Q({10/sig:.3f}) = {Q(10/sig):.2e}, as on the practice page)')
off = sum((y - (-31.4 - 3.86 * x)) ** 2 for x, y in zip(xs, MM)) / n
print(f'official K=-31.4, gamma=3.86 -> MSE on the data = {off:.1f} (larger than LS {mse:.2f}) ; official Pout 6.19e-4 not reproducible')
Prl = 0 - 26.67 - 10 * 3.97 * log10(150)
Ml = Prl - (-118)
sl = sqrt(3.36)
print(f'lecture p.16: Pr = {Prl:.2f} dBm ; M = {Ml:.2f} dB ; sigma = sqrt(3.36) = {sl:.3f} dB ; M/sigma = {Ml/sl:.3f} -> Q({r2(Ml/sl)}) = {Q(r2(Ml/sl)):.4f}')
print(f'   wrong (divide by variance): {Ml:.2f}/3.36 = {Ml/3.36:.3f} -> Q({r2(Ml/3.36)}) = {Q(r2(Ml/3.36)):.4f} ; ratio = {Q(r2(Ml/3.36))/Q(r2(Ml/sl)):.1f}x')

# ------------------------------------------------------------------ table B (backward)
sec('[TB] backward: 2023-24 S2 Q1(a)(ii)  (margin 10 dB, P_out < 1%, max variance of psi_dB)')
x = Qinv(0.01)
print(f'table: Q(2.32) = {Q(2.32):.4f} , Q(2.33) = {Q(2.33):.4f} ; exact Qinv(0.01) = {x:.4f}')
print(f'with 2.326: sigma < 10/2.326 = {10/2.326:.3f} dB ; sigma^2 < {(10/2.326)**2:.2f} dB^2')
print(f'with 2.33 : sigma < 10/2.33 = {10/2.33:.3f} dB ; sigma^2 < {(10/2.33)**2:.2f} dB^2')
print(f'check: 4.30^2 = {4.30**2:.2f}')

sec('[TB] backward: mock A Q2(c)  (P_out <= 1%, d_max)')
Pt, K, g, Pmin, s = dBm(100), -31.5, 3.6, -110, 6
Mreq = 2.326 * s
Prmin = Pmin + Mreq
rhs = Pt + K - Prmin
print(f'M >= 2.326 x 6 = {Mreq:.2f} dB ; Pr >= -110 + {Mreq:.2f} = {Prmin:.2f} dBm')
print(f'36 log10 d <= 20 - 31.5 + {-Prmin:.2f} = {rhs:.2f} ; log10 d <= {rhs:.2f}/36 = {rhs/36:.3f} ; d <= {10**(rhs/36):.1f} m')
dexact = 10 ** ((Pt + K - Pmin - x * s) / (10 * g))
print(f'closed form d0*10^((Pt+K-Pmin-x*sigma)/(10 gamma)) with exact x = {dexact:.1f} m')

sec('[SRC-B] Practice 1 Q2(b)')
print(f'mu > 10 + 4 x 2.326 = {10 + 4*2.326:.2f} dBm (official 19.32 = 10 + 4 x 2.33 = {10 + 4*2.33:.2f})')

# ------------------------------------------------------------------ table C (macro-diversity)
sec('[TC] macro-diversity: mock C Q1')
W, T, s = -95, -105, 8
D = W - T
p1 = Q(D / s)
p2 = p1 ** 2
xr = Qinv(p2)
print(f'Delta = {W} - ({T}) = {D} dB ; Delta/sigma = {D/s:.2f} ; Q(1.25) = {p1:.4f}')
print(f'p^2 = {p1:.4f}^2 = {p2:.5f} = {p2:.3e}')
print(f'table: Q(2.28) = {Q(2.28):.4f} , Q(2.29) = {Q(2.29):.4f} ; exact Qinv = {xr:.3f} ; '
      f'interpolated between the two table rows = {interp(2.28, p2):.3f}')
print(f'M_eq = 2.29 x 8 = {2.29*s:.2f} dB -> gain = {2.29*s - D:.2f} dB ; exact M_eq = {xr*s:.2f}, gain {xr*s - D:.2f} dB')
print(f'hand arithmetic with the rounded table value: 0.1056^2 = {0.1056**2:.5f} -> {0.1056**2:.3e}')
print(f'page: 0.01115 is midway between the table rows 0.0113 and 0.0110 -> x = 2.28 + 0.01 x {(0.0113 - 0.01115)/(0.0113 - 0.0110):.2f} = '
      f'{2.28 + 0.01*(0.0113 - 0.01115)/(0.0113 - 0.0110):.3f} ; M_eq = 2.285 x 8 = {2.285*s:.2f} ~ {2.285*s:.1f} dB ; '
      f'G = {2.285*s - D:.2f} ~ {2.285*s - D:.1f} dB')
print(f'note: exact x = {xr:.4f} is 2.28 to 2 dp; the practice page reads 2.29 (2.29 x 8 = {2.29*s:.2f}), same 18.3 dB after rounding')

# ------------------------------------------------------------------ worked examples
sec('[E1] 2 W, K -38 dB, gamma 3.2, Pmin -100 dBm, MSE 30.25 dB^2; d = 400 m and 1 km')
Pt = dBm(2000); K, g, Pmin = -38, 3.2, -100
s = sqrt(30.25)
print(f'Pt = 10log10(2000) = {Pt:.2f} dBm ; sigma = sqrt(30.25) = {s:.2f} dB')
for d in (400, 1000):
    pl = 10 * g * log10(d); Pr = Pt + K - pl; M = Pr - Pmin; a = M / s
    print(f'd = {d}: 32 log10 d = {pl:.2f} dB ; Pr = {Pt:.2f} - 38 - {pl:.2f} = {Pr:.2f} dBm ; M = {M:.2f} dB ; '
          f'M/sigma = {a:.4f} -> {r2(a)} ; Q({r2(a)}) = {Q(r2(a)):.4f} (unrounded {Q(a):.4f})')
print(f'negative margin: Q(0.18) = {Q(0.18):.4f} ; Q(-0.18) = 1 - Q(0.18) = {1 - Q(0.18):.4f} ; Phi(0.18) = {Phi(0.18):.4f}')
print(f'hand arithmetic: 11.74/5.5 = {11.74/5.5:.4f} -> {r2(11.74/5.5)} ; Q({r2(11.74/5.5)}) = {Q(r2(11.74/5.5)):.4f} '
      f'(the page follows the shown 11.74; do not round 2.1345 -> 2.135 -> 2.14) ; -0.99/5.5 = {-0.99/5.5:.3f}')

sec('[E2] Pt 100 mW, K -40 dB, gamma 3, Pmin -95 dBm, sigma 6 dB')
Pt, K, g, Pmin, s = dBm(100), -40, 3, -95, 6
x5 = Qinv(0.05)
print(f'(a) table Q(1.64) = {Q(1.64):.4f} , Q(1.65) = {Q(1.65):.4f} ; interpolated {interp(1.64, 0.05):.3f} ; exact Qinv(0.05) = {x5:.4f}')
M = 1.645 * s; Prmin = Pmin + M; rhs = Pt + K - Prmin
print(f'    M >= 1.645 x 6 = {M:.2f} dB ; Pr >= -95 + {M:.2f} = {Prmin:.2f} dBm')
print(f'    30 log10 d <= 20 - 40 + {-Prmin:.2f} = {rhs:.2f} ; log10 d <= {rhs/30:.3f} ; d <= {10**(rhs/30):.1f} m')
pl200 = 10 * g * log10(200)
Ptmin = Prmin - K + pl200
print(f'(b) 30 log10 200 = {pl200:.2f} dB ; Pt >= {Prmin:.2f} + 40 + {pl200:.2f} = {Ptmin:.2f} dBm = {mW(Ptmin):.1f} mW ; '
      f'extra {Ptmin - Pt:.2f} dB ; from the shown 3.90 dB: 10^0.390 = {10**0.390:.4f} ~ x{10**0.390:.2f} (= 245.47/100)')
Pr100 = Pt + K - 10 * g * log10(100); M100 = Pr100 - Pmin; x3 = Qinv(0.001)
print(f'(c) Pr(100) = {Pr100:.2f} dBm ; M = {M100:.2f} dB ; table Q(3.09) = {Q(3.09):.5f} ; exact Qinv(0.001) = {x3:.4f}')
print(f'    sigma <= 15/3.09 = {15/3.09:.3f} dB ; sigma^2 <= {(15/3.09)**2:.2f} dB^2 ; check 4.85^2 = {4.85**2:.2f}')

sec('[E3] macro-diversity: each BS -92 dBm, threshold -104 dBm, sigma 8 dB, independent')
W, T, s = -92, -104, 8
D = W - T; p1 = Q(D / s); p2 = p1 ** 2; xr = Qinv(p2)
print(f'(a) Delta = {D} dB ; Delta/sigma = {D/s} ; Q(1.5) = {p1:.4f}')
print(f'(b) p^2 = {p2:.5f} = {p2:.3e} ; table Q(2.61) = {Q(2.61):.5f} , Q(2.62) = {Q(2.62):.5f} ; interpolated {interp(2.61, p2):.3f} ; exact Qinv = {xr:.4f}')
print(f'    M_eq = 2.615 x 8 = {2.615*s:.2f} dB ; gain = {2.615*s - D:.2f} dB ; exact {xr*s:.2f} / {xr*s - D:.2f}')
x1 = Qinv(0.1)
print(f'(c) sqrt(0.01) = {sqrt(0.01):.2f} ; table Q(1.28) = {Q(1.28):.4f} , Q(1.29) = {Q(1.29):.4f} ; interpolated {interp(1.28, 0.1):.3f} ; exact Qinv(0.1) = {x1:.4f}')
print(f'    per-link Delta >= 1.282 x 8 = {1.282*s:.2f} dB (exact {x1*s:.2f}) ; single BS 2.326 x 8 = {2.326*s:.2f} dB ; '
      f'saving {2.326*s - 1.282*s:.2f} dB')
print(f'hand arithmetic: 0.0668^2 = {0.0668**2:.6f} -> {0.0668**2:.3e}')
print(f'(d) fully correlated: P_out = Q(1.5) = {p1:.4f}')


def corr_out(dn, rho, L=10.0, n=20000):
    """P_out = int phi(u) Q((dn + b u)/a)^2 du, a^2 + b^2 = 1, rho = b^2 (Practice 2 Q2(c), u = y/sigma)."""
    b = sqrt(rho); a = sqrt(1 - rho); h = 2 * L / n; tot = 0.0
    for k in range(n + 1):
        u = -L + k * h; w = 0.5 if k in (0, n) else 1.0
        tot += w * Q((dn + b * u) / a) ** 2 * exp(-u * u / 2) / sqrt(2 * pi)
    return tot * h


print(f'    partially correlated rho = b^2 = 0.5, Delta/sigma = 1.5 (numerical integral): {corr_out(1.5, 0.5):.4f}')
print(f'    sanity: rho -> 0 gives {corr_out(1.5, 1e-9):.5f} (= p^2 {p2:.5f}) ; Delta = sigma, rho = 0.5: {corr_out(1.0, 0.5):.4f} (practice page 0.0625)')

# ------------------------------------------------------------------ exam English line
sec('[EN] exam English (mock A numbers + 2023-24 numbers)')
PrA = dBm(100) - 31.5 - 36 * log10(300)
print(f'Pr = {PrA:.2f} dBm, M = {PrA + 110:.2f} dB, Q({r2((PrA + 110) / 6)}) = {Q(r2((PrA + 110) / 6)):.4f} ; '
      f'sigma < 10/2.326 = {10/2.326:.2f} dB ; sigma^2 < {(10/2.326)**2:.1f} dB^2')

# ------------------------------------------------------------------ rounded values as displayed
sec('[DISPLAY] rounded values exactly as they appear in the fragment')
print(f'given: gamma (mock A) = 3.6 ; 10 log10 2 = {10*log10(2):.2f} (2 W = {dBm(2000):.2f} dBm, not 3.01)')
print(f'TA  P1Q2(a): Q(0.625) = {Q(0.625):.3f} = {100*Q(0.625):.1f}%')
print(f'SRC P1Q1: K = {Kdb:.1f} dB ; gamma = {gam:.2f} ; sigma = {sig:.2f} dB ; Q({10/sig:.2f}) = {Q(r2(10/sig)):.2e} ; '
      f'practice page Q({10/sig:.3f}) = {Q(10/sig):.2e}')
print(f'SRC p.16 wrong: Q(1.47) = {Q(1.47):.3f}')
print(f'TB  2.33 variant: sigma < {10/2.33:.2f} dB ; sigma^2 < {(10/2.33)**2:.1f} dB^2 ; P1Q2(b) mu > {10 + 4*2.326:.1f} dBm')
pC = Q(10 / 8) ** 2
print(f'TC  mock C: 0.1056^2 = {0.1056**2:.5f} ~ {0.1056**2:.4f} = {0.1056**2*100:.2f}e-2 ; exact p^2 = {pC:.4f} ; '
      f'M_eq = 2.285 x 8 = {2.285*8:.2f} ~ {2.285*8:.1f} dB ; G = {2.285*8 - 10:.1f} dB ; practice page 2.29 x 8 = {2.29*8:.2f}')
print(f'TA  mock A shown: 9.32/6 = {9.32/6:.3f} ; Q(1.553) = {Q(9.32/6):.4f}')
print(f'E1  (a) shown chain 11.74/5.5 = {11.74/5.5:.4f} -> 2.13 ; Q(2.13) = {Q(2.13):.4f} = {100*Q(2.13):.1f}% ; '
      f'unrounded Q = {Q((dBm(2000) - 38 - 32*log10(400) + 100)/5.5):.4f} ; (b) 1 - Q(0.18) = {1 - Q(0.18):.3f} = {100*(1 - Q(0.18)):.0f}%')
print(f'E2  (b) exponent 23.90/10 = {23.90/10:.3f} -> 10^2.390 = {10**2.390:.1f} mW ; 10^0.390 = {10**0.390:.2f} ; '
      f'(c) sigma^2 <= {(15/3.09)**2:.1f} dB^2 , sigma <= {15/3.09:.2f} dB')
print(f'TRAP rounding: 2.1345 -> {round(2.1345 + 1e-12, 2):.2f} (double rounding 2.1345 -> 2.135 -> 2.14 is wrong)')
pE = Q(1.5) ** 2
print(f'E3  (b) p^2 = {pE*1e3:.2f}e-3 ; M_eq = {2.615*8:.1f} dB ; G = {2.615*8 - 12:.1f} dB')
