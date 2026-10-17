#!/usr/bin/python3
"""Add the missing step-by-step derivations to Part 2 chapters 3–7 (learn_03..07.html).

Same style as derive_ch2.py. Each block sits between <!-- DRV:name --> and <!-- /DRV:name --> and is
inserted *before* its anchor. An anchor is either ('worked', title) – the line that opens the worked
example whose summary contains `title` – or ('text', literal).
Run order after editing fragments: enrich_p2.py → derive_ch2.py → derive_p2.py → kp_p2.py → build_learn.py.
"""
import pathlib, re

B = pathlib.Path(__file__).parent

def S(n, html):
    return f'<div class="wstep"><div class="wn">{n}</div><div class="wtext">{html}</div></div>'

def W(title, steps, ans, tail=''):
    body = ''.join(S(i + 1, s) for i, s in enumerate(steps))
    return (f'<div class="worked">\n        <summary><span class="wtag">推导</span>{title}</summary>\n'
            f'        <div class="wbody">\n          {body}\n          <div class="wans">{ans}</div>{tail}\n        </div>\n      </div>\n      ')

def X(label, html):
    return f'<div class="extra">\n        <div class="lbl">课外补充 · {label}</div>\n        {html}\n      </div>\n      '

BLOCKS = []   # (file, name, anchor, html)

# ================================================================ CH 3
BLOCKS.append(('learn_03.html', 'noise', ('text', '      <div class="formula-card">\n        <div class="flbl">SNR 的几种写法（p.16–17）</div>'), W(
    '为什么每个坐标上的噪声都是 \\(\\mathcal N(0,N_0/2)\\)，而且互相独立（p.12、p.15）', [
    r'第 j 个判决变量是收到的信号和第 j 个基函数做内积（p.14）：\(y_j=\int_0^Tx(t)\psi_j(t)dt=\int_0^Ts_i(t)\psi_j(t)dt+\int_0^Tw(t)\psi_j(t)dt=s_{ij}+w_j\)。前一项正是 p.4 定义的坐标 \(s_{ij}\)，后一项 \(w_j=\int_0^Tw(t)\psi_j(t)dt\) 就是这个坐标上的噪声。',
    r'<b>均值</b>：期望和积分可以交换顺序，\(E[w_j]=\int_0^TE[w(t)]\psi_j(t)dt=0\)（p.12：\(E[w(t)]=0\)）。',
    r'<b>协方差</b>：两个积分相乘写成二重积分，再代入白噪声的自相关 \(E[w(t)w(s)]=\frac{N_0}{2}\delta(t-s)\)（p.12）：<div class="calc">E[w_j w_k] = ∫∫ E[w(t)w(s)] ψ_j(t) ψ_k(s) dt ds = (N₀/2) ∫ ψ_j(t) ψ_k(t) dt</div>δ 函数的"筛选"作用：对 s 积分时只留下 s = t 那一点。最后的积分由基函数正交归一（p.4）得到：j = k 时为 1，j ≠ k 时为 0。所以 \(E[w_j^2]=N_0/2\)，\(E[w_jw_k]=0\)。',
    r'<b>高斯、独立</b>：积分是"加权求和"的极限，高斯过程经过线性运算仍是高斯；联合高斯的变量不相关就等于独立（第 2 章 I/Q 推导用过同一个结论）。',
    ], 'w ~ N(0, (N₀/2)I)：每个坐标的噪声方差都是 N₀/2，和基函数怎么选无关；这就是 p.15 的向量信道 y = s<sub>i</sub> + w',
    '\n          <p style="margin-top:12px">"白"的作用在第 3 步：自相关是 δ 函数，不同时刻的噪声不相关，投影到互相垂直的基函数上以后，各坐标的噪声也就不相关。</p>')))

BLOCKS.append(('learn_03.html', 'mlmd', ('text', '      <div class="formula-card">\n        <div class="flbl">误符号率的上界与 BPSK（p.20–21）</div>'), W(
    'MAP → ML → 最小距离，一步一步（p.18–19）', [
    r'<b>贝叶斯</b>（第 1 章）：\(p(\mathbf s_i\mid\mathbf y)=\dfrac{p(\mathbf y\mid\mathbf s_i)P(\mathbf s_i)}{p(\mathbf y)}\)。分母 \(p(\mathbf y)\) 对所有候选符号都一样，比大小时可以不管：MAP = \(\arg\max_i p(\mathbf y\mid\mathbf s_i)P(\mathbf s_i)\)。',
    r'<b>等概</b>：\(P(\mathbf s_i)=1/M\) 也和 i 无关，再去掉，只剩似然：MAP = ML = \(\arg\max_i p(\mathbf y\mid\mathbf s_i)\)。',
    r'<b>写出似然</b>：D 个坐标独立，每个 \(y_j\sim\mathcal N(s_{ij},N_0/2)\)。把方差 \(\sigma^2=N_0/2\) 代入高斯 PDF，\(2\sigma^2=N_0\)：每个坐标 \(\frac{1}{\sqrt{\pi N_0}}e^{-(y_j-s_{ij})^2/N_0}\)。独立 → 相乘，指数相加：<div class="calc">p(y | s<sub>i</sub>) = (πN₀)<sup>−D/2</sup> exp( −Σ<sub>j</sub>(y<sub>j</sub> − s<sub>ij</sub>)² / N₀ ) = (πN₀)<sup>−D/2</sup> exp( −‖y − s<sub>i</sub>‖² / N₀ )</div>这就是 p.19 的式子。',
    r'前面的系数和 i 无关，exp 是增函数，指数前面是负号：<mark class="hl">似然最大 ⇔ \(\|\mathbf y-\mathbf s_i\|^2\) 最小</mark>，即选离 y 最近的星座点。',
    r'<b>相关器形式</b>（p.19 Note）：展开 \(\|\mathbf y-\mathbf s_i\|^2=\|\mathbf y\|^2-2\langle\mathbf y,\mathbf s_i\rangle+\|\mathbf s_i\|^2\)，第一项和 i 无关，所以等价于 \(\arg\max_i\big(2\langle\mathbf y,\mathbf s_i\rangle-\|\mathbf s_i\|^2\big)\)。各点能量相同（如 PSK）时连 \(\|\mathbf s_i\|^2\) 也可以去掉，只比内积。',
    ], '等概 + 高斯白噪声：MAP = ML = 最小距离 = 最大相关（能量相同时）')))

BLOCKS.append(('learn_03.html', 'union', ('worked', '噪声方差不同时的 ML 判决'), W(
    '两点之间的误码率 Q(d/√(2N₀)) 和 (M − 1) 上界（p.20–21）', [
    r'先只看两个点 \(\mathbf s_i\)、\(\mathbf s_k\)，距离 \(d_{ik}\)。发 \(\mathbf s_i\) 却判成 \(\mathbf s_k\)，当且仅当 y 跑到两点连线的中垂线另一边，即噪声沿 \(\mathbf s_i\to\mathbf s_k\) 方向的分量超过 \(d_{ik}/2\)。',
    r'噪声在任意单位方向 \(\mathbf u\) 上的投影 \(n=\langle\mathbf w,\mathbf u\rangle=\sum_ju_jw_j\)，方差 \(\sum_ju_j^2\cdot\frac{N_0}{2}=\frac{N_0}{2}\)（\(\|\mathbf u\|=1\)，各坐标独立）：<b>白噪声在每个方向上一样大</b>。',
    r'所以 \(P(\mathbf s_i\to\mathbf s_k)=P\big(n>d_{ik}/2\big)=Q\!\left(\dfrac{d_{ik}/2}{\sqrt{N_0/2}}\right)=Q\!\left(\dfrac{d_{ik}}{\sqrt{2N_0}}\right)\)。和 3.3 节图里的 Q(d/2σ) 是同一个式子，σ = √(N₀/2)。',
    r'M 个点时，出错 = "比 \(\mathbf s_i\) 更靠近某个别的点"，是 M − 1 个事件的并集。并集的概率 ≤ 各概率之和（联合界）：<div class="calc">P_s ≤ Σ<sub>k≠i</sub> Q(d<sub>ik</sub>/√(2N₀)) ≤ (M − 1) Q(d<sub>min</sub>/√(2N₀))</div>最后一步：Q 是减函数，每个 \(d_{ik}\ge d_{\min}\)。',
    r'BPSK 只有两个点，M − 1 = 1，上界就是精确值：\(d_{\min}=2A\)，\(E_b=A^2\)，\(\dfrac{2A}{\sqrt{2N_0}}=\sqrt{\dfrac{2A^2}{N_0}}=\sqrt{\dfrac{2E_b}{N_0}}\)（p.21）。',
    ], 'P(s<sub>i</sub> → s<sub>k</sub>) = Q(d<sub>ik</sub>/√(2N₀))；P<sub>s</sub> ≤ (M − 1)Q(d<sub>min</sub>/√(2N₀))；BPSK 取等号') + X(
    'MPSK 的最小距离：M 越大越吃亏多少', r'''<p>MPSK 的 M 个点均匀排在半径 \(\sqrt{E_s}\) 的圆上，相邻两点夹角 2π/M，弦长 \(d_{\min}=2\sqrt{E_s}\sin(\pi/M)\)。M = 2：\(2\sqrt{E_s}\)；M = 4（QPSK）：\(1.414\sqrt{E_s}\)；M = 8：\(0.765\sqrt{E_s}\)。代入上界：\(P_s\le(M-1)\,Q\big(\sqrt{2\gamma_s}\sin(\pi/M)\big)\)。实际上每个点只有 2 个最近邻，所以常用近似 \(2Q\big(\sqrt{2\gamma_s}\sin(\pi/M)\big)\)。M 再翻倍（8 → 16），sin(π/M) 约减半，要多花约 6 dB 的 SNR 才能保持同样误码率，这就是 p.22 说的"点越挤，误码越多"。</p>''')))

BLOCKS.append(('learn_03.html', 'fadeavg', ('worked', 'BPSK 在瑞利衰落下需要多大平均 SNR'), W(
    '衰落下的平均误码率为什么只按 1/SNR 下降（p.31–32）', [
    r'公式 \(\bar P=\int_0^\infty P(\gamma)\,p(\gamma)\,d\gamma\)，瑞利衰落下 SNR 是指数分布 \(p(\gamma)=\frac{1}{\bar\gamma}e^{-\gamma/\bar\gamma}\)（第 2 章 p.26）。',
    r'DPSK 的 \(P(\gamma)=\tfrac12e^{-\gamma}\) 最好积分：两个指数相乘还是指数，用 \(\int_0^\infty e^{-a\gamma}d\gamma=1/a\)：<div class="calc">P̄ = (1/2γ̄) ∫₀^∞ e^(−γ(1 + 1/γ̄)) dγ = (1/2γ̄) · 1/(1 + 1/γ̄) = 1 / (2(1 + γ̄))</div>这正是第 4 章 p.25 中 M = 1 的结果。',
    r'高 SNR 时 \(\bar P\approx\dfrac{1}{2\bar\gamma}\)：γ̄ 提高 10 倍，误码率只降 10 倍。对比 AWGN 下 \(\tfrac12e^{-\gamma}\)：γ 从 10 到 20，误码率从 2.3×10⁻⁵ 降到 1.0×10⁻⁹。',
    r'原因：平均误码率几乎全部来自"掉进深衰落"的那段时间。SNR 低于 1 的概率 \(1-e^{-1/\bar\gamma}\approx1/\bar\gamma\)，这段时间里误码率接近 ½，所以 \(\bar P\) 正比于 1/γ̄。',
    r'中断概率是同一个 PDF 积到门限：\(P_{\mathrm{out}}=\int_0^{\gamma_0}\frac1{\bar\gamma}e^{-\gamma/\bar\gamma}d\gamma=1-e^{-\gamma_0/\bar\gamma}\)（p.31，第 1 章"由 PDF 求 CDF"）。',
    ], '瑞利 + DPSK：P̄ = 1/(2(1 + γ̄)) ≈ 1/(2γ̄)，线性下降；深衰落决定平均误码率，这正是第 4 章分集要解决的问题') + X(
    'BPSK 的结果', r'''<p>BPSK 的 \(Q(\sqrt{2\gamma})\) 积分要分部积分，结果是 \(\bar P_b=\tfrac12\Big(1-\sqrt{\tfrac{\bar\gamma}{1+\bar\gamma}}\Big)\approx\dfrac{1}{4\bar\gamma}\)。γ̄ = 100（20 dB）时 2.48×10⁻³，而 AWGN 下 20 dB 的 BPSK 误码率小到可以忽略。讲义只要求 p.32 的结论（衰落下线性下降），不要求这个积分。</p>''')))

# ================================================================ CH 4
BLOCKS.append(('learn_04.html', 'sdpdf', ('worked', '选择分集的中断概率（第 4 章 p.13）'), W(
    '选择分集的 CDF、PDF 和平均输出 SNR（p.11–12）', [
    r'<b>CDF</b>："最大值小于 γ" ⇔ "每一路都小于 γ"。独立 → 相乘：\(F(\gamma)=P(\gamma_{SD}\lt\gamma)=\prod_iP(\gamma_i\lt\gamma)=\big(1-e^{-\gamma/\bar\gamma}\big)^M\)。把 γ 换成门限 γ₀ 就是中断概率。',
    r'<b>PDF</b>：对 CDF 求导（链式法则，外层 \(u^M\)，内层 \(u=1-e^{-\gamma/\bar\gamma}\)，\(u^{\prime}=\frac1{\bar\gamma}e^{-\gamma/\bar\gamma}\)）：<div class="calc">p(γ) = (M/γ̄) (1 − e^(−γ/γ̄))^(M−1) e^(−γ/γ̄)　← p.12</div>',
    r'<b>M = 2 的平均值</b>：\(p(\gamma)=\frac2{\bar\gamma}\big(e^{-\gamma/\bar\gamma}-e^{-2\gamma/\bar\gamma}\big)\)。用 \(\int_0^\infty\gamma e^{-b\gamma}d\gamma=1/b^2\)：<div class="calc">E[γ_SD] = (2/γ̄)(γ̄² − γ̄²/4) = 2γ̄ − γ̄/2 = 1.5γ̄ = γ̄(1 + 1/2)</div>',
    r'一般 M：把 \((1-e^{-\gamma/\bar\gamma})^{M-1}\) 用二项式展开、逐项积分，结果整理成 \(\bar\gamma\sum_{i=1}^M\frac1i\)（讲义直接给结果）。第 M 路只多贡献 γ̄/M：<b>收益递减</b>，2 路 1.5 倍，3 路 1.83 倍，6 路 2.45 倍。',
    r'通信成功的概率 = 1 − 中断概率 = \(1-(1-e^{-\gamma_0/\bar\gamma})^M\)（p.12）。',
    ], 'F(γ) = (1 − e<sup>−γ/γ̄</sup>)<sup>M</sup>；p(γ) = 求导；γ̄<sub>SD</sub> = γ̄ Σ 1/i')))

BLOCKS.append(('learn_04.html', 'mrcsnr', ('worked', '三种合并方法比一比'), W(
    'MRC 和 EGC 的输出 SNR，以及为什么 MRC 最好（p.15–16、p.19）', [
    r'<b>MRC 合并</b>：把 \(r_i=A_ie^{j\theta_i}s+w_i\) 代进 \(y=\sum_iA_ie^{-j\theta_i}r_i\)：<div class="calc">y = (Σ A<sub>i</sub>²) s + Σ A<sub>i</sub>e<sup>−jθ<sub>i</sub></sup> w<sub>i</sub></div>\(e^{-j\theta_i}e^{j\theta_i}=1\)：所有支路的相位都转到 0，信号同相相加（p.16）。',
    r'<b>信号功率</b>：\((\sum A_i^2)^2E_b\)。<b>噪声功率</b>：各 \(w_i\) 独立、方差 \(N_0\)；乘 \(A_ie^{-j\theta_i}\) 后方差 \(A_i^2N_0\)（\(|e^{-j\theta}|=1\) 不改变功率）；独立相加，方差相加 → \(\sum A_i^2N_0\)。',
    r'相除：\(\gamma_{MRC}=\dfrac{(\sum A_i^2)^2E_b}{\sum A_i^2N_0}=\dfrac{\sum A_i^2E_b}{N_0}=\sum_i\gamma_i\)，\(\gamma_i=A_i^2E_b/N_0\) 是第 i 路单独的 SNR。',
    r'<b>EGC</b>：权重只有 \(e^{-j\theta_i}\)。信号 \((\sum A_i)s\)，功率 \((\sum A_i)^2E_b\)；噪声 M 路各 \(N_0\)，共 \(MN_0\)：\(\gamma_{EGC}=\dfrac{(\sum A_i)^2E_b}{MN_0}\)（p.19）。',
    r'<b>为什么 MRC 最好</b>：任意权重 \(\beta_i\) 时 \(\mathrm{SNR}=\dfrac{|\sum\beta_iA_ie^{j\theta_i}|^2E_b}{\sum|\beta_i|^2N_0}\)。由柯西-施瓦茨 \(|\sum\beta_ia_i|^2\le\sum|\beta_i|^2\sum|a_i|^2\)，SNR ≤ \(\sum A_i^2E_b/N_0\)，当 \(\beta_i\propto A_ie^{-j\theta_i}\)（增益的共轭）时取等号。EGC、SD 都是某种特殊的权重，所以都不超过 MRC。第 5 章 p.13–15 是同一个推导的矩阵写法。',
    ], 'γ<sub>MRC</sub> = Σγ<sub>i</sub>（最优）；γ<sub>EGC</sub> = (ΣA<sub>i</sub>)²E<sub>b</sub>/(MN₀)；γ<sub>SD</sub> = max γ<sub>i</sub>')))

BLOCKS.append(('learn_04.html', 'dpsksd', ('text', '      <div class="formula-card">\n        <div class="flbl">阵列增益与分集增益（p.27–28）</div>'), W(
    'DPSK + 选择分集的积分（p.24–26）', [
    r'代入 \(P_b(\gamma)=\tfrac12e^{-\gamma}\) 和上面推出的 SD 的 PDF：<div class="calc">P̄ = ∫₀^∞ ½e^(−γ) · (M/γ̄)(1 − e^(−γ/γ̄))^(M−1) e^(−γ/γ̄) dγ</div>',
    r'二项式展开 \((1-x)^{M-1}=\sum_{n=0}^{M-1}\binom{M-1}{n}(-1)^nx^n\)，\(x=e^{-\gamma/\bar\gamma}\)。每一项都只是一个指数：\(e^{-\gamma}\cdot e^{-n\gamma/\bar\gamma}\cdot e^{-\gamma/\bar\gamma}=e^{-\gamma(1+(n+1)/\bar\gamma)}\)。',
    r'逐项用 \(\int_0^\infty e^{-a\gamma}d\gamma=1/a\)，\(a=1+\frac{n+1}{\bar\gamma}\)：<div class="calc">(M/2γ̄)(−1)ⁿ C(M−1, n) · 1/(1 + (n+1)/γ̄) = (M/2)(−1)ⁿ C(M−1, n) / (γ̄ + n + 1)</div>求和就是讲义 p.25 的公式。',
    r'M = 1：\(\dfrac{1}{2(\bar\gamma+1)}\)。M = 2：\(\dfrac{1}{\bar\gamma+1}-\dfrac{1}{\bar\gamma+2}=\dfrac{1}{(\bar\gamma+1)(\bar\gamma+2)}\approx\dfrac1{\bar\gamma^2}\)。数值：γ̄ = 10 时 0.045 → 0.0076；γ̄ = 100 时 4.95×10⁻³ → 9.7×10⁻⁵。',
    ], '高 SNR 时 P̄ ∝ γ̄<sup>−M</sup>：log-log 图上斜率 = −M，这个 M 就是分集阶数 d')))

# ================================================================ CH 5
BLOCKS.append(('learn_05.html', 'xxh', ('worked', 'Alamouti 的判决变量（Practice 5 第 2 题）'), W(
    '验证 Alamouti 码正交：逐项算 X X<sup>H</sup>（p.22；2023-24 Q1(b)(iii)）', [
    r'\(\mathbf X=\begin{bmatrix}s_1&s_2\\-s_2^*&s_1^*\end{bmatrix}\)，共轭转置 \(\mathbf X^H=\begin{bmatrix}s_1^*&-s_2\\s_2^*&s_1\end{bmatrix}\)（先转置，再每个元素取共轭）。',
    r'(1,1)：\(s_1s_1^*+s_2s_2^*=|s_1|^2+|s_2|^2\)；(2,2)：\((-s_2^*)(-s_2)+s_1^*s_1=|s_1|^2+|s_2|^2\)。',
    r'(1,2)：\(s_1(-s_2)+s_2s_1=0\)；(2,1)：\((-s_2^*)s_1^*+s_1^*s_2^*=0\)。交叉项正好抵消。',
    r'所以 \(\mathbf X\mathbf X^H=(|s_1|^2+|s_2|^2)\mathbf I=\|\mathbf s\|^2\mathbf I\)，满足 OSTBC 的定义（p.27）。同样可以验证 \(\mathbf X^H\mathbf X=\|\mathbf s\|^2\mathbf I\)。',
    ], '第二行 = 两个符号<b>对调</b> + <b>取共轭</b> + <b>一个负号</b>，三者缺一不可，交叉项才会抵消')))

BLOCKS.append(('learn_05.html', 'alaml', ('text', '      <div class="formula-card">\n        <div class="flbl">SNR 对比（p.26、p.30）</div>'), W(
    'Alamouti 的 ML 检测和每个符号的 SNR（p.23–26）', [
    r'接收模型 \(\tilde{\mathbf y}=\mathbf F\mathbf s+\tilde{\mathbf v}\)，噪声白、高斯 → ML = 最小化 \(\|\tilde{\mathbf y}-\mathbf F\mathbf s\|^2\)（第 3 章：ML = 最小距离）。',
    r'展开：\(\|\tilde{\mathbf y}-\mathbf F\mathbf s\|^2=\|\tilde{\mathbf y}\|^2-2\mathrm{Re}\{\mathbf s^H\mathbf F^H\tilde{\mathbf y}\}+\mathbf s^H\mathbf F^H\mathbf F\mathbf s\)，而 \(\mathbf F^H\mathbf F=\|\mathbf h\|^2\mathbf I\)，最后一项 = \(\|\mathbf h\|^2\|\mathbf s\|^2\)。',
    r'配方（p.23）：上式 \(=\dfrac{1}{\|\mathbf h\|^2}\big\|\mathbf F^H\tilde{\mathbf y}-\|\mathbf h\|^2\mathbf s\big\|^2+\Big[\|\tilde{\mathbf y}\|^2-\dfrac{\|\mathbf F^H\tilde{\mathbf y}\|^2}{\|\mathbf h\|^2}\Big]\)。展开第一项就能验证；方括号和 s 无关（\(\mathbf F\mathbf F^H=\|\mathbf h\|^2\mathbf I\) 时它等于 0）。',
    r'第一项为 0 时最小：\(\hat{\mathbf s}=\dfrac{1}{\|\mathbf h\|^2}\mathbf F^H\tilde{\mathbf y}=\mathbf s+\dfrac{1}{\|\mathbf h\|^2}\mathbf F^H\tilde{\mathbf v}\)（p.24）。<b>两个符号各自独立判决</b>，不用联合搜索 M² 种组合。',
    r'噪声协方差：\(\dfrac{1}{\|\mathbf h\|^4}\mathbf F^HE[\tilde{\mathbf v}\tilde{\mathbf v}^H]\mathbf F=\dfrac{\sigma^2}{\|\mathbf h\|^4}\mathbf F^H\mathbf F=\dfrac{\sigma^2}{\|\mathbf h\|^2}\mathbf I\)，所以 \(\hat{\mathbf s}\sim\mathcal N\big(\mathbf s,\frac{\sigma^2}{\|\mathbf h\|^2}\mathbf I\big)\)；每个符号的 SNR \(=\dfrac{E\{|s_n|^2\}}{\sigma^2}(|h_1|^2+|h_2|^2)\)（p.25）。',
    r'和 MRC 比：总功率相同时两根天线各发一半，\(E\{|s_n|^2\}=E_b/2\)，SNR = \(\tfrac12\|\mathbf h\|^2E_b/\sigma^2\)；1 发 2 收 MRC 是 \(\|\mathbf h\|^2E_b/\sigma^2\)。分集阶数相同（都是 2），Alamouti 少 3 dB 阵列增益（p.30）。',
    ], 'ŝ = F<sup>H</sup>ỹ/‖h‖² = s + 噪声，噪声方差 σ²/‖h‖²；SNR ∝ |h₁|² + |h₂|²')))

BLOCKS.append(('learn_05.html', 'cap', ('text', '      <ul>\n        <li><b>SISO</b>（N = M = 1）'), W(
    'MIMO 容量化成"r 条管道之和"，以及 SIMO / MISO（p.33–38）', [
    r'\(\mathbf H\mathbf P\mathbf H^H\) 是 M×M 的半正定厄米矩阵，可以特征分解 \(\mathbf U\boldsymbol\Lambda\mathbf U^H\)，\(\mathbf U^H\mathbf U=\mathbf I\)，\(\boldsymbol\Lambda=\mathrm{diag}(\lambda_1,\dots,\lambda_r,0,\dots)\)（p.33）。',
    r'取 \(\mathbf A=\mathbf U\)、\(\mathbf B=\frac{1}{\sigma^2}\boldsymbol\Lambda\mathbf U^H\)，用 \(\det(\mathbf I+\mathbf A\mathbf B)=\det(\mathbf I+\mathbf B\mathbf A)\)：<div class="calc">det(I + UΛU<sup>H</sup>/σ²) = det(I + ΛU<sup>H</sup>U/σ²) = det(I + Λ/σ²)</div>',
    r'对角矩阵的行列式 = 对角元素之积 \(\prod_i(1+\lambda_i/\sigma^2)\)（\(\lambda_i=0\) 的项是 1）。log 把积变成和：\(C=B\sum_{i=1}^r\log_2(1+\lambda_i/\sigma^2)\)（p.34）。',
    r'<b>SIMO</b>（N = 1，h 是 M×1，P 是一个数）：\(\mathbf H\mathbf P\mathbf H^H=P\mathbf h\mathbf h^H\)，秩 1，唯一的非零特征值是 \(P\mathbf h^H\mathbf h=P\|\mathbf h\|^2\)：\(C=B\log_2(1+P\|\mathbf h\|^2/\sigma^2)\)（p.37）。加接收天线只是让 \(\|\mathbf h\|^2\) 变大，容量按 log 增长。',
    r'<b>MISO</b>（M = 1，h 是 1×N）：\(\mathbf h\mathbf P\mathbf h^H\) 是一个数。讲义 p.38 写成 \(P\|\mathbf h\|^2\)，对应把全部功率沿 h 的方向发（发射端知道信道）；不知道信道、功率平分 \(\mathbf P=\frac PN\mathbf I\) 时是 \(\frac PN\|\mathbf h\|^2\)。两种情况都只有 1 条管道。',
    r'<b>高 SNR</b>：\(\log_2(1+x)\approx\log_2x\)，各 \(\lambda_i\) 都和总功率成正比，所以 \(C\approx r\,B\log_2\mathrm{SNR}+\)常数：SNR 每翻一倍，容量多 r bit/s/Hz，r 最大 min(N, M)（第 4 章 p.31 的复用增益）。',
    ], 'C = B Σ log₂(1 + λ<sub>i</sub>/σ²)：r 条并行 SISO 管道；SIMO/MISO 只有 1 条，r = 1')))

# ================================================================ CH 6
BLOCKS.append(('learn_06.html', 'noisevar', ('worked', '迫零均衡把噪声放大多少'), W(
    '白噪声经过 FIR 滤波器后的方差 = σ² × 系数平方和（p.25、p.27）', [
    r'均衡器输出的噪声是输入噪声和系数的卷积：\(w^{\prime}_n=\sum_ic_iw_{n-i}\)。均值 \(E[w^{\prime}_n]=\sum_ic_iE[w_{n-i}]=0\)。',
    r'方差：\(E[(w^{\prime}_n)^2]=E\Big[\sum_ic_iw_{n-i}\sum_kc_kw_{n-k}\Big]=\sum_i\sum_kc_ic_k\,E[w_{n-i}w_{n-k}]\)。',
    r'白噪声：不同时刻不相关，\(E[w_{n-i}w_{n-k}]=\sigma^2\)（i = k）或 0（i ≠ k）。双重求和只剩对角项：<mark class="hl">\(\sigma^{\prime 2}=\sigma^2\sum_ic_i^2=\sigma^2\|\mathbf c\|^2\)</mark>（p.27）。',
    r'理想 ZF 的无限长系数，例如 \(1/(1+az^{-1})=\sum_k(-a)^kz^{-k}\)：平方和是等比级数 \(\sum_ka^{2k}=\dfrac{1}{1-a^2}\)（|a| &lt; 1），输出噪声 \(\sigma^2/(1-a^2)\)。',
    r'首项 \(c_0=1\) 时 \(\sum c_i^2\ge1\)，只要还有别的非零系数就 &gt; 1：<b>线性均衡器一定放大噪声</b>（2025-26 S1 Q2(a)(iii)）。',
    ], 'σ′² = σ² Σ c<sub>i</sub>²；例 c = {1, −0.3}：Σc² = 1.09（不是 (Σc)² = 0.49）')))

BLOCKS.append(('learn_06.html', 'perf', ('worked', '有 ISI 时的误码率（Practice 6 第 2 题）'), W(
    '有 ISI 时误码率的一般算法（p.27–28）', [
    r'均衡器输出：\(y_n=m_nq_0+\sum_{i\ne0}m_{n-i}q_i+w^{\prime}_n\)。q 是信道和均衡器级联后的响应（\(Q(z)=H(z)C(z)\)，p.22），\(w^{\prime}_n\sim\mathcal N(0,\sigma^2\|\mathbf c\|^2)\)。没有均衡器时 q 就是信道系数 h。',
    r'先固定其他所有符号（记为 \(\mathbf m_l\)），ISI 就是一个确定的数。发 \(m_n=+1\) 时出错 ⇔ \(y_n\lt0\) ⇔ \(w^{\prime}_n\lt-\big(q_0+\sum_{i\ne0}m_{n+i}q_i\big)\)。',
    r'高斯左尾 = 右尾：\(P_e\mid\mathbf m_l=Q\!\left(\dfrac{q_0+\sum_{i\ne0}m_{n+i}q_i}{\sigma\|\mathbf c\|}\right)\)（p.28）。分子是"这一种 ISI 组合下，信号离门限多远"。',
    r'再对 ISI 组合取平均：每个干扰符号 ±1 等概，K 个干扰项共 \(2^K\) 种组合，各占 \(1/2^K\)。一个干扰项：\(\tfrac12\big[Q\big(\frac{q_0+q_1}{\sigma^{\prime}}\big)+Q\big(\frac{q_0-q_1}{\sigma^{\prime}}\big)\big]\)；两个干扰项：\(q_0\pm q_1\pm q_2\) 四种，各 ¼。',
    r'发 −1 由对称性结果相同，所以只算发 +1 的情况就是总误码率。',
    ], 'P<sub>e</sub> = E[ Q((q₀ + Σ m q<sub>i</sub>)/σ′) ]：固定 ISI → Q 函数 → 对 ISI 组合平均') + X(
    'MMSE 系数的一般解法（正交原理）', r'''<p>线性 MMSE 要最小化 \(E\big[(s-\sum_ic_ir_i)^2\big]\)（p.26）。对每个 \(c_j\) 求导令其为 0：\(-2E\big[(s-\sum_ic_ir_i)\,r_j\big]=0\)，即<b>估计误差和每个观测都不相关</b>（正交原理），得到一组线性方程 \(\sum_ic_iE[r_ir_j]=E[sr_j]\)。Practice 6 第 3 题只有一个待定系数 q：误差 \(u_n-A_n=\tfrac q2A_n+\tfrac12A_{n-1}+qA_{n+1}+z_n+qz_{n+1}\)，观测 \(y_{n+1}=A_{n+1}+\tfrac12A_n+z_{n+1}\)，两者乘积的期望 \(=\tfrac q4+q+q=2.25q\)，令其为 0 得 q = 0，和直接对 1.25 + 2.25q² 求导的结果一样。噪声很小时 MMSE 趋近 ZF；噪声大时 MMSE 少消一点 ISI、少放大一点噪声。</p>''')))

BLOCKS.append(('learn_06.html', 'ls', ('text', '      <!-- ENR:learn_06.html:summary -->'), W(
    'LS 信道估计和"MSE ∝ N²"（p.37–38）', [
    r'先看最简单的标量情况：1 发 1 收，发已知的训练符号 x，收到 \(y=hx+v\)。让 \(|y-hx|^2\) 最小：\(\hat h=\dfrac{yx^*}{|x|^2}\)，就是"收到的除以发出的"。',
    r'矩阵情况：目标 \(J(\mathbf H)=\|\mathbf Y-\mathbf H\mathbf X\|^2\)。对 H 求导令其为 0（和第 2 章最小二乘求导同理）：\((\mathbf Y-\mathbf H\mathbf X)\mathbf X^H=\mathbf 0\)，即 \(\mathbf H\mathbf X\mathbf X^H=\mathbf Y\mathbf X^H\)。',
    r'\(\mathbf X\mathbf X^H\) 可逆（训练长度 ≥ N，各行线性无关）时：\(\hat{\mathbf H}_{LS}=\mathbf Y\mathbf X^H(\mathbf X\mathbf X^H)^{-1}=\mathbf Y\mathbf X^\dagger\)（p.37）。',
    r'最优训练 \(\mathbf X\mathbf X^H=\frac PN\mathbf I\)，逆矩阵就是 \(\frac NP\mathbf I\)：\(\hat{\mathbf H}_{LS}=\frac NP\mathbf Y\mathbf X^H=\frac NP(\mathbf H\mathbf X+\mathbf V)\mathbf X^H=\mathbf H+\frac NP\mathbf V\mathbf X^H\)（p.38）。',
    r'误差 \(\frac NP\mathbf V\mathbf X^H\) 的均方值（V 的 M×T 个元素独立、方差 σ²，\(\mathrm{tr}(\mathbf X\mathbf X^H)=P\)）：<div class="calc">E‖(N/P) V X<sup>H</sup>‖² = (N/P)² · Mσ² · tr(X X<sup>H</sup>) = M N² σ² / P</div>总功率 P 固定时，发射天线越多，每根分到的训练功率越少、要估计的未知数越多，MSE ∝ N²。',
    ], 'Ĥ = Y X<sup>H</sup>(X X<sup>H</sup>)<sup>−1</sup>；最优训练下 Ĥ = H + (N/P)VX<sup>H</sup>，MSE = MN²σ²/P')))

# ================================================================ CH 7
BLOCKS.append(('learn_07.html', 'ortho', ('text', '      <p>频谱互相重叠，所以 OFDM 比传统频分复用'), W(
    '子载波为什么正交、频谱为什么是 sinc（p.7、p.9–11）', [
    r'\(\dfrac1T\int_0^Te^{j2\pi(j-k)t/T}dt\)。j = k 时被积函数恒为 1，结果 1。',
    r'j ≠ k 时记 m = j − k（非零整数）：<div class="calc">(1/T) · [ e^(j2πmt/T) / (j2πm/T) ]₀^T = (e^(j2πm) − 1) / (j2πm) = 0</div>因为 \(e^{j2\pi m}=1\)。物理意义：两个子载波的差频在 T 秒内正好转整数圈，正负面积抵消。子载波间隔必须正好是 1/T 的整数倍。',
    r'<b>频谱</b>：每个子载波只持续 T 秒，相当于乘了一个宽 T 的矩形窗。矩形窗的傅里叶变换是 sinc，所以第 k 个子载波的频谱幅度 ∝ \(\mathrm{sinc}(fT-k)\)，主瓣中心在 f = k/T（p.9）。',
    r'\(\mathrm{sinc}(x)=\dfrac{\sin\pi x}{\pi x}\) 在所有非零整数 x 处为 0。在 f = k/T 处，其他子载波的值 \(\mathrm{sinc}(k-m)=0\)，只剩 \(s_k\)：<b>频谱重叠但在采样点上互不干扰</b>（p.10 的图）。',
    r'N 个子载波的主瓣铺满约 N/T 的宽度，N 很大时总带宽 \(B\approx N/T=1/T_s\)（p.11）。',
    ], '间隔 1/T → 差频整数圈 → 积分为 0；频域里每个 sinc 的峰正好落在其他 sinc 的零点上')))

BLOCKS.append(('learn_07.html', 'idft', ('text', '      <!-- ENR:learn_07.html:7.2 -->'), W(
    '发端是 IDFT、收端是 DFT（p.19–20）', [
    r'一个块内 \(x(t)=\frac{1}{\sqrt T}\sum_ks_ke^{j2\pi kt/T}\)。每 \(T_s=T/N\) 采样一次，\(t=iT/N\)：\(x_i=\frac{1}{\sqrt T}\sum_{k=0}^{N-1}s_ke^{j2\pi ki/N}\)，i = 0 … N − 1。和 N 点 IDFT \(x_i=\frac1N\sum_ks_ke^{j2\pi ki/N}\) 只差一个常数（讲义 p.19 写的是 1/N 版本）。',
    r'收端对 N 个采样做 DFT：<div class="calc">Σ<sub>i</sub> x<sub>i</sub> e^(−j2πik/N) = (1/N) Σ<sub>m</sub> s<sub>m</sub> Σ<sub>i</sub> e^(j2π(m−k)i/N)</div>',
    r'里面的和是等比数列，公比 \(q=e^{j2\pi(m-k)/N}\)。m = k 时 q = 1，和为 N；m ≠ k 时 \(\sum_{i=0}^{N-1}q^i=\dfrac{1-q^N}{1-q}=\dfrac{1-e^{j2\pi(m-k)}}{1-q}=0\)。所以结果正好是 \(s_k\)：这是上面积分正交的<b>离散版本</b>。',
    r'p.20 的相关器 \(\frac1T\int_0^Tx(t)e^{-j2\pi kt/T}dt\) 用 N 个采样求和近似，就是 DFT。N 个相关器 = 一次 FFT，运算量 N log N，而不是 N² 次乘法。',
    ], 'x = IDFT{s}，s = DFT{x}；离散正交 Σ<sub>i</sub> e<sup>j2π(m−k)i/N</sup> = Nδ[m − k]')))

BLOCKS.append(('learn_07.html', 'circ', ('worked', '最短需要多长的循环前缀'), W(
    '为什么加了循环前缀以后 r<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + w<sub>k</sub>（p.15–22）', [
    r'采样后的多径信道是离散卷积：\(r_i=\sum_{l=0}^{L-1}h_lx_{i-l}+w_i\)，L 个抽头，最长的回波晚 L − 1 个采样。',
    r'<b>没有 CP</b>：块内前几个采样（i &lt; L − 1）里，\(x_{i-l}\) 的下标是负的，取到的是<b>上一个块</b>的数据 → 块间干扰（p.16 的 Delay Spread 项）；接收窗口里看到的也不是完整的周期信号，子载波失去正交 → ICI。',
    r'<b>有 CP</b>：发送 \(x_{-G},\dots,x_{-1},x_0,\dots,x_{N-1}\)，其中 \(x_{-m}=x_{N-m}\)（块尾复制到块头，p.21）。只要 <mark class="hl">G ≥ L − 1</mark>，接收端保留的 i = 0 … N − 1 用到的 \(x_{i-l}\) 下标都 ≥ −G，全在本块里，而且 \(x_{i-l}=x_{(i-l)\bmod N}\)：<div class="calc">r<sub>i</sub> = Σ<sub>l</sub> h<sub>l</sub> x<sub>(i−l) mod N</sub> + w<sub>i</sub>　← 循环卷积</div>',
    r'代入 \(x_n=\frac1N\sum_ks_ke^{j2\pi kn/N}\)。\(e^{j2\pi kn/N}\) 以 N 为周期，mod N 不影响它：<div class="calc">r<sub>i</sub> = (1/N) Σ<sub>k</sub> s<sub>k</sub> e^(j2πki/N) · Σ<sub>l</sub> h<sub>l</sub> e^(−j2πkl/N) + w<sub>i</sub> = (1/N) Σ<sub>k</sub> (H<sub>k</sub>s<sub>k</sub>) e^(j2πki/N) + w<sub>i</sub></div>中间那个求和正是 \(H_k=\sum_lh_le^{-j2\pi lk/N}\)（p.15）。',
    r'上式说明 \(\{r_i\}\) 是 \(\{H_ks_k\}\) 的 IDFT。收端做 DFT：<mark class="hl">\(R_k=H_ks_k+W_k\)</mark>（p.22）。每个子载波只乘一个复数，频域均衡就是除以 \(H_k\)（p.25）。',
    r'代价：每块多发 G 个采样，效率 N/(N + G)，功率损失 \(10\log_{10}\frac{N+G}{N}=10\log_{10}\frac{NT_s+T_G}{NT_s}\) dB（p.18）。',
    ], 'CP ≥ L − 1 → 线性卷积变循环卷积 → DFT 后变乘法：r<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + w<sub>k</sub>（用 h = {0.8, 0.6}、N = 4、G = 1 数值验证过）')))


def worked_start(s, title):
    i = s.find(title)
    if i < 0:
        raise SystemExit(f'title not found: {title}')
    j = s.rfind('<div class="worked">', 0, i)
    return s.rfind('\n', 0, j) + 1


def apply():
    files = sorted({b[0] for b in BLOCKS})
    n = 0
    for fn in files:
        f = B / fn
        s = f.read_text(encoding='utf-8')
        for _, name, _, _ in [b for b in BLOCKS if b[0] == fn]:
            s = re.sub(rf'<!-- DRV:{name} -->.*?<!-- /DRV:{name} -->\n', '', s, flags=re.S)
        for _, name, (kind, key), html in [b for b in BLOCKS if b[0] == fn]:
            block = f'      <!-- DRV:{name} -->\n      {html}<!-- /DRV:{name} -->\n'
            if kind == 'worked':
                i = worked_start(s, key)
            else:
                i = s.find(key)
                if i < 0:
                    raise SystemExit(f'anchor for {name} not found')
                i = s.rfind('\n', 0, i) + 1
            s = s[:i] + block + s[i:]
            n += 1
        f.write_text(s, encoding='utf-8')
    print('derivations added:', n)

apply()
