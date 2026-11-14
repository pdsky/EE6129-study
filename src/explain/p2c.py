# -*- coding: utf-8 -*-
# 知识讲解 + 详细解析 for mock quiz group p2c (prac_8.html: p8q1, p8q7–p8q11). Bilingual: 'zh' + 'en'.
# Numbers checked by check_p2c.py (run with /usr/bin/python3).
XPL = {

# ------------------------------------------------------------------ p8q1
'p8q1': {
'title': '知识讲解 + 详细解析：全概率、贝叶斯与离散期望方差',
'title_en': 'Concept + step by step: total probability, Bayes, discrete mean and variance',
'zh': r'''<h4><span class="st">知识讲解</span>条件概率、全概率、贝叶斯是一套工具</h4>
<p><b>条件概率</b>（conditional probability）P(A | B) 读作"已知 B 发生了，A 发生的概率"。本题给的误比特率就是条件概率：P(e | G) = 10⁻⁴ 的意思是"在好状态下，一个比特出错的概率"。</p>
<p><b>乘法规则</b>（multiplication rule，讲义第 1b 章 p.6）：P(A ∩ B) = P(A) P(B | A)。例如"处于坏状态并且出错"的概率 = P(B) P(e | B) = 0.3 × 10⁻² = 3 × 10⁻³。</p>
<p><b>全概率定理</b>（total probability theorem，p.8）：把所有可能的情况 A₁、A₂、……（互不重叠、合起来是全部）分开，每种情况各算"这种情况发生并且 B 发生"，再全部加起来：P(B) = Σ P(A<sub>i</sub>) P(B | A<sub>i</sub>)。讲义叫它"分而治之"（divide and conquer）。</p>
<p><b>贝叶斯公式</b>（Bayes' rule，p.9，蓝框必背）：已知结果 B，反过来问原因 A<sub>i</sub>：\(P(A_i\mid B)=\dfrac{P(A_i)\,P(B\mid A_i)}{\sum_j P(A_j)\,P(B\mid A_j)}\)。分子是乘法规则，分母就是全概率。P(A<sub>i</sub>) 叫先验概率（a priori），P(A<sub>i</sub> | B) 叫后验概率（a posteriori）。</p>
<p>老师课上强调：往年有人把 P(B) 只写成一项 P(A₁)P(B | A₁)，全概率<b>必须对所有情况求和</b>；贝叶斯在第 3、6 章（最大似然检测、MLSE）还会反复用到。</p>
<p>把概率换成"个数"最好理解。假设发送 100 万个比特：</p>
<div class="tw"><table class="mini"><thead><tr><th>状态</th><th>发送的比特数</th><th>出错的比特数</th></tr></thead><tbody>
<tr><td>好（概率 0.7）</td><td>70 万</td><td>70 万 × 10⁻⁴ = 70</td></tr>
<tr><td>坏（概率 0.3）</td><td>30 万</td><td>30 万 × 10⁻² = 3000</td></tr>
<tr><td>合计</td><td>100 万</td><td>3070</td></tr>
</tbody></table></div>
<p>(a) 总误码率 = 3070 / 100 万；(b) 在所有出错的比特里，坏状态贡献的占 3000 / 3070。这就是全概率和贝叶斯的直观版。</p>
<h4><span class="st">详细解析</span>(a) 全概率：分情况，再加权求和</h4>
<ol>
<li>做什么：把"出错"按发送时的状态分成两种情况。为什么：每种状态下的误码率已知，但不知道某个比特是在哪种状态下发的，只能两种都算、按出现概率加权。</li>
<li>怎么算：<div class="calc">P(G) P(e | G) = 0.7 × 10⁻⁴ = 7 × 10⁻⁵<br>P(B) P(e | B) = 0.3 × 10⁻² = 3 × 10⁻³<br>P<sub>e</sub> = 7 × 10⁻⁵ + 3 × 10⁻³ = 0.00007 + 0.003 = 3.07 × 10⁻³</div></li>
<li>计算器提示：两个数差两个数量级，先都写成小数再相加，不容易错位。</li>
</ol>
<h4><span class="st">详细解析</span>(b) 贝叶斯：由结果反推原因</h4>
<p>做什么：已知"出错了"，求"当时是坏状态"的后验概率。为什么答案不是 0.3：0.3 是看到结果之前的先验；"出错"这个信息让坏状态的可能性大大增加，因为坏状态下出错的概率是好状态的 100 倍。</p>
<div class="calc">P(B | e) = P(B) P(e | B) / P<sub>e</sub> = 3 × 10⁻³ / 3.07 × 10⁻³ = 0.977<br>P(G | e) = 7 × 10⁻⁵ / 3.07 × 10⁻³ = 0.023<br>检验：0.977 + 0.023 = 1</div>
<p>对比一下：如果知道这个比特<b>没有</b>出错，坏状态的概率 = 0.3 × 0.99 / (1 − 0.00307) = 0.298，几乎还是 0.3。"出错"带来的信息很多，"没出错"几乎不改变判断，因为两种状态下绝大多数比特都是对的。</p>
<h4><span class="st">知识讲解</span>离散随机变量的期望和方差</h4>
<p>离散随机变量（discrete random variable）只取有限几个值，每个值有一个概率。<b>期望</b>（expectation，也叫均值 mean，p.10，老师说要背）E[X] = Σ x P<sub>X</sub>(x)，就是"按概率加权的平均"。<b>方差</b>（variance，p.11）V[X] = E[(X − E[X])²] = E[X²] − (E[X])²，衡量取值离平均值有多分散；标准差是方差开根号，单位和 X 一样。</p>
<p>讲义 p.10 还有一句：一般来说 E[g(X)] ≠ g(E[X])（老师说这是往年常见错误）。dB 换算就是一个 g：g(γ) = 10 log₁₀γ。"先换成 dB 再平均"算的是 E[g(γ)]，"先平均再换成 dB"算的是 g(E[γ])，两者不相等。题目问"平均 SNR 用 dB 表示"，要的是后者。</p>
<h4><span class="st">详细解析</span>(c) 先换线性值，再列表算</h4>
<div class="tw"><table class="mini"><thead><tr><th>状态</th><th>概率 p</th><th>SNR（dB）</th><th>线性 γ</th><th>γ·p</th><th>γ²·p</th></tr></thead><tbody>
<tr><td>好</td><td>0.7</td><td>10 dB</td><td>10</td><td>7</td><td>70</td></tr>
<tr><td>坏</td><td>0.3</td><td>0 dB</td><td>1</td><td>0.3</td><td>0.3</td></tr>
<tr><td>合计</td><td>1</td><td></td><td></td><td>7.3</td><td>70.3</td></tr>
</tbody></table></div>
<div class="calc">10 dB → 10^(10/10) = 10；0 dB → 10⁰ = 1<br>E[γ] = 7 + 0.3 = 7.3<br>E[γ²] = 70 + 0.3 = 70.3<br>Var(γ) = 70.3 − 7.3² = 70.3 − 53.29 = 17.01；标准差 = √17.01 = 4.12<br>平均 SNR = 10 log₁₀7.3 = 10 × 0.8633 = 8.63 dB</div>
<p>检验（按定义算方差）：0.7 × (10 − 7.3)² + 0.3 × (1 − 7.3)² = 0.7 × 7.29 + 0.3 × 39.69 = 5.103 + 11.907 = 17.01，和上面一样。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>(b) 写成 0.3：把先验当成了后验。</li>
<li>贝叶斯的分母只写了坏状态那一项，结果等于 1，显然不对；分母是 (a) 的总和。</li>
<li>直接平均 dB 值：0.7 × 10 + 0.3 × 0 = 7 dB，相当于线性 5.01，比正确的 7.3 小。老师说没做 dB ↔ 线性换算会扣分。</li>
<li>方差忘了减 (E[γ])²，写成 70.3；也不要把方差再换成 dB，方差没有 dB 的意义，题目也没问。</li>
<li>10⁻⁴ 和 10⁻² 相加时数量级对错。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Let G and B denote the good and bad states and e a bit error: P(G) = 0.7, P(B) = 0.3, P(e | G) = 10⁻⁴, P(e | B) = 10⁻².</p><p>(a) By the total probability theorem, P<sub>e</sub> = P(G)P(e | G) + P(B)P(e | B) = 0.7 × 10⁻⁴ + 0.3 × 10⁻² = 3.07 × 10⁻³.</p><p>(b) By Bayes' rule, P(B | e) = P(B)P(e | B) / P<sub>e</sub> = (3 × 10⁻³) / (3.07 × 10⁻³) = 0.977.</p><p>(c) In linear scale the SNR is 10 (10 dB) with probability 0.7 and 1 (0 dB) with probability 0.3. E[γ] = 0.7 × 10 + 0.3 × 1 = 7.3, i.e. 10 log₁₀7.3 = 8.63 dB. E[γ²] = 0.7 × 100 + 0.3 × 1 = 70.3, so Var(γ) = 70.3 − 7.3² = 17.01. The dB values must not be averaged directly, because E[g(X)] ≠ g(E[X]).</p></div>
<div class="ans">一句话：先列"状态—概率—条件概率"表；全概率是加权求和，贝叶斯是"其中一项 ÷ 总和"；求均值和方差前先把 dB 换成线性值。</div>''',
'en': r'''<h4><span class="st">Concept</span>Conditional probability, total probability and Bayes are one toolkit</h4>
<p><b>Conditional probability</b> P(A | B) reads "the probability of A, given that B has happened". The bit error probabilities in this question are conditional probabilities: P(e | G) = 10⁻⁴ means "the probability that a bit is in error when the link is in the good state".</p>
<p><b>Multiplication rule</b> (Ch 1b p.6): P(A ∩ B) = P(A) P(B | A). For example, the probability of "bad state and error" = P(B) P(e | B) = 0.3 × 10⁻² = 3 × 10⁻³.</p>
<p><b>Total probability theorem</b> (p.8): split all possible cases A₁, A₂, … (non-overlapping, together covering everything), compute "this case happens and B happens" for each, then add them all: P(B) = Σ P(A<sub>i</sub>) P(B | A<sub>i</sub>). The slide calls it "divide and conquer".</p>
<p><b>Bayes' rule</b> (p.9, blue box, memorise): given the result B, ask backwards about the cause A<sub>i</sub>: \(P(A_i\mid B)=\dfrac{P(A_i)\,P(B\mid A_i)}{\sum_j P(A_j)\,P(B\mid A_j)}\). The numerator is the multiplication rule, the denominator is total probability. P(A<sub>i</sub>) is the a priori probability and P(A<sub>i</sub> | B) the a posteriori probability.</p>
<p>The lecturer stressed in class: in past years some students wrote P(B) as the single term P(A₁)P(B | A₁); total probability <b>must sum over all cases</b>. Bayes' rule comes back again and again in Ch 3 and Ch 6 (maximum likelihood detection, MLSE).</p>
<p>Turning probabilities into counts makes it easiest to see. Suppose 1 million bits are sent:</p>
<div class="tw"><table class="mini"><thead><tr><th>State</th><th>Bits sent</th><th>Bits in error</th></tr></thead><tbody>
<tr><td>Good (probability 0.7)</td><td>0.7 million</td><td>0.7 million × 10⁻⁴ = 70</td></tr>
<tr><td>Bad (probability 0.3)</td><td>0.3 million</td><td>0.3 million × 10⁻² = 3000</td></tr>
<tr><td>Total</td><td>1 million</td><td>3070</td></tr>
</tbody></table></div>
<p>(a) The overall error rate = 3070 / 1 million; (b) among all bits in error, the share from the bad state is 3000 / 3070. That is the intuitive version of total probability and Bayes.</p>
<h4><span class="st">Step by step</span>(a) Total probability: split into cases, then a weighted sum</h4>
<ol>
<li>What: split "error" by the state at the time the bit was sent. Why: the error rate in each state is known, but we do not know which state a given bit was sent in, so we compute both and weight them by how often each state occurs.</li>
<li>How: <div class="calc">P(G) P(e | G) = 0.7 × 10⁻⁴ = 7 × 10⁻⁵<br>P(B) P(e | B) = 0.3 × 10⁻² = 3 × 10⁻³<br>P<sub>e</sub> = 7 × 10⁻⁵ + 3 × 10⁻³ = 0.00007 + 0.003 = 3.07 × 10⁻³</div></li>
<li>Calculator hint: the two numbers differ by two orders of magnitude; write both as decimals before adding so the digits line up.</li>
</ol>
<h4><span class="st">Step by step</span>(b) Bayes: from the result back to the cause</h4>
<p>What: knowing "an error happened", find the a posteriori probability that the link was in the bad state. Why the answer is not 0.3: 0.3 is the a priori probability before seeing the result; the information "error" makes the bad state much more likely, because errors are 100 times more likely in the bad state than in the good state.</p>
<div class="calc">P(B | e) = P(B) P(e | B) / P<sub>e</sub> = 3 × 10⁻³ / 3.07 × 10⁻³ = 0.977<br>P(G | e) = 7 × 10⁻⁵ / 3.07 × 10⁻³ = 0.023<br>Check: 0.977 + 0.023 = 1</div>
<p>For comparison: if we know the bit was <b>not</b> in error, the probability of the bad state = 0.3 × 0.99 / (1 − 0.00307) = 0.298, still almost 0.3. "Error" carries a lot of information; "no error" hardly changes the picture, because almost all bits are correct in both states.</p>
<h4><span class="st">Concept</span>Mean and variance of a discrete random variable</h4>
<p>A discrete random variable takes only a few values, each with a probability. The <b>expectation</b> (mean, p.10, the lecturer said to memorise it) E[X] = Σ x P<sub>X</sub>(x) is the probability-weighted average. The <b>variance</b> (p.11) V[X] = E[(X − E[X])²] = E[X²] − (E[X])² measures how spread out the values are around the mean; the standard deviation is its square root and has the same unit as X.</p>
<p>Slide p.10 also says: in general E[g(X)] ≠ g(E[X]) (the lecturer said this is a common past mistake). Converting to dB is such a g: g(γ) = 10 log₁₀γ. "Convert to dB, then average" computes E[g(γ)]; "average, then convert to dB" computes g(E[γ]); they are not equal. The question asks for the mean SNR expressed in dB, which is the second one.</p>
<h4><span class="st">Step by step</span>(c) Convert to linear first, then use a table</h4>
<div class="tw"><table class="mini"><thead><tr><th>State</th><th>Probability p</th><th>SNR (dB)</th><th>Linear γ</th><th>γ·p</th><th>γ²·p</th></tr></thead><tbody>
<tr><td>Good</td><td>0.7</td><td>10 dB</td><td>10</td><td>7</td><td>70</td></tr>
<tr><td>Bad</td><td>0.3</td><td>0 dB</td><td>1</td><td>0.3</td><td>0.3</td></tr>
<tr><td>Total</td><td>1</td><td></td><td></td><td>7.3</td><td>70.3</td></tr>
</tbody></table></div>
<div class="calc">10 dB → 10^(10/10) = 10; 0 dB → 10⁰ = 1<br>E[γ] = 7 + 0.3 = 7.3<br>E[γ²] = 70 + 0.3 = 70.3<br>Var(γ) = 70.3 − 7.3² = 70.3 − 53.29 = 17.01; standard deviation = √17.01 = 4.12<br>mean SNR = 10 log₁₀7.3 = 10 × 0.8633 = 8.63 dB</div>
<p>Check (variance from the definition): 0.7 × (10 − 7.3)² + 0.3 × (1 − 7.3)² = 0.7 × 7.29 + 0.3 × 39.69 = 5.103 + 11.907 = 17.01, the same as above.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>(b) answered as 0.3: the a priori probability taken as the a posteriori one.</li>
<li>Only the bad-state term in the Bayes denominator, giving 1, which is clearly wrong; the denominator is the total from (a).</li>
<li>Averaging the dB values directly: 0.7 × 10 + 0.3 × 0 = 7 dB, i.e. 5.01 in linear scale, smaller than the correct 7.3. The lecturer said a missing dB ↔ linear conversion loses marks.</li>
<li>Forgetting to subtract (E[γ])² in the variance and writing 70.3; also do not convert the variance to dB, it has no meaning in dB and the question does not ask for it.</li>
<li>Misaligning the orders of magnitude when adding 10⁻⁴ and 10⁻² terms.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
<div class="tmpl" lang="en"><p>Let G and B denote the good and bad states and e a bit error: P(G) = 0.7, P(B) = 0.3, P(e | G) = 10⁻⁴, P(e | B) = 10⁻².</p><p>(a) By the total probability theorem, P<sub>e</sub> = P(G)P(e | G) + P(B)P(e | B) = 0.7 × 10⁻⁴ + 0.3 × 10⁻² = 3.07 × 10⁻³.</p><p>(b) By Bayes' rule, P(B | e) = P(B)P(e | B) / P<sub>e</sub> = (3 × 10⁻³) / (3.07 × 10⁻³) = 0.977.</p><p>(c) In linear scale the SNR is 10 (10 dB) with probability 0.7 and 1 (0 dB) with probability 0.3. E[γ] = 0.7 × 10 + 0.3 × 1 = 7.3, i.e. 10 log₁₀7.3 = 8.63 dB. E[γ²] = 0.7 × 100 + 0.3 × 1 = 70.3, so Var(γ) = 70.3 − 7.3² = 17.01. The dB values must not be averaged directly, because E[g(X)] ≠ g(E[X]).</p></div>
<div class="ans">In one line: first make a "state – probability – conditional probability" table; total probability is a weighted sum, Bayes is "one term ÷ the total"; convert dB to linear before taking the mean and variance.</div>'''},

# ------------------------------------------------------------------ p8q7
'p8q7': {
'title': '知识讲解 + 详细解析：阴影中断、宏分集与等效 dB 增益',
'title_en': 'Concept + step by step: shadowing outage, macro-diversity, gain in dB',
'zh': r'''<h4><span class="st">知识讲解</span>阴影中断为什么是 Q(余量/σ)</h4>
<p><b>阴影</b>（shadowing，大尺度衰落 large-scale fading）是楼房、树木等障碍物挡住信号，使接收功率在平均值附近随机起伏。讲义第 2 章 p.11–12：阴影 ψ<sub>dB</sub> 服从均值 0、标准差 σ 的高斯分布（所以叫对数正态 log-normal），接收功率 P<sub>r,dB</sub> = 不含阴影的平均功率 + ψ<sub>dB</sub>。</p>
<p><b>中断</b>（outage，p.14–15）= 接收功率低于门限 P<sub>min</sub>。把它整理成"随机变量 &lt; −x"的形式：P(ψ<sub>dB</sub> &lt; −x)，其中 x = 平均功率 − 门限，叫<b>余量</b>（margin）。高斯分布关于 0 对称，P(ψ &lt; −x) = P(ψ &gt; x) = Q(x/σ)。老师要求掌握这个整理技巧，第 3、6、7 章算误码率都用它；P<sub>out</sub> = Q(x/σ) 要背。</p>
<p><b>Q 函数</b>（Q-function）：Q(k) = 标准高斯随机变量大于 k 的概率，k 越大 Q 越小。查表时行看前两位（1.2），列看第三位（0.05），Q(1.25) = 0.1056。老师说 Q 表一定会考，正着查、倒着查都要会。</p>
<h4><span class="st">知识讲解</span>宏分集，以及"独立就相乘"</h4>
<p><b>分集</b>（diversity，第 4 章 p.2–3）：同一信号经过几条不同的信道送到，几条同时都很差的可能性很小。讲义 p.3：M 个独立分支时 P<sub>out,diversity</sub> = P<sub>out</sub><sup>M</sup>。<b>宏分集</b>（macroscopic diversity，p.4）用的是几个不同位置的基站，对付的是阴影：一个方向被大楼挡住时，另一个方向的基站不一定被挡。</p>
<p>为什么能相乘：第 1b 章 p.6，A、B 独立时 P(A ∩ B) = P(A)P(B)。"两条链路都低于门限"就是两个独立事件同时发生。</p>
<p>老师课上（Practice 4 第 1 题）说宏分集的解释题答两点就够：① 宏分集是什么（同一信息经不同基站 / 路径传送）；② 为什么能降低中断（所有路径同时中断的可能性很小）。</p>
<h4><span class="st">详细解析</span>(a) 单个基站</h4>
<div class="calc">余量 x = −95 − (−105) = 10 dB（dBm − dBm = dB）<br>x/σ = 10/8 = 1.25<br>P<sub>out,1</sub> = Q(1.25) = 0.1056 ≈ 10.6%</div>
<p>为什么除以 σ 而不是 σ²：Q 函数的参数是"离均值几个标准差"，标准差 σ = 8 dB 和余量单位相同；σ² = 64 dB² 单位都对不上。</p>
<h4><span class="st">详细解析</span>(b) 两个基站：独立，相乘</h4>
<div class="calc">P<sub>out,2</sub> = P(链路 1 中断) × P(链路 2 中断) = 0.1056 × 0.1056 ≈ 0.0112 = 1.12 × 10⁻²</div>
<p>要写出依据："两条链路的阴影独立，所以两者同时低于门限的概率等于各自概率的乘积"。老师说只写数字不说理由只给一半分。</p>
<h4><span class="st">详细解析</span>(c) 反查 Q 表：把"概率"换回"dB"</h4>
<ol>
<li>做什么：找单个基站需要的余量 m，使 Q(m/8) = 0.0112。为什么：(b) 的可靠性如果只靠一个基站得到，只能加大余量（加发射功率或缩短距离）；两种做法一比，就知道宏分集"值"多少 dB。</li>
<li>反查 Q 表：Q(2.28) = 0.0113，Q(2.29) = 0.0110，0.0112 夹在两者之间。线性插值得 x ≈ 2.28 + 0.01 × (0.0113 − 0.0112)/(0.0113 − 0.0110) ≈ 2.283；用不舍入的概率精确算是 2.2848。本题解答取 2.29，取 2.28 或 2.29 都可以，结果都约 18.3 dB。</li>
<li>换回 dB：<div class="calc">所需余量 = x σ ≈ 2.285 × 8 = 18.3 dB（取 2.28：18.24 dB；取 2.29：18.32 dB）<br>宏分集增益 = 18.3 − 10 = 8.3 dB</div></li>
</ol>
<p>含义：一点发射功率都不加，靠两个基站就相当于余量从 10 dB 提高到约 18.3 dB。</p>
<h4><span class="st">检查</span>合不合理、还能怎么问</h4>
<ul>
<li>(b) 的概率比 (a) 小 → 需要的余量比 10 dB 大 → 增益为正，方向对。</li>
<li>极端情况：两条链路完全相关（总是一起被挡），P<sub>out</sub> 还是 0.106，增益 0 dB；完全独立是最理想的情况。P2 Q2 (c) 是部分相关（有共同阴影）的版本。</li>
<li>三个独立基站：P<sub>out</sub> = 0.1056³ ≈ 1.18 × 10⁻³，反查 x ≈ 3.04，相当于余量 24.3 dB，增益 14.3 dB。第二个基站带来 8.3 dB，第三个只再加约 6.0 dB，越加越少。</li>
</ul>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>理解成"任意一个低于门限就中断"：1 − (1 − 0.106)² = 0.200，反而比单基站更差，方向就错了。</li>
<li>用方差除：10/64，Q 的参数不对。</li>
<li>反查时用了 (a) 的 0.106，而不是 (b) 的 0.0112。</li>
<li>把 18.3 dB 当成增益：18.3 dB 是单基站所需的余量，增益要减去已有的 10 dB。</li>
<li>没写"独立"这个前提就直接相乘。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(a) The margin is x = −95 − (−105) = 10 dB. Since ψ<sub>dB</sub> ~ N(0, σ²) with σ = 8 dB, P<sub>out</sub> = P(ψ<sub>dB</sub> &lt; −x) = Q(x/σ) = Q(1.25) = 0.106.</p><p>(b) The shadowing on the two links is independent, so the probability that both received powers are below −105 dBm is the product: P<sub>out</sub> = Q(1.25)² = 0.106² ≈ 1.12 × 10⁻².</p><p>(c) A single base station needs Q(m/σ) = 0.0112. From the Q table, m/σ ≈ 2.29, so m ≈ 2.29 × 8 ≈ 18.3 dB. The actual margin is 10 dB, so the macro-diversity gain is about 18.3 − 10 ≈ 8.3 dB: two independent base stations give the same reliability as about 8.3 dB of extra margin, without extra transmit power.</p></div>
<div class="ans">一句话：单基站 Q(10/8) = 0.106；两个独立基站相乘得 0.0112；反查 Q 表，单基站要约 18.3 dB 余量才能做到，所以宏分集等效增益约 8.3 dB。</div>''',
'en': r'''<h4><span class="st">Concept</span>Why shadowing outage is Q(margin/σ)</h4>
<p><b>Shadowing</b> (large-scale fading) is caused by obstacles such as buildings and trees blocking the signal, so the received power fluctuates randomly around its average. Ch 2 p.11–12: the shadowing ψ<sub>dB</sub> is Gaussian with mean 0 and standard deviation σ (hence log-normal), and the received power is P<sub>r,dB</sub> = average power without shadowing + ψ<sub>dB</sub>.</p>
<p><b>Outage</b> (p.14–15) = received power below the threshold P<sub>min</sub>. Rearrange it into the form "random variable &lt; −x": P(ψ<sub>dB</sub> &lt; −x), where x = average power − threshold is the <b>margin</b>. The Gaussian is symmetric about 0, so P(ψ &lt; −x) = P(ψ &gt; x) = Q(x/σ). The lecturer wants you to master this rearrangement, since Ch 3, 6 and 7 use it for every error probability; memorise P<sub>out</sub> = Q(x/σ).</p>
<p>The <b>Q-function</b>: Q(k) = the probability that a standard Gaussian random variable exceeds k; the larger k, the smaller Q. In the table, the row gives the first two digits (1.2) and the column the third (0.05): Q(1.25) = 0.1056. The lecturer said the Q table will definitely be tested, both forward and inverse lookup.</p>
<h4><span class="st">Concept</span>Macro-diversity, and "independent means multiply"</h4>
<p><b>Diversity</b> (Ch 4 p.2–3): the same signal arrives over several different channels, and it is unlikely that all of them are bad at the same time. Slide p.3: with M independent branches, P<sub>out,diversity</sub> = P<sub>out</sub><sup>M</sup>. <b>Macroscopic diversity</b> (p.4) uses several base stations at different locations and fights shadowing: when one direction is blocked by a building, the base station in another direction is not necessarily blocked.</p>
<p>Why we may multiply: Ch 1b p.6, if A and B are independent then P(A ∩ B) = P(A)P(B). "Both links below the threshold" is two independent events happening together.</p>
<p>The lecturer said in class (Practice 4 Q1) that a macro-diversity explanation needs only two points: ① what macro-diversity is (the same information sent via different base stations / paths); ② why it reduces outage (it is very unlikely that all paths are in outage at the same time).</p>
<h4><span class="st">Step by step</span>(a) One base station</h4>
<div class="calc">margin x = −95 − (−105) = 10 dB (dBm − dBm = dB)<br>x/σ = 10/8 = 1.25<br>P<sub>out,1</sub> = Q(1.25) = 0.1056 ≈ 10.6%</div>
<p>Why divide by σ and not σ²: the argument of Q is "how many standard deviations from the mean"; σ = 8 dB has the same unit as the margin, whereas σ² = 64 dB² does not even match in unit.</p>
<h4><span class="st">Step by step</span>(b) Two base stations: independent, so multiply</h4>
<div class="calc">P<sub>out,2</sub> = P(link 1 in outage) × P(link 2 in outage) = 0.1056 × 0.1056 ≈ 0.0112 = 1.12 × 10⁻²</div>
<p>Write the reason: "the shadowing on the two links is independent, so the probability that both are below the threshold is the product of the individual probabilities". The lecturer said a number without a reason gets only half the marks.</p>
<h4><span class="st">Step by step</span>(c) Inverse Q lookup: turn the probability back into dB</h4>
<ol>
<li>What: find the margin m a single base station needs so that Q(m/8) = 0.0112. Why: if the reliability of (b) had to come from one base station, the only way is a larger margin (more transmit power or a shorter distance); comparing the two approaches tells us how many dB macro-diversity is "worth".</li>
<li>Inverse lookup: Q(2.28) = 0.0113 and Q(2.29) = 0.0110, and 0.0112 lies between them. Linear interpolation gives x ≈ 2.28 + 0.01 × (0.0113 − 0.0112)/(0.0113 − 0.0110) ≈ 2.283; with the unrounded probability the exact value is 2.2848. The solution above uses 2.29; either 2.28 or 2.29 is fine, both give about 18.3 dB.</li>
<li>Back to dB: <div class="calc">required margin = x σ ≈ 2.285 × 8 = 18.3 dB (with 2.28: 18.24 dB; with 2.29: 18.32 dB)<br>macro-diversity gain = 18.3 − 10 = 8.3 dB</div></li>
</ol>
<p>Meaning: without adding any transmit power, two base stations act like raising the margin from 10 dB to about 18.3 dB.</p>
<h4><span class="st">Check</span>Does it make sense, and other ways to ask</h4>
<ul>
<li>The probability in (b) is smaller than in (a) → the required margin is larger than 10 dB → the gain is positive: right direction.</li>
<li>Extreme case: fully correlated links (always blocked together) still give P<sub>out</sub> = 0.106 and a gain of 0 dB; fully independent links are the best case. P2 Q2 (c) is the partly correlated (common shadowing) version.</li>
<li>Three independent base stations: P<sub>out</sub> = 0.1056³ ≈ 1.18 × 10⁻³, inverse lookup x ≈ 3.04, i.e. a margin of 24.3 dB and a gain of 14.3 dB. The second base station brings 8.3 dB, the third only about 6.0 dB more: diminishing returns.</li>
</ul>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Reading it as "outage if either link is below the threshold": 1 − (1 − 0.106)² = 0.200, worse than one base station, so the direction is wrong.</li>
<li>Dividing by the variance: 10/64 is the wrong Q argument.</li>
<li>Using 0.106 from (a) in the inverse lookup instead of 0.0112 from (b).</li>
<li>Calling 18.3 dB the gain: 18.3 dB is the margin a single base station needs; the gain subtracts the existing 10 dB.</li>
<li>Multiplying without stating the assumption of independence.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
<div class="tmpl" lang="en"><p>(a) The margin is x = −95 − (−105) = 10 dB. Since ψ<sub>dB</sub> ~ N(0, σ²) with σ = 8 dB, P<sub>out</sub> = P(ψ<sub>dB</sub> &lt; −x) = Q(x/σ) = Q(1.25) = 0.106.</p><p>(b) The shadowing on the two links is independent, so the probability that both received powers are below −105 dBm is the product: P<sub>out</sub> = Q(1.25)² = 0.106² ≈ 1.12 × 10⁻².</p><p>(c) A single base station needs Q(m/σ) = 0.0112. From the Q table, m/σ ≈ 2.29, so m ≈ 2.29 × 8 ≈ 18.3 dB. The actual margin is 10 dB, so the macro-diversity gain is about 18.3 − 10 ≈ 8.3 dB: two independent base stations give the same reliability as about 8.3 dB of extra margin, without extra transmit power.</p></div>
<div class="ans">In one line: one base station gives Q(10/8) = 0.106; two independent base stations multiply to 0.0112; the inverse Q lookup shows one base station would need about 18.3 dB of margin, so the macro-diversity gain is about 8.3 dB.</div>'''},

# ------------------------------------------------------------------ p8q8
'p8q8': {
'title': '知识讲解 + 详细解析：衰落类型两个维度、LCR 与 AFD',
'title_en': 'Concept + step by step: the two fading dimensions, LCR and AFD',
'zh': r'''<h4><span class="st">知识讲解</span>衰落类型：两个维度，各比一次</h4>
<p>小尺度衰落要从两个互不相关的方向判断（讲义第 2 章 p.31–39），老师说"问衰落类型只答一个维度只给一半分"：</p>
<div class="tw"><table class="mini"><thead><tr><th>维度</th><th>比较什么</th><th>平坦 / 慢</th><th>频率选择性 / 快</th><th>讲义</th></tr></thead><tbody>
<tr><td>频率维（由时延扩展引起，时间色散）</td><td>信号带宽 B<sub>s</sub> 和相干带宽 B<sub>C</sub>（等价：σ<sub>τ</sub> 和 T<sub>s</sub>）</td><td>B<sub>s</sub> &lt; B<sub>C</sub> → 平坦衰落（flat）</td><td>B<sub>s</sub> &gt; B<sub>C</sub> → 频率选择性衰落（frequency-selective），有 ISI</td><td>p.31–33</td></tr>
<tr><td>时间维（由多普勒扩展引起，频率色散）</td><td>多普勒扩展 B<sub>D</sub> 和 B<sub>s</sub>（等价：相干时间 T<sub>C</sub> 和 T<sub>s</sub>）</td><td>B<sub>D</sub> ≪ B<sub>s</sub>（T<sub>s</sub> ≪ T<sub>C</sub>）→ 慢衰落（slow）</td><td>B<sub>D</sub> 接近或大于 B<sub>s</sub> → 快衰落（fast）</td><td>p.35–37</td></tr>
</tbody></table></div>
<p>符号含义：<b>相干带宽</b>（coherence bandwidth）B<sub>C</sub> 是"两个频率相差多远，衰落就不再相关"（p.31）；<b>多普勒扩展</b>（Doppler spread）B<sub>D</sub> = f<sub>m</sub>，f<sub>m</sub> = v f<sub>c</sub>/c 是最大多普勒频移（p.34–35）；<b>相干时间</b>（coherence time）T<sub>C</sub> ≈ 1/f<sub>m</sub>，是信道"基本不变"的时长（p.36）。</p>
<p>为什么这样判断：B<sub>s</sub> &lt; B<sub>C</sub> 时，整个信号带宽里的衰落几乎一样，信道只是把整个信号乘上一个复数，不变形；T<sub>s</sub> ≪ T<sub>C</sub> 时，一个符号期间信道几乎不变，幅度和相位可以看成常数（p.37）。</p>
<h4><span class="st">详细解析</span>(a) 套到本题</h4>
<div class="calc">频率维：B<sub>s</sub> ≈ 50 kHz &lt; B<sub>C</sub> = 200 kHz（B<sub>C</sub>/B<sub>s</sub> = 4）→ 平坦<br>时间维：B<sub>D</sub> = f<sub>m</sub> = 100 Hz，B<sub>s</sub>/B<sub>D</sub> = 50 kHz / 100 Hz = 500 → B<sub>D</sub> ≪ B<sub>s</sub> → 慢<br>等价写法：T<sub>C</sub> ≈ 1/f<sub>m</sub> = 1/100 = 10 ms，T<sub>s</sub> = 1/50000 = 20 µs，T<sub>C</sub>/T<sub>s</sub> = 500</div>
<p>结论：<b>平坦慢衰落</b>（flat, slow fading）。两个维度各写一句比较和结论，不要把 B<sub>D</sub> 和 B<sub>C</sub> 拿来比（那是两个维度混在一起了）。</p>
<h4><span class="st">知识讲解</span>LCR 和 AFD 按定义算（不需要瑞利）</h4>
<p><b>电平通过率</b>（level crossing rate，LCR，p.40）：信号强度每秒<b>向下</b>穿过门限 Z<sub>min</sub> 的平均次数，也就是"每秒掉进深衰落几次"。<b>平均衰落时长</b>（average fade duration，AFD，p.42）：每次掉下去以后在门限下面待的平均时间 = 各次衰落时长之和 ÷ 衰落次数。</p>
<p>p.43 把两者联系起来：AFD = P(z &lt; Z<sub>min</sub>) / L<sub>Z</sub>，即 <b>L<sub>Z</sub> × AFD = 信号低于门限的时间比例</b>。直观理解：每秒掉下去 30 次，每次 0.5 ms，每秒就有 15 ms 在深衰落里。</p>
<p>老师课上强调（今年 Quiz 第 2 题的常见错误）：题目没说是瑞利衰落时，LCR、AFD 要<b>按定义</b>算（他比作"算平均价格"）；含 f<sub>m</sub>、ρ 的那两个公式只适用于瑞利衰落。本题 (b) 就是按定义算，(c) 才假设瑞利。</p>
<h4><span class="st">详细解析</span>(b) 每一步做什么、为什么</h4>
<ol>
<li>LCR：次数除以观测时间，因为 LCR 的单位是"次/秒"。<div class="calc">LCR = 300 次 ÷ 10 s = 30 次/s</div></li>
<li>时间比例：LCR × AFD（每秒几次 × 每次多久 = 每秒有多少时间在深衰落里）。AFD 先换成秒。<div class="calc">时间比例 = 30 × 0.5 × 10⁻³ = 0.015 = 1.5%</div></li>
<li>每次衰落错几个符号：AFD 除以符号时长（老师说给的是符号速率时就乘 R<sub>s</sub>）。<div class="calc">T<sub>s</sub> = 1/R<sub>s</sub> = 1/50000 = 20 µs<br>每次衰落的符号数 = 0.5 ms / 20 µs = 0.5 × 10⁻³ × 50000 = 25</div></li>
<li>每秒错误符号数：每秒衰落次数 × 每次错的个数。<div class="calc">每秒错误符号数 = 30 × 25 = 750<br>另一条路：1.5% × 50000 = 750（一致）<br>符号错误率 SER = 750 / 50000 = 1.5 × 10⁻²</div></li>
</ol>
<p>讲义 p.45–47 的例题是同一个套路（AFD × R<sub>s</sub> 得每次错的个数，再乘 LCR）。</p>
<h4><span class="st">详细解析</span>(c) 两个瑞利公式相乘，f<sub>m</sub> 消掉</h4>
<p>ρ = Z<sub>min</sub>/Z<sub>rms</sub> 是门限幅度和 rms 幅度之比（老师说解释 ρ 时一定要提到 Z<sub>min</sub> 和 Z<sub>rms</sub>），ρ² 才是功率比。做法：\(L_Z\bar\tau_Z=\sqrt{2\pi}f_m\rho e^{-\rho^2}\cdot\dfrac{e^{\rho^2}-1}{\sqrt{2\pi}f_m\rho}=1-e^{-\rho^2}\)。为什么可以这样：由 p.43，L<sub>Z</sub> τ̄<sub>Z</sub> 就是 P(z &lt; Z<sub>min</sub>)，而瑞利衰落下这个概率是 1 − e<sup>−ρ²</sup>（就是瑞利中断公式 1 − e<sup>−γ₀/γ̄</sup>，ρ² = γ₀/γ̄）。</p>
<div class="calc">1 − e<sup>−ρ²</sup> = 0.015 → e<sup>−ρ²</sup> = 0.985 → ρ² = ln(1/0.985) = 0.01511<br>门限比 rms 功率：10 log₁₀(0.01511) = −18.2 dB<br>ρ = √0.01511 = 0.123（幅度比；20 log₁₀0.123 = −18.2 dB，同一个答案）</div>
<p>计算器提示：ln 是自然对数键（ln），不是 log。ρ² 很小时 1 − e<sup>−ρ²</sup> ≈ ρ²，所以 ρ² ≈ 0.015，10 log₁₀0.015 = −18.24 dB，可以用来快速估算。</p>
<p>检验：把 ρ 代回 LCR 公式反推 f<sub>m</sub> = 30 / (√(2π) × 0.123 × e<sup>−0.0151</sup>) ≈ 98.8 Hz，和题目给的 100 Hz 吻合，说明这组数据确实像瑞利衰落。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>衰落类型只答"平坦"或只答"慢"：只给一半分。</li>
<li>LCR 写成 300：忘了除以 10 秒。</li>
<li>AFD 没换成秒：30 × 0.5 = 15，"时间比例"大于 1，明显不对。</li>
<li>(b) 去套瑞利公式：题目给了观测数据，按定义算就行。</li>
<li>(c) 把 ρ 当功率比：10 log₁₀0.123 = −9.1 dB 是错的；功率比用 ρ²，或者用 20 log₁₀ρ。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(a) Frequency dimension: the signal bandwidth B<sub>s</sub> ≈ 50 kHz is smaller than the coherence bandwidth B<sub>C</sub> = 200 kHz, so all frequency components fade together: flat fading. Time dimension: the Doppler spread B<sub>D</sub> = f<sub>m</sub> = 100 Hz ≪ B<sub>s</sub>; equivalently the coherence time T<sub>C</sub> ≈ 1/f<sub>m</sub> = 10 ms ≫ T<sub>s</sub> = 20 µs, so the channel is constant over a symbol: slow fading. The system experiences flat, slow fading.</p><p>(b) LCR = 300/10 = 30 fades per second. Fraction of time in deep fades = LCR × AFD = 30 × 0.5 ms = 0.015 (1.5%). Each fade covers AFD/T<sub>s</sub> = 0.5 ms / 20 µs = 25 symbols, so there are 30 × 25 = 750 symbol errors per second.</p><p>(c) Multiplying the two formulas, L<sub>Z</sub> τ̄<sub>Z</sub> = 1 − e<sup>−ρ²</sup> = 0.015, so ρ² = ln(1/0.985) = 0.0151, where ρ = Z<sub>min</sub>/Z<sub>rms</sub>. In dB, 10 log₁₀(0.0151) = −18.2 dB: the threshold is about 18.2 dB below the rms power.</p></div>
<div class="ans">一句话：衰落类型两个维度各比一次（B<sub>s</sub> 对 B<sub>C</sub>，B<sub>D</sub> 对 B<sub>s</sub>）；LCR = 次数 ÷ 时间，LCR × AFD = 时间比例；瑞利下 1 − e<sup>−ρ²</sup> = 时间比例，解出 ρ² 再取 10 log₁₀。</div>''',
'en': r'''<h4><span class="st">Concept</span>Fading type: two dimensions, one comparison each</h4>
<p>Small-scale fading is classified along two independent directions (Ch 2 p.31–39). The lecturer said that answering only one dimension when asked for the fading type gets only half the marks:</p>
<div class="tw"><table class="mini"><thead><tr><th>Dimension</th><th>What to compare</th><th>Flat / slow</th><th>Frequency-selective / fast</th><th>Slides</th></tr></thead><tbody>
<tr><td>Frequency (caused by delay spread, time dispersion)</td><td>signal bandwidth B<sub>s</sub> vs coherence bandwidth B<sub>C</sub> (equivalently σ<sub>τ</sub> vs T<sub>s</sub>)</td><td>B<sub>s</sub> &lt; B<sub>C</sub> → flat fading</td><td>B<sub>s</sub> &gt; B<sub>C</sub> → frequency-selective fading, with ISI</td><td>p.31–33</td></tr>
<tr><td>Time (caused by Doppler spread, frequency dispersion)</td><td>Doppler spread B<sub>D</sub> vs B<sub>s</sub> (equivalently coherence time T<sub>C</sub> vs T<sub>s</sub>)</td><td>B<sub>D</sub> ≪ B<sub>s</sub> (T<sub>s</sub> ≪ T<sub>C</sub>) → slow fading</td><td>B<sub>D</sub> close to or above B<sub>s</sub> → fast fading</td><td>p.35–37</td></tr>
</tbody></table></div>
<p>Symbols: the <b>coherence bandwidth</b> B<sub>C</sub> is "how far apart two frequencies must be before their fading is no longer correlated" (p.31); the <b>Doppler spread</b> B<sub>D</sub> = f<sub>m</sub>, where f<sub>m</sub> = v f<sub>c</sub>/c is the maximum Doppler shift (p.34–35); the <b>coherence time</b> T<sub>C</sub> ≈ 1/f<sub>m</sub> is how long the channel stays essentially unchanged (p.36).</p>
<p>Why these rules: when B<sub>s</sub> &lt; B<sub>C</sub>, the fading is almost the same across the whole signal bandwidth, so the channel just multiplies the whole signal by one complex number without distorting it; when T<sub>s</sub> ≪ T<sub>C</sub>, the channel hardly changes during a symbol, so amplitude and phase can be treated as constant (p.37).</p>
<h4><span class="st">Step by step</span>(a) Applying it here</h4>
<div class="calc">Frequency: B<sub>s</sub> ≈ 50 kHz &lt; B<sub>C</sub> = 200 kHz (B<sub>C</sub>/B<sub>s</sub> = 4) → flat<br>Time: B<sub>D</sub> = f<sub>m</sub> = 100 Hz, B<sub>s</sub>/B<sub>D</sub> = 50 kHz / 100 Hz = 500 → B<sub>D</sub> ≪ B<sub>s</sub> → slow<br>Equivalently: T<sub>C</sub> ≈ 1/f<sub>m</sub> = 1/100 = 10 ms, T<sub>s</sub> = 1/50000 = 20 µs, T<sub>C</sub>/T<sub>s</sub> = 500</div>
<p>Conclusion: <b>flat, slow fading</b>. Write one comparison and one conclusion for each dimension; do not compare B<sub>D</sub> with B<sub>C</sub> (that mixes the two dimensions).</p>
<h4><span class="st">Concept</span>LCR and AFD from their definitions (no Rayleigh needed)</h4>
<p>The <b>level crossing rate</b> (LCR, p.40) is the average number of times per second the signal strength crosses <b>downwards</b> through the threshold Z<sub>min</sub>, i.e. "how many deep fades per second". The <b>average fade duration</b> (AFD, p.42) is the average time spent below the threshold per fade = sum of the fade durations ÷ number of fades.</p>
<p>Slide p.43 links the two: AFD = P(z &lt; Z<sub>min</sub>) / L<sub>Z</sub>, i.e. <b>L<sub>Z</sub> × AFD = fraction of time below the threshold</b>. Intuition: 30 fades per second, 0.5 ms each, means 15 ms of every second is spent in deep fades.</p>
<p>The lecturer stressed in class (a common mistake in this year's Quiz Q2): if the question does not say Rayleigh fading, compute LCR and AFD <b>from the definitions</b> (he compared it to "computing an average price"); the two formulas with f<sub>m</sub> and ρ apply only to Rayleigh fading. Part (b) here uses the definitions; only (c) assumes Rayleigh.</p>
<h4><span class="st">Step by step</span>(b) What each step does and why</h4>
<ol>
<li>LCR: count divided by observation time, because LCR is in "per second". <div class="calc">LCR = 300 fades ÷ 10 s = 30 per second</div></li>
<li>Fraction of time: LCR × AFD (fades per second × duration of each = time per second spent in deep fades). Convert the AFD to seconds first. <div class="calc">fraction of time = 30 × 0.5 × 10⁻³ = 0.015 = 1.5%</div></li>
<li>Symbols lost per fade: AFD divided by the symbol duration (the lecturer said: when the symbol rate is given, multiply by R<sub>s</sub>). <div class="calc">T<sub>s</sub> = 1/R<sub>s</sub> = 1/50000 = 20 µs<br>symbols per fade = 0.5 ms / 20 µs = 0.5 × 10⁻³ × 50000 = 25</div></li>
<li>Symbol errors per second: fades per second × errors per fade. <div class="calc">symbol errors per second = 30 × 25 = 750<br>Other route: 1.5% × 50000 = 750 (same)<br>symbol error rate SER = 750 / 50000 = 1.5 × 10⁻²</div></li>
</ol>
<p>The example on slides p.45–47 follows the same recipe (AFD × R<sub>s</sub> gives the errors per fade, then multiply by the LCR).</p>
<h4><span class="st">Step by step</span>(c) Multiply the two Rayleigh formulas: f<sub>m</sub> cancels</h4>
<p>ρ = Z<sub>min</sub>/Z<sub>rms</sub> is the ratio of the threshold amplitude to the rms amplitude (the lecturer said that when explaining ρ you must mention Z<sub>min</sub> and Z<sub>rms</sub>); ρ² is the power ratio. Method: \(L_Z\bar\tau_Z=\sqrt{2\pi}f_m\rho e^{-\rho^2}\cdot\dfrac{e^{\rho^2}-1}{\sqrt{2\pi}f_m\rho}=1-e^{-\rho^2}\). Why this works: by p.43, L<sub>Z</sub> τ̄<sub>Z</sub> is P(z &lt; Z<sub>min</sub>), and for Rayleigh fading this probability is 1 − e<sup>−ρ²</sup> (the Rayleigh outage formula 1 − e<sup>−γ₀/γ̄</sup> with ρ² = γ₀/γ̄).</p>
<div class="calc">1 − e<sup>−ρ²</sup> = 0.015 → e<sup>−ρ²</sup> = 0.985 → ρ² = ln(1/0.985) = 0.01511<br>threshold relative to rms power: 10 log₁₀(0.01511) = −18.2 dB<br>ρ = √0.01511 = 0.123 (amplitude ratio; 20 log₁₀0.123 = −18.2 dB, the same answer)</div>
<p>Calculator hint: use the natural-log key (ln), not log. For small ρ², 1 − e<sup>−ρ²</sup> ≈ ρ², so ρ² ≈ 0.015 and 10 log₁₀0.015 = −18.24 dB, a quick estimate.</p>
<p>Check: putting ρ back into the LCR formula gives f<sub>m</sub> = 30 / (√(2π) × 0.123 × e<sup>−0.0151</sup>) ≈ 98.8 Hz, matching the 100 Hz given, so the data do look like Rayleigh fading.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Answering only "flat" or only "slow": half marks.</li>
<li>LCR written as 300: forgot to divide by 10 seconds.</li>
<li>AFD not converted to seconds: 30 × 0.5 = 15, a "fraction of time" above 1, clearly wrong.</li>
<li>Using the Rayleigh formulas in (b): the question gives observed data, so the definitions are enough.</li>
<li>Treating ρ as a power ratio in (c): 10 log₁₀0.123 = −9.1 dB is wrong; for power use ρ², or 20 log₁₀ρ.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
<div class="tmpl" lang="en"><p>(a) Frequency dimension: the signal bandwidth B<sub>s</sub> ≈ 50 kHz is smaller than the coherence bandwidth B<sub>C</sub> = 200 kHz, so all frequency components fade together: flat fading. Time dimension: the Doppler spread B<sub>D</sub> = f<sub>m</sub> = 100 Hz ≪ B<sub>s</sub>; equivalently the coherence time T<sub>C</sub> ≈ 1/f<sub>m</sub> = 10 ms ≫ T<sub>s</sub> = 20 µs, so the channel is constant over a symbol: slow fading. The system experiences flat, slow fading.</p><p>(b) LCR = 300/10 = 30 fades per second. Fraction of time in deep fades = LCR × AFD = 30 × 0.5 ms = 0.015 (1.5%). Each fade covers AFD/T<sub>s</sub> = 0.5 ms / 20 µs = 25 symbols, so there are 30 × 25 = 750 symbol errors per second.</p><p>(c) Multiplying the two formulas, L<sub>Z</sub> τ̄<sub>Z</sub> = 1 − e<sup>−ρ²</sup> = 0.015, so ρ² = ln(1/0.985) = 0.0151, where ρ = Z<sub>min</sub>/Z<sub>rms</sub>. In dB, 10 log₁₀(0.0151) = −18.2 dB: the threshold is about 18.2 dB below the rms power.</p></div>
<div class="ans">In one line: compare once in each dimension (B<sub>s</sub> vs B<sub>C</sub>, B<sub>D</sub> vs B<sub>s</sub>); LCR = count ÷ time, LCR × AFD = fraction of time; for Rayleigh, 1 − e<sup>−ρ²</sup> = that fraction, so solve for ρ² and take 10 log₁₀.</div>'''},

# ------------------------------------------------------------------ p8q9
'p8q9': {
'title': '知识讲解 + 详细解析：SINR、香农容量与瑞利中断容量',
'title_en': 'Concept + step by step: SINR, Shannon capacity, Rayleigh outage capacity',
'zh': r'''<h4><span class="st">知识讲解</span>SNR、SIR、SINR：只差在分母</h4>
<p>三个比值的分子都是有用信号功率 S，分母不同：</p>
<div class="tw"><table class="mini"><thead><tr><th>名称</th><th>定义</th><th>分母里有什么</th><th>什么时候用</th></tr></thead><tbody>
<tr><td>SNR（signal-to-noise ratio）</td><td>S/N</td><td>只有噪声</td><td>没有干扰，或干扰已被消除</td></tr>
<tr><td>SIR（signal-to-interference ratio）</td><td>S/I</td><td>只有干扰</td><td>蜂窝规划，噪声可忽略时</td></tr>
<tr><td>SINR（signal-to-interference-plus-noise ratio）</td><td>S/(I + N)</td><td>干扰 + 噪声</td><td>两者都有，把干扰当噪声处理时</td></tr>
</tbody></table></div>
<p>SINR 的定义在讲义第 1a 章 p.16（"Interference: Friend or Foe?"）：干扰当噪声处理时是"敌人"，就用 SINR。第 1a 章老师说不考，但这个定义 Practice 2 第 3 题要用。一个好用的关系：1/SINR = 1/SNR + 1/SIR，所以 SINR 一定比 SNR 和 SIR 都小。</p>
<h4><span class="st">知识讲解</span>香农容量</h4>
<p>讲义第 2 章 p.48：AWGN 信道的容量 C = B log₂(1 + γ)（bit/s），γ 是接收 SNR（<b>线性值</b>），B 是带宽。意义：传输速率 R &lt; C 时，存在编码能让误码率任意小；R &gt; C 时做不到。老师说这是通信工程师最基本的公式，必须背。干扰被当成高斯噪声时，它和噪声没有区别，γ 就换成 SINR。</p>
<p>计算器提示：log₂x = log₁₀x / 0.301；dB → 线性：10^(dB/10)。B 用 MHz 代入，C 的单位就是 Mbps。</p>
<h4><span class="st">详细解析</span>(a) 三个比值和容量</h4>
<div class="calc">SNR = 2 / 0.05 = 40 → 10 log₁₀40 = 16.0 dB<br>SIR = 2 / 0.5 = 4 → 10 log₁₀4 = 6.0 dB<br>SINR = 2 / (0.5 + 0.05) = 2 / 0.55 = 3.64 → 10 log₁₀3.64 = 5.6 dB<br>检验：1/40 + 1/4 = 0.025 + 0.25 = 0.275 = 1/3.64<br>C = 10 MHz × log₂(1 + 3.64) = 10 × (log₁₀4.64 / 0.301) = 10 × 2.213 = 22.1 Mbps</div>
<p>为什么用 SINR：题目说"把干扰当高斯噪声"，那接收机看到的"噪声"就是 I + N。功率都是 mW，相除后单位消掉，不用换成 W。</p>
<h4><span class="st">详细解析</span>(b) 干扰完全消除</h4>
<div class="calc">只剩噪声，用 SNR = 40：C = 10 × log₂41 = 10 × 5.358 = 53.6 Mbps<br>53.6 / 22.1 ≈ 2.4 倍</div>
<p>为什么提升这么大：干扰 0.5 mW 是噪声 0.05 mW 的 10 倍，SINR ≈ SIR，这种系统叫<b>干扰受限</b>（interference-limited）。对比一下：噪声减半，SINR = 2/0.525，C 只到 22.7 Mbps；干扰减半，SINR = 2/0.3，C 升到 29.4 Mbps。要提升容量，就要对付干扰（干扰消除、多用户检测 MUD、扇区化等）。</p>
<h4><span class="st">知识讲解</span>衰落信道：遍历容量和中断容量</h4>
<p>衰落信道里 SNR γ 是随机变量（老师强调这一点贯穿第 2–7 章）。讲义给了两种容量：</p>
<ul>
<li><b>遍历容量</b>（ergodic capacity，p.49）：对 B log₂(1 + γ) 求平均。由 Jensen 不等式，它不会超过同样平均 SNR 的 AWGN 容量（老师说 Jensen 只要求懂概念）。</li>
<li><b>中断容量</b>（outage capacity，p.50，适用于慢衰落）：允许 ε 的时间中断，其余时间保证速率 C<sub>ε</sub> = B log₂(1 + γ<sub>min</sub>)，γ<sub>min</sub> 满足 P(γ &lt; γ<sub>min</sub>) = ε。</li>
</ul>
<p>瑞利衰落时 P(γ &lt; γ<sub>min</sub>) = 1 − e<sup>−γ<sub>min</sub>/γ̄</sup>（必背的瑞利中断公式）。令它等于 ε，解出 γ<sub>min</sub> = γ̄ ln(1/(1 − ε))（p.51），代进香农公式就是题目给的 C<sub>ε</sub>。p.51 还说：和 AWGN 达到同样容量需要的衰落余量（fade margin）= 10 log₁₀[1/ln(1/(1 − ε))]，ε = 1% 时是 20 dB。</p>
<h4><span class="st">详细解析</span>(c) 一步一步代</h4>
<ol>
<li>dB 换线性：γ̄ = 10^(20/10) = 100。</li>
<li>求 γ<sub>min</sub>：ln 是自然对数。<div class="calc">ln(1/0.99) = 0.01005<br>γ<sub>min</sub> = 100 × 0.01005 = 1.005（约 0.02 dB，也就是约 0 dB）</div></li>
<li>代香农：<div class="calc">C<sub>ε</sub> = 10 × log₂(1 + 1.005) = 10 × log₂2.005 = 10 × 1.004 = 10.0 Mbps</div></li>
<li>和 AWGN 比：<div class="calc">C<sub>AWGN</sub> = 10 × log₂(1 + 100) = 10 × 6.658 = 66.6 Mbps<br>66.6 / 10.0 ≈ 6.6 倍<br>衰落余量 = 20 − 0.02 = 19.98 ≈ 20 dB</div></li>
</ol>
<p>为什么差这么多：要保证 99% 的时间都不中断，只能按"最差的 1%"附近的 SNR（约 0 dB）来定速率，比平均 SNR 低约 20 dB。ε 很小时 ln(1/(1 − ε)) ≈ ε，所以 γ<sub>min</sub> ≈ γ̄ ε：ε = 1% 就是低 20 dB。p.50 还给了"不出错的平均速率" (1 − ε)C<sub>ε</sub> = 0.99 × 10.04 = 9.94 Mbps。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>(a) 用 SNR 代香农：题目有干扰且当噪声处理，要用 SINR。</li>
<li>把 dB 值代进 log₂：log₂(1 + 5.6) 是错的，必须用线性值 3.64。</li>
<li>(c) 把 ln 按成 log₁₀：log₁₀(1/0.99) = 0.00436，会得到 γ<sub>min</sub> = 0.436、C = 5.2 Mbps，错。</li>
<li>γ̄ = 20 直接代入（没换成 100）。</li>
<li>只给数字不比较：(c) 要说明 C<sub>ε</sub> 远小于 AWGN 的原因（衰落余量约 20 dB）。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(a) SNR = S/N = 2/0.05 = 40 (16.0 dB); SIR = S/I = 2/0.5 = 4 (6.0 dB); SINR = S/(I + N) = 2/0.55 = 3.64 (5.6 dB). Treating the interference as Gaussian noise, C = B log₂(1 + SINR) = 10⁷ × log₂(4.64) = 22.1 Mbps.</p><p>(b) With the interference removed, C = B log₂(1 + SNR) = 10⁷ × log₂(41) = 53.6 Mbps, about 2.4 times larger, because the link is interference-limited.</p><p>(c) γ̄ = 20 dB = 100. For Rayleigh fading, γ<sub>min</sub> = γ̄ ln(1/(1 − ε)) = 100 × ln(1/0.99) = 1.005, so C<sub>ε</sub> = 10⁷ × log₂(2.005) = 10.0 Mbps. An AWGN channel with SNR 20 dB gives C = 10⁷ × log₂(101) = 66.6 Mbps. The outage capacity is much lower because, to avoid outage 99% of the time, the rate must be set by an SNR about 20 dB below the average (the fade margin).</p></div>
<div class="ans">一句话：干扰当噪声就用 SINR = S/(I + N) 代香农；去掉干扰改用 SNR；瑞利中断容量先算 γ<sub>min</sub> = γ̄ ln(1/(1 − ε))，ε = 1% 时比 γ̄ 低约 20 dB，所以容量远低于 AWGN。</div>''',
'en': r'''<h4><span class="st">Concept</span>SNR, SIR, SINR: only the denominator differs</h4>
<p>All three ratios have the useful signal power S on top; the denominators differ:</p>
<div class="tw"><table class="mini"><thead><tr><th>Name</th><th>Definition</th><th>What is in the denominator</th><th>When to use it</th></tr></thead><tbody>
<tr><td>SNR (signal-to-noise ratio)</td><td>S/N</td><td>noise only</td><td>no interference, or the interference has been cancelled</td></tr>
<tr><td>SIR (signal-to-interference ratio)</td><td>S/I</td><td>interference only</td><td>cellular planning, when noise is negligible</td></tr>
<tr><td>SINR (signal-to-interference-plus-noise ratio)</td><td>S/(I + N)</td><td>interference + noise</td><td>both present, interference treated as noise</td></tr>
</tbody></table></div>
<p>SINR is defined on Ch 1a p.16 ("Interference: Friend or Foe?"): when interference is treated as noise it is a "foe", and SINR is used. The lecturer said Ch 1a is not examined, but Practice 2 Q3 needs this definition. A handy relation: 1/SINR = 1/SNR + 1/SIR, so SINR is always smaller than both SNR and SIR.</p>
<h4><span class="st">Concept</span>Shannon capacity</h4>
<p>Ch 2 p.48: the capacity of an AWGN channel is C = B log₂(1 + γ) (bit/s), where γ is the received SNR (<b>linear value</b>) and B the bandwidth. Meaning: if the rate R &lt; C, codes exist that make the error probability arbitrarily small; if R &gt; C, this is impossible. The lecturer said this is the most basic formula of a communication engineer and must be memorised. When interference is treated as Gaussian noise it is no different from noise, so γ becomes the SINR.</p>
<p>Calculator hint: log₂x = log₁₀x / 0.301; dB → linear: 10^(dB/10). With B in MHz, C comes out in Mbps.</p>
<h4><span class="st">Step by step</span>(a) The three ratios and the capacity</h4>
<div class="calc">SNR = 2 / 0.05 = 40 → 10 log₁₀40 = 16.0 dB<br>SIR = 2 / 0.5 = 4 → 10 log₁₀4 = 6.0 dB<br>SINR = 2 / (0.5 + 0.05) = 2 / 0.55 = 3.64 → 10 log₁₀3.64 = 5.6 dB<br>Check: 1/40 + 1/4 = 0.025 + 0.25 = 0.275 = 1/3.64<br>C = 10 MHz × log₂(1 + 3.64) = 10 × (log₁₀4.64 / 0.301) = 10 × 2.213 = 22.1 Mbps</div>
<p>Why SINR: the question says "treat the interference as Gaussian noise", so the "noise" the receiver sees is I + N. All powers are in mW and the units cancel in the ratios, so there is no need to convert to W.</p>
<h4><span class="st">Step by step</span>(b) Interference completely removed</h4>
<div class="calc">Only noise is left, so use SNR = 40: C = 10 × log₂41 = 10 × 5.358 = 53.6 Mbps<br>53.6 / 22.1 ≈ 2.4 times</div>
<p>Why such a big jump: the interference (0.5 mW) is 10 times the noise (0.05 mW), so SINR ≈ SIR; such a system is <b>interference-limited</b>. Compare: halving the noise gives SINR = 2/0.525 and C only rises to 22.7 Mbps; halving the interference gives SINR = 2/0.3 and C rises to 29.4 Mbps. To raise the capacity, deal with the interference (interference cancellation, multi-user detection MUD, sectoring, etc.).</p>
<h4><span class="st">Concept</span>Fading channels: ergodic capacity and outage capacity</h4>
<p>In a fading channel the SNR γ is a random variable (the lecturer stressed that this runs through Ch 2–7). The slides give two capacities:</p>
<ul>
<li><b>Ergodic capacity</b> (p.49): the average of B log₂(1 + γ). By Jensen's inequality it cannot exceed the AWGN capacity with the same average SNR (the lecturer said only the concept of Jensen is required).</li>
<li><b>Outage capacity</b> (p.50, for slow fading): allow outage a fraction ε of the time and guarantee the rate C<sub>ε</sub> = B log₂(1 + γ<sub>min</sub>) the rest of the time, where P(γ &lt; γ<sub>min</sub>) = ε.</li>
</ul>
<p>For Rayleigh fading, P(γ &lt; γ<sub>min</sub>) = 1 − e<sup>−γ<sub>min</sub>/γ̄</sup> (the Rayleigh outage formula, memorise). Setting it equal to ε gives γ<sub>min</sub> = γ̄ ln(1/(1 − ε)) (p.51); substituting into Shannon gives the C<sub>ε</sub> in the question. Slide p.51 also says: the fade margin needed to reach the same capacity as AWGN is 10 log₁₀[1/ln(1/(1 − ε))], which is 20 dB for ε = 1%.</p>
<h4><span class="st">Step by step</span>(c) Substituting step by step</h4>
<ol>
<li>dB to linear: γ̄ = 10^(20/10) = 100.</li>
<li>Find γ<sub>min</sub>; ln is the natural logarithm. <div class="calc">ln(1/0.99) = 0.01005<br>γ<sub>min</sub> = 100 × 0.01005 = 1.005 (about 0.02 dB, i.e. about 0 dB)</div></li>
<li>Into Shannon: <div class="calc">C<sub>ε</sub> = 10 × log₂(1 + 1.005) = 10 × log₂2.005 = 10 × 1.004 = 10.0 Mbps</div></li>
<li>Compare with AWGN: <div class="calc">C<sub>AWGN</sub> = 10 × log₂(1 + 100) = 10 × 6.658 = 66.6 Mbps<br>66.6 / 10.0 ≈ 6.6 times<br>fade margin = 20 − 0.02 = 19.98 ≈ 20 dB</div></li>
</ol>
<p>Why the gap is so large: to avoid outage 99% of the time, the rate must be set by an SNR near the "worst 1%" (about 0 dB), about 20 dB below the average. For small ε, ln(1/(1 − ε)) ≈ ε, so γ<sub>min</sub> ≈ γ̄ ε: ε = 1% means 20 dB lower. Slide p.50 also gives the "average rate without errors" (1 − ε)C<sub>ε</sub> = 0.99 × 10.04 = 9.94 Mbps.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Using SNR in Shannon in (a): there is interference treated as noise, so use SINR.</li>
<li>Putting the dB value into log₂: log₂(1 + 5.6) is wrong; use the linear value 3.64.</li>
<li>Pressing log₁₀ instead of ln in (c): log₁₀(1/0.99) = 0.00436 would give γ<sub>min</sub> = 0.436 and C = 5.2 Mbps, wrong.</li>
<li>Substituting γ̄ = 20 directly (not converted to 100).</li>
<li>Giving numbers without the comparison: (c) should explain why C<sub>ε</sub> is far below the AWGN value (a fade margin of about 20 dB).</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
<div class="tmpl" lang="en"><p>(a) SNR = S/N = 2/0.05 = 40 (16.0 dB); SIR = S/I = 2/0.5 = 4 (6.0 dB); SINR = S/(I + N) = 2/0.55 = 3.64 (5.6 dB). Treating the interference as Gaussian noise, C = B log₂(1 + SINR) = 10⁷ × log₂(4.64) = 22.1 Mbps.</p><p>(b) With the interference removed, C = B log₂(1 + SNR) = 10⁷ × log₂(41) = 53.6 Mbps, about 2.4 times larger, because the link is interference-limited.</p><p>(c) γ̄ = 20 dB = 100. For Rayleigh fading, γ<sub>min</sub> = γ̄ ln(1/(1 − ε)) = 100 × ln(1/0.99) = 1.005, so C<sub>ε</sub> = 10⁷ × log₂(2.005) = 10.0 Mbps. An AWGN channel with SNR 20 dB gives C = 10⁷ × log₂(101) = 66.6 Mbps. The outage capacity is much lower because, to avoid outage 99% of the time, the rate must be set by an SNR about 20 dB below the average (the fade margin).</p></div>
<div class="ans">In one line: with interference treated as noise, put SINR = S/(I + N) into Shannon; without interference use SNR; for Rayleigh outage capacity first find γ<sub>min</sub> = γ̄ ln(1/(1 − ε)), which for ε = 1% is about 20 dB below γ̄, so the capacity is far below AWGN.</div>'''},

# ------------------------------------------------------------------ p8q10
'p8q10': {
'title': '知识讲解 + 详细解析：自由空间公式与简化路径损耗模型',
'title_en': 'Concept + step by step: free-space formula vs simplified path loss model',
'zh': r'''<h4><span class="st">知识讲解</span>自由空间（Friis）公式：每个符号是什么</h4>
<p>讲义第 2 章 p.4：没有任何遮挡、只有一条直射路径（LOS）时，\(P_r=\dfrac{P_tG_tG_r\lambda^2}{(4\pi)^2d^2}\)。P<sub>t</sub>、P<sub>r</sub> 是发射、接收功率；G<sub>t</sub>、G<sub>r</sub> 是收发天线增益（本题都是 1）；λ = c/f 是波长；d 是距离。讲义的两句结论：接收功率和 d² 成反比，和 λ² 成正比（也就是和 f² 成反比）。</p>
<p>取 dB 形式最好算：P<sub>r,dBm</sub> = P<sub>t,dBm</sub> + G<sub>t,dB</sub> + G<sub>r,dB</sub> + 20 log₁₀(λ/(4πd))。为什么是 20：(λ/4πd)² 取 10 log₁₀ 就等于 20 log₁₀(λ/4πd)。Part A 讲义（p.51）给的经验写法是 L(dB) = 32 + 20 log f(MHz) + 20 log d(km)，更精确的常数是 32.44。</p>
<h4><span class="st">课外补充</span>d² 和 λ² 从哪来（讲义没解释原因）</h4>
<p>d² 来自功率在半径为 d 的球面上摊开，球面积 4πd²；λ² 来自接收天线的有效面积和 λ² 成正比，频率越高，同样增益的天线"接住"的功率越少。</p>
<h4><span class="st">知识讲解</span>简化路径损耗模型：自由空间是它的特例</h4>
<p>讲义 p.8：P<sub>r,dB</sub> = P<sub>t,dB</sub> + K<sub>dB</sub> − 10γ log₁₀(d/d₀)，γ 是路径损耗指数（path loss exponent），K 和 γ 由实测数据拟合。老师说这个模型线性和 dB 两种形式都要背，考试不给；"simplified path loss model"是专有名词，往年 Quiz 有学生把它用成了自由空间模型。</p>
<p>把自由空间写成同样的形式：取 d₀ = 1 m，K<sub>dB</sub> = 20 log₁₀(λ/4π)，γ = 2。所以两个模型真正的区别是指数：每 10 倍距离，自由空间少 20 dB，γ = 3.5 时少 35 dB。</p>
<h4><span class="st">详细解析</span>(a) 1 km 处的自由空间接收功率</h4>
<ol>
<li>求波长：<div class="calc">λ = c/f = 3 × 10⁸ / (9 × 10⁸) = 0.3333 m</div></li>
<li>发射功率换 dBm（老师说 W / mW 没换会扣分）：<div class="calc">P<sub>t</sub> = 1 W = 1000 mW → 10 log₁₀1000 = 30 dBm</div></li>
<li>代 dB 公式（d 用米，和 λ 单位一致）：<div class="calc">λ/(4πd) = 0.3333 / (4π × 1000) = 0.3333 / 12566 = 2.65 × 10⁻⁵<br>20 log₁₀(2.65 × 10⁻⁵) = 20 × (−4.576) = −91.5 dB<br>P<sub>r</sub> = 30 − 91.5 = −61.5 dBm；路径损耗 = 30 − (−61.5) = 91.5 dB</div></li>
<li>核对：32.44 + 20 log₁₀900 + 20 log₁₀1 = 32.44 + 59.08 + 0 = 91.5 dB（这里 f 用 MHz、d 用 km）。</li>
</ol>
<h4><span class="st">详细解析</span>(b) 距离加倍、频率加倍</h4>
<div class="calc">P<sub>r</sub> ∝ d⁻²：d 加倍 → 少 20 log₁₀2 = 6.02 dB → −61.53 − 6.02 = −67.55 dBm<br>P<sub>r</sub> ∝ λ² ∝ f⁻²：f 再加倍 → 再少 6.02 dB → −67.55 − 6.02 = −73.6 dBm</div>
<p>规律：某个量在公式里是 n 次方，它加倍时功率变化 n × 3 dB（10 log₁₀2 ≈ 3）。自由空间里 d 和 f 都是 −2 次方，所以各是 −6 dB。</p>
<p>说明：上面解答里写的 −67.6 dBm 是舍入差。精确值是 −67.547 dBm，四舍五入到一位小数是 −67.5 dBm（两位小数 −67.55），相差 0.05 dB，不影响结论。</p>
<h4><span class="st">详细解析</span>(c) 简化模型，以及为什么不能用自由空间</h4>
<div class="calc">P<sub>r</sub> = 30 + (−31.5) − 10 × 3.5 × log₁₀1000 = 30 − 31.5 − 105 = −106.5 dBm<br>和自由空间相差：−61.5 − (−106.5) = 45 dB（功率比约 3.1 万倍）</div>
<p>为什么正好约 45 dB：900 MHz 时自由空间的 K<sub>dB</sub> = 20 log₁₀(0.3333/4π) = −31.5 dB，和题目的 K<sub>dB</sub> 几乎一样，所以两个模型在 1 m 处相同；从 1 m 到 1 km 是 3 个"10 倍"，自由空间少 20 × 3 = 60 dB，简化模型少 35 × 3 = 105 dB，差 45 dB。</p>
<p>为什么是严重错误：城区有楼房遮挡、地面和墙面反射，功率随距离衰减得比自由空间快得多。用自由空间会把接收功率高估约 45 dB，覆盖范围、中断概率、容量全都算错。题目写了 simplified path loss model，就必须用它。另外讲义 p.9 的表里城区宏蜂窝的 γ 是 3.7–6.5（γ 的取值表不用背），实际衰减可能比 γ = 3.5 更快，差距更大。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>用 10 log₁₀(λ/4πd)：λ/4πd 是幅度比，要用 20 log₁₀（或者先平方再 10 log₁₀）。</li>
<li>1 W 没换成 30 dBm，直接写 P<sub>r</sub> = 1 − 91.5。</li>
<li>Friis 公式里 d 代 km（λ 是米）：单位不一致。简化模型 d₀ = 1 m 时 d 也要用米：log₁₀1000 = 3，不是 log₁₀1 = 0（老师说今年 Quiz 有人这样丢了计算分）。</li>
<li>(b) 把"再加倍频率"理解成功率增加：f 越高 λ 越小，接收功率越小。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(a) λ = c/f = 3 × 10⁸ / 9 × 10⁸ = 0.333 m and P<sub>t</sub> = 1 W = 30 dBm. In free space, P<sub>r</sub> = P<sub>t</sub>G<sub>t</sub>G<sub>r</sub>(λ/4πd)², so P<sub>r,dBm</sub> = 30 + 20 log₁₀(0.333/(4π × 1000)) = 30 − 91.5 = −61.5 dBm, and the path loss is 91.5 dB.</p><p>(b) P<sub>r</sub> ∝ d⁻², so doubling d reduces P<sub>r</sub> by 20 log₁₀2 = 6 dB (to −67.55 dBm). P<sub>r</sub> ∝ λ² ∝ f⁻², so doubling f reduces it by another 6 dB (to −73.6 dBm).</p><p>(c) P<sub>r,dBm</sub> = P<sub>t,dBm</sub> + K<sub>dB</sub> − 10γ log₁₀(d/d₀) = 30 − 31.5 − 35 log₁₀(1000) = −106.5 dBm, about 45 dB below the free-space value. Free space assumes an unobstructed LOS path with γ = 2, whereas in an urban macrocell the power decays much faster (γ = 3.5) because of obstruction and reflections. Using free space would overestimate the received power by about 45 dB and give completely wrong coverage and outage results.</p></div>
<div class="ans">一句话：自由空间 P<sub>r</sub> = P<sub>t</sub>G<sub>t</sub>G<sub>r</sub>(λ/4πd)²，用 20 log₁₀ 算，d、f 加倍各少 6 dB；它等于 γ = 2 的简化模型，城区 γ = 3.5 时 1 km 处要再低约 45 dB，所以题目说简化模型就绝不能用自由空间。</div>''',
'en': r'''<h4><span class="st">Concept</span>The free-space (Friis) formula: what each symbol means</h4>
<p>Ch 2 p.4: with no obstruction and only a direct line-of-sight (LOS) path, \(P_r=\dfrac{P_tG_tG_r\lambda^2}{(4\pi)^2d^2}\). P<sub>t</sub> and P<sub>r</sub> are the transmit and received powers; G<sub>t</sub> and G<sub>r</sub> the antenna gains (both 1 here); λ = c/f the wavelength; d the distance. The two conclusions on the slide: the received power is inversely proportional to d² and proportional to λ² (i.e. inversely proportional to f²).</p>
<p>The dB form is easiest to compute: P<sub>r,dBm</sub> = P<sub>t,dBm</sub> + G<sub>t,dB</sub> + G<sub>r,dB</sub> + 20 log₁₀(λ/(4πd)). Why 20: taking 10 log₁₀ of (λ/4πd)² equals 20 log₁₀(λ/4πd). The Part A slides (p.51) give the practical form L(dB) = 32 + 20 log f(MHz) + 20 log d(km); the more precise constant is 32.44.</p>
<h4><span class="st">Beyond the slides</span>Where d² and λ² come from (the slide does not explain why)</h4>
<p>The factor d² comes from the power spreading over a sphere of radius d with area 4πd²; the factor λ² comes from the effective area of the receive antenna being proportional to λ², so at a higher frequency an antenna of the same gain "catches" less power.</p>
<h4><span class="st">Concept</span>The simplified path loss model: free space is a special case</h4>
<p>Slide p.8: P<sub>r,dB</sub> = P<sub>t,dB</sub> + K<sub>dB</sub> − 10γ log₁₀(d/d₀), where γ is the path loss exponent and K and γ are fitted to measured data. The lecturer said both the linear and dB forms must be memorised (not given in the exam); "simplified path loss model" is a proper name, and in past Quizzes some students used the free-space model instead.</p>
<p>Free space written in the same form: with d₀ = 1 m, K<sub>dB</sub> = 20 log₁₀(λ/4π) and γ = 2. So the real difference between the two models is the exponent: per factor of 10 in distance, free space loses 20 dB, while γ = 3.5 loses 35 dB.</p>
<h4><span class="st">Step by step</span>(a) Free-space received power at 1 km</h4>
<ol>
<li>Wavelength: <div class="calc">λ = c/f = 3 × 10⁸ / (9 × 10⁸) = 0.3333 m</div></li>
<li>Transmit power in dBm (the lecturer said a missing W / mW conversion loses marks): <div class="calc">P<sub>t</sub> = 1 W = 1000 mW → 10 log₁₀1000 = 30 dBm</div></li>
<li>Into the dB formula (d in metres, the same unit as λ): <div class="calc">λ/(4πd) = 0.3333 / (4π × 1000) = 0.3333 / 12566 = 2.65 × 10⁻⁵<br>20 log₁₀(2.65 × 10⁻⁵) = 20 × (−4.576) = −91.5 dB<br>P<sub>r</sub> = 30 − 91.5 = −61.5 dBm; path loss = 30 − (−61.5) = 91.5 dB</div></li>
<li>Check: 32.44 + 20 log₁₀900 + 20 log₁₀1 = 32.44 + 59.08 + 0 = 91.5 dB (here f in MHz, d in km).</li>
</ol>
<h4><span class="st">Step by step</span>(b) Doubling the distance, doubling the frequency</h4>
<div class="calc">P<sub>r</sub> ∝ d⁻²: doubling d → 20 log₁₀2 = 6.02 dB less → −61.53 − 6.02 = −67.55 dBm<br>P<sub>r</sub> ∝ λ² ∝ f⁻²: then doubling f → another 6.02 dB less → −67.55 − 6.02 = −73.6 dBm</div>
<p>Rule: if a quantity appears to the power n, doubling it changes the power by n × 3 dB (10 log₁₀2 ≈ 3). In free space d and f both appear to the power −2, so each gives −6 dB.</p>
<p>Note: the −67.6 dBm in the solution above is a rounding slip. The exact value is −67.547 dBm, which rounds to −67.5 dBm to one decimal (−67.55 to two); the 0.05 dB difference does not change any conclusion.</p>
<h4><span class="st">Step by step</span>(c) The simplified model, and why free space must not be used</h4>
<div class="calc">P<sub>r</sub> = 30 + (−31.5) − 10 × 3.5 × log₁₀1000 = 30 − 31.5 − 105 = −106.5 dBm<br>Difference from free space: −61.5 − (−106.5) = 45 dB (a power ratio of about 31 thousand)</div>
<p>Why almost exactly 45 dB: at 900 MHz the free-space K<sub>dB</sub> = 20 log₁₀(0.3333/4π) = −31.5 dB, almost the same as the K<sub>dB</sub> in the question, so the two models agree at 1 m; from 1 m to 1 km is three factors of 10, so free space loses 20 × 3 = 60 dB and the simplified model 35 × 3 = 105 dB, a difference of 45 dB.</p>
<p>Why it is a serious mistake: in a city, buildings block the signal and the ground and walls reflect it, so the power decays with distance much faster than in free space. Free space would overestimate the received power by about 45 dB, and coverage, outage probability and capacity would all be wrong. The question says simplified path loss model, so it must be used. Also, the table on slide p.9 gives γ = 3.7–6.5 for urban macrocells (the γ table need not be memorised), so the real decay may be even faster than γ = 3.5 and the gap even larger.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Using 10 log₁₀(λ/4πd): λ/4πd is an amplitude ratio, so use 20 log₁₀ (or square first, then 10 log₁₀).</li>
<li>Not converting 1 W to 30 dBm and writing P<sub>r</sub> = 1 − 91.5.</li>
<li>Putting d in km into Friis while λ is in metres: inconsistent units. In the simplified model with d₀ = 1 m, d must also be in metres: log₁₀1000 = 3, not log₁₀1 = 0 (the lecturer said some students lost the calculation marks this way in this year's Quiz).</li>
<li>In (b), thinking the power increases when the frequency doubles: a higher f means a smaller λ and a smaller received power.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
<div class="tmpl" lang="en"><p>(a) λ = c/f = 3 × 10⁸ / 9 × 10⁸ = 0.333 m and P<sub>t</sub> = 1 W = 30 dBm. In free space, P<sub>r</sub> = P<sub>t</sub>G<sub>t</sub>G<sub>r</sub>(λ/4πd)², so P<sub>r,dBm</sub> = 30 + 20 log₁₀(0.333/(4π × 1000)) = 30 − 91.5 = −61.5 dBm, and the path loss is 91.5 dB.</p><p>(b) P<sub>r</sub> ∝ d⁻², so doubling d reduces P<sub>r</sub> by 20 log₁₀2 = 6 dB (to −67.55 dBm). P<sub>r</sub> ∝ λ² ∝ f⁻², so doubling f reduces it by another 6 dB (to −73.6 dBm).</p><p>(c) P<sub>r,dBm</sub> = P<sub>t,dBm</sub> + K<sub>dB</sub> − 10γ log₁₀(d/d₀) = 30 − 31.5 − 35 log₁₀(1000) = −106.5 dBm, about 45 dB below the free-space value. Free space assumes an unobstructed LOS path with γ = 2, whereas in an urban macrocell the power decays much faster (γ = 3.5) because of obstruction and reflections. Using free space would overestimate the received power by about 45 dB and give completely wrong coverage and outage results.</p></div>
<div class="ans">In one line: free space is P<sub>r</sub> = P<sub>t</sub>G<sub>t</sub>G<sub>r</sub>(λ/4πd)², computed with 20 log₁₀, and doubling d or f costs 6 dB each; it is the simplified model with γ = 2, and with an urban γ = 3.5 the power at 1 km is about 45 dB lower, so when the question says simplified model, never use free space.</div>'''},

# ------------------------------------------------------------------ p8q11
'p8q11': {
'title': '知识讲解 + 详细解析：双径模型、临界距离与幂次换 dB',
'title_en': 'Concept + step by step: two-ray model, critical distance, powers to dB',
'zh': r'''<h4><span class="st">知识讲解</span>双径模型：直射 + 一次地面反射</h4>
<p>讲义第 2 章 p.5：接收端收到两路信号，一路直射（LOS），一路经地面反射一次。超过临界距离（critical distance）d<sub>c</sub> 后，接收功率近似为 \(P_r\approx P_tG_tG_r\dfrac{(h_th_r)^2}{d^4}\)，\(d_c=\dfrac{4h_th_r}{\lambda}\)。h<sub>t</sub>、h<sub>r</sub> 是收发天线高度，λ 是波长。Part A 第五章把它说成"远处 n = 4"，自由空间是 n = 2。</p>
<p>取 dB 形式：P<sub>r,dBm</sub> = P<sub>t,dBm</sub> + G<sub>t,dB</sub> + G<sub>r,dB</sub> + 20 log₁₀(h<sub>t</sub>h<sub>r</sub>) − 40 log₁₀d。注意：<b>远处的公式里没有 λ</b>，λ 只出现在 d<sub>c</sub> 里。</p>
<h4><span class="st">课外补充</span>为什么远处是 d⁻⁴（讲义只给结论）</h4>
<p>距离很远时，反射路径只比直射路径长约 2h<sub>t</sub>h<sub>r</sub>/d，而且地面反射会把相位翻转约 180°，两路几乎等大反相、大部分抵消。剩下的差值幅度和 1/d² 成正比，功率就和 1/d⁴ 成正比。d &lt; d<sub>c</sub> 时两路时而相加、时而抵消，功率随距离上下起伏，d⁻⁴ 公式不适用。</p>
<h4><span class="st">详细解析</span>(a) 临界距离</h4>
<div class="calc">λ = c/f = 3 × 10⁸ / (9 × 10⁸) = 0.3333 m<br>d<sub>c</sub> = 4 × 30 × 1.5 / 0.3333 = 180 / 0.3333 = 540 m</div>
<p>为什么先算它：双径的 d⁻⁴ 公式只在 d &gt; d<sub>c</sub> 时成立，(b)(c) 都要先确认距离在 d<sub>c</sub> 以外。</p>
<h4><span class="st">详细解析</span>(b) 5 km 处：双径对比自由空间</h4>
<ol>
<li>检查条件：5000 m &gt; 540 m，可以用双径公式。</li>
<li>线性算：<div class="calc">P<sub>r</sub> = 10 × (30 × 1.5)² / 5000⁴ = 10 × 2025 / 6.25 × 10¹⁴ = 3.24 × 10⁻¹¹ W</div></li>
<li>换 dBm（10 W = 40 dBm），也可以直接用 dB 形式核对：<div class="calc">10 log₁₀(3.24 × 10⁻¹¹) + 30 = −74.9 dBm<br>dB 形式：40 + 20 log₁₀45 − 40 log₁₀5000 = 40 + 33.06 − 147.96 = −74.9 dBm</div></li>
<li>同距离自由空间：<div class="calc">P<sub>r</sub> = 40 + 20 log₁₀(0.3333 / (4π × 5000)) = 40 − 105.5 = −65.5 dBm<br>双径比自由空间低：−65.5 − (−74.9) = 9.4 dB</div></li>
</ol>
<h4><span class="st">课外补充</span>差值的一般式（由讲义的两个公式自己相除得到）</h4>
<p>双径 ÷ 自由空间 = (4πh<sub>t</sub>h<sub>r</sub>/(λd))² = (πd<sub>c</sub>/d)²，所以差值 = 20 log₁₀(d/(πd<sub>c</sub>)) = 20 log₁₀(5000/1696) = 9.4 dB。π d<sub>c</sub> ≈ 1.7 km 以外双径比自由空间低，而且距离每远 10 倍，多低 20 dB。</p>
<h4><span class="st">详细解析</span>(c) 看幂次，换成 dB</h4>
<p>方法：某个量在公式里是 n 次方，它加倍时功率变化 10 log₁₀(2ⁿ) = n × 3.01 dB。</p>
<div class="tw"><table class="mini"><thead><tr><th>变化</th><th>双径（d &gt; d<sub>c</sub>）</th><th>自由空间</th></tr></thead><tbody>
<tr><td>(i) d 加倍</td><td>d⁻⁴ → −40 log₁₀2 = −12.04 dB</td><td>d⁻² → −6.02 dB</td></tr>
<tr><td>(ii) f 加倍</td><td>公式里没有 λ → 不变（0 dB）</td><td>λ² → −6.02 dB</td></tr>
<tr><td>(iii) h<sub>t</sub> 加倍</td><td>h<sub>t</sub>² → +20 log₁₀2 = +6.02 dB</td><td>和高度无关 → 0 dB</td></tr>
</tbody></table></div>
<p>别忘了检查前提：(ii) 频率加倍时 λ 减半，d<sub>c</sub> 变成 1080 m；(iii) h<sub>t</sub> 加倍时 d<sub>c</sub> 也变成 1080 m。两种情况 5 km 仍在 d<sub>c</sub> 以外，结论成立。</p>
<p>直觉：把基站天线架高，两条路径的长度差变大，抵消得少一些，收到的功率就多；这也是基站天线要装得高的原因之一。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>没先检查 d &gt; d<sub>c</sub> 就用 d⁻⁴ 公式。</li>
<li>以为双径远处功率也和频率有关：频率只影响 d<sub>c</sub>。</li>
<li>dB 系数用错：d⁻⁴ 是 −40 log₁₀d，(h<sub>t</sub>h<sub>r</sub>)² 是 +20 log₁₀(h<sub>t</sub>h<sub>r</sub>)。</li>
<li>10 W 没换成 40 dBm；或者 W 换 dBm 时忘了加 30。</li>
<li>算 d<sub>c</sub> 时 λ 用错（900 MHz 对应 1/3 m）。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(a) λ = c/f = 0.333 m, so d<sub>c</sub> = 4h<sub>t</sub>h<sub>r</sub>/λ = 4 × 30 × 1.5 / 0.333 = 540 m.</p><p>(b) Since d = 5 km &gt; d<sub>c</sub>, the two-ray approximation applies: P<sub>r</sub> = 10 × (30 × 1.5)² / 5000⁴ = 3.24 × 10⁻¹¹ W = −74.9 dBm. In free space, P<sub>r</sub> = 10 × (0.333/(4π × 5000))² = 2.81 × 10⁻¹⁰ W = −65.5 dBm. The two-ray power is about 9.4 dB lower, because far from the transmitter the ground-reflected ray nearly cancels the direct ray.</p><p>(c) Beyond d<sub>c</sub>, P<sub>r</sub> ∝ (h<sub>t</sub>h<sub>r</sub>)²/d⁴ and does not depend on λ. (i) Doubling d reduces P<sub>r</sub> by 40 log₁₀2 = 12 dB. (ii) Doubling the carrier frequency leaves P<sub>r</sub> unchanged (only d<sub>c</sub> doubles to 1080 m, still below 5 km). (iii) Doubling h<sub>t</sub> increases P<sub>r</sub> by 20 log₁₀2 = 6 dB.</p></div>
<div class="ans">一句话：先算 d<sub>c</sub> = 4h<sub>t</sub>h<sub>r</sub>/λ 并确认 d &gt; d<sub>c</sub>；远处 P<sub>r</sub> ∝ (h<sub>t</sub>h<sub>r</sub>)²/d⁴ 与频率无关；看幂次换 dB：距离加倍 −12 dB，频率加倍不变，天线高度加倍 +6 dB。</div>''',
'en': r'''<h4><span class="st">Concept</span>The two-ray model: direct ray + one ground reflection</h4>
<p>Ch 2 p.5: the receiver gets two signals, one direct (LOS) and one reflected once by the ground. Beyond the critical distance d<sub>c</sub>, the received power is approximately \(P_r\approx P_tG_tG_r\dfrac{(h_th_r)^2}{d^4}\), with \(d_c=\dfrac{4h_th_r}{\lambda}\). h<sub>t</sub> and h<sub>r</sub> are the antenna heights and λ the wavelength. Part A chapter 5 calls this "n = 4 at large distance"; free space is n = 2.</p>
<p>In dB: P<sub>r,dBm</sub> = P<sub>t,dBm</sub> + G<sub>t,dB</sub> + G<sub>r,dB</sub> + 20 log₁₀(h<sub>t</sub>h<sub>r</sub>) − 40 log₁₀d. Note: <b>there is no λ in the far-distance formula</b>; λ appears only in d<sub>c</sub>.</p>
<h4><span class="st">Beyond the slides</span>Why it is d⁻⁴ far away (the slide gives only the result)</h4>
<p>At a large distance the reflected path is only about 2h<sub>t</sub>h<sub>r</sub>/d longer than the direct path, and the ground reflection flips the phase by about 180°, so the two rays are almost equal and opposite and mostly cancel. The amplitude of what is left is proportional to 1/d², so the power is proportional to 1/d⁴. For d &lt; d<sub>c</sub> the two rays alternately add and cancel, the power oscillates with distance, and the d⁻⁴ formula does not apply.</p>
<h4><span class="st">Step by step</span>(a) Critical distance</h4>
<div class="calc">λ = c/f = 3 × 10⁸ / (9 × 10⁸) = 0.3333 m<br>d<sub>c</sub> = 4 × 30 × 1.5 / 0.3333 = 180 / 0.3333 = 540 m</div>
<p>Why compute it first: the two-ray d⁻⁴ formula holds only for d &gt; d<sub>c</sub>, so (b) and (c) both need to confirm the distance is beyond d<sub>c</sub>.</p>
<h4><span class="st">Step by step</span>(b) At 5 km: two-ray vs free space</h4>
<ol>
<li>Check the condition: 5000 m &gt; 540 m, so the two-ray formula can be used.</li>
<li>Linear: <div class="calc">P<sub>r</sub> = 10 × (30 × 1.5)² / 5000⁴ = 10 × 2025 / 6.25 × 10¹⁴ = 3.24 × 10⁻¹¹ W</div></li>
<li>To dBm (10 W = 40 dBm), or check directly with the dB form: <div class="calc">10 log₁₀(3.24 × 10⁻¹¹) + 30 = −74.9 dBm<br>dB form: 40 + 20 log₁₀45 − 40 log₁₀5000 = 40 + 33.06 − 147.96 = −74.9 dBm</div></li>
<li>Free space at the same distance: <div class="calc">P<sub>r</sub> = 40 + 20 log₁₀(0.3333 / (4π × 5000)) = 40 − 105.5 = −65.5 dBm<br>two-ray is lower than free space by −65.5 − (−74.9) = 9.4 dB</div></li>
</ol>
<h4><span class="st">Beyond the slides</span>The general gap (obtained by dividing the two slide formulas yourself)</h4>
<p>Two-ray ÷ free space = (4πh<sub>t</sub>h<sub>r</sub>/(λd))² = (πd<sub>c</sub>/d)², so the difference = 20 log₁₀(d/(πd<sub>c</sub>)) = 20 log₁₀(5000/1696) = 9.4 dB. Beyond π d<sub>c</sub> ≈ 1.7 km the two-ray power is below free space, and every factor of 10 in distance adds another 20 dB to the gap.</p>
<h4><span class="st">Step by step</span>(c) Read off the powers, convert to dB</h4>
<p>Method: if a quantity appears to the power n, doubling it changes the power by 10 log₁₀(2ⁿ) = n × 3.01 dB.</p>
<div class="tw"><table class="mini"><thead><tr><th>Change</th><th>Two-ray (d &gt; d<sub>c</sub>)</th><th>Free space</th></tr></thead><tbody>
<tr><td>(i) d doubled</td><td>d⁻⁴ → −40 log₁₀2 = −12.04 dB</td><td>d⁻² → −6.02 dB</td></tr>
<tr><td>(ii) f doubled</td><td>no λ in the formula → unchanged (0 dB)</td><td>λ² → −6.02 dB</td></tr>
<tr><td>(iii) h<sub>t</sub> doubled</td><td>h<sub>t</sub>² → +20 log₁₀2 = +6.02 dB</td><td>independent of height → 0 dB</td></tr>
</tbody></table></div>
<p>Do not forget to check the condition: in (ii) doubling the frequency halves λ, so d<sub>c</sub> becomes 1080 m; in (iii) doubling h<sub>t</sub> also makes d<sub>c</sub> 1080 m. In both cases 5 km is still beyond d<sub>c</sub>, so the conclusions hold.</p>
<p>Intuition: raising the base station antenna increases the path-length difference between the two rays, so they cancel less and more power arrives; this is one reason base station antennas are mounted high.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Using the d⁻⁴ formula without first checking d &gt; d<sub>c</sub>.</li>
<li>Thinking the far-distance two-ray power depends on frequency: the frequency only affects d<sub>c</sub>.</li>
<li>Wrong dB coefficients: d⁻⁴ is −40 log₁₀d, (h<sub>t</sub>h<sub>r</sub>)² is +20 log₁₀(h<sub>t</sub>h<sub>r</sub>).</li>
<li>Not converting 10 W to 40 dBm, or forgetting the +30 when converting W to dBm.</li>
<li>Using the wrong λ for d<sub>c</sub> (900 MHz corresponds to 1/3 m).</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
<div class="tmpl" lang="en"><p>(a) λ = c/f = 0.333 m, so d<sub>c</sub> = 4h<sub>t</sub>h<sub>r</sub>/λ = 4 × 30 × 1.5 / 0.333 = 540 m.</p><p>(b) Since d = 5 km &gt; d<sub>c</sub>, the two-ray approximation applies: P<sub>r</sub> = 10 × (30 × 1.5)² / 5000⁴ = 3.24 × 10⁻¹¹ W = −74.9 dBm. In free space, P<sub>r</sub> = 10 × (0.333/(4π × 5000))² = 2.81 × 10⁻¹⁰ W = −65.5 dBm. The two-ray power is about 9.4 dB lower, because far from the transmitter the ground-reflected ray nearly cancels the direct ray.</p><p>(c) Beyond d<sub>c</sub>, P<sub>r</sub> ∝ (h<sub>t</sub>h<sub>r</sub>)²/d⁴ and does not depend on λ. (i) Doubling d reduces P<sub>r</sub> by 40 log₁₀2 = 12 dB. (ii) Doubling the carrier frequency leaves P<sub>r</sub> unchanged (only d<sub>c</sub> doubles to 1080 m, still below 5 km). (iii) Doubling h<sub>t</sub> increases P<sub>r</sub> by 20 log₁₀2 = 6 dB.</p></div>
<div class="ans">In one line: first compute d<sub>c</sub> = 4h<sub>t</sub>h<sub>r</sub>/λ and confirm d &gt; d<sub>c</sub>; far away P<sub>r</sub> ∝ (h<sub>t</sub>h<sub>r</sub>)²/d⁴, independent of frequency; read off the powers in dB: doubling distance −12 dB, doubling frequency no change, doubling antenna height +6 dB.</div>'''},
}

NOTES = '''p8q7 (c): "x ≈ 2.29" is double-rounded. With Q(1.25)² = 0.011162 the exact inverse is x = 2.2848 (interpolating the 4-digit table, 0.0112 between Q(2.28) = 0.0113 and Q(2.29) = 0.0110, gives ≈ 2.283, i.e. nearer 2.28). The final answers are unaffected: required margin 18.28 ≈ 18.3 dB, gain ≈ 8.3 dB (2.28 → 18.24 dB, 2.29 → 18.32 dB). The box says "2.28 or 2.29 both fine"; the solution text was not changed.
p8q10 (c): the question labels γ = 3.5 as "urban macrocell", but the table on Ch 2 slide p.9 gives γ = 3.7–6.5 for urban macro-cells (3.5 is the upper end of urban micro-cells, 2.7–3.5). Harmless for the calculation (γ is given); the box mentions it neutrally as "the real decay may be even faster".
p8q10 (b): the solution (zh + en) gives the 2 km free-space power as −67.6 dBm; exact is −67.547 dBm (verify_mock prints −67.55), i.e. −67.5 to one decimal. The box uses −67.55 and says so neutrally; −73.6 dBm at 1.8 GHz is correct.
(aside, not in this group's boxes) Ch 2 slide p.47 LCR/AFD example: AFD should be 72.17 µs and 9950 errors/s (slide says 71.17 µs, 9812); already noted as 课外补充 on p2-learn.html.'''
