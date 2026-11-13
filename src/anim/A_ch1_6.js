/* EE6129 Part A (partA.html), chapters 1–6: multiple access, cellular idea, 1G→4G, duplex & spectral
   efficiency, path loss, cluster & reuse distance.  One figure per section, ids 'A:x.y'. */
(function () {
  'use strict';
  var S3 = Math.sqrt(3);
  var UC = ['acc', 'gold', 'good', 'pur'];
  /* 13 fills for frequency groups (group 0 = the highlighted co-channel set) */
  var PAL = ['f-acc op7', 'f-golds', 'f-goods', 'f-purs', 'f-bads', 'f-accs', 'f-line', 'f-gold op3', 'f-good op3', 'f-pur op3', 'f-bad op3', 'f-faint op5', 'f-soft op3'];
  function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
  function op(el, v) { el.setAttribute('opacity', (+clamp(v, 0, 1)).toFixed(2)); }
  function f1(x) { return (+x).toFixed(1); }
  /* pointy-top hexagon, vertices at 30°, 90°, … (y axis points down on screen) */
  function hexPts(cx, cy, R) { var p = []; for (var k = 0; k < 6; k++) { var a = Math.PI / 180 * (30 + 60 * k); p.push([cx + R * Math.cos(a), cy - R * Math.sin(a)]); } return p; }
  function hexD(cx, cy, R) { return 'M' + hexPts(cx, cy, R).map(function (p) { return f1(p[0]) + ' ' + f1(p[1]); }).join('L') + 'Z'; }
  /* hex lattice: e1 = √3R at 0°, e2 = √3R at 60°  → neighbour cells share an edge */
  function latXY(a, b, R, cx, cy) { return [cx + S3 * R * (a + b / 2), cy - 1.5 * R * b]; }
  var DIRS = [[1, 0], [0, 1], [-1, 1], [-1, 0], [0, -1], [1, -1]];   // directions 0°, 60°, …, 300°
  function hexDist(a, b) { return Math.max(Math.abs(a), Math.abs(b), Math.abs(a + b)); }
  /* all cells with centre distance ≤ rmax (in units of R), sorted by distance, then angle */
  function cellsWithin(rmax) {
    var out = [];
    for (var a = -14; a <= 14; a++) for (var b = -14; b <= 14; b++) {
      var d = S3 * Math.sqrt(a * a + a * b + b * b);
      if (d > rmax + 1e-9) continue;
      var ang = Math.atan2(b * S3 / 2, a + b / 2); if (ang < -1e-9) ang += 2 * Math.PI;
      out.push({ a: a, b: b, d: d, ang: ang });
    }
    out.sort(function (p, q) { return Math.abs(p.d - q.d) > 1e-6 ? p.d - q.d : p.ang - q.ang; });
    return out;
  }
  /* frequency-group labeller for cluster (i, j): two cells share a group iff their difference lies in the
     co-channel sublattice spanned by (i, j) and its 60° rotation (−j, i+j). Labels follow call order. */
  function labeler(i, j) {
    var N = i * i + i * j + j * j, reps = [];
    return function (a, b) {
      for (var k = 0; k < reps.length; k++) {
        var da = a - reps[k][0], db = b - reps[k][1];
        if (((i + j) * da + j * db) % N === 0 && (i * db - j * da) % N === 0) return k;
      }
      reps.push([a, b]); return reps.length - 1;
    };
  }
  function tower(A, x, y, c, p) {
    var g = A.g({}, p);
    A.path('M' + (x - 6) + ' ' + (y + 16) + 'L' + x + ' ' + y + 'L' + (x + 6) + ' ' + (y + 16) + 'M' + (x - 3.4) + ' ' + (y + 8) + 'L' + (x + 3.4) + ' ' + (y + 8), 's-' + c + ' w2', g);
    A.path('M' + (x - 6) + ' ' + (y - 5) + 'A8 8 0 0 1 ' + (x - 6) + ' ' + (y + 5) + 'M' + (x + 6) + ' ' + (y - 5) + 'A8 8 0 0 0 ' + (x + 6) + ' ' + (y + 5), 's-' + c + ' w1', g);
    A.circle(x, y, 2.2, 'f-' + c, g);
    return g;
  }
  function phone(A, x, y, c, p) {
    var g = A.g({}, p);
    A.rect(x - 4.5, y - 7.5, 9, 15, 'f-card s-' + c + ' w2', g, 2);
    A.line(x - 2, y + 4.5, x + 2, y + 4.5, 's-' + c + ' w1', g);
    return g;
  }
  function along(pts, s) {
    var L = [0], i;
    for (i = 1; i < pts.length; i++) L.push(L[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    var d = clamp(s, 0, 1) * L[L.length - 1];
    for (i = 1; i < pts.length; i++) if (d <= L[i] || i === pts.length - 1) {
      var u = (d - L[i - 1]) / ((L[i] - L[i - 1]) || 1);
      return [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * u, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * u];
    }
    return pts[0];
  }
  function sg(v) { return v > 0 ? '+' + v : v < 0 ? '−' + (-v) : '0'; }
  function sumStr(arr) { return arr.map(function (v, i) { return i === 0 ? (v < 0 ? '−' + (-v) : String(v)) : (v < 0 ? '−' : '+') + Math.abs(v); }).join(''); }
  /* 1G→4G timeline strip used by 3.1–3.4 */
  function timeline(A, k) {
    var sub = ['模拟 · FDMA', 'TDMA / CDMA', 'WCDMA · 数据', 'OFDMA · 全 IP'];
    for (var i = 0; i < 4; i++) {
      var x = 4 + 99 * i, on = i === k;
      A.rect(x, 4, 94, 36, on ? 'f-acc s-acc w1' : 'f-card s-line w1', null, 6);
      A.text(x + 47, 19, (i + 1) + 'G', { cls: 't-b' + (on ? ' f-card' : ''), anchor: 'middle' });
      A.text(x + 47, 34, sub[i], { cls: on ? 'f-card' : 'f-soft', size: 10.5, anchor: 'middle' });
    }
  }

  /* ================= 1.1 FDMA ================= */
  ANIM.reg('A:1.1', {
    title: 'FDMA：频带切成车道，各占一条',
    cap: '横轴时间、纵轴频率。每个用户分到一条窄频带，<b>一直</b>占着；4 条都被占满后，第 5 个用户只能等——车道数是固定的。',
    h: 206,
    init: function (A) {
      var x0 = 52, x1 = 300, W = x1 - x0, y0 = 24, bh = 34, nB = 4, ya = y0 + nB * bh + 4;
      A.arrow(x0 - 4, ya, x1 + 14, ya, 's-soft w1', null, 5);
      A.arrow(x0 - 4, ya, x0 - 4, y0 - 12, 's-soft w1', null, 5);
      A.text(x1 + 14, ya + 14, '时间 t', { cls: 't-s', anchor: 'end' });
      A.text(x0 + 2, y0 - 6, '频率 f', { cls: 't-s' });
      var fills = [], waves = [], mids = [];
      for (var k = 0; k < nB; k++) {
        var y = y0 + (nB - 1 - k) * bh, c = UC[k];
        A.rect(x0, y + 2, W, bh - 4, 'f-none s-line w1 dash', null, 3);
        fills.push(A.rect(x0, y + 2, 0, bh - 4, 'f-' + c + 's s-none', null, 3));
        waves.push(A.path('', 's-' + c + ' w1'));
        mids.push(y + bh / 2);
        A.text(x0 - 9, y + bh / 2 + 4, 'f_{' + (k + 1) + '}', { cls: 't-s', anchor: 'end' });
        A.circle(x1 + 18, y + bh / 2, 4, 'f-' + c);
        A.text(x1 + 26, y + bh / 2 + 4, '用户 ' + (k + 1));
      }
      var cur = A.line(x0, y0 - 4, x0, ya, 's-ink w1');
      var msg = A.text(200, 196, '用户 5 来了：4 条频带全被占 → 阻塞，只能等', { cls: 'f-bad t-b', anchor: 'middle' });
      return function (t) {
        var u = Math.min(1, (t % 8) / 6), cx = x0 + W * u;
        for (var k = 0; k < nB; k++) {
          A.set(fills[k], { width: cx - x0 });
          var d = '', lam = 12 + 4 * k;
          for (var x = x0; x <= cx; x += 2.5) d += (d ? 'L' : 'M') + f1(x) + ' ' + f1(mids[k] + 8 * Math.sin(2 * Math.PI * (x - x0) / lam));
          waves[k].setAttribute('d', d);
        }
        A.set(cur, { x1: cx, x2: cx });
        op(msg, (u - 0.45) * 4);
      };
    }
  });

  /* ================= 1.2 TDMA ================= */
  ANIM.reg('A:1.2', {
    title: 'TDMA：同一频率，轮流发言',
    cap: '所有人共用同一个频率。时间切成<b>帧（frame）</b>，每帧再切成时隙（time slot），每人只在自己的时隙里发，其余时间静默。轮换很快，听起来像连续通话。',
    h: 206,
    init: function (A) {
      var x0 = 52, nS = 4, nF = 3, sw = 18, W = sw * nS * nF, x1 = x0 + W, yb = 52, bh = 92, ya = yb + bh + 10;
      A.arrow(x0 - 4, ya, x1 + 14, ya, 's-soft w1', null, 5);
      A.text(x1 + 14, ya + 14, '时间 t', { cls: 't-s', anchor: 'end' });
      A.text(x0 - 6, yb + bh / 2 + 4, 'f_{0}', { cls: 't-s', anchor: 'end' });
      A.text(x0, yb + bh + 30, '只有一个频率 f₀，按时间轮流用', { cls: 't-s' });
      var slots = [];
      for (var f = 0; f < nF; f++) {
        var fx = x0 + f * nS * sw;
        A.path('M' + (fx + 1) + ' 40V36H' + (fx + nS * sw - 1) + 'V40', 's-soft w1');
        A.text(fx + nS * sw / 2, 30, '帧 ' + (f + 1), { cls: 't-s', anchor: 'middle' });
        for (var s = 0; s < nS; s++) {
          var sx = fx + s * sw, c = UC[s];
          A.rect(sx + 1, yb, sw - 2, bh, 'f-none s-line w1 dash', null, 2);
          var r = A.rect(sx + 1, yb, 0, bh, 'f-' + c + 's s-' + c + ' w1', null, 2);
          var tx = A.text(sx + sw / 2, yb + bh / 2 + 4, String(s + 1), { cls: 't-b f-' + c, anchor: 'middle' });
          slots.push({ x: sx, r: r, t: tx, u: s });
        }
      }
      var cur = A.line(x0, 26, x0, ya, 's-ink w1');
      var dots = [], st = [];
      for (var k = 0; k < nS; k++) {
        dots.push(A.circle(x1 + 22, yb + 12 + 23 * k, 4.5, 'f-' + UC[k]));
        st.push(A.text(x1 + 32, yb + 16 + 23 * k, '', {}));
      }
      return function (t) {
        var u = Math.min(1, (t % 9) / 7.5), cx = x0 + W * u, act = -1;
        slots.forEach(function (s) {
          var w = clamp(cx - s.x - 1, 0, sw - 2);
          A.set(s.r, { width: w }); op(s.t, w > sw / 2 ? 1 : 0);
          if (cx > s.x && cx <= s.x + sw && u < 1) act = s.u;
        });
        A.set(cur, { x1: cx, x2: cx });
        for (var k = 0; k < nS; k++) {
          A.set(dots[k], { r: k === act ? 6.5 : 4 }); op(dots[k], k === act ? 1 : 0.35);
          A.setText(st[k], '用户 ' + (k + 1) + (k === act ? '：发送中' : '：静默')); A.set(st[k], { cls: k === act ? 't-b' : 'f-soft' });
        }
      };
    }
  });

  /* ================= 1.3 CDMA ================= */
  (function () {
    var cA = [1, -1, 1, -1], cB = [1, 1, -1, -1], bA = 1, bB = -1;
    function mul(a, b) { return a.map(function (v, i) { return v * b[i]; }); }
    function sc(a, s) { return a.map(function (v) { return v * s; }); }
    function sum(a) { return a.reduce(function (p, v) { return p + v; }, 0); }
    var sA = sc(cA, bA), sB = sc(cB, bB), r = sA.map(function (v, i) { return v + sB[i]; });
    var L = cA.length, rA = mul(r, cA), xB = mul(sB, cA), rB = mul(r, cB);
    function seq(a) { return '(' + a.map(sg).join(', ') + ')'; }
    ANIM.reg('A:1.3', {
      title: 'CDMA：同频同时，靠码区分',
      cap: '两位用户<b>同时</b>占满整段频带。码 c<sub>A</sub>、c<sub>B</sub> 正交（逐片相乘再求和 = 0）。接收机拿自己的码做相关：自己的比特被放大成 ±4，别人的被压成 0。',
      h: 266, tween: 1.2, stepDur: 4.2,
      steps: [
        'A、B 同时用整段频带。各有一串 ±1 码片：c<sub>A</sub>·c<sub>B</sub> = ' + sumStr(mul(cA, cB)) + ' = ' + sum(mul(cA, cB)) + '，两个码正交。',
        '扩频：A 发比特 ' + sg(bA) + ' → 送出 ' + sg(bA) + '·c<sub>A</sub>；B 发比特 ' + sg(bB) + ' → 送出 ' + sg(bB) + '·c<sub>B</sub>。',
        '空中两路直接相加，接收机收到的是混合信号 r = ' + seq(r) + '。',
        '接收机 A：r 逐片乘 c<sub>A</sub> 再求和 = ' + sum(rA) + '，除以 ' + L + ' → ' + sg(sum(rA) / L) + '，正是 A 的比特。',
        '为什么 B 不干扰 A？B 那部分乘 c<sub>A</sub> 求和 = ' + sum(xB) + '，被压成零。',
        '接收机 B 换用 c<sub>B</sub>：求和 = ' + sum(rB) + '，除以 ' + L + ' → ' + sg(sum(rB) / L) + '，B 的比特也恢复了。'
      ],
      init: function (A) {
        var cx0 = 112, cw = 44, u = 10;
        function row(y, lab, c) {
          var g = A.g();
          A.line(cx0, y, cx0 + L * cw, y, 's-line w1', g);
          var o = { g: g, y: y, bars: [], lab: A.text(6, y + 4, lab, {}, g), val: A.text(296, y + 4, '', { cls: 't-m' }, g) };
          for (var i = 0; i < L; i++) { A.line(cx0 + i * cw, y - 3, cx0 + i * cw, y + 3, 's-line w1', g); o.bars.push(A.rect(cx0 + i * cw + 4, y, cw - 8, 0, 'f-' + c, g, 1)); }
          return o;
        }
        function setRow(o, v, p, c) {
          for (var i = 0; i < L; i++) {
            var hgt = Math.abs(v[i]) * u * p;
            A.set(o.bars[i], { y: v[i] >= 0 ? o.y - hgt : o.y, height: hgt, cls: 'f-' + c });
          }
          A.setText(o.val, v.map(sg).join(' '));
        }
        A.line(cx0 + L * cw, 14, cx0 + L * cw, 240, 's-line w1 dot');
        var rows = [row(26, '码 c_{A}', 'acc'), row(58, '码 c_{B}', 'gold'), row(94, 'A 发 ' + sg(bA) + '·c_{A}', 'acc'),
          row(126, 'B 发 ' + sg(bB) + '·c_{B}', 'gold'), row(166, '空中叠加 r', 'soft'), row(216, '', 'acc')];
        var data = [cA, cB, sA, sB, r], cols = ['acc', 'gold', 'acc', 'gold', 'soft'];
        var r5 = [{ l: 'r × c_{A}', v: rA, c: 'acc' }, { l: 'B 部分 × c_{A}', v: xB, c: 'gold' }, { l: 'r × c_{B}', v: rB, c: 'gold' }];
        var bottom = A.text(200, 258, '', { cls: 't-b', anchor: 'middle' });
        var msgs = ['c_{A}·c_{B} = ' + sumStr(mul(cA, cB)) + ' = ' + sum(mul(cA, cB)) + ' → 正交',
          '每个比特 × 码 → 变成 ' + L + ' 个码片（扩频）', 'r = A 的 + B 的 = ' + seq(r),
          'Σ = ' + sumStr(rA) + ' = ' + sum(rA) + '，÷' + L + ' = ' + sg(sum(rA) / L) + ' → A 的比特 ✓',
          'Σ = ' + sumStr(xB) + ' = ' + sum(xB) + ' → B 对 A 的干扰没了',
          'Σ = ' + sumStr(rB) + ' = ' + sum(rB) + '，÷' + L + ' = ' + sg(sum(rB) / L) + ' → B 的比特 ✓'];
        var K = 0;
        return {
          step: function (k) { K = k; A.setText(bottom, msgs[k]); A.set(bottom, { cls: 't-b ' + (k === 4 ? 'f-gold' : k >= 3 ? 'f-good' : '') }); },
          frame: function (ts) {
            var p = A.prog(ts, 0.8);
            for (var i = 0; i < 5; i++) {
              var vis = i < 2 ? 1 : i < 4 ? (K >= 1 ? 1 : 0) : (K >= 2 ? 1 : 0);
              var grow = (i >= 2 && i < 4 && K === 1) || (i === 4 && K === 2) ? p : 1;
              op(rows[i].g, vis); setRow(rows[i], data[i], grow, cols[i]);
            }
            var q = r5[Math.max(0, K - 3)];
            op(rows[5].g, K >= 3 ? 1 : 0); A.setText(rows[5].lab, q.l); setRow(rows[5], q.v, K >= 3 ? p : 0, q.c);
            op(bottom, A.prog(ts, 0.6, 0.3));
          }
        };
      }
    });
  })();

  /* ================= 2.1 why small cells ================= */
  (function () {
    var S = 70, N = 7, cells = cellsWithin(3 * S3 + 1e-6).filter(function (c) { return hexDist(c.a, c.b) <= 3; });
    var nC = cells.length, per = S / N, cap = nC * per;
    ANIM.reg('A:2.1', {
      title: '一个大塔 vs 很多小蜂窝',
      cap: '信道总数一样多，但小蜂窝功率低、传不远，隔得够远的小区可以<b>重复使用</b>同一组信道，所以全区同时能打的电话多得多（数字为示意，设 S = ' + S + '）。',
      h: 240, tween: 1.2, stepDur: 4,
      steps: [
        '老办法：一个高功率大塔覆盖全区。设共 ' + S + ' 个信道，全区同时最多 ' + S + ' 通电话。',
        '换成 ' + nC + ' 个低功率小基站，每个只覆盖一小块（一个 cell）。',
        S + ' 个信道分成 ' + N + ' 组，每区 ' + per + ' 个；隔得够远的小区重复用同一组 = 频率复用。',
        '同时通话：' + nC + ' × ' + per + ' = ' + cap + '，是大塔的 ' + (cap / S).toFixed(1) + ' 倍。小区越多越小，容量越大。',
        '这就是蜂窝系统的起点：低功率小区 → 频率复用 → 切换/集中控制 → 小区分裂。'
      ],
      init: function (A) {
        var R = 13, cx = 112, cy = 128, lab = labeler(2, 1);
        var big = A.circle(cx, cy, 92, 'f-golds s-gold w1');
        var gMap = A.g(), hexes = [], nums = [];
        cells.forEach(function (c) {
          var p = latXY(c.a, c.b, R, cx, cy); c.gr = lab(c.a, c.b);
          hexes.push(A.path(hexD(p[0], p[1], R), 'f-paper s-soft w1', gMap));
          A.circle(p[0], p[1] + 5, 1.6, 'f-ink', gMap);
          nums.push(A.text(p[0], p[1] + 1, String(c.gr + 1), { cls: c.gr === 0 ? 'f-card t-b' : '', size: 10.5, anchor: 'middle' }, gMap));
        });
        var bigT = tower(A, cx, cy - 10, 'gold');
        var px = 226, panels = [];
        function P(lines) { var g = A.g(); lines.forEach(function (l) { A.text(px, l[0], l[1], l[2] || {}, g); }); panels.push(g); return g; }
        P([[66, '设共有 S = ' + S + ' 个信道', { cls: 't-b' }], [92, '一个大塔覆盖全区：'], [110, '每个信道全区只能用一次'], [140, '同时通话 ≤ ' + S, { cls: 't-l t-b f-gold' }]]);
        P([[66, '换成 ' + nC + ' 个低功率小基站', { cls: 't-b' }], [92, '每个只覆盖一小块'], [116, '功率低 → 信号传不远'], [134, '→ 远处可以再用同一频率']]);
        P([[66, '分 N = ' + N + ' 组', { cls: 't-b' }], [88, '每组 ' + S + ' ÷ ' + N + ' = ' + per + ' 个信道'], [112, '数字相同 = 同一组信道'], [130, '同组小区隔得够远'], [148, '→ 互不干扰（频率复用）']]);
        var g3 = P([[62, '同时通话数', { cls: 't-b' }], [86, '大塔', { cls: 't-s' }], [128, '小蜂窝 ' + nC + ' × ' + per, { cls: 't-s' }], [180, '≈ ' + (cap / S).toFixed(1) + ' 倍', { cls: 't-l t-b f-good' }]]);
        var sc = 120 / cap, b1 = A.rect(px, 92, 0, 14, 'f-gold', g3, 2), b2 = A.rect(px, 134, 0, 14, 'f-good', g3, 2);
        var v1 = A.text(px, 103, String(S), { cls: 't-m' }, g3), v2 = A.text(px, 145, String(cap), { cls: 't-m' }, g3);
        P([[58, '蜂窝系统四要素', { cls: 't-b' }], [82, '① 低功率 + 小覆盖（本章）'], [104, '② 频率复用（6、7 章）'], [126, '③ 切换 + 集中控制（10 章）'], [148, '④ 小区分裂扩容（9 章）']]);
        var K = 0;
        return {
          step: function (k) {
            K = k;
            hexes.forEach(function (h, i) { A.set(h, { cls: (k >= 2 ? PAL[cells[i].gr] : 'f-paper') + ' s-soft w1' }); });
          },
          frame: function (ts) {
            var p = A.prog(ts, 0.9);
            op(big, K === 0 ? 1 : K === 1 ? 1 - p : 0); op(bigT, K === 0 ? 1 : K === 1 ? 1 - p : 0);
            op(gMap, K === 0 ? 0 : K === 1 ? p : 1);
            nums.forEach(function (n) { op(n, K >= 2 ? (K === 2 ? p : 1) : 0); });
            panels.forEach(function (g, i) { op(g, i === K ? p : 0); });
            var q = K === 3 ? p : 1;
            A.set(b1, { width: S * sc * q }); A.set(b2, { width: cap * sc * q });
            A.set(v1, { x: px + S * sc * q + 5 }); A.set(v2, { x: px + cap * sc * q + 5 });
          }
        };
      }
    });
  })();

  /* ================= 2.2 why hexagons ================= */
  (function () {
    var shapes = [{ n: 3, l: '三角形' }, { n: 4, l: '正方形' }, { n: 6, l: '六边形' }];
    shapes.forEach(function (s) { s.f = s.n / 2 * Math.sin(2 * Math.PI / s.n) / Math.PI; });   // inscribed polygon area / circle area
    ANIM.reg('A:2.2', {
      title: '为什么画成六边形',
      cap: '六边形能<b>不留空隙、不重叠</b>地铺满平面，又是能这样铺的形状里最接近圆的。R = 中心到顶点，相邻小区中心距 d = √3·R。',
      h: 236, tween: 1.2, stepDur: 4,
      steps: [
        '单个基站天线的覆盖，理论上接近一个圆。',
        '拿圆去铺：圆和圆相切时，中间留下空隙（红色）= 盲区。',
        '把圆挤近消灭空隙，又会互相重叠（颜色更深处）= 浪费。',
        '三角形、正方形能铺满，但离圆太远：同一个圆里只盖住 ' + Math.round(shapes[0].f * 100) + '%、' + Math.round(shapes[1].f * 100) + '%。',
        '六边形：铺满平面、无空隙无重叠，每个邻居共享一条完整的边，盖住圆的 ' + Math.round(shapes[2].f * 100) + '%。',
        'R = 中心到顶点；相邻两个中心相距 d = √3·R ≈ ' + S3.toFixed(2) + 'R（后面算复用距离要用）。'
      ],
      init: function (A) {
        var G = [];
        var g0 = A.g(); A.circle(200, 112, 56, 'f-accs s-acc w2', g0); tower(A, 200, 102, 'ink', g0);
        A.text(200, 200, '天线覆盖 ≈ 圆', { cls: 't-b', anchor: 'middle' }, g0); G.push(g0);
        var g1 = A.g(); A.rect(95, 79, 204, 68, 'f-bad op5 s-none', g1, 0);
        for (var r = 0; r < 2; r++) for (var c = 0; c < 4; c++) { A.circle(95 + 68 * c, 79 + 68 * r, 34, 'f-paper s-none', g1); A.circle(95 + 68 * c, 79 + 68 * r, 34, 'f-accs s-acc w1', g1); }
        A.text(200, 212, '红色空隙 = 盲区（没有信号）', { cls: 't-b f-bad', anchor: 'middle' }, g1); G.push(g1);
        var g2 = A.g(), dx = S3 * 34;
        for (var c2 = 0; c2 < 4; c2++) { A.circle(88 + dx * c2, 84, 34, 'f-acc op3 s-acc w1', g2); A.circle(88 + dx / 2 + dx * c2, 135, 34, 'f-acc op3 s-acc w1', g2); }
        A.text(200, 212, '深色重叠 = 浪费（两个基站抢同一块地方）', { cls: 't-b', anchor: 'middle' }, g2); G.push(g2);
        var g3 = A.g();
        shapes.forEach(function (s, i) {
          var x = 75 + 125 * i, y = 104, rr = 44, pts = [];
          A.circle(x, y, rr, 'f-none s-faint w1 dash', g3);
          for (var m = 0; m < s.n; m++) { var a = Math.PI / 2 + 2 * Math.PI * m / s.n + (s.n === 4 ? Math.PI / 4 : 0); pts.push([x + rr * Math.cos(a), y - rr * Math.sin(a)]); }
          A.poly(pts, (s.n === 6 ? 'f-goods s-good' : 'f-accs s-acc') + ' w2', g3);
          A.text(x, 172, s.l + ' ' + Math.round(s.f * 100) + '%', { cls: 't-b' + (s.n === 6 ? ' f-good' : ''), anchor: 'middle' }, g3);
        });
        A.text(200, 200, '（多边形面积 ÷ 外接圆面积）', { cls: 't-s', anchor: 'middle' }, g3); G.push(g3);
        var g4 = A.g(), R = 30, cx = 200, cy = 112;
        cellsWithin(S3 + 1e-6).forEach(function (c) { var p = latXY(c.a, c.b, R, cx, cy); A.path(hexD(p[0], p[1], R), 'f-goods s-good w2', g4); A.circle(p[0], p[1], 2.2, 'f-ink', g4); });
        var cap4 = A.text(200, 222, '无空隙、无重叠，和 6 个邻居各共享一条边', { cls: 't-b', anchor: 'middle' }, g4); G.push(g4);
        var g5 = A.g();
        A.line(cx, cy, cx, cy - R, 's-gold w3', g5); A.text(cx - 5, cy - 12, 'R', { cls: 't-b f-gold', anchor: 'end' }, g5);
        A.line(cx, cy, cx + S3 * R, cy, 's-pur w3', g5);
        A.text(cx + S3 * R / 2, cy + 16, 'd', { cls: 't-b f-pur', anchor: 'middle' }, g5);
        A.text(200, 222, 'd = √3·R ≈ 1.73R（相邻两中心距）', { cls: 't-b f-pur', anchor: 'middle' }, g5); G.push(g5);
        var vis = [[0], [1], [2], [3], [4], [4, 5]], K = 0;
        return {
          step: function (k) { K = k; },
          frame: function (ts) {
            var p = A.prog(ts, 0.8);
            G.forEach(function (g, i) { var on = vis[K].indexOf(i) >= 0; op(g, on ? (i === vis[K][vis[K].length - 1] ? p : 1) : 0); });
            op(cap4, K === 4 ? 1 : 0);
          }
        };
      }
    });
  })();

  /* ================= 2.3 system roles ================= */
  ANIM.reg('A:2.3', {
    title: '蜂窝系统里的角色和两类信道',
    cap: 'MS ↔ BS 走无线；BS ↔ MTSO（MSC）走有线；MTSO 再接到固定电话网 PSTN。无线链路上分<b>控制信道</b>（信令）和<b>业务信道</b>（语音/数据）。',
    h: 246, live: true, tween: 1, stepDur: 4,
    steps: [
      'MS（Mobile Station，移动台）= 你的手机，在小区里到处移动。',
      'BS（基站）：每个小区一个，含天线、控制器和一批收发信机，跟本区手机对话。',
      'MTSO（移动交换中心，也叫 MSC）：所有基站都连到它，是整个系统的"大脑"。',
      'MTSO 还是通往固定电话网 PSTN 的出口：手机可以打给座机。',
      '控制信道：只传"建立通话、挂断、切换"这类信令，不传语音本身。',
      '业务信道：真正承载你的声音（或数据）的信道。'
    ],
    init: function (A) {
      var C1 = [70, 70], C2 = [70, 182], MT = [222, 126], PS = [345, 126], LL = [345, 200];
      var gBS = A.g(), gMS = A.g(), gMT = A.g(), gPS = A.g(), gCt = A.g(), gTr = A.g();
      [C1, C2].forEach(function (c) { A.path(hexD(c[0], c[1], 46), 'f-card s-line w2', gBS); tower(A, c[0], c[1] - 10, 'ink', gBS); A.text(c[0] - 10, c[1] + 22, 'BS', { cls: 't-b', anchor: 'end' }, gBS); });
      var M1 = [100, 94];
      [M1, [42, 50], [98, 204]].forEach(function (m) { phone(A, m[0], m[1], 'acc', gMS); });
      A.text(108, 98, 'MS', { cls: 't-b f-acc' }, gMS);
      A.line(C1[0] + 8, C1[1] + 4, MT[0] - 50, MT[1] - 8, 's-soft w2', gMT); A.line(C2[0] + 8, C2[1], MT[0] - 50, MT[1] + 8, 's-soft w2', gMT);
      A.rect(MT[0] - 50, MT[1] - 22, 100, 44, 'f-card s-none', gMT, 8); A.rect(MT[0] - 50, MT[1] - 22, 100, 44, 'f-accs s-acc w2', gMT, 8);
      A.text(MT[0], MT[1] - 3, 'MTSO', { cls: 't-b', anchor: 'middle' }, gMT); A.text(MT[0], MT[1] + 13, '(MSC)  大脑', { cls: 't-s', anchor: 'middle' }, gMT);
      A.line(MT[0] + 50, MT[1], PS[0] - 40, PS[1], 's-soft w2', gPS);
      A.el('ellipse', { cx: PS[0], cy: PS[1], rx: 40, ry: 24, cls: 'f-card s-none' }, gPS); A.el('ellipse', { cx: PS[0], cy: PS[1], rx: 40, ry: 24, cls: 'f-golds s-gold w2' }, gPS);
      A.text(PS[0], PS[1] - 2, 'PSTN', { cls: 't-b', anchor: 'middle' }, gPS); A.text(PS[0], PS[1] + 13, '固定电话网', { cls: 't-s', anchor: 'middle' }, gPS);
      A.line(PS[0], PS[1] + 24, LL[0], LL[1] - 10, 's-soft w2', gPS);
      A.rect(LL[0] - 16, LL[1] - 10, 32, 18, 'f-card s-ink w2', gPS, 4); A.text(LL[0], LL[1] + 24, '座机', { cls: 't-s', anchor: 'middle' }, gPS);
      /* control: dashed gold link with signalling packets; traffic: accent link with voice dots */
      A.line(M1[0] - 2, M1[1] - 8, C1[0] + 4, C1[1] + 2, 's-gold w2 dash', gCt);
      var pk = A.rect(0, 0, 9, 6, 'f-gold', gCt, 1);
      var ctT = A.text(158, 30, '控制信道：建立 / 挂断 / 切换', { cls: 't-b f-gold' }, gCt);
      var route = [M1, C1, [MT[0] - 50, MT[1] - 8], MT, [PS[0] - 40, PS[1]], PS, LL];
      A.path('M' + route.map(function (p) { return p[0] + ' ' + p[1]; }).join('L'), 's-acc w3', gTr);
      var vd = []; for (var i = 0; i < 6; i++) vd.push(A.circle(0, 0, 3.2, 'f-acc', gTr));
      A.text(158, 30, '业务信道：你的声音 / 数据', { cls: 't-b f-acc' }, gTr);
      A.svg.insertBefore(gTr, gMT);
      var lab = A.text(390, 30, '', { cls: 't-l t-b', anchor: 'end' });
      var names = ['MS = 手机', 'BS = 基站', 'MTSO = 交换中心', 'PSTN = 固定电话网', '', ''];
      var G = [gMS, gBS, gMT, gPS, gCt, gTr], K = 0;
      return {
        step: function (k) { K = k; A.setText(lab, names[k]); },
        frame: function (ts) {
          var p = A.prog(ts, 0.7);
          G.forEach(function (g, i) {
            var v = i < 4 ? (i < K ? (K >= 4 ? 1 : 0.45) : i === K ? p : 0) : (i === K ? p : 0);
            if (i === 1 && K === 0) v = 0.3;
            op(g, v);
          });
          op(lab, p); op(ctT, 1);
          var s = (ts * 0.6) % 1, q = s < 0.5 ? s * 2 : 2 - s * 2;   // packet goes up and back
          var pp = along([[M1[0] - 2, M1[1] - 8], [C1[0] + 4, C1[1] + 2]], q);
          A.set(pk, { x: pp[0] - 4.5, y: pp[1] - 3 });
          vd.forEach(function (d, i) { var xy = along(route, ((ts * 0.18) + i / vd.length) % 1); A.set(d, { cx: xy[0], cy: xy[1] }); });
        }
      };
    }
  });

  /* ================= 2.4 making a call ================= */
  ANIM.reg('A:2.4', {
    title: '打一通电话：从开机到接通',
    cap: '金色小球 = 控制信道上的信令；蓝色粗线 = 分配好的业务信道。MTSO 在中间调度一切。',
    h: 246, live: true, tween: 1, stepDur: 4.6,
    steps: [
      '开机：手机扫描控制信道，锁定最强的那个，经基站向 MTSO 登记身份和位置。',
      '主叫拨号：先确认控制信道空闲，把被叫号码发给基站，基站转给 MTSO。',
      '寻呼 paging：MTSO 不知道被叫在哪个小区，让一批基站在控制信道上广播"有人找你"。',
      '被叫手机认出自己的号码，应答，经基站一路回传到 MTSO。',
      'MTSO 接通两个基站之间的电路，两边各分配一个空闲业务信道，手机调过去，开始通话。',
      '通话中被叫走进相邻小区 → 切换 handoff：业务信道换到新基站（第十章）。'
    ],
    init: function (A) {
      var MT = [200, 34], B = [[62, 180], [200, 180], [338, 180]], top = [MT[0], MT[1] + 18];
      var M1 = [82, 206], M2a = [220, 206], M2b = [324, 206];
      A.rect(MT[0] - 48, MT[1] - 18, 96, 36, 'f-accs s-acc w2', null, 8); A.text(MT[0], MT[1] + 5, 'MTSO', { cls: 't-b', anchor: 'middle' });
      ['A', 'B', 'C'].forEach(function (n, i) {
        A.path(hexD(B[i][0], B[i][1], 46), 'f-card s-line w2'); A.line(B[i][0], B[i][1] - 12, top[0], top[1], 's-line w2');
        tower(A, B[i][0], B[i][1] - 12, 'ink'); A.text(B[i][0] - 24, B[i][1] + 30, n + ' 区', { cls: 't-s', anchor: 'middle' });
      });
      var gTr = A.g(), gB = A.g({}, gTr), gC = A.g({}, gTr);
      A.path('M' + M1.join(' ') + 'L' + B[0][0] + ' ' + (B[0][1] - 12) + 'L' + top.join(' '), 's-acc w4', gTr);
      A.line(top[0], top[1], B[1][0], B[1][1] - 12, 's-acc w4', gB); var airB = A.line(B[1][0], B[1][1] - 12, M2a[0], M2a[1], 's-acc w4', gB);
      A.line(top[0], top[1], B[2][0], B[2][1] - 12, 's-acc w4', gC); var airC = A.line(B[2][0], B[2][1] - 12, M2b[0], M2b[1], 's-acc w4', gC);
      phone(A, M1[0], M1[1], 'acc'); var ph2 = phone(A, M2a[0], M2a[1], 'gold');
      A.text(M1[0] + 9, M1[1] + 22, '主叫', { cls: 't-s' }); var t2 = A.text(M2a[0] + 9, M2a[1] + 22, '被叫', { cls: 't-s' });
      var rings = [0, 1, 2].map(function () { return A.circle(0, 0, 0, 'f-none s-gold w2'); });
      var tok = [0, 1].map(function () { var g = A.g(); A.circle(0, 0, 5, 'f-gold', g); g._t = A.text(0, -9, '', { cls: 't-b f-gold', anchor: 'middle', size: 11 }, g); return g; });
      var vd = [0, 1, 2, 3].map(function () { return A.circle(0, 0, 3, 'f-acc'); });
      var up = function (bi, m) { return [m, [B[bi][0], B[bi][1] - 12], top]; };
      var down = function (bi) { return [top, [B[bi][0], B[bi][1] - 12]]; };
      var plan = [
        [{ p: up(0, M1), l: '登记' }, { p: up(1, M2a), l: '登记' }],
        [{ p: up(0, M1), l: '被叫号码' }],
        [{ p: down(1), l: '寻呼' }, { p: down(2), l: '寻呼' }],
        [{ p: up(1, M2a), l: '应答' }],
        [{ p: down(0).concat([M1]), l: '信道号' }, { p: down(1).concat([M2a]), l: '信道号' }],
        []
      ];
      var K = 0;
      return {
        step: function (k) { K = k; plan[k].forEach(function (m, i) { A.setText(tok[i]._t, m.l); }); },
        frame: function (ts) {
          var pl = plan[K];
          tok.forEach(function (g, i) {
            if (!pl[i]) { op(g, 0); return; }
            var s = clamp((ts - 0.5) / 1.8, 0, 1), xy = along(pl[i].p, s);
            g.setAttribute('transform', 'translate(' + f1(xy[0]) + ' ' + f1(xy[1]) + ')'); op(g, ts < 0.5 || s >= 1 ? 0 : 1);
          });
          /* scanning rings at power-on, broadcast rings while paging */
          rings.forEach(function (c, i) {
            var on = false, cx = 0, cy = 0, rr = 0, ph = (ts * 0.8 + i / 3) % 1;
            if (K === 0 && ts < 1.2) { on = true; cx = M1[0]; cy = M1[1]; rr = 6 + 30 * ph; }
            if (K === 2 && ts > 2.2 && i < 2) { on = true; cx = B[i + 1][0]; cy = B[i + 1][1] - 12; rr = 8 + 34 * ((ts * 0.8) % 1); }
            A.set(c, { cx: cx, cy: cy, r: rr }); op(c, on ? 1 - (K === 0 ? ph : (ts * 0.8) % 1) : 0);
          });
          var talk = K >= 4, hp = K === 5 ? A.prog(ts, 2.2, 0.3) : 0;
          var m2 = [A.lerp(M2a[0], M2b[0], hp), M2a[1]];
          ph2.setAttribute('transform', 'translate(' + f1(m2[0] - M2a[0]) + ' 0)'); A.set(t2, { x: m2[0] + 9 });
          op(gTr, talk ? (K === 4 ? 0.75 * clamp((ts - 2.2) * 2, 0, 1) : 0.75) : 0);
          op(gB, hp < 0.5 ? 1 : 0); op(gC, hp >= 0.5 ? 1 : 0);
          A.set(airC, { x2: m2[0], y2: m2[1] }); A.set(airB, { x2: m2[0], y2: m2[1] });
          var route = [M1, [B[0][0], B[0][1] - 12], top, hp < 0.5 ? [B[1][0], B[1][1] - 12] : [B[2][0], B[2][1] - 12], m2];
          vd.forEach(function (d, i) { var xy = along(route, (ts * 0.22 + i / 4) % 1); A.set(d, { cx: xy[0], cy: xy[1] }); op(d, talk && (K === 5 || ts > 2.6) ? 1 : 0); });
        }
      };
    }
  });

  /* ================= 3.1 1G ================= */
  ANIM.reg('A:3.1', {
    title: '1G：纯模拟，一条信道一个人',
    cap: '1G 用模拟调制传语音，多址方式就是 FDMA：工作在 800–900 MHz，信道间隔 AMPS 30 kHz、ETACS 25 kHz，只为打电话，没有数据业务。',
    h: 230,
    init: function (A) {
      timeline(A, 0);
      A.text(200, 60, 'AMPS（美/澳）· ETACS（欧）· NTT（日）', { cls: 't-b', anchor: 'middle' });
      A.rect(40, 70, 290, 12, 'f-accs s-acc w1', null, 2);
      A.text(36, 80, '800', { cls: 't-s', anchor: 'end' }); A.text(334, 80, '900 MHz', { cls: 't-s' });
      A.rect(241, 67, 4, 18, 'f-gold', null, 1);   // ≈ 870 MHz
      A.text(40, 108, '其中一小段放大（金色处）：每条信道一个用户的模拟语音', { cls: 't-s' });
      var x0 = 40, x1 = 360, yb = 186, span = 240;
      A.line(x0, yb, x1, yb, 's-soft w1');
      var humps = [], ticks = A.path('', 's-line w1'), dim = A.g();
      for (var i = 0; i < 10; i++) humps.push(A.path('', 'f-accs s-acc w1'));
      var dimL = A.arrow(x0, 198, x0 + 40, 198, 's-ink w1', dim, 5), dimT = A.text(0, 214, '', { cls: 't-m', size: 11, anchor: 'middle' }, dim);
      var sys = 0, sp = [30, 25], name = ['AMPS', 'ETACS'];
      A.choice({ label: '系统', options: ['AMPS 30 kHz', 'ETACS 25 kHz'], value: 0, on: function (v) { sys = v; A.redraw(); } });
      return function (t) {
        var cw = (x1 - x0) * sp[sys] / span, n = Math.floor(span / sp[sys]), td = '';
        for (var i = 0; i < humps.length; i++) {
          if (i >= n) { humps[i].setAttribute('d', ''); continue; }
          var xc = x0 + cw * (i + 0.5), hw = cw / 2 - 2.5, a = 0.45 + 0.4 * Math.abs(Math.sin(t * (0.9 + 0.23 * i) + i * 1.7)), d = '';
          for (var s = 0; s <= 16; s++) { var x = xc - hw + 2 * hw * s / 16, c = Math.cos(Math.PI * (x - xc) / (2 * hw)); d += (s ? 'L' : 'M') + f1(x) + ' ' + f1(yb - 62 * a * c * c); }
          A.set(humps[i], { d: d + 'Z', cls: 'f-' + UC[i % 4] + 's s-' + UC[i % 4] + ' w1' });
          td += 'M' + f1(x0 + cw * i) + ' ' + (yb - 70) + 'V' + (yb + 4);
        }
        ticks.setAttribute('d', td + 'M' + f1(x0 + cw * n) + ' ' + (yb - 70) + 'V' + (yb + 4));
        A.moveArrow(dimL, x0 + 1, 198, x0 + cw - 1, 198); A.set(dimT, { x: x0 + cw / 2 }); A.setText(dimT, sp[sys] + ' kHz');
        A.note(name[sys] + '：信道间隔 ' + sp[sys] + ' kHz → 每 MHz 约 ' + Math.floor(1000 / sp[sys]) + ' 条信道（1000 ÷ ' + sp[sys] + '）');
      };
    }
  });

  /* ================= 3.2 2G ================= */
  ANIM.reg('A:3.2', {
    title: '2G：数字化的三条路线',
    cap: '2G 要更大容量、更低成本、跨国漫游。GSM 走 TDMA，IS-95 走 CDMA（扩频 + Walsh 码 + 1 ms 功率控制），N-AMPS 是把 AMPS 信道一分为三的过渡方案。',
    h: 256,
    init: function (A) {
      timeline(A, 1);
      var views = [A.g(), A.g(), A.g()], v = 0;
      /* GSM: carriers × TDMA slots */
      var G = views[0], gx = 62, sw = 19, nS = 8, rows = 4, rh = 26, gy = 66, cells = [];
      A.text(gx - 6, gy - 4, 'f', { cls: 't-s', anchor: 'end' }, G);
      for (var r = 0; r < rows; r++) {
        A.text(gx - 6, gy + r * rh + 17, '载波' + (r + 1), { cls: 't-s', anchor: 'end' }, G);
        for (var c = 0; c < 2 * nS; c++) {
          var mine = r === 1 && c % nS === 2;
          cells.push({ c: c, el: A.rect(gx + c * sw + 0.5, gy + r * rh + 1, sw - 1, rh - 2, mine ? 'f-acc' : 'f-line', G, 1), mine: mine });
        }
      }
      [0, 1].forEach(function (f) { A.text(gx + (f + 0.5) * nS * sw, gy + rows * rh + 14, '帧 ' + (f + 1) + '：8 个时隙', { cls: 't-s', anchor: 'middle' }, G); });
      A.line(gx + nS * sw, gy - 4, gx + nS * sw, gy + rows * rh + 4, 's-ink w2', G);
      var gcur = A.line(gx, gy - 6, gx, gy + rows * rh + 4, 's-bad w2', G);
      A.text(200, 206, '25 MHz ÷ 200 kHz = ' + (25e6 / 200e3) + ' 个 200 kHz 载波', { cls: 't-b', anchor: 'middle' }, G);
      A.text(200, 226, '每个载波再用 TDMA 切时隙，蓝色 = 一个用户的时隙', { cls: 't-s', anchor: 'middle' }, G);
      /* IS-95: spread + power control */
      var C = views[1], bars = [], lvl = [], tick = -1;
      A.rect(30, 66, 160, 110, 'f-none s-soft w1 dash', C, 4);
      for (var u = 0; u < 4; u++) A.rect(34 + u * 3, 70 + u * 3, 150, 100, 'f-' + UC[u] + ' op3 s-' + UC[u] + ' w1', C, 3);
      A.text(110, 126, '4 个用户叠在一起', { cls: 't-b', anchor: 'middle' }, C);
      A.text(110, 192, '同一宽频带，同时发', { cls: 't-s', anchor: 'middle' }, C); A.text(110, 208, '靠 Walsh 码区分', { cls: 't-s', anchor: 'middle' }, C);
      var tgt = 130; A.line(250, tgt, 392, tgt, 's-good w2 dash', C); A.text(246, tgt + 4, '目标', { cls: 't-b f-good', size: 11, anchor: 'end' }, C);
      A.line(250, 176, 392, 176, 's-soft w1', C);
      for (var b = 0; b < 4; b++) { bars.push(A.rect(260 + b * 34, tgt, 24, 176 - tgt, 'f-' + UC[b], C, 2)); lvl.push(0); }
      var pcT = A.text(318, 194, '', { cls: 't-b', anchor: 'middle', size: 11 }, C);
      A.text(318, 212, '太强压别人，太弱被淹没', { cls: 't-s', anchor: 'middle' }, C);
      A.text(200, 236, '每个窄带信号被"摊薄"铺满整个宽带（直接序列扩频）', { cls: 't-s', anchor: 'middle' }, C);
      /* N-AMPS: 30 kHz → 3 × 10 kHz */
      var Nn = views[2], nx = 80, nw = 240, ny = 80, nh = 70, parts = [];
      A.rect(nx, ny, nw, nh, 'f-accs s-acc w2', Nn, 4);
      for (var q = 0; q < 3; q++) parts.push(A.rect(nx + q * nw / 3 + 2, ny + 2, nw / 3 - 4, nh - 4, 'f-' + UC[q] + 's s-' + UC[q] + ' w2', Nn, 3));
      var nT = A.text(200, ny + nh / 2 + 5, '', { cls: 't-b', anchor: 'middle' }, Nn);
      A.text(200, 180, '30 kHz ÷ 10 kHz = ' + (30 / 10) + ' → 容量 ×' + (30 / 10), { cls: 't-l t-b f-good', anchor: 'middle' }, Nn);
      A.text(200, 202, '1G 到 2G 之间的折中方案', { cls: 't-s', anchor: 'middle' }, Nn);
      A.choice({ options: ['GSM（TDMA）', 'IS-95（CDMA）', 'N-AMPS'], value: 0, on: function (k) { v = k; A.redraw(); } });
      var rng = A.rng(7);
      return function (t, dt) {
        views.forEach(function (g, i) { op(g, i === v ? 1 : 0); g.style.display = i === v ? '' : 'none'; });
        if (v === 0) {
          var u = (t % 6) / 6, cx = gx + 2 * nS * sw * u;
          A.set(gcur, { x1: cx, x2: cx });
          cells.forEach(function (o) { op(o.el, o.mine ? (gx + o.c * sw < cx ? 1 : 0.25) : (gx + o.c * sw < cx ? 0.8 : 0.3)); });
        } else if (v === 1) {
          var tk = Math.floor(t / 0.9);
          if (tk !== tick) { tick = tk; for (var b = 0; b < 4; b++) lvl[b] = 0; }
          var ph = (t % 0.9) / 0.9;
          for (var b2 = 0; b2 < 4; b2++) {
            if (ph > 0.15) lvl[b2] += (rng() - 0.5) * 70 * (dt || 0.05);
            var hgt = clamp(176 - tgt + lvl[b2] * 22, 8, 106);
            A.set(bars[b2], { y: 176 - hgt, height: hgt });
          }
          A.setText(pcT, ph < 0.15 ? '功率控制：全部拉回目标！' : '每 1 ms 调一次功率');
        } else {
          var s = (t % 6) / 6, split = s > 0.35;
          parts.forEach(function (p) { op(p, split ? A.ease((s - 0.35) * 5) : 0); });
          A.setText(nT, split ? '3 × 10 kHz：3 个用户（N-AMPS）' : '30 kHz：1 个用户（AMPS）');
        }
      };
    }
  });

  /* ================= 3.3 3G ================= */
  ANIM.reg('A:3.3', {
    title: '3G：从打电话到上网',
    cap: '3G 第一次把目标定在高速多媒体数据上，同时支持电路交换（语音）和分组交换（数据）；空口用 WCDMA / MC-CDMA，数据用 Turbo 码；蜂窝变成宏-微-微微分层结构。',
    h: 262, live: true, tween: 1, stepDur: 4,
    steps: [
      '电路交换：通话期间整条线路一直被占着，没说话也占（适合语音）。',
      '分组交换：数据切成一个个包，有数据才发，多个用户共用一条链路（适合上网）。',
      '3G 两种都支持；空口用 WCDMA 或 MC-CDMA，数据用纠错更强的 Turbo 码。',
      '分层蜂窝：大的宏蜂窝里套微蜂窝，微蜂窝里再套微微蜂窝。'
    ],
    init: function (A) {
      timeline(A, 2);
      var gC = A.g(), gP = A.g(), gI = A.g(), gH = A.g();
      A.text(10, 60, '电路交换（语音）', { cls: 't-b' }, gC); A.text(390, 60, '整条线一直被 A–B 占着', { cls: 't-s', anchor: 'end' }, gC);
      A.text(14, 84, 'A', { cls: 't-b' }, gC); A.text(386, 84, 'B', { cls: 't-b', anchor: 'end' }, gC);
      A.rect(28, 70, 344, 18, 'f-accs s-acc w1', gC, 9);
      var vd = []; for (var i = 0; i < 10; i++) vd.push(A.circle(0, 79, 3.2, 'f-acc', gC));
      A.text(10, 110, '分组交换（数据）', { cls: 't-b' }, gP); A.text(390, 110, '大家共用，有包才发', { cls: 't-s', anchor: 'end' }, gP);
      A.line(28, 128, 372, 128, 's-line w4', gP);
      var pk = [], rng = A.rng(33), off = 0;
      for (var j = 0; j < 9; j++) { off += 0.06 + rng() * 0.08; pk.push({ el: A.rect(0, 122, 14, 12, 'f-' + UC[j % 3 === 0 ? 0 : j % 3 === 1 ? 1 : 2], gP, 2), o: off }); }
      A.text(200, 156, '空口 WCDMA / MC-CDMA · 数据纠错用 Turbo 码', { cls: 't-b f-pur', anchor: 'middle', size: 11.5 }, gI);
      var hx = 104, hy = 214;
      A.path(hexD(hx, hy, 44), 'f-accs s-acc w2', gH);
      [[-16, -9], [16, -9], [0, 18]].forEach(function (o) {
        A.path(hexD(hx + o[0], hy + o[1], 14), 'f-golds s-gold w2', gH);
        A.circle(hx + o[0] - 4, hy + o[1] + 2, 3.6, 'f-good', gH); A.circle(hx + o[0] + 5, hy + o[1] - 2, 3.6, 'f-good', gH);
      });
      A.line(148, 186, 172, 186, 's-acc w1', gH); A.text(176, 190, '宏蜂窝 macro：大，覆盖广', { cls: 'f-acc', size: 11 }, gH);
      A.line(134, 205, 172, 214, 's-gold w1', gH); A.text(176, 218, '微蜂窝 micro：街区', { cls: 'f-gold', size: 11 }, gH);
      A.line(126, 234, 172, 242, 's-good w1', gH); A.text(176, 246, '微微蜂窝 pico：楼内 / 热点', { cls: 'f-good', size: 11 }, gH);
      var G = [gC, gP, gI, gH], K = 0;
      return {
        step: function (k) { K = k; },
        frame: function (ts) {
          var p = A.prog(ts, 0.7);
          G.forEach(function (g, i) { op(g, i === K ? p : i < K ? (K === 2 && i < 2 ? 1 : 0.4) : 0); });
          if (K === 2) op(gI, p);
          var talk = Math.sin(ts * 2.2) > -0.2;                    // talk spurts: pipe stays reserved
          vd.forEach(function (d, i) { var x = 30 + ((ts * 60 + i * 34.4) % 344); A.set(d, { cx: x }); op(d, talk ? 1 : 0); });
          pk.forEach(function (o) { var s = (ts * 0.16 + o.o) % 1; A.set(o.el, { x: 28 + s * 330 }); });
        }
      };
    }
  });

  /* ================= 3.4 4G ================= */
  ANIM.reg('A:3.4', {
    title: '4G LTE：OFDMA + 一切走 IP',
    cap: '下行 OFDMA：频带切成许多正交子载波，调度器每个时刻把一块块时频资源分给不同用户（抗多径能力强）。上行用省电的 SC-FDMA，配合 MIMO 下行峰值可超过 300 Mbps。',
    h: 236,
    init: function (A) {
      timeline(A, 3);
      var gx = 40, gy = 56, cw = 18, rh = 16, nc = 12, nr = 8, cells = [];
      for (var r = 0; r < nr; r++) for (var c = 0; c < nc; c++) cells.push(A.rect(gx + c * cw + 0.5, gy + r * rh + 0.5, cw - 1, rh - 1, 'f-line', null, 1));
      A.arrow(gx - 4, gy + nr * rh + 4, gx + nc * cw + 10, gy + nr * rh + 4, 's-soft w1', null, 5);
      A.arrow(gx - 4, gy + nr * rh + 4, gx - 4, gy - 6, 's-soft w1', null, 5);
      A.text(gx + nc * cw + 10, gy + nr * rh + 18, '时间', { cls: 't-s', anchor: 'end' });
      A.text(gx - 8, gy + 8, '子', { cls: 't-s', anchor: 'end' }); A.text(gx - 8, gy + 22, '载', { cls: 't-s', anchor: 'end' }); A.text(gx - 8, gy + 36, '波', { cls: 't-s', anchor: 'end' });
      for (var u = 0; u < 4; u++) { A.rect(gx + u * 50, 212, 10, 10, 'f-' + UC[u], null, 2); A.text(gx + u * 50 + 14, 221, '用户' + (u + 1), { cls: 't-s' }); }
      var tx = 270, L = [[62, '下行：OFDMA', 't-b f-acc'], [80, '抗多径衰落'], [106, '上行：SC-FDMA', 't-b f-gold'], [124, '省电，适合手机'], [150, 'MIMO 多天线', 't-b'], [168, '峰值 > 300 Mbps'], [194, '一切业务走 IP', 't-b f-good']];
      L.forEach(function (l) { A.text(tx, l[0], l[1], { cls: l[2] || '', size: l[2] ? null : 11 }); });
      var rng = A.rng(11), tab = [];
      for (var k = 0; k < 64; k++) { var row = [], blk = 0; for (var r2 = 0; r2 < nr; r2++) { if (r2 % 2 === 0) blk = Math.floor(rng() * 5); row.push(blk); } tab.push(row); }
      return function (t) {
        var T = Math.floor(t / 0.55);
        for (var c = 0; c < nc; c++) for (var r = 0; r < nr; r++) {
          var a = tab[(T + c) % 64][r];
          A.set(cells[r * nc + c], { cls: a === 4 ? 'f-line op5' : 'f-' + UC[a] + (c === nc - 1 ? '' : ' op7') });
        }
      };
    }
  });

  /* ================= 4.1 duplex ================= */
  ANIM.reg('A:4.1', {
    title: 'FDD vs TDD：上下行怎么不打架',
    cap: 'FDD：上行、下行各一段频率，永久分开，同时进行。TDD：同一段频率，按时隙轮流；可以把更多时隙给下行（刷视频时下行多），FDD 做不到这种调整。',
    h: 226,
    init: function (A) {
      var x0 = 112, W = 270, ya = 200, mode = 0, nd = 3;
      tower(A, 46, 30, 'ink'); A.text(46, 64, 'BS', { cls: 't-b', anchor: 'middle' });
      phone(A, 46, 184, 'ink');
      var dl = A.arrow(36, 72, 36, 168, 's-acc w3', null, 8), ul = A.arrow(58, 168, 58, 72, 's-gold w3', null, 8);
      A.text(28, 124, 'DL', { cls: 't-b f-acc', anchor: 'end' }); A.text(66, 124, 'UL', { cls: 't-b f-gold' });
      A.arrow(x0 - 6, ya, x0 + W + 12, ya, 's-soft w1', null, 5); A.arrow(x0 - 6, ya, x0 - 6, 26, 's-soft w1', null, 5);
      A.text(x0 + W + 12, ya + 14, '时间 t', { cls: 't-s', anchor: 'end' }); A.text(x0 - 2, 24, '频率 f', { cls: 't-s' });
      var gF = A.g(), gT = A.g();
      A.rect(x0, 36, W, 40, 'f-none s-line w1 dash', gF, 3); A.rect(x0, 146, W, 40, 'f-none s-line w1 dash', gF, 3);
      var fD = A.rect(x0, 36, 0, 40, 'f-accs s-acc w1', gF, 3), fU = A.rect(x0, 146, 0, 40, 'f-golds s-gold w1', gF, 3);
      A.text(x0 + 6, 60, '下行 DL：频段 f₂', { cls: 't-b f-acc', size: 11 }, gF); A.text(x0 + 6, 170, '上行 UL：频段 f₁', { cls: 't-b f-gold', size: 11 }, gF);
      A.text(x0 + W / 2, 116, '两段频率永久分开，可同时收发', { cls: 't-s', anchor: 'middle' }, gF);
      A.text(x0, 82, '同一段频率 f₀，上下行轮流用', { cls: 't-s' }, gT);
      var nS = 10, sw = W / nS, sl = [];
      for (var i = 0; i < nS; i++) {
        A.rect(x0 + i * sw + 1, 92, sw - 2, 60, 'f-none s-line w1 dash', gT, 2);
        sl.push({ r: A.rect(x0 + i * sw + 1, 92, 0, 60, 'f-accs', gT, 2), t: A.text(x0 + i * sw + sw / 2, 127, '', { cls: 't-b', anchor: 'middle' }, gT) });
      }
      var cur = A.line(x0, 30, x0, ya, 's-ink w1');
      A.choice({ label: '方式', options: ['FDD', 'TDD'], value: 0, on: function (v) { mode = v; A.redraw(); } });
      A.slider({ label: 'TDD 下行时隙', min: 1, max: 4, step: 1, value: nd, fmt: function (v) { return v + ' : ' + (5 - v); }, on: function (v) { nd = v; A.redraw(); } });
      return function (t) {
        var u = Math.min(1, (t % 7.5) / 6.5), cx = x0 + W * u, act = -1;
        A.set(cur, { x1: cx, x2: cx });
        op(gF, mode === 0 ? 1 : 0); op(gT, mode === 1 ? 1 : 0);
        if (mode === 0) {
          A.set(fD, { width: cx - x0 }); A.set(fU, { width: cx - x0 });
          op(dl, 1); op(ul, 1);
          A.note('FDD：上下行各占一段固定频带 → 同时进行，但比例改不了');
        } else {
          sl.forEach(function (s, i) {
            var isD = (i % 5) < nd, w = clamp(cx - (x0 + i * sw) - 1, 0, sw - 2);
            A.set(s.r, { width: w, cls: isD ? 'f-accs s-acc w1' : 'f-golds s-gold w1' });
            A.setText(s.t, w > sw / 2 ? (isD ? 'D' : 'U') : ''); A.set(s.t, { cls: 't-b ' + (isD ? 'f-acc' : 'f-gold') });
            if (cx > x0 + i * sw && cx <= x0 + (i + 1) * sw && u < 1) act = isD ? 0 : 1;
          });
          op(dl, act === 0 ? 1 : 0.15); op(ul, act === 1 ? 1 : 0.15);
          A.note('TDD：每 5 个时隙 下行 ' + nd + ' : 上行 ' + (5 - nd) + ' → 下行占 ' + Math.round(nd / 5 * 100) + ' % 时间（可按需调）');
        }
      };
    }
  });

  /* ================= 4.2 spectral efficiency worked example ================= */
  (function () {
    var BW = 12.5, sp = 30, ctlPer = 3, N = 7, Aerl = 45.9, area = 4, total = 2000;   // Erlang value as printed on the page
    var nCh = Math.floor(BW * 1000 / sp), ctl = ctlPer * N, voice = nCh - ctl, perCell = Math.floor(voice / N);
    var dens = Aerl / area, eta = Aerl / (BW * area), cellsTot = total / area;
    ANIM.reg('A:4.2', {
      title: '例题：AMPS 的 ηₘ 一步步算',
      cap: 'η<sub>m</sub> = 每小区话务量 ÷（带宽 × 小区面积）。只有语音信道能产生话务量，所以先扣掉控制信道。总面积 ' + total + ' km² 不影响结果：全网 ' + cellsTot + ' 个小区 × ' + Aerl + ' ÷ (' + BW + ' × ' + total + ') ≈ ' + (cellsTot * Aerl / (BW * total)).toFixed(2) + '，一样。',
      h: 236, tween: 1.2, stepDur: 4.4,
      steps: [
        '每家运营商 ' + BW + ' MHz，按 ' + sp + ' kHz 一条切：' + BW + ' MHz ÷ ' + sp + ' kHz = ' + nCh + ' 条（取整）。',
        '每小区留 ' + ctlPer + ' 条控制信道，一簇 ' + N + ' 个小区共 ' + ctl + ' 条：' + nCh + ' − ' + ctl + ' = ' + voice + ' 条语音信道。',
        voice + ' 条分给簇里 ' + N + ' 个小区：' + voice + ' ÷ ' + N + ' ≈ ' + perCell + ' 条/小区。',
        '查 Erlang B 表：' + perCell + ' 条、GoS 2% → 每小区 ' + Aerl + ' Erlang，即 ' + dens.toFixed(1) + ' Erl/km²。',
        'η<sub>m</sub> = ' + Aerl + ' ÷ (' + BW + ' × ' + area + ') ≈ ' + eta.toFixed(2) + ' Erlang/MHz/km²。'
      ],
      init: function (A) {
        var bx = 20, bw = 360, by = 34;
        A.text(bx, 26, BW + ' MHz（一家运营商）', { cls: 't-b' });
        var nT = A.text(380, 26, '÷ ' + sp + ' kHz = ' + nCh + ' 条', { cls: 't-b f-acc', anchor: 'end' });
        A.rect(bx, by, bw, 22, 'f-accs s-acc w1', null, 2);
        var d = ''; for (var i = 1; i < nCh; i++) d += 'M' + f1(bx + bw * i * sp / (BW * 1000)) + ' ' + by + 'V' + (by + 22);
        A.path(d, 's-acc w1 op3');
        var gCtl = A.g(), cw = bw * ctl * sp / (BW * 1000);
        A.rect(bx, by, cw, 22, 'f-gold', gCtl, 2);
        A.text(bx, 74, ctl + ' 条控制（' + ctlPer + ' × ' + N + '）', { cls: 'f-gold t-b', size: 11 }, gCtl);
        A.text(380, 74, voice + ' 条语音', { cls: 'f-acc t-b', anchor: 'end', size: 11 }, gCtl);
        var gCl = A.g(), R = 25, cx = 96, cy = 166, ring = null;
        cellsWithin(S3 + 1e-6).forEach(function (c, k) {
          var p = latXY(c.a, c.b, R, cx, cy);
          A.path(hexD(p[0], p[1], R), 'f-card s-acc w1', gCl);
          A.text(p[0], p[1] + 4, String(perCell), { cls: 't-b t-m', anchor: 'middle' }, gCl);
          if (k === 0) ring = A.path(hexD(p[0], p[1], R - 2), 'f-none s-gold w3', gCl);
        });
        var tx = 200, lines = [
          [100, voice + ' ÷ ' + N + ' = ' + (voice / N).toFixed(1) + ' → ' + perCell + ' 条/小区', 2],
          [128, 'Erlang B（GoS 2%）：', 3], [146, perCell + ' 条 → ' + Aerl + ' Erl/小区', 3], [164, Aerl + ' ÷ ' + area + ' km² = ' + dens.toFixed(1) + ' Erl/km²', 3],
          [192, 'η_{m} = ' + Aerl + ' ÷ (' + BW + ' × ' + area + ')', 4], [216, '≈ ' + eta.toFixed(2) + ' Erl/MHz/km²', 4]
        ].map(function (l, i) { return { k: l[2], el: A.text(tx, l[0], l[1], { cls: i === 5 ? 't-l t-b f-good' : i === 0 || i === 4 ? 't-b' : '' }) }; });
        var K = 0;
        return {
          step: function (k) { K = k; },
          frame: function (ts) {
            var p = A.prog(ts, 0.8);
            op(nT, K === 0 ? p : 1); op(gCtl, K === 1 ? p : K > 1 ? 1 : 0); op(gCl, K === 2 ? p : K > 2 ? 1 : 0); op(ring, K >= 3 ? 1 : 0);
            lines.forEach(function (l) { op(l.el, l.k < K ? 0.6 : l.k === K ? p : 0); });
          }
        };
      }
    });
  })();

  /* ================= 5.1 free space ================= */
  ANIM.reg('A:5.1', {
    title: '自由空间：能量摊在越来越大的球面上',
    cap: '距离翻倍，同样的能量要摊到 4 倍面积上，每一格只分到 1/4（−6 dB）。下图是课件公式 L = 32 + 20 log f(MHz) + 20 log d(km)：距离 ×10 或频率 ×10，损耗都 +20 dB。',
    h: 262,
    init: function (A) {
      var sx = 28, sy = 70, k = 9 / 70;
      A.circle(sx, sy, 5, 'f-gold'); A.text(sx, sy + 20, '发射', { cls: 't-s', anchor: 'middle' });
      A.line(sx, sy, sx + 216, sy - 216 * k, 's-faint w1 dash'); A.line(sx, sy, sx + 216, sy + 216 * k, 's-faint w1 dash');
      var lbl = ['d：1 格', '2d：4 格', '3d：9 格'], per = ['每格 1', '每格 1/4', '每格 1/9'];
      for (var m = 1; m <= 3; m++) {
        var x = sx + 70 * m, hs = 9 * m, g = A.g();
        A.rect(x - hs / 2, sy - hs, hs, 2 * hs, 'f-accs s-acc w1', g, 1);     // a face-on square, drawn squeezed
        for (var q = 1; q < m; q++) { A.line(x - hs / 2, sy - hs + 2 * hs * q / m, x + hs / 2, sy - hs + 2 * hs * q / m, 's-acc w1', g); A.line(x - hs / 2 + hs * q / m, sy - hs, x - hs / 2 + hs * q / m, sy + hs, 's-acc w1', g); }
        A.text(x, sy + 46, lbl[m - 1], { cls: 't-s', anchor: 'middle' });
        A.text(x, sy + 62, per[m - 1], { cls: 't-b f-acc', anchor: 'middle', size: 11 });
      }
      [[48, 'P_{r} ∝ 1/d²', 't-l t-b'], [72, '能量摊在球面'], [90, '面积 4πd² 上'], [114, '距离 ×2 → −' + (20 * Math.log10(2)).toFixed(1) + ' dB'], [132, '距离 ×10 → −20 dB']]
        .forEach(function (l) { A.text(292, l[0], l[1], { cls: l[2] || '', size: l[2] ? null : 11 }); });
      var parts = [], rng = A.rng(5);
      for (var i = 0; i < 26; i++) parts.push({ s: (rng() * 2 - 1) * k * 0.95, o: rng(), el: A.circle(0, 0, 2, 'f-gold') });
      var L = function (f, d) { return 32 + 20 * Math.log10(f) + 20 * Math.log10(d); };
      var fs = [900, 1800, 9000], fl = ['900 MHz', '1800 MHz', '9 GHz'], sel = 0;
      var ax = A.axes({ x: 52, y: 164, w: 250, h: 74, xr: [0, Math.log10(20)], yr: [85, 140], yl: 'L (dB)', xAxisAt: 'bottom',
        ticksX: [{ v: 0, l: '1' }, { v: Math.log10(2), l: '2' }, { v: Math.log10(5), l: '5' }, { v: 1, l: '10' }, { v: Math.log10(20), l: '20 km' }], ticksY: [90, 110, 130], grid: true });
      var cv = fs.map(function (f) { return A.curve(ax, function (x) { return L(f, Math.pow(10, x)); }, 's-faint w1'); });
      var m1 = A.circle(0, 0, 3.5, 'f-acc'), m2 = A.circle(0, 0, 3.5, 'f-acc');
      var t1 = A.text(0, 0, '', { cls: 't-m f-acc', size: 11, anchor: 'start' }), t2 = A.text(0, 0, '', { cls: 't-m f-acc', size: 11, anchor: 'end' });
      var fT = A.text(310, 180, '', { cls: 't-b f-acc' });
      A.choice({ label: '频率 f', options: fl, value: 0, on: function (v) { sel = v; A.redraw(); } });
      return function (t) {
        parts.forEach(function (p) { var x = sx + 222 * ((t * 0.22 + p.o) % 1); A.set(p.el, { cx: x, cy: sy + p.s * (x - sx) }); });
        cv.forEach(function (c, i) { A.set(c, { cls: i === sel ? 's-acc w3' : 's-faint w1' }); });
        var f = fs[sel], a = L(f, 1), b = L(f, 10);
        A.set(m1, { cx: ax.X(0), cy: ax.Y(a) }); A.set(m2, { cx: ax.X(1), cy: ax.Y(b) });
        A.set(t1, { x: ax.X(0) + 6, y: ax.Y(a) + 15 }); A.setText(t1, a.toFixed(1));
        A.set(t2, { x: ax.X(1) + 6, y: ax.Y(b) + 15 }); A.set(t2, { anchor: 'start' }); A.setText(t2, b.toFixed(1));
        A.set(fT, { y: ax.Y(L(f, 20)) + 4 }); A.setText(fT, fl[sel]);
        A.note('f = ' + fl[sel] + '：L(1 km) = ' + a.toFixed(1) + ' dB，L(10 km) = ' + b.toFixed(1) + ' dB（+' + (b - a).toFixed(0) + ' dB）' +
          (sel ? '；比 900 MHz 多 ' + (a - L(900, 1)).toFixed(1) + ' dB' : ''));
      };
    }
  });

  /* ================= 5.2 empirical model: fit a line to measurements ================= */
  (function () {
    var gTrue = -35.4, rng = ANIM.util.rng(26), pts = [], n = 26, i;
    for (i = 0; i < n; i++) { var u = Math.log10(1) + (i + rng()) / n * Math.log10(20); pts.push([Math.pow(10, u), gTrue * u + 4 * rng.gauss()]); }
    var mx = 0, my = 0, sxx = 0, sxy = 0;
    pts.forEach(function (p) { mx += Math.log10(p[0]) / n; my += p[1] / n; });
    pts.forEach(function (p) { var x = Math.log10(p[0]) - mx; sxx += x * x; sxy += x * (p[1] - my); });
    var gam = sxy / sxx, P0 = my - gam * mx;
    ANIM.reg('A:5.2', {
      title: '经验模型：拿实测点拟合一条直线',
      cap: 'Okumura–Hata、CCIR 等经验模型都是"基础值 + 修正项"，从大量实测数据拟合出来。图中散点是模拟的城区测量（真实斜率 −35.4，加了随机起伏），用来演示拟合思路。',
      h: 246, tween: 1.6, stepDur: 4.2,
      steps: [
        '真实城区算不准，就去实测：在不同距离 d 记下接收功率，每个点是一次测量。',
        '横轴改用 log d（1、2、5、10、20 km）：散点大致排成一条下降的直线。',
        '最小二乘拟合 P<sub>R</sub> = P₀ + γ·log d：斜率 γ ≈ ' + gam.toFixed(1) + ' dB/十倍距离。',
        '对比：自由空间 γ = −20，平地 −40，城区 −30 ~ −35.4。γ 越负，蜂窝就得越小。'
      ],
      init: function (A) {
        var box = { x: 52, y: 26, w: 300, h: 180, yr: [-56, 4], yl: 'P_{R} − P₀ (dB)', ticksY: [0, -20, -40], xAxisAt: 'bottom', yAxisAt: 'left', grid: true };
        var axL = A.axes(Object.assign({}, box, { xr: [0, 20], ticksX: [0, 5, 10, 15, { v: 20, l: '20 km' }] }));
        var axG = A.axes(Object.assign({}, box, { xr: [0, Math.log10(20)], ticksX: [{ v: 0, l: '1' }, { v: Math.log10(2), l: '2' }, { v: Math.log10(5), l: '5' }, { v: 1, l: '10' }, { v: Math.log10(20), l: '20 km' }] }));
        var dots = pts.map(function () { return A.circle(0, 0, 3.2, 'f-soft op7'); });
        var fit = A.curve(axG, function (x) { return P0 + gam * x; }, 's-acc w3');
        var fs = A.curve(axG, function (x) { return -20 * x; }, 's-good w2 dash'), fl = A.curve(axG, function (x) { return -40 * x; }, 's-bad w2 dash');
        var X2 = Math.log10(20);
        function leg(y, cls, txt) { var g = A.g(); A.line(62, y - 4, 84, y - 4, cls, g); A.text(90, y, txt, { cls: 't-b f-' + cls.split(' ')[0].slice(2), size: 11 }, g); return g; }
        var tFit = leg(156, 's-acc w3', '城区拟合 γ ≈ ' + gam.toFixed(1)), tFs = leg(174, 's-good w2 dash', '自由空间 γ = −20'), tFl = leg(192, 's-bad w2 dash', '平地 γ = −40');
        var K = 0;
        return {
          step: function (k) { K = k; },
          frame: function (ts) {
            var p = A.prog(ts, 1.4), m = K === 0 ? 0 : K === 1 ? p : 1;
            op(axL.g, 1 - m); op(axG.g, m);
            pts.forEach(function (q, i) { var x = A.lerp(axL.X(q[0]), axG.X(Math.log10(q[0])), m); A.set(dots[i], { cx: x, cy: axG.Y(q[1]) }); });
            var pf = K === 2 ? A.prog(ts, 1) : K > 2 ? 1 : 0, pr = K === 3 ? A.prog(ts, 1) : 0;
            A.setCurve(fit, axG, [[0, P0], [X2 * pf, P0 + gam * X2 * pf]]); op(fit, pf > 0 ? 1 : 0); op(tFit, pf);
            [fs, fl, tFs, tFl].forEach(function (e) { op(e, pr); });
            A.note(K >= 2 ? '拟合结果：P_R − P₀ ≈ ' + P0.toFixed(1) + ' ' + (gam < 0 ? '−' : '+') + ' ' + Math.abs(gam).toFixed(1) + '·log d　（距离 ×10 → 弱 ' + Math.abs(gam).toFixed(1) + ' dB）' : '');
          }
        };
      }
    });
  })();

  /* ================= 5.3 path-loss exponent n ================= */
  ANIM.reg('A:5.3', {
    title: '路径损耗指数 n：拖一拖看衰减多快',
    cap: 'P<sub>r</sub> ∝ d<sup>−n</sup>，换成 dB：距离 ×10 掉 10n dB，距离 ×2 掉 10n·log2 ≈ 3n dB。灰线是课件三种环境：自由空间 n = 2、CCIR 城区 n = 3.54、平地双径 n = 4。',
    h: 236,
    init: function (A) {
      var ax = A.axes({ x: 52, y: 28, w: 270, h: 176, xr: [0, 1], yr: [-52, 2], yl: '相对 1 km 处 (dB)', xAxisAt: 'bottom', yAxisAt: 'left', grid: true,
        ticksX: [{ v: 0, l: '1' }, { v: Math.log10(2), l: '2' }, { v: Math.log10(5), l: '5' }, { v: 1, l: '10 km' }], ticksY: [0, -10, -20, -30, -40, -50] });
      [[2, 'n = 2'], [3.54, 'n = 3.54'], [4, 'n = 4']].forEach(function (r) {
        A.curve(ax, function (x) { return -10 * r[0] * x; }, 's-faint w1 dash');
        A.text(ax.X(1) + 6, ax.Y(-10 * r[0]) + 4, r[1], { cls: 't-s' });
      });
      var cv = A.curve(ax, function () { return 0; }, 's-acc w3');
      var p2 = A.circle(0, 0, 4, 'f-gold'), p10 = A.circle(0, 0, 4, 'f-bad');
      A.circle(64, 166, 4, 'f-gold'); A.circle(64, 184, 4, 'f-bad');
      var t2 = A.text(74, 170, '', { cls: 't-b f-gold', size: 11 }), t10 = A.text(74, 188, '', { cls: 't-b f-bad', size: 11 });
      var sl = A.text(396, 16, '', { cls: 't-b f-acc', anchor: 'end' });
      var n = 3.54;
      A.slider({ label: '指数 n', min: 2, max: 5, step: 0.02, value: n, fmt: function (v) { return v.toFixed(2); }, on: function (v) { n = v; draw(); } });
      function draw() {
        A.setCurve(cv, ax, function (x) { return -10 * n * x; });
        var l2 = Math.log10(2), d2 = 10 * n * l2, d10 = 10 * n;
        A.set(p2, { cx: ax.X(l2), cy: ax.Y(-d2) }); A.set(p10, { cx: ax.X(1), cy: ax.Y(-d10) });
        A.setText(t2, '1 → 2 km：−' + d2.toFixed(1) + ' dB');
        A.setText(t10, '1 → 10 km：−' + d10.toFixed(1) + ' dB');
        A.setText(sl, '斜率 −10n = −' + d10.toFixed(1) + ' dB/十倍距离');
        A.note('n = ' + n.toFixed(2) + '：距离 ×2 → 功率 ×1/' + A.fmt(Math.pow(2, n), 3) + '；距离 ×10 → 弱 ' + A.fmt(Math.pow(10, n), 3) + ' 倍');
      }
      draw();
      return {};
    }
  });

  /* ================= 6.1 cluster N = i² + ij + j² ================= */
  (function () {
    var IJ = [[1, 1], [2, 0], [2, 1], [3, 0], [2, 2], [3, 1]];
    ANIM.reg('A:6.1', {
      title: '簇：用 i、j 走到最近的同频小区',
      cap: '同一个数字 = 同一组信道（频率集）。粗线框是一个簇，含 N 个小区，正好用完全部信道；整片区域就是这个簇一块块重复铺出来的。蓝色 = 第 1 组的所有同频小区。',
      h: 290, tween: 2.4, stepDur: 4,
      steps: [
        '每个数字是一组信道。粗线框里是一个簇：N 个小区刚好把全部信道用完一遍。',
        '找最近的同频小区：从中心小区出发，垂直穿过六边形的边，直走 i 个小区。',
        '然后左转 60°，再直走 j 个小区——到了！这里和出发点用同一组信道。',
        '六个方向都这样走，得到一圈 6 个最近的同频小区；簇就这样不留缝地重复铺开。',
        'N = i² + ij + j²。只有 1、3、4、7、9、12、13、19、21… 能这样整齐镶嵌。'
      ],
      init: function (A) {
        var R = 15, cx = 200, cy = 143, H = A.H, ij = [2, 1];
        var cells = cellsWithin(8.6).filter(function (c) {
          var p = latXY(c.a, c.b, R, cx, cy); c.x = p[0]; c.y = p[1];
          return p[0] - S3 / 2 * R >= 2 && p[0] + S3 / 2 * R <= 398 && p[1] - R >= 2 && p[1] + R <= H - 2;
        });
        var have = {}; cells.forEach(function (c) { have[c.a + ',' + c.b] = 1; });
        var gHex = A.g(), paths = PAL.map(function (c) { return A.path('', c + ' s-card w2', gHex); });
        var nums = cells.map(function (c) { return A.text(c.x, c.y + 4, '', { size: 10.5, anchor: 'middle' }); });
        var outT = A.path('', 's-ink w1 dash'), out = A.path('', 's-ink w3');
        var leg1 = A.arrow(cx, cy, cx, cy, 's-gold w3', null, 8), leg2 = A.arrow(cx, cy, cx, cy, 's-gold w3', null, 8);
        var rings = [0, 1, 2, 3, 4, 5].map(function () { return A.circle(0, 0, R * 0.8, 'f-none s-gold w3'); });
        var dot = A.circle(cx, cy, 5, 'f-gold');
        var i, j, N, co = [];
        function edgePath(set, da, db) {
          var d = '';
          set.forEach(function (k) {
            var c = cells[k];
            if (!have[(c.a + da) + ',' + (c.b + db)]) return;
            DIRS.forEach(function (D, m) {
              if (set.some(function (q) { return cells[q].a === c.a + D[0] && cells[q].b === c.b + D[1]; })) return;
              var p = latXY(c.a + da, c.b + db, R, cx, cy), a1 = Math.PI / 180 * (60 * m - 30), a2 = Math.PI / 180 * (60 * m + 30);
              var x1 = p[0] + R * Math.cos(a1), y1 = p[1] - R * Math.sin(a1), x2 = p[0] + R * Math.cos(a2), y2 = p[1] - R * Math.sin(a2);
              if (Math.min(x1, x2) < 1 || Math.max(x1, x2) > 399 || Math.min(y1, y2) < 1 || Math.max(y1, y2) > H - 1) return;
              d += 'M' + f1(x1) + ' ' + f1(y1) + 'L' + f1(x2) + ' ' + f1(y2);
            });
          });
          return d;
        }
        function build() {
          i = ij[0]; j = ij[1]; N = i * i + i * j + j * j;
          var lab = labeler(i, j), ds = PAL.map(function () { return ''; }), clu = [];
          cells.forEach(function (c, k) {
            c.g = lab(c.a, c.b); ds[c.g] += hexD(c.x, c.y, R);
            A.setText(nums[k], String(c.g + 1)); A.set(nums[k], { cls: c.g === 0 ? 'f-card t-b' : '' });
            if (clu.length < N && clu.every(function (q) { return cells[q].g !== c.g; })) clu.push(k);
          });
          paths.forEach(function (p, g) { p.setAttribute('d', ds[g]); });
          out.setAttribute('d', edgePath(clu, 0, 0));
          var v = [i, j], dT = '';
          co = [];
          for (var r = 0; r < 6; r++) { co.push(latXY(v[0], v[1], R, cx, cy)); dT += edgePath(clu, v[0], v[1]); v = [-v[1], v[0] + v[1]]; }
          outT.setAttribute('d', dT);
          A.note('i = ' + i + '，j = ' + j + ' → N = ' + i + '² + ' + i + '·' + j + ' + ' + j + '² = ' + (i * i) + ' + ' + (i * j) + ' + ' + (j * j) + ' = ' + N);
        }
        A.choice({ label: '(i, j)', options: IJ.map(function (q) { return '(' + q[0] + ',' + q[1] + ') N=' + (q[0] * q[0] + q[0] * q[1] + q[1] * q[1]); }), value: 2,
          on: function (v) { ij = IJ[v]; build(); A.redraw(); } });
        build();
        var K = 0;
        return {
          step: function (k) { K = k; },
          frame: function (ts) {
            var p1 = K === 1 ? A.prog(ts, 1.6, 0.2) : K > 1 ? 1 : 0, p2 = K === 2 ? A.prog(ts, 1.6, 0.2) : K > 2 ? 1 : 0;
            var a = latXY(i * p1, 0, R, cx, cy), b = latXY(i, j * p2, R, cx, cy);
            A.moveArrow(leg1, cx, cy, a[0], a[1]); A.moveArrow(leg2, a[0], a[1], p1 >= 1 ? b[0] : a[0], p1 >= 1 ? b[1] : a[1]);
            op(leg1, K >= 1 && K <= 3 ? 1 : 0); op(leg2, K >= 2 && K <= 3 ? 1 : 0);
            var pos = K === 1 ? a : K >= 2 ? b : [cx, cy];
            A.set(dot, { cx: pos[0], cy: pos[1] }); op(dot, K >= 1 && K <= 3 ? 1 : 0);
            var pr = K === 3 ? A.prog(ts, 1.8) : 0;
            rings.forEach(function (c, r) { A.set(c, { cx: co[r][0], cy: co[r][1] }); op(c, r === 0 ? (K === 2 ? p2 : K >= 3 ? 1 : 0) : K >= 3 ? (K === 3 ? clamp(pr * 6 - r, 0, 1) : 1) : 0); });
            op(outT, K >= 3 ? 0.7 * (K === 3 ? pr : 1) : 0);
          }
        };
      }
    });
  })();

  /* ================= 6.2 reuse distance and reuse ratio ================= */
  (function () {
    var IJ = [[1, 1], [2, 0], [2, 1], [3, 0], [2, 2], [3, 1]], CH = 560;
    ANIM.reg('A:6.2', {
      title: '复用距离 D = R√(3N) 与复用比 q',
      cap: 'D 是最近两个同频小区的中心距（蓝色小区同频）。q = D/R = √(3N) 只跟 N 有关。N 越大 → q 越大、同频干扰越小，但每个小区分到的信道越少（以例题的 560 个双工信道为例）。',
      h: 236,
      init: function (A) {
        var R = 12, cx = 124, cy = 118, H = A.H;
        var cells = cellsWithin(8.2).filter(function (c) {
          var p = latXY(c.a, c.b, R, cx, cy); c.x = p[0]; c.y = p[1];
          return p[0] - S3 / 2 * R >= 2 && p[0] + S3 / 2 * R <= 246 && p[1] - R >= 2 && p[1] + R <= H - 2;
        });
        A.path(cells.map(function (c) { return hexD(c.x, c.y, R); }).join(''), 'f-card s-line w1');
        var co = A.path('', 'f-acc op5 s-acc w1');
        A.path(hexD(cx, cy, R), 'f-acc s-acc w1');
        A.line(cx, cy, cx, cy - R, 's-gold w3');
        var Dl = A.arrow(cx, cy, cx, cy, 's-bad w3', null, 7), Dt = A.text(0, 0, 'D', { cls: 't-b f-bad t-l', anchor: 'middle' });
        A.text(cx - 4, cy - 15, 'R', { cls: 't-b f-gold', anchor: 'end' });
        var x0 = 254, T = function (y, s, o) { return A.text(x0, y, s, o || {}); };
        var tN = T(26, '', { cls: 't-l t-b' }); T(48, 'D = R·√(3N)', { cls: 't-m' });
        var tD = T(66, '', { cls: 't-m f-bad' }), tQ = T(88, '', { cls: 't-b t-m' });
        T(118, '复用比 q（越大干扰越小）', { size: 10.5, cls: 'f-soft' });
        var bQ = A.rect(x0, 124, 0, 12, 'f-good', null, 2);
        T(156, '每小区信道 = ' + CH + ' ÷ N', { size: 10.5, cls: 'f-soft' });
        var bC = A.rect(x0, 162, 0, 12, 'f-gold', null, 2), tC = T(194, '', { cls: 't-b t-m' });
        T(222, 'N↑：质量↑ 容量↓', { cls: 't-b' });
        var maxQ = Math.sqrt(3 * 13), maxC = CH / 3;
        function draw(v) {
          var i = IJ[v][0], j = IJ[v][1], N = i * i + i * j + j * j, q = Math.sqrt(3 * N), lab = labeler(i, j), d = '';
          cells.forEach(function (c) { if (lab(c.a, c.b) === 0 && (c.a || c.b)) d += hexD(c.x, c.y, R); });
          co.setAttribute('d', d);
          var p = latXY(i, j, R, cx, cy);
          A.moveArrow(Dl, cx, cy, p[0], p[1]);
          var nx = -(p[1] - cy), ny = p[0] - cx, L = Math.hypot(nx, ny);
          A.set(Dt, { x: (cx + p[0]) / 2 + nx / L * 12, y: (cy + p[1]) / 2 + ny / L * 12 + 5 });
          A.setText(tN, 'N = ' + N + '  (i=' + i + ', j=' + j + ')');
          A.setText(tD, '= √' + (3 * N) + '·R = ' + q.toFixed(2) + ' R');
          A.setText(tQ, 'q = D/R = ' + q.toFixed(2));
          A.set(bQ, { width: 138 * q / maxQ });
          var per = CH / N;
          A.set(bC, { width: 138 * per / maxC });
          A.setText(tC, CH + ' ÷ ' + N + (per % 1 ? ' ≈ ' + per.toFixed(1) : ' = ' + per) + ' 个');
          A.note('相邻小区中心距 d = √3·R = ' + S3.toFixed(2) + 'R；D/d = √N = ' + Math.sqrt(N).toFixed(2));
        }
        A.choice({ label: '簇大小 N', options: IJ.map(function (q) { return String(q[0] * q[0] + q[0] * q[1] + q[1] * q[1]); }), value: 2, on: draw });
        draw(2);
        return {};
      }
    });
  })();

  /* ================= 6.2 (2) worked example: 560 duplex channels ================= */
  (function () {
    var BW = 30, ctl = 2, sp = 25, N = 7, voiceBW = BW - ctl, dir = voiceBW / 2, nCh = dir * 1000 / sp, per = nCh / N;
    ANIM.reg('A:6.2/2', {
      title: '例题：' + BW + ' MHz、N = ' + N + ' 的信道数',
      cap: 'FDD 系统：一个双工信道 = 上行一条 + 下行一条单工信道，所以带宽要先对半分再切。',
      h: 222, tween: 1.2, stepDur: 4.2,
      steps: [
        '总带宽 ' + BW + ' MHz，先刨掉 ' + ctl + ' MHz 控制信道：' + BW + ' − ' + ctl + ' = ' + voiceBW + ' MHz 给语音。',
        'FDD 双工要上、下行各一条，对称分：' + voiceBW + ' ÷ 2 = ' + dir + ' MHz 每个方向。',
        '每个方向按 ' + sp + ' kHz 一条切：' + (dir * 1000).toLocaleString('en') + ' kHz ÷ ' + sp + ' kHz = ' + nCh + ' 条单工信道。',
        '上行一条 + 下行一条 = 1 个双工信道，共 ' + nCh + ' 个；分给 ' + N + ' 个小区：' + nCh + ' ÷ ' + N + ' = ' + per + ' 个/小区。'
      ],
      init: function (A) {
        var bx = 20, bw = 360, sc = bw / BW;
        A.text(bx, 22, '总带宽 ' + BW + ' MHz', { cls: 't-b' });
        A.rect(bx, 30, bw, 22, 'f-accs s-acc w1', null, 2);
        var gC = A.g(); A.rect(bx, 30, ctl * sc, 22, 'f-gold', gC, 2);
        A.text(bx, 68, '控制 ' + ctl + ' MHz', { cls: 'f-gold t-b', size: 11 }, gC); A.text(380, 68, '语音 ' + voiceBW + ' MHz', { cls: 'f-acc t-b', anchor: 'end', size: 11 }, gC);
        var gS = A.g(), rows = [['上行 UL', 'gold', 90], ['下行 DL', 'acc', 122]], tk = [];
        rows.forEach(function (r) {
          A.text(bx, r[2] + 15, r[0], { cls: 't-b f-' + r[1], size: 11 }, gS);
          A.rect(bx + 56, r[2], dir * sc, 22, 'f-' + r[1] + 's s-' + r[1] + ' w1', gS, 2);
          A.text(bx + 62 + dir * sc, r[2] + 15, dir + ' MHz', { cls: 't-m', size: 11 }, gS);
          var d = ''; for (var i = 1; i < nCh; i++) d += 'M' + f1(bx + 56 + dir * sc * i / nCh) + ' ' + r[2] + 'v22';
          tk.push(A.path(d, 's-' + r[1] + ' w1', gS));
        });
        var tN = A.text(380, 164, '÷ ' + sp + ' kHz = ' + nCh + ' 条 / 方向', { cls: 't-b', anchor: 'end' });
        var gH = A.g(), R = 17, cx = 70, cy = 176;
        cellsWithin(S3 + 1e-6).forEach(function (c) { var p = latXY(c.a, c.b, R * 0.62, cx, cy); A.path(hexD(p[0], p[1], R * 0.62), 'f-card s-acc w1', gH); });
        A.text(130, 184, nCh + ' 个双工信道 ÷ ' + N + ' = ' + per + ' 个/小区', { cls: 't-l t-b f-good' }, gH);
        var K = 0;
        return {
          step: function (k) { K = k; },
          frame: function (ts) {
            var p = A.prog(ts, 0.8);
            op(gC, K === 0 ? p : 1); op(gS, K === 1 ? p : K > 1 ? 1 : 0);
            tk.forEach(function (t) { op(t, K >= 2 ? (K === 2 ? p * 0.3 : 0.3) : 0); });
            op(tN, K === 2 ? p : K > 2 ? 0.6 : 0); op(gH, K === 3 ? p : 0);
          }
        };
      }
    });
  })();
})();
