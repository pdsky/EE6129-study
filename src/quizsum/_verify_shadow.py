#!/usr/bin/python3
"""Independent re-check of frag_shadow.html (topic t5: log-normal shadowing outage, inverse Q,
maximum distance / allowed sigma, macro-diversity).

Written separately from check_shadow.py, with its own code paths:
  * Q via statistics.NormalDist, cross-checked against math.erfc; Q^-1 via NormalDist.inv_cdf,
    cross-checked by bisection on the erfc form;
  * table lookups done on the 4-decimal table values a student reads, rounding half-up;
  * least-squares fit of Practice 1 Q1 via the raw normal equations (not the centred formula);
  * the correlated macro-diversity integral by composite Simpson + a Monte-Carlo cross-check.
For every number printed in the fragment it recomputes the value, rounds it to the precision shown
and asserts the fragment shows exactly that string in that place. It then lists any decimal in the
fragment that no check covers, checks the quoted source numbers / lecturer claims / status badges
against the source files, and lints the HTML and TeX.
usage: /usr/bin/python3 _verify_shadow.py      (exit status 1 if anything fails)
"""
import html, math, pathlib, random, re, sys
from decimal import Decimal, ROUND_HALF_UP
from html.parser import HTMLParser
from statistics import NormalDist

B = pathlib.Path(__file__).resolve().parent
SRC = B.parent
FRAG = B / 'frag_shadow.html'
RAW = FRAG.read_text(encoding='utf-8')

FAIL = []
NOTE = []
COVERED = set()


def fail(msg):
    FAIL.append(msg)
    print('  FAIL', msg)


# ------------------------------------------------------------------ text normalisation
def norm(s, flat):
    s = re.sub(r'<sup>(.*?)</sup>', r'^\1', s)
    s = re.sub(r'<sub>(.*?)</sub>', r'_\1', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s).replace('−', '-').replace('\xa0', ' ')
    return re.sub(r'\s+', '', s) if flat else re.sub(r'\s+', ' ', s)


TXT, FLAT = norm(RAW, False), norm(RAW, True)

# ------------------------------------------------------------------ Q function, own implementation
ND = NormalDist()


def Q(x):
    return ND.cdf(-x)


def Qe(x):
    return 0.5 * math.erfc(x / math.sqrt(2))


def Qinv(p):
    return -ND.inv_cdf(p)


def Qinv_bisect(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if Qe(mid) > p else (lo, mid)
    return (lo + hi) / 2


def rnd(v, nd):
    """round half-up the way it is done by hand, return the string with an ASCII minus"""
    q = Decimal(1).scaleb(-nd)
    d = Decimal(repr(v)).quantize(q, rounding=ROUND_HALF_UP)
    if d == 0:
        d = abs(d)
    return f'{d:f}'


def Qtab(x):
    """value as printed in a 4-decimal Q table (more decimals for small values)"""
    v = Q(x)
    return float(rnd(v, 4)) if v >= 0.01 else float(rnd(v, 5))


def interp(x0, p, table=True):
    q0, q1 = (Qtab(x0), Qtab(x0 + 0.01)) if table else (Q(x0), Q(x0 + 0.01))
    return x0 + 0.01 * (q0 - p) / (q0 - q1)


dBm = lambda mw: 10 * math.log10(mw)


def chk(label, value, nd, ctx, shown=None):
    """value rounded to nd decimals must appear where ctx says ('§' marks the number)."""
    s = rnd(value, nd)
    if shown is not None and s != shown:
        fail(f'{label}: computed {value!r} rounds to {s}, page needs {shown}')
        s = shown
    COVERED.add(s.lstrip('-'))
    want = re.sub(r'\s+', '', ctx.replace('§', s)).replace('−', '-')
    ok = want in FLAT
    print(f'  {"ok  " if ok else "MISS"} {label:<44} {value:>14.6g} -> {s:<10} {"" if ok else "| expected: " + want}')
    if not ok:
        fail(f'{label}: "{want}" not found in fragment (value {value!r} -> {s})')


def sec(t):
    print(f'\n=== {t}')


# ------------------------------------------------------------------ 0. Q implementation sanity
sec('0. Q / Q^-1 cross-check (NormalDist vs erfc vs bisection)')
for x in [0, 0.18, 0.62, 0.625, 0.63, 1, 1.25, 1.28, 1.282, 1.29, 1.47, 1.5, 1.55, 1.553, 1.64, 1.645, 1.65,
          2, 2.13, 2.28, 2.29, 2.32, 2.326, 2.33, 2.61, 2.62, 2.69, 2.9, 3.09]:
    if abs(Q(x) - Qe(x)) > 1e-12:
        fail(f'Q mismatch at {x}')
for p in [0.1, 0.05, 0.01, 0.001, 0.0112, 0.00446]:
    if abs(Qinv(p) - Qinv_bisect(p)) > 1e-9:
        fail(f'Qinv mismatch at {p}')
print('  Q and Q^-1 agree to 1e-9 on every point used')

# ------------------------------------------------------------------ 1. formula cards + symbol table
sec('1. formula cards and symbol table')
chk('100 mW -> dBm', dBm(100), 0, '100mW=§dBm；2W')
chk('2 W -> dBm', dBm(2000), 2, '2W=2000mW=§dBm。dBm')
chk('1 W -> dBm', dBm(1000), 0, r'1\\mathrm{W}=§\\mathrm{dBm}')
chk('Q(0)', Q(0), 1, 'Q(0)=§，x越大')
chk('Q(1)', Q(1), 4, 'Q(1)=§，')
chk('Q(1.282) ~ 0.1', Q(1.282), 1, 'Q(1.282)≈§，')
chk('Q(1.645)', Q(1.645), 2, 'Q(1.645)=§，Q(2)')
chk('Q(2)', Q(2), 4, 'Q(2)=§，Q(2.326)')
chk('Q(2.326)', Q(2.326), 2, 'Q(2.326)=§，Q(3.09)')
chk('Q(3.09)', Q(3.09), 3, 'Q(3.09)=§。')
chk('x_0.1', Qinv(0.1), 3, r'\(x_{0.1}=§\)')
chk('x_0.05', Qinv(0.05), 3, r'\(x_{0.05}=§\)')
chk('x_0.01', Qinv(0.01), 3, r'\(x_{0.01}=§\)')
chk('x_0.001', Qinv(0.001), 2, r'\(x_{0.001}=§\)')
chk('symbol table Q^-1(0.01)', Qinv(0.01), 3, r'\(Q^{-1}(0.01)=§\)')
chk('lecture p.16: 1% <-> M >= 2.33 sigma', Qinv(0.01), 2, r'\(M\ge§\sigma\)')

# ------------------------------------------------------------------ 2. table A (forward)
sec('2. table A: Practice 1 Q2(a) and mock A Q2(a)(b)')
chk('P1Q2 margin 15-10', 15 - 10, 0, '15-10=§dB')
chk('P1Q2 5/8', 5 / 8, 3, '5/8=§')
chk('Q(0.62) table', Q(0.62), 4, 'Q(0.62)=§、')
chk('Q(0.63) table', Q(0.63), 4, 'Q(0.63)=§→')
chk('Q(0.625) by interpolation of table rows', (Qtab(0.62) + Qtab(0.63)) / 2, 3, 'Q(0.625)≈§（26.6%）')
chk('Q(0.625) exact', Q(0.625), 3, 'Q(0.625)≈§（')
chk('Q(0.625) in %', 100 * Q(0.625), 1, '（§%）')
PtA = dBm(100)
plA = 10 * 3.6 * math.log10(300)
PrA = PtA - 31.5 - plA
MA = PrA + 110
chk('mock A Pt', PtA, 0, '100mW→10log₁₀100=§dBm；σ=6dB')
chk('mock A 10*gamma', 10 * 3.6, 0, '20-31.5-§log₁₀300=20-31.5')
chk('mock A 36 log10 300', plA, 2, '20-31.5-§=-100.68dBm')
chk('mock A Pr(300)', PrA, 2, '89.18=§dBm')
chk('mock A margin', MA, 2, '-100.68-(-110)=§dB')
chk('mock A 9.32/6 (shown operands)', 9.32 / 6, 3, '9.32/6=§≈1.55')
chk('mock A argument to 2 dp (shown)', 9.32 / 6, 2, '≈§')
chk('mock A argument to 2 dp (unrounded M)', MA / 6, 2, 'Q(§)=0.0606')
chk('mock A Q(1.55)', Q(1.55), 4, 'Q(1.55)=§（')
chk('mock A Q(1.553) (not rounded to 2 dp)', Q(9.32 / 6), 4, '按1.553插值是§）')
chk('mock A Q(1.553) by table interpolation', Qtab(1.55) + (9.32 / 6 - 1.55) / 0.01 * (Qtab(1.56) - Qtab(1.55)), 4, '插值是§）')

# ------------------------------------------------------------------ 3. src line A: P1Q1(b), lecture p.16
sec('3. Practice 1 Q1(b) least squares (raw normal equations) and lecture p.16 example')
d1 = [5, 25, 65, 110, 400, 1000]
M1 = [-60, -80, -105, -115, -130, -150]
x1 = [10 * math.log10(v) for v in d1]
n = len(x1)
Sx, Sy = sum(x1), sum(M1)
Sxx, Sxy = sum(v * v for v in x1), sum(a * b for a, b in zip(x1, M1))
slope = (n * Sxy - Sx * Sy) / (n * Sxx - Sx * Sx)        # M = K - gamma x  -> slope = -gamma
gam = -slope
Kdb = (Sy - slope * Sx) / n
res = [m - (Kdb - gam * x) for x, m in zip(x1, M1)]
mse = sum(r * r for r in res) / n
sig = math.sqrt(mse)
print(f'  K = {Kdb:.4f} dB, gamma = {gam:.4f}, MSE = {mse:.4f}, sigma = {sig:.4f}, sum residuals = {sum(res):.1e}')
chk('P1Q1 K_dB', Kdb, 1, 'K≈§dB、γ≈3.94')
chk('P1Q1 gamma', gam, 2, 'γ≈§、MSE')
chk('P1Q1 MSE', mse, 2, 'MSE=§dB²')
chk('P1Q1 sigma', sig, 2, 'σ=§dB，')
chk('P1Q1 10/sigma to 2 dp', 10 / sig, 2, '=Q(§)=1.87')
chk('P1Q1 Q(2.90) (x1e-3)', Q(2.90) * 1e3, 2, 'Q(2.90)=§×10⁻³')
chk('P1Q1 10/sigma unrounded', 10 / sig, 3, '不舍入的§算得')
chk('P1Q1 Q(10/sigma) unrounded (x1e-3)', Q(10 / sig) * 1e3, 2, '算得§×10⁻³')
off = sum((m - (-31.4 - 3.86 * x)) ** 2 for x, m in zip(x1, M1)) / n
print(f'  official K = -31.4, gamma = 3.86 give MSE {off:.2f} on the same data (> LS {mse:.2f}): '
      f'the official numbers are not a least-squares fit; Q(10/sqrt(9.656)) = {Q(10 / math.sqrt(9.656)):.3e}')
Prl = 0 - 26.67 - 10 * 3.97 * math.log10(150)
Ml = Prl + 118
sl = math.sqrt(3.36)
chk('lecture p.16 margin', Ml, 2, '150m处余量§dB')
chk('lecture p.16 sigma = sqrt(3.36)', sl, 3, '√3.36=§dB，Q(2.69)')
chk('lecture p.16 argument (unrounded margin)', Ml / sl, 2, 'Q(§)≈0.0036）')
chk('lecture p.16 Q(2.69)', Q(2.69), 4, 'Q(2.69)≈§）')
print(f'  note: with the rounded operands 4.94/1.833 = {4.94 / 1.833:.4f} (2 dp half-up: {rnd(4.94 / 1.833, 2)});'
      f' the lecture reads Q(2.69). Exact Q({Ml / sl:.4f}) = {Q(Ml / sl):.5f}')

# ------------------------------------------------------------------ 4. table B (backward)
sec('4. table B: 2023-24 S2 Q1(a)(ii) and mock A Q2(c)')
chk('Q(2.32) table', Q(2.32), 4, 'Q(2.32)=§、')
chk('Q(2.33) table', Q(2.33), 4, 'Q(2.33)=§→x')
chk('nearest table row x ~ 2.33', Qinv(0.01), 2, 'x≈§（精确')
chk('exact Q^-1(0.01)', Qinv(0.01), 3, '（精确§）')
chk('sigma < 10/2.326', 10 / 2.326, 2, 'σ<10/2.326=§dB')
chk('sigma^2 < 4.30^2', 4.30 ** 2, 1, '4.30²=§dB²')
chk('sigma^2 from unrounded sigma', (10 / 2.326) ** 2, 1, '<4.30²=§dB²')
chk('2.33 variant sigma', 10 / 2.33, 2, '用2.33得σ<§、')
chk('2.33 variant sigma^2', (10 / 2.33) ** 2, 1, 'σ²<§，同一题')
chk('mock A margin 2.326 x 6', 2.326 * 6, 2, 'M≥2.326×6=§dB')
chk('mock A Pr_min', -110 + 13.96, 2, '-110+13.96=§dBm')
chk('mock A 36 log d <=', 20 - 31.5 + 96.04, 2, '36log₁₀d≤§→')
chk('mock A log d <=', 84.54 / 36, 3, 'log₁₀d≤§→d≤10')
chk('mock A d_max', 10 ** 2.348, 0, 'd≤10^2.348≈§m')
dexact = 10 ** ((dBm(100) - 31.5 + 110 - Qinv(0.01) * 6) / 36)
chk('mock A d_max with exact x (closed form)', dexact, 0, '≈§m')
chk('P1Q2(b) mu > 10 + 4 x 2.326', 10 + 4 * 2.326, 1, r'10+4\times2.326=§\)dBm')
chk('P1Q2(b) official 19.32 = 10 + 4 x 2.33', 10 + 4 * 2.33, 2, '官方答案§）')

# ------------------------------------------------------------------ 5. table C (macro-diversity)
sec('5. table C: mock C Q1')
pC1 = Q(10 / 8)
chk('mock C Delta', -95 - (-105), 0, 'Δ=§dB；σ=8dB')
chk('mock C 10/8', 10 / 8, 2, 'Q(10/8)=Q(§)=')
chk('mock C Q(1.25)', pC1, 4, 'Q(1.25)=§')
chk('mock C 0.1056^2 (shown operand)', 0.1056 ** 2, 5, '0.1056²=§≈0.0112')
chk('mock C p^2 exact', pC1 ** 2, 4, '≈§（1.12')
chk('mock C p^2 mantissa x1e-2', pC1 ** 2 * 100, 2, '（§×10⁻²）')
chk('Q(2.28) table', Q(2.28), 4, 'Q(2.28)=§、')
chk('Q(2.29) table', Q(2.29), 4, 'Q(2.29)=§，')
chk('interp. with table rows and p = 0.01115', interp(2.28, 0.01115), 3, '0.01115正好在中间→插值x≈§→')
chk('exact Q^-1(p^2)', Qinv(pC1 ** 2), 3, '插值x≈§→')
chk('M_eq = 2.285 x 8', 2.285 * 8, 2, '2.285×8=§≈18.3dB')
chk('M_eq = 2.285 x 8 to 3 s.f.', 2.285 * 8, 1, '=18.28≈§dB→G')
chk('M_eq with exact x', Qinv(pC1 ** 2) * 8, 1, '≈§dB→G')
chk('practice page x = 2.29: 2.29 x 8', 2.29 * 8, 2, '2.29×8=§，也是18.3dB')
print(f'  note: exact x = {Qinv(pC1 ** 2):.4f} rounds to {rnd(Qinv(pC1 ** 2), 2)} at 2 dp; the practice page reads 2.29 '
      f'(2.285 -> 2.29 is a double rounding). Final M_eq {Qinv(pC1 ** 2) * 8:.2f} dB, gain {Qinv(pC1 ** 2) * 8 - 10:.2f} dB')
chk('G = 18.3 - 10', 18.3 - 10, 1, 'G=18.3-10=§dB')

# ------------------------------------------------------------------ 6. example 1
sec('6. example 1 (2 W, MSE 30.25, d = 400 m and 1 km)')
Pt1 = dBm(2000)
s1 = math.sqrt(30.25)
pl400 = 32 * math.log10(400)
Pr400 = Pt1 - 38 - pl400
M400 = Pr400 + 100
chk('E1 Pt', Pt1, 2, '10log₁₀2000=§dBm')
chk('E1 sigma', s1, 1, '√30.25=§dB')
chk('E1 32 log10 400', pl400, 2, '33.01-38-§=-88.26')
chk('E1 Pr(400)', Pr400, 2, '83.27=§dBm')
chk('E1 margin', M400, 2, 'M=-88.26-(-100)=§dB')
chk('E1 11.74/5.5 (shown operands)', 11.74 / 5.5, 4, '11.74/5.5=§≈2.13')
chk('E1 argument to 2 dp (shown operands)', 11.74 / 5.5, 2, '≈§，')
chk('E1 Q(2.13)', Q(2.13), 4, 'Q(2.13)=§（')
chk('E1 Q unrounded', Q(M400 / s1), 4, '不舍入算是§）')
print(f'  note: unrounded M/sigma = {M400 / s1:.4f} (rounds to {rnd(M400 / s1, 2)}); '
      f'with the shown 11.74 it is {11.74 / 5.5:.4f} -> {rnd(11.74 / 5.5, 2)}')
chk('E1 32 x 3 -> Pr(1 km)', Pt1 - 38 - 32 * math.log10(1000), 2, '32×3=§dBm')
chk('E1 margin at 1 km', Pt1 - 38 - 96 + 100, 2, 'M=-100.99-(-100)=§dB')
chk('E1 -0.99/5.5', -0.99 / 5.5, 2, '-0.99/5.5=§。')
chk('E1 Q(0.18)', Q(0.18), 4, '1-Q(0.18)=1-§=')
chk('E1 1 - Q(0.18)', 1 - Q(0.18), 3, '=1-0.4286=§。')
chk('E1 Phi(0.18)', ND.cdf(0.18), 3, r'\Phi(0.18)\)=§。')
chk('E1 answer (a) %', 100 * Q(2.13), 1, '0.0166≈§%')
chk('E1 answer (b) %', 100 * (1 - Q(0.18)), 0, '≈§%（')

# ------------------------------------------------------------------ 7. example 2
sec('7. example 2 (100 mW, K -40 dB, gamma 3, threshold -95 dBm, sigma 6 dB)')
chk('E2 Pt', dBm(100), 0, r'\(P_t\)=10log₁₀100=§dBm。(a)')
chk('Q(1.64) table', Q(1.64), 4, 'Q(1.64)=§、')
chk('Q(1.65) table', Q(1.65), 4, 'Q(1.65)=§→x')
chk('E2 x for 5% (interp.)', interp(1.64, 0.05), 3, '→x=§。所需')
chk('E2 x for 5% exact', Qinv(0.05), 3, '→x=§。所需')
chk('E2 margin 1.645 x 6', 1.645 * 6, 2, '1.645×6=§dB')
chk('E2 Pr_min', -95 + 9.87, 2, '-95+9.87=§dBm')
chk('E2 30 log d <=', 20 - 40 + 85.13, 2, '30log₁₀d≤§→')
chk('E2 log d <=', 65.13 / 30, 3, 'log₁₀d≤§→d≤10')
chk('E2 d_max', 10 ** 2.171, 1, '10^2.171=§m')
chk('E2 d_max answer', 10 ** 2.171, 0, 'd_max≈§m')
dE2 = 10 ** ((20 - 40 + 95 - Qinv(0.05) * 6) / 30)
chk('E2 d_max with exact x', dE2, 0, 'd_max≈§m')
chk('E2 30 log10 200', 30 * math.log10(200), 2, '30log₁₀200=§dB')
chk('E2 Pt_min (dBm)', -85.13 + 40 + 69.03, 2, r'\(P_t\)≥§dBm=10')
chk('E2 Pt_min exponent', 23.90 / 10, 3, '10^§mW')
chk('E2 Pt_min (mW)', 10 ** 2.390, 1, 'mW=§mW')
chk('E2 extra dB', 23.90 - 20, 2, '多§dB')
chk('E2 extra exponent', 3.90 / 10, 3, '10^§≈')
chk('E2 extra as a ratio', 10 ** 0.390, 2, '≈§倍')
chk('E2 ratio check 245.47/100', 10 ** 2.390 / 100, 2, '≈§倍')
chk('E2 Pr(100 m)', 20 - 40 - 30 * 2, 0, '30×2=§dBm')
chk('E2 margin at 100 m', -80 - (-95), 0, 'M=-80-(-95)=§dB')
chk('Q(3.09) table', Q(3.09), 3, 'Q(3.09)=§→x')
chk('E2 sigma max', 15 / 3.09, 3, '15/3.09=§dB')
chk('E2 sigma^2 (shown operand)', 4.854 ** 2, 2, '4.854²=§dB²')
chk('E2 sigma^2 answer', (15 / 3.09) ** 2, 1, 'σ²≤§dB²（σ≤')
chk('E2 sigma answer', 15 / 3.09, 2, '（σ≤§dB）')
chk('E2 answer Pt', -85.13 + 40 + 69.03, 2, r'\(P_t\)≥§dBm≈245.5mW')

# ------------------------------------------------------------------ 8. example 3 (+ correlated integral)
sec('8. example 3 (macro-diversity -92 / -104 dBm, sigma 8 dB)')
p31 = Q(1.5)
chk('E3 Delta', -92 - (-104), 0, 'Δ=-92-(-104)=§dB')
chk('E3 12/8', 12 / 8, 1, '12/8=§，')
chk('E3 Q(1.5)', p31, 4, 'Q(1.5)=§。')
chk('E3 0.0668^2 x1e-3 (shown operand)', 0.0668 ** 2 * 1e3, 2, '0.0668²=§×10⁻³')
chk('E3 p^2 exact x1e-3', p31 ** 2 * 1e3, 2, '0.0668²=§×10⁻³')
chk('Q(2.61) table', Q(2.61), 5, 'Q(2.61)=§、')
chk('Q(2.62) table', Q(2.62), 5, 'Q(2.62)=§→')
chk('E3 x by interpolation (p = 0.00446)', interp(2.61, 0.00446), 3, '→x≈§，')
chk('E3 x exact', Qinv(p31 ** 2), 3, '→x≈§，')
chk('E3 M_eq', 2.615 * 8, 2, '2.615×8=§dB')
chk('E3 gain', 20.92 - 12, 2, '20.92-12=§dB')
chk('E3 sqrt(0.01)', math.sqrt(0.01), 1, r'\sqrt{0.01}=§\)')
chk('Q(1.28) table', Q(1.28), 4, 'Q(1.28)=§、')
chk('Q(1.29) table', Q(1.29), 4, 'Q(1.29)=§→')
chk('E3 x for 0.1 (interp.)', interp(1.28, 0.1), 3, '→x=§，Δ≥')
chk('E3 per-link Delta', 1.282 * 8, 2, '1.282×8=§dB')
print(f'  (with the unrounded x = {Qinv(0.1):.4f} the per-link margin is {Qinv(0.1) * 8:.3f} dB; the page uses x = 1.282 -> 10.26)')
chk('E3 single BS', 2.326 * 8, 2, '2.326×8=§dB')
chk('E3 saving', 18.61 - 10.26, 2, '少要§dB')
chk('E3 (d) fully correlated', p31, 4, 'Q(1.5)=§，和单基站')


def corr_simpson(dn, rho, L=12.0, m=6000):
    """int phi(u) Q((dn + b u)/a)^2 du, a^2 + b^2 = 1, rho = b^2 (Practice 2 Q2(c) after u = y/sigma)."""
    b, a = math.sqrt(rho), math.sqrt(1 - rho)
    h = 2 * L / m
    f = lambda u: math.exp(-u * u / 2) / math.sqrt(2 * math.pi) * Q((dn + b * u) / a) ** 2
    s = f(-L) + f(L) + sum((4 if k % 2 else 2) * f(-L + k * h) for k in range(1, m))
    return s * h / 3


def corr_mc(dn, rho, N=1000000, seed=6129):
    """Monte Carlo: Z_i = a Y_i + b Y in units of sigma, outage when both Z_i < -dn."""
    r = random.Random(seed)
    b, a = math.sqrt(rho), math.sqrt(1 - rho)
    hit = 0
    for _ in range(N):
        y = r.gauss(0, 1)
        if a * r.gauss(0, 1) + b * y < -dn and a * r.gauss(0, 1) + b * y < -dn:
            hit += 1
    return hit / N


c15 = corr_simpson(1.5, 0.5)
chk('E3 (d) b^2 = 0.5 numerical integral', c15, 4, '约§（Quiz')
mc = corr_mc(1.5, 0.5)
se = math.sqrt(c15 * (1 - c15) / 1000000)
print(f'  Monte Carlo (1M): {mc:.4f}  (Simpson {c15:.4f}, |diff| = {abs(mc - c15):.1e}, 3 s.e. = {3 * se:.1e})')
if abs(mc - c15) > 4 * se:
    fail('Monte Carlo disagrees with the Simpson integral')
for rho, want in [(0, 0.0252), (0.25, 0.0417), (0.5, 0.0625), (0.75, 0.0905), (0.9, 0.1155)]:
    got = corr_simpson(1.0, rho)
    ok = rnd(got, 4) == rnd(want, 4)
    print(f'  practice-page table Delta = sigma, rho = {rho}: {got:.4f} (page {want}) {"ok" if ok else "MISMATCH"}')
    if not ok:
        fail(f'practice page rho table {rho}')
chk('E3 answer (a)', p31, 4, '答案：(a)§；')
chk('E3 answer (b)', p31 ** 2 * 1e3, 2, '(b)§×10⁻³，')
chk('E3 answer M_eq', 2.615 * 8, 1, '单站余量§dB')
chk('E3 answer gain', 2.615 * 8 - 12, 1, '增益约§dB')
chk('E3 answer (c)', 1.282 * 8, 2, '每站≥§dB')
chk('E3 answer (c) single', 2.326 * 8, 2, '（单站要§dB）')

# ------------------------------------------------------------------ 9. traps + English
sec('9. traps and exam English')
chk('trap lecture argument (unrounded margin)', Ml / sl, 2, '≈Q(§)≈0.0036')
chk('trap divide by variance 4.94/3.36', 4.94 / 3.36, 2, '错除3.36得Q(§)')
chk('trap Q(1.47)', Q(1.47), 3, 'Q(1.47)≈§，')
chk('trap ratio Q(1.47)/Q(2.69)', Q(1.47) / Q(2.69), 0, '大了约§倍')
chk('trap sigma^2 < 18.5', (10 / 2.326) ** 2, 1, '平方成σ²<§dB²')
chk('trap sigma < 4.30', 10 / 2.326, 2, '只写σ<§dB')
chk('trap 2 W = 33.01 dBm', dBm(2000), 2, '2W=§dBm，不是')
chk('trap 10log10(2) = 3.01 dBW', 10 * math.log10(2), 2, '不是§，§是dBW')
chk('trap 10 gamma = 36', 10 * 3.6, 0, '系数是§）')
chk('trap 2.326', Qinv(0.01), 3, r'M/\sigma\gt§\)')
chk('trap 148.3 m', 10 ** 2.171, 1, '（§m写148m）')
chk('trap double rounding: 2.1345 to 2 dp', 2.1345, 2, '2.1345舍到2位是§，')
chk('trap double rounding: 2.1345 to 3 dp', 2.1345, 3, '先变§再变')
chk('trap double rounding: 2.135 to 2 dp', 2.135, 2, '再变§）')
chk('trap d <= 223 m', 10 ** 2.348, 0, '（d≤§m、')
chk('trap sigma^2 < 18.5', (10 / 2.326) ** 2, 1, 'σ²<§dB²）；')
chk('trap 0.625', 5 / 8, 3, '（§这种')
chk('EN Pt', dBm(100), 0, r'\(P_t=10\log_{10}100=§\)dBm')
chk('EN Pr', PrA, 2, r'36\log_{10}300=§\)dBm')
chk('EN margin', MA, 2, r'\(M=-100.68-(-110)=§\)dB')
chk('EN Q(1.55)', Q(1.55), 4, r'Q(9.32/6)=Q(1.55)=§\)')
chk('EN Q^-1(0.01)', Qinv(0.01), 3, r'Q^{-1}(0.01)=§\)')
chk('EN sigma < 4.30', 10 / 2.326, 2, r'\(\sigma_\psi\lt§\)dB')
chk('EN sigma^2 < 18.5', (10 / 2.326) ** 2, 1, r'below\(§\\mathrm{dB}^2\)')

# ------------------------------------------------------------------ 10. coverage of decimals
sec('10. every decimal on the page is either recomputed above or given data')
GIVEN = {  # decimals that are input data, Q-table row positions or quoted official answers (not recomputed)
    '31.5': 'mock A K_dB (prac_8 p8q2)', '3.6': 'mock A gamma (prac_8 p8q2)', '3.2': 'E1 gamma (own example)',
    '30.25': 'E1 MSE (own example)', '3.36': 'lecture p.16 MSE (learn_02)', '0.5': 'b^2 = 0.5 (own example)',
    '31.4': 'official P1Q1 K (prac_1; not reproducible)', '3.86': 'official P1Q1 gamma (prac_1)',
    '6.19': 'official P1Q1 Pout x1e-4 (prac_1)', '0.62': 'table row', '0.63': 'table row', '1.28': 'table row',
    '1.29': 'table row', '1.64': 'table row', '1.65': 'table row', '2.28': 'table row', '2.32': 'table row',
    '2.61': 'table row', '2.62': 'table row', '0.01': '1% target', '0.05': '5% target', '0.001': '0.1% target',
    '0.1': 'Q(.) <= 0.1 target', '2.29': 'table row (and the practice page reads x = 2.29)',
}
toks = re.findall(r'(?<![0-9.])-?[0-9]+\.[0-9]+', TXT)
unk = sorted({t.lstrip('-') for t in toks} - COVERED - set(GIVEN), key=float)
print(f'  {len(toks)} decimal tokens, {len({t.lstrip("-") for t in toks})} distinct; recomputed {len(COVERED)} distinct strings')
for u in unk:
    ctx = [m.start() for m in re.finditer(r'(?<![0-9.])' + re.escape(u) + r'(?![0-9])', TXT)][:1]
    snippet = TXT[max(0, ctx[0] - 40): ctx[0] + 40] if ctx else ''
    fail(f'decimal {u} not covered by any check: …{snippet}…')
if not unk:
    print('  every decimal on the page is covered')
unused = [g for g in GIVEN if g not in {t.lstrip('-') for t in toks}]
if unused:
    print('  (given-list entries not on the page any more: ' + ', '.join(unused) + ')')


# ------------------------------------------------------------------ 11. sources
sec('11. sources: quoted numbers, labels, lecturer claims, status badges')


def art(fname, aid):
    s = (SRC / 'p2build' / fname).read_text(encoding='utf-8')
    m = re.search(rf'<article class="ex" id="{aid}">(.*?)</article>', s, re.S)
    assert m, (fname, aid)
    return norm(m.group(1), True)


def need(where, text, needles):
    for nd in needles:
        k = re.sub(r'\s+', '', nd).replace('−', '-')
        if k not in text:
            fail(f'{where}: "{nd}" not in source')
        else:
            print(f'  ok   {where:<28} has "{nd}"')


p8q2 = art('prac_8.html', 'p8q2')
need('prac_8 p8q2 (模拟 A·Q2)', p8q2, ['模拟 A · Q2', 'transmits 100 mW', r'\(K_{dB}=-31.5\)', r'\(\gamma=3.6\)', 'at least −110 dBm',
                                     'standard deviation of 6 dB', 'd = 300 m', 'does not exceed 1%', '−100.68 dBm', '9.32 dB',
                                     'Q(1.55) = 0.060', '2.326 × 6 = 13.96 dB', '≈ 223 m'])
p8q7 = art('prac_8.html', 'p8q7')
need('prac_8 p8q7 (模拟 C·Q1)', p8q7, ['模拟 C · Q1', 'is −95 dBm', 'at least −105 dBm', 'standard deviation of 8 dB',
                                     'statistically independent', 'Q(1.25) = 0.106', '0.1056² = 1.12 × 10⁻²',
                                     'Q(2.28) = 0.0113、Q(2.29) = 0.0110', '2.29 × 8 ≈ 18.3 dB', '18.3 − 10 ≈ 8.3 dB'])
p1q1 = art('prac_1.html', 'p1q1')
need('prac_1 p1q1', p1q1, ['10 dB above', r'\(\gamma=3.94\)', '-30.8', '11.87', r'\(\sigma_\psi=3.45\)', 'Q(2.90)=1.85',
                           'K_dB = −31.4 dB，γ = 3.86', '6.19 × 10⁻⁴'])
tab = re.findall(r'<td>([0-9,]+)</td>\s*<td>([−-][0-9]+)</td>',
                 re.search(r'<article class="ex" id="p1q1">(.*?)</article>', (SRC / 'p2build' / 'prac_1.html').read_text(encoding='utf-8'), re.S).group(1))
dd = [int(a.replace(',', '')) for a, _ in tab][:6]
mm = [int(b.replace('−', '-')) for _, b in tab][:6]
print(f'  P1Q1 table read from prac_1.html: d = {dd}, M = {mm}')
if dd != d1 or mm != M1:
    fail('P1Q1 data used in the least-squares check differ from prac_1.html')
p1q2 = art('prac_1.html', 'p1q2')
need('prac_1 p1q2', p1q2, [r'\(\mu_\psi\) = 15 dBm', r'\(\sigma_\psi\) = 8 dBm', 'above 10 dBm', r'\(\sigma_\psi\) = 4 dBm',
                           'less than 1%', '官方答案：(a) 26%', '19.32'])
p2q2 = art('prac_2.html', 'p2q2')
need('prac_2 p2q2', p2q2, [r'\(P_{r,1}=W+Z_1', 'both', 'T is smaller than W by Δ', r'\(P_{out}=[Q(\Delta/\sigma)]^2\)',
                           r'\(Z_1=aY_1+bY\)', r'\frac{\Delta+by\sigma}{|a|\sigma}', '相关系数 ρ = b²', '0.0625',
                           '先固定 Y'])
d2324 = norm((SRC / 'exams' / 'data_2324.py').read_text(encoding='utf-8'), True)
need('data_2324 Q1(a)(ii)', d2324, ['Semester 2 Examination 2023-2024', "q='Q1(a)'",
                                    'mean value of P_r,dB is 10 dB higher than the minimum received signal power needed for non-outage',
                                    'maximum value of the variance of ψ_dB', 'outage probability lower than 1%',
                                    'σ < 10/2.33 = 4.30 dB　→　σ² < 18.5 dB²'])
shadow_finals = [f.name for f in sorted((SRC / 'exams').glob('data_*.py'))
                 if re.search(r'shadow', f.read_text(encoding='utf-8'), re.I)]
print(f'  finals that contain shadowing: {shadow_finals} (page says 期末 1/4 套)')
if shadow_finals != ['data_2324.py']:
    fail(f'shadowing finals {shadow_finals}')
l02 = norm((SRC / 'p2build' / 'learn_02.html').read_text(encoding='utf-8'), True)
need('learn_02 2.1–2.2', l02, ['简化路径损耗模型（p.8）', '路径损耗 + 阴影（p.12）', '中断概率怎么推出来（p.14–15）', '中断概率（p.15）',
                               '中断 = ψ < −x', '（p.16），对应余量 ≥ 2.33σ', 'MSE = 3.36', r'\(K_{\mathrm{dB}}=-26.67\)', 'γ = 3.97',
                               'd = 150 m', r'\(P_m=-118\)', '−113.06 − (−118) = 4.94 dB', r'\sqrt{3.36}=1.833', 'Q(2.69) ≈ 0.0036',
                               'Q(1.47) ≈ 0.071'])
l01 = norm((SRC / 'p2build' / 'learn_01.html').read_text(encoding='utf-8'), True)
need('learn_01 1.5', l01, ['考卷 Appendix A 给 Q 函数表', 'Q(−x)=1−Q(x)', 'Q(k) = 0.01 → k ≈ 2.33'])
p4q1 = art('prac_4.html', 'p4q1')
need('prac_4 p4q1', p4q1, ['讲义第 4 章 p.3–4', '被同一障碍物同时挡住的可能性小'])

notes = (SRC / 'teacher' / 'notes.py').read_text(encoding='utf-8')
W8, W9, W10 = 'Part 2 第 8 周录音', 'Part 2 第 9 周录音', 'Part 2 第 10 周录音'


def note_block(at):
    m = re.search(r"n\('(?:p2|prac)', \(" + re.escape(at) + r"\), (.*?)\]\)", notes, re.S)
    assert m, at
    return m.group(1)


claims = [  # (page text that attributes something to the lecturer, notes.py anchor, words that must be there, weeks the page cites)
    ('老师说 Q 函数表一定会考到，正查、反查都要会（第 8、9 周录音）', "'h3', '1.5'", ['Q 函数表一定会考到', '正着查和倒着查'], ['W8', 'W9']),
    ('老师说 mW 没换成 dBm 会扣分（第 8、9 周录音）', "'h3', '2.1'", ['mW 没换成 dBm 会扣分'], ['W8', 'W9']),
    ('线性和 dB 两种形式都要背，考试不给（第 8、9 周录音）', "'h3', '0.1'", ['线性和 dB 两种形式都要背，考试不给'], ['W8', 'W9']),
    ('均值 = 不含阴影的路径损耗结果，方差 = 阴影方差（第 9 周录音）', "'h3', '2.2'", ['平均路径损耗 = 不含阴影的路径损耗', '路径损耗的方差 = 阴影的方差'], ['W9']),
    ('老师要求的写法（第 9 周录音）：随机变量 < −M', "'h3', '2.2'", ['老师要求掌握的技巧', '随机变量留在左边'], ['W9']),
    ('老师说不会考积分（第 8–10 周录音）', "'chapter', 'ch0'", ['不会考积分'], ['第 8–10 周']),
    ('他讲这题的方法（第 10 周录音）', "'article', 'p2q2'", ['先把其中一个当成常数', '对它的 PDF 积分', '换元 u = y/σ'], ['W10']),
    ('老师说没写 dB ↔ 线性换算会扣分（第 8–10 周录音）', "'chapter', 'ch0'", ['没做 dB ↔ 线性换算会扣分'], ['第 8–10 周']),
    ('"10 dB above"的 10 就是 dB，不要换成线性（第 10 周录音）', "'article', 'p1q1'", ['"10 dB above"里的 10 是 dB', '不要换成线性'], ['W10']),
]
for text, at, words, weeks in claims:
    blk = note_block(at)
    srcline = blk.split(',')[0]
    for w in words:
        if w not in blk:
            fail(f'lecturer claim "{text}": "{w}" not in notes.py {at}')
    for w in weeks:
        if w not in srcline:
            fail(f'lecturer claim "{text}": week {w} not in the note source {srcline}')
    print(f'  ok   lecturer claim backed by notes.py {at:<20} {text[:40]}')
page_claims = re.findall(r'老师[^。；]*', TXT)
print(f'  lecturer attributions on the page: {len(page_claims)}')
for c in page_claims:
    print('     · ' + c[:90])

qm = (SRC / 'p2build' / 'quiz_marks.py').read_text(encoding='utf-8')
for frag_label, kind in [("'中断概率（p.15）', 'must'", 'must'), ("'简化路径损耗模型（p.8）', 'must'", 'must'),
                         ("'Q 函数（第 2 章 p.15', 'give'", 'give')]:
    if frag_label not in qm:
        fail(f'quiz_marks.py: {frag_label}')
    else:
        print(f'  ok   quiz_marks.py {frag_label}')
fms = re.findall(r'<div class="fl">(.*?)</div>', RAW)
badge = {re.sub(r'<[^>]+>', '', f).split('·')[0].strip(): re.findall(r'class="st (\w+)"', f) for f in fms}
expect = {'dBm 与 W 互换': ['def'], '简化路径损耗 + 阴影（讲义第 2 章 p.8、p.12）': ['must'], '中断概率（讲义第 2 章 p.14–15）': ['must'],
          'Q 函数、Φ 与对称性': ['give', 'def'], '倒着用：所需余量、允许的 σ、最大距离': ['def'],
          '宏分集，两路阴影独立（Practice 2 Q2(b)）': ['def'], '宏分集，两路阴影相关（Practice 2 Q2(c)）': ['give']}
for k, v in expect.items():
    got = badge.get(k)
    print(f'  {"ok  " if got == v else "FAIL"} badge {k}: {got}')
    if got != v:
        fail(f'badge {k}: {got} != {v}')

# ------------------------------------------------------------------ 12. HTML / TeX lint + structure
sec('12. HTML / TeX lint and page structure')
VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'wbr', 'col', 'source'}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.err, self.tags = [], [], []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.err.append(f'</{tag}> at {self.getpos()} but open: {self.stack[-1] if self.stack else None}')
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    break
        else:
            self.stack.pop()


p = P()
p.feed(RAW)
p.close()
for e in p.err:
    fail('tag mismatch ' + e)
for t, pos in p.stack:
    fail(f'unclosed <{t}> opened at {pos}')
print(f'  tags balanced: {not p.err and not p.stack} ({len(p.tags)} start tags)')
for bad in ('style', 'script', 'html', 'head', 'body'):
    if any(t == bad for t, _ in p.tags):
        fail(f'<{bad}> present')
tex = re.findall(r'\\\((.*?)\\\)', RAW, re.S) + re.findall(r'\\\[(.*?)\\\]', RAW, re.S)
badtex = [t for t in tex if re.search(r'[<>]|&lt;|&gt;|&amp;', t)]
for t in badtex:
    fail('raw < > or entity inside TeX: ' + t[:80])
print(f'  TeX snippets: {len(tex)}, with raw < > or entities: {len(badtex)}')
opn = len(re.findall(r'\\\(', RAW)), len(re.findall(r'\\\)', RAW)), len(re.findall(r'\\\[', RAW)), len(re.findall(r'\\\]', RAW))
if opn[0] != opn[1] or opn[2] != opn[3]:
    fail(f'unbalanced TeX delimiters {opn}')
for t in tex:
    if t.count('{') != t.count('}'):
        fail('unbalanced braces in TeX: ' + t[:80])
for envtex in tex:
    for cmd in re.findall(r'\\([A-Za-z]+)', envtex):
        if cmd not in {'mathcal', 'bar', 'text', 'min', 'mathrm', 'sim', 'psi', 'sigma', 'lt', 'gt', 'le', 'ge', 'Big', 'big', 'frac',
                       'log', 'qquad', 'Longrightarrow', 'underbrace', 'gamma', 'mu', 'iff', 'int', 'infty', 'sqrt', 'pi', 'Phi', 'Delta',
                       'cap', 'times', 'cdot', 'max', 'dfrac', 'tfrac', 'quad', 'left', 'right', 'operatorname', 'mid', 'bigl', 'bigr'}:
            fail(f'unexpected TeX command \\{cmd}')
sec_m = re.findall(r'<section class="topic" id="(t\d+)">.*?</section>', RAW, re.S)
print(f'  build_quizsum.py section regex finds: {sec_m}')
if sec_m != ['t5']:
    fail('section regex')
order = re.findall(r'<h3>(.*?)</h3>', RAW)
want_h3 = ['符号与含义 · Symbols', '公式 · Formulas', '解题步骤 · Steps', '中文例子 · 怎么用', '易错 · Traps']
print(f'  h3 order: {order}')
if order != want_h3:
    fail('h3 order')
if not re.search(r'<h2><span class="tn">5</span>[^<]+ · [^<]+</h2>', RAW):
    fail('h2 format')
meta = re.search(r'<div class="meta">(.*?)</div>', RAW, re.S).group(1)
if not re.search(r'<span class="st (must|try|give|def)">', meta) or '<span class="freq">出现：' not in meta:
    fail('meta line')
if '<p class="why">' not in RAW:
    fail('p.why missing')
sym = re.search(r'<table class="sym"><thead><tr>(.*?)</tr></thead><tbody>(.*?)</tbody></table>', RAW, re.S)
if re.findall(r'<th>(.*?)</th>', sym.group(1)) != ['符号', '中文', 'English', '含义（大白话）', '单位']:
    fail('symbol table header')
rows = re.findall(r'<tr>(.*?)</tr>', sym.group(2), re.S)
badrows = [r for r in rows if len(re.findall(r'<td>', r)) != 5]
print(f'  symbol table: {len(rows)} rows, rows without 5 cells: {len(badrows)}')
if badrows:
    fail('symbol table rows')
fm = re.findall(r'<div class="fm"><div class="fl">.*?</div><div class="fx">.*?</div><div class="fn">.*?</div></div>', RAW, re.S)
n_fm = RAW.count('<div class="fm">')
print(f'  formula cards (.fm > .fl/.fx/.fn): {len(fm)} of {n_fm}')
if len(fm) != RAW.count('<div class="fm">'):
    fail('formula card structure')
steps = re.findall(r'<table class="steps"><thead><tr>(.*?)</tr></thead><tbody>(.*?)</tbody></table></div>\s*<p class="src">', RAW, re.S)
print(f'  steps tables followed by p.src: {len(steps)} of {RAW.count("<table class=" + chr(34) + "steps" + chr(34))}')
if len(steps) != RAW.count('<table class="steps">'):
    fail('steps table without p.src')
for head, body in steps:
    th = re.findall(r'<th>(.*?)</th>', head)
    if len(th) != 4 or th[:2] != ['步骤', '做法']:
        fail(f'steps header {th}')
    for r in re.findall(r'<tr>(.*?)</tr>', body, re.S):
        if len(re.findall(r'<td>', r)) != 4:
            fail('steps row without 4 cells: ' + r[:60])
    print(f'     columns: {th[2]} | {th[3]}')
if len(steps) > 1 and len(re.findall(r'<h4>', RAW)) < len(steps):
    fail('h4 before each steps table')
egs = re.findall(r'<div class="eg"><div class="egh">(.*?)</div>\s*<p class="q">.*?</p>\s*<ol class="work">.*?</ol>\s*<p class="ans">.*?</p>\s*</div>', RAW, re.S)
print(f'  examples (.eg > .egh, p.q, ol.work, p.ans): {len(egs)} of {RAW.count("<div class=" + chr(34) + "eg" + chr(34))}: {egs}')
if not 2 <= len(egs) <= 3 or len(egs) != RAW.count('<div class="eg">'):
    fail('examples')
trap = re.search(r'<ul class="trap">(.*?)</ul>', RAW, re.S)
nt = len(re.findall(r'<li>', trap.group(1))) if trap else 0
print(f'  traps: {nt}')
if not 3 <= nt <= 6:
    fail('trap count')
en = re.search(r'<div class="en"><div class="enl">英文答题模板 · Exam English</div>(.*?)</div>\s*</section>', RAW, re.S)
if not en or '<p>' not in en.group(1):
    fail('English template')

# ------------------------------------------------------------------ summary
print('\n' + ('ALL CHECKS PASSED' if not FAIL else f'{len(FAIL)} FAILURE(S)'))
sys.exit(1 if FAIL else 0)
