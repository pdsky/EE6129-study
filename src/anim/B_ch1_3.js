/* EE6129 Part B 第 1–3 章（WLAN / IEEE 802.11）动画：B:1.1 … B:3.5 */
(function () {
  'use strict';
  var R = ANIM.reg;

  /* ---------- shared helpers ---------- */
  function op(el, v) { el.setAttribute('opacity', (+v).toFixed(2)); }
  function shown(el, on) { el.setAttribute('display', on ? 'inline' : 'none'); }
  // fade-in for steps mode: 0 before step s, eased in at step s, 1 after; 0 again from step e (optional)
  function fin(A, k, ts, s, e, dur) { if (e != null && k >= e) return 0; return k > s ? 1 : k === s ? A.prog(ts, dur || 0.7) : 0; }
  function tw(s, px) { var w = 0; for (var i = 0; i < s.length; i++) w += /[⺀-￿]/.test(s[i]) ? px : px * 0.58; return w; }
  function laptop(A, x, y, lab, p) {
    var g = A.g({}, p);
    g.scr = A.rect(x - 9, y - 9, 18, 12, 'f-card s-ink w1', g, 1.5);
    A.line(x - 12, y + 5, x + 12, y + 5, 's-ink w2', g);
    if (lab) A.text(x, y + 18, lab, { cls: 't-s', anchor: 'middle' }, g);
    return g;
  }
  function apIcon(A, x, y, lab, p) {
    var g = A.g({}, p);
    A.line(x - 7, y - 7, x - 10, y - 16, 's-ink w2', g);
    A.line(x + 7, y - 7, x + 10, y - 16, 's-ink w2', g);
    g.box = A.rect(x - 15, y - 8, 30, 16, 'f-accs s-acc w2', g, 3);
    A.text(x, y + 4, lab || 'AP', { cls: 't-s t-b', anchor: 'middle' }, g);
    return g;
  }
  function star(A, cx, cy, r1, r2, n, cls, p) {
    var pts = [];
    for (var i = 0; i < 2 * n; i++) { var a = Math.PI * i / n, r = i % 2 ? r2 : r1; pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
    return A.poly(pts, cls || 'f-bads s-bad w2', p);
  }
  /* time-line boxes revealed by a cursor (time units); cur = number or function(item) → number */
  function Boxes(A, X, parent) {
    var L = [];
    function add(y, a, b, lab, cls, o) {
      o = o || {};
      var g = A.g({}, parent), h = o.h || 17, it = { a: a, b: b, g: g, o: o };
      it.r = A.rect(X(a), y - h / 2, Math.max(0, X(b) - X(a)), h, cls, g, 2);
      if (lab) it.t = A.text((X(a) + X(b)) / 2, y + 3.8, lab, { cls: o.tc || 't-s', anchor: 'middle' }, g);
      L.push(it); return it;
    }
    function txt(x, y, s, cls, at, o) {
      o = o || {};
      var g = A.g({}, parent), it = { a: at, b: at, g: g, o: o, txt: true };
      it.t = A.text(x, y, s, { cls: cls || 't-s', anchor: o.anchor || 'middle' }, g);
      L.push(it); return it;
    }
    function show(cur, k) {
      L.forEach(function (it) {
        var c = typeof cur === 'function' ? cur(it) : cur, o = it.o;
        var on = !(o.ms != null && k < o.ms) && !(o.vis && !o.vis(k)) && (it.txt ? c >= it.a : c > it.a);
        shown(it.g, on);
        if (!on || it.txt) return;
        A.set(it.r, { width: Math.max(0, X(Math.min(c, it.b)) - X(it.a)) });
        if (it.t) op(it.t, c >= it.a + (it.b - it.a) * 0.7 ? 1 : 0);
      });
    }
    return { add: add, txt: txt, show: show, list: L };
  }
  // per-step cursor: item with o.s < k → full, > k → hidden, == k → current cursor
  function stepCur(k, cur) { return function (it) { var s = it.o.s; return s == null ? cur : s < k ? Infinity : s > k ? -Infinity : cur; }; }

  /* ================= 1.1 WLAN 的基本样子 ================= */
  ANIM.reg('B:1.1', {
    title: '一个小区只有一个信道',
    cap: '三个小区各用一个频率：中间的控制模块 CM（作用相当于 AP）接到 100 Mbps 以太网交换机，周围是用户模块 UM。<b>同一小区里上行、下行共用一个频率</b>，所以每个小区里同一时刻只有一个小点在跑；相邻小区频率不同，可以同时传。',
    h: 250,
    init: function (A) {
      var cx = [72, 200, 328], cy = 165, r = 58, col = ['acc', 'gold', 'good'], ang = [-160, -20, 90], cells = [];
      A.rect(128, 8, 144, 22, 'f-card s-ink w1', null, 4);
      A.text(200, 23, '100 Mbps 以太网交换机', { cls: 't-s', anchor: 'middle' });
      A.text(6, 18, '覆盖 50–500 m', 't-s'); A.text(6, 33, '速率 1–54 Mbps', 't-s');
      A.text(394, 18, 'CM 控制模块', { cls: 't-s', anchor: 'end' }); A.text(394, 33, 'UM 用户模块', { cls: 't-s', anchor: 'end' });
      for (var i = 0; i < 3; i++) {
        A.circle(cx[i], cy, r, 'f-' + col[i] + 's s-' + col[i] + ' w1');
        A.text(cx[i], cy + r + 15, '频率 ' + (i + 1), { cls: 't-b f-' + col[i], anchor: 'middle' });
      }
      for (i = 0; i < 3; i++) A.path('M' + (200 + (i - 1) * 40) + ' 30V52H' + cx[i] + 'V' + (cy - 10), 's-soft w2');
      for (i = 0; i < 3; i++) {
        var C = { um: [], scr: [] };
        apIcon(A, cx[i], cy, 'CM');
        ang.forEach(function (a) {
          var p = [cx[i] + 38 * Math.cos(a * Math.PI / 180), cy + 38 * Math.sin(a * Math.PI / 180)];
          C.um.push([p[0], p[1] - 4]); C.scr.push(laptop(A, p[0], p[1]).scr);
        });
        C.dot = A.circle(cx[i], cy, 4.5, 'f-' + col[i]);
        cells.push(C);
      }
      return function (t) {
        for (var i = 0; i < 3; i++) {
          var T = t + i * 0.55, P = 1.3, n = Math.floor(T / P), ph = T / P - n;
          var j = n % 3, up = (Math.floor(n / 3) + j) % 2 === 0, C = cells[i], u = C.um[j];
          var p = A.clamp((ph - 0.08) / 0.7, 0, 1), a = up ? u : [cx[i], cy], b = up ? [cx[i], cy] : u;
          A.set(C.dot, { cx: A.lerp(a[0], b[0], p), cy: A.lerp(a[1], b[1], p) });
          op(C.dot, ph < 0.08 || ph > 0.85 ? 0 : 1);
          for (var q = 0; q < 3; q++) C.scr[q].setAttribute('class', q === j ? 'f-card s-' + col[i] + ' w3' : 'f-card s-ink w1');
        }
      };
    }
  });

  /* ================= 1.2 架构 ================= */
  ANIM.reg('B:1.2', {
    title: 'BSS、AP、DS、ESS 怎么拼起来',
    cap: '按“下一步”一层层搭：站点 → BSS → AP → 分布系统 DS → ESS，最后对比没有 AP 的 Ad Hoc 模式。',
    h: 262,
    steps: [
      '一群竞争同一个无线信道的站点 STA 叫一个 BSS（基本服务集），也就是“一个小区”。',
      '每个 BSS 有一个 AP：相当于网桥，负责 BSS 和外界的连接，并提供中心协调。',
      '把多个 AP 连起来的交换机、有线或无线网络，叫分布系统 DS。',
      '两个以上 BSS 经 DS 互联 = ESS（扩展服务集）；DS 再经门户 portal 接到其他 802.x 局域网。',
      'STA4 从 BSS 1 走到 BSS 2：两个 BSS 属于同一个 ESS，对外看还是同一个网络。',
      '对比 Ad Hoc 模式：没有 AP，终端直接互连，临时组成对等网络。'
    ],
    init: function (A) {
      var inf = A.g(), adh = A.g();
      var gEss = A.g({}, inf), gBss = A.g({}, inf), gDS = A.g({}, inf), gPor = A.g({}, inf), gLink = A.g({}, inf), gAP = A.g({}, inf), gSta = A.g({}, inf);
      A.rect(8, 40, 384, 220, 'f-none s-pur w2 dash', gEss, 10);
      A.text(16, 78, 'ESS 扩展服务集', { cls: 't-b f-pur' }, gEss);
      [[110, 'acc', 'BSS 1'], [290, 'gold', 'BSS 2']].forEach(function (b) {
        A.el('ellipse', { cx: b[0], cy: 160, rx: 88, ry: 78, cls: 'f-' + b[1] + 's s-' + b[1] + ' w1' }, gBss);
        A.text(b[0], 252, b[2], { cls: 't-b f-' + b[1], anchor: 'middle' }, gBss);
      });
      A.rect(40, 46, 320, 14, 'f-purs s-pur w1', gDS, 4);
      A.text(200, 57, '分布系统 DS', { cls: 't-s', anchor: 'middle' }, gDS);
      A.line(110, 60, 110, 84, 's-pur w2', gDS); A.line(290, 60, 290, 84, 's-pur w2', gDS);
      A.line(200, 28, 200, 46, 's-pur w2', gPor);
      A.rect(150, 6, 100, 22, 'f-card s-pur w1', gPor, 4);
      A.text(200, 21, '门户 portal', { cls: 't-s', anchor: 'middle' }, gPor);
      A.text(256, 21, '→ 其他 802.x LAN', 't-s', gPor);
      apIcon(A, 110, 92, 'AP1', gAP); apIcon(A, 290, 92, 'AP2', gAP);
      var S = [[55, 140, 0], [160, 140, 0], [65, 198, 0], [150, 198, 0], [240, 140, 1], [340, 140, 1], [290, 198, 1]];
      var l4, sta4;
      S.forEach(function (s, i) {
        var l = A.line(s[0], s[1] - 9, s[2] ? 290 : 110, 100, 's-acc w1 dash op7', gLink);
        var g = laptop(A, s[0], s[1], 'STA' + (i + 1), gSta);
        if (i === 3) { l4 = l; sta4 = g; }
      });
      A.text(200, 34, 'Ad Hoc：没有 AP，终端直接互连', { cls: 't-b', anchor: 'middle' }, adh);
      var Q = [[140, 110], [260, 110], [150, 190], [250, 190]];
      Q.forEach(function (a, i) { Q.forEach(function (b, j) { if (j > i) A.line(a[0], a[1], b[0], b[1], 's-acc w1 dash', adh); }); });
      Q.forEach(function (a, i) { laptop(A, a[0], a[1], 'STA' + (i + 1), adh); });
      return {
        frame: function (ts, dt, k) {
          op(gBss, fin(A, k, ts, 0, 5)); op(gSta, fin(A, k, ts, 0, 5));
          op(gAP, fin(A, k, ts, 1, 5)); op(gLink, fin(A, k, ts, 1, 5));
          op(gDS, fin(A, k, ts, 2, 5));
          op(gEss, fin(A, k, ts, 3, 5)); op(gPor, fin(A, k, ts, 3, 5));
          op(adh, k === 5 ? A.prog(ts, 0.7) : 0);
          var p = k < 4 ? 0 : k === 4 ? A.prog(ts, 1.4) : 1, x = A.lerp(150, 240, p);
          sta4.setAttribute('transform', 'translate(' + (x - 150).toFixed(2) + ' 0)');
          A.set(l4, { x1: x, x2: p < 0.5 ? 110 : 290 });
        }
      };
    }
  });

  /* ================= 1.3 物理层与 802.11 家族 ================= */
  ANIM.reg('B:1.3', {
    title: '802.11 家族：频段、技术、速率',
    cap: '横轴是速率（对数刻度）；下面两个框是频段，宽度按真实带宽比例画。老师要记的两个：<b>b = 2.4 GHz + DSSS</b>，<b>a = 5 GHz + OFDM</b>。',
    h: 290,
    steps: [
      '1997 年的 802.11：三种物理层 FHSS、DSSS、红外 IR，速率都只有 1、2 Mbps。',
      '802.11b：还在 2.4 GHz，DSSS 加上 CCK 码，速率提到 5.5、11 Mbps。',
      '802.11a：换到 5 GHz，用 OFDM（Part 2 的多载波），速率 6–54 Mbps。',
      '要记：b = 2.4 GHz + DSSS；a = 5 GHz + OFDM。a 频率高 → 损耗大、覆盖小。',
      '其他字母：d 漫游、e QoS、g 最高 54 Mbps、h DFS/TPC、i 安全、j 日本、k 测量。'
    ],
    init: function (A) {
      var LG = Math.log10, X = function (r) { return 130 + LG(r) / LG(60) * 252; };
      var rows = [
        { n: '802.11 FHSS', s: '2.4 GHz 跳频', r: [1, 2], c: 'soft' },
        { n: '802.11 DSSS', s: '2.4 GHz 直接序列', r: [1, 2], c: 'soft' },
        { n: '802.11 IR', s: '红外 850–950 nm', r: [1, 2], c: 'soft' },
        { n: '802.11b', s: '2.4 GHz DSSS+CCK', r: [5.5, 11], c: 'gold' },
        { n: '802.11a', s: '5 GHz OFDM', r: [6, 54], c: 'acc', bar: true }
      ];
      var hl = rows.map(function (rw, i) { return A.rect(2, 30 + 32 * i - 16, 396, 31, 'f-accs s-none', null, 6); });
      [1, 2, 5.5, 11, 54].forEach(function (v) {
        A.line(X(v), 16, X(v), 178, 's-line w1 dash op5');
        A.text(X(v), 194, String(v), { cls: 't-s', anchor: 'middle' });
      });
      A.line(126, 180, 388, 180, 's-soft w1');
      A.text(8, 194, '速率 Mbps', 't-s');
      var rg = rows.map(function (rw, i) {
        var y = 30 + 32 * i, g = A.g();
        A.text(8, y - 3, rw.n, 't-b', g); A.text(8, y + 12, rw.s, 't-s', g);
        if (rw.bar) {
          A.rect(X(rw.r[0]), y - 3, X(rw.r[1]) - X(rw.r[0]), 10, 'f-' + rw.c + ' s-none', g, 5);
          A.text((X(rw.r[0]) + X(rw.r[1])) / 2, y - 7, rw.r[0] + '–' + rw.r[1], { cls: 't-s t-b', anchor: 'middle' }, g);
        } else rw.r.forEach(function (v) {
          A.circle(X(v), y + 2, 5, 'f-' + rw.c, g);
          A.text(X(v), y - 7, String(v), { cls: 't-s', anchor: 'middle' }, g);
        });
        return g;
      });
      A.text(8, 226, '频段', 't-b');
      var bands = [[2.400, 2.4835, 130, 'gold', '2.4 GHz', '2.400–2.4835'], [5.725, 5.850, 252, 'acc', '5 GHz', '5.725–5.850']].map(function (b) {
        var g = A.g(), w = Math.round((b[1] - b[0]) * 10000) / 10;   // MHz, 1 px per MHz
        A.rect(b[2], 212, w, 20, 'f-' + b[3] + 's s-' + b[3] + ' w1', g, 3);
        A.text(b[2] + w / 2, 226, b[5], { cls: 't-s', anchor: 'middle' }, g);
        A.text(b[2] + w / 2, 247, b[4] + ' · 宽 ' + w + ' MHz', { cls: 't-s', anchor: 'middle' }, g);
        return g;
      });
      var chips = A.g(), cx = 8;
      ['d 漫游', 'e QoS', 'g 最高 54M', 'h DFS/TPC', 'i 安全', 'j 日本', 'k 测量'].forEach(function (s) {
        var w = tw(s, 10.5) + 10;
        A.rect(cx, 262, w, 20, 'f-purs s-pur w1', chips, 10);
        A.text(cx + w / 2, 276, s, { cls: 't-s', anchor: 'middle' }, chips);
        cx += w + 4;
      });
      var HL = [[0, 1, 2], [3], [4], [3, 4], []], VIS = [2, 3, 4, 4, 4];
      return {
        frame: function (ts, dt, k) {
          var p = A.prog(ts, 0.7);
          rg.forEach(function (g, i) { var s = i <= 2 ? 0 : i - 2; op(g, i <= VIS[k] ? (s === k ? p : 1) : 0.12); });
          hl.forEach(function (h, i) { op(h, HL[k].indexOf(i) >= 0 ? p : 0); });
          op(bands[0], k === 2 ? 0.35 : 1);
          op(bands[1], k < 2 ? 0.12 : k === 2 ? 0.12 + 0.88 * p : 1);
          op(chips, k === 4 ? p : 0);
        }
      };
    }
  });

  /* ================= 2.1 两帧 / 四帧交换 ================= */
  ANIM.reg('B:2.1', {
    title: '两帧交换与四帧交换',
    cap: '横轴是时间。上：DATA → ACK；下：RTS → CTS → DATA → ACK。紫色虚线框是邻站的 NAV：计时器归零前不发送。',
    h: 222,
    tween: 2.1,
    steps: [
      '两帧交换：源站先发 DATA。',
      '目的站检查 FCS（CRC）没错，隔一个 SIFS 回 ACK，这次传输成功。',
      'DATA 出错或丢了 → 目的站不回 ACK → 源站等不到 ACK，就重传。',
      '四帧交换：RTS（请求发送）→ CTS（允许发送）→ DATA → ACK，帧间只隔 SIFS。',
      'RTS、CTS 里写着后面还要占用多久。邻站 C 听到 RTS，按这个时长设 NAV，不发送。',
      '邻站 D 听不到源站的 RTS，但听得到目的站的 CTS，照样设 NAV 让路。'
    ],
    init: function (A) {
      var X = function (u) { return u; };
      A.text(8, 16, '两帧交换', 't-b'); A.text(8, 102, '四帧交换（RTS/CTS）', 't-b');
      [['源站', 34], ['目的站', 58], ['源站', 128], ['目的站', 152], ['邻站 C', 180], ['邻站 D', 206]].forEach(function (r) {
        A.text(8, r[1] + 4, r[0], 't-s'); A.line(68, r[1], 392, r[1], 's-line w1');
      });
      var B = Boxes(A, X), ok = function (k) { return k !== 2; }, bad = function (k) { return k === 2; };
      var D = 'f-accs s-acc w1', K = 'f-goods s-good w1', G = 'f-golds s-gold w1', N = 'f-purs s-pur w1 dash';
      B.add(34, 80, 150, 'DATA', D, { s: 0, vis: ok });
      B.add(58, 164, 190, 'ACK', K, { s: 1, vis: ok });
      B.txt(157, 79, 'SIFS', 't-s', 152, { s: 1, vis: ok });
      B.txt(198, 55, '✓ 成功', 't-s t-b f-good', 190, { s: 1, vis: ok, anchor: 'start' });
      B.add(34, 80, 150, 'DATA', D, { s: 2, vis: bad });
      B.txt(115, 54, '✗ FCS 出错', 't-s t-b f-bad', 150, { s: 2, vis: bad });
      B.add(34, 150, 214, '超时', 'f-none s-bad w1 dash', { s: 2, vis: bad });
      B.add(34, 220, 290, '重传 DATA', D, { s: 2, vis: bad });
      B.add(58, 304, 330, 'ACK', K, { s: 2, vis: bad });
      B.txt(297, 79, 'SIFS', 't-s', 292, { s: 2, vis: bad });
      var F = [[128, 80, 110, 'RTS', G], [152, 124, 154, 'CTS', G], [128, 168, 238, 'DATA', D], [152, 252, 282, 'ACK', K]];
      F.forEach(function (f, i) {
        B.add(f[0], f[1], f[2], f[3], f[4], { s: 3 });
        if (i) B.txt((F[i - 1][2] + f[1]) / 2, 117, 'SIFS', 't-s', F[i - 1][2] + 2, { s: 3 });
      });
      B.add(180, 110, 282, 'NAV（听到 RTS）', N, { s: 4 });
      B.add(206, 154, 282, 'NAV（只听到 CTS）', N, { s: 5 });
      var CUR = [[80, 150], [150, 190], [80, 330], [80, 282], [110, 282], [154, 282]];
      return {
        frame: function (ts, dt, k) {
          var c = A.lerp(CUR[k][0], CUR[k][1], A.prog(ts, 1.9));
          B.show(stepCur(k, c), k);
        }
      };
    }
  });

  /* ================= 2.2 DCF vs PCF ================= */
  ANIM.reg('B:2.2', {
    title: 'DCF 抢 vs PCF 点名',
    cap: '左边 DCF：各站自己用 CSMA/CA 竞争，两个站同时发就会冲突。右边 PCF：AP 逐个轮询，被点到才发，不会冲突。PCF 是可选的，叠在 DCF 之上、和它共存。',
    h: 248,
    init: function (A) {
      A.line(200, 6, 200, 200, 's-line w1');
      A.text(100, 18, 'DCF：大家抢（CSMA/CA）', { cls: 't-b f-acc', anchor: 'middle' });
      A.text(300, 18, 'PCF：AP 逐个点名', { cls: 't-b f-gold', anchor: 'middle' });
      var P = [[30, 140], [76, 160], [124, 160], [170, 140]];
      function side(ox) {
        var s = { st: [] };
        apIcon(A, ox + 100, 56, 'AP');
        P.forEach(function (p) { A.line(ox + p[0], p[1] - 12, ox + 100, 66, 's-line w1 dash'); });
        P.forEach(function (p, i) { s.st.push(laptop(A, ox + p[0], p[1], 'STA' + (i + 1)).scr); });
        s.msg = A.text(ox + 100, 196, '', { cls: 't-s', anchor: 'middle' });
        return s;
      }
      var L = side(0), Rt = side(200);
      var dots = P.map(function () { return A.circle(0, 0, 4.5, 'f-acc'); });
      var st = star(A, 100, 62, 17, 8, 8);
      var pd = A.circle(0, 0, 4.5, 'f-gold'), rd = A.circle(0, 0, 4.5, 'f-acc');
      A.rect(10, 204, 380, 18, 'f-golds s-gold w1', null, 4);
      A.text(200, 217, 'PCF 点协调（可选，建在 DCF 之上）：AP 轮询 · 无冲突 · 适合语音', { cls: 't-s', anchor: 'middle' });
      A.rect(10, 226, 380, 18, 'f-accs s-acc w1', null, 4);
      A.text(200, 239, 'DCF 分布式协调（必须的基本方案）：CSMA/CA 竞争 · 适合突发数据', { cls: 't-s', anchor: 'middle' });
      var EV = [{ t: 0.2, s: [0], m: 'STA1 侦听到空闲 → 发送' }, { t: 1.8, s: [2], m: 'STA3 抢到信道 → 发送' },
        { t: 3.4, s: [1, 3], m: 'STA2、STA4 同时发 → 冲突！', bad: true },
        { t: 5.3, s: [1], m: 'STA2 随机退避后重发' }, { t: 6.7, s: [3], m: 'STA4 退避更久，后发' }];
      return function (t) {
        var tc = t % 8, msg = '侦听信道，空闲才发…', isBad = false, act = [];
        dots.forEach(function (d) { op(d, 0); }); op(st, 0);
        EV.forEach(function (e) {
          var u = tc - e.t;
          if (u < 0 || u > 1.5) return;
          msg = e.m; isBad = !!e.bad;
          e.s.forEach(function (i) {
            var p = A.clamp(u / 0.8, 0, 1);
            A.set(dots[i], { cx: A.lerp(P[i][0], 100, p), cy: A.lerp(P[i][1] - 12, 66, p) });
            op(dots[i], u < 0.9 ? 1 : 0); act.push(i);
          });
          if (e.bad && u > 0.75) op(st, 1);
        });
        A.setText(L.msg, msg); L.msg.setAttribute('class', isBad ? 't-s t-b f-bad' : 't-s');
        L.st.forEach(function (s, i) { s.setAttribute('class', act.indexOf(i) >= 0 ? 'f-card s-acc w3' : 'f-card s-ink w1'); });
        var i = Math.floor(tc / 2), u = tc - 2 * i, none = i === 2;
        var p1 = A.clamp((u - 0.1) / 0.7, 0, 1), p2 = A.clamp((u - 0.95) / 0.7, 0, 1);
        var sx = 200 + P[i][0], sy = P[i][1] - 12;
        A.set(pd, { cx: A.lerp(300, sx, p1), cy: A.lerp(66, sy, p1) }); op(pd, u > 0.1 && u < 0.85 ? 1 : 0);
        A.set(rd, { cx: A.lerp(sx, 300, p2), cy: A.lerp(sy, 66, p2), cls: none ? 'f-soft' : 'f-acc' }); op(rd, u > 0.95 && u < 1.7 ? 1 : 0);
        A.setText(Rt.msg, u < 0.9 ? 'AP → STA' + (i + 1) + '：CF-Poll' : none ? 'STA3 没数据，只回 CF-ACK' : 'STA' + (i + 1) + ' → AP：数据 + CF-ACK');
        Rt.st.forEach(function (s, j) { s.setAttribute('class', j === i ? 'f-card s-gold w3' : 'f-card s-ink w1'); });
      };
    }
  });

  /* ================= 2.3 IFS ================= */
  ANIM.reg('B:2.3', {
    title: '帧间间隔：等得越短越先发',
    cap: '信道一空（竖虚线），三类帧各等自己的 IFS。条越短越先等完；先等完的一发，其他人就听到信道又忙了，只能推迟。',
    h: 222,
    tween: 2.3,
    steps: [
      '信道刚空下来。三类帧都不能马上发，各自要先等一段帧间间隔 IFS。',
      '三类都在等：SIFS 最短，ACK/CTS 先发；其余站听到信道又忙了，只能推迟。',
      '没有 ACK 要回时：AP 等完 PIFS 就发轮询，抢在普通数据之前。',
      '只有普通数据：要等满最长的 DIFS（之后按 DCF 还要随机退避，见 2.4）。',
      '结论：SIFS < PIFS < DIFS。优先级：ACK > 有时限分组（PCF）> 无时限数据。'
    ],
    init: function (A) {
      var X0 = 120, LN = [30, 50, 70], FR = [36, 52, 50], NM = ['SIFS', 'PIFS', 'DIFS'], FN = ['ACK', 'CF-Poll', 'DATA'];
      var CL = ['good', 'gold', 'acc'], Y = [92, 132, 172], LB = ['要回 ACK/CTS 的站', 'AP（PCF 轮询）', '普通数据站'];
      A.text(8, 44, '信道上', 't-s');
      A.rect(50, 31, X0 - 50, 18, 'f-line s-soft w1', null, 2);
      A.text(85, 44, '上一帧', { cls: 't-s', anchor: 'middle' });
      A.line(X0, 26, X0, 184, 's-faint w1 dash');
      A.text(X0 + 4, 20, '信道变空闲', 't-s');
      var rows = Y.map(function (y, i) {
        var o = { g: A.g() };
        A.text(8, y + 4, LB[i], 't-s', o.g);
        o.bar = A.rect(X0, y - 9, 0, 18, 'f-' + CL[i] + 's s-' + CL[i] + ' w1', o.g, 2);
        o.bt = A.text(X0 + LN[i] / 2, y + 4, NM[i], { cls: 't-s t-b', anchor: 'middle' }, o.g);
        o.st = A.text(0, y + 4, '', 't-s f-bad', o.g);
        o.fr = A.rect(0, 31, 0, 18, 'f-' + CL[i] + 's s-' + CL[i] + ' w2', null, 2);
        o.ft = A.text(0, 44, FN[i], { cls: 't-s t-b', anchor: 'middle' });
        return o;
      });
      var bo = A.rect(X0 + LN[2], Y[2] - 9, 0, 18, 'f-none s-soft w1 dash', null, 2);
      var bot = A.text(X0 + LN[2] + 15, Y[2] + 4, '退避', { cls: 't-s', anchor: 'middle' });
      var sum = A.text(200, 210, 'SIFS < PIFS < DIFS：等得越短，优先级越高', { cls: 't-s', anchor: 'middle' });
      var ACT = [[], [0, 1, 2], [1, 2], [2], [0, 1, 2]];
      return {
        frame: function (ts, dt, k) {
          var act = ACT[k], w = act.length ? act[0] : -1, c = A.prog(ts, 2.2) * 160, all = k === 4;
          var Tw = w >= 0 ? LN[w] : 0, bk = w === 2 ? 30 : 0;
          rows.forEach(function (o, i) {
            var on = act.indexOf(i) >= 0;
            op(o.g, on || k === 0 ? 1 : 0.3);
            var bw = !on ? 0 : all ? LN[i] : Math.min(LN[i], c, Tw);
            A.set(o.bar, { width: bw }); op(o.bt, bw >= LN[i] - 2 ? 1 : 0);
            A.setText(o.st, on && !all && i !== w && c >= Tw ? '听到忙 → 推迟' : !on && k > 0 && k < 4 ? '（没有这类帧）' : '');
            A.set(o.st, { x: on ? X0 + Tw + 6 : X0 + 6 });
            var f = !all && i === w ? A.clamp(c - Tw - bk, 0, FR[i]) : 0;
            A.set(o.fr, { x: X0 + Tw + bk, width: f }); A.set(o.ft, { x: X0 + Tw + bk + FR[i] / 2 }); op(o.ft, f >= FR[i] * 0.7 ? 1 : 0);
          });
          var b = w === 2 && !all ? A.clamp(c - Tw, 0, 30) : 0;
          A.set(bo, { width: b }); op(bot, b > 20 ? 1 : 0);
          sum.setAttribute('class', all ? 't-b' : 't-s');
        }
      };
    }
  });

  /* ================= 2.4 DCF 流程 ================= */
  ANIM.reg('B:2.4', {
    title: 'DCF：先听，再等，再退避',
    cap: '上面是“信道空闲”的情况，下面是“信道忙”的情况。退避计数器 τ 只在信道空闲的时隙里减 1，信道一忙就冻结。',
    h: 200,
    tween: 2.1,
    steps: [
      '有分组要发 → 先侦听信道。下面分两种情况。',
      '① 信道空闲：再等一个 DIFS，期间仍空闲 → 直接发送 DATA。',
      '发完等 SIFS：收到 ACK 就成功；收不到 ACK 就重发。',
      '② 信道忙：一直侦听到空闲，再等 DIFS，然后随机选退避 τ（例：5 个时隙）。',
      '信道每空闲一个时隙，τ 减 1；别人一发（忙）就冻结，空闲 DIFS 后接着减。',
      'τ 减到 0 → 发送 DATA，再等 SIFS 收 ACK。'
    ],
    init: function (A) {
      var X = function (u) { return u; }, SL = 14, T0 = 5;
      A.text(8, 16, '① 信道空闲', 't-b'); A.text(8, 102, '② 信道忙', 't-b');
      [['信道', 38], ['站 X', 60], ['信道', 124], ['站 X', 148]].forEach(function (r) {
        A.text(8, r[1] + 4, r[0], 't-s'); A.line(50, r[1], 392, r[1], 's-line w1');
      });
      var B = Boxes(A, X), D = 'f-accs s-acc w1', K = 'f-goods s-good w1', O = 'f-line s-soft w1', W = 'f-purs s-pur w1';
      B.txt(54, 34, '空闲', 't-s', 0, { s: 0, anchor: 'start' }); B.txt(54, 56, '侦听', 't-s', 0, { s: 0, anchor: 'start' });
      B.add(60, 80, 108, 'DIFS', W, { s: 1 });
      B.add(38, 108, 168, 'DATA', D, { s: 1 });
      B.txt(173, 25, 'SIFS', 't-s', 170, { s: 2 });
      B.add(38, 178, 202, 'ACK', K, { s: 2 });
      B.txt(210, 34, '有 ACK → 成功；没有 → 重发', 't-s t-b f-good', 202, { s: 2, anchor: 'start' });
      B.add(124, 52, 100, '别人在发', O, { s: 3 });
      B.txt(54, 144, '侦听到忙', 't-s', 52, { s: 3, anchor: 'start' });
      B.add(148, 100, 128, 'DIFS', W, { s: 3 });
      // first idle slots, busy (freeze), DIFS, remaining slots
      var n1 = 2, a = 128, cnt = T0, slotsAt = [];
      for (var i = 0; i < n1; i++) { B.add(148, a, a + SL, String(cnt--), 'f-golds s-gold w1', { s: 4 }); slotsAt.push(a); a += SL; }
      var fz = a;
      B.add(124, fz, fz + 44, 'Y 在发', O, { s: 4 });
      B.add(148, fz, fz + 44, '冻结 ' + cnt, 'f-none s-bad w1 dash', { s: 4, tc: 't-s f-bad' });
      B.add(148, fz + 44, fz + 72, 'DIFS', W, { s: 4 });
      a = fz + 72; var n2 = cnt;
      for (i = 0; i < n2; i++) { B.add(148, a, a + SL, String(cnt--), 'f-golds s-gold w1', { s: 4 }); slotsAt.push(a); a += SL; }
      var tx = a;
      B.add(124, tx, tx + 60, 'DATA', D, { s: 5 });
      B.txt(tx + 65, 111, 'SIFS', 't-s', tx + 62, { s: 5 });
      B.add(124, tx + 70, tx + 94, 'ACK', K, { s: 5 });
      var cl = A.line(0, 112, 0, 160, 's-ink w1 op5');
      var rd = A.text(8, 186, '', 't-m');
      var CUR = [[0, 50], [50, 168], [168, 202], [50, 128], [128, tx], [tx, tx + 94]];
      return {
        frame: function (ts, dt, k) {
          var c = A.lerp(CUR[k][0], CUR[k][1], A.prog(ts, 2.0));
          B.show(stepCur(k, c), k);
          var on = k >= 3; shown(cl, on && k < 5 || (k === 5 && c < tx + 94)); A.set(cl, { x1: c, x2: c });
          if (!on) { A.setText(rd, ''); return; }
          var done = slotsAt.filter(function (s) { return c >= s + SL; }).length, tau = T0 - done;
          var s = c < 128 ? 'τ 还没选（等完 DIFS 才选）' : done >= T0 ? 'τ = 0 → 发送！' :
            (c >= fz && c < fz + 72) ? 'τ = ' + tau + '（信道忙 → 冻结）' : 'τ = ' + tau + '（空闲时隙，每个 −1）';
          A.setText(rd, '退避计数器 ' + s);
        }
      };
    }
  });

  /* ================= 2.5 二进制指数退避 ================= */
  (function () {
    var CW = [0, 1, 2, 3, 4].map(function (i) { return Math.min(32 * Math.pow(2, i), 256); });
    function m(cw) { return String((cw - 1) / 2); }
    var ST = CW.map(function (cw, i) {
      if (i === 0) return '第 1 次：CW = CW_min = ' + cw + '，在 0…' + (cw - 1) + ' 里均匀抽，平均 (' + cw + ' − 1)/2 = ' + m(cw) + ' 个时隙。';
      if (i === 4) return '第 5 次及以后：CW 封顶在 CW_max = ' + cw + '，平均一直是 ' + m(cw) + '，不再增加。';
      return '又冲突 → CW 翻倍为 ' + cw + (cw === 256 ? '（= CW_max）' : '') + '：在 0…' + (cw - 1) + ' 里抽，平均 ' + m(cw) + '。' +
        (i === 2 ? '最大只到 ' + (cw - 1) + '，不可能抽到 150。' : '');
    });
    ANIM.reg('B:2.5', {
      title: '二进制指数退避：CW 32 → 256',
      cap: '每一行是一次尝试：蓝条是可选范围 0…CW − 1，金线是平均值 (CW − 1)/2，红点是这次抽到的值。每冲突一次 CW 翻倍，到 256 封顶。',
      h: 222,
      steps: ST,
      init: function (A) {
        var X = function (v) { return 120 + v * 265 / 256; };
        [32, 64, 128, 256].forEach(function (v) { A.line(X(v), 18, X(v), 188, 's-line w1 dash op5'); });
        A.line(118, 190, 388, 190, 's-soft w1');
        [0, 32, 64, 128, 256].forEach(function (v) { A.text(X(v), 204, String(v), { cls: 't-s', anchor: 'middle' }); });
        A.text(8, 204, '退避值（时隙）', 't-s');
        var picks = CW.map(function (cw) { return Math.floor(A.rand() * cw); });
        var rows = CW.map(function (cw, i) {
          var y = 36 + 34 * i, o = { g: A.g() };
          A.text(8, y + 4, '第 ' + (i + 1) + ' 次 CW = ' + cw, 't-s', o.g);
          A.rect(X(0), y - 7, X(cw) - X(0), 14, 'f-accs s-acc w1', o.g, 2);
          A.line(X(cw / 2), y - 9, X(cw / 2), y + 9, 's-gold w3', o.g);
          o.dot = A.circle(X(0), y, 4.5, 'f-bad', o.g);
          o.info = A.text(X(0), y - 11, '', 't-s', o.g);
          o.tag = A.text(392, y - 11, i < 4 ? '✗ 冲突' : '封顶', { cls: 't-s t-b ' + (i < 4 ? 'f-bad' : 'f-gold'), anchor: 'end' }, o.g);
          return o;
        });
        return {
          frame: function (ts, dt, k) {
            rows.forEach(function (o, i) {
              op(o.g, i < k ? 0.55 : i === k ? A.prog(ts, 0.4) : 0);
              var cw = CW[i], p = i === k ? A.clamp(ts / 1.1, 0, 1) : 1;
              var v = p < 1 ? Math.floor((ts * 7.3 % 1) * cw) : picks[i];
              A.set(o.dot, { cx: X(v + 0.5) });
              A.setText(o.info, '0…' + (cw - 1) + ' · 抽到 ' + v + ' · 均值 ' + m(cw));
              op(o.tag, (i < 4 && i < k) || (i === 4 && k === 4) ? 1 : 0);
            });
          }
        };
      }
    });
  })();

  /* ================= 2.6 RTS/CTS 完整时间线（p.25） ================= */
  ANIM.reg('B:2.6', {
    title: 'RTS/CTS + NAV：退避的冻结与恢复',
    cap: '四个站 A、B、C、D 的时间线（p.25）。金色小格是退避时隙，紫色虚线框是 NAV。下方读数是两个站的退避计数器。',
    h: 196,
    tween: 2.1,
    steps: [
    '背景：D 刚给 C 发完数据，C 回了 ACK。接着 A 和 C 都有数据要发：A 抽到退避 8，C 抽到 12。',
    '信道空闲 DIFS 后 A、C 同时倒数。8 个时隙后 A 先数到 0，发 RTS 给 B。',
    'C 此时数到 12 − 8 = 4，听到信道忙 → 冻结计数器，剩下的 4 先留着。',
    'C 按 RTS、D 按 CTS 设 NAV。A 的两个分片和 B 的两个 ACK 只隔 SIFS，别人插不进。',
    '最后一个 ACK 后空闲 DIFS，C 从 4 接着数到 0，发数据给 D，D 回 ACK。',
    'A 重新抽到 15，比 C 剩的 4 长：数到 11 就被 C 打断而冻结。等得久的先发，更公平。'
    ],
    init: function (A) {
      var nA = 8, nC = 12, left = nC - nA, nA2 = 15, SL = 4, u = 0;
      function nx(d) { var a = u; u += d; return [a, u]; }
      var dD = nx(26); nx(5); var aC = nx(22); var difs1 = nx(14); var sl1 = nx(nA * SL);
      var rts = nx(22); nx(5); var cts = nx(22); nx(5); var f1 = nx(28); nx(5); var k1 = nx(22); nx(5); var f2 = nx(28); nx(5); var k2 = nx(22);
      var difs2 = nx(14); var sl2 = nx(left * SL); var dC = nx(28); nx(5); var aD = nx(22), U = u;
      var X = function (v) { return 24 + v * 372 / U; }, Y = { A: 40, B: 78, C: 116, D: 154 };
      Object.keys(Y).forEach(function (n) { A.text(6, Y[n] + 4, n, 't-b'); A.line(22, Y[n], 396, Y[n], 's-line w1'); });
      var B = Boxes(A, X), DA = 'f-accs s-acc w1', K = 'f-goods s-good w1', G = 'f-golds s-gold w1', N = 'f-purs s-pur w1 dash', S = 'f-golds s-gold w1';
      function slots(y, a, n, o) { for (var i = 0; i < n; i++) B.add(y, a + i * SL, a + (i + 1) * SL, '', S, o); }
      B.add(Y.D, dD[0], dD[1], '数据', DA); B.add(Y.C, aC[0], aC[1], 'ACK', K);
      B.txt((X(difs1[0]) + X(difs1[1])) / 2, 186, 'DIFS', 't-s', difs1[0]);
      slots(Y.A, sl1[0], nA); slots(Y.C, sl1[0], nA);
      B.txt((X(sl1[0]) + X(sl1[1])) / 2, Y.A - 13, nA + ' → 0', 't-s t-b', sl1[0] + 2);
      B.txt((X(sl1[0]) + X(sl1[1])) / 2, Y.C - 13, nC + ' → ' + left + '，冻结', 't-s t-b f-bad', 0, { ms: 2 });
      B.add(Y.A, rts[0], rts[1], 'RTS', G); B.add(Y.B, cts[0], cts[1], 'CTS', G);
      B.add(Y.C, rts[1], k2[1], 'NAV（听到 RTS）', N); B.add(Y.D, cts[1], k2[1], 'NAV（听到 CTS）', N);
      B.add(Y.A, f1[0], f1[1], '分片1', DA); B.add(Y.B, k1[0], k1[1], 'ACK', K);
      B.add(Y.A, f2[0], f2[1], '分片2', DA); B.add(Y.B, k2[0], k2[1], 'ACK', K);
      B.txt((X(difs2[0]) + X(difs2[1])) / 2, 186, 'DIFS', 't-s', difs2[0]);
      slots(Y.C, sl2[0], left);
      B.txt((X(sl2[0]) + X(sl2[1])) / 2, Y.C - 13, left + ' → 0', 't-s t-b', sl2[0] + 2);
      B.add(Y.C, dC[0], dC[1], '数据', DA); B.add(Y.D, aD[0], aD[1], 'ACK', K);
      slots(Y.A, sl2[0], left, { ms: 5 });
      B.add(Y.A, sl2[1], U, '剩 ' + (nA2 - left), 'f-none s-bad w1 dash', { ms: 5, tc: 't-s f-bad' });
      B.txt((X(sl2[0]) + X(sl2[1])) / 2, Y.A - 13, nA2 + ' → ' + (nA2 - left), 't-s t-b f-bad', 0, { ms: 5 });
      var cl = A.line(0, 22, 0, 166, 's-ink w1 op5');
      var CUR = [[0, aC[1]], [aC[1], rts[1]], [rts[1], rts[1]], [rts[1], k2[1]], [k2[1], U], [U, U]];
      function cnt(c, k) {
        var a = c < sl1[1] ? nA - Math.max(0, Math.floor((c - sl1[0]) / SL)) : c < k2[1] ? '0（在发送）' : k < 5 ? '发完了' : (nA2 - left) + '（重新抽 ' + nA2 + '，冻结）';
        var cc = c < sl1[1] ? nC - Math.max(0, Math.floor((c - sl1[0]) / SL)) : c < sl2[0] ? left + '（冻结）' : c < sl2[1] ? left - Math.floor((c - sl2[0]) / SL) : c < dC[1] ? '0（在发送）' : '0（发完了）';
        return '退避计数器　A：' + a + '　C：' + cc;
      }
      return {
        frame: function (ts, dt, k) {
          var c = A.lerp(CUR[k][0], CUR[k][1], A.prog(ts, 2.0));
          B.show(c, k);
          A.set(cl, { x1: X(c), x2: X(c) });
          B.list.forEach(function (it) { if (it.o.ms === 5) op(it.g, k === 5 ? A.prog(ts, 0.8) : 1); });
          A.note(cnt(c, k));
        }
      };
    }
  });

  /* ================= 2.7 隐藏节点 ================= */
  ANIM.reg('B:2.7', {
    title: '隐藏节点：A、C 互相听不到',
    cap: '虚线椭圆是各站的覆盖范围。C 在 B 的范围里、却在 A 的范围外，所以是 A 的隐藏节点。RTS/CTS 的关键：<b>C 听不到 RTS，但听得到 B 回的 CTS</b>。',
    h: 222,
    tween: 2.3,
    steps: [
      'A 要发给 B。C 在 B 的范围内，却在 A 的范围外（虚线是各自的覆盖范围）。',
      '不用 RTS/CTS：A 开始发数据。C 听不到 A，以为信道空闲，也开始发。',
      '两路信号在 B 处叠在一起 → 冲突！C 就是 A 的“隐藏节点”。',
      '用 RTS/CTS：A 先发 RTS。C 在 A 的范围外，听不到。',
      'B 回 CTS，C 在 B 的范围内，听得到！C 按 CTS 里的时长设 NAV，保持安静。',
      'A 的数据安全到达 B，B 回 ACK，没有冲突。'
    ],
    init: function (A) {
      var cp = A.el('clipPath', { id: 'anB27clip' }); A.rect(0, 0, 400, 222, '', cp, 0);
      var G = A.g({ 'clip-path': 'url(#anB27clip)' });
      var N = [[70, 'A', 'acc', '发送站'], [200, 'B', 'good', '目的站'], [330, 'C', 'gold', '隐藏节点']], y = 118, RX = 140, RY = 84;
      var rng = A.g({}, G);
      N.forEach(function (n) { A.el('ellipse', { cx: n[0], cy: y, rx: RX, ry: RY, cls: 'f-none s-' + n[2] + ' w1 dash' }, rng); });
      var ring = N.map(function (n) { return A.el('ellipse', { cx: n[0], cy: y, rx: 1, ry: 1, cls: 'f-none s-' + n[2] + ' w3' }, G); });
      var stx = N.map(function (n) {
        A.circle(n[0], y, 13, 'f-' + n[2]);
        A.text(n[0], y + 4.5, n[1], { cls: 't-b f-card', anchor: 'middle' });
        A.text(n[0], y + 30, n[3], { cls: 't-s', anchor: 'middle' });
        return A.text(n[0], 92, '', { cls: 't-s t-b', anchor: 'middle' });
      });
      var mode = A.text(8, 18, '', 't-b');
      var dA = A.circle(0, y, 5, 'f-acc'), dC = A.circle(0, y, 5, 'f-gold'), dB = A.circle(0, y, 5, 'f-good');
      var bang = star(A, 200, y, 24, 11, 8);
      var nav = A.g(); A.rect(296, 160, 68, 18, 'f-purs s-pur w1', nav, 4); A.text(330, 173, 'NAV 静默', { cls: 't-s t-b', anchor: 'middle' }, nav);
      function wave(i, p) { A.set(ring[i], { rx: Math.max(1, RX * p), ry: Math.max(1, RY * p) }); op(ring[i], p > 0 && p < 1 ? 1 - 0.7 * p : 0); }
      function dot(d, x1, x2, p, on) { A.set(d, { cx: A.lerp(x1, x2, p) }); op(d, on ? 1 : 0); }
      function say(i, s, cls) { A.setText(stx[i], s); stx[i].setAttribute('class', 't-s t-b ' + (cls || '')); }
      return {
        frame: function (ts, dt, k) {
          op(rng, k === 0 ? A.prog(ts, 0.8) : 1);
          A.setText(mode, k < 3 ? '不用 RTS/CTS' : '用 RTS/CTS');
          [0, 1, 2].forEach(function (i) { wave(i, 0); say(i, ''); });
          op(dA, 0); op(dB, 0); op(dC, 0); op(bang, 0); op(nav, k >= 4 ? (k === 4 ? A.prog(ts, 0.6, 1.3) : 1) : 0);
          var p1 = A.prog(ts, 1.0), p2 = A.prog(ts, 0.9, 0.9);
          if (k === 0) { say(0, '要发给 B', 'f-acc'); }
          else if (k === 1) {
            wave(0, p1); dot(dA, 70, 140, p1, true);
            say(2, p1 > 0.6 ? '听不到 A → 以为空闲' : '', 'f-gold');
            if (ts > 0.9) { wave(2, p2); dot(dC, 330, 260, p2, true); }
          } else if (k === 2) {
            dot(dA, 140, 200, p1, p1 < 1); dot(dC, 260, 200, p1, p1 < 1);
            op(bang, A.prog(ts, 0.3, 0.9)); say(1, ts > 0.9 ? '冲突！' : '', 'f-bad');
          } else if (k === 3) {
            wave(0, p1); say(0, 'RTS', 'f-acc'); say(2, p1 > 0.7 ? '听不到 RTS' : '', 'f-gold');
          } else if (k === 4) {
            wave(1, p1); say(1, 'CTS', 'f-good');
            say(0, p1 > 0.5 ? '收到 CTS' : '', 'f-acc'); say(2, p1 > 0.5 ? '听到 CTS！' : '', 'f-gold');
          } else {
            dot(dA, 70, 200, p1, p1 < 1); dot(dB, 200, 70, p2, ts > 0.9 && p2 < 1);
            say(0, ts > 1.8 ? '收到 ACK ✓' : '发数据', 'f-acc'); say(1, ts > 0.9 ? '收到 ✓ 回 ACK' : '', 'f-good'); say(2, '安静等待', 'f-gold');
          }
        }
      };
    }
  });

  /* ================= 3.1 PCF 轮询 ================= */
  ANIM.reg('B:3.1', {
    title: 'PCF：AP 逐个点名',
    cap: '上：AP 和三个站之间的帧；下：信道上的时间线（D = Data）。被点到才发，所以不会冲突；轮询期间 DCF 的异步业务暂停。',
    h: 232,
    tween: 2.1,
    steps: [
      'AP 有数据给 STA1：把数据和轮询合成一帧 Data + CF-Poll 发给它（捎带）。',
      'STA1 被点名、自己也有数据：隔 SIFS 回 Data + CF-ACK。',
      'AP 接着点 STA2：CF-Poll。STA2 没数据，只回 CF-ACK。',
      'AP 点 STA3：它没回应。AP 等一个 PIFS 就收回信道（比 DIFS 短，别人插不进）。',
      '都点完了（或无竞争期时间用完）：AP 广播 CF-End，无竞争期结束，回到 DCF。'
    ],
    init: function (A) {
      var SX = [90, 200, 310], SY = 104;
      SX.forEach(function (x) { A.line(200, 48, x, SY - 12, 's-line w1 dash'); });
      apIcon(A, 200, 40, 'AP');
      var scr = SX.map(function (x, i) { return laptop(A, x, SY, 'STA' + (i + 1)).scr; });
      var mode = A.text(8, 18, '', 't-b');
      var ml = A.text(0, 0, '', 't-s t-b'), d1 = A.circle(0, 0, 5, 'f-gold'), d2 = A.circle(0, 0, 5, 'f-acc');
      var bc = SX.map(function () { return A.circle(0, 0, 4.5, 'f-pur'); });
      var no = A.text(330, 104, '没回应', 't-s t-b f-bad');
      var LP = [[140, 66, 'end'], [208, 76, 'start'], [260, 66, 'start']];
      var u = 0; function nx(d) { var a = u; u += d; return [a, u]; }
      var I = [nx(44)]; nx(6); I.push(nx(44)); nx(6); I.push(nx(34)); nx(6); I.push(nx(34)); nx(6); I.push(nx(34)); var pf = nx(12); I.push(nx(36));
      var U = u, X = function (v) { return 40 + v * 352 / U; };
      A.text(8, 170, 'AP', 't-s'); A.text(8, 198, '各站', 't-s');
      A.line(38, 166, 394, 166, 's-line w1'); A.line(38, 194, 394, 194, 's-line w1');
      var B = Boxes(A, X), G = 'f-golds s-gold w1', D = 'f-accs s-acc w1';
      B.add(166, I[0][0], I[0][1], 'D+Poll→1', G); B.add(194, I[1][0], I[1][1], '1: D+ACK', D);
      B.add(166, I[2][0], I[2][1], 'Poll→2', G); B.add(194, I[3][0], I[3][1], '2: ACK', 'f-paper s-soft w1');
      B.add(166, I[4][0], I[4][1], 'Poll→3', G);
      B.txt((X(pf[0]) + X(pf[1])) / 2, 154, 'PIFS', 't-s t-b', pf[0]);
      B.add(166, I[5][0], I[5][1], 'CF-End', 'f-purs s-pur w1');
      A.text(8, 224, 'D = Data；帧间只隔 SIFS，站没回应时 AP 等 PIFS', 't-s');
      var CUR = [[0, I[0][1]], [I[0][1], I[1][1]], [I[1][1], I[3][1]], [I[3][1], pf[1]], [pf[1], U]];
      var ML = ['Data + CF-Poll', 'Data + CF-ACK'];
      function fly(d, i, back, p) {
        var a = [200, 48], b = [SX[i], SY - 12]; if (back) { var t = a; a = b; b = t; }
        A.set(d, { cx: A.lerp(a[0], b[0], p), cy: A.lerp(a[1], b[1], p) }); op(d, p > 0 && p < 1 ? 1 : 0);
      }
      function lab(i, s) { A.set(ml, { x: LP[i][0], y: LP[i][1], 'text-anchor': LP[i][2] }); A.setText(ml, s); }
      return {
        frame: function (ts, dt, k) {
          B.show(A.lerp(CUR[k][0], CUR[k][1], A.prog(ts, 2.0)), k);
          A.setText(mode, k < 4 ? '无竞争期 CFP：被点名才能发' : 'CF-End → 回到竞争期（DCF）');
          op(d1, 0); op(d2, 0); op(no, 0); bc.forEach(function (c) { op(c, 0); }); A.setText(ml, '');
          var p = A.prog(ts, 0.9), q = A.prog(ts, 0.9, 1.0), cur = [0, 0, 1, 2, -1][k];
          scr.forEach(function (s, i) { s.setAttribute('class', i === cur ? 'f-card s-gold w3' : 'f-card s-ink w1'); });
          if (k === 0) { fly(d1, 0, false, p); lab(0, ML[0]); }
          else if (k === 1) { fly(d2, 0, true, p); lab(0, ML[1]); }
          else if (k === 2) { fly(d1, 1, false, p); fly(d2, 1, true, q); lab(1, ts < 1 ? 'CF-Poll' : 'CF-ACK（没数据）'); }
          else if (k === 3) { fly(d1, 2, false, p); lab(2, ts < 1 ? 'CF-Poll' : 'AP 等 PIFS 收回'); op(no, A.prog(ts, 0.3, 1.0)); }
          else { bc.forEach(function (c, i) { fly(c, i, false, p); }); lab(1, 'CF-End（广播）'); }
        }
      };
    }
  });

  /* ================= 3.2 超帧 ================= */
  ANIM.reg('B:3.2', {
    title: '超帧 = CFP + CP（p.30 时间线）',
    cap: '上面一条是超帧的全貌；下面放大一次 TBTT 前后的细节。CFP 里帧与帧只隔 SIFS 或 PIFS（都比 DIFS 短），普通站插不进来。',
    h: 268,
    tween: 2.1,
    steps: [
      'CP 末尾：AP 给 B 发数据，B 隔 SIFS 回 ACK。这时到了目标信标时刻 TBTT。',
      'AP 再等一个 PIFS 抢到信道，发 Beacon：CFP 开始，所有站把 NAV 设到最大值。',
      'AP 隔 SIFS 发 Data + CF-Poll 给 A；A 隔 SIFS 回 Data + CF-Ack。',
      'AP 再发 CF-Poll，被点的站隔 SIFS 没回应 → AP 再等 PIFS 收回信道，接着点 B。',
      'B 只回 CF-Ack（没数据要发）。AP 广播 CF-End，NAV 清零，回到竞争期 CP。',
      '超帧 = CFP + CP。若到 TBTT 时信道正忙，AP 只能等它空闲，这个超帧就被缩短。'
    ],
    init: function (A) {
      // overview strip
      var O = [20, 200, 380];
      O.forEach(function (x) { A.line(x, 16, x, 46, 's-soft w1 dash'); A.text(x, 57, 'TBTT', { cls: 't-s', anchor: 'middle' }); });
      function sf(a, c, b, p) {
        A.rect(a, 24, c - a, 16, 'f-purs s-pur w1', p, 2); A.text((a + c) / 2, 36, 'CFP（PCF）', { cls: 't-s', anchor: 'middle' }, p);
        A.rect(c, 24, b - c, 16, 'f-accs s-acc w1', p, 2); A.text((c + b) / 2, 36, 'CP（DCF）', { cls: 't-s', anchor: 'middle' }, p);
        A.rect(a, 24, 6, 16, 'f-gold s-none', p, 1);
      }
      sf(20, 110, 200);
      A.text(110, 15, '超帧 = CFP + CP', { cls: 't-s t-b', anchor: 'middle' });
      var n2 = A.g(), s2 = A.g();
      sf(200, 290, 380, n2);
      A.rect(186, 22, 26, 20, 'f-line s-soft w1', s2, 2); A.text(199, 36, '忙', { cls: 't-s t-b', anchor: 'middle' }, s2);
      sf(218, 298, 380, s2);
      A.text(299, 15, '缩短的超帧（晚开始）', { cls: 't-s t-b f-bad', anchor: 'middle' }, s2);
      // detail
      var u = 0; function nx(d) { var a = u; u += d; return [a, u]; }
      var dB = nx(26); nx(4); var aB = nx(25); nx(4); var tb = u; var pi1 = nx(10); var bc = nx(36); nx(4); var dp = nx(36); nx(4);
      var da = nx(34); nx(4); var p0 = nx(26); var pi2 = nx(10); var pB = nx(26); nx(4); var ca = nx(36); nx(4); var ce = nx(36); nx(16);
      var U = u, X = function (v) { return 30 + v * 362 / U; }, Y = { AP: 114, A: 146, B: 178, NAV: 210 };
      Object.keys(Y).forEach(function (n) { A.text(4, Y[n] + 4, n, 't-s t-b'); A.line(28, Y[n], 394, Y[n], 's-line w1'); });
      [[0, bc[0], 'CP'], [bc[0], ce[1], 'CFP（无竞争期）'], [ce[1], U, 'CP']].forEach(function (b) {
        A.path('M' + (X(b[0]) + 1) + ' 86V80H' + (X(b[1]) - 1) + 'V86', 's-soft w1');
        A.text((X(b[0]) + X(b[1])) / 2, 76, b[2], { cls: 't-s', anchor: 'middle' });
      });
      A.line(X(tb), 84, X(tb), 220, 's-bad w1 dash'); A.text(X(tb), 236, 'TBTT', { cls: 't-s t-b f-bad', anchor: 'middle' });
      var B = Boxes(A, X), D = 'f-accs s-acc w1', K = 'f-goods s-good w1', G = 'f-golds s-gold w1', P = 'f-purs s-pur w1';
      B.add(Y.AP, dB[0], dB[1], 'Data', D); B.add(Y.B, aB[0], aB[1], 'ACK', K);
      B.txt((X(pi1[0]) + X(pi1[1])) / 2, 99, 'PIFS', 't-s t-b', pi1[0]);
      B.add(Y.AP, bc[0], bc[1], 'Beacon', 'f-gold s-gold w1');
      B.add(Y.AP, dp[0], dp[1], 'D+Poll', G); B.add(Y.A, da[0], da[1], 'D+Ack', D);
      B.add(Y.AP, p0[0], p0[1], 'Poll', G); B.txt(X(pi2[0]) + 2, Y.A - 3, '无回应', 't-s f-bad', p0[1]);
      B.txt((X(pi2[0]) + X(pi2[1])) / 2, 99, 'PIFS', 't-s t-b', pi2[0]);
      B.add(Y.AP, pB[0], pB[1], 'Poll', G); B.add(Y.B, ca[0], ca[1], 'CF-Ack', K);
      B.add(Y.AP, ce[0], ce[1], 'CF-End', P);
      var nav = A.rect(X(bc[1]), Y.NAV - 8, 0, 16, 'f-purs s-pur w1 dash', null, 2);
      var nt = A.text(0, Y.NAV + 4, '', { cls: 't-s', anchor: 'middle' });
      var clr = A.text(X(ce[1]) + 3, Y.NAV + 4, '清零', 't-s t-b f-bad');
      A.text(200, 256, '帧间只隔 SIFS / PIFS，都比 DIFS 短 → 普通站插不进 CFP', { cls: 't-s', anchor: 'middle' });
      var CUR = [[0, tb], [tb, bc[1]], [bc[1], da[1]], [da[1], pB[1]], [pB[1], U], [U, U]];
      return {
        frame: function (ts, dt, k) {
          var c = A.lerp(CUR[k][0], CUR[k][1], A.prog(ts, 2.0));
          B.show(c, k);
          var on = c >= bc[1], cut = k >= 4 && c >= ce[1], end = cut ? ce[1] : U;
          shown(nav, on); shown(nt, on); op(clr, cut ? 1 : 0);
          A.set(nav, { width: X(end) - X(bc[1]) });
          A.set(nt, { x: (X(bc[1]) + X(end)) / 2 }); A.setText(nt, cut ? 'NAV' : 'NAV 设到最大（整个 CFP 不竞争）');
          op(n2, k === 5 ? 1 - A.prog(ts, 0.6) : 1); op(s2, k === 5 ? A.prog(ts, 0.6, 0.4) : 0);
        }
      };
    }
  });

  /* ================= 3.3 加入 WLAN ================= */
  ANIM.reg('B:3.3', {
    title: '新设备加入 WLAN：扫描 → 认证 → 关联',
    cap: '左边竖线是 AP，右边竖线是新设备，箭头是它们之间交换的帧（从上往下按时间）。只有关联完成后才能收发数据帧。',
    h: 272,
    tween: 2.0,
    steps: [
      '① 被动扫描：AP 周期性广播信标 Beacon，新设备听到就知道附近有这个 AP。',
      '① 主动扫描：设备自己发 Probe Request，AP 回 Probe Response。两种方式用一种即可。',
      '② 认证：AP 和设备互相证明自己知道某个密码（老师提醒：一定要设密码）。',
      '③ 关联：交换设备和 BSS 的能力信息，并通过 DS 告诉所有 AP 这个设备现在在哪。',
      '关联完成，设备才能收发数据帧。（类比酒店：找酒店 → 出示证件 → 登记拿房卡）'
    ],
    init: function (A) {
      var XA = 110, XS = 300;
      var ds = A.g(); A.rect(14, 20, 50, 20, 'f-purs s-pur w1', ds, 4); A.text(39, 34, 'DS', { cls: 't-s t-b', anchor: 'middle' }, ds);
      A.line(64, 30, 95, 30, 's-pur w2');
      var dsn = A.text(14, 56, 'DS 记下位置', 't-s t-b f-pur');
      var dd = A.circle(0, 30, 4, 'f-pur');
      apIcon(A, XA, 34, 'AP'); laptop(A, XS, 32, '新设备');
      A.line(XA, 46, XA, 264, 's-faint w1 dash'); A.line(XS, 54, XS, 264, 's-faint w1 dash');
      var PH = [['① 扫描', '被动/主动', 70, 130], ['② 认证', '', 146, 182], ['③ 关联', '', 198, 234]].map(function (p) {
        var g = A.g();
        A.line(62, p[2], 62, p[3], 's-soft w2', g);
        A.text(8, (p[2] + p[3]) / 2 + (p[1] ? -2 : 4), p[0], 't-b', g);
        if (p[1]) A.text(8, (p[2] + p[3]) / 2 + 12, p[1], 't-s', g);
        return g;
      });
      var M = [[78, 1, 'Beacon（被动扫描：等信标）', 0, 0, 'gold'], [102, 0, 'Probe Request（主动扫描）', 1, 0, 'acc'], [124, 1, 'Probe Response', 1, 1, 'acc'],
        [154, 0, '认证请求', 2, 0, 'pur'], [176, 1, '认证响应（密码对上了）', 2, 1, 'pur'],
        [206, 0, '关联请求（能力信息）', 3, 0, 'good'], [228, 1, '关联响应', 3, 1, 'good']].map(function (m) {
        var g = A.g(), x1 = m[1] ? XA : XS, x2 = m[1] ? XS : XA;
        var ar = A.arrow(x1, m[0], x2, m[0], 's-' + m[5] + ' w2' + (m[3] === 0 ? ' dash' : ''), g);
        var t = A.text((XA + XS) / 2, m[0] - 5, m[2], { cls: 't-s', anchor: 'middle' }, g);
        return { g: g, ar: ar, t: t, x1: x1, x2: x2, y: m[0], s: m[3], d: m[4] };
      });
      var dg = A.g();
      A.arrow(205, 256, XS, 256, 's-acc w2', dg); A.arrow(205, 256, XA, 256, 's-acc w2', dg);
      A.text(205, 251, '关联完成 → 收发数据帧 ✓', { cls: 't-s t-b f-good', anchor: 'middle' }, dg);
      return {
        frame: function (ts, dt, k) {
          M.forEach(function (m) {
            var p = m.s < k ? 1 : m.s > k ? 0 : A.prog(ts, 0.8, m.d * 0.9);
            shown(m.g, p > 0);
            A.moveArrow(m.ar, m.x1, m.y, A.lerp(m.x1, m.x2, Math.max(p, 0.02)), m.y); op(m.t, p > 0.3 ? 1 : 0);
          });
          PH.forEach(function (g, i) { var ph = Math.min(k, 3) - 1; op(g, k === 4 || i === Math.max(0, ph) ? 1 : 0.35); });
          op(dg, k === 4 ? A.prog(ts, 0.7) : 0);
          var q = A.prog(ts, 0.8, 1.9);
          A.set(dd, { cx: A.lerp(95, 64, q) }); op(dd, k === 3 && q > 0 && q < 1 ? 1 : 0);
          op(dsn, k === 3 ? (q >= 1 ? 1 : 0) : k > 3 ? 1 : 0);
          op(ds, k >= 3 ? 1 : 0.5);
        }
      };
    }
  });

  /* ================= 3.4 MAC 帧格式 ================= */
  (function () {
    var F = [['帧控制', 2], ['时长/ID', 2, ['时长', '/ID']], ['地址 1', 6], ['地址 2', 6], ['地址 3', 6], ['序号控制', 2, ['序号', '控制']], ['地址 4', 6], ['帧体', '0–2312'], ['FCS', 4]];
    var HDR = F.filter(function (f) { return typeof f[1] === 'number'; }).map(function (f) { return f[1]; });
    var OV = HDR.reduce(function (a, b) { return a + b; }, 0), BODY = 1500;
    var EFF = (100 * BODY / (BODY + OV)).toFixed(1);
    var ACKF = [['帧控制', 2], ['时长', 2], ['目的地址', 6], ['CRC', 4]], ACKN = ACKF.reduce(function (a, f) { return a + f[1]; }, 0);
    ANIM.reg('B:3.4', {
      title: 'MAC 数据帧：一个字段一个字段看',
      cap: '上面是三类帧；中间是数据帧格式（数字是字节数），下面解释当前高亮的字段。老师点到的是<b>时长/ID</b>（旁人据此设 NAV）和<b>地址</b>（谁发、谁收）。',
      h: 226,
      steps: [
        '三类 MAC 帧：数据帧传数据；控制帧做预约和确认（RTS/CTS/ACK）；管理帧做关联、同步、安全。',
        '帧控制（2 字节）：说明这是控制帧、数据帧还是管理帧，还有 To DS/From DS、重试等标志。',
        '时长/ID（2 字节）：这一帧要占用信道多少微秒，旁人据此设 NAV。★ 老师点到',
        '地址 1–4（各 6 字节）：目的、源、BSS、发送方或接收方。★ 老师点到：谁发、谁收',
        '序号控制（2）：分片与重组；帧体（0–2312）：MSDU 或其分片；FCS（4）：32 位 CRC。',
        '开销 = 帧头 + FCS = ' + OV + ' 字节，装 ' + BODY + ' 字节时效率 ' + EFF + '%；ACK 帧只有 ' + ACKN + ' 字节。'
      ],
      init: function (A) {
        var cx = 8, chips = [];
        [['数据帧：传数据', 'acc'], ['控制帧：RTS/CTS/ACK', 'gold'], ['管理帧：关联·同步·安全', 'pur']].forEach(function (c) {
          var w = tw(c[0], 10.5) + 14, g = A.g();
          A.rect(cx, 8, w, 20, 'f-' + c[1] + 's s-' + c[1] + ' w1', g, 10);
          A.text(cx + w / 2, 22, c[0], { cls: 't-s', anchor: 'middle' }, g);
          chips.push(g); cx += w + 8;
        });
        A.text(10, 46, '数据帧格式（数字 = 字节数）', 't-s t-b');
        var x = 10, cells = F.map(function (f, i) {
          var w = i === 7 ? 66 : i === 8 ? 34 : 40;
          var r = A.rect(x, 54, w, 34, 'f-card s-line w1', null, 0);
          if (f[2]) { A.text(x + w / 2, 68, f[2][0], { cls: 't-s', anchor: 'middle' }); A.text(x + w / 2, 82, f[2][1], { cls: 't-s', anchor: 'middle' }); }
          else A.text(x + w / 2, 75, f[0], { cls: 't-s', anchor: 'middle' });
          A.text(x + w / 2, 102, String(f[1]), { cls: 't-s t-m', anchor: 'middle' });
          x += w; return r;
        });
        var lines = [0, 1, 2].map(function (i) { return A.text(12, 130 + 18 * i, '', 't-s'); });
        var ack = A.g(); x = 12;
        ACKF.forEach(function (f) {
          var w = tw(f[0] + ' ' + f[1], 10.5) + 10;
          A.rect(x, 186, w, 22, 'f-goods s-good w1', ack, 0);
          A.text(x + w / 2, 201, f[0] + ' ' + f[1], { cls: 't-s', anchor: 'middle' }, ack);
          x += w;
        });
        A.text(x + 8, 201, '= ' + ACKN + ' 字节（ACK 帧）', 't-s t-b', ack);
        var TX = [
          ['控制帧：RTS、CTS 做信道预约，ACK 做接收确认', '管理帧：关联和解除关联、定时同步、安全控制', '下面这一条是数据帧的格式'],
          ['帧控制（2 字节）：控制帧、数据帧还是管理帧？', '标志位：协议版本、类型/子类型、To DS/From DS、', '更多分片、重试、功率管理、WEP'],
          ['时长/ID（2 字节）：这一帧要占用信道多少微秒', '旁边的站读出这个值来设置 NAV（虚拟载波侦听）', '★ 老师点到的字段'],
          ['地址 1–4（各 6 字节）：目的、源、BSS、', '发送方或接收方的地址', '★ 老师点到：谁发、谁收'],
          ['序号控制（2）：用于分片和重组', '帧体（0–2312）：MAC 服务数据单元 MSDU 或它的一个分片', 'FCS（4）：32 位 CRC'],
          ['帧头 + FCS = ' + HDR.join(' + ') + ' = ' + OV + ' 字节', '装 ' + BODY + ' 字节：效率 = ' + BODY + ' / (' + BODY + ' + ' + OV + ') = ' + EFF + '%', 'ACK 帧只有 4 个字段：']
        ];
        var HL = [[], [0], [1], [2, 3, 4, 6], [5, 7, 8]];
        return {
          frame: function (ts, dt, k) {
            chips.forEach(function (g) { op(g, k === 0 ? 1 : 0.45); });
            cells.forEach(function (r, i) {
              var c = k === 5 ? (i === 7 ? 'f-goods s-good w2' : 'f-bads s-bad w1') : HL[k].indexOf(i) >= 0 ? 'f-golds s-gold w3' : 'f-card s-line w1';
              r.setAttribute('class', c);
            });
            lines.forEach(function (l, i) { A.setText(l, TX[k][i]); op(l, A.prog(ts, 0.5, i * 0.15)); });
            op(ack, k === 5 ? A.prog(ts, 0.6, 0.5) : 0);
          }
        };
      }
    });
  })();

  /* ================= 3.5 802.11e EDCA ================= */
  ANIM.reg('B:3.5', {
    title: 'EDCA：语音 AIFS 短、CW 小，更常抢到',
    cap: '同一个节点里的两个业务队列在竞争：先等各自的 AIFS，再按退避计数器倒数，先到 0 的发；输的一方冻结，下次接着数。图中取语音 AIFS = 2 时隙、CW = 4，网页 AIFS = 3 时隙、CW = 16（<b>示意值</b>，讲义没给数字）。802.11e 一共定义 8 个业务类。',
    h: 244,
    init: function (A) {
      var X0 = 100, PX = 13, SL = 0.22, PRE = 0.5, TXD = 0.9, HOLD = 0.9;
      var LN = [{ y: 92, a: 2, cw: 4, n: '语音', sub: 'AIFS 短 · CW 小', c: 'acc' }, { y: 146, a: 3, cw: 16, n: '网页', sub: 'AIFS 长 · CW 大', c: 'gold' }];
      A.text(8, 40, '信道', 't-s');
      A.rect(40, 27, X0 - 40, 18, 'f-line s-soft w1', null, 2); A.text(70, 40, '上一帧', { cls: 't-s', anchor: 'middle' });
      A.line(X0, 22, X0, 160, 's-faint w1 dash'); A.text(X0 + 4, 18, '信道变空闲', 't-s');
      A.line(X0, 36, 392, 36, 's-line w1');
      var win = A.rect(0, 27, 50, 18, 'f-accs s-acc w2', null, 2), wt = A.text(0, 40, '', { cls: 't-s t-b', anchor: 'middle' });
      LN.forEach(function (L) {
        A.text(8, L.y - 2, L.n, 't-b f-' + L.c); A.text(8, L.y + 12, L.sub, 't-s');
        L.ab = A.rect(X0, L.y - 9, 0, 18, 'f-' + L.c + 's s-' + L.c + ' w1', null, 2);
        L.at = A.text(X0 + L.a * PX / 2, L.y + 4, 'AIFS', { cls: 't-s', anchor: 'middle' });
        L.cells = [];
        for (var j = 0; j < 16; j++) {
          var g = A.g(), x = X0 + (L.a + j) * PX;
          A.rect(x, L.y - 9, PX, 18, 'f-golds s-gold w1', g, 0);
          L.cells.push({ g: g, t: A.text(x + PX / 2, L.y + 4, '', { cls: 't-s', anchor: 'middle' }, g) });
        }
        L.fz = A.text(0, L.y + 4, '', 't-s t-b f-bad');
      });
      var info = A.text(8, 182, '', 't-s'), tally = A.text(8, 202, '', 't-s t-b');
      A.text(8, 232, 'HCCA：类似 PCF，混合协调器 HC 按各站每类业务的负载分配无竞争发送机会', 't-s');
      var rng, st, lastT = -1;
      function d(n) { return Math.floor(rng() * n); }
      function plan() {
        var ev = LN[0].a + st.c[0], ew = LN[1].a + st.c[1];
        st.E = Math.min(ev, ew); st.w = ev <= ew ? 0 : 1; st.tie = ev === ew; st.dur = PRE + st.E * SL + TXD + HOLD;
      }
      function reset() { rng = A.rng(2026); st = { t0: 0, c: [d(LN[0].cw), d(LN[1].cw)], win: [0, 0] }; plan(); }
      function advance() {
        var w = st.w, l = 1 - w;
        st.win[w]++;
        st.c[l] = st.tie ? d(LN[l].cw) : st.c[l] - Math.max(0, st.E - LN[l].a);
        st.c[w] = d(LN[w].cw);
        st.t0 += st.dur; plan();
      }
      reset();
      return function (t) {
        if (t < lastT) reset();
        lastT = t;
        var guard = 0;
        while (t >= st.t0 + st.dur && guard++ < 500) advance();
        var tau = t - st.t0, s = A.clamp((tau - PRE) / SL, 0, st.E), done = tau >= PRE + st.E * SL;
        LN.forEach(function (L, i) {
          var c = st.c[i], n = i === st.w ? c : Math.max(0, Math.min(c, st.E - L.a));
          A.set(L.ab, { width: Math.min(s, L.a) * PX }); op(L.at, s >= L.a ? 1 : 0);
          L.cells.forEach(function (cl, j) { var on = j < n && s > L.a + j; shown(cl.g, on); if (on) A.setText(cl.t, String(c - j)); });
          var lose = done && i !== st.w;
          A.setText(L.fz, !lose ? '' : st.tie ? '同时到 0：节点内部碰撞，让给语音' : '冻结，剩 ' + (c - n));
          A.set(L.fz, { x: X0 + Math.max(st.E, Math.min(L.a, st.E)) * PX + 4 });
        });
        var wx = X0 + st.E * PX, wp = A.clamp((tau - PRE - st.E * SL) / 0.5, 0, 1);
        A.set(win, { x: wx, width: 50 * wp, cls: st.w ? 'f-golds s-gold w2' : 'f-accs s-acc w2' });
        A.set(wt, { x: wx + 25 }); A.setText(wt, st.w ? '网页帧' : '语音帧'); op(wt, wp > 0.7 ? 1 : 0);
        var tv = LN[0].a + st.c[0], tb = LN[1].a + st.c[1];
        A.setText(info, '本轮：语音 ' + LN[0].a + ' + ' + st.c[0] + ' = ' + tv + ' 个时隙，网页 ' + LN[1].a + ' + ' + st.c[1] + ' = ' + tb + ' 个 → ' + (st.w ? '网页' : '语音') + '先发');
        op(info, done ? 1 : 0.35);
        A.setText(tally, '累计：语音抢到 ' + (st.win[0] + (done && !st.w ? 1 : 0)) + ' 次，网页抢到 ' + (st.win[1] + (done && st.w ? 1 : 0)) + ' 次');
      };
    }
  });
})();
