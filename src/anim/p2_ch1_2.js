/* EE6129 p2-learn (Part 2, Ser Wee): animations for 0.1 and chapters 1–2. Numbers follow the section texts. */
(function () {
  'use strict';

  /* fade groups in/out between steps: add(el, k => target opacity) */
  function fader(A) {
    var items = [], k = 0;
    return {
      add: function (el, fn) { items.push({ el: el, fn: fn, cur: null, from: 0 }); return el; },
      step: function (kk) { k = kk; items.forEach(function (o) { o.from = o.cur == null ? o.fn(kk) : o.cur; }); },
      frame: function (ts) {
        var p = A.prog(ts, 0.7);
        items.forEach(function (o) {
          o.cur = A.lerp(o.from, o.fn(k), p);
          o.el.setAttribute('opacity', o.cur.toFixed(2));
          o.el.style.display = o.cur < 0.01 ? 'none' : '';
        });
      }
    };
  }
  function gpdf(x, m, s) { return Math.exp(-(x - m) * (x - m) / (2 * s * s)) / (s * Math.sqrt(2 * Math.PI)); }
  /* sum-of-sinusoids Rayleigh fading (Jakes-like); returns env(t, fm) with E[env²] = 1 */
  function sos(rand, N) {
    var th = [], ph = [];
    for (var i = 0; i < N; i++) { th.push(2 * Math.PI * (i + rand()) / N); ph.push(2 * Math.PI * rand()); }
    return function (t, fm) {
      var re = 0, im = 0;
      for (var i = 0; i < N; i++) { var p = ph[i] + 2 * Math.PI * fm * Math.cos(th[i]) * t; re += Math.cos(p); im += Math.sin(p); }
      return Math.sqrt((re * re + im * im) / N);
    };
  }
  /* probability text: 0.266, 0.00357, 1.23×10^{-5} */
  function fp(p) {
    if (p >= 0.01) return p.toFixed(3);
    if (p >= 1e-4) return p.toPrecision(3);
    var e = Math.floor(Math.log10(p)), m = p / Math.pow(10, e);
    return m.toFixed(2) + '×10^{' + e + '}';
  }

  /* ================= 0.1 overview ================= */
  ANIM.reg('p2:0.1', {
    title: '一条信号的旅程：信道伤它，接收机救它',
    cap: '看什么：上面是接收功率随距离的变化（示意），一层层叠上路径损耗、阴影、多径衰落（第 2 章）；下面五块是接收机的五种“救法”（第 3–7 章），按步骤逐个点亮。',
    h: 272,
    steps: [
      '第 2 章 · 路径损耗：平均功率随距离按 10γ·log₁₀d 下降，dB 图上是一条直线。',
      '第 2 章 · 阴影：障碍物让平均值慢慢上下浮动几 dB，dB 值服从高斯（σ，第 1 章）。',
      '第 2 章 · 多径衰落：回波相加又相消，走几步就掉进一个深坑（红点 = 深衰落）。',
      '第 3 章 · 检测：在噪声里判 0/1，Pb = Q(d/2σ)；衰落让 SNR 也变成随机的。',
      '第 4、5 章 · 分集 / MIMO：两路独立，同时深衰落很少；绿线取两路中较强的一路。',
      '第 6、7 章 · 均衡 / OFDM：回波拖进下个符号 = ISI；均衡器抵消它，OFDM 用长符号 + CP 躲开。'
    ],
    init: function (A) {
      var F = fader(A), i;
      A.rect(10, 8, 42, 26, 'f-card s-soft w1', null, 6); A.text(31, 26, 'Tx', { cls: 't-b', anchor: 'middle' });
      A.arrow(54, 21, 78, 21, 's-soft w1', null, 5);
      F.add(A.rect(80, 8, 248, 26, 'f-golds s-gold w2', null, 6), function (k) { return k <= 2 ? 1 : 0; });
      A.rect(80, 8, 248, 26, 'f-none s-soft w1', null, 6);
      A.text(204, 26, '信道：路径损耗 · 阴影 · 多径（第 2 章）', { cls: 't-s', anchor: 'middle' });
      A.arrow(330, 21, 352, 21, 's-soft w1', null, 5);
      F.add(A.rect(356, 8, 36, 26, 'f-accs s-acc w2', null, 6), function (k) { return k >= 3 ? 1 : 0; });
      A.rect(356, 8, 36, 26, 'f-none s-soft w1', null, 6); A.text(374, 26, 'Rx', { cls: 't-b', anchor: 'middle' });

      var ax = A.axes({ x: 40, y: 52, w: 340, h: 108, xr: [0, 1], yr: [-62, 8], xl: 'log 距离 →', yl: '接收功率 (dB)', xAxisAt: 'bottom' });
      var r1 = sos(A.rng(7), 14), r2 = sos(A.rng(29), 14);
      var a0 = 6.28 * A.rand(), b0 = 6.28 * A.rand();
      function pl(x) { return -4 - 34 * x; }
      function sh(x) { return 3.2 * Math.sin(2 * Math.PI * 1.4 * x + a0) + 2.4 * Math.sin(2 * Math.PI * 3.1 * x + b0); }
      function fd(r, x) { return Math.max(-26, 20 * Math.log10(r(x, 22) + 1e-9)); }
      var c0 = [], c1 = [], c2 = [], c3 = [], c4 = [], deep = [];
      for (i = 0; i <= 320; i++) {
        var x = i / 320, f1 = fd(r1, x), f2 = fd(r2, x), base = pl(x) + sh(x);
        c0.push([x, pl(x)]); c1.push([x, base]); c2.push([x, base + f1]); c3.push([x, base + f2]); c4.push([x, base + Math.max(f1, f2)]);
        if (i > 0 && f1 < -14 && f1 <= fd(r1, (i - 1) / 320) && f1 <= fd(r1, (i + 1) / 320)) deep.push([x, base + f1]);
      }
      F.add(A.curve(ax, c3, 's-gold w1'), function (k) { return k === 4 ? 0.6 : 0; });
      F.add(A.curve(ax, c2, 's-acc w1'), function (k) { return k < 2 ? 0 : k === 4 ? 0.3 : k === 2 ? 1 : 0.55; });
      F.add(A.curve(ax, c4, 's-good w2'), function (k) { return k === 4 ? 1 : 0; });
      F.add(A.curve(ax, c1, 's-gold w2'), function (k) { return k === 1 ? 1 : k > 1 ? 0.35 : 0; });
      F.add(A.curve(ax, c0, 's-acc w2'), function (k) { return k === 0 ? 1 : 0.35; });
      var gd = F.add(A.g(), function (k) { return k === 2 ? 1 : 0; });
      deep.forEach(function (p) { A.circle(ax.X(p[0]), ax.Y(p[1]), 3.2, 'f-bad', gd); });
      var lab = A.text(380, 64, '', { cls: 't-s t-b', anchor: 'end' });
      var labs = ['路径损耗：直线下降', '+ 阴影：慢、几 dB', '+ 多径：快、深坑', '衰落 → SNR 是随机的', '金 = 第 2 路，绿 = 取较强者', '每一处深坑都会出错'];

      // illustration area (y 172–228)
      F.add(A.text(200, 204, '信道造成的问题，接收机用下面五招对付（第 3–7 章）', { cls: 't-s', anchor: 'middle' }), function (k) { return k < 3 ? 1 : 0; });
      var gDet = F.add(A.g(), function (k) { return k === 3 ? 1 : 0; });
      var bl = [], br = [], tail = [[118, 222]];
      for (i = 0; i <= 60; i++) {
        var u = 30 + i * 2.6, y1 = 222 - 30 * Math.exp(-Math.pow(u - 88, 2) / 648), y2 = 222 - 30 * Math.exp(-Math.pow(u - 148, 2) / 648);
        bl.push([u, y1]); br.push([u, y2]); if (u >= 118) tail.push([u, y1]);
      }
      tail.push([186, 222]);
      A.poly(tail, 'f-bad s-none op3', gDet);
      A.poly(bl, 's-acc w2', gDet); A.poly(br, 's-gold w2', gDet);
      A.line(28, 222, 192, 222, 's-soft w1', gDet); A.line(118, 182, 118, 224, 's-ink w1 dash', gDet);
      A.text(212, 196, 'y = s + w：噪声让两个钟形重叠', { cls: 't-s' }, gDet);
      A.text(212, 214, '红色 = 判错的概率 P_{b} = Q(d/2σ)', { cls: 't-s' }, gDet);
      var gDiv = F.add(A.g(), function (k) { return k === 4 ? 1 : 0; });
      A.text(200, 194, '两路独立：同时深衰落的概率 = 各自概率相乘', { cls: 't-s', anchor: 'middle' }, gDiv);
      A.text(200, 212, 'MIMO（第 5 章）：多发多收，还能并行传多路数据', { cls: 't-s', anchor: 'middle' }, gDiv);
      var gIsi = F.add(A.g(), function (k) { return k === 5 ? 1 : 0; });
      A.rect(30, 186, 80, 22, 'f-accs s-acc w1', gIsi, 2); A.rect(110, 186, 80, 22, 'f-golds s-gold w1', gIsi, 2);
      A.rect(60, 212, 50, 10, 'f-none s-acc w1 dash', gIsi, 1); A.rect(110, 212, 30, 10, 'f-bads s-bad w1', gIsi, 1);
      A.text(70, 201, '符号 1', { cls: 't-s', anchor: 'middle' }, gIsi); A.text(150, 201, '符号 2', { cls: 't-s', anchor: 'middle' }, gIsi);
      A.text(206, 200, '符号 1 的回波拖进符号 2 = ISI', { cls: 't-s' }, gIsi);
      A.text(206, 218, '第 6 章均衡抵消 / 第 7 章 OFDM 加 CP', { cls: 't-s' }, gIsi);

      var chips = [['第 3 章', '检测', [3]], ['第 4 章', '分集', [4]], ['第 5 章', 'MIMO', [4]], ['第 6 章', '均衡', [5]], ['第 7 章', 'OFDM', [5]]];
      chips.forEach(function (c, j) {
        var x = 6 + j * 78;
        A.rect(x, 234, 74, 34, 'f-card s-line w1', null, 7);
        F.add(A.rect(x, 234, 74, 34, 'f-accs s-acc w2', null, 7), function (k) { return c[2].indexOf(k) >= 0 ? 1 : 0; });
        A.text(x + 37, 248, c[0], { cls: 't-s', anchor: 'middle' });
        A.text(x + 37, 263, c[1], { cls: 't-b', anchor: 'middle' });
      });
      return {
        step: function (k) { F.step(k); A.setText(lab, labs[k]); },
        frame: function (ts) { F.frame(ts); }
      };
    }
  });

  /* ================= 1.1 existing systems ================= */
  ANIM.reg('p2:1.1', {
    title: '各种系统的速率：横轴每格 ×10',
    cap: '看什么：横轴是对数刻度，每格速率乘 10。蜂窝每一代都跨了好几格；WiFi、蓝牙、ZigBee 按用途在速率和功耗之间取舍。数字取自第 1a 章 p.3–10（这一章不考）。',
    h: 248,
    steps: [
      '2G（数字蜂窝）：9.6–14.4 kbps，够打电话、发短信。',
      '3G：384 kbps–2 Mbps，手机开始能上网。',
      '4G：1 Gbps。每一代都要在“速率 × 移动性”上有突破（p.3–4）。',
      '5G：20 Gbps，约是 2G 的 200 万倍，横轴上跨了六格多。',
      'WiFi 用免授权 ISM 频段：11 → 54 → 600 Mbps；蓝牙、ZigBee 速率低，但短距离、省电。'
    ],
    init: function (A) {
      var F = fader(A);
      function X(b) { return 74 + (Math.log10(b) - 3) / 8 * 312; }
      var tl = ['1k', '10k', '100k', '1M', '10M', '100M', '1G', '10G', '100G'];
      for (var e = 3; e <= 11; e++) {
        A.line(X(Math.pow(10, e)), 18, X(Math.pow(10, e)), 214, 's-line w1 dash op5');
        A.text(X(Math.pow(10, e)), 228, tl[e - 3], { cls: 't-s', anchor: 'middle' });
      }
      A.line(70, 214, 390, 214, 's-soft w1');
      A.text(390, 244, '速率（bit/s，对数刻度）', { cls: 't-s', anchor: 'end' });
      var rows = [
        { n: '2G', y: 32, v: [9.6e3, 14.4e3], t: '9.6–14.4 kbps', s: 0 },
        { n: '3G', y: 56, v: [384e3, 2e6], t: '384 kbps–2 Mbps', s: 1 },
        { n: '4G', y: 80, v: [1e9], t: '1 Gbps', s: 2, left: 1 },
        { n: '5G', y: 104, v: [20e9], t: '20 Gbps', s: 3, left: 1 },
        { n: 'WiFi', y: 158, v: [11e6, 54e6, 600e6], t: 'b 11 / a,g 54 / n 600 Mbps', s: 4, left: 1, dots: 1 },
        { n: '蓝牙', y: 182, v: [1e6, 2e6], t: 'BR 1 / EDR 2 Mbps', s: 4 },
        { n: 'ZigBee', y: 206, v: [250e3], t: '250 kbps', s: 4 }
      ];
      rows.forEach(function (r) {
        var g = F.add(A.g(), function (k) { return k >= r.s ? 1 : 0; });
        var c = r.s < 4 ? 'acc' : 'gold', x0 = X(r.v[0]), x1 = X(r.v[r.v.length - 1]);
        A.text(8, r.y + 4, r.n, { cls: 't-b' }, g);
        if (r.dots) { A.line(x0, r.y, x1, r.y, 's-' + c + ' w1 op5', g); r.v.forEach(function (v) { A.circle(X(v), r.y, 4.5, 'f-' + c, g); }); }
        else if (r.v.length === 1) A.circle(x0, r.y, 5, 'f-' + c, g);
        else A.rect(x0 - 3, r.y - 5, x1 - x0 + 6, 10, 'f-' + c, g, 5);
        if (r.left) A.text(x0 - 10, r.y + 4, r.t, { cls: 't-s', anchor: 'end' }, g);
        else A.text(x1 + 10, r.y + 4, r.t, { cls: 't-s' }, g);
      });
      var ga = F.add(A.g(), function (k) { return k >= 3 ? 1 : 0; });
      A.arrow(X(9.6e3), 122, X(20e9), 122, 's-bad w2', ga, 6);
      A.text(200, 138, '5G ÷ 2G ≈ ' + Math.round(20e9 / 9.6e3 / 1e4) + ' 万倍', { cls: 't-s t-b f-bad', anchor: 'middle' }, ga);
      return { step: function (k) { F.step(k); }, frame: function (ts) { F.frame(ts); } };
    }
  });

  /* ================= 1.2 four rules / Bayes ================= */
  ANIM.reg('p2:1.2', {
    title: '四条概率规则：数一数就懂',
    cap: '看什么：骰子（A = 偶数，B = 质数）演示交集、并集；摸弹珠演示条件概率；最后两步是“信道好坏与误码”的全概率和贝叶斯，数字都和正文例题一样。',
    h: 232,
    steps: [
      '掷骰子：A = 偶数 {2,4,6}，B = 质数 {2,3,5}。等可能时 P = 个数 ÷ 6。',
      '交集 A∩B（同时发生）：既偶又质，只有 2，P(A∩B) = 1/6。',
      '并集 A∪B（至少一个）：数出 5 个。加法规则：3/6 + 3/6 − 1/6，减掉被数两遍的 2。',
      '条件概率：3 红 4 蓝，已知先摸出蓝（B），袋里剩 3 红 3 蓝 → P(红 | B) = 3/6 = 1/2。',
      '全概率：80% 时间信道好（误码 10⁻⁴），20% 深衰落（10⁻²），分情况加权再相加。',
      '贝叶斯反推原因：出了错，是深衰落造成的概率 = 0.002 ÷ 0.00208 ≈ 96%。'
    ],
    init: function (A) {
      var F = fader(A);
      /* --- dice --- */
      var gD = F.add(A.g(), function (k) { return k <= 2 ? 1 : 0; });
      A.rect(16, 30, 368, 168, 'f-none s-soft w1', gD, 8);
      A.text(24, 46, '样本空间 {1,…,6}', { cls: 't-s' }, gD);
      var defs = A.el('defs', {}, gD), cp = A.el('clipPath', { id: 'p2c12clipA' }, defs);
      A.el('ellipse', { cx: 165, cy: 120, rx: 95, ry: 62 }, cp);
      var uni = F.add(A.g({}, gD), function (k) { return k === 2 ? 1 : 0; });
      A.el('ellipse', { cx: 165, cy: 120, rx: 95, ry: 62, cls: 'f-accs' }, uni);
      A.el('ellipse', { cx: 245, cy: 120, rx: 95, ry: 62, cls: 'f-accs' }, uni);
      F.add(A.el('ellipse', { cx: 245, cy: 120, rx: 95, ry: 62, cls: 'f-golds', 'clip-path': 'url(#p2c12clipA)' }, gD), function (k) { return k === 1 ? 1 : 0; });
      A.el('ellipse', { cx: 165, cy: 120, rx: 95, ry: 62, cls: 'f-none s-acc w2' }, gD);
      A.el('ellipse', { cx: 245, cy: 120, rx: 95, ry: 62, cls: 'f-none s-gold w2' }, gD);
      A.text(80, 64, 'A：偶数', { cls: 't-b f-acc', anchor: 'middle' }, gD);
      A.text(330, 64, 'B：质数', { cls: 't-b f-gold', anchor: 'middle' }, gD);
      var pos = { 1: [356, 176], 2: [205, 120], 3: [290, 100], 4: [120, 100], 5: [290, 145], 6: [120, 145] };
      var Aset = [2, 4, 6], Bset = [2, 3, 5];
      for (var n = 1; n <= 6; n++) {
        A.circle(pos[n][0], pos[n][1], 13, 'f-card s-soft w1', gD);
        A.text(pos[n][0], pos[n][1] + 5, String(n), { cls: 't-l t-b', anchor: 'middle' }, gD);
      }
      var nAB = Aset.filter(function (v) { return Bset.indexOf(v) >= 0; }).length, nU = Aset.length + Bset.length - nAB;
      var dtxt = A.text(200, 220, '', { cls: 't-b', anchor: 'middle' }, gD);
      var dl = ['P(A) = ' + Aset.length + '/6，P(B) = ' + Bset.length + '/6',
        'P(A∩B) = ' + nAB + '/6',
        'P(A∪B) = ' + Aset.length + '/6 + ' + Bset.length + '/6 − ' + nAB + '/6 = ' + nU + '/6'];
      /* --- marbles --- */
      var gM = F.add(A.g(), function (k) { return k === 3 ? 1 : 0; });
      A.rect(30, 52, 150, 120, 'f-none s-soft w2', gM, 16);
      A.text(105, 190, '袋子：3 红 4 蓝', { cls: 't-s', anchor: 'middle' }, gM);
      [[62, 92], [96, 92], [130, 92]].forEach(function (p) { A.circle(p[0], p[1], 12, 'f-bad', gM); });
      [[79, 136], [113, 136], [147, 136]].forEach(function (p) { A.circle(p[0], p[1], 12, 'f-acc', gM); });
      var mv = A.circle(160, 92, 12, 'f-acc', gM);
      A.text(212, 66, '先摸出 1 个蓝：P(B) = 4/7', { cls: 't-s' }, gM);
      var mt = A.g({}, gM);
      A.text(212, 146, '袋里剩 3 红 3 蓝', { cls: 't-s' }, mt);
      A.text(212, 168, 'P(红 | B) = 3/6 = 1/2', { cls: 't-b' }, mt);
      A.text(212, 190, '核对：4/7 × 3/6 = 2/7 = P(B∩红)', { cls: 't-s' }, mt);
      /* --- tree --- */
      var pG = 0.8, pF = 0.2, eG = 1e-4, eF = 1e-2, j1 = pG * eG, j2 = pF * eF, tot = j1 + j2;
      var gT = F.add(A.g(), function (k) { return k >= 4 ? 1 : 0; });
      A.circle(26, 120, 6, 'f-soft', gT);
      A.line(30, 117, 100, 72, 's-soft w2', gT); A.line(30, 123, 100, 168, 's-soft w2', gT);
      F.add(A.g({}, gT), function (k) { return k === 5 ? 1 : 0; }).appendChild(A.path('M30 123L100 168M158 170L200 170', 's-bad w4'));
      A.rect(100, 58, 58, 26, 'f-goods s-good w1', gT, 6); A.text(129, 76, '好', { cls: 't-b', anchor: 'middle' }, gT);
      A.rect(100, 156, 58, 26, 'f-bads s-bad w1', gT, 6); A.text(129, 174, '深衰落', { cls: 't-b', anchor: 'middle' }, gT);
      A.text(58, 86, String(pG), { cls: 't-s t-b', anchor: 'middle' }, gT); A.text(58, 162, String(pF), { cls: 't-s t-b', anchor: 'middle' }, gT);
      A.line(158, 71, 200, 71, 's-soft w2', gT); A.line(158, 170, 200, 170, 's-soft w2', gT);
      A.text(179, 63, '10^{−4}', { cls: 't-s', anchor: 'middle' }, gT); A.text(179, 162, '10^{−2}', { cls: 't-s', anchor: 'middle' }, gT);
      A.rect(200, 58, 40, 26, 'f-card s-soft w1', gT, 6); A.text(220, 76, '错', { anchor: 'middle' }, gT);
      A.rect(200, 156, 40, 26, 'f-card s-soft w1', gT, 6); A.text(220, 174, '错', { anchor: 'middle' }, gT);
      A.text(248, 76, '0.8×10^{−4} = ' + j1.toFixed(5), { cls: 't-s t-m' }, gT);
      A.text(248, 175, '0.2×10^{−2} = ' + j2.toFixed(3), { cls: 't-s t-m' }, gT);
      A.text(200, 214, 'P(错) = ' + j1.toFixed(5) + ' + ' + j2.toFixed(3) + ' = ' + tot.toFixed(5), { cls: 't-b', anchor: 'middle' }, gT);
      F.add(A.text(296, 126, 'P(衰落 | 错) = ' + j2.toFixed(3) + '/' + tot.toFixed(5) + ' ≈ ' + Math.round(j2 / tot * 100) + '%', { cls: 't-b f-bad', anchor: 'middle' }, gT), function (k) { return k === 5 ? 1 : 0; });
      var cur = 0;
      return {
        step: function (k) { cur = k; F.step(k); if (k <= 2) A.setText(dtxt, dl[k]); },
        frame: function (ts) {
          F.frame(ts);
          var p = cur === 3 ? A.prog(ts, 0.9, 0.3) : 0;
          A.set(mv, { cx: A.lerp(160, 300, p), cy: A.lerp(92, 106, p) });
          mt.setAttribute('opacity', (cur === 3 ? A.prog(ts, 0.6, 1.0) : 0).toFixed(2));
        }
      };
    }
  });

  /* ================= 1.3 mean / variance ================= */
  ANIM.reg('p2:1.3', {
    title: '期望是平衡点，方差是抖动',
    cap: '看什么：竖线位置 = 取值，高度 = 概率（Practice 4 第 2 题的 SNR：⅓ 取 8，⅔ 取 11）。金色虚线是期望（跷跷板的平衡点），金色横条是 ±σ。看 aX + b 和两路相加时它们怎么变。',
    h: 212,
    tween: 1.4,
    steps: [
      'X（线性 SNR）：⅓ 的概率取 8，⅔ 的概率取 11。竖线高度 = 概率。',
      '期望 = 按概率加权平均：8×⅓ + 11×⅔ = 10，就是跷跷板的平衡点。',
      'E[X²] = 64×⅓ + 121×⅔ = 102，Var = 102 − 10² = 2，σ ≈ 1.41。',
      'Y = 2X + 3：取值 19、25。E[Y] = 23，Var(Y) = 2²×2 = 8（“+3”不改方差）。',
      '两路独立相加 X₁+X₂：取 16、19、22（概率 1/9、4/9、4/9），均值 20，方差 2+2 = 4。'
    ],
    init: function (A) {
      var t3 = 1 / 3, ST = [
        { n: 'X', v: [8, 11, 11], p: [t3, 2 * t3, 0], l: ['1/3', '2/3', ''] },
        { n: 'Y', v: [19, 25, 25], p: [t3, 2 * t3, 0], l: ['1/3', '2/3', ''] },
        { n: 'X₁+X₂', v: [16, 19, 22], p: [1 / 9, 4 / 9, 4 / 9], l: ['1/9', '4/9', '4/9'] }
      ];
      var map = [0, 0, 0, 1, 2];
      var tk = []; for (var v = 0; v <= 30; v += 5) tk.push({ v: v, l: v === 0 || v === 30 ? String(v) : '' });
      var ax = A.axes({ x: 30, y: 44, w: 352, h: 120, xr: [0, 31], yr: [0, 0.95], ticksX: tk, xl: '' });
      var meanL = A.line(0, 40, 0, 164, 's-gold w2 dash'), meanT = A.text(0, 36, '', { cls: 't-s t-b f-gold', anchor: 'middle' });
      var sig = A.line(0, 52, 0, 52, 's-gold w4'), sigT = A.text(0, 56, '±σ', { cls: 't-s f-gold' });
      var stems = [];
      for (var i = 0; i < 3; i++) {
        var g = A.g();
        stems.push({ g: g, l: A.line(0, 0, 0, 0, 's-acc w3', g), c: A.circle(0, 0, 5, 'f-acc', g), pt: A.text(0, 0, '', { cls: 't-s t-b', anchor: 'middle' }, g), vt: A.text(0, 180, '', { cls: 't-b f-acc', anchor: 'middle' }, g) });
      }
      var info = A.text(12, 204, '', { cls: 't-m' });
      var cur = 0, prev = 0;
      function stats(s) {
        var m = 0, m2 = 0;
        for (var i = 0; i < 3; i++) { m += s.v[i] * s.p[i]; m2 += s.v[i] * s.v[i] * s.p[i]; }
        return { m: m, v: m2 - m * m, m2: m2 };
      }
      return {
        step: function (k) { prev = cur; cur = k; },
        frame: function (ts, dt, k) {
          var a = ST[map[prev]], b = ST[map[k]], p = A.prog(ts, 1.0);
          if (map[prev] === map[k]) p = 1;
          for (var i = 0; i < 3; i++) {
            var vv = A.lerp(a.v[i], b.v[i], p), pp = A.lerp(a.p[i], b.p[i], p), s = stems[i];
            var x = ax.X(vv), y = ax.Y(pp);
            A.set(s.l, { x1: x, y1: ax.Y(0), x2: x, y2: y }); A.set(s.c, { cx: x, cy: y });
            A.set(s.pt, { x: x, y: y - 9, text: p > 0.5 ? b.l[i] : a.l[i] }); A.set(s.vt, { x: x, text: String(Math.round(vv)) });
            s.g.style.display = pp < 0.01 ? 'none' : '';
          }
          var sa = stats(a), sb = stats(b), m = A.lerp(sa.m, sb.m, p), sd = Math.sqrt(A.lerp(sa.v, sb.v, p));
          var showM = k >= 1, showS = k >= 2;
          meanL.style.display = meanT.style.display = showM ? '' : 'none';
          sig.style.display = sigT.style.display = showS ? '' : 'none';
          A.set(meanL, { x1: ax.X(m), x2: ax.X(m) }); A.set(meanT, { x: ax.X(m), text: 'E = ' + A.fmt(m, 4) });
          A.set(sig, { x1: ax.X(m - sd), x2: ax.X(m + sd) }); A.set(sigT, { x: ax.X(m + sd) + 5 });
          var t = b.n + '：';
          if (k === 0) t += '取值 ' + b.v[0] + '、' + b.v[1] + '，概率 ⅓、⅔';
          else if (k === 1) t += 'E = ' + A.fmt(sb.m, 4);
          else t += 'E = ' + A.fmt(sb.m, 4) + '　E[' + (k === 4 ? '(X₁+X₂)' : b.n) + '²] = ' + A.fmt(sb.m2, 4) + '　Var = ' + A.fmt(sb.v, 4) + '　σ = ' + A.fmt(Math.sqrt(sb.v), 3);
          A.setText(info, t);
        }
      };
    }
  });

  /* ================= 1.4 PDF and CDF ================= */
  ANIM.reg('p2:1.4', {
    title: 'PDF 下的面积 = CDF 的高度',
    cap: '看什么：拖动 x，上图蓝色面积 = P(X ≤ x)，正好是下图 CDF 在 x 处的高度。默认是正文例题：指数分布 γ̄ = 100，γ₀ = 10 → 面积 0.095。',
    h: 242,
    init: function (A) {
      var D = [
        { xr: [0, 400], yr: [0, 0.0118], pdf: function (x) { return x < 0 ? 0 : Math.exp(-x / 100) / 100; }, cdf: function (x) { return x < 0 ? 0 : 1 - Math.exp(-x / 100); }, tx: [0, 100, 200, 300, 400], v: 'γ', p0: 2.5,
          note: '指数分布（瑞利衰落下的 SNR）：P(γ ≤ γ₀) = 1 − e<sup>−γ₀/γ̄</sup>，γ̄ = 100' },
        { xr: [-4, 4], yr: [0, 0.45], pdf: function (x) { return gpdf(x, 0, 1); }, cdf: function (x) { return 1 - A.Q(x); }, tx: [-3, -2, -1, 0, 1, 2, 3], v: 'x', p0: 62.5,
          note: '标准高斯 N(0, 1)：F(x) = 1 − Q(x)，钟形对称，F(0) = 0.5' },
        { xr: [-2, 12], yr: [0, 0.118], pdf: function (x) { return x >= 0 && x <= 10 ? 0.1 : 0; }, cdf: function (x) { return A.clamp(x / 10, 0, 1); }, tx: [0, 5, 10], v: 'x', p0: 50,
          note: '均匀 U(0, 10)：PDF = 1/10，F(x) = x/10，面积是一个长方形' }
      ];
      var cur = 0, pos = D[0].p0, gP = A.g(), gC = A.g(), ax1, ax2, shade, vl1, vl2, dot, hl, vt, at;
      function xOf(p) { var d = D[cur]; return d.xr[0] + p / 100 * (d.xr[1] - d.xr[0]); }
      function build() {
        while (gP.firstChild) gP.removeChild(gP.firstChild);
        while (gC.firstChild) gC.removeChild(gC.firstChild);
        var d = D[cur];
        ax1 = A.axes({ x: 44, y: 26, w: 334, h: 78, xr: d.xr, yr: d.yr, ticksX: d.tx, yl: 'PDF p(' + d.v + ')', parent: gP, yAxisAt: 'left' });
        shade = A.path('', 'f-accs s-none', gP);
        A.curve(ax1, d.pdf, 's-acc w2', gP, 280);
        vl1 = A.line(0, 26, 0, 104, 's-ink w1 dash', gP);
        at = A.text(386, 22, '', { cls: 't-s t-b f-acc', anchor: 'end' }, gP);
        ax2 = A.axes({ x: 44, y: 144, w: 334, h: 74, xr: d.xr, yr: [0, 1.12], ticksX: d.tx, ticksY: [{ v: 0.5, l: '0.5' }, { v: 1, l: '1' }], yl: 'CDF F(' + d.v + ')', parent: gC, yAxisAt: 'left' });
        A.curve(ax2, d.cdf, 's-gold w2', gC, 280);
        vl2 = A.line(0, 144, 0, 218, 's-ink w1 dash', gC);
        hl = A.line(44, 0, 0, 0, 's-gold w1 dash', gC);
        dot = A.circle(0, 0, 5, 'f-gold', gC);
        vt = A.text(0, 0, '', { cls: 't-s t-b f-gold' }, gC);
        A.note(d.note);
      }
      function draw() {
        var d = D[cur], x = xOf(pos), Fx = d.cdf(x), pts = [[ax1.X(d.xr[0]), ax1.Y(0)]];
        for (var i = 0; i <= 160; i++) { var u = d.xr[0] + (x - d.xr[0]) * i / 160; pts.push([ax1.X(u), ax1.Y(d.pdf(u))]); }
        pts.push([ax1.X(x), ax1.Y(0)]);
        A.set(shade, { d: A.pts(pts) + 'Z' });
        A.set(vl1, { x1: ax1.X(x), x2: ax1.X(x) }); A.set(vl2, { x1: ax2.X(x), x2: ax2.X(x) });
        A.set(hl, { y1: ax2.Y(Fx), x2: ax2.X(x), y2: ax2.Y(Fx) }); A.set(dot, { cx: ax2.X(x), cy: ax2.Y(Fx) });
        var right = ax2.X(x) < 300;
        A.set(vt, { x: ax2.X(x) + (right ? 8 : -8), y: ax2.Y(Fx) + (Fx > 0.85 ? 14 : -6), 'text-anchor': right ? 'start' : 'end', text: 'F(' + A.fmt(x, 3) + ') = ' + Fx.toFixed(3) });
        A.setText(at, '蓝色面积 = P(' + d.v + ' ≤ ' + A.fmt(x, 3) + ') = ' + Fx.toFixed(3));
      }
      var sl = A.slider({ label: 'x 的位置', min: 0, max: 100, step: 0.5, value: pos, fmt: function (p) { return D[cur].v + ' = ' + A.fmt(xOf(p), 3); }, on: function (p) { pos = p; draw(); } });
      A.choice({ label: '分布', options: ['指数 γ̄=100', '高斯 N(0,1)', '均匀 U(0,10)'], value: 0, on: function (i) { cur = i; build(); sl.set(D[i].p0); } });
      build(); draw();
      return {};
    }
  });

  /* ================= 1.5 Gaussian and Q ================= */
  ANIM.reg('p2:1.5', {
    title: 'Q(x)：钟形曲线右边那条尾巴',
    cap: '看什么：Q(x) = P(Z > x) 是标准高斯右尾的面积（考卷给 Q 表）。由对称性，左尾 P(Z < −x) 也是 Q(x)；中间那块是 1 − 2Q(x)。',
    h: 206,
    init: function (A) {
      var x = 1, mode = 0;
      var ax = A.axes({ x: 30, y: 30, w: 352, h: 128, xr: [-4, 4], yr: [0, 0.45], ticksX: [-3, -2, -1, 0, 1, 2, 3], xl: 'z' });
      var sh = A.path('', 'f-bad s-none op3');
      A.curve(ax, function (z) { return gpdf(z, 0, 1); }, 's-acc w2', null, 240);
      var lR = A.line(0, 34, 0, 158, 's-ink w1 dash'), lL = A.line(0, 34, 0, 158, 's-ink w1 dash');
      var tR = A.text(0, 30, '', { cls: 't-s' }), tL = A.text(0, 30, '', { cls: 't-s', anchor: 'end' });
      var big = A.text(200, 196, '', { cls: 't-l t-b', anchor: 'middle' });
      function area(a, b) {
        var pts = [[ax.X(a), ax.Y(0)]];
        for (var i = 0; i <= 90; i++) { var u = a + (b - a) * i / 90; pts.push([ax.X(u), ax.Y(gpdf(u, 0, 1))]); }
        pts.push([ax.X(b), ax.Y(0)]);
        return A.pts(pts) + 'Z';
      }
      function draw() {
        var q = A.Q(x), xs = A.fmt(x, 3);
        A.set(sh, { d: mode === 0 ? area(x, 4) : mode === 1 ? area(-4, -x) : area(-x, x) });
        A.set(lR, { x1: ax.X(x), x2: ax.X(x) }); A.set(lL, { x1: ax.X(-x), x2: ax.X(-x) });
        lL.style.display = tL.style.display = mode === 0 ? 'none' : '';
        lR.style.display = tR.style.display = mode === 1 ? 'none' : '';
        A.set(tR, { x: ax.X(x) + (x > 3.2 ? -3 : 3), 'text-anchor': x > 3.2 ? 'end' : 'start', text: 'x = ' + xs }); A.set(tL, { x: ax.X(-x) - 3, text: '−' + xs });
        var t = mode === 0 ? 'Q(' + xs + ') = P(Z > ' + xs + ') = ' + fp(q)
          : mode === 1 ? 'P(Z < −' + xs + ') = Q(' + xs + ') = ' + fp(q)
            : 'P(|Z| < ' + xs + ') = 1 − 2Q(' + xs + ') = ' + (1 - 2 * q).toFixed(3);
        A.setText(big, t);
      }
      var sl = A.slider({ label: 'x', min: 0, max: 4, step: 0.005, value: x, fmt: function (v) { return v.toFixed(3); }, on: function (v) { x = v; draw(); } });
      var ch = A.choice({ label: '看哪块', options: ['右尾 Q(x)', '左尾', '中间'], value: 0, on: function (i) { mode = i; draw(); } });
      A.button('反查 Q = 0.01', function () { ch.set(0, true); mode = 0; sl.set(2.33); });
      A.button('例 Q(0.625)', function () { ch.set(1, true); mode = 1; sl.set(0.625); });
      A.note('表里常用：Q(1) = 0.159，Q(2) = 0.0228，Q(2.33) ≈ 0.0099，Q(3) = 0.00135');
      draw();
      return {};
    }
  });

  /* ================= 2.1 path-loss least squares ================= */
  ANIM.reg('p2:2.1', {
    title: '最小二乘拟合 K 和 γ（Practice 1 Q1）',
    cap: '看什么：六个实测点画在 x = 10 log₁₀d 的横轴上，dB 模型 M = K<sub>dB</sub> − γx 是一条直线。直线绕平均点转到误差平方和最小，剩下的平均误差平方就是阴影方差 σψ²。',
    h: 236,
    tween: 2.0,
    steps: [
      '六个实测点：d = 5–1000 m，M = (Pr/Pt) dB。横轴 x = 10 log₁₀d（d₀ = 1 m）。',
      'dB 形式 M = KdB − γx 是直线。最小二乘的直线一定过平均点 (x̄, M̄)。',
      '绕平均点转动直线，让误差平方和最小：斜率 −3.94 → γ ≈ 3.94，KdB ≈ −30.8 dB。',
      '残差 ei = 实测 − 直线（红线），有正有负，加起来为 0。',
      'MSE = Σe²/6 ≈ 11.87 dB²，就是阴影方差 σψ²，σψ ≈ 3.45 dB（下一节要用）。'
    ],
    init: function (A) {
      var d = [5, 25, 65, 110, 400, 1000], M = [-60, -80, -105, -115, -130, -150], n = 6, i;
      var x = d.map(function (v) { return 10 * Math.log10(v); });
      var xb = 0, Mb = 0; for (i = 0; i < n; i++) { xb += x[i] / n; Mb += M[i] / n; }
      var sxy = 0, sxx = 0; for (i = 0; i < n; i++) { sxy += (x[i] - xb) * (M[i] - Mb); sxx += (x[i] - xb) * (x[i] - xb); }
      var gam = -sxy / sxx, K = Mb + gam * xb;
      function mse(s) { var e = 0; for (var i = 0; i < n; i++) { var r = M[i] - (Mb + s * (x[i] - xb)); e += r * r; } return e / n; }
      var ax = A.axes({ x: 52, y: 20, w: 326, h: 160, xr: [0, 35], yr: [-165, -45], ticksX: [0, 10, 20, 30], ticksY: [-60, -90, -120, -150], yl: 'M (dB)' });
      ['1 m', '10 m', '100 m', '1 km'].forEach(function (s, j) { A.text(ax.X(j * 10), 207, 'd = ' + s, { cls: 't-s f-acc', anchor: 'middle' }); });
      A.text(215, 228, '横轴 x = 10 log₁₀d（每 10 个单位 = 距离 ×10）', { cls: 't-s', anchor: 'middle' });
      var line = A.line(0, 0, 0, 0, 's-gold w2');
      var res = A.g();
      var rl = x.map(function () { return A.line(0, 0, 0, 0, 's-bad w2', res); });
      x.forEach(function (v, j) { A.circle(ax.X(v), ax.Y(M[j]), 4.2, 'f-acc'); });
      var mp = A.g();
      A.circle(ax.X(xb), ax.Y(Mb), 6, 'f-gold s-card w2', mp);
      A.text(ax.X(xb) + 8, ax.Y(Mb) - 12, '(x̄, M̄) = (' + xb.toFixed(2) + ', ' + Mb.toFixed(1) + ')', { cls: 't-s t-b f-gold' }, mp);
      var r1 = A.text(374, 36, '', { cls: 't-b', anchor: 'end' }), r2 = A.text(374, 54, '', { cls: 't-s', anchor: 'end' });
      return {
        frame: function (ts, dt, k) {
          var s = k < 2 ? 0 : k === 2 ? A.lerp(0, -gam, A.prog(ts, 1.6, 0.2)) : -gam;
          mp.style.display = k >= 1 ? '' : 'none';
          line.style.display = k >= 2 ? '' : 'none';
          res.style.display = k >= 3 ? '' : 'none';
          A.set(line, { x1: ax.X(4), y1: ax.Y(Mb + s * (4 - xb)), x2: ax.X(34), y2: ax.Y(Mb + s * (34 - xb)) });
          for (var j = 0; j < n; j++) A.set(rl[j], { x1: ax.X(x[j]), y1: ax.Y(M[j]), x2: ax.X(x[j]), y2: ax.Y(Mb + s * (x[j] - xb)) });
          var m = mse(s);
          A.setText(r1, k < 2 ? '' : k < 4 ? 'γ = ' + (-s).toFixed(2) + '，K_{dB} = ' + (Mb - s * xb).toFixed(1) + ' dB' : 'σ_{ψ}^{2} = MSE = ' + m.toFixed(2) + ' dB²');
          A.setText(r2, k < 2 ? '' : k < 4 ? 'MSE = ' + m.toFixed(2) + ' dB²' + (k === 2 && s > -gam + 1e-6 ? '（还在变小）' : '（最小）') : 'σ_{ψ} = ' + Math.sqrt(m).toFixed(2) + ' dB');
          A.note(k >= 3 ? '残差 e<sub>i</sub>：' + x.map(function (v, j) { var e = M[j] - (K - gam * v); return (e >= 0 ? '+' : '') + e.toFixed(2); }).join('，') + '（和 = 0）' : '');
        }
      };
    }
  });

  /* ================= 2.2 shadowing outage ================= */
  ANIM.reg('p2:2.2', {
    title: '阴影中断：Pout = Q(余量 / σ)',
    cap: '看什么：有阴影时接收功率（dBm）是以平均值为中心的高斯。红色面积 = 低于门限的概率 = 中断概率。默认是第 2 章 p.16 例题：平均 −113.06 dBm、门限 −118 dBm、MSE = 3.36（是方差，要开根号）。',
    h: 216,
    init: function (A) {
      var mu = 0 - 26.67 - 39.7 * Math.log10(150), mg = 4.94, v2 = 3.36;
      var ao = { x: 30, y: 46, w: 352, h: 114, xr: [-140, -96], yr: [0, 1], ticksX: [-140, -130, -120, -110, -100] };
      var ax = A.axes(ao);
      A.text(394, 174, 'dBm', { cls: 't-s', anchor: 'end' });
      var sh = A.path('', 'f-bad s-none op3'), cv = A.path('', 's-acc w2');
      A.line(ax.X(mu), 24, ax.X(mu), 160, 's-soft w1 dash');
      var tl = A.line(0, 24, 0, 160, 's-bad w2');
      var mt = A.text(0, 18, '', { cls: 't-s' }), tt = A.text(0, 18, '', { cls: 't-s f-bad' });
      var br = A.arrow(0, 0, 0, 0, 's-gold w2', null, 6), bt = A.text(0, 0, '', { cls: 't-s t-b f-gold', anchor: 'middle' });
      var big = A.text(200, 194, '', { cls: 't-b', anchor: 'middle' }), sm = A.text(200, 211, '', { cls: 't-s', anchor: 'middle' });
      function draw() {
        var s = Math.sqrt(v2), thr = mu - mg, k = Math.round(mg / s * 100) / 100, q = A.Q(k);
        ao.yr = [0, 1.2 * gpdf(0, 0, s)];
        A.setCurve(cv, ax, function (u) { return gpdf(u, mu, s); }, 240);
        var lo = -140, pts = [[ax.X(lo), ax.Y(0)]];
        for (var i = 0; i <= 120; i++) { var u = lo + (Math.max(lo, thr) - lo) * i / 120; pts.push([ax.X(u), ax.Y(gpdf(u, mu, s))]); }
        pts.push([ax.X(Math.max(lo, thr)), ax.Y(0)]);
        A.set(sh, { d: A.pts(pts) + 'Z' });
        var xt = ax.X(thr), xm = ax.X(mu), pos = mg >= 0;
        A.set(tl, { x1: xt, x2: xt });
        A.set(mt, { x: xm + (pos ? 4 : -4), 'text-anchor': pos ? 'start' : 'end', text: '平均 ' + mu.toFixed(2) });
        A.set(tt, { x: xt + (pos ? -4 : 4), 'text-anchor': pos ? 'end' : 'start', text: '门限 ' + thr.toFixed(2) });
        A.moveArrow(br, xm, 41, xt, 41);
        A.set(bt, { x: (xm + xt) / 2, y: 35, text: '余量 ' + mg.toFixed(2) + ' dB' });
        A.setText(big, 'P_{out} = Q(' + mg.toFixed(2) + ' / ' + s.toFixed(3) + ') = Q(' + k.toFixed(2) + ') = ' + fp(q));
        A.setText(sm, '中断 1% 需要余量 ≥ 2.326σ = ' + (2.326 * s).toFixed(2) + ' dB（查表前 k 舍到 2 位小数）');
      }
      A.slider({ label: '余量（dB）', min: -5, max: 15, step: 0.01, value: mg, fmt: function (v) { return v.toFixed(2) + ' dB'; }, on: function (v) { mg = v; draw(); } });
      A.slider({ label: '阴影方差 σ²', min: 1, max: 64, step: 0.01, value: v2, fmt: function (v) { return v.toFixed(2) + ' dB² → σ = ' + Math.sqrt(v).toFixed(3); }, on: function (v) { v2 = v; draw(); } });
      draw();
      return {};
    }
  });

  /* ================= 2.3 multipath phasors → Rayleigh ================= */
  ANIM.reg('p2:2.3', {
    title: '回波相量相加：包络为什么是瑞利',
    cap: '看什么：左边每支灰箭头是一条回波，手机移动时各自按自己的多普勒频移转动；首尾相接的合成箭头（金）长度就是包络 z。掉进红圈（ρ = 0.3）就是深衰落。右上是 z 随时间的起伏（dB），右下把很多时刻的 z 攒成直方图，越来越像瑞利 PDF。',
    h: 282,
    init: function (A) {
      var N = 12, al = [], th = [], ph = [], s = 0, i, fm = 0.4;
      for (i = 0; i < N; i++) { al.push(0.5 + A.rand()); th.push(2 * Math.PI * (i + A.rand()) / N); ph.push(2 * Math.PI * A.rand()); s += al[i] * al[i]; }
      for (i = 0; i < N; i++) al[i] /= Math.sqrt(s);
      function sum(t, chain) {
        var re = 0, im = 0;
        for (var i = 0; i < N; i++) { var p = ph[i] + 2 * Math.PI * fm * Math.cos(th[i]) * t; re += al[i] * Math.cos(p); im += al[i] * Math.sin(p); if (chain) chain.push([re, im]); }
        return Math.sqrt(re * re + im * im);
      }
      var O = [100, 150], S = 66;
      var defs = A.el('defs'), cp = A.el('clipPath', { id: 'p2c23clip' }, defs);
      A.el('rect', { x: 2, y: 22, width: 200, height: 240 }, cp);
      A.text(8, 16, '回波相量首尾相接（相对 z_{rms}）', { cls: 't-s' });
      A.circle(O[0], O[1], S, 'f-none s-soft w1 dash');
      A.circle(O[0], O[1], 0.3 * S, 'f-bads s-bad w1 dash');
      A.text(O[0], O[1] - S - 4, 'z_{rms}', { cls: 't-s', anchor: 'middle' });
      var gp = A.g({ 'clip-path': 'url(#p2c23clip)' });
      var arr = []; for (i = 0; i < N; i++) arr.push(A.arrow(0, 0, 1, 1, 's-soft w1', gp, 5));
      var res = A.arrow(0, 0, 1, 1, 's-gold w3', gp, 8);
      var zt = A.text(8, 276, '', { cls: 't-m' }), dt2 = A.text(200, 276, '深衰落！', { cls: 't-b f-bad', anchor: 'end' });
      /* envelope strip */
      A.text(222, 16, '包络 z(t)，dB（最近 4 秒）', { cls: 't-s' });
      var ax = A.axes({ x: 226, y: 28, w: 160, h: 82, xr: [-4, 0], yr: [-25, 8], ticksY: [{ v: 0, l: '0' }, { v: -20, l: '−20' }], xAxisAt: 'bottom', yAxisAt: 'left' });
      A.line(226, ax.Y(20 * Math.log10(0.3)), 386, ax.Y(20 * Math.log10(0.3)), 's-bad w1 dash');
      var env = A.path('', 's-acc w2'), now = A.circle(0, 0, 3.5, 'f-gold');
      /* histogram */
      A.text(222, 140, '很多时刻 z/z_{rms} 的直方图', { cls: 't-s' });
      var hx = A.axes({ x: 226, y: 152, w: 160, h: 98, xr: [0, 2.6], yr: [0, 1.05], ticksX: [0, 1, 2], xAxisAt: 'bottom', yAxisAt: 'left' });
      var NB = 20, bw = 0.125, bins = [], bars = [], cnt = 0, tot = 0;
      for (i = 0; i < NB; i++) { bins.push(0); bars.push(A.rect(hx.X(i * bw) + 0.5, 250, hx.X(bw) - hx.X(0) - 1, 0, 'f-accs s-acc w1', null, 0)); }
      A.curve(hx, function (z) { return 2 * z * Math.exp(-z * z); }, 's-gold w2', null, 100);
      A.text(hx.X(1.5), hx.Y(0.6), '瑞利 PDF', { cls: 't-s t-b f-gold' });
      var nt = A.text(392, 160, '', { cls: 't-s', anchor: 'end' });
      function add(m) {
        for (var j = 0; j < m; j++) { var z = sum(37 + cnt * 0.37); cnt++; var b = Math.floor(z / bw); if (b < NB) bins[b]++; tot++; }
      }
      function reset() { for (var j = 0; j < NB; j++) bins[j] = 0; cnt = 0; tot = 0; add(40); }
      reset();
      return {
        reset: reset,
        frame: function (t, dt) {
          if (dt > 0) add(6);
          var ch = [], z = sum(t, ch), px = O[0], py = O[1];
          for (var i = 0; i < N; i++) { var nx = O[0] + S * ch[i][0], ny = O[1] - S * ch[i][1]; A.moveArrow(arr[i], px, py, nx, ny); px = nx; py = ny; }
          A.moveArrow(res, O[0], O[1], px, py);
          A.setText(zt, 'z = ' + z.toFixed(2) + ' z_{rms}');
          dt2.style.display = z < 0.3 ? '' : 'none';
          var pts = [];
          for (var k = 0; k <= 90; k++) { var u = -4 + 4 * k / 90; pts.push([u, Math.max(-25, 20 * Math.log10(sum(t + u) + 1e-9))]); }
          A.setCurve(env, ax, pts);
          A.set(now, { cx: ax.X(0), cy: ax.Y(Math.max(-25, 20 * Math.log10(z + 1e-9))) });
          for (var b = 0; b < NB; b++) { var hgt = Math.min(1.05, bins[b] / (tot * bw)); var y = hx.Y(hgt); A.set(bars[b], { y: y, height: Math.max(0, 250 - y) }); }
          A.setText(nt, '已统计 ' + tot + ' 个');
        }
      };
    }
  });

  /* ================= 2.4 delay spread / ISI ================= */
  ANIM.reg('p2:2.4', {
    title: '时延扩展 vs 符号时长：会不会 ISI',
    cap: '看什么：上面是正文例题的功率时延分布（0、1、2 µs，0/−3/−6 dB），按线性功率加权得 μ 和 σ。下面三行是三条回波各自送来的三个符号；红色是拖进下一个符号时段的部分（ISI）。拖动 T<sub>s</sub>，看 σ<sub>Tm</sub>/T<sub>s</sub> 和 0.1 比。',
    h: 268,
    init: function (A) {
      var tau = [0, 1, 2], pdb = [0, -3, -6], P = pdb.map(function (v) { return Math.round(A.undb(v) * 100) / 100; });
      var sp = 0, m1 = 0, m2 = 0, i, j;
      for (i = 0; i < 3; i++) { sp += P[i]; m1 += P[i] * tau[i]; m2 += P[i] * tau[i] * tau[i]; }
      var mu = m1 / sp, sig = Math.sqrt(m2 / sp - mu * mu), Ts = 10;
      var ax = A.axes({ x: 30, y: 30, w: 150, h: 70, xr: [-0.6, 2.6], yr: [0, 1.15], ticksX: [{ v: 0, l: '0' }, { v: 1, l: '1' }, { v: 2, l: '2 µs' }], yAxisAt: 'left' });
      A.text(30, 18, '功率时延分布 P_{r}(τ)', { cls: 't-s' });
      for (i = 0; i < 3; i++) {
        A.line(ax.X(tau[i]), ax.Y(0), ax.X(tau[i]), ax.Y(P[i]), 's-acc w3');
        A.text(ax.X(tau[i]), ax.Y(P[i]) - 5, pdb[i] === 0 ? '0 dB' : '−' + (-pdb[i]) + ' dB', { cls: 't-s', anchor: 'middle' });
      }
      var by = 122;
      A.line(ax.X(mu - sig), by, ax.X(mu + sig), by, 's-gold w2');
      A.line(ax.X(mu - sig), by - 4, ax.X(mu - sig), by + 4, 's-gold w2'); A.line(ax.X(mu + sig), by - 4, ax.X(mu + sig), by + 4, 's-gold w2');
      A.circle(ax.X(mu), by, 3.5, 'f-gold');
      A.text(ax.X(mu + sig) + 5, by + 4, 'μ ± σ', { cls: 't-s f-gold' });
      A.text(206, 34, 'μ_{Tm} = ' + mu.toFixed(3) + ' µs', { cls: 't-m' });
      A.text(206, 52, 'σ_{Tm} = ' + sig.toFixed(3) + ' µs', { cls: 't-m' });
      var r1 = A.text(206, 72, '', { cls: 't-m' }), vd = A.text(206, 92, '', { cls: 't-b' });
      A.text(206, 110, '平坦要 T_{s} > σ/0.1 = ' + (sig / 0.1).toFixed(2) + ' µs', { cls: 't-s' });
      /* symbol rows */
      var X0 = 50, XW = 340, ry = [160, 188, 216], cols = ['f-accs s-acc', 'f-golds s-gold', 'f-purs s-pur'];
      ['τ=0', 'τ=1', 'τ=2'].forEach(function (s, k) { A.text(4, ry[k] + 4, s, { cls: 't-s' }); });
      A.text(4, 146, '回波', { cls: 't-s' });
      A.line(X0, 232, X0 + XW, 232, 's-soft w1');
      var bnd = [], bl = [], sl = [], own = [], spill = [];
      for (i = 0; i < 3; i++) {
        bnd.push(A.line(0, 140, 0, 232, 's-line w1 dash'));
        bl.push(A.text(0, 244, (i + 1) + 'T_{s}', { cls: 't-s', anchor: 'middle' }));
        sl.push(A.text(0, 142, '符号 ' + (i + 1), { cls: 't-s', anchor: 'middle' }));
        for (j = 0; j < 3; j++) { own.push(A.rect(0, 0, 0, 0, cols[i] + ' w1', null, 1)); spill.push(A.rect(0, 0, 0, 0, 'f-bads s-bad w1', null, 1)); }
      }
      A.text(200, 263, '红色 = 拖进下一个符号时段的回波（ISI）', { cls: 't-s f-bad', anchor: 'middle' });
      function draw() {
        var span = 3 * Ts + 2.4, X = function (t) { return X0 + t / span * XW; }, slot = X(Ts) - X(0);
        for (var i = 0; i < 3; i++) {
          A.set(bnd[i], { x1: X((i + 1) * Ts), x2: X((i + 1) * Ts) }); A.set(bl[i], { x: X((i + 1) * Ts) });
          A.set(sl[i], { x: X((i + 0.5) * Ts) }); sl[i].style.display = slot > 44 ? '' : 'none';
          bl[i].style.display = slot > 26 ? '' : 'none';
          for (var j = 0; j < 3; j++) {
            var hgt = 22 * Math.sqrt(P[j]), y = ry[j] - hgt / 2, a = i * Ts + tau[j], b = (i + 1) * Ts + tau[j], e = (i + 1) * Ts;
            A.set(own[i * 3 + j], { x: X(a), y: y, width: Math.max(0, X(Math.min(b, e)) - X(a)), height: hgt });
            var s0 = Math.max(a, e);
            A.set(spill[i * 3 + j], { x: X(s0), y: y, width: Math.max(0, X(b) - X(s0)), height: hgt });
          }
        }
        var r = sig / Ts;
        A.setText(r1, 'T_{s} = ' + A.fmt(Ts, 3) + ' µs → σ/T_{s} = ' + r.toFixed(3));
        A.set(vd, { cls: 't-b ' + (r < 0.1 ? 'f-good' : r < 0.5 ? 'f-gold' : 'f-bad'),
          text: r < 0.1 ? '< 0.1 → 平坦衰落' : r < 0.5 ? '略大于 0.1：不能直接下结论' : '远大于 0.1 → 频率选择性（ISI）' });
        A.note('符号速率 R<sub>s</sub> = 1/T<sub>s</sub> = ' + A.fmt(1000 / Ts, 3) + ' ksps；平坦衰落要 R<sub>s</sub> &lt; ' + A.fmt(100 / sig, 3) + ' ksps');
      }
      A.slider({ label: '符号时长 T<sub>s</sub>', min: 0.5, max: 30, step: 0.1, value: Ts, unit: 'µs', on: function (v) { Ts = v; draw(); } });
      draw();
      return {};
    }
  });

  /* ================= 2.5 Doppler, T_C vs T_s ================= */
  ANIM.reg('p2:2.5', {
    title: '多普勒：相干时间 TC 和符号时长比',
    cap: '看什么：蓝线是接收包络在 20 ms 里的起伏，车越快、载频越高，起伏越密（f<sub>m</sub> = v f<sub>c</sub>/c）。下面把一个符号 T<sub>s</sub> 和相干时间 T<sub>C</sub> ≈ 1/f<sub>m</sub> 摆在一起比：T<sub>s</sub> ≪ T<sub>C</sub> 是慢衰落。',
    h: 228,
    speed: 1,
    init: function (A) {
      var v = 120, fcI = 2, tsI = 0, FC = [0.9e9, 2e9, 5e9], TS = [1e-6, 1e-4, 1e-3, 5e-3], TSL = ['1 µs', '0.1 ms', '1 ms', '5 ms'];
      var env = sos(A.rng(4242), 16), W = 20e-3;
      var ax = A.axes({ x: 42, y: 20, w: 344, h: 108, xr: [0, 20], yr: [-30, 10], ticksX: [0, 5, 10, 15, { v: 20, l: '20 ms' }], ticksY: [{ v: 0, l: '0 dB' }, { v: -20, l: '−20' }], xAxisAt: 'bottom', yAxisAt: 'left' });
      var cv = A.path('', 's-acc w2');
      var box = A.rect(42, 146, 2, 14, 'f-golds s-gold w1', null, 1), bt = A.text(0, 157, '', { cls: 't-s' });
      var tc = A.line(42, 174, 42, 174, 's-good w3'), tcE = A.line(0, 168, 0, 180, 's-good w2'), tcA = A.text(0, 178, '', { cls: 't-s t-b f-good' });
      var tct = A.text(42, 198, '', { cls: 't-s' }), vd = A.text(42, 218, '', { cls: 't-b' });
      function fm() { return v / 3.6 * FC[fcI] / 3e8; }
      function frame(t) {
        var f = fm(), t0 = t * 0.004, pts = [];
        for (var k = 0; k <= 220; k++) { var u = k / 220 * W; pts.push([u * 1000, Math.max(-30, 20 * Math.log10(env(t0 + u, f) + 1e-9))]); }
        A.setCurve(cv, ax, pts);
        var Ts = TS[tsI], wpx = Math.max(2, Ts / W * 344);
        A.set(box, { width: wpx }); A.set(bt, { x: 42 + wpx + 6, text: '一个符号 T_{s} = ' + TSL[tsI] });
        var Tc = f > 0 ? 1 / f : Infinity, tpx = Math.min(344, Tc / W * 344);
        A.set(tc, { x2: 42 + tpx }); A.set(tcE, { x1: 42 + tpx, x2: 42 + tpx });
        tcE.style.display = Tc <= W ? '' : 'none';
        A.set(tcA, { x: Tc <= W ? 42 + tpx + 6 : 386, 'text-anchor': Tc <= W ? 'start' : 'end', text: Tc <= W ? 'T_{C}' : 'T_{C} → 超出 20 ms' });
        A.setText(tct, f > 0 ? 'f_{m} = ' + f.toFixed(1) + ' Hz，T_{C} ≈ 1/f_{m} = ' + A.fmt(Tc * 1000, 3) + ' ms' : 'v = 0：没有多普勒，信道时不变（T_{C} → ∞）');
        var r = Ts * f;
        A.set(vd, { cls: 't-b ' + (r < 0.1 ? 'f-good' : 'f-bad'),
          text: 'T_{s}/T_{C} = ' + (r >= 0.01 ? r.toFixed(2) : r === 0 ? '0' : r.toPrecision(2)) + (r < 0.1 ? ' ≪ 1 → 慢衰落' : r < 1 ? '，和 T_{C} 相当 → 快衰落' : ' ≥ 1 → 快衰落') });
        A.note('f<sub>m</sub> = v·f<sub>c</sub>/c = ' + (v / 3.6).toFixed(2) + ' m/s × ' + FC[fcI] / 1e9 + ' GHz ÷ 3×10<sup>8</sup> = ' + f.toFixed(1) + ' Hz（km/h 先 ÷ 3.6）');
      }
      A.slider({ label: '车速 v', min: 0, max: 200, step: 1, value: v, unit: 'km/h', on: function (x) { v = x; A.redraw(); } });
      A.choice({ label: '载频 f<sub>c</sub>', options: ['900 MHz', '2 GHz', '5 GHz'], value: fcI, on: function (i) { fcI = i; A.redraw(); } });
      A.choice({ label: '符号 T<sub>s</sub>', options: TSL, value: tsI, on: function (i) { tsI = i; A.redraw(); } });
      return frame;
    }
  });

  /* ================= 2.6 LCR and AFD by counting ================= */
  ANIM.reg('p2:2.6', {
    title: '按定义数 LCR 和 AFD',
    cap: '看什么：1 秒的瑞利包络（f<sub>m</sub> = 20 Hz，以 Z<sub>rms</sub> 为 0 dB）和门限 ρ = Z<sub>min</sub>/Z<sub>rms</sub>。先数向下穿越的次数得 LCR，再把每次衰落的时长加起来求平均得 AFD。拖动 ρ 看数字怎么变。',
    h: 250,
    steps: [
      '包络 z(t) 和门限 Zmin（金虚线）。ρ = Zmin/Zrms，可以用滑块调。观察 T = 1 s。',
      '数“向下”穿过门限的次数（红点）。向上穿回不算，否则每次衰落数两遍。',
      'LCR = 向下穿越次数 ÷ 观察时间：每秒进入几次深衰落。',
      '每次衰落从向下穿到向上穿回的时长 τi（红色阴影），加起来 = 低于门限的总时间。',
      'AFD = Στi ÷ 衰落次数，像“算平均价格”。题目没说瑞利时就按这个定义算。',
      '只有瑞利衰落才能套公式 LZ = √(2π)·fm·ρ·e^(−ρ²)；1 秒的样本和公式有随机出入。'
    ],
    init: function (A) {
      var fm = 20, NS = 1200, z = [], i, seed, rho = 0.3;
      for (seed = 1; seed < 80; seed++) {
        var e = sos(A.rng(100 + seed), 16), s2 = 0;
        z = []; for (i = 0; i <= NS; i++) { z.push(e(i / NS, fm)); s2 += z[i] * z[i]; }
        var rm = Math.sqrt(s2 / (NS + 1)); z = z.map(function (v) { return v / rm; });
        if (z[0] > 0.7 && z[NS] > 0.7) break;
      }
      var ax = A.axes({ x: 42, y: 20, w: 344, h: 150, xr: [0, 1], yr: [-35, 8], ticksX: [0, 0.5, { v: 1, l: '1 s' }], ticksY: [{ v: 0, l: '0 dB' }, { v: -20, l: '−20' }], xAxisAt: 'bottom', yAxisAt: 'left' });
      var gB = A.g(), bands = [], dots = [];
      for (i = 0; i < 40; i++) bands.push(A.rect(0, 0, 0, 0, 'f-bad s-none op3', gB, 0));
      A.curve(ax, z.map(function (v, k) { return [k / NS, Math.max(-35, 20 * Math.log10(v + 1e-9))]; }), 's-acc w1');
      var thl = A.line(42, 0, 386, 0, 's-gold w2 dash'), tht = A.text(386, 0, '', { cls: 't-s t-b f-gold', anchor: 'end' });
      for (i = 0; i < 40; i++) dots.push(A.circle(0, 0, 3.6, 'f-bad s-card w1'));
      var L1 = A.text(12, 204, '', { cls: 't-b' }), L2 = A.text(12, 224, '', { cls: 't-b' }), L3 = A.text(12, 243, '', { cls: 't-s' });
      function cross(r) {
        var dn = [], fd = [], t0 = null;
        for (var k = 1; k <= NS; k++) {
          var a = z[k - 1], b = z[k], tc = (k - 1 + (a - r) / (a - b)) / NS;
          if (a >= r && b < r) { dn.push(tc); t0 = tc; }
          else if (a < r && b >= r && t0 != null) { fd.push([t0, tc]); t0 = null; }
        }
        return { dn: dn, fd: fd };
      }
      A.slider({ label: 'ρ = Z<sub>min</sub>/Z<sub>rms</sub>', min: 0.1, max: 0.6, step: 0.01, value: rho, fmt: function (v) { return v.toFixed(2) + '（' + (20 * Math.log10(v)).toFixed(1) + ' dB）'; }, on: function (v) { rho = v; A.redraw(); } });
      return {
        frame: function (ts, dt, k) {
          var c = cross(rho), yT = ax.Y(20 * Math.log10(rho)), Nc = c.dn.length, sum = 0, p = A.prog(ts, 1.0);
          A.set(thl, { y1: yT, y2: yT }); A.set(tht, { y: yT - 5, text: '门限 ρ = ' + rho.toFixed(2) + '（' + (20 * Math.log10(rho)).toFixed(1) + ' dB）' });
          c.fd.forEach(function (f) { sum += f[1] - f[0]; });
          for (var j = 0; j < 40; j++) {
            var on = j < Nc && k >= 1, f = c.fd[j];
            dots[j].style.display = on ? '' : 'none';
            if (on) A.set(dots[j], { cx: ax.X(c.dn[j]), cy: yT, opacity: k === 1 ? A.clamp(p * Nc - j, 0, 1) : 1 });
            var bo = f && k >= 3;
            bands[j].style.display = bo ? '' : 'none';
            if (bo) A.set(bands[j], { x: ax.X(f[0]), y: yT, width: ax.X(f[1]) - ax.X(f[0]), height: ax.Y(-35) - yT });
          }
          var lz = Math.sqrt(2 * Math.PI) * fm * rho * Math.exp(-rho * rho), afd = (Math.exp(rho * rho) - 1) / (Math.sqrt(2 * Math.PI) * fm * rho);
          A.setText(L1, k < 1 ? '' : '向下穿越 N = ' + Nc + ' 次' + (k >= 2 ? '　→　LCR = N / T = ' + Nc + ' 次/秒' : ''));
          A.setText(L2, k < 3 ? '' : 'Στ_{i} = ' + (sum * 1000).toFixed(1) + ' ms' + (k >= 4 && Nc ? '　→　AFD = Στ_{i} / N = ' + (sum / Nc * 1000).toFixed(2) + ' ms' : ''));
          A.setText(L3, k < 5 ? '' : '瑞利公式（f_{m} = 20 Hz）：L_{Z} = ' + lz.toFixed(1) + ' 次/秒，AFD = ' + (afd * 1000).toFixed(2) + ' ms');
          A.note(k < 5 ? '' : '检查：L<sub>Z</sub>·AFD = 1 − e<sup>−ρ²</sup> = ' + (1 - Math.exp(-rho * rho)).toFixed(4) + '（低于门限的时间比例）；本样本 Στ<sub>i</sub>/T = ' + sum.toFixed(4));
        }
      };
    }
  });

  /* ================= 2.7 Shannon capacity ================= */
  ANIM.reg('p2:2.7', {
    title: '香农容量 C = B log₂(1 + SNR)',
    cap: '看什么：曲线是每赫兹的容量 C/B，横轴是 SNR（dB），但公式里要代线性值。高 SNR 时每多 3 dB（SNR 翻倍）只多约 1 bit/s/Hz；带宽翻倍容量直接翻倍。两个按钮是 Practice 2 第 3 题。',
    h: 220,
    init: function (A) {
      var B = 20, sdb = 20, lin = 100;
      var ax = A.axes({ x: 40, y: 22, w: 344, h: 118, xr: [-10, 40], yr: [0, 14.5], ticksX: [-10, 0, 10, 20, 30, { v: 40, l: '40 dB' }], ticksY: [5, 10], grid: true, xAxisAt: 'bottom', yAxisAt: 'left', yl: 'C/B (bit/s/Hz)' });
      function se(db) { return Math.log2(1 + A.undb(db)); }
      A.curve(ax, se, 's-acc w2', null, 200);
      [10 / 10.1, 100].forEach(function (g) { A.circle(ax.X(A.db(g)), ax.Y(Math.log2(1 + g)), 6.5, 'f-none s-pur w2'); });
      var st = A.path('', 's-gold w2'), stt = A.text(0, 0, '', { cls: 't-s t-b f-gold', anchor: 'end' });
      var gl = A.path('', 's-ink w1 dash'), dot = A.circle(0, 0, 5.5, 'f-gold s-card w1');
      var pt = A.text(0, 0, '', { cls: 't-s t-b', anchor: 'end' });
      var CMAX = 600, x0 = 40, w = 344;
      A.text(40, 168, '容量 C（Mbps）', { cls: 't-s' });
      A.rect(x0, 174, w, 14, 'f-card s-line w1', null, 3);
      var bar = A.rect(x0, 174, 0, 14, 'f-acc s-none', null, 3);
      [0, 200, 400, 600].forEach(function (v) { A.text(x0 + v / CMAX * w, 200, String(v), { cls: 't-s', anchor: 'middle' }); });
      var ct = A.text(200, 216, '', { cls: 't-b', anchor: 'middle' });
      function draw() {
        var c = Math.log2(1 + lin), db = A.db(lin), X = ax.X(db), Y = ax.Y(c);
        A.set(dot, { cx: X, cy: Y }); A.set(gl, { d: 'M' + X + ' ' + ax.Y(0) + 'V' + Y + 'H' + ax.X(-10) });
        A.set(pt, { x: X < 170 ? X + 9 : X - 9, y: Y - 10, 'text-anchor': X < 170 ? 'start' : 'end', text: 'γ = ' + A.fmt(lin, 3) + ' → ' + c.toFixed(2) });
        var show = db >= 10 && db <= 37;
        st.style.display = stt.style.display = show ? '' : 'none';
        if (show) {
          var c2 = Math.log2(1 + A.undb(db + 3));
          A.set(st, { d: 'M' + X + ' ' + Y + 'H' + ax.X(db + 3) + 'V' + ax.Y(c2) });
          A.set(stt, { x: X - 9, y: Y - 24, text: '+3 dB → +' + (c2 - c).toFixed(2) });
        }
        var C = B * c;
        A.set(bar, { width: Math.min(w, C / CMAX * w) });
        A.setText(ct, 'C = ' + B + ' MHz × log₂(1 + ' + A.fmt(lin, 4) + ') = ' + C.toFixed(2) + ' Mbps');
      }
      var sB = A.slider({ label: '带宽 B', min: 1, max: 40, step: 1, value: B, unit: 'MHz', on: function (v) { B = v; draw(); } });
      var sS = A.slider({ label: 'SNR', min: -10, max: 40, step: 0.01, value: sdb, fmt: function (v) { return v.toFixed(2) + ' dB = ' + A.fmt(A.undb(v), 3); }, on: function (v) { sdb = v; lin = A.undb(v); draw(); } });
      A.button('例 (a) SINR = 10/10.1', function () { sB.set(20); sS.set(A.db(10 / 10.1)); lin = 10 / 10.1; draw(); });
      A.button('例 (b) SNR = 10/0.1', function () { sB.set(20); sS.set(20); lin = 100; draw(); });
      draw();
      return {};
    }
  });

  /* ================= 2.8 water-filling ================= */
  ANIM.reg('p2:2.8', {
    title: '注水：往高低不平的池子里倒功率',
    cap: '看什么：每格池底高度 = 1/γ<sub>j</sub>（信道越好池底越低），水面 = 1/γ₀，每格的水深 = 分到的功率 P<sub>j</sub>/P，总水量 = 1。数字是第 2 章 p.56–57 例题：γ = 17.77、2.63、0.087。纵轴 1 以上压缩画。',
    h: 278,
    tween: 2.2,
    steps: [
      '三个子信道：池底高 = 1/γj，信道越好池底越低。总功率 P 当成一桶水（总量 = 1）。',
      '先假设三个都分：3/γ₀ = 1 + Σ1/γj ≈ 12.93 → γ₀ ≈ 0.23，水位 1/γ₀ ≈ 4.31。',
      '可池 3 的底 11.49 高过水位：P₃ = 4.31 − 11.49 &lt; 0，功率不能为负 → 去掉池 3。',
      '只给前两个倒水：2/γ₀ = 1 + 1/17.77 + 1/2.63 ≈ 1.437 → γ₀ ≈ 1.39。',
      '功率 = 水位 − 池底：P₁ ≈ 0.66P，P₂ ≈ 0.34P，P₃ = 0，加起来 = P ✓。',
      '容量 C = Σ log₂(γj/γ₀) ≈ 3.67 + 0.92 = 4.59 bit/s/Hz，只对分到功率的求和'
    ],
    init: function (A) {
      var G = [17.77, 2.63, 0.087], fl = G.map(function (g) { return 1 / g; }), i;
      var s3 = 1, s2 = 1; for (i = 0; i < 3; i++) { s3 += fl[i]; if (i < 2) s2 += fl[i]; }
      var L3 = s3 / 3, L2 = s2 / 2, g0 = 1 / L2;
      var BOT = 232, MID = 104, TOP = 30;
      function Y(v) { return v <= 1 ? BOT - v * (BOT - MID) : MID - (MID - TOP) * Math.log(v) / Math.log(12); }
      var vx = [50, 136, 222], vw = 72;
      A.line(40, BOT, 40, TOP - 4, 's-soft w1');
      [[0, '0'], [0.5, '0.5'], [1, '1'], [4, '4'], [12, '12']].forEach(function (t) { A.line(37, Y(t[0]), 43, Y(t[0]), 's-soft w1'); A.text(34, Y(t[0]) + 4, t[1], { cls: 't-s', anchor: 'end' }); });
      A.path('M35 ' + (MID - 7) + 'l10 -4M35 ' + (MID - 2) + 'l10 -4', 's-soft w1');
      var water = [], neg, lbl = [], cross;
      for (i = 0; i < 3; i++) {
        var x = vx[i];
        A.rect(x, Y(fl[i]), vw, BOT - Y(fl[i]), 'f-line s-soft w1', null, 0);
        water.push(A.rect(x + 1, BOT, vw - 2, 0, 'f-acc s-none op3', null, 0));
        A.line(x, TOP, x, BOT, 's-ink w2'); A.line(x + vw, TOP, x + vw, BOT, 's-ink w2'); A.line(x, BOT, x + vw, BOT, 's-ink w2');
        A.text(x + vw / 2, 252, 'γ_{' + (i + 1) + '} = ' + G[i], { cls: 't-s t-b', anchor: 'middle' });
        A.text(x + vw / 2, 270, '底 1/γ = ' + fl[i].toFixed(fl[i] < 1 ? 3 : 2), { cls: 't-s', anchor: 'middle' });
        lbl.push(A.text(x + vw / 2, 0, '', { cls: 't-s t-b f-acc', anchor: 'middle' }));
      }
      neg = A.rect(vx[2] + 6, 0, vw - 12, 0, 'f-bads s-bad w1 dash', null, 0);
      cross = A.path('M' + (vx[2] + 14) + ' 112l46 46M' + (vx[2] + 60) + ' 112l-46 46', 's-bad w4');
      var lev = A.line(44, 0, 396, 0, 's-acc w2 dash'), levT = A.text(396, 0, '', { cls: 't-s t-b f-acc', anchor: 'end' });
      var capT = A.text(220, 16, '', { cls: 't-b', anchor: 'middle' });
      var cur = 0;
      function level(ts, k) {
        if (k === 0) return null;
        if (k === 1) return A.lerp(fl[0], L3, A.prog(ts, 1.4));
        if (k === 2) return L3;
        if (k === 3) return A.lerp(fl[0], L2, A.prog(ts, 1.8, 0.2));
        return L2;
      }
      return {
        step: function (k) { cur = k; },
        frame: function (ts, dt, k) {
          var L = level(ts, k), act = k <= 2 ? 3 : 2;
          lev.style.display = levT.style.display = L == null ? 'none' : '';
          if (L != null) { A.set(lev, { y1: Y(L), y2: Y(L) }); A.set(levT, { y: Y(L) - 5, text: '水位 1/γ₀ = ' + L.toFixed(L > 1 ? 2 : 3) }); }
          for (var j = 0; j < 3; j++) {
            var on = L != null && j < act && L > fl[j];
            var top = on ? Y(L) : BOT, bt = Y(fl[j]);
            A.set(water[j], { y: top, height: on ? Math.max(0, bt - top) : 0 });
            var showP = k >= 4 && j < 2;
            lbl[j].style.display = showP ? '' : 'none';
            if (showP) A.set(lbl[j], { y: Math.max(Y(L), 40) - 6, text: 'P_{' + (j + 1) + '} = ' + (L - fl[j]).toFixed(2) + 'P' });
          }
          var ng = (k === 1 || k === 2) && L > fl[0];
          neg.style.display = ng && L < fl[2] ? '' : 'none';
          if (ng) A.set(neg, { y: Y(fl[2]), height: Math.max(0, Y(L) - Y(fl[2])) });
          cross.style.display = k >= 2 ? '' : 'none';
          cross.setAttribute('opacity', k === 2 ? A.prog(ts, 0.6, 0.4).toFixed(2) : '1');
          var c1 = Math.log2(G[0] * L2), c2 = Math.log2(G[1] * L2);
          A.setText(capT, k === 1 ? '3 个都分：γ₀ = ' + (1 / L3).toFixed(3) : k === 2 ? 'P₃ = ' + L3.toFixed(2) + ' − ' + fl[2].toFixed(2) + ' = ' + (L3 - fl[2]).toFixed(2) + ' < 0 ✗'
            : k === 3 ? '只用 2 个：γ₀ = ' + g0.toFixed(3) : k === 4 ? 'P₁ + P₂ = ' + (L2 - fl[0]).toFixed(3) + ' + ' + (L2 - fl[1]).toFixed(3) + ' = ' + (2 * L2 - fl[0] - fl[1]).toFixed(3) + ' P'
              : k === 5 ? 'C = ' + c1.toFixed(2) + ' + ' + c2.toFixed(2) + ' = ' + (c1 + c2).toFixed(2) + ' bit/s/Hz' : '');
          void cur;
        }
      };
    }
  });
})();
