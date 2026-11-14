# -*- coding: utf-8 -*-
# 知识讲解 + 详细解析 for EE6129 past finals 2025-26 S1 and S2 (group exB).
# Every number is checked by check_exB.py (run with /usr/bin/python3).

XPL = {

# ===================================================================== 2025-26 S1
'y2526s1-q1a': {'title': '知识讲解 + 详细解析：BPSK 星座、条件高斯与 Q(2)', 'zh': '''
<h4><span class="st">知识讲解</span>星座图、维数和距离</h4>
<p>星座图（signal constellation）就是把每一个可能发送的符号画成空间里的一个点。需要几个正交归一的基函数（orthonormal basis functions）才能表示全部符号，星座就是几维（讲义第 3 章 p.4–8）。本题 s 只取 +1 或 −1，两个点都在同一条实轴上，一个基函数就够，所以是 <b>1 维</b>，这就是 BPSK（也可以看成 2-PAM）。</p>
<p>两点之间的欧氏距离 d 决定抗噪声的能力：d 越大，噪声越难把一个点"推"到另一个点那一边。老师课上强调：要会判断一个调制方式的星座是几维，"signal constellation"这个术语要记住；AWGN 噪声的方差在数值上等于 N₀/2。</p>
<h4><span class="st">知识讲解</span>为什么 y 是高斯，均值和方差怎么来</h4>
<p>给定 s 以后，s 是常数，y = s + w 只是把零均值的高斯噪声 w 整体平移了 s。第 1b 章的两条性质：E[c + X] = c + E[X]；Var[c + X] = Var[X]（常数没有波动，不贡献方差）。所以 y | s ~ N(s, σ²)。高斯分布完全由均值和方差两个数确定，算出这两个数再代进题目给的 PDF 公式就行。</p>
<h4><span class="st">知识讲解</span>误码率和 Q 函数</h4>
<p>Q(z) 是标准正态变量大于 z 的概率（右尾面积）。对均值 μ、标准差 σ 的高斯变量，P(X &gt; μ + a) = Q(a/σ)。老师要求掌握的技巧：把"出错"整理成"噪声 &lt; −距离"，再由对称性写成 Q(距离/σ)。二进制等概信号、门限放在中点时，P<sub>b</sub> = Q(d/(2σ))，d/2 就是每个点到门限的距离。</p>
<h4><span class="st">详细解析</span>(i)(ii)(iii) 逐步</h4>
<ol>
<li><b>(i)</b> 画一条横轴，标出 −1、0、+1，在 ±1 处画两个实心点。维数 = 1；距离 d = |(+1) − (−1)| = 2。</li>
<li><b>(ii)</b> 先把方差换成标准差：σ² = 0.25 → σ = 0.5。PDF 指数的分母是 2σ² = 0.5，前面的系数 1/√(2πσ²) = 1/√(0.5π) ≈ 0.798。
<div class="calc">s = +1：E[y] = 1，Var[y] = 0.25，p(y | s = +1) = 0.798 e<sup>−(y−1)²/0.5</sup><br>s = −1：E[y] = −1，Var[y] = 0.25，p(y | s = −1) = 0.798 e<sup>−(y+1)²/0.5</sup></div>
如果要不带条件的 y 的 PDF，用全概率：p(y) = ½p(y | +1) + ½p(y | −1)，是两个"钟形"的混合。</li>
<li><b>(iii)</b> 发 +1 时出错 ⇔ y ≤ 0 ⇔ 1 + w ≤ 0 ⇔ w ≤ −1：
<div class="calc">P(w ≤ −1) = P(w ≥ 1) = Q(1/σ) = Q(1/0.5) = Q(2) ≈ 0.0228</div>
发 −1 时出错 ⇔ w &gt; 1，概率同样是 Q(2)。两个符号等概：P<sub>b</sub> = ½Q(2) + ½Q(2) = Q(2) ≈ 0.0228。</li>
</ol>
<p><b>查表</b>：Q 函数表查 z = 2.00，得 0.02275（老师说 Q 函数表一定会考到，正查、反查都要会）。<b>自检</b>：用 BPSK 公式 Q(√(2γ<sub>b</sub>))，E<sub>b</sub> = 1，N₀ = 2σ² = 0.5，γ<sub>b</sub> = E<sub>b</sub>/N₀ = 2，得 Q(√4) = Q(2)，两条路结果一致。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>把方差 0.25 当成 σ 代进 Q：Q(1/0.25) = Q(4) 是错的，要用 σ = 0.5。</li>
<li>PDF 指数写成 −(y−1)²/0.25，忘了分母是 2σ²。</li>
<li>(ii) 只写"是高斯"，不写均值、方差的数值，也不写出 PDF。</li>
<li>维数答成 2：只要所有点都在一条直线上就是 1 维。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) The constellation has two points, s = +1 and s = −1, on the real axis (sketch). Only one basis function is needed, so the constellation is one-dimensional. The distance between the two signal points is d = |1 − (−1)| = 2.</p>
<p>(ii) Given s, y = s + w is a constant plus a zero-mean Gaussian random variable, so y is Gaussian with E[y | s] = s and Var[y | s] = σ² = 0.25. For s = +1: mean = 1, variance = 0.25. For s = −1: mean = −1, variance = 0.25. Hence p(y | s = ±1) = (1/√(0.5π)) exp[−(y ∓ 1)²/0.5].</p>
<p>(iii) σ = √0.25 = 0.5. P(error | s = +1) = P(y ≤ 0 | s = +1) = P(w ≤ −1) = Q(1/0.5) = Q(2). By symmetry, P(error | s = −1) = Q(2). As the two symbols are equally likely, P<sub>b</sub> = Q(2) ≈ 0.0228.</p></div>
<div class="ans">一句话：y 是"以 ±1 为中心、方差 0.25 的高斯"，门限在 0，离门限的距离 1 = 2σ，所以误码率 Q(2) ≈ 0.023。</div>
'''},

'y2526s1-q1b1': {'title': '知识讲解 + 详细解析：MRC 平均 SNR 与分集增益', 'zh': '''
<h4><span class="st">知识讲解</span>分集合并、MRC、阵列增益和分集增益</h4>
<p><b>分集（diversity）</b>：同一个信号经过几条独立衰落的支路（branch）到达接收端，几条同时深衰落的概率很小，把它们合并起来就能抗衰落（第 4 章 p.2–3）。</p>
<p><b>最大比合并（MRC，Maximal Ratio Combining）</b>：每一路乘上自己信道增益的共轭再相加（p.15），相当于匹配滤波。结果是<b>合并后的瞬时 SNR 等于各支路 SNR 之和</b>：γ<sub>Σ</sub> = γ₁ + γ₂ + …（p.16）。因为求平均是线性运算，平均输出 SNR 也等于各支路平均 SNR 之和；两路同分布时就是 2γ̄。</p>
<p><b>两个性能指标</b>（p.27，老师说这两个公式"简单、要记住"）：</p>
<ul>
<li>阵列增益（array gain）g ≈ γ̄<sub>Σ</sub>/γ̄：合并后的平均 SNR 比合并前提高了几倍。</li>
<li>分集增益（diversity order）d：高 SNR 下 P̄<sub>e</sub> ≈ γ̄<sup>−d</sup>，取对数得 d ≈ −log₁₀P̄<sub>e</sub> / log₁₀γ̄。这里的 γ̄ 是<b>合并器输入</b>的平均 SNR。d 表示 SNR 每增加 10 倍，误码率下降 10<sup>d</sup> 倍（曲线有多陡）。</li>
</ul>
<p>讲义 p.28 还说：M 支路接收时 d ≤ M，满分集时 d = M。</p>
<h4><span class="st">详细解析</span>一步一步算</h4>
<ol>
<li><b>dB 换线性</b>（SNR 是功率比，平均必须在线性域做）：10<sup>x/10</sup>
<div class="calc">11 dB → 10<sup>1.1</sup> = 12.59<br>12 dB → 10<sup>1.2</sup> = 15.85<br>13 dB → 10<sup>1.3</sup> = 19.95</div></li>
<li><b>平均输入 SNR</b>：按概率加权（离散分布的期望 E[X] = Σx·p(x)）：
<div class="calc">γ̄ = 0.2 × 12.59 + 0.5 × 15.85 + 0.3 × 19.95 = 2.518 + 7.924 + 5.986 = 16.43<br>10 log₁₀(16.43) = 12.16 dB</div></li>
<li><b>MRC 平均输出 SNR</b>：每一次的输出都是 γ₁ + γ₂，取平均就是 γ̄ + γ̄：
<div class="calc">γ̄<sub>Σ</sub> = 2 × 16.43 = 32.86 → 15.17 dB；g = 32.86/16.43 = 2（3 dB）</div></li>
<li><b>分集增益</b>：P̄<sub>e</sub> = 2×10⁻⁴，γ̄ 用输入的 16.43。计算器提示：log₁₀(2×10⁻⁴) = 0.301 − 4 = −3.699。
<div class="calc">d ≈ 3.699 / log₁₀(16.43) = 3.699 / 1.216 ≈ 3.04 ≈ 3.0</div></li>
</ol>
<p><b>合理性检查</b>：d ≈ 3 比支路数 2 还大，和 p.28 的 d ≤ M 不一致。原因是 d 的公式是"高 SNR 近似"，用一个误码率点反算出来的数不是严格的渐近斜率。考试按讲义 p.27 的公式算即可，有时间可以加一句说明（见下面的英文模板最后一句）。现有解答和 Practice 4 Q2 的官方答案都是这样处理的。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>直接平均 dB 值：0.2×11 + 0.5×12 + 0.3×13 = 12.1 dB，方法错（老师说没做 dB ↔ 线性换算会扣分）。</li>
<li>d 用输出 SNR 32.86 代入，得到 3.699/1.517 ≈ 2.44，和讲义定义不符。</li>
<li>MRC 平均输出写成 max 或平均值：MRC 是相加，选择分集（SD）才是取最大。</li>
<li>结果不写 dB 值或不写单位。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Converting to linear scale: 11 dB = 12.59, 12 dB = 15.85, 13 dB = 19.95.</p>
<p>Average receiver input SNR: γ̄ = 0.2(12.59) + 0.5(15.85) + 0.3(19.95) = 16.43 (12.16 dB).</p>
<p>For MRC, the output SNR is the sum of the branch SNRs, so the average output SNR is γ̄<sub>Σ</sub> = 2γ̄ = 32.86 (15.17 dB), i.e. an array gain of 2 (3 dB).</p>
<p>Diversity gain: P̄<sub>e</sub> ≈ γ̄<sup>−d</sup>, where γ̄ is the average combiner input SNR. d ≈ −log₁₀(2×10⁻⁴)/log₁₀(16.43) = 3.699/1.216 ≈ 3.0. (This is a high-SNR approximation obtained from a single error-rate point.)</p></div>
<div class="ans">一句话：先换线性再平均得 16.43（12.2 dB），MRC 相加得 32.86（15.2 dB），d 用输入 SNR 算得约 3.0。</div>
'''},

'y2526s1-q1b2': {'title': '知识讲解 + 详细解析：SIMO 分集与 MIMO 并行信道', 'zh': '''
<h4><span class="st">知识讲解</span>MIMO 的输入输出关系和 SIMO</h4>
<p>平坦衰落下，N 根发射天线、M 根接收天线的 MIMO 信道写成 y<sub>m</sub> = Σ<sub>n</sub> h<sub>m,n</sub>x<sub>n</sub> + v<sub>m</sub>，矩阵形式 y = Hx + v（第 5 章 p.5–6）。"输入"指发送信号的个数，"输出"指接收信号的个数。<b>SIMO</b>（Single-Input Multiple-Output）就是 N = 1、M ≥ 2：一个发送符号，多个接收信号（p.11–12）。</p>
<p><b>SIMO 怎么得到分集</b>（p.13–14）：接收端做线性合并 x̂ = w₁*y₁ + w₂*y₂，选 w = αh 使输出 SNR 最大，得到 SNR<sub>max</sub> = E{|x|²}(|h₁|² + |h₂|²)/σ²。它和 |h₁|² + |h₂|² 成正比：即使 h₁ 很小，只要 h₂ 大，仍能正确检测。若 h₁、h₂ 统计独立，两者同时很小的概率远小于其中一个很小的概率，这就是接收分集。这个接收机就是第 4 章的 MRC，老师建议两章一起学。</p>
<h4><span class="st">知识讲解</span>MIMO 容量为什么是并行信道之和</h4>
<p>容量公式 C = B log₂det(I + HPH<sup>H</sup>/σ²)（p.32–35）。对 HPH<sup>H</sup> 做特征分解 UΛU<sup>H</sup>，再用 det(I + AB) = det(I + BA) 和 U<sup>H</sup>U = I，就化成题目给的 B log₂det{I + Λ/σ²}（考试会给前面这部分，让你推剩下的）。Λ 是对角阵，对角元素是特征值 λ<sub>i</sub>，非零的个数 r = rank(H) ≤ min(N, M)。老师强调：容量是 r 条子信道之和，<b>r 是秩，不是 N × M</b>。</p>
<h4><span class="st">详细解析</span>(ii) 要点展开</h4>
<ol>
<li><b>为什么是 SIMO</b>：方程里只有一个发送符号 s（单输入），却有两个接收信号 y₁、y₂（多输出），所以是 1 × 2 的 SIMO，即一根发射天线、两根接收天线。</li>
<li><b>两条支路各自独立</b>：y₁、y₂ 带的是同一个 s，但经过不同的信道增益 h₁、h₂，噪声 v₁、v₂ 也互不相关。只要两根接收天线间距足够大，h₁ 和 h₂ 就是独立衰落的。</li>
<li><b>合并</b>：用 MRC，z = h₁*y₁ + h₂*y₂ = (|h₁|² + |h₂|²)s + h₁*v₁ + h₂*v₂，输出 SNR 与 |h₁|² + |h₂|² 成正比。</li>
<li><b>为什么能抗衰落</b>：设每一路深衰落的概率是 p，两路同时深衰落的概率是 p²。例如 p = 0.1 时只有 0.01，链路可靠性大大提高，分集阶数为 2。</li>
</ol>
<h4><span class="st">详细解析</span>(iii) 化简步骤</h4>
<ol>
<li>Λ = diag(λ₁, …, λ<sub>r</sub>)，所以 I + Λ/σ² 也是对角阵，对角元素是 1 + λ<sub>i</sub>/σ²。</li>
<li>对角阵的行列式 = 对角元素之积：det{I + Λ/σ²} = Π(1 + λ<sub>i</sub>/σ²)。</li>
<li>对数把乘积变成求和：log₂Π(…) = Σlog₂(…)。</li>
<li>每一项 B log₂(1 + λ<sub>i</sub>/σ²) 正是一条 SNR 为 λ<sub>i</sub>/σ² 的单发单收信道的香农容量。</li>
</ol>
<div class="calc">C = B log₂ Π<sub>i=1</sub><sup>r</sup>(1 + λ<sub>i</sub>/σ²) = Σ<sub>i=1</sub><sup>r</sup> B log₂(1 + λ<sub>i</sub>/σ²)</div>
<p><b>数字小例子</b>：两条特征子信道 λ₁/σ² = 3、λ₂/σ² = 1。det = (1 + 3)(1 + 1) = 8，log₂8 = 3 bit/s/Hz；分开算 log₂4 + log₂2 = 2 + 1 = 3 bit/s/Hz，两者相等。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>(ii) 只说"有两根天线"，没写"同一个符号、独立衰落、合并后同时深衰落概率小"这条逻辑链。</li>
<li>忘了独立衰落的前提（天线间距足够大）。</li>
<li>(iii) 子信道个数写成 N × M；应是 r = rank(H) ≤ min(N, M)。</li>
<li>只写结论，不写"对角阵行列式 = 对角元素之积"这一步。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(ii) There is only one transmitted symbol s (single input) but two received signals y₁ and y₂ (multiple outputs), each through its own channel gain h₁, h₂ and independent noise v₁, v₂. Hence it is a 1 × 2 SIMO system with one transmit antenna and two receive antennas.</p>
<p>The same symbol s reaches the receiver through two different paths. If the receive antennas are sufficiently separated, h₁ and h₂ fade independently, so the probability that both are in a deep fade at the same time is much smaller than that of a single path. The receiver combines the two signals, e.g. by MRC: z = h₁*y₁ + h₂*y₂ = (|h₁|² + |h₂|²)s + h₁*v₁ + h₂*v₂. The output SNR is proportional to |h₁|² + |h₂|², so s can still be detected reliably when one gain is small as long as the other is large. This gives a diversity order of 2.</p>
<p>(iii) Since Λ = diag(λ₁, …, λ<sub>r</sub>) is diagonal, I + Λ/σ² is diagonal and its determinant is the product of its diagonal elements:</p>
<p>C = B log₂ Π<sub>i=1</sub><sup>r</sup>(1 + λ<sub>i</sub>/σ²) = Σ<sub>i=1</sub><sup>r</sup> B log₂(1 + λ<sub>i</sub>/σ²).</p>
<p>Each term is the Shannon capacity of a SISO channel with SNR λ<sub>i</sub>/σ². Therefore the MIMO channel is equivalent to r = rank(H) ≤ min(N, M) independent parallel sub-channels, and its capacity is the sum of their capacities.</p></div>
<div class="ans">一句话：一发两收、独立衰落、合并后同时深衰落的概率很小，就是 SIMO 分集；对角阵行列式是乘积，取 log 变成求和，就是 MIMO = r 条并行信道。</div>
'''},

'y2526s1-q2a': {'title': '知识讲解 + 详细解析：ISI 误码率与噪声增强', 'zh': '''
<h4><span class="st">知识讲解</span>离散 ISI 信道模型</h4>
<p>信道有多径时，一个符号的能量会"拖尾"到后面几个采样时刻，造成符号间干扰（ISI，Inter-Symbol Interference）。按符号间隔采样后，信道就是一组抽头系数 h[1], h[2], …, h[L]，接收信号是消息序列和抽头的卷积加噪声（第 6 章 p.22）：r[n] = Σh[i]m[n − i + 1] + w(n)。信道的 Z 变换 H(Z) = h[1] + h[2]Z⁻¹ + …，Z⁻¹ 表示延迟一个符号，所以 <b>H(Z) 有几项，L 就是几</b>。</p>
<h4><span class="st">知识讲解</span>有残余 ISI 时怎么求误码率</h4>
<p>讲义 p.27–28：判决变量 = 期望信号 + ISI 项 + 高斯噪声。ISI 项取决于前面发的符号，是离散随机变量。做法：<b>先固定 ISI 的取值</b>，求条件误码率 Q((q₀ + ISI)/σ)；<b>再对 ISI 所有可能取值求平均</b>。和第 3 章的思路一样，只多了一层平均。</p>
<h4><span class="st">知识讲解</span>均衡器为什么放大噪声</h4>
<p>均衡器 C(Z) 是一个 FIR 滤波器，它不仅作用在信号上，也作用在噪声上（p.21、p.25）：w′(n) = Σc<sub>j</sub>w(n − j)。各个 w 独立、方差都是 σ²，独立变量之和的方差 = 各项方差之和，系数要平方：σ′² = σ²Σc<sub>j</sub>²。主抽头为 1 时，只要还有别的非零抽头，Σc<sub>j</sub>² 就大于 1，这就是"噪声增强"（p.41）。老师说均衡这一章要会三件事：用 Z 变换写信道和均衡器、迫零系数（长除法）、算噪声功率。</p>
<h4><span class="st">详细解析</span>(i) 信道长度</h4>
<div class="calc">H(Z) = 1 + 0.3Z⁻¹ → h[1] = 1，h[2] = 0.3 → L = 2<br>r[n] = m[n] + 0.3m[n−1] + w(n)</div>
<h4><span class="st">详细解析</span>(ii) 不均衡、直接判决</h4>
<p>σ = √0.36 = 0.6。由对称性只看 m[n] = +1（发 −1 的结果相同）。干扰 0.3m[n−1] 等概为 +0.3 或 −0.3：</p>
<div class="tw"><table class="mini"><thead><tr><th>m[n−1]</th><th>r[n] 的均值</th><th>出错条件</th><th>条件误码率</th></tr></thead><tbody>
<tr><td>+1（概率 ½）</td><td>1 + 0.3 = 1.3</td><td>w &lt; −1.3</td><td>Q(1.3/0.6) = Q(2.17) = 0.0151</td></tr>
<tr><td>−1（概率 ½）</td><td>1 − 0.3 = 0.7</td><td>w &lt; −0.7</td><td>Q(0.7/0.6) = Q(1.17) = 0.1217</td></tr>
</tbody></table></div>
<div class="calc">P<sub>e</sub> = ½(0.0151 + 0.1217) = 0.0684 ≈ 0.068</div>
<p><b>对比</b>：没有 ISI 时 P<sub>e</sub> = Q(1/0.6) = Q(1.67) ≈ 0.0478。ISI 时好时坏，但"坏"的那一半（0.1217）拉高了平均，所以总体变差。</p>
<h4><span class="st">详细解析</span>(iii) 均衡器输出噪声</h4>
<ol>
<li>噪声经过 C(Z)：w′(n) = w(n) − c₁w(n−1) + c₂w(n−2)。</li>
<li>三项独立，方差相加，系数平方（负号平方后消失）：
<div class="calc">Var[w′] = σ²(1 + c₁² + c₂²) = 0.36(1 + c₁² + c₂²)</div></li>
<li>c₁ &gt; 0、c₂ &gt; 0，所以 c₁² + c₂² &gt; 0，Var[w′] &gt; 0.36，噪声方差增大。</li>
</ol>
<p><b>举个具体的例子</b>：这个信道的迫零均衡器 1/(1 + 0.3Z⁻¹) 用长除法取前三项，正好是 1 − 0.3Z⁻¹ + 0.09Z⁻²（c₁ = 0.3，c₂ = 0.09，和题目的形式一致）。此时输出噪声方差 = 0.36 × (1 + 0.09 + 0.0081) = 0.36 × 1.0981 ≈ 0.395，比 0.36 大约 10%；而级联后 H(Z)C(Z) = 1 + 0.027Z⁻³，ISI 只剩 0.027。ISI 少了，噪声多了，这就是均衡的代价。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>σ 写成 0.36：Q 里除的是标准差 0.6。</li>
<li>只算一种 ISI 情况，忘了两种各乘 ½ 再相加。</li>
<li>(iii) 系数不平方，写成 σ²(1 − c₁ + c₂)；或者忘了"各项独立"这个前提。</li>
<li>L 答成 1（只数延迟）：L 是抽头个数。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) H(Z) = 1 + 0.3Z⁻¹ has two taps, h[1] = 1 and h[2] = 0.3, so L = 2 and r[n] = m[n] + 0.3m[n−1] + w(n).</p>
<p>(ii) σ = √0.36 = 0.6. By symmetry, consider m[n] = +1. The ISI term 0.3m[n−1] is +0.3 or −0.3 with equal probability.<br>If m[n−1] = +1: P(e) = P(w &lt; −1.3) = Q(1.3/0.6) = Q(2.17) = 0.0151.<br>If m[n−1] = −1: P(e) = P(w &lt; −0.7) = Q(0.7/0.6) = Q(1.17) = 0.1217.<br>Average P<sub>e</sub> = ½(0.0151 + 0.1217) ≈ 0.068 (compared with Q(1.67) ≈ 0.048 without ISI).</p>
<p>(iii) The noise also passes through the equalizer: w′(n) = w(n) − c₁w(n−1) + c₂w(n−2). Since the noise samples are independent with variance σ², Var[w′] = σ²(1 + c₁² + c₂²) = 0.36(1 + c₁² + c₂²). Because c₁ &gt; 0 and c₂ &gt; 0, Var[w′] &gt; 0.36, i.e. the equalizer increases the noise variance (noise enhancement).</p></div>
<div class="ans">一句话：L 是抽头数 2；ISI ±0.3 分两种情况求 Q 再平均得 0.068；噪声过均衡器后方差乘 (1 + c₁² + c₂²)，一定变大。</div>
'''},

'y2526s1-q2b': {'title': '知识讲解 + 详细解析：OFDM 子载波数、速率与正交性', 'zh': '''
<h4><span class="st">知识讲解</span>OFDM 的设计思路</h4>
<p>单载波高速传输时，信号带宽 B 大于相干带宽 B<sub>c</sub>，就是频率选择性衰落，会产生 ISI。OFDM（正交频分复用）的办法是：把可用带宽 B 切成 N 个窄的子载波，每个子载波带宽 Δf = B/N（第 7 章 p.5–8）。只要 <b>Δf &lt; B<sub>c</sub></b>，每个子载波看到的都是平坦衰落。</p>
<p>代价是每个子载波上的符号变慢：子载波符号时长 T = 1/Δf = NT<sub>S</sub>（T<sub>S</sub> = 1/B 是不用 OFDM 时的符号时长）。符号变长后，时延扩展 T<sub>D</sub> 只占它的一小部分；再在每个 OFDM 块前面加保护间隔 T<sub>G</sub> ≥ T<sub>D</sub>（p.17–18），块与块之间的 ISI 就完全消掉。保护间隔不传新数据，所以有效速率要用块长 T + T<sub>G</sub> 来算。</p>
<p><b>子载波为什么不互相干扰</b>：子载波频率间隔正好是 1/T，在一个符号期 T 内，任意两个不同子载波的乘积积分为 0（正交，p.7、p.13）。所以接收端用第 n 个相关器只能"看到"第 n 个子载波。老师说 OFDM 的数学相对简单。</p>
<h4><span class="st">详细解析</span>(i) 最少子载波数</h4>
<div class="calc">要求 500/N &lt; 30 kHz → N &gt; 500/30 = 16.7 → N<sub>min</sub> = 17</div>
<p>检查：N = 17 时 Δf = 500/17 = 29.4 kHz &lt; 30 kHz，满足；N = 16 时 31.25 kHz &gt; 30 kHz，不满足。</p>
<h4><span class="st">详细解析</span>(ii) N = 50 的有效速率</h4>
<ol>
<li>子载波带宽：Δf = 500/50 = 10 kHz（&lt; 30 kHz，平坦）。</li>
<li>子载波符号时长（题目说 T = 1/B）：T = 1/10 kHz = 100 µs，远大于 T<sub>D</sub> = 10 µs。</li>
<li>为消除时延扩展的 ISI，加保护间隔 T<sub>G</sub> = T<sub>D</sub> = 10 µs，块长 = 110 µs。</li>
<li>每个块传 50 个 4-QAM 符号，每个符号 log₂4 = 2 bit，共 100 bit：
<div class="calc">R<sub>eff</sub> = 100 bit / 110 µs ≈ 909 kbit/s</div></li>
</ol>
<p>对比：不计保护间隔是 100 bit / 100 µs = 1 Mbit/s；有效速率是它的 100/110 = 90.9%。（课外补充：同时还有 10 log₁₀(110/100) ≈ 0.41 dB 的功率损失，公式在 p.18，本题没问。）</p>
<h4><span class="st">详细解析</span>(iii) 相关器输出 = s<sub>n</sub></h4>
<ol>
<li>第 n 个相关器：把 r(t) 乘以 (1/√T)e<sup>−j2πnt/T</sup>，在一个符号期 [0, T] 内积分（T = T<sub>OFDM</sub>）。</li>
<li>代入 x(t)，常数 (1/√T)·(1/√T) = 1/T 提出来，求和与积分交换顺序，s<sub>k</sub> 在一个符号期内是常数，也提出来：
<div class="calc">(1/T) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub> ∫₀<sup>T</sup> e<sup>j2π(k−n)t/T</sup> dt</div></li>
<li>k = n：被积函数 = e⁰ = 1，积分 = T。</li>
<li>k ≠ n：在 [0, T] 内正好转了 (k − n) 整圈，积分 = T(e<sup>j2π(k−n)</sup> − 1)/(j2π(k − n)) = 0。</li>
<li>所以求和里只剩 k = n 一项：(1/T)·s<sub>n</sub>·T = s<sub>n</sub>(t)。噪声项另算（相关后仍是零均值高斯）。</li>
</ol>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>(i) N 不取整或向下取整成 16。</li>
<li>(ii) 忘了保护间隔，答 1 Mbit/s；"effective"就是要扣掉保护间隔。</li>
<li>(ii) 4-QAM 每个符号是 2 bit，不是 4 bit。</li>
<li>(iii) 只写 k = n 的情况，没写 k ≠ n 积分为 0（正交性），证明不完整。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) For flat fading, each sub-carrier bandwidth must be smaller than the coherence bandwidth: 500/N &lt; 30 kHz, so N &gt; 16.7. The minimum number of carriers is N = 17.</p>
<p>(ii) With N = 50, the sub-carrier bandwidth is Δf = 500/50 = 10 kHz, so the symbol duration on each sub-carrier is T = 1/Δf = 100 µs. A guard interval T<sub>G</sub> ≥ T<sub>D</sub> = 10 µs is added to remove ISI, so each OFDM block lasts 110 µs. Each block carries 50 × log₂4 = 100 bits. The effective bit rate is 100/(110 µs) ≈ 909 kbit/s (1 Mbit/s if the guard interval is ignored).</p>
<p>(iii) The output of the n-th correlator is (1/√T)∫₀<sup>T</sup> x(t)e<sup>−j2πnt/T</sup>dt = (1/T)Σ<sub>k</sub> s<sub>k</sub>∫₀<sup>T</sup> e<sup>j2π(k−n)t/T</sup>dt. For k = n the integral equals T; for k ≠ n it is the integral of a complex exponential over an integer number of periods, which is zero (orthogonal sub-carriers). Hence the output is (1/T)·s<sub>n</sub>·T = s<sub>n</sub>(t): only the n-th symbol remains and the other sub-carriers cause no interference.</p></div>
<div class="ans">一句话：子载波带宽小于相干带宽 → N ≥ 17；N = 50 时块长 100 + 10 µs，传 100 bit，有效速率约 909 kbit/s；子载波正交，相关器只留下 s<sub>n</sub>。</div>
'''},

'y2526s1-q3a': {'title': '知识讲解 + 详细解析：小区数、信道数与频谱效率', 'zh': '''
<h4><span class="st">知识讲解</span>蜂窝规划里的几个基本量</h4>
<ul>
<li><b>六边形小区面积</b>：半径 R（中心到顶点，也等于边长）的正六边形面积 = (3√3/2)R² ≈ 2.598R²。</li>
<li><b>信道数</b>：可用频谱扣掉保护带（guard band，防止相邻系统干扰、不能用来传信号），再除以每条信道的带宽。题目直接给了"全双工信道带宽 30 kHz"，一条全双工信道就占 30 kHz，不用再除以 2。</li>
<li><b>控制信道</b>（control channel）用来建立呼叫、传信令，不承载话音；小区容量通常指<b>话务信道</b>（traffic channel）数。</li>
<li><b>簇（cluster）</b>：N 个相邻小区分完全部信道，簇与簇之间重复使用（频率复用，Part A p.78–81）。均匀固定分配时，每小区分到 1/N。</li>
<li><b>频谱效率</b>（spectral efficiency，Part A p.38–40）：每 MHz 频谱、每 km² 面积上能提供几条信道。公式 η = (B<sub>w</sub>/B<sub>c</sub>)/(B<sub>w</sub>·A<sub>c</sub>·N) = 1/(B<sub>c</sub>·A<sub>c</sub>·N)，B<sub>c</sub> 是信道间隔（MHz），A<sub>c</sub> 是小区面积（km²），N 是簇大小。老师说这个公式"要试着记住"，本题 (iv) 就考了。</li>
</ul>
<h4><span class="st">详细解析</span>(i) 小区数</h4>
<div class="calc">A<sub>cell</sub> = 2.598 × 2² = 10.39 km²<br>小区数 = 1500 / 10.39 = 144.3 → 145 个</div>
<p>为什么向上取整：144 个小区盖不满 1500 km²，必须再加一个。</p>
<h4><span class="st">详细解析</span>(ii) 不复用时的信道数</h4>
<div class="calc">可用带宽 = 25 000 kHz − 40 kHz = 24 960 kHz<br>信道数 = 24 960 / 30 = 832 条</div>
<p>"without frequency reuse"就是整个系统一共有多少条不同的信道。</p>
<h4><span class="st">详细解析</span>(iii) 小区容量</h4>
<div class="calc">话务信道 = 832 − 18 = 814 条<br>每小区 = 814 / 9 = 90.4 → 90 条话务信道</div>
<p>向下取整：半条信道不能用。如果把控制信道也算进去，是 832/9 ≈ 92 条；写清楚自己的口径即可。</p>
<h4><span class="st">详细解析</span>(iv) 频谱效率</h4>
<div class="calc">B<sub>c</sub> = 30 kHz = 0.03 MHz<br>η = 1/(0.03 × 10.39 × 9) = 1/2.806 ≈ 0.356 channels/MHz/km²</div>
<p><b>用定义自检</b>：系统总信道数 = 每小区 832/9 = 92.44 条 × 144.3 个小区 ≈ 13 344 条，除以 (25 MHz × 1500 km²) = 37 500，得 0.356，一致。讲义公式里 B<sub>w</sub> 上下约掉，所以用 25 MHz 还是扣掉保护带后的带宽，结果都是 0.356。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>忘了扣 40 kHz 保护带（得 833 条）。</li>
<li>把 30 kHz 当成单向信道，又除以 2。</li>
<li>小区容量不扣控制信道，或者不取整。</li>
<li>η 的单位：B<sub>c</sub> 要用 MHz（0.03），面积用 km²；答案要写单位 channels/MHz/km²（老师说答案要写单位）。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) Area of one hexagonal cell = (3√3/2)R² = 2.598 × 2² = 10.39 km². Number of cells = 1500/10.39 = 144.3, so about 145 cells are needed to cover the area.</p>
<p>(ii) Usable spectrum = 25 MHz − 40 kHz = 24 960 kHz. Number of full-duplex channels without frequency reuse = 24 960/30 = 832 channels.</p>
<p>(iii) Traffic channels = 832 − 18 control channels = 814. Cell capacity = 814/9 = 90.4, i.e. 90 traffic channels per cell.</p>
<p>(iv) Spectral efficiency η = (B<sub>w</sub>/B<sub>c</sub>)/(B<sub>w</sub>A<sub>c</sub>N) = 1/(B<sub>c</sub>A<sub>c</sub>N) = 1/(0.03 MHz × 10.39 km² × 9) ≈ 0.356 channels/MHz/km².</p></div>
<div class="ans">一句话：面积 10.39 km² → 145 个小区；(25 000 − 40)/30 = 832 条；扣 18 条控制信道再 ÷9 得 90 条/小区；η = 1/(B<sub>c</sub>A<sub>c</sub>N) ≈ 0.356 channels/MHz/km²。</div>
'''},

'y2526s1-q3b': {'title': '知识讲解 + 详细解析：Erlang C 查表与通话时长', 'zh': '''
<h4><span class="st">知识讲解</span>话务量、Erlang B 和 Erlang C</h4>
<p><b>话务量</b>（traffic intensity）A = λH，单位 Erlang：λ 是单位时间的呼叫次数，H 是平均通话时长（holding time）（Part A p.104、p.115）。一个用户每小时打 λ<sub>u</sub> 次、每次 H 小时，他的话务量 A<sub>u</sub> = λ<sub>u</sub>H。1 Erlang 相当于一条信道被一直占满。</p>
<p>所有信道都忙时，新呼叫怎么办？两种模型：</p>
<div class="tw"><table class="mini"><thead><tr><th></th><th>Erlang B</th><th>Erlang C</th></tr></thead><tbody>
<tr><td>新呼叫遇到全忙</td><td>直接被拒绝（blocked calls cleared）</td><td>排队等待（blocked calls delayed）</td></tr>
<tr><td>题目给的概率</td><td>阻塞概率 GoS</td><td>呼叫被延迟（要排队）的概率</td></tr>
<tr><td>讲义</td><td>Part A p.118–119</td><td>Part A p.125–126（Queued Model）</td></tr>
</tbody></table></div>
<p>考试附录给 Erlang B 表和 C 表，老师说实际都是<b>查表</b>，并提醒先确认用对表。表里没有的信道数用<b>线性插值</b>（p.127）：A = A₁ + (M − M₁)(A₂ − A₁)/(M₂ − M₁)。</p>
<h4><span class="st">详细解析</span>(i) 每小区话务量</h4>
<ol>
<li>每小区信道数 = 1001/9 = 111.2 → 111 条（向下取整，半条信道不能用）。</li>
<li>题目说"Erlang C system"、概率 5%，所以查 Erlang C 表的 5% 列。</li>
<li>表在 100 条以上每 5 条一档，在 110 和 115 之间插值。按公式算出的表值约为 A(110) ≈ 92.5、A(115) ≈ 97.1（以考场附录为准）：
<div class="calc">A(111) ≈ 92.5 + (111 − 110)/(115 − 110) × (97.1 − 92.5) = 92.5 + 0.92 ≈ 93.4 Erlang/小区</div></li>
</ol>
<h4><span class="st">详细解析</span>(ii) 每 km² 用户数</h4>
<div class="calc">每小区用户数 = A / A<sub>u</sub> = 93.44 / 0.03 ≈ 3114 用户<br>每 km² = 3114 / 4 ≈ 779 用户/km²</div>
<h4><span class="st">详细解析</span>(iii) 平均通话时长</h4>
<div class="calc">A<sub>u</sub> = λ<sub>u</sub> × H → H = 0.03 / 1.5 = 0.02 小时 = 0.02 × 3600 = 72 秒</div>
<p><b>合理性检查</b>：72 秒一次通话、每小时 1.5 次，每小时打电话 108 秒，占 3%，正好是 0.03 Erlang。题目给的 3500 km² 三问都用不到，它可以用来算总小区数 3500/4 = 875 个，全系统约 3114 × 875 ≈ 272 万用户。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>用了 Erlang B 表：题目明确是 Erlang C（排队）。</li>
<li>信道数 111.2 不取整就去查表，或者不会插值直接取 110 或 115 那一行。</li>
<li>λ 是"每小时"，H 算出来是小时，要换成秒；答案要写单位。</li>
<li>用户数 = 话务量 ÷ 每用户话务量，别乘反了。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) Channels per cell = 1001/9 = 111.2, i.e. 111 channels. From the Erlang C table with a delay probability of 5%, interpolating between M = 110 (A ≈ 92.5 E) and M = 115 (A ≈ 97.1 E): A ≈ 92.5 + (1/5)(97.1 − 92.5) ≈ 93.4 Erlangs per cell.</p>
<p>(ii) Users per cell = 93.4/0.03 ≈ 3114 users. Cell area = 4 km², so the user density ≈ 3114/4 ≈ 779 users/km².</p>
<p>(iii) A<sub>u</sub> = λH, so H = A<sub>u</sub>/λ = 0.03/1.5 = 0.02 h = 72 s.</p></div>
<div class="ans">一句话：111 条信道查 Erlang C 表 5% 并插值得约 93.4 E/小区，÷0.03 ÷4 得约 779 用户/km²，H = 0.03/1.5 小时 = 72 秒。</div>
'''},

'y2526s1-q3c': {'title': '知识讲解 + 详细解析：固定与动态信道分配', 'zh': '''
<h4><span class="st">知识讲解</span>为什么要讲信道分配</h4>
<p>频谱有限，用户很多。信道分配（channel assignment）决定"哪个小区可以用哪些信道"，分得好，同样的频谱能接更多的呼叫（Part A p.92）。两种基本方法：固定分配（FCA，Fixed Channel Assignment）和动态分配（DCA，Dynamic Channel Assignment）。</p>
<h4><span class="st">知识讲解</span>FCA：预先固定分好</h4>
<ul>
<li>每个小区（基站）预先分到一组固定的信道（p.92）。</li>
<li>小区里的呼叫只能用<b>本小区</b>空闲的信道；本小区的信道全忙，新呼叫就被阻塞，<b>即使邻区有空闲信道也不能用</b>（p.94 的例子）。</li>
<li>均匀 FCA（UFCA）：簇内每个小区分到相同数量，例如 210 条信道、N = 7，每小区 30 条，其中 1 条作控制信道，剩 29 条（p.93）；非均匀 FCA：按各小区的业务量分不同数量。</li>
<li>优点是简单、容易管理；缺点是适应不了业务量的变化（忙的小区不够用，闲的小区浪费）。</li>
</ul>
<h4><span class="st">知识讲解</span>DCA：按需分配</h4>
<ul>
<li>信道不永久分给小区，放在一个公共池里。新呼叫到来时，任何基站都可以按一定算法使用任何信道，只要<b>不违反干扰约束</b>（p.95）。</li>
<li>基本干扰约束：一条信道在某小区使用时，复用距离 D 以内的其他小区不能同时用它（p.96）。</li>
<li>算法的依据：对未来阻塞的预测、信道的复用距离、其他代价函数（p.96）。</li>
<li>信道借用（channel borrowing）是 DCA 的一个例子：小区 A 向邻区 C 借一条信道，通话期间持续监测，通话结束后归还（p.95）。</li>
<li>业务量大的小区可以用更多信道，所以灵活、阻塞率低；代价是需要集中控制、更多的计算和信令。</li>
</ul>
<p>老师课上说：固定分配简单但不灵活，动态分配和信道借用更灵活；借用时仍要满足复用距离，不能造成同频干扰。</p>
<h4><span class="st">详细解析</span>答题要点（4 分）</h4>
<div class="tw"><table class="mini"><thead><tr><th></th><th>FCA</th><th>DCA</th></tr></thead><tbody>
<tr><td>信道归属</td><td>每小区预先分配一组固定信道</td><td>公共池，呼叫到来时才分配</td></tr>
<tr><td>全忙时</td><td>阻塞，即使邻区空闲</td><td>可以用任何满足复用距离的空闲信道</td></tr>
<tr><td>优点</td><td>简单</td><td>灵活，阻塞率低，适应业务变化</td></tr>
<tr><td>缺点</td><td>不灵活，信道利用率低</td><td>需要集中控制，计算复杂</td></tr>
</tbody></table></div>
<p>4 分题一般是"每种 2 分"：概念 1 分 + 特点（优缺点）1 分。两个概念都要写，并写出对比。</p>
<h4><span class="st">课外补充</span>（讲义没有，不写也不扣分）</h4>
<p>经典研究结论：业务量轻到中等时 DCA 阻塞率比 FCA 低；业务量很重时，所有小区都忙，DCA 没有空闲信道可调，性能不比 FCA 好。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>说 DCA"随便用任何信道"，漏了"不能违反复用距离 D 的同频干扰约束"。</li>
<li>FCA 只写"固定"，没写"全忙就阻塞，即使邻区有空闲信道"。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p><b>Fixed channel assignment (FCA):</b> each cell (base station) is allocated a predetermined set of channels. A call in a cell can only use the unused channels of that cell; if all of them are busy, the call is blocked even if there are free channels in neighbouring cells. The channels may be allocated equally to all cells in a cluster (uniform FCA) or according to the traffic load of each cell (non-uniform FCA). FCA is simple to implement but cannot adapt to changes in traffic.</p>
<p><b>Dynamic channel assignment (DCA):</b> channels are not allocated to cells permanently but are kept in a common pool. When a new call arrives, any base station can use any channel, chosen by an algorithm based on, e.g., the predicted future blocking, the reuse distance and other cost functions, as long as the interference constraint is not violated (the same channel cannot be reused within the reuse distance D). Channel borrowing is one example. A cell with high traffic can therefore use more channels, which gives more flexibility and lower blocking, at the cost of centralised control and more computation.</p></div>
<div class="ans">一句话：FCA 是每个小区预先分好一组固定信道，简单但不灵活；DCA 是呼叫到来时从公共池按需分配，只要满足复用距离，灵活但复杂。</div>
'''},

'y2526s1-q4a': {'title': '知识讲解 + 详细解析：接入 AP 的扫描、认证与关联', 'zh': '''
<h4><span class="st">知识讲解</span>先认识几个名词</h4>
<ul>
<li><b>AP</b>（Access Point，接入点）：WLAN 和有线网络之间的"门"，相当于无线局域网的基站。</li>
<li><b>BSS</b>（Basic Service Set，基本服务集）：一个 AP 和它下面的站点组成的一个"小区"（Part B p.10）。</li>
<li><b>DS</b>（Distribution System，分布系统）：把多个 AP（多个 BSS）连起来的骨干网（p.10）。讲义 p.32 写作 DSS，指"所有 AP 的集合"。</li>
</ul>
<p>一个节点（手机、电脑）想通过 AP 上网，不能直接发数据，要先完成一个<b>建立连接</b>的过程（connection set up，Part B p.31–32），一共三步。</p>
<h4><span class="st">详细解析</span>三步展开</h4>
<ol>
<li><b>扫描、获取同步信息（scanning）</b>：节点要加入一个已有的 BSS，首先要从 AP 那里得到同步信息（时间、参数）。两种方式：
<ul><li><b>被动扫描</b>（passive scanning）：节点只是等待 AP 周期性广播的信标帧（Beacon Frame）。省电，但要等。</li>
<li><b>主动扫描</b>（active scanning）：节点主动发探测请求帧（Probe Request Frame），等 AP 回探测响应帧（Probe Response）。快，但要多发帧。</li></ul></li>
<li><b>认证（authentication）</b>：找到 AP 后，节点和 AP 交换信息，<b>双方都要证明自己知道约定的密码</b>（p.32）。
<ul><li>作用：确认对方的身份是合法的，<b>防止未授权的设备接入网络</b>、使用网络资源或窃听；同时节点也确认自己连的是合法的 AP。</li>
<li>老师课上特别提到这一步，提醒大家自己的 Wi-Fi 一定要设密码。</li></ul></li>
<li><b>关联（association）</b>：认证通过后才开始关联。节点和 AP 交换关于节点和 BSS 能力（capabilities，如支持的速率）的信息，并<b>把节点当前的位置告诉 DS</b>，这样发给这个节点的数据才知道该送到哪个 AP（p.32）。</li>
<li><b>开始通信</b>：只有关联完成以后，节点才能收发数据帧（p.32）。</li>
</ol>
<p><b>记忆</b>："扫 → 认 → 联 → 传"。题目问了两件事：过程（三步），和认证的作用，第二件要单独写清楚，不要只写一句"认证"。</p>
<h4><span class="st">课外补充</span>（讲义没有，不写也不扣分）</h4>
<p>802.11 标准里有开放系统认证和共享密钥认证；现在常用的 WPA2/WPA3 在关联之后还有一个"四次握手"来生成加密密钥。考试按讲义的三步写就够了。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>认证和关联的顺序写反：先认证，后关联。</li>
<li>扫描只写一种方式：被动和主动都要写，并写出对应的帧名（Beacon、Probe Request/Response）。</li>
<li>认证的作用只写"安全"两个字：要写"双方证明知道密码 → 确认合法身份 → 防止未授权接入"。</li>
<li>漏了最后一句"关联完成后才能传数据"。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>The connection establishment between a node and an AP has three steps.</p>
<p><b>1. Scanning (synchronization):</b> to join an existing BSS, the node first obtains synchronization information from the AP. In passive scanning, the node simply waits to receive a Beacon frame that the AP broadcasts periodically. In active scanning, the node transmits Probe Request frames and waits for a Probe Response from the AP.</p>
<p><b>2. Authentication:</b> once the node has found an AP, the node and the AP exchange information in which each side proves the knowledge of a given (shared) password. The function of authentication is to verify that the node is a legitimate user (and that the AP is a legitimate AP), so that unauthorised devices are prevented from accessing the network and its resources.</p>
<p><b>3. Association:</b> after the node is authenticated, it starts the association process, in which the node and the AP exchange information about the node and BSS capabilities, and the distribution system (the set of APs) is informed of the current position of the node, so that frames for the node can be delivered through the correct AP.</p>
<p>Only after the association is completed can the node transmit and receive data frames.</p></div>
<div class="ans">一句话：扫描（被动等 Beacon / 主动发 Probe）→ 认证（双方证明知道密码，防止非法接入）→ 关联（交换能力、向 DS 登记位置）→ 才能收发数据。</div>
'''},

'y2526s1-q4bc': {'title': '知识讲解 + 详细解析：IoT 五个难点与雾计算特征', 'zh': '''
<h4><span class="st">知识讲解</span>IoT 为什么难</h4>
<p>物联网（IoT，Internet of Things）要把原来不联网的"物"（传感器、执行器、家电、车……）都连起来。和传统互联网相比，它的设备<b>数量极多</b>、<b>能力很弱</b>（电池、低算力）、<b>种类繁杂</b>、产生的数据<b>又多又敏感</b>。讲义 Part B p.82–83 把由此带来的障碍归纳为五个：可扩展性、安全、隐私、大数据与分析、互操作性。</p>
<h4><span class="st">详细解析</span>(b) 五个难点逐个展开（10 分，每个 2 分：名称 + 一两句解释）</h4>
<ol>
<li><b>可扩展性（Scalability）</b>：IoT 规模可能达到数百万台设备，整个系统（寻址、接入、管理）如何支撑这么多设备是关键问题。网络层可以用 IPv6 给海量设备分配地址。</li>
<li><b>安全（Security）</b>：联网的"物"越多，被攻击的面越大。一个设备被黑以后，它的连接能力本身就是威胁：被攻破的设备可以成为攻击其他设备和系统的跳板。很多设备算力弱，难以运行复杂的安全协议。</li>
<li><b>隐私（Privacy）</b>：传感器越来越多，采集的数据大多和具体的人及其活动有关，可能包含敏感信息和凭证。数据如何保护、是否共享、和谁共享，是关键问题。</li>
<li><b>大数据与分析（Big data and analytics）</b>：大量传感器会产生数据洪流。数据只有被高效处理才能提供关键信息；难点在于要及时处理来自不同来源、不同格式的海量数据。</li>
<li><b>互操作性（Interoperability）</b>：各种协议和架构在争夺市场份额和标准地位，有的基于私有组件，有的是开放的。新的 IoT 标准能缓解，但实际网络里仍有多种协议和实现并存，不同厂家的设备难以互通。</li>
</ol>
<p><b>记忆</b>：规模、安全、隐私、数据、互通（Scalability, Security, Privacy, Big data, Interoperability）。</p>
<h4><span class="st">知识讲解</span>为什么需要雾计算</h4>
<p>如果所有数据都上传到云端处理，会遇到（p.105）：最后一公里带宽很有限；时延很大，做不到实时响应；网关的回传链路（3G/LTE 甚至卫星）不可靠；回传的数据量太大；数据越来越多，实时分析几乎不可能。解决办法是把数据管理分散到尽量靠近网络边缘的地方，这就是<b>雾计算（fog computing）</b>（p.106）。任何有计算、存储和网络连接能力的设备都可以做雾节点（fog node）。</p>
<h4><span class="st">详细解析</span>(c) 雾计算的关键特征（7 分）</h4>
<p>讲义 p.109 的五个特征（每个写一句解释）：</p>
<ol>
<li><b>上下文位置感知和低时延</b>（contextual location awareness and low latency）：雾节点尽可能靠近 IoT 终端，就近做分布式计算；因为地理上靠近，它了解自己管理的传感器的上下文，能更快地对网络里的事件做出反应（p.108）。</li>
<li><b>地理分布</b>（geographic distribution）：雾节点服务的业务和应用需要大范围分布式部署。</li>
<li><b>部署在 IoT 终端附近</b>（deployment near IoT endpoints）：雾节点通常部署在有大量 IoT 终端的地方。</li>
<li><b>雾节点和终端之间用无线通信</b>：一个雾节点要连接大量终端，无线接入是实现大规模可扩展的最简单方式。</li>
<li><b>用于实时交互</b>（real-time interactions）：在雾节点先做预处理，上层应用只需要对数据的一个子集做批处理。</li>
</ol>
<p>为了拿满 7 分，再写两三条好处（p.106、p.108）：降低时延；减轻核心网的流量（不用把 GB 级数据都传上去）；敏感数据留在本地网络；提供分布式的边缘控制回路，不用等云端服务器就能实时监控和控制；整体上减少数据量（data reduction）。老师课上总结的好处也是这几条：分布式处理不用等中心服务器所以快、上传前先精简数据、能实时处理、雾节点和终端无线连接。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>(b) 只列五个名词不解释：题目要求 "briefly describe each"，每个要有一两句。</li>
<li>(b) 写成 IoT 的应用或优点，答非所问。</li>
<li>(c) 把雾计算说成"取代云计算"：讲义 p.111 说边缘和雾只是第一道处理，不取代云。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p><b>(b)</b> Five potential difficulties in the development of IoT:</p>
<p>1. <b>Scalability:</b> IoT may grow to include millions of devices. How the overall system (addressing, access and management) can support such a huge number of devices is a critical issue; IPv6 can provide enough addresses at the network layer.</p>
<p>2. <b>Security:</b> as more "things" are connected with other things and people, the threat surface is greatly expanded. If a device is hacked, its connectivity becomes a major concern, because a compromised device can serve as a launching point to attack other devices and systems.</p>
<p>3. <b>Privacy:</b> much of the data gathered by sensors is specific to individuals and their activities and may contain sensitive information and credentials. How the data are protected, and whether and with whom they are shared, is a critical issue.</p>
<p>4. <b>Big data and analytics:</b> the large number of sensors produces a deluge of data. The data provide useful insights only if they are processed efficiently; the challenge is to evaluate massive amounts of data arriving from different sources in various forms in a timely manner.</p>
<p>5. <b>Interoperability:</b> many protocols and architectures, some proprietary and some open, are competing for market share and standardisation. Devices and networks using different protocols and implementations cannot easily work together.</p>
<p><b>(c)</b> Fog computing distributes data processing to fog nodes at the edge of the network, close to where IoT data are generated. Its key features are:</p>
<p>1. <b>Contextual location awareness and low latency:</b> the fog node sits as close to the IoT endpoints as possible, so it knows the context of the sensors it manages and can react to events much faster than a remote cloud.</p>
<p>2. <b>Geographic distribution:</b> the services and applications served by fog nodes require widely distributed deployments.</p>
<p>3. <b>Deployment near IoT endpoints:</b> fog nodes are typically deployed where there is a large number of IoT endpoints.</p>
<p>4. <b>Wireless communication between the fog node and the IoT endpoints:</b> since a fog node must handle many endpoints, wireless access is the easiest way to achieve large scalability.</p>
<p>5. <b>Use for real-time interactions:</b> data are pre-processed at the fog nodes, so upper-layer applications only need to perform batch processing on a subset of the data.</p>
<p>As a result, fog computing reduces latency, offloads traffic from the core network and the backhaul, keeps sensitive data inside the local network, reduces the amount of data to be sent, and provides a distributed edge control loop for real-time monitoring and control.</p></div>
<div class="ans">一句话：IoT 五难是规模、安全、隐私、大数据、互通；雾计算把处理放到靠近终端的雾节点，特征是低时延/位置感知、地理分布、靠近终端、无线接入、实时交互。</div>
'''},

# ===================================================================== 2025-26 S2
'y2526s2-q1a': {'title': '知识讲解 + 详细解析：衰落类型、LCR 与衰落余量', 'zh': '''
<h4><span class="st">知识讲解</span>衰落类型的两个独立维度</h4>
<p>无线信道对信号有两种"色散"，要分开判断（第 2 章 p.30–39）：</p>
<ul>
<li><b>时间色散</b>（多径时延扩展引起）→ 用<b>相干带宽 B<sub>c</sub></b> 描述（B<sub>c</sub> ≈ 1/σ<sub>τ</sub>，在这个带宽内各频率的衰落基本相同）。比较信号带宽 B<sub>s</sub>：B<sub>s</sub> &lt; B<sub>c</sub> → <b>平坦衰落</b>（flat）；B<sub>s</sub> &gt; B<sub>c</sub> → <b>频率选择性衰落</b>（frequency selective），时域上表现为 ISI。</li>
<li><b>频率色散</b>（移动引起的多普勒扩展）→ 用<b>多普勒扩展 B<sub>D</sub></b> 描述，对应相干时间 T<sub>c</sub> ≈ 1/B<sub>D</sub>（信道在这段时间内基本不变）。比较 B<sub>s</sub>：B<sub>s</sub> ≫ B<sub>D</sub>（等价于符号时长 T<sub>s</sub> ≪ T<sub>c</sub>）→ <b>慢衰落</b>（slow），一个符号内幅度相位不变；B<sub>s</sub> 不比 B<sub>D</sub> 大多少（T<sub>s</sub> 接近或大于 T<sub>c</sub>）→ <b>快衰落</b>（fast）（p.37）。</li>
</ul>
<div class="tw"><table class="mini"><thead><tr><th></th><th>B<sub>s</sub> ≫ B<sub>D</sub>（慢）</th><th>B<sub>s</sub> 接近 B<sub>D</sub>（快）</th></tr></thead><tbody>
<tr><td>B<sub>s</sub> &lt; B<sub>c</sub></td><td>平坦慢衰落</td><td>平坦快衰落</td></tr>
<tr><td>B<sub>s</sub> &gt; B<sub>c</sub></td><td>频率选择性慢衰落</td><td>频率选择性快衰落</td></tr>
</tbody></table></div>
<p>老师课上强调：问衰落类型<b>必须两个维度都答</b>，只答一个维度只给一半分；简单记法是"带宽在相干带宽以内就平坦，符号在相干时间以内就慢"。</p>
<h4><span class="st">知识讲解</span>LCR 和 AFD 的定义</h4>
<p>电平通过率（LCR，Level Crossing Rate）：信号强度每秒<b>向下</b>穿过门限 Z<sub>min</sub> 的平均次数（p.40）。平均衰落时长（AFD，Average Fade Duration）：每次衰落中信号低于门限的平均时长（p.42）。老师说今年 Quiz 的常见错误是：题目没说瑞利衰落时，要<b>按定义</b>算，不能套含 f<sub>m</sub>、ρ 的瑞利公式。</p>
<h4><span class="st">知识讲解</span>中断容量和衰落余量</h4>
<p>慢衰落下，允许一个很小的中断概率 ε：ε = P(γ &lt; γ<sub>min</sub>)。瑞利衰落时 SNR 服从指数分布，CDF = 1 − e<sup>−γ/γ̄</sup>，反解得 γ<sub>min</sub> = γ̄ ln(1/(1 − ε))，代入香农公式就是题目给的 C<sub>ε</sub>（p.50–51）。γ<sub>min</sub> 就是"AWGN 信道要达到同样容量所需的 SNR"。衰落余量（fade margin）= 衰落信道需要的平均 SNR − AWGN 需要的 SNR（dB 相减）= 10 log₁₀[1/ln(1/(1 − ε))]，只和 ε 有关。老师说这个公式"有点难记，但要尽量记"。</p>
<h4><span class="st">详细解析</span>(ii) LCR 和每秒连续误符号</h4>
<ol>
<li>LCR 按定义：
<div class="calc">LCR = 40 次 / 10 s = 4 次/秒</div></li>
<li>每次衰落平均 20 ms，符号 5 ms，每次衰落连续错几个符号：
<div class="calc">AFD / T<sub>s</sub> = 20 ms / 5 ms = 4 个</div></li>
<li>每秒误符号数：
<div class="calc">4 次/秒 × 4 个/次 = 16 个/秒（每秒 4 串，每串 4 个连续错误）</div></li>
</ol>
<p><b>合理性检查</b>：每秒处于衰落的时间 = LCR × AFD = 4 × 0.02 = 0.08 s（8%）；每秒发 1/5 ms = 200 个符号，200 × 8% = 16 个，和上面一致。</p>
<h4><span class="st">详细解析</span>(iii) 最小 SNR 和衰落余量</h4>
<ol>
<li>dB 换线性：25 dB → 10<sup>2.5</sup> = 316.2。</li>
<li>ln(1/(1 − ε)) = ln(1/0.995) = 0.005013（ε 很小时 ≈ ε，可用来检查）。</li>
<li><div class="calc">γ<sub>min</sub> = 316.2 × 0.005013 = 1.585 → 10 log₁₀1.585 = 2.0 dB</div></li>
<li><div class="calc">FM = 25 − 2.0 = 23.0 dB（= 10 log₁₀[1/0.005013]）</div></li>
</ol>
<p>含义：瑞利衰落下平均 SNR 是 25 dB，但为了保证 99.5% 的时间不中断，能用的容量只相当于 SNR 为 2 dB 的 AWGN 信道，C<sub>ε</sub>/B = log₂(1 + 1.585) ≈ 1.37 bit/s/Hz；"浪费"的 23 dB 就是为衰落留的余量。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>(i) 拿 B<sub>c</sub> 和 B<sub>D</sub> 互相比较：两个维度都是和信号带宽 B<sub>s</sub> 比。</li>
<li>(ii) LCR 写成 40（忘了除以 10 s），或者套瑞利 LCR 公式。</li>
<li>(iii) 25 dB 不换线性直接乘；γ<sub>min</sub> 不换回 dB 就和 25 dB 相减。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) Two comparisons are needed. (1) Signal bandwidth B<sub>s</sub> versus coherence bandwidth B<sub>c</sub> (caused by multipath delay spread): if B<sub>s</sub> &lt; B<sub>c</sub>, all frequency components fade together and the signal experiences flat fading; if B<sub>s</sub> &gt; B<sub>c</sub>, different frequencies fade differently, i.e. frequency-selective fading, which causes ISI. (2) Signal bandwidth B<sub>s</sub> versus Doppler spread B<sub>D</sub> (caused by motion): if B<sub>s</sub> ≫ B<sub>D</sub> (symbol duration much shorter than the coherence time T<sub>c</sub> ≈ 1/B<sub>D</sub>), the channel is constant over a symbol and the fading is slow; otherwise the amplitude and phase change within a symbol and the fading is fast. Combining both gives flat slow, flat fast, frequency-selective slow or frequency-selective fast fading.</p>
<p>(ii) LCR = number of downward crossings per second = 40/10 = 4 crossings/s. Each fade lasts 20 ms on average, i.e. 20/5 = 4 consecutive symbols in error per fade. Number of symbol errors per second = 4 × 4 = 16 (4 bursts of 4 consecutive errors).</p>
<p>(iii) γ̄<sub>R</sub> = 25 dB = 316.2. Minimum SNR: γ<sub>min</sub> = γ̄<sub>R</sub> ln(1/(1 − ε)) = 316.2 × ln(1/0.995) = 316.2 × 0.005013 = 1.585 (2.0 dB). This is the SNR an AWGN channel needs to achieve the same capacity. Fade margin = 25 − 2.0 = 23.0 dB = 10 log₁₀[1/ln(1/(1 − ε))].</p></div>
<div class="ans">一句话：B<sub>s</sub> 比 B<sub>c</sub> 判平坦/频选，B<sub>s</sub> 比 B<sub>D</sub> 判慢/快；LCR = 4/s，每次连错 4 个，每秒 16 个；γ<sub>min</sub> ≈ 2.0 dB，衰落余量 23 dB。</div>
'''},

'y2526s2-q1b1': {'title': '知识讲解 + 详细解析：阵列增益与由 d 求误码率', 'zh': '''
<h4><span class="st">知识讲解</span>阵列增益 g 和分集增益 d</h4>
<p>分集合并有两个性能指标（第 4 章 p.27，老师说这两个公式"简单、要记住"）：</p>
<ul>
<li><b>阵列增益</b>（array gain）g ≈ γ̄<sub>Σ</sub>/γ̄：合并器输出平均 SNR 除以输入平均 SNR，表示平均 SNR 提高了几倍。dB 下就是相减。题目写的 "gain array" 就是它。</li>
<li><b>分集增益</b>（diversity gain / order）d：高 SNR 下平均误码率 P̄<sub>e</sub> ≈ γ̄<sup>−d</sup>，γ̄ 是<b>合并器输入</b>的平均 SNR。d 越大，误码率曲线越陡：SNR 提高 10 倍，误码率下降 10<sup>d</sup> 倍。</li>
</ul>
<p>本题是把公式"反过来用"：已知 d，求 P̄<sub>e</sub>。</p>
<h4><span class="st">详细解析</span>一步一步算</h4>
<ol>
<li><b>阵列增益</b>：dB 下直接相减，再换线性：
<div class="calc">g = 15 dB − 12 dB = 3 dB → 10<sup>0.3</sup> = 1.995 ≈ 2</div>
意思是合并后平均 SNR 翻了一倍。</li>
<li><b>输入 SNR 换线性</b>：12 dB → 10<sup>1.2</sup> = 15.85（计算器提示：log₁₀15.85 = 1.2，后面正好用到）。</li>
<li><b>误码率</b>：
<div class="calc">P̄<sub>e</sub> ≈ γ̄<sup>−d</sup> = 15.85<sup>−3.7</sup> = 10<sup>−1.2 × 3.7</sup> = 10<sup>−4.44</sup> ≈ 3.6×10⁻⁵</div>
计算器没有直接算的话：10<sup>−4.44</sup> = 10<sup>0.56</sup> × 10⁻⁵ = 3.63 × 10⁻⁵。</li>
</ol>
<p><b>对比</b>：如果误用输出 SNR（15 dB = 31.62），得 31.62<sup>−3.7</sup> ≈ 2.8×10⁻⁶，差了一个数量级，所以一定要记住 γ̄ 是输入 SNR（讲义和 Practice 4 的官方答案都用输入）。再如 d = 2 时 15.85⁻² ≈ 4×10⁻³，可见 d 越大误码率越低。</p>
<h4><span class="st">补充思考</span>这组数字合理吗</h4>
<p>p.28 说 M 支路接收时 d ≤ M，所以 d = 3.7 至少要 4 条支路。g ≈ 2 也说得通：例如 4 支路选择分集（SD）的平均输出 SNR 是 γ̄Σ1/i，g = 1 + 1/2 + 1/3 + 1/4 = 2.08（3.2 dB），和 3 dB 很接近。这只是帮助理解，考试不用写。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>把 dB 值直接相除：15/12 = 1.25 是错的，dB 要相减或先换线性再相除。</li>
<li>P̄<sub>e</sub> 公式里代 dB 值：12<sup>−3.7</sup> 是错的，必须用线性值 15.85（老师说没做 dB ↔ 线性换算会扣分）。</li>
<li>用输出 SNR 代入，得 2.8×10⁻⁶。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Array gain: g = γ̄<sub>Σ</sub>/γ̄, where γ̄<sub>Σ</sub> is the average combiner output SNR and γ̄ the average combiner input SNR. In dB, g = 15 − 12 = 3 dB, i.e. g = 10<sup>0.3</sup> ≈ 2.</p>
<p>Probability of error: at high SNR, P̄<sub>e</sub> ≈ γ̄<sup>−d</sup>, with γ̄ the average input SNR. γ̄ = 12 dB = 10<sup>1.2</sup> = 15.85, so P̄<sub>e</sub> ≈ 15.85<sup>−3.7</sup> = 10<sup>−4.44</sup> ≈ 3.6 × 10⁻⁵.</p></div>
<div class="ans">一句话：阵列增益 = 15 − 12 = 3 dB ≈ 2 倍；误码率 P̄<sub>e</sub> ≈ γ̄<sup>−d</sup>，用输入 SNR 15.85，得 10<sup>−4.44</sup> ≈ 3.6×10⁻⁵。</div>
'''},

'y2526s2-q1b2': {'title': '知识讲解 + 详细解析：MIMO 模型与 Alamouti', 'zh': '''
<h4><span class="st">知识讲解</span>平坦衰落下每条信道为什么只有一个增益</h4>
<p>第 5 章 p.4 列出了几种信道：<b>平坦、时不变</b>衰落时 y(t) = h × x(t)，信道只是一个复数系数；<b>频率选择性</b>衰落时 y(t) = ∫h(t − τ)x(τ)dτ，是卷积。平坦衰落意味着信号带宽小于相干带宽（时延扩展远小于符号时长），各条多径到达的时间差可以忽略，它们在一个符号内叠加成<b>一个复数增益</b>（幅度 + 相位），没有可以分辨的多个抽头，也就没有 ISI。所以每一对"发射天线 j → 接收天线 i"之间只需要一个数 h<sub>ij</sub>。</p>
<h4><span class="st">知识讲解</span>MIMO 的输入输出关系</h4>
<p>讲义 p.5–6：每根接收天线收到的是所有发射天线信号的加权和，再加上自己的噪声：y<sub>i</sub> = Σ<sub>j</sub> h<sub>ij</sub>x<sub>j</sub> + v<sub>i</sub>。把它们排成列向量就是 y = Hx + v。H 的<b>行对应接收天线、列对应发射天线</b>。老师说这个关系要能直接写出来，单个元素的式子和矩阵形式都要会。</p>
<h4><span class="st">知识讲解</span>Alamouti 检测量的分布</h4>
<p>Alamouti 码（2 发 1 收，编码矩阵是蓝框、要背）经过重新排列后得到 ỹ = Fs + ṽ，F 满足 F<sup>H</sup>F = ‖h‖²I（p.23）。ML 检测的结果是 ŝ = (1/‖h‖²)F<sup>H</sup>ỹ = s + (1/‖h‖²)F<sup>H</sup>ṽ（p.25），题目里的 G 就是 F<sup>H</sup>。讲义的结论是 ŝ ~ N(s, (σ²/‖h‖²)·1)，本题就是要你推出这个结论。要用的两条性质（第 1b 章）：E[a + cX] = a + cE[X]；Var[a + cX] = c²Var[X]（常数 a 不贡献方差，系数要平方）。</p>
<h4><span class="st">详细解析</span>(ii) 4 发 6 收</h4>
<ol>
<li>平坦衰落 → 每对天线一个复数增益 h<sub>ij</sub>，共 6 × 4 = 24 个。</li>
<li>尺寸：x 是 4×1（4 根发射天线），y、v 是 6×1（6 根接收天线），所以 H 是 <b>6×4</b>。</li>
<li>写出矩阵：
<div class="calc">y = Hx + v<br>H = [h<sub>11</sub> h<sub>12</sub> h<sub>13</sub> h<sub>14</sub>; h<sub>21</sub> h<sub>22</sub> h<sub>23</sub> h<sub>24</sub>; … ; h<sub>61</sub> h<sub>62</sub> h<sub>63</sub> h<sub>64</sub>]（6 行 4 列）<br>y<sub>i</sub> = Σ<sub>j=1</sub><sup>4</sup> h<sub>ij</sub>x<sub>j</sub> + v<sub>i</sub>，i = 1, …, 6</div></li>
</ol>
<p>检查方法：矩阵乘法 (6×4)(4×1) = 6×1，和 y 的尺寸一致。</p>
<h4><span class="st">详细解析</span>(iii) 均值和方差</h4>
<ol>
<li><b>均值</b>：s 是发送的确定信号；h、G 对检测来说是已知常数；w 零均值：
<div class="calc">E[ŝ] = s + (1/‖h‖²)·G·E[w] = s + 0 = s</div>
检测是<b>无偏</b>的（unbiased），平均来说正好等于发送的符号。</li>
<li><b>方差</b>：s 是常数，不贡献方差；随机部分是 (1/‖h‖²)Gw，系数 1/‖h‖² 平方后是 1/‖h‖⁴：
<div class="calc">Var[ŝ] = (1/‖h‖⁴)·Var[Gw] = (1/‖h‖⁴)·σ²‖h‖²·(1, 1)<sup>T</sup> = (σ²/‖h‖²)·(1, 1)<sup>T</sup></div></li>
<li><b>含义</b>：两个符号的噪声方差都是 σ²/‖h‖² = σ²/(|h₁|² + |h₂|²)，所以 ŝ ~ N(s, σ²/‖h‖²)。两条路径的功率增益相加，噪声被压低：只要 h₁、h₂ 不同时很小，检测就可靠，这就是 Alamouti 的发射分集（分集阶数 2）。对应的每个符号的 SNR = E{|s<sub>n</sub>|²}‖h‖²/σ²（p.26）。</li>
</ol>
<p><b>数字小例子</b>：|h₁|² = 0.5、|h₂|² = 1.5 → ‖h‖² = 2，噪声方差变成 σ²/2，比只有一条增益为 1 的路径好一倍。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>H 写成 4×6：行数 = 接收天线数 = 6。</li>
<li>(ii) 只写 y = Hx + v，没解释"为什么只有一个增益"（平坦 → 无可分辨多径 → 一个复系数）。</li>
<li>(iii) 方差只乘 1/‖h‖²（没平方），得到 σ²，结论就错了。</li>
<li>漏写"零均值 → 无偏"的理由，只写一个结果（老师说只写数不写理由只给一半分）。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(ii) In a flat fading channel the signal bandwidth is smaller than the coherence bandwidth (the delay spread is much smaller than the symbol duration), so the multipath components between each transmit–receive antenna pair cannot be resolved and add up to a single complex gain. There is no ISI, and each channel is described by one gain h<sub>ij</sub>.</p>
<p>The input-output relationship is y = Hx + v, where x is the 4 × 1 transmitted vector, y and v are 6 × 1 received and noise vectors, and H is the 6 × 4 channel matrix H = [h<sub>ij</sub>], i = 1, …, 6 (receive antennas, rows), j = 1, …, 4 (transmit antennas, columns). Element by element: y<sub>i</sub> = Σ<sub>j=1</sub><sup>4</sup> h<sub>ij</sub>x<sub>j</sub> + v<sub>i</sub>.</p>
<p>(iii) Since s is deterministic and w has zero mean, E[ŝ] = s + (1/‖h‖²)G E[w] = s, i.e. the detection is unbiased.</p>
<p>The constant s does not contribute to the variance, and the scalar 1/‖h‖² is squared: Var[ŝ] = (1/‖h‖⁴)Var[Gw] = (1/‖h‖⁴)σ²‖h‖²(1, 1)<sup>T</sup> = (σ²/‖h‖²)(1, 1)<sup>T</sup>.</p>
<p>Hence each detected symbol is Gaussian with mean s<sub>n</sub> and variance σ²/‖h‖² = σ²/(|h₁|² + |h₂|²): the gains of the two paths add up and reduce the effective noise, which gives diversity.</p></div>
<div class="ans">一句话：平坦衰落每对天线一个复增益，y = Hx + v，H 是 6×4；Alamouti 检测量均值为 s（无偏），方差 σ²/‖h‖²（系数平方后乘噪声方差）。</div>
'''},

'y2526s2-q2a': {'title': '知识讲解 + 详细解析：Nyquist 准则与残余 ISI', 'zh': '''
<h4><span class="st">知识讲解</span>ISI 是怎么来的，Nyquist 准则说什么</h4>
<p>发送端每隔 T 秒发一个脉冲，脉冲经过发送滤波器和信道后会展宽。接收端在 t = nT 采样时，采到的是（第 6 章 p.10–12）：</p>
<div class="calc">y(nT) = m[n]g<sub>e</sub>(0) + Σ<sub>i≠n</sub> m[i]g<sub>e</sub>(nT − iT) + w(nT)</div>
<p>第一项是想要的符号，第二项是其他符号的脉冲"拖尾"到这个采样时刻的部分，就是 ISI。<b>Nyquist 无 ISI 准则</b>：如果等效脉冲 g<sub>e</sub> 在本符号的采样时刻为 1、在其他所有符号的采样时刻都为 0，即 g<sub>e</sub>(nT − iT) = 1（n = i）、0（n ≠ i），那么第二项消失，传输没有 ISI。脉冲可以在采样点之间不为零，只要在别人的采样点上恰好过零就行。老师说这个准则"值得记住"：一句话（传输没有 ISI）加一个式子。</p>
<p>离散模型（p.22）：按符号间隔采样后，信道就是抽头 h[1], …, h[L]，r[n] = Σh[i]m[n − i + 1] + w[n]。用这个模型说，Nyquist 准则就是 h[1] = 1、其余 h[i] = 0。</p>
<h4><span class="st">知识讲解</span>线性均衡器的输出噪声和残余 ISI</h4>
<p>均衡器是 M 个抽头的 FIR 滤波器，噪声也要经过它：w′(n) = Σc<sub>j</sub>w(n − j + 1)。各个噪声样本独立、方差都是 σ²，所以输出噪声功率 σ′² = σ²Σc<sub>j</sub>²（p.27 的"variance σ²‖c‖²"）。均衡后如果还留有一点 ISI，误码率按"先固定 ISI 求条件误码率、再对 ISI 取平均"来算（p.27–28）。</p>
<h4><span class="st">详细解析</span>(i) 模型和准则</h4>
<div class="calc">r[n] = Σ<sub>i=1</sub><sup>L</sup> h[i]m[n − i + 1] + w[n] = h[1]m[n] + h[2]m[n−1] + … + h[L]m[n−L+1] + w[n]</div>
<p>第一项 h[1]m[n] 是想要的，其余 h[i]m[n − i + 1]（i ≥ 2）是前面符号造成的 ISI。再写 Nyquist 准则（上面那句话 + 式子）。</p>
<h4><span class="st">详细解析</span>(ii) 输出噪声功率</h4>
<div class="calc">σ′² = σ²Σc<sub>j</sub>² = 0.25 × 2.56 = 0.64</div>
<p>比输入的 0.25 大了 2.56 倍：这就是均衡器的噪声增强。</p>
<h4><span class="st">详细解析</span>(iii) 残余 ISI 下的误码率</h4>
<p>σ′ = √0.64 = 0.8。由对称性只看 m(n) = +1，0.2m(n−1) 等概为 ±0.2：</p>
<div class="tw"><table class="mini"><thead><tr><th>m(n−1)</th><th>y(n) 的均值</th><th>条件误码率</th></tr></thead><tbody>
<tr><td>+1（概率 ½）</td><td>1.2</td><td>Q(1.2/0.8) = Q(1.5) = 0.0668</td></tr>
<tr><td>−1（概率 ½）</td><td>0.8</td><td>Q(0.8/0.8) = Q(1) = 0.1587</td></tr>
</tbody></table></div>
<div class="calc">P<sub>e</sub> = ½(0.0668 + 0.1587) = 0.1127 ≈ 0.113</div>
<p><b>对比</b>：即使均衡器把 ISI 全部去掉，噪声已被放大到 0.64，P<sub>e</sub> = Q(1/0.8) = Q(1.25) ≈ 0.106；如果原信道本来就没有 ISI、也不用均衡，P<sub>e</sub> = Q(1/0.5) = Q(2) ≈ 0.023。可见噪声增强的代价很大。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>(ii) 答成 0.25 × 2.56 后又开根号，或者把 Σc<sub>j</sub>² 再平方。</li>
<li>(iii) Q 里除以方差 0.64：要除以标准差 0.8。</li>
<li>(iii) 只算一种情况，或者忘了各乘 ½。</li>
<li>(i) 准则只写"没有 ISI"，没写采样时刻为 1、其他时刻为 0 的条件。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) r[n] = Σ<sub>i=1</sub><sup>L</sup> h[i] m[n − i + 1] + w[n]. The term h[1]m[n] is the desired symbol and the terms with i ≥ 2 are ISI from previous symbols.</p>
<p>Nyquist ISI criterion: after sampling, y(nT) = m[n]g<sub>e</sub>(0) + Σ<sub>i≠n</sub> m[i]g<sub>e</sub>(nT − iT) + w(nT). If the equivalent pulse satisfies g<sub>e</sub>(nT − iT) = 1 for n = i and 0 for n ≠ i, i.e. each pulse is zero at the sampling instants of all other symbols, the ISI term vanishes and the transmission is ISI-free. For the discrete model this means h[1] = 1 and h[i] = 0 for i ≥ 2.</p>
<p>(ii) The equalizer output noise is w′(n) = Σc<sub>j</sub>w(n − j + 1). Since the noise samples are independent with variance σ², the output noise power is σ′² = σ²Σc<sub>j</sub>² = 0.25 × 2.56 = 0.64.</p>
<p>(iii) σ′ = 0.8. By symmetry, take m(n) = +1. If m(n − 1) = +1, P(e) = P(w′ &lt; −1.2) = Q(1.2/0.8) = Q(1.5) = 0.0668. If m(n − 1) = −1, P(e) = P(w′ &lt; −0.8) = Q(1) = 0.1587. Average P<sub>e</sub> = ½(0.0668 + 0.1587) ≈ 0.113.</p></div>
<div class="ans">一句话：Nyquist 准则是脉冲在别人的采样点上为零；噪声功率 0.25 × 2.56 = 0.64；σ′ = 0.8，ISI ±0.2 两种情况平均得 P<sub>e</sub> ≈ 0.113。</div>
'''},

'y2526s2-q2b': {'title': '知识讲解 + 详细解析：子载波增益、IDFT 与循环前缀', 'zh': '''
<h4><span class="st">知识讲解</span>子载波信道增益</h4>
<p>OFDM 把频率选择性信道切成 N 个平坦的子信道，第 k 个子载波看到的是一个复数增益 H<sub>k</sub>（第 7 章 p.15）：</p>
<div class="calc">H<sub>k</sub> = Σ<sub>i=0</sub><sup>L−1</sup> h<sub>i</sub> e<sup>−j2πik/N</sup>，k = 1, …, N（注意 H<sub>N</sub> = H<sub>0</sub>）</div>
<p>它就是信道抽头的 N 点 DFT，也等于把 Z = e<sup>j2πk/N</sup> 代进 H(Z)。加了循环前缀后，每个子载波的接收信号就是 r<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + w<sub>k</sub>（p.17、p.22），接收端只要每个子载波除以一个 H<sub>k</sub> 就完成了均衡。</p>
<h4><span class="st">知识讲解</span>为什么 OFDM 调制就是 IDFT</h4>
<p>p.19：把一个 OFDM 块的 x(t) 在 N 个等间隔时刻采样，得到的 N 个样本正好是 {s<sub>k</sub>} 的 IDFT；p.20：接收端相关器的输出正好是 DFT。所以实际系统用 IFFT/FFT 芯片就能实现，不需要 N 个振荡器。</p>
<h4><span class="st">知识讲解</span>循环前缀（CP）和功率损失</h4>
<p>保护间隔 T<sub>G</sub> ≥ 最大时延扩展 T<sub>D</sub>，前一个块的拖尾落在保护间隔里，被接收端丢掉，所以块间没有 ISI（p.17–18）。保护间隔里放的是块末尾 G 个样本的复制，叫<b>循环前缀</b>（p.21–22），这样信道的线性卷积变成循环卷积，每个子载波才是简单的 H<sub>k</sub>s<sub>k</sub>。代价是 CP 也要花发射功率，却不带新信息，功率损失（p.18）= 10 log₁₀[(NT<sub>S</sub> + T<sub>G</sub>)/(NT<sub>S</sub>)]。</p>
<h4><span class="st">详细解析</span>(i) 4 个子载波的增益</h4>
<p>h<sub>0</sub> = 1，h<sub>1</sub> = 0.3，N = 4，H<sub>k</sub> = 1 + 0.3e<sup>−j2πk/4</sup>。先算 e<sup>−jπk/2</sup>：k = 1 → −j，k = 2 → −1，k = 3 → j，k = 4 → 1。</p>
<div class="calc">H₁ = 1 + 0.3(−j) = 1 − 0.3j（|H₁| = 1.044）<br>H₂ = 1 + 0.3(−1) = 0.7<br>H₃ = 1 + 0.3(j) = 1 + 0.3j<br>H₄ = 1 + 0.3(1) = 1.3（= H₀）</div>
<p><b>检查</b>：h 是实数，所以 H₃ = H₁ 的共轭，成立。增益从 0.7 到 1.3 不等，说明原信道是频率选择性的，但每个子载波内部只是一个常数。</p>
<h4><span class="st">详细解析</span>(ii) 为什么是 IDFT</h4>
<ol>
<li>在一个块内按 t = iT/N（i = 0, …, N−1）采样，代入 x(t)：
<div class="calc">x<sub>i</sub> = x(iT/N) = (1/√T) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub> e<sup>j2πki/N</sup></div></li>
<li>N 点 IDFT 的定义是 x<sub>i</sub> = (1/N)Σ<sub>k</sub> X<sub>k</sub> e<sup>j2πki/N</sup>。两式只差一个常数比例，形式完全相同。</li>
<li>所以把频域的 N 个符号 {s<sub>k</sub>} 变成时域的 N 个样本，就是做一次 IDFT；发射端用 IFFT 实现，接收端用 FFT 解调。</li>
</ol>
<h4><span class="st">详细解析</span>(iii) 符号时长和功率损失</h4>
<ol>
<li>4 个基带符号并行，每个子载波上的符号时长（有用部分）T = NT<sub>S</sub> = 4 × 2 = 8 µs。</li>
<li>加 CP：
<div class="calc">T<sub>OFDM</sub> = 8 + 20 = 28 µs</div></li>
<li>功率损失（计算器：28/8 = 3.5，log₁₀3.5 = 0.544）：
<div class="calc">10 log₁₀(28/8) = 10 log₁₀3.5 ≈ 5.44 dB</div></li>
</ol>
<p>20/28 ≈ 71% 的发射能量花在 CP 上，非常浪费。实际设计会增大 N，让 NT<sub>S</sub> 远大于 CP。（补充思考：信道 1 + 0.3Z⁻¹ 只延迟一个基带符号，即 2 µs，CP 有 2 µs 就够；题目给 20 µs 是为了练公式，答题照题目算即可。）</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>(i) e<sup>−j2πk/4</sup> 的符号搞反，H₁ 和 H₃ 写反。</li>
<li>(iii) 有用部分用 2 µs（一个基带符号）而不是 NT<sub>S</sub> = 8 µs，得出 10 log₁₀11 的错误答案。</li>
<li>(iii) 功率损失写成 20/28 或 28/8 而不换成 dB。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) h<sub>0</sub> = 1, h<sub>1</sub> = 0.3, N = 4. The sub-channel gains are H<sub>k</sub> = Σ<sub>i</sub> h<sub>i</sub>e<sup>−j2πik/N</sup> = 1 + 0.3e<sup>−jπk/2</sup>: H₁ = 1 − 0.3j, H₂ = 0.7, H₃ = 1 + 0.3j, H₄ = H₀ = 1.3.</p>
<p>(ii) Sampling the OFDM block at t = iT/N, i = 0, 1, …, N − 1, gives x<sub>i</sub> = (1/√T)Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub>e<sup>j2πki/N</sup>. Apart from a constant scaling factor, this is exactly the N-point inverse DFT of {s<sub>k</sub>}: the N frequency-domain symbols are transformed into N time-domain samples. Hence the OFDM modulator can be implemented with an IFFT, and the receiver demodulates with an FFT.</p>
<p>(iii) The useful OFDM symbol duration is NT<sub>S</sub> = 4 × 2 µs = 8 µs. With a cyclic prefix of 20 µs, the OFDM symbol duration is 8 + 20 = 28 µs. Power loss due to the cyclic prefix = 10 log₁₀[(NT<sub>S</sub> + T<sub>G</sub>)/NT<sub>S</sub>] = 10 log₁₀(28/8) ≈ 5.44 dB.</p></div>
<div class="ans">一句话：H<sub>k</sub> = 1 + 0.3e<sup>−jπk/2</sup> 得 {1−0.3j, 0.7, 1+0.3j, 1.3}；按 t = iT/N 采样就是 IDFT；块长 8 + 20 = 28 µs，功率损失 10 log₁₀3.5 ≈ 5.44 dB。</div>
'''},

'y2526s2-q3a': {'title': '知识讲解 + 详细解析：簇复制次数与系统容量', 'zh': '''
<h4><span class="st">知识讲解</span>频率复用和系统容量</h4>
<p>运营商只有一组有限的信道（本题 1071 条）。蜂窝系统的办法是（Part A p.78–81）：</p>
<ul>
<li>把 N 个相邻小区组成一个<b>簇</b>（cluster），簇内 N 个小区分完全部 S 条信道，相邻小区频率不同，避免干扰；均匀固定分配时每小区 S/N 条。</li>
<li>整个服务区由 C 个簇拼成，每个簇都重复使用同一组 S 条信道（频率复用，frequency reuse），相同频率之间隔开复用距离 D = R√(3N)。</li>
<li>系统容量（全系统能同时提供的信道总数）T = C × N × S/N = C × S（p.81）。</li>
</ul>
<p>所以容量的来源就是"复制了几次簇"：簇越小（N 越小），簇面积越小，复制次数越多，容量越大，但同频小区靠得更近，干扰更强（p.78：N 的选择是容量和服务质量之间的折中）。</p>
<h4><span class="st">详细解析</span>逐步计算</h4>
<ol>
<li><b>每小区信道</b>：
<div class="calc">S/N = 1071 / 7 = 153 条/小区</div></li>
<li><b>每簇面积</b>：一个簇有 7 个小区，每个 6 km²：
<div class="calc">7 × 6 = 42 km²</div></li>
<li><b>复制次数</b>：
<div class="calc">C = 2100 / 42 = 50 次（共 50 × 7 = 350 个小区）</div></li>
<li><b>系统容量</b>：
<div class="calc">T = C × S = 50 × 1071 = 53 550 条信道（= 153 × 350）</div></li>
</ol>
<p><b>检查</b>：两种算法（每簇信道 × 簇数，每小区信道 × 小区数）结果相同。1071 条信道被重复用了 50 次，容量放大了 50 倍。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>系统容量答成 1071：那只是一个簇的信道数。</li>
<li>复制次数用小区面积去除：2100/6 = 350 是小区数，不是簇数。</li>
<li>答案不写单位（条信道、km²、次）。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) Number of channels per cell = 1071/7 = 153 channels. Coverage area of each cluster = 7 × 6 km² = 42 km².</p>
<p>(ii) Number of times the cluster is replicated = 2100/42 = 50 (i.e. 350 cells in total).</p>
<p>(iii) System capacity = (channels per cluster) × (number of clusters) = 1071 × 50 = 53 550 channels (= 153 × 350). The same set of 1071 channels is reused 50 times through frequency reuse.</p></div>
<div class="ans">一句话：每小区 1071/7 = 153 条，簇面积 42 km²，复制 2100/42 = 50 次，系统容量 1071 × 50 = 53 550 条信道。</div>
'''},

'y2526s2-q3bc': {'title': '知识讲解 + 详细解析：Erlang C 与 M/M/m', 'zh': '''
<h4><span class="st">知识讲解</span>(b) 话务量和 Erlang C</h4>
<p>话务量 A = λH（Erlang），每用户话务量 A<sub>u</sub> = λ<sub>u</sub>H（Part A p.104、p.115）。题目说的是 <b>Erlang C 系统</b>：所有信道都忙时，新呼叫<b>排队等待</b>（blocked calls delayed，p.125），给的 5% 是"呼叫需要等待的概率"。查附录 Erlang C 表的 5% 列，表里没有的信道数用线性插值（p.127）。老师提醒先确认用对表（B 还是 C）。</p>
<h4><span class="st">知识讲解</span>(c) M/M/m 排队模型和生灭过程</h4>
<p>M/M/m：到达是泊松过程（M）、服务时间是指数分布（M）、有 m 个服务台（m 条信道）（Kendall 记号，p.102）。<b>状态 k</b> = 系统里正在通话和排队的呼叫总数。</p>
<ul>
<li>到达率 λ<sub>k</sub> = λ：不管系统里有多少人，新呼叫都以速率 λ 到来（k → k+1）。</li>
<li>服务率 μ<sub>k</sub>：每条忙的信道以速率 μ 结束通话。k ≤ m 时 k 条信道都在服务，μ<sub>k</sub> = kμ；k ≥ m 时只有 m 条信道，其余在排队，μ<sub>k</sub> = mμ 封顶（p.106）。</li>
<li><b>平衡方程</b>：稳态时，相邻两个状态之间"向右流的概率流 = 向左流的概率流"：λP<sub>k−1</sub> = μ<sub>k</sub>P<sub>k</sub>。</li>
</ul>
<p>老师说 M/M/m 的<b>状态转移图要会画</b>，会列平衡方程、递推求 P<sub>k</sub> 和 P₀，本题 (c) 就考了。</p>
<h4><span class="st">详细解析</span>(b) 三小问</h4>
<ol>
<li><b>(i)</b> 每小区 1071/7 = 153 条信道，查 Erlang C 表 5% 列，在 150 和 155 之间插值。按公式算出的表值约为 A(150) ≈ 129.5、A(155) ≈ 134.1（以考场附录为准）：
<div class="calc">A(153) ≈ 129.5 + (153 − 150)/(155 − 150) × (134.1 − 129.5) = 129.5 + 2.76 ≈ 132.2 Erlang/小区</div></li>
<li><b>(ii)</b>
<div class="calc">每小区用户 = 132.2 / 0.03 ≈ 4408；每 km² = 4408 / 6 ≈ 735 用户/km²</div></li>
<li><b>(iii)</b>
<div class="calc">H = A<sub>u</sub>/λ<sub>u</sub> = 0.03/1.2 小时 = 0.025 h = 0.025 × 3600 = 90 s</div></li>
</ol>
<h4><span class="st">详细解析</span>(c)(i) 画状态转移图</h4>
<p>画法：一排圆圈标 0, 1, 2, …, m−1, m, m+1, …；每两个相邻圆圈之间画一对箭头。上面向右的箭头全标 λ；下面向左的箭头依次标 μ, 2μ, 3μ, …, mμ（从状态 k 回到 k−1 的速率是 μ<sub>k</sub>），从 m → m−1 起一直都是 mμ。最后在右边画省略号表示状态无限多（队列无限长）。</p>
<h4><span class="st">详细解析</span>(c)(ii) 推导 P<sub>k</sub></h4>
<ol>
<li><b>k ≤ m</b>：kμP<sub>k</sub> = λP<sub>k−1</sub> → P<sub>k</sub> = (ρ/k)P<sub>k−1</sub>，ρ = λ/μ。一路往下递推：
<div class="calc">P₁ = ρP₀，P₂ = (ρ/2)P₁ = (ρ²/2!)P₀，…，P<sub>k</sub> = P₀ρ<sup>k</sup>/k!，k ≤ m</div></li>
<li><b>k ≥ m</b>：mμP<sub>k</sub> = λP<sub>k−1</sub> → P<sub>k</sub> = (ρ/m)P<sub>k−1</sub>。从 P<sub>m</sub> = P₀ρ<sup>m</sup>/m! 出发，再乘 (k − m) 次 ρ/m：
<div class="calc">P<sub>k</sub> = P₀(ρ<sup>m</sup>/m!)(ρ/m)<sup>k−m</sup> = P₀ρ<sup>k</sup>/(m!·m<sup>k−m</sup>)，k ≥ m</div></li>
<li><b>检查</b>：k = m 时两式都等于 P₀ρ<sup>m</sup>/m!，一致。</li>
<li><b>P₀</b>（题目没要求，但老师说要会）：由 ΣP<sub>k</sub> = 1，k ≥ m 的部分是公比 ρ/m 的等比数列，要求 ρ/m &lt; 1（否则队列无限增长）：
<div class="calc">P₀ = [Σ<sub>k=0</sub><sup>m−1</sup> ρ<sup>k</sup>/k! + (ρ<sup>m</sup>/m!)·1/(1 − ρ/m)]⁻¹</div>
"所有信道都忙、必须排队"的概率 ΣP<sub>k</sub>（k ≥ m）就是 Erlang C 公式（p.110）。</li>
</ol>
<p><b>数字小例子</b>（自己验算用）：m = 3、ρ = 2。P₀ = 1/[1 + 2 + 2 + (8/6) × 3] = 1/9；排队概率 = (8/6)(1/9) × 3 = 4/9 ≈ 0.444，和 Erlang C 公式算出的 E<sub>2,3</sub>(2) 相同。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>(b) 用了 Erlang B 表；153 条不插值。</li>
<li>(b)(iii) H 算出 0.025 后不换成秒（题目要秒）。</li>
<li>(c) 向左箭头全写 μ，或 k ≥ m 后还写 kμ：服务率最多 mμ。</li>
<li>题目平衡式写成"mμP<sub>k</sub> = λP<sub>k</sub>"，应是 λP<sub>k−1</sub>（讲义 p.106），按 P<sub>k−1</sub> 推导，可在答卷上注明。</li>
<li>记号：题目的 ρ = λ/μ（就是话务量 A）；讲义 p.105 把 ρ = λ/(mμ) 叫利用率。按题目的定义写，稳定条件就是 ρ/m &lt; 1。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(b)(i) Channels per cell = 1071/7 = 153. From the Erlang C table with a delay probability of 5%, interpolating between M = 150 (A ≈ 129.5 E) and M = 155 (A ≈ 134.1 E): A ≈ 129.5 + (3/5)(4.6) ≈ 132.2 Erlangs per cell.</p>
<p>(ii) Users per cell = 132.2/0.03 ≈ 4408. Users per km² = 4408/6 ≈ 735 users/km².</p>
<p>(iii) H = A<sub>u</sub>/λ = 0.03/1.2 h = 0.025 h = 90 s.</p>
<p>(c)(i) [Sketch: states 0, 1, 2, …, m − 1, m, m + 1, … in a row. Each forward transition k → k + 1 has rate λ. Each backward transition k → k − 1 has rate kμ for k ≤ m (μ, 2μ, …, mμ) and mμ for k &gt; m.]</p>
<p>(ii) For k ≤ m: kμP<sub>k</sub> = λP<sub>k−1</sub>, so P<sub>k</sub> = (ρ/k)P<sub>k−1</sub>. Applying this recursively, P<sub>k</sub> = P₀ρ<sup>k</sup>/k!.</p>
<p>For k ≥ m: mμP<sub>k</sub> = λP<sub>k−1</sub>, so P<sub>k</sub> = (ρ/m)P<sub>k−1</sub>. Starting from P<sub>m</sub> = P₀ρ<sup>m</sup>/m!, P<sub>k</sub> = P₀(ρ<sup>m</sup>/m!)(ρ/m)<sup>k−m</sup> = P₀ρ<sup>k</sup>/(m!·m<sup>k−m</sup>).</p>
<p>Both expressions agree at k = m. P₀ is obtained from ΣP<sub>k</sub> = 1, which requires ρ/m &lt; 1.</p></div>
<div class="ans">一句话：153 条查 Erlang C 表 5% 插值约 132.2 E，÷0.03 ÷6 ≈ 735 用户/km²，H = 0.025 h = 90 s；M/M/m 由 λP<sub>k−1</sub> = μ<sub>k</sub>P<sub>k</sub> 递推，k ≤ m 时 P₀ρ<sup>k</sup>/k!，k ≥ m 时 P₀ρ<sup>k</sup>/(m!m<sup>k−m</sup>)。</div>
'''},

'y2526s2-q4a': {'title': '知识讲解 + 详细解析：硬切换与软切换', 'zh': '''
<h4><span class="st">知识讲解</span>什么是切换</h4>
<p>手机通话时从一个小区移动到另一个小区，信号越来越弱，必须把通话从旧基站转交给新基站，这就是<b>切换</b>（handover / handoff）。基站收到的信号降到切换门限 P<sub>HO</sub>（略高于最低可用电平 P<sub>min</sub>）时就要开始切换（Part A p.153）；如果新小区没有空闲信道、交换中心处理太慢，或者目标链路失败，通话就会掉线。地面蜂窝系统有两种切换（p.154–155）。</p>
<h4><span class="st">详细解析</span>两种切换展开</h4>
<ol>
<li><b>硬切换（hard handover）——"先断后连"（break before make）</b>（p.154）：
<ul><li>机制：先释放和旧基站之间的信道，再和新基站建立新信道。任何时刻手机只连一个基站。</li>
<li>特点：实现简单；但有短暂的通信中断，可能掉话。</li>
<li>使用的系统：<b>基于 FDMA/TDMA 的系统</b>，如 GSM、IS-136。</li></ul></li>
<li><b>软切换（soft handover）——"先连后断"（make before break）</b>（p.155）：
<ul><li>机制：先和新基站建立信道，新旧两条信道同时用于通信，确认新链路可靠后才断开旧的。</li>
<li>特点：在小区边界上同时收两个基站的信号，有分集增益，边界上的通信质量改善；切换过程中通信不中断。</li>
<li>使用的系统：<b>基于 CDMA 的系统</b>，如 IS-95、WCDMA、cdma2000。</li></ul></li>
</ol>
<p><b>为什么是这样分</b>（讲义没写，是理解用的补充）：CDMA 相邻小区用同一个频率，靠不同的码区分，手机不用换频就能同时和两个基站通信，所以能做软切换；FDMA/TDMA 相邻小区频率不同，手机一般只有一套收发信机，只能先断开再换到新频率。</p>
<p><b>记忆</b>："硬"是断了再接，"软"是接上再断。4 分题：每种机制 1 分 + 系统 1 分。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>"break before make"和"make before break"写反。</li>
<li>只写机制不写系统，或者只写"CDMA"不举具体系统名；写出 GSM、IS-136、IS-95、WCDMA、cdma2000 更稳。</li>
<li>把软切换的优点写成"更简单"：软切换更复杂，优点是不中断、有分集。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p><b>Hard handover ("break before make"):</b> the current channel with the old base station is released before the new channel with the new base station is set up, so the mobile is connected to only one base station at a time. It is simple to implement, but there is a short interruption of communication and the call may be dropped. Hard handover is used in FDMA/TDMA-based systems such as GSM and IS-136.</p>
<p><b>Soft handover ("make before break"):</b> a new channel with the new base station is set up in parallel with the current channel with the old base station, and both channels are used simultaneously before the old one is released. The availability of diversity improves the link at the cell boundary, and there is no interruption of communication during the handover. Soft handover is used in CDMA-based systems such as IS-95, WCDMA and cdma2000.</p></div>
<div class="ans">一句话：硬切换先断后连，简单但有中断，用于 FDMA/TDMA（GSM、IS-136）；软切换先连后断，新旧同时用、有分集不中断，用于 CDMA（IS-95、WCDMA、cdma2000）。</div>
'''},

'y2526s2-q4b': {'title': '知识讲解 + 详细解析：LEO/MEO 卫星的四种切换', 'zh': '''
<h4><span class="st">知识讲解</span>为什么 LEO/MEO 卫星系统会有切换</h4>
<p>GEO（地球静止轨道）卫星相对地面不动，地面用户一直看到同一颗卫星。MEO（中轨）和 LEO（低轨）卫星相对地面高速运动，一颗 LEO 卫星对某个地点只可见十几分钟。如果卫星本身充当基站（卫星上载有基站功能），那么除了用户移动，<b>卫星自己的运动</b>也会引起切换（Part C p.40）。讲义列出 4 种，按范围从小到大记：<b>波束 → 卫星 → 网关 → 系统</b>。老师说卫星这部分讲得少，但期末考过的就是这一题。</p>
<h4><span class="st">详细解析</span>四种切换逐个展开（8 分，每种 2 分：名称 + 起因/机制）</h4>
<ol>
<li><b>星内切换（intra-satellite handover）</b>：一颗卫星用多个点波束把覆盖区分成多个扇区（类似蜂窝的小区）。用户在<b>同一颗卫星</b>的覆盖范围内从一个扇区移到另一个扇区时，换到另一个波束（换频率/信道），卫星不变。</li>
<li><b>星间切换（inter-satellite handover）</b>：用户从一颗卫星的覆盖区移到另一颗卫星的覆盖区，<b>或者卫星自己飞走了</b>，通话要转给下一颗卫星。LEO 卫星运动快、每颗可见时间短，这种切换很频繁。</li>
<li><b>网关切换（gateway handover）</b>：卫星通过地面网关（gateway）接入地面网络。卫星移动后离开了当前连接的网关，就要换到另一个网关（即使用户没有动）。</li>
<li><b>系统间切换（inter-system handover）</b>：在<b>卫星系统和地面蜂窝系统之间</b>的切换。例如用户进入城市、地面蜂窝信号更好时，从卫星切到蜂窝；反之亦然。依据是信号强度和 QoS 性能，它是一种<b>垂直切换</b>（vertical handover，不同类型网络之间）。</li>
</ol>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>只写四个名字：每个都要写起因（用户移动还是卫星移动）。</li>
<li>星间切换只写"用户移动"，漏了"卫星飞走"这个卫星系统特有的原因。</li>
<li>系统间切换要写出"垂直切换"和"依据信号强度和 QoS"。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>In MEO/LEO systems the satellites move relative to the earth, so if a satellite acts as a base station, handovers are caused not only by the movement of the users but also by the movement of the satellites. Four types of handover can occur:</p>
<p>1. <b>Intra-satellite handover:</b> caused by the movement of a mobile user within the coverage of one satellite from one sector (spot beam) to another. The user is switched to another beam/channel of the same satellite.</p>
<p>2. <b>Inter-satellite handover:</b> caused by the movement of a user from the coverage of one satellite to that of another, or by the satellite moving away. The connection is handed over to the next satellite. This is frequent in LEO systems because each satellite is visible for only a short time.</p>
<p>3. <b>Gateway handover:</b> caused by the movement of the satellite away from the current ground gateway, so the satellite link has to be switched to another gateway, even if the user does not move.</p>
<p>4. <b>Inter-system handover:</b> a handover between the satellite system and a terrestrial cellular system, based on signal strength and QoS performance. This is a vertical handover between two different types of network.</p></div>
<div class="ans">一句话：星内（同一卫星换波束）、星间（换卫星，用户动或卫星飞走）、网关（卫星离开当前网关）、系统间（卫星与地面蜂窝之间的垂直切换）。</div>
'''},

'y2526s2-q4c': {'title': '知识讲解 + 详细解析：传感器网络的通信架构', 'zh': '''
<h4><span class="st">知识讲解</span>无线传感器网络是什么</h4>
<p>无线传感器网络（WSN，Wireless Sensor Network）由大量小型传感器节点组成，密集地布在要监测的区域里，采集温度、振动等数据。它借用了无线自组网（ad hoc）的技术，但有自己的特点（Part B p.56）：节点数量比 ad hoc 网络多几个数量级；节点密集部署、容易失效，拓扑变化频繁；节点用广播方式通信，而 ad hoc 是点对点；节点的电量、计算能力和存储都很有限。这些特点决定了它的通信方式：<b>没有基础设施、多跳转发</b>。</p>
<h4><span class="st">详细解析</span>通信架构的要点（Part B p.57–58）</h4>
<ol>
<li><b>传感区域（sensor field）</b>：传感器节点散布在传感区域里，每个节点既能采集数据，也能把数据路由回汇聚节点。</li>
<li><b>汇聚节点（sink）</b>：所有数据最终送到 sink。数据以<b>多跳、无基础设施</b>（multi-hop, infrastructureless）的方式，一个节点接一个节点地转发到 sink。为什么多跳：每个节点电量有限、发射功率小，覆盖距离短，靠邻居接力既省电又能覆盖大片区域。</li>
<li><b>任务管理节点（task manager node）</b>：sink 通过<b>互联网或卫星</b>与任务管理节点通信。网络的管理者（用户）在任务管理节点获取数据，也从那里向网络下发任务（查询、指令沿相反方向传回节点）。</li>
<li><b>信息回传的路径</b>：传感器 A → 传感器 B → 传感器 C → … → sink → Internet/卫星 → task manager（用户）。</li>
</ol>
<p><b>作图提示</b>：画一个方框表示 sensor field，里面画很多小圆点，从某个节点 A 画几段箭头经过 B、C 到 sink（标"multi-hop"）；sink 在方框边上，再画箭头到云（Internet/satellite），最后到 task manager 和 user。题目说 "show how"，画图加文字最稳。</p>
<h4><span class="st">详细解析</span>加分点（时间够再写）</h4>
<ul>
<li><b>设计影响因素</b>（p.57）：可靠性（容错）、可扩展性、生产成本、工作环境、网络拓扑、硬件约束、传输介质、功耗。</li>
<li><b>协议栈</b>（p.59）：物理层、数据链路（MAC）层、网络层、传输层、应用层五层，加上功耗管理、移动性管理、任务管理三个平面。老师说协议栈记住五层就行，功耗是最关键的因素，因为节点大多靠电池。</li>
</ul>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>写成每个节点直接发给基站（单跳）：讲义强调的是多跳、无基础设施。</li>
<li>漏了 sink 到 task manager 这一段（经 Internet 或卫星）。</li>
<li>只罗列协议栈各层，没讲"信息怎么一路传回管理者"，题目问的重点是后者。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>The sensor nodes are scattered in a sensor field. Each sensor node has the capability to collect data and to route data back to the sink. Since the nodes have limited power and short transmission range, data are routed back to the sink through a multi-hop, infrastructureless architecture: each node forwards its data to a neighbouring node, which relays it hop by hop towards the sink.</p>
<p>The sink then communicates with the task manager node via the Internet or a satellite link. The manager (user) obtains the sensed information at the task manager node and can also send tasks/queries back to the sensor nodes in the reverse direction.</p>
<p>[Sketch: sensor node A → B → C → … → Sink → Internet/Satellite → Task manager node → User.]</p>
<p>The design of this architecture is influenced by reliability (fault tolerance), scalability, production cost, operating environment, network topology, hardware constraints, transmission media and power consumption. Each node uses a protocol stack of physical, data link, network, transport and application layers, together with power, mobility and task management planes.</p></div>
<div class="ans">一句话：传感器节点采集数据，多跳、无基础设施地接力转发到 sink，sink 再经 Internet 或卫星送到任务管理节点，管理者在那里取数据、下发任务。</div>
'''},

'y2526s2-q4d': {'title': '知识讲解 + 详细解析：IoT 通信网络层四个子层', 'zh': '''
<h4><span class="st">知识讲解</span>IoT 核心功能栈</h4>
<p>讲义用 Cisco 的简化框架描述 IoT 的核心功能栈（Part B p.89–90），老师说这个框架最好理解。它有三层：</p>
<ul>
<li><b>第 1 层"物"层</b>（things：传感器和执行器）：物理设备要适应部署环境的限制，同时提供所需的信息。</li>
<li><b>第 2 层通信网络层</b>（communications network layer）：智能物体不能自给自足时，要和外部系统通信，通常用无线技术。本题问的就是这一层，它分成<b>四个子层</b>。</li>
<li><b>第 3 层应用与分析层</b>：处理采集到的数据，控制智能物体、做智能决策。</li>
</ul>
<p>四个子层可以按数据的走向记："<b>接入 → 汇聚回传 → 传输（IP）→ 管理（应用协议）</b>"：数据先从物体无线接入，在网关汇聚后回传，用 IP/TCP/UDP 在网络里传输，最后由应用协议和头端应用交换。</p>
<h4><span class="st">详细解析</span>四个子层逐个展开（8 分，每个 2 分：名称 + 特点/例子）</h4>
<ol>
<li><b>接入网子层（access network sublayer）</b>（p.89、p.93–97）：IoT 网络的"最后一公里"，通常是无线技术，如 IEEE 802.11ah、802.15.4g、LoRa。选什么技术取决于通信距离（按范围分 PAN、HAN、NAN、FAN、LAN、MAN、WAN）、一个采集单元里的物体数量和吞吐量、成本和功耗；拓扑可以是点对点，也可以是点对多点（星形、簇状星形、mesh）。</li>
<li><b>网关与回传子层（gateways and backhaul network sublayer）</b>（p.89、p.98）：把一片区域里的多个智能物体组织到一个公共网关上，网关负责不同介质之间的通信，用更长距离的介质（如蜂窝、光纤）把采集的信息转发到头端中心站。物体可以静止或在小范围内移动，网关通常是固定的。</li>
<li><b>网络传输子层（network transport sublayer）</b>（p.90、p.98–99）：要实现成功的通信，必须有网络层和传输层协议，如 IP 和 UDP/TCP，以支持各种设备和介质。协议要开放、基于标准，能扩展到成千上万甚至数百万个传感器，并保证安全。IP 满足这些要求，也能用于低功耗、高丢包、低带宽的网络；在 IP 之上，用 TCP 由网络控制可靠交付，或用 UDP 把控制交给应用。</li>
<li><b>IoT 网络管理子层（IoT network management sublayer）</b>（p.90、p.99）：额外的应用层协议，让头端应用能和传感器交换数据。例如基于 TCP 的 HTTP（传感器作为客户端连接 IoT 应用），以及 WebSocket：一种轻量、源自 Web 的协议，适应低内存、低功耗、低带宽、高丢包的环境，在智能物体和外部应用之间提供简单的双向连接。</li>
</ol>
<p>这道题和 2024-25 Q4(b) 一样，四年里考了两次，属于必背内容。</p>
<h4><span class="st">易错</span>常见失分点</h4>
<ul>
<li>把三层（物、通信网络、应用分析）当成四个子层来答：题目问的是通信网络层<b>里面</b>的四个子层。</li>
<li>只写名称不写特点，或者每个子层不举例子（802.11ah/LoRa、IP/UDP/TCP、HTTP/WebSocket）。</li>
<li>顺序乱：按"接入 → 网关回传 → 传输 → 管理"写最清楚。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>The communications network layer of the core IoT functional stack has four sublayers:</p>
<p>1. <b>Access network sublayer:</b> the last mile of the IoT network, typically made up of wireless technologies such as IEEE 802.11ah, 802.15.4g and LoRa. The choice of technology depends on the communication range (PAN, HAN, NAN, FAN, LAN, MAN, WAN), the number of objects and throughput per collection cell, cost and power consumption. Topologies can be point-to-point or point-to-multipoint (star, clustered star, mesh).</p>
<p>2. <b>Gateways and backhaul network sublayer:</b> multiple smart objects in a given area are organised around a common gateway, which is in charge of the inter-medium communication and forwards the collected information through a longer-range medium (backhaul) to a headend central station. The smart objects may be static or mobile within a limited area, while the gateway is usually static.</p>
<p>3. <b>Network transport sublayer:</b> network and transport layer protocols such as IP and UDP/TCP are implemented to support the variety of devices and media. The protocol must be open and standards-based, scalable to thousands or millions of sensors, and secure. IP meets these requirements, even over low-power, lossy, low-bandwidth networks; TCP or UDP is chosen depending on whether the network or the application controls the delivery.</p>
<p>4. <b>IoT network management sublayer:</b> additional application protocols allow the headend applications to exchange data with the sensors, for example HTTP over TCP (the sensor acting as a client) and WebSocket, a lightweight web-derived protocol that provides a simple bidirectional connection in low-memory, low-power, low-bandwidth and high-loss environments.</p></div>
<div class="ans">一句话：通信网络层四子层是接入网（最后一公里无线：802.11ah、802.15.4g、LoRa）、网关与回传（汇聚后长距离送到中心）、网络传输（IP + UDP/TCP，开放、可扩展、安全）、IoT 网络管理（HTTP、WebSocket 等应用协议）。</div>
'''},
}

NOTES = '''y2526s1-q1b1: the computed diversity gain d ≈ 3.0 exceeds the number of branches (2), while Ch4 p.28 states d ≤ M. The existing solution already notes this (high-SNR single-point approximation); the box explains it neutrally and keeps d ≈ 3.0.
y2526s2-q3bc: the question uses ρ = λ/μ (the traffic A), whereas Part A slide p.105 defines utilization ρ = λ/(mμ); the box follows the question and states the stability condition as ρ/m less than 1. (The question's typo "mμP_k = λP_k" is already flagged in the existing solution.)
y2526s1-q3b / y2526s2-q3bc: the Erlang C table is not available as text, so the interpolation end points (A(110) ≈ 92.5, A(115) ≈ 97.1, A(150) ≈ 129.5, A(155) ≈ 134.1) were computed from the Erlang C formula; the box says "以考场附录为准". Results agree with the existing solution (93.4, 132.2).'''

