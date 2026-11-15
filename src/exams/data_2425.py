# EE6129 Semester 2 Examination 2024-2025 (April/May 2025)

P = 'y2425s2'

def S(n, html):
    return f'<div class="wstep"><div class="wn">{n}</div><div class="wtext">{html}</div></div>'

FIG1 = '''<div class="figwrap"><svg viewBox="0 0 420 220" role="img" aria-label="原卷 Figure 1：纵轴 Path Loss，横轴 log10(d)；直线从 d = 1 m 处的 A 点向右下降，与横轴交于 B；A 到横轴的高度标注 88 dB">
<line x1="70" y1="30" x2="70" y2="185" style="stroke:var(--ink)" stroke-width="1.5"/>
<line x1="60" y1="150" x2="390" y2="150" style="stroke:var(--ink)" stroke-width="1.5"/>
<line x1="62" y1="38" x2="320" y2="160" style="stroke:var(--ink)" stroke-width="3"/>
<line x1="56" y1="42" x2="84" y2="42" style="stroke:var(--ink)"/>
<line x1="78" y1="46" x2="78" y2="146" style="stroke:var(--accent)" stroke-width="1.4"/>
<text x="84" y="100" font-size="13" style="fill:var(--accent-ink)">88 dB</text>
<text x="40" y="47" font-size="15" font-weight="700" style="fill:var(--ink)">A</text>
<text x="290" y="178" font-size="15" font-weight="700" style="fill:var(--ink)">B</text>
<line x1="298" y1="142" x2="298" y2="158" style="stroke:var(--ink)"/>
<text x="46" y="200" font-size="12" style="fill:var(--ink)">d = 1 m</text>
<text x="74" y="24" font-size="12" style="fill:var(--ink)">Path Loss</text>
<text x="350" y="140" font-size="12" style="fill:var(--ink)">log₁₀(d)</text>
</svg><div class="cap">按原卷 Figure 1 重画（不按比例）。</div></div>'''

FIG2 = '''<div class="figwrap"><svg viewBox="0 0 420 170" role="img" aria-label="原卷 Figure 2：三抽头横向滤波器，r_i 经过两个 Z^-1 延迟，三个抽头分别乘 c0、c1、c2 后相加得到 y_i">
<g style="stroke:var(--ink);fill:none" stroke-width="1.4">
<line x1="40" y1="40" x2="120" y2="40"/><rect x="120" y="25" width="44" height="30"/><line x1="164" y1="40" x2="220" y2="40"/><rect x="220" y="25" width="44" height="30"/><line x1="264" y1="40" x2="300" y2="40"/>
<line x1="90" y1="40" x2="90" y2="85"/><line x1="190" y1="40" x2="190" y2="85"/><line x1="300" y1="40" x2="300" y2="85"/>
<circle cx="90" cy="92" r="7"/><circle cx="190" cy="92" r="7"/><circle cx="300" cy="92" r="7"/>
<line x1="90" y1="99" x2="90" y2="120"/><line x1="190" y1="99" x2="190" y2="120"/><line x1="300" y1="99" x2="300" y2="120"/>
<rect x="70" y="120" width="250" height="30"/><line x1="320" y1="135" x2="360" y2="135"/>
</g>
<g font-size="12" style="fill:var(--ink)"><text x="20" y="44">r<tspan font-size="9" dy="3">i</tspan></text><text x="128" y="45">Z⁻¹</text><text x="228" y="45">Z⁻¹</text>
<text x="100" y="86">c₀</text><text x="200" y="86">c₁</text><text x="310" y="86">c₂</text><text x="186" y="141" font-size="15">Σ</text><text x="366" y="139">y<tspan font-size="9" dy="3">i</tspan></text></g>
<g style="stroke:var(--ink)"><line x1="85" y1="87" x2="95" y2="97"/><line x1="95" y1="87" x2="85" y2="97"/><line x1="185" y1="87" x2="195" y2="97"/><line x1="195" y1="87" x2="185" y2="97"/><line x1="295" y1="87" x2="305" y2="97"/><line x1="305" y1="87" x2="295" y2="97"/></g>
</svg><div class="cap">按原卷 Figure 2 重画：三抽头横向（FIR）均衡器。</div></div>'''

QS = [
dict(id='y2425s2-q1a', paper=P, q='Q1(a)', marks=13, page='p2', ch='ch2', quiz=True,
 topic='路径损耗图读数 · LCR/AFD 求误符号数 · 注水功率分配',
 en='''<p>1. (a) Mobile radio channels introduce path loss and fading to the transmitted radio signals.</p>
<p>(i) Consider the simplified path loss model, P<sub>r</sub> = P<sub>t</sub>K(d)<sup>−3.5</sup>, where P<sub>r</sub>, P<sub>t</sub>, K, and d, are the received signal power, transmitted signal power, a constant, and distance between the transmitter and receiver, respectively. Using the dB form of the model, a plot of the path loss (in dB) versus log<sub>10</sub>(d) is shown in Figure 1 on page 2. Determine the values of <b>A</b> and <b>B</b> if K<sub>dB</sub> = −30 dB, where K<sub>dB</sub> is the value of K in dB.</p>''' + FIG1 + '''
<p>(ii) A fading channel has an average fade duration of of 6 × 10<sup>−6</sup> second and a level crossing rate of 5. If the average fade duration covers exactly three (3) consecutive symbols, determine the symbol duration. If an error is assumed to have occurred in a symbol when more than half of the symbol lies within a deep fade, determine the average number of symbol errors per second.</p>
<p>(iii) The spectrum of a frequency selective channel is organized into three sub-bands. The signal-to-noise ratios (SNR's) of the sub-bands are 18dB, 10dB, and 3dB, respectively. The transmitted powers of the sub-bands are allocated using the formula below,
<span class="eq">P<sub>i</sub> = P(1/γ<sub>0</sub> − 1/γ<sub>i</sub>) when γ<sub>i</sub> ≥ γ<sub>0</sub>;　P<sub>i</sub> = 0 when γ<sub>i</sub> &lt; γ<sub>0</sub></span>
where P = 1W is the total power, γ<sub>i</sub> and P<sub>i</sub> are the signal-to-noise ratio and allocated signal power for the i<sup>th</sup> sub-band, and γ<sub>0</sub> is a suitable threshold value. Determine the allocated powers for the three sub-bands.</p>
<p class="marks">(13 Marks)</p>''',
 sol=S(1, '<b>(i) 写成 dB 形式，求 A</b>：P<sub>r</sub> = P<sub>t</sub>K d<sup>−3.5</sup> 两边取 10 log₁₀（讲义 Ch2 p.8，参考距离 d₀ = 1 m）：<div class="calc">10 log₁₀(P<sub>r</sub>/P<sub>t</sub>) = K<sub>dB</sub> − 35 log₁₀ d</div>这是关于 log₁₀ d 的一条直线，斜率 −35 dB/十倍距离（per decade）。图中的线从 A 往右<b>下降</b>，说明纵轴画的是 10 log₁₀(P<sub>r</sub>/P<sub>t</sub>)（损耗越大越往下）。A 在 d = 1 m，log₁₀ 1 = 0：<div class="calc">A = K<sub>dB</sub> − 35 × 0 = −30 dB</div>即 1 m 处信号已经衰减 30 dB。')
  + S(2, '<b>(i) 求 B</b>：从 A 竖直落到横轴是 88 dB。直线每走 1 个单位的 log₁₀ d 就下降 35 dB，所以横向要走：<div class="calc">35 × B = 88 → B = 88/35 = 2.51<br>d = 10<sup>2.514</sup> ≈ 327 m</div>自检：B 点纵坐标 = −30 − 35 × 2.514 = −118 dB，正好比 A 低 88 dB ✓。')
  + S(3, '<b>(ii) 符号时长</b>：平均衰落时长（average fade duration, AFD）τ̄ = 6 × 10⁻⁶ s，正好盖住 3 个符号：<div class="calc">T<sub>s</sub> = τ̄/3 = 6 µs / 3 = 2 µs<br>R<sub>s</sub> = 1/T<sub>s</sub> = 5 × 10⁵ symbol/s</div>')
  + S(4, '<b>(ii) 每次衰落错几个符号</b>：一次衰落长 3T<sub>s</sub>。如果衰落起点和符号边界对齐，3 个符号整个落在衰落里，全错；如果不对齐，就是 2 个完整符号加头尾两个"碎片"，两个碎片长度之和正好是 1 个 T<sub>s</sub>，必有一个超过一半（恰好各一半是边界情况）。两种情况都是<b>每次衰落 3 个错符号</b>。')
  + S(5, '<b>(ii) 每秒误符号数</b>：电平通过率（level crossing rate, LCR）L<sub>Z</sub> = 5 次/秒，即每秒平均 5 次衰落。用讲义 Ch2 p.46–47 例题的公式 (τ̄R<sub>s</sub>) × L<sub>Z</sub>：<div class="calc">误符号数 = 3 × 5 = 15 个/秒</div>自检：信号处在衰落中的时间比例 = L<sub>Z</sub>τ̄ = 5 × 6 × 10⁻⁶ = 3 × 10⁻⁵；误符号率 = 15/(5 × 10⁵) = 3 × 10⁻⁵，两者一致 ✓。')
  + S(6, '<b>(iii) dB 化线性</b>：γ = 10<sup>dB/10</sup>，顺便算出倒数：<div class="calc">γ₁ = 10<sup>1.8</sup> = 63.10，1/γ₁ = 0.0158<br>γ₂ = 10<sup>1.0</sup> = 10，　1/γ₂ = 0.1000<br>γ₃ = 10<sup>0.3</sup> = 1.995，1/γ₃ = 0.5012</div>')
  + S(7, '<b>(iii) 求门限 γ₀</b>：这是注水法（water-filling，讲义 Ch2 p.54）。先假设三个子带都分到功率，用总功率约束 ΣP<sub>i</sub> = P = 1：<div class="calc">Σ(1/γ₀ − 1/γ<sub>i</sub>) = 1<br>3/γ₀ = 1 + 0.0158 + 0.1 + 0.5012 = 1.6170<br>1/γ₀ = 0.5390 → γ₀ = 1.855（2.7 dB）</div>检查假设：最差的 γ₃ = 1.995 ≥ γ₀ = 1.855 ✓，三个子带都该开，不用去掉子带重算（讲义 p.56 例题就是因为 γ₃ &lt; γ₀，要去掉第 3 个信道再算一遍）。')
  + S(8, '<b>(iii) 分配功率 + 自检</b>：P<sub>i</sub> = P(1/γ₀ − 1/γ<sub>i</sub>)，P = 1 W：<div class="calc">P₁ = 0.5390 − 0.0158 = 0.523 W<br>P₂ = 0.5390 − 0.1000 = 0.439 W<br>P₃ = 0.5390 − 0.5012 = 0.038 W</div>自检：0.523 + 0.439 + 0.038 = 1.000 W ✓。SNR 越好的子带分到的功率越多；最差的 3 dB 子带只比门限高一点，分到的很少。')
  + '<div class="wans">(i) A = −30 dB，B ≈ 2.51　(ii) T<sub>s</sub> = 2 µs，15 个误符号/秒　(iii) P ≈ 0.523 / 0.439 / 0.038 W</div>',
 note='如果把纵轴理解为正的路径损耗 −K<sub>dB</sub> + 35 log d，则 A = 30 dB；但那条线应该上升。按图中下降的线，A = K<sub>dB</sub> = −30 dB。B 两种理解都一样。'),

dict(id='y2425s2-q1b1', paper=P, q='Q1(b)(i)', marks='(b) 共 12', page='p2', ch='ch4',
 topic='BPSK 选择分集：由 P<sub>out</sub> 反求支路数 M',
 en='''<p>(b) One common technique used to mitigate fading effects is Diversity.</p>
<p>(i) The Selection Diversity scheme of a BPSK system uses M branches. The BPSK system's outage probability at a probability of error of P<sub>b</sub> = Q(√(2 × γ<sub>b</sub>)) = 1.35 × 10<sup>−3</sup> can be expressed as,
<span class="eq">P<sub>out</sub> = (1 − e<sup>−γ<sub>b</sub>/30</sup>)<sup>M</sup></span>
If P<sub>out</sub> equals 0.02 approximately, determine the number of branches used by the BPSK system.</p>''',
 sol=S(1, '<b>查 Q 表求门限 γ<sub>b</sub></b>：P<sub>b</sub> = Q(√(2γ<sub>b</sub>)) = 1.35 × 10⁻³。Q 表中 Q(3.00) = 0.00135，所以：<div class="calc">√(2γ<sub>b</sub>) = 3.0 → 2γ<sub>b</sub> = 9 → γ<sub>b</sub> = 4.5（6.5 dB）</div>γ<sub>b</sub> 是满足误码率要求的最低 SNR，也就是中断门限 γ₀。')
  + S(2, '<b>认出公式</b>：选择分集（selection diversity）、Rayleigh 衰落、各支路平均 SNR 相同时（讲义 Ch4 p.11）：<div class="calc">P<sub>out</sub> = (1 − e<sup>−γ₀/γ̄</sup>)<sup>M</sup></div>对照题目，分母 30 就是每支路的平均 SNR γ̄ = 30（14.8 dB）。中断（outage）= M 条支路<b>全部</b>低于门限；每条的概率是 1 − e<sup>−γ₀/γ̄</sup>，支路独立，所以相乘得 M 次方。')
  + S(3, '<b>算单支路中断概率</b>：<div class="calc">γ<sub>b</sub>/γ̄ = 4.5/30 = 0.15<br>e<sup>−0.15</sup> = 0.8607<br>1 − 0.8607 = 0.1393</div>')
  + S(4, '<b>解 M</b>：两边取自然对数：<div class="calc">0.1393<sup>M</sup> = 0.02<br>M = ln 0.02 / ln 0.1393<br>　= (−3.912)/(−1.971) ≈ 1.98</div>支路数必须是整数，取最接近的 <b>M = 2</b>。')
  + S(5, '<b>自检</b>：把 M = 1、2、3 代回去：<div class="calc">M = 1：0.139<br>M = 2：0.1393² = 0.0194 ≈ 0.02 ✓<br>M = 3：0.1393³ = 0.0027</div>只有 M = 2 "约等于 0.02"。这和讲义 Ch4 p.13 例题几乎一样（γ̄ = 15 dB、P<sub>b</sub> = 10⁻³ 时，M = 2 的 P<sub>out</sub> = 0.020）。')
  + '<div class="wans">M = 2 个支路</div>'),

dict(id='y2425s2-q1b2', paper=P, q='Q1(b)(ii)(iii)', marks='(b) 共 12', page='p2', ch='ch5',
 topic='最大分集增益 N×M · 分集-复用折中求速率 · 无信息发射机的 MIMO 容量',
 en='''<p>(ii) For a MIMO system that uses 5 transmit antennas and 3 receive antennas, what is the maximum diversity gain of the system? If the system operates with a diversity gain of 3 and a multiplexing gain of 2, determine the maximum transmission rate per Hz of the system at a probability of error of 10<sup>−3</sup>.</p>
<p>(iii) The channel capacity of a MIMO system with N transmitter antennas and M receiver antennas can be expressed as,
<span class="eq">C<sub>MIMO</sub> = B × log<sub>2</sub> det{I + (1/σ<sup>2</sup>) HPH<sup>H</sup>}</span>
where B is the receiver bandwidth, I is the Identity matrix, σ<sup>2</sup> is the noise power, H and P are the channel matrix and transmit power matrix respectively, H<sup>H</sup> is the conjugate transpose of H, and det{X} is the determinant of the matrix X. Simplify the channel capacity expression if the MIMO system has an uninformed transmitter with a total transmit power of P. Hence determine the channel capacity per Hz of this system if N = M = 1, P = 1, σ<sup>2</sup> = 0.25, and the channel gain is 2.</p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(ii) 最大分集增益</b>：N = 5 根发射、M = 3 根接收天线，每一对收发天线都是一条独立衰落的路径（讲义 Ch4 p.31–32）：<div class="calc">d<sub>max</sub> = N × M = 5 × 3 = 15</div>')
  + S(2, '<b>(ii) 由误码率和分集增益求 SNR</b>：高 SNR 时 P<sub>e</sub> ≈ SNR<sup>−d</sup>（讲义 Ch4 p.33）。代入 P<sub>e</sub> = 10⁻³、d = 3：<div class="calc">10⁻³ = SNR⁻³ → SNR = (10⁻³)<sup>−1/3</sup> = 10（10 dB）</div>')
  + S(3, '<b>(ii) 由复用增益求速率</b>：复用增益（multiplexing gain）的定义是 r = R / log₂ SNR（讲义 Ch4 p.32），所以 R = r log₂ SNR：<div class="calc">log₂ 10 = log₁₀ 10 / 0.301 = 3.32<br>R = 2 × 3.32 ≈ 6.64 bit/s/Hz</div>')
  + S(4, '<b>(ii) 检查 (r, d) 能否做到</b>：最优折中曲线连接点 (r, (N − r)(M − r))，r = 0 … min(N, M) = 3：<div class="calc">r = 0, 1, 2, 3 → d = 15, 8, 3, 0</div>r = 2 时 d(2) = (5 − 2)(3 − 2) = 3，正好等于题给的 d = 3 ✓。这个工作点在最优曲线上，所以 6.64 bit/s/Hz 就是最大速率。')
  + S(5, '<b>(iii) 无信息发射机的化简</b>：无信息发射机（uninformed transmitter）不知道 H，只能把总功率 P 平均分给 N 根天线（讲义 Ch5 p.37）：<div class="calc">P = (P/N) I，tr P = P</div>代入原式：<div class="calc">C = B log₂ det{I + (P/(Nσ²)) HH<sup>H</sup>}</div>')
  + S(6, '<b>(iii) 代入 N = M = 1</b>：所有矩阵都变成标量，det 就是这个数本身。"channel gain is 2" 按幅度增益 h = 2 理解（讲义 Ch5 p.33 的 SISO 例子也用 h 表示信道增益），HH<sup>H</sup> = |h|² = 4：<div class="calc">C/B = log₂(1 + P|h|²/σ²)<br>　= log₂(1 + 1 × 4/0.25)<br>　= log₂(1 + 16) = log₂ 17</div>这就是 Shannon 公式，SNR = 16（12 dB）。')
  + S(7, '<b>(iii) 换算 + 自检</b>：<div class="calc">log₂ 17 = log₁₀ 17 / 0.301<br>　= 1.2304/0.301 ≈ 4.09 bit/s/Hz</div>自检：2⁴ = 16 &lt; 17 &lt; 2⁵ = 32，结果应在 4 和 5 之间、略大于 4 ✓。')
  + '<div class="wans">(ii) d<sub>max</sub> = 15；R ≈ 6.64 bit/s/Hz　(iii) C/B = log₂17 ≈ 4.09 bit/s/Hz</div>',
 note='"channel gain is 2" 按幅度增益 h = 2 理解（|h|² = 4）。如果理解成功率增益 |h|² = 2，结果是 log₂ 9 ≈ 3.17。'),

dict(id='y2425s2-q2a', paper=P, q='Q2(a)', marks=13, page='p2', ch='ch6',
 topic='横向滤波器 · 迫零均衡抽头 · 残余 ISI 下的误码率',
 en='''<p>2. (a) The Z-transform of a channel is H(Z) = 1 + hZ<sup>−1</sup>, where h is the channel gain. The equalizer at the receiver is implemented as a transversal filter shown in Figure 2, where r<sub>i</sub> and y<sub>i</sub> are the received signal and equalizer output respectively, c<sub>0</sub>, c<sub>1</sub> and c<sub>2</sub> are the equalizer gain coefficients, and Z<sup>−1</sup> represents a delay of 1 symbol duration.</p>''' + FIG2 + '''
<p>(i) What should the value of h be for an AWGN channel without fading? What would you observe on the value of h for fast-fading channels? Explain your answers.</p>
<p>(ii) If the equalizer implements the zero-forcing technique, determine the values of c<sub>1</sub>, c<sub>2</sub>, and c<sub>3</sub> in Figure 2, if h = 0.2.</p>
<p>(iii) The equalizer is now implemented with another design such that the decision variable is y<sub>i</sub> = s<sub>i</sub> + 0.6s<sub>i−1</sub> + w′<sub>i</sub>, where s<sub>i</sub> is the transmitted symbol that is equally likely to be 1 or −1, and w′<sub>i</sub> is an additive white Gaussian noise with zero mean and a variance of 0.64. The decision rule is such that, s<sub>i</sub> will be detected as 1 if y<sub>i</sub> ≥ 0, or −1 if y<sub>i</sub> &lt; 0. Determine the probability of error for this equalizer.</p>
<p class="marks">(13 Marks)</p>''',
 sol=S(1, '<b>(i) AWGN 无衰落时的 h</b>：H(Z) = 1 + hZ⁻¹ 里，1 是直达路径，hZ⁻¹ 是晚一个符号到达的多径回波。纯 AWGN 信道只有一条直达路径加噪声，没有回波，所以 <b>h = 0</b>，H(Z) = 1，没有 ISI，均衡器只要 c₀ = 1、其余为 0。')
  + S(2, '<b>(i) 快衰落时的 h</b>：快衰落（fast fading）的相干时间（coherence time）和符号时长相当甚至更短，h 是随时间变化的复随机量，幅度和相位在几个符号内就明显改变。所以 <b>h 不是常数，而是快速时变</b>：均衡器系数必须不断重新估计、自适应跟踪（更频繁地发训练序列），否则很快失配。')
  + S(3, '<b>(ii) 迫零原理</b>：迫零均衡（zero-forcing）要让级联响应 H(Z)C(Z) = 1，也就是完全没有 ISI（讲义 Ch6 p.23）：<div class="calc">C(Z) = 1/H(Z) = 1/(1 + 0.2Z⁻¹)</div>')
  + S(4, '<b>(ii) 长除法展开</b>（同讲义 Ch6 p.24 例题的做法），1 ÷ (1 + 0.2Z⁻¹)：<div class="calc">商 1：减去 1 + 0.2Z⁻¹，余 −0.2Z⁻¹<br>商 −0.2Z⁻¹：减去 −0.2Z⁻¹ − 0.04Z⁻²，余 0.04Z⁻²<br>商 0.04Z⁻²：减去 0.04Z⁻² + 0.008Z⁻³，余 −0.008Z⁻³</div><div class="calc">C(Z) = 1 − 0.2Z⁻¹ + 0.04Z⁻² − 0.008Z⁻³ + …</div>规律：第 k 项的系数是 (−0.2)<sup>k</sup>。')
  + S(5, '<b>(ii) 取 3 个抽头 + 自检</b>：Figure 2 只有 3 个抽头，取前三项。题目文字写 "c₁, c₂, c₃"，对应图里的 c₀、c₁、c₂：<div class="calc">c₀ = 1，c₁ = −0.2，c₂ = 0.04</div>自检：(1 + 0.2Z⁻¹)(1 − 0.2Z⁻¹ + 0.04Z⁻²) = 1 + 0·Z⁻¹ + 0·Z⁻² + 0.008Z⁻³，只剩截断造成的 0.008 残余 ISI ✓。')
  + S(6, '<b>(iii) 按前一个符号分两种情况</b>：σ² = 0.64 → σ = 0.8。先看发 s<sub>i</sub> = +1，出错条件是 y<sub>i</sub> &lt; 0。前一个符号 s<sub>i−1</sub> = ±1 各占一半：<div class="calc">s<sub>i−1</sub> = +1：y = 1.6 + w′ → P = Q(1.6/0.8) = Q(2.0)<br>s<sub>i−1</sub> = −1：y = 0.4 + w′ → P = Q(0.4/0.8) = Q(0.5)</div>这就是讲义 Ch6 p.28 的做法：先在给定 ISI 下求条件误码率 Q((q₀ + ISI)/σ)（这里 q₀ = 1，ISI = ±0.6），再对 ISI 取平均。')
  + S(7, '<b>(iii) 查 Q 表、取平均</b>：Q(2.0) = 0.0228，Q(0.5) = 0.3085：<div class="calc">P<sub>e</sub> = ½(0.0228 + 0.3085) = ½ × 0.3313 ≈ 0.166</div>发 −1 时 y = −1 ± 0.6 + w′，出错条件 y ≥ 0，到判决门限的距离还是 1.6 和 0.4，由对称性结果相同，所以总 P<sub>e</sub> ≈ 0.166。')
  + S(8, '<b>(iii) 对比 + 评价</b>：如果没有 ISI，P<sub>e</sub> = Q(1/0.8) = Q(1.25) = 0.106。0.6 的残余 ISI 把误码率提高到 0.166，主要来自眼图只张开 0.4 的那一半情况（Q(0.5) = 0.31）。残余 ISI 太大，说明这个设计不好。')
  + '<div class="wans">(i) h = 0；快衰落时 h 快速时变　(ii) 1，−0.2，0.04　(iii) P<sub>e</sub> ≈ 0.166</div>',
 note='原题 (ii) 写的是 "c₁, c₂, and c₃"，但 Figure 2 标的是 c₀、c₁、c₂，按图作答。'),

dict(id='y2425s2-q2b', paper=P, q='Q2(b)', marks=12, page='p2', ch='ch7',
 topic='OFDM 速率划分 · 加循环前缀的表达式 · 等容量功率分配',
 en='''<p>(b) A 4-level communication system has a transmitted symbol rate of 5 million symbols per second. The system experiences severe fading effects and will be modified to use the OFDM technique with N = 4, where N is the number of sub-carriers of the OFDM system.</p>
<p>(i) Determine the transmission bit rates for the system and for each of the OFDM sub-carriers.</p>
<p>(ii) The transmitted signal of an OFDM signal can be expressed as,
<span class="eq">x(t) = (1/√T) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub>(t)e<sup>j2π(k/T)t</sup>,　nT ≤ t ≤ (n + 1)T</span>
where s<sub>k</sub>(t) is the signals in the k<sup>th</sup> OFDM sub-carrier and T is the OFDM symbol duration. Modify this expression to incorporate the inclusion of a cyclic prefix of T<sub>g</sub>.</p>
<p>(iii) The channel capacity per Hz for the k<sup>th</sup> sub-carrier of an OFDM system has been derived to be,
<span class="eq">C<sub>k</sub> = ¼ log<sub>2</sub>(1 + P<sub>k</sub>|H<sub>k</sub>|<sup>2</sup>), k = 1, 2, 3, 4</span>
where P<sub>k</sub> is the power allocated to the k<sup>th</sup> OFDM sub-carrier and H<sub>k</sub> is the channel gain experienced by the k<sup>th</sup> OFDM sub-carrier signal. Powers are allocated to the sub-carriers to have the same channel capacity per Hz of C<sub>k</sub> = 0.9 bit per second per Hz. Determine the total power needed for this system if the channel gains have the following values.
<span class="eq">|H<sub>1</sub>| = 1, |H<sub>2</sub>| = 0.2, |H<sub>3</sub>| = 1, |H<sub>4</sub>| = 1.4</span></p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(i) 系统速率</b>：4 电平（4-level）→ 每个符号 log₂ 4 = 2 bit：<div class="calc">R<sub>b</sub> = R<sub>s</sub> × 2 = 5 × 10⁶ × 2 = 10 Mbit/s</div>改用 OFDM 不改变总速率，只是把这条高速流拆成 N 路低速流并行传。')
  + S(2, '<b>(i) 每个子载波的速率</b>：讲义 Ch7 p.8，每个子载波的符号率 R = 1/T = 1/(NT<sub>s</sub>) = R<sub>s</sub>/N：<div class="calc">R = 5 M/4 = 1.25 Msymbol/s<br>每子载波 = 1.25 M × 2 = 2.5 Mbit/s</div>自检：4 × 2.5 = 10 Mbit/s ✓。OFDM 符号时长 T = 4T<sub>s</sub> = 4 × 0.2 µs = 0.8 µs，符号变长 4 倍，这正是 OFDM 抗多径的原因。')
  + S(3, '<b>(ii) 加循环前缀</b>：讲义 Ch7 p.17、p.21 的写法：表达式不变，只把每个块的时间范围往前延伸 T<sub>g</sub>：<div class="calc">x(t) = (1/√T) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub>(t) e<sup>j2πkt/T</sup>，<br>nT − T<sub>g</sub> ≤ t &lt; (n+1)T</div>')
  + S(4, '<b>(ii) 为什么叫"循环"</b>：e<sup>j2πkt/T</sup> 以 T 为周期，所以前面多出的 T<sub>g</sub> 段正好是块尾 T<sub>g</sub> 段的复制，这就是循环前缀（cyclic prefix）。只要 T<sub>g</sub> 不小于最大时延扩展，上一块的回波只落在前缀里；接收端丢掉这一段，只取 nT ≤ t &lt; (n+1)T。（若按块周期 T + T<sub>g</sub> 计时，也可写成区间 n(T+T<sub>g</sub>) ≤ t &lt; (n+1)(T+T<sub>g</sub>)、指数里用 t − n(T+T<sub>g</sub>) − T<sub>g</sub>。）')
  + S(5, '<b>(iii) 每个子载波的条件</b>：要求每个 C<sub>k</sub> = 0.9：<div class="calc">¼ log₂(1 + P<sub>k</sub>|H<sub>k</sub>|²) = 0.9<br>log₂(1 + P<sub>k</sub>|H<sub>k</sub>|²) = 3.6<br>1 + P<sub>k</sub>|H<sub>k</sub>|² = 2<sup>3.6</sup></div>')
  + S(6, '<b>(iii) 算 2<sup>3.6</sup></b>：<div class="calc">2<sup>3.6</sup> = 2³ × 2<sup>0.6</sup> = 8 × 1.5157 = 12.126<br>P<sub>k</sub>|H<sub>k</sub>|² = 12.126 − 1 = 11.126（≈ 11.13）</div>四个子载波的接收 SNR 都要等于 11.126，所以 P<sub>k</sub> = 11.126/|H<sub>k</sub>|²：信道越差，要的功率越多。')
  + S(7, '<b>(iii) 逐个求 P<sub>k</sub></b>：|H<sub>k</sub>|² = 1、0.04、1、1.96：<div class="calc">P₁ = 11.126/1 = 11.13<br>P₂ = 11.126/0.04 = 278.1<br>P₃ = 11.126/1 = 11.13<br>P₄ = 11.126/1.96 = 5.68</div>（P₂ 用没四舍五入的 11.126 算；如果先写成 11.13 再除，得 278.25，只是舍入差别，两个都算对。）')
  + S(8, '<b>(iii) 求和 + 自检</b>：<div class="calc">P<sub>total</sub> = 11.126 + 278.14 + 11.126 + 5.676<br>　≈ 306.1（功率单位）</div>自检：P₄ 代回，¼ log₂(1 + 5.68 × 1.96) = ¼ log₂ 12.13 = ¼ × 3.6 = 0.9 ✓。差的子载波（|H₂| = 0.2）一个就吃掉 278.1/306.1 ≈ 91% 的功率。这正好说明为什么要用注水法，而不是强求每个子载波容量相同。')
  + '<div class="wans">(i) 10 Mbit/s；每子载波 2.5 Mbit/s　(iii) 总功率 ≈ 306</div>'),

dict(id='y2425s2-q3', paper=P, q='Q3', marks=25, page='A', ch='ch9',
 topic='FDD-TDMA 信道数 · 由 SIR 选簇 · Erlang B · 小区分裂 · 三扇区重新选簇',
 en='''<p>3. A particular city deploys a frequency division duplexing-time division multiple access (FDD-TDMA) cellular network. The cellular network has a total of 60 cells with a cell radius of 1,000 meters. An omni-directional antenna is used in the system. A total of 40 MHz bandwidth is allocated to the system. Each link (uplink or downlink) uses 2 MHz of bandwidth for control and signalling transmission. The carrier frequency is 200 KHz and each frame has 8 timeslots. The minimum acceptable signal-to-interference ratio (SIR) is 18 dB for the downlink. There is a potential subscriber density of 2,000 subscribers/km<sup>2</sup> in the system and the traffic loads are uniformly distributed over the city and covered by the cellular network. On average, each user generates about 0.03 Erlangs of traffic. The path-loss exponent is assumed to be 3.7.</p>
<p>Assume that the co-channel cells in the first tier create significant interference and all the interfering base stations are equidistant from the desired mobile unit which is located at the edge of the cell. You may use any suitable assumptions and approximation to answer the following questions.</p>
<p>Note: A hexagonal-shaped cell is assumed in the analysis and the area of the hexagonal cell with the cell radius R is given by A<sub>ce</sub> = (3√3/2)R<sup>2</sup>.</p>
<p>(a) Determine the number of duplex channels per cell. <span class="marks">(6 Marks)</span></p>
<p>(b) Can the system support 1% call blocking probability? <span class="marks">(6 Marks)</span></p>
<p>(c) Show that the cell splitting technique can be used to get 1% call blocking probability. Determine the new cell radius. <span class="marks">(4 Marks)</span></p>
<p>(d) If a 3-sector directional antenna is used, how many cells are required in order to have a 1% call blocking probability? Assume that a single carrier can be shared between two sectors. <span class="marks">(9 Marks)</span></p>''',
 sol=S(1, '<b>(a) 带宽 → 信道数</b>：FDD 上下行各用一半：40/2 = 20 MHz 每方向；每个方向扣掉 2 MHz 控制信令，剩 18 MHz 给业务。"carrier frequency is 200 KHz" 应理解为每个载波<b>带宽</b> 200 kHz（GSM 式 FDD-TDMA）：<div class="calc">载波数 = 18 MHz / 200 kHz = 90<br>双工信道 = 90 × 8 时隙 = 720</div>每个时隙在上行、下行各占一个，配成一条双工信道（duplex channel）。这 720 条是一个簇（cluster）共用的总数。')
  + S(2, '<b>(a) 由 SIR 求簇大小下限</b>：手机在小区边缘、第一层 6 个同频基站等距 D（讲义 Part A p.88）：<div class="calc">S/I = R<sup>−n</sup>/(6D<sup>−n</sup>) = Q<sup>n</sup>/6<br>Q = D/R = √(3N)</div>要求 S/I ≥ 18 dB = 10<sup>1.8</sup> = 63.1，n = 3.7：<div class="calc">Q<sup>3.7</sup> ≥ 6 × 63.1 = 378.6<br>Q ≥ 378.6<sup>1/3.7</sup> = 4.975<br>N = Q²/3 ≥ 4.975²/3 = 8.25</div>')
  + S(3, '<b>(a) 选合法的 N</b>：六边形簇大小只能是 N = i² + ij + j² = 1, 3, 4, 7, 9, 12, …，≥ 8.25 的最小值是 <b>N = 9</b>（i = 3, j = 0）。验算：<div class="calc">N = 7：Q = √21 = 4.583，Q<sup>3.7</sup>/6 = 46.6 → 16.7 dB ✗<br>N = 9：Q = √27 = 5.196，Q<sup>3.7</sup>/6 = 74.1 → 18.7 dB ✓</div><div class="calc">每小区信道 = 720/9 = 80 条双工信道</div>')
  + S(4, '<b>(b) 每小区的话务量</b>：<div class="calc">A<sub>ce</sub> = (3√3/2) × 1² = 2.598 km²<br>用户数 = 2.598 × 2000 = 5196<br>话务量 = 5196 × 0.03 = 155.9 E</div>')
  + S(5, '<b>(b) 查 Erlang B 表比较</b>：M = 80 条、阻塞率 1% 时，表中可承载的话务量 A ≈ <b>65.4 E</b>。需要 155.9 E，远大于 65.4 E，所以<b>不能</b>满足 1% 阻塞率。把 A = 155.9、M = 80 代回 Erlang B 公式，阻塞率约 49%，差得很远。')
  + S(6, '<b>(c) 为什么小区分裂可行</b>：小区分裂（cell splitting，讲义 Part A p.135–136）保持 N = 9 不变，D 和 R 同比例缩小，Q = D/R 不变，所以 SIR 不变，每小区仍是 80 条信道、仍能承载 65.4 E；但每个小区面积变小，覆盖的用户变少。只要小区够小，每小区的话务量就能降到 65.4 E 以下。')
  + S(7, '<b>(c) 新半径</b>：单位面积话务量 = 2000 × 0.03 = 60 E/km²：<div class="calc">小区面积 ≤ 65.4/60 = 1.09 km²<br>2.598R² ≤ 1.09 → R² ≤ 0.4196<br>R ≤ 0.648 km（约 650 m）</div>自检：R = 0.648 km 时面积 = 2.598 × 0.648² = 1.09 km²，话务量 = 1.09 × 60 = 65.4 E ✓。全城 155.9 km² 需要 155.9/1.09 ≈ 143.0 → 约 144 个小区（原来 60 个，约 2.4 倍）。')
  + S(8, '<b>(d) 三扇区后重新选簇</b>：120° 三扇区时，每个扇区第一层只剩 2 个同频干扰，最坏情况（讲义 Part A p.145）：<div class="calc">S/I = 1/(Q<sup>−n</sup> + (Q + 0.7)<sup>−n</sup>)</div>SIR 变好了，可以用更小的簇（讲义 p.143–146）：<div class="calc">N = 3：Q = 3<br>　3<sup>−3.7</sup> + 3.7<sup>−3.7</sup> = 0.01717 + 0.00790 = 0.02507<br>　S/I = 39.9 → 16.0 dB ✗<br>N = 4：Q = √12 = 3.464<br>　3.464<sup>−3.7</sup> + 4.164<sup>−3.7</sup> = 0.01008 + 0.00510 = 0.01518<br>　S/I = 65.9 → 18.2 dB ✓</div>取 <b>N = 4</b>。')
  + S(9, '<b>(d) 每扇区信道数</b>：<div class="calc">每小区 720/4 = 180 条（90/4 = 22.5 个载波）<br>每扇区 22.5/3 = 7.5 个载波 = 7.5 × 8 = 60 条</div>半个载波怎么分？题目说"一个载波可被两个扇区共用"（8 个时隙两边各用 4 个），正好让每扇区分到 7.5 个载波 = 60 条。如果不能共用，每扇区只能有 7 个载波 = 56 条。')
  + S(10, '<b>(d) 所需小区数</b>：Erlang B（M = 60，1%）→ A ≈ 46.95 E/扇区，每小区 3 × 46.95 = 140.8 E。全城的面积和总话务量：<div class="calc">面积 = 60 × 2.598 = 155.9 km²<br>总话务量 = 155.9 × 60 = 9353 E<br>小区数 = 9353/140.8 = 66.4 → 67 个</div>自检：67 个小区，每个面积 155.9/67 = 2.327 km²（R ≈ 0.95 km），话务量 2.327 × 60 = 139.6 E ≤ 140.8 E ✓。')
  + S(11, '<b>(d) 对比</b>：如果只加扇区、不改簇（仍 N = 9，每扇区约 26–27 条），每小区只能承载约 52.6 E，需要约 178 个小区，比 (c) 的全向小区分裂（约 144 个）还多：扇区把信道池切小，中继效率下降（讲义 Part A p.148–149）。所以扇区化必须配合缩小簇才划算。')
  + '<div class="wans">(a) N = 9，80 条/小区　(b) 需 155.9 E，只能承载 65.4 E，不能　(c) R ≈ 0.65 km　(d) N = 4，每扇区 60 条，约 67 个小区</div>',
 note='(d) 的题意有不同理解，这里采用"扇区化 → 允许更小的簇 → 每小区信道更多"的思路，并说明了只加扇区不改簇的结果。'),

dict(id='y2425s2-q4a', paper=P, q='Q4(a)', marks=8, page='A', ch='ch2', hw='HW1 Q1(a)',
 topic='蜂窝系统六大组成之数据库：HLR 与 VLR',
 en='''<p>4. (a) For every cellular network, a database unit is one of the six basic components. What are the basic functions of the database unit? Describe the differences between the home location register (HLR) and the visitor location register (VLR) in the database units.</p>
<p class="marks">(8 Marks)</p>''',
 sol=S(1, '<b>数据库在哪里</b>：讲义 Part A p.11 列出蜂窝网的六个基本组成：① 到有线网的网关、② 基站（BS）、③ 数据库（Databases）、④ 安全机制、⑤ 空中接口标准、⑥ 移动台（MS）。数据库挂在移动交换中心（MTSO/MSC）上，交换中心处理每个呼叫都要查它。')
  + S(2, '<b>数据库的基本功能</b>：<br>• <b>存用户签约信息</b>：号码、开通的业务、计费信息——交换中心据此决定这个用户能不能打、能用哪些业务。<br>• <b>位置管理</b>：记录用户当前在哪个位置区——用户在移动，来电时只有知道位置，才能在正确的基站寻呼（paging）。<br>• <b>鉴权和安全参数</b>：配合安全机制确认"是不是本人"，防止盗用。<br>• <b>支持漫游和切换</b>：用户到了别的网络或区域，靠数据库之间交换信息继续提供服务。')
  + S(3, '<b>HLR（归属位置寄存器，home location register）</b>：每个用户在其归属网络的 HLR 里有一条<b>永久记录</b>，存全部签约资料、鉴权参数，以及"当前在哪个 VLR/MSC 区域"的指针。一个运营商通常只有一个（逻辑上的）HLR，它是用户资料的唯一"正本"。')
  + S(4, '<b>VLR（拜访位置寄存器，visitor location register）</b>：和每个 MSC/MTSO 服务区关联，保存当前<b>在本区域内</b>的用户（包括外地来的漫游用户）的<b>临时副本</b>：用户进入时从 HLR 下载，离开后删除。本地的呼叫建立和寻呼查 VLR 就够，不必每次都去问远处的 HLR，减少信令和时延。')
  + S(5, '<b>区别一句话</b>：HLR 是"户口所在地"，永久、集中、存全部签约信息；VLR 是"暂住登记"，临时、分布在各个服务区、只存当前在场用户的副本。<br><b>两者怎么配合</b>：用户移动到新区域时，新 VLR 向 HLR 登记，HLR 更新位置并通知旧 VLR 删除记录；有人打给他时，网络先问 HLR 他在哪个 VLR，再由那个 VLR 所在的 MSC 去寻呼。')
  + '<div class="wans">数据库存用户与位置信息；HLR 永久归属记录，VLR 临时拜访记录</div>',
 note='讲义只在 p.11 的框图里列出 "Databases"，HLR/VLR 的细节属于课外补充（GSM 的标准结构），和 HW1 Q1(a) 的答法一致。'),

dict(id='y2425s2-q4b', paper=P, q='Q4(b)', marks=8, page='B', ch='ch7',
 topic='IoT 通信网络层的四个子层',
 en='''<p>(b) Internet of Things (IoT) networks are built around the concept of "things" or smart objects performing functions and delivering new connected services. For the core functional IoT stack, the communication network layer is structured with four sublayers. List down each of these sublayers and briefly describe the each of the features.</p>
<p class="marks">(8 Marks)</p>''',
 sol=S(1, '<b>先定位</b>：核心 IoT 功能栈（core IoT functional stack）分三层：Things 层（传感器/执行器）→ 通信网络层 → 应用与分析层（讲义 Part B p.89–90）。题目问的是中间的通信网络层，它的四个子层按数据从物体走向中心的顺序排列。')
  + S(2, '<b>接入网子层（Access network）</b>：IoT 网络的"最后一公里"，通常是无线技术，如 802.11ah、802.15.4g、LoRa；按覆盖范围分 PAN、HAN、NAN、FAN、LAN、MAN/WAN（讲义 p.89、p.93–97）。为什么要按距离、物体数量和成本来选：智能物体大多电池供电、数据量小，不同场景要的距离和功耗差别很大，没有一种技术通吃；拓扑可以是点对点，也可以是点对多点（星形、簇状星形、网状）。')
  + S(3, '<b>网关与回传子层（Gateways and backhaul）</b>：把一片区域内的多个智能物体汇聚到一个公共网关，网关再用更长距离的介质（如蜂窝、光纤）把数据转发到头端中心站（讲义 p.89、p.98）。为什么需要：接入技术距离短、速率低，不能直接连到远处的中心，网关负责两种介质之间的转换。物体可以静止或在小范围内移动，网关通常固定。')
  + S(4, '<b>网络传输子层（Network transport）</b>：用开放、标准化的网络层和传输层协议（IP、UDP/TCP）把各种设备和介质连起来；要求能扩展到成千上万个传感器，并保证安全（讲义 p.90、p.98–99）。为什么选 IP：它灵活，能跑在低功耗、低带宽、高丢包的网络上；TCP 由网络负责可靠传送，UDP 把控制交给应用，按需要选。')
  + S(5, '<b>IoT 网络管理子层（IoT network management）</b>：应用层协议，负责智能物体与头端应用之间的数据交换（讲义 p.90、p.99），例如基于 TCP 的 HTTP（传感器作为客户端去连应用），以及适合低内存、低功耗、低带宽、高丢包环境的轻量双向协议 WebSocket。为什么需要：光有 IP 连通还不够，两端还要约定数据怎么打包、怎么请求和回应。')
  + '<div class="wans">Access network / Gateways &amp; backhaul / Network transport / IoT network management</div>'),

dict(id='y2425s2-q4c', paper=P, q='Q4(c)', marks=9, page='A', ch='ch8', hw='HW1 Q1(b)',
 topic='Erlang B：承载话务量 · 中继效率 · 用户数 · 换簇大小',
 en='''<p>(c) For a cellular system, suppose you selected the cluster size of N<sub>c</sub> = 9, with a total number of available channels of 504. Assume that the average users place 2 calls of 15 minutes duration per hour for the given cellular system.</p>
<p>(i) Determine the carrier load per cell and the trunking efficiency for a 2% Grade of Service (GOS)?</p>
<p>(ii) Calculate the number of users that can be accommodated for this cell at that given GOS.</p>
<p>(iii) Compute the carried load and trunking efficiency if the cluster size is changed to N<sub>c</sub>=7. Comment on your results.</p>
<p class="marks">(9 Marks)</p>''',
 sol=S(1, '<b>(i) 每小区信道数</b>：<div class="calc">M = 504/9 = 56 条/小区</div>')
  + S(2, '<b>(i) 查 Erlang B 表</b>：M = 56、GOS（阻塞率）= 2% → 可承载的话务量 A ≈ <b>45.9 E</b>（和讲义 Part A p.44 AMPS 例题同一个数：56 条、2% → 45.9 E）。')
  + S(3, '<b>(i) 承载话务量</b>：题目的 "carrier load" 是 carried load（承载话务量）的笔误。严格定义 C = A(1 − P<sub>B</sub>)（讲义 Part A p.120）：<div class="calc">C = 45.9 × (1 − 0.02) = 45.9 × 0.98 = 45.0 E</div>阻塞率小时 C ≈ A，所以答 45.9 E 也可以。')
  + S(4, '<b>(i) 中继效率</b>：中继效率（trunking efficiency）= 每条信道平均承载的 Erlang 数（讲义 Part A p.124）：<div class="calc">η = 45.9/56 ≈ 0.82<br>（用 45.0 算：45.0/56 = 0.80）</div>')
  + S(5, '<b>(ii) 用户数</b>：每用户话务量 = 每小时呼叫数 × 每次时长（小时）：<div class="calc">A<sub>u</sub> = 2 × 15/60 = 0.5 E/用户<br>U = A/A<sub>u</sub> = 45.9/0.5 = 91.8 → 91 个用户</div>向下取整：91 × 0.5 = 45.5 E ≤ 45.9 ✓；92 × 0.5 = 46.0 E &gt; 45.9，阻塞率会超过 2%。')
  + S(6, '<b>(iii) 换成 N = 7</b>：<div class="calc">M = 504/7 = 72 条/小区<br>Erlang B（72，2%）：A ≈ 61.0 E<br>承载 = 61.0 × 0.98 = 59.8 E<br>η = 61.0/72 ≈ 0.85（用 59.8 算：0.83）<br>用户 = 61.0/0.5 = 122 人</div>')
  + S(7, '<b>(iii) 评论</b>：簇变小，每小区信道变成 72/56 = 1.29 倍（+29%），可承载话务量却变成 61.0/45.9 = 1.33 倍（+33%），中继效率从 0.82 升到 0.85：信道池越大，中继效率越高（讲义 Part A p.123–124）。代价是同频小区离得更近，Q = √(3N) 变小，SIR 下降（按 n = 4）：<div class="calc">N = 9：Q⁴/6 = 27²/6 = 121.5 → 20.8 dB<br>N = 7：Q⁴/6 = 21²/6 = 73.5 → 18.7 dB</div>（同讲义 Part A p.89 的表。）只要 SIR 要求不超过 18 dB，N = 7 更划算。')
  + '<div class="wans">N = 9：45.9 E，η ≈ 0.82，91 人；N = 7：61.0 E，η ≈ 0.85，122 人</div>'),
]
