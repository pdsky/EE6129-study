#!/usr/bin/python3
"""Insert verbatim English questions from the Part A slides into examples.html.

Run once; it refuses to run twice (checks for the .orig marker).
"""
import pathlib, re, sys

REPO = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129-study')
SRC = REPO / 'examples.html'
FIG = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_text/renders/fig140.b64').read_text().strip()

html = SRC.read_text(encoding='utf-8')
if 'class="orig"' in html:
    sys.exit('already has English questions')

Q = '<span class="blank">?</span>'

# id -> (slide label, note or None, body html)
ORIG = {
'p44': ('Slide 43', None, '''
<p>Consider an AMPS system with two operators sharing the 25 MHz bandwidth. Assume each cell uses 3 control channels. Calculate the spectral efficiency based on the following parameters.</p>
<ul>
<li>Area of cell = 4 km<sup>2</sup></li>
<li>Total coverage area = 2000 km<sup>2</sup></li>
<li>Average number of calls per user per hour = 1.2</li>
<li>Average holding time of a call = 100 sec</li>
<li>Call blocking probability: GOS = 2%</li>
<li>Frequency reuse factor = 7</li>
</ul>'''),
'p47': ('Slide 47', None, '''
<p>In the North American TDMA system, the parameters are as follows. Calculate the multiple access spectral efficiency.</p>
<ul>
<li>Single operator bandwidth = 12.5 MHz with channel spacing = 30 kHz</li>
<li>Total data channels = 395</li>
<li>Frame duration = 40 ms with time slots per frame = 6</li>
<li>Speech rate = 13 kbps and gross data rate = 16.2 kbps</li>
</ul>'''),
'p65': ('Slide 65', None, '''
<p>Find the received power using CCIR model for</p>
<ul class="plain">
<li>P<sub>T</sub> = 5W, d = 2km</li>
<li>G<sub>T</sub> = 10dBd, G<sub>R</sub> = 0 dBd</li>
<li>h<sub>T</sub> = 25m, h<sub>R</sub> = 2m</li>
</ul>'''),
'p82': ('Slide 82', None, '''
<p>A 7-cell reuse FDD cellular system has a total of 30 MHz of bandwidth. Each simplex voice channel occupies 25 kHz bandwidth. A total of 2 MHz bandwidth is allocated to control channels. Determine the number of duplex voice channels in the system and per cell. Assume that uniform fixed channel assignment (UFCA) is used.</p>'''),
'p89': ('Slide 89', None, '''
<p>If a SIR of 10 dB is required for a cellular system, find the optimum cluster size with the path loss exponent to be 4. Using simple analysis assumptions.</p>'''),
'p91': ('Slide 91 · “The Worse Case”', '这页是推导页，没有单独的题干。下面是原文，结果用 ? 代替。', f'''
<p><b>Case 1:</b> Then SIR,</p>
<p class="eq">S/I = R<sup>−n</sup> / [2(D − R)<sup>−n</sup> + 2D<sup>−n</sup> + 2(D + R)<sup>−n</sup>] = 1 / [2(Q − 1)<sup>−n</sup> + 2Q<sup>−n</sup> + 2(Q + 1)<sup>−n</sup>]</p>
<p>N = 7, n = 4, S/I = {Q} dB</p>
<p><b>Case 2:</b> To be conservative, shortest distance D − R for all 6 interferers, then</p>
<p class="eq">S/I = R<sup>−n</sup> / 6(D − R)<sup>−n</sup> = 1 / 6(Q − 1)<sup>−n</sup></p>
<p>N = 7, n = 4, S/I = {Q} dB</p>'''),
'p93': ('Slide 93', None, '''
<p>If the total number of system channel is 210. Compute the number of channels per cell if the fixed channel assignment is used.</p>'''),
'p121': ('Slides 121–122', '讲解型例题，原文自带结果。下面照录原文，结果用 ? 代替。', f'''
<p>Typical call arrival rate λ in a large population of mobile users, during the busy hour can range from 0.4 calls/hr/per subscriber to 1.2 calls/hr/per subscriber.</p>
<p>Typical holding time 1/μ can be around 100 seconds. Thus, it can give rise to an offered traffic of λ/μ = (1.2)(100/3600) = {Q} Erlangs.</p>
<p>Typical values of blocking probability are:</p>
<ul>
<li>For P<sub>B</sub> = 0.05, M = 10, A = 6.2, M = 20, A = 15.2, M = 50, A = 44.3</li>
<li>For P<sub>B</sub> = 0.02, M = 10, A = 5.08, M = 20, A = 13.2, M = 50, A = 40.3</li>
</ul>
<p>A cell with 50 channels would be able to handle 40.3 Erlangs with P<sub>B</sub> = 2%. This is equivalent to handling {Q} mobile subscribers with 2% GoS during busy hour traffic.</p>
<p>Trunking gain is defined as: Trunking gain = the number of users served by a set of channels (or trunks) with a specified GOS / the number of channels (or trunks). In the mobile environment, under busy hour traffic conditions, the trunking gain is ≈ {Q} for a GoS of 2%.</p>'''),
'p123': ('Slides 123–124 · “Trunking Efficiency”', '讲解型例题，原文自带结果。下面照录原文，结果用 ? 代替。', f'''
<p>Trunking efficiency: 10 trunked channels at a GoS of 0.01 can support {Q} Erlangs of traffic. Two groups of 5 trunked channels at the same GoS (0.01) support 2 × {Q} = {Q} Erlangs of traffic.</p>
<p>Trunking efficiency: is expressed as value between 0 and 1 and is the carried traffic in Erlangs/channel. It is a function of the number of channels per cell for a specified GOS parameter i.e. P(blocking) = 0.01 for Erlang B a fixed channel C = 10.</p>
<p>For 1st case: Trunking efficiency is = {Q}<br>For 2nd case: Trunking efficiency is = {Q}</p>
<p>So 1 group of 10 channels support {Q}% more traffic than 2 groups of 5 channels. But the SIR for 2 groups would probably be better.</p>'''),
'p130': ('Slide 130', None, '''
<p>In a residential area with 1.2 million people, there are 3 service providers (Singa, Mobi, Hubba). Singa has 380 cells with 20 channels each. Mobi has 100 cells with 60 channels each. Hubba has 60 cell with 100 channels each.</p>
<p>Find the number of users supported by each blocked system with GoS of 2%. Given that each user has average 3 calls per hour with an average call duration of 5 minutes. Assuming that all 3 service provider operates at maximum capacity, compute the percentage market penetration for each provider.</p>'''),
'p133': ('Slide 133', None, '''
<p>A city has an area of 1300 km<sup>2</sup> and is covered by a seven-cell reuse pattern system. Each cell has an area of 41.5 km<sup>2</sup>, and each cluster is allocated 40MHz of spectrum with a full duplex channel bandwidth of 60kHz. Assume a GoS of 2% for an Erlang B system is specified. If the offered traffic per user is 0.03 Erlangs, Compute:</p>
<ul>
<li>Number of cells in the service area</li>
<li>Number of channels per cell</li>
<li>Traffic intensity of each cell</li>
<li>Maximum traffic</li>
<li>Total number of users that can be served for 2% GoS</li>
<li>Numbers of mobiles per unique channel</li>
<li>Theoretical maximum number of users that could be served at one time by the system</li>
</ul>'''),
'p136': ('Slide 136 · “Cell Splitting”', '讲解型例题，原文自带结果。下面照录原文，结果用 ? 代替。', f'''
<p>Subdivide congested cell into smaller cells (microcells), each with its own base station. These smaller cells have lower antenna height and smaller transmit power. Capacity is increased due to additional channels per unit area.</p>
<p>If microcells have half of the radius of original cell,</p>
<p class="eq">P<sub>r</sub>[original cell] ∝ P<sub>t1</sub>R<sup>−n</sup><br>P<sub>r</sub>[microcell] ∝ P<sub>t2</sub>(R/2)<sup>−n</sup></p>
<p>If path loss exponent n = 4, P<sub>t2</sub> = {Q}. Transmitted power for microcell has to be reduced by {Q} dB in order to maintain the same SIR.</p>'''),
'p140': ('Slide 140', None, f'''
<figure class="slidefig"><img src="data:image/png;base64,{FIG}" alt="Slide 140 figure: hexagonal cells of radius R around base station A, each split into microcells of radius R/2, with a square drawn around A" width="533" height="356"><figcaption>课件 p.140 原图</figcaption></figure>
<p>For the above figure, each base station uses 60 channels regardless of cell size. If original cell radius is 1km and microcell has 0.5km radius, find the number of channels contained in a 3km by 3km square centered around A, under following conditions:</p>
<ul>
<li>Without microcells</li>
<li>With the microcells used</li>
</ul>'''),
'p145': ('Slides 144–145 · “Sectoring” / “Cell Sectoring”', '讲解型例题，原文自带结果。下面照录原文，结果用 ? 代替（p.145 原文本身就写着 “S/I = ? dB”）。', f'''
<p>By using 120 degree sectoring, first tier interference can be reduced to {Q}. SIR is found to be {Q} dB as compared to 18dB for omni-directional without sectoring, which is a significant improvement.</p>
<p>The improvement in SIR decreases cluster size N, improves frequency reuse, thus system capacity. If SIR for 7 cell is 18dB, with 120 degree, the SIR improved is comparable to 12 cells. Therefore, increase in channel capacity by a factor of {Q}.</p>
<p>Co-channel interference reduction with cell sectoring due to use of directional antennas:</p>
<p><b>3-sector, worst case:</b></p>
<p class="eq">S/I = R<sup>−n</sup> / {{D<sup>−n</sup> + (D + 0.7R)<sup>−n</sup>}} = 1 / {{Q<sup>−n</sup> + (Q + 0.7)<sup>−n</sup>}}</p>
<p>When N = 7 and n = 4, S/I = ? dB</p>
<p><b>6-sector, worst case:</b></p>
<p class="eq">S/I = R<sup>−n</sup> / (D + 0.7R)<sup>−n</sup> = 1 / (Q + 0.7)<sup>−n</sup></p>
<p>When N = 7 and n = 4, S/I = ? dB</p>'''),
'p148': ('Slide 148', None, '''
<p>A system has an average call duration of 2 minutes with the probability of blocking no more then 1%. Assume that this is a blocked system and each user makes 1 call per hour on average, if there are 395 traffic channels for a 7 cell reuse system, there will be 57 channels per cell.</p>
<p>Find the number of calls per hour if no sectoring is used.</p>
<p>Compute the number of calls per hour when 120 degree and 60 degree sectoring is used.</p>'''),
}

def block(label, note, body):
    n = f'<div class="orig-note">{note}</div>' if note else ''
    return (f'\n    <div class="orig" lang="en"><div class="orig-lab"><span>Original question</span>'
            f'<span>{label}</span></div>{body.strip()}\n    {n}</div>')

count = 0
for aid, (label, note, body) in ORIG.items():
    pat = re.compile(r'(<article class="ex"[^>]*id="' + aid + r'">\s*<header>.*?</header>)', re.S)
    html, k = pat.subn(lambda m: m.group(1) + block(label, note, body), html, count=1)
    if k != 1:
        sys.exit(f'article {aid} not found')
    count += 1

CSS = '''
/* 课件英文原题 */
:root{--img-filter:none}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--img-filter:invert(.88) hue-rotate(180deg)}}
:root[data-theme="dark"]{--img-filter:invert(.88) hue-rotate(180deg)}
.orig{border:1px solid var(--border);border-radius:10px;padding:10px 14px 8px;margin-bottom:10px;font-size:.92rem;line-height:1.6}
.orig-lab{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 10px;font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--accent-strong);margin-bottom:6px}
.orig-lab span:last-child{color:var(--muted);text-transform:none;letter-spacing:0}
.orig p{margin:.35em 0}
.orig ul{margin:.3em 0 .4em;padding-left:1.3em}
.orig ul.plain{list-style:none;padding-left:.2em}
.orig li{margin:.12em 0}
.orig .eq{font-family:'IBM Plex Mono',monospace;font-size:.84rem;background:var(--surface-2);border-radius:6px;padding:6px 10px;overflow-x:auto}
.orig .blank{display:inline-block;min-width:2.2em;text-align:center;border-bottom:1.5px solid var(--accent);color:var(--accent-strong);font-weight:600}
.orig-note{font-size:.78rem;color:var(--muted);margin-top:6px}
.slidefig{margin:4px 0 8px}
.slidefig img{display:block;max-width:100%;height:auto;filter:var(--img-filter)}
.slidefig figcaption{font-size:.74rem;color:var(--muted)}
.q::before{content:'中文题意';display:block;font-family:'IBM Plex Mono',monospace;font-size:.66rem;letter-spacing:.06em;color:var(--muted);margin-bottom:2px}
'''
html = html.replace('</style>', CSS + '</style>', 1)

old_lede = re.search(r'<p class="lede">讲义里的 15 道例题.*?</p>', html, re.S)
if not old_lede:
    sys.exit('lede not found')
html = html.replace(old_lede.group(0),
    '<p class="lede">讲义里的 15 道例题按页码整理。每题先给<b>课件原版英文题目</b>（逐字照录，没有删改），再给中文题意，然后是分步解法 → 答案 → 记忆方法 → 易错点。几页讲解型例题原文自带结果，照录时把结果换成 ?，方便自测。讲义里的 Erlang 值是查表取整的，我用公式重新算过，差别写在「核对」里。打开「自测模式」会先隐藏解法，适合考前默写。</p>', 1)

SRC.write_text(html, encoding='utf-8')
print('inserted', count, 'English questions')
