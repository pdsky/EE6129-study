/* Part A (cellular systems), sections 7.1–10.5: SIR, Erlang B/C, trunking, cell splitting, sectoring, handoff, power control. */
(function () {
  'use strict';
  var S3 = Math.sqrt(3);
  function dB(x) { return 10 * Math.log10(x); }
  function mn(x) { return String(x).replace('-', '−'); }
  function th(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  /* Erlang B by the recursion B(m) = A·B(m−1) / (m + A·B(m−1)), B(0) = 1 */
  function erlB(M, A) { var b = 1; for (var k = 1; k <= M; k++) b = A * b / (k + A * b); return b; }
  /* offered traffic A that a pool of M channels carries at blocking g (bisection on Erlang B) */
  function erlA(M, g) { var lo = 0, hi = 3 * M + 10; for (var i = 0; i < 60; i++) { var m = (lo + hi) / 2; if (erlB(M, m) > g) hi = m; else lo = m; } return lo; }
  function erlC(M, A) { var b = erlB(M, A); return M * b / (M - A * (1 - b)); }
  /* hexagon path, radius r; rot = 0 → flat-top (vertices at 0°, 60°, …), rot = π/6 → pointy-top */
  function hexD(cx, cy, r, rot) {
    var d = '';
    for (var k = 0; k < 6; k++) { var a = (rot || 0) + k * Math.PI / 3; d += (k ? 'L' : 'M') + (cx + r * Math.cos(a)).toFixed(2) + ' ' + (cy - r * Math.sin(a)).toFixed(2); }
    return d + 'Z';
  }
  function bs(A, x, y, cls, p) { return A.poly([[x - 5, y + 6], [x + 5, y + 6], [x, y - 7]], cls || 'f-ink', p); }
  function phone(A, x, y, cls, p) { return A.rect(x - 3.5, y - 6, 7, 12, cls || 'f-ink', p, 1.5); }
  /* flat-top hex lattice (unit R): neighbours at 30° + 60°k, distance √3 */
  function latt(rmax) {
    var out = [], n = Math.ceil(rmax / 1.5) + 2;
    for (var a = -n; a <= n; a++) for (var b = -n; b <= n; b++) {
      var x = 1.5 * a, y = S3 * (b + a / 2);
      if (Math.sqrt(x * x + y * y) <= rmax + 1e-9) out.push([x, y]);
    }
    return out;
  }
  /* first-tier co-channel cell centres for cluster (i, j): i steps along a neighbour direction, turn 60°, j steps */
  function cochan(i, j) {
    var out = [];
    for (var k = 0; k < 6; k++) {
      var a = (30 + 60 * k) * Math.PI / 180, b = a + Math.PI / 3;
      out.push([S3 * (i * Math.cos(a) + j * Math.cos(b)), S3 * (i * Math.sin(a) + j * Math.sin(b))]);
    }
    return out;
  }
  var IJ = { 1: [1, 0], 3: [1, 1], 4: [2, 0], 7: [2, 1], 9: [3, 0], 12: [2, 2], 13: [3, 1] };
  function show(el, on) { el.style.display = on ? '' : 'none'; }
  function clear(g) { while (g.firstChild) g.removeChild(g.firstChild); }

  /* ================= 7.1 SIR ================= */
  ANIM.reg('A:7.1', {
    title: 'SIR：有用信号 ÷ 全部干扰之和',
    cap: '蓝 = 自己基站送来的有用信号 S，红 = 6 个同频小区的干扰。右边柱子比较 S 和干扰总和 ΣI：前几步只是示意，最后一步按 18 dB 的真实比例画。',
    h: 230, live: true, stepDur: 3.6,
    steps: [
      '手机站在自己小区的边上：自己的基站送来有用信号 S（蓝）。',
      '用同一组频率的 6 个同频小区也在发射，每一路都是干扰 I（红）。',
      '每路信号按距离的 −n 次方衰减：自己基站离 R，干扰基站离 D 左右。',
      'SIR = S / (I₁ + I₂ + … + I₆)：有用信号除以全部干扰之和，噪声先忽略。',
      '语音要求 SIR > 18 dB：10^(18/10) ≈ ' + Math.round(Math.pow(10, 1.8)) + '，S 要比干扰总和强 63 倍。'
    ],
    init: function (A) {
      var cx = 100, cy = 118, R = 26, D = 86, mx = cx + R, my = cy;
      var gI = A.g({ opacity: 0 }), src = [];
      for (var k = 0; k < 6; k++) {
        var a = (30 + 60 * k) * Math.PI / 180, x = cx + D * Math.cos(a), y = cy - D * Math.sin(a);
        A.path(hexD(x, y, 14), 'f-bads s-bad w1', gI);
        A.line(x, y, mx, my, 's-bad w1 dash op7', gI);
        bs(A, x, y, 'f-bad', gI);
        src.push([x, y]);
      }
      A.path(hexD(cx, cy, R), 'f-accs s-acc w2');
      A.line(cx, cy, mx, my, 's-acc w3');
      bs(A, cx, cy, 'f-acc');
      phone(A, mx + 1, my, 'f-ink');
      var pS = [], pI = [], j;
      for (j = 0; j < 2; j++) pS.push(A.circle(cx, cy, 2.6, 'f-acc'));
      for (j = 0; j < 12; j++) pI.push(A.circle(0, 0, 2.4, 'f-bad', gI));
      var tR = A.text(113, 110, 'R', { cls: 't-s t-b f-acc', anchor: 'middle' });
      var tD = A.text(64, 152, '≈ D', { cls: 't-s t-b f-bad', anchor: 'middle' });
      var base = 196, bw = 44, b1 = 240, b2 = 318, hS = 130;
      A.line(222, base, 392, base, 's-soft w1');
      A.rect(b1, base - hS, bw, hS, 'f-acc s-none', null, 2);
      A.text(b1 + bw / 2, base + 15, '有用 S', { cls: 't-s', anchor: 'middle' });
      A.text(b2 + bw / 2, base + 15, '干扰之和 ΣI', { cls: 't-s', anchor: 'middle' });
      var seg = [];
      for (j = 0; j < 6; j++) seg.push(A.rect(b2, base, bw, 0, 'f-bad s-card w1', null, 0));
      var tI = A.text(b2 + bw / 2, base - 6, '', { cls: 't-s', anchor: 'middle' });
      var t1 = A.text(305, 22, '', { anchor: 'middle' }), t2 = A.text(305, 40, '', { cls: 't-s', anchor: 'middle' });
      var T = 0, hReal = hS / Math.pow(10, 1.8);
      var L1 = ['S：有用信号', 'I₁ … I₆：6 路干扰', 'S ∝ R^{−n}，I ∝ D^{−n}', 'SIR = S / ΣI', '18 dB：S ≈ 63 × ΣI'];
      var L2 = ['', '同一组频率 → 同频干扰', '离得越远越弱', 'ΣI = I₁ + I₂ + … + I₆', '10^{1.8} = ' + Math.pow(10, 1.8).toFixed(1)];
      return {
        frame: function (ts, dt, k) {
          T += dt || 0;
          gI.setAttribute('opacity', k === 0 ? 0 : k === 1 ? A.prog(ts, 0.7).toFixed(2) : 1);
          for (var j = 0; j < 2; j++) A.set(pS[j], { cx: A.lerp(cx, mx, (T * 0.7 + j / 2) % 1) });
          for (j = 0; j < 12; j++) {
            var s = src[j % 6], f = (T * 0.35 + (j < 6 ? 0 : 0.5) + (j % 6) * 0.13) % 1;
            A.set(pI[j], { cx: A.lerp(s[0], mx, f), cy: A.lerp(s[1], my, f) });
          }
          var hI = k === 0 ? 0 : k < 4 ? 48 * (k === 1 ? A.prog(ts, 0.8) : 1) : A.lerp(48, hReal, A.prog(ts, 1.2));
          for (j = 0; j < 6; j++) A.set(seg[j], { y: base - hI * (j + 1) / 6, height: hI / 6, cls: k === 4 && ts > 0.6 ? 'f-bad s-bad w1' : 'f-bad s-card w1' });
          A.set(tI, { y: base - hI - 6, text: k === 0 ? '' : k < 4 ? '（示意）' : '真实比例：一条细线' });
          show(tR, k >= 2); show(tD, k >= 2);
          A.setText(t1, L1[k]); A.setText(t2, L2[k]);
        }
      };
    }
  });

  /* ================= 7.2 simplified SIR vs N ================= */
  ANIM.reg('A:7.2', {
    title: '簇越大，同频小区越远，SIR 越高',
    cap: '选簇大小 N 和路径损耗指数 n。左边按真实几何画出第一层 6 个同频小区（红），距离都是 D = √(3N)·R；右边柱子是简化算法 S/I = (√(3N))ⁿ/6 的结果，金色虚线是 18 dB 门槛。',
    h: 240,
    init: function (A) {
      var Ns = [1, 3, 4, 7, 9, 12, 13], iN = 3, n = 4, cx = 110, cy = 128;
      var map = A.g({});
      var tTop = A.text(6, 15, '', { cls: 't-s' });
      var tMin = A.text(394, 15, '', { cls: 't-s t-b', anchor: 'end' });
      var ax = A.axes({ x: 246, y: 40, w: 140, h: 162, xr: [0, 7], yr: [0, 30], yl: 'SIR (dB)', xl: 'N', ticksY: [0, 10, 18, 30],
        xAxisAt: 'bottom', yAxisAt: 'left', ticksX: Ns.map(function (N, i) { return { v: i + 0.5, l: String(N) }; }) });
      A.line(ax.X(0), ax.Y(10), ax.X(7), ax.Y(10), 's-faint w1 dash');
      A.line(ax.X(0), ax.Y(18), ax.X(7), ax.Y(18), 's-gold w2 dash');
      var bars = Ns.map(function (N, i) { return A.rect(ax.X(i + 0.2), ax.Y(0), ax.X(0.6) - ax.X(0), 0, 'f-good', null, 1); });
      var vLab = A.text(0, 0, '', { cls: 't-s t-b', anchor: 'middle' });
      function sir(N) { return dB(Math.pow(Math.sqrt(3 * N), n) / 6); }
      function draw() {
        clear(map);
        var N = Ns[iN], Q = Math.sqrt(3 * N), r = 100 / (Q + 1.95), cc = cochan(IJ[N][0], IJ[N][1]);
        latt(Q + 0.95).forEach(function (p) { A.path(hexD(cx + p[0] * r, cy - p[1] * r, r), 'f-card s-line w1', map); });
        A.path(hexD(cx, cy, r), 'f-accs s-acc w2', map);
        cc.forEach(function (p) {
          var x = cx + p[0] * r, y = cy - p[1] * r;
          A.path(hexD(x, y, r), 'f-bads s-bad w2', map);
          A.line(cx, cy, x, y, 's-bad w1 dash', map);
          A.circle(x, y, 2.4, 'f-bad', map);
        });
        A.circle(cx, cy, 2.6, 'f-acc', map);
        var p0 = cc[1], mxp = cx + p0[0] * r / 2, myp = cy - p0[1] * r / 2, L = Math.sqrt(p0[0] * p0[0] + p0[1] * p0[1]);
        A.text(mxp + 9 * p0[1] / L, myp + 9 * p0[0] / L + 4, 'D', { cls: 't-s t-b f-bad', anchor: 'middle' }, map);
        A.setText(tTop, 'N = ' + N + '（i = ' + IJ[N][0] + ', j = ' + IJ[N][1] + '）：D = ' + Q.toFixed(2) + 'R');
        var minN = null;
        Ns.forEach(function (M, i) {
          var v = sir(M), h = A.clamp(v, 0, 30);
          A.set(bars[i], { y: ax.Y(h), height: ax.Y(0) - ax.Y(h), cls: (v >= 18 ? 'f-good' : v >= 10 ? 'f-gold' : 'f-bad') + (i === iN ? ' s-ink w2' : ' s-none op7') });
          if (minN == null && v >= 18) minN = M;
        });
        var v = sir(N), qn = Math.pow(Q, n);
        A.set(vLab, { x: Math.min(ax.X(iN + 0.5), 382), y: ax.Y(A.clamp(v, 0, 30)) - 4, text: mn(v.toFixed(2)) });
        A.setText(tMin, minN ? '≥ 18 dB 的最小 N = ' + minN : 'N ≤ 13 都不到 18 dB');
        A.note('N = ' + N + '，n = ' + n + '：Q = √(3N) = √' + (3 * N) + ' = ' + Q.toFixed(3) + '<br>S/I = Qⁿ/6 = ' + qn.toFixed(1) + ' / 6 = ' + (qn / 6).toFixed(1) +
          ' → <b>' + mn(v.toFixed(2)) + ' dB</b> ' + (v >= 18 ? '≥ 18 dB ✓' : '< 18 dB ✗'));
      }
      A.choice({ label: '簇大小 N', options: Ns.map(String), value: iN, on: function (i) { iN = i; draw(); } });
      A.choice({ label: '路径损耗指数', options: ['n = 3', 'n = 4'], value: 1, on: function (i) { n = i ? 4 : 3; draw(); } });
      draw();
      return {};
    }
  });

  /* ================= 7.3 worst case ================= */
  (function () {
    var Q = Math.sqrt(21), q4 = Math.pow(Q, 4), qm = Math.pow(Q - 1, 4), qp = Math.pow(Q + 1, 4);
    var iS = 6 / q4, i1 = 2 / qm + 2 / q4 + 2 / qp, i2 = 6 / qm;
    var rows = [[1 / q4, 1 / q4, 1 / q4, 1 / q4, 1 / q4, 1 / q4], [1 / qm, 1 / qm, 1 / q4, 1 / q4, 1 / qp, 1 / qp], [1 / qm, 1 / qm, 1 / qm, 1 / qm, 1 / qm, 1 / qm]];
    var sums = [iS, i1, i2];
    ANIM.reg('A:7.3', {
      title: '最坏情况：手机在小区边上',
      cap: '上图：手机从基站走到小区边上，一边的干扰变近、另一边变远。下图：6 个干扰的强度（n = 4，每个 ∝ 距离⁻⁴）加起来，红 = D−R，金 = D，紫 = D+R。',
      h: 252,
      steps: [
        '简化算法：6 个干扰都当成在 D = ' + Q.toFixed(2) + 'R，总和 6 × 1/' + Math.round(q4) + ' = ' + iS.toFixed(4) + ' → ' + dB(1 / iS).toFixed(2) + ' dB。',
        '手机走到小区边上（离自己基站 R）：右边 2 个干扰变近，只有 D − R = ' + (Q - 1).toFixed(2) + 'R。',
        '左边 2 个变远：D + R = ' + (Q + 1).toFixed(2) + 'R；上下 2 个大致还是 D。',
        '近的每个 1/' + qm.toFixed(1) + ' = ' + (1 / qm).toFixed(5) + '（强 ' + (q4 / qm).toFixed(1) + ' 倍），远的 ' + (1 / qp).toFixed(5) + '（只弱到 ' + (q4 / qp).toFixed(2) + ' 倍）。',
        'Case 1 合计 ' + i1.toFixed(5) + '，比简化多 ' + Math.round((i1 / iS - 1) * 100) + '% → S/I = ' + (1 / i1).toFixed(1) + ' → ' + dB(1 / i1).toFixed(2) + ' dB，不到 18 dB。',
        'Case 2 更保守：6 个都按 D − R → ' + qm.toFixed(1) + ' / 6 = ' + (qm / 6).toFixed(1) + ' → ' + dB(qm / 6).toFixed(2) + ' dB。'
      ],
      init: function (A) {
        var u = 38, c0 = 200, yl = 62;
        function X(v) { return c0 + u * v; }
        A.path(hexD(c0, yl, u), 'f-accs s-acc w1');
        A.line(X(-Q), yl, X(Q), yl, 's-line w1');
        bs(A, c0, yl - 6, 'f-acc');
        bs(A, X(-Q), yl - 6, 'f-bad'); bs(A, X(Q), yl - 6, 'f-bad');
        A.text(X(-Q), yl - 20, '干扰 ×2', { cls: 't-s f-bad', anchor: 'middle' });
        A.text(X(Q), yl - 20, '干扰 ×2', { cls: 't-s f-bad', anchor: 'middle' });
        var tUD = A.text(c0, 18, '（上下方向另有 2 个干扰，距离仍约 D）', { cls: 't-s', anchor: 'middle' });
        var mob = A.g({}); phone(A, 0, 0, 'f-ink', mob);
        var dy = 104, dL = A.line(0, dy, 0, dy, 's-soft w1'), dR = A.line(0, dy, 0, dy, 's-soft w1');
        var tk = [A.line(X(-Q), dy - 4, X(-Q), dy + 4, 's-soft w1'), A.line(0, dy - 4, 0, dy + 4, 's-soft w1'), A.line(X(Q), dy - 4, X(Q), dy + 4, 's-soft w1')];
        var lL = A.text(0, dy - 5, '', { cls: 't-s', anchor: 'middle' }), lR = A.text(0, dy - 5, '', { cls: 't-s', anchor: 'middle' });
        A.text(8, 126, '6 个干扰之和（n = 4，距离以 R 计）', { cls: 't-s' });
        [['f-bad', 'D−R', 286], ['f-gold', 'D', 326], ['f-pur', 'D+R', 352]].forEach(function (c) {
          A.rect(c[2], 118, 8, 8, c[0] + ' s-none', null, 1); A.text(c[2] + 11, 126, c[1], { cls: 't-s' });
        });
        var yR = [134, 174, 214], x0 = 62, sc = 215 / i2, segs = [], tS = [], tDb = [], tSI = [];
        var nm = ['简化', 'Case 1', 'Case 2'];
        for (var r = 0; r < 3; r++) {
          A.text(8, yR[r] + 13, nm[r], { cls: 't-s t-b' });
          var row = [];
          for (var j = 0; j < 6; j++) {
            var v = rows[r][j];
            row.push(A.rect(x0, yR[r], 0, 18, (v === 1 / qm ? 'f-bad' : v === 1 / q4 ? 'f-gold' : 'f-pur') + ' s-card w1', null, 0));
          }
          segs.push(row);
          tS.push(A.text(x0, yR[r] + 31, 'ΣI = ' + sums[r].toFixed(r === 0 ? 4 : 5) + (r === 1 ? '（+' + Math.round((i1 / iS - 1) * 100) + '%）' : ''), { cls: 't-s' }));
          tDb.push(A.text(286, yR[r] + 13, dB(1 / sums[r]).toFixed(2) + ' dB', { cls: 't-b' + (dB(1 / sums[r]) >= 18 ? ' f-good' : ' f-bad') }));
          tSI.push(A.text(286, yR[r] + 28, 'S/I = ' + (1 / sums[r]).toFixed(1), { cls: 't-s' }));
        }
        var tMid = A.text(286, yR[1] + 13, '', { cls: 't-s' }), tMid2 = A.text(286, yR[1] + 27, '', { cls: 't-s' });
        return {
          frame: function (ts, dt, k) {
            var p = A.prog(ts, 0.9), mu = k === 0 ? 0 : k === 1 ? p : 1, mx = X(mu);
            mob.setAttribute('transform', 'translate(' + mx.toFixed(1) + ',' + (yl + 8) + ')');
            A.set(dL, { x1: X(-Q), x2: mx }); A.set(dR, { x1: mx, x2: X(Q) }); A.set(tk[1], { x1: mx, x2: mx });
            A.set(lL, { x: (X(-Q) + mx) / 2, text: k >= 2 ? 'D + R = ' + (Q + 1).toFixed(2) + 'R' : 'D = ' + Q.toFixed(2) + 'R', cls: k >= 2 ? 't-s t-b f-pur' : 't-s' });
            A.set(lR, { x: (X(Q) + mx) / 2, text: k >= 1 ? 'D − R = ' + (Q - 1).toFixed(2) + 'R' : 'D = ' + Q.toFixed(2) + 'R', cls: k >= 1 ? 't-s t-b f-bad' : 't-s' });
            show(tUD, k >= 2);
            for (var r = 0; r < 3; r++) {
              var x = x0;
              for (var j = 0; j < 6; j++) {
                var full = rows[r][j] * sc, vis = 1;
                if (r === 1) vis = k === 0 ? 0 : k === 1 ? (j < 2 ? p : 0) : k === 2 ? (j < 2 ? 1 : p) : 1;
                if (r === 2) vis = k < 5 ? 0 : p;
                A.set(segs[r][j], { x: x, width: full * vis }); x += full * vis;
              }
            }
            show(tS[1], k >= 4); show(tDb[1], k >= 4); show(tSI[1], k >= 4);
            show(tS[2], k >= 5); show(tDb[2], k >= 5); show(tSI[2], k >= 5);
            A.setText(tMid, k === 3 ? '近：×' + (q4 / qm).toFixed(1) + '（多 ' + (1 / qm - 1 / q4).toFixed(4) + '）' : '');
            A.setText(tMid2, k === 3 ? '远：×' + (q4 / qp).toFixed(2) + '（少 ' + (1 / q4 - 1 / qp).toFixed(4) + '）' : '');
          }
        };
      }
    });
  })();

  /* ================= 7.4 FCA vs borrowing / DCA ================= */
  ANIM.reg('A:7.4', {
    title: '固定分配 FCA vs 信道借用 / DCA',
    cap: '每列是一个蜂窝的信道：蓝 = 正在通话，白 = 空闲。看 A 蜂窝忙不过来时，FCA 和借用 / DCA 各怎么处理。',
    h: 222,
    steps: [
      'FCA：每个蜂窝预先分到固定的一组信道（这里各 4 条），只能用自己的。',
      '话务不均：A 的 4 条全忙，第 5 个呼叫被阻塞——而 B 还空着 3 条。',
      '信道借用：A 向邻居 B 借一条空闲信道 f8，第 5 个呼叫接通。',
      '借之前要检查：复用距离内没有小区正在用 f8，否则会产生同频干扰。',
      '通话结束，借来的 f8 要还给 B。',
      'DCA：信道不固定属于谁，MSC 按需从公共池分配。更灵活，但调度更复杂。'
    ],
    init: function (A) {
      var xs = [75, 200, 325], nm = ['A', 'B', 'C'], busy0 = [4, 1, 2], sy = [56, 80, 104, 128], sw = 80, sh = 20;
      var pool = A.rect(22, 48, 360, 128, 'f-none s-pur w2 dash', null, 10);
      var slots = [], stat = [];
      for (var c = 0; c < 3; c++) {
        A.path(hexD(xs[c], 26, 20), 'f-card s-soft w1');
        A.text(xs[c], 31, nm[c], { cls: 't-b', anchor: 'middle' });
        for (var i = 0; i < 4; i++) {
          slots.push(A.rect(xs[c] - sw / 2, sy[i], sw, sh, 'f-card s-line w1', null, 4));
          A.text(xs[c] - sw / 2 + 5, sy[i] + 14, 'f' + (4 * c + i + 1), { cls: 't-s t-m' });
          stat.push(A.text(xs[c] + 12, sy[i] + 14, '', { cls: 't-s', anchor: 'middle' }));
        }
      }
      var bor = A.g({}); A.rect(-sw / 2, 0, sw, sh, 'f-golds s-gold w2', bor, 4);
      A.text(-sw / 2 + 5, 14, 'f8', { cls: 't-s t-m t-b', }, bor); var borT = A.text(12, 14, '', { cls: 't-s', anchor: 'middle' }, bor);
      var call = A.g({}); var callP = phone(A, 0, 0, 'f-bad', call); var callT = A.text(-14, 24, '', { cls: 't-s t-b' }, call);
      var b1 = A.text(200, 200, '', { cls: 't-s t-b', anchor: 'middle' }), b2 = A.text(200, 216, '', { cls: 't-s', anchor: 'middle' });
      var B1 = ['FCA：各蜂窝信道固定，互不相借', 'A 全忙 → 第 5 个呼叫被阻塞', '借用：B 的空闲信道 f8 借给 A', '条件：复用距离内没有小区在用 f8', '通话结束 → f8 还给 B', 'DCA：所有信道放进公共池，MSC 按需分配'];
      var B2 = ['', 'B 还空着 3 条，FCA 下借不到', '', '否则借来的信道会造成同频干扰', '', '只要满足复用距离约束，谁需要谁用'];
      var fromX = xs[1], fromY = sy[3], toX = xs[0], toY = 152;
      return {
        frame: function (ts, dt, k) {
          var p = A.prog(ts, 1.0);
          for (var c = 0; c < 3; c++) for (var i = 0; i < 4; i++) {
            var id = 4 * c + i, busy = i < busy0[c] && (k > 0 || c !== 0 || p * 4 > i);
            var lent = c === 1 && i === 3 && (k === 2 || k === 3 || (k === 4 && p < 1));
            var hl = k === 1 && c === 1 && i >= busy0[1];
            A.set(slots[id], { cls: busy ? 'f-accs s-acc w1' : hl ? 'f-golds s-gold w2' : 'f-card s-line w1' });
            A.setText(stat[id], busy ? '● 通话中' : lent ? '借出' : '空闲');
          }
          var bx = fromX, by = fromY, bo = 0;
          if (k === 2) { bx = A.lerp(fromX, toX, p); by = A.lerp(fromY, toY, p); bo = 1; }
          if (k === 3) { bx = toX; by = toY; bo = 1; }
          if (k === 4) { bx = A.lerp(toX, fromX, p); by = A.lerp(toY, fromY, p); bo = p < 1 ? 1 : 0; }
          bor.setAttribute('transform', 'translate(' + bx.toFixed(1) + ',' + by.toFixed(1) + ')');
          bor.setAttribute('opacity', bo);
          A.setText(borT, k === 3 ? '✓ 无干扰' : k === 2 && p > 0.95 ? '● 通话中' : '借来');
          call.setAttribute('transform', 'translate(18,162)');
          call.setAttribute('opacity', k >= 1 && k <= 3 ? 1 : 0);
          A.set(callP, { cls: k === 1 ? 'f-bad' : 'f-good' });
          A.set(callT, { text: '第 5 个呼叫 ' + (k === 1 ? '✗ 阻塞' : '✓ 接通'), cls: 't-s t-b ' + (k === 1 ? 'f-bad' : 'f-good') });
          show(pool, k === 5);
          A.setText(b1, B1[k]); A.setText(b2, B2[k]);
        }
      };
    }
  });

  /* ================= 8.1 queueing: random arrivals, M servers ================= */
  ANIM.reg('A:8.1', {
    title: '随机到达 + 有限信道 = 排队问题',
    cap: '每个圆点是一个呼叫：随机到达，占一条信道（服务台）打一段随机时长，蓝条是剩余通话时间。信道全忙时：<b>Erlang B</b> 直接阻塞、清除；<b>Erlang C</b> 排队等空出来的信道。',
    h: 222, seed: 160,
    init: function (A) {
      var M = 5, lam = 0.9, H = 4, Aoff = lam * H, mode = 0;
      var arr = [], hold = [], t = 0.8;
      while (t < 34) { arr.push(t); hold.push(A.clamp(-H * Math.log(1 - A.rand()), 0.8, 12)); t += -Math.log(1 - A.rand()) / lam; }
      function sim(queue) {
        var free = [], out = [], s;
        for (s = 0; s < M; s++) free.push(0);
        for (var i = 0; i < arr.length; i++) {
          var f = -1;
          for (s = 0; s < M; s++) if (free[s] <= arr[i]) { f = s; break; }
          if (f < 0 && !queue) { out.push({ a: arr[i], blk: true }); continue; }
          if (f < 0) { f = 0; for (s = 1; s < M; s++) if (free[s] < free[f]) f = s; }
          var st = Math.max(arr[i], free[f]); free[f] = st + hold[i];
          out.push({ a: arr[i], s: f, st: st, en: free[f] });
        }
        return out;
      }
      var sch = [sim(false), sim(true)];
      var cyc = sch.map(function (c) { var m = 0; c.forEach(function (x) { m = Math.max(m, x.blk ? x.a + 1.6 : x.en + 0.8); }); return m + 1; });
      var SX = 16, GX = 118, GY = 100, LX = 150, LW = 170, QY = 186;
      function ly(s) { return 36 + s * 26; }
      A.circle(SX, GY, 6, 'f-none s-acc w1');
      A.text(4, GY + 22, '随机到达', { cls: 't-s' });
      A.line(GX, GY - 16, GX, GY + 16, 's-soft w2');
      A.text(GX - 6, GY - 22, '有空信道？', { cls: 't-s', anchor: 'middle' });
      A.text(LX, 30, '信道（服务台）', { cls: 't-s' });
      A.text(394, 30, '挂断 →', { cls: 't-s', anchor: 'end' });
      var bars = [];
      for (var s = 0; s < M; s++) {
        A.rect(LX, ly(s), LW, 18, 'f-card s-line w1', null, 3);
        A.text(LX - 5, ly(s) + 13, String(s + 1), { cls: 't-s', anchor: 'end' });
        bars.push(A.rect(LX + 22, ly(s) + 3, 0, 12, 'f-accs s-acc w1', null, 2));
      }
      var binT = A.text(GX, QY + 26, '', { cls: 't-s', anchor: 'middle' });
      var stat = A.text(4, 14, '', { cls: 't-s' }), theo = A.text(394, 14, '', { cls: 't-s', anchor: 'end' });
      var dots = [];
      for (var i = 0; i < 30; i++) dots.push(A.circle(0, 0, 5, 'f-acc'));
      function setMode(i) {
        mode = i;
        A.setText(binT, i ? '排队等待（Erlang C）' : '阻塞 → 清除（Erlang B）');
        A.setText(theo, 'A = λH = ' + Aoff.toFixed(1) + ' E，理论 ' + (i ? 'P(等待) = ' + (100 * erlC(M, Aoff)).toFixed(0) : 'P_{B} = ' + (100 * erlB(M, Aoff)).toFixed(0)) + '%');
      }
      A.choice({ label: '信道全忙时', options: ['阻塞清除（Erlang B）', '排队等待（Erlang C）'], value: 0, on: function (i) { setMode(i); A.redraw(); } });
      setMode(0);
      return function frame(t) {
        var c = sch[mode], tt = t % cyc[mode], nd = 0, na = 0, nb = 0, s;
        for (s = 0; s < M; s++) A.set(bars[s], { width: 0 });
        for (var i = 0; i < c.length; i++) {
          var x = c[i], pos = null, cls = 'f-acc', op = 1;
          if (x.a <= tt) { na++; if (x.blk || x.st > x.a + 1e-9) nb++; }
          if (tt < x.a - 1.2) continue;
          if (tt < x.a) { var f = A.ease((tt - x.a + 1.2) / 1.2); pos = [A.lerp(SX, GX, f), GY]; }
          else if (x.blk) {
            if (tt > x.a + 1.6) continue;
            pos = [GX, A.lerp(GY, QY, A.ease((tt - x.a) / 0.8))]; cls = 'f-bad'; op = 1 - A.clamp((tt - x.a - 0.9) / 0.7, 0, 1);
          } else if (tt < x.st) {
            var q = 0;
            for (var j = 0; j < i; j++) if (c[j].a <= tt && c[j].st > tt) q++;
            var qx = GX - 14 * q, g = A.ease((tt - x.a) / 0.5);
            pos = [A.lerp(GX, qx, g), A.lerp(GY, QY, g)]; cls = 'f-gold';
          } else if (tt < x.en) {
            var h = A.ease((tt - x.st) / 0.4), fx = x.st > x.a + 1e-9 ? GX : GX, fy = x.st > x.a + 1e-9 ? QY : GY;
            pos = [A.lerp(fx, LX + 11, h), A.lerp(fy, ly(x.s) + 9, h)];
            A.set(bars[x.s], { width: (LW - 26) * (x.en - tt) / 12 });
          } else if (tt < x.en + 0.7) {
            var e = (tt - x.en) / 0.7; pos = [A.lerp(LX + 11, 392, e), ly(x.s) + 9]; op = 1 - e;
          } else continue;
          if (nd < dots.length) { A.set(dots[nd], { cx: pos[0], cy: pos[1], cls: cls, opacity: op.toFixed(2) }); dots[nd].style.display = ''; nd++; }
        }
        for (; nd < dots.length; nd++) dots[nd].style.display = 'none';
        A.setText(stat, '到达 ' + na + ' · ' + (mode ? '要排队 ' : '被阻塞 ') + nb + (na ? '（' + Math.round(100 * nb / na) + '%）' : ''));
      };
    }
  });

  /* ================= 8.2 Erlang: A = λH ================= */
  ANIM.reg('A:8.2', {
    title: '话务量 A = λH（Erlang）',
    cap: '一小时里随机来了 100 个电话，每个 3 分钟（每条横条是一通电话）。光标扫过时，下图是“此刻同时在线的通话数”，它的平均值正好是 A = λH = 5 Erlang。',
    h: 232, seed: 82,
    init: function (A) {
      var NC = 100, Hm = 3, st = [], lane = [], laneEnd = [], i, l;
      for (i = 0; i < NC; i++) st.push(A.rand() * (60 - Hm));
      st.sort(function (a, b) { return a - b; });
      st.forEach(function (s) { for (l = 0; l < laneEnd.length; l++) if (laneEnd[l] <= s) break; laneEnd[l] = s + Hm; lane.push(l); });
      var L = laneEnd.length, gy = 40, lh = Math.min(9, 92 / L);
      function X(m) { return 40 + m / 60 * 340; }
      function nAt(t) { var c = 0; for (var i = 0; i < NC; i++) if (st[i] <= t && t < st[i] + Hm) c++; return c; }
      var pts = [], mx = 0;
      for (i = 0; i <= 600; i++) { var v = nAt(i / 10); pts.push([i / 10, v]); mx = Math.max(mx, v); }
      A.text(6, 14, 'λ = 100 次/小时，H = 3 分钟 = 1/20 小时 → A = λH = 5 Erlang', { cls: 't-s' });
      var stat = A.text(6, 31, '', { cls: 't-s t-b' });
      A.text(8, gy + 10, '通话', { cls: 't-s' });
      var rs = st.map(function (s, i) { return A.rect(X(s), gy + lane[i] * lh, 0, lh - 1.5, 'f-acc s-none', null, 1); });
      var ax = A.axes({ x: 40, y: 150, w: 340, h: 56, xr: [0, 60], yr: [0, Math.max(12, mx + 1)], yl: '同时在线数', ticksY: [0, 5, 10],
        ticksX: [0, 15, 30, 45, { v: 60, l: '60 min' }], xAxisAt: 'bottom', yAxisAt: 'left' });
      A.line(X(0), ax.Y(5), X(60), ax.Y(5), 's-gold w2 dash');
      A.text(X(60), ax.Y(5) - 4, '平均 = 5', { cls: 't-s t-b f-gold', anchor: 'end' });
      var cur = A.curve(ax, [[0, 0]], 's-acc w2');
      var cursor = A.line(0, gy - 4, 0, 206, 's-ink w1');
      return function frame(t) {
        var tm = Math.min(60, (t % 14) * 5), area = 0;
        for (var i = 0; i < NC; i++) {
          var w = A.clamp(tm - st[i], 0, Hm);
          A.set(rs[i], { width: w / 60 * 340 }); area += w;
        }
        A.setCurve(cur, ax, pts.slice(0, Math.floor(tm * 10) + 1));
        A.set(cursor, { x1: X(tm), x2: X(tm) });
        A.setText(stat, tm >= 60 ? '平均 = 100 × 3 分钟 / 60 分钟 = ' + (area / 60).toFixed(2) + ' Erlang ✓'
          : 't = ' + Math.floor(tm) + ' 分钟 · 此刻在线 ' + nAt(tm) + ' · 到目前平均 ' + (tm > 0.5 ? (area / tm).toFixed(2) : '—'));
      };
    }
  });

  /* ================= 8.3 Erlang B + Singa / Mobi / Hubba ================= */
  (function () {
    var ops = [{ n: 'Singa', c: 380, M: 20, A: 13 }, { n: 'Mobi', c: 100, M: 60, A: 50 }, { n: 'Hubba', c: 60, M: 100, A: 90 }], pu = 0.25, pop = 1200000;
    var tot = 0;
    ops.forEach(function (o) { o.u = Math.round(o.A / pu); o.tot = o.u * o.c; tot += o.tot; });
    var pct = (100 * tot / pop).toFixed(2);
    ANIM.reg('A:8.3', {
      title: 'Erlang B：全忙就阻塞，查表算用户数',
      cap: '上面一排格子是一个蜂窝的 M 条信道。表里的 A 是课件例题查 Erlang B 表（GoS = 2%）得到的值；每用户 0.25 Erlang（每小时 3 次、每次 5 分钟）。',
      h: 248,
      steps: [
        'Erlang B：M 条信道全忙时，新呼叫直接被阻塞、清除，不排队。阻塞概率就是 GoS。',
        '例题：GoS = 2%，每用户 0.25 E。Singa 每蜂窝 M = 20，查 B 表：A = 13 E。',
        'Singa：13 / 0.25 = ' + ops[0].u + ' 用户/蜂窝，× 380 蜂窝 = ' + th(ops[0].tot) + ' 用户。',
        'Mobi：M = 60 → A = 50 E → ' + ops[1].u + ' 用户/蜂窝 × 100 = ' + th(ops[1].tot) + ' 用户。',
        'Hubba：M = 100 → A = 90 E → ' + ops[2].u + ' 用户/蜂窝 × 60 = ' + th(ops[2].tot) + ' 用户。',
        '合计 ' + th(tot) + ' 用户 = 120 万人口的 ' + pct + '%。蜂窝信道越多，每条信道服务的人越多。'
      ],
      init: function (A) {
        var cells = [], i;
        for (i = 0; i < 100; i++) cells.push(A.rect(0, 0, 0, 0, 'f-card s-line w1', null, 1));
        var sLab = A.text(10, 14, '', { cls: 't-s' });
        var call = A.g({}); phone(A, 0, 0, 'f-bad', call); A.text(0, 22, '✗ 阻塞', { cls: 't-s t-b f-bad', anchor: 'middle' }, call);
        var aLab = A.text(364, 44, '', { cls: 't-s t-b f-acc', anchor: 'middle' });
        var xs = [170, 258, 346], ry = [104, 123, 142, 161, 180, 199];
        var hl = A.rect(0, 70, 80, 136, 'f-golds s-none', null, 6);
        ['蜂窝数', '每蜂窝信道 M', '查表 A（GoS 2%）', '用户/蜂窝 = A/0.25', '总用户', '每条信道的用户'].forEach(function (s, r) { A.text(8, ry[r], s, { cls: 't-s' }); });
        A.line(6, 90, 394, 90, 's-line w1');
        var cellT = ops.map(function (o, c) {
          A.text(xs[c], 84, o.n, { cls: 't-b', anchor: 'middle' });
          return [String(o.c), String(o.M), o.A + ' E', String(o.u), th(o.tot), (o.u / o.M).toFixed(2)].map(function (s, r) {
            return A.text(xs[c], ry[r], s, { cls: r === 4 ? 't-b t-m' : r === 5 ? 't-m f-good' : 't-m', anchor: 'middle' });
          });
        });
        var sum1 = A.text(8, 222, '合计 ' + ops.map(function (o) { return th(o.tot); }).join(' + ') + ' = ' + th(tot) + ' 用户', { cls: 't-s' });
        var sum2 = A.text(8, 240, '= 120 万人口的 ' + pct + '%，Hubba 蜂窝最少却服务最多', { cls: 't-s t-b f-good' });
        function layout(M, k, p) {
          var rows = M > 20 ? 2 : 1, per = M / rows, gap = M > 60 ? 1 : 2, w = (320 - gap * (per - 1)) / per, h = rows === 1 ? 30 : 15;
          for (var i = 0; i < 100; i++) {
            if (i >= M) { cells[i].style.display = 'none'; continue; }
            cells[i].style.display = '';
            var r = Math.floor(i / per), c = i % per;
            A.set(cells[i], { x: 10 + c * (w + gap), y: 22 + r * (h + 3), width: w, height: h, cls: k === 0 ? (i < p * M ? 'f-acc s-none' : 'f-card s-line w1') : 'f-accs s-acc w1' });
          }
        }
        return {
          frame: function (ts, dt, k) {
            var o = k <= 2 ? ops[0] : k === 3 ? ops[1] : ops[2], p = A.prog(ts, 1.4);
            layout(o.M, k, p);
            A.setText(sLab, k === 0 ? (p < 1 ? 'M = 20 条信道陆续被占用…' : 'M = 20 条全忙：第 21 个呼叫进来') : o.n + '：每蜂窝 M = ' + o.M + ' 条信道');
            call.setAttribute('transform', 'translate(364,32)');
            call.setAttribute('opacity', k === 0 ? A.prog(ts, 0.5, 1.4).toFixed(2) : 0);
            A.setText(aLab, k === 0 ? '' : 'A = ' + o.A + ' E');
            for (var c = 0; c < 3; c++) for (var r = 0; r < 6; r++) {
              var at = c === 0 ? (r < 3 ? 1 : 2) : c + 2;
              cellT[c][r].setAttribute('opacity', k >= at ? 1 : 0);
            }
            var ci = k === 0 ? -1 : k <= 2 ? 0 : k === 3 ? 1 : k === 4 ? 2 : -1;
            show(hl, ci >= 0); if (ci >= 0) A.set(hl, { x: xs[ci] - 42, width: 84 });
            show(sum1, k === 5); show(sum2, k === 5);
          }
        };
      }
    });
  })();

  /* ================= 8.4 trunking efficiency ================= */
  ANIM.reg('A:8.4', {
    title: '集群增益：信道合起来用更划算',
    cap: '同样的 GoS 下，把两个各 M 条信道的小池合成一个 2M 条的大池，能承载的话务量更多。左图：中继效率 η = A/M（每条信道平均承载的话务量）随 M 上升。数值由 Erlang B 递推算出。8.3 例题里信道 20 → 100（×5），用户 52 → 360（×6.9）也是这个道理。',
    h: 236,
    init: function (A) {
      var M = 10, g = 0.02, gs = [0.01, 0.02, 0.05];
      A.text(6, 14, '中继效率 η = A/M', { cls: 't-s' });
      var ax = A.axes({ x: 36, y: 34, w: 168, h: 160, xr: [0, 110], yr: [0, 1], xl: 'M', yl: 'η', ticksX: [0, 20, 50, 100], ticksY: [0, 0.5, 1], xAxisAt: 'bottom', yAxisAt: 'left' });
      var curve = A.curve(ax, [[0, 0]], 's-acc w2');
      var m1 = A.circle(0, 0, 4.5, 'f-acc s-card w1'), m2 = A.circle(0, 0, 4.5, 'f-good s-card w1');
      var l1 = A.text(0, 0, 'M', { cls: 't-s t-b f-acc' }), l2 = A.text(0, 0, '2M', { cls: 't-s t-b f-good', anchor: 'middle' });
      var base = 194, top = 56, bxa = 250, bxb = 330, bw = 50;
      A.line(236, base, 394, base, 's-soft w1');
      var ba1 = A.rect(bxa, base, bw, 0, 'f-acc s-card w1', null, 0), ba2 = A.rect(bxa, base, bw, 0, 'f-acc s-card w1', null, 0);
      var bb = A.rect(bxb, base, bw, 0, 'f-good s-none', null, 0);
      var va = A.text(bxa + bw / 2, 0, '', { cls: 't-s t-b', anchor: 'middle' }), vb = A.text(bxb + bw / 2, 0, '', { cls: 't-s t-b', anchor: 'middle' });
      var la = A.text(bxa + bw / 2, base + 14, '', { cls: 't-s', anchor: 'middle' }), lb = A.text(bxb + bw / 2, base + 14, '', { cls: 't-s', anchor: 'middle' });
      A.text(bxa + bw / 2, base + 27, '分开用', { cls: 't-s', anchor: 'middle' }); A.text(bxb + bw / 2, base + 27, '合起来用', { cls: 't-s', anchor: 'middle' });
      var gain = A.text(315, 22, '', { cls: 't-b f-good', anchor: 'middle' }), gT = A.text(315, 38, '', { cls: 't-s', anchor: 'middle' });
      function draw() {
        var pts = [];
        for (var m = 1; m <= 110; m++) pts.push([m, erlA(m, g) / m]);
        A.setCurve(curve, ax, pts);
        var a1 = erlA(M, g), a2 = erlA(2 * M, g);
        A.set(m1, { cx: ax.X(M), cy: ax.Y(a1 / M) }); A.set(m2, { cx: ax.X(2 * M), cy: ax.Y(a2 / (2 * M)) });
        A.set(l1, { x: ax.X(M) + 7, y: ax.Y(a1 / M) + 12 }); A.set(l2, { x: ax.X(2 * M), y: ax.Y(a2 / (2 * M)) - 8 });
        var sc = (base - top) / (a2 * 1.05), h1 = a1 * sc;
        A.set(ba1, { y: base - h1, height: h1 }); A.set(ba2, { y: base - 2 * h1, height: h1 }); A.set(bb, { y: base - a2 * sc, height: a2 * sc });
        A.set(va, { y: base - 2 * h1 - 5, text: (2 * a1).toFixed(1) + ' E' }); A.set(vb, { y: base - a2 * sc - 5, text: a2.toFixed(1) + ' E' });
        A.setText(la, '2 个 × ' + M + ' 条'); A.setText(lb, '1 个 × ' + 2 * M + ' 条');
        A.setText(gain, '多承载 ' + Math.round(100 * (a2 / (2 * a1) - 1)) + '%');
        A.setText(gT, '同样 GoS = ' + Math.round(g * 100) + '%，同样 ' + 2 * M + ' 条信道');
        A.note('两个池各 ' + M + ' 条：2 × ' + a1.toFixed(2) + ' = ' + (2 * a1).toFixed(2) + ' E（η = ' + (a1 / M).toFixed(2) + '）<br>合成 1 个 ' + 2 * M + ' 条：' + a2.toFixed(2) + ' E（η = ' + (a2 / (2 * M)).toFixed(2) + '）');
      }
      A.slider({ label: '每个小池 M', min: 2, max: 50, step: 1, value: M, fmt: function (v) { return v + ' 条'; }, on: function (v) { M = v; draw(); } });
      A.choice({ label: 'GoS', options: ['1%', '2%', '5%'], value: 1, on: function (i) { g = gs[i]; draw(); } });
      draw();
      return {};
    }
  });

  /* ================= 8.5 Erlang C: M/M/M state diagram ================= */
  ANIM.reg('A:8.5', {
    title: 'Erlang C：状态图与排队概率',
    cap: '状态 k = 系统里的呼叫数。上箭头 λ：来一个呼叫；下箭头：一通电话结束，k 条在通话时速率 kμ，k ≥ M 时最多 M 条在服务，所以是 Mμ。割线两边概率流相等：Pₖ·λ = Pₖ₊₁·min(k+1, M)·μ。金色柱 = 信道全忙要排队，加起来就是 P<sub>D</sub>。',
    h: 250,
    init: function (A) {
      var M = 5, Av = 3, K = 13, i;
      A.text(6, 14, 'M/M/M 状态图（M = 5 条信道）', { cls: 't-s' });
      function nx(i) { return 24 + i * 44; }
      var ny = 52;
      for (i = 0; i <= 7; i++) {
        A.circle(nx(i), ny, 12, (i >= M ? 'f-golds s-gold' : 'f-accs s-acc') + ' w1');
        A.text(nx(i), ny + 4, String(i), { cls: 't-s t-b', anchor: 'middle' });
      }
      A.text(nx(8) - 4, ny + 4, '…', { anchor: 'middle' });
      for (i = 0; i < 8; i++) {
        var x1 = nx(i) + 13, x2 = i < 7 ? nx(i + 1) - 13 : nx(8) - 14;
        A.arrow(x1, ny - 5, x2, ny - 5, 's-acc w1', null, 4);
        A.arrow(x2, ny + 5, x1, ny + 5, 's-soft w1', null, 4);
        A.text((x1 + x2) / 2, ny - 10, 'λ', { cls: 't-s', anchor: 'middle' });
        var c = Math.min(i + 1, M);
        A.text((x1 + x2) / 2, ny + 19, (c === 1 ? '' : c) + 'μ', { cls: 't-s', anchor: 'middle' });
      }
      A.text(6, 90, 'k ≥ M（金色）：5 条信道全忙，新来的呼叫排队', { cls: 't-s' });
      var ax = A.axes({ x: 36, y: 112, w: 340, h: 96, xr: [-0.5, K - 0.5], yr: [0, 0.4], xl: 'k', yl: 'P_{k}',
        ticksX: [0, 5, 10].map(function (v) { return { v: v, l: String(v) }; }), ticksY: [0, 0.2, 0.4], xAxisAt: 'bottom', yAxisAt: 'left' });
      var bw = (ax.X(1) - ax.X(0)) * 0.7, bars = [];
      for (i = 0; i < K; i++) bars.push(A.rect(ax.X(i) - bw / 2, ax.Y(0), bw, 0, (i >= M ? 'f-gold' : 'f-acc') + ' s-none', null, 1));
      var tPD = A.text(376, 126, '', { cls: 't-s t-b f-gold', anchor: 'end' });
      function fact(n) { var f = 1; for (var j = 2; j <= n; j++) f *= j; return f; }
      function draw() {
        var rho = Av / M, u = [], head = 0, k;
        for (k = 0; k < K; k++) u.push(k <= M ? Math.pow(Av, k) / fact(k) : u[M] * Math.pow(rho, k - M));
        for (k = 0; k < M; k++) head += u[k];
        var tail = u[M] / (1 - rho), P0 = 1 / (head + tail), PD = tail * P0;
        for (k = 0; k < K; k++) { var h = ax.Y(0) - ax.Y(Math.min(0.4, u[k] * P0)); A.set(bars[k], { y: ax.Y(0) - h, height: h }); }
        A.setText(tPD, 'P_{D} = P(k ≥ 5) = ' + (100 * PD).toFixed(1) + '%');
        A.note('A = ' + Av.toFixed(1) + ' E，ρ = A/M = ' + rho.toFixed(2) + '（必须 &lt; 1，否则队列越排越长）<br>P₀ = ' + P0.toFixed(4) + ' · <b>P<sub>D</sub> = C(5, A) = ' + (100 * PD).toFixed(1) + '%</b><br>同样条件按 Erlang B 只算阻塞：' + (100 * erlB(M, Av)).toFixed(1) + '%');
      }
      A.slider({ label: '话务量 A', min: 1, max: 4.8, step: 0.1, value: Av, fmt: function (v) { return v.toFixed(1) + ' E'; }, on: function (v) { Av = v; draw(); } });
      draw();
      return {};
    }
  });

  /* ================= 9.1 cell splitting ================= */
  ANIM.reg('A:9.1', {
    title: '小区分裂：半径减半，容量 ×4',
    cap: '4:1 分裂：新基站（金点）放在两个旧基站连线的中点，微蜂窝半径 R/2。最后一步手机沿虚线走一趟：蓝点 = 穿过大蜂窝边界，红点 = 穿过微蜂窝边界（几何上只多约 2 倍，课件给的经验值是半径 ÷4 时切换约 ×10）。',
    h: 250, live: true,
    steps: [
      '拥挤区域的大蜂窝：半径 R，每个基站固定 60 条信道。',
      '4:1 分裂：在两个旧基站连线的中点加新基站，新半径 R/2，面积变 1/4。',
      '蜂窝边缘功率要不变：P<sub>t2</sub> = P<sub>t1</sub>·(1/2)⁴ = P<sub>t1</sub>/16，即降 ' + dB(16).toFixed(2) + ' dB（n = 4）。',
      '原来 1 个蜂窝的面积里有 4 个微蜂窝，各 60 条：49.6 E → ' + (4 * 49.6).toFixed(1) + ' E，正好 ×4。',
      '代价：要建很多新基站；蜂窝越小，手机越频繁穿过边界，切换变多。'
    ],
    init: function (A) {
      var cx = 118, cy = 125, R = 46, i;
      var big = [[0, 0]], mic = [[0, 0]];
      for (i = 0; i < 6; i++) {
        var a = (30 + 60 * i) * Math.PI / 180, b = 60 * i * Math.PI / 180;
        big.push([S3 * Math.cos(a), S3 * Math.sin(a)]);
        mic.push([S3 / 2 * Math.cos(a), S3 / 2 * Math.sin(a)]);
      }
      for (i = 0; i < 6; i++) mic.push([1.5 * Math.cos(i * Math.PI / 3), 1.5 * Math.sin(i * Math.PI / 3)]);
      function P(p) { return [cx + p[0] * R, cy - p[1] * R]; }
      big.forEach(function (p) { var q = P(p); A.path(hexD(q[0], q[1], R), 'f-card s-soft w2'); });
      var gM = A.g({});
      mic.forEach(function (p) { var q = P(p); A.path(hexD(q[0], q[1], R / 2), 'f-golds s-gold w1', gM); });
      var hl = A.path(hexD(cx, cy, R), 'f-none s-acc w3');
      big.forEach(function (p) { var q = P(p); bs(A, q[0], q[1], 'f-ink'); });
      mic.forEach(function (p, j) { if (j) { var q = P(p); A.circle(q[0], q[1], 2.8, 'f-gold', gM); } });
      var yr = 0.25, xr0 = -1.85, xr1 = 1.85;
      function near(set, x) { var bi = 0, bd = 1e9; set.forEach(function (p, j) { var d = (p[0] - x) * (p[0] - x) + (p[1] - yr) * (p[1] - yr); if (d < bd) { bd = d; bi = j; } }); return bi; }
      var cross = [], lb = near(big, xr0), lm = near(mic, xr0);
      for (var x = xr0; x <= xr1; x += 0.005) {
        var nb = near(big, x), nm = near(mic, x);
        if (nb !== lb) cross.push([x, 1]); if (nm !== lm) cross.push([x, 0]);
        lb = nb; lm = nm;
      }
      var gR = A.g({});
      A.line(P([xr0, yr])[0], P([0, yr])[1], P([xr1, yr])[0], P([0, yr])[1], 's-ink w1 dash', gR);
      var marks = cross.map(function (c) { var q = P([c[0], yr]); return A.circle(q[0], q[1], c[1] ? 4.5 : 3, c[1] ? 'f-acc s-card w1' : 'f-bad', gR); });
      var mob = A.g({}, gR); phone(A, 0, 0, 'f-ink', mob);
      var px = 252, T = 0;
      var pan = [0, 1, 2, 3, 4].map(function () { return A.g({}); });
      function tx(k, y, s, cls) { return A.text(px, y, s, { cls: cls || 't-s' }, pan[k]); }
      tx(0, 40, '分裂前', 't-b'); tx(0, 62, '半径 R'); tx(0, 80, '每个基站 60 条信道'); tx(0, 98, '发射功率 P_{t1}');
      tx(1, 40, '4:1 分裂', 't-b'); tx(1, 62, '新基站在两个旧基站'); tx(1, 80, '连线的中点'); tx(1, 98, '半径 R/2，面积 1/4');
      tx(2, 40, '降功率保持 SIR', 't-b'); tx(2, 62, 'P_{t2} = P_{t1} × (1/2)^{4}'); tx(2, 80, '= P_{t1} / 16');
      tx(2, 98, '→ −' + dB(16).toFixed(2) + ' dB', 't-s t-b f-bad');
      var pb1 = A.rect(px + 20, 216 - 96, 30, 96, 'f-acc s-none', pan[2], 2), pb2 = A.rect(px + 80, 216 - 6, 30, 6, 'f-gold s-none', pan[2], 1);
      A.text(px + 35, 232, 'P_{t1}', { cls: 't-s', anchor: 'middle' }, pan[2]); A.text(px + 95, 232, 'P_{t2}', { cls: 't-s', anchor: 'middle' }, pan[2]);
      tx(3, 40, '容量 ×4', 't-b'); tx(3, 62, '1 个大蜂窝面积'); tx(3, 80, '= 4 个微蜂窝'); tx(3, 98, '信道 60 → 4 × 60 = 240');
      tx(3, 116, 'A：49.6 → ' + (4 * 49.6).toFixed(1) + ' E'); tx(3, 134, 'η = 49.6/60 = ' + (49.6 / 60).toFixed(2) + ' 不变', 't-s f-good');
      tx(4, 40, '切换变多', 't-b');
      var cB = tx(4, 62, ''), cM = tx(4, 80, '');
      tx(4, 104, '课件经验值：半径 ÷4', 't-s'); tx(4, 122, '→ 每用户切换 ≈ ×10', 't-s t-b f-bad');
      return {
        frame: function (ts, dt, k) {
          T += dt || 0;
          var p = A.prog(ts, 1.0);
          gM.setAttribute('opacity', k === 0 ? 0 : k === 1 ? p.toFixed(2) : 1);
          show(hl, k === 3);
          for (var j = 0; j < 5; j++) pan[j].setAttribute('opacity', j === k ? 1 : 0);
          if (k === 2) { A.set(pb1, { height: 96, y: 120 }); var h2 = A.lerp(96, 6, p); A.set(pb2, { height: h2, y: 216 - h2 }); }
          show(gR, k === 4);
          if (k === 4) {
            var f = A.clamp(((ts || 0) % 6) / 5, 0, 1), x = A.lerp(xr0, xr1, f), q = P([x, yr]), nB = 0, nM = 0;
            mob.setAttribute('transform', 'translate(' + q[0].toFixed(1) + ',' + (q[1] - 9).toFixed(1) + ')');
            cross.forEach(function (c, i) { var on = c[0] <= x; marks[i].style.display = on ? '' : 'none'; if (on) { if (c[1]) nB++; else nM++; } });
            A.setText(cB, '穿过大蜂窝边界：' + nB + ' 次');
            A.setText(cM, '穿过微蜂窝边界：' + nM + ' 次');
          }
        }
      };
    }
  });

  /* ================= 9.2 sectoring ================= */
  (function () {
    var Q = Math.sqrt(21), q4 = Math.pow(Q, 4), qm = Math.pow(Q - 1, 4), qp = Math.pow(Q + 1, 4), q7 = Math.pow(Q + 0.7, 4);
    var modes = [
      { nm: '全向', nI: 6, si: 1 / (2 / qm + 2 / q4 + 2 / qp), pool: '57 条 × 1 个池', Ae: 44.2,
        f: '最坏(p.91 Case 1) S/I = 1/[2(Q−1)⁻⁴ + 2Q⁻⁴ + 2(Q+1)⁻⁴]', extra: '（简化算法 Q⁴/6 = ' + (q4 / 6).toFixed(1) + ' → ' + dB(q4 / 6).toFixed(2) + ' dB）' },
      { nm: '120°', nI: 2, si: 1 / (1 / q4 + 1 / q7), pool: '19 条 × 3 个池', Ae: 33.6, f: 'S/I = 1/[Q⁻⁴ + (Q+0.7)⁻⁴]', extra: '' },
      { nm: '60°', nI: 1, si: q7, pool: '9.5 条 × 6 个池', Ae: 24.7, f: 'S/I = (Q+0.7)⁴', extra: '' }
    ];
    modes.forEach(function (m) { m.db = dB(m.si); m.calls = Math.round(m.Ae * 30); });
    ANIM.reg('A:9.2', {
      title: '扇区化：干扰变少，信道池变小',
      cap: 'N = 7 按真实几何画出。浅红 = 各同频小区的 1 号扇区，朝向全都一样（小箭头）；深红是天线照得到手机的，实线 = 真正的干扰，虚线 = 被挡掉的。手机站在 1 号扇区的角上（最坏位置）。右边：SIR 用课件 p.91/p.145 公式，呼叫数用课件 p.148–149 的查表结果（GoS 1%，每次 2 分钟）。',
      h: 262,
      init: function (A) {
        var s = 21, cx = 124, cy = 136, mode = 1, cc = cochan(2, 1), mob = [1, 0];
        function P(x, y) { return [cx + x * s, cy - y * s]; }
        A.text(6, 16, 'N = 7，n = 4，手机在扇区角上', { cls: 't-s' });
        latt(4.6).forEach(function (p) { var q = P(p[0], p[1]); A.path(hexD(q[0], q[1], s), 'f-none s-line w1'); });
        var dyn = A.g({});
        var V = []; for (var i = 0; i < 6; i++) V.push([Math.cos(i * Math.PI / 3), Math.sin(i * Math.PI / 3)]);
        var sec = [[[0, 0], V[0], V[1], V[2]], [[0, 0], V[0], V[1]]];
        var px = 258, x0 = 290, rowsS = [56, 74, 92], rowsC = [146, 164, 182], sS = 70 / 30, sC = 70 / 1400;
        var tTitle = A.text(px, 22, '', { cls: 't-b' });
        A.text(px, 46, '最坏情况 SIR（dB）', { cls: 't-s' });
        A.text(px, 136, '每蜂窝呼叫/小时', { cls: 't-s' });
        var gx = x0 + 18 * sS;
        A.line(gx, 52, gx, 108, 's-gold w1 dash'); A.text(gx, 118, '18', { cls: 't-s f-gold', anchor: 'middle' });
        var bS = [], bC = [], nS = [], nC = [], vS = [], vC = [];
        modes.forEach(function (m, j) {
          nS.push(A.text(px, rowsS[j] + 10, m.nm, { cls: 't-s' }));
          bS.push(A.rect(x0, rowsS[j], m.db * sS, 13, 'f-line s-none', null, 1));
          vS.push(A.text(Math.max(x0 + m.db * sS, gx) + 3, rowsS[j] + 10, m.db.toFixed(1), { cls: 't-s' }));
          nC.push(A.text(px, rowsC[j] + 10, m.nm, { cls: 't-s' }));
          bC.push(A.rect(x0, rowsC[j], m.calls * sC, 13, 'f-line s-none', null, 1));
          vC.push(A.text(x0 + m.calls * sC + 3, rowsC[j] + 10, String(m.calls), { cls: 't-s' }));
        });
        var tP = A.text(px, 214, '', { cls: 't-s' }), tA = A.text(px, 232, '', { cls: 't-s' }), tCh = A.text(px, 250, '', { cls: 't-s t-b' });
        function draw() {
          clear(dyn);
          var m = modes[mode], w = mode === 1 ? 120 : 60, o = P(0, 0), mp = P(mob[0], mob[1]), bo = (mode === 1 ? 60 : 30) * Math.PI / 180;
          A.path(hexD(o[0], o[1], s), 'f-accs s-acc w2', dyn);
          if (mode) {
            A.poly(sec[mode - 1].map(function (v) { return P(v[0], v[1]); }), 'f-acc op3 s-acc w1', dyn);
            V.forEach(function (v, j) { if (mode === 2 || j % 2 === 0) { var q = P(v[0], v[1]); A.line(o[0], o[1], q[0], q[1], 's-acc w1', dyn); } });
          }
          cc.forEach(function (p) {
            var dx = mob[0] - p[0], dy = mob[1] - p[1], d = Math.sqrt(dx * dx + dy * dy), a = (Math.atan2(dy, dx) * 180 / Math.PI + 360) % 360;
            var hit = mode === 0 || (a > 1e-6 && a < w - 1e-6), c = P(p[0], p[1]);
            A.path(hexD(c[0], c[1], s), (mode === 0 ? 'f-bads' : 'f-none') + ' s-bad w1', dyn);
            if (mode) A.poly(sec[mode - 1].map(function (v) { return P(p[0] + v[0], p[1] + v[1]); }), (hit ? 'f-bad op7' : 'f-bad op3') + ' s-none', dyn);
            A.line(c[0], c[1], mp[0], mp[1], hit ? 's-bad w2' : 's-faint w1 dash', dyn);
            if (mode && hit) {
              var t = 0.5, lx = A.lerp(c[0], mp[0], t), ly = A.lerp(c[1], mp[1], t), L = Math.sqrt((mp[0] - c[0]) * (mp[0] - c[0]) + (mp[1] - c[1]) * (mp[1] - c[1]));
              A.text(lx + 14 * (mp[1] - c[1]) / L, ly - 14 * (mp[0] - c[0]) / L + 4, d.toFixed(2) + 'R', { cls: 't-s t-b f-bad', anchor: 'middle' }, dyn);
            }
            A.circle(c[0], c[1], 2.6, 'f-bad', dyn);
            if (mode) A.arrow(c[0], c[1], c[0] + 0.8 * s * Math.cos(bo), c[1] - 0.8 * s * Math.sin(bo), 's-ink w1', dyn, 4);
          });
          A.circle(o[0], o[1], 2.6, 'f-acc', dyn);
          if (mode) A.arrow(o[0], o[1], o[0] + 0.8 * s * Math.cos(bo), o[1] - 0.8 * s * Math.sin(bo), 's-ink w1', dyn, 4);
          phone(A, mp[0] + 2, mp[1], 'f-ink', dyn);
          A.setText(tTitle, m.nm + (mode ? ' 扇区' : '天线') + '：' + m.nI + ' 个干扰');
          modes.forEach(function (q, j) {
            var on = j === mode;
            A.set(bS[j], { cls: (on ? (q.db >= 18 ? 'f-good' : 'f-bad') : 'f-line') + ' s-none' });
            A.set(bC[j], { cls: (on ? 'f-acc' : 'f-line') + ' s-none' });
            [nS[j], vS[j], nC[j], vC[j]].forEach(function (e) { A.set(e, { cls: 't-s' + (on ? ' t-b' : '') }); });
          });
          A.setText(tP, '每个池：' + m.pool);
          A.setText(tA, 'A = ' + m.Ae + ' E，η = ' + (m.Ae / 57).toFixed(2));
          var ch = Math.round(100 * (m.calls / modes[0].calls - 1));
          A.set(tCh, { text: mode ? '呼叫数 ' + mn(ch) + '%' : '基准（不分扇区）', cls: 't-s t-b' + (mode ? ' f-bad' : '') });
          A.note(m.f + ' = ' + m.si.toFixed(1) + ' → <b>' + m.db.toFixed(2) + ' dB</b>' + (mode ? '（比全向最坏 +' + (m.db - modes[0].db).toFixed(1) + ' dB）' : m.extra) +
            '<br>Q = √21 = ' + Q.toFixed(3) + '，每蜂窝 57 条：' + m.pool + ' → A = ' + m.Ae + ' E × 30 = ' + m.calls + ' 次/小时');
        }
        A.choice({ label: '天线', options: ['全向', '120° × 3', '60° × 6'], value: mode, on: function (i) { mode = i; draw(); } });
        draw();
        return {};
      }
    });
  })();

  /* ================= 9.3 comparison table ================= */
  (function () {
    var Q = Math.sqrt(21), worst = dB(1 / (2 / Math.pow(Q - 1, 4) + 2 / Math.pow(Q, 4) + 2 / Math.pow(Q + 1, 4)));
    var g120 = dB(1 / (1 / Math.pow(Q, 4) + 1 / Math.pow(Q + 0.7, 4))) - worst, g60 = dB(Math.pow(Q + 0.7, 4)) - worst;
    var e120 = Math.round(100 * (1 - 33.6 / 44.2)), e60 = Math.round(100 * (1 - 24.7 / 44.2));
    ANIM.reg('A:9.3', {
      title: '小区分裂 vs 扇区化：一张表比清楚',
      cap: '左列小区分裂（加基站），右列扇区化（换天线）。绿色 = 变好，红色 = 变差。数字来自 9.1、9.2 的例题。',
      h: 262,
      steps: [
        '两种扩容办法：小区分裂是加基站把蜂窝做小；扇区化是基站不动，换定向天线。',
        'SIR：分裂后各站按 (1/2)⁴ 降功率，SIR 不变；扇区化干扰源变少，SIR 升高。',
        '中继效率：分裂后每站还是 60 条，效率不变；扇区化把信道池切小，效率下降。',
        '容量：分裂 4:1 直接 ×4；扇区化要拿 SIR 余量把 N 从 12 降到 7，才得 ×' + (12 / 7).toFixed(2) + '。',
        '代价：分裂要建站、切换变多（半径 ÷4 约 ×10）；扇区化扇区间切换多、设备多。'
      ],
      init: function (A) {
        var c1 = 155, c2 = 315, i;
        A.path(hexD(c1, 34, 26), 'f-none s-soft w1 dash');
        A.path(hexD(c1, 34, 13), 'f-golds s-gold w1');
        for (i = 0; i < 6; i++) { var a = (30 + 60 * i) * Math.PI / 180; A.path(hexD(c1 + 13 * S3 * Math.cos(a), 34 - 13 * S3 * Math.sin(a), 13), 'f-golds s-gold w1 op5'); }
        A.path(hexD(c2, 34, 26), 'f-accs s-acc w1');
        [0, 2, 4].forEach(function (j) { var a = j * Math.PI / 3; A.line(c2, 34, c2 + 26 * Math.cos(a), 34 - 26 * Math.sin(a), 's-acc w1'); });
        [1, 3, 5].forEach(function (j) { var a = j * Math.PI / 3; A.arrow(c2, 34, c2 + 18 * Math.cos(a), 34 - 18 * Math.sin(a), 's-ink w1', null, 4); });
        A.text(c1, 76, '小区分裂', { cls: 't-b', anchor: 'middle' }); A.text(c2, 76, '扇区化', { cls: 't-b', anchor: 'middle' });
        A.line(235, 4, 235, 258, 's-line w1');
        var R = [
          ['怎么做', ['加基站，蜂窝变小', '4:1 → 半径 R/2'], ['基站不变', '换 3 或 6 副定向天线'], '', ''],
          ['SIR', ['不变', '（新基站降功率 12 dB）'], ['升高：干扰 6 → 2 → 1', '120° +' + g120.toFixed(1) + ' dB，60° +' + g60.toFixed(1) + ' dB'], '', 'f-good'],
          ['中继效率', ['不变', '（每站信道数不变）'], ['下降：信道池被切小', '120° −' + e120 + '%，60° −' + e60 + '%'], 'f-good', 'f-bad'],
          ['容量', ['单位面积基站 ×4', '4:1 分裂 → ×4'], ['SIR 余量换更小的 N', 'N 12 → 7：×' + (12 / 7).toFixed(2)], 'f-good', 'f-good'],
          ['代价', ['建站成本高', '半径 ÷4 → 切换 ≈ ×10'], ['扇区间切换增多', '天线和射频设备更多'], 'f-bad', 'f-bad']
        ];
        var hl = A.rect(4, 0, 392, 34, 'f-golds s-none', null, 6), rows = [];
        R.forEach(function (r, j) {
          var y = 84 + j * 35, g = A.g({});
          A.line(4, y, 396, y, 's-line w1', g);
          A.text(8, y + 21, r[0], { cls: 't-s t-b' }, g);
          A.text(c1, y + 14, r[1][0], { cls: 't-s t-b ' + r[3], anchor: 'middle' }, g); A.text(c1, y + 28, r[1][1], { cls: 't-s', anchor: 'middle' }, g);
          A.text(c2, y + 14, r[2][0], { cls: 't-s t-b ' + r[4], anchor: 'middle' }, g); A.text(c2, y + 28, r[2][1], { cls: 't-s', anchor: 'middle' }, g);
          rows.push(g);
        });
        return {
          frame: function (ts, dt, k) {
            rows.forEach(function (g, j) { g.setAttribute('opacity', j < k ? 1 : j === k ? A.prog(ts, 0.6).toFixed(2) : 0); });
            A.set(hl, { y: 84 + k * 35 + 1 });
          }
        };
      }
    });
  })();

  /* ================= 10.1 what is a handoff ================= */
  ANIM.reg('A:10.1', {
    title: '切换：通话换到另一个信道上',
    cap: '<b>小区间</b>：手机从 A 走到 B，通话由 A 交给 B（同一个 MSC 管），通话不断。<b>小区内</b>：同一个基站里，当前信道干扰大，换一条信道。要求：transparent、uninterrupted、infrequent、successful。',
    h: 214,
    init: function (A) {
      var mode = 0, R = 58, yc = 128, xa = 200 - R * S3 / 2, xb = 200 + R * S3 / 2, ym = 152;
      A.rect(232, 10, 60, 24, 'f-card s-soft w1', null, 5); A.text(262, 26, 'MSC', { cls: 't-s t-b', anchor: 'middle' });
      A.path(hexD(xa, yc, R, Math.PI / 6), 'f-accs s-acc w1'); A.path(hexD(xb, yc, R, Math.PI / 6), 'f-goods s-good w1');
      A.line(xa, yc - 6, 262, 34, 's-soft w1 dash'); A.line(xb, yc - 6, 262, 34, 's-soft w1 dash');
      bs(A, xa, yc, 'f-acc'); bs(A, xb, yc, 'f-good');
      A.text(xa - 14, yc + 4, 'A', { cls: 't-b f-acc', anchor: 'middle' }); A.text(xb + 14, yc + 4, 'B', { cls: 't-b f-good', anchor: 'middle' });
      var link = A.line(xa, yc, xa, ym, 's-acc w3');
      var mob = A.g({}); phone(A, 0, 0, 'f-ink', mob);
      var chT = A.text(0, 0, '', { cls: 't-s t-b t-m', anchor: 'middle' });
      var flash = A.text(200, 206, '', { cls: 't-s t-b f-gold', anchor: 'middle' });
      var stat = A.text(6, 16, '', { cls: 't-s' });
      var gIn = A.g({}), chs = [], chx = [64, 88, 112];
      for (var i = 0; i < 3; i++) { chs.push(A.rect(chx[i] - 10, 50, 20, 16, 'f-card s-line w1', gIn, 3)); A.text(chx[i], 62, 'f' + (i + 1), { cls: 't-s t-m', anchor: 'middle' }, gIn); }
      A.text(6, 62, 'A 的信道', { cls: 't-s' }, gIn);
      var intf = A.g({}, gIn);
      A.path('M 92 196 L 106 186 L 102 194 L 122 180', 's-bad w2', intf);
      A.text(88, 202, '同频干扰', { cls: 't-s t-b f-bad', anchor: 'end' }, intf);
      A.choice({ label: '类型', options: ['小区间切换', '小区内切换'], value: 0, on: function (i) { mode = i; A.redraw(); } });
      return function frame(t) {
        var tt = t % 8, mx, ch, serv;
        show(gIn, mode === 1);
        if (mode === 0) {
          mx = A.lerp(110, 290, A.clamp(tt / 6, 0, 1)); serv = mx < 200 ? 0 : 1; ch = serv ? 'f₂' : 'f₁';
          A.set(link, { x1: serv ? xb : xa, y1: yc, x2: mx, y2: ym, cls: serv ? 's-good w3' : 's-acc w3' });
          A.setText(flash, Math.abs(mx - 200) < 16 ? '切换！A → B' : '');
          A.setText(stat, '小区间：服务基站 ' + (serv ? 'B' : 'A') + '，信道 ' + ch);
        } else {
          mx = xa - 10 + 6 * Math.sin(t * 1.3); var sw = tt >= 3.4; ch = sw ? 'f₂' : 'f₁';
          A.set(link, { x1: xa, y1: yc, x2: mx, y2: ym, cls: 's-acc w3' });
          intf.setAttribute('opacity', tt >= 1.5 && tt < 3.4 ? 1 : tt >= 3.4 ? 0.3 : 0);
          chs.forEach(function (r, i) { A.set(r, { cls: i === (sw ? 1 : 0) && !(i === 0 && tt >= 1.5) ? 'f-accs s-acc w3' : (i === 0 && tt >= 1.5 ? 'f-bads s-bad w1' : 'f-card s-line w1') }); });
          A.setText(flash, tt >= 3.4 && tt < 4.4 ? '小区内切换：f₁ → f₂' : '');
          A.setText(stat, '小区内：还是基站 A，信道 ' + ch + (tt >= 1.5 && !sw ? '（干扰大）' : ''));
        }
        mob.setAttribute('transform', 'translate(' + mx.toFixed(1) + ',' + ym + ')');
        A.set(chT, { x: mx, y: ym + 20, text: ch });
      };
    }
  });

  /* ================= 10.2 handoff margin ================= */
  ANIM.reg('A:10.2', {
    title: '切换裕量 Δ：信号多弱时开始切换',
    cap: '手机开车远离基站，接收功率（蓝）按 40·log₁₀d 下降（n = 4），在 2 km 处跌到 P<sub>min</sub>。跌到 P<sub>HO</sub> = P<sub>min</sub> + Δ 时开始切换，MSC 约需 10 s 完成。拖 Δ、换车速：Δ 太小来不及 → 掉话；Δ 太大 → 离边界还远就切换，白切。',
    h: 236,
    init: function (A) {
      var Dl = 2, v = 60, d0 = 800, dmin = 2000, Tho = 10, K = 8;
      var ax = A.axes({ x: 44, y: 36, w: 330, h: 150, xr: [800, 2200], yr: [-4, 17], xl: 'd (m)', yl: 'P − P_{min} (dB)', ticksX: [1000, 1500, 2000], ticksY: [0, 5, 10, 15], xAxisAt: 'bottom', yAxisAt: 'left' });
      function Pd(d) { return 40 * Math.log10(dmin / d); }
      var band = A.rect(ax.X(800), ax.Y(2), 330, 10, 'f-golds s-none', null, 0);
      A.line(ax.X(800), ax.Y(0), ax.X(2200), ax.Y(0), 's-bad w1 dash');
      A.text(ax.X(2200), ax.Y(0) - 8, 'P_{min}', { cls: 't-s t-b f-bad', anchor: 'end' });
      var lHO = A.line(0, 0, 0, 0, 's-gold w2 dash'), tHO = A.text(ax.X(800) + 4, 0, 'P_{HO} = P_{min} + Δ', { cls: 't-s t-b f-gold' });
      A.curve(ax, Pd, 's-acc w2');
      var vline = A.line(0, 0, 0, 0, 's-gold w1 dash'), tdho = A.text(0, 0, 'd_{HO}', { cls: 't-s f-gold', anchor: 'middle' });
      var dot = A.circle(0, 0, 4.5, 'f-ink s-card w1');
      var stat = A.text(6, 16, '', { cls: 't-s t-b' });
      var ok, dho, vms, tHOs, tMin, tDone, tEnd;
      function calc() {
        vms = v / 3.6; dho = dmin * Math.pow(10, -Dl / 40); tHOs = (dho - d0) / vms; tMin = (dmin - d0) / vms; tDone = tHOs + Tho; ok = tDone <= tMin; tEnd = ok ? tDone + 1 : tMin;
        A.set(band, { y: ax.Y(Dl), height: ax.Y(0) - ax.Y(Dl) });
        A.set(lHO, { x1: ax.X(800), x2: ax.X(2200), y1: ax.Y(Dl), y2: ax.Y(Dl) }); A.set(tHO, { y: ax.Y(Dl) - 8 });
        A.set(vline, { x1: ax.X(dho), x2: ax.X(dho), y1: ax.Y(Dl), y2: ax.Y(-4) }); A.set(tdho, { x: ax.X(dho) - 4, y: ax.Y(-4) - 10, anchor: 'end' });
        var mg = dmin - dho, tm = mg / vms;
        A.note('Δ = ' + Dl + ' dB：d<sub>HO</sub> = 2000 × 10^(−Δ/40) = ' + Math.round(dho) + ' m，余量 ' + Math.round(mg) + ' m<br>' + v + ' km/h（' + vms.toFixed(1) + ' m/s）：' + Math.round(mg) + ' / ' + vms.toFixed(1) + ' = ' + tm.toFixed(1) + ' s ' +
          (tm >= Tho ? '≥ 10 s ✓ 来得及' : '&lt; 10 s ✗ 来不及 → 掉话') + (Dl >= 10 ? '<br>Δ 太大：离基站才 ' + Math.round(dho) + ' m 就切换，原基站其实还能用 → 不必要的切换' : ''));
      }
      A.slider({ label: '裕量 Δ', min: 0.5, max: 12, step: 0.5, value: Dl, unit: 'dB', on: function (x) { Dl = x; calc(); A.redraw(); } });
      A.choice({ label: '车速', options: ['60 km/h', '120 km/h'], value: 0, on: function (i) { v = i ? 120 : 60; calc(); A.redraw(); } });
      calc();
      return function frame(t) {
        var cyc = tEnd / K + 2, tr = Math.min((t % cyc) * K, tEnd), d = Math.min(2200, d0 + vms * tr);
        A.set(dot, { cx: ax.X(d), cy: ax.Y(Pd(d)) });
        var s, c = 't-s t-b';
        if (tr < tHOs) s = '行驶中：信号还高于 P_{HO}';
        else if (ok && tr >= tDone) { s = '✓ 切换完成（10 s 内到了新基站）'; c += ' f-good'; }
        else if (!ok && tr >= tMin) { s = '✗ 掉话：跌到 P_{min} 时切换还没完成'; c += ' f-bad'; }
        else { s = '切换中… ' + (tr - tHOs).toFixed(1) + ' / 10 s'; c += ' f-gold'; }
        A.set(stat, { text: s, cls: c });
      };
    }
  });

  /* ================= 10.3 hard vs soft handoff ================= */
  ANIM.reg('A:10.3', {
    title: '硬切换（先断后连）vs 软切换（先连后断）',
    cap: '下面两条时间线是“手机和 A、B 的链路是否接通”。硬切换中间有一小段两条都断；软切换在边界附近同时连着 A 和 B（分集，更可靠），代价是这段时间占两份资源。',
    h: 230,
    init: function (A) {
      var mode = 0, xA = 34, xB = 366, yB = 66, ym = 112, xs = 70, xe = 330;
      bs(A, xA, yB, 'f-acc'); bs(A, xB, yB, 'f-good');
      A.text(xA, yB - 14, 'BS A', { cls: 't-s t-b f-acc', anchor: 'middle' }); A.text(xB, yB - 14, 'BS B', { cls: 't-s t-b f-good', anchor: 'middle' });
      A.line(200, 40, 200, 128, 's-line w1 dash'); A.text(200, 34, '小区边界', { cls: 't-s', anchor: 'middle' });
      var la = A.line(xA, yB, xA, yB, 's-acc w3'), lb = A.line(xB, yB, xB, yB, 's-good w3');
      var mob = A.g({}); var mp = phone(A, 0, 0, 'f-ink', mob);
      var mT = A.text(0, 0, '', { cls: 't-s t-b', anchor: 'middle' });
      var top = A.text(6, 16, '', { cls: 't-s t-b' });
      A.text(8, 166, '链路 A', { cls: 't-s' }); A.text(8, 190, '链路 B', { cls: 't-s' });
      A.rect(xs, 156, xe - xs, 14, 'f-paper s-line w1', null, 2); A.rect(xs, 180, xe - xs, 14, 'f-paper s-line w1', null, 2);
      var ra = A.rect(xs, 156, 0, 14, 'f-acc s-none', null, 2), rb = A.rect(xs, 180, 0, 14, 'f-good s-none', null, 2);
      var cur = A.line(0, 150, 0, 200, 's-ink w1');
      var res = A.text(6, 218, '', { cls: 't-s' });
      var P = [{ a: 196, b: 216 }, { a: 250, b: 150 }];
      function setMode(i) { mode = i; A.set(top, { text: i ? '软切换 make before break：CDMA（IS-95、WCDMA）' : '硬切换 break before make：FDMA/TDMA（GSM）', cls: 't-s t-b ' + (i ? 'f-good' : 'f-acc') }); }
      A.choice({ label: '方式', options: ['硬切换', '软切换'], value: 0, on: function (i) { setMode(i); A.redraw(); } });
      setMode(0);
      return function frame(t) {
        var tt = t % 9, x = A.lerp(xs, xe, A.clamp(tt / 7, 0, 1)), p = P[mode], onA = x < p.a, onB = x >= p.b;
        mob.setAttribute('transform', 'translate(' + x.toFixed(1) + ',' + ym + ')');
        A.set(la, { x2: onA ? x : xA, y2: onA ? ym : yB }); A.set(lb, { x2: onB ? x : xB, y2: onB ? ym : yB });
        A.set(mp, { cls: !onA && !onB ? 'f-bad' : 'f-ink' });
        var n = (onA ? 1 : 0) + (onB ? 1 : 0);
        A.set(mT, { x: x, y: ym + 22, text: n === 0 ? '中断！' : n === 2 ? '分集：同时连 A、B' : '', cls: 't-s t-b ' + (n === 0 ? 'f-bad' : 'f-good') });
        A.set(ra, { x: xs, width: Math.max(0, Math.min(x, p.a) - xs) });
        A.set(rb, { x: p.b, width: Math.max(0, x - p.b) });
        A.set(cur, { x1: x, x2: x });
        A.set(res, { text: '此刻占用链路：' + n + ' 条' + (n === 0 ? '（通话中断，可能掉话）' : n === 2 ? '（两份资源）' : ''), cls: 't-s' + (n === 0 ? ' f-bad t-b' : '') });
      };
    }
  });

  /* ================= 10.4 guard channels ================= */
  ANIM.reg('A:10.4', {
    title: '信道预留：给切换留 r 条“专座”',
    cap: '一个蜂窝 M = 10 条信道，新呼叫 5 E、切换进来 1 E。空闲信道 ≤ r 时只接切换。柱子按生灭过程算出：pₖ = pₖ₋₁ ×（到达话务量）/ k，再归一化；r = 0 就是普通 Erlang B。',
    h: 222,
    init: function (A) {
      var M = 10, An = 5, Ah = 1, r = 1, i;
      function calc(r) {
        var p = [1], s = 1, nb = 0, k;
        for (k = 1; k <= M; k++) { p.push(p[k - 1] * (k - 1 < M - r ? An + Ah : Ah) / k); s += p[k]; }
        for (k = M - r; k <= M; k++) nb += p[k];
        return [100 * nb / s, 100 * p[M] / s];
      }
      var res = [0, 1, 2, 3].map(calc);
      A.text(10, 16, 'M = 10 条信道', { cls: 't-s' });
      var slots = [];
      for (i = 0; i < M; i++) { slots.push(A.rect(20 + i * 36, 24, 32, 24, 'f-accs s-acc w1', null, 4)); A.text(36 + i * 36, 40, String(i + 1), { cls: 't-s', anchor: 'middle' }); }
      A.rect(20, 58, 9, 9, 'f-accs s-acc w1', null, 1); A.text(33, 66, '新呼叫、切换都能用', { cls: 't-s' });
      A.rect(160, 58, 9, 9, 'f-golds s-gold w1', null, 1); var tg = A.text(173, 66, '', { cls: 't-s' });
      A.text(10, 88, '新呼叫 5 E + 切换 1 E', { cls: 't-s' });
      A.rect(250, 80, 9, 9, 'f-gold s-none', null, 1); A.text(262, 88, '新呼叫阻塞', { cls: 't-s' });
      A.rect(322, 80, 9, 9, 'f-bad s-none', null, 1); A.text(334, 88, '切换掉话', { cls: 't-s' });
      var ax = A.axes({ x: 40, y: 104, w: 340, h: 90, xr: [-0.5, 3.5], yr: [0, 24], yl: '%', ticksY: [0, 10, 20],
        ticksX: [0, 1, 2, 3].map(function (v) { return { v: v, l: 'r = ' + v }; }), xAxisAt: 'bottom', yAxisAt: 'left' });
      var grp = res.map(function (v, j) {
        var g = A.g({}), x = ax.X(j);
        A.rect(x - 24, ax.Y(v[0]), 18, ax.Y(0) - ax.Y(v[0]), 'f-gold s-none', g, 1);
        A.rect(x + 6, ax.Y(v[1]), 18, Math.max(0.5, ax.Y(0) - ax.Y(v[1])), 'f-bad s-none', g, 1);
        A.text(x - 15, ax.Y(v[0]) - 4, v[0].toFixed(2), { cls: 't-s', anchor: 'middle' }, g);
        A.text(x + 15, ax.Y(v[1]) - 4, v[1] < 0.1 ? v[1].toFixed(3) : v[1].toFixed(2), { cls: 't-s', anchor: 'middle' }, g);
        return g;
      });
      function draw() {
        for (var i = 0; i < M; i++) A.set(slots[i], { cls: i >= M - r ? 'f-golds s-gold w2' : 'f-accs s-acc w1' });
        A.setText(tg, r ? '只给切换（预留 r = ' + r + ' 条）' : '（r = 0：不预留）');
        grp.forEach(function (g, j) { g.setAttribute('opacity', j === r ? 1 : 0.35); });
        var v = res[r];
        A.note('r = ' + r + '：新呼叫阻塞 <b>' + v[0].toFixed(2) + '%</b>，切换掉话 <b>' + (v[1] < 0.1 ? v[1].toFixed(3) : v[1].toFixed(2)) + '%</b>' +
          (r ? '<br>和 r = 0（都是 ' + res[0][0].toFixed(2) + '%）比：切换掉话降到约 1/' + Math.round(res[0][1] / v[1]) + '，新呼叫阻塞升高' : '<br>r = 0 就是 Erlang B：B(10, 6 E) = ' + (100 * erlB(10, 6)).toFixed(2) + '%'));
      }
      A.choice({ label: '预留信道', options: ['r = 0', 'r = 1', 'r = 2', 'r = 3'], value: r, on: function (i) { r = i; draw(); } });
      draw();
      return {};
    }
  });

  /* ================= 10.5 power control / near–far ================= */
  (function () {
    var Gp = 1.2288e6 / 9.6e3, GpdB = dB(Gp), ratio = 40 * Math.log10(1000 / 100), after = -ratio + GpdB, need = 7, Kmax = Math.floor(1 + Gp / Math.pow(10, need / 10));
    ANIM.reg('A:10.5', {
      title: '功率控制：近的调小、远的调大',
      cap: 'CDMA 里所有用户同一频段，基站同时收。下面的柱子是两部手机信号到达基站时的功率（dB，以近手机不控制时为 0 dB）。参数取 IS-95：1.2288 Mchip/s，话音 9.6 kbit/s，要求解扩后 SIR ≥ 7 dB。',
      h: 236, live: true, stepDur: 4,
      steps: [
        '两部手机发射功率一样：近的离基站 100 m，远的 1 km（n = 4）。',
        '到基站时功率差 (1000/100)⁴ = 10⁴ 倍 = ' + ratio.toFixed(0) + ' dB：近的把远的淹没，这叫远近效应。',
        '远用户解扩前 SIR = −40 dB，解扩（+' + GpdB.toFixed(1) + ' dB）后 ' + mn(after.toFixed(1)) + ' dB，比 7 dB 差约 ' + Math.round(need - after) + ' dB。',
        '功率控制：近手机降 40 dB，两路到达基站一样强 → 解扩后 ' + GpdB.toFixed(1) + ' dB ≥ 7 dB ✓',
        '闭环做法：基站估计 SIR，高了命令降功率、低了命令升（CDMA 每 1 ms 一次）。',
        '理想功率控制：' + Gp + '/(K − 1) ≥ ' + Math.pow(10, 0.7).toFixed(2) + ' → K ≤ ' + Kmax + '，一个小区约 ' + Kmax + ' 个用户。'
      ],
      init: function (A) {
        var bx = 30, by = 70, near = [100, 48], far = [340, 92];
        bs(A, bx, by, 'f-ink'); A.text(bx, by + 22, '基站', { cls: 't-s', anchor: 'middle' });
        A.line(bx, by, near[0], near[1], 's-line w1 dash'); A.line(bx, by, far[0], far[1], 's-line w1 dash');
        phone(A, near[0], near[1], 'f-ink'); phone(A, far[0], far[1], 'f-ink');
        A.text(near[0], near[1] + 20, '近：100 m', { cls: 't-s t-b f-acc', anchor: 'middle' });
        A.text(far[0], far[1] + 20, '远：1 km', { cls: 't-s t-b f-gold', anchor: 'middle' });
        var txN = A.rect(near[0] + 9, 0, 7, 0, 'f-acc s-none', null, 1), txF = A.rect(far[0] + 9, 0, 7, 0, 'f-gold s-none', null, 1);
        A.text(near[0] + 19, near[1] + 4, 'Tx', { cls: 't-s' }); A.text(far[0] + 19, far[1] + 4, 'Tx', { cls: 't-s' });
        var cmdN = A.text(near[0] + 22, near[1] - 14, '', { cls: 't-s t-b f-gold' }), cmdF = A.text(far[0] - 10, far[1] - 26, '', { cls: 't-s t-b f-gold', anchor: 'end' });
        var pN = [], pF = [], j;
        for (j = 0; j < 3; j++) { pN.push(A.circle(0, 0, 3, 'f-acc')); pF.push(A.circle(0, 0, 3, 'f-gold')); }
        var base = 214, sc = 1.3;
        A.line(30, base, 166, base, 's-soft w1');
        A.text(30, 130, '到达基站的功率', { cls: 't-s' });
        var rN = A.rect(50, base, 36, 0, 'f-acc s-none', null, 2), rF = A.rect(110, base, 36, 0, 'f-gold s-none', null, 2);
        var vN = A.text(68, 0, '', { cls: 't-s t-b', anchor: 'middle' }), vF = A.text(128, 0, '', { cls: 't-s t-b', anchor: 'middle' });
        A.text(68, base + 14, '近', { cls: 't-s', anchor: 'middle' }); A.text(128, base + 14, '远', { cls: 't-s', anchor: 'middle' });
        var lines = []; for (j = 0; j < 5; j++) lines.push(A.text(182, 140 + j * 18, '', { cls: 't-s' }));
        var TX = [
          ['同样的发射功率', '近手机 100 m，远手机 1 km', '路径损耗指数 n = 4'],
          ['到达功率比 (1000/100)^{4} = 10^{4}', '= 40 dB：近的强得多', '→ 远近效应 near–far'],
          ['远用户解扩前 SIR = −40 dB', 'G_{p} = 1.2288M / 9.6k = ' + Gp, '= ' + GpdB.toFixed(1) + ' dB → 解扩后 ' + mn(after.toFixed(1)) + ' dB', '要求 ≥ 7 dB ✗'],
          ['近手机发射功率降 40 dB', '两路到达基站一样强', '解扩前 0 dB → 解扩后 ' + GpdB.toFixed(1) + ' dB', '≥ 7 dB ✓'],
          ['基站持续估计 SIR', 'SIR 偏高 → 命令降功率', 'SIR 偏低 → 命令升功率', 'CDMA 每 1 ms 调一次'],
          ['理想功率控制：K 个用户等功率', '解扩后 SIR = ' + Gp + '/(K − 1)', '≥ 5.01 → K − 1 ≤ ' + (Gp / Math.pow(10, 0.7)).toFixed(1), '→ K ≤ ' + Kmax]
        ];
        var T = 0;
        return {
          frame: function (ts, dt, k) {
            T += dt || 0;
            var pc = k >= 3, p = k === 3 ? A.prog(ts, 1.2) : pc ? 1 : 0;
            var txNdB = -40 * p, rxN = txNdB, rxF = -ratio;
            var hN = (rxN + 50) * sc, hF = (rxF + 50) * sc;
            A.set(rN, { y: base - hN, height: hN }); A.set(rF, { y: base - hF, height: hF });
            A.set(vN, { y: base - hN - 4, text: mn(rxN.toFixed(0)) + ' dB' }); A.set(vF, { y: base - hF - 4, text: mn(rxF.toFixed(0)) + ' dB' });
            var tN = 30 + 0.6 * txNdB;
            A.set(txN, { y: near[1] + 6 - tN, height: tN }); A.set(txF, { y: far[1] + 6 - 30, height: 30 });
            var rn = 1.5 + 4.5 * (rxN + 40) / 40, rf = 1.5;
            for (var j = 0; j < 3; j++) {
              var f = (T * 0.5 + j / 3) % 1;
              A.set(pN[j], { cx: A.lerp(near[0], bx, f), cy: A.lerp(near[1], by, f), r: k === 0 ? 3 : rn });
              A.set(pF[j], { cx: A.lerp(far[0], bx, f), cy: A.lerp(far[1], by, f), r: k === 0 ? 3 : rf });
            }
            A.setText(cmdN, k === 4 ? '↓ 降' : ''); A.setText(cmdF, k === 4 ? '↑ 升（若偏低）' : '');
            for (j = 0; j < 5; j++) {
              var s = TX[k][j] || '';
              A.set(lines[j], { text: s, cls: 't-s' + (/✗/.test(s) ? ' t-b f-bad' : /✓|K ≤/.test(s) ? ' t-b f-good' : '') });
            }
          }
        };
      }
    });
  })();
})();
