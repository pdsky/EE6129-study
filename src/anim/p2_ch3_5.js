/* EE6129 Part 2 (Ser Wee) ch.3–5: signal space, detection, fading BER, diversity, MIMO. Page p2 = p2-learn.html */
(function () {
  'use strict';
  var TAU = 2 * Math.PI, DEG = Math.PI / 180;

  /* number for SVG text (x^{e}) or HTML (<sup>) */
  function sci(x, html) {
    if (x == null || !isFinite(x)) return '—';
    if (x === 0 || x >= 0.01) return String(+x.toPrecision(3));
    var e = Math.floor(Math.log10(x)), m = x / Math.pow(10, e);
    if (+m.toFixed(2) >= 10) { m /= 10; e += 1; }
    var es = String(e).replace('-', '−');
    return (+m.toFixed(2)) + '×10' + (html ? '<sup>' + es + '</sup>' : '^{' + es + '}');
  }
  function r2(x) { var v = Math.round(x * 100) / 100; return (v === 0 ? 0 : v).toFixed(2).replace('-', '−'); }
  function dB(x) { return 10 * Math.log10(Math.max(x, 1e-9)); }
  function logTicks(a, b) {
    var t = [];
    for (var e = a; e <= b; e++) t.push({ v: e, l: e === 0 ? '1' : '10^{' + String(e).replace('-', '−') + '}' });
    return t;
  }
  /* Rayleigh fading h(t) by sum of sinusoids, E|h|² = 1 */
  function rayGen(A, N, fd) {
    var ph = [], ang = [], i;
    for (i = 0; i < N; i++) { ph.push(A.rand() * TAU); ang.push(A.rand() * TAU); }
    var s = 1 / Math.sqrt(N);
    return function (t) {
      var re = 0, im = 0;
      for (var j = 0; j < N; j++) { var p = ph[j] + TAU * fd * Math.cos(ang[j]) * t; re += Math.cos(p); im += Math.sin(p); }
      return [re * s, im * s];
    };
  }
  /* complex helpers [re, im] */
  function cx(r, a) { return [r * Math.cos(a), r * Math.sin(a)]; }
  function cadd(a, b) { return [a[0] + b[0], a[1] + b[1]]; }
  function csub(a, b) { return [a[0] - b[0], a[1] - b[1]]; }
  function cmul(a, b) { return [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]]; }
  function conj(a) { return [a[0], -a[1]]; }
  function abs2(a) { return a[0] * a[0] + a[1] * a[1]; }
  function cstr(a) { var im = Math.round(a[1] * 100) / 100; return r2(a[0]) + (im < 0 ? '−' : '+') + Math.abs(im).toFixed(2) + 'j'; }
  function sm(el) { el.style.fontSize = '10.5px'; return el; } /* small coloured text (.t-s would override the f-* colour) */
  function show(el, on) { el.style.display = on ? '' : 'none'; }
  function op(el, v) { el.setAttribute('opacity', (+v).toFixed(2)); }

  /* ================= 3.1 signals as vectors ================= */
  ANIM.reg('p2:3.1', {
    title: '波形 → 坐标：星座图从哪来',
    cap: '左：第 i 个信号 s<sub>i</sub>(t)（黑）= s<sub>i1</sub>ψ₁(t)（蓝虚线）+ s<sub>i2</sub>ψ₂(t)（金虚线）。坐标 s<sub>ij</sub> 就是“乘 ψ<sub>j</sub> 再在 [0, T] 上积分”，这里真的做了数值积分。把坐标画到右边平面上就是星座点。换调制方式看维数：PAM 1 维，PSK、QAM 2 维。',
    h: 250,
    init: function (A) {
      var fc = 3, NS = 240, s2 = Math.SQRT2; /* T = 1, ψ1 = √(2/T)cos 2πfct, ψ2 = √(2/T)sin 2πfct */
      function p1(t) { return s2 * Math.cos(TAU * fc * t); }
      function p2(t) { return s2 * Math.sin(TAU * fc * t); }
      var mods = [
        { name: '4-PAM', D: 1, M: 4, wave: function (i) { var Ai = 2 * i - 1 - 4; return function (t) { return Ai * p1(t); }; } },
        { name: '8-PSK', D: 2, M: 8, wave: function (i) { var ph = TAU * (i - 1) / 8; return function (t) { return s2 * Math.cos(TAU * fc * t + ph); }; } },
        { name: '16-QAM', D: 2, M: 16, wave: function (i) { var a = 2 * ((i - 1) % 4) - 3, b = 3 - 2 * Math.floor((i - 1) / 4); return function (t) { return a * p1(t) + b * p2(t); }; } }
      ];
      function proj(f) { /* s_ij = ∫ s_i ψ_j dt (midpoint rule, exact for whole cycles) */
        var a = 0, b = 0, dt = 1 / NS;
        for (var n = 0; n < NS; n++) { var t = (n + 0.5) * dt, v = f(t); a += v * p1(t) * dt; b += v * p2(t) * dt; }
        return [Math.round(a * 1000) / 1000, Math.round(b * 1000) / 1000];
      }
      mods.forEach(function (m) {
        m.pts = []; m.R = 0;
        for (var i = 1; i <= m.M; i++) { var c = proj(m.wave(i)); m.pts.push(c); m.R = Math.max(m.R, Math.abs(c[0]), Math.abs(c[1])); }
      });
      var ax = A.axes({ x: 26, y: 28, w: 178, h: 116, xr: [0, 1], yr: [-1.15, 1.15], yl: 's_{i}(t)', ticksX: [{ v: 1, l: 'T' }] });
      var c1 = A.curve(ax, function () { return 0; }, 's-acc w1 dash');
      var c2 = A.curve(ax, function () { return 0; }, 's-gold w1 dash');
      var cs = A.curve(ax, function () { return 0; }, 's-ink w2');
      var t1 = A.text(10, 176, '', { cls: 'f-acc' }), t2 = A.text(10, 196, '', { cls: 'f-gold' });
      var t3 = A.text(10, 218, '', { cls: 't-b' });
      A.text(10, 238, 'ψ_{1}, ψ_{2} = √(2/T)·cos, sin(2πf_{c}t)', { cls: 't-s' });
      /* constellation */
      var X0 = 308, Y0 = 112, RP = 70;
      var ttl = A.text(X0, 18, '', { cls: 't-b', anchor: 'middle' });
      A.arrow(X0 - 84, Y0, X0 + 86, Y0, 's-soft w1', null, 5);
      A.arrow(X0, Y0 + 84, X0, Y0 - 86, 's-soft w1', null, 5);
      A.text(X0 + 88, Y0 - 6, 'ψ_{1}', { anchor: 'end', cls: 't-s' });
      A.text(X0 + 6, Y0 - 78, 'ψ_{2}', { cls: 't-s' });
      var pl1 = A.line(0, 0, 0, 0, 's-acc w1 dash'), pl2 = A.line(0, 0, 0, 0, 's-gold w1 dash');
      var dots = [];
      for (var i = 0; i < 16; i++) dots.push(A.circle(0, 0, 3.6, 'f-faint'));
      var cur = A.circle(0, 0, 6, 'f-acc s-card w2');
      var dimt = A.text(X0, 222, '', { cls: 't-s', anchor: 'middle' });
      var mi = 1, si = 2;
      function draw() {
        var m = mods[mi], k = RP / m.R, f = m.wave(si), c = m.pts[si - 1];
        var amp = m.R * s2 * (m.D === 2 && mi === 2 ? s2 : 1);
        A.setCurve(cs, ax, function (t) { return f(t) / amp; }, 200);
        A.setCurve(c1, ax, function (t) { return c[0] * p1(t) / amp; }, 200);
        A.setCurve(c2, ax, function (t) { return c[1] * p2(t) / amp; }, 200);
        A.setText(t1, 's_{i1} = ∫s_{i}(t)ψ_{1}(t)dt = ' + r2(c[0]));
        A.setText(t2, 's_{i2} = ∫s_{i}(t)ψ_{2}(t)dt = ' + r2(c[1]));
        A.setText(t3, 'i = ' + si + '：点 (' + r2(c[0]) + ', ' + r2(c[1]) + ')');
        A.setText(ttl, '星座图：' + m.name);
        A.setText(dimt, m.D === 1 ? 'D = 1：点排在一条线上（ψ₂ 坐标全是 0）' : 'D = 2：点铺在 ψ₁–ψ₂ 平面上');
        for (var j = 0; j < 16; j++) {
          show(dots[j], j < m.M);
          if (j < m.M) A.set(dots[j], { cx: X0 + m.pts[j][0] * k, cy: Y0 - m.pts[j][1] * k });
        }
        var px = X0 + c[0] * k, py = Y0 - c[1] * k;
        A.set(cur, { cx: px, cy: py });
        A.set(pl1, { x1: px, y1: py, x2: px, y2: Y0 });
        A.set(pl2, { x1: px, y1: py, x2: X0, y2: py });
      }
      var sl = A.slider({ label: '信号编号', min: 1, max: 8, step: 1, value: si, fmt: function (v) { return 'i = ' + v; }, on: function (v) { si = v; draw(); } });
      A.choice({ label: '调制', options: ['4-PAM', '8-PSK', '16-QAM'], value: mi, on: function (v) {
        mi = v; sl.input.max = mods[v].M; if (si > mods[v].M) si = mods[v].M; sl.set(si);
      } });
      draw();
      return {};
    }
  });

  /* ================= 3.2 AWGN vector channel ================= */
  ANIM.reg('p2:3.2', {
    title: 'AWGN：每个坐标各加一份高斯噪声',
    cap: '发的是 QPSK 四个点之一，收到 y = s<sub>i</sub> + w。每个点的噪声分成水平 w₁（蓝）和竖直 w₂（金）两份，各自独立、均值 0、方差 σ² = N₀/2。拖 σ：点云按比例变大，但形状始终是圆的（各方向一样大）。',
    h: 250,
    init: function (A) {
      var cx = 120, cy = 125, k = 44, sig = 0.4, P = 150;
      var S = [[1, 1], [-1, 1], [-1, -1], [1, -1]];
      A.arrow(cx - 112, cy, cx + 114, cy, 's-soft w1', null, 5);
      A.arrow(cx, cy + 112, cx, cy - 114, 's-soft w1', null, 5);
      A.text(cx + 112, cy + 14, 'y_{1}', { anchor: 'end', cls: 't-s' });
      A.text(cx + 6, cy - 104, 'y_{2}', { cls: 't-s' });
      var rings = S.map(function (s) { return A.circle(cx + s[0] * k, cy - s[1] * k, 1, 'f-none s-gold w1 dash'); });
      var gD = A.g(), dots = [], data = [];
      for (var i = 0; i < P; i++) { dots.push(A.circle(0, 0, 2.2, 'f-acc op5', gD)); data.push(null); }
      S.forEach(function (s) { A.circle(cx + s[0] * k, cy - s[1] * k, 4.5, 'f-ink'); });
      var a1 = A.arrow(0, 0, 0, 0, 's-acc w2', null, 5), a2 = A.arrow(0, 0, 0, 0, 's-gold w2', null, 5);
      var ring = A.circle(0, 0, 5, 'f-none s-ink w2');
      /* right panel */
      A.text(250, 26, 'y = s_{i} + w', { cls: 't-b' });
      A.text(250, 46, 'w_{1}, w_{2} 独立，各 ~ N(0, σ²)', { cls: 't-s' });
      var bx = 320, bk = 24, by = 132;
      A.line(254, by, 388, by, 's-soft w1');
      var bell = A.path('', 's-ink w2');
      var tkL = A.line(0, 0, 0, 0, 's-soft w1'), tkR = A.line(0, 0, 0, 0, 's-soft w1');
      var tsL = A.text(0, by + 13, '−σ', { cls: 't-s', anchor: 'middle' }), tsR = A.text(0, by + 13, '+σ', { cls: 't-s', anchor: 'middle' });
      var d1 = A.circle(0, by, 3.5, 'f-acc'), d2 = A.circle(0, by, 3.5, 'f-gold');
      A.text(bx, 72, '最新一点的 w₁、w₂', { cls: 't-s', anchor: 'middle' });
      var tS = A.text(250, 168, '', { cls: 't-m' }), tN = A.text(250, 188, '', { cls: 't-m' }), tW = A.text(250, 208, '', { cls: 't-m t-s' });
      A.text(250, 228, '金色虚线圈：半径 2σ', { cls: 't-s' });
      A.text(250, 244, '约 ' + Math.round(100 * (1 - Math.exp(-2))) + '% 的点落在圈内', { cls: 't-s' });
      var count = 0, lastT = 0;
      A.slider({ label: '噪声 σ', min: 0.1, max: 0.8, step: 0.05, value: sig, fmt: function (v) { return 'σ = ' + v.toFixed(2); }, on: function (v) { sig = v; A.redraw(); } });
      return function frame(t) {
        if (t < lastT - 1e-9) count = 0;
        lastT = t;
        var target = Math.floor(t * 22);
        while (count < target) { data[count % P] = [Math.floor(A.rand() * 4), A.rand.gauss(), A.rand.gauss()]; count++; }
        for (var j = 0; j < P; j++) {
          var on = j < Math.min(count, P), d = data[j], s, u, v;
          if (on) { s = S[d[0]]; u = s[0] + sig * d[1]; v = s[1] + sig * d[2]; on = Math.abs(u) < 2.5 && Math.abs(v) < 2.5; }
          show(dots[j], on);
          if (on) A.set(dots[j], { cx: cx + u * k, cy: cy - v * k });
        }
        rings.forEach(function (r) { A.set(r, { r: 2 * sig * k }); });
        var pts = [];
        for (var n = 0; n <= 60; n++) { var u = -2.6 + 5.2 * n / 60; pts.push([bx + u * sig * bk, by - 48 * Math.exp(-u * u / 2)]); }
        A.set(bell, { d: A.pts(pts) });
        A.set(tkL, { x1: bx - sig * bk, y1: by - 4, x2: bx - sig * bk, y2: by + 3 }); A.set(tkR, { x1: bx + sig * bk, y1: by - 4, x2: bx + sig * bk, y2: by + 3 });
        A.set(tsL, { x: bx - Math.max(sig * bk, 12) }); A.set(tsR, { x: bx + Math.max(sig * bk, 12) });
        A.setText(tS, 'σ = ' + sig.toFixed(2));
        A.setText(tN, 'N₀/2 = σ² = ' + (sig * sig).toFixed(3));
        var nw = count > 0 ? data[(count - 1) % P] : null;
        [a1, a2, ring, d1, d2].forEach(function (e) { show(e, !!nw); });
        if (nw) {
          var s0 = S[nw[0]], x0 = cx + s0[0] * k, y0 = cy - s0[1] * k, x1 = A.clamp(x0 + sig * nw[1] * k, 12, 228), y1 = A.clamp(y0 - sig * nw[2] * k, 14, 236);
          A.moveArrow(a1, x0, y0, x1, y0); A.moveArrow(a2, x1, y0, x1, y1);
          A.set(ring, { cx: x1, cy: y1 });
          A.set(d1, { cx: A.clamp(bx + sig * nw[1] * bk, 256, 386) }); A.set(d2, { cx: A.clamp(bx + sig * nw[2] * bk, 256, 386) });
          A.setText(tW, 'w = (' + r2(sig * nw[1]) + ', ' + r2(sig * nw[2]) + ')');
        } else A.setText(tW, '');
      };
    }
  });

  /* ================= 3.3 ML = minimum distance, Pe = Q(d/2σ) ================= */
  ANIM.reg('p2:3.3', {
    title: 'ML 检测：选最近的点，越过中垂线就错',
    cap: '左：QPSK 星座和判决区域（每个点管离它最近的一块）。右：只看沿 s₁→s₂ 方向的那一维，两个钟形曲线是 y | s₁、y | s₂，红色阴影就是“发 s₁ 却判成 s₂”的概率 Q(d/2σ)。拖 σ 看阴影怎么变。',
    h: 270,
    steps: [
      '发 s₁ = (+1, +1)，噪声把它推到 y = s₁ + w（金点）。接收端只看到 y。',
      'ML = 最小距离：量 y 到 4 个星座点的距离，最近的是 s₁（绿线）→ 判对。',
      '每个点“管”离它最近的一块：判决区域 Z<sub>i</sub>，边界是两点连线的中垂线。',
      '噪声再大一点，y 越过中垂线进了 Z₂：最近的变成 s₂ → 判错（红）。',
      '会不会错只看沿 s₁→s₂ 方向的噪声 n ~ N(0, σ²)：n 超过 d/2 就错。',
      'P(s₁→s₂) = Q(d/2σ)。d = 2、σ = 0.5 → Q(2) ≈ 0.023；σ 越小越难错。'
    ],
    tween: 1.2,
    init: function (A) {
      var cx = 100, cy = 138, k = 50, sig = 0.5;
      function P(p) { return [cx + p[0] * k, cy - p[1] * k]; }
      var S = [[1, 1], [-1, 1], [-1, -1], [1, -1]], nm = ['s₁', 's₂', 's₃', 's₄'];
      var Y0 = [0.62, 1.38], Y1 = [-0.28, 0.82];
      var gR = A.g({ opacity: 0 }), fills = ['f-goods', 'f-golds', 'f-accs', 'f-purs'], L = 92;
      [[cx, cy - L], [cx - L, cy - L], [cx - L, cy], [cx, cy]].forEach(function (o, i) {
        A.rect(o[0], o[1], L, L, fills[i] + ' s-none', gR, 0);
        A.text(o[0] + (i === 0 || i === 3 ? L - 4 : 4), o[1] + (i < 2 ? 14 : L - 5), 'Z_{' + (i + 1) + '}', { cls: 't-s', anchor: i === 0 || i === 3 ? 'end' : 'start' }, gR);
      });
      A.line(cx - L, cy, cx + L, cy, 's-soft w2 dash', gR); A.line(cx, cy - L, cx, cy + L, 's-soft w2 dash', gR);
      A.line(cx - L, cy, cx + L, cy, 's-line w1'); A.line(cx, cy - L, cx, cy + L, 's-line w1');
      A.text(cx, 22, '星座图（左右 = y₁，上下 = y₂）', { cls: 't-s', anchor: 'middle' });
      var dl = S.map(function () { return A.line(0, 0, 0, 0, 's-line w1'); });
      S.forEach(function (s, i) { var p = P(s); A.circle(p[0], p[1], 5, 'f-ink'); A.text(p[0] + (s[0] > 0 ? 8 : -8), p[1] + (s[1] > 0 ? -7 : 15), nm[i], { anchor: s[0] > 0 ? 'start' : 'end', cls: 't-b' }); });
      var na = A.arrow(0, 0, 0, 0, 's-soft w1', null, 5);
      var yp = A.circle(0, 0, 5.5, 'f-gold s-card w1');
      var ylab = A.text(0, 0, 'y', { cls: 't-b' });
      /* right: 1-D view along s1 -> s2 */
      var gP = A.g({ opacity: 0.15 });
      A.text(304, 22, '沿 s₂ ↔ s₁ 方向（y₁）', { cls: 't-s', anchor: 'middle' }, gP);
      var ax = A.axes({ x: 222, y: 52, w: 166, h: 112, xr: [-2.4, 2.4], yr: [0, 1.15], yAxisAt: 'left', ticksX: [{ v: -1, l: '−1' }, { v: 0, l: '0' }, { v: 1, l: '+1' }], parent: gP });
      var shade = A.path('', 'f-bad s-none', gP);
      var g2 = A.path('', 's-gold w2', gP), g1 = A.path('', 's-acc w2', gP);
      A.line(ax.X(0), ax.Y(1.12), ax.X(0), ax.Y(0), 's-soft w2 dash', gP);
      A.text(ax.X(-1), ax.Y(1.03) - 3, 'y | s₂', { cls: 't-s', anchor: 'middle' }, gP);
      A.text(ax.X(1), ax.Y(1.03) - 3, 'y | s₁', { cls: 't-s', anchor: 'middle' }, gP);
      var dA = A.arrow(ax.X(0), ax.Y(0) + 26, ax.X(1), ax.Y(0) + 26, 's-ink w1', gP, 5);
      A.text(ax.X(0.5), ax.Y(0) + 40, 'd/2 = 1', { cls: 't-s', anchor: 'middle' }, gP);
      var qt = A.text(304, 230, '', { cls: 't-b', anchor: 'middle' }), qv = A.text(304, 250, '', { cls: 'f-bad t-b', anchor: 'middle' });
      function curves() {
        function g(x, mu) { return Math.exp(-(x - mu) * (x - mu) / (2 * sig * sig)); }
        A.setCurve(g1, ax, function (x) { return g(x, 1); }, 120);
        A.setCurve(g2, ax, function (x) { return g(x, -1); }, 120);
        var pts = [[ax.X(-2.4), ax.Y(0)]];
        for (var n = 0; n <= 60; n++) { var x = -2.4 + 2.4 * n / 60; pts.push([ax.X(x), ax.Y(g(x, 1))]); }
        pts.push([ax.X(0), ax.Y(0)]);
        A.set(shade, { d: A.pts(pts) + 'Z' });
      }
      var kk = 0;
      A.slider({ label: '噪声 σ', min: 0.2, max: 1, step: 0.05, value: sig, fmt: function (v) { return 'σ = ' + v.toFixed(2); }, on: function (v) { sig = v; curves(); A.redraw(); } });
      curves();
      return {
        step: function (k) { kk = k; },
        frame: function (ts, dt, k) {
          var p = A.prog(ts, 0.9), y;
          if (k === 0) y = [A.lerp(1, Y0[0], p), A.lerp(1, Y0[1], p)];
          else if (k < 3) y = Y0;
          else if (k === 3) y = [A.lerp(Y0[0], Y1[0], p), A.lerp(Y0[1], Y1[1], p)];
          else y = Y1;
          var py = P(y), s1 = P(S[0]);
          A.set(yp, { cx: py[0], cy: py[1], cls: k >= 3 ? 'f-bad s-card w1' : 'f-gold s-card w1' });
          A.set(ylab, { x: py[0] + 8, y: py[1] - 6 });
          A.moveArrow(na, s1[0], s1[1], py[0], py[1]);
          var dd = S.map(function (s) { return Math.hypot(y[0] - s[0], y[1] - s[1]); }), best = dd.indexOf(Math.min.apply(null, dd));
          var showD = k === 1 || (k === 3 && p > 0.95) || k > 3;
          dl.forEach(function (l, i) {
            var q = P(S[i]); show(l, showD);
            A.set(l, { x1: py[0], y1: py[1], x2: q[0], y2: q[1], cls: i === best ? (best === 0 ? 's-good w3' : 's-bad w3') : 's-line w1 dash' });
          });
          op(gR, k < 2 ? 0 : k === 2 ? p : 1);
          op(gP, k < 4 ? 0.15 : 1);
          op(shade, (k < 4 ? 0 : k === 4 ? p : 1) * 0.6);
          op(dA, k >= 4 ? 1 : 0);
          var arg = 1 / sig;
          A.setText(qt, k === 5 ? 'Q(d/2σ) = Q(' + arg.toFixed(2) + ')' : '');
          A.setText(qv, k === 5 ? '= ' + sci(A.Q(arg)) : '');
          if (showD && (k === 1 || k === 3)) A.note(nm.map(function (n, i) { return '‖y−' + n + '‖=' + dd[i].toFixed(2); }).join('　') + ' → 判 ' + nm[best]);
          else if (k >= 4) A.note('σ = ' + sig.toFixed(2) + '：P(s₁→s₂) = Q(1/' + sig.toFixed(2) + ') = Q(' + arg.toFixed(2) + ') = ' + sci(A.Q(arg), true));
          else A.note('');
        }
      };
    }
  });

  /* ================= 3.4 power vs bandwidth efficiency ================= */
  ANIM.reg('p2:3.4', {
    title: '功率效率 vs 带宽效率：两个系统比一比',
    cap: '两个系统每维平均能量都是 1。系统 I 用 1 维发 1 bit（±1）；系统 II 用 2 维发 1 bit（两点同号 ±(1, 1)，这是按讲义 b̄ = ½、P̄<sub>s</sub> = ½Q(√2/σ) 还原的画法），两点距离从 2 拉到 2√2，误码率更低，代价是维数 D = 2BT 翻倍 = 带宽翻倍。',
    h: 236,
    init: function (A) {
      var sig = 0.5;
      A.text(100, 18, '系统 I（D = 1）', { cls: 't-b', anchor: 'middle' });
      A.text(300, 18, '系统 II（D = 2）', { cls: 't-b', anchor: 'middle' });
      A.line(200, 6, 200, 226, 's-line w1');
      /* system I: 1-D */
      var c1x = 100, c1y = 98, k1 = 40;
      A.line(18, c1y, 182, c1y, 's-soft w1');
      A.line(c1x, c1y - 58, c1x, c1y + 6, 's-soft w1 dash');
      var b1 = [A.path('', 's-acc w2'), A.path('', 's-acc w2')];
      [-1, 1].forEach(function (s) { A.circle(c1x + s * k1, c1y, 4.5, 'f-ink'); A.text(c1x + s * k1, c1y + 15, s > 0 ? '+1' : '−1', { cls: 't-s', anchor: 'middle' }); });
      A.line(c1x - k1, c1y + 24, c1x + k1, c1y + 24, 's-ink w1');
      A.text(c1x, c1y + 38, 'd = 2', { cls: 't-s', anchor: 'middle' });
      /* system II: 2-D */
      var c2x = 300, c2y = 80, k2 = 30;
      A.line(c2x - 62, c2y, c2x + 62, c2y, 's-soft w1'); A.line(c2x, c2y - 58, c2x, c2y + 58, 's-soft w1');
      A.line(c2x - 50, c2y - 50, c2x + 50, c2y + 50, 's-soft w1 dash');
      var r2c = [A.circle(c2x + k2, c2y - k2, 1, 'f-none s-acc w1'), A.circle(c2x - k2, c2y + k2, 1, 'f-none s-acc w1')];
      A.line(c2x - k2, c2y + k2, c2x + k2, c2y - k2, 's-ink w1');
      A.circle(c2x + k2, c2y - k2, 4.5, 'f-ink'); A.circle(c2x - k2, c2y + k2, 4.5, 'f-ink');
      A.text(c2x + k2 + 32, c2y - k2 - 18, '(1, 1)', { cls: 't-s' });
      A.text(c2x - k2 - 32, c2y + k2 + 26, '(−1, −1)', { cls: 't-s', anchor: 'end' });
      A.text(348, 106, 'd = 2√2', { cls: 't-s' });
      /* numbers */
      A.text(14, 160, '带宽', { cls: 't-s' }); A.rect(44, 151, 40, 11, 'f-accs s-acc w1', null, 2); A.text(90, 160, '1 份', { cls: 't-s' });
      A.text(210, 160, '带宽', { cls: 't-s' }); A.rect(240, 151, 80, 11, 'f-accs s-acc w1', null, 2); A.text(326, 160, '2 份', { cls: 't-s' });
      A.text(14, 180, 'b/D = 1 bit/维'); A.text(210, 180, 'b/D = ½ bit/维');
      A.text(14, 199, '每维能量 ε_{x}/D = 1', { cls: 't-s' }); A.text(210, 199, '每维能量 ε_{x}/D = (1+1)/2 = 1', { cls: 't-s' });
      var p1 = A.text(14, 222, '', { cls: 't-b' }), p2 = A.text(208, 222, '', { cls: 't-b f-good' });
      function draw() {
        [-1, 1].forEach(function (s, i) {
          var pts = [];
          for (var n = 0; n <= 50; n++) { var u = -2.8 + 5.6 * n / 50; pts.push([c1x + (s + u * sig) * k1, c1y - 40 * Math.exp(-u * u / 2)]); }
          A.set(b1[i], { d: A.pts(pts.filter(function (q) { return q[0] >= 16 && q[0] <= 184; })) });
        });
        r2c.forEach(function (c) { A.set(c, { r: sig * k2 }); });
        var P1 = A.Q(1 / sig), P2 = 0.5 * A.Q(Math.SQRT2 / sig);
        A.setText(p1, 'P_{s}/D = Q(1/σ) = ' + sci(P1));
        A.setText(p2, 'P_{s}/D = ½Q(√2/σ) = ' + sci(P2));
        A.note('σ = ' + sig.toFixed(2) + '：系统 II 的每维误码率是系统 I 的 1/' + (P1 / P2).toPrecision(3) + '，但带宽是 2 倍：用带宽效率换功率效率');
      }
      A.slider({ label: '噪声 σ', min: 0.3, max: 1, step: 0.05, value: sig, fmt: function (v) { return 'σ = ' + v.toFixed(2); }, on: function (v) { sig = v; draw(); } });
      draw();
      return {};
    }
  });

  /* ================= 3.5 BER in Rayleigh fading ================= */
  ANIM.reg('p2:3.5', {
    title: '衰落下的误码率：瀑布 vs 斜坡',
    cap: '蓝：AWGN（SNR 固定），误码率随 SNR 指数下降，像瀑布。红：瑞利衰落下的平均误码率，只按 1/γ̄ 线性下降（log 图上是斜率 −1 的直线），因为平均值几乎全来自深衰落那段时间。虚线是高 SNR 近似。',
    h: 246,
    init: function (A) {
      var mod = 0, g = 20;
      var M = [
        { n: 'BPSK', aw: function (x) { return A.Q(Math.sqrt(2 * x)); }, ry: function (x) { return 0.5 * (1 - Math.sqrt(x / (1 + x))); }, as: function (x) { return 1 / (4 * x); }, an: '1/(4γ̄)', fa: 'Q(√(2γ))', fr: '½(1−√(γ̄/(1+γ̄)))' },
        { n: 'DPSK', aw: function (x) { return 0.5 * Math.exp(-x); }, ry: function (x) { return 1 / (2 * (1 + x)); }, as: function (x) { return 1 / (2 * x); }, an: '1/(2γ̄)', fa: '½e^{−γ}', fr: '1/(2(1+γ̄))' }
      ];
      var ax = A.axes({ x: 46, y: 16, w: 328, h: 184, xr: [0, 40], yr: [-6, 0], yl: 'P_{b}', ticksX: [0, 10, 20, 30, 40], ticksY: logTicks(-6, 0), grid: true, xAxisAt: 'bottom' });
      A.text(210, 238, '平均 SNR γ̄（dB）', { cls: 't-s', anchor: 'middle' });
      function L(f) { return function (x) { var p = f(A.undb(x)); return p >= 1e-6 ? Math.log10(p) : null; }; }
      var cAs = A.curve(ax, function () { return null; }, 's-bad w1 dash op7');
      var cAw = A.curve(ax, function () { return null; }, 's-acc w3');
      var cRy = A.curve(ax, function () { return null; }, 's-bad w3');
      var lAw = A.text(0, 0, 'AWGN', { cls: 'f-acc t-b' }), lRy = A.text(0, 0, '瑞利衰落', { cls: 'f-bad t-b', anchor: 'end' });
      var gap = A.g(), ga1 = A.arrow(0, 0, 0, 0, 's-ink w1', gap, 5), ga2 = A.arrow(0, 0, 0, 0, 's-ink w1', gap, 5), gt = A.text(0, 0, '', { cls: 't-s', anchor: 'middle' }, gap);
      var vl = A.line(0, ax.y, 0, ax.y + ax.h, 's-gold w2 dash');
      var dA = A.circle(0, 0, 4.5, 'f-acc s-card w1'), dR = A.circle(0, 0, 4.5, 'f-bad s-card w1');
      function solve(f, target) { /* dB where f(dB) = target, f decreasing */
        var a = -10, b = 60;
        for (var i = 0; i < 80; i++) { var m = (a + b) / 2; if (f(A.undb(m)) > target) a = m; else b = m; }
        return (a + b) / 2;
      }
      function curves() {
        var m = M[mod];
        A.setCurve(cAw, ax, L(m.aw), 240); A.setCurve(cRy, ax, L(m.ry), 160);
        A.setCurve(cAs, ax, function (x) { return x < 6 ? null : L(m.as)(x); }, 120);
        var x5 = solve(m.aw, 1e-5);
        A.set(lAw, { x: ax.X(x5) + 7, y: ax.Y(-5) + 4 });
        A.set(lRy, { x: ax.X(39), y: ax.Y(Math.log10(m.ry(A.undb(39)))) + 20 });
        var xa = solve(m.aw, 1e-3), xr = solve(m.ry, 1e-3), yy = ax.Y(-3), mid = (ax.X(xa) + ax.X(xr)) / 2;
        A.moveArrow(ga1, mid, yy, ax.X(xa) + 3, yy); A.moveArrow(ga2, mid, yy, ax.X(xr) - 3, yy);
        A.set(gt, { x: mid, y: yy - 6, text: '差 ' + (xr - xa).toFixed(1) + ' dB' });
      }
      function draw() {
        var m = M[mod], x = A.undb(g), pa = m.aw(x), pr = m.ry(x);
        A.set(vl, { x1: ax.X(g), x2: ax.X(g) });
        show(dA, pa >= 1e-6); A.set(dA, { cx: ax.X(g), cy: ax.Y(Math.log10(Math.max(pa, 1e-6))) });
        A.set(dR, { cx: ax.X(g), cy: ax.Y(Math.log10(pr)) });
        var drop = g <= 30 ? '；γ̄ 再 +10 dB，瑞利只降 ' + (pr / m.ry(x * 10)).toFixed(1) + ' 倍' : '';
        A.note(m.n + '，γ̄ = ' + g + ' dB = ' + sci(x, true) + '：AWGN ' + sci(pa, true) + '；瑞利 ' + sci(pr, true) + '（≈ ' + m.an + ' = ' + sci(m.as(x), true) + '）' + drop);
      }
      A.choice({ label: '调制', options: ['BPSK', 'DPSK'], value: 0, on: function (v) { mod = v; curves(); draw(); } });
      A.slider({ label: '平均 SNR', min: 0, max: 40, step: 1, value: g, unit: 'dB', on: function (v) { g = v; draw(); } });
      curves(); draw();
      return {};
    }
  });

  /* ================= 4.1 macro vs micro diversity ================= */
  ANIM.reg('p2:4.1', {
    title: '分集：独立的两条支路很难同时变差',
    cap: '两条支路（蓝、金）各自衰落。红线标出“两路同时低于门限”的时刻，它比单路低于门限少得多，前提是两路独立。微分集：几根天线隔开几个波长，对付多径快衰落；宏分集：几个不同位置的基站，对付楼房造成的阴影。频率、时间、极化分集同理：只要支路独立。',
    h: 262,
    init: function (A) {
      var mode = 0, th = dB(0.151);
      var gm = A.g(), gM = A.g();
      function tower(x, y, g) { A.poly([[x - 6, y + 20], [x, y], [x + 6, y + 20]], 's-ink w1', g); A.circle(x, y, 2.5, 'f-ink', g); }
      function phone(x, y, g) { A.rect(x - 5, y, 10, 17, 'f-card s-ink w1', g, 2); }
      tower(32, 12, gm); tower(56, 12, gm); A.text(44, 48, '相距几个 λ', { cls: 't-s', anchor: 'middle' }, gm);
      phone(340, 14, gm);
      A.poly([[32, 12], [150, 6], [335, 20]], 's-acc w1', gm); A.poly([[56, 12], [210, 40], [335, 24]], 's-gold w1', gm);
      A.poly([[32, 12], [260, 44], [338, 28]], 's-acc w1 op5', gm); A.poly([[56, 12], [110, 40], [338, 18]], 's-gold w1 op5', gm);
      A.text(200, 62, '同一基站两根天线：各自的多径叠加独立', { cls: 't-s', anchor: 'middle' }, gm);
      tower(30, 10, gM); tower(370, 10, gM); phone(200, 22, gM);
      A.text(30, 46, '基站 A', { cls: 't-s', anchor: 'middle' }, gM); A.text(370, 46, '基站 B', { cls: 't-s', anchor: 'middle' }, gM);
      A.rect(100, 12, 26, 38, 'f-line s-soft w1', gM, 1);
      A.line(30, 12, 195, 28, 's-acc w1 dash', gM); A.line(370, 12, 205, 28, 's-gold w1', gM);
      A.text(200, 62, '被楼挡住的方向和另一个基站的方向不同', { cls: 't-s', anchor: 'middle' }, gM);
      var ax = A.axes({ x: 40, y: 80, w: 326, h: 136, xr: [0, 1], yr: [-30, 10], xl: 't', yl: 'SNR（dB，相对 γ̄）', ticksY: [{ v: -30, l: '−30' }, { v: -20, l: '−20' }, { v: -10, l: '−10' }, { v: 0, l: '0' }, { v: 10, l: '10' }], xAxisAt: 'bottom' });
      A.line(ax.X(0), ax.Y(th), ax.X(1), ax.Y(th), 's-bad w1 dash');
      sm(A.text(ax.X(1) + 4, ax.Y(th) + 4, '门限', { cls: 'f-bad' }));
      var both = A.path('', 's-bad w4');
      var c1 = A.path('', 's-acc w2'), c2 = A.path('', 's-gold w2');
      var st = A.text(40, 254, '', { cls: 't-s' });
      var r1 = rayGen(A, 10, 6), r2g = rayGen(A, 10, 6);
      var sh = [0, 1].map(function () { var f = [], p = []; for (var i = 0; i < 6; i++) { f.push(0.3 + A.rand() * 1.4); p.push(A.rand() * TAU); } return { f: f, p: p }; });
      function shadow(s, t) { var v = 0; for (var i = 0; i < 6; i++) v += Math.sqrt(2 / 6) * Math.cos(TAU * s.f[i] * t + s.p[i]); return 6 * v; }
      function theory() {
        if (mode === 0) { var p = 1 - Math.exp(-0.151); A.note('多径（瑞利）：门限 γ₀/γ̄ = 0.151（' + th.toFixed(1) + ' dB），单路 p = 1 − e<sup>−0.151</sup> = ' + (100 * p).toFixed(1) + '%；独立两路同时 p² = ' + (100 * p * p).toFixed(1) + '%'); }
        else { var q = A.Q(-th / 6); A.note('阴影（σ = 6 dB 对数正态）：单路 p = Q(' + (-th).toFixed(1) + '/6) = ' + (100 * q).toFixed(1) + '%；独立两路同时 p² = ' + (100 * q * q).toFixed(2) + '%'); }
      }
      A.choice({ options: ['微分集（多径）', '宏分集（阴影）'], value: 0, on: function (v) { mode = v; theory(); A.redraw(); } });
      theory();
      return function frame(t) {
        show(gm, mode === 0); show(gM, mode === 1);
        var N = 200, p1 = [], p2 = [], d = '', n1 = 0, n2 = 0, nb = 0, run = -1;
        for (var i = 0; i <= N; i++) {
          var x = i / N, tt = t * 0.12 + x, v1, v2;
          if (mode === 0) { v1 = dB(abs2(r1(tt))); v2 = dB(abs2(r2g(tt))); }
          else { v1 = shadow(sh[0], tt); v2 = shadow(sh[1], tt); }
          p1.push([ax.X(x), ax.Y(A.clamp(v1, -30, 10))]); p2.push([ax.X(x), ax.Y(A.clamp(v2, -30, 10))]);
          var b1 = v1 < th, b2 = v2 < th;
          n1 += b1; n2 += b2;
          var bb = b1 && b2;
          if (bb) { nb++; if (run < 0) run = i; }
          if (run >= 0 && (!bb || i === N)) {
            var end = bb ? i : i - 1, yb = (ax.y + ax.h - 3).toFixed(1);
            d += 'M' + ax.X(run / N).toFixed(1) + ' ' + yb + 'L' + ax.X(Math.min(1, Math.max(end, run + 0.5) / N)).toFixed(1) + ' ' + yb;
            run = -1;
          }
        }
        A.set(c1, { d: A.pts(p1) }); A.set(c2, { d: A.pts(p2) }); A.set(both, { d: d });
        var pc = function (n) { return Math.round(100 * n / (N + 1)) + '%'; };
        A.setText(st, '这一段：路 1 低于门限 ' + pc(n1) + '，路 2 ' + pc(n2) + '，两路同时（红）' + pc(nb));
      };
    }
  });

  /* ================= 4.2 SC / EGC / MRC ================= */
  ANIM.reg('p2:4.2', {
    title: 'SC / EGC / MRC：两路怎么合成一路',
    cap: '上：两路瞬时 SNR γ₁、γ₂（每路平均 γ̄ = 1，即 0 dB）和所选合并器的输出（绿）。下：右端时刻的数值，A<sub>i</sub> = √γ<sub>i</sub>（E<sub>b</sub>/N₀ = 1）。SC 只能挑大的，MRC 把两路相加，EGC 只对齐相位、等权相加，和 MRC 很接近。',
    h: 286,
    init: function (A) {
      var m = 2, h1 = rayGen(A, 10, 3), h2 = rayGen(A, 10, 3);
      var ax = A.axes({ x: 40, y: 24, w: 330, h: 118, xr: [0, 1], yr: [-20, 10], yl: 'SNR（dB）', ticksY: [{ v: -20, l: '−20' }, { v: -10, l: '−10' }, { v: 0, l: '0' }, { v: 10, l: '10' }], grid: true, xAxisAt: 'bottom' });
      A.line(150, 10, 166, 10, 's-acc w2'); A.text(169, 14, 'γ₁', { cls: 't-s' });
      A.line(192, 10, 208, 10, 's-gold w2'); A.text(211, 14, 'γ₂', { cls: 't-s' });
      A.line(234, 10, 250, 10, 's-good w3'); var lt = A.text(253, 14, '', { cls: 't-s' });
      A.line(ax.X(1), ax.y, ax.X(1), ax.y + ax.h, 's-soft w1 dash');
      var c1 = A.path('', 's-acc w1'), c2 = A.path('', 's-gold w1'), co = A.path('', 's-good w3');
      var names = ['γ₁', 'γ₂', 'SC', 'EGC', 'MRC'], forms = ['A₁²', 'A₂²', 'max(γ₁,γ₂)', '(A₁+A₂)²/2', 'γ₁ + γ₂'];
      var base = 250, sc = 24, bars = [], vals = [], X = [62, 134, 206, 278, 350];
      A.line(24, base, 390, base, 's-soft w1');
      for (var i = 0; i < 5; i++) {
        bars.push(A.rect(X[i] - 17, base, 34, 0, i === 0 ? 'f-acc op7 s-none' : i === 1 ? 'f-gold op7 s-none' : 'f-line s-none', null, 2));
        vals.push(A.text(X[i], base - 4, '', { cls: 't-s t-m', anchor: 'middle' }));
        A.text(X[i], 266, names[i], { cls: 't-b', anchor: 'middle' });
        A.text(X[i], 281, forms[i], { cls: 't-s', anchor: 'middle' });
      }
      A.note('每路平均 γ̄ = 1 时的平均输出：SC γ̄(1 + ½) = ' + (1 + 1 / 2) + '，EGC 1 + π/4 = ' + (1 + Math.PI / 4).toFixed(2) + '，MRC γ̄ + γ̄ = 2');
      function comb(a1, a2) { var g1 = a1 * a1, g2 = a2 * a2; return [g1, g2, Math.max(g1, g2), (a1 + a2) * (a1 + a2) / 2, g1 + g2]; }
      A.choice({ label: '合并', options: ['SC 选择', 'EGC 等增益', 'MRC 最大比'], value: m, on: function (v) { m = v; A.redraw(); } });
      return function frame(t) {
        var N = 160, p1 = [], p2 = [], po = [], last;
        for (var i = 0; i <= N; i++) {
          var x = i / N, tt = t * 0.15 + x, v = comb(Math.sqrt(abs2(h1(tt))), Math.sqrt(abs2(h2(tt))));
          p1.push([ax.X(x), ax.Y(A.clamp(dB(v[0]), -20, 10))]); p2.push([ax.X(x), ax.Y(A.clamp(dB(v[1]), -20, 10))]);
          po.push([ax.X(x), ax.Y(A.clamp(dB(v[2 + m]), -20, 10))]);
          last = v;
        }
        A.set(c1, { d: A.pts(p1) }); A.set(c2, { d: A.pts(p2) }); A.set(co, { d: A.pts(po) });
        A.setText(lt, names[2 + m] + ' 输出');
        for (var j = 0; j < 5; j++) {
          var hgt = Math.min(last[j], 3.3) * sc;
          A.set(bars[j], { y: base - hgt, height: hgt });
          if (j >= 2) A.set(bars[j], { cls: j === 2 + m ? 'f-good s-none' : 'f-line s-none' });
          A.set(vals[j], { y: base - hgt - 4, text: last[j].toFixed(2) + (last[j] > 3.3 ? '↑' : '') });
        }
      };
    }
  });

  /* ================= 4.3 BER after diversity: slope = diversity order ================= */
  ANIM.reg('p2:4.3', {
    title: '分集后的误码率：斜率 = 分集阶数',
    cap: 'DPSK + M 路选择分集，用讲义 p.25 的公式 P̄<sub>b</sub> = (M/2)Σ(−1)<sup>n</sup>C(M−1,n)/(γ̄+n+1)。两个圆点相差 10 dB：M = 1 只降约 10 倍，M = 2 约 100 倍，M = 4 约 10⁴ 倍，高 SNR 时斜率趋于 −M。',
    h: 250,
    init: function (A) {
      var g = 10, Ms = [1, 2, 4], cls = ['bad', 'gold', 'good'];
      function binom(n, k) { var r = 1; for (var i = 1; i <= k; i++) r = r * (n - k + i) / i; return r; }
      function pb(M, x) { var s = 0; for (var n = 0; n < M; n++) s += (n % 2 ? -1 : 1) * binom(M - 1, n) / (x + n + 1); return M / 2 * s; }
      var ax = A.axes({ x: 50, y: 18, w: 326, h: 190, xr: [0, 30], yr: [-10, 0], yl: '平均 P_{b}', ticksX: [0, 10, 20, 30], ticksY: logTicks(-10, 0).filter(function (t) { return t.v % 2 === 0; }), grid: true, xAxisAt: 'bottom' });
      A.text(213, 244, '每路平均 SNR γ̄（dB）', { cls: 't-s', anchor: 'middle' });
      var v1 = A.line(0, ax.y, 0, ax.y + ax.h, 's-soft w1 dash'), v2 = A.line(0, ax.y, 0, ax.y + ax.h, 's-soft w1 dash');
      var dots = [];
      Ms.forEach(function (M, i) {
        A.curve(ax, function (x) { var p = pb(M, A.undb(x)); return p >= 1e-10 ? Math.log10(p) : null; }, 's-' + cls[i] + ' w3', null, 200);
        A.line(222 + i * 56, 32, 240 + i * 56, 32, 's-' + cls[i] + ' w3');
        A.text(244 + i * 56, 36, 'M=' + M, { cls: 't-s' });
        dots.push([A.circle(0, 0, 4, 'f-' + cls[i] + ' s-card w1'), A.circle(0, 0, 4, 'f-' + cls[i] + ' s-card w1')]);
      });
      function draw() {
        var a = A.undb(g), b = A.undb(g + 10), parts = [];
        A.set(v1, { x1: ax.X(g), x2: ax.X(g) }); A.set(v2, { x1: ax.X(g + 10), x2: ax.X(g + 10) });
        Ms.forEach(function (M, i) {
          var pa = pb(M, a), pB = pb(M, b);
          A.set(dots[i][0], { cx: ax.X(g), cy: ax.Y(Math.log10(pa)) });
          A.set(dots[i][1], { cx: ax.X(g + 10), cy: ax.Y(Math.log10(pB)) });
          show(dots[i][1], pB >= 1e-10);
          parts.push('M=' + M + '：' + sci(pa, true) + ' → ' + sci(pB, true) + '，斜率 ' + Math.log10(pa / pB).toFixed(2));
        });
        A.note('γ̄ = ' + g + ' → ' + (g + 10) + ' dB<br>' + parts.join('<br>'));
      }
      A.slider({ label: '左圆点 γ̄', min: 0, max: 20, step: 1, value: g, unit: 'dB', on: function (v) { g = v; draw(); } });
      draw();
      return {};
    }
  });

  /* ================= 4.4 diversity–multiplexing trade-off ================= */
  ANIM.reg('p2:4.4', {
    title: '分集-复用折中：8 × 4 MIMO 能传多快',
    cap: 'Practice 5 第 3 题：N = 8 发、M = 4 收，d(r) = (N − r)(M − r)，r、d 取整数。d 管误码率（P<sub>e</sub> = γ<sup>−d</sup>），r 管速率（R = r log₂γ）。多拿一份复用，就少一大块分集。',
    h: 250,
    steps: [
      '横轴 r 管速率，纵轴 d 管误码率。全用来分集：r = 0，d = N × M = 32。',
      '每多复用一路：d(r) = (8−r)(4−r) = 32、21、12、5、0；r ≤ min(N, M) = 4。',
      '要求 P<sub>e</sub> = γ<sup>−d</sup> ≤ 10⁻³，γ = 10 dB = 10（线性）→ 10<sup>−d</sup> ≤ 10⁻³ → d ≥ 3。',
      '满足 d ≥ 3 的最大 r 是 3（d = 5）；r = 4 时 d = 0，不满足。',
      '速率 R = r·log₂γ = 3 × log₂10 ≈ 9.97 bit/s/Hz；误码率 P<sub>e</sub> = 10⁻⁵。'
    ],
    tween: 1,
    init: function (A) {
      var N = 8, M = 4, gam = 10, Pe = 1e-3, rmax = Math.min(N, M);
      var dmin = Math.ceil(-Math.log10(Pe) / Math.log10(gam) - 1e-9);
      var pts = [], best = 0;
      for (var r = 0; r <= rmax; r++) { var d = (N - r) * (M - r); pts.push([r, d]); if (d >= dmin) best = r; }
      var dB_ = pts[best][1], R = best * Math.log2(gam);
      var ax = A.axes({ x: 40, y: 24, w: 210, h: 196, xr: [0, 4.5], yr: [0, 35], xl: 'r', yl: 'd', ticksX: [0, 1, 2, 3, 4], ticksY: [0, 10, 20, 30], grid: true, xAxisAt: 'bottom', yAxisAt: 'left' });
      var line = A.curve(ax, pts, 's-acc w1 dot');
      var dots = pts.map(function (p) { return A.circle(ax.X(p[0]), ax.Y(p[1]), 5, 'f-acc s-card w1'); });
      var labs = pts.map(function (p) { return A.text(ax.X(p[0]) + 12, ax.Y(p[1]) - 8, String(p[1]), { cls: 't-s t-b' }); });
      var req = A.g({ opacity: 0 });
      A.rect(ax.X(0), ax.Y(dmin), ax.w, ax.Y(0) - ax.Y(dmin), 'f-bads s-none', req, 0);
      A.line(ax.X(0), ax.Y(dmin), ax.X(4.5), ax.Y(dmin), 's-bad w2 dash', req);
      A.text(ax.X(4.45), ax.Y(dmin) - 5, 'd ≥ ' + dmin, { cls: 'f-bad t-b', anchor: 'end' }, req);
      var ring = A.circle(ax.X(best), ax.Y(dB_), 10, 'f-none s-good w3');
      var res = A.g({ opacity: 0 });
      A.text(ax.X(4.4), 46, 'R = ' + best + ' × log₂' + gam, { anchor: 'end', cls: 't-b' }, res);
      A.text(ax.X(4.4), 64, '= ' + R.toFixed(2) + ' bit/s/Hz', { anchor: 'end', cls: 't-b f-good' }, res);
      A.text(ax.X(4.4), 84, 'P_{e} = γ^{−d} = ' + gam + '^{−' + dB_ + '}' + (gam === 10 ? '' : ' = 10^{−' + Math.round(dB_ * Math.log10(gam)) + '}'), { anchor: 'end' }, res);
      /* table */
      var tx = 270;
      A.text(tx, 34, 'r', { cls: 't-b' }); A.text(tx + 28, 34, 'd = (8−r)(4−r)', { cls: 't-b t-s' });
      var rows = pts.map(function (p, i) {
        var g = A.g({ opacity: 0 });
        var bg = A.rect(tx - 6, 44 + i * 26, 126, 22, 'f-none s-none', g, 4);
        A.text(tx, 59 + i * 26, String(p[0]), { cls: 't-m' }, g);
        A.text(tx + 28, 59 + i * 26, '(' + (N - p[0]) + ')(' + (M - p[0]) + ') = ' + p[1], { cls: 't-m' }, g);
        return { g: g, bg: bg };
      });
      var kk = 0;
      return {
        step: function (k) { kk = k; },
        frame: function (ts, dt, k) {
          var p = A.prog(ts, 1);
          pts.forEach(function (q, i) {
            var on = k === 0 ? (i === 0 ? 1 : 0) : k === 1 ? A.clamp(p * 5 - i + 1, 0, 1) : 1;
            if (k === 0 && i === 0) on = p;
            op(dots[i], on); op(labs[i], on); op(rows[i].g, on);
            var good = q[1] >= dmin;
            A.set(dots[i], { cls: k >= 2 ? (good ? 'f-acc s-card w1' : 'f-bad s-card w1') : 'f-acc s-card w1' });
            A.set(rows[i].bg, { cls: k >= 3 && i === best ? 'f-goods s-good w1' : k >= 2 && !good ? 'f-bads s-none' : 'f-none s-none' });
          });
          op(line, k >= 1 ? (k === 1 ? p : 1) : 0);
          op(req, k >= 2 ? (k === 2 ? p : 1) : 0);
          op(ring, k >= 3 ? (k === 3 ? p : 1) : 0);
          op(res, k >= 4 ? p : 0);
        }
      };
    }
  });

  /* ================= 5.1 y = Hx + v ================= */
  ANIM.reg('p2:5.1', {
    title: 'MIMO 信号模型 y = Hx + v',
    cap: 'N = 2 根发射、M = 3 根接收（讲义约定 N 发 M 收）。H 是 M × N = 3 × 2：行对应接收天线，列对应发射天线，h<sub>m,n</sub> = 第 n 根发 → 第 m 根收。平坦、时不变信道：每对天线一个复数增益。',
    h: 266,
    steps: [
      'N = 2 根发射天线发 x₁、x₂，M = 3 根接收天线收 y₁、y₂、y₃。',
      'h<sub>m,n</sub>：第 n 根发 → 第 m 根收。h₂₁（Tx1 → Rx2）放在 H 第 2 行第 1 列。',
      '第 1 根接收天线收到所有发射信号的加权和，再加噪声：y₁ = h₁₁x₁ + h₁₂x₂ + v₁。',
      '每根接收天线写一行：行 = 接收天线，列 = 发射天线，H 是 M × N = 3 × 2。',
      '叠起来：y = Hx + v。v 每根接收天线一个，互相独立、方差 σ²。',
      '平坦衰落：各条回波在一个符号内叠成一个复数，每对天线只有一个 h，没有 ISI。'
    ],
    tween: 1.6,
    live: true,
    init: function (A) {
      var TX = [[48, 82], [48, 162]], RX = [[184, 52], [184, 122], [184, 192]];
      function ant(x, y, lab, right) {
        A.line(x, y + 10, x, y - 10, 's-ink w2'); A.poly([[x - 7, y - 16], [x, y - 8], [x + 7, y - 16]], 's-ink w1');
        A.text(right ? x + 12 : x - 12, y + 4, lab, { cls: 't-b', anchor: right ? 'start' : 'end' });
      }
      var links = [], lab = [], pulses = [];
      for (var m = 0; m < 3; m++) for (var n = 0; n < 2; n++) {
        links.push(A.line(TX[n][0] + 6, TX[n][1], RX[m][0] - 6, RX[m][1], 's-line w1'));
        var tx = A.lerp(TX[n][0], RX[m][0], 0.3), ty = A.lerp(TX[n][1], RX[m][1], 0.3);
        lab.push(sm(A.text(tx, ty - 9, 'h_{' + (m + 1) + (n + 1) + '}', { cls: 'f-acc', anchor: 'middle' })));
        pulses.push(A.circle(0, 0, 3, 'f-acc'));
      }
      TX.forEach(function (p, i) { ant(p[0], p[1], 'x_{' + (i + 1) + '}', false); });
      RX.forEach(function (p, i) { ant(p[0], p[1], 'y_{' + (i + 1) + '}', true); });
      A.text(40, 22, '发射 N = 2', { cls: 't-s', anchor: 'middle' }); A.text(192, 22, '接收 M = 3', { cls: 't-s', anchor: 'middle' });
      var noise = RX.map(function (p, i) { var g = A.g({ opacity: 0 }); A.arrow(p[0] + 30, p[1] + 30, p[0] + 6, p[1] + 12, 's-bad w1', g, 5); sm(A.text(p[0] + 33, p[1] + 36, 'v_{' + (i + 1) + '}', { cls: 'f-bad' }, g)); return g; });
      /* matrix */
      var mx = 288, my = 60;
      A.text(250, my + 70, 'H =', { cls: 't-b t-l', anchor: 'end' });
      A.text(mx, 40, 'Tx1', { cls: 't-s', anchor: 'middle' }); A.text(mx + 50, 40, 'Tx2', { cls: 't-s', anchor: 'middle' });
      A.path('M' + (mx - 30) + ' ' + (my - 4) + 'h-5v' + 128 + 'h5', 's-ink w2'); A.path('M' + (mx + 80) + ' ' + (my - 4) + 'h5v' + 128 + 'h-5', 's-ink w2');
      var cells = [], rowl = [];
      for (m = 0; m < 3; m++) {
        rowl.push(A.text(mx + 99, my + 22 + m * 40, 'Rx' + (m + 1), { cls: 't-s', anchor: 'middle' }));
        for (n = 0; n < 2; n++) {
          var c = A.rect(mx - 22 + n * 50, my + 4 + m * 40, 44, 28, 'f-none s-none', null, 4);
          A.text(mx + n * 50, my + 23 + m * 40, 'h_{' + (m + 1) + (n + 1) + '}', { cls: 't-m', anchor: 'middle' });
          cells.push(c);
        }
      }
      var dim = A.text(mx + 25, my + 148, '', { cls: 't-s', anchor: 'middle' });
      var eq = A.text(200, 250, '', { cls: 't-b t-l', anchor: 'middle' });
      var EQ = ['x = [x₁, x₂]ᵀ → y = [y₁, y₂, y₃]ᵀ', 'h₂₁：Tx1 → Rx2', 'y₁ = h₁₁x₁ + h₁₂x₂ + v₁', 'y_{m} = Σ_{n} h_{m,n} x_{n} + v_{m}', 'y (3×1) = H (3×2) · x (2×1) + v (3×1)', 'h_{m,n} = |h_{m,n}| e^{jθ_{m,n}}（一个复数）'];
      function on(k, m, n) { return k === 1 ? (m === 1 && n === 0) : k === 2 ? m === 0 : true; }
      return {
        step: function (k) { A.setText(eq, EQ[k]); A.setText(dim, k >= 3 ? 'M × N = 3 × 2' : ''); },
        frame: function (ts, dt, k) {
          for (var m = 0; m < 3; m++) for (var n = 0; n < 2; n++) {
            var i = m * 2 + n, o = on(k, m, n), hl = k === 1 || k === 2;
            A.set(links[i], { cls: o ? (hl ? 's-acc w2' : 's-acc w1 op7') : 's-line w1 op5' });
            show(lab[i], o && (hl || k === 3));
            show(pulses[i], o);
            var f = ((ts * 0.6 + n * 0.5) % 1);
            A.set(pulses[i], { cx: A.lerp(TX[n][0] + 6, RX[m][0] - 6, f), cy: A.lerp(TX[n][1], RX[m][1], f), cls: n === 0 ? 'f-acc' : 'f-gold' });
            var cc = 'f-none s-none';
            if (k === 1 && m === 1 && n === 0) cc = 'f-golds s-gold w1';
            else if (k === 2 && m === 0) cc = 'f-accs s-acc w1';
            else if (k >= 3) cc = m % 2 ? 'f-goods s-none' : 'f-accs s-none';
            A.set(cells[i], { cls: cc });
          }
          noise.forEach(function (g, m) { op(g, k >= 4 || (k === 2 && m === 0) ? 1 : 0); });
          rowl.forEach(function (t, m) { op(t, k >= 3 || (k === 2 && m === 0) || (k === 1 && m === 1) ? 1 : 0.35); });
        }
      };
    }
  });

  /* ================= 5.2 SIMO receive diversity = MRC ================= */
  ANIM.reg('p2:5.2', {
    title: 'SIMO：乘 h* 把两路相位对齐再相加',
    cap: '箭头是两路信道 h₁（蓝）、h₂（金）在复平面上的样子。直接相加会随相位差时长时短；MRC 用 w = h，每路乘 h<sub>i</sub>*，变成实数 |h<sub>i</sub>|²，同相相加，合起来总是 |h₁|² + |h₂|²。拖两个滑块：MRC 的结果和相位差无关。',
    h: 270,
    steps: [
      '1 发 2 收：同一个 x 经过 h₁、h₂ 到两根天线，两路幅度、相位都不同。',
      '直接相加 y₁ + y₂：箭头首尾相接。相位差大时互相抵消，合起来很短（红）。',
      'MRC：每路乘 h<sub>i</sub>*，转回 −θ<sub>i</sub>（相位对齐），长度变成 |h<sub>i</sub>|²（按强弱加权）。',
      '对齐后同相相加：总长 |h₁|² + |h₂|² = ‖h‖²，不会抵消（绿）。',
      'SNR = E|x|²/σ² · ‖h‖²。w ∝ h 时最大（柯西-施瓦茨），这就是 MRC。'
    ],
    tween: 1.4,
    init: function (A) {
      var a2 = 0.7, dth = 150, th1 = 30 * DEG;
      var ox = 85, oy = 162, KS = 70;
      A.line(6, oy, 234, oy, 's-line w1'); A.line(ox, 14, ox, 258, 's-line w1');
      A.text(234, oy + 14, 'Re', { cls: 't-s', anchor: 'end' }); A.text(ox - 5, 24, 'Im', { cls: 't-s', anchor: 'end' });
      var ar1 = A.arrow(0, 0, 0, 0, 's-acc w3'), ar2 = A.arrow(0, 0, 0, 0, 's-gold w3'), res = A.arrow(0, 0, 0, 0, 's-bad w2');
      var l1 = A.text(0, 0, '', { cls: 'f-acc t-b', anchor: 'middle' }), l2 = A.text(0, 0, '', { cls: 'f-gold t-b', anchor: 'middle' });
      /* right panel: SNR bars */
      var bx = 248, bk = 52;
      A.text(bx, 30, 'SNR（取 E|x|²/σ² = 1）', { cls: 't-s' });
      var rowsT = ['单根天线 |h₁|²', '直接相加 |h₁+h₂|²/2', 'MRC  |h₁|²+|h₂|²'], cl = ['f-acc', 'f-bad', 'f-good'];
      var rows = rowsT.map(function (t, i) {
        var g = A.g({ opacity: 0 });
        A.text(bx, 58 + i * 52, t, { cls: 't-s' }, g);
        var r = A.rect(bx, 66 + i * 52, 10, 12, cl[i] + ' s-none', g, 2);
        var v = A.text(bx, 76 + i * 52, '', { cls: 't-s t-m' }, g);
        return { g: g, r: r, v: v };
      });
      function H() { return [cx(1, th1), cx(a2, th1 + dth * DEG)]; }
      var kk = 0;
      A.slider({ label: '相位差 θ₂−θ₁', min: 0, max: 360, step: 5, value: dth, unit: '°', on: function (v) { dth = v; A.redraw(); } });
      A.slider({ label: '|h₂|', min: 0.2, max: 1, step: 0.05, value: a2, fmt: function (v) { return v.toFixed(2); }, on: function (v) { a2 = v; A.redraw(); } });
      return {
        step: function (k) { kk = k; },
        frame: function (ts, dt, k) {
          var h = H(), p = A.prog(ts, 1.1), m1 = Math.sqrt(abs2(h[0])), m2 = Math.sqrt(abs2(h[1]));
          var t1 = Math.atan2(h[0][1], h[0][0]), t2 = Math.atan2(h[1][1], h[1][0]);
          var v1 = h[0], v2 = h[1], s2 = [0, 0], q = 0;
          if (k >= 2) { q = k === 2 ? p : 1; v1 = cx(m1 * A.lerp(1, m1, q), t1 * (1 - q)); v2 = cx(m2 * A.lerp(1, m2, q), t2 * (1 - q)); }
          if (k === 1) s2 = [v1[0] * p, v1[1] * p];
          else if (k === 3) s2 = [v1[0] * p, v1[1] * p];
          else if (k >= 4) s2 = v1;
          function P(z) { return [ox + z[0] * KS, oy - z[1] * KS]; }
          var a = P([0, 0]), b = P(v1), c = P(s2), d = P(cadd(s2, v2));
          A.moveArrow(ar1, a[0], a[1], b[0], b[1]); A.moveArrow(ar2, c[0], c[1], d[0], d[1]);
          var showRes = (k === 1 && p > 0.95) || k >= 3 && (k > 3 || p > 0.95);
          show(res, showRes);
          if (showRes) { var e = P(cadd(s2, v2)); A.moveArrow(res, a[0], a[1] + (k >= 3 ? 10 : 0), e[0], e[1] + (k >= 3 ? 10 : 0)); A.set(res, { cls: 'an-arrow ' + (k >= 3 ? 's-good w3' : 's-bad w2') }); }
          function lab(el, u, v, side, txt) {
            var dx = v[0] - u[0], dy = v[1] - u[1], L = Math.hypot(dx, dy) || 1;
            A.set(el, { x: (u[0] + v[0]) / 2 + side * 13 * dy / L, y: (u[1] + v[1]) / 2 - side * 13 * dx / L + 4, text: txt });
          }
          lab(l1, a, b, 1, k >= 2 ? '|h₁|²' : 'h₁'); lab(l2, c, d, k >= 3 ? 1 : -1, k >= 2 ? '|h₂|²' : 'h₂');
          var sn = [m1 * m1, abs2(cadd(h[0], h[1])) / 2, m1 * m1 + m2 * m2];
          rows.forEach(function (r, i) {
            op(r.g, i === 0 || (i === 1 && k >= 1) || (i === 2 && k >= 3) ? 1 : 0);
            A.set(r.r, { width: Math.max(1, sn[i] * bk) });
            A.set(r.v, { x: bx + Math.max(1, sn[i] * bk) + 5, text: sn[i].toFixed(2) });
          });
          A.note('h₁ = 1∠30°，h₂ = ' + a2.toFixed(2) + '∠' + (30 + dth) % 360 + '°：|h₁+h₂|² = ' + abs2(cadd(h[0], h[1])).toFixed(2) + '，‖h‖² = ' + sn[2].toFixed(2));
        }
      };
    }
  });

  /* ================= 5.3 MISO with / without CSI ================= */
  ANIM.reg('p2:5.3', {
    title: 'MISO：发端知不知道信道',
    cap: '2 发 1 收，总发射功率相同。知道 CSI：w = h/‖h‖，发端预先转好相位，两路在接收端同相相加，SNR = |h₁|² + |h₂|²，有分集。不知道：固定 w = [1, 1]/√2，两路随机地相加或抵消，SNR = |h₁+h₂|²/2，和单根天线的 |h|² 同分布，没有分集。',
    h: 262,
    init: function (A) {
      var mode = 0, h1 = rayGen(A, 10, 2.5), h2 = rayGen(A, 10, 2.5), th = -10;
      var ox = 70, oy = 128, k = 30;
      A.line(6, oy, 150, oy, 's-line w1'); A.line(ox, 56, ox, 204, 's-line w1');
      var ttl = A.text(76, 30, '', { cls: 't-b', anchor: 'middle' }), sub = A.text(76, 46, '', { cls: 't-s', anchor: 'middle' });
      var ar1 = A.arrow(0, 0, 0, 0, 's-acc w2', null, 6), ar2 = A.arrow(0, 0, 0, 0, 's-gold w2', null, 6), res = A.arrow(0, 0, 0, 0, 's-good w3', null, 7);
      var val = A.text(76, 224, '', { cls: 't-m', anchor: 'middle' });
      var ax = A.axes({ x: 186, y: 34, w: 196, h: 156, xr: [0, 1], yr: [-25, 10], xl: 't', yl: '接收 SNR（dB）', ticksY: [{ v: -20, l: '−20' }, { v: -10, l: '−10' }, { v: 0, l: '0' }, { v: 10, l: '10' }], xAxisAt: 'bottom' });
      A.line(ax.X(0), ax.Y(th), ax.X(1), ax.Y(th), 's-soft w1 dash');
      var cu = A.path('', 's-bad w1'), ci = A.path('', 's-good w2');
      var s1 = sm(A.text(186, 230, '', { cls: 'f-good' })), s2 = sm(A.text(186, 246, '', { cls: 'f-bad' }));
      A.note('低于 −10 dB 的理论概率：知道 CSI P(|h₁|²+|h₂|² &lt; 0.1) = 1 − e<sup>−0.1</sup>(1 + 0.1) = ' + (100 * (1 - Math.exp(-0.1) * 1.1)).toFixed(2) + '%；不知道 P(|h|² &lt; 0.1) = 1 − e<sup>−0.1</sup> = ' + (100 * (1 - Math.exp(-0.1))).toFixed(1) + '%');
      A.choice({ options: ['发端知道 CSI', '发端不知道 CSI'], value: 0, on: function (v) { mode = v; A.redraw(); } });
      return function frame(t) {
        var N = 160, pu = [], pi = [], nu = 0, ni = 0, a, b;
        for (var i = 0; i <= N; i++) {
          var x = i / N, tt = t * 0.15 + x;
          a = h1(tt); b = h2(tt);
          var su = abs2(cadd(a, b)) / 2, si = abs2(a) + abs2(b);
          pu.push([ax.X(x), ax.Y(A.clamp(dB(su), -25, 10))]); pi.push([ax.X(x), ax.Y(A.clamp(dB(si), -25, 10))]);
          if (dB(su) < th) nu++; if (dB(si) < th) ni++;
        }
        A.set(cu, { d: A.pts(pu), cls: mode === 1 ? 's-bad w3' : 's-bad w1' }); A.set(ci, { d: A.pts(pi), cls: mode === 0 ? 's-good w3' : 's-good w1' });
        A.setText(s1, '知道 CSI ‖h‖²：这一段低于 −10 dB ' + Math.round(100 * ni / (N + 1)) + '%');
        A.setText(s2, '不知道 |h₁+h₂|²/2：低于 −10 dB ' + Math.round(100 * nu / (N + 1)) + '%');
        var nh = Math.sqrt(abs2(a) + abs2(b)), c1, c2;
        if (mode === 0) { c1 = [abs2(a) / nh, 0]; c2 = [abs2(b) / nh, 0]; }
        else { c1 = [a[0] / Math.SQRT2, a[1] / Math.SQRT2]; c2 = [b[0] / Math.SQRT2, b[1] / Math.SQRT2]; }
        function P(z) { return [ox + A.clamp(z[0], -2.2, 2.6) * k, oy - A.clamp(z[1], -2.4, 2.4) * k]; }
        var o = P([0, 0]), e1 = P(c1), e2 = P(cadd(c1, c2));
        var dy = mode === 0 ? -6 : 0;
        A.moveArrow(ar1, o[0], o[1] + dy, e1[0], e1[1] + dy); A.moveArrow(ar2, e1[0], e1[1] + dy, e2[0], e2[1] + dy);
        A.moveArrow(res, o[0], o[1] + (mode === 0 ? 6 : 0), e2[0], e2[1] + (mode === 0 ? 6 : 0));
        A.set(res, { cls: 'an-arrow ' + (mode === 0 ? 's-good w3' : 's-bad w3') });
        A.setText(ttl, mode === 0 ? '同相相加（波束成形）' : '随机相加，时长时短');
        A.setText(sub, mode === 0 ? 'w = h/‖h‖' : 'w = [1, 1]/√2');
        A.setText(val, '|wᴴh|² = ' + abs2(cadd(c1, c2)).toFixed(2));
      };
    }
  });

  /* ================= 5.4 Alamouti ================= */
  ANIM.reg('p2:5.4', {
    title: 'Alamouti：两个时隙、两根天线',
    cap: '编码矩阵 X 的行 = 时隙，列 = 天线。接收端只有 1 根天线，两个时隙信道 h₁、h₂ 不变。把 y₂ 取共轭后线性合并，交叉项抵消，每个符号都拿到 |h₁|² + |h₂|² 的增益：2 阶分集，而发端不需要知道信道。',
    h: 268,
    steps: [
      '时隙 1：天线 1 发 s₁，天线 2 发 s₂（X 的第 1 行）。',
      '时隙 2：天线 1 发 −s₂*，天线 2 发 s₁*：对调 + 共轭 + 负号，三者缺一不可。',
      '一根接收天线收两次，h₁、h₂ 两个时隙不变：写出 y₁、y₂。',
      '把 y₂ 取共轭：s₁、s₂ 都以不带共轭的形式出现，可以线性合并。',
      'z₁ = h₁*y₁ + h₂y₂*：s₂ 的两项 h₁*h₂s₂ − h₂h₁*s₂ 抵消，只剩 ‖h‖²s₁。',
      'z₂ = h₂*y₁ − h₁y₂* 同理。每个符号增益 |h₁|²+|h₂|²：2 阶分集。'
    ],
    tween: 1.4,
    init: function (A) {
      var T1 = [12, 26], T2 = [12, 86], R = [142, 56];
      A.rect(T1[0], T1[1], 40, 22, 'f-card s-ink w1', null, 4); A.text(32, T1[1] + 15, 'Tx1', { anchor: 'middle', cls: 't-b' });
      A.rect(T2[0], T2[1], 40, 22, 'f-card s-ink w1', null, 4); A.text(32, T2[1] + 15, 'Tx2', { anchor: 'middle', cls: 't-b' });
      A.rect(R[0], R[1], 36, 22, 'f-card s-ink w1', null, 4); A.text(160, R[1] + 15, 'Rx', { anchor: 'middle', cls: 't-b' });
      A.line(52, 37, 142, 67, 's-acc w2'); A.line(52, 97, 142, 67, 's-gold w2');
      A.text(122, 50, 'h₁', { cls: 'f-acc t-b', anchor: 'middle' }); A.text(122, 92, 'h₂', { cls: 'f-gold t-b', anchor: 'middle' });
      var slot = A.text(96, 18, '', { cls: 't-b', anchor: 'middle' });
      var m1 = A.text(0, 0, '', { cls: 't-b t-m f-acc', anchor: 'middle' }), m2 = A.text(0, 0, '', { cls: 't-b t-m f-gold', anchor: 'middle' });
      /* matrix */
      A.text(204, 22, 'X(s) =', { cls: 't-b' });
      A.text(290, 38, '天线 1', { cls: 't-s', anchor: 'middle' }); A.text(350, 38, '天线 2', { cls: 't-s', anchor: 'middle' });
      A.text(214, 64, '时隙 1', { cls: 't-s' }); A.text(214, 96, '时隙 2', { cls: 't-s' });
      var rowR = [A.rect(258, 45, 122, 28, 'f-none s-none', null, 5), A.rect(258, 77, 122, 28, 'f-none s-none', null, 5)];
      var cellT = [['s₁', 's₂'], ['−s₂*', 's₁*']], cells = [];
      cellT.forEach(function (r, i) { r.forEach(function (s, j) { cells.push(A.text(290 + j * 60, 65 + i * 32, s, { cls: 't-l t-m t-b', anchor: 'middle' })); }); });
      var orth = A.text(318, 124, 'XXᴴ = (|s₁|² + |s₂|²) I', { cls: 't-s', anchor: 'middle' });
      var EQ = [['y₁ = h₁s₁ + h₂s₂ + w₁', ''], ['y₂ = −h₁s₂* + h₂s₁* + w₂', ''], ['y₂* = h₂*s₁ − h₁*s₂ + w₂*', 'f-pur'], ['z₁ = h₁*y₁ + h₂y₂* = (|h₁|²+|h₂|²)s₁ + 噪声', 'f-good'], ['z₂ = h₂*y₁ − h₁y₂* = (|h₁|²+|h₂|²)s₂ + 噪声', 'f-good']];
      var eqs = EQ.map(function (e, i) { return A.text(14, 156 + i * 24, e[0], { cls: 't-m ' + e[1] }); });
      var showAt = [2, 2, 3, 4, 5];
      /* numeric check */
      var h1 = cx(0.8, 30 * DEG), h2 = cx(0.5, -100 * DEG), s1 = [1, 1], s2 = [-1, 1];
      var y1 = cadd(cmul(h1, s1), cmul(h2, s2)), y2 = cadd(cmul([-h1[0], -h1[1]], conj(s2)), cmul(h2, conj(s1)));
      var z1 = cadd(cmul(conj(h1), y1), cmul(h2, conj(y2))), z2 = csub(cmul(conj(h2), y1), cmul(h1, conj(y2)));
      var nh = abs2(h1) + abs2(h2);
      return {
        step: function (k) {
          if (k >= 4) A.note('数值例（无噪声）：h₁ = 0.8∠30°，h₂ = 0.5∠−100°，s₁ = 1+j，s₂ = −1+j，‖h‖² = ' + nh.toFixed(2) + '<br>z₁ = ' + cstr(z1) + ' → z₁/‖h‖² = ' + cstr([z1[0] / nh, z1[1] / nh]) + (k >= 5 ? '；z₂ = ' + cstr(z2) + ' → z₂/‖h‖² = ' + cstr([z2[0] / nh, z2[1] / nh]) : ''));
          else A.note('');
        },
        frame: function (ts, dt, k) {
          var p = A.prog(ts, 1.2), sl = k === 0 ? 0 : 1, fly = k <= 1;
          A.setText(slot, k <= 1 ? '时隙 ' + (k + 1) : '两个时隙都收完');
          show(m1, fly); show(m2, fly);
          if (fly) {
            var f = 0.12 + 0.5 * p;
            A.set(m1, { x: A.lerp(52, 142, f), y: A.lerp(37, 67, f) - 8, text: cellT[sl][0] });
            A.set(m2, { x: A.lerp(52, 142, f), y: A.lerp(97, 67, f) + 18, text: cellT[sl][1] });
          }
          rowR.forEach(function (r, i) { A.set(r, { cls: k <= 1 && i === k ? 'f-accs s-acc w1' : 'f-none s-none' }); });
          cells.forEach(function (c, i) { op(c, i < 2 || k >= 1 ? (i >= 2 && k === 1 ? p : 1) : 0.15); });
          op(orth, k >= 1 ? (k === 1 ? p : 1) : 0);
          eqs.forEach(function (e, i) { op(e, k > showAt[i] ? 1 : k === showAt[i] ? p : 0); });
        }
      };
    }
  });

  /* ================= 5.5 MIMO capacity: min(N, M) pipes ================= */
  ANIM.reg('p2:5.5', {
    title: 'MIMO 容量：几根天线 = 几条并行管道',
    cap: '取理想信道 H = I（各子信道增益相同）、发端不知道信道（每根天线 P/N），C/B = Σ log₂(1 + λ<sub>i</sub>/σ²) = N·log₂(1 + SNR/N)。高 SNR 时每 +3 dB，N × N 多 N bit/s/Hz（斜率 = min(N, M)）。1 × 4 SIMO（|h<sub>i</sub>| = 1）只有 1 条管道：log₂(1 + 4SNR)，曲线只是平移，斜率不变。',
    h: 252,
    init: function (A) {
      var snr = 20;
      var cfg = [
        { n: '1×1', r: 1, cls: 'acc', C: function (s) { return Math.log2(1 + s); } },
        { n: '1×4 SIMO', r: 1, cls: 'pur', C: function (s) { return Math.log2(1 + 4 * s); }, dash: true },
        { n: '2×2', r: 2, cls: 'gold', C: function (s) { return 2 * Math.log2(1 + s / 2); } },
        { n: '4×4', r: 4, cls: 'good', C: function (s) { return 4 * Math.log2(1 + s / 4); } }
      ];
      var ax = A.axes({ x: 40, y: 20, w: 214, h: 190, xr: [0, 30], yr: [0, 35], yl: 'C/B（bit/s/Hz）', ticksX: [0, 10, 20, 30], ticksY: [0, 10, 20, 30], grid: true, xAxisAt: 'bottom' });
      A.text(147, 244, 'SNR = P/σ²（dB）', { cls: 't-s', anchor: 'middle' });
      var vl = A.line(0, ax.y, 0, ax.y + ax.h, 's-soft w1 dash');
      var dots = cfg.map(function (c, i) {
        A.curve(ax, function (x) { return c.C(A.undb(x)); }, 's-' + c.cls + ' w' + (c.dash ? '2 dash' : '3'), null, 120);
        A.line(50, 34 + i * 15, 66, 34 + i * 15, 's-' + c.cls + ' w3' + (c.dash ? ' dash' : ''));
        A.text(70, 38 + i * 15, c.n, { cls: 't-s' });
        return A.circle(0, 0, 4, 'f-' + c.cls + ' s-card w1');
      });
      /* pipes */
      var px = 272, pw = 9;
      A.text(px, 22, '并行管道（每条的容量）', { cls: 't-s' });
      var groups = [], y = 40;
      [0, 2, 3].forEach(function (ci) {
        var c = cfg[ci], g = { c: c, pipes: [], tot: null };
        A.text(px, y + 10, c.n, { cls: 't-b' });
        g.tot = A.text(394, y + 10, '', { cls: 't-s t-m', anchor: 'end' });
        y += 16;
        for (var j = 0; j < c.r; j++) { g.pipes.push(A.rect(px, y, 10, pw, 'f-' + c.cls + ' s-none', null, 4)); y += pw + 4; }
        y += 10;
        groups.push(g);
      });
      function draw() {
        var s = A.undb(snr);
        A.set(vl, { x1: ax.X(snr), x2: ax.X(snr) });
        cfg.forEach(function (c, i) { A.set(dots[i], { cx: ax.X(snr), cy: ax.Y(c.C(s)) }); });
        groups.forEach(function (g) {
          var per = g.c.C(s) / g.c.r;
          g.pipes.forEach(function (p) { A.set(p, { width: Math.max(2, per * 11) }); });
          A.setText(g.tot, g.c.r + ' × ' + per.toFixed(2) + ' = ' + g.c.C(s).toFixed(1));
        });
        A.note('SNR = ' + snr + ' dB：' + cfg.map(function (c) { return c.n + ' ' + c.C(s).toFixed(2); }).join('，') + '<br>SNR 再 +3 dB（×2）：' + cfg.map(function (c) { return c.n + ' +' + (c.C(2 * s) - c.C(s)).toFixed(2); }).join('，'));
      }
      A.slider({ label: 'SNR', min: 0, max: 30, step: 1, value: snr, unit: 'dB', on: function (v) { snr = v; draw(); } });
      draw();
      return {};
    }
  });
})();
