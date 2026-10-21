#!/usr/bin/python3
"""More learning-page boxes for extra_notes.py: dB line, least squares, fade margin, water-filling,
which outage formula (10 cases with examples), rounding habits. Numbers: verify_notes.py."""

MORE = [
 ('learn_02.html', ('after_p', '<p><b>怎么从左边的式子得到右边</b>'), 'dbline', r'''      <div class="extra">
        <div class="lbl">课外补充 · 为什么 dB 形式是一条直线：M = K<sub>dB</sub> − γx 的推导</div>
        <p>起点是必背的简化路径损耗模型。两边除以 \(P_t\)，得到表里实测的那个比值：\(P_r/P_t=K\,(d_0/d)^{\gamma}\)。记 \(M=(P_r/P_t)_{dB}=10\log_{10}(P_r/P_t)\)。</p>
        <div class="tblwrap"><table><thead><tr><th>对数规则</th><th>作用</th></tr></thead><tbody>
          <tr><td>log(a·b) = log a + log b</td><td>乘法变加法</td></tr>
          <tr><td>log(aⁿ) = n·log a</td><td>指数变成系数</td></tr>
          <tr><td>log(1/a) = −log a</td><td>倒数变成负号</td></tr>
        </tbody></table></div>
        <ol class="steps">
          <li>两边取 \(10\log_{10}\)：\(M=10\log_{10}\big[K(d_0/d)^{\gamma}\big]\)。</li>
          <li>乘法变加法：\(M=10\log_{10}K+10\log_{10}(d_0/d)^{\gamma}\)。</li>
          <li>指数提到前面：\(M=K_{dB}+\gamma\cdot10\log_{10}(d_0/d)\)。</li>
          <li>倒数变负号：\(M=K_{dB}-\gamma\cdot10\log_{10}(d/d_0)\)。</li>
          <li>令 \(d_0=1\) m、\(x=10\log_{10}d\)：\(M=K_{dB}-\gamma x\)。</li>
        </ol>
        <div class="tblwrap"><table><thead><tr><th>直线 y = b + kx</th><th>路径损耗</th></tr></thead><tbody>
          <tr><td>纵坐标 y</td><td>M = (P<sub>r</sub>/P<sub>t</sub>)<sub>dB</sub></td></tr>
          <tr><td>横坐标 x</td><td>10 log₁₀d</td></tr>
          <tr><td>截距 b</td><td>K<sub>dB</sub>：x = 0，也就是 d = 1 m 时的增益</td></tr>
          <tr><td>斜率 k</td><td>−γ</td></tr>
        </tbody></table></div>
        <p><b>为什么横坐标用 10 log₁₀d，不用 log₁₀d：</b>这样斜率正好是 −γ。用 log₁₀d 当横坐标，式子变成 \(M=K_{dB}-10\gamma\log_{10}d\)，斜率是 −10γ，把它直接当 γ 就会大 10 倍。</p>
        <p><b>代数验证</b>（练习页模拟 B · Q2 的拟合结果 K<sub>dB</sub> = −37.0 dB、γ = 3.37）：d = 100 m 时 x = 20，\(M=-37.0-3.37\times20=-104.3\) dB；实测 −105 dB，差的 −0.7 dB 就是这个点的阴影（残差）。</p>
        <p><b>为什么要写成直线：</b>原式里 K 乘在外面、γ 在指数上，不好直接求；取 dB 后变成直线，就能用最小二乘求斜率和截距，点偏离直线的程度就是阴影。</p>
      </div>
'''),
 ('learn_02.html', ('after', '<!-- /DRV:lsderiv -->'), 'lsq', r'''      <div class="extra">
        <div class="lbl">课外补充 · 最小二乘的另一种写法：直线过平均点，斜率 = 协方差 / 方差</div>
        <p>上面的推导框解出的是"四列求和"的形式。把同样的两个方程换个写法，结果更好记，手算也更快。</p>
        <p><b>要最小化什么：</b>第 i 个点的残差 \(e_i=M_i-(K-\gamma x_i)\)，让 \(F=\sum e_i^2\) 最小（讲义再除以 n，最小值的位置不变）。用平方是因为：残差有正有负，直接相加会抵消；平方可以求导；最后剩下的平均平方误差正好就是阴影方差 \(\sigma_\psi^2\)。</p>
        <ol class="steps">
          <li>F 是 K、γ 的二次函数，像一个碗，碗底两个方向的斜率都为 0：\(\partial F/\partial K=0\)、\(\partial F/\partial\gamma=0\)。用链式法则得到两个正规方程：① \(\sum(M_i-K+\gamma x_i)=0\)；② \(\sum x_i(M_i-K+\gamma x_i)=0\)。</li>
          <li>① 除以 n：\(\bar M-K+\gamma\bar x=0\ \Rightarrow\ K=\bar M+\gamma\bar x\)。<b>最佳直线一定经过平均点</b> \((\bar x,\bar M)\)；① 本身还说明<b>残差之和为 0</b>，可以用来检查算没算错。</li>
          <li>把 K 代入 ② 的括号：\(M_i-K+\gamma x_i=(M_i-\bar M)+\gamma(x_i-\bar x)\)。前面的 \(x_i\) 可以换成 \(x_i-\bar x\)（多减掉的部分是 \(\bar x\) 乘以偏差之和，等于 0），得到 \(\sum(x_i-\bar x)(M_i-\bar M)+\gamma\sum(x_i-\bar x)^2=0\)。</li>
          <li>解出 \(\gamma=-\dfrac{\sum(x_i-\bar x)(M_i-\bar M)}{\sum(x_i-\bar x)^2}\)。分式本身就是直线的斜率，模型里斜率是 −γ，所以 γ 取它的相反数。</li>
        </ol>
        <p><b>直观理解：</b>K = M̄ + γx̄ 说明直线穿过所有点的"重心"；斜率 = 协方差 / 方差，分子是 x 和 M 一起变化的程度，分母是 x 自己散开的程度，x 每增加 1，M 平均变化多少就是斜率。</p>
        <p><b>手算列表：</b>d、x = 10 log₁₀d、x − x̄、M − M̄、(x − x̄)(M − M̄)、(x − x̄)²。例（练习页模拟 B · Q2）：x̄ = 15、M̄ = −87.5，Σ(x − x̄)(M − M̄) = −194.95，Σ(x − x̄)² = 57.92，斜率 −3.37 → γ = 3.37，K<sub>dB</sub> = −87.5 + 3.37 × 15 = −37.0 dB；残差 +2.67、−5.20、+3.20、−0.67，加起来为 0。</p>
        <p><b>考试要求：</b>讲义 p.13 写出 F 并说"令两个偏导为 0"，一般不会让你从头推。记住三点：直线过平均点；斜率 = Σ(x − x̄)(M − M̄)/Σ(x − x̄)²；γ 取斜率的负号。</p>
      </div>
'''),
 ('learn_02.html', ('card', '瑞利衰落的衰落余量'), 'fm', r'''      <div class="extra">
        <div class="lbl">课外补充 · 衰落余量公式怎么记：从瑞利中断反解</div>
        <p>不用死记，它就是把必背的瑞利中断公式 \(\varepsilon=1-e^{-\gamma_0/\bar\gamma}\) 反过来解，两步：</p>
        <ol class="steps">
          <li>解出比值：\(e^{-\gamma_0/\bar\gamma}=1-\varepsilon\ \Rightarrow\ \gamma_0/\bar\gamma=\ln\frac{1}{1-\varepsilon}\)。</li>
          <li>倒过来取 dB：\(\bar\gamma/\gamma_0=1/\ln\frac{1}{1-\varepsilon}\)，所以 \(\text{FM}=10\log_{10}\Big[1\Big/\ln\frac{1}{1-\varepsilon}\Big]\) dB。</li>
        </ol>
        <p>ε 很小时 \(\ln\frac{1}{1-\varepsilon}\approx\varepsilon\)，于是 \(\text{FM}\approx10\log_{10}(1/\varepsilon)\)。<b>口诀：中断要求每严 10 倍，余量多 10 dB；1% → 20 dB。</b></p>
        <div class="tblwrap"><table><thead><tr><th>ε</th><th>1/ε</th><th>FM 近似</th><th>FM 精确</th></tr></thead><tbody>
          <tr><td>10%</td><td>10</td><td>10 dB</td><td>9.8 dB</td></tr>
          <tr><td>1%</td><td>100</td><td>20 dB</td><td>20.0 dB</td></tr>
          <tr><td>0.5%</td><td>200</td><td>23 dB</td><td>23.0 dB</td></tr>
          <tr><td>0.1%</td><td>1000</td><td>30 dB</td><td>30.0 dB</td></tr>
        </tbody></table></div>
        <p><b>直观：</b>瑞利衰落下 SNR 低于平均值 1/k 的概率约为 1/k（因为 \(1-e^{-x}\approx x\)）。想让 SNR 只有 1% 的时间低于门限，门限就得是平均值的 1/100，即平均值要高 100 倍（20 dB）。</p>
        <p><b>例</b>（练习页模拟 B · Q1）：门限 7 dB、中断 1%，FM = 10 log₁₀(1/0.01005) = 19.98 ≈ 20 dB，所需平均 SNR = 7 + 20 = 27 dB。易错：FM 是两个 dB 值相减；ln 是自然对数。</p>
      </div>
'''),
 ('learn_02.html', ('card', '注水法（p.54）'), 'wf', r'''      <div class="extra">
        <div class="lbl">课外补充 · 注水法是什么：往高低不平的水池里倒水</div>
        <p><b>它回答的问题：</b>有几条好坏不一的并行子信道，总功率固定，怎样分配功率才能让总容量最大。</p>
        <p><b>比喻：</b>每条子信道是水池的一格，<b>池底高度 = 1/γ<sub>j</sub></b>：信道越好池底越低。把总功率当一桶水倒进去，水流到低处，形成平的水面 1/γ₀。每格分到的功率 = 水面 − 池底：好信道多给，差信道少给，池底高过水面的信道一点都不给。</p>
        <ol class="steps">
          <li>先假设 n 条都分到功率，由 \(\sum(1/\gamma_0-1/\gamma_j)=1\) 解出 \(n/\gamma_0=1+\sum 1/\gamma_j\)。</li>
          <li>检查每条 \(\gamma_j\ge\gamma_0\)。有不满足的，去掉最差的那条（n 减 1），重新解 γ₀，再检查。</li>
          <li>功率 \(P_j/P=1/\gamma_0-1/\gamma_j\)，容量 \(C=\sum B_j\log_2(\gamma_j/\gamma_0)\)（只对分到功率的求和）。</li>
        </ol>
        <p><b>例 1（Practice 5 第 1 题，三条都分）：</b>SNR 80、40、40，B = 10 MHz。\(3/\gamma_0=1+1/80+1/40+1/40=1.0625\)，γ₀ = 2.82，都大于 2.82。功率 0.342、0.329、0.329；C = 10 MHz × [log₂(80/2.82) + 2 log₂(40/2.82)] ≈ 124.7 Mbps。</p>
        <p><b>例 2（模拟 B · Q3，最差的被放弃）：</b>SNR 20、0.5，各 1 MHz。先假设都分：2/γ₀ = 1 + 1/20 + 1/0.5 = 3.05，γ₀ = 0.656 &gt; 0.5，第 2 条放弃；只剩一条：1/γ₀ = 1.05，P₁ = P，C = log₂(20/0.952) = log₂21 = 4.39 Mbps。平分功率时只有 log₂11 + log₂1.25 = 3.78 Mbps。</p>
        <p><b>为什么这样分最优：</b>容量是 log₂(1 + SNR)，增长越来越慢。差信道多给功率也抬不起 SNR，收益小；好信道每单位功率收益更高，但一直加也会递减。最后"水面持平"，就是每条信道最后一点功率的收益相等（讲义说 γ₀ 来自拉格朗日乘子，严格推导不考）。</p>
        <p><b>易错：</b>γ<sub>j</sub> 用线性值；一定要检查 γ<sub>j</sub> ≥ γ₀，否则会算出负功率；容量是 log₂(γ<sub>j</sub>/γ₀)，不是 log₂(1 + γ<sub>j</sub>)；去掉子信道后 n 要跟着改。发射端必须知道信道（informed transmitter）才能这样分；第 5 章 MIMO（P5 Q1）、第 7 章 OFDM（P7 Q1 (d)）都用它。</p>
      </div>
'''),
 ('learn_02.html', ('before_key', '★ 第二章 Quiz 清单'), 'outage', r'''      <div class="extra">
        <div class="lbl">课外补充 · 求"中断概率"用哪个公式：先认随机性从哪来</div>
        <div class="tblwrap"><table><thead><tr><th>题目特征（关键词）</th><th>用什么</th><th>范围</th></tr></thead><tbody>
          <tr><td>只有路径损耗，没有 σ、没有 shadowing / fading</td><td>直接算功率，和门限比较（没有概率）</td><td>Quiz</td></tr>
          <tr><td>shadowing、log-normal、给了 σ（dB）、"path loss alone … dB above"</td><td>\(Q(\text{余量}/\sigma)\)，在 dB 上相减</td><td>Quiz</td></tr>
          <tr><td>Rayleigh fading、给了平均 SNR、没有 σ</td><td>\(1-e^{-\gamma_0/\bar\gamma}\)，在线性上相除</td><td>Quiz</td></tr>
          <tr><td>两个基站 / 多条独立链路，"both fall below"</td><td>各自的概率相乘</td><td>Quiz（P2 Q2 (b)）</td></tr>
          <tr><td>链路有共同阴影（相关）</td><td>先固定共同变量 → 相乘 → 对它的 PDF 积分</td><td>Quiz（P2 Q2 (c)，考思路）</td></tr>
          <tr><td>SNR 只取几个值，"with a probability of …"</td><td>低于门限的那些取值的概率相加</td><td>Quiz</td></tr>
          <tr><td>给了 ρ、LCR、AFD，问低于门限的时间比例</td><td>\(L_Z\bar\tau_Z=1-e^{-\rho^2}\)</td><td>Quiz</td></tr>
          <tr><td>Rician、给了 K</td><td>只做定性判断（公式考试给）</td><td>Quiz（懂含义）</td></tr>
          <tr><td>"误码率超过 … 就算中断"</td><td>先由误码率反求 γ₀，再用上面的公式</td><td>期末（第 3 章）</td></tr>
          <tr><td>M 条支路选择分集</td><td>\((1-e^{-\gamma_0/\bar\gamma})^M\)</td><td>期末（第 4 章）</td></tr>
        </tbody></table></div>
        <p><b>判断流程：</b>没有随机 → 直接比较；阴影 → Q；瑞利 → 指数；离散 → 概率求和；多条独立链路 → 相乘；有共享部分 → 先条件化再积分。阴影和瑞利最容易混：同样"平均比门限高 8 dB"，阴影（σ = 3.35 dB）下中断 0.84%，瑞利下是 \(1-e^{-0.158}\approx14.7\%\)，瑞利的坑深得多。</p>
      </div>
      <div class="worked">
        <summary><span class="wtag">例题</span>10 种情况各举一例（数字已用脚本验算）</summary>
        <div class="wbody">
          <div class="wstep"><div class="wn">1</div><div class="wtext"><b>只有路径损耗。</b>P<sub>t</sub> = 20 dBm，K<sub>dB</sub> = −31.5 dB，γ = 3.6，门限 −110 dBm。300 m 处 <div class="calc">P_r = 20 − 31.5 − 36 log₁₀300 = −100.68 dBm &gt; −110 dBm → 能通信</div>最远距离：36 log₁₀d ≤ 98.5 → d ≤ 545 m。没有随机量，所以没有"概率"，只有够或不够。</div></div>
          <div class="wstep"><div class="wn">2</div><div class="wtext"><b>阴影（Practice 1 第 2 题 (a)）。</b>平均 15 dBm，门限 10 dBm，σ = 8 dB。余量 5 dB：<div class="calc">P_out = Q(5/8) = Q(0.625) = 0.266</div></div></div>
          <div class="wstep"><div class="wn">3</div><div class="wtext"><b>瑞利。</b>平均 SNR 20 dB（100），门限 10 dB（10）：<div class="calc">P_out = 1 − e^(−10/100) = 1 − e^(−0.1) = 0.0952</div>先换线性值再相除，不能把 dB 代进指数。</div></div>
          <div class="wstep"><div class="wn">4</div><div class="wtext"><b>宏分集，阴影独立（P2 Q2 (b)）。</b>余量 Δ = σ：单个基站 Q(1) = 0.159；两个都要低于门限：<div class="calc">P_out = [Q(1)]² = 0.0252</div></div></div>
          <div class="wstep"><div class="wn">5</div><div class="wtext"><b>宏分集，共同阴影（P2 Q2 (c)）。</b>相关系数 ρ = b² = 0.5，Δ = σ：先固定共同阴影 Y，两条链路条件独立、相乘，再对 Y 的 PDF 积分。数值积分得 <div class="calc">P_out ≈ 0.0625</div>介于独立（0.0252）和完全相关（0.159）之间。Quiz 不考积分，考这个思路。</div></div>
          <div class="wstep"><div class="wn">6</div><div class="wtext"><b>离散 SNR。</b>SNR 4 dB（概率 0.2）、8 dB（0.5）、12 dB（0.3），门限 6 dB。只有 4 dB 那个取值低于门限：<div class="calc">P_out = 0.2</div>顺便：平均 SNR = 0.2 × 2.51 + 0.5 × 6.31 + 0.3 × 15.85 = 8.41（9.25 dB），不是把 dB 值平均得到的 8.4 dB。</div></div>
          <div class="wstep"><div class="wn">7</div><div class="wtext"><b>ρ、LCR、AFD。</b>f<sub>m</sub> = 50 Hz，门限比 rms 功率低 10 dB → ρ² = 0.1、ρ = 0.316：<div class="calc">低于门限的时间比例 = 1 − e^(−0.1) = 0.0952　LCR = √(2π) × 50 × 0.316 × e^(−0.1) = 35.9 次/s　AFD = 0.0952 / 35.9 = 2.65 ms</div>时间比例其实就是第 3 种情况的瑞利中断（ρ² 就是功率比）。</div></div>
          <div class="wstep"><div class="wn">8</div><div class="wtext"><b>莱斯。</b>K = 6 dB = 3.98：直射功率约为散射功率的 4 倍，衰落比瑞利轻。K = 0 退化成瑞利（最糟），K → ∞ 几乎不衰落、接近 AWGN。莱斯分布公式考试会给，不会让你算它的中断概率。</div></div>
          <div class="wstep"><div class="wn">9</div><div class="wtext"><b>用误码率定义中断（期末，第 3 章）。</b>BPSK 要求 P<sub>b</sub> = Q(√(2γ)) ≤ 10⁻³ → √(2γ₀) = 3.09 → γ₀ = 4.77（6.79 dB）。瑞利、平均 SNR 20 dB：<div class="calc">P_out = 1 − e^(−4.77/100) = 0.0466</div></div></div>
          <div class="wstep"><div class="wn">10</div><div class="wtext"><b>选择分集（期末，第 4 章）。</b>同上的 γ₀/γ̄，M 条独立支路全部低于门限才中断：<div class="calc">M = 1：0.0466　M = 2：2.17 × 10⁻³　M = 3：1.01 × 10⁻⁴</div>和第 4 种情况同一个道理：独立就相乘。</div></div>
          <div class="wans">先认随机性从哪来，再选公式：阴影 → Q；瑞利 → 指数；离散 → 求和；独立多条 → 相乘；共享 → 条件化</div>
        </div>
      </div>
'''),
 ('learn_02.html', ('before_key', '★ 第二章 Quiz 清单'), 'rounding', r'''      <div class="extra">
        <div class="lbl">答题习惯 · 保留几位小数</div>
        <p>讲义和老师都没有规定位数。老师讲 Practice 1 第 1 题时说，结果取决于小数怎么取舍，"在 −31.4、3.86 附近就可以"：方法对、数值接近就给分。总原则：<b>中间步骤多留几位（3–4 位有效数字），只在最后舍入；最终答案约 3 位有效数字。</b></p>
        <div class="tblwrap"><table><thead><tr><th>量</th><th>建议</th><th>例子</th></tr></thead><tbody>
          <tr><td>dB / dBm 值（功率、余量、K）</td><td>1–2 位小数</td><td>−100.7 dBm；K = −37.0 dB</td></tr>
          <tr><td>路径损耗指数 γ</td><td>2 位小数</td><td>3.37、3.94</td></tr>
          <tr><td>Q 函数的参数</td><td>2 位小数（Q 表就是这么列的）</td><td>Q(1.55)、Q(2.39)</td></tr>
          <tr><td>概率</td><td>3 位有效数字，很小时用科学记数法</td><td>0.0601、8.42 × 10⁻³</td></tr>
          <tr><td>线性 SNR、比值</td><td>3 位有效数字</td><td>50.2、0.316、5.01</td></tr>
          <tr><td>时间、容量</td><td>3 位有效数字</td><td>1.03 µs、8.33 ms、28.4 Mbps</td></tr>
          <tr><td>整数性质的量</td><td>取整，说明往哪边取</td><td>55 个符号；N = 60</td></tr>
        </tbody></table></div>
        <p>注意：查 Q 表前先把参数舍到 2 位小数；反查 Q(x) = 0.01 用 2.33 或 2.326 都行，同一题前后一致；dB ↔ 线性换算时多留一位（7 dB → 5.01，不要写 5）；"最大距离""至少"这类答案注意舍入方向。</p>
      </div>
'''),
]
