#!/usr/bin/python3
"""Page-specific clean-up before translation.

prep(page, s) → (s, keeps). Parts that must stay Chinese (they already have an English twin on the page) are cut
out and replaced by <!--KEEP:n--> comments, which the translator does not touch; restore() puts them back.
The hub is bilingual: questions keep their Chinese lines, answers show English and then 中文.
"""
import re


class Keeper:
    def __init__(self):
        self.parts = []

    def __call__(self, frag):
        self.parts.append(frag)
        return f'<!--KEEP:{len(self.parts) - 1}-->'


def block_end(s, i, tag):
    """End index of the balanced <tag …> block that starts at s[i]."""
    depth = 0
    for m in re.compile(rf'<{tag}\b|</{tag}>').finditer(s, i):
        depth += 1 if m.group(0) != f'</{tag}>' else -1
        if depth == 0:
            return m.end()
    raise ValueError(s[i:i + 80])


def p2_practice(s, keep):
    # question translations and table-header glosses stay Chinese, under the English original
    s, n1 = re.subn(r'<p class="zh" lang="zh-CN">.*?</p>', lambda m: keep(m.group(0)), s, flags=re.S)
    s, n2 = re.subn(r'<br><span class="zh-th">[^<]*</span>', lambda m: keep(m.group(0)), s)
    # Chinese solution: moved after its English twin; both are shown
    n3 = 0
    while True:
        i = s.find('<div class="sol sol-zh">')
        if i < 0:
            break
        j = block_end(s, i, 'div'); zh = s[i:j]
        s = s[:i] + s[j:]
        k = s.find('<div class="sol sol-en"', i)
        e = block_end(s, k, 'div')
        s = s[:e] + '\n    ' + keep(zh) + s[e:]; n3 += 1
    # Chinese lines inside the English 知识讲解 boxes (add_xpl.py): already bilingual
    n6 = 0
    while True:
        i = s.find('<span class="zhsub xz" lang="zh-CN">')
        if i < 0:
            break
        j = block_end(s, i, 'span'); s = s[:i] + keep(s[i:j]) + s[j:]; n6 += 1
    assert n6 > 100, n6
    s = s.replace('<div class="wrap lang-en" id="root">', '<div class="wrap" id="root">')
    s, n4 = re.subn(r'(<label class="toggle"><input type="checkbox" id="zhMode" checked> )题目中文对照(</label>)',
                    lambda m: m.group(1) + 'Show ' + keep('中文') + m.group(2), s)
    s, n5 = re.subn(r'<span class="seg" id="langSeg".*?</button></span>', '<span id="langSeg" hidden></span>', s, flags=re.S)
    old = "setLang(store.get('ee6129-p2:sollang')==='zh'?'zh':'en');"
    s = s.replace(old, "root.classList.remove('lang-en','lang-zh');")
    assert n1 > 50 and n2 >= 3 and n3 == 33 and n4 == 1 and n5 == 1 and old not in s, (n1, n2, n3, n4, n5)
    return s


def hw1(s, keep):
    # the 中文答案 tab stays as it is (the "English answers" tab is its twin)
    i = s.find('<section id="zh" role="tabpanel"')
    j = block_end(s, i, 'section')
    s = s[:i] + keep(s[i:j]) + s[j:]
    s, n = re.subn(r'(<button class="tab" role="tab" id="tab-zh"[^>]*>)中文答案(</button>)',
                   lambda m: m.group(1) + keep('中文答案') + m.group(2), s)
    assert n == 1
    return s


def homework_sw(s, keep):
    # already bilingual (question + 中文, English answer + 中文答案): used as it is
    return keep(s)


def bc_practice(s, keep):
    old = "fbtn('只看'+TYPE[t]+'题','t:'+t)"
    assert old in s
    return s.replace(old, "fbtn(TYPE[t]+' only','t:'+t)")


def fix_js(pairs):
    """Animation strings built from pieces whose shared word (第 …) needs a different English word per figure."""
    def f(s, keep):
        for old, new in pairs:
            assert old in s, old
            s = s.replace(old, new)
        return s
    return f


def quiz_summary(s, keep):
    # symbol tables have a 中文 column next to the English one: keep it Chinese
    n = 0
    def table(m):
        nonlocal n
        def row(r):
            nonlocal n
            n += 1
            return r.group(1) + keep(r.group(2)) + r.group(3)
        return re.sub(r'(<tr><td>(?:(?!</td>).)*</td><td>)((?:(?!</td>).)*)(</td>)', row, m.group(0), flags=re.S)
    s = re.sub(r'<table class="sym">.*?</table>', table, s, flags=re.S)
    assert n > 50, n
    return s


PREP = {'quiz-summary': quiz_summary, 'p2-practice': p2_practice, 'hw1': hw1, 'homework-sw': homework_sw, 'bc-practice': bc_practice,
        'partB': fix_js([("'第 ' + (i + 1) + ' 次 CW = '", "'Attempt ' + (i + 1) + ': CW = '")]),
        'partC': fix_js([("'第 ' + (Math.floor(th / 24) + 1) + ' 天 '", "'Day ' + (Math.floor(th / 24) + 1) + ' · '")])}


def prep(page, s):
    keep = Keeper()
    f = PREP.get(page)
    return (f(s, keep) if f else s), keep.parts


def restore(s, parts):
    return re.sub(r'<!--KEEP:(\d+)-->', lambda m: parts[int(m.group(1))], s)
