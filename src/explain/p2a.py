# -*- coding: utf-8 -*-
"""知识讲解 + 详细解析 boxes for Part 2 practice, group p2a (Practice 1–4).
Bilingual: 'title'/'zh' (Chinese) and 'title_en'/'en' (English). The 考试 template is English and
identical in both languages (shared via TM). Numbers checked by check_p2a.py."""

# ---------------------------------------------------------------- shared English exam templates
TM = {}

TM['p1q1'] = r'''<div class="tmpl" lang="en">
<p>(a) In dB the model is a straight line, \(M=K_{dB}-\gamma x\), with \(x=10\log_{10}(d/d_0)\) and \(d_0\) = 1 m. Least squares minimises \(F(K,\gamma)=\sum_i(M_i-K_{dB}+\gamma x_i)^2\). Setting \(\partial F/\partial K=0\) and \(\partial F/\partial\gamma=0\) gives \(K_{dB}=\bar M+\gamma\bar x\) and \(\gamma=-S_{xM}/S_{xx}\).</p>
<p>With Σx = 115.53, Σx² = 2566.75, ΣM = −640 and ΣxM = −13671.57: S<sub>xx</sub> = 342.11, S<sub>xM</sub> = −1348.08, so γ = 3.94 and K<sub>dB</sub> = −106.67 + 3.94 × 19.26 = −30.8 dB.</p>
<p>(b) The shadowing variance equals the MSE of the fit: σ<sub>ψ</sub>² = (1/6)Σe<sub>i</sub>² = 71.23/6 = 11.87 dB², σ<sub>ψ</sub> = 3.45 dB. Outage occurs when shadowing lowers the power by more than the 10 dB margin: P<sub>out</sub> = P(ψ<sub>dB</sub> &lt; −10) = Q(10/σ<sub>ψ</sub>) = Q(2.90) ≈ 1.85 × 10⁻³.</p>
</div>'''

TM['p1q2'] = r'''<div class="tmpl" lang="en">
<p>Log-normal shadowing means the received power in dBm is Gaussian, \(P_r\sim\mathcal N(\mu_\psi,\sigma_\psi^2)\). Outage: \(P_{out}=P(P_r\lt10\text{ dBm})=Q\big((\mu_\psi-10)/\sigma_\psi\big)\).</p>
<p>(a) P<sub>out</sub> = Q((15 − 10)/8) = Q(0.625) ≈ 0.266, i.e. about 26.6%.</p>
<p>(b) Require Q((μ<sub>ψ</sub> − 10)/4) &lt; 0.01. Q is decreasing and Q(2.326) = 0.01, so (μ<sub>ψ</sub> − 10)/4 &gt; 2.326, i.e. μ<sub>ψ</sub> &gt; 10 + 4 × 2.326 = 19.3 dBm.</p>
</div>'''

TM['p1q3'] = r'''<div class="tmpl" lang="en">
<p>(a) Use P<sub>r</sub>(τ) as the weight: \(\mu_{T_m}=\dfrac{\int_0^{10}\tau P_r(\tau)d\tau}{\int_0^{10}P_r(\tau)d\tau}=\dfrac{50}{10}=5\) µs, and \(\sigma_{T_m}^2=\dfrac{\int_0^{10}(\tau-\mu_{T_m})^2P_r(\tau)d\tau}{\int_0^{10}P_r(\tau)d\tau}=\dfrac{83.33}{10}=8.33\) µs², so σ<sub>Tm</sub> = 2.89 µs.</p>
<p>(b) Flat fading requires σ<sub>Tm</sub>/T<sub>s</sub> &lt; 0.1, i.e. T<sub>s</sub> &gt; 10σ<sub>Tm</sub> = 28.87 µs, so R<sub>s</sub> = 1/T<sub>s</sub> &lt; 34.6 ksps.</p>
</div>'''

TM['p2q1'] = r'''<div class="tmpl" lang="en">
<p>For Rayleigh fading, AFD = (e<sup>ρ²</sup> − 1)/(√(2π) f<sub>D</sub> ρ), where ρ = Z<sub>min</sub>/Z<sub>rms</sub> is the ratio of the minimum acceptable signal strength to the rms signal strength, and f<sub>D</sub> is the maximum Doppler shift.</p>
<p>Here ρ = 0.1 and f<sub>D</sub> = 50 Hz: AFD = (e<sup>0.01</sup> − 1)/(2.5066 × 50 × 0.1) = 0.01005/12.53 = 8.0 × 10⁻⁴ s ≈ 0.8 ms.</p>
<p>So each time the signal falls below 0.1 of its rms value, it stays below for about 0.8 ms on average.</p>
</div>'''

TM['p3q1'] = r'''<div class="tmpl" lang="en">
<p>(a) Using cos(a + b) = cos a cos b − sin a sin b: \(A_i\cos(2\pi t/T+\phi_j)=A_i\cos\phi_j\cos(2\pi t/T)-A_i\sin\phi_j\sin(2\pi t/T)\), so every signal is a linear combination of cos(2πt/T) and sin(2πt/T).</p>
<p>They are orthogonal: \(\int_0^T\cos(2\pi t/T)\sin(2\pi t/T)dt=\tfrac12\int_0^T\sin(4\pi t/T)dt=0\). Each has energy \(\int_0^T\cos^2(2\pi t/T)dt=T/2\), so dividing by √(T/2) gives the orthonormal basis \(\psi_1(t)=\sqrt{2/T}\cos(2\pi t/T)\), \(\psi_2(t)=\sqrt{2/T}\sin(2\pi t/T)\), 0 ≤ t ≤ T.</p>
<p>(b) Two basis functions are needed, so the dimension is D = 2. Each signal is the point (A<sub>i</sub>cosφ<sub>j</sub>√(T/2), −A<sub>i</sub>sinφ<sub>j</sub>√(T/2)) in this plane (a QAM constellation).</p>
</div>'''

TM['p3q2'] = r'''<div class="tmpl" lang="en">
<p>(a) Given x<sub>n</sub> = 0, y<sub>n</sub> ~ N(0, σ₀²); given x<sub>n</sub> = 1, y<sub>n</sub> ~ N(1, σ₁²). The ML detector chooses the x that maximises f(y | x): decide 1 if \(\frac{1}{\sigma_1}e^{-(y-1)^2/2\sigma_1^2}\gt\frac{1}{\sigma_0}e^{-y^2/2\sigma_0^2}\).</p>
<p>Taking ln: decide 1 if \(g(y)=\frac{y^2}{2\sigma_0^2}-\frac{(y-1)^2}{2\sigma_1^2}+\ln\frac{\sigma_0}{\sigma_1}\gt0\). The threshold ỹ is the root of g(ỹ) = 0 between 0 and 1, i.e. of \((\sigma_1^2-\sigma_0^2)\tilde y^2+2\sigma_0^2\tilde y-\sigma_0^2-\sigma_0^2\sigma_1^2\ln(\sigma_1^2/\sigma_0^2)=0\). Rule: \(\hat x_n=1\) if y<sub>n</sub> &gt; ỹ, otherwise \(\hat x_n=0\).</p>
<p>(b) \(P_e=\tfrac12P(y\gt\tilde y\mid x=0)+\tfrac12P(y\lt\tilde y\mid x=1)=\tfrac12\big[Q(\tilde y/\sigma_0)+Q\big((1-\tilde y)/\sigma_1\big)\big]\).</p>
</div>'''

TM['p3q3'] = r'''<div class="tmpl" lang="en">
<p>The error floor is caused by ISI, which depends on the delay spread relative to the <b>symbol</b> duration, so for QPSK use T<sub>s</sub>: P<sub>floor</sub> ≈ (σ<sub>Tm</sub>/T<sub>s</sub>)².</p>
<p>(σ<sub>Tm</sub>/T<sub>s</sub>)² ≤ 10⁻³ ⇒ T<sub>s</sub> ≥ σ<sub>Tm</sub>/√10⁻³ = 3 µs/0.0316 = 94.87 µs.</p>
<p>QPSK carries log₂4 = 2 bits per symbol, so R<sub>b</sub> = 2/T<sub>s</sub> ≤ 2/94.87 µs = 21.08 kbps.</p>
</div>'''

TM['p4q1'] = r'''<div class="tmpl" lang="en">
<p>Macro-diversity: the signal from the mobile is received by several base stations at different locations, and the strongest one is used (or the signals are combined).</p>
<p>Outage is mainly caused by shadowing (large-scale fading): buildings or terrain block the path and the received power stays below the threshold for a long time.</p>
<p>Because the base stations are far apart, the paths to them pass different obstacles, so the shadowing on the links is (nearly) independent.</p>
<p>Outage occurs only if all links are below the threshold at the same time: P<sub>out</sub> = P<sub>out,1</sub> × P<sub>out,2</sub> × …, which is much smaller than for one link (e.g. 10% → 1% with two base stations).</p>
<p>The gain is smaller if the shadowing on the links is correlated (e.g. the mobile is inside a building).</p>
</div>'''

TM['p4q2'] = r'''<div class="tmpl" lang="en">
<p>(a) P<sub>T</sub> = σ<sub>n</sub>² = 1 W, so γ = α. \(\bar\gamma=8\cdot\tfrac13+11\cdot\tfrac23=10\); \(\bar P_s=\tfrac13\cdot\tfrac12e^{-8}+\tfrac23\cdot\tfrac12e^{-11}=6.15\times10^{-5}\).</p>
<p>(b) MRC output SNR γ<sub>Σ</sub> = γ₁ + γ₂. With independent branches, γ<sub>Σ</sub> = 16, 19, 22 with probabilities 1/9, 4/9, 4/9. \(\bar\gamma_\Sigma=20\); \(\bar P_s=\tfrac12\big(\tfrac19e^{-16}+\tfrac49e^{-19}+\tfrac49e^{-22}\big)=7.56\times10^{-9}\); g = γ̄<sub>Σ</sub>/γ̄ = 20/10 = 2 (3 dB); d = −log₁₀P̄<sub>s</sub>/log₁₀γ̄ = 8.12/1 = 8.1.</p>
<p>(c) γ<sub>Σ</sub> = r₁ + r₂ + 2β with r₁, r₂, β independent. E[γ<sub>i</sub>] = E[r] + E[β] = 1 + 9 = 10, so γ̄<sub>Σ</sub> = 20 and g = 2. \(\bar P_s=\tfrac12E[e^{-r_1}]E[e^{-r_2}]E[e^{-2\beta}]=\tfrac12(0.3837)^2(2.786\times10^{-7})=2.05\times10^{-8}\); d = −log₁₀(2.05 × 10⁻⁸) = 7.7.</p>
<p>The shared shadowing β leaves the array gain unchanged but raises the error probability and lowers the diversity gain.</p>
</div>'''

TM['p4q3'] = r'''<div class="tmpl" lang="en">
<p>(a) b = ±1 are equally likely and the problem is symmetric, so P<sub>b</sub> = P(z ≤ 0 | b = +1). With M = 1, z = α√E + w. α and w are independent Gaussians, so z is Gaussian with mean α₀√E and variance σ₁²E + σ₂².</p>
<p>Write z = α₀√E + n with n ~ N(0, σ₁²E + σ₂²): \(P_b=P(n\le-\alpha_0\sqrt E)=Q\Big(\dfrac{\alpha_0\sqrt E}{\sqrt{\sigma_1^2E+\sigma_2^2}}\Big)\).</p>
<p>(b) Equal-weight combining: \(z=\sum_{k=1}^My_k=b\sqrt E\sum_k\alpha_k+\sum_kw_k\). With independent α<sub>k</sub> and w<sub>k</sub> and b = +1, z is Gaussian with mean Mα₀√E and variance M(σ₁²E + σ₂²).</p>
<p>\(P_b=Q\Big(\dfrac{M\alpha_0\sqrt E}{\sqrt{M(\sigma_1^2E+\sigma_2^2)}}\Big)=Q\Big(\dfrac{\sqrt M\,\alpha_0\sqrt E}{\sqrt{\sigma_1^2E+\sigma_2^2}}\Big)\): combining M branches multiplies the argument of Q by √M.</p>
</div>'''


XPL = {}

# ================================================================ P1 Q1
XPL['p1q1'] = {
'title': '知识讲解 + 详细解析：最小二乘拟合 K、γ，再求阴影中断',
'title_en': 'Concept + walkthrough: least-squares fit of K, γ, then shadowing outage',
'zh': r'''<h4><span class="st">知识讲解</span>路径损耗 + 阴影 = 一条直线 + 随机散布</h4>
<p>简化路径损耗模型（simplified path loss model，讲义第 2 章 p.8）：\(P_r=P_tK(d_0/d)^{\gamma}\)，d₀ = 1 m。K 是 1 m 处的功率增益（由环境、天线决定的常数），γ 是路径损耗指数（path loss exponent）。老师课上强调：这是专有名词，线性和 dB 两种形式都要背，考试不给。</p>
<p>两边取 10 log₁₀ 变成 dB：\(M=(P_r/P_t)_{dB}=K_{dB}-\gamma\cdot10\log_{10}(d/d_0)\)。令 \(x=10\log_{10}d\)，它就是一条直线 \(M=K_{dB}-\gamma x\)：截距是 K<sub>dB</sub>，斜率是 −γ。</p>
<p>实测点不会正好落在直线上，偏离的部分就是阴影（shadowing）\(\psi_{dB}\sim\mathcal N(0,\sigma_\psi^2)\)（p.11–12）。讲义 p.13 的做法：找让"实测 − 模型"的均方误差（MSE）最小的直线，并且 MSE = E[X<sub>i</sub>²] = σ<sub>ψ</sub>²。所以一组数据同时给出两样东西：直线（平均趋势）和点的散布（阴影方差）。</p>
<p>中断概率（outage probability，p.14–15）：\(P_{out}=P(\psi_{dB}\lt-x)=Q(x/\sigma_\psi)\)，x = 不含阴影时的平均接收功率 − 最低要求功率，也就是余量（margin）。</p>
<div class="tw"><table class="mini"><thead><tr><th>符号</th><th>含义</th><th>本题</th></tr></thead><tbody>
<tr><td>x<sub>i</sub></td><td>10 log₁₀d<sub>i</sub>，直线的横坐标</td><td>6.99 … 30.00</td></tr>
<tr><td>M<sub>i</sub></td><td>实测 (P<sub>r</sub>/P<sub>t</sub>)<sub>dB</sub>，纵坐标</td><td>−60 … −150</td></tr>
<tr><td>K<sub>dB</sub>，γ</td><td>截距；斜率的相反数</td><td>待求</td></tr>
<tr><td>σ<sub>ψ</sub>²</td><td>阴影方差 = 拟合的 MSE</td><td>待求</td></tr>
<tr><td>余量 x</td><td>平均功率比门限高多少 dB</td><td>10 dB</td></tr>
</tbody></table></div>
<h4><span class="st">详细解析</span>(a) 用两个正规方程求 K 和 γ</h4>
<ol>
<li><b>做什么</b>：写出误差平方和 \(F(K,\gamma)=\sum_i(M_i-K+\gamma x_i)^2\)。<b>为什么</b>：最小二乘就是让 F 最小，老师课上就是这样写的。</li>
<li><b>对 K 求偏导令其为 0</b>：\(\sum_i(M_i-K+\gamma x_i)=0\) → \(K=\bar M+\gamma\bar x\)。意思是最佳直线一定经过平均点 (x̄, M̄)。</li>
<li><b>对 γ 求偏导令其为 0</b>：\(\sum_i x_i(M_i-K+\gamma x_i)=0\)，把上一式代入整理，得 \(\gamma=-S_{xM}/S_{xx}\)。</li>
<li><b>怎么算</b>：计算器上先求四个和，再算两个 S（这样比逐点算 x − x̄ 少出错）：</li>
</ol>
<div class="calc">x<sub>i</sub> = 10 log₁₀d<sub>i</sub>：6.99、13.98、18.13、20.41、26.02、30.00<br>Σx = 115.53，Σx² = 2566.75，ΣM = −640，ΣxM = −13671.57<br>S<sub>xx</sub> = Σx² − (Σx)²/6 = 2566.75 − 2224.64 = 342.11<br>S<sub>xM</sub> = ΣxM − ΣxΣM/6 = −13671.57 + 12323.49 = −1348.08<br>γ = 1348.08 / 342.11 = 3.94<br>K<sub>dB</sub> = M̄ + γx̄ = −106.67 + 3.94 × 19.26 = −30.8 dB</div>
<h4><span class="st">详细解析</span>(b) 残差 → σ → Q 函数</h4>
<ol>
<li><b>残差</b> e<sub>i</sub> = 实测 − 预测（解答里的表已逐点列出）：−1.67、+5.88、−2.77、−3.77、+3.32、−0.99。它们加起来是 0，这是最小二乘的性质，正好用来检查。</li>
<li><b>阴影方差</b>：σ<sub>ψ</sub>² = Σe²/6。为什么除以 6 而不是 5：讲义定义 MSE = E[X<sub>i</sub>²]，就是简单平均，考试照讲义除以 n。</li>
<li><b>余量</b>："只算路径损耗时比最低功率高 10 dB" → x = 10 dB。中断 = 阴影把功率往下拉超过 10 dB：\(P_{out}=P(\psi_{dB}\lt-10)=Q(10/\sigma_\psi)\)。</li>
</ol>
<div class="calc">σ<sub>ψ</sub>² = 71.23 / 6 = 11.87 dB²<br>σ<sub>ψ</sub> = √11.87 = 3.45 dB<br>10 / 3.45 = 2.90<br>P<sub>out</sub> = Q(2.90) ≈ 1.85 × 10⁻³（约 0.19%；查表取 2.90 得 1.87 × 10⁻³，差别只是取整）</div>
<h4><span class="st">自检</span>三个快速检查</h4>
<ul>
<li>直线经过平均点 (19.26, −106.67)；残差之和 = 0。</li>
<li>γ = 3.94 落在讲义 p.9 表里城市宏蜂窝的 3.7–6.5 范围内，合理。</li>
<li>余量 10 dB ≈ 2.9σ，中断约千分之二。对比：余量 2.33σ 才对应 1%，量级对得上。</li>
</ul>
<h4><span class="st">官方答案</span>为什么和标准最小二乘对不上</h4>
<p>官方答案是 K = −31.4 dB、γ = 3.86、P<sub>out</sub> = 6.19 × 10⁻⁴。把官方的 K、γ 代回 6 个点，MSE = 13.1，比最小二乘的 11.87 还大，所以它不是这组数据的最小二乘解。(b) 用的是老师课上的 MSE = 9.656：10/√9.656 = 3.22，查表取 3.23 得 6.19 × 10⁻⁴。老师说结果"在 −31.4、3.86 附近就可以"。考试照上面的方法写清每一步、用自己算出的数即可。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>横坐标用 log₁₀d 而不是 10 log₁₀d：γ 会变成 39.4，明显不合理。</li>
<li>斜率是 −γ：算出斜率 −3.94，所以 γ = +3.94，别写成负的。</li>
<li>d 用米代入（d₀ = 1 m）。老师说今年 Quiz 有人把 2 km 写成 log 2。</li>
<li>MSE 是方差，进 Q 之前要开根号；写成 Q(10/11.87) 是错的。</li>
<li>余量 10 dB 直接用 dB，不要换成线性：这个中断公式本来就是 dB 形式推出来的（老师课上特别提醒）。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
''' + TM['p1q1'] + r'''
<div class="ans">一句话：dB 下路径损耗是一条直线，最小二乘给出 K、γ，剩下的均方误差就是阴影方差 σ²；中断概率 = Q(余量 / σ)。</div>''',
'en': r'''<h4><span class="st">Concept</span>Path loss + shadowing = a straight line + random scatter</h4>
<p>Simplified path loss model (lecture Ch 2 p.8): \(P_r=P_tK(d_0/d)^{\gamma}\), d₀ = 1 m. K is the power gain at 1 m (a constant set by the environment and antennas), and γ is the path loss exponent. The lecturer stressed in class that this is a fixed name, and that both the linear and the dB forms must be memorised; they are not given in the exam.</p>
<p>Take 10 log₁₀ of both sides to get dB: \(M=(P_r/P_t)_{dB}=K_{dB}-\gamma\cdot10\log_{10}(d/d_0)\). With \(x=10\log_{10}d\) this is a straight line \(M=K_{dB}-\gamma x\): the intercept is K<sub>dB</sub> and the slope is −γ.</p>
<p>The measured points never lie exactly on the line; the deviation is the shadowing \(\psi_{dB}\sim\mathcal N(0,\sigma_\psi^2)\) (p.11–12). The method on p.13: find the line that minimises the mean squared error (MSE) between measurement and model, and MSE = E[X<sub>i</sub>²] = σ<sub>ψ</sub>². So one data set gives two things: the line (mean trend) and the scatter of the points (shadowing variance).</p>
<p>Outage probability (p.14–15): \(P_{out}=P(\psi_{dB}\lt-x)=Q(x/\sigma_\psi)\), where x = mean received power without shadowing − minimum required power, i.e. the margin.</p>
<div class="tw"><table class="mini"><thead><tr><th>Symbol</th><th>Meaning</th><th>Here</th></tr></thead><tbody>
<tr><td>x<sub>i</sub></td><td>10 log₁₀d<sub>i</sub>, horizontal axis of the line</td><td>6.99 … 30.00</td></tr>
<tr><td>M<sub>i</sub></td><td>measured (P<sub>r</sub>/P<sub>t</sub>)<sub>dB</sub>, vertical axis</td><td>−60 … −150</td></tr>
<tr><td>K<sub>dB</sub>, γ</td><td>intercept; minus the slope</td><td>unknown</td></tr>
<tr><td>σ<sub>ψ</sub>²</td><td>shadowing variance = MSE of the fit</td><td>unknown</td></tr>
<tr><td>margin x</td><td>how many dB the mean power is above the threshold</td><td>10 dB</td></tr>
</tbody></table></div>
<h4><span class="st">Step by step</span>(a) K and γ from the two normal equations</h4>
<ol>
<li><b>What</b>: write the sum of squared errors \(F(K,\gamma)=\sum_i(M_i-K+\gamma x_i)^2\). <b>Why</b>: least squares means minimising F; this is how the lecturer wrote it in class.</li>
<li><b>Set the derivative with respect to K to 0</b>: \(\sum_i(M_i-K+\gamma x_i)=0\) → \(K=\bar M+\gamma\bar x\). So the best line always passes through the mean point (x̄, M̄).</li>
<li><b>Set the derivative with respect to γ to 0</b>: \(\sum_i x_i(M_i-K+\gamma x_i)=0\); substitute the previous result and simplify to \(\gamma=-S_{xM}/S_{xx}\).</li>
<li><b>How to compute</b>: on the calculator first get four sums, then the two S values (fewer slips than computing x − x̄ point by point):</li>
</ol>
<div class="calc">x<sub>i</sub> = 10 log₁₀d<sub>i</sub>: 6.99, 13.98, 18.13, 20.41, 26.02, 30.00<br>Σx = 115.53, Σx² = 2566.75, ΣM = −640, ΣxM = −13671.57<br>S<sub>xx</sub> = Σx² − (Σx)²/6 = 2566.75 − 2224.64 = 342.11<br>S<sub>xM</sub> = ΣxM − ΣxΣM/6 = −13671.57 + 12323.49 = −1348.08<br>γ = 1348.08 / 342.11 = 3.94<br>K<sub>dB</sub> = M̄ + γx̄ = −106.67 + 3.94 × 19.26 = −30.8 dB</div>
<h4><span class="st">Step by step</span>(b) Residuals → σ → Q function</h4>
<ol>
<li><b>Residuals</b> e<sub>i</sub> = measured − predicted (listed point by point in the solution table): −1.67, +5.88, −2.77, −3.77, +3.32, −0.99. They add up to 0, a property of least squares and a handy check.</li>
<li><b>Shadowing variance</b>: σ<sub>ψ</sub>² = Σe²/6. Why divide by 6 and not 5: the slides define MSE = E[X<sub>i</sub>²], a plain average, so in the exam divide by n as the slides do.</li>
<li><b>Margin</b>: "10 dB above the minimum power due to path loss alone" → x = 10 dB. Outage = shadowing pulls the power down by more than 10 dB: \(P_{out}=P(\psi_{dB}\lt-10)=Q(10/\sigma_\psi)\).</li>
</ol>
<div class="calc">σ<sub>ψ</sub>² = 71.23 / 6 = 11.87 dB²<br>σ<sub>ψ</sub> = √11.87 = 3.45 dB<br>10 / 3.45 = 2.90<br>P<sub>out</sub> = Q(2.90) ≈ 1.85 × 10⁻³ (about 0.19%; the table entry at exactly 2.90 gives 1.87 × 10⁻³, the difference is only rounding)</div>
<h4><span class="st">Check</span>Three quick checks</h4>
<ul>
<li>The line passes through the mean point (19.26, −106.67); the residuals sum to 0.</li>
<li>γ = 3.94 lies in the urban macro-cell range 3.7–6.5 of the table on p.9, which is reasonable.</li>
<li>A 10 dB margin ≈ 2.9σ gives an outage of about two in a thousand. For comparison, a margin of 2.33σ gives 1%, so the order of magnitude fits.</li>
</ul>
<h4><span class="st">Official answer</span>Why it does not match standard least squares</h4>
<p>The official answer is K = −31.4 dB, γ = 3.86, P<sub>out</sub> = 6.19 × 10⁻⁴. Substituting the official K and γ back into the 6 points gives MSE = 13.1, larger than the least-squares 11.87, so it is not the least-squares solution for these data. Part (b) uses the lecturer's in-class MSE of 9.656: 10/√9.656 = 3.22, and the table at 3.23 gives 6.19 × 10⁻⁴. The lecturer said anything "around −31.4 and 3.86" is fine. In the exam, write every step of the method above and use your own numbers.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Using log₁₀d instead of 10 log₁₀d on the horizontal axis: γ becomes 39.4, which is clearly unreasonable.</li>
<li>The slope is −γ: the slope is −3.94, so γ = +3.94; do not write it as negative.</li>
<li>Substitute d in metres (d₀ = 1 m). The lecturer said that in this year's Quiz some students wrote 2 km as log 2.</li>
<li>The MSE is a variance: take the square root before putting it into Q; Q(10/11.87) is wrong.</li>
<li>Use the 10 dB margin directly in dB, do not convert to linear: this outage formula was derived in dB (the lecturer pointed this out in class).</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
''' + TM['p1q1'] + r'''
<div class="ans">In one line: in dB the path loss is a straight line; least squares gives K and γ, the remaining mean squared error is the shadowing variance σ², and the outage probability is Q(margin / σ).</div>''',
}

# ================================================================ P1 Q2
XPL['p1q2'] = {
'title': '知识讲解 + 详细解析：对数正态阴影的中断正算与反算',
'title_en': 'Concept + walkthrough: log-normal shadowing outage, forwards and backwards',
'zh': r'''<h4><span class="st">知识讲解</span>为什么阴影在 dB 上是高斯</h4>
<p>阴影（shadowing）是信号沿途被很多障碍物（楼、树、墙）各衰减一次：总衰减 ψ = A₁A₂…A<sub>M</sub>，是很多因子的<b>乘积</b>（讲义第 2 章 p.11）。取对数后乘积变成<b>和</b>：log ψ = Σ log A<sub>i</sub>。很多随机量相加，按中心极限定理趋向高斯，所以 ψ<sub>dB</sub> 服从高斯，ψ 本身（线性值）就叫对数正态（log-normal）。</p>
<p>结论：只要在 dB（dBm）上算，接收功率就是普通的高斯 \(P_r\sim\mathcal N(\mu_\psi,\sigma_\psi^2)\)。μ<sub>ψ</sub> 是不含阴影时的平均接收功率（阴影零均值，老师课上强调），σ<sub>ψ</sub> 是阴影的标准差，单位其实是 dB。</p>
<h4><span class="st">知识讲解</span>Q 函数与老师要求的"移项"技巧</h4>
<p>Q 函数（第 1b 章）：\(Q(x)=P(N\gt x)\)，N ~ N(0, 1)，就是标准高斯右尾的面积。Q 是减函数：Q(0) = 0.5，x 越大越小；对称性 Q(−x) = 1 − Q(x)。</p>
<p>老师要求掌握的技巧（p.14–15）：把"P<sub>r</sub> &lt; P<sub>min</sub>"整理成"随机量 &lt; −x"，随机量留在左边，其余移到右边，再用对称性写成 Q(x/σ)。</p>
<div class="tw"><table class="mini"><thead><tr><th>x</th><th>Q(x)</th><th>用途</th></tr></thead><tbody>
<tr><td>0</td><td>0.5</td><td>余量 0：一半时间中断</td></tr>
<tr><td>1</td><td>0.1587</td><td>余量 1σ</td></tr>
<tr><td>1.645</td><td>0.05</td><td>中断 5%</td></tr>
<tr><td>2.326</td><td>0.01</td><td>中断 1%（本题 (b)）</td></tr>
<tr><td>3.09</td><td>10⁻³</td><td>中断千分之一</td></tr>
</tbody></table></div>
<h4><span class="st">详细解析</span>(a) 正算：已知 μ、σ 求中断</h4>
<ol>
<li><b>写已知</b>：μ<sub>ψ</sub> = 15 dBm，σ<sub>ψ</sub> = 8 dB，门限 P<sub>min</sub> = 10 dBm。</li>
<li><b>移项</b>：P<sub>r</sub> = 15 + ψ，所以 \(P(P_r\lt10)=P(\psi\lt-5)\)。门限比均值低 5 dB。</li>
<li><b>标准化</b>：除以 σ = 8，\(P(\psi/8\lt-0.625)=P(N\gt0.625)=Q(0.625)\)。</li>
<li><b>查表</b>：表里只有两位小数，Q(0.62) = 0.2676，Q(0.63) = 0.2643，取中间得 Q(0.625) ≈ 0.266。</li>
</ol>
<div class="calc">(15 − 10) / 8 = 0.625<br>P<sub>out</sub> = Q(0.625) ≈ 0.266 ≈ 26.6%</div>
<p>合理性：余量还不到一个 σ，所以中断约四分之一；余量为 0 时是 Q(0) = 50%。</p>
<h4><span class="st">详细解析</span>(b) 反算：已知中断要求求 μ</h4>
<ol>
<li><b>列不等式</b>：把 μ 当未知数，\(Q\big((\mu_\psi-10)/4\big)\lt0.01\)。</li>
<li><b>反查 Q 表</b>：Q(2.32) = 0.0102，Q(2.33) = 0.0099，所以 Q(2.326) = 0.01。</li>
<li><b>翻转不等号</b>：Q 是减函数，"Q 值 &lt; 0.01"等价于"参数 &gt; 2.326"：\((\mu_\psi-10)/4\gt2.326\)。</li>
<li><b>解出 μ</b>：需要的余量 = 2.326 × 4 = 9.31 dB。</li>
</ol>
<div class="calc">μ<sub>ψ</sub> &gt; 10 + 4 × 2.326 = 19.3 dBm<br>代回检查：μ = 19.3 dBm 时 (19.3 − 10)/4 = 2.326，Q = 0.01 ✓</div>
<p>举一反三：σ = 8 dB 时 μ 要 &gt; 10 + 8 × 2.326 = 28.6 dBm，比 σ = 4 dB 多 9.3 dB。阴影越大，同样的中断要求要留的余量越多。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>题目把 σ 写成 dBm，实际单位是 dB：两个 dBm 相减得到的是 dB。</li>
<li>不要把 dBm 换成 mW 再算：对数正态只在 dB 上才是高斯。</li>
<li>(b) 的不等号方向：Q 是减函数，"概率 &lt; 1%"要翻成"参数 &gt; 2.326"。</li>
<li>门限在均值以下，Q 的参数是正的，结果一定小于 0.5；算出 0.734（= 1 − 0.266）说明符号弄反了。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
''' + TM['p1q2'] + r'''
<div class="ans">一句话：阴影在 dB 上是高斯，中断概率 = Q(余量 / σ)；(a) 正着查表得 26.6%，(b) 用 Q⁻¹(0.01) = 2.326 反推余量 9.3 dB，μ &gt; 19.3 dBm。</div>''',
'en': r'''<h4><span class="st">Concept</span>Why shadowing is Gaussian in dB</h4>
<p>Shadowing means the signal is attenuated once by each of many obstacles on the way (buildings, trees, walls): the total attenuation ψ = A₁A₂…A<sub>M</sub> is a <b>product</b> of many factors (lecture Ch 2 p.11). Taking the log turns the product into a <b>sum</b>: log ψ = Σ log A<sub>i</sub>. A sum of many random terms tends to a Gaussian (central limit theorem), so ψ<sub>dB</sub> is Gaussian, and ψ itself (the linear value) is called log-normal.</p>
<p>Conclusion: as long as you work in dB (dBm), the received power is an ordinary Gaussian, \(P_r\sim\mathcal N(\mu_\psi,\sigma_\psi^2)\). μ<sub>ψ</sub> is the mean received power without shadowing (shadowing has zero mean, as the lecturer stressed), and σ<sub>ψ</sub> is the standard deviation of the shadowing, whose unit is really dB.</p>
<h4><span class="st">Concept</span>The Q function and the lecturer's "rearrange" trick</h4>
<p>The Q function (Ch 1b): \(Q(x)=P(N\gt x)\) with N ~ N(0, 1), i.e. the area of the right tail of the standard Gaussian. Q is decreasing: Q(0) = 0.5 and it gets smaller as x grows; by symmetry Q(−x) = 1 − Q(x).</p>
<p>The trick the lecturer wants you to master (p.14–15): rewrite "P<sub>r</sub> &lt; P<sub>min</sub>" as "random variable &lt; −x", keeping the random variable on the left and moving everything else to the right, then use symmetry to write it as Q(x/σ).</p>
<div class="tw"><table class="mini"><thead><tr><th>x</th><th>Q(x)</th><th>Use</th></tr></thead><tbody>
<tr><td>0</td><td>0.5</td><td>zero margin: outage half the time</td></tr>
<tr><td>1</td><td>0.1587</td><td>margin of 1σ</td></tr>
<tr><td>1.645</td><td>0.05</td><td>5% outage</td></tr>
<tr><td>2.326</td><td>0.01</td><td>1% outage (part (b))</td></tr>
<tr><td>3.09</td><td>10⁻³</td><td>outage of one in a thousand</td></tr>
</tbody></table></div>
<h4><span class="st">Step by step</span>(a) Forwards: given μ and σ, find the outage</h4>
<ol>
<li><b>List the data</b>: μ<sub>ψ</sub> = 15 dBm, σ<sub>ψ</sub> = 8 dB, threshold P<sub>min</sub> = 10 dBm.</li>
<li><b>Rearrange</b>: P<sub>r</sub> = 15 + ψ, so \(P(P_r\lt10)=P(\psi\lt-5)\). The threshold is 5 dB below the mean.</li>
<li><b>Standardise</b>: divide by σ = 8, \(P(\psi/8\lt-0.625)=P(N\gt0.625)=Q(0.625)\).</li>
<li><b>Table</b>: the table has two decimals, Q(0.62) = 0.2676 and Q(0.63) = 0.2643; halfway gives Q(0.625) ≈ 0.266.</li>
</ol>
<div class="calc">(15 − 10) / 8 = 0.625<br>P<sub>out</sub> = Q(0.625) ≈ 0.266 ≈ 26.6%</div>
<p>Sanity check: the margin is less than one σ, so the outage is about a quarter; with zero margin it would be Q(0) = 50%.</p>
<h4><span class="st">Step by step</span>(b) Backwards: given the outage target, find μ</h4>
<ol>
<li><b>Write the inequality</b>: treat μ as unknown, \(Q\big((\mu_\psi-10)/4\big)\lt0.01\).</li>
<li><b>Invert with the Q table</b>: Q(2.32) = 0.0102 and Q(2.33) = 0.0099, so Q(2.326) = 0.01.</li>
<li><b>Flip the inequality</b>: Q is decreasing, so "Q value &lt; 0.01" means "argument &gt; 2.326": \((\mu_\psi-10)/4\gt2.326\).</li>
<li><b>Solve for μ</b>: the required margin is 2.326 × 4 = 9.31 dB.</li>
</ol>
<div class="calc">μ<sub>ψ</sub> &gt; 10 + 4 × 2.326 = 19.3 dBm<br>Check: with μ = 19.3 dBm, (19.3 − 10)/4 = 2.326 and Q = 0.01 ✓</div>
<p>Variation: with σ = 8 dB, μ must exceed 10 + 8 × 2.326 = 28.6 dBm, 9.3 dB more than with σ = 4 dB. The stronger the shadowing, the larger the margin needed for the same outage target.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>The question writes σ in dBm, but its unit is really dB: the difference of two dBm values is in dB.</li>
<li>Do not convert dBm to mW before computing: log-normal is Gaussian only in dB.</li>
<li>Direction of the inequality in (b): Q is decreasing, so "probability &lt; 1%" becomes "argument &gt; 2.326".</li>
<li>The threshold is below the mean, so the argument of Q is positive and the result must be below 0.5; getting 0.734 (= 1 − 0.266) means a sign is wrong.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
''' + TM['p1q2'] + r'''
<div class="ans">In one line: shadowing is Gaussian in dB and the outage probability is Q(margin / σ); (a) a forward table lookup gives 26.6%, (b) Q⁻¹(0.01) = 2.326 gives a 9.3 dB margin, so μ &gt; 19.3 dBm.</div>''',
}

# ================================================================ P1 Q3
XPL['p1q3'] = {
'title': '知识讲解 + 详细解析：时延扩展与平坦衰落的速率上限',
'title_en': 'Concept + walkthrough: delay spread and the flat-fading rate limit',
'zh': r'''<h4><span class="st">知识讲解</span>功率时延谱、平均时延、rms 时延扩展</h4>
<p>多径信道里，同一个发射脉冲经不同路径到达，最早那条记为 τ = 0，其余晚到 τ。功率时延谱（power delay profile）P<sub>r</sub>(τ) 就是"晚到 τ 的那部分有多少功率"（讲义第 2 章 p.30）。</p>
<p>把 P<sub>r</sub>(τ) 当成权重（除以总功率后就是一个概率分布），就能像求随机变量那样求两个数（p.30 的公式，考试会给，老师说不用背）：</p>
<ul>
<li>平均时延（mean delay spread）\(\mu_{T_m}=\int\tau P_r(\tau)d\tau\,/\int P_r(\tau)d\tau\)：回声"平均"晚到多久。</li>
<li>rms 时延扩展 \(\sigma_{T_m}=\sqrt{\int(\tau-\mu_{T_m})^2P_r(\tau)d\tau\,/\int P_r(\tau)d\tau}\)：回声在时间上"散得多开"，就是标准差。</li>
</ul>
<p>为什么关心 σ<sub>Tm</sub>：回声拖得比符号还长，就会漏进下一个符号，造成码间干扰（ISI），这叫频率选择性衰落（p.32）；回声相对符号很短，整个信号带宽内衰落一样，叫平坦衰落（flat fading，p.33）。讲义的经验判据（<b>蓝框，要背</b>）：</p>
<div class="tw"><table class="mini"><thead><tr><th>条件</th><th>结论</th></tr></thead><tbody>
<tr><td>σ<sub>Tm</sub>/T<sub>s</sub> &lt; 0.1</td><td>平坦衰落</td></tr>
<tr><td>σ<sub>Tm</sub>/T<sub>s</sub> ≫ 1</td><td>频率选择性衰落</td></tr>
<tr><td>介于两者之间（如 0.15）</td><td>老师说：不能下结论</td></tr>
</tbody></table></div>
<h4><span class="st">详细解析</span>(a) 均匀时延谱的 μ 和 σ</h4>
<ol>
<li><b>分母（总功率）</b>：\(\int_0^{10}1\,d\tau=10\)。<b>为什么要除</b>：P<sub>r</sub>(τ) = 1 没有归一化，不除就不是加权平均。</li>
<li><b>平均时延</b>：\(\int_0^{10}\tau\,d\tau=\tau^2/2\,\big|_0^{10}=50\)，μ = 50/10 = 5 µs。直觉：均匀分布左右对称，均值在正中间。</li>
<li><b>rms 时延扩展</b>，两种算法结果一样：
 <br>按讲义定义：\(\int_0^{10}(\tau-5)^2d\tau=\big[(\tau-5)^3/3\big]_0^{10}=125/3+125/3=83.33\)，除以 10 得 8.33 µs²；
 <br>或用 E[τ²] − μ²：\(\int_0^{10}\tau^2d\tau/10=(1000/3)/10=33.33\)，33.33 − 25 = 8.33 µs²。</li>
<li><b>开根号</b>：σ = √8.33 = 2.89 µs。捷径：[0, a] 上均匀分布的标准差 = a/√12 = 10/3.46。</li>
</ol>
<div class="calc">μ<sub>Tm</sub> = 50 / 10 = 5 µs<br>σ<sub>Tm</sub>² = 83.33 / 10 = 8.33 µs²<br>σ<sub>Tm</sub> = 2.89 µs</div>
<h4><span class="st">详细解析</span>(b) 平坦衰落允许的最高符号速率</h4>
<ol>
<li><b>套判据</b>：σ<sub>Tm</sub>/T<sub>s</sub> &lt; 0.1 → T<sub>s</sub> &gt; 10σ<sub>Tm</sub>。意思是回声最多只占一个符号的十分之一。</li>
<li><b>算 T<sub>s</sub></b>：T<sub>s</sub> &gt; 10 × 2.887 = 28.87 µs。</li>
<li><b>换成速率</b>：R<sub>s</sub> = 1/T<sub>s</sub>，符号越长速率越低，所以不等号翻过来。1/µs = 10⁶/s。</li>
</ol>
<div class="calc">T<sub>s</sub> &gt; 28.87 µs<br>R<sub>s</sub> &lt; 1 / (28.87 × 10⁻⁶ s) = 34641 sym/s ≈ 34.6 ksps</div>
<p>合理性：1 MHz 的信号（T<sub>s</sub> = 1 µs）σ/T<sub>s</sub> = 2.89 ≫ 0.1，是频率选择性，需要均衡（第 6 章）或 OFDM（第 7 章）；所以平坦衰落只能用几十 ksps 量级，对得上。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>以为 P<sub>r</sub>(τ) = 1 已经归一化，分母写 1：μ 会变成 50 µs。</li>
<li>rms 时延扩展是标准差：8.33 要开根号。</li>
<li>不等号方向：平坦衰落要求符号长、速率低，答案是上限 R<sub>s</sub> &lt; 34.6 ksps，不是"等于"。</li>
<li>题目说的 mean delay spread 就是平均时延 μ<sub>Tm</sub>，不是 σ。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
''' + TM['p1q3'] + r'''
<div class="ans">一句话：把功率时延谱当成概率分布，均值 5 µs、标准差 2.89 µs；平坦衰落要求 T<sub>s</sub> &gt; 10σ = 28.87 µs，所以 R<sub>s</sub> &lt; 34.6 ksps。</div>''',
'en': r'''<h4><span class="st">Concept</span>Power delay profile, mean delay, rms delay spread</h4>
<p>In a multipath channel one transmitted pulse arrives over different paths; the first arrival is τ = 0 and the others arrive τ later. The power delay profile P<sub>r</sub>(τ) says how much power arrives with delay τ (lecture Ch 2 p.30).</p>
<p>Treat P<sub>r</sub>(τ) as a weight (divided by the total power it is a probability distribution) and compute two numbers just as for a random variable (formulas on p.30; they are given in the exam and the lecturer said they need not be memorised):</p>
<ul>
<li>Mean delay (mean delay spread) \(\mu_{T_m}=\int\tau P_r(\tau)d\tau\,/\int P_r(\tau)d\tau\): how late the echoes arrive "on average".</li>
<li>rms delay spread \(\sigma_{T_m}=\sqrt{\int(\tau-\mu_{T_m})^2P_r(\tau)d\tau\,/\int P_r(\tau)d\tau}\): how widely the echoes are spread in time, i.e. the standard deviation.</li>
</ul>
<p>Why σ<sub>Tm</sub> matters: if the echoes last longer than a symbol they leak into the next symbol and cause inter-symbol interference (ISI); this is frequency-selective fading (p.32). If the echoes are short compared with the symbol, the fading is the same across the whole signal bandwidth: flat fading (p.33). The rule of thumb on the slides (<b>blue box, memorise it</b>):</p>
<div class="tw"><table class="mini"><thead><tr><th>Condition</th><th>Conclusion</th></tr></thead><tbody>
<tr><td>σ<sub>Tm</sub>/T<sub>s</sub> &lt; 0.1</td><td>flat fading</td></tr>
<tr><td>σ<sub>Tm</sub>/T<sub>s</sub> ≫ 1</td><td>frequency-selective fading</td></tr>
<tr><td>in between (e.g. 0.15)</td><td>the lecturer: no conclusion can be drawn</td></tr>
</tbody></table></div>
<h4><span class="st">Step by step</span>(a) μ and σ of a uniform delay profile</h4>
<ol>
<li><b>Denominator (total power)</b>: \(\int_0^{10}1\,d\tau=10\). <b>Why divide</b>: P<sub>r</sub>(τ) = 1 is not normalised; without dividing it is not a weighted average.</li>
<li><b>Mean delay</b>: \(\int_0^{10}\tau\,d\tau=\tau^2/2\,\big|_0^{10}=50\), μ = 50/10 = 5 µs. Intuition: the uniform distribution is symmetric, so the mean is in the middle.</li>
<li><b>rms delay spread</b>, two ways with the same result:
 <br>by the slide definition: \(\int_0^{10}(\tau-5)^2d\tau=\big[(\tau-5)^3/3\big]_0^{10}=125/3+125/3=83.33\), divided by 10 gives 8.33 µs²;
 <br>or with E[τ²] − μ²: \(\int_0^{10}\tau^2d\tau/10=(1000/3)/10=33.33\), and 33.33 − 25 = 8.33 µs².</li>
<li><b>Square root</b>: σ = √8.33 = 2.89 µs. Shortcut: the standard deviation of a uniform distribution on [0, a] is a/√12 = 10/3.46.</li>
</ol>
<div class="calc">μ<sub>Tm</sub> = 50 / 10 = 5 µs<br>σ<sub>Tm</sub>² = 83.33 / 10 = 8.33 µs²<br>σ<sub>Tm</sub> = 2.89 µs</div>
<h4><span class="st">Step by step</span>(b) Highest symbol rate for flat fading</h4>
<ol>
<li><b>Apply the rule</b>: σ<sub>Tm</sub>/T<sub>s</sub> &lt; 0.1 → T<sub>s</sub> &gt; 10σ<sub>Tm</sub>. The echoes may occupy at most a tenth of a symbol.</li>
<li><b>Compute T<sub>s</sub></b>: T<sub>s</sub> &gt; 10 × 2.887 = 28.87 µs.</li>
<li><b>Convert to a rate</b>: R<sub>s</sub> = 1/T<sub>s</sub>; a longer symbol means a lower rate, so the inequality flips. 1/µs = 10⁶/s.</li>
</ol>
<div class="calc">T<sub>s</sub> &gt; 28.87 µs<br>R<sub>s</sub> &lt; 1 / (28.87 × 10⁻⁶ s) = 34641 sym/s ≈ 34.6 ksps</div>
<p>Sanity check: a 1 MHz signal (T<sub>s</sub> = 1 µs) has σ/T<sub>s</sub> = 2.89 ≫ 0.1, so it is frequency-selective and needs equalisation (Ch 6) or OFDM (Ch 7); flat fading is only possible at rates of tens of ksps, which fits.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Assuming P<sub>r</sub>(τ) = 1 is already normalised and using 1 as the denominator: μ would become 50 µs.</li>
<li>The rms delay spread is a standard deviation: take the square root of 8.33.</li>
<li>Direction of the inequality: flat fading needs long symbols and a low rate, so the answer is an upper limit R<sub>s</sub> &lt; 34.6 ksps, not an equality.</li>
<li>The "mean delay spread" in the question is the mean delay μ<sub>Tm</sub>, not σ.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
''' + TM['p1q3'] + r'''
<div class="ans">In one line: treat the power delay profile as a probability distribution, mean 5 µs and standard deviation 2.89 µs; flat fading needs T<sub>s</sub> &gt; 10σ = 28.87 µs, so R<sub>s</sub> &lt; 34.6 ksps.</div>''',
}

# ================================================================ P2 Q1
XPL['p2q1'] = {
'title': '知识讲解 + 详细解析：LCR、AFD 与 ρ 的含义',
'title_en': 'Concept + walkthrough: LCR, AFD and the meaning of ρ',
'zh': r'''<h4><span class="st">知识讲解</span>电平通过率 LCR 和平均衰落时长 AFD</h4>
<p>瑞利衰落下，接收信号幅度 z(t) 随时间快速起伏，时不时掉到最低可用电平 Z<sub>min</sub> 以下（一个"坑"）。描述这些坑有两个量（讲义第 2 章 p.40–43）：</p>
<ul>
<li><b>LCR</b>（level crossing rate，电平通过率）L<sub>Z</sub>：每秒钟信号<b>往下</b>穿过 Z<sub>min</sub> 的次数，也就是每秒掉进几个坑。</li>
<li><b>AFD</b>（average fade duration，平均衰落时长）：每个坑平均待多久。定义（p.42）：在 T 秒里，总的低于时间 Σt<sub>i</sub> 除以坑的个数 L<sub>Z</sub>T。</li>
</ul>
<p>p.43 把定义改写成 AFD = P(z &lt; Z<sub>min</sub>) / L<sub>Z</sub>：低于门限的<b>时间比例</b>除以<b>每秒的坑数</b>。瑞利分布下 P(z &lt; Z<sub>min</sub>) = 1 − e<sup>−ρ²</sup>，L<sub>Z</sub> = √(2π) f<sub>m</sub> ρ e<sup>−ρ²</sup>，两者相除就是题目给的式子。</p>
<div class="tw"><table class="mini"><thead><tr><th>符号</th><th>含义</th><th>本题</th></tr></thead><tbody>
<tr><td>ρ = Z<sub>min</sub>/Z<sub>rms</sub></td><td>门限与 rms 值之比（<b>幅度</b>比）</td><td>0.1，即低 20 dB</td></tr>
<tr><td>f<sub>m</sub>（= f<sub>D</sub>）</td><td>最大多普勒频移，信道变化有多快，f<sub>D</sub> = v/λ</td><td>50 Hz</td></tr>
</tbody></table></div>
<p>老师课上强调：LCR、AFD 公式考试会给，但要会用一句话解释 ρ = Z<sub>min</sub>/Z<sub>rms</sub> 和 f<sub>m</sub>；而且这两个公式<b>只适用于瑞利衰落</b>，题目没说瑞利时要按定义算（今年 Quiz 第 2 题很多人在这里丢分）。</p>
<h4><span class="st">详细解析</span>一步一步代公式</h4>
<ol>
<li><b>定 ρ</b>：最低信号强度是 rms 值的 0.1 倍。signal strength 指幅度，所以 ρ = 0.1；换成 dB 是 20 log₁₀0.1 = −20 dB，是很深的坑。</li>
<li><b>分子</b>：先平方 ρ² = 0.01，再 e<sup>0.01</sup> − 1 = 0.01005。计算器提示：x 很小时 e<sup>x</sup> − 1 ≈ x，所以约等于 0.01。</li>
<li><b>分母</b>：√(2π) = 2.5066，× 50 × 0.1 = 12.53。</li>
<li><b>相除</b>，再把秒换成毫秒。</li>
</ol>
<div class="calc">ρ² = 0.01，e<sup>0.01</sup> − 1 = 0.01005<br>√(2π) × 50 × 0.1 = 2.5066 × 5 = 12.53<br>AFD = 0.01005 / 12.53 = 8.0 × 10⁻⁴ s ≈ 0.8 ms</div>
<h4><span class="st">自检</span>用 LCR 反过来验证</h4>
<div class="calc">LCR = 12.53 × e<sup>−0.01</sup> = 12.41 次/秒<br>AFD × LCR = 8.02 × 10⁻⁴ × 12.41 = 0.00995 = 1 − e<sup>−0.01</sup></div>
<p>意思是：每秒掉坑约 12 次，每次约 0.8 ms，合起来约 1% 的时间低于门限，正好等于瑞利分布 P(z &lt; Z<sub>min</sub>)。另一个检查：ρ 很小时 AFD ≈ ρ/(√(2π) f<sub>D</sub>) = 0.1/125.3 = 7.98 × 10⁻⁴ s，几乎一样。</p>
<p>工程意义：一次衰落吞掉的符号数 = AFD × R<sub>s</sub>（老师课上讲过）。举例：若符号速率 10 ksps，0.8 ms 就连错约 8 个符号，交织深度要比这个大。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>ρ 是幅度比：rms 值的 0.1 倍 → ρ = 0.1。若题目说"功率是 0.1 倍"，ρ = √0.1 = 0.316，AFD 变成 2.65 ms，差 3 倍多。</li>
<li>指数是 ρ² 不是 ρ：e<sup>0.1</sup> − 1 = 0.105 会让答案大 10 倍。</li>
<li>题目给 "20 dB below rms" 时，ρ = 10<sup>−20/20</sup> = 0.1（幅度用 20 log）。</li>
<li>没说瑞利衰落就不能套这个公式，要按定义：总低于时间 ÷ 次数。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
''' + TM['p2q1'] + r'''
<div class="ans">一句话：AFD = 低于门限的时间比例 ÷ 每秒掉坑次数；ρ = Z<sub>min</sub>/Z<sub>rms</sub> = 0.1（幅度比），代入瑞利公式得 0.8 ms。</div>''',
'en': r'''<h4><span class="st">Concept</span>Level crossing rate (LCR) and average fade duration (AFD)</h4>
<p>In Rayleigh fading the received amplitude z(t) fluctuates quickly and now and then drops below the minimum usable level Z<sub>min</sub> (a "fade"). Two quantities describe these fades (lecture Ch 2 p.40–43):</p>
<ul>
<li><b>LCR</b> (level crossing rate) L<sub>Z</sub>: the number of times per second the signal crosses Z<sub>min</sub> <b>downwards</b>, i.e. how many fades per second.</li>
<li><b>AFD</b> (average fade duration): how long each fade lasts on average. Definition (p.42): over T seconds, the total time below, Σt<sub>i</sub>, divided by the number of fades L<sub>Z</sub>T.</li>
</ul>
<p>p.43 rewrites the definition as AFD = P(z &lt; Z<sub>min</sub>) / L<sub>Z</sub>: the <b>fraction of time</b> below the threshold divided by the <b>number of fades per second</b>. For Rayleigh, P(z &lt; Z<sub>min</sub>) = 1 − e<sup>−ρ²</sup> and L<sub>Z</sub> = √(2π) f<sub>m</sub> ρ e<sup>−ρ²</sup>; dividing gives the formula in the question.</p>
<div class="tw"><table class="mini"><thead><tr><th>Symbol</th><th>Meaning</th><th>Here</th></tr></thead><tbody>
<tr><td>ρ = Z<sub>min</sub>/Z<sub>rms</sub></td><td>threshold over rms value (an <b>amplitude</b> ratio)</td><td>0.1, i.e. 20 dB down</td></tr>
<tr><td>f<sub>m</sub> (= f<sub>D</sub>)</td><td>maximum Doppler shift, how fast the channel changes, f<sub>D</sub> = v/λ</td><td>50 Hz</td></tr>
</tbody></table></div>
<p>The lecturer stressed in class: the LCR and AFD formulas are given in the exam, but you must be able to explain ρ = Z<sub>min</sub>/Z<sub>rms</sub> and f<sub>m</sub> in one sentence; and the two formulas <b>apply only to Rayleigh fading</b>. If the question does not say Rayleigh, use the definitions (many students lost marks on this in Q2 of this year's Quiz).</p>
<h4><span class="st">Step by step</span>Substituting into the formula</h4>
<ol>
<li><b>Find ρ</b>: the minimum signal strength is 0.1 of the rms value. Signal strength means amplitude, so ρ = 0.1; in dB that is 20 log₁₀0.1 = −20 dB, a deep fade.</li>
<li><b>Numerator</b>: square first, ρ² = 0.01, then e<sup>0.01</sup> − 1 = 0.01005. Calculator hint: for small x, e<sup>x</sup> − 1 ≈ x, so it is about 0.01.</li>
<li><b>Denominator</b>: √(2π) = 2.5066, × 50 × 0.1 = 12.53.</li>
<li><b>Divide</b>, then convert seconds to milliseconds.</li>
</ol>
<div class="calc">ρ² = 0.01, e<sup>0.01</sup> − 1 = 0.01005<br>√(2π) × 50 × 0.1 = 2.5066 × 5 = 12.53<br>AFD = 0.01005 / 12.53 = 8.0 × 10⁻⁴ s ≈ 0.8 ms</div>
<h4><span class="st">Check</span>Verify with the LCR</h4>
<div class="calc">LCR = 12.53 × e<sup>−0.01</sup> = 12.41 crossings/s<br>AFD × LCR = 8.02 × 10⁻⁴ × 12.41 = 0.00995 = 1 − e<sup>−0.01</sup></div>
<p>Meaning: about 12 fades per second, each about 0.8 ms, so the signal is below the threshold about 1% of the time, exactly the Rayleigh P(z &lt; Z<sub>min</sub>). Another check: for small ρ, AFD ≈ ρ/(√(2π) f<sub>D</sub>) = 0.1/125.3 = 7.98 × 10⁻⁴ s, almost the same.</p>
<p>Engineering meaning: symbols lost per fade = AFD × R<sub>s</sub> (covered in class). Example: at 10 ksps, 0.8 ms wipes out about 8 consecutive symbols, so the interleaver depth must be larger than that.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>ρ is an amplitude ratio: 0.1 of the rms value → ρ = 0.1. If a question says "0.1 of the power", ρ = √0.1 = 0.316 and the AFD becomes 2.65 ms, more than 3 times larger.</li>
<li>The exponent is ρ², not ρ: e<sup>0.1</sup> − 1 = 0.105 would make the answer 10 times too large.</li>
<li>If the question says "20 dB below rms", ρ = 10<sup>−20/20</sup> = 0.1 (amplitudes use 20 log).</li>
<li>Without Rayleigh fading this formula does not apply; use the definition: total time below ÷ number of fades.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
''' + TM['p2q1'] + r'''
<div class="ans">In one line: AFD = fraction of time below the threshold ÷ fades per second; ρ = Z<sub>min</sub>/Z<sub>rms</sub> = 0.1 (an amplitude ratio), and the Rayleigh formula gives 0.8 ms.</div>''',
}

# ================================================================ P3 Q1
XPL['p3q1'] = {
'title': '知识讲解 + 详细解析：信号空间、正交归一基与维数',
'title_en': 'Concept + walkthrough: signal space, orthonormal basis and dimension',
'zh': r'''<h4><span class="st">知识讲解</span>把波形当成向量：信号空间</h4>
<p>讲义第 3 章 p.4–8 的核心思想：M 个有限能量的信号 s<sub>i</sub>(t) 都可以写成 D 个基函数（basis function）的线性组合 \(s_i(t)=\sum_{j=1}^{D}s_{ij}\psi_j(t)\)，D ≤ M。这和平面上的向量一模一样：ψ<sub>j</sub> 是坐标轴，s<sub>ij</sub> 是坐标。</p>
<div class="tw"><table class="mini"><thead><tr><th>平面向量</th><th>信号空间</th></tr></thead><tbody>
<tr><td>单位向量 x̂、ŷ</td><td>基函数 ψ₁(t)、ψ₂(t)</td></tr>
<tr><td>点积 a·b</td><td>内积 \(\langle a,b\rangle=\int_0^Ta(t)b(t)dt\)（相乘再积分）</td></tr>
<tr><td>x̂·ŷ = 0，x̂·x̂ = 1</td><td>正交归一（orthonormal）：\(\int_0^T\psi_i\psi_j\,dt=1\)（i = j），0（i ≠ j）</td></tr>
<tr><td>坐标 = 向量在轴上的投影</td><td>\(s_{ij}=\int_0^Ts_i(t)\psi_j(t)dt\)</td></tr>
<tr><td>向量长度²</td><td>信号能量 E = Σ<sub>j</sub>s<sub>ij</sub>²</td></tr>
</tbody></table></div>
<p>维数 D = 需要几个坐标轴，和信号有多少个无关。把所有信号画成点就是星座图（signal constellation，p.8）：PAM 是 1 维（p.9），PSK、QAM 是 2 维（p.10–11）。老师课上强调：基函数是<b>正交归一</b>的，不只是正交；还要会判断一个调制方式是几维。</p>
<h4><span class="st">详细解析</span>(a) 找基：拆开 → 验正交 → 归一化</h4>
<ol>
<li><b>做什么</b>：用和角公式拆开 \(A_i\cos(2\pi t/T+\phi_j)=A_i\cos\phi_j\cdot\cos(2\pi t/T)-A_i\sin\phi_j\cdot\sin(2\pi t/T)\)。<b>为什么</b>：把"携带信息、不随 t 变的数"（A<sub>i</sub>cosφ<sub>j</sub>、A<sub>i</sub>sinφ<sub>j</sub>）和"随 t 变的波形"分开。不随 t 变的数就是坐标，随 t 变的波形就是坐标轴的候选。</li>
<li><b>候选方向</b>：所有信号都只用到 cos(2πt/T) 和 sin(2πt/T) 两个波形。</li>
<li><b>验正交</b>：用 sin 2a = 2 sin a cos a，\(\int_0^T\cos(2\pi t/T)\sin(2\pi t/T)dt=\tfrac12\int_0^T\sin(4\pi t/T)dt=0\)，因为 sin(4πt/T) 在 0 到 T 上正好两个完整周期，正负面积抵消。</li>
<li><b>求能量</b>：用 cos²a = (1 + cos 2a)/2，\(\int_0^T\cos^2(2\pi t/T)dt=\tfrac T2+\tfrac12\int_0^T\cos(4\pi t/T)dt=T/2\)；sin² 同样是 T/2。</li>
<li><b>归一化</b>：能量是 T/2，要变成 1，就除以 √(T/2)，即乘 √(2/T)。</li>
</ol>
<div class="calc">∫₀<sup>T</sup> cos·sin dt = 0（正交）<br>∫₀<sup>T</sup> cos² dt = ∫₀<sup>T</sup> sin² dt = T/2<br>ψ₁(t) = √(2/T) cos(2πt/T)，ψ₂(t) = √(2/T) sin(2πt/T)，0 ≤ t ≤ T</div>
<p>顺便得到每个信号的坐标：s<sub>i</sub> = (A<sub>i</sub>cosφ<sub>j</sub>√(T/2), −A<sub>i</sub>sinφ<sub>j</sub>√(T/2))，到原点的距离 A<sub>i</sub>√(T/2) = √E，正好是信号能量的平方根，可以用来自检。</p>
<h4><span class="st">详细解析</span>(b) 维数</h4>
<ol>
<li>(a) 用了两个基函数，所以 D = 2。</li>
<li><b>为什么不是更多</b>：不管 A<sub>i</sub>、φ<sub>j</sub> 取多少个值，所有信号都在这个平面里。</li>
<li><b>为什么不是 1</b>：φ 在变，cos 和 sin 两个分量都会出现，而且 sin 不能由 cos 表示（两者正交）。如果 φ 固定（只调幅度），就只剩一个方向，D = 1（PAM）。</li>
</ol>
<p>老师说这类题可以直接出成考题，并会追问"还能怎么问"，比如"这是什么调制"：幅度和相位都调 → QAM。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>归一化系数写成 1/√T 或 √T：cos² 在一个周期上积分是 T/2，不是 T，系数是 √(2/T)。</li>
<li>只验了正交没归一化（或反过来），两个条件都要写。</li>
<li>以为 A<sub>i</sub>、φ<sub>j</sub> 取值越多维数越大：维数只看基函数个数。</li>
<li>sin 前面的负号放进坐标里，基函数本身取 +sin 或 −sin 都对（基不唯一，旋转一下仍正交归一），写最自然的那组即可。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
''' + TM['p3q1'] + r'''
<div class="ans">一句话：用和角公式把信号拆成 cos 和 sin 两个方向，它们正交、能量各为 T/2，乘 √(2/T) 归一化就是基；两个基函数，维数是 2。</div>''',
'en': r'''<h4><span class="st">Concept</span>Waveforms as vectors: the signal space</h4>
<p>The core idea of lecture Ch 3 p.4–8: M finite-energy signals s<sub>i</sub>(t) can all be written as linear combinations of D basis functions, \(s_i(t)=\sum_{j=1}^{D}s_{ij}\psi_j(t)\), with D ≤ M. This is exactly like vectors in a plane: ψ<sub>j</sub> are the axes and s<sub>ij</sub> are the coordinates.</p>
<div class="tw"><table class="mini"><thead><tr><th>Vectors in a plane</th><th>Signal space</th></tr></thead><tbody>
<tr><td>unit vectors x̂, ŷ</td><td>basis functions ψ₁(t), ψ₂(t)</td></tr>
<tr><td>dot product a·b</td><td>inner product \(\langle a,b\rangle=\int_0^Ta(t)b(t)dt\) (multiply, then integrate)</td></tr>
<tr><td>x̂·ŷ = 0, x̂·x̂ = 1</td><td>orthonormal: \(\int_0^T\psi_i\psi_j\,dt=1\) (i = j), 0 (i ≠ j)</td></tr>
<tr><td>coordinate = projection on an axis</td><td>\(s_{ij}=\int_0^Ts_i(t)\psi_j(t)dt\)</td></tr>
<tr><td>length² of the vector</td><td>signal energy E = Σ<sub>j</sub>s<sub>ij</sub>²</td></tr>
</tbody></table></div>
<p>The dimension D is the number of axes needed; it has nothing to do with how many signals there are. Drawing all signals as points gives the signal constellation (p.8): PAM is 1-dimensional (p.9), PSK and QAM are 2-dimensional (p.10–11). The lecturer stressed in class that the basis functions are <b>orthonormal</b>, not just orthogonal, and that you should be able to tell how many dimensions a modulation has.</p>
<h4><span class="st">Step by step</span>(a) Finding the basis: expand → check orthogonality → normalise</h4>
<ol>
<li><b>What</b>: expand with the angle-sum formula, \(A_i\cos(2\pi t/T+\phi_j)=A_i\cos\phi_j\cdot\cos(2\pi t/T)-A_i\sin\phi_j\cdot\sin(2\pi t/T)\). <b>Why</b>: it separates the numbers that carry information and do not depend on t (A<sub>i</sub>cosφ<sub>j</sub>, A<sub>i</sub>sinφ<sub>j</sub>) from the waveforms that depend on t. The numbers are coordinates; the waveforms are the candidate axes.</li>
<li><b>Candidate directions</b>: every signal uses only the two waveforms cos(2πt/T) and sin(2πt/T).</li>
<li><b>Orthogonality</b>: with sin 2a = 2 sin a cos a, \(\int_0^T\cos(2\pi t/T)\sin(2\pi t/T)dt=\tfrac12\int_0^T\sin(4\pi t/T)dt=0\), because sin(4πt/T) has exactly two full periods on 0 to T and the positive and negative areas cancel.</li>
<li><b>Energy</b>: with cos²a = (1 + cos 2a)/2, \(\int_0^T\cos^2(2\pi t/T)dt=\tfrac T2+\tfrac12\int_0^T\cos(4\pi t/T)dt=T/2\); sin² also gives T/2.</li>
<li><b>Normalise</b>: the energy is T/2 and must become 1, so divide by √(T/2), i.e. multiply by √(2/T).</li>
</ol>
<div class="calc">∫₀<sup>T</sup> cos·sin dt = 0 (orthogonal)<br>∫₀<sup>T</sup> cos² dt = ∫₀<sup>T</sup> sin² dt = T/2<br>ψ₁(t) = √(2/T) cos(2πt/T), ψ₂(t) = √(2/T) sin(2πt/T), 0 ≤ t ≤ T</div>
<p>The coordinates of each signal follow directly: s<sub>i</sub> = (A<sub>i</sub>cosφ<sub>j</sub>√(T/2), −A<sub>i</sub>sinφ<sub>j</sub>√(T/2)). Its distance from the origin, A<sub>i</sub>√(T/2) = √E, is the square root of the signal energy, a useful self-check.</p>
<h4><span class="st">Step by step</span>(b) Dimension</h4>
<ol>
<li>Part (a) uses two basis functions, so D = 2.</li>
<li><b>Why not more</b>: however many values A<sub>i</sub> and φ<sub>j</sub> take, all signals lie in this plane.</li>
<li><b>Why not 1</b>: φ varies, so both the cos and the sin components appear, and sin cannot be expressed with cos (they are orthogonal). If φ were fixed (amplitude only), one direction would remain and D = 1 (PAM).</li>
</ol>
<p>The lecturer said this type of question can appear directly in the exam, with follow-ups such as "which modulation is this?": amplitude and phase both modulated → QAM.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Writing the normalisation factor as 1/√T or √T: cos² integrates to T/2 over one period, not T, so the factor is √(2/T).</li>
<li>Checking orthogonality but not normalisation (or the other way round); both conditions must be shown.</li>
<li>Thinking more values of A<sub>i</sub>, φ<sub>j</sub> give more dimensions: the dimension is only the number of basis functions.</li>
<li>The minus sign in front of sin goes into the coordinate; taking +sin or −sin as the basis function are both correct (the basis is not unique, a rotation is still orthonormal), so write the most natural pair.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
''' + TM['p3q1'] + r'''
<div class="ans">In one line: the angle-sum formula splits the signal into a cos and a sin direction; they are orthogonal with energy T/2 each, so multiplying by √(2/T) gives the basis; two basis functions, so the dimension is 2.</div>''',
}

# ================================================================ P3 Q2
XPL['p3q2'] = {
'title': '知识讲解 + 详细解析：方差不等时的 ML 门限与误码率',
'title_en': 'Concept + walkthrough: ML threshold and error rate with unequal noise variances',
'zh': r'''<h4><span class="st">知识讲解</span>ML 检测：比较两条似然曲线</h4>
<p>最大似然（maximum likelihood, ML）检测（讲义第 3 章 p.18–20）：收到 y 以后，对每个可能发送的 x 算似然 f(y | x)，"如果发的是 x，收到这个 y 的可能性有多大"，选最大的那个。由贝叶斯公式（p.20），后验 P(x | y) ∝ f(y | x)P(x)；0、1 等概时 P(x) 相同，所以 ML = MAP（最大后验），也就是误码率最小的检测器。</p>
<p>本题的似然：y = x + w，所以 y 的 PDF 就是噪声的 PDF 平移到 x（老师课上的说法）：发 0 时 \(y\sim\mathcal N(0,\sigma_0^2)\)，发 1 时 \(y\sim\mathcal N(1,\sigma_1^2)\)。</p>
<div class="tw"><table class="mini"><thead><tr><th>情况</th><th>门限在哪</th><th>原因</th></tr></thead><tbody>
<tr><td>σ₀ = σ₁（讲义的标准情况）</td><td>中点 0.5</td><td>ML = 最小距离，选离 y 最近的点</td></tr>
<tr><td>σ₁ &gt; σ₀（本题）</td><td>两条 PDF 的交点，比 0.5 靠近 0</td><td>发 1 的 PDF 又矮又宽，在中点处反而更高</td></tr>
</tbody></table></div>
<p>例：σ₀² = 0.1、σ₁² = 0.4 时，在 y = 0.5 处 f(0.5 | 0) = 0.361，f(0.5 | 1) = 0.461，判 1 的似然更大，所以门限要往 0 那边移。</p>
<h4><span class="st">详细解析</span>(a) 推导判决门限</h4>
<ol>
<li><b>写两个似然（系数不能丢）</b>：判 1 当 \(\frac{1}{\sqrt{2\pi}\sigma_1}e^{-(y-1)^2/2\sigma_1^2}\gt\frac{1}{\sqrt{2\pi}\sigma_0}e^{-y^2/2\sigma_0^2}\)。√(2π) 两边约掉，1/σ 约不掉。</li>
<li><b>取 ln</b>：ln 是增函数，不改变不等号方向，指数变成多项式：\(g(y)=\frac{y^2}{2\sigma_0^2}-\frac{(y-1)^2}{2\sigma_1^2}+\ln\frac{\sigma_0}{\sigma_1}\gt0\)。</li>
<li><b>整理成二次式</b>：两边乘 2σ₀²σ₁²（正数，不等号不变）：\((\sigma_1^2-\sigma_0^2)y^2+2\sigma_0^2y-\sigma_0^2-\sigma_0^2\sigma_1^2\ln(\sigma_1^2/\sigma_0^2)\gt0\)。</li>
<li><b>求门限</b>：二次项系数 σ₁² − σ₀² &gt; 0，抛物线开口向上，两根之外 g &gt; 0。取 0 和 1 之间的那个根作门限 ỹ（老师说门限只取正根）：
 <br>\(\tilde y=\dfrac{-\sigma_0^2+\sqrt{\sigma_0^4+(\sigma_1^2-\sigma_0^2)\big(\sigma_0^2+\sigma_0^2\sigma_1^2\ln(\sigma_1^2/\sigma_0^2)\big)}}{\sigma_1^2-\sigma_0^2}\)</li>
<li><b>判决规则</b>：y &gt; ỹ 判 1，y &lt; ỹ 判 0。</li>
</ol>
<div class="calc">数值例 σ₀² = 0.1，σ₁² = 0.4：<br>g(y) = 3.75y² + 2.5y − 1.943<br>两根：ỹ = 0.46（门限），另一根 −1.13<br>若忘了系数 1/σ：门限变成 0.33（错）</div>
<p>负根 −1.13 是什么：y 极负时，宽的 N(1, σ₁²) 尾巴比窄的 N(0, σ₀²) 厚，所以那里也判 1。但发 0 时 y 落到那里的概率只有约 2 × 10⁻⁴，标准答案忽略它，误码率只差约 10⁻⁴。</p>
<p><b>自检</b>：σ₀ = σ₁ 时二次项消失，剩 2σ₀²y − σ₀² = 0，ỹ = 0.5，回到中点 ✓。</p>
<h4><span class="st">详细解析</span>(b) 误码率：两种错误分别算</h4>
<ol>
<li><b>全概率</b>：\(P_e=P(x=0)P(\text{判 1}\mid0)+P(x=1)P(\text{判 0}\mid1)\)，两个先验都是 ½。</li>
<li><b>发 0 判成 1</b>：积分区间是 ỹ 到 ∞（老师强调要写对区间）。换元 u = y/σ₀：\(P(y\gt\tilde y\mid0)=Q(\tilde y/\sigma_0)\)。</li>
<li><b>发 1 判成 0</b>：区间 −∞ 到 ỹ。换元 u = (y − 1)/σ₁，再用对称性：\(P(y\lt\tilde y\mid1)=P(u\lt(\tilde y-1)/\sigma_1)=Q\big((1-\tilde y)/\sigma_1\big)\)。</li>
<li><b>合起来</b>：\(P_e=\tfrac12\big[Q(\tilde y/\sigma_0)+Q\big((1-\tilde y)/\sigma_1\big)\big]\)。注意两项用各自的 σ。</li>
</ol>
<div class="calc">数值例：ỹ/σ₀ = 0.460/0.3162 = 1.455，(1 − ỹ)/σ₁ = 0.540/0.6325 = 0.854<br>P<sub>e</sub> = ½[Q(1.455) + Q(0.854)] = ½[0.0728 + 0.1966] = 0.135<br>对比用中点 0.5：½[Q(1.581) + Q(0.791)] = 0.136，ML 门限更好一点 ✓</div>
<p>老师说 (b) 这种"写积分区间 → 换元成 Q 函数"的步骤后面 Practice 还会反复出现，期末经常以不同形式考到。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>只比较指数、丢掉系数 1/σ₀、1/σ₁：门限会错（数值例里 0.33 对 0.46）。</li>
<li>两种错误用同一个 σ：发 0 用 σ₀，发 1 用 σ₁。</li>
<li>二次方程有两个根，取 0 和 1 之间的那个；ln(σ₀/σ₁) 是负数，别丢符号。</li>
<li>直接写门限 0.5：那只在方差相等时成立。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
''' + TM['p3q2'] + r'''
<div class="ans">一句话：ML 门限是两条似然曲线的交点，方差不等时要连 1/σ 系数一起比，解二次方程取 0 和 1 之间的根；误码率 = ½[Q(ỹ/σ₀) + Q((1 − ỹ)/σ₁)]。</div>''',
'en': r'''<h4><span class="st">Concept</span>ML detection: compare two likelihood curves</h4>
<p>Maximum likelihood (ML) detection (lecture Ch 3 p.18–20): after receiving y, compute for each possible x the likelihood f(y | x), "how likely is this y if x was sent", and choose the largest. By Bayes' rule (p.20) the posterior P(x | y) ∝ f(y | x)P(x); with 0 and 1 equally likely, P(x) is the same for both, so ML = MAP (maximum a posteriori), the detector with the smallest error probability.</p>
<p>The likelihoods here: y = x + w, so the PDF of y is the noise PDF shifted to x (as the lecturer put it): if 0 is sent \(y\sim\mathcal N(0,\sigma_0^2)\); if 1 is sent \(y\sim\mathcal N(1,\sigma_1^2)\).</p>
<div class="tw"><table class="mini"><thead><tr><th>Case</th><th>Where the threshold is</th><th>Reason</th></tr></thead><tbody>
<tr><td>σ₀ = σ₁ (standard case in the slides)</td><td>the midpoint 0.5</td><td>ML = minimum distance, choose the point closest to y</td></tr>
<tr><td>σ₁ &gt; σ₀ (this question)</td><td>where the two PDFs cross, closer to 0 than 0.5</td><td>the PDF for 1 is lower and wider, yet higher at the midpoint</td></tr>
</tbody></table></div>
<p>Example: with σ₀² = 0.1 and σ₁² = 0.4, at y = 0.5 we have f(0.5 | 0) = 0.361 and f(0.5 | 1) = 0.461; deciding 1 is more likely there, so the threshold moves towards 0.</p>
<h4><span class="st">Step by step</span>(a) Deriving the threshold</h4>
<ol>
<li><b>Write both likelihoods (keep the coefficients)</b>: decide 1 if \(\frac{1}{\sqrt{2\pi}\sigma_1}e^{-(y-1)^2/2\sigma_1^2}\gt\frac{1}{\sqrt{2\pi}\sigma_0}e^{-y^2/2\sigma_0^2}\). √(2π) cancels on both sides; 1/σ does not.</li>
<li><b>Take ln</b>: ln is increasing, so the inequality keeps its direction, and the exponents become polynomials: \(g(y)=\frac{y^2}{2\sigma_0^2}-\frac{(y-1)^2}{2\sigma_1^2}+\ln\frac{\sigma_0}{\sigma_1}\gt0\).</li>
<li><b>Rewrite as a quadratic</b>: multiply both sides by 2σ₀²σ₁² (positive, inequality unchanged): \((\sigma_1^2-\sigma_0^2)y^2+2\sigma_0^2y-\sigma_0^2-\sigma_0^2\sigma_1^2\ln(\sigma_1^2/\sigma_0^2)\gt0\).</li>
<li><b>Find the threshold</b>: the y² coefficient σ₁² − σ₀² is positive, so the parabola opens upwards and g &gt; 0 outside the two roots. Take the root between 0 and 1 as the threshold ỹ (the lecturer said to take only the positive root):
 <br>\(\tilde y=\dfrac{-\sigma_0^2+\sqrt{\sigma_0^4+(\sigma_1^2-\sigma_0^2)\big(\sigma_0^2+\sigma_0^2\sigma_1^2\ln(\sigma_1^2/\sigma_0^2)\big)}}{\sigma_1^2-\sigma_0^2}\)</li>
<li><b>Decision rule</b>: decide 1 if y &gt; ỹ, decide 0 if y &lt; ỹ.</li>
</ol>
<div class="calc">Numerical example σ₀² = 0.1, σ₁² = 0.4:<br>g(y) = 3.75y² + 2.5y − 1.943<br>roots: ỹ = 0.46 (threshold), the other root −1.13<br>forgetting the 1/σ coefficients: the threshold becomes 0.33 (wrong)</div>
<p>What the negative root −1.13 means: for very negative y, the wide N(1, σ₁²) has a heavier tail than the narrow N(0, σ₀²), so 1 is decided there as well. But when 0 is sent, y lands there with probability only about 2 × 10⁻⁴; the standard answer ignores it and the error rate changes by only about 10⁻⁴.</p>
<p><b>Check</b>: with σ₀ = σ₁ the quadratic term vanishes, leaving 2σ₀²y − σ₀² = 0, so ỹ = 0.5, back to the midpoint ✓.</p>
<h4><span class="st">Step by step</span>(b) Error probability: the two error types separately</h4>
<ol>
<li><b>Total probability</b>: \(P_e=P(x=0)P(\text{decide }1\mid0)+P(x=1)P(\text{decide }0\mid1)\), both priors ½.</li>
<li><b>0 sent, 1 decided</b>: the integration range is ỹ to ∞ (the lecturer stressed getting the range right). Substitute u = y/σ₀: \(P(y\gt\tilde y\mid0)=Q(\tilde y/\sigma_0)\).</li>
<li><b>1 sent, 0 decided</b>: the range is −∞ to ỹ. Substitute u = (y − 1)/σ₁ and use symmetry: \(P(y\lt\tilde y\mid1)=P(u\lt(\tilde y-1)/\sigma_1)=Q\big((1-\tilde y)/\sigma_1\big)\).</li>
<li><b>Combine</b>: \(P_e=\tfrac12\big[Q(\tilde y/\sigma_0)+Q\big((1-\tilde y)/\sigma_1\big)\big]\). Each term uses its own σ.</li>
</ol>
<div class="calc">Numerical example: ỹ/σ₀ = 0.460/0.3162 = 1.455, (1 − ỹ)/σ₁ = 0.540/0.6325 = 0.854<br>P<sub>e</sub> = ½[Q(1.455) + Q(0.854)] = ½[0.0728 + 0.1966] = 0.135<br>With the midpoint 0.5 instead: ½[Q(1.581) + Q(0.791)] = 0.136, so the ML threshold is slightly better ✓</div>
<p>The lecturer said this step in (b), "write the integration range → substitute to get a Q function", comes back again and again in later Practices and often appears in the final in different forms.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Comparing only the exponents and dropping the coefficients 1/σ₀, 1/σ₁: the threshold is wrong (0.33 instead of 0.46 in the example).</li>
<li>Using the same σ for both errors: use σ₀ when 0 is sent and σ₁ when 1 is sent.</li>
<li>The quadratic has two roots; take the one between 0 and 1. ln(σ₀/σ₁) is negative, keep its sign.</li>
<li>Writing the threshold as 0.5: that holds only for equal variances.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
''' + TM['p3q2'] + r'''
<div class="ans">In one line: the ML threshold is where the two likelihood curves cross; with unequal variances compare them including the 1/σ coefficients and take the root of the quadratic between 0 and 1; the error rate is ½[Q(ỹ/σ₀) + Q((1 − ỹ)/σ₁)].</div>''',
}

# ================================================================ P3 Q3
XPL['p3q3'] = {
'title': '知识讲解 + 详细解析：时延扩展误码平台与 QPSK 速率',
'title_en': 'Concept + walkthrough: delay-spread error floor and QPSK data rate',
'zh': r'''<h4><span class="st">知识讲解</span>什么是不可消除的误码平台</h4>
<p>平时误码率随 SNR 增大一直下降。但有些错误不是噪声造成的，SNR → ∞ 也消不掉，误码率停在一个"平台"上，叫不可消除的误码平台（irreducible error floor，讲义第 3 章 p.35）。两个来源：</p>
<div class="tw"><table class="mini"><thead><tr><th>来源</th><th>平台近似式</th><th>要求符号</th><th>给出速率</th></tr></thead><tbody>
<tr><td>多普勒扩展（信道在一个符号内就变了）</td><td>0.5(πf<sub>D</sub>T<sub>b</sub>)²（讲义 p.35–36，DPSK）</td><td>短</td><td>下限</td></tr>
<tr><td>时延扩展（回声拖进下一个符号，ISI）</td><td>(σ<sub>Tm</sub>/T<sub>b</sub>)²（本题给出，BPSK）</td><td>长</td><td>上限</td></tr>
</tbody></table></div>
<p>本题的时延扩展平台公式讲义正文没有，由题目给出；老师说误码平台公式是框了但不是蓝框，不用背，会写在题目里。</p>
<p>ISI 的物理图像：一个符号的能量有一部分晚到，落进下一个符号的时间里，和下一个符号叠在一起。接收机按"这一段时间里收到什么"做判决，被拖进来的上一个符号就像一个和数据有关的干扰。信号功率加大，拖进来的回声也同比例加大，比值不变，所以加功率消不掉，只能让符号变长（回声占比变小），或者用均衡、OFDM 把回声处理掉。</p>
<p>公式的含义：ISI 有多严重，取决于"回声长度 σ<sub>Tm</sub> 相对一个<b>符号</b>有多长"。BPSK 一个符号就是一个比特，所以公式里写 T<sub>b</sub>；换成 QPSK（M = 4，每符号 log₂4 = 2 bit），起作用的是符号时长 T<sub>s</sub>。速率换算：R<sub>b</sub> = log₂M / T<sub>s</sub>。</p>
<h4><span class="st">详细解析</span>从平台要求反推最短符号时长</h4>
<ol>
<li><b>写已知</b>：σ<sub>Tm</sub> = 3 µs，平台要求 P<sub>floor</sub> = 10⁻³，调制 QPSK。</li>
<li><b>换符号</b>：QPSK 用 \(P_{floor}\approx(\sigma_{T_m}/T_s)^2\)。<b>为什么</b>：ISI 只看回声相对符号的长度，和一个符号装几个比特无关。</li>
<li><b>开根号</b>：\((3\,\mu s/T_s)^2=10^{-3}\) → \(3\,\mu s/T_s=\sqrt{10^{-3}}=0.0316\)。计算器提示：√10⁻³ = 10<sup>−1.5</sup>。</li>
<li><b>解 T<sub>s</sub></b>：T<sub>s</sub> = 3 / 0.0316 = 94.87 µs。平台要 ≤ 10⁻³，符号就要 ≥ 94.87 µs（越长平台越低）。</li>
<li><b>换成比特速率</b>：每个符号 2 bit，R<sub>b</sub> = 2/T<sub>s</sub>。</li>
</ol>
<div class="calc">√10⁻³ = 0.0316<br>T<sub>s</sub> = 3 µs / 0.0316 = 94.87 µs<br>R<sub>b</sub> = 2 / 94.87 µs = 21.08 kbps（最大）<br>对比 BPSK：1 / 94.87 µs = 10.54 kbps</div>
<h4><span class="st">自检</span>和第 2 章判据对一下</h4>
<ul>
<li>σ<sub>Tm</sub>/T<sub>s</sub> = 0.0316 &lt; 0.1，满足平坦衰落判据（Practice 1 第 3 题），说得通。</li>
<li>有趣的联系：如果刚好在平坦衰落边界 σ/T<sub>s</sub> = 0.1，平台 ≈ 0.1² = 10⁻²；要 10⁻³ 就得比边界更保守。</li>
<li>QPSK 速率是 BPSK 的 2 倍：符号时长一样，每个符号多装 1 bit。</li>
</ul>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>把公式里的 T 当成比特时长直接用：得到 10.54 kbps，少了一半。</li>
<li>忘了开根号：σ/T 等于 √P<sub>floor</sub>，不是 P<sub>floor</sub>。</li>
<li>答案是上限：写成 "R<sub>b</sub> ≤ 21.08 kbps"，并说明速率再高平台就超过 10⁻³。</li>
<li>σ<sub>Tm</sub> 是 rms 时延扩展，不是最大时延。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
''' + TM['p3q3'] + r'''
<div class="ans">一句话：误码平台由"时延扩展 / 符号时长"决定，√10⁻³ 反推 T<sub>s</sub> ≥ 94.87 µs，QPSK 每符号 2 bit，最高 21.08 kbps。</div>''',
'en': r'''<h4><span class="st">Concept</span>What an irreducible error floor is</h4>
<p>Normally the error rate keeps falling as the SNR rises. But some errors are not caused by noise and do not go away even as SNR → ∞; the error rate levels off at a "floor", the irreducible error floor (lecture Ch 3 p.35). Two sources:</p>
<div class="tw"><table class="mini"><thead><tr><th>Source</th><th>Floor approximation</th><th>Symbols must be</th><th>Gives a rate</th></tr></thead><tbody>
<tr><td>Doppler spread (the channel changes within a symbol)</td><td>0.5(πf<sub>D</sub>T<sub>b</sub>)² (slides p.35–36, DPSK)</td><td>short</td><td>lower limit</td></tr>
<tr><td>delay spread (echoes leak into the next symbol, ISI)</td><td>(σ<sub>Tm</sub>/T<sub>b</sub>)² (given in this question, BPSK)</td><td>long</td><td>upper limit</td></tr>
</tbody></table></div>
<p>The delay-spread floor formula used here is not in the main slides; the question gives it. The lecturer said the error floor formulas are boxed but not in blue boxes, so they need not be memorised and will be given in the question.</p>
<p>The physical picture of ISI: part of a symbol's energy arrives late, falls into the time slot of the next symbol and overlaps with it. The receiver decides on "what arrived in this time slot", so the leaked previous symbol acts as data-dependent interference. Raising the signal power raises the leaked echo by the same factor, so the ratio does not change and more power cannot remove it; the only cures are longer symbols (a smaller echo fraction), or equalisation or OFDM to deal with the echoes.</p>
<p>What the formula means: how severe the ISI is depends on how long the echo σ<sub>Tm</sub> is compared with one <b>symbol</b>. For BPSK one symbol is one bit, so the formula is written with T<sub>b</sub>; for QPSK (M = 4, log₂4 = 2 bits per symbol) what matters is the symbol duration T<sub>s</sub>. Rate conversion: R<sub>b</sub> = log₂M / T<sub>s</sub>.</p>
<h4><span class="st">Step by step</span>From the floor target to the shortest symbol duration</h4>
<ol>
<li><b>List the data</b>: σ<sub>Tm</sub> = 3 µs, floor target P<sub>floor</sub> = 10⁻³, modulation QPSK.</li>
<li><b>Switch to the symbol duration</b>: for QPSK use \(P_{floor}\approx(\sigma_{T_m}/T_s)^2\). <b>Why</b>: ISI depends only on the echo length relative to the symbol, not on how many bits a symbol carries.</li>
<li><b>Take the square root</b>: \((3\,\mu s/T_s)^2=10^{-3}\) → \(3\,\mu s/T_s=\sqrt{10^{-3}}=0.0316\). Calculator hint: √10⁻³ = 10<sup>−1.5</sup>.</li>
<li><b>Solve for T<sub>s</sub></b>: T<sub>s</sub> = 3 / 0.0316 = 94.87 µs. For a floor ≤ 10⁻³ the symbol must be ≥ 94.87 µs (longer symbol, lower floor).</li>
<li><b>Convert to a bit rate</b>: 2 bits per symbol, R<sub>b</sub> = 2/T<sub>s</sub>.</li>
</ol>
<div class="calc">√10⁻³ = 0.0316<br>T<sub>s</sub> = 3 µs / 0.0316 = 94.87 µs<br>R<sub>b</sub> = 2 / 94.87 µs = 21.08 kbps (maximum)<br>For comparison, BPSK: 1 / 94.87 µs = 10.54 kbps</div>
<h4><span class="st">Check</span>Compare with the Ch 2 rule</h4>
<ul>
<li>σ<sub>Tm</sub>/T<sub>s</sub> = 0.0316 &lt; 0.1, so the flat-fading rule (Practice 1 Q3) is satisfied, which makes sense.</li>
<li>A nice link: exactly at the flat-fading boundary σ/T<sub>s</sub> = 0.1 the floor would be ≈ 0.1² = 10⁻²; a floor of 10⁻³ needs a more conservative design than the boundary.</li>
<li>The QPSK rate is twice the BPSK rate: same symbol duration, one more bit per symbol.</li>
</ul>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Using the T in the formula as a bit duration: this gives 10.54 kbps, half the answer.</li>
<li>Forgetting the square root: σ/T equals √P<sub>floor</sub>, not P<sub>floor</sub>.</li>
<li>The answer is an upper limit: write "R<sub>b</sub> ≤ 21.08 kbps" and say that a higher rate pushes the floor above 10⁻³.</li>
<li>σ<sub>Tm</sub> is the rms delay spread, not the maximum delay.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
''' + TM['p3q3'] + r'''
<div class="ans">In one line: the error floor is set by delay spread / symbol duration; √10⁻³ gives T<sub>s</sub> ≥ 94.87 µs, and with 2 bits per QPSK symbol the maximum rate is 21.08 kbps.</div>''',
}

# ================================================================ P4 Q1
XPL['p4q1'] = {
'title': '知识讲解 + 详细解析：宏分集为什么降低中断',
'title_en': 'Concept + walkthrough: why macro-diversity reduces outage',
'zh': r'''<h4><span class="st">知识讲解</span>两种衰落，两种分集</h4>
<p>无线信道的起伏分两个尺度（讲义第 2 章）：</p>
<ul>
<li><b>大尺度衰落 = 阴影（shadowing）</b>：楼房、山体挡住传播路径，信号在几十米到几百米的范围内一直偏低，变化慢。它是中断（outage，接收功率低于门限）的主要原因。</li>
<li><b>小尺度衰落 = 多径（multipath）</b>：多条路径的信号时而相加时而抵消，几个波长内就变化，比如瑞利衰落。</li>
</ul>
<p>分集（diversity）的基本想法（第 4 章 p.2–3）：把同样的信息经过几条<b>独立</b>的信道送到，一条深衰落时其他的大概率还好。对付哪种衰落，信道之间就要隔多远：</p>
<div class="tw"><table class="mini"><thead><tr><th></th><th>宏分集（macroscopic，p.4）</th><th>微分集（microscopic，p.5）</th></tr></thead><tbody>
<tr><td>对付</td><td>阴影（大尺度）</td><td>多径（小尺度）</td></tr>
<tr><td>做法</td><td>多个基站同时连一部手机，用信号最强的那个</td><td>同一处多根天线、不同频率、不同时间、极化</td></tr>
<tr><td>间隔</td><td>基站相距很远（不同发射位置）</td><td>几个波长就够</td></tr>
</tbody></table></div>
<p>为什么同一个基站多装几根天线解决不了阴影：手机被同一栋楼挡住时，几根天线的路径都穿过这栋楼，一起变差。讲义 p.4 原话的意思是：阴影造成的明显起伏只在大的距离上才发生，所以必须是不同位置的基站。</p>
<h4><span class="st">答题要点</span>每一点为什么要写</h4>
<ol>
<li><b>先说宏分集是什么</b>：手机的信号同时被几个不同位置的基站接收和处理，选最强的（或合并）。老师说解释题第一步就是描述这个东西是什么。</li>
<li><b>中断来自阴影</b>：说明你知道要对付的是哪种衰落。阴影慢而深，靠加功率（加余量）对付很不划算。</li>
<li><b>不同位置 → 阴影近似独立</b>：这是机制的核心。路径不同，挡住它们的障碍物不同，一条被挡不影响另一条。</li>
<li><b>全部同时中断才算中断 → 概率相乘</b>：独立时 \(P_{out}=\prod_iP_{out,i}\)。这是"为什么能降低"的定量答案。</li>
<li><b>条件</b>：链路相关时效果变差（p.21）。写上这一句说明你理解前提，但老师说两点（是什么 + 为什么）就够，多写的部分写错会扣分。</li>
</ol>
<div class="calc">单条链路中断 10%：两个独立基站 0.1² = 1%，三个 0.1³ = 0.1%<br>用 Practice 2 第 2 题的公式，取余量 Δ = σ：一个基站 Q(1) = 0.1587，两个独立 [Q(1)]² = 0.0252</div>
<h4><span class="st">知识讲解</span>相关为什么削弱分集（p.21）</h4>
<p>讲义写：P(两条同时深衰落) = P(r₁ 深衰落 | r₂ 深衰落) × P(r₂ 深衰落) ≥ P(r₁ 深衰落) × P(r₂ 深衰落)，链路不相关时取等号。意思是：相关时一条变差，另一条也倾向于变差，"同时中断"比相乘的结果大。例如手机进了地下室，所有基站的信号一起变弱。Practice 2 第 2(c) 题把这件事定量化了：相关系数 0.5 时，上面的 2.5% 变成 6.3%。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>说成"对付多径 / 瑞利衰落"：那是微分集。</li>
<li>只说"有多个基站所以更可靠"，没说<b>独立</b>和<b>全部同时</b>：机制没讲清，拿不到满分。</li>
<li>以为同一基站多天线也行：阴影对它们是一样的。</li>
<li>写成大段文字：老师建议写成几个要点，英文不好也没关系。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
''' + TM['p4q1'] + r'''
<div class="ans">一句话：中断主要来自阴影，相距很远的基站被同一障碍物挡住的可能性小，阴影近似独立，全部同时中断的概率是各自概率之积，所以大大降低。</div>''',
'en': r'''<h4><span class="st">Concept</span>Two kinds of fading, two kinds of diversity</h4>
<p>Wireless channel variations happen on two scales (lecture Ch 2):</p>
<ul>
<li><b>Large-scale fading = shadowing</b>: buildings or hills block the path, and the signal stays low over tens to hundreds of metres; it changes slowly. It is the main cause of outage (received power below the threshold).</li>
<li><b>Small-scale fading = multipath</b>: signals on several paths add up and cancel by turns, changing within a few wavelengths, e.g. Rayleigh fading.</li>
</ul>
<p>The basic idea of diversity (Ch 4 p.2–3): send the same information over several <b>independent</b> channels; when one is in a deep fade the others are probably fine. How far apart the channels must be depends on which fading you fight:</p>
<div class="tw"><table class="mini"><thead><tr><th></th><th>Macroscopic diversity (p.4)</th><th>Microscopic diversity (p.5)</th></tr></thead><tbody>
<tr><td>Fights</td><td>shadowing (large-scale)</td><td>multipath (small-scale)</td></tr>
<tr><td>How</td><td>several base stations linked to one mobile, the strongest is used</td><td>several antennas at one place, different frequencies, times, polarisations</td></tr>
<tr><td>Separation</td><td>base stations far apart (different transmitter locations)</td><td>a few wavelengths is enough</td></tr>
</tbody></table></div>
<p>Why extra antennas on the same base station do not fix shadowing: when the mobile is behind one building, the paths to all those antennas pass through that building and get worse together. Slide p.4 says, in effect, that the strong variations caused by shadowing happen only over large distances, so the base stations must be at different locations.</p>
<h4><span class="st">Answer points</span>Why each point is needed</h4>
<ol>
<li><b>First say what macro-diversity is</b>: the mobile's signal is received and processed by several base stations at different locations, and the strongest is used (or they are combined). The lecturer said the first step of an explanation question is to describe the thing.</li>
<li><b>Outage comes from shadowing</b>: shows you know which fading is being fought. Shadowing is slow and deep, so fighting it with more power (a larger margin) is expensive.</li>
<li><b>Different locations → nearly independent shadowing</b>: this is the core of the mechanism. Different paths are blocked by different obstacles, so one link being blocked does not affect another.</li>
<li><b>Outage only if all links fail at once → multiply</b>: with independence \(P_{out}=\prod_iP_{out,i}\). This is the quantitative answer to "why it reduces outage".</li>
<li><b>Condition</b>: the gain shrinks if the links are correlated (p.21). This sentence shows you understand the assumption, but the lecturer said two points (what + why) are enough, and anything extra that is wrong loses marks.</li>
</ol>
<div class="calc">Single-link outage 10%: two independent base stations 0.1² = 1%, three 0.1³ = 0.1%<br>With the formula of Practice 2 Q2 and margin Δ = σ: one base station Q(1) = 0.1587, two independent [Q(1)]² = 0.0252</div>
<h4><span class="st">Concept</span>Why correlation weakens diversity (p.21)</h4>
<p>The slide says: P(both in deep fade) = P(r₁ in deep fade | r₂ in deep fade) × P(r₂ in deep fade) ≥ P(r₁ in deep fade) × P(r₂ in deep fade), with equality when the links are uncorrelated. In words: with correlation, when one link gets worse the other tends to get worse too, so "both in outage" is more likely than the product. For example, when the mobile goes into a basement, the signals from all base stations drop together. Practice 2 Q2(c) makes this quantitative: with correlation coefficient 0.5 the 2.5% above becomes 6.3%.</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Saying it fights multipath / Rayleigh fading: that is microscopic diversity.</li>
<li>Only saying "more base stations, so more reliable" without <b>independent</b> and <b>all at the same time</b>: the mechanism is missing and full marks are not given.</li>
<li>Thinking several antennas on one base station would do: shadowing is the same for all of them.</li>
<li>Writing one long paragraph: the lecturer recommends a few bullet points; imperfect English is fine.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
''' + TM['p4q1'] + r'''
<div class="ans">In one line: outage is mainly caused by shadowing; base stations far apart are unlikely to be blocked by the same obstacle, so their shadowing is nearly independent and the probability that all are in outage at once is the product of the individual probabilities, which is much smaller.</div>''',
}

# ================================================================ P4 Q2
XPL['p4q2'] = {
'title': '知识讲解 + 详细解析：离散 SNR 的平均误码率、MRC、g 与 d',
'title_en': 'Concept + walkthrough: average error rate with discrete SNR, MRC, g and d',
'zh': r'''<h4><span class="st">知识讲解</span>衰落下要对误码率求平均</h4>
<p>AWGN 信道里 SNR 是常数；衰落信道里 SNR γ 是随机变量（老师课上反复强调），所以误码率 P<sub>s</sub>(γ) 也是随机的，要求平均：\(\bar P_s=E[P_s(\gamma)]=\sum_kP_s(\gamma_k)\,p_k\)（讲义第 4 章 p.23 的积分式，离散分布就换成求和）。老师说<b>不会考积分</b>，但离散分布的平均误码率会考。</p>
<p>关键：<b>E[f(γ)] ≠ f(E[γ])</b>。本题如果把平均 SNR 10 直接代进去，½e⁻¹⁰ = 2.27 × 10⁻⁵，而真正的平均是 6.15 × 10⁻⁵，差近 3 倍：误码主要来自 SNR 差的那些时刻，平均 SNR 把它们"抹平"了。</p>
<h4><span class="st">知识讲解</span>MRC、阵列增益 g、分集增益 d</h4>
<ul>
<li><b>MRC</b>（最大比合并，p.15–16）：每条支路乘以信道增益的共轭再相加，输出 SNR = 各支路 SNR 之和：γ<sub>Σ</sub> = γ₁ + γ₂。</li>
<li><b>阵列增益</b>（p.27）\(g=\bar\gamma_\Sigma/\bar\gamma\)：合并后平均 SNR 是输入的几倍。</li>
<li><b>分集增益</b>（p.27）\(d\approx-\log_{10}\bar P_e/\log_{10}\bar\gamma\)：来自高 SNR 下 \(\bar P_e\approx\bar\gamma^{-d}\)，误码率随 SNR 下降的"斜率"。γ̄ 是合并器<b>输入</b>的平均 SNR。</li>
</ul>
<p>老师说 g 和 d 的公式"简单、要记住"（蓝框，考试不给）。p.21：支路相关时，同时深衰落的概率更大，分集变差。</p>
<h4><span class="st">详细解析</span>(a) 单支路</h4>
<ol>
<li><b>γ 就是 α</b>：γ = αP<sub>T</sub>/σ<sub>n</sub>² 且 P<sub>T</sub> = σ<sub>n</sub>² = 1 W，所以 γ = 8（1/3）或 11（2/3）。老师提醒先问一句：这些数是线性值还是 dB？这里是线性值，不用换算。</li>
<li><b>平均 SNR</b>：Σ 取值 × 概率。</li>
<li><b>平均误码率</b>：Σ P<sub>s</sub>(取值) × 概率，不能代平均 SNR。</li>
</ol>
<div class="calc">γ̄ = 8 × ⅓ + 11 × ⅔ = 10<br>P̄<sub>s</sub> = ⅓ × ½e⁻⁸ + ⅔ × ½e⁻¹¹ = 5.59 × 10⁻⁵ + 0.56 × 10⁻⁵ = 6.15 × 10⁻⁵</div>
<h4><span class="st">详细解析</span>(b) 两条独立支路 MRC</h4>
<ol>
<li><b>列组合表</b>：两路独立，概率相乘；19 有 (8, 11)、(11, 8) 两种排列。</li>
<li><b>输出 SNR</b> 相加，再按概率加权。</li>
</ol>
<div class="tw"><table class="mini"><thead><tr><th>(γ₁, γ₂)</th><th>γ<sub>Σ</sub></th><th>概率</th><th>½e<sup>−γΣ</sup> × 概率</th></tr></thead><tbody>
<tr><td>(8, 8)</td><td>16</td><td>1/9</td><td>6.25 × 10⁻⁹</td></tr>
<tr><td>(8, 11)、(11, 8)</td><td>19</td><td>2 × ⅓ × ⅔ = 4/9</td><td>1.25 × 10⁻⁹</td></tr>
<tr><td>(11, 11)</td><td>22</td><td>4/9</td><td>0.06 × 10⁻⁹</td></tr>
</tbody></table></div>
<div class="calc">γ̄<sub>Σ</sub> = (16 × 1 + 19 × 4 + 22 × 4)/9 = 180/9 = 20<br>P̄<sub>s</sub> = 6.25 + 1.25 + 0.06 = 7.56 × 10⁻⁹<br>g = 20/10 = 2（= 3.01 dB）<br>d = −log₁₀(7.56 × 10⁻⁹) / log₁₀10 = 8.12 / 1 = 8.1</div>
<p>注意：概率只有 1/9 的"两路都差"(8, 8) 贡献了八成以上的误码。捷径：两路独立，\(E[e^{-(\gamma_1+\gamma_2)}]=(E[e^{-\gamma}])^2\)，而 (a) 已得 E[e<sup>−γ</sup>] = 2 × 6.15 × 10⁻⁵ = 1.23 × 10⁻⁴，所以 P̄<sub>s</sub> = ½ × (1.23 × 10⁻⁴)² = 7.56 × 10⁻⁹。</p>
<h4><span class="st">详细解析</span>(c) 共享阴影 β：先固定 β（老师的方法）</h4>
<ol>
<li><b>平均 SNR 不变</b>：E[r] = 0.6 × ⅓ + 1.2 × ⅔ = 1，E[β] = 7 × ⅓ + 10 × ⅔ = 9，E[γ<sub>i</sub>] = 10，γ̄<sub>Σ</sub> = 20，g = 2。</li>
<li><b>输出 SNR</b>：γ<sub>Σ</sub> = r₁ + r₂ + 2β，β 出现两次，所以指数里是 2β。</li>
<li><b>先把 β 当常数</b>（和 Practice 2 第 2 题同一招）：给定 β，r₁、r₂ 独立，\(P_s\mid\beta=\tfrac12(E[e^{-r}])^2e^{-2\beta}\)。</li>
<li><b>再对 β 加权平均</b>。</li>
</ol>
<div class="calc">E[e<sup>−r</sup>] = ⅓e<sup>−0.6</sup> + ⅔e<sup>−1.2</sup> = 0.1829 + 0.2008 = 0.3837<br>β = 7：½ × 0.3837² × e⁻¹⁴ = 6.12 × 10⁻⁸<br>β = 10：½ × 0.3837² × e⁻²⁰ = 1.52 × 10⁻¹⁰<br>P̄<sub>s</sub> = ⅓ × 6.12 × 10⁻⁸ + ⅔ × 1.52 × 10⁻¹⁰ = 2.05 × 10⁻⁸<br>（等价：E[e<sup>−2β</sup>] = ⅓e⁻¹⁴ + ⅔e⁻²⁰ = 2.786 × 10⁻⁷，½ × 0.3837² × 2.786 × 10⁻⁷ = 2.05 × 10⁻⁸）<br>d = −log₁₀(2.05 × 10⁻⁸) = 8 − 0.31 = 7.7</div>
<p>结论：(b)(c) 平均 SNR 都是 20、g 都是 2，但 (c) 误码率是 (b) 的 2.7 倍，d 从 8.1 降到 7.7。误码几乎全部发生在共享阴影 β = 7 的时候，两路一起变差，这就是 p.21 说的"相关削弱分集"。</p>
<h4><span class="st">课外补充</span>为什么 d = 8.1 比支路数 2 还大</h4>
<p>讲义 p.28 说 d ≤ M。这里 d = 8.1 &gt; 2，原因是 p.27 的 d 是高 SNR 下的"斜率"定义，针对的是瑞利这类会出现很深衰落的信道（P̄<sub>e</sub> ∝ γ̄<sup>−d</sup>）。本题的离散分布 γ 最低也有 8，没有深衰落，误码率随 SNR 指数下降，在 γ̄ = 10 这一点代公式得到的只是一个数，不是真正的分集阶数（连单支路 (a) 代进去都得 4.2）。考试照公式算即可（官方答案也是这样），用它来比较 (b)(c)。</p>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>把平均 SNR 代进误码率公式：E[½e<sup>−γ</sup>] ≠ ½e<sup>−E[γ]</sup>。</li>
<li>19 只算一种排列：概率是 4/9 不是 2/9。</li>
<li>d 的分母用输出的 20：应该用输入的 10，log₁₀10 = 1。</li>
<li>(c) 指数里写 β 而不是 2β。</li>
<li>e⁻¹⁶ 这类极小数要保留有效数字，别四舍五入成 0。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
''' + TM['p4q2'] + r'''
<div class="ans">一句话：误码率要按 SNR 的分布加权平均；MRC 输出 SNR = 两路相加，g = 输出 ÷ 输入平均 SNR，d = −log P̄ / log γ̄；共享阴影 β 不改变 g，但让误码率变大、d 变小。</div>''',
'en': r'''<h4><span class="st">Concept</span>In fading, the error rate must be averaged</h4>
<p>In an AWGN channel the SNR is a constant; in a fading channel the SNR γ is a random variable (the lecturer stressed this repeatedly), so the error rate P<sub>s</sub>(γ) is random too and must be averaged: \(\bar P_s=E[P_s(\gamma)]=\sum_kP_s(\gamma_k)\,p_k\) (the integral on lecture Ch 4 p.23 becomes a sum for a discrete distribution). The lecturer said <b>integrals will not be examined</b>, but average error rates for discrete distributions can be.</p>
<p>Key point: <b>E[f(γ)] ≠ f(E[γ])</b>. Substituting the mean SNR 10 directly gives ½e⁻¹⁰ = 2.27 × 10⁻⁵, while the true average is 6.15 × 10⁻⁵, almost 3 times larger: the errors come mainly from the moments of low SNR, and the mean SNR "smooths them away".</p>
<h4><span class="st">Concept</span>MRC, array gain g, diversity gain d</h4>
<ul>
<li><b>MRC</b> (maximal ratio combining, p.15–16): each branch is multiplied by the conjugate of its channel gain and the branches are added; the output SNR is the sum of the branch SNRs: γ<sub>Σ</sub> = γ₁ + γ₂.</li>
<li><b>Array gain</b> (p.27) \(g=\bar\gamma_\Sigma/\bar\gamma\): how many times larger the average SNR is after combining.</li>
<li><b>Diversity gain</b> (p.27) \(d\approx-\log_{10}\bar P_e/\log_{10}\bar\gamma\): from \(\bar P_e\approx\bar\gamma^{-d}\) at high SNR, the "slope" at which the error rate falls with SNR. γ̄ is the average SNR at the combiner <b>input</b>.</li>
</ul>
<p>The lecturer called the g and d formulas "simple, remember them" (blue box, not given in the exam). p.21: with correlated branches, simultaneous deep fades are more likely and diversity is weaker.</p>
<h4><span class="st">Step by step</span>(a) Single branch</h4>
<ol>
<li><b>γ equals α</b>: γ = αP<sub>T</sub>/σ<sub>n</sub>² and P<sub>T</sub> = σ<sub>n</sub>² = 1 W, so γ = 8 (1/3) or 11 (2/3). The lecturer's reminder: first ask whether the numbers are linear or dB. Here they are linear, so no conversion is needed.</li>
<li><b>Average SNR</b>: Σ value × probability.</li>
<li><b>Average error rate</b>: Σ P<sub>s</sub>(value) × probability; do not substitute the average SNR.</li>
</ol>
<div class="calc">γ̄ = 8 × ⅓ + 11 × ⅔ = 10<br>P̄<sub>s</sub> = ⅓ × ½e⁻⁸ + ⅔ × ½e⁻¹¹ = 5.59 × 10⁻⁵ + 0.56 × 10⁻⁵ = 6.15 × 10⁻⁵</div>
<h4><span class="st">Step by step</span>(b) MRC with two independent branches</h4>
<ol>
<li><b>Tabulate the combinations</b>: independent branches, so probabilities multiply; 19 has two orderings, (8, 11) and (11, 8).</li>
<li><b>Add the output SNRs</b>, then weight by the probabilities.</li>
</ol>
<div class="tw"><table class="mini"><thead><tr><th>(γ₁, γ₂)</th><th>γ<sub>Σ</sub></th><th>Probability</th><th>½e<sup>−γΣ</sup> × probability</th></tr></thead><tbody>
<tr><td>(8, 8)</td><td>16</td><td>1/9</td><td>6.25 × 10⁻⁹</td></tr>
<tr><td>(8, 11), (11, 8)</td><td>19</td><td>2 × ⅓ × ⅔ = 4/9</td><td>1.25 × 10⁻⁹</td></tr>
<tr><td>(11, 11)</td><td>22</td><td>4/9</td><td>0.06 × 10⁻⁹</td></tr>
</tbody></table></div>
<div class="calc">γ̄<sub>Σ</sub> = (16 × 1 + 19 × 4 + 22 × 4)/9 = 180/9 = 20<br>P̄<sub>s</sub> = 6.25 + 1.25 + 0.06 = 7.56 × 10⁻⁹<br>g = 20/10 = 2 (= 3.01 dB)<br>d = −log₁₀(7.56 × 10⁻⁹) / log₁₀10 = 8.12 / 1 = 8.1</div>
<p>Note: the "both branches bad" case (8, 8), with probability only 1/9, contributes more than 80% of the errors. Shortcut: with independent branches \(E[e^{-(\gamma_1+\gamma_2)}]=(E[e^{-\gamma}])^2\), and (a) already gives E[e<sup>−γ</sup>] = 2 × 6.15 × 10⁻⁵ = 1.23 × 10⁻⁴, so P̄<sub>s</sub> = ½ × (1.23 × 10⁻⁴)² = 7.56 × 10⁻⁹.</p>
<h4><span class="st">Step by step</span>(c) Shared shadowing β: fix β first (the lecturer's method)</h4>
<ol>
<li><b>Average SNR unchanged</b>: E[r] = 0.6 × ⅓ + 1.2 × ⅔ = 1, E[β] = 7 × ⅓ + 10 × ⅔ = 9, E[γ<sub>i</sub>] = 10, γ̄<sub>Σ</sub> = 20, g = 2.</li>
<li><b>Output SNR</b>: γ<sub>Σ</sub> = r₁ + r₂ + 2β; β appears twice, so the exponent contains 2β.</li>
<li><b>Treat β as a constant first</b> (the same trick as Practice 2 Q2): given β, r₁ and r₂ are independent, \(P_s\mid\beta=\tfrac12(E[e^{-r}])^2e^{-2\beta}\).</li>
<li><b>Then average over β</b>.</li>
</ol>
<div class="calc">E[e<sup>−r</sup>] = ⅓e<sup>−0.6</sup> + ⅔e<sup>−1.2</sup> = 0.1829 + 0.2008 = 0.3837<br>β = 7: ½ × 0.3837² × e⁻¹⁴ = 6.12 × 10⁻⁸<br>β = 10: ½ × 0.3837² × e⁻²⁰ = 1.52 × 10⁻¹⁰<br>P̄<sub>s</sub> = ⅓ × 6.12 × 10⁻⁸ + ⅔ × 1.52 × 10⁻¹⁰ = 2.05 × 10⁻⁸<br>(equivalently: E[e<sup>−2β</sup>] = ⅓e⁻¹⁴ + ⅔e⁻²⁰ = 2.786 × 10⁻⁷, ½ × 0.3837² × 2.786 × 10⁻⁷ = 2.05 × 10⁻⁸)<br>d = −log₁₀(2.05 × 10⁻⁸) = 8 − 0.31 = 7.7</div>
<p>Conclusion: (b) and (c) both have average SNR 20 and g = 2, but the error rate in (c) is 2.7 times that of (b) and d drops from 8.1 to 7.7. Almost all errors occur when the shared shadowing is β = 7 and both branches are bad together; this is what p.21 means by "correlation weakens diversity".</p>
<h4><span class="st">Beyond the slides</span>Why d = 8.1 is larger than the number of branches</h4>
<p>Slide p.28 says d ≤ M. Here d = 8.1 &gt; 2 because the d of p.27 is a high-SNR "slope" definition meant for channels such as Rayleigh that have very deep fades (P̄<sub>e</sub> ∝ γ̄<sup>−d</sup>). In this discrete distribution γ never drops below 8, so there are no deep fades and the error rate falls exponentially with SNR; evaluating the formula at the single point γ̄ = 10 just gives a number, not a true diversity order (even the single branch of (a) gives 4.2). In the exam, apply the formula as the official answer does and use it to compare (b) and (c).</p>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Substituting the average SNR into the error formula: E[½e<sup>−γ</sup>] ≠ ½e<sup>−E[γ]</sup>.</li>
<li>Counting only one ordering for 19: the probability is 4/9, not 2/9.</li>
<li>Using the output 20 in the denominator of d: use the input 10, log₁₀10 = 1.</li>
<li>Writing β instead of 2β in the exponent in (c).</li>
<li>Keep significant figures for tiny numbers such as e⁻¹⁶; do not round them to 0.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
''' + TM['p4q2'] + r'''
<div class="ans">In one line: average the error rate over the SNR distribution; the MRC output SNR is the sum of the two branches, g = output ÷ input average SNR, d = −log P̄ / log γ̄; the shared shadowing β leaves g unchanged but raises the error rate and lowers d.</div>''',
}

# ================================================================ P4 Q3
XPL['p4q3'] = {
'title': '知识讲解 + 详细解析：高斯衰落因子与等权合并',
'title_en': 'Concept + walkthrough: Gaussian fading factor and equal-weight combining',
'zh': r'''<h4><span class="st">知识讲解</span>判决量是高斯时，误码率 = Q(均值 / 标准差)</h4>
<p>本题的接收信号 \(y_k=\alpha_kb\sqrt E+w_k\) 里有两种"噪声"（老师课上的说法）：α<sub>k</sub> 乘在信号上，是<b>乘性</b>噪声（衰落）；w<sub>k</sub> 加在信号上，是<b>加性</b>噪声。特别之处是 α<sub>k</sub> 被建模成高斯（不是瑞利），这样整个判决量都是高斯，误码率可以直接写成 Q 函数。</p>
<p>要用到的三条概率工具（第 1b 章）：</p>
<div class="tw"><table class="mini"><thead><tr><th>工具</th><th>式子</th><th>本题用在哪</th></tr></thead><tbody>
<tr><td>常数乘随机变量</td><td>E[cX] = cE[X]，Var(cX) = c²Var(X)</td><td>α√E 的方差是 σ₁²E</td></tr>
<tr><td>独立变量相加</td><td>均值相加，方差相加</td><td>α√E + w；M 路相加</td></tr>
<tr><td>独立高斯之和</td><td>仍是高斯</td><td>z 是高斯，才能写 Q</td></tr>
</tbody></table></div>
<p>再加第 2 章 p.14 的"移项"技巧：z = m + n，n ~ N(0, s²)，则 P(z ≤ 0) = P(n ≤ −m) = Q(m/s)。</p>
<p>等权合并（equal weight combining）：所有 y<sub>k</sub> 直接相加。老师特别提醒它<b>不是</b>讲义 p.19 的等增益合并（EGC）：EGC 要先按各路相位旋转，这里各路都是实数，直接加。</p>
<h4><span class="st">详细解析</span>(a) M = 1：老师总结的三步</h4>
<ol>
<li><b>只算 b = +1</b>：b 等概取 ±1，两种情况对称，P<sub>b</sub> = ½P(错 | +1) + ½P(错 | −1) = P(错 | +1)。</li>
<li><b>求总均值和总方差</b>（老师说这一步最关键）：z = α√E + w。均值 E[α]√E + E[w] = α₀√E；方差 Var(α)E + Var(w) = σ₁²E + σ₂²（α 与 w 独立）。所以 z = α₀√E + n，n ~ N(0, σ₁²E + σ₂²)。</li>
<li><b>写成 Q</b>：b = +1 时出错 = z ≤ 0 ⇔ n ≤ −α₀√E，由对称性 P = Q(均值 / 标准差)。</li>
</ol>
<div class="calc">均值 α₀√E，方差 σ₁²E + σ₂²<br>P<sub>b</sub> = Q( α₀√E / √(σ₁²E + σ₂²) )</div>
<h4><span class="st">详细解析</span>(b) M 路等权相加</h4>
<ol>
<li><b>写出判决量</b>：\(z=\sum_{k=1}^My_k=b\sqrt E\sum_k\alpha_k+\sum_kw_k\)。</li>
<li><b>均值</b>：M 个 α₀√E 相加 = Mα₀√E。</li>
<li><b>方差</b>：2M 个独立项，方差相加 = M(σ₁²E + σ₂²)。题目没明说各 α<sub>k</sub> 相互独立，标准解默认独立（不同天线的衰落独立）。</li>
<li><b>Q 函数</b>：均值 / 标准差 = Mα₀√E / √(M(σ₁²E + σ₂²))，约掉 √M。</li>
</ol>
<div class="calc">P<sub>b</sub> = Q( √M · α₀√E / √(σ₁²E + σ₂²) )</div>
<p><b>为什么合并有好处</b>：均值按 M 增长，标准差只按 √M 增长，所以 Q 的参数放大 √M 倍。信号是"同向相加"（每路都是 α₀√E），噪声是"随机相加"（有正有负，部分抵消）。</p>
<h4><span class="st">课外补充</span>数值感受与两个极端</h4>
<div class="calc">举例 α₀ = 1，E = 1，σ₁² = σ₂² = 0.1，参数 = √M × 1/√0.2：<br>M = 1：Q(2.24) = 0.0127<br>M = 2：Q(3.16) = 7.8 × 10⁻⁴（蒙特卡洛模拟 8.0 × 10⁻⁴，对得上）<br>M = 4：Q(4.47) = 3.9 × 10⁻⁶</div>
<ul>
<li><b>没有噪声（σ₂ = 0）</b>：误码率 Q(α₀/σ₁) 仍不为 0，因为衰落因子本身可能变成负数，把符号翻过来，这是衰落造成的"平台"；合并后变成 Q(√M α₀/σ₁)，平台降低。</li>
<li><b>各路 α<sub>k</sub> 完全相同（完全相关）</b>：方差变成 M²σ₁²E + Mσ₂²，参数随 M 增大最多趋向 α₀/σ₁。上面的例子 M = 4 只有 Q(2.83) = 2.3 × 10⁻³，比独立时的 3.9 × 10⁻⁶ 差得多，又是"相关削弱分集"（p.21）。</li>
</ul>
<h4><span class="st">易错</span>常见丢分点</h4>
<ul>
<li>方差写成 σ₁² + σ₂²，漏乘 E：α 乘的是 √E，方差要乘 (√E)² = E。</li>
<li>标准差写成 σ₁√E + σ₂：方差能相加，标准差不能。</li>
<li>把等权合并当成 EGC 或 MRC：这里就是直接相加。</li>
<li>(b) 只写到 Q(Mα₀√E / √(M(…)))，没约成 √M：不算错，但约完才看得出合并的好处。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
''' + TM['p4q3'] + r'''
<div class="ans">一句话：设 b = +1，求判决量的总均值和总方差，误码率 = Q(均值 / 标准差)；M 路等权相加时均值 × M、标准差 × √M，Q 的参数放大 √M 倍。</div>''',
'en': r'''<h4><span class="st">Concept</span>If the decision variable is Gaussian, error rate = Q(mean / standard deviation)</h4>
<p>The received signal \(y_k=\alpha_kb\sqrt E+w_k\) contains two kinds of "noise" (the lecturer's words): α<sub>k</sub> multiplies the signal, a <b>multiplicative</b> noise (fading); w<sub>k</sub> is added to it, an <b>additive</b> noise. What is special is that α<sub>k</sub> is modelled as Gaussian (not Rayleigh), so the whole decision variable is Gaussian and the error rate can be written directly as a Q function.</p>
<p>Three probability tools are needed (Ch 1b):</p>
<div class="tw"><table class="mini"><thead><tr><th>Tool</th><th>Formula</th><th>Used for</th></tr></thead><tbody>
<tr><td>constant times a random variable</td><td>E[cX] = cE[X], Var(cX) = c²Var(X)</td><td>the variance of α√E is σ₁²E</td></tr>
<tr><td>sum of independent variables</td><td>means add, variances add</td><td>α√E + w; the sum over M branches</td></tr>
<tr><td>sum of independent Gaussians</td><td>still Gaussian</td><td>z is Gaussian, so Q can be used</td></tr>
</tbody></table></div>
<p>Plus the "rearrange" trick of Ch 2 p.14: if z = m + n with n ~ N(0, s²), then P(z ≤ 0) = P(n ≤ −m) = Q(m/s).</p>
<p>Equal-weight combining: all y<sub>k</sub> are simply added. The lecturer specifically warned that this is <b>not</b> the equal gain combining (EGC) of slide p.19: EGC first rotates each branch by its phase, while here all branches are real and are just added.</p>
<h4><span class="st">Step by step</span>(a) M = 1: the lecturer's three steps</h4>
<ol>
<li><b>Only b = +1 is needed</b>: b = ±1 are equally likely and the two cases are symmetric, P<sub>b</sub> = ½P(error | +1) + ½P(error | −1) = P(error | +1).</li>
<li><b>Find the total mean and total variance</b> (the lecturer said this is the key step): z = α√E + w. Mean E[α]√E + E[w] = α₀√E; variance Var(α)E + Var(w) = σ₁²E + σ₂² (α and w independent). So z = α₀√E + n with n ~ N(0, σ₁²E + σ₂²).</li>
<li><b>Write it as Q</b>: for b = +1 an error is z ≤ 0 ⇔ n ≤ −α₀√E, and by symmetry P = Q(mean / standard deviation).</li>
</ol>
<div class="calc">mean α₀√E, variance σ₁²E + σ₂²<br>P<sub>b</sub> = Q( α₀√E / √(σ₁²E + σ₂²) )</div>
<h4><span class="st">Step by step</span>(b) Equal-weight sum of M branches</h4>
<ol>
<li><b>Write the decision variable</b>: \(z=\sum_{k=1}^My_k=b\sqrt E\sum_k\alpha_k+\sum_kw_k\).</li>
<li><b>Mean</b>: M copies of α₀√E add up to Mα₀√E.</li>
<li><b>Variance</b>: 2M independent terms, variances add to M(σ₁²E + σ₂²). The question does not state explicitly that the α<sub>k</sub> are mutually independent; the standard solution assumes so (fading on different antennas is independent).</li>
<li><b>Q function</b>: mean / standard deviation = Mα₀√E / √(M(σ₁²E + σ₂²)); cancel √M.</li>
</ol>
<div class="calc">P<sub>b</sub> = Q( √M · α₀√E / √(σ₁²E + σ₂²) )</div>
<p><b>Why combining helps</b>: the mean grows like M but the standard deviation only like √M, so the argument of Q grows by √M. The signal adds "coherently" (every branch contributes α₀√E), while the noise adds "randomly" (positive and negative parts partly cancel).</p>
<h4><span class="st">Beyond the slides</span>Numbers and two extremes</h4>
<div class="calc">Example α₀ = 1, E = 1, σ₁² = σ₂² = 0.1, argument = √M × 1/√0.2:<br>M = 1: Q(2.24) = 0.0127<br>M = 2: Q(3.16) = 7.8 × 10⁻⁴ (Monte Carlo simulation gives 8.0 × 10⁻⁴, consistent)<br>M = 4: Q(4.47) = 3.9 × 10⁻⁶</div>
<ul>
<li><b>No noise (σ₂ = 0)</b>: the error rate Q(α₀/σ₁) is still not 0, because the fading factor itself can become negative and flip the sign; this is a fading-induced "floor". After combining it becomes Q(√M α₀/σ₁), a lower floor.</li>
<li><b>All α<sub>k</sub> identical (fully correlated)</b>: the variance becomes M²σ₁²E + Mσ₂², and as M grows the argument at most approaches α₀/σ₁. In the example above, M = 4 gives only Q(2.83) = 2.3 × 10⁻³, far worse than 3.9 × 10⁻⁶ in the independent case: again, "correlation weakens diversity" (p.21).</li>
</ul>
<h4><span class="st">Pitfalls</span>Where marks are usually lost</h4>
<ul>
<li>Writing the variance as σ₁² + σ₂² without the factor E: α is multiplied by √E, so its variance is multiplied by (√E)² = E.</li>
<li>Writing the standard deviation as σ₁√E + σ₂: variances add, standard deviations do not.</li>
<li>Treating equal-weight combining as EGC or MRC: here the branches are simply added.</li>
<li>Stopping at Q(Mα₀√E / √(M(…))) in (b) without simplifying to √M: not wrong, but only the simplified form shows the benefit of combining.</li>
</ul>
<h4><span class="st">Exam</span>How to write it in English</h4>
''' + TM['p4q3'] + r'''
<div class="ans">In one line: take b = +1, find the total mean and total variance of the decision variable, and the error rate is Q(mean / standard deviation); summing M branches multiplies the mean by M and the standard deviation by √M, so the argument of Q grows by √M.</div>''',
}

NOTES = '''p1q1: official answer (K = −31.4 dB, γ = 3.86, Pout = 6.19e-4) is not reproducible from the data (LS gives −30.8 dB, 3.94, MSE 11.87, Pout 1.85e-3; official K, γ give MSE 13.1; lecturer's MSE 9.656 gives 10/√9.656 = 3.22, Q ≈ 6.45e-4, 6.19e-4 is Q(3.23)). Box keeps the page's existing treatment.
p1q1: existing solution writes "Q(2.90) = 1.85e-3"; 1.85e-3 is Q(2.902) (unrounded σ). The table value at exactly 2.90 is 1.87e-3. Box says so (rounding only); not an error.
p4q2: d = 8.1 (b) and 7.7 (c) exceed the number of branches M = 2, although slide Ch 4 p.28 says d ≤ M. Not an error in the solution (official answer agrees); the p.27 single-point formula is not a true diversity order for this toy discrete distribution without deep fades. Explained in the box as 课外补充.
p4q3: the question does not state that the α_k are mutually independent; the standard solution (and the box) assumes it.'''
