# English expanded steps for group g1: p1q1, p1q2, p1q3 (prac_1.html), p2q1, p2q2, p2q3 (prac_2.html).
# Same steps, formulas and numbers as the Chinese sol-zh steps. Merged into sol_en.py by the main session.

# Identical to RESID_TABLE in src/p2build/sol_en.py (kept inside the p1q1 residual step).
RESID_TABLE = r'''<div class="tw"><table class="mini"><thead><tr><th>d (m)</th><th>\(x_i\)</th><th>\(\gamma x_i\)</th><th>prediction \(\hat y_i\)</th><th>measured \(M_i\)</th><th>residual \(e_i\)</th><th>\(e_i^2\)</th></tr></thead><tbody>
            <tr><td>5</td><td>6.99</td><td>27.54</td><td>−58.33</td><td>−60</td><td>−1.67</td><td>2.78</td></tr>
            <tr><td>25</td><td>13.98</td><td>55.09</td><td>−85.88</td><td>−80</td><td>+5.88</td><td>34.53</td></tr>
            <tr><td>65</td><td>18.13</td><td>71.44</td><td>−102.23</td><td>−105</td><td>−2.77</td><td>7.68</td></tr>
            <tr><td>110</td><td>20.41</td><td>80.44</td><td>−111.23</td><td>−115</td><td>−3.77</td><td>14.20</td></tr>
            <tr><td>400</td><td>26.02</td><td>102.53</td><td>−133.32</td><td>−130</td><td>+3.32</td><td>11.05</td></tr>
            <tr><td>1000</td><td>30.00</td><td>118.22</td><td>−149.01</td><td>−150</td><td>−0.99</td><td>0.99</td></tr>
          </tbody></table></div>'''

STEPS = {

'p1q1': [
r'''<b>(a) Turn the model into a straight line</b>: take 10 log₁₀ of both sides (d₀ = 1 m, Ch 2 p.8, p.12):
\[\begin{aligned}M=\Big(\frac{P_r}{P_t}\Big)_{dB}&=K_{dB}-\gamma\cdot10\log_{10}d\\&=K_{dB}-\gamma\,x,\qquad x=10\log_{10}d\end{aligned}\]
With x on the horizontal axis and the measured M on the vertical axis, the 6 points should lie close to a straight line with intercept \(K_{dB}\) and slope \(-\gamma\). First convert the distances (in metres) to x:
<div class="calc">10 log₁₀5 = 6.99, 10 log₁₀25 = 13.98<br>10 log₁₀65 = 18.13, 10 log₁₀110 = 20.41<br>10 log₁₀400 = 26.02, 10 log₁₀1000 = 30.00</div>''',

r'''<b>(a) The four sums</b>: least squares needs only these four sums (a calculator's statistics mode gives them directly); also find the two means:
<div class="calc">Σx = 115.53, Σx² = 2566.75<br>ΣM = −640, ΣxM = −13671.57<br>x̄ = 115.53 / 6 = 19.26<br>M̄ = −640 / 6 = −106.67</div>''',

r'''<b>(a) Normal equations for γ</b>: least squares minimises the sum of squared errors \(F=\sum_i(M_i-K_{dB}+\gamma x_i)^2\) (Ch 2 p.13: minimise the MSE between measured and model path loss). Setting \(\partial F/\partial K=0\) and \(\partial F/\partial\gamma=0\) (the normal equations) gives \(K_{dB}=\bar M+\gamma\bar x\) and \(\gamma=-S_{xM}/S_{xx}\):
\[\begin{aligned}S_{xx}&=\textstyle\sum x^2-(\sum x)^2/6\\&=2566.75-2224.64=342.11\\ S_{xM}&=\textstyle\sum xM-\sum x\sum M/6\\&=-13671.57+12323.49\\&=-1348.08\end{aligned}\]
\[\gamma=-\frac{S_{xM}}{S_{xx}}=\frac{1348.08}{342.11}=3.94\]
\(S_{xx}=\sum(x_i-\bar x)^2\) and \(S_{xM}=\sum(x_i-\bar x)(M_i-\bar M)\); the expanded forms above are easier on a calculator. The slope is −3.94, so γ = +3.94.''',

r'''<b>(a) Intercept K</b>: from \(\partial F/\partial K=0\), the best line always passes through the mean point \((\bar x,\bar M)\):
\[\begin{aligned}K_{dB}&=\bar M+\gamma\bar x\\&=-106.67+3.94\times19.26\\&=-106.67+75.88=-30.79\approx-30.8\ \text{dB}\end{aligned}\]
γ = 3.94 lies in the 3.7–6.5 range for urban macro-cells in the table on Ch 2 p.9, so it is reasonable.''',

r'''<b>(b) Residuals → shadowing variance</b>: residual \(e_i=M_i-\hat y_i\): first compute the fitted prediction \(\hat y_i=K_{dB}-\gamma x_i=-30.79-3.94\,x_i\), then subtract it from the measurement \(M_i\).''' + RESID_TABLE
+ r'''\(\sum e_i^2=71.23\), so the MSE is \(\sigma_\psi^2=71.23/6=11.87\) and \(\sigma_\psi=3.45\) dB. (Least-squares residuals always sum to 0, a quick arithmetic check.)
Row example (d = 5 m): \(\hat y_1=-30.79-27.54=-58.33\), \(e_1=-60-(-58.33)=-1.67\), \(e_1^2=2.78\). Why the MSE is the shadowing variance: Ch 2 p.13 defines the error \(X_i\) (measured − model) and sets its mean square \(E[X_i^2]=\sigma_\psi^2\), so divide by n = 6 (not 5), as in the definition.''',

r'''<b>(b) Write the outage probability</b>: the mean received power from path loss alone is 10 dB above the minimum required power, i.e. the margin is x = 10 dB. Outage means shadowing pulls the power down by more than 10 dB (Ch 2 p.14–15):
\[\begin{aligned}P_{out}&=P\big(P_{r,dB}\lt P_{m,dB}\big)\\&=P\big(\psi_{dB}\lt-10\big)=Q\Big(\frac{10}{\sigma_\psi}\Big)\end{aligned}\]
Last step: divide by \(\sigma_\psi\) to standardise, then use the symmetry of the Gaussian, P(N &lt; −a) = P(N &gt; a) = Q(a). Use the margin in dB directly; do not convert it to linear.''',

r'''<b>(b) Substitute and look up Q</b>: the MSE is a variance, so take the square root before putting it in Q:
<div class="calc">σ<sub>ψ</sub> = √11.87 = 3.45 dB<br>10 / σ<sub>ψ</sub> = 10 / 3.45 = 2.90<br>P<sub>out</sub> = Q(2.90) ≈ 1.85 × 10⁻³ (about 0.19%)</div>
A two-decimal Q table gives Q(2.90) = 1.87 × 10⁻³; 1.85 × 10⁻³ uses the unrounded 10/3.446 = 2.902. The difference is only rounding.''',

r'''<b>Check</b>: ① the residuals sum to −1.67 + 5.88 − 2.77 − 3.77 + 3.32 − 0.99 = 0 ✓ (a property of least squares); ② the line passes through the mean point: −30.79 − 3.94 × 19.26 = −106.67 = M̄ ✓; ③ order of magnitude: a 10 dB margin is about 2.9σ, a little less than the 3.09σ for Q(3.09) = 10⁻³, so the outage is a little above 10⁻³ ✓.''',
],

'p1q2': [
r'''<b>Model (standardise)</b>: log-normal means the value in dBm is Gaussian, \(P_r\sim\mathcal N(\mu_\psi,\sigma_\psi^2)\). Shadowing is a product of many obstruction losses; the logarithm turns the product into a sum, so it is Gaussian in dB (Ch 2 p.11). Outage means below 10 dBm; subtract the mean and divide by the standard deviation (Ch 2 p.14–15):
\[\begin{aligned}P_{out}&=P(P_r\lt10)=P\Big(N\lt\frac{10-\mu_\psi}{\sigma_\psi}\Big)\\&=Q\Big(\frac{\mu_\psi-10}{\sigma_\psi}\Big)\end{aligned}\]
N ~ N(0, 1); the last step uses the symmetry P(N &lt; −a) = Q(a). The numerator μ<sub>ψ</sub> − 10 is the margin; the difference of two dBm values is in dB.''',

r'''<b>(a) Substitute</b>: μ<sub>ψ</sub> = 15 dBm, σ<sub>ψ</sub> = 8 dB:
\[P_{out}=Q\Big(\frac{15-10}{8}\Big)=Q\Big(\frac{5}{8}\Big)=Q(0.625)\]
The threshold is 5 dB below the mean, i.e. 0.625 standard deviations.''',

r'''<b>(a) Look up the Q table</b>: the table has two decimals, so take the value halfway between Q(0.62) = 0.2676 and Q(0.63) = 0.2643:
<div class="calc">Q(0.625) ≈ (0.2676 + 0.2643) / 2 = 0.266 ≈ 26.6%</div>
Sanity check: with zero margin Q(0) = 0.5, with a 1σ margin Q(1) = 0.159; 0.625σ lies in between ✓.''',

r'''<b>(b) Set up the inequality and invert Q</b>: σ<sub>ψ</sub> = 4 dB and μ<sub>ψ</sub> is the unknown:
\[Q\Big(\frac{\mu_\psi-10}{4}\Big)\lt0.01\]
From the table, Q(2.32) = 0.0102 and Q(2.33) = 0.0099, so \(Q^{-1}(0.01)=2.326\). Q is decreasing, so "Q value &lt; 0.01" becomes "argument &gt; 2.326":
\[\frac{\mu_\psi-10}{4}\gt2.326\]''',

r'''<b>(b) Solve for μ</b>: multiply both sides by 4, then add 10:
\[\begin{aligned}\mu_\psi&\gt10+4\times2.326\\&=10+9.30=19.3\ \text{dBm}\end{aligned}\]
The required margin is 9.3 dB = 2.326σ. The official 19.32 uses Q⁻¹(0.01) ≈ 2.33: 10 + 4 × 2.33 = 19.32, so the two agree.''',

r'''<b>Check</b>: substitute μ<sub>ψ</sub> = 19.3 dBm back: (19.3 − 10)/4 = 2.325, Q(2.325) ≈ 0.0100, exactly on the 1% boundary ✓. Compare with (a): a margin of only 0.625σ gives 26.6% outage; to bring it down to 1% the margin must grow to 2.326σ (here 9.3 dB).''',
],

'p1q3': [
r'''<b>(a) Denominator (total power)</b>: \(\mu_{T_m}\) and \(\sigma_{T_m}\) on Ch 2 p.30 are both averages weighted by \(P_r(\tau)\), so first compute the denominator (τ in µs):
\[\int_0^{10}P_r(\tau)\,d\tau=\int_0^{10}1\,d\tau=10\]
\(P_r(\tau)=1\) is not normalised, so every integral below is divided by 10. This is the same as treating it as a uniform distribution on 0–10 µs.''',

r'''<b>(a) Mean delay</b>:
\[\begin{aligned}\mu_{T_m}&=\frac{\int_0^{10}\tau\,d\tau}{10}=\frac{[\tau^2/2]_0^{10}}{10}\\&=\frac{50}{10}=5\ \mu s\end{aligned}\]
A uniform distribution is symmetric, so the mean is in the middle, 10/2 = 5 µs ✓.''',

r'''<b>(a) Second moment</b>: with the same weight \(P_r(\tau)\), find \(E[\tau^2]\):
\[\begin{aligned}E[\tau^2]&=\frac{\int_0^{10}\tau^2d\tau}{10}=\frac{[\tau^3/3]_0^{10}}{10}\\&=\frac{1000/3}{10}=33.33\ \mu s^2\end{aligned}\]''',

r'''<b>(a) rms delay spread</b>: the slide definition is \(\sigma_{T_m}^2=\frac{\int(\tau-\mu_{T_m})^2P_r\,d\tau}{\int P_r\,d\tau}\); expanding the square gives "second moment − mean²":
\[\begin{aligned}\sigma_{T_m}^2&=E[\tau^2]-\mu_{T_m}^2\\&=33.33-5^2=8.33\ \mu s^2\\ \sigma_{T_m}&=\sqrt{8.33}=2.89\ \mu s\end{aligned}\]
The rms delay spread is a standard deviation, so take the square root.''',

r'''<b>(a) Check</b>: integrate directly with the slide definition:
\[\begin{aligned}\int_0^{10}(\tau-5)^2d\tau&=\Big[\tfrac{(\tau-5)^3}{3}\Big]_0^{10}\\&=\tfrac{125}{3}+\tfrac{125}{3}=83.33\end{aligned}\]
83.33 / 10 = 8.33 µs² ✓. Shortcut: the standard deviation of a uniform distribution on [0, a] is a/√12 = 10/3.464 = 2.89 µs ✓.''',

r'''<b>(b) Flat-fading condition</b>: the rule of thumb on Ch 2 p.33 is flat fading when \(\sigma_{T_m}/T_s\lt0.1\), i.e. the delay spread is at most a tenth of the symbol duration, so there is no ISI:
\[\begin{aligned}\frac{\sigma_{T_m}}{T_s}\lt0.1\;&\Rightarrow\;T_s\gt10\,\sigma_{T_m}\\&=10\times2.887=28.87\ \mu s\end{aligned}\]''',

r'''<b>(b) Convert to symbol rate</b>: \(R_s=1/T_s\); longer symbols mean a lower rate, so the inequality flips; 1 µs = 10⁻⁶ s:
\[\begin{aligned}R_s&\lt\frac{1}{28.87\times10^{-6}\ \text{s}}\\&=34\,641\ \text{sym/s}\approx34.6\ \text{ksps}\end{aligned}\]
Check: at R<sub>s</sub> = 34.6 ksps, T<sub>s</sub> = 28.9 µs and σ/T<sub>s</sub> = 2.89/28.9 = 0.1, exactly on the boundary ✓. The answer is an upper limit, not an equality.''',
],

'p2q1': [
r'''<b>Parameters</b>: maximum Doppler shift f<sub>D</sub> = 50 Hz; ρ = Z<sub>min</sub>/Z<sub>rms</sub> (Ch 2 p.41). "Signal strength" is an <b>amplitude</b>, so "0.1 of the rms value" means ρ = 0.1. In dB: 20 log₁₀0.1 = −20 dB, i.e. a power ratio ρ² = 0.01.''',

r'''<b>Numerator</b>: square first, then take the exponential:
\[\begin{aligned}\rho^2&=0.1^2=0.01\\ e^{\rho^2}-1&=1.01005-1=0.01005\end{aligned}\]
Where it comes from (Ch 2 p.43): AFD = P(z &lt; Z<sub>min</sub>) / L<sub>Z</sub>; for Rayleigh fading P(z &lt; Z<sub>min</sub>) = 1 − e<sup>−ρ²</sup> and L<sub>Z</sub> = √(2π) f<sub>D</sub> ρ e<sup>−ρ²</sup>; dividing top and bottom by e<sup>−ρ²</sup> gives the numerator e<sup>ρ²</sup> − 1. For small x, e<sup>x</sup> − 1 ≈ x, so it is about 0.01.''',

r'''<b>Denominator</b>:
\[\begin{aligned}\sqrt{2\pi}\,f_D\,\rho&=\sqrt{6.2832}\times50\times0.1\\&=2.5066\times5=12.53\ \text{s}^{-1}\end{aligned}\]
f<sub>D</sub> is in Hz = 1/s, so the denominator is in 1/s and the result of the division is in seconds.''',

r'''<b>Divide</b>:
\[\begin{aligned}AFD&=\frac{e^{\rho^2}-1}{\sqrt{2\pi}\,f_D\,\rho}=\frac{0.01005}{12.53\ \text{s}^{-1}}\\&=8.02\times10^{-4}\ \text{s}\approx0.8\ \text{ms}\end{aligned}\]
Meaning: each time the signal drops below 0.1 of its rms value, it takes on average 0.8 ms to come back above the threshold.''',

r'''<b>Check</b>: verify with the LCR (Ch 2 p.41):
<div class="calc">LCR = √(2π) f<sub>D</sub> ρ e<sup>−ρ²</sup> = 12.53 × 0.99005 = 12.41 crossings/s<br>AFD × LCR = 8.02 × 10⁻⁴ × 12.41 = 0.00995<br>1 − e<sup>−0.01</sup> = 0.00995 ✓</div>
About 12 fades per second, each about 0.8 ms long, add up to about 1% of the time below the threshold, which is exactly the Rayleigh P(z &lt; Z<sub>min</sub>). The small-ρ approximation AFD ≈ ρ/(√(2π) f<sub>D</sub>) = 0.1/125.3 = 7.98 × 10⁻⁴ s agrees too ✓.''',
],

'p2q2': [
r'''<b>(a) Interpret the terms</b>: W: the <b>mean received power</b> (dBm) due to path loss alone; the mean path loss to the two base stations is the same, so both links share the same W. \(Z_1,Z_2\): the <b>shadowing</b> components (dB) of the two links. Shadowing in dB is zero-mean Gaussian (Ch 2 p.11–12), so \(Z_i\sim\mathcal N(0,\sigma^2)\) and \(E[P_{r,i}]=W\).''',

r'''<b>(b) Write outage as a condition on Z</b>: the threshold is T = W − Δ, so for each link
\[\begin{aligned}P_{r,i}\lt T&\iff W+Z_i\lt W-\Delta\\&\iff Z_i\lt-\Delta\end{aligned}\]
The phone can use either base station (macroscopic diversity, Ch 4 p.4), so outage happens only when <b>both</b> links are below T: \(P_{out}=P(Z_1\lt-\Delta\ \text{and}\ Z_2\lt-\Delta)\).''',

r'''<b>(b) One link → multiply (independent)</b>: divide by σ to standardise, then use the symmetry of the Gaussian:
\[\begin{aligned}P(Z_i\lt-\Delta)&=P\Big(\frac{Z_i}{\sigma}\lt-\frac{\Delta}{\sigma}\Big)\\&=P\Big(N\gt\frac{\Delta}{\sigma}\Big)=Q\Big(\frac{\Delta}{\sigma}\Big)\end{aligned}\]
\(Z_1,Z_2\) are independent, so the probability that both happen is the product:
\[P_{out}=Q\Big(\frac{\Delta}{\sigma}\Big)\cdot Q\Big(\frac{\Delta}{\sigma}\Big)=\Big[Q\Big(\frac{\Delta}{\sigma}\Big)\Big]^2\]
For a feel of the numbers: with Δ = σ, one base station gives Q(1) = 0.159 and two give 0.159² = 0.025 (Ch 4 p.3: M independent branches give \(P_{out}^M\)).''',

r'''<b>(c) Why we cannot just square</b>: both links contain the same bY. Y, Y₁, Y₂ are independent with zero mean, so every cross term has zero expectation:
\[\begin{aligned}\operatorname{Cov}(Z_1,Z_2)&=E[(aY_1+bY)(aY_2+bY)]\\&=b^2E[Y^2]=b^2\sigma^2\neq0\end{aligned}\]
So Z₁ and Z₂ are correlated and \(P(A\cap B)\neq P(A)P(B)\). (To be consistent with \(Z_i\sim\mathcal N(0,\sigma^2)\) we need \(a^2+b^2=1\); the correlation coefficient is then b².) Trick: <b>fix the shared Y first</b> (conditioning).''',

r'''<b>(c) Fix Y</b>: to match the form of the answer, let \(Y=\sigma u\) with \(u\sim\mathcal N(0,1)\). Given u, \(b\sigma u\) is just a constant shift and the only random part is \(aY_i\sim\mathcal N(0,a^2\sigma^2)\) (standard deviation \(|a|\sigma\)):
\[Z_i\mid u\ \sim\ \mathcal N\big(b\sigma u,\ a^2\sigma^2\big)\]
Given u, Z₁ depends only on Y₁ and Z₂ only on Y₂, so the two are <b>conditionally independent</b>.''',

r'''<b>(c) Conditional outage</b>: for one link, standardise as in (b):
\[\begin{aligned}P(Z_i\lt-\Delta\mid u)&=P\big(aY_i\lt-(\Delta+b\sigma u)\big)\\&=Q\Big(\frac{\Delta+b\sigma u}{|a|\sigma}\Big)\end{aligned}\]
Conditionally independent → multiply:
\[P(\text{outage}\mid u)=\Big[Q\Big(\frac{\Delta+b\sigma u}{|a|\sigma}\Big)\Big]^2\]
The more negative u (the deeper the common shadow), the smaller the argument of Q and the larger Q: outage becomes more likely.''',

r'''<b>(c) Average with the total probability theorem</b>: \(P(A)=\int P(A\mid u)\,f_U(u)\,du\), with the density of u \(f_U(u)=\frac{1}{\sqrt{2\pi}}e^{-u^2/2}\):
\[\begin{aligned}P_{out}&=\int_{-\infty}^{\infty}P(\text{outage}\mid u)\,f_U(u)\,du\\&=\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}\Big[Q\Big(\frac{\Delta+b\sigma u}{|a|\sigma}\Big)\Big]^2\\&\qquad\times e^{-u^2/2}\,du\end{aligned}\]
Renaming the integration variable u to y gives the question's expression (its \(Q[\cdot]^2\) means \([Q(\cdot)]^2\)). If you integrate over Y = y directly, \(f_Y\) has an extra 1/σ, which cancels after substituting y = σu, dy = σ du; the result is the same.''',

r'''<b>Check</b>: ① b = 0 (no common shadowing, a = 1): Q no longer depends on u and comes out of the integral, \(\int\frac{1}{\sqrt{2\pi}}e^{-u^2/2}du=1\), giving \([Q(\Delta/\sigma)]^2\), part (b) ✓; ② a → 0 (fully shared, b = 1): Q → 1 for u &lt; −Δ/σ and Q → 0 otherwise, so \(P_{out}=P(u\lt-\Delta/\sigma)=Q(\Delta/\sigma)\), the same as one base station: no diversity ✓.''',
],

'p2q3': [
r'''<b>Formula and data</b>: Shannon capacity (Ch 2 p.48) \(C=B\log_2(1+\gamma)\) with γ as a <b>linear</b> ratio. With interference treated as noise, γ becomes the SINR (Ch 1a p.16):
\[\text{SINR}=\frac{P}{N+I}\]
Data (all powers in mW): P₁ = P₂ = 10 mW, N = 0.1 mW; B = 20 MHz = 20 × 10⁶ Hz.''',

r'''<b>(a) SINR of user 1</b>: when user 1 is decoded first, user 2 is still transmitting; the question says it behaves like AWGN, so it joins the noise (interference I = P₂):
\[\text{SINR}_1=\frac{P_1}{P_2+N}=\frac{10}{10+0.1}=\frac{10}{10.1}=0.990\]
This is a linear value (about −0.04 dB), not dB.''',

r'''<b>(a) Capacity</b>: \(\log_2x=\log_{10}x/\log_{10}2\) with \(\log_{10}2=0.30103\):
\[\begin{aligned}\log_2 1.990&=\frac{\log_{10}1.990}{0.30103}=\frac{0.2989}{0.30103}\\&=0.993\\ C_1&=20\times10^6\times0.993\\&=19.86\times10^6\ \text{bit/s}=19.86\ \text{Mbps}\end{aligned}\]''',

r'''<b>(b) SNR of user 2</b>: MUD has decoded user 1 and removed it completely from the received signal, so only thermal noise is left when user 2 is decoded:
\[\text{SNR}_2=\frac{P_2}{N}=\frac{10}{0.1}=100\quad(=20\ \text{dB})\]''',

r'''<b>(b) Capacity</b>:
\[\begin{aligned}\log_2 101&=\frac{\log_{10}101}{0.30103}=\frac{2.0043}{0.30103}\\&=6.658\\ C_2&=20\times10^6\times6.658\\&=133.16\ \text{Mbps}\end{aligned}\]
Dividing by 0.301 gives 6.659 and 133.18 Mbps; keep more digits (0.30103) or use the calculator's log₂ to match the official 133.16.''',

r'''<b>Check</b>: the sum of the two capacities
\[\begin{aligned}C_1+C_2&=19.86+133.16=153.02\ \text{Mbps}\\&=20\log_2\Big(1+\frac{10+10}{0.1}\Big)\\&=20\times\log_2 201=20\times7.651\end{aligned}\]
20 × 7.651 = 153.02 ✓: with successive interference cancellation, the sum capacity equals the single-user capacity with the two powers combined. (b) is much larger than (a) because user 2 no longer faces 10 mW of interference, only 0.1 mW of noise.''',
],

}

IDEA = {}
