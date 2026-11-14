# -*- coding: utf-8 -*-
# 知识讲解 + 详细解析 for EE6129 past final exams 2023-24 S2 and 2024-25 S2 (group exA).
# Numbers checked by check_exA.py (run with /usr/bin/python3).

XPL = {

# ====================================================================== 2023-24 S2
'y2324s2-q1a': {'title': '知识讲解 + 详细解析：路径损耗直线、阴影中断、衰落类型、衰落余量', 'zh': '''
<h4><span class="st">知识讲解</span>① 为什么要把路径损耗模型化成 dB</h4>
<p>路径损耗（path loss）描述信号功率随距离变弱。线性形式 P<sub>r</sub> = P<sub>t</sub>K d<sup>−γ</sup>ψ 是几个量相乘，不好画也不好算；两边取 10 log₁₀ 以后，乘法变加法，d 的幂次变成系数，整个模型就成了一条直线（讲义第 2 章 p.8–12）。</p>
<ul><li><b>K</b>：和天线、频率有关的常数，K<sub>dB</sub> = 10 log₁₀K，一般是负数（例如 −30 dB）。</li>
<li><b>γ</b>：路径损耗指数（path loss exponent），自由空间是 2，城区一般 3–5。含义：距离每变成 10 倍，损耗多 10γ dB。</li>
<li><b>ψ</b>：阴影衰落（shadowing），由楼房、地形遮挡造成。取 dB 后 ψ<sub>dB</sub> 是零均值的高斯随机变量，方差 σ²（单位 dB²），所以叫对数正态（log-normal）阴影。</li></ul>
<p>老师课上强调：简化路径损耗模型的线性形式和 dB 形式<b>都要背</b>，考试不给。</p>
<h4><span class="st">知识讲解</span>② 本题另外三个概念</h4>
<div class="tw"><table class="mini"><thead><tr><th>概念</th><th>判据 / 公式</th><th>讲义</th></tr></thead><tbody>
<tr><td>阴影中断概率</td><td>P<sub>out</sub> = Q((μ − P<sub>min</sub>)/σ)</td><td>第 2 章 p.14–15</td></tr>
<tr><td>平坦衰落（flat fading）</td><td>σ<sub>τ</sub>/T<sub>s</sub> &lt; 0.1</td><td>p.33</td></tr>
<tr><td>慢衰落（slow fading）</td><td>T<sub>s</sub> 远小于相干时间 T<sub>C</sub></td><td>p.37</td></tr>
<tr><td>衰落余量（fade margin）</td><td>FM = 10 log₁₀[1/ln(1/(1 − ε))]</td><td>p.51</td></tr>
</tbody></table></div>
<p>中断（outage）就是接收功率低于能正常工作的最低功率 P<sub>min</sub>。P<sub>r,dB</sub> 服从高斯分布，"低于门限的概率"就是高斯曲线左尾的面积，用 Q 函数写出来：门限离均值越远（以 σ 为单位计），中断越少。衰落余量是：在瑞利衰落信道里，平均 SNR 要比 AWGN 信道多给多少 dB，才能在中断概率 ε 下得到同样的容量。</p>
<h4><span class="st">详细解析</span>(i) 化 dB 并画图</h4>
<ol><li><b>做什么</b>：两边取 10 log₁₀。<b>为什么</b>：log 把乘积拆成和，把 d<sup>−γ</sup> 变成 −γ·10 log₁₀d。<b>得到</b>：P<sub>r,dB</sub> = P<sub>t,dB</sub> + K<sub>dB</sub> − γ·10 log₁₀d + ψ<sub>dB</sub>。</li>
<li>路径损耗 = 发射 − 接收：P<sub>L,dB</sub> = −K<sub>dB</sub> + γ·(10 log₁₀d) − ψ<sub>dB</sub>。</li>
<li>画图：横轴 x = 10 log₁₀d（"距离的 dB"），纵轴 P<sub>L,dB</sub>。去掉随机项就是 y = −K<sub>dB</sub> + γx：<b>斜率 γ</b>，在 x = 0（d = 1）处<b>截距 −K<sub>dB</sub></b>；实测点因为 ψ<sub>dB</sub> 散在直线上下。例：γ = 3 时，d 从 10 m 到 100 m，横轴走 10 dB，损耗多 30 dB。</li></ol>
<h4><span class="st">详细解析</span>(ii) 求 ψ<sub>dB</sub> 方差的上限</h4>
<ol><li>写中断概率：均值比门限高 10 dB，所以 P<sub>out</sub> = Q(10/σ)。</li>
<li>倒查 Q 表：找 Q(x) ≈ 0.01，表中 Q(2.33) = 0.0099，所以 x ≈ 2.33（精确值 2.326）。</li>
<li>Q 是减函数：要 P<sub>out</sub> &lt; 0.01，就要 10/σ &gt; 2.33。</li></ol>
<div class="calc">σ &lt; 10/2.326 = 4.30 dB</div>
<div class="calc">σ² &lt; 4.30² = 18.5 dB²</div>
<p>检查：若 σ = 5 dB，Q(10/5) = Q(2) = 0.0228，大于 1%，确实不满足。σ 越大，点散得越开，掉到门限下面的机会越多。</p>
<h4><span class="st">详细解析</span>(iii) 两个维度判衰落类型</h4>
<ol><li><b>频率维</b>（时延扩展和符号时长比）：σ<sub>τ</sub>/T<sub>s</sub> = 0.01 ms / 1 ms = 0.01 &lt; 0.1 → <b>平坦衰落</b>。直觉：多径回波最多只拖 1% 个符号，几乎没有符号间干扰（ISI）。</li>
<li><b>时间维</b>（信道变化快慢和符号时长比）：冲激响应不随时间变，说明没有多普勒扩展，相干时间趋于无穷，T<sub>s</sub> 远小于 T<sub>C</sub> → <b>慢衰落</b>。</li>
<li>结论：平坦、慢衰落（flat, slow fading）。老师改卷时说过：只答一个维度只给一半分。</li></ol>
<h4><span class="st">详细解析</span>(iv) 衰落余量</h4>
<div class="calc">ln(1/(1 − 0.001)) = ln(1.001001) = 0.0010005</div>
<div class="calc">FM = 10 log₁₀(1/0.0010005) = 10 log₁₀(999.5) ≈ 30.0 dB</div>
<p>计算器提示：ε 很小时 ln(1/(1 − ε)) ≈ ε，所以 FM ≈ 10 log₁₀(1/ε)：ε = 10⁻² → 20 dB（讲义例子），ε = 10⁻³ → 30 dB。物理意义：瑞利信道的平均 SNR 要比最低需要的 SNR 高 1000 倍，才能保证只有 0.1% 的时间掉到最低值以下。</p>
<h4><span class="st">易错</span>注意这几点</h4>
<ul><li>截距是 −K<sub>dB</sub>（纵轴是"损耗"），不是 K<sub>dB</sub>。</li>
<li>(ii) 问的是方差：写 σ² &lt; 18.5 dB²，同时写出 σ &lt; 4.3 dB。</li>
<li>Q(x) = 0.01 要倒查表：在表的正文里找最接近 0.01 的数，再读出 x。</li>
<li>(iii) 频率、时间两个维度都要答，并写出理由。</li>
<li>(iv) 里的 ln 是自然对数，不是 log₁₀。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) Taking 10 log₁₀ of both sides: P<sub>r,dB</sub> = P<sub>t,dB</sub> + K<sub>dB</sub> − 10γ log₁₀d + ψ<sub>dB</sub>. The path loss in dB is P<sub>L,dB</sub> = P<sub>t,dB</sub> − P<sub>r,dB</sub> = −K<sub>dB</sub> + γ(10 log₁₀d) − ψ<sub>dB</sub>. Plotting P<sub>L,dB</sub> against 10 log₁₀d gives a straight line with slope γ and intercept −K<sub>dB</sub> at d = 1 (0 dB). The shadowing term ψ<sub>dB</sub> is a zero-mean Gaussian random variable, so the measured points scatter about this line.</p>
<p>(ii) P<sub>r,dB</sub> is Gaussian with standard deviation σ (in dB). P<sub>out</sub> = P(P<sub>r,dB</sub> &lt; P<sub>min</sub>) = Q((μ − P<sub>min</sub>)/σ) = Q(10/σ) &lt; 0.01. From the Q-function table, Q(2.33) ≈ 0.01, so 10/σ &gt; 2.33, σ &lt; 4.30 dB, and the maximum variance of ψ<sub>dB</sub> is σ² ≈ 18.5 dB².</p>
<p>(iii) σ<sub>τ</sub>/T<sub>s</sub> = 0.01 ms / 1 ms = 0.01 &lt; 0.1, so the delay spread is negligible compared with the symbol duration and there is no significant ISI: the channel is flat fading. The impulse response is time invariant, so there is no Doppler spread and the coherence time is much longer than T<sub>s</sub>: the channel is slow fading. Hence it is a flat, slow fading channel.</p>
<p>(iv) To achieve the same capacity as the AWGN channel, the required fade margin is FM = 10 log₁₀[1/ln(1/(1 − ε))]. With ε = 0.001, ln(1/0.999) = 1.0005 × 10⁻³, so FM = 10 log₁₀(999.5) ≈ 30 dB.</p></div>
<div class="ans">一句话：取 dB 后是一条直线（斜率 γ、截距 −K<sub>dB</sub>）；中断 = Q(余量/σ)，σ² &lt; 18.5 dB²；衰落类型两个维度都要答（平坦 + 慢）；衰落余量只看 ε，0.1% → 30 dB。</div>
'''},

'y2324s2-q1b1': {'title': '知识讲解 + 详细解析：选择分集的离散 SNR 平均与误码率', 'zh': '''
<h4><span class="st">知识讲解</span>选择分集（Selection Diversity）在做什么</h4>
<p>分集（diversity）的想法：把同一个信号经过几条<b>互相独立</b>的衰落路径（支路，branch）送到接收端，所有支路同时很差的概率远小于一条支路很差的概率。选择分集最简单：接收机看哪条支路的 SNR 最大，就只用那一条，输出 SNR = max(γ₁, γ₂, …)（讲义第 4 章 p.10–14）。</p>
<p>本题的 SNR 不是连续分布，而是<b>离散随机变量</b>（只取 10 dB、12 dB 两个值）。离散分布求平均就是"每个取值 × 它的概率，再相加"：E[X] = Σ x·p(x)。老师课上说：<b>不会考积分，但离散分布的平均误码率会考</b>。DPSK 的 P<sub>s</sub> = ½e<sup>−γ</sup> 是"太复杂、题目会给"的那类公式，但式中的 γ 必须是<b>线性值</b>。</p>
<div class="tw"><table class="mini"><thead><tr><th>支路 1</th><th>支路 2</th><th>概率</th><th>SD 输出</th></tr></thead><tbody>
<tr><td>10 dB</td><td>10 dB</td><td>0.2 × 0.2 = 0.04</td><td>10 dB</td></tr>
<tr><td>10 dB</td><td>12 dB</td><td>0.2 × 0.8 = 0.16</td><td>12 dB</td></tr>
<tr><td>12 dB</td><td>10 dB</td><td>0.8 × 0.2 = 0.16</td><td>12 dB</td></tr>
<tr><td>12 dB</td><td>12 dB</td><td>0.8 × 0.8 = 0.64</td><td>12 dB</td></tr>
</tbody></table></div>
<p>所以 SD 输出只有两种：10 dB（概率 0.04）和 12 dB（概率 0.16 + 0.16 + 0.64 = 0.96）。两条支路独立，所以概率可以相乘。</p>
<h4><span class="st">详细解析</span>一步一步算</h4>
<ol><li><b>dB 换线性</b>（为什么：公式里的 γ 和求平均都要用线性值）：10 dB → 10<sup>1.0</sup> = 10；12 dB → 10<sup>1.2</sup> = 15.85。计算器：10^(12÷10)。</li>
<li><b>每条支路接收信号的平均 SNR</b>：<div class="calc">γ̄ = 0.2 × 10 + 0.8 × 15.85 = 2 + 12.68 = 14.68 → 10 log₁₀14.68 = 11.67 dB</div></li>
<li><b>SD 输出的平均 SNR</b>（顺便写上，保险）：<div class="calc">0.04 × 10 + 0.96 × 15.85 = 15.61 → 11.94 dB</div></li>
<li><b>每种输出情况的误符号率</b>：<div class="calc">½e<sup>−10</sup> = 2.27×10⁻⁵；　½e<sup>−15.85</sup> = 6.54×10⁻⁸</div></li>
<li><b>按概率加权</b>（全概率公式）：<div class="calc">P̄<sub>s</sub> = 0.04 × 2.27×10⁻⁵ + 0.96 × 6.54×10⁻⁸ = 9.08×10⁻⁷ + 6.28×10⁻⁸ ≈ 9.71×10⁻⁷</div></li></ol>
<p><b>合理性检查</b>：不用分集时 P̄<sub>s</sub> = 0.2 × 2.27×10⁻⁵ + 0.8 × 6.54×10⁻⁸ ≈ 4.59×10⁻⁶。分集后约小 4.7 倍。原因很清楚：误码几乎全部来自"10 dB"这种差情况（9.08×10⁻⁷ 占总数约 94%），SD 把它出现的概率从 0.2 压到 0.04，正好约 5 倍。</p>
<h4><span class="st">易错</span>三个典型错误</h4>
<ul><li>直接平均 dB 值：0.2 × 10 + 0.8 × 12 = 11.6 dB，是错的；先在线性域平均再换 dB 才对（11.67 dB）。</li>
<li>把平均 SNR 代进 ½e<sup>−γ</sup>：½e<sup>−15.61</sup> ≈ 8.3×10⁻⁸，比正确答案小一个数量级。平均误码率 ≠ 平均 SNR 的误码率，必须对每种情况分别算再加权。</li>
<li>选择分集取<b>最大</b>，不是把两路 SNR 相加（相加是 MRC）。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Converting to linear values: 10 dB = 10 and 12 dB = 15.85. The average SNR of the received signal on each branch is γ̄ = 0.2 × 10 + 0.8 × 15.85 = 14.68, i.e. 11.67 dB.</p>
<p>Selection diversity selects the branch with the larger SNR. Since the branches are independent, the output SNR is 10 dB only when both branches are at 10 dB, with probability 0.2 × 0.2 = 0.04; otherwise it is 12 dB, with probability 0.96. (Average SNR at the SD output = 0.04 × 10 + 0.96 × 15.85 = 15.61, i.e. 11.94 dB.)</p>
<p>Average symbol error probability: P̄<sub>s</sub> = 0.04 × ½e<sup>−10</sup> + 0.96 × ½e<sup>−15.85</sup> = 9.08 × 10⁻⁷ + 6.28 × 10⁻⁸ ≈ 9.71 × 10⁻⁷. (Without diversity it would be about 4.59 × 10⁻⁶, so SD reduces the error probability by a factor of about 5.)</p></div>
<div class="ans">一句话：先换线性值，列出两路组合的概率（差情况只剩 0.2² = 0.04），每种情况分别算 ½e<sup>−γ</sup> 再加权：平均 SNR 11.67 dB，SD 误符号率 ≈ 9.71×10⁻⁷。</div>
'''},

'y2324s2-q1b2': {'title': '知识讲解 + 详细解析：空间复用、Alamouti 正交性与分集', 'zh': '''
<h4><span class="st">知识讲解</span>多根天线的两种用法：分集 vs 复用</h4>
<p>有 N 根发射天线、M 根接收天线（MIMO）时，可以有两种用法（讲义第 4 章 p.29–33）：</p>
<ul><li><b>分集（diversity）</b>：把<b>同一个</b>信息经过多条独立路径送过去，换取可靠性（误码率随 SNR 下降得更快）。最大分集增益 d<sub>max</sub> = N × M。</li>
<li><b>空间复用（spatial multiplexing）</b>：每根发射天线同时发<b>不同的</b>数据符号，速率变成 N 倍，但没有分集增益，衰落信道里误码性能可能较差。复用增益 r = lim R/log₂SNR，最大值 r<sub>max</sub> = min(N, M)。</li></ul>
<p>为什么空间复用要 <b>M ≥ N</b>？接收端每根天线得到一个方程（N 个符号的线性组合加噪声），要解出 N 个未知符号，至少需要 N 个方程，所以接收天线数不能少于数据流数。这也解释了 r<sub>max</sub> = min(N, M)：天线少的那一端决定能同时开几条"并行管道"。</p>
<h4><span class="st">知识讲解</span>正交空时分组码（OSTBC）和 Alamouti 码</h4>
<p>空时分组码把 K 个符号排成矩阵 X：一个维度是天线，一个维度是时隙。讲义第 5 章 p.27 的定义：X 是正交的，当且仅当 <b>X X<sup>H</sup> = (|s₁|² + … + |s<sub>K</sub>|²) I</b>。X<sup>H</sup> 是共轭转置（先转置，再每个元素取共轭）。正交的好处：接收端只用简单的线性合并就能把 s₁、s₂ 完全分开，两者互不干扰，而且每个符号都拿到全部路径的能量。2 根天线的正交码就是 Alamouti 码（第 5 章 p.21–26）。</p>
<h4><span class="st">详细解析</span>(ii) 空间复用</h4>
<p>原理：N 个不同数据流同时从 N 根天线发出，速率提高 N 倍；接收端需要 M ≥ N 根天线才能解出 N 个流。</p>
<div class="calc">N = 3，M = 5：r<sub>max</sub> = min(3, 5) = 3</div>
<p>（同一系统的最大分集增益是 3 × 5 = 15，两者不能同时取到最大，这就是分集-复用折中。）</p>
<h4><span class="st">详细解析</span>(iii) 逐项算 X X<sup>H</sup></h4>
<ol><li>写出 X 和 X<sup>H</sup>：X = (s₁, −s₂* ; s₂, s₁*)，X<sup>H</sup> = (s₁*, s₂* ; −s₂, s₁)。</li>
<li>(1,1) 元：s₁s₁* + (−s₂*)(−s₂) = |s₁|² + |s₂|²。</li>
<li>(2,2) 元：s₂s₂* + s₁*s₁ = |s₂|² + |s₁|²。</li>
<li>(1,2) 元：s₁s₂* + (−s₂*)(s₁) = s₁s₂* − s₁s₂* = 0；(2,1) 元是它的共轭，也是 0。</li></ol>
<div class="calc">X X<sup>H</sup> = (|s₁|² + |s₂|²) I　→　是正交 STBC</div>
<p>数字检验：取 s₁ = 1 + j，s₂ = 1 − j，|s₁|² + |s₂|² = 2 + 2 = 4，代入得 X X<sup>H</sup> = 4I，非对角元确实为 0。读矩阵：每一<b>行</b>是一根天线，每一<b>列</b>是一个时隙——时隙 1 两根天线发 s₁、s₂，时隙 2 发 −s₂*、s₁*。</p>
<h4><span class="st">详细解析</span>(iv) Alamouti 有没有分集增益</h4>
<p>有。以 2 发 1 收为例，信道增益 h₁、h₂ 独立：</p>
<div class="calc">y₁ = h₁s₁ + h₂s₂ + w₁；　y₂ = −h₁s₂* + h₂s₁* + w₂</div>
<div class="calc">h₁*y₁ + h₂y₂* = (|h₁|² + |h₂|²) s₁ + 噪声</div>
<p>s₂ 被完全抵消（这就是正交性的作用），s₁ 的增益是 |h₁|² + |h₂|²：只有两条路径<b>同时</b>深衰落时检测才会出错，所以分集阶数是 2；有 M 根接收天线时是 2M，即满分集 N × M。它不需要发射端知道信道。</p>
<p><span class="st">课外补充</span>（讲义只说 "MRC has array gain over OSTBC &amp; Alamouti code"，第 5 章 p.30）：总发射功率相同时，Alamouti 要把功率分给两根天线，所以和 1 发 2 收的 MRC 分集阶数相同，但 SNR 少约 3 dB。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>算 (1,2) 元时第二行要<b>取共轭</b>：(−s₂*)·(s₁*)* = −s₂*s₁。</li>
<li>题目矩阵是讲义写法的转置（讲义按行排时隙），结论一样，不用纠结。</li>
<li>原题把 "s₁ and s₂" 印成 "s₁ and s₁"，按 s₁、s₂ 理解。</li>
<li>2 发 M 收的分集阶数是 2M，不是 2。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(ii) In spatial multiplexing, N different data symbols are transmitted simultaneously from the N transmit antennas, so the data rate is N times higher, but there is no diversity gain. To separate and decode the N data streams, the receiver needs M ≥ N receive antennas. The maximum multiplexing gain is r<sub>max</sub> = min(N, M) = min(3, 5) = 3.</p>
<p>(iii) X X<sup>H</sup> = (s₁, −s₂* ; s₂, s₁*)(s₁*, s₂* ; −s₂, s₁). The diagonal elements are |s₁|² + |s₂|². The off-diagonal element is s₁s₂* − s₂*s₁ = 0 (and its conjugate is 0). Hence X X<sup>H</sup> = (|s₁|² + |s₂|²)I, so X is an orthogonal space-time block code (it is the Alamouti code).</p>
<p>(iv) Yes. Each symbol is transmitted from both antennas over two time slots and reaches the receiver through two independent fading paths. Because of the orthogonality, linear combining h₁*y₁ + h₂y₂* = (|h₁|² + |h₂|²)s₁ + noise removes s₂ completely. An error occurs only if both paths fade simultaneously, so the Alamouti code achieves full diversity of order 2 (2M with M receive antennas) without channel knowledge at the transmitter.</p></div>
<div class="ans">一句话：空间复用要 M ≥ N，最大复用增益 min(3, 5) = 3；X X<sup>H</sup> 对角元 |s₁|² + |s₂|²、非对角元 0，所以正交；Alamouti 合并后增益 |h₁|² + |h₂|²，有满分集 2M。</div>
'''},

'y2324s2-q2a': {'title': '知识讲解 + 详细解析：ISI 离散模型、线性滤波与残余 ISI 误码率', 'zh': '''
<h4><span class="st">知识讲解</span>ISI 的离散模型和 Z 变换</h4>
<p>符号间干扰（ISI）：多径让每个符号"拖尾巴"，后面的采样里混进前面的符号（讲义第 6 章 p.4–5、p.12）。离散模型 r[i] = Σ h[n] m[i − n + 1] + w[i] 就是一个线性滤波器：h[1] 乘当前符号，h[2] 乘前一个，h[3] 乘前两个。</p>
<ul><li><b>Z 变换</b>：Z⁻¹ 表示"晚一个符号"。H(Z) = h[1] + h[2]Z⁻¹ + h[3]Z⁻²，系数就是冲激响应的抽头值。</li>
<li><b>两个滤波器串联</b>：Z 变换相乘，C(Z)H(Z) 就是"信道 + 均衡器"的总响应。</li>
<li><b>白噪声经过滤波器</b>：各采样独立，所以输出噪声方差 = σ² × Σc<sub>k</sub>²（只经过 C(Z)，不经过 H(Z)）。</li>
<li><b>判决规则</b>：m 等概取 ±1，干扰和噪声都关于 0 对称，所以 f(y | +1) 和 f(y | −1) 关于 y = 0 镜像；ML 规则"选似然大的那个"就变成以 0 为门限取符号。</li></ul>
<h4><span class="st">详细解析</span>(i)(ii) 读出 ISI 和抽头</h4>
<ol><li>展开求和：r[i] = h[1]m[i] + h[2]m[i−1] + h[3]m[i−2] + w[i]。除了要的 m[i]，还有前两个符号 → ISI 存在（只要 h[2]、h[3] 不全为 0）。</li>
<li>H(Z) = 1 + 0.6Z⁻² 和 h[1] + h[2]Z⁻¹ + h[3]Z⁻² 逐项对比：<div class="calc">h[1] = 1，h[2] = 0，h[3] = 0.6</div>非零的只有 h[1] 和 h[3]。</li></ol>
<h4><span class="st">详细解析</span>(iii) 推判决规则</h4>
<ol><li>总响应（为什么：先看滤波后还剩多少 ISI）：<div class="calc">C(Z)H(Z) = (1 − 0.6Z⁻²)(1 + 0.6Z⁻²) = 1 − 0.36Z⁻⁴</div>平方差公式，Z⁻² 项抵消。</li>
<li>噪声只经过 C(Z)：w′[i] = w[i] − 0.6w[i−2]。</li>
<li>判决变量：<div class="calc">y[i] = m[i] − 0.36m[i−4] + w′[i]</div>ISI 从 0.6 降到 0.36，并被推到 4 个符号之外。</li>
<li>判决：y[i] ≥ 0 判 m̂[i] = +1，y[i] &lt; 0 判 −1。</li></ol>
<h4><span class="st">详细解析</span>(iv) 误码率</h4>
<ol><li>噪声方差：<div class="calc">σ′² = 0.3 × (1² + 0.6²) = 0.3 × 1.36 = 0.408，σ′ = √0.408 = 0.639</div></li>
<li>发 +1 时，m[i−4] 等概 ±1，残余干扰 −0.36m[i−4] 等概为 −0.36 或 +0.36，信号离门限 0 的距离是 1 − 0.36 = 0.64 或 1 + 0.36 = 1.36：<div class="calc">P<sub>b</sub> = ½Q(0.64/0.639) + ½Q(1.36/0.639) = ½Q(1.00) + ½Q(2.13)</div><div class="calc">= ½ × 0.1587 + ½ × 0.0166 ≈ 0.087</div></li>
<li>发 −1 时对称，结果相同，所以平均 P<sub>b</sub> ≈ 0.087。</li></ol>
<p><b>对比检查</b>：不加滤波器，直接用 r[i] = m[i] + 0.6m[i−2] + w[i] 判决，σ = √0.3 = 0.548，P<sub>b</sub> = ½Q(0.4/0.548) + ½Q(1.6/0.548) ≈ 0.117。滤波器把误码率从 0.117 降到 0.087，虽然噪声被放大了（0.3 → 0.408），但 ISI 降得更多。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>h[2] = 0（H(Z) 没有 Z⁻¹ 项），别写成 h[2] = 0.6。</li>
<li>噪声方差要乘 Σc² = 1.36；只有 σ′² 开方后才能放进 Q 函数。</li>
<li>Q 的自变量是"距离/标准差"，不是"距离/方差"。</li>
<li>残余 ISI 有两种取值，要各算一次再平均，不能只算一种。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) Expanding, r[i] = h[1]m[i] + h[2]m[i−1] + h[3]m[i−2] + w[i]. Besides the desired symbol m[i], the sample also contains the previous symbols m[i−1] and m[i−2]; this is inter-symbol interference (present whenever h[2] or h[3] is non-zero).</p>
<p>(ii) H(Z) = h[1] + h[2]Z⁻¹ + h[3]Z⁻². Comparing with 1 + 0.6Z⁻²: h[1] = 1 and h[3] = 0.6 (h[2] = 0).</p>
<p>(iii) The overall response is C(Z)H(Z) = (1 − 0.6Z⁻²)(1 + 0.6Z⁻²) = 1 − 0.36Z⁻⁴ and the filtered noise is w′[i] = w[i] − 0.6w[i−2]. So y[i] = m[i] − 0.36m[i−4] + w′[i]. Since m[i] = ±1 are equally likely and the interference and noise are symmetric about zero, the ML decision rule is: m̂[i] = 1 if y[i] ≥ 0, and m̂[i] = −1 if y[i] &lt; 0.</p>
<p>(iv) Noise variance σ′² = 0.3(1 + 0.36) = 0.408, σ′ = 0.639. Given m[i] = 1, the residual ISI is ±0.36 with equal probability, so P<sub>b</sub> = ½Q(0.64/0.639) + ½Q(1.36/0.639) = ½Q(1.00) + ½Q(2.13) = ½(0.1587) + ½(0.0166) ≈ 0.087. By symmetry the same holds for m[i] = −1, so the average bit error probability is about 0.087.</p></div>
<div class="ans">一句话：H(Z) 的系数就是抽头（h[1] = 1、h[3] = 0.6），C(Z)H(Z) = 1 − 0.36Z⁻⁴ 留下残余 ISI 0.36，噪声方差变 0.408，按 ±0.36 两种情况平均得 P<sub>b</sub> ≈ 0.087。</div>
'''},

'y2324s2-q2b': {'title': '知识讲解 + 详细解析：OFDM 子载波数、子信道增益与保护间隔', 'zh': '''
<h4><span class="st">知识讲解</span>OFDM 为什么能对付频率选择性衰落</h4>
<p>宽带信号的带宽大于相干带宽 B<sub>C</sub> 时，不同频率衰落不一样（频率选择性衰落），时域上表现为 ISI。OFDM（正交频分复用）的办法是把总带宽 B 切成 N 个窄的子载波（sub-carrier），每个子载波带宽 B/N 小于 B<sub>C</sub>，于是每个子载波只经历<b>平坦衰落</b>（讲义第 7 章 p.5–8）。</p>
<ul><li><b>子信道增益</b>（第 7 章 p.15）：H<sub>k</sub> = Σ<sub>i</sub> h<sub>i</sub> e<sup>−j2πik/N</sup>，就是信道冲激响应的 N 点 DFT。每个子载波只被乘上一个复数 H<sub>k</sub>，接收端除以 H<sub>k</sub> 就完成均衡。</li>
<li><b>符号时长</b>：原来的符号时长 T<sub>s</sub> = 1/B；一个 OFDM 块含 N 个符号，长 NT<sub>s</sub>，所以每个子载波上的符号变长 N 倍，ISI 的相对影响变小。</li>
<li><b>保护间隔</b>（guard interval，第 7 章 p.17–18）：每个块前面加长度 T<sub>G</sub> 的一段，要求 T<sub>G</sub> 大于最大时延扩展，让上一个块的拖尾落在这段里，接收端直接丢掉。代价是这段时间也要发功率，功率损失 = 10 log₁₀[(NT<sub>s</sub> + T<sub>G</sub>)/(NT<sub>s</sub>)]。</li></ul>
<h4><span class="st">详细解析</span>(i) 子载波数</h4>
<div class="calc">每个子载波带宽 = B<sub>C</sub>/2 = 500/2 = 250 kHz</div>
<div class="calc">N = 1 MHz / 250 kHz = 4</div>
<p>取 B<sub>C</sub> 的一半是为了留余量，保证每个子载波确实是平坦衰落。</p>
<h4><span class="st">详细解析</span>(ii) 四个子信道增益</h4>
<p>N = 4 时 e<sup>−j2πk/4</sup> 很好算，第三个抽头乘的是它的平方：</p>
<div class="tw"><table class="mini"><thead><tr><th>k</th><th>e<sup>−j2πk/4</sup></th><th>e<sup>−j2π·2k/4</sup></th><th>H<sub>k</sub> = 1 − 0.6(·) + 0.2(·)</th><th>|H<sub>k</sub>|</th></tr></thead><tbody>
<tr><td>1</td><td>−j</td><td>−1</td><td>1 + 0.6j − 0.2 = 0.8 + 0.6j</td><td>1</td></tr>
<tr><td>2</td><td>−1</td><td>1</td><td>1 + 0.6 + 0.2 = 1.8</td><td>1.8</td></tr>
<tr><td>3</td><td>j</td><td>−1</td><td>1 − 0.6j − 0.2 = 0.8 − 0.6j</td><td>1</td></tr>
<tr><td>4（= 0）</td><td>1</td><td>1</td><td>1 − 0.6 + 0.2 = 0.6</td><td>0.6</td></tr>
</tbody></table></div>
<p>自检：H₁ 和 H₃ 互为共轭（因为 h 是实数）；H₄ = H₀ = 抽头之和。|H| 从 0.6 到 1.8，说明这个信道确实是频率选择性的，但每个子载波内部只是一个常数增益。</p>
<h4><span class="st">详细解析</span>(iii)(iv) 块长和功率损失</h4>
<div class="calc">T<sub>s</sub> = 1/B = 1/(1 MHz) = 1 µs；　NT<sub>s</sub> = 4 µs（= 1/250 kHz）</div>
<div class="calc">T<sub>block</sub> = NT<sub>s</sub> + T<sub>G</sub> = 4 + 1 = 5 µs</div>
<div class="calc">功率损失 = 10 log₁₀(5/4) = 10 × 0.0969 ≈ 0.97 dB</div>
<p>直觉：5 µs 里只有 4 µs 有用，20% 的时间和能量花在保护间隔上，速率也只剩原来的 4/5。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>第三个抽头在 k = 1 时乘 (−j)² = −1，不是 −j。</li>
<li>功率损失的分子是总块长 5 µs，分母是有用部分 4 µs，比值 &gt; 1，dB 为正。</li>
<li>N 必须是整数；子载波带宽是相干带宽的一半，不是等于相干带宽。</li>
<li>补充一点（不影响本题作答）：抽头间隔 1 µs、共 3 个抽头，信道拖尾约 2 µs；按讲义 p.5"保护间隔要长于最大时延扩展"，严格说 1 µs 的保护间隔偏短。考试按题目给的 1 µs 计算即可。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) Bandwidth of each sub-carrier = B<sub>C</sub>/2 = 250 kHz, so N = 1 MHz / 250 kHz = 4.</p>
<p>(ii) The sub-channel gains are the N-point DFT of the channel impulse response, H<sub>k</sub> = Σ<sub>i</sub> h<sub>i</sub>e<sup>−j2πik/N</sup> with h = {1, −0.6, 0.2} and N = 4: H₁ = 1 − 0.6(−j) + 0.2(−1) = 0.8 + 0.6j; H₂ = 1 + 0.6 + 0.2 = 1.8; H₃ = 0.8 − 0.6j; H₄ (= H₀) = 1 − 0.6 + 0.2 = 0.6. Each sub-carrier therefore sees a flat channel with a single complex gain.</p>
<p>(iii) Original symbol duration T<sub>s</sub> = 1/B = 1 µs. The OFDM block duration is NT<sub>s</sub> = 4 µs, and with the 1 µs guard interval the total block duration is 4 + 1 = 5 µs.</p>
<p>(iv) Power loss = 10 log₁₀[(NT<sub>s</sub> + T<sub>G</sub>)/(NT<sub>s</sub>)] = 10 log₁₀(5/4) ≈ 0.97 dB.</p></div>
<div class="ans">一句话：子载波带宽 250 kHz → N = 4；H<sub>k</sub> 是 h 的 4 点 DFT = {0.8+0.6j, 1.8, 0.8−0.6j, 0.6}；块长 4 + 1 = 5 µs；功率损失 10 log₁₀(5/4) ≈ 0.97 dB。</div>
'''},

'y2324s2-q3a': {'title': '知识讲解 + 详细解析：Erlang B 反推小区半径、集群增益与扇区化', 'zh': '''
<h4><span class="st">知识讲解</span>话务量、Erlang B 和集群增益</h4>
<ul><li><b>话务量（traffic）</b>：A = λH，λ 是每小时呼叫次数，H 是平均通话时长（小时）。单位 Erlang（E），1 E = 一条信道一直被占满。每用户话务量 A<sub>u</sub> = 每小时呼叫数 × 通话时长 / 3600（讲义 Part A p.115–116）。</li>
<li><b>Erlang B</b>：blocked calls cleared（被阻塞的呼叫直接丢弃、不排队）时，M 条信道、话务量 A 下的阻塞概率 P<sub>B</sub>（p.118–120）。考试<b>查表</b>：已知 M 和 P<sub>B</sub>（GoS），读出能承载的 A。老师课上说附录虽给公式但从没见过真用它算，都是查表，要会线性插值。</li>
<li><b>集群（trunking）</b>：很多用户共用一组信道，因为不会所有人同时打电话。信道池越大，每条信道平均能多承担话务（集群效率高）。集群增益 T<sub>g</sub> = 一组信道在给定 GoS 下能服务的用户数 ÷ 信道数（p.122）。</li>
<li><b>扇区化（sectoring）</b>：用 120° 定向天线把一个小区分成 3 个扇区，同频干扰源从 6 个减到 2 个，SIR 提高；但每个扇区只有 1/3 的信道，各成独立的池，集群效率下降（p.143–149）。老师课上强调这一点要会讲。讲义 p.148–149 的例题正好也是"57 条信道、1%、120° 扇区每扇区 19 条、少了 24%"，和本题同一组数。</li></ul>
<h4><span class="st">详细解析</span>先写假设（题目要求 State and justify）</h4>
<ul><li>均匀固定信道分配（UFCA）：每个小区信道数相同；</li>
<li>399 条都是话务信道（题目已说 traffic channels），控制信道另算；</li>
<li>blocked calls cleared → 用 Erlang B；呼叫按泊松到达，用户数很多；</li>
<li>用户在服务区内均匀分布，按忙时（busy hour）话务设计；六边形小区。</li></ul>
<h4><span class="st">详细解析</span>(i)–(iv) 一步一步</h4>
<ol><li><b>每小区信道</b>：一个簇用完全部 399 条，<div class="calc">M = 399/7 = 57 条/小区</div></li>
<li><b>查 Erlang B 表</b>（M = 57，P<sub>B</sub> = 1%）：<div class="calc">A ≈ 44.2 E/小区</div></li>
<li><b>每用户话务量</b>（注意单位：秒 → 小时）：<div class="calc">A<sub>u</sub> = 0.9 × 90/3600 = 0.0225 E</div></li>
<li><b>每小区用户数</b>：令用户产生的话务量 = 小区能承载的话务量，<div class="calc">m = 44.2/0.0225 ≈ 1965 用户/小区；每小区话务量 = 1965 × 0.0225 ≈ 44.2 E</div></li>
<li><b>小区面积和半径</b>：<div class="calc">面积 = 1965/720 = 2.73 km²</div><div class="calc">R = √(2.73/2.598) = √1.051 ≈ 1.03 km</div>计算器：3√3/2 = 2.598。</li>
<li><b>集群增益</b>：<div class="calc">T<sub>g</sub> = 1965/57 ≈ 34.5 用户/信道</div>（对照讲义 p.122 例子：50 条、2% 时为 24.2。信道多了，T<sub>g</sub> 也大。）</li></ol>
<h4><span class="st">详细解析</span>(v) 120° 扇区化</h4>
<ol><li>每扇区 57/3 = 19 条，查表（M = 19，1%）：A ≈ 11.2 E/扇区，每小区 3 × 11.23 = 33.7 E。</li>
<li><div class="calc">m = 33.7/0.0225 ≈ 1497；面积 = 1497/720 = 2.08 km²；R = √(2.08/2.598) ≈ 0.89 km</div></li>
<li><div class="calc">T<sub>g</sub> = 1497/57 ≈ 26.3</div></li>
<li>对比：每小区能提供的话务量（表值 A）从 44.2 E 降到 33.7 E（少约 24%）；集群效率 A/M 从 0.78 降到 0.59；小区面积变小，覆盖同一个岛需要约 2.73/2.08 ≈ 1.31 倍的基站。</li></ol>
<p><b>运营商角度的评论</b>：在簇大小 N = 7 不变的前提下单纯加扇区，换来的是更好的 SIR（干扰源 6 → 2），付出的是集群效率、覆盖面积和更多的切换；只有利用 SIR 余量<b>缩小簇</b>（例如 N = 7 → 4），扇区化才能真正提高容量。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>A<sub>u</sub> 的单位：90 s 要除以 3600 变成小时。</li>
<li>扇区化后要按 19 条查表再乘 3，不能还按 57 条查。</li>
<li>面积用六边形公式 (3√3/2)R²，不是 πR²。</li>
<li>查表时确认是 Erlang B 表、1% 那一列。</li>
<li>用户数取整时向下取（1965），多一个人就超过 1% 阻塞。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Assumptions: uniform fixed channel assignment (equal channels per cell); all 399 channels are traffic channels; blocked calls are cleared, so the Erlang B model applies (Poisson arrivals, large user population); users are uniformly distributed and the design is for the busy hour.</p>
<p>(i) Channels per cluster = 399, so channels per cell = 399/7 = 57. From the Erlang B table with M = 57 and GOS = 1%, the offered traffic supported is A ≈ 44.2 Erlangs per cell.</p>
<p>(ii) Traffic per user A<sub>u</sub> = 0.9 × 90/3600 = 0.0225 E. Number of users per cell m = 44.2/0.0225 ≈ 1965, and the offered traffic generated by these users is 1965 × 0.0225 ≈ 44.2 E per cell.</p>
<p>(iii) Cell area = 1965/720 = 2.73 km² = (3√3/2)R², so R = √(2.73/2.598) ≈ 1.03 km.</p>
<p>(iv) Trunking gain T<sub>g</sub> = users served / number of channels = 1965/57 ≈ 34.5 users per channel.</p>
<p>(v) With 120° sectoring each sector has 57/3 = 19 channels. From the Erlang B table, A ≈ 11.2 E per sector, i.e. 33.7 E per cell. Users per cell = 33.7/0.0225 ≈ 1497, cell area = 1497/720 = 2.08 km², R ≈ 0.89 km, and T<sub>g</sub> = 1497/57 ≈ 26.3.</p>
<p>Observation: the traffic carried per cell falls by about 24% because the channels are split into three smaller trunk groups, so the trunking efficiency drops (0.78 to 0.59). The cell radius must be reduced from 1.03 km to 0.89 km, so about 31% more base stations are needed. From the operator's perspective, sectoring with the same cluster size only improves the SIR (interferers reduced from 6 to 2) at the cost of capacity, coverage and more handoffs; it increases capacity only if the improved SIR is used to reduce the cluster size.</p></div>
<div class="ans">一句话：57 条/小区 → 查表 44.2 E → 1965 人 → 2.73 km² → R ≈ 1.03 km，T<sub>g</sub> ≈ 34.5；扇区化把信道池切成 3 份，降到 33.7 E、R ≈ 0.89 km、T<sub>g</sub> ≈ 26.3，换来的只是 SIR。</div>
'''},

'y2324s2-q3b': {'title': '知识讲解 + 详细解析：FDMA / TDMA / CDMA 与代表系统', 'zh': '''
<h4><span class="st">知识讲解</span>多址（multiple access）是什么</h4>
<p>频谱有限，用户很多。多址技术就是规定"许多用户怎样同时共用一段频谱而不互相干扰"。办法是把某种资源切开分给用户：切<b>频率</b>、切<b>时间</b>，或者大家同时同频、靠<b>码</b>来区分（讲义 Part A p.7 的定义，p.15–26 介绍 1G–3G 系统）。</p>
<div class="tw"><table class="mini"><thead><tr><th>方式</th><th>切什么</th><th>每个用户得到</th><th>代表系统</th></tr></thead><tbody>
<tr><td>FDMA</td><td>频率</td><td>通话期间独占一个窄带频率信道</td><td>1G：AMPS（30 kHz 信道）</td></tr>
<tr><td>TDMA</td><td>时间</td><td>共用一个载波，只在自己的时隙发送</td><td>2G：GSM（200 kHz 载波、每帧 8 时隙）、IS-54/IS-136</td></tr>
<tr><td>CDMA</td><td>码</td><td>同时占用整段宽带频谱，有自己的扩频码</td><td>2G：IS-95；3G：WCDMA、cdma2000</td></tr>
</tbody></table></div>
<h4><span class="st">详细解析</span>答题要点（每种方式写"怎么分 + 举例"）</h4>
<ol><li><b>FDMA</b>（频分多址）：把频带分成等宽的信道，每个通话占一个频率。为什么重要：最早、最简单，模拟系统只能这样做；缺点是需要保护频带、每个信道要一套收发设备。</li>
<li><b>TDMA</b>（时分多址）：一个载波按时间切成周期性的时隙，几个用户轮流发送。为什么重要：数字化以后才能做，一个载波可以给多个用户，提高效率；需要严格同步。GSM 实际是 FDMA/TDMA 混合（先分多个 200 kHz 载波，每个再分 8 个时隙），写上这一句更完整。</li>
<li><b>CDMA</b>（码分多址）：给每个用户分配一个（近似）正交的码，所有用户同时、同频发送，接收端用对应的码解扩，别人的信号表现为低电平噪声。为什么重要：频率复用系数可以为 1，抗多径能力强（讲义 p.28 说 CDMA 需要的基站更少、抗多径更好）。</li></ol>
<p><span class="st">课外补充</span>4G/5G 用的是 OFDMA（第 7 章 OFDM 的多址版本），本题只问 1G–3G，可以不写。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>每种方式都要<b>举一个真实系统</b>，只描述不举例会丢分。</li>
<li>别把 GSM 写成 CDMA，也别把 IS-95 写成 TDMA。</li>
<li>5 分题写清"怎么分 + 例子"即可，不用写两页。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p><b>FDMA (Frequency Division Multiple Access):</b> the available spectrum is divided into frequency channels of equal bandwidth, and each user is assigned its own channel for the whole duration of the call, so different users transmit on different frequencies. Example: the 1G analogue system AMPS (30 kHz channels).</p>
<p><b>TDMA (Time Division Multiple Access):</b> one carrier frequency is divided cyclically into time slots of equal duration, and several users share the carrier by transmitting only in their own time slot. Example: the 2G system GSM (200 kHz carriers with 8 time slots per frame, i.e. combined FDMA/TDMA); IS-54/IS-136 in North America.</p>
<p><b>CDMA (Code Division Multiple Access):</b> all users transmit at the same time over the same wideband spectrum; each user is assigned a different (nearly orthogonal) spreading code, and the receiver separates its own signal by correlating with that code, while other users appear as low-level noise. Examples: the 2G system IS-95 and the 3G systems WCDMA and cdma2000.</p></div>
<div class="ans">一句话：FDMA 分频率（AMPS），TDMA 分时隙（GSM、IS-136），CDMA 同时同频靠码区分（IS-95、WCDMA）。</div>
'''},

'y2324s2-q4ab': {'title': '知识讲解 + 详细解析：简化 IoT 架构两个栈与雾计算', 'zh': '''
<h4><span class="st">知识讲解</span>简化 IoT 架构：一对三层的并行栈</h4>
<p>IoT 系统里有成千上万个传感器，数据要从"物"一路送到应用。为了看清楚，讲义（Part B p.86–91）用 Cisco 的<b>简化 IoT 架构</b>：两个并行的三层栈。老师课上说学这一部分用这个简化框架，比另外两个标准好理解。</p>
<div class="tw"><table class="mini"><thead><tr><th>Core IoT Functional Stack（核心功能栈）</th><th>IoT Data Management and Compute Stack（数据管理与计算栈）</th></tr></thead><tbody>
<tr><td>Layer 3：应用与分析层（Applications and analytics）</td><td>云（cloud，数据中心）</td></tr>
<tr><td>Layer 2：通信网络层（Communications network），四个子层</td><td>雾（fog，网关 / 路由器等网络设备）</td></tr>
<tr><td>Layer 1："Things" 层（传感器、执行器）</td><td>边缘（edge / mist，设备本身）</td></tr>
</tbody></table></div>
<p>左边回答"数据怎么<b>传</b>"，右边回答"数据在哪里<b>算</b>"，两者一层对一层。</p>
<h4><span class="st">详细解析</span>(a) 两个栈的组成（7 分，每个部件写"是什么 + 作用"）</h4>
<ol><li><b>Things 层</b>：传感器、执行器等智能物体。设计时要适应部署环境的约束（电池或市电、静止或移动、上报频率、数据量、覆盖距离、密度），同时还能提供需要的数据（p.89–91）。</li>
<li><b>通信网络层</b>：物体不能自给自足时，要和外部系统通信，分四个子层：接入网子层（最后一公里，802.11ah、802.15.4g、LoRa）、网关与回传子层（把一片区域的物体汇聚到网关，再用长距离介质送回中心站）、网络传输子层（IP、UDP/TCP）、IoT 网络管理子层（HTTP、WebSocket 等应用协议）。</li>
<li><b>应用与分析层</b>：处理收集到的数据，做智能决策，并反过来控制"物"或其他系统改变行为或参数。</li>
<li><b>数据管理与计算栈</b>：边缘（mist）在传感器 / 设备里做最基本的过滤和判断；雾在离终端最近的网络设备上做实时处理；云做集中存储、历史数据和大规模分析。三者互补，不是替代（p.110–111）。</li></ol>
<h4><span class="st">详细解析</span>(b) 为什么要引入雾计算（6 分：先问题，再好处）</h4>
<p>如果所有数据都送到云端集中处理（优点只是简单），讲义 p.103–105 列出的问题：</p>
<ul><li>最后一公里的 IoT 网络带宽很有限，海量数据送不上去；</li>
<li>时延大，失去实时响应能力；</li>
<li>网关的回传常靠 3G/LTE 甚至卫星，不可靠；</li>
<li>回传上的数据量太大，大数据越来越难做实时分析。</li></ul>
<p>雾计算（p.106–109）把数据处理分散到尽量靠近 IP 网络边缘的地方，任何有计算、存储和联网能力的设备都可以做雾节点。好处：就近分析<b>降低时延</b>；为核心网<b>卸载</b>大量流量；<b>敏感数据留在本地网络</b>；雾节点地理上靠近传感器，有<b>上下文感知</b>，能形成分布式的边缘控制回路，实时监测和控制设备而不必等云端；上传前先做<b>数据精简</b>（预处理后上层只需批处理一部分数据）。老师课上概括为：分布式处理、不用等中心服务器所以快、上传前先精简、能实时处理、雾节点和终端之间用无线连接。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>两个栈各三层，别把"通信网络层的四个子层"当成第四、五层。</li>
<li>边缘在设备上，雾在网关 / 路由器上，云在数据中心，距离终端越来越远。</li>
<li>(b) 只写好处不写问题会显得没回答"necessity"；先写问题再写雾怎么解决。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(a) The simplified IoT architecture consists of two parallel three-layer stacks.</p>
<p><b>Core IoT Functional Stack.</b> (1) "Things" layer: sensors, actuators and other smart objects; they must fit the constraints of the deployment environment (power source, mobility, reporting frequency, data volume, range, density) while still providing the required information. (2) Communications network layer, divided into four sublayers: the access network sublayer (the last mile, typically wireless such as IEEE 802.11ah, 802.15.4g and LoRa); the gateways and backhaul sublayer (smart objects in an area are organised around a common gateway, which forwards the data over a longer-range medium to a headend station); the network transport sublayer (open, standard network and transport protocols such as IP, UDP and TCP); and the IoT network management sublayer (application protocols such as HTTP and WebSocket that let headend applications exchange data with the sensors). (3) Application and analytics layer: applications process the collected data, make intelligent decisions and, in turn, instruct the things or other systems to adapt their behaviour or parameters.</p>
<p><b>Data Management and Compute Stack.</b> It defines where the data is processed: at the edge (mist) inside the sensors and devices themselves for basic filtering and simple decisions; in the fog, on network devices such as gateways and routers close to the endpoints, for real-time processing; and in the cloud (data centre) for centralised storage, historical data and large-scale analytics. These layers complement each other.</p>
<p>(b) If all data were sent to the cloud for centralised processing: the available bandwidth in last-mile IoT networks is very limited; the latency is high, so real-time response is lost; the backhaul from the gateway is often unreliable (3G/LTE or satellite); and the volume of data is too large to transport and to analyse in real time. Fog computing solves these problems by distributing data management as close to the edge of the IP network as possible. Analysing data near where it is collected minimises latency, offloads large amounts of traffic from the core network and keeps sensitive data inside the local network. Because a fog node is geographically close to the sensors it has contextual awareness and can react to events quickly, providing a distributed edge control loop in real time without waiting for the cloud. It also reduces the data (pre-processing) before sending it upstream, so the cloud only needs to handle a subset of the data.</p></div>
<div class="ans">一句话：核心功能栈 = Things / 通信网络（接入、网关回传、传输、管理四子层）/ 应用分析，计算栈 = 边缘 / 雾 / 云；雾计算是为了解决带宽、时延、回传不可靠和数据量过大四个问题。</div>
'''},

'y2324s2-q4c': {'title': '知识讲解 + 详细解析：SIR 公式推导、反求 n、最坏情况与扇区', 'zh': '''
<h4><span class="st">知识讲解</span>同频干扰和 Q = D/R</h4>
<p>蜂窝系统里，簇大小为 N 的每个簇用完全部信道，相隔一定距离 D 的小区重复使用同一组频率（同频小区）。D 越大干扰越小。六边形几何给出 <b>Q = D/R = √(3N)</b>（讲义 Part A p.78），Q 叫同频复用比（co-channel reuse ratio）。</p>
<p>讲义 p.88 的简化分析假设：只算第一层 6 个同频干扰；手机在小区边缘，到本基站距离 R；6 个干扰基站到手机都近似为 D；接收功率与距离的 −n 次方成正比（n 是路径损耗指数）。</p>
<div class="calc">S/I = R<sup>−n</sup> / (6D<sup>−n</sup>) = (D/R)<sup>n</sup>/6 = Q<sup>n</sup>/6</div>
<div class="tw"><table class="mini"><thead><tr><th>情况</th><th>公式</th><th>N = 7、n = 4（讲义）</th></tr></thead><tbody>
<tr><td>简化（6 个都在 D）</td><td>Q<sup>n</sup>/6</td><td>18.66 dB（p.89）</td></tr>
<tr><td>最坏全向（2 个 D−R、2 个 D、2 个 D+R）</td><td>1/[2(Q−1)<sup>−n</sup> + 2Q<sup>−n</sup> + 2(Q+1)<sup>−n</sup>]</td><td>17.27 dB（p.91）</td></tr>
<tr><td>120° 扇区（只剩 2 个）</td><td>1/[Q<sup>−n</sup> + (Q+0.7)<sup>−n</sup>]</td><td>p.145</td></tr>
</tbody></table></div>
<h4><span class="st">详细解析</span>推导 SIR<sub>dB</sub> = 1.76 + 20 log₁₀N</h4>
<ol><li>从 S/I = Q<sup>n</sup>/6 出发，代入 Q = √(3N)、n = 4：Q⁴ = (3N)²。</li>
<li><div class="calc">S/I = (3N)²/6 = 9N²/6 = 1.5N²</div></li>
<li>取 10 log₁₀：<div class="calc">SIR<sub>dB</sub> = 10 log₁₀1.5 + 10 log₁₀N² = 1.76 + 20 log₁₀N</div></li></ol>
<h4><span class="st">详细解析</span>(i) N = 7</h4>
<div class="calc">SIR<sub>dB</sub> = 1.76 + 20 log₁₀7 = 1.76 + 16.90 = 18.66 dB</div>
<p>评论：比语音质量需要的约 18 dB 稍高（讲义 p.89 说 N = 7 是最优簇大小），所以 7 小区复用最常用。但这个模型把 6 个干扰都放在 D，忽略了手机靠近某些干扰小区的情况，偏乐观；n = 4 也是假设。</p>
<h4><span class="st">详细解析</span>(ii) 反求 n</h4>
<p>题目写的 "SNR" 这里指 SIR。20 dB → 线性 100：</p>
<div class="calc">Q<sup>n</sup>/6 ≥ 100 → Q<sup>n</sup> ≥ 600，Q = √21 = 4.583</div>
<div class="calc">n = log₁₀600 / log₁₀4.583 = 2.778/0.661 ≈ 4.20</div>
<p>为什么用对数：未知数在指数上，两边取 log 把它拿下来。</p>
<h4><span class="st">详细解析</span>(iii) 最坏情况（n = 4.2）</h4>
<div class="calc">(Q − 1)<sup>4.2</sup> = 3.583<sup>4.2</sup> = 212.6；Q<sup>4.2</sup> = 597.9；(Q + 1)<sup>4.2</sup> = 5.583<sup>4.2</sup> = 1370</div>
<div class="calc">SIR = 1/(2/212.6 + 2/597.9 + 2/1370) = 1/0.0142 ≈ 70.4 → 18.5 dB</div>
<p>计算器：a<sup>4.2</sup> 用 x<sup>y</sup> 键，或 10^(4.2 × log₁₀a)。结果低于 20 dB：手机在小区边上时有两个干扰基站只隔 D − R，最近的两项贡献了一大半干扰。</p>
<h4><span class="st">详细解析</span>(iv) 120° 扇区（n = 4.2）</h4>
<div class="calc">(Q + 0.7)<sup>4.2</sup> = 5.283<sup>4.2</sup> = 1086</div>
<div class="calc">SIR = 1/(1/597.9 + 1/1086) ≈ 385.7 → 25.9 dB</div>
<p>评论：比 (iii) 高约 7.4 dB，满足 20 dB 还剩约 6 dB 余量。原因是定向天线只"看见"2 个同频干扰。代价：每扇区信道只有 1/3，集群效率下降，切换增多；多出的 SIR 余量可以用来缩小簇、提高容量。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>20 dB 是线性 100，不是 20。</li>
<li>最坏情况的距离以 R 为单位：Q − 1、Q、Q + 1，各 2 个。</li>
<li>扇区情况只剩 2 项，别还写 6 项。</li>
<li>推导里 10 log₁₀N² = 20 log₁₀N，这一步要写出来。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Derivation: assume only the six first-tier co-channel interferers, the mobile at the cell edge (distance R from its own base station) and all interferers at distance D. With received power proportional to d<sup>−n</sup>, S/I = R<sup>−n</sup>/(6D<sup>−n</sup>) = Q<sup>n</sup>/6, where Q = D/R = √(3N<sub>c</sub>). With n = 4, S/I = (3N<sub>c</sub>)²/6 = 1.5N<sub>c</sub>², so SIR<sub>dB</sub> = 10 log₁₀1.5 + 20 log₁₀N<sub>c</sub> = 1.76 + 20 log₁₀N<sub>c</sub>.</p>
<p>(i) For N<sub>c</sub> = 7: SIR<sub>dB</sub> = 1.76 + 20 log₁₀7 = 18.66 dB. This just exceeds the 18 dB needed for good voice quality, which is why N<sub>c</sub> = 7 is widely used; however, the simplified model is optimistic because it places all six interferers at distance D.</p>
<p>(ii) For SIR ≥ 20 dB = 100: Q<sup>n</sup>/6 ≥ 100 with Q = √21 = 4.583, so n = log₁₀600 / log₁₀4.583 ≈ 4.2.</p>
<p>(iii) With n = 4.2: SIR = 1/[2(3.583)<sup>−4.2</sup> + 2(4.583)<sup>−4.2</sup> + 2(5.583)<sup>−4.2</sup>] = 1/0.0142 ≈ 70.4, i.e. 18.5 dB, which is below the 20 dB requirement.</p>
<p>(iv) With 120° sectoring only two interferers remain: SIR = 1/[Q<sup>−n</sup> + (Q + 0.7)<sup>−n</sup>] = 1/[(4.583)<sup>−4.2</sup> + (5.283)<sup>−4.2</sup>] ≈ 386, i.e. 25.9 dB. This is about 7.4 dB better than the worst-case omnidirectional result and meets the 20 dB requirement with margin, because the directional antennas reduce the number of interferers from six to two. The cost is fewer channels per sector, lower trunking efficiency and more handoffs.</p></div>
<div class="ans">一句话：S/I = Q<sup>n</sup>/6、Q² = 3N、n = 4 → 1.5N² → 1.76 + 20 log N；N = 7 得 18.66 dB；要 20 dB 需 n ≈ 4.2；最坏全向 18.5 dB，120° 扇区 25.9 dB。</div>
'''},

# ====================================================================== 2024-25 S2
'y2425s2-q1a': {'title': '知识讲解 + 详细解析：路径损耗图读数、LCR/AFD 与注水分配', 'zh': '''
<h4><span class="st">知识讲解</span>三个工具</h4>
<ul><li><b>路径损耗图</b>（讲义第 2 章 p.8–10）：dB 形式 10 log₁₀(P<sub>r</sub>/P<sub>t</sub>) = K<sub>dB</sub> − 10γ log₁₀d。以 log₁₀d 为横轴是一条直线：d = 1 处纵坐标是 K<sub>dB</sub>，斜率是 −10γ（每十倍距离多损耗 10γ dB）。本题 γ = 3.5，斜率 35 dB/十倍距离。</li>
<li><b>电平通过率（LCR，level crossing rate）</b>：每秒信号包络<b>向下</b>穿过某个门限的平均次数，即每秒"深衰落"开始几次（p.40）。<b>平均衰落时长（AFD，average fade duration）</b>：每次掉到门限以下平均持续多久（p.42）。两者相乘 = 处于深衰落的时间比例。老师课上说 LCR、AFD 公式考试会给，但要会解释。</li>
<li><b>注水（water-filling）</b>（p.52–57）：频率选择性信道分成几个子带，总功率 P 固定，按 P<sub>i</sub>/P = 1/γ₀ − 1/γ<sub>i</sub> 分配，γ<sub>i</sub> &lt; γ₀ 的子带不分。名字的来历：把 1/γ<sub>i</sub> 看成"池底高度"，倒进总量为 1 的水，水面高度是 1/γ₀，每个子带分到的功率就是水深。好子带池底低、水深，分得多。老师课上说这个式子是<b>框起来要背</b>的，今年 Quiz 第 3 题就考了注水。</li></ul>
<h4><span class="st">详细解析</span>(i) 读 A 和 B</h4>
<ol><li>图中直线向右下降，说明纵轴是 10 log₁₀(P<sub>r</sub>/P<sub>t</sub>)（距离越远越小）。</li>
<li>A 在 log₁₀d = 0（d = 1 m）处，纵坐标 = K<sub>dB</sub>：<div class="calc">A = −30 dB</div></li>
<li>从 A 降到横轴共 88 dB，每个十倍距离降 35 dB：<div class="calc">35 × B = 88 → B = 88/35 = 2.51（d = 10<sup>2.51</sup> ≈ 327 m）</div></li></ol>
<h4><span class="st">详细解析</span>(ii) 符号时长和每秒误符号数</h4>
<ol><li>一次平均衰落正好盖住 3 个符号：<div class="calc">T<sub>s</sub> = 6 µs / 3 = 2 µs</div></li>
<li>每次衰落里有几个错符号：衰落长 3T<sub>s</sub>。如果和符号边界对齐，3 个符号全在里面；不对齐时是 2 个完整符号加头尾两段，两段合起来正好一个符号长，其中必有一段超过一半。所以每次约 3 个错符号。</li>
<li>LCR = 5 次/秒：<div class="calc">误符号数 = 5 × 3 = 15 个/秒</div></li></ol>
<p><b>检查</b>：符号率 1/2 µs = 5×10⁵ 个/秒，误符号比例 15/(5×10⁵) = 3×10⁻⁵，正好等于 LCR × AFD = 5 × 6×10⁻⁶ = 3×10⁻⁵（处于深衰落的时间比例）。两条思路一致。</p>
<h4><span class="st">详细解析</span>(iii) 注水分配</h4>
<ol><li><b>dB 换线性</b>：18 dB → 63.1；10 dB → 10；3 dB → 2.0。</li>
<li><b>先假设三个子带都分到功率</b>，把三个式子相加，ΣP<sub>i</sub> = P：<div class="calc">3/γ₀ − (1/63.1 + 1/10 + 1/2.0) = 1</div><div class="calc">1/γ₀ = (1 + 0.0158 + 0.100 + 0.501)/3 = 1.617/3 = 0.539</div>γ₀ = 1/0.539 = 1.855（2.7 dB）。</li>
<li><b>检查假设</b>：三个 γ<sub>i</sub>（63.1、10、2.0）都 ≥ 1.855，成立。如果某个 γ<sub>i</sub> &lt; γ₀，就把它去掉、用剩下的子带重算。</li>
<li><b>分配</b>：<div class="calc">P₁ = 0.539 − 0.016 = 0.523 W；P₂ = 0.539 − 0.100 = 0.439 W；P₃ = 0.539 − 0.501 = 0.038 W</div>和为 1 W ✓。</li></ol>
<h4><span class="st">易错</span>注意</h4>
<ul><li>B 是 log₁₀d 的值（2.51），不是 d 本身。</li>
<li>斜率是 10γ = 35 dB/十倍距离，不是 3.5。</li>
<li>注水公式里 SNR 必须先换线性；求完 γ₀ 一定要回头检查每个 γ<sub>i</sub> ≥ γ₀。</li>
<li>P = 1 W，所以 P<sub>i</sub> = 1/γ₀ − 1/γ<sub>i</sub> 直接就是瓦数；P 不是 1 时要乘 P。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) In dB form, 10 log₁₀(P<sub>r</sub>/P<sub>t</sub>) = K<sub>dB</sub> − 35 log₁₀d, a straight line against log₁₀d with slope −35 dB per decade. At d = 1 m, log₁₀d = 0, so A = K<sub>dB</sub> = −30 dB. The line falls by 88 dB from A to the horizontal axis, so 35B = 88 and B = log₁₀d = 2.51 (d ≈ 327 m).</p>
<p>(ii) The average fade duration covers three symbols, so T<sub>s</sub> = 6 µs/3 = 2 µs. In each fade, three symbols (or, if not aligned, two full symbols plus a part of another lying more than half in the fade) are in error, so about 3 symbol errors occur per fade. With a level crossing rate of 5 fades per second, the average number of symbol errors is 5 × 3 = 15 per second.</p>
<p>(iii) The SNRs in linear values are γ₁ = 63.1, γ₂ = 10 and γ₃ = 2.0. Assuming all three sub-bands are allocated power, ΣP<sub>i</sub> = P gives 3/γ₀ − (1/63.1 + 1/10 + 1/2.0) = 1, so 1/γ₀ = 0.539 and γ₀ = 1.855. All γ<sub>i</sub> ≥ γ₀, so the assumption holds. P₁ = 0.539 − 0.016 = 0.523 W, P₂ = 0.539 − 0.100 = 0.439 W, P₃ = 0.539 − 0.501 = 0.038 W (total 1 W).</p></div>
<div class="ans">一句话：A = K<sub>dB</sub> = −30 dB，B = 88/35 = 2.51；T<sub>s</sub> = 2 µs，每秒 5 次衰落 × 3 个 = 15 个误符号；注水先求 1/γ₀ = 0.539，再分 0.523 / 0.439 / 0.038 W。</div>
'''},

'y2425s2-q1b1': {'title': '知识讲解 + 详细解析：选择分集中断概率反求支路数', 'zh': '''
<h4><span class="st">知识讲解</span>选择分集的中断概率</h4>
<p>中断（outage）：瞬时 SNR 低于能满足误码要求的最低值 γ<sub>b</sub>。瑞利衰落下单条支路的 SNR 服从指数分布，掉到 γ<sub>b</sub> 以下的概率是 1 − e<sup>−γ<sub>b</sub>/γ̄</sup>（γ̄ 是平均 SNR，老师说这个要背）。选择分集只有在 <b>M 条支路全部</b>低于门限时才中断，支路独立，概率相乘（讲义第 4 章 p.11–13）：</p>
<div class="calc">P<sub>out</sub> = (1 − e<sup>−γ<sub>b</sub>/γ̄</sup>)<sup>M</sup></div>
<p>本题公式里的 30 就是 γ̄（每支路平均 SNR，线性值，约 14.8 dB），γ<sub>b</sub> 要从误码率要求反推出来。BPSK 的 P<sub>b</sub> = Q(√(2γ<sub>b</sub>)) 老师说考试会给，但要会<b>倒查 Q 表</b>。</p>
<p>为什么单支路中断是 1 − e<sup>−γ<sub>b</sub>/γ̄</sup>：瑞利衰落下 SNR 的概率密度是 p(γ) = (1/γ̄)e<sup>−γ/γ̄</sup>，从 0 积到 γ<sub>b</sub> 就得到这个式子（考试不考积分，直接用结果）。它只取决于比值 γ<sub>b</sub>/γ̄：本题门限只有平均值的 15%（4.5/30），所以一条支路掉到门限下面的概率是 13.9%。整题的思路是一条链：<b>误码率要求 → 最低 SNR γ<sub>b</sub> → 单支路中断 → M 条支路全中断</b>，每一环都是一个公式，按顺序代就行。</p>
<h4><span class="st">详细解析</span>四步</h4>
<ol><li><b>由误码率求 γ<sub>b</sub></b>：在 Q 表里找 1.35×10⁻³，对应 x = 3.00，所以 √(2γ<sub>b</sub>) = 3.0：<div class="calc">γ<sub>b</sub> = 3.0²/2 = 4.5（6.53 dB）</div></li>
<li><b>单支路中断概率</b>：<div class="calc">1 − e<sup>−4.5/30</sup> = 1 − e<sup>−0.15</sup> = 1 − 0.861 = 0.139</div></li>
<li><b>解 M</b>（未知数在指数上 → 取对数）：<div class="calc">0.139<sup>M</sup> = 0.02 → M = ln 0.02 / ln 0.139 = (−3.91)/(−1.97) ≈ 1.98</div></li>
<li><b>取整并代回验证</b>：M 必须是整数，取 M = 2：<div class="calc">P<sub>out</sub> = 0.139² = 0.0194 ≈ 0.02 ✓</div></li></ol>
<div class="tw"><table class="mini"><thead><tr><th>M</th><th>1</th><th>2</th><th>3</th></tr></thead><tbody>
<tr><td>P<sub>out</sub> = 0.139<sup>M</sup></td><td>0.139</td><td>0.0194</td><td>0.0027</td></tr>
</tbody></table></div>
<p>表里只有 M = 2 接近 0.02。每加一条支路，中断概率约乘 0.139，这就是分集"指数式"降低中断的意思。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>γ<sub>b</sub> = 4.5 是线性值；30 也是线性值，不要再换 dB。</li>
<li>两个 ln 都是负数，比值为正；用 log₁₀ 算也一样（log₁₀0.02 / log₁₀0.139）。</li>
<li>M 一定要取整，并代回验证；本题 1.98 很接近 2，题目说 "approximately 0.02"。</li>
<li>Q 表倒查：在表的正文里找 1.35×10⁻³，不是在表头找。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>From the Q-function table, Q(3.0) = 1.35 × 10⁻³, so √(2γ<sub>b</sub>) = 3.0 and the minimum SNR is γ<sub>b</sub> = 9/2 = 4.5. Each branch has average SNR 30, so the outage probability of one branch is 1 − e<sup>−4.5/30</sup> = 1 − e<sup>−0.15</sup> = 0.139. For selection diversity, an outage occurs only when all M independent branches are in outage: P<sub>out</sub> = 0.139<sup>M</sup> = 0.02, so M = ln 0.02 / ln 0.139 ≈ 1.98. Since M must be an integer, M = 2 branches (check: 0.139² = 0.0194 ≈ 0.02).</p></div>
<div class="ans">一句话：倒查 Q 表得 γ<sub>b</sub> = 4.5 → 单支路中断 0.139 → 0.139<sup>M</sup> = 0.02 → M ≈ 1.98，取 M = 2 并验证 0.0194。</div>
'''},

'y2425s2-q1b2': {'title': '知识讲解 + 详细解析：分集-复用折中与无信息发射机 MIMO 容量', 'zh': '''
<h4><span class="st">知识讲解</span>分集增益 d、复用增益 r 和它们的折中</h4>
<p>讲义第 4 章 p.31–33 用两个"斜率"描述 MIMO：</p>
<ul><li><b>分集增益 d</b>：高 SNR 时 P<sub>e</sub> ≈ SNR<sup>−d</sup>，即 SNR 每涨 10 倍，误码率降 10<sup>d</sup> 倍。最大 d<sub>max</sub> = N × M（N 发 M 收，所有路径都独立时）。</li>
<li><b>复用增益 r</b>：高 SNR 时速率 R ≈ r log₂SNR，即 SNR 每翻倍，速率多 r bit/s/Hz。最大 r<sub>max</sub> = min(N, M)。</li>
<li><b>折中（trade-off）</b>：两者不能同时取最大。最优折中曲线把点 (r, (N − r)(M − r))（r = 0, 1, …, min(N, M)）连成折线。老师课上点名：<b>d 和阵列增益的公式简单，要记住</b>。</li></ul>
<h4><span class="st">知识讲解</span>无信息发射机（uninformed transmitter）的 MIMO 容量</h4>
<p>"无信息"指发射端不知道信道 H。它没法把功率往好的方向集中，只能把总功率 P 平均分给 N 根天线：功率矩阵 P = (P/N)I（讲义第 5 章 p.37）。代入一般式，HPH<sup>H</sup> = (P/N)HH<sup>H</sup>：</p>
<div class="calc">C = B log₂ det{I + (P/(Nσ²)) HH<sup>H</sup>}</div>
<p>N = M = 1 时 H 就是一个数 h，det 就是这个数本身，退化成熟悉的香农公式 C = B log₂(1 + P|h|²/σ²)。</p>
<h4><span class="st">详细解析</span>(ii) 最大分集增益和速率</h4>
<ol><li><div class="calc">d<sub>max</sub> = N × M = 5 × 3 = 15</div></li>
<li>由误码率和 d 求 SNR（为什么：速率公式需要 SNR）：<div class="calc">10⁻³ = SNR⁻³ → SNR = (10⁻³)<sup>−1/3</sup> = 10（10 dB）</div></li>
<li>求速率：<div class="calc">R = r log₂SNR = 2 × log₂10 = 2 × 3.32 ≈ 6.64 bit/s/Hz</div>计算器：log₂10 = 1/0.301 = 3.32。</li>
<li>自检：(r, d) = (2, 3) 在最优曲线上吗？d(2) = (5 − 2)(3 − 2) = 3 ✓；r = 2 也不超过 r<sub>max</sub> = 3。</li></ol>
<p>物理含义：r = 2 相当于同时开 2 条并行数据流（速率随 log₂SNR 以 2 倍增长）；剩下的天线自由度换来 d = 3，误码率按 SNR⁻³ 下降。用满 15 的分集就只能 r = 0，用满 r = 3 的复用就 d = 0，这就是"折中"。解题顺序为什么是"先 d 求 SNR，再 r 求 R"：两个公式共用同一个 SNR，误码率要求把 SNR 定下来，速率随之确定。</p>
<h4><span class="st">详细解析</span>(iii) 化简并代数</h4>
<ol><li>化简：P = (P/N)I 代入，得 C = B log₂ det{I + (P/(Nσ²)) HH<sup>H</sup>}。</li>
<li>N = M = 1，P = 1，σ² = 0.25，h = 2（幅度增益），|h|² = 4：<div class="calc">C/B = log₂(1 + 1 × 4/0.25) = log₂(1 + 16) = log₂17</div><div class="calc">log₂17 = log₁₀17/0.301 = 1.230/0.301 ≈ 4.09 bit/s/Hz</div></li></ol>
<p>如果把 "channel gain is 2" 理解成功率增益 |h|² = 2，结果是 log₂9 ≈ 3.17。建议在答卷上写一句 "taking the channel gain as the amplitude gain h = 2, |h|² = 4"，把假设说清楚。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>d<sub>max</sub> 是乘积 15，r<sub>max</sub> 才是 min(N, M) = 3，别弄反。</li>
<li>P<sub>e</sub> = SNR<sup>−d</sup> 里的 SNR 是线性值；开 d 次方根。</li>
<li>容量公式里要的是 |h|²，不是 h。</li>
<li>"per Hz" 就是 C/B，单位 bit/s/Hz。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(ii) The maximum diversity gain is d<sub>max</sub> = N × M = 5 × 3 = 15. With diversity gain d = 3, P<sub>e</sub> ≈ SNR<sup>−d</sup> gives 10⁻³ = SNR⁻³, so SNR = 10. With multiplexing gain r = 2, the maximum rate is R = r log₂SNR = 2 log₂10 ≈ 6.64 bit/s/Hz. (Check: (r, d) = (2, 3) lies on the optimal trade-off curve, d(2) = (5 − 2)(3 − 2) = 3.)</p>
<p>(iii) For an uninformed transmitter the channel is unknown at the transmitter, so equal power is allocated to every transmit antenna: P = (P/N)I. The capacity becomes C = B log₂ det{I + (P/(Nσ²)) HH<sup>H</sup>}. For N = M = 1, H = h and C/B = log₂(1 + P|h|²/σ²). Taking the channel gain as the amplitude gain h = 2 (|h|² = 4): C/B = log₂(1 + 1 × 4/0.25) = log₂17 ≈ 4.09 bit/s/Hz.</p></div>
<div class="ans">一句话：d<sub>max</sub> = 5 × 3 = 15；SNR = (10⁻³)<sup>−1/3</sup> = 10，R = 2 log₂10 ≈ 6.64 bit/s/Hz；无信息发射机 P = (P/N)I，单天线时 C/B = log₂(1 + 16) ≈ 4.09 bit/s/Hz。</div>
'''},

'y2425s2-q2a': {'title': '知识讲解 + 详细解析：横向滤波器、迫零抽头与残余 ISI 误码率', 'zh': '''
<h4><span class="st">知识讲解</span>横向滤波器和迫零均衡</h4>
<ul><li><b>横向滤波器</b>（transversal filter，讲义第 6 章）：就是 FIR 滤波器。输入 r<sub>i</sub> 经过一串 Z⁻¹（每个延迟一个符号），每个抽头乘一个系数 c<sub>k</sub>，再相加：y<sub>i</sub> = c₀r<sub>i</sub> + c₁r<sub>i−1</sub> + c₂r<sub>i−2</sub>，即 C(Z) = c₀ + c₁Z⁻¹ + c₂Z⁻²。</li>
<li><b>迫零均衡</b>（zero-forcing, ZF）：要求"信道 × 均衡器 = 1"，即 C(Z) = 1/H(Z)，把 ISI 强行压成零（不管噪声）。1/H(Z) 一般是无穷长，有限个抽头只能取长除法的前几项（第 6 章 p.24 的例子：1/(1 + 0.3Z⁻¹) 的前两个抽头是 1、−0.3）。</li>
<li><b>h 的含义</b>：H(Z) = 1 + hZ⁻¹ 说明有一条直达路径，外加一条晚一个符号、增益为 h 的回波。h = 0 就没有 ISI。</li>
<li><b>快衰落</b>（fast fading）：相干时间和符号时长相当甚至更短，信道在几个符号内就变（第 2 章 p.37）。</li></ul>
<h4><span class="st">详细解析</span>(i) h 的取值</h4>
<p>纯 AWGN、没有衰落：只有一条直达路径、没有多径回波，H(Z) = 1，所以 <b>h = 0</b>，无 ISI，不需要均衡。快衰落信道：h 的幅度和相位都会在很短时间内随机变化，所以 h 不是常数；均衡器系数必须不断重新估计、自适应跟踪，否则很快失配。</p>
<h4><span class="st">详细解析</span>(ii) 迫零抽头（h = 0.2）</h4>
<ol><li>C(Z) = 1/(1 + 0.2Z⁻¹)，长除法（或用 1/(1 + x) = 1 − x + x² − …，x = 0.2Z⁻¹）：<div class="calc">1/(1 + 0.2Z⁻¹) = 1 − 0.2Z⁻¹ + 0.04Z⁻² − 0.008Z⁻³ + …</div></li>
<li>只有三个抽头，取前三项：<div class="calc">c₀ = 1，c₁ = −0.2，c₂ = 0.04</div></li>
<li>检验：<div class="calc">C(Z)H(Z) = (1 − 0.2Z⁻¹ + 0.04Z⁻²)(1 + 0.2Z⁻¹) = 1 + 0.008Z⁻³</div>Z⁻¹、Z⁻² 项抵消，只剩 0.008 的微小残余 ISI，这就是截断带来的误差。</li></ol>
<h4><span class="st">详细解析</span>(iii) 另一种设计的误码率</h4>
<ol><li>噪声标准差：<div class="calc">σ = √0.64 = 0.8</div></li>
<li>设发 s<sub>i</sub> = +1。前一个符号 s<sub>i−1</sub> 等概 ±1，带来 ±0.6 的干扰，分两种情况：<br>• s<sub>i−1</sub> = +1：y 的均值 1.6，错判需 y &lt; 0 → Q(1.6/0.8) = Q(2) = 0.0228<br>• s<sub>i−1</sub> = −1：y 的均值 0.4 → Q(0.4/0.8) = Q(0.5) = 0.3085</li>
<li>平均：<div class="calc">P<sub>e</sub> = ½(0.3085 + 0.0228) ≈ 0.166</div></li>
<li>发 −1 时对称，结果相同。</li></ol>
<p><b>对比</b>：如果没有残余 ISI，P<sub>e</sub> = Q(1/0.8) = Q(1.25) ≈ 0.106。0.6 的残余 ISI 让误码率变成约 1.6 倍，主要来自"均值只剩 0.4"那一半情况，说明这个设计不好。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>原题写 "c₁, c₂, c₃"，但图里标的是 c₀、c₁、c₂，按图作答并写明对应关系。</li>
<li>抽头符号正负交替：+1、−0.2、+0.04。</li>
<li>方差 0.64 要开方成 σ = 0.8 再放进 Q。</li>
<li>Q(0.5) = 0.3085 要会查（表的第一行附近）。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) For an AWGN channel without fading there is only the direct path and no multipath echo, so H(Z) = 1 and h = 0 (no ISI). In a fast-fading channel the coherence time is comparable to or shorter than the symbol duration, so the value of h (amplitude and phase) changes rapidly with time; the equalizer coefficients must therefore be re-estimated and adaptively tracked continuously.</p>
<p>(ii) For zero forcing, C(Z) = 1/H(Z) = 1/(1 + 0.2Z⁻¹) = 1 − 0.2Z⁻¹ + 0.04Z⁻² − 0.008Z⁻³ + … . With three taps, c₀ = 1, c₁ = −0.2 and c₂ = 0.04 (the coefficients labelled in Figure 2). Then C(Z)H(Z) = 1 + 0.008Z⁻³, so only a very small residual ISI remains.</p>
<p>(iii) σ = √0.64 = 0.8. Given s<sub>i</sub> = 1: if s<sub>i−1</sub> = 1, the mean of y<sub>i</sub> is 1.6 and P(error) = Q(1.6/0.8) = Q(2) = 0.0228; if s<sub>i−1</sub> = −1, the mean is 0.4 and P(error) = Q(0.4/0.8) = Q(0.5) = 0.3085. Since s<sub>i−1</sub> = ±1 with equal probability, P<sub>e</sub> = ½(0.3085 + 0.0228) ≈ 0.166, and by symmetry the same result holds for s<sub>i</sub> = −1.</p></div>
<div class="ans">一句话：无衰落时 h = 0，快衰落时 h 快速时变要跟踪；迫零取 1/(1 + 0.2Z⁻¹) 的前三项 1、−0.2、0.04；残余 ISI 0.6 时按 ±0.6 两种情况平均，P<sub>e</sub> ≈ 0.166。</div>
'''},

'y2425s2-q2b': {'title': '知识讲解 + 详细解析：OFDM 速率划分、循环前缀与等容量功率', 'zh': '''
<h4><span class="st">知识讲解</span>OFDM 的速率怎么分，循环前缀怎么写</h4>
<ul><li><b>每符号比特数</b>：M 电平调制每个符号带 log₂M bit。系统比特率 = 符号率 × log₂M。</li>
<li><b>分到 N 个子载波</b>（讲义第 7 章 p.8）：原来一个高速串行流拆成 N 路并行的低速流，每个子载波的符号率是 R<sub>s</sub>/N，符号时长变成 N 倍。总速率不变，但每个符号变长了，ISI 的相对影响变小。</li>
<li><b>循环前缀</b>（cyclic prefix, CP，p.17–21）：每个 OFDM 块前面加长度 T<sub>g</sub> 的保护间隔，里面放的是块<b>尾部</b>的复制。因为 e<sup>j2πkt/T</sup> 以 T 为周期，只要把原表达式的时间范围往前延伸 T<sub>g</sub>，前面多出来的那段自然就是尾巴的复制。接收端丢掉这一段。</li>
<li><b>OFDM 子载波容量</b>（p.24）：N 个子载波是 N 条并行的高斯信道，每条占 1/N 的带宽，所以每赫兹容量 C<sub>k</sub> = (1/N) log₂(1 + P<sub>k</sub>|H<sub>k</sub>|²)（本题 N = 4，所以是 ¼）。</li></ul>
<h4><span class="st">详细解析</span>(i) 速率</h4>
<div class="calc">每符号 log₂4 = 2 bit；系统比特率 = 5×10⁶ × 2 = 10 Mbit/s</div>
<div class="calc">每个子载波：符号率 5/4 = 1.25 Msymbol/s，比特率 10/4 = 2.5 Mbit/s</div>
<p>对应的时长：原符号 T<sub>s</sub> = 1/(5×10⁶) = 0.2 µs，OFDM 符号 T = 4T<sub>s</sub> = 0.8 µs。</p>
<h4><span class="st">详细解析</span>(ii) 加循环前缀</h4>
<div class="calc">x(t) = (1/√T) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub>(t) e<sup>j2π(k/T)t</sup>，　nT − T<sub>g</sub> ≤ t &lt; (n + 1)T</div>
<p>为什么只改区间：表达式本身不变，只把每个块的开始时间提前 T<sub>g</sub>。由于周期性，x(t) 在 [nT − T<sub>g</sub>, nT) 这段等于 [(n+1)T − T<sub>g</sub>, (n+1)T) 那段，也就是尾巴的复制。接收端只取 nT ≤ t &lt; (n + 1)T。（也可以按块周期 T + T<sub>g</sub> 计时来写，意思相同。）</p>
<h4><span class="st">详细解析</span>(iii) 等容量所需功率</h4>
<ol><li>每个子载波都要 ¼ log₂(1 + P<sub>k</sub>|H<sub>k</sub>|²) = 0.9，先乘 4：<div class="calc">log₂(1 + P<sub>k</sub>|H<sub>k</sub>|²) = 3.6 → 1 + P<sub>k</sub>|H<sub>k</sub>|² = 2<sup>3.6</sup> = 12.126</div>计算器：2<sup>3.6</sup> = 10<sup>3.6 × 0.301</sup> = 10<sup>1.084</sup> ≈ 12.13。</li>
<li><div class="calc">P<sub>k</sub>|H<sub>k</sub>|² = 11.126（≈ 11.13）</div></li>
<li>|H<sub>k</sub>|² 分别是 1、0.04、1、1.96：<div class="calc">P₁ = 11.13；P₂ = 11.126/0.04 = 278.1；P₃ = 11.13；P₄ = 11.126/1.96 = 5.68</div></li>
<li><div class="calc">P<sub>total</sub> = 11.13 + 278.1 + 11.13 + 5.68 ≈ 306.1（功率单位）</div></li></ol>
<p><b>观察</b>：最差的子载波（|H₂| = 0.2）一个就用掉 278.1/306.1 ≈ 91% 的功率。"每个子载波容量一样"等于用功率去补偿信道（信道反转），在深衰落的子载波上非常浪费；注水法正好相反，把功率多给好的子载波。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>先乘回 4 再取 2 的幂：2<sup>3.6</sup>，不是 2<sup>0.9</sup>。</li>
<li>|H₂| = 0.2 要平方成 0.04，|H₄| = 1.4 平方成 1.96。</li>
<li>P₂ 用 11.126 算得 278.1；先四舍五入成 11.13 再除得 278.25，只是舍入差别。</li>
<li>CP 只改时间区间，不改表达式；区间写 nT − T<sub>g</sub>，不是 nT + T<sub>g</sub>。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) A 4-level system carries log₂4 = 2 bits per symbol, so the system bit rate is 5 × 10⁶ × 2 = 10 Mbit/s. With N = 4 sub-carriers, each sub-carrier carries 5/4 = 1.25 Msymbol/s, i.e. 10/4 = 2.5 Mbit/s.</p>
<p>(ii) With a cyclic prefix of duration T<sub>g</sub>, each block is extended by T<sub>g</sub> at its start: x(t) = (1/√T) Σ<sub>k=0</sub><sup>N−1</sup> s<sub>k</sub>(t)e<sup>j2π(k/T)t</sup>, nT − T<sub>g</sub> ≤ t &lt; (n + 1)T. Because e<sup>j2πkt/T</sup> is periodic with period T, the extra segment is a copy of the last T<sub>g</sub> of the block (a cyclic prefix); the receiver discards it and processes only nT ≤ t &lt; (n + 1)T.</p>
<p>(iii) For each sub-carrier, ¼ log₂(1 + P<sub>k</sub>|H<sub>k</sub>|²) = 0.9, so 1 + P<sub>k</sub>|H<sub>k</sub>|² = 2<sup>3.6</sup> = 12.126 and P<sub>k</sub>|H<sub>k</sub>|² = 11.126. Hence P₁ = 11.126/1 = 11.13, P₂ = 11.126/0.04 = 278.1, P₃ = 11.13 and P₄ = 11.126/1.96 = 5.68. The total power needed is about 306.1 (power units). The weak sub-carrier |H₂| = 0.2 alone needs about 91% of the total power, showing that equal-capacity allocation is inefficient compared with water-filling.</p></div>
<div class="ans">一句话：10 Mbit/s 分 4 份每份 2.5 Mbit/s；CP 只把区间改成 nT − T<sub>g</sub> ≤ t &lt; (n+1)T；等容量要 P<sub>k</sub>|H<sub>k</sub>|² = 2<sup>3.6</sup> − 1 = 11.126，总功率 ≈ 306.1，差子载波吃掉 91%。</div>
'''},

'y2425s2-q3': {'title': '知识讲解 + 详细解析：FDD-TDMA 信道、选簇、Erlang B、分裂与扇区', 'zh': '''
<h4><span class="st">知识讲解</span>本题用到的五块知识</h4>
<div class="tw"><table class="mini"><thead><tr><th>步骤</th><th>知识</th><th>讲义 Part A</th></tr></thead><tbody>
<tr><td>数信道</td><td>FDD：一半上行一半下行；信道数 = 载波数 × 每帧时隙数</td><td>p.37、p.82</td></tr>
<tr><td>选簇</td><td>S/I = Q<sup>n</sup>/6，Q = √(3N)；合法 N = i² + ij + j² = 1、3、4、7、9、12…</td><td>p.75–78、p.88–89</td></tr>
<tr><td>能否满足 GoS</td><td>Erlang B 查表：已知 M 和 1%，读出能承载的 A</td><td>p.118–120</td></tr>
<tr><td>小区分裂</td><td>小区变小，每小区信道数不变（SIR 只看 Q = D/R），每小区用户变少</td><td>p.135–138</td></tr>
<tr><td>扇区化</td><td>3 扇区只剩 2 个干扰：S/I = 1/[Q<sup>−n</sup> + (Q+0.7)<sup>−n</sup>]，可以用更小的簇</td><td>p.143–146</td></tr>
</tbody></table></div>
<p>老师课上强调：扇区化提高 SIR，但每个扇区信道变少、集群效率下降，这一点要会讲；Erlang B 一律查表。</p>
<h4><span class="st">详细解析</span>(a) 每小区双工信道数</h4>
<ol><li>FDD：40 MHz 一半上行、一半下行，每方向 20 MHz；扣掉控制信令 2 MHz，剩 18 MHz。</li>
<li>"carrier frequency is 200 KHz" 理解为每个载波<b>带宽</b> 200 kHz（GSM 式）：<div class="calc">载波数 = 18 MHz / 200 kHz = 90；双工信道 = 90 × 8 = 720</div></li>
<li>选簇：要 S/I ≥ 18 dB = 10<sup>1.8</sup> = 63.1：<div class="calc">Q<sup>3.7</sup>/6 ≥ 63.1 → Q<sup>3.7</sup> ≥ 378.6 → Q ≥ 378.6<sup>1/3.7</sup> = 4.98</div><div class="calc">N = Q²/3 ≥ 4.98²/3 = 8.25 → 取合法值 N = 9</div>检查：N = 7 只有 16.7 dB ✗，N = 9 为 18.7 dB ✓。</li>
<li><div class="calc">每小区信道 = 720/9 = 80 条双工信道</div></li></ol>
<h4><span class="st">详细解析</span>(b) 能否满足 1% 阻塞</h4>
<div class="calc">小区面积 = 2.598 × 1² = 2.598 km²；用户 = 2.598 × 2000 = 5196；话务需求 = 5196 × 0.03 = 155.9 E</div>
<div class="calc">Erlang B（M = 80，1%）：能承载 A ≈ 65.4 E</div>
<p>155.9 E 远大于 65.4 E，<b>不能</b>满足。按 Erlang B 公式算，80 条信道承受 155.9 E 时阻塞率约 49%。</p>
<h4><span class="st">详细解析</span>(c) 小区分裂</h4>
<ol><li>为什么分裂有用：小区缩小后 D 和 R 同比例缩小，Q 不变，所以 N = 9、每小区 80 条都不变；但每个小区覆盖的用户变少。</li>
<li>要求每小区话务 ≤ 65.4 E：<div class="calc">面积 ≤ 65.4/(2000 × 0.03) = 1.09 km²</div><div class="calc">R = √(1.09/2.598) ≈ 0.648 km ≈ 650 m</div></li>
<li>代价：全城 155.9 km² 需要约 155.9/1.09 ≈ 144 个小区（原来 60 个，约 2.4 倍基站）。</li></ol>
<h4><span class="st">详细解析</span>(d) 三扇区</h4>
<ol><li>扇区化后只剩 2 个干扰，试更小的簇：<div class="calc">N = 3：Q = 3 → 16.0 dB ✗；　N = 4：Q = √12 = 3.46 → 18.2 dB ✓</div></li>
<li>N = 4：每小区 720/4 = 180 条，每扇区 60 条。每小区 90/4 = 22.5 个载波，分给 3 个扇区每个 7.5 个——半个载波正是靠"一个载波可以被两个扇区共用"（按时隙分）实现，7.5 × 8 = 60 条。</li>
<li>Erlang B（M = 60，1%）：A ≈ 46.95 E/扇区，每小区 3 × 46.95 = 140.8 E。</li>
<li>全城面积 60 × 2.598 = 155.9 km²，总话务 155.9 × 2000 × 0.03 = 9353 E：<div class="calc">小区数 = 9353/140.8 = 66.4 → 67 个（半径约 0.95 km）</div></li></ol>
<p>对比：不改簇（N = 9）只加扇区，每扇区约 26–27 条，需要约 178 个小区，比分裂还多。扇区化必须配合缩小簇才划算。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>FDD 要先把带宽对半分，再扣控制信道。</li>
<li>N 必须取合法值（i² + ij + j²），8.25 → 9，不是 8。</li>
<li>18 dB 换线性 63.1；n = 3.7 不是 4。</li>
<li>小区分裂不改每小区信道数；小区数向上取整。</li>
<li>(d) 题意可以有不同理解，答卷上写清自己的假设（选 N = 4 的理由）。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Assumptions: hexagonal cells, uniform traffic, Erlang B (blocked calls cleared), six equidistant first-tier interferers with the mobile at the cell edge, each carrier has a bandwidth of 200 kHz.</p>
<p>(a) FDD: 40 MHz is split into 20 MHz per direction; removing 2 MHz for control leaves 18 MHz. Number of carriers = 18 MHz / 200 kHz = 90, so the system has 90 × 8 = 720 duplex channels. SIR requirement: Q<sup>n</sup>/6 ≥ 10<sup>1.8</sup> = 63.1, so Q<sup>3.7</sup> ≥ 378.6, Q ≥ 4.98 and N = Q²/3 ≥ 8.25. The smallest valid cluster size is N = 9 (SIR = 18.7 dB; N = 7 gives only 16.7 dB). Channels per cell = 720/9 = 80.</p>
<p>(b) Cell area = (3√3/2)(1)² = 2.598 km²; subscribers per cell = 2.598 × 2000 = 5196; offered traffic = 5196 × 0.03 = 155.9 E. From the Erlang B table, 80 channels at 1% blocking support only about 65.4 E. Since 155.9 E is much larger than 65.4 E, the system cannot support 1% blocking.</p>
<p>(c) With cell splitting the cluster size and the 80 channels per cell are unchanged (the SIR depends only on Q = D/R), but each smaller cell serves fewer users. Requiring the traffic per cell to be at most 65.4 E: area ≤ 65.4/(2000 × 0.03) = 1.09 km², so R = √(1.09/2.598) ≈ 0.65 km. Hence cell splitting achieves 1% blocking with a new cell radius of about 650 m.</p>
<p>(d) With 3-sector antennas only two interferers remain: SIR = 1/[Q<sup>−n</sup> + (Q + 0.7)<sup>−n</sup>]. N = 3 gives 16.0 dB (not enough) and N = 4 gives 18.2 dB, so N = 4 is used. Channels per cell = 720/4 = 180, i.e. 60 per sector (22.5 carriers per cell; sharing a carrier between two sectors gives 7.5 carriers = 60 channels per sector). From the Erlang B table, A ≈ 46.9 E per sector, 140.8 E per cell. Total area = 60 × 2.598 = 155.9 km², total traffic = 155.9 × 2000 × 0.03 = 9353 E, so the number of cells required = 9353/140.8 = 66.4, i.e. 67 cells.</p></div>
<div class="ans">一句话：720 条信道、SIR 选 N = 9 → 每小区 80 条只能承载 65.4 E，远低于 155.9 E；分裂到 R ≈ 0.65 km 即可；三扇区让 N 降到 4，每扇区 60 条，约 67 个小区。</div>
'''},

'y2425s2-q4a': {'title': '知识讲解 + 详细解析：蜂窝数据库与 HLR / VLR', 'zh': '''
<h4><span class="st">知识讲解</span>蜂窝系统的六个基本组成</h4>
<p>讲义 Part A p.11 的框图：① 移动台（MS）、② 基站（BS）、③ <b>数据库（Databases）</b>、④ 安全机制、⑤ 空中接口标准、⑥ 移动交换中心（MTSO / MSC）连到 PSTN。老师课上说 MTSO 是整个蜂窝系统的"大脑"；而大脑做决定（这个用户能不能打、现在在哪、怎么接通）靠的就是数据库。</p>
<p><span class="st">课外补充</span>讲义只在框图里写了 "Databases"，HLR / VLR 的细节来自 GSM 标准结构（也是 HW1 Q1(a) 的答法），下面的内容属于课外补充，但是本题的得分点。</p>
<div class="tw"><table class="mini"><thead><tr><th></th><th>HLR（归属位置寄存器）</th><th>VLR（拜访位置寄存器）</th></tr></thead><tbody>
<tr><td>位置</td><td>用户的归属网络，一个运营商通常一个（逻辑上）</td><td>每个 MSC 服务区一个，分布式</td></tr>
<tr><td>记录性质</td><td>永久的主记录</td><td>临时副本</td></tr>
<tr><td>存什么</td><td>签约资料、业务权限、鉴权参数、"当前在哪个 VLR/MSC 区域"</td><td>当前在本区的所有用户（本地和漫游）的资料和较精确的位置区</td></tr>
<tr><td>何时更新</td><td>用户换到另一个 MSC 区域时</td><td>用户进入本区时从 HLR 下载，离开后删除</td></tr>
<tr><td>比喻</td><td>户口所在地</td><td>暂住登记</td></tr>
</tbody></table></div>
<h4><span class="st">详细解析</span>答题要点展开</h4>
<ol><li><b>数据库的基本功能</b>：保存用户信息（号码、签约业务、计费）和位置信息，供 MSC 在呼叫建立、寻呼被叫、鉴权、漫游和切换时查询。为什么重要：没有它，网络不知道"这个用户是谁、有没有权限、现在在哪"，就无法接通。</li>
<li><b>HLR</b>：每个用户在归属网络里的永久主记录，集中存储；记录用户当前所在的 VLR/MSC，来电时网络先问 HLR "他在哪个区"。</li>
<li><b>VLR</b>：和 MSC 关联的临时数据库，只存当前在本区的用户。好处：本区的呼叫、寻呼直接查 VLR，不必每次都去问可能很远的 HLR，减少信令和时延。</li>
<li><b>加分点（流程）</b>：用户移动到新区域 → 新 VLR 向 HLR 登记 → HLR 更新位置并通知旧 VLR 删除记录。</li></ol>
<h4><span class="st">易错</span>注意</h4>
<ul><li>VLR 不只存漫游用户，本地用户在本区也登记在 VLR。</li>
<li>HLR 存的是"在哪个 VLR/MSC 区域"，不是精确到小区的位置。</li>
<li>8 分题：功能 + 区别都要写，最好用对比的句式（永久 vs 临时、集中 vs 分布、全部签约信息 vs 当前在场用户）。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p><b>Basic functions of the database unit:</b> the databases store subscriber information (identity, subscribed services, authentication and billing data) and location information of the mobile users. The MSC/MTSO queries them during call set-up, paging of the called user, authentication, roaming and handoff. Without the databases, the network would not know who the user is, what services the user may use and where the user is located.</p>
<p><b>Home Location Register (HLR):</b> a permanent, centralised database in the subscriber's home network. It holds the master record of every subscriber registered with the operator, including the subscription profile, authentication parameters and the identity of the VLR/MSC area where the subscriber is currently located. An operator normally has one (logical) HLR.</p>
<p><b>Visitor Location Register (VLR):</b> a temporary, distributed database associated with each MSC service area. It stores a copy of the relevant data of all subscribers currently in that area, both local users and visiting (roaming) users, together with their current location area. When a user enters the area the record is downloaded from the HLR, and it is deleted when the user leaves. Local calls and paging are handled by the VLR without querying the HLR each time, which reduces signalling.</p>
<p><b>Differences:</b> the HLR is permanent, centralised and holds complete subscription data for its own subscribers; the VLR is temporary, located in each service area and holds only the users currently present. When a user moves to a new area, the new VLR registers the user with the HLR, the HLR updates the location and instructs the old VLR to delete its record.</p></div>
<div class="ans">一句话：数据库存用户签约信息和位置，供 MSC 接续、寻呼、鉴权和漫游查询；HLR 是永久集中的"户口"，VLR 是各服务区临时的"暂住登记"。</div>
'''},

'y2425s2-q4b': {'title': '知识讲解 + 详细解析：IoT 通信网络层的四个子层', 'zh': '''
<h4><span class="st">知识讲解</span>通信网络层在整个 IoT 栈里的位置</h4>
<p>核心 IoT 功能栈有三层：Things 层 → <b>通信网络层</b> → 应用与分析层（讲义 Part B p.88–90）。智能物体（smart objects）如果不能自给自足，就要把采集到的信息报告出去、和别的物体交换、或接受管理平台控制，这些都靠通信网络层。它由下往上分四个子层（p.89–99），可以理解为"数据从传感器走到应用要过的四道关"。</p>
<div class="tw"><table class="mini"><thead><tr><th>子层</th><th>负责什么</th><th>典型技术</th></tr></thead><tbody>
<tr><td>接入网（Access network）</td><td>最后一公里，把物体接进网络</td><td>802.11ah、802.15.4g、LoRa；PAN/HAN/NAN/FAN/LAN/WAN</td></tr>
<tr><td>网关与回传（Gateways and backhaul）</td><td>把一片区域的物体汇聚到网关，再长距离送回中心</td><td>网关 + 蜂窝 / 光纤等长距离链路</td></tr>
<tr><td>网络传输（Network transport）</td><td>用开放标准的网络层、传输层协议连接各种设备和介质</td><td>IP、UDP、TCP</td></tr>
<tr><td>IoT 网络管理（IoT network management）</td><td>头端应用和传感器之间的数据交换</td><td>HTTP、WebSocket</td></tr>
</tbody></table></div>
<h4><span class="st">详细解析</span>每个子层的特点（为什么要这样设计）</h4>
<ol><li><b>接入网子层</b>：IoT 网络的最后一公里，通常是无线技术。不同技术的覆盖范围、功耗、速率不同，所以按范围分成 PAN、HAN、NAN、FAN、LAN、WAN 等；技术和它支持的拓扑（星形、网状等）直接相关（p.94–97）。老师课上提到：mesh 拓扑有多条备选路由，更可靠。</li>
<li><b>网关与回传子层</b>：一个公共通信系统把某一区域的多个物体组织到一个网关周围，网关负责"跨介质"通信，用更长距离的介质把数据转发到头端中心站。物体可以静止或在小范围内移动，网关一般固定（p.98）。</li>
<li><b>网络传输子层</b>：要支持多行业、多介质，协议必须开放、标准化；还要可扩展到单个网络里成千上万甚至上百万个传感器，并保证安全。IP 满足这些要求，能嵌入各种物体、跑在低功耗、低带宽、高丢包的网络上；上面的 TCP 由网络控制可靠传输，UDP 则把控制交给应用（p.98–99）。</li>
<li><b>IoT 网络管理子层</b>：应用层协议负责智能物体和其他系统之间的数据传输。例如基于 TCP 的 HTTP（传感器作为客户端连接 IoT 应用）；WebSocket 是轻量的 Web 派生协议，适合低内存、低功耗、低带宽、高丢包环境，提供简单的双向连接（p.99）。</li></ol>
<h4><span class="st">易错</span>注意</h4>
<ul><li>顺序自下而上：接入 → 网关回传 → 传输 → 管理，按这个顺序写，阅卷人好对。</li>
<li>网络传输是 IP/TCP/UDP，网络管理是 HTTP/WebSocket，别放反。</li>
<li>8 分 = 4 个子层 × 2 分：每个子层写"名字 + 作用 + 例子"三样。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>The communications network layer of the Core IoT Functional Stack connects the smart objects to external systems and is divided into four sublayers:</p>
<p><b>1. Access network sublayer:</b> the last mile of the IoT network, typically wireless technologies such as IEEE 802.11ah, 802.15.4g and LoRa. Technologies are classified by range (PAN, HAN, NAN, FAN, LAN, WAN), and each technology supports particular topologies (e.g. star or mesh).</p>
<p><b>2. Gateways and backhaul sublayer:</b> smart objects in a given area are organised around a common gateway, which performs the inter-medium communication and forwards the collected data over a longer-range backhaul medium (e.g. cellular or fibre) to a headend central station. The objects may be static or mobile within a limited area, while the gateway is usually static.</p>
<p><b>3. Network transport sublayer:</b> open, standards-based network and transport protocols, mainly IP with UDP or TCP, connect the variety of devices and media. They must be scalable to thousands or millions of sensors and secure. IP can run over low-power, low-bandwidth and lossy networks; TCP lets the network control reliable delivery, while UDP leaves the control to the application.</p>
<p><b>4. IoT network management sublayer:</b> application protocols that allow the headend applications to exchange data with the sensors, e.g. HTTP over TCP (the sensor acts as a client of the IoT application) and WebSocket, a lightweight web-derived protocol that provides a simple bidirectional connection in low-memory, low-power, low-bandwidth and high-loss environments.</p></div>
<div class="ans">一句话：接入网（最后一公里无线：802.11ah、802.15.4g、LoRa）→ 网关与回传（区域汇聚、长距离送回中心）→ 网络传输（IP、UDP/TCP）→ 网络管理（HTTP、WebSocket）。</div>
'''},

'y2425s2-q4c': {'title': '知识讲解 + 详细解析：承载话务量、中继效率与换簇大小', 'zh': '''
<h4><span class="st">知识讲解</span>提供话务、承载话务和中继效率</h4>
<ul><li><b>提供话务量</b>（offered traffic）A：用户想打的话务总量。Erlang B 表给的是在 M 条信道、阻塞率 P<sub>B</sub> 下能接受的最大 A（讲义 Part A p.118–120）。</li>
<li><b>承载话务量</b>（carried traffic）：真正接通的部分，被阻塞的那部分不算：C = A(1 − P<sub>B</sub>)（p.120）。题目里的 "carrier load" 是 carried load 的笔误。</li>
<li><b>中继效率</b>（trunking efficiency）：每条信道平均承担的话务，取值 0–1（p.123–124）。讲义例子用 A/M（10 条、1% 时 4.46/10 = 44.6%）；严格按承载话务算是 A(1 − P<sub>B</sub>)/M。两种都写上最保险。</li>
<li><b>用户数</b> = A/A<sub>u</sub>，A<sub>u</sub> = 每小时呼叫数 × 每次时长（小时）。</li>
<li>讲义 p.44 的 AMPS 例题正好也是"56 条、2% → 45.9 E"，可以对照。</li></ul>
<h4><span class="st">详细解析</span>(i) N = 9</h4>
<ol><li><div class="calc">每小区信道 M = 504/9 = 56</div></li>
<li>查 Erlang B（M = 56，P<sub>B</sub> = 2%）：<div class="calc">A ≈ 45.9 E</div></li>
<li>承载话务：<div class="calc">C = 45.9 × (1 − 0.02) = 45.0 E</div></li>
<li>中继效率：<div class="calc">η = 45.9/56 ≈ 0.82（按承载话务 45.0/56 ≈ 0.80）</div></li></ol>
<h4><span class="st">详细解析</span>(ii) 用户数</h4>
<div class="calc">A<sub>u</sub> = 2 × 15/60 = 0.5 E/用户</div>
<div class="calc">U = 45.9/0.5 = 91.8 → 91 个用户</div>
<p>为什么向下取整：92 个人会产生 46 E，超过 45.9 E，阻塞率就会超过 2%。</p>
<p>为什么信道池越大效率越高（下一问要用）：呼叫是随机到达的，话务量围绕平均值上下波动。信道少时，为了让偶尔的高峰也只有 2% 被阻塞，平时必须空着很大一部分信道；信道多时，大量用户的波动互相抵消，相对平均值的起伏变小，可以让每条信道平均更忙。所以同样的 GoS 下，A/M 随 M 增大而增大（讲义 p.122–124："1 组 10 条比 2 组 5 条多承载 60% 的话务"）。</p>
<h4><span class="st">详细解析</span>(iii) 换成 N = 7</h4>
<ol><li><div class="calc">M = 504/7 = 72；查表 A ≈ 61.0 E</div></li>
<li><div class="calc">承载 C = 61.0 × 0.98 = 59.8 E；η = 61.0/72 ≈ 0.85（按承载 0.83）</div></li>
<li><div class="calc">用户 = 61.0/0.5 = 122 人</div></li></ol>
<p><b>评论</b>：簇变小，每小区信道从 56 增到 72（多 29%），能提供的话务量（表值 A）却从 45.9 增到 61.0 E（多 33%），中继效率从 0.82 升到 0.85——信道池越大，集群效率越高。代价是同频小区离得更近，按 n = 4 的简化模型 SIR 从 20.85 dB（N = 9）降到 18.66 dB（N = 7）（讲义 p.89），余量变小。</p>
<h4><span class="st">易错</span>注意</h4>
<ul><li>A<sub>u</sub> = 2 次/小时 × 15/60 小时 = 0.5 E，15 分钟要换成小时。</li>
<li>查 2% 那一列，不是 1%。</li>
<li>用户数向下取整（91，不是 92）。</li>
<li>评论要两面写：容量和效率提高，SIR 下降。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(i) Channels per cell = 504/9 = 56. From the Erlang B table with M = 56 and GOS = 2%, the offered traffic is A ≈ 45.9 Erlangs per cell, so the carried load is A(1 − P<sub>B</sub>) = 45.9 × 0.98 ≈ 45.0 E. Trunking efficiency = 45.9/56 ≈ 0.82 (or 45.0/56 ≈ 0.80 using the carried load).</p>
<p>(ii) Traffic per user A<sub>u</sub> = 2 × 15/60 = 0.5 E. Number of users = 45.9/0.5 = 91.8, so 91 users can be accommodated per cell (rounded down to keep the blocking at or below 2%).</p>
<p>(iii) For N<sub>c</sub> = 7: channels per cell = 504/7 = 72, A ≈ 61.0 E, carried load = 61.0 × 0.98 ≈ 59.8 E, trunking efficiency = 61.0/72 ≈ 0.85 (0.83 using the carried load), and about 122 users per cell. Comment: a smaller cluster gives more channels per cell (+29%) and the traffic capacity increases even more (+33%) because a larger trunk group has a higher trunking efficiency. However, co-channel cells are closer, so the co-channel interference increases (SIR falls from about 20.9 dB to 18.7 dB for n = 4), reducing the margin above the required SIR.</p></div>
<div class="ans">一句话：56 条/小区查表 45.9 E，承载 45.0 E，η ≈ 0.82，91 人；换 N = 7 后 72 条、61.0 E、η ≈ 0.85、122 人，容量和效率都升，但 SIR 降。</div>
'''},

}

NOTES = '''y2324s2-q2b: with taps {1, −0.6, 0.2} at Ts = 1 µs the channel memory is about 2 µs, so the given 1 µs guard interval is shorter than the maximum delay spread required by Ch7 p.5/p.17; the box mentions this neutrally and keeps the question's 1 µs (block 5 µs, loss 0.97 dB).
y2324s2-q4c: part (ii) says "SNR_dB" but means SIR; the box says so (no change to the numbers).'''
