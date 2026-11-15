"""English expanded steps for group g2: p3q2, p3q3 (prac_3.html) and p4q1, p4q2, p4q3 (prac_4.html).
Same steps, formulas and numbers as the Chinese <ol class="steps"> in the sol-zh blocks.
Merged into src/p2build/sol_en.py by src/steps/merge_en.py.
"""

STEPS = {
 'p3q2': [
r'''<b>Write the two likelihoods</b>: \(y_n=x_n+w_n\), so given x the PDF of y is the noise PDF shifted to x:
\[\begin{aligned}f(y\mid0)&=\tfrac{1}{\sqrt{2\pi}\,\sigma_0}\,e^{-y^2/2\sigma_0^2}\\ f(y\mid1)&=\tfrac{1}{\sqrt{2\pi}\,\sigma_1}\,e^{-(y-1)^2/2\sigma_1^2}\end{aligned}\]
i.e. \(y\sim\mathcal N(0,\sigma_0^2)\) if 0 is sent and \(y\sim\mathcal N(1,\sigma_1^2)\) if 1 is sent. The ML detector chooses the larger likelihood (lecture Ch 3 p.18–19); both priors are ½, so ML makes the same decisions as MAP and minimises the error probability.''',
r'''<b>Compare the likelihoods and take logs</b>: decide 1 when \(f(y\mid1)\gt f(y\mid0)\). The \(\sqrt{2\pi}\) cancels on both sides, but 1/σ does not (σ₀ ≠ σ₁):
\[\frac{1}{\sigma_1}e^{-\frac{(y-1)^2}{2\sigma_1^2}}\gt\frac{1}{\sigma_0}e^{-\frac{y^2}{2\sigma_0^2}}\]
ln is increasing, so taking logs keeps the direction of the inequality: \(-\ln\sigma_1-\frac{(y-1)^2}{2\sigma_1^2}\gt-\ln\sigma_0-\frac{y^2}{2\sigma_0^2}\). Moving everything to the left:
\[g(y)=\frac{y^2}{2\sigma_0^2}-\frac{(y-1)^2}{2\sigma_1^2}+\ln\frac{\sigma_0}{\sigma_1}\gt0\]''',
r'''<b>Rewrite as a quadratic</b>: multiply both sides by \(2\sigma_0^2\sigma_1^2\) (positive, so the inequality is unchanged) and use \(2\ln\frac{\sigma_0}{\sigma_1}=-\ln\frac{\sigma_1^2}{\sigma_0^2}\):
\[\begin{aligned}&\sigma_1^2y^2-\sigma_0^2(y-1)^2-\sigma_0^2\sigma_1^2\ln\tfrac{\sigma_1^2}{\sigma_0^2}\gt0\\ \Rightarrow\;&(\sigma_1^2-\sigma_0^2)\,y^2+2\sigma_0^2\,y\\&\quad-\sigma_0^2\Big(1+\sigma_1^2\ln\tfrac{\sigma_1^2}{\sigma_0^2}\Big)\gt0\end{aligned}\]
Write it as \(ay^2+by+c\gt0\) with \(a=\sigma_1^2-\sigma_0^2\gt0\), \(b=2\sigma_0^2\), \(c=-\sigma_0^2\big(1+\sigma_1^2\ln\frac{\sigma_1^2}{\sigma_0^2}\big)\lt0\) (σ₁² &gt; σ₀², so the ln term is positive).''',
r'''<b>(a) Threshold and decision rule</b>: a &gt; 0, so the parabola opens upwards and g &gt; 0 (decide 1) outside the two roots. The product of the roots is c/a &lt; 0, so one root is positive and one negative; the threshold ỹ is the positive root:
\[\begin{aligned}\tilde y&=\frac{-b+\sqrt{b^2-4ac}}{2a}\\&=\frac{-\sigma_0^2+\sqrt{\sigma_0^4-ac}}{\sigma_1^2-\sigma_0^2}\\ -ac&=(\sigma_1^2-\sigma_0^2)\,\sigma_0^2\Big(1+\sigma_1^2\ln\tfrac{\sigma_1^2}{\sigma_0^2}\Big)\end{aligned}\]
Decision rule: \(\hat x_n=1\) if \(y_n\gt\tilde y\), \(\hat x_n=0\) if \(y_n\lt\tilde y\). Below the negative root g is also &gt; 0 (a very negative y is also decided as 1), but when 0 is sent y lands there with probability only about 2 × 10⁻⁴ (see the example in step 5), so the standard answer ignores it.''',
r'''<b>(a) Self-check</b>: ① Equal variances (σ₀ = σ₁ = σ): a = 0 and the ln term is 0, leaving \(2\sigma^2y-\sigma^2\gt0\), i.e. y &gt; 0.5, back to the midpoint (minimum-distance rule, lecture p.20) ✓. ② Numerical example σ₀² = 0.1, σ₁² = 0.4:
<div class="calc">g(y) = y²/0.2 − (y − 1)²/0.8 + ln(√0.1/√0.4)<br>= 5y² − 1.25(y² − 2y + 1) + ln 0.5<br>= 3.75y² + 2.5y − 1.25 − 0.6931<br>= 3.75y² + 2.5y − 1.9431<br>b² − 4ac = 2.5² + 4 × 3.75 × 1.9431 = 35.397, √35.397 = 5.9496<br>ỹ = (−2.5 + 5.9496)/7.5 = 0.460<br>other root = (−2.5 − 5.9496)/7.5 = −1.127</div>
Substituting back into the two PDFs: f(0.460 | 0) = f(0.460 | 1) = 0.438, equal at the threshold ✓. ỹ = 0.46 &lt; 0.5: the noise is larger when 1 is sent, so the threshold moves towards 0 ✓.''',
r'''<b>(b) Turn each error event into a Q function</b>: by total probability, \(P_e=P(x=0)\,P(y\gt\tilde y\mid0)+P(x=1)\,P(y\lt\tilde y\mid1)\). 0 sent, 1 decided: the range is ỹ to ∞; substitute u = y/σ₀:
\[\begin{aligned}P(y\gt\tilde y\mid0)&=\int_{\tilde y}^{\infty}\tfrac{1}{\sqrt{2\pi}\,\sigma_0}e^{-y^2/2\sigma_0^2}dy\\&=\int_{\tilde y/\sigma_0}^{\infty}\tfrac{1}{\sqrt{2\pi}}e^{-u^2/2}du\\&=Q\Big(\tfrac{\tilde y}{\sigma_0}\Big)\end{aligned}\]
1 sent, 0 decided: the range is −∞ to ỹ; substitute u = (y − 1)/σ₁, so the upper limit becomes (ỹ − 1)/σ₁ &lt; 0; by Gaussian symmetry P(u &lt; −a) = Q(a):
\[P(y\lt\tilde y\mid1)=P\Big(u\lt\tfrac{\tilde y-1}{\sigma_1}\Big)=Q\Big(\tfrac{1-\tilde y}{\sigma_1}\Big)\]
(The same substitution as for the outage probability in lecture Ch 2 p.15.)''',
r'''<b>(b) Combine and check numerically</b>: both priors are ½:
\[P_e=\tfrac12\Big[Q\Big(\tfrac{1-\tilde y}{\sigma_1}\Big)+Q\Big(\tfrac{\tilde y}{\sigma_0}\Big)\Big]\]
Each term uses its own σ. Numerical example (σ₀ = √0.1 = 0.3162, σ₁ = √0.4 = 0.6325, ỹ = 0.460):
<div class="calc">ỹ/σ₀ = 0.460/0.3162 = 1.455 → Q(1.455) = 0.0728<br>(1 − ỹ)/σ₁ = 0.540/0.6325 = 0.854 → Q(0.854) = 0.1966<br>P<sub>e</sub> = ½(0.0728 + 0.1966) = 0.135</div>
For comparison, with the midpoint 0.5 as the threshold P<sub>e</sub> = ½[Q(1.581) + Q(0.791)] = ½(0.0569 + 0.2145) = 0.136, larger than with the ML threshold ✓ (the ML threshold is the one that minimises P<sub>e</sub>).''',
 ],
 'p3q3': [
r'''<b>List the data and the goal</b>: σ<sub>Tm</sub> = 3 µs = 3 × 10⁻⁶ s (rms delay spread), floor target P<sub>floor</sub> ≤ 10⁻³, modulation QPSK: M = 4, log₂4 = 2 bits per symbol. We want the highest data rate R<sub>b</sub> for which the floor does not exceed 10⁻³.''',
r'''<b>Replace T<sub>b</sub> in the formula by the symbol duration T<sub>s</sub></b>: the error floor comes from intersymbol interference (ISI), whose severity depends only on "how long the echo σ<sub>Tm</sub> is compared with one <b>symbol</b>", not on how many bits a symbol carries. For BPSK one symbol = 1 bit and T<sub>s</sub> = T<sub>b</sub>, which is why the question writes T<sub>b</sub>; for QPSK use
\[P_{floor}\approx\Big(\frac{\sigma_{T_m}}{T_s}\Big)^2\]
This formula is not in the main slides; the question gives it (lecture Ch 3 p.35 has the Doppler floor 0.5(πf<sub>D</sub>T<sub>b</sub>)²).''',
r'''<b>Take the square root</b>: both sides are positive, so "square ≤ 10⁻³" is the same as "ratio ≤ √10⁻³":
\[\begin{aligned}\Big(\frac{\sigma_{T_m}}{T_s}\Big)^2\le10^{-3}\;&\Rightarrow\;\frac{\sigma_{T_m}}{T_s}\le\sqrt{10^{-3}}\\&=10^{-1.5}=0.03162\end{aligned}\]''',
r'''<b>Solve for the shortest symbol duration</b>:
\[T_s\ge\frac{\sigma_{T_m}}{0.03162}=\frac{3\ \mu\text{s}}{0.03162}=94.87\ \mu\text{s}\]
Direction: a longer T<sub>s</sub> makes the echo a smaller fraction of the symbol and lowers the floor, so 94.87 µs is a lower limit on the symbol duration and gives an upper limit on the rate.''',
r'''<b>Convert to a bit rate</b>: the symbol rate is R<sub>s</sub> = 1/T<sub>s</sub>, and QPSK carries log₂4 = 2 bits per symbol:
\[\begin{aligned}R_s&=\frac{1}{94.87\ \mu\text{s}}=10.54\ \text{ksymbol/s}\\ R_b&=2R_s=2\times10.54=21.08\ \text{kbps}\end{aligned}\]
So R<sub>b</sub> ≤ 21.08 kbps. Under the same conditions BPSK carries 1 bit per symbol and gives only 10.54 kbps.''',
r'''<b>Self-check</b>: substituting back, (σ<sub>Tm</sub>/T<sub>s</sub>)² = (3/94.87)² = 0.03162² = 1.000 × 10⁻³, exactly the floor target ✓. σ<sub>Tm</sub>/T<sub>s</sub> = 0.032 &lt; 0.1, so the flat-fading rule (Practice 1 Q3) is also satisfied ✓.''',
 ],
 'p4q1': [
r'''<b>What it is</b>: macro-diversity connects <b>several base stations at different locations</b> to one mobile at the same time: the system keeps monitoring the signal level from each base station and uses the strongest one (or combines the signals of several) (lecture Ch 4 p.4). Why start with this: an explanation question first states what the technique is, so that the "why" has something to refer to.''',
r'''<b>Outage is mainly caused by shadowing</b>: outage means the SNR is below the threshold, \(P_{out}=P(\gamma\lt\gamma_{min})\) (p.3). What keeps the signal below the threshold <b>for a long time</b> is mainly shadowing (large-scale fading): buildings or terrain block the path between the mobile and the base station. Why shadowing: the signal stays low over tens to hundreds of metres and changes slowly, so the mobile cannot escape it by moving a little; multipath (small-scale) fading changes within a few wavelengths and lasts only briefly.''',
r'''<b>Different locations → nearly independent shadowing</b>: the base stations lie in different directions, so the paths from the mobile to them pass different obstacles; one path being blocked says little about the others, so the shadowing on the links is approximately independent. Why it must be different base stations: p.4 says significant shadowing variations occur only over large distances; several antennas on the same base station are only a few wavelengths apart and are blocked by the same building together (that is micro-diversity, which combats multipath, p.5).''',
r'''<b>Outage only if all links fail together → probabilities multiply</b>: using the strongest base station, the call survives as long as one link is strong enough, so outage occurs only when <b>all</b> links are below the threshold at the same time. For independent events the joint probability is the product of the individual probabilities (p.3):
\[\begin{aligned}P_{out,div}&=P(\gamma_1\lt\gamma_{min},\dots,\gamma_M\lt\gamma_{min})\\&=\prod_{i=1}^{M}P_{out,i}=P_{out}^M\end{aligned}\]
The last step assumes every link has the same outage probability. Each P<sub>out,i</sub> &lt; 1, so the product is smaller than the outage probability of any single link.''',
r'''<b>Numerical example</b>:
<div class="calc">one link P<sub>out</sub> = 10%: two independent base stations 0.1² = 1%, three 0.1³ = 0.1%<br>Practice 2 Q2 with margin Δ = σ: one base station Q(1) = 0.1587<br>two independent base stations [Q(1)]² = 0.1587² = 0.0252</div>
Without any extra transmit power the outage drops from 10% to 1% (or from 15.9% to 2.5%); this is the quantitative answer to "why it reduces outage".''',
r'''<b>Condition: correlated links reduce the benefit</b>: lecture p.21:
\[\begin{aligned}&P(\text{deep fade in }r_1\text{ and }r_2)\\&=P(\text{deep fade in }r_1\mid\text{deep fade in }r_2)\\&\quad\times P(\text{deep fade in }r_2)\\&\ge P(\text{deep fade in }r_1)\,P(\text{deep fade in }r_2)\end{aligned}\]
with equality when the links are uncorrelated. Reason: if the links are correlated, when one goes into a deep fade the other tends to as well, e.g. the mobile goes into a basement and all base stations become weak together. Practice 2 Q2(c): with a shadowing correlation of 0.5 (Δ = σ), 2.5% becomes 6.3%.''',
 ],
 'p4q2': [
r'''<b>(a) Values of γ and the mean SNR</b>: \(\gamma=\alpha P_T/\sigma_n^2\) with \(P_T=\sigma_n^2=1\) W, so γ = α: 8 (probability ⅓) or 11 (probability ⅔). These are linear values, not dB, so no conversion is needed; the probabilities sum to ⅓ + ⅔ = 1 ✓. Discrete expectation = Σ value × probability (Ch 1b p.10):
\[\bar\gamma=8\times\tfrac13+11\times\tfrac23=\tfrac{8+22}{3}=10\]''',
r'''<b>(a) Mean error probability</b>: under fading γ is a random variable, so the error probability must be averaged over the distribution of γ (lecture Ch 4 p.23, with the integral replaced by a sum): \(\bar P_s=E\big[\tfrac12e^{-\gamma}\big]=\sum_k\tfrac12e^{-\gamma_k}p_k\).
<div class="calc">e⁻⁸ = 3.355 × 10⁻⁴, e⁻¹¹ = 1.670 × 10⁻⁵<br>P̄<sub>s</sub> = ⅓ × ½ × 3.355 × 10⁻⁴ + ⅔ × ½ × 1.670 × 10⁻⁵<br>= 5.59 × 10⁻⁵ + 0.56 × 10⁻⁵ = 6.15 × 10⁻⁵</div>
Do not substitute γ̄ into the formula: ½e⁻¹⁰ = 2.27 × 10⁻⁵ is 2.7 times too small (E[f(γ)] ≠ f(E[γ]); most errors happen when γ = 8).''',
r'''<b>(b) MRC output SNR: tabulate the combinations</b>: the maximal ratio combining (MRC) output SNR is the sum of the branch SNRs, γ<sub>Σ</sub> = γ₁ + γ₂ (lecture p.16: \(\gamma_{MRC}=\sum_iA_i^2E_b/N_0\)). The branches are independent, so the joint probabilities multiply; 19 arises in two orders, (8, 11) and (11, 8):
<div class="tw"><table class="mini"><thead><tr><th>(γ₁, γ₂)</th><th>γ<sub>Σ</sub></th><th>probability</th></tr></thead><tbody>
<tr><td>(8, 8)</td><td>16</td><td>⅓ × ⅓ = 1/9</td></tr>
<tr><td>(8, 11), (11, 8)</td><td>19</td><td>2 × ⅓ × ⅔ = 4/9</td></tr>
<tr><td>(11, 11)</td><td>22</td><td>⅔ × ⅔ = 4/9</td></tr>
</tbody></table></div>
The probabilities sum to (1 + 4 + 4)/9 = 1 ✓.''',
r'''<b>(b) Mean output SNR and mean error probability</b>: weight both by the table:
<div class="calc">γ̄<sub>Σ</sub> = (16 × 1 + 19 × 4 + 22 × 4)/9 = 180/9 = 20<br>e⁻¹⁶ = 1.125 × 10⁻⁷, e⁻¹⁹ = 5.603 × 10⁻⁹, e⁻²² = 2.790 × 10⁻¹⁰<br>½ × 1/9 × e⁻¹⁶ = 6.25 × 10⁻⁹<br>½ × 4/9 × e⁻¹⁹ = 1.25 × 10⁻⁹<br>½ × 4/9 × e⁻²² = 0.06 × 10⁻⁹<br>P̄<sub>s</sub> = (6.25 + 1.25 + 0.06) × 10⁻⁹ = 7.56 × 10⁻⁹</div>
Checks: γ̄<sub>Σ</sub> = 2γ̄ = 20 ✓ (expectations add); shortcut ½(E[e<sup>−γ</sup>])² = ½(2 × 6.15 × 10⁻⁵)² = ½(1.23 × 10⁻⁴)² = 7.56 × 10⁻⁹ ✓.''',
r'''<b>(b) Array gain g and diversity gain d</b>: definitions (lecture p.27, to be memorised) \(g=\bar\gamma_\Sigma/\bar\gamma\), \(d=-\log_{10}\bar P_s/\log_{10}\bar\gamma\); γ̄ is the mean SNR at the combiner <b>input</b> (one branch), 10, not the output 20:
<div class="calc">g = 20/10 = 2 (10 log₁₀2 = 3.01 dB)<br>log₁₀(7.56 × 10⁻⁹) = log₁₀7.56 − 9 = 0.879 − 9 = −8.121<br>d = 8.121/log₁₀10 = 8.121/1 = 8.1</div>
The formula for d comes from \(\bar P_s\approx\bar\gamma^{-d}\) at high SNR, taking log₁₀ of both sides.''',
r'''<b>(c) Mean SNR and g</b>: expectation is linear, so sharing β does not change the means:
<div class="calc">E[r] = 0.6 × ⅓ + 1.2 × ⅔ = 0.2 + 0.8 = 1<br>E[β] = 7 × ⅓ + 10 × ⅔ = 2.333 + 6.667 = 9<br>E[γ<sub>i</sub>] = E[r<sub>i</sub>] + E[β] = 1 + 9 = 10</div>
γ̄<sub>Σ</sub> = E[γ₁] + E[γ₂] = 20 and g = 20/10 = 2, the same as in (b).''',
r'''<b>(c) Split the exponential into independent factors</b>: \(\gamma_\Sigma=r_1+r_2+2\beta\) (β is common to both branches, so it appears twice). \(e^{-\gamma_\Sigma}=e^{-r_1}e^{-r_2}e^{-2\beta}\), and r₁, r₂, β are independent, so the expectation splits into a product (Ch 1b p.10: E[g(X)h(Y)] = E[g(X)]E[h(Y)]):
<div class="calc">E[e<sup>−r</sup>] = ⅓e<sup>−0.6</sup> + ⅔e<sup>−1.2</sup> = ⅓ × 0.5488 + ⅔ × 0.3012<br>= 0.1829 + 0.2008 = 0.3837<br>E[e<sup>−2β</sup>] = ⅓e⁻¹⁴ + ⅔e⁻²⁰<br>= ⅓ × 8.315 × 10⁻⁷ + ⅔ × 2.061 × 10⁻⁹<br>= 2.772 × 10⁻⁷ + 0.014 × 10⁻⁷ = 2.786 × 10⁻⁷<br>P̄<sub>s</sub> = ½ × 0.3837² × 2.786 × 10⁻⁷<br>= ½ × 0.1472 × 2.786 × 10⁻⁷ = 2.05 × 10⁻⁸</div>''',
r'''<b>(c) Diversity gain and comparison with (b)</b>:
<div class="calc">log₁₀(2.05 × 10⁻⁸) = log₁₀2.05 − 8 = 0.312 − 8 = −7.688<br>d = 7.688/1 = 7.7</div>
Check (fix β first, the lecturer's method): for β = 7, ½ × 0.1472 × e⁻¹⁴ = 6.12 × 10⁻⁸; for β = 10, ½ × 0.1472 × e⁻²⁰ = 1.52 × 10⁻¹⁰; weighted, ⅓ × 6.12 × 10⁻⁸ + ⅔ × 1.52 × 10⁻¹⁰ = 2.05 × 10⁻⁸ ✓. The mean SNR and g are the same as in (b), but P̄<sub>s</sub> is 2.05/0.756 = 2.7 times larger and d drops from 8.1 to 7.7: 99.5% of the errors occur when β = 7 and both branches are poor together (shared shadowing weakens diversity, lecture p.21).''',
 ],
 'p4q3': [
r'''<b>(a) Consider only b = +1</b>: b = ±1 are equally likely, \(P_b=\tfrac12P(\text{error}\mid b=+1)+\tfrac12P(\text{error}\mid b=-1)\). For b = −1 the distribution of z is the mirror image about 0 of the one for b = +1 (α is Gaussian, symmetric about α₀, and −w has the same distribution as w), so the two terms are equal and \(P_b=P(z\le0\mid b=+1)\).''',
r'''<b>(a) Mean and variance of the decision variable</b>: with M = 1 and b = +1, \(z=y=\alpha\sqrt E+w\). Use the rules of Ch 1b p.10–11, E[aX] = aE[X] and V(aX) = a²V(X); α and w are independent, so both means and variances add:
\[\begin{aligned}E[z]&=\sqrt E\,E[\alpha]+E[w]=\alpha_0\sqrt E\\ \mathrm{Var}(z)&=(\sqrt E)^2\sigma_1^2+\sigma_2^2=\sigma_1^2E+\sigma_2^2\end{aligned}\]
A sum of independent Gaussians is Gaussian, so \(z\sim\mathcal N(\alpha_0\sqrt E,\ \sigma_1^2E+\sigma_2^2)\).''',
r'''<b>(a) Standardise and write it as Q</b>: let \(u=\dfrac{z-\alpha_0\sqrt E}{\sqrt{\sigma_1^2E+\sigma_2^2}}\sim\mathcal N(0,1)\). Then z ≤ 0 ⇔ \(u\le-\dfrac{\alpha_0\sqrt E}{\sqrt{\sigma_1^2E+\sigma_2^2}}\), and by symmetry P(u ≤ −a) = Q(a) (the same substitution as Ch 2 p.15):
\[P_b=Q\!\left(\frac{\alpha_0\sqrt E}{\sqrt{\sigma_1^2E+\sigma_2^2}}\right)\]
i.e. Q(mean / standard deviation).''',
r'''<b>(b) Write the combined decision variable</b>: equal-weight combining gives every branch weight 1 and simply adds them (this is not the EGC of lecture p.19, which first rotates each branch by its phase; here all branches are real):
\[z=\sum_{k=1}^My_k=b\sqrt E\sum_{k=1}^M\alpha_k+\sum_{k=1}^Mw_k\]
The standard solution assumes the α<sub>k</sub> of different antennas are independent, and the w<sub>k</sub> are independent too.''',
r'''<b>(b) Mean and variance</b>: b = +1, a sum of 2M independent Gaussians:
\[\begin{aligned}E[z]&=\textstyle\sum_k\alpha_0\sqrt E=M\alpha_0\sqrt E\\ \mathrm{Var}(z)&=M\sigma_1^2E+M\sigma_2^2\\&=M(\sigma_1^2E+\sigma_2^2)\end{aligned}\]
Standard deviation \(=\sqrt M\,\sqrt{\sigma_1^2E+\sigma_2^2}\): the mean grows by M, the standard deviation only by √M.''',
r'''<b>(b) Write it as Q and simplify</b>: as in (a), P<sub>b</sub> = Q(mean / standard deviation); then use M/√M = √M:
\[\begin{aligned}P_b&=Q\!\left(\frac{M\alpha_0\sqrt E}{\sqrt{M(\sigma_1^2E+\sigma_2^2)}}\right)\\&=Q\!\left(\frac{\sqrt M\,\alpha_0\sqrt E}{\sqrt{\sigma_1^2E+\sigma_2^2}}\right)\end{aligned}\]''',
r'''<b>Self-check</b>: ① M = 1 gives back (a) ✓. ② Numerical example α₀ = 1, E = 1, σ₁² = σ₂² = 0.1: argument = √M × 1/√0.2 = 2.236√M:
<div class="calc">M = 1: Q(2.236) = 0.0127<br>M = 2: Q(3.162) = 7.8 × 10⁻⁴<br>M = 4: Q(4.472) = 3.9 × 10⁻⁶</div>
The error probability falls faster as M grows, so combining helps ✓.''',
 ],
}

IDEA = {}
