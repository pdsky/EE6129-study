#!/usr/bin/python3
"""Numbers for the self-written mock Quiz questions (practice page group P8, p8q1–p8q6). Run to re-check."""
from math import log10, log2, sqrt, exp, erfc, pi, log
from statistics import NormalDist

Q = lambda x: 0.5 * erfc(x / sqrt(2))
Qinv = lambda p: NormalDist().inv_cdf(1 - p)
lin = lambda db: 10 ** (db / 10)
dB = lambda x: 10 * log10(x)

print('--- p8q1  two-state channel, total probability, Bayes, discrete SNR')
pG, pB, eG, eB = 0.7, 0.3, 1e-4, 1e-2
Pe = pG * eG + pB * eB
print(f'(a) Pe = {Pe:.4e}')
print(f'(b) P(Bad | error) = {pB*eB/Pe:.4f}')
vals, probs = [lin(10), lin(0)], [0.7, 0.3]
m = sum(v * p for v, p in zip(vals, probs)); m2 = sum(v * v * p for v, p in zip(vals, probs))
print(f'(c) E[g] = {m:.3f} = {dB(m):.2f} dB ; E[g^2] = {m2:.3f} ; Var = {m2-m*m:.3f} ; std = {sqrt(m2-m*m):.3f} ; avg of dB values = {0.7*10+0.3*0:.1f} dB')

print('--- p8q2  simplified path loss + shadowing outage')
Pt, K, g, Pmin, s = dB(100), -31.5, 3.6, -110, 6
Pr300 = Pt + K - 10 * g * log10(300)
print(f'Pt = {Pt:.1f} dBm ; (a) Pr(300 m) = {Pr300:.2f} dBm ; (b) margin = {Pr300-Pmin:.2f} dB ; Pout = Q({(Pr300-Pmin)/s:.3f}) = {Q((Pr300-Pmin)/s):.4f}')
x = Qinv(0.01); need = Pmin + x * s
dmax = 10 ** ((Pt + K - need) / (10 * g))
print(f'(c) Q^-1(0.01) = {x:.3f} ; margin {x*s:.2f} dB ; Pr >= {need:.2f} dBm ; dmax = {dmax:.1f} m')

print('--- p8q3  discrete power delay profile, Doppler, AFD')
taus, pdb = [0, 1, 3], [0, -3, -6]
P = [lin(p) for p in pdb]; S = sum(P)
mu = sum(t * p for t, p in zip(taus, P)) / S
e2 = sum(t * t * p for t, p in zip(taus, P)) / S
sig = sqrt(e2 - mu * mu)
print(f'P = {[round(p,4) for p in P]} sum {S:.4f} ; (a) mu = {mu:.3f} us ; E[t^2] = {e2:.3f} ; sigma = {sig:.3f} us')
Ts = 1 / 50e3
print(f'(b) Ts = {Ts*1e6:.0f} us ; sigma/Ts = {sig*1e-6/Ts:.4f} ; max Rs flat = {0.1/(sig*1e-6)/1e3:.1f} ksps')
v, fc = 72 / 3.6, 1.8e9
fm = v * fc / 3e8; Tc = 1 / fm
print(f'(b) fm = {fm:.1f} Hz ; Tc = {Tc*1e3:.2f} ms ; Ts/Tc = {Ts/Tc:.2e}')
rho = sqrt(0.1)
afd = (exp(rho**2) - 1) / (sqrt(2 * pi) * fm * rho); lcr = sqrt(2 * pi) * fm * rho * exp(-rho**2)
print(f'(c) rho = {rho:.4f} ; AFD = {afd*1e3:.3f} ms ; LCR = {lcr:.2f} /s ; symbols per fade = {afd/Ts:.1f} ; fraction below = {afd*lcr:.4f} = 1-e^-0.1 = {1-exp(-0.1):.4f}')
afd_wrong = (exp(0.01) - 1) / (sqrt(2 * pi) * fm * 0.1)
print(f'    (trap) rho = 0.1 would give AFD = {afd_wrong*1e3:.3f} ms')

print('--- p8q4  Rayleigh outage, fade margin')
gbar, g0 = lin(20), lin(7)
print(f'(a) g0/gbar = {g0/gbar:.4f} ; Pout = {1-exp(-g0/gbar):.4f}')
gneed = g0 / log(1 / (1 - 0.01))
print(f'(b) gbar needed = {gneed:.1f} = {dB(gneed):.2f} dB ; fade margin = {dB(gneed)-7:.2f} dB ; formula 10log10(1/ln(1/0.99)) = {dB(1/log(1/0.99)):.2f} dB')
print(f'(c) P(g > gbar) = e^-1 = {exp(-1):.4f} ; P(g < gbar/10) = {1-exp(-0.1):.4f}')

print('--- p8q5  least-squares fit (4 points) + outage')
d = [10, 20, 50, 100]; M = [-68, -86, -91, -105]
xs = [10 * log10(t) for t in d]; n = len(d)
xb = sum(xs) / n; Mb = sum(M) / n
Sxy = sum((x - xb) * (y - Mb) for x, y in zip(xs, M)); Sxx = sum((x - xb) ** 2 for x in xs)
gam = -Sxy / Sxx; Kdb = Mb + gam * xb
pred = [Kdb - gam * x for x in xs]; res = [y - p for y, p in zip(M, pred)]
mse = sum(r * r for r in res) / n
print('x =', [round(x, 2) for x in xs], f'xbar = {xb:.4f} Mbar = {Mb:.2f}')
print('x-xbar =', [round(x - xb, 3) for x in xs], 'M-Mbar =', [round(y - Mb, 2) for y in M])
print(f'Sxy = {Sxy:.3f} Sxx = {Sxx:.3f} ; (a) gamma = {gam:.3f} ; K_dB = {Kdb:.2f} dB')
print('pred =', [round(p, 2) for p in pred], 'res =', [round(r, 2) for r in res], f'sum res = {sum(res):.1e}')
print(f'(b) MSE = {mse:.3f} ; sigma = {sqrt(mse):.3f} dB')
print(f'(c) Pout = Q(8/{sqrt(mse):.3f}) = Q({8/sqrt(mse):.3f}) = {Q(8/sqrt(mse)):.3e}')

print('--- p8q6  Shannon capacity, bandwidth, water-filling')
Pr, N0, Bw = -90, -174, 5e6
Nn = N0 + dB(Bw); snr = lin(Pr - Nn)
print(f'(a) N = {Nn:.2f} dBm ; SNR = {Pr-Nn:.2f} dB = {snr:.2f} ; C = {Bw*log2(1+snr)/1e6:.2f} Mbps')
Nn2 = N0 + dB(2 * Bw); snr2 = lin(Pr - Nn2)
print(f'(b) 2B: SNR = {Pr-Nn2:.2f} dB = {snr2:.2f} ; C = {2*Bw*log2(1+snr2)/1e6:.2f} Mbps ; ratio = {2*Bw*log2(1+snr2)/(Bw*log2(1+snr)):.3f}')
gs = [20, 0.5]
inv0 = (1 + sum(1 / x for x in gs)) / 2
print(f'(c) both on: 1/g0 = {inv0:.4f} g0 = {1/inv0:.4f} -> 0.5 < g0, drop')
inv0 = 1 + 1 / 20; g0 = 1 / inv0
print(f'    one on: 1/g0 = {inv0:.4f} g0 = {g0:.4f} ; P1/P = {inv0-1/20:.3f} ; C/B = log2(20/g0) = {log2(20/g0):.4f} bit/s/Hz ; per 1 MHz subchannel C = {log2(20/g0):.3f} Mbps')
print(f'    equal split (each P/2): C/B = {log2(1+10)+log2(1+0.25):.4f} ; all power to ch1: {log2(21):.4f}')

print('--- p8q7  macro-diversity with independent shadowing, diversity gain in dB')
Pav, Pth, s = -95, -105, 8
x1 = (Pav - Pth) / s
p1 = Q(x1)
print(f'(a) margin {Pav-Pth} dB ; Q({x1:.2f}) = {p1:.4f}')
print(f'(b) two independent BS: {p1:.4f}^2 = {p1*p1:.4e}')
xr = Qinv(p1 * p1)
print(f'(c) single BS needs Q(x) = {p1*p1:.4e} -> x = {xr:.3f} -> margin {xr*s:.2f} dB -> extra {xr*s-10:.2f} dB')
print(f'    table-style: Q^-1 ~ 2.29 -> margin {2.29*s:.2f} dB, extra {2.29*s-10:.2f} dB')

print('--- p8q8  fading type, LCR from counts, Rayleigh consistency')
Bc, fm, Rs = 200e3, 100, 50e3
print(f'(a) Bs ~ Rs = {Rs/1e3:.0f} kHz < Bc {Bc/1e3:.0f} kHz -> flat ; Bd = fm = {fm} Hz << Bs ; Tc ~ 1/fm = {1e3/fm:.0f} ms >> Ts = {1e6/Rs:.0f} us -> slow')
N, T, afd = 300, 10, 0.5e-3
lcr = N / T; frac = lcr * afd; Ts = 1 / Rs
print(f'(b) LCR = {lcr:.0f}/s ; fraction below = {frac:.4f} ; symbols per fade = {afd/Ts:.1f} ; symbol errors per s = {lcr*afd/Ts:.0f} = {frac*Rs:.0f}')
rho2 = log(1 / (1 - frac)); rho = sqrt(rho2)
print(f'(c) rho^2 = ln(1/(1-{frac})) = {rho2:.5f} ; rho = {rho:.4f} ; threshold {dB(rho2):.2f} dB below rms power')
fm_imp = lcr / (sqrt(2 * pi) * rho * exp(-rho2))
print(f'    implied fm = {fm_imp:.1f} Hz (vs 100 Hz given)')

print('--- p8q9  SNR / SIR / SINR, interference cancellation, Rayleigh outage capacity')
S, I, Nn, B = 2.0, 0.5, 0.05, 10e6
sinr = S / (I + Nn); sir = S / I; snr = S / Nn
print(f'(a) SNR = {snr:.1f} ({dB(snr):.2f} dB) ; SIR = {sir:.1f} ({dB(sir):.2f} dB) ; SINR = {sinr:.3f} ({dB(sinr):.2f} dB) ; C = {B*log2(1+sinr)/1e6:.2f} Mbps')
print(f'(b) interference removed: C = {B*log2(1+snr)/1e6:.2f} Mbps ; gain x{log2(1+snr)/log2(1+sinr):.2f}')
gb, eps = lin(20), 0.01
gmin = gb * log(1 / (1 - eps))
print(f'(c) gamma_min = {gmin:.3f} ({dB(gmin):.2f} dB) ; C_eps = {B*log2(1+gmin)/1e6:.2f} Mbps ; AWGN at 20 dB = {B*log2(1+gb)/1e6:.2f} Mbps ; FM = {20-dB(gmin):.2f} dB')
