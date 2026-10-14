# EE6129 Semester 2 Examination 2025-2026 (April/May 2026)

P = 'y2526s2'

def S(n, html):
    return f'<div class="wstep"><div class="wn">{n}</div><div class="wtext">{html}</div></div>'

MMM = '''<div class="figwrap"><svg viewBox="0 0 560 150" role="img" aria-label="M/M/m 状态转移图：状态 0 到 m+1，向右的箭头都是 λ，向左的箭头依次是 μ、2μ、…、mμ，状态 m 以后都是 mμ">
<defs><marker id="mmm-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" style="fill:var(--ink)"/></marker></defs>
<g style="stroke:var(--accent);fill:var(--accent-soft)" stroke-width="1.6">
<circle cx="40" cy="75" r="22"/><circle cx="130" cy="75" r="22"/><circle cx="220" cy="75" r="22"/><circle cx="340" cy="75" r="22"/><circle cx="430" cy="75" r="22"/><circle cx="520" cy="75" r="22"/></g>
<g font-size="13" text-anchor="middle" style="fill:var(--ink)"><text x="40" y="80">0</text><text x="130" y="80">1</text><text x="220" y="80">2</text><text x="340" y="80">m−1</text><text x="430" y="80">m</text><text x="520" y="80">m+1</text><text x="280" y="80">⋯</text></g>
<g style="stroke:var(--ink);fill:none" stroke-width="1.3" marker-end="url(#mmm-ar)">
<path d="M58 62 Q85 40 112 62"/><path d="M148 62 Q175 40 202 62"/><path d="M358 62 Q385 40 412 62"/><path d="M448 62 Q475 40 502 62"/>
<path d="M112 88 Q85 110 58 88"/><path d="M202 88 Q175 110 148 88"/><path d="M412 88 Q385 110 358 88"/><path d="M502 88 Q475 110 448 88"/></g>
<g font-size="12" text-anchor="middle" style="fill:var(--ink)"><text x="85" y="38">λ</text><text x="175" y="38">λ</text><text x="385" y="38">λ</text><text x="475" y="38">λ</text>
<text x="85" y="124">μ</text><text x="175" y="124">2μ</text><text x="385" y="124">mμ</text><text x="475" y="124">mμ</text></g>
<text x="280" y="145" font-size="11" text-anchor="middle" style="fill:var(--ink-soft)">到达率恒为 λ；服务率 = 忙着的信道数 × μ，最多 mμ</text>
</svg><div class="cap">M/M/m 的生灭过程。状态 k = 系统里的呼叫数（含排队）。</div></div>'''

QS = [
dict(id='y2526s2-q1a', paper=P, q='Q1(a)', marks=12, page='p2', ch='ch2', quiz=True,
 topic='用 B<sub>c</sub>、B<sub>D</sub>、B<sub>s</sub> 判衰落类型 · LCR 与连续误符号 · 衰落余量',
 en='''<p>1. (a) (i) Explain how coherence bandwidth, doppler spread, and signal bandwidth can be used to determine the type of fading the signal is experiencing.</p>
<p>(ii) A wireless system transmits a signal over a fading channel. The signal has a symbol duration of 5 ms and the average fade duration has been estimated to be 20 ms. For a period of 10 seconds, deep fades have been observed to have occurred 40 times. Assume that whenever a deep fade occurs, the affected symbol will be in error. Determine the Level Crossing Rate and the average number of consecutive symbol errors per second.</p>
<p>(iii) For an outage probability of ε, the channel capacity of a Rayleigh fading channel can be expressed as,
<span class="eq">C<sub>ε</sub> = B × log<sub>2</sub>[1 + γ̄<sub>R</sub> ln(1/(1 − ε))]</span>
where B is the signal bandwidth and γ̄<sub>R</sub> = 25dB is the average signal to noise ratio (SNR). If ε = 0.005, determine the minimum SNR and the Fade Margin compared to transmission over an Additive White Gaussian (AWGN) channel.</p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(i)</b> 讲义 Ch2 p.39 的图，两组比较：<br>• <b>信号带宽 B<sub>s</sub> vs 相干带宽 B<sub>c</sub></b>（多径时延扩展引起）：B<sub>s</sub> &lt; B<sub>c</sub> → <b>平坦衰落</b>，整个信号带宽内衰落相关、频谱失真小；B<sub>s</sub> &gt; B<sub>c</sub> → <b>频率选择性衰落</b>，不同频率衰落不同，时域上产生 ISI。<br>• <b>信号带宽 B<sub>s</sub> vs 多普勒扩展 B<sub>D</sub></b>（移动引起）：B<sub>s</sub> ≫ B<sub>D</sub>（等价于符号时长 ≪ 相干时间 T<sub>c</sub> ≈ 1/B<sub>D</sub>）→ <b>慢衰落</b>，一个符号内信道几乎不变；B<sub>s</sub> 与 B<sub>D</sub> 相当或更小 → <b>快衰落</b>，符号内幅度相位就在变。<br>两组判断组合成四类：平坦慢、平坦快、频选慢、频选快。')
  + S(2, '<b>(ii)</b> LCR = 每秒穿越门限（进入深衰落）的次数：<div class="calc">LCR = 40 次 / 10 s = 4 次/秒</div>每次深衰落平均持续 20 ms，覆盖 20/5 = 4 个符号，即每次产生约 4 个<b>连续</b>错符号：<div class="calc">每秒误符号数 = 4 次/秒 × 4 个/次 = 16 个/秒</div>（错误成串出现，每秒 4 串、每串 4 个。）')
  + S(3, '<b>(iii)</b> γ̄<sub>R</sub> = 25 dB = 316.2。达到 C<sub>ε</sub> 所需的最小（即和 AWGN 等效的）SNR：<div class="calc">γ<sub>min</sub> = γ̄<sub>R</sub> ln(1/(1−ε)) = 316.2 × ln(1/0.995) = 316.2 × 0.005013 = 1.585 → 2.0 dB</div>衰落余量 = 平均 SNR − 等效 AWGN SNR：<div class="calc">FM = 25 − 2.0 = 23.0 dB（= 10 log₁₀[1/0.005013]）</div>')
  + '<div class="wans">(ii) LCR = 4 /s；每秒约 16 个错符号（每次衰落 4 个连续错误）　(iii) γ<sub>min</sub> ≈ 2.0 dB，FM ≈ 23 dB</div>'),

dict(id='y2526s2-q1b1', paper=P, q='Q1(b)(i)', marks='(b) 共 13', page='p2', ch='ch4',
 topic='由输入/输出 SNR 求阵列增益 · 由分集增益求误码率',
 en='''<p>(b) (i) Consider a receiver diversity combining technique. If the average input Signal-to-Noise Ratio (SNR) is 12dB, the average combiner output SNR is 15dB, and the diversity gain is 3.7, determine the gain array and the probability of error.</p>''',
 sol=S(1, '<b>阵列增益</b>（题中的 "gain array"）g = γ̄<sub>Σ</sub>/γ̄（讲义 Ch4 p.27）：<div class="calc">g = 15 − 12 = 3 dB → 10<sup>0.3</sup> ≈ 2</div>')
  + S(2, '<b>误码率</b>：P̄<sub>e</sub> ≈ γ̄<sup>−d</sup>，γ̄ 用合并器<b>输入</b>平均 SNR，12 dB = 15.85：<div class="calc">P̄<sub>e</sub> ≈ 15.85<sup>−3.7</sup> = 10<sup>−1.2×3.7</sup> = 10<sup>−4.44</sup> ≈ 3.6×10⁻⁵</div>')
  + '<div class="wans">阵列增益 ≈ 2（3 dB）；P̄<sub>e</sub> ≈ 3.6×10⁻⁵</div>',
 note='如果误用输出 SNR（15 dB）代入，会得到 2.8×10⁻⁶。讲义和 Practice 4 的官方答案都用输入 SNR。'),

dict(id='y2526s2-q1b2', paper=P, q='Q1(b)(ii)(iii)', marks='(b) 共 13', page='p2', ch='ch5',
 topic='平坦衰落 MIMO 的 y = Hx + v · 2×1 Alamouti 检测信号的均值与方差',
 en='''<p>(ii) A MIMO system uses 4 transmitter antennas and 6 receiver antennas and operates in a flat fading channel. Denote x, y, v and H as the transmitted signal vector, received signal vector, channel noise vector and the channel matrix, respectively. Explain why there is only channel gain for each channel. Express the input-output relationship of the MIMO system with an equation and the channel matrix as a function of the channel gains {h<sub>i,j</sub>}, where h<sub>ij</sub> is the channel gain between the j<sup>th</sup> transmitter antenna and the i<sup>th</sup> receiver antenna.</p>
<p>(iii) In a 2 × 1 MIMO system, the detected signal vector can be expressed as,
<span class="eq">ŝ = s + (1/‖h‖<sup>2</sup>) Gw</span>
where s is the transmitted signal vector, h is the channel gain vector, G is a suitable matrix, and w is a Gaussian noise vector with zero mean. Given that, the variance of Gw is,
<span class="eq">σ<sup>2</sup>‖h‖<sup>2</sup> (1 ; 1)</span>
Derive the expected value and variance of the detected signal.</p>
<p class="marks">(13 Marks)</p>''',
 sol=S(1, '<b>(ii) 为什么每条信道只有一个增益</b>：平坦衰落意味着信号带宽小于相干带宽（时延扩展远小于符号时长），每对发收天线之间的多径在一个符号内叠加成<b>一个复数增益 h<sub>ij</sub></b>，没有可分辨的多个抽头，也就没有 ISI。<br><b>输入输出关系</b>：<div class="calc">y = Hx + v，y、v 为 6×1，x 为 4×1，H 为 6×4</div><div class="calc">H = [h<sub>ij</sub>]，i = 1…6（行，接收天线），j = 1…4（列，发射天线）</div>逐个写：y<sub>i</sub> = Σ<sub>j=1</sub><sup>4</sup> h<sub>ij</sub>x<sub>j</sub> + v<sub>i</sub>，每根接收天线收到 4 根发射天线信号的加权和。')
  + S(2, '<b>(iii) 均值</b>：s 是确定的发送信号，噪声零均值：<div class="calc">E[ŝ] = s + (1/‖h‖²)·G·E[w] = s</div>检测是<b>无偏</b>的。<br><b>方差</b>：常数 s 不贡献方差；随机项乘了常数 1/‖h‖²，方差乘 1/‖h‖⁴：<div class="calc">Var[ŝ] = (1/‖h‖⁴)·σ²‖h‖²·(1, 1)<sup>T</sup> = (σ²/‖h‖²)·(1, 1)<sup>T</sup></div>两个符号的噪声方差都是 σ²/‖h‖² = σ²/(|h₁|² + |h₂|²)：两条路径的增益相加，噪声就被压低，这就是 Alamouti 的分集作用。')
  + '<div class="wans">(ii) y = Hx + v，H 为 6×4 的 [h<sub>ij</sub>]　(iii) E[ŝ] = s；Var = σ²/‖h‖²（每个分量）</div>'),

dict(id='y2526s2-q2a', paper=P, q='Q2(a)', marks=12, page='p2', ch='ch6',
 topic='ISI 离散模型 · Nyquist 无 ISI 准则 · 均衡器输出噪声功率 · 残余 ISI 误码率',
 en='''<p>2. (a) A system transmits message symbols, {m[n]}, over an Additive White Gaussian Noise (AWGN) Inter-Symbol Interference (ISI) channel. The symbol m[n] is equally likely to be +1 or −1, the Gaussian noise, w(n), is a random variable with zero mean and a variance of 0.25, the channel impulse response is denoted as {h[i]}, i = 1, 2, …, L.</p>
<p>(i) Express the received signal, r[n], as a discrete time function of {m[n]}, {w[n]}, and {h[i]}. Explain the Nyquist ISI criterion.</p>
<p>(ii) The receiver uses a linear equalizer to reduce the ISI effect. The equalizer is designed with tap coefficients, {c<sub>j</sub>}, j = 1,2, …, M, where Σ<sub>j=1</sub><sup>M</sup> c<sub>j</sub><sup>2</sup> = 2.56. Determine the noise power at the equalizer output.</p>
<p>(iii) The equalizer output can be derived to be,
<span class="eq">y[n] = m(n) + 0.2m(n − 1) + w′(n)</span>
where w′(n) is the noise at the equalizer output. Using the decision rule of m̂(n) = sgn[y(n)], determine the average probability of error of this system.</p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(i)</b><div class="calc">r[n] = Σ<sub>i=1</sub><sup>L</sup> h[i] m[n − i + 1] + w[n]</div><b>Nyquist 准则</b>（讲义 Ch6 p.12）：采样后 y(nT) = m[n]g<sub>e</sub>(0) + Σ<sub>i≠n</sub> m[i]g<sub>e</sub>(nT − iT) + w(nT)，中间那一项就是 ISI。若等效脉冲在采样时刻满足 g<sub>e</sub>(nT − iT) = 1（n = i）、0（n ≠ i），即每个脉冲在别的符号的采样点上都恰好为零，则传输<b>无 ISI</b>。对上式就是 h[1] = 1、其余 h[i] = 0。')
  + S(2, '<b>(ii)</b> 输出噪声 w′ = Σ c<sub>j</sub>w[n − j + 1]，各 w 独立同方差：<div class="calc">σ′² = σ² Σ c<sub>j</sub>² = 0.25 × 2.56 = 0.64</div>')
  + S(3, '<b>(iii)</b> σ′ = 0.8。发 m(n) = +1，0.2m(n−1) 等概为 ±0.2：<br>• +0.2：均值 1.2 → Q(1.2/0.8) = Q(1.5) = 0.0668<br>• −0.2：均值 0.8 → Q(0.8/0.8) = Q(1) = 0.1587<div class="calc">P<sub>e</sub> = ½(0.1587 + 0.0668) ≈ 0.113</div>')
  + '<div class="wans">(ii) 0.64　(iii) P<sub>e</sub> ≈ 0.113</div>'),

dict(id='y2526s2-q2b', paper=P, q='Q2(b)', marks=13, page='p2', ch='ch7',
 topic='4 子载波的信道增益 · OFDM 即 IDFT · 循环前缀与功率损失',
 en='''<p>(b) An OFDM system uses 4 sub-carriers to transmit a baseband signal that has a symbol duration of 2 μs. The fading channel has a Z-transform of 1 + 0.3Z<sup>−1</sup>. The baseband signal can be organized into N signals {s<sub>k</sub>(t)} to form the transmitted OFDM signal,
<span class="eq">x(t) = (1/√T) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub>(t)e<sup>j2π(k/T)t</sup>,　nT ≤ t ≤ (n + 1)T</span></p>
<p>(i) Determine the channel gain coefficients of the OFDM system.</p>
<p>(ii) Explain why the transformation of the signal, {s<sub>k</sub>(t)}, into the OFDM signal, x(t), can be viewed as an inverse Discrete Fourier transform process.</p>
<p>(iii) If the OFDM system uses a cyclic prefix of 20 μs, determine the OFDM symbol duration and the power loss due to the addition of the cyclic prefix.</p>
<p class="marks">(13 Marks)</p>''',
 sol=S(1, '<b>(i)</b> h = {1, 0.3}，N = 4，H<sub>k</sub> = 1 + 0.3e<sup>−j2πk/4</sup>：<div class="calc">H₁ = 1 − 0.3j；H₂ = 0.7；H₃ = 1 + 0.3j；H₄ (= H₀) = 1.3</div>')
  + S(2, '<b>(ii)</b> 在一个块内按 t = iT/N（i = 0…N−1）采样（讲义 Ch7 p.19）：<div class="calc">x<sub>i</sub> = (1/√T) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub> e<sup>j2πki/N</sup></div>这正是 N 点 IDFT 的形式（只差一个常数比例）：频域的 N 个符号 {s<sub>k</sub>} 被变换成时域的 N 个采样。所以发射端可以用 IFFT 实现，接收端用 FFT 解调，不需要 N 个独立的振荡器。')
  + S(3, '<b>(iii)</b> 4 个基带符号并行，每个 OFDM 块长 NT<sub>s</sub> = 4 × 2 = 8 µs；加 20 µs 循环前缀：<div class="calc">T<sub>OFDM</sub> = 8 + 20 = 28 µs</div><div class="calc">功率损失 = 10 log₁₀(28/8) ≈ 5.44 dB</div>CP 比数据部分还长，损失很大。实际设计会增加 N，让 NT<sub>s</sub> 远大于 CP。')
  + '<div class="wans">(i) {1−0.3j, 0.7, 1+0.3j, 1.3}　(iii) 28 µs，≈ 5.44 dB</div>'),

dict(id='y2526s2-q3a', paper=P, q='Q3(a)', marks=6, page='A', ch='ch6',
 topic='每小区信道 · 簇面积 · 簇复制次数 · 系统容量',
 en='''<p>3. (a) A new operator B is designing the cellular network for a city in South China which has a total of 1071 radio channels available for handling the traffic. Suppose the area of each cell is 6 km<sup>2</sup> and the total area of the entire system is 2100 km<sup>2</sup>. Let the cluster size of the design be 7. Determine the following results.</p>
<p>(i) Number of channels per cell and the total coverage area of each cluster.</p>
<p>(ii) Number of times to replicate this cluster to cover the entire system.</p>
<p>(iii) System capacity for this network.</p>
<p class="marks">(6 Marks)</p>''',
 sol=S(1, '<b>(i)</b> 每小区 1071/7 = <b>153</b> 条；每簇面积 7 × 6 = <b>42 km²</b>。')
  + S(2, '<b>(ii)</b> 复制次数 = 2100/42 = <b>50</b> 次（共 350 个小区）。')
  + S(3, '<b>(iii)</b> 系统容量 = 每簇信道 × 复制次数 = 1071 × 50 = <b>53 550</b> 条信道（也等于 153 × 350）。同一组 1071 条信道被重复用了 50 次，这就是频率复用带来的容量。')
  + '<div class="wans">153 条/小区，42 km²/簇；复制 50 次；系统容量 53 550 条信道</div>'),

dict(id='y2526s2-q3bc', paper=P, q='Q3(b)(c)', marks=19, page='A', ch='ch8',
 topic='Erlang C（5% 延迟）· 每 km² 用户 · 平均通话时长 · M/M/m 状态转移图与 P<sub>k</sub>',
 en='''<p>(b) For the cluster size of 7 in the cellular network in Part 3(a), the operator obtained the survey results that it has traffic load per user of 0.03 Erlangs and an average number of 1.2 calls per hour per user for an Erlang C system, with a probability of delaying a call being 5%. Determine the following results.</p>
<p>(i) Traffic load per cell.</p>
<p>(ii) The number of users per km<sup>2</sup> that can be supported by the cellular system.</p>
<p>(iii) The mean duration of a call in seconds.</p>
<p class="marks">(8 Marks)</p>
<p>(c) The traffic performance of cellular network can be modeled using a simple Markovian queueing model such as M/M/m with m servers representing each channel in the cell.</p>
<p>(i) Draw the state transition diagram for the M/M/m model with the various arrival rates λ<sub>k</sub> and service rates μ<sub>k</sub> given by the following recursive equations,
<span class="eq">λ<sub>k</sub> = λ for k = 0, 1, 2, …;　μ<sub>k</sub> = kμ for k = 1, 2, … m−1;　μ<sub>k</sub> = mμ for k = m, m+1, m+2, …</span>
<span class="eq">k μ P<sub>k</sub> = λ P<sub>k−1</sub> for k ≤ m;　m μ P<sub>k</sub> = λ P<sub>k</sub> for k ≥ m</span>
where P<sub>k</sub> represents the state probability of the system state being at k and system utilization ρ = λ/μ.</p>
<p>(ii) Derive the probability P<sub>k</sub> in terms of m, ρ, and the probability of state zero P<sub>0</sub> for the two cases where k ≤ m and k ≥ m, respectively.</p>
<p class="marks">(11 Marks)</p>''',
 sol=S(1, '<b>(b)(i)</b> 每小区 153 条，查 Erlang C 表（延迟概率 5%）：<div class="calc">A ≈ 132.2 Erlang / 小区</div>（表在 150 与 155 之间线性插值，附录给了插值公式。）')
  + S(2, '<b>(b)(ii)</b> 每小区用户 = 132.2/0.03 ≈ 4408，小区面积 6 km²：<div class="calc">4408/6 ≈ 735 用户/km²</div>')
  + S(3, '<b>(b)(iii)</b> H = A<sub>u</sub>/λ<sub>u</sub> = 0.03/1.2 小时 = 0.025 h = <b>90 s</b>。')
  + S(4, '<b>(c)(i) 状态转移图</b>：状态 k = 系统中的呼叫数。向右（k → k+1）的速率都是 λ；向左（k → k−1）的速率是 kμ（k ≤ m，k 条信道都在服务），k ≥ m 后封顶为 mμ（只有 m 条信道，其余在排队）。' + MMM)
  + S(5, '<b>(c)(ii) k ≤ m</b>：由 kμP<sub>k</sub> = λP<sub>k−1</sub> 得 P<sub>k</sub> = (ρ/k)P<sub>k−1</sub>，一路递推到 P₀：<div class="calc">P<sub>k</sub> = P₀ · ρ<sup>k</sup>/k!，　k ≤ m</div><b>k ≥ m</b>：mμP<sub>k</sub> = λP<sub>k−1</sub>（题中写成 λP<sub>k</sub> 是笔误，讲义 p.106 是 P<sub>k−1</sub>），即 P<sub>k</sub> = (ρ/m)P<sub>k−1</sub>，从 P<sub>m</sub> = P₀ρ<sup>m</sup>/m! 出发再乘 (k − m) 次 ρ/m：<div class="calc">P<sub>k</sub> = P₀ · ρ<sup>k</sup>/(m! · m<sup>k−m</sup>)，　k ≥ m</div>两式在 k = m 处一致。P₀ 由 ΣP<sub>k</sub> = 1 求出（要求 ρ/m &lt; 1），再由此得到 Erlang C 公式。')
  + '<div class="wans">(b) ≈ 132.2 E/小区；≈ 735 用户/km²；90 s　(c) P<sub>k</sub> = P₀ρ<sup>k</sup>/k!（k ≤ m），P₀ρ<sup>k</sup>/(m!m<sup>k−m</sup>)（k ≥ m）</div>'),

dict(id='y2526s2-q4a', paper=P, q='Q4(a)', marks=4, page='A', ch='ch10',
 topic='硬切换与软切换及各自使用的系统',
 en='''<p>4. (a) For terrestrial cellular systems there are two types of handovers. Describe the basic mechanisms of these two handovers and identify the types of cellular systems that deploy each of these two handovers respectively.</p>
<p class="marks">(4 Marks)</p>''',
 sol=S(1, '<b>硬切换（break before make，先断后连）</b>（讲义 Part A p.154）：先释放与旧基站的信道，再建立与新基站的信道。实现简单，但有短暂中断，可能掉话。用于 <b>FDMA/TDMA 系统</b>，如 GSM、IS-136（以及 AMPS）。')
  + S(2, '<b>软切换（make before break，先连后断）</b>（p.155）：先和新基站建立信道，新旧两条同时使用，确认后再断开旧的。边界处有分集增益，通话不中断。用于 <b>CDMA 系统</b>，如 IS-95、WCDMA、cdma2000。')
  + '<div class="wans">硬切换：先断后连，GSM/IS-136；软切换：先连后断，IS-95/WCDMA/cdma2000</div>'),

dict(id='y2526s2-q4b', paper=P, q='Q4(b)', marks=8, page='C', ch='ch6',
 topic='MEO/LEO 卫星系统的四种切换',
 en='''<p>(b) In a satellite system with Medium Earth Orbit (MEO) or Low Earth Orbit (LEO) satellites, there could also be handovers in the system if the satellite acts as a base station. Briefly describe the 4 different types of handovers that can occur in this type of satellite system.</p>
<p class="marks">(8 Marks)</p>''',
 sol=S(1, '<b>星内切换（Intra-satellite）</b>（讲义 Part C p.40）：用户在同一颗卫星的覆盖区内，从一个扇区（点波束）移到另一个扇区。')
  + S(2, '<b>星间切换（Inter-satellite）</b>：用户从一颗卫星的覆盖区移到另一颗卫星的覆盖区，或者卫星自己飞走了。LEO 卫星每次只可见 15–20 分钟，这种切换很频繁。')
  + S(3, '<b>网关切换（Gateway）</b>：卫星移动后离开了当前连接的地面网关，需要换一个网关。')
  + S(4, '<b>系统间切换（Inter-system）</b>：卫星系统和地面蜂窝系统之间，根据信号强度和 QoS 进行的<b>垂直切换</b>。')
  + '<div class="wans">星内、星间、网关、系统间（垂直）切换</div>'),

dict(id='y2526s2-q4c', paper=P, q='Q4(c)', marks=5, page='B', ch='ch5',
 topic='传感器网络的通信架构：节点多跳 → sink → 任务管理节点',
 en='''<p>(c) A sensor network is composed of many sensor nodes which are densely distributed to sense the environment. Briefly describe the communication architecture in the sensor networks to support the network operations. Describe briefly the communication architecture and show how the sensor nodes can relay the information back to the manager of the sensor network.</p>
<p class="marks">(5 Marks)</p>''',
 sol=S(1, '<b>架构</b>（讲义 Part B p.56–57）：传感器节点散布在传感区域里，每个节点都能采集数据并把数据路由回<b>汇聚节点（sink）</b>。数据以<b>多跳、无基础设施</b>的方式，一个节点接一个节点地转发到 sink；sink 再经<b>互联网或卫星</b>与<b>任务管理节点（task manager）</b>通信，管理者在那里获取数据、下发任务。')
  + S(2, '<b>设计影响因素</b>：可靠性、可扩展性、生产成本、工作环境、网络拓扑、硬件约束、传输介质和功耗。协议栈分为物理层、数据链路层、网络层、传输层、应用层，外加功耗管理、移动性管理、任务管理三个平面（p.59）。')
  + S(3, '<b>示意</b>：传感器 A → 传感器 B → 传感器 C → … → Sink → Internet/卫星 → 任务管理节点（用户）。')
  + '<div class="wans">传感器节点多跳转发 → Sink → Internet/卫星 → Task manager</div>'),

dict(id='y2526s2-q4d', paper=P, q='Q4(d)', marks=8, page='B', ch='ch7',
 topic='IoT 通信网络层的四个子层（同 2024-25 Q4(b)）',
 en='''<p>(d) In the core Internet of Things (IoT) functional stack, the communication network layer is structured with four sublayers. Describe the features of each of the sublayers.</p>
<p class="marks">(8 Marks)</p>''',
 sol=S(1, '和 2024-25 Q4(b) 是同一道题，答案见那里。四个子层：接入网（最后一公里无线接入：802.11ah、802.15.4g、LoRa）、网关与回传（汇聚后用长距离介质送往中心）、网络传输（IP + UDP/TCP，开放标准、可扩展、安全）、IoT 网络管理（HTTP、WebSocket 等应用协议，负责物体与头端应用的数据交换）。')
  + '<div class="wans">Access network / Gateways &amp; backhaul / Network transport / IoT network management</div>',
 same='y2425s2-q4b'),
]
