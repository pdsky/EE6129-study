/* EE6129 Part B (partB.html) chapters 4–7: MANET, WSN, LTE, IoT. One figure per section, ids B:4.1 … B:7.6. */
(function () {
  'use strict';
  if (!window.ANIM) return;

  /* ---------- shared helpers (local to this file) ---------- */
  function c01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function op(el, v) { var s = c01(v).toFixed(2); if (el._op !== s) { el.setAttribute('opacity', s); el._op = s; } }
  function st(A, el, s) { if (el._s !== s) { A.setText(el, s); el._s = s; } }
  function cls(el, c) { if (el._c !== c) { el.setAttribute('class', c); el._c = c; } }
  function box(A, x, y, w, h, label, bcls, parent, tcls, rx) {
    var g = A.g({}, parent);
    g._r = A.rect(x, y, w, h, bcls || 'f-card s-line w1', g, rx == null ? 6 : rx);
    var ls = String(label).split('\n'), lh = /t-s|t-xs/.test(tcls || '') ? 13.5 : 16.5;
    g._t = ls.map(function (s, i) {
      return A.text(x + w / 2, y + h / 2 + 4 - (ls.length - 1) * lh / 2 + i * lh, s, { cls: tcls || '', anchor: 'middle' }, g);
    });
    return g;
  }
  function node(A, x, y, label, ncls, parent, r) {
    var g = A.g({}, parent);
    g._c = A.circle(x, y, r || 11, ncls || 'f-accs s-acc w2', g);
    g._t = A.text(x, y + 4, label || '', { cls: 't-b', anchor: 'middle' }, g);
    return g;
  }
  function moveNode(A, g, x, y) { A.set(g._c, { cx: x, cy: y }); A.set(g._t, { x: x, y: y + 4 }); }
  function along(pts, u) {
    var n = pts.length - 1;
    if (n < 1) return pts[0];
    u = c01(u) * n;
    var i = Math.min(n - 1, Math.floor(u)), f = u - i;
    return [pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f];
  }
  function bfs(adj, s, d) {
    var prev = {}, q = [s], seen = {}; seen[s] = 1;
    while (q.length) {
      var u = q.shift();
      if (u === d) break;
      (adj[u] || []).forEach(function (v) { if (!seen[v]) { seen[v] = 1; prev[v] = u; q.push(v); } });
    }
    if (!seen[d]) return null;
    var p = [d];
    while (p[0] !== s) p.unshift(prev[p[0]]);
    return p;
  }
  function hops(adj, s) {
    var h = {}, q = [s]; h[s] = 0;
    while (q.length) { var u = q.shift(); (adj[u] || []).forEach(function (v) { if (h[v] == null) { h[v] = h[u] + 1; q.push(v); } }); }
    return h;
  }
  function dist(a, b) { var dx = a[0] - b[0], dy = a[1] - b[1]; return Math.sqrt(dx * dx + dy * dy); }
  function vtext(A, x, y, s, tcls, parent) {           // vertical CJK label, one char per line
    var g = A.g({}, parent);
    for (var i = 0; i < s.length; i++) A.text(x, y + i * 13, s[i], { cls: tcls || 't-s', anchor: 'middle' }, g);
    return g;
  }
  function battery(A, x, y, w, h, level, fcls, parent) {
    var g = A.g({}, parent);
    A.rect(x, y, w, h, 'f-card s-soft w1', g, 2);
    A.rect(x + w, y + h * 0.3, 2.5, h * 0.4, 'f-soft s-none', g, 1);
    A.rect(x + 1.5, y + 1.5, (w - 3) * level, h - 3, fcls + ' s-none', g, 1);
    return g;
  }

  /* =====================================================================
     Chapter 4  MANET
     ===================================================================== */

  ANIM.reg('B:4.1', {
    title: 'MANET：没有 AP，节点自己组网',
    cap: '看什么：先看“一切经过 AP”，再看去掉 AP 后节点怎样直接相连。连线 = 两个节点之间信道够好；金色小点是数据包。',
    h: 230, tween: 3.6, stepDur: 4.4,
    steps: [
      '有基础设施的网络：每个包都要先交给 AP（或基站）再转出去，AP 是中心。',
      'MANET 没有 AP：信道够好的节点直接相连，远的靠中间节点多跳转发。',
      '没有固定控制器：需要时由节点动态选一个出来，或者把控制功能分散到所有节点。',
      '三个“自”：自建立、自组织、自管理。节点 7 移走，旧链路断（红），包自动改走新路。',
      '规模可小可大：蓝牙组成身体域网/个域网（半径约 10 m）；802.11 能做单跳，也能做几平方公里的多跳网。'
    ],
    init: function (A) {
      var P = [[45, 165], [110, 110], [130, 195], [200, 150], [275, 190], [285, 105], [360, 150]];
      var R = 95, AP = [200, 52];
      var main = A.g(), apG = A.g({}, main), linkG = A.g({}, main), deco = A.g({}, main), nodeG = A.g({}, main);
      var apL = P.map(function (p) { return A.line(p[0], p[1], AP[0], AP[1], 's-faint w1 dash', apG); });
      A.rect(AP[0] - 17, AP[1] - 12, 34, 24, 'f-golds s-gold w2', apG, 5);
      A.text(AP[0], AP[1] + 4, 'AP', { cls: 't-b', anchor: 'middle' }, apG);
      var apX = A.g({}, main);
      A.line(AP[0] - 22, AP[1] - 17, AP[0] + 22, AP[1] + 17, 's-bad w3', apX);
      A.line(AP[0] + 22, AP[1] - 17, AP[0] - 22, AP[1] + 17, 's-bad w3', apX);
      var L = [];
      for (var i = 0; i < P.length; i++) for (var j = i + 1; j < P.length; j++) L.push({ i: i, j: j, el: A.line(0, 0, 0, 0, 's-acc w2', linkG), b0: dist(P[i], P[j]) < R });
      var ctrlRing = A.circle(P[3][0], P[3][1], 17, 'f-none s-gold w3', deco);
      var ctrlTxt = A.text(P[3][0], P[3][1] - 24, '选出的控制器', { cls: 't-s f-gold t-b', anchor: 'middle' }, deco);
      var rings = P.map(function (p) { return A.circle(p[0], p[1], 15, 'f-none s-gold w2', deco); });
      var nodes = P.map(function (p, i) { return node(A, p[0], p[1], String(i + 1), 'f-accs s-acc w2', nodeG); });
      var head = A.text(12, 20, '', { cls: 't-b' }, main);
      var pkt = A.circle(0, 0, 5, 'f-gold s-card w1', main);
      // scene 2: scale
      var sc2 = A.g();
      A.circle(100, 128, 62, 'f-accs s-acc w1 dash', sc2);
      A.text(100, 42, '身体域网 / 个域网', { cls: 't-b', anchor: 'middle' }, sc2);
      var small = [[80, 105], [128, 118], [92, 155]];
      A.line(80, 105, 128, 118, 's-acc w2', sc2); A.line(128, 118, 92, 155, 's-acc w2', sc2); A.line(92, 155, 80, 105, 's-acc w2', sc2);
      small.forEach(function (p) { A.circle(p[0], p[1], 7, 'f-card s-acc w2', sc2); });
      A.text(100, 208, '蓝牙 · 半径约 10 m · 单跳', { cls: 't-s', anchor: 'middle' }, sc2);
      var chain = [[218, 160], [262, 112], [306, 150], [348, 98], [384, 140]];
      A.text(300, 42, '802.11 多跳网', { cls: 't-b', anchor: 'middle' }, sc2);
      for (var c = 0; c < chain.length - 1; c++) A.line(chain[c][0], chain[c][1], chain[c + 1][0], chain[c + 1][1], 's-acc w2', sc2);
      chain.forEach(function (p) { A.circle(p[0], p[1], 7, 'f-card s-acc w2', sc2); });
      A.text(300, 208, '可覆盖几平方公里', { cls: 't-s', anchor: 'middle' }, sc2);
      A.line(200, 40, 200, 215, 's-line w1 dash', sc2);
      var pkt2 = A.circle(0, 0, 4.5, 'f-gold', sc2);
      var heads = ['有基础设施：一切经过 AP', 'MANET：没有 AP，节点直接相连', '没有固定控制器', '自建立 · 自组织 · 自管理', ''];

      return {
        frame: function (ts, dt, k) {
          var pos = P.map(function (p) { return p.slice(); });
          if (k === 3) { var u = A.prog(ts, 1.4, 0.4); pos[6] = [A.lerp(360, 352, u), A.lerp(150, 58, u)]; }
          nodes.forEach(function (g, i) { moveNode(A, g, pos[i][0], pos[i][1]); A.set(apL[i], { x1: pos[i][0], y1: pos[i][1] }); });
          op(main, k === 4 ? 1 - A.prog(ts, 0.5) : 1);
          op(sc2, k === 4 ? A.prog(ts, 0.6, 0.3) : 0);
          op(apG, k === 0 ? 1 : k === 1 ? 1 - A.prog(ts, 0.8) * 0.75 : 0.25);
          op(apX, k === 0 ? 0 : k === 1 ? A.prog(ts, 0.6, 0.2) : 1);
          var adj = {};
          L.forEach(function (l) {
            var on = dist(pos[l.i], pos[l.j]) < R;
            if (on) { (adj[l.i] = adj[l.i] || []).push(l.j); (adj[l.j] = adj[l.j] || []).push(l.i); }
            A.set(l.el, { x1: pos[l.i][0], y1: pos[l.i][1], x2: pos[l.j][0], y2: pos[l.j][1] });
            var show = k === 0 ? 0 : (on || (k === 3 && l.b0)) ? (k === 1 ? A.prog(ts, 0.8, 0.3) : 1) : 0;
            cls(l.el, k === 3 && l.b0 && !on ? 's-bad w2 dash' : k === 3 && !l.b0 && on ? 's-good w3' : 's-acc w2');
            op(l.el, show);
          });
          var tx = heads[k];
          if (k === 2 && ts > 1.9) tx = '或：控制功能分散到每个节点';
          st(A, head, tx);
          op(ctrlRing, k === 2 ? A.prog(ts, 0.5) * (ts > 1.9 ? 0 : 1) : 0);
          op(ctrlTxt, k === 2 && ts <= 1.9 ? A.prog(ts, 0.5) : 0);
          rings.forEach(function (r) { op(r, k === 2 && ts > 1.9 ? A.prog(ts, 0.5, 1.9) : 0); });
          var path = null, pu = -1;
          if (k === 0) { path = [P[0], AP, P[6]]; pu = A.prog(ts, 2.4, 0.4); }
          else if (k === 1 || k === 3) {
            var b = bfs(adj, 0, 6);
            if (b) path = b.map(function (n) { return pos[n]; });
            pu = k === 1 ? A.prog(ts, 2.4, 0.9) : A.prog(ts, 1.8, 1.8);
          }
          var arrived = path && pu >= 1;
          if (path && !arrived && ts > (k === 3 ? 1.8 : k === 1 ? 0.9 : 0.4)) { var q = along(path, pu); A.set(pkt, { cx: q[0], cy: q[1] }); op(pkt, 1); } else op(pkt, 0);
          cls(nodes[6]._c, arrived ? 'f-golds s-gold w3' : 'f-accs s-acc w2');
          if (k === 4) { var q2 = along(chain, A.prog(ts, 2.4, 0.9)); A.set(pkt2, { cx: q2[0], cy: q2[1] }); op(pkt2, ts > 0.9 ? 1 : 0); }
        }
      };
    }
  });

  ANIM.reg('B:4.2', {
    title: '每个节点都是路由器：多跳中继',
    cap: '前两步是讲义 p.44 的拓扑（连线 = 信道够好），后三步是 p.46 的例题：新节点 C 加入时，路由表怎样一步步建起来。',
    h: 240, tween: 3.8, stepDur: 4.8,
    steps: [
      '讲义 p.44：A 和 C 之间没有直达信道（红虚线），B 替 A 转发，B 就在当路由器。',
      'A → E 也一样，由 D 中继。所以每个节点都要能随时当路由器；选出的无环路径叫 route。',
      '例题 p.46：开始只有 A、B。两者各自广播信标（地址+位置），交换控制消息后更新路由表。',
      'C 加入并广播信标。情况一：A、B 都直接听到 C，三者之间全是单跳直连。',
      '情况二：只有 B 听到 C。更新顺序 ① B↔C ② B↔A ③ B↔C，最后 A、C 都知道“经 B 可达”。'
    ],
    init: function (A) {
      var s1 = A.g(), s2 = A.g();
      var N = { A: [70, 165], B: [150, 62], C: [290, 62], D: [215, 165], E: [340, 165] };
      [['A', 'B'], ['B', 'C'], ['B', 'D'], ['A', 'D'], ['D', 'E'], ['C', 'E']].forEach(function (e) {
        A.line(N[e[0]][0], N[e[0]][1], N[e[1]][0], N[e[1]][1], 's-line w3', s1);
      });
      var noAC = A.g({}, s1);
      A.line(N.A[0], N.A[1], N.C[0], N.C[1], 's-bad w2 dash', noAC);
      A.text(240, 102, '无直达', { cls: 't-s f-bad', anchor: 'middle' }, noAC);
      var noAE = A.g({}, s1);
      A.path('M70 165 Q205 232 340 165', 's-bad w2 dash', noAE);
      A.text(205, 214, '无直达', { cls: 't-s f-bad', anchor: 'middle' }, noAE);
      var hlG = A.g({ cls: 'op7' }, s1), hl1 = A.poly([N.A, N.B, N.C], 's-gold w4', hlG), hl2 = A.poly([N.A, N.D, N.E], 's-gold w4', hlG);
      var nd = {};
      Object.keys(N).forEach(function (k) { nd[k] = node(A, N[k][0], N[k][1], k, k === 'A' ? 'f-acc s-acc w2' : 'f-accs s-acc w2', s1, 13); });
      A.set(nd.A._t, { cls: 't-b f-card' });
      var rtB = A.text(150, 36, 'B 当路由器', { cls: 't-s f-gold t-b', anchor: 'middle' }, s1);
      var rtD = A.text(252, 150, 'D 当路由器', { cls: 't-s f-gold t-b', anchor: 'middle' }, s1);
      var pkt = A.circle(0, 0, 5.5, 'f-gold s-card w1', s1);
      // scene 2: p.46 example
      var M = { A: [60, 68], B: [200, 68], C: [340, 68] };
      var lAB = A.line(60, 68, 200, 68, 's-acc w3', s2), lBC = A.line(200, 68, 340, 68, 's-acc w3', s2);
      var lAC = A.path('M60 68 Q200 4 340 68', 's-acc w3', s2);
      var noTxt = A.text(200, 24, 'A 听不到 C', { cls: 't-s f-bad', anchor: 'middle' }, s2);
      var beacon = { A: A.circle(60, 68, 0, 'f-none s-gold w2', s2), B: A.circle(200, 68, 0, 'f-none s-gold w2', s2), C: A.circle(340, 68, 0, 'f-none s-gold w2', s2) };
      var md = {};
      Object.keys(M).forEach(function (k) { md[k] = node(A, M[k][0], M[k][1], k, 'f-accs s-acc w2', s2, 13); });
      var msg = A.circle(0, 0, 5, 'f-pur s-card w1', s2);
      var tag = A.text(200, 98, '', { cls: 't-s f-pur t-b', anchor: 'middle' }, s2);
      var tb = {};
      ['A', 'B', 'C'].forEach(function (k, i) {
        var g = A.g({}, s2), x = 12 + i * 130;
        A.rect(x, 108, 116, 120, 'f-card s-line w1', g, 6);
        A.text(x + 58, 126, k + ' 的路由表', { cls: 't-b', anchor: 'middle' }, g);
        A.line(x + 8, 133, x + 108, 133, 's-line w1', g);
        tb[k] = { g: g, rows: [A.text(x + 14, 154, '', { cls: 't-m' }, g), A.text(x + 14, 178, '', { cls: 't-m' }, g)] };
      });
      function setRows(k, arr, ts) {
        tb[k].rows.forEach(function (r, i) {
          var e = arr[i];
          st(A, r, e ? e[0] : '');
          cls(r, e && /经/.test(e[0]) ? 't-m f-gold t-b' : 't-m');
          op(r, e ? (e[1] == null ? 1 : A.prog(ts, 0.4, e[1])) : 0);
        });
      }
      function bounce(a, b, t0, ts) {         // message a → b → a during [t0, t0+1]
        var u = ts - t0;
        if (u < 0 || u > 1) return null;
        var p = u < 0.5 ? along([M[a], M[b]], u * 2) : along([M[b], M[a]], (u - 0.5) * 2);
        return p;
      }
      return {
        frame: function (ts, dt, k) {
          var sc = k <= 1 ? 0 : 1;
          op(s1, sc === 0 ? 1 : 0); op(s2, sc === 1 ? (k === 2 ? A.prog(ts, 0.5) : 1) : 0);
          if (sc === 0) {
            op(noAC, k === 0 ? A.prog(ts, 0.5) : 0.25); op(noAE, k === 1 ? A.prog(ts, 0.5) : 0);
            op(hl1, k === 0 ? A.prog(ts, 0.5, 2.6) : 0); op(hl2, k === 1 ? A.prog(ts, 0.5, 2.6) : 0);
            op(rtB, k === 0 ? A.prog(ts, 0.4, 1.0) : 0); op(rtD, k === 1 ? A.prog(ts, 0.4, 1.0) : 0);
            A.set(nd.B._c, { cls: k === 0 && ts > 1 ? 'f-golds s-gold w3' : 'f-accs s-acc w2' });
            A.set(nd.D._c, { cls: k === 1 && ts > 1 ? 'f-golds s-gold w3' : 'f-accs s-acc w2' });
            var q = along(k === 0 ? [N.A, N.B, N.C] : [N.A, N.D, N.E], A.prog(ts, 2.2, 0.4));
            A.set(pkt, { cx: q[0], cy: q[1] }); op(pkt, ts > 0.4 ? 1 : 0);
            return;
          }
          var hasC = k >= 3;
          op(md.C, hasC ? (ts < 0.4 ? A.prog(ts, 0.4) : 1) : 0);
          op(tb.C.g, hasC ? 1 : 0.15);
          op(lAB, k === 2 ? A.prog(ts, 0.4, 1.4) : 1);
          op(lBC, k === 3 ? A.prog(ts, 0.4, 1.2) : k === 4 ? A.prog(ts, 0.4, 0.9) : 0);
          op(lAC, k === 3 ? A.prog(ts, 0.4, 1.2) : k === 4 ? 0.8 * A.prog(ts, 0.4, 0.9) : 0);
          cls(lAC, k === 4 ? 's-bad w2 dash' : 's-acc w3');
          op(noTxt, k === 4 ? A.prog(ts, 0.4, 0.9) : 0);
          ['A', 'B', 'C'].forEach(function (n) {
            var on = (k === 2 && n !== 'C') || (k >= 3 && n === 'C');
            var u = (ts % 1.2) / 1.2;
            A.set(beacon[n], { r: on && ts < 2.4 ? 6 + 32 * u : 0 });
            op(beacon[n], on && ts < 2.4 ? 1 - u : 0);
          });
          var heard = function (n) { return (k === 3 && n !== 'C') || (k === 4 && n === 'B'); };
          ['A', 'B'].forEach(function (n) { A.set(md[n]._c, { cls: heard(n) && ts > 0.8 && ts < 2.2 ? 'f-golds s-gold w3' : 'f-accs s-acc w2' }); });
          var p = null, lab = '';
          if (k === 2) { p = bounce('A', 'B', 0.4, ts); lab = '交换控制消息'; }
          if (k === 4) {
            p = bounce('B', 'C', 0.9, ts) || bounce('B', 'A', 1.9, ts) || bounce('B', 'C', 2.9, ts);
            lab = ts < 0.9 ? '' : ts < 1.9 ? '① B↔C' : ts < 2.9 ? '② B↔A' : '③ B↔C';
          }
          if (p) { A.set(msg, { cx: p[0], cy: p[1] }); op(msg, 1); } else op(msg, 0);
          st(A, tag, lab); op(tag, lab ? 1 : 0);
          if (k === 2) { setRows('A', [['B：直达', 1.4]], ts); setRows('B', [['A：直达', 1.4]], ts); setRows('C', [], ts); }
          if (k === 3) {
            setRows('A', [['B：直达'], ['C：直达', 1.2]], ts); setRows('B', [['A：直达'], ['C：直达', 1.2]], ts);
            setRows('C', [['A：直达', 1.2], ['B：直达', 1.2]], ts);
          }
          if (k === 4) {
            setRows('A', [['B：直达'], ['C：经 B', 2.4]], ts); setRows('B', [['A：直达'], ['C：直达', 1.4]], ts);
            setRows('C', [['A：经 B', 3.4], ['B：直达', 1.4]], ts);
          }
        }
      };
    }
  });

  ANIM.reg('B:4.3', {
    title: '拓扑总在变：组合稳定性',
    cap: '绿线 = 刚形成的链路，红虚线 = 刚断开的链路，灰色节点 = 电池耗尽/故障。拖动速度：拓扑变化快过更新传遍全网的速度，网络就不再组合稳定。条形长度只是示意。',
    h: 256, seed: 11,
    init: function (A) {
      var N = 9, R = 100, X0 = 14, X1 = 386, Y0 = 34, Y1 = 150, CAP = 3, TAU = 5;
      var pos = [], vel = [];
      for (var i = 0; i < N; i++) {
        pos.push([A.lerp(X0 + 30, X1 - 30, (i % 3 + 0.5) / 3) + (A.rand() - 0.5) * 60, A.lerp(Y0 + 10, Y1 - 10, (Math.floor(i / 3) + 0.5) / 3) + (A.rand() - 0.5) * 24]);
        var a = A.rand() * 2 * Math.PI; vel.push([Math.cos(a), Math.sin(a)]);
      }
      var start = pos.map(function (p) { return p.slice(); });
      A.rect(6, 26, 388, 132, 'f-none s-line w1 dash', null, 8);
      var linkG = A.g(), L = [];
      for (i = 0; i < N; i++) for (var j = i + 1; j < N; j++) L.push({ i: i, j: j, el: A.line(0, 0, 0, 0, 's-acc w2', linkG), on: false, tc: -9, up: true });
      var nodes = pos.map(function (p) { return A.circle(p[0], p[1], 7, 'f-accs s-acc w2'); });
      var status = A.text(388, 18, '', { cls: 't-b', anchor: 'end' });
      A.text(12, 18, '节点移动、电池耗尽 → 链路断开/形成', { cls: 't-s' });
      var BX = 118, BW = 200, SC = BW / 8;
      A.text(BX - 8, 180, '拓扑变化速度', { cls: 't-s', anchor: 'end' });
      A.text(BX - 8, 202, '更新传遍全网', { cls: 't-s', anchor: 'end' });
      A.rect(BX, 171, BW, 12, 'f-paper s-line w1', null, 3);
      var barC = A.rect(BX, 171, 0, 12, 'f-acc s-none', null, 3);
      A.rect(BX, 193, BW, 12, 'f-paper s-line w1', null, 3);
      A.rect(BX, 193, CAP * SC, 12, 'f-good s-none', null, 3);
      A.line(BX + CAP * SC, 166, BX + CAP * SC, 210, 's-good w1 dash');
      var rateTx = A.text(BX + BW + 8, 181, '', { cls: 't-s t-m' });
      A.text(BX + BW + 8, 203, '（协议能力）', { cls: 't-s' });
      A.text(BX - 8, 233, '带宽', { cls: 't-s', anchor: 'end' });
      var bwU = A.rect(BX, 224, 0, 13, 'f-gold s-none', null, 3), bwD = A.rect(BX, 224, BW, 13, 'f-goods s-good w1', null, 3);
      var bwT1 = A.text(BX + 4, 248, '路由更新', { cls: 't-s f-gold' }), bwT2 = A.text(BX + BW, 248, '用户数据', { cls: 't-s f-good', anchor: 'end' });
      var speed = 0.4, acc = 0, lastT = 0;
      A.slider({ label: '节点移动速度', min: 0, max: 3, step: 0.1, value: speed, fmt: function (v) { return v.toFixed(1) + '（相对）'; }, on: function (v) { speed = v; A.redraw(); } });
      return {
        reset: function () { for (var i = 0; i < N; i++) pos[i] = start[i].slice(); acc = 0; },
        frame: function (t, dt) {
          if (t < lastT) { for (var r = 0; r < N; r++) pos[r] = start[r].slice(); acc = 0; L.forEach(function (l) { l.on = false; l.tc = -9; }); }
          lastT = t;
          for (var n = 0; n < N; n++) {
            pos[n][0] += vel[n][0] * speed * 13 * dt; pos[n][1] += vel[n][1] * speed * 13 * dt;
            if (pos[n][0] < X0 || pos[n][0] > X1) { vel[n][0] *= -1; pos[n][0] = A.clamp(pos[n][0], X0, X1); }
            if (pos[n][1] < Y0 || pos[n][1] > Y1) { vel[n][1] *= -1; pos[n][1] = A.clamp(pos[n][1], Y0, Y1); }
          }
          var dead = (t % 12) > 6 && (t % 12) < 9;
          var ch = 0;
          L.forEach(function (l) {
            var alive = !(dead && (l.i === 0 || l.j === 0));
            var on = alive && dist(pos[l.i], pos[l.j]) < R;
            if (on !== l.on && t > 0.05) { ch++; l.tc = t; l.up = on; }
            l.on = on;
            var age = t - l.tc;
            A.set(l.el, { x1: pos[l.i][0], y1: pos[l.i][1], x2: pos[l.j][0], y2: pos[l.j][1] });
            if (on) { cls(l.el, age < 1 ? 's-good w3' : 's-acc w2'); op(l.el, 1); }
            else if (age < 1) { cls(l.el, 's-bad w2 dash'); op(l.el, 1 - age); }
            else op(l.el, 0);
          });
          nodes.forEach(function (c, n) { A.set(c, { cx: pos[n][0], cy: pos[n][1] }); cls(c, n === 0 && dead ? 'f-line s-faint w2' : 'f-accs s-acc w2'); });
          if (dt > 0) acc = acc * Math.exp(-dt / TAU) + ch;
          var rate = acc / TAU;
          A.set(barC, { width: Math.min(BW, rate * SC) });
          st(A, rateTx, rate.toFixed(1) + ' 次/秒');
          var stable = rate <= CAP;
          st(A, status, stable ? '组合稳定 ✓' : '不稳定：更新跟不上');
          cls(status, 't-b ' + (stable ? 'f-good' : 'f-bad'));
          cls(barC, (stable ? 'f-acc' : 'f-bad') + ' s-none');
          var fu = Math.min(0.92, 0.06 + 0.4 * rate / CAP);
          A.set(bwU, { width: BW * fu }); A.set(bwD, { x: BX + BW * fu, width: BW * (1 - fu) });
          op(bwT1, 1); op(bwT2, 1);
        }
      };
    }
  });

  ANIM.reg('B:4.4', {
    title: '周期性路由 vs 按需路由',
    cap: '右上角数一数控制消息（数字只对这张示意图成立）。周期性协议一直在发；按需协议只在 S 有数据要发给 D 时才发。RREQ/RREP 是按需协议（如 AODV）里路由请求/应答的常用叫法。',
    h: 240, tween: 5.2, stepDur: 5.4,
    steps: [
      '周期性（表驱动）：不管有没有数据，每个节点都定期广播路由信息，维护到所有节点的路由。',
      '好处：S 要发数据时查表马上就走，不用等。代价：没数据时也在不停交换，开销大。',
      '按需：平时不发控制消息。S 有数据要发，才广播路由请求 RREQ，一跳一跳地泛洪出去。',
      'D 收到 RREQ 后沿反向路径回一个路由应答 RREP，沿途节点记住“去 D 走哪一跳”。',
      '路由建好后才发数据：第一个包要等路由发现，但平时省带宽、省电。',
      '链路 e–D 断了（节点移走）→ 路由重构：重新发现一条新路，数据改走新路。'
    ],
    init: function (A) {
      var P = { S: [38, 125], a: [105, 64], b: [110, 185], c: [190, 122], d: [200, 205], e: [275, 64], f: [285, 160], D: [360, 115] };
      var K = Object.keys(P);
      var E = [['S', 'a'], ['S', 'b'], ['a', 'c'], ['b', 'c'], ['b', 'd'], ['a', 'e'], ['c', 'e'], ['c', 'f'], ['d', 'f'], ['e', 'D'], ['f', 'D']];
      function adjOf(skip) {
        var adj = {};
        E.forEach(function (e) { if (skip && e.join() === skip) return; (adj[e[0]] = adj[e[0]] || []).push(e[1]); (adj[e[1]] = adj[e[1]] || []).push(e[0]); });
        return adj;
      }
      var adj1 = adjOf(null), adj2 = adjOf('e,D');
      var path1 = bfs(adj1, 'S', 'D'), path2 = bfs(adj2, 'S', 'D');
      var h1 = hops(adj1, 'S'), h2 = hops(adj2, 'S');
      var nRREQ1 = K.filter(function (k) { return k !== 'D' && h1[k] != null; }).length;
      var nRREQ2 = K.filter(function (k) { return k !== 'D' && h2[k] != null; }).length;
      var linkEl = {};
      E.forEach(function (e) { linkEl[e.join()] = A.line(P[e[0]][0], P[e[0]][1], P[e[1]][0], P[e[1]][1], 's-line w2'); });
      var brk = A.text((P.e[0] + P.D[0]) / 2 + 4, (P.e[1] + P.D[1]) / 2 - 2, '✕', { cls: 't-l t-b f-bad', anchor: 'middle' });
      var routeG = A.g({ cls: 'op7' });
      function routeLines(p) { var out = []; for (var i = 0; i < p.length - 1; i++) out.push(A.line(P[p[i]][0], P[p[i]][1], P[p[i + 1]][0], P[p[i + 1]][1], 's-good w4', routeG)); return out; }
      var r1 = routeLines(path1), r2 = routeLines(path2);
      var rings = {}, nodes = {};
      K.forEach(function (k) { rings[k] = A.circle(P[k][0], P[k][1], 0, 'f-none s-gold w2'); });
      K.forEach(function (k) { nodes[k] = node(A, P[k][0], P[k][1], k, k === 'S' || k === 'D' ? 'f-acc s-acc w2' : 'f-accs s-acc w2', null, 11); });
      A.set(nodes.S._t, { cls: 't-b f-card' }); A.set(nodes.D._t, { cls: 't-b f-card' });
      var rrep = A.circle(0, 0, 5, 'f-good s-card w1'), pkt = A.circle(0, 0, 5.5, 'f-acc s-card w1');
      var mode = A.text(10, 20, '', { cls: 't-b' }), cnt = A.text(390, 20, '', { cls: 't-m t-b', anchor: 'end' });
      function ring(k, t0, ts) {
        var u = (ts - t0) / 0.8;
        if (u < 0 || u > 1) return false;
        A.set(rings[k], { r: 12 + 22 * u }); op(rings[k], 1 - u); return true;
      }
      function flood(hmap, t0, ts, dh) {  // RREQ: node at hop h rebroadcasts at t0 + dh·h ; D only receives
        var n = 0;
        K.forEach(function (k) {
          var h = hmap[k], tk = t0 + dh * h;
          var lit = ts >= tk;
          A.set(nodes[k]._c, { cls: lit && k !== 'S' && k !== 'D' ? 'f-golds s-gold w2' : (k === 'S' || k === 'D' ? 'f-acc s-acc w2' : 'f-accs s-acc w2') });
          if (k !== 'D' && lit) { n++; ring(k, tk, ts); }
        });
        return n;
      }
      return {
        frame: function (ts, dt, k) {
          K.forEach(function (n) { op(rings[n], 0); A.set(nodes[n]._c, { cls: n === 'S' || n === 'D' ? 'f-acc s-acc w2' : 'f-accs s-acc w2' }); });
          var broken = k === 5 && ts > 0.3;
          cls(linkEl['e,D'], broken ? 's-bad w2 dash' : 's-line w2'); op(brk, broken ? 1 : 0);
          op(rrep, 0); op(pkt, 0);
          r1.forEach(function (l) { op(l, 0); }); r2.forEach(function (l) { op(l, 0); });
          var count = 0, pk = null;
          if (k <= 1) {
            st(A, mode, '周期性（表驱动）');
            var rounds = k === 0 ? Math.min(3, Math.floor(ts / 1.2) + 1) : 4;
            if (k === 1 && ts < 1.2) rounds = 3;
            var tr = k === 0 ? (rounds - 1) * 1.2 : 1.2;
            if (k === 0 || ts >= 1.2) K.forEach(function (n) { ring(n, tr, ts); });
            count = rounds * K.length;
            if (k === 1) { r1.forEach(function (l) { op(l, 1); }); pk = A.prog(ts, 2, 0.2) < 1 && along(path1.map(function (n) { return P[n]; }), A.prog(ts, 2, 0.2)); }
          } else if (k <= 4) {
            st(A, mode, '按需（on-demand）');
            if (k === 2) count = flood(h1, 0.3, ts, 0.6);
            else {
              count = nRREQ1;
              var back = path1.slice().reverse().map(function (n) { return P[n]; }), nh = path1.length - 1;
              if (k === 3) {
                var u = A.prog(ts, 0.7 * nh, 0.3);
                var q = along(back, u); A.set(rrep, { cx: q[0], cy: q[1] }); op(rrep, ts > 0.3 && u < 1 ? 1 : 0);
                count += Math.min(nh, Math.floor(u * nh + 1e-6));
                r1.forEach(function (l, i) { op(l, u * nh >= nh - i ? 1 : 0); });
              } else {
                count += nh;
                r1.forEach(function (l) { op(l, 1); });
                pk = A.prog(ts, 2, 0.3) < 1 && along(path1.map(function (n) { return P[n]; }), A.prog(ts, 2, 0.3));
              }
            }
          } else {
            st(A, mode, '按需：路由重构');
            count = nRREQ1 + path1.length - 1;
            if (ts > 0.6) count += flood(h2, 0.6, ts, 0.45);
            var nh2 = path2.length - 1, t2 = 0.6 + 0.45 * h2.D + 0.2;
            var u2 = A.prog(ts, 0.25 * nh2, t2);
            count += ts > t2 ? Math.min(nh2, Math.floor(u2 * nh2 + 1e-6)) : 0;
            r2.forEach(function (l, i) { op(l, u2 * nh2 >= nh2 - i ? 1 : 0); });
            var u3 = A.prog(ts, 1.2, t2 + 0.25 * nh2 + 0.1);
            if (u2 >= 1 && u3 < 1) pk = along(path2.map(function (n) { return P[n]; }), u3);
          }
          st(A, cnt, '控制消息：' + count);
          if (pk) { A.set(pkt, { cx: pk[0], cy: pk[1] }); op(pkt, 1); }
        }
      };
    }
  });

  /* =====================================================================
     Chapter 5  wireless sensor networks
     ===================================================================== */

  ANIM.reg('B:5.1', {
    title: '传感器网络 vs 一般自组网',
    cap: '左右对比讲义 p.56 的四点不同：数量、部署与可靠性、通信方式、资源。节点个数只是示意（真实传感网可多几个数量级）。',
    h: 235, live: true, stepDur: 3.8, seed: 5,
    steps: [
      '节点数量：传感器网络的节点比一般自组网多几个数量级，而且每个都很小、很便宜。',
      '部署与可靠性：传感器密集部署，经常失效（红点），所以拓扑变化非常频繁；自组网相对稳定。',
      '通信方式：自组网多是点对点；传感器多用广播，“谁在附近谁收到”（金色圈内都收到）。',
      '资源：传感器的电量、计算能力、内存都很有限，撒出去后很难换电池，所以协议要省电。'
    ],
    init: function (A) {
      A.rect(8, 28, 186, 148, 'f-card s-line w1', null, 8);
      A.rect(206, 28, 186, 148, 'f-card s-line w1', null, 8);
      A.text(101, 19, '一般自组网 MANET', { cls: 't-b', anchor: 'middle' });
      A.text(299, 19, '传感器网络 WSN', { cls: 't-b', anchor: 'middle' });
      var LP = [[40, 60], [95, 52], [150, 72], [50, 130], [110, 112], [160, 140]];
      var lg = A.g();
      [[0, 1], [1, 2], [0, 3], [1, 4], [3, 4], [4, 5], [2, 5]].forEach(function (e) { A.line(LP[e[0]][0], LP[e[0]][1], LP[e[1]][0], LP[e[1]][1], 's-line w2', lg); });
      LP.forEach(function (p) { A.circle(p[0], p[1], 9, 'f-accs s-acc w2', lg); });
      var uni = A.circle(0, 0, 4.5, 'f-gold s-card w1');
      var uniA = A.arrow(LP[3][0] + 10, LP[3][1] - 4, LP[4][0] - 10, LP[4][1] + 3, 's-gold w2', null, 6);
      var RP = [], rnd = A.rng(5), rg = A.g();
      for (var i = 0; i < 70; i++) RP.push([A.lerp(216, 382, rnd()), A.lerp(38, 166, rnd())]);
      var bc = [300, 100];
      var bring = A.circle(bc[0], bc[1], 0, 'f-golds s-gold w2', rg);
      var rn = RP.map(function (p) { return A.circle(p[0], p[1], 2.8, 'f-acc s-none', rg); });
      var src = A.circle(bc[0], bc[1], 4.5, 'f-gold s-none', rg);
      var ph = RP.map(function () { return rnd() * 6.28; }), w = RP.map(function () { return 0.7 + rnd() * 1.6; });
      var bL = battery(A, 150, 150, 32, 16, 1, 'f-good'), bR = battery(A, 364, 156, 18, 9, 0.25, 'f-bad');
      var prop = A.text(200, 197, '', { cls: 't-b', anchor: 'middle' });
      var vL = A.text(101, 220, '', { cls: 't-s', anchor: 'middle' }), vR = A.text(299, 220, '', { cls: 't-s', anchor: 'middle' });
      var T = [['① 节点数量', '较少', '多几个数量级'], ['② 部署与可靠性', '相对稳定', '密集、易失效、拓扑常变'],
        ['③ 通信方式', '点对点', '广播'], ['④ 资源', '相对充裕', '电量/计算/内存都很有限']];
      return {
        frame: function (ts, dt, k) {
          st(A, prop, T[k][0]); st(A, vL, T[k][1]); st(A, vR, T[k][2]);
          rn.forEach(function (c, i) {
            var fail = k === 1 && Math.sin(ts * w[i] + ph[i]) > 0.8;
            var inR = k === 2 && dist(RP[i], bc) < 46 * ((ts % 1.6) / 1.6);
            cls(c, fail ? 'f-bad s-none' : inR ? 'f-gold s-none' : 'f-acc s-none');
            op(c, k === 0 ? c01((ts * 2.2) - i / 40) : 1);
          });
          var u = (ts % 1.6) / 1.6;
          A.set(bring, { r: k === 2 ? 46 * u : 0 }); op(bring, k === 2 ? 1 - u * 0.7 : 0); op(src, k === 2 ? 1 : 0);
          var q = along([LP[3], LP[4]], (ts % 1.4) / 1.4);
          A.set(uni, { cx: q[0], cy: q[1] }); op(uni, k === 2 ? 1 : 0); op(uniA, k === 2 ? 1 : 0);
          op(bL, k === 3 ? 1 : 0); op(bR, k === 3 ? 0.55 + 0.45 * Math.abs(Math.sin(ts * 3)) : 0);
        }
      };
    }
  });

  ANIM.reg('B:5.2', {
    title: '传感器网络的通信结构与节点组成',
    cap: '这就是真题 2025-26 S2 Q4(c) 要画的图：传感器节点 → 多跳 → sink → Internet/卫星 → 任务管理节点。最后一步是 p.58 的节点内部结构。',
    h: 250, tween: 3.4, stepDur: 4.4,
    steps: [
      '节点散布在“传感区”里，每个节点都能采集数据，也能把数据路由回 sink。',
      '某处发生事件：数据一个节点接一个节点地转发到 sink，这就是多跳（multi-hop）、无基础设施的传输。',
      'sink 再经 Internet 或卫星，把数据交给任务管理节点（task manager），用户在那里看结果。',
      '反过来，管理者也能经 sink 向传感区下发任务或查询。',
      '节点内部（p.58）：感知单元（传感器+ADC）→ 处理单元（处理器+存储）→ 收发器，电源单元给全部供电。'
    ],
    init: function (A) {
      var s1 = A.g(), s2 = A.g();
      A.rect(8, 30, 214, 190, 'f-none s-line w1 dash', s1, 10);
      A.text(16, 212, '传感区 sensor field', { cls: 't-s' }, s1);
      var NP = [[36, 150], [44, 70], [80, 110], [92, 180], [126, 58], [132, 142], [176, 100], [180, 178], [206, 52], [160, 200], [60, 196], [118, 92]];
      var chain = [0, 2, 5, 6];
      var SK = [258, 118], CL = [334, 52], TM = [334, 182];
      var nodesG = A.g({}, s1);
      var nc = NP.map(function (p) { return A.circle(p[0], p[1], 6.5, 'f-accs s-acc w2', nodesG); });
      var hopG = A.g({}, s1), hopA = [];
      var cp = chain.map(function (i) { return NP[i]; }).concat([SK]);
      for (var i = 0; i < cp.length - 1; i++) {
        var a = cp[i], b = cp[i + 1], dd = dist(a, b), ux = (b[0] - a[0]) / dd, uy = (b[1] - a[1]) / dd;
        hopA.push(A.arrow(a[0] + ux * 9, a[1] + uy * 9, b[0] - ux * (i === cp.length - 2 ? 16 : 9), b[1] - uy * (i === cp.length - 2 ? 16 : 9), 's-gold w2', hopG, 6));
      }
      var mh = A.text(108, 168, 'multi-hop', { cls: 't-s f-gold t-b t-m' }, s1);
      var ev = A.g({}, s1);
      A.circle(NP[0][0] - 16, NP[0][1] - 18, 9, 'f-bads s-bad w1', ev);
      A.text(NP[0][0] - 16, NP[0][1] - 14, '!', { cls: 't-b f-bad', anchor: 'middle' }, ev);
      var sk = node(A, SK[0], SK[1], '', 'f-gold s-gold w2', s1, 13);
      A.text(SK[0], SK[1] + 30, 'sink', { cls: 't-b t-m', anchor: 'middle' }, s1);
      A.text(SK[0], SK[1] + 44, '汇聚节点', { cls: 't-s', anchor: 'middle' }, s1);
      var cg = A.g({}, s1);
      A.path('M302 66 a14 14 0 0 1 8 -26 a18 18 0 0 1 34 -6 a14 14 0 0 1 22 18 a12 12 0 0 1 -6 22 Z', 'f-accs s-acc w1', cg);
      A.text(CL[0], 58, 'Internet', { cls: 't-s t-b', anchor: 'middle' }, cg);
      A.text(CL[0], 88, '或 卫星', { cls: 't-s', anchor: 'middle' }, cg);
      box(A, 290, 168, 88, 36, '任务管理节点', 'f-goods s-good w2', s1, 't-s t-b');
      A.text(TM[0], 218, '（用户在这里）', { cls: 't-s', anchor: 'middle' }, s1);
      var up1 = A.arrow(270, 106, 300, 76, 's-acc w2', s1, 6), up2 = A.arrow(334, 96, 334, 164, 's-acc w2', s1, 6);
      var dn = A.g({}, s1);
      A.path('M302 167 Q300 128 280 123', 's-pur w2 dash', dn);
      A.arrow(284, 124, 273, 121, 's-pur w2', dn, 6);
      var dnRing = A.circle(SK[0], SK[1], 0, 'f-none s-pur w2', s1);
      var pkt = A.circle(0, 0, 5, 'f-gold s-card w1', s1), tsk = A.circle(0, 0, 5, 'f-pur s-card w1', s1);
      // scene 2: node anatomy (p.58)
      var opt = A.g({}, s2);
      box(A, 40, 26, 140, 28, '定位系统（可选）', 'f-none s-line w1 dash', opt, 't-s');
      box(A, 220, 26, 140, 28, '移动装置（可选）', 'f-none s-line w1 dash', opt, 't-s');
      A.rect(10, 70, 126, 76, 'f-accs s-acc w1', s2, 8);
      A.text(73, 86, '感知单元', { cls: 't-b', anchor: 'middle' }, s2);
      box(A, 18, 96, 50, 40, '传感器', 'f-card s-acc w1', s2, 't-s');
      box(A, 80, 96, 48, 40, 'ADC', 'f-card s-acc w1', s2, 't-s t-b');
      A.rect(150, 70, 116, 76, 'f-golds s-gold w1', s2, 8);
      A.text(208, 86, '处理单元', { cls: 't-b', anchor: 'middle' }, s2);
      box(A, 158, 96, 50, 40, '处理器', 'f-card s-gold w1', s2, 't-s');
      box(A, 214, 96, 46, 40, '存储', 'f-card s-gold w1', s2, 't-s');
      box(A, 282, 84, 76, 50, '收发器', 'f-goods s-good w1', s2, 't-b');
      A.line(366, 109, 366, 86, 's-good w2', s2);
      var wave = A.path('', 's-good w2', s2);
      A.arrow(68, 116, 80, 116, 's-acc w2', s2, 5); A.arrow(136, 116, 150, 116, 's-ink w2', s2, 5); A.arrow(266, 116, 282, 116, 's-ink w2', s2, 5);
      box(A, 10, 176, 380, 34, '电源单元（可配发电装置，如太阳能）', 'f-paper s-soft w1', s2, 't-s t-b');
      [73, 208, 320].forEach(function (x) { A.arrow(x, 176, x, 148, 's-soft w1 dash', s2, 5); });
      var flow = A.circle(0, 0, 4.5, 'f-acc s-card w1', s2);
      A.text(200, 234, '可选部件：定位系统、移动装置（虚线框）', { cls: 't-s', anchor: 'middle' }, s2);
      return {
        frame: function (ts, dt, k) {
          op(s1, k < 4 ? 1 : 1 - A.prog(ts, 0.5)); op(s2, k === 4 ? A.prog(ts, 0.6, 0.3) : 0);
          nc.forEach(function (c, i) {
            var pulse = k === 0 ? 0.5 + 0.5 * Math.sin(ts * 6 - i) : 0;
            var onChain = (k === 1 || k === 2) && chain.indexOf(i) >= 0;
            cls(c, onChain ? 'f-golds s-gold w2' : pulse > 0.75 ? 'f-acc s-acc w2' : 'f-accs s-acc w2');
          });
          op(ev, k === 1 ? A.prog(ts, 0.3) : 0);
          var hu = k === 1 ? A.prog(ts, 2.4, 0.5) : (k >= 2 ? 1 : 0);
          hopA.forEach(function (a, i) { op(a, k >= 1 && k <= 3 ? (hu * hopA.length > i ? (k === 1 ? 1 : 0.45) : 0) : 0); });
          op(mh, k >= 1 && k <= 3 ? hu : 0);
          op(up1, k === 2 ? A.prog(ts, 0.4, 0.2) : k === 3 ? 0.3 : 0); op(up2, k === 2 ? A.prog(ts, 0.4, 1.3) : k === 3 ? 0.3 : 0);
          var p = null;
          if (k === 1 && ts > 0.5) p = along(cp, hu);
          if (k === 2) p = along([SK, CL, [334, 168]], A.prog(ts, 2.2, 0.2));
          if (p) { A.set(pkt, { cx: p[0], cy: p[1] }); op(pkt, 1); } else op(pkt, 0);
          op(dn, k === 3 ? A.prog(ts, 0.4) : 0);
          if (k === 3) {
            var q = along([[302, 167], [298, 136], [274, 121]], A.prog(ts, 1.2, 0.2));
            A.set(tsk, { cx: q[0], cy: q[1] }); op(tsk, ts > 0.2 && ts < 1.5 ? 1 : 0);
            var u = A.prog(ts, 1.4, 1.5);
            A.set(dnRing, { r: 14 + 120 * u }); op(dnRing, ts > 1.5 ? 1 - u : 0);
          } else { op(tsk, 0); op(dnRing, 0); }
          if (k === 4) {
            var fl = along([[43, 116], [104, 116], [183, 116], [237, 116], [320, 116]], A.prog(ts, 2.2, 0.7));
            A.set(flow, { cx: fl[0], cy: fl[1] }); op(flow, ts > 0.7 && ts < 3 ? 1 : 0);
            var wv = A.prog(ts, 0.8, 2.6), d = '';
            for (var r = 1; r <= 3; r++) if (wv * 3 >= r) d += 'M' + (366 + 5 * r) + ' ' + (86 - 6 * r) + ' a' + 7 * r + ' ' + 7 * r + ' 0 0 1 0 ' + 12 * r;
            A.set(wave, { d: d || 'M0 0' }); op(wave, d ? 1 : 0);
          }
        }
      };
    }
  });

  ANIM.reg('B:5.3', {
    title: '传感器网络协议栈：五层 + 三个管理平面',
    cap: '左边五层自下而上逐层点亮，右边是贯穿所有层的功率、移动、任务三个管理平面（p.59）。下方方框是讲义对这一层的要求。',
    h: 250, tween: 1.8, stepDur: 3.8,
    steps: [
      '物理层：要简单但稳健的调制、发射和接收技术（节点便宜、低功耗）。',
      'MAC（数据链路）层：必须省电（power-aware），并尽量减少和邻居广播的冲突。',
      '网络层：为传输层交下来的数据选路，把数据一跳一跳送到 sink。',
      '传输层：维持数据流。',
      '应用层：在上面构建各种不同的传感应用。',
      '三个管理平面贯穿所有层：监控各节点的电量、移动情况和任务分配。功耗是最关键的因素。'
    ],
    init: function (A) {
      var names = ['应用层', '传输层', '网络层', '数据链路层（MAC）', '物理层'];
      var req = ['在上面构建各种应用', '维持数据流', '为传输层送来的数据选路', '省电 + 减少与邻居广播的冲突', '简单但稳健的调制、发射和接收'];
      var Y = [30, 62, 94, 126, 158], LH = 28;
      var lay = names.map(function (n, i) { return box(A, 14, Y[i], 214, LH, n, 'f-card s-line w1', null, 't-b'); });
      var planes = ['功率管理平面', '移动管理平面', '任务管理平面'];
      var pl = planes.map(function (n, i) {
        var g = A.g(), x = 246 + i * 50;
        g._r = A.rect(x, 30, 42, 156, 'f-card s-line w1', g, 6);
        vtext(A, x + 21, 72, n, 't-s t-b', g);
        return g;
      });
      var pkt = A.circle(0, 0, 5, 'f-gold s-card w1');
      A.rect(14, 198, 372, 40, 'f-paper s-line w1', null, 8);
      var rq = A.text(200, 223, '', { cls: 't-b', anchor: 'middle' });
      return {
        frame: function (ts, dt, k) {
          var li = k <= 4 ? 4 - k : -1;
          lay.forEach(function (b, i) {
            var c = i === li ? 'f-accs s-acc w3' : (li >= 0 && i > li ? 'f-goods s-good w1' : 'f-card s-line w1');
            if (k === 5) c = 'f-card s-line w1';
            cls(b._r, c); op(b, k === 5 ? 0.55 : 1);
          });
          pl.forEach(function (g, i) {
            cls(g._r, k === 5 ? (i === 0 ? 'f-golds s-gold w3' : 'f-purs s-pur w2') : 'f-card s-line w1');
            op(g, k === 5 ? A.lerp(0.8, 1, A.prog(ts, 0.5, i * 0.25)) : 0.8);
          });
          st(A, rq, k === 5 ? '监控各节点的电量、移动和任务分配（功耗最关键）' : req[li]);
          if (li >= 0) {
            var y0 = Y[4] + LH / 2, y1 = Y[li] + LH / 2, u = A.prog(ts, 1.0, 0.1);
            A.set(pkt, { cx: 206, cy: A.lerp(y0, y1, u) }); op(pkt, 1);
          } else op(pkt, 0);
        }
      };
    }
  });

  /* =====================================================================
     Chapter 6  LTE
     ===================================================================== */

  ANIM.reg('B:6.1', {
    title: 'EPS = E-UTRAN + EPC',
    cap: '按讲义 p.62 的结构图重画。实线 = 用户数据（用户面），虚线 = 信令（控制面）。接口名（LTE-Uu、S1-U、S11…）都是标准化的。',
    h: 250, tween: 3, stepDur: 4.2,
    steps: [
      '目标：在终端 UE 和分组数据网 PDN 之间提供无缝的 IP 连接，用户移动时应用不中断。',
      '整个系统叫 EPS = E-UTRAN（接入网，LTE 的成果）+ EPC（核心网，SAE 的成果）。',
      'E-UTRAN 基本上只有一种节点：eNodeB，它通过无线接口 LTE-Uu 连接 UE。',
      'EPC 有多个逻辑节点。用户数据走 eNodeB → S-GW（服务网关）→ P-GW（PDN 网关）→ IP 网。',
      'MME 是核心网的控制节点，只走信令（虚线）；HSS（用户数据库）、PCRF（策略与计费规则）也在 EPC 里。',
      '各网元之间的接口都标准化（金色），所以不同厂商的设备可以互通。'
    ],
    init: function (A) {
      var shL = A.rect(2, 26, 140, 192, 'f-accs s-none', null, 8), shR = A.rect(146, 26, 252, 192, 'f-golds s-none', null, 8);
      A.line(144, 24, 144, 188, 's-soft w1 dash');
      var lbL = A.text(72, 18, 'E-UTRAN（接入网）', { cls: 't-b f-acc', anchor: 'middle' });
      var lbR = A.text(272, 18, 'EPC（核心网）', { cls: 't-b f-gold', anchor: 'middle' });
      var gU = A.g(), gE = A.g(), gD = A.g(), gC = A.g(), gI = A.g();
      var Y = 170;
      box(A, 6, Y - 15, 40, 30, 'UE', 'f-card s-acc w2', gU, 't-b');
      box(A, 70, Y - 15, 58, 30, 'eNodeB', 'f-card s-acc w2', gE, 't-b');
      A.line(46, Y, 70, Y, 's-ink w2', gE);
      A.line(128, Y, 162, Y, 's-ink w2', gD);
      box(A, 162, Y - 15, 52, 30, 'S-GW', 'f-card s-gold w2', gD, 't-b');
      A.line(214, Y, 240, Y, 's-ink w2', gD);
      box(A, 240, Y - 15, 52, 30, 'P-GW', 'f-card s-gold w2', gD, 't-b');
      A.line(292, Y, 300, Y, 's-ink w2', gD);
      A.el('ellipse', { cx: 348, cy: Y, rx: 48, ry: 23, cls: 'f-goods s-good w2' }, gD);
      A.text(348, Y - 2, '运营商 IP 业务', { cls: 't-s t-b', anchor: 'middle' }, gD);
      A.text(348, Y + 11, '（IMS、PSS…）', { cls: 't-s', anchor: 'middle' }, gD);
      box(A, 162, 88, 52, 26, 'MME', 'f-card s-pur w2', gC, 't-b');
      box(A, 232, 30, 50, 24, 'HSS', 'f-card s-pur w1', gC, 't-b');
      box(A, 282, 88, 52, 26, 'PCRF', 'f-card s-pur w1', gC, 't-b');
      A.poly([[99, Y - 15], [99, 101], [162, 101]], 's-pur w2 dash', gC);
      A.line(188, 114, 188, Y - 15, 's-pur w2 dash', gC);
      A.poly([[188, 88], [188, 42], [232, 42]], 's-pur w2 dash', gC);
      A.poly([[266, Y - 15], [266, 101], [282, 101]], 's-pur w2 dash', gC);
      A.poly([[334, 101], [366, 101], [366, Y - 22]], 's-pur w2 dash', gC);
      var IF = [['LTE-Uu', 58, Y + 30, 'middle'], ['S1-U', 145, Y + 30, 'middle'], ['S5/S8', 227, Y + 30, 'middle'], ['SGi', 296, Y + 30, 'middle'],
        ['S1-MME', 104, 95, 'start'], ['S11', 193, 140, 'start'], ['S6a', 194, 36, 'start'], ['Gx', 261, 140, 'end'], ['Rx', 371, 128, 'start']];
      var ifs = IF.map(function (f) { return A.text(f[1], f[2], f[0], { cls: 't-s t-m', anchor: f[3] }, gI); });
      A.line(12, 238, 36, 238, 's-ink w2'); A.text(40, 242, '用户数据', { cls: 't-s' });
      A.line(120, 238, 144, 238, 's-pur w2 dash'); A.text(148, 242, '信令', { cls: 't-s' });
      var pkt = A.circle(0, 0, 5, 'f-acc s-card w1'), sig = A.circle(0, 0, 4.5, 'f-pur s-card w1');
      var dataPath = [[26, Y], [99, Y], [188, Y], [266, Y], [330, Y]];
      var sigPath = [[99, Y - 15], [99, 101], [162, 101], [188, 101], [188, Y - 15]];
      return {
        frame: function (ts, dt, k) {
          var lo = 0.28;
          op(shL, k === 1 || k === 2 ? 0.9 : 0.25); op(shR, k === 1 || k >= 3 && k <= 4 ? 0.9 : 0.25);
          op(gU, k === 3 || k === 4 ? lo + 0.3 : 1);
          op(gE, 1);
          op(gD, k === 2 ? lo : 1);
          op(gC, k === 0 || k === 2 || k === 3 ? lo : 1);
          op(gI, k === 5 ? 1 : k === 0 ? 0.5 : 0.75);
          ifs.forEach(function (t) { cls(t, k === 5 ? 't-s t-m t-b f-gold' : 't-s t-m'); });
          var u = A.prog(ts, 2.2, 0.3);
          if (k === 0 || k === 3) { var q = along(dataPath, u); A.set(pkt, { cx: q[0], cy: q[1] }); op(pkt, u < 1 ? 1 : 0); }
          else if (k === 2) { var q2 = along([[26, Y], [99, Y]], A.prog(ts, 1, 0.3)); A.set(pkt, { cx: q2[0], cy: q2[1] }); op(pkt, A.prog(ts, 1, 0.3) < 1 ? 1 : 0); }
          else op(pkt, 0);
          if (k === 4) { var s = along(sigPath, u); A.set(sig, { cx: s[0], cy: s[1] }); op(sig, u < 1 ? 1 : 0); } else op(sig, 0);
          cls(lbL, 't-b f-acc'); cls(lbR, 't-b f-gold');
        }
      };
    }
  });

  ANIM.reg('B:6.2', {
    title: '扁平化接入网：撤掉 RNC',
    cap: '对比 2G/3G 的“基站 → 集中控制器 → 核心网”和 LTE 的“eNodeB → EPC”。X2 连 eNodeB 与 eNodeB，S1 连 eNodeB 与 EPC（S1-MME 走信令，S1-U 走用户数据）。',
    h: 255, tween: 2.6, stepDur: 4.2,
    steps: [
      '2G/3G：基站上面还有一个集中控制器（BSC/RNC），它管无线控制，再往上才是核心网。',
      'LTE 撤掉了这个中间层：所有无线控制功能都集成进 eNodeB，所以叫“扁平化”。',
      'eNodeB 之间用 X2 接口直接相连，邻站之间直接沟通，不用经过中心。',
      'S1 接口连到 EPC：S1-MME 到 MME（信令，虚线），S1-U 到 S-GW（用户数据，实线）。',
      'E-UTRAN 负责所有和无线有关的功能：无线资源管理、IP 包头压缩、安全（空口加密）、连接 EPC。'
    ],
    init: function (A) {
      var BX = [80, 200, 320], BY = 140;
      var core = box(A, 150, 18, 100, 28, '核心网', 'f-golds s-gold w2', null, 't-b');
      var epcBox = A.rect(64, 10, 272, 44, 'f-none s-gold w1 dash', null, 8);
      var epcT = A.text(200, 64, 'EPC', { cls: 't-s t-b f-gold', anchor: 'middle' });
      var mme = box(A, 76, 18, 80, 28, 'MME', 'f-card s-pur w2', null, 't-b');
      var sgw = box(A, 244, 18, 80, 28, 'S-GW', 'f-card s-gold w2', null, 't-b');
      var rnc = box(A, 160, 80, 80, 26, 'BSC/RNC', 'f-bads s-bad w2', null, 't-b');
      var rncX = A.g();
      A.line(150, 74, 250, 112, 's-bad w3', rncX); A.line(250, 74, 150, 112, 's-bad w3', rncX);
      var old = A.g();
      BX.forEach(function (x) { A.line(x, BY - 13, 200, 106, 's-soft w2', old); });
      A.line(200, 80, 200, 46, 's-soft w2', old);
      var direct = A.g();
      BX.forEach(function (x) { A.line(x, BY - 13, 200, 46, 's-acc w2', direct); });
      var s1 = A.g();
      BX.forEach(function (x) { A.line(x - 6, BY - 13, 116, 46, 's-pur w2 dash', s1); A.line(x + 6, BY - 13, 284, 46, 's-acc w2', s1); });
      var s1t = A.g();
      A.text(40, 96, 'S1-MME', { cls: 't-s t-m f-pur t-b' }, s1t);
      A.text(360, 96, 'S1-U', { cls: 't-s t-m f-acc t-b', anchor: 'end' }, s1t);
      var x2 = A.g();
      A.line(115, BY, 165, BY, 's-good w3', x2); A.line(235, BY, 285, BY, 's-good w3', x2);
      A.text(140, BY - 5, 'X2', { cls: 't-s t-m t-b f-good', anchor: 'middle' }, x2);
      A.text(260, BY - 5, 'X2', { cls: 't-s t-m t-b f-good', anchor: 'middle' }, x2);
      var bs = BX.map(function (x) { return box(A, x - 35, BY - 13, 70, 26, 'NodeB', 'f-card s-acc w2', null, 't-b'); });
      BX.forEach(function (x) {
        A.rect(x - 5, 176, 10, 16, 'f-card s-soft w1', null, 2);
        A.line(x, 174, x, 154, 's-faint w1 dash');
      });
      A.text(358, 190, 'UE', { cls: 't-s' });
      var fn = A.g();
      A.rect(10, 202, 380, 48, 'f-card s-acc w1', fn, 8);
      ['无线资源管理（调度、接纳、移动性）', 'IP 包头压缩', '安全：空口数据全部加密', '连接 EPC（MME 信令、S-GW 承载）'].forEach(function (s, i) {
        A.text(i % 2 ? 210 : 20, 221 + Math.floor(i / 2) * 19, '• ' + s, { cls: 't-s' }, fn);
      });
      var m1 = A.circle(0, 0, 4.5, 'f-good s-card w1'), m2 = A.circle(0, 0, 4.5, 'f-pur s-card w1'), m3 = A.circle(0, 0, 4.5, 'f-acc s-card w1');
      return {
        frame: function (ts, dt, k) {
          var u = A.prog(ts, 0.8, 0.2);
          op(rnc, k === 0 ? 1 : k === 1 ? 1 - u : 0); op(rncX, k === 1 ? Math.min(u * 2, 1 - A.prog(ts, 0.6, 1.4)) : 0);
          op(old, k === 0 ? 1 : k === 1 ? 1 - u : 0);
          op(direct, k === 1 || k === 2 ? (k === 1 ? A.prog(ts, 0.6, 0.9) : 1) : 0);
          op(core, k <= 2 ? 1 : 0); st(A, core._t[0], k === 0 ? '核心网' : 'EPC');
          op(mme, k >= 3 ? 1 : 0); op(sgw, k >= 3 ? 1 : 0); op(epcBox, k >= 3 ? 1 : 0); op(epcT, k >= 3 ? 1 : 0);
          op(s1, k >= 3 ? (k === 3 ? A.prog(ts, 0.6) : 0.6) : 0); op(s1t, k === 3 ? 1 : 0);
          op(x2, k === 2 ? A.prog(ts, 0.6) : k > 2 ? 0.6 : 0);
          bs.forEach(function (b) { st(A, b._t[0], k === 0 ? 'BTS/NodeB' : 'eNodeB'); cls(b._r, k === 1 && ts > 0.9 ? 'f-accs s-acc w3' : 'f-card s-acc w2'); });
          op(fn, k === 4 ? A.prog(ts, 0.6) : 0);
          op(m1, 0); op(m2, 0); op(m3, 0);
          if (k === 2) { var p = along([[115, BY], [165, BY]], (ts % 1.2) / 1.2); A.set(m1, { cx: p[0], cy: p[1] }); op(m1, 1); }
          if (k === 3) {
            var v = A.prog(ts, 1.6, 0.6);
            var a = along([[194, BY - 13], [116, 46]], v), b = along([[206, BY - 13], [284, 46]], v);
            A.set(m2, { cx: a[0], cy: a[1] }); A.set(m3, { cx: b[0], cy: b[1] }); op(m2, v < 1 ? 1 : 0); op(m3, v < 1 ? 1 : 0);
          }
        }
      };
    }
  });

  ANIM.reg('B:6.3', {
    title: 'E-UTRA 的四个主要指标（p.65）',
    cap: '四行依次点亮：带宽、峰值速率、移动性、覆盖。条形按数值比例画（覆盖一行是对数刻度）。',
    h: 262, tween: 2, stepDur: 4,
    steps: [
      '带宽可伸缩：1.4 MHz 到 20 MHz 之间灵活选择（1G 每个信道的带宽是固定的）。',
      '峰值速率：下行用 4×4 MIMO 时超过 300 Mbps；上行最高可达 86 Mbps。',
      '移动性：针对 15 km/h 以下的低速优化，最高支持 350 km/h，甚至 500 km/h。',
      '覆盖可伸缩：从毫微微小区（femtocell）一直到半径 100 km 的大小区。'
    ],
    init: function (A) {
      var X0 = 92, XW = 288, rows = [], g;
      function row(i, title) { g = A.g(); A.text(10, 24 + i * 62, title, { cls: 't-b' }, g); rows.push(g); return g; }
      // 1 bandwidth
      row(0, '① 带宽');
      var bwX = function (v) { return X0 + v / 20 * XW; };
      A.line(X0, 48, X0 + XW, 48, 's-line w1', g);
      var bwBar = A.rect(X0, 36, 0, 10, 'f-acc s-none', g, 2);
      A.text(bwX(1.4), 62, '1.4', { cls: 't-s t-m', anchor: 'middle' }, g);
      A.text(bwX(20), 62, '20 MHz', { cls: 't-s t-m', anchor: 'end' }, g);
      var bwT = A.text(X0 + XW, 24, '', { cls: 't-s t-m t-b f-acc', anchor: 'end' }, g);
      // 2 peak rate
      row(1, '② 峰值速率');
      var rX = function (v) { return X0 + v / 350 * XW; };
      A.text(X0 - 6, 104, '下行', { cls: 't-s', anchor: 'end' }, g);
      A.text(X0 - 6, 121, '上行', { cls: 't-s', anchor: 'end' }, g);
      var dl = A.rect(X0, 95, 0, 11, 'f-acc s-none', g, 2), ul = A.rect(X0, 112, 0, 11, 'f-gold s-none', g, 2);
      var dlA = A.arrow(rX(300), 100.5, rX(335), 100.5, 's-acc w2', g, 6);
      var dlT = A.text(X0 + XW, 88, '下行 > 300 Mbps（4×4 MIMO）', { cls: 't-s t-b f-acc', anchor: 'end' }, g);
      var ulT = A.text(rX(86) + 5, 121, '86 Mbps', { cls: 't-s t-b' }, g);
      // 3 mobility
      row(2, '③ 移动性');
      var vX = function (v) { return X0 + v / 500 * XW; };
      A.line(X0, 172, X0 + XW, 172, 's-line w1', g);
      var mv1 = A.rect(X0, 160, vX(15) - X0, 12, 'f-good s-none', g, 1);
      var mv2 = A.rect(vX(15), 162, vX(350) - vX(15), 8, 'f-gold s-none', g, 1);
      var mv3 = A.rect(vX(350), 164, vX(500) - vX(350), 4, 'f-golds s-gold w1 dash', g, 1);
      A.text(vX(15), 186, '15', { cls: 't-s t-m f-good', anchor: 'middle' }, g);
      A.text(vX(350), 186, '350', { cls: 't-s t-m', anchor: 'middle' }, g);
      A.text(vX(500), 186, '500 km/h', { cls: 't-s t-m', anchor: 'end' }, g);
      var car = A.circle(X0, 166, 5, 'f-ink s-card w1', g);
      A.text(X0 + 30, 155, '≤15 km/h 优化', { cls: 't-s f-good' }, g);
      A.text(vX(350), 155, '支持 350，甚至 500', { cls: 't-s', anchor: 'end' }, g);
      // 4 coverage (log scale 10 m … 100 km)
      row(3, '④ 覆盖');
      var cX = function (m) { return X0 + (Math.log10(m) - 1) / 4 * XW; };
      A.line(X0, 234, X0 + XW, 234, 's-soft w1', g);
      [[1e3, '1 km'], [1e4, '10 km'], [1e5, '100 km']].forEach(function (t) {
        A.line(cX(t[0]), 230, cX(t[0]), 238, 's-soft w1', g);
        A.text(cX(t[0]), 250, t[1], { cls: 't-s t-m', anchor: t[0] === 1e5 ? 'end' : 'middle' }, g);
      });
      var cov = A.rect(X0, 226, 0, 8, 'f-acc s-none', g, 2);
      A.circle(X0 + 4, 230, 4, 'f-gold s-none', g);
      A.text(X0 - 6, 250, 'femtocell', { cls: 't-s t-m', anchor: 'start' }, g);
      A.text(X0 + 40, 220, '毫微微小区 → 100 km 大小区', { cls: 't-s' }, g);
      return {
        frame: function (ts, dt, k) {
          rows.forEach(function (r, i) { op(r, i === k ? 1 : i < k ? 0.6 : 0.18); });
          var u = k === 0 ? A.prog(ts, 1.4, 0.2) : 1;
          var bw = k === 0 ? (u < 0.5 ? 1.4 : A.lerp(1.4, 20, (u - 0.5) * 2)) : 20;
          if (k === 0 && u < 0.5) bw = 1.4;
          A.set(bwBar, { width: bwX(bw) - X0 });
          st(A, bwT, k === 0 && u < 0.5 ? '最窄 1.4 MHz' : u >= 1 || k > 0 ? '最宽 20 MHz' : '');
          var v = k === 1 ? A.prog(ts, 1.2, 0.2) : (k > 1 ? 1 : 0);
          A.set(dl, { width: (rX(300) - X0) * v }); A.set(ul, { width: (rX(86) - X0) * v });
          op(dlA, v >= 1 ? 1 : 0); op(dlT, v >= 1 ? 1 : 0); op(ulT, v >= 1 ? 1 : 0);
          var w = k === 2 ? A.prog(ts, 1.6, 0.2) : (k > 2 ? 1 : 0);
          A.set(car, { cx: X0 + (vX(500) - X0) * w });
          op(mv1, 1); op(mv2, 1); op(mv3, 1);
          A.set(cov, { width: (cX(1e5) - X0) * (k === 3 ? A.prog(ts, 1.4, 0.2) : (k > 3 ? 1 : 0)) });
        }
      };
    }
  });

  ANIM.reg('B:6.4', {
    title: 'LTE 帧结构与资源网格',
    cap: '从 10 ms 的无线帧一路放大到一个资源单元 RE。切换“扩展 CP”看看一个时隙从 7 个符号变成 6 个时，RE 数怎样变。',
    h: 262, tween: 2.8, stepDur: 4.6,
    steps: [
      'FDD：一个无线帧 10 ms，分成 10 个子帧，每个子帧 1 ms。',
      '每个子帧分 2 个时隙，每个 0.5 ms，所以一帧有 10 × 2 = 20 个时隙。',
      '放大一个时隙：时间上 7 个 OFDM 符号（常规 CP），频率上 12 个子载波，合起来是 1 个资源块 RB。',
      '最小的格子叫资源单元 RE（1 个符号 × 1 个子载波）。一个 RB 有 12 × 7 = 84 个 RE。',
      '一个子帧 = 2 个时隙，所以一个子帧里的一列 RB 有 84 × 2 = 168 个 RE。',
      'TDD：两个 5 ms 半帧；第一个半帧 = 4 个普通子帧 + 1 个特殊子帧（DwPTS+GP+UpPTS）。',
      '课外验算：每个流约 100.8 Mbps，4×4 MIMO 四个流约 403 Mbps，扣开销后 > 300 Mbps。'
    ],
    init: function (A) {
      var NS = 7;
      var FX = 20, FW = 360, SW = FW / 10;
      var top = A.g(), sf = [];
      for (var i = 0; i < 10; i++) sf.push(A.rect(FX + i * SW, 26, SW, 22, 'f-card s-soft w1', top, 0));
      var sfn = [];
      for (i = 0; i < 10; i++) sfn.push(A.text(FX + i * SW + SW / 2, 41, String(i), { cls: 't-s t-m', anchor: 'middle' }, top));
      var spec = A.g({}, top);
      [0, 1].forEach(function (h) {
        var x = FX + (1 + 5 * h) * SW;
        A.rect(x, 26, SW * 0.4, 22, 'f-accs s-acc w1', spec, 0); A.rect(x + SW * 0.4, 26, SW * 0.25, 22, 'f-paper s-soft w1', spec, 0); A.rect(x + SW * 0.65, 26, SW * 0.35, 22, 'f-golds s-gold w1', spec, 0);
      });
      var spec2 = A.rect(FX + 6 * SW, 26, SW, 22, 'f-none s-bad w2 dash', top, 0);
      var frT = A.text(200, 16, '', { cls: 't-s t-b', anchor: 'middle' }, top);
      var bra = A.text(FX + SW / 2, 62, '1 ms', { cls: 't-s t-m', anchor: 'middle' }, top);
      var tdd = A.g();
      A.text(FX + 2.5 * SW, 62, '半帧 5 ms', { cls: 't-s', anchor: 'middle' }, tdd);
      A.text(FX + 7.5 * SW, 62, '半帧 5 ms', { cls: 't-s', anchor: 'middle' }, tdd);
      A.line(FX + 5 * SW, 22, FX + 5 * SW, 52, 's-ink w3', tdd);
      A.text(FX + 1.5 * SW, 80, '特殊子帧：DwPTS | GP | UpPTS = 1 ms', { cls: 't-s f-acc t-b', anchor: 'start' }, tdd);
      A.text(FX + 6.5 * SW, 98, '第二个特殊子帧：看 5 ms 还是 10 ms 周期', { cls: 't-s f-bad', anchor: 'middle' }, tdd);
      var slots = A.g();
      A.line(FX, 48, FX, 72, 's-faint w1 dash', slots); A.line(FX + SW, 48, 220, 72, 's-faint w1 dash', slots);
      var sl0 = A.rect(FX, 72, 100, 20, 'f-accs s-acc w2', slots, 0), sl1 = A.rect(FX + 100, 72, 100, 20, 'f-card s-acc w1', slots, 0);
      A.text(FX + 50, 86, '时隙 0.5 ms', { cls: 't-s', anchor: 'middle' }, slots);
      A.text(FX + 150, 86, '时隙 0.5 ms', { cls: 't-s', anchor: 'middle' }, slots);
      var slT = A.text(232, 86, '一帧 10 × 2 = 20 个时隙', { cls: 't-s t-b', anchor: 'start' }, slots);
      var GX = 60, GY = 112, GH = 120, CH = GH / 12, GW = 154;
      var grid = A.g(), cells = [];
      for (var r = 0; r < 12; r++) for (var c = 0; c < 14; c++) cells.push({ r: r, c: c, el: A.rect(0, GY + r * CH, 1, CH, 'f-card s-soft w1', grid, 0) });
      var mid = A.line(0, GY - 3, 0, GY + GH + 3, 's-ink w3', grid);
      var zoom = A.g();
      A.line(FX, 92, GX, GY, 's-faint w1 dash', zoom); A.line(FX + 100, 92, GX + GW, GY, 's-faint w1 dash', zoom);
      var ax = A.g({}, grid);
      A.set(A.text(46, GY + GH / 2, '频率：12 个子载波', { cls: 't-s', anchor: 'middle' }, ax), { transform: 'rotate(-90 46 ' + (GY + GH / 2) + ')' });
      var tx = A.text(GX + GW / 2, GY + GH + 15, '', { cls: 't-s', anchor: 'middle' }, ax);
      var info = A.g({}, grid), I1 = A.text(232, 140, '', { cls: 't-b' }, info), I2 = A.text(232, 162, '', { cls: 't-s t-m' }, info),
        I3 = A.text(232, 184, '', { cls: 't-s t-m' }, info), I4 = A.text(232, 206, '', { cls: 't-s' }, info);
      var calc = A.g(), cl = [];
      for (i = 0; i < 5; i++) cl.push(A.text(20, 128 + i * 24, '', { cls: i === 4 ? 't-b f-good' : 't-m', anchor: 'start' }, calc));
      A.choice({ label: '循环前缀', options: ['常规 CP（7 个符号）', '扩展 CP（6 个符号）'], value: 0, on: function (v) { NS = v ? 6 : 7; A.redraw(); } });
      return {
        frame: function (ts, dt, k) {
          var re = 12 * NS, re2 = 2 * re;
          op(top, 1);
          st(A, frT, k === 5 ? 'TDD 无线帧 10 ms' : '无线帧 10 ms（FDD）');
          sf.forEach(function (e, i) { op(e, k === 0 ? A.prog(ts, 0.3, i * 0.12) : 1); cls(e, k >= 1 && k <= 4 && i === 0 ? 'f-accs s-acc w2' : 'f-card s-soft w1'); });
          sfn.forEach(function (e, i) { op(e, k === 0 ? A.prog(ts, 0.3, i * 0.12) : (k === 5 && (i === 1 || i === 6) ? 0 : 1)); });
          op(spec, k === 5 ? A.prog(ts, 0.5, 0.4) : 0); op(spec2, k === 5 ? A.prog(ts, 0.5, 1.2) : 0); op(tdd, k === 5 ? A.prog(ts, 0.5, 0.2) : 0);
          op(bra, k <= 4 ? 1 : 0);
          op(slots, k >= 1 && k <= 4 ? (k === 1 ? A.prog(ts, 0.6) : 0.85) : 0);
          op(slT, k === 1 ? A.prog(ts, 0.5, 0.8) : 0);
          cls(sl1, k === 4 ? 'f-accs s-acc w2' : 'f-card s-acc w1');
          op(zoom, k >= 2 && k <= 4 ? 1 : 0);
          op(grid, k >= 2 && k <= 4 ? (k === 2 ? A.prog(ts, 0.6) : 1) : 0);
          var nc = k === 4 ? 2 * NS : NS, cw = GW / nc, filled = 0;
          if (k === 3) filled = Math.floor(A.prog(ts, 2, 0.5) * re + 1e-6);
          cells.forEach(function (o) {
            var col = o.c, show = (k === 4 ? col < 2 * NS : col < NS);
            if (!show) { op(o.el, 0); return; }
            A.set(o.el, { x: GX + col * cw, width: cw });
            var idx = col * 12 + (11 - o.r);
            var cc = 'f-card s-soft w1';
            if (k === 3 && idx < filled) cc = 'f-accs s-soft w1';
            if (k === 3 && o.r === 11 && col === 0) cc = 'f-gold s-soft w1';
            if (k === 4) cc = col < NS ? 'f-accs s-soft w1' : 'f-goods s-soft w1';
            cls(o.el, cc); op(o.el, 1);
          });
          A.set(mid, { x1: GX + NS * cw, x2: GX + NS * cw }); op(mid, k === 4 ? 1 : 0);
          st(A, tx, k === 4 ? '2 个时隙 × ' + NS + ' 个符号 = 1 ms 子帧' : '时间：' + NS + ' 个 OFDM 符号（' + (NS === 7 ? '常规' : '扩展') + ' CP）');
          st(A, I1, k === 2 ? '1 个资源块 RB' : k === 3 ? 'RE 数：' + (filled >= re ? re : filled) : '一个子帧一列 RB');
          st(A, I2, k === 2 ? '= 1 时隙 × 12 子载波' : k === 3 ? '12 × ' + NS + ' = ' + re + ' RE' : re + ' × 2 = ' + re2 + ' RE');
          st(A, I3, k === 3 ? '金色格 = 1 个 RE' : k === 2 ? '0.5 ms × 12 子载波' : '');
          st(A, I4, k === 3 ? '(1 符号 × 1 子载波)' : '');
          op(I3, k === 3 ? A.prog(ts, 0.4) : 1);
          op(calc, k === 6 ? A.prog(ts, 0.5) : 0);
          if (k === 6) {
            var nRB = 100, perMs = nRB * 168, bits = 6, perStream = perMs * bits / 1e3, streams = 4;
            var L = ['20 MHz：100 个 RB（子载波间隔 15 kHz，课外）',
              '每 1 ms：' + nRB + ' × 168 = ' + perMs.toLocaleString('en-US') + ' 个 RE（常规 CP）',
              '× ' + bits + ' bit（64-QAM）= ' + A.fmt(perStream, 4) + ' Mbps / 每个流',
              '× ' + streams + ' 个流（4×4 MIMO）≈ ' + Math.round(perStream * streams) + ' Mbps',
              '扣掉参考信号、控制信道、编码 → 讲义的“> 300 Mbps”'];
            cl.forEach(function (e, i) { st(A, e, L[i]); op(e, A.prog(ts, 0.4, 0.3 + i * 0.5)); });
          }
        }
      };
    }
  });

  ANIM.reg('B:6.5', {
    title: 'QoS：承载、QCI 与 ARP',
    cap: '按页面例题：一部手机同时刷网页、打 VoLTE 电话。每根“管道”是一条承载；括号里是讲义 p.72 表中的优先级（数字越小越优先）。',
    h: 262, tween: 2.6, stepDur: 4.8, live: true,
    steps: [
      '承载（bearer）= 网关和 UE 之间一条有特定 QoS 的 IP 分组流，是一条逻辑连接。',
      'UE 一接入就建立默认承载，必须是 non-GBR。刷网页走它（QCI 8 或 9，优先级 8/9）。',
      '拨 VoLTE 电话先要呼叫信令：IMS 信令 QCI 5，non-GBR，但优先级最高（1）。',
      '通话建专用 GBR 承载 QCI 1（100 ms、丢包 10⁻²）：永久预留 GBR，资源富余时可到 MBR。',
      'eNodeB 按 QCI 调度：优先级数字越小越先发，QCI 5（1）→ QCI 1（2）→ QCI 8/9（8/9）。',
      '小区拥塞时由 ARP 决定：新承载接不接纳、能不能抢占低 ARP 的承载。建好以后转发只看 QCI、GBR、MBR。'
    ],
    init: function (A) {
      box(A, 6, 40, 46, 160, 'UE', 'f-card s-acc w2', null, 't-b');
      box(A, 340, 40, 54, 160, '网关\nP-GW', 'f-card s-gold w2', null, 't-b');
      var enb = A.g();
      A.rect(68, 34, 46, 172, 'f-none s-soft w1 dash', enb, 6);
      A.text(91, 28, 'eNodeB 调度', { cls: 't-s t-b', anchor: 'middle' }, enb);
      var PY = [72, 120, 168], pipes = [], lbl = [], pk = [];
      var names = ['默认承载 · non-GBR · QCI 8/9（8/9）', 'IMS 信令 · non-GBR · QCI 5（1）', '专用承载 · GBR · QCI 1（2）'];
      var pcls = ['f-accs s-acc w1', 'f-purs s-pur w1', 'f-goods s-good w2'];
      PY.forEach(function (y, i) {
        var g = A.g();
        A.rect(54, y - 13, 284, 26, pcls[i], g, 13);
        lbl.push(A.text(334, y - 17, names[i], { cls: 't-s t-b', anchor: 'end' }, g));
        pipes.push(g);
      });
      var gbrBand = A.rect(56, PY[2] - 5, 280, 10, 'f-good s-none', pipes[2], 5);
      A.text(334, PY[2] + 26, '深绿 = 保证的 GBR；外管 = 上限 MBR', { cls: 't-s f-good', anchor: 'end' }, pipes[2]);
      for (var i = 0; i < 9; i++) pk.push(A.rect(0, 0, 10, 8, ['f-acc', 'f-pur', 'f-good'][i % 3] + ' s-card w1', null, 2));
      var badge = PY.map(function (y, i) { return A.text(91, y + 4, '', { cls: 't-b t-m f-gold', anchor: 'middle' }); });
      var arp = A.g();
      A.rect(54, 214, 130, 38, 'f-golds s-gold w2', arp, 8);
      A.text(119, 230, '新承载请求', { cls: 't-s t-b', anchor: 'middle' }, arp);
      A.text(119, 245, 'ARP 高', { cls: 't-s t-m', anchor: 'middle' }, arp);
      var vic = A.g({}, arp);
      A.rect(208, 214, 130, 38, 'f-bads s-bad w2', vic, 8);
      A.text(273, 230, '别人的已有承载', { cls: 't-s t-b', anchor: 'middle' }, vic);
      A.text(273, 245, 'ARP 低 → 被抢占', { cls: 't-s t-m f-bad', anchor: 'middle' }, vic);
      var arpA = A.arrow(186, 233, 206, 233, 's-bad w2', arp, 6);
      return {
        frame: function (ts, dt, k) {
          op(pipes[0], k === 0 ? A.prog(ts, 0.6) : 1);
          op(pipes[1], k < 2 ? 0 : k === 2 ? A.prog(ts, 0.6) : 1);
          op(pipes[2], k < 3 ? 0 : k === 3 ? A.prog(ts, 0.6) : 1);
          st(A, lbl[0], k === 0 ? '一条承载（有自己的 QoS）' : names[0]);
          op(gbrBand, k >= 3 ? 0.55 + 0.45 * A.prog(ts, 0.8, 0.6) : 0);
          op(enb, k >= 4 ? 1 : 0.25);
          var order = ['③', '①', '②'];
          badge.forEach(function (b, i) { st(A, b, order[i]); op(b, k === 4 ? A.prog(ts, 0.4, 0.3 + [2, 0, 1][i] * 0.5) : 0); });
          op(arp, k === 5 ? A.prog(ts, 0.6) : 0); op(vic, k === 5 ? A.prog(ts, 0.5, 0.8) : 0); op(arpA, k === 5 ? A.prog(ts, 0.4, 0.8) : 0);
          var nAct = k < 2 ? 1 : k < 3 ? 2 : 3;
          pk.forEach(function (p, j) {
            var lane = j % 3, n = Math.floor(j / 3);
            if (lane >= nAct) { op(p, 0); return; }
            var speed = lane === 1 ? 0.55 : lane === 2 ? 0.45 : 0.3;
            if (k === 4) speed = [0.25, 0.6, 0.45][lane];
            var u = ((ts * speed) + n / 3) % 1;
            A.set(p, { x: A.lerp(328, 58, u), y: PY[lane] - 4 });
            op(p, 1);
          });
        }
      };
    }
  });

  /* =====================================================================
     Chapter 7  IoT
     ===================================================================== */

  ANIM.reg('B:7.1', {
    title: 'IoT 是什么：增长与五大挑战',
    cap: '第 2 步按讲义 p.80 的图（世界人口、联网设备数，单位十亿）。后五步对应真题 2025-26 S1 Q4(b) 的五个难点：可扩展性、安全、隐私、大数据与分析、互操作性。',
    h: 250, live: true, stepDur: 4.2, seed: 9,
    steps: [
      'IoT：把还没联网的东西连起来，让它们能和人、和别的物体通信，从而感知和控制物理世界。',
      '联网设备增长速度是电力和电话普及的 5 倍：2008 年前后超过世界人口，2020 年约 500 亿，人均 6–7 个。',
      '① 可扩展性：设备数以百万计，系统要撑得住；网络层可以用 IPv6 提供海量地址。',
      '② 安全：攻击面大大扩大；一台设备被攻破，就成了攻击其他设备和系统的跳板。',
      '③ 隐私：传感数据往往和个人及其活动相关（位置、健康…），怎么保护、和谁共享？',
      '④ 大数据与分析：海量、多源、多格式的数据，要及时处理才能变成有用的信息。',
      '⑤ 互操作性：协议和架构林立，有专有的也有开放的，不同厂家的设备难以互通。'
    ],
    init: function (A) {
      // scene 0: things get connected
      var s0 = A.g(), s1 = A.g(), s2 = A.g();
      var C0 = [200, 120];
      A.path('M170 136 a18 18 0 0 1 4 -34 a24 24 0 0 1 44 -6 a18 18 0 0 1 18 30 a10 10 0 0 1 -6 10 Z', 'f-accs s-acc w2', s0);
      A.text(C0[0], 124, 'Internet', { cls: 't-b', anchor: 'middle' }, s0);
      var TH = [['冰箱', 60, 50], ['汽车', 60, 120], ['水表', 60, 190], ['手表', 340, 50], ['路灯', 340, 120], ['机器', 340, 190], ['门锁', 200, 215]];
      var thL = [], thB = [];
      TH.forEach(function (t) {
        var dx = t[1] - C0[0], dy = t[2] - C0[1], f = 1 / Math.sqrt(dx * dx / (40 * 40) + dy * dy / (26 * 26));
        thL.push(A.line(t[1], t[2], C0[0] + dx * f, C0[1] + dy * f, 's-acc w2 dash', s0));
        thB.push(box(A, t[1] - 26, t[2] - 13, 52, 26, t[0], 'f-card s-soft w1', s0, 't-s t-b'));
      });
      // scene 1: growth chart (p.80)
      var ax = A.axes({ x: 48, y: 30, w: 300, h: 180, xr: [2003, 2020], yr: [0, 50], yl: '十亿', ticksX: [2003, 2008, 2010, 2015, 2020], ticksY: [10, 20, 30, 40, 50], grid: true, parent: s1, xAxisAt: 'bottom', yAxisAt: 'left' });
      var POP = [[2003, 6.307], [2008, 6.721], [2010, 6.894], [2015, 7.347], [2020, 7.83]];
      var DEV = [[2003, 0.5], [2008, 6.721], [2010, 12.5], [2015, 25], [2020, 50]];
      var popC = A.curve(ax, [], 's-acc w3', s1), devC = A.curve(ax, [], 's-good w3', s1);
      A.text(ax.X(2020) - 2, ax.Y(7.83) - 6, '世界人口 78.3 亿', { cls: 't-s f-acc t-b', anchor: 'end' }, s1);
      var g50 = A.text(ax.X(2020) - 6, ax.Y(50) + 4, '500 亿设备', { cls: 't-s f-good t-b', anchor: 'end' }, s1);
      var inf = A.g({}, s1);
      A.circle(ax.X(2008), ax.Y(6.721), 9, 'f-none s-gold w2', inf);
      A.text(ax.X(2008), ax.Y(6.721) - 14, '拐点 2008', { cls: 't-s f-gold t-b', anchor: 'middle' }, inf);
      var pp = A.text(60, 46, '', { cls: 't-s t-b' }, s1);
      function part(src, u) { // first fraction u of a polyline (in x)
        var xe = A.lerp(2003, 2020, u), out = [];
        for (var i = 0; i < src.length; i++) {
          if (src[i][0] <= xe) out.push(src[i]);
          else { var a = src[i - 1], b = src[i], f = (xe - a[0]) / (b[0] - a[0]); out.push([xe, a[1] + (b[1] - a[1]) * f]); break; }
        }
        return out;
      }
      // scene 2: challenges on one IoT system
      var chips = ['可扩展性', '安全', '隐私', '大数据', '互操作性'];
      var chipB = chips.map(function (c, i) { return box(A, 8 + i * 77, 8, 72, 22, c, 'f-card s-line w1', s2, 't-s t-b', 11); });
      var GW = [256, 130], CL = [350, 130];
      box(A, GW[0] - 26, GW[1] - 14, 52, 28, '网关', 'f-card s-soft w2', s2, 't-s t-b');
      A.path('M326 146 a14 14 0 0 1 2 -28 a18 18 0 0 1 34 -4 a14 14 0 0 1 14 24 a8 8 0 0 1 -4 8 Z', 'f-accs s-acc w2', s2);
      A.text(CL[0], 140, '云', { cls: 't-b', anchor: 'middle' }, s2);
      A.line(GW[0] + 26, GW[1], 326, GW[1], 's-soft w2', s2);
      var DP = [[40, 60], [96, 52], [150, 70], [60, 112], [118, 104], [176, 122], [40, 168], [100, 160], [160, 182], [90, 210]];
      var NB = [[0, 1], [1, 2], [0, 3], [1, 4], [3, 4], [4, 5], [2, 5], [3, 6], [4, 7], [6, 7], [7, 8], [5, 8], [7, 9]];
      var nbL = NB.map(function (e) { return A.line(DP[e[0]][0], DP[e[0]][1], DP[e[1]][0], DP[e[1]][1], 's-line w1', s2); });
      var upL = [2, 5, 8].map(function (i) { return A.line(DP[i][0], DP[i][1], GW[0] - 26, GW[1], 's-soft w1', s2); });
      var extra = A.g({}, s2), rnd = A.rng(3), EX = [];
      for (var i = 0; i < 36; i++) { var p = [A.lerp(22, 196, rnd()), A.lerp(44, 222, rnd())]; EX.push(A.circle(p[0], p[1], 2.6, 'f-acc s-none', extra)); }
      var dv = DP.map(function (p) { return A.circle(p[0], p[1], 7, 'f-accs s-acc w2', s2); });
      var tagG = A.g({}, s2), tags = DP.map(function (p, i) { return A.text(p[0], p[1] + 4, 'ABC'[i % 3], { cls: 't-xs t-b', anchor: 'middle' }, tagG); });
      var person = A.g({}, s2);
      A.circle(206, 172, 7, 'f-golds s-gold w2', person); A.path('M194 200 q12 -18 24 0', 's-gold w2', person);
      A.text(206, 216, '个人数据', { cls: 't-s f-gold', anchor: 'middle' }, person);
      var pk = [];
      for (i = 0; i < 12; i++) pk.push(A.rect(0, 0, 7, 7, 'f-acc s-none', s2, i % 3 === 0 ? 3.5 : i % 3 === 1 ? 0 : 1.5));
      var note = A.text(200, 244, '', { cls: 't-s t-b', anchor: 'middle' }, s2);
      var notes = ['设备从几十个变成几百万个 → IPv6 海量地址', '红色：一台被攻破，沿连接扩散到其他设备', '金色包 = 和个人相关的敏感数据，送到哪里、谁能看？', '多源、多格式的数据洪流涌向云端，要及时处理', 'A、B、C 三种协议：不同协议之间连不通（红虚线）'];
      var infect = [3, 0, 4, 1, 6, 7, 2, 5, 9, 8];
      return {
        frame: function (ts, dt, k) {
          op(s0, k === 0 ? 1 : 0); op(s1, k === 1 ? 1 : 0); op(s2, k >= 2 ? 1 : 0);
          if (k === 0) {
            thL.forEach(function (l, i) { op(l, A.prog(ts, 0.4, 0.3 + i * 0.35)); });
            thB.forEach(function (b, i) { cls(b._r, ts > 0.5 + i * 0.35 ? 'f-goods s-good w2' : 'f-card s-soft w1'); });
            return;
          }
          if (k === 1) {
            var u = A.prog(ts, 2.4, 0.2);
            A.setCurve(popC, ax, part(POP, u)); A.setCurve(devC, ax, part(DEV, u));
            op(inf, u > 0.35 ? 1 : 0); op(g50, u >= 1 ? 1 : 0);
            st(A, pp, u >= 1 ? '人均 ≈ 500 ÷ 78.3 ≈ ' + A.fmt(50 / 7.83, 2) + ' 个' : '');
            return;
          }
          var c = k - 2;
          chipB.forEach(function (b, i) { cls(b._r, i === c ? 'f-golds s-gold w2' : 'f-card s-line w1'); });
          st(A, note, notes[c]); cls(note, 't-s t-b ' + (c === 1 || c === 4 ? 'f-bad' : ''));
          op(extra, c === 0 ? A.prog(ts, 1.2, 0.3) : 0);
          EX.forEach(function (e, i) { op(e, c === 0 ? A.prog(ts, 0.3, 0.3 + i * 0.04) : 0); });
          var nInf = c === 1 ? Math.floor(A.clamp((ts - 0.5) / 0.35, 0, 10)) : 0;
          dv.forEach(function (d, i) {
            var bad = c === 1 && infect.indexOf(i) < nInf;
            var grp = ['f-accs s-acc w2', 'f-golds s-gold w2', 'f-purs s-pur w2'][i % 3];
            cls(d, bad ? 'f-bads s-bad w3' : c === 4 ? grp : 'f-accs s-acc w2');
          });
          op(tagG, c === 4 ? 1 : 0);
          NB.forEach(function (e, j) {
            var cross = c === 4 && e[0] % 3 !== e[1] % 3;
            cls(nbL[j], cross ? 's-bad w1 dash' : c === 1 && infect.indexOf(e[0]) < nInf && infect.indexOf(e[1]) < nInf ? 's-bad w2' : 's-line w1');
          });
          op(person, c === 2 ? 1 : 0);
          var flow = c === 2 || c === 3, np = c === 3 ? 12 : 4;
          pk.forEach(function (p, j) {
            if (!flow || j >= np) { op(p, 0); return; }
            var srcI = c === 2 ? 8 : [0, 2, 5, 8, 1, 7][j % 6];
            var sp = c === 2 ? [206, 172] : DP[srcI];
            var u = ((ts * (c === 3 ? 0.55 : 0.35)) + j / np) % 1;
            var q = along([sp, [GW[0] - 26, GW[1]], [CL[0] - 18, CL[1]]], u);
            A.set(p, { x: q[0] - 3.5, y: q[1] - 3.5 });
            cls(p, (c === 2 ? 'f-gold' : ['f-acc', 'f-good', 'f-pur'][j % 3]) + ' s-none');
            op(p, 1);
          });
        }
      };
    }
  });

  ANIM.reg('B:7.2', {
    title: 'IoT 架构：两个标准 + 简化框架',
    cap: '真题 2023-24 S2 Q4(a) 要求描述两个并行栈；2024-25 S2 Q4(b) 和 2025-26 S2 Q4(d) 两次考通信网络层的四个子层（第 4 步）。',
    h: 262, tween: 2.4, stepDur: 4.8,
    steps: [
      '两个标准：oneM2M（ETSI，2012）做通用服务层；IoTWF（2014）是 7 层模型，含边缘计算和数据存储。',
      '讲义用的简化框架：两个并行的三层栈。左边是核心 IoT 功能栈，右边是数据管理与计算栈，中间贯穿“安全”。',
      '“物”层：传感器和执行器，要适应部署环境的限制（供电、体积、移动），同时提供需要的数据。',
      '通信网络层分四个子层：接入网 → 网关与回程 → 网络传输 → IoT 网络管理。',
      '应用与分析层：处理收集到的数据，必要时反过来控制物体，并做出智能决策。',
      '数据栈管“数据在哪里处理”：边缘（设备本身）、雾（网关/路由器）、云（数据中心）。'
    ],
    init: function (A) {
      var s0 = A.g(), s1 = A.g();
      // scene 0
      A.rect(6, 8, 190, 246, 'f-card s-line w1', s0, 8);
      A.text(101, 26, 'oneM2M（ETSI，2012）', { cls: 't-b', anchor: 'middle' }, s0);
      A.rect(20, 46, 70, 70, 'f-accs s-acc w1', s0, 6);
      A.text(55, 64, '现场设备', { cls: 't-s t-b', anchor: 'middle' }, s0);
      A.rect(24, 88, 62, 22, 'f-golds s-gold w2', s0, 4);
      A.text(55, 103, '通用服务层', { cls: 't-s t-b', anchor: 'middle' }, s0);
      box(A, 116, 64, 70, 36, '应用服务器', 'f-goods s-good w1', s0, 't-s t-b');
      var m2mA = A.arrow(88, 82, 114, 82, 's-gold w2', s0, 6);
      ['关注：智能抄表、智能电网、', '智慧城市、电子健康、车联网'].forEach(function (t, i) { A.text(14, 146 + i * 17, t, { cls: 't-s' }, s0); });
      A.text(14, 196, '目标：一个通用的服务层，', { cls: 't-s' }, s0);
      A.text(14, 213, '方便设备和应用服务器通信', { cls: 't-s' }, s0);
      A.rect(204, 8, 190, 246, 'f-card s-line w1', s0, 8);
      A.text(299, 26, 'IoTWF（2014）7 层', { cls: 't-b', anchor: 'middle' }, s0);
      var L7 = ['7 协作与流程', '6 应用', '5 数据抽象', '4 数据存储', '3 边缘计算', '2 连接', '1 物理设备与控制器'];
      L7.forEach(function (n, i) {
        var hl = i >= 2 && i <= 4;
        box(A, 236, 36 + i * 24, 126, 20, n, hl ? 'f-golds s-gold w1' : 'f-paper s-line w1', s0, 't-s' + (hl ? ' t-b' : ''), 4);
      });
      A.arrow(222, 46, 222, 196, 's-pur w2', s0, 6); A.arrow(378, 196, 378, 46, 's-acc w2', s0, 6);
      A.text(212, 222, '左：控制从云流向边缘', { cls: 't-s f-pur' }, s0);
      A.text(212, 240, '右：数据从边缘向上（北向）', { cls: 't-s f-acc' }, s0);
      var m2mPk = A.circle(0, 0, 4, 'f-gold', s0);
      // scene 1: two parallel stacks (p.87)
      A.text(95, 18, '核心 IoT 功能栈', { cls: 't-b', anchor: 'middle' }, s1);
      A.text(305, 18, '数据管理与计算栈', { cls: 't-b', anchor: 'middle' }, s1);
      var LY = [28, 76, 124];
      var core = ['应用与分析', '通信网络', '物：传感器和执行器'].map(function (n, i) { return box(A, 20, LY[i], 150, 40, n, 'f-card s-line w2', s1, 't-b'); });
      var data = ['云 Cloud', '雾 Fog', '边缘 Edge'].map(function (n, i) { return box(A, 230, LY[i], 150, 40, n, 'f-card s-line w2', s1, 't-b'); });
      var sec = A.g({}, s1);
      A.arrow(200, 120, 200, 30, 's-ink w2', sec, 6); A.arrow(200, 80, 200, 164, 's-ink w2', sec, 6);
      A.rect(186, 82, 28, 36, 'f-paper s-none', sec, 3);
      A.text(200, 96, '安', { cls: 't-s t-b', anchor: 'middle' }, sec); A.text(200, 110, '全', { cls: 't-s t-b', anchor: 'middle' }, sec);
      var pairs = A.g({}, s1);
      LY.forEach(function (y) { A.line(172, y + 20, 228, y + 20, 's-gold w2 dash', pairs); });
      A.rect(10, 176, 380, 80, 'f-paper s-line w1', s1, 8);
      var dt1 = A.text(200, 200, '', { cls: 't-b', anchor: 'middle' }, s1), dt2 = A.text(200, 222, '', { cls: 't-s', anchor: 'middle' }, s1), dt3 = A.text(200, 242, '', { cls: 't-s', anchor: 'middle' }, s1);
      var subG = A.g({}, s1);
      var SUB = [['接入网', '最后一公里', '802.11ah', 'LoRa、15.4g'], ['网关与回程', '汇聚后远传', '网关一般固定', ''], ['网络传输', 'IP', 'UDP / TCP', ''], ['IoT 网络管理', '应用层协议', 'HTTP', 'WebSocket']];
      var subB = SUB.map(function (s, i) {
        var g = A.g({}, subG), x = 16 + i * 93;
        A.rect(x, 182, 88, 68, 'f-card s-acc w1', g, 6);
        A.text(x + 44, 199, s[0], { cls: 't-s t-b', anchor: 'middle' }, g);
        for (var j = 1; j <= 3; j++) if (s[j]) A.text(x + 44, 201 + j * 15, s[j], { cls: 't-s', anchor: 'middle' }, g);
        if (i < 3) A.arrow(x + 88, 216, x + 93, 216, 's-acc w1', subG, 4);
        return g;
      });
      var TXT = {
        1: ['两个并行的三层栈 + 贯穿的安全', '核心栈管“连得上、能控制”', '数据栈管“数据在哪里处理”'],
        2: ['“物”层：传感器和执行器', '适应部署环境的限制（供电、体积、移动）', '智能物体按上下文和目标自己行动'],
        4: ['应用与分析层', '处理数据、必要时控制物体', '根据信息做出智能决策'],
        5: ['边缘 → 雾 → 云：离终端越来越远', '边缘：设备本身 · 雾：网关/路由器 · 云：数据中心', '虚线：各层与核心栈对应']
      };
      return {
        frame: function (ts, dt, k) {
          op(s0, k === 0 ? 1 : 0); op(s1, k >= 1 ? (k === 1 ? A.prog(ts, 0.5) : 1) : 0);
          if (k === 0) { var q = along([[88, 82], [114, 82]], (ts % 1.2) / 1.2); A.set(m2mPk, { cx: q[0], cy: q[1] }); op(m2mA, 1); return; }
          var hc = k === 2 ? 2 : k === 3 ? 1 : k === 4 ? 0 : -1;
          core.forEach(function (b, i) { cls(b._r, i === hc ? 'f-accs s-acc w3' : k === 1 ? 'f-accs s-acc w2' : 'f-card s-line w2'); op(b, k === 5 ? 0.45 : 1); });
          data.forEach(function (b, i) { cls(b._r, k === 5 || k === 1 ? 'f-golds s-gold w' + (k === 5 ? 3 : 2) : 'f-card s-line w2'); op(b, k >= 2 && k <= 4 ? 0.45 : 1); });
          op(pairs, k === 5 ? A.prog(ts, 0.5, 0.4) : 0);
          op(sec, k === 1 ? 1 : 0.5);
          var t = TXT[k];
          op(subG, k === 3 ? 1 : 0);
          subB.forEach(function (g, i) { op(g, k === 3 ? A.prog(ts, 0.4, 0.2 + i * 0.4) : 0); });
          [dt1, dt2, dt3].forEach(function (e, i) { st(A, e, t ? t[i] : ''); op(e, t ? A.prog(ts, 0.4, 0.2 + i * 0.25) : 0); });
        }
      };
    }
  });

  ANIM.reg('B:7.3', {
    title: '第 1 层：按移动性 × 吞吐量分类',
    cap: '按讲义 p.92 的图：横轴吞吐量，纵轴移动性。会跑的点 = 高移动，包发得密 = 高吞吐。分类时还要看（p.91）：供电方式、上报频率、数据简单还是丰富、上报距离、部署密度。',
    h: 250,
    init: function (A) {
      var X0 = 34, Y0 = 8, QW = 180, QH = 112;
      A.text(X0 + QW, 246, '吞吐量：低 ←→ 高', { cls: 't-s t-b', anchor: 'middle' });
      A.set(A.text(14, Y0 + QH, '移动性：低 ←→ 高', { cls: 't-s t-b', anchor: 'middle' }), { transform: 'rotate(-90 14 ' + (Y0 + QH) + ')' });
      var Q = [
        { c: 0, r: 1, t: '低移动 · 低吞吐', e: ['泵/电机、气象传感器、', '消防安防、售货机/POS'], mob: 0, thr: 0, cls: 'f-accs' },
        { c: 1, r: 1, t: '低移动 · 高吞吐', e: ['数字广告屏、远程医疗、', '交通摄像头、联网电器'], mob: 0, thr: 1, cls: 'f-goods' },
        { c: 0, r: 0, t: '高移动 · 低吞吐', e: ['车辆远程信息、车队管理、', '战场通信'], mob: 1, thr: 0, cls: 'f-golds' },
        { c: 1, r: 0, t: '高移动 · 高吞吐', e: ['车载通信与娱乐、', '个人智能设备、视频监控'], mob: 1, thr: 1, cls: 'f-purs' }
      ];
      Q.forEach(function (q) {
        var x = X0 + q.c * (QW + 4), y = Y0 + q.r * (QH + 4);
        q.x = x; q.y = y;
        A.rect(x, y, QW, QH, q.cls + ' s-line w1', null, 8);
        A.text(x + 10, y + 18, q.t, { cls: 't-b' });
        q.e.forEach(function (s, i) { A.text(x + 10, y + 36 + i * 15, s, { cls: 't-s' }); });
        A.rect(x + QW - 32, y + 66, 22, 30, 'f-card s-soft w1', null, 3);
        A.text(x + QW - 21, y + 106, '采集', { cls: 't-xs', anchor: 'middle' });
        q.dev = A.circle(0, 0, 6, 'f-ink s-card w1');
        q.pk = [];
        for (var i = 0; i < (q.thr ? 7 : 2); i++) q.pk.push(A.rect(0, 0, 5, 5, 'f-acc s-none', null, 1));
      });
      return function (t) {
        Q.forEach(function (q) {
          var cx = q.x + 40, cy = q.y + 82;
          if (q.mob) { cx = q.x + 46 + 30 * Math.sin(t * 1.3); cy = q.y + 82 + 10 * Math.sin(t * 2.1); }
          A.set(q.dev, { cx: cx, cy: cy });
          var n = q.pk.length, per = q.thr ? 0.3 : 2.2, life = 1.1;
          q.pk.forEach(function (p, i) {
            var age = (t - i * per) % (per * n);
            if (age < 0) age += per * n;
            if (age > life) { op(p, 0); return; }
            var u = age / life, tx = q.x + QW - 21, ty = q.y + 81;
            var sx = q.mob ? q.x + 46 + 30 * Math.sin((t - age) * 1.3) : q.x + 40, sy = q.mob ? q.y + 82 + 10 * Math.sin((t - age) * 2.1) : q.y + 82;
            A.set(p, { x: A.lerp(sx, tx, u) - 2.5, y: A.lerp(sy, ty, u) - 2.5 }); op(p, 1);
          });
        });
      };
    }
  });

  ANIM.reg('B:7.4', {
    title: '第 2 层：按距离挑接入技术',
    cap: '横轴是对数刻度的通信距离（讲义 p.94–95；范围本来就不严格）。最后两步：通信网络层的四个子层（真题考过两次），以及用分类挑技术的三个练习场景。',
    h: 266, tween: 2.4, stepDur: 4.8,
    steps: [
      '选接入技术先看物体到采集点的距离（再看设备数和成本）。最近的是 NFC：< 10 cm，如刷卡 EMV。',
      'PAN 个域网几米：蓝牙、MiWi、ANT+。HAN 家域网几十米：ZigBee、Z-Wave、Thread、BLE。',
      'LAN 局域网约 100 m：802.11a/b/g/n/ac/ax、11ah、11p（车联网）、11af。',
      'FAN 几十到几百米（户外厂区）：WirelessHART 等；NAN 几百米：Wi-SUN、802.11 mesh。',
      '几公里以上：蜂窝（LTE 等，< 5 km）；LPWA：SIGFOX、LoRaWAN、NB-IoT（< 100 km）。',
      '接入网只是通信网络层的第一个子层。四个子层自下而上：接入网 → 网关与回程 → 网络传输 → IoT 网络管理。',
      '练习：城市水表（远、省电、数据少）→ LPWA；厂区振动监测 → FAN；车载娱乐（高移动高吞吐）→ 蜂窝 LTE。'
    ],
    init: function (A) {
      var XL = 30, XR = 392;
      var X = function (m) { return XL + (Math.log10(m) + 2) / 7 * (XR - XL); };
      var axG = A.g();
      A.line(XL, 40, XR, 40, 's-soft w1', axG);
      [[0.01, '1 cm'], [0.1, '10 cm'], [1, '1 m'], [10, '10 m'], [100, '100 m'], [1e3, '1 km'], [1e4, '10 km'], [1e5, '100 km']].forEach(function (t, i) {
        A.line(X(t[0]), 36, X(t[0]), 44, 's-soft w1', axG);
        A.line(X(t[0]), 44, X(t[0]), 186, 's-line w1 dash', axG);
        if (i !== 6) A.text(X(t[0]), 30, t[1], { cls: 't-s t-m', anchor: i === 0 ? 'start' : i === 7 ? 'end' : 'middle' }, axG);
      });
      A.text(XL, 14, '物体到采集点的距离（对数刻度）', { cls: 't-s t-b' }, axG);
      var CAT = [
        { n: 'NFC  < 10 cm', a: 0.01, b: 0.1, s: 0 }, { n: 'PAN 几米', a: 1, b: 10, s: 1 }, { n: 'HAN 几十米', a: 10, b: 90, s: 1 },
        { n: 'LAN 约 100 m', a: 1, b: 100, s: 2 }, { n: 'FAN 几十～几百米', a: 20, b: 800, s: 3 }, { n: 'NAN 几百米', a: 100, b: 1000, s: 3 },
        { n: '蜂窝 < 5 km', a: 1000, b: 5000, s: 4 }, { n: 'LPWA < 100 km', a: 1000, b: 1e5, s: 4 }
      ];
      var col = ['f-acc', 'f-acc', 'f-good', 'f-pur', 'f-gold', 'f-gold', 'f-bad', 'f-bad'];
      CAT.forEach(function (c, i) {
        var y = 54 + i * 16, g = A.g({}, axG);
        c.bar = A.rect(X(c.a), y, X(c.b) - X(c.a), 10, col[i] + ' s-none', g, 3);
        var right = X(c.b) < 300;
        c.txt = A.text(right ? X(c.b) + 5 : X(c.a) - 5, y + 9, c.n, { cls: 't-s t-b', anchor: right ? 'start' : 'end' }, g);
        c.g = g;
      });
      var techG = A.g();
      A.rect(10, 190, 380, 70, 'f-card s-line w1', techG, 8);
      var tl = [0, 1, 2].map(function (i) { return A.text(20, 210 + i * 19, '', { cls: 't-s' }, techG); });
      var TECH = [
        ['NFC（< 10 cm）：NFC、EMV 刷卡', '', ''],
        ['PAN（几米）：蓝牙、MiWi、ANT+', 'HAN（几十米）：ZigBee、Z-Wave、Thread、BLE', ''],
        ['LAN（约 100 m）：802.11a/b/g/n/ac/ax', '802.11ah、802.11p（车联网 V2X）、802.11af', ''],
        ['FAN（几十～几百米，户外/厂区）：', '　ISA 100.11a、WirelessHART', 'NAN（几百米）：Wi-SUN、ZigBee NAN、802.11 mesh'],
        ['蜂窝（授权，< 5 km）：LTE、GSM、WCDMA、WiMAX', 'LPWA 免授权：SIGFOX、LoRaWAN', 'LPWA 授权：NB-IoT（< 100 km）'],
        ['', '', ''],
        ['① 城市水表 → LPWA　② 厂区振动监测 → FAN', '③ 车载娱乐（高移动高吞吐）→ 蜂窝 LTE', '先按“距离×设备数×成本”定类别，再看移动性、吞吐、供电']
      ];
      var sub = A.g();
      A.rect(6, 46, 388, 214, 'f-paper s-none', sub, 8);
      var SUB = [['IoT 网络管理', 'HTTP（传感器当客户端）、WebSocket'], ['网络传输', 'IP + UDP / TCP，开放标准、可扩展'], ['网关与回程', '网关在不同介质间转发，一般固定'], ['接入网', '最后一公里：802.11ah、802.15.4g、LoRa']];
      var subB = SUB.map(function (s, i) {
        var g = A.g({}, sub), y = 54 + i * 50;
        A.rect(20, y, 360, 40, i === 3 ? 'f-accs s-acc w2' : 'f-card s-acc w1', g, 6);
        A.text(32, y + 25, s[0], { cls: 't-b' }, g);
        A.text(370, y + 25, s[1], { cls: 't-s', anchor: 'end' }, g);
        if (i < 3) A.arrow(200, y + 48, 200, y + 42, 's-acc w2', g, 5);
        return g;
      });
      var marks = A.g(), MK = [[3000, 54 + 7 * 16 - 2, '水表'], [300, 54 + 4 * 16 - 2, '振动'], [4000, 54 + 6 * 16 - 2, '车载']];
      MK.forEach(function (m, i) { A.circle(X(m[0]), m[1] + 7, 7, 'f-card s-ink w2', marks); A.text(X(m[0]), m[1] + 11, String(i + 1), { cls: 't-s t-b', anchor: 'middle' }, marks); });
      return {
        frame: function (ts, dt, k) {
          op(axG, k === 5 ? 0 : 1); op(sub, k === 5 ? A.prog(ts, 0.4) : 0);
          subB.forEach(function (g, i) { op(g, k === 5 ? A.prog(ts, 0.4, 0.2 + (3 - i) * 0.4) : 0); });
          CAT.forEach(function (c) {
            var on = k === 6 ? true : c.s === k, past = c.s < k;
            op(c.g, on ? 1 : past ? 0.45 : 0.12);
            if (on && k <= 4) A.set(c.bar, { width: (X(c.b) - X(c.a)) * A.prog(ts, 0.8, 0.2) });
            else A.set(c.bar, { width: X(c.b) - X(c.a) });
          });
          op(marks, k === 6 ? A.prog(ts, 0.5, 0.3) : 0);
          op(techG, k === 5 ? 0 : 1);
          var T = TECH[k];
          tl.forEach(function (e, i) { st(A, e, T[i]); op(e, A.prog(ts, 0.4, 0.3 + i * 0.3)); cls(e, i === 0 ? 't-s t-b' : 't-s'); });
        }
      };
    }
  });

  ANIM.reg('B:7.5', {
    title: '第 3 层：应用与分析',
    cap: '控制类应用“动手”，分析类应用“看数据”。分析又分数据分析和网络分析；数据分析又分静态和灵活两种（p.100–102）。',
    h: 240, tween: 2.8, stepDur: 4.6, live: true,
    steps: [
      '控制类应用：收集几个物体的数据，按单个物体里编不进去的复杂逻辑，反过来控制执行器。',
      '分析类应用：收集多个物体的数据，处理后显示历史报告、统计、趋势和系统状态。',
      '网络分析：连接丢失或变差会严重影响效率。偶尔报状态的系统看连通性就够；准实时控制要详细分析网络。',
      '数据分析的两种：静态（传感器和分析内容事先定死，常见于工业现场）和灵活（可以加传感器，上下游都能扩展）。'
    ],
    init: function (A) {
      var s1 = A.g(), s2 = A.g();
      var SP = [[44, 50], [44, 100], [44, 150]], AC = [44, 204], APP = [178, 120];
      var links = SP.map(function (p) { return A.line(p[0] + 12, p[1], APP[0] - 40, APP[1], 's-soft w1', s1); });
      var cmdL = A.line(APP[0] - 40, APP[1] + 10, AC[0] + 16, AC[1], 's-gold w2 dash', s1);
      ['温度', '湿度', '门磁'].forEach(function (n, i) { box(A, 20, SP[i][1] - 13, 48, 26, n, 'f-card s-acc w1', s1, 't-s t-b'); });
      var act = box(A, 16, AC[1] - 14, 56, 28, '阀门', 'f-card s-gold w2', s1, 't-s t-b');
      A.text(44, 234, '执行器', { cls: 't-s', anchor: 'middle' }, s1);
      var app = box(A, APP[0] - 40, APP[1] - 30, 80, 60, '应用', 'f-accs s-acc w2', s1, 't-b');
      var rule = A.text(APP[0], APP[1] + 46, '若 温度高 且 门关 → 开阀', { cls: 't-s f-gold t-b', anchor: 'middle' }, s1);
      var dash = A.g({}, s1);
      A.rect(258, 30, 136, 180, 'f-card s-line w1', dash, 8);
      A.text(326, 48, '仪表盘', { cls: 't-s t-b', anchor: 'middle' }, dash);
      var chart = A.path('', 's-acc w2', dash);
      A.line(268, 120, 386, 120, 's-line w1', dash);
      var bars = [0, 1, 2, 3].map(function (i) { return A.rect(272 + i * 28, 190, 18, 0, 'f-gold s-none', dash, 2); });
      A.text(326, 136, '历史 · 统计 · 趋势', { cls: 't-s', anchor: 'middle' }, dash);
      A.arrow(APP[0] + 40, APP[1], 256, APP[1], 's-acc w2', s1, 6);
      var net = A.g({}, s1);
      A.text(326, 226, '网络：1 条链路变差', { cls: 't-s f-bad t-b', anchor: 'middle' }, net);
      var pk = [0, 1, 2].map(function () { return A.circle(0, 0, 4, 'f-acc s-card w1', s1); });
      var cmd = A.circle(0, 0, 4.5, 'f-gold s-card w1', s1);
      // scene 2: static vs flexible
      A.rect(6, 8, 190, 226, 'f-card s-line w1', s2, 8); A.rect(204, 8, 190, 226, 'f-card s-line w1', s2, 8);
      A.text(101, 28, '静态（固定）', { cls: 't-b', anchor: 'middle' }, s2); A.text(299, 28, '灵活（可扩展）', { cls: 't-b', anchor: 'middle' }, s2);
      box(A, 70, 150, 62, 34, '固定分析', 'f-accs s-acc w1', s2, 't-s t-b');
      [40, 101, 162].forEach(function (x) { A.circle(x, 70, 9, 'f-accs s-acc w2', s2); A.line(x, 106, 101, 150, 's-soft w1', s2); A.text(x, 98, '定死', { cls: 't-xs', anchor: 'middle' }, s2); });
      A.text(101, 210, '例：工业现场', { cls: 't-s', anchor: 'middle' }, s2);
      box(A, 268, 150, 62, 34, '可扩展分析', 'f-goods s-good w1', s2, 't-s t-b');
      var fx = [234, 274, 314, 354], fl = [], fc = [];
      fx.forEach(function (x, i) { fl.push(A.line(x, 79, 299, 150, 's-soft w1', s2)); fc.push(A.circle(x, 70, 9, i === 3 ? 'f-goods s-good w2' : 'f-accs s-acc w2', s2)); });
      var plus = A.text(354, 52, '+ 新传感器', { cls: 't-s f-good t-b', anchor: 'middle' }, s2);
      var down = A.arrow(299, 186, 299, 206, 's-good w2', s2, 6);
      A.text(299, 222, '下游也能扩展', { cls: 't-s f-good', anchor: 'middle' }, s2);
      return {
        frame: function (ts, dt, k) {
          op(s1, k <= 2 ? 1 : 0); op(s2, k === 3 ? A.prog(ts, 0.5) : 0);
          if (k === 3) { var u3 = A.prog(ts, 0.6, 0.6); op(fc[3], u3); op(fl[3], u3); op(plus, u3); op(down, A.prog(ts, 0.5, 1.2)); return; }
          op(dash, k >= 1 ? (k === 1 ? A.prog(ts, 0.5) : 1) : 0.15);
          op(rule, k === 0 ? A.prog(ts, 0.4, 0.8) : 0); op(cmdL, k === 0 ? A.prog(ts, 0.4, 1.2) : 0.15);
          var cyc = (ts % 1.6) / 1.6;
          pk.forEach(function (p, i) {
            var q = along([[SP[i][0] + 12, SP[i][1]], [APP[0] - 40, APP[1]]], cyc);
            A.set(p, { cx: q[0], cy: q[1] });
            var broken = k === 2 && i === 2;
            op(p, broken ? (cyc < 0.5 ? 1 : 0) : 1);
          });
          links.forEach(function (l, i) { cls(l, k === 2 && i === 2 ? 's-bad w2 dash' : 's-soft w1'); });
          op(net, k === 2 ? A.prog(ts, 0.4, 0.3) : 0);
          if (k === 0) { var q2 = along([[APP[0] - 40, APP[1] + 10], [AC[0] + 16, AC[1]]], cyc); A.set(cmd, { cx: q2[0], cy: q2[1] }); op(cmd, ts > 1.2 ? 1 : 0); } else op(cmd, 0);
          cls(act._r, k === 0 && ts > 1.2 && cyc > 0.9 ? 'f-golds s-gold w3' : 'f-card s-gold w2');
          var g = k >= 1 ? A.prog(ts, 1.2, 0.4) : 0, d = '';
          for (var i = 0; i <= 10; i++) { var x = 270 + i * 11, y = 104 - (i * 4 + 12 * Math.sin(i * 0.9)) * (k >= 1 ? 1 : 0); if (i / 10 <= g) d += (d ? 'L' : 'M') + x + ' ' + y.toFixed(1); }
          A.set(chart, { d: d || 'M0 0' });
          bars.forEach(function (b, i) { var hh = [24, 40, 30, 52][i] * g; A.set(b, { y: 190 - hh, height: hh }); });
        }
      };
    }
  });

  ANIM.reg('B:7.6', {
    title: '雾计算与边缘计算：数据不必都上云',
    cap: '左边是 p.107 的层级数量：越往下越多、时延越低。数字例子（1000 个振动传感器）是页面上的练习，不是讲义原数据；最后一步是真题 2025-26 S1 Q4(c) 的雾计算五个特点。',
    h: 262, tween: 3, stepDur: 5, live: true,
    steps: [
      '全部上云：1000 个传感器 × 10 次/秒 × 100 B = 1 MB/s = 8 Mbps，全部挤过回程上云。',
      '问题：最后一公里带宽小、回程（3G/LTE/卫星）不可靠、数据量太大、到云端时延大，做不到实时。',
      '边缘：传感器自己判断振动超限，立刻停机。毫秒级的决定不能等云。',
      '雾：雾节点每分钟把每个传感器汇总成 1 条 100 B 的统计，上传降到约 13 kbps，少约 600 倍。',
      '云：存历史数据，做几个月的趋势分析和预测性维护。边缘、雾、云互补，不是替代。',
      '雾计算的五个特点（p.109）：位置感知与低时延、地理分布、靠近大量终端、与终端无线连接、用于实时交互。'
    ],
    init: function (A) {
      var N = 1000, HZ = 10, B = 100, all = N * HZ * B, fog = N * B / 60;
      var allMbps = all * 8 / 1e6, fogKbps = fog * 8 / 1e3, ratio = all / fog;
      var BX = 82, BW = 206;
      var T = [['云 / 数据中心', 18, '几百个'], ['回程：核心 IPv6 网', 76, '几千个'], ['雾层：网关、路由器', 134, '几万个'], ['智能物体（边缘）', 192, '几百万个']];
      var bands = T.map(function (t, i) {
        var g = A.g();
        g._r = A.rect(BX, t[1], BW, 36, ['f-accs s-acc w1', 'f-paper s-soft w1', 'f-goods s-good w1', 'f-golds s-gold w1'][i], g, 18);
        A.text(BX + 14, t[1] + 14, t[0], { cls: 't-s t-b' }, g);
        A.text(BX - 6, t[1] + 22, t[2], { cls: 't-s t-b', anchor: 'end' }, g);
        return g;
      });
      A.set(A.text(14, 124, '越往下：数量越多、时延越低 →', { cls: 't-s', anchor: 'middle' }), { transform: 'rotate(90 14 124)' });
      var SX = [110, 142, 174, 206, 238, 270];
      SX.forEach(function (x) { A.circle(x, 216, 5, 'f-gold s-card w1'); });
      var FN = [130, 190, 250];
      FN.forEach(function (x) { A.rect(x - 9, 148, 18, 12, 'f-good s-card w1', null, 2); });
      var right = A.g(), RT = [A.text(296, 38, '', { cls: 't-s' }, right), A.text(296, 96, '', { cls: 't-s' }, right), A.text(296, 154, '', { cls: 't-s' }, right), A.text(296, 212, '', { cls: 't-s' }, right)];
      var RT2 = [A.text(296, 52, '', { cls: 't-s' }, right), A.text(296, 110, '', { cls: 't-s' }, right), A.text(296, 168, '', { cls: 't-s' }, right), A.text(296, 226, '', { cls: 't-s' }, right)];
      var pk = [];
      for (var i = 0; i < 12; i++) pk.push(A.rect(0, 0, 6, 6, 'f-gold s-none', null, 1));
      var trickle = A.rect(0, 0, 6, 6, 'f-good s-none', null, 1);
      var loop = A.g();
      A.path('M261 209 a10 10 0 1 1 18 0', 's-bad w2', loop); A.arrow(280, 205, 279, 211, 's-bad w2', loop, 5);
      var stop = A.circle(270, 216, 7, 'f-none s-bad w2', loop);
      var cloudChart = A.path('M210 46 L222 40 L234 43 L246 32 L258 36 L270 26', 's-acc w2');
      var rate = A.text(200, 252, '', { cls: 't-m t-b', anchor: 'middle' });
      var feat = A.g();
      A.rect(6, 10, 388, 232, 'f-card s-good w2', feat, 10);
      A.text(200, 34, '雾计算的五个特点（p.109）', { cls: 't-b f-good', anchor: 'middle' }, feat);
      var FT = ['① 上下文位置感知、低时延：雾节点尽量靠近终端', '② 地理上分布：服务需要广泛的分布式部署', '③ 部署在大量 IoT 终端附近', '④ 雾节点与终端之间用无线通信（容易扩展）', '⑤ 用于实时交互：雾节点预处理，上层只批处理子集'];
      var ft = FT.map(function (s, i) { return A.text(20, 70 + i * 36, s, { cls: '' }, feat); });
      var NOTE = [
        [['', ''], ['', ''], ['', ''], ['', '']],
        [['时延大', '做不到实时'], ['不可靠、', '数据量太大'], ['', ''], ['最后一公里', '带宽很小']],
        [['', ''], ['', ''], ['', ''], ['超限→停机！', '毫秒级，就地']],
        [['', ''], ['只剩汇总', '数据'], ['毫秒/亚秒级', '响应（p.107）'], ['', '']],
        [['历史、趋势', '预测性维护'], ['', ''], ['', ''], ['', '']]
      ];
      return {
        frame: function (ts, dt, k) {
          op(feat, k === 5 ? A.prog(ts, 0.4) : 0);
          ft.forEach(function (e, i) { op(e, k === 5 ? A.prog(ts, 0.4, 0.3 + i * 0.35) : 0); });
          if (k === 5) { st(A, rate, ''); return; }
          bands.forEach(function (b, i) {
            var c = ['f-accs s-acc w1', 'f-paper s-soft w1', 'f-goods s-good w1', 'f-golds s-gold w1'][i];
            if ((k === 0 || k === 1) && i === 1) c = 'f-bads s-bad w2';
            if (k === 2 && i === 3 || k === 3 && i === 2 || k === 4 && i === 0) c = c.replace('w1', 'w3');
            cls(b._r, c);
          });
          RT.forEach(function (e, i) { st(A, e, NOTE[k][i][0]); st(A, RT2[i], NOTE[k][i][1]); cls(e, 't-s t-b' + (k === 1 || k === 2 ? ' f-bad' : '')); });
          op(right, A.prog(ts, 0.4, 0.2));
          op(loop, k === 2 ? 1 : 0); op(stop, k === 2 ? (Math.sin(ts * 6) > -0.3 ? 1 : 0.3) : 0);
          op(cloudChart, k === 4 ? A.prog(ts, 0.6, 0.2) : 0);
          var top = k <= 1 ? 30 : 154, sp = 0.7;
          pk.forEach(function (p, j) {
            if (k === 2 || k === 4) { op(p, 0); return; }
            var x = SX[j % 6], u = ((ts * sp) + j / 12) % 1;
            var y = A.lerp(210, top, u);
            A.set(p, { x: x - 3, y: y - 3 }); op(p, 1);
          });
          if (k === 3 || k === 4) { var u2 = (ts * 0.25) % 1; A.set(trickle, { x: 187, y: A.lerp(146, 30, u2) - 3 }); op(trickle, 1); } else op(trickle, 0);
          var rt = k <= 1 ? '上传：' + A.fmt(all / 1e6, 3) + ' MB/s = ' + A.fmt(allMbps, 3) + ' Mbps' :
            k === 2 ? '停机决定在本地做，不占回程' :
            k === 3 ? '上传：' + A.fmt(fog / 1e3, 2) + ' kB/s ≈ ' + Math.round(fogKbps) + ' kbps（少 ' + Math.round(ratio) + ' 倍）' :
            '边缘停机 · 雾做分钟统计 · 云看长期趋势';
          st(A, rate, rt);
        }
      };
    }
  });
})();
