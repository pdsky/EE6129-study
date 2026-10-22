#!/usr/bin/python3
"""Independent check of every number in frag_rayleigh.html (t6 Rayleigh outage / fade margin, t7 Rician K).

Written by the adversarial checker; does not import or reuse check_rayleigh.py.
stdlib only. Q via statistics.NormalDist. Rician outage by the exact Poisson-mixture series of the
noncentral chi-square (no numerical integration), cross-checked by Monte Carlo.
Run: /usr/bin/python3 _verify_rayleigh.py
"""
import math
import random
from statistics import NormalDist

N01 = NormalDist()


def Q(x):
    return 1.0 - N01.cdf(x)


def db2lin(d):
    return 10.0 ** (d / 10.0)


def lin2db(x):
    return 10.0 * math.log10(x)


def ray_out(g0, gbar):
    """Rayleigh outage P(gamma < g0), linear inputs."""
    return 1.0 - math.exp(-g0 / gbar)


def lnf(eps):
    return math.log(1.0 / (1.0 - eps))


def rice_cdf(u, K):
    """P(gamma/gbar < u) for Rician fading, exact series.
    2(K+1)gamma/gbar is noncentral chi-square, 2 dof, noncentrality 2K = Poisson(K) mixture of
    central chi-square with 2n+2 dof:  F = sum_n e^-K K^n/n! * P(n+1, (K+1)u)."""
    y = (K + 1.0) * u
    tot = 0.0
    w = math.exp(-K)                       # Poisson weight n = 0
    term = math.exp(-y)                    # e^-y y^k/k!, k = 0
    partial = term                         # sum_{k<=n} e^-y y^k/k!
    nmax = int(K + 60 * math.sqrt(K + 1) + 80)
    for n in range(nmax):
        tot += w * (1.0 - partial)
        w *= K / (n + 1)
        term *= y / (n + 1)
        partial += term
    return tot


def poisson_tail(n, y):
    """sum_{k>n} e^-y y^k/k!  computed directly (no 1 - partial cancellation)."""
    lt = -y + (n + 1) * math.log(y) - math.lgamma(n + 2) if y > 0 else -math.inf
    if lt == -math.inf:
        return 0.0
    t = math.exp(lt)
    s = 0.0
    k = n + 1
    while True:
        s += t
        k += 1
        t *= y / k
        if t < 1e-18 * s or k > n + 2000:
            return s


def rice_cdf_stable(u, K):
    """Same series as rice_cdf but each incomplete-gamma term is the Poisson tail; for tiny CDFs."""
    y = (K + 1.0) * u
    tot = 0.0
    nmax = int(K + 60 * math.sqrt(K + 1) + 80)
    for n in range(nmax):
        lw = -K + (n * math.log(K) if K > 0 else (0.0 if n == 0 else -math.inf)) - math.lgamma(n + 1)
        if lw == -math.inf:
            break
        tot += math.exp(lw) * poisson_tail(n, y)
    return tot


def rice_mc(u, K, n=400000, seed=1):
    """Monte Carlo: total mean power 1; LOS amplitude^2 = K/(K+1); scattered power 1/(K+1)."""
    rnd = random.Random(seed)
    s = math.sqrt(K / (K + 1.0))
    sig = math.sqrt(1.0 / (K + 1.0) / 2.0)
    c = 0
    for _ in range(n):
        i = s + rnd.gauss(0, sig)
        q = rnd.gauss(0, sig)
        if i * i + q * q < u:
            c += 1
    return c / n


def hdr(t):
    print('\n==== ' + t)


# ------------------------------------------------------------------ t6
hdr('t6 formula card: Rayleigh outage approximation error, dB rule, complement, rho')
for x in (5.012 / 100, 0.1, 0.5):
    e = ray_out(x, 1)
    print(f'x={x:.5f}: 1-e^-x={e:.6f}  approx x too high by {(x - e) / e * 100:.2f}%')
for d in (10, 20, 30):
    print(f'threshold {d} dB below mean: x={db2lin(-d):g}  Pout={ray_out(db2lin(-d), 1):.6f} = {ray_out(db2lin(-d), 1) * 100:.4f}%')
print(f'e^-1 = {math.exp(-1):.5f} ; 1-e^-1 = {1 - math.exp(-1):.5f}')
print(f'rho=0.1 -> rho^2=0.01 -> 1-e^-0.01 = {1 - math.exp(-0.01):.6f}')

hdr('t6 formula card: fade margin vs eps')
for eps in (0.10, 0.05, 0.02, 0.01, 0.005, 0.001):
    print(f'eps={eps}: ln(1/(1-eps))={lnf(eps):.7f}  FM exact={lin2db(1 / lnf(eps)):.4f} dB  approx 10log(1/eps)={lin2db(1 / eps):.4f} dB')

hdr('t6 table A col: final 2024-25 Q1(b)(i) single branch (Ch4)')
qb = Q(3.0)
gb = 3.0 ** 2 / 2
print(f'Q(3.0)={qb:.6f} (paper 1.35e-3) -> sqrt(2 gb)=3.0 -> gb={gb}')
x = gb / 30
print(f'x=4.5/30={x:.4f}  Pout=1-e^-0.15={ray_out(gb, 30):.6f}  approx x={x} too high by {(x - ray_out(gb, 30)) / ray_out(gb, 30) * 100:.2f}%')
print(f'  (rest of the question, Ch4) M = ln0.02/ln{ray_out(gb, 30):.4f} = {math.log(0.02) / math.log(ray_out(gb, 30)):.3f}')

hdr('t6 table A col: mock B Q1(a)')
g, g0 = db2lin(20), db2lin(7)
print(f'gbar=20 dB={g:.4f}  g0=7 dB={g0:.5f}  x={g0 / g:.6f}  Pout={ray_out(g0, g):.6f}')

hdr('t6 table A (writer col 4 / now src line): focused Q3(c)')
Pt_dBm = lin2db(1000.0)
Pr = Pt_dBm + (-40) - 10 * 3 * math.log10(1000 / 1)
print(f'Pt=1 W={Pt_dBm:.2f} dBm  Pr={Pr:.3f} dBm  gbar={Pr - (-120):.3f} dB={db2lin(Pr + 120):.4f}  g0=10 dB={db2lin(10):.4f}  Pout={ray_out(10, 100):.6f}')

hdr('t6 table B: final 2025-26 S2 Q1(a)(iii)')
gR = db2lin(25)
gmin = gR * lnf(0.005)
print(f'gbarR=25 dB={gR:.4f}  ln(1/0.995)={lnf(0.005):.7f}  gmin={gmin:.5f} = {lin2db(gmin):.4f} dB  FM=25-{lin2db(gmin):.4f}={25 - lin2db(gmin):.4f} dB  formula={lin2db(1 / lnf(0.005)):.4f}')
print(f'  rounded chain 316.2*0.005013 = {316.2 * 0.005013:.4f}')

hdr('t6 table B: mock B Q1(b)')
need = db2lin(7) / lnf(0.01)
print(f'g0={db2lin(7):.5f}  ln(1/0.99)={lnf(0.01):.7f}  gbar={need:.4f} = {lin2db(need):.4f} dB  FM={lin2db(need) - 7:.4f} dB  formula={lin2db(1 / lnf(0.01)):.4f}')
print(f'  rounded chain 5.012/0.01005 = {5.012 / 0.01005:.3f}')
print(f'final 2023-24 Q1(a)(iv): ln(1/0.999)={lnf(0.001):.8f}  FM={lin2db(1 / lnf(0.001)):.4f} dB')

hdr('t6 example 1')
gdb = -92 - (-110)
g = db2lin(gdb)
g0 = db2lin(6)
x = g0 / g
print(f'gbar={gdb} dB={g:.4f}  g0=6 dB={g0:.5f}  x={x:.6f} (10^-1.2={db2lin(-12):.6f})  Pout={ray_out(g0, g):.6f}')
g21 = db2lin(21)
print(f'(b) 21 dB={g21:.3f}  ratio={g21 / g:.5f} (10^0.3={db2lin(3):.5f})  P(gamma>21 dB)=e^-ratio={math.exp(-g21 / g):.5f}')

hdr('t6 example 2')
g0 = db2lin(8)
need = g0 / lnf(0.02)
print(f'g0=8 dB={g0:.5f}  ln(1/0.98)={lnf(0.02):.7f}  gbar={need:.4f} = {lin2db(need):.4f} dB  FM={lin2db(need) - 8:.4f}  formula={lin2db(1 / lnf(0.02)):.4f}  approx 10log50={lin2db(50):.4f}')
prmin = -115 + lin2db(need)
rhs = 30 - 40 - prmin
print(f'Pr,min={prmin:.4f} dBm  35 log d <= {rhs:.4f}  log d <= {rhs / 35:.5f}  d <= {10 ** (rhs / 35):.3f} m')
print(f'  with rounded 80.05: log d <= {80.05 / 35:.5f}  d <= {10 ** (80.05 / 35):.3f} m')

hdr('t6 example 3')
print(f'shadow Q(15/6)=Q(2.5)={Q(2.5):.6f}   Rayleigh 10^-1.5={db2lin(-15):.6f} Pout={ray_out(db2lin(-15), 1):.6f}  ratio={ray_out(db2lin(-15), 1) / Q(2.5):.3f}')
for M in (10, 15, 20):
    print(f'  sigma 8, margin {M}: shadow Q({M / 8})={Q(M / 8):.6f}  Rayleigh={ray_out(db2lin(-M), 1):.6f}')

hdr('t6 traps')
print(f'1-e^-(7/20)={1 - math.exp(-7 / 20):.5f}  correct={ray_out(db2lin(7), 100):.5f}')
print(f'log10(1/0.99)={math.log10(1 / 0.99):.7f} -> 10log10(1/that)={lin2db(1 / math.log10(1 / 0.99)):.4f} dB')
print(f'498.7-5.012={498.7 - 5.012:.3f} ; exact {db2lin(7) / lnf(0.01) - db2lin(7):.3f}')
print(f'10^0.85={db2lin(8.5):.4f}')

# ------------------------------------------------------------------ t7
hdr('t7 Rician: implementation sanity (learn_02 table, rho=0.3 -> u=0.09: 8.6, 6.6, 1.4, 0.06 %)')
for K in (0, 1, 4, 10):
    print(f'  K={K}: P(env<0.3 rms)={rice_cdf(0.09, K) * 100:.3f}%')

hdr('t7 Rician outage, gbar 20 dB, g0 10 dB (u=0.1) -- series and Monte Carlo')
for K in (0, 1, db2lin(6), 4, 10):
    ser = rice_cdf(0.1, K)
    mc = rice_mc(0.1, K)
    print(f'  K={K:.4f} ({"-inf" if K == 0 else f"{lin2db(K):.3f}"} dB): series={ser:.6f} ({ser * 100:.4f}%)  MC={mc:.5f}')
print(f'  ratio Rayleigh/K=10: {rice_cdf(0.1, 0) / rice_cdf(0.1, 10):.2f}')

hdr('t7 K-trend: is outage decreasing in K for every threshold below the mean?')
Ks = [0, 0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40, 50, 70, 100]
print(f'  stable vs plain series agree at u=0.1: K=4 {rice_cdf_stable(0.1, 4):.6f} vs {rice_cdf(0.1, 4):.6f}; K=10 {rice_cdf_stable(0.1, 10):.3e} vs {rice_cdf(0.1, 10):.3e}')
first_bad = None
for i in range(1, 151):
    u = i / 100
    v = [rice_cdf_stable(u, K) for K in Ks]
    mono = all(b < a * (1 - 1e-9) for a, b in zip(v, v[1:]) if a > 1e-280)
    if not mono and first_bad is None:
        first_bad = u
print(f'  smallest threshold ratio u (step 0.01, K grid 0..100) where outage is NOT decreasing in K: u = {first_bad}')
first_bad = None
for i in range(900, 1101):
    u = i / 1000
    v = [rice_cdf_stable(u, K) for K in Ks]
    if not all(b < a * (1 - 1e-9) for a, b in zip(v, v[1:]) if a > 1e-280):
        first_bad = u
        break
print(f'  finer (step 0.001 from 0.900): first non-monotone u = {first_bad}')
for u in (0.9, 0.95, 0.99, 1.0, 1.05, 1.1, 1.5):
    v = [rice_cdf(u, K) for K in (0, 1, 4, 10, 30)]
    print(f'  u={u}: ' + ' '.join(f'{a:.4f}' for a in v))

hdr('t7 numbers in tables / examples / traps')
print(f'K=4 -> {lin2db(4):.4f} dB  share {4 / 5:.3f}/{1 / 5:.3f}')
K6 = db2lin(6)
print(f'K=6 dB -> {K6:.5f}  K+1={K6 + 1:.5f}  share {K6 / (K6 + 1) * 100:.3f}% / {1 / (K6 + 1) * 100:.3f}%')
d = db2lin(-80)
sc = [db2lin(v) for v in (-90, -92, -95)]
S = sum(sc)
Kx = d / S
print(f'ex1: direct {d:.4e}; scattered {sc[0]:.4e} {sc[1]:.4e} {sc[2]:.4e}; sum {S:.4e} mW = {lin2db(S):.4f} dBm; K={Kx:.4f} = {lin2db(Kx):.4f} dB; share {Kx / (Kx + 1) * 100:.3f}%')
Km = db2lin(-3)
print(f'ex2: K=10^-0.3={Km:.5f}  share {Km / (Km + 1) * 100:.3f}% / {1 / (Km + 1) * 100:.3f}%')
print(f'traps: 20log4={20 * math.log10(4):.4f}  10log4={lin2db(4):.4f}  10log2={lin2db(2):.4f}  K=0 dB -> {db2lin(0)} -> 50/50')
