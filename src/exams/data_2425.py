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
 sol=S(1, '<b>(i) 读图。</b>dB 形式：10 log₁₀(P<sub>r</sub>/P<sub>t</sub>) = K<sub>dB</sub> − 35 log₁₀ d。图中的线从 A 往右<b>下降</b>，说明纵轴画的是 10 log₁₀(P<sub>r</sub>/P<sub>t</sub>)（损耗越大越往下）。<br>• d = 1 m 时 log₁₀ d = 0，纵坐标就是 K<sub>dB</sub>：<b>A = −30 dB</b>（即 1 m 处损耗 30 dB）。<br>• 从 A 到横轴下降了 88 dB，斜率是 −35 dB/十倍距离：<div class="calc">35 × B = 88 → B = log₁₀ d = 2.51（d ≈ 327 m）</div>')
  + S(2, '<b>(ii) 符号时长</b>：一次平均衰落正好盖住 3 个符号：T<sub>s</sub> = 6 µs / 3 = <b>2 µs</b>。<br><b>每秒误符号数</b>：每次衰落持续 3T<sub>s</sub>。如果和符号边界对齐，正好 3 个符号全在衰落里；如果不对齐，就是 2 个完整符号加头尾两个"碎片"，两个碎片加起来是一个符号长，必有一个超过一半（恰好各一半是边界情况）。所以每次衰落约 3 个错符号。LCR = 5 次/秒：<div class="calc">误符号数 = 5 × 3 = 15 个/秒</div>')
  + S(3, '<b>(iii) 注水分配。</b>SNR 化线性：γ = 63.1、10、2.0。先假设三个子带都分到功率，ΣP<sub>i</sub> = 1：<div class="calc">3/γ₀ − (1/63.1 + 1/10 + 1/2.0) = 1 → 1/γ₀ = (1 + 0.0158 + 0.1 + 0.501)/3 = 0.539</div>γ₀ = 1.855（2.7 dB），三个 γ<sub>i</sub> 都 ≥ γ₀，假设成立。<div class="calc">P₁ = 0.539 − 0.016 = 0.523 W；P₂ = 0.539 − 0.100 = 0.439 W；P₃ = 0.539 − 0.501 = 0.038 W</div>三者之和为 1 W。SNR 越好的子带分到的功率越多；最差的 3 dB 子带只比门限高一点，分到的很少。')
  + '<div class="wans">(i) A = −30 dB，B ≈ 2.51　(ii) T<sub>s</sub> = 2 µs，15 个误符号/秒　(iii) P ≈ 0.523 / 0.439 / 0.038 W</div>',
 note='如果把纵轴理解为正的路径损耗 −K<sub>dB</sub> + 35 log d，则 A = 30 dB；但那条线应该上升。按图中下降的线，A = K<sub>dB</sub> = −30 dB。B 两种理解都一样。'),

dict(id='y2425s2-q1b1', paper=P, q='Q1(b)(i)', marks='(b) 共 12', page='p2', ch='ch4',
 topic='BPSK 选择分集：由 P<sub>out</sub> 反求支路数 M',
 en='''<p>(b) One common technique used to mitigate fading effects is Diversity.</p>
<p>(i) The Selection Diversity scheme of a BPSK system uses M branches. The BPSK system's outage probability at a probability of error of P<sub>b</sub> = Q(√(2 × γ<sub>b</sub>)) = 1.35 × 10<sup>−3</sup> can be expressed as,
<span class="eq">P<sub>out</sub> = (1 − e<sup>−γ<sub>b</sub>/30</sup>)<sup>M</sup></span>
If P<sub>out</sub> equals 0.02 approximately, determine the number of branches used by the BPSK system.</p>''',
 sol=S(1, '先从误码率门限求 γ<sub>b</sub>：查 Q 表，Q(3.0) = 1.35×10⁻³，所以 √(2γ<sub>b</sub>) = 3.0：<div class="calc">γ<sub>b</sub> = 9/2 = 4.5</div>这里 30 是每支路的平均 SNR，γ<sub>b</sub> 是能接受的最低 SNR。')
  + S(2, '<div class="calc">1 − e<sup>−4.5/30</sup> = 1 − e<sup>−0.15</sup> = 0.139</div><div class="calc">0.139<sup>M</sup> = 0.02 → M = ln 0.02 / ln 0.139 = (−3.91)/(−1.97) ≈ 1.98</div>验证：M = 2 时 P<sub>out</sub> = 0.139² = 0.0194 ≈ 0.02 ✓（M = 1 是 0.139，M = 3 是 0.0027）。')
  + '<div class="wans">M = 2 个支路</div>'),

dict(id='y2425s2-q1b2', paper=P, q='Q1(b)(ii)(iii)', marks='(b) 共 12', page='p2', ch='ch5',
 topic='最大分集增益 N×M · 分集-复用折中求速率 · 无信息发射机的 MIMO 容量',
 en='''<p>(ii) For a MIMO system that uses 5 transmit antennas and 3 receive antennas, what is the maximum diversity gain of the system? If the system operates with a diversity gain of 3 and a multiplexing gain of 2, determine the maximum transmission rate per Hz of the system at a probability of error of 10<sup>−3</sup>.</p>
<p>(iii) The channel capacity of a MIMO system with N transmitter antennas and M receiver antennas can be expressed as,
<span class="eq">C<sub>MIMO</sub> = B × log<sub>2</sub> det{I + (1/σ<sup>2</sup>) HPH<sup>H</sup>}</span>
where B is the receiver bandwidth, I is the Identity matrix, σ<sup>2</sup> is the noise power, H and P are the channel matrix and transmit power matrix respectively, H<sup>H</sup> is the conjugate transpose of H, and det{X} is the determinant of the matrix X. Simplify the channel capacity expression if the MIMO system has an uninformed transmitter with a total transmit power of P. Hence determine the channel capacity per Hz of this system if N = M = 1, P = 1, σ<sup>2</sup> = 0.25, and the channel gain is 2.</p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(ii) 最大分集增益</b> d<sub>max</sub> = N × M = 5 × 3 = <b>15</b>。<br><b>速率</b>：讲义 Ch4 p.32–33，P<sub>e</sub> ≈ SNR<sup>−d</sup>，R = r log₂ SNR。先由误码率和分集增益求 SNR：<div class="calc">10⁻³ = SNR⁻³ → SNR = 10</div><div class="calc">R = r log₂ SNR = 2 × log₂ 10 = 2 × 3.32 ≈ 6.64 bit/s/Hz</div>顺便检查：(r, d) = (2, 3) 正好在最优折中曲线上，d(2) = (5−2)(3−2) = 3。')
  + S(2, '<b>(iii) 无信息发射机</b>：发射端不知道信道，就把总功率平均分给 N 根天线，P = (P/N) I（讲义 Ch5 p.37）：<div class="calc">C = B log₂ det{I + (P/(Nσ²)) HH<sup>H</sup>}</div>N = M = 1 时 H 就是标量 h，HH<sup>H</sup> = |h|² = 4：<div class="calc">C/B = log₂(1 + 1 × 4/0.25) = log₂ 17 ≈ 4.09 bit/s/Hz</div>')
  + '<div class="wans">(ii) d<sub>max</sub> = 15；R ≈ 6.64 bit/s/Hz　(iii) C/B = log₂17 ≈ 4.09 bit/s/Hz</div>',
 note='"channel gain is 2" 按幅度增益 h = 2 理解（|h|² = 4）。如果理解成功率增益 |h|² = 2，结果是 log₂ 9 ≈ 3.17。'),

dict(id='y2425s2-q2a', paper=P, q='Q2(a)', marks=13, page='p2', ch='ch6',
 topic='横向滤波器 · 迫零均衡抽头 · 残余 ISI 下的误码率',
 en='''<p>2. (a) The Z-transform of a channel is H(Z) = 1 + hZ<sup>−1</sup>, where h is the channel gain. The equalizer at the receiver is implemented as a transversal filter shown in Figure 2, where r<sub>i</sub> and y<sub>i</sub> are the received signal and equalizer output respectively, c<sub>0</sub>, c<sub>1</sub> and c<sub>2</sub> are the equalizer gain coefficients, and Z<sup>−1</sup> represents a delay of 1 symbol duration.</p>''' + FIG2 + '''
<p>(i) What should the value of h be for an AWGN channel without fading? What would you observe on the value of h for fast-fading channels? Explain your answers.</p>
<p>(ii) If the equalizer implements the zero-forcing technique, determine the values of c<sub>1</sub>, c<sub>2</sub>, and c<sub>3</sub> in Figure 2, if h = 0.2.</p>
<p>(iii) The equalizer is now implemented with another design such that the decision variable is y<sub>i</sub> = s<sub>i</sub> + 0.6s<sub>i−1</sub> + w′<sub>i</sub>, where s<sub>i</sub> is the transmitted symbol that is equally likely to be 1 or −1, and w′<sub>i</sub> is an additive white Gaussian noise with zero mean and a variance of 0.64. The decision rule is such that, s<sub>i</sub> will be detected as 1 if y<sub>i</sub> ≥ 0, or −1 if y<sub>i</sub> &lt; 0. Determine the probability of error for this equalizer.</p>
<p class="marks">(13 Marks)</p>''',
 sol=S(1, '<b>(i)</b> 纯 AWGN、没有多径衰落时，信道只有一条直达路径，H(Z) = 1，所以 <b>h = 0</b>（没有 ISI）。快衰落信道的相干时间和符号时长相当甚至更短，<b>h 会随时间快速变化</b>（幅度和相位都在变），均衡器系数必须不断重新估计和跟踪，否则很快失配。')
  + S(2, '<b>(ii) 迫零均衡</b>：C(Z) = 1/H(Z) = 1/(1 + 0.2Z⁻¹)，长除法展开（讲义 Ch6 p.24 的做法）：<div class="calc">1/(1 + 0.2Z⁻¹) = 1 − 0.2Z⁻¹ + 0.04Z⁻² − 0.008Z⁻³ + …</div>只有 3 个抽头，取前三项：<div class="calc">c₀ = 1，c₁ = −0.2，c₂ = 0.04</div>')
  + S(3, '<b>(iii)</b> σ = √0.64 = 0.8。发 s<sub>i</sub> = +1 时，前一个符号带来 ±0.6 的干扰，各占一半：<br>• s<sub>i−1</sub> = +1：y 的均值 1.6，出错要 y &lt; 0 → Q(1.6/0.8) = Q(2) = 0.0228<br>• s<sub>i−1</sub> = −1：均值 0.4 → Q(0.4/0.8) = Q(0.5) = 0.3085<div class="calc">P<sub>e</sub> = ½(0.3085 + 0.0228) ≈ 0.166</div>发 −1 时由对称性相同。残余 ISI 太大（0.6），误码率很高，说明这个设计不好。')
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
 sol=S(1, '<b>(i)</b> 4 电平 → 每符号 log₂4 = 2 bit。系统速率 = 5 M × 2 = <b>10 Mbit/s</b>。分到 4 个子载波，每个子载波符号率 1.25 Msymbol/s，<b>2.5 Mbit/s</b>。')
  + S(2, '<b>(ii)</b> 讲义 Ch7 p.17、p.21 的写法：表达式不变，只把每个块的时间范围往前延伸 T<sub>g</sub>：<div class="calc">x(t) = (1/√T) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub>(t) e<sup>j2πkt/T</sup>，　nT − T<sub>g</sub> ≤ t &lt; (n+1)T</div>因为 e<sup>j2πkt/T</sup> 以 T 为周期，前面多出的 T<sub>g</sub> 段正好是块尾 T<sub>g</sub> 段的复制，这就是"循环"前缀；接收端丢掉这一段，只取 nT ≤ t &lt; (n+1)T。（若按块周期 T + T<sub>g</sub> 计时，也可写成区间 n(T+T<sub>g</sub>) ≤ t &lt; (n+1)(T+T<sub>g</sub>)、指数里用 t − n(T+T<sub>g</sub>) − T<sub>g</sub>。）')
  + S(3, '<b>(iii)</b> 每个子载波都要 ¼ log₂(1 + P<sub>k</sub>|H<sub>k</sub>|²) = 0.9：<div class="calc">1 + P<sub>k</sub>|H<sub>k</sub>|² = 2<sup>3.6</sup> = 12.13 → P<sub>k</sub>|H<sub>k</sub>|² = 11.13</div><div class="calc">P₁ = 11.13/1 = 11.13；P₂ = 11.13/0.04 = 278.1；P₃ = 11.13；P₄ = 11.13/1.96 = 5.68</div><div class="calc">P<sub>total</sub> ≈ 306.1（功率单位）</div>差的子载波（|H₂| = 0.2）一个人就吃掉 90% 的功率。这正好说明为什么要用注水法，而不是强求每个子载波容量相同。')
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
 sol=S(1, '<b>(a) 系统总信道数。</b>FDD：40 MHz 一半上行一半下行，每个方向 20 MHz，扣掉 2 MHz 控制信令，剩 18 MHz。"carrier frequency is 200 KHz" 应理解为每个载波<b>带宽</b> 200 kHz：<div class="calc">载波数 = 18 MHz / 200 kHz = 90；双工信道 = 90 × 8 时隙 = 720</div><b>选簇大小</b>：6 个等距干扰、手机在小区边缘，S/I = Q<sup>n</sup>/6 ≥ 10<sup>1.8</sup> = 63.1：<div class="calc">Q<sup>3.7</sup> ≥ 378.6 → Q ≥ 4.98 → N = Q²/3 ≥ 8.25</div>合法簇大小（i² + ij + j²）里 ≥ 8.25 的最小值是 <b>N = 9</b>（N = 7 只有 16.7 dB，不够；N = 9 为 18.7 dB）。<div class="calc">每小区信道 = 720/9 = 80 条双工信道</div>')
  + S(2, '<b>(b)</b> 小区面积 = 2.598 × 1² = 2.598 km²，用户 = 2.598 × 2000 = 5196，话务量 = 5196 × 0.03 = <b>155.9 E</b>。Erlang B 表 M = 80、B = 1%：A ≈ <b>65.4 E</b>。155.9 远大于 65.4，<b>不能</b>满足 1% 阻塞率（阻塞率会远高于 1%）。')
  + S(3, '<b>(c) 小区分裂</b>：分裂后每个小区信道数不变（仍 80 条，SIR 只取决于 Q = D/R，分裂后 D 和 R 同比例缩小），但每个小区覆盖的用户变少。要求每小区话务量 ≤ 65.4 E：<div class="calc">面积 ≤ 65.4/(2000 × 0.03) = 1.09 km² → R = √(1.09/2.598) ≈ 0.648 km</div>新半径约 <b>650 m</b>（基站数约增加到 2.4 倍），即可满足 1%。')
  + S(4, '<b>(d) 三扇区</b>：每个扇区只剩 2 个同频干扰，SIR = 1/(Q<sup>−n</sup> + (Q + 0.7)<sup>−n</sup>)，可以用更小的簇：<div class="calc">N = 3：Q = 3 → 16.0 dB ✗；　N = 4：Q = 3.46 → 18.2 dB ✓</div>取 N = 4：每小区 720/4 = 180 条，每扇区 60 条（每小区 22.5 个载波，"一个载波可被两个扇区共用"正是让每扇区分到 7.5 个载波 = 60 条成立）。Erlang B（M = 60，1%）：A ≈ 46.9 E/扇区，每小区 140.8 E。<br>全城面积 = 60 × 2.598 = 155.9 km²，总话务量 = 155.9 × 2000 × 0.03 = 9353 E：<div class="calc">小区数 = 9353 / 140.8 ≈ 66.4 → 67 个小区</div>（对应半径约 0.95 km。）对比：不改簇、只加扇区（N = 9、每扇区约 26–27 条）需要约 180 个小区，反而更多。扇区化必须配合缩小簇才划算。')
  + '<div class="wans">(a) N = 9，80 条/小区　(b) 需 155.9 E，只能承载 65.4 E，不能　(c) R ≈ 0.65 km　(d) N = 4，每扇区 60 条，约 67 个小区</div>',
 note='(d) 的题意有不同理解，这里采用"扇区化 → 允许更小的簇 → 每小区信道更多"的思路，并说明了只加扇区不改簇的结果。'),

dict(id='y2425s2-q4a', paper=P, q='Q4(a)', marks=8, page='A', ch='ch2', hw='HW1 Q1(a)',
 topic='蜂窝系统六大组成之数据库：HLR 与 VLR',
 en='''<p>4. (a) For every cellular network, a database unit is one of the six basic components. What are the basic functions of the database unit? Describe the differences between the home location register (HLR) and the visitor location register (VLR) in the database units.</p>
<p class="marks">(8 Marks)</p>''',
 sol=S(1, '<b>数据库的基本功能</b>（讲义 Part A p.11 的 Component 3）：保存用户签约信息（号码、业务权限、计费信息）和<b>位置信息</b>，供 MTSO 在呼叫建立、寻呼被叫、鉴权、漫游和切换时查询；没有它，网络不知道"这个用户是谁、现在在哪"。')
  + S(2, '<b>HLR（归属位置寄存器）</b>：每个用户在其归属网络里有一条<b>永久记录</b>，存签约资料、鉴权参数和"当前在哪个 VLR/MSC 区域"的指针。一个运营商通常只有一个（逻辑上的）HLR。')
  + S(3, '<b>VLR（拜访位置寄存器）</b>：和每个 MSC/MTSO 区域关联，保存当前<b>在本区域内</b>的用户（包括外地来的漫游用户）的<b>临时副本</b>，用户进入时从 HLR 下载，离开后删除。本地呼叫和寻呼查 VLR 就够，不用每次都去问 HLR，减少信令。')
  + S(4, '<b>区别一句话</b>：HLR 是"户口所在地"，永久、集中、存全部签约信息；VLR 是"暂住登记"，临时、分布在各个服务区、只存当前在场的用户。用户移动到新区域时，新 VLR 向 HLR 登记，HLR 更新位置并通知旧 VLR 删除记录。')
  + '<div class="wans">数据库存用户与位置信息；HLR 永久归属记录，VLR 临时拜访记录</div>',
 note='讲义只在 p.11 的框图里列出 "Databases"，HLR/VLR 的细节属于课外补充（GSM 的标准结构），和 HW1 Q1(a) 的答法一致。'),

dict(id='y2425s2-q4b', paper=P, q='Q4(b)', marks=8, page='B', ch='ch7',
 topic='IoT 通信网络层的四个子层',
 en='''<p>(b) Internet of Things (IoT) networks are built around the concept of "things" or smart objects performing functions and delivering new connected services. For the core functional IoT stack, the communication network layer is structured with four sublayers. List down each of these sublayers and briefly describe the each of the features.</p>
<p class="marks">(8 Marks)</p>''',
 sol=S(1, '<b>接入网子层（Access network）</b>：IoT 网络的"最后一公里"，通常是无线技术，如 802.11ah、802.15.4g、LoRa；按覆盖范围分 PAN、HAN、NAN、FAN、LAN、WAN 等（讲义 p.89、p.94–95）。')
  + S(2, '<b>网关与回传子层（Gateways and backhaul）</b>：把一片区域内的多个智能物体汇聚到一个公共网关，网关再用更长距离的介质（如蜂窝、光纤）把数据转发到中心站；物体可以静止或在小范围移动，网关通常固定。')
  + S(3, '<b>网络传输子层（Network transport）</b>：用开放、标准化的网络层和传输层协议（IP、UDP/TCP）连接各种设备和介质；要求可扩展到成千上万个传感器并保证安全。IP 能适应低功耗、低带宽、高丢包的网络；TCP 由网络控制可靠传输，UDP 把控制交给应用。')
  + S(4, '<b>IoT 网络管理子层（IoT network management）</b>：应用层协议，负责智能物体与头端应用之间的数据交换，如基于 TCP 的 HTTP（传感器作为客户端），以及适合低内存、低带宽、高丢包环境的轻量双向协议 WebSocket。')
  + '<div class="wans">Access network / Gateways &amp; backhaul / Network transport / IoT network management</div>'),

dict(id='y2425s2-q4c', paper=P, q='Q4(c)', marks=9, page='A', ch='ch8', hw='HW1 Q1(b)',
 topic='Erlang B：承载话务量 · 中继效率 · 用户数 · 换簇大小',
 en='''<p>(c) For a cellular system, suppose you selected the cluster size of N<sub>c</sub> = 9, with a total number of available channels of 504. Assume that the average users place 2 calls of 15 minutes duration per hour for the given cellular system.</p>
<p>(i) Determine the carrier load per cell and the trunking efficiency for a 2% Grade of Service (GOS)?</p>
<p>(ii) Calculate the number of users that can be accommodated for this cell at that given GOS.</p>
<p>(iii) Compute the carried load and trunking efficiency if the cluster size is changed to N<sub>c</sub>=7. Comment on your results.</p>
<p class="marks">(9 Marks)</p>''',
 sol=S(1, '<b>(i)</b> 每小区 M = 504/9 = 56 条。Erlang B（M = 56，2%）：A ≈ <b>45.9 E</b>（和讲义 p.44 AMPS 例题同一个数）。严格的承载话务量 = A(1 − P<sub>B</sub>) = 45.9 × 0.98 = 45.0 E。中继效率 = 45.9/56 ≈ <b>0.82</b>（用 45.0 算是 0.80）。"carrier load" 是 carried load 的笔误。')
  + S(2, '<b>(ii)</b> A<sub>u</sub> = 2 × 15/60 = 0.5 E/用户：<div class="calc">U = 45.9/0.5 = 91.8 → 91 个用户</div>向下取整，多一个人就超过 2% 阻塞率。')
  + S(3, '<b>(iii)</b> N = 7：M = 504/7 = 72，A ≈ 61.0 E，承载 61.0 × 0.98 = 59.8 E，中继效率 61.0/72 ≈ <b>0.85</b>，用户 122 人。<br><b>评论</b>：簇变小，每小区信道多了 29%，话务量却多了 33%，因为信道池越大集群效率越高；代价是同频小区离得更近，SIR 从 20.8 dB 降到 18.7 dB（n = 4），余量变小。')
  + '<div class="wans">N = 9：45.9 E，η ≈ 0.82，91 人；N = 7：61.0 E，η ≈ 0.85，122 人</div>'),
]
