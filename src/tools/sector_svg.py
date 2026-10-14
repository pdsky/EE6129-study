#!/usr/bin/python3
"""Static SVG for Part A ch9: 120° rhombus sectors, MS at the worst corner, N = 7."""
import math
R = 26.0; s3 = math.sqrt(3); D = math.sqrt(21) * R
def P(x, y): return f"{x:.1f},{-y:.1f}"          # math coords -> svg (y down)
def hexpts(cx, cy):
    return " ".join(P(cx + R*math.cos(math.radians(90+60*k)), cy + R*math.sin(math.radians(90+60*k))) for k in range(6))
def rhombus(cx, cy):   # sector 1: centre -> vertices at -30°, 30°, 90°
    v = lambda a: (cx + R*math.cos(math.radians(a)), cy + R*math.sin(math.radians(a)))
    return " ".join(P(*q) for q in [(cx, cy), v(-30), v(30), v(90)])
base = math.degrees(math.atan2(1.5, 2.5*s3))
cells = [(0.0, 0.0)] + [(D*math.cos(math.radians(base+60*k)), D*math.sin(math.radians(base+60*k))) for k in range(6)]
ms = (R*math.cos(math.radians(-30)), R*math.sin(math.radians(-30)))
inbeam = {4, 5}          # cells[4] = 199.1°, cells[5] = 259.1°
out = ['<svg class="sectfig" viewBox="-150 -150 300 300" role="img" aria-label="120 度扇区：中心小区 1 号扇区角上的手机，只被两个同频小区的 1 号扇区照到">']
for i, (x, y) in enumerate(cells):
    out.append(f'<polygon class="sf-cell{" home" if i == 0 else ""}" points="{hexpts(x, y)}"/>')
    out.append(f'<polygon class="sf-sec{" on" if (i == 0 or i in inbeam) else ""}" points="{rhombus(x, y)}"/>')
labels = []
for i, (x, y) in enumerate(cells[1:], start=1):
    d = math.hypot(ms[0]-x, ms[1]-y) / R
    on = i in inbeam
    out.append(f'<line class="sf-line{" on" if on else ""}" x1="{x:.1f}" y1="{-y:.1f}" x2="{ms[0]:.1f}" y2="{-ms[1]:.1f}"/>')
    t = 0.55; lx, ly = ms[0] + (x-ms[0])*t, ms[1] + (y-ms[1])*t
    nx, ny = -(y-ms[1]), (x-ms[0]); L = math.hypot(nx, ny); nx, ny = nx/L*10, ny/L*10
    txt = f"{d:.2f}R"
    if i == 4: txt += " ≈ D+0.7R"
    if i == 5: txt += " ≈ D"
    labels.append(f'<text class="sf-lab{" on" if on else ""}" x="{lx+nx:.1f}" y="{-(ly+ny):.1f}" text-anchor="middle">{txt}</text>')
for (x, y) in cells:
    out.append(f'<circle class="sf-bs" cx="{x:.1f}" cy="{-y:.1f}" r="3"/>')
out += labels
out.append(f'<circle class="sf-ms" cx="{ms[0]:.1f}" cy="{-ms[1]:.1f}" r="5"/>')
out.append(f'<text class="sf-mslab" x="{ms[0]+8:.1f}" y="{-ms[1]+14:.1f}">手机</text>')
out.append('</svg>')
print("\n".join(out))
