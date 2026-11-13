/* EE6129 Part 2 (Ser Wee) — chapter 6 (ISI & equalization) and chapter 7 (OFDM) animated figures.
   Page p2 = p2-learn.html. All numbers are computed below from the section's own examples. */
(function () {
  'use strict';
  /* ---------- shared helpers ---------- */
  function nm(x, d) {                       // number with a real minus sign, trailing zeros trimmed
    var v = +(+x).toFixed(d == null ? 2 : d);
    if (v === 0) v = 0;
    var s = String(v);
    return s.charAt(0) === '-' ? '−' + s.slice(1) : s;
  }
  function fx(x, d) {                       // fixed decimals, real minus sign
    var s = (+x).toFixed(d);
    if (+s === 0) s = (0).toFixed(d);
    return s.charAt(0) === '-' ? '−' + s.slice(1) : s;
  }
  function cplx(re, im, d) {
    d = d == null ? 2 : d;
    if (Math.abs(im) < 5e-4) return nm(re, d);
    if (Math.abs(re) < 5e-4) return nm(im, d) + 'j';
    return nm(re, d) + (im < 0 ? ' − ' : ' + ') + nm(Math.abs(im), d) + 'j';
  }
  function sinc(x) { return Math.abs(x) < 1e-9 ? 1 : Math.sin(Math.PI * x) / (Math.PI * x); }
  function mix(a, b, p) { var o = {}; for (var k in b) o[k] = a[k] + (b[k] - a[k]) * p; return o; }
  function copy(o) { var r = {}; for (var k in o) r[k] = o[k]; return r; }
  function tx(A, x, y, s, cls, anchor, parent, px) {   // text; px = font size via inline style (beats the CSS default)
    var e = A.text(x, y, s, { cls: cls || '', anchor: anchor }, parent);
    if (px) e.setAttribute('style', 'font-size:' + px + 'px');
    return e;
  }
  function op(e, v) { e.setAttribute('opacity', (+v).toFixed(2)); }
  var SUB = ['₀', '₁', '₂', '₃', '₄', '₅', '₆'];

  /* =====================================================================
     6.1  Nyquist pulses, ISI from a two-path channel, reading H(Z)
     ===================================================================== */
  (function () {
    var m = [1, -1, 1, 1];
    // per-step targets: ind = opacity of single pulses, sum = sum curve, a = echo gain, d = echo delay (symbols)
    var TG = [
      { ind: 1, sum: 0, a: 0, d: 1, box: 0 },
      { ind: 0.35, sum: 1, a: 0, d: 1, box: 1 },
      { ind: 0.35, sum: 1, a: 1, d: 1, box: 0 },
      { ind: 0.35, sum: 1, a: 1, d: 1, box: 1 },
      { ind: 0.35, sum: 1, a: 0.3, d: 1, box: 1 },
      { ind: 0.35, sum: 1, a: 0.6, d: 2, box: 1 }
    ];
    var L1 = [
      'ψ(t) = sinc(t/T)：在 t = nT（n ≠ 0）处为 0',
      'y(nT) = m[n]：没有 ISI',
      'h(t) = δ(t) + δ(t − T)：每个脉冲多一个回声',
      'y(nT) = m[n] + m[n − 1]',
      'r[n] = m[n] + 0.3m[n − 1] + w[n]',
      'r[n] = m[n] + 0.6m[n − 2] + w[n]'
    ];
    var L2 = [
      '发送 m = +1, −1, +1, +1（n = 0…3）',
      'Nyquist：g_{e}(nT − iT) = 1（n = i），0（n ≠ i）',
      'p(t) = sinc(t) + sinc(t − 1)',
      'm̂_{1} = m_{0} + m_{1} = ' + nm(m[0] + m[1]) + '　← ISI',
      'H(Z) = 1 + 0.3Z^{−1} → h = {1, 0.3}，L = 2',
      'H(Z) = 1 + 0.6Z^{−2} → h[1] = 1，h[2] = 0，h[3] = 0.6'
    ];
    ANIM.reg('p2:6.1', {
      title: 'Nyquist 脉冲与 ISI：回声晚一个符号',
      cap: '看什么：竖虚线是采样时刻 nT。sinc 脉冲在别人的采样点上正好为 0，所以采样值就是 m[n]；信道加了回声（金色）后，采样值里混进前面的符号，这就是 ISI。后两步练习从 H(Z) 读回声：Z 的次数 = 晚几个符号，系数 = 回声大小。',
      h: 246,
      stepDur: 4.2,
      steps: [
        '发射 sinc 脉冲 m<sub>n</sub>ψ(t − nT)：每个脉冲在自己的采样点为 m<sub>n</sub>，在别人的采样点为 0（绿点）。',
        '叠加后采样：y(nT) = m[n]，互不干扰。这就是 Nyquist 无 ISI 准则。',
        '经过信道 h(t) = δ(t) + δ(t − T)：每个脉冲后面多了一个晚 T 的回声（金色）。',
        '采样值变成 m[n] + m[n − 1]（红框）：例如 m̂<sub>1</sub> = m<sub>0</sub> + m<sub>1</sub> = 0，这就是 ISI。',
        '读 Z 变换：H(Z) = 1 + 0.3Z⁻¹ → 回声晚 1 个符号、大小 0.3：h = {1, 0.3}，L = 2。',
        'H(Z) = 1 + 0.6Z⁻² → 回声晚 2 个符号；没有 Z⁻¹ 项，所以 h[2] = 0。'
      ],
      init: function (A) {
        var ax = A.axes({ x: 30, y: 26, w: 350, h: 118, xr: [-1.2, 5.6], yr: [-1.7, 2.5],
          ticksX: [0, 1, 2, 3, 4, 5].map(function (n) { return { v: n, l: '' }; }), ticksY: [{ v: 1, l: '1' }, { v: -1, l: '−1' }] });
        var n, i;
        for (n = 0; n <= 5; n++) {
          A.line(ax.X(n), 22, ax.X(n), 148, 's-line w1 dash');
          tx(A, ax.X(n), 160, n + 'T', 't-s', 'middle');
        }
        tx(A, 4, 14, '蓝：发送脉冲', 'f-acc', null, null, 10.5);
        tx(A, 82, 14, '金：回声', 'f-gold', null, null, 10.5);
        tx(A, 136, 14, '黑：接收到的叠加波形', '', null, null, 10.5);
        var ind = [], ech = [];
        for (i = 0; i < 4; i++) { ind.push(A.path('', 's-acc w1 dash')); ech.push(A.path('', 's-gold w1 dash')); }
        var sum = A.path('', 's-ink w2');
        var dots = [];
        for (n = 0; n <= 5; n++) dots.push(A.circle(0, 0, 3.4, 'f-good'));
        tx(A, 4, 186, '采样值', 't-s');
        var boxes = [];
        for (n = 0; n <= 5; n++) {
          var g = A.g();
          var rc = A.rect(ax.X(n) - 19, 172, 38, 20, 'f-card s-line w1', g, 4);
          var tt = tx(A, ax.X(n), 186, '', 't-m', 'middle', g);
          boxes.push({ g: g, r: rc, t: tt });
        }
        var t1 = tx(A, 200, 214, '', 't-m', 'middle');
        var t2 = tx(A, 200, 236, '', '', 'middle');
        var cur = copy(TG[0]), from = copy(TG[0]), K = 0;
        function pulse(i, t, P) { return m[i] * sinc(t - i); }
        function echo(i, t, P) { return P.a * m[i] * sinc(t - i - P.d); }
        function S(t, P) { var s = 0; for (var i = 0; i < 4; i++) s += pulse(i, t, P) + echo(i, t, P); return s; }
        return {
          step: function (k) { from = copy(cur); K = k; A.setText(t1, L1[k]); A.setText(t2, L2[k]); },
          frame: function (ts, dt, k) {
            var P = mix(from, TG[k], A.prog(ts, 1.1));
            cur = P;
            for (var i = 0; i < 4; i++) {
              A.setCurve(ind[i], ax, function (t) { return pulse(i, t, P); }, 140);
              op(ind[i], i === 1 && k === 0 ? 1 : P.ind);
              A.set(ind[i], { cls: i === 1 && k === 0 ? 's-acc w2' : 's-acc w1 dash' });
              A.setCurve(ech[i], ax, function (t) { return echo(i, t, P); }, 140);
              op(ech[i], Math.min(1, P.a * 3) * 0.9);
            }
            A.setCurve(sum, ax, function (t) { return S(t, P); }, 220);
            op(sum, P.sum);
            for (var n = 0; n <= 5; n++) {
              var y = k === 0 ? pulse(1, n, P) : S(n, P);
              A.set(dots[n], { cx: ax.X(n), cy: ax.Y(y) });
              var want = n < 4 ? m[n] : 0, isi = Math.abs(y - want) > 0.01;
              A.set(dots[n], { cls: k === 0 ? 'f-good' : (isi ? 'f-bad' : 'f-good') });
              A.setText(boxes[n].t, nm(y, 2));
              A.set(boxes[n].r, { cls: isi ? 'f-bads s-bad w1' : 'f-card s-line w1' });
              op(boxes[n].g, P.box);
            }
          }
        };
      }
    });
  })();

  /* =====================================================================
     6.2  MLSE / Viterbi trellis (BPSK, channel memory L = 2 → 4 states)
     ===================================================================== */
  (function () {
    var h = [1, 0.5, 0.3];
    var m = [1, -1, -1, 1, 1, 1];
    var w = [-0.3, -0.4, 0, -0.4, 0, -0.4];
    var full = [1, 1].concat(m), r = [], n, i;
    for (n = 0; n < 6; n++) r.push(+(full[n + 2] + h[1] * full[n + 1] + h[2] * full[n] + w[n]).toFixed(2));
    var S = [[1, 1], [1, -1], [-1, 1], [-1, -1]];            // state = (m[n], m[n−1])
    function sidx(a, b) { for (var j = 0; j < 4; j++) if (S[j][0] === a && S[j][1] === b) return j; return -1; }
    var met = [0, Infinity, Infinity, Infinity], br = [], best = [];
    for (n = 0; n < 6; n++) {
      var nmet = [Infinity, Infinity, Infinity, Infinity], bi = [-1, -1, -1, -1];
      for (var f = 0; f < 4; f++) {
        if (!isFinite(met[f])) continue;
        [1, -1].forEach(function (c) {
          var to = sidx(c, S[f][0]);
          var e = r[n] - (c + h[1] * S[f][0] + h[2] * S[f][1]);
          var b = { n: n, from: f, to: to, acc: met[f] + e * e, surv: false, path: false };
          br.push(b);
          if (b.acc < nmet[to]) { nmet[to] = b.acc; bi[to] = br.length - 1; }
        });
      }
      bi.forEach(function (j) { if (j >= 0) br[j].surv = true; });
      best.push(bi); met = nmet;
    }
    var end = 0;
    for (i = 1; i < 4; i++) if (met[i] < met[end]) end = i;
    var dec = [], st = end;
    for (n = 5; n >= 0; n--) { var bb = br[best[n][st]]; bb.path = true; dec[n] = S[st][0]; st = bb.from; }
    var sg = r.map(function (x) { return x >= 0 ? 1 : -1; });
    var errN = -1; for (n = 0; n < 6; n++) if (sg[n] !== m[n]) errN = n + 1;
    var finalMet = met;
    function pm(v) { return v > 0 ? '+1' : '−1'; }

    ANIM.reg('p2:6.2', {
      title: 'MLSE 的维特比算法：只留幸存路径',
      cap: '看什么：每一列是一个时刻 n，每一行是一个状态 (m[n], m[n−1])。两条支路汇到同一状态时只留累计距离 Σ(r − 无噪声输出)² 小的那条，复杂度从 M<sup>K</sup> 降到每步 M<sup>L</sup> 个状态。本例信道 r[n] = m[n] + 0.5m[n−1] + 0.3m[n−2] + w[n]。',
      h: 246,
      stepDur: 4.2,
      tween: 3.6,
      steps: [
        '穷举：6 个 ±1 符号有 2⁶ = 64 种序列；K 个 M 进制符号是 M<sup>K</sup> 种，K 一大就算不动。',
        '信道记忆 L = 2：输出只取决于最近 2 个符号，所以状态 = (m[n], m[n−1])，共 2² = 4 个。',
        '从已知状态 (+,+) 出发，每个状态分出两条支路（下一个符号 +1 或 −1），支路距离 = (r − 无噪声输出)²。',
        '两条支路汇到同一状态时，只留累计距离小的（蓝，幸存路径），另一条剪掉（红虚线）。',
        '最后选累计距离最小的状态回溯（绿）：6 个全对；逐个 sgn(r) 判决在 n = ' + errN + ' 判错（红）。'
      ],
      init: function (A) {
        function X(n) { return 84 + n * 47; }
        function Y(s) { return 46 + s * 40; }
        var lab = ['(+,+)', '(+,−)', '(−,+)', '(−,−)'], labs = [];
        for (var s = 0; s < 4; s++) labs.push(tx(A, 62, Y(s) + 4, lab[s], 't-m', 'end'));
        tx(A, 62, 22, 'r[n]', 't-s', 'end');
        var rt = [];
        for (var n = 1; n <= 6; n++) { rt.push(tx(A, X(n), 22, nm(r[n - 1], 2), 't-m', 'middle')); tx(A, X(n), 34, 'n=' + n, 't-xs', 'middle'); }
        var lines = br.map(function (b) { return A.line(X(b.n), Y(b.from), X(b.n + 1), Y(b.to), 's-line w1'); });
        var nodes = [];
        for (n = 0; n <= 6; n++) for (s = 0; s < 4; s++) nodes.push(A.circle(X(n), Y(s), 4, 'f-card s-soft w1'));
        var rowY = [196, 214, 232], rowL = ['发送 m', 'sgn(r) 判决', 'Viterbi 判决'], rowsT = [];
        for (var j = 0; j < 3; j++) {
          tx(A, 62, rowY[j], rowL[j], 't-s', 'end');
          var arr = [];
          for (n = 1; n <= 6; n++) {
            var v = j === 0 ? m[n - 1] : j === 1 ? sg[n - 1] : dec[n - 1];
            arr.push(tx(A, X(n), rowY[j], pm(v), 't-m ' + (j > 0 && v !== m[n - 1] ? 'f-bad t-b' : j === 2 ? 'f-good' : ''), 'middle'));
          }
          rowsT.push(arr);
        }
        var fm = [];
        for (s = 0; s < 4; s++) fm.push(tx(A, X(6) + 8, Y(s) + 4, nm(finalMet[s], 2), 't-xs t-m'));
        function rowOp(j, v) { rowsT[j].forEach(function (e) { op(e, v); }); }
        return {
          step: function () {},
          frame: function (ts, dt, k) {
            labs.forEach(function (e) { A.set(e, { cls: 't-m' + (k === 1 ? ' f-gold t-b' : '') }); });
            for (var n = 0; n <= 6; n++) for (var s = 0; s < 4; s++) {
              var reach = n >= 2 || (n === 0 && s === 0) || (n === 1 && (s === 0 || s === 2));
              A.set(nodes[n * 4 + s], { cls: k >= 1 && reach ? 'f-card s-acc w1' : 'f-card s-faint w1', r: k === 4 && n === 6 && s === end ? 6 : 4 });
              if (k === 4 && n === 6 && s === end) A.set(nodes[n * 4 + s], { cls: 'f-good s-good w1' });
            }
            br.forEach(function (b, i) {
              var L = lines[i], cls = 's-line w1', o = 1;
              if (k <= 1) { cls = 's-faint w1'; o = 0.35; }
              else if (k === 2) {
                if (b.n < 2) { cls = 's-acc w2'; o = A.prog(ts, 0.6, b.n * 0.6); } else { cls = 's-faint w1'; o = 0.35; }
              } else {
                var p = b.n < 2 ? 1 : A.clamp((ts - (b.n - 2) * 0.75) / 0.5, 0, 1);
                if (k === 4) p = 1;
                if (b.n >= 2 && p < 1) { cls = 's-faint w1'; o = 0.35 + 0.65 * p; }
                else if (b.surv) cls = 's-acc w2';
                else { cls = 's-bad w1 dash'; o = k === 4 ? 0.25 : 0.7; }
                if (k === 4 && b.path) { cls = 's-good w4'; o = 1; }
                if (k === 4 && !b.path && b.surv) o = 0.45;
              }
              A.set(L, { cls: cls }); op(L, o);
            });
            rowOp(0, 1); rowOp(1, k === 4 ? 1 : 0); rowOp(2, k === 4 ? A.prog(ts, 0.8, 0.3) : 0);
            fm.forEach(function (e) { op(e, k >= 3 ? (k === 3 ? A.clamp((ts - 3) / 0.5, 0, 1) : 1) : 0); });
          }
        };
      }
    });
  })();

  /* =====================================================================
     6.3  ZF by long division  C(z) = 1/H(z),  H(z) = 1 + 0.3z⁻¹ + 0.1z⁻²
     ===================================================================== */
  (function () {
    var H = [1, 0.3, 0.1], NP = 5, rows = [], c = [], rem = [1, 0, 0, 0, 0], k, i;
    rows.push({ lab: '被除数 1', v: [1, null, null, null, null], kind: 'd' });
    function term(v, p) { return nm(v, 3) + (p ? 'z^{−' + p + '}' : ''); }
    for (k = 0; k < 3; k++) {
      var ck = +rem[k].toFixed(6); c.push(ck);
      var sub = [null, null, null, null, null];
      for (i = 0; i < H.length; i++) if (k + i < NP) sub[k + i] = +(ck * H[i]).toFixed(6);
      rem = rem.map(function (r, j) { return +(r - (sub[j] || 0)).toFixed(6); });
      rows.push({ lab: '减 ' + (k ? '(' + term(ck, k) + ')' : '1') + '·H', v: sub, kind: 's' });
      rows.push({ lab: '余数', v: rem.map(function (r, j) { return j <= k || (Math.abs(r) < 1e-9 && j > k + 2) ? null : r; }), kind: 'r' });
    }
    var c3 = rem[3];                       // next coefficient (shown in step 4 text)
    var q = [0, 0, 0, 0];                  // Q(z) = H(z)(c0 + c1 z^-1): two-tap truncation
    for (i = 0; i < 3; i++) for (k = 0; k < 2; k++) q[i + k] += H[i] * c[k];
    q = q.map(function (v) { return +v.toFixed(6); });
    var sc2 = c[0] * c[0] + c[1] * c[1];
    function poly(v) {
      var s = '';
      v.forEach(function (x, p) {
        if (Math.abs(x) < 1e-9) return;
        var a = nm(Math.abs(x), 3) + (p ? 'z⁻' + '¹²³⁴'.charAt(p - 1) : '');
        s += s ? (x < 0 ? ' − ' : ' + ') + a : (x < 0 ? '−' : '') + a;
      });
      return s;
    }
    var r1 = rows[2].v.map(function (x) { return x || 0; }), r2 = rows[4].v.map(function (x) { return x || 0; });
    ANIM.reg('p2:6.3', {
      title: '迫零均衡：长除法求 C(z) = 1/H(z)',
      cap: '看什么：表格按 z 的次数分列，同一列才能相减（z⁻¹ 和 z⁻² 不能相加）。每一步：余数的第一项就是商的下一项，乘回 H(z) 再减。最后两步看只取两个抽头时剩下的残余 ISI 和噪声增强。',
      h: 290,
      stepDur: 4.4,
      steps: [
        '目标 H(z)C(z) = 1。H(z) = 1 + 0.3z⁻¹ + 0.1z⁻²，按 z 的次数分列，同一列才能相减。',
        '商第一项 c₀ = ' + nm(c[0]) + '：1 − 1·H(z) = ' + poly(r1) + '。',
        '余数第一项给出 c₁ = ' + nm(c[1], 3) + '：减去 (' + nm(c[1], 3) + 'z⁻¹)·H(z)，余数 ' + poly(r2) + '。',
        'c₂ = ' + nm(c[2], 3) + '，余数 ' + poly(rem) + '，越来越小。捷径：c₂ = −0.3c₁ − 0.1c₀。',
        '只取两个抽头 {1, ' + nm(c[1]) + '}：Q(z) = HC = ' + poly(q) + '，剩残余 ISI。',
        '噪声也要过均衡器：σ′² = σ²(1² + 0.3²) = ' + nm(sc2) + 'σ²。是系数平方和，不是 (Σc)²。'
      ],
      init: function (A) {
        function CX(p) { return 140 + p * 54; }
        var pw = ['z^{0}', 'z^{−1}', 'z^{−2}', 'z^{−3}', 'z^{−4}'];
        for (var p = 0; p < 5; p++) tx(A, CX(p), 20, pw[p], 't-s', 'middle');
        A.line(8, 27, 392, 27, 's-line w1');
        tx(A, 8, 44, '商 C(z) 的系数', 't-s t-b');
        var qc = [];
        for (p = 0; p < 3; p++) {
          var g = A.g();
          A.rect(CX(p) - 24, 31, 48, 19, 'f-golds s-gold w1', g, 5);
          tx(A, CX(p), 45, nm(c[p], 3), 't-m t-b', 'middle', g);
          qc.push(g);
        }
        var dots = tx(A, CX(3), 45, '+ …', 't-m', 'middle');
        A.line(8, 55, 392, 55, 's-line w1');
        var RY = [72, 90, 110, 128, 148, 166, 186], RG = [];
        rows.forEach(function (row, j) {
          var g = A.g();
          tx(A, 8, RY[j], row.lab, 't-s', null, g);
          row.v.forEach(function (v, p) {
            if (v == null) return;
            tx(A, CX(p), RY[j], nm(v, 3), 't-m' + (row.kind === 'r' ? ' t-b' : ''), 'middle', g);
          });
          if (row.kind === 's') A.line(112, RY[j] + 6, 392, RY[j] + 6, 's-soft w1', g);
          RG.push(g);
        });
        var hi = A.rect(110, 0, 284, 18, 'f-accs s-acc w1', null, 4);
        hi.parentNode.insertBefore(hi, RG[0]);
        // bottom: two-tap residual ISI
        var bot = A.g();
        tx(A, 8, 204, '只用两个抽头 {1, ' + nm(c[1]) + '}：Q(z) = H(z)C(z)', 't-s t-b', null, bot);
        A.line(112, 258, 392, 258, 's-soft w1', bot);
        for (p = 0; p < 4; p++) {
          var y1 = 258 - 30 * q[p];
          A.line(CX(p), 258, CX(p), y1, p === 0 ? 's-good w3' : 's-bad w3', bot);
          A.circle(CX(p), y1, 3, p === 0 ? 'f-good' : 'f-bad', bot);
          tx(A, CX(p), q[p] >= 0.5 ? y1 - 6 : 250 - (q[p] < 0 ? 0 : 0), nm(q[p], 3), 't-m' + (p ? ' f-bad' : ''), 'middle', bot);
        }
        tx(A, 8, 248, 'q₀ 想要，其余 = 残余 ISI', 't-xs', null, bot);
        var noise = tx(A, 200, 280, '噪声 σ′² = σ²(1² + ' + nm(Math.abs(c[1])) + '²) = ' + nm(sc2) + 'σ² > σ²', 't-m f-bad', 'middle');
        var K = 0;
        return {
          step: function (k) { K = k; },
          frame: function (ts, dt, k) {
            for (var p = 0; p < 3; p++) op(qc[p], p < k ? (p === k - 1 && k <= 3 ? A.prog(ts, 0.5) : 1) : 0);
            op(dots, k >= 4 ? 1 : 0);
            for (var j = 0; j < rows.length; j++) {
              var need = j === 0 ? 0 : Math.ceil(j / 2);                    // row j shows from step need
              var o = k > need || (k >= 4) ? 1 : k === need ? (j === 0 ? 1 : A.prog(ts, 0.6, j % 2 ? 0.3 : 1.0)) : 0;
              if (need > 3) o = 0;
              op(RG[j], k >= 4 ? 0.55 : o);
            }
            if (k >= 1 && k <= 3) { A.set(hi, { y: RY[2 * k] - 13 }); op(hi, A.prog(ts, 0.5, 1.0) * 0.9); } else op(hi, 0);
            op(bot, k >= 4 ? A.prog(ts, 0.7) : 0);
            op(noise, k >= 5 ? A.prog(ts, 0.7) : 0);
          }
        };
      }
    });
  })();

  /* =====================================================================
     6.3/2  Residual ISI → Pe = ½[Q((1−a)/σ′) + Q((1+a)/σ′)]  (final Q2(a) every year)
     ===================================================================== */
  (function () {
    var PRE = [
      { l: '23-24', a: 0.36, s: Math.sqrt(0.3 * 1.36), src: '√(0.3 × 1.36)', isi: 'y[i] = m[i] − 0.36m[i−4] + w′[i]' },
      { l: '24-25', a: 0.6, s: Math.sqrt(0.64), src: '√0.64', isi: 'y<sub>i</sub> = s<sub>i</sub> + 0.6s<sub>i−1</sub> + w′<sub>i</sub>' },
      { l: '25-26 S1', a: 0.3, s: Math.sqrt(0.36), src: '√0.36', isi: 'r[n] = m[n] + 0.3m[n−1] + w(n)（不均衡）' },
      { l: '25-26 S2', a: 0.2, s: Math.sqrt(0.25 * 2.56), src: '√(0.25 × 2.56)', isi: 'y[n] = m(n) + 0.2m(n−1) + w′(n)' }
    ];
    ANIM.reg('p2:6.3/2', {
      title: '残余 ISI 下的误码率：分两种情况再平均',
      cap: '看什么：发 +1 时，前一个符号的残余 ISI 把判决量推到 1 + a 或 1 − a，各占一半；红色面积（y < 0）就是出错概率。按钮是四年期末 Q2(a) 的数字，也可以自己拖 a 和 σ′。注意 Q 里除的是标准差 σ′。',
      h: 246,
      stepDur: 4.4,
      steps: [
        '判决量 y = m[n] + a·m[n−1] + w′，按 sgn(y) 判决。设发 +1，y < 0 就错。',
        '先算 σ′：均衡器输出噪声方差 σ′² = σ²Σc²，再开根号（题目给的 0.25、0.36、0.64 都是方差）。',
        '若 m[n−1] = +1（蓝）：均值 1 + a，离门限 0 远，出错概率 Q((1 + a)/σ′) 很小。',
        '若 m[n−1] = −1（金）：均值 1 − a，离门限近，Q((1 − a)/σ′) 大得多。',
        '两种情况各占 ½：Pe = ½[Q((1 − a)/σ′) + Q((1 + a)/σ′)]。发 −1 由对称性结果一样。'
      ],
      init: function (A) {
        var a = PRE[0].a, s = PRE[0].s, pre = 0, lock = false, K = 0;
        var ax = A.axes({ x: 26, y: 30, w: 354, h: 132, xr: [-1.5, 2.9], yr: [0, 1.15], xl: 'y',
          ticksX: [{ v: -1, l: '−1' }, { v: 0, l: '0' }, { v: 1, l: '1' }, { v: 2, l: '2' }] });
        A.line(ax.X(0), 26, ax.X(0), 162, 's-bad w2 dash');
        tx(A, ax.X(0) - 4, 40, '门限 0', 'f-bad', 'end', null, 10.5);
        tx(A, ax.X(0) - 4, 54, 'y < 0 → 判错', 'f-bad', 'end', null, 10.5);
        tx(A, 4, 14, '蓝：m[n−1] = +1', 'f-acc', null, null, 10.5);
        tx(A, 104, 14, '金：m[n−1] = −1', 'f-gold', null, null, 10.5);
        tx(A, 206, 14, '红：出错面积', 'f-bad', null, null, 10.5);
        var tailB = A.path('', 'f-bads s-bad w1'), tailG = A.path('', 'f-bads s-bad w1');
        var pB = A.path('', 's-acc w2'), pG = A.path('', 's-gold w2');
        var one = A.circle(0, 0, 3.5, 'f-ink'), arrB = A.arrow(0, 0, 1, 0, 's-acc w2', null, 5), arrG = A.arrow(0, 0, 1, 0, 's-gold w2', null, 5);
        var mB = A.circle(0, 0, 3.5, 'f-acc'), mG = A.circle(0, 0, 3.5, 'f-gold');
        var lB = tx(A, 0, 188, '1 + a', 'f-acc', 'middle', null, 10.5), lG = tx(A, 0, 188, '1 − a', 'f-gold', 'middle', null, 10.5);
        var sigBar = A.g(), sbL = A.line(0, 0, 0, 0, 's-pur w2', sigBar), sbT = tx(A, 0, 0, 'σ′', 'f-pur', 'middle', sigBar, 10.5);
        var f1 = tx(A, 200, 212, 'Pe = ½[Q((1 − a)/σ′) + Q((1 + a)/σ′)]', 't-m', 'middle');
        var f2 = tx(A, 200, 234, '', 't-m t-b', 'middle');
        var ch = A.choice({ label: '期末题', options: PRE.map(function (p) { return p.l; }), value: 0, on: function (i) {
          pre = i; a = PRE[i].a; s = PRE[i].s; lock = true; sa.set(a); ss.set(+s.toFixed(3)); lock = false; A.redraw(); } });
        var sa = A.slider({ label: '残余 ISI a', min: 0, max: 0.9, step: 0.01, value: a, fmt: function (v) { return nm(v, 2); },
          on: function (v) { if (lock) return; a = v; pre = -1; ch.set(-1, true); A.redraw(); } });
        var ss = A.slider({ label: 'σ′', min: 0.2, max: 1.2, step: 0.001, value: +s.toFixed(3), fmt: function (v) { return v.toFixed(3); },
          on: function (v) { if (lock) return; s = v; pre = -1; ch.set(-1, true); A.redraw(); } });
        function pdf(mu) { return function (y) { var z = (y - mu) / s; return Math.exp(-z * z / 2); }; }
        function tail(path, mu) {
          var pts = [[ax.X(-1.5), ax.Y(0)]], f = pdf(mu);
          for (var i = 0; i <= 60; i++) { var y = -1.5 + 1.5 * i / 60; pts.push([ax.X(y), ax.Y(f(y))]); }
          pts.push([ax.X(0), ax.Y(0)]);
          A.set(path, { d: A.pts(pts) + 'Z' });
        }
        return {
          step: function (k) { K = k; },
          frame: function (ts, dt, k) {
            var QB = A.Q((1 + a) / s), QG = A.Q((1 - a) / s), Pe = 0.5 * (QB + QG);
            A.setCurve(pB, ax, pdf(1 + a), 200); A.setCurve(pG, ax, pdf(1 - a), 200);
            tail(tailB, 1 + a); tail(tailG, 1 - a);
            var y0 = ax.Y(0);
            A.set(one, { cx: ax.X(1), cy: y0 });
            A.moveArrow(arrB, ax.X(1), y0 - 8, ax.X(1 + a), y0 - 8);
            A.moveArrow(arrG, ax.X(1), y0 - 8, ax.X(1 - a), y0 - 8);
            A.set(mB, { cx: ax.X(1 + a), cy: y0 }); A.set(mG, { cx: ax.X(1 - a), cy: y0 });
            A.set(lB, { x: ax.X(1 + a) + (a < 0.18 ? 14 : 0) }); A.set(lG, { x: ax.X(1 - a) - (a < 0.18 ? 14 : 0) });
            var yy = ax.Y(Math.exp(-0.5));
            A.set(sbL, { x1: ax.X(1 + a), y1: yy, x2: ax.X(1 + a + s), y2: yy });
            A.set(sbT, { x: ax.X(1 + a + s / 2), y: yy - 4 });
            var showB = k >= 2 ? 1 : k === 1 ? 0.35 : 0, showG = k >= 3 ? 1 : k === 1 ? 0.35 : 0;
            if (k === 2) showB = A.prog(ts, 0.6); if (k === 3) showG = A.prog(ts, 0.6);
            op(pB, showB); op(pG, k === 2 ? 0.25 : showG);
            op(tailB, k >= 2 ? showB : 0); op(tailG, k >= 3 ? showG : 0);
            op(sigBar, k === 1 ? 1 : 0);
            op(f1, k >= 4 ? 1 : 0); op(f2, k >= 4 ? 1 : 0);
            A.setText(f2, '= ½[Q(' + fx((1 - a) / s, 2) + ') + Q(' + fx((1 + a) / s, 2) + ')] ≈ ' + A.fmt(Pe, 3));
            var P = pre >= 0 ? PRE[pre] : null;
            var line1 = (P ? P.isi + '<br>' : '') + 'σ′ = ' + (P ? P.src + ' = ' : '') + nm(s, 3);
            var notes = [line1,
              line1,
              line1 + '<br>Q((1 + a)/σ′) = Q(' + fx((1 + a) / s, 2) + ') = ' + A.fmt(QB, 3),
              line1 + '<br>Q((1 + a)/σ′) = Q(' + fx((1 + a) / s, 2) + ') = ' + A.fmt(QB, 3) + '<br>Q((1 − a)/σ′) = Q(' + fx((1 - a) / s, 2) + ') = ' + A.fmt(QG, 3),
              line1 + '<br>Pe = ½(' + A.fmt(QG, 3) + ' + ' + A.fmt(QB, 3) + ') ≈ ' + A.fmt(Pe, 3) + '<br>（对比：没有 ISI 时 Q(1/σ′) = ' + A.fmt(A.Q(1 / s), 3) + '）'];
            A.note(k === 0 ? 'a = ' + nm(a) + '：残余 ISI 系数（符号不影响结果）' : notes[k]);
          }
        };
      }
    });
  })();

  /* =====================================================================
     6.4  DFE: feedback subtracts the decided past symbol; error propagation
     ===================================================================== */
  (function () {
    var Aseq = [1, -1, 1, -1, -1, 1], z = [0.2, -0.3, -1.2, 0.2, 0.3, -0.1];
    var rowsV = [], pa = 1, pd = 1, n;
    for (n = 0; n < 6; n++) {
      var y = Aseq[n] + 0.5 * pa + z[n], fb = -0.5 * pd, u = y + fb, d = u >= 0 ? 1 : -1;
      rowsV.push({ A: Aseq[n], y: y, fb: fb, u: u, d: d, prevWrong: pd !== pa });
      pa = Aseq[n]; pd = d;
    }
    var p1 = ANIM.util.Q(1), p2 = 0.5 * ANIM.util.Q(2) + 0.25, pSS = p1 / (1 - p2 + p1);
    var pLin = 0.5 * ANIM.util.Q(1.5) + 0.5 * ANIM.util.Q(0.5);
    var e3 = rowsV[2], e4 = rowsV[3];
    function pm(v) { return v > 0 ? '+1' : '−1'; }
    ANIM.reg('p2:6.4', {
      title: 'DFE：用已判决的符号减掉过去的 ISI',
      cap: '看什么：反馈支路把上一个判决 Â<sub>n−1</sub> 乘 ½ 后减掉（本例前馈滤波器 = 1）。判对时 ISI 消得干干净净、噪声不被放大；判错一次，下一次减的是错的 ISI，干扰反而加倍，这就是错误传播。例题来自 Practice 6 第 3 题：y<sub>n</sub> = A<sub>n</sub> + ½A<sub>n−1</sub> + z<sub>n</sub>，噪声方差 1。',
      h: 290,
      stepDur: 4.4,
      steps: [
        '结构：前馈滤波器压制未来符号的 ISI；反馈滤波器用已判决的 Â 重构过去的 ISI 并减掉。',
        '判对时 u<sub>n</sub> = y<sub>n</sub> − ½Â<sub>n−1</sub> = A<sub>n</sub> + z<sub>n</sub>：ISI 全消，噪声也不放大。',
        'n = 3：噪声 z = ' + nm(z[2], 1) + ' 太大，u = ' + nm(e3.u, 1) + '，判成 ' + pm(e3.d) + '，判错了（红）。',
        'n = 4：反馈减的是错的 ISI，u = A<sub>n</sub> + A<sub>n−1</sub> + z = ' + nm(e4.u, 1) + '，又判错——错误传播。',
        '连续判对后恢复。稳态 p = (1 − p)·' + nm(p1, 3) + ' + p·' + nm(p2, 3) + ' → p = ' + nm(pSS, 3) + '，比线性 ' + nm(pLin, 3) + ' 好。'
      ],
      init: function (A) {
        // block diagram
        var y0 = 34;
        tx(A, 6, y0 + 4, 'y_{n}', 't-m');
        A.arrow(26, y0, 50, y0, 's-ink w1', null, 5);
        var bF = A.rect(50, y0 - 12, 70, 24, 'f-card s-acc w1', null, 5);
        tx(A, 85, y0 + 4, '前馈 = 1', '', 'middle', null, 11);
        A.arrow(120, y0, 146, y0, 's-ink w1', null, 5);
        A.circle(156, y0, 10, 'f-card s-ink w1'); tx(A, 156, y0 + 4, 'Σ', '', 'middle');
        A.arrow(166, y0, 192, y0, 's-ink w1', null, 5);
        tx(A, 178, y0 - 6, 'u_{n}', 't-s', 'middle');
        A.rect(192, y0 - 12, 62, 24, 'f-card s-ink w1', null, 5);
        tx(A, 223, y0 + 4, '判决 sgn', '', 'middle', null, 11);
        A.arrow(254, y0, 296, y0, 's-ink w1', null, 5);
        tx(A, 300, y0 + 4, 'Â_{n}', 't-m');
        var fbG = A.g();
        A.path('M272 ' + y0 + 'V78H252', 's-pur w2', fbG);
        A.rect(178, 66, 74, 24, 'f-purs s-pur w1', fbG, 5);
        tx(A, 215, 82, '反馈 ½z^{−1}', 'f-pur', 'middle', fbG, 11);
        A.path('M178 78H156V' + (y0 + 14), 's-pur w2', fbG);
        A.arrow(156, 60, 156, y0 + 10, 's-pur w2', fbG, 5);
        tx(A, 146, 64, '−', 'f-pur t-b', 'end', fbG);
        tx(A, 282, 64, 'Â_{n−1}', 'f-pur', null, fbG, 11);
        // table
        function CX(n) { return 128 + n * 50; }
        var RY = [116, 134, 152, 170, 188, 206], RL = ['n', '发送 A_{n}', '收到 y_{n}', '减 ½Â_{n−1}', 'u_{n}', '判决 Â_{n}'];
        RL.forEach(function (l, j) { tx(A, 8, RY[j], l, j ? 't-s' : 't-s t-b'); });
        A.line(8, 106, 392, 106, 's-line w1'); A.line(8, 194 + 0, 392, 194, 's-line w1');
        var cols = [];
        rowsV.forEach(function (v, i) {
          var g = A.g();
          var bg = A.rect(CX(i) - 22, 105, 44, 108, 'f-none s-none', g, 5);
          tx(A, CX(i), RY[0], String(i + 1), 't-b', 'middle', g);
          tx(A, CX(i), RY[1], pm(v.A), 't-m', 'middle', g);
          tx(A, CX(i), RY[2], nm(v.y, 1), 't-m', 'middle', g);
          tx(A, CX(i), RY[3], (v.fb > 0 ? '+' : '') + nm(v.fb, 1), 't-m ' + (v.prevWrong ? 'f-bad' : 'f-pur'), 'middle', g);
          tx(A, CX(i), RY[4], nm(v.u, 1), 't-m t-b', 'middle', g);
          tx(A, CX(i), RY[5], pm(v.d), 't-m t-b ' + (v.d === v.A ? 'f-good' : 'f-bad'), 'middle', g);
          cols.push({ g: g, bg: bg, ok: v.d === v.A, pw: v.prevWrong });
        });
        var b1 = tx(A, 200, 232, '', '', 'middle'), b2 = tx(A, 200, 252, '', '', 'middle'), b3 = tx(A, 200, 274, '', 't-b', 'middle');
        var show = [0, 2, 3, 4, 6];
        var BT = [
          ['前馈：线性压制未来符号的 ISI', '反馈：减掉已判决的过去符号的 ISI', ''],
          ['上次判对：u = A_{n} + z_{n}，错误概率 Q(1) = ' + nm(p1, 3), '和没有 ISI 一样，噪声没被放大', ''],
          ['z_{3} = ' + nm(z[2], 1) + '：u = ' + nm(e3.u, 1) + ' < 0 → 判错', '这个错误会被反馈到下一个符号', ''],
          ['上次判错：减的 ISI 符号反了，u = A_{n} + A_{n−1} + z_{n}', '幅度 2 或 0：出错概率 ½Q(2) + ½·½ = ' + nm(p2, 3), ''],
          ['p = Q(1) / (1 − ' + nm(p2, 3) + ' + Q(1)) = ' + nm(pSS, 3), '无错误传播时 ' + nm(p1, 3) + '；线性（q = 0）½Q(1.5) + ½Q(0.5) = ' + nm(pLin, 3), 'DFE 更好，但错误传播吃掉一部分优势']
        ];
        return {
          step: function (k) { A.setText(b1, BT[k][0]); A.setText(b2, BT[k][1]); A.setText(b3, BT[k][2]); },
          frame: function (ts, dt, k) {
            cols.forEach(function (c, i) {
              var vis = i < show[k] ? 1 : 0;
              if (vis && i >= (k ? show[k - 1] : 0)) vis = A.prog(ts, 0.6, (i - (k ? show[k - 1] : 0)) * 0.4);
              op(c.g, vis);
              var cur = (k === 2 && i === 2) || (k === 3 && i === 3);
              A.set(c.bg, { cls: cur ? (c.ok ? 'f-goods s-good w1' : 'f-bads s-bad w1') : (!c.ok && k >= 2 ? 'f-bads s-none' : 'f-none s-none') });
            });
            A.set(fbG.firstChild, { cls: k === 3 ? 's-bad w2' : 's-pur w2' });
            op(fbG, k === 0 ? 0.5 + 0.5 * Math.abs(Math.sin(ts * 3)) : 1);
            A.set(bF, { cls: k === 0 ? 'f-accs s-acc w2' : 'f-card s-acc w1' });
          }
        };
      }
    });
  })();

  /* =====================================================================
     6.5  LS channel estimation with a training sequence (★ 了解)
     ===================================================================== */
  ANIM.reg('p2:6.5', {
    title: '训练序列做信道估计：Ĥ = YX†',
    cap: '看什么：每一帧开头有一段双方都知道的训练序列 X，接收端由 Y = HX + V 反解出 Ĥ（蓝点），散在真值 H（绿叉）周围。训练功率 P 越大，点越集中；发射天线 N 越多，总功率分得越散，MSE ∝ N²。',
    h: 220,
    seed: 6129,
    init: function (A) {
      var PdB = 10, N = 1;
      tx(A, 10, 16, '一帧', 't-s');
      A.rect(10, 24, 62, 22, 'f-golds s-gold w1', null, 3); tx(A, 41, 39, '训练 X', 'f-gold', 'middle', null, 11);
      A.rect(72, 24, 150, 22, 'f-accs s-acc w1', null, 3); tx(A, 147, 39, '数据', 'f-acc', 'middle', null, 11);
      var scan = A.line(10, 20, 10, 50, 's-ink w2');
      var lines = ['Y = HX + V', 'Ĥ_{LS} = YX^{H}(XX^{H})^{−1}', '最优训练：XX^{H} = (P/N)·I', '→ Ĥ = H + (N/P)VX^{H}', '总 MSE = MN^{2}σ^{2}/P'];
      lines.forEach(function (s, i) { tx(A, 12, 80 + i * 24, s, 't-m'); });
      var cx = 300, cy = 118, sc = 76, h = [0.55, 0.45];
      A.line(cx - 72, cy, cx + 92, cy, 's-line w1'); A.line(cx, cy - 64, cx, cy + 74, 's-line w1');
      tx(A, cx + 92, cy + 13, 'Re', 't-s', 'end'); tx(A, cx + 4, cy - 54, 'Im', 't-s');
      var hx = cx + h[0] * sc, hy = cy - h[1] * sc;
      var ring = A.circle(hx, hy, 10, 'f-accs s-acc w1 dash');
      var NP = 30, dots = [], g = [];
      for (var i = 0; i < NP; i++) { dots.push(A.circle(0, 0, 2.6, 'f-acc')); g.push([A.rand.gauss(), A.rand.gauss()]); }
      A.path('M' + (hx - 5) + ' ' + (hy - 5) + 'L' + (hx + 5) + ' ' + (hy + 5) + 'M' + (hx + 5) + ' ' + (hy - 5) + 'L' + (hx - 5) + ' ' + (hy + 5), 's-good w3');
      tx(A, 240, 210, '绿叉 = 真值 H，蓝点 = 各帧的 Ĥ', 't-xs');
      A.slider({ label: '训练功率 P/σ²', min: 0, max: 20, step: 1, value: PdB, unit: 'dB', on: function (v) { PdB = v; A.redraw(); } });
      A.choice({ label: '发射天线 N', options: ['1', '2', '4'], value: 0, on: function (i) { N = [1, 2, 4][i]; A.redraw(); } });
      var shown = 0;
      return function (t) {
        var per = 0.7, ph = (t % per) / per;
        A.set(scan, { x1: 10 + 212 * ph, x2: 10 + 212 * ph });
        shown = Math.min(NP, Math.floor(t / per) + 1);
        var vEl = N / A.undb(PdB), sd = Math.sqrt(vEl / 2);           // per-entry error variance Nσ²/P, split over Re/Im
        A.set(ring, { r: A.clamp(Math.sqrt(vEl) * sc, 2, 100) });
        var start = Math.floor(t / per);
        for (var i = 0; i < NP; i++) {
          var j = (start - i) % NP; if (j < 0) j += NP;
          var x = hx + g[j][0] * sd * sc, y = hy - g[j][1] * sd * sc, inside = x > 230 && x < 396 && y > 50 && y < 198;
          A.set(dots[i], { cx: x, cy: y });
          op(dots[i], i < shown && inside ? 1 - i / NP * 0.7 : 0);
        }
        A.note('P/σ² = ' + PdB + ' dB，N = ' + N + '：每个元素误差方差 Nσ²/P = ' + nm(vEl, 3) + 'σ²；M = 1 时总 MSE = MN²σ²/P = ' + nm(N * vEl, 3) + 'σ²');
      };
    }
  });

  /* =====================================================================
     7.1  Two design rules: B/N < B_C (flat), T ≫ delay spread (T_G > T_D)
     ===================================================================== */
  ANIM.reg('p2:7.1', {
    title: '子载波怎么分：每份窄到平坦，符号长过时延',
    cap: '看什么：上图把 B = 500 kHz 的频率选择性信道切成 N 份，每份宽 Δf = B/N；Δf < B<sub>C</sub> = 30 kHz 时每份里 |H| 几乎不变（绿）。下图是同一个 N 对应的符号时长 T = N·T<sub>s</sub>（T<sub>s</sub> = 1/B = 2 µs），红色是被 T<sub>D</sub> = 10 µs 回声污染的部分。数字取自 2025-26 S1 期末题；上图的 |H(f)| 曲线只是示意信道，不是按这组数字算出来的。',
    h: 250,
    init: function (A) {
      var B = 500, BC = 30, Ts = 2, TD = 10, N = 4;
      var tau = [0, 3, 6, 10], amp = [1, 0.62, 0.48, 0.35], ph = [0, 1.1, 2.3, 0.6];
      function Hf(f) { var re = 0, im = 0; for (var i = 0; i < 4; i++) { var a = -2 * Math.PI * f * 1e3 * tau[i] * 1e-6 + ph[i]; re += amp[i] * Math.cos(a); im += amp[i] * Math.sin(a); } return Math.sqrt(re * re + im * im); }
      var ax = A.axes({ x: 30, y: 26, w: 350, h: 76, xr: [0, B], yr: [0, 2.6], yl: '|H(f)|　（f：kHz）',
        ticksX: [0, 100, 200, 300, 400, 500].map(function (v) { return { v: v, l: String(v) }; }) });
      var strips = A.path('', 'f-goods s-none'), divs = A.path('', 's-soft w1');
      A.curve(ax, Hf, 's-acc w2', null, 300);
      var bc = A.g();
      A.path('M' + ax.X(420) + ' 30v-6H' + ax.X(450) + 'v6', 's-gold w2', bc);
      tx(A, ax.X(435), 18, 'B_{C} = 30 kHz', 'f-gold', 'middle', bc, 10.5);
      var v1 = tx(A, 30, 134, '', 't-b');
      // time panel
      var tx0 = 30, tw = 350, Tmax = 150;
      function TX(t) { return tx0 + t / Tmax * tw; }
      tx(A, 30, 156, '时间（µs）：一串 OFDM 符号，每个长 T', 't-s');
      A.rect(TX(0), 164, tw, 22, 'f-accs s-none', null, 0);
      var redP = A.path('', 'f-bads s-none'), bnd = A.path('', 's-acc w1');
      A.line(TX(0), 186, TX(Tmax), 186, 's-soft w1');
      [0, 50, 100, 150].forEach(function (v) { A.line(TX(v), 186, TX(v), 190, 's-soft w1'); tx(A, TX(v), 201, String(v), 't-s', 'middle'); });
      var v2 = tx(A, 30, 222, '', 't-b'), v3 = tx(A, 30, 240, '', 't-s');
      function draw() {
        var df = B / N, flat = df < BC, d = '', s = '';
        for (var i = 1; i < N; i++) d += 'M' + ax.X(i * df).toFixed(1) + ' 26V102';
        A.set(divs, { d: d });
        A.set(strips, { d: 'M' + ax.X(0) + ' 26H' + ax.X(B) + 'V102H' + ax.X(0) + 'Z', cls: flat ? 'f-goods s-none' : 'f-bads s-none' });
        A.setText(v1, 'Δf = B/N = ' + nm(df, 3) + ' kHz ' + (flat ? '< ' : '> ') + 'B_{C} = 30 kHz → ' + (flat ? '每个子信道平坦 ✓' : '子信道内仍有起伏 ✗'));
        A.set(v1, { cls: 't-b ' + (flat ? 'f-good' : 'f-bad') });
        var T = N * Ts; d = ''; s = '';
        for (var t = 0; t < Tmax - 1e-9; t += T) {
          if (t > 0) d += 'M' + TX(t).toFixed(1) + ' 164V186';
          if (t > 0) s += 'M' + TX(t).toFixed(1) + ' 164H' + TX(Math.min(Tmax, t + TD)).toFixed(1) + 'V186H' + TX(t).toFixed(1) + 'Z';
        }
        A.set(bnd, { d: d }); A.set(redP, { d: s });
        var frac = TD / T;
        A.setText(v2, 'T = N·T_{s} = ' + nm(T, 3) + ' µs，回声 T_{D} = 10 µs 占 ' + (frac >= 1 ? '整个符号（>100%）' : Math.round(frac * 100) + '%'));
        A.set(v2, { cls: 't-b ' + (frac <= 0.2 ? 'f-good' : 'f-bad') });
        A.setText(v3, '再加保护间隔 T_{G} ≥ T_{D} 把这段红色挡掉（7.4 节）；N 越大红色占比越小');
        A.note('N = ' + N + '：平坦要求 N > B/B<sub>C</sub> = 500/30 = 16.7 → 最少 N = 17。N 也不能太大：T = N/B 要远小于相干时间 1/B<sub>d</sub>。');
      }
      A.slider({ label: '子载波数 N', min: 1, max: 64, step: 1, value: N, on: function (v) { N = v; draw(); } });
      draw();
      return {};
    }
  });

  /* =====================================================================
     7.2  Orthogonality: Δf = 1/T, sinc peaks on the others' zeros, ∫ = 0
     ===================================================================== */
  ANIM.reg('p2:7.2', {
    title: '子载波正交：频谱重叠却不干扰',
    cap: '看什么：上图 5 个子载波的 sinc 频谱，间隔 1/T 时每个峰正好落在别人的零点上；下图把子载波 1 和 2 在一个符号 T 内相乘再积分，正负面积抵消为 0。最后一步把间隔改成 1.2/T，两件事同时失效（ICI）。',
    h: 286,
    stepDur: 4.4,
    tween: 3.4,
    steps: [
      '子载波间隔 Δf = 1/T。每个子载波只持续 T 秒，频谱是 sinc(fT − k)，主瓣互相重叠。',
      '在 f = 2/T 处采样：其他子载波正好过零（绿点），只剩 s₂，不受干扰。',
      '时域看：子载波 1 和 2 在一个符号 T 内正好转整数圈（1 圈、2 圈）。',
      '相乘再积分：正（绿）负（红）面积正好抵消，(1/T)∫₀<sup>T</sup> = 0，这就是正交。',
      '若间隔不是 1/T（如 1.2/T）：积分 ≠ 0，峰也不在别人的零点上 → 子载波间干扰 ICI。'
    ],
    init: function (A) {
      var sp = 1, spFrom = 1;
      var axF = A.axes({ x: 26, y: 24, w: 356, h: 96, xr: [-1.3, 6.2], yr: [-0.3, 1.1], xl: 'f', xAxisAt: 'bottom',
        ticksX: [0, 1, 2, 3, 4, 5].map(function (k) { return { v: k, l: k ? k + '/T' : '0' }; }) });
      A.line(axF.X(-1.3), axF.Y(0), axF.X(6.2), axF.Y(0), 's-line w1');
      var sp5 = [];
      for (var k = 0; k < 5; k++) sp5.push(A.path('', k === 2 ? 's-acc w3' : 's-soft w1'));
      var sl = A.line(0, 20, 0, 122, 's-ink w1 dash');
      var dd = [];
      for (k = 0; k < 5; k++) dd.push(A.circle(0, 0, k === 2 ? 4 : 3.4, k === 2 ? 'f-acc' : 'f-good'));
      var fl = tx(A, 380, 16, '', 't-s', 'end');
      var axT = A.axes({ x: 26, y: 160, w: 340, h: 88, xr: [0, 1], yr: [-1.15, 1.15], xAxisAt: 'bottom',
        ticksX: [{ v: 0, l: '0' }, { v: 0.5, l: 'T/2' }, { v: 1, l: 'T' }] });
      A.line(axT.X(0), axT.Y(0), axT.X(1), axT.Y(0), 's-line w1');
      var fp = A.path('', 'f-goods s-none'), fn = A.path('', 'f-bads s-none');
      var c1 = A.path('', 's-gold w1'), c2 = A.path('', 's-pur w1'), pr = A.path('', 's-acc w2');
      var sw = A.line(0, 158, 0, 248, 's-ink w1');
      var lg = A.g();
      tx(A, 30, 150, '子载波 1', 'f-gold', null, lg, 10.5); tx(A, 86, 150, '子载波 2', 'f-pur', null, lg, 10.5); tx(A, 142, 150, '蓝 = 两者乘积', 'f-acc', null, lg, 10.5);
      var iv = tx(A, 390, 150, '', 't-m t-b', 'end');
      function prod(t) { return Math.cos(2 * Math.PI * sp * t) * Math.cos(2 * Math.PI * 2 * sp * t); }
      function integ(T) {   // closed form of ∫0^T cos(a t)cos(b t) dt, a = 2π sp, b = 4π sp
        var a = 2 * Math.PI * sp, b = 4 * Math.PI * sp;
        return 0.5 * (Math.sin((b - a) * T) / (b - a) + Math.sin((b + a) * T) / (b + a));
      }
      var K = 0;
      return {
        step: function (k) { spFrom = sp; K = k; },
        frame: function (ts, dt, k) {
          sp = A.lerp(spFrom, k === 4 ? 1.2 : 1, A.prog(ts, 1.0));
          for (var j = 0; j < 5; j++) {
            A.setCurve(sp5[j], axF, function (f) { return sinc(f - j * sp); }, 260);
            op(sp5[j], j === 2 ? 1 : 0.8);
          }
          var f0 = 2 * sp, showS = k === 1 || k === 4;
          A.set(sl, { x1: axF.X(f0), x2: axF.X(f0) }); op(sl, showS ? 1 : 0);
          var worst = 0;
          for (j = 0; j < 5; j++) {
            var v = sinc(f0 - j * sp);
            if (j !== 2) worst = Math.max(worst, Math.abs(v));
            A.set(dd[j], { cx: axF.X(f0), cy: axF.Y(v), cls: j === 2 ? 'f-acc' : (Math.abs(v) < 0.01 ? 'f-good' : 'f-bad') });
            op(dd[j], showS ? 1 : 0);
          }
          A.setText(fl, showS ? (worst < 0.01 ? '其他子载波在 f = 2/T 处 = 0' : '其他子载波在采样点 ≠ 0（最大 ' + nm(worst, 2) + '）') : 'Δf = ' + nm(sp, 2) + '/T');
          var bot = k >= 2 ? 1 : 0.15;
          op(c1, bot); op(c2, bot); op(lg, bot);
          A.setCurve(c1, axT, function (t) { return Math.cos(2 * Math.PI * sp * t); }, 160);
          A.setCurve(c2, axT, function (t) { return Math.cos(4 * Math.PI * sp * t); }, 160);
          var tEnd = k === 3 ? A.clamp(ts / 2.6, 0, 1) : (k === 4 ? 1 : 0);
          A.setCurve(pr, axT, prod, 200); op(pr, k >= 3 ? 1 : 0);
          var P = [[axT.X(0), axT.Y(0)]], Ng = [[axT.X(0), axT.Y(0)]];
          for (var i = 0; i <= 160; i++) { var t = tEnd * i / 160, y = prod(t); P.push([axT.X(t), axT.Y(Math.max(0, y))]); Ng.push([axT.X(t), axT.Y(Math.min(0, y))]); }
          P.push([axT.X(tEnd), axT.Y(0)]); Ng.push([axT.X(tEnd), axT.Y(0)]);
          A.set(fp, { d: A.pts(P) + 'Z' }); A.set(fn, { d: A.pts(Ng) + 'Z' });
          A.set(sw, { x1: axT.X(tEnd), x2: axT.X(tEnd) }); op(sw, k >= 3 ? 1 : 0);
          var I = integ(tEnd);
          A.setText(iv, k >= 3 ? '(1/T)∫ = ' + fx(I, 3) : '');
          A.set(iv, { cls: 't-m t-b ' + (k === 4 ? 'f-bad' : (tEnd >= 1 ? 'f-good' : '')) });
        }
      };
    }
  });

  /* =====================================================================
     7.3  H_k = Σ h_i e^{−j2πik/N}: phasor sum per subcarrier, |H_k| bars
     ===================================================================== */
  (function () {
    var CH = [
      { l: 'Practice 7 {0.8, 0.6}', h: [0.8, 0.6] },
      { l: '25-26 S2 {1, 0.3}', h: [1, 0.3] },
      { l: '23-24 {1, −0.6, 0.2}', h: [1, -0.6, 0.2] }
    ];
    var N = 4;
    function Hk(h, k) { var re = 0, im = 0; h.forEach(function (v, i) { var a = -2 * Math.PI * i * k / N; re += v * Math.cos(a); im += v * Math.sin(a); }); return [re, im]; }
    ANIM.reg('p2:7.3', {
      title: '子信道增益 Hₖ：抽头转一转再相加',
      cap: '看什么：左图是复平面，H<sub>k</sub> = h₀ + h₁e<sup>−j2πk/4</sup> + …：第 i 个抽头每换一个子载波就多转 −i×90°，首尾相加得到绿色的 H<sub>k</sub>。右图柱子是 |H<sub>k</sub>|，虚线是整个频率响应，子载波就是在它上面取了 N 个点。按钮可换成期末题的信道。',
      h: 250,
      stepDur: 4.2,
      steps: [
        'H<sub>k</sub> = Σ h<sub>i</sub>e<sup>−j2πik/N</sup>，N = 4：第 i 个抽头每加 1 个 k 就转 −i×90°，再首尾相加。',
        'k = 1：e<sup>−jπ/2</sup> = −j，h₁ 转到 −j 方向（h₂ 转到 −1）。绿色箭头就是 H₁。',
        'k = 2：e<sup>−jπ</sup> = −1，h₁ 反向（h₂ 转回 +1）。两路相消时就是深衰落（红柱）。',
        'k = 3：e<sup>−j3π/2</sup> = +j。抽头是实数时 H₃ 是 H₁ 的共轭（上下对称）。',
        'k = 4（= 0）：全部同向，H₄ = H₀ = 所有抽头之和。',
        '自检：Σ|H<sub>k</sub>|² = N·Σh<sub>i</sub>²。每个子载波只乘一个复数 → 频率选择性信道变成 N 个平坦子信道。'
      ],
      init: function (A) {
        var ci = 0, kFrom = 0, kCur = 0;
        var cx = 96, cy = 122, sc = 50;
        A.line(cx - 92, cy, cx + 92, cy, 's-line w1'); A.line(cx, cy - 98, cx, cy + 98, 's-line w1');
        tx(A, cx + 92, cy + 13, 'Re', 't-s', 'end'); tx(A, cx + 4, cy - 88, 'Im', 't-s');
        A.circle(cx, cy, sc, 'f-none s-line w1 dash');
        var tipColor = ['s-acc', 's-gold', 's-pur'];
        var res = A.arrow(cx, cy, cx + 1, cy, 's-good w4 op7', null, 10);
        var arr = [0, 1, 2].map(function (i) { return A.arrow(cx, cy, cx + 1, cy, tipColor[i] + ' w2', null, 6); });
        var kl = tx(A, 6, 16, '', 't-b');
        var bx = A.axes({ x: 222, y: 34, w: 156, h: 170, xr: [0, 4.6], yr: [0, 2], xl: 'k', yl: '|H_{k}|',
          ticksX: [1, 2, 3, 4].map(function (k) { return { v: k, l: String(k) }; }), ticksY: [{ v: 1, l: '1' }, { v: 2, l: '2' }] });
        var resp = A.path('', 's-faint w1 dash');
        var bars = [], bl = [];
        for (var k = 1; k <= 4; k++) { bars.push(A.rect(0, 0, 18, 0, 'f-good', null, 2)); bl.push(tx(A, bx.X(k), 0, '', 't-m', 'middle', null, 10.5)); }
        var chk = tx(A, 222, 244, '', 't-s');
        A.choice({ label: '信道', options: CH.map(function (c) { return c.l; }), value: 0, on: function (i) { ci = i; A.redraw(); } });
        return {
          step: function (k) { kFrom = kCur; },
          frame: function (ts, dt, k) {
            var h = CH[ci].h, kt = k >= 1 && k <= 4 ? k : (k === 0 ? 0 : 4);
            kCur = A.lerp(kFrom, kt, A.prog(ts, 1.2));
            if (k === 0) kCur = 0;
            var x = cx, y = cy;
            for (var i = 0; i < 3; i++) {
              if (i >= h.length) { arr[i].style.display = 'none'; continue; }
              var a = -2 * Math.PI * i * kCur / N, nx = x + h[i] * Math.cos(a) * sc, ny = y - h[i] * Math.sin(a) * sc;
              A.moveArrow(arr[i], x, y, nx, ny); x = nx; y = ny;
            }
            A.moveArrow(res, cx, cy, x, y);
            res.style.display = k === 0 ? 'none' : res.style.display;
            var H = Hk(h, Math.round(kCur));
            A.setText(kl, k === 0 ? 'h = {' + h.map(function (v) { return nm(v); }).join(', ') + '}（蓝 h₀ 金 h₁ 紫 h₂）' : 'k = ' + nm(kCur, 1) + '：H = ' + (Math.abs(kCur - Math.round(kCur)) < 0.02 ? cplx(H[0], H[1]) : '…'));
            A.setCurve(resp, bx, function (v) { var z = Hk(h, v); return Math.sqrt(z[0] * z[0] + z[1] * z[1]); }, 120);
            var list = [], s2 = 0;
            for (var q = 1; q <= 4; q++) {
              var Z = Hk(h, q), mag = Math.sqrt(Z[0] * Z[0] + Z[1] * Z[1]);
              s2 += mag * mag;
              var on = k >= 5 || q <= k;
              A.set(bars[q - 1], { x: bx.X(q) - 9, y: bx.Y(mag), height: Math.max(0.5, bx.Y(0) - bx.Y(mag)), cls: mag * mag < 0.25 ? 'f-bad' : (q === k ? 'f-good' : 'f-goods s-good w1') });
              op(bars[q - 1], on ? (q === k ? A.prog(ts, 0.5, 0.9) : 1) : 0);
              A.set(bl[q - 1], { y: bx.Y(mag) - 4 }); A.setText(bl[q - 1], nm(mag, 2)); op(bl[q - 1], on ? 1 : 0);
              if (on) list.push('H' + SUB[q] + ' = ' + cplx(Z[0], Z[1]));
            }
            var sh = h.reduce(function (s, v) { return s + v * v; }, 0);
            A.setText(chk, k >= 5 ? 'Σ|H_{k}|² = ' + nm(s2, 3) + ' = 4 × ' + nm(sh, 3) : '');
            A.note(list.length ? list.join('　') + (k >= 5 ? '<br>|H|²：' + [1, 2, 3, 4].map(function (q) { var Z = Hk(h, q); return nm(Z[0] * Z[0] + Z[1] * Z[1], 3); }).join('，') : '') : 'H<sub>k</sub> = Σ h<sub>i</sub> e<sup>−j2πik/4</sup>，k = 1…4（H₄ = H₀）');
          }
        };
      }
    });
  })();

  /* =====================================================================
     7.4  Guard interval vs cyclic prefix: echo transition must fall inside the CP
     ===================================================================== */
  ANIM.reg('p2:7.4', {
    title: '循环前缀：把回声的"过渡"藏进 CP',
    cap: '看什么：上行是直达径，下行是晚 τ 到达的回声（×0.6）。接收端只取虚线框（FFT 窗，长 T）里的采样。窗里的回声必须是本块的完整循环移位，子载波才保持正交。',
    h: 236,
    stepDur: 4.6,
    steps: [
      '不加保护间隔：上一块的回声拖进本块的 FFT 窗（红）→ ISI，窗里也不是完整周期 → ICI。',
      '加一段空白保护间隔 T<sub>G</sub> ≥ τ：上一块的回声被挡住，但窗里回声开头缺一截 → 仍有 ICI。',
      '循环前缀：把本块最后 T<sub>cp</sub> 那一段复制到最前面（金色）。',
      '回声的过渡落在 CP 里，被接收端丢掉；窗里的回声是完整的循环移位 → 无 ISI、无 ICI，R<sub>k</sub> = H<sub>k</sub>s<sub>k</sub>。',
      '若最大时延 τ > T<sub>cp</sub>：过渡进了窗，ISI 又回来。所以 T<sub>cp</sub> ≥ 最大时延扩展（离散：G ≥ L − 1）。'
    ],
    init: function (A) {
      var T = 128, G = 32, x0 = 22, tauA = 22, tauB = 44;
      var yD = 62, yE = 128, amp = 17;
      var blk = [
        { a: [0.5, 0.4, 0.3], f: [2, 3, 5], p: [0.3, 1.0, 2.0] },
        { a: [0.55, 0.35, 0.3], f: [1, 4, 6], p: [2.1, 0.2, 1.3] }
      ];
      function wave(b, u) { var s = 0; for (var i = 0; i < 3; i++) s += b.a[i] * Math.cos(2 * Math.PI * b.f[i] * u + b.p[i]); return s; }
      var paths = { d: [], e: [] };
      ['d', 'e'].forEach(function (r) { for (var i = 0; i < 4; i++) paths[r].push(A.path('', (i % 2 ? 's-acc' : 's-gold') + ' w2')); });
      var bnd = A.path('', 's-faint w1 dash');
      var tailB = A.path('', 's-gold w2'), tailT = tx(A, 0, 30, '复制这段', 'f-gold', 'middle', null, 10.5);
      var copyG = A.g(), copyP = A.path('', 's-gold w3', copyG);
      var isiR = A.rect(0, yE - 26, 0, 52, 'f-bads s-bad w1', null, 2);
      var iciR = A.rect(0, yE - 26, 0, 52, 'f-golds s-gold w1 dash', null, 2);
      var winR = A.rect(0, yE + 32, T, 18, 'f-none s-ink w2 dash', null, 3);
      var winT = tx(A, 0, yE + 45, 'FFT 窗（长 T）', 't-s', 'middle');
      tx(A, 6, 14, '上：直达径　下：回声（晚 τ、×0.6）　灰 = 块 n−1，蓝 = 块 n', 't-s');
      var tag = tx(A, 0, yE - 30, '', 't-b', 'middle');
      var cpL = [tx(A, 0, yD - 24, 'CP', 'f-gold t-b', 'middle'), tx(A, 0, yD - 24, 'CP', 'f-gold t-b', 'middle')];
      var bl = [tx(A, 0, yD - 24, '块 n−1', 't-s', 'middle'), tx(A, 0, yD - 24, '块 n', 't-s', 'middle')];
      var tauA_ = A.arrow(0, 0, 1, 0, 's-pur w1', null, 4), tauT = tx(A, 0, 0, 'τ', 'f-pur t-b', 'middle');
      var mark = A.line(0, yE - 22, 0, yE + 22, 's-good w3');
      var bottom = tx(A, 200, 226, '', 't-b', 'middle');
      var K = 0, tauFrom = tauA, tauNow = tauA;
      function geom(mode) {      // mode 0 none, 1 blank guard, 2 cyclic prefix
        var g = mode === 0 ? 0 : G;
        return { g: g, s0: x0, d0: x0 + g, s1: x0 + g + T, d1: x0 + 2 * g + T, end: x0 + 2 * g + 2 * T };
      }
      function seg(b, from, to, dataStart, scale, shift, yc, blank) {
        var pts = [];
        for (var i = 0; i <= 80; i++) {
          var x = from + (to - from) * i / 80, u = (x - dataStart) / T;
          var v = blank && x < dataStart ? 0 : wave(b, u);
          pts.push([x + shift, yc - v * amp * scale]);
        }
        return A.pts(pts);
      }
      return {
        step: function (k) { K = k; tauFrom = tauNow; },
        frame: function (ts, dt, k) {
          var mode = k === 0 ? 0 : k === 1 ? 1 : 2, Gm = geom(mode);
          tauNow = A.lerp(tauFrom, k === 4 ? tauB : tauA, A.prog(ts, 1.2));
          var tau = tauNow, blank = mode === 1;
          var rows = [['d', 1, 0, yD], ['e', 0.6, tau, yE]];
          rows.forEach(function (R) {
            var P = paths[R[0]];
            A.set(P[0], { d: Gm.g ? seg(blk[0], Gm.s0, Gm.d0, Gm.d0, R[1], R[2], R[3], blank) : '' });
            A.set(P[1], { d: seg(blk[0], Gm.d0, Gm.s1, Gm.d0, R[1], R[2], R[3], false) });
            A.set(P[2], { d: Gm.g ? seg(blk[1], Gm.s1, Gm.d1, Gm.d1, R[1], R[2], R[3], blank) : '' });
            A.set(P[3], { d: seg(blk[1], Gm.d1, Gm.end, Gm.d1, R[1], R[2], R[3], false) });
            for (var i = 0; i < 4; i++) A.set(P[i], { cls: (i === 1 ? 's-soft' : i === 3 ? 's-acc' : 's-gold') + ' w2' });
          });
          // copy animation (step 2): tail of block n slides to its CP
          if (k === 2) {
            var p = A.prog(ts, 1.6, 0.3);
            A.set(copyP, { d: seg(blk[1], Gm.end - G, Gm.end, Gm.d1, 1, 0, yD, false) });
            copyG.setAttribute('transform', 'translate(' + (-T * p).toFixed(1) + ' 0)');
            op(copyG, p < 1 ? 1 : 0);
            op(paths.d[2], p); op(paths.e[2], p); op(paths.d[0], p); op(paths.e[0], p);
          } else { op(copyG, 0); for (var i = 0; i < 4; i++) { op(paths.d[i], 1); op(paths.e[i], 1); } }
          A.set(tailB, { d: 'M' + (Gm.end - G) + ' 40v-5H' + Gm.end + 'v5' }); A.set(tailT, { x: Gm.end - G / 2 });
          op(tailB, mode === 2 && k <= 2 ? 1 : 0); op(tailT, mode === 2 && k <= 2 ? 1 : 0);
          // FFT window = data part of block n; dashed lines = block boundaries
          A.set(bnd, { d: 'M' + Gm.s1 + ' 40V' + (yE + 30) + (Gm.g ? 'M' + Gm.d1 + ' 40V' + (yE + 30) : '') });
          A.set(winR, { x: Gm.d1 }); A.set(winT, { x: Gm.d1 + T / 2 });
          A.set(cpL[0], { x: Gm.s0 + G / 2 }); A.set(cpL[1], { x: Gm.s1 + G / 2 });
          op(cpL[0], Gm.g ? 1 : 0); op(cpL[1], Gm.g ? 1 : 0);
          A.setText(cpL[0], mode === 1 ? '空白' : 'CP'); A.setText(cpL[1], mode === 1 ? '空白' : 'CP');
          A.set(bl[0], { x: Gm.d0 + T / 2 }); A.set(bl[1], { x: Gm.d1 + T / 2 });
          A.moveArrow(tauA_, Gm.s1, yE + 24, Gm.s1 + tau, yE + 24);
          A.set(tauT, { x: Gm.s1 + tau / 2, y: yE + 20 });
          // where does the echo transition (block n−1 → n) land?
          var trans = Gm.s1 + tau;                       // echo of block n starts here
          var intoWin = trans - Gm.d1;                    // > 0 → inside the FFT window
          var isiW = 0, iciW = 0, txt = '', tcls = 'f-good';
          if (mode === 0) { isiW = tau; txt = 'ISI + ICI'; tcls = 'f-bad'; }
          else if (mode === 1) { iciW = tau; txt = '缺口 → ICI'; tcls = 'f-gold'; }
          else if (intoWin > 0.5) { isiW = intoWin; txt = 'τ > T_{cp}：ISI'; tcls = 'f-bad'; }
          else { txt = '过渡在 CP 内 ✓'; tcls = 'f-good'; }
          A.set(isiR, { x: Gm.d1, width: isiW }); op(isiR, isiW ? 0.9 : 0);
          var gapStart = Gm.d1, gapEnd = Math.min(Gm.d1 + iciW, Gm.d1 + tau);
          A.set(iciR, { x: gapStart, width: Math.max(0, gapEnd - gapStart) }); op(iciR, iciW ? 0.9 : 0);
          A.set(mark, { x1: trans, x2: trans, cls: intoWin > 0.5 ? 's-bad w3' : 's-good w3' }); op(mark, mode === 2 && k >= 3 ? 1 : 0);
          A.setText(tag, txt); A.set(tag, { x: Math.max(70, Math.min(330, Gm.d1 + 20)), cls: 't-b ' + tcls });
          op(tag, mode === 2 && k < 3 ? 0 : 1);
          A.setText(bottom, mode === 2 ? (k >= 3 ? (intoWin > 0.5 ? 'τ = ' + Math.round(tau / G * 10) / 10 + '×T_{cp} 太长：需要 T_{cp} ≥ 最大时延' : '窗内 = 本块的循环移位 → R_{k} = H_{k}s_{k}') : '块尾那段复制到块头 → x(t) 在 [−T_{cp}, T) 上是周期的') : (mode === 1 ? '空白挡住了 ISI，但窗里的回声不完整' : '回声把上一块拖进本块'));
          A.set(bottom, { cls: 't-b ' + (mode === 2 && k === 3 ? 'f-good' : (k === 4 ? 'f-bad' : '')) });
        }
      };
    }
  });

  /* =====================================================================
     7.4/2  Guard/CP overhead: block = NT_s + T_G, loss = 10log((NT_s+T_G)/NT_s)
     ===================================================================== */
  (function () {
    var PRE = [
      { l: '23-24', N: 4, Ts: 1, TG: 1, b: 0, src: 'B = 1 MHz → T<sub>s</sub> = 1/B' },
      { l: '25-26 S1', N: 50, Ts: 2, TG: 10, b: 2, src: 'B = 500 kHz → T<sub>s</sub> = 1/B，4-QAM' },
      { l: '25-26 S2', N: 4, Ts: 2, TG: 20, b: 0, src: '基带符号 2 µs，CP = 20 µs' },
      { l: 'Practice 7 Q2', N: 60, Ts: 1e3 / 600, TG: 20, b: 4, src: 'B = 600 kHz → T<sub>s</sub> = 1/B，16-QAM' }
    ];
    ANIM.reg('p2:7.4/2', {
      title: 'CP 的代价：块长、效率与功率损失',
      cap: '看什么：一个 OFDM 块 = 有用部分 T = N·T<sub>s</sub>（蓝）+ 保护间隔/CP T<sub>G</sub>（金）。CP 不带数据却占时间和功率：效率 T/(T + T<sub>G</sub>)，功率损失 10log₁₀[(NT<sub>s</sub> + T<sub>G</sub>)/(NT<sub>s</sub>)] dB。按钮是期末题和 Practice 7 的数字；拖 N 看 N 越大开销越小。',
      h: 236,
      init: function (A) {
        var cur = copy(PRE[0]), lock = false;
        var barY = 30, bx0 = 16, bw = 368;
        var cpR = A.rect(bx0, barY, 10, 26, 'f-golds s-gold w1', null, 3), usR = A.rect(bx0, barY, 10, 26, 'f-accs s-acc w1', null, 3);
        var cpT = tx(A, 0, barY - 6, '', 'f-gold', 'middle', null, 10.5), usT = tx(A, 0, barY + 17, '', 'f-acc t-b', 'middle', null, 11);
        var totT = tx(A, 200, barY + 44, '', 't-m t-b', 'middle');
        var ax = A.axes({ x: 46, y: 96, w: 330, h: 106, xr: [0, 128], yr: [0, 12], yl: '功率损失 (dB)　横轴：子载波数 N',
          ticksX: [0, 32, 64, 96, 128].map(function (v) { return { v: v, l: String(v) }; }), ticksY: [0, 4, 8, 12].map(function (v) { return { v: v, l: String(v) }; }), grid: true, yAxisAt: 'left' });
        var cv = A.path('', 's-gold w2'), dot = A.circle(0, 0, 4.5, 'f-bad'), dl = tx(A, 0, 0, '', 't-m t-b f-bad', 'start');
        var ch = A.choice({ label: '题目', options: PRE.map(function (p) { return p.l; }), value: 0, on: function (i) {
          cur = copy(PRE[i]); lock = true; sN.set(cur.N); sG.set(cur.TG); lock = false; draw(); } });
        var sN = A.slider({ label: '子载波 N', min: 1, max: 128, step: 1, value: cur.N, on: function (v) { if (lock) return; cur.N = v; ch.set(-1, true); draw(); } });
        var sG = A.slider({ label: 'T<sub>G</sub>', min: 0, max: 40, step: 0.5, value: cur.TG, unit: 'µs', on: function (v) { if (lock) return; cur.TG = v; ch.set(-1, true); draw(); } });
        function draw() {
          var T = cur.N * cur.Ts, Tb = T + cur.TG, eff = T / Tb, loss = 10 * Math.log10(Tb / T);
          var s = bw / Tb, wG = cur.TG * s;
          A.set(cpR, { x: bx0, width: wG }); A.set(usR, { x: bx0 + wG, width: bw - wG });
          A.set(cpT, { x: bx0 + Math.max(wG / 2, 30) }); A.setText(cpT, 'T_{G} = ' + nm(cur.TG, 3) + ' µs');
          A.set(usT, { x: bx0 + wG + (bw - wG) / 2 }); A.setText(usT, bw - wG > 120 ? 'T = N·T_{s} = ' + nm(T, 4) + ' µs' : nm(T, 4) + ' µs');
          A.setText(totT, '块长 ' + nm(Tb, 4) + ' µs · 效率 ' + (eff * 100).toFixed(1) + '% · 损失 ' + fx(loss, 2) + ' dB');
          A.setCurve(cv, ax, function (n) { return n < 1 ? null : 10 * Math.log10((n * cur.Ts + cur.TG) / (n * cur.Ts)); }, 256);
          var yy = Math.min(12, loss);
          A.set(dot, { cx: ax.X(cur.N), cy: ax.Y(yy) });
          A.set(dl, { x: ax.X(cur.N) + (cur.N > 90 ? -8 : 8), y: ax.Y(yy) - 8, 'text-anchor': cur.N > 90 ? 'end' : 'start' });
          A.setText(dl, fx(loss, 2) + ' dB');
          var rate = cur.b ? cur.N * cur.b / Tb : 0;     // bits per µs = Mbit/s
          A.note('T<sub>s</sub> = ' + nm(cur.Ts, 4) + ' µs（' + (ch.get() >= 0 ? PRE[ch.get()].src : '自定') + '）<br>损失 = 10log₁₀(' + nm(Tb, 4) + '/' + nm(T, 4) + ') = ' + fx(loss, 2) + ' dB' +
            (rate ? '<br>速率 = N·log₂M/(T + T<sub>G</sub>) = ' + cur.N * cur.b + ' bit / ' + nm(Tb, 4) + ' µs = ' + (rate >= 1 ? A.fmt(rate, 3) + ' Mbit/s' : A.fmt(rate * 1000, 3) + ' kbit/s') : ''));
        }
        draw();
        return {};
      }
    });
  })();

  /* =====================================================================
     7.5  One-tap equalizer per subcarrier + capacity (water-filling vs equal capacity)
     ===================================================================== */
  (function () {
    var hT = [0.8, 0.6], N = 4, Ptot = 10, H = [], g = [];
    for (var k = 1; k <= N; k++) {
      var re = 0, im = 0;
      hT.forEach(function (v, i) { re += v * Math.cos(-2 * Math.PI * i * k / N); im += v * Math.sin(-2 * Math.PI * i * k / N); });
      H.push([re, im]); g.push(re * re + im * im);
    }
    var floor = g.map(function (v) { return 1 / v; });              // N_k/|H_k|², noise N_k = 1
    var act = [0, 1, 2, 3], mu = 0;
    for (;;) {
      mu = (Ptot + act.reduce(function (s, i) { return s + floor[i]; }, 0)) / act.length;
      var drop = act.filter(function (i) { return floor[i] >= mu; });
      if (!drop.length) break;
      act = act.filter(function (i) { return floor[i] < mu; });
    }
    var Pw = floor.map(function (f) { return Math.max(0, mu - f); });
    var Cw = g.reduce(function (s, v, i) { return s + Math.log2(1 + v * Pw[i]); }, 0);
    var cEq = Ptot / floor.reduce(function (s, v) { return s + v; }, 0);
    var Pe = g.map(function (v) { return cEq / v; });
    var Ce = 4 * Math.log2(1 + cEq);
    var worst = Pe.indexOf(Math.max.apply(null, Pe));
    function li(arr, d) { return arr.map(function (v) { return nm(v, d); }).join(', '); }
    ANIM.reg('p2:7.5', {
      title: '每个子载波一抽头均衡，容量逐个相加',
      cap: '看什么：上排是 4 个子载波上的 QPSK 星座（示意噪声），沿用 7.3 节 h = {0.8, 0.6} 的 H<sub>k</sub>。除以 H<sub>k</sub> 就把星座转回来，但 |H₂| = 0.2 的子载波噪声被放大 5 倍。下图是 Practice 7 第 1(c)(d) 题：噪声 1、总功率 10 的注水和等容量分配。',
      h: 300,
      stepDur: 4.6,
      steps: [
        '加 CP 后每个子载波：R<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + W<sub>k</sub>。QPSK 星座被 H<sub>k</sub> 旋转、缩放。',
        '一抽头均衡 ŝ<sub>k</sub> = R<sub>k</sub>/H<sub>k</sub>：星座转回原位。但子载波 2（|H₂| = 0.2）噪声放大 5 倍。',
        '容量 = Σ log₂(1 + |H<sub>k</sub>|²P<sub>k</sub>/N<sub>k</sub>)。注水池底 N<sub>k</sub>/|H<sub>k</sub>|² = ' + li(floor, 2) + '。',
        '注水（总功率 10）：水面 μ = ' + nm(mu, 2) + '，子载波 2 池底高过水面，不给功率。C = ' + nm(Cw, 2) + ' bit/OFDM 符号。',
        '对比等容量：P<sub>k</sub> ∝ 1/|H<sub>k</sub>|²，子载波 2 吃掉 ' + nm(Pe[worst], 2) + '（' + Math.round(Pe[worst] / Ptot * 100) + '%），总容量只有 ' + nm(Ce, 2) + ' bit/OFDM 符号。'
      ],
      init: function (A) {
        var CXs = [52, 149, 246, 343], cy = 70, sc = 26, half = 44;
        var Sx = [[1, 1], [-1, 1], [-1, -1], [1, -1]].map(function (p) { return [p[0] / Math.SQRT2, p[1] / Math.SQRT2]; });
        var pts = [], ideal = [], R = A.rng(77);
        for (var k = 0; k < 4; k++) {
          A.rect(CXs[k] - half, cy - half, 2 * half, 2 * half, 'f-card s-line w1', null, 6);
          A.line(CXs[k] - half, cy, CXs[k] + half, cy, 's-line w1'); A.line(CXs[k], cy - half, CXs[k], cy + half, 's-line w1');
          tx(A, CXs[k], 16, '子载波 ' + (k + 1), 't-s t-b', 'middle');
          tx(A, CXs[k], cy + half + 13, 'H = ' + cplx(H[k][0], H[k][1]), 't-xs t-m', 'middle');
          var arr = [];
          for (var s = 0; s < 4; s++) {
            ideal.push({ k: k, s: s, e: A.circle(0, 0, 4.2, 'f-none s-ink w1') });
            for (var j = 0; j < 5; j++) arr.push({ s: s, w: [R.gauss() * 0.06, R.gauss() * 0.06], e: A.circle(0, 0, 2, k === 1 ? 'f-bad' : 'f-acc') });
          }
          pts.push(arr);
        }
        // water-filling panel
        var ax = A.axes({ x: 44, y: 160, w: 340, h: 112, xr: [0.4, 4.6], yr: [0, 10], yl: '功率 / 池底',
          ticksX: [1, 2, 3, 4].map(function (k) { return { v: k, l: 'k=' + k }; }), ticksY: [0, 5, 10].map(function (v) { return { v: v, l: String(v) }; }), yAxisAt: 'left' });
        var cols = [];
        for (k = 0; k < 4; k++) {
          var x = ax.X(k + 1), fh = Math.min(10, floor[k]);
          var fl = A.rect(x - 30, ax.Y(fh), 38, ax.Y(0) - ax.Y(fh), 'f-line s-soft w1', null, 0);
          var wt = A.rect(x - 30, ax.Y(floor[k] + Pw[k]), 38, ax.Y(floor[k]) - ax.Y(floor[k] + Pw[k]), 'f-accs s-acc w1', null, 0);
          var wl = tx(A, x - 11, ax.Y(floor[k] + Pw[k] / 2) + 4, nm(Pw[k], 3), 'f-acc t-b', 'middle', null, 10.5);
          var ftx = tx(A, x - 11, floor[k] > 10 ? ax.Y(10) + 30 : ax.Y(fh) - 4, floor[k] > 10 ? nm(floor[k]) + ' ↑' : nm(floor[k], 2), 't-xs', 'middle');
          var eb = A.rect(x + 13, ax.Y(Pe[k]), 10, ax.Y(0) - ax.Y(Pe[k]), 'f-pur s-none', null, 1);
          var el = tx(A, x + 18, ax.Y(Pe[k]) - 4, nm(Pe[k], 2), 'f-pur', 'middle', null, 10.5);
          cols.push({ fl: fl, wt: wt, wl: wl, ftx: ftx, eb: eb, el: el });
        }
        var muL = A.line(ax.X(0.5), ax.Y(mu), ax.X(4.5), ax.Y(mu), 's-acc w1 dash');
        var muT = tx(A, ax.X(4.5), ax.Y(mu) - 4, 'μ = ' + nm(mu, 2), 'f-acc', 'end', null, 10.5);
        var capT = tx(A, 44, 146, 'C = Σ log₂(1 + |H_{k}|²P_{k}/N_{k})', 't-m');
        return {
          step: function () {},
          frame: function (ts, dt, k) {
            var pe = k === 0 ? 0 : k === 1 ? A.prog(ts, 1.4, 0.3) : 1;
            for (var q = 0; q < 4; q++) {
              var Hr = H[q][0], Hi = H[q][1], d2 = Hr * Hr + Hi * Hi;
              pts[q].forEach(function (P) {
                var s = Sx[P.s], rr = Hr * s[0] - Hi * s[1] + P.w[0], ri = Hr * s[1] + Hi * s[0] + P.w[1];
                var er = (rr * Hr + ri * Hi) / d2, ei = (ri * Hr - rr * Hi) / d2;           // R/H
                var x = A.lerp(rr, er, pe), y = A.lerp(ri, ei, pe);
                A.set(P.e, { cx: A.clamp(CXs[q] + x * sc, CXs[q] - half + 2, CXs[q] + half - 2), cy: A.clamp(cy - y * sc, cy - half + 2, cy + half - 2) });
              });
            }
            ideal.forEach(function (I) {
              var s = Sx[I.s], Hr = H[I.k][0], Hi = H[I.k][1];
              var x = A.lerp(Hr * s[0] - Hi * s[1], s[0], pe), y = A.lerp(Hr * s[1] + Hi * s[0], s[1], pe);
              A.set(I.e, { cx: CXs[I.k] + x * sc, cy: cy - y * sc });
            });
            var bot = k >= 2 ? 1 : 0.2;
            op(capT, bot);
            cols.forEach(function (c, i) {
              op(c.fl, bot); op(c.ftx, bot);
              var w = k === 3 ? A.prog(ts, 1.2, 0.2) : (k >= 4 ? 0.45 : 0);
              op(c.wt, Pw[i] > 0 ? w : 0); op(c.wl, Pw[i] > 0 ? w : 0);
              var e = k >= 4 ? A.prog(ts, 0.8, 0.2) : 0;
              op(c.eb, e); op(c.el, e);
            });
            op(muL, k === 3 ? A.prog(ts, 1.2, 0.2) : (k >= 4 ? 0.45 : 0)); op(muT, k >= 3 ? (k === 3 ? A.prog(ts, 1.2, 0.2) : 0.45) : 0);
            var notes = [
              'R<sub>k</sub> = H<sub>k</sub>s<sub>k</sub> + W<sub>k</sub>：每个子载波只是一个复数增益',
              '噪声放大 1/|H<sub>k</sub>| = ' + H.map(function (z) { return nm(1 / Math.sqrt(z[0] * z[0] + z[1] * z[1]), 2); }).join(', ') + '（时域均衡要多抽头，这里一除了事）',
              '|H<sub>k</sub>|² = ' + li(g, 2) + '，池底 1/|H<sub>k</sub>|² = ' + li(floor, 2),
              '注水 P<sub>k</sub> = ' + li(Pw, 2) + '，C = ' + nm(Cw, 2) + ' bit/OFDM 符号 = ' + nm(Cw / 4, 2) + ' bit/s/Hz',
              '紫 = 等容量 P<sub>k</sub> = ' + li(Pe, 2) + '，每个 ' + nm(Ce / 4, 2) + ' bit，共 ' + nm(Ce, 2) + ' bit/OFDM 符号（注水 ' + nm(Cw, 2) + '）'
            ];
            A.note(notes[k]);
          }
        };
      }
    });
  })();
})();
