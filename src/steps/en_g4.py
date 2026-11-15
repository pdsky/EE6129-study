# g4: expanded English steps for p8q1-p8q12 (prac_8.html, self-written mock quiz on Ch1b + Ch2).
# Numbers recomputed with /usr/bin/python3 (src/steps/_work/g4/calc.py) and consistent with src/p2build/verify_mock.py.
STEPS = {

'p8q1': [
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
\[\begin{aligned}&0.7\times(10-7.3)^2+0.3\times(1-7.3)^2\\&=5.103+11.907=17.01\ \checkmark\end{aligned}\]''',
],

'p8q2': [
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
and 223 m &lt; 300 m agrees with the 6% &gt; 1% outage found at 300 m in (b) ✓.''',
],

'p8q3': [
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
Check: LCR \(L_Z=\sqrt{2\pi}f_m\rho e^{-\rho^2}=95.1\times0.905=86.1\) per second, and \(L_Z\bar\tau=86.1\times1.106\times10^{-3}=0.095\), exactly \(1-e^{-0.1}=0.095\) ✓ (the fraction of time below the threshold, p.43).''',
],

'p8q4': [
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
The result does not depend on γ̄. The exponential distribution has a long right tail: a few large values pull the mean up, so the SNR is above its mean only 36.8% of the time and below it 63.2% of the time.''',
],

'p8q5': [
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
Q table: Q(2.39) = 0.00842, i.e. about 0.84%. Check: the margin is about 2.4σ, so the result must lie between Q(2) = 0.023 and Q(2.5) = 0.0062 ✓.''',
],

'p8q6': [
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
Check: with all the power on subchannel 1, Shannon's formula directly gives \(\log_2(1+20)=\log_221\), the same ✓.''',
],

'p8q7': [
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
In other words, a single base station would need about \(10^{8.28/10}\approx6.7\) times the transmit power to do as well.''',
],

'p8q8': [
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
The threshold is about <b>18.2 dB</b> below the rms power. Back-substitution: \(1-e^{-0.0151}=0.0150\) ✓.''',
],

'p8q9': [
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
\(66.6/10.0=6.6\) times more. Reason: to stay out of outage 99% of the time, the Rayleigh link must set its rate by the minimum SNR (about 0 dB). Check: \(\bar\gamma_{dB}-\gamma_{min,dB}=20-0.02=19.98\) dB, exactly the 20 dB fade margin for ε = 1% on p.51 ✓ (same as Mock B Q1 (b)).''',
],

'p8q10': [
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
r'''<b>(c) Comparison and explanation</b>: the two differ by \(-61.5-(-106.5)=45\) dB, a factor of \(10^{4.5}\approx3\times10^4\). Check: the two models almost agree at 1 m (free space gives \(20\log_{10}(\lambda/4\pi)=-31.5\) dB = K<sub>dB</sub>), and after that they drift apart by 35 − 20 = 15 dB per decade of distance; 1 m → 1 km is 3 decades, 3 × 15 = 45 dB ✓. Reason: in a city, buildings block the path and cause many reflections, so the power falls much faster with distance (γ = 3.5 instead of 2). The free-space model would overestimate the received power by about 45 dB and get the coverage and outage completely wrong.''',
],

'p8q11': [
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
r'''<b>(c)(iii) Double the base station antenna height</b>: \(P_r\propto h_t^2\), so the power becomes 4 times: \(10\log_{10}4=20\log_{10}2=6.0\) dB, <b>6 dB up</b>. d<sub>c</sub> also becomes 1080 m, still well below 5 km. This is one reason base station antennas are mounted high.''',
],

'p8q12': [
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
\(T_s/T_C=100\ \mu\text{s}/10\text{ ms}=0.01\ll1\): the channel hardly changes during a symbol → <b>slow fading</b> (p.37). Together with (e): flat, slow fading.''',
],
}

IDEA = {}
