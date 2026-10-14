#!/usr/bin/python3
"""Static Rician-fading figure for Part 2 section 2.3 (LOS + scatter phasors, PDF family, envelope K=0 vs K=10).

Writes rician_fig.txt (HTML snippet); deterministic. Total power normalised to 1 (Zrms = 1):
s^2 = K/(K+1), 2*sigma^2 = 1/(K+1).
"""
import math, pathlib, random

B = pathlib.Path(__file__).parent
rnd = random.Random(4)
RHO = 0.3

def i0e(x):
    if x < 15:
        s = t = 1.0
        for k in range(1, 80):
            t *= (x / 2) ** 2 / (k * k); s += t
            if t < 1e-14 * s: break
        return s * math.exp(-x)
    return (1 + 1 / (8 * x) + 9 / (128 * x * x)) / math.sqrt(2 * math.pi * x)

def pdf(z, K):
    s2 = 1 / (K + 1) / 2; s = math.sqrt(K / (K + 1))
    return 0.0 if z <= 0 else z / s2 * math.exp(-(z - s) ** 2 / (2 * s2)) * i0e(z * s / s2)

def cdf(r, K, n=2000):
    return sum(pdf((i + 0.5) / n * r, K) * r / n for i in range(n))

def arrow(x0, y0, x1, y1, style, w):
    a = math.atan2(y1 - y0, x1 - x0); L = min(8, math.hypot(x1 - x0, y1 - y0) * 0.5)
    return (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" style="stroke:{style}" stroke-width="{w}"/>'
            f'<path d="M{x1:.1f} {y1:.1f} L{x1-L*math.cos(a-0.4):.1f} {y1-L*math.sin(a-0.4):.1f} L{x1-L*math.cos(a+0.4):.1f} {y1-L*math.sin(a+0.4):.1f}Z" style="fill:{style}"/>')

# ---- 1. phasors, K = 4 (6 dB, as on slide p.28)
K1 = 4
W1, H1 = 300, 250
s = math.sqrt(K1 / (K1 + 1)); sg = math.sqrt(1 / (K1 + 1))
ph = [rnd.random() * 2 * math.pi for _ in range(10)]; am = [0.6 + 0.8 * rnd.random() for _ in range(10)]
nrm = math.sqrt(sum(a * a for a in am))
pts = [(0.0, 0.0), (s, 0.0)]
for am_, p_ in zip(am, ph):
    r = am_ / nrm * sg * 1.1
    pts.append((pts[-1][0] + r * math.cos(p_), pts[-1][1] + r * math.sin(p_)))
xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
sc = min((W1 - 50) / (max(xs) - min(xs)), (H1 - 80) / max(1e-9, max(ys) - min(ys)))
ox = 25 - sc * min(xs) + ((W1 - 50) - sc * (max(xs) - min(xs))) / 2
oy = 34 + sc * max(ys) + ((H1 - 80) - sc * (max(ys) - min(ys))) / 2
Pp = lambda q: (ox + sc * q[0], oy - sc * q[1])
parts = [f'<line x1="8" y1="{oy:.1f}" x2="{W1-8}" y2="{oy:.1f}" style="stroke:var(--line-strong)" stroke-width="0.8"/>',
         f'<line x1="{ox:.1f}" y1="12" x2="{ox:.1f}" y2="{H1-24}" style="stroke:var(--line-strong)" stroke-width="0.8"/>']
parts.append(arrow(*Pp(pts[0]), *Pp(pts[1]), 'var(--good)', 3))
for q0, q1 in zip(pts[1:], pts[2:]):
    parts.append(arrow(*Pp(q0), *Pp(q1), 'var(--ink-faint)', 1.2))
parts.append(arrow(*Pp(pts[0]), *Pp(pts[-1]), 'var(--key)', 2.6))
parts.append(f'<text x="{ox+6:.1f}" y="{oy+16:.1f}" font-size="11" style="fill:var(--good)">直射波 s（固定）</text>')
parts.append(f'<text x="12" y="{H1-8}" font-size="12" style="fill:var(--key)">合成包络 z = {math.hypot(*pts[-1]):.2f}</text>')
parts.append(f'<text x="{W1-96}" y="{H1-8}" font-size="11" style="fill:var(--ink-soft)">K = 4（6 dB）</text>')
svg1 = f'<svg viewBox="0 0 {W1} {H1}" role="img" aria-label="一条固定的直射波加上十条相位随机的散射波，合成包络在直射波附近小幅摆动">' + ''.join(parts) + '</svg>'

# ---- 2. PDF family
KS = [(0, 'var(--ink-faint)', 'K = 0（瑞利）', '5 4'), (1, 'var(--extra)', 'K = 1（0 dB）', ''), (4, 'var(--accent)', 'K = 4（6 dB）', ''), (10, 'var(--good)', 'K = 10（10 dB）', '')]
W2, H2 = 320, 250
L2, R2, T2, Bt2, zmax = 34, W2 - 10, 14, H2 - 32, 2.0
pmax = max(pdf(zmax * i / 300, K) for K, *_ in KS for i in range(1, 301)) * 1.06
X = lambda z: L2 + z / zmax * (R2 - L2); Y = lambda v: Bt2 - v / pmax * (Bt2 - T2)
parts = [f'<line x1="{L2}" y1="{Bt2}" x2="{R2}" y2="{Bt2}" style="stroke:var(--line-strong)"/>',
         f'<line x1="{L2}" y1="{T2}" x2="{L2}" y2="{Bt2}" style="stroke:var(--line-strong)"/>',
         f'<text x="4" y="{T2+4}" font-size="11" style="fill:var(--ink-soft)">p(z)</text>',
         f'<text x="{R2-58}" y="{H2-6}" font-size="11" style="fill:var(--ink-soft)">z / Z_rms</text>']
for z in (0, 0.5, 1, 1.5, 2):
    parts.append(f'<text x="{X(z)-7:.1f}" y="{Bt2+14}" font-size="11" style="fill:var(--ink-soft)">{z:g}</text>')
for i, (K, col, lab, dash) in enumerate(KS):
    d = 'M' + ' L'.join(f'{X(zmax*j/300):.1f} {Y(pdf(zmax*j/300, K)):.1f}' for j in range(301))
    parts.append(f'<path d="{d}" style="fill:none;stroke:{col}" stroke-width="{1.6 if dash else 2.2}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    parts.append(f'<line x1="{L2+8}" y1="{T2+10+i*15}" x2="{L2+26}" y2="{T2+10+i*15}" style="stroke:{col}" stroke-width="2"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    parts.append(f'<text x="{L2+30}" y="{T2+14+i*15}" font-size="11" style="fill:var(--ink-soft)">{lab}</text>')
parts.append(f'<line x1="{X(RHO):.1f}" y1="{T2+70}" x2="{X(RHO):.1f}" y2="{Bt2}" style="stroke:var(--key)" stroke-dasharray="4 3" stroke-width="1.2"/>')
parts.append(f'<text x="{X(RHO)+3:.1f}" y="{Bt2-6}" font-size="10.5" style="fill:var(--key)">ρ = 0.3</text>')
svg2 = f'<svg viewBox="0 0 {W2} {H2}" role="img" aria-label="不同 K 的莱斯分布：K = 0 是瑞利，K 越大曲线越窄、越集中在 1 附近，靠近 0 的部分越小">' + ''.join(parts) + '</svg>'

# ---- 3. envelope over time, same scatter, K = 0 vs K = 10
M, fm, NS = 16, 20, 800
th = [2 * math.pi * (i + rnd.random()) / M for i in range(M)]
phs = [(rnd.random() * 2 * math.pi, rnd.random() * 2 * math.pi) for _ in range(M)]
SC = []
for k in range(NS):
    t = k / NS; I = Q = 0.0
    for i in range(M):
        w = 2 * math.pi * fm * math.cos(th[i]) * t
        I += math.cos(w + phs[i][0]); Q += math.sin(w + phs[i][1])
    SC.append((I, Q))
rms = math.sqrt(sum(I * I + Q * Q for I, Q in SC) / NS); SC = [(I / rms, Q / rms) for I, Q in SC]
def env(K):
    s = math.sqrt(K / (K + 1)); g = math.sqrt(1 / (K + 1)); out = []
    for k, (I, Q) in enumerate(SC):
        a = 2 * math.pi * fm * 0.5 * k / NS
        out.append(20 * math.log10(max(1e-4, math.hypot(s * math.cos(a) + g * I, s * math.sin(a) + g * Q))))
    return out
e0, e10 = env(0), env(10)
W3, H3 = 660, 200
L3, R3, T3, Bt3, lo, hi = 46, W3 - 10, 10, H3 - 26, -35, 10
Yd = lambda d: T3 + (hi - max(lo, min(hi, d))) / (hi - lo) * (Bt3 - T3); Xk = lambda k: L3 + k / (NS - 1) * (R3 - L3)
parts = []
for d in (10, 0, -10, -20, -30):
    parts.append(f'<line x1="{L3}" y1="{Yd(d):.1f}" x2="{R3}" y2="{Yd(d):.1f}" style="stroke:var(--line)" stroke-width="0.8"/>')
    parts.append(f'<text x="4" y="{Yd(d)+4:.1f}" font-size="11" style="fill:var(--ink-soft)">{d} dB</text>')
parts.append('<path d="M' + ' L'.join(f'{Xk(i):.1f} {Yd(e0[i]):.1f}' for i in range(NS)) + '" style="fill:none;stroke:var(--ink-faint)" stroke-width="1.1"/>')
parts.append('<path d="M' + ' L'.join(f'{Xk(i):.1f} {Yd(e10[i]):.1f}' for i in range(NS)) + '" style="fill:none;stroke:var(--good)" stroke-width="1.9"/>')
thr = 20 * math.log10(RHO)
parts.append(f'<line x1="{L3}" y1="{Yd(thr):.1f}" x2="{R3}" y2="{Yd(thr):.1f}" style="stroke:var(--key)" stroke-dasharray="5 4" stroke-width="1.3"/>')
parts.append(f'<text x="{R3-64}" y="{H3-6}" font-size="11" style="fill:var(--ink-soft)">时间 → 1 s</text>')
svg3 = f'<svg viewBox="0 0 {W3} {H3}" role="img" aria-label="同一组散射波下，没有直射波时包络深跌到 −30 dB，加了 K = 10 的直射波后只在 0 dB 上下几 dB 摆动">' + ''.join(parts) + '</svg>'

P = {K: cdf(RHO, K) for K in (0, 1, 4, 10)}
html = f'''<div class="figwrap">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;align-items:start">
<div>{svg1}<div class="cap">① 绿色直射波长度固定；灰色散射波相位随机，只能让合成箭头（橙色）在直射波的箭头尖附近摆动，很难抵消到 0。</div></div>
<div>{svg2}<div class="cap">② 总功率都归一化为 1。K 越大，曲线越窄、越集中在 z ≈ 1，靠近 0（深衰落）的部分越小；K → ∞ 时趋于一根尖峰，就是不衰落（讲义 p.28 的图）。</div></div>
</div>
<div style="margin-top:14px">{svg3}<div class="cap">③ 同一组散射波：灰色是没有直射波（瑞利，K = 0），绿色是加了直射波（K = 10）。瑞利下包络多次跌破门限（橙色虚线，ρ = 0.3），K = 10 时只在 0 dB 上下几 dB 摆动。</div></div>
</div>'''
(B / 'rician_fig.txt').write_text(html, encoding='utf-8')
print({K: round(v, 6) for K, v in P.items()}, 'e10 min', round(min(e10), 1), 'e0 min', round(min(e0), 1))
