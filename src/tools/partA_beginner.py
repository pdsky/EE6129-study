#!/usr/bin/python3
"""Beginner-level rewrite of Part A ch5 (add 5.3), ch7, ch9, ch10.
Course content cites slide pages; anything not in the slides goes in a .extra box."""
import pathlib, re

REPO = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129-study')
P = REPO / 'partA.html'
SECTOR_SVG = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_text/tools/sector.svg').read_text(encoding='utf-8').strip()
s = P.read_text(encoding='utf-8')

# ------------------------------------------------------------------ CSS
CSS = '''
/* 课外补充框 */
:root{--extra:#7a4fc4;--extra-soft:#f2ecfb;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--extra:#b79cf0;--extra-soft:rgba(183,156,240,.12);}}
:root[data-theme="dark"]{--extra:#b79cf0;--extra-soft:rgba(183,156,240,.12);}
.extra{border:1.5px solid var(--extra);border-radius:10px;padding:16px 20px 18px;margin:30px 0;background:var(--extra-soft);}
.extra > .lbl{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.1em;color:var(--extra);font-weight:700;margin-bottom:8px;}
.extra .worked{margin:16px 0 4px;}
.extra > p:last-child{margin-bottom:0;}
.chapter h4{font-family:var(--f-display);font-size:17px;font-weight:600;margin:26px 0 10px;color:var(--ink);}
/* 示意图 */
.figwrap{margin:26px 0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 14px 12px;}
.figwrap svg{display:block;width:100%;height:auto;margin:0 auto;}
.figwrap svg.sectfig{max-width:440px;}
.figwrap .cap{font-size:13.5px;color:var(--ink-soft);margin-top:8px;line-height:1.65;}
.figwrap svg text{font-family:var(--f-body);fill:var(--ink);}
.nl-axis{stroke:var(--line-strong);stroke-width:2;}
.nl-bs{fill:var(--ink);} .nl-int{fill:var(--gold);} .nl-ms{fill:var(--accent);stroke:var(--card);stroke-width:2;}
.nl-dim{stroke:var(--ink-soft);stroke-width:1;fill:none;}
.figwrap svg .nl-t{font-size:12.5px;font-weight:600;}
.figwrap svg .nl-d{font-family:var(--f-mono);font-size:11.5px;fill:var(--ink-soft);}
.figwrap svg .nl-d.near{fill:var(--gold);font-weight:700;}
.sf-cell{fill:var(--card);stroke:var(--line-strong);stroke-width:1;}
.sf-cell.home{stroke:var(--ink);stroke-width:1.5;}
.sf-sec{fill:var(--accent-soft);}
.sf-sec.on{fill:var(--accent);fill-opacity:.3;}
.sf-line{stroke:var(--ink-faint);stroke-width:1.2;stroke-dasharray:4 3;}
.sf-line.on{stroke:var(--gold);stroke-width:2.2;stroke-dasharray:none;}
.figwrap svg .sf-lab{font-family:var(--f-mono);font-size:9px;fill:var(--ink-faint);paint-order:stroke;stroke:var(--card);stroke-width:3px;}
.figwrap svg .sf-lab.on{fill:var(--gold);font-weight:700;font-size:9.5px;}
.sf-bs{fill:var(--ink);}
.sf-ms{fill:var(--accent);stroke:var(--card);stroke-width:1.5;}
.figwrap svg .sf-mslab{font-size:11px;font-weight:700;fill:var(--accent-ink);}
'''
if '.extra{' not in s:
    s = s.replace('@media (prefers-reduced-motion:reduce)', CSS + '\n@media (prefers-reduced-motion:reduce)', 1)

def replace_section(html, cid, new):
    start = html.index(f'    <section class="chapter" id="{cid}">')
    end = html.index('</section>', start) + len('</section>')
    return html[:start] + new.strip('\n') + html[end:]

# ------------------------------------------------------------------ CH5: add 5.3
CH5_ADD = '''
      <h3><span class="zh-num">5.3</span>路径损耗指数 n：信号衰减得有多快</h3>
      <p>后面几章会反复用到一个字母 <b>n</b>：同频干扰、小区分裂、扇区化都离不开它。它叫<b>路径损耗指数（path loss exponent）</b>，回答一个很具体的问题：<b>离基站远了以后，信号会弱多少？</b></p>
      <div class="formula-card">
        <div class="flbl">路径损耗指数（课件 p.84：2 ≤ n ≤ 5）</div>
        <div class="fexpr">P_r ∝ P_t · d⁻ⁿ = P_t / dⁿ</div>
        <div class="fmeaning">"∝"读作"正比于"，意思是只看比例，把天线增益、波长这些不随距离变化的常数先省掉。d⁻ⁿ 就是 1/dⁿ。所以<b>距离变成 2 倍，收到的功率就变成 1/2ⁿ</b>。n 越大，信号随距离掉得越快。</div>
      </div>

      <h4>先学会 dB：把"差几千倍"变成好算的数</h4>
      <p>无线信号的强弱经常差几百、几千甚至上万倍，直接写倍数很不方便，所以工程上用 <b>dB（分贝）</b>：</p>
      <div class="formula-card">
        <div class="flbl">dB 速成</div>
        <div class="fexpr">比值(dB) = 10 · log₁₀(比值)</div>
        <div class="fmeaning">只要记住两句：<b>乘 2 就加 3 dB，乘 10 就加 10 dB</b>；除法就是减。比如 16 = 2 × 2 × 2 × 2，所以 16 倍 = 3 + 3 + 3 + 3 = 12 dB；1/16 就是 −12 dB。</div>
      </div>
      <div class="tblwrap"><table><thead><tr><th>倍数</th><th>dB</th><th>倍数</th><th>dB</th></tr></thead><tbody>
        <tr><td>2 倍</td><td>+3 dB</td><td>1/2</td><td>−3 dB</td></tr>
        <tr><td>4 倍</td><td>+6 dB</td><td>1/4</td><td>−6 dB</td></tr>
        <tr><td>10 倍</td><td>+10 dB</td><td>1/10</td><td>−10 dB</td></tr>
        <tr><td>16 倍</td><td>+12 dB</td><td>1/16</td><td>−12 dB</td></tr>
        <tr><td>63 倍</td><td>+18 dB</td><td>1/100</td><td>−20 dB</td></tr>
      </tbody></table></div>
      <p>还有一个常见的单位 <b>dBm</b>：以 1 毫瓦（mW）为基准的 dB。0 dBm = 1 mW，30 dBm = 1 W，40 dBm = 10 W；第十章会出现的 −90 dBm 是 10⁻⁹ mW，也就是一万亿分之一瓦。手机收到的信号就是这么弱。</p>

      <h4>n 是怎么来的：课件里的三种环境</h4>
      <p><b>① 自由空间：n = 2（课件 p.50–51）。</b>想象空中挂着一个灯泡，光向四面八方均匀散开。距离 d 处，这些能量摊在一个半径为 d 的球面上，球面面积是 4πd²。距离变成 2 倍，球面面积变成 4 倍，每一小块面积分到的能量就只剩 1/4。课件的自由空间公式 P_R = P_T·G_T·G_R / L，其中 L = (4πd/λ)²，d 在分母上是<b>平方</b>，所以 n = 2。距离翻倍，信号掉 6 dB。</p>
      <p><b>② 平地双径模型：n = 4（课件 p.52–53）。</b>现实里有地面。手机收到两路信号：一路从基站直接过来，一路先打到地面再弹过来。距离很远时，两条路几乎一样长，而地面反射会把信号"翻个面"（课件写反射系数 R ≈ −1），两路信号一正一负，几乎互相抵消，剩下的一点点差值随距离衰减得更快。课件的结果是：</p>
      <div class="formula-card">
        <div class="flbl">平地双径模型，距离很远时（课件 p.53）</div>
        <div class="fexpr">P_R ≈ P_T·G_T·G_R·(h_T·h_R / d²)² ∝ 1/d⁴</div>
        <div class="fmeaning">h_T、h_R 是基站和手机的天线高度。课件原话是 "Path loss exponent of 4"，对应的损耗 L = 40 log d − 20 log(h_T·h_R)。距离翻倍，信号掉 12 dB。</div>
      </div>
      <div class="analogy">
        <div class="lbl">类比</div>
        <p>降噪耳机的原理是放出一段和噪音"正负相反"的声波，两者叠在一起几乎抵消。地面反射波就像那段反向的声波，把直射信号抵消掉了一大半。</p>
      </div>
      <p><b>③ 真实城区：n ≈ 3.5（课件 p.55、p.60）。</b>楼房遮挡、反射、散射太复杂，公式推不出来，只能实测以后拟合。课件的 CCIR 城区模型里，距离那一项是 (45 − 6.5 log h_T) × log d。基站天线高 30 m 时，6.5 × log₁₀30 = 6.5 × 1.477 = 9.6，斜率 = 45 − 9.6 = 35.4 dB/十倍距离，也就是 n = 3.54。课件还注明：天线高 5.9 m 时斜率正好是 40，即 n = 4。</p>
      <div class="tblwrap"><table><thead><tr><th>环境（课件 p.60）</th><th>斜率 γ = −10n</th><th>n</th><th>距离翻倍，信号掉</th></tr></thead><tbody>
        <tr><td>自由空间</td><td>−20</td><td>2</td><td>6.0 dB</td></tr>
        <tr><td>城区（CCIR，h_T = 30 m）</td><td>−35.4</td><td>3.54</td><td>10.7 dB</td></tr>
        <tr><td>平地双径</td><td>−40</td><td>4</td><td>12.0 dB</td></tr>
      </tbody></table></div>

      <div class="worked">
        <summary><span class="wtag">例题</span>同一部手机走远了，信号掉多少</summary>
        <div class="wbody">
          <p>已知条件：手机从离基站 1 km 的地方走到 2 km，再走到 10 km。分别按三种环境，算信号下降了多少 dB。</p>
          <div class="wstep"><div class="wn">1</div><div class="wtext">P_r ∝ d⁻ⁿ，两个距离的功率比是 (d₂/d₁)⁻ⁿ，换成 dB：<div class="calc">下降量 = 10 · n · log₁₀(d₂ / d₁)</div></div></div>
          <div class="wstep"><div class="wn">2</div><div class="wtext">1 km → 2 km，log₁₀2 = 0.301：<div class="calc">n = 2：6.0 dB；n = 3.54：10.7 dB；n = 4：12.0 dB</div></div></div>
          <div class="wstep"><div class="wn">3</div><div class="wtext">1 km → 10 km，log₁₀10 = 1：<div class="calc">n = 2：20 dB（弱 100 倍）；n = 3.54：35.4 dB（弱约 3500 倍）；n = 4：40 dB（弱 10000 倍）</div></div></div>
          <div class="wans">同样走到 10 km，自由空间只弱 100 倍，城区和平地要弱几千到一万倍。所以城区的蜂窝要做得小</div>
          <p style="margin-top:14px">反过来，n 大也有好处：远处同频小区的干扰同样衰减得快。第七章算同频干扰时会看到，课件例题一般取 n = 4。</p>
        </div>
      </div>
'''
ch5_start = s.index('    <section class="chapter" id="ch5">')
ch5_end = s.index('</section>', ch5_start)
if '路径损耗指数 n：信号衰减得有多快' not in s:
    s = s[:ch5_end] + CH5_ADD.lstrip('\n') + '    ' + s[ch5_end:]

# ------------------------------------------------------------------ CH7
NUMBER_LINE = '''<svg viewBox="0 0 640 140" role="img" aria-label="一条直线上：左边同频基站、你的基站、手机、右边同频基站，标出 R、D − R、D + R">
          <line class="nl-axis" x1="20" y1="66" x2="620" y2="66"/>
          <path class="nl-dim" d="M320 24 V30 M590 24 V30 M320 27 H590"/>
          <text class="nl-d" x="455" y="20" text-anchor="middle">D = 4.58 km</text>
          <circle class="nl-int" cx="50" cy="66" r="8"/><text class="nl-t" x="50" y="50" text-anchor="middle">左边同频基站</text>
          <rect class="nl-bs" x="313" y="59" width="14" height="14"/><text class="nl-t" x="300" y="50" text-anchor="middle">你的基站</text>
          <circle class="nl-ms" cx="379" cy="66" r="7"/><text class="nl-t" x="388" y="50" text-anchor="middle" style="fill:var(--accent-ink)">手机</text>
          <circle class="nl-int" cx="590" cy="66" r="8"/><text class="nl-t" x="590" y="50" text-anchor="middle">右边同频基站</text>
          <path class="nl-dim" d="M320 84 V92 M379 84 V92 M320 88 H379"/>
          <text class="nl-d" x="349" y="106" text-anchor="middle">R = 1</text>
          <path class="nl-dim" d="M379 84 V92 M590 84 V92 M379 88 H590"/>
          <text class="nl-d near" x="484" y="106" text-anchor="middle">D − R = 3.58 km（变近）</text>
          <path class="nl-dim" d="M50 114 V122 M379 114 V122 M50 118 H379"/>
          <text class="nl-d" x="214" y="136" text-anchor="middle">D + R = 5.58 km（变远）</text>
        </svg>'''

CH7 = '''
    <section class="chapter" id="ch7">
      <div class="chapter-head"><span class="chapter-num">第七章</span><h2>同频干扰与信道该怎么分配</h2></div>

      <h3><span class="zh-num">7.1</span>先弄懂 SIR：有用信号和干扰的比</h3>
      <p>频率复用带来容量，代价是用同一组频率的蜂窝之间会互相"听见"对方，造成<b>同频干扰</b>。衡量干扰严不严重的指标叫<b>信干比（SIR，Signal-to-Interference Ratio）</b>。</p>
      <div class="analogy">
        <div class="lbl">类比</div>
        <p>你在咖啡馆里和对面的朋友聊天。朋友的声音是"有用信号"，邻桌几个人的说话声是"干扰"。朋友声音越大、邻桌离你越远，你就听得越清楚。SIR 就是"朋友的声音"除以"所有邻桌声音加起来"。</p>
      </div>
      <div class="formula-card">
        <div class="flbl">信干比（课件 p.84）</div>
        <div class="fexpr">S/I = S / (I₁ + I₂ + … + I_m)</div>
        <div class="fmeaning">S 是从自己基站收到的有用信号，I₁、I₂…是各个同频小区传过来的干扰。课件的分母里还有噪声 N₀；蜂窝系统里干扰远大于噪声，所以先忽略噪声。每一路信号都按第五章的规律衰减：<b>离得越远越弱，按距离的 −n 次方变化</b>。</div>
      </div>
      <p>SIR 要多大才够？课件 p.89 说：<b>SIR 要大于 18 dB，语音质量才够好</b>。18 dB 是多少倍？10^(18/10) ≈ 63，意思是有用信号要比所有干扰加起来强 63 倍。</p>

      <h3><span class="zh-num">7.2</span>简化算法：6 个干扰都当成距离 D（课件 p.86–88）</h3>
      <p>先看课件 p.86 的图：中间红色那片是你所在的簇，蓝点是手机，站在自己小区 A 的边上；周围 6 个同样标着 A 的小区用同一组频率，6 条白色箭头就是 6 路干扰。</p>
      <p>课件 p.88 列了 5 条假设，逐条翻译：</p>
      <ol>
        <li>第一层同频干扰小区有 <b>6 个</b>：不管 N 是多少，同频小区围成一圈都正好 6 个。</li>
        <li>第二层离得远，<b>忽略不计</b>。</li>
        <li>手机站在<b>小区边缘</b>：这里离自己基站最远，有用信号最弱。</li>
        <li>手机到自己基站的距离是 <b>R</b>，到 6 个干扰基站的距离<b>都当作 D</b>（课件原文 "equidistant, D"）。</li>
        <li>D 比 R 大很多。</li>
      </ol>
      <div class="worked">
        <summary><span class="wtag">例题</span>一步步推出 S/I = Qⁿ/6，并算出 N = 7 的 SIR</summary>
        <div class="wbody">
          <p>已知条件：N = 7，n = 4，按课件 p.88 的假设计算。</p>
          <div class="wstep"><div class="wn">1</div><div class="wtext">有用信号：手机离自己基站 R：<div class="calc">S ∝ R⁻ⁿ</div></div></div>
          <div class="wstep"><div class="wn">2</div><div class="wtext">干扰：6 个基站都在距离 D，每个 ∝ D⁻ⁿ，加起来：<div class="calc">I ∝ 6 · D⁻ⁿ</div></div></div>
          <div class="wstep"><div class="wn">3</div><div class="wtext">两者相除。R⁻ⁿ / D⁻ⁿ 等于 Dⁿ / Rⁿ，也就是 (D/R)ⁿ：<div class="calc">S/I = R⁻ⁿ / (6 · D⁻ⁿ) = (D/R)ⁿ / 6 = Qⁿ / 6</div></div></div>
          <div class="wstep"><div class="wn">4</div><div class="wtext">第六章学过 Q = D/R = √(3N)。N = 7：<div class="calc">Q = √21 = 4.583</div></div></div>
          <div class="wstep"><div class="wn">5</div><div class="wtext">n = 4 时，√21 的四次方就是 21 的平方，不用开根号：<div class="calc">Q⁴ = 21² = 441，S/I = 441 / 6 = 73.5</div></div></div>
          <div class="wstep"><div class="wn">6</div><div class="wtext">换成 dB：<div class="calc">10 · log₁₀73.5 = 18.66 dB</div></div></div>
          <div class="wans">简化算法下，N = 7 的 SIR 是 18.66 dB：有用信号比 6 路干扰之和强 73.5 倍，刚过 18 dB 的门槛</div>
        </div>
      </div>
      <div class="formula-card">
        <div class="flbl">n = 4 时的捷径（HW1 Q2(b) 要你推的就是它）</div>
        <div class="fexpr">SIR(dB) = 1.76 + 20 · log₁₀N</div>
        <div class="fmeaning">把 Q = √(3N) 和 n = 4 代进 Qⁿ/6：(3N)² / 6 = 1.5N²。取 dB：10 log₁₀1.5 = 1.76，10 log₁₀N² = 20 log₁₀N。所以 1.76 dB 就是 N = 1 时的 SIR。</div>
      </div>

      <div class="worked">
        <summary><span class="wtag">例题</span>找到满足 10 dB 要求的最小簇大小（课件 p.89）</summary>
        <div class="wbody">
          <p>已知条件：系统要求 SIR 至少 10 dB，路径损耗指数 n = 4，按简化算法。求最小可用的簇大小 N。</p>
          <div class="wstep"><div class="wn">1</div><div class="wtext">N 只能取 1、3、4、7、9、12、13…（第六章），逐个代入 1.76 + 20 log₁₀N：</div></div>
          <div class="tblwrap"><table><thead><tr><th>N</th><th>SIR (dB)</th><th>≥ 10 dB？</th><th>≥ 18 dB？</th></tr></thead><tbody>
            <tr><td>1</td><td>1.76</td><td>✗</td><td>✗</td></tr>
            <tr><td>3</td><td>11.30</td><td>✓</td><td>✗</td></tr>
            <tr><td>4</td><td>13.80</td><td>✓</td><td>✗</td></tr>
            <tr><td>7</td><td>18.66</td><td>✓</td><td>✓</td></tr>
            <tr><td>9</td><td>20.85</td><td>✓</td><td>✓</td></tr>
            <tr><td>12</td><td>23.34</td><td>✓</td><td>✓</td></tr>
          </tbody></table></div>
          <div class="wstep"><div class="wn">2</div><div class="wtext">N = 3 是第一个超过 10 dB 的；N = 7 是第一个超过 18 dB 的。N 再大，质量更好，但每个蜂窝分到的信道更少。</div></div>
          <div class="wans">满足 10 dB 的最小簇是 N = 3；要达到语音质量的 18 dB，课件给的最优簇大小是 N = 7（"Optimum cluster size is 7"）</div>
        </div>
      </div>

      <h3><span class="zh-num">7.3</span>最坏情况：手机在边上，干扰离得不一样远（课件 p.91）</h3>
      <p>上面第 4 条假设其实不太对：手机站在小区边上，离自己基站有 R 那么远，它就不可能和 6 个干扰基站一样远。先只看一条直线上的情况：</p>
      <div class="figwrap">
        ''' + NUMBER_LINE + '''
        <div class="cap">取 R = 1 km、N = 7，则 D = √21 × 1 = 4.58 km。手机从自己基站往右走了 1 km，到了小区边上。</div>
      </div>
      <ul>
        <li>右边那个干扰基站：4.58 − 1 = <b>3.58 km</b>，变近了；</li>
        <li>左边那个：4.58 + 1 = <b>5.58 km</b>，变远了；</li>
        <li>上下方向那两个，距离大致还是 4.58 km。</li>
      </ul>
      <p>6 个干扰源里，<b>2 个变近、2 个变远、2 个基本不变</b>。这就是课件 p.91 Case 1 分母里 2(D−R)、2D、2(D+R) 三项的来历。</p>
      <p>一个变近、一个变远，能不能互相抵消？<b>不能</b>。先看一个更简单的例子：</p>
      <div class="worked">
        <summary><span class="wtag">小例子</span>两个音箱：一近一远，为什么总声音变大了</summary>
        <div class="wbody">
          <p>你站在两个音箱正中间，离每个都是 4 m。声音强度按 1/距离⁴ 算（和 n = 4 一样）。</p>
          <div class="wstep"><div class="wn">1</div><div class="wtext">站在中间：<div class="calc">1/4⁴ + 1/4⁴ = 1/256 + 1/256 = 0.0039 + 0.0039 = 0.0078</div></div></div>
          <div class="wstep"><div class="wn">2</div><div class="wtext">往右走 1 m，右边变 3 m，左边变 5 m：<div class="calc">1/3⁴ + 1/5⁴ = 1/81 + 1/625 = 0.0123 + 0.0016 = 0.0139</div></div></div>
          <div class="wstep"><div class="wn">3</div><div class="wtext">右边音箱从 0.0039 涨到 0.0123，多了 0.0084；左边音箱从 0.0039 降到 0.0016，只少了 0.0023。</div></div>
          <div class="wans">总声音从 0.0078 变成 0.0139，大了将近 1.8 倍。近的那个多出来的，远的那个补不回来</div>
        </div>
      </div>
      <p>原因在于 −4 次方这个规律：距离稍微缩短一点，强度就涨很多；距离拉长同样多，强度只降一点。同频干扰也是一样的道理。</p>

      <div class="worked">
        <summary><span class="wtag">例题</span>课件 p.91 Case 1：N = 7、n = 4 的最坏情况</summary>
        <div class="wbody">
          <p>已知条件：N = 7，n = 4。手机在小区边缘，6 个干扰源中 2 个在 D − R、2 个在 D、2 个在 D + R。</p>
          <div class="wstep"><div class="wn">1</div><div class="wtext">课件公式，分子分母同除以 R⁻ⁿ，距离都以 R 为单位：<div class="calc">S/I = 1 / [2(Q−1)⁻ⁿ + 2Q⁻ⁿ + 2(Q+1)⁻ⁿ]</div></div></div>
          <div class="wstep"><div class="wn">2</div><div class="wtext">三种距离：Q − 1 = 3.583，Q = 4.583，Q + 1 = 5.583。分别算每个干扰的强度：</div></div>
          <div class="tblwrap"><table><thead><tr><th>距离</th><th>距离⁴</th><th>每个干扰的强度</th><th>和"都在 D"比</th></tr></thead><tbody>
            <tr><td>D − R（变近）</td><td>3.583⁴ = 164.7</td><td>1/164.7 = 0.00607</td><td>2.7 倍</td></tr>
            <tr><td>D</td><td>4.583⁴ = 441</td><td>1/441 = 0.00227</td><td>1 倍</td></tr>
            <tr><td>D + R（变远）</td><td>5.583⁴ = 971.3</td><td>1/971.3 = 0.00103</td><td>0.45 倍</td></tr>
          </tbody></table></div>
          <div class="wstep"><div class="wn">3</div><div class="wtext">每种各 2 个，加起来：<div class="calc">2 × 0.00607 + 2 × 0.00227 + 2 × 0.00103 = 0.01874</div>对比简化算法的 6 × 0.00227 = 0.01361，总干扰多了约 38%。</div></div>
          <div class="wstep"><div class="wn">4</div><div class="wtext">取倒数，换成 dB：<div class="calc">S/I = 1 / 0.01874 = 53.4 → 10 log₁₀53.4 = 17.27 dB</div></div></div>
          <div class="wans">最坏情况 17.27 dB，比简化算法的 18.66 dB 低 1.4 dB，已经不到 18 dB 了</div>
        </div>
      </div>
      <p>课件还给了一个更保守的 <b>Case 2</b>，原文是 "To be conservative"，意思是往最坏处想：<b>6 个干扰全部按最近的 D − R 算</b>：</p>
      <div class="formula-card">
        <div class="flbl">Case 2（课件 p.91）</div>
        <div class="fexpr">S/I = 1 / [6(Q−1)⁻ⁿ] = (Q−1)ⁿ / 6</div>
        <div class="fmeaning">N = 7、n = 4：164.7 / 6 = 27.5 → <b>14.39 dB</b>。实际上 6 个干扰不可能同时都离你最近，所以 Case 2 是一个"保底值"：真实情况一定比它好。</div>
      </div>
      <div class="tblwrap"><table><thead><tr><th>算法</th><th>6 个干扰的距离</th><th>N = 7、n = 4</th><th>和 18 dB 比</th></tr></thead><tbody>
        <tr><td>简化（p.88）</td><td>都在 D</td><td>18.66 dB</td><td>刚过</td></tr>
        <tr><td>Case 1（p.91）</td><td>2 个 D−R、2 个 D、2 个 D+R</td><td>17.27 dB</td><td>不够</td></tr>
        <tr><td>Case 2（p.91）</td><td>都在 D−R</td><td>14.39 dB</td><td>差很多</td></tr>
      </tbody></table></div>
      <p>三种算法是同一个系统，只是对"干扰离多远"的假设一个比一个悲观，算出来的 SIR 一个比一个低。工程上要看最坏情况，是因为要保证小区里<b>每个位置</b>都能正常通话：最差的位置都达标，其他位置自然没问题。按 Case 1，N = 7 在小区边上已经不到 18 dB，这就是第九章要用扇区化提升 SIR 的原因。HW1 Q2(b)(iii) 给的公式就是这页的 Case 1。</p>
      <div class="checkpoint">
        <div class="lbl">停下来想一想</div>
        <p>为什么课件每次都假设手机在小区边上，而不是在小区中间？</p>
        <details class="reveal"><summary>点击看提示</summary>
          <div class="ans">手机在小区中间时，离自己基站很近，有用信号 S 很强，SIR 很高。越往边上走，S 越弱，而且离某几个干扰基站越近，SIR 越低。小区边上是最差的位置，按它来设计，整个小区都能保证达标。</div>
        </details>
      </div>

      <h3><span class="zh-num">7.4</span>信道怎么分给每个蜂窝：固定 vs 动态</h3>
      <p>算出了每个蜂窝该有多少个信道之后，还有一个问题：具体是<b>哪些</b>信道分给哪个蜂窝？两种思路：</p>
      <ul>
        <li><b>固定信道分配（FCA）</b>：每个蜂窝提前分配好一组固定信道，用完了就是用完了，哪怕隔壁蜂窝的信道还空着一大把，你也借不到——话务分布不均匀时会很浪费。</li>
        <li><b>动态信道分配（DCA）</b>：信道不永久属于某个蜂窝，谁有需要、谁就可以按需申请任何一个空闲信道，只要不违反"同频干扰约束"（也就是不能借用一个正在被复用距离范围内的邻居使用的信道）。DCA更灵活，但需要更复杂的中心调度算法。</li>
      </ul>
    </section>
'''
s = replace_section(s, 'ch7', CH7)

# ------------------------------------------------------------------ CH9
CH9 = '''
    <section class="chapter" id="ch9">
      <div class="chapter-head"><span class="chapter-num">第九章</span><h2>信道不够用了怎么办：小区分裂与扇区化</h2></div>

      <p>话务量涨上来、每个蜂窝的信道不够用时，课件给了两条路（p.135）：<b>小区分裂</b>——多建基站，把蜂窝做小；<b>扇区化</b>——不加基站，换定向天线压干扰。两者都能提升容量，但付出的代价完全不同。这一章每个结论都配一道可以自己算一遍的例题。</p>

      <h3><span class="zh-num">9.1</span>小区分裂——把大蜂窝拆成小蜂窝</h3>
      <p>把拥挤的蜂窝细分成更多、更小的微蜂窝，每个配一个天线更低、功率更小的基站（p.136）。每个基站的信道数不变，蜂窝变小了，<b>单位面积里的信道数</b>就多了。课件给了两种分法（p.138–139）：</p>
      <ul>
        <li><b>4:1 分裂</b>：新基站放在两个旧基站连线的中点，新半径 = <b>R/2</b>，面积变 1/4。N = 3、7、9 常用。</li>
        <li><b>3:1 分裂</b>：新基站放在三个旧蜂窝交界的角上，新半径 = <b>R/√3</b>，面积变 1/3。N = 4、7 常用。</li>
      </ul>
      <div class="formula-card">
        <div class="flbl">分裂后的发射功率（课件 p.136）</div>
        <div class="fexpr">P_t2 = P_t1 × (R_new / R_old)ⁿ</div>
        <div class="fmeaning">依据：分裂前后，蜂窝边缘收到的功率要一样，SIR 才能保持不变。边缘功率 ∝ P_t · R⁻ⁿ，所以<b>半径缩小多少倍，功率就要按 n 次方缩小</b>。</div>
      </div>
      <p>公式里的 <b>n</b> 就是第五章 5.3 节的路径损耗指数：信号按距离的 −n 次方衰减，所以半径的缩小比例要按 n 次方算进功率。不同环境下，半径减半要降的功率不一样：</p>
      <div class="tblwrap"><table><thead><tr><th>环境</th><th>n</th><th>半径减半，功率降为</th><th>降低</th></tr></thead><tbody>
        <tr><td>自由空间</td><td>2</td><td>1/4</td><td>6 dB</td></tr>
        <tr><td>城区（CCIR）</td><td>3.54</td><td>1/11.6</td><td>10.7 dB</td></tr>
        <tr><td>课件取值</td><td>4</td><td>1/16</td><td>12 dB</td></tr>
      </tbody></table></div>
      <p>为什么"边缘功率一样，SIR 就不变"？可以这样想：分裂后整片区域按同一个比例缩小，簇大小 N 不变，所以 Q = D/R 也不变。所有微蜂窝都按同一个规则降功率，那么手机在新蜂窝里任何一个对应位置收到的有用信号和干扰，都和分裂前一样强，比值自然不变。</p>

      <div class="worked">
        <summary><span class="wtag">例题</span>验证"半径减半，功率要降 12 dB"（课件 p.136）</summary>
        <div class="wbody">
          <p>已知条件：4:1 分裂，微蜂窝半径是原来的一半，路径损耗指数 n = 4。求微蜂窝基站要把发射功率降低多少。</p>
          <div class="wstep"><div class="wn">1</div><div class="wtext">让两种蜂窝边缘的接收功率相等：<div class="calc">P_t1 · R⁻⁴ = P_t2 · (R/2)⁻⁴</div></div></div>
          <div class="wstep"><div class="wn">2</div><div class="wtext">(R/2)⁻⁴ = 16 · R⁻⁴，整理：<div class="calc">P_t2 = P_t1 / 16</div></div></div>
          <div class="wstep"><div class="wn">3</div><div class="wtext">换成 dB，16 = 2 × 2 × 2 × 2，每个 2 是 3 dB：<div class="calc">10 log₁₀16 = 12.04 dB</div></div></div>
          <div class="wstep"><div class="wn">4</div><div class="wtext">换个条件再验证一次。3:1 分裂，半径是 R/√3：<div class="calc">P_t2 = P_t1 · (1/√3)⁴ = P_t1 / 9 → 降 9.54 dB</div></div></div>
          <div class="wans">4:1、n = 4 时功率降为 1/16，即 −12 dB，与课件一致。降多少取决于半径比和 n 两个量，不是固定的 12 dB</div>
        </div>
      </div>

      <div class="worked">
        <summary><span class="wtag">例题</span>验证"分裂后容量变 4 倍"（课件 p.140–142）</summary>
        <div class="wbody">
          <p>已知条件：每个基站固定用 60 条信道，原蜂窝半径 1 km，微蜂窝半径 0.5 km。求以基站 A 为中心的 3 km × 3 km 正方形里有多少条信道：(a) 不用微蜂窝；(b) 用微蜂窝。</p>
          <div class="wstep"><div class="wn">1</div><div class="wtext">正方形从 A 向上下左右各延伸 1.5 km。按课件的图数，里面约有 <b>4 个</b>原蜂窝的基站：<div class="calc">4 × 60 = 240 条</div></div></div>
          <div class="wstep"><div class="wn">2</div><div class="wtext">半径减半，面积变 1/4，同样面积最多能放 4 × 4 = 16 个微蜂窝。按图数，正方形里约有 15 个基站：<div class="calc">15 × 60 = 900 条</div></div></div>
          <div class="wstep"><div class="wn">3</div><div class="wtext">再用 Erlang B 验证"能服务的话务量"也是 4 倍。GoS = 2% 时查表，60 条信道能承载 49.6 Erlang，中继效率 49.6 / 60 = 0.83。分裂后，原来一个蜂窝的面积里有 4 个微蜂窝，每个仍是 60 条信道：<div class="calc">4 × 49.6 = 198.4 Erlang（原来 49.6）</div>每个微蜂窝的信道池没变小，中继效率仍是 0.83。</div></div>
          <div class="wans">信道数 240 → 900，约 4 倍；话务量 49.6 → 198.4 Erlang，正好 4 倍，而且中继效率不变。这就是课件 p.135 说小区分裂 "without suffering from trunking efficiency" 的原因</div>
        </div>
      </div>

      <p>代价有两项。一是要新建基站，成本高。二是切换变多：蜂窝越小，手机越频繁地穿过边界。课件 p.139 给的经验值是<b>半径缩小到 1/4，每个用户的切换率涨到约 10 倍</b>，这是运营商决定要不要分裂时必须算的账。</p>

      <div class="extra">
        <div class="lbl">课外补充 · 课件没有推导</div>
        <p><b>为什么是 10 倍，而不是 4 倍？</b>只看几何的话，手机走同样一段路，穿过的蜂窝边界数和半径成反比：半径缩小到 1/4，边界多 4 倍，切换也只多 4 倍。课件的 10 倍是工程经验值，没有给推导，它比几何估算大，说明实际切换增加得比"边界变多"还要快。考试按课件写"约 10 倍"即可。</p>
      </div>

      <h3><span class="zh-num">9.2</span>扇区化——同一个基站，换一副"眼睛"</h3>
      <p>另一条路是<b>扇区化（sectoring）</b>：不新建基站，把全向天线换成几个指向不同方向的定向天线，最常见是 3 个 120° 扇区或 6 个 60° 扇区（p.143）。</p>
      <div class="analogy">
        <div class="lbl">类比</div>
        <p>全向天线像是站在房间中央大声喊话，四面八方的人都能听到你、你也会被四面八方的噪音干扰；扇区化则像是用一个喇叭对着一个方向喊，声音更集中，也只需要担心正前方那个方向传来的干扰声。</p>
      </div>

      <h4>为什么干扰源从 6 个变成 2 个</h4>
      <p>课件 p.143 的图里，每个六边形切成 3 个菱形扇区，编号 1、2、3。关键有两点：</p>
      <ol>
        <li><b>所有小区的扇区朝向都一样</b>：每个小区的 1 号扇区都朝同一个方向；</li>
        <li><b>同频小区的同号扇区用同一组信道</b>：你在 1 号扇区，能用同一组信道发射的，只有各同频小区的 1 号扇区天线。</li>
      </ol>
      <p>这些 1 号天线全都朝同一个方向，只照得到自己前方 120° 的范围。于是：</p>
      <ul>
        <li>位于你<b>后方</b>的同频基站，天线正好朝着你，照得到你 → <b>有干扰</b>；</li>
        <li>位于你<b>前方</b>的同频基站，天线背对着你，照不到你 → <b>没有干扰</b>。</li>
      </ul>
      <p>第一层 6 个同频小区每隔 60° 一个，"后方 120°"的范围里只放得下 2 个。60° 扇区的范围更窄，只剩 1 个。课件 p.144 的图里那两条虚线，画的就是这两路干扰。</p>
      <div class="figwrap">
        ''' + SECTOR_SVG + '''
        <div class="cap">按 N = 7、半径 R 精确画出。浅色菱形是各小区的 1 号扇区，朝向全都一样；深色的是能照到手机的两个。手机站在自己 1 号扇区最远的那个角上，这是最坏的位置。实线是照得到手机的 2 路干扰，虚线是被挡掉的 4 路。</div>
      </div>
      <p>注意被挡掉的是哪几个：离手机最近的 3.61R 和 4.00R 两个，恰好都在手机前方，被挡掉了。剩下两个都在手机身后，距离不小于约 D。这就是为什么扇区化的公式里<b>没有 (Q−1) 这一项</b>，SIR 提升得这么明显。</p>
      <div class="formula-card">
        <div class="flbl">扇区化的最坏情况 SIR（课件 p.145）</div>
        <div class="fexpr">120°：S/I = 1 / [Q⁻ⁿ + (Q+0.7)⁻ⁿ]<br>60°：&nbsp;S/I = (Q+0.7)ⁿ</div>
        <div class="fmeaning">分母里有几项，就是还剩几个干扰源。全向时 6 个干扰都按 D 算、合并成 6·D⁻ⁿ，所以有"÷6"；扇区化后剩下的两个距离不同（D 和 D + 0.7R），没法合并，只能写成两项相加。60° 只剩一项。</div>
      </div>

      <div class="extra">
        <div class="lbl">课外补充 · 课件没有推导</div>
        <p><b>0.7R 是怎么来的？</b>课件 p.145 直接给了 D 和 D + 0.7R，没说怎么来的。我按上面那张图的几何精确算了一遍：手机站在 1 号扇区最远的角上，离自己基站 R，两个照得到它的同频基站分别在 <b>5.29R</b> 和 <b>4.36R</b> 处。D = √21 R = 4.58R，所以：</p>
        <ul>
          <li>5.29R = D + 0.71R → 就是课件的 <b>D + 0.7R</b>；</li>
          <li>4.36R = D − 0.22R → 课件近似成 <b>D</b>。</li>
        </ul>
        <p>按精确距离算，SIR = 1 / (1/4.36⁴ + 1/5.29⁴) ≈ 23.9 dB；课件公式给 24.5 dB，偏乐观约 0.6 dB。课件 p.144 写的"约 23 dB"反而更接近精确值。考试按 p.145 的公式写即可。</p>
      </div>

      <div class="worked">
        <summary><span class="wtag">例题</span>验证扇区化的 SIR 提升（N = 7，n = 4）</summary>
        <div class="wbody">
          <p>已知条件：7 小区复用，n = 4。分别算全向、120° 扇区、60° 扇区的 SIR，看提升了多少。</p>
          <div class="wstep"><div class="wn">1</div><div class="wtext">先把要用的几个数算好：<div class="calc">Q = √21 = 4.583，Q⁴ = 441，(Q−1)⁴ = 164.7，(Q+1)⁴ = 971.3，(Q+0.7)⁴ = 5.283⁴ = 778.7</div></div></div>
          <div class="wstep"><div class="wn">2</div><div class="wtext">全向，简化算法（第七章 7.2，6 个干扰都在 D）：<div class="calc">S/I = 441 / 6 = 73.5 → 18.66 dB</div></div></div>
          <div class="wstep"><div class="wn">3</div><div class="wtext">全向，最坏情况（第七章 7.3，课件 p.91 Case 1）：<div class="calc">S/I = 1 / (2/164.7 + 2/441 + 2/971.3) = 53.4 → 17.27 dB</div></div></div>
          <div class="wstep"><div class="wn">4</div><div class="wtext">120° 扇区：<div class="calc">S/I = 1 / (1/441 + 1/778.7) = 281.6 → 24.50 dB</div></div></div>
          <div class="wstep"><div class="wn">5</div><div class="wtext">60° 扇区：<div class="calc">S/I = 778.7 → 28.91 dB</div></div></div>
          <div class="tblwrap"><table><thead><tr><th>天线</th><th>干扰源</th><th>S/I</th><th>SIR</th><th>比全向最坏情况</th></tr></thead><tbody>
            <tr><td>全向（简化）</td><td>6</td><td>73.5</td><td>18.66 dB</td><td>—</td></tr>
            <tr><td>全向（最坏）</td><td>6</td><td>53.4</td><td>17.27 dB</td><td>基准</td></tr>
            <tr><td>120° 扇区</td><td>2</td><td>281.6</td><td>24.50 dB</td><td>+7.2 dB</td></tr>
            <tr><td>60° 扇区</td><td>1</td><td>778.7</td><td>28.91 dB</td><td>+11.6 dB</td></tr>
          </tbody></table></div>
          <div class="wans">120° 扇区 24.5 dB、60° 扇区 28.9 dB，与课件 p.145 一致</div>
        </div>
      </div>

      <p>SIR 提升后能换来什么？课件 p.144 的算法是：120° 扇区下 N = 7 的 SIR（24.5 dB）已经超过全向 N = 12 的水平（简化算法 23.3 dB）。本来要 12 个蜂窝一簇才够的干扰要求，现在 7 个一簇就满足了，每个蜂窝分到的信道变成 12/7 = <b>1.714 倍</b>。</p>

      <div class="worked">
        <summary><span class="wtag">例题</span>验证扇区化的代价：中继效率下降（课件 p.148–149）</summary>
        <div class="wbody">
          <p>已知条件：呼损制系统，GoS ≤ 1%，平均通话 2 分钟，每用户每小时 1 次。7 小区复用共 395 条业务信道，每蜂窝 57 条。比较不分扇区、120°、60° 时每蜂窝每小时能处理多少次呼叫。</p>
          <div class="wstep"><div class="wn">1</div><div class="wtext">换算：一次通话 2 分钟，每 Erlang 每小时能接 30 次通话：<div class="calc">每小时呼叫数 = A × 60 / 2 = A × 30</div></div></div>
          <div class="wstep"><div class="wn">2</div><div class="wtext">不分扇区：57 条信道一个池，查表 GoS 1%：<div class="calc">A = 44.2 E → 44.2 × 30 = 1326 次/小时</div></div></div>
          <div class="wstep"><div class="wn">3</div><div class="wtext">120°：每扇区 57 / 3 = 19 条，查表：<div class="calc">A = 11.2 E/扇区 × 3 = 33.6 E → 1008 次/小时</div></div></div>
          <div class="wstep"><div class="wn">4</div><div class="wtext">60°：每扇区 57 / 6 = 9.5 条，取 M = 9 和 10 的表值平均：<div class="calc">(3.78 + 4.46) / 2 = 4.12 E/扇区 × 6 = 24.7 E → 741 次/小时</div></div></div>
          <div class="tblwrap"><table><thead><tr><th>方式</th><th>每池信道</th><th>每蜂窝话务量</th><th>中继效率</th><th>呼叫/小时</th><th>变化</th></tr></thead><tbody>
            <tr><td>不分扇区</td><td>57</td><td>44.2 E</td><td>0.78</td><td>1326</td><td>—</td></tr>
            <tr><td>120° 扇区</td><td>19 × 3</td><td>33.6 E</td><td>0.59</td><td>1008</td><td>−24%</td></tr>
            <tr><td>60° 扇区</td><td>9.5 × 6</td><td>24.7 E</td><td>0.43</td><td>741</td><td>−44%</td></tr>
          </tbody></table></div>
          <div class="wans">总信道数没变，只是被切成小池子：120° 少了 24%，60° 少了 44%，与课件一致。这就是第八章"集群增益"反过来的效果</div>
        </div>
      </div>

      <p>一边提升 SIR，一边又损失中继效率，扇区化到底划不划算？关键看提升出来的 SIR 怎么用：<b>只有拿它去缩小簇大小 N，扇区化才真正增加容量。</b></p>

      <div class="extra">
        <div class="lbl">课外补充 · 课件没有这道题</div>
        <p>下面这道题是我用课件的公式和 Erlang B 表构造的，把"SIR 提升"和"中继效率损失"两笔账放在一起算。</p>
        <div class="worked">
          <summary><span class="wtag">例题</span>验证"扇区化 + 缩小簇"的净收益</summary>
          <div class="wbody">
            <p>已知条件：沿用上题，395 条业务信道，GoS 1%，n = 4。方案甲：全向天线、N = 7。方案乙：120° 扇区、N = 4。比较两个方案的最坏情况 SIR 和每蜂窝话务量。</p>
            <div class="wstep"><div class="wn">1</div><div class="wtext">方案甲的结果上面都算过了：<div class="calc">最坏 SIR = 17.27 dB；57 条信道 → 44.2 E/蜂窝</div></div></div>
            <div class="wstep"><div class="wn">2</div><div class="wtext">方案乙先算 SIR。N = 4 时 Q = √12 = 3.464：<div class="calc">S/I = 1 / (1/3.464⁴ + 1/4.164⁴) = 1 / (1/144 + 1/300.7) = 97.4 → 19.9 dB</div>比方案甲的 17.3 dB 还高。如果 N = 4 不分扇区，最坏情况只有 11.4 dB，根本不能用。</div></div>
            <div class="wstep"><div class="wn">3</div><div class="wtext">方案乙再算容量。每蜂窝 395 / 4 = 98.75，取 98 条，分到 3 个扇区是 33 + 33 + 32 条，查表 GoS 1%：<div class="calc">22.9 + 22.9 + 22.0 = 67.8 E/蜂窝</div></div></div>
            <div class="wstep"><div class="wn">4</div><div class="wtext">比较：<div class="calc">67.8 / 44.2 = 1.53</div></div></div>
            <div class="wans">方案乙每蜂窝多承载 53% 的话务量，最坏情况 SIR 还从 17.3 dB 升到 19.9 dB。中继效率的损失被"簇变小、每蜂窝信道变多"抵消还有余</div>
          </div>
        </div>
      </div>

      <div class="checkpoint">
        <div class="lbl">停下来想一想</div>
        <p>60° 扇区的 SIR 比 120° 还高 4.4 dB，为什么实际网络里最常见的反而是 3 扇区？</p>
        <details class="reveal"><summary>点击看提示</summary>
          <div class="ans">看上面的例题：60° 扇区在 N = 7 时中继效率损失 44%，每扇区只有 9–10 条信道；扇区边界多了一倍，切换更频繁，天线和射频设备也要 6 套。120° 扇区在 SIR 提升和中继效率之间折中得最好。</div>
        </details>
      </div>

      <h3><span class="zh-num">9.3</span>两种方法放在一起比</h3>
      <div class="tblwrap"><table><thead><tr><th></th><th>小区分裂</th><th>扇区化</th></tr></thead><tbody>
        <tr><td>怎么做</td><td>加基站，把蜂窝做小</td><td>基站不变，换定向天线</td></tr>
        <tr><td>SIR</td><td>不变（靠降功率保持）</td><td>升高：120° 约 +7 dB，60° 约 +12 dB</td></tr>
        <tr><td>中继效率</td><td>不变（每站信道数不变）</td><td>下降：120° −24%，60° −44%</td></tr>
        <tr><td>容量从哪来</td><td>单位面积里基站更多：4:1 分裂 ×4</td><td>SIR 余量换更小的 N：12/7 = 1.714 倍（p.144）</td></tr>
        <tr><td>代价</td><td>建站成本；半径 ÷4 时切换约 ×10</td><td>扇区间切换增多；天线和设备更多</td></tr>
      </tbody></table></div>
    </section>
'''
s = replace_section(s, 'ch9', CH9)

# ------------------------------------------------------------------ CH10
CH10 = '''
    <section class="chapter" id="ch10">
      <div class="chapter-head"><span class="chapter-num">第十章</span><h2>切换与功率控制：让你在移动中感觉不到任何变化</h2></div>

      <p>第九章的两种扩容方法都有同一个副作用：蜂窝和扇区越小，手机越频繁地跨越边界，<b>切换（handover / handoff）</b>就越多（p.150）。这一章讲切换怎么触发、怎么避免掉话，以及功率控制怎么压住干扰。课件这部分（p.150–158）只讲概念，没有数值例题；为了帮助理解，我补了几道用数字说话的例题，都放在紫色的"课外补充"框里。</p>

      <h3><span class="zh-num">10.1</span>什么是切换</h3>
      <p>切换就是把一通正在进行的通话，从一个业务信道（频率、时隙或码）换到另一个上，起因通常是信号变弱（p.150）。课件分两类：</p>
      <ul>
        <li><b>小区内切换（intra-cell）</b>：同一个基站内换信道，比如当前信道干扰大，为了改善质量。</li>
        <li><b>小区间切换（inter-cell）</b>：手机从一个基站移动到同一 MSC 下的另一个基站，通话不断。</li>
      </ul>
      <p>一次切换要找到新基站，并在新基站上同时分配话音/数据信道和对应的控制信道。课件对它的要求是四个词：<b>transparent、uninterrupted、infrequent、successful</b>——用户感觉不到、不中断、不频繁、要成功。</p>

      <h3><span class="zh-num">10.2</span>什么时候触发：切换裕量 Δ</h3>
      <div class="formula-card">
        <div class="flbl">切换裕量（课件 p.153）</div>
        <div class="fexpr">Δ = P_HO − P_min</div>
        <div class="fmeaning">P_min 是基站维持可接受通话所需的最低信号强度，课件给的是 −90 到 −100 dBm（dBm 见第五章 5.3：−90 dBm 是一万亿分之一瓦）。P_HO 是触发切换的门限，比 P_min 略高。信号一降到 P_HO 就开始切换，到 P_min 之前必须完成。所以 <b>Δ 就是留给切换过程的"缓冲"</b>。</div>
      </div>
      <div class="analogy">
        <div class="lbl">类比</div>
        <p>手机电量剩 20% 时会提醒你充电（这就是 P_HO），到 0% 才关机（这就是 P_min），中间这 20% 就是 Δ。提醒得太早，比如 60% 就开始提醒，你会被不停打扰，其实还早得很；提醒得太晚，比如 2% 才提醒，你还没找到充电器手机就关机了。</p>
      </div>
      <p>课件 p.153 留了两个问题："If Δ is too large, ?" 和 "If Δ is too small, ?"。按上面的思路回答：</p>
      <ul>
        <li><b>Δ 太大</b>：信号还很好时就开始切换，原基站其实还能服务，造成不必要的切换，加重 MSC 的负担。</li>
        <li><b>Δ 太小</b>：信号快到 P_min 才开始切换，没有足够时间完成，通话掉线。p.153 列出的掉话原因里正好有这一条（"no enough time due to small Δ"）。</li>
      </ul>

      <div class="extra">
        <div class="lbl">课外补充 · 用数字验证 Δ 的取值</div>
        <div class="worked">
          <summary><span class="wtag">例题</span>Δ 太小会掉话、太大会白切换</summary>
          <div class="wbody">
            <p>假设：手机沿直线远离基站，在 2 km 处信号正好降到 P_min；路径损耗指数 n = 4，不考虑阴影衰落；MSC 完成一次切换需要约 10 s（1G 模拟系统的典型值，出自课件参考书 Rappaport 第 3 章）。车速分别取 60 km/h 和 120 km/h。</p>
            <div class="wstep"><div class="wn">1</div><div class="wtext">接收功率按 10n log₁₀d 衰减（第五章 5.3）。信号比 P_min 高 Δ dB 的位置：<div class="calc">d_HO = d_min × 10^(−Δ / 10n) = 2000 × 10^(−Δ / 40) m</div></div></div>
            <div class="wstep"><div class="wn">2</div><div class="wtext">从触发切换到掉到 P_min，手机还能走 d_min − d_HO，除以车速就是留给切换的时间。以 Δ = 2 dB 为例：<div class="calc">d_HO = 2000 × 10^(−0.05) = 1782 m → 余量 218 m → 60 km/h（16.7 m/s）时 218 / 16.7 = 13 s</div></div></div>
            <div class="wstep"><div class="wn">3</div><div class="wtext">换几个 Δ 列成表（✓ 表示时间够 10 s）：</div></div>
            <div class="tblwrap"><table><thead><tr><th>Δ</th><th>开始切换的位置</th><th>距离余量</th><th>60 km/h</th><th>120 km/h</th></tr></thead><tbody>
              <tr><td>0.5 dB</td><td>1943 m</td><td>57 m</td><td>3.4 s ✗</td><td>1.7 s ✗</td></tr>
              <tr><td>1 dB</td><td>1888 m</td><td>112 m</td><td>6.7 s ✗</td><td>3.4 s ✗</td></tr>
              <tr><td>2 dB</td><td>1782 m</td><td>218 m</td><td>13.0 s ✓</td><td>6.5 s ✗</td></tr>
              <tr><td>3 dB</td><td>1683 m</td><td>317 m</td><td>19.0 s ✓</td><td>9.5 s ✗</td></tr>
              <tr><td>6 dB</td><td>1416 m</td><td>584 m</td><td>35.0 s ✓</td><td>17.5 s ✓</td></tr>
              <tr><td>12 dB</td><td>1002 m</td><td>998 m</td><td>59.9 s ✓</td><td>29.9 s ✓</td></tr>
            </tbody></table></div>
            <div class="wstep"><div class="wn">4</div><div class="wtext">要留够 10 s，反推最小的 Δ：<div class="calc">60 km/h：余量 167 m → Δ ≥ 1.5 dB；120 km/h：余量 333 m → Δ ≥ 3.2 dB</div></div></div>
            <div class="wans">Δ ≤ 1 dB 时来不及切换就掉线，车越快需要的 Δ 越大；Δ = 12 dB 时，手机才走到一半的 1 km 处就开始切换，是白切</div>
            <p style="margin-top:14px">这个模型没算阴影衰落。实际信号会随机起伏好几 dB，所以 1G 系统实际取 6–12 dB，切换更快的 GSM 取 0–6 dB（Rappaport 第 3 章）。</p>
          </div>
        </div>
      </div>

      <p>Δ 设得合适也不能保证不掉话。课件 p.153 列了切换掉话的三种情况：</p>
      <ul>
        <li>新小区<b>没有空闲信道</b>；</li>
        <li>MSC 处理<b>太慢</b>，或者 Δ 太小、来不及完成切换；</li>
        <li>切换执行过程中，<b>目标链路本身出了问题</b>。</li>
      </ul>

      <h3><span class="zh-num">10.3</span>硬切换 vs 软切换：先断后连，还是先连后断</h3>
      <ul>
        <li><b>硬切换（"break before make"，p.154）</b>：先释放旧基站的信道，再建立新基站的信道。实现简单，但有短暂中断，可能掉话。用在 FDMA/TDMA 系统（GSM、IS-136），因为这类手机同一时间通常只能锁定一个信道。</li>
        <li><b>软切换（"make before break"，p.155）</b>：新旧两条信道并行建立、同时使用，等新链路稳定再断旧的。通话不中断，而且<b>边界处同时有两条链路，形成分集</b>（课件原文 "boundary conditions improved due to availability of diversity"），信号更可靠。代价是这段时间占用两份资源。用在 CDMA 系统（IS-95、WCDMA、cdma2000），因为 CDMA 用户靠码区分，所有基站用同一频段，手机天然可以同时连两个基站。</li>
      </ul>
      <div class="analogy">
        <div class="lbl">类比</div>
        <p>硬切换像过河时先松开这边的扶手、再去抓对岸的扶手，中间有一瞬间两手都是空的；软切换像先抓住对岸的扶手、确认抓稳了，再松开这边的。</p>
      </div>

      <div class="extra">
        <div class="lbl">课外补充 · 用数字理解"分集"</div>
        <div class="worked">
          <summary><span class="wtag">例题</span>软切换在边界处为什么更可靠</summary>
          <div class="wbody">
            <p>假设：手机在两个基站的边界，受阴影衰落影响，每条链路有 10% 的时间信号低于可用门限，两条链路的衰落相互独立。</p>
            <div class="wstep"><div class="wn">1</div><div class="wtext">硬切换任一时刻只连一个基站，中断概率就是这一条链路的：<div class="calc">P_中断 = 10%</div></div></div>
            <div class="wstep"><div class="wn">2</div><div class="wtext">软切换同时连两个基站，只有两条<b>同时</b>不可用才会中断：<div class="calc">P_中断 = 0.1 × 0.1 = 1%</div></div></div>
            <div class="wstep"><div class="wn">3</div><div class="wtext">代价：处在软切换中的通话占两个基站的资源。如果某一时刻有 30% 的通话处在软切换中：<div class="calc">平均每通话占用 0.7 × 1 + 0.3 × 2 = 1.3 条链路</div>同样多的资源，能同时服务的通话只有原来的 1 / 1.3 ≈ 77%。</div></div>
            <div class="wans">边界处的中断概率从 10% 降到 1%，换来约 30% 的额外资源开销</div>
            <p style="margin-top:14px">"两条链路独立"是理想化假设。实际两条路径的阴影衰落有一定相关性，改善没有这么多，但方向不变。</p>
          </div>
        </div>
      </div>

      <h3><span class="zh-num">10.4</span>优先保住正在进行的通话</h3>
      <p>对用户来说，打电话时"打不通"（新呼叫被阻塞）只是有点烦，"通话中突然断了"（切换掉话）要糟糕得多。所以课件 p.156 规定：<b>切换呼叫比新呼叫优先</b>。两种做法：</p>
      <ul>
        <li><b>切换排队（handover queuing）</b>：信道全忙时，切换请求先放进缓冲区等一会儿，缓冲区满了才丢弃。手机在 Δ 对应的那段距离里还能维持通话，正好有时间等。</li>
        <li><b>信道预留（handover reservation）</b>：留出 r 条信道只给切换用。空闲信道数 ≤ r 时，新呼叫就被拒绝，只接受切换呼叫。</li>
      </ul>
      <div class="analogy">
        <div class="lbl">类比</div>
        <p>信道预留就像公交车上的"老弱病残孕专座"：平时空着别人不能坐，留给最需要的人。代价是普通乘客能坐的位子少了。</p>
      </div>

      <div class="extra">
        <div class="lbl">课外补充 · 拓展计算</div>
        <div class="worked">
          <summary><span class="wtag">例题</span>预留几条信道，切换掉话能降多少</summary>
          <div class="wbody">
            <p>假设：一个蜂窝 M = 10 条信道，新呼叫话务量 5 Erlang，从邻区切换进来的话务量 1 Erlang。比较预留 r = 0、1、2、3 条信道时两种呼叫的失败概率。用的模型和第八章的 Erlang B 是同一套"生灭过程"。</p>
            <div class="wstep"><div class="wn">1</div><div class="wtext">设 p_k 为 k 条信道忙的概率。忙信道少于 M − r 条时，新呼叫和切换都能进来，到达话务量是 5 + 1 = 6 E；达到 M − r 条以后，只有切换能进来，到达话务量是 1 E：<div class="calc">p_k = p_(k−1) × (到达话务量) / k，最后把所有 p_k 归一化</div></div></div>
            <div class="wstep"><div class="wn">2</div><div class="wtext">新呼叫被阻塞 = 忙信道 ≥ M − r 的概率之和；切换掉话 = 10 条全忙的概率 p_10。</div></div>
            <div class="wstep"><div class="wn">3</div><div class="wtext">先验证模型：r = 0 时两类呼叫一视同仁，就是普通的 Erlang B，10 条信道、6 E：<div class="calc">P_B = 4.31%，与 Erlang B 公式结果一致</div></div></div>
            <div class="tblwrap"><table><thead><tr><th>预留 r</th><th>新呼叫阻塞</th><th>切换掉话</th></tr></thead><tbody>
              <tr><td>0</td><td>4.31%</td><td>4.31%</td></tr>
              <tr><td>1</td><td>8.20%</td><td>0.75%</td></tr>
              <tr><td>2</td><td>13.48%</td><td>0.13%</td></tr>
              <tr><td>3</td><td>20.57%</td><td>0.025%</td></tr>
            </tbody></table></div>
            <div class="wans">只预留 1 条，切换掉话从 4.31% 降到 0.75%（约 1/6），新呼叫阻塞从 4.31% 升到 8.20%。所以 r 通常只取 1–2 条</div>
          </div>
        </div>
      </div>

      <h3><span class="zh-num">10.5</span>功率控制：既要够用，又不要浪费</h3>
      <p>限制蜂窝容量的一个主要因素是同频干扰（p.157）。功率控制的思路很简单：<b>信号太弱就加功率，太强就减功率</b>，谁都不用比"刚好够"更多的功率。好处有两个：手机更省电，对别人的干扰也更小。</p>
      <p>具体做法（p.158）：</p>
      <ol>
        <li>接收端持续估计收到的 SIR：下行由手机估计，上行由基站估计；</li>
        <li>信道好、SIR 比要求的高 → 命令发射端<b>降</b>功率；</li>
        <li>信道差、SIR 比要求的低 → 命令发射端<b>升</b>功率。</li>
      </ol>
      <p>课件 p.28 提到，CDMA 的功率控制每 <b>1 ms</b> 调整一次，而且是 CDMA 容量提升的两个关键之一（"all transmitters are under SS precise power control"）。</p>
      <div class="analogy">
        <div class="lbl">类比</div>
        <p>功率控制像开会时大家调音量：离麦克风近的人说小声点，离得远的人说大声点，让主持人听到每个人的音量都差不多，谁也不会把别人盖住。</p>
      </div>

      <div class="extra">
        <div class="lbl">课外补充 · 远近效应：CDMA 为什么离不开功率控制</div>
        <p>CDMA 的所有用户同时用同一频段，基站同时收所有人的信号。离基站近的手机信号强得多，会把远处手机的信号淹没，这叫<b>远近效应（near-far problem）</b>。课件只说 CDMA 要精确功率控制，没有讲这个名词，下面两道题用数字说明它有多严重。参数取 IS-95 的典型值：码片速率 1.2288 Mchip/s，话音速率 9.6 kbit/s，要求解扩后 SIR ≥ 7 dB。</p>
        <div class="worked">
          <summary><span class="wtag">例题</span>没有功率控制时，远处用户无法通信</summary>
          <div class="wbody">
            <p>假设：两部手机用同样的发射功率，一部离基站 100 m，一部离基站 1 km，n = 4。</p>
            <div class="wstep"><div class="wn">1</div><div class="wtext">两个信号到达基站的功率比：<div class="calc">(1000 / 100)⁴ = 10⁴ → 近处手机强 40 dB</div></div></div>
            <div class="wstep"><div class="wn">2</div><div class="wtext">所以远处手机解扩前的 SIR 是 −40 dB。扩频的处理增益（解扩能把有用信号相对干扰放大的倍数）：<div class="calc">G_p = 1.2288 M / 9.6 k = 128 → 21.1 dB</div></div></div>
            <div class="wstep"><div class="wn">3</div><div class="wtext">解扩后：<div class="calc">−40 + 21.1 = −18.9 dB，比要求的 7 dB 差了约 26 dB</div></div></div>
            <div class="wstep"><div class="wn">4</div><div class="wtext">加上功率控制，让近处手机把功率降 40 dB，两个信号到达基站时一样强：<div class="calc">解扩前 0 dB → 解扩后 21.1 dB ≥ 7 dB ✓</div></div></div>
            <div class="wans">仅仅一个近处用户，就能让远处用户的 SIR 比要求低 26 dB；有了功率控制，两个人都能正常通话</div>
          </div>
        </div>
        <div class="worked">
          <summary><span class="wtag">例题</span>有了理想功率控制，一个 CDMA 小区能容纳多少用户</summary>
          <div class="wbody">
            <p>假设：沿用上题参数。理想功率控制下，K 个用户到达基站的功率都一样；只考虑本小区干扰，忽略热噪声、话音激活和邻区干扰。</p>
            <div class="wstep"><div class="wn">1</div><div class="wtext">对任一用户，其余 K − 1 个用户都是干扰，功率都一样：<div class="calc">解扩前 SIR = 1 / (K − 1)，解扩后 SIR = 128 / (K − 1)</div></div></div>
            <div class="wstep"><div class="wn">2</div><div class="wtext">要求解扩后 ≥ 7 dB，即 ≥ 5.01：<div class="calc">128 / (K − 1) ≥ 5.01 → K − 1 ≤ 25.5 → K ≤ 26</div></div></div>
            <div class="wans">理想功率控制下约 26 个用户共用同一频段；没有功率控制时，一个离得近的用户就能让别人全部无法通信</div>
          </div>
        </div>
        <p><b>那 GSM 为什么不需要这么严格？</b>GSM 同一小区里的用户用不同的频率或时隙，基站不会同时在同一频率上收两个本小区用户的信号，近处用户不会直接淹没远处用户。GSM 做功率控制主要是为了省电，以及减少对其他同频小区的干扰（p.157 的 CCI）。</p>
      </div>

      <h3><span class="zh-num">10.6</span>本章数字速记（只列课件内容）</h3>
      <div class="tblwrap"><table><thead><tr><th>内容</th><th>要点</th><th>出处</th></tr></thead><tbody>
        <tr><td>P_min</td><td>−90 到 −100 dBm</td><td>p.153</td></tr>
        <tr><td>Δ 太大 / 太小</td><td>不必要的切换 / 来不及切换而掉话</td><td>p.153</td></tr>
        <tr><td>掉话原因</td><td>新小区无信道；MSC 太慢或 Δ 太小；目标链路失败</td><td>p.153</td></tr>
        <tr><td>硬切换</td><td>break before make；GSM、IS-136</td><td>p.154</td></tr>
        <tr><td>软切换</td><td>make before break；分集；IS-95、WCDMA、cdma2000</td><td>p.155</td></tr>
        <tr><td>减少切换掉话</td><td>切换优先：排队、预留 r 条信道</td><td>p.156</td></tr>
        <tr><td>功率控制</td><td>SIR 高就降、低就升；省电、减少 CCI</td><td>p.157–158</td></tr>
        <tr><td>CDMA 功率控制</td><td>每 1 ms 一次</td><td>p.28</td></tr>
      </tbody></table></div>
    </section>
'''
s = replace_section(s, 'ch10', CH10)

# roadmap line in ch2 now that 7 has worst case
P.write_text(s, encoding='utf-8')
print('ok', len(s))
