# EE6129 Semester 1 Examination 2025-2026 (November/December 2025)

P = 'y2526s1'

def S(n, html):
    return f'<div class="wstep"><div class="wn">{n}</div><div class="wtext">{html}</div></div>'

CONST = '''<div class="figwrap"><svg viewBox="0 0 400 110" role="img" aria-label="BPSK 星座图：一维实轴上两个点 −1 和 +1，相距 2">
<line x1="30" y1="55" x2="370" y2="55" style="stroke:var(--ink)" stroke-width="1.4"/>
<line x1="200" y1="45" x2="200" y2="65" style="stroke:var(--ink-faint)"/>
<circle cx="110" cy="55" r="7" style="fill:var(--accent)"/><circle cx="290" cy="55" r="7" style="fill:var(--accent)"/>
<text x="98" y="84" font-size="13" style="fill:var(--ink)">s = −1</text><text x="278" y="84" font-size="13" style="fill:var(--ink)">s = +1</text>
<text x="194" y="84" font-size="12" style="fill:var(--ink-soft)">0</text>
<line x1="110" y1="28" x2="290" y2="28" style="stroke:var(--gold)" stroke-width="1.4"/>
<text x="176" y="22" font-size="12" style="fill:var(--gold)">距离 = 2</text>
<text x="350" y="46" font-size="12" style="fill:var(--ink-soft)">实轴</text>
</svg><div class="cap">两个信号点都在一条直线（实轴）上，所以星座是一维的。</div></div>'''

QS = [
dict(id='y2526s1-q1a', paper=P, q='Q1(a)', marks=12, page='p2', ch='ch3',
 topic='二进制 AWGN：星座维数与距离 · 条件高斯分布 · 误码率 Q(2)',
 en='''<p>1. (a) A binary signal is transmitted over an Additive White Gaussian Noise (AWGN) channel, where the Gaussian noise has a zero mean and a variance of 0.25. The received signal can be expressed as, y = s + w, where s is a transmitted symbol which is equally likely to be +1 or −1, and w is the AWGN component. Note: The probability density function of a Gaussian random variable x with mean μ, variance σ<sup>2</sup> is,
<span class="eq">p(x) = (1/√(2πσ<sup>2</sup>)) e<sup>−(x−μ)<sup>2</sup>/(2σ<sup>2</sup>)</sup></span></p>
<p>(i) Sketch the signal constellation of s. Find the dimension of this constellation and the distance between the two possible signal vectors.</p>
<p>(ii) y can be shown to be a random variable with a Gaussian distribution. Determine the expected values and variances of y when s = 1 and when s = −1. Hence, derive the corresponding probability density function of y.</p>
<p>(iii) If the decision rule is, ŝ = +1 when y &gt; 0 and ŝ = −1 when y ≤ 0, determine the bit error probability of this system. Note: The Q-function of z is,
<span class="eq">Q(z) = ∫<sub>z</sub><sup>+∞</sup> (1/√(2π)) e<sup>−x<sup>2</sup>/2</sup> dx</span></p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(i)</b> 两个点 +1 和 −1 都在实轴上：<b>维数 = 1</b>，两点距离 = |1 − (−1)| = <b>2</b>。' + CONST)
  + S(2, '<b>(ii)</b> s 给定时 y = s + w 只是把零均值噪声平移了 s：<div class="calc">s = +1：E[y] = 1，Var[y] = 0.25；　s = −1：E[y] = −1，Var[y] = 0.25</div>（常数加随机变量，均值加上常数、方差不变，Ch1b 的性质。）条件概率密度：<div class="calc">p(y | s = ±1) = (1/√(0.5π)) e<sup>−(y ∓ 1)²/0.5</sup></div>两者等概，y 的（无条件）概率密度是两个高斯的平均：<div class="calc">p(y) = ½ · (1/√(0.5π)) [e<sup>−(y−1)²/0.5</sup> + e<sup>−(y+1)²/0.5</sup>]</div>')
  + S(3, '<b>(iii)</b> 发 +1、判成 −1 的条件是 y ≤ 0，即噪声 w ≤ −1。σ = 0.5：<div class="calc">P(y ≤ 0 | s = +1) = P(w ≤ −1) = Q(1/0.5) = Q(2) ≈ 0.0228</div>由对称性，发 −1 出错的概率也是 Q(2)，所以 <b>P<sub>b</sub> = Q(2) ≈ 0.023</b>。一般式：P<sub>b</sub> = Q(d/(2σ))，d = 2 是 (i) 求的距离。')
  + '<div class="wans">(i) 1 维，距离 2　(ii) 均值 ±1，方差 0.25　(iii) P<sub>b</sub> = Q(2) ≈ 0.0228</div>',
 note='这道题 (ii) 用到的高斯随机变量性质属于 Ch1b（概率复习），也是 Quiz 范围内的知识。'),

dict(id='y2526s1-q1b1', paper=P, q='Q1(b)(i)', marks='(b) 共 13', page='p2', ch='ch4',
 topic='两支路 MRC：平均输入/输出 SNR · 由误码率求分集增益',
 en='''<p>(b) Mobile radio systems operating with multiple antennas (or branches) at the transmitter and/or receiver can provide diversity in a fading environment.</p>
<p>(i) Consider a system that uses a 2-branch receiver combining technique. The Signal to Noise Ratios (SNR) at the input of the receiver, γ<sub>1</sub> and γ<sub>2</sub>, have the following values and probability distributions.
<span class="eq">γ<sub>i</sub> = 11 dB with a probability of 0.2;　12 dB with a probability of 0.5;　13 dB with a probability of 0.3;　i = 1,2</span>
Determine the average receiver input SNR, the average receiver output SNR if the receiver uses the Maximal Ratio Combing (MRC) technique, and the diversity gain of this system at a probability of error of 2 × 10<sup>−4</sup>.</p>''',
 sol=S(1, 'dB 化线性：11 dB → 12.59，12 dB → 15.85，13 dB → 19.95。<div class="calc">γ̄ = 0.2 × 12.59 + 0.5 × 15.85 + 0.3 × 19.95 = 16.43 → 12.16 dB</div>')
  + S(2, '<b>MRC 输出 SNR = 各支路 SNR 之和</b>，所以平均值也相加：<div class="calc">γ̄<sub>Σ</sub> = 2 × 16.43 = 32.86 → 15.17 dB</div>阵列增益 g = γ̄<sub>Σ</sub>/γ̄ = 2（3 dB）。')
  + S(3, '<b>分集增益</b>（讲义 Ch4 p.27）：P̄<sub>e</sub> ≈ γ̄<sup>−d</sup>，γ̄ 是<b>合并器输入</b>的平均 SNR：<div class="calc">d ≈ −log₁₀ P̄<sub>e</sub> / log₁₀ γ̄ = −log₁₀(2×10⁻⁴) / log₁₀(16.43) = 3.70/1.216 ≈ 3.0</div>Practice 4 Q2 的官方答案也是用输入 SNR 算 d（γ̄ = 10，P̄<sub>s</sub> = 7.6×10⁻⁹ → d = 8.1）。')
  + '<div class="wans">输入 ≈ 16.4（12.2 dB）；MRC 输出 ≈ 32.9（15.2 dB）；d ≈ 3.0</div>',
 note='d ≈ 3 比支路数 2 还大，因为讲义的 d 是用"高 SNR 近似"由单个误码率点反算的，不是严格的渐近斜率。考试按讲义公式算即可。'),

dict(id='y2526s1-q1b2', paper=P, q='Q1(b)(ii)(iii)', marks='(b) 共 13', page='p2', ch='ch5',
 topic='SIMO 如何获得分集 · MIMO 容量 = 并行信道容量之和',
 en='''<p>(ii) The input-output relationship of a MIMO system is given below,
<span class="eq">y<sub>1</sub> = (h<sub>1</sub> × s) + v<sub>1</sub>;　y<sub>2</sub> = (h<sub>2</sub> × s) + v<sub>2</sub></span>
where s is the transmitted symbol, h<sub>1</sub>, h<sub>2</sub> are the channel gains, v<sub>1</sub>, v<sub>2</sub> are the Additive White Gaussian Noise (AWGN), and y<sub>1</sub>, y<sub>2</sub> are the received signals. Explain why this can be a Single-Input Multiple-Output (SIMO) system. Using the input-output relationship, explain conceptually how such systems can achieve diversity.</p>
<p>(iii) The channel capacity of a MIMO system can be simplified to,
<span class="eq">B log<sub>2</sub> det{I + (1/σ<sup>2</sup>)Λ}</span>
where B is the bandwidth, det{•} is the Determinant of {•}, I is the Identity matrix, σ<sup>2</sup> is the noise variance, and Λ is a diagonal matrix whose diagonal elements are some eigenvalues. Simplify this expression further and use it to explain that the channel capacity of a MIMO system is equal to the sum of the channel capacities of a set of parallel channels.</p>
<p class="marks">(13 Marks)</p>''',
 sol=S(1, '<b>(ii) 为什么是 SIMO</b>：只有一个发送符号 s（一根发射天线），却有两个接收信号 y₁、y₂（两根接收天线），各经过不同的信道增益 h₁、h₂ 和独立噪声，所以是单输入多输出（1 × 2）。<br><b>怎么得到分集</b>：同一个 s 经过两条（若天线间距足够则）独立衰落的路径到达。h₁ 深衰落时 h₂ 大概率不衰落，两条同时深衰落的概率是各自概率的乘积，小得多。接收端把两路合并，例如 MRC：z = h₁*y₁ + h₂*y₂ = (|h₁|² + |h₂|²)s + 噪声，有效增益是两路之和，分集阶数为 2。')
  + S(2, '<b>(iii)</b> Λ 是对角阵 diag(λ₁, …, λ<sub>K</sub>)，所以 I + Λ/σ² 也是对角阵，行列式就是对角元素的乘积：<div class="calc">det{I + Λ/σ²} = Π<sub>i</sub>(1 + λ<sub>i</sub>/σ²)</div>对数把乘积变成求和：<div class="calc">C = B log₂ Π(1 + λ<sub>i</sub>/σ²) = Σ<sub>i=1</sub><sup>K</sup> B log₂(1 + λ<sub>i</sub>/σ²)</div>每一项正是一个 SNR 为 λ<sub>i</sub>/σ² 的 SISO 信道的香农容量。所以 MIMO 信道（经 SVD 分解后）等价于 K = rank(H) ≤ min(N, M) 个互不干扰的并行子信道，总容量是它们之和；这也是 MIMO 容量随 min(N, M) 线性增长的原因。')
  + '<div class="wans">(ii) 1 发 2 收；两条独立衰落路径合并 → 分集阶数 2　(iii) C = Σ B log₂(1 + λ<sub>i</sub>/σ²)</div>'),

dict(id='y2526s1-q2a', paper=P, q='Q2(a)', marks=13, page='p2', ch='ch6',
 topic='ISI 信道长度 L · 不均衡直接判决的误码率 · 均衡器放大噪声',
 en='''<p>2. (a) A mobile radio system transmits message symbols, {m[n]} over an AWGN Inter-Symbol Interference (ISI) channel. The received signal can be expressed as,
<span class="eq">r[n] = Σ<sub>i=1</sub><sup>L</sup> m[n − i + 1]h[i] + w(n)</span>
where m[n] is equally likely to be +1 or −1, {w(n)} is a Gaussian random variable with zero mean and a variance of 0.36, and the ISI channel, {h[i]}, has a Z-transform of H(Z) = 1 + 0.3Z<sup>−1</sup>.</p>
<p>(i) Determine the value of L in the expression for r[n] above.</p>
<p>(ii) r[n] can be used as a decision variable to detect m[n]. Determine the average probability of error if the decision rule is m̂[n] = sgn[r[n]].</p>
<p>(iii) The receiver uses an equalizer that has a Z-transform of C(Z) = 1 − c<sub>1</sub>Z<sup>−1</sup> + c<sub>2</sub>Z<sup>−2</sup>, where c<sub>1</sub> &gt; 0 and c<sub>2</sub> &gt; 0. Show that there is an increase in the noise variance at the equalizer output.</p>
<p class="marks">(13 Marks)</p>''',
 sol=S(1, '<b>(i)</b> H(Z) = 1 + 0.3Z⁻¹ 有两项：h[1] = 1，h[2] = 0.3，所以 <b>L = 2</b>：r[n] = m[n] + 0.3m[n−1] + w(n)。')
  + S(2, '<b>(ii)</b> σ = √0.36 = 0.6。发 m[n] = +1，干扰 0.3m[n−1] 等概为 ±0.3：<br>• m[n−1] = +1：均值 1.3 → 出错概率 Q(1.3/0.6) = Q(2.17) = 0.0151<br>• m[n−1] = −1：均值 0.7 → Q(0.7/0.6) = Q(1.17) = 0.1217<div class="calc">P<sub>e</sub> = ½(0.1217 + 0.0151) ≈ 0.068</div>对比没有 ISI 时 Q(1/0.6) = Q(1.67) ≈ 0.048，ISI 让误码率变差。')
  + S(3, '<b>(iii)</b> 噪声经过均衡器：w′(n) = w(n) − c₁w(n−1) + c₂w(n−2)。各个 w 独立、方差都是 σ²，独立变量之和的方差 = 方差之和（系数要平方）：<div class="calc">Var[w′] = σ²(1 + c₁² + c₂²) = 0.36(1 + c₁² + c₂²) &gt; 0.36</div>只要 c₁、c₂ 不全为 0，输出噪声方差就比输入大，这就是线性均衡器的"噪声增强"（讲义 Ch6 p.41）。')
  + '<div class="wans">(i) L = 2　(ii) P<sub>e</sub> ≈ 0.068　(iii) σ′² = 0.36(1 + c₁² + c₂²) &gt; 0.36</div>'),

dict(id='y2526s1-q2b', paper=P, q='Q2(b)', marks=12, page='p2', ch='ch7',
 topic='平坦衰落所需最少子载波 · 有效速率 · 相关器输出 = s<sub>n</sub>',
 en='''<p>(b) An 4-QAM OFDM system transmits data with an available bandwidth of 500 kHz. The coherence bandwidth and maximum delay spread of the channel have been measured to be 30 kHz and 10 microseconds (μs) respectively. Note: For this question, you may assume T = 1/B, where T is signal duration and B is the corresponding bandwidth.</p>
<p>(i) Determine the minimum number of carriers the OFDM system should use for its signal to experience flat fading.</p>
<p>(ii) If the OFDM system uses N = 50 carriers, determine the effective transmission bit rate of this system.</p>
<p>(iii) The received OFDM signal can be expressed as,
<span class="eq">r(t) = x(t) + w(t) = (1/√T<sub>OFDM</sub>) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub>(t)e<sup>j2π(k/T<sub>OFDM</sub>)t</sup> + w(t)</span>
where s<sub>k</sub>(t) is the transmitted signal with the k<sup>th</sup> carrier and w(t) is an Additive White Gaussian Noise. At the receiver, r(t) is passed through a set of correlators. Show that at the output of the n<sup>th</sup> correlator, the signal x(t) is simplified to s<sub>n</sub>(t).</p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(i)</b> 每个子载波带宽 500/N 要小于相干带宽 30 kHz：<div class="calc">N &gt; 500/30 = 16.7 → N<sub>min</sub> = 17</div>')
  + S(2, '<b>(ii)</b> N = 50：子载波带宽 10 kHz → 子载波符号时长 T = 1/10 kHz = 100 µs。为消除时延扩展的 ISI 要加保护间隔 T<sub>G</sub> ≥ 10 µs，块长 110 µs。每个 OFDM 块携带 50 × 2 = 100 bit（4-QAM 每符号 2 bit）：<div class="calc">R<sub>eff</sub> = 100 bit / 110 µs ≈ 909 kbit/s</div>不计保护间隔的原始速率是 100/100 µs = 1 Mbit/s；"effective" 指扣掉保护间隔后的速率。')
  + S(3, '<b>(iii)</b> 第 n 个相关器把 r(t) 乘以 (1/√T)e<sup>−j2πnt/T</sup> 再在一个符号期 T 内积分（T = T<sub>OFDM</sub>，s<sub>k</sub> 在符号期内为常数）：<div class="calc">(1/√T)∫₀<sup>T</sup> x(t)e<sup>−j2πnt/T</sup>dt = (1/T) Σ<sub>k</sub> s<sub>k</sub> ∫₀<sup>T</sup> e<sup>j2π(k−n)t/T</sup>dt</div>当 k = n，被积函数是 1，积分 = T；当 k ≠ n，积分的是整数个完整周期的复指数，结果为 0（子载波正交）：<div class="calc">∫₀<sup>T</sup> e<sup>j2π(k−n)t/T</sup>dt = T·δ[k − n] → 输出 = (1/T)·s<sub>n</sub>·T = s<sub>n</sub>(t)</div>噪声项另算，所以信号部分只剩 s<sub>n</sub>，其他子载波对它没有干扰。')
  + '<div class="wans">(i) N ≥ 17　(ii) ≈ 909 kbit/s（不计保护间隔 1 Mbit/s）　(iii) 子载波正交 → 输出 s<sub>n</sub></div>'),

dict(id='y2526s1-q3a', paper=P, q='Q3(a)', marks=12, page='A', ch='ch4',
 topic='小区数 · 总信道数（扣保护带）· 小区容量 · 频谱效率 channels/MHz/km²',
 en='''<p>3. (a) A metropolis city with a total area of 1500 km<sup>2</sup> is covered by a hexagonal cellular system with a cluster size of 9. Suppose that each cell has a radius R of 2 km and the cellular system is allocated 25 MHz of spectrum, with a full-duplex channel bandwidth of 30 kHz and a total 40 kHz guard bands. The system uses frequency division multiple access (FDMA) with 18 control channels. Determine:</p>
<p>(i) the number of cells in the service area;</p>
<p>(ii) the number of channels without frequency reuse;</p>
<p>(iii) The cell capacity; and</p>
<p>(iv) The system spectral efficiency in the units of channels/ MHz / km<sup>2</sup>.</p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(i)</b> 小区面积 = (3√3/2) × 2² = 10.39 km²：<div class="calc">小区数 = 1500 / 10.39 = 144.3 → 约 145 个（向上取整才能覆盖全区）</div>')
  + S(2, '<b>(ii)</b> 扣掉保护带后可用 25 000 − 40 = 24 960 kHz：<div class="calc">信道数 = 24 960 / 30 = 832 条（全双工信道）</div>这就是不复用时整个系统能用的信道数。')
  + S(3, '<b>(iii) 小区容量</b>：832 条里 18 条是控制信道，话务信道 814 条，分给簇内 9 个小区：<div class="calc">814 / 9 = 90.4 → 每小区 90 条话务信道</div>（若把控制信道也算进来是 832/9 ≈ 92 条。）')
  + S(4, '<b>(iv) 频谱效率</b>（讲义 Part A p.40）η = (B<sub>w</sub>/B<sub>c</sub>)/(B<sub>w</sub>·A<sub>c</sub>·N) = 1/(B<sub>c</sub>·A<sub>c</sub>·N)：<div class="calc">η = 1/(0.03 MHz × 10.39 km² × 9) ≈ 0.356 channels/MHz/km²</div>也可以从定义直接算：系统总信道数 = (832/9) × 144.3 ≈ 13 340，除以 25 MHz × 1500 km²，同样约 0.356。')
  + '<div class="wans">(i) ≈ 145 个小区　(ii) 832 条　(iii) 90 条话务信道/小区　(iv) ≈ 0.36 channels/MHz/km²</div>'),

dict(id='y2526s1-q3b', paper=P, q='Q3(b)', marks=9, page='A', ch='ch8',
 topic='Erlang C（5% 延迟概率）· 每 km² 用户数 · 平均通话时长',
 en='''<p>(b) A cellular system has a cluster size of 9. In the system, there are 1001 radio channels for traffic. The area of each cell is 4 km<sup>2</sup>. The entire service area of the system is 3500 km<sup>2</sup>. Given that the traffic load per user is 0.03 Erlangs and the average number of calls per hour per user is 1.5. For an Erlang C system with a blocking probability of 5%, determine the following:</p>
<p>(i) The traffic load per cell;</p>
<p>(ii) The number of users per km<sup>2</sup>; and</p>
<p>(iii) The average call duration of a call.</p>
<p class="marks">(9 Marks)</p>''',
 sol=S(1, '<b>(i)</b> 每小区信道 = 1001/9 = 111.2 → 111 条。查 Erlang C 表（M = 111，延迟概率 5%）：<div class="calc">A ≈ 93.4 Erlang / 小区</div>（Erlang C 表在 100 条以上按 5 条一档，可在 110 与 115 之间线性插值，附录给了插值公式。）')
  + S(2, '<b>(ii)</b> 每小区用户 = 93.4/0.03 ≈ 3114，每 km²：<div class="calc">3114 / 4 ≈ 779 用户/km²</div>')
  + S(3, '<b>(iii)</b> A<sub>u</sub> = λ<sub>u</sub> × H → H = 0.03 / 1.5 = 0.02 小时 = <b>72 秒</b>。')
  + '<div class="wans">(i) ≈ 93.4 E　(ii) ≈ 779 用户/km²　(iii) 72 s</div>',
 note='3500 km² 这个条件在三小问里都用不到（可以用来算总小区数 875 个）。'),

dict(id='y2526s1-q3c', paper=P, q='Q3(c)', marks=4, page='A', ch='ch7',
 topic='固定信道分配 FCA 与动态信道分配 DCA',
 en='''<p>(c) Briefly describe the concept of fixed and dynamic channel assignment for a cellular system.</p>
<p class="marks">(4 Marks)</p>''',
 sol=S(1, '<b>固定信道分配（FCA）</b>（讲义 Part A p.92–94）：每个小区预先分配一组固定的信道，小区内的呼叫只能用本小区空闲的信道，用完就阻塞，哪怕邻区有空闲信道。可均匀分配（UFCA），也可按业务量不均匀分配。简单，但对业务量的变化适应性差。')
  + S(2, '<b>动态信道分配（DCA）</b>（p.95–96）：信道不永久分给小区；新呼叫到来时，任何基站都可以按某种算法使用任一信道，只要不违反同频干扰约束（同一信道不能在复用距离 D 以内重复使用）。算法依据未来阻塞预测、复用距离和其他代价函数。信道借用是一种 DCA。业务量大的小区可以用更多信道，灵活、阻塞率低，但需要集中控制和更多计算。')
  + '<div class="wans">FCA：固定分组、简单但不灵活；DCA：按需分配、受复用距离约束、灵活但复杂</div>'),

dict(id='y2526s1-q4a', paper=P, q='Q4(a)', marks=8, page='B', ch='ch3',
 topic='接入 AP 的过程：扫描 → 认证 → 关联',
 en='''<p>4. (a) An Access Point (AP) is a portal of a Wireless Local Area Network (WLAN), which can be used to connect to the Internet. When a user tries to connect to an AP, there will be a connection establishment procedure. Describe the connection establishment process and explain the function of the authentication process.</p>
<p class="marks">(8 Marks)</p>''',
 sol=S(1, '<b>① 获取同步信息（扫描）</b>（讲义 Part B p.31–32）：节点要加入已有的 BSS，先要从 AP 获得同步信息。两种方式：<b>被动扫描</b>，等待 AP 周期性广播的信标帧（Beacon）；<b>主动扫描</b>，发送探测请求帧（Probe Request），等待 AP 回复探测响应帧（Probe Response）。')
  + S(2, '<b>② 认证（Authentication）</b>：找到 AP 后，节点和 AP 交换信息，<b>双方证明自己知道约定的密码</b>。作用：确认对方是合法用户/合法 AP，防止未授权设备接入网络。')
  + S(3, '<b>③ 关联（Association）</b>：认证通过后，交换节点和 BSS 的能力信息，并把节点当前的位置告诉分布式系统（DSS，所有 AP 的集合），以便数据能正确地送到这个节点。')
  + S(4, '只有关联完成后，节点才能收发数据帧。')
  + '<div class="wans">扫描（被动/主动）→ 认证（互证密码，防止非法接入）→ 关联（交换能力、登记位置）→ 开始传数据</div>'),

dict(id='y2526s1-q4bc', paper=P, q='Q4(b)(c)', marks=17, page='B', ch='ch7',
 topic='IoT 的五个难点 · 雾计算的关键特征',
 en='''<p>(b) The Internet of Things (IoT) is the technique that connects all unconnected objects. Discuss five of the potential difficulties and briefly describe each of them in the context of the development of IoT.</p>
<p class="marks">(10 Marks)</p>
<p>(c) An outstanding technique that processes data generated by IoT sensors is fog computing. Discuss the key features of fog computing.</p>
<p class="marks">(7 Marks)</p>''',
 sol=S(1, '<b>(b) 五个难点</b>（讲义 Part B p.82–83）：<br>① <b>可扩展性（Scalability）</b>：设备数量可达数百万，系统如何支撑是关键；网络层可用 IPv6 分配海量地址。<br>② <b>安全（Security）</b>：联网"物"越多，攻击面越大；一个设备被攻破后可以成为攻击其他设备和系统的跳板。<br>③ <b>隐私（Privacy）</b>：传感器收集的大量数据与具体个人及其活动相关，可能包含敏感信息和凭证，如何保护、与谁共享是关键问题。<br>④ <b>大数据与分析（Big data and analytics）</b>：海量传感器产生的数据洪流，要及时处理来自不同来源、不同格式的大量数据才能得到有价值的信息。<br>⑤ <b>互操作性（Interoperability）</b>：各种协议和架构争夺市场和标准，有的私有、有的开放，导致不同设备/网络难以互通。')
  + S(2, '<b>(c) 雾计算的关键特征</b>（讲义 p.109）：<br>• <b>上下文位置感知与低时延</b>：雾节点尽可能靠近 IoT 终端，就近做分布式计算；<br>• <b>地理分布</b>：雾节点服务的业务需要广泛分布式部署；<br>• <b>部署在大量 IoT 终端附近</b>；<br>• <b>雾节点与终端之间用无线通信</b>，便于连接大量终端、实现可扩展；<br>• <b>用于实时交互</b>：在雾节点预处理数据，上层应用只需批处理数据子集。<br>好处：降低时延、减轻核心网流量、敏感数据留在本地、提供分布式边缘控制回路、减少需要上传的数据量。')
  + '<div class="wans">(b) 可扩展性、安全、隐私、大数据分析、互操作性　(c) 低时延/位置感知、地理分布、靠近终端、无线接入、实时交互</div>'),
]
