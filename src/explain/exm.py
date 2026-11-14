# -*- coding: utf-8 -*-
# 知识讲解 + 详细解析 for the 15 Part A worked examples (examples.html, id = slide page).
# Numbers checked by check_exm.py (run with /usr/bin/python3).
XPL = {

# ---------------------------------------------------------------- p.43–44
'p44': {'title': '知识讲解 + 详细解析：频谱效率 ηm 与话务换算', 'zh': '''
<h4><span class="st">知识讲解</span>频谱效率（spectral efficiency）到底在量什么</h4>
<p>频谱是运营商花大钱买来的。<b>频谱效率</b>回答一个问题：每 1 MHz 频谱、每 1 km² 面积，能撑起多少通话？讲义 Part A p.38–39 把它拆成两部分：<b>调制频谱效率 η<sub>m</sub></b>（modulation spectral efficiency）和<b>多址频谱效率 η<sub>a</sub></b>（multiple access spectral efficiency），总效率 η = η<sub>m</sub> × η<sub>a</sub>（p.46）。</p>
<p>η<sub>m</sub> 有两种写法：</p>
<ul>
<li><b>按信道数</b>（p.40）：η<sub>m</sub> = (B<sub>w</sub>/B<sub>c</sub>) / (B<sub>w</sub> · A<sub>c</sub> · N)，单位 channels/MHz/km²。B<sub>w</sub> 是系统带宽，B<sub>c</sub> 是信道间隔，A<sub>c</sub> 是一个小区的面积，N 是簇尺寸（复用因子）。</li>
<li><b>按话务量</b>（p.41）：η<sub>m</sub> = 系统承载的总话务量 / (带宽 × 总覆盖面积)，单位 Erlang/MHz/km²。本题用的是这一种。</li>
</ul>
<p>为什么分母只用一个小区的面积 4 km²？因为"总话务量 = 每小区话务量 × 小区数"，"总面积 = 每小区面积 × 小区数"，小区数上下约掉，剩下 η<sub>m</sub> = A<sub>小区</sub> / (B<sub>w</sub> × A<sub>c</sub>)。所以总覆盖 2000 km² 不影响结果。</p>
<p>另外两个工具：<b>话务量 A</b>（Erlang）= 呼叫次数 × 每次通话时长（单位要统一成小时），讲义 p.118；<b>Erlang B 表</b>：给定信道数 M 和阻塞率 GoS，查出一个小区最多能承载的话务量 A（p.119–121）。老师课上强调：频谱效率公式"要试着记住"（2025-26 S1 Q3(a)(iv) 考过）；Erlang B 考试<b>只查表</b>，附录会给表。</p>
<div class="tw"><table class="mini"><thead><tr><th>符号</th><th>含义</th><th>本题数值</th></tr></thead><tbody>
<tr><td>B<sub>w</sub></td><td>每家运营商的带宽</td><td>25 ÷ 2 = 12.5 MHz</td></tr>
<tr><td>B<sub>c</sub></td><td>信道间隔（AMPS）</td><td>30 kHz</td></tr>
<tr><td>N</td><td>簇尺寸</td><td>7</td></tr>
<tr><td>A<sub>c</sub></td><td>小区面积</td><td>4 km²</td></tr>
<tr><td>λ、h</td><td>每用户呼叫率、平均通话时长</td><td>1.2 次/小时、100 s</td></tr>
</tbody></table></div>
<h4><span class="st">详细解析</span>一步一步算</h4>
<ol>
<li><b>分带宽</b>：两家运营商平分 25 MHz，每家 12.5 MHz。</li>
<li><b>算总信道数</b>：带宽 ÷ 信道宽。12.5×10⁶ ÷ 30×10³ = 416.67，信道不能是小数，<b>向下取整</b>为 416。</li>
<li><b>扣控制信道</b>：这 416 条要分给一簇 7 个小区，每个小区自己要留 3 条控制信道（建立呼叫、寻呼用），所以整簇扣 3 × 7 = 21 条，剩 395 条业务信道（voice channels）。</li>
<li><b>分到每个小区</b>：395 ÷ 7 = 56.43，向下取整 56 条。</li>
<li><b>查 Erlang B 表</b>：在 M = 56 那一行、GoS = 0.02 那一列读出 A = 45.9 Erlang/小区（用公式精确算是 45.88，与表一致）。这就是一个小区在 2% 阻塞率下能承载的最大话务量。</li>
<li><b>求 η<sub>m</sub></b>：45.9 ÷ (12.5 MHz × 4 km²)。</li>
<li><b>话务量 → 呼叫数</b>：A = (每小时呼叫数) × h，所以每小时呼叫数 = A ÷ h。h = 100 s = 100/3600 小时。</li>
<li><b>呼叫数 → 用户数</b>：每个用户每小时打 1.2 次，所以用户数 = 呼叫数 ÷ 1.2。</li>
</ol>
<div class="calc">12.5×10⁶ ÷ 30×10³ = 416.67 → 416 条<br>416 − 3 × 7 = 395 条<br>395 ÷ 7 = 56.43 → 56 条/小区<br>Erlang B（M = 56，2%）→ A = 45.9 Er/小区；45.9 ÷ 4 = 11.5 Er/km²<br>η<sub>m</sub> = 45.9 ÷ (12.5 × 4) = 0.918 ≈ 0.92 Er/MHz/km²<br>呼叫数 = 45.9 × 3600 ÷ 100 = 1652.4 次/小时/小区；1652.4 ÷ 4 = 413.1 次/小时/km²<br>用户数 = 1652.4 ÷ 1.2 = 1377 用户/小区</div>
<p><b>验算</b>（换一条路）：每用户话务量 A<sub>u</sub> = 1.2 × 100/3600 = 0.0333 Er，用户数 = 45.9 ÷ 0.0333 = 45.9 × 30 = 1377，和第 8 步一致。</p>
<p><b>顺带两个量</b>：① 按信道数的 η<sub>m</sub>（p.40）= 1/(B<sub>c</sub> · A<sub>c</sub> · N) = 1/(0.03 × 4 × 7) = 1.19 channels/MHz/km²，可以看到 B<sub>w</sub> 约掉了，这正是 p.41 说"η<sub>m</sub> 与系统带宽无关"的原因。② 如果追问全区用户数：2000 ÷ 4 = 500 个小区，500 × 1377 = 688,500 用户（这是变式，讲义没算）。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>控制信道扣 21 条，不是 3 条；416.67 和 56.43 都要向下取整。</li>
<li>h 要换成小时（100/3600），否则呼叫数差 3600 倍。</li>
<li>单位别丢：Er/MHz/km²、次/小时/小区、用户/小区。老师说答案要写单位。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Bandwidth per operator = 25/2 = 12.5 MHz. Number of 30 kHz channels = 12.5×10⁶ / 30×10³ = 416. Voice channels = 416 − 3×7 = 395; per cell = 395/7 ≈ 56. From the Erlang B table (M = 56, GoS = 2%), A = 45.9 Erlangs/cell = 11.5 Erlangs/km². Spectral efficiency ηm = 45.9 / (12.5 MHz × 4 km²) = 0.92 Erlangs/MHz/km². Calls per hour per cell = 45.9 × 3600/100 = 1652.4 calls/hr/cell (413.1 calls/hr/km²). Users per cell = 1652.4/1.2 = 1377 users/cell.</p></div>
<div class="ans">一句话：带宽 → 信道 → 扣控制 → 分小区 → 查表得 A → A ÷ (B<sub>w</sub> × A<sub>c</sub>) 就是 η<sub>m</sub>，A ÷ h 是呼叫数，再 ÷ 1.2 是用户数。</div>
'''},

# ---------------------------------------------------------------- p.47
'p47': {'title': '知识讲解 + 详细解析：窄带 TDMA 的多址效率 ηa', 'zh': '''
<h4><span class="st">知识讲解</span>多址频谱效率 η<sub>a</sub>：时频格子里有多少是"真话"</h4>
<p>把系统资源画成一张<b>时间 × 频率</b>的格子图。多址频谱效率 η<sub>a</sub>（讲义 Part A p.45）= 真正用来传语音（数据）的时频面积 ÷ 系统全部时频面积，所以一定 ≤ 1。剩下的部分花在了开销上：控制信道、保护时隙、同步和训练序列等。</p>
<div class="tw"><table class="mini"><thead><tr><th>系统</th><th>公式</th><th>含义</th></tr></thead><tbody>
<tr><td>FDMA（p.45）</td><td>η<sub>a</sub> = B<sub>e</sub>N<sub>t</sub>/B<sub>w</sub></td><td>频率方向的利用率</td></tr>
<tr><td>宽带 TDMA（p.45）</td><td>η<sub>a</sub> = T<sub>s</sub>M<sub>t</sub>/T<sub>f</sub></td><td>时间方向的利用率</td></tr>
<tr><td>窄带 TDMA（p.46）</td><td>η<sub>a</sub> = (T<sub>s</sub>M<sub>t</sub>/T<sub>f</sub>)(B<sub>u</sub>N<sub>u</sub>/B<sub>w</sub>)</td><td>时间利用率 × 频率利用率</td></tr>
</tbody></table></div>
<p>符号：T<sub>s</sub> = 一个时隙中<b>纯信息</b>占的时间；T<sub>f</sub> = 帧长；M<sub>t</sub> = 每帧时隙数；B<sub>u</sub> = 一个子带的带宽；N<sub>u</sub> = 子带数（同一时隙、不同频率的用户数）；B<sub>w</sub> = 总带宽。</p>
<p><b>窄带 TDMA</b>（narrowband TDMA）是先把总带宽切成很多 30 kHz 子带（像 FDMA），每个子带里再按时间轮流用（TDMA）。所以两个方向的浪费都要算，两个因子相乘。北美 TDMA（IS-54/IS-136，也叫 D-AMPS）就是这种结构。</p>
<h4><span class="st">详细解析</span>先算时间因子，再算频率因子</h4>
<ol>
<li><b>每个时隙多长</b>：一帧 40 ms 分成 6 个时隙，每个 40/6 = 6.67 ms。</li>
<li><b>其中多少是语音</b>：每个时隙的总速率是 16.2 kbps，其中语音只占 13 kbps，比例 13/16.2 = 0.8025。剩下的 3.2 kbps 是同步、保护、控制等开销。所以 T<sub>s</sub> = 0.8025 × 6.67 ms。</li>
<li><b>时间因子</b>：T<sub>s</sub>M<sub>t</sub>/T<sub>f</sub>。注意 40/6 × 6/40 = 1 会约掉，时间因子其实就等于 13/16.2。</li>
<li><b>频率因子</b>：395 条数据信道，每条 30 kHz，共占 395 × 30 = 11,850 kHz，总带宽 12,500 kHz，比例 0.948。这和例 1（p.45）的 FDMA 效率是同一个数。</li>
<li><b>相乘</b>得到 η<sub>a</sub>。</li>
</ol>
<div class="calc">T<sub>s</sub> = (13/16.2) × (40/6) = 0.8025 × 6.667 = 5.35 ms<br>时间因子 = 5.35 × 6 ÷ 40 = 0.8025<br>频率因子 = 30 × 395 ÷ 12500 = 0.948<br>η<sub>a</sub> = 0.8025 × 0.948 = 0.7607 ≈ 0.76</div>
<p><b>合理性检查</b>：η<sub>a</sub> 在 0 和 1 之间，且比两个因子都小（两次打折）。0.76 表示约 24% 的时频资源用在开销和控制上。讲义 p.47 的写法 η<sub>a</sub> = (13/16.2) × (30 × 395/12500) 就是把约掉的部分直接省了。</p>
<h4><span class="st">课外补充</span>16.2 kbps 从哪来（讲义没讲）</h4>
<p>IS-54 每个 30 kHz 载波总速率 48.6 kbps，一个全速率用户用每帧 6 个时隙中的 2 个，即 1/3 的载波，48.6 ÷ 3 = 16.2 kbps。考试不用写这一点，只是帮你理解题目数据。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>T<sub>s</sub> 不是 40/6 = 6.67 ms，要乘 13/16.2 扣掉开销（"carrying pure information"）。</li>
<li>窄带 TDMA 必须乘频率因子；只算 T<sub>s</sub>M<sub>t</sub>/T<sub>f</sub> = 0.80 是宽带 TDMA 的答案。</li>
<li>频率因子单位统一：30 kHz 和 12.5 MHz = 12,500 kHz。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>This is a narrowband TDMA system, so ηa = (Ts·Mt/Tf)(Bu·Nu/Bw). The useful slot duration is Ts = (13/16.2) × (40/6) = 5.35 ms, with Tf = 40 ms, Mt = 6, Bu = 30 kHz, Nu = 395 and Bw = 12.5 MHz. Hence ηa = (5.35 × 6/40) × (30 × 395/12500) = 0.8025 × 0.948 ≈ 0.76.</p></div>
<div class="ans">一句话：窄带 TDMA 的 η<sub>a</sub> = 时间因子（13/16.2 = 0.80）× 频率因子（395 × 30/12500 = 0.948）≈ 0.76。</div>
'''},

# ---------------------------------------------------------------- p.65
'p65': {'title': '知识讲解 + 详细解析：CCIR 模型的标准线与修正', 'zh': '''
<h4><span class="st">知识讲解</span>经验路径损耗模型：先画一条标准线，再逐项修正</h4>
<p>真实城市里信号被楼房反射、遮挡，理论公式算不准，只能用实测数据拟合出<b>经验模型</b>（empirical path loss model），讲义 Part A p.55–64。核心关系（p.59，全部用 dB）：</p>
<p><b>P<sub>R</sub> = P<sub>T</sub> + G<sub>T</sub> + G<sub>R</sub> − L</b>，L 是路径损耗。</p>
<p>讲义先规定一组<b>标准条件</b>（p.58–59）：f = 900 MHz，P<sub>T</sub> = 10 W（= 40 dBm），G<sub>T</sub> = 6 dBd，G<sub>R</sub> = 0 dBd，h<sub>T</sub> = 30 m，h<sub>R</sub> = 3 m。在标准条件下，接收功率对 log d 是一条直线：</p>
<p><b>P<sub>R</sub> = P<sub>0</sub> + γ log<sub>10</sub>d</b>（d 用 km），P<sub>0</sub> 是 d = 1 km 处的截距，γ 是斜率（= −10n）。p.60 的表给出 CCIR 城区：P<sub>0</sub> = −71.04 dBm，γ = −35.4。</p>
<p>条件和标准不同时，按 p.62–64 的修正表加减。每一项修正都来自 p.55 的 CCIR 公式 L = 69 + 26 log f − 14 log h<sub>T</sub> + (45 − 6.5 log h<sub>T</sub>) log d − A(h<sub>R</sub>)，因为 P<sub>R</sub> 里是 "−L"，所以符号要反过来：</p>
<div class="tw"><table class="mini"><thead><tr><th>参数</th><th>L 里的项</th><th>对 P<sub>R</sub> 的修正</th></tr></thead><tbody>
<tr><td>P<sub>T</sub></td><td>—</td><td>10 log(P<sub>T</sub>′/10 W)</td></tr>
<tr><td>h<sub>T</sub>（截距）</td><td>−14 log h<sub>T</sub></td><td>+14 log(h<sub>T</sub>′/30)</td></tr>
<tr><td>h<sub>T</sub>（斜率）</td><td>−6.5 log h<sub>T</sub> × log d</td><td>+6.5 log(h<sub>T</sub>′/30) × log d</td></tr>
<tr><td>h<sub>R</sub></td><td>−(log f − 0.7)h<sub>R</sub></td><td>+(log 900 − 0.7)(h<sub>R</sub>′ − 3) = 2.25(h<sub>R</sub>′ − 3)</td></tr>
<tr><td>G<sub>T</sub>、G<sub>R</sub></td><td>—</td><td>(G<sub>T</sub>′ − 6) + (G<sub>R</sub>′ − 0)，单位 dBd</td></tr>
</tbody></table></div>
<p>注意 h<sub>R</sub> 的修正是<b>线性</b>的（直接乘高度差），h<sub>T</sub> 的修正是<b>对数</b>的（log 高度比）。天线增益用 dBd（相对半波偶极子），0 dBd = 2.14 dBi；题目和标准都用 dBd，直接相减即可。</p>
<h4><span class="st">详细解析</span>五项修正逐个算</h4>
<ol>
<li><b>标准线</b>：d = 2 km，log<sub>10</sub>2 = 0.301。−71.04 − 35.4 × 0.301。</li>
<li><b>发射功率</b>：5 W 比 10 W 少一半，10 log 0.5 = −3.01 dB。</li>
<li><b>基站高度（截距）</b>：25 m 比 30 m 低，log(25/30) = log 0.8333 = −0.0792，乘 14。</li>
<li><b>基站高度（斜率）</b>：同一个 −0.0792，乘 6.5，<b>还要乘 log d = 0.301</b>，因为它改的是直线的斜率。</li>
<li><b>终端高度</b>：2 m 比 3 m 低 1 m，乘 2.25。</li>
<li><b>天线增益</b>：G<sub>T</sub> 10 dBd 比标准 6 dBd 多 4 dB；G<sub>R</sub> 不变。</li>
<li><b>全部相加</b>。</li>
</ol>
<div class="calc">标准线：−71.04 − 35.4 × 0.301 = −71.04 − 10.66 = −81.70 dBm<br>P<sub>T</sub>：10 log(5/10) = −3.01 dB<br>h<sub>T</sub> 截距：14 × log(25/30) = 14 × (−0.0792) = −1.11 dB<br>h<sub>T</sub> 斜率：6.5 × (−0.0792) × 0.301 = −0.15 dB<br>h<sub>R</sub>：2.25 × (2 − 3) = −2.25 dB<br>增益：(10 − 6) + (0 − 0) = +4 dB<br>P<sub>R</sub> = −81.70 − 3.01 − 1.11 − 0.15 − 2.25 + 4 = −84.22 dBm</div>
<p><b>合理性检查</b>：功率减半、两根天线都更低，所以比标准线（−81.70 dBm）弱；发射天线增益多 4 dB 抵掉一部分。净变化 −2.52 dB，方向对。换成瓦：10<sup>−84.22/10</sup> mW ≈ 3.8 × 10⁻⁹ mW = 3.8 pW，手机接收功率在这个量级是正常的。</p>
<p>计算器提示：log 0.8333 直接按；10 log(5/10) 记住"减半 = −3 dB"。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>功率修正用比值 P<sub>T</sub>′/10 W，不要写 10 log 5 = 7 dB。</li>
<li>基站高度有<b>两项</b>修正，斜率那项要乘 log d，漏掉就差 0.15 dB。</li>
<li>h<sub>R</sub> 修正不取对数；增益差直接用 dBd 相减，不要再加 2.14。</li>
<li>d 必须用 km，log 是以 10 为底。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Under the standard conditions (PT = 10 W, GT = 6 dBd, GR = 0 dBd, hT = 30 m, hR = 3 m, f = 900 MHz), the CCIR urban model gives PR = P0 + γ log d with P0 = −71.04 dBm and γ = −35.4. At d = 2 km: PR = −71.04 − 35.4 log 2 = −81.70 dBm. Corrections: transmit power 10 log(5/10) = −3.01 dB; BS height (intercept) 14 log(25/30) = −1.11 dB; BS height (slope) 6.5 log(25/30) log 2 = −0.15 dB; MS height 2.25(2 − 3) = −2.25 dB; antenna gain (10 − 6) + (0 − 0) = +4 dB. Therefore PR = −81.70 − 3.01 − 1.11 − 0.15 − 2.25 + 4 = −84.22 dBm.</p></div>
<div class="ans">一句话：先在标准线上读出 −81.70 dBm，再加五项修正（功率比、基站高度两项、终端高度、增益差），得 −84.22 dBm。</div>
'''},

# ---------------------------------------------------------------- p.82
'p82': {'title': '知识讲解 + 详细解析：FDD 双工信道数', 'zh': '''
<h4><span class="st">知识讲解</span>单工、双工与 FDD</h4>
<p>打电话是双向的：你说话走<b>上行</b>（uplink，手机 → 基站），听对方走<b>下行</b>（downlink，基站 → 手机）。</p>
<ul>
<li><b>单工信道</b>（simplex channel）：只管一个方向，本题每条占 25 kHz。</li>
<li><b>双工信道</b>（duplex channel）：一条上行 + 一条下行配成一对，才能完成一次通话。</li>
<li><b>FDD</b>（Frequency Division Duplex，讲义 Part A p.37）：上行和下行用两段<b>分开的频带</b>，各占一半带宽。TDD 则是同一频带按时间轮流上下行。</li>
</ul>
<p><b>均匀固定信道分配</b>（UFCA，uniform fixed channel assignment，p.81、p.92）：一簇 N 个小区平分全部信道，每个小区 S/N 条。<b>控制信道</b>负责呼叫建立和寻呼，不能拿来通话，所以要先把它们的带宽扣掉。</p>
<h4><span class="st">详细解析</span>四步：减控制 → 对半分 → 除信道宽 → 除 N</h4>
<ol>
<li><b>减控制</b>：30 MHz 中有 2 MHz 给控制信道，剩 28 MHz 给语音。</li>
<li><b>对半分</b>：FDD 上下行各一半，每个方向 14 MHz。</li>
<li><b>除信道宽</b>：每个方向能放多少条 25 kHz 的单工信道。</li>
<li><b>配对</b>：上行第 k 条和下行第 k 条组成第 k 个双工信道，所以双工信道数 = 一个方向的单工信道数。</li>
<li><b>除 N</b>：UFCA 下 7 个小区平分。</li>
</ol>
<div class="calc">语音带宽 = 30 − 2 = 28 MHz<br>每个方向 = 28 ÷ 2 = 14 MHz<br>单工信道/方向 = 14000 kHz ÷ 25 kHz = 560<br>双工信道（系统）= 560<br>每小区 = 560 ÷ 7 = 80</div>
<p><b>为什么要对半分</b>：每一通电话同时需要一条上行和一条下行，所以上下行的信道数必须一样多；FDD 把语音带宽平均切成上行频带和下行频带（讲义 p.82 原文 "assume each link has 14 MHz"）。如果是 TDD，就不分频带，而是同一频带按时隙轮流上下行（p.37）。</p>
<p><b>验算</b>（另一种算法）：一个双工信道总共占 2 × 25 = 50 kHz，28000 ÷ 50 = 560，结果相同。</p>
<p><b>变式</b>（讲义没问）：如果问控制信道数，同样做法 2000 kHz ÷ 50 kHz = 40 个双工控制信道，平均每小区 40 ÷ 7 ≈ 5.7 个（实际分配时有的小区 6 个、有的 5 个）。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>写成 28000 ÷ 25 = 1120 个双工信道是错的：1120 是上下行加起来的<b>单工</b>信道总数，两条才配一个双工。</li>
<li>先减控制再对半分；顺序反过来（30 ÷ 2 − 2）会得到 13 MHz/方向，错。</li>
<li>单位统一成 kHz 再除。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Bandwidth for voice = 30 − 2 = 28 MHz. In FDD, each link (uplink and downlink) has 28/2 = 14 MHz. Number of simplex voice channels per link = 14 000 kHz / 25 kHz = 560. Since each duplex voice channel needs one simplex channel in each link, the system has 560 duplex voice channels. With UFCA and N = 7, each cell has 560/7 = 80 duplex voice channels.</p></div>
<div class="ans">一句话：减控制 → 对半分 → 除 25 kHz → 一对单工 = 一个双工 → 除 7，得系统 560、每小区 80。</div>
'''},

# ---------------------------------------------------------------- p.89
'p89': {'title': '知识讲解 + 详细解析：用 SIR 选簇尺寸 N', 'zh': '''
<h4><span class="st">知识讲解</span>同频干扰、复用比 Q 与簇尺寸 N</h4>
<p><b>频率复用</b>：同一组频率每隔一个簇就重复使用一次。两个使用同一频率的小区中心相距 <b>D</b>（复用距离，reuse distance），讲义 Part A p.78：D = R√(3N)，<b>Q = D/R = √(3N)</b> 叫复用比。</p>
<p>N 只能取 i² + ij + j²（i、j 为非负整数，p.75）这样的值：1, 3, 4, 7, 9, 12, 13 …，因为六边形必须能无缝拼成簇。</p>
<p><b>SIR</b>（signal-to-interference ratio，p.83–84）：S/I = S / ΣI<sub>i</sub>。只考虑路径损耗时，接收功率 ∝ 距离<sup>−n</sup>，n 是路径损耗指数。</p>
<p><b>简化假设</b>（p.88）：只算第一层 6 个同频干扰小区；手机在小区边缘，到自己基站距离 R；6 个干扰基站都按距离 D 算。于是</p>
<p><b>S/I = R<sup>−n</sup> / (6 D<sup>−n</sup>) = Q<sup>n</sup>/6 = (√(3N))<sup>n</sup>/6</b></p>
<p>n = 4 时根号正好消掉：S/I = (3N)²/6。<b>取舍</b>（p.78）：N 大 → D 远 → SIR 好，但每个小区分到的信道少（S/N），容量低；N 小则相反。所以要找"刚好够用"的 N。</p>
<h4><span class="st">详细解析</span>两种做法：列表试 N，或者反解</h4>
<p><b>做法一：逐个代入</b>（讲义 p.89 的做法）。</p>
<div class="tw"><table class="mini"><thead><tr><th>N</th><th>Q = √(3N)</th><th>(3N)²/6</th><th>SIR (dB)</th></tr></thead><tbody>
<tr><td>1</td><td>1.732</td><td>1.5</td><td>1.76</td></tr>
<tr><td>3</td><td>3.000</td><td>13.5</td><td>11.30</td></tr>
<tr><td>4</td><td>3.464</td><td>24</td><td>13.80</td></tr>
<tr><td>7</td><td>4.583</td><td>73.5</td><td>18.66</td></tr>
<tr><td>9</td><td>5.196</td><td>121.5</td><td>20.85</td></tr>
<tr><td>12</td><td>6.000</td><td>216</td><td>23.34</td></tr>
<tr><td>13</td><td>6.245</td><td>253.5</td><td>24.04</td></tr>
</tbody></table></div>
<p>以 N = 7 为例：3 × 7 = 21，21² = 441，441 ÷ 6 = 73.5，10 log<sub>10</sub>73.5 = 18.66 dB。</p>
<p><b>做法二：反解</b>（更快，考场推荐）。先把 dB 换成线性值，再解 N，最后往上取到最近的合法 N。</p>
<div class="calc">10 dB → 10<sup>10/10</sup> = 10<br>(3N)²/6 ≥ 10 → 3N ≥ √60 = 7.746 → N ≥ 2.58 → 合法 N = 3<br>18 dB → 10<sup>1.8</sup> = 63.1<br>(3N)²/6 ≥ 63.1 → 3N ≥ 19.46 → N ≥ 6.49 → 合法 N = 7</div>
<p><b>合理性检查</b>：n = 4 时 S/I ∝ N²，所以 N 变成 4 倍，SIR 增加 10 log 16 = 12.04 dB。表里 N = 3 → 12：11.30 → 23.34 dB，正好差 12.04 dB；N 越大 SIR 越高，方向也对。</p>
<p><b>为什么有两个答案</b>：题目说 SIR 要求 10 dB，满足它的最小 N 是 3，讲义称为 required cluster size。但讲义接着说语音质量要 SIR 大于 18 dB（AMPS 的经验要求），所以 optimum cluster size 取 7。考试把两个都写出来并说明理由。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>N = 5、6、8 不是合法簇尺寸，反解出 6.49 要取 7，不是 6.5 或 6。</li>
<li>比较前先统一单位：要么都用 dB，要么都用线性值。</li>
<li>n = 4 时 Q⁴ = (3N)²，不用再开根号。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>With the simple assumptions (six first-tier co-channel interferers, all at distance D, mobile at the cell edge), S/I = Q<sup>n</sup>/6 with Q = √(3N). For n = 4, S/I = (3N)²/6. For N = 1, 3, 4, 7, 9, 12, 13 this gives 1.76, 11.30, 13.80, 18.66, 20.85, 23.34 and 24.04 dB. N ≥ 3 gives SIR above 10 dB, so the required cluster size is N = 3. For sufficient voice quality the SIR should exceed 18 dB, so the optimum cluster size is N = 7 (S/I = 73.5 = 18.66 dB).</p></div>
<div class="ans">一句话：n = 4 时 S/I = (3N)²/6；10 dB 要求的最小 N = 3，满足 18 dB 语音质量的最优 N = 7。</div>
'''},

# ---------------------------------------------------------------- p.91
'p91': {'title': '知识讲解 + 详细解析：最坏情况 SIR 两种算法', 'zh': '''
<h4><span class="st">知识讲解</span>为什么要算"最坏情况"</h4>
<p>p.88 的简化算法假设 6 个干扰基站都离手机 D。可手机站在小区边缘时，它离某些干扰小区更近、离另一些更远。讲义 Part A p.90–91 用两种更悲观的近似：</p>
<ul>
<li><b>情况 1</b>：6 个干扰源分成三组，2 个在 D − R，2 个在 D，2 个在 D + R。<br>S/I = R<sup>−n</sup> / [2(D−R)<sup>−n</sup> + 2D<sup>−n</sup> + 2(D+R)<sup>−n</sup>] = 1 / [2(Q−1)<sup>−n</sup> + 2Q<sup>−n</sup> + 2(Q+1)<sup>−n</sup>]</li>
<li><b>情况 2</b>（保守，conservative）：6 个全按最近距离 D − R 算。<br>S/I = 1 / [6(Q−1)<sup>−n</sup>] = (Q−1)<sup>n</sup>/6</li>
</ul>
<p>第二个等号的来历：分子分母同除以 R<sup>−n</sup>，D/R 就变成 Q。所以只要知道 Q = √(3N) 和 n 就能算。</p>
<p><b>要点</b>：干扰功率 ∝ 距离<sup>−n</sup>，n = 4 时距离近一点，干扰就大很多（距离 × 0.78，干扰 × 2.7）。所以最近的那两个干扰源贡献了大部分干扰。</p>
<h4><span class="st">详细解析</span>先把四次方算好，再代入</h4>
<ol>
<li><b>求 Q</b>：N = 7，Q = √21 = 4.5826（四次方会放大误差，中间多留几位小数）。</li>
<li><b>三个距离的四次方</b>（计算器提示：x⁴ = (x²)²）。</li>
<li><b>情况 1</b>：把三组干扰相加（每组系数 2），再取倒数。</li>
<li><b>情况 2</b>：直接 (Q−1)⁴ ÷ 6。</li>
<li><b>换 dB</b>：10 log<sub>10</sub>。</li>
</ol>
<div class="calc">Q − 1 = 3.5826：3.5826² = 12.835，12.835² = 164.7<br>Q⁴ = 21² = 441<br>Q + 1 = 5.5826：5.5826² = 31.165，31.165² = 971.3<br>情况 1：2/164.7 + 2/441 + 2/971.3 = 0.01214 + 0.00454 + 0.00206 = 0.01874<br>S/I = 1 ÷ 0.01874 = 53.4 → 10 log 53.4 = 17.27 dB<br>情况 2：S/I = 164.7 ÷ 6 = 27.5 → 10 log 27.5 = 14.39 dB</div>
<p>（解法里写的 164.9、971.8 是四舍五入带来的小差别，最后的 dB 值不变。）</p>
<p><b>三种口径对比</b>：越悲观 SIR 越低。</p>
<div class="tw"><table class="mini"><thead><tr><th>假设</th><th>S/I</th><th>dB</th></tr></thead><tbody>
<tr><td>6 个都在 D（p.88–89）</td><td>73.5</td><td>18.66</td></tr>
<tr><td>2 + 2 + 2（情况 1）</td><td>53.4</td><td>17.27</td></tr>
<tr><td>6 个都在 D − R（情况 2）</td><td>27.5</td><td>14.39</td></tr>
</tbody></table></div>
<p><b>意义</b>：按最坏情况算，N = 7 的 SIR 低于 18 dB 的语音要求。解决办法要么加大 N，要么用<b>扇区化</b>（p.143–145）减少干扰源，这就是后面 p.145 例题的动机。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>情况 2 分母仍然有 6（6 个干扰源），只是距离都换成 D − R。</li>
<li>情况 1 不是三个干扰源，是三组、每组 2 个，每项前面系数 2。</li>
<li>先相加再取倒数，不能把三项的 dB 值相加。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>For N = 7, Q = √(3N) = √21 = 4.583. Case 1: S/I = 1/[2(Q−1)⁻⁴ + 2Q⁻⁴ + 2(Q+1)⁻⁴] = 1/[2/164.7 + 2/441 + 2/971.3] = 1/0.01874 = 53.4, i.e. 17.27 dB. Case 2 (all six interferers at D − R): S/I = (Q−1)⁴/6 = 164.7/6 = 27.5, i.e. 14.39 dB. Both are lower than the 18.66 dB obtained with the simple equidistant assumption.</p></div>
<div class="ans">一句话：N = 7、n = 4 时，2+2+2 分组得 17.27 dB，全按 D − R 得 14.39 dB，都比简化算法的 18.66 dB 低。</div>
'''},

# ---------------------------------------------------------------- p.93
'p93': {'title': '知识讲解 + 详细解析：固定信道分配 FCA', 'zh': '''
<h4><span class="st">知识讲解</span>信道怎么分给每个小区：固定分配 vs 动态分配</h4>
<p>频谱有限，用户很多，所以要设计<b>信道分配</b>（channel assignment）方法，讲义 Part A p.92–95。</p>
<ul>
<li><b>固定信道分配 FCA</b>（fixed channel assignment）：事先给每个小区（基站）一组固定的信道。小区里的呼叫只能用本小区的空闲信道；全部占满就阻塞（blocked）。</li>
<li><b>均匀 FCA（UFCA）</b>：一簇里每个小区分到一样多的信道，每小区 = 总信道数 S ÷ N（p.81）。</li>
<li><b>非均匀 FCA</b>：按各小区的话务量多少分，忙的多分。</li>
<li><b>动态分配 DCA</b>（dynamic，p.95）：信道不永久归某个小区，来一个呼叫就按规则挑一条可用信道，只要不违反同频干扰约束。<b>信道借用</b>（channel borrowing）是 DCA 的一种：忙的小区向邻区借，通话结束要还回去。</li>
</ul>
<p><b>FCA 的问题</b>（p.94）：本小区信道用完了，即使隔壁小区有空闲信道，新呼叫也只能被拒绝。老师课上强调：固定分配简单但不灵活；借来的信道用完要还，借用时仍要满足复用距离，不能造成同频干扰。</p>
<p>p.81 还给出全区信道总数 T = C × N × (S/N) = C × S，C 是簇的个数：每个簇都把 S 条信道全部用一遍。</p>
<h4><span class="st">详细解析</span>两步：平分，再留控制信道</h4>
<ol>
<li><b>确认 N</b>：题目没写簇尺寸，讲义解法默认 7 小区复用。考试时先写一句"Assume N = 7"，把假设说清楚。</li>
<li><b>平分</b>：UFCA 下每个小区分到 1/7。</li>
<li><b>扣控制信道</b>：每个小区通常留 1 条做控制信道（呼叫建立、寻呼），剩下的才能通话。</li>
</ol>
<div class="calc">每小区信道数 = 210 ÷ 7 = 30 条<br>可用于通话 = 30 − 1 = 29 条</div>
<p><b>为什么要留控制信道</b>：手机开机后要先在控制信道上登记、收寻呼、发起呼叫请求，基站再给它分一条语音信道。没有控制信道，语音信道再多也没法接通电话。所以每个小区至少留 1 条。</p>
<p><b>检查</b>：30 × 7 = 210，刚好分完，没有余数。如果是 N = 4 或 N = 12，就会是 210 ÷ 4 = 52.5、210 ÷ 12 = 17.5，不整除，要说明怎么取整（这也说明讲义选 7 是配好的）。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>只写 30 不写 29，会漏掉"控制信道"这一分。</li>
<li>不要把 210 当成每小区信道数，210 是一簇（系统）总数。</li>
<li>题目没给 N 时要写出假设。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Assume a 7-cell reuse pattern (N = 7). With uniform fixed channel assignment, each cell in a cluster is allocated 1/7 of the total system channels: 210/7 = 30 channels per cell. Usually one channel in each cell is used as a control channel, leaving 30 − 1 = 29 channels for voice traffic.</p></div>
<div class="ans">一句话：UFCA 每小区 = 总数 ÷ N = 210 ÷ 7 = 30 条，留 1 条控制，29 条通话。</div>
'''},

# ---------------------------------------------------------------- p.121–122
'p121': {'title': '知识讲解 + 详细解析：Erlang、用户数与干线增益', 'zh': '''
<h4><span class="st">知识讲解</span>Erlang、Erlang B 与干线增益</h4>
<p><b>话务量 A</b>（traffic，单位 Erlang），讲义 Part A p.118：A = λ/μ = λ × h。λ 是平均呼叫到达率（次/小时），1/μ = h 是平均通话时长（小时）。直观意思：<b>平均有多少条信道同时在忙</b>。1 Erlang = 一条信道连续忙一小时。</p>
<p><b>呼损制（blocked model）</b>（p.118–119）：信道全忙时新呼叫直接被拒绝，不排队，用 M/M/m/m 模型和 <b>Erlang B 公式</b>算阻塞概率 P<sub>B</sub>，P<sub>B</sub> 就是服务等级 GoS（p.116：1%–2% 很好，超过 5% 用户不能接受）。考试查表：已知 M 和 GoS，读出最大 A。</p>
<p><b>承载话务量</b>（carried traffic，p.120）：C = A(1 − P<sub>B</sub>)，被拒绝的部分是 A·P<sub>B</sub>。P<sub>B</sub> 小时 C ≈ A。</p>
<p><b>干线增益</b>（trunking gain，p.122）= 一组信道在给定 GoS 下能服务的用户数 ÷ 信道数，即"一条信道平均养活几个用户"。用户远多于信道，是因为大家不会同时打电话。p.122 两条规律：<b>GoS 固定时 M 越大，增益越大；M 固定时 GoS 放宽（数值变大），增益越大</b>。</p>
<h4><span class="st">详细解析</span>三步：每人话务量 → 用户数 → 增益</h4>
<ol>
<li><b>每用户话务量</b>：取忙时上限 1.2 次/小时，通话 100 s = 100/3600 小时。</li>
<li><b>查表</b>：M = 50、P<sub>B</sub> = 2% → A = 40.3 Er（讲义已给）。</li>
<li><b>用户数</b> = 小区能承载的总话务 ÷ 每人话务。A<sub>u</sub> 精确值是 1/30，除以 1/30 就是乘 30。</li>
<li><b>干线增益</b> = 用户数 ÷ 信道数。</li>
</ol>
<div class="calc">A<sub>u</sub> = 1.2 × 100/3600 = 0.0333 Er（= 1/30）<br>用户数 = 40.3 ÷ (1/30) = 40.3 × 30 = 1209 ≈ 1210<br>干线增益 = 1209 ÷ 50 = 24.2<br>承载话务 C = 40.3 × (1 − 0.02) = 39.5 Er</div>
<p>注意：如果把 A<sub>u</sub> 先四舍五入成 0.033 再除，40.3 ÷ 0.033 = 1221，和讲义的 1210 对不上。讲义的 1210 是用精确的 1/30 算的，考试写"40.3 × 30 = 1209 ≈ 1210"最稳。</p>
<p><b>用讲义的六个表值验证 p.122 的两条规律</b>（用户数 = A × 30，增益 = 用户数 ÷ M）：</p>
<div class="tw"><table class="mini"><thead><tr><th>GoS</th><th>M = 10</th><th>M = 20</th><th>M = 50</th></tr></thead><tbody>
<tr><td>2%</td><td>5.08 Er → 152 人 → 15.2</td><td>13.2 Er → 396 人 → 19.8</td><td>40.3 Er → 1209 人 → 24.2</td></tr>
<tr><td>5%</td><td>6.2 Er → 186 人 → 18.6</td><td>15.2 Er → 456 人 → 22.8</td><td>44.3 Er → 1329 人 → 26.6</td></tr>
</tbody></table></div>
<p>每一行从左到右增大（M 越大越划算），每一列从上到下增大（GoS 越宽松越多人）。（用公式精确算 M = 50、5% 是 44.53 Er，讲义写 44.3，不影响结论。）</p>
<p><b>变式</b>：如果取忙时下限 0.4 次/小时，A<sub>u</sub> = 0.4 × 100/3600 = 1/90 Er，同一个小区能服务 40.3 × 90 = 3627 人。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>h 的单位换成小时：100 s ÷ 3600。</li>
<li>干线增益是"用户数 ÷ 信道数"，不是"话务量 ÷ 信道数"（后者是干线效率，见 p.123）。</li>
<li>查 Erlang B 表时看准 GoS 列，2% 和 5% 差别不小。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Offered traffic per user Au = λ/μ = 1.2 × 100/3600 = 0.0333 Erlang. A cell with M = 50 channels at PB = 2% can carry A = 40.3 Erlangs (Erlang B table), so it can support 40.3/0.0333 ≈ 1210 subscribers during the busy hour. Trunking gain = number of users served / number of channels = 1210/50 ≈ 24.2 at a GoS of 2%. The trunking gain increases with M for a fixed GoS, and increases as the GoS value increases for a fixed M.</p></div>
<div class="ans">一句话：A<sub>u</sub> = 1.2 × 100/3600 = 1/30 Er，50 条信道 2% 下承载 40.3 Er，可服务约 1210 人，干线增益 24.2。</div>
'''},

# ---------------------------------------------------------------- p.123–124
'p123': {'title': '知识讲解 + 详细解析：干线效率，大池子为什么更划算', 'zh': '''
<h4><span class="st">知识讲解</span>干线效率（trunking efficiency）</h4>
<p>讲义 Part A p.124 定义：<b>干线效率 = 在指定 GoS 下每条信道承载的话务量（Erlang/信道）</b>，在 0 和 1 之间。它和 p.42 的 η<sub>t</sub> = 话务量 ÷ 信道数是同一个意思。</p>
<p><b>为什么信道合在一起更划算</b>：呼叫是随机到达的。两个小组分开时，可能 A 组 5 条全忙、新呼叫被拒，同时 B 组还有空闲信道却用不上。合成一个 10 条的大组后，任何空闲信道都能接任何呼叫，"忙闲互补"。为了保持同样的阻塞率 1%，小组必须留更多余量，所以平均利用率低。这叫<b>集群效应</b>（trunking），像银行一条队对多个窗口，比每个窗口各排一队效率高。</p>
<p>代价是什么：把信道分成两组通常是因为分给了两个扇区或两个小区，每组面对的同频干扰更少，<b>SIR 可能更好</b>（p.123 原文最后一句）。这正是后面扇区化（p.145、p.148）的取舍。</p>
<h4><span class="st">详细解析</span>查表 → 求效率 → 比较</h4>
<ol>
<li><b>一组 10 条</b>：Erlang B 表 M = 10、GoS = 0.01 → A = 4.46 Er。</li>
<li><b>两组各 5 条</b>：M = 5、GoS = 0.01 → 每组 1.36 Er，两组共 2 × 1.36。</li>
<li><b>干线效率</b>：都除以总信道数 10。</li>
<li><b>比较</b>：用大的除以小的，减 1 就是"多出百分之几"。</li>
</ol>
<div class="calc">一组：A = 4.46 Er，效率 = 4.46 ÷ 10 = 0.446 = 44.6%<br>两组：A = 2 × 1.36 = 2.72 Er，效率 = 2.72 ÷ (2 × 5) = 0.272 = 27.2%<br>比值 = 4.46 ÷ 2.72 = 1.64 → 多承载 64%（讲义写"60%"，是取整的说法）</div>
<p>（公式精确值：M = 10 为 4.461，M = 5 为 1.361，表值正确。）</p>
<p><b>反过来说</b>：拆成两组后承载量少了 (4.46 − 2.72) ÷ 4.46 = 39%。考试题如果问"多多少"，以小的为基准（64%，约 60%）；问"少多少"，以大的为基准（39%）。基准别弄反。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>两组的话务量要乘 2，效率的分母是总共 10 条信道。</li>
<li>评述要两面写：容量（干线效率）下降，但 SIR 可能更好。只写容量不完整。</li>
<li>查表时 GoS 是 0.01（1%），不是 2%。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>From the Erlang B table at GoS = 0.01, 10 trunked channels support 4.46 Erlangs, while two groups of 5 channels support 2 × 1.36 = 2.72 Erlangs. Trunking efficiency (carried Erlangs per channel) is 4.46/10 = 0.446 (44.6%) for one group and 2.72/10 = 0.272 (27.2%) for two groups. Hence one group of 10 channels carries about 60% more traffic (4.46/2.72 = 1.64) than two groups of 5 channels, because a larger trunk pool shares idle channels among all calls. However, splitting into two groups (e.g. two sectors) would probably give a better SIR.</p></div>
<div class="ans">一句话：同样 1% 阻塞，10 条合用承载 4.46 Er（44.6%），拆成 5 + 5 只有 2.72 Er（27.2%），合用多约 60%，代价是 SIR 不如分组。</div>
'''},

# ---------------------------------------------------------------- p.130–132
'p130': {'title': '知识讲解 + 详细解析：三家运营商的用户数与渗透率', 'zh': '''
<h4><span class="st">知识讲解</span>从"信道数"算到"市场渗透率"</h4>
<p>这道题把 Erlang B 用到运营商对比上（讲义 Part A p.130–132）。用到三个概念：</p>
<ul>
<li><b>每用户话务量</b> A<sub>u</sub> = 每小时呼叫次数 × 每次时长（小时），p.118。</li>
<li><b>每小区最大话务量</b> A：查 Erlang B 表（M = 每小区信道数，GoS = 2%），p.119–121。题目说"满负荷运行"（maximum capacity），就是每个小区都跑到 2% 阻塞时的 A。</li>
<li><b>市场渗透率</b>（market penetration）= 运营商能服务的用户数 ÷ 区域总人口。</li>
</ul>
<p>计算链：<b>查表得 A → 每小区用户 U = A/A<sub>u</sub> → 乘小区数得总用户 → 除以总人口</b>。</p>
<p>本题的深层道理是<b>干线效率</b>（p.123–124）：每小区信道越多，每条信道承载的话务越多。所以总信道数多不一定用户多，关键看信道是否集中。</p>
<h4><span class="st">详细解析</span>同一套三步，做三遍</h4>
<ol>
<li><b>A<sub>u</sub></b>：3 次/小时 × 5 分钟，5 分钟 = 5/60 小时。</li>
<li><b>查表</b>：GoS = 0.02，M = 20、60、100 分别读出 13、50、90 Erlang（讲义取的整数）。</li>
<li><b>每小区用户</b> = A ÷ 0.25，即 A × 4。</li>
<li><b>总用户</b> = 每小区用户 × 小区数。</li>
<li><b>渗透率</b> = 总用户 ÷ 1,200,000。</li>
</ol>
<div class="calc">A<sub>u</sub> = 3 × 5/60 = 0.25 Er<br>Singa：13 ÷ 0.25 = 52 人/小区，52 × 380 = 19,760 人，19,760 ÷ 1,200,000 = 1.65%<br>Mobi：50 ÷ 0.25 = 200 人/小区，200 × 100 = 20,000 人，1.67%<br>Hubba：90 ÷ 0.25 = 360 人/小区，360 × 60 = 21,600 人，1.80%<br>合计：61,360 ÷ 1,200,000 = 5.11%</div>
<p><b>为什么 Hubba 赢</b>：看每家的干线效率和"每条信道的用户数"。</p>
<div class="tw"><table class="mini"><thead><tr><th>运营商</th><th>总信道</th><th>干线效率 A/M</th><th>用户/信道</th></tr></thead><tbody>
<tr><td>Singa</td><td>380 × 20 = 7600</td><td>13/20 = 0.65</td><td>2.6</td></tr>
<tr><td>Mobi</td><td>100 × 60 = 6000</td><td>50/60 = 0.83</td><td>3.33</td></tr>
<tr><td>Hubba</td><td>60 × 100 = 6000</td><td>90/100 = 0.90</td><td>3.6</td></tr>
</tbody></table></div>
<p>Singa 信道最多，却因为每小区只有 20 条、干线效率只有 65%，用户反而最少。和 p.123"一大锅比两小锅强"是同一个道理。</p>
<p><b>精确值说明</b>：用 Erlang B 公式算，M = 20 为 13.18，M = 60 为 49.64，M = 100 为 87.97（讲义取 90）。按精确值 Hubba 是 87.97 × 4 × 60 = 21,113 人（1.76%），Mobi 19,858 人（1.65%），排名和结论不变。考试按表值写。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>5 分钟要除以 60 换成小时，写成 3 × 5 = 15 Er 就错了 60 倍。</li>
<li>渗透率分母是 120 万总人口，不是三家用户之和。</li>
<li>每家都要乘自己的小区数（380、100、60），别混。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Traffic per user Au = 3 × 5/60 = 0.25 Erlang. Singa: from the Erlang B table (GoS = 0.02, M = 20), A = 13 Erlangs, so U = A/Au = 52 users per cell and 52 × 380 = 19 760 users. Mobi: M = 60 gives A = 50 Erlangs, U = 200 users per cell, 200 × 100 = 20 000 users. Hubba: M = 100 gives A = 90 Erlangs, U = 360 users per cell, 360 × 60 = 21 600 users. Market penetration: Singa 19 760/1 200 000 = 1.65%, Mobi 1.67%, Hubba 1.80%; total 61 360/1 200 000 = 5.11%. Hubba supports the most users with the fewest cells because more channels per cell give a higher trunking efficiency.</p></div>
<div class="ans">一句话：A<sub>u</sub> = 0.25 Er，查表 → ÷ 0.25 → × 小区数 → ÷ 120 万，得 1.65%、1.67%、1.80%，合计 5.11%；信道越集中，干线效率越高。</div>
'''},

# ---------------------------------------------------------------- p.133–134
'p133': {'title': '知识讲解 + 详细解析：城市蜂窝系统规划七问', 'zh': '''
<h4><span class="st">知识讲解</span>一次完整的系统规划要算什么</h4>
<p>讲义 Part A p.133–134 把前面学的东西串成一条链：面积 → 小区数；频谱 → 每小区信道数；Erlang B → 每小区话务量；再到用户数。先搞清几个词：</p>
<ul>
<li><b>全双工信道带宽 60 kHz</b>（full duplex channel bandwidth）：已经包含上下行，一个双工信道就占 60 kHz，不用再乘 2（对比 p.82 给的是单工 25 kHz）。</li>
<li><b>每簇 40 MHz</b>：一簇 7 个小区共用这 40 MHz，所以每小区信道数 = 40 MHz ÷ (60 kHz × 7)。</li>
<li><b>唯一信道</b>（unique channel）：一簇里所有不同的信道，共 95 × 7 = 665 条。全区其他簇只是重复使用这 665 条。</li>
<li><b>理论最大同时服务数</b>：所有小区所有信道同时被占满时的通话数 = 每小区信道数 × 小区数。</li>
</ul>
<p>Erlang B 查表（p.119–121）：老师课上强调只查表，表里没有的信道数用线性插值（p.127）。</p>
<h4><span class="st">详细解析</span>七问一条链</h4>
<ol>
<li><b>小区数</b>：总面积 ÷ 每小区面积 = 31.3，按讲义取 31（整数个小区）。</li>
<li><b>每小区信道数</b>：40,000 kHz ÷ (60 × 7) = 95.2，向下取整 95。</li>
<li><b>每小区话务量</b>：Erlang B 表 M = 95、GoS = 0.02 → A = 84 Erlang/小区（讲义值）。</li>
<li><b>最大话务量</b>：31 个小区 × 84。</li>
<li><b>用户数</b>：总话务 ÷ 每用户 0.03 Er。</li>
<li><b>每个唯一信道的用户数</b>：用户数 ÷ 665。</li>
<li><b>理论最大同时服务数</b>：95 × 31，再和总用户数比。</li>
</ol>
<div class="calc">① 1300 ÷ 41.5 = 31.3 → 31 个小区<br>② 40000 ÷ (60 × 7) = 95.2 → 95 条/小区<br>③ A = 84 Er/小区<br>④ 31 × 84 = 2604 Er<br>⑤ 2604 ÷ 0.03 = 86,800 用户<br>⑥ 唯一信道 95 × 7 = 665；86,800 ÷ 665 = 130.5 ≈ 130 用户/信道<br>⑦ 95 × 31 = 2945；2945 ÷ 86,800 = 3.4%</div>
<p><b>验算⑥</b>：全区物理信道 2945 条，每条平均 86,800 ÷ 2945 = 29.47 人；每个唯一信道在全区被重复使用 31 ÷ 7 = 4.429 次，29.47 × 4.429 = 130.5，和⑥一致。</p>
<p><b>⑦ 的意义</b>：系统同一时刻最多只能让 3.4% 的用户通话，却能服务 86,800 人，因为每人平均只占 0.03 Er（忙时 3% 的时间在打电话）。</p>
<p><b>精确值说明</b>：Erlang B 公式算 M = 95、2% 是 83.1 Er（讲义取 84），按精确值用户数约 85,900。考试按表值写，或注明查表所得。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>60 kHz 已是全双工带宽，不要再乘 2。</li>
<li>"唯一信道"是一簇的 665 条，不是全区的 2945 条。</li>
<li>⑦ 是信道数 × 小区数，不是用户数。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(1) Number of cells = 1300/41.5 ≈ 31 cells. (2) Channels per cell M = 40 000 kHz/(60 kHz × 7) ≈ 95 channels. (3) From the Erlang B table (GoS = 0.02, M = 95), A = 84 Erlangs/cell. (4) Maximum traffic = 31 × 84 = 2604 Erlangs. (5) Number of users = 2604/0.03 = 86 800 users. (6) Number of unique channels = 95 × 7 = 665, so mobiles per unique channel = 86 800/665 ≈ 130. (7) Theoretical maximum number of users served at one time = 95 × 31 = 2945, which is about 3.4% of the subscribers.</p></div>
<div class="ans">一句话：面积比得 31 个小区，带宽比得 95 条信道，查表 84 Er，× 31 = 2604 Er，÷ 0.03 = 86,800 人，÷ 665 ≈ 130 人/信道，同时最多 2945 人通话（3.4%）。</div>
'''},

# ---------------------------------------------------------------- p.136
'p136': {'title': '知识讲解 + 详细解析：小区分裂要降多少功率', 'zh': '''
<h4><span class="st">知识讲解</span>小区分裂（cell splitting）</h4>
<p>话务增长到信道不够时，讲义 Part A p.135–139 给出两种扩容方法：小区分裂和扇区化。<b>小区分裂</b>：把一个拥挤的大小区拆成若干<b>微小区</b>（microcell），每个都有自己的基站，天线更低、功率更小。单位面积里的基站多了，信道就多了，容量上升。</p>
<p><b>为什么要降功率</b>：分裂后所有小区按比例缩小，D/R 不变，所以只要每个基站在自己小区边缘产生的接收功率和原来一样，SIR 就保持不变。如果微小区仍用原来的大功率，它会覆盖到更远处，干扰远处的同频小区。</p>
<p>接收功率 P<sub>r</sub> ∝ P<sub>t</sub> × 距离<sup>−n</sup>（n 是路径损耗指数）。在小区边缘，原小区距离 R，微小区距离 R/2。</p>
<p>p.138–139：<b>4:1 分裂</b>新半径是 R/2，<b>3:1 分裂</b>新半径是 R/√3；小区越小，切换越频繁（半径缩小 4 倍，每用户切换率约增加 10 倍）。</p>
<h4><span class="st">详细解析</span>令两种小区边缘的接收功率相等</h4>
<ol>
<li><b>列等式</b>：P<sub>t1</sub> R<sup>−n</sup> = P<sub>t2</sub> (R/2)<sup>−n</sup>。</li>
<li><b>化简</b>：(R/2)<sup>−n</sup> = 2<sup>n</sup> R<sup>−n</sup>，两边约掉 R<sup>−n</sup>，P<sub>t1</sub> = P<sub>t2</sub> × 2<sup>n</sup>，所以 P<sub>t2</sub> = P<sub>t1</sub>/2<sup>n</sup>。</li>
<li><b>代 n = 4</b>：2⁴ = 16。</li>
<li><b>换成 dB</b>：降低 10 log<sub>10</sub>16 dB。</li>
</ol>
<div class="calc">P<sub>t2</sub> = P<sub>t1</sub> / 2⁴ = P<sub>t1</sub> / 16<br>10 log<sub>10</sub>16 = 4 × 10 log<sub>10</sub>2 = 4 × 3.01 = 12.04 dB ≈ 12 dB</div>
<p><b>通用公式</b>：半径缩小为 R/k，功率降低 10n log<sub>10</sub>k dB。</p>
<div class="tw"><table class="mini"><thead><tr><th>分裂方式</th><th>n = 2</th><th>n = 3</th><th>n = 4</th></tr></thead><tbody>
<tr><td>4:1（R/2）</td><td>6.02 dB</td><td>9.03 dB</td><td>12.04 dB</td></tr>
<tr><td>3:1（R/√3）</td><td>4.77 dB</td><td>7.16 dB</td><td>9.54 dB</td></tr>
</tbody></table></div>
<p><b>为什么这样 SIR 就不变</b>：简化公式 S/I = Q<sup>n</sup>/6，Q = D/R（p.88）。所有小区一起缩小一半，D 和 R 同时减半，Q 不变；功率按 2<sup>n</sup> 降低后，有用信号和干扰按同样比例变小，比值不变。</p>
<p><b>代回检查</b>：微小区边缘 R/2 处收到 (P<sub>t1</sub>/16) × (R/2)<sup>−4</sup> = (P<sub>t1</sub>/16) × 16R<sup>−4</sup> = P<sub>t1</sub>R<sup>−4</sup>，和原小区边缘完全一样。</p>
<p><b>容量变化</b>：半径减半 → 每个小区面积变 1/4 → 同样面积里基站数 × 4 → 信道数 × 4（p.140–142 的例题就是这个结论）。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>是功率<b>降为</b> 1/16，即<b>降低</b> 12 dB，不是降低 1/16 dB 或 16 dB。</li>
<li>3:1 分裂的半径是 R/√3，结果是 9.54 dB，不能照搬 12 dB。</li>
<li>指数是 n，不是 2：n = 4 时 2⁴ = 16。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>To keep the same SIR, the received power at the boundary of the microcell must equal that at the boundary of the original cell: Pt1·R<sup>−n</sup> = Pt2·(R/2)<sup>−n</sup>. Hence Pt2 = Pt1/2<sup>n</sup>. For n = 4, Pt2 = Pt1/16, i.e. the transmit power of the microcell must be reduced by 10 log 16 = 12 dB. Since the cell area is reduced to 1/4, the number of channels per unit area (and hence capacity) increases about four times.</p></div>
<div class="ans">一句话：边缘接收功率相等 → P<sub>t2</sub> = P<sub>t1</sub>/2ⁿ，n = 4 时降为 1/16，即降低 12 dB。</div>
'''},

# ---------------------------------------------------------------- p.140–142
'p140': {'title': '知识讲解 + 详细解析：分裂前后 3km×3km 内的信道数', 'zh': '''
<h4><span class="st">知识讲解</span>区域内信道数 = 基站数 × 每站信道数</h4>
<p>讲义 Part A p.140–142 的例题：每个基站不管大小都固定 60 条信道。所以一块区域里有多少信道，只取决于这块区域里有<b>几个基站</b>。小区分裂（p.136）把半径缩小，基站密度增大，信道密度就增大。</p>
<p><b>面积与半径的关系</b>：小区面积 ∝ R²。半径变成 1/2，面积变成 1/4，同一块地要的小区数变成 4 倍。这就是"半径 ÷ 2 → 容量 × 4"的来源。</p>
<p>题目要在图上数小区（图在讲义 p.140），所以讲义说个数"只能估计"（can only be an estimate），因为正方形边上的小区只被切进去一部分。</p>
<h4><span class="st">详细解析</span>先定范围，再数小区，最后乘 60</h4>
<ol>
<li><b>定范围</b>：3 km × 3 km 正方形以 A 为中心，所以从 A 向上下左右各延伸 1.5 km。</li>
<li><b>(a) 不用微小区</b>：大小区半径 1 km，从图上数，正方形里大约有 4 个大小区（基站）。</li>
<li><b>(b) 用微小区</b>：微小区半径 0.5 km，面积是大小区的 1/4，所以最多 (R ÷ R/2)² × 4 = 4 × 4 = 16 个；从图上数约 15 个（边缘有些不完整）。</li>
<li><b>乘每站信道数</b> 60。</li>
</ol>
<div class="calc">(a) 4 × 60 = 240 条<br>(b) 最多 (1/0.5)² × 4 = 16 个微小区；按图估 15 个：15 × 60 = 900 条<br>增长倍数 900 ÷ 240 = 3.75 ≈ 4 倍（取 16 个则 16 × 60 = 960 条，正好 4 倍）</div>
<h4><span class="st">课外补充</span>用面积粗算核对（讲义没算）</h4>
<p>正六边形面积 = (3√3/2)R² ≈ 2.6R²。R = 1 km 时约 2.6 km²，正方形 9 km² 约能放 9 ÷ 2.6 = 3.5 个；R = 0.5 km 时约 0.65 km²，能放约 13.9 个。比例仍是 4 倍。讲义从图上数出 4 和 15，是把边上被切进去一部分的小区也算上了，所以略大，属正常估计。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>面积比是半径比的<b>平方</b>：半径 ÷ 2 → 小区数 × 4，不是 × 2。</li>
<li>每个基站 60 条信道"regardless of cell size"，微小区也是 60 条。</li>
<li>15 和 16 都可以，但要写清是估计，并说明结论"约 4 倍"。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>The 3 km × 3 km square extends 1.5 km above, below, left and right of base station A. (a) Without microcells: from the figure, about 4 large cells (base stations) lie within the square, so the number of channels is 4 × 60 = 240. (b) With microcells of half the radius, each cell area is reduced to 1/4, so there are at most (R/(R/2))² × 4 = 16 small cells; from the figure about 15. The number of channels is 15 × 60 = 900, which is about a four-fold increase.</p></div>
<div class="ans">一句话：信道数 = 基站数 × 60；半径减半，基站数约 × 4，所以 240 条变成约 900 条。</div>
'''},

# ---------------------------------------------------------------- p.144–145
'p145': {'title': '知识讲解 + 详细解析：扇区化后的 SIR 与容量', 'zh': '''
<h4><span class="st">知识讲解</span>扇区化（sectoring）：换一副"有方向的眼睛"</h4>
<p>全向天线（omni-directional）四面八方都收，第一层 6 个同频干扰小区全能"听到"。<b>扇区化</b>（讲义 Part A p.143–146）把一个小区分成几个扇区，每个扇区用一根<b>定向天线</b>，只朝一个方向收发：</p>
<ul>
<li><b>120° 扇区（3 扇区）</b>：每根天线只看到 6 个干扰源中的 <b>2 个</b>。</li>
<li><b>60° 扇区（6 扇区）</b>：只看到 <b>1 个</b>。</li>
</ul>
<p>最坏情况公式（p.145）：手机在扇区边缘，剩下的干扰源距离分别是 D 和 D + 0.7R（几何近似）。</p>
<p>3 扇区：S/I = 1 / [Q<sup>−n</sup> + (Q + 0.7)<sup>−n</sup>]；6 扇区：S/I = 1 / (Q + 0.7)<sup>−n</sup> = (Q + 0.7)<sup>n</sup>。</p>
<p><b>容量逻辑</b>（p.144）：SIR 变好以后，就可以用更小的簇尺寸 N 达到同样质量，复用更密，容量提高。讲义的说法：全向 N = 7 约 18 dB；120° 扇区化后的 SIR 和全向 N = 12 相当（简化公式下 N = 12 是 23.34 dB，见 p.89），所以本来需要 N = 12 的系统可以改用 N = 7，每小区信道数 × 12/7。</p>
<p><b>代价</b>：每个扇区只分到 1/3 或 1/6 的信道，干线效率下降（p.145、p.148），切换增多（p.146）。老师课上强调：扇区化提高 SIR，但每扇区信道变少，集群效率下降，这一点要会讲。</p>
<h4><span class="st">详细解析</span>算 Q 和 Q + 0.7 的四次方，再代入</h4>
<ol>
<li><b>Q</b> = √(3 × 7) = 4.583，Q⁴ = 21² = 441。</li>
<li><b>Q + 0.7</b> = 5.2826，四次方用 (x²)²，中间多留几位小数。</li>
<li><b>3 扇区</b>：两个干扰项相加，再取倒数。</li>
<li><b>6 扇区</b>：只剩一项，S/I 直接等于 (Q + 0.7)⁴。</li>
<li><b>容量倍数</b>：12/7。</li>
</ol>
<div class="calc">5.2826² = 27.906，27.906² = 778.7<br>3 扇区：1/441 + 1/778.7 = 0.002268 + 0.001284 = 0.003552<br>S/I = 1 ÷ 0.003552 = 281.6 → 10 log 281.6 = 24.5 dB<br>6 扇区：S/I = 778.7 → 10 log 778.7 = 28.9 dB<br>容量 × 12/7 = 1.714</div>
<div class="tw"><table class="mini"><thead><tr><th>N = 7，n = 4</th><th>干扰源数</th><th>SIR</th></tr></thead><tbody>
<tr><td>全向，简化（p.89）</td><td>6</td><td>18.66 dB</td></tr>
<tr><td>全向，最坏情况 1（p.91）</td><td>6</td><td>17.27 dB</td></tr>
<tr><td>120°，最坏（p.145）</td><td>2</td><td>24.5 dB</td></tr>
<tr><td>60°，最坏（p.145）</td><td>1</td><td>28.9 dB</td></tr>
</tbody></table></div>
<p>说明：p.144 文字写的是"SIR 约 23 dB"，p.145 按公式算是 24.5 dB。两者都比 18 dB 好很多，都和全向 N = 12 的 23.34 dB 同一水平。考试如果问 p.145 的公式，写 24.5 dB；复述 p.144 的结论时可以写"about 23–24.5 dB"。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>扇区化公式里没有"÷ 6"：有几个干扰源，分母就加几项（3 扇区 2 项，6 扇区 1 项）。</li>
<li>(Q + 0.7) 是 Q 加 0.7，不是 Q × 0.7。</li>
<li>只写"SIR 提高"不完整，要同时写干线效率下降、切换增多。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>For N = 7, Q = √21 = 4.583. With 120° sectoring only 2 of the 6 first-tier interferers remain. Worst case: S/I = 1/[Q⁻⁴ + (Q+0.7)⁻⁴] = 1/(1/441 + 1/778.7) = 281.6, i.e. 24.5 dB. With 60° sectoring only 1 interferer remains: S/I = (Q+0.7)⁴ = 778.7, i.e. 28.9 dB. Compared with about 18 dB for the omni-directional case, the SIR with 120° sectoring is comparable to that of a 12-cell cluster, so the cluster size can be reduced from 12 to 7 and the capacity increases by a factor of 12/7 ≈ 1.714. The drawbacks are lower trunking efficiency and more handoffs.</p></div>
<div class="ans">一句话：120° 扇区剩 2 个干扰源，S/I = 24.5 dB；60° 剩 1 个，28.9 dB；SIR 相当于全向 N = 12，容量约 × 12/7 = 1.714，代价是干线效率下降。</div>
'''},

# ---------------------------------------------------------------- p.148–149
'p148': {'title': '知识讲解 + 详细解析：扇区化后每小时呼叫数下降', 'zh': '''
<h4><span class="st">知识讲解</span>扇区化的另一面：干线效率下降</h4>
<p>p.145 讲了扇区化让 SIR 变好；这道题（讲义 Part A p.148–149）算它的代价。扇区化后，一个小区的 57 条信道被拆给 3 个或 6 个扇区，每个扇区只能用自己那一份。由 p.123 的道理，<b>几个小池子承载的总话务比一个大池子少</b>。</p>
<p>用到的换算：话务量 A = 每小时呼叫数 × h（h 用小时，p.118），所以 <b>每小时呼叫数 = A ÷ h</b>。h = 2 分钟 = 1/30 小时，所以每小时呼叫数 = A × 30。</p>
<p>每扇区的 A 用 Erlang B 表（GoS = 1%）查。表里没有的信道数用<b>线性插值</b>（讲义 p.127）：f(x) = f(x<sub>i</sub>) + (x − x<sub>i</sub>)/(x<sub>i+1</sub> − x<sub>i</sub>) × [f(x<sub>i+1</sub>) − f(x<sub>i</sub>)]。老师课上强调插值要会。</p>
<h4><span class="st">详细解析</span>三种情况逐个算</h4>
<ol>
<li><b>不分扇区</b>：M = 57，GoS = 1%，查表 A = 44.2 Er，乘 30。</li>
<li><b>120° 扇区</b>：每扇区 57 ÷ 3 = 19 条，查表 A = 11.2 Er，乘 30 得每扇区呼叫数，再 × 3 个扇区。</li>
<li><b>下降比例</b>：1 − 扇区化后 ÷ 扇区化前。</li>
<li><b>60° 扇区</b>：每扇区 57 ÷ 6 = 9.5 条，不是整数，讲义没写怎么算。用 M = 9（3.78 Er）和 M = 10（4.46 Er）插值取中点，再 × 6。</li>
</ol>
<div class="calc">不分扇区：44.2 × 30 = 1326 次/小时<br>120°：11.2 × 30 = 336 次/小时/扇区，× 3 = 1008 次/小时<br>下降：1 − 1008/1326 = 0.24 → 24%<br>60°：A(9.5) = 3.78 + 0.5 × (4.46 − 3.78) = 4.12 Er/扇区<br>6 × 4.12 = 24.72 Er → 24.72 × 30 = 741.6 ≈ 742 次/小时<br>下降：1 − 24.72/44.2 = 0.44 → 44%</div>
<p>（公式精确值：M = 57 为 44.22，M = 19 为 11.23，M = 9 为 3.78，M = 10 为 4.46，表值正确。）如果 60° 时按每扇区 9 条（向下取整）算：6 × 3.78 = 22.68 Er，下降 49%。讲义的 44% 对应插值的做法。</p>
<p><b>用干线效率看</b>：不分扇区 44.2/57 = 0.78；120° 33.6/57 = 0.59；60° 24.72/57 = 0.43。扇区越多，每条信道承载的话务越少。</p>
<p><b>用户数</b>：每用户每小时 1 次，所以每小时呼叫数就等于能服务的用户数：1326 人 → 1008 人。</p>
<p><b>SIR 方面</b>：p.149 说 60° 时 SIR 提高到约 29 dB（p.145 公式算 28.9 dB），第一层干扰源只剩 1 个；但切换次数增加。</p>
<h4><span class="st">易错</span></h4>
<ul>
<li>120° 要 × 3 个扇区再和 1326 比，不能拿 336 去比。</li>
<li>GoS 是 1%，查 0.01 那一列。</li>
<li>评述一定要两面写：SIR 升高，干线效率（容量）下降。</li>
</ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>With a 2-minute holding time, calls per hour = A × 60/2 = 30A. Unsectored: from the Erlang B table (M = 57, GoS = 1%), A = 44.2 Erlangs, i.e. 44.2 × 30 = 1326 calls/hour. 120° sectoring: each sector has 57/3 = 19 channels, A = 11.2 Erlangs, i.e. 336 calls/hour per sector and 3 × 336 = 1008 calls/hour per cell, a 24% decrease. 60° sectoring: each sector has 9.5 channels; by interpolation A ≈ 4.12 Erlangs per sector, 6 × 4.12 = 24.7 Erlangs (about 742 calls/hour), a decrease of about 44%. Sectoring improves the SIR but reduces trunking efficiency and increases the number of handoffs.</p></div>
<div class="ans">一句话：每小时呼叫数 = A × 30；不分扇区 1326，120° 只剩 1008（−24%），60° 约降 44%：SIR 升高，干线效率下降。</div>
'''},
}

NOTES = '''p121: existing solution writes "40.3 ÷ 0.033 ≈ 1210"; 40.3/0.033 is actually 1221. Slide's 1210 comes from the exact Au = 1/30 (40.3 × 30 = 1209). Explained in the box.
p123: 4.46/2.72 = 1.64, i.e. 64% more traffic; the slide (and existing solution) say "60%". Box gives 64% and says the slide rounds to about 60%.
p91: existing solution's intermediate values (Q−1)⁴ = 164.9 and (Q+1)⁴ = 971.8 are slightly off (exact 164.7 and 971.3); final 17.27 / 14.39 dB unchanged. Box uses the exact values and mentions the rounding.
p145: slide p.144 says 120° sectoring SIR "23 dB", p.145 computes 24.5 dB (existing solution uses 24.5). Box mentions both neutrally; 23 dB matches omni N = 12 (23.34 dB).
p148: slide p.149 says 60° SIR "29dB (compared to 27dB and 17dB)"; 27 dB matches nothing in the slides (120° worst case is 24.5 dB). Not used in the box.
p65: CCIR P0 = −71.04 dBm (slide p.60) could not be reproduced from the p.55 formula with the p.59 standard conditions (gives about −72.0 dBm with dBi gains); box uses the slide table value as the existing solution does.
p130: existing "记忆" line says Hubba has the fewest channels (6000), but Mobi also has 6000 (100 × 60). Minor wording.
p130/p133: Erlang B table values used by the slides (M = 100, 2%: 90 vs exact 87.97; M = 95, 2%: 84 vs exact 83.13) are rounded up; already noted in the existing solution.'''
