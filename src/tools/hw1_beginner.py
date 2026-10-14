#!/usr/bin/python3
"""HW1 page: course-based Q2(c) derivation, detailed Q2(b) explanation,
worst-corner interference figure, extra-curricular boxes."""
import pathlib

P = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129-study/hw1.html')
s = P.read_text(encoding='utf-8')

def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (n, old[:70])
    s = s.replace(old, new)

# ---------------------------------------------------------------- CSS
rep('footer{margin-top:40px;', '''.extra{border:1.5px solid var(--extra);background:var(--extra-soft);border-radius:10px;padding:10px 16px 12px;margin:14px 0;max-width:76ch}
.extra-lbl{font-family:'IBM Plex Mono',monospace;font-size:.7rem;letter-spacing:.06em;color:var(--extra);font-weight:700;margin-bottom:4px}
.extra p{margin:.4em 0}
.extra ul{margin:.3em 0;padding-left:1.3em}
.extra .tw{margin:8px 0}
footer{margin-top:40px;''')
rep('  --ok:#137a3f; --near:#b4361f; --mid:#b07a12; --far:#2f6fb0;\n',
    '  --ok:#137a3f; --near:#b4361f; --mid:#b07a12; --far:#2f6fb0;\n  --extra:#7a4fc4; --extra-soft:#f2ecfb;\n')
rep('    --ok:#4fd087; --near:#f2857c; --mid:#e9b85a; --far:#7fb3ec;\n',
    '    --ok:#4fd087; --near:#f2857c; --mid:#e9b85a; --far:#7fb3ec;\n    --extra:#b79cf0; --extra-soft:rgba(183,156,240,.12);\n')
rep('  --ok:#4fd087; --near:#f2857c; --mid:#e9b85a; --far:#7fb3ec;\n  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 22px rgba(0,0,0,.4);\n}',
    '  --ok:#4fd087; --near:#f2857c; --mid:#e9b85a; --far:#7fb3ec;\n  --extra:#b79cf0; --extra-soft:rgba(183,156,240,.12);\n  --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 22px rgba(0,0,0,.4);\n}')
rep('.wedge{fill:var(--accent);opacity:.16;stroke:var(--accent);stroke-width:1}',
    '.wedge{fill:var(--accent);opacity:.12;stroke:var(--accent);stroke-width:.8}\n.wedge.hit{opacity:.32}')
rep('  <div class="notice"><b>写作业前先看：</b>',
    '  <div class="notice"><b>紫色框</b>是课件以外的补充内容，帮助理解，考试以课件为准。<br><b>写作业前先看：</b>')

# ---------------------------------------------------------------- Q1(a) extra
rep('''      <li>只画图、不写功能，或只列名字、不讲怎么配合，都会丢分。14 分大致是 4 个部件各 2–2.5 分，图和流程说明占剩下的分。</li>
    </ul></div>''', '''      <li>只画图、不写功能，或只列名字、不讲怎么配合，都会丢分。14 分大致是 4 个部件各 2–2.5 分，图和流程说明占剩下的分。</li>
    </ul></div>
    <div class="extra"><div class="extra-lbl">课外补充 · 课件里没有这些名字</div>
      <p>课件 p.11 只写了 "Databases" 和 "Security Mechanism"。上面提到的 <b>HLR</b>（归属位置寄存器）、<b>VLR</b>（拜访位置寄存器）、<b>AuC</b>（鉴权中心）、<b>EIR</b>（设备识别寄存器）、<b>MSC</b>，是 GSM 标准里对应部件的名字。答案里写上能显得具体，但不是课件要求的内容。</p>
      <p>可以这样理解：HLR 像你的"户口本"，永远记着你是谁、开通了什么业务、现在大概在哪个区域；VLR 像酒店的"住客登记"，你漫游到哪里，那里的 VLR 就临时登记你；AuC 像"门卫查身份证"；EIR 像"失窃手机黑名单"。</p>
    </div>''')

# ---------------------------------------------------------------- Q2(b) explanation + figure
rep('''      <li>(iv) 120° 扇区：<div class="f">SIR = 1 / (Q<sup>−n</sup> + (Q+0.7)<sup>−n</sup>) = 1 / (1/597.9 + 1/1086.3) = 385.7 → 25.9 dB</div>比 (iii) 高约 7.4 dB，满足 20 dB 且余量约 6 dB。</li>
    </ol>''', '''      <li>(iv) 120° 扇区：<div class="f">SIR = 1 / (Q<sup>−n</sup> + (Q+0.7)<sup>−n</sup>) = 1 / (1/597.9 + 1/1086.3) = 385.7 → 25.9 dB</div>比 (iii) 高约 7.4 dB，满足 20 dB 且余量约 6 dB。</li>
    </ol>
    <h3>(i) 那句评论在说什么：简化算法 vs 最坏情况</h3>
    <div class="prose">
      <p>课件对同一个系统给了三种算法，区别只在一个问题上：<b>6 个干扰基站离手机有多远？</b>（完整的零基础讲解，见 Part A 讲解长文第七章 7.2–7.3。）</p>
      <ul>
        <li><b>简化算法（p.88）</b>：假设 6 个都在距离 D（课件原文 "equidistant, D"），S/I = Q<sup>n</sup>/6 → <b>18.66 dB</b>。</li>
        <li><b>Case 1（p.91）</b>：手机站在小区边上，等于从自己基站往一边走了 R。于是 2 个干扰变近（D − R），2 个变远（D + R），2 个基本不变（D）→ <b>17.27 dB</b>。</li>
        <li><b>Case 2（p.91）</b>："To be conservative"，往最坏处想，6 个都按最近的 D − R 算 → <b>14.39 dB</b>。</li>
      </ul>
      <p>为什么一近一远不能抵消？因为强度按距离的 −4 次方变化。取 R = 1、N = 7，则 D = 4.58：</p>
    </div>
    <div class="tw"><table style="min-width:440px">
      <thead><tr><th>距离</th><th class="num">距离⁴</th><th class="num">每个干扰的强度</th><th class="num">和"都在 D"比</th></tr></thead>
      <tbody>
        <tr><td>D − R = 3.58（变近）</td><td class="num">164.7</td><td class="num">0.00607</td><td class="num">2.7 倍</td></tr>
        <tr><td>D = 4.58</td><td class="num">441</td><td class="num">0.00227</td><td class="num">1 倍</td></tr>
        <tr><td>D + R = 5.58（变远）</td><td class="num">971.3</td><td class="num">0.00103</td><td class="num">0.45 倍</td></tr>
      </tbody>
    </table></div>
    <div class="prose"><p>变近的强了 2.7 倍，变远的只弱到 0.45 倍，6 个加起来总干扰多了约 38%。所以 SIR 从 18.66 dB 降到 17.27 dB，低于课件 p.89 要求的 18 dB。这就是评论里"简化模型偏乐观"的意思，也是 (iii) 要你用最坏情况公式重算的原因。</p></div>''')

rep('''        <button type="button" id="mode-omni" aria-pressed="true">全向天线 · 6 个干扰</button>''',
    '''        <button type="button" id="mode-omni" aria-pressed="true">全向天线 · 6 个干扰</button>''')
rep('''      <div class="legend" id="int-legend"><span><i style="background:var(--near)"></i>约 D − R（最近两个）</span><span><i style="background:var(--mid)"></i>约 D</span><span><i style="background:var(--far)"></i>约 D + R（最远两个）</span></div>
      <figcaption id="int-cap">N = 7，按比例画。移动台在小区边缘，到 6 个同频基站的距离分成三组，正是 (iii) 公式里 2(Q−1)、2Q、2(Q+1) 三项的来源。</figcaption>
    </figure>''', '''      <div class="legend" id="int-legend"><span><i style="background:var(--near)"></i>最近两个，约 D − R</span><span><i style="background:var(--mid)"></i>中间两个，约 D</span><span><i style="background:var(--far)"></i>最远两个，约 D + R</span></div>
      <figcaption id="int-cap"></figcaption>
    </figure>''')

rep('''    <div class="mem">从乐观到保守，三个口径依次是：''', '''    <div class="extra"><div class="extra-lbl">课外补充 · 课件没有推导</div>
      <p><b>(iv) 公式里的 D 和 D + 0.7R 是怎么来的？</b>课件 p.145 直接给了这两个距离。我按上图的几何精确算了一遍：手机站在自己 1 号扇区最远的那个角上（离自己基站 R），能照到它的只有身后两个同频小区的 1 号扇区，距离分别是 <b>5.29R</b> 和 <b>4.36R</b>。D = √21 R = 4.58R，所以 5.29R = D + 0.71R，就是课件的 D + 0.7R；4.36R = D − 0.22R，课件近似成 D。</p>
      <p>为什么只剩 2 个：所有小区的 1 号扇区朝向一样，同频小区的 1 号扇区用同一组信道。这些天线只照前方 120°，所以只有位于手机<b>身后</b>的同频基站照得到它；前方的几个（包括最近的 3.61R 和 4.00R）天线背对手机，被挡掉了。这就是扇区化公式里没有 (Q − 1) 项、SIR 提升这么多的原因。</p>
    </div>
    <div class="mem">从乐观到保守，三个口径依次是：''')

# ---------------------------------------------------------------- drawInterf: worst corner
old_start = s.index('  /* ---------- Q2(b) interference geometry ---------- */')
old_end = s.index("  document.querySelectorAll('svg.hexgrid').forEach(drawHex);")
NEW_DRAW = '''  /* ---------- Q2(b) interference geometry: MS at the far corner of its 120° sector ---------- */
  function drawInterf(svg){
    var R=20, s3=Math.sqrt(3), D=Math.sqrt(21)*R, deg=Math.PI/180;
    var base=Math.atan2(1.5, 2.5*s3)/deg;           // first-tier co-channel cells at 19.1° + 60°k
    var ms=[R*Math.cos(-30*deg), -R*Math.sin(-30*deg)];   // hexagon vertex at −30°
    function rhombus(cx, cy){                        // sector 1: centre → vertices at −30°, 30°, 90°
      var p=[[cx,cy]];
      [-30,30,90].forEach(function(a){ p.push([cx+R*Math.cos(a*deg), cy-R*Math.sin(a*deg)]); });
      return p.map(function(q){ return q[0].toFixed(1)+','+q[1].toFixed(1); }).join(' ');
    }
    el('polygon',{points:hexPts(0,0,R),'class':'cell7 home'}, svg);
    el('polygon',{points:rhombus(0,0),'class':'wedge hit'}, svg);
    var cells=[];
    for (var k=0;k<6;k++){
      var a=(base+60*k)*deg, x=D*Math.cos(a), y=-D*Math.sin(a);
      cells.push({k:k, x:x, y:y, d:Math.hypot(x-ms[0], y-ms[1])/R, hit:(k===3||k===4)});
    }
    var order=cells.slice().sort(function(p,q){ return p.d-q.d; });
    order.forEach(function(c,i){ c.grp = i<2 ? 'near' : i<4 ? 'mid' : 'far'; });
    var lines=el('g',{},svg), labs=el('g',{},svg);
    cells.forEach(function(c){
      el('polygon',{points:hexPts(c.x,c.y,R),'class':'cell7'}, svg);
      el('polygon',{points:rhombus(c.x,c.y),'class':'wedge'+(c.hit?' hit':'')}, svg);
      el('circle',{cx:c.x,cy:c.y,r:3.2,'class':'bs'}, svg);
      el('line',{x1:c.x.toFixed(1),y1:c.y.toFixed(1),x2:ms[0].toFixed(1),y2:ms[1].toFixed(1),'class':'il '+c.grp+(c.hit?'':' blocked')}, lines);
      var t=0.58, mx=ms[0]+(c.x-ms[0])*t, my=ms[1]+(c.y-ms[1])*t;
      var L=Math.hypot(c.x-ms[0], c.y-ms[1]), nx=-(c.y-ms[1])/L, ny=(c.x-ms[0])/L;
      var omni=c.d.toFixed(2)+'R', sect=omni+(c.k===3?' ≈ D+0.7R':c.k===4?' ≈ D':'');
      var tx=el('text',{x:(mx+nx*9).toFixed(1),y:(my+ny*9+3).toFixed(1),'text-anchor':'middle','class':'ilab '+c.grp+(c.hit?'':' blocked')}, labs, omni);
      tx.setAttribute('data-omni', omni); tx.setAttribute('data-sect', sect);
    });
    el('circle',{cx:0,cy:0,r:3.2,'class':'bs'}, svg);
    el('text',{x:-6,y:-6,'font-size':10,'text-anchor':'end','font-weight':600}, svg, 'BS');
    el('circle',{cx:ms[0].toFixed(1),cy:ms[1].toFixed(1),r:4.5,'class':'ms'}, svg);
    el('text',{x:(ms[0]+7).toFixed(1),y:(ms[1]+13).toFixed(1),'font-size':10,'font-weight':700,'style':'fill:var(--accent-strong)'}, svg, 'MS');
  }

'''
s = s[:old_start] + NEW_DRAW + s[old_end:]

rep('''    intsvg.querySelectorAll('.wedge.off').forEach(function(w){ w.style.opacity=0; });
    cap.textContent = sect
      ? '120° 扇区：各小区同方向的扇区天线只覆盖 120°。移动台只会被 2 个同频扇区照到（实线），其余 4 个被挡掉（虚线）。课件最坏情况把这两个距离取为 D 和 D + 0.7R。n = 4.2 时 SIR ≈ 25.9 dB。'
      : 'N = 7，按比例画。移动台在小区边缘，到 6 个同频基站的距离分成三组，正是 (iii) 公式里 2(Q−1)、2Q、2(Q+1) 三项的来源。n = 4.2 时 SIR ≈ 18.5 dB。';''',
'''    intsvg.querySelectorAll('.ilab').forEach(function(t){ t.textContent = t.getAttribute(sect?'data-sect':'data-omni'); });
    cap.textContent = sect
      ? '120° 扇区：每个小区切成 3 个菱形扇区，1 号扇区（浅色菱形）朝向全都一样。手机只被身后 2 个同频小区的 1 号扇区照到（实线），前方 4 个被挡掉（虚线），包括最近的 3.61R 和 4.00R。剩下两个在 5.29R ≈ D + 0.7R 和 4.36R ≈ D，正是课件 p.145 公式里的两项。n = 4.2 时 SIR ≈ 25.9 dB。'
      : 'N = 7，按比例画（D = 4.58R）。手机站在小区边上（六边形的一个角）。6 个同频基站的距离从 3.61R 到 5.57R 不等：最近两个约 D − R，中间两个约 D，最远两个约 D + R，这就是 (iii) 公式里 2(Q−1)、2Q、2(Q+1) 三项的来历。n = 4.2 时课件公式给 SIR ≈ 18.5 dB。';''')

# ---------------------------------------------------------------- Q2(c) guide: course method p.73–76
rep('''    <div class="chips"><span class="chip">相邻小区中心距 √3R</span><span class="chip">i、j 坐标</span><span class="chip">余弦定理</span><span class="chip">面积比</span><span class="chip src">课件 p.9, 73–78</span></div>''',
    '''    <div class="chips"><span class="chip">相邻小区中心距 √3R</span><span class="chip">i、j 坐标</span><span class="chip">归一化距离 D<sub>norm</sub></span><span class="chip">大六边形面积</span><span class="chip src">课件 p.73–76</span></div>''')
g_start = s.index('''      <li><b>相邻小区中心距离</b>：六边形半径 R（中心到顶点 = 边长），中心到边的距离是 R cos30° = (√3/2)R，所以相邻两个小区中心相距 <b>√3 R</b>。</li>''')
g_end = s.index('''      <li>求 N 那一步要写出面积比的理由，只写结论 N = i² + ij + j² 拿不到推导分。</li>
    </ul></div>''') + len('''      <li>求 N 那一步要写出面积比的理由，只写结论 N = i² + ij + j² 拿不到推导分。</li>
    </ul></div>''')
GUIDE_2C = '''      <li><b>相邻小区中心距离（p.73）</b>：六边形半径 R（中心到顶点，等于边长）。中心到一条边的垂直距离是 R cos30° = (√3/2)R，相邻两个小区中心隔着一条公共边，所以相距 <div class="f">2R cos30° = √3 R</div></li>
      <li><b>建 i、j 坐标（p.73–74）</b>：把相邻中心的距离 √3R 当作 1 个单位（"归一化"）。以参考小区中心为原点 (0, 0)，i 轴和 j 轴分别穿过两条相邻的边、垂直于这两条边，<b>两轴夹角 60°</b>。这样每个小区中心都落在整数坐标 (i, j) 上：沿 i 轴走 i 格，再沿 j 轴方向走 j 格。</li>
      <li><b>算归一化距离（p.75）</b>：60° 斜坐标不能直接用勾股定理，先把"沿 j 轴走 j 格"拆成两个互相垂直的分量：沿 i 轴方向是 j sin30° = j/2，垂直于 i 轴方向是 j cos30° = (√3/2) j。于是：
        <div class="f">D<sub>norm</sub><sup>2</sup> = [j cos30°]<sup>2</sup> + [i + j sin30°]<sup>2</sup> = (3/4)j<sup>2</sup> + i<sup>2</sup> + ij + (1/4)j<sup>2</sup> = i<sup>2</sup> + ij + j<sup>2</sup></div></li>
      <li><b>乘回实际长度（p.75）</b>：1 个单位是 √3R：<div class="f">D = √3 R · D<sub>norm</sub> = √3 R · √(i<sup>2</sup> + ij + j<sup>2</sup>)</div>例：i = 2、j = 1，D<sub>norm</sub><sup>2</sup> = 4 + 2 + 1 = 7，D = √3R × √7 = √21 R ≈ 4.58R。</li>
      <li><b>求 N（p.76）</b>：同频小区中心之间相距 D，就像普通小区中心之间相距 √3R。普通小区的半径是 √3R ÷ √3 = R；按同样的比例，每个同频小区"管"的那块区域是一个半径 <b>D/√3</b> 的大六边形，它的面积正好等于一个簇（N 个小区）。半径 r 的正六边形面积是 (3√3/2) r<sup>2</sup>，所以：
        <div class="f">N × (3√3/2) R<sup>2</sup> = (3√3/2) (D/√3)<sup>2</sup>   →   N = D<sup>2</sup> / (3R<sup>2</sup>)</div>
        把第 4 步的 D<sup>2</sup> = 3R<sup>2</sup>(i<sup>2</sup> + ij + j<sup>2</sup>) 代进去：<div class="f">N = i<sup>2</sup> + ij + j<sup>2</sup> = D<sub>norm</sub><sup>2</sup></div></li>
      <li><b>结论（p.75）</b>：N = D<sub>norm</sub><sup>2</sup>，所以 D = √3R · √N：<div class="f">D = R√(3N)，  Q = D/R = √(3N)</div>N 只能取 1, 3, 4, 7, 9, 12, 13 …（p.76–77）；例如 i = 2、j = 1 时 N = 7。</li>
    </ol>
    <div class="trap"><ul>
      <li>相邻小区中心距离是 √3R，不是 R，也不是 2R。</li>
      <li>i、j 两轴夹角是 60°，不能直接 D² = i² + j²。要先把 j 拆成 j/2 和 (√3/2)j 两个分量，展开时 (3/4)j² + (1/4)j² 合起来才是 j²。</li>
      <li>求 N 要写出"大六边形面积 = 簇面积"这一步和半径 D/√3 的理由，只写结论拿不到推导分。</li>
    </ul></div>
    <div class="extra"><div class="extra-lbl">课外补充 · 另一种算 D 的方法</div>
      <p>也可以用余弦定理：两段位移长 i√3R 和 j√3R，在三角形里夹角是 120°，D² = (i√3R)² + (j√3R)² − 2(i√3R)(j√3R)cos120° = 3R²(i² + ij + j²)，结果一样。作业里写课件 p.75 的投影法更稳妥。</p>
    </div>'''
s = s[:g_start] + GUIDE_2C + s[g_end:]

# ---------------------------------------------------------------- Q2(c) answers
ZH_OLD_START = s.index('''      <li>取夹角 60° 的两条坐标轴。从某小区出发，沿一个方向移动 i 个小区，逆时针转 60° 再移动 j 个小区，即到达最近的同频小区（i、j 为非负整数）。</li>''')
ZH_OLD_END = s.index('''    <div class="box"><b>D = R√(3N)</b>，<b>N = i<sup>2</sup> + ij + j<sup>2</sup></b>，同频复用比 Q = D/R = √(3N)</div>''')
ZH_NEW = '''      <li>以相邻中心距离 √3R 为 1 个单位，以参考小区中心为原点建立 i、j 坐标轴：两轴分别垂直于六边形的两条相邻边，夹角 60°。每个小区中心都位于整数坐标 (i, j)，最近的同频小区在 (i, j) 处（i、j 为非负整数）。</li>
      <li>把沿 j 轴的位移分解为沿 i 轴方向的 j sin30° 和垂直方向的 j cos30°，归一化距离为
        <div class="f">D<sub>norm</sub> = {[j cos30°]<sup>2</sup> + [i + j sin30°]<sup>2</sup>}<sup>1/2</sup> = {(3/4)j<sup>2</sup> + i<sup>2</sup> + ij + (1/4)j<sup>2</sup>}<sup>1/2</sup> = (i<sup>2</sup> + ij + j<sup>2</sup>)<sup>1/2</sup></div>
        实际距离 D = √3R · D<sub>norm</sub> = √3R (i<sup>2</sup> + ij + j<sup>2</sup>)<sup>1/2</sup>。</li>
      <li>同频小区中心相距 D，以每个同频小区为中心、半径为 D/√3 的大六边形覆盖的面积等于一个 N 小区簇的面积（正六边形面积 = (3√3/2)r<sup>2</sup>）：
        <div class="f">N × (3√3/2)R<sup>2</sup> = (3√3/2)(D/√3)<sup>2</sup>  ⇒  N = D<sup>2</sup> / 3R<sup>2</sup> = i<sup>2</sup> + ij + j<sup>2</sup> = D<sub>norm</sub><sup>2</sup></div></li>
    </ol>
'''
s = s[:ZH_OLD_START] + ZH_NEW + s[ZH_OLD_END:]

EN_OLD_START = s.index('''      <li>Use two axes of the hexagonal grid separated by 60°. Starting from a cell, move i cells along one axis, turn 60° anticlockwise and move j cells; this reaches the nearest co-channel cell (i, j are non-negative integers).</li>''')
EN_OLD_END = s.index('''    <div class="box"><b>D = R√(3N)</b>, <b>N = i<sup>2</sup> + ij + j<sup>2</sup></b>, co-channel reuse ratio Q = D/R = √(3N)</div>''')
EN_NEW = '''      <li>Normalise the centre-to-centre distance √3R to one unit and take the centre of the reference cell as the origin. The i and j axes pass perpendicularly through two adjacent sides of the hexagon, so they are 60° apart, and every cell centre lies at integer co-ordinates (i, j). The nearest co-channel cell is at (i, j), with i, j non-negative integers.</li>
      <li>Resolving the j displacement into j sin30° along the i axis and j cos30° perpendicular to it, the normalised distance is
        <div class="f">D<sub>norm</sub> = {[j cos30°]<sup>2</sup> + [i + j sin30°]<sup>2</sup>}<sup>1/2</sup> = {(3/4)j<sup>2</sup> + i<sup>2</sup> + ij + (1/4)j<sup>2</sup>}<sup>1/2</sup> = (i<sup>2</sup> + ij + j<sup>2</sup>)<sup>1/2</sup></div>
        and the actual distance is D = √3R · D<sub>norm</sub> = √3R (i<sup>2</sup> + ij + j<sup>2</sup>)<sup>1/2</sup>.</li>
      <li>Co-channel cell centres are D apart, so a large hexagon of radius D/√3 centred on each co-channel cell covers the same area as one N-cell cluster (area of a regular hexagon = (3√3/2)r<sup>2</sup>):
        <div class="f">N × (3√3/2)R<sup>2</sup> = (3√3/2)(D/√3)<sup>2</sup>  ⇒  N = D<sup>2</sup> / 3R<sup>2</sup> = i<sup>2</sup> + ij + j<sup>2</sup> = D<sub>norm</sub><sup>2</sup></div></li>
    </ol>
'''
s = s[:EN_OLD_START] + EN_NEW + s[EN_OLD_END:]

# ---------------------------------------------------------------- Q3(b) table → extra box
rep('''    <div class="tw"><table style="min-width:560px">
      <thead><tr><th>项目</th><th>IEEE 802.11a（1999）</th><th>WiFi 7 · IEEE 802.11be</th></tr></thead>''',
    '''    <div class="extra"><div class="extra-lbl">课外补充 · 题目要求查课外资料（课件 Part B 只讲到 802.11a）</div>
    <div class="tw"><table style="min-width:560px">
      <thead><tr><th>项目</th><th>IEEE 802.11a（1999）</th><th>WiFi 7 · IEEE 802.11be</th></tr></thead>''')
rep('''        <tr><td>峰值速率</td><td>54 Mbit/s</td><td>单链路约 23 Gbit/s（8 流、320 MHz、4096-QAM）</td></tr>
      </tbody>
    </table></div>''', '''        <tr><td>峰值速率</td><td>54 Mbit/s</td><td>单链路约 23 Gbit/s（8 流、320 MHz、4096-QAM）</td></tr>
      </tbody>
    </table></div>
    <p>名词速查：<b>OFDM</b> 把一个宽信道切成很多窄的子载波并行传；<b>OFDMA</b> 在此基础上把不同子载波分给不同用户，多人同时传；<b>QAM</b> 的阶数越高，每个符号携带的比特越多（64-QAM 6 bit，4096-QAM 12 bit），但要求信号更干净；<b>空间流</b>是用多根天线同时传几路不同的数据；<b>MLO</b> 让设备同时在 2.4/5/6 GHz 几个频段上收发。</p>
    </div>''')

P.write_text(s, encoding='utf-8')
print('ok', len(s))
