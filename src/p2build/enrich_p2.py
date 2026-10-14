#!/usr/bin/python3
"""Add importance stars, key-point boxes, pitfalls and extra explanations to Part 2 chapters 3–7.

Idempotent: each insertion is wrapped in <!-- ENR:id --> ... <!-- /ENR:id --> and skipped if present;
stars are only added to an <h3> that has no .imp badge yet.  Run before build_learn.py.
"""
import pathlib, re

B = pathlib.Path(__file__).parent
STAR = {3: '<span class="imp">★★★ 必考</span>', 2: '<span class="imp i2">★★ 常考</span>', 1: '<span class="imp i1">★ 了解</span>'}

def S(n, html):
    return f'<div class="wstep"><div class="wn">{n}</div><div class="wtext">{html}</div></div>'

GAUSS = (B / 'gauss_svg.txt').read_text(encoding='utf-8')

# ------------------------------------------------------------------ chapter 3
CH3 = {
 'stars': {'3.1': 2, '3.2': 2, '3.3': 3, '3.4': 1, '3.5': 2},
 'after': {
  '3.1': '''<div class="key"><div class="lbl">★ 考试重点 · 星座的维数和距离</div>
<ul><li><mark class="hl">维数 = 拼出所有信号需要的正交基函数个数</mark>：只用一个 cos（PAM、二进制 ±A）是 1 维；cos 和 sin 都用（PSK、QPSK、QAM）是 2 维。</li>
<li>两点间的距离就是坐标差的长度：±1 两点距离 2；QPSK 四点 (±1, ±1) 相邻点距离 2、对角距离 2√2。</li>
<li>期末 2025-26 S1 Q1(a)(i) 原题：画 ±1 的星座，求维数（1）和距离（2）。</li></ul></div>''',
  '3.3': '''<h4>二进制检测：一张图看懂 P<sub>b</sub> = Q(d/2σ)</h4>
<p>这是第 3 章最常考的计算，也是第 4、6 章所有误码率题的底子。设发 s = +A 或 −A（等概），收到 y = s + w，w ~ N(0, σ²)：</p>
''' + GAUSS + '''
<ol class="steps">
<li><b>条件分布</b>：s 固定时 y 只是把噪声平移了 s，所以 y | s = +A ~ N(+A, σ²)，y | s = −A ~ N(−A, σ²)（第 1 章：加常数只改均值，方差不变）。</li>
<li><b>判决门限</b>：两个钟形曲线一样胖、一样高（等概），ML 判决就是"离谁近判谁"，门限在中点 0：y &gt; 0 判 +A，y ≤ 0 判 −A。</li>
<li><b>误码率</b>：发 +A 却判成 −A，要噪声把 y 拉到 0 以下，即 w &lt; −A。A 是 A/σ 个标准差：<mark class="hl">P<sub>b</sub> = Q(A/σ) = Q(d/(2σ))</mark>，d = 2A 是两点距离。发 −A 由对称性一样。</li>
<li><b>换成 E<sub>b</sub>/N<sub>0</sub></b>：E<sub>b</sub> = A²，σ² = N<sub>0</sub>/2，得到 BPSK 的 Q(√(2E<sub>b</sub>/N<sub>0</sub>))。</li>
</ol>
<div class="worked"><summary><span class="wtag">例题</span>噪声方差 0.25 的 ±1 系统</summary><div class="wbody">
''' + S(1, 'σ = √0.25 = 0.5。门限 0，信号到门限的距离 1 = 2σ。') + S(2, '<div class="calc">P_b = Q(1/0.5) = Q(2) ≈ 0.0228</div>') + S(3, '噪声方差降到 0.09（σ = 0.3）：Q(1/0.3) = Q(3.33) ≈ 4×10⁻⁴。噪声标准差减小 40%，误码率降了 50 多倍：AWGN 下误码率随 SNR <b>指数</b>下降。') + '''<div class="wans">P_b = Q(2) ≈ 0.023（期末 2025-26 S1 Q1(a)(iii) 就是这组数）</div></div></div>
<div class="pitfall"><div class="lbl">⚠ 易错</div><ul>
<li>Q 里放的是"<b>信号到门限的距离 ÷ 标准差</b>"，是 d/2，不是整个距离 d。</li>
<li>先验概率不等或两边噪声方差不同时，门限不在中点（Practice 3 第 2 题），要用 ML / MAP 条件重新解门限。</li>
<li>有 ISI 时信号到门限的距离会随前一个符号变化，要分情况算再平均（第 6 章）。</li></ul></div>''',
  '3.5': '''<div class="key"><div class="lbl">★ 考试重点 · 衰落下的误码率</div><ul>
<li>平均误码率 = 把 AWGN 误码率按 SNR 的分布加权平均：连续分布用积分，<b>离散分布直接按概率加权求和</b>（第 4 章期末题都是离散的）。</li>
<li>瑞利衰落中断：P<sub>out</sub> = 1 − e<sup>−γ₀/γ̄</sup>，反求 γ̄ = γ₀ / (−ln(1 − P<sub>out</sub>))。</li>
<li>误码平台：多普勒要速率<b>高</b>，时延扩展要速率<b>低</b>，两个公式方向相反。</li></ul></div>''',
 },
 'summary': '''<div class="key"><div class="lbl">★ 第三章考试重点</div><ul>
<li>正交基、维数、星座图；两点距离。</li>
<li>AWGN 下 ML = 最小距离；二进制 P<sub>b</sub> = Q(d/2σ)，BPSK = Q(√(2γ<sub>b</sub>))。</li>
<li>y = s + w 的条件均值、方差和条件 PDF（第 1 章性质的直接应用）。</li>
<li>衰落下平均误码率 = 加权平均；瑞利中断概率；两种误码平台。</li></ul></div>''',
}

# ------------------------------------------------------------------ chapter 4
CH4 = {
 'stars': {'4.1': 2, '4.2': 3, '4.3': 3, '4.4': 3},
 'after': {
  '4.2': '''<div class="key"><div class="lbl">★ 考试重点 · 离散 SNR 分布下的 SD 和 MRC（期末 4 年考了 3 次）</div>
<ol class="steps">
<li><b>dB 全部换成线性值</b>。</li>
<li><b>列出两个支路的所有组合</b>和概率（独立 → 概率相乘）。两个取值就是 4 种组合，三个取值就是 9 种。</li>
<li><b>每种组合的输出 SNR</b>：SD 取较大的 max(γ₁, γ₂)；MRC 取和 γ₁ + γ₂。</li>
<li><b>加权平均</b>：平均输出 SNR = Σ 概率 × 输出 SNR；平均误码率 = Σ 概率 × P<sub>e</sub>(输出 SNR)，比如 DPSK 的 ½e<sup>−γ</sup>。</li></ol>
<p>捷径：<mark class="hl">MRC 的平均输出 SNR = 各支路平均 SNR 之和</mark>，不用列组合；但平均误码率仍要列组合（e<sup>−γ</sup> 不是线性的）。</p></div>
<div class="worked"><summary><span class="wtag">例题</span>SD 和 MRC 同一组数比一比（自编）</summary><div class="wbody">
<p>已知条件：两支路独立，每支路 SNR 以 0.5 的概率是 4、0.5 的概率是 9（线性值），DPSK，P<sub>s</sub> = ½e<sup>−γ</sup>。</p>
''' + S(1, '组合和概率：(4,4) 0.25，(4,9) 0.25，(9,4) 0.25，(9,9) 0.25。') + S(2, '<b>SD</b>：输出 4（只有两支都是 4 时，0.25）或 9（0.75）。<div class="calc">平均 = 0.25 × 4 + 0.75 × 9 = 7.75；P̄_s = 0.25 × ½e⁻⁴ + 0.75 × ½e⁻⁹ = 2.29×10⁻³ + 4.6×10⁻⁵ ≈ 2.3×10⁻³</div>') + S(3, '<b>MRC</b>：输出 8（0.25）、13（0.5）、18（0.25）。<div class="calc">平均 = 2 + 6.5 + 4.5 = 13（= 6.5 + 6.5）；P̄_s = 0.25 × ½e⁻⁸ + 0.5 × ½e⁻¹³ + 0.25 × ½e⁻¹⁸ ≈ 4.3×10⁻⁵</div>') + S(4, '单支路：P̄<sub>s</sub> = 0.5 × ½e⁻⁴ + 0.5 × ½e⁻⁹ ≈ 4.6×10⁻³。') + '''<div class="wans">误码率：单支路 4.6×10⁻³ → SD 2.3×10⁻³ → MRC 4.3×10⁻⁵；MRC 好得多，因为它把两路能量加起来</div></div></div>''',
  '4.3': '''<div class="key"><div class="lbl">★ 考试重点 · 阵列增益 g 和分集增益 d（2025-26 两次期末都考）</div>
<ul><li><mark class="hl">g = γ̄<sub>Σ</sub> / γ̄</mark>：合并器<b>输出</b>平均 SNR ÷ <b>输入</b>平均 SNR；dB 下就是两者相减（15 dB − 12 dB = 3 dB → g = 2）。</li>
<li><mark class="hl">P̄<sub>e</sub> ≈ γ̄<sup>−d</sup>，d ≈ −log₁₀P̄<sub>e</sub> / log₁₀γ̄</mark>，这里的 γ̄ 是合并器<b>输入</b>的平均 SNR（Practice 4 官方答案 d = 8.1 就是用输入 γ̄ = 10 算的）。</li>
<li>已知 d 求误码率：P̄<sub>e</sub> = γ̄<sup>−d</sup>（2025-26 S2：12 dB、d = 3.7 → 15.85<sup>−3.7</sup> ≈ 3.6×10⁻⁵）。</li>
<li>理论上 d ≤ M（M 支路），MIMO 满分集 d = N × M。由单个误码率点反算的 d 可能超过 M，这是高 SNR 近似的结果，按公式写即可。</li></ul></div>
<div class="pitfall"><div class="lbl">⚠ 易错</div><ul>
<li>用输出 SNR 代 d 的公式；或者 g 用 dB 值相除（应该相减，或者先换线性再相除）。</li>
<li>DPSK 的误码率是 ½e<sup>−γ</sup>，BPSK 是 Q(√(2γ))，题目会给，别混。</li></ul></div>''',
  '4.4': '''<div class="key"><div class="lbl">★ 考试重点 · 分集-复用折中的计算（2024-25 Q1(b)(ii)、Practice 5 第 3 题）</div>
<ol class="steps">
<li>最大分集 d<sub>max</sub> = N × M；最大复用 r<sub>max</sub> = min(N, M)；空间复用要 M ≥ N。</li>
<li>由误码率和 d 求 SNR：P<sub>e</sub> = SNR<sup>−d</sup> → SNR = P<sub>e</sub><sup>−1/d</sup>（10⁻³ 和 d = 3 → SNR = 10）。</li>
<li>速率 R = r · log₂SNR（r = 2 → 2 × log₂10 = 6.64 bit/s/Hz）。</li>
<li>检查 (r, d) 是否在最优曲线上：d(r) = (N − r)(M − r)。</li></ol></div>''',
 },
 'summary': '''<div class="key"><div class="lbl">★ 第四章考试重点</div><ul>
<li>独立分支：P<sub>out</sub> = P<sub>out,单支</sub><sup>M</sup>；SD 中断 (1 − e<sup>−γ₀/γ̄</sup>)<sup>M</sup>，会反求 M。</li>
<li>SD 取最大、MRC 取和、EGC 只对齐相位；MRC 平均输出 = 各支路平均之和。</li>
<li>离散 SNR 分布：列组合 → 输出 SNR → 加权平均。</li>
<li>g = 输出/输入；d 用输入 SNR；P<sub>e</sub> ≈ γ̄<sup>−d</sup>。</li>
<li>d(r) = (N − r)(M − r)，R = r log₂SNR。</li></ul></div>''',
}

# ------------------------------------------------------------------ chapter 5
CH5 = {
 'stars': {'5.1': 3, '5.2': 3, '5.3': 2, '5.4': 3, '5.5': 3},
 'after': {
  '5.1': '''<div class="key"><div class="lbl">★ 考试重点 · 写出 MIMO 模型（2025-26 S2 Q1(b)(ii)）</div>
<ul><li>N 根发射、M 根接收：y（M×1）= H（M×N）x（N×1）+ v（M×1）。<mark class="hl">H 的行对应接收天线、列对应发射天线</mark>，h<sub>ij</sub> 是第 j 根发射到第 i 根接收的增益。</li>
<li>为什么每对天线只有一个增益：<b>平坦衰落</b>下各条回波在一个符号内叠成一个复数，没有可分辨的多个抽头，也就没有 ISI。频率选择性时才会出现 H<sub>0</sub>, H<sub>1</sub>, … 多个矩阵（p.8）。</li>
<li>例：4 发 6 收 → H 是 6×4，y<sub>i</sub> = Σ<sub>j=1..4</sub> h<sub>ij</sub>x<sub>j</sub> + v<sub>i</sub>。</li></ul></div>''',
  '5.2': '''<div class="key"><div class="lbl">★ 答题模板 · SIMO 为什么能得到分集（2025-26 S1 Q1(b)(ii)）</div>
<ol class="steps"><li><b>为什么是 SIMO</b>：只有一个发送符号 s（单输入），收到两个信号 y₁、y₂（多输出）。</li>
<li><b>独立</b>：两根接收天线隔开足够远，h₁、h₂ 独立衰落，同时深衰落的概率是各自概率的乘积。</li>
<li><b>合并</b>：MRC 用 h₁*、h₂* 加权相加，有效增益 |h₁|² + |h₂|²，只要有一路好，输出 SNR 就不会太差 → 分集阶数 2。</li></ol></div>''',
  '5.4': '''<div class="key"><div class="lbl">★ 考试重点 · Alamouti 三件事</div>
<ul><li><b>验证正交</b>（2023-24 Q1(b)(iii)）：算 X X<sup>H</sup>。逐行做内积：同一行和自己的内积 = |s₁|² + |s₂|²；不同两行的内积要<b>抵消为 0</b>。成立就是 <mark class="hl">X X<sup>H</sup> = (|s₁|² + |s₂|²) I，正交 STBC</mark>。行列交换（转置）不影响结论。</li>
<li><b>有没有分集</b>（2023-24 Q1(b)(iv)）：有，2 发 1 收是 2 阶，2 发 M 收是 2M 阶（满分集），而且发射端不需要知道信道；代价是比 MRC 少 3 dB 阵列增益（p.30）。</li>
<li><b>检测后的统计量</b>（2025-26 S2 Q1(b)(iii)）：ŝ = s + Gw/‖h‖²。均值 E[ŝ] = s（噪声零均值，<b>无偏</b>）；方差乘了 1/‖h‖⁴：σ²‖h‖²/‖h‖⁴ = <mark class="hl">σ²/‖h‖²</mark>。两路增益相加让噪声变小，这就是分集。</li></ul></div>''',
  '5.5': '''<div class="key"><div class="lbl">★ 考试重点 · MIMO 容量的三种写法</div>
<ul><li><b>并行信道</b>（2025-26 S1 Q1(b)(iii)）：Λ 是对角阵 → det(I + Λ/σ²) = Π(1 + λ<sub>i</sub>/σ²) → <mark class="hl">C = B Σ log₂(1 + λ<sub>i</sub>/σ²)</mark>：r 条互不干扰的 SISO 信道容量之和。</li>
<li><b>发射端不知道信道</b>（2024-25 Q1(b)(iii)）：功率平分，P = (P/N)I → C = B log₂det(I + (P/(Nσ²))HH<sup>H</sup>)。N = M = 1、h = 2、P = 1、σ² = 0.25 时 C/B = log₂(1 + 4/0.25) = log₂17 ≈ 4.09。</li>
<li><b>高 SNR</b>：C/B ≈ min(N, M) log₂SNR，容量随天线数<b>线性</b>增长；SIMO / MISO 只按 log 增长。</li></ul></div>''',
 },
 'summary': '''<div class="key"><div class="lbl">★ 第五章考试重点</div><ul>
<li>y = Hx + v，H 是 M×N；平坦衰落 → 每对天线一个复增益。</li>
<li>SIMO/MRC：w ∝ h，SNR ∝ ‖h‖²；MISO 不知道信道时没有分集。</li>
<li>Alamouti：X X<sup>H</sup> = ‖s‖² I；满分集 2M；检测量无偏、方差 σ²/‖h‖²。</li>
<li>容量 = Σ log₂(1 + λ<sub>i</sub>/σ²)；不知道信道时 P/N 平分；复用增益 min(N, M)。</li></ul></div>''',
}

# ------------------------------------------------------------------ chapter 6
CH6 = {
 'stars': {'6.1': 3, '6.2': 1, '6.3': 3, '6.4': 2, '6.5': 1},
 'after': {
  '6.1': '''<div class="key"><div class="lbl">★ 先学会读 Z 变换（Q2(a) 四年都要用）</div>
<ul><li><b>Z⁻¹ 就是"晚一个符号"</b>。H(Z) = 1 + 0.3Z⁻¹ 的意思是：收到的 = 1 × 当前符号 + 0.3 × 上一个符号，即 h = {1, 0.3}，信道长度 L = 2（2025-26 S1 Q2(a)(i)）。</li>
<li>Z 的次数就是延迟几个符号：H(Z) = 1 + 0.6Z⁻² → 只有当前符号和前<b>两个</b>符号有关，中间那个系数是 0（2023-24 Q2(a)(ii)：按 r[i] = Σ h[n]m[i−n+1] 的编号，h[1] = 1、h[2] = 0、h[3] = 0.6）。</li>
<li><b>两个滤波器串起来 = 多项式相乘</b>：(1 − 0.6Z⁻²)(1 + 0.6Z⁻²) = 1 − 0.36Z⁻⁴。噪声只经过后一个滤波器。</li>
<li>写离散模型：<mark class="hl">r[n] = Σ<sub>i=1..L</sub> h[i] m[n − i + 1] + w[n]</mark>，除 i = 1 以外的项都是 ISI。</li></ul></div>''',
  '6.3': '''<div class="key"><div class="lbl">★ 考试重点 · 有残余 ISI 时的误码率（期末 Q2(a) 四年四次）</div>
<p>判决变量 y = m[n] + a·m[n−1] + w′，m = ±1 等概，w′ ~ N(0, σ′²)，按 sgn(y) 判决：</p>
<ol class="steps"><li><b>先算 σ′</b>：均衡器输出噪声方差 <mark class="hl">σ′² = σ²(c₀² + c₁² + …)</mark>（系数平方和），再开根号。</li>
<li><b>分两种情况</b>：发 +1 时，前一个符号同号 → 信号离门限 1 + a；异号 → 1 − a，各占一半。</li>
<li><b>平均</b>：<mark class="hl">P<sub>e</sub> = ½Q((1 − a)/σ′) + ½Q((1 + a)/σ′)</mark>。发 −1 对称，结果一样。</li></ol>
<div class="tblwrap" style="margin:8px 0"><table><thead><tr><th>期末</th><th>残余 ISI a</th><th>σ′</th><th>P<sub>e</sub></th></tr></thead><tbody>
<tr><td>2023-24 S2</td><td>0.36（滞后 4 个符号）</td><td>√(0.3 × 1.36) = 0.639</td><td>½[Q(1.00) + Q(2.13)] ≈ 0.087</td></tr>
<tr><td>2024-25 S2</td><td>0.6</td><td>0.8</td><td>½[Q(0.5) + Q(2)] ≈ 0.166</td></tr>
<tr><td>2025-26 S1</td><td>0.3（不均衡）</td><td>0.6</td><td>½[Q(1.17) + Q(2.17)] ≈ 0.068</td></tr>
<tr><td>2025-26 S2</td><td>0.2</td><td>√(0.25 × 2.56) = 0.8</td><td>½[Q(1) + Q(1.5)] ≈ 0.113</td></tr></tbody></table></div>
<p><b>迫零系数</b>：C(Z) = 1/H(Z)，用长除法展开取前几项；1/(1 + hZ⁻¹) = 1 − hZ⁻¹ + h²Z⁻² − …（2024-25：h = 0.2 → 1、−0.2、0.04）。<b>噪声增强</b>：任何 c₁、c₂ 不全为 0 的线性均衡器，输出噪声方差 σ²(1 + c₁² + c₂²) &gt; σ²（2025-26 S1 Q2(a)(iii)）。</p></div>
<div class="pitfall"><div class="lbl">⚠ 易错</div><ul>
<li>Q 函数里除的是<b>标准差</b> σ′，题目给的 0.25、0.36、0.64 都是方差。</li>
<li>只算 Q((1 − a)/σ) 一项、忘了另一半；或者忘了乘 ½。</li>
<li>噪声方差用系数和的平方 (Σc)²：应该是系数平方和 Σc²。</li></ul></div>''',
 },
 'summary': '''<div class="key"><div class="lbl">★ 第六章考试重点</div><ul>
<li>由 H(Z) 读抽头和 L；写出 r[n] = Σ h[i]m[n − i + 1] + w[n]；Nyquist 准则：等效脉冲在其他采样点为 0。</li>
<li>迫零 C = 1/H，长除法；噪声增强 σ²Σc²。</li>
<li>残余 ISI 误码率 ½[Q((1 − a)/σ′) + Q((1 + a)/σ′)]。</li>
<li>DFE：用已判决符号减掉过去的 ISI，不放大噪声，代价是错误传播。</li></ul></div>''',
}

# ------------------------------------------------------------------ chapter 7
CH7 = {
 'stars': {'7.1': 3, '7.2': 3, '7.3': 3, '7.4': 3, '7.5': 2},
 'after': {
  '7.1': '''<div class="key"><div class="lbl">★ 考试重点 · 子载波数和速率（期末每年都有一问）</div>
<ul><li><b>平坦条件</b>：每个子载波带宽 B/N 要小于相干带宽：<mark class="hl">N &gt; B/B<sub>C</sub></mark>，取整往上（2025-26 S1：500/30 = 16.7 → 17；2023-24：子载波带宽取 B<sub>C</sub>/2 → N = 1 MHz / 250 kHz = 4）。</li>
<li><b>时间关系</b>：原始符号时长 T<sub>s</sub> = 1/B；一个 OFDM 块 T = N T<sub>s</sub>（N 个符号并行，每个拉长 N 倍）。</li>
<li><b>速率</b>：每个 OFDM 块传 N log₂M 比特。不加保护间隔速率 = N log₂M / T；<mark class="hl">加了 T<sub>G</sub> 后有效速率 = N log₂M / (T + T<sub>G</sub>)</mark>（2025-26 S1：100 bit / 110 µs ≈ 909 kbit/s）。每个子载波的速率 = 总速率 / N（2024-25：10 Mbit/s → 每个 2.5 Mbit/s）。</li></ul></div>''',
  '7.2': '''<div class="key"><div class="lbl">★ 两个证明题的答题要点</div>
<ul><li><b>相关器输出 = s<sub>n</sub></b>（2025-26 S1 Q2(b)(iii)）：乘 (1/√T)e<sup>−j2πnt/T</sup> 在 [0, T] 积分，得 (1/T)Σ<sub>k</sub> s<sub>k</sub>∫e<sup>j2π(k−n)t/T</sup>dt。k = n 时被积函数为 1，积分 = T；k ≠ n 时是整数个周期的复指数，积分 = 0。所以只剩 s<sub>n</sub>。</li>
<li><b>为什么是 IDFT</b>（2025-26 S2 Q2(b)(ii)）：在一个块内按 t = iT/N 采样，x<sub>i</sub> = (1/√T)Σ s<sub>k</sub>e<sup>j2πki/N</sup>，和 N 点 IDFT 的式子只差一个常数。频域的 N 个符号变成时域的 N 个采样，发端用 IFFT、收端用 FFT。</li></ul></div>''',
  '7.3': '''<div class="key"><div class="lbl">★ 考试重点 · 手算 H<sub>k</sub>（N = 4 的速算表）</div>
<p><mark class="hl">H<sub>k</sub> = Σ<sub>i</sub> h<sub>i</sub> e<sup>−j2πik/N</sup></mark>，k = 1…N，H<sub>N</sub> = H<sub>0</sub>。N = 4 时 e<sup>−j2πk/4</sup> 依次是：</p>
<div class="tblwrap" style="margin:6px 0"><table><thead><tr><th>k</th><th>1</th><th>2</th><th>3</th><th>4（= 0）</th></tr></thead><tbody>
<tr><td>e<sup>−j2πk/4</sup>（乘 h₁）</td><td>−j</td><td>−1</td><td>j</td><td>1</td></tr>
<tr><td>e<sup>−j2π·2k/4</sup>（乘 h₂）</td><td>−1</td><td>1</td><td>−1</td><td>1</td></tr></tbody></table></div>
<p>例：h = {1, 0.3}（2025-26 S2）→ H₁ = 1 − 0.3j，H₂ = 0.7，H₃ = 1 + 0.3j，H₄ = 1.3。h = {1, −0.6, 0.2}（2023-24）→ 0.8 + 0.6j、1.8、0.8 − 0.6j、0.6。<b>自检</b>：H₄ = 所有抽头之和；H₁ 和 H₃ 互为共轭（抽头是实数时）。</p></div>''',
  '7.4': '''<div class="key"><div class="lbl">★ 考试重点 · 循环前缀</div>
<ul><li><b>表达式</b>（2024-25 Q2(b)(ii)）：式子不变，只把时间范围往前延长 T<sub>G</sub>：x(t) = (1/√T)Σ s<sub>k</sub>e<sup>j2πkt/T</sup>，<mark class="hl">nT − T<sub>G</sub> ≤ t &lt; (n+1)T</mark>。e<sup>j2πkt/T</sup> 以 T 为周期，所以前面多出来的一段正好是块尾的复制。</li>
<li><b>功率损失</b>：<mark class="hl">10 log₁₀[(NT<sub>s</sub> + T<sub>G</sub>)/(NT<sub>s</sub>)]</mark> dB（2023-24：4 µs + 1 µs → 0.97 dB；2025-26 S2：8 µs + 20 µs → 5.44 dB）。</li>
<li><b>长度</b>：T<sub>G</sub> ≥ 最大时延扩展；离散时 CP ≥ 信道长度 − 1 个采样（Practice 7 第 3 题）。</li></ul></div>''',
  '7.5': '''<div class="pitfall"><div class="lbl">⚠ 易错 · 等容量分配（2024-25 Q2(b)(iii)）</div><ul>
<li>C<sub>k</sub> = ¼log₂(1 + P<sub>k</sub>|H<sub>k</sub>|²) = 0.9 → 1 + P<sub>k</sub>|H<sub>k</sub>|² = 2<sup>3.6</sup>，别忘了先乘回 4。</li>
<li>给的是 |H<sub>k</sub>|，公式里要平方：|H₂| = 0.2 → |H₂|² = 0.04。</li></ul></div>''',
 },
 'summary': '''<div class="key"><div class="lbl">★ 第七章考试重点</div><ul>
<li>N &gt; B/B<sub>C</sub>；T = NT<sub>s</sub>；速率 N log₂M/(T + T<sub>G</sub>)。</li>
<li>子载波正交 → 相关器输出 s<sub>n</sub>；发端是 IDFT。</li>
<li>H<sub>k</sub> = Σ h<sub>i</sub>e<sup>−j2πik/N</sup>，N = 4 速算。</li>
<li>CP 表达式（nT − T<sub>G</sub> ≤ t）和功率损失 10 log((NT<sub>s</sub> + T<sub>G</sub>)/NT<sub>s</sub>)。</li>
<li>OFDM 容量 = Σ log₂(1 + |H<sub>k</sub>|²P<sub>k</sub>/N<sub>k</sub>)，最优是注水；频域均衡 ŝ<sub>k</sub> = R<sub>k</sub>/H<sub>k</sub>。</li></ul></div>''',
}

def wrap(tag, html):
    return f'<!-- ENR:{tag} -->\n      {html}\n      <!-- /ENR:{tag} -->\n      '

def apply(fname, spec):
    p = B / fname
    s = p.read_text(encoding='utf-8')
    for num, lvl in spec['stars'].items():
        s = re.sub(rf'(<h3><span class="zh-num">{re.escape(num)}</span>(?:(?!</h3>).)*?)(</h3>)',
                   lambda m: m.group(0) if 'class="imp' in m.group(1) else m.group(1) + STAR[lvl] + m.group(2), s, count=1)
    nums = sorted(spec['stars'], key=lambda x: float(x))
    for num, html in spec['after'].items():
        tag = f'{fname}:{num}'
        if f'<!-- ENR:{tag} -->' in s:
            continue
        i = nums.index(num)
        if i + 1 < len(nums):
            anchor = f'<h3><span class="zh-num">{nums[i + 1]}</span>'
            pos = s.index(anchor)
        else:
            pos = s.rindex('<div class="checkpoint">')
        s = s[:pos] + wrap(tag, html) + s[pos:]
    tag = f'{fname}:summary'
    if f'<!-- ENR:{tag} -->' not in s:
        pos = s.rindex('<div class="checkpoint">')
        s = s[:pos] + wrap(tag, spec['summary']) + s[pos:]
    p.write_text(s, encoding='utf-8')
    print('enriched', fname)

for f, spec in [('learn_03.html', CH3), ('learn_04.html', CH4), ('learn_05.html', CH5), ('learn_06.html', CH6), ('learn_07.html', CH7)]:
    apply(f, spec)
