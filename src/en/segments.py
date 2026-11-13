#!/usr/bin/python3
"""Find and replace the Chinese text units of a built EE6129 page (for the English practice hub).

A unit is one of
  html  – a run of text + inline tags between two block-level tags (a sentence/paragraph with its <b>, <sub>, math …)
  attr  – a title / aria-label / placeholder / alt / data-label / value attribute
  js    – a string literal inside <script> (double-quoted ones are JSON-decoded first)
that contains at least one CJK character. walk(s, fn) rebuilds the page with fn(kind, text) in place of each unit.
"""
import json, re

CJK = re.compile(r'[　-〿一-鿿！-～]')
TOK = re.compile(r'<!--.*?-->|<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[a-zA-Z/!][^>]*>|[^<]+|<', re.S)
INLINE = {'a', 'abbr', 'b', 'bdi', 'br', 'cite', 'code', 'em', 'i', 'kbd', 'mark', 'q', 's', 'samp', 'small', 'span',
          'strong', 'sub', 'sup', 'u', 'var', 'wbr', 'del', 'ins', 'tspan', 'time', 'nobr'}
ATTR = re.compile(r'''(\s(?:title|aria-label|placeholder|alt|data-label|value|label)=)("[^"]*"|'[^']*')''')


def has(s):
    return bool(CJK.search(s))


def _tagname(tok):
    m = re.match(r'</?([a-zA-Z][\w:-]*)', tok)
    return m.group(1).lower() if m else None


def _attrs(tok, fn):
    def rep(m):
        q = m.group(2)[0]; v = m.group(2)[1:-1]
        if not has(v):
            return m.group(0)
        return m.group(1) + q + fn('attr', v).replace(q, '&quot;' if q == '"' else '&#39;') + q
    return ATTR.sub(rep, tok)


def _js(code, fn):
    out = []; i = 0; n = len(code)
    while i < n:
        c = code[i]
        if c == '/' and code.startswith('//', i):
            j = code.find('\n', i); j = n if j < 0 else j
            out.append(code[i:j]); i = j; continue
        if c == '/' and code.startswith('/*', i):
            j = code.find('*/', i + 2); j = n if j < 0 else j + 2
            out.append(code[i:j]); i = j; continue
        if c in '"\'`':
            j = i + 1
            while j < n and code[j] != c:
                j += 2 if code[j] == '\\' else 1
            raw = code[i + 1:j]
            if has(raw) and c != '`':
                if c == '"':
                    try:
                        txt = json.loads('"' + raw + '"')
                        tr = fn('js', txt)
                        new = raw if tr == txt else json.dumps(tr, ensure_ascii=False)[1:-1].replace('</', '<\\/')
                    except ValueError:
                        new = fn('js', raw)
                else:
                    tr = fn('js', raw)
                    new = raw if tr == raw else tr.replace("\\'", "'").replace("'", "\\'")
                out.append(c + new + c)
            else:
                out.append(code[i:j + 1])
            i = j + 1; continue
        out.append(c); i += 1
    return ''.join(out)


def walk(s, fn):
    out = []; run = []

    def flush():
        if not run:
            return
        txt = ''.join(run); run.clear()
        if has(txt):
            core = txt.strip()
            lead = txt[:len(txt) - len(txt.lstrip())]; trail = txt[len(txt.rstrip()):]
            out.append(lead + fn('html', core) + trail)
        else:
            out.append(txt)

    for m in TOK.finditer(s):
        t = m.group(0)
        if t.startswith('<script'):
            flush()
            k = t.find('>') + 1; e = t.rfind('</script>')
            out.append(t[:k] + _js(t[k:e], fn) + t[e:]); continue
        if t.startswith('<!--') or t.startswith('<style'):
            flush(); out.append(t); continue
        if t.startswith('<') and len(t) > 1:
            name = _tagname(t)
            if name in INLINE:
                run.append(t); continue
            flush(); out.append(_attrs(t, fn)); continue
        run.append(t)
    flush()
    return ''.join(out)


def units(s):
    seen = {}
    def rec(kind, txt):
        seen.setdefault(txt, kind); return txt
    walk(s, rec)
    return seen


def visible_cjk(s):
    """CJK characters left in what a reader sees (text, attributes, script strings; not comments)."""
    left = []
    def rec(kind, txt):
        left.append(txt); return txt
    walk(s, rec)
    return left
