/* EE6129 animation core — shared by every animated figure on the learning pages.
   Each figure:  <figure class="anim" data-anim="p2:6.3"></figure>
   Each animation file calls ANIM.reg(id, def). See README.md for the API. */
(function () {
  'use strict';
  if (window.ANIM && window.ANIM.__core) return;
  var NS = 'http://www.w3.org/2000/svg';
  var REG = {};
  var ORDER = [];
  var reduce = false;
  try { reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  function reg(id, def) { if (!REG[id]) ORDER.push(id); REG[id] = def; }

  /* ---------- small maths helpers ---------- */
  function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function ease(t) { t = clamp(t, 0, 1); return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
  function erfc(x) {
    var z = Math.abs(x), t = 1 / (1 + 0.5 * z);
    var r = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))));
    return x >= 0 ? r : 2 - r;
  }
  function Q(x) { return 0.5 * erfc(x / Math.SQRT2); }
  function rng(seed) {
    var a = (seed >>> 0) || 1;
    var f = function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
    f.gauss = function () { var u = 0, v = 0; while (u === 0) u = f(); v = f(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
    return f;
  }
  function fmt(x, d) {
    if (x == null || !isFinite(x)) return '—';
    d = d == null ? 3 : d;
    var a = Math.abs(x);
    if (a !== 0 && (a < 1e-3 || a >= 1e6)) return x.toExponential(Math.max(0, d - 1)).replace('e', '×10^').replace('^+', '^');
    return (+x.toPrecision(d)).toString();
  }
  function db(x) { return 10 * Math.log10(x); }
  function undb(x) { return Math.pow(10, x / 10); }

  /* ---------- SVG helpers ---------- */
  function setText(e, str) {
    while (e.firstChild) e.removeChild(e.firstChild);
    str = String(str);
    var re = /([_^])\{([^}]*)\}/g, last = 0, m, shift = 0;
    function plain(s) { if (!s) return; var t = document.createElementNS(NS, 'tspan'); t.textContent = s; if (shift) { t.setAttribute('dy', -shift); shift = 0; } e.appendChild(t); }
    while ((m = re.exec(str))) {
      plain(str.slice(last, m.index));
      var t = document.createElementNS(NS, 'tspan');
      var dy = m[1] === '_' ? 3.5 : -5;
      t.setAttribute('dy', dy - shift); shift = dy;
      t.setAttribute('font-size', '72%');
      t.textContent = m[2];
      e.appendChild(t);
      last = re.lastIndex;
    }
    if (last < str.length) plain(str.slice(last));
    else if (shift) { var z = document.createElementNS(NS, 'tspan'); z.setAttribute('dy', -shift); z.textContent = '​'; e.appendChild(z); }
  }
  function set(e, attrs) {
    if (!attrs) return e;
    for (var k in attrs) {
      if (!Object.prototype.hasOwnProperty.call(attrs, k)) continue;
      var v = attrs[k];
      if (v == null) continue;
      if (k === 'text') setText(e, v);
      else if (k === 'cls') e.setAttribute('class', v);
      else if (k === 'anchor') e.setAttribute('text-anchor', v);
      else e.setAttribute(k, typeof v === 'number' ? +v.toFixed(2) : v);
    }
    return e;
  }
  function mk(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    set(e, attrs);
    if (parent) parent.appendChild(e);
    return e;
  }
  function n2(v) { return +(+v).toFixed(2); }
  function ptsToPath(pts) {
    var d = '';
    for (var i = 0; i < pts.length; i++) {
      var p = pts[i];
      if (p == null || !isFinite(p[0]) || !isFinite(p[1])) continue;
      d += (d && pts[i - 1] != null ? 'L' : 'M') + n2(p[0]) + ' ' + n2(p[1]);
    }
    return d;
  }

  /* ---------- figure runtime ---------- */
  var figs = [];
  function makeApi(fig, def) {
    var W = def.w || 400, H = def.h || 240;
    var A = { fig: fig, W: W, H: H, reduce: reduce, def: def };
    var head = document.createElement('div'); head.className = 'an-head';
    head.innerHTML = '<span class="an-k">▶ 动画示意</span><span class="an-t"></span>';
    head.querySelector('.an-t').textContent = def.title || '';
    fig.appendChild(head);
    var svg = mk('svg', { viewBox: '0 0 ' + W + ' ' + H, 'class': 'an-svg', role: 'img', 'aria-label': def.alt || def.title || '' }, fig);
    A.svg = svg;
    A.steptext = null;
    if (def.steps) { A.steptext = document.createElement('div'); A.steptext.className = 'an-steptext'; A.steptext.setAttribute('aria-live', 'polite'); fig.appendChild(A.steptext); }
    var ctrl = document.createElement('div'); ctrl.className = 'an-ctrl'; fig.appendChild(ctrl);
    var params = document.createElement('div'); params.className = 'an-params'; fig.appendChild(params);
    var read = document.createElement('div'); read.className = 'an-read'; read.hidden = true; fig.appendChild(read);
    if (def.cap) { var cap = document.createElement('figcaption'); cap.className = 'an-cap'; cap.innerHTML = def.cap; fig.appendChild(cap); }
    A._ctrl = ctrl; A._params = params; A._read = read;

    A.el = function (tag, attrs, parent) { return mk(tag, attrs, parent || svg); };
    A.set = set;
    A.g = function (attrs, parent) { return mk('g', attrs, parent || svg); };
    A.line = function (x1, y1, x2, y2, cls, parent) { return mk('line', { x1: x1, y1: y1, x2: x2, y2: y2, cls: cls || 's-ink' }, parent || svg); };
    A.rect = function (x, y, w, h, cls, parent, rx) { return mk('rect', { x: x, y: y, width: Math.max(0, w), height: Math.max(0, h), rx: rx == null ? 3 : rx, cls: cls || 'f-accs s-acc' }, parent || svg); };
    A.circle = function (cx, cy, r, cls, parent) { return mk('circle', { cx: cx, cy: cy, r: r, cls: cls || 'f-acc' }, parent || svg); };
    A.path = function (d, cls, parent) { return mk('path', { d: d, cls: cls || 's-ink' }, parent || svg); };
    A.poly = function (pts, cls, parent) { return mk('path', { d: ptsToPath(pts) + (cls && /f-/.test(cls) ? 'Z' : ''), cls: cls || 's-ink' }, parent || svg); };
    A.pts = ptsToPath;
    A.text = function (x, y, str, opt, parent) {
      opt = typeof opt === 'string' ? { cls: opt } : (opt || {});
      var a = { x: x, y: y, cls: opt.cls || '', text: str };
      if (opt.anchor) a['text-anchor'] = opt.anchor;
      if (opt.size) a.style = 'font-size:' + opt.size + (typeof opt.size === 'number' ? 'px' : '');
      if (opt.weight) a['font-weight'] = opt.weight;
      return mk('text', a, parent || svg);
    };
    A.setText = setText;
    A.arrow = function (x1, y1, x2, y2, cls, parent, head) {
      var g = mk('g', { cls: 'an-arrow ' + (cls || 's-ink') }, parent || svg);
      g._l = mk('line', {}, g); g._h = mk('path', {}, g); g._s = head || 7;
      A.moveArrow(g, x1, y1, x2, y2);
      return g;
    };
    A.moveArrow = function (g, x1, y1, x2, y2) {
      var dx = x2 - x1, dy = y2 - y1, L = Math.sqrt(dx * dx + dy * dy) || 1, ux = dx / L, uy = dy / L, s = Math.min(g._s, L * 0.6);
      var bx = x2 - ux * s, by = y2 - uy * s;
      set(g._l, { x1: x1, y1: y1, x2: bx + ux * 0.5, y2: by + uy * 0.5 });
      set(g._h, { d: 'M' + n2(x2) + ' ' + n2(y2) + 'L' + n2(bx - uy * s * 0.5) + ' ' + n2(by + ux * s * 0.5) + 'L' + n2(bx + uy * s * 0.5) + ' ' + n2(by - ux * s * 0.5) + 'Z' });
      g.style.display = L < 1.5 ? 'none' : '';
    };
    /* axes: {x,y,w,h, xr:[a,b], yr:[a,b], xl, yl, ticksX:[..], ticksY:[..], grid:false} */
    A.axes = function (o) {
      var g = mk('g', { cls: 'an-axes' }, o.parent || svg);
      var ax = { x: o.x, y: o.y, w: o.w, h: o.h, xr: o.xr, yr: o.yr, g: g };
      ax.X = function (v) { return o.x + (v - o.xr[0]) / (o.xr[1] - o.xr[0]) * o.w; };
      ax.Y = function (v) { return o.y + o.h - (v - o.yr[0]) / (o.yr[1] - o.yr[0]) * o.h; };
      var y0 = o.yr[0] <= 0 && o.yr[1] >= 0 ? ax.Y(0) : o.y + o.h;
      var x0 = o.xr[0] <= 0 && o.xr[1] >= 0 ? ax.X(0) : o.x;
      if (o.xAxisAt === 'bottom') y0 = o.y + o.h;
      if (o.yAxisAt === 'left') x0 = o.x;
      A.arrow(o.x - 2, y0, o.x + o.w + 8, y0, 's-soft w1', g, 5);
      A.arrow(x0, o.y + o.h + 2, x0, o.y - 8, 's-soft w1', g, 5);
      if (o.xl) A.text(o.x + o.w + 8, y0 + 14, o.xl, { cls: 't-s', anchor: 'end' }, g);
      if (o.yl) A.text(x0 + 5, o.y - 2, o.yl, { cls: 't-s' }, g);
      (o.ticksX || []).forEach(function (t) {
        var v = t.v != null ? t.v : t, lb = t.l != null ? t.l : String(t);
        A.line(ax.X(v), y0 - 2.5, ax.X(v), y0 + 2.5, 's-soft w1', g);
        if (lb) A.text(ax.X(v), y0 + 13, lb, { cls: 't-s', anchor: 'middle' }, g);
        if (o.grid) A.line(ax.X(v), o.y, ax.X(v), o.y + o.h, 's-line w1 dash op5', g);
      });
      (o.ticksY || []).forEach(function (t) {
        var v = t.v != null ? t.v : t, lb = t.l != null ? t.l : String(t);
        A.line(x0 - 2.5, ax.Y(v), x0 + 2.5, ax.Y(v), 's-soft w1', g);
        if (lb) A.text(x0 - 5, ax.Y(v) + 3.5, lb, { cls: 't-s', anchor: 'end' }, g);
        if (o.grid) A.line(o.x, ax.Y(v), o.x + o.w, ax.Y(v), 's-line w1 dash op5', g);
      });
      return ax;
    };
    /* curve on axes: fn(v) or array of [vx, vy] in data units */
    A.curve = function (ax, src, cls, parent, n) {
      var p = mk('path', { cls: cls || 's-acc w2' }, parent || svg);
      A.setCurve(p, ax, src, n);
      return p;
    };
    A.setCurve = function (p, ax, src, n) {
      var pts = [];
      if (typeof src === 'function') {
        n = n || 160;
        for (var i = 0; i <= n; i++) {
          var v = ax.xr[0] + (ax.xr[1] - ax.xr[0]) * i / n, y = src(v);
          pts.push(y == null || !isFinite(y) ? null : [ax.X(v), ax.Y(y)]);
        }
      } else pts = src.map(function (q) { return q == null ? null : [ax.X(q[0]), ax.Y(q[1])]; });
      p.setAttribute('d', ptsToPath(pts));
      return p;
    };

    /* ---------- controls ---------- */
    A.slider = function (o) {
      var row = document.createElement('label'); row.className = 'an-param';
      var lb = document.createElement('span'); lb.className = 'an-pl'; lb.innerHTML = o.label || '';
      var inp = document.createElement('input'); inp.type = 'range';
      inp.min = o.min; inp.max = o.max; inp.step = o.step || (o.max - o.min) / 100; inp.value = o.value;
      var out = document.createElement('output');
      row.appendChild(lb); row.appendChild(inp); row.appendChild(out);
      params.appendChild(row);
      var f = o.fmt || function (v) { return fmt(v, 3) + (o.unit ? ' ' + o.unit : ''); };
      var api = {
        get: function () { return +inp.value; },
        set: function (v) { inp.value = v; out.textContent = f(+inp.value); if (o.on) o.on(+inp.value); },
        input: inp
      };
      inp.addEventListener('input', function () { out.textContent = f(+inp.value); if (o.on) o.on(+inp.value); });
      out.textContent = f(+inp.value);
      return api;
    };
    A.choice = function (o) {
      var row = document.createElement('div'); row.className = 'an-choice';
      if (o.label) { var lb = document.createElement('span'); lb.className = 'an-pl'; lb.innerHTML = o.label; row.appendChild(lb); }
      var cur = o.value != null ? o.value : 0, btns = [];
      o.options.forEach(function (t, i) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'an-btn'; b.innerHTML = t;
        b.addEventListener('click', function () { api.set(i); });
        row.appendChild(b); btns.push(b);
      });
      params.appendChild(row);
      var api = {
        get: function () { return cur; },
        set: function (i, silent) { cur = i; btns.forEach(function (b, j) { b.setAttribute('aria-pressed', j === i ? 'true' : 'false'); }); if (o.on && !silent) o.on(i); }
      };
      api.set(cur, true);
      return api;
    };
    A.button = function (label, fn) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'an-btn'; b.innerHTML = label;
      b.addEventListener('click', fn); ctrl.appendChild(b); return b;
    };
    A.redraw = function () {};
    A.note = function (html) { read.hidden = !html; read.innerHTML = html || ''; };

    A.clamp = clamp; A.lerp = lerp; A.ease = ease; A.Q = Q; A.erfc = erfc; A.fmt = fmt; A.db = db; A.undb = undb;
    A.rng = rng; A.rand = rng(def.seed || 12345);
    /* tween helper for steps mode: progress 0..1 of the current step's first `dur` seconds */
    A.prog = function (ts, dur, delay) { return ease(((ts || 0) - (delay || 0)) / (dur || 0.8)); };
    return A;
  }

  function build(f) {
    var def = REG[f.id];
    var fig = f.el;
    fig.innerHTML = '';
    var A = makeApi(fig, def);
    f.A = A;
    var r;
    try { r = def.init(A); } catch (e) { fail(f, e); return; }
    if (typeof r === 'function') r = { frame: r };
    f.r = r || {};
    A.redraw = function () { safe(f, function () { if (!f.r.frame) return; if (f.mode === 'steps') f.r.frame(reduce ? 99 : f.ts, 0, f.k); else f.r.frame(f.t, 0); }); };
    f.mode = def.steps ? 'steps' : (f.r.frame ? 'loop' : 'static');
    f.t = 0; f.k = 0; f.ts = 0; f.idle = false;
    f.playing = f.mode === 'loop' ? !reduce && def.autoplay !== false : (f.mode === 'steps' ? false : false);
    if (f.mode === 'loop') {
      f.bPlay = A.button('', function () { f.playing = !f.playing; ui(f); kick(); });
      A.button('↺ 重来', function () { f.t = 0; if (f.r.reset) f.r.reset(); safe(f, function () { f.r.frame(0, 0); }); kick(); });
    } else if (f.mode === 'steps') {
      f.bPrev = A.button('◀ 上一步', function () { go(f, f.k - 1); f.playing = false; ui(f); });
      f.ind = document.createElement('span'); f.ind.className = 'an-ind'; A._ctrl.appendChild(f.ind);
      f.bNext = A.button('下一步 ▶', function () { go(f, f.k + 1); f.playing = false; ui(f); });
      f.bPlay = A.button('', function () { f.playing = !f.playing; if (f.playing && f.k >= def.steps.length - 1) go(f, 0); f.auto = 0; ui(f); kick(); });
    }
    if (!A._ctrl.children.length) A._ctrl.hidden = true;
    if (f.mode === 'steps') go(f, 0);
    else if (f.mode === 'loop') safe(f, function () { f.r.frame(0, 0); });
    ui(f);
  }
  function go(f, k) {
    var n = f.A.def.steps.length;
    k = clamp(k, 0, n - 1);
    f.k = k; f.ts = 0; f.auto = 0; f.idle = false; f.settled = false;
    f.A.steptext.innerHTML = '<b>' + (k + 1) + ' / ' + n + '</b>　' + f.A.def.steps[k];
    safe(f, function () { if (f.r.step) f.r.step(k); if (f.r.frame) f.r.frame(reduce ? 99 : 0, 0, k); });
    ui(f); kick();
  }
  function ui(f) {
    if (f.bPlay) { f.bPlay.textContent = f.playing ? '⏸ 暂停' : (f.mode === 'steps' ? '▶ 自动播放' : '▶ 播放'); f.bPlay.setAttribute('aria-pressed', f.playing ? 'true' : 'false'); }
    if (f.mode === 'steps') {
      var n = f.A.def.steps.length;
      f.ind.textContent = (f.k + 1) + ' / ' + n;
      f.bPrev.disabled = f.k === 0; f.bNext.disabled = f.k === n - 1;
    }
  }
  function fail(f, e) {
    f.dead = true;
    if (window.console) console.error('[anim ' + f.id + ']', e);
    var d = document.createElement('div'); d.className = 'an-err'; d.textContent = '这个动画加载失败（' + (e && e.message || e) + '），不影响正文。';
    f.el.appendChild(d);
  }
  function safe(f, fn) { if (f.dead) return; try { fn(); } catch (e) { fail(f, e); } }

  var last = 0, running = false;
  function kick() { if (!running) { running = true; last = 0; requestAnimationFrame(tick); } }
  function tick(now) {
    var dt = last ? Math.min(0.05, (now - last) / 1000) : 0; last = now;
    var any = false;
    for (var i = 0; i < figs.length; i++) {
      var f = figs[i];
      if (!f.r || f.dead || !f.vis) continue;
      if (f.mode === 'loop' && f.playing) {
        f.t += dt * (f.A.def.speed || 1);
        safe(f, function () { f.r.frame(f.t, dt); });
        any = true;
      } else if (f.mode === 'steps') {
        var d = f.A.def, tw = d.tween == null ? 1.6 : d.tween;
        if (f.ts <= tw + 0.05 || (f.r.frame && d.live)) {
          f.ts += dt;
          if (f.r.frame) safe(f, function () { f.r.frame(reduce ? 99 : f.ts, dt, f.k); });
          any = true;
        } else if (!f.settled && f.r.frame) {
          // tween window over: draw the finished state once, so nothing stays half-faded
          f.settled = true;
          safe(f, function () { f.r.frame(99, 0, f.k); });
        }
        if (f.playing) {
          f.auto += dt; any = true;
          var dur = (d.stepDur || 3.4) * (f.k === d.steps.length - 1 ? 1.5 : 1);
          if (f.auto >= dur) {
            if (f.k < d.steps.length - 1) go(f, f.k + 1); else go(f, 0);
          }
        }
      }
    }
    if (any) requestAnimationFrame(tick); else running = false;
  }

  function boot() {
    var els = document.querySelectorAll('figure.anim[data-anim]');
    var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        var f = en.target.__anim;
        if (!f) return;
        if (en.isIntersecting && !f.r && !f.dead) build(f);
        f.vis = en.isIntersecting;
        if (f.vis) kick();
      });
    }, { rootMargin: '150px 0px' }) : null;
    Array.prototype.forEach.call(els, function (el) {
      if (el.__anim) return;
      var id = el.getAttribute('data-anim');
      if (!REG[id]) return;
      var f = { id: id, el: el, vis: !io };
      el.__anim = f; figs.push(f);
      if (io) io.observe(el); else build(f);
    });
    kick();
  }

  /* test hook: build everything now and drive frames deterministically (harness only) */
  function selftest(seconds) {
    var out = [];
    figs.forEach(function (f) {
      if (!f.r && !f.dead) build(f);
      var rec = { id: f.id, ok: !f.dead, mode: f.mode, err: null, nan: false, nodes: 0 };
      try {
        if (f.mode === 'loop') { for (var t = 0; t <= (seconds || 12); t += 0.05) f.r.frame(t, 0.05); }
        else if (f.mode === 'steps') { for (var k = 0; k < f.A.def.steps.length; k++) { go(f, k); for (var s = 0; s <= 3; s += 0.05) if (f.r.frame) f.r.frame(s, 0.05, k); } go(f, 0); }
      } catch (e) { rec.ok = false; rec.err = String(e && e.stack || e); }
      if (f.dead) rec.ok = false;
      var html = f.A ? f.A.svg.outerHTML : '';
      rec.nan = /NaN|undefined|Infinity/.test(html);
      rec.nodes = f.A ? f.A.svg.querySelectorAll('*').length : 0;
      out.push(rec);
    });
    return out;
  }

  window.ANIM = { __core: true, reg: reg, REG: REG, ORDER: ORDER, boot: boot, selftest: selftest, figs: figs,
    util: { clamp: clamp, lerp: lerp, ease: ease, Q: Q, erfc: erfc, fmt: fmt, rng: rng, db: db, undb: undb } };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(boot, 0); });
  else setTimeout(boot, 0);
})();
