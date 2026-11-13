# EE6129 animated figures

Every numbered section of the four learning pages (p2-learn, partA, partB, partC) gets an animated SVG figure
beside it (right column on screens ≥ 1320 px, directly under the heading on narrower screens).

* `core.js` – runtime + drawing API (do not edit without the owner's OK)
* `anim.css` – figure card, colour classes, layout
* `<page>_<group>.js` – the animations, `page` = `p2 | A | B | C`
* `inject_anim.py` – wraps the sections and inlines css+core+page js into the built pages (run last; called from inject_teacher.py)
* `harness.html?f=<file>` – test bench with automatic self-test (served by the `ee6129-study` preview on port 8129)
* `sec_text.py <page> <sec…>` – prints a section's text so you can see what the figure must explain
* `_example.js` – two short reference animations (loop + steps)

## Registering an animation

```js
ANIM.reg('p2:6.3', {            // id = page:section number, exactly as in <span class="zh-num">; 2nd figure: 'p2:6.3/2'
  title: '迫零均衡：把信道"除掉"',   // short Chinese title (≤ 22 chars)
  cap: '看什么：……',                 // 1–2 sentences, HTML allowed, NO TeX (use Unicode: γ̄ σ² τ₀ ≤ → ×)
  h: 240,                         // viewBox height; width is always 400; keep 160–300
  steps: ['…', '…'],              // optional → "steps" mode with ◀ 上一步 / 下一步 ▶ / 自动播放
  stepDur: 3.4,                   // optional, seconds per step when auto-playing
  tween: 1.6,                     // optional, seconds frame() keeps being called after a step change
  live: false,                    // optional, steps mode: keep calling frame() forever (e.g. a moving wave)
  autoplay: true,                 // optional, loop mode starts playing (default true, except reduced motion)
  speed: 1,                       // optional, loop-mode time scale
  seed: 12345,                    // optional, seed for A.rand
  init: function (A) {
    // build the static drawing once here, keep references to the elements you will move
    return function frame(t, dt) { … };          // loop mode (t = seconds while playing)
    // or: return { step: function (k) {…}, frame: function (ts, dt, k) {…} };   // steps mode
    // or: return {};                             // static/interactive: redraw yourself in slider callbacks
  }
});
```

Modes: **loop** = continuous phenomenon (fading, orbits, waves); **steps** = a process or calculation
(CSMA/CA, handoff, long division, Alamouti, Erlang lookup) – the step texts are the explanation, write them like a tutor;
**static + sliders** = a relation between parameters (SIR vs N, path-loss exponent). Sliders can be added to loop and steps
mode too. After a slider change call `A.redraw()` (it re-runs frame with the current time/step).

## API (`A`)

| call | does |
|---|---|
| `A.W`, `A.H`, `A.svg` | 400, h, the root `<svg>` |
| `A.g(attrs?, parent?)` | `<g>` |
| `A.line(x1,y1,x2,y2,cls,parent)` · `A.rect(x,y,w,h,cls,parent,rx)` · `A.circle(cx,cy,r,cls,parent)` · `A.path(d,cls,parent)` · `A.poly([[x,y],…],cls,parent)` | shapes (poly closes when cls has a fill class) |
| `A.text(x,y,str,{cls,anchor:'middle'|'end',size},parent)` | text; `str` may contain `x_{sub}` and `x^{sup}` |
| `A.arrow(x1,y1,x2,y2,cls,parent,head)` · `A.moveArrow(g,x1,y1,x2,y2)` | arrow (line + filled head, colour from `s-*` class) |
| `A.el(tag, attrs, parent)` · `A.set(el, attrs)` · `A.setText(el, str)` | raw element / update attributes (`cls` → class, `text` → content) |
| `A.axes({x,y,w,h,xr:[a,b],yr:[a,b],xl,yl,ticksX:[v or {v,l}],ticksY,grid,xAxisAt:'bottom',yAxisAt:'left'})` | returns `ax` with `ax.X(v)`, `ax.Y(v)`, `ax.g` |
| `A.curve(ax, fn or [[x,y],…], cls, parent, n)` · `A.setCurve(path, ax, src, n)` | data curve in axis units (`null` = gap) |
| `A.slider({label,min,max,step,value,unit,fmt,on})` | → `{get,set}` |
| `A.choice({label,options:[html…],value,on})` | segmented buttons → `{get,set}` |
| `A.button(label, fn)` | extra button in the control row |
| `A.note(html)` | live read-out line under the figure (mono font); `A.note('')` hides it |
| `A.prog(ts, dur, delay)` | eased 0→1 progress inside a step |
| `A.lerp, A.clamp, A.ease, A.Q, A.erfc, A.fmt(x,digits), A.db, A.undb` | helpers |
| `A.rand()` · `A.rand.gauss()` · `A.rng(seed)` | seeded random (repeatable pictures) |
| `A.reduce` | true if the reader asked for reduced motion |

## Colour and text classes (never hard-code colours – the pages have a dark mode)

* stroke: `s-ink s-soft s-faint s-line s-acc s-gold s-good s-bad s-pur s-card s-none`
* fill: `f-ink f-soft f-faint f-line f-acc f-gold f-good f-bad f-pur` and soft fills `f-accs f-golds f-goods f-bads f-purs f-card f-paper f-none`
* stroke width `w1 w2 w3 w4`, `dash`, `dot`, opacity `op3 op5 op7`
* text: default 12 px ink; `t-s` 10.5 px soft, `t-xs` 9.5 px, `t-l` 14 px, `t-b` bold, `t-m` mono; colour text with `f-*`
* Meaning: accent blue = the signal / the thing being explained; gold = second item / highlight; good green = success / wanted;
  bad red = error, interference, collision, deep fade; purple = optional extra.

## Quality bar

1. **Explain the section's mechanism**, not decoration. Read the section first (`sec_text.py`). Use the section's own
   example numbers where it has them (e.g. H(z) = 1 + 0.3z⁻¹ + 0.1z⁻²; Singa/Mobi/Hubba Erlang example) so the figure and the text agree.
2. **Every number shown must be right.** Compute from formulas in code rather than typing results; check against the
   section's worked example. If a value comes from a table (Erlang B), use the values printed on the page.
3. Chinese labels, short; keep the English exam terms (DIFS, CW, RTS/CTS, MRC, ZF, CP, SIR, GoS…).
4. Readable: SVG text ≥ 10.5 units, nothing overlapping, everything inside 0…400 × 0…h, works at 343 px wide.
5. Light and dark mode both readable (only use the classes above).
6. Cheap per frame: create elements once, move them in frame(); no more than ~300 nodes; no setInterval/timers.
7. Plain ES2017 JavaScript, no libraries, no `</script` anywhere, no global variables (wrap helpers in an IIFE or inside init).
8. Aim for ≤ 150 lines per animation.

## Testing (required)

Open `http://localhost:8129/src/anim/harness.html?f=<your file without .js>` (several files: `f=a,b`; one figure: `&only=p2:6.3`).
The grey report at the top must say 全部通过 (no runtime error, no NaN in the SVG). Then look at every figure:
play it, click through every step, move every slider, switch to dark mode and to 343 px width.
