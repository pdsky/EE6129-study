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
 sol=S(1, '<b>(i) 第一组比较：B<sub>s</sub> vs B<sub>c</sub> → 平坦 / 频率选择性</b>：相干带宽（coherence bandwidth）B<sub>c</sub> 是信道频率响应仍然相关的最大频率间隔，由多径时延扩展决定：时延扩展越大，B<sub>c</sub> 越小（讲义 Ch2 p.31–33）。<br>• B<sub>s</sub> &lt; B<sub>c</sub>：信号带宽内所有频率的衰落基本相同 → <b>平坦衰落（flat fading）</b>，频谱失真小；时域上等价于 rms 时延扩展 ≪ 符号时长（经验值 σ<sub>τ</sub>/T<sub>s</sub> &lt; 0.1）。<br>• B<sub>s</sub> &gt; B<sub>c</sub>：不同频率分量衰落不同 → <b>频率选择性衰落（frequency-selective fading）</b>；时域上时延扩展占符号时长相当一部分，前一个符号拖进下一个，产生 ISI。')
  + S(2, '<b>(i) 第二组比较：B<sub>s</sub> vs B<sub>D</sub> → 慢 / 快衰落</b>：多普勒扩展（Doppler spread）B<sub>D</sub> = f<sub>m</sub> = f<sub>c</sub>v/c 由移动造成；相干时间 T<sub>c</sub> ≈ 1/B<sub>D</sub> 是信道基本不变的时长（p.35–37）。因为 B<sub>s</sub> ≈ 1/T<sub>s</sub>，比带宽就等于比时长：<br>• B<sub>s</sub> ≫ B<sub>D</sub>（⇔ T<sub>s</sub> ≪ T<sub>c</sub>）：一个符号内信道的幅度、相位几乎不变 → <b>慢衰落（slow fading）</b>。<br>• B<sub>s</sub> 与 B<sub>D</sub> 相当或更小（T<sub>s</sub> ≳ T<sub>c</sub>）：符号内信道就在变 → <b>快衰落（fast fading）</b>。<br><b>组合</b>：两个判断互相独立（一个看多径时延，一个看移动速度），p.39 的图把它们组合成四类：平坦慢、平坦快、频选慢、频选快。例：B<sub>D</sub> ≪ B<sub>s</sub> &lt; B<sub>c</sub> → 平坦慢衰落。')
  + S(3, '<b>(ii) 求 LCR</b>：电平通过率（level crossing rate）L<sub>Z</sub> = 信号每秒向下穿过门限 Z<sub>min</sub> 的平均次数（p.40）。每次深衰落对应一次向下穿越，所以直接用次数除以观测时间：<div class="calc">L<sub>Z</sub> = 40 次 / 10 s = 4 次/秒</div>')
  + S(4, '<b>(ii) 连续误符号数</b>：平均衰落持续时间（AFD）τ̄ = 20 ms，符号时长 T<sub>s</sub> = 5 ms，题设衰落里的符号全错，所以每次衰落连错：<div class="calc">τ̄ / T<sub>s</sub> = 20 ms / 5 ms = 4 个连续错符号</div><br>每秒有 4 次衰落：<div class="calc">每秒误符号数 = L<sub>Z</sub> × τ̄/T<sub>s</sub><br>= 4 次/s × 4 个/次 = 16 个/s</div><br>错误成串出现：每秒 4 串，每串 4 个。<br><b>自检</b>：每秒共 1/T<sub>s</sub> = 1/0.005 = 200 个符号，16/200 = 8%；信号处在深衰落里的时间比例 = L<sub>Z</sub> × τ̄ = 4 × 0.02 = 0.08 = 8%（p.42 的 AFD 定义反过来用）。两者一致 ✓')
  + S(5, '<b>(iii) 换线性</b>：公式里的 SNR 必须用线性值：<div class="calc">γ̄<sub>R</sub> = 25 dB → 10<sup>25/10</sup> = 10<sup>2.5</sup> = 316.2</div><br><div class="calc">1/(1 − ε) = 1/0.995 = 1.005025<br>ln(1.005025) = 0.0050125</div><br>（ε 很小时 ln(1/(1−ε)) ≈ ε = 0.005，可以用来估算。）')
  + S(6, '<b>(iii) 最小 SNR</b>：Rayleigh 衰落下 SNR 的 CDF 是 F(γ) = 1 − e<sup>−γ/γ̄</sup>。令 P(γ &lt; γ<sub>min</sub>) = ε，解出 γ<sub>min</sub> = F<sup>−1</sup>(ε)，就是题中公式 log 里的那一项（讲义 Ch2 p.50–51）：<div class="calc">γ<sub>min</sub> = γ̄<sub>R</sub> ln(1/(1−ε))<br>= 316.2 × 0.0050125 = 1.585<br>→ 10 log₁₀1.585 = 2.0 dB</div><br>意思：以 1 − ε = 99.5% 的概率，瞬时 SNR 不低于 1.585（2.0 dB），所以 C<sub>ε</sub> = B log₂(1 + 1.585) = 1.37B bit/s。')
  + S(7, '<b>(iii) 衰落余量</b>：AWGN 信道要达到同样的容量 C<sub>ε</sub>，只需 γ<sub>AWGN</sub> = γ<sub>min</sub> = 2.0 dB；衰落信道却要平均 25 dB。差值就是衰落余量（fade margin）（p.51）：<div class="calc">FM = γ̄<sub>R,dB</sub> − γ<sub>AWGN,dB</sub><br>= 25 − 2.0 = 23.0 dB</div><br><b>自检</b>：用 p.51 的公式直接算，FM = 10 log₁₀[1/ln(1/(1−ε))] = 10 log₁₀(1/0.0050125) = 10 × 2.300 = 23.0 dB ✓（与 γ̄<sub>R</sub> 无关）。p.51 的例子 ε = 0.01 → 20 dB；ε 减半，余量多 3 dB，吻合 ✓')
  + '<div class="wans">(ii) LCR = 4 /s；每秒约 16 个错符号（每次衰落 4 个连续错误）　(iii) γ<sub>min</sub> ≈ 2.0 dB，FM ≈ 23 dB</div>'),

dict(id='y2526s2-q1b1', paper=P, q='Q1(b)(i)', marks='(b) 共 13', page='p2', ch='ch4',
 topic='由输入/输出 SNR 求阵列增益 · 由分集增益求误码率',
 en='''<p>(b) (i) Consider a receiver diversity combining technique. If the average input Signal-to-Noise Ratio (SNR) is 12dB, the average combiner output SNR is 15dB, and the diversity gain is 3.7, determine the gain array and the probability of error.</p>''',
 sol=S(1, '<b>阵列增益</b>（array gain，题中写作 "gain array"）：定义 g = γ̄<sub>Σ</sub>/γ̄，即合并器输出平均 SNR 与输入平均 SNR 之比（讲义 Ch4 p.27）。两个 SNR 都是 dB，比值在 dB 下就是相减，再换回线性：<div class="calc">g<sub>dB</sub> = 15 − 12 = 3 dB<br>g = 10<sup>3/10</sup> = 10<sup>0.3</sup> = 1.995 ≈ 2</div><br>意思：合并后平均 SNR 约提高到 2 倍。')
  + S(2, '<b>输入 SNR 换线性</b>：<div class="calc">γ̄ = 12 dB → 10<sup>12/10</sup> = 10<sup>1.2</sup> = 15.85</div><br>保留 10<sup>1.2</sup> 的形式，下一步直接乘指数，不用算 15.85 的 3.7 次方。')
  + S(3, '<b>误码率</b>：高 SNR 下 P̄<sub>e</sub> ≈ γ̄<sup>−d</sup>，d = 分集增益（diversity gain）= 3.7。p.27 的定义里 γ̄ 是合并器<b>输入</b>平均 SNR，所以代 12 dB：<div class="calc">P̄<sub>e</sub> ≈ (10<sup>1.2</sup>)<sup>−3.7</sup> = 10<sup>−1.2×3.7</sup> = 10<sup>−4.44</sup><br>= 10<sup>0.56</sup> × 10<sup>−5</sup> = 3.63 × 10⁻⁵ ≈ 3.6 × 10⁻⁵</div>')
  + S(4, '<b>自检</b>：用 p.27 的定义反算 d = −log₁₀P̄<sub>e</sub> / log₁₀γ̄ = 4.44 / 1.2 = 3.7 ✓。d = 3.7 表示平均 SNR 每升 10 dB，误码率降到 1/10<sup>3.7</sup> ≈ 1/5000。')
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
 sol=S(1, '<b>(ii) 为什么每条信道只有一个增益</b>：平坦衰落 ⇔ 信号带宽 &lt; 相干带宽，即多径时延扩展远小于符号时长（讲义 Ch2 p.31–33）。所以从第 j 根发射天线到第 i 根接收天线的各条多径几乎同时到达，在一个符号内叠加成<b>一个复数增益 h<sub>ij</sub></b>（模 = 衰落幅度，辐角 = 相移）。没有可分辨的第二个抽头，也就没有 ISI：整个带宽都乘同一个数，所以每对天线只需一个增益（讲义 Ch5 p.4–5）。')
  + S(2, '<b>(ii) 逐根接收天线写</b>（Ch5 p.5）：第 i 根接收天线收到 4 根发射天线信号的加权和，再加本天线的噪声：<div class="calc">y<sub>i</sub> = Σ<sub>j=1</sub><sup>4</sup> h<sub>ij</sub>x<sub>j</sub> + v<sub>i</sub>，i = 1, 2, …, 6</div><br>v<sub>i</sub> 是零均值、方差 σ² 的高斯白噪声，各天线互相独立。')
  + S(3, '<b>(ii) 写成矩阵</b>（p.6）：把 6 个式子上下叠起来：<div class="calc">y = Hx + v<br>y、v：6×1；x：4×1；H：6×4</div><br><div class="calc">H = ⎡h<sub>11</sub> h<sub>12</sub> h<sub>13</sub> h<sub>14</sub>⎤<br>　　⎢h<sub>21</sub> h<sub>22</sub> h<sub>23</sub> h<sub>24</sub>⎥<br>　　⎢ ⋮　 ⋮　 ⋮　 ⋮ ⎥<br>　　⎣h<sub>61</sub> h<sub>62</sub> h<sub>63</sub> h<sub>64</sub>⎦</div><br>行号 i = 接收天线，列号 j = 发射天线。<b>维数自检</b>：(6×4)(4×1) = 6×1，与 y 一致 ✓')
  + S(4, '<b>(iii) 均值</b>：s 是发送的确定信号；h、G 是接收端已知的确定量；只有 w 随机，且 E[w] = 0。期望是线性的：<div class="calc">E[ŝ] = s + (1/‖h‖²)·G·E[w]<br>= s + 0 = s</div><br>所以检测量是<b>无偏</b>（unbiased）的。')
  + S(5, '<b>(iii) 方差</b>：常数 s 不贡献方差；随机项前乘了常数 1/‖h‖²，方差要乘它的平方（Var(aX) = a²Var(X)）：<div class="calc">Var[ŝ] = (1/‖h‖²)² · Var[Gw]<br>= (1/‖h‖⁴) · σ²‖h‖² (1, 1)<sup>T</sup><br>= (σ²/‖h‖²) (1, 1)<sup>T</sup></div><br>即两个检测符号的噪声方差都是 σ²/‖h‖² = σ²/(|h₁|² + |h₂|²)，ŝ ~ N(s, (σ²/‖h‖²)·1)（讲义 Ch5 p.25）。')
  + S(6, '<b>自检与意义</b>：题给的 Var[Gw] 来自 G = F<sup>H</sup> 且 F<sup>H</sup>F = ‖h‖²I：Cov(Gw) = F<sup>H</sup>(σ²I)F = σ²‖h‖²I，对角线正是 σ²‖h‖²(1, 1) ✓。每个子信道 SNR = E|s<sub>n</sub>|²‖h‖²/σ²（p.26）：两条路径的增益 |h₁|² + |h₂|² 相加，噪声被压低，这就是 Alamouti 的二阶分集。')
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
 sol=S(1, '<b>(i) 离散模型</b>：第 n 个接收采样 = 当前符号和前 L − 1 个符号分别乘信道抽头后相加，再加噪声（讲义 Ch6 p.22；讲义下标从 0 开始，这里题目从 1 开始，所以写成 n − i + 1）：<div class="calc">r[n] = Σ<sub>i=1</sub><sup>L</sup> h[i] m[n − i + 1] + w[n]<br>　　 = h[1]m[n] + Σ<sub>i=2</sub><sup>L</sup> h[i]m[n − i + 1] + w[n]</div><br>第一项是想要的符号；中间的和是前面的符号漏进来的 <b>ISI</b>；w[n] 是零均值、方差 0.25 的高斯噪声。')
  + S(2, '<b>(i) Nyquist 准则</b>（p.12）：采样后 y(nT) = m[n]g<sub>e</sub>(0) + Σ<sub>i≠n</sub> m[i]g<sub>e</sub>(nT − iT) + w(nT)，其中 g<sub>e</sub> = g<sub>T</sub> * g<sub>C</sub> * g<sub>R</sub> 是发送滤波器、信道、接收滤波器的等效脉冲，中间的和就是 ISI。无 ISI 的条件：<div class="calc">g<sub>e</sub>(nT − iT) = 1，n = i<br>g<sub>e</sub>(nT − iT) = 0，n ≠ i</div><br>即每个脉冲在<b>其他符号的采样时刻</b>恰好为零（脉冲可以拖尾，只要过零点对准别人的采样点）。对上面的离散模型就是 h[1] = 1、h[2] = … = h[L] = 0。')
  + S(3, '<b>(ii) 输出噪声功率</b>：均衡器是 M 抽头的 FIR 滤波器，噪声也被它滤波：<div class="calc">w′(n) = Σ<sub>j=1</sub><sup>M</sup> c<sub>j</sub> w[n − j + 1]</div><br>w 是白噪声：不同时刻独立、零均值，交叉项 E[w(a)w(b)] = 0（a ≠ b），平方展开后只剩平方项：<div class="calc">σ′² = E[w′²] = Σ<sub>j</sub> c<sub>j</sub>² E[w²] = σ² Σ c<sub>j</sub>²<br>= 0.25 × 2.56 = 0.64</div><br>这就是 p.27 的结论"w′ 的方差 = σ²‖c‖²"。线性均衡消 ISI 的代价：噪声被放大 2.56 倍（约 4.1 dB）。')
  + S(4, '<b>(iii) 化成条件概率</b>：σ′ = √0.64 = 0.8。m(n) = ±1 等概且对称，所以 P<sub>e</sub> = P(错 | m(n) = +1)。此时 y(n) = 1 + 0.2m(n − 1) + w′(n)，sgn 判决出错 ⇔ y(n) &lt; 0。残余 ISI 0.2m(n−1) 等概取 ±0.2，分两种情况（p.28）。')
  + S(5, '<b>(iii) 两种情况</b>：<br>• m(n−1) = +1：均值 1 + 0.2 = 1.2，出错 ⇔ w′ &lt; −1.2：<div class="calc">P = Q(1.2/0.8) = Q(1.5) = 0.0668</div><br>• m(n−1) = −1：均值 1 − 0.2 = 0.8，出错 ⇔ w′ &lt; −0.8：<div class="calc">P = Q(0.8/0.8) = Q(1.0) = 0.1587</div><br>查 Q 表：行 1.5、列 0.00 → 6.681E−02；行 1.0、列 0.00 → 1.587E−01。注意 Q 里除的是标准差 0.8，不是方差 0.64。')
  + S(6, '<b>(iii) 平均</b>：两种情况各占 ½：<div class="calc">P<sub>e</sub> = ½(0.1587 + 0.0668)<br>= ½ × 0.2255 = 0.11275 ≈ 0.113</div><br><b>自检</b>：如果没有残余 ISI，P<sub>e</sub> = Q(1/0.8) = Q(1.25) = 0.1056；有 ISI 时更大（0.113 &gt; 0.106）✓。原因：Q 在正半轴是凸函数，ISI 帮倒忙那一半多出的误码比帮忙那一半省下的多。')
  + '<div class="wans">(ii) 0.64　(iii) P<sub>e</sub> ≈ 0.113</div>'),

dict(id='y2526s2-q2b', paper=P, q='Q2(b)', marks=13, page='p2', ch='ch7',
 topic='4 子载波的信道增益 · OFDM 即 IDFT · 循环前缀与功率损失',
 en='''<p>(b) An OFDM system uses 4 sub-carriers to transmit a baseband signal that has a symbol duration of 2 μs. The fading channel has a Z-transform of 1 + 0.3Z<sup>−1</sup>. The baseband signal can be organized into N signals {s<sub>k</sub>(t)} to form the transmitted OFDM signal,
<span class="eq">x(t) = (1/√T) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub>(t)e<sup>j2π(k/T)t</sup>,　nT ≤ t ≤ (n + 1)T</span></p>
<p>(i) Determine the channel gain coefficients of the OFDM system.</p>
<p>(ii) Explain why the transformation of the signal, {s<sub>k</sub>(t)}, into the OFDM signal, x(t), can be viewed as an inverse Discrete Fourier transform process.</p>
<p>(iii) If the OFDM system uses a cyclic prefix of 20 μs, determine the OFDM symbol duration and the power loss due to the addition of the cyclic prefix.</p>
<p class="marks">(13 Marks)</p>''',
 sol=S(1, '<b>(i) 写出公式</b>：信道 Z 变换 1 + 0.3Z<sup>−1</sup> → 冲激响应 h₀ = 1、h₁ = 0.3（L = 2）。第 k 个子载波的增益就是信道冲激响应的 N 点 DFT（讲义 Ch7 p.15，k = 1…N，H<sub>N</sub> = H₀）：<div class="calc">H<sub>k</sub> = Σ<sub>i=0</sub><sup>L−1</sup> h<sub>i</sub>e<sup>−j2πik/N</sup><br>= 1 + 0.3e<sup>−j2πk/4</sup></div><br>N = 4 时 e<sup>−j2πk/4</sup> = e<sup>−jπk/2</sup> 只取 4 个值：k = 1, 2, 3, 4 → −j, −1, +j, 1。')
  + S(2, '<b>(i) 代入</b>：<div class="calc">H₁ = 1 + 0.3(−j) = 1 − 0.3j，|H₁| = 1.044<br>H₂ = 1 + 0.3(−1) = 0.7<br>H₃ = 1 + 0.3(+j) = 1 + 0.3j，|H₃| = 1.044<br>H₄ = 1 + 0.3(1) = 1.3（= H₀）</div><br>每个子载波只看到一个复数增益：频率选择性信道被拆成 4 个平坦子信道，H₂ 最弱。<br><b>自检</b>（Parseval）：(1/N)Σ|H<sub>k</sub>|² = (1.09 + 0.49 + 1.09 + 1.69)/4 = 4.36/4 = 1.09 = h₀² + h₁² = 1 + 0.09 ✓')
  + S(3, '<b>(ii) 在一个块内采样</b>：块 n 占 nT ≤ t &lt; (n+1)T，取 N 个等间隔采样 t = nT + iT/N，i = 0, 1, …, N−1（讲义 Ch7 p.19）。代入第 k 个子载波：<div class="calc">e<sup>j2π(k/T)(nT + iT/N)</sup> = e<sup>j2πkn</sup> · e<sup>j2πki/N</sup><br>= e<sup>j2πki/N</sup></div><br>（k、n 都是整数，e<sup>j2πkn</sup> = 1。）')
  + S(4, '<b>(ii) 和 IDFT 对比</b>：采样值为<div class="calc">x<sub>i</sub> = (1/√T) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub> e<sup>j2πki/N</sup>，i = 0…N−1</div><br>N 点 IDFT 的定义是 x<sub>i</sub> = (1/N)Σ<sub>k</sub> X<sub>k</sub>e<sup>j2πki/N</sup>：核 e<sup>j2πki/N</sup> 完全相同，只差一个常数比例。所以 x(t) 的 N 个采样就是 {s<sub>k</sub>} 的 IDFT：s<sub>k</sub> 是第 k 个子载波（频域）上的符号，IDFT 把 N 个频域符号变成 N 个时域采样。好处：发射端用一次 IFFT 生成 OFDM 信号，接收端用 FFT 解调，不需要 N 个独立的振荡器和滤波器。')
  + S(5, '<b>(iii) OFDM 符号时长</b>：N = 4 个基带符号（各 T<sub>s</sub> = 2 µs）串并转换后在 4 个子载波上并行传，所以有用部分（数据块）长 NT<sub>s</sub>；前面再加循环前缀（cyclic prefix）T<sub>G</sub>（讲义 Ch7 p.18）：<div class="calc">NT<sub>s</sub> = 4 × 2 µs = 8 µs<br>T<sub>OFDM</sub> = NT<sub>s</sub> + T<sub>G</sub> = 8 + 20 = 28 µs</div>')
  + S(6, '<b>(iii) 功率损失</b>：CP 是复制的数据，接收端直接丢掉，但发射时照样消耗能量（p.18）：<div class="calc">损失 = 10 log₁₀[(NT<sub>s</sub> + T<sub>G</sub>)/NT<sub>s</sub>]<br>= 10 log₁₀(28/8) = 10 log₁₀3.5<br>= 10 × 0.544 = 5.44 dB</div><br><b>自检</b>：有用能量占 8/28 = 28.6%，10 log₁₀0.286 = −5.44 dB ✓。CP 比数据部分还长，所以损失很大；实际设计会增大 N，让 NT<sub>s</sub> ≫ T<sub>G</sub>。')
  + '<div class="wans">(i) {1−0.3j, 0.7, 1+0.3j, 1.3}　(iii) 28 µs，≈ 5.44 dB</div>'),

dict(id='y2526s2-q3a', paper=P, q='Q3(a)', marks=6, page='A', ch='ch6',
 topic='每小区信道 · 簇面积 · 簇复制次数 · 系统容量',
 en='''<p>3. (a) A new operator B is designing the cellular network for a city in South China which has a total of 1071 radio channels available for handling the traffic. Suppose the area of each cell is 6 km<sup>2</sup> and the total area of the entire system is 2100 km<sup>2</sup>. Let the cluster size of the design be 7. Determine the following results.</p>
<p>(i) Number of channels per cell and the total coverage area of each cluster.</p>
<p>(ii) Number of times to replicate this cluster to cover the entire system.</p>
<p>(iii) System capacity for this network.</p>
<p class="marks">(6 Marks)</p>''',
 sol=S(1, '<b>(i) 每小区信道</b>：簇大小 N = 7，一个簇用全部 S = 1071 条信道；均匀固定分配（UFCA）时每个小区分到 S/N 条（讲义 Part A p.81）：<div class="calc">k = S/N = 1071/7 = 153 条/小区</div>')
  + S(2, '<b>(i) 簇面积</b>：一个簇由 7 个小区组成：<div class="calc">A<sub>cluster</sub> = N × A<sub>cell</sub> = 7 × 6 km² = 42 km²</div>')
  + S(3, '<b>(ii) 复制次数</b>：整个服务区要被簇铺满：<div class="calc">M = A<sub>sys</sub>/A<sub>cluster</sub> = 2100/42 = 50 次</div><br>共 7 × 50 = 350 个小区；直接算 2100/6 = 350 ✓')
  + S(4, '<b>(iii) 系统容量</b>：每个簇都把全部 1071 条信道用一遍，簇复制了 M 次（p.81：T = C × N × S/N = CS，讲义的 C 是簇数，这里就是 M）：<div class="calc">T = M × S = 50 × 1071 = 53 550 条信道</div><br><b>自检</b>：按小区算 153 条 × 350 个小区 = 53 550 ✓。同一组 1071 条信道被重复用了 50 次，这就是频率复用带来的容量。')
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
 sol=S(1, '<b>(b)(i) 查 Erlang C 表</b>：由 3(a)，每小区 m = 153 条信道；延迟概率 P<sub>D</sub> = 5% → 表的 0.05 列。表里没有 153，取相邻两行：<div class="calc">150 条 → 129.490 E<br>155 条 → 134.137 E</div>')
  + S(2, '<b>(b)(i) 线性插值</b>：用附录 A 的公式 f(x) = f(x<sub>i</sub>) + (x − x<sub>i</sub>)/(x<sub>i+1</sub> − x<sub>i</sub>) × [f(x<sub>i+1</sub>) − f(x<sub>i</sub>)]：<div class="calc">A = 129.490 + (153 − 150)/(155 − 150) × (134.137 − 129.490)<br>= 129.490 + 0.6 × 4.647<br>= 129.490 + 2.788 = 132.28 ≈ 132.3 E/小区</div><br>（用 Erlang C 公式直接数值求解得 132.24 E，插值误差很小。）<b>检查</b>：每信道负载 A/m = 132.28/153 = 0.865 &lt; 1，排队系统稳定 ✓')
  + S(3, '<b>(b)(ii) 每 km² 用户数</b>：每用户话务量 A<sub>u</sub> = 0.03 E，所以每小区能支持的用户数和用户密度：<div class="calc">U = A/A<sub>u</sub> = 132.28/0.03 = 4409 用户/小区<br>密度 = 4409 / 6 km² = 734.8 ≈ 735 用户/km²</div>')
  + S(4, '<b>(b)(iii) 平均通话时长</b>：每用户话务量 A<sub>u</sub> = λ<sub>u</sub>H（讲义 Part A p.121），λ<sub>u</sub> = 1.2 次/小时：<div class="calc">H = A<sub>u</sub>/λ<sub>u</sub> = 0.03/1.2 = 0.025 h<br>= 0.025 × 3600 s = 90 s</div><br><b>自检</b>：1.2 次/h × 90 s ÷ 3600 s/h = 0.03 E ✓')
  + S(5, '<b>(c)(i) 状态转移图</b>：状态 k = 系统里的呼叫数（正在通话 + 排队）。<br>• 向右 k → k+1：来一个新呼叫，Poisson 到达，速率 λ<sub>k</sub> = λ，与 k 无关。<br>• 向左 k → k−1：结束一个呼叫。k ≤ m 时 k 个呼叫都在占用信道，各以速率 μ 结束，合起来 kμ；k ≥ m 时只有 m 条信道在服务，其余在排队，速率封顶 mμ。' + MMM)
  + S(6, '<b>(c)(ii) 平衡方程</b>：稳态时相邻两个状态之间的流量平衡：从 k−1 往右流的 = 从 k 往左流的（讲义 Part A p.106）：<div class="calc">λP<sub>k−1</sub> = μ<sub>k</sub>P<sub>k</sub></div><br>题中 k ≥ m 那一式写成 mμP<sub>k</sub> = λP<sub>k</sub> 是笔误（那样会得出 λ = mμ），讲义 p.106 是 λP<sub>k−1</sub>。ρ = λ/μ。')
  + S(7, '<b>(c)(ii) k ≤ m</b>：μ<sub>k</sub> = kμ，所以 P<sub>k</sub> = (λ/kμ)P<sub>k−1</sub> = (ρ/k)P<sub>k−1</sub>，从 P₀ 一路递推：<div class="calc">P₁ = ρP₀<br>P₂ = (ρ/2)P₁ = (ρ²/2!)P₀<br>P₃ = (ρ/3)P₂ = (ρ³/3!)P₀<br>⋯<br>P<sub>k</sub> = P₀ · ρ<sup>k</sup>/k!，　k ≤ m</div>')
  + S(8, '<b>(c)(ii) k ≥ m</b>：μ<sub>k</sub> = mμ，所以 P<sub>k</sub> = (ρ/m)P<sub>k−1</sub>。从 P<sub>m</sub> = P₀ρ<sup>m</sup>/m! 出发，再乘 (k − m) 次 ρ/m：<div class="calc">P<sub>k</sub> = P<sub>m</sub>(ρ/m)<sup>k−m</sup><br>= P₀ · (ρ<sup>m</sup>/m!) · ρ<sup>k−m</sup>/m<sup>k−m</sup><br>= P₀ · ρ<sup>k</sup>/(m! · m<sup>k−m</sup>)，　k ≥ m</div><br><b>自检</b>：k = m 时两式都等于 P₀ρ<sup>m</sup>/m! ✓。P₀ 由 ΣP<sub>k</sub> = 1 求出：P₀ = [Σ<sub>k=0</sub><sup>m−1</sup> ρ<sup>k</sup>/k! + ρ<sup>m</sup>/(m!(1 − ρ/m))]<sup>−1</sup>，其中几何级数收敛要求 ρ/m &lt; 1。再求 P(k ≥ m) 就得到附录里的 Erlang C 公式（附录的 A 就是这里的 ρ，附录的 ρ 是这里的 ρ/m）。')
  + '<div class="wans">(b) ≈ 132.3 E/小区（查表插值 132.28）；≈ 735 用户/km²；90 s　(c) P<sub>k</sub> = P₀ρ<sup>k</sup>/k!（k ≤ m），P₀ρ<sup>k</sup>/(m!m<sup>k−m</sup>)（k ≥ m）</div>'),

dict(id='y2526s2-q4a', paper=P, q='Q4(a)', marks=4, page='A', ch='ch10',
 topic='硬切换与软切换及各自使用的系统',
 en='''<p>4. (a) For terrestrial cellular systems there are two types of handovers. Describe the basic mechanisms of these two handovers and identify the types of cellular systems that deploy each of these two handovers respectively.</p>
<p class="marks">(4 Marks)</p>''',
 sol=S(1, '<b>硬切换（hard handover，break before make，先断后连）</b>（讲义 Part A p.154）：<br>• <b>机制</b>：先释放与旧基站的信道，再在新基站上建立新信道；任何时刻手机只连一个基站。<br>• <b>特点</b>：一次只维护一条链路，实现简单；但断开和接上之间有空档，通信会短暂中断；新小区没有空闲信道或切换失败时就会掉话（call dropping）。<br>• <b>使用系统</b>：<b>FDMA/TDMA 系统</b>，如 GSM、IS-136（以及 AMPS）。原因：相邻小区用不同的频率组，手机的收发机一次只能调在一个频率上，必须先离开旧频率才能换到新频率。')
  + S(2, '<b>软切换（soft handover，make before break，先连后断）</b>（p.155）：<br>• <b>机制</b>：先和新基站建立信道，新旧两条信道同时用于通信，确认新链路可靠后再断开旧的。<br>• <b>特点</b>：切换期间通信不中断；在小区边界上同时收两个基站的信号，有分集增益，边界性能改善。<br>• <b>使用系统</b>：<b>CDMA 系统</b>，如 IS-95、WCDMA、cdma2000。原因：CDMA 相邻小区用同一个频率、靠不同的码区分用户，手机不用换频就能同时和两个基站通信。')
  + '<div class="wans">硬切换：先断后连，GSM/IS-136；软切换：先连后断，IS-95/WCDMA/cdma2000</div>'),

dict(id='y2526s2-q4b', paper=P, q='Q4(b)', marks=8, page='C', ch='ch6',
 topic='MEO/LEO 卫星系统的四种切换',
 en='''<p>(b) In a satellite system with Medium Earth Orbit (MEO) or Low Earth Orbit (LEO) satellites, there could also be handovers in the system if the satellite acts as a base station. Briefly describe the 4 different types of handovers that can occur in this type of satellite system.</p>
<p class="marks">(8 Marks)</p>''',
 sol=S(1, '<b>背景</b>：MEO/LEO 不是同步轨道，卫星相对地面高速运动。卫星充当基站时，除了用户移动，卫星自己移动也会触发切换，所以共有 4 种（讲义 Part C p.40）。')
  + S(2, '<b>① 星内切换（intra-satellite handover）</b>：用户在<b>同一颗卫星</b>的覆盖区内，从一个扇区（点波束，spot beam）移到另一个扇区。原因：一颗卫星用多个点波束覆盖地面，每个波束相当于一个小区，跨波束就像蜂窝网里跨小区。')
  + S(3, '<b>② 星间切换（inter-satellite handover）</b>：用户从一颗卫星的覆盖区移到另一颗卫星的覆盖区，或者卫星自己飞走了，连接要交给下一颗卫星。LEO 轨道低、相对地面运动快，两地之间的通信通常要把信号从一颗卫星交给另一颗（p.17）；每颗星对一个用户只可见约 15–20 分钟，所以这种切换很频繁；MEO 轨道高，切换少得多（p.39）。')
  + S(4, '<b>③ 网关切换（gateway handover）</b>：卫星移动后离开了当前连接的地面网关（gateway），卫星与地面网络之间的链路要换到另一个网关。原因：网关是固定的地面站，卫星在动。')
  + S(5, '<b>④ 系统间切换（inter-system handover）</b>：在卫星系统和地面蜂窝系统之间切换，根据信号强度和 QoS 决定，属于不同类型网络之间的<b>垂直切换（vertical handover）</b>。例：用户进入有地面蜂窝覆盖的地区时从卫星切到蜂窝网，离开覆盖区时再切回卫星。')
  + '<div class="wans">星内、星间、网关、系统间（垂直）切换</div>'),

dict(id='y2526s2-q4c', paper=P, q='Q4(c)', marks=5, page='B', ch='ch5',
 topic='传感器网络的通信架构：节点多跳 → sink → 任务管理节点',
 en='''<p>(c) A sensor network is composed of many sensor nodes which are densely distributed to sense the environment. Briefly describe the communication architecture in the sensor networks to support the network operations. Describe briefly the communication architecture and show how the sensor nodes can relay the information back to the manager of the sensor network.</p>
<p class="marks">(5 Marks)</p>''',
 sol=S(1, '<b>① 传感器节点</b>（讲义 Part B p.57）：大量传感器节点散布在传感区域（sensor field）里，每个节点都能采集数据，也能把数据路由回<b>汇聚节点（sink）</b>。原因：单个节点的功率、计算能力和存储都很有限（p.56），只能做短距离通信，所以每个节点既是数据源，也要帮别人转发。')
  + S(2, '<b>② 多跳转发到 sink</b>：数据以<b>多跳、无基础设施（multi-hop, infrastructureless）</b>的方式，一个节点接一个节点地转发到 sink。原因：节点射程短，离 sink 远的节点必须靠中间节点中继；现场没有基站，只能用 ad hoc 方式组网；几段短距离传输也比一跳长距离传输更省电。')
  + S(3, '<b>③ sink → 管理者</b>：sink 再经<b>互联网或卫星</b>与<b>任务管理节点（task manager node）</b>通信。管理者（用户）在那里获取数据，也从那里反方向下发任务和查询。原因：sink 是传感网与外部网络之间的网关，而用户通常远离传感区域。')
  + S(4, '<b>示意</b>：传感器 A → 传感器 B → 传感器 C → … → Sink → Internet/卫星 → 任务管理节点（用户）。作图时画一串节点箭头指向 sink，标上 "multi-hop"。')
  + S(5, '<b>支撑网络运行的其他要素（加分）</b>：设计受可靠性、可扩展性、生产成本、工作环境、网络拓扑、硬件约束、传输介质和功耗影响（p.57）。协议栈分为物理层、数据链路层（MAC）、网络层、传输层、应用层，外加功耗管理、移动性管理、任务管理三个平面，负责监控各节点的能量、移动和任务分配（p.59）。')
  + '<div class="wans">传感器节点多跳转发 → Sink → Internet/卫星 → Task manager</div>'),

dict(id='y2526s2-q4d', paper=P, q='Q4(d)', marks=8, page='B', ch='ch7',
 topic='IoT 通信网络层的四个子层（同 2024-25 Q4(b)）',
 en='''<p>(d) In the core Internet of Things (IoT) functional stack, the communication network layer is structured with four sublayers. Describe the features of each of the sublayers.</p>
<p class="marks">(8 Marks)</p>''',
 sol=S(1, '和 2024-25 Q4(b) 是同一道题。<b>① 接入网子层（access network sublayer）</b>：IoT 网络的"最后一公里"，把智能物体接进网络，通常是无线技术，如 IEEE 802.11ah、802.15.4g、LoRa（讲义 Part B p.89）。为什么有这么多种：选哪种取决于通信距离（PAN、HAN、NAN、FAN、LAN、MAN、WAN）、一个采集小区里的物体数量、成本和功耗（p.95–96）；拓扑可以是点到点，或点到多点（星形、簇星、网状）（p.96–97）。')
  + S(2, '<b>② 网关与回传子层（gateways and backhaul sublayer）</b>：把一个区域内的多个智能物体汇聚到一个公共网关，网关再通过更长距离的介质把采集到的数据转发到头端中心站（headend）（p.89、p.98）。原因：物体射程短、功耗低，不能直接连到远处的中心，需要网关做不同介质之间的转换。物体可以静止或在小范围内移动，网关通常固定。')
  + S(3, '<b>③ 网络传输子层（network transport sublayer）</b>：用网络层和传输层协议（IP，UDP/TCP）把各种设备、各种介质连起来（p.90、p.98–99）。要求协议开放、标准化，能扩展到成千上万个传感器，并且安全。IP 满足这些要求，能嵌入各种物体、跑在低功耗、低带宽、高丢包的网络上；TCP 由网络保证可靠交付，UDP 把控制交给应用。')
  + S(4, '<b>④ IoT 网络管理子层（IoT network management sublayer）</b>：应用层协议，让头端应用和传感器（智能物体）交换数据（p.90、p.99）。例：基于 TCP 的 HTTP，传感器作为客户端连到 IoT 应用；WebSocket 是轻量的双向协议，适合低内存、低功耗、低带宽、高丢包的环境。')
  + '<div class="wans">Access network / Gateways &amp; backhaul / Network transport / IoT network management</div>',
 same='y2425s2-q4b'),
]
