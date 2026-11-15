"""English versions of the practice-page solutions and knowledge points (used by add_en.py).

Each entry: idea (optional), steps, ans, official, note (optional), kp = [(label, html), ...].
Numbers are the same as the Chinese solutions (verified earlier); keep the two in sync when editing.
"""

def C(x):
    return f'<div class="calc">{x}</div>'

RESID_TABLE = r'''<div class="tw"><table class="mini"><thead><tr><th>d (m)</th><th>\(x_i\)</th><th>\(\gamma x_i\)</th><th>prediction \(\hat y_i\)</th><th>measured \(M_i\)</th><th>residual \(e_i\)</th><th>\(e_i^2\)</th></tr></thead><tbody>
            <tr><td>5</td><td>6.99</td><td>27.54</td><td>−58.33</td><td>−60</td><td>−1.67</td><td>2.78</td></tr>
            <tr><td>25</td><td>13.98</td><td>55.09</td><td>−85.88</td><td>−80</td><td>+5.88</td><td>34.53</td></tr>
            <tr><td>65</td><td>18.13</td><td>71.44</td><td>−102.23</td><td>−105</td><td>−2.77</td><td>7.68</td></tr>
            <tr><td>110</td><td>20.41</td><td>80.44</td><td>−111.23</td><td>−115</td><td>−3.77</td><td>14.20</td></tr>
            <tr><td>400</td><td>26.02</td><td>102.53</td><td>−133.32</td><td>−130</td><td>+3.32</td><td>11.05</td></tr>
            <tr><td>1000</td><td>30.00</td><td>118.22</td><td>−149.01</td><td>−150</td><td>−0.99</td><td>0.99</td></tr>
          </tbody></table></div>'''

EN = {}

# ================================================================ Practice 1
EN['p1q1'] = dict(
 idea=r'''In dB the model is a straight line \(y=K_{dB}-\gamma x\) with \(x=10\log_{10}d\) (\(d_0\) = 1 m). Least squares finds the line closest to the 6 points; the remaining mean squared error is the shadowing variance.''',
 steps=[
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
  r'''<b>(b) Residuals → shadowing variance</b>: residual \(e_i=M_i-\hat y_i\): first compute the fitted prediction \(\hat y_i=K_{dB}-\gamma x_i=-30.79-3.94\,x_i\), then subtract it from the measurement \(M_i\).<div class="tw"><table class="mini"><thead><tr><th>d (m)</th><th>\(x_i\)</th><th>\(\gamma x_i\)</th><th>prediction \(\hat y_i\)</th><th>measured \(M_i\)</th><th>residual \(e_i\)</th><th>\(e_i^2\)</th></tr></thead><tbody>
            <tr><td>5</td><td>6.99</td><td>27.54</td><td>−58.33</td><td>−60</td><td>−1.67</td><td>2.78</td></tr>
            <tr><td>25</td><td>13.98</td><td>55.09</td><td>−85.88</td><td>−80</td><td>+5.88</td><td>34.53</td></tr>
            <tr><td>65</td><td>18.13</td><td>71.44</td><td>−102.23</td><td>−105</td><td>−2.77</td><td>7.68</td></tr>
            <tr><td>110</td><td>20.41</td><td>80.44</td><td>−111.23</td><td>−115</td><td>−3.77</td><td>14.20</td></tr>
            <tr><td>400</td><td>26.02</td><td>102.53</td><td>−133.32</td><td>−130</td><td>+3.32</td><td>11.05</td></tr>
            <tr><td>1000</td><td>30.00</td><td>118.22</td><td>−149.01</td><td>−150</td><td>−0.99</td><td>0.99</td></tr>
          </tbody></table></div>\(\sum e_i^2=71.23\), so the MSE is \(\sigma_\psi^2=71.23/6=11.87\) and \(\sigma_\psi=3.45\) dB. (Least-squares residuals always sum to 0, a quick arithmetic check.)
Row example (d = 5 m): \(\hat y_1=-30.79-27.54=-58.33\), \(e_1=-60-(-58.33)=-1.67\), \(e_1^2=2.78\). Why the MSE is the shadowing variance: Ch 2 p.13 defines the error \(X_i\) (measured − model) and sets its mean square \(E[X_i^2]=\sigma_\psi^2\), so divide by n = 6 (not 5), as in the definition.''',
  r'''<b>(b) Write the outage probability</b>: the mean received power from path loss alone is 10 dB above the minimum required power, i.e. the margin is x = 10 dB. Outage means shadowing pulls the power down by more than 10 dB (Ch 2 p.14–15):
\[\begin{aligned}P_{out}&=P\big(P_{r,dB}\lt P_{m,dB}\big)\\&=P\big(\psi_{dB}\lt-10\big)=Q\Big(\frac{10}{\sigma_\psi}\Big)\end{aligned}\]
Last step: divide by \(\sigma_\psi\) to standardise, then use the symmetry of the Gaussian, P(N &lt; −a) = P(N &gt; a) = Q(a). Use the margin in dB directly; do not convert it to linear.''',
  r'''<b>(b) Substitute and look up Q</b>: the MSE is a variance, so take the square root before putting it in Q:
<div class="calc">σ<sub>ψ</sub> = √11.87 = 3.45 dB<br>10 / σ<sub>ψ</sub> = 10 / 3.45 = 2.90<br>P<sub>out</sub> = Q(2.90) ≈ 1.85 × 10⁻³ (about 0.19%)</div>
A two-decimal Q table gives Q(2.90) = 1.87 × 10⁻³; 1.85 × 10⁻³ uses the unrounded 10/3.446 = 2.902. The difference is only rounding.''',
  r'''<b>Check</b>: ① the residuals sum to −1.67 + 5.88 − 2.77 − 3.77 + 3.32 − 0.99 = 0 ✓ (a property of least squares); ② the line passes through the mean point: −30.79 − 3.94 × 19.26 = −106.67 = M̄ ✓; ③ order of magnitude: a 10 dB margin is about 2.9σ, a little less than the 3.09σ for Q(3.09) = 10⁻³, so the outage is a little above 10⁻³ ✓.'''],
 ans=r'''<b>Standard least squares:</b> K ≈ −30.8 dB, γ ≈ 3.94, σ²<sub>ψ</sub> ≈ 11.9 dB², P<sub>out</sub> ≈ 1.85 × 10⁻³''',
 official=r'''(a) K<sub>dB</sub> = −31.4 dB, γ = 3.86; (b) 6.19 × 10⁻⁴''',
 note=r'''Part (b) of the official answer comes from the MSE the lecturer used in class, 9.656: he took 10/√9.656 ≈ 3.23 and read Q(3.23) = 6.19 × 10⁻⁴ from the table (week 10 recording; precisely 10/3.107 = 3.22 and Q ≈ 6.5 × 10⁻⁴). But 9.656 does not match the official K and γ either: substituting K = −31.4, γ = 3.86 back into the 6 points gives an MSE of 13.1, and standard least squares gives 11.87. In class the lecturer said the numbers depend on rounding and anything "around −31.4 and 3.86" is fine. <b>In the exam, state the method clearly (least squares, σ² = MSE, P<sub>out</sub> = Q(10/σ)) and use the numbers you obtain.</b>''',
 kp=[
  ('What it tests', '''Fitting K and γ of the simplified path-loss model to measured data by least squares, then using the fitted MSE as the shadowing variance to find the outage probability (Ch 2 p.8, p.12–15).'''),
  ('Background', '''dB arithmetic; least squares (set the partial derivatives with respect to K and γ to zero, see the derivation box in Section 2.1 of the learning page); the Q function (Ch 1b).'''),
  ('Method', '''① x<sub>i</sub> = 10 log₁₀(d<sub>i</sub>/d₀); ② tabulate x, M, x², xM and sum each column; ③ solve the two normal equations for K and γ; ④ compute the residuals e<sub>i</sub> = measured − predicted, MSE = σ<sub>ψ</sub>²; ⑤ P<sub>out</sub> = Q(margin/σ<sub>ψ</sub>).'''),
  ('Key formulas', '''γ = −Σ(x<sub>i</sub> − x̄)(M<sub>i</sub> − M̄) / Σ(x<sub>i</sub> − x̄)²; K<sub>dB</sub> = M̄ + γx̄; σ<sub>ψ</sub>² = (1/n)Σe<sub>i</sub>²; P<sub>out</sub> = Q(10/σ<sub>ψ</sub>).'''),
  ('Common mistakes', '''The slope of the line is −γ, so keep the minus sign. Use 10 log₁₀d, not log₁₀d (otherwise γ comes out 10 times too large). The MSE is a variance: take the square root before putting it in Q. "10 dB above" means a 10 dB margin.'''),
  ('Check', '''The residuals sum to 0; the fitted line passes through the mean point (19.26, −106.67); Σe² = 71.23 from the table in step 4.'''),
  ('Variations', '''Given K, γ and σ, find the outage probability at some distance, or the maximum coverage distance for a target outage (lecture p.16 example, Section 2.2 of the learning page). See the note above on why the official answer cannot be reproduced.''')])

EN['p1q2'] = dict(
 idea=r'''The received power in dBm is Gaussian. Probability of falling below the threshold: subtract the mean, divide by the standard deviation, look up the Q table.''',
 steps=[
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
  r'''<b>Check</b>: substitute μ<sub>ψ</sub> = 19.3 dBm back: (19.3 − 10)/4 = 2.325, Q(2.325) ≈ 0.0100, exactly on the 1% boundary ✓. Compare with (a): a margin of only 0.625σ gives 26.6% outage; to bring it down to 1% the margin must grow to 2.326σ (here 9.3 dB).'''],
 ans=r'''(a) ≈ 26%; (b) μ<sub>ψ</sub> &gt; 19.3 dBm''',
 official=r'''(a) 26%; (b) μ<sub>ψ</sub> &gt; 19.32 dB ✓''',
 kp=[
  ('What it tests', '''Log-normal shadowing means the dB value is Gaussian; outage probability computed forwards and backwards (Ch 2 p.11–15).'''),
  ('Background', '''Standardisation: (threshold − mean)/standard deviation; Q is decreasing and Q(−x) = 1 − Q(x); common values Q(1.645) = 0.05, Q(2.326) = 0.01, Q(3.09) = 10⁻³.'''),
  ('Method', '''(a) How many standard deviations is the threshold from the mean → Q. (b) Treat μ as unknown, write Q((μ − 10)/σ) &lt; 0.01 and invert: (μ − 10)/σ &gt; 2.326.'''),
  ('Key formula', '''P<sub>out</sub> = P(P<sub>r</sub> &lt; P<sub>min</sub>) = Q((μ<sub>ψ</sub> − P<sub>min</sub>)/σ<sub>ψ</sub>). The difference μ − P<sub>min</sub> is the shadowing margin.'''),
  ('Common mistakes', '''Q is decreasing, so "probability &lt; 1%" becomes "argument &gt; 2.326". Do not confuse σ with σ². The difference of two dBm values is in dB.'''),
  ('Variations', '''A larger σ needs a larger margin for the same outage: with σ = 8 dB, μ must exceed 10 + 8 × 2.326 = 28.6 dBm, 9.3 dB more than with σ = 4 dB.'''),
  ('Physical meaning', '''Shadowing is large-scale, slowly varying fading (blocking by buildings and terrain), so it is handled with a margin; small-scale multipath fading is handled with diversity (Ch 4).''')])

EN['p1q3'] = dict(
 steps=[
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
Check: at R<sub>s</sub> = 34.6 ksps, T<sub>s</sub> = 28.9 µs and σ/T<sub>s</sub> = 2.89/28.9 = 0.1, exactly on the boundary ✓. The answer is an upper limit, not an equality.'''],
 ans=r'''μ = 5 µs, σ = 2.89 µs; R<sub>s</sub> &lt; 34.6 ksps''',
 official=r'''5 µs, 2.89 µs; 34.6 ksps ✓''',
 kp=[
  ('What it tests', '''Mean delay and rms delay spread from a power delay profile, and the flat / frequency-selective decision (Ch 2 p.29–33).'''),
  ('Background', '''Normalise P(τ) and treat it as a probability density; E[τ], E[τ²] and variance = E[τ²] − (E[τ])² (Ch 1b).'''),
  ('Method', '''① μ = ∫τP(τ)dτ / ∫P(τ)dτ; ② E[τ²] = ∫τ²P(τ)dτ / ∫P(τ)dτ; ③ σ = √(E[τ²] − μ²); ④ flat if σ/T<sub>s</sub> &lt; 0.1 → lower bound on T<sub>s</sub> → upper bound on R<sub>s</sub>.'''),
  ('Key formula', '''Uniform on [0, a]: μ = a/2, σ = a/√12. Here a = 10 µs → 5 µs and 2.89 µs.'''),
  ('Common mistakes', '''The denominator is ∫P = 10, not 1. Flat fading needs long symbols (low rate), so keep the inequality the right way round; 34.6 ksps is an upper limit.'''),
  ('Variations', '''"Is a 1 MHz signal (T<sub>s</sub> = 1 µs) flat?" σ/T<sub>s</sub> = 2.89 &gt; 0.1 → frequency-selective, needs equalisation or OFDM. For a discrete profile (a few echoes) replace the integrals by weighted sums (Section 2.4 example on the learning page).'''),
  ('Link', '''Larger delay spread means smaller coherence bandwidth (B<sub>C</sub> ∝ 1/σ<sub>Tm</sub>); the same σ appears in the Ch 3 error floor (σ<sub>Tm</sub>/T<sub>b</sub>)².''')])

# ================================================================ Practice 2
EN['p2q1'] = dict(
 steps=[
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
About 12 fades per second, each about 0.8 ms long, add up to about 1% of the time below the threshold, which is exactly the Rayleigh P(z &lt; Z<sub>min</sub>). The small-ρ approximation AFD ≈ ρ/(√(2π) f<sub>D</sub>) = 0.1/125.3 = 7.98 × 10⁻⁴ s agrees too ✓.'''],
 ans='AFD ≈ 0.8 ms', official='0.8 ms ✓',
 note=r'''By-product, the level crossing rate: \(\sqrt{2\pi}\times50\times0.1\times e^{-0.01}=12.4\) crossings/s. AFD × LCR = 0.00995 ≈ 1%, the fraction of time the signal is more than 20 dB below its rms value.''',
 kp=[
  ('What it tests', '''Average fade duration (AFD) in Rayleigh fading (Ch 2 p.42–43).'''),
  ('Background', '''ρ = Z<sub>min</sub>/Z<sub>rms</sub> is an <b>amplitude</b> ratio; Rayleigh P(z &lt; Z<sub>min</sub>) = 1 − e<sup>−ρ²</sup>; Doppler f<sub>D</sub> = v f<sub>c</sub>/c.'''),
  ('Method', '''Find ρ → e<sup>ρ²</sup> − 1 → denominator √(2π) f<sub>D</sub> ρ → divide.'''),
  ('Key formulas', '''AFD = (e<sup>ρ²</sup> − 1)/(√(2π) f<sub>D</sub> ρ); LCR = √(2π) f<sub>D</sub> ρ e<sup>−ρ²</sup>; AFD × LCR = 1 − e<sup>−ρ²</sup> (fraction of time below the threshold).'''),
  ('Common mistakes', '''"0.1 of the rms value" is an amplitude, so ρ = 0.1 (power 20 dB down). If a question says "0.1 of the power", then ρ = √0.1 = 0.316.'''),
  ('Variations', '''Given vehicle speed and carrier frequency, compute f<sub>D</sub> first. Number of symbols lost per fade = AFD × symbol rate: at 1 Msps, 0.8 ms ≈ 800 symbols (Section 2.6 example on the learning page).'''),
  ('Intuition', '''For small ρ, AFD ≈ ρ/(√(2π) f<sub>D</sub>): the lower the threshold, the shorter the time spent below it; the faster the vehicle (larger f<sub>D</sub>), the shorter but more frequent the fades.''')])

EN['p2q2'] = dict(
 steps=[
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
  r'''<b>Check</b>: ① b = 0 (no common shadowing, a = 1): Q no longer depends on u and comes out of the integral, \(\int\frac{1}{\sqrt{2\pi}}e^{-u^2/2}du=1\), giving \([Q(\Delta/\sigma)]^2\), part (b) ✓; ② a → 0 (fully shared, b = 1): Q → 1 for u &lt; −Δ/σ and Q → 0 otherwise, so \(P_{out}=P(u\lt-\Delta/\sigma)=Q(\Delta/\sigma)\), the same as one base station: no diversity ✓.'''],
 ans='(b) [Q(Δ/σ)]²; (c) ∫ (1/√(2π)) Q[(Δ + bσu)/(|a|σ)]² e<sup>−u²/2</sup> du',
 official='same as above ✓ (the question writes byσ; its integration variable y is the normalised u)',
 note='''Sanity check: b = 0 reduces to the independent case (b); a = 0 makes the two links identical, P<sub>out</sub> = Q(Δ/σ), and diversity is useless. The stronger the correlation, the weaker the macro-diversity gain.''',
 kp=[
  ('What it tests', '''Outage with macro-diversity for independent and correlated shadowing; conditional probability plus total probability (Ch 2 p.12–15; Ch 4 p.3–4, p.21).'''),
  ('Background', '''Independent events multiply; a linear combination of independent Gaussians is Gaussian, aY₁ + bY ~ N(0, (a² + b²)σ²); continuous total probability P(A) = ∫P(A | y)p(y)dy.'''),
  ('Method', '''(b) Single-link outage P(Z<sub>i</sub> &lt; −Δ) = Q(Δ/σ), independent → square. (c) Fix the shared Y ("condition on it"), the links are then independent → multiply the conditional outages → integrate over the PDF of Y.'''),
  ('Key step', '''Let Y = σu, u ~ N(0, 1). Given u: Z<sub>i</sub> ~ N(bσu, a²σ²), P(Z<sub>i</sub> &lt; −Δ | u) = Q((Δ + bσu)/(|a|σ)).'''),
  ('Hidden assumption', '''To be consistent with Z<sub>i</sub> ~ N(0, σ²) we need a² + b² = 1. The correlation coefficient of Z₁ and Z₂ is then b²: the larger b, the more alike the two links.'''),
  ('Check', '''b = 0 gives the [Q(Δ/σ)]² of part (b); a = 0 (fully correlated) makes the links identical, P<sub>out</sub> = Q(Δ/σ), no diversity at all.'''),
  ('Link', '''Practice 4 Q1 explains the same idea in words; Ch 4 p.21 "correlation reduces diversity"; Practice 4 Q2(c) is a discrete version with shared shadowing.''')])

# collapsible step-by-step walk-through of part (c), rendered after the note (add_en.py)
EN['p2q2']['detail'] = r'''      <details class="deep">
        <summary>(c) Step by step: fix Y → multiply → integrate over Y → substitute</summary>
        <div class="deep-body">
          <h4><span class="st">Step 0</span>Write outage as a condition on Z</h4>
          <p>\(P_{r,i}=W+Z_i\) and the threshold is \(T=W-\Delta\), so</p>
          <div class="eqb">\[P_{r,i}\lt T\iff W+Z_i\lt W-\Delta\iff Z_i\lt-\Delta,\qquad P_{out}=P\big(Z_1\lt-\Delta\ \text{and}\ Z_2\lt-\Delta\big)\]</div>
          <p>The outage condition is the same in (b) and (c); only the relation between Z₁ and Z₂ changes.</p>

          <h4><span class="st">Step 1</span>Why we cannot just square, as in (b)</h4>
          <p>\(Z_1=aY_1+bY\), \(Z_2=aY_2+bY\): both links contain the same \(bY\). When Y is very negative, both links get worse together, so Z₁ and Z₂ are not independent: \(P(A\cap B)\neq P(A)P(B)\), and we cannot simply multiply.</p>
          <p>Intuition (not in the slides): \(bY\) is shadowing common to both links, e.g. the phone is behind a building or inside a car, so the signal from either base station must pass through it; \(aY_1\), \(aY_2\) are the shadowing specific to each path, independent of each other.</p>
          <p>How strong the correlation is: the cross terms vanish because the variables are independent with zero mean,</p>
          <div class="eqb">\[\operatorname{Cov}(Z_1,Z_2)=E\big[(aY_1+bY)(aY_2+bY)\big]=b^2E[Y^2]=b^2\sigma^2,\qquad \operatorname{Var}(Z_i)=(a^2+b^2)\sigma^2\]</div>
          <p>The question says \(Z_i\sim\mathcal N(0,\sigma^2)\), which implies \(a^2+b^2=1\); the correlation coefficient is \(\rho=b^2\). The larger b, the more alike the two links.</p>

          <h4><span class="st">Step 2</span>Lecturer's method ①: treat Y as a constant</h4>
          <p>Suppose Y = y is known. In \(Z_1=aY_1+by\) the term \(by\) is just a constant shift; the only random part is \(aY_1\sim\mathcal N(0,a^2\sigma^2)\) (a constant times a Gaussian, standard deviation \(|a|\sigma\)), so</p>
          <div class="eqb">\[Z_i\mid y\ \sim\ \mathcal N\big(by,\ a^2\sigma^2\big)\]</div>
          <p><b>Key point:</b> given y, Z₁ depends only on Y₁ and Z₂ only on Y₂, and Y₁, Y₂ are independent, so Z₁ and Z₂ are <b>conditionally independent</b>. The shared part is "frozen" and the correlation disappears.</p>

          <h4><span class="st">Step 3</span>Conditional outage of one link</h4>
          <div class="eqb">\[P(Z_1\lt-\Delta\mid y)=P\big(aY_1\lt-(\Delta+by)\big)=P\Big(N\lt-\frac{\Delta+by}{|a|\sigma}\Big)=P\Big(N\gt\frac{\Delta+by}{|a|\sigma}\Big)=Q\Big(\frac{\Delta+by}{|a|\sigma}\Big)\]</div>
          <p>N ~ N(0, 1) is aY₁ divided by its standard deviation |a|σ; the third equality uses the symmetry of the Gaussian about 0; the last step is the definition Q(x) = P(N &gt; x). We write |a| because a standard deviation must be positive; a negative a leaves the distribution unchanged. The more negative y (deeper common shadow), the smaller Δ + by and the larger Q: outage becomes more likely.</p>

          <h4><span class="st">Step 4</span>Multiply the two links</h4>
          <div class="eqb">\[P(\text{outage}\mid y)=P(Z_1\lt-\Delta\mid y)\,P(Z_2\lt-\Delta\mid y)=\Big[Q\Big(\frac{\Delta+by}{|a|\sigma}\Big)\Big]^2\]</div>
          <p>This is the "independent → multiply" of part (b), done under the condition that Y is known.</p>

          <h4><span class="st">Step 5</span>Lecturer's method ②: make Y random again and integrate over its PDF</h4>
          <p>Total probability theorem, continuous form: \(P(A)=\int P(A\mid Y=y)\,f_Y(y)\,dy\) (discrete form \(\sum_k P(A\mid B_k)P(B_k)\)): a weighted average over every case, weighted by how likely it is. With \(f_Y(y)=\frac{1}{\sqrt{2\pi}\,\sigma}e^{-y^2/(2\sigma^2)}\):</p>
          <div class="eqb">\[P_{out}=\int_{-\infty}^{\infty}\Big[Q\Big(\frac{\Delta+by}{|a|\sigma}\Big)\Big]^2\,\frac{1}{\sqrt{2\pi}\,\sigma}\,e^{-y^2/(2\sigma^2)}\,dy\]</div>
          <p>This is already correct; it just does not look like the required form yet.</p>

          <h4><span class="st">Step 6</span>Lecturer's method ③: substitute u = y/σ</h4>
          <p>\(y=\sigma u\), \(dy=\sigma\,du\), limits still ±∞. The 1/σ in front of the PDF cancels the σ in dy; \(e^{-y^2/(2\sigma^2)}=e^{-u^2/2}\); the argument of Q becomes \((\Delta+b\sigma u)/(|a|\sigma)\):</p>
          <div class="eqb">\[P_{out}=\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}\Big[Q\Big(\frac{\Delta+b\sigma u}{|a|\sigma}\Big)\Big]^2e^{-u^2/2}\,du\]</div>
          <p>The integration variable is a dummy variable. Renaming u to y gives the question's \((\Delta+by\sigma)/(|a|\sigma)\), so <b>the y in the question is the normalised u</b>, not the original Y. The question's \(Q[\cdot]^2\) means \([Q(\cdot)]^2\), not Q of a squared argument.</p>

          <h4><span class="st">Check</span>Two extreme cases</h4>
          <ul>
            <li><b>b = 0</b> (no common shadowing, a = 1): Q no longer depends on u and comes out of the integral, leaving \(\int\frac{1}{\sqrt{2\pi}}e^{-u^2/2}du=1\). The result is \([Q(\Delta/\sigma)]^2\), part (b) ✓</li>
            <li><b>a → 0</b> (fully shared, b = 1): the argument of Q goes to ±∞. For u &gt; −Δ/σ, Q → 0; for u &lt; −Δ/σ, Q → 1. So \(P_{out}=P(u\lt-\Delta/\sigma)=Q(\Delta/\sigma)\), the same as a single base station: no diversity at all ✓</li>
          </ul>

          <div class="note">Numbers for intuition (not in the slides; numerical integration, checked by Monte Carlo simulation). With Δ = σ (e.g. both 8 dB), a single base station has outage Q(1) = 0.1587:
            <div class="tw"><table class="mini"><thead><tr><th>ρ = b²</th><th>0</th><th>0.25</th><th>0.5</th><th>0.75</th><th>0.9</th><th>1</th></tr></thead><tbody><tr><td>P<sub>out</sub></td><td>0.0252</td><td>0.0417</td><td>0.0625</td><td>0.0905</td><td>0.1155</td><td>0.1587</td></tr></tbody></table></div>
            For ρ = 0.5 the conditional outage P(outage | u) is 0.52 at u = −2, 0.0062 at u = 0 and about 6×10⁻⁵ at u = +1. Almost all outages happen when the common shadow is deep (u very negative) and both base stations fail together. That is why correlation weakens macro-diversity.</div>

          <h4><span class="st">Exam</span>Compact answer (write it in this order)</h4>
          <div class="tmpl">
            <p>Outage ⇔ \(Z_1\lt-\Delta\) and \(Z_2\lt-\Delta\). \(Z_1\) and \(Z_2\) share the term \(bY\), so they are correlated; condition on \(Y=y\).</p>
            <p>Given y, \(Z_i=aY_i+by\sim\mathcal N(by,\,a^2\sigma^2)\), and \(Z_1,Z_2\) are independent since \(Y_1,Y_2\) are independent.</p>
            <p>\(P(Z_i\lt-\Delta\mid y)=P\big(aY_i\lt-(\Delta+by)\big)=Q\big(\tfrac{\Delta+by}{|a|\sigma}\big)\), so \(P(\text{out}\mid y)=Q^2\big(\tfrac{\Delta+by}{|a|\sigma}\big)\).</p>
            <p>By the total probability theorem, \(P_{out}=\int P(\text{out}\mid y)f_Y(y)\,dy=\int Q^2\big(\tfrac{\Delta+by}{|a|\sigma}\big)\tfrac{1}{\sqrt{2\pi}\,\sigma}e^{-y^2/2\sigma^2}dy\).</p>
            <p>Let \(u=y/\sigma\) (\(dy=\sigma\,du\)): \(P_{out}=\int\tfrac{1}{\sqrt{2\pi}}Q^2\big(\tfrac{\Delta+b\sigma u}{|a|\sigma}\big)e^{-u^2/2}du\), which is the required result.</p>
          </div>
          <div class="ans">In one line: fix the shared variable → conditionally independent, multiply → integrate over its PDF → substitute u = y/σ. Practice 4 Q2(c) is the discrete version of the same method.</div>
        </div>
      </details>'''

EN['p2q3'] = dict(
 steps=[
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
20 × 7.651 = 153.02 ✓: with successive interference cancellation, the sum capacity equals the single-user capacity with the two powers combined. (b) is much larger than (a) because user 2 no longer faces 10 mW of interference, only 0.1 mW of noise.'''],
 ans='(a) 19.86 Mbps; (b) 133.16 Mbps', official='19.86 Mbps; 133.16 Mbps ✓',
 kp=[
  ('What it tests', '''Shannon capacity, SINR (interference treated as noise) and multi-user detection / successive interference cancellation (Ch 1a p.16; Ch 2 p.48).'''),
  ('Background', '''C = B log₂(1 + SNR) with SNR as a linear value; log₂x = ln x / ln 2 = log₁₀x / 0.301.'''),
  ('Method', '''(a) SINR₁ = P₁/(P₂ + N); (b) user 1 already subtracted, SNR₂ = P₂/N; substitute each into Shannon's formula.'''),
  ('Check', '''C₁ + C₂ = 19.86 + 133.16 = 153.02 Mbps = 20 log₂(1 + (10 + 10)/0.1): <mark class="hl">the sum capacity with successive cancellation equals the single-user capacity with the two powers combined</mark>, independent of the decoding order.'''),
  ('Common mistakes', '''SINR 0.990 is linear, not dB; log₂1.99 = 0.993; remember to multiply by the 20 MHz bandwidth; use the same unit (mW) for both powers.'''),
  ('Variations', '''Decoding user 2 first swaps the two results; the sum stays the same. Without MUD, each user treats the other as noise and the total is only 2 × 19.86 = 39.7 Mbps, less than a third of the MUD total. That is the value of multi-user detection.''')])

# ================================================================ Practice 3
EN['p3q1'] = dict(
 steps=[
  r'''<b>Expand (find the directions)</b>: with the angle-sum identity \(\cos(a+b)=\cos a\cos b-\sin a\sin b\),
\[\begin{aligned}A_i\cos\!\Big(\tfrac{2\pi t}{T}+\phi_j\Big)&=\underbrace{A_i\cos\phi_j}_{\text{constant}}\cos\tfrac{2\pi t}{T}\\&\quad+\underbrace{(-A_i\sin\phi_j)}_{\text{constant}}\sin\tfrac{2\pi t}{T}\end{aligned}\]
\(A_i\) and \(\phi_j\) do not change with t, so they are just two coefficients; only \(\cos\frac{2\pi t}{T}\) and \(\sin\frac{2\pi t}{T}\) depend on t. Whatever values \(A_i\) and \(\phi_j\) take, every signal is a combination of these two waveforms, so they are the candidate basis functions.''',
  r'''<b>Check orthogonality</b>: with \(\sin a\cos a=\tfrac12\sin 2a\),
\[\begin{aligned}\int_0^T\cos\tfrac{2\pi t}{T}\sin\tfrac{2\pi t}{T}\,dt&=\tfrac12\int_0^T\sin\tfrac{4\pi t}{T}\,dt\\&=\tfrac12\Big[-\tfrac{T}{4\pi}\cos\tfrac{4\pi t}{T}\Big]_0^T\\&=-\tfrac{T}{8\pi}(\cos4\pi-\cos0)=0\end{aligned}\]
\(\sin\frac{4\pi t}{T}\) completes exactly two full periods between 0 and T, so the positive and negative areas cancel and the two functions are orthogonal.''',
  r'''<b>Find the energy</b>: with \(\cos^2a=\tfrac{1+\cos2a}{2}\),
\[\begin{aligned}E_c=\int_0^T\cos^2\tfrac{2\pi t}{T}\,dt&=\int_0^T\frac{1+\cos\frac{4\pi t}{T}}{2}\,dt\\&=\frac T2+\frac12\Big[\frac{T}{4\pi}\sin\frac{4\pi t}{T}\Big]_0^T=\frac T2\end{aligned}\]
The same holds for \(\sin^2\) (\(\sin^2a=\tfrac{1-\cos2a}{2}\)), so its energy is also \(T/2\). Intuitively, cos² swings between 0 and 1 with an average of ½, so the energy is ½ × the duration T.''',
  r'''<b>Normalise</b>: let the basis function be \(c\cos\frac{2\pi t}{T}\) and require unit energy:
\[\int_0^T\Big(c\cos\tfrac{2\pi t}{T}\Big)^2dt=c^2\cdot\frac T2=1\;\Rightarrow\;c=\sqrt{\frac2T}\]
i.e. divide by \(\sqrt{E_c}=\sqrt{T/2}\). This gives
\[\begin{aligned}\psi_1(t)&=\sqrt{\tfrac2T}\cos\tfrac{2\pi t}{T}\\ \psi_2(t)&=\sqrt{\tfrac2T}\sin\tfrac{2\pi t}{T}\end{aligned}\qquad 0\le t\le T\]
Check: \(\int_0^T\psi_1^2\,dt=\frac2T\cdot\frac T2=1\) ✓. Multiplying by a constant does not affect the orthogonality from step 2.''',
  r'''<b>Coordinates and self-check</b>:
\[\begin{aligned}s_{ij}(t)&=\underbrace{\sqrt{\tfrac T2}A_i\cos\phi_j}_{s_1}\,\psi_1(t)\\&\quad+\underbrace{\Big(-\sqrt{\tfrac T2}A_i\sin\phi_j\Big)}_{s_2}\,\psi_2(t)\end{aligned}\]
The sum of squared coordinates \(s_1^2+s_2^2=\frac T2A_i^2\) equals the signal energy computed directly, \(\int_0^T s_{ij}^2\,dt=\frac T2A_i^2\) ✓.''',
  r'''<b>(b) Dimension</b>: every signal needs only the two basis functions \(\psi_1\) and \(\psi_2\), so the dimension is D = 2. More values of \(A_i\) and \(\phi_j\) only add more points (constellation points) in the same plane; they do not add dimensions.'''],
 ans='(a) { √(2/T)·cos(2πt/T), √(2/T)·sin(2πt/T) }; (b) dimension 2', official='same as above ✓',
 kp=[
  ('What it tests', '''Signal space: orthonormal basis and dimension (Ch 3 p.4–11).'''),
  ('Background', '''Angle-sum identity cos(a + b) = cos a cos b − sin a sin b; ∫₀<sup>T</sup> cos²(2πt/T) dt = T/2; inner product = multiply and integrate.'''),
  ('Method', '''① Write the signal as a linear combination of a few fixed waveforms; ② check they are mutually orthogonal; ③ divide each by √energy to normalise; ④ the number of basis functions is the dimension.'''),
  ('Key result', '''ψ₁ = √(2/T) cos(2πt/T), ψ₂ = √(2/T) sin(2πt/T). Coordinates (A<sub>i</sub>cosφ<sub>j</sub>√(T/2), −A<sub>i</sub>sinφ<sub>j</sub>√(T/2)); distance from the origin A<sub>i</sub>√(T/2) = √E.'''),
  ('Common mistakes', '''Forgetting the normalising factor √(2/T); thinking many values of A<sub>i</sub>, φ<sub>j</sub> mean many dimensions (the dimension only counts basis functions, D ≤ M); the minus sign of the sin term belongs in the coordinate.'''),
  ('Variations', '''Amplitude only (φ fixed) → 1-D (PAM); phase only → 2-D (PSK); both → 2-D (QAM, as here). 2025-26 S1 Q1(a)(i): sketch the ±1 constellation, dimension 1, distance 2.''')])

EN['p3q2'] = dict(
 steps=[
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
For comparison, with the midpoint 0.5 as the threshold P<sub>e</sub> = ½[Q(1.581) + Q(0.791)] = ½(0.0569 + 0.2145) = 0.136, larger than with the ML threshold ✓ (the ML threshold is the one that minimises P<sub>e</sub>).'''],
 ans='x̂<sub>n</sub> = 1 if y<sub>n</sub> &gt; ỹ, otherwise 0; P<sub>e</sub> = ½[Q((1 − ỹ)/σ₁) + Q(ỹ/σ₀)]', official='same as above ✓',
 note='''A numerical feel: with σ₀² = 0.1 and σ₁² = 0.4, g(y) = 3.75y² + 2.5y − 1.943 and ỹ ≈ 0.46. Strictly, the quadratic has a second root at a very negative y (where the rule decides 1 again); its probability is negligible and the answer ignores it.''',
 kp=[
  ('What it tests', '''Non-standard ML detection: the two hypotheses have different noise variances (Ch 3 p.18–20).'''),
  ('Background', '''Gaussian PDF (keep the factor 1/(√(2π)σ)); ln is increasing, so likelihoods can be compared after taking logs; roots of a quadratic; the Q function.'''),
  ('Method', '''① Write both conditional PDFs; ② compare likelihoods, take logs, rearrange to g(y) &gt; 0; ③ solve g(ỹ) = 0 for the threshold; ④ compute the two error events separately; ⑤ weight by the priors (½ each).'''),
  ('Key formulas', '''g(y) = y²/(2σ₀²) − (y − 1)²/(2σ₁²) + ln(σ₀/σ₁); P<sub>e</sub> = ½[Q((1 − ỹ)/σ₁) + Q(ỹ/σ₀)].'''),
  ('Numerical example', '''σ₀² = 0.1, σ₁² = 0.4: ỹ ≈ 0.46, P<sub>e</sub> = ½[Q(0.54/0.632) + Q(0.46/0.316)] = ½[Q(0.85) + Q(1.46)] ≈ 0.135.'''),
  ('Common mistakes', '''Comparing only the exponents and dropping 1/σ gives the wrong threshold; each error event uses its own σ; the quadratic has two roots, take the one between 0 and 1.'''),
  ('Variations', '''Equal variances → ỹ = 0.5, P<sub>e</sub> = Q(0.5/σ). Unequal priors → MAP, add ln P(x) inside the log; the threshold moves towards the less likely symbol.''')])

EN['p3q3'] = dict(
 steps=[
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
  r'''<b>Self-check</b>: substituting back, (σ<sub>Tm</sub>/T<sub>s</sub>)² = (3/94.87)² = 0.03162² = 1.000 × 10⁻³, exactly the floor target ✓. σ<sub>Tm</sub>/T<sub>s</sub> = 0.032 &lt; 0.1, so the flat-fading rule (Practice 1 Q3) is also satisfied ✓.'''],
 ans='R ≈ 21.08 kbps', official='21.08 kbps ✓',
 kp=[
  ('What it tests', '''The irreducible error floor caused by delay spread; converting between bit and symbol durations (Ch 3 p.35).'''),
  ('Background', '''M-ary signalling carries log₂M bits per symbol: R<sub>b</sub> = log₂M / T<sub>s</sub>; QPSK has M = 4.'''),
  ('Method', '''From the floor requirement find the shortest symbol duration T = σ<sub>Tm</sub>/√P<sub>floor</sub>, then convert to a bit rate.'''),
  ('Key formula', '''(σ<sub>Tm</sub>/T)² = P<sub>floor</sub> → T = 3 µs / √10⁻³ = 3/0.0316 = 94.9 µs → R<sub>b</sub> = 2/94.9 µs = 21.08 kbps.'''),
  ('Common mistakes', '''T in the formula is the <b>symbol</b> duration (ISI depends on how long the echo is compared with one symbol); treating it as a bit duration gives 10.54 kbps. σ<sub>Tm</sub> is the rms delay spread, not the maximum delay.'''),
  ('Contrast', '''The Doppler floor ½(πf<sub>D</sub>T<sub>b</sub>)² needs <b>short</b> symbols (a minimum rate); the delay-spread floor needs <b>long</b> symbols (a maximum rate). With both present, the rate must lie between the two limits.'''),
  ('Physical meaning', '''A "floor" means the error rate stops falling however high the SNR: the errors come from the signal's own echoes, not from noise. The remedies are equalisation (Ch 6) or OFDM (Ch 7).''')])

# ================================================================ Practice 4
EN['p4q1'] = dict(
 steps=[
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
with equality when the links are uncorrelated. Reason: if the links are correlated, when one goes into a deep fade the other tends to as well, e.g. the mobile goes into a basement and all base stations become weak together. Practice 2 Q2(c): with a shadowing correlation of 0.5 (Δ = σ), 2.5% becomes 6.3%.'''],
 ans='Shadowing on links to different base stations is roughly independent; the probability that all links are in a deep fade together is the product of the individual probabilities, far smaller than for one link',
 official='see the lecture notes (Ch 4 p.3–4)',
 kp=[
  ('What it tests', '''The principle of macro-diversity (essay question, Ch 4 p.3–6).'''),
  ('Answer outline', '''① Outage is mainly due to <b>shadowing</b> (large-scale, slowly varying; extra power is an inefficient fix); ② base stations at different locations have different propagation paths, so the shadowing is roughly independent; ③ selecting the strongest base station or combining means outage only when <b>all</b> links are poor, P<sub>out</sub> = ΠP<sub>out,i</sub>; ④ condition: correlated links reduce the gain (p.21).'''),
  ('Do not confuse', '''Macro-diversity combats shadowing, with base stations far apart; micro-diversity combats multipath, with antennas only a few wavelengths apart (p.4–5).'''),
  ('Numbers', '''One link in outage 10%: two independent base stations 1%, three 0.1%.'''),
  ('Link', '''Practice 2 Q2 gives the quantitative formula: [Q(Δ/σ)]² when independent; when correlated, condition first and then integrate.'''),
  ('Writing tip', '''Write an essay answer as four sentences, "cause → mechanism → formula → condition", one point each. That earns marks more reliably than one long paragraph.''')])

EN['p4q2'] = dict(
 steps=[
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
Check (fix β first, the lecturer's method): for β = 7, ½ × 0.1472 × e⁻¹⁴ = 6.12 × 10⁻⁸; for β = 10, ½ × 0.1472 × e⁻²⁰ = 1.52 × 10⁻¹⁰; weighted, ⅓ × 6.12 × 10⁻⁸ + ⅔ × 1.52 × 10⁻¹⁰ = 2.05 × 10⁻⁸ ✓. The mean SNR and g are the same as in (b), but P̄<sub>s</sub> is 2.05/0.756 = 2.7 times larger and d drops from 8.1 to 7.7: 99.5% of the errors occur when β = 7 and both branches are poor together (shared shadowing weakens diversity, lecture p.21).'''],
 ans='(a) γ̄ = 10, P̄<sub>s</sub> = 6.15×10⁻⁵; (b) γ̄<sub>Σ</sub> = 20, P̄<sub>s</sub> = 7.6×10⁻⁹, g = 2, d = 8.1; (c) γ̄<sub>Σ</sub> = 20, P̄<sub>s</sub> = 2.05×10⁻⁸, g = 2, d = 7.7',
 official='identical ✓',
 note='''(b) and (c) have the same mean SNR, yet (c) has a 2.7 times higher error rate and d drops from 8.1 to 7.7: the shared shadowing β makes both branches fade together, which weakens diversity (lecture p.21).''',
 kp=[
  ('What it tests', '''Mean SNR and mean error rate for a discrete SNR distribution; MRC; array gain g and diversity gain d; correlated branches (Ch 4 p.16, p.21, p.27–28).'''),
  ('Background', '''Discrete expectation Σx·p; independent events multiply; E[f(X)] ≠ f(E[X]); for independent variables E[g(X)h(Y)] = E[g(X)]E[h(Y)].'''),
  ('Method', '''(a) Take the expectation directly. (b) Tabulate the 2 × 2 combinations → output SNR = sum of the branches → weight by probability. (c) Split e<sup>−γ<sub>Σ</sub></sup> into a product of independent factors and average each.'''),
  ('Key formulas', '''g = γ̄<sub>Σ</sub>/γ̄; d = −log₁₀P̄<sub>s</sub> / log₁₀γ̄ (γ̄ is the mean SNR at the combiner <b>input</b>).'''),
  ('Shortcut', '''(b) needs no table: for independent branches E[e<sup>−(γ₁+γ₂)</sup>] = (E[e<sup>−γ</sup>])², and (a) already gives E[e<sup>−γ</sup>] = 2 × 6.15×10⁻⁵ = 1.23×10⁻⁴, so P̄<sub>s</sub> = ½ × (1.23×10⁻⁴)² = 7.56×10⁻⁹.'''),
  ('Common mistakes', '''8 + 11 occurs in two orders, (8, 11) and (11, 8), probability 4/9. Keep enough significant figures for tiny numbers like e⁻¹⁶. Use the input SNR 10 for d, not the output 20. In (c) the shared β enters the exponent as 2β.'''),
  ('Conclusion', '''In (b) and (c) the mean SNR is 20 and g = 2, but correlation raises the error rate 2.7 times and lowers d from 8.1 to 7.7.''')])

EN['p4q3'] = dict(
 steps=[
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
The error probability falls faster as M grows, so combining helps ✓.'''],
 ans='(a) Q(α₀√E / √(σ₁²E + σ₂²)); (b) Q(√M·α₀√E / √(σ₁²E + σ₂²))', official='same as above ✓',
 note='''The mean grows like M while the standard deviation grows like √M, so the argument of Q increases by √M. That is the combining gain.''',
 kp=[
  ('What it tests', '''BPSK error rate when the fading factor is Gaussian; equal-weight combining (Ch 4 p.19; sums of independent Gaussians, Ch 1b).'''),
  ('Background', '''A sum of independent Gaussians is Gaussian with means and variances adding; Var(cX) = c²Var(X), so Var(α√E) = σ₁²E.'''),
  ('Method', '''Assume b = +1 (symmetric) → mean and variance of the decision variable z → error when z ≤ 0 → P = Q(mean / standard deviation).'''),
  ('Key result', '''Summing M branches with equal weights multiplies the mean by M and the variance by M, so the standard deviation grows by √M and the Q argument by √M.'''),
  ('Common mistakes', '''Do not forget the factor E in σ₁²E; the standard deviation is √(σ₁²E + σ₂²), not σ₁√E + σ₂.'''),
  ('Physical meaning', '''Even without noise (σ₂ = 0) the error rate is Q(α₀/σ₁) ≠ 0: the fading factor itself can become negative and flip the symbol, a fading-induced floor. Combining M branches lowers it to Q(√M α₀/σ₁).'''),
  ('Variation', '''If the receiver knew each α<sub>k</sub> it could weight by α<sub>k</sub> (MRC, p.15); here it does not, so equal weights are used.''')])

# ================================================================ Practice 5
EN['p5q1'] = dict(
 steps=[
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
Check with \(\log_2(1+\gamma_iP_i/P)\) directly: \(1+80\times0.3417=28.33\), \(1+40\times0.3292=14.17\), the same as in the previous step ✓.'''],
 ans='C ≈ 124.7 Mbps ≈ 125 Mbps', official='125 Mbps ✓',
 kp=[
  ('What it tests', '''MIMO capacity with an informed transmitter: eigen-sub-channels plus water-filling (Ch 5 p.19, p.40; Ch 2 p.54–57).'''),
  ('Background', '''The SVD splits a MIMO channel into non-interfering parallel sub-channels; the water-filling formulas.'''),
  ('Method', '''① Assume every sub-channel gets power and find γ₀ from Σ(1/γ₀ − 1/γ<sub>i</sub>) = 1; ② check that the weakest γ<sub>i</sub> ≥ γ₀, otherwise drop it and repeat; ③ P<sub>i</sub>/P = 1/γ₀ − 1/γ<sub>i</sub>; ④ C = B Σ log₂(γ<sub>i</sub>/γ₀).'''),
  ('Key numbers', '''γ₀ = 3/1.0625 = 2.82; powers 0.342, 0.329, 0.329 (sum 1); C = 10 MHz × (4.82 + 7.65) = 124.7 Mbps.'''),
  ('Comparison 1', '''Equal power (uninformed transmitter): the SNRs become 80/3, 40/3, 40/3 and C = 10 MHz × [log₂(1 + 80/3) + 2 log₂(1 + 40/3)] ≈ 124.7 Mbps, almost the same as water-filling (about 0.006 Mbps less). At high SNR channel knowledge at the transmitter matters little (p.41–42). Do not drop the "1 +": log₂(80/3) would give a wrong 122.1 Mbps.'''),
  ('Comparison 2', '''At low SNR the difference is large: dividing all three SNRs by 100 (0.8, 0.4, 0.4), water-filling uses only the first sub-channel and gives 0.85 bit/s/Hz, while equal power gives 0.70 bit/s/Hz: water-filling is about 21% higher (equal power about 17% lower).'''),
  ('Common mistakes', '''The γ<sub>i</sub> in water-filling is the SNR if <b>all</b> the power went to that sub-channel; with equal power each gets only P/3; multiply by B at the end.''')])

EN['p5q2'] = dict(
 steps=[
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
  r'''<b>Check</b>: the SNR of each symbol is \(\|\mathbf h\|^2E|u|^2/N_0\) (Ch 5 p.26), where \(\|\mathbf h\|^2=|h_A|^2+|h_B|^2\) is a sum of two independently fading gains ⇒ diversity order 2. Set \(h_B=0\): \(z_1=h_A^*y_1=|h_A|^2u_1+h_A^*w_1\), the ordinary single-antenna matched filter ✓.'''],
 ans='z₁ = ‖h‖u₁ + w̃₁, z₂ = ‖h‖u₂ + w̃₂, ‖h‖² = |h<sub>A</sub>|² + |h<sub>B</sub>|², w̃₁, w̃₂ ~ N(0, N₀)',
 official='z₁ = ‖h₁‖u₁ + w̃₁, z₂ = ‖h₂‖u₂ + w̃₂ (the two norms are in fact the same ‖h‖) ✓',
 note='''The effective SNR of each symbol is proportional to |h<sub>A</sub>|² + |h<sub>B</sub>|². Both paths fading at the same time is unlikely, which gives second-order diversity, and the transmitter needs no channel knowledge.''',
 kp=[
  ('What it tests', '''Reception, decision variables and diversity order of the Alamouti space-time block code (Ch 5 p.21–26).'''),
  ('Background', '''Complex conjugate (ab)* = a*b*; 2 × 2 matrix multiplication; multiplying noise by a complex c scales its variance by |c|².'''),
  ('Method', '''① Write y₁ and y₂ for the two slots; ② conjugate y₂ so u₁ and u₂ appear without conjugates; ③ write ỹ = Fu + ṽ; ④ pre-multiply by F<sup>H</sup>; ⑤ divide by ‖h‖ to normalise.'''),
  ('Key properties', '''X X<sup>H</sup> = ‖s‖²I (orthogonal code) → F<sup>H</sup>F = (|h<sub>A</sub>|² + |h<sub>B</sub>|²)I (the receiver can separate the two symbols completely).'''),
  ('Common mistakes', '''In slot 2 antenna A sends −u₂* (both the minus sign and the conjugate); the noise in z₁ is h<sub>A</sub>*w₁ + h<sub>B</sub>w₂*, variance (|h<sub>A</sub>|² + |h<sub>B</sub>|²)N₀.'''),
  ('Why order 2', '''The effective gain |h<sub>A</sub>|² + |h<sub>B</sub>|² is a sum of two independently fading terms; both being small at once is much less likely than one being small. And the transmitter does not need the channel.'''),
  ('Variations', '''2 transmit, M receive antennas: the gain is a sum of 2M terms |h|², diversity 2M (full diversity). 2025-26 S2 asks for the statistics of ŝ: unbiased, variance σ²/‖h‖². Compared with 1 × 2 MRC the diversity is the same but 3 dB is lost (power split between two antennas, p.30).''')])

EN['p5q3'] = dict(
 steps=[
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
  r'''<b>(b) Error probability</b>: r = 3 → \(d(3)=(8-3)(4-3)=5\) → \(P_e=\gamma^{-5}=10^{-5}\). Check: \(10^{-5}\le10^{-3}\) ✓. It beats the target by two orders of magnitude because r must be an integer: d jumps from 5 straight to 0, there is no point with exactly d = 3.'''],
 ans='(a) ≈ 9.96 bit/s/Hz; (b) P<sub>e</sub> = 10⁻⁵', official='9.96 bits/s/Hz; 10⁻⁵ ✓',
 kp=[
  ('What it tests', '''The diversity-multiplexing trade-off d(r) = (N − r)(M − r) and the rate R = r log₂SNR (Ch 4 p.31–34).'''),
  ('Background', '''Diversity gain d: how fast the error rate falls when the SNR doubles, at most N × M. Multiplexing gain r: how many extra bit/s/Hz per doubling of SNR, at most min(N, M).'''),
  ('Method', '''① From P<sub>e</sub> = γ<sup>−d</sup> ≤ target find the minimum d; ② list d for r = 0 … min(N, M); ③ take the largest r that meets it; ④ R = r log₂γ, P<sub>e</sub> = γ<sup>−d(r)</sup>.'''),
  ('Key numbers', '''γ = 10 → d ≥ 3; d(3) = 5 ≥ 3, d(4) = 0 &lt; 3 → r = 3; R = 3 × 3.32 = 9.97 bit/s/Hz, P<sub>e</sub> = 10⁻⁵.'''),
  ('Common mistakes', '''Use the linear SNR (10 dB → 10, 20 dB → 100); d must be an integer, round up; r cannot exceed min(N, M) = 4.'''),
  ('Variations', '''At SNR = 20 dB (100): 100<sup>−d</sup> ≤ 10⁻³ → d ≥ 1.5 → 2; r = 3 (d = 5) still works, r = 4 does not → R = 3 log₂100 = 19.9 bit/s/Hz. Given P<sub>e</sub> and d, the SNR is P<sub>e</sub><sup>−1/d</sup>.'''),
  ('Physical meaning', '''r is the number of independent data streams sent at once, d is the robustness against fading: the antennas can be used either to send more or to send more reliably.''')])

# ================================================================ Practice 6
EN['p6q1'] = dict(
 steps=[
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
The equaliser lowers the error rate about 15 times ✓.'''],
 ans='(b) Better with the equaliser: the worst-case effective distance is larger. E.g. α = 0.4: 0.6 without, 0.78 with',
 official='expressions as above; (b) Better to operate with the proposed equalizer ✓',
 kp=[
  ('What it tests', '''Error rate of an ISI channel; the equaliser trade-off between less ISI and more noise; comparison at high SNR (Ch 6 p.22–28).'''),
  ('Background', '''Multiplying Z-transforms = cascading filters; white noise through an FIR filter has variance σ²Σc²; average the conditional error rates; at high SNR the smallest Q argument dominates.'''),
  ('Method', '''Without equaliser: the previous symbol has the same or opposite sign, ½ each. With equaliser: the signal sees H(z)U(z) = 1 − α²z⁻², the noise sees only U(z) and its variance becomes (N₀/2)(1 + α²); again two cases.'''),
  ('Key comparison', '''(1 − α²)/√(1 + α²) &gt; 1 − α ⇔ (1 + α)/√(1 + α²) &gt; 1 ⇔ (1 + α)² &gt; 1 + α² ⇔ 2α &gt; 0, always true for α &gt; 0.'''),
  ('Common mistakes', '''The noise goes through U(z) only, not H(z); after equalisation the residual ISI is −α² at position n − 2, not zero; divide by √(1 + α²) times the standard deviation inside Q.'''),
  ('Numbers', '''α = 0.4: worst-case argument 0.6 without the equaliser, 0.84/1.077 = 0.78 with it, so the equaliser is better.'''),
  ('Link', '''Final-exam Q2(a) asked this four years running: residual ISI a plus amplified noise σ′, P<sub>e</sub> = ½[Q((1 − a)/σ′) + Q((1 + a)/σ′)].''')])

EN['p6q2'] = dict(
 steps=[
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
ZF is about 9 times better; as a → 0 both formulas become \(Q(1/\sqrt{0.1})=Q(3.16)\) ✓.'''],
 ans='(a) ½Q((1+a)/√0.1) + ½Q((1−a)/√0.1); (b) Q(√((1−a²)/0.1))', official='same as above ✓',
 note='''Comparison: the ZF Q argument is √(1−a²)/√0.1, the worst no-equaliser term is (1−a)/√0.1. Since √(1−a²) = √((1−a)(1+a)) &gt; 1−a, ZF is better at high SNR; but as a → 1 ZF amplifies the noise heavily.''',
 kp=[
  ('What it tests', '''Error rate with direct decisions (no equaliser) and with an ideal zero-forcing equaliser (Ch 6 p.23–28).'''),
  ('Background', '''Average the conditional error rates; ZF: C(z) = 1/H(z); geometric series Σa<sup>2k</sup> = 1/(1 − a²); filtered-noise variance σ²Σc².'''),
  ('Method', '''(a) Two cases b<sub>n−1</sub> = ±1, distances 1 ± a from the threshold, standard deviation √0.1. (b) 1/(1 + az⁻¹) = Σ(−a)<sup>k</sup>z<sup>−k</sup>; ISI vanishes, noise variance 0.1/(1 − a²), a single Q term.'''),
  ('Numbers', '''a = 0.5: (a) ½[Q(4.74) + Q(1.58)] ≈ 0.028; (b) Q(√7.5) = Q(2.74) ≈ 0.0031, ZF about 9 times better.'''),
  ('Comparison', '''At high SNR compare the worst Q arguments: ZF √(1 − a²), no equaliser 1 − a; √(1 − a²) = √((1 − a)(1 + a)) &gt; 1 − a, so ZF is better. But as a → 1 the noise amplification 1/(1 − a²) blows up.'''),
  ('Common mistakes', '''√0.1 is the standard deviation, 0.1 the variance; after ZF there is no ISI, so no case split; without the equaliser do not keep only the Q((1 − a)/σ) term.''')])

EN['p6q3'] = dict(
 steps=[
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
Check: starting at n = 1 (\(A_0=0\), so the first decision has no ISI), \(p_1=0.159\) and \(p_n=0.159+0.102\,p_{n-1}\): \(p_2=0.175\), \(p_3=0.177\), quickly converging to 0.177 ✓. Also 0.159 (no error propagation) &lt; 0.177 (DFE) &lt; 0.188 (linear equaliser), a sensible order.'''],
 ans='(a) q = 0, P<sub>e</sub> ≈ 0.19; (b) P<sub>e</sub> ≈ 0.18', official='(a) q = 0, P<sub>e</sub> ≈ 0.19; (b) P<sub>e</sub> ≈ 0.18 ✓',
 note='''Without error propagation the DFE error rate would be Q(1) = 0.159; error propagation raises it to 0.177, still better than the linear equaliser's 0.188.''',
 kp=[
  ('What it tests', '''Error rates of an MMSE linear equaliser and a decision-feedback equaliser; DFE error propagation (Ch 6 p.26–34).'''),
  ('Background', '''Mean squares of independent zero-mean variables add; A<sub>n</sub>² = 1; total probability; solving a linear equation for the steady state.'''),
  ('Method', '''(a) Split u<sub>n</sub> − A<sub>n</sub> into independent terms → MSE 1.25 + 2.25q² → derivative gives q = 0 → u<sub>n</sub> = y<sub>n</sub>, amplitude 1.5 or 0.5 → average. (b) Conditional error rates: previous correct → Q(1); previous wrong → ½Q(2) + ½ × ½ → solve the steady-state equation.'''),
  ('Why q = 0', '''Using the future sample y<sub>n+1</sub> adds ½A<sub>n</sub> of useful signal but also brings in A<sub>n+1</sub> interference and z<sub>n+1</sub> noise; the net effect is negative, so the best choice is not to use it.'''),
  ('Key formula', '''DFE steady state: p = (1 − p)·0.159 + p·0.261 → p = 0.159/(1 − 0.261 + 0.159) = 0.177.'''),
  ('Common mistakes', '''Dropping the (q/2)A<sub>n</sub> term when expanding; after a wrong decision the amplitude is 2 or 0 (the ISI doubles), and amplitude 0 gives error probability ½; solving the steady-state equation incorrectly.'''),
  ('Conclusion', '''Linear 0.188 &gt; DFE 0.177 &gt; DFE without error propagation 0.159: the DFE does not amplify noise, but error propagation eats part of the advantage (p.34).''')])

# ================================================================ Practice 7
EN['p7q1'] = dict(
 steps=[
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
Each sub-carrier occupies only B/4, \(C=\sum_k\frac B4\log_2(\cdot)\), so per hertz \(C/B=7.15/4=1.79\approx1.8\) bit/s/Hz (matches the official answer). Compare (c): only 0.447 bit/s/Hz, so water-filling is about 4 times higher.'''],
 ans='(a) B/B<sub>C</sub> ≪ N ≪ B/B<sub>d</sub>; (b) 1.4, 0.8−0.6j, 0.2, 0.8+0.6j; (c) 0.36, 9.09, 0.36, 0.19; (d) ≈ 1.8 bit/s/Hz',
 official='identical ✓ (the official solution labels k = 1…4 as H₁…H₄, with H₄ = H₀ = 1.4)',
 note='''Compare (c) and (d): to make every sub-channel "equal", (c) spends 91% of the power on the worst sub-channel; water-filling (d) simply abandons it and gets a much higher total capacity.''',
 kp=[
  ('What it tests', '''The four core OFDM calculations: choosing N, H<sub>k</sub>, equal-capacity power allocation, water-filling capacity (Ch 7 p.5, p.15, p.24; water-filling from Ch 2).'''),
  ('Background', '''Coherence bandwidth and coherence time; Euler: e<sup>−jπk/2</sup> is 1, −j, −1, j in turn; water-filling; log₂.'''),
  ('Method', '''(a) Flat N ≫ B/B<sub>C</sub>, slow N ≪ B/B<sub>d</sub>; (b) H<sub>k</sub> = h₀ + h₁e<sup>−j2πk/N</sup>; (c) |H<sub>k</sub>|²P<sub>k</sub> = c, find c from ΣP<sub>k</sub> = 10; (d) floors 1/|H<sub>k</sub>|², water level μ, drop sub-channels whose floor is above the water.'''),
  ('Key numbers', '''|H<sub>k</sub>|² = 1, 0.04, 1, 1.96; c = 10/27.51 = 0.3635; water level 4.17, powers 3.17, 0, 3.17, 3.66; 7.15 bit / 4 = 1.79 bit/s/Hz.'''),
  ('Check', '''Σ|H<sub>k</sub>|² = N Σh<sub>i</sub>² = 4 × (0.64 + 0.36) = 4; the powers in (c) and (d) both sum to 10; the dropped sub-channel 2 has floor 25, above the water level.'''),
  ('Common mistakes', '''Index k = 1…4 (H₄ = H₀); use |H<sub>k</sub>|², not |H<sub>k</sub>|; noise σ² = 1; divide by N at the end to get bit/s/Hz.'''),
  ('Conclusion', '''Equal capacity pours 91% of the power into the worst sub-channel; water-filling gives up on it. Use (c) for fairness, (d) for maximum total capacity.''')])

EN['p7q2'] = dict(
 steps=[
  r'''<b>Bit rate → symbol rate</b>: 16-QAM carries \(\log_2 16=4\) bits per symbol:
\[R_s=\frac{2\times10^6\text{ bit/s}}{4\text{ bit/symbol}}=5\times10^5\text{ symbols/s}\]''',
  r'''<b>OFDM timing</b>: with N sub-carriers the spacing is \(\Delta f=B/N\) and the useful symbol duration is \(T=1/\Delta f=N/B\) (Ch 7 p.8). With the cyclic prefix \(T_G=T_D=20\) µs one OFDM block lasts \(T+T_G\) (p.18), during which each of the N sub-carriers sends one symbol:
\[\text{symbol rate}=\frac{N}{T+T_G}=\frac{N}{N/B+T_G}\]''',
  r'''<b>Solve for N</b>: set it equal to \(R_s\):
\[\begin{aligned}N&=R_s\Big(\frac NB+T_G\Big)\\&=\tfrac{500\text{k}}{600\text{k}}N+500\text{k}\times20\ \mu\text{s}\\&=0.8333N+10\\ N&=\frac{10}{1-0.8333}=\frac{10}{0.1667}=60\end{aligned}\]''',
  r'''<b>Symbol durations</b>:
\[\begin{aligned}T&=\frac NB=\frac{60}{600\text{ kHz}}=100\ \mu\text{s}\\ T+T_G&=100+20=120\ \mu\text{s}=0.12\text{ ms}\end{aligned}\]
Sub-carrier spacing Δf = 600 kHz / 60 = 10 kHz = 1/T ✓.''',
  r'''<b>Check</b>: each OFDM block carries 60 × 4 = 240 bits, and 240 bits / 120 µs = 2 × 10⁶ bit/s = 2 Mbps ✓. The CP takes 20/120 = 1/6 of the time; the power loss is \(10\log_{10}(120/100)=0.79\) dB (Ch 7 p.18).'''],
 ans='N = 60, OFDM symbol duration 0.12 ms', official='60; 0.12 ms ✓',
 note='''Without the CP, 600 kHz would carry 500 k symbols/s for any N and the problem would have no unique answer. The CP overhead is what fixes N: the larger N, the smaller the CP fraction. Here the CP takes 20/120 = 1/6 of the time, so the bandwidth must exceed 500 k by 1/5, exactly 600 kHz.''',
 kp=[
  ('What it tests', '''OFDM system design: number of sub-carriers, OFDM symbol duration, CP overhead (Ch 7 p.8, p.17–18).'''),
  ('Background', '''Useful symbol duration T = N/B = 1/Δf; one OFDM block lasts T + T<sub>G</sub>, during which each sub-carrier sends one symbol.'''),
  ('Method', '''① Bit rate ÷ log₂M = required symbol rate; ② write N / (N/B + T<sub>G</sub>) = symbol rate; ③ solve for N; ④ T = N/B, total T + T<sub>G</sub>.'''),
  ('Key numbers', '''2 Mbps / 4 = 500 k symbols/s; N = 0.8333N + 10 → N = 60; T = 100 µs, total 120 µs.'''),
  ('Check', '''60 × 4 bit / 120 µs = 2 Mbps; the CP takes 1/6 of the time, power loss 10 log(120/100) = 0.79 dB.'''),
  ('Variations', '''With a 40 µs delay spread: N = 0.8333N + 20 → N = 120, T = 200 µs, total 240 µs. A larger delay spread needs a larger N to keep the CP fraction small.'''),
  ('Common mistakes', '''Without a CP any N would do and there would be no unique answer, so the CP must be included in the duration; the given rate is a bit rate, divide by 4 first.''')])

EN['p7q3'] = dict(
 steps=[
  r'''<b>Read the impulse response</b>: \(H(Z)=\sum_ih_iZ^{-i}\), and \(Z^{-1}\) means one sample later. So \(h_0=1\) (direct path) and \(h_1=0.9\) (an echo one sample late): channel length L = 2, longest echo L − 1 = 1 sample late.''',
  r'''<b>Where the ISI comes from</b>: a received sample is \(r_i=x_i+0.9x_{i-1}+w_i\). The first sample of a block, i = 0, uses \(x_{-1}\); without a CP that is the last sample of the <b>previous</b> block, which causes inter-block interference (ISI). For i ≥ 1 only the current block is used, so just 1 sample per block is corrupted.''',
  r'''<b>Add a 1-sample CP</b>: copy the last sample of the block to its front: \(x_{-1}=x_{N-1}\). The receiver discards the CP sample \(r_{-1}\) (it contains the echo of the previous block); the first sample kept is
\[r_0=x_0+0.9\,x_{N-1}+w_0\]
which contains only current-block data: the ISI is caught inside the CP.''',
  r'''<b>Why copy the tail</b>: the N kept samples satisfy \(r_i=\sum_lh_lx_{(i-l)\bmod N}+w_i\), a circular convolution. After the DFT this gives exactly \(R_k=H_kS_k+W_k\) (Ch 7 p.22) with \(H_k=1+0.9e^{-j2\pi k/N}\): the sub-carriers stay orthogonal, there is no ICI, and one complex division \(\hat s_k=R_k/H_k\) equalises each sub-carrier. A guard interval filled with zeros would also block the ISI, but it breaks the circular structure and ICI appears.''',
  r'''<b>Conclusion and check</b>: minimum CP = L − 1 = 1 sample (one symbol duration \(T_S\)). G = 0 fails (ISI and ICI); G = 2 also works but wastes a sample and lowers the efficiency N/(N + G). Check with N = 4: the kept samples are \(r_0=x_0+0.9x_3\), \(r_1=x_1+0.9x_0\), \(r_2=x_2+0.9x_1\), \(r_3=x_3+0.9x_2\), exactly the 4-point circular convolution of [1, 0.9] with x ✓. The size of the coefficient 0.9 does not affect the CP length; only how many samples the echo is delayed matters.'''],
 ans='Minimum CP = 1 sample (symbol) = L − 1', official='1 symbol length ✓',
 kp=[
  ('What it tests', '''The minimum cyclic-prefix length (Ch 7 p.17–22).'''),
  ('Background', '''Z-transform: Z⁻¹ means one sample later; a channel with L taps has its longest echo L − 1 samples late.'''),
  ('Method', '''Read the impulse response h = [1, 0.9] from H(Z) → L = 2 → CP ≥ L − 1 = 1 sample.'''),
  ('Why it is enough', '''With CP ≥ L − 1 the N samples kept by the receiver contain only data from the current block, the linear convolution becomes circular, and after the DFT r<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + w<sub>k</sub> (derivation box in Section 7.4 of the learning page).'''),
  ('Why copy the tail', '''An empty guard interval would also block the previous block's echo, but the receive window would no longer see a complete periodic signal, the sub-carriers would lose orthogonality and ICI would appear. Only copying the tail keeps the circular structure.'''),
  ('Common mistakes', '''It is L − 1 = 1 sample, not L = 2; the size of the coefficient 0.9 does not matter, only how many samples the echo is delayed.'''),
  ('Variations', '''H(Z) = 1 + 0.5Z⁻³ → delay 3 samples → CP ≥ 3; in time, T<sub>G</sub> ≥ the maximum delay spread T<sub>D</sub>. Each extra CP sample lowers the efficiency to N/(N + G).''')])

# ---------------------------------------------------------------- mock Quiz (self-written, group P8)
EN['p8q1'] = dict(
 idea=r'''(a) Split into cases and weight them: total probability. (b) The result (an error) is known and we ask about the cause (the state): Bayes' rule. (c) Mean and variance of a discrete random variable, after converting dB to linear values.''',
 steps=[
  r'''<b>(a) Table of states</b>: the two states are mutually exclusive and cover all cases: P(G) + P(B) = 0.7 + 0.3 = 1 ✓, so {G, B} is a partition. The given bit error probabilities are conditional probabilities \(P(e\mid G)=10^{-4}\) and \(P(e\mid B)=10^{-2}\). First use the multiplication rule (Ch 1b p.6) for the two joint probabilities:
\[\begin{aligned}P(G\cap e)&=P(G)\,P(e\mid G)\\&=0.7\times10^{-4}=7\times10^{-5}\\P(B\cap e)&=P(B)\,P(e\mid B)\\&=0.3\times10^{-2}=3\times10^{-3}\end{aligned}\]''',
  r'''<b>(a) Total probability</b>: when an error occurs the link is in exactly one of G or B, so add the two terms; this is the total probability theorem (p.8):
\[\begin{aligned}P_e&=P(G)P(e\mid G)+P(B)P(e\mid B)\\&=7\times10^{-5}+3\times10^{-3}\\&=0.00307=3.07\times10^{-3}\end{aligned}\]
Check: the average lies between \(10^{-4}\) and \(10^{-2}\) ✓; it is close to the bad-state term because \(3\times10^{-3}\) is 43 times \(7\times10^{-5}\).''',
  r'''<b>(b) Bayes' rule</b>: the result (an error) is known and we ask about the cause (the bad state), so use Bayes' rule (p.9). The numerator is the bad-state term of (a); the denominator is the total from (a):
\[\begin{aligned}P(B\mid e)&=\frac{P(B)\,P(e\mid B)}{P_e}\\&=\frac{3\times10^{-3}}{3.07\times10^{-3}}=0.977\end{aligned}\]''',
  r'''<b>(b) Check</b>: for the other state \(P(G\mid e)=\dfrac{7\times10^{-5}}{3.07\times10^{-3}}=0.023\), and the two posterior probabilities add up to 0.977 + 0.023 = 1 ✓. The probability of the bad state rises from 0.3 before the observation (a priori) to 0.977 after it (a posteriori), because an error is 100 times more likely in the bad state.''',
  r'''<b>(c) dB to linear</b>: \(\gamma=10^{\gamma_{dB}/10}\): 10 dB → \(10^{1}=10\), 0 dB → \(10^{0}=1\). So the SNR is a discrete random variable: γ = 10 with probability 0.7 and γ = 1 with probability 0.3. dB is logarithmic and cannot be averaged directly; convert to linear first.''',
  r'''<b>(c) Mean</b>: expectation of a discrete random variable, \(E[\gamma]=\sum\gamma\,P(\gamma)\) (p.10):
\[\begin{aligned}E[\gamma]&=0.7\times10+0.3\times1=7+0.3=7.3\\ \bar\gamma_{dB}&=10\log_{10}7.3=10\times0.8633\\&=8.63\text{ dB}\end{aligned}\]''',
  r'''<b>(c) Variance</b>: use \(\mathrm{Var}(\gamma)=E[\gamma^2]-(E[\gamma])^2\) (p.11), so find the second moment first:
\[\begin{aligned}E[\gamma^2]&=0.7\times10^2+0.3\times1^2\\&=70+0.3=70.3\\ \mathrm{Var}(\gamma)&=70.3-7.3^2=70.3-53.29\\&=17.01\end{aligned}\]
Standard deviation \(\sqrt{17.01}=4.12\). Check with the definition \(E[(\gamma-\mu)^2]\):
\[\begin{aligned}&0.7\times(10-7.3)^2+0.3\times(1-7.3)^2\\&=5.103+11.907=17.01\ \checkmark\end{aligned}\]'''],
 ans='(a) 3.07 × 10⁻³; (b) 0.977; (c) E[γ] = 7.3 (8.63 dB), Var(γ) = 17.0',
 official='none (self-written mock question); all numbers checked by src/p2build/verify_mock.py',
 note='''Averaging the dB values gives 0.7 × 10 + 0.3 × 0 = 7 dB, which is wrong: dB is logarithmic, so convert to linear before averaging. The lecturer said a missing dB ↔ linear conversion loses marks. Part (b) is typical: the bad state occupies only 30% of the time but causes 97.7% of the errors.''',
 kp=[
  ('What it tests', '''Total probability, Bayes' rule (blue box, memorise), mean and variance of a discrete random variable (Ch 1b p.5–14, Quiz scope).'''),
  ('Background', '''P(B) = ΣP(A<sub>i</sub>)P(B | A<sub>i</sub>); P(A<sub>i</sub> | B) = P(A<sub>i</sub>)P(B | A<sub>i</sub>)/P(B); E[X] = Σx·p(x); Var(X) = E[X²] − (E[X])².'''),
  ('Method', '''Make a table of state, probability and conditional probability. (a) Weighted sum; (b) the matching term of (a) divided by the total of (a); (c) convert to linear, then E[X] and E[X²] from the table.'''),
  ('Common mistakes', '''Averaging dB values (7 dB, wrong); forgetting to subtract the squared mean; the Bayes denominator is the total error probability from total probability; total probability must sum over all states (a past mistake the lecturer pointed out).'''),
  ('Intuition', '''The bad state is 30% of the time but gives 97.7% of the errors: the average error rate is set almost entirely by the bad periods, which is why Ch 4 uses diversity.'''),
  ('Variations', '''A three-state channel works the same with one more row; or "probability that two consecutive bits are both wrong" (multiply if independent).'''),
  ('Link', '''Practice 4 Q2 (average error rate over a discrete SNR); P2 Q2 (c) is the continuous version of total probability.''')])

EN['p8q2'] = dict(
 idea=r'''Convert mW to dBm and use the dB form for the average received power. The amount by which the average exceeds the threshold is the margin, and outage = Q(margin/σ). For (c), work backwards: 1% → inverse Q → required margin → distance.''',
 steps=[
  r'''<b>Units first</b>: in the dB form the powers must be in dBm: \(P_t=10\log_{10}\dfrac{100\text{ mW}}{1\text{ mW}}=10\times2=20\) dBm (leaving it in mW loses marks).''',
  r'''<b>(a) dB form</b>: take \(10\log_{10}\) of both sides of \(P_r=P_tK(d_0/d)^{\gamma}\); products become sums and the power becomes a factor (Ch 2 p.8):
\[\begin{aligned}P_{r,dBm}&=P_{t,dBm}+K_{dB}-10\gamma\log_{10}\frac{d}{d_0}\\&=20-31.5-36\log_{10}d\end{aligned}\]
Here \(10\gamma=10\times3.6=36\); d₀ = 1 m, so d is entered directly in metres.''',
  r'''<b>(a) Substitute d = 300 m</b>: \(\log_{10}300=2.477\):
\[\begin{aligned}P_r(300\text{ m})&=20-31.5-36\times2.477\\&=20-31.5-89.18\\&=-100.68\text{ dBm}\end{aligned}\]
This is the average due to path loss alone; shadowing makes the actual power fluctuate around it.''',
  r'''<b>(b) Margin</b>: outage means the received power is below −110 dBm. The amount by which the average power exceeds the threshold is the margin:
\[x=\bar P_r-P_{min}=-100.68-(-110)=9.32\text{ dB}\]
The shadowing is \(\psi_{dB}\sim\mathcal N(0,\sigma^2)\), so \(P_{out}=P(\psi_{dB}\lt-x)=Q(x/\sigma)\) (p.14–15).''',
  r'''<b>(b) Q table</b>: \(x/\sigma=9.32/6=1.553\). From the Q table, Q(1.55) = 0.0606 and Q(1.56) = 0.0594; 1.553 lies between them, so interpolate:
\[\begin{aligned}P_{out}=Q(1.553)&\approx0.0606-0.3\times0.0012\\&\approx0.060\end{aligned}\]
About 6.0%. Check: 1 &lt; 1.553 &lt; 2, so the result must lie between Q(1) = 0.159 and Q(2) = 0.023 ✓.''',
  r'''<b>(c) Inverse Q lookup</b>: we need \(Q(x/\sigma)\le0.01\). Q decreases as its argument grows, so the margin must be large enough. From the Q table, Q(2.32) = 0.0102 and Q(2.33) = 0.0099, giving \(Q^{-1}(0.01)=2.326\):
\[\begin{aligned}x&\ge2.326\times6=13.96\text{ dB}\\ \bar P_r&\ge-110+13.96=-96.04\text{ dBm}\end{aligned}\]''',
  r'''<b>(c) Solve for the distance</b>: put the expression from (a) into the inequality and rearrange:
\[\begin{aligned}20-31.5-36\log_{10}d&\ge-96.04\\36\log_{10}d&\le20-31.5+96.04\\&=84.54\\ \log_{10}d&\le84.54/36=2.348\\ d&\le10^{2.348}\approx223\text{ m}\end{aligned}\]
Check: put d = 223 m back:
\[\begin{aligned}P_r(223\text{ m})&=20-31.5-36\log_{10}223\\&=-11.5-84.54=-96.04\text{ dBm}\ \checkmark\end{aligned}\]
and 223 m &lt; 300 m agrees with the 6% &gt; 1% outage found at 300 m in (b) ✓.'''],
 ans='(a) P<sub>r,dB</sub> = P<sub>t,dB</sub> + K<sub>dB</sub> − 36 log₁₀d, ≈ −100.7 dBm at 300 m; (b) P<sub>out</sub> ≈ 6.0%; (c) d<sub>max</sub> ≈ 223 m',
 official='none (self-written mock question); all numbers checked by src/p2build/verify_mock.py',
 note='''At 300 m the outage is 6%, far above the usual 1% target. To reach 1%, either shrink the coverage radius to about 223 m or raise the transmit power by 13.96 − 9.32 = 4.64 dB.''',
 kp=[
  ('What it tests', '''dB form of the simplified path loss model (memorise), shadowing outage P<sub>out</sub> = Q(margin/σ) (memorise), inverse Q lookup (Ch 2 p.8, p.12–16).'''),
  ('Background', '''P<sub>r,dB</sub> = P<sub>t,dB</sub> + K<sub>dB</sub> − 10γ log₁₀(d/d₀); mW → dBm: 10 log₁₀(value in mW); Q(2.326) = 0.01.'''),
  ('Method', '''① Convert units; ② average power from the model; ③ margin = average − threshold; ④ P<sub>out</sub> = Q(margin/σ). For the distance, reverse it: outage target → inverse Q → margin = xσ → minimum average power → solve for d.'''),
  ('Key step', '''(c) Margin 13.96 dB → average power ≥ −96.04 dBm → 36 log₁₀d ≤ 84.54 → d ≤ 223 m.'''),
  ('Common mistakes', '''Using 100 mW without converting to 20 dBm (loses marks); 10γ = 36, not 3.6; Q takes margin over σ, not over σ².'''),
  ('Variations', '''Required transmit power for a given distance; or the largest allowed σ for a given outage (asked in 2023-24 S2 Q1(a)(ii)).'''),
  ('Link', '''Practice 1 Q2 (outage forwards and backwards); Practice 1 Q1 (b).''')])

EN['p8q3'] = dict(
 idea=r'''(a) Use the linear power of each path as a weight and find the weighted mean and standard deviation of the delay. (b) Judge two dimensions separately: σ against T<sub>s</sub> for flat / frequency-selective, T<sub>C</sub> against T<sub>s</sub> for fast / slow. (c) Get the amplitude ratio ρ from "10 dB below" first, then use the AFD formula.''',
 steps=[
  r'''<b>(a) dB to linear</b>: the weights of the power delay profile must be linear powers (Ch 2 p.30), \(P=10^{P_{dB}/10}\):
\[\begin{aligned}0\text{ dB}&\to1,\qquad-3\text{ dB}\to10^{-0.3}=0.501\\-6\text{ dB}&\to10^{-0.6}=0.251\\ \sum_kP(\tau_k)&=1+0.501+0.251=1.752\end{aligned}\]''',
  r'''<b>(a) Mean delay</b>: the power-weighted average:
\[\begin{aligned}\mu_{T_m}&=\frac{\sum_k\tau_kP(\tau_k)}{\sum_kP(\tau_k)}\\&=\frac{0\times1+1\times0.501+3\times0.251}{1.752}\\&=\frac{1.255}{1.752}=0.716\ \mu\text{s}\end{aligned}\]
Check: μ lies between 0 and 3 µs and close to 0, because the strongest path is at τ = 0 ✓.''',
  r'''<b>(a) rms delay spread</b>: find the second moment, then use "variance = second moment − mean²":
\[\begin{aligned}\overline{\tau^2}&=\frac{0+1^2\times0.501+3^2\times0.251}{1.752}\\&=\frac{0.501+2.261}{1.752}=\frac{2.762}{1.752}=1.576\ \mu\text{s}^2\\ \sigma_{T_m}&=\sqrt{1.576-0.716^2}=\sqrt{1.576-0.513}\\&=\sqrt{1.063}=1.03\ \mu\text{s}\end{aligned}\]
Check with the definition \(\sigma^2=\sum_k(\tau_k-\mu)^2P(\tau_k)/\sum_kP(\tau_k)\):
\[\begin{aligned}&0.716^2\times1+0.284^2\times0.501+2.284^2\times0.251\\&=0.513+0.040+1.310=1.863\\&1.863/1.752=1.063\ \checkmark\end{aligned}\]''',
  r'''<b>(b) Flat or selective</b>: symbol duration \(T_s=1/R_s=1/(50\times10^3)=20\ \mu\)s. Rule of thumb (p.33): \(\sigma_{T_m}/T_s\lt0.1\) means flat fading:
\[\frac{\sigma_{T_m}}{T_s}=\frac{1.03\ \mu\text{s}}{20\ \mu\text{s}}=0.052\lt0.1\]
→ <b>flat fading</b>: the delay spread is only about 5% of a symbol, the paths arrive almost together, and there is no significant inter-symbol interference (ISI).''',
  r'''<b>(b) Doppler and coherence time</b>: convert the speed first, v = 72/3.6 = 20 m/s. Maximum Doppler shift (p.34) and coherence time (p.36):
\[\begin{aligned}f_m&=\frac{vf_c}{c}=\frac{20\times1.8\times10^9}{3\times10^8}=120\text{ Hz}\\T_C&\approx\frac1{f_m}=\frac1{120}=8.33\text{ ms}\end{aligned}\]''',
  r'''<b>(b) Fast or slow</b>: compare T<sub>C</sub> with T<sub>s</sub> (p.37): \(T_s/T_C=20\ \mu\text{s}/8.33\text{ ms}=2.4\times10^{-3}\ll1\), so the channel hardly changes during a symbol → <b>slow fading</b>. The frequency view agrees: \(B_D=f_m=120\) Hz ≪ \(B_s\approx50\) kHz. Conclusion: <b>flat, slow fading</b>.''',
  r'''<b>(c) Find ρ</b>: ρ is an amplitude ratio, \(\rho=Z_{min}/Z_{rms}\) (p.41), but "10 dB below" refers to power. The power ratio is \(10^{-10/10}=0.1\), and the amplitude ratio is its square root:
\[\rho^2=0.1,\qquad\rho=\sqrt{0.1}=0.316\]''',
  r'''<b>(c) Average fade duration</b>: use the given AFD formula (p.43) with \(\sqrt{2\pi}=2.507\) and \(e^{0.1}=1.1052\):
\[\begin{aligned}\bar\tau&=\frac{e^{\rho^2}-1}{\sqrt{2\pi}f_m\rho}=\frac{e^{0.1}-1}{2.507\times120\times0.316}\\&=\frac{0.1052}{95.1}=1.106\times10^{-3}\text{ s}\approx1.11\text{ ms}\end{aligned}\]''',
  r'''<b>(c) Symbols affected</b>: one fade lasts \(\bar\tau\) on average and one symbol lasts T<sub>s</sub>; the ratio is the number of symbols covered by one fade (p.46):
\[\frac{\bar\tau}{T_s}=\frac{1.106\text{ ms}}{20\ \mu\text{s}}=55.3\approx55\]
Check: LCR \(L_Z=\sqrt{2\pi}f_m\rho e^{-\rho^2}=95.1\times0.905=86.1\) per second, and \(L_Z\bar\tau=86.1\times1.106\times10^{-3}=0.095\), exactly \(1-e^{-0.1}=0.095\) ✓ (the fraction of time below the threshold, p.43).'''],
 ans='(a) μ ≈ 0.72 µs, σ ≈ 1.03 µs; (b) f<sub>m</sub> = 120 Hz, T<sub>C</sub> ≈ 8.3 ms, flat slow fading; (c) AFD ≈ 1.1 ms, about 55 symbols per fade',
 official='none (self-written mock question); all numbers checked by src/p2build/verify_mock.py',
 note='''Taking ρ = 0.1 by mistake gives AFD = 0.33 ms, more than 3 times too small. Also LCR = √(2π) × 120 × 0.316 × e<sup>−0.1</sup> ≈ 86 per second, and AFD × LCR = 1 − e<sup>−0.1</sup> ≈ 0.095: the signal is below the threshold about 9.5% of the time.''',
 kp=[
  ('What it tests', '''μ and σ of a discrete power delay profile (Ch 2 p.30); fading type in two dimensions, flat/selective and fast/slow (p.33–36); average fade duration (p.42–43).'''),
  ('Background', '''Power-weighted: μ = ΣP<sub>i</sub>τ<sub>i</sub>/ΣP<sub>i</sub>, σ = √(E[τ²] − μ²); σ/T<sub>s</sub> &lt; 0.1 → flat (memorise); f<sub>m</sub> = v f<sub>c</sub>/c, T<sub>C</sub> ≈ 1/f<sub>m</sub>; ρ = threshold amplitude / rms amplitude.'''),
  ('Method', '''(a) dB → linear → weighted mean and second moment from a table; (b) compare T<sub>s</sub> with σ and with T<sub>C</sub>; (c) square root of the power ratio gives ρ → AFD → divide by T<sub>s</sub> for the symbol count.'''),
  ('Common mistakes', '''Using dB values as weights; "10 dB down in power" means ρ = √0.1, not 0.1; answering only one dimension of the fading type gets half marks (the lecturer said so), give both flat/selective and fast/slow; convert km/h to m/s.'''),
  ('Check', '''AFD × LCR = 1 − e<sup>−ρ²</sup> = 0.095: the signal is below the threshold about 9.5% of the time.'''),
  ('Variations', '''At 200 k symbols/s, T<sub>s</sub> = 5 µs and σ/T<sub>s</sub> = 0.21, so the fading can no longer be called flat.'''),
  ('Link', '''Practice 1 Q3 (continuous delay profile); Practice 2 Q1 (AFD); 2025-26 S2 Q1(a)(i)(ii).''')])

EN['p8q4'] = dict(
 idea=r'''In Rayleigh fading the instantaneous SNR is exponentially distributed and the outage probability is its CDF; (b) solves it backwards for the average SNR; (c) uses the exponential tail directly.''',
 steps=[
  r'''<b>(a) State the pdf</b>: in Rayleigh fading the envelope z is Rayleigh distributed, so the power z² is exponential and so is the instantaneous SNR (Ch 2 p.25–26):
\[p(\gamma)=\frac1{\bar\gamma}e^{-\gamma/\bar\gamma},\qquad\gamma\ge0\]
where γ̄ is the average SNR (linear).''',
  r'''<b>(a) Outage formula</b>: outage means the instantaneous SNR is below the threshold γ₀; integrate the pdf from 0 to γ₀ (this is the CDF):
\[\begin{aligned}P_{out}&=\int_0^{\gamma_0}\frac1{\bar\gamma}e^{-\gamma/\bar\gamma}d\gamma\\&=\Big[-e^{-\gamma/\bar\gamma}\Big]_0^{\gamma_0}=1-e^{-\gamma_0/\bar\gamma}\end{aligned}\]''',
  r'''<b>(a) Convert to linear and substitute</b>: \(\bar\gamma=10^{20/10}=100\), \(\gamma_0=10^{7/10}=10^{0.7}=5.01\):
\[\begin{aligned}\gamma_0/\bar\gamma&=5.01/100=0.0501\\P_{out}&=1-e^{-0.0501}=1-0.9511\\&=0.0489\approx4.9\%\end{aligned}\]
Check: for small x, \(1-e^{-x}\approx x=0.050\) ✓.''',
  r'''<b>(b) Solve for the average SNR</b>: set \(P_{out}=\varepsilon=0.01\) with the same threshold γ₀ = 5.01:
\[\begin{aligned}e^{-\gamma_0/\bar\gamma}&=1-0.01=0.99\\ \frac{\gamma_0}{\bar\gamma}&=\ln\frac1{0.99}=0.01005\\ \bar\gamma&=\frac{5.01}{0.01005}=498.7\\ \bar\gamma_{dB}&=10\log_{10}498.7=26.98\approx27.0\text{ dB}\end{aligned}\]''',
  r'''<b>(b) Fade margin and check</b>: fade margin = required average SNR − threshold; in dB simply subtract:
\[FM=26.98-7=19.98\approx20.0\text{ dB}\]
This matches the formula on p.51: \(10\log_{10}\dfrac1{\ln(1/0.99)}=10\log_{10}99.5=19.98\) dB ≈ \(10\log_{10}(1/\varepsilon)=20\) dB ✓. Back-substitution: \(1-e^{-5.01/498.7}=1-e^{-0.01005}=0.0100\) ✓.''',
  r'''<b>(c) Tail of the exponential</b>: integrate from γ̄ to ∞:
\[\begin{aligned}P(\gamma\gt\bar\gamma)&=\int_{\bar\gamma}^{\infty}\frac1{\bar\gamma}e^{-\gamma/\bar\gamma}d\gamma\\&=e^{-\bar\gamma/\bar\gamma}=e^{-1}=0.368\end{aligned}\]
The result does not depend on γ̄. The exponential distribution has a long right tail: a few large values pull the mean up, so the SNR is above its mean only 36.8% of the time and below it 63.2% of the time.'''],
 ans='(a) p(γ) = (1/γ̄)e<sup>−γ/γ̄</sup>, P<sub>out</sub> ≈ 4.9%; (b) γ̄ ≈ 27 dB, fade margin ≈ 20 dB; (c) e⁻¹ ≈ 0.368',
 official='none (self-written mock question); all numbers checked by src/p2build/verify_mock.py',
 note='''Part (c) shows that in Rayleigh fading the instantaneous SNR is above its average only about 37% of the time; most of the time it is below, which is why a fade margin is needed. In an AWGN channel without fading the SNR always equals its average, so an average of 7 dB would be enough; Rayleigh fading needs 20 dB more.''',
 kp=[
  ('What it tests', '''Exponential SNR distribution in Rayleigh fading (memorise), Rayleigh outage (memorise), fade margin (try to remember) (Ch 2 p.25–26, p.51).'''),
  ('Background', '''p(γ) = (1/γ̄)e<sup>−γ/γ̄</sup>; P(γ &lt; γ₀) = 1 − e<sup>−γ₀/γ̄</sup>; P(γ &gt; x) = e<sup>−x/γ̄</sup>; ln(1/(1 − ε)) ≈ ε.'''),
  ('Method', '''Convert every dB value to linear → 1 − e<sup>−γ₀/γ̄</sup>; backwards γ̄ = γ₀ / ln(1/(1 − ε)); fade margin = γ̄<sub>dB</sub> − γ<sub>0,dB</sub>.'''),
  ('Key step', '''For ε = 1%, ln(1/0.99) = 0.01005, so γ̄ ≈ 100γ₀ and the fade margin ≈ 20 dB.'''),
  ('Common mistakes', '''Putting dB values into the exponent; the formula to memorise is the exponential SNR distribution, not the Rayleigh envelope PDF; the fade margin is a difference of two dB values.'''),
  ('Quick rule', '''ε = 1% → 20 dB, 0.5% → 23 dB, 0.1% → 30 dB: each 10 times stricter outage needs 10 dB more margin.'''),
  ('Link', '''Learning page sections 2.3 and 2.7; 2025-26 S2 Q1(a)(iii) (outage capacity and fade margin of a Rayleigh channel).''')])

EN['p8q5'] = dict(
 idea=r'''Same method as Practice 1 Q1: in dB the model is a straight line \(M=K_{dB}-\gamma x\) with \(x=10\log_{10}d\). Least squares gives the slope and intercept, the mean squared residual is the shadowing variance, then Q(margin/σ).''',
 steps=[
  r'''<b>Change the x axis</b>: in dB the model is \(M=(P_r/P_t)_{dB}=K_{dB}-10\gamma\log_{10}(d/d_0)\) (Ch 2 p.12–13). With \(x=10\log_{10}d\) (d₀ = 1 m) it is a straight line \(M=K_{dB}-\gamma x\): intercept K<sub>dB</sub>, slope −γ.
\[\begin{aligned}x_i&=10\log_{10}d_i=10,\ 13.01,\ 16.99,\ 20\\ \bar x&=(10+13.01+16.99+20)/4=15.00\\ \bar M&=(-68-86-91-105)/4=-87.5\end{aligned}\]''',
  r'''<b>(a) Least-squares formulas</b>: minimise the sum of squared errors \(F=\sum_i(M_i-K_{dB}+\gamma x_i)^2\) (p.13: minimum MSE). Setting the partial derivatives with respect to K<sub>dB</sub> and γ to zero gives
\[\begin{aligned}K_{dB}&=\bar M+\gamma\bar x\\ \gamma&=-\frac{\sum(x_i-\bar x)(M_i-\bar M)}{\sum(x_i-\bar x)^2}\end{aligned}\]
The first equation says the fitted line always passes through the mean point \((\bar x,\bar M)\).''',
  r'''<b>(a) Table of sums</b>: subtract the means, then multiply row by row:
<div class="tw"><table class="mini"><thead><tr><th>d (m)</th><th>\(x_i-\bar x\)</th><th>\(M_i-\bar M\)</th><th>product</th><th>\((x_i-\bar x)^2\)</th></tr></thead><tbody>
<tr><td>10</td><td>−5</td><td>19.5</td><td>−97.500</td><td>25</td></tr>
<tr><td>20</td><td>−1.990</td><td>1.5</td><td>−2.985</td><td>3.959</td></tr>
<tr><td>50</td><td>1.990</td><td>−3.5</td><td>−6.964</td><td>3.959</td></tr>
<tr><td>100</td><td>5</td><td>−17.5</td><td>−87.500</td><td>25</td></tr>
<tr><td colspan="3">sum</td><td>−194.95</td><td>57.92</td></tr>
</tbody></table></div>
Check: \(\sum(x_i-\bar x)=0\) and \(\sum(M_i-\bar M)=19.5+1.5-3.5-17.5=0\) ✓.''',
  r'''<b>(a) γ and K<sub>dB</sub></b>:
\[\begin{aligned}\gamma&=-\frac{-194.95}{57.92}=3.366\approx3.37\\K_{dB}&=-87.5+3.366\times15\\&=-87.5+50.49=-37.0\text{ dB}\end{aligned}\]
γ = 3.37 lies in the typical ranges of the table on p.9 (e.g. urban micro-cells 2.7–3.5), so it is reasonable ✓.''',
  r'''<b>(b) Predictions and residuals</b>: \(\hat M_i=K_{dB}-\gamma x_i=-37.01-3.366x_i\), residual \(e_i=M_i-\hat M_i\):
<div class="tw"><table class="mini"><thead><tr><th>d (m)</th><th>\(\gamma x_i\)</th><th>\(\hat M_i\)</th><th>\(M_i\)</th><th>\(e_i\)</th></tr></thead><tbody>
<tr><td>10</td><td>33.66</td><td>−70.67</td><td>−68</td><td>+2.670</td></tr>
<tr><td>20</td><td>43.79</td><td>−80.80</td><td>−86</td><td>−5.197</td></tr>
<tr><td>50</td><td>57.19</td><td>−94.20</td><td>−91</td><td>+3.197</td></tr>
<tr><td>100</td><td>67.32</td><td>−104.33</td><td>−105</td><td>−0.670</td></tr>
</tbody></table></div>
Check: the residuals sum to 2.670 − 5.197 + 3.197 − 0.670 = 0 ✓ (the line passes through the mean point, so the residuals always add up to 0).''',
  r'''<b>(b) Shadowing variance</b>: p.13: MSE \(=E[X_i^2]=\sigma_{\psi_{dB}}^2\), the mean of the squared residuals (divide by n = 4):
\[\begin{aligned}\sigma_\psi^2&=\frac{2.670^2+5.197^2+3.197^2+0.670^2}{4}\\&=\frac{7.13+27.01+10.22+0.45}{4}\\&=\frac{44.81}{4}=11.2\text{ dB}^2\\ \sigma_\psi&=\sqrt{11.2}=3.35\text{ dB}\end{aligned}\]''',
  r'''<b>(c) Outage probability</b>: the margin is 8 dB, and the Q function takes the standard deviation σ, not the variance (p.15):
\[P_{out}=Q\Big(\frac{8}{3.35}\Big)=Q(2.39)=8.4\times10^{-3}\]
Q table: Q(2.39) = 0.00842, i.e. about 0.84%. Check: the margin is about 2.4σ, so the result must lie between Q(2) = 0.023 and Q(2.5) = 0.0062 ✓.'''],
 ans='(a) γ ≈ 3.37, K<sub>dB</sub> ≈ −37.0 dB; (b) σ²<sub>ψ</sub> ≈ 11.2 dB² (σ ≈ 3.35 dB); (c) P<sub>out</sub> ≈ 0.84%',
 official='none (self-written mock question); all numbers checked by src/p2build/verify_mock.py',
 note='''Fewer points than Practice 1 Q1, which is a more likely size for a 30-minute quiz. Always use 10 log₁₀d on the x axis; the slope is −γ, keep the sign; the MSE is a variance, take the square root before using Q.''',
 kp=[
  ('What it tests', '''Least-squares fit of the simplified path loss model, shadowing variance = MSE, shadowing outage (Ch 2 p.8–16).'''),
  ('Background', '''In dB the model is the line M = K<sub>dB</sub> − γx with x = 10 log₁₀d; slope = Σ(x − x̄)(M − M̄)/Σ(x − x̄)²; the fitted line passes through (x̄, M̄).'''),
  ('Method', '''Table of x, x − x̄, M − M̄, products and squares → slope → γ = −slope → K<sub>dB</sub> = M̄ + γx̄ → residuals → MSE → Q(margin/σ).'''),
  ('Key formulas', '''γ = −Σ(x − x̄)(M − M̄)/Σ(x − x̄)²; K<sub>dB</sub> = M̄ + γx̄; σ²<sub>ψ</sub> = (1/n)Σe<sub>i</sub>².'''),
  ('Common mistakes', '''Using log₁₀d instead of 10 log₁₀d makes γ 10 times too large; the slope is −γ; the MSE divides by n (the slides' definition); take the square root before Q.'''),
  ('Check', '''The residuals sum to 0 (2.67 − 5.20 + 3.20 − 0.67 = 0).'''),
  ('Link', '''Practice 1 Q1 (the same method with 6 points).''')])

EN['p8q6'] = dict(
 idea=r'''Noise power = N₀ × B, which in dB is a sum. Convert the SNR to linear before Shannon's formula. For (c), water-filling first assumes every subchannel gets power, then checks whether any SNR is below the cut-off γ₀; if so, drop it and recompute.''',
 steps=[
  r'''<b>(a) Noise power</b>: the noise power is \(N=N_0B\); in dB the product becomes a sum:
\[\begin{aligned}10\log_{10}(5\times10^6)&=10\times(0.699+6)=66.99\text{ dB}\\N&=-174+66.99=-107.01\text{ dBm}\end{aligned}\]''',
  r'''<b>(a) SNR</b>: dBm − dBm = dB, then convert to linear:
\[\begin{aligned}\mathrm{SNR}&=-90-(-107.01)=17.01\text{ dB}\\ \gamma&=10^{17.01/10}=10^{1.701}=50.2\end{aligned}\]''',
  r'''<b>(a) Shannon capacity</b>: \(C=B\log_2(1+\gamma)\) (Ch 2 p.48) with γ in linear form; \(\log_2x=\log_{10}x/0.301\):
\[\begin{aligned}\log_2(1+50.2)&=\frac{\log_{10}51.2}{0.301}=\frac{1.710}{0.301}=5.68\\C&=5\times10^6\times5.68=28.4\text{ Mbps}\end{aligned}\]
Check: at high SNR every 3 dB is worth about 1 bit/s/Hz, and 17/3 ≈ 5.7 ✓.''',
  r'''<b>(b) New SNR</b>: the received power is unchanged and the noise power is proportional to B, so doubling the bandwidth adds \(10\log_{10}2=3.01\) dB of noise:
\[\begin{aligned}N&=-174+10\log_{10}10^7\\&=-174+70=-104.0\text{ dBm}\\ \mathrm{SNR}&=-90+104.0=14.0\text{ dB}=25.1\end{aligned}\]
Exactly half of the earlier 50.2 ✓.''',
  r'''<b>(b) New capacity and explanation</b>:
\[\begin{aligned}\log_2(1+25.1)&=\frac{\log_{10}26.1}{0.301}=\frac{1.417}{0.301}=4.71\\C&=10\times10^6\times4.71=47.1\text{ Mbps}\end{aligned}\]
\(47.1/28.4=1.66\): the capacity <b>does not double</b>. The B outside the log doubles, but the SNR inside the log halves (the noise grows with the bandwidth), so the capacity per Hz drops from 5.68 to 4.71 bit/s/Hz. Capacity would double only if the SNR stayed the same (i.e. the transmit power were doubled as well).''',
  r'''<b>(c) First assume both subchannels get power</b>: water-filling (p.54): \(\dfrac{P_j}{P}=\dfrac1{\gamma_0}-\dfrac1{\gamma_j}\) (only for subchannels with \(\gamma_j\ge\gamma_0\)), with the power constraint \(\sum_j\big(\frac1{\gamma_0}-\frac1{\gamma_j}\big)=1\):
\[\begin{aligned}\frac2{\gamma_0}&=1+\frac1{20}+\frac1{0.5}=1+0.05+2=3.05\\ \frac1{\gamma_0}&=1.525,\qquad\gamma_0=0.656\end{aligned}\]
Check: \(\gamma_2=0.5\lt\gamma_0=0.656\), so subchannel 2 would get \(P_2/P=1.525-2=-0.475\). Power cannot be negative, so subchannel 2 gets no power; drop it and recompute.''',
  r'''<b>(c) Only subchannel 1 left</b>:
\[\begin{aligned}\frac1{\gamma_0}&=1+\frac1{20}=1.05,\qquad\gamma_0=0.952\\ \frac{P_1}{P}&=1.05-0.05=1\end{aligned}\]
\(\gamma_1=20\ge0.952\) ✓, so this cut-off is valid: <b>P₁ = P, P₂ = 0</b>, all the power goes to subchannel 1.''',
  r'''<b>(c) Total capacity</b>: \(C=\sum_{\gamma_j\ge\gamma_0}B_j\log_2(\gamma_j/\gamma_0)\) (p.54):
\[\begin{aligned}C&=1\text{ MHz}\times\log_2\frac{20}{0.952}=1\text{ MHz}\times\log_221\\&=1\text{ MHz}\times\frac{1.322}{0.301}=4.39\text{ Mbps}\end{aligned}\]
Check: with all the power on subchannel 1, Shannon's formula directly gives \(\log_2(1+20)=\log_221\), the same ✓.'''],
 ans='(a) SNR ≈ 17 dB (50.2), C ≈ 28.4 Mbps; (b) C ≈ 47.1 Mbps, about 1.66 times, not double; (c) subchannel 2 gets no power, P₁ = P, C ≈ 4.39 Mbps',
 official='none (self-written mock question); all numbers checked by src/p2build/verify_mock.py',
 note='''For comparison, splitting the power equally (P/2 each, SNRs 10 and 0.25) gives C = log₂11 + log₂1.25 = 3.78 Mbps, 0.61 Mbps less than water-filling. Power given to a very poor subchannel buys almost no capacity.''',
 kp=[
  ('What it tests', '''Shannon capacity (memorise), noise power N₀B, how capacity depends on bandwidth, water-filling (Ch 2 p.48, p.54–57).'''),
  ('Background', '''C = B log₂(1 + SNR) with linear SNR; N = N₀B, in dB N₀ + 10 log₁₀B; water-filling: Σ(1/γ₀ − 1/γ<sub>j</sub>) = 1, C = ΣB<sub>j</sub> log₂(γ<sub>j</sub>/γ₀).'''),
  ('Method', '''(a)(b) Noise → SNR (dB → linear) → Shannon; (c) assume all subchannels on → solve γ₀ → check every γ<sub>j</sub> ≥ γ₀ → if not, drop the worst one and recompute.'''),
  ('Key step', '''(c) The first γ₀ = 0.656 &gt; 0.5, so subchannel 2 is dropped; with one subchannel left, P₁ = P.'''),
  ('Common mistakes', '''Putting the SNR in dB into log₂; forgetting that doubling the bandwidth doubles the noise; not checking γ<sub>j</sub> ≥ γ₀ and using a negative power.'''),
  ('Intuition', '''With fixed power, doubling the bandwidth halves the SNR, so capacity grows by less than a factor of two. Water-filling gives up on very poor subchannels and concentrates the power on the good ones.'''),
  ('Link', '''Practice 5 Q1 (water-filling over three subchannels); Practice 2 Q3 (Shannon capacity and SINR); Practice 7 Q1 (d).''')])

# collapsible walk-through for mock A·Q3 (rendered by add_en.py after the note)
EN['p8q3']['detail'] = r'''      <details class="deep">
        <summary>Step by step: what each quantity is, how to compute it, what to memorise</summary>
        <div class="deep-body">
          <h4><span class="st">Memorise?</span>Formulas used here (from the lecturer's week 8–10 recordings)</h4>
          <div class="tw"><table class="mini"><thead><tr><th>Formula</th><th>Part</th><th>Memorise?</th></tr></thead><tbody>
            <tr><td>Mean delay μ, rms delay spread σ</td><td>(a)</td><td>Given in the exam; know how to weight by power</td></tr>
            <tr><td>\(\sigma_{T_m}/T_s\lt0.1\) → flat</td><td>(b)</td><td><b>Memorise</b> (blue box)</td></tr>
            <tr><td>\(f_m=vf_c/c\), \(T_C\approx1/f_m\)</td><td>(b)</td><td>Not named in the recordings; short and often needed first, so worth remembering</td></tr>
            <tr><td>AFD, LCR</td><td>(c)</td><td>Given (this question gives AFD); be able to say ρ = Z<sub>min</sub>/Z<sub>rms</sub> and that f<sub>m</sub> is the maximum Doppler shift</td></tr>
            <tr><td>Power ∝ amplitude²</td><td>(c)</td><td>Basic relation, must know</td></tr>
          </tbody></table></div>
          <p>Rayleigh fading itself: <b>memorise</b> the exponential SNR distribution \(p(\gamma)=\frac{1}{\bar\gamma}e^{-\gamma/\bar\gamma}\) and the Rayleigh outage \(1-e^{-\gamma_0/\bar\gamma}\) (the lecturer said it "often appears"); the Rayleigh envelope PDF need not be memorised; its derivation will not be asked; try to remember the fade-margin formula.</p>

          <h4><span class="st">(a)</span>What mean delay and rms delay spread are</h4>
          <p>A very short pulse arrives as several echoes: the strongest at 0 µs (0 dB), a weaker one at 1 µs (−3 dB), the weakest at 3 µs (−6 dB). That table is the power delay profile. The mean delay μ is the "centre of gravity" of the echo energy in time; the rms delay spread σ is how widely the energy is spread. σ is what matters: it decides whether echoes leak into the next symbol.</p>
          <p><b>Why divide by 1.752:</b> this is a power-weighted average, and a weighted average is divided by the sum of the weights, just like a credit-weighted grade average is divided by the total credits. The linear powers are 1, 0.501 and 0.251, which sum to 1.752.</p>
          <p>Equivalently, dividing by 1.752 turns powers into energy fractions: 1/1.752 = 0.571, 0.501/1.752 = 0.286, 0.251/1.752 = 0.143, which sum to 1 like a discrete probability distribution. Then μ = 0 × 0.571 + 1 × 0.286 + 3 × 0.143 = 0.716 µs and σ is the standard deviation of that distribution: the same mean and variance as for a discrete random variable in Ch 1b.</p>
          <ul>
            <li>The weights must be linear; the dB values (0, −3, −6) are negative and cannot be weights.</li>
            <li>σ is not "largest delay − smallest delay": the delays span 3 µs but σ is only 1.03 µs, because late echoes carry little power.</li>
          </ul>

          <h4><span class="st">(b)</span>Fading type: two separate dimensions</h4>
          <div class="tw"><table class="mini"><thead><tr><th>Dimension</th><th>Question</th><th>Compare</th><th>Here</th></tr></thead><tbody>
            <tr><td>Flat / frequency-selective</td><td>Do echoes leak into the next symbol?</td><td>σ with T<sub>s</sub>: σ/T<sub>s</sub> &lt; 0.1 → flat</td><td>1.03/20 = 0.052 → flat</td></tr>
            <tr><td>Slow / fast</td><td>Does the channel change within one symbol?</td><td>T<sub>C</sub> with T<sub>s</sub>: T<sub>s</sub> ≪ T<sub>C</sub> → slow</td><td>20 µs ≪ 8.33 ms → slow</td></tr>
          </tbody></table></div>
          <p>The two dimensions are independent: delay spread decides flat/selective, Doppler decides fast/slow. The symbol duration sits in between: \(\sigma_{T_m}\ll T_s\ll T_C\) means flat, slow fading. <b>Answering only one dimension gets half marks</b> (the lecturer said so). If σ/T<sub>s</sub> is only slightly above 0.1 (e.g. 0.15), no conclusion can be drawn; it must be well above 0.1 to call the fading frequency-selective.</p>

          <h4><span class="st">(b)</span>Maximum Doppler shift and coherence time</h4>
          <p><b>Maximum Doppler shift f<sub>m</sub>:</b> a moving receiver sees a slightly shifted frequency (like a siren rising in pitch as an ambulance approaches). The shift is \(f_d=\frac{v}{c}f_c\cos\theta\), largest when moving straight along the signal direction (cos θ = 1): \(f_m=vf_c/c\). Here v = 72 km/h ÷ 3.6 = 20 m/s and \(f_m=20\times1.8\times10^9/3\times10^8=120\) Hz.</p>
          <p><b>Coherence time T<sub>C</sub>:</b> how long the channel stays roughly constant. A larger Doppler makes the echo phases change faster, so the channel changes faster and T<sub>C</sub> is shorter: \(T_C\approx1/f_m=1/120=8.33\) ms. They are reciprocals: faster movement, larger f<sub>m</sub>, shorter T<sub>C</sub>; with no movement, f<sub>m</sub> = 0 and the channel does not change.</p>
          <ul>
            <li>Divide km/h by 3.6 to get m/s; convert GHz to Hz; put T<sub>C</sub> and T<sub>s</sub> in the same unit before comparing.</li>
          </ul>

          <h4><span class="st">(c)</span>Where ρ comes from: power ratio first, then square root</h4>
          <p>ρ = Z<sub>min</sub>/Z<sub>rms</sub> is an <b>amplitude</b> ratio, but the question gives a <b>power</b> condition ("not more than 10 dB below its rms value"). Power is amplitude squared (P = V²/R), so amplitude is the square root of power:</p>
          <div class="eqb">\[\frac{P_{\min}}{P_{\mathrm{rms}}}=10^{-10/10}=0.1=\Big(\frac{Z_{\min}}{Z_{\mathrm{rms}}}\Big)^2=\rho^2\ \Rightarrow\ \rho=\sqrt{0.1}=0.316\]</div>
          <div class="tw"><table class="mini"><thead><tr><th>Amplitude ratio ρ</th><th>Power ratio ρ²</th><th>Power down by</th></tr></thead><tbody>
            <tr><td>0.707</td><td>0.5</td><td>3 dB</td></tr><tr><td>0.316</td><td>0.1</td><td>10 dB</td></tr><tr><td>0.1</td><td>0.01</td><td>20 dB</td></tr>
          </tbody></table></div>
          <p>For power, divide the dB value by 10; for amplitude, by 20: \(\rho=10^{-10/20}=0.316\). The ρ² in the exponent of the AFD formula is exactly the power ratio 0.1. Compare Practice 2 Q1: "signal <b>strength</b> is 0.1 of the rms value" refers to amplitude, so there ρ = 0.1 directly. If the question talks about amplitude (strength, envelope), use the number as ρ; if it talks about power or gives dB, convert to a power ratio and take the square root. Taking ρ = 0.1 here would give AFD = 0.33 ms, more than 3 times too small.</p>

          <h4><span class="st">(c)</span>Why divide by 20 µs</h4>
          <p>20 µs is one symbol duration: 50 k symbols/s → \(T_s=1/50000=20\) µs. A deep fade lasts 1.11 ms = 1110 µs on average, which covers 1110 / 20 ≈ 55 symbols, so one fade affects about 55 consecutive symbols. Equivalently AFD × symbol rate = 1.11×10⁻³ × 50×10³ ≈ 55.</p>
          <p>Errors therefore come in bursts, not one at a time, which is why interleaving is used to spread consecutive bits apart before error-correcting codes fix them.</p>

          <h4><span class="st">Exam</span>Compact answer for (b) and (c)</h4>
          <div class="tmpl">
            <p>Flat or frequency-selective: \(\sigma_{T_m}/T_s=1.03/20=0.052\lt0.1\), so the fading is <b>flat</b>.</p>
            <p>Fast or slow: \(f_m=vf_c/c=120\) Hz, \(T_C\approx1/f_m=8.33\) ms ≫ \(T_s\) = 20 µs, so the channel is almost constant over a symbol and the fading is <b>slow</b>. Hence the signal experiences flat, slow fading.</p>
            <p>(c) A power 10 dB below the rms value means \(\rho^2=0.1\), \(\rho=\sqrt{0.1}=0.316\). AFD \(=(e^{0.1}-1)/(\sqrt{2\pi}\times120\times0.316)=1.11\) ms. Symbols per fade \(=\text{AFD}/T_s=1.11\text{ ms}/20\ \mu s\approx55\).</p>
          </div>
          <div class="ans">In one line: power-weighted μ and σ (divide by the total power) → σ vs T<sub>s</sub> for flat/selective, T<sub>C</sub> = 1/f<sub>m</sub> vs T<sub>s</sub> for fast/slow → square root of the power ratio gives ρ → AFD ÷ T<sub>s</sub> gives the symbols per fade.</div>
        </div>
      </details>'''

# walk-throughs added from the user's questions (rendered by add_en.py after the note)
EN['p2q3']['detail'] = r'''      <details class="deep">
        <summary>Step by step: SNR, SIR, SINR, and why the denominator in (a) is 10 + 0.1</summary>
        <div class="deep-body">
          <h4><span class="st">Three ratios</span>They differ only in the denominator</h4>
          <div class="tw"><table class="mini"><thead><tr><th>Measure</th><th>Denominator</th><th>When used</th></tr></thead><tbody>
            <tr><td>SNR = S/N</td><td>Noise only</td><td>Single user, no interference (AWGN channel)</td></tr>
            <tr><td>SIR = S/I</td><td>Interference only</td><td>Interference far above noise, noise negligible (Part A co-channel reuse)</td></tr>
            <tr><td>SINR = S/(I + N)</td><td>Interference + noise</td><td>The general case where neither can be ignored</td></tr>
          </tbody></table></div>
          <p>S is the wanted signal, I is the signal of other users or cells (interference), N is the receiver's thermal noise. SINR is the most complete: with I = 0 it becomes SNR, with N = 0 it becomes SIR, so SINR is smaller than both.</p>

          <h4><span class="st">(a)</span>Why the denominator is 10 + 0.1, not 0.1</h4>
          <p>Both users transmit at the same time on the same frequency, so the antenna receives the sum of user 1 (10 mW), user 2 (10 mW) and noise (0.1 mW). The receiver cannot "listen only to user 1".</p>
          <div class="tw"><table class="mini"><thead><tr><th>Component</th><th>Power</th><th>For decoding user 1</th></tr></thead><tbody>
            <tr><td>User 1's signal</td><td>10 mW</td><td>Wanted: numerator S</td></tr>
            <tr><td>User 2's signal</td><td>10 mW</td><td>Unwanted: interference I</td></tr>
            <tr><td>Thermal noise</td><td>0.1 mW</td><td>Unwanted: noise N</td></tr>
          </tbody></table></div>
          <p>User 2's signal is useful to user 2, but for decoding user 1 it blurs the signal just like noise, and it is 100 times stronger than the noise. Everything unwanted goes in the denominator: SINR₁ = 10/(10 + 0.1) = 0.99. Writing only 0.1 (giving 100) pretends user 2 is silent and badly overestimates the capacity.</p>
          <p>Analogy: listening to friend A in a noisy room, the air conditioner is the noise (small) and friend B talking loudly at the same time is the interference. B's voice, not the air conditioner, is the main obstacle.</p>

          <h4><span class="st">(b)</span>When the denominator is 0.1</h4>
          <p>MUD first decodes user 1 and subtracts it, leaving "user 2 + noise". When user 2 is decoded only noise remains, so SNR₂ = 10/0.1 = 100. Compare: (a) user 2 is still present when decoding user 1 → 10 + 0.1; (b) user 1 has been removed when decoding user 2 → 0.1.</p>

          <h4><span class="st">Shannon</span>Why the formula says SNR but SINR is used here</h4>
          <p>Shannon's result is for the single-user AWGN channel y = x + w: one transmitter and Gaussian noise only, so I = 0 and SINR equals SNR. What the formula really needs is that everything in the denominator together is Gaussian noise. The question says user 2's signal behaves like noise (<b>assume it is AWGN</b>), so in \(y=x_1+(x_2+w)\) the term \(x_2+w\) is one larger Gaussian noise of 10 + 0.1 mW, and the formula still applies with N replaced by I + N.</p>
          <div class="tw"><table class="mini"><thead><tr><th>Case</th><th>Denominator</th><th>Formula</th></tr></thead><tbody>
            <tr><td>Single user (Shannon's model)</td><td>N</td><td>B log₂(1 + SNR)</td></tr>
            <tr><td>Interference treated as Gaussian noise</td><td>I + N</td><td>B log₂(1 + SINR)</td></tr>
          </tbody></table></div>
          <p>Inside the bracket it is always "wanted power / all power treated as noise". Treating interference as Gaussian noise gives a conservative capacity; MUD does better because it uses the fact that the interference is another user's data, decodes it and subtracts it.</p>

          <h4><span class="st">Exam</span>Compact answer</h4>
          <div class="tmpl">
            <p>(a) When user 1 is decoded, user 2's signal is treated as AWGN, so it adds to the noise: SINR₁ = P₁/(P₂ + N) = 10/(10 + 0.1) = 0.990, C₁ = B log₂(1 + SINR₁) = 19.86 Mbps.</p>
            <p>(b) After MUD removes user 1, only noise remains for user 2: SNR₂ = P₂/N = 10/0.1 = 100, C₂ = B log₂(1 + SNR₂) = 133.16 Mbps.</p>
          </div>
          <div class="ans">In one line: the denominator is the sum of all unwanted power. User 2 is still present when user 1 is decoded, so 10 + 0.1; after user 1 is subtracted, user 2 sees only the 0.1 mW noise.</div>
        </div>
      </details>'''

EN['p8q2']['detail'] = r'''      <details class="deep">
        <summary>Step by step: dB versus dBm, and the unit of every quantity</summary>
        <div class="deep-body">
          <h4><span class="st">Difference</span>dBm is "how much", dB is "how many times"</h4>
          <div class="tw"><table class="mini"><thead><tr><th></th><th>dB</th><th>dBm</th></tr></thead><tbody>
            <tr><td>Meaning</td><td>Ratio of two powers, no unit</td><td>Absolute power, referenced to 1 mW</td></tr>
            <tr><td>Definition</td><td>10 log₁₀(P₁/P₂)</td><td>10 log₁₀(P / 1 mW)</td></tr>
            <tr><td>Examples</td><td>×100 = +20 dB; down to 1/1000 = −30 dB</td><td>100 mW = 20 dBm; 1 mW = 0 dBm</td></tr>
          </tbody></table></div>

          <h4><span class="st">K</span>Why K is in dB, not dBm</h4>
          <p>In the linear form \(P_r=P_t\cdot K\cdot(d_0/d)^{\gamma}\), \(P_r\) and \(P_t\) are powers (mW) while K and \((d_0/d)^{\gamma}\) are unitless factors multiplying the power. K means "how many times the transmit power is received at the reference distance d₀", a ratio, so in log form it is in dB. \(K_{dB}=-31.5\) dB means the signal at 1 m is \(10^{-3.15}\approx1/1400\) of the transmit power.</p>
          <p>Taking dB turns products into sums; only \(P_t\) is in dBm and everything else is in dB, so the result is in dBm:</p>
          <div class="eqb">\[\underbrace{P_{r,dBm}}_{\text{dBm}}=\underbrace{P_{t,dBm}}_{\text{dBm}}+\underbrace{K_{dB}}_{\text{dB}}-\underbrace{10\gamma\log_{10}(d/d_0)}_{\text{dB}}\]</div>
          <div class="tw"><table class="mini"><thead><tr><th>Operation</th><th>Result</th><th>Meaning</th></tr></thead><tbody>
            <tr><td>dBm + dB</td><td>dBm</td><td>A power times a factor is still a power</td></tr>
            <tr><td>dBm − dBm</td><td>dB</td><td>A ratio of two powers (margin, SNR)</td></tr>
            <tr><td>dB + dB</td><td>dB</td><td>A factor times a factor is still a factor</td></tr>
            <tr><td>dBm + dBm</td><td>Meaningless</td><td>Power times power is not a power</td></tr>
          </tbody></table></div>
          <p>Check: if K were in dBm, the right-hand side would be dBm + dBm, i.e. "power × power", which has no physical meaning.</p>

          <h4><span class="st">Here</span>Unit of each quantity</h4>
          <div class="tw"><table class="mini"><thead><tr><th>Quantity</th><th>Value</th><th>Unit</th></tr></thead><tbody>
            <tr><td>Transmit power</td><td>100 mW = 20</td><td>dBm (absolute power)</td></tr>
            <tr><td>K</td><td>−31.5</td><td>dB (ratio)</td></tr>
            <tr><td>Path loss term 36 log₁₀300</td><td>89.18</td><td>dB (ratio)</td></tr>
            <tr><td>Average received power</td><td>−100.68</td><td>dBm</td></tr>
            <tr><td>Threshold</td><td>−110</td><td>dBm</td></tr>
            <tr><td>Margin = received power − threshold</td><td>9.32</td><td>dB (dBm − dBm)</td></tr>
            <tr><td>Shadowing standard deviation σ</td><td>6</td><td>dB (a fluctuation about the mean, also a ratio)</td></tr>
          </tbody></table></div>
          <p>Practice 1 Q2 writes σ in "dBm"; strictly it should be dB.</p>
          <div class="ans">In one line: dBm is an absolute power, dB is a ratio. In the path loss model only the transmit and received powers are in dBm; K, path loss, shadowing and margin are all in dB.</div>
        </div>
      </details>'''

EN['p8q4']['detail'] = r'''      <details class="deep">
        <summary>Step by step: where the Rayleigh outage 1 − e<sup>−γ₀/γ̄</sup> comes from (not examined, for understanding)</summary>
        <div class="deep-body">
          <p>The lecturer said the Rayleigh derivation will not be asked and the Quiz has no integration; in the exam, remember the result and use it. This only shows where it comes from.</p>
          <h4><span class="st">Idea</span>Multipath → Rayleigh → exponential → integrate</h4>
          <p>Multipath sum → Gaussian I and Q components → Rayleigh envelope z → exponential power z² (and SNR γ) → integrating the exponential from 0 to γ₀ gives the outage probability.</p>
          <h4><span class="st">Step 1</span>Why the envelope is Rayleigh</h4>
          <p>The phone receives many echoes with random phases: \(r_I=\sum\alpha_n\cos\phi_n\), \(r_Q=\sum\alpha_n\sin\phi_n\). Each is a sum of many random terms, so by the central limit theorem they are approximately independent zero-mean Gaussians with variance σ². The envelope is the length of this 2-D vector, \(z=\sqrt{r_I^2+r_Q^2}\), and the length of two independent zero-mean Gaussians is Rayleigh: \(p(z)=\frac{z}{\sigma^2}e^{-z^2/(2\sigma^2)},\ z\ge0\).</p>
          <h4><span class="st">Step 2</span>From envelope to SNR</h4>
          <p>Power is amplitude squared: received power z², mean power E[z²] = 2σ². SNR is proportional to power: \(\gamma=z^2/N\), mean \(\bar\gamma=2\sigma^2/N\).</p>
          <h4><span class="st">Step 3</span>Integrate for the outage</h4>
          <p>"γ &lt; γ₀" is the same as "z &lt; z₀" with \(z_0^2=\gamma_0N\). Substitute \(u=z^2/(2\sigma^2)\), \(du=z\,dz/\sigma^2\):</p>
          <div class="eqb">\[P_{out}=\int_0^{z_0}\frac{z}{\sigma^2}e^{-z^2/(2\sigma^2)}dz=\int_0^{z_0^2/(2\sigma^2)}e^{-u}du=1-e^{-z_0^2/(2\sigma^2)}=1-e^{-\gamma_0/\bar\gamma}\]</div>
          <p>The last step uses \(z_0^2/(2\sigma^2)=\gamma_0N/(\bar\gamma N)=\gamma_0/\bar\gamma\).</p>
          <h4><span class="st">Other way</span>The two formulas to memorise are a pair</h4>
          <p>Differentiating \(1-e^{-\gamma_0/\bar\gamma}\) with respect to γ₀ gives the exponential SNR distribution \(p(\gamma)=\frac{1}{\bar\gamma}e^{-\gamma/\bar\gamma}\); conversely \(\int_0^{\gamma_0}\frac{1}{\bar\gamma}e^{-\gamma/\bar\gamma}d\gamma=1-e^{-\gamma_0/\bar\gamma}\). The exponential distribution is the PDF and the outage probability is its CDF: remember one and you get the other.</p>
          <h4><span class="st">Check</span>Does it make sense?</h4>
          <div class="tw"><table class="mini"><thead><tr><th>Case</th><th>Substitute</th><th>Result</th><th>Meaning</th></tr></thead><tbody>
            <tr><td>γ₀ = 0</td><td>1 − e⁰</td><td>0</td><td>No SNR required, never in outage</td></tr>
            <tr><td>γ₀ → ∞</td><td>1 − e<sup>−∞</sup></td><td>1</td><td>Never reachable, always in outage</td></tr>
            <tr><td>γ₀ = γ̄</td><td>1 − e⁻¹</td><td>0.632</td><td>Below the mean 63% of the time (the other side of part (c))</td></tr>
            <tr><td>γ₀ ≪ γ̄</td><td>e<sup>−x</sup> ≈ 1 − x</td><td>≈ γ₀/γ̄</td><td>1% outage needs γ̄ ≈ 100γ₀, a margin of about 20 dB (part (b))</td></tr>
          </tbody></table></div>
          <h4><span class="st">Use</span>When substituting</h4>
          <ul>
            <li>Convert γ₀ and γ̄ to linear values first (7 dB → 5.01, 20 dB → 100); only their ratio matters, so any consistent unit works.</li>
            <li>Average SNR backwards: \(\bar\gamma=\gamma_0/\ln\frac{1}{1-P_{out}}\).</li>
          </ul>
          <div class="ans">In one line: the multipath sum makes the envelope Rayleigh → the power (SNR) exponential → integrating the exponential from 0 to γ₀ gives P<sub>out</sub> = 1 − e<sup>−γ₀/γ̄</sup>.</div>
        </div>
      </details>'''

EN['p8q5']['detail'] = r'''      <details class="deep">
        <summary>Step by step: where the line comes from, how least squares works, why (c) uses Q and not the exponential formula</summary>
        <div class="deep-body">
          <h4><span class="st">Line</span>Where M = K<sub>dB</sub> − γx comes from</h4>
          <p>Take \(10\log_{10}\) of \(P_r/P_t=K(d_0/d)^{\gamma}\): products become sums, the exponent becomes a factor, and \(d_0/d\) is the reciprocal of \(d/d_0\), giving a minus sign: \(M=K_{dB}-\gamma\cdot10\log_{10}(d/d_0)\). With \(d_0=1\) m and \(x=10\log_{10}d\) this is \(M=K_{dB}-\gamma x\): a line with intercept \(K_{dB}\) and slope −γ. Using 10 log₁₀d on the x axis makes the slope exactly −γ; with log₁₀d it would be −10γ.</p>
          <h4><span class="st">Least squares</span>Two partial derivatives equal to 0</h4>
          <p>Residual \(e_i=M_i-(K-\gamma x_i)\); minimise \(F=\sum e_i^2\) (squares: signs cannot cancel, it is differentiable, and the minimum is the shadowing variance). At the bottom of this bowl both slopes are 0:</p>
          <ol>
            <li>\(\partial F/\partial K=0\ \Rightarrow\ \sum(M_i-K+\gamma x_i)=0\ \Rightarrow\ K=\bar M+\gamma\bar x\): the line passes through the mean point and the residuals sum to 0.</li>
            <li>\(\partial F/\partial\gamma=0\ \Rightarrow\ \sum x_i(M_i-K+\gamma x_i)=0\); substituting K and replacing \(x_i\) by \(x_i-\bar x\): \(\gamma=-\dfrac{\sum(x_i-\bar x)(M_i-\bar M)}{\sum(x_i-\bar x)^2}\).</li>
          </ol>
          <p>Here: x̄ = 15, M̄ = −87.5, Σ(x − x̄)(M − M̄) = −194.95, Σ(x − x̄)² = 57.92, slope −3.37 → γ = 3.37, K<sub>dB</sub> = −37.0 dB. Check: at d = 100 m, M = −37.0 − 3.37 × 20 = −104.3 dB against a measured −105 dB; the −0.7 dB difference is that point's residual (shadowing).</p>
          <h4><span class="st">(c)</span>Why Q and not 1 − e<sup>−γ₀/γ̄</sup></h4>
          <div class="tw"><table class="mini"><thead><tr><th></th><th>Shadowing</th><th>Rayleigh fading</th></tr></thead><tbody>
            <tr><td>Cause</td><td>Buildings, hills block the path (large scale)</td><td>Multipath phases cancel (small scale)</td></tr>
            <tr><td>Distribution</td><td>dB value is Gaussian (log-normal)</td><td>Linear SNR is exponential</td></tr>
            <tr><td>Outage</td><td>Q(margin/σ), subtract in dB</td><td>1 − e<sup>−γ₀/γ̄</sup>, divide in linear</td></tr>
            <tr><td>Parameters</td><td>Margin (dB) and σ (dB)</td><td>Threshold SNR and average SNR, no σ</td></tr>
          </tbody></table></div>
          <p>Clues here: "path loss alone … 8 dB above" means the mean is set by path loss and shadowing fluctuates around it, and (b) has just found the shadowing σ = 3.35 dB from the fit. So it is shadowing and Q applies: P<sub>out</sub> = Q(8/3.35) = Q(2.39) ≈ 0.84%.</p>
          <p>For comparison, with "Rayleigh fading, average SNR 8 dB above the threshold": \(\gamma_0/\bar\gamma=10^{-0.8}=0.158\), \(P_{out}=1-e^{-0.158}\approx14.7\%\). The same 8 dB margin gives a much larger outage, because Rayleigh fades are much deeper.</p>
          <div class="ans">In one line: in dB the model is a line with intercept K<sub>dB</sub> and slope −γ; least squares = both partial derivatives 0 → the line passes through the mean point and slope = covariance/variance; shadowing with σ uses Q, Rayleigh with an average SNR uses the exponential formula.</div>
        </div>
      </details>'''

EN['p8q6']['detail'] = r'''      <details class="deep">
        <summary>Step by step: what water-filling is and why it allocates power this way</summary>
        <div class="deep-body">
          <h4><span class="st">Question</span>What water-filling answers</h4>
          <p>Given several parallel subchannels of different quality and a fixed total power, how should the power be split to maximise the total capacity? The transmitter must know the channel (informed transmitter).</p>
          <h4><span class="st">Analogy</span>Pouring water into an uneven pool</h4>
          <p>Each subchannel is one cell of a pool whose <b>floor height is 1/γ<sub>j</sub></b> (γ<sub>j</sub> is its SNR with all the power): the better the channel, the lower the floor. Pour the total power in like water; it settles to a flat surface at 1/γ₀. Each cell gets power = surface − floor: good channels get more, poor ones less, and a cell whose floor is above the surface gets none.</p>
          <div class="eqb">\[\frac{P_j}{P}=\frac{1}{\gamma_0}-\frac{1}{\gamma_j}\ (\gamma_j\ge\gamma_0),\qquad \sum_j\Big(\frac{1}{\gamma_0}-\frac{1}{\gamma_j}\Big)=1,\qquad C=\sum_{\gamma_j\ge\gamma_0}B_j\log_2\frac{\gamma_j}{\gamma_0}\]</div>
          <h4><span class="st">Steps</span>Assume all on, check, drop and redo if needed</h4>
          <ol>
            <li>Assume all n subchannels get power: \(n/\gamma_0=1+\sum1/\gamma_j\); solve for γ₀.</li>
            <li>Check every \(\gamma_j\ge\gamma_0\); if one fails, drop the worst (n − 1) and solve again.</li>
            <li>Compute the powers and the capacity.</li>
          </ol>
          <h4><span class="st">Here</span>Subchannel 2 is dropped</h4>
          <p>Assume both on: 2/γ₀ = 1 + 1/20 + 1/0.5 = 3.05, γ₀ = 0.656; subchannel 2 has SNR 0.5 &lt; 0.656 (its floor 1/0.5 = 2 is above the surface 1/0.656 = 1.52), so drop it. One left: 1/γ₀ = 1.05, P₁/P = 1.05 − 0.05 = 1, C = log₂(20/0.952) = log₂21 = 4.39 Mbps. An equal split gives only log₂11 + log₂1.25 = 3.78 Mbps.</p>
          <p>Compare Practice 5 Q1 (SNRs 80, 40, 40): γ₀ = 2.82, all three are above it and all get power (0.342, 0.329, 0.329), C ≈ 124.7 Mbps.</p>
          <h4><span class="st">Why</span>This split is optimal</h4>
          <p>Capacity is log₂(1 + SNR), which grows more and more slowly. Extra power on a poor channel barely raises its SNR; a good channel returns more per unit of power, but with diminishing returns too. At the optimum the surface is flat: the last bit of power earns the same on every channel used (the slides say γ₀ comes from a Lagrange multiplier; the formal derivation is not examined).</p>
          <ul>
            <li>Common mistakes: use linear γ<sub>j</sub>; always check γ<sub>j</sub> ≥ γ₀ or you get a negative power; capacity uses log₂(γ<sub>j</sub>/γ₀), not log₂(1 + γ<sub>j</sub>); update n after dropping a subchannel.</li>
          </ul>
          <div class="ans">In one line: treat 1/γ<sub>j</sub> as the pool floor and pour in the total power to a flat surface 1/γ₀; good channels get more, poor ones less, very poor ones none. Assume all on → solve γ₀ → check γ<sub>j</sub> ≥ γ₀ → drop and redo if needed.</div>
        </div>
      </details>'''

# ---------------------------------------------------------------- mock Quiz set C
EN['p8q7'] = dict(
 idea=r'''Shadowing → a single base station's outage is Q(margin/σ); the two links are independent and outage needs both below the threshold → multiply; (c) works backwards from the probability in (b) with the Q table.''',
 steps=[
  r'''<b>(a) Margin</b>: margin = average power due to path loss alone − threshold:
\[x=-95-(-105)=10\text{ dB}\]
Shadowing in dB is \(\mathcal N(0,\sigma^2)\), so the outage probability of one base station is \(Q(x/\sigma)\) (Ch 2 p.15).''',
  r'''<b>(a) Q table</b>:
\[P_{out,1}=Q\Big(\frac{10}{8}\Big)=Q(1.25)=0.1056\approx0.106\]
About 10.6%, far above the usual 1% target.''',
  r'''<b>(b) Independent → multiply</b>: with macro-diversity, outage happens only when <b>both</b> links are below the threshold, an "AND" event. The shadowing of the two links is independent, so use the multiplication rule \(P(A\cap B)=P(A)P(B)\) (Ch 1b p.6):
\[\begin{aligned}P_{out,2}&=Q(1.25)\times Q(1.25)=0.1056^2\\&=0.01116\approx1.12\times10^{-2}\end{aligned}\]
About 1.1%, nearly 10 times smaller than with one base station.''',
  r'''<b>(c) Inverse Q lookup</b>: for one base station to reach the same outage we need \(Q(x'/\sigma)=0.01116\). From the Q table, Q(2.28) = 0.01130 and Q(2.29) = 0.01101; interpolate linearly:
\[\begin{aligned}\frac{x'}{\sigma}&\approx2.28+0.01\times\frac{0.01130-0.01116}{0.01130-0.01101}\\&=2.28+0.01\times0.48=2.285\end{aligned}\]''',
  r'''<b>(c) Required margin</b>:
\[x'=2.285\times8=18.28\approx18.3\text{ dB}\]
Check: \(Q(18.3/8)=Q(2.29)=0.0110\approx0.011\) ✓, matching the 1.1% of (b).''',
  r'''<b>(c) Macro-diversity gain</b>: each base station actually has only 10 dB of margin, yet the pair performs like a single base station with 18.3 dB:
\[G=18.3-10=8.3\text{ dB}\]
In other words, a single base station would need about \(10^{8.28/10}\approx6.7\) times the transmit power to do as well.'''],
 ans='(a) ≈ 0.106 (10.6%); (b) ≈ 1.12 × 10⁻² (1.1%); (c) a single base station would need about 18.3 dB of margin; macro-diversity gain ≈ 8.3 dB',
 official='none (self-written mock question); all numbers checked by src/p2build/verify_mock.py',
 note='''Outage drops from 10.6% to 1.1%, as if more than 8 dB of margin were gained without extra transmit power. This assumes independent shadowing; with common shadowing (P2 Q2 (c)) the gain is smaller.''',
 kp=[
  ('What it tests', '''Shadowing outage P<sub>out</sub> = Q(margin/σ) (memorise), multiplying independent events, inverse Q lookup; why macro-diversity helps (Ch 2 p.12–16; Ch 4 p.3–4).'''),
  ('Background', '''Margin = average power − threshold (dBm − dBm = dB); independent: P(A and B) = P(A)P(B); forward and inverse Q table lookup.'''),
  ('Method', '''(a) margin ÷ σ → Q; (b) square it; (c) inverse Q of the probability in (b) → required margin = xσ → subtract the actual margin to get the macro-diversity gain.'''),
  ('Key step', '''Q(1.25) = 0.1056 → squared 0.0112 → inverse x ≈ 2.29 → 18.3 dB, about 8.3 dB more than the actual 10 dB.'''),
  ('Common mistakes', '''Outage needs both links below the threshold, not either; Q takes margin over the standard deviation σ, not the variance; the inverse lookup uses the probability from (b), not (a).'''),
  ('Intuition', '''Macro-diversity works because "if one fails, the other is still there": both links blocked at once has probability equal to the product. With correlated shadowing the product no longer holds and the gain shrinks (P2 Q2 (c)).'''),
  ('Link', '''A numerical version of P2 Q2 (b); P4 Q1 explains the same idea in words; mock A·Q2 is single-base-station shadowing outage.''')])

EN['p8q8'] = dict(
 idea=r'''(a) The frequency dimension compares signal bandwidth with coherence bandwidth, the time dimension compares Doppler spread with signal bandwidth; answer both. (b) LCR is "deep fades per second"; times the duration of each gives the fraction of time in deep fades. (c) Multiply the two given formulas: f<sub>m</sub> cancels and only ρ remains.''',
 steps=[
  r'''<b>(a) Frequency dimension: flat or selective</b>: compare the signal bandwidth B<sub>s</sub> with the coherence bandwidth B<sub>C</sub> (Ch 2 p.31–33). B<sub>s</sub> &lt; B<sub>C</sub> → <b>flat fading</b>: frequency components closer than B<sub>C</sub> fade in a correlated way, so the whole signal rises and falls together and the spectrum is hardly distorted. B<sub>s</sub> &gt; B<sub>C</sub> → <b>frequency-selective fading</b>: different frequencies fade differently; in the time domain the rms delay spread is a significant fraction of the symbol duration, which causes inter-symbol interference (ISI).''',
  r'''<b>(a) Time dimension: fast or slow</b>: compare the Doppler spread \(B_D=f_m\) (p.35) with B<sub>s</sub>, or equivalently the coherence time \(T_C\approx1/B_D\) (p.36) with the symbol duration T<sub>s</sub>. B<sub>D</sub> ≪ B<sub>s</sub> (T<sub>C</sub> ≫ T<sub>s</sub>) → <b>slow fading</b>: the channel amplitude and phase stay almost constant during a symbol. B<sub>D</sub> close to or above B<sub>s</sub> (T<sub>C</sub> shorter than T<sub>s</sub>) → <b>fast fading</b>: the channel changes before a symbol is finished (p.37).''',
  r'''<b>(a) This system</b>:
\[\begin{aligned}\frac{B_s}{B_C}&=\frac{50\text{ kHz}}{200\text{ kHz}}=0.25\lt1\ \Rightarrow\ \text{flat}\\ \frac{B_D}{B_s}&=\frac{100\text{ Hz}}{50\text{ kHz}}=0.002\ll1\ \Rightarrow\ \text{slow}\end{aligned}\]
Time-domain check: \(T_s=1/R_s=20\ \mu\)s and \(T_C\approx1/f_m=1/100=10\) ms, 500 times T<sub>s</sub> ✓. Conclusion: <b>flat, slow fading</b>.''',
  r'''<b>(b) LCR</b>: the level crossing rate is the average number of downward crossings of the threshold per second (p.40):
\[L_Z=\frac{300}{10\text{ s}}=30\text{ s}^{-1}\]''',
  r'''<b>(b) Fraction of time in deep fades</b>: p.42: in T seconds there are \(L_ZT\) fades, each lasting \(\bar\tau\) on average, so the total fade time is \(\sum\tau_i=L_ZT\bar\tau\). Divide by T:
\[\begin{aligned}\frac{\sum\tau_i}{T}&=L_Z\bar\tau=30\times0.5\times10^{-3}\\&=0.015=1.5\%\end{aligned}\]
Check: in 10 s a total of 300 × 0.5 ms = 0.15 s is spent in deep fades, and 0.15 / 10 = 1.5% ✓.''',
  r'''<b>(b) Symbol errors per second</b>: \(T_s=1/(50\times10^3)=20\ \mu\)s. Each deep fade wipes out \(\bar\tau/T_s=\bar\tau R_s\) consecutive symbols (p.46), and there are L<sub>Z</sub> deep fades per second:
\[\begin{aligned}\frac{\bar\tau}{T_s}&=\frac{0.5\text{ ms}}{20\ \mu\text{s}}=25\\ N_{err}&=L_Z\times25=30\times25=750\text{ s}^{-1}\end{aligned}\]
Check: 50 000 symbols are sent per second and 1.5% of them fall in deep fades: 0.015 × 50 000 = 750 ✓.''',
  r'''<b>(c) Multiply the two formulas to cancel f<sub>m</sub></b>: f<sub>m</sub> and \(\sqrt{2\pi}\rho\) appear once in the numerator and once in the denominator:
\[\begin{aligned}L_Z\bar\tau_Z&=\sqrt{2\pi}f_m\rho e^{-\rho^2}\cdot\frac{e^{\rho^2}-1}{\sqrt{2\pi}f_m\rho}\\&=e^{-\rho^2}(e^{\rho^2}-1)=1-e^{-\rho^2}\end{aligned}\]
This is the Rayleigh probability of being below the threshold, \(P(z\lt Z_{min})\) (p.43). Set it equal to the 0.015 of (b):
\[\rho^2=\ln\frac1{1-0.015}=\ln\frac1{0.985}=0.0151\]''',
  r'''<b>(c) Convert to dB</b>: \(\rho=Z_{min}/Z_{rms}\) is an amplitude ratio; ρ² is the power ratio:
\[\begin{aligned}10\log_{10}\rho^2&=10\log_{10}0.0151=-18.2\text{ dB}\\ \rho&=\sqrt{0.0151}=0.123\end{aligned}\]
The threshold is about <b>18.2 dB</b> below the rms power. Back-substitution: \(1-e^{-0.0151}=0.0150\) ✓.'''],
 ans='(a) flat (B<sub>s</sub> &lt; B<sub>C</sub>), slow (B<sub>D</sub> ≪ B<sub>s</sub>) fading; (b) LCR = 30 per second, 1.5% of the time in deep fades, about 750 symbol errors per second; (c) the threshold is about 18.2 dB below the rms power',
 official='none (self-written mock question); all numbers checked by src/p2build/verify_mock.py',
 note='''Check: putting ρ = 0.123 back into the LCR formula gives f<sub>m</sub> = 30 / (√(2π) × 0.123 × e<sup>−0.0151</sup>) ≈ 99 Hz, matching the 100 Hz given. Errors come in bursts (25 in a row), which is why interleaving is used to spread them out.''',
 kp=[
  ('What it tests', '''Fading type from B<sub>C</sub>, B<sub>D</sub> and B<sub>s</sub> (two dimensions); meaning and use of LCR and AFD; for Rayleigh, LCR × AFD = 1 − e<sup>−ρ²</sup> (Ch 2 p.31–43). 2025-26 S2 Q1(a)(i)(ii) is this type of question.'''),
  ('Background', '''B<sub>s</sub> &lt; B<sub>C</sub> → flat; B<sub>D</sub> ≪ B<sub>s</sub> (T<sub>C</sub> ≫ T<sub>s</sub>) → slow; LCR = downward crossings of the threshold per second; AFD = average time below the threshold per crossing; ρ is an amplitude ratio, ρ² a power ratio.'''),
  ('Method', '''(a) Compare and conclude in each dimension separately; (b) LCR = count / observation time → fraction = LCR × AFD → symbols per fade = AFD / T<sub>s</sub> → errors per second = LCR × symbols per fade; (c) multiply the two formulas to cancel f<sub>m</sub> and solve for ρ².'''),
  ('Key formulas', '''L<sub>Z</sub> τ̄<sub>Z</sub> = 1 − e<sup>−ρ²</sup>; the threshold is 10 log₁₀(1/ρ²) dB below the rms power.'''),
  ('Common mistakes', '''Answering only one dimension of the fading type gets half marks (the lecturer said so); LCR is per second, so divide by the observation time; ρ² is the power ratio, so in dB use 10 log₁₀(ρ²) (= 20 log₁₀ρ).'''),
  ('Check', '''Putting ρ back into the LCR formula gives f<sub>m</sub> ≈ 99 Hz, matching the 100 Hz given.'''),
  ('Link', '''Practice 2 Q1 (AFD); mock A·Q3 (delay profile + Doppler + AFD); learning page sections 2.4–2.6.''')])

EN['p8q9'] = dict(
 idea=r'''The three ratios differ only in the denominator; with interference treated as Gaussian noise, Shannon's formula uses the SINR; in (c) the formula is given, and \(\bar\gamma\ln\frac{1}{1-\varepsilon}\) is just the minimum SNR obtained by inverting the Rayleigh outage formula.''',
 steps=[
  r'''<b>(a) The three ratios (linear)</b>: all have the signal power on top and differ only in the denominator:
\[\begin{aligned}\mathrm{SNR}&=\frac SN=\frac{2}{0.05}=40\\ \mathrm{SIR}&=\frac SI=\frac{2}{0.5}=4\\ \mathrm{SINR}&=\frac{S}{I+N}=\frac{2}{0.5+0.05}=\frac{2}{0.55}=3.64\end{aligned}\]
All are mW / mW, so they have no unit.''',
  r'''<b>(a) Convert to dB</b>: \(10\log_{10}40=16.0\) dB, \(10\log_{10}4=6.0\) dB, \(10\log_{10}3.64=5.6\) dB. Check: the SINR has the largest denominator, so it is the smallest: 5.6 dB &lt; 6.0 dB &lt; 16.0 dB ✓.''',
  r'''<b>(a) Capacity</b>: with the interference treated as Gaussian noise, the total "noise" is I + N, so Shannon's formula (Ch 2 p.48) uses the SINR:
\[\begin{aligned}\log_2(1+3.64)&=\frac{\log_{10}4.64}{0.301}=\frac{0.666}{0.301}=2.213\\C&=10\times10^6\times2.213=22.1\text{ Mbps}\end{aligned}\]''',
  r'''<b>(b) Interference removed</b>: only the noise remains, so use SNR = 40:
\[\begin{aligned}\log_2(1+40)&=\frac{\log_{10}41}{0.301}=\frac{1.613}{0.301}=5.358\\C&=10\times10^6\times5.358=53.6\text{ Mbps}\end{aligned}\]
That is 53.6 / 22.1 = 2.42 times the value in (a).''',
  r'''<b>(c) Minimum SNR</b>: \(\bar\gamma=10^{20/10}=100\). The term \(\bar\gamma\ln\frac1{1-\varepsilon}\) in the given formula is γ<sub>min</sub> obtained by inverting the Rayleigh CDF \(1-e^{-\gamma_{min}/\bar\gamma}=\varepsilon\) (p.50–51):
\[\begin{aligned}\ln\frac1{1-0.01}&=\ln\frac1{0.99}=0.01005\\ \gamma_{min}&=100\times0.01005=1.005\end{aligned}\]
i.e. \(10\log_{10}1.005=0.02\) dB, about 0 dB.''',
  r'''<b>(c) Outage capacity</b>:
\[\begin{aligned}C_\varepsilon&=10\times10^6\times\log_2(1+1.005)\\&=10\times10^6\times\frac{\log_{10}2.005}{0.301}\\&=10\times10^6\times\frac{0.3021}{0.301}=10\times10^6\times1.004\\&=10.0\text{ Mbps}\end{aligned}\]''',
  r'''<b>(c) Comparison with AWGN</b>: an AWGN channel with the same 20 dB always has SNR 100:
\[\begin{aligned}C_{AWGN}&=10\times10^6\times\frac{\log_{10}101}{0.301}\\&=10\times10^6\times6.658=66.6\text{ Mbps}\end{aligned}\]
\(66.6/10.0=6.6\) times more. Reason: to stay out of outage 99% of the time, the Rayleigh link must set its rate by the minimum SNR (about 0 dB). Check: \(\bar\gamma_{dB}-\gamma_{min,dB}=20-0.02=19.98\) dB, exactly the 20 dB fade margin for ε = 1% on p.51 ✓ (same as Mock B Q1 (b)).'''],
 ans='(a) SNR 16.0 dB, SIR 6.0 dB, SINR 5.6 dB, C ≈ 22.1 Mbps; (b) C ≈ 53.6 Mbps; (c) C<sub>ε</sub> ≈ 10.0 Mbps, far below the 66.6 Mbps of the AWGN channel',
 official='none (self-written mock question); all numbers checked by src/p2build/verify_mock.py',
 note='''The interference (0.5 mW) is 10 times the noise (0.05 mW), so SINR ≈ SIR: the system is interference-limited, and lowering the noise further barely helps; the interference must be reduced. The SINR is always smaller than both the SNR and the SIR.''',
 kp=[
  ('What it tests', '''SNR, SIR and SINR; Shannon capacity with interference treated as Gaussian noise; outage capacity in Rayleigh fading (Ch 2 p.48–51). 2025-26 S2 Q1(a)(iii) gives the same C<sub>ε</sub> formula.'''),
  ('Background', '''SNR = S/N, SIR = S/I, SINR = S/(I + N); C = B log₂(1 + x) with x linear; Rayleigh outage 1 − e<sup>−γ₀/γ̄</sup> (memorise), inverted γ₀ = γ̄ ln(1/(1 − ε)).'''),
  ('Method', '''(a) Three ratios → dB → Shannon with the SINR; (b) I = 0, use the SNR; (c) γ<sub>min</sub> = γ̄ ln(1/(1 − ε)) first, then Shannon, and compare with the AWGN B log₂(1 + γ̄).'''),
  ('Key step', '''For ε = 1%, ln(1/0.99) = 0.01005, so γ<sub>min</sub> ≈ γ̄/100: 20 dB below the average, which is the fade margin.'''),
  ('Common mistakes', '''With interference use the SINR, not the SNR; keep the power units consistent; use linear values inside log₂; the ln in (c) is the natural log.'''),
  ('Intuition', '''When interference is 10 times the noise, SINR ≈ SIR and the system is interference-limited. Rayleigh fading forces a margin for the worst 1% of the time, so the capacity that can be guaranteed is far below the one for the average SNR.'''),
  ('Link', '''Practice 2 Q3 (SINR, MUD); mock B·Q1 (Rayleigh outage and fade margin); the SNR/SIR/SINR and fade-margin boxes in section 2.7 of the learning page.''')])

# ---------------------------------------------------------------- focused practice: free space and two-ray
EN['p8q10'] = dict(
 idea=r'''Use the free-space formula \(P_r=P_tG_tG_r\big(\frac{\lambda}{4\pi d}\big)^2\) in dB; distance and frequency both appear squared, so each doubling costs 6 dB; in (c) compute with the simplified model and compare: the difference is tens of dB.''',
 steps=[
  r'''<b>(a) Wavelength and transmit power</b>:
\[\begin{aligned}\lambda&=\frac cf=\frac{3\times10^8}{9\times10^8}=0.333\text{ m}\\P_t&=1\text{ W}=10\log_{10}\frac{1000\text{ mW}}{1\text{ mW}}=30\text{ dBm}\end{aligned}\]''',
  r'''<b>(a) Free-space gain</b>: Friis formula (Ch 2 p.4) \(P_r=P_tG_tG_r\big(\frac{\lambda}{4\pi d}\big)^2\) with G<sub>t</sub> = G<sub>r</sub> = 1. The square becomes 20 log in dB:
\[\begin{aligned}\frac{\lambda}{4\pi d}&=\frac{0.333}{4\pi\times1000}=\frac{0.333}{12566}\\&=2.65\times10^{-5}\\20\log_{10}\frac{\lambda}{4\pi d}&=20\log_{10}(2.65\times10^{-5})\\&=-91.5\text{ dB}\end{aligned}\]''',
  r'''<b>(a) Received power and path loss</b>:
\[\begin{aligned}P_r&=30-91.5=-61.5\text{ dBm}\\ PL&=P_t-P_r=30-(-61.5)=91.5\text{ dB}\end{aligned}\]
Check with the Part A formula (f in MHz, d in km):
\[\begin{aligned}PL&=32.44+20\log_{10}900+20\log_{10}1\\&=32.44+59.08+0=91.5\text{ dB}\ \checkmark\end{aligned}\]''',
  r'''<b>(b) Double the distance</b>: \(P_r\propto d^{-2}\), so d → 2d makes the power 1/4:
\[\Delta=10\log_{10}4=20\log_{10}2=6.02\text{ dB}\]
\(P_r(2\text{ km})=-61.53-6.02=-67.5\) dBm.''',
  r'''<b>(b) Then double the frequency</b>: \(P_r\propto\lambda^2\propto f^{-2}\): doubling f halves λ and makes the power 1/4 again, another 6.02 dB down: \(P_r=-67.55-6.02=-73.6\) dBm. Reason: the effective area of a unity-gain antenna is proportional to λ², so at a higher frequency the receiving antenna "catches" less power.''',
  r'''<b>(c) Simplified model</b>: \(P_r=P_t+K_{dB}-10\gamma\log_{10}(d/d_0)\) (p.8) with \(\log_{10}(1000/1)=3\):
\[\begin{aligned}P_r&=30+(-31.5)-10\times3.5\times3\\&=30-31.5-105=-106.5\text{ dBm}\end{aligned}\]''',
  r'''<b>(c) Comparison and explanation</b>: the two differ by \(-61.5-(-106.5)=45\) dB, a factor of \(10^{4.5}\approx3\times10^4\). Check: the two models almost agree at 1 m (free space gives \(20\log_{10}(\lambda/4\pi)=-31.5\) dB = K<sub>dB</sub>), and after that they drift apart by 35 − 20 = 15 dB per decade of distance; 1 m → 1 km is 3 decades, 3 × 15 = 45 dB ✓. Reason: in a city, buildings block the path and cause many reflections, so the power falls much faster with distance (γ = 3.5 instead of 2). The free-space model would overestimate the received power by about 45 dB and get the coverage and outage completely wrong.'''],
 ans='(a) P<sub>r</sub> ≈ −61.5 dBm, path loss ≈ 91.5 dB; (b) 6 dB each (−67.5 dBm, then −73.6 dBm); (c) −106.5 dBm, about 45 dB below free space, so free space would grossly overestimate',
 official='none (self-written practice question); all numbers checked by src/p2build/verify_mock.py',
 note='''A coincidence: at 900 MHz the free-space gain at 1 m, 20 log₁₀(λ/4π) = −31.5 dB, equals the K<sub>dB</sub> used in (c). So both models agree at 1 m and differ only in the exponent: per decade of distance, free space loses 20 dB while γ = 3.5 loses 35 dB. The lecturer warned that in a past quiz some students used the free-space model on a simplified-model question.''',
 kp=[
  ('What it tests', '''The free-space (Friis) formula and its d⁻², f⁻² behaviour; how it differs from the simplified path loss model (Ch 2 p.3–4, p.8). Not asked directly in the practices or past papers, but the lecturer warned that past quiz students used free space on a simplified-model question.'''),
  ('Background', '''P<sub>r</sub> = P<sub>t</sub>G<sub>t</sub>G<sub>r</sub>(λ/4πd)²; λ = c/f; 1 W = 30 dBm; simplified model P<sub>r,dB</sub> = P<sub>t,dB</sub> + K<sub>dB</sub> − 10γ log₁₀(d/d₀).'''),
  ('Method', '''(a) Find λ, then in dB P<sub>r</sub> = P<sub>t</sub> + 20 log₁₀(λ/4πd); (b) squared dependence → 6 dB per doubling; (c) use the simplified model and compare with (a).'''),
  ('Key numbers', '''900 MHz, 1 km: path loss 91.5 dB; per decade of distance γ = 2 loses 20 dB, γ = 3.5 loses 35 dB; at 1 km the two models differ by about 45 dB.'''),
  ('Common mistakes', '''If the question says simplified path loss model, do not use free space; convert W to dBm; 20 log₁₀, not 10 log₁₀ (λ/4πd is an amplitude ratio, its square is the power ratio).'''),
  ('Intuition', '''Free space is the ideal "nothing in the way" case where power only spreads over a sphere; real cities block and reflect, so the power falls much faster.'''),
  ('Link', '''Part A Ch 5 (n = 2); focused Q2 two-ray (n = 4); mock A·Q2 (simplified model).''')])

EN['p8q11'] = dict(
 idea=r'''Find the critical distance from λ; beyond it, use the two-ray formula directly (note that it contains no λ); for (c), read off the power of each quantity in the formula and convert to dB.''',
 steps=[
  r'''<b>(a) Critical distance</b>: \(\lambda=c/f=3\times10^8/9\times10^8=0.333\) m; use the formula on Ch 2 p.5:
\[d_c=\frac{4h_th_r}{\lambda}=\frac{4\times30\times1.5}{0.333}=\frac{180}{0.333}=540\text{ m}\]''',
  r'''<b>(b) Two-ray received power</b>: first confirm the d⁻⁴ formula applies: 5000 m ≫ d<sub>c</sub> = 540 m ✓. With G<sub>t</sub> = G<sub>r</sub> = 1:
\[\begin{aligned}(h_th_r)^2&=(30\times1.5)^2=45^2=2025\text{ m}^4\\d^4&=5000^4=6.25\times10^{14}\text{ m}^4\\P_r&=\frac{10\times2025}{6.25\times10^{14}}=3.24\times10^{-11}\text{ W}\\&=10\log_{10}\frac{3.24\times10^{-11}}{10^{-3}}\text{ dBm}\\&=-74.9\text{ dBm}\end{aligned}\]
To convert to dBm, divide by 1 mW = 10⁻³ W.''',
  r'''<b>(b) Compare with free space</b>: at the same 5 km:
\[\begin{aligned}\frac{\lambda}{4\pi d}&=\frac{0.333}{4\pi\times5000}=5.31\times10^{-6}\\P_r&=10\times(5.31\times10^{-6})^2=2.81\times10^{-10}\text{ W}\\&=-65.5\text{ dBm}\end{aligned}\]
The two-ray value is −65.5 − (−74.9) = 9.4 dB lower: far away the ground-reflected wave is almost in antiphase with the direct wave, so most of it cancels. Check: the ratio of the two is \(\big(\frac{4\pi h_th_r}{\lambda d}\big)^2=\big(\frac{565.5}{1667}\big)^2=0.115\), and \(10\log_{10}0.115=-9.4\) dB ✓.''',
  r'''<b>(c)(i) Double the distance</b>: \(P_r\propto d^{-4}\), so the power becomes \(1/2^4=1/16\): \(10\log_{10}16=40\log_{10}2=12.0\) dB, <b>12 dB down</b> (5 km → 10 km: −74.9 → −86.9 dBm). Free space would lose only 6 dB.''',
  r'''<b>(c)(ii) Double the frequency</b>: the formula \(P_tG_tG_r(h_th_r)^2/d^4\) contains no λ, so the received power is <b>unchanged</b> (0 dB), whereas free space would lose 6 dB. Note that \(d_c=4h_th_r/\lambda\) doubles to 1080 m with the frequency; 5 km is still beyond d<sub>c</sub>, so the formula still applies.''',
  r'''<b>(c)(iii) Double the base station antenna height</b>: \(P_r\propto h_t^2\), so the power becomes 4 times: \(10\log_{10}4=20\log_{10}2=6.0\) dB, <b>6 dB up</b>. d<sub>c</sub> also becomes 1080 m, still well below 5 km. This is one reason base station antennas are mounted high.'''],
 ans='(a) d<sub>c</sub> = 540 m; (b) −74.9 dBm, about 9.4 dB below free space (−65.5 dBm); (c) doubling distance −12 dB, doubling frequency no change, doubling antenna height +6 dB',
 official='none (self-written practice question); all numbers checked by src/p2build/verify_mock.py',
 note='''For d &lt; d<sub>c</sub> the direct and reflected waves alternately add and cancel, so the power rises and falls with distance and the d⁻⁴ formula does not apply; only beyond d<sub>c</sub> does it fall steadily as d⁻⁴. This is the n = 2 (free space) and n = 4 (two-ray, far) of Part A Ch 5, and one reason why γ in the simplified model usually lies between 2 and 4.''',
 kp=[
  ('What it tests', '''The two-ray model: critical distance d<sub>c</sub> = 4h<sub>t</sub>h<sub>r</sub>/λ and P<sub>r</sub> ∝ (h<sub>t</sub>h<sub>r</sub>)²/d⁴ far away (Ch 2 p.5). Not asked directly in the practices or past papers.'''),
  ('Background', '''λ = c/f; power in dBm = 10 log₁₀(W) + 30; powers to dB: if a quantity appears to the n-th power, doubling it changes the result by n × 3 dB.'''),
  ('Method', '''(a) Substitute into d<sub>c</sub>; (b) check d &gt; d<sub>c</sub>, use the two-ray formula, then compare with free space; (c) read the powers of d, λ and h<sub>t</sub>: d⁻⁴ → −12 dB, λ⁰ → no change, h<sub>t</sub>² → +6 dB.'''),
  ('Key numbers', '''d<sub>c</sub> = 540 m; at 5 km two-ray −74.9 dBm, free space −65.5 dBm, a 9.4 dB difference.'''),
  ('Common mistakes', '''The d⁻⁴ formula is not valid for d &lt; d<sub>c</sub>; the far two-ray formula has no λ, so the power does not change with frequency; antenna height enters squared.'''),
  ('Intuition', '''Far away the ground reflection is almost opposite in phase to the direct wave and cancels most of it, leaving a small difference, so the power falls faster than in free space; raising the antenna increases the path difference and recovers some power.'''),
  ('Link', '''Part A Ch 5 (n = 4); focused Q1 free space (n = 2); the derivation box in section 2.1 of the learning page.''')])

EN['p8q12'] = dict(
 idea=r'''Each part isolates one effect and uses its own formula: path loss gives the mean; shadowing is Gaussian in dB, so use Q; Rayleigh SNR is exponential, so use 1 − e<sup>−γ₀/γ̄</sup>; Rician needs only K; flat/selective compares σ with T<sub>s</sub>; fast/slow compares T<sub>C</sub> with T<sub>s</sub>.''',
 steps=[
  r'''<b>(a) Average received power and SNR</b>: \(P_t=1\) W = 30 dBm and \(\log_{10}(1000/1)=3\); use the simplified model (Ch 2 p.8):
\[\begin{aligned}P_r&=P_t+K_{dB}-10\gamma\log_{10}\frac d{d_0}\\&=30-40-10\times3\times3=-100\text{ dBm}\end{aligned}\]
Average SNR: dBm − dBm = dB, \(\bar\gamma=-100-(-120)=20\) dB, linear \(10^{20/10}=100\).''',
  r'''<b>(b) Shadowing outage</b>: shadowing makes the received power in dB Gaussian, \(\mathcal N(-100,\ 8^2)\). Margin \(x=-100-(-110)=10\) dB (p.14–15):
\[P_{out}=Q\Big(\frac x\sigma\Big)=Q\Big(\frac{10}{8}\Big)=Q(1.25)=0.106\]
Q table: Q(1.25) = 0.1056, about 10.6%.''',
  r'''<b>(c) Rayleigh outage</b>: in Rayleigh fading the instantaneous SNR is exponential, \(P_{out}=1-e^{-\gamma_0/\bar\gamma}\) (p.26, p.51). Convert the threshold to linear first: \(\gamma_0=10^{10/10}=10\):
\[\begin{aligned}\gamma_0/\bar\gamma&=10/100=0.1\\P_{out}&=1-e^{-0.1}=1-0.905=0.0952\end{aligned}\]
About 9.5%. Check: for small x, \(1-e^{-x}\approx x=0.1\), and the exact value is slightly smaller ✓.''',
  r'''<b>(d) Rician K factor</b>: by definition (p.28), K = LOS power / scattered power \(=s^2/2\sigma^2=4\):
\[K_{dB}=10\log_{10}4=6.02\text{ dB}\]''',
  r'''<b>(d) How the outage changes</b>: it becomes <b>smaller</b> (below the 9.5% of (c)). Reason: a strong LOS path keeps the envelope away from 0, so deep fades are rarer and the SNR falls below 10 dB less often. The two limits (p.28): K = 0 reduces to Rayleigh, outage 9.5%; K → ∞ approaches AWGN, the SNR stays at 20 dB &gt; 10 dB and the outage → 0.''',
  r'''<b>(e) Flat or selective</b>: \(T_s=1/R_s=1/(10\times10^3)=100\ \mu\)s; rule of thumb (p.33):
\[\frac{\sigma_{T_m}}{T_s}=\frac{2\ \mu\text{s}}{100\ \mu\text{s}}=0.02\lt0.1\]
→ <b>flat fading</b>: the delay spread is only 2% of a symbol, so there is almost no ISI.''',
  r'''<b>(f) Fast or slow</b>: v = 54/3.6 = 15 m/s (p.34, p.36):
\[\begin{aligned}f_m&=\frac{vf_c}{c}=\frac{15\times2\times10^9}{3\times10^8}=100\text{ Hz}\\T_C&\approx\frac1{f_m}=\frac1{100}=10\text{ ms}\end{aligned}\]
\(T_s/T_C=100\ \mu\text{s}/10\text{ ms}=0.01\ll1\): the channel hardly changes during a symbol → <b>slow fading</b> (p.37). Together with (e): flat, slow fading.'''],
 ans='(a) −100 dBm, 20 dB; (b) ≈ 10.6%; (c) ≈ 9.5%; (d) K = 6.0 dB, outage below 9.5%; (e) flat (0.02 &lt; 0.1); (f) slow (T<sub>C</sub> ≈ 10 ms ≫ 100 µs)',
 official='none (self-written practice question); all numbers checked by src/p2build/verify_mock.py',
 note='''Rician numbers for reference (not in the slides; numerical integration; the quiz will not ask you to compute them): with the same 20 dB average and 10 dB threshold, K = 4 gives about 1.6% outage, K = 10 about 0.07%, and K = 0 returns exactly the Rayleigh 9.5%. The stronger the direct path, the fewer the deep fades.''',
 kp=[
  ('What it tests', '''The formula and use of each of six Ch 2 channel effects: simplified path loss (p.8), shadowing outage (p.12–16), Rayleigh outage (p.25–26), Rician factor (p.27–28), flat/selective (p.31–33), fast/slow (p.34–36).'''),
  ('Background', '''Path loss in dB (memorise); P<sub>out</sub> = Q(margin/σ) (memorise); p(γ) = (1/γ̄)e<sup>−γ/γ̄</sup> and 1 − e<sup>−γ₀/γ̄</sup> (memorise); K = s²/2σ²; σ/T<sub>s</sub> &lt; 0.1 (memorise); f<sub>m</sub> = v f<sub>c</sub>/c, T<sub>C</sub> ≈ 1/f<sub>m</sub>.'''),
  ('Method', '''First identify which effect the part asks about, then use its own formula: σ given → Q; average SNR and no line of sight → exponential; line of sight with a power ratio → K; flat? → σ vs T<sub>s</sub>; fast or slow? → T<sub>C</sub> vs T<sub>s</sub>.'''),
  ('Key differences', '''Shadowing subtracts in dB (margin/σ), Rayleigh divides in linear (γ₀/γ̄); Rayleigh = Rician with K = 0; flat/fast describe how the fading relates to the signal, Rayleigh/Rician describe the amplitude distribution, and the two classifications are independent.'''),
  ('Common mistakes', '''Using the exponential formula for shadowing or Q for Rayleigh; putting dB values into the Rayleigh formula; K is a power ratio, so use 10 log₁₀; answering only one dimension of the fading type.'''),
  ('Numbers', '''Same 20 dB average, 10 dB threshold: Rayleigh 9.5%, Rician K = 4 about 1.6%, K = 10 about 0.07% (numerical, beyond the slides).'''),
  ('Link', '''Mock A·Q2 (shadowing), B·Q1 (Rayleigh), A·Q3 (flat / fast-slow), C·Q2 (fading type); the "which outage formula" table at the end of Ch 2 on the learning page.''')])

EN['p8q12']['detail'] = r'''      <details class="deep">
        <summary>Step by step: what each of the six effects covers and which formula it uses</summary>
        <div class="deep-body">
          <h4><span class="st">Table</span>The differences at a glance</h4>
          <div class="tw"><table class="mini"><thead><tr><th>Effect</th><th>Describes</th><th>Random?</th><th>Formula</th><th>Used in</th><th>Memorise?</th></tr></thead><tbody>
            <tr><td>Path loss</td><td>Large scale: mean power falls with distance</td><td>No</td><td>\(P_r=P_t+K_{dB}-10\gamma\log_{10}(d/d_0)\)</td><td>(a) mean power</td><td>Yes</td></tr>
            <tr><td>Shadowing</td><td>Large scale: buildings and hills, slow fluctuation about the mean</td><td>Gaussian in dB</td><td>\(P_{r,dB}\sim\mathcal N(\text{mean},\sigma^2)\)</td><td>(b) Q(margin/σ), subtract in dB</td><td>Yes</td></tr>
            <tr><td>Rayleigh</td><td>Small scale: multipath, no line of sight</td><td>Exponential SNR</td><td>\(p(\gamma)=\frac1{\bar\gamma}e^{-\gamma/\bar\gamma}\)</td><td>(c) 1 − e<sup>−γ₀/γ̄</sup>, divide in linear</td><td>Yes</td></tr>
            <tr><td>Rician</td><td>Small scale: multipath plus a direct path</td><td>Rician</td><td>\(K=s^2/2\sigma^2\) (PDF given in the exam)</td><td>(d) K, qualitative</td><td>Know what K means</td></tr>
            <tr><td>Flat / selective</td><td>Frequency: echoes shorter or longer than a symbol</td><td>A judgement</td><td>\(\sigma_{T_m}/T_s\lt0.1\), or B<sub>s</sub> &lt; B<sub>C</sub></td><td>(e)</td><td>Memorise 0.1</td></tr>
            <tr><td>Fast / slow</td><td>Time: does the channel change within a symbol</td><td>A judgement</td><td>\(f_m=vf_c/c\), \(T_C\approx1/f_m\)</td><td>(f) T<sub>s</sub> ≪ T<sub>C</sub> → slow</td><td>Worth remembering</td></tr>
          </tbody></table></div>

          <h4><span class="st">Layers</span>The first four stack on top of each other</h4>
          <p>The actual received power = the mean set by <b>path loss</b> (changes over hundreds of metres to kilometres) + the slow fluctuation of <b>shadowing</b> around it (changes when you pass a building, tens of metres) + the fast fluctuation of <b>multipath</b> (Rayleigh or Rician, changes within half a wavelength, about 7.5 cm at 2 GHz). A question usually asks about one layer at a time, so read carefully which one it means. (The comparison of the three scales is a supplement beyond the slides.)</p>

          <h4><span class="st">Pitfalls</span>The three pairs most often confused</h4>
          <ul>
            <li><b>Shadowing vs Rayleigh:</b> shadowing gives σ (dB), so compute the margin in dB and use Q; Rayleigh gives an average SNR and no σ, so convert to linear, divide, and use the exponential formula. With the same 10 dB margin, shadowing (σ = 8 dB) gives 10.6% here and Rayleigh 9.5%, from completely different formulas.</li>
            <li><b>Rayleigh vs Rician:</b> Rayleigh is the special case of Rician with K = 0 (no direct path). The larger K, the stronger the direct path and the closer to no fading, so a line-of-sight path lowers the outage probability.</li>
            <li><b>Flat/fast vs Rayleigh/Rician:</b> independent questions. Flat/selective and fast/slow describe how the fading relates to the signal (are echoes long, does it change quickly); Rayleigh/Rician describe the distribution of the amplitude. A channel can be "flat, slow and Rayleigh" at the same time.</li>
          </ul>

          <h4><span class="st">Exam</span>Compact answer</h4>
          <div class="tmpl">
            <p>(a) \(P_r=30-40-30\log_{10}1000=-100\) dBm; average SNR = −100 − (−120) = 20 dB.</p>
            <p>(b) Shadowing makes the received power in dB Gaussian with mean −100 dBm and σ = 8 dB; margin = 10 dB, so \(P_{out}=Q(10/8)=Q(1.25)=0.106\).</p>
            <p>(c) In Rayleigh fading the SNR is exponential: \(P_{out}=1-e^{-\gamma_0/\bar\gamma}=1-e^{-10/100}=0.0952\).</p>
            <p>(d) K = 4 = 6.0 dB. The line-of-sight component makes deep fades less likely, so the outage probability is lower than in (c); K = 0 gives Rayleigh and K → ∞ gives AWGN.</p>
            <p>(e) \(\sigma_{T_m}/T_s=2\ \mu s/100\ \mu s=0.02\lt0.1\): flat fading. (f) \(f_m=vf_c/c=100\) Hz, \(T_C\approx1/f_m=10\) ms ≫ \(T_s\): slow fading.</p>
          </div>
          <div class="ans">In one line: path loss sets the mean, shadowing uses Q (subtract in dB), Rayleigh uses 1 − e<sup>−γ₀/γ̄</sup> (divide in linear), Rician is about K (K = 0 is Rayleigh), flat/selective compares σ with T<sub>s</sub>, fast/slow compares T<sub>C</sub> with T<sub>s</sub>.</div>
        </div>
      </details>'''
