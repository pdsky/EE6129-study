#!/usr/bin/python3
"""Mark the 23 Oct 2026 Quiz (CA2) scope and the formulas to memorise.

Scope (lecture slide + week-8/9/10 recordings, see src/teacher/notes.py): Ch1b, Ch2, Practice 1–2;
Ch1a and Ch3–7 not tested; no integration. Formula status follows the recordings: 背 = blue box,
must memorise; 尽量记 = lecturer said try to remember; 考试给 = given in the paper, know the meaning.

Learn fragments (learn_01..07): a Quiz box at the top of ch0, badges on chapter heads and section
headings, and a status line under selected formula cards. Practice fragments (prac_1..8): badges on
the Practice group headings and on every P1/P2/mock question. Everything this script adds carries the
class qz / qzline / qzbox and is removed before re-inserting, so it is idempotent.
Run before build_learn.py and build_practice.py.
"""
import pathlib, re

B = pathlib.Path(__file__).parent

IN, OUT = '<span class="qz in">Quiz</span>', '<span class="qz out">Quiz 不考</span>'
BADGE = {'must': '背', 'try': '尽量记', 'give': '考试给', 'note': 'Quiz'}

CHAPTER = {'ch1': '<span class="qz in">Quiz 范围：第 1b 章</span>',
           'ch2': '<span class="qz in">Quiz 范围</span>',
           **{f'ch{i}': '<span class="qz out">Quiz 不考 · 期末考</span>' for i in range(3, 8)}}

SECTION_OUT = {'1.1'}                                    # Ch1a
SECTION_IN = {'1.2', '1.3', '1.4', '1.5'} | {f'2.{i}' for i in range(1, 10)}

# (fragment, formula-card label substring, kind, text)
CARDS = [
  ('learn_01.html', '四条规则（第 1b 章', 'must', '贝叶斯公式是蓝框，要背。加法、乘法、全概率要会用；全概率必须对所有 A<sub>i</sub> 求和。'),
  ('learn_01.html', '定义（第 1b 章 p.10–11）', 'must', '期望 E[X] = Σx·P(x) 要背，离散分布的求和会考。方差公式要会用。'),
  ('learn_01.html', 'PDF 与 CDF（第 1b 章', 'note', 'Quiz 不考积分：知道"概率 = PDF 下的面积""CDF = P(X ≤ x)"就够了。'),
  ('learn_01.html', 'Q 函数（第 2 章 p.15', 'give', '考卷附 Q 函数表，数值不用背；正查、反查都要会，一定会用到。'),
  ('learn_02.html', '简化路径损耗模型（p.8）', 'must', '线性和 dB 两种形式都要背，考试不给。γ 的取值范围表不用背。'),
  ('learn_02.html', '中断概率（p.15）', 'must', 'P<sub>out</sub> = Q(余量/σ) 要背。'),
  ('learn_02.html', '瑞利衰落（p.25–26）', 'must', '要背 SNR 的指数分布 p(γ) = (1/γ̄)e<sup>−γ/γ̄</sup> 和瑞利中断 P(γ &lt; γ₀) = 1 − e<sup>−γ₀/γ̄</sup>（老师说"经常出现"）。包络的瑞利 PDF 不用背。'),
  ('learn_02.html', '莱斯分布与莱斯因子', 'give', '考试会给，懂 K 的含义即可。'),
  ('learn_02.html', '平均时延与 rms 时延扩展', 'give', '公式考试会给，要会按功率加权去算。'),
  ('learn_02.html', '瑞利衰落的 LCR 与 AFD', 'give', '公式考试会给，要会解释 ρ 和 f<sub>m</sub>。'),
  ('learn_02.html', 'AWGN 信道的香农容量', 'must', 'C = B log₂(1 + SNR) 要背，SNR 用线性值。'),
  ('learn_02.html', '瑞利衰落的衰落余量', 'try', '尽量记：老师说"有点难记，但要试着记"。'),
  ('learn_02.html', '注水法（p.54）', 'try', '功率分配式尽量记，注水法要会算。'),
]
# inline 背 badge after an exact anchor string
INLINE = [('learn_02.html', '<mark class="hl">\\(\\sigma_{T_m}/T_s<0.1\\)：平坦衰落</mark>')]

BOX = '''      <div class="qzbox">
        <div class="lbl">10 月 23 日 Quiz · 周五 3:00–3:30 pm · LT23 · 闭卷 30 分钟 · 3 道短题</div>
        <p><b>范围</b>：第 1b 章概率复习（本页 1.2–1.5）、第 2 章无线信道（本页 2.1–2.8）、Practice 1–2（练习页 P1、P2）。<b>不考</b>：第 1a 章（1.1）、第 3–7 章、积分计算（离散求和会考）。</p>
        <p><b>页面标记</b>：<span class="qz in">Quiz</span> 本节在范围内　<span class="qz out">Quiz 不考</span>　公式卡下方：<span class="qz must">背</span> 讲义蓝框，考试不给，要背　<span class="qz try">尽量记</span>　<span class="qz give">考试给</span> 只要懂含义。</p>
        <p><b>必背公式（录音里老师点名）</b>：贝叶斯公式；E[X] = Σx·P(x)；简化路径损耗模型（线性 + dB）；P<sub>out</sub> = Q(余量/σ)；平坦衰落 σ<sub>Tm</sub>/T<sub>s</sub> &lt; 0.1；SNR 指数分布 p(γ) = (1/γ̄)e<sup>−γ/γ̄</sup>；瑞利中断 1 − e<sup>−γ₀/γ̄</sup>；香农 C = B log₂(1 + SNR)。<b>尽量记</b>：衰落余量公式、注水功率分配式。</p>
        <p><b>要带</b>：认可的计算器、带照片的证件、正常大小的答题纸和笔；提前 10–15 分钟到。字写清楚，dB ↔ 线性换算要写出来，漏了会扣分。</p>
      </div>
'''


def strip(s):
    s = re.sub(r'[ \t]*<div class="qzbox">.*?\n      </div>\n', '', s, flags=re.S)
    s = re.sub(r'\n[ \t]*<div class="qzline">.*?</div>(?=\n)', '', s)
    return re.sub(r'<span class="qz [a-z]+">[^<]*</span>', '', s)


def learn():
    for i in range(1, 8):
        f = B / f'learn_{i:02d}.html'
        s = strip(f.read_text(encoding='utf-8'))
        for ch, badge in CHAPTER.items():
            m = re.search(rf'<section class="chapter" id="{ch}">\s*<div class="chapter-head">.*?</h2>', s, re.S)
            if m:
                s = s[:m.end()] + badge + s[m.end():]
        def h3(m):
            num = m.group(1)
            tag = OUT if num in SECTION_OUT else IN if num in SECTION_IN else ''
            return m.group(0)[:-5] + tag + '</h3>'
        s = re.sub(r'<h3><span class="zh-num">([\d.]+)</span>.*?</h3>', h3, s)
        if f.name == 'learn_01.html':
            m = re.search(r'<section class="chapter" id="ch0">\s*<div class="chapter-head">.*?</div>\n', s, re.S)
            s = s[:m.end()] + BOX + s[m.end():]
        for frag, label, kind, text in CARDS:
            if frag != f.name:
                continue
            a = s.find(f'<div class="flbl">{label}')
            assert a >= 0, label
            e = s.find('</div>', s.find('<div class="fexpr">', a)) + len('</div>')
            s = s[:e] + f'\n        <div class="qzline"><span class="qz {kind}">{BADGE[kind]}</span>{text}</div>' + s[e:]
        for frag, anchor in INLINE:
            if frag == f.name:
                assert anchor in s, anchor
                s = s.replace(anchor, anchor + '<span class="qz must">背</span>', 1)
        f.write_text(s, encoding='utf-8')


def practice():
    for i in range(1, 9):                                # prac_8 = self-written mock Quiz
        f = B / f'prac_{i}.html'
        s = strip(f.read_text(encoding='utf-8'))
        inq = i <= 2 or i == 8
        s = re.sub(r'(<div class="group" id="P\d"><h2>.*?)(</h2>)',
                   lambda m: m.group(1) + ('<span class="qz in">Quiz 范围</span>' if inq else '<span class="qz out">Quiz 不考</span>') + m.group(2), s, count=1)
        if inq:
            s = re.sub(r'(<article class="ex" id="p\dq\d+">\s*<header><span class="pg">[^<]*</span><h3>.*?)(</h3>)',
                       lambda m: m.group(1) + IN + m.group(2), s, flags=re.S)
        f.write_text(s, encoding='utf-8')


learn()
practice()
print('quiz marks: learn_01–07, prac_1–8')
