#!/usr/bin/python3
"""Independent re-check of every number in frag_pathloss.html (t3 simplified path loss model, t4 least squares).

Written by the adversarial checker; it does not import or reuse check_pathloss.py.
stdlib only. Q and Q^-1 via statistics.NormalDist. The least-squares fits are solved by Cramer's rule on the
two normal equations (sum form), cross-checked against the deviation form, and confirmed to be a minimum of
F(K, gamma) by perturbing K and gamma. Free space uses Friis directly with c = 3e8 m/s.

How it checks: every line below rebuilds the text the fragment prints (numbers formatted from MY values) and
asserts that exact text is in the fragment (tags stripped, <sub>x</sub> -> _x, <sup>x</sup> -> ^x, table cells
joined by " | "). Then every number token in the fragment must be accounted for (a checked string or the given
question data). Finally the structure: balanced tags, no raw < > (or &lt; &gt;) inside TeX, no <style>/<script>,
and the required blocks of each topic section.
Run: /usr/bin/python3 _verify_pathloss.py      (exit code 1 if anything fails)
"""
import html
import pathlib
import re
import sys
from html.parser import HTMLParser
from math import floor, isclose, log10, pi, sqrt
from statistics import NormalDist

FRAG = pathlib.Path(__file__).with_name('frag_pathloss.html')
RAW = FRAG.read_text(encoding='utf-8')
N01 = NormalDist()
C = 3e8


def Q(x):
    return 1.0 - N01.cdf(x)


def Qinv(p):
    return N01.inv_cdf(1.0 - p)


def plain(s):
    s = re.sub(r'</t[dh]>\s*<t[dh][^>]*>', ' | ', s)
    s = re.sub(r'<sup>(.*?)</sup>', r'^\1', s)
    s = re.sub(r'<sub>(.*?)</sub>', r'_\1', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s).replace(' ', ' ')
    return re.sub(r'\s+', ' ', s)


TXT = plain(RAW)


def f(v, nd=2, sign=False):
    """fixed point with the typographic minus used in the fragment"""
    s = f'{v:+.{nd}f}' if sign else f'{v:.{nd}f}'
    return s.replace('-', '−')


def sciu(v, nd=None):
    """2.5×10^−10 style (plain-text form of 2.5×10<sup>−10</sup>)"""
    e = floor(log10(abs(v)))
    m = v / 10 ** e
    ms = f'{m:.{nd}f}' if nd is not None else f'{m:g}'
    return f'{ms}×10^{e}'.replace('-', '−')


def scit(v):
    """2.5\\times10^{-10} style (TeX)"""
    e = floor(log10(abs(v)))
    return f'{v / 10 ** e:g}\\times10^{{{e}}}'


def x2(v):
    """10 / 13.01 style: two decimals, trailing .00 dropped"""
    s = f'{v:.2f}'
    return s[:-3] if s.endswith('.00') else s


class Fit:
    def __init__(self, d, M, d0=1.0):
        self.d, self.M, self.d0 = d, M, d0
        x = [10 * log10(t / d0) for t in d]
        n = len(x)
        Sx, Sx2, SM, SxM = sum(x), sum(t * t for t in x), sum(M), sum(a * b for a, b in zip(x, M))
        # normal equations  n K - g Sx = SM ;  K Sx - g Sx2 = SxM   ->  Cramer on [[n, -Sx], [Sx, -Sx2]]
        det = n * (-Sx2) - (-Sx) * Sx
        K = (SM * (-Sx2) - (-Sx) * SxM) / det
        g = (n * SxM - SM * Sx) / det
        # deviation form, must agree
        xb, Mb = Sx / n, SM / n
        Sxy = sum((a - xb) * (b - Mb) for a, b in zip(x, M))
        Sxx = sum((a - xb) ** 2 for a in x)
        assert isclose(g, -Sxy / Sxx, rel_tol=1e-12) and isclose(K, Mb + g * xb, rel_tol=1e-12)
        F = lambda KK, gg: sum((b - KK + gg * a) ** 2 for a, b in zip(x, M)) / n
        for dK, dg in ((1e-3, 0), (-1e-3, 0), (0, 1e-4), (0, -1e-4), (1e-3, 1e-4), (-1e-3, -1e-4)):
            assert F(K + dK, g + dg) > F(K, g)          # really the minimum
        self.x, self.n, self.Sx, self.Sx2, self.SM, self.SxM = x, n, Sx, Sx2, SM, SxM
        self.xb, self.Mb, self.Sxy, self.Sxx, self.K, self.g = xb, Mb, Sxy, Sxx, K, g
        self.pred = [K - g * a for a in x]
        self.e = [b - p for b, p in zip(M, self.pred)]
        assert abs(sum(self.e)) < 1e-9                # residuals sum to 0
        self.sse = sum(t * t for t in self.e)
        self.mse = self.sse / n
        assert isclose(self.mse, F(K, g))


ok = bad = 0
used = []


def chk(label, text):
    global ok, bad
    used.append(text)
    if text in TXT:
        ok += 1
        print(f'  ok   {label}: {text}')
    else:
        bad += 1
        print(f'  FAIL {label}: NOT IN FRAGMENT -> {text}')


def note(label, cond, msg=''):
    global ok, bad
    if cond:
        ok += 1
        print(f'  ok   {label} {msg}')
    else:
        bad += 1
        print(f'  FAIL {label} {msg}')


# =====================================================================================================
print('== T3 symbols / formula cards')
chk('dBm 100 mW', f'100 mW = {10 * log10(100):.0f} dBm')
chk('dBm 4 W', f'4 W = 4000 mW = {10 * log10(4000):.2f} dBm')
chk('1e-3 in dB', f'10^−3 = {f(10 * log10(1e-3), 0)} dB')
chk('K -30 dB', f'−30 dB 就是 K = 10^{f(-30 / 10, 0)}')

print('== T3 steps table 1, real: 2024-25 Q1(a)(i)  (K_dB = -30 dB, gamma = 3.5, drop 88 dB)')
g25 = 3.5
B25 = 88 / (10 * g25)
chk('2425 line', f'(P_r/P_t)_dB = −30 − {10 * g25:.0f} log₁₀d（10γ = {10 * g25:.0f}）')
chk('2425 A', 'd = 1 m：log₁₀1 = 0 → A = K_dB = −30 dB')
chk('2425 B', f'{10 * g25:.0f} × B = 88 → B = log₁₀d = {B25:.2f}（d ≈ {10 ** B25:.0f} m）')
chk('2425 trap', f'按正的路径损耗理解则 A = 30 dB（那样线应该往上走），B 两种理解都是 {B25:.2f}')
chk('2425 axis honest', '原图纵轴标 Path Loss，但线往下走 → 按 (P_r/P_t)_dB 读')
chk('dB card intercept', 'P_L 是截距 −K_dB（d = d₀ = 1 m 处）、斜率 γ 的直线')

print('== T3 steps table 1, mock A.Q2  (100 mW, K_dB -31.5, d0 1 m, gamma 3.6, Pmin -110 dBm, sigma 6 dB)')
PtA = 10 * log10(100)
LA = 36 * log10(300)
PrA = PtA - 31.5 - LA
chk('A2 Pt', f'100 mW → 10 log₁₀100 = {PtA:.0f} dBm')
chk('A2 line', f'P_r = {PtA:.0f} − 31.5 − {10 * 3.6:.0f} log₁₀d（10γ = {10 * 3.6:.0f}）')
chk('A2 Pr300', f'd = 300 m：36 × {log10(300):.4f} = {LA:.2f} dB → P_r = 20 − 31.5 − {LA:.2f} = {f(PrA)} dBm')
xq = Qinv(0.01)
needT = -110 + round(xq, 3) * 6                     # with the table value 2.326
needX = -110 + xq * 6                               # with the exact inverse
allowT = PtA - 31.5 - needT
dT, dX = 10 ** (allowT / 36), 10 ** ((PtA - 31.5 - needX) / 36)
note('A2 dmax table vs exact', round(dT) == round(dX) == 223, f'table {dT:.2f} m, exact {dX:.2f} m')
chk('A2 dmax', f'中断 ≤ 1%：平均 P_r ≥ −110 + {xq:.3f} × 6 = {f(needT)} dBm；36 log₁₀d ≤ {allowT:.2f} → log₁₀d ≤ {allowT / 36:.3f} → d ≈ {dT:.0f} m')
note('A2 against prac_8 p8q2', (f(PrA), f'{allowT:.2f}', f'{allowT / 36:.3f}', f'{dT:.0f}') == ('−100.68', '84.54', '2.348', '223'))
chk('A2 src', '发射 100 mW，K_dB = −31.5 dB，d₀ = 1 m，γ = 3.6，门限 −110 dBm，阴影 σ = 6 dB')
chk('A2 trap', f'log₁₀d ≤ {allowT / 36:.3f} → d ≤ 10^{allowT / 36:.3f} ≈ {dT:.0f} m')
chk('A2 EN Pr', f'P_r = 20-31.5-36\\log_{{10}}300\\) \\(= -{-PrA:.2f}')
chk('A2 EN d', f'36 log₁₀d ≤ {allowT:.2f} gives d ≤ 10^{allowT / 36:.3f} ≈ {dT:.0f} m')
chk('A2 EN Pt', f'= 10 log₁₀100 = {PtA:.0f} dBm')

print('== T3 steps table 2: real 2023-24 Q1(a)(i) (symbolic) + mock B.Q2 fit used to draw the line')
FB = Fit([10, 20, 50, 100], [-68, -86, -91, -105])
chk('B2 line', f'M = {f(FB.K)} − {FB.g:.3f}x，x = 10 log₁₀d')
chk('B2 K', f'K_dB = {f(FB.K, 1)} dB')
chk('B2 slope', f'斜率 {f(-FB.g)} → γ = {FB.g:.2f}')
p100 = FB.K - FB.g * 20
chk('B2 d=100', f'd = 100 m（x = 20）：线上 {f(p100)} dB，实测 −105 dB，差 {f(-105 - p100)} dB')
chk('B2 src', f'最小二乘得 K_dB = {f(FB.K, 1)} dB、γ = {FB.g:.2f}')
chk('2324 (ii)', f'σ² < {(10 / xq) ** 2:.1f} dB²')
note('2324 (ii) table 2.326 gives the same', f'{(10 / 2.326) ** 2:.1f}' == f'{(10 / xq) ** 2:.1f}',
     f'(10/2.326)^2 = {(10 / 2.326) ** 2:.2f}; FYI with 2.33: 10/2.33 = {10 / 2.33:.3f} -> {(10 / 2.33) ** 2:.2f} '
     '(data_2324.py prints 10/2.33 = 4.30; its 18.5 holds for 2.326, not for 2.33)')

print('== T3 example 1: 4 W, K = 5e-4 linear, gamma 3, d0 1 m, d 200 m then 400 m')
Pt1, K1, L1 = 10 * log10(4000), 10 * log10(5e-4), 30 * log10(200)
Pr1 = Pt1 + K1 - L1
chk('e1 Pt', f'P_t = 4 W = 4000 mW → 10 log₁₀4000 = {Pt1:.2f} dBm；K_dB = 10 log₁₀(5×10^−4) = {f(K1)} dB')
chk('e1 Pr', f'30 × log₁₀200 = 30 × {log10(200):.3f} = {L1:.2f} dB；P_r = {Pt1:.2f} − {-K1:.2f} − {L1:.2f} = {f(Pr1)} dBm')
lin1 = 4 * 5e-4 * (1 / 200) ** 3
chk('e1 lin TeX', f'4\\times5\\times10^{{-4}}\\times(1/200)^3\\) \\(= {scit(4 * 5e-4)}\\times{scit((1 / 200) ** 3)}\\) \\(= {scit(lin1)}')
note('e1 lin -> dBm', f(10 * log10(lin1 * 1e3)) == f(Pr1), f'{10 * log10(lin1 * 1e3):.4f} vs {Pr1:.4f}')
chk('e1 lin mW', f'W = {sciu(lin1 * 1e3)} mW → 10 log₁₀({sciu(lin1 * 1e3)}) = {f(10 * log10(lin1 * 1e3))} dBm')
drop = 30 * log10(2)
chk('e1 (b) drop', f'10γ log₁₀2 = 30 × {log10(2):.3f} = {drop:.2f} dB')
chk('e1 (b) 1/8', f'1/2³ = 1/{2 ** 3}')
lin400 = 4 * 5e-4 * (1 / 400) ** 3
note('e1 (b) linear check', isclose(lin400, lin1 / 8) and f(10 * log10(lin400 * 1e3)) == f(Pr1 - drop))
chk('e1 (b) Pr400', f'P_r(400 m) = {f(Pr1)} − {drop:.2f} = {f(Pr1 - drop)} dBm = {sciu(lin400)} W')
chk('e1 ans', f'(a) {f(Pr1)} dBm = {sciu(lin1)} W；(b) 降 {drop:.2f} dB，即 1/8')

print('== T3 example 2: 1 W, K_dB -50 dB at d0 = 10 m, gamma 4, Pmin -100 dBm; then 2 km')
Pt2 = 10 * log10(1000)
allow2 = Pt2 - 50 + 100
chk('e2 Pt', f'P_t = 1 W = {Pt2:.0f} dBm。要求 P_r ≥ −100 dBm：{Pt2:.0f} − 50 − 40 log₁₀(d/10) ≥ −100')
chk('e2 dmax', f'40 log₁₀(d/10) ≤ {allow2:.0f} → log₁₀(d/10) ≤ {allow2 / 40:.0f} → d/10 ≤ {10 ** (allow2 / 40):.0f} → d ≤ {10 * 10 ** (allow2 / 40):.0f} m')
chk('e2 wrong d0', f'忘了除以 d₀ 会解出 d ≤ {10 ** (allow2 / 40):.0f} m')
L2 = 40 * log10(2000 / 10)
Ptn = -100 + 50 + L2
chk('e2 (b)', f'40 log₁₀(2000/10) = 40 × {log10(200):.3f} = {L2:.2f} dB；P_t ≥ −100 + 50 + {L2:.2f} = {Ptn:.2f} dBm')
Wn = 10 ** (Ptn / 10)
chk('e2 (b) W', f'10^{Ptn:.2f}/10 mW = {Wn:,.0f} mW = {Wn / 1e3:.1f} W'.replace(',', ' '))
chk('e2 (b) x16', f'40 log₁₀2 = {40 * log10(2):.2f} dB，功率要 ×{10 ** (4 * log10(2)):.0f}')
chk('e2 ans', f'(a) d_max = {10 * 10 ** (allow2 / 40):.0f} m；(b) P_t ≥ {Ptn:.2f} dBm ≈ {Wn / 1e3:.1f} W')
chk('e2 trap', f'例 2 忘了会把 {10 * 10 ** (allow2 / 40):.0f} m 算成 {10 ** (allow2 / 40):.0f} m')

print('== T3 example 3: graph 40 dB at log d = 0, 145 dB at log d = 3; Pt 20 dBm at 200 m; free space 2 GHz')
sl = (145 - 40) / 3
g3 = sl / 10
chk('e3 (a)', f'P_L(1 m) = −K_dB = 40 dB → K_dB = −40 dB。斜率：(145 − 40)/3 = {sl:.0f} dB/十倍距离 = 10γ → γ = {g3:.1f}')
PL3 = 40 + 10 * g3 * log10(200)
chk('e3 (b)', f'P_L(200 m) = 40 + 35 log₁₀200 = 40 + 35 × {log10(200):.3f} = 40 + {10 * g3 * log10(200):.2f} = {PL3:.2f} dB；P_r = 20 − {PL3:.2f} = {f(20 - PL3)} dBm')
lam = C / 2e9
arg = 4 * pi * 200 / lam
PLfs = 20 * log10(arg)
note('e3 Friis direct', isclose(20 + 20 * log10(lam / (4 * pi * 200)), 20 - PLfs), '(20 log of the amplitude ratio, not 10 log)')
chk('e3 (c)', (f'λ = c/f = 3×10^8/2×10^9 = {lam:.3f} m；P_L = 20 log₁₀(4πd/λ) = 20 log₁₀(4π × 200/{lam:.3f}) = '
               f'20 log₁₀({arg:,.0f}) = {PLfs:.2f} dB → P_r = 20 − {PLfs:.2f} = {f(20 - PLfs)} dBm').replace(',', ' '))
dif = PL3 - PLfs
chk('e3 diff', f'两者差 {PL3:.2f} − {PLfs:.2f} ≈ {dif:.1f} dB，约 {10 ** (dif / 10) / 1e3:.1f}×10³ 倍')
chk('e3 ans', f'(a) K_dB = −40 dB，γ = {g3:.1f}；(b) {f(20 - PL3)} dBm；(c) {f(20 - PLfs)} dBm，高估约 {dif:.0f} dB')

print('== T3 traps: focused Q1 (p8q10) gap at 1 km, per-decade slopes')
fs1k = 30 + 20 * log10((C / 900e6) / (4 * pi * 1000))
sp1k = 30 - 31.5 - 35 * log10(1000)
chk('trap gap', f'专项 Q1 里 1 km 处两者差约 {fs1k - sp1k:.0f} dB')
chk('trap decade', f'自由空间每十倍距离只降 {20 * log10(10):.0f} dB，γ = 3.5 时降 {35 * log10(10):.0f} dB')
chk('trap 10γ', f'γ = 3.6 时距离项是 {10 * 3.6:.0f} log₁₀d，不是 3.6 log₁₀d')

# =====================================================================================================
print('== T4 steps table: Practice 1 Q1 (6 points) vs mock B.Q2 (4 points)')
F1 = Fit([5, 25, 65, 110, 400, 1000], [-60, -80, -105, -115, -130, -150])
chk('P1 x', 'd = 5、25、65、110、400、1000 m → x = ' + '、'.join(f'{t:.2f}' for t in F1.x))
chk('P1 means', f'\\(\\bar x\\) = {F1.xb:.2f}，\\(\\bar M\\) = {f(F1.SM, 0)}/6 = {f(F1.Mb)}')
chk('P1 S', f'S_xy = {f(F1.Sxy)}，S_xx = {F1.Sxx:.2f}')
chk('P1 gamma', f'{-F1.Sxy:.2f}/{F1.Sxx:.2f} = {F1.g:.2f}')
chk('P1 K', f'{f(F1.Mb)} + {F1.g:.3f} × {F1.xb:.2f} = {f(F1.K)} dB')
chk('P1 e', 'e = ' + '、'.join(f(t, 2, True) for t in F1.e) + f'；Σe² = {F1.sse:.2f} → σ² = {F1.sse:.2f}/6 = {F1.mse:.2f} dB²')
s1 = sqrt(F1.mse)
chk('P1 Pout', (f'σ = {s1:.2f} dB，余量 10 dB：Q(10/{s1:.2f}) = Q({10 / s1:.2f}) = {sciu(Q(round(10 / s1, 2)), 2)}'
                f'（查表；参数不舍入为 {sciu(Q(10 / s1), 2)}）'))
note('P1 against prac_1.html', (f'{F1.g:.2f}', f'{F1.K:.2f}', f'{F1.sse:.2f}', f'{F1.mse:.2f}', f'{s1:.2f}')
     == ('3.94', '-30.79', '71.23', '11.87', '3.45'), '(prac_1: gamma 3.94, K -30.79, SSE 71.23, MSE 11.87, sigma 3.45)')
chk('P1 src data', 'd = 5、25、65、110、400、1000 m，(P_r/P_t)_dB = −60、−80、−105、−115、−130、−150 dB')
FBx = ' '.join(x2(t) for t in FB.x)
chk('B x', 'd = 10、20、50、100 m → x = ' + '、'.join(x2(t) for t in FB.x))
chk('B means', f'\\(\\bar x\\) = {FB.xb:.2f}，\\(\\bar M\\) = {f(FB.SM, 0)}/4 = {f(FB.Mb)}')
chk('B S', f'S_xy = {f(FB.Sxy)}，S_xx = {FB.Sxx:.2f}')
chk('B gamma', f'{-FB.Sxy:.2f}/{FB.Sxx:.2f} = {FB.g:.2f}')
chk('B K', f'{f(FB.Mb, 1)} + {FB.g:.3f} × {FB.xb:.0f} = {f(FB.K)} dB')
chk('B e', 'e = ' + '、'.join(f(t, 2, True) for t in FB.e) + f'；Σe² = {FB.sse:.2f} → σ² = {FB.sse:.2f}/4 = {FB.mse:.2f} dB²')
sB = sqrt(FB.mse)
chk('B Pout', f'σ = {sB:.2f} dB，余量 8 dB：Q(8/{sB:.2f}) = Q({8 / sB:.2f}) = {sciu(Q(round(8 / sB, 2)), 2)}')
note('B Pout exact arg', sciu(Q(8 / sB), 2) == sciu(Q(round(8 / sB, 2)), 2), f'exact Q({8 / sB:.4f}) = {Q(8 / sB):.4e}')
chk('B src data', '(P_r/P_t)_dB = −68、−86、−91、−105 dB，(c) 余量 8 dB')
chk('B EN gamma', f'so \\(\\gamma = {-FB.Sxy:.2f}/{FB.Sxx:.2f} = {FB.g:.2f}\\)')
chk('B EN K', f'\\(= -87.5 + {FB.g:.3f}\\times15\\) \\(= {f(FB.K).replace("−", "-")}\\) dB')
chk('B EN sigma', f'\\(\\sigma_\\psi^2 = {FB.sse:.2f}/4 = {FB.mse:.2f}\\) dB², so \\(\\sigma_\\psi = {sB:.2f}\\) dB')
chk('B EN Pout', f'\\(P_{{\\mathrm{{out}}}} = Q(8/{sB:.2f})\\) \\(= Q({8 / sB:.2f}) = {Q(round(8 / sB, 2)) * 1e3:.2f}\\times10^{{-3}}\\)')

print('== T4 example 1: d = 5, 50, 500, 5000 m; M = -56, -92, -118, -155 dB; margin 5 dB')
E1 = Fit([5, 50, 500, 5000], [-56, -92, -118, -155])
chk('e1 x', (f'10 log₁₀5 = {10 * log10(5):.2f}，d 每 ×10，x 加 10 → x = ' + '、'.join(f'{t:.2f}' for t in E1.x)
             + f'；\\(\\bar x\\) = {E1.xb:.2f}，\\(\\bar M\\) = (−56 − 92 − 118 − 155)/4 = {f(E1.SM, 0)}/4 = {f(E1.Mb)}'))
for dd, xx, MM in zip(E1.d, E1.x, E1.M):
    dx, dm = xx - E1.xb, MM - E1.Mb
    chk(f'e1 row {dd}', f'{dd} | {xx:.2f} | {f(MM, 0)} | {f(dx, 0, True) if dx > 0 else f(dx, 0)} | {f(dm, 2, True)} | {f(dx * dm)} | {dx * dx:.0f}')
chk('e1 sums', f'\\(\\bar x\\) = {E1.xb:.2f} | \\(\\bar M\\) = {f(E1.Mb)} | 0 | 0 | S_xy = {f(E1.Sxy, 0)} | S_xx = {E1.Sxx:.0f}')
chk('e1 gamma K', f'1615/500 = {E1.g:.2f}；K_dB = \\(\\bar M\\) + γ\\(\\bar x\\) = {f(E1.Mb)} + {E1.g:.2f} × {E1.xb:.2f} = {f(E1.K)} dB')
note('e1 S exact', isclose(-E1.Sxy, 1615, abs_tol=1e-9) and isclose(E1.Sxx, 500, abs_tol=1e-9))
chk('e1 pred line', f'预测 \\(\\hat M\\) = {f(E1.K)} − {E1.g:.2f}x')
for dd, xx, pp, MM, ee in zip(E1.d, E1.x, E1.pred, E1.M, E1.e):
    chk(f'e1 resid {dd}', f'{dd} | {E1.g * xx:.2f} | {f(pp)} | {f(MM, 0)} | {f(ee, 2, True)} | {ee * ee:.2f}')
chk('e1 SSE', f'0（自检通过） | {E1.sse:.2f}')
sE = sqrt(E1.mse)
chk('e1 sigma', f'σ_ψ² = {E1.sse:.2f}/4 = {E1.mse:.3f} dB²，σ_ψ = √{E1.mse:.3f} = {sE:.2f} dB')
chk('e1 Pout', f'P_out = Q(5/{sE:.3f}) = Q({5 / sE:.2f}) = {Q(round(5 / sE, 2)):.4f}，约 {100 * Q(round(5 / sE, 2)):.1f}%')
note('e1 Pout exact arg', f'{Q(5 / sE):.3f}' == '0.017', f'exact Q({5 / sE:.4f}) = {Q(5 / sE):.5f}')
chk('e1 ans', f'γ = {E1.g:.2f}，K_dB = {f(E1.K)} dB；σ_ψ² = {E1.mse:.3f} dB²（σ = {sE:.2f} dB）；P_out ≈ {Q(round(5 / sE, 2)):.4f}')

print('== T4 example 2: Pt 1 W, d0 = 10 m, d = 20, 100, 500 m, Pr = -40, -61, -88 dBm (sum form)')
Pt = 10 * log10(1000)
E2 = Fit([20, 100, 500], [p - Pt for p in (-40, -61, -88)], d0=10)
chk('e2 M x', ('P_t = 1 W = 30 dBm，M = P_r − P_t = ' + '、'.join(f(t, 0) for t in E2.M)
             + ' dB。横坐标用 d/d₀：x = 10 log₁₀(20/10)、10 log₁₀(100/10)、10 log₁₀(500/10) = '
             + '、'.join(f'{t:.4f}' for t in E2.x)))
for dd, MM, xx in zip(E2.d, E2.M, E2.x):
    chk(f'e2 row {dd}', f'{dd} | {f(MM, 0)} | {xx:.4f} | {xx * xx:.3f} | {f(xx * MM, 3)}')
chk('e2 sums', f'Σ | {f(E2.SM, 0)} | {E2.Sx:.4f} | {E2.Sx2:.3f} | {f(E2.SxM, 3)}')
num = E2.n * E2.SxM - E2.Sx * E2.SM
den = E2.n * E2.Sx2 - E2.Sx ** 2
chk('e2 num', f'3 × ({f(E2.SxM, 3)}) − 30 × ({f(E2.SM, 0)}) = {f(E2.n * E2.SxM)} + {-E2.Sx * E2.SM:.2f} = {f(num)}')
chk('e2 den', f'3 × {E2.Sx2:.3f} − 30² = {E2.n * E2.Sx2:.2f} − {E2.Sx ** 2:.2f} = {den:.2f}')
chk('e2 gamma', f'−γ = {f(num)}/{den:.2f} = {f(num / den, 4)} → γ = {E2.g:.2f}')
note('e2 gamma same both forms', isclose(-num / den, E2.g))
chk('e2 K', (f'K_dB = (ΣM + γΣx)/n = ({f(E2.SM, 0)} + {E2.g:.4f} × 30)/3 = ({f(E2.SM, 0)} + {E2.g * E2.Sx:.2f})/3 = '
             f'{f(E2.SM + E2.g * E2.Sx)}/3 = {f(E2.K)} dB'))
chk('e2 resid', ('预测 ' + '、'.join(f(t) for t in E2.pred) + '，e = ' + '、'.join(f(t, 2, True) for t in E2.e)
                 + f'（和为 0）；σ_ψ² = (1 + 4 + 1)/3 = {E2.mse:.2f} dB²，σ_ψ = {sqrt(E2.mse):.2f} dB'))
note('e2 e^2 = 1, 4, 1', [round(t * t, 6) for t in E2.e] == [1.0, 4.0, 1.0])
chk('e2 ans', f'K_dB = {f(E2.K)} dB（d₀ = 10 m），γ = {E2.g:.2f}，σ_ψ = {sqrt(E2.mse):.2f} dB')
E2w = Fit(E2.d, E2.M, d0=1.0)                       # trap: forgot d0 = 10 m
note('e2 trap gamma unchanged', isclose(E2w.g, E2.g))
chk('e2 trap', f'γ 不变（{E2w.g:.2f}），K_dB 却变成 {f(E2w.K)} dB')

print('== T4 example 3: n = 5, SSE = 101.25 dB^2, margin 9 dB, target 1 %')
m3 = 101.25 / 5
s3 = sqrt(m3)
chk('e3 sigma', f'σ_ψ² = 101.25/5 = {m3:.2f} dB²，σ_ψ = √{m3:.2f} = {s3:.2f} dB')
chk('e3 Pout', f'P_out = Q(9/{s3:.2f}) = Q({9 / s3:.2f}) = {Q(9 / s3):.4f}')
chk('e3 1%', f'Q(x) = 0.01 → x = {xq:.3f}，余量至少 {xq:.3f} × {s3:.2f} = {round(xq, 3) * s3:.2f} dB，比现在的 9 dB 还差 {round(xq, 3) * s3 - 9:.2f} dB')
note('e3 1% exact inverse', f'{xq * s3 - 9:.2f}' == f'{round(xq, 3) * s3 - 9:.2f}', f'exact {xq * s3:.3f}')
w3 = 101.25 / 3
chk('e3 wrong n-2', f'除以 n − 2 = 3 得 {w3:.2f} dB²、σ = {sqrt(w3):.2f} dB，Q(9/{sqrt(w3):.2f}) = Q({9 / sqrt(w3):.2f}) = {Q(round(9 / sqrt(w3), 2)):.4f}')
note('e3 wrong n-2 exact', f'{Q(9 / sqrt(w3)):.3f}' == f'{Q(round(9 / sqrt(w3), 2)):.3f}', f'exact Q({9 / sqrt(w3):.4f}) = {Q(9 / sqrt(w3)):.4f}')
chk('e3 wrong var', f'Q(9/{m3:.2f}) = Q({9 / m3:.2f}) = {Q(round(9 / m3, 2)):.3f}')
chk('e3 ans', f'σ_ψ² = {m3:.2f} dB²，σ_ψ = {s3:.2f} dB；P_out ≈ {Q(9 / s3):.4f}；还要再提高约 {round(xq, 3) * s3 - 9:.2f} dB')

print('== T4 traps: log10 d axis, official P1Q1 answer put back, lecturer MSE 9.656')
chk('trap log axis', f'会算出 γ = {10 * F1.g:.1f}，大了 10 倍')
off = sum((b - (-31.4 - 3.86 * a)) ** 2 for a, b in zip(F1.x, F1.M)) / 6
chk('trap official MSE', f'MSE = {off:.1f}，比最小二乘的 {F1.mse:.2f} 还大')
chk('trap 9.656', f'MSE = 9.656（10/√9.656 = {10 / sqrt(9.656):.2f}，老师取 3.23，查 Q(3.23)）')
note('Q(3.23) = 6.19e-4', sciu(Q(3.23), 2) == '6.19×10^−4', sciu(Q(3.23), 2))
chk('trap official nums', 'K = −31.4 dB、γ = 3.86、P_out = 6.19×10^−4')
chk('trap own nums', f'K ≈ {f(F1.K, 1)} dB、γ ≈ {F1.g:.2f}、σ² ≈ {F1.mse:.2f} dB²')

print('== question texts of my own examples carry exactly the inputs used above')
chk('t3 e1 q', '发射功率 4 W，简化路径损耗模型 K = 5×10^−4（线性值），γ = 3，d₀ = 1 m。(a) 求 200 m 处的接收功率')
chk('t3 e1 q2', '(b) 距离加倍到 400 m')
chk('t3 e2 q', '发射功率 1 W，K_dB = −50 dB（在 d₀ = 10 m 处定的），γ = 4，接收机最低需要 −100 dBm')
chk('t3 e2 q2', '(b) 要覆盖 2 km')
chk('t3 e3 q', 'd = 1 m（log₁₀d = 0）处 P_L = 40 dB，log₁₀d = 3 处 P_L = 145 dB。(a) 求 K_dB 和 γ。(b) P_t = 20 dBm，求 200 m 处的 P_r')
chk('t3 e3 q2', '（f = 2 GHz，G_t = G_r = 1）算 200 m 处的 P_r')
chk('t4 e1 q', '在 d = ' + '、'.join(str(t) for t in E1.d) + ' m 处测得 (P_r/P_t)_dB = ' + '、'.join(f(t, 0) for t in E1.M)
    + ' dB，d₀ = 1 m')
chk('t4 e1 q2', '比门限高 5 dB，求中断概率')
chk('t4 e2 q', f'发射功率 1 W，参考距离 d₀ = {E2.d0:.0f} m。在 ' + '、'.join(str(t) for t in E2.d) + ' m 处测得接收功率 '
    + '、'.join(f(t + Pt, 0) for t in E2.M) + ' dBm')
chk('t4 e3 q', '用 5 个测量点拟合简化路径损耗模型，残差平方和 Σe_i² = 101.25 dB²')
chk('t4 e3 q2', '平均接收功率比门限高 9 dB 时的中断概率？(c) 要把中断概率降到 1%')

# =====================================================================================================
print('== number inventory: every number token in the fragment must come from a checked string or the givens')
# question givens (data of the cited questions and of my own examples) and structural integers
# (years, page numbers p.4-p.15, section 2.1, Q numbers, small counts); everything else must be in a checked string
GIVEN = set('''0 1 2 3 4 5 6 7 8 9 10 12 13 15 2023 24 2024 25 2.1
3.5 3.6 31.5 88 100 110 300 30 1000 2000 50 40 145 200 20 3.86 31.4 9.656 101.25'''.split())
acc = set(GIVEN)
for t in used:
    acc |= set(re.findall(r'\d+(?:\.\d+)?', t))
tokens = re.findall(r'\d+(?:\.\d+)?', TXT)
miss = sorted({t for t in tokens if t not in acc}, key=lambda s: float(s))
decs = sorted({t for t in tokens if '.' in t}, key=float)
print(f'  {len(tokens)} number tokens, {len(decs)} distinct decimals; unaccounted: {miss if miss else "none"}')
if miss:
    bad += 1

# =====================================================================================================
print('== structure')
VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'wbr', 'col'}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.err = [], []

    def handle_starttag(self, tag, a):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            self.err.append(f'line {self.getpos()[0]}: </{tag}> but open is {self.stack[-1] if self.stack else None}')
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    break
        else:
            self.stack.pop()


p = P()
p.feed(RAW)
p.close()
note('tags balanced', not p.err and not p.stack, f'errors {p.err} unclosed {p.stack}')
note('no style/script/html/head/body', not re.search(r'<(style|script|html|head|body)\b', RAW, re.I))
tex = re.findall(r'\\\((.*?)\\\)', RAW, re.S) + re.findall(r'\\\[(.*?)\\\]', RAW, re.S)
badtex = [t for t in tex if re.search(r'[<>]|&lt;|&gt;', t)]
note('no raw < > in TeX', not badtex, f'{len(tex)} TeX blocks; offenders: {badtex[:3]}')
note('TeX delimiters paired', RAW.count('\\(') == RAW.count('\\)') and RAW.count('\\[') == RAW.count('\\]'))
SYM_HEAD = '<thead><tr><th>符号</th><th>中文</th><th>English</th><th>含义（大白话）</th><th>单位</th></tr></thead>'
for sec in re.finditer(r'<section class="topic" id="(t\d+)">(.*?)</section>', RAW, re.S):
    sid, body = sec.group(1), sec.group(2)
    egs = re.findall(r'<div class="eg">(.*?)\n  </div>', body, re.S)
    traps = re.search(r'<ul class="trap">(.*?)</ul>', body, re.S)
    ntrap = len(re.findall(r'<li>', traps.group(1))) if traps else 0
    steps = re.findall(r'<table class="steps"><thead><tr><th>步骤</th><th>做法</th><th>[^<]+</th><th>[^<]+</th></tr></thead>.*?</table></div>\s*<p class="src">', body, re.S)
    checks = {
        'h2 tn': re.search(rf'<h2><span class="tn">{sid[1:]}</span>[^<]+ · [^<]+</h2>', body),
        'meta st+freq': re.search(r'<div class="meta">(<span class="st (must|try|give|def)">[^<]+</span>)+<span class="freq">出现：', body),
        'why': '<p class="why">' in body,
        'h3 sym': '<h3>符号与含义 · Symbols</h3>' in body and SYM_HEAD in body,
        'h3 fm': '<h3>公式 · Formulas</h3>' in body and body.count('<div class="fm"><div class="fl">') >= 1,
        'fm parts': body.count('<div class="fm">') == body.count('<div class="fx">') == body.count('<div class="fn">'),
        'h3 steps + src': '<h3>解题步骤 · Steps</h3>' in body and len(steps) >= 1 and len(steps) == body.count('<table class="steps">'),
        'h4 when 2 tables': body.count('<table class="steps">') < 2 or body.count('<h4>') >= body.count('<table class="steps">'),
        'h3 eg': '<h3>中文例子 · 怎么用</h3>' in body,
        '2-3 eg complete': 2 <= len(egs) <= 3 and all(all(k in e for k in ('<div class="egh">', '<p class="q">', '<ol class="work">', '<p class="ans">')) for e in egs),
        'traps 3-6': '<h3>易错 · Traps</h3>' in body and 3 <= ntrap <= 6,
        'en': re.search(r'<div class="en"><div class="enl">英文答题模板 · Exam English</div>', body),
    }
    for k, v in checks.items():
        note(f'{sid} {k}', bool(v), f'(eg {len(egs)}, traps {ntrap}, steps tables {len(steps)})' if k in ('2-3 eg complete', 'traps 3-6', 'h3 steps + src') else '')

print(f'\nRESULT: {ok} ok, {bad} failed')
sys.exit(1 if bad else 0)
