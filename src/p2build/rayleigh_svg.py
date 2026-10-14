#!/usr/bin/python3
"""Static Rayleigh-fading figure for Part 2 section 2.3 (phasor sum, PDF, envelope over time).

Writes rayleigh_fig.txt (an HTML snippet); deterministic (fixed seed).
"""
import math, pathlib, random

B = pathlib.Path(__file__).parent
rnd = random.Random(4)
RHO = 0.3                      # threshold Zmin / Zrms
THR_DB = 20 * math.log10(RHO)

def arrow(x0, y0, x1, y1, style, w):
    a = math.atan2(y1 - y0, x1 - x0); L = min(8, math.hypot(x1 - x0, y1 - y0) * 0.5)
    hx1, hy1 = x1 - L * math.cos(a - 0.4), y1 - L * math.sin(a - 0.4)
    hx2, hy2 = x1 - L * math.cos(a + 0.4), y1 - L * math.sin(a + 0.4)
    return (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" style="stroke:{style}" stroke-width="{w}"/>'
            f'<path d="M{x1:.1f} {y1:.1f} L{hx1:.1f} {hy1:.1f} L{hx2:.1f} {hy2:.1f}Z" style="fill:{style}"/>')

# ---- 1. phasor sum (auto-scaled so the whole chain fills the panel)
W1, H1 = 300, 270
steps = []
for i in range(12):
    ph = rnd.random() * 2 * math.pi; a = (0.6 + 0.8 * rnd.random()) / math.sqrt(12) * 1.6
    steps.append((a * math.cos(ph), a * math.sin(ph)))
pts = [(0.0, 0.0)]
for dx, dy in steps:
    pts.append((pts[-1][0] + dx, pts[-1][1] + dy))
xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
sc = min((W1 - 60) / max(1e-9, max(xs) - min(xs)), (H1 - 70) / max(1e-9, max(ys) - min(ys)))
ox = 30 + (W1 - 60 - sc * (max(xs) - min(xs))) / 2 - sc * min(xs)
oy = 30 + (H1 - 70 - sc * (max(ys) - min(ys))) / 2 + sc * max(ys)
P = lambda q: (ox + sc * q[0], oy - sc * q[1])
cx, cy = P((0, 0))
parts = [f'<line x1="10" y1="{cy:.1f}" x2="{W1-10}" y2="{cy:.1f}" style="stroke:var(--line-strong)" stroke-width="0.8"/>',
         f'<line x1="{cx:.1f}" y1="12" x2="{cx:.1f}" y2="{H1-26}" style="stroke:var(--line-strong)" stroke-width="0.8"/>',
         f'<text x="{W1-56}" y="{cy-6:.1f}" font-size="11" style="fill:var(--ink-soft)">实部 r_I</text>',
         f'<text x="{cx+6:.1f}" y="22" font-size="11" style="fill:var(--ink-soft)">虚部 r_Q</text>']
for a, b in zip(pts, pts[1:]):
    parts.append(arrow(*P(a), *P(b), 'var(--ink-faint)', 1.3))
parts.append(arrow(cx, cy, *P(pts[-1]), 'var(--key)', 2.8))
sx, sy = pts[-1]
parts.append(f'<text x="12" y="{H1-8}" font-size="12" style="fill:var(--key)">合成包络 z = {math.hypot(sx, sy):.2f}</text>')
svg1 = (f'<svg viewBox="0 0 {W1} {H1}" role="img" aria-label="12 条随机相位的回波首尾相接，合成箭头的长度就是包络 z">'
        + ''.join(parts) + '</svg>')

# ---- 2. Rayleigh PDF (z normalised to Zrms, sigma = 1/sqrt2)
W2, H2 = 320, 270
L2, R2, T2, Bt2 = 36, W2 - 12, 18, H2 - 34
s = 1 / math.sqrt(2); zmax, pmax = 3.0, 0.95
p = lambda z: z / (s * s) * math.exp(-z * z / (2 * s * s))
X = lambda z: L2 + z / zmax * (R2 - L2)
Y = lambda v: Bt2 - v / pmax * (Bt2 - T2)
curve = ' L'.join(f'{X(zmax*i/300):.1f} {Y(p(zmax*i/300)):.1f}' for i in range(301))
shade = f'M{X(0):.1f} {Bt2} L' + ' L'.join(f'{X(RHO*i/60):.1f} {Y(p(RHO*i/60)):.1f}' for i in range(61)) + f' L{X(RHO):.1f} {Bt2} Z'
parts = [f'<line x1="{L2}" y1="{Bt2}" x2="{R2}" y2="{Bt2}" style="stroke:var(--line-strong)"/>',
         f'<line x1="{L2}" y1="{T2}" x2="{L2}" y2="{Bt2}" style="stroke:var(--line-strong)"/>',
         f'<path d="{shade}" style="fill:var(--key);opacity:.35"/>',
         f'<path d="M{curve}" style="fill:none;stroke:var(--accent)" stroke-width="2.2"/>',
         f'<line x1="{X(s):.1f}" y1="{Y(p(s)):.1f}" x2="{X(s):.1f}" y2="{Bt2}" style="stroke:var(--ink-faint)" stroke-dasharray="4 3"/>',
         f'<line x1="{X(s)+2:.1f}" y1="{Y(p(s))-2:.1f}" x2="{X(1.3):.1f}" y2="{Y(p(s))-2:.1f}" style="stroke:var(--ink-faint)" stroke-width="0.8"/><text x="{X(1.32):.1f}" y="{Y(p(s))+2:.1f}" font-size="11" style="fill:var(--ink-soft)">最可能值 z = σ</text>',
         f'<line x1="{X(RHO):.1f}" y1="{T2}" x2="{X(RHO):.1f}" y2="{Bt2}" style="stroke:var(--key)" stroke-dasharray="5 4" stroke-width="1.4"/>',
         f'<text x="{X(RHO)+4:.1f}" y="{Bt2-6}" font-size="11" style="fill:var(--key)">门限 ρ = 0.3</text>',
         f'<text x="{L2-30}" y="{T2+4}" font-size="11" style="fill:var(--ink-soft)">p(z)</text>',
         f'<text x="{R2-62}" y="{H2-6}" font-size="11" style="fill:var(--ink-soft)">z / Z_rms</text>']
for z in (0, 1, 2, 3):
    parts.append(f'<text x="{X(z)-3:.1f}" y="{Bt2+14}" font-size="11" style="fill:var(--ink-soft)">{z}</text>')
svg2 = (f'<svg viewBox="0 0 {W2} {H2}" role="img" aria-label="瑞利分布概率密度曲线，z 从 0 开始，在 z = σ 处最高，右边拖尾；门限左侧阴影面积是深衰落概率">'
        + ''.join(parts) + '</svg>')

# ---- 3. envelope over time (Jakes sum of sinusoids)
M, fm, NS = 16, 20, 800
th = [2 * math.pi * (i + rnd.random()) / M for i in range(M)]
ph = [(rnd.random() * 2 * math.pi, rnd.random() * 2 * math.pi) for _ in range(M)]
z = []
for k in range(NS):
    t = k / NS; I = Q = 0.0
    for i in range(M):
        w = 2 * math.pi * fm * math.cos(th[i]) * t
        I += math.cos(w + ph[i][0]); Q += math.sin(w + ph[i][1])
    z.append(math.hypot(I, Q))
rms = math.sqrt(sum(v * v for v in z) / NS); z = [v / rms for v in z]
db = [20 * math.log10(max(v, 1e-4)) for v in z]
W3, H3 = 660, 210
L3, R3, T3, Bt3, lo, hi = 46, W3 - 10, 10, H3 - 28, -35, 10
Yd = lambda d: T3 + (hi - max(lo, min(hi, d))) / (hi - lo) * (Bt3 - T3)
Xk = lambda k: L3 + k / (NS - 1) * (R3 - L3)
parts = []
for d in (10, 0, -10, -20, -30):
    parts.append(f'<line x1="{L3}" y1="{Yd(d):.1f}" x2="{R3}" y2="{Yd(d):.1f}" style="stroke:var(--line)" stroke-width="0.8"/>')
    parts.append(f'<text x="4" y="{Yd(d)+4:.1f}" font-size="11" style="fill:var(--ink-soft)">{d} dB</text>')
# shaded deep fades
fades = 0; k = 0
while k < NS:
    if db[k] < THR_DB:
        j = k
        while j < NS and db[j] < THR_DB: j += 1
        pts = f'M{Xk(k):.1f} {Yd(THR_DB):.1f} ' + ' '.join(f'L{Xk(i):.1f} {Yd(db[i]):.1f}' for i in range(k, j)) + f' L{Xk(j-1):.1f} {Yd(THR_DB):.1f} Z'
        parts.append(f'<path d="{pts}" style="fill:var(--key);opacity:.3"/>')
        if k > 0: fades += 1
        k = j
    else:
        k += 1
parts.append('<path d="M' + ' L'.join(f'{Xk(i):.1f} {Yd(db[i]):.1f}' for i in range(NS)) + '" style="fill:none;stroke:var(--accent)" stroke-width="1.5"/>')
parts.append(f'<line x1="{L3}" y1="{Yd(THR_DB):.1f}" x2="{R3}" y2="{Yd(THR_DB):.1f}" style="stroke:var(--key)" stroke-dasharray="5 4" stroke-width="1.4"/>')
parts.append(f'<text x="{R3-64}" y="{H3-8}" font-size="11" style="fill:var(--ink-soft)">时间 → 1 s</text>')
svg3 = (f'<svg viewBox="0 0 {W3} {H3}" role="img" aria-label="包络随时间起伏的曲线，单位 dB，多处跌到门限以下形成深衰落">'
        + ''.join(parts) + '</svg>')

lcr = math.sqrt(2 * math.pi) * fm * RHO * math.exp(-RHO ** 2)
frac = 1 - math.exp(-RHO ** 2)
html = f'''<div class="figwrap">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;align-items:start">
<div>{svg1}<div class="cap">① 12 条回波（灰色）相位随机，首尾相接；橙色合成箭头的长度就是包络 z。实部、虚部都是很多随机量之和，所以都是高斯的。</div></div>
<div>{svg2}<div class="cap">② 统计很多时刻的 z，得到瑞利分布。阴影面积 = z 低于门限的概率 = 1 − e<sup>−ρ²</sup> = {frac*100:.1f}%。</div></div>
</div>
<div style="margin-top:14px">{svg3}<div class="cap">③ 手机移动时（f<sub>m</sub> = 20 Hz，画 1 秒，以 rms 为 0 dB），包络在 +{max(db):.0f} dB 到 {min(db):.0f} dB 之间起伏。橙色虚线是门限 ρ = 0.3（{THR_DB:.1f} dB），每次跌到虚线以下就是一次深衰落：这段仿真里有 {fades} 次，LCR 公式给出 √(2π)·f<sub>m</sub>·ρ·e<sup>−ρ²</sup> ≈ {lcr:.1f} 次/秒（公式是长时间平均，一秒的样本会有随机出入）。</div></div>
</div>'''
(B / 'rayleigh_fig.txt').write_text(html, encoding='utf-8')
print('fades', fades, 'lcr', round(lcr, 1), 'frac', round(frac, 3), 'min dB', round(min(db), 1), 'max dB', round(max(db), 1))
