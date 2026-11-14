# -*- coding: utf-8 -*-
# 知识讲解 + 详细解析 for Part C (satellite) practice questions c1 … c23.
# Source questions: src/p2build/bc_questions.py; slides: EE6129_text/partC.txt; numbers checked by check_bcC.py.
XPL = {

# ---------------------------------------------------------------- 轨道
'c1': {'title': '知识讲解 + 详细解析：三类轨道的高度', 'zh': '''<h4><span class="st">知识讲解</span>高度决定一切</h4>
<p>卫星按高度分三类（讲义 Part C p.10）：<b>GEO</b>（地球静止轨道，Geostationary Earth Orbit）35,863 km；<b>MEO</b>（中轨，Medium Earth Orbit）8,000–18,000 km；<b>LEO</b>（低轨，Low Earth Orbit）500–1,500 km。越高，看到的地面越大、绕一圈越慢，但信号越弱、时延越大。GPS 用的是 24 颗 MEO（p.9）。老师课上强调：GEO 离地约 36,000 km，所以地面站必须用高增益天线。</p>
<h4><span class="st">逐项分析</span>四个选项</h4>
<ul><li><b>A 对</b>：三个数字和 p.10 完全一致。</li>
<li><b>B 错</b>：GEO 只有一个高度 35,863 km；20,000 km 比讲义给的 MEO 范围（8,000–18,000 km）还高一点（课外补充：GPS 卫星约 20,200 km，通常也归为 MEO）；100 km 太低，大气阻力会让卫星很快掉下来。</li>
<li><b>C 错</b>：GEO 对，但 MEO、LEO 的范围都写低了；讲义 LEO 下限是 500 km。</li>
<li><b>D 错</b>：42,000 km 是 GEO 到<b>地心</b>的轨道半径（6,370 + 35,863 = 42,233 km），不是离地高度。</li></ul>
<h4><span class="st">记忆</span>口诀</h4>
<p>"低一千、中一万、静止三万六"：LEO 约 1,000 km 量级，MEO 约 10,000 km 量级，GEO 约 36,000 km。</p>
<div class="ans">一句话：GEO 35,863 km，MEO 8,000–18,000 km，LEO 500–1,500 km，选 A；42,000 km 是轨道半径，别混。</div>'''},

'c2': {'title': '知识讲解 + 详细解析：轨道按形状和倾角分类', 'zh': '''<h4><span class="st">知识讲解</span>描述一条轨道的三个维度</h4>
<p>讲义 Part C p.10–11 用三个维度描述卫星轨道：<b>高度</b>（GEO / MEO / LEO，见 c1）、<b>形状</b>（shape）和<b>倾角</b>（inclination）。本题问后两个。</p>
<div class="tw"><table class="mini"><thead><tr><th>维度</th><th>分类</th><th>要点</th></tr></thead><tbody>
<tr><td>形状</td><td>圆轨道（circular）</td><td>圆心在地心，高度不变</td></tr>
<tr><td>形状</td><td>椭圆轨道（elliptical）</td><td>地心在椭圆的<b>一个焦点</b>上，高度时高时低</td></tr>
<tr><td>倾角</td><td>赤道轨道（equatorial）</td><td>轨道面就是赤道面</td></tr>
<tr><td>倾角</td><td>极轨道（polar）</td><td>经过南北两极</td></tr>
<tr><td>倾角</td><td>倾斜轨道（inclined）</td><td>其他所有倾角</td></tr></tbody></table></div>
<h4><span class="st">详细解析</span>为什么这样分</h4>
<ol><li><b>形状</b>决定卫星离地距离是否变化：圆轨道上信号损耗、时延都稳定；椭圆轨道在远地点走得慢，可以在某地区上空停留较久。</li>
<li><b>倾角</b>决定卫星能飞过哪些纬度：赤道轨道永远只在赤道上空，高纬度地区仰角很低；极轨道每圈都经过两极，地球在下面自转，几圈下来可以扫过全球。</li>
<li>GEO = 圆轨道 + 赤道轨道 + 35,863 km，三个条件缺一不可，否则卫星相对地面不会"静止"（p.15）。</li></ol>
<h4><span class="st">课外补充</span>（讲义没有）</h4>
<p>极轨道常用于对地成像、气象卫星；高倾角椭圆轨道（如俄罗斯的 Molniya 轨道）用来照顾 GEO 覆盖不好的高纬度地区。</p>
<h4><span class="st">易错</span></h4>
<ul><li>椭圆轨道是"一个焦点在地心"，不是"中心在地心"。</li>
<li>倾斜轨道是"除赤道、极轨道以外的其他轨道"，不要只答两类。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>By shape: (1) circular orbit, with the centre of the circle at the earth's centre; (2) elliptical orbit, with one focus at the earth's centre. By inclination: (1) equatorial orbit, directly above the earth's equator; (2) polar orbit, passing over both poles; (3) all other orbits are called inclined orbits. (A GEO satellite uses a circular equatorial orbit at 35,863 km.)</p></div>
<div class="ans">一句话：形状分圆（圆心在地心）和椭圆（一个焦点在地心）；倾角分赤道、极轨道和倾斜轨道。</div>'''},

'c3': {'title': '知识讲解 + 详细解析：仰角与覆盖角', 'zh': '''<h4><span class="st">知识讲解</span>两个角度定位卫星</h4>
<p>讲义 Part C p.12–13：卫星在天空中的位置用两个角度描述。</p>
<ul><li><b>仰角 θ（elevation angle）</b>：站在地面站，从<b>水平线</b>（地表在天线处的切线）抬头到天线主瓣中心（天线正对卫星）的夹角。θ = 90° 是正头顶，θ = 0° 是贴着地平线。</li>
<li><b>覆盖角 β（coverage angle）</b>：在<b>最小仰角</b>下，卫星能看到的那部分地球表面有多大，用地心处张开的角度表示。</li></ul>
<p>两者的关系（由 p.13 的几何图推出，讲义没写公式）：cos(θ + β) = R·cos θ / (R + h)，R 是地球半径，h 是卫星高度。最小仰角 θ 越小，β 越大。</p>
<h4><span class="st">详细解析</span>答题要点逐条展开</h4>
<ol><li><b>仰角</b>：要说清"从哪里量到哪里"——从地面站处的地表切线量到天线指向卫星的主瓣中心。只写"天线抬起的角度"会丢分。</li>
<li><b>覆盖角</b>：关键词是"在最小仰角下卫星可见的地表部分"。</li>
<li><b>理想最小仰角 = 0°</b>：仰角下限放到 0°，离星下点很远的地面站也能看到卫星，覆盖一直延伸到卫星的<b>光学地平线</b>（optical horizon），覆盖最大（p.12）。</li>
<li><b>实际不用 0°</b>：仰角越低，信号穿过的大气越厚，雨、雾、大气吸收都大增（p.21、p.23），所以实际取 5°–10°。</li></ol>
<div class="calc">GEO，θ = 0°：cos β = 6370 / 42233 = 0.1508 → β = 81.3°<br>GEO，θ = 10°：cos(θ + β) = 6370 × 0.9848 / 42233 = 0.1485 → θ + β = 81.46° → β = 71.46°<br>覆盖直径 ≈ 2βR：0° 时约 18,000 km，10° 时约 15,900 km（≈ 讲义 p.14 表里的 16,000 km）</div>
<h4><span class="st">易错</span></h4>
<ul><li>仰角在<b>地面站</b>处量，覆盖角在<b>地心</b>处量，别画错位置。</li>
<li>"理想 0°"是为了覆盖最大，不代表实际最好；两句都要写，体现权衡。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Elevation angle θ is the angle from the horizontal (the line tangent to the earth's surface at the antenna's location) to the centre of the antenna's main beam when the antenna points directly at the satellite. Coverage angle β is the measure of the portion of the earth's surface visible to the satellite with the minimum elevation angle. To obtain maximum coverage, a minimum elevation angle of 0° is preferred, so that the coverage extends to the satellite's optical horizon in all directions. In practice a few degrees (e.g. 5°–10°) is used, because at low elevation the signal passes through more atmosphere and suffers larger attenuation.</p></div>
<div class="ans">一句话：仰角在地面站量（切线到卫星方向），覆盖角在地心量（最小仰角下可见的地表）；理想最小仰角 0°，覆盖到光学地平线。</div>'''},

'c4': {'title': '知识讲解 + 详细解析：GEO 传播时延', 'zh': '''<h4><span class="st">知识讲解</span>时延 = 路程 ÷ 光速</h4>
<p>无线电波在真空中以光速 c = 3×10⁸ m/s = 300,000 km/s 传播。传播时延 t = d / c。卫星通信里，信号从一个地面站<b>上行</b>到卫星，卫星转发后再<b>下行</b>到另一个地面站，所以路程是"上 + 下"两段。讲义 Part C p.16：两地都在卫星正下方时，"round-trip propagation delay"是 0.24 s；p.14 表里 GEO 往返时延约 250 ms。这里的"往返"指<b>经卫星走一趟（地 → 星 → 地）</b>。</p>
<h4><span class="st">详细解析</span>一步一步算</h4>
<ol><li>做什么：求路程。为什么：两站都在卫星正下方附近，斜距 ≈ 高度 h。</li>
<li>做什么：除以光速。注意单位统一用 km 和 km/s。</li></ol>
<div class="calc">d = 2 × 35,863 km = 71,726 km<br>t = 71,726 km ÷ 300,000 km/s = 0.239 s ≈ 0.24 s</div>
<p><b>合理性检查</b>：和讲义 p.16 的 0.24 s 一致。如果地面站在覆盖边缘（仰角 10°），斜距约 40,660 km，一趟约 0.27 s，所以表里写"约 250 ms"是个典型值。打电话"一问一答"要经过卫星两趟，约 0.48 s，能明显感觉到停顿。</p>
<h4><span class="st">易错</span></h4>
<ul><li>只算单程 35,863 km 得 0.12 s：漏了下行那一段。</li>
<li>把 "round trip" 理解成对话一来一回再乘 2 得 0.48 s：讲义的 0.24 s 指地 → 星 → 地一趟。</li>
<li>km 和 m 混用，差 1000 倍。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Path length = uplink + downlink = 2 × 35,863 km = 71,726 km. Propagation delay t = d / c = 71,726 km / (3 × 10⁵ km/s) ≈ 0.239 s ≈ 0.24 s.</p></div>
<div class="ans">一句话：上行 + 下行共 71,726 km，除以 3×10⁵ km/s，约 0.239 s。</div>'''},

'c5': {'title': '知识讲解 + 详细解析：GEO 覆盖角', 'zh': '''<h4><span class="st">知识讲解</span>从 p.13 的几何图出发（课外补充）</h4>
<p>讲义 Part C p.13 只画了图，公式是本题补充的。画三角形 O–E–S：O 是地心，E 是地面站，S 是卫星。OE = R（地球半径），OS = R + h。仰角 θ = 0° 时，地面站看卫星的视线正好贴着地表，<b>和半径 OE 垂直</b>，所以三角形在 E 处是直角。直角三角形里，β 的邻边是 R，斜边是 R + h：</p>
<div class="calc">cos β = R / (R + h)</div>
<p>一般仰角时公式是 cos(θ + β) = R·cos θ / (R + h)，θ = 0° 时就退化成上式。</p>
<h4><span class="st">详细解析</span>一步一步算</h4>
<ol><li>求 R + h：卫星到地心的距离。</li>
<li>求 cos β，再用计算器 cos⁻¹（注意计算器在 DEG 模式）。</li>
<li>换成地面直径：弧长 = 半径 × 角度（弧度），覆盖区直径 = 2βR。</li></ol>
<div class="calc">R + h = 6,370 + 35,863 = 42,233 km<br>cos β = 6,370 / 42,233 = 0.1508<br>β = cos⁻¹ 0.1508 = 81.3°<br>直径 ≈ 2 × (81.3° × π/180) × 6,370 = 2 × 1.419 × 6,370 ≈ 18,000 km</div>
<p><b>合理性检查</b>：β 必须小于 90°（卫星不可能看到半个地球以上），81.3° 合理。讲义 p.14 表里 GEO 覆盖直径约 16,000 km，是按最小仰角 10° 算的（β = 71.46°，直径约 15,900 km），两个数不矛盾。</p>
<h4><span class="st">课外补充</span>"1/4 个地球"从哪来</h4>
<p>讲义 p.15 说一颗 GEO 覆盖 "¼ of the earth"。按几何，可见的球冠面积占地球表面 (1 − cos β)/2：仰角 0° 时约 42%，仰角 10° 时约 34%（这就是常说的"约 1/3"）。讲义的 1/4 是偏保守的说法，考试照讲义写即可。三颗相隔 120° 的 GEO 拼起来覆盖除两极外的几乎全球（p.15）。</p>
<h4><span class="st">易错</span></h4>
<ul><li>用 cos β = R / h（忘了加 R）：得到 cos β = 0.178，β 偏小。</li>
<li>计算器在 RAD 模式，cos⁻¹ 得 1.419 却当成度。</li>
<li>直径用 β 的度数直接乘 R，没换成弧度。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>At 0° elevation the line of sight is tangent to the earth, so it is perpendicular to the earth radius at the earth station. Hence cos β = R / (R + h) = 6,370 / (6,370 + 35,863) = 0.1508, giving β ≈ 81.3°. The coverage diameter on the ground is about 2βR ≈ 18,000 km.</p></div>
<div class="ans">一句话：仰角 0° 时视线垂直于半径，cos β = 6370/42233 = 0.1508，β ≈ 81.3°，覆盖直径约 18,000 km。</div>'''},

'c6': {'title': '知识讲解 + 详细解析：GEO 的优缺点', 'zh': '''<h4><span class="st">知识讲解</span>GEO 为什么"静止"</h4>
<p>GEO 在赤道上空 35,863 km 的圆轨道上，转速和地球自转一样，看上去始终停在赤道某点正上方（讲义 Part C p.15）。优点（p.15）：相对地面几乎不动，<b>多普勒频移</b>（Doppler shift）影响小；地面站<b>跟踪简单</b>；覆盖大，3 颗相隔 120° 就几乎覆盖全球。缺点（p.16）：信号走 35,000 多公里后很弱；<b>极地和高纬度地区服务差</b>；时延大（往返 0.24 s）；大波束做点对点通信浪费频谱。</p>
<h4><span class="st">逐项分析</span>找"不是特点"的那项</h4>
<ul><li><b>A 是特点</b>：卫星相对地面不动，天线对准后基本不用动。</li>
<li><b>B 是特点</b>：没有相对运动，就几乎没有多普勒频移。</li>
<li><b>C 是特点</b>：p.14 表里 GEO 往返时延约 250 ms（p.16 写 0.24 s）。</li>
<li><b>D 不是特点，选它</b>：GEO 在赤道上空，越往两极，地面站看卫星的仰角越低，信号穿过的大气越厚，甚至看不到卫星。所以高纬度覆盖<b>差</b>，是缺点。</li></ul>
<h4><span class="st">记忆</span></h4>
<p>"赤道上的灯泡"：照赤道附近亮，照两极几乎贴着地平线，照不到。</p>
<div class="ans">一句话：GEO 在赤道上空，极地和高纬度仰角太低、覆盖差，所以 D 不是它的特点。</div>'''},

'c7': {'title': '知识讲解 + 详细解析：LEO 的问题、优点与分类', 'zh': '''<h4><span class="st">知识讲解</span>LEO 为什么又好又麻烦</h4>
<p>LEO 只有 500–1,500 km 高，离地近，所以<b>信号强、时延小</b>；但离地近也意味着<b>飞得快</b>（约 7 km/s，1.5–2 小时绕一圈）、<b>一颗只能看到 15–20 分钟</b>（讲义 Part C p.14），所以要一大群卫星接力。讲义 p.17 讲问题，p.18 讲优点，p.19 讲 Little / Big LEO。</p>
<h4><span class="st">详细解析</span>答案要点逐条展开</h4>
<p><b>问题（p.17）</b></p>
<ol><li><b>多普勒频移大</b>：卫星相对地面高速运动，收到的频率会偏移，接收机必须跟踪。课外估算：1,000 km 高的 LEO 速度约 7.35 km/s，2 GHz 载频最大偏移 f·v/c ≈ 49 kHz，远大于地面手机的几百 Hz。</li>
<li><b>大气阻力</b>（atmospheric drag）明显，轨道逐渐衰退，卫星寿命有限。</li>
<li>要<b>多个轨道面、每面多颗卫星</b>才能连续覆盖。</li>
<li>两地通信常要把信号从一颗卫星<b>切换</b>到另一颗。</li></ol>
<p><b>优点（p.18）</b></p>
<ol><li>同样发射功率下，收到的信号<b>比 GEO 强得多</b>。课外估算：自由空间损耗只差距离项 20 log(35,863 / 1,000) ≈ 31 dB。</li>
<li>覆盖更局部，频谱可以在不同地区复用，更省频谱。</li>
<li>适合需要强信号的<b>手持 / 移动终端</b>。</li>
<li>代价：要 24 小时全覆盖需要很多颗卫星。</li></ol>
<div class="tw"><table class="mini"><thead><tr><th></th><th>Little LEO</th><th>Big LEO</th></tr></thead><tbody>
<tr><td>频率</td><td>1 GHz 以下</td><td>1 GHz 以上</td></tr>
<tr><td>带宽 / 速率</td><td>小于 5 MHz，最高 10 kbps</td><td>可达几 Mbps</td></tr>
<tr><td>业务</td><td>寻呼、跟踪、低速消息</td><td>Little LEO 全部业务 + 话音、定位</td></tr></tbody></table></div>
<h4><span class="st">易错</span></h4>
<ul><li>Little / Big 的分界是<b>频率 1 GHz</b>，不是卫星大小或高度。</li>
<li>Big LEO 是"在 Little LEO 的基础上<b>加上</b>话音和定位"，不是另一套业务。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Problems: (1) the satellite moves fast relative to the ground, so the system must cope with large Doppler shifts; (2) atmospheric drag is significant, causing gradual orbital deterioration; (3) multiple orbital planes, each with multiple satellites, are needed; (4) communication between two earth stations usually involves handing off from one satellite to another. Advantages: the received signal is much stronger than a GEO signal for the same transmit power; coverage is more localised so spectrum is better conserved; suitable for mobile and personal terminals. Little LEOs operate below 1 GHz with less than 5 MHz bandwidth and up to 10 kbps, for paging, tracking and low-rate messaging. Big LEOs operate above 1 GHz with data rates up to a few Mbps, offering the Little-LEO services plus voice and positioning.</p></div>
<div class="ans">一句话：LEO 近所以信号强、省频谱、适合手持，但多普勒大、有大气阻力、要很多卫星和频繁切换；Little LEO 在 1 GHz 以下、10 kbps，Big LEO 在 1 GHz 以上、几 Mbps 并加上话音和定位。</div>'''},

'c8': {'title': '知识讲解 + 详细解析：MEO 与 LEO 对比', 'zh': '''<h4><span class="st">知识讲解</span>MEO 是 LEO 和 GEO 之间的折中</h4>
<p>MEO 高 8,000–18,000 km（讲义 Part C p.10），每颗可见 2–8 小时，LEO 只有 15–20 分钟（p.14）。所以 MEO <b>切换少得多</b>；但离地更远，<b>传播时延和所需功率比 LEO 大</b>；需要的卫星数比 LEO 少（p.20）。用途：数字话音、数据、传真、消息；GPS 就是 24 颗 MEO（p.9）。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A 错</b>：正好反了。卫星越高，每颗看得越久，切换越少。</li>
<li><b>B 对</b>：和 p.20 原话一致："much fewer handoffs"，"propagation delay … and the power required are greater than those of LEOs"。</li>
<li><b>C 错</b>：MEO 更高，时延是几十 ms，LEO 只有几 ms（p.14）。</li>
<li><b>D 错</b>：GPS 正是 MEO 导航系统。</li></ul>
<h4><span class="st">记忆</span></h4>
<p>"越高越稳、越高越远"：高度往上走，切换少、卫星少（稳）；时延和功率大（远）。</p>
<div class="ans">一句话：MEO 比 LEO 切换少得多，但时延和所需功率更大，选 B。</div>'''},

'c9': {'title': '知识讲解 + 详细解析：LEO 每次可见时长', 'zh': '''<h4><span class="st">知识讲解</span>讲义 p.14 的轨道参数表</h4>
<div class="tw"><table class="mini"><thead><tr><th>参数</th><th>LEO</th><th>MEO</th><th>GEO</th></tr></thead><tbody>
<tr><td>周期</td><td>1.5–2 h</td><td>5–10 h</td><td>24 h</td></tr>
<tr><td>每次可见</td><td>15–20 min</td><td>2–8 h</td><td>永久</td></tr>
<tr><td>往返时延</td><td>几 ms</td><td>几十 ms</td><td>约 250 ms</td></tr>
<tr><td>覆盖直径（仰角 10°）</td><td>约 6,000 km</td><td>12,000–15,000 km</td><td>约 16,000 km</td></tr></tbody></table></div>
<p>为什么 LEO 只能看 15–20 分钟？课外补充：由开普勒第三定律 T = 2π√(a³/μ)，500 km 高的 LEO 周期约 1.57 h、速度约 7.6 km/s。一圈 90 多分钟，每次从地平线升起到落下只占其中一小段，所以每次可见十几分钟。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A 对</b>：表中 LEO 一行。</li>
<li><b>B 错</b>：2–8 小时是 MEO。</li>
<li><b>C 错</b>：一直可见的是 GEO（永久可见）。</li>
<li><b>D 错</b>：几秒太短，LEO 再快也要十几分钟才飞过天空。</li></ul>
<div class="ans">一句话：LEO 每次过顶约 15–20 分钟（MEO 2–8 小时，GEO 永久），选 A。</div>'''},

# ---------------------------------------------------------------- 链路
'c10': {'title': '知识讲解 + 详细解析：链路质量三大因素', 'zh': '''<h4><span class="st">知识讲解</span>信号在路上损失在哪</h4>
<p>讲义 Part C p.21–23 列出影响卫星链路性能的三大因素。老师课上强调：这三个因素非常重要，他"必须强调"。思路就是从卫星天线到地面站天线，信号沿路被"削弱"的三个原因：<b>距离</b>、<b>偏离波束中心</b>、<b>大气</b>。</p>
<h4><span class="st">详细解析</span>三个因素逐条展开</h4>
<ol><li><b>卫星天线和地面站天线之间的距离</b>：自由空间损耗 L(dB) = 32.44 + 20 log f(MHz) + 20 log d(km)。所以<b>频率越高、卫星越高，损耗越大</b>（p.21，p.22 的图）。课外举例：同一颗 GEO，Ku 12 GHz 比 C 4 GHz 多损耗 20 log 3 ≈ 9.5 dB；GEO 比 1,000 km 的 LEO 多损耗约 31 dB。</li>
<li><b>下行时地面站离卫星"瞄准点"（aim point）的地面距离</b>：卫星波束对准地面某一点，覆盖区<b>中心功率最高</b>，越往边缘越弱。所以同一颗卫星，覆盖边缘的用户需要更大的天线。</li>
<li><b>大气衰减</b>：受氧气、水汽、仰角和频率影响。<b>仰角越小，信号穿过的大气越厚</b>，衰减越大；频率越高越严重（p.21、p.23）。课外：仰角 5° 时穿过大气的路程约为 30° 时的 5.7 倍（按 1/sin θ 估算）。</li></ol>
<div class="calc">频率项：20 log(12/4) = 9.5 dB<br>距离项：20 log(35,863 / 1,000) = 31.1 dB<br>大气路程比（平地近似）：sin 30° / sin 5° = 0.5 / 0.0872 ≈ 5.7</div>
<h4><span class="st">易错</span></h4>
<ul><li>第二个因素只在<b>下行</b>时讲，答题时把"For downlink"写上。</li>
<li>第一个因素要同时写"频率越高"和"卫星越高"两个方向。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(1) Distance between the satellite antenna and the earth-station antenna: the higher the signal frequency and the higher the satellite, the greater the signal power loss. (2) For the downlink, the terrestrial distance between the earth-station antenna and the "aim point" of the satellite: the centre of the coverage area receives the highest power, and the power drops off away from the centre. (3) Atmospheric attenuation: affected by oxygen, water, the elevation angle and frequency; the smaller the elevation angle, the more atmosphere the signal must travel through, and higher frequencies suffer more.</p></div>
<div class="ans">一句话：距离（频率高、卫星高损耗大）、下行时离瞄准点的距离（中心最强）、大气衰减（仰角低、频率高衰减大）。</div>'''},

'c11': {'title': '知识讲解 + 详细解析：GEO 自由空间损耗', 'zh': '''<h4><span class="st">知识讲解</span>自由空间损耗公式</h4>
<p>自由空间损耗（free-space path loss）来自 Friis 公式：L = (4πd/λ)²。换成 dB，并把 f 用 MHz、d 用 km 表示，常数合在一起就是：</p>
<div class="calc">L(dB) = 32.44 + 20 log₁₀ f(MHz) + 20 log₁₀ d(km)</div>
<p>每个符号：f 是载波频率（MHz），d 是收发距离（km）。规律：f 或 d 每增加 10 倍，损耗多 20 dB。Part A 讲义 p.51 写的常数是 32（取整），本题用 32.44。讲义 Part C p.22 的图就是这条公式画出来的（1、4、10、40 GHz 四条平行线）。</p>
<h4><span class="st">详细解析</span>一步一步算</h4>
<ol><li>换单位：4 GHz = 4,000 MHz（公式要求 MHz，填 4 会差 60 dB）。</li>
<li>算两个对数项。计算器提示：log 4000 = log 4 + 3 = 0.602 + 3 = 3.602。</li>
<li>三项相加。</li></ol>
<div class="calc">20 log 4,000 = 20 × 3.602 = 72.04 dB<br>20 log 35,863 = 20 × 4.555 = 91.09 dB<br>L = 32.44 + 72.04 + 91.09 = 195.6 dB<br>（常数用 32：L = 195.1 dB，也算对）</div>
<p><b>合理性检查</b>：p.22 图上 4 GHz、GEO 高度处约 196 dB，吻合。对比：同样 4 GHz、1,000 km 的 LEO 只有 164.5 dB，差约 31 dB；同一颗 GEO 用 1 GHz 是 183.5 dB。</p>
<h4><span class="st">易错</span></h4>
<ul><li>f 用 GHz 代入：20 log 4 = 12.04，少了 60 dB。</li>
<li>d 用 m 代入：多了 60 dB。</li>
<li>用 10 log 代替 20 log：功率与距离平方、频率平方成正比，所以是 20 log。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>L(dB) = 32.44 + 20 log₁₀(4000) + 20 log₁₀(35,863) = 32.44 + 72.04 + 91.09 ≈ 195.6 dB.</p></div>
<div class="ans">一句话：32.44 + 72.04 + 91.09 ≈ 195.6 dB，f 用 MHz、d 用 km。</div>'''},

'c12': {'title': '知识讲解 + 详细解析：仰角与雨雾衰减', 'zh': '''<h4><span class="st">知识讲解</span>仰角越低，穿过的大气越厚</h4>
<p>大气层大约只有十几公里厚。卫星在头顶（仰角 90°）时，信号笔直穿过大气，路程最短；仰角越低，信号斜着穿过大气，路程越长，氧气、水汽、雨、雾对它的吸收和散射也越多（讲义 Part C p.21）。p.23 的图画了<b>大气吸收、雾、雨</b>三种衰减随仰角的变化：都随仰角升高而迅速下降，仰角低于 10° 时急剧增大，雨的影响最大。</p>
<p>课外补充（平地近似）：穿过大气的路程 ∝ 1/sin θ。sin 30° / sin 5° = 0.5 / 0.0872 ≈ 5.7，仰角从 30° 降到 5°，路程约长 5.7 倍。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A 错</b>：仰角变化对大气路程影响很大，不会不变。</li>
<li><b>B 对</b>：路程变长，雨衰、雾衰都明显增大。</li>
<li><b>C 错</b>：方向反了。</li>
<li><b>D 错</b>：雨和雾都随路程增大，不会只有一种增大；而且雨的影响更大。</li></ul>
<div class="ans">一句话：仰角越低，信号穿过的大气越厚，雨衰和雾衰都明显增大，选 B。</div>'''},

'c13': {'title': '知识讲解 + 详细解析：三种通信配置', 'zh': '''<h4><span class="st">知识讲解</span>按"谁和谁通信"来分</h4>
<p>讲义 Part C p.24–25 把卫星通信分成三种常见配置。区分的方法是看<b>发射站和接收站的数量关系</b>：一对一、一对多、中心对多（双向）。</p>
<div class="tw"><table class="mini"><thead><tr><th>配置</th><th>关系</th><th>例子</th></tr></thead><tbody>
<tr><td>点对点（point-to-point）</td><td>一对一，双向</td><td>跨洋干线</td></tr>
<tr><td>广播（broadcast）</td><td>一个发射站 → 多个接收站</td><td>卫星电视</td></tr>
<tr><td>双向星形（VSAT 网）</td><td>一个 hub ↔ 多个远端站</td><td>银行网点、加油站</td></tr></tbody></table></div>
<h4><span class="st">详细解析</span>每种配置的关键点</h4>
<ol><li><b>点对点</b>：卫星给两个<b>相距很远</b>的地面站提供一条链路，替代跨洋电缆，这正是卫星最初的用途（p.4）。</li>
<li><b>广播</b>：一个带发射机的地面站，对许多只有接收机的地面站。GEO 一个波束覆盖很大，最适合广播（p.16）。</li>
<li><b>双向星形</b>：一个中心站（hub）和许多远端客户站。远端站<b>共享卫星容量</b>发给 hub；hub 和各站交换消息，并在远端站之间<b>中转</b>。远端站通常是天线很小的 VSAT（0.3–0.9 m，p.26），因为 hub 天线大，链路预算主要靠 hub 撑起来。</li></ol>
<h4><span class="st">易错</span></h4>
<ul><li>星形网里远端站之间<b>不直接通信</b>，要经 hub 中转（卫星 → hub → 卫星）。</li>
<li>广播是单向的；点对点和星形都是双向。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(1) Point-to-point: the satellite provides a link between two distant earth stations. (2) Broadcast: the satellite provides service between one earth station with a transmitter and a number of earth stations with receivers. (3) Two-way star (VSAT network): one central hub and many remote client stations; the clients share the satellite capacity to transmit to the hub, and the hub exchanges messages with each client and relays messages between clients.</p></div>
<div class="ans">一句话：点对点（两站）、广播（一发多收）、双向星形（hub 加许多 VSAT，远端经 hub 中转）。</div>'''},

'c14': {'title': '知识讲解 + 详细解析：地面站天线尺寸', 'zh': '''<h4><span class="st">知识讲解</span>地面站按天线大小分三类</h4>
<p>地面站由天线、跟踪系统、接收机、发射机、复用器和经调制解调器的地面链路组成；区分地面站的<b>主要特征是天线大小</b>（讲义 Part C p.26）。</p>
<div class="tw"><table class="mini"><thead><tr><th>类型</th><th>天线直径</th></tr></thead><tbody>
<tr><td>大型地面站</td><td>10–60 m</td></tr><tr><td>小型地面站</td><td>1–10 m</td></tr><tr><td>VSAT（甚小口径终端）</td><td>0.3–0.9 m</td></tr></tbody></table></div>
<p>天线越大，业务容量越大。课外补充：抛物面天线增益 ∝ 直径²，直径大 10 倍，增益多 20 dB。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A 错</b>：10–60 m 是大型地面站。</li>
<li><b>B 错</b>：1–10 m 是小型地面站。</li>
<li><b>C 对</b>：VSAT = Very Small Aperture Terminal，名字就说明口径"非常小"，0.3–0.9 m，和家里的卫星电视锅差不多。</li>
<li><b>D 错</b>：几厘米的天线增益太低，收不到 GEO 卫星的弱信号。</li></ul>
<div class="ans">一句话：VSAT 天线 0.3–0.9 m（小型 1–10 m，大型 10–60 m），选 C。</div>'''},

'c15': {'title': '知识讲解 + 详细解析：卫星频段与业务', 'zh': '''<h4><span class="st">知识讲解</span>讲义 p.27 的频段表</h4>
<div class="tw"><table class="mini"><thead><tr><th>频段</th><th>范围</th><th>主要业务</th></tr></thead><tbody>
<tr><td>L</td><td>1–2 GHz</td><td>MSS（移动）</td></tr><tr><td>S</td><td>2–4 GHz</td><td>MSS、NASA、深空</td></tr>
<tr><td>C</td><td>4–8 GHz</td><td>FSS（固定）</td></tr><tr><td>X</td><td>8–12.5 GHz</td><td>军用、气象</td></tr>
<tr><td>Ku</td><td>12.5–18 GHz</td><td>FSS、<b>BSS</b></td></tr><tr><td>K</td><td>18–26.5 GHz</td><td><b>BSS</b>、FSS</td></tr>
<tr><td>Ka</td><td>26.5–40 GHz</td><td>FSS</td></tr></tbody></table></div>
<p>BSS（Broadcast Satellite Service，广播卫星业务）是电视、广播直播（p.8）。用 Ku 的原因：频率高、带宽大，同样的天线增益更高，家用小锅（0.6 m 左右）就能收。老师课上强调：Ku、Ka 很常用，但<b>雨衰大</b>，因为雨滴尺寸接近波长（Ku 波长约 1.7–2.4 cm）。</p>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A 错</b>：L 波段用于移动卫星业务 MSS。</li>
<li><b>B 错</b>：C 波段主要是固定卫星业务 FSS。</li>
<li><b>C 对</b>：Ku（以及 K）用于 BSS。</li>
<li><b>D 错</b>：S 波段是 MSS 和深空研究。</li></ul>
<h4><span class="st">记忆</span></h4>
<p>"低频给移动（L、S），C 给固定，Ku/K 给广播"。</p>
<div class="ans">一句话：BSS 主要用 Ku（以及 K）波段；L、S 是移动，C 是固定，选 C。</div>'''},

# ---------------------------------------------------------------- 多址
'c16': {'title': '知识讲解 + 详细解析：信道可用带宽', 'zh': '''<h4><span class="st">知识讲解</span>FDMA 先切信道，保护带要扣掉</h4>
<p>卫星的总容量先用 <b>FDMA</b>（频分多址）切成若干物理信道，信道里面再进一步分配（讲义 Part C p.28）。相邻信道之间必须留<b>保护带</b>（guard band）：滤波器不是理想的，信号频谱会"漏"到旁边，保护带就是一段空着不用的频率，防止相邻信道互相干扰。所以：</p>
<div class="calc">可用带宽 = 信道带宽 − 保护带</div>
<h4><span class="st">详细解析</span>一步一步算</h4>
<ol><li>每个信道 40 MHz，其中 4 MHz 是保护带，不能传数据。</li>
<li>相减得到可用带宽；顺便算保护带占比。</li>
<li>检查总量：24 个信道共 960 MHz，大于总带宽 500 MHz，说明用了<b>频率复用</b>（讲义原话 "by frequency reuse technique"）。</li></ol>
<div class="calc">可用 = 40 − 4 = 36 MHz<br>保护带占比 = 4 / 40 = 10%<br>24 × 40 = 960 MHz ≈ 1.9 × 500 MHz</div>
<h4><span class="st">课外补充</span>复用怎么做到</h4>
<p>常见做法是两种正交极化：500 MHz 里放 12 个 40 MHz 信道（480 MHz），水平、垂直极化各用一遍，就是 24 个。</p>
<h4><span class="st">易错</span></h4>
<ul><li>用 500 / 24 = 20.8 MHz：题目已说每信道 40 MHz，靠复用，不是平分。</li>
<li>用 40 − 2 × 4：保护带 4 MHz 已经<b>包含在</b>40 MHz 里，只扣一次。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Each 40-MHz channel includes a 4-MHz guard band, so the usable bandwidth per channel = 40 − 4 = 36 MHz. (24 × 40 = 960 MHz exceeds 500 MHz, which is possible by frequency reuse.)</p></div>
<div class="ans">一句话：40 − 4 = 36 MHz，保护带占 10%；24 个信道靠频率复用装进 500 MHz。</div>'''},

'c17': {'title': '知识讲解 + 详细解析：FAMA、DAMA 与 CSC', 'zh': '''<h4><span class="st">知识讲解</span>容量"固定分"还是"按需分"</h4>
<p>讲义 Part C p.29–30。<b>FAMA</b>（Fixed-Assignment Multiple Access，固定分配多址）：容量预先固定分给各站。<b>DAMA</b>（Demand-Assignment Multiple Access，按需分配多址）：根据各站需求的变化随时调整分配。老师课上强调：FAMA 预先分好、不能改；DAMA 把一部分链路当公共池，按需分配，更灵活。</p>
<div class="tw"><table class="mini"><thead><tr><th></th><th>FAMA</th><th>DAMA</th></tr></thead><tbody>
<tr><td>分配方式</td><td>固定</td><td>按需动态</td></tr>
<tr><td>缺点</td><td>需求波动时容量大量闲置</td><td>需要信令和调度</td></tr>
<tr><td>FDMA 版本</td><td>各站频带预先分好</td><td>子信道组成池，按需分一对</td></tr></tbody></table></div>
<h4><span class="st">详细解析</span>CSC 的工作过程</h4>
<ol><li><b>资源池</b>：一个信道里的子信道（subchannel）当作可用链路池。两个地面站要<b>全双工</b>通信时，动态分给它们<b>一对</b>子信道（一去一回）。</li>
<li><b>分布式分配</b>：没有中心站逐个审批，由各地面站自己通过<b>公共信令信道 CSC</b>（Common Signalling Channel）协调。</li>
<li><b>CSC 帧结构</b>：CSC 反复发送一个 TDMA 帧，<b>50 个时隙</b>；第 1 个用于<b>同步</b>，其余 49 个<b>永久分给 49 个站</b>。</li>
<li><b>占用广播</b>：某站选好子信道后，在自己的时隙里广播所选子信道的编号；其他站都听得到，就不会再选这些子信道，避免冲突。</li>
<li><b>公平</b>：要公平使用子信道，还需要一个集中调度器（p.30 最后一点）。</li></ol>
<p>为什么 DAMA 好：某站空闲时，FAMA 下它那份容量别人用不上；DAMA 下空闲的子信道回到池里给忙的站用。</p>
<h4><span class="st">易错</span></h4>
<ul><li>CSC 本身是 <b>TDMA</b> 帧，而它分配的是 <b>FDMA</b> 子信道，两层别混。</li>
<li>能支持的站数是 49，不是 50（见 c18）。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>FAMA assigns capacity to the stations in a fixed manner; since demand fluctuates, capacity is significantly under-used. DAMA changes the assignment as needed to respond to demand. In DAMA-FDMA, the subchannels in a channel form a pool; a pair of subchannels is dynamically assigned for a full-duplex link between two earth stations. The assignment is done in a distributed way using a common signalling channel (CSC), which carries a repetitive TDMA frame of 50 slots: the first slot is for synchronisation and the other 49 are permanently assigned to 49 stations. A station that selects subchannels transmits their identifiers in its own slot, so other stations will not select them. A centralised scheduler is needed for fair use.</p></div>
<div class="ans">一句话：FAMA 固定分、浪费；DAMA 按需分；DAMA-FDMA 靠 CSC（50 时隙 TDMA 帧，1 同步 + 49 站）广播自己占用的子信道。</div>'''},

'c18': {'title': '知识讲解 + 详细解析：CSC 支持的站数', 'zh': '''<h4><span class="st">知识讲解</span>CSC 的 50 个时隙怎么用</h4>
<p>DAMA-FDMA 的公共信令信道 CSC 反复发送一个 TDMA 帧，共 50 个时隙（讲义 Part C p.30）。<b>第 1 个时隙用于同步</b>：所有站靠它对齐帧的起点，才知道"现在是第几个时隙"，否则各站会在别人的时隙里发送。<b>其余 49 个时隙永久分给 49 个站</b>，每站一个，用来广播自己选了哪些子信道。</p>
<h4><span class="st">详细解析</span></h4>
<ol><li>做什么：从总时隙里扣掉同步时隙。为什么：同步时隙不属于任何站。</li>
<li>每站固定占一个时隙，所以站数 = 剩下的时隙数。</li></ol>
<div class="calc">支持站数 = 50 − 1 = 49 个</div>
<p><b>合理性检查</b>：讲义原话 "Others are permanently assigned to 49 stations"，一致。</p>
<h4><span class="st">易错</span></h4>
<ul><li>答 50：忘了第 1 个时隙是同步用的。</li>
<li>答 24 或 25（以为全双工要两个时隙一对）：时隙用来<b>发信令</b>，每站一个；成对的是 FDMA 子信道，不是 CSC 时隙。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>The CSC frame has 50 slots; the first slot is used for synchronisation and the remaining 49 slots are permanently assigned to stations, so at most 50 − 1 = 49 earth stations are supported.</p></div>
<div class="ans">一句话：50 个时隙减去 1 个同步时隙，最多 49 个站。</div>'''},

'c19': {'title': '知识讲解 + 详细解析：TDMA 为何比 FDMA 高效', 'zh': '''<h4><span class="st">知识讲解</span>比的是"开销"占多少容量</h4>
<p>两种多址都有开销：<b>FDMA</b> 相邻信道之间要留<b>保护带</b>（guard band，一段不用的频率）；<b>TDMA</b> 相邻突发之间要留<b>保护时间</b>（guard time），每帧还有参考突发和前导等<b>控制比特</b>。讲义 Part C p.35 原话：TDMA 的保护时间和控制比特占用的容量，<b>比 FDMA 的保护带少</b>，所以 TDMA 通常更高效。在 Ku、K 高频段还能用窄波束做多波束复用，效率更高。</p>
<div class="calc">课外举例：TDMA 帧 2 ms，参考突发 20 µs，10 站各 10 µs 前导 + 2 µs 保护：开销 140 µs → 效率 93%<br>FDMA：40 MHz 信道含 4 MHz 保护带 → 效率 90%</div>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A 错</b>：恰恰相反，TDMA <b>需要</b>严格的时间同步，各站才能准确落在自己的时隙里。</li>
<li><b>B 对</b>：讲义 p.35 的原因。</li>
<li><b>C 错</b>：两者共用同一个转发器带宽，效率差别来自开销，不是带宽大小。</li>
<li><b>D 错</b>：卫星通信当然需要地面站。</li></ul>
<div class="ans">一句话：TDMA 的保护时间和控制比特比 FDMA 的保护带占用更少容量，选 B。</div>'''},

'c20': {'title': '知识讲解 + 详细解析：SS/TDMA 模式数', 'zh': '''<h4><span class="st">知识讲解</span>卫星在天上当交换机</h4>
<p>Ku、K 频段可以用多个窄波束分别照 N 个区域（讲义 Part C p.35）。同一区域内的站用普通 FAMA-TDMA；不同区域之间通信，卫星要把某个上行波束的时隙<b>交换</b>到另一个下行波束上，这叫<b>卫星交换 TDMA（SS/TDMA）</b>，是 DAMA-TDMA 的一种（p.36）。任一时刻，星上开关把 N 个上行波束<b>一一对应</b>地接到 N 个下行波束，每一种接法叫一个<b>模式（mode）</b>。讲义：全连通需要 <b>N!</b> 种模式；卫星周期性换模式，最多每个时隙换一次，模式和时长可由地面指令调整。</p>
<h4><span class="st">详细解析</span>为什么是 N!</h4>
<ol><li>一种模式 = 把 N 个上行波束排到 N 个下行位置上，每个下行只接一个上行，这正是 N 个元素的一个<b>排列</b>。</li>
<li>第 1 个上行有 N 种选择，第 2 个剩 N − 1 种……所以排列数 = N × (N − 1) × … × 1 = N!。</li>
<li>代入 N = 5。</li></ol>
<div class="calc">N = 3：3! = 6（ABC、ACB、BAC、BCA、CAB、CBA）<br>N = 4：4! = 24<br>N = 5：5! = 5 × 4 × 3 × 2 × 1 = 120 种</div>
<h4><span class="st">课外补充</span>（讲义没有）</h4>
<p>严格说，N! 是所有可能的开关模式总数。如果只要求"任意两个区域之间某个时刻能连通"，N 个循环移位模式就能覆盖全部 N² 个上下行组合。考试按讲义写 N!。</p>
<h4><span class="st">易错</span></h4>
<ul><li>答 N² = 25 或 N(N − 1) = 20：那是"上下行对"的个数，不是模式数。</li>
<li>答 5 × 2 = 10 等：模式是整体排列，不是单条连接。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Each mode is a one-to-one connection of the N uplink beams to the N downlink beams, i.e. a permutation, so N! modes are required for full connectivity: 5! = 120 modes.</p></div>
<div class="ans">一句话：每种模式是一个排列，全连通需要 N! 种，5! = 120。</div>'''},

'c21': {'title': '知识讲解 + 详细解析：TDMA 帧结构', 'zh': '''<h4><span class="st">知识讲解</span>为什么 TDMA 帧要这样设计</h4>
<p>卫星 TDMA（讲义 Part C p.31）：传输是重复的帧，每帧分成若干时隙，每个站分到一个或多个时隙；各站轮流在自己的时隙发上行，卫星把收到的内容<b>广播给所有站</b>，每个站要知道哪个时隙发、哪个时隙收。难点在于：各站离卫星距离不同，时钟也不完全一样，所以帧里必须有"定时基准"和"自我介绍"。p.32 的图就是答案。</p>
<div class="tw"><table class="mini"><thead><tr><th>部分</th><th>内容</th><th>作用</th></tr></thead><tbody>
<tr><td>参考突发（reference burst）</td><td>载波与比特定时恢复、协调数据</td><td>给全网一个时间基准，告诉各站帧从哪里开始</td></tr>
<tr><td>保护时间（guard time）</td><td>突发之间的空隙</td><td>吸收各站的定时误差，防止突发重叠</td></tr>
<tr><td>各站数据突发</td><td>前导 + 信息</td><td>每站在自己的时隙发送</td></tr></tbody></table></div>
<h4><span class="st">详细解析</span>前导（preamble）的四个字段</h4>
<ol><li><b>载波与比特定时恢复</b>（carrier and bit timing recovery）：接收机先锁定这个突发的载波相位和比特时钟，才能正确解调。每个站的突发来自不同发射机，所以每个突发都要重新恢复。</li>
<li><b>唯一字</b>（unique word）：一段固定的比特图样，用来准确找到突发里信息开始的位置（突发定位）。</li>
<li><b>站识别</b>（station identification）：说明这个突发是哪个站发的。</li>
<li><b>网络控制与请求</b>（network control and request）：传网络管理信息，或请求更多容量。</li></ol>
<p>前导后面才是真正的<b>信息</b>（information）。p.33–34：上行时各站在不同时隙发送；下行时卫星把整帧广播回去，各站挑出发给自己的部分。</p>
<h4><span class="st">易错</span></h4>
<ul><li>参考突发在<b>帧开头</b>，每帧一个；前导在<b>每个站的突发开头</b>，每站一个。</li>
<li>保护时间、参考突发、前导都是开销，这就是 c19 说的"保护时间和控制比特"。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>A TDMA frame starts with a reference burst (carrier and bit timing recovery, coordination data), followed by the data bursts of the individual stations, separated by guard times. Each station's burst consists of a preamble and information. The preamble contains carrier and bit timing recovery, a unique word, station identification, and network control and request; the information field carries the user data.</p></div>
<div class="ans">一句话：参考突发 + 各站数据突发（中间隔保护时间）；每个突发 = 前导（定时恢复、唯一字、站识别、网络控制与请求）+ 信息。</div>'''},

# ---------------------------------------------------------------- 网络
'c22': {'title': '知识讲解 + 详细解析：星间链路的路由', 'zh': '''<h4><span class="st">知识讲解</span>两种路由方案</h4>
<p>讲义 Part C p.39：两个用户分别在两颗卫星下面。<b>有星间链路</b>（ISL，Inter-Satellite Link）时，信息在太空中直接从一颗卫星转到另一颗；<b>没有</b>时，卫星先下传到地面网关，经地面网络路由到负责另一颗卫星的网关，再上传。</p>
<div class="tw"><table class="mini"><thead><tr><th></th><th>有 ISL</th><th>无 ISL</th></tr></thead><tbody>
<tr><td>路径</td><td>用户 A ↑ 卫星 1 → 卫星 2 ↓ 用户 B</td><td>A ↑ 卫星 1 ↓ 网关 1 → 地面网 → 网关 2 ↑ 卫星 2 ↓ B</td></tr>
<tr><td>链路数</td><td>1 上 + 1 下</td><td>2 上 + 2 下</td></tr>
<tr><td>地面网关</td><td>少</td><td>多</td></tr></tbody></table></div>
<h4><span class="st">逐项分析</span></h4>
<ul><li><b>A 对</b>：上行一次进入太空，星间转发，下行一次到达对方。</li>
<li><b>B 错</b>：这是<b>没有</b>星间链路的情况。</li>
<li><b>C 错</b>：用户在地面，至少要一上一下。</li>
<li><b>D 错</b>：上下行数应相等，单向路径进出太空各一次。</li></ul>
<h4><span class="st">记忆</span></h4>
<p>数"进出太空"的次数：有 ISL 进出各一次；无 ISL 中途要回地面一趟，进出各两次。</p>
<div class="ans">一句话：有星间链路时 1 上 1 下，还能少建网关；没有时 2 上 2 下，选 A。</div>'''},

'c23': {'title': '知识讲解 + 详细解析：卫星系统四种切换', 'zh': '''<h4><span class="st">知识讲解</span>为什么 MEO/LEO 系统要切换</h4>
<p>地面蜂窝里，切换（handover）几乎都是用户在动引起的。MEO、LEO 卫星相对地面在动（LEO 每颗只可见 15–20 分钟），如果卫星本身带着"基站"，即使用户不动，卫星一飞走也要切换（讲义 Part C p.40）。GEO 相对地面静止，几乎不用切换。这一题是 <b>2025-26 S2 期末 Q4(b)，8 分</b>；老师课上强调卫星是未来很重要的方向，并提到期末考过这一题，属于必背。</p>
<h4><span class="st">详细解析</span>四种切换，看"谁变了"</h4>
<div class="tw"><table class="mini"><thead><tr><th>切换</th><th>原因</th><th>例子</th></tr></thead><tbody>
<tr><td>星内切换（intra-satellite）</td><td>用户在同一颗卫星覆盖区内，从一个扇区（点波束）移到另一个</td><td>开车穿过两个点波束交界</td></tr>
<tr><td>星间切换（inter-satellite）</td><td>用户移到另一颗卫星的覆盖区，<b>或卫星自己飞走</b></td><td>头顶 LEO 落下地平线，转到下一颗</td></tr>
<tr><td>网关切换（gateway）</td><td>卫星离开当前地面网关</td><td>卫星改连另一个网关</td></tr>
<tr><td>系统间切换（inter-system）</td><td>卫星系统与地面蜂窝系统之间，因信号强度和 QoS 发生的<b>垂直切换</b></td><td>从野外进城，从卫星转到 4G</td></tr></tbody></table></div>
<ol><li>星内：波束变，卫星不变。</li>
<li>星间：卫星变。原因有两个，都要写，"卫星飞走"是卫星系统特有的。</li>
<li>网关：地面网关变，和用户无关，是卫星和地面之间那条链路在换。</li>
<li>系统间：网络类型变，所以叫<b>垂直切换</b>（vertical handover），判断依据是信号强度和 QoS。</li></ol>
<h4><span class="st">易错</span></h4>
<ul><li>星间切换只写"用户移动"，漏了"卫星移走"。</li>
<li>系统间切换要写出 "vertical handover" 和 "signal strength and QoS"。</li>
<li>8 分题四点各约 2 分：每种写"名称 + 原因"一句，不要只列名字。</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>(1) Intra-satellite handover: caused by the movement of a mobile user within the coverage of one satellite, from one sector (spot beam) to another. (2) Inter-satellite handover: caused by the movement of a mobile user from the coverage of one satellite to that of another, or because the satellite moves away. (3) Gateway handover: caused by the movement of the satellite away from its current gateway, so the satellite must connect to another gateway. (4) Inter-system handover: between the satellite system and a terrestrial cellular system; it is a vertical handover triggered by signal strength and QoS performance.</p></div>
<div class="ans">一句话：波束变 → 星内；卫星变 → 星间；网关变 → 网关；系统变 → 系统间（垂直切换）。</div>'''},
}

NOTES = '''c5/c6: slide p.15 says one GEO covers "1/4 of the earth"; geometrically the visible cap is (1 − cos β)/2 ≈ 42 % at 0° elevation and ≈ 34 % at 10° (usually quoted ~1/3). Box says 1/4 is conservative and to write the slide figure in the exam.
c5: GEO coverage diameter ≈ 18,000 km at 0° elevation vs ≈ 16,000 km (slide p.14 table) at 10°; existing solution already reconciles this, box repeats it.
c20: slide p.36 says "N! different modes are required for full connectivity"; N! is the number of possible one-to-one switch configurations, while N cyclic-shift modes already connect every uplink/downlink pair. Box keeps N! (slide answer) and mentions this as 课外补充.
c11: Part A slide uses constant 32 instead of 32.44 (195.1 vs 195.6 dB); existing solution already accepts both.'''
