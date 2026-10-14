#!/usr/bin/python3
"""Static Doppler figure for Part 2 section 2.5: geometry (θ, v) and Doppler spectrum. Writes doppler_fig.txt."""
import math, pathlib

B = pathlib.Path(__file__).parent
V, FC = 120 / 3.6, 5e9
FM = V * FC / 3e8                      # 555.6 Hz (slide example)
TH = math.radians(45)
SCAT = [2 * math.pi * (i + 0.5) / 12 for i in range(12)]

def arrow(x0, y0, x1, y1, style, w, L=9):
    a = math.atan2(y1 - y0, x1 - x0)
    return (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" style="stroke:{style}" stroke-width="{w}"/>'
            f'<path d="M{x1:.1f} {y1:.1f} L{x1-L*math.cos(a-0.4):.1f} {y1-L*math.sin(a-0.4):.1f} L{x1-L*math.cos(a+0.4):.1f} {y1-L*math.sin(a+0.4):.1f}Z" style="fill:{style}"/>')

# ---- geometry
W1, H1 = 300, 270
cx, cy, R = 150, 132, 102
p = [f'<circle cx="{cx}" cy="{cy}" r="{R}" style="fill:none;stroke:var(--line-strong)" stroke-dasharray="3 4"/>']
for a in SCAT:
    sx, sy = cx + R * math.cos(a), cy - R * math.sin(a)
    p.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{cx}" y2="{cy}" style="stroke:var(--ink-faint)" stroke-width="0.8" opacity="0.6"/>')
    p.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="3.5" style="fill:var(--ink-faint)"/>')
sx, sy = cx + R * math.cos(TH), cy - R * math.sin(TH)
p.append(arrow(sx, sy, cx + 14 * math.cos(TH), cy - 14 * math.sin(TH), 'var(--key)', 2.4))
p.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="5" style="fill:var(--key)"/>')
p.append(f'<path d="M{cx+34} {cy} A34 34 0 0 0 {cx+34*math.cos(TH):.1f} {cy-34*math.sin(TH):.1f}" style="fill:none;stroke:var(--key)" stroke-width="1.3"/>')
p.append(f'<text x="{cx+40*math.cos(TH/2)+2:.1f}" y="{cy-40*math.sin(TH/2)+4:.1f}" font-size="13" style="fill:var(--key)">θ</text>')
p.append(f'<rect x="{cx-14}" y="{cy-8}" width="28" height="16" rx="3" style="fill:var(--extra)"/>')
p.append(arrow(cx + 16, cy, cx + 86, cy, 'var(--extra)', 2.6))
p.append(f'<text x="{cx+60}" y="{cy+18}" font-size="12" style="fill:var(--extra)">速度 v</text>')
p.append(f'<text x="{sx+8:.1f}" y="{sy-6:.1f}" font-size="11" style="fill:var(--key)">θ = 45°</text>')
p.append(f'<text x="{cx+R-34}" y="{cy-6}" font-size="11" style="fill:var(--ink-soft)">迎面 θ=0°</text>')
p.append(f'<text x="{cx-R+2}" y="{cy-6}" font-size="11" style="fill:var(--ink-soft)">背后 180°</text>')
p.append(f'<text x="8" y="{H1-8}" font-size="11" style="fill:var(--ink-soft)">灰点：周围的散射体，各送来一条回波</text>')
svg1 = f'<svg viewBox="0 0 {W1} {H1}" role="img" aria-label="俯视图：手机向右移动，周围一圈散射体从各个方向送来回波，其中一条与前进方向成 45 度">' + ''.join(p) + '</svg>'

# ---- spectrum
W2, H2 = 340, 270
L, Rr, base, top = 20, W2 - 14, H2 - 52, 18
mid, half = (L + Rr) / 2, (Rr - L) / 2 * 0.86
X = lambda f: mid + f / FM * half
p = [f'<line x1="{L}" y1="{base}" x2="{Rr}" y2="{base}" style="stroke:var(--line-strong)"/>']
pts = [f'{X(-FM*0.995):.1f} {base}']
for i in range(-99, 100):
    u = i / 100; y = base - min(base - top - 18, 30 / math.sqrt(1 - u * u))
    pts.append(f'{X(u*FM):.1f} {y:.1f}')
pts.append(f'{X(FM*0.995):.1f} {base}')
p.append(f'<path d="M{" L".join(pts)} Z" style="fill:var(--accent-soft);stroke:var(--accent)" stroke-width="2"/>')
for a in SCAT:
    xx = X(FM * math.cos(a))
    p.append(f'<line x1="{xx:.1f}" y1="{base}" x2="{xx:.1f}" y2="{base-68}" style="stroke:var(--ink-faint)" stroke-width="1.3"/><circle cx="{xx:.1f}" cy="{base-68}" r="3" style="fill:var(--ink-faint)"/>')
xr = X(FM * math.cos(TH))
p.append(f'<line x1="{xr:.1f}" y1="{base}" x2="{xr:.1f}" y2="{base-110}" style="stroke:var(--key)" stroke-width="2.4"/><circle cx="{xr:.1f}" cy="{base-110}" r="4.5" style="fill:var(--key)"/>')
p.append(f'<text x="{xr-8:.1f}" y="{base-116}" font-size="11" text-anchor="end" style="fill:var(--key)">θ = 45°：+{FM*math.cos(TH):.0f} Hz</text>')
p.append(f'<line x1="{mid}" y1="{base}" x2="{mid}" y2="{top}" style="stroke:var(--ink-faint)" stroke-dasharray="4 3"/>')
for f, lab in ((-FM, 'f_c − 556 Hz'), (0, 'f_c'), (FM, 'f_c + 556 Hz')):
    p.append(f'<text x="{X(f):.1f}" y="{base+16}" font-size="11" text-anchor="middle" style="fill:var(--ink-soft)">{lab}</text>')
p.append(f'<text x="{X(-FM*0.5):.1f}" y="{base+34}" font-size="11" text-anchor="middle" style="fill:var(--ink-soft)">← 背向：频率降低</text>')
p.append(f'<text x="{X(FM*0.5):.1f}" y="{base+34}" font-size="11" text-anchor="middle" style="fill:var(--ink-soft)">迎面：频率升高 →</text>')
p.append(f'<text x="{L+4}" y="{top+6}" font-size="11" style="fill:var(--accent-ink)">多普勒谱 f_c ± f_m（讲义记 B_D = f_m）</text>')
svg2 = f'<svg viewBox="0 0 {W2} {H2}" role="img" aria-label="频率轴：每条回波移到 f_c 加 f_m 乘 cos θ，合起来是 f_c 两侧各宽 f_m 的 U 形多普勒谱">' + ''.join(p) + '</svg>'

html = f'''<div class="figwrap">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;align-items:start">
<div>{svg1}<div class="cap">① 俯视图：手机以 v 向右开，θ 是电波来的方向和前进方向的夹角。橙色那条 θ = 45°。</div></div>
<div>{svg2}<div class="cap">② 取讲义的数：v = 120 km/h、f<sub>c</sub> = 5 GHz → f<sub>m</sub> = 556 Hz。θ = 45° 的回波移了 556 × cos45° ≈ +393 Hz。所有方向的回波合起来，一根谱线被展宽成 f<sub>c</sub> ± f<sub>m</sub> 之间的 U 形谱（两端回波最密，因为 cos θ 在 0° 和 180° 附近变化最慢）。</div></div>
</div>
</div>'''
(B / 'doppler_fig.txt').write_text(html, encoding='utf-8')
print('fm', round(FM, 1), 'fd45', round(FM * math.cos(TH), 1))
