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
 sol=S(1, '<b>(i) 取对数（化成 dB）</b>：P<sub>r</sub> = P<sub>t</sub>K d<sup>−γ</sup>ψ 是乘积，两边取 10 log₁₀，乘法变加法，幂变系数（10 log₁₀ d<sup>−γ</sup> = −10γ log₁₀ d）：<div class="calc">P<sub>r,dB</sub> = P<sub>t,dB</sub> + K<sub>dB</sub><br>　　　 − 10γ log₁₀ d + ψ<sub>dB</sub></div>其中 K<sub>dB</sub> = 10 log₁₀ K，ψ<sub>dB</sub> = 10 log₁₀ ψ。ψ 服从对数正态（log-normal）分布，所以 ψ<sub>dB</sub> ~ N(0, σ²<sub>ψdB</sub>)，是零均值高斯随机变量（讲义 Ch2 p.12）。')
  + S(2, '<b>(i) 写成路径损耗、画图</b>：路径损耗（path loss）= 发射功率 − 接收功率：<div class="calc">P<sub>L,dB</sub> = P<sub>t,dB</sub> − P<sub>r,dB</sub><br>　　 = −K<sub>dB</sub> + γ·(10 log₁₀ d) − ψ<sub>dB</sub></div>横轴取 x = 10 log₁₀ d（"距离的 dB"），纵轴 y = P<sub>L,dB</sub>，去掉随机项就是直线 y = −K<sub>dB</sub> + γx：<b>斜率 = γ</b>（距离每大 10 倍，x 加 10 dB，损耗加 10γ dB）；d = 1（x = 0）处的<b>截距 = −K<sub>dB</sub></b>（K<sub>dB</sub> 通常为负，如讲义 p.10 的 −26.67 dB，所以截距在横轴上方）。ψ<sub>dB</sub> 让实测点随机散在直线两侧。' + SVG_PL)
  + S(3, '<b>(ii) 写出中断概率</b>：中断（outage）= 接收功率低于门限 P<sub>min</sub>。P<sub>r,dB</sub> = 均值 μ + ψ<sub>dB</sub>，是高斯分布，标准差 σ = σ<sub>ψdB</sub>，σ² 就是题目要的 ψ<sub>dB</sub> 方差（讲义 Ch2 p.14–15）：<div class="calc">P<sub>out</sub> = P(P<sub>r,dB</sub> &lt; P<sub>min</sub>)<br>　 = P(ψ<sub>dB</sub> &lt; −(μ − P<sub>min</sub>))<br>　 = Q((μ − P<sub>min</sub>)/σ) = Q(10/σ)</div>最后一步用了高斯分布的对称性：P(ψ<sub>dB</sub> &lt; −x) = P(ψ<sub>dB</sub> &gt; x) = Q(x/σ)。题目给出 μ − P<sub>min</sub> = 10 dB。')
  + S(4, '<b>(ii) 查 Q 表反求 σ</b>：要求 Q(10/σ) &lt; 0.01。查 Q 表：Q(2.32) ≈ 0.0102，Q(2.33) ≈ 0.0099，插值得 Q⁻¹(0.01) ≈ 2.326。Q 是减函数，要 Q 值更小，自变量就要更大：<div class="calc">10/σ &gt; 2.326<br>σ &lt; 10/2.326 = 4.30 dB<br>σ² &lt; 4.30² = 18.5 dB²</div>验算：σ = 4.30 dB 时 10/σ = 2.326，Q(2.326) ≈ 0.0100，正好在 1% 边界上 ✓；σ 再大，中断就超过 1%。')
  + S(5, '<b>(iii) 频率维：平坦还是频率选择性</b>：比较 rms 时延扩展和符号时长（讲义 Ch2 p.33 经验法则：σ<sub>τ</sub>/T<sub>s</sub> &lt; 0.1 为平坦衰落）：<div class="calc">σ<sub>τ</sub>/T<sub>s</sub> = 0.01 ms / 1 ms = 0.01 &lt; 0.1</div>所以是<b>平坦衰落</b>（flat fading）：多径回波在 1% 个符号时长内就到齐，几乎没有符号间干扰（ISI），整个信号频谱经历相同的衰落。换到频域看：信号带宽约 1/T<sub>s</sub> = 1 kHz，相干带宽量级 1/σ<sub>τ</sub> = 100 kHz，远大于信号带宽，结论一样。')
  + S(6, '<b>(iii) 时间维：快还是慢</b>：信道冲激响应不随时间变化（time invariant）→ 没有多普勒扩展 → 相干时间 T<sub>c</sub> → ∞。符号时长 1 ms 远小于 T<sub>c</sub>，一个符号内幅度和相位都不变，所以是<b>慢衰落</b>（slow fading，讲义 Ch2 p.37）。<br>结论：<b>平坦慢衰落</b>（flat, slow fading）。两个维度要分开判断：频率维看时延扩展，时间维看多普勒扩展 / 相干时间。')
  + S(7, '<b>(iv) 推衰落余量公式</b>：瑞利信道 SNR 的 CDF 是 F(γ) = 1 − e<sup>−γ/γ̄<sub>R</sub></sup>。令 F(γ<sub>min</sub>) = ε，解出中断概率为 ε 时允许的最低 SNR（讲义 Ch2 p.51）：<div class="calc">γ<sub>min</sub> = γ̄<sub>R</sub> ln(1/(1 − ε))<br>C<sub>ε</sub> = log₂(1 + γ<sub>min</sub>)</div>AWGN 信道 C = log₂(1 + γ<sub>AWGN</sub>)。两者容量相等 ⇒ γ<sub>AWGN</sub> = γ̄<sub>R</sub> ln(1/(1 − ε))，所以衰落余量（fade margin）是瑞利信道要多给的平均 SNR：<div class="calc">FM = γ̄<sub>R,dB</sub> − γ<sub>AWGN,dB</sub><br>　 = 10 log₁₀[1 / ln(1/(1 − ε))]</div>')
  + S(8, '<b>(iv) 代入 ε = 0.1%</b>：ε = 0.001：<div class="calc">1/(1 − ε) = 1/0.999 = 1.001001<br>ln 1.001001 = 0.0010005<br>1/0.0010005 = 999.5<br>FM = 10 log₁₀ 999.5 = 30.0 dB</div>自检：ε 很小时 ln(1/(1 − ε)) ≈ ε，FM ≈ 10 log₁₀(1/ε) = 10 log₁₀ 1000 = 30 dB ✓。讲义例子 ε = 1% 时是 20 dB；中断要求严 10 倍，余量多 10 dB ✓。')
  + '<div class="wans">(ii) σ² &lt; 18.5 dB²（σ &lt; 4.3 dB）　(iii) 平坦、慢衰落　(iv) 衰落余量 ≈ 30 dB</div>'),

dict(id='y2324s2-q1b1', paper=P, q='Q1(b)(i)', marks='(b) 共 13', page='p2', ch='ch4',
 topic='DPSK 两支路选择分集 · 离散 SNR 分布求平均',
 en='''<p>(b) Diversity techniques can be used to lower the outage probability of a wireless system operating in a fading channel.</p>
<p>(i) A Differential Phase Shift Keying (DPSK) system uses a 2-branch Selection Diversity (SD) scheme to mitigate fading. The signal to noise ratio (SNR) of the received signal for each branch is assumed to be a discrete random variable with the following distribution:
<span class="eq">10 dB with a probability of 0.2;　12 dB with a probability of 0.8</span>
Determine the average SNR in dB of the received signals and the average symbol error probability of the SD scheme. Note: Symbol error probability of DPSK is ½e<sup>−SNR</sup>.</p>''',
 sol=S(1, '<b>dB 换线性</b>：DPSK 公式 ½e<sup>−SNR</sup> 里的 SNR 必须是线性值，用 γ = 10<sup>γ<sub>dB</sub>/10</sup>：<div class="calc">10 dB → 10<sup>1.0</sup> = 10<br>12 dB → 10<sup>1.2</sup> = 15.85</div>')
  + S(2, '<b>每支路接收信号的平均 SNR</b>：离散随机变量的均值 = Σ 取值 × 概率，在线性域算：<div class="calc">γ̄ = 0.2 × 10 + 0.8 × 15.85<br>　= 2 + 12.68 = 14.68<br>10 log₁₀ 14.68 = 11.67 dB</div>先线性平均再转 dB。直接平均 dB 值（0.2×10 + 0.8×12 = 11.6 dB）是错的：dB 是对数，对数的平均不等于平均的对数。')
  + S(3, '<b>SD 输出 SNR 的分布</b>：选择分集（selection diversity）输出 γ<sub>SD</sub> = max(γ₁, γ₂)（讲义 Ch4 p.11）。两支路独立，列出 4 种组合：<div class="calc">(10, 10)：0.2 × 0.2 = 0.04 → 输出 10 dB<br>(10, 12)：0.2 × 0.8 = 0.16 → 输出 12 dB<br>(12, 10)：0.8 × 0.2 = 0.16 → 输出 12 dB<br>(12, 12)：0.8 × 0.8 = 0.64 → 输出 12 dB</div>所以 P(γ<sub>SD</sub> = 10 dB) = 0.04，P(γ<sub>SD</sub> = 12 dB) = 0.16 + 0.16 + 0.64 = 0.96。检查：0.04 + 0.96 = 1 ✓。只有两支同时"差"，输出才差。')
  + S(4, '<b>SD 输出的平均 SNR</b>（顺带写出，方便对照）：<div class="calc">γ̄<sub>SD</sub> = 0.04 × 10 + 0.96 × 15.85<br>　= 0.40 + 15.21 = 15.61<br>10 log₁₀ 15.61 = 11.94 dB</div>比单支路的 11.67 dB 高约 0.27 dB。')
  + S(5, '<b>每种情况的误符号率</b>：P<sub>s</sub>(γ) = ½e<sup>−γ</sup>，γ 用线性值：<div class="calc">γ = 10：½e<sup>−10</sup> = ½ × 4.54×10⁻⁵ = 2.27×10⁻⁵<br>γ = 15.85：½e<sup>−15.85</sup> = ½ × 1.31×10⁻⁷ = 6.54×10⁻⁸</div>')
  + S(6, '<b>按概率加权求平均误符号率</b>：讲义 Ch4 p.23 的 P̄<sub>s</sub> = E[P<sub>s</sub>(γ)]，离散分布就是加权求和：<div class="calc">P̄<sub>s</sub> = 0.04 × 2.27×10⁻⁵ + 0.96 × 6.54×10⁻⁸<br>　= 9.08×10⁻⁷ + 6.28×10⁻⁸<br>　≈ 9.7×10⁻⁷</div>要对 P<sub>s</sub> 求平均，不能把平均 SNR 代进公式：½e<sup>−15.61</sup> ≈ 8.3×10⁻⁸，小了一个数量级多，是错的。')
  + S(7, '<b>对比（自检）</b>：不用分集（单支路）时 P̄<sub>s</sub> = 0.2 × 2.27×10⁻⁵ + 0.8 × 6.54×10⁻⁸ = 4.54×10⁻⁶ + 5.2×10⁻⁸ ≈ 4.6×10⁻⁶。SD 让误符号率降到约 1/4.7。原因：误码几乎全来自 10 dB 那种情况，分集把它出现的概率从 0.2 压到 0.04（正好 1/5）✓。')
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
 sol=S(1, '<b>(ii) 空间复用原理</b>（spatial multiplexing，讲义 Ch4 p.30）：把数据拆成 N 路，N 个<b>不同</b>的符号在同一频带、同一时刻从 N 根发射天线同时发出，速率变成单天线的 N 倍。每个符号只发一次、没有冗余，所以<b>没有分集增益</b>，衰落信道里误码性能可能较差。')
  + S(2, '<b>(ii) 收发天线数的关系</b>：每根接收天线收到的都是 N 路信号的混合，y = Hx + v，相当于 M 个方程、N 个未知符号。要解出 N 路数据流，方程数不能少于未知数，所以需要 <b>M ≥ N</b> 根接收天线（讲义 Ch4 p.30）。')
  + S(3, '<b>(ii) 最大复用增益</b>：高 SNR 时 MIMO 容量 C → min(N, M) log₂ SNR（讲义 Ch4 p.31–32），所以 r<sub>max</sub> = min(N, M)：<div class="calc">N = 3，M = 5<br>r<sub>max</sub> = min(3, 5) = 3</div>数据流数被 3 根发射天线限制住（M = 5 ≥ 3，满足上一步的条件 ✓）；多出的 2 根接收天线不能再加流，只能让检测更可靠。')
  + S(4, '<b>(iii) 逐个元素算 X X<sup>H</sup></b>：正交 STBC 的定义（讲义 Ch5 p.22、p.27）是 X X<sup>H</sup> = (|s₁|² + |s₂|²) I。X 的两行 r₁ = (s₁, −s₂*)，r₂ = (s₂, s₁*)；(X X<sup>H</sup>)<sub>ij</sub> = r<sub>i</sub>·r<sub>j</sub><sup>H</sup>（第 j 行取共轭，对应相乘再求和）：<div class="calc">(1,1)：s₁s₁* + (−s₂*)(−s₂*)* = |s₁|² + |s₂|²<br>(2,2)：s₂s₂* + s₁*(s₁*)* = |s₂|² + |s₁|²<br>(1,2)：s₁s₂* + (−s₂*)(s₁*)*<br>　　 = s₁s₂* − s₂*s₁ = 0<br>(2,1)：(1,2) 的共轭 = 0</div>')
  + S(5, '<b>(iii) 结论和数字自检</b>：<div class="calc">X X<sup>H</sup> = (|s₁|² + |s₂|²) I</div>而且 X 的元素都是 s₁、s₂ 及其共轭的线性函数，满足讲义 p.27 的两个条件，<b>是正交 STBC</b>。它就是讲义 Alamouti 矩阵的转置：讲义行 = 时隙、列 = 天线；本题行 = 天线、列 = 时隙（天线 1 先发 s₁ 再发 −s₂*，天线 2 先发 s₂ 再发 s₁*，和讲义 p.21 完全一样）。自检：取 s₁ = 1 + j，s₂ = 2 − j，算得 X X<sup>H</sup> = 7I，而 |s₁|² + |s₂|² = 2 + 5 = 7 ✓。')
  + S(6, '<b>(iv) Alamouti 有分集增益</b>：接收端线性处理后得到 ỹ = Fs + ṽ，两个符号分到两个独立的 AWGN 子信道，每个子信道 SNR = (|h₁|² + |h₂|²)E{|s|²}/σ²（讲义 Ch5 p.26）。SNR 由两条独立衰落增益之<b>和</b>决定，只有 h₁、h₂ 同时深衰落才会出错，概率远小于单条路径深衰落，所以有分集。分集阶数：2 发 1 收为 2，2 发 M 收为 2M，即<b>满分集</b> N × M（p.27）。对比：发射端不知道信道、只用固定权重时，SNR 和单条 |h₁|² 同分布，没有分集（p.18）；Alamouti 不需要发射端知道信道就拿到了分集。代价：没有阵列增益（array gain），SNR 比接收端 MRC 低 3 dB（p.30，发射功率被两根天线平分）。')
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
 sol=S(1, '<b>(i) 展开求和式</b>：n = 1, 2, 3 逐项写出：<div class="calc">r[i] = h[1]m[i] + h[2]m[i−1]<br>　　 + h[3]m[i−2] + w[i]</div>第 i 个采样里除了想要的 m[i]，还混进了前两个符号 m[i−1]、m[i−2]，这就是符号间干扰（ISI）。原因是信道相当于一个有记忆的线性滤波器（讲义 Ch6 p.4），冲激响应比一个符号长。只要 h[2]、h[3] 不全为 0，就有 ISI。')
  + S(2, '<b>(ii) 对照 Z 变换系数</b>：按这个求和式，h[n] 乘的是延迟 n − 1 个符号的 m，对应 Z<sup>−(n−1)</sup>：<div class="calc">H(Z) = h[1] + h[2]Z⁻¹ + h[3]Z⁻²<br>　　 = 1 + 0·Z⁻¹ + 0.6Z⁻²</div>逐项对照：<b>h[1] = 1，h[3] = 0.6</b>（h[2] = 0）。于是 r[i] = m[i] + 0.6m[i−2] + w[i]。检查：H(1) = 1 + 0.6 = 1.6 = h[1] + h[2] + h[3] ✓。')
  + S(3, '<b>(iii) 级联响应</b>：滤波后的总 Z 变换是两者相乘（讲义 Ch6 p.22 的 Q(Z) = H(Z)C(Z)）：<div class="calc">C(Z)H(Z) = (1 − 0.6Z⁻²)(1 + 0.6Z⁻²)<br>　= 1 + 0.6Z⁻² − 0.6Z⁻² − 0.36Z⁻⁴<br>　= 1 − 0.36Z⁻⁴</div>平方差公式：Z⁻² 项抵消了，但生出一个 Z⁻⁴ 项。')
  + S(4, '<b>(iii) 时域写出判决变量</b>：C(Z) 对应 y[i] = r[i] − 0.6r[i−2]，代入 r：<div class="calc">y[i] = [m[i] + 0.6m[i−2] + w[i]]<br>　 − 0.6[m[i−2] + 0.6m[i−4] + w[i−2]]<br>　= m[i] − 0.36m[i−4] + w′[i]</div>其中 w′[i] = w[i] − 0.6w[i−2]（噪声也经过了滤波器）。结果和上一步的 1 − 0.36Z⁻⁴ 一致 ✓。ISI 没完全消掉，但系数从 0.6 降到 0.36，而且被推到 4 个符号之外。')
  + S(5, '<b>(iii) 判决规则</b>：m[i] 等概取 ±1，噪声零均值、对称，最优门限在两个取值的中点 0（等先验时的 ML 判决）。残余 ISI 当作噪声，逐符号判决：<div class="calc">m̂[i] = +1，若 y[i] ≥ 0<br>m̂[i] = −1，若 y[i] &lt; 0</div>')
  + S(6, '<b>(iv) 滤波后的噪声方差</b>：w[i] 和 w[i−2] 是独立的噪声样本，独立变量之和的方差相加，系数要平方：<div class="calc">σ′² = 0.3 × (1² + 0.6²)<br>　 = 0.3 × 1.36 = 0.408<br>σ′ = √0.408 = 0.639</div>滤波器把噪声功率放大了 1.36 倍，这是线性均衡减小 ISI 的代价。')
  + S(7, '<b>(iv) 分情况求条件误码率</b>：设发 m[i] = +1，则 y = 1 − 0.36m[i−4] + w′。m[i−4] 等概为 ±1，信号到门限 0 的距离：<div class="calc">m[i−4] = +1：1 − 0.36 = 0.64<br>m[i−4] = −1：1 + 0.36 = 1.36</div>出错 = 噪声把 y 推到 0 以下，概率为 Q(距离/σ′)：<div class="calc">Q(0.64/0.639) = Q(1.00) ≈ 0.158<br>Q(1.36/0.639) = Q(2.13) ≈ 0.0166</div>')
  + S(8, '<b>(iv) 平均并自检</b>：两种情况各占 ½：<div class="calc">P<sub>b</sub> = ½ × 0.158 + ½ × 0.0166<br>　= 0.079 + 0.0083 ≈ 0.087</div>发 −1 时由对称性结果相同，所以平均误码率 ≈ 0.087（查表用 Q(1.00) = 0.1587 得 0.0876，同样可以）。对比：不加滤波器时 r = m[i] + 0.6m[i−2] + w，σ = √0.3 = 0.548，P<sub>b</sub> = ½Q(0.4/0.548) + ½Q(1.6/0.548) = ½Q(0.73) + ½Q(2.92) ≈ 0.117。滤波器让误码率从 0.117 降到 0.087 ✓；完全没有 ISI 时是 Q(1/0.548) = Q(1.83) ≈ 0.034，这是下限。')
  + '<div class="wans">(ii) h[1] = 1，h[3] = 0.6　(iii) y[i] = m[i] − 0.36m[i−4] + w′[i]，按符号判决　(iv) P<sub>b</sub> ≈ 0.087</div>'),

dict(id='y2324s2-q2b', paper=P, q='Q2(b)', marks=12, page='p2', ch='ch7',
 topic='OFDM 子载波数 · 子信道增益 H<sub>k</sub> · 保护间隔与功率损失',
 en='''<p>(b) A wireless system operates with a bandwidth of 1 MHz and implements an OFDM scheme with N sub-carriers. The fading channel has a coherence bandwidth of 500 kHz and a sampled channel impulse response of {1, −0.6, 0.2}.</p>
<p>(i) Determine the value of N if the bandwidth of each OFDM sub-carrier is to be half of the coherence bandwidth.</p>
<p>(ii) Determine the channel gain coefficient values for the N sub-channels.</p>
<p>(iii) Using the simplified formula, T = 1/B, where T is the signal symbol duration and B is the signal bandwidth, determine the total OFDM block duration if a Guard interval of 1 microsecond is added.</p>
<p>(iv) For the question in 2(b) part (iii) above, determine the power loss due to the addition of the guard interval.</p>
<p class="marks">(12 Marks)</p>''',
 sol=S(1, '<b>(i) 子载波带宽 → N</b>：每个子载波带宽取相干带宽的一半，这样每个子载波都比 B<sub>c</sub> 窄，经历平坦衰落：<div class="calc">Δf = B<sub>c</sub>/2 = 500 kHz / 2 = 250 kHz<br>N = B/Δf = 1000 kHz / 250 kHz = 4</div>')
  + S(2, '<b>(ii) 写出子信道增益公式</b>：讲义 Ch7 p.15：H<sub>k</sub> = Σ<sub>i=0</sub><sup>L−1</sup> h<sub>i</sub> e<sup>−j2πik/N</sup>，k = 1, …, N。这里 h₀ = 1，h₁ = −0.6，h₂ = 0.2，L = 3，N = 4。记 W = e<sup>−j2πk/4</sup> = e<sup>−jπk/2</sup>，则 H<sub>k</sub> = 1 − 0.6W + 0.2W²，先列出 W 和 W²：<div class="calc">k = 1：W = −j，W² = −1<br>k = 2：W = −1，W² = 1<br>k = 3：W = j，W² = −1<br>k = 4：W = 1，W² = 1</div>')
  + S(3, '<b>(ii) 逐个代入</b>：<div class="calc">H₁ = 1 − 0.6(−j) + 0.2(−1) = 0.8 + 0.6j<br>H₂ = 1 − 0.6(−1) + 0.2(1) = 1.8<br>H₃ = 1 − 0.6(j) + 0.2(−1) = 0.8 − 0.6j<br>H₄ = 1 − 0.6(1) + 0.2(1) = 0.6</div>模值：|H₁| = |H₃| = √(0.8² + 0.6²) = 1，|H₂| = 1.8，|H₄| = 0.6（k = 4 时 W = 1，和 k = 0 一样，所以 H₄ = H₀：H<sub>k</sub> 以 N 为周期）。每个子信道只剩一个复数增益 r<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + w<sub>k</sub>（p.17），这就是 OFDM 把频率选择性信道变成 N 个平坦子信道的意思。')
  + S(4, '<b>(ii) 自检</b>：① h 是实数，所以 H₃ = H₁*（共轭对称）✓；② 帕塞瓦尔定理（Parseval）：<div class="calc">(1/N)Σ|H<sub>k</sub>|² = (1 + 3.24 + 1 + 0.36)/4 = 1.4<br>Σh<sub>i</sub>² = 1 + 0.36 + 0.04 = 1.4 ✓</div>')
  + S(5, '<b>(iii) OFDM 块长</b>：按 T = 1/B，原始符号时长 T<sub>s</sub> = 1/(1 MHz) = 1 µs。一个 OFDM 块装 N 个符号，再加保护间隔（讲义 Ch7 p.18：块长 = NT<sub>s</sub> + T<sub>G</sub>）：<div class="calc">NT<sub>s</sub> = 4 × 1 µs = 4 µs<br>T<sub>block</sub> = NT<sub>s</sub> + T<sub>G</sub> = 4 + 1 = 5 µs</div>检查：4 µs 也等于子载波带宽的倒数 1/(250 kHz) ✓。')
  + S(6, '<b>(iv) 保护间隔的功率损失</b>：保护间隔不携带新信息，花在它上面的能量白白浪费（讲义 Ch7 p.18）：<div class="calc">损失 = 10 log₁₀[(NT<sub>s</sub> + T<sub>G</sub>)/(NT<sub>s</sub>)]<br>　= 10 log₁₀(5/4) = 10 × 0.0969<br>　≈ 0.97 dB</div>换个角度：有用能量只占 4/5 = 80%，10 log₁₀ 0.8 = −0.97 dB ✓。')
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
 sol=S(1, '<b>假设</b>：① 固定、均匀信道分配（UFCA），每小区信道数相同；② blocked calls cleared（被阻塞的呼叫直接丢弃、不排队）→ 用 Erlang B；③ 399 条全是话务信道（题目说 traffic channels，不扣控制信道）；④ 用户在服务区内均匀分布，忙时每个用户的话务量相同。')
  + S(2, '<b>(i) 每簇、每小区信道数</b>：一个簇正好把全部信道用一遍，所以每簇 399 条；N<sub>c</sub> = 7 个小区平分：<div class="calc">399 / 7 = 57 条/小区<br>（57 × 7 = 399 ✓，整除）</div>')
  + S(3, '<b>(i) 查 Erlang B 表</b>：Erlang B 公式 B = (A<sup>M</sup>/M!) / Σ<sub>k=0</sub><sup>M</sup>(A<sup>k</sup>/k!)（讲义 Part A p.118–119）。查表 M = 57 行、B = 1% 列：<div class="calc">A ≈ 44.2 Erlang / 小区</div>验算：把 A = 44.22、M = 57 代回公式，B = 0.0100 ✓。这就是 GoS 允许的每小区最大提供话务量（offered traffic）。')
  + S(4, '<b>(ii) 每用户话务量</b>：A<sub>u</sub> = 呼叫率 × 平均时长，时长换成小时：<div class="calc">A<sub>u</sub> = 0.9 次/h × (90/3600) h<br>　= 0.9 × 0.025 = 0.0225 Erlang</div>')
  + S(5, '<b>(ii) 每小区用户数</b>：小区内 m 个用户产生的话务量 = m × 0.0225 E。令它等于小区能支持的 44.22 E：<div class="calc">m = 44.22 / 0.0225 = 1965.3<br>→ 1965 用户/小区</div>向下取整，保证阻塞不超过 1%。每小区用户产生的话务量 = 1965 × 0.0225 ≈ 44.2 E。')
  + S(6, '<b>(iii) 面积 → 半径</b>：每小区面积 = 用户数 / 用户密度，再用六边形面积公式反求 R：<div class="calc">A<sub>ce</sub> = 1965.3 / 720 = 2.730 km²<br>(3√3/2)R² = 2.598R² = 2.730<br>R² = 2.730 / 2.598 = 1.051<br>R = √1.051 ≈ 1.03 km</div>验算：2.598 × 1.025² × 720 ≈ 1965 用户 ✓。')
  + S(7, '<b>(iv) 集群增益</b>：讲义 p.122：集群增益（trunking gain）= 在给定 GoS 下一组信道能服务的用户数 ÷ 信道数：<div class="calc">T<sub>g</sub> = 1965 / 57 ≈ 34.5 用户/信道</div>顺带：集群效率 = 44.22/57 = 77.6%（每条信道平均有 77.6% 的时间在忙）。')
  + S(8, '<b>(v) 120° 扇区：重新计算</b>：每小区 57 条信道分给 3 个扇区，每扇区 57/3 = 19 条，各自成为独立的信道池（一个扇区的用户借不到另一个扇区的空闲信道）。查 Erlang B（M = 19，B = 1%）：<div class="calc">A ≈ 11.23 E/扇区<br>每小区 3 × 11.23 = 33.69 E<br>m = 33.69 / 0.0225 = 1497 用户<br>面积 = 1497 / 720 = 2.080 km²<br>R = √(2.080 / 2.598) = √0.800 ≈ 0.89 km<br>T<sub>g</sub> = 1497 / 57 ≈ 26.3</div>')
  + S(9, '<b>(v) 观察与评论</b>：信道总数不变，但被切成 3 个小池，集群效率下降：57 条合用能承载 44.2 E，切开只有 33.7 E，少了约 24%（1 − 33.69/44.22 = 0.238）。所以每个小区覆盖的面积变小（R 从 1.03 降到 0.89 km），同样的服务区要多约 31% 的基站（44.22/33.69 = 1.31），集群增益从 34.5 降到 26.3。对运营商的好处在 SIR：第一层同频干扰从 6 个降到 2 个，N = 7、n = 4 时约 24.5 dB（讲义 p.145），比全向的 18.7 dB 高约 6 dB。有了这个余量才能改用更小的簇 N（p.144），每小区信道变多，扇区化才真正换来容量；在 N 不变的前提下单纯加扇区，只换来干扰改善，付出的是覆盖、集群效率和更多切换（p.146）。')
  + '<div class="wans">57 条/小区，A ≈ 44.2 E；m ≈ 1965；R ≈ 1.03 km；T<sub>g</sub> ≈ 34.5；扇区化后 R ≈ 0.89 km，T<sub>g</sub> ≈ 26.3</div>',
 note='Erlang B 的 A 值用公式精确算出（44.22、11.23），和考卷附表读数相同到小数点后一位。'),

dict(id='y2324s2-q3b', paper=P, q='Q3(b)', marks=5, page='A', ch='ch1',
 topic='FDMA / TDMA / CDMA 及系统举例',
 en='''<p>(b) Multiple access schemes are important features in mobile cellular systems as they allow many users to share the limited spectrum simultaneously. There are three basic multiple access schemes used in the 1G-3G mobile cellular systems. Briefly describe each of the multiple access schemes and give an example of an existing mobile cellular system for each scheme.</p>
<p class="marks">(5 Marks)</p>''',
 sol=S(1, '<b>FDMA</b>（频分多址，frequency division multiple access）：把频谱切成许多等宽的窄带信道，每个用户在通话期间独占一个频率信道（讲义 Part A p.7）。用户靠<b>频率</b>区分、互不重叠，所以不需要时间同步；但信道整个通话期间都被占着，空闲时也不能给别人。例：1G 的 <b>AMPS</b>（30 kHz 信道，p.15–16）。')
  + S(2, '<b>TDMA</b>（时分多址）：一个载波按时间切成等长时隙，循环分给几个用户，每人只在自己的时隙里突发发送（p.7）。用户靠<b>时间</b>区分；发送不连续，所以需要帧同步和保护时间。例：2G 的 <b>GSM</b>（200 kHz 载波、每帧 8 个时隙，实际是 FDMA + TDMA 组合，p.22–23）、IS-136。')
  + S(3, '<b>CDMA</b>（码分多址）：所有用户同时占用同一段宽带频谱，每人分配一个不同的扩频码（正交或低相关），接收端用自己的码做相关运算解出自己的信号，其他用户的信号看起来像噪声（p.7）。用户靠<b>码</b>区分，频率和时间都共享。例：2G 的 <b>IS-95</b>，3G 的 <b>WCDMA</b>、cdma2000（p.26、p.155）。')
  + S(4, '<b>一句话对比</b>：FDMA 切频率、TDMA 切时间、CDMA 切码。1G 模拟系统用 FDMA；2G 数字系统用 TDMA（GSM）或 CDMA（IS-95）（p.18）；3G 基于宽带 CDMA。')
  + '<div class="wans">FDMA–AMPS；TDMA–GSM；CDMA–IS-95/WCDMA</div>'),

dict(id='y2324s2-q4ab', paper=P, q='Q4(a)(b)', marks=13, page='B', ch='ch7',
 topic='简化 IoT 架构的两个并行栈 · 为什么要引入雾计算',
 en='''<p>4. (a) For Internet of Things (IoT), the simplified IoT architecture consists of two parallel stacks, i.e., the Management and Compute Stack and Core IoT Functional Stack. Briefly describe the major components in each of the two stacks.</p>
<p class="marks">(7 Marks)</p>
<p>(b) Discuss the necessity to introduce Fog Computing into the simplified IoT architecture.</p>
<p class="marks">(6 Marks)</p>''',
 sol=S(1, '<b>(a) 总体框架</b>（讲义 Part B p.86）：简化 IoT 架构是两个并排的三层栈。左边 Core IoT Functional Stack 回答"数据怎么从物体传到应用"，右边 IoT Data Management and Compute Stack 回答"数据在哪里处理"，两栈逐层对应。')
  + S(2, '<b>(a) 核心功能栈（Core IoT Functional Stack，三层）</b>（p.89–90）：<br>① <b>"Things" 层</b>（传感器、执行器等智能物体）：物理设备要适应部署环境的约束（供电、体积、移动性），同时还要能提供所需的数据；<br>② <b>通信网络层</b>：物体不能自给自足时要和外部系统通信，分四个子层——<b>接入网</b>（最后一公里，802.11ah、802.15.4g、LoRa 等）、<b>网关与回传</b>（把一片区域内的设备汇聚到网关，再用长距离链路送回中心站）、<b>网络传输</b>（IP、UDP/TCP，要开放、标准、能扩展到海量设备）、<b>IoT 网络管理</b>（HTTP、WebSocket 等应用协议，让头端应用和传感器交换数据，p.99）；<br>③ <b>应用与分析层</b>：处理收集的数据，既做数据分析、网络分析和智能决策，也反过来控制物体，让它们调整行为或参数（p.100–101）。')
  + S(3, '<b>(a) 数据管理与计算栈（Data Management and Compute Stack）</b>（p.103、p.110–113）：决定数据在哪里过滤、汇聚、存储和分析，三个层次对应核心栈：<br>① <b>边缘（edge / mist）</b>：在传感器或设备本身做最基本的过滤和判断（新一代终端已有这样的算力）；<br>② <b>雾（fog）</b>：在靠近终端的网关、路由器等网络设备上做实时处理；<br>③ <b>云（cloud / 数据中心）</b>：集中存储、历史数据、大数据分析。<br>分工原则：越要求实时的数据越靠近边缘处理，不急的数据送云（p.113）。')
  + S(4, '<b>(b) 只用云端会出什么问题</b>（p.104–105）：数据全部直接送云处理时——<br>• 最后一公里 IoT 网络带宽很有限，海量数据挤不进去；<br>• 来回时延大，失去实时响应能力；<br>• 网关的回传链路常依赖 3G/LTE 甚至卫星，不可靠；<br>• 回传上的数据量太大，数据中心难以接收、存储和处理；<br>• 大数据越来越大，实时分析和响应几乎不可能。')
  + S(5, '<b>(b) 雾计算怎么解决</b>（p.106–109）：把数据处理分散到尽量靠近 IP 网络边缘的地方（任何有计算、存储和联网能力的设备都能当雾节点）：<br>• 就近分析 → <b>降低时延</b>，能实时反应；<br>• 只把结果或摘要往上送 → <b>卸载核心网</b>大量流量，<b>压缩/精简数据</b>；<br>• <b>敏感数据留在本地</b>网络里；<br>• 雾节点地理上靠近传感器，有<b>上下文/位置感知</b>，形成分布式的边缘控制回路，不必等云端指令。<br>雾和边缘不取代云，而是云的"第一道防线"，三层配合工作（p.111）。')
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
 sol=S(1, '<b>推导：列假设，写 S/I</b>（讲义 Part A p.88）：只算第一层 6 个同频干扰（第二层太远，忽略）；手机在小区边缘，离本基站 R；6 个干扰基站都近似在距离 D；接收功率 ∝ d<sup>−n</sup>：<div class="calc">S/I = R<sup>−n</sup> / (6D<sup>−n</sup>)<br>　= (D/R)<sup>n</sup>/6 = Q<sup>n</sup>/6</div>')
  + S(2, '<b>推导：代入 Q 和 n = 4</b>：六边形几何给出同频复用因子 Q = D/R = √(3N)（p.78）。n = 4 时 Q⁴ = (3N)² = 9N²：<div class="calc">S/I = 9N²/6 = 1.5N²<br>SIR<sub>dB</sub> = 10 log₁₀ 1.5 + 10 log₁₀ N²<br>　= 1.76 + 20 log₁₀ N</div>其中 10 log₁₀ 1.5 = 1.761，10 log₁₀ N² = 20 log₁₀ N。证毕。')
  + S(3, '<b>(i) 代入 N = 7</b>：<div class="calc">20 log₁₀ 7 = 20 × 0.8451 = 16.90 dB<br>SIR = 1.76 + 16.90 = 18.66 dB</div>直接验算：Q = √21 = 4.583，Q⁴/6 = 441/6 = 73.5，10 log₁₀ 73.5 = 18.66 dB ✓。<b>评论</b>：刚好高于语音质量所需的约 18 dB（讲义 p.89），所以 7 小区复用最常用。但简化模型把 6 个干扰都放在 D，偏乐观；最坏情况（p.91）在 n = 4 时只有 17.27 dB，低于 18 dB。')
  + S(4, '<b>(ii) 反求 n</b>：要 SIR ≥ 20 dB，换成线性值 10<sup>20/10</sup> = 100，两边取 log₁₀：<div class="calc">Q<sup>n</sup>/6 ≥ 100 → Q<sup>n</sup> ≥ 600<br>n log₁₀ Q ≥ log₁₀ 600<br>log₁₀ Q = ½ log₁₀ 21 = ½ × 1.3222 = 0.6611<br>n ≥ 2.7782 / 0.6611 ≈ 4.20</div>验算：4.583<sup>4.2</sup> = 597.9，597.9/6 = 99.7 → 19.99 dB ≈ 20 dB ✓。n 比 4 大，信号随距离衰减更快，远处的干扰就更弱，SIR 才够。')
  + S(5, '<b>(iii) 最坏情况（全向天线）</b>：手机在小区角上，2 个干扰在 D − R，2 个在 D，2 个在 D + R（p.91），除以 R 后就是 Q − 1、Q、Q + 1。n = 4.2：<div class="calc">(Q − 1)<sup>4.2</sup> = 3.583<sup>4.2</sup> = 212.6<br>Q<sup>4.2</sup> = 4.583<sup>4.2</sup> = 597.9<br>(Q + 1)<sup>4.2</sup> = 5.583<sup>4.2</sup> = 1370</div><div class="calc">分母 = 2/212.6 + 2/597.9 + 2/1370<br>　= 0.00941 + 0.00334 + 0.00146<br>　= 0.01421<br>SIR = 1/0.01421 = 70.4 → 18.5 dB</div>')
  + S(6, '<b>(iii) 评论</b>：18.5 dB &lt; 20 dB，没达到要求。原因是两个干扰只隔 D − R，单这两项就占分母的约 2/3（0.00941/0.01421 = 0.66）。所以按简化模型定出的 n，在最坏位置不够用。')
  + S(7, '<b>(iv) 120° 扇区</b>：每个扇区天线只朝 120° 方向发射，第一层只剩 2 个干扰，最坏情况距离为 D 和 D + 0.7R（讲义 p.145）：<div class="calc">Q + 0.7 = 5.283，5.283<sup>4.2</sup> = 1086<br>SIR = 1/(1/597.9 + 1/1086)<br>　= 1/(0.001672 + 0.000921)<br>　= 1/0.002593 = 385.7 → 25.9 dB</div>')
  + S(8, '<b>(iv) 和 (iii) 比较并评论</b>：25.9 − 18.5 = 7.4 dB，扇区化后满足 20 dB 还有约 5.9 dB 余量（讲义 p.145：n = 4 时为 24.5 dB；n 变大后更高，趋势一致 ✓）。代价：每扇区只有 1/3 的信道，集群效率下降；切换次数增多，系统复杂度增加（p.146）。好处：可以用这个余量减小簇 N，提高频率复用和容量（p.144）。')
  + '<div class="wans">(i) 18.66 dB　(ii) n ≈ 4.2　(iii) 18.5 dB　(iv) 25.9 dB</div>'),
]
