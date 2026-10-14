#!/usr/bin/python3
"""Add the missing step-by-step derivations to Part 2 chapter 2 (learn_02.html).

Covers slides p.4–5 (free space, two-ray), p.12–15 (mean/variance, LS normal equations, outage integral),
p.20–26 (impulse response → baseband → narrowband → I/Q → Rayleigh / exponential), p.31 (coherence bandwidth),
p.42–43 (AFD), p.49–50 (Jensen, outage capacity), p.53–54, 58–59 (water-filling).
Idempotent: every block sits between <!-- DRV:name --> and <!-- /DRV:name -->.
"""
import pathlib, re

B = pathlib.Path(__file__).parent
F = B / 'learn_02.html'

def S(n, html):
    return f'<div class="wstep"><div class="wn">{n}</div><div class="wtext">{html}</div></div>'

BLOCKS = []   # (name, anchor, position 'before'|'after', html)

# ---------------------------------------------------------------- 2.1 free space and two-ray
BLOCKS.append(('fs2ray', '      <div class="formula-card">\n        <div class="flbl">简化路径损耗模型（p.8）—— 必背</div>', 'before', r'''<div class="extra">
        <div class="lbl">课外补充 · 两个公式是怎么推出来的（讲义只给结果）</div>
        <p><b>自由空间（p.4）</b>：</p>
        <ol class="steps">
          <li>全向天线把功率 \(P_t\) 均匀撒到半径 d 的球面上，球面面积 \(4\pi d^2\)，单位面积功率 \(P_t/(4\pi d^2)\)；发射天线增益 \(G_t\) 表示朝接收方向多集中 \(G_t\) 倍。</li>
          <li>接收天线能"接住"的面积叫有效面积 \(A_e=G_r\lambda^2/(4\pi)\)。</li>
          <li>相乘：\(P_r=\dfrac{P_tG_t}{4\pi d^2}\cdot\dfrac{G_r\lambda^2}{4\pi}=P_t\dfrac{G_tG_r\lambda^2}{(4\pi d)^2}\)。所以 \(P_r\propto d^{-2}\)（γ = 2），且 \(\lambda=c/f\) 使 \(P_r\propto f^{-2}\)。</li>
        </ol>
        <p><b>双径（p.5）为什么远处变成 d⁻⁴</b>：</p>
        <ol class="steps">
          <li>直射路径长 l，地面反射路径长 l′。d 远大于天线高度时，两条路程差 \(\Delta l=l'-l\approx\dfrac{2h_th_r}{d}\)。</li>
          <li>路程差造成相位差 \(\Delta\phi=\dfrac{2\pi\Delta l}{\lambda}=\dfrac{4\pi h_th_r}{\lambda d}\)；地面反射系数约为 −1（反相）。</li>
          <li>合成场强 ∝ \(\dfrac{\lambda}{4\pi d}\,\big|1-e^{-j\Delta\phi}\big|\)。d 大到 Δφ 很小时 \(|1-e^{-j\Delta\phi}|\approx\Delta\phi\)，两路几乎抵消，只剩一点差值。</li>
          <li>功率是场强的平方：\(P_r\approx P_tG_tG_r\Big(\dfrac{\lambda}{4\pi d}\Big)^2\Big(\dfrac{4\pi h_th_r}{\lambda d}\Big)^2=P_tG_tG_r\dfrac{(h_th_r)^2}{d^4}\)，和讲义一致。λ 消掉了，所以远处的双径损耗<b>和频率无关</b>。</li>
          <li>临界距离 \(d_c=4h_th_r/\lambda\) 就是 Δφ = π 的位置：比它近，两路时而相加时而抵消（随距离起伏）；比它远，按 d⁻⁴ 单调下降。</li>
        </ol>
      </div>
      '''))

# ---------------------------------------------------------------- 2.1 LS normal equations
BLOCKS.append(('lsderiv', '      <div class="worked">\n        <summary><span class="wtag">例题</span>Practice 1 第 1 题：六个测量点</summary>', 'before', r'''<div class="worked">
        <summary><span class="wtag">推导</span>最小二乘的两个方程（p.13 的"最小化 MSE"具体怎么做）</summary>
        <div class="wbody">
          <p>记 \(x_i=10\log_{10}(d_i/d_0)\)，模型 \(\hat M_i=K-\gamma x_i\)，误差 \(e_i=M_i-K+\gamma x_i\)，要让 \(F=\frac1n\sum e_i^2\) 最小。</p>
          ''' + S(1, r'对 K 求偏导：\(\dfrac{\partial F}{\partial K}=-\dfrac2n\sum_i(M_i-K+\gamma x_i)=0\ \Rightarrow\ nK-\gamma\sum x_i=\sum M_i\)。') + S(2, r'对 γ 求偏导：\(\dfrac{\partial F}{\partial\gamma}=\dfrac2n\sum_i x_i(M_i-K+\gamma x_i)=0\ \Rightarrow\ K\sum x_i-\gamma\sum x_i^2=\sum x_iM_i\)。') + S(3, r'两个一次方程、两个未知数（K、γ），代入 \(\sum x_i,\ \sum x_i^2,\ \sum M_i,\ \sum x_iM_i\) 四个和直接解。第一个方程也说明：<b>最佳直线一定经过数据的平均点</b> \((\bar x,\bar M)\)。') + S(4, r'解出 K、γ 后，把它们代回去算 \(F_{\min}=\frac1n\sum e_i^2\)，这就是阴影方差 \(\sigma_\psi^2\)（p.13："MSE = \(\sigma_{\psi_{dB}}^2\)"）。') + r'''
          <div class="wans">考试手算时：先列 x、M、x²、xM 四列，求和，代进两个方程</div>
        </div>
      </div>
      '''))

# ---------------------------------------------------------------- 2.2 mean / variance and outage integral
BLOCKS.append(('meanvar', '      <p><b>中断概率怎么推出来</b>（p.14–15）', 'before', r'''<p><b>均值和方差</b>（p.12）：上式里 \(K_{\mathrm{dB}}-10\gamma\log_{10}(d/d_0)\) 是常数，\(\psi_{\mathrm{dB}}\) 是均值 0、方差 \(\sigma_\psi^2\) 的高斯。用第 1 章"加常数只挪位置、不改变方差"：</p>
      <div class="calc">E[P<sub>r,dB</sub> − P<sub>t,dB</sub>] = K<sub>dB</sub> − 10γ log₁₀(d/d₀) + E[ψ<sub>dB</sub>] = K<sub>dB</sub> − 10γ log₁₀(d/d₀)</div>
      <div class="calc">Var[P<sub>r,dB</sub> − P<sub>t,dB</sub>] = Var[ψ<sub>dB</sub>] = σ<sub>ψ</sub>²</div>
      <p>所以接收功率（dB）服从 \(\mathcal N\big(\text{平均路径损耗结果},\ \sigma_\psi^2\big)\)。</p>
      '''))
BLOCKS.append(('outint', '      <div class="formula-card">\n        <div class="flbl">中断概率（p.15）—— 必背</div>', 'before', r'''<div class="worked">
        <summary><span class="wtag">推导</span>讲义 p.15 的积分一步一步</summary>
        <div class="wbody">
          ''' + S(1, r'ψ 的概率密度是 \(\frac{1}{\sqrt{2\pi}\sigma}e^{-\psi^2/2\sigma^2}\)（σ 是 \(\sigma_{\psi_{dB}}\)）。中断 = ψ &lt; −x：<div class="calc">P_out = ∫<sub>−∞</sub><sup>−x</sup> (1/(√(2π)σ)) e^(−ψ²/2σ²) dψ</div>') + S(2, r'高斯曲线左右对称，左尾 (−∞, −x) 的面积等于右尾 (x, ∞) 的面积：<div class="calc">P_out = ∫<sub>x</sub><sup>∞</sup> (1/(√(2π)σ)) e^(−ψ²/2σ²) dψ</div>') + S(3, r'换元 u = ψ/σ，dψ = σ du，下限 ψ = x 变成 u = x/σ，σ 正好约掉：<div class="calc">P_out = ∫<sub>x/σ</sub><sup>∞</sup> (1/√(2π)) e^(−u²/2) du = Q(x/σ)</div>') + r'''
          <div class="wans">换元除掉的是 σ（标准差），这就是 Q 里一定除标准差的原因</div>
        </div>
      </div>
      '''))

# ---------------------------------------------------------------- 2.3 impulse response → I/Q → Rayleigh
IQ = r'''<h4>从冲激响应到 I/Q 分量（p.20–24）：瑞利分布的来历</h4>
      <p>讲义 p.22–24 用四步把"很多条回波"变成"两个高斯随机变量"，这是瑞利分布、莱斯分布、第 4 章分集、第 5 章 MIMO 的共同起点。</p>
      <p><b>第一步：收到的信号 = 冲激响应和发送信号的卷积</b>（p.22）。冲激响应是一串延迟、加权的冲激，和冲激卷积就是"延迟再加权"，所以收到的是 N 份延迟、缩放、转了相位的发送信号之和：\(r(t)=c(\tau,t)*s(t)\)。</p>
      <p><b>第二步：用基带等效表示发送信号</b>。无线信号是把信息 u(t) 搬到载波 \(f_c\) 上发出去的：</p>
      <div class="formula-card">
        <div class="flbl">基带等效（p.22）</div>
        <div class="fexpr">\(s(t)=\mathrm{Re}\{u(t)\,e^{j2\pi f_ct}\}\)　　\(r(t)=\mathrm{Re}\Big\{\Big[\displaystyle\sum_{n=1}^{N}\alpha_n(t)e^{-j\phi_n(t)}u(t-\tau_n(t))\Big]e^{j2\pi f_ct}\Big\}\)</div>
        <div class="fmeaning">u(t) 叫<b>复基带信号</b>，装着信息，变化慢；\(e^{j2\pi f_ct}=\cos2\pi f_ct+j\sin2\pi f_ct\) 是载波，变化极快。Re{·} 取实部，因为天线上发的是实信号。u(t) = 1 时 \(s(t)=\cos2\pi f_ct\)，就是一个纯载波。每条回波的相位 \(\phi_n\) 里包含了路程造成的 \(2\pi f_c\tau_n\) 和多普勒造成的相位变化。</div>
      </div>
      <p><b>第三步：窄带假设</b>（p.23）。如果时延扩展远小于信号带宽的倒数（符号很长），各条回波晚到的那一点时间对 u(t) 几乎没有影响：\(u(t-\tau_n)\approx u(t)\)。于是 u(t) 可以提到求和外面：</p>
      <div class="formula-card">
        <div class="flbl">窄带衰落模型（p.23）</div>
        <div class="fexpr">\(r(t)\approx\mathrm{Re}\Big\{\underbrace{\Big[\displaystyle\sum_{n}\alpha_n(t)e^{-j\phi_n(t)}\Big]}_{\text{复数缩放因子}}\,u(t)\,e^{j2\pi f_ct}\Big\}\)</div>
        <div class="fmeaning"><mark class="hl">多径只是把信号乘上了一个随机的复数</mark>：波形不变形（没有 ISI），只是幅度被缩放、相位被转动。这正是"平坦衰落"。把 u(t) 取成 1，剩下的复数缩放因子就是 r(t) 的基带等效。</div>
      </div>
      <p><b>第四步：拆成同相（I）和正交（Q）分量</b>（p.24）。把 \(e^{j2\pi f_ct}=\cos+j\sin\) 代进去取实部，r(t) 变成两个载波的叠加：</p>
      <div class="formula-card">
        <div class="flbl">I/Q 分量（p.24）—— 必懂</div>
        <div class="fexpr">\(r(t)=r_I(t)\cos2\pi f_ct-r_Q(t)\sin2\pi f_ct\)<br>\(r_I(t)=\displaystyle\sum_{n}\alpha_n(t)\cos\phi_n(t)\)　　\(r_Q(t)=\displaystyle\sum_{n}\alpha_n(t)\sin\phi_n(t)\)</div>
        <div class="fmeaning">cos 和 sin 是两个相差 90° 的载波，互相正交，可以各自携带一个独立的数。\(r_I\)（In-phase，同相分量）是和 cos 载波同相的那一部分的幅度，\(r_Q\)（Quadrature，正交分量）是和 sin 载波那一部分的幅度。把它们当作平面坐标 \((r_I, r_Q)\)，就是本节后面瑞利图①里合成箭头终点的横坐标和纵坐标：<b>每条回波贡献一个小箭头 \(\alpha_n(\cos\phi_n,\sin\phi_n)\)，\(r_I\)、\(r_Q\) 是所有小箭头 x、y 分量之和</b>。</div>
      </div>
      <div class="worked">
        <summary><span class="wtag">推导</span>为什么 \(r_I\)、\(r_Q\) 是零均值、独立的高斯（p.24 的三句话）</summary>
        <div class="wbody">
          ''' + S(1, r'<b>高斯</b>：\(r_I=\sum\alpha_n\cos\phi_n\) 是 N 个随机量之和，N 很大时由中心极限定理趋于高斯；\(r_Q\) 同理，而且两者<b>联合</b>高斯。') + S(2, r'<b>零均值</b>：均匀散射时 \(\phi_n\) 在 [0, 2π) 上均匀分布，与 \(\alpha_n\) 独立。\(E[\cos\phi_n]=\frac{1}{2\pi}\int_0^{2\pi}\cos\phi\,d\phi=0\)，所以 \(E[r_I]=\sum E[\alpha_n]E[\cos\phi_n]=0\)，\(E[r_Q]=0\) 同理。') + S(3, r'<b>方差</b>：\(E[\cos^2\phi_n]=\frac12\)，不同回波相互独立，交叉项均值为 0，所以 \(\mathrm{Var}(r_I)=\sum E[\alpha_n^2]\cdot\frac12=\sigma^2\)，\(\mathrm{Var}(r_Q)=\sigma^2\)，一样大。总平均功率 \(E[r_I^2+r_Q^2]=\sum E[\alpha_n^2]=2\sigma^2\)，这就是 p.25 说"2σ² 是平均接收功率"的原因。') + S(4, r'<b>独立</b>：\(E[r_Ir_Q]=\sum E[\alpha_n^2]E[\cos\phi_n\sin\phi_n]=\sum E[\alpha_n^2]\cdot\frac12E[\sin2\phi_n]=0\)，不相关。<b>联合高斯的变量不相关就等于独立</b>。') + r'''
          <div class="wans">r<sub>I</sub>, r<sub>Q</sub> ~ N(0, σ²)，相互独立；平均功率 2σ²</div>
        </div>
      </div>
      <div class="extra">
        <div class="lbl">课外补充 · 接收机怎么把 r<sub>I</sub>、r<sub>Q</sub> 取出来</div>
        <p>把 r(t) 乘以 2cos2πf<sub>c</sub>t：\(2r_I\cos^2-2r_Q\sin\cos=r_I(1+\cos4\pi f_ct)-r_Q\sin4\pi f_ct\)。再过低通滤波器去掉 2f<sub>c</sub> 的高频项，只剩 \(r_I\)。乘以 −2sin2πf<sub>c</sub>t 再低通，得到 \(r_Q\)。这就是"I/Q 解调"，所有数字接收机的第一步。</p>
        <p>符号约定提醒：讲义 p.22 的冲激响应写的是 \(e^{-j\phi_n}\)，p.24 的 \(r_Q=\sum\alpha_n\sin\phi_n\) 对应 \(e^{+j\phi_n}\) 的写法，两页差一个正负号。φ<sub>n</sub> 均匀分布时 sin φ 和 −sin φ 的统计性质完全一样，所以不影响任何结论，考试按 p.24 写即可。</p>
      </div>
      <p>有了两个独立的 \(\mathcal N(0,\sigma^2)\)，包络和功率的分布就是纯数学了：</p>
      <div class="worked">
        <summary><span class="wtag">推导</span>从 \(r_I,r_Q\) 到瑞利分布、指数分布（p.25–26 的结果怎么来的）</summary>
        <div class="wbody">
          ''' + S(1, r'<b>联合 PDF</b>：独立 → 相乘（第 1 章 p.14）：\(p(r_I,r_Q)=\frac{1}{2\pi\sigma^2}e^{-(r_I^2+r_Q^2)/2\sigma^2}\)。它只和 \(r_I^2+r_Q^2\)（离原点的距离）有关，是一个"圆对称"的钟。') + S(2, r'<b>换成极坐标</b>：\(r_I=z\cos\theta,\ r_Q=z\sin\theta\)，面积元 \(dr_I\,dr_Q=z\,dz\,d\theta\)（多出的 z 是雅可比行列式：离原点越远，同样 dz、dθ 围出的面积越大）：<div class="calc">p(z, θ) = (z/(2πσ²)) e^(−z²/2σ²)</div>') + S(3, r'<b>对 θ 积分</b>（θ 从 0 到 2π，被积函数和 θ 无关，乘 2π）：<div class="calc">p(z) = (z/σ²) e^(−z²/2σ²)，z ≥ 0　← 瑞利（p.25）</div>同时得到相位 θ 在 [0, 2π) 上均匀分布。') + S(4, r'<b>CDF</b>：\(P(z\lt Z)=\int_0^Z\frac{z}{\sigma^2}e^{-z^2/2\sigma^2}dz=1-e^{-Z^2/2\sigma^2}\)。因为 \(Z_{\mathrm{rms}}^2=E[z^2]=2\sigma^2\)，令 \(\rho=Z/Z_{\mathrm{rms}}\) 就得到 <mark class="hl">\(P(z\lt Z_{\min})=1-e^{-\rho^2}\)</mark>，2.6 节 AFD 公式里用的就是它。') + S(5, r'<b>功率是指数分布</b>：令 w = z²，则 dw = 2z dz，\(p_w(w)=\frac{p_z(\sqrt w)}{2\sqrt w}=\frac{1}{2\sigma^2}e^{-w/2\sigma^2}\)（p.26）。SNR γ 只是功率除以噪声功率，形状不变，均值换成 \(\bar\gamma\)：\(p(\gamma)=\frac{1}{\bar\gamma}e^{-\gamma/\bar\gamma}\)。') + r'''
          <div class="wans">两个独立零均值高斯 → 极坐标 → 包络瑞利、相位均匀、功率指数</div>
        </div>
      </div>
      '''
BLOCKS.append(('iq', '      <!-- DRVSLOT:iq -->', 'before', IQ))

# ---------------------------------------------------------------- 2.4 coherence bandwidth definition
BLOCKS.append(('bc', '      <p>时延扩展在频域的对应量是<b>相干带宽</b>', 'before', r'''<div class="formula-card">
        <div class="flbl">相干带宽的定义（p.31）</div>
        <div class="fexpr">\(P_r(\Delta f)=\mathcal F\{P_r(\tau)\}\)；\(B_C\) = 使 \(P_r(\Delta f)\approx0\) 的最小频率间隔 Δf</div>
        <div class="fmeaning">对功率时延分布做傅里叶变换，得到"两个相隔 Δf 的频率，衰落有多相关"。相关性降到约 0 时的 Δf 就是相干带宽。时延分布越宽，它的傅里叶变换越窄（时域宽 ↔ 频域窄），所以 <mark class="hl">时延扩展越大，相干带宽越小，\(B_C\propto1/\sigma_{T_m}\)</mark>。讲义没有给具体比例系数，判断平坦/选择性用 p.33 的 σ<sub>Tm</sub>/T<sub>s</sub> &lt; 0.1。</div>
      </div>
      '''))

# ---------------------------------------------------------------- 2.6 AFD derivation
BLOCKS.append(('afd', '      <div class="key">\n        <div class="lbl">★ 考试重点 · 数错误的两个公式</div>', 'before', r'''<div class="worked">
        <summary><span class="wtag">推导</span>AFD 公式是怎么来的（p.42–43）</summary>
        <div class="wbody">
          ''' + S(1, r'观察 T 秒。第 i 次衰落持续 \(\tau_i\) 秒，总共 \(L_Z T\) 次（LCR 乘时间）。平均每次多久：<div class="calc">τ̄ = Στ<sub>i</sub> / (L<sub>Z</sub>T)</div>') + S(2, r'\(\sum\tau_i/T\) 是"T 秒里有多大比例的时间信号在门限以下"，T 很长时就是概率 \(P(z\lt Z_{\min})\)：<div class="calc">τ̄ = P(z &lt; Z<sub>min</sub>) / L<sub>Z</sub></div>这一步对任何衰落都成立。') + S(3, r'代入瑞利的 \(P(z\lt Z_{\min})=1-e^{-\rho^2}\)（2.3 节推导第 4 步）和 \(L_Z=\sqrt{2\pi}f_m\rho e^{-\rho^2}\)：<div class="calc">τ̄ = (1 − e^(−ρ²)) / (√(2π) f<sub>m</sub> ρ e^(−ρ²)) = (e^(ρ²) − 1) / (√(2π) f<sub>m</sub> ρ)</div>分子分母同乘 \(e^{\rho^2}\) 就是讲义的形式。') + r'''
          <div class="wans">AFD = 低于门限的时间比例 ÷ LCR；LCR 的公式讲义直接给出，不要求推导</div>
        </div>
      </div>
      '''))

# ---------------------------------------------------------------- 2.7 Jensen and outage capacity
BLOCKS.append(('jensen', '      <div class="formula-card">\n        <div class="flbl">瑞利衰落的衰落余量（p.51）—— 必背</div>', 'before', r'''<div class="extra">
        <div class="lbl">课外补充 · 两种容量的推导细节</div>
        <p><b>Jensen 不等式</b>（p.49）：log 是"凹"函数（向下弯），弯曲的函数先平均再取值，和先取值再平均不一样。凹函数满足 \(E[f(X)]\le f(E[X])\)。取 \(f(\gamma)=B\log_2(1+\gamma)\)：<span class="calc">E[B log₂(1+γ)] ≤ B log₂(1+E[γ]) = B log₂(1+γ̄)</span>。直观：SNR 时高时低，低的时候损失的容量比高的时候多赚的多，所以平均下来吃亏。</p>
        <p><b>中断容量</b>（p.50）：要求只有 ε 的时间不够用，就要找门限 γ<sub>min</sub> 使 \(P(\gamma\lt\gamma_{\min})=\varepsilon\)，即 \(F(\gamma_{\min})=\varepsilon\)，反过来 \(\gamma_{\min}=F^{-1}(\varepsilon)\)（F 是 CDF，F⁻¹ 是它的反函数，"已知概率求门限"）。按这个 γ<sub>min</sub> 设计速率 \(C_\varepsilon=B\log_2(1+\gamma_{\min})\)，1 − ε 的时间能无错传输，平均无错速率 \((1-\varepsilon)C_\varepsilon\)。瑞利信道 \(F(\gamma)=1-e^{-\gamma/\bar\gamma}\)，解 \(1-e^{-\gamma_{\min}/\bar\gamma}=\varepsilon\) 得 \(\gamma_{\min}=\bar\gamma\ln\frac{1}{1-\varepsilon}\)。</p>
      </div>
      '''))

# ---------------------------------------------------------------- 2.8 water-filling Lagrange + time-varying
BLOCKS.append(('wf', '      <div class="key">\n        <div class="lbl">★ 考试重点 · 注水三步</div>', 'before', r'''<div class="extra">
        <div class="lbl">课外补充 · 注水公式的推导（讲义说 γ₀ 是拉格朗日乘子，p.54）</div>
        <ol class="steps">
          <li>目标：在 \(\sum P_j=P\) 的约束下最大化 \(\sum B\log_2\!\big(1+\gamma_jP_j/P\big)\)（\(\gamma_j\) 是全部功率给第 j 个子信道时的 SNR）。</li>
          <li>拉格朗日函数 \(\mathcal L=\sum\ln(1+\gamma_jP_j/P)-\lambda\sum P_j\)，对 \(P_j\) 求导令其为 0：\(\dfrac{\gamma_j/P}{1+\gamma_jP_j/P}=\lambda\)。</li>
          <li>整理：\(\dfrac{P_j}{P}=\dfrac{1}{\lambda P}-\dfrac{1}{\gamma_j}\)。记 \(\gamma_0=\lambda P\)，就是 \(\dfrac{P_j}{P}=\dfrac1{\gamma_0}-\dfrac1{\gamma_j}\)。</li>
          <li>功率不能为负，右边小于 0 时只能取 0，这就是"γ<sub>j</sub> &lt; γ<sub>0</sub> 不分功率"。</li>
          <li>代回容量：\(\log_2(1+\gamma_jP_j/P)=\log_2\big(1+\gamma_j/\gamma_0-1\big)=\log_2(\gamma_j/\gamma_0)\)，所以 \(C=\sum_{\gamma_j\ge\gamma_0}B_j\log_2(\gamma_j/\gamma_0)\)。</li>
        </ol>
        <p><b>时变的频率选择性信道</b>（p.58–59）：每个子带的 γ<sub>j</sub> 不再是常数而是随机的，有自己的 PDF。做法相同，只是把"对 j 求和"换成"对 j 求和 + 对 γ<sub>j</sub> 的分布积分"：\(C=\sum_j\int_{\gamma_0}^\infty B_c\log_2(\gamma_j/\gamma_0)p(\gamma_j)d\gamma_j\)，γ₀ 由 \(\sum_j\int_{\gamma_0}^\infty(1/\gamma_0-1/\gamma_j)p(\gamma_j)d\gamma_j=1\) 定出。讲义没有出这类计算题。</p>
      </div>
      '''))

def apply():
    s = F.read_text(encoding='utf-8')
    for name, anchor, pos, html in BLOCKS:
        s = re.sub(rf'<!-- DRV:{name} -->.*?<!-- /DRV:{name} -->\n', '', s, flags=re.S)
    for name, anchor, pos, html in BLOCKS:
        block = f'<!-- DRV:{name} -->\n      {html}<!-- /DRV:{name} -->\n'
        i = s.find(anchor)
        if i < 0:
            raise SystemExit(f'anchor for {name} not found')
        if pos == 'before':
            s = s[:i] + block + s[i:]
    F.write_text(s, encoding='utf-8')
    print('derivations added:', len(BLOCKS))

apply()
