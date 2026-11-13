#!/usr/bin/python3
"""Put an animated figure beside every section that has one (src/anim/<page>_*.js), repo copy and artifact copy.

Each section = an <h3> with <span class="zh-num">N.M</span> plus everything after it up to the next h2/h3,
past-exam block or chapter navigation. It is wrapped as

  <!--ANIM:open ID--><div class="asec" id="asec-ID">h3<!--ANIM:fig ID--><aside class="asec-fig">FIGS</aside><div class="asec-body"><!--/ANIM:fig ID-->
  ...section body...
  <!--ANIM:close ID--></div></div>

and the CSS + core + that page's animation scripts go between <!--ANIM:assets--> and <!--/ANIM:assets--> at the end.
Idempotent: every run strips the previous wrapping first.  Called at the end of inject_teacher.py.
Usage: inject_anim.py            (all pages)
       inject_anim.py --strip    (remove all animations)
"""
import pathlib, re, sys
from html.parser import HTMLParser

T = pathlib.Path(__file__).resolve().parent
REPO = T.parents[1]
ART = pathlib.Path('/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts')
PAGES = {'p2': 'p2-learn.html', 'A': 'partA.html', 'B': 'partB.html', 'C': 'partC.html'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
STOP_CLASSES = ('pastq-block', 'chapter-nav', 'next-up', 'chapter-head')


def strip(s):
    s = re.sub(r'<!--ANIM:assets-->.*?<!--/ANIM:assets-->\n?', '', s, flags=re.S)
    s = re.sub(r'<!--ANIM:open (\S+)--><div class="asec"[^>]*>', '', s)
    s = re.sub(r'<!--ANIM:fig (\S+)-->.*?<!--/ANIM:fig \1-->', '', s, flags=re.S)
    s = re.sub(r'<!--ANIM:close (\S+)--></div></div>', '', s)
    s = re.sub(r'<!--EXHIT:(\S+)-->.*?<!--/EXHIT:\1-->', '', s, flags=re.S)
    return s


class Walker(HTMLParser):
    """Record, for every element, its start offset, end offset, depth, tag and class."""
    def __init__(self, s):
        super().__init__(convert_charrefs=False)
        self.s = s
        self.lines = [0]
        for m in re.finditer('\n', s):
            self.lines.append(m.end())
        self.stack, self.nodes, self.comments, self.warn = [], [], [], []

    def off(self):
        ln, col = self.getpos()
        return self.lines[ln - 1] + col

    def handle_starttag(self, tag, attrs):
        o = self.off()
        cls = dict(attrs).get('class') or ''
        node = {'tag': tag, 'start': o, 'end': None, 'depth': len(self.stack), 'cls': cls,
                'parent': self.stack[-1] if self.stack else None}
        self.nodes.append(node)
        if tag not in VOID:
            self.stack.append(node)
        else:
            node['end'] = o + len(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        o = self.off()
        self.nodes.append({'tag': tag, 'start': o, 'end': o + len(self.get_starttag_text()), 'depth': len(self.stack),
                           'cls': dict(attrs).get('class') or '', 'parent': self.stack[-1] if self.stack else None})

    def handle_endtag(self, tag):
        o = self.off()
        if tag in VOID:
            return
        if not any(n['tag'] == tag for n in self.stack):
            self.warn.append(f'stray </{tag}> at {o}')
            return
        while self.stack:
            n = self.stack.pop()
            n['end_tag'] = o
            n['end'] = self.s.find('>', o) + 1
            if n['tag'] == tag:
                break
            self.warn.append(f'unclosed <{n["tag"]}> closed by </{tag}> at {o}')

    def handle_comment(self, data):
        self.comments.append({'start': self.off(), 'data': data, 'parent': self.stack[-1] if self.stack else None})


def sections_of(s):
    """{ 'N.M': (h3_start, h3_end, sec_end) } for h3s inside a chapter."""
    w = Walker(s)
    w.feed(s)
    w.close()
    out = {}
    nodes = w.nodes
    for i, n in enumerate(nodes):
        if n['tag'] != 'h3':
            continue
        m = re.match(r'<h3[^>]*>\s*<span class="zh-num">([^<]+)</span>', s[n['start']:n['start'] + 200])
        if not m:
            continue
        num = m.group(1).strip()
        par = n['parent']
        if par is None or 'chapter' not in par['cls'].split():
            continue
        end = par.get('end_tag', len(s))
        for k in nodes[i + 1:]:
            if k['start'] >= end:
                break
            if k['parent'] is not par:
                continue
            c = k['cls'].split()
            if k['tag'] in ('h2', 'h3') or any(x in c for x in STOP_CLASSES):
                end = k['start']
                break
        for c in w.comments:
            if c['parent'] is par and n['end'] <= c['start'] < end and 'PASTQ:begin' in c['data']:
                end = c['start']
                break
        # don't swallow trailing whitespace into the wrapper
        e = end
        while e > n['end'] and s[e - 1] in ' \t\n':
            e -= 1
        out[num] = (n['start'], n['end'], e)
    if w.warn:
        print('  html warnings:', len(w.warn), w.warn[:3])
    return out


def load_page_js(page):
    files = sorted(T.glob(f'{page}_*.js'))
    js, ids = [], []
    for f in files:
        src = f.read_text(encoding='utf-8')
        if re.search(r'</script', src, re.I):
            raise SystemExit(f'{f.name}: contains </script')
        found = re.findall(r"ANIM\.reg\(\s*'([^']+)'", src)
        for i in found:
            if not i.startswith(page + ':'):
                raise SystemExit(f'{f.name}: id {i} does not start with {page}:')
        ids += found
        js.append(f'/* {f.name} */\n' + src)
    return js, ids


def exhit_html(page, sec, qs):
    """The 🎯 期末考点 line under a section heading: which of the 4 past papers tested this section."""
    from exam_hits import PAPERS, SHORT, years
    n = years(qs)
    hit = {q['paper'] for q in qs}
    lab = {4: '4 份卷都考了', 3: '4 份卷考了 3 份', 2: '4 份卷考了 2 份', 1: '考过 1 次'}[n]
    dots = ''.join(f'<i class="{"on" if p in hit else ""}" title="{name}"></i>' for p, name in PAPERS)
    chips = []
    for q in qs:
        t = f'{SHORT[q["paper"]]} {q["q"]}'
        tip = html_attr(q['topic'])
        if q['page'] == page:
            chips.append(f'<a class="ex-q" href="#pq-{q["id"]}" title="{tip}">{t}</a>')
        else:
            chips.append(f'<span class="ex-q" title="{tip}">{t}</span>')
    sid = page + '-' + sec.replace('.', '_')
    return (f'<!--EXHIT:{sid}--><div class="exhit y{n}"><span class="ex-k">🎯 期末考点</span>'
            f'<span class="ex-dots" aria-hidden="true">{dots}</span><span class="ex-n">{lab}</span>{"".join(chips)}</div><!--/EXHIT:{sid}-->')


def html_attr(t):
    return t.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def fig_html(ids):
    return ''.join(f'<figure class="anim" data-anim="{i}"></figure>' for i in ids)


def inject(path, page, js, ids):
    if not path.exists():
        return 0
    s = strip(path.read_text(encoding='utf-8'))
    if not ids:
        path.write_text(s, encoding='utf-8')
        return 0
    by_sec = {}
    for i in ids:
        sec = i.split(':', 1)[1].split('/')[0]
        by_sec.setdefault(sec, []).append(i)
    from exam_hits import by_section
    hits = {k.split(':', 1)[1]: v for k, v in by_section().items() if k.split(':', 1)[0] == page}
    secs = sections_of(s)
    nohit = [k for k in hits if k not in secs]
    if nohit:
        raise SystemExit(f'{path}: exam-hit sections not found: {nohit}')
    for sec in sorted(hits, key=lambda k: secs[k][0], reverse=True):
        h1 = secs[sec][1]
        s = s[:h1] + exhit_html(page, sec, hits[sec]) + s[h1:]
    secs = sections_of(s)
    missing = [k for k in by_sec if k not in secs]
    if missing:
        raise SystemExit(f'{path}: sections not found: {missing}')
    # apply from the end so offsets stay valid
    for sec in sorted(by_sec, key=lambda k: secs[k][0], reverse=True):
        h0, h1, e = secs[sec]
        sid = page + '-' + sec.replace('.', '_')
        m = re.match(r'<!--EXHIT:(\S+)-->.*?<!--/EXHIT:\1-->', s[h1:], re.S)
        if m:  # keep the exam line right under the heading, before the figure
            h1 += m.end()
        s = (s[:h0] + f'<!--ANIM:open {sid}--><div class="asec" id="asec-{sid}">' + s[h0:h1]
             + f'<!--ANIM:fig {sid}--><aside class="asec-fig">{fig_html(by_sec[sec])}</aside><div class="asec-body"><!--/ANIM:fig {sid}-->'
             + s[h1:e] + f'<!--ANIM:close {sid}--></div></div>' + s[e:])
    css = (T / 'anim.css').read_text(encoding='utf-8')
    core = (T / 'core.js').read_text(encoding='utf-8')
    # one <script> per file, so a mistake in one file cannot take the other animations down with it
    assets = ('<!--ANIM:assets--><style id="anim-css">\n' + css + '</style>\n<script>\n' + core + '\n</script>\n'
              + ''.join('<script>\n' + j + '\n</script>\n' for j in js) + '<!--/ANIM:assets-->\n')
    k = s.rfind('</body>')
    s = s[:k] + assets + s[k:] if k >= 0 else s.rstrip('\n') + '\n' + assets
    path.write_text(s, encoding='utf-8')
    return len(by_sec)


def main():
    stripping = '--strip' in sys.argv
    res = []
    for page, fn in PAGES.items():
        js, ids = ([], []) if stripping else load_page_js(page)
        if len(set(ids)) != len(ids):
            raise SystemExit(f'{page}: duplicate animation ids')
        a = inject(REPO / fn, page, js, ids)
        b = inject(ART / fn, page, js, ids)
        res.append(f'{page} {a}/{b}')
    print('animations (sections):', ', '.join(res))


if __name__ == '__main__':
    main()
