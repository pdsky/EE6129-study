#!/usr/bin/python3
"""Page-specific clean-up before translation (drop the Chinese copies that already have an English twin)."""
import re


def drop_div(s, opener):
    """Remove every <div …opener…> … </div> block (balanced)."""
    while True:
        i = s.find(opener)
        if i < 0:
            return s
        depth = 0; j = i
        for m in re.compile(r'<div\b|</div>').finditer(s, i):
            depth += 1 if m.group(0) == '<div' else -1
            if depth == 0:
                j = m.end(); break
        a = s.rfind('\n', 0, i) + 1
        if s[a:i].strip() == '':
            i = a
        s = s[:i] + s[j:]


def p2_practice(s):
    s = re.sub(r'\n[ \t]*<p class="zh" lang="zh-CN">.*?</p>', '', s, flags=re.S)
    s = re.sub(r'<br><span class="zh-th">[^<]*</span>', '', s)
    s = drop_div(s, '<div class="sol sol-zh">')
    s = s.replace('<label class="toggle"><input type="checkbox" id="zhMode" checked> 题目中文对照</label>',
                  '<input type="checkbox" id="zhMode" hidden>')
    s, n = re.subn(r'<span class="seg" id="langSeg".*?</button></span>', '<span id="langSeg" hidden></span>', s, flags=re.S)
    assert n == 1
    s = s.replace("setLang(store.get('ee6129-p2:sollang')==='zh'?'zh':'en');", "setLang('en');")
    assert 'sol-zh">' not in s and 'id="zhMode" hidden' in s and "setLang('en');" in s
    return s


def drop_tag(s, opener, tag):
    """Remove the first <tag …> block that starts with `opener` (balanced on `tag`)."""
    i = s.find(opener)
    assert i >= 0, opener
    depth = 0
    for m in re.compile(rf'<{tag}\b|</{tag}>').finditer(s, i):
        depth += 1 if m.group(0) != f'</{tag}>' else -1
        if depth == 0:
            return s[:i] + s[m.end():]
    raise ValueError(opener)


def hw1(s):
    # the 中文答案 tab has the same content as "English answers": keep the English one only
    s = re.sub(r'\n[ \t]*<button class="tab" role="tab" id="tab-zh"[^\n]*</button>', '', s)
    s = drop_tag(s, '<section id="zh" role="tabpanel"', 'section')
    assert 'id="tab-zh"' not in s and 'id="zh1a"' not in s
    return s


def homework_sw(s):
    # no language switch; drop the Chinese translation of the essay (the English essay is right above it)
    s = re.sub(r'<span class="seg" role="group".*?</span>', '', s, count=1, flags=re.S)
    s = s.replace("var m = 'both'; try { m = localStorage.getItem('hw-sw-lang') || 'both'; } catch(e){}", "var m = 'both';")
    s = drop_tag(s, '<div class="ans zh">\n      <div class="lbl">中文译文', 'div')
    assert "var m = 'both';\n" in s and '中文译文' not in s
    return s


def bc_practice(s):
    old = "fbtn('只看'+TYPE[t]+'题','t:'+t)"
    assert old in s
    return s.replace(old, "fbtn(TYPE[t]+' only','t:'+t)")


PREP = {'p2-practice': p2_practice, 'hw1': hw1, 'homework-sw': homework_sw, 'bc-practice': bc_practice}


def prep(page, s):
    return PREP.get(page, lambda x: x)(s)
