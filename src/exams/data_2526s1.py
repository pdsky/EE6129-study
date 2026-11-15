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
 sol=S(1, '<b>(i) 星座、维数、距离</b>：s 只取 +1 和 −1 两个实数，都在同一条实轴上，只要一个基函数（一个坐标轴）就能表示，所以<b>维数 D = 1</b>（和 BPSK / 2-PAM 一样，讲义第 3 章 p.21）。两点距离：<div class="calc">d = |s₂ − s₁| = |(+1) − (−1)| = <b>2</b></div>每个点的能量 E<sub>b</sub> = 1² = 1，所以 d = 2√E<sub>b</sub>，与讲义 BPSK 的 d<sub>min</sub> = 2A（A = 1）一致 ✓。' + CONST)
  + S(2, '<b>(ii) 条件均值和方差</b>：给定 s 后它是常数，y = s + w 只是把零均值噪声平移了 s。用 Ch1b 的性质 E[X + a] = E[X] + a（p.10）、V[X + a] = V[X]（p.11）：<div class="calc">s = +1：E[y] = 1 + E[w] = 1 + 0 = 1，Var[y] = Var[w] = 0.25<br>s = −1：E[y] = −1 + 0 = −1，Var[y] = 0.25</div>标准差 σ = √0.25 = 0.5。高斯变量加常数仍是高斯，所以 y | s ~ N(±1, 0.25)。')
  + S(3, '<b>(ii) 条件概率密度</b>：把 μ = ±1、σ² = 0.25 代入题给的高斯 pdf。先算两个常数：<div class="calc">2σ² = 2 × 0.25 = 0.5<br>1/√(2πσ²) = 1/√(0.5π) = 1/1.2533 ≈ 0.798</div>所以<div class="calc">p(y | s = +1) = (1/√(0.5π)) e<sup>−(y−1)²/0.5</sup> ≈ 0.798 e<sup>−2(y−1)²</sup><br>p(y | s = −1) = (1/√(0.5π)) e<sup>−(y+1)²/0.5</sup> ≈ 0.798 e<sup>−2(y+1)²</sup></div>两条形状相同的钟形曲线，中心分别在 +1 和 −1。')
  + S(4, '<b>(ii) y 的（无条件）pdf</b>：用全概率公式（total probability，Ch1b p.9），P(s = +1) = P(s = −1) = ½：<div class="calc">p(y) = ½ p(y | +1) + ½ p(y | −1)<br>= ½ · (1/√(0.5π)) [e<sup>−(y−1)²/0.5</sup> + e<sup>−(y+1)²/0.5</sup>]</div>自检：每个条件 pdf 的面积都是 1，½ × 1 + ½ × 1 = 1，所以 p(y) 也是合法的 pdf ✓。')
  + S(5, '<b>(iii) 写出出错事件</b>：发 +1 时，判决规则在 y ≤ 0 时判成 −1，即 1 + w ≤ 0 → w ≤ −1。把 w 除以 σ = 0.5 化成标准正态 z：<div class="calc">P(e | s = +1) = P(w ≤ −1) = P(z ≤ −1/0.5) = P(z ≤ −2) = Q(2)</div>标准正态关于 0 对称，P(z ≤ −2) = P(z ≥ 2) = Q(2)，这一步正好用上题给的 Q 函数定义。')
  + S(6, '<b>(iii) 平均误码率</b>：由对称性，发 −1 时出错是 y &gt; 0，即 w &gt; 1，概率也是 Q(1/0.5) = Q(2)。两个符号等概：<div class="calc">P<sub>b</sub> = ½ Q(2) + ½ Q(2) = Q(2) = 0.02275 ≈ 0.0228</div>（查 Q 表 z = 2.00：2.275 × 10⁻²。）')
  + S(7, '<b>自检</b>：讲义第 3 章 p.21 的公式 P<sub>b</sub> = Q(d<sub>min</sub>/(2σ)) = Q(2/(2 × 0.5)) = Q(2) ✓。也可以用 SNR 验算：σ² = N₀/2 = 0.25 → N₀ = 0.5，E<sub>b</sub>/N₀ = 1/0.5 = 2，P<sub>b</sub> = Q(√(2E<sub>b</sub>/N₀)) = Q(√4) = Q(2) ✓。')
  + '<div class="wans">(i) 1 维，距离 2　(ii) 均值 ±1，方差 0.25　(iii) P<sub>b</sub> = Q(2) ≈ 0.0228</div>',
 note='这道题 (ii) 用到的高斯随机变量性质属于 Ch1b（概率复习），也是 Quiz 范围内的知识。'),

dict(id='y2526s1-q1b1', paper=P, q='Q1(b)(i)', marks='(b) 共 13', page='p2', ch='ch4',
 topic='两支路 MRC：平均输入/输出 SNR · 由误码率求分集增益',
 en='''<p>(b) Mobile radio systems operating with multiple antennas (or branches) at the transmitter and/or receiver can provide diversity in a fading environment.</p>
<p>(i) Consider a system that uses a 2-branch receiver combining technique. The Signal to Noise Ratios (SNR) at the input of the receiver, γ<sub>1</sub> and γ<sub>2</sub>, have the following values and probability distributions.
<span class="eq">γ<sub>i</sub> = 11 dB with a probability of 0.2;　12 dB with a probability of 0.5;　13 dB with a probability of 0.3;　i = 1,2</span>
Determine the average receiver input SNR, the average receiver output SNR if the receiver uses the Maximal Ratio Combing (MRC) technique, and the diversity gain of this system at a probability of error of 2 × 10<sup>−4</sup>.</p>''',
 sol=S(1, '<b>dB → 线性</b>：SNR 要在线性域取平均（dB 是对数，不能直接加权平均）。γ = 10<sup>dB/10</sup>：<div class="calc">11 dB → 10<sup>1.1</sup> = 12.59<br>12 dB → 10<sup>1.2</sup> = 15.85<br>13 dB → 10<sup>1.3</sup> = 19.95</div>')
  + S(2, '<b>平均输入 SNR</b>：离散随机变量的期望 E[γ] = Σ γ<sub>k</sub>P<sub>k</sub>（Ch1b p.10）：<div class="calc">γ̄ = 0.2 × 12.59 + 0.5 × 15.85 + 0.3 × 19.95<br>= 2.518 + 7.924 + 5.986 = 16.43<br>10 log₁₀ 16.43 = 12.16 dB</div>对比：直接平均 dB 得 0.2 × 11 + 0.5 × 12 + 0.3 × 13 = 12.1 dB，偏小，是错误做法。')
  + S(3, '<b>MRC 平均输出 SNR</b>：MRC 的输出 SNR 是各支路 SNR 之和 γ<sub>Σ</sub> = γ₁ + γ₂（讲义第 4 章 p.16：γ<sub>MRC</sub> = ΣA<sub>i</sub>²E<sub>b</sub>/N₀）。期望是线性的，两支路同分布：<div class="calc">γ̄<sub>Σ</sub> = E[γ₁] + E[γ₂] = 2 × 16.43 = 32.86<br>10 log₁₀ 32.86 = 15.17 dB</div>自检：阵列增益（array gain）g = γ̄<sub>Σ</sub>/γ̄ = 32.86/16.43 = 2 → 3.01 dB，正好等于 15.17 − 12.16 = 3.01 dB ✓。')
  + S(4, '<b>分集增益公式</b>（讲义第 4 章 p.27）：高 SNR 时 P̄<sub>e</sub> ≈ γ̄<sup>−d</sup>，两边取 log₁₀：<div class="calc">log₁₀P̄<sub>e</sub> = −d · log₁₀γ̄ → d ≈ −log₁₀P̄<sub>e</sub> / log₁₀γ̄</div>讲义写明 γ̄ 是<b>合并器输入</b>的平均 SNR，而且要用线性值，不是 dB。')
  + S(5, '<b>代数</b>：<div class="calc">log₁₀(2 × 10⁻⁴) = log₁₀2 − 4 = 0.301 − 4 = −3.699<br>log₁₀(16.43) = 1.216<br>d ≈ 3.699 / 1.216 = 3.04 ≈ 3.0</div>')
  + S(6, '<b>自检</b>：反代 16.43<sup>−3.04</sup> ≈ 2 × 10⁻⁴ ✓。常见错误：代入输出 SNR 32.86，得 d = 3.699/1.517 = 2.44，不符合讲义的定义。Practice 4 Q2 的官方答案也是用输入 SNR 算 d（γ̄ = 10，P̄<sub>s</sub> = 7.6×10⁻⁹ → d = 8.1）。')
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
 sol=S(1, '<b>(ii) 为什么是 SIMO</b>：两个方程里只有<b>一个</b>发送符号 s（一根发射天线，N = 1），却有<b>两个</b>接收信号 y₁、y₂（两根接收天线，M = 2），各自经过不同的信道增益 h₁、h₂，再叠加独立噪声 v₁、v₂。所以是单输入多输出（Single-Input Multiple-Output，1 × 2）。写成向量（讲义第 5 章 p.12）：<div class="calc">y = [y₁, y₂]<sup>T</sup> = s · h + v<br>h = [h₁, h₂]<sup>T</sup>，v = [v₁, v₂]<sup>T</sup></div>')
  + S(2, '<b>(ii) 线性合并</b>：接收端给两路加权再相加（讲义第 5 章 p.13）：<div class="calc">ŝ = w₁*y₁ + w₂*y₂<br>= s(w₁*h₁ + w₂*h₂) + (w₁*v₁ + w₂*v₂)<br>SNR = E|s|² · |w<sup>H</sup>h|² / (σ² ‖w‖²)</div>取 w ∝ h（每路乘自己信道增益的共轭，即最大比合并 MRC）时 SNR 最大（p.14–15）：<div class="calc">SNR<sub>max</sub> = (E|s|²/σ²)(|h₁|² + |h₂|²)</div>')
  + S(3, '<b>(ii) 为什么得到分集</b>：SNR<sub>max</sub> 正比于 |h₁|² + |h₂|²，只有两路<b>同时</b>很弱时它才小；h₁ 深衰落而 h₂ 较大时，仍能从 ŝ 正确检测 s（p.15）。若 h₁、h₂ 统计独立（天线间距足够大），两路同时深衰落的概率是各自概率的乘积：例如单路深衰落概率为 0.1，两路同时只有 0.1 × 0.1 = 0.01（第 4 章 p.3：P<sub>out</sub><sup>M</sup>）。所以误码率随 SNR 下降得更快，分集阶数 d = M = 2（第 4 章 p.28）。这就是接收分集（receive diversity）。')
  + S(4, '<b>(iii) 求行列式</b>：Λ = diag(λ₁, …, λ<sub>r</sub>) 是对角阵，I + Λ/σ² 也是对角阵，对角元为 1 + λ<sub>i</sub>/σ²。对角阵的行列式 = 对角元素的乘积：<div class="calc">det{I + Λ/σ²} = (1 + λ₁/σ²)(1 + λ₂/σ²)…(1 + λ<sub>r</sub>/σ²)<br>= Π<sub>i=1</sub><sup>r</sup>(1 + λ<sub>i</sub>/σ²)</div>（Λ 来自 HPH<sup>H</sup> = UΛU<sup>H</sup> 的特征分解，用 det(I + AB) = det(I + BA) 和 U<sup>H</sup>U = I 把 U 消掉，讲义第 5 章 p.34–35。）')
  + S(5, '<b>(iii) 对数把乘积变成求和</b>：用 log₂(ab) = log₂a + log₂b：<div class="calc">C = B log₂ Π<sub>i</sub>(1 + λ<sub>i</sub>/σ²)<br>= Σ<sub>i=1</sub><sup>r</sup> B log₂(1 + λ<sub>i</sub>/σ²)</div>')
  + S(6, '<b>(iii) 解释：并行信道容量之和</b>：每一项 B log₂(1 + λ<sub>i</sub>/σ²) 正是一个 SNR 为 λ<sub>i</sub>/σ² 的 SISO 信道的香农容量（第 5 章 p.33）。所以 MIMO 信道等价于 r 个互不干扰的并行“数据管道”（eigen-sub-channels），总容量是它们之和（p.36）。r = rank(HPH<sup>H</sup>) ≤ min(N, M)，这也是 MIMO 容量随 min(N, M) 线性增长的原因。小例子：r = 2，λ₁/σ² = 4，λ₂/σ² = 1，每 Hz 容量 log₂ det = log₂(5 × 2) = log₂10 = 3.32，等于 log₂5 + log₂2 = 2.32 + 1 = 3.32 ✓。')
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
 sol=S(1, '<b>(i) 读出信道系数</b>：H(Z) 的各项系数就是信道冲激响应：Z⁰ 项 → h[1] = 1，Z⁻¹ 项 → h[2] = 0.3。共 2 个抽头，所以 <b>L = 2</b>。代回题中的求和式（i = 1 → m[n]h[1]，i = 2 → m[n−1]h[2]）：<div class="calc">r[n] = m[n] + 0.3m[n−1] + w(n)</div>即当前符号 + 前一个符号 30% 的干扰（ISI）+ 噪声。')
  + S(2, '<b>(ii) 写出出错条件</b>：σ = √0.36 = 0.6。设 m[n] = +1，m̂[n] = sgn(r[n]) 出错当且仅当 r[n] ≤ 0：<div class="calc">1 + 0.3m[n−1] + w ≤ 0 → w ≤ −(1 + 0.3m[n−1])</div>前一符号 m[n−1] = ±1 等概，所以分两种情况：先求给定 ISI 的条件误码率，再对 ISI 取平均（讲义第 6 章 p.27–28）。')
  + S(3, '<b>(ii) 两种情况</b>：P(w ≤ −a) = Q(a/σ)：<div class="calc">m[n−1] = +1：a = 1.3，Q(1.3/0.6) = Q(2.17) ≈ 0.0150<br>m[n−1] = −1：a = 0.7，Q(0.7/0.6) = Q(1.17) ≈ 0.1210</div>（Q 表取两位小数；用精确的 z = 2.167、1.167 是 0.0151、0.1217。）ISI 与当前符号同号时信号被加强，异号时被削弱，误码主要来自后者。')
  + S(4, '<b>(ii) 取平均</b>：<div class="calc">P<sub>e</sub> = ½(0.0150 + 0.1210) = 0.068（精确值 ½(0.0151 + 0.1217) = 0.0684）</div>m[n] = −1 时完全对称，结果相同，所以平均误码率 <b>P<sub>e</sub> ≈ 0.068</b>。对比：没有 ISI 时 P<sub>e</sub> = Q(1/0.6) = Q(1.67) ≈ 0.0475，ISI 让误码率变为约 1.4 倍。')
  + S(5, '<b>(iii) 噪声经过均衡器</b>：均衡器是 FIR 滤波器，输出噪声是输入噪声与抽头的卷积（第 6 章 p.21：w′ = w ∗ c）。C(Z) = 1 − c₁Z⁻¹ + c₂Z⁻² 的抽头是 (1, −c₁, c₂)：<div class="calc">w′(n) = w(n) − c₁w(n−1) + c₂w(n−2)</div>')
  + S(6, '<b>(iii) 求输出噪声方差</b>：w(n)、w(n−1)、w(n−2) 相互独立（白噪声）、方差都是 σ² = 0.36。独立变量和的方差 = 方差之和，系数要平方（Ch1b p.11：V(aX) = a²V(X)）：<div class="calc">Var[w′] = σ²(1² + (−c₁)² + c₂²) = 0.36(1 + c₁² + c₂²)</div>这就是讲义 p.27 的 σ²‖c‖²。因为 c₁ &gt; 0、c₂ &gt; 0，c₁² + c₂² &gt; 0，所以 Var[w′] &gt; 0.36，输出噪声方差多出 0.36(c₁² + c₂²)。这就是线性均衡器的“噪声增强”（第 6 章 p.29、p.41）。')
  + S(7, '<b>(iii) 数字例子</b>：这个 C(Z) 正好是本信道迫零均衡器（ZFE）的前三个抽头：长除法 1/(1 + 0.3Z⁻¹) = 1 − 0.3Z⁻¹ + 0.09Z⁻² − …（同讲义 p.24 的做法），即 c₁ = 0.3、c₂ = 0.09：<div class="calc">Var[w′] = 0.36 × (1 + 0.09 + 0.0081) = 0.36 × 1.0981 = 0.395 &gt; 0.36 ✓</div>噪声功率增加约 9.8%（0.41 dB）。')
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
 sol=S(1, '<b>(i) 平坦衰落条件</b>：每个子载波的带宽要小于相干带宽，子信道才是平坦衰落（讲义第 7 章 p.5：1/T &lt; B<sub>C</sub>）。子载波带宽 Δf = B/N（p.8）：<div class="calc">Δf = B/N &lt; B<sub>C</sub> → N &gt; B/B<sub>C</sub> = 500 kHz / 30 kHz = 16.67</div>N 是整数，向上取 <b>N<sub>min</sub> = 17</b>。验算：500/17 = 29.4 kHz &lt; 30 kHz ✓；N = 16 时 500/16 = 31.25 kHz &gt; 30 kHz ✗。')
  + S(2, '<b>(ii) 子载波带宽与符号时长</b>：N = 50（50 &gt; 17，满足平坦衰落）：<div class="calc">Δf = 500 kHz / 50 = 10 kHz<br>T = 1/Δf = 1/(10 × 10³ Hz) = 100 µs</div>另一种算法：T<sub>S</sub> = 1/B = 1/500 kHz = 2 µs，T = NT<sub>S</sub> = 50 × 2 µs = 100 µs ✓。')
  + S(3, '<b>(ii) 加保护间隔</b>：为消除时延扩展造成的块间干扰，保护间隔要满足 T<sub>G</sub> ≥ T<sub>D</sub> = 10 µs（第 7 章 p.5、p.17），取 T<sub>G</sub> = 10 µs。一个 OFDM 块的总时长（p.18）：<div class="calc">NT<sub>S</sub> + T<sub>G</sub> = 100 µs + 10 µs = 110 µs</div>')
  + S(4, '<b>(ii) 每块比特数与有效速率</b>：4-QAM 每个符号 log₂4 = 2 bit，每块 50 个子载波各送一个符号：<div class="calc">每块 50 × 2 = 100 bit<br>R<sub>eff</sub> = 100 bit / 110 µs = 9.09 × 10⁵ bit/s ≈ 909 kbit/s</div>不计保护间隔时是 100 bit / 100 µs = 1 Mbit/s；保护间隔占掉 10/110 = 9.1% 的时间，所以有效速率 = 1 Mbit/s × 100/110 ≈ 909 kbit/s ✓。')
  + S(5, '<b>(iii) 相关器做什么</b>：第 n 个相关器把 r(t) 乘以 (1/√T)e<sup>−j2πnt/T</sup>，在一个 OFDM 符号期 [0, T] 内积分（T = T<sub>OFDM</sub>，第 7 章 p.12–13）。只看信号部分 x(t)；s<sub>k</sub> 在一个符号期内是常数，可以提到积分号外：<div class="calc">(1/√T)∫₀<sup>T</sup> x(t)e<sup>−j2πnt/T</sup>dt<br>= (1/√T)(1/√T) Σ<sub>k</sub> s<sub>k</sub> ∫₀<sup>T</sup> e<sup>j2πkt/T</sup>e<sup>−j2πnt/T</sup>dt<br>= (1/T) Σ<sub>k</sub> s<sub>k</sub> ∫₀<sup>T</sup> e<sup>j2π(k−n)t/T</sup>dt</div>')
  + S(6, '<b>(iii) 用正交性算积分</b>：k = n 时被积函数是 e⁰ = 1，积分 = T。k ≠ n 时：<div class="calc">∫₀<sup>T</sup> e<sup>j2π(k−n)t/T</sup>dt = [T/(j2π(k−n))] (e<sup>j2π(k−n)</sup> − 1) = 0</div>因为 k − n 是非零整数，e<sup>j2π(k−n)</sup> = 1（在 T 内走完整数个周期）。合起来就是 ∫₀<sup>T</sup> e<sup>j2π(k−n)t/T</sup>dt = T·δ[k − n]，即子载波正交（第 7 章 p.7）。')
  + S(7, '<b>(iii) 结果</b>：求和里只剩 k = n 一项：<div class="calc">输出 = (1/T) · s<sub>n</sub> · T = s<sub>n</sub>(t)</div>其他 N − 1 个子载波的贡献全部为 0，没有子载波间干扰（ICI）；噪声项单独积分成 w<sub>n</sub>，所以 r<sub>n</sub> = s<sub>n</sub> + w<sub>n</sub>（p.13）。')
  + '<div class="wans">(i) N ≥ 17　(ii) ≈ 909 kbit/s（不计保护间隔 1 Mbit/s）　(iii) 子载波正交 → 输出 s<sub>n</sub></div>'),

dict(id='y2526s1-q3a', paper=P, q='Q3(a)', marks=12, page='A', ch='ch4',
 topic='小区数 · 总信道数（扣保护带）· 小区容量 · 频谱效率 channels/MHz/km²',
 en='''<p>3. (a) A metropolis city with a total area of 1500 km<sup>2</sup> is covered by a hexagonal cellular system with a cluster size of 9. Suppose that each cell has a radius R of 2 km and the cellular system is allocated 25 MHz of spectrum, with a full-duplex channel bandwidth of 30 kHz and a total 40 kHz guard bands. The system uses frequency division multiple access (FDMA) with 18 control channels. Determine:</p>
<p>(i) the number of cells in the service area;</p>
<p>(ii) the number of channels without frequency reuse;</p>
<p>(iii) The cell capacity; and</p>
<p>(iv) The system spectral efficiency in the units of channels/ MHz / km<sup>2</sup>.</p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(i) 小区面积</b>：正六边形由 6 个边长为 R 的等边三角形组成，面积 = (3√3/2)R²：<div class="calc">A<sub>c</sub> = (3√3/2) × 2² = 2.598 × 4 = 10.39 km²</div>')
  + S(2, '<b>(i) 小区数</b>：<div class="calc">N<sub>cells</sub> = 1500 / 10.39 = 144.3 → 145 个</div>小区数必须是整数，向上取整才能完全覆盖 1500 km²（写 ≈ 144 并说明是近似也可以）。')
  + S(3, '<b>(ii) 不复用时的信道数</b>：先扣掉保护带，再除以每条全双工信道的带宽（题目的 30 kHz 已经是一条全双工信道占用的带宽，算法同讲义 Part A p.44 例题）：<div class="calc">可用带宽 = 25 MHz − 40 kHz = 25 000 − 40 = 24 960 kHz<br>信道数 = 24 960 / 30 = 832 条</div>')
  + S(4, '<b>(iii) 小区容量</b>：832 条中有 18 条控制信道（簇内每小区 18/9 = 2 条），话务信道 832 − 18 = 814 条。每簇 9 个小区平分全部信道（均匀固定分配 UFCA，讲义 p.92–93）：<div class="calc">814 / 9 = 90.4 → 每小区 90 条话务信道</div>信道不能取分数，向下取整。（若把控制信道也算进来：832/9 = 92.4 → 92 条。）')
  + S(5, '<b>(iv) 频谱效率</b>（讲义 Part A p.40）：η<sub>m</sub> = (B<sub>w</sub>/B<sub>c</sub>)/(B<sub>w</sub>·A<sub>c</sub>·N)，分子是系统信道数，分母是带宽 × 一个簇的面积。B<sub>w</sub> 约掉，B<sub>c</sub> 换成 MHz（30 kHz = 0.03 MHz）：<div class="calc">η = 1/(B<sub>c</sub>·A<sub>c</sub>·N) = 1/(0.03 × 10.39 × 9)<br>= 1/2.806 = 0.356 channels/MHz/km²</div>')
  + S(6, '<b>(iv) 自检</b>：用实际的 832 条信道按定义直接算（每簇 832 条信道覆盖 9 个小区）：<div class="calc">η = 832 / (25 MHz × 9 × 10.39 km²) = 832 / 2338 = 0.356 ✓</div>全系统算也一样：每小区 832/9 = 92.4 条 × 144.3 个小区 ≈ 13 340 条，÷ (25 × 1500) ≈ 0.356 ✓。')
  + '<div class="wans">(i) ≈ 145 个小区　(ii) 832 条　(iii) 90 条话务信道/小区　(iv) ≈ 0.36 channels/MHz/km²</div>'),

dict(id='y2526s1-q3b', paper=P, q='Q3(b)', marks=9, page='A', ch='ch8',
 topic='Erlang C（5% 延迟概率）· 每 km² 用户数 · 平均通话时长',
 en='''<p>(b) A cellular system has a cluster size of 9. In the system, there are 1001 radio channels for traffic. The area of each cell is 4 km<sup>2</sup>. The entire service area of the system is 3500 km<sup>2</sup>. Given that the traffic load per user is 0.03 Erlangs and the average number of calls per hour per user is 1.5. For an Erlang C system with a blocking probability of 5%, determine the following:</p>
<p>(i) The traffic load per cell;</p>
<p>(ii) The number of users per km<sup>2</sup>; and</p>
<p>(iii) The average call duration of a call.</p>
<p class="marks">(9 Marks)</p>''',
 sol=S(1, '<b>(i) 每小区信道数</b>：簇大小 9，1001 条话务信道均分：<div class="calc">M = 1001 / 9 = 111.2 → 111 条/小区</div>信道只能取整数，向下取。')
  + S(2, '<b>(i) 查 Erlang C 表</b>：Erlang C 是排队（呼叫等待）模型（讲义 Part A p.125），题中的 5% 是呼叫需要等待的概率（probability of non-zero delay）。附录表在 100 条以上每 5 条一行，没有 111，取 0.05 列的相邻两行：<div class="calc">M = 110 → A = 92.519 E<br>M = 115 → A = 97.108 E</div>')
  + S(3, '<b>(i) 线性插值</b>（讲义 p.127，附录也给了公式 f(x) = f(x<sub>i</sub>) + (x − x<sub>i</sub>)/(x<sub>i+1</sub> − x<sub>i</sub>) · [f(x<sub>i+1</sub>) − f(x<sub>i</sub>)]）：<div class="calc">A = 92.519 + (111 − 110)/(115 − 110) × (97.108 − 92.519)<br>= 92.519 + 0.2 × 4.589 = 92.519 + 0.918 = 93.44 E</div>用 Erlang C 公式精确求解也是 93.44 E，插值误差可忽略 ✓。所以每小区话务量 ≈ <b>93.4 Erlang</b>。')
  + S(4, '<b>(ii) 每 km² 用户数</b>：每个用户贡献 A<sub>u</sub> = 0.03 E，小区面积 4 km²：<div class="calc">每小区用户 U = A/A<sub>u</sub> = 93.44 / 0.03 = 3114.7<br>每 km² 用户 = 3114.7 / 4 = 778.7 ≈ 779 用户/km²</div>')
  + S(5, '<b>(iii) 平均通话时长</b>：每用户话务量 = 呼叫率 × 平均时长，A<sub>u</sub> = λ<sub>u</sub>H（讲义 p.121 的 λ/μ）：<div class="calc">H = A<sub>u</sub>/λ<sub>u</sub> = 0.03 E / (1.5 次/小时) = 0.02 小时<br>0.02 × 3600 s = <b>72 s</b></div>验算：1.5 × 72/3600 = 0.03 E ✓。')
  + '<div class="wans">(i) ≈ 93.4 E　(ii) ≈ 779 用户/km²　(iii) 72 s</div>',
 note='3500 km² 这个条件在三小问里都用不到（可以用来算总小区数 875 个）。'),

dict(id='y2526s1-q3c', paper=P, q='Q3(c)', marks=4, page='A', ch='ch7',
 topic='固定信道分配 FCA 与动态信道分配 DCA',
 en='''<p>(c) Briefly describe the concept of fixed and dynamic channel assignment for a cellular system.</p>
<p class="marks">(4 Marks)</p>''',
 sol=S(1, '<b>固定信道分配（Fixed Channel Assignment，FCA）</b>（讲义 Part A p.92）：每个小区（基站）预先分到一组固定的信道，小区内的呼叫只能使用本小区空闲的信道。原因：信道组是按簇和复用距离事先规划好的，同频干扰在设计时就已控制住，运行时不需要再计算。')
  + S(2, '<b>FCA 的两种形式和缺点</b>：均匀 FCA（UFCA）每个小区信道数相同，例如共 210 条、N = 7 → 每小区 30 条（1 条控制，29 条话务，p.93）；非均匀 FCA 按各小区的业务量分配不同数量。缺点（p.94）：本小区信道用完，新呼叫就被阻塞，即使相邻小区还有空闲信道。原因是信道被“锁死”在小区里，不能随业务量的变化流动。简单，但适应性差。')
  + S(3, '<b>动态信道分配（Dynamic Channel Assignment，DCA）</b>（p.95）：信道不永久分给小区；新呼叫到来时，任何基站都可以按某种算法使用任意信道，只要不违反同频干扰约束。最简单的形式是信道借用（channel borrowing）：小区 A 借用小区 C 的空闲信道，通话期间持续监测，结束后归还。')
  + S(4, '<b>DCA 的规则和优缺点</b>（p.96）：算法依据对未来阻塞的预测、信道的复用距离和其他代价函数；基本约束：一个信道在某小区使用时，复用距离 D 以内的其他小区不能同时使用它，否则同频干扰超标。优点：业务量大的小区可以用更多信道，灵活、阻塞率低；代价：要实时监测信道，需要集中控制和更多计算，更复杂。')
  + '<div class="wans">FCA：固定分组、简单但不灵活；DCA：按需分配、受复用距离约束、灵活但复杂</div>'),

dict(id='y2526s1-q4a', paper=P, q='Q4(a)', marks=8, page='B', ch='ch3',
 topic='接入 AP 的过程：扫描 → 认证 → 关联',
 en='''<p>4. (a) An Access Point (AP) is a portal of a Wireless Local Area Network (WLAN), which can be used to connect to the Internet. When a user tries to connect to an AP, there will be a connection establishment procedure. Describe the connection establishment process and explain the function of the authentication process.</p>
<p class="marks">(8 Marks)</p>''',
 sol=S(1, '<b>① 获取同步信息（扫描，scanning）</b>（讲义 Part B p.31）：节点要加入已有的 BSS，必须先从 AP 获得同步信息，否则不知道 AP 的存在和参数。两种方式：<b>被动扫描</b>（passive），等待 AP 周期性广播的信标帧（Beacon Frame）；<b>主动扫描</b>（active），节点发送探测请求帧（Probe Request），等待 AP 回复探测响应帧（Probe Response）。被动扫描只需接收，主动扫描不用等下一个信标，找 AP 更快。')
  + S(2, '<b>② 认证（Authentication）</b>（p.32）：找到 AP 后，节点和 AP 交换信息，<b>双方各自证明知道约定的密码</b>。作用：确认对方是合法用户 / 合法 AP，只让授权设备接入网络，防止未授权用户占用资源或窃取数据。它是关联之前的“门禁”：认证不通过就不能进行下一步。')
  + S(3, '<b>③ 关联（Association）</b>（p.32）：认证通过后开始关联，交换节点和 BSS 的能力信息，并把节点当前的位置通知分布系统（DSS，所有 AP 的集合）。为什么要登记位置：分布系统要知道这个节点挂在哪个 AP 下，发给它的数据才能转发到正确的 AP。')
  + S(4, '<b>④ 开始传数据</b>：只有关联完成后，节点才能收发数据帧。顺序是固定的：扫描 → 认证 → 关联 → 数据，前一步不完成，后一步无法进行。')
  + '<div class="wans">扫描（被动/主动）→ 认证（互证密码，防止非法接入）→ 关联（交换能力、登记位置）→ 开始传数据</div>'),

dict(id='y2526s1-q4bc', paper=P, q='Q4(b)(c)', marks=17, page='B', ch='ch7',
 topic='IoT 的五个难点 · 雾计算的关键特征',
 en='''<p>(b) The Internet of Things (IoT) is the technique that connects all unconnected objects. Discuss five of the potential difficulties and briefly describe each of them in the context of the development of IoT.</p>
<p class="marks">(10 Marks)</p>
<p>(c) An outstanding technique that processes data generated by IoT sensors is fog computing. Discuss the key features of fog computing.</p>
<p class="marks">(7 Marks)</p>''',
 sol=S(1, '<b>(b) 难点 ①–③</b>（讲义 Part B p.82）：<br>① <b>可扩展性（Scalability）</b>：IoT 设备可达数百万个，整个系统如何支撑这么多设备是关键问题；网络层可用 IPv6 为海量设备分配地址（IPv4 地址不够用）。<br>② <b>安全（Security）</b>：联网的“物”越多，攻击面越大；一台设备被攻破后，它的连通性反而成为攻击其他设备和系统的跳板。<br>③ <b>隐私（Privacy）</b>：传感器越来越多，采集的数据往往与具体个人及其活动相关，可能包含敏感信息和凭证；数据如何保护、是否共享、与谁共享都是关键问题。')
  + S(2, '<b>(b) 难点 ④–⑤</b>（p.83）：<br>④ <b>大数据与分析（Big data and analytics）</b>：海量传感器产生数据洪流，只有高效处理才能得到有价值的信息；难点在于要及时处理来自不同来源、不同格式的大量数据。<br>⑤ <b>互操作性（Interoperability）</b>：各种协议和架构在争夺市场和标准，有的私有、有的开放，不同设备 / 网络难以互通；新的 IoT 标准能缓解，但实际中仍并存多种协议和实现。')
  + S(3, '<b>(c) 雾计算是什么</b>（p.106）：把数据管理和处理尽量放到 IP 网络的边缘、靠近传感器的地方；任何有计算、存储和网络连接能力的设备都可以做雾节点，相当于在传统 IT 计算模型里多出一层“雾层”（fog layer）。为什么需要：IoT 数据量巨大，全部送到云端会带来高时延和核心网拥塞。')
  + S(4, '<b>(c) 关键特征</b>（p.109）：<br>• <b>上下文位置感知与低时延</b>：雾节点尽可能靠近 IoT 终端做分布式计算，数据不必绕到云端，反应快；<br>• <b>地理分布</b>：雾节点服务的业务和应用需要广泛的分布式部署；<br>• <b>部署在大量 IoT 终端附近</b>：一个雾节点通常管理很多终端；<br>• <b>雾节点与终端之间用无线通信</b>：要连接大量终端，无线接入最容易实现大规模扩展；<br>• <b>用于实时交互</b>：在雾节点预处理数据，上层应用只需对数据子集做批处理。')
  + S(5, '<b>(c) 带来的好处</b>（p.106、p.108）：就近分析数据可以降低时延、卸载核心网的大量流量、让敏感数据留在本地网络；雾节点了解所管理传感器的上下文，能比云端更快地响应事件，形成分布式边缘控制回路（实时监测、控制和分析，不用等云端），并减少需要上传的数据量。')
  + '<div class="wans">(b) 可扩展性、安全、隐私、大数据分析、互操作性　(c) 低时延/位置感知、地理分布、靠近终端、无线接入、实时交互</div>'),
]
