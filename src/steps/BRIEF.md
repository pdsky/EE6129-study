# Brief: expand every worked solution step by step (EE6129 practice page)

The student (M.Sc., Chinese native, writes the final exam in English, exam 27 Nov 2026) saw the
new P3 Q1 solution and asked: "每道题都给我这样" — make every question's main solution as detailed.

## The reference (read it first)
- Chinese: `src/p2build/prac_3.html`, article `id="p3q1"`, the `<ol class="steps">` inside
  `<div class="sol sol-zh">` (6 steps).
- English: `src/p2build/sol_en.py`, `EN['p3q1']['steps']`.

What makes it good:
1. Each step starts with `<b>步骤名</b>：` and says what this step does
   (e.g. 拆开（找方向）, 验正交, 求能量, 归一化, 坐标和自检, (b) 维数).
2. The formula in symbols first, then the numbers substituted, then the result with units.
   No jumps: every intermediate value is written down.
3. One sentence of *why* (where the formula comes from, why this approach; slide page such as
   讲义第 2 章 p.xx if you know it).
4. Conversions and lookups are explicit: dB ↔ linear, kHz → Hz, log₂x = log₁₀x / 0.301,
   Q-table / Erlang-B table entry used.
5. A check at the end where possible (back-substitute, sums, energy/units, order of magnitude), marked ✓.
6. Multi-part questions: put (a)/(b)/(c) in the step names.

Typical size: 4–8 steps, each 2–5 lines. Don't pad. Each question already has a separate
"知识讲解 + 详细解析" box that teaches the theory, so focus on the calculation chain, not on
re-teaching the concept from zero. For descriptive (non-calculation) parts, expand each answer
point with one sentence of why it is true, keeping the model answer.

## Numbers
- Recompute every number with `/usr/bin/python3` (never mental arithmetic). Put scratch scripts in
  `src/steps/_work/<your group>/` (on this data drive; never /tmp).
- Keep the rounding style of the existing answer.
- If an existing answer is wrong: fix it in the steps AND in the answer line (`.ans` / `wans`), and
  list it in your report with the evidence. Never change an `official` (官方答案) line; if you
  disagree with it, only report.
- Part 2 mock quiz (prac_8) numbers are also in `src/p2build/verify_mock.py`; exams have
  `src/exams/verify.py`. Keep them consistent; report if they disagree.

## HTML safety (important)
- Never write a raw `<` or `>` meaning less/greater than, in text or in math. Use `&lt;` / `&gt;` in
  text and `\lt` `\gt` `\le` `\ge` in MathJax. (A raw `0<t<T` once swallowed half a question.)
- Keep every marker comment (`<!-- … -->`) and every block you were not asked to edit.

## What to edit, per page type

### A. Part 2 practice — `src/p2build/prac_N.html` (MathJax page)
- Edit ONLY the `<ol class="steps">…</ol>` inside `<div class="sol sol-zh">` of your questions
  (and the `<p class="idea">` line above it if it needs updating).
- Do NOT touch: `.orig` question text, INTENT block, `.ans` (unless wrong), `.official`, `.note`,
  `<details class="deep">` / XPL / PKP blocks, `<div class="sol sol-en">` blocks (those are
  generated from sol_en.py by add_en.py and would be overwritten).
- p1q1 has `<!-- ZH:resid -->…<!-- /ZH:resid -->` inside a step: leave that region exactly as is
  (add_zh.py regenerates it).
- Math: inline `\( \)`, display `\[ \]`. Split long display formulas with
  `\begin{aligned} … \\ … \end{aligned}` so each line fits a 360-px phone screen (about 40
  characters of formula per line). `<div class="calc">` and `<div class="tw"><table class="mini">`
  are fine.
- English: write the matching English steps (same steps, same formulas, plain English) to your
  own file `src/steps/en_<group>.py`:
  ```python
  STEPS = {
   'p1q1': [r'''<b>…</b>: …''', r'''…'''],
   ...
  }
  IDEA = {}   # only if you changed the idea line: {'p1q1': r'''…'''}
  ```
  Do NOT edit sol_en.py (the main session merges your file). If p1q1's English residual table is
  part of a step in sol_en.py, keep it in your English version of that step.

### B. Past exams — `src/exams/data_XXXX.py` (no MathJax on these pages)
- Edit only the `sol=` expression of each `dict(...)`: keep the `S(n, '…')` step structure
  (renumber as needed) and the final `<div class="wans">…</div>` (change only if wrong).
- Math is plain HTML/Unicode: `<sub>`, `<sup>`, ×, √, ≈, `<div class="calc">`. No `\( \)`.
- Do not edit `en=`, `note=`, `topic=`, figures, or other files (kp_exams.py etc.).
- Check the module still imports: `/usr/bin/python3 -c "import runpy; runpy.run_path('src/exams/data_XXXX.py')"`.

### C. Part A examples — `examples.html` (repo root; no MathJax)
- Edit only the `<ol class="steps">…</ol>` inside each `<div class="sol">`. Keep `.ans`, `.mem`,
  `.trap`, the XPL `<details>` box and everything else untouched.
- Same Unicode/HTML math style as the existing steps (`<span class="calc">`, sub/sup).

## Rules
- Chinese: short, plain sentences; give the English term in parentheses the first time
  (e.g. 中断概率（outage probability））. The student writes the exam in English, so keep symbols
  and units exam-ready.
- Do not run build scripts (build_practice.py, build_exams.py, build_hub.py, add_*.py,
  build_artifacts.py) — the main session builds once all groups finish.
- Do not delete any file. Do not git commit or push.
- Final report (short): per question, steps before → after; every error you found and fixed (with
  the numbers); anything you are unsure about.
