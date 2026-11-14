# Brief: translate EE6129 practice pages into English

Course: NTU EE6129 Wireless & Mobile Radio Systems (MSc). The pages are a student's exam-revision site:
past final exams with worked solutions, Part 2 practice sheets (wireless channel, detection, diversity, MIMO,
equalisation, OFDM), Part A cellular examples (Erlang B/C, reuse, SIR, sectoring), HW1, Part B/C quizzes
(WLAN, ad hoc, sensor networks, LTE, IoT, satellite) and a homework page. The student writes the exam in English,
so the English must read like a good model answer / clear study note — natural, precise, concise.

## Input
`batches/in_N.json`: a list of {id, page, kind, zh}. `zh` is a unit of the page that contains Chinese:
- kind "html": an HTML fragment (text with inline tags such as <b>, <sub>, <a href>, <span class>, MathJax TeX
  inside \( \) or \[ \]). Translate the human text, keep the markup.
- kind "attr": a plain attribute value (title / aria-label …).
- kind "js": a string from a script (button labels, quiz question/option/explanation text). It may contain HTML.

## Output
Write `batches/out_N.json`: one JSON object {"<id>": "<english>", …} with EVERY id of the input, UTF-8,
valid JSON (check it with `/usr/bin/python3 -c "import json;json.load(open('…'))"`; use /usr/bin/python3, not conda).

## Rules
1. Keep every HTML tag, attribute, class name, id, href, entity (&amp; &lt; …), HTML comment and TeX command exactly.
   Only translate the human-readable text. Inside TeX translate only \text{…} content that is Chinese.
   You may move an inline tag with the words it wraps when English word order needs it, but never drop or add tags.
2. Keep all numbers, units, symbols, equation results, question ids (P1 · Q1, Q2(a), p.44 …) unchanged.
   Do not "fix" maths; translate faithfully. If something looks wrong, still translate it and list it in your final report.
3. Parts already in English stay as they are. The output must contain no Chinese characters at all,
   except: keep the literal word 中文 only where it labels a Chinese-language option.
4. Chinese punctuation → English punctuation (，→ ,  ：→ :  （）→ ()  “”→ "" 、→ , ；→ ; 。→ .). Keep ① ② ③ … and → ⇒ ≈ etc.
5. Style: plain, exam-oriented English; short sentences; "you" for advice to the reader. No filler.
   Headings stay short. Button labels stay short (e.g. 显示解答 → "Show solution", 自测模式 → "Self-test mode").
6. Fixed terms (use these consistently):
   讲义 = lecture notes (讲义 p.12 = notes p.12; 讲义第 2 章 = Ch. 2 of the notes) · 讲解页 = learning page ·
   老师 / 老师课上强调 = the lecturer / Lecturer's emphasis in class · 本题知识点 = Key points ·
   考什么 / 前置知识 / 解题套路 / 关键公式 / 易错 / 自检 / 举一反三 = What it tests / Background / Method / Key formulas /
   Common mistakes / Self-check / Variations · 题意讲解 = What the question is asking ·
   场景 / 符号 / 要求 / 注意 / 目的 / 一句话 = Scenario / Symbols / What each part asks / Watch out / Purpose / In one line ·
   思路 = Approach · 官方答案 = Official answer · 课外补充 / 补充 = Beyond the notes ·
   背 = memorise · 考试给 = given in the exam · 尽量记 = try to memorise · 真题 = past exam (question) ·
   模拟题 = mock question · 自测模式 = Self-test mode · 已掌握 = mastered · 随机练习 = Random drill ·
   中断概率 = outage probability · 阴影 = shadowing · 衰落余量 = fade margin · 路径损耗 = path loss ·
   时延扩展 = delay spread · 相干带宽/时间 = coherence bandwidth/time · 电平通过率 = level crossing rate (LCR) ·
   平均衰落时长 = average fade duration (AFD) · 分集 = diversity · 最大比合并 = MRC · 等增益合并 = EGC ·
   选择合并 = selection combining · 阵列增益 = array gain · 注水 = water-filling · 迫零 = zero-forcing (ZF) ·
   判决门限 = decision threshold · 误码平台 = error floor · 码间干扰 = ISI · 循环前缀 = cyclic prefix ·
   子载波 = subcarrier · 话务量 = traffic (Erlang) · 呼损率/阻塞概率 = blocking probability (GoS) ·
   簇 = cluster · 频率复用 = frequency reuse · 同频干扰 = co-channel interference · 扇区化 = sectoring ·
   小区分裂 = cell splitting · 中继效率 = trunking efficiency · 信道 = channel · 多址 = multiple access ·
   自组网 = ad hoc network · 传感器网络 = sensor network · 卫星 = satellite · 星座 = constellation (orbit context).
7. Course parts: Part A (cellular), Part B (wireless systems), Part C (satellite), Part 2 (Ch. 1–7). Keep these names.

If a unit is ambiguous, look at the page it came from for context:
/run/media/paddy/新加卷/NTUlearn/EE6129_artifacts/<page>.html
(homework-sw is /run/media/paddy/新加卷/NTUlearn/EE6129_HW_SW/homework_sw.html).

Final report (short): number of ids written, the JSON check result, and any possible errors you noticed in the source.

## Addendum for the learning pages (batches/learn/in_N.json → batches/learn/out_N.json)
Pages: learn-guide (exam guide of the learning hub), p2-learn (Part 2 Ch. 1–7 notes), quiz-summary (Ch. 1b–2 problem
types), partA / partB / partC (Part 1 notes). Context files: /run/media/paddy/新加卷/NTUlearn/EE6129_artifacts/<page>.html
(learn-guide: src/hub/build_hub.py GUIDE_LEARN).
- kind "js" units here are mostly from the animated figures (src/anim/*.js): figure titles, captions (cap), step
  texts, slider labels, button labels and **SVG labels drawn inside the figure**. Short SVG labels must stay short
  (similar width to the Chinese; abbreviate: "Tx", "Rx", "BS", "MS", "SNR", "freq.", "dist."). Keep `_{…}` / `^{…}`
  sub/superscript markup, `\n`, and any leading/trailing spaces or punctuation that joins pieces of a concatenated string.
- Animation UI: ▶ 动画示意 = ▶ Animation · ▶ 播放 = ▶ Play · ⏸ 暂停 = ⏸ Pause · ▶ 自动播放 = ▶ Auto-play ·
  下一步 = Next · 上一步 = Back · 重来/重置 = Reset · 期末考点 = Final-exam topic · 考过 N 年 = tested in N years.
- More fixed terms: 课外补充 = Beyond the notes · 例题 = worked example · 推导 = derivation · 本节小结 = Section summary ·
  必背 = must memorise · 易错 = common mistake · 重点 = key point · 讲义第 N 页 / p.N = notes p.N · 课件 = slides ·
  题型 = problem type · 步骤 = step · 做法 = method · 模拟题 = mock question · 真题 = past exam.
