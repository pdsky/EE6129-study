# -*- coding: utf-8 -*-
# 知识讲解 + 详细解析 for EE6129 Part B practice questions b1–b39 (src/p2build/bc_questions.py).
# Slide pages = Part B PDF (EE6129_text/partB.txt). Checked by check_bcB.py.
XPL = {

# ======================= WLAN =======================
'b1': {'title': '知识讲解 + 详细解析：WLAN 覆盖多大', 'zh': '''
<h4><span class="st">知识讲解</span>WLAN 的三个关键数</h4>
<p>无线局域网（Wireless LAN, WLAN）就是把有线 LAN 的最后一段换成无线：笔记本等终端带天线，和接入点（Access Point, AP）之间走无线链路。讲义 Part B p.6 给了三个数：覆盖<b>中等距离 50–500 m</b>；每个小区只有<b>一个物理信道</b>，所有收发方、上行和下行共用一个频率；速率从 1 Mbps 到 54 Mbps。</p>
<h4><span class="st">逐项分析</span>四个范围各是什么网</h4>
<ul><li><b>A. 5–50 m</b>：错。这是个人 / 家庭网络的尺度：蓝牙 PAN 几米，ZigBee、BLE 的 HAN 几十米（p.95）。</li>
<li><b>B. 50–500 m</b>：对，讲义 p.6 原话 "Radio coverage: medium 50-500 meters"。</li>
<li><b>C. 0.5–5 km</b>：错。这是城域网 MAN（几公里）的量级（p.95）。</li>
<li><b>D. 5–50 km</b>：错。这是广域网 WAN、蜂窝宏小区的量级，Wi-Fi 的发射功率到不了。</li></ul>
<h4><span class="st">易错</span>讲义里两个数不一样</h4>
<ul><li>IoT 部分 p.95 写 LAN（IEEE 802.11）"up to 100 m"。问 WLAN 覆盖按 p.6 答 50–500 m；只有在 IoT 按距离分类时才用 p.95 的分档。</li></ul>
<div class="ans">一句话：选 B：WLAN 覆盖中等距离 50–500 m，一个小区共用一个频率，速率 1–54 Mbps（p.6）。</div>
'''},

'b2': {'title': '知识讲解 + 详细解析：BSS、ESS、AP、DS', 'zh': '''
<h4><span class="st">知识讲解</span>802.11 架构的四块积木（p.10）</h4>
<div class="tw"><table class="mini"><thead><tr><th>名称</th><th>是什么</th><th>打个比方</th></tr></thead><tbody>
<tr><td>BSS 基本服务集（Basic Service Set）</td><td>一群竞争同一无线信道的站点，就是一个小区；可以孤立，也可以经 AP 接到 DS</td><td>一间教室</td></tr>
<tr><td>AP 接入点</td><td>一个设备，当网桥用，承担中心协调功能</td><td>教室门口的老师</td></tr>
<tr><td>DS 分布系统（Distribution System）</td><td>把 AP 连起来的交换机、有线或无线网</td><td>走廊</td></tr>
<tr><td>ESS 扩展服务集（Extended Service Set）</td><td>两个以上 BSS 经 DS 互联</td><td>整栋教学楼</td></tr></tbody></table></div>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. IBSS</b>：错。（课外补充：讲义没出现这个缩写。）IBSS = 独立 BSS，就是 p.10 说的"孤立"BSS，不接 DS、没有 AP，站点直接对话，正好和"多个 BSS 经 DS 互联"相反。</li>
<li><b>B. ESS</b>：对，p.10 定义。</li>
<li><b>C. AP</b>：错。AP 是一个设备，不是一组 BSS。</li>
<li><b>D. DSSS</b>：错。这是物理层的直接序列扩频，里面的 DS 是 direct sequence，不是 distribution system，是个字面陷阱。</li></ul>
<p><b>记忆</b>：Basic 小、Extended 大，ESS 由多个 BSS 拼成。</p>
<div class="ans">一句话：选 B：多个 BSS 通过 DS 连起来叫 ESS（p.10）。</div>
'''},

'b3': {'title': '知识讲解 + 详细解析：802.11 / a / b 物理层', 'zh': '''
<h4><span class="st">知识讲解</span>物理层对照表（p.12–14）</h4>
<div class="tw"><table class="mini"><thead><tr><th>标准</th><th>频段</th><th>技术</th><th>速率</th></tr></thead><tbody>
<tr><td>802.11-1997</td><td>红外 850–950 nm；2.4 GHz</td><td>红外 IR、跳频 FHSS、直扩 DSSS 三种</td><td>1、2 Mbps</td></tr>
<tr><td>802.11b</td><td>2.4 GHz ISM</td><td>DSSS 的扩展</td><td>5.5、11 Mbps</td></tr>
<tr><td>802.11a</td><td>5 GHz</td><td>OFDM（正交频分复用）</td><td>6–54 Mbps</td></tr></tbody></table></div>
<p>老师课上强调：802.11 家族里<b>要记住 a 和 b</b>：b 在 2.4 GHz 用 DSSS，a 在 5 GHz 用 OFDM。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A</b>：错。"5 GHz、OFDM、54 Mbps"是 a 的参数，被安到了 b 身上。</li>
<li><b>B</b>：错。反过来，把 b 的"2.4 GHz、DSSS、11 Mbps"安到了 a 身上。</li>
<li><b>C</b>：对，p.14 原文：OFDM、5 GHz、6 to 54 Mbps。</li>
<li><b>D</b>：错。802.11-1997 定义了<b>三种</b>物理层（红外、FHSS、DSSS），都是 1/2 Mbps（p.12）。</li></ul>
<p><b>记忆</b>：a 跑高频高速（5 GHz、OFDM、54），b 留在 2.4 GHz 走老路 DSSS（11）。课外补充：802.11g 是 2.4 GHz + OFDM、54 Mbps，讲义 p.15 只提了名字。</p>
<div class="ans">一句话：选 C：802.11a = 5 GHz + OFDM + 6–54 Mbps；802.11b = 2.4 GHz + DSSS + 5.5/11 Mbps。</div>
'''},

'b4': {'title': '知识讲解 + 详细解析：WLAN 四类应用', 'zh': '''
<h4><span class="st">知识讲解</span>为什么要有 WLAN</h4>
<p>有线 LAN 速度快、稳定，但要拉线：大空间布线贵，两栋楼之间不好挖沟，人走动时也没法带着网线。WLAN 的四类应用（讲义 Part B p.7–8）正好对应这四种"拉线不方便"的场景。记的时候按<b>距离从近到远、从固定到移动</b>排：扩展 → 楼间 → 游牧 → 自组。</p>
<h4><span class="st">详细解析</span>四点逐条展开</h4>
<ol><li><b>LAN 扩展（LAN Extension）</b>：无线 LAN 接在同一场所的有线 LAN 上。有线部分做骨干，接服务器和固定工作站；无线部分覆盖大的开放空间，如厂房、证券交易大厅、仓库。为什么：这些地方面积大、布局常变，拉线不划算。</li>
<li><b>楼间互联（Cross-Building Interconnect）</b>：用<b>点对点</b>无线链路把相邻建筑的 LAN 连起来，两头的设备通常是网桥或路由器。为什么：楼之间挖沟埋线成本高。</li>
<li><b>游牧接入（Nomadic Access）</b>：在校园这种中等距离范围内，带着笔记本边走边上网、传数据。</li>
<li><b>自组网（Ad Hoc Networking）</b>：为眼前的需要临时搭一个<b>对等</b>网络，没有 AP；例：员工开会时把笔记本连成临时网络，会开完就散。</li></ol>
<h4><span class="st">易错</span></h4>
<ul><li>楼间互联是"点对点链路 + 网桥/路由器"，不是普通用户接入，别和游牧接入混。</li>
<li>题目要"各举一个例子"，每条都要有例子，只写名称会丢分。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(1) LAN extension: a wireless LAN is linked into a wired LAN on the same premises. The wired backbone supports servers and stationary workstations, while the wireless part serves stations in large open areas, e.g. manufacturing plants, stock-exchange trading floors and warehouses.</p>
<p>(2) Cross-building interconnect: a point-to-point wireless link connects the LANs in nearby buildings; the connected devices are typically bridges or routers.</p>
<p>(3) Nomadic access: supports mobile computing within a medium distance, e.g. a student moving around the campus with a laptop.</p>
<p>(4) Ad hoc networking: a temporary peer-to-peer network set up to meet an immediate need, e.g. employees with laptops linking their computers for the duration of a meeting.</p></div>
<div class="ans">一句话：WLAN 四类应用：LAN 扩展、楼间互联、游牧接入、自组网，每类配一个例子（p.7–8）。</div>
'''},

'b5': {'title': '知识讲解 + 详细解析：两帧 / 四帧交换', 'zh': '''
<h4><span class="st">知识讲解</span>为什么要帧交换协议</h4>
<p>无线信道误码多、还会冲突，发出去不等于收到了。802.11 用<b>帧交换协议</b>（frame exchange protocol）保证可靠传输（p.16）：接收方用 CRC（帧校验序列 FCS）检查，没错才回确认（ACK）；发送方等不到 ACK 就认为失败、重传。</p>
<p><b>隐藏节点</b>（hidden node）：A 发给 B，C 在 B 的范围内、A 的范围外（p.48）。C 听不到 A，以为信道空，一发就在 B 处撞车。只靠 ACK 解决不了：撞了只能重传，还会反复撞。</p>
<p>课外补充：有线以太网可以边发边听、发现冲突就停（CSMA/CD）；无线发射时自己的信号太强，听不到别人，所以只能"先避让、后确认"。</p>
<h4><span class="st">详细解析</span>两种流程和 NAV</h4>
<div class="calc">两帧：源 → DATA；目的检查 CRC → ACK；没收到 ACK → 重传<br>四帧：源 → RTS；目的 → CTS；源 → DATA；目的 → ACK</div>
<ol><li>RTS（请求发送）和 CTS（允许发送）都带<b>持续时间</b>（后面的数据 + ACK 要占多久）（p.17）。</li>
<li>周围节点读到这个时长，设置自己的计时器 NAV（网络分配向量），在 NAV 归零前不发送。</li>
<li>关键：隐藏节点 C 听不到 A 的 RTS，但<b>听得到 B 的 CTS</b>，于是也设 NAV、闭嘴。老师课上强调的就是这一句。</li>
<li>代价：多了两个短帧的开销，所以四帧交换换来的是可靠性。</li></ol>
<p>老师课上说 RTS/CTS 的时间线<b>不会让画</b>，理解过程即可。</p>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Two-frame exchange: the source transmits a data frame; the destination checks the frame check sequence (CRC) and replies with an ACK if the frame is received correctly; if the source does not receive the ACK, it retransmits the frame.</p>
<p>Four-frame exchange: RTS → CTS → DATA → ACK. Both RTS and CTS carry the duration of the coming data/ACK transmission, so all surrounding nodes set their NAV and defer. A hidden node, which cannot hear the RTS from the source, can still hear the CTS from the destination and defers, so collisions at the destination are avoided. The four-frame exchange improves robustness and solves the hidden node problem.</p></div>
<div class="ans">一句话：两帧 = DATA + ACK；四帧 = RTS + CTS + DATA + ACK，靠 CTS 让听不到发送方的隐藏节点也设 NAV 避让。</div>
'''},

# ======================= MAC =======================
'b6': {'title': '知识讲解 + 详细解析：SIFS、PIFS、DIFS 排序', 'zh': '''
<h4><span class="st">知识讲解</span>帧间间隔 = 优先级</h4>
<p>帧间间隔（Interframe Space, IFS）是信道空闲后必须再等多久才能发（p.20）。大家看到信道空了都要等，<b>谁要等的时间短，谁先抢到</b>，所以间隔越短、优先级越高。</p>
<div class="tw"><table class="mini"><thead><tr><th>间隔</th><th>长度</th><th>谁用</th></tr></thead><tbody>
<tr><td>SIFS（Short IFS）</td><td>最短</td><td>ACK、CTS、轮询应答这类立即响应</td></tr>
<tr><td>PIFS（PCF IFS）</td><td>中间</td><td>PCF 里 AP 发轮询，优先于普通竞争</td></tr>
<tr><td>DIFS（DCF IFS）</td><td>最长</td><td>普通异步数据帧竞争前的最短等待</td></tr></tbody></table></div>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A</b>：错，整个顺序反了，DIFS 是最长的。</li>
<li><b>B</b>：错，PIFS 必须比 DIFS 短，AP 才能压过普通竞争开始 CFP（p.29）。</li>
<li><b>C</b>：对，SIFS &lt; PIFS &lt; DIFS（p.29 原文）。</li>
<li><b>D</b>：错，SIFS 是最短的，ACK 必须最先发出。</li></ul>
<p><b>记忆</b>：S-P-D：Short 最短，Point 居中，Distributed 最长。优先级 ACK &gt; 有时限分组 &gt; 无时限数据（p.29）。课外补充：标准里 PIFS = SIFS + 1 个时隙，DIFS = SIFS + 2 个时隙。</p>
<div class="ans">一句话：选 C：SIFS &lt; PIFS &lt; DIFS，越短越优先。</div>
'''},

'b7': {'title': '知识讲解 + 详细解析：DCF 与 PCF 的关系', 'zh': '''
<h4><span class="st">知识讲解</span>802.11 MAC 的两个子层（p.18）</h4>
<p>802.11 的 MAC 叫 DFWMAC，分两层：<b>DCF</b>（分布式协调功能）是基础，用 CSMA/CA 竞争，适合突发数据；<b>PCF</b>（点协调功能）是<b>可选</b>的，与 DCF 共存、<b>建在 DCF 之上</b>，由 AP 轮询，提供面向连接、无冲突、有时限的服务。老师课上强调 PCF 的关键词是"无竞争"（contention-free）。</p>
<h4><span class="st">逐项分析</span>（本题选"错误"的一句）</h4>
<ul><li><b>A</b>：正确描述。DCF 用 CSMA/CA，适合异步、突发业务。</li>
<li><b>B</b>：正确描述。PCF 由 AP 轮询，无冲突、有时限。</li>
<li><b>C</b>：<b>错误描述，是答案</b>。PCF 不能单独工作：超帧 = CFP + CP，CP 里大家还是用 DCF 竞争（p.28）；AP 开始 CFP 也是靠 DCF 的帧间间隔机制，用 PIFS 抢信道。</li>
<li><b>D</b>：正确描述，p.18 原话 "Optional, coexist with DCF and built on DCF"。</li></ul>
<p><b>记忆</b>：DCF 是地基，PCF 是加盖的楼层，没有地基盖不了楼。</p>
<div class="ans">一句话：选 C：PCF 是可选的，建立在 DCF 之上，不能单独工作。</div>
'''},

'b8': {'title': '知识讲解 + 详细解析：二进制指数退避平均值', 'zh': '''
<h4><span class="st">知识讲解</span>二进制指数退避（p.22）</h4>
<p>站点发送失败（没收到 ACK）说明信道太挤。二进制指数退避（Binary Exponential Backoff, BEB）的思路：<b>每失败一次，把等待的范围翻倍</b>，让大家的重发时间散开，减少再次碰撞。讲义规则：</p>
<ul><li>退避时间在 0 到 CW − 1 个时隙之间<b>均匀</b>随机选，CW 叫竞争窗口（contention window）。</li>
<li>第 1 次尝试 CW = CW<sub>min</sub>；每失败一次 CW 翻倍；到 CW<sub>max</sub> 后不再增大。</li>
<li>讲义推荐 CW<sub>min</sub> = 32，CW<sub>max</sub> = 256。</li></ul>
<p>写成公式：第 k 次尝试 CW<sub>k</sub> = min(CW<sub>min</sub> × 2<sup>k−1</sup>, CW<sub>max</sub>)。0 到 N 的整数均匀分布，平均值 = (0 + N) / 2，所以平均退避 = (CW − 1) / 2。老师课上强调 DCF 流程图很重要，二进制指数退避就是用来应对重负载的。</p>
<h4><span class="st">详细解析</span>一步步数</h4>
<ol><li>先把"失败次数"换成"第几次尝试"：失败 3 次后准备的是<b>第 4 次</b>尝试，CW 翻倍了 3 次。</li>
<li>逐次算 CW，并和上限比较：</li></ol>
<div class="calc">第 1 次尝试：CW = 32<br>第 2 次尝试：CW = 32 × 2 = 64<br>第 3 次尝试：CW = 64 × 2 = 128<br>第 4 次尝试：CW = 128 × 2 = 256（= CW<sub>max</sub>，刚好到顶）<br>可选值：0, 1, …, 255，共 256 个<br>平均 = (0 + 255) / 2 = 127.5 个时隙</div>
<p><b>验算</b>：平均值应略小于 CW / 2 = 128，因为最大值是 255 不是 256；127.5 合理。</p>
<h4><span class="st">易错</span></h4>
<ul><li>范围是 0 到 CW − 1，不是 0 到 CW；用 (0 + 256)/2 = 128 就错了。</li>
<li>失败次数和尝试次数差 1。本题因为碰到上限，数错一次结果碰巧不变；但若只失败 2 次（第 3 次尝试），正确是 CW = 128、平均 (0 + 127)/2 = 63.5，数错就会得 127.5。</li>
<li>课外补充：实际 802.11b（DSSS）用 CW<sub>min</sub> = 31、CW<sub>max</sub> = 1023；考试按讲义的 32 / 256 算。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>CW starts at CW<sub>min</sub> = 32 and is doubled after each unsuccessful attempt, up to CW<sub>max</sub> = 256. After 3 failures, the 4th attempt uses CW = 32 × 2<sup>3</sup> = 256 = CW<sub>max</sub>. The backoff is uniformly chosen from 0 to CW − 1 = 255 slots, so the mean backoff = (0 + 255)/2 = 127.5 slots.</p></div>
<div class="ans">一句话：第 4 次尝试 CW = 256，退避在 0–255 均匀取，平均 127.5 个时隙。</div>
'''},

'b9': {'title': '知识讲解 + 详细解析：CW 到上限后不再增长', 'zh': '''
<h4><span class="st">知识讲解</span>CW<sub>max</sub> 是天花板</h4>
<p>讲义 p.22："CW stops increase when it reaches its maximum value CWmax"。翻倍规则只到 CW<sub>max</sub> 为止：第 k 次尝试 CW<sub>k</sub> = min(32 × 2<sup>k−1</sup>, 256)。为什么要封顶：窗口无限翻倍，一个站失败几次后就要等非常久，时延不可接受，也不公平。</p>
<h4><span class="st">详细解析</span></h4>
<ol><li>上题第 4 次尝试已是 CW = 256。又失败 2 次 → 第 6 次尝试。</li>
<li>按公式不封顶会算到 1024，再取上限：</li></ol>
<div class="calc">不封顶：32 × 2<sup>5</sup> = 1024<br>封顶：CW<sub>6</sub> = min(1024, 256) = 256<br>平均退避仍是 (0 + 255) / 2 = 127.5 个时隙</div>
<h4><span class="st">易错</span></h4>
<ul><li>直接写 1024 或 512 就是忘了上限。</li>
<li>课外补充：标准里发送<b>成功</b>后 CW 重置回 CW<sub>min</sub>，重传超过上限次数就丢弃该帧；讲义 p.22 没写，题目问到再提。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>CW is doubled after each failure but stops increasing at CW<sub>max</sub>. For the 6th attempt, 32 × 2<sup>5</sup> = 1024 &gt; 256, so CW = CW<sub>max</sub> = 256.</p></div>
<div class="ans">一句话：CW 到 CW<sub>max</sub> = 256 就封顶，第 6 次尝试仍是 256。</div>
'''},

'b10': {'title': '知识讲解 + 详细解析：RTS/CTS 三方动作', 'zh': '''
<h4><span class="st">知识讲解</span>信道预约（Channel Reservation，p.24–25）</h4>
<p>RTS/CTS 就是"先订座、再上菜"：发送方先用短帧 RTS 订下信道，接收方用 CTS 确认，周围的人从这两个帧里读出要占用多久，自觉让开。用到两个间隔：<b>DIFS</b>（长，普通竞争前要等的）和 <b>SIFS</b>（短，同一次交换里的应答之间用）。同一次交换内部只隔 SIFS，别的站至少要等 DIFS，所以中途没人插得进来。</p>
<h4><span class="st">详细解析</span>按时间顺序</h4>
<div class="calc">发送方：侦听到信道空闲 DIFS → 发 RTS<br>接收方：等 SIFS → 回 CTS<br>发送方：收到 CTS，等 SIFS → 发数据<br>接收方：收完数据，等 SIFS → 回 ACK<br>其他站：读 RTS/CTS 的持续时间 → 设 NAV → 等 NAV + DIFS → 退避后再竞争</div>
<ol><li><b>发送方</b>先等 DIFS：确认信道真的空了，且让高优先级的帧（用 SIFS、PIFS 的）先走。</li>
<li><b>接收方</b>只等 SIFS 就回 CTS、ACK：应答优先级最高，要最快回。</li>
<li><b>其他站点</b>做虚拟载波侦听：读出帧里的 duration 字段设置 NAV，推迟"NAV + DIFS"，之后还要走一次退避（p.24 "Backoff after defer"），避免大家同时冲出来。</li></ol>
<p>老师课上说时间线<b>不会让画</b>，但要能按顺序写出每一方的动作。</p>
<h4><span class="st">易错</span></h4>
<ul><li>发送方开头等的是 DIFS 不是 SIFS；中间的应答才用 SIFS。</li>
<li>其他站点推迟的是 NAV + DIFS，最后还有退避，别漏。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Sender: senses the channel free for a DIFS interval, transmits an RTS to reserve the channel; once a CTS is received, waits for an SIFS and then sends the data packet.</p>
<p>Receiver: on receiving the RTS, waits for an SIFS and responds with a CTS; once the packet has been received, waits for an SIFS and responds with an ACK.</p>
<p>All other stations: listen to the channel, read the duration field and set their NAV, defer access for the NAV time plus DIFS, and then back off.</p></div>
<div class="ans">一句话：发送方 DIFS → RTS，接收方 SIFS → CTS，发送方 SIFS → 数据，接收方 SIFS → ACK；旁人设 NAV，等 NAV + DIFS 再退避。</div>
'''},

'b11': {'title': '知识讲解 + 详细解析：NAV 与虚拟载波侦听', 'zh': '''
<h4><span class="st">知识讲解</span>两种"听信道"的办法</h4>
<p><b>物理载波侦听</b>：真的去测信道上有没有信号。缺点：隐藏节点听不到发送方，测出来是"空"。<b>虚拟载波侦听</b>（virtual carrier sense，p.23）：每个帧带一个持续时间（duration）字段，说明这次传输（含后续分片和 ACK）要占多久；附近节点据此更新自己的计时器 NAV（Network Allocation Vector）。要发送前先看 NAV：不为零就当信道忙，等它数到零。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. 物理载波侦听</b>：错。那是测射频能量，NAV 是读帧里的数字。</li>
<li><b>B. 虚拟载波侦听</b>：对，p.23 原话 "Collision Avoidance is achieved by a virtual carrier sense mechanism"。</li>
<li><b>C. 功率控制</b>：错。NAV 不改发射功率。</li>
<li><b>D. 跳频同步</b>：错。跳频（FHSS）是物理层的事，和 NAV 无关。</li></ul>
<p><b>记忆</b>：物理侦听是"竖起耳朵听"，虚拟侦听是"看别人贴出的占用时间表"。老师说帧格式里要记的就是地址字段和 duration 字段，后者正是 NAV 的来源。</p>
<div class="ans">一句话：选 B：NAV 根据帧里的 duration 字段计时，实现虚拟载波侦听。</div>
'''},

'b12': {'title': '知识讲解 + 详细解析：PCF 轮询与超帧', 'zh': '''
<h4><span class="st">知识讲解</span>PCF 就是 AP 点名</h4>
<p>DCF 是大家抢着说，PCF（点协调功能）是 AP 当主持人、挨个点名，所以无冲突、有时限（p.26）。点名期间 AP 占住信道，异步业务全部锁住，DCF 暂停工作。</p>
<p><b>超帧</b>（superframe，p.28）：两个 DTIM 信标（Delivery Traffic Indication Message，提供同步和定时）之间的时间 = <b>CFP</b>（无竞争期，AP 轮询）+ <b>CP</b>（竞争期，大家用 DCF）。CFP 的长度随业务量变，因为各站发的帧长不同。</p>
<h4><span class="st">详细解析</span>三问逐个答</h4>
<ol><li><b>轮询过程</b>（p.27）：AP 给某个节点发 CF-Poll；AP 自己有数据时，把数据和 CF-Poll 捎带（piggyback）在一帧里。被点到的节点回 Data+CF-ACK（有数据）或 CF-ACK（没数据）。和这个节点交换完，AP 点下一个。所有节点点完或 CFP 时间到，AP 广播 CF-End 宣布 CFP 结束。</li>
<li><b>超帧组成</b>：CFP + CP，由 DTIM 信标开始。AP 在信标里广播实际 CFP 时长，各节点据此设 NAV；CFP 结束时所有节点把 NAV 清零，之后到下一个 DTIM 前都用 DCF 竞争（p.29）。</li>
<li><b>为什么 CFP 不会被 CP 打断</b>：因为 SIFS &lt; PIFS &lt; DIFS。AP 用 PIFS 抢信道，普通站点要等更长的 DIFS，AP 一定先拿到；CFP 内部的应答只隔 SIFS，普通站点插不进来。优先级：ACK &gt; 有时限分组 &gt; 无时限数据（p.29）。</li></ol>
<h4><span class="st">易错</span></h4>
<ul><li>CF-End 是 AP 广播的，不是最后一个被轮询的站发的。</li>
<li>"不被打断"的原因要落到 IFS 长短上，只写"PCF 优先级高"不够。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Polling is started by the AP sending a CF-Poll frame to a node; if the AP has pending data, it piggybacks the CF-Poll on a data frame. The polled node responds with Data+CF-ACK or CF-ACK. The AP then polls the next node in its list. When all nodes have been polled or the CFP duration has expired, the AP broadcasts a CF-End frame.</p>
<p>A superframe consists of a contention-free period (CFP), in which the AP polls the nodes, followed by a contention period (CP), in which nodes contend using DCF; it starts with a DTIM beacon.</p>
<p>A CFP cannot be interrupted by a CP because SIFS &lt; PIFS &lt; DIFS: the AP seizes the channel with PIFS, which is shorter than the DIFS used by contending stations, so the CFP has higher priority.</p></div>
<div class="ans">一句话：AP 发 CF-Poll 挨个点名、最后广播 CF-End；超帧 = CFP + CP；PIFS 比 DIFS 短，所以 CFP 不会被打断。</div>
'''},

'b13': {'title': '知识讲解 + 详细解析：超帧被缩短', 'zh': '''
<h4><span class="st">知识讲解</span>CP 结束时 AP 要抢信道（p.29）</h4>
<p>超帧的标称长度由 DTIM 信标的间隔定好。CP 末尾，AP 用 PIFS 竞争信道：信道空闲，AP 拿到信道，CP 结束、新的 CFP 开始；信道正忙（某站的帧还没发完），AP 只能<b>等它变空</b>，于是 CFP 晚开始，下一周期的超帧被压短，讲义叫 "foreshortened superframe"。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A</b>：错。802.11 没有"打断别人"的机制，PIFS 只是让 AP 在信道空闲后先抢，正在发的帧要让它发完。</li>
<li><b>B</b>：对，讲义原话 "resulting in a foreshortened superframe for the next cycle"。</li>
<li><b>C</b>：错。讲义没有"取消 CFP"，只是晚一点开始。</li>
<li><b>D</b>：错。NAV 清零发生在 CFP 结束时（p.29），和这里的情况无关。</li></ul>
<p><b>记忆</b>：上课铃响了，前一个人话还没说完，老师得等他说完再点名，这节课就短了一截。</p>
<div class="ans">一句话：选 B：AP 等信道空闲才能开始 CFP，下一周期的超帧被缩短。</div>
'''},

'b14': {'title': '知识讲解 + 详细解析：扫描、认证、关联', 'zh': '''
<h4><span class="st">知识讲解</span>新节点加入 BSS 的三步（p.31–32）</h4>
<ol><li><b>扫描</b>（scanning）：先找到 AP、拿到同步信息。被动扫描：等 AP 发的信标帧（Beacon）；主动扫描：自己发 Probe Request，等 AP 回 Probe Response。</li>
<li><b>认证</b>（authentication）：AP 和节点交换信息，双方证明自己知道约定的密码。</li>
<li><b>关联</b>（association）：交换节点和 BSS 的能力信息，并告诉分布系统（所有 AP）这个节点现在在哪。<b>关联完成后才能收发数据帧</b>。</li></ol>
<p>老师课上特别提到认证这一步，提醒大家一定要设密码；这一题 2025-26 S1 Q4(a) 考过。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A</b>：错。还没找到 AP，跟谁认证？</li>
<li><b>B</b>：错。认证必须在关联之前，没确认身份不能登记。</li>
<li><b>C</b>：对。</li>
<li><b>D</b>：错。关联是最后一步。</li></ul>
<p><b>记忆</b>：找门（扫描）→ 验身份（认证）→ 登记住址（关联）。</p>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Scanning: the node gets synchronization information from the AP, either passively by waiting for a beacon frame, or actively by sending probe request frames and waiting for a probe response. Authentication: the AP and the node exchange information to prove that each side knows a given password. Association: they exchange information about the node and BSS capabilities, and the distribution system is informed of the node's current position. Only after association can the node transmit and receive data frames.</p></div>
<div class="ans">一句话：选 C：扫描 → 认证 → 关联，关联完才能收发数据。</div>
'''},

'b15': {'title': '知识讲解 + 详细解析：三类 MAC 帧', 'zh': '''
<h4><span class="st">知识讲解</span>MAC 帧分三类（p.33）</h4>
<div class="tw"><table class="mini"><thead><tr><th>类型</th><th>干什么</th><th>例子</th></tr></thead><tbody>
<tr><td>数据帧</td><td>传数据</td><td>普通数据帧，末尾 FCS 是 32 位 CRC（p.34）</td></tr>
<tr><td>控制帧</td><td>预约信道、确认收到</td><td>RTS、CTS、ACK</td></tr>
<tr><td>管理帧</td><td>与 AP 关联 / 解除关联、定时同步、安全控制</td><td>信标、Probe、认证、关联</td></tr></tbody></table></div>
<p>帧格式里的帧控制（Frame Control）字段标明这是哪一类（p.34）。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. 数据帧</b>：错，只负责传数据。</li>
<li><b>B. 控制帧</b>：错，管的是信道预约和确认，是"交通指挥"不是"行政手续"。</li>
<li><b>C. 管理帧</b>：对，题干三项就是 p.33 管理帧的三条原文。</li>
<li><b>D</b>：错。信标帧负责同步（p.31），本身就属于管理帧，"信标以外的所有帧"说不通。</li></ul>
<p><b>记忆</b>：管理帧 = 办手续（入网、对时、安全）；控制帧 = 指挥交通（RTS/CTS/ACK）。</p>
<div class="ans">一句话：选 C：关联、同步、安全控制都是管理帧的活。</div>
'''},

'b16': {'title': '知识讲解 + 详细解析：802.11e 的 EDCA', 'zh': '''
<h4><span class="st">知识讲解</span>802.11e 给业务分优先级（p.39–40）</h4>
<p>原始 DCF 对所有帧一视同仁，语音、视频得不到保证。802.11e 加了两种模式：<b>EDCA</b>（增强分布式信道接入）是带优先级的 DCF；<b>HCCA</b> 类似 PCF，由混合协调器 HC 按各业务类的负载调度无竞争发送机会。</p>
<p>EDCA 的做法（讲义原话 "eight traffic classes"）：<b>8 个业务类</b>，每类在节点内有自己的队列和<b>独立的退避参数</b>，再加一个仲裁帧间间隔 AIFS（Arbitration IFS）。各类先在节点内部竞争一个"虚拟信道"，胜出的帧再像原来的 DCF 一样竞争真正的信道。AIFS 短、竞争窗口小的类，等得少，就更优先，和 b6 里"间隔越短越优先"是同一个道理。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. 4 个，靠不同信道</b>：错。数量和讲义不符；而且各类共用同一个信道，靠的是参数不同，不是信道不同。</li>
<li><b>B. 8 个，靠各自的退避参数和 AIFS</b>：对，按讲义。</li>
<li><b>C. 8 个，靠 AP 轮询</b>：错。轮询是 HCCA（和 PCF）的做法，EDCA 是竞争式的。</li>
<li><b>D. 16 个，靠 QCI</b>：错。QCI 是 LTE 承载的 QoS 标识（p.71），不是 WLAN 的。</li></ul>
<h4><span class="st">课外补充</span>标准里其实是 4 个接入类别</h4>
<p>802.11e 标准中是 8 个用户优先级（0–7），映射成 <b>4 个接入类别</b> AC：背景 AC_BK、尽力而为 AC_BE、视频 AC_VI、语音 AC_VO，每个 AC 一个队列、一套 AIFS 和 CW。讲义写的是 8 个业务类，<b>考试按讲义选 8</b>；简答题也照讲义写 "eight traffic classes"。</p>
<div class="ans">一句话：选 B：EDCA 有 8 个业务类（讲义说法），每类独立队列、独立退避参数和 AIFS。</div>
'''},

# ======================= MANET / WSN =======================
'b17': {'title': '知识讲解 + 详细解析：MANET 是什么', 'zh': '''
<h4><span class="st">知识讲解</span>没有基础设施的网</h4>
<p>移动自组网（Mobile Ad Hoc Network, MANET）：一组无线移动节点，在没有基础设施（没有 AP、没有基站）的地方，自由、动态地自己组织成临时的、任意形状的网络（p.42）。它是对等（peer-to-peer）网络：不需要固定控制器，控制器由节点<b>动态选举</b>或<b>分散在所有节点</b>上；网络自建、自组织、自管理（self-creating, self-organizing, self-administering，p.43）。</p>
<div class="tw"><table class="mini"><thead><tr><th></th><th>有 AP 的 WLAN</th><th>MANET</th></tr></thead><tbody>
<tr><td>基础设施</td><td>AP + 分布系统</td><td>没有</td></tr>
<tr><td>控制</td><td>AP 集中协调</td><td>动态选举或分布式</td></tr>
<tr><td>转发</td><td>都经过 AP，单跳到 AP</td><td>节点互相转发，可多跳</td></tr></tbody></table></div>
<h4><span class="st">详细解析</span>答题要点</h4>
<ol><li><b>定义</b>：写出"无基础设施、自组织、临时拓扑"三个关键词。</li>
<li><b>最大区别</b>：每个节点都必须能<b>按需当路由器</b>（p.45）。A 和 C 之间没有直接无线信道时，由中间节点 B 中继，这就是多跳（multi-hop）。选的路径必须无环（loop free），才叫路由。</li>
<li><b>可以补一句</b>：802.11 很简单，适合做单跳自组网，也能搭几平方公里的多跳网；蓝牙可以组半径约 10 m 的体域网 / 个域网（p.43）。</li></ol>
<h4><span class="st">易错</span></h4>
<ul><li>只答"没有 AP"不够，要点出"每个节点都是路由器、多跳中继"。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>A MANET is a system of wireless mobile nodes that freely and dynamically self-organize into arbitrary and temporary network topologies, so that devices can be connected in areas without infrastructure. No fixed controller is required: a controller is dynamically elected or distributed among the nodes, and the network is self-creating, self-organizing and self-administering. The key difference from an infrastructure WLAN is that every node must be able to act as a router on demand: when two nodes have no direct radio channel, intermediate nodes relay the packets (multi-hop), instead of all traffic going through an AP.</p></div>
<div class="ans">一句话：MANET 是无基础设施、自组织的临时网络；和 WLAN 最大的区别是每个节点都要当路由器、多跳转发。</div>
'''},

'b18': {'title': '知识讲解 + 详细解析：隐藏节点在哪', 'zh': '''
<h4><span class="st">知识讲解</span>冲突发生在接收端</h4>
<p>无线冲突要看<b>接收端</b>：只要 B 同时收到两路信号，B 就收不好。隐藏节点（hidden node，p.48）= 在<b>目的端 B 范围内</b>、在<b>发送端 A 范围外</b>的节点 C。C 听不到 A，侦听结果是"信道空"，一发就在 B 处和 A 的数据撞车，造成低利用率。解决：RTS/CTS，C 虽听不到 A 的 RTS，却能听到 B 的 CTS，于是设 NAV 推迟（p.17）。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. 在 A 范围内、B 范围外</b>：错。它听得到 A，会主动避让，不是隐藏节点。（课外补充：这种节点叫"暴露节点" exposed node，它想发给别人时会被 A 不必要地挡住。）</li>
<li><b>B. 在 B 范围内、A 范围外</b>：对。</li>
<li><b>C. 同时在两人范围内</b>：错。它能听到 A，载波侦听就够用了。</li>
<li><b>D. 不在任何人范围内</b>：错。它的信号到不了 B，不会造成冲突。</li></ul>
<p><b>记忆</b>："藏"在发送方的视线外，却站在接收方身边。</p>
<div class="ans">一句话：选 B：隐藏节点在目的端范围内、发送端范围外。</div>
'''},

'b19': {'title': '知识讲解 + 详细解析：自组网的路由协议', 'zh': '''
<h4><span class="st">知识讲解</span>四类路由方式（p.51–53）</h4>
<div class="tw"><table class="mini"><thead><tr><th>类别</th><th>什么时候找路由</th><th>代价</th></tr></thead><tbody>
<tr><td>周期性（表驱动）</td><td>一直周期交换，不管用不用</td><td>随时有路，但耗带宽</td></tr>
<tr><td>按需（on-demand）</td><td>有数据要发才做路由发现，通信期间维护</td><td>省带宽，首包要等发现</td></tr>
<tr><td>混合</td><td>本地区域用周期性，全局用按需</td><td>折中</td></tr>
<tr><td>基于位置</td><td>只需自己、目的和邻居的位置</td><td>不存路由表，但要准确的位置服务</td></tr></tbody></table></div>
<p>老师课上说：按需路由只在需要时做路由发现，只激活相关节点，不浪费带宽。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. 周期性</b>：错，正好相反，平时一直在维护。</li>
<li><b>B. 按需</b>：对，p.52 原话 "create routes only when necessary"。</li>
<li><b>C. 混合</b>：错，它在本地区域仍周期维护。</li>
<li><b>D. 基于位置</b>：错，它根本不建路由，靠位置逐跳转发。</li></ul>
<p>课外补充：常见例子 AODV、DSR 是按需，DSDV、OLSR 是表驱动，ZRP 是混合。</p>
<div class="ans">一句话：选 B：按需协议平时不维护路由，有数据要发才发起路由发现。</div>
'''},

'b20': {'title': '知识讲解 + 详细解析：组合稳定性', 'zh': '''
<h4><span class="st">知识讲解</span>拓扑在变，更新跟得上吗</h4>
<p>自组网里"谁能直接连到谁"（可达关系）会随时间变化，原因是：节点移动、电池耗尽、软件或硬件故障（p.47）。每次变化都要发拓扑更新，这些更新会吃掉本来给用户数据的带宽。</p>
<p><b>组合稳定性</b>（combinatorial stability）：在给定的时间窗内，如果拓扑变化<b>足够慢</b>，慢到所有必要的拓扑更新都能成功传播出去，这个网络在这段时间内就是组合稳定的。"组合"指的是节点之间的连接关系（哪些边存在），稳定就是这张连接图的变化速度不超过网络消化更新的速度。</p>
<h4><span class="st">详细解析</span>由哪些因素决定</h4>
<ol><li><b>网络的连通性</b>：连接关系本身变得多快、多剧烈。</li>
<li><b>路由协议的复杂度</b>：协议越复杂，一次更新要交换的消息越多、传播越慢。</li>
<li><b>节点的瞬时计算能力</b>：节点算得慢，处理更新就慢。</li></ol>
<p>讲义原话强调"不仅取决于连通性"，所以三个因素都要写，只写"移动速度"会丢分。</p>
<h4><span class="st">易错</span></h4>
<ul><li>"拓扑变化的原因"（移动、电池、故障）和"稳定性的决定因素"（连通性、协议复杂度、计算能力）是两组东西，别混在一起答。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>The reachability relations among nodes change with time because of node mobility, battery depletion and software or hardware failures, and the resulting topology updates consume bandwidth. Given a specific time window, an ad hoc network is combinatorially stable if and only if the topology changes occur sufficiently slowly to allow successful propagation of all necessary topology updates. Combinatorial stability is determined not only by the connectivity properties of the network, but also by the complexity of the routing protocol in use and the instantaneous computational capacity of the nodes.</p></div>
<div class="ans">一句话：拓扑变化慢到所有更新都能传播完就叫组合稳定，取决于连通性、路由协议复杂度和节点计算能力。</div>
'''},

'b21': {'title': '知识讲解 + 详细解析：WSN 与自组网四点不同', 'zh': '''
<h4><span class="st">知识讲解</span>传感器网络是什么</h4>
<p>无线传感器网络（Wireless Sensor Network, WSN）：大量低成本、低功耗的小节点（感知 + 数据处理 + 通信），密集地部署在被测现象内部或附近，可以随机撒在难以到达的地方或灾区；协议必须能自组织，节点要相互协作（p.76）。它要用自组网技术实现，但自组网已有的协议不一定适合，因为有四点不同（p.56）。</p>
<div class="tw"><table class="mini"><thead><tr><th>方面</th><th>一般自组网</th><th>传感器网络</th></tr></thead><tbody>
<tr><td>节点数量</td><td>较少</td><td>多几个数量级</td></tr>
<tr><td>部署与拓扑</td><td>拓扑会变</td><td>部署密集、易失效，拓扑变化非常频繁</td></tr>
<tr><td>通信方式</td><td>点对点</td><td>广播</td></tr>
<tr><td>资源</td><td>笔记本、手机，较充足</td><td>功率、计算能力、内存都很有限</td></tr></tbody></table></div>
<h4><span class="st">详细解析</span>每点为什么重要</h4>
<ol><li><b>数量大</b> → 协议要能扩展，不能每个节点都存全网路由表。</li>
<li><b>密集、易坏、拓扑常变</b> → 路由要能快速自愈。</li>
<li><b>广播</b> → MAC 要尽量减少和邻居广播的冲突（p.59）。</li>
<li><b>资源有限</b> → 一切以省电为先；老师课上说功耗是最关键的因素，因为节点大多靠电池。</li></ol>
<p>结论：自组网的协议不能直接照搬到传感器网络。</p>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(1) The number of sensor nodes is huge, up to several orders of magnitude higher than in an ad hoc network. (2) Sensor nodes are densely deployed and prone to failures, so the topology changes very frequently. (3) Sensor nodes use a broadcast communication paradigm, while ad hoc networks are based on point-to-point communications. (4) Sensor nodes are limited in power, computational capacity and memory. Therefore protocols designed for ad hoc networks may not fit sensor networks well.</p></div>
<div class="ans">一句话：WSN 节点多几个数量级、密集易坏拓扑常变、用广播、功率计算内存都受限。</div>
'''},

'b22': {'title': '知识讲解 + 详细解析：传感器协议栈三平面', 'zh': '''
<h4><span class="st">知识讲解</span>五层 + 三个平面（p.59）</h4>
<p>五层自下而上：物理层（简单而稳健的调制、收发）、MAC 层（要省电、尽量减少与邻居广播的冲突）、网络层（给传输层交来的数据选路）、传输层（维持数据流）、应用层。另有三个<b>管理平面</b>纵向贯穿各层，监控节点之间的：</p>
<ul><li><b>功率管理</b>：节点怎么用电，比如电量低时少转发。</li>
<li><b>移动管理</b>：节点的移动，记住邻居是谁。</li>
<li><b>任务管理</b>：在节点间分配感知任务。</li></ul>
<p>老师课上说协议栈记住<b>五层</b>就行，功耗是最关键的因素。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. 功率、移动、任务</b>：对，p.59 原话 "power, mobility, and task management planes"。</li>
<li><b>B. 安全、QoS、计费</b>：错，讲义的传感器协议栈没有这三项。</li>
<li><b>C. 时钟、路由、存储</b>：错，路由是网络层的事，不是平面。</li>
<li><b>D. 频率、功率、编码</b>：错，频率和编码属于物理层。</li></ul>
<p><b>记忆</b>：传感器最缺电、会挪动、要分工，所以是"电、动、活"三个平面。</p>
<div class="ans">一句话：选 A：三个管理平面是功率、移动、任务。</div>
'''},

# ======================= LTE =======================
'b23': {'title': '知识讲解 + 详细解析：EPS 的两大部分', 'zh': '''
<h4><span class="st">知识讲解</span>LTE 系统的两半（p.61–62）</h4>
<p>LTE 是 3GPP 在 UMTS（3G）之后的演进，目标是终端 UE 和分组数据网 PDN 之间无缝的 IP 连接。整个系统叫<b>演进分组系统 EPS</b>（Evolved Packet System），由两半组成：</p>
<div class="tw"><table class="mini"><thead><tr><th>部分</th><th>来自哪个项目</th><th>里面有什么</th></tr></thead><tbody>
<tr><td>EPC 演进分组核心网</td><td>SAE（系统架构演进）</td><td>很多逻辑节点，如 MME、S-GW</td></tr>
<tr><td>E-UTRAN 演进的无线接入网</td><td>LTE</td><td>基本只有一种节点：eNodeB</td></tr></tbody></table></div>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. UTRAN + GSM 核心网</b>：错。UTRAN 是 3G UMTS 的接入网，LTE 用的是"演进的"E-UTRAN，名字前多个 E。</li>
<li><b>B. EPC + E-UTRAN</b>：对。</li>
<li><b>C. eNodeB + MME</b>：错。这是两边各一个节点，不是两大组成部分。</li>
<li><b>D. S1 + X2</b>：错。这是接口，不是网络部分。</li></ul>
<p><b>记忆</b>：SAE 管"核心"（Core → EPC），LTE 管"无线"（Radio → E-UTRAN）。</p>
<div class="ans">一句话：选 B：EPS = 核心网 EPC + 接入网 E-UTRAN。</div>
'''},

'b24': {'title': '知识讲解 + 详细解析：X2 与 S1 接口', 'zh': '''
<h4><span class="st">知识讲解</span>扁平的接入网（p.63）</h4>
<p>E-UTRAN 由许多 eNodeB 组成，普通用户业务<b>没有集中控制器</b>。各 eNodeB 之间用 <b>X2</b> 接口横向相连；eNodeB 向上用 <b>S1</b> 接口连核心网 EPC，S1 又分两条：</p>
<ul><li><b>S1-MME</b>：接移动性管理实体 MME，走信令（控制面）。</li>
<li><b>S1-U</b>：接服务网关 S-GW，走用户数据（U = user plane）。</li></ul>
<p>eNodeB 和 UE 之间跑的是空中接口信令（AS）协议（讲义 p.63 原话 "air signaling (AS) protocols"；课外补充：3GPP 标准里 AS 指接入层 Access Stratum）。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. S1；X2</b>：错，正好颠倒。</li>
<li><b>B. X2；S1</b>：对，p.63 原文。</li>
<li><b>C. Uu；S1</b>：错。（课外补充：Uu 是 UE 和 eNodeB 之间的空中接口，不是 eNodeB 之间的。）</li>
<li><b>D. X2；Gi</b>：错。（课外补充：Gi 是 3G 核心网连外部数据网的接口，LTE 里对应 SGi，不连 eNodeB。）</li></ul>
<p><b>记忆</b>：X 像交叉，横着连兄弟；S1 往上连核心网，MME 走信令、U 走用户数据。</p>
<div class="ans">一句话：选 B：eNodeB 之间是 X2，到核心网是 S1（S1-MME 到 MME，S1-U 到 S-GW）。</div>
'''},

'b25': {'title': '知识讲解 + 详细解析：E-UTRAN 的功能', 'zh': '''
<h4><span class="st">知识讲解</span>无线的事都归 eNodeB</h4>
<p>E-UTRAN 负责<b>所有和无线有关的功能</b>（p.64）。因为接入网只有 eNodeB 一种节点、没有集中控制器（p.63），这些功能全部集成在 eNodeB 里。课外补充：3G 里有集中的无线网络控制器 RNC，LTE 把它去掉、做成扁平结构，路径更短、时延更低。</p>
<h4><span class="st">详细解析</span>四类功能，逐条说为什么</h4>
<ol><li><b>无线资源管理</b>（Radio Resource Management）：与无线承载有关的全部功能：无线承载控制、无线接纳控制、无线移动性控制、上下行的调度和动态资源分配。为什么：空口资源（时间、频率）有限，要按需分给各 UE。</li>
<li><b>包头压缩</b>（Header Compression）：压缩 IP 包头，减少开销。为什么：语音等小包的 IP 头占比大，压缩后空口效率更高。</li>
<li><b>安全</b>（Security）：空中接口上发送的所有数据都加密。为什么：无线信号谁都能收到。</li>
<li><b>连接 EPC</b>（Connectivity to the EPC）：到 MME 的信令和到 S-GW 的承载路径，也就是 S1-MME 和 S1-U。</li></ol>
<h4><span class="st">易错</span></h4>
<ul><li>无线资源管理下的四个小项（承载控制、接纳控制、移动控制、调度）要写全，这是得分细节。</li>
<li>别把核心网的功能（如 MME 的移动性管理信令处理）写成 E-UTRAN 的。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>The E-UTRAN is responsible for all radio-related functions: (1) radio resource management, i.e. all functions related to radio bearers, including radio bearer control, radio admission control, radio mobility control, and scheduling and dynamic allocation of resources to UEs in both uplink and downlink; (2) header compression of IP packet headers to reduce overhead; (3) security: all data sent over the radio interface is encrypted; (4) connectivity to the EPC: the signalling towards the MME and the bearer path to the S-GW. All these functions reside in the eNodeBs; there is no centralized controller.</p></div>
<div class="ans">一句话：E-UTRAN 管无线资源管理、包头压缩、空口加密、连接 EPC，全部做在 eNodeB 里。</div>
'''},

'b26': {'title': '知识讲解 + 详细解析：E-UTRA 主要指标', 'zh': '''
<h4><span class="st">知识讲解</span>四组指标（p.65）</h4>
<div class="tw"><table class="mini"><thead><tr><th>指标</th><th>讲义数字</th></tr></thead><tbody>
<tr><td>可伸缩带宽</td><td>1.4 MHz 到 20 MHz</td></tr>
<tr><td>高速率</td><td>下行峰值超过 300 Mbps（4×4 MIMO）；上行峰值 86 Mbps</td></tr>
<tr><td>高移动性</td><td>针对 15 km/h 以下的低速优化，最高支持 350 甚至 500 km/h</td></tr>
<tr><td>可伸缩覆盖</td><td>毫微微小区（femtocell）到 100 km 小区</td></tr></tbody></table></div>
<p>老师课上说 LTE 带宽可以在 1.4–20 MHz 之间灵活选，不像 1G 那样每个信道带宽固定。</p>
<h4><span class="st">逐项分析</span>（本题找"不符"的一项）</h4>
<ul><li><b>A</b>：符合。</li>
<li><b>B</b>：符合，前提是 4×4 MIMO。</li>
<li><b>C</b>：符合。</li>
<li><b>D</b>：<b>不符，是答案</b>。两个数对调了：优化的是 15 km/h（步行、低速），350 km/h 是最高"支持"的速度（高铁）。</li></ul>
<p><b>记忆</b>：优化给大多数人（走路 15），支持到极端情况（高铁 350/500）。</p>
<div class="ans">一句话：选 D：LTE 针对 15 km/h 以下优化，最高支持 350 甚至 500 km/h。</div>
'''},

'b27': {'title': '知识讲解 + 详细解析：LTE 帧里有几个时隙', 'zh': '''
<h4><span class="st">知识讲解</span>FDD 帧结构（p.66）</h4>
<p>LTE 在时间上分三级：<b>无线帧</b>（radio frame）10 ms → <b>子帧</b>（subframe）1 ms → <b>时隙</b>（slot）0.5 ms。FDD（频分双工）模式下，一帧 10 个子帧，每个子帧 2 个时隙。TDD 模式帧长也是 10 ms，但分成两个 5 ms 半帧，里面可能有含 DwPTS、GP、UpPTS 的特殊子帧，本题问的是 FDD。</p>
<h4><span class="st">详细解析</span>两种算法互相验算</h4>
<div class="calc">按层级：10 个子帧 × 2 个时隙/子帧 = 20 个时隙<br>按时长：10 ms ÷ 0.5 ms = 20 个时隙</div>
<p>课外补充：1 ms 的子帧是 LTE 调度的基本时间单位（TTI）；一个时隙是资源块在时间上的长度（见 b28）。</p>
<h4><span class="st">易错</span></h4>
<ul><li>别把子帧（10 个）当成时隙（20 个）。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>In FDD mode, each 10 ms radio frame consists of 10 subframes of 1 ms, and each subframe consists of 2 slots of 0.5 ms. Hence one radio frame contains 10 × 2 = 20 slots (check: 10 ms / 0.5 ms = 20).</p></div>
<div class="ans">一句话：10 ms 帧 = 10 个 1 ms 子帧 = 20 个 0.5 ms 时隙。</div>
'''},

'b28': {'title': '知识讲解 + 详细解析：资源块里的资源单元', 'zh': '''
<h4><span class="st">知识讲解</span>资源网格（p.67）</h4>
<p>LTE 下行用 OFDMA，资源是一张"时间 × 频率"的网格。</p>
<ul><li><b>资源单元 RE</b>（Resource Element）：1 个子载波 × 1 个 OFDM 符号，网格里最小的一格。</li>
<li><b>资源块 RB</b>（Resource Block）：频域 <b>12 个子载波</b> × 时域 <b>1 个时隙</b>（0.5 ms）。</li>
<li>一个时隙里有几个 OFDM 符号取决于循环前缀 CP：常规 CP 是 <b>7</b> 个，扩展 CP 是 <b>6</b> 个（大小区用，见 b29）。</li></ul>
<p>老师课上也提到每个资源块 12 个子载波。</p>
<h4><span class="st">详细解析</span></h4>
<div class="calc">常规 CP：RE = 12 子载波 × 7 符号 = 84 个<br>扩展 CP：RE = 12 子载波 × 6 符号 = 72 个</div>
<p>课外补充：LTE 子载波间隔 15 kHz，所以一个 RB 宽 12 × 15 = 180 kHz；一个 1 ms 子帧里两个时隙的 RB 对共 2 × 84 = 168 个 RE。</p>
<h4><span class="st">易错</span></h4>
<ul><li>RB 在时间上是 1 个<b>时隙</b>，不是 1 个子帧，别乘成 12 × 14。</li>
<li>题目写"常规循环前缀"就用 7；没说明时按常规 CP 算，并注明假设。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>A resource block spans 12 subcarriers in the frequency domain and one slot in the time domain. With the normal cyclic prefix there are 7 OFDM symbols per slot, and a resource element is one subcarrier × one OFDM symbol, so one RB contains 12 × 7 = 84 REs (72 with the extended CP).</p></div>
<div class="ans">一句话：RB = 12 子载波 × 7 符号 = 84 个 RE（扩展 CP 为 72）。</div>
'''},

'b29': {'title': '知识讲解 + 详细解析：何时用扩展 CP', 'zh': '''
<h4><span class="st">知识讲解</span>循环前缀挡回波</h4>
<p>循环前缀（Cyclic Prefix, CP）是把 OFDM 符号末尾的一小段复制到符号前面，当保护间隔。多径信号走不同的路，晚到的回波会拖进下一个符号造成干扰；只要保护间隔不短于最大时延扩展，回波就落在 CP 里，接收机丢掉 CP 即可。Part 2 第 7 章 p.17 的条件：保护间隔 T<sub>G</sub> ≥ 最大时延扩展 T<sub>D</sub>。</p>
<p>讲义 Part B p.67："The extended CP is used when the cell size is large."小区大 → 反射路径长、回波来得更晚 → 时延扩展大 → 要更长的 CP。代价：时隙长度固定 0.5 ms，CP 变长后只放得下 6 个符号（常规 7 个），开销变大。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. 小区很小</b>：错，小区小时延扩展小，常规 CP 就够。</li>
<li><b>B. 小区很大</b>：对，p.67 原文。</li>
<li><b>C. 上行时</b>：错，CP 长短看时延扩展，不看上下行。</li>
<li><b>D. TDD 模式</b>：错，FDD 和 TDD 都有常规 / 扩展两种 CP。</li></ul>
<p>课外补充：常规 CP 约 4.7 μs，对应路程差 4.7 μs × 3×10⁸ m/s ≈ 1.4 km；扩展 CP 约 16.7 μs，对应约 5 km，所以能容忍大小区里更远的回波。</p>
<div class="ans">一句话：选 B：大小区时延扩展大，用扩展 CP，代价是每时隙只剩 6 个符号。</div>
'''},

'b30': {'title': '知识讲解 + 详细解析：GBR 与 non-GBR 承载', 'zh': '''
<h4><span class="st">知识讲解</span>承载是什么</h4>
<p>LTE 全 IP，用<b>EPS 承载</b>（bearer）把 IP 业务从 PDN 网关送到 UE：一个承载就是网关和 UE 之间一条<b>有确定 QoS 的 IP 分组流</b>，是一条逻辑连接（p.68）。每个承载都有一个 QCI 和一个 ARP（p.69）。按提供的 QoS 分两类，老师课上说记住这<b>两类</b>就行。</p>
<div class="tw"><table class="mini"><thead><tr><th></th><th>GBR 承载</th><th>non-GBR 承载</th></tr></thead><tbody>
<tr><td>速率保证</td><td>有最低保证速率 GBR</td><td>不保证任何速率</td></tr>
<tr><td>资源</td><td>建立（或修改）时永久分配专用资源</td><td>不永久分配</td></tr>
<tr><td>上限</td><td>资源富余时可超过 GBR，上限是 MBR</td><td>—</td></tr>
<tr><td>适合</td><td>VoIP、语音</td><td>网页浏览、FTP</td></tr></tbody></table></div>
<h4><span class="st">详细解析</span>答题要点</h4>
<ol><li><b>区别</b>：按上表三行写：保证不保证、资源是否永久分配、典型业务。GBR 提一句 MBR 更完整。</li>
<li><b>默认承载</b>（default bearer）：<b>必须是 non-GBR</b>，UE 一接入网络就建立，用于初始连接（p.70）。为什么：UE 刚开机还不知道要跑什么业务，不能一上来就永久占资源。</li>
<li><b>专用承载</b>（dedicated bearer）：可以是 GBR 也可以是 non-GBR，有新业务、QoS 要求不同时才建立。</li></ol>
<h4><span class="st">易错</span></h4>
<ul><li>GBR 不是"速率固定"：资源有富余时可以超过 GBR，最多到 MBR。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>A GBR bearer has a minimum guaranteed bit rate, for which dedicated transmission resources are permanently allocated at bearer establishment or modification; it is used for applications such as VoIP. A bit rate higher than the GBR may be allowed if resources are available, up to the maximum bit rate (MBR). A non-GBR bearer does not guarantee any particular bit rate and no bandwidth resources are allocated permanently; it is used for web browsing or FTP. The default bearer, created when the UE connects to the network, must be a non-GBR bearer; a dedicated bearer can be either GBR or non-GBR.</p></div>
<div class="ans">一句话：GBR 保证最低速率、永久占资源（VoIP），non-GBR 不保证（网页）；默认承载必须是 non-GBR。</div>
'''},

'b31': {'title': '知识讲解 + 详细解析：ARP 与 QCI 的分工', 'zh': '''
<h4><span class="st">知识讲解</span>每个承载两个 QoS 参数</h4>
<p><b>ARP</b>（Allocation and Retention Priority，分配与保持优先级，p.74）用于<b>呼叫接纳控制和抢占</b>：无线拥塞时决定新承载建不建；新承载请求来时决定能不能抢占别人；系统过载时决定先断哪些连接，保住高优先级连接。承载建立成功后，ARP <b>不再影响</b>分组转发。</p>
<p><b>QCI</b>（QoS Class Identifier，p.71–73）由优先级、分组时延预算、可接受丢包率刻画，决定 eNodeB 怎么处理分组：调度、队列管理、限速策略和 RLC 模式；丢包要求严的承载用 RLC 确认模式（AM）。转发处理由 QCI、GBR、MBR 决定。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A</b>：错，正好是讲义说 ARP <b>不管</b>的事，那是 QCI、GBR、MBR 的职责。</li>
<li><b>B</b>：对，p.74 的三条：接纳、抢占、过载时断谁。</li>
<li><b>C</b>：错，调制方式属于链路自适应（p.75 列为开放问题），与 ARP 无关。</li>
<li><b>D</b>：错，RLC 模式由 QCI 决定（p.73）。</li></ul>
<p><b>记忆</b>：ARP 管"门口"（进不进、踢谁走），QCI 管"路上"（怎么排队、怎么送）。</p>
<div class="ans">一句话：选 B：ARP 决定拥塞时接不接纳、能否抢占、过载先断谁；建好后转发看 QCI。</div>
'''},

# ======================= IoT =======================
'b32': {'title': '知识讲解 + 详细解析：IoT 五大挑战', 'zh': '''
<h4><span class="st">知识讲解</span>IoT 难在哪</h4>
<p>物联网（Internet of Things, IoT）就是把原来不联网的物体连起来，让它们能和人、和其他物体通信交互（p.78）。设备一多、数据一多、标准一多，就带来五个挑战（p.82–83）。这一题 <b>2025-26 S1 Q4(b)</b> 期末考过。</p>
<h4><span class="st">详细解析</span>五点，每点"是什么 + 为什么难"</h4>
<ol><li><b>可扩展性</b>（Scalability）：规模要扩到数以百万计的设备，整个系统怎么支撑是关键问题；网络层可以靠 IPv6 给设备分配海量地址。</li>
<li><b>安全</b>（Security）：越来越多的"物"互相连接，攻击面大大扩大；一个设备被黑，它的连接就成了问题，被攻破的设备可以当跳板攻击其他设备和系统。</li>
<li><b>隐私</b>（Privacy）：传感器越来越多，采到的数据很多和具体的人及其活动有关，可能含敏感信息和凭据；数据怎么保护、要不要共享、和谁共享是关键问题。</li>
<li><b>大数据与分析</b>（Big data and analysis）：海量传感器带来数据洪流；难点是要及时处理来自不同来源、不同格式的海量数据，才能得到有价值的信息。</li>
<li><b>互操作性</b>（Interoperability）：各种协议和架构争夺市场和标准，有的专有、有的开放；新标准能缓解，但实现方式仍然很多。</li></ol>
<h4><span class="st">易错</span></h4>
<ul><li>"大数据与分析"算一点，不要拆成两点再漏掉互操作性。</li>
<li>每点要写一句解释，只列五个名词拿不全分。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(1) Scalability: the IoT may grow to millions of devices, and how the overall system supports such a huge number of devices is a critical issue; IPv6 can provide the addresses. (2) Security: the threat surface is greatly expanded, and a compromised device can serve as a launching point to attack other devices and systems. (3) Privacy: much of the sensed data is specific to individuals and their activities and may contain sensitive information; how it is protected and with whom it is shared is critical. (4) Big data and analysis: the deluge of data from many sources in various forms must be evaluated in a timely and efficient manner. (5) Interoperability: various proprietary and open protocols and architectures compete for market share and standardization.</p></div>
<div class="ans">一句话：IoT 五大挑战：可扩展性、安全、隐私、大数据与分析、互操作性。</div>
'''},

'b33': {'title': '知识讲解 + 详细解析：IoTWF 参考架构几层', 'zh': '''
<h4><span class="st">知识讲解</span>两个标准 + 一个简化框架（p.84–86）</h4>
<div class="tw"><table class="mini"><thead><tr><th>架构</th><th>谁提出、何时</th><th>特点</th></tr></thead><tbody>
<tr><td>oneM2M</td><td>ETSI 的 M2M 技术委员会，2012</td><td>目标是一个公共服务层</td></tr>
<tr><td>IoTWF</td><td>IoT World Forum 架构委员会，2014</td><td><b>7 层</b>参考模型，含边缘计算、数据存储和访问；数据从边缘往上流到中心</td></tr>
<tr><td>简化框架（讲义采用）</td><td>Cisco 教材</td><td>两个并行的三层栈：核心 IoT 功能栈 + 数据管理与计算栈</td></tr></tbody></table></div>
<p>老师课上说学习时用简化框架，比另外两个标准好理解。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. 3 层</b>：错，3 层是简化框架里每个栈的层数。</li>
<li><b>B. 5 层</b>：错，那是传感器网络协议栈的层数（p.59），别串。</li>
<li><b>C. 7 层</b>：对，p.85 "seven-layer IoT architectural reference model"。</li>
<li><b>D. 两个三层栈</b>：错，这是讲义的简化框架，不是 IoTWF。</li></ul>
<p>课外补充：IoTWF 七层自下而上是物理设备与控制器、连接、边缘（雾）计算、数据积累、数据抽象、应用、协作与流程。</p>
<div class="ans">一句话：选 C：IoTWF 是 7 层；讲义的简化框架才是两个三层栈。</div>
'''},

'b34': {'title': '知识讲解 + 详细解析：核心功能栈与四子层', 'zh': '''
<h4><span class="st">知识讲解</span>核心 IoT 功能栈（p.88–90）</h4>
<p>简化框架有两个并行栈，这题问的是<b>核心 IoT 功能栈</b>（Core IoT Functional Stack），它描述"物"怎么把信息送到应用：</p>
<ol><li><b>"物"层</b>（Things：传感器和执行器）：物理设备，既要适应部署环境的限制，又要提供所需信息。</li>
<li><b>通信网络层</b>（Communications network layer）：智能物体不能自给自足时，要和外部系统通信，分四个子层。</li>
<li><b>应用与分析层</b>（Application and analytics layer）：处理采集的数据，必要时控制智能物体，并据此做智能决策。</li></ol>
<p>这一部分是期末高频题：<b>2024-25 S2 Q4(b)</b> 和 <b>2025-26 S2 Q4(d)</b> 两次考了通信网络层的四个子层，2023-24 S2 Q4(a) 要求描述两个并行栈。</p>
<h4><span class="st">详细解析</span>通信网络层的四个子层，自下而上</h4>
<div class="tw"><table class="mini"><thead><tr><th>子层</th><th>做什么</th><th>例子</th></tr></thead><tbody>
<tr><td>接入网</td><td>IoT 网络的"最后一公里"</td><td>802.11ah、802.15.4g、LoRa</td></tr>
<tr><td>网关与回程</td><td>把一片区域的智能物体汇聚到公共网关，再经更远距离的介质送到中心站</td><td>网关通常固定</td></tr>
<tr><td>网络传输</td><td>网络层和传输层协议，要开放、标准、可扩展、安全</td><td>IP、UDP/TCP</td></tr>
<tr><td>IoT 网络管理</td><td>让中心应用和传感器交换数据的应用协议</td><td>HTTP、WebSocket</td></tr></tbody></table></div>
<p><b>记忆</b>："接入 → 汇聚回传 → 传输（IP）→ 管理（应用协议）"。</p>
<h4><span class="st">易错</span></h4>
<ul><li>网络传输子层是 IP/UDP/TCP，网络管理子层是 HTTP/WebSocket，别放反。</li>
<li>"三层"问的是功能栈，不是数据管理与计算栈（边缘 / 雾 / 云）。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>The Core IoT Functional Stack has three layers: (1) the "things" layer of sensors and actuators; (2) the communications network layer; (3) the application and analytics layer. The communications network layer is divided into four sublayers: (a) the access network sublayer, the last mile of the IoT network, typically wireless technologies such as IEEE 802.11ah, 802.15.4g and LoRa; (b) the gateways and backhaul network sublayer, where smart objects in an area are organized around a common gateway that forwards the collected information over a longer-range medium to a headend station; (c) the network transport sublayer, which implements network and transport protocols such as IP, UDP and TCP; (d) the IoT network management sublayer, which uses application protocols such as HTTP and WebSocket so that headend applications can exchange data with the sensors.</p></div>
<div class="ans">一句话：三层 = 物、通信网络、应用与分析；通信网络层四子层 = 接入网、网关与回程、网络传输、IoT 网络管理。</div>
'''},

'b35': {'title': '知识讲解 + 详细解析：按距离分的网络', 'zh': '''
<h4><span class="st">知识讲解</span>按通信距离分档（p.95）</h4>
<p>选 IoT 接入技术的第一个参数是智能物体和信息采集器之间的距离。讲义按场景分档：</p>
<div class="tw"><table class="mini"><thead><tr><th>类别</th><th>范围</th><th>例子</th></tr></thead><tbody>
<tr><td>PAN 个域网</td><td>几米</td><td>蓝牙</td></tr>
<tr><td>HAN 家庭网</td><td>几十米</td><td>ZigBee、BLE</td></tr>
<tr><td>NAN 邻域网</td><td>几百米</td><td>802.11 mesh</td></tr>
<tr><td>FAN 场域网</td><td>几十到几百米，户外开阔区</td><td>—</td></tr>
<tr><td>LAN</td><td>约 100 m</td><td>802.11</td></tr>
<tr><td>MAN / WAN</td><td>几公里 / 超过几公里</td><td>—</td></tr></tbody></table></div>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. PAN</b>：错，讲义 PAN 的例子是经典蓝牙；BLE 被放在 HAN。</li>
<li><b>B. HAN</b>：对，p.95 原文 "such as ZigBee and Bluetooth Low Energy (BLE)"。</li>
<li><b>C. NAN</b>：错，NAN 的例子是 802.11 mesh。</li>
<li><b>D. WAN</b>：错，ZigBee、BLE 都是短距、低功耗技术。</li></ul>
<p><b>易错</b>：蓝牙（PAN）和 BLE（HAN）在讲义里分在不同档，别因为都叫蓝牙就选 A。</p>
<div class="ans">一句话：选 B：ZigBee 和 BLE 属于 HAN，几十米。</div>
'''},

'b36': {'title': '知识讲解 + 详细解析：选接入技术看什么', 'zh': '''
<h4><span class="st">知识讲解</span>三个决定因素（p.95–96）</h4>
<ol><li><b>通信距离</b>：智能物体到信息采集器有多远，决定选哪一档（PAN、HAN……）。</li>
<li><b>单个采集小区里的目标设备数量</b>：结合传输距离和所需吞吐量，这个参数决定<b>小区大小</b>。</li>
<li><b>技术成本</b>。</li></ol>
<p>通常要把成本、距离、功耗和可用带宽综合考虑。这些都是"网络能不能连上、连多少、花多少"的问题。</p>
<h4><span class="st">逐项分析</span>（本题找"不包括"的一项）</h4>
<ul><li><b>A. 通信距离</b>：包括，第一因素。</li>
<li><b>B. 设备数量</b>：包括，第二因素。</li>
<li><b>C. 技术成本</b>：包括，第三因素。</li>
<li><b>D. 屏幕分辨率</b>：<b>不包括，是答案</b>。大多数传感器根本没有屏幕，这是终端显示属性，与接入网络无关。</li></ul>
<p><b>记忆</b>：远不远、多不多、贵不贵。</p>
<div class="ans">一句话：选 D：前三个因素是距离、单小区设备数量、成本，屏幕分辨率无关。</div>
'''},

'b37': {'title': '知识讲解 + 详细解析：为什么需要雾计算', 'zh': '''
<h4><span class="st">知识讲解</span>全送云端的好处和问题</h4>
<p>最自然的做法是把数据全送到云端集中处理，好处是简单：物体只要连上一个中心应用，它能看到所有节点、做所有分析（p.103）。但 IoT 数据量太大，带宽管理成问题：网络要扛得住流量，服务器要吞得下、存得下、算得动（p.104）。</p>
<h4><span class="st">详细解析</span>第一问：五个问题（p.105）</h4>
<ol><li><b>最后一公里带宽很小</b>：接入网多是低功耗无线，传不了海量原始数据。</li>
<li><b>时延大</b>：来回一趟云端，做不到实时响应。</li>
<li><b>回程不可靠</b>：网关的回程常靠 3G/LTE 甚至卫星。</li>
<li><b>回程上数据量太大</b>，处理不过来。</li>
<li><b>大数据越来越大</b>：实时分析和响应几乎不可能。</li></ol>
<h4><span class="st">详细解析</span>第二问：雾计算怎么解决（p.106–108）</h4>
<ul><li><b>思路</b>：把数据管理分布到整个 IoT 系统里，尽量靠近 IP 网络的边缘。任何有计算、存储和联网能力的设备都可以当雾节点（fog node），多了一个"雾层"。</li>
<li><b>好处</b>：在数据产生处附近分析 → 时延最小；把大量流量从核心网卸掉；敏感数据留在本地网络。</li>
<li><b>还有</b>：雾节点离传感器近，有上下文感知，能更快对事件作反应，形成分布式的边缘控制回路；上传前先做数据精简（p.108）。</li></ul>
<p>老师课上强调雾计算的好处：分布式处理，不用等中心服务器，所以快；上传前先精简数据；能实时处理。</p>
<h4><span class="st">易错</span></h4>
<ul><li>雾计算<b>不取代</b>云，二者互补（p.111）；别写成"不用云了"。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Sending all IoT data to the cloud is a problem because: the bandwidth of last-mile IoT networks is very limited; latency can be very high, so real-time response is lost; the backhaul from the gateway can be unreliable, often depending on 3G/LTE or even satellite links; the volume of data on the backhaul is too high; and big data keeps growing, making real-time analysis almost impossible.</p>
<p>Fog computing distributes data management throughout the IoT system, as close to the network edge as possible. Any device with computing, storage and network connectivity can be a fog node. Analysing data close to where it is collected minimizes latency, offloads network traffic from the core network and keeps sensitive data inside the local network; the fog node is aware of the context of its sensors and can react to events quickly, and the data is reduced before being sent upstream.</p></div>
<div class="ans">一句话：全送云端会遇到带宽小、时延大、回程不可靠、数据太多；雾计算在边缘附近处理，降时延、减流量、数据留本地。</div>
'''},

'b38': {'title': '知识讲解 + 详细解析：雾计算五个特点', 'zh': '''
<h4><span class="st">知识讲解</span>雾节点在哪、干什么</h4>
<p>雾节点是放在 IoT 终端附近的、有计算存储联网能力的设备（常见在网关、路由器里），在数据送到云之前先处理一遍（p.106）。讲义 p.109 把它的特点总结成五条。这一题 <b>2025-26 S1 Q4(c)</b> 期末考过。</p>
<h4><span class="st">详细解析</span>五条，每条说清"为什么"</h4>
<ol><li><b>上下文位置感知、低时延</b>（contextual location awareness and low latency）：雾节点尽量靠近 IoT 终端，知道自己管的是哪些传感器，就近处理所以快。</li>
<li><b>地理上分布</b>（geographic distribution）：雾节点服务的业务和应用需要大范围分散部署。</li>
<li><b>部署在大量 IoT 终端附近</b>（deployment near IoT endpoints）：通常有大量终端的地方才放雾节点。</li>
<li><b>雾与终端之间用无线通信</b>（wireless communication）：一个雾节点要连大量终端，无线接入最容易扩展。</li>
<li><b>用于实时交互</b>（use for real-time interactions）：在雾节点上先做预处理，上层应用只需对一部分数据做批处理。</li></ol>
<p>老师课上强调的四个好处（快、先精简数据、实时、无线连接）都能对应到这五条里。</p>
<h4><span class="st">易错</span></h4>
<ul><li>"特点"和"雾计算要解决的问题"（b37）不是一回事，别答成带宽小、时延大那一组。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(1) Contextual location awareness and low latency: the fog node sits as close to the IoT endpoints as possible to deliver distributed computing. (2) Geographic distribution: the services and applications targeted by fog nodes demand widely distributed deployments. (3) Deployment near IoT endpoints: fog nodes are typically deployed in the presence of a large number of IoT endpoints. (4) Wireless communication between the fog and the IoT endpoints: since a fog node deals with a large number of endpoints, wireless access is the easiest way to achieve scalability. (5) Use for real-time interactions: pre-processing at the fog nodes allows upper-layer applications to perform batch processing on only a subset of the data.</p></div>
<div class="ans">一句话：雾计算五特点：位置感知低时延、地理分布、靠近大量终端、与终端无线连接、用于实时交互。</div>
'''},

'b39': {'title': '知识讲解 + 详细解析：边缘、雾、云的分工', 'zh': '''
<h4><span class="st">知识讲解</span>按时间敏感度分层（p.110–113）</h4>
<p>边缘（mist / edge）计算：把雾再往前推，直接放进 IoT 终端设备本身，有算力的终端自己做初步分析和过滤（p.110）。边缘、雾、云<b>互补</b>而不是互相取代（p.111）：边缘和雾是第一道防线，过滤和分析数据，免得每个事件都去问云。数据去哪处理，看它<b>多急</b>（p.113）：</p>
<div class="tw"><table class="mini"><thead><tr><th>时间敏感度</th><th>送到哪里</th></tr></thead><tbody>
<tr><td>最敏感</td><td>边缘或离设备最近的雾节点</td></tr>
<tr><td>可以等几秒到几分钟</td><td>汇聚节点（aggregation node）</td></tr>
<tr><td>不敏感</td><td>云：历史分析、大数据分析、长期存储</td></tr></tbody></table></div>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A. 边缘节点</b>：错，留给最紧急的数据。</li>
<li><b>B. 最近的雾节点</b>：错，同样是给最紧急的数据。</li>
<li><b>C. 汇聚节点</b>：对，p.113 原文 "seconds or minutes … aggregation node"。</li>
<li><b>D. 云端</b>：错，云处理的是不在乎时间的历史数据。</li></ul>
<p><b>记忆</b>：越急越靠近设备：毫秒级在边缘 / 雾，秒到分钟在汇聚，不急的上云。</p>
<div class="ans">一句话：选 C：能等几秒到几分钟的数据送汇聚节点。</div>
'''},
}

NOTES = '''b16: slide p.39 says EDCA has "eight traffic classes"; the 802.11e standard maps 8 user priorities to 4 access categories. Box keeps the slide answer (8) and gives the standard as 课外补充 (known, as instructed).
b1/b35: slides are internally inconsistent: p.6 gives WLAN coverage 50-500 m, p.95 gives LAN (IEEE 802.11) "up to 100 ms" (typo for 100 m). Box answers with p.6 and points out the difference.
No errors found in the existing b1-b39 solutions.'''
