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
  r'''Convert the distances to \(x_i=10\log_{10}d_i\): 6.99, 13.98, 18.13, 20.41, 26.02, 30.00 (mean \(\bar x=19.26\)); the mean of \(y_i\) is \(\bar y=-106.67\).''',
  r'''Slope \(=\dfrac{\sum(x_i-\bar x)(y_i-\bar y)}{\sum(x_i-\bar x)^2}=-3.94\), so \(\gamma=3.94\).''',
  r'''Intercept \(K_{dB}=\bar y+\gamma\bar x=-106.67+3.94\times19.26=-30.8\) dB.''',
  r'''(b) Residual \(e_i=M_i-\hat y_i\): first compute the fitted prediction \(\hat y_i=K_{dB}-\gamma x_i=-30.79-3.94\,x_i\), then subtract it from the measurement \(M_i\).''' + RESID_TABLE
  + r'''\(\sum e_i^2=71.23\), so the MSE is \(\sigma_\psi^2=71.23/6=11.87\) and \(\sigma_\psi=3.45\) dB. (Least-squares residuals always sum to 0, a quick arithmetic check.)''',
  r'''The mean received power is 10 dB above the threshold: \(P_{out}=Q(10/\sigma_\psi)=Q(2.90)=1.85\times10^{-3}\).'''],
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
  r'''(a) The threshold is 15 − 10 = 5 dB below the mean, i.e. 5/8 = 0.625 standard deviations: \(P_{out}=Q(0.625)=0.266\).''',
  r'''(b) Require \(Q\big((\mu_\psi-10)/4\big)\lt0.01\). From the table \(Q(2.326)=0.01\); Q is decreasing, so \((\mu_\psi-10)/4>2.326\).''',
  r'''\(\mu_\psi>10+4\times2.326=19.3\) dBm.'''],
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
  r'''Treat \(P_r(\tau)\) as a uniform distribution on 0–10 µs: \(\mu_{T_m}=\dfrac{\int_0^{10}\tau\,d\tau}{\int_0^{10}d\tau}=\dfrac{50}{10}=5\) µs.''',
  r'''\(E[\tau^2]=\dfrac{\int_0^{10}\tau^2d\tau}{10}=\dfrac{1000/3}{10}=33.33\); \(\sigma_{T_m}=\sqrt{33.33-5^2}=\sqrt{8.33}=2.89\) µs. (Standard deviation of a uniform distribution = width/√12 = 10/3.46.)''',
  r'''(b) Flat fading: \(\sigma_{T_m}/T_s\lt0.1\) → \(T_s>28.9\) µs → \(R_s\lt1/28.9\,\mu s=34.6\) ksps.'''],
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
  r'''ρ = 0.1, \(e^{\rho^2}-1=e^{0.01}-1=0.01005\).''',
  r'''Denominator: \(\sqrt{2\pi}\times50\times0.1=2.5066\times5=12.53\).''',
  r'''\(AFD=0.01005/12.53=8.0\times10^{-4}\) s.'''],
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
  r'''(a) W: the <b>mean received power</b> due to path loss alone (the same for both base stations); \(Z_1,Z_2\): the <b>shadowing</b> components (dB) of the two links.''',
  r'''(b) Outage = both below T = W − Δ, i.e. \(Z_1\lt-\Delta\) and \(Z_2\lt-\Delta\). Each has probability \(P(Z_i\lt-\Delta)=Q(\Delta/\sigma)\) (by symmetry). Independent → multiply: \(P_{out}=[Q(\Delta/\sigma)]^2\).''',
  r'''(c) The two links share bY, which makes them correlated. Trick: <b>condition on Y first</b>; then \(Z_1,Z_2\) contain only the independent parts \(aY_1,aY_2\).''',
  r'''To match the form of the answer, let \(Y=\sigma u\), \(u\sim\mathcal N(0,1)\). Given u: \(Z_i\sim\mathcal N(b\sigma u,\ a^2\sigma^2)\),''' + C('P(Z<sub>i</sub> &lt; −Δ | u) = Q( (Δ + bσu) / (|a|σ) )'),
  r'''Given u the two links are independent: \(P(\text{outage}\mid u)=Q\big(\tfrac{\Delta+b\sigma u}{|a|\sigma}\big)^2\).''',
  r'''Average over the standard normal density of u, \(\tfrac{1}{\sqrt{2\pi}}e^{-u^2/2}\) (total probability theorem), which gives the result.'''],
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

EN['p2q3'] = dict(
 steps=[
  r'''(a) User 2 treated as noise: SINR = 10 / (10 + 0.1) = 0.990.''' + C('C₁ = 20×10⁶ × log₂(1 + 0.990) = 20×10⁶ × 0.993 = 19.86 Mbps'),
  r'''(b) User 1 completely removed, only noise remains: SNR = 10 / 0.1 = 100.''' + C('C₂ = 20×10⁶ × log₂(101) = 20×10⁶ × 6.658 = 133.16 Mbps')],
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
  r'''Expand: \(A_i\cos(2\pi t/T+\phi_j)=(A_i\cos\phi_j)\cos(2\pi t/T)+(-A_i\sin\phi_j)\sin(2\pi t/T)\). Every signal lies along the cos and sin directions.''',
  r'''Orthogonal: \(\int_0^T\cos(2\pi t/T)\sin(2\pi t/T)dt=\tfrac12\int_0^T\sin(4\pi t/T)dt=0\).''',
  r'''Normalise: \(\int_0^T\cos^2(2\pi t/T)dt=T/2\), so multiply by \(\sqrt{2/T}\) to get unit energy.'''],
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
  r'''Sending 0: \(y\sim\mathcal N(0,\sigma_0^2)\); sending 1: \(y\sim\mathcal N(1,\sigma_1^2)\). ML: choose the hypothesis with the larger likelihood.''',
  r'''Decide 1 when \(\dfrac{1}{\sigma_1}e^{-(y-1)^2/2\sigma_1^2}>\dfrac{1}{\sigma_0}e^{-y^2/2\sigma_0^2}\); taking logarithms:''' + C('g(y) = y²/(2σ₀²) − (y − 1)²/(2σ₁²) + ln(σ₀/σ₁) &gt; 0'),
  r'''g(y) = 0 is a quadratic in y; the root between 0 and 1 is the threshold ỹ: decide 1 if y &gt; ỹ, 0 if y &lt; ỹ. With equal variances ỹ = 0.5; with σ₁ &gt; σ₀ the threshold moves towards 0.''',
  r'''(b) Two error events: sending 0 and the noise pushes y above ỹ, probability \(Q(\tilde y/\sigma_0)\); sending 1 and y falls below ỹ, probability \(Q((1-\tilde y)/\sigma_1)\). Equal priors, weight ½ each.'''],
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
  r'''What matters in the floor formula is "echo length / symbol length". For BPSK a symbol is one bit, so the formula uses \(T_b\); for QPSK use the <b>symbol</b> duration \(T_s\).''',
  r'''\((3\,\mu s/T_s)^2=10^{-3}\) → \(3/T_s=0.0316\) → \(T_s=94.9\) µs.''',
  r'''QPSK carries 2 bits per symbol: \(R_b=2/T_s=2/94.9\,\mu s=21.08\) kbps. (Under the same conditions BPSK gives only 10.54 kbps.)'''],
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
  r'''Outage is mainly caused by <b>shadowing</b> (large-scale fading): buildings or terrain block the path between the mobile and a base station, keeping the signal low for a long time.''',
  r'''The base stations are at <b>different locations</b>, so the propagation paths differ and are unlikely to be blocked by the same obstacle; the shadowing on the different links is approximately independent.''',
  r'''Macro-diversity selects the strongest base station (or combines several). Outage occurs only when <b>all</b> links are below the threshold; for independent links \(P_{out}=\prod_iP_{out,i}\), much smaller than for a single link.''',
  r'''Example: a single link is in outage 10% of the time; two independent base stations are in outage together only 1% of the time ([Q(Δ/σ)]² in Practice 2 Q2). Correlated links reduce the benefit.'''],
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
  r'''(a) \(P_T=\sigma_n^2=1\), so γ = α. \(\bar\gamma=8\cdot\tfrac13+11\cdot\tfrac23=10\).''' + C('P̄<sub>s</sub> = ⅓·½e⁻⁸ + ⅔·½e⁻¹¹ = 5.59×10⁻⁵ + 0.56×10⁻⁵ = 6.15×10⁻⁵'),
  r'''(b) The MRC output SNR is the sum of the two branches. With independent branches the combinations are 8+8 = 16 (1/9), 8+11 = 19 (2 × 1/3 × 2/3 = 4/9), 11+11 = 22 (4/9).''' + C('γ̄<sub>Σ</sub> = (16 + 76 + 88)/9 = 20') + C('P̄<sub>s</sub> = ½[e⁻¹⁶·1/9 + e⁻¹⁹·4/9 + e⁻²²·4/9] = 7.56×10⁻⁹'),
  r'''\(g=\bar\gamma_\Sigma/\bar\gamma=20/10=2\); \(d=-\log_{10}\bar P_s/\log_{10}\bar\gamma=8.12/1=8.1\) (γ̄ is the per-branch input SNR, 10).''',
  r'''(c) \(E[\gamma_i]=E[r_i]+E[\beta]=(0.2+0.8)+(7/3+20/3)=1+9=10\), \(\bar\gamma_\Sigma=20\), g = 2.''',
  r'''\(\gamma_\Sigma=r_1+r_2+2\beta\); the three are independent, so the exponential factorises: \(E[e^{-\gamma_\Sigma}]=E[e^{-r_1}]\,E[e^{-r_2}]\,E[e^{-2\beta}]\).''' + C('E[e<sup>−r</sup>] = ⅓e<sup>−0.6</sup> + ⅔e<sup>−1.2</sup> = 0.1829 + 0.2008 = 0.3837') + C('E[e<sup>−2β</sup>] = ⅓e<sup>−14</sup> + ⅔e<sup>−20</sup> = 2.786×10⁻⁷') + C('P̄<sub>s</sub> = ½ × 0.3837² × 2.786×10⁻⁷ = 2.05×10⁻⁸, d = 8 − log₁₀2.05 = 7.7')],
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
  r'''(a) Take b = +1 (the other case is symmetric). \(z=y=\alpha\sqrt E+w\): the sum of two independent Gaussians is Gaussian.''' + C('mean α₀√E, variance σ₁²E + σ₂²'),
  r'''Error = z ≤ 0: \(P_b=P(z\le0)=Q\!\left(\dfrac{\alpha_0\sqrt E}{\sqrt{\sigma_1^2E+\sigma_2^2}}\right)\).''',
  r'''(b) Equal-weight sum: \(z=\sum_ky_k=b\sqrt E\sum_k\alpha_k+\sum_kw_k\). All \(\alpha_k\) and \(w_k\) are independent:''' + C('mean Mα₀√E, variance M(σ₁²E + σ₂²)'),
  r'''\(P_b=Q\!\left(\dfrac{M\alpha_0\sqrt E}{\sqrt{M(\sigma_1^2E+\sigma_2^2)}}\right)=Q\!\left(\dfrac{\sqrt M\,\alpha_0\sqrt E}{\sqrt{\sigma_1^2E+\sigma_2^2}}\right)\).'''],
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
  r'''Assume all three sub-channels get power: \(\sum_{i=1}^{3}\big(\tfrac1{\gamma_0}-\tfrac1{\gamma_i}\big)=1\Rightarrow\dfrac3{\gamma_0}=1+\dfrac1{80}+\dfrac1{40}+\dfrac1{40}=1.0625\).''',
  r'''\(\gamma_0=3/1.0625=2.82\). All three SNRs (80, 40, 40) exceed 2.82, so the assumption holds and no sub-channel is dropped.''',
  r'''Powers: \(P_1/P=1/2.82-1/80=0.342\), \(P_2/P=P_3/P=1/2.82-1/40=0.329\).''',
  r'''Capacity: \(C=B\sum\log_2(\gamma_i/\gamma_0)=10\text{ MHz}\times[\log_2(28.33)+2\log_2(14.17)]=10\times(4.82+7.65)\).'''],
 ans='C ≈ 124.7 Mbps ≈ 125 Mbps', official='125 Mbps ✓',
 kp=[
  ('What it tests', '''MIMO capacity with an informed transmitter: eigen-sub-channels plus water-filling (Ch 5 p.19, p.40; Ch 2 p.54–57).'''),
  ('Background', '''The SVD splits a MIMO channel into non-interfering parallel sub-channels; the water-filling formulas.'''),
  ('Method', '''① Assume every sub-channel gets power and find γ₀ from Σ(1/γ₀ − 1/γ<sub>i</sub>) = 1; ② check that the weakest γ<sub>i</sub> ≥ γ₀, otherwise drop it and repeat; ③ P<sub>i</sub>/P = 1/γ₀ − 1/γ<sub>i</sub>; ④ C = B Σ log₂(γ<sub>i</sub>/γ₀).'''),
  ('Key numbers', '''γ₀ = 3/1.0625 = 2.82; powers 0.342, 0.329, 0.329 (sum 1); C = 10 MHz × (4.82 + 7.65) = 124.7 Mbps.'''),
  ('Comparison 1', '''Equal power (uninformed transmitter): the SNRs become 80/3, 40/3, 40/3 and C = 122.1 Mbps, only 2% less. At high SNR channel knowledge at the transmitter matters little (p.41–42).'''),
  ('Comparison 2', '''At low SNR the difference is large: dividing all three SNRs by 100 (0.8, 0.4, 0.4), water-filling uses only the first sub-channel and gives 0.85 bit/s/Hz, while equal power gives 0.70 bit/s/Hz, 21% less.'''),
  ('Common mistakes', '''The γ<sub>i</sub> in water-filling is the SNR if <b>all</b> the power went to that sub-channel; with equal power each gets only P/3; multiply by B at the end.''')])

EN['p5q2'] = dict(
 steps=[
  r'''Received in the two slots: \(y_1=h_Au_1+h_Bu_2+w_1\), \(y_2=-h_Au_2^*+h_Bu_1^*+w_2\).''',
  r'''Conjugate \(y_2\) so that the unknowns appear as \(u_1,u_2\) without conjugates: \(y_2^*=h_B^*u_1-h_A^*u_2+w_2^*\).''',
  r'''In matrix form: \(\begin{bmatrix}y_1\\y_2^*\end{bmatrix}=\underbrace{\begin{bmatrix}h_A&h_B\\h_B^*&-h_A^*\end{bmatrix}}_{\mathbf F}\begin{bmatrix}u_1\\u_2\end{bmatrix}+\begin{bmatrix}w_1\\w_2^*\end{bmatrix}\), with \(\mathbf F^H\mathbf F=(|h_A|^2+|h_B|^2)\mathbf I\).''',
  r'''Pre-multiply by \(\mathbf F^H\); the two symbols separate completely:''' + C('z₁ = h<sub>A</sub>* y₁ + h<sub>B</sub> y₂* = (|h<sub>A</sub>|² + |h<sub>B</sub>|²)u₁ + h<sub>A</sub>* w₁ + h<sub>B</sub> w₂*') + C('z₂ = h<sub>B</sub>* y₁ − h<sub>A</sub> y₂* = (|h<sub>A</sub>|² + |h<sub>B</sub>|²)u₂ + h<sub>B</sub>* w₁ − h<sub>A</sub> w₂*'),
  r'''The noise variance is \((|h_A|^2+|h_B|^2)N_0\). Dividing by \(\|\mathbf h\|=\sqrt{|h_A|^2+|h_B|^2}\) brings it back to \(N_0\).'''],
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
  r'''γ = 10 dB = 10. \(10^{-d}\le10^{-3}\) → d ≥ 3.''',
  r'''N = 8, M = 4, try each r:<div class="tw"><table class="mini"><thead><tr><th>r</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th></tr></thead><tbody><tr><td>d = (8−r)(4−r)</td><td>32</td><td>21</td><td>12</td><td>5</td><td>0</td></tr></tbody></table></div>The largest r with d ≥ 3 is 3.''',
  r'''By definition of the multiplexing gain \(r=R/\log_2\mathrm{SNR}\), so \(R=r\log_2\gamma=3\times\log_210=3\times3.32=9.97\) bit/s/Hz.''',
  r'''(b) r = 3 → d = 5 → \(P_e=10^{-5}\).'''],
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
  r'''Let \(A=\sqrt{2E_b/N_0}\). Without ISI \(P_e=Q(A)\): signal amplitude \(\sqrt{E_b}\), noise standard deviation \(\sqrt{N_0/2}\).''',
  r'''(a) No equaliser: \(z(n)=\sqrt{E_b}(a_n+\alpha a_{n-1})+w(n)\). If the previous symbol has the same sign the amplitude is \((1+\alpha)\sqrt{E_b}\), otherwise \((1-\alpha)\sqrt{E_b}\), each half the time:''' + C('P<sub>e</sub> = ½Q((1 − α)A) + ½Q((1 + α)A)'),
  r'''With the equaliser: overall response \(H(z)U(z)=(1+\alpha z^{-1})(1-\alpha z^{-1})=1-\alpha^2z^{-2}\), so the ISI drops from α to α²; but the noise also passes through U(z) and its variance becomes \(\tfrac{N_0}{2}(1+\alpha^2)\) (sum of squared coefficients).''',
  r'''\(z(n)=\sqrt{E_b}(a_n-\alpha^2a_{n-2})+w^{\prime}(n)\): amplitudes \((1\pm\alpha^2)\sqrt{E_b}\), standard deviation scaled by \(\sqrt{1+\alpha^2}\):''' + C('P<sub>e</sub> = ½Q( (1 − α²)/√(1 + α²) · A ) + ½Q( (1 + α²)/√(1 + α²) · A )'),
  r'''(b) At high SNR the error rate is dominated by the term with the <b>smallest</b> Q argument. Compare: without equaliser \(1-\alpha\); with equaliser \((1-\alpha^2)/\sqrt{1+\alpha^2}\).''',
  r'''\(\dfrac{1-\alpha^2}{\sqrt{1+\alpha^2}}>1-\alpha\ \Leftrightarrow\ \dfrac{1+\alpha}{\sqrt{1+\alpha^2}}>1\ \Leftrightarrow\ (1+\alpha)^2>1+\alpha^2\ \Leftrightarrow\ 2\alpha>0\), which always holds for α &gt; 0.'''],
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
  r'''(a) Take \(b_n=+1\): if \(b_{n-1}=+1\) the amplitude is 1 + a, if \(b_{n-1}=-1\) it is 1 − a; the noise standard deviation is √0.1:''' + C('P<sub>e</sub> = ½Q((1 + a)/√0.1) + ½Q((1 − a)/√0.1)'),
  r'''(b) Ideal zero forcing: \(C(z)=\dfrac{1}{1+az^{-1}}=\sum_{k\ge0}(-a)^kz^{-k}\) (converges for |a| &lt; 1); the output is \(b_n\) plus filtered noise.''',
  r'''Noise variance = 0.1 × sum of squared coefficients = \(0.1\sum_k a^{2k}=\dfrac{0.1}{1-a^2}\).''',
  r'''\(P_e=Q\!\left(\dfrac{1}{\sqrt{0.1/(1-a^2)}}\right)=Q\!\left(\sqrt{\dfrac{1-a^2}{0.1}}\right)\).'''],
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
  r'''(a) Expand: \(u_n=A_n+\tfrac12A_{n-1}+z_n+q\big(A_{n+1}+\tfrac12A_n+z_{n+1}\big)\), so \(u_n-A_n=\tfrac q2A_n+\tfrac12A_{n-1}+qA_{n+1}+z_n+qz_{n+1}\).''',
  r'''All terms are independent with zero mean, so their mean squares add: \(E[(u_n-A_n)^2]=\tfrac{q^2}4+\tfrac14+q^2+1+q^2=1.25+2.25q^2\), minimised at q = 0.''',
  r'''With q = 0, \(u_n=y_n\) and the amplitude is 1.5 or 0.5:''' + C('P<sub>e</sub> = ½Q(1.5) + ½Q(0.5) = ½(0.0668) + ½(0.3085) = 0.188'),
  r'''(b) Previous decision correct: the ISI is cancelled exactly, \(u_n=A_n+z_n\), error probability \(Q(1)=0.159\).''',
  r'''Previous decision wrong (\(\hat A_{n-1}=-A_{n-1}\)): \(u_n=A_n+A_{n-1}+z_n\), amplitude 2 or 0 with equal probability, error probability \(\tfrac12Q(2)+\tfrac12\cdot\tfrac12=0.261\).''',
  r'''Let p be the long-run error rate: \(p=(1-p)\times0.159+p\times0.261\) → \(p=\dfrac{0.159}{1-0.261+0.159}=0.177\).'''],
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
  r'''(a) Flat: the sub-channel width B/N must be much smaller than the coherence bandwidth → \(N\gg B/B_C\). Slow: the OFDM symbol duration ≈ N/B must be much shorter than the coherence time 1/B<sub>d</sub> → \(N\ll B/B_d\). Hence \(B/B_C\ll N\ll B/B_d\).''',
  r'''(b) \(H_k=h_0+h_1e^{-j2\pi k/N}=0.8+0.6e^{-j\pi k/2}\):''' + C('H₀ = H₄ = 1.4, H₁ = 0.8 − 0.6j, H₂ = 0.2, H₃ = 0.8 + 0.6j') + 'Power gains |H<sub>k</sub>|² (k = 1, 2, 3, 4): 1, 0.04, 1, 1.96.',
  r'''(c) Equal capacity \(\log_2(1+|H_k|^2P_k)\) ⇔ the same \(|H_k|^2P_k=c\): \(P_k=c/|H_k|^2\).''' + C('c(1/1 + 1/0.04 + 1/1 + 1/1.96) = c × 27.51 = 10 → c = 0.3635') + C('P₁ = 0.36, P₂ = 9.09, P₃ = 0.36, P₄ = 0.19'),
  r'''(d) Water-filling: floor levels \(1/|H_k|^2\) = 1, 25, 1, 0.51. Filling all four gives a water level (10 + 27.51)/4 = 9.38 &lt; 25, so sub-channel 2 is dropped.''',
  r'''With three left: level μ = (10 + 1 + 1 + 0.51)/3 = 4.17, powers 3.17, 3.17, 3.66 (all positive).''' + C('C = log₂(4.17 × 1) + log₂(4.17 × 1) + log₂(4.17 × 1.96) = 2.06 + 2.06 + 3.03 = 7.15 bit'),
  r'''These 7.15 bit are carried by 4 sub-carriers, each occupying B/4, so per hertz: 7.15/4 = 1.79 bit/s/Hz.'''],
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
  r'''16-QAM carries 4 bits per symbol: the required total symbol rate is 2 Mbps / 4 = 500 k symbols/s.''',
  r'''With N sub-carriers: useful symbol duration T = N/B = N/600k; with the CP one OFDM symbol lasts T + 20 µs, during which each of the N sub-carriers sends one symbol.''',
  r'''\(\dfrac{N}{N/600\text{k}+20\,\mu s}=500\text{k}\) → \(N=0.8333N+10\) → N = 60.''',
  r'''T = 60/600 kHz = 100 µs; total OFDM symbol 100 + 20 = 120 µs = 0.12 ms.'''],
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
  r'''Impulse response h = [1, 0.9]: a direct path plus an echo one sample later; channel length L = 2, maximum delay spread = 1 sample.''',
  r'''The last sample of the previous OFDM block leaks into the first sample of the next block through 0.9z⁻¹. The CP must cover at least this 1 sample so the ISI stays inside the CP, which the receiver discards.''',
  r'''Because the CP is a copy of the block tail, the linear convolution looks like a circular convolution inside the receive window; after the DFT this gives exactly \(H_ks_k\), and the sub-carriers stay orthogonal.'''],
 ans='Minimum CP = 1 sample (symbol) = L − 1', official='1 symbol length ✓',
 kp=[
  ('What it tests', '''The minimum cyclic-prefix length (Ch 7 p.17–22).'''),
  ('Background', '''Z-transform: Z⁻¹ means one sample later; a channel with L taps has its longest echo L − 1 samples late.'''),
  ('Method', '''Read the impulse response h = [1, 0.9] from H(Z) → L = 2 → CP ≥ L − 1 = 1 sample.'''),
  ('Why it is enough', '''With CP ≥ L − 1 the N samples kept by the receiver contain only data from the current block, the linear convolution becomes circular, and after the DFT r<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + w<sub>k</sub> (derivation box in Section 7.4 of the learning page).'''),
  ('Why copy the tail', '''An empty guard interval would also block the previous block's echo, but the receive window would no longer see a complete periodic signal, the sub-carriers would lose orthogonality and ICI would appear. Only copying the tail keeps the circular structure.'''),
  ('Common mistakes', '''It is L − 1 = 1 sample, not L = 2; the size of the coefficient 0.9 does not matter, only how many samples the echo is delayed.'''),
  ('Variations', '''H(Z) = 1 + 0.5Z⁻³ → delay 3 samples → CP ≥ 3; in time, T<sub>G</sub> ≥ the maximum delay spread T<sub>D</sub>. Each extra CP sample lowers the efficiency to N/(N + G).''')])
