# -*- coding: utf-8 -*-
"""Check src/explain/bcB.py: ids, structure, HTML, MCQ answer letters, numbers, slide quotes.
Run: /usr/bin/python3 check_bcB.py"""
import importlib.util, os, re, sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))                     # EE6129-study
SLIDES = os.path.join(os.path.dirname(ROOT), 'EE6129_text', 'partB.txt')
SW7 = os.path.join(os.path.dirname(ROOT), 'EE6129_text', 'sw', 'Chapter_7__OFDM_.txt')

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

X = load('bcB', os.path.join(HERE, 'bcB.py'))
QB = load('bcq', os.path.join(ROOT, 'src', 'p2build', 'bc_questions.py'))
Q = {q['id']: q for q in QB.Q}
err = []
def bad(msg): err.append(msg)

# ---------- ids ----------
ids = ['b%d' % i for i in range(1, 40)]
for i in ids:
    if i not in X.XPL: bad('missing ' + i)
for k in X.XPL:
    if k not in ids: bad('unexpected id ' + k)
if not isinstance(X.NOTES, str): bad('NOTES not str')

# ---------- HTML ----------
ALLOWED = {'h4', 'span', 'p', 'ul', 'ol', 'li', 'b', 'i', 'sub', 'sup', 'br', 'div',
           'table', 'thead', 'tbody', 'tr', 'th', 'td'}
DIVCLS = {'calc', 'tw', 'ans', 'tmpl'}
class P(HTMLParser):
    def __init__(s, qid):
        super().__init__(convert_charrefs=False); s.qid = qid; s.stack = []
    def handle_starttag(s, tag, attrs):
        a = dict(attrs)
        if tag not in ALLOWED: bad(f'{s.qid}: tag {tag}')
        if 'style' in a: bad(f'{s.qid}: inline style')
        if tag == 'span' and (a != {'class': 'st'} or not s.stack or s.stack[-1] != 'h4'):
            bad(f'{s.qid}: span must be h4 > span.st')
        if tag == 'div':
            c = a.get('class')
            if c not in DIVCLS: bad(f'{s.qid}: div class {c}')
            if c == 'tmpl' and a.get('lang') != 'en': bad(f'{s.qid}: tmpl needs lang=en')
            if c != 'tmpl' and set(a) != {'class'}: bad(f'{s.qid}: div attrs {a}')
        elif tag == 'table':
            if a != {'class': 'mini'} or not s.stack or s.stack[-1] != 'div': bad(f'{s.qid}: table must be div.tw > table.mini')
        elif tag != 'span' and a: bad(f'{s.qid}: attrs on {tag}: {a}')
        if tag != 'br': s.stack.append(tag)
    def handle_endtag(s, tag):
        if tag == 'br': return
        if not s.stack or s.stack[-1] != tag: bad(f'{s.qid}: unbalanced </{tag}> stack={s.stack[-3:]}')
        else: s.stack.pop()
    def handle_data(s, d):
        if '<' in d or '>' in d: bad(f'{s.qid}: raw < or > in text: {d[:40]!r}')
        if '$' in d or '\\(' in d or '\\[' in d: bad(f'{s.qid}: LaTeX-like text')

def cjk(s): return len(re.findall(r'[一-鿿]', s))

lens = {}
for qid in ids:
    e = X.XPL.get(qid)
    if not e: continue
    t, z = e['title'], e['zh']
    if not t.startswith('知识讲解 + 详细解析：'): bad(f'{qid}: title prefix')
    if len(t) > 30: bad(f'{qid}: title {len(t)} chars')
    for must in ('<span class="st">知识讲解</span>', '<div class="ans">一句话：'):
        if must not in z: bad(f'{qid}: missing {must}')
    if '<script' in z or '<img' in z or '<a ' in z: bad(f'{qid}: forbidden element')
    p = P(qid); p.feed(z); p.close()
    if p.stack: bad(f'{qid}: unclosed {p.stack}')
    body_no_en = re.sub(r'<div class="tmpl" lang="en">.*?</div>', '', z, flags=re.S)
    vis = lambda h: len(re.sub(r'\s+', '', re.sub(r'&[a-z]+;', 'x', re.sub(r'<[^>]+>', '', h))))
    lens[qid] = (cjk(re.sub(r'<[^>]+>', '', body_no_en)), vis(body_no_en), vis(z))
    q = Q[qid]
    if q['type'] == 'mcq':
        L = 'ABCD'[q['ans']]
        m = re.search(r'<div class="ans">一句话：选 ([A-D])：', z)
        if not m: bad(f'{qid}: MCQ ans line must start 一句话：选 X：')
        elif m.group(1) != L: bad(f'{qid}: ans letter {m.group(1)} != source {L}')
        for k in 'ABCD':
            if f'<li><b>{k}' not in z: bad(f'{qid}: option {k} not analysed')
        if '逐项分析' not in z: bad(f'{qid}: no 逐项分析')
    else:
        if '<div class="tmpl" lang="en">' not in z: bad(f'{qid}: no English template')
    if q['type'] == 'num':
        a = q['ans']; s = ('%g' % a)
        if s not in z: bad(f'{qid}: answer {s} not in box')

# ---------- numbers ----------
def chk(name, got, want, tol=1e-9):
    if abs(got - want) > tol: bad(f'number {name}: got {got} want {want}')
def cw(k, lo=32, hi=256): return min(lo * 2 ** (k - 1), hi)
# b8
chk('b8 CW seq', sum(abs(cw(k) - v) for k, v in zip(range(1, 5), [32, 64, 128, 256])), 0)
chk('b8 mean', (0 + cw(4) - 1) / 2, 127.5)
chk('b8 mean == source', (cw(4) - 1) / 2, Q['b8']['ans'])
chk('b8 wrong mean 0..CW', (0 + 256) / 2, 128)
chk('b8 attempt3 CW', cw(3), 128); chk('b8 attempt3 mean', (cw(3) - 1) / 2, 63.5)
chk('b8 32*2^3', 32 * 2 ** 3, 256)
# b9
chk('b9 uncapped', 32 * 2 ** 5, 1024); chk('b9 CW6', cw(6), 256); chk('b9 == source', cw(6), Q['b9']['ans'])
# b27
chk('b27 a', 10 * 2, 20); chk('b27 b', 10 / 0.5, 20); chk('b27 == source', 10 / 0.5, Q['b27']['ans'])
# b28
chk('b28 normal', 12 * 7, 84); chk('b28 ext', 12 * 6, 72); chk('b28 == source', 12 * 7, Q['b28']['ans'])
chk('b28 RB kHz', 12 * 15, 180); chk('b28 RB pair', 2 * 84, 168)
# b29 (课外 CP lengths: normal 160/30.72 us for first symbol, 144/30.72 others; extended 512/30.72)
chk('b29 normal CP us', round(144 / 30.72, 1), 4.7); chk('b29 ext CP us', round(512 / 30.72, 1), 16.7)
chk('b29 normal km', round(4.7e-6 * 3e8 / 1e3, 1), 1.4); chk('b29 ext km', round(16.7e-6 * 3e8 / 1e3), 5)
for qid, s in [('b8', '127.5'), ('b8', '63.5'), ('b9', '1024'), ('b27', '20'), ('b28', '84'), ('b28', '72'),
               ('b28', '180 kHz'), ('b28', '168'), ('b29', '4.7 μs'), ('b29', '16.7 μs'), ('b29', '1.4 km'), ('b29', '5 km')]:
    if s not in X.XPL[qid]['zh']: bad(f'{qid}: expected "{s}" in text')

# ---------- slide quotes on cited pages ----------
pages, buf = {}, []
for line in open(SLIDES, encoding='utf-8'):
    t = line.strip()
    m = re.fullmatch(r'(.*?)\s{5,}(\d{1,3})', t)
    if m and m.group(1):
        buf.append(m.group(1)); t = m.group(2)
    if re.fullmatch(r'\d{1,3}', t):
        pages[int(t)] = pages.get(int(t), '') + ' ' + ' '.join(buf); buf = []
    elif t: buf.append(t)
def norm(s): return re.sub(r'\s+', ' ', s).lower()
pages = {k: norm(v) for k, v in pages.items()}
QUOTES = [
 (6, 'medium 50-500 meters'), (6, 'over 1 mbps to 54 mbps'), (95, 'up to 100 ms, such as ieee 802.11'),
 (95, 'zigbee and bluetooth low energy (ble)'), (95, 'such as the bluetooth'), (95, 'ieee 802.11 mesh'),
 (8, 'temporary network for duration of meeting'), (7, 'bridges or routers'),
 (10, 'two or more basic service sets interconnected by ds'), (10, 'isolated or connected to backbone ds'),
 (12, 'three physical (phy) sub- layers'), (13, 'between 850 and 950 nm'), (14, '6 to 54 mbps'), (14, '5.5 and 11 mbps'),
 (15, '802.11g'), (17, 'even if a node cannot hear the rts'), (18, 'coexist with dcf and built on dcf'),
 (20, 'longest ifs'), (22, 'cwmin =32 and cwmax= 256'), (22, 'between 0 to cw-1'), (22, 'cw stops increase'),
 (23, 'virtual carrier sense'), (24, 'defer access the channel by nav time units plus difs'), (24, 'backoff after defer'),
 (26, 'locks out all asynchronous traffic'), (27, 'cf-end'), (28, 'superframe= cfp+cp'),
 (29, 'sifs<pifs<difs'), (29, 'foreshortened superframe'), (29, 'reset their navs to zero'),
 (31, 'probe request'), (32, 'proves the knowledge of a given password'), (32, 'only after the association process'),
 (33, 'timing and synchronization'), (34, '32-bit crc'), (39, 'eight traffic classes'), (39, 'arbitration interframe space'),
 (40, 'hybrid coordinator'), (42, 'dynamically elected or distributed'), (43, 'self-administering'),
 (43, 'radius of 10 meters'), (45, 'function as routers on demand'), (45, 'loop free'),
 (47, 'combinatorially stable'), (47, 'instantaneous computational capacity'), (48, 'out of the range of the sender'),
 (52, 'create routes only when necessary'), (52, 'periodic routing protocol within a local zone'),
 (53, 'no need to store routing tables'), (56, 'several orders of magnitude'), (56, 'broadcast communication paradigm'),
 (59, 'power, mobility, and task management planes'), (59, 'there are 5 layers'),
 (61, 'evolved packet core (epc)'), (62, 'evolved nodeb (enodeb)'), (63, 's1-mme'), (63, 's1-u'), (63, 'x2 interface'),
 (64, 'all data sent over the radio interface is encrypted'), (64, 'radio admission control'),
 (65, '1.4mhz up to 20mhz'), (65, 'higher than 300mbps when 4 by 4 mimo'), (65, '86mbps'), (65, 'up to 15km/h'),
 (65, '350 or even 500km/h'), (65, 'femtocells to 100km'), (66, '10 subframes'), (66, '0.5ms long'),
 (67, '12 subcarriers'), (67, 'either 7 or 6 ofdm symbols'), (67, 'extended cp is used when the cell size is large'),
 (68, 'ip packet flow with a defined qos'), (69, 'such as voip'), (69, 'maximum bit rate (mbr)'), (69, 'web browsing or ftp'),
 (70, 'default bearer has to be non-gbr'), (73, 'acknowledged mode'), (74, 'call admission control'),
 (74, 'does not have any impact on the bearer-level packet forwarding'), (75, 'link adaption'),
 (82, 'ipv6'), (82, 'launching point'), (83, 'interoperabilty'), (84, 'oneM2M'.lower()), (84, '2012'),
 (85, 'seven-layer'), (85, '2014'), (86, 'two parallel stacks'), (89, '802.11ah, 802.15.4g, and lora'),
 (90, 'ip and udp'), (99, 'websocket'), (96, 'the cost of the technology is the third determining factor'),
 (96, 'determines the size of the cell'), (105, '3g/lte or even satellite'), (106, 'any device with computing, storage, and network connectivity'),
 (106, 'keep sensitive data inside the local network'), (108, 'data reduction'), (109, 'wireless communication between the fog and the iot endpoint'),
 (109, 'batch processing on a subset'), (110, 'mist or edge'), (111, 'in no way replace the cloud'),
 (113, 'seconds or minutes for actions is passed along to an aggregation node'), (76, 'disaster relief'),
]
for pg, s in QUOTES:
    if norm(s) not in pages.get(pg, ''): bad(f'slide p.{pg}: quote not found: {s!r}')
sw7 = norm(open(SW7, encoding='utf-8').read())
if 'maximum delay spread' not in sw7: bad('Part 2 Ch7: delay spread quote')

# ---------- report ----------
print('ids:', len([i for i in ids if i in X.XPL]), '/ 39')
for qid in ids:
    if qid in lens:
        t = Q[qid]['type']; c, v, a = lens[qid]
        flag = ''
        if t == 'mcq' and not 250 <= v <= 600: flag = '  <-- MCQ length outside 250-600'
        if t != 'mcq' and not 600 <= a <= 1500: flag = '  <-- outside 600-1500'
        print(f'  {qid:4s} {t:5s} CJK {c:4d} | visible chars (no EN tmpl) {v:4d} | all visible {a:4d}{flag}')
if err:
    print('\nERRORS:'); [print(' -', e) for e in err]; sys.exit(1)
print('\nALL CHECKS PASSED')
