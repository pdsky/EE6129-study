#!/usr/bin/python3
"""Numbers for frag_pathloss.html: t3 simplified path loss model, t4 least-squares fit of K, gamma and sigma^2.

Every number printed in the fragment (steps tables and worked examples) is printed here, labelled.
Sources of the table numbers: exams/data_2425.py (Q1(a)(i)), exams/data_2324.py (Q1(a)(i)),
p2build/prac_8.html (mock A.Q2 = p8q2, mock B.Q2 = p8q5, focused Q1 = p8q10), p2build/prac_1.html (P1 Q1).
Run: /usr/bin/python3 check_pathloss.py   (stdlib only)
"""
from math import log10, sqrt, pi
from statistics import NormalDist

ND = NormalDist()
Q = lambda x: 1 - ND.cdf(x)
Qinv = lambda p: ND.inv_cdf(1 - p)
dB = lambda v: 10 * log10(v)
C = 3e8


def fit(d, M, d0=1.0):
    """Least squares for M = K_dB - gamma * x, x = 10 log10(d/d0)."""
    x = [10 * log10(t / d0) for t in d]
    n = len(x)
    xb, Mb = sum(x) / n, sum(M) / n
    Sxy = sum((a - xb) * (b - Mb) for a, b in zip(x, M))
    Sxx = sum((a - xb) ** 2 for a in x)
    g = -Sxy / Sxx
    K = Mb + g * xb
    pred = [K - g * a for a in x]
    res = [b - p for b, p in zip(M, pred)]
    sse = sum(r * r for r in res)
    return dict(x=x, n=n, xb=xb, Mb=Mb, Sxy=Sxy, Sxx=Sxx, g=g, K=K, pred=pred, res=res, sse=sse, mse=sse / n)


def show(label, f, M):
    print(f'  {label}: x =', [round(v, 2) for v in f['x']], f'xbar = {f["xb"]:.4f} Mbar = {f["Mb"]:.4f}')
    print('    x-xbar =', [round(v - f['xb'], 2) for v in f['x']], 'M-Mbar =', [round(v - f['Mb'], 2) for v in M])
    print('    (x-xbar)(M-Mbar) =', [round((a - f['xb']) * (b - f['Mb']), 2) for a, b in zip(f['x'], M)],
          '(x-xbar)^2 =', [round((a - f['xb']) ** 2, 2) for a in f['x']])
    print(f'    Sxy = {f["Sxy"]:.3f} Sxx = {f["Sxx"]:.3f} slope = {-f["g"]:.4f} gamma = {f["g"]:.4f} K_dB = {f["K"]:.3f}')
    print('    gamma*x =', [round(f['g'] * a, 2) for a in f['x']])
    print('    pred =', [round(p, 2) for p in f['pred']], 'res =', [round(r, 2) for r in f['res']],
          'res^2 =', [round(r * r, 2) for r in f['res']], f'sum res = {sum(f["res"]):.1e}')
    print(f'    SSE = {f["sse"]:.3f} MSE = {f["mse"]:.4f} sigma = {sqrt(f["mse"]):.4f}')


print('=' * 70)
print('T3 TABLE 1  forward Pr / backward distance')
print('-- 2024-25 Q1(a)(i): Pr = Pt K d^-3.5, K_dB = -30 dB, A to axis drop 88 dB')
g = 3.5
B = 88 / (10 * g)
print(f'  10*gamma = {10*g:.0f} ; A = K_dB = -30 dB ; B = 88/{10*g:.0f} = {B:.4f} ; d = 10^B = {10**B:.1f} m')
print('-- mock A.Q2 (p8q2): Pt 100 mW, K_dB -31.5, gamma 3.6, Pmin -110 dBm, sigma 6 dB')
Pt = dB(100)
L300 = 36 * log10(300)
Pr300 = Pt - 31.5 - L300
print(f'  Pt = 10log10(100) = {Pt:.2f} dBm ; log10(300) = {log10(300):.4f} ; 36 log10 300 = {L300:.2f} dB ; Pr(300) = {Pr300:.2f} dBm')
x01 = Qinv(0.01)
need = -110 + 2.326 * 6
allow = Pt - 31.5 - need
print(f'  Q^-1(0.01) = {x01:.4f} (table 2.326) ; margin 2.326*6 = {2.326*6:.3f} dB ; need Pr >= {need:.2f} dBm')
print(f'  36 log10 d <= {allow:.2f} ; log10 d <= {allow/36:.4f} ; dmax = {10**(allow/36):.1f} m')

print('=' * 70)
print('T3 TABLE 2  dB form + sketch')
print('-- mock B.Q2 (p8q5) fit used to draw the line')
dB2 = [10, 20, 50, 100]; MB2 = [-68, -86, -91, -105]
fB = fit(dB2, MB2)
print(f'  K_dB = {fB["K"]:.3f} ; gamma = {fB["g"]:.4f} ; slope = {-fB["g"]:.4f}')
x100 = 10 * log10(100)
p100 = fB['K'] - fB['g'] * x100
print(f'  d = 100 m: x = {x100:.0f} ; line value = {p100:.2f} dB ; measured -105 ; residual = {-105 - p100:.2f} dB')

print('=' * 70)
print('T3 EXAMPLES')
print('-- ex1: Pt 4 W, K = 5e-4 (linear), gamma 3, d 200 m, d0 1 m ; then d = 400 m')
Pt1 = dB(4000); K1 = dB(5e-4); L1 = 30 * log10(200); Pr1 = Pt1 + K1 - L1
lin1 = 4 * 5e-4 * (1 / 200) ** 3
print(f'  Pt = 10log10(4000 mW) = {Pt1:.2f} dBm ; K_dB = 10log10(5e-4) = {K1:.2f} dB ; log10 200 = {log10(200):.5f} ; 30 log10 200 = {L1:.2f} dB')
print(f'  Pr = {Pt1:.2f} {K1:+.2f} - {L1:.2f} = {Pr1:.2f} dBm')
print(f'  linear: 4 * 5e-4 = {4*5e-4:.1e} ; (1/200)^3 = {(1/200)**3:.3e} ; Pr = {lin1:.3e} W = {lin1*1e3:.3e} mW -> {dB(lin1*1e3):.2f} dBm')
drop = 30 * log10(2)
lin1b = lin1 / 8
print(f'  d doubled: drop 30 log10 2 = {drop:.2f} dB ; factor 2^3 = 8 ; Pr(400) = {Pr1-drop:.2f} dBm = {lin1b:.4e} W -> {dB(lin1b*1e3):.2f} dBm')
print('-- ex2: Pt 1 W, K_dB -50 dB at d0 = 10 m, gamma 4, Pmin -100 dBm')
Pt2 = dB(1000)
allow2 = Pt2 - 50 + 100
print(f'  Pt = {Pt2:.0f} dBm ; 40 log10(d/10) <= {allow2:.0f} ; log10(d/10) <= {allow2/40:.0f} ; dmax = {10*10**(allow2/40):.0f} m')
print(f'  wrong (no d0): 40 log10 d <= {allow2:.0f} -> d <= {10**(allow2/40):.0f} m')
L2 = 40 * log10(2000 / 10)
Ptneed = -100 + 50 + L2
print(f'  cover 2000 m: log10(200) = {log10(200):.5f} ; 40 log10 200 = {L2:.2f} dB ; Pt >= -100 + 50 + {L2:.2f} = {Ptneed:.2f} dBm')
print(f'  = 10^({Ptneed:.2f}/10) mW = {10**(Ptneed/10):.0f} mW = {10**(Ptneed/10)/1e3:.2f} W ; extra vs 1000 m = {40*log10(2):.2f} dB = x{10**(40*log10(2)/10):.1f}')
print('-- ex3: graph PL vs log10 d: 40 dB at log10 d = 0, 145 dB at log10 d = 3 ; Pt 20 dBm, d 200 m ; free space at 2 GHz')
slope3 = (145 - 40) / 3
g3 = slope3 / 10
PL3 = 40 + 35 * log10(200)
Pr3 = 20 - PL3
lam3 = C / 2e9
PLfs = 20 * log10(4 * pi * 200 / lam3)
print(f'  slope = (145-40)/3 = {slope3:.1f} dB per unit log10 d ; 10 gamma = {slope3:.0f} -> gamma = {g3:.2f} ; K_dB = -40 dB')
print(f'  35 log10 200 = {35*log10(200):.2f} dB ; PL(200) = {PL3:.2f} dB ; Pr = 20 - {PL3:.2f} = {Pr3:.2f} dBm')
print(f'  lambda = 3e8/2e9 = {lam3:.3f} m ; 4 pi d / lambda = {4*pi*200/lam3:.1f} ; free-space PL = 20 log10(...) = {PLfs:.2f} dB ; Pr_fs = {20-PLfs:.2f} dBm')
print(f'  difference = {PL3-PLfs:.2f} dB (1 dp {PL3-PLfs:.1f}) = x{10**((PL3-PLfs)/10):.0f} = {10**((PL3-PLfs)/10):.1e}')
print(f'  per decade: free space 20 dB, simplified 10*gamma = {10*g3:.0f} dB')
print('-- trap: focused Q1 (p8q10) free space 900 MHz 1 km vs simplified K -31.5 gamma 3.5, Pt 30 dBm')
fs1k = 30 + 20 * log10((C / 900e6) / (4 * pi * 1000)); sp1k = 30 - 31.5 - 35 * log10(1000)
print(f'  free space {fs1k:.2f} dBm ; simplified {sp1k:.2f} dBm ; gap {fs1k-sp1k:.2f} dB')
print(f'  units: 100 mW = {dB(100):.0f} dBm ; 4 W = {dB(4000):.2f} dBm ; 1e-3 = {dB(1e-3):.0f} dB')

print('=' * 70)
print('T4 TABLE  least squares: Practice 1 Q1 vs mock B.Q2')
d1 = [5, 25, 65, 110, 400, 1000]; M1 = [-60, -80, -105, -115, -130, -150]
f1 = fit(d1, M1)
show('P1 Q1', f1, M1)
s1 = sqrt(f1['mse'])
print(f'    sum M = {sum(M1)} ; /6 = {sum(M1)/6:.2f} ; Sxy/Sxx = {f1["Sxy"]:.2f}/{f1["Sxx"]:.2f}')
print(f'    SSE/6 = {f1["sse"]:.2f}/6 = {f1["mse"]:.2f} ; sigma = {s1:.2f} ; 10/3.45 = {10/3.45:.2f}')
print(f'    trap: x = log10 d instead of 10 log10 d -> gamma would be {10*f1["g"]:.1f}')
print(f'    (b) margin 10 dB: 10/sigma = {10/s1:.4f} ; Q(exact) = {Q(10/s1):.3e} ; Q(2.90) table = {Q(2.90):.3e}')
print(f'    check K: Mbar + gamma*xbar = {f1["Mb"]:.2f} + {f1["g"]:.3f}*{f1["xb"]:.2f} = {f1["Mb"]+f1["g"]*f1["xb"]:.2f}')
x1 = f1['x']
offm = sum((b - (-31.4 - 3.86 * a)) ** 2 for a, b in zip(x1, M1)) / 6
print(f'    official K=-31.4, gamma=3.86 put back: MSE = {offm:.2f}')
print(f'    lecturer MSE 9.656: 10/sqrt = {10/sqrt(9.656):.3f} (2 dp {10/sqrt(9.656):.2f}; lecturer used 3.23) ; Q(3.23) table = {Q(3.23):.3e}')
show('mock B.Q2', fB, MB2)
sB = sqrt(fB['mse'])
print(f'    sum M = {sum(MB2)} ; /4 = {sum(MB2)/4:.2f} ; 194.95/57.92 = {194.95/57.92:.4f} ; SSE/4 = {fB["sse"]:.2f}/4 = {fB["mse"]:.2f} ; 8/3.35 = {8/3.35:.3f}')
print(f'    check K: -87.5 + 3.366*15 = {-87.5 + 3.366*15:.2f}')
print(f'    (c) margin 8 dB: 8/sigma = {8/sB:.4f} ; Q(exact) = {Q(8/sB):.3e} ; Q(2.39) table = {Q(2.39):.3e}')
print(f'    SSE check 2.67^2+5.20^2+3.20^2+0.67^2 = {2.67**2+5.20**2+3.20**2+0.67**2:.2f}')

print('=' * 70)
print('T4 EXAMPLES')
print('-- ex1: d = 5, 50, 500, 5000 m ; M = -56, -92, -118, -155 dB ; d0 = 1 m ; margin 5 dB')
de1 = [5, 50, 500, 5000]; Me1 = [-56, -92, -118, -155]
fe1 = fit(de1, Me1)
show('ex1', fe1, Me1)
se1 = sqrt(fe1['mse'])
print(f'    10 log10 5 = {10*log10(5):.4f} ; sum M = {sum(Me1)} ; /4 = {sum(Me1)/4:.2f} ; SSE/4 = {fe1["sse"]:.2f}/4 = {fe1["mse"]:.3f} ; 5/2.361 = {5/2.361:.3f}')
print(f'    K: {fe1["Mb"]:.2f} + {fe1["g"]:.2f}*{fe1["xb"]:.2f} = {fe1["Mb"]+fe1["g"]*fe1["xb"]:.2f}')
print(f'    pred via Mbar - gamma*(x-xbar): {[round(fe1["Mb"] - fe1["g"]*(a-fe1["xb"]), 2) for a in fe1["x"]]}')
print(f'    margin 5 dB: 5/sigma = {5/se1:.4f} ; Q(exact) = {Q(5/se1):.4f} ; Q(2.12) table = {Q(2.12):.4f}')
print('-- ex2: Pt 30 dBm ; d = 20, 100, 500 m ; Pr = -40, -61, -88 dBm ; d0 = 10 m ; normal equations (sums)')
de2 = [20, 100, 500]; Pr2 = [-40, -61, -88]; Me2 = [p - 30 for p in Pr2]
fe2 = fit(de2, Me2, d0=10)
x2 = fe2['x']; n2 = 3
Sx = sum(x2); Sx2 = sum(a * a for a in x2); SM = sum(Me2); SxM = sum(a * b for a, b in zip(x2, Me2))
print(f'  M = Pr - Pt = {Me2} ; x = 10log10(d/10) = {[round(a, 4) for a in x2]}')
print(f'  x^2 = {[round(a*a, 3) for a in x2]} ; xM = {[round(a*b, 3) for a, b in zip(x2, Me2)]}')
print(f'  sum x = {Sx:.4f} ; sum x^2 = {Sx2:.3f} ; sum M = {SM} ; sum xM = {SxM:.3f}')
num = n2 * SxM - Sx * SM; den = n2 * Sx2 - Sx ** 2
gs = -num / den; Ks = (SM + gs * Sx) / n2
print(f'  n*sum xM = {n2*SxM:.2f} ; sum x * sum M = {Sx*SM:.2f} ; numerator = {num:.2f}')
print(f'  n*sum x^2 = {n2*Sx2:.2f} ; (sum x)^2 = {Sx**2:.2f} ; denominator = {den:.2f}')
print(f'  -gamma = {num/den:.4f} -> gamma = {gs:.4f} ; K = ({SM} + {gs:.4f}*{Sx:.2f})/3 = {Ks:.3f} dB')
print(f'  gamma*sum x = {gs*Sx:.2f} ; (sum M + that) = {SM + gs*Sx:.2f}')
print(f'  deviation-form check: gamma = {fe2["g"]:.4f} K = {fe2["K"]:.3f}')
print('  pred =', [round(p, 2) for p in fe2['pred']], 'res =', [round(r, 2) for r in fe2['res']],
      f'MSE = {fe2["mse"]:.3f} sigma = {sqrt(fe2["mse"]):.3f}')
print(f'  wrong (d0 = 1 m used): x = {[round(10*log10(t), 2) for t in de2]} ; K would be {fit(de2, Me2)["K"]:.2f} (gamma same {fit(de2, Me2)["g"]:.4f})')
print('-- ex3: n = 5, SSE = 101.25 dB^2 ; margin 9 dB ; target 1%')
mse3 = 101.25 / 5; s3 = sqrt(mse3)
print(f'  MSE = {mse3:.2f} dB^2 ; sigma = {s3:.2f} dB ; 9/sigma = {9/s3:.2f} ; Pout = Q(2.00) = {Q(9/s3):.4f}')
print(f'  1%: margin >= 2.326*{s3:.1f} = {2.326*s3:.2f} dB ; extra = {2.326*s3-9:.2f} dB')
w1 = 101.25 / 3
print(f'  wrong n-2: {w1:.2f} -> sigma {sqrt(w1):.3f} -> 9/sigma = {9/sqrt(w1):.3f} -> Q(1.55) = {Q(1.55):.4f} (exact {Q(9/sqrt(w1)):.4f})')
print(f'  wrong /sigma^2: 9/20.25 = {9/mse3:.3f} -> Q(0.44) = {Q(0.44):.3f} (exact {Q(9/mse3):.3f})')

print('=' * 70)
print('2023-24 Q1(a)(ii) number (only quoted in passing): sigma < 10/2.326 =', f'{10/2.326:.2f} dB ; sigma^2 < {(10/2.326)**2:.1f} dB^2')

print('=' * 70)
print('ROUNDED VALUES AS QUOTED IN THE FRAGMENT')
print(f'  log10 2 = {log10(2):.3f} ; log10 200 = {log10(200):.3f}')
print(f'  2024-25: B = {B:.2f} ; d = {10**B:.0f} m')
print(f'  mock A.Q2: dmax ~ {10**(allow/36):.0f} m ; log10 d <= {allow/36:.3f}')
print(f'  focused Q1 gap ~ {fs1k-sp1k:.0f} dB ; ex3 overestimate ~ {PL3-PLfs:.0f} dB')
print(f'  P1 Q1: gamma = {f1["g"]:.2f} ; K_dB = {f1["K"]:.1f} (2 dp {f1["K"]:.2f}) ; sigma^2 = {f1["mse"]:.2f} ; sigma = {s1:.2f} ; official put-back MSE = {offm:.1f}')
print(f'  mock B.Q2: gamma = {fB["g"]:.2f} ; K_dB = {fB["K"]:.1f} (2 dp {fB["K"]:.2f}) ; sigma^2 = {fB["mse"]:.2f} ; sigma = {sB:.2f}')
print(f'  t4 ex1: gamma = {fe1["g"]:.2f} ; K_dB = {fe1["K"]:.2f} ; sigma = {se1:.2f} ; Pout = {Q(2.12):.4f} = {100*Q(2.12):.1f} %')
print(f'  t4 ex2: gamma = {fe2["g"]:.2f} ; K_dB = {fe2["K"]:.2f} ; sigma = {sqrt(fe2["mse"]):.2f}')
print(f'  t4 ex3: wrong n-2 sigma = {sqrt(w1):.2f} ; wrong /sigma^2 Q arg = {9/mse3:.2f}')

print('=' * 70)
print('FIXED-DECIMAL FORMS AS PRINTED IN THE FRAGMENT (added by the checker: the lines above print some of these')
print('as 0.8 / 1.852e-03 etc.; same values, shown here with the fragment\'s decimals so each appears literally)')
print('  t4 ex1 pred =', ', '.join(f'{p:.2f}' for p in fe1['pred']), '; res =', ', '.join(f'{r:+.2f}' for r in fe1['res']))
print('  t4 ex2 pred =', ', '.join(f'{p:.2f}' for p in fe2['pred']), '; res =', ', '.join(f'{r:+.2f}' for r in fe2['res']))
print('  t4 ex2 x =', ', '.join(f'{a:.4f}' for a in x2), '; x^2 =', ', '.join(f'{a*a:.3f}' for a in x2),
      '; xM =', ', '.join(f'{a*b:.3f}' for a, b in zip(x2, Me2)))
print(f'  mock B.Q2 xbar = {fB["xb"]:.2f}')
print(f'  t3 ex1: (1/200)^3 = {(1/200)**3/1e-7:.2f}e-7 ; Pr = {lin1/1e-10:.1f}e-10 W ; Pr(400 m) = {lin1b/1e-11:.3f}e-11 W')
print(f'  P1 Q1 (b): Q(2.90) = {Q(2.90)/1e-3:.2f}e-3 (table) ; unrounded Q(10/sigma) = {Q(10/s1)/1e-3:.2f}e-3 ;'
      f' mock B.Q2 Q(2.39) = {Q(2.39)/1e-3:.2f}e-3 ; Q(3.23) = {Q(3.23)/1e-4:.2f}e-4')
