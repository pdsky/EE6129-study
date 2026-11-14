# Brief: 知识讲解 + 详细解析 for every EE6129 practice question

The student (M.Sc., Chinese native, writes the final exam in English, exam Fri 27 Nov 2026) asked:
"把练习题里面的东西给我添加相应的知识讲解，给我详细的解析" — for every practice question, add the
underlying knowledge explained from scratch plus a detailed, step-by-step analysis.

Each question gets ONE collapsible box (we wrap it in `<details class="deep">`; you write only the
summary title and the body HTML). The box is shown after the existing solution, so do not repeat
the existing solution / 本题知识点 / 题意讲解 boxes word for word — go deeper: teach the concept,
explain *why* each step is done, show how to compute it, and how to write it in the exam.

## Body structure (Chinese, beginner level, short sentences)

```html
<h4><span class="st">知识讲解</span>小标题</h4>
<p>… the concept from zero: what it is, why it exists, the formula and what every symbol means,
   where it is in the slides (讲义 Part A p.xx / 第 3 章 p.xx) …</p>
<div class="tw"><table class="mini"><thead><tr><th>…</th></tr></thead><tbody><tr><td>…</td></tr></tbody></table></div>   (optional)
<h4><span class="st">详细解析</span>小标题</h4>
<p>or <ol><li> — each step: 做什么 → 为什么 → 怎么算</p>
<div class="calc">numbers with units, one line per calculation</div>
<h4><span class="st">易错</span>…</h4>
<ul><li>…</li></ul>
<h4><span class="st">考试</span>英文写法</h4>
<div class="tmpl" lang="en"><p>Model exam answer in English, the way it should be written on the paper.</p></div>
<div class="ans">一句话：…</div>
```

- More than one 知识讲解 / 详细解析 section is fine (e.g. one per sub-part (a)(b)(c)); add a
  `<span class="st">课外补充</span>` section for anything not in the slides and say so explicitly.
- MCQ: 知识讲解, then 逐项分析 (each option: why right / why wrong), then a memory hook, then 一句话.
  The 考试 section is optional for MCQ.
- Short-answer / descriptive: 知识讲解, then the answer points expanded (why each point matters),
  then the English answer template (that is what earns marks), then 一句话.
- Calculation: 知识讲解 (formula + symbols + where it comes from), 详细解析 (every step, calculator
  hints e.g. log₂x = log₁₀x / 0.301, dB ↔ linear), a sanity check, 易错, 考试英文写法, 一句话.
- Typical length: MCQ 250–600 Chinese characters; calculation / descriptive 600–1500.

## Allowed HTML only
`h4 > span.st`, `p`, `ul`, `ol`, `li`, `b`, `i`, `sub`, `sup`, `br`, `div.calc`, `div.tw > table.mini`
(thead/tbody/tr/th/td), `div.ans`, `div.tmpl[lang=en] > p`. No LaTeX, no MathJax, no `<` or `>`
characters in text (write `&lt;` / `&gt;`), no inline styles, no scripts, no images, no links.
Math in plain Unicode: γ, σ², √, ×, ≈, log₁₀, ₀₁₂, ⁻¹, etc.

## Content rules
1. Ground everything in the course: slide text is in
   `/run/media/paddy/新加卷/NTUlearn/EE6129_text/` (`partA.txt`, `partB.txt`, `partC.txt`,
   `sw/Chapter_*.txt` for Part 2). The study pages with explanations are in
   `/run/media/paddy/新加卷/NTUlearn/EE6129-study/` (`p2-learn.html`, `partA.html`, `partB.html`,
   `partC.html`). Lecturer emphasis (what was said in class) is in `src/teacher/notes.py` — mention
   it as 老师课上强调 where relevant. Cite slide pages.
2. Read the question and its current solution first (source files are given in your task), and stay
   consistent with that solution's numbers and answer. If you think the existing solution or the
   slide is wrong, do NOT silently change it: explain in the box neutrally only if you are sure,
   and list it in `NOTES` (see output).
3. Every number you write must be checked by a script: write
   `/run/media/paddy/新加卷/NTUlearn/EE6129-study/src/explain/check_<group>.py` and run it with
   `/usr/bin/python3` (never conda python). Fix any mismatch before finishing.
4. Plain, friendly Chinese for a beginner; English technical terms in parentheses the first time.
   Use 中文 punctuation in Chinese text.

## Output
Write ONLY your own files in `/run/media/paddy/新加卷/NTUlearn/EE6129-study/src/explain/`
(do not edit or delete any other file):

`<group>.py`:
```python
# -*- coding: utf-8 -*-
XPL = {
  'id1': {'title': '知识讲解 + 详细解析：……(短，≤ 30 字)', 'zh': '''<h4>…</h4>…'''},
  ...
}
NOTES = '''possible errors in the existing solution / slides, one per line (empty if none)'''
```
Then verify: `/usr/bin/python3 -c "import importlib.util,sys; ..."` — at minimum import the file,
check every required id is present, every body has 知识讲解 and 一句话, and that the HTML tags are
balanced (e.g. with html.parser). Report in your final message: ids done, anything skipped, NOTES.
