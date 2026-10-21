#!/usr/bin/python3
"""Extra explanation boxes on the Part 2 learning page, written from the user's questions (2026-10).

Each note is a purple 课外补充 box inserted right after a formula card (found by its label) in a
learn_NN.html fragment, between <!-- NOTE:id --> and <!-- /NOTE:id --> markers, so re-running is
idempotent. Run before build_learn.py (any order relative to quiz_marks.py).
"""
import pathlib, re

B = pathlib.Path(__file__).parent

NOTES = [
 ('learn_02.html', '简化路径损耗模型（p.8）', 'dbm', r'''      <div class="extra">
        <div class="lbl">课外补充 · dB 和 dBm：K 为什么是 dB，不是 dBm</div>
        <p><b>dBm 是绝对功率</b>（以 1 mW 为参考）：\(10\log_{10}(P/1\,\text{mW})\)，例如 100 mW = 20 dBm、1 mW = 0 dBm。<b>dB 是两个功率的比值</b>：\(10\log_{10}(P_1/P_2)\)，没有单位，例如衰减到 1/1000 是 −30 dB。可以记成：dBm 是"有多少"，dB 是"变了多少倍"。</p>
        <p>线性式 \(P_r=P_tK(d_0/d)^{\gamma}\) 里只有 \(P_t\)、\(P_r\) 是功率；K 和 \((d_0/d)^{\gamma}\) 都是乘在功率上的倍数（K 就是 d = d₀ 处的 \(P_r/P_t\)）。取对数后乘法变加法，所以只有 \(P_t\)、\(P_r\) 是 dBm，\(K_{dB}\) 和 \(10\gamma\log_{10}(d/d_0)\) 都是 dB：</p>
        <div class="tblwrap"><table><thead><tr><th>运算</th><th>结果</th><th>意思</th></tr></thead><tbody>
          <tr><td>dBm + dB</td><td>dBm</td><td>功率乘一个倍数，还是功率（路径损耗模型就是这样）</td></tr>
          <tr><td>dBm − dBm</td><td>dB</td><td>两个功率相除得到倍数：余量、SNR</td></tr>
          <tr><td>dB + dB</td><td>dB</td><td>倍数乘倍数，还是倍数</td></tr>
          <tr><td>dBm + dBm</td><td>没有意义</td><td>功率乘功率不是功率</td></tr>
        </tbody></table></div>
        <p>所以余量（平均功率 − 门限，两个 dBm 相减）和阴影的标准差 σ 都是 dB。Practice 1 第 2 题原文把 σ 写成 "dBm"，严格说应该是 dB。</p>
      </div>
'''),
 ('learn_02.html', '瑞利衰落（p.25–26）', 'rayout', r'''      <div class="extra">
        <div class="lbl">课外补充 · 瑞利中断 1 − e<sup>−γ₀/γ̄</sup> 是怎么积出来的（推导不考，帮助理解）</div>
        <p>老师说瑞利分布的推导不会让推，Quiz 也不考积分；这里只是说明公式从哪来，考试记住结果、会用就行。</p>
        <ol class="steps">
          <li>SNR 和功率成正比：\(\gamma=z^2/N\)，平均 \(\bar\gamma=E[z^2]/N=2\sigma^2/N\)。"γ 低于 γ₀"就是"z 低于 z₀"，其中 \(z_0^2=\gamma_0N\)。</li>
          <li>对瑞利 PDF 从 0 积到 z₀，换元 \(u=z^2/(2\sigma^2)\)、\(du=z\,dz/\sigma^2\)：\(P(z\lt z_0)=\displaystyle\int_0^{z_0}\frac{z}{\sigma^2}e^{-z^2/(2\sigma^2)}dz=\int_0^{z_0^2/(2\sigma^2)}e^{-u}du=1-e^{-z_0^2/(2\sigma^2)}\)。</li>
          <li>指数里的量换成 SNR：\(\dfrac{z_0^2}{2\sigma^2}=\dfrac{\gamma_0N}{\bar\gamma N}=\dfrac{\gamma_0}{\bar\gamma}\)，所以 \(P_{out}=1-e^{-\gamma_0/\bar\gamma}\)。</li>
          <li>对 γ₀ 求导就得到 SNR 的指数分布 \(p(\gamma)=\frac{1}{\bar\gamma}e^{-\gamma/\bar\gamma}\)。两个要背的公式是一对：指数分布是 PDF，中断概率是它的 CDF。</li>
        </ol>
        <div class="tblwrap"><table><thead><tr><th>检查</th><th>代入</th><th>结果</th><th>含义</th></tr></thead><tbody>
          <tr><td>γ₀ = 0</td><td>1 − e⁰</td><td>0</td><td>不要求 SNR，永远不中断</td></tr>
          <tr><td>γ₀ → ∞</td><td>1 − e<sup>−∞</sup></td><td>1</td><td>永远达不到，总是中断</td></tr>
          <tr><td>γ₀ = γ̄</td><td>1 − e⁻¹</td><td>0.632</td><td>63% 的时间低于平均值，所以要留余量</td></tr>
          <tr><td>γ₀ ≪ γ̄</td><td>e<sup>−x</sup> ≈ 1 − x</td><td>≈ γ₀/γ̄</td><td>中断 1% 要 γ̄ ≈ 100γ₀，即衰落余量约 20 dB</td></tr>
        </tbody></table></div>
        <p>用的时候：γ₀、γ̄ 先换成线性值（公式里是两者的比值，单位一致即可）；反求平均 SNR 用 \(\bar\gamma=\gamma_0/\ln\frac{1}{1-P_{out}}\)。</p>
      </div>
'''),
 ('learn_02.html', 'AWGN 信道的香农容量', 'sinr', r'''      <div class="extra">
        <div class="lbl">课外补充 · SNR、SIR、SINR 的区别，香农公式里该用哪个</div>
        <div class="tblwrap"><table><thead><tr><th>指标</th><th>分母</th><th>什么时候用</th></tr></thead><tbody>
          <tr><td>SNR = S/N</td><td>只有噪声</td><td>单用户、没有干扰，例如 AWGN 信道</td></tr>
          <tr><td>SIR = S/I</td><td>只有干扰</td><td>干扰远大于噪声、噪声可以忽略，例如 Part A 的同频复用</td></tr>
          <tr><td>SINR = S/(I + N)</td><td>干扰 + 噪声</td><td>两者都不能忽略的一般情况</td></tr>
        </tbody></table></div>
        <p>分母就是"所有不是你想要的功率"。SINR 最完整：I = 0 时变成 SNR，N = 0 时变成 SIR，所以 SINR 比 SNR、SIR 都小。</p>
        <p><b>为什么 Practice 2 第 3 题 (a) 的分母是 10 + 0.1：</b>两个用户同时同频发，接收机收到的是"用户 1（10 mW）+ 用户 2（10 mW）+ 噪声（0.1 mW）"。解用户 1 时，用户 2 的信号也在、而且比噪声强 100 倍，它和噪声一样会把用户 1 弄模糊，所以 SINR = 10 /(10 + 0.1) = 0.99。只写 0.1 等于假装用户 2 不存在。(b) 用 MUD 把用户 1 解出来并减掉以后，解用户 2 时只剩噪声，分母才是 0.1。</p>
        <p><b>为什么香农公式写的是 SNR：</b>香农推导的是单用户 AWGN 信道 y = x + w，只有一个发射机、只有高斯噪声，I = 0，SINR 就是 SNR。公式真正要求的是"分母里的东西整体是高斯噪声"。题目说把用户 2 的信号当成 AWGN（"assume it is AWGN"），"干扰 + 噪声"就成了一个更大的高斯噪声，公式照用，只是 N 换成 I + N：\(C=B\log_2(1+\text{SINR})\)。把干扰当高斯噪声算出的是保守的容量；MUD 利用"干扰其实是另一个用户的数据"把它减掉，所以能做得更好。</p>
      </div>
'''),
]


def card_end(s, label):
    a = s.find(f'<div class="flbl">{label}')
    assert a >= 0, label
    return s.find('\n      </div>\n', a) + len('\n      </div>\n')


def apply():
    for frag in sorted({n[0] for n in NOTES}):
        f = B / frag
        s = re.sub(r'<!-- NOTE:(\w+) -->\n.*?<!-- /NOTE:\1 -->\n', '', f.read_text(encoding='utf-8'), flags=re.S)
        for fr, label, nid, html in NOTES:
            if fr == frag:
                e = card_end(s, label)
                if nid == 'dbm':                 # after the paragraph that turns the model into dB form
                    p = s.find('<p><b>怎么从左边的式子得到右边</b>', e)
                    assert p >= 0
                    e = s.find('</p>\n', p) + len('</p>\n')
                s = s[:e] + f'<!-- NOTE:{nid} -->\n' + html + f'<!-- /NOTE:{nid} -->\n' + s[e:]
        f.write_text(s, encoding='utf-8')
    print('extra notes:', len(NOTES))

apply()
