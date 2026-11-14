# -*- coding: utf-8 -*-
# 知识讲解 + 详细解析 for Part 2 practice, chapters 4–7 (diversity, MIMO, equalization, OFDM).
# Group p2b: p5q1–p5q3, p6q1–p6q3, p7q1–p7q3. Bilingual: 'zh' + 'en' bodies with the same structure.
# Every number is checked by check_p2b.py (run with /usr/bin/python3).

XPL = {}

# =====================================================================================  P5 Q1
XPL['p5q1'] = {
'title': '知识讲解 + 详细解析：注水法分配功率求容量',
'zh': r'''<h4><span class="st">知识讲解</span>为什么要"注水"</h4>
<p>MIMO 信道做奇异值分解（SVD）以后，等价于几条互不干扰的并行子信道（特征子信道，eigen-sub-channel，讲义第 5 章 p.19）。本题直接给出 3 条子信道。问题是：总功率 P 固定，怎么分给这 3 条，总容量最大？</p>
<p>每条子信道的容量都是香农公式 log₂(1 + SNR)。log 曲线"先陡后平"：SNR 小时多给一点功率，容量涨得快；SNR 已经很大时再加功率，涨得慢。所以最优分法不是平分，而是好信道多给、差信道少给、太差的干脆不给，这就是注水（water-filling，第 2 章 p.54–57；第 5 章 p.40 说发射端知道信道（informed transmitter）时就用它）。</p>
<p>三个公式（老师课上强调：求 γ₀ 的那个式子是他框起来要背的，考试不给，今年 Quiz 第 3 题就考了注水）：</p>
<div class="calc">P<sub>j</sub>/P = 1/γ₀ − 1/γ<sub>j</sub>（γ<sub>j</sub> ≥ γ₀ 时），否则 P<sub>j</sub> = 0</div>
<div class="calc">Σ<sub>j</sub> (1/γ₀ − 1/γ<sub>j</sub>) = 1（各子信道功率加起来等于 P）</div>
<div class="calc">C = B Σ<sub>j</sub> log₂(γ<sub>j</sub>/γ₀)（只对分到功率的子信道求和）</div>
<p>符号：γ<sub>j</sub> 是"把全部功率 P 都给第 j 条子信道"时它的 SNR（题目里的 80、40、40）；γ₀ 是截止值（cut-off），γ<sub>j</sub> 低于它的子信道一点功率都不给。形象地看：1/γ<sub>j</sub> 是"池底"，1/γ₀ 是"水面"，每条子信道分到的功率就是水面到池底的那段"水深"。</p>
<p>容量公式里为什么没有"1 +"：第 j 条分到 P<sub>j</sub> 后，SNR = γ<sub>j</sub>·P<sub>j</sub>/P = γ<sub>j</sub>(1/γ₀ − 1/γ<sub>j</sub>) = γ<sub>j</sub>/γ₀ − 1。代进香农公式：log₂(1 + γ<sub>j</sub>/γ₀ − 1) = log₂(γ<sub>j</sub>/γ₀)，"1 +"被抵消了。</p>
<div class="tw"><table class="mini"><thead><tr><th>子信道</th><th>γ<sub>j</sub></th><th>池底 1/γ<sub>j</sub></th><th>水深 P<sub>j</sub>/P</th></tr></thead><tbody><tr><td>1</td><td>80</td><td>0.0125</td><td>0.342</td></tr><tr><td>2</td><td>40</td><td>0.025</td><td>0.329</td></tr><tr><td>3</td><td>40</td><td>0.025</td><td>0.329</td></tr></tbody></table></div>
<p>水面 1/γ₀ = 0.354，三个池底都在水面以下，所以三条都分到功率。</p>
<h4><span class="st">详细解析</span>四步算出 124.7 Mbps</h4>
<ol>
<li><b>先假设三条都分到功率。</b>为什么：事先不知道哪条会被放弃，先全算，再检查。怎么算：Σ(1/γ₀ − 1/γ<sub>j</sub>) = 1 → 3/γ₀ = 1 + 1/80 + 1/40 + 1/40 = 1 + 0.0125 + 0.025 + 0.025 = 1.0625。</li>
<li><b>求 γ₀ 并检查。</b>γ₀ = 3/1.0625 = 2.82。最小的 γ<sub>j</sub> = 40 远大于 2.82，三条都保留，假设成立。如果有 γ<sub>j</sub> &lt; γ₀，就把它去掉，"3"改成"2"重算（第 2 章 p.56–57 的例题就去掉了 γ₃ = 0.087）。</li>
<li><b>分功率（题目没问，用来自检）。</b>1/γ₀ = 0.354；P₁/P = 0.354 − 0.0125 = 0.342，P₂/P = P₃/P = 0.354 − 0.025 = 0.329；加起来 0.342 + 0.329 + 0.329 = 1 ✓。</li>
<li><b>算容量。</b>γ₁/γ₀ = 80/2.82 = 28.33，γ₂/γ₀ = γ₃/γ₀ = 40/2.82 = 14.17。计算器没有 log₂ 时用 log₂x = log₁₀x / 0.301：log₂28.33 = 1.452/0.301 ≈ 4.82，log₂14.17 = 1.151/0.301 ≈ 3.82。</li>
</ol>
<div class="calc">C = 10 MHz × (4.82 + 3.82 + 3.82) = 10 MHz × 12.47 bit/s/Hz ≈ 124.7 Mbps ≈ 125 Mbps</div>
<h4><span class="st">自检</span>和功率平分比一比</h4>
<p>发射端不知道信道（uninformed）时只能平分：每条子信道分到 P/3，SNR 变成 80/3 = 26.7、40/3 = 13.3、13.3。</p>
<div class="calc">C = 10 MHz × [log₂(1 + 26.7) + 2 log₂(1 + 13.3)] = 10 × (4.79 + 2 × 3.84) ≈ 124.7 Mbps</div>
<p>只比注水少约 0.006 Mbps。原因：三条子信道 SNR 都很高，都在 log 曲线"平"的那一段，怎么分差别都很小。讲义第 5 章 p.42 也说：高 SNR 时 informed 和 uninformed 几乎没有差别。注水的好处在低 SNR 才明显（本题知识点框"对比 2"：SNR 都除以 100 后，注水 0.85 bit/s/Hz，平分 0.70 bit/s/Hz，注水高约 21%）。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>把 γ<sub>j</sub> 当成"分到功率以后"的 SNR。题目给的 80、40、40 是全部功率都给它时的 SNR。</li>
<li>平分时漏了"1 +"：写成 log₂(80/3) 会算出 122.1 Mbps（错）。注水公式没有"1 +"是因为被抵消了，平分公式必须有。</li>
<li>忘了检查 γ<sub>j</sub> ≥ γ₀；去掉一条子信道后忘了把 3/γ₀ 改成 2/γ₀。</li>
<li>最后忘了乘带宽 B = 10 MHz，或者单位写成 bit/s/Hz。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Informed transmitter → water-filling. Assume all three sub-channels are allocated power: \(\sum_{j=1}^{3}(1/\gamma_0-1/\gamma_j)=1\Rightarrow 3/\gamma_0=1+1/80+1/40+1/40=1.0625\Rightarrow\gamma_0=2.82\).</p><p>Since every \(\gamma_j\ge\gamma_0\), all three sub-channels are used, with \(P_j/P=1/\gamma_0-1/\gamma_j\) = 0.342, 0.329, 0.329 (sum = 1).</p><p>\(C=B\sum_j\log_2(\gamma_j/\gamma_0)=10\text{ MHz}\times[\log_2(80/2.82)+2\log_2(40/2.82)]=10\times(4.82+7.65)\approx124.7\text{ Mbps}\approx125\text{ Mbps}\).</p></div>
<div class="ans">一句话：先假设全分，由 Σ(1/γ₀ − 1/γ<sub>j</sub>) = 1 求出 γ₀ = 2.82，三条都比它大 → C = B Σ log₂(γ<sub>j</sub>/γ₀) ≈ 125 Mbps；高 SNR 下平分（124.7 Mbps）几乎一样。</div>''',
'title_en': 'Concept + walkthrough: water-filling capacity',
'en': r'''<h4><span class="st">Concept</span>Why "water-filling"</h4>
<p>After a singular value decomposition (SVD), a MIMO channel is equivalent to a few non-interfering parallel sub-channels (eigen-sub-channels, Ch 5 p.19). This question gives the 3 sub-channels directly. The problem: with a fixed total power P, how should it be split among the 3 to maximise the total capacity?</p>
<p>Each sub-channel's capacity is Shannon's log₂(1 + SNR). The log curve is "steep first, flat later": a little extra power on a low-SNR channel raises capacity quickly; on a channel whose SNR is already high it adds little. So the optimum is not an equal split: give more to good channels, less to poor ones, and nothing to very poor ones. This is water-filling (Ch 2 p.54–57; Ch 5 p.40 says it is used when the transmitter knows the channel, i.e. an informed transmitter).</p>
<p>Three formulas (lecturer's emphasis: the equation for γ₀ is boxed for memorising and will not be given in the exam; this year's Quiz Q3 was water-filling):</p>
<div class="calc">P<sub>j</sub>/P = 1/γ₀ − 1/γ<sub>j</sub> (if γ<sub>j</sub> ≥ γ₀), otherwise P<sub>j</sub> = 0</div>
<div class="calc">Σ<sub>j</sub> (1/γ₀ − 1/γ<sub>j</sub>) = 1 (the sub-channel powers add up to P)</div>
<div class="calc">C = B Σ<sub>j</sub> log₂(γ<sub>j</sub>/γ₀) (sum only over sub-channels that receive power)</div>
<p>Symbols: γ<sub>j</sub> is the SNR of sub-channel j if all the power P went to it (80, 40, 40 here); γ₀ is the cut-off: a sub-channel with γ<sub>j</sub> below it gets no power. Picture it: 1/γ<sub>j</sub> is the "floor" of a pool, 1/γ₀ is the "water level", and the power of each sub-channel is the "water depth" between the level and its floor.</p>
<p>Why there is no "1 +" in the capacity formula: after receiving P<sub>j</sub>, sub-channel j has SNR = γ<sub>j</sub>·P<sub>j</sub>/P = γ<sub>j</sub>(1/γ₀ − 1/γ<sub>j</sub>) = γ<sub>j</sub>/γ₀ − 1. In Shannon's formula: log₂(1 + γ<sub>j</sub>/γ₀ − 1) = log₂(γ<sub>j</sub>/γ₀); the "1 +" cancels.</p>
<div class="tw"><table class="mini"><thead><tr><th>Sub-channel</th><th>γ<sub>j</sub></th><th>Floor 1/γ<sub>j</sub></th><th>Depth P<sub>j</sub>/P</th></tr></thead><tbody><tr><td>1</td><td>80</td><td>0.0125</td><td>0.342</td></tr><tr><td>2</td><td>40</td><td>0.025</td><td>0.329</td></tr><tr><td>3</td><td>40</td><td>0.025</td><td>0.329</td></tr></tbody></table></div>
<p>Water level 1/γ₀ = 0.354; all three floors are below it, so all three get power.</p>
<h4><span class="st">Step by step</span>Four steps to 124.7 Mbps</h4>
<ol>
<li><b>Assume all three get power.</b> Why: we do not know in advance which one might be dropped, so compute with all, then check. How: Σ(1/γ₀ − 1/γ<sub>j</sub>) = 1 → 3/γ₀ = 1 + 1/80 + 1/40 + 1/40 = 1 + 0.0125 + 0.025 + 0.025 = 1.0625.</li>
<li><b>Find γ₀ and check.</b> γ₀ = 3/1.0625 = 2.82. The smallest γ<sub>j</sub> = 40 is far above 2.82, so all three stay and the assumption holds. If some γ<sub>j</sub> &lt; γ₀, drop it, change "3" to "2" and recompute (the example on Ch 2 p.56–57 drops γ₃ = 0.087).</li>
<li><b>Allocate power (not asked, used as a check).</b> 1/γ₀ = 0.354; P₁/P = 0.354 − 0.0125 = 0.342, P₂/P = P₃/P = 0.354 − 0.025 = 0.329; sum 0.342 + 0.329 + 0.329 = 1 ✓.</li>
<li><b>Compute the capacity.</b> γ₁/γ₀ = 80/2.82 = 28.33, γ₂/γ₀ = γ₃/γ₀ = 40/2.82 = 14.17. Without a log₂ key use log₂x = log₁₀x / 0.301: log₂28.33 = 1.452/0.301 ≈ 4.82, log₂14.17 = 1.151/0.301 ≈ 3.82.</li>
</ol>
<div class="calc">C = 10 MHz × (4.82 + 3.82 + 3.82) = 10 MHz × 12.47 bit/s/Hz ≈ 124.7 Mbps ≈ 125 Mbps</div>
<h4><span class="st">Check</span>Compare with an equal split</h4>
<p>An uninformed transmitter can only split equally: each sub-channel gets P/3, so the SNRs become 80/3 = 26.7, 40/3 = 13.3, 13.3.</p>
<div class="calc">C = 10 MHz × [log₂(1 + 26.7) + 2 log₂(1 + 13.3)] = 10 × (4.79 + 2 × 3.84) ≈ 124.7 Mbps</div>
<p>Only about 0.006 Mbps below water-filling. Reason: all three SNRs are high, on the flat part of the log curve, so the split hardly matters. Ch 5 p.42 says the same: at high SNR informed and uninformed transmitters are virtually identical. Water-filling pays off at low SNR (comparison 2 in the key-points box: with every SNR divided by 100, water-filling gives 0.85 bit/s/Hz and the equal split 0.70 bit/s/Hz, about 21% more for water-filling).</p>
<h4><span class="st">Pitfalls</span>Where marks are lost</h4>
<ul>
<li>Treating γ<sub>j</sub> as the SNR after allocation. The given 80, 40, 40 are the SNRs if all the power went to that sub-channel.</li>
<li>Dropping the "1 +" in the equal split: log₂(80/3) gives a wrong 122.1 Mbps. Water-filling has no "1 +" only because it cancels; the equal-split formula must keep it.</li>
<li>Forgetting to check γ<sub>j</sub> ≥ γ₀; after dropping a sub-channel, forgetting to change 3/γ₀ into 2/γ₀.</li>
<li>Forgetting to multiply by B = 10 MHz at the end, or giving the unit as bit/s/Hz.</li>
</ul>
<h4><span class="st">Exam</span>How to write it</h4>
<div class="tmpl" lang="en"><p>Informed transmitter → water-filling. Assume all three sub-channels are allocated power: \(\sum_{j=1}^{3}(1/\gamma_0-1/\gamma_j)=1\Rightarrow 3/\gamma_0=1+1/80+1/40+1/40=1.0625\Rightarrow\gamma_0=2.82\).</p><p>Since every \(\gamma_j\ge\gamma_0\), all three sub-channels are used, with \(P_j/P=1/\gamma_0-1/\gamma_j\) = 0.342, 0.329, 0.329 (sum = 1).</p><p>\(C=B\sum_j\log_2(\gamma_j/\gamma_0)=10\text{ MHz}\times[\log_2(80/2.82)+2\log_2(40/2.82)]=10\times(4.82+7.65)\approx124.7\text{ Mbps}\approx125\text{ Mbps}\).</p></div>
<div class="ans">In one line: assume all get power, solve Σ(1/γ₀ − 1/γ<sub>j</sub>) = 1 for γ₀ = 2.82, all three exceed it → C = B Σ log₂(γ<sub>j</sub>/γ₀) ≈ 125 Mbps; at this high SNR an equal split (124.7 Mbps) is practically the same.</div>''',
}

# =====================================================================================  P5 Q2
XPL['p5q2'] = {
'title': '知识讲解 + 详细解析：Alamouti 码的判决变量',
'zh': r'''<h4><span class="st">知识讲解</span>Alamouti 码在解决什么问题</h4>
<p>发射分集（transmit diversity）：发射端 2 根天线、接收端 1 根，而且发射端<b>不知道</b>信道。如果两根天线同时发同一个符号，收到的是 (h<sub>A</sub> + h<sub>B</sub>)u，而 h<sub>A</sub> + h<sub>B</sub> 只是另一个高斯随机变量，照样会深衰落，<b>没有分集</b>（第 5 章 p.18）。Alamouti 的办法是把两个符号在"空间（两根天线）× 时间（两个时隙）"上交错排列，叫空时块码（STBC，第 5 章 p.20–21）：</p>
<div class="tw"><table class="mini"><thead><tr><th>时隙</th><th>天线 A</th><th>天线 B</th></tr></thead><tbody><tr><td>1</td><td>u₁</td><td>u₂</td></tr><tr><td>2</td><td>−u₂*</td><td>u₁*</td></tr></tbody></table></div>
<p>老师课上强调：这个编码矩阵是蓝框，要背。它的关键性质是正交：X X<sup>H</sup> = (|u₁|² + |u₂|²) I（第 5 章 p.22、p.29）。正交性到了接收端，就变成下面矩阵 F 的性质 F<sup>H</sup>F = ‖h‖² I：两个符号可以用简单的线性运算完全分开。</p>
<p>要用到的工具：共轭规则 (ab)* = a*b*、(a*)* = a；|h|² = h·h*；F<sup>H</sup> 是共轭转置（先转置，再每个元素取共轭）；噪声乘上复数 c 后方差变成 |c|²N₀；两个独立噪声相加，方差相加。</p>
<p>判决变量（decision variable）：接收端最后拿去判决的那个量。老师说它要满足两点：只含要检测的那一个符号，而且符号前面乘的是标量，不是向量。</p>
<h4><span class="st">详细解析</span>六步推出 z₁、z₂</h4>
<ol>
<li><b>写出两个时隙的接收信号。</b>为什么：先把发送方案翻译成方程。<div class="calc">y₁ = h<sub>A</sub>u₁ + h<sub>B</sub>u₂ + w₁</div><div class="calc">y₂ = h<sub>A</sub>(−u₂*) + h<sub>B</sub>u₁* + w₂ = −h<sub>A</sub>u₂* + h<sub>B</sub>u₁* + w₂</div></li>
<li><b>对 y₂ 取共轭。</b>为什么：y₂ 里出现的是 u₁*、u₂*，和 y₁ 里的 u₁、u₂ 不是同一组未知数，没法联立（老师说：两个方程四个未知数，解不出来）。共轭以后两个式子都只含 u₁、u₂：<div class="calc">y₂* = h<sub>B</sub>*u₁ − h<sub>A</sub>*u₂ + w₂*</div></li>
<li><b>写成矩阵并检查正交。</b>\(\tilde{\mathbf y}=\begin{bmatrix}y_1\\y_2^*\end{bmatrix}=\mathbf F\begin{bmatrix}u_1\\u_2\end{bmatrix}+\begin{bmatrix}w_1\\w_2^*\end{bmatrix}\)，\(\mathbf F=\begin{bmatrix}h_A&amp;h_B\\h_B^*&amp;-h_A^*\end{bmatrix}\)（第 5 章 p.23）。F<sup>H</sup>F 的对角元 = |h<sub>A</sub>|² + |h<sub>B</sub>|²；非对角元 = h<sub>A</sub>*h<sub>B</sub> − h<sub>B</sub>h<sub>A</sub>* = 0。所以 F<sup>H</sup>F = ‖h‖² I。</li>
<li><b>左乘 F<sup>H</sup>。</b>为什么：交叉项是 0，每个输出只剩一个符号。<div class="calc">z₁ = h<sub>A</sub>*y₁ + h<sub>B</sub>y₂*，z₂ = h<sub>B</sub>*y₁ − h<sub>A</sub>y₂*</div>展开 z₁ 验证：h<sub>A</sub>*(h<sub>A</sub>u₁ + h<sub>B</sub>u₂ + w₁) + h<sub>B</sub>(h<sub>B</sub>*u₁ − h<sub>A</sub>*u₂ + w₂*) = (|h<sub>A</sub>|² + |h<sub>B</sub>|²)u₁ + (h<sub>A</sub>*h<sub>B</sub> − h<sub>B</sub>h<sub>A</sub>*)u₂ + h<sub>A</sub>*w₁ + h<sub>B</sub>w₂*。u₂ 的两项正好抵消，这就是 −u₂* 里负号和共轭的作用。z₂ 同理。</li>
<li><b>算噪声方差。</b>h<sub>A</sub>*w₁ 的方差是 |h<sub>A</sub>|²N₀，h<sub>B</sub>w₂* 的方差是 |h<sub>B</sub>|²N₀，两者独立，相加得 (|h<sub>A</sub>|² + |h<sub>B</sub>|²)N₀ = ‖h‖²N₀。</li>
<li><b>归一化。</b>两边除以 ‖h‖ = √(|h<sub>A</sub>|² + |h<sub>B</sub>|²)，信号项变成 ‖h‖u₁，噪声方差回到 ‖h‖²N₀/‖h‖² = N₀：<div class="calc">z₁ = ‖h‖u₁ + w̃₁，z₂ = ‖h‖u₂ + w̃₂，w̃₁, w̃₂ ~ N(0, N₀)</div>这就是官方答案的形式。如果改为除以 ‖h‖²，就得到讲义 p.25 的 û = u + 噪声，噪声方差 N₀/‖h‖²。</li>
</ol>
<p><b>数字验证</b>（不含噪声）：取 h<sub>A</sub> = 1、h<sub>B</sub> = j、u₁ = 1、u₂ = −1。y₁ = 1 − j，y₂ = −1·(−1) + j·1 = 1 + j，y₂* = 1 − j。z₁ = 1·(1 − j) + j(1 − j) = 2 = ‖h‖²u₁ ✓（‖h‖² = 2）；z₂ = (−j)(1 − j) − (1 − j) = −2 = ‖h‖²u₂ ✓。</p>
<p><b>为什么是二阶分集：</b>每个符号的有效 SNR ∝ |h<sub>A</sub>|² + |h<sub>B</sub>|²，两条独立衰落路径同时很弱的概率远小于一条很弱的概率（讲义 p.26）。而且发射端完全不需要知道信道，只有接收端要知道 h<sub>A</sub>、h<sub>B</sub>（用来算 F<sup>H</sup>）。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>第二时隙天线 A 发的是 −u₂*：负号和共轭缺一不可，少了负号 u₂ 的交叉项就消不掉。</li>
<li>只对 y₂ 取共轭，y₁ 不动；z₁ 里乘的是 h<sub>B</sub>（不带共轭）乘 y₂*。</li>
<li>左乘 F<sup>H</sup> 后噪声方差是 ‖h‖²N₀，不是 N₀；除以 ‖h‖ 以后才回到 N₀。</li>
<li>官方答案写成 ‖h₁‖、‖h₂‖ 两个符号，其实是同一个 √(|h<sub>A</sub>|² + |h<sub>B</sub>|²)。</li>
<li>如果总发射功率固定，两根天线各分一半，Alamouti 的 SNR 比 1 发 2 收的 MRC 低 3 dB（第 5 章 p.30），但分集阶数一样是 2。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Received signals: \(y_1=h_Au_1+h_Bu_2+w_1\), \(y_2=-h_Au_2^*+h_Bu_1^*+w_2\). Take the conjugate of \(y_2\): \(y_2^*=h_B^*u_1-h_A^*u_2+w_2^*\).</p><p>Matrix form: \([y_1,\ y_2^*]^T=\mathbf F[u_1,\ u_2]^T+[w_1,\ w_2^*]^T\) with \(\mathbf F=\begin{bmatrix}h_A&amp;h_B\\h_B^*&amp;-h_A^*\end{bmatrix}\) and \(\mathbf F^H\mathbf F=(|h_A|^2+|h_B|^2)\mathbf I=\|\mathbf h\|^2\mathbf I\).</p><p>Pre-multiply by \(\mathbf F^H\): \(z_1=h_A^*y_1+h_By_2^*=\|\mathbf h\|^2u_1+h_A^*w_1+h_Bw_2^*\), \(z_2=h_B^*y_1-h_Ay_2^*=\|\mathbf h\|^2u_2+h_B^*w_1-h_Aw_2^*\); the noise terms have variance \(\|\mathbf h\|^2N_0\).</p><p>Dividing by \(\|\mathbf h\|\): \(z_1=\|\mathbf h\|u_1+\tilde w_1\), \(z_2=\|\mathbf h\|u_2+\tilde w_2\), \(\tilde w_i\sim\mathcal N(0,N_0)\). Each symbol sees \(|h_A|^2+|h_B|^2\): diversity order 2 without channel knowledge at the transmitter.</p></div>
<div class="ans">一句话：y₂ 取共轭 → ỹ = Fu + w̃，F 正交 → 左乘 F<sup>H</sup> 得 z<sub>i</sub> = ‖h‖²u<sub>i</sub> + 噪声 → 除以 ‖h‖：z<sub>i</sub> = ‖h‖u<sub>i</sub> + w̃<sub>i</sub>，w̃<sub>i</sub> ~ N(0, N₀)；二阶分集，发射端不用知道信道。</div>''',
'title_en': 'Concept + walkthrough: Alamouti decision variables',
'en': r'''<h4><span class="st">Concept</span>What problem the Alamouti code solves</h4>
<p>Transmit diversity: 2 antennas at the transmitter, 1 at the receiver, and the transmitter does <b>not</b> know the channel. If both antennas sent the same symbol at the same time, the receiver would get (h<sub>A</sub> + h<sub>B</sub>)u; but h<sub>A</sub> + h<sub>B</sub> is just another Gaussian random variable that fades just as deeply, so there is <b>no diversity</b> (Ch 5 p.18). Alamouti's idea is to arrange the two symbols across "space (two antennas) × time (two slots)", a space-time block code (STBC, Ch 5 p.20–21):</p>
<div class="tw"><table class="mini"><thead><tr><th>Slot</th><th>Antenna A</th><th>Antenna B</th></tr></thead><tbody><tr><td>1</td><td>u₁</td><td>u₂</td></tr><tr><td>2</td><td>−u₂*</td><td>u₁*</td></tr></tbody></table></div>
<p>Lecturer's emphasis: this code matrix is in a blue box and must be memorised. Its key property is orthogonality: X X<sup>H</sup> = (|u₁|² + |u₂|²) I (Ch 5 p.22, p.29). At the receiver orthogonality becomes the property F<sup>H</sup>F = ‖h‖² I of the matrix F below: the two symbols can be separated completely by simple linear operations.</p>
<p>Tools needed: conjugate rules (ab)* = a*b*, (a*)* = a; |h|² = h·h*; F<sup>H</sup> is the conjugate transpose (transpose, then conjugate every element); multiplying noise by a complex c scales its variance by |c|²; the variances of two independent noises add.</p>
<p>Decision variable: the quantity the receiver finally feeds to the decision. The lecturer says it must satisfy two things: it contains only the one symbol being detected, and that symbol is multiplied by a scalar, not a vector.</p>
<h4><span class="st">Step by step</span>Six steps to z₁ and z₂</h4>
<ol>
<li><b>Write the received signals in the two slots.</b> Why: translate the transmission scheme into equations.<div class="calc">y₁ = h<sub>A</sub>u₁ + h<sub>B</sub>u₂ + w₁</div><div class="calc">y₂ = h<sub>A</sub>(−u₂*) + h<sub>B</sub>u₁* + w₂ = −h<sub>A</sub>u₂* + h<sub>B</sub>u₁* + w₂</div></li>
<li><b>Conjugate y₂.</b> Why: y₂ contains u₁* and u₂*, not the same unknowns as u₁ and u₂ in y₁, so the two equations cannot be solved together (lecturer: two equations, four unknowns). After conjugating, both equations contain only u₁ and u₂:<div class="calc">y₂* = h<sub>B</sub>*u₁ − h<sub>A</sub>*u₂ + w₂*</div></li>
<li><b>Write it as a matrix and check orthogonality.</b> \(\tilde{\mathbf y}=\begin{bmatrix}y_1\\y_2^*\end{bmatrix}=\mathbf F\begin{bmatrix}u_1\\u_2\end{bmatrix}+\begin{bmatrix}w_1\\w_2^*\end{bmatrix}\), \(\mathbf F=\begin{bmatrix}h_A&amp;h_B\\h_B^*&amp;-h_A^*\end{bmatrix}\) (Ch 5 p.23). The diagonal elements of F<sup>H</sup>F are |h<sub>A</sub>|² + |h<sub>B</sub>|²; the off-diagonal ones are h<sub>A</sub>*h<sub>B</sub> − h<sub>B</sub>h<sub>A</sub>* = 0. Hence F<sup>H</sup>F = ‖h‖² I.</li>
<li><b>Pre-multiply by F<sup>H</sup>.</b> Why: the cross terms are 0, so each output keeps only one symbol.<div class="calc">z₁ = h<sub>A</sub>*y₁ + h<sub>B</sub>y₂*, z₂ = h<sub>B</sub>*y₁ − h<sub>A</sub>y₂*</div>Expand z₁ to verify: h<sub>A</sub>*(h<sub>A</sub>u₁ + h<sub>B</sub>u₂ + w₁) + h<sub>B</sub>(h<sub>B</sub>*u₁ − h<sub>A</sub>*u₂ + w₂*) = (|h<sub>A</sub>|² + |h<sub>B</sub>|²)u₁ + (h<sub>A</sub>*h<sub>B</sub> − h<sub>B</sub>h<sub>A</sub>*)u₂ + h<sub>A</sub>*w₁ + h<sub>B</sub>w₂*. The two u₂ terms cancel exactly; that is what the minus sign and the conjugate in −u₂* are for. z₂ works the same way.</li>
<li><b>Noise variance.</b> h<sub>A</sub>*w₁ has variance |h<sub>A</sub>|²N₀, h<sub>B</sub>w₂* has variance |h<sub>B</sub>|²N₀; they are independent, so the total is (|h<sub>A</sub>|² + |h<sub>B</sub>|²)N₀ = ‖h‖²N₀.</li>
<li><b>Normalise.</b> Divide by ‖h‖ = √(|h<sub>A</sub>|² + |h<sub>B</sub>|²): the signal term becomes ‖h‖u₁ and the noise variance returns to ‖h‖²N₀/‖h‖² = N₀:<div class="calc">z₁ = ‖h‖u₁ + w̃₁, z₂ = ‖h‖u₂ + w̃₂, w̃₁, w̃₂ ~ N(0, N₀)</div>This is the form of the official answer. Dividing by ‖h‖² instead gives û = u + noise with variance N₀/‖h‖², as on slide p.25.</li>
</ol>
<p><b>Numerical check</b> (no noise): take h<sub>A</sub> = 1, h<sub>B</sub> = j, u₁ = 1, u₂ = −1. y₁ = 1 − j, y₂ = −1·(−1) + j·1 = 1 + j, y₂* = 1 − j. z₁ = 1·(1 − j) + j(1 − j) = 2 = ‖h‖²u₁ ✓ (‖h‖² = 2); z₂ = (−j)(1 − j) − (1 − j) = −2 = ‖h‖²u₂ ✓.</p>
<p><b>Why diversity order 2:</b> the effective SNR of each symbol is proportional to |h<sub>A</sub>|² + |h<sub>B</sub>|²; two independently fading paths being weak at the same time is far less likely than one being weak (slide p.26). And the transmitter needs no channel knowledge at all; only the receiver must know h<sub>A</sub>, h<sub>B</sub> (to form F<sup>H</sup>).</p>
<h4><span class="st">Pitfalls</span>Where marks are lost</h4>
<ul>
<li>In slot 2 antenna A sends −u₂*: both the minus sign and the conjugate are needed; without the minus sign the u₂ cross terms do not cancel.</li>
<li>Only y₂ is conjugated, y₁ is left alone; in z₁, h<sub>B</sub> (no conjugate) multiplies y₂*.</li>
<li>After pre-multiplying by F<sup>H</sup> the noise variance is ‖h‖²N₀, not N₀; it returns to N₀ only after dividing by ‖h‖.</li>
<li>The official answer writes ‖h₁‖ and ‖h₂‖, but both are the same √(|h<sub>A</sub>|² + |h<sub>B</sub>|²).</li>
<li>With a fixed total transmit power, each antenna gets half, so Alamouti's SNR is 3 dB below 1 × 2 MRC (Ch 5 p.30), but the diversity order is the same, 2.</li>
</ul>
<h4><span class="st">Exam</span>How to write it</h4>
<div class="tmpl" lang="en"><p>Received signals: \(y_1=h_Au_1+h_Bu_2+w_1\), \(y_2=-h_Au_2^*+h_Bu_1^*+w_2\). Take the conjugate of \(y_2\): \(y_2^*=h_B^*u_1-h_A^*u_2+w_2^*\).</p><p>Matrix form: \([y_1,\ y_2^*]^T=\mathbf F[u_1,\ u_2]^T+[w_1,\ w_2^*]^T\) with \(\mathbf F=\begin{bmatrix}h_A&amp;h_B\\h_B^*&amp;-h_A^*\end{bmatrix}\) and \(\mathbf F^H\mathbf F=(|h_A|^2+|h_B|^2)\mathbf I=\|\mathbf h\|^2\mathbf I\).</p><p>Pre-multiply by \(\mathbf F^H\): \(z_1=h_A^*y_1+h_By_2^*=\|\mathbf h\|^2u_1+h_A^*w_1+h_Bw_2^*\), \(z_2=h_B^*y_1-h_Ay_2^*=\|\mathbf h\|^2u_2+h_B^*w_1-h_Aw_2^*\); the noise terms have variance \(\|\mathbf h\|^2N_0\).</p><p>Dividing by \(\|\mathbf h\|\): \(z_1=\|\mathbf h\|u_1+\tilde w_1\), \(z_2=\|\mathbf h\|u_2+\tilde w_2\), \(\tilde w_i\sim\mathcal N(0,N_0)\). Each symbol sees \(|h_A|^2+|h_B|^2\): diversity order 2 without channel knowledge at the transmitter.</p></div>
<div class="ans">In one line: conjugate y₂ → ỹ = Fu + w̃ with orthogonal F → pre-multiply by F<sup>H</sup> to get z<sub>i</sub> = ‖h‖²u<sub>i</sub> + noise → divide by ‖h‖: z<sub>i</sub> = ‖h‖u<sub>i</sub> + w̃<sub>i</sub>, w̃<sub>i</sub> ~ N(0, N₀); diversity order 2, no channel knowledge needed at the transmitter.</div>''',
}

# =====================================================================================  P5 Q3
XPL['p5q3'] = {
'title': '知识讲解 + 详细解析：分集-复用折中求速率和 P_e',
'zh': r'''<h4><span class="st">知识讲解</span>分集增益 d 和复用增益 r</h4>
<p>N 发 M 收的 MIMO 有两种用法（第 4 章 p.31–33）：</p>
<ul>
<li><b>分集（diversity）</b>：同一份数据走很多条独立路径，求"稳"。用分集增益 d 衡量：高 SNR 时 P<sub>e</sub> ≈ SNR<sup>−d</sup>，d 越大，SNR 每提高一点误码率降得越快。最大 d = N × M。</li>
<li><b>复用（multiplexing）</b>：同时发几路不同的数据，求"快"。用复用增益 r 衡量：速率 R = r·log₂SNR（bit/s/Hz），相当于同时有 r 路数据，每路 log₂SNR。最大 r = min(N, M)，因为高 SNR 时容量 C ≈ min(N, M)·log₂SNR（p.31）。</li>
</ul>
<p>两者不能同时拉满：天线资源用来"多传"就不能全用来"传得稳"。题目给的折中曲线 d(r) = (N − r)(M − r)（p.33）：r = 0 时 d = N × M（全分集），r = min(N, M) 时 d = 0（全复用）。老师课上强调：这只是其中一种折中关系，r、d 都取整数，画出来是离散的点。</p>
<p>本题的解题思路就是"把题目给的符号连起来"（老师讲 p.34 例题时的说法）：P<sub>e</sub> 的要求 → 最小 d → 最大 r → 速率 R。</p>
<h4><span class="st">详细解析</span>(a) 由误码率要求定出 r</h4>
<ol>
<li><b>dB 换线性。</b>为什么：公式 P<sub>e</sub> = γ<sup>−d</sup> 里的 γ 是线性值。γ = 10<sup>10/10</sup> = 10。</li>
<li><b>求 d 的下限。</b>10<sup>−d</sup> ≤ 10<sup>−3</sup> ⇔ −d ≤ −3 ⇔ d ≥ 3。一般情况：d ≥ log(1/P<sub>e,目标</sub>) / log γ = 3/1 = 3。</li>
<li><b>找满足 d ≥ 3 的最大 r。</b>两种做法：
<div class="tw"><table class="mini"><thead><tr><th>r</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody><tr><td>d = (8 − r)(4 − r)</td><td>32</td><td>21</td><td>12</td><td>5</td><td>0</td></tr></tbody></table></div>
逐个列表：r = 3 时 d = 5 ≥ 3，r = 4 时 d = 0，不行。老师的做法：解 (8 − r)(4 − r) = 3，即 r² − 12r + 29 = 0，r = 6 ± √7 ≈ 3.35 或 8.65。8.65 超过 min(N, M) = 4，舍去；在 0 ≤ r ≤ 4 内 d 随 r 增大而减小，所以要 r ≤ 3.35，取整数 r = 3。</li>
<li><b>算速率。</b>由定义 r = R/log₂SNR：<div class="calc">R = r·log₂γ = 3 × log₂10 = 3 × 3.32 = 9.97 bit/s/Hz</div>log₂10 = 1/0.301 = 3.32。精确值 3 × 3.3219 = 9.966，官方答案写 9.96（截断），写 9.97 或 9.96 都对。</li>
</ol>
<h4><span class="st">详细解析</span>(b) 代回去求实际误码率</h4>
<p>r = 3 → d = (8 − 3)(4 − 3) = 5 → P<sub>e</sub> = γ<sup>−d</sup> = 10<sup>−5</sup>。比要求的 10<sup>−3</sup> 还好，因为 r 只能取整数，从 3.35 退到 3，多出来的分集就变成了更低的误码率。</p>
<h4><span class="st">自检</span>合理吗</h4>
<ul>
<li>r = 3 ≤ min(8, 4) = 4 ✓；d = 5 ≤ N × M = 32 ✓。</li>
<li>如果取 r = 4：R = 4 × 3.32 = 13.3 bit/s/Hz 更快，但 d = 0，误码率不随 SNR 下降，不满足要求。</li>
<li>如果取 r = 2：d = 12，P<sub>e</sub> = 10<sup>−12</sup> 很稳，但 R = 6.64 bit/s/Hz，浪费了速率。</li>
</ul>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>SNR 没换成线性值（10 dB → 10）。</li>
<li>d 必须是整数：d ≥ 3 时 r 要向下取整到 3，不能取 3.35。</li>
<li>二次方程的另一个根 8.65 超出 min(N, M)，没有意义。</li>
<li>R 用 log₂，不是 log₁₀ 或 ln。</li>
<li>(b) 问的是用 r = 3 实际得到的 P<sub>e</sub>（10<sup>−5</sup>），不是题目要求的 10<sup>−3</sup>。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(a) γ = 10 dB = 10. \(P_e=\gamma^{-d}\le10^{-3}\Rightarrow10^{-d}\le10^{-3}\Rightarrow d\ge3\).</p><p>With N = 8, M = 4: d(r) = (8 − r)(4 − r) gives d = 32, 21, 12, 5, 0 for r = 0, 1, 2, 3, 4 (r ≤ min(N, M) = 4, integer). The largest r with d ≥ 3 is r = 3.</p><p>Since \(r=R/\log_2\mathrm{SNR}\), the maximum rate is \(R=r\log_2\gamma=3\log_210\approx9.97\) bit/s/Hz.</p><p>(b) With r = 3, d = (8 − 3)(4 − 3) = 5, so \(P_e=\gamma^{-5}=10^{-5}\).</p></div>
<div class="ans">一句话：10 dB → 10，P<sub>e</sub> ≤ 10⁻³ 要求 d ≥ 3 → d(r) = (8 − r)(4 − r) ≥ 3 的最大整数 r = 3 → R = 3 log₂10 ≈ 9.97 bit/s/Hz，d(3) = 5 → P<sub>e</sub> = 10⁻⁵。</div>''',
'title_en': 'Concept + walkthrough: DMT, rate and P_e',
'en': r'''<h4><span class="st">Concept</span>Diversity gain d and multiplexing gain r</h4>
<p>An N × M MIMO system can be used in two ways (Ch 4 p.31–33):</p>
<ul>
<li><b>Diversity</b>: the same data travels over many independent paths, for "reliability". Measured by the diversity gain d: at high SNR P<sub>e</sub> ≈ SNR<sup>−d</sup>; the larger d, the faster the error rate falls as the SNR rises. Maximum d = N × M.</li>
<li><b>Multiplexing</b>: several different data streams are sent at once, for "speed". Measured by the multiplexing gain r: the rate R = r·log₂SNR (bit/s/Hz), as if r streams each carried log₂SNR. Maximum r = min(N, M), because at high SNR the capacity C ≈ min(N, M)·log₂SNR (p.31).</li>
</ul>
<p>Both cannot be maxed out at once: antennas used to "send more" cannot all be used to "send reliably". The trade-off curve given here, d(r) = (N − r)(M − r) (p.33): r = 0 gives d = N × M (full diversity), r = min(N, M) gives d = 0 (full multiplexing). Lecturer's emphasis: this is only one possible trade-off; r and d are integers, so the curve is a set of discrete points.</p>
<p>The method is to "connect the symbols the question gives you" (the lecturer's words on the p.34 example): P<sub>e</sub> requirement → minimum d → maximum r → rate R.</p>
<h4><span class="st">Step by step</span>(a) Find r from the error-rate requirement</h4>
<ol>
<li><b>dB to linear.</b> Why: the γ in P<sub>e</sub> = γ<sup>−d</sup> is a linear value. γ = 10<sup>10/10</sup> = 10.</li>
<li><b>Lower bound on d.</b> 10<sup>−d</sup> ≤ 10<sup>−3</sup> ⇔ −d ≤ −3 ⇔ d ≥ 3. In general: d ≥ log(1/P<sub>e,target</sub>) / log γ = 3/1 = 3.</li>
<li><b>Largest r with d ≥ 3.</b> Two ways:
<div class="tw"><table class="mini"><thead><tr><th>r</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody><tr><td>d = (8 − r)(4 − r)</td><td>32</td><td>21</td><td>12</td><td>5</td><td>0</td></tr></tbody></table></div>
By the table: r = 3 gives d = 5 ≥ 3, r = 4 gives d = 0, which fails. The lecturer's way: solve (8 − r)(4 − r) = 3, i.e. r² − 12r + 29 = 0, r = 6 ± √7 ≈ 3.35 or 8.65. 8.65 exceeds min(N, M) = 4 and is discarded; for 0 ≤ r ≤ 4, d falls as r grows, so we need r ≤ 3.35, and the integer is r = 3.</li>
<li><b>Rate.</b> From the definition r = R/log₂SNR:<div class="calc">R = r·log₂γ = 3 × log₂10 = 3 × 3.32 = 9.97 bit/s/Hz</div>log₂10 = 1/0.301 = 3.32. Exactly, 3 × 3.3219 = 9.966; the official answer writes 9.96 (truncated); 9.97 or 9.96 are both fine.</li>
</ol>
<h4><span class="st">Step by step</span>(b) Substitute back for the actual error rate</h4>
<p>r = 3 → d = (8 − 3)(4 − 3) = 5 → P<sub>e</sub> = γ<sup>−d</sup> = 10<sup>−5</sup>. Better than the required 10<sup>−3</sup>: r must be an integer, so it drops from 3.35 to 3, and the spare diversity shows up as a lower error rate.</p>
<h4><span class="st">Check</span>Is it reasonable?</h4>
<ul>
<li>r = 3 ≤ min(8, 4) = 4 ✓; d = 5 ≤ N × M = 32 ✓.</li>
<li>With r = 4: R = 4 × 3.32 = 13.3 bit/s/Hz is faster, but d = 0, the error rate does not fall with SNR, so the requirement fails.</li>
<li>With r = 2: d = 12, P<sub>e</sub> = 10<sup>−12</sup> is very reliable, but R = 6.64 bit/s/Hz wastes rate.</li>
</ul>
<h4><span class="st">Pitfalls</span>Where marks are lost</h4>
<ul>
<li>Not converting the SNR to linear (10 dB → 10).</li>
<li>d must be an integer: for d ≥ 3, r is rounded down to 3, not 3.35.</li>
<li>The other root of the quadratic, 8.65, exceeds min(N, M) and is meaningless.</li>
<li>R uses log₂, not log₁₀ or ln.</li>
<li>(b) asks for the P<sub>e</sub> actually obtained with r = 3 (10<sup>−5</sup>), not the required 10<sup>−3</sup>.</li>
</ul>
<h4><span class="st">Exam</span>How to write it</h4>
<div class="tmpl" lang="en"><p>(a) γ = 10 dB = 10. \(P_e=\gamma^{-d}\le10^{-3}\Rightarrow10^{-d}\le10^{-3}\Rightarrow d\ge3\).</p><p>With N = 8, M = 4: d(r) = (8 − r)(4 − r) gives d = 32, 21, 12, 5, 0 for r = 0, 1, 2, 3, 4 (r ≤ min(N, M) = 4, integer). The largest r with d ≥ 3 is r = 3.</p><p>Since \(r=R/\log_2\mathrm{SNR}\), the maximum rate is \(R=r\log_2\gamma=3\log_210\approx9.97\) bit/s/Hz.</p><p>(b) With r = 3, d = (8 − 3)(4 − 3) = 5, so \(P_e=\gamma^{-5}=10^{-5}\).</p></div>
<div class="ans">In one line: 10 dB → 10, P<sub>e</sub> ≤ 10⁻³ needs d ≥ 3 → the largest integer r with (8 − r)(4 − r) ≥ 3 is r = 3 → R = 3 log₂10 ≈ 9.97 bit/s/Hz; d(3) = 5 → P<sub>e</sub> = 10⁻⁵.</div>''',
}

# =====================================================================================  P6 Q1
XPL['p6q1'] = {
'title': '知识讲解 + 详细解析：ISI 误码率与均衡器的取舍',
'zh': r'''<h4><span class="st">知识讲解</span>ISI 信道、Z 变换和"滤波后的噪声"</h4>
<p><b>离散时间 ISI 模型</b>（第 6 章 p.22）：接收样本 = 当前符号 + 前面符号漏过来的部分（码间干扰 ISI）+ 噪声。用 Z 变换写：z⁻¹ 表示"晚一个采样"，所以 H(z) = 1 + αz⁻¹ 的意思是"当前符号 × 1 + 上一个符号 × α"。两个滤波器串联，Z 变换相乘：Q(z) = H(z)U(z)。</p>
<p><b>关键：信号和噪声走的路不一样。</b>信号先过信道 H(z) 再过均衡器 U(z)；噪声是在信道之后加进来的，<b>只过 U(z)</b>。白噪声（方差 σ²）过一个系数为 c₀, c₁, … 的 FIR 滤波器后，方差变成 σ²(c₀² + c₁² + …)（各项独立，方差相加，p.25、p.27）。老师课上强调：均衡器有几个抽头，噪声就变成几项，每项平方再相加，这就是噪声增强（noise enhancement）。</p>
<p><b>有 ISI 时的误码率</b>（p.27–28）：先固定 ISI 符号，算条件误码率 Q(信号到门限的距离 / 噪声标准差)，再按 ISI 符号每种取值的概率平均。没有 ISI 时：幅度 √E<sub>b</sub>，噪声标准差 √(N₀/2)，P<sub>e</sub> = Q(√E<sub>b</sub> / √(N₀/2)) = Q(√(2E<sub>b</sub>/N₀))。下面记 A = √(2E<sub>b</sub>/N₀)。</p>
<p><b>高 SNR 怎么比：</b>Q(x) 随 x 增大下降得极快（大约像 e<sup>−x²/2</sup>）。几个 Q 相加时，参数最小的那一项远大于其他项，误码率几乎就等于它。所以高 SNR 时只比"最坏情况的 Q 参数"。</p>
<h4><span class="st">详细解析</span>(a) 不加均衡器</h4>
<ol>
<li><b>写出判决变量。</b>z(n) = √E<sub>b</sub>(a<sub>n</sub> + α a<sub>n−1</sub>) + w(n)。</li>
<li><b>只算 a<sub>n</sub> = +1。</b>为什么：±1 等概、判决门限 0 对称，两种情况误码率一样。出错 ⇔ z(n) &lt; 0。</li>
<li><b>按上一个符号分两种情况，各占 ½。</b>a<sub>n−1</sub> = +1（同号）：均值 (1 + α)√E<sub>b</sub>，回声帮忙，P = Q((1 + α)A)；a<sub>n−1</sub> = −1（异号）：均值 (1 − α)√E<sub>b</sub>，回声捣乱，P = Q((1 − α)A)。</li>
</ol>
<div class="calc">P<sub>e</sub> = ½Q((1 − α)A) + ½Q((1 + α)A)，A = √(2E<sub>b</sub>/N₀)</div>
<h4><span class="st">详细解析</span>(a) 加均衡器 U(z) = 1 − αz⁻¹</h4>
<ol>
<li><b>信号的总响应。</b>(1 + αz⁻¹)(1 − αz⁻¹) = 1 − α²z⁻²。ISI 没有完全消掉，只是从"上一个符号 × α"变成"前两个符号 × (−α²)"，小了很多（α &lt; ½ 时 α² &lt; ¼）。原因：1/H(z) = 1 − αz⁻¹ + α²z⁻² − …（长除法），U(z) 只取了前两项，是截断的迫零均衡器。</li>
<li><b>噪声。</b>w′(n) = w(n) − αw(n − 1)，方差 = (N₀/2)(1² + α²) = (N₀/2)(1 + α²)，标准差放大 √(1 + α²) 倍。w′(n) 在相邻时刻相关，但每次判决只看一个样本，只需要它的方差。</li>
<li><b>两种情况。</b>z(n) = √E<sub>b</sub>(a<sub>n</sub> − α²a<sub>n−2</sub>) + w′(n)。a<sub>n−2</sub> = +1：幅度 (1 − α²)√E<sub>b</sub>（注意现在是同号时变差）；a<sub>n−2</sub> = −1：幅度 (1 + α²)√E<sub>b</sub>。Q 的参数 = 幅度 / 标准差 = (1 ∓ α²)√E<sub>b</sub> / √((N₀/2)(1 + α²)) = (1 ∓ α²)/√(1 + α²) · A。</li>
</ol>
<div class="calc">P<sub>e</sub> = ½Q( (1 − α²)/√(1 + α²) · A ) + ½Q( (1 + α²)/√(1 + α²) · A )</div>
<h4><span class="st">详细解析</span>(b) 高 SNR 加不加</h4>
<p>比较两种情况最坏项的 Q 参数（都去掉公共的 A）：不加是 1 − α，加是 (1 − α²)/√(1 + α²)。</p>
<div class="calc">(1 − α²)/√(1 + α²) &gt; 1 − α ⇔ (1 + α)/√(1 + α²) &gt; 1 ⇔ (1 + α)² &gt; 1 + α² ⇔ 2α &gt; 0</div>
<p>第一步两边同除以 (1 − α) &gt; 0；平方时两边都为正，不改变方向。α &gt; 0 时总成立，所以<b>加均衡器更好</b>：ISI 减小带来的好处大于噪声放大的损失。</p>
<div class="tw"><table class="mini"><thead><tr><th>α = 0.4</th><th>最坏项参数</th><th>A = 2</th><th>A = 3</th></tr></thead><tbody><tr><td>不加</td><td>0.6A</td><td>P<sub>e</sub> = 0.0588</td><td>P<sub>e</sub> = 0.0180</td></tr><tr><td>加</td><td>0.84/1.077·A = 0.78A</td><td>P<sub>e</sub> = 0.0375</td><td>P<sub>e</sub> = 0.0051</td></tr></tbody></table></div>
<p>A = 3 时，不加均衡器的 P<sub>e</sub> = 0.0180 几乎全来自 ½Q(1.8) = 0.0180，另一项 ½Q(4.2) 只有约 7 × 10⁻⁶，这就是"高 SNR 只看最坏项"。</p>
<h4><span class="st">课外补充</span>为什么题目要说"高 SNR"</h4>
<p>讲义没有这一点，是用上面的公式算的：α = 0.4 时，如果 A 小于约 1.06（E<sub>b</sub>/N₀ 低于约 −2.5 dB），不加均衡器反而略好（A = 1：不加 0.1775，加 0.1792）。噪声占主导时，均衡器放大噪声的坏处更明显。所以结论要加"高 SNR"这个前提。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>噪声只经过 U(z)，不经过 H(z)；不要把噪声方差也乘上 H(z) 的系数。</li>
<li>均衡后的残余 ISI 是 −α²，位置在 n − 2，不是 0，也不是 n − 1。</li>
<li>Q 里分母是标准差 √(1 + α²)·√(N₀/2)，不是方差。</li>
<li>只写最坏项、漏了 ½ 或漏了另一项；(a) 要的是完整表达式。</li>
<li>(b) 只给结论不给比较过程拿不到满分，要写出 2α &gt; 0 那一串。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Let \(A=\sqrt{2E_b/N_0}\). By symmetry assume \(a_n=+1\); an error occurs if \(z(n)\lt0\).</p><p>Without equaliser: \(z(n)=\sqrt{E_b}(a_n+\alpha a_{n-1})+w(n)\), noise variance \(N_0/2\). With \(a_{n-1}=\pm1\) (prob. ½ each) the amplitude is \((1\pm\alpha)\sqrt{E_b}\): \(P_e=\tfrac12Q((1-\alpha)A)+\tfrac12Q((1+\alpha)A)\).</p><p>With equaliser: signal response \(H(z)U(z)=1-\alpha^2z^{-2}\); the noise passes through U(z) only, \(w'(n)=w(n)-\alpha w(n-1)\), variance \(\tfrac{N_0}{2}(1+\alpha^2)\). Amplitudes \((1\mp\alpha^2)\sqrt{E_b}\): \(P_e=\tfrac12Q\big(\tfrac{1-\alpha^2}{\sqrt{1+\alpha^2}}A\big)+\tfrac12Q\big(\tfrac{1+\alpha^2}{\sqrt{1+\alpha^2}}A\big)\).</p><p>(b) At high SNR \(P_e\) is dominated by the smallest Q argument. \(\tfrac{1-\alpha^2}{\sqrt{1+\alpha^2}}\gt1-\alpha\Leftrightarrow(1+\alpha)^2\gt1+\alpha^2\Leftrightarrow2\alpha\gt0\), true for α &gt; 0. Hence it is better to operate with the equaliser: the reduction in ISI outweighs the noise enhancement.</p></div>
<div class="ans">一句话：不加：½Q((1 − α)A) + ½Q((1 + α)A)；加 1 − αz⁻¹：ISI 变成 −α²、噪声方差乘 (1 + α²)，½Q((1 − α²)A/√(1 + α²)) + ½Q((1 + α²)A/√(1 + α²))；高 SNR 比最坏项，(1 + α)² &gt; 1 + α²，加均衡器更好。</div>''',
'title_en': 'Concept + walkthrough: ISI error rate, equaliser trade-off',
'en': r'''<h4><span class="st">Concept</span>ISI channel, Z-transform and "filtered noise"</h4>
<p><b>Discrete-time ISI model</b> (Ch 6 p.22): received sample = current symbol + leakage from earlier symbols (inter-symbol interference, ISI) + noise. In Z-transform notation z⁻¹ means "one sample later", so H(z) = 1 + αz⁻¹ means "current symbol × 1 + previous symbol × α". Two filters in cascade multiply their Z-transforms: Q(z) = H(z)U(z).</p>
<p><b>Key point: signal and noise take different paths.</b> The signal goes through the channel H(z) and then the equaliser U(z); the noise is added after the channel and goes <b>only through U(z)</b>. White noise (variance σ²) through an FIR filter with coefficients c₀, c₁, … has variance σ²(c₀² + c₁² + …) (independent terms, variances add; p.25, p.27). Lecturer's emphasis: the noise becomes as many terms as the equaliser has taps; square each and add to get the output noise power. This is noise enhancement.</p>
<p><b>Error rate with ISI</b> (p.27–28): first fix the ISI symbols and compute the conditional error rate Q(distance from signal to threshold / noise standard deviation), then average over the probabilities of the ISI symbol values. Without ISI: amplitude √E<sub>b</sub>, noise standard deviation √(N₀/2), P<sub>e</sub> = Q(√E<sub>b</sub> / √(N₀/2)) = Q(√(2E<sub>b</sub>/N₀)). Below, A = √(2E<sub>b</sub>/N₀).</p>
<p><b>How to compare at high SNR:</b> Q(x) falls extremely fast as x grows (roughly like e<sup>−x²/2</sup>). In a sum of Q terms the one with the smallest argument is far larger than the others and the error rate is essentially that term. So at high SNR we compare only the "worst-case Q arguments".</p>
<h4><span class="st">Step by step</span>(a) Without the equaliser</h4>
<ol>
<li><b>Write the decision variable.</b> z(n) = √E<sub>b</sub>(a<sub>n</sub> + α a<sub>n−1</sub>) + w(n).</li>
<li><b>Take only a<sub>n</sub> = +1.</b> Why: ±1 are equally likely and the threshold 0 is symmetric, so both cases have the same error rate. Error ⇔ z(n) &lt; 0.</li>
<li><b>Two cases for the previous symbol, ½ each.</b> a<sub>n−1</sub> = +1 (same sign): mean (1 + α)√E<sub>b</sub>, the echo helps, P = Q((1 + α)A); a<sub>n−1</sub> = −1 (opposite sign): mean (1 − α)√E<sub>b</sub>, the echo hurts, P = Q((1 − α)A).</li>
</ol>
<div class="calc">P<sub>e</sub> = ½Q((1 − α)A) + ½Q((1 + α)A), A = √(2E<sub>b</sub>/N₀)</div>
<h4><span class="st">Step by step</span>(a) With the equaliser U(z) = 1 − αz⁻¹</h4>
<ol>
<li><b>Overall signal response.</b> (1 + αz⁻¹)(1 − αz⁻¹) = 1 − α²z⁻². The ISI is not removed completely; it changes from "previous symbol × α" to "symbol two back × (−α²)", much smaller (α &lt; ½ gives α² &lt; ¼). Reason: 1/H(z) = 1 − αz⁻¹ + α²z⁻² − … (long division), and U(z) keeps only the first two terms: a truncated zero-forcing equaliser.</li>
<li><b>Noise.</b> w′(n) = w(n) − αw(n − 1), variance = (N₀/2)(1² + α²) = (N₀/2)(1 + α²); the standard deviation grows by √(1 + α²). w′(n) is correlated between neighbouring instants, but each decision uses one sample, so only its variance matters.</li>
<li><b>Two cases.</b> z(n) = √E<sub>b</sub>(a<sub>n</sub> − α²a<sub>n−2</sub>) + w′(n). a<sub>n−2</sub> = +1: amplitude (1 − α²)√E<sub>b</sub> (note: now the same sign is the bad case); a<sub>n−2</sub> = −1: amplitude (1 + α²)√E<sub>b</sub>. Q argument = amplitude / standard deviation = (1 ∓ α²)√E<sub>b</sub> / √((N₀/2)(1 + α²)) = (1 ∓ α²)/√(1 + α²) · A.</li>
</ol>
<div class="calc">P<sub>e</sub> = ½Q( (1 − α²)/√(1 + α²) · A ) + ½Q( (1 + α²)/√(1 + α²) · A )</div>
<h4><span class="st">Step by step</span>(b) With or without at high SNR</h4>
<p>Compare the worst-case Q arguments (dropping the common A): without, 1 − α; with, (1 − α²)/√(1 + α²).</p>
<div class="calc">(1 − α²)/√(1 + α²) &gt; 1 − α ⇔ (1 + α)/√(1 + α²) &gt; 1 ⇔ (1 + α)² &gt; 1 + α² ⇔ 2α &gt; 0</div>
<p>The first step divides both sides by (1 − α) &gt; 0; squaring keeps the direction because both sides are positive. This holds for every α &gt; 0, so it is <b>better with the equaliser</b>: the gain from less ISI outweighs the loss from noise enhancement.</p>
<div class="tw"><table class="mini"><thead><tr><th>α = 0.4</th><th>Worst-case argument</th><th>A = 2</th><th>A = 3</th></tr></thead><tbody><tr><td>Without</td><td>0.6A</td><td>P<sub>e</sub> = 0.0588</td><td>P<sub>e</sub> = 0.0180</td></tr><tr><td>With</td><td>0.84/1.077·A = 0.78A</td><td>P<sub>e</sub> = 0.0375</td><td>P<sub>e</sub> = 0.0051</td></tr></tbody></table></div>
<p>At A = 3, the no-equaliser P<sub>e</sub> = 0.0180 comes almost entirely from ½Q(1.8) = 0.0180; the other term ½Q(4.2) is only about 7 × 10⁻⁶. This is "at high SNR only the worst term matters".</p>
<h4><span class="st">Extra (not in the slides)</span>Why the question says "high SNR"</h4>
<p>Not in the slides; computed from the formulas above: with α = 0.4, if A is below about 1.06 (E<sub>b</sub>/N₀ below about −2.5 dB), the system is slightly better without the equaliser (A = 1: 0.1775 without, 0.1792 with). When noise dominates, the noise enhancement hurts more. Hence the conclusion needs the "high SNR" condition.</p>
<h4><span class="st">Pitfalls</span>Where marks are lost</h4>
<ul>
<li>The noise goes through U(z) only, not H(z); do not multiply the noise variance by the coefficients of H(z).</li>
<li>After equalisation the residual ISI is −α² at position n − 2, not 0 and not at n − 1.</li>
<li>The denominator inside Q is the standard deviation √(1 + α²)·√(N₀/2), not the variance.</li>
<li>Writing only the worst term, or dropping the ½ or the other term; (a) asks for the full expression.</li>
<li>In (b) a bare conclusion without the comparison does not earn full marks; write out the chain down to 2α &gt; 0.</li>
</ul>
<h4><span class="st">Exam</span>How to write it</h4>
<div class="tmpl" lang="en"><p>Let \(A=\sqrt{2E_b/N_0}\). By symmetry assume \(a_n=+1\); an error occurs if \(z(n)\lt0\).</p><p>Without equaliser: \(z(n)=\sqrt{E_b}(a_n+\alpha a_{n-1})+w(n)\), noise variance \(N_0/2\). With \(a_{n-1}=\pm1\) (prob. ½ each) the amplitude is \((1\pm\alpha)\sqrt{E_b}\): \(P_e=\tfrac12Q((1-\alpha)A)+\tfrac12Q((1+\alpha)A)\).</p><p>With equaliser: signal response \(H(z)U(z)=1-\alpha^2z^{-2}\); the noise passes through U(z) only, \(w'(n)=w(n)-\alpha w(n-1)\), variance \(\tfrac{N_0}{2}(1+\alpha^2)\). Amplitudes \((1\mp\alpha^2)\sqrt{E_b}\): \(P_e=\tfrac12Q\big(\tfrac{1-\alpha^2}{\sqrt{1+\alpha^2}}A\big)+\tfrac12Q\big(\tfrac{1+\alpha^2}{\sqrt{1+\alpha^2}}A\big)\).</p><p>(b) At high SNR \(P_e\) is dominated by the smallest Q argument. \(\tfrac{1-\alpha^2}{\sqrt{1+\alpha^2}}\gt1-\alpha\Leftrightarrow(1+\alpha)^2\gt1+\alpha^2\Leftrightarrow2\alpha\gt0\), true for α &gt; 0. Hence it is better to operate with the equaliser: the reduction in ISI outweighs the noise enhancement.</p></div>
<div class="ans">In one line: without: ½Q((1 − α)A) + ½Q((1 + α)A); with 1 − αz⁻¹: ISI becomes −α² and the noise variance is multiplied by (1 + α²), giving ½Q((1 − α²)A/√(1 + α²)) + ½Q((1 + α²)A/√(1 + α²)); at high SNR compare the worst terms, (1 + α)² &gt; 1 + α², so the equaliser is better.</div>''',
}

# =====================================================================================  P6 Q2
XPL['p6q2'] = {
'title': '知识讲解 + 详细解析：直接判决 vs 理想迫零均衡',
'zh': r'''<h4><span class="st">知识讲解</span>迫零均衡器（ZF）和噪声放大</h4>
<p><b>迫零（zero-forcing）</b>的目标是把 ISI 压到零（第 6 章 p.23）：让信道和均衡器串起来的总响应等于 1，即 H(z)C(z) = 1，C(z) = 1/H(z)。"理想"迫零就是这个逆滤波器的所有抽头都用上，输出完全没有 ISI。</p>
<p><b>怎么求 1/H(z)：长除法</b>（p.24 例题；老师课上强调：迫零的长除法必须会）。1 除以 (1 + az⁻¹)：</p>
<ol>
<li>商的第一项 1：1 − 1·(1 + az⁻¹) = −az⁻¹（余数）。</li>
<li>商的第二项 −az⁻¹：−az⁻¹ − (−az⁻¹)(1 + az⁻¹) = a²z⁻²。</li>
<li>商的第三项 a²z⁻²，余数 −a³z⁻³ ……每次乘 −a。</li>
</ol>
<div class="calc">C(z) = 1/(1 + az⁻¹) = 1 − az⁻¹ + a²z⁻² − a³z⁻³ + … = Σ<sub>k≥0</sub> (−a)<sup>k</sup>z<sup>−k</sup></div>
<p>|a| &lt; 1 时这个无穷级数收敛。抽头有无穷多个，实际只能取前几个（取前两个就是 P6 Q1 的 1 − αz⁻¹）。</p>
<p><b>噪声放大</b>：噪声只过 C(z)，方差 = σ² × 系数平方和（p.25、p.27）。等比级数 1 + a² + a⁴ + … = 1/(1 − a²)，所以输出噪声方差 = σ²/(1 − a²)，比 σ² 大；a 越接近 1，放大越厉害。老师说：迫零只管 ISI、不管噪声，所以在 p.35 的比较图里它最差。</p>
<h4><span class="st">详细解析</span>(a) 直接按 y<sub>n</sub> 的正负判决</h4>
<ol>
<li><b>只算 b<sub>n</sub> = +1。</b>±1 对称，误码率一样；出错 ⇔ y<sub>n</sub> &lt; 0。</li>
<li><b>按上一个比特分两种情况，各 ½。</b>b<sub>n−1</sub> = +1：y<sub>n</sub> = 1 + a + w<sub>n</sub>，离门限 1 + a；b<sub>n−1</sub> = −1：离门限 1 − a。</li>
<li><b>噪声标准差。</b>方差 0.1 → 标准差 √0.1 = 0.316。P(1 + a + w &lt; 0) = P(w &lt; −(1 + a)) = Q((1 + a)/√0.1)。</li>
</ol>
<div class="calc">P<sub>e</sub> = ½Q((1 + a)/√0.1) + ½Q((1 − a)/√0.1)</div>
<h4><span class="st">详细解析</span>(b) 理想迫零后判决</h4>
<ol>
<li><b>信号：</b>H(z)C(z) = 1，输出就是 b<sub>n</sub>，没有 ISI，不用再分情况。</li>
<li><b>噪声：</b>w<sub>n</sub> 过 C(z)，系数 1, −a, a², −a³, …，平方和 1 + a² + a⁴ + … = 1/(1 − a²)：<div class="calc">输出噪声方差 = 0.1/(1 − a²)</div></li>
<li><b>误码率：</b>距离 1，标准差 √(0.1/(1 − a²))：<div class="calc">P<sub>e</sub> = Q(1/√(0.1/(1 − a²))) = Q(√((1 − a²)/0.1))</div></li>
</ol>
<h4><span class="st">自检</span>代数字比一比</h4>
<div class="tw"><table class="mini"><thead><tr><th>a</th><th>(a) 直接判决</th><th>(b) 理想迫零</th><th>噪声放大 1/(1 − a²)</th></tr></thead><tbody><tr><td>0.5</td><td>½Q(4.74) + ½Q(1.58) ≈ 0.0285</td><td>Q(2.74) ≈ 0.0031</td><td>1.33</td></tr><tr><td>0.9</td><td>½Q(6.01) + ½Q(0.316) ≈ 0.188</td><td>Q(1.38) ≈ 0.084</td><td>5.26</td></tr></tbody></table></div>
<p>a = 0.5 时迫零好约 9 倍。一般地，高 SNR 时比最坏项的 Q 参数：迫零 √(1 − a²)/√0.1，直接判决 (1 − a)/√0.1。√(1 − a²) = √((1 − a)(1 + a)) &gt; √((1 − a)(1 − a)) = 1 − a，所以理想迫零总是更好；但 a → 1 时噪声放大 1/(1 − a²) 趋于无穷，迫零的绝对性能也会很差。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>0.1 是方差，Q 里除的是标准差 √0.1。</li>
<li>迫零后没有 ISI，只剩一项 Q，不要再分两种情况。</li>
<li>噪声方差要乘系数<b>平方</b>和 1/(1 − a²)，不是系数和 1/(1 + a)。</li>
<li>(a) 别只写最坏项 Q((1 − a)/√0.1)，两项都要、各乘 ½。</li>
<li>"理想"迫零是无穷多抽头；如果题目说只取两个抽头，就变成 P6 Q1 那样有残余 ISI。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(a) By symmetry take \(b_n=+1\). With \(b_{n-1}=\pm1\) (prob. ½ each), \(y_n=1\pm a+w_n\) and the noise standard deviation is \(\sqrt{0.1}\), so \(P_e=\tfrac12Q\big(\tfrac{1+a}{\sqrt{0.1}}\big)+\tfrac12Q\big(\tfrac{1-a}{\sqrt{0.1}}\big)\).</p><p>(b) The ideal ZF equaliser is \(C(z)=1/H(z)=1/(1+az^{-1})=\sum_{k\ge0}(-a)^kz^{-k}\) (|a| \(\lt\) 1). The output is \(b_n\) plus filtered noise with no ISI.</p><p>Output noise variance \(=0.1\sum_{k\ge0}a^{2k}=\dfrac{0.1}{1-a^2}\) (noise enhancement), so \(P_e=Q\Big(\sqrt{\dfrac{1-a^2}{0.1}}\Big)\).</p></div>
<div class="ans">一句话：(a) 上一个比特同号 / 异号各 ½：½Q((1 + a)/√0.1) + ½Q((1 − a)/√0.1)；(b) 理想迫零 C = 1/(1 + az⁻¹) = Σ(−a)<sup>k</sup>z<sup>−k</sup>，ISI 为零但噪声方差变成 0.1/(1 − a²)：P<sub>e</sub> = Q(√((1 − a²)/0.1))。</div>''',
'title_en': 'Concept + walkthrough: direct decision vs ideal ZF',
'en': r'''<h4><span class="st">Concept</span>Zero-forcing (ZF) equaliser and noise enhancement</h4>
<p>The goal of <b>zero forcing</b> is to drive the ISI to zero (Ch 6 p.23): make the cascade of channel and equaliser equal to 1, i.e. H(z)C(z) = 1, C(z) = 1/H(z). "Ideal" zero forcing uses all taps of this inverse filter, so the output has no ISI at all.</p>
<p><b>How to find 1/H(z): long division</b> (example on p.24; lecturer's emphasis: ZF long division is a must). Divide 1 by (1 + az⁻¹):</p>
<ol>
<li>First quotient term 1: 1 − 1·(1 + az⁻¹) = −az⁻¹ (remainder).</li>
<li>Second quotient term −az⁻¹: −az⁻¹ − (−az⁻¹)(1 + az⁻¹) = a²z⁻².</li>
<li>Third quotient term a²z⁻², remainder −a³z⁻³ … each step multiplies by −a.</li>
</ol>
<div class="calc">C(z) = 1/(1 + az⁻¹) = 1 − az⁻¹ + a²z⁻² − a³z⁻³ + … = Σ<sub>k≥0</sub> (−a)<sup>k</sup>z<sup>−k</sup></div>
<p>For |a| &lt; 1 this infinite series converges. It has infinitely many taps; in practice only the first few are used (the first two give the 1 − αz⁻¹ of P6 Q1).</p>
<p><b>Noise enhancement</b>: the noise passes only through C(z), so its variance = σ² × sum of squared coefficients (p.25, p.27). The geometric series 1 + a² + a⁴ + … = 1/(1 − a²), so the output noise variance is σ²/(1 − a²), larger than σ²; the closer a is to 1, the worse. The lecturer says ZF only cares about ISI, not noise, which is why it is the worst in the comparison figure on p.35.</p>
<h4><span class="st">Step by step</span>(a) Decide directly on the sign of y<sub>n</sub></h4>
<ol>
<li><b>Take only b<sub>n</sub> = +1.</b> ±1 are symmetric, same error rate; error ⇔ y<sub>n</sub> &lt; 0.</li>
<li><b>Two cases for the previous bit, ½ each.</b> b<sub>n−1</sub> = +1: y<sub>n</sub> = 1 + a + w<sub>n</sub>, distance 1 + a from the threshold; b<sub>n−1</sub> = −1: distance 1 − a.</li>
<li><b>Noise standard deviation.</b> Variance 0.1 → standard deviation √0.1 = 0.316. P(1 + a + w &lt; 0) = P(w &lt; −(1 + a)) = Q((1 + a)/√0.1).</li>
</ol>
<div class="calc">P<sub>e</sub> = ½Q((1 + a)/√0.1) + ½Q((1 − a)/√0.1)</div>
<h4><span class="st">Step by step</span>(b) Decide after ideal zero forcing</h4>
<ol>
<li><b>Signal:</b> H(z)C(z) = 1, the output is just b<sub>n</sub>, no ISI, no case split.</li>
<li><b>Noise:</b> w<sub>n</sub> goes through C(z) with coefficients 1, −a, a², −a³, …; sum of squares 1 + a² + a⁴ + … = 1/(1 − a²):<div class="calc">Output noise variance = 0.1/(1 − a²)</div></li>
<li><b>Error rate:</b> distance 1, standard deviation √(0.1/(1 − a²)):<div class="calc">P<sub>e</sub> = Q(1/√(0.1/(1 − a²))) = Q(√((1 − a²)/0.1))</div></li>
</ol>
<h4><span class="st">Check</span>Compare with numbers</h4>
<div class="tw"><table class="mini"><thead><tr><th>a</th><th>(a) Direct decision</th><th>(b) Ideal ZF</th><th>Noise enhancement 1/(1 − a²)</th></tr></thead><tbody><tr><td>0.5</td><td>½Q(4.74) + ½Q(1.58) ≈ 0.0285</td><td>Q(2.74) ≈ 0.0031</td><td>1.33</td></tr><tr><td>0.9</td><td>½Q(6.01) + ½Q(0.316) ≈ 0.188</td><td>Q(1.38) ≈ 0.084</td><td>5.26</td></tr></tbody></table></div>
<p>At a = 0.5 ZF is about 9 times better. In general, at high SNR compare the worst-case Q arguments: ZF √(1 − a²)/√0.1, direct decision (1 − a)/√0.1. √(1 − a²) = √((1 − a)(1 + a)) &gt; √((1 − a)(1 − a)) = 1 − a, so ideal ZF is always better; but as a → 1 the noise enhancement 1/(1 − a²) goes to infinity and ZF's absolute performance also becomes poor.</p>
<h4><span class="st">Pitfalls</span>Where marks are lost</h4>
<ul>
<li>0.1 is the variance; inside Q divide by the standard deviation √0.1.</li>
<li>After ZF there is no ISI, only one Q term; do not split into two cases.</li>
<li>The noise variance is multiplied by the sum of <b>squared</b> coefficients 1/(1 − a²), not the plain sum 1/(1 + a).</li>
<li>In (a) do not write only the worst term Q((1 − a)/√0.1); both terms are needed, each times ½.</li>
<li>"Ideal" ZF has infinitely many taps; if a question keeps only two taps, residual ISI remains as in P6 Q1.</li>
</ul>
<h4><span class="st">Exam</span>How to write it</h4>
<div class="tmpl" lang="en"><p>(a) By symmetry take \(b_n=+1\). With \(b_{n-1}=\pm1\) (prob. ½ each), \(y_n=1\pm a+w_n\) and the noise standard deviation is \(\sqrt{0.1}\), so \(P_e=\tfrac12Q\big(\tfrac{1+a}{\sqrt{0.1}}\big)+\tfrac12Q\big(\tfrac{1-a}{\sqrt{0.1}}\big)\).</p><p>(b) The ideal ZF equaliser is \(C(z)=1/H(z)=1/(1+az^{-1})=\sum_{k\ge0}(-a)^kz^{-k}\) (|a| \(\lt\) 1). The output is \(b_n\) plus filtered noise with no ISI.</p><p>Output noise variance \(=0.1\sum_{k\ge0}a^{2k}=\dfrac{0.1}{1-a^2}\) (noise enhancement), so \(P_e=Q\Big(\sqrt{\dfrac{1-a^2}{0.1}}\Big)\).</p></div>
<div class="ans">In one line: (a) previous bit same / opposite sign, ½ each: ½Q((1 + a)/√0.1) + ½Q((1 − a)/√0.1); (b) ideal ZF C = 1/(1 + az⁻¹) = Σ(−a)<sup>k</sup>z<sup>−k</sup> removes all ISI but the noise variance becomes 0.1/(1 − a²): P<sub>e</sub> = Q(√((1 − a²)/0.1)).</div>''',
}

# =====================================================================================  P6 Q3
XPL['p6q3'] = {
'title': '知识讲解 + 详细解析：MMSE 均衡与 DFE 错误传播',
'zh': r'''<h4><span class="st">知识讲解</span>MMSE 准则和判决反馈均衡（DFE）</h4>
<p><b>MMSE（最小均方误差，minimum mean-square error）</b>（第 6 章 p.26）：选均衡器系数，让输出和真实符号的差的平方的平均值 E[(u<sub>n</sub> − A<sub>n</sub>)²] 最小。它同时考虑 ISI 和噪声，不像迫零只管 ISI。</p>
<p>求法的关键工具：如果 X₁, X₂, … 相互独立、均值都是 0，那么 E[(X₁ + X₂ + …)²] = E[X₁²] + E[X₂²] + …（交叉项的期望都是 0）。这里 A<sub>n</sub>² = 1，噪声 E[z²] = σ² = 1。</p>
<p><b>DFE（decision-feedback equalizer）</b>（p.29–34）：前馈部分处理"未来"符号的 ISI，反馈部分用<b>已经判出来的过去符号</b>把它们的 ISI 直接减掉。好处：减法不经过滤波器，不会放大噪声。坏处：如果上一次判错，减掉的是错的值，ISI 反而变大，下一次更容易错，叫<b>错误传播（error propagation，p.34）</b>。老师课上强调：DFE 不用从头推到尾，但要知道两个滤波器各管什么，这类题"靠逻辑多于靠记忆"。</p>
<p><b>长期误码率</b>：第 n 次出错的概率取决于第 n − 1 次对不对（全概率公式）：p<sub>n</sub> = P(错 | 上次对)(1 − p<sub>n−1</sub>) + P(错 | 上次错)p<sub>n−1</sub>。n → ∞ 时 p<sub>n</sub> = p<sub>n−1</sub> = p，解一个一次方程就行。</p>
<h4><span class="st">详细解析</span>(a) 求最优 q 和误码率</h4>
<ol>
<li><b>展开 u<sub>n</sub>。</b>y<sub>n</sub> = A<sub>n</sub> + ½A<sub>n−1</sub> + z<sub>n</sub>，y<sub>n+1</sub> = A<sub>n+1</sub> + ½A<sub>n</sub> + z<sub>n+1</sub>，所以<div class="calc">u<sub>n</sub> − A<sub>n</sub> = (q/2)A<sub>n</sub> + ½A<sub>n−1</sub> + qA<sub>n+1</sub> + z<sub>n</sub> + qz<sub>n+1</sub></div>注意 (q/2)A<sub>n</sub>：u<sub>n</sub> 里 A<sub>n</sub> 的系数是 1 + q/2，多出来的 q/2 也算误差。</li>
<li><b>求均方误差。</b>五项独立、均值 0，平方的期望直接相加：<div class="calc">E[(u<sub>n</sub> − A<sub>n</sub>)²] = q²/4 + 1/4 + q² + 1 + q² = 1.25 + 2.25q²</div></li>
<li><b>求最小。</b>对 q 求导：4.5q = 0 → q = 0，最小均方误差 1.25。直观理由：y<sub>n+1</sub> 里只有 A<sub>n+1</sub>、A<sub>n</sub> 和 z<sub>n+1</sub>，<b>根本不含 A<sub>n−1</sub></b>，没法抵消 ½A<sub>n−1</sub> 这个 ISI；它带进来的全是新的误差，所以最好不用它。</li>
<li><b>误码率。</b>q = 0 时 u<sub>n</sub> = y<sub>n</sub>。设 A<sub>n</sub> = +1：A<sub>n−1</sub> = +1 时幅度 1.5，A<sub>n−1</sub> = −1 时幅度 0.5，噪声标准差 1：<div class="calc">P<sub>e</sub> = ½Q(1.5) + ½Q(0.5) = ½(0.0668) + ½(0.3085) = 0.188 ≈ 0.19</div></li>
</ol>
<h4><span class="st">详细解析</span>(b) DFE 的长期误码率</h4>
<ol>
<li><b>写出判决变量。</b>u<sub>n</sub> = y<sub>n</sub> − ½Â<sub>n−1</sub> = A<sub>n</sub> + ½(A<sub>n−1</sub> − Â<sub>n−1</sub>) + z<sub>n</sub>。</li>
<li><b>上一次判对</b>（Â<sub>n−1</sub> = A<sub>n−1</sub>）：括号为 0，u<sub>n</sub> = A<sub>n</sub> + z<sub>n</sub>，ISI 被完全减掉：<div class="calc">P(错 | 上次对) = Q(1) = 0.159</div></li>
<li><b>上一次判错</b>（Â<sub>n−1</sub> = −A<sub>n−1</sub>）：括号 = 2A<sub>n−1</sub>，u<sub>n</sub> = A<sub>n</sub> + A<sub>n−1</sub> + z<sub>n</sub>，ISI 从 ½ 变成 1（加倍）。设 A<sub>n</sub> = +1：同号时幅度 2，出错 Q(2) = 0.0228；异号时幅度 0，纯靠噪声正负，出错 ½。两种各 ½（A<sub>n</sub> 和过去无关）：<div class="calc">P(错 | 上次错) = ½Q(2) + ½ × ½ = 0.0114 + 0.25 = 0.261</div></li>
<li><b>列稳态方程。</b><div class="calc">p = (1 − p) × 0.159 + p × 0.261 → p(1 − 0.261 + 0.159) = 0.159 → p = 0.159/0.898 = 0.177 ≈ 0.18</div></li>
</ol>
<p>"时间从 n = 1 开始、A₀ = 0"的作用：第一个符号前面没有 ISI，p₁ = Q(1) = 0.159。之后按上面的递推：p₂ = 0.175，p₃ = 0.1766，p₄ = 0.1768，很快收敛到 0.177。</p>
<h4><span class="st">自检</span>三个数排个队</h4>
<div class="tw"><table class="mini"><thead><tr><th>方法</th><th>P<sub>e</sub></th><th>原因</th></tr></thead><tbody><tr><td>线性 MMSE（q = 0）</td><td>0.188</td><td>ISI 完全没处理</td></tr><tr><td>DFE（有错误传播）</td><td>0.177</td><td>大部分时间 ISI 被减掉</td></tr><tr><td>DFE（假设反馈永远对）</td><td>0.159 = Q(1)</td><td>相当于没有 ISI</td></tr></tbody></table></div>
<p>DFE 比线性好，因为它不放大噪声；但错误传播吃掉了一部分优势（0.159 → 0.177）。p 一定在 0.159 和 0.261 之间，0.177 合理。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>展开时漏了 (q/2)A<sub>n</sub> 项，均方误差会算错。</li>
<li>以为"均衡器总会有用"，硬求出一个非零 q。这里 q = 0 才对，题目就是想考这一点。</li>
<li>上次判错时 ISI 是加倍（幅度 2 或 0），不是消失；幅度为 0 时误码率是 ½，不是 0 也不是 1。</li>
<li>稳态方程移项出错：p 的系数是 1 − 0.261 + 0.159，不是 1 − 0.261 − 0.159。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(a) \(u_n-A_n=\tfrac q2A_n+\tfrac12A_{n-1}+qA_{n+1}+z_n+qz_{n+1}\). The terms are independent and zero-mean, so \(E[(u_n-A_n)^2]=\tfrac{q^2}{4}+\tfrac14+q^2+1+q^2=1.25+2.25q^2\), minimised at q = 0.</p><p>Then \(u_n=y_n\); for \(A_n=+1\) the amplitude is 1.5 or 0.5 with prob. ½ each: \(P_e=\tfrac12Q(1.5)+\tfrac12Q(0.5)=\tfrac12(0.0668)+\tfrac12(0.3085)\approx0.19\).</p><p>(b) \(u_n=A_n+\tfrac12(A_{n-1}-\hat A_{n-1})+z_n\). If the previous decision is correct, \(u_n=A_n+z_n\) and \(P(e\mid c)=Q(1)=0.159\). If it is wrong, \(u_n=A_n+A_{n-1}+z_n\) (amplitude 2 or 0), so \(P(e\mid e)=\tfrac12Q(2)+\tfrac12\cdot\tfrac12=0.261\).</p><p>In steady state \(p=(1-p)(0.159)+p(0.261)\Rightarrow p=\dfrac{0.159}{1-0.261+0.159}\approx0.18\). Error propagation raises \(P_e\) above Q(1), but the DFE still beats the linear equaliser.</p></div>
<div class="ans">一句话：(a) 均方误差 1.25 + 2.25q²，y<sub>n+1</sub> 帮不上忙 → q = 0，P<sub>e</sub> = ½Q(1.5) + ½Q(0.5) ≈ 0.19；(b) 上次对 → Q(1)，上次错 → ½Q(2) + ¼，稳态 p = 0.159/(1 − 0.261 + 0.159) ≈ 0.18。</div>''',
'title_en': 'Concept + walkthrough: MMSE linear eq. vs DFE',
'en': r'''<h4><span class="st">Concept</span>The MMSE criterion and the decision-feedback equaliser (DFE)</h4>
<p><b>MMSE (minimum mean-square error)</b> (Ch 6 p.26): choose the equaliser coefficients to minimise the average squared difference between the output and the true symbol, E[(u<sub>n</sub> − A<sub>n</sub>)²]. It accounts for both ISI and noise, unlike zero forcing, which only cares about ISI.</p>
<p>The key tool: if X₁, X₂, … are independent with zero mean, then E[(X₁ + X₂ + …)²] = E[X₁²] + E[X₂²] + … (all cross terms have zero expectation). Here A<sub>n</sub>² = 1 and the noise has E[z²] = σ² = 1.</p>
<p><b>DFE (decision-feedback equaliser)</b> (p.29–34): the feedforward part handles ISI from "future" symbols; the feedback part uses <b>past symbols that have already been decided</b> to subtract their ISI directly. Advantage: the subtraction does not pass through a filter, so the noise is not enhanced. Drawback: if the previous decision was wrong, the wrong value is subtracted and the ISI grows, making the next decision more likely to fail: <b>error propagation (p.34)</b>. Lecturer's emphasis: you need not derive the DFE end to end, but you must know what each filter does; such questions rely "more on logic than on memory".</p>
<p><b>Long-run error rate</b>: the probability of an error at time n depends on whether decision n − 1 was right (total probability): p<sub>n</sub> = P(error | previous correct)(1 − p<sub>n−1</sub>) + P(error | previous wrong)p<sub>n−1</sub>. As n → ∞, p<sub>n</sub> = p<sub>n−1</sub> = p, and one linear equation gives p.</p>
<h4><span class="st">Step by step</span>(a) Optimal q and error rate</h4>
<ol>
<li><b>Expand u<sub>n</sub>.</b> y<sub>n</sub> = A<sub>n</sub> + ½A<sub>n−1</sub> + z<sub>n</sub>, y<sub>n+1</sub> = A<sub>n+1</sub> + ½A<sub>n</sub> + z<sub>n+1</sub>, so<div class="calc">u<sub>n</sub> − A<sub>n</sub> = (q/2)A<sub>n</sub> + ½A<sub>n−1</sub> + qA<sub>n+1</sub> + z<sub>n</sub> + qz<sub>n+1</sub></div>Note the (q/2)A<sub>n</sub>: the coefficient of A<sub>n</sub> in u<sub>n</sub> is 1 + q/2, and the extra q/2 also counts as error.</li>
<li><b>Mean-square error.</b> Five independent zero-mean terms, so the squared expectations simply add:<div class="calc">E[(u<sub>n</sub> − A<sub>n</sub>)²] = q²/4 + 1/4 + q² + 1 + q² = 1.25 + 2.25q²</div></li>
<li><b>Minimise.</b> Differentiate with respect to q: 4.5q = 0 → q = 0, minimum MSE 1.25. Intuition: y<sub>n+1</sub> contains only A<sub>n+1</sub>, A<sub>n</sub> and z<sub>n+1</sub> and <b>does not contain A<sub>n−1</sub> at all</b>, so it cannot cancel the ISI term ½A<sub>n−1</sub>; everything it brings in is new error, so it is best not to use it.</li>
<li><b>Error rate.</b> With q = 0, u<sub>n</sub> = y<sub>n</sub>. Take A<sub>n</sub> = +1: amplitude 1.5 if A<sub>n−1</sub> = +1, 0.5 if A<sub>n−1</sub> = −1; noise standard deviation 1:<div class="calc">P<sub>e</sub> = ½Q(1.5) + ½Q(0.5) = ½(0.0668) + ½(0.3085) = 0.188 ≈ 0.19</div></li>
</ol>
<h4><span class="st">Step by step</span>(b) Long-run error rate of the DFE</h4>
<ol>
<li><b>Write the decision variable.</b> u<sub>n</sub> = y<sub>n</sub> − ½Â<sub>n−1</sub> = A<sub>n</sub> + ½(A<sub>n−1</sub> − Â<sub>n−1</sub>) + z<sub>n</sub>.</li>
<li><b>Previous decision correct</b> (Â<sub>n−1</sub> = A<sub>n−1</sub>): the bracket is 0, u<sub>n</sub> = A<sub>n</sub> + z<sub>n</sub>, the ISI is removed completely:<div class="calc">P(error | previous correct) = Q(1) = 0.159</div></li>
<li><b>Previous decision wrong</b> (Â<sub>n−1</sub> = −A<sub>n−1</sub>): the bracket is 2A<sub>n−1</sub>, u<sub>n</sub> = A<sub>n</sub> + A<sub>n−1</sub> + z<sub>n</sub>, the ISI grows from ½ to 1 (doubles). Take A<sub>n</sub> = +1: same sign gives amplitude 2, error Q(2) = 0.0228; opposite sign gives amplitude 0, decided purely by the sign of the noise, error ½. Each case has prob. ½ (A<sub>n</sub> is independent of the past):<div class="calc">P(error | previous wrong) = ½Q(2) + ½ × ½ = 0.0114 + 0.25 = 0.261</div></li>
<li><b>Steady-state equation.</b><div class="calc">p = (1 − p) × 0.159 + p × 0.261 → p(1 − 0.261 + 0.159) = 0.159 → p = 0.159/0.898 = 0.177 ≈ 0.18</div></li>
</ol>
<p>What "time starts at n = 1 and A₀ = 0" does: the first symbol has no ISI, so p₁ = Q(1) = 0.159. Then by the recursion above: p₂ = 0.175, p₃ = 0.1766, p₄ = 0.1768, quickly converging to 0.177.</p>
<h4><span class="st">Check</span>Rank the three numbers</h4>
<div class="tw"><table class="mini"><thead><tr><th>Method</th><th>P<sub>e</sub></th><th>Reason</th></tr></thead><tbody><tr><td>Linear MMSE (q = 0)</td><td>0.188</td><td>ISI not handled at all</td></tr><tr><td>DFE (with error propagation)</td><td>0.177</td><td>ISI subtracted most of the time</td></tr><tr><td>DFE (feedback always correct)</td><td>0.159 = Q(1)</td><td>as if there were no ISI</td></tr></tbody></table></div>
<p>The DFE beats the linear equaliser because it does not enhance noise, but error propagation eats part of the advantage (0.159 → 0.177). p must lie between 0.159 and 0.261, so 0.177 is reasonable.</p>
<h4><span class="st">Pitfalls</span>Where marks are lost</h4>
<ul>
<li>Dropping the (q/2)A<sub>n</sub> term when expanding, which makes the MSE wrong.</li>
<li>Assuming "an equaliser always helps" and forcing a non-zero q. Here q = 0 is correct; that is exactly the point of the question.</li>
<li>After a wrong decision the ISI doubles (amplitude 2 or 0), it does not vanish; with amplitude 0 the error probability is ½, not 0 or 1.</li>
<li>Mistakes in rearranging the steady-state equation: the coefficient of p is 1 − 0.261 + 0.159, not 1 − 0.261 − 0.159.</li>
</ul>
<h4><span class="st">Exam</span>How to write it</h4>
<div class="tmpl" lang="en"><p>(a) \(u_n-A_n=\tfrac q2A_n+\tfrac12A_{n-1}+qA_{n+1}+z_n+qz_{n+1}\). The terms are independent and zero-mean, so \(E[(u_n-A_n)^2]=\tfrac{q^2}{4}+\tfrac14+q^2+1+q^2=1.25+2.25q^2\), minimised at q = 0.</p><p>Then \(u_n=y_n\); for \(A_n=+1\) the amplitude is 1.5 or 0.5 with prob. ½ each: \(P_e=\tfrac12Q(1.5)+\tfrac12Q(0.5)=\tfrac12(0.0668)+\tfrac12(0.3085)\approx0.19\).</p><p>(b) \(u_n=A_n+\tfrac12(A_{n-1}-\hat A_{n-1})+z_n\). If the previous decision is correct, \(u_n=A_n+z_n\) and \(P(e\mid c)=Q(1)=0.159\). If it is wrong, \(u_n=A_n+A_{n-1}+z_n\) (amplitude 2 or 0), so \(P(e\mid e)=\tfrac12Q(2)+\tfrac12\cdot\tfrac12=0.261\).</p><p>In steady state \(p=(1-p)(0.159)+p(0.261)\Rightarrow p=\dfrac{0.159}{1-0.261+0.159}\approx0.18\). Error propagation raises \(P_e\) above Q(1), but the DFE still beats the linear equaliser.</p></div>
<div class="ans">In one line: (a) MSE 1.25 + 2.25q² and y<sub>n+1</sub> cannot help → q = 0, P<sub>e</sub> = ½Q(1.5) + ½Q(0.5) ≈ 0.19; (b) previous correct → Q(1), previous wrong → ½Q(2) + ¼, steady state p = 0.159/(1 − 0.261 + 0.159) ≈ 0.18.</div>''',
}

# =====================================================================================  P7 Q1
XPL['p7q1'] = {
'title': '知识讲解 + 详细解析：OFDM 选 N、算 H_k、分功率',
'zh': r'''<h4><span class="st">知识讲解</span>OFDM 把频率选择性信道切成 N 条平坦子信道</h4>
<p>多径信道 y(t) = h₀x(t) + h₁x(t − τ) + w(t) 的频率响应随频率起伏（频率选择性衰落），单载波传输会有 ISI。OFDM 把总带宽 B 切成 N 个子载波，每个宽 Δf = B/N（第 7 章 p.8），一个 OFDM 符号长 T = N/B（p.7）。只要每个子载波足够窄，它在自己那一小段频率里看到的增益就近似是常数，即平坦衰落；接收端 DFT 以后得到 r<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + w<sub>k</sub>（p.6、p.17）。</p>
<p><b>两个条件</b>（第 2 章 p.31–37）：</p>
<ul>
<li><b>平坦（flat）</b>：信号带宽 &lt; 相干带宽 B<sub>C</sub>。这里"信号"是一个子载波，所以 B/N ≪ B<sub>C</sub>。</li>
<li><b>慢衰落（slow）</b>：符号时长 &lt; 相干时间 T<sub>C</sub> ≈ 1/B<sub>d</sub>（p.36：相干时间是多普勒扩展的对偶）。这里"符号"是一个 OFDM 符号，所以 N/B ≪ 1/B<sub>d</sub>。</li>
</ul>
<p><b>子信道增益</b>（第 7 章 p.15）：H<sub>k</sub> = Σ<sub>i</sub> h<sub>i</sub> e<sup>−j2πik/N</sup>，就是冲激响应 [h₀, h₁, …] 的 N 点 DFT。这里假设回波延迟 τ 正好是一个采样间隔（i = 0, 1）。讲义注明 H<sub>N</sub> = H₀，所以 k = 1…N 和 k = 0…N − 1 是同一组值。</p>
<p><b>容量</b>（第 7 章 p.24）：N 条独立的并行高斯子信道，C = Σ<sub>k</sub> log₂(1 + |H<sub>k</sub>|²P<sub>k</sub>/N<sub>k</sub>)，本题噪声 N<sub>k</sub> = σ² = 1。功率怎么分，(c)(d) 给了两种原则。</p>
<h4><span class="st">详细解析</span>(a) N 的选取原则</h4>
<ol>
<li>平坦：B/N ≪ B<sub>C</sub> → N ≫ B/B<sub>C</sub>（N 太小，子载波太宽，又变回频率选择性）。</li>
<li>慢衰落：T = N/B ≪ 1/B<sub>d</sub> → N ≪ B/B<sub>d</sub>（N 太大，OFDM 符号太长，信道在一个符号内就变了，子载波失去正交，产生载波间干扰 ICI）。</li>
<li>合起来：B/B<sub>C</sub> ≪ N ≪ B/B<sub>d</sub>。能找到这样的 N 的前提是 B<sub>d</sub> ≪ B<sub>C</sub>，实际系统一般满足。</li>
</ol>
<h4><span class="st">详细解析</span>(b) 算 H<sub>k</sub></h4>
<p>N = 4：e<sup>−j2πk/4</sup> = e<sup>−jπk/2</sup>，k = 0, 1, 2, 3 依次是 1、−j、−1、j（在单位圆上每次顺时针转 90°）。</p>
<div class="calc">H₀ = H₄ = 0.8 + 0.6 = 1.4，|H|² = 1.96</div>
<div class="calc">H₁ = 0.8 + 0.6(−j) = 0.8 − 0.6j，|H|² = 0.64 + 0.36 = 1</div>
<div class="calc">H₂ = 0.8 − 0.6 = 0.2，|H|² = 0.04</div>
<div class="calc">H₃ = 0.8 + 0.6j，|H|² = 1</div>
<p>自检：Σ|H<sub>k</sub>|² = 1.96 + 1 + 0.04 + 1 = 4 = N(h₀² + h₁²) = 4 × 1 ✓（帕塞瓦尔定理，课外补充）。子信道 2 的增益只有 0.2：两条路径反相抵消，这就是频率选择性衰落里的"深衰落"。按题目编号 k = 1, 2, 3, 4，功率增益为 1、0.04、1、1.96。</p>
<h4><span class="st">详细解析</span>(c) 等容量分配</h4>
<ol>
<li>容量 log₂(1 + |H<sub>k</sub>|²P<sub>k</sub>) 都相等 ⇔ 每条的 SNR |H<sub>k</sub>|²P<sub>k</sub> 都等于同一个常数 c → P<sub>k</sub> = c/|H<sub>k</sub>|²。增益越差，分的功率越多（"劫富济贫"）。</li>
<li>由总功率求 c：<div class="calc">c(1/1 + 1/0.04 + 1/1 + 1/1.96) = c(1 + 25 + 1 + 0.51) = 27.51c = 10 → c = 0.3635</div></li>
<li>各子信道：<div class="calc">P₁ = 0.3635/1 = 0.36，P₂ = 0.3635/0.04 = 9.09，P₃ = 0.36，P₄ = 0.3635/1.96 = 0.19</div>加起来 0.36 + 9.09 + 0.36 + 0.19 = 10 ✓。</li>
</ol>
<h4><span class="st">详细解析</span>(d) 注水求最大和容量</h4>
<ol>
<li><b>池底</b> = 噪声/增益 = 1/|H<sub>k</sub>|²：1、25、1、0.51。功率 P<sub>k</sub> = μ − 1/|H<sub>k</sub>|²（μ 是水面），水面以下的子信道才分功率。</li>
<li><b>先全放水</b>：4μ − 27.51 = 10 → μ = 37.51/4 = 9.38。但子信道 2 的池底 25 &gt; 9.38，它会分到负功率，不行，去掉。</li>
<li><b>剩三条</b>：3μ − (1 + 1 + 0.51) = 10 → μ = 12.51/3 = 4.17。功率 4.17 − 1 = 3.17、3.17、4.17 − 0.51 = 3.66，都为正 ✓，加起来 10 ✓。</li>
<li><b>容量</b>：分到功率后每条的 SNR = |H<sub>k</sub>|²P<sub>k</sub>，1 + SNR = |H<sub>k</sub>|²μ：<div class="calc">C = log₂(4.17) + log₂(4.17) + log₂(4.17 × 1.96) = 2.06 + 2.06 + 3.03 = 7.15 bit</div></li>
<li><b>换成每赫兹</b>：这 7.15 bit 是 4 个子载波一起传的，每个子载波只占 B/4，所以每赫兹总带宽：7.15/4 = 1.79 ≈ 1.8 bit/s/Hz（官方答案 1.8）。</li>
</ol>
<p>和第 2 章的写法对上：每条的满功率 SNR γ<sub>k</sub> = |H<sub>k</sub>|² × 10 = 10、0.4、10、19.6，用 Σ(1/γ₀ − 1/γ<sub>k</sub>) = 1 解出 γ₀ = 2.40，γ₂ = 0.4 &lt; γ₀ 被去掉，C = Σ log₂(γ<sub>k</sub>/γ₀) = 7.15 bit，结果一样（μ = P/γ₀）。</p>
<h4><span class="st">自检</span>三种分法比一比</h4>
<div class="tw"><table class="mini"><thead><tr><th>分法</th><th>功率</th><th>总比特</th><th>bit/s/Hz</th></tr></thead><tbody><tr><td>(c) 等容量</td><td>0.36、9.09、0.36、0.19</td><td>4 × 0.447 = 1.79</td><td>0.447</td></tr><tr><td>平分（课外补充）</td><td>2.5、2.5、2.5、2.5</td><td>6.31</td><td>1.58</td></tr><tr><td>(d) 注水</td><td>3.17、0、3.17、3.66</td><td>7.15</td><td>1.79</td></tr></tbody></table></div>
<p>(c) 把 91% 的功率砸在最差的子信道上，总容量最低；注水干脆放弃它，总容量最高。注意 (c) 的"总比特 1.79"和 (d) 的"bit/s/Hz 1.79"只是数字巧合，单位不同，别混。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>功率增益要用 |H<sub>k</sub>|²，不是 |H<sub>k</sub>|；复数的模平方 = 实部² + 虚部²。</li>
<li>编号：题目 k = 1…4，H₄ = H₀ = 1.4；P₄ 对应 1.96。</li>
<li>注水不检查池底，直接用 μ = 9.38 会给子信道 2 分到负功率。</li>
<li>(d) 要的是 bit/s/Hz：最后除以 N = 4。讲义 p.24 把求和式叫"capacity per Hertz"，那是按每个子载波的带宽算的；官方答案 1.8 是除以 N 以后的值。</li>
<li>(a) 只写一个条件不够，"平坦"和"慢衰落"两边都要写，并说明理由。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(a) Each sub-carrier has bandwidth B/N and the OFDM symbol lasts about N/B. Flat fading requires B/N ≪ B<sub>C</sub>, i.e. N ≫ B/B<sub>C</sub>; slow fading requires N/B ≪ T<sub>C</sub> ≈ 1/B<sub>d</sub>, i.e. N ≪ B/B<sub>d</sub>. Hence choose \(B/B_C\ll N\ll B/B_d\).</p><p>(b) \(H_k=h_0+h_1e^{-j2\pi k/N}=0.8+0.6e^{-j\pi k/2}\): H₀ = H₄ = 1.4, H₁ = 0.8 − j0.6, H₂ = 0.2, H₃ = 0.8 + j0.6; \(|H_k|^2\) = 1, 0.04, 1, 1.96 for k = 1, 2, 3, 4.</p><p>(c) Equal capacity ⇔ \(|H_k|^2P_k=c\). \(\sum P_k=c\sum1/|H_k|^2=27.51c=10\Rightarrow c=0.3635\); P₁ = 0.36, P₂ = 9.09, P₃ = 0.36, P₄ = 0.19.</p><p>(d) Water-filling with floors \(1/|H_k|^2\) = 1, 25, 1, 0.51. Using all four gives μ = 9.38 \(\lt\) 25, so sub-channel 2 is dropped. With three: μ = (10 + 2.51)/3 = 4.17, P = 3.17, 3.17, 3.66. \(C=2\log_2(4.17)+\log_2(4.17\times1.96)=7.15\) bit over 4 sub-carriers, i.e. 7.15/4 ≈ 1.8 bit/s/Hz.</p></div>
<div class="ans">一句话：(a) B/B<sub>C</sub> ≪ N ≪ B/B<sub>d</sub>（子载波要窄于相干带宽，OFDM 符号要短于相干时间）；(b) H<sub>k</sub> = DFT{0.8, 0.6} = 1.4、0.8 − 0.6j、0.2、0.8 + 0.6j；(c) P<sub>k</sub> ∝ 1/|H<sub>k</sub>|²：0.36、9.09、0.36、0.19；(d) 注水去掉增益 0.2 的子信道，7.15 bit / 4 ≈ 1.8 bit/s/Hz。</div>''',
'title_en': 'Concept + walkthrough: OFDM N, H_k, power allocation',
'en': r'''<h4><span class="st">Concept</span>OFDM cuts a frequency-selective channel into N flat sub-channels</h4>
<p>The multipath channel y(t) = h₀x(t) + h₁x(t − τ) + w(t) has a frequency response that varies with frequency (frequency-selective fading), and single-carrier transmission suffers ISI. OFDM cuts the total bandwidth B into N sub-carriers, each Δf = B/N wide (Ch 7 p.8); one OFDM symbol lasts T = N/B (p.7). As long as each sub-carrier is narrow enough, the gain it sees over its small band is nearly constant, i.e. flat fading; after the DFT the receiver gets r<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + w<sub>k</sub> (p.6, p.17).</p>
<p><b>Two conditions</b> (Ch 2 p.31–37):</p>
<ul>
<li><b>Flat</b>: signal bandwidth &lt; coherence bandwidth B<sub>C</sub>. Here the "signal" is one sub-carrier, so B/N ≪ B<sub>C</sub>.</li>
<li><b>Slow</b>: symbol duration &lt; coherence time T<sub>C</sub> ≈ 1/B<sub>d</sub> (p.36: coherence time is the dual of the Doppler spread). Here the "symbol" is one OFDM symbol, so N/B ≪ 1/B<sub>d</sub>.</li>
</ul>
<p><b>Sub-channel gains</b> (Ch 7 p.15): H<sub>k</sub> = Σ<sub>i</sub> h<sub>i</sub> e<sup>−j2πik/N</sup>, the N-point DFT of the impulse response [h₀, h₁, …]. This assumes the echo delay τ is exactly one sampling interval (i = 0, 1). The slide notes H<sub>N</sub> = H₀, so k = 1…N and k = 0…N − 1 give the same set of values.</p>
<p><b>Capacity</b> (Ch 7 p.24): N independent parallel Gaussian sub-channels, C = Σ<sub>k</sub> log₂(1 + |H<sub>k</sub>|²P<sub>k</sub>/N<sub>k</sub>); here the noise N<sub>k</sub> = σ² = 1. (c) and (d) give two rules for splitting the power.</p>
<h4><span class="st">Step by step</span>(a) How to choose N</h4>
<ol>
<li>Flat: B/N ≪ B<sub>C</sub> → N ≫ B/B<sub>C</sub> (if N is too small the sub-carriers are too wide and become frequency-selective again).</li>
<li>Slow: T = N/B ≪ 1/B<sub>d</sub> → N ≪ B/B<sub>d</sub> (if N is too large the OFDM symbol is too long, the channel changes within one symbol, the sub-carriers lose orthogonality and inter-carrier interference, ICI, appears).</li>
<li>Together: B/B<sub>C</sub> ≪ N ≪ B/B<sub>d</sub>. Such an N exists only if B<sub>d</sub> ≪ B<sub>C</sub>, which practical systems normally satisfy.</li>
</ol>
<h4><span class="st">Step by step</span>(b) Compute H<sub>k</sub></h4>
<p>N = 4: e<sup>−j2πk/4</sup> = e<sup>−jπk/2</sup> is 1, −j, −1, j for k = 0, 1, 2, 3 (a 90° clockwise step around the unit circle each time).</p>
<div class="calc">H₀ = H₄ = 0.8 + 0.6 = 1.4, |H|² = 1.96</div>
<div class="calc">H₁ = 0.8 + 0.6(−j) = 0.8 − 0.6j, |H|² = 0.64 + 0.36 = 1</div>
<div class="calc">H₂ = 0.8 − 0.6 = 0.2, |H|² = 0.04</div>
<div class="calc">H₃ = 0.8 + 0.6j, |H|² = 1</div>
<p>Check: Σ|H<sub>k</sub>|² = 1.96 + 1 + 0.04 + 1 = 4 = N(h₀² + h₁²) = 4 × 1 ✓ (Parseval's theorem, not in the slides). Sub-channel 2 has gain only 0.2: the two paths cancel each other, a "deep fade" of frequency-selective fading. With the question's numbering k = 1, 2, 3, 4 the power gains are 1, 0.04, 1, 1.96.</p>
<h4><span class="st">Step by step</span>(c) Equal-capacity allocation</h4>
<ol>
<li>All capacities log₂(1 + |H<sub>k</sub>|²P<sub>k</sub>) equal ⇔ every SNR |H<sub>k</sub>|²P<sub>k</sub> equals the same constant c → P<sub>k</sub> = c/|H<sub>k</sub>|². The weaker the gain, the more power ("rob the rich to pay the poor").</li>
<li>Find c from the total power:<div class="calc">c(1/1 + 1/0.04 + 1/1 + 1/1.96) = c(1 + 25 + 1 + 0.51) = 27.51c = 10 → c = 0.3635</div></li>
<li>Each sub-channel:<div class="calc">P₁ = 0.3635/1 = 0.36, P₂ = 0.3635/0.04 = 9.09, P₃ = 0.36, P₄ = 0.3635/1.96 = 0.19</div>Sum 0.36 + 9.09 + 0.36 + 0.19 = 10 ✓.</li>
</ol>
<h4><span class="st">Step by step</span>(d) Water-filling for the maximum sum capacity</h4>
<ol>
<li><b>Floors</b> = noise/gain = 1/|H<sub>k</sub>|²: 1, 25, 1, 0.51. Power P<sub>k</sub> = μ − 1/|H<sub>k</sub>|² (μ is the water level); only sub-channels below the water level get power.</li>
<li><b>Fill all four first</b>: 4μ − 27.51 = 10 → μ = 37.51/4 = 9.38. But sub-channel 2 has floor 25 &gt; 9.38 and would get negative power, which is impossible, so drop it.</li>
<li><b>Three left</b>: 3μ − (1 + 1 + 0.51) = 10 → μ = 12.51/3 = 4.17. Powers 4.17 − 1 = 3.17, 3.17, 4.17 − 0.51 = 3.66, all positive ✓, sum 10 ✓.</li>
<li><b>Capacity</b>: after allocation each SNR is |H<sub>k</sub>|²P<sub>k</sub>, so 1 + SNR = |H<sub>k</sub>|²μ:<div class="calc">C = log₂(4.17) + log₂(4.17) + log₂(4.17 × 1.96) = 2.06 + 2.06 + 3.03 = 7.15 bit</div></li>
<li><b>Per hertz</b>: these 7.15 bit are carried by 4 sub-carriers together, each occupying B/4, so per hertz of total bandwidth: 7.15/4 = 1.79 ≈ 1.8 bit/s/Hz (official answer 1.8).</li>
</ol>
<p>Matching the Ch 2 notation: each full-power SNR γ<sub>k</sub> = |H<sub>k</sub>|² × 10 = 10, 0.4, 10, 19.6; solving Σ(1/γ₀ − 1/γ<sub>k</sub>) = 1 gives γ₀ = 2.40, γ₂ = 0.4 &lt; γ₀ is dropped, and C = Σ log₂(γ<sub>k</sub>/γ₀) = 7.15 bit, the same result (μ = P/γ₀).</p>
<h4><span class="st">Check</span>Three allocations side by side</h4>
<div class="tw"><table class="mini"><thead><tr><th>Allocation</th><th>Powers</th><th>Total bits</th><th>bit/s/Hz</th></tr></thead><tbody><tr><td>(c) Equal capacity</td><td>0.36, 9.09, 0.36, 0.19</td><td>4 × 0.447 = 1.79</td><td>0.447</td></tr><tr><td>Equal power (not in the slides)</td><td>2.5, 2.5, 2.5, 2.5</td><td>6.31</td><td>1.58</td></tr><tr><td>(d) Water-filling</td><td>3.17, 0, 3.17, 3.66</td><td>7.15</td><td>1.79</td></tr></tbody></table></div>
<p>(c) pours 91% of the power into the worst sub-channel and has the lowest total; water-filling gives that sub-channel up and has the highest. Note that the "1.79 total bits" of (c) and the "1.79 bit/s/Hz" of (d) are a numerical coincidence with different units; do not mix them up.</p>
<h4><span class="st">Pitfalls</span>Where marks are lost</h4>
<ul>
<li>The power gain is |H<sub>k</sub>|², not |H<sub>k</sub>|; the squared modulus of a complex number = real² + imaginary².</li>
<li>Numbering: the question uses k = 1…4, H₄ = H₀ = 1.4; P₄ goes with 1.96.</li>
<li>Water-filling without checking the floors: using μ = 9.38 directly gives sub-channel 2 negative power.</li>
<li>(d) asks for bit/s/Hz: divide by N = 4 at the end. Slide p.24 calls the sum "capacity per Hertz", counted per sub-carrier bandwidth; the official 1.8 is the value after dividing by N.</li>
<li>In (a) one condition is not enough: write both "flat" and "slow" with the reason for each.</li>
</ul>
<h4><span class="st">Exam</span>How to write it</h4>
<div class="tmpl" lang="en"><p>(a) Each sub-carrier has bandwidth B/N and the OFDM symbol lasts about N/B. Flat fading requires B/N ≪ B<sub>C</sub>, i.e. N ≫ B/B<sub>C</sub>; slow fading requires N/B ≪ T<sub>C</sub> ≈ 1/B<sub>d</sub>, i.e. N ≪ B/B<sub>d</sub>. Hence choose \(B/B_C\ll N\ll B/B_d\).</p><p>(b) \(H_k=h_0+h_1e^{-j2\pi k/N}=0.8+0.6e^{-j\pi k/2}\): H₀ = H₄ = 1.4, H₁ = 0.8 − j0.6, H₂ = 0.2, H₃ = 0.8 + j0.6; \(|H_k|^2\) = 1, 0.04, 1, 1.96 for k = 1, 2, 3, 4.</p><p>(c) Equal capacity ⇔ \(|H_k|^2P_k=c\). \(\sum P_k=c\sum1/|H_k|^2=27.51c=10\Rightarrow c=0.3635\); P₁ = 0.36, P₂ = 9.09, P₃ = 0.36, P₄ = 0.19.</p><p>(d) Water-filling with floors \(1/|H_k|^2\) = 1, 25, 1, 0.51. Using all four gives μ = 9.38 \(\lt\) 25, so sub-channel 2 is dropped. With three: μ = (10 + 2.51)/3 = 4.17, P = 3.17, 3.17, 3.66. \(C=2\log_2(4.17)+\log_2(4.17\times1.96)=7.15\) bit over 4 sub-carriers, i.e. 7.15/4 ≈ 1.8 bit/s/Hz.</p></div>
<div class="ans">In one line: (a) B/B<sub>C</sub> ≪ N ≪ B/B<sub>d</sub> (sub-carriers narrower than the coherence bandwidth, OFDM symbol shorter than the coherence time); (b) H<sub>k</sub> = DFT{0.8, 0.6} = 1.4, 0.8 − 0.6j, 0.2, 0.8 + 0.6j; (c) P<sub>k</sub> ∝ 1/|H<sub>k</sub>|²: 0.36, 9.09, 0.36, 0.19; (d) water-filling drops the gain-0.2 sub-channel, 7.15 bit / 4 ≈ 1.8 bit/s/Hz.</div>''',
}

# =====================================================================================  P7 Q2
XPL['p7q2'] = {
'title': '知识讲解 + 详细解析：由速率和 CP 解出子载波数',
'zh': r'''<h4><span class="st">知识讲解</span>OFDM 的时间账：有用部分 + 循环前缀</h4>
<p>OFDM 把带宽 B 分成 N 个子载波，子载波间隔 Δf = B/N（第 7 章 p.8）。为了让子载波相互正交，有用符号时长必须是 T = 1/Δf = N/B（p.7）。在这段时间里，N 个子载波<b>各发一个</b>调制符号。</p>
<p>每个 OFDM 块前面还要加一段保护间隔 T<sub>G</sub>（实现上就是循环前缀 CP），T<sub>G</sub> ≥ 最大时延扩展 T<sub>D</sub>，用来挡住上一个块的回波（p.5、p.17）。所以一个 OFDM 块总长 T + T<sub>G</sub>（p.18），但 CP 不带新数据。</p>
<div class="calc">数据速率 = N × log₂M bit ÷ (N/B + T<sub>G</sub>)</div>
<p>符号：M 是调制阶数，16-QAM 的 log₂16 = 4 bit/符号；B = 600 kHz；T<sub>G</sub> = 20 µs。CP 占用时间还带来功率损失 10 log₁₀((T + T<sub>G</sub>)/T) dB（p.18）。</p>
<h4><span class="st">详细解析</span>四步解出 N 和符号时长</h4>
<ol>
<li><b>比特速率换成符号速率。</b>为什么：一个子载波一次发一个 QAM 符号，按符号数列方程更方便。2 Mbps ÷ 4 bit = 500 k 符号/秒。</li>
<li><b>列方程。</b>每个 OFDM 块发 N 个符号，耗时 N/B + T<sub>G</sub>：<div class="calc">N / (N/600 kHz + 20 µs) = 500 k 符号/秒</div></li>
<li><b>解方程。</b>两边乘以分母：N = 500k × N/600k + 500k × 20 × 10⁻⁶ = 0.8333N + 10 → 0.1667N = 10 → N = 60。</li>
<li><b>算时长。</b>T = N/B = 60/600 kHz = 100 µs（Δf = 10 kHz）；OFDM 符号总长 T + T<sub>G</sub> = 100 + 20 = 120 µs = 0.12 ms。</li>
</ol>
<p><b>更快的想法：</b>不加 CP 时 600 kHz 能发 600 k 符号/秒，只需要 500 k，所以有用时间只能占 500/600 = 5/6，CP 占 1/6：T<sub>G</sub> = T/5 → T = 5 × 20 = 100 µs → N = B·T = 600 k × 100 µs = 60。</p>
<h4><span class="st">自检</span>回代检查</h4>
<ul>
<li>速率：60 × 4 bit / 120 µs = 2 × 10⁶ bit/s = 2 Mbps ✓。</li>
<li>每个子载波：每 120 µs 发一个符号，8.33 k 符号/秒，× 60 = 500 k 符号/秒 ✓。</li>
<li>平坦吗：相干带宽约 B<sub>C</sub> ≈ 1/T<sub>D</sub> = 1/20 µs = 50 kHz（第 7 章 p.14 用 T<sub>D</sub> = 1/B<sub>c</sub>），子载波宽 10 kHz &lt; 50 kHz ✓。</li>
<li>CP 功率损失：10 log₁₀(120/100) = 0.79 dB。</li>
</ul>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>忘了 CP：没有 CP 时 600 kHz 本来就够发 500 k 符号/秒，N 取多少都行，题目就没有唯一解。正是 CP 的开销决定了 N。</li>
<li>直接拿 2 Mbps 列方程，忘了先除以 4 bit/符号。</li>
<li>单位：N/600 kHz 的单位是秒，60/600 000 = 10⁻⁴ s = 100 µs；20 µs = 2 × 10⁻⁵ s。</li>
<li>"OFDM symbol duration"官方答案 0.12 ms 是含 CP 的总长；如果题目问有用符号时长，答 100 µs。两个都写出来最稳。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>16-QAM carries log₂16 = 4 bits/symbol, so the required symbol rate is 2 Mbps / 4 = 500 k symbols/s.</p><p>With N sub-carriers, the useful OFDM symbol duration is T = N/B and each OFDM block lasts T + T<sub>G</sub> with T<sub>G</sub> = 20 µs, carrying N symbols: \(\dfrac{N}{N/(600\text{ kHz})+20\,\mu\text{s}}=500\text{ k}\Rightarrow N=0.8333N+10\Rightarrow N=60\).</p><p>Useful duration T = 60/600 kHz = 100 µs (Δf = 10 kHz); OFDM symbol duration including the CP = 100 + 20 = 120 µs = 0.12 ms. Check: 60 × 4 bits / 120 µs = 2 Mbps.</p></div>
<div class="ans">一句话：2 Mbps ÷ 4 = 500 k 符号/秒；N/(N/600 kHz + 20 µs) = 500 k → N = 60；T = 100 µs，加 CP 后 OFDM 符号长 120 µs = 0.12 ms。</div>''',
'title_en': 'Concept + walkthrough: N from rate and CP',
'en': r'''<h4><span class="st">Concept</span>OFDM time budget: useful part + cyclic prefix</h4>
<p>OFDM divides the bandwidth B into N sub-carriers with spacing Δf = B/N (Ch 7 p.8). For the sub-carriers to be orthogonal, the useful symbol duration must be T = 1/Δf = N/B (p.7). During this time each of the N sub-carriers sends <b>one</b> modulated symbol.</p>
<p>Each OFDM block is also preceded by a guard interval T<sub>G</sub> (implemented as a cyclic prefix, CP), with T<sub>G</sub> ≥ the maximum delay spread T<sub>D</sub>, to block the echo of the previous block (p.5, p.17). So one OFDM block lasts T + T<sub>G</sub> in total (p.18), but the CP carries no new data.</p>
<div class="calc">Data rate = N × log₂M bit ÷ (N/B + T<sub>G</sub>)</div>
<p>Symbols: M is the modulation order, log₂16 = 4 bits/symbol for 16-QAM; B = 600 kHz; T<sub>G</sub> = 20 µs. The time spent on the CP also costs power: 10 log₁₀((T + T<sub>G</sub>)/T) dB (p.18).</p>
<h4><span class="st">Step by step</span>Four steps to N and the symbol duration</h4>
<ol>
<li><b>Bit rate to symbol rate.</b> Why: each sub-carrier sends one QAM symbol at a time, so it is easier to count symbols. 2 Mbps ÷ 4 bits = 500 k symbols/s.</li>
<li><b>Set up the equation.</b> Each OFDM block carries N symbols and takes N/B + T<sub>G</sub>:<div class="calc">N / (N/600 kHz + 20 µs) = 500 k symbols/s</div></li>
<li><b>Solve.</b> Multiply both sides by the denominator: N = 500k × N/600k + 500k × 20 × 10⁻⁶ = 0.8333N + 10 → 0.1667N = 10 → N = 60.</li>
<li><b>Durations.</b> T = N/B = 60/600 kHz = 100 µs (Δf = 10 kHz); total OFDM symbol T + T<sub>G</sub> = 100 + 20 = 120 µs = 0.12 ms.</li>
</ol>
<p><b>A quicker way:</b> without a CP, 600 kHz could carry 600 k symbols/s, but only 500 k are needed, so the useful time can take only 500/600 = 5/6 of each block and the CP takes 1/6: T<sub>G</sub> = T/5 → T = 5 × 20 = 100 µs → N = B·T = 600 k × 100 µs = 60.</p>
<h4><span class="st">Check</span>Substitute back</h4>
<ul>
<li>Rate: 60 × 4 bits / 120 µs = 2 × 10⁶ bit/s = 2 Mbps ✓.</li>
<li>Per sub-carrier: one symbol every 120 µs, 8.33 k symbols/s, × 60 = 500 k symbols/s ✓.</li>
<li>Flat? The coherence bandwidth is about B<sub>C</sub> ≈ 1/T<sub>D</sub> = 1/20 µs = 50 kHz (Ch 7 p.14 uses T<sub>D</sub> = 1/B<sub>c</sub>); the sub-carrier width 10 kHz &lt; 50 kHz ✓.</li>
<li>CP power loss: 10 log₁₀(120/100) = 0.79 dB.</li>
</ul>
<h4><span class="st">Pitfalls</span>Where marks are lost</h4>
<ul>
<li>Forgetting the CP: without it, 600 kHz is already enough for 500 k symbols/s, any N works and there is no unique answer. It is the CP overhead that fixes N.</li>
<li>Using 2 Mbps directly in the equation without first dividing by 4 bits/symbol.</li>
<li>Units: N/600 kHz is in seconds, 60/600 000 = 10⁻⁴ s = 100 µs; 20 µs = 2 × 10⁻⁵ s.</li>
<li>The official "OFDM symbol duration" of 0.12 ms is the total including the CP; if a question asks for the useful symbol duration, answer 100 µs. Writing both is safest.</li>
</ul>
<h4><span class="st">Exam</span>How to write it</h4>
<div class="tmpl" lang="en"><p>16-QAM carries log₂16 = 4 bits/symbol, so the required symbol rate is 2 Mbps / 4 = 500 k symbols/s.</p><p>With N sub-carriers, the useful OFDM symbol duration is T = N/B and each OFDM block lasts T + T<sub>G</sub> with T<sub>G</sub> = 20 µs, carrying N symbols: \(\dfrac{N}{N/(600\text{ kHz})+20\,\mu\text{s}}=500\text{ k}\Rightarrow N=0.8333N+10\Rightarrow N=60\).</p><p>Useful duration T = 60/600 kHz = 100 µs (Δf = 10 kHz); OFDM symbol duration including the CP = 100 + 20 = 120 µs = 0.12 ms. Check: 60 × 4 bits / 120 µs = 2 Mbps.</p></div>
<div class="ans">In one line: 2 Mbps ÷ 4 = 500 k symbols/s; N/(N/600 kHz + 20 µs) = 500 k → N = 60; T = 100 µs, and with the CP the OFDM symbol lasts 120 µs = 0.12 ms.</div>''',
}

# =====================================================================================  P7 Q3
XPL['p7q3'] = {
'title': '知识讲解 + 详细解析：最短循环前缀 = L − 1',
'zh': r'''<h4><span class="st">知识讲解</span>信道"记忆"和循环前缀</h4>
<p><b>从 H(z) 读冲激响应</b>：z⁻¹ 表示晚一个采样，H(z) = 1 + 0.9z⁻¹ → h = [1, 0.9]，一条直射 + 一条晚 1 个采样、强度 0.9 的回波。抽头数 L = 2，信道的"记忆"（最大时延）是 L − 1 = 1 个采样：每个输出样本 r<sub>i</sub> = x<sub>i</sub> + 0.9x<sub>i−1</sub>，会用到前一个输入样本。</p>
<p><b>问题在块边界</b>：OFDM 一块一块地发（每块是 N 个子载波符号做 IDFT 得到的 N 个采样，第 7 章 p.19）。一个块的第一个采样 r₀ = x₀ + 0.9 × (上一块的最后一个采样)，混进了上一块的数据，这就是块间的 ISI。</p>
<p><b>循环前缀 CP</b>（p.21–22）：把每块最后 G 个采样复制一份放到块前面，接收端把这 G 个采样丢掉，只留后 N 个。G ≥ L − 1 时，上一块的回波只会落在被丢掉的 CP 里。</p>
<p><b>为什么要"复制块尾"而不是放空白</b>：放 CP 后，块的第一个采样前面"看到"的是本块的最后一个采样，线性卷积在接收窗口里就变成循环卷积。循环卷积做 DFT 正好变成乘法：R<sub>k</sub> = H<sub>k</sub>S<sub>k</sub> + W<sub>k</sub>（p.17、p.22），每个子载波只乘一个复数，子载波之间保持正交。如果只放空白（补零），能挡住 ISI，但接收窗口里不再是循环结构，子载波失去正交，产生载波间干扰（ICI）。</p>
<h4><span class="st">详细解析</span>用 N = 4 的小例子看清楚</h4>
<ol>
<li><b>发送</b>：一块的采样是 x₀ x₁ x₂ x₃，加 1 个采样的 CP 后发 [x₃ | x₀ x₁ x₂ x₃]。</li>
<li><b>接收</b>（r<sub>i</sub> = x<sub>i</sub> + 0.9x<sub>i−1</sub>）：<div class="calc">CP 位置：x₃ + 0.9 × (上一块最后一个采样) ← 有 ISI，但会被丢掉</div><div class="calc">r₀ = x₀ + 0.9x₃（前一个采样正好是 CP 里的 x₃）</div><div class="calc">r₁ = x₁ + 0.9x₀，r₂ = x₂ + 0.9x₁，r₃ = x₃ + 0.9x₂</div></li>
<li><b>看结构</b>：留下的 r₀…r₃ 里每个 x 都只和它"循环意义下的前一个"相加（x₀ 的前一个是 x₃），这就是 h 和 x 的 4 点循环卷积，完全没有上一块的数据。</li>
<li><b>DFT 后</b>：R<sub>k</sub> = H<sub>k</sub>S<sub>k</sub>，H<sub>k</sub> = 1 + 0.9e<sup>−j2πk/4</sup> = 1.9、1 − 0.9j、0.1、1 + 0.9j。接收端每个子载波除以 H<sub>k</sub> 就完成均衡（p.25–26）。</li>
<li><b>结论</b>：最短 CP = L − 1 = 1 个采样（1 个符号长度）。再短（0 个）就挡不住 ISI；更长也可以，但浪费时间，效率 N/(N + G)。</li>
</ol>
<p>附带一点：H₂ = 0.1，第 2 个子载波几乎被两条路径抵消。OFDM 不能消除衰落，只是把频率选择性衰落变成每个子载波上的平坦衰落，这时就需要编码或 P7 Q1 那样的功率分配。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>答成 L = 2 个采样。CP 要盖住的是"回波晚到的那部分"，是 L − 1，不是 L。</li>
<li>以为系数 0.9 越大 CP 要越长。CP 长度只看延迟几个采样，和回波强弱无关。</li>
<li>只说"挡住 ISI"，不说为什么要用块尾的复制品（保持循环卷积 / 子载波正交，避免 ICI）。题目要求 Explain，这一点是得分点。</li>
<li>换成时间单位：CP ≥ 1 个采样间隔 T<sub>s</sub>，即 T<sub>G</sub> ≥ 最大时延扩展 T<sub>D</sub>。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>From \(H(z)=1+0.9z^{-1}\), the channel impulse response is h = [1, 0.9]: L = 2 taps, so the channel memory (maximum delay spread) is L − 1 = 1 sample.</p><p>The last sample of each OFDM block therefore leaks into the first sample of the next block (ISI). A cyclic prefix of G ≥ L − 1 samples, i.e. a copy of the last sample of the block placed in front of it, absorbs this leakage, and the receiver discards the CP.</p><p>Because the prefix is cyclic, the linear convolution with h becomes a circular convolution over the N retained samples, so after the DFT \(r_k=H_ks_k+w_k\): no ISI and no ICI, and each sub-carrier is equalised by one complex gain.</p><p>Minimum cyclic prefix = 1 symbol (sample) length.</p></div>
<div class="ans">一句话：h = [1, 0.9]，回波晚 1 个采样 → 最短 CP = L − 1 = 1 个符号长度；用块尾复制品做前缀，既把 ISI 留在被丢掉的 CP 里，又让线性卷积变成循环卷积，DFT 后 r<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + w<sub>k</sub>。</div>''',
'title_en': 'Concept + walkthrough: minimum CP = L − 1',
'en': r'''<h4><span class="st">Concept</span>Channel "memory" and the cyclic prefix</h4>
<p><b>Read the impulse response from H(z)</b>: z⁻¹ means one sample later, so H(z) = 1 + 0.9z⁻¹ → h = [1, 0.9]: a direct path plus an echo 1 sample later with strength 0.9. The number of taps is L = 2 and the channel "memory" (maximum delay) is L − 1 = 1 sample: each output sample r<sub>i</sub> = x<sub>i</sub> + 0.9x<sub>i−1</sub> uses the previous input sample.</p>
<p><b>The problem is at block boundaries</b>: OFDM is sent block by block (each block is the N samples obtained by an IDFT of N sub-carrier symbols, Ch 7 p.19). The first sample of a block is r₀ = x₀ + 0.9 × (last sample of the previous block), which mixes in data from the previous block: inter-block ISI.</p>
<p><b>Cyclic prefix (CP)</b> (p.21–22): copy the last G samples of each block to its front; the receiver discards these G samples and keeps only the last N. With G ≥ L − 1, the echo of the previous block lands only inside the discarded CP.</p>
<p><b>Why "copy the tail" instead of leaving a gap</b>: with the CP, the sample "seen" before the first sample of the block is the last sample of the same block, so inside the receive window the linear convolution becomes a circular convolution. The DFT turns circular convolution exactly into multiplication: R<sub>k</sub> = H<sub>k</sub>S<sub>k</sub> + W<sub>k</sub> (p.17, p.22); each sub-carrier is multiplied by one complex number and the sub-carriers stay orthogonal. An empty gap (zero padding) also blocks the ISI, but the window no longer has a circular structure, so the sub-carriers lose orthogonality and inter-carrier interference (ICI) appears.</p>
<h4><span class="st">Step by step</span>A small N = 4 example makes it clear</h4>
<ol>
<li><b>Transmit</b>: a block has samples x₀ x₁ x₂ x₃; with a 1-sample CP we send [x₃ | x₀ x₁ x₂ x₃].</li>
<li><b>Receive</b> (r<sub>i</sub> = x<sub>i</sub> + 0.9x<sub>i−1</sub>):<div class="calc">CP slot: x₃ + 0.9 × (last sample of the previous block) ← contains ISI, but is discarded</div><div class="calc">r₀ = x₀ + 0.9x₃ (the previous sample is exactly the x₃ in the CP)</div><div class="calc">r₁ = x₁ + 0.9x₀, r₂ = x₂ + 0.9x₁, r₃ = x₃ + 0.9x₂</div></li>
<li><b>Look at the structure</b>: in the kept r₀…r₃ each x is added only to its "cyclic predecessor" (the predecessor of x₀ is x₃). This is the 4-point circular convolution of h and x, with no data from the previous block at all.</li>
<li><b>After the DFT</b>: R<sub>k</sub> = H<sub>k</sub>S<sub>k</sub> with H<sub>k</sub> = 1 + 0.9e<sup>−j2πk/4</sup> = 1.9, 1 − 0.9j, 0.1, 1 + 0.9j. The receiver equalises by dividing each sub-carrier by H<sub>k</sub> (p.25–26).</li>
<li><b>Conclusion</b>: minimum CP = L − 1 = 1 sample (1 symbol length). Shorter (0) cannot block the ISI; longer also works but wastes time, efficiency N/(N + G).</li>
</ol>
<p>A side note: H₂ = 0.1, so sub-carrier 2 is almost cancelled by the two paths. OFDM does not remove fading; it turns frequency-selective fading into flat fading on each sub-carrier, which then needs coding or power allocation as in P7 Q1.</p>
<h4><span class="st">Pitfalls</span>Where marks are lost</h4>
<ul>
<li>Answering L = 2 samples. The CP must cover the part of the echo that arrives late, which is L − 1, not L.</li>
<li>Thinking a larger coefficient 0.9 needs a longer CP. The CP length depends only on how many samples the echo is delayed, not on its strength.</li>
<li>Saying only "it blocks ISI" without saying why the copy of the tail is used (keeps the circular convolution / sub-carrier orthogonality, avoids ICI). The question says "Explain"; this point earns marks.</li>
<li>In time units: CP ≥ 1 sampling interval T<sub>s</sub>, i.e. T<sub>G</sub> ≥ the maximum delay spread T<sub>D</sub>.</li>
</ul>
<h4><span class="st">Exam</span>How to write it</h4>
<div class="tmpl" lang="en"><p>From \(H(z)=1+0.9z^{-1}\), the channel impulse response is h = [1, 0.9]: L = 2 taps, so the channel memory (maximum delay spread) is L − 1 = 1 sample.</p><p>The last sample of each OFDM block therefore leaks into the first sample of the next block (ISI). A cyclic prefix of G ≥ L − 1 samples, i.e. a copy of the last sample of the block placed in front of it, absorbs this leakage, and the receiver discards the CP.</p><p>Because the prefix is cyclic, the linear convolution with h becomes a circular convolution over the N retained samples, so after the DFT \(r_k=H_ks_k+w_k\): no ISI and no ICI, and each sub-carrier is equalised by one complex gain.</p><p>Minimum cyclic prefix = 1 symbol (sample) length.</p></div>
<div class="ans">In one line: h = [1, 0.9], the echo is 1 sample late → minimum CP = L − 1 = 1 symbol length; a prefix copied from the block tail keeps the ISI inside the discarded CP and turns the linear convolution into a circular one, so after the DFT r<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + w<sub>k</sub>.</div>''',
}

NOTES = '''p5q3: the existing solution writes 9.97 bit/s/Hz in step 3 but "≈ 9.96" in the answer line; exact 3·log2(10) = 9.966 (official 9.96 is truncated). The box says both are acceptable.
p5q1: the existing key-points box (comparison 2) says equal power gives 0.70 bit/s/Hz vs water-filling 0.85, "差 21%" / EN "21% less". 0.85/0.70 = 1.21, so water-filling is 21% MORE; equal power is only about 17% LESS. The EN wording "21% less" is inaccurate (ZH "差 21%" is ambiguous). The box here says "water-filling about 21% higher".
p6q1: the question states 0 < α < 1/2, but the 题意讲解 (intent) symbol table says "α（0 < α < 1）". The (b) conclusion holds for any α > 0, so nothing in the box depends on it.
p6q1: (b) "better with the equaliser" holds only at high SNR; with α = 0.4 the no-equaliser system is slightly better for √(2Eb/N0) below ≈ 1.06 (Eb/N0 ≈ −2.5 dB). Mentioned in the box as 课外补充.
p7q1: slide Ch 7 p.24 labels Σ log2(1 + |Hk|²Pk/Nk) as "capacity per Hertz" without dividing by N; the official answer 1.8 bit/s/Hz divides 7.15 by N = 4 (per Hz of total bandwidth). The box explains this neutrally.'''
