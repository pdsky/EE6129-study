# English expanded steps for group g3 (p5q1–p5q3, p6q1–p6q3, p7q1–p7q3).
# Same steps, formulas and numbers as the Chinese <ol class="steps"> in prac_5/6/7.html.
STEPS = {
'p5q1': [
r'''<b>Choose the method</b>: the transmitter knows the channel (informed transmitter), so by Ch 5 p.40 we use water-filling (Ch 2 p.54). The given 80, 40, 40 are the SNRs \(\gamma_i\) a sub-channel would have if it received all the power P. Formulas:
\[\begin{aligned}\frac{P_i}{P}&=\frac1{\gamma_0}-\frac1{\gamma_i}\quad(\gamma_i\ge\gamma_0)\\ \sum_i\frac{P_i}{P}&=1,\qquad C=B\sum_i\log_2\frac{\gamma_i}{\gamma_0}\end{aligned}\]
\(\gamma_0\) is the cut-off: a sub-channel whose SNR is below it gets no power.''',
r'''<b>Assume all three get power and find γ₀</b>: expand the power constraint \(\sum_{i=1}^{3}\big(\tfrac1{\gamma_0}-\tfrac1{\gamma_i}\big)=1\):
\[\begin{aligned}\frac3{\gamma_0}&=1+\frac1{80}+\frac1{40}+\frac1{40}\\&=1+0.0125+0.025+0.025=1.0625\\ \gamma_0&=\frac{3}{1.0625}=2.82\end{aligned}\]''',
r'''<b>Check the cut-off</b>: the weakest \(\gamma_i=40\gt\gamma_0=2.82\), so all three powers are positive; the assumption holds and no sub-channel is dropped. (Compare the example on Ch 2 p.56: there \(\gamma_3=0.087\lt\gamma_0\), so that sub-channel is dropped and γ₀ recomputed.)''',
r'''<b>Power allocation</b>: \(1/\gamma_0=1.0625/3=0.3542\):
\[\begin{aligned}\frac{P_1}{P}&=0.3542-\tfrac1{80}\\&=0.3542-0.0125=0.342\\ \frac{P_2}{P}=\frac{P_3}{P}&=0.3542-\tfrac1{40}\\&=0.3542-0.025=0.329\end{aligned}\]
Check: 0.342 + 0.329 + 0.329 = 1.000 ✓. The better sub-channel gets a little more, but the difference is small because all three SNRs are far above \(\gamma_0\).''',
r'''<b>log₂ of each sub-channel</b>: why \(\gamma_i/\gamma_0\): after allocation \(1+\gamma_i\frac{P_i}{P}=1+\gamma_i\big(\frac1{\gamma_0}-\frac1{\gamma_i}\big)=\frac{\gamma_i}{\gamma_0}\). With \(\log_2x=\log_{10}x/0.301\):
\[\begin{aligned}\log_2\tfrac{80}{2.82}&=\log_2 28.33=\tfrac{1.452}{0.301}=4.824\\ \log_2\tfrac{40}{2.82}&=\log_2 14.17=\tfrac{1.151}{0.301}=3.824\end{aligned}\]''',
r'''<b>Total capacity</b>: the three MIMO sub-channels are spatial eigen-channels (from the SVD) and each uses the full 10 MHz, so every term is multiplied by the whole B (not B/3):
\[\begin{aligned}C&=B\,(4.824+2\times3.824)\\&=10\text{ MHz}\times12.47\text{ bit/s/Hz}\\&=124.7\text{ Mbps}\approx125\text{ Mbps}\end{aligned}\]
Check with \(\log_2(1+\gamma_iP_i/P)\) directly: \(1+80\times0.3417=28.33\), \(1+40\times0.3292=14.17\), the same as in the previous step ✓.''',
],

'p5q2': [
r'''<b>Received signals in the two slots</b>: the single receive antenna gets \(y=h_Ax_A+h_Bx_B+w\). Insert the transmit table; the channel is the same in both slots (\(h_A(1)=h_A(2)=h_A\), likewise for B):
\[\begin{aligned}y_1&=h_Au_1+h_Bu_2+w_1\\ y_2&=-h_Au_2^*+h_Bu_1^*+w_2\end{aligned}\]
A channel that stays constant over the two slots is what lets Alamouti separate the two symbols.''',
r'''<b>Conjugate y₂</b>: with \((ab)^*=a^*b^*\) and \((u^*)^*=u\):
\[y_2^*=h_B^*u_1-h_A^*u_2+w_2^*\]
Purpose: both equations become linear in \(u_1,u_2\) (no conjugates), so they can be written as one matrix equation. \(w_2^*\) has the same statistics as \(w_2\); its variance is still \(N_0\).''',
r'''<b>Matrix form and orthogonality check</b>:
\[\tilde{\mathbf y}=\begin{bmatrix}y_1\\y_2^*\end{bmatrix}=\mathbf F\begin{bmatrix}u_1\\u_2\end{bmatrix}+\begin{bmatrix}w_1\\w_2^*\end{bmatrix}\]
\[\begin{aligned}\mathbf F&=\begin{bmatrix}h_A&h_B\\h_B^*&-h_A^*\end{bmatrix}\\ \mathbf F^H&=\begin{bmatrix}h_A^*&h_B\\h_B^*&-h_A\end{bmatrix}\end{aligned}\]
Element by element:
\[\begin{aligned}(\mathbf F^H\mathbf F)_{11}&=h_A^*h_A+h_Bh_B^*=|h_A|^2+|h_B|^2\\ (\mathbf F^H\mathbf F)_{12}&=h_A^*h_B-h_Bh_A^*=0\end{aligned}\]
The (2,1) element is also 0 and the (2,2) element is also \(|h_A|^2+|h_B|^2\), so \(\mathbf F^H\mathbf F=\|\mathbf h\|^2\mathbf I\) (orthogonal, Ch 5 p.23).''',
r'''<b>Matched filter: pre-multiply by F<sup>H</sup></b>: \(\mathbf z=\mathbf F^H\tilde{\mathbf y}\). First row, inserting \(y_1\) and \(y_2^*\):
\[\begin{aligned}z_1&=h_A^*y_1+h_By_2^*\\&=h_A^*(h_Au_1+h_Bu_2+w_1)\\&\quad+h_B(h_B^*u_1-h_A^*u_2+w_2^*)\\&=(|h_A|^2+|h_B|^2)\,u_1\\&\quad+\underbrace{(h_A^*h_B-h_Bh_A^*)}_{=0}\,u_2\\&\quad+h_A^*w_1+h_Bw_2^*\end{aligned}\]
Second row in the same way:
\[\begin{aligned}z_2&=h_B^*y_1-h_Ay_2^*\\&=(|h_A|^2+|h_B|^2)\,u_2\\&\quad+h_B^*w_1-h_Aw_2^*\end{aligned}\]
\(u_2\) cancels exactly in \(z_1\) (and \(u_1\) in \(z_2\)), so the two symbols are fully separated; this is what the orthogonality of \(\mathbf F\) buys.''',
r'''<b>Noise variance and correlation</b>: let \(n_1=h_A^*w_1+h_Bw_2^*\) and \(n_2=h_B^*w_1-h_Aw_2^*\). Multiplying noise by a complex c scales its variance by \(|c|^2\); \(w_1,w_2\) are independent with variance \(N_0\) each:
\[\mathrm{Var}(n_1)=\mathrm{Var}(n_2)=(|h_A|^2+|h_B|^2)N_0\]
Cross-correlation \(E[n_1n_2^*]=h_A^*h_BN_0-h_Bh_A^*N_0\), which is 0: the two noises are uncorrelated (Gaussian ⇒ independent), so \(u_1\) and \(u_2\) can be detected separately.''',
r'''<b>Normalise to get the decision variables</b>: divide both sides by \(\|\mathbf h\|=\sqrt{|h_A|^2+|h_B|^2}\):
\[\begin{aligned}\tilde z_1&=\|\mathbf h\|\,u_1+\tilde w_1\\ \tilde z_2&=\|\mathbf h\|\,u_2+\tilde w_2\\ \tilde w_{1,2}&=n_{1,2}/\|\mathbf h\|\sim\mathcal N(0,N_0)\end{aligned}\]
The noise variance is \(\|\mathbf h\|^2N_0/\|\mathbf h\|^2=N_0\). Decision: map \(\tilde z_n/\|\mathbf h\|\) to the nearest constellation point. The \(\hat{\mathbf s}=\mathbf F^H\tilde{\mathbf y}/\|\mathbf h\|^2\) on Ch 5 p.25 is the same quantity, just divided by one more \(\|\mathbf h\|\).''',
r'''<b>Check</b>: the SNR of each symbol is \(\|\mathbf h\|^2E|u|^2/N_0\) (Ch 5 p.26), where \(\|\mathbf h\|^2=|h_A|^2+|h_B|^2\) is a sum of two independently fading gains ⇒ diversity order 2. Set \(h_B=0\): \(z_1=h_A^*y_1=|h_A|^2u_1+h_A^*w_1\), the ordinary single-antenna matched filter ✓.''',
],

'p5q3': [
r'''<b>Convert dB to linear</b>: \(\gamma=10^{10/10}=10\). The formula \(P_e=\gamma^{-d}\) needs the linear value.''',
r'''<b>Minimum d from the error target</b>:
\[P_e=10^{-d}\le10^{-3}\;\Rightarrow\;-d\le-3\;\Rightarrow\;d\ge3\]
In general:
\[d\ge\frac{\log_{10}(1/P_e^{\text{target}})}{\log_{10}\gamma}=\frac31=3\]''',
r'''<b>Trade-off table</b>: N = 8, M = 4; the multiplexing gain r can only be 0 … min(N, M) = 4 (Ch 4 p.33):<div class="tw"><table class="mini"><thead><tr><th>r</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody><tr><td>(8−r)(4−r)</td><td>8×4</td><td>7×3</td><td>6×2</td><td>5×1</td><td>4×0</td></tr><tr><td>d</td><td>32</td><td>21</td><td>12</td><td>5</td><td>0</td></tr><tr><td>d ≥ 3?</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>✗</td></tr></tbody></table></div>Each extra unit of r lowers d: one more data stream means less protection against fading.''',
r'''<b>(a) Largest r</b>: r = 3 gives d = 5 ≥ 3 ✓; r = 4 gives d = 0 &lt; 3 ✗. So r = 3.''',
r'''<b>(a) Rate</b>: from the definition of the multiplexing gain \(r=R/\log_2\mathrm{SNR}\) (Ch 4 p.32), \(R=r\log_2\gamma\). \(\log_2 10=1/0.301=3.32\) (since \(\log_{10}10=1\)):
\[R=3\times3.32=9.96\ \text{bit/s/Hz}\]
The exact value is 3 × 3.3219 = 9.966; the official answer uses 3.32 and gets 9.96. Check: the upper limit \(r_{\max}\log_2\gamma=4\times3.32=13.3\) bit/s/Hz, and 9.96 is below it ✓.''',
r'''<b>(b) Error probability</b>: r = 3 → \(d(3)=(8-3)(4-3)=5\) → \(P_e=\gamma^{-5}=10^{-5}\). Check: \(10^{-5}\le10^{-3}\) ✓. It beats the target by two orders of magnitude because r must be an integer: d jumps from 5 straight to 0, there is no point with exactly d = 3.''',
],

'p6q1': [
r'''<b>Baseline: no ISI</b>: the threshold is 0 and the signal is \(\sqrt{E_b}\) away from it; the noise variance is \(R_w(0)=N_0/2\), standard deviation \(\sigma=\sqrt{N_0/2}\):
\[P_e=Q\!\Big(\frac{\sqrt{E_b}}{\sqrt{N_0/2}}\Big)=Q\!\Big(\sqrt{\tfrac{2E_b}{N_0}}\Big)\equiv Q(A)\]
Every term below is Q(distance / standard deviation), written as Q(coefficient × A).''',
r'''<b>(a) No equaliser: split into cases and average</b>: \(H(z)=1+\alpha z^{-1}\) means "current symbol + α times the previous symbol": \(z(n)=\sqrt{E_b}(a_n+\alpha a_{n-1})+w(n)\). Take \(a_n=+1\) (−1 is symmetric and gives the same result):<div class="tw"><table class="mini"><thead><tr><th>\(a_{n-1}\)</th><th>mean</th><th>error probability</th></tr></thead><tbody><tr><td>+1 (same sign)</td><td>\((1+\alpha)\sqrt{E_b}\)</td><td>\(Q\big((1+\alpha)A\big)\)</td></tr><tr><td>−1 (opposite sign)</td><td>\((1-\alpha)\sqrt{E_b}\)</td><td>\(Q\big((1-\alpha)A\big)\)</td></tr></tbody></table></div>Each case has probability ½; average them (Ch 6 p.28):<div class="calc">P<sub>e</sub> = ½Q((1 − α)A) + ½Q((1 + α)A)</div>''',
r'''<b>(a) With the equaliser: the signal sees H·U</b>: the signal passes through the channel and then the equaliser, so the overall response is
\[\begin{aligned}H(z)U(z)&=(1+\alpha z^{-1})(1-\alpha z^{-1})\\&=1-\alpha z^{-1}+\alpha z^{-1}-\alpha^2z^{-2}\\&=1-\alpha^2z^{-2}\end{aligned}\]
The signal part becomes \(\sqrt{E_b}(a_n-\alpha^2a_{n-2})\): the ISI drops from α to α² (for α = 0.4, from 0.4 to 0.16), but it is not removed; it moves to n − 2.''',
r'''<b>(a) With the equaliser: the noise sees only U</b>: the noise is added after the channel, so it passes only through U(z): \(w^{\prime}(n)=w(n)-\alpha w(n-1)\). The two samples are independent, so the variance is the input variance times the sum of squared coefficients (\(\sigma^2\|\mathbf c\|^2\), Ch 6 p.27):
\[\sigma'^2=\frac{N_0}{2}(1^2+\alpha^2)\;\Rightarrow\;\sigma'=\sqrt{\tfrac{N_0}{2}}\sqrt{1+\alpha^2}\]''',
r'''<b>(a) With the equaliser: split into cases and average</b>: \(z(n)=\sqrt{E_b}(a_n-\alpha^2a_{n-2})+w^{\prime}(n)\); take \(a_n=+1\) and divide the distance by \(\sigma'\):<div class="tw"><table class="mini"><thead><tr><th>\(a_{n-2}\)</th><th>mean</th><th>error probability</th></tr></thead><tbody><tr><td>+1 (same sign)</td><td>\((1-\alpha^2)\sqrt{E_b}\)</td><td>\(Q\Big(\frac{1-\alpha^2}{\sqrt{1+\alpha^2}}A\Big)\)</td></tr><tr><td>−1 (opposite sign)</td><td>\((1+\alpha^2)\sqrt{E_b}\)</td><td>\(Q\Big(\frac{1+\alpha^2}{\sqrt{1+\alpha^2}}A\Big)\)</td></tr></tbody></table></div><div class="calc">P<sub>e</sub> = ½Q( (1 − α²)/√(1 + α²) · A ) + ½Q( (1 + α²)/√(1 + α²) · A )</div>Check: as α → 0 both expressions return to Q(A) ✓.''',
r'''<b>(b) At high SNR look at the worst term</b>: \(Q(x)\le\tfrac12e^{-x^2/2}\) falls extremely fast with x, so at high SNR \(P_e\) is dominated by the term with the <b>smallest</b> Q argument. The smallest coefficients are: without equaliser \(1-\alpha\); with equaliser \((1-\alpha^2)/\sqrt{1+\alpha^2}\).''',
r'''<b>(b) Show that the equaliser is better</b>: divide both sides by \(1-\alpha\gt0\):
\[\begin{aligned}\frac{1-\alpha^2}{\sqrt{1+\alpha^2}}\gt1-\alpha&\Leftrightarrow\frac{1+\alpha}{\sqrt{1+\alpha^2}}\gt1\\&\Leftrightarrow(1+\alpha)^2\gt1+\alpha^2\\&\Leftrightarrow2\alpha\gt0\end{aligned}\]
This always holds for α &gt; 0, so at high SNR it is <b>better to use the equaliser</b>: the gain from the smaller ISI outweighs the loss from the noise growing by \(\sqrt{1+\alpha^2}\).''',
r'''<b>Numerical check</b>: α = 0.4: worst coefficient 0.6 without, \(0.84/1.077=0.78\) with the equaliser. At \(E_b/N_0=10\) dB (linear 10, \(A=\sqrt{20}=4.47\)):
\[\begin{aligned}\text{without}&:\ \tfrac12Q(2.68)+\tfrac12Q(6.26)\\&\ =1.8\times10^{-3}\\ \text{with}&:\ \tfrac12Q(3.49)+\tfrac12Q(4.82)\\&\ =1.2\times10^{-4}\end{aligned}\]
The equaliser lowers the error rate about 15 times ✓.''',
],

'p6q2': [
r'''<b>(a) Split into cases</b>: noise variance 0.1, standard deviation \(\sigma=\sqrt{0.1}=0.316\); threshold 0. Take \(b_n=+1\); an error means \(y_n\lt0\):<div class="tw"><table class="mini"><thead><tr><th>\(b_{n-1}\)</th><th>mean of \(y_n\)</th><th>error probability</th></tr></thead><tbody><tr><td>+1</td><td>1 + a</td><td>\(Q\big(\frac{1+a}{\sqrt{0.1}}\big)\)</td></tr><tr><td>−1</td><td>1 − a</td><td>\(Q\big(\frac{1-a}{\sqrt{0.1}}\big)\)</td></tr></tbody></table></div>0 &lt; a &lt; 1 keeps 1 − a &gt; 0, so the mean stays on the correct side of the threshold.''',
r'''<b>(a) Average</b>: each case has probability ½; \(b_n=-1\) is symmetric and gives the same result (Ch 6 p.28):<div class="calc">P<sub>e</sub> = ½Q((1 + a)/√0.1) + ½Q((1 − a)/√0.1)</div>''',
r'''<b>(b) Ideal zero-forcing equaliser</b>: zero forcing (ZF) uses \(C(z)=1/H(z)\), so that \(C(z)H(z)=1\) (Ch 6 p.23). Expand as a geometric series (|a| &lt; 1, so it converges and is stable):
\[\begin{aligned}C(z)&=\frac{1}{1+az^{-1}}=\sum_{k\ge0}(-a)^kz^{-k}\\&=1-az^{-1}+a^2z^{-2}-\cdots\end{aligned}\]
Output \(=b_n+\tilde w_n\) with \(\tilde w_n=\sum_k(-a)^kw_{n-k}\): the ISI is gone completely, so there is no case split.''',
r'''<b>(b) Noise enhancement</b>: white noise through a filter has variance = input variance × sum of squared coefficients:
\[\begin{aligned}\sigma_{\tilde w}^2&=0.1\sum_{k\ge0}a^{2k}=0.1(1+a^2+a^4+\cdots)\\&=\frac{0.1}{1-a^2}\end{aligned}\]
The closer a is to 1, the larger \(1/(1-a^2)\): this is the noise enhancement of zero forcing.''',
r'''<b>(b) Error probability</b>: signal amplitude 1, standard deviation \(\sqrt{0.1/(1-a^2)}\):
\[\begin{aligned}P_e&=Q\!\left(\frac{1}{\sqrt{0.1/(1-a^2)}}\right)\\&=Q\!\left(\sqrt{\frac{1-a^2}{0.1}}\right)\end{aligned}\]''',
r'''<b>Numerical check</b>: take a = 0.5:
\[\begin{aligned}\text{(a)}&:\ \tfrac12Q(4.74)+\tfrac12Q(1.58)\\&\ \approx\tfrac12(0.057)=0.028\\ \text{(b)}&:\ \sigma_{\tilde w}^2=\tfrac{0.1}{0.75}=0.133\\&\ Q(\sqrt{7.5})=Q(2.74)=0.0031\end{aligned}\]
ZF is about 9 times better; as a → 0 both formulas become \(Q(1/\sqrt{0.1})=Q(3.16)\) ✓.''',
],

'p6q3': [
r'''<b>(a) Expand the error</b>: with \(x_0=1\), \(x_1=\tfrac12\): \(y_n=A_n+\tfrac12A_{n-1}+z_n\) and \(y_{n+1}=A_{n+1}+\tfrac12A_n+z_{n+1}\):
\[\begin{aligned}u_n-A_n&=y_n+qy_{n+1}-A_n\\&=\tfrac q2A_n+\tfrac12A_{n-1}+qA_{n+1}\\&\quad+z_n+qz_{n+1}\end{aligned}\]
Note that \(y_{n+1}\) also contains \(\tfrac12A_n\), so the coefficient of \(A_n\) in \(u_n\) is \(1+\tfrac q2\) and \(\tfrac q2A_n\) is left in the error.''',
r'''<b>(a) Mean squared error (MSE)</b>: the five terms are independent with zero mean, so the cross terms average to 0 and the mean squares simply add; \(E[A^2]=1\), \(E[z^2]=\sigma^2=1\):
\[\begin{aligned}E[(u_n-A_n)^2]&=\tfrac{q^2}4+\tfrac14+q^2+1+q^2\\&=1.25+2.25q^2\end{aligned}\]''',
r'''<b>(a) Optimal q</b>: \(\frac{d}{dq}(1.25+2.25q^2)=4.5q\); setting it to 0 gives q = 0, minimum MSE = 1.25. Reason: using \(y_{n+1}\) adds only \(\tfrac q2A_n\) of useful signal but brings in \(qA_{n+1}\) interference and \(qz_{n+1}\) noise, a net loss.''',
r'''<b>(a) Error probability</b>: with q = 0, \(u_n=y_n\) and σ = 1. Take \(A_n=+1\): the mean is 1.5 if \(A_{n-1}=+1\) and 0.5 if \(A_{n-1}=-1\), ½ each. From the Q-table: Q(1.5) = 0.0668, Q(0.5) = 0.3085:
\[P_e=\tfrac12(0.0668)+\tfrac12(0.3085)=0.188\approx0.19\]''',
r'''<b>(b) Previous decision correct</b>:
\[\begin{aligned}u_n&=y_n-\tfrac12\hat A_{n-1}\\&=A_n+\tfrac12(A_{n-1}-\hat A_{n-1})+z_n\end{aligned}\]
If the decision was correct the bracket is 0 and \(u_n=A_n+z_n\): the ISI is cancelled exactly, error probability \(Q(1/1)=Q(1)=0.159\).''',
r'''<b>(b) Previous decision wrong</b>: \(\hat A_{n-1}=-A_{n-1}\), the bracket is \(2A_{n-1}\) and \(u_n=A_n+A_{n-1}+z_n\): instead of being removed, the ISI is doubled. Take \(A_n=+1\): if \(A_{n-1}=+1\) the mean is 2 → Q(2) = 0.0228; if \(A_{n-1}=-1\) the mean is 0, right on the threshold → Q(0) = ½:
\[\begin{aligned}&P(\text{error}\mid\text{previous error})\\&=\tfrac12(0.0228)+\tfrac12(0.5)=0.261\end{aligned}\]''',
r'''<b>(b) Steady-state error rate</b>: for large n the error probability tends to one value p; by total probability:
\[\begin{aligned}p&=(1-p)\times0.159+p\times0.261\\ p&=\frac{0.159}{1-0.261+0.159}\\&=\frac{0.159}{0.898}=0.177\approx0.18\end{aligned}\]
Check: starting at n = 1 (\(A_0=0\), so the first decision has no ISI), \(p_1=0.159\) and \(p_n=0.159+0.102\,p_{n-1}\): \(p_2=0.175\), \(p_3=0.177\), quickly converging to 0.177 ✓. Also 0.159 (no error propagation) &lt; 0.177 (DFE) &lt; 0.188 (linear equaliser), a sensible order.''',
],

'p7q1': [
r'''<b>(a) Flat condition</b>: the bandwidth of each sub-carrier, \(\Delta f=B/N\), must be much smaller than the coherence bandwidth \(B_C\), so the frequency response is almost constant inside one sub-band and each sub-carrier sees a single complex gain \(H_k\):
\[\frac BN\ll B_C\;\Rightarrow\;N\gg\frac{B}{B_C}\]
The condition \(T=NT_S\gg T_D\approx1/B_C\) on Ch 7 p.5 and p.14 is the same thing.''',
r'''<b>(a) Slow condition</b>: the OFDM symbol duration \(T=N/B\) (\(=NT_S\), \(T_S=1/B\)) must be much shorter than the coherence time \(T_C\approx1/B_d\), so the channel does not change during one OFDM symbol and the sub-carriers stay orthogonal (no ICI):
\[\frac NB\ll\frac1{B_d}\;\Rightarrow\;N\ll\frac{B}{B_d}\]
Together: \(\dfrac{B}{B_C}\ll N\ll\dfrac{B}{B_d}\), which has a solution only if \(B_d\ll B_C\). Example: B = 1 MHz, \(B_C\) = 50 kHz, \(B_d\) = 100 Hz → 20 ≪ N ≪ 10⁴, e.g. N = 256 (a power of 2 for the FFT).''',
r'''<b>(b) Write H<sub>k</sub></b>: the impulse response of the two-path channel is \(h=[h_0,h_1]=[0.8,0.6]\) (τ is one sampling interval). The sub-channel gains are its DFT (Ch 7 p.15):
\[H_k=\sum_{i=0}^{L-1}h_ie^{-j2\pi ik/N}=0.8+0.6\,e^{-j\pi k/2}\]
For k = 1, 2, 3, 4, \(e^{-j\pi k/2}=-j,\ -1,\ j,\ 1\):
\[\begin{aligned}H_1&=0.8-0.6j\\ H_2&=0.8-0.6=0.2\\ H_3&=0.8+0.6j\\ H_4&=H_0=0.8+0.6=1.4\end{aligned}\]''',
r'''<b>(b) Power gains and check</b>: the power allocation needs \(|H_k|^2\):
\[\begin{aligned}|H_1|^2&=|H_3|^2=0.8^2+0.6^2=1\\ |H_2|^2&=0.2^2=0.04,\quad|H_4|^2=1.4^2=1.96\end{aligned}\]
Check (Parseval): the four \(|H_k|^2\) add up to 1 + 0.04 + 1 + 1.96 = 4, equal to \(N(h_0^2+h_1^2)=4\times1=4\) ✓.''',
r'''<b>(c) Equal-capacity allocation</b>: noise \(\sigma^2=1\), capacity of sub-channel k is \(\log_2(1+|H_k|^2P_k)\). Equal capacities ⇔ equal received SNR \(|H_k|^2P_k=c\), so \(P_k=c/|H_k|^2\). Insert into the total power:
\[\begin{aligned}10&=c\Big(\tfrac11+\tfrac1{0.04}+\tfrac11+\tfrac1{1.96}\Big)\\&=c(1+25+1+0.510)=27.51\,c\\ c&=10/27.51=0.3635\end{aligned}\]
\[\begin{aligned}P_1&=P_3=0.3635/1=0.36\\ P_2&=0.3635/0.04=9.09\\ P_4&=0.3635/1.96=0.19\end{aligned}\]
Check: 0.36 + 9.09 + 0.36 + 0.19 = 10.0 ✓. Every sub-channel has capacity \(\log_2 1.3635=0.447\) bit, and the worst sub-channel 2 takes 91% of the power.''',
r'''<b>(d) Water-filling: first try all four</b>: the water-filling solution is \(P_k=(\mu-1/|H_k|^2)^+\), with floors \(1/|H_k|^2\) = 1, 25, 1, 0.51. Filling all four:
\[\begin{aligned}\mu&=\frac{10+(1+25+1+0.51)}{4}\\&=\frac{37.51}{4}=9.38\end{aligned}\]
But \(9.38\lt25\): sub-channel 2 would get negative power (\(9.38-25\lt0\)), so drop it and recompute.''',
r'''<b>(d) Three sub-channels left</b>:
\[\begin{aligned}\mu&=\frac{10+1+1+0.51}{3}=\frac{12.51}{3}=4.17\\ P_1&=P_3=4.17-1=3.17\\ P_4&=4.17-0.51=3.66\end{aligned}\]
All positive ✓; 3.17 + 3.17 + 3.66 = 10.0 ✓; the floor of sub-channel 2 (25) is above the water level 4.17, so it stays out ✓.''',
r'''<b>(d) Sum capacity</b>: each sub-channel gives \(\log_2(1+|H_k|^2P_k)=\log_2(\mu|H_k|^2)\); with \(\log_2x=\log_{10}x/0.301\):
\[\begin{aligned}C_1=C_3&=\log_2 4.17=\tfrac{0.620}{0.301}=2.06\\ C_4&=\log_2(4.17\times1.96)\\&=\log_2 8.17=\tfrac{0.912}{0.301}=3.03\\ \textstyle\sum_k C_k&=2.06+2.06+3.03=7.15\text{ bit}\end{aligned}\]
Each sub-carrier occupies only B/4, \(C=\sum_k\frac B4\log_2(\cdot)\), so per hertz \(C/B=7.15/4=1.79\approx1.8\) bit/s/Hz (matches the official answer). Compare (c): only 0.447 bit/s/Hz, so water-filling is about 4 times higher.''',
],

'p7q2': [
r'''<b>Bit rate → symbol rate</b>: 16-QAM carries \(\log_2 16=4\) bits per symbol:
\[R_s=\frac{2\times10^6\text{ bit/s}}{4\text{ bit/symbol}}=5\times10^5\text{ symbols/s}\]''',
r'''<b>OFDM timing</b>: with N sub-carriers the spacing is \(\Delta f=B/N\) and the useful symbol duration is \(T=1/\Delta f=N/B\) (Ch 7 p.8). With the cyclic prefix \(T_G=T_D=20\) µs one OFDM block lasts \(T+T_G\) (p.18), during which each of the N sub-carriers sends one symbol:
\[\text{symbol rate}=\frac{N}{T+T_G}=\frac{N}{N/B+T_G}\]''',
r'''<b>Solve for N</b>: set it equal to \(R_s\):
\[\begin{aligned}N&=R_s\Big(\frac NB+T_G\Big)\\&=\tfrac{500\text{k}}{600\text{k}}N+500\text{k}\times20\ \mu\text{s}\\&=0.8333N+10\\ N&=\frac{10}{1-0.8333}=\frac{10}{0.1667}=60\end{aligned}\]''',
r'''<b>Symbol durations</b>:
\[\begin{aligned}T&=\frac NB=\frac{60}{600\text{ kHz}}=100\ \mu\text{s}\\ T+T_G&=100+20=120\ \mu\text{s}=0.12\text{ ms}\end{aligned}\]
Sub-carrier spacing Δf = 600 kHz / 60 = 10 kHz = 1/T ✓.''',
r'''<b>Check</b>: each OFDM block carries 60 × 4 = 240 bits, and 240 bits / 120 µs = 2 × 10⁶ bit/s = 2 Mbps ✓. The CP takes 20/120 = 1/6 of the time; the power loss is \(10\log_{10}(120/100)=0.79\) dB (Ch 7 p.18).''',
],

'p7q3': [
r'''<b>Read the impulse response</b>: \(H(Z)=\sum_ih_iZ^{-i}\), and \(Z^{-1}\) means one sample later. So \(h_0=1\) (direct path) and \(h_1=0.9\) (an echo one sample late): channel length L = 2, longest echo L − 1 = 1 sample late.''',
r'''<b>Where the ISI comes from</b>: a received sample is \(r_i=x_i+0.9x_{i-1}+w_i\). The first sample of a block, i = 0, uses \(x_{-1}\); without a CP that is the last sample of the <b>previous</b> block, which causes inter-block interference (ISI). For i ≥ 1 only the current block is used, so just 1 sample per block is corrupted.''',
r'''<b>Add a 1-sample CP</b>: copy the last sample of the block to its front: \(x_{-1}=x_{N-1}\). The receiver discards the CP sample \(r_{-1}\) (it contains the echo of the previous block); the first sample kept is
\[r_0=x_0+0.9\,x_{N-1}+w_0\]
which contains only current-block data: the ISI is caught inside the CP.''',
r'''<b>Why copy the tail</b>: the N kept samples satisfy \(r_i=\sum_lh_lx_{(i-l)\bmod N}+w_i\), a circular convolution. After the DFT this gives exactly \(R_k=H_kS_k+W_k\) (Ch 7 p.22) with \(H_k=1+0.9e^{-j2\pi k/N}\): the sub-carriers stay orthogonal, there is no ICI, and one complex division \(\hat s_k=R_k/H_k\) equalises each sub-carrier. A guard interval filled with zeros would also block the ISI, but it breaks the circular structure and ICI appears.''',
r'''<b>Conclusion and check</b>: minimum CP = L − 1 = 1 sample (one symbol duration \(T_S\)). G = 0 fails (ISI and ICI); G = 2 also works but wastes a sample and lowers the efficiency N/(N + G). Check with N = 4: the kept samples are \(r_0=x_0+0.9x_3\), \(r_1=x_1+0.9x_0\), \(r_2=x_2+0.9x_1\), \(r_3=x_3+0.9x_2\), exactly the 4-point circular convolution of [1, 0.9] with x ✓. The size of the coefficient 0.9 does not affect the CP length; only how many samples the echo is delayed matters.''',
],
}

IDEA = {}
