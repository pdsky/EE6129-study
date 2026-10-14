# EE6129 Semester 2 Examination 2023-2024 (April/May 2024)
# Verbatim question text transcribed from the scanned paper; solutions checked by verify.py.

P = 'y2324s2'

def S(n, html):  # one solution step
    return f'<div class="wstep"><div class="wn">{n}</div><div class="wtext">{html}</div></div>'

SVG_PL = '''<div class="figwrap"><svg viewBox="0 0 460 250" role="img" aria-label="路径损耗（dB）对 10log10 d 的草图：一条斜率为 γ 的直线，截距为 −K_dB，阴影衰落使测量点散布在直线两侧">
<line x1="50" y1="215" x2="440" y2="215" style="stroke:var(--ink)" stroke-width="1.5"/>
<line x1="50" y1="215" x2="50" y2="15" style="stroke:var(--ink)" stroke-width="1.5"/>
<line x1="50" y1="170" x2="420" y2="45" style="stroke:var(--accent)" stroke-width="2.5"/>
<g style="fill:var(--gold)"><circle cx="90" cy="150" r="3.5"/><circle cx="120" cy="160" r="3.5"/><circle cx="150" cy="122" r="3.5"/><circle cx="185" cy="140" r="3.5"/><circle cx="215" cy="104" r="3.5"/><circle cx="250" cy="122" r="3.5"/><circle cx="280" cy="80" r="3.5"/><circle cx="315" cy="98" r="3.5"/><circle cx="345" cy="62" r="3.5"/><circle cx="380" cy="72" r="3.5"/></g>
<line x1="250" y1="102" x2="320" y2="102" style="stroke:var(--ink-faint)" stroke-dasharray="4 3"/>
<line x1="320" y1="102" x2="320" y2="78" style="stroke:var(--ink-faint)" stroke-dasharray="4 3"/>
<text x="326" y="96" font-size="12" style="fill:var(--ink)">斜率 = γ</text>
<text x="8" y="174" font-size="12" style="fill:var(--accent-ink)">−K<tspan font-size="9" dy="3">dB</tspan></text>
<text x="56" y="28" font-size="12" style="fill:var(--ink)">P<tspan font-size="9" dy="3">L,dB</tspan><tspan dy="-3"> = P</tspan><tspan font-size="9" dy="3">t,dB</tspan><tspan dy="-3"> − P</tspan><tspan font-size="9" dy="3">r,dB</tspan></text>
<text x="330" y="238" font-size="12" style="fill:var(--ink)">10 log₁₀ d (dB)</text>
<text x="44" y="232" font-size="11" style="fill:var(--ink-soft)">0（d = 1）</text>
<text x="140" y="196" font-size="11" style="fill:var(--gold)">● 实测点：阴影衰落 ψ<tspan font-size="8" dy="3">dB</tspan><tspan dy="-3"> 让它们散在直线两侧</tspan></text>
</svg><div class="cap">横轴用 10 log₁₀ d（单位 dB），纵轴是路径损耗（dB）。直线在 d = 1 处的截距是 −K<sub>dB</sub>，斜率是 γ。</div></div>'''

QS = [
dict(id='y2324s2-q1a', paper=P, q='Q1(a)', marks=12, page='p2', ch='ch2', quiz=True,
 topic='路径损耗 dB 形式 · 阴影衰落中断 · 平坦/慢衰落判别 · 衰落余量',
 en='''<p>1. (a) A wireless channel can be modelled using a simplified path loss model, or a model incorporating the effect of shadowing, or a more complex fading model, depending on the types of the channels assumed.</p>
<p>(i) The path loss model that includes shadowing can be expressed as,
<span class="eq">P<sub>r</sub> = P<sub>t</sub>K(d)<sup>−γ</sup>ψ</span>
where P<sub>r</sub> and P<sub>t</sub> are the received and transmitted signal power respectively, d is the distance between the transmitter and the receiver, K is a constant, γ is the path loss exponent, and ψ is a random variable due to shadowing. Convert this model into the dB form and use it to sketch a graph of path loss (in dB) versus distance (in dB) and indicate how K<sub>dB</sub> and γ fit in the graph.</p>
<p>(ii) For the model described in part (a)(i) above, if the mean value of P<sub>r,dB</sub> is 10 dB higher than the minimum received signal power needed for non-outage, determine the maximum value of the variance of ψ<sub>dB</sub> that will result in an outage probability lower than 1%.</p>
<p>(iii) A signal, s(t), with a symbol duration of 1 ms, is transmitted through a fading channel. The channel has a time invariant channel impulse response and a rms delay spread of 0.01ms. What is the fading type of this channel? Explain your answer.</p>
<p>(iv) Consider the Rayleigh fading channel. At an outage probability of ε, the outage capacity per Hz of the channel can be expressed as
<span class="eq">C<sub>ε</sub> = log<sub>2</sub>[1 + γ̄<sub>R</sub> ln(1/(1 − ε))]</span>
where γ̄<sub>R</sub> is the average signal to noise ratio for the fading channel. Determine the fade margin at an outage probability of 0.1%.</p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(i) 化成 dB。</b>两边取 10 log₁₀：<div class="calc">P<sub>r,dB</sub> = P<sub>t,dB</sub> + K<sub>dB</sub> − 10γ log₁₀ d + ψ<sub>dB</sub></div>路径损耗定义为发射功率减接收功率：<div class="calc">P<sub>L,dB</sub> = P<sub>t,dB</sub> − P<sub>r,dB</sub> = −K<sub>dB</sub> + γ·(10 log₁₀ d) − ψ<sub>dB</sub></div>把横轴取成 10 log₁₀ d（"距离的 dB"），去掉随机项后就是一条直线：<b>斜率是 γ</b>，在 d = 1（横轴 0 dB）处的<b>截距是 −K<sub>dB</sub></b>。ψ<sub>dB</sub> 是零均值高斯随机变量，所以实测点散布在直线两侧。' + SVG_PL)
  + S(2, '<b>(ii) 阴影衰落的中断概率。</b>P<sub>r,dB</sub> 服从均值 μ、标准差 σ（dB）的高斯分布，σ² 就是 ψ<sub>dB</sub> 的方差。中断 = 接收功率低于门限 P<sub>min</sub>：<div class="calc">P<sub>out</sub> = P(P<sub>r,dB</sub> &lt; P<sub>min</sub>) = Q((μ − P<sub>min</sub>)/σ) = Q(10/σ)</div>要求 Q(10/σ) &lt; 0.01。查 Q 表：Q(2.33) ≈ 0.01，Q 是减函数，所以要 10/σ &gt; 2.33：<div class="calc">σ &lt; 10/2.33 = 4.30 dB　→　σ² &lt; 18.5 dB²</div>')
  + S(3, '<b>(iii) 衰落类型。</b>两个维度分别判断：<br>• <b>频率上</b>：σ<sub>τ</sub>/T<sub>s</sub> = 0.01 ms / 1 ms = 0.01 &lt; 0.1，满足讲义的经验法则，所以是<b>平坦衰落</b>（时延扩展远小于符号时长，几乎没有 ISI）。<br>• <b>时间上</b>：信道冲激响应不随时间变化，相当于没有多普勒扩展、相干时间无穷大，符号时长远小于相干时间，所以是<b>慢衰落</b>。<br>结论：<b>平坦慢衰落</b>（flat, slow fading）。')
  + S(4, '<b>(iv) 衰落余量。</b>要和 AWGN 信道达到同样容量，瑞利信道需要多出的平均 SNR（讲义 Ch2 p.51）：<div class="calc">FM = 10 log₁₀[1 / ln(1/(1 − ε))]</div>ε = 0.001：ln(1/0.999) = 0.0010005，<div class="calc">FM = 10 log₁₀(1/0.0010005) ≈ 30.0 dB</div>对照讲义例子：ε = 1% 时是 20 dB。中断概率要求严 10 倍，余量就多 10 dB。')
  + '<div class="wans">(ii) σ² &lt; 18.5 dB²（σ &lt; 4.3 dB）　(iii) 平坦、慢衰落　(iv) 衰落余量 ≈ 30 dB</div>'),

dict(id='y2324s2-q1b1', paper=P, q='Q1(b)(i)', marks='(b) 共 13', page='p2', ch='ch4',
 topic='DPSK 两支路选择分集 · 离散 SNR 分布求平均',
 en='''<p>(b) Diversity techniques can be used to lower the outage probability of a wireless system operating in a fading channel.</p>
<p>(i) A Differential Phase Shift Keying (DPSK) system uses a 2-branch Selection Diversity (SD) scheme to mitigate fading. The signal to noise ratio (SNR) of the received signal for each branch is assumed to be a discrete random variable with the following distribution:
<span class="eq">10 dB with a probability of 0.2;　12 dB with a probability of 0.8</span>
Determine the average SNR in dB of the received signals and the average symbol error probability of the SD scheme. Note: Symbol error probability of DPSK is ½e<sup>−SNR</sup>.</p>''',
 sol=S(1, '先把 dB 换成线性值（公式里的 SNR 一定要用线性值）：10 dB → 10，12 dB → 15.85。')
  + S(2, '<b>每支路接收信号的平均 SNR</b>：<div class="calc">γ̄ = 0.2 × 10 + 0.8 × 15.85 = 14.68 → 11.67 dB</div>注意要先在线性域平均再转 dB。直接平均 dB 值（0.2×10 + 0.8×12 = 11.6 dB）是错的做法。')
  + S(3, '<b>选择分集取两支路中 SNR 较大的一个。</b>两支路独立，只有两支都是 10 dB 时输出才是 10 dB：<div class="calc">P(输出 = 10 dB) = 0.2 × 0.2 = 0.04；P(输出 = 12 dB) = 1 − 0.04 = 0.96</div>SD 输出的平均 SNR = 0.04 × 10 + 0.96 × 15.85 = 15.61 → 11.94 dB。')
  + S(4, '<b>平均误符号率</b>：对每种输出情况算 ½e<sup>−SNR</sup> 再按概率加权：<div class="calc">P̄<sub>s</sub> = 0.04 × ½e<sup>−10</sup> + 0.96 × ½e<sup>−15.85</sup> = 9.08×10⁻⁷ + 6.2×10⁻⁸ ≈ 9.7×10⁻⁷</div>对比不用分集（单支路）：0.2 × ½e<sup>−10</sup> + 0.8 × ½e<sup>−15.85</sup> ≈ 4.6×10⁻⁶。分集让误码率降到约 1/5，主要是把"差的那种情况"出现的概率从 0.2 压到 0.04。')
  + '<div class="wans">接收信号平均 SNR ≈ 11.7 dB（SD 输出平均 ≈ 11.9 dB）；SD 平均误符号率 ≈ 9.7×10⁻⁷</div>',
 note='题目说的 "average SNR of the received signals" 指每支路的接收 SNR。为保险，SD 输出端的平均 SNR 也一并写出。'),

dict(id='y2324s2-q1b2', paper=P, q='Q1(b)(ii)–(iv)', marks='(b) 共 13', page='p2', ch='ch5',
 topic='空间复用 · 复用增益 min(N,M) · Alamouti 正交性与分集增益',
 en='''<p>(ii) Briefly describe the basic principle of the spatial multiplexing scheme and the mathematical relationship between the number of transmit antennas and the number of receive antennas for the scheme. For a MIMO system with 3 transmit antennas and 5 receive antennas, find the maximum possible multiplexing gain.</p>
<p>(iii) A Space-Time Block Coding system uses 2 transmit antennas and 2 time slots to transmit 2 complex symbols, s<sub>1</sub> and s<sub>2</sub>. The code can be represented by the matrix
<span class="eq">X = ( s<sub>1</sub>　−s<sub>2</sub>* ; s<sub>2</sub>　s<sub>1</sub>* )</span>
where s<sub>1</sub> and s<sub>1</sub> are the two transmitted symbols, and s<sub>1</sub>* and s<sub>2</sub>* are the complex conjugates of s<sub>1</sub> and s<sub>1</sub> respectively. Show that this is or is not an orthogonal space time block code.</p>
<p>(iv) Does the Alamouti code have diversity gain? Explain your answer.</p>
<p class="marks">(13 Marks)</p>''',
 sol=S(1, '<b>(ii) 空间复用</b>（讲义 Ch4 p.30）：把 N 个不同的数据符号同时从 N 根发射天线发出去，速率变成原来的 N 倍；代价是没有分集增益，衰落信道里误码性能可能较差。接收端要解出 N 路数据流，需要 <b>M ≥ N</b> 根接收天线。最大复用增益 r<sub>max</sub> = min(N, M)：<div class="calc">N = 3，M = 5 → r<sub>max</sub> = min(3, 5) = 3</div>')
  + S(2, '<b>(iii) 正交性检验。</b>正交 STBC 的定义（讲义 Ch5 p.22、p.27）是 X X<sup>H</sup> = (|s₁|² + |s₂|²) I。题中的 X 有两行：r₁ = (s₁, −s₂*)，r₂ = (s₂, s₁*)。<div class="calc">r₁·r₁<sup>H</sup> = |s₁|² + |s₂|²；　r₂·r₂<sup>H</sup> = |s₂|² + |s₁|²</div><div class="calc">r₁·r₂<sup>H</sup> = s₁s₂* + (−s₂*)(s₁*)* = s₁s₂* − s₂*s₁ = 0</div>所以 X X<sup>H</sup> = (|s₁|² + |s₂|²) I，<b>是正交 STBC</b>。它其实就是讲义 Alamouti 矩阵的转置（讲义把行当时隙，这里把列当时隙），本质一样。')
  + S(3, '<b>(iv) Alamouti 有分集增益。</b>每个符号在两个时隙里分别从两根天线各发一次，经过两条独立衰落的路径到达接收端；接收端利用正交结构做线性合并，得到的检测量里有 (|h₁|² + |h₂|²)，两条路径同时深衰落的概率很小。2 发 1 收时分集阶数为 2，2 发 M 收时为 2M，即<b>满分集</b> N × M。代价：它不需要发射端知道信道，但相比接收端 MRC 少了阵列增益（讲义 Ch5 p.30 "MRC has array gain over OSTBC &amp; Alamouti code"）。')
  + '<div class="wans">(ii) 需 M ≥ N；最大复用增益 = 3　(iii) X X<sup>H</sup> = (|s₁|²+|s₂|²)I，是正交 STBC　(iv) 有，满分集 2M</div>',
 note='原题 (iii) 把 "s₁ and s₂" 印成了 "s₁ and s₁"，按 s₁、s₂ 理解即可。'),

dict(id='y2324s2-q2a', paper=P, q='Q2(a)', marks=13, page='p2', ch='ch6',
 topic='ISI 离散模型 · 由 H(Z) 读冲激响应 · 线性均衡后的判决与误码率',
 en='''<p>2. (a) The discrete time representation of the received signal, {r[i], i = 1,2, …}, at the output of an Additive White Gaussian Noise (AWGN) Inter-Symbol-Interference (ISI) channel can be expressed as,
<span class="eq">r[i] = Σ<sub>n=1</sub><sup>3</sup> h[n] m[i − n + 1] + w[i]</span>
where m[k] is the k<sup>th</sup> transmitted symbol which is assumed to be equally likely to be −1 or 1, h[n] is the n<sup>th</sup> component of the sampled channel impulse response, and w[i] is the i<sup>th</sup> sample of the AWGN with zero mean and a variance of 0.3.</p>
<p>(i) Explain how the discrete time representation above shows that ISI is present.</p>
<p>(ii) If the Z-transform of the channel is, H(Z) = 1 + 0.6Z<sup>−2</sup>, determine all non-zero values of h[n].</p>
<p>(iii) The received signal is processed by a linear filter which has a Z-transform of C(Z) = 1 − 0.6Z<sup>−2</sup>. The output of the filter is used as the decision variable for detecting m[i]. Derive the decision rule.</p>
<p>(iv) Using the decision rule, determine the average probability of bit error of this system.</p>
<p class="marks">(13 Marks)</p>''',
 sol=S(1, '<b>(i)</b> 把求和展开：r[i] = h[1]m[i] + h[2]m[i−1] + h[3]m[i−2] + w[i]。第 i 个采样里除了想要的 m[i]，还混进了前两个符号 m[i−1]、m[i−2]，这就是符号间干扰（ISI）。只要 h[2]、h[3] 不全为 0 就存在 ISI。')
  + S(2, '<b>(ii)</b> 按这个求和式，H(Z) = h[1] + h[2]Z⁻¹ + h[3]Z⁻²（h[n] 对应 Z<sup>−(n−1)</sup>）。对照 1 + 0.6Z⁻²：<div class="calc">h[1] = 1，h[3] = 0.6（h[2] = 0）</div>')
  + S(3, '<b>(iii) 滤波后的信号。</b>总响应 C(Z)H(Z) = (1 − 0.6Z⁻²)(1 + 0.6Z⁻²) = 1 − 0.36Z⁻⁴。噪声也经过滤波：w′[i] = w[i] − 0.6w[i−2]。所以<div class="calc">y[i] = m[i] − 0.36 m[i−4] + w′[i]</div>ISI 没有完全消掉，但从 0.6 降到了 0.36，而且被推到 4 个符号之外。m[i] 等概取 ±1，判决规则取符号：<div class="calc">m̂[i] = +1，若 y[i] ≥ 0；m̂[i] = −1，若 y[i] &lt; 0</div>')
  + S(4, '<b>(iv) 误码率。</b>先算滤波后的噪声方差：<div class="calc">σ′² = 0.3 × (1² + 0.6²) = 0.3 × 1.36 = 0.408，σ′ = 0.639</div>设发 m[i] = +1，残余干扰 −0.36m[i−4] 等概为 −0.36 或 +0.36，有用信号到判决门限（0）的距离分别是 0.64 和 1.36：<div class="calc">P<sub>b</sub> = ½Q(0.64/0.639) + ½Q(1.36/0.639) = ½Q(1.00) + ½Q(2.13)</div><div class="calc">= ½(0.158) + ½(0.0166) ≈ 0.087</div>发 −1 时由对称性结果相同。')
  + '<div class="wans">(ii) h[1] = 1，h[3] = 0.6　(iii) y[i] = m[i] − 0.36m[i−4] + w′[i]，按符号判决　(iv) P<sub>b</sub> ≈ 0.087</div>'),

dict(id='y2324s2-q2b', paper=P, q='Q2(b)', marks=12, page='p2', ch='ch7',
 topic='OFDM 子载波数 · 子信道增益 H<sub>k</sub> · 保护间隔与功率损失',
 en='''<p>(b) A wireless system operates with a bandwidth of 1 MHz and implements an OFDM scheme with N sub-carriers. The fading channel has a coherence bandwidth of 500 kHz and a sampled channel impulse response of {1, −0.6, 0.2}.</p>
<p>(i) Determine the value of N if the bandwidth of each OFDM sub-carrier is to be half of the coherence bandwidth.</p>
<p>(ii) Determine the channel gain coefficient values for the N sub-channels.</p>
<p>(iii) Using the simplified formula, T = 1/B, where T is the signal symbol duration and B is the signal bandwidth, determine the total OFDM block duration if a Guard interval of 1 microsecond is added.</p>
<p>(iv) For the question in 2(b) part (iii) above, determine the power loss due to the addition of the guard interval.</p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(i)</b> 每个子载波带宽 = 500/2 = 250 kHz，<div class="calc">N = 1 MHz / 250 kHz = 4</div>')
  + S(2, '<b>(ii)</b> 子信道增益（讲义 Ch7 p.15）H<sub>k</sub> = Σ<sub>i</sub> h<sub>i</sub> e<sup>−j2πik/N</sup>，h = {1, −0.6, 0.2}，N = 4，e<sup>−j2πk/4</sup> 依次是 −j、−1、j、1：<div class="calc">H₁ = 1 − 0.6(−j) + 0.2(−1) = 0.8 + 0.6j　(|H₁| = 1)</div><div class="calc">H₂ = 1 − 0.6(−1) + 0.2(1) = 1.8</div><div class="calc">H₃ = 1 − 0.6(j) + 0.2(−1) = 0.8 − 0.6j　(|H₃| = 1)</div><div class="calc">H₄ = H₀ = 1 − 0.6 + 0.2 = 0.6</div>每个子信道只剩一个复数增益，这正是 OFDM 把频率选择性信道变成 N 个平坦子信道的意思。')
  + S(3, '<b>(iii)</b> 原始符号时长 T<sub>s</sub> = 1/(1 MHz) = 1 µs；一个 OFDM 块 = N T<sub>s</sub> = 4 µs（也等于每个子载波的 1/250 kHz）。加 1 µs 保护间隔：<div class="calc">T<sub>block</sub> = 4 + 1 = 5 µs</div>')
  + S(4, '<b>(iv)</b> 讲义 Ch7 p.18：<div class="calc">功率损失 = 10 log₁₀[(NT<sub>s</sub> + T<sub>G</sub>)/(NT<sub>s</sub>)] = 10 log₁₀(5/4) ≈ 0.97 dB</div>')
  + '<div class="wans">N = 4；H = {0.8+0.6j, 1.8, 0.8−0.6j, 0.6}；块长 5 µs；功率损失 ≈ 0.97 dB</div>'),

dict(id='y2324s2-q3a', paper=P, q='Q3(a)', marks=20, page='A', ch='ch8',
 topic='Erlang B 反推小区半径 · 集群增益 · 120° 扇区化的代价',
 en='''<p>3. (a) A heavily populated small island has a user density of 720 users per km<sup>2</sup> for the service area. The operator A decides to select a cellular system that has a cluster size N<sub>c</sub> = 7 and a total of 399 duplex traffic channels. The system uses a fixed channel assignment, blocked calls cleared scheme and omni-directional antennas at the base station (BS). During the busy hour, on the average, a user generates 0.9 call with a holding time of 90 seconds. The expected Grade of Service (GOS) is given by 1% blocking probability. The service area will be covered by hexagonal cells with radius R. Note: The area of each hexagonal cell is A<sub>ce</sub> = (3√3/2)R<sup>2</sup>. State and justify any necessary assumptions.</p>
<p>(i) Determine the number of channels per cluster and the offered traffic supported by the GOS.</p>
<p>(ii) Determine the number of users m and the offered traffic generated by users in each cell.</p>
<p>(iii) Determine the cell radius R, when the offered traffic generated by users is equal to the offered traffic supported for the given GOS for each cell.</p>
<p>(iv) Determine the trunking gain T<sub>g</sub> of the system.</p>
<p>(v) Suppose the operator A decides to improve the hexagonal cellular design further where one uses the 120-degree sector being deployed in each cell for the BS. For this new design, calculate the new value of R and T<sub>g</sub>. State your observation and comment on the changes to the results from the operator's perspective.</p>
<p class="marks">(20 Marks)</p>''',
 sol=S(1, '<b>假设</b>：均匀固定分配（UFCA），每小区信道数相同；blocked calls cleared → 用 Erlang B；399 条全是话务信道（题目已说 traffic channels）；用户在服务区内均匀分布。')
  + S(2, '<b>(i)</b> 每簇 399 条信道（一个簇用完全部信道），每小区 399/7 = <b>57</b> 条。查 Erlang B 表 M = 57、B = 1%：<div class="calc">A ≈ 44.2 Erlang / 小区</div>')
  + S(3, '<b>(ii)</b> 每用户话务量 A<sub>u</sub> = 0.9 × 90/3600 = 0.0225 E。每小区用户产生的话务量 = m × 0.0225；令它等于小区能支持的 44.2 E：<div class="calc">m = 44.2 / 0.0225 ≈ 1965 用户/小区</div>')
  + S(4, '<b>(iii)</b> 用户密度 720 /km²，所以每小区面积 = 1965/720 = 2.73 km²：<div class="calc">(3√3/2)R² = 2.73 → R² = 2.73/2.598 = 1.051 → R ≈ 1.03 km</div>')
  + S(5, '<b>(iv)</b> 讲义 p.122：集群增益 = 一组信道在给定 GoS 下能服务的用户数 ÷ 信道数：<div class="calc">T<sub>g</sub> = 1965 / 57 ≈ 34.5 用户/信道</div>')
  + S(6, '<b>(v) 120° 扇区。</b>每小区 57 条信道分给 3 个扇区，每扇区 19 条，各自成为独立的信道池。查 Erlang B（M = 19，1%）：A ≈ 11.2 E/扇区，每小区 3 × 11.2 = 33.7 E。<div class="calc">m = 33.7/0.0225 ≈ 1497；面积 = 1497/720 = 2.08 km²；R = √(2.08/2.598) ≈ 0.89 km</div><div class="calc">T<sub>g</sub> = 1497/57 ≈ 26.3</div><b>评论</b>：信道总数不变，但被切成 3 个小池，集群效率下降（57 条一起用能承载 44.2 E，切开只有 33.7 E，少了约 24%），所以每个小区只能覆盖更小的面积，需要更多基站，集群增益从 34.5 降到 26.3。对运营商的好处在于 SIR：只剩 2 个同频干扰源（N = 7、n = 4 时约 24.5 dB，见讲义 p.145）。如果改用更小的簇，扇区化才真正换来容量；在 N 不变的前提下单纯加扇区，只换来干扰改善，付出的是覆盖和集群效率。')
  + '<div class="wans">57 条/小区，A ≈ 44.2 E；m ≈ 1965；R ≈ 1.03 km；T<sub>g</sub> ≈ 34.5；扇区化后 R ≈ 0.89 km，T<sub>g</sub> ≈ 26.3</div>',
 note='Erlang B 的 A 值用公式精确算出（44.22、11.23），和考卷附表读数相同到小数点后一位。'),

dict(id='y2324s2-q3b', paper=P, q='Q3(b)', marks=5, page='A', ch='ch1',
 topic='FDMA / TDMA / CDMA 及系统举例',
 en='''<p>(b) Multiple access schemes are important features in mobile cellular systems as they allow many users to share the limited spectrum simultaneously. There are three basic multiple access schemes used in the 1G-3G mobile cellular systems. Briefly describe each of the multiple access schemes and give an example of an existing mobile cellular system for each scheme.</p>
<p class="marks">(5 Marks)</p>''',
 sol=S(1, '<b>FDMA</b>：把频谱切成许多窄带信道，每个用户在通话期间独占一个频率信道。例：1G 的 <b>AMPS</b>（30 kHz 信道）。')
  + S(2, '<b>TDMA</b>：几个用户共用一个载波，按时隙轮流发送，每人只在自己的时隙里发。例：2G 的 <b>GSM</b>（200 kHz 载波、每帧 8 个时隙）、IS-136。')
  + S(3, '<b>CDMA</b>：所有用户同时占用同一段宽带频谱，每人用不同的扩频码区分，接收端靠码的正交性/低相关性把自己的信号解出来。例：2G 的 <b>IS-95</b>，3G 的 <b>WCDMA</b>、cdma2000。')
  + '<div class="wans">FDMA–AMPS；TDMA–GSM；CDMA–IS-95/WCDMA</div>'),

dict(id='y2324s2-q4ab', paper=P, q='Q4(a)(b)', marks=13, page='B', ch='ch7',
 topic='简化 IoT 架构的两个并行栈 · 为什么要引入雾计算',
 en='''<p>4. (a) For Internet of Things (IoT), the simplified IoT architecture consists of two parallel stacks, i.e., the Management and Compute Stack and Core IoT Functional Stack. Briefly describe the major components in each of the two stacks.</p>
<p class="marks">(7 Marks)</p>
<p>(b) Discuss the necessity to introduce Fog Computing into the simplified IoT architecture.</p>
<p class="marks">(6 Marks)</p>''',
 sol=S(1, '<b>(a) Core IoT Functional Stack（核心功能栈，三层）</b>（讲义 Part B p.86–91）：<br>① <b>"Things" 层</b>：传感器、执行器等智能物体，要适应部署环境的约束（供电、体积、移动性），同时提供所需的数据；<br>② <b>通信网络层</b>：分四个子层——接入网（最后一公里，802.11ah、802.15.4g、LoRa 等）、网关与回传（把一片区域内的设备汇聚到网关，再用长距离链路送回中心）、网络传输（IP、UDP/TCP）、IoT 网络管理（HTTP、WebSocket 等应用协议）；<br>③ <b>应用与分析层</b>：处理收集的数据，既做分析决策，也反过来控制物体。')
  + S(2, '<b>(a) Data Management and Compute Stack（数据管理与计算栈）</b>：决定数据在哪里处理，三个层次对应核心栈：<b>边缘（edge/mist）</b>在传感器或设备本身做最基本的过滤和判断；<b>雾（fog）</b>在靠近终端的网关/路由器等网络设备上做实时处理；<b>云（cloud/数据中心）</b>做集中存储、历史数据和大规模分析。')
  + S(3, '<b>(b) 为什么需要雾计算</b>（讲义 p.103–106）：如果所有数据都直接送云端处理——<br>• 最后一公里带宽很有限，海量数据挤不进去；<br>• 来回时延大，无法做实时响应；<br>• 网关的回传链路常依赖 3G/LTE 甚至卫星，不可靠；<br>• 回传和数据中心要承受的数据量太大，大数据越来越难做实时分析。<br>雾计算把数据处理分散到靠近网络边缘的地方：就近分析能<b>降低时延</b>，<b>卸载核心网</b>大量流量，把<b>敏感数据留在本地</b>；雾节点地理上靠近传感器，具备上下文感知，能形成分布式的边缘控制回路，并在上传前<b>压缩/精简数据</b>。')
  + '<div class="wans">两栈：Things / 通信网络（4 子层）/ 应用与分析；Edge / Fog / Cloud。雾计算解决带宽、时延、回传可靠性和数据量问题</div>'),

dict(id='y2324s2-q4c', paper=P, q='Q4(c)', marks=12, page='A', ch='ch7', hw='HW1 Q2(b)',
 topic='推导 SIR = 1.76 + 20 log N · 反求 n · 最坏情况与 120° 扇区',
 en='''<p>(c) Derive and establish the following relationship between Signal-to-Interference Ratio SIR<sub>dB</sub> and cluster size N<sub>c</sub>.
<span class="eq">SIR<sub>dB</sub> = 1.76 + 20 log<sub>10</sub>(N<sub>c</sub>)</span></p>
<p>(i) Consider the Simplified SIR analysis where SIR = (1/6)Q<sup>n</sup> and Q is the co-channel reuse factor and there are six co-channel interferers in the first tier. You may assume a path loss exponent of n = 4 in your initial evaluation. Determine the SIR<sub>dB</sub> for N<sub>c</sub>=7 and comment on your results.</p>
<p>(ii) If the required minimum SNR<sub>dB</sub> is to be least 20 dB, derive the corresponding value of the path loss exponent n for this case.</p>
<p>(iii) Using the new value of n from part (ii), determine Co-Channel interference SIR for the worst case omnidirectional as shown below.
<span class="eq">SIR = 1 / [2(Q − 1)<sup>−n</sup> + 2Q<sup>−n</sup> + 2(Q + 1)<sup>−n</sup>]</span></p>
<p>(iv) Using the new value of n from part (ii), determine the SIR when using co-channel interference SIR with 120° sectoring. State and comment on your results when compared to part (iii).</p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>推导</b>：只算第一层 6 个同频干扰，手机在小区边缘离本基站 R，6 个干扰基站都近似在距离 D：<div class="calc">S/I = R<sup>−n</sup> / (6D<sup>−n</sup>) = Q<sup>n</sup>/6，　Q = D/R = √(3N)</div>n = 4：S/I = (3N)²/6 = 1.5N²，取 dB：<div class="calc">SIR<sub>dB</sub> = 10 log₁₀ 1.5 + 20 log₁₀ N = 1.76 + 20 log₁₀ N</div>')
  + S(2, '<b>(i)</b> N = 7：1.76 + 20 log 7 = 1.76 + 16.90 = <b>18.66 dB</b>，刚好高于语音约需的 18 dB，所以 7 小区复用最常用。但这个简化模型把 6 个干扰都放在 D，偏乐观。')
  + S(3, '<b>(ii)</b> 要 Q<sup>n</sup>/6 ≥ 100（20 dB），Q = √21 = 4.583：<div class="calc">n = log₁₀ 600 / log₁₀ 4.583 = 2.778/0.661 ≈ 4.20</div>')
  + S(4, '<b>(iii)</b> n = 4.2 代入最坏情况：(Q−1)<sup>4.2</sup> = 212.6，Q<sup>4.2</sup> = 597.9，(Q+1)<sup>4.2</sup> = 1370<div class="calc">SIR = 1/(2/212.6 + 2/597.9 + 2/1370) = 1/0.0142 = 70.4 → 18.5 dB</div>没达到 20 dB：手机在边上时有两个干扰只隔 D − R。')
  + S(5, '<b>(iv)</b> 120° 扇区只剩 2 个干扰：<div class="calc">SIR = 1/(Q<sup>−n</sup> + (Q + 0.7)<sup>−n</sup>) = 1/(1/597.9 + 1/1086) = 385.7 → 25.9 dB</div>比 (iii) 高约 7.4 dB，满足 20 dB 还有约 6 dB 余量。代价是每扇区信道变少、集群效率下降、切换增多。')
  + '<div class="wans">(i) 18.66 dB　(ii) n ≈ 4.2　(iii) 18.5 dB　(iv) 25.9 dB</div>'),
]
