/* EE6129 Part C (satellite communications) — one animated figure per section of partC.html.
   Built from src/anim/_work/C_all/p*.js. Geometry/orbit numbers are computed here (R = 6,370 km, μ = 398,600 km³/s²). */
(function () {
  'use strict';
  var R = 6370, MU = 398600, CL = 3e5, HGEO = 35863, DEG = Math.PI / 180;
  function period(h) { var a = R + h; return 2 * Math.PI * Math.sqrt(a * a * a / MU); }                 // seconds
  function betaR(h, th) { var t = th * DEG; return Math.acos(R * Math.cos(t) / (R + h)) - t; }        // coverage angle, rad
  function slant(h, b) { var s = R + h; return Math.sqrt(R * R + s * s - 2 * R * s * Math.cos(b)); }  // km
  function elevR(h, phi) { phi = Math.abs(phi); return Math.atan2(Math.cos(phi) - R / (R + h), Math.sin(phi)); }
  function grp(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function cl(x, a, b) { return x < a ? a : x > b ? b : x; }
  function place(g, x, y, rot) { g.setAttribute('transform', 'translate(' + x.toFixed(1) + ',' + y.toFixed(1) + ')' + (rot ? ' rotate(' + rot.toFixed(1) + ')' : '')); }
  function show(el, on) { el.style.display = on ? '' : 'none'; }
  function op(el, v) { el.setAttribute('opacity', (+v).toFixed(2)); }
  /* satellite icon centred on its origin */
  function sat(A, parent, c, s) {
    s = s || 1;
    var g = A.g({}, parent);
    A.line(-9 * s, 0, 9 * s, 0, 's-' + c + ' w1', g);
    A.rect(-15 * s, -3.5 * s, 8 * s, 7 * s, 'f-card s-' + c + ' w1', g, 1);
    A.rect(7 * s, -3.5 * s, 8 * s, 7 * s, 'f-card s-' + c + ' w1', g, 1);
    A.rect(-4.5 * s, -5 * s, 9 * s, 10 * s, 'f-' + c + ' s-none', g, 1.5);
    return g;
  }
  /* ground antenna, origin = foot */
  function dish(A, parent, c, s) {
    s = s || 1;
    var g = A.g({}, parent);
    A.line(0, 0, 0, -7 * s, 's-' + c + ' w2', g);
    A.path('M' + (-8 * s) + ' ' + (-13 * s) + 'Q0 ' + (-3 * s) + ' ' + (8 * s) + ' ' + (-13 * s) + 'Z', 'f-' + c + ' s-' + c + ' w1', g);
    A.line(-5 * s, 0, 5 * s, 0, 's-' + c + ' w2', g);
    return g;
  }
  /* point at fraction p (0..1, by length) along a polyline */
  function along(pts, p) {
    var L = [0], tot = 0, i;
    for (i = 1; i < pts.length; i++) { tot += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); L.push(tot); }
    var s = cl(p, 0, 1) * tot;
    for (i = 1; i < pts.length; i++) if (s <= L[i] || i === pts.length - 1) {
      var f = L[i] > L[i - 1] ? (s - L[i - 1]) / (L[i] - L[i - 1]) : 0;
      return [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f];
    }
    return pts[0];
  }
  function mv(c, p) { c.setAttribute('cx', p[0].toFixed(1)); c.setAttribute('cy', p[1].toFixed(1)); }

  /* ================= 1.1 terms ================= */
  ANIM.reg('C:1.1', {
    title: '上行 → 转发器 → 下行 → 覆盖区',
    cap: '蓝点是上行频率 f<sub>u</sub> 的信号，变成金点表示转发器已经<b>变频</b>到下行频率 f<sub>d</sub> 并放大。卫星像山顶的回音壁，只负责收、变、放、转，不"理解"内容。',
    h: 240, live: true, stepDur: 4,
    steps: [
      '<b>地面站</b> Earth Station：地面上或地面附近的天线系统。站 A 要把信号送给很远的站 B。',
      '<b>Uplink 上行</b>：地面站 → 卫星，用上行频率 f<sub>u</sub>。',
      '<b>Transponder 转发器</b>：接收 → 变频（f<sub>u</sub> 换成 f<sub>d</sub>）→ 放大 → 转发。',
      '<b>Downlink 下行</b>：卫星 → 地面站，用变频后的下行频率 f<sub>d</sub>。',
      '<b>覆盖区</b>（footprint）：卫星波束照到的地面范围，可以是全球、区域或一个国家。',
      '三种业务：<b>FSS</b> 卫星与固定站之间；<b>BSS</b> 电视、广播直播；<b>MSS</b> 飞机、船、车辆。'
    ],
    init: function (A) {
      function yE(x) { return 1100 - Math.sqrt(810000 - (x - 200) * (x - 200)); }
      var x, ep = [];
      for (x = 0; x <= 400; x += 10) ep.push([x, yE(x)]);
      A.poly(ep.concat([[400, 240], [0, 240]]), 'f-goods s-none');
      A.poly(ep, 's-good w2');
      var S = [150, 60], E1 = [50, yE(50)], E2 = [330, yE(330)];
      var foot = A.g({ opacity: 0 }), fp = [];
      A.poly([S, [20, yE(20)], [370, yE(370)]], 'f-golds s-none op7', foot);
      for (x = 20; x <= 370; x += 10) fp.push([x, yE(x)]);
      A.poly(fp, 's-gold w4', foot);
      A.text(200, 228, '覆盖区 footprint', { cls: 't-s t-b f-gold', anchor: 'middle' }, foot);
      var up = A.line(E1[0], E1[1] - 12, S[0], S[1], 's-acc w2 dash'), dn = A.line(S[0], S[1], E2[0], E2[1] - 12, 's-gold w2 dash');
      var upL = A.g(), dnL = A.g();
      A.text(92, 134, '上行', { cls: 't-b f-acc', anchor: 'end' }, upL);
      A.text(80, 150, 'uplink f_{u}', { cls: 't-s f-acc', anchor: 'end' }, upL);
      A.text(252, 120, '下行', { cls: 't-b f-gold' }, dnL);
      A.text(252, 136, 'downlink f_{d}', { cls: 't-s f-gold' }, dnL);
      var st = A.g();
      dish(A, st, 'soft'); place(st.lastChild, E1[0], E1[1]);
      dish(A, st, 'soft'); place(st.lastChild, E2[0], E2[1]);
      A.text(E1[0], E1[1] + 16, '地面站 A', { cls: 't-s t-b', anchor: 'middle' }, st);
      A.text(E2[0], E2[1] + 16, '地面站 B', { cls: 't-s t-b', anchor: 'middle' }, st);
      var sg = sat(A, null, 'ink', 1.1); place(sg, S[0], S[1]);
      A.text(S[0], S[1] - 14, '卫星', { cls: 't-s', anchor: 'middle' });
      /* transponder strip */
      var tp = A.g(), boxes = [], names = ['接收', '变频', '放大', '转发'];
      A.path('M' + (S[0] + 18) + ' ' + S[1] + 'L228 30', 's-faint w1 dot', tp);
      names.forEach(function (n, i) {
        boxes.push(A.rect(231 + i * 41, 14, 36, 22, 'f-card s-line w1', tp, 5));
        A.text(249 + i * 41, 29, n, { cls: 't-s t-b', anchor: 'middle' }, tp);
      });
      A.text(312, 52, '转发器 transponder 内部', { cls: 't-s', anchor: 'middle' }, tp);
      var sv = A.g({ opacity: 0 });
      ['FSS：卫星 ↔ 固定站', 'BSS：电视、广播直播', 'MSS：飞机、船、车'].forEach(function (s, i) { A.text(8, 18 + i * 16, s, { cls: 't-s t-b' }, sv); });
      var pu = A.circle(0, 0, 4.5, 'f-acc'), pd = [0, 1, 2].map(function () { return A.circle(0, 0, 4.5, 'f-gold'); });
      var cur = 0;
      return {
        step: function (k) {
          cur = k;
          op(up, k >= 1 ? 1 : 0.3); op(upL, k >= 1 ? 1 : 0.3);
          op(dn, k >= 3 ? 1 : 0.3); op(dnL, k >= 3 ? 1 : 0.3);
          op(tp, k >= 2 ? 1 : 0.45); op(foot, k >= 4 ? 1 : 0); op(sv, k === 5 ? 1 : 0);
          op(st, 1);
        },
        frame: function (ts, dt, k) {
          var p = (ts % 1.8) / 1.8;
          show(pu, k === 1); if (k === 1) mv(pu, along([[E1[0], E1[1] - 12], S], p));
          var tg = [[E2[0], E2[1] - 12], [40, yE(40) - 2], [200, 198]];
          pd.forEach(function (c, i) {
            var on = k === 3 ? i === 0 : k >= 4;
            show(c, on); if (on) mv(c, along([S, tg[i]], p));
          });
          boxes.forEach(function (b, i) {
            var act = k === 2 && Math.floor(ts / 0.7) % 4 === i;
            A.set(b, { cls: act ? (i === 0 ? 'f-accs s-acc w2' : 'f-golds s-gold w2') : 'f-card s-line w1' });
          });
        }
      };
    }
  });

  /* ================= 1.2 three kinds ================= */
  ANIM.reg('C:1.2', {
    title: 'GEO、MEO、LEO 各干什么',
    cap: '半径没按比例（真实 GEO 半径是地球的 6.6 倍）；转速按开普勒定律算（LEO 取 1,000 km、MEO 取 10,000 km），动画 1 秒 = 1 小时。GEO 跟着地面上的金点一起转，所以从地面看它不动。',
    h: 230,
    init: function (A) {
      var cx = 108, cy = 115, TE = period(HGEO);
      var orb = [
        { n: 'LEO', h: 1000, r: 46, c: 'good' },
        { n: 'MEO', h: 10000, r: 72, c: 'gold' },
        { n: 'GEO', h: HGEO, r: 102, c: 'acc' }];
      orb.forEach(function (o) { A.circle(cx, cy, o.r, 'f-none s-' + o.c + ' w1 dash'); });
      A.circle(cx, cy, 30, 'f-goods s-good w2');
      var mer = A.line(cx, cy, cx + 30, cy, 's-gold w2'), gp = A.circle(cx + 30, cy, 3.5, 'f-gold');
      orb.forEach(function (o) { o.g = sat(A, null, o.c, 0.75); o.T = period(o.h) / 3600; });
      var L = [
        [30, 'GEO　T = ' + orb[2].T.toFixed(1) + ' h', 'f-acc'], [47, '承担大部分通信业务', ''], [63, '固定站用高增益天线', ''],
        [100, 'MEO　T = ' + orb[1].T.toFixed(1) + ' h', 'f-gold'], [117, '导航：GPS 用 24 颗 MEO', ''],
        [152, 'LEO　T = ' + orb[0].T.toFixed(2) + ' h', 'f-good'], [169, '移动通信：话音和数据', ''], [185, '对地成像、监视', '']];
      L.forEach(function (l) { A.text(234, l[0], l[1], { cls: l[2] ? 't-b ' + l[2] : 't-s' }); });
      var clk = A.text(234, 216, '', { cls: 't-s t-m' });
      return function (t) {
        orb.forEach(function (o) { var a = 2 * Math.PI * t / o.T; place(o.g, cx + o.r * Math.cos(a), cy - o.r * Math.sin(a)); });
        var e = 2 * Math.PI * t * 3600 / TE;
        A.set(mer, { x2: cx + 30 * Math.cos(e), y2: cy - 30 * Math.sin(e) }); A.set(gp, { cx: cx + 30 * Math.cos(e), cy: cy - 30 * Math.sin(e) });
        A.setText(clk, '经过 ' + t.toFixed(1) + ' h');
      };
    }
  });

  /* ================= 1.3 orbit dimensions ================= */
  ANIM.reg('C:1.3', {
    title: '轨道的三个维度：高度、形状、倾角',
    cap: '点上面的按钮切换维度。"高度"图是按比例画的：LEO 贴着地面，GEO 远在 5.6 个地球半径之外。椭圆轨道上卫星近地点快、远地点慢。',
    h: 220,
    init: function (A) {
      var vw = [A.g(), A.g(), A.g()];
      /* view 0: altitude, to scale, vertical */
      var g = vw[0], Y = function (km) { return 205 - km * 180 / 40000; };
      A.rect(0, 205, 400, 15, 'f-goods s-none', g, 0); A.line(0, 205, 400, 205, 's-good w2', g);
      A.text(8, 217, '地面', { cls: 't-s f-good' }, g);
      [0, 10000, 20000, 30000, 40000].forEach(function (v, i) {
        A.line(40, Y(v), 44, Y(v), 's-soft w1', g);
        A.text(36, Y(v) + 4, i ? i + ' 万' : '0', { cls: 't-s', anchor: 'end' }, g);
      });
      A.line(42, 205, 42, 20, 's-soft w1', g); A.text(48, 22, '高度 km', { cls: 't-s' }, g);
      A.rect(50, Y(1500), 200, Math.max(4, Y(500) - Y(1500)), 'f-good s-none', g, 0);
      A.rect(50, Y(18000), 200, Y(8000) - Y(18000), 'f-golds s-gold w1', g, 0);
      A.line(50, Y(HGEO), 250, Y(HGEO), 's-acc w3', g);
      A.text(258, Y(1000) + 1, 'LEO 500–1,500 km', { cls: 't-s t-b f-good' }, g);
      A.text(258, Y(13000) + 4, 'MEO 8,000–18,000 km', { cls: 't-s t-b f-gold' }, g);
      A.text(258, Y(HGEO) + 4, 'GEO 35,863 km', { cls: 't-s t-b f-acc' }, g);
      A.line(388, 205, 388, Y(R), 's-ink w2', g); A.line(384, Y(R), 392, Y(R), 's-ink w2', g);
      A.text(382, Y(R) + 10, '地球半径 6,370 km', { cls: 't-s', anchor: 'end' }, g);
      /* view 1: shape */
      g = vw[1];
      var fx = 120, fy = 112, a = 112, e = 0.5, b = a * Math.sqrt(1 - e * e), rc = 40;
      A.el('ellipse', { cx: fx + a * e, cy: fy, rx: a, ry: b, cls: 'f-none s-gold w2' }, g);
      A.circle(fx, fy, rc, 'f-none s-acc w2', g);
      A.circle(fx, fy, 20, 'f-goods s-good w2', g);
      A.circle(fx + 2 * a * e, fy, 2.5, 'f-none s-gold w1', g);
      A.text(fx, fy + 4, '地心', { cls: 't-s', anchor: 'middle' }, g);
      A.text(fx, fy + rc + 18, '圆轨道：圆心在地心', { cls: 't-s t-b f-acc', anchor: 'middle' }, g);
      A.text(fx + a + a * e + 6, fy - 12, '椭圆轨道：', { cls: 't-s t-b f-gold' }, g);
      A.text(fx + a + a * e + 6, fy + 4, '地心在一个焦点上', { cls: 't-s t-b f-gold' }, g);
      A.text(fx + a + a * e + 6, fy + 24, '远地点：慢', { cls: 't-s' }, g);
      A.text(fx - a * (1 - e) - 6, fy + 4, '近地点：快', { cls: 't-s', anchor: 'end' }, g);
      A.text(fx + 2 * a * e, fy + 16, '另一个焦点', { cls: 't-s', anchor: 'middle' }, g);
      var sC = sat(A, g, 'acc', 0.6), sE = sat(A, g, 'gold', 0.6);
      /* view 2: inclination */
      g = vw[2];
      var cx = 200, cy = 116;
      function ell(rot, cls) { return A.el('ellipse', { cx: 0, cy: 0, rx: 95, ry: 19, cls: 'f-none ' + cls, transform: 'translate(' + cx + ',' + cy + ') rotate(' + rot + ')' }, g); }
      A.circle(cx, cy, 50, 'f-goods s-good w2', g);
      A.el('ellipse', { cx: cx, cy: cy, rx: 50, ry: 10, cls: 'f-none s-good w1 dash' }, g);
      ell(0, 's-acc w2'); ell(90, 's-gold w2'); ell(-40, 's-pur w2');
      A.text(cx, cy - 54, 'N', { cls: 't-s t-b', anchor: 'middle' }, g); A.text(cx, cy + 64, 'S', { cls: 't-s t-b', anchor: 'middle' }, g);
      A.text(cx + 99, cy + 4, '赤道轨道', { cls: 't-s t-b f-acc' }, g);
      A.text(cx + 26, 22, '极轨道（经过两极）', { cls: 't-s t-b f-gold' }, g);
      A.text(cx + 80, cy - 70, '倾斜轨道', { cls: 't-s t-b f-pur' }, g);
      var sI = [sat(A, g, 'acc', 0.55), sat(A, g, 'gold', 0.55), sat(A, g, 'pur', 0.55)];
      var view = 0;
      A.choice({ label: '维度', options: ['高度', '形状', '倾角'], value: 0, on: function (i) { view = i; vw.forEach(function (v, j) { show(v, j === i); }); A.redraw(); } });
      vw.forEach(function (v, j) { show(v, j === 0); });
      return function (t) {
        if (view === 1) {
          var T = 7, M = 2 * Math.PI * t / T, E = M;
          for (var i = 0; i < 6; i++) E -= (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
          place(sE, fx - a * (Math.cos(E) - e), fy - b * Math.sin(E));
          var ac = 2 * Math.PI * t / (T * Math.pow(rc / a, 1.5));
          place(sC, fx - rc * Math.cos(ac), fy - rc * Math.sin(ac));
        } else if (view === 2) {
          var u = 2 * Math.PI * t / 6;
          [0, 90, -40].forEach(function (rot, j) {
            var px = 95 * Math.cos(u + j * 2.1), py = 19 * Math.sin(u + j * 2.1), r = rot * DEG;
            place(sI[j], cx + px * Math.cos(r) - py * Math.sin(r), cy + px * Math.sin(r) + py * Math.cos(r));
          });
        }
      };
    }
  });

  /* ================= 1.3 / 2: why GEO is one altitude ================= */
  ANIM.reg('C:1.3/2', {
    title: '为什么"静止"轨道只有一个高度',
    cap: '从北极往下看，地球逆时针自转（金点 = 赤道上某个地面站；动画 1 秒 = 2 小时）。拖高度：只有 35,863 km 时卫星周期 = 24 h，卫星一直停在金点正上方。还必须在赤道上空：倾斜的 24 h 轨道每天会南北摆动。',
    h: 230, speed: 2,
    init: function (A) {
      var cx = 118, cy = 115, re = 36, h = 20000;
      function rpx(hh) { return re * Math.sqrt((R + hh) / R); }
      var orbit = A.circle(cx, cy, rpx(h), 'f-none s-acc w1 dash');
      A.circle(cx, cy, re, 'f-goods s-good w2');
      A.text(cx, cy + 4, '北极', { cls: 't-s', anchor: 'middle' });
      var ray = A.line(cx, cy, cx, cy, 's-gold w1 dash'), gp = A.circle(0, 0, 4, 'f-gold');
      var sg = sat(A, null, 'acc', 0.8);
      var tx = 248, L1 = A.text(tx, 34, '', { cls: 't-l t-b t-m f-acc' });
      A.text(tx, 54, '地球自转一圈 24 h', { cls: 't-s' });
      var L3 = A.text(tx, 84, '', { cls: 't-b' }), L4 = A.text(tx, 102, '', { cls: 't-s' });
      var L5 = A.text(tx, 140, '', { cls: 't-s t-m' });
      A.text(tx, 158, 'T = 2π√(a³/μ)', { cls: 't-s t-m' });
      var clk = A.text(tx, 214, '', { cls: 't-s t-m' });
      var sl = A.slider({ label: '高度 h', min: 500, max: 50000, step: 1, value: h, fmt: function (v) { return grp(v) + ' km'; },
        on: function (v) { if (v !== HGEO && Math.abs(v - HGEO) < 450) { sl.set(HGEO); return; } h = v; A.redraw(); } });
      A.button('设为 35,863 km', function () { sl.set(HGEO); });
      return function (t) {
        var T = period(h) / 3600, th = t, sync = Math.abs(h - HGEO) < 1;
        var ag = 2 * Math.PI * th / 24, as = sync ? ag : 2 * Math.PI * th / T, r = rpx(h);
        A.set(orbit, { r: r });
        mv(gp, [cx + re * Math.cos(ag), cy - re * Math.sin(ag)]);
        A.set(ray, { x1: cx + re * Math.cos(ag), y1: cy - re * Math.sin(ag), x2: cx + (r + 14) * Math.cos(ag), y2: cy - (r + 14) * Math.sin(ag) });
        place(sg, cx + r * Math.cos(as), cy - r * Math.sin(as));
        A.setText(L1, 'T = ' + (T < 10 ? T.toFixed(2) : T.toFixed(1)) + ' h');
        var rel = 24 / T - 1;
        A.setText(L3, sync ? '同步：停在正上方' : rel > 0 ? '比地面快 → 向东漂' : '比地面慢 → 向西漂');
        A.set(L3, { cls: 't-b ' + (sync ? 'f-good' : 'f-bad') });
        A.setText(L4, sync ? '地面天线对准后不用再转' : '地面过一天，卫星' + (rel > 0 ? '多' : '少') + '转 ' + Math.abs(rel).toFixed(2) + ' 圈');
        A.setText(L5, 'a = R + h = ' + grp(R + h) + ' km');
        A.setText(clk, '第 ' + (Math.floor(th / 24) + 1) + ' 天 ' + (th % 24).toFixed(1) + ' h');
      };
    }
  });

  /* circle polygon clamped to the viewBox (big Earth discs) */
  function discPath(A, cx, cy, r, H) {
    var pts = [];
    for (var i = 0; i <= 120; i++) { var a = i * Math.PI / 60; pts.push([cl(cx + r * Math.sin(a), 0, 400), cl(cy - r * Math.cos(a), 0, H)]); }
    return A.pts(pts) + 'Z';
  }
  /* arc path around c from angle a1 to a2 (screen atan2 angles, shortest way) */
  function arcD(A, c, r, a1, a2) {
    var d = a2 - a1; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI;
    var pts = [];
    for (var i = 0; i <= 16; i++) { var a = a1 + d * i / 16; pts.push([c[0] + r * Math.cos(a), c[1] + r * Math.sin(a)]); }
    return A.pts(pts);
  }

  /* ================= 2.1 elevation & coverage angle ================= */
  ANIM.reg('C:2.1', {
    title: '仰角 θ 和覆盖角 β',
    cap: '按比例画：卫星 S 固定在上方，地球大小随 h 变。θ 在地面站 E 处从水平线量到卫星方向；β 在地心 O 处。金色弧 = 覆盖区。β = arccos(R·cos θ/(R+h)) − θ，R = 6,370 km。',
    h: 270,
    init: function (A) {
      var H = 270, O = [150, 250], top = 50, h = HGEO, th = 10;
      var earth = A.path('', 'f-goods s-good w2'), cov = A.path('', 's-gold w4');
      var c1 = A.line(0, 0, 0, 0, 's-faint w1 dash'), c2 = A.line(0, 0, 0, 0, 's-faint w1 dash');
      var lOS = A.line(O[0], O[1], O[0], top, 's-soft w1 dash'), lOE = A.line(0, 0, 0, 0, 's-soft w1 dash');
      var tan = A.line(0, 0, 0, 0, 's-ink w1'), lES = A.line(0, 0, 0, 0, 's-acc w2');
      var arcT = A.path('', 's-bad w2'), arcB = A.path('', 's-pur w2');
      var tT = A.text(0, 0, 'θ', { cls: 't-b f-bad', anchor: 'middle' }), tB = A.text(0, 0, 'β', { cls: 't-b f-pur', anchor: 'middle' });
      var dE = A.circle(0, 0, 3.5, 'f-acc'), dE2 = A.circle(0, 0, 2.5, 'f-faint');
      A.circle(O[0], O[1], 3, 'f-ink');
      A.text(O[0] - 7, O[1] + 4, 'O', { cls: 't-b', anchor: 'end' });
      var tE = A.text(0, 0, 'E', { cls: 't-b f-acc' }), tR = A.text(0, 0, 'R', { cls: 't-s' }), tD = A.text(0, 0, 'd', { cls: 't-s t-b f-acc' });
      A.text(O[0] - 6, top + 70, 'R + h', { cls: 't-s', anchor: 'end' });
      place(sat(A, null, 'ink', 0.9), O[0], top);
      A.text(O[0] + 18, top - 8, 'S', { cls: 't-b' });
      /* inset: the local view at E (horizon drawn level) */
      var Ei = [304, 88];
      A.rect(286, 8, 108, 96, 'f-card s-line w1', null, 6);
      A.rect(287, Ei[1], 106, 15, 'f-goods s-none', null, 0);
      A.line(290, Ei[1], 390, Ei[1], 's-ink w1');
      A.text(292, 22, '站在 E 处看', { cls: 't-s t-b' });
      A.text(388, Ei[1] + 12, '水平线', { cls: 't-s', anchor: 'end' });
      var iRay = A.arrow(Ei[0], Ei[1], Ei[0] + 70, Ei[1], 's-acc w2', null, 6), iArc = A.path('', 's-bad w2');
      var iT = A.text(0, 0, '', { cls: 't-s t-b f-bad' }), iS = A.text(0, 0, '→ S', { cls: 't-s t-b f-acc' });
      A.circle(Ei[0], Ei[1], 3, 'f-acc');
      function draw() {
        var rp = 200 * R / (R + h), b = betaR(h, th), sb = Math.sin(b), cb = Math.cos(b);
        var E = [O[0] + rp * sb, O[1] - rp * cb], E2 = [O[0] - rp * sb, E[1]], S = [O[0], top];
        A.set(earth, { d: discPath(A, O[0], O[1], rp, H) });
        A.set(cov, { d: 'M' + E2[0].toFixed(1) + ' ' + E2[1].toFixed(1) + 'A' + rp.toFixed(1) + ' ' + rp.toFixed(1) + ' 0 0 1 ' + E[0].toFixed(1) + ' ' + E[1].toFixed(1) });
        A.set(c1, { x1: S[0], y1: S[1], x2: E2[0], y2: E2[1] });
        A.set(c2, { x1: S[0], y1: S[1], x2: E[0], y2: E[1] });
        A.set(lOE, { x1: O[0], y1: O[1], x2: E[0], y2: E[1] });
        A.set(lES, { x1: E[0], y1: E[1], x2: S[0], y2: S[1] });
        var t2 = [-cb, -sb], dn = Math.min(18, (H - 2 - E[1]) / Math.max(sb, 0.01));
        A.set(tan, { x1: E[0] + 70 * t2[0], y1: E[1] + 70 * t2[1], x2: E[0] - dn * t2[0], y2: E[1] - dn * t2[1] });
        var vx = S[0] - E[0], vy = S[1] - E[1], vl = Math.hypot(vx, vy), aT = Math.atan2(t2[1], t2[0]), aV = Math.atan2(vy, vx);
        A.set(arcT, { d: arcD(A, E, 24, aT, aV) });
        var mT = Math.atan2(t2[1] + vy / vl, t2[0] + vx / vl);
        A.set(tT, { x: E[0] + 34 * Math.cos(mT), y: E[1] + 34 * Math.sin(mT) + 4 });
        var rb = Math.min(28, rp * 0.6), aU = Math.atan2(-cb, sb);
        A.set(arcB, { d: arcD(A, O, rb, -Math.PI / 2, aU) });
        var mB = Math.atan2(-1 - cb, sb);
        A.set(tB, { x: O[0] + (rb + 9) * Math.cos(mB), y: O[1] + (rb + 9) * Math.sin(mB) + 4 });
        mv(dE, E); mv(dE2, E2);
        A.set(tE, { x: E[0] + 9 * sb + 4, y: E[1] - 9 * cb + 4 });
        A.set(tR, { x: O[0] + rp * sb / 2 + 6 * cb, y: O[1] - rp * cb / 2 + 6 * sb + 4 });
        tR.style.display = rp > 70 ? '' : 'none';
        A.set(tD, { x: (E[0] + S[0]) / 2 + 8, y: (E[1] + S[1]) / 2 });
        var tr = th * DEG, L = 66;
        A.moveArrow(iRay, Ei[0], Ei[1], Ei[0] + L * Math.cos(tr), Ei[1] - L * Math.sin(tr));
        A.set(iArc, { d: arcD(A, Ei, 30, 0, -tr) });
        A.set(iT, th < 16 ? { x: Ei[0] + 12, y: Ei[1] - 30 } : { x: Ei[0] + 34, y: Ei[1] - 4 - 34 * Math.sin(tr / 2) });
        A.setText(iT, 'θ = ' + th + '°');
        A.set(iS, { x: Ei[0] + L * Math.cos(tr) - (th > 50 ? 10 : 6), y: Ei[1] - L * Math.sin(tr) - 6 });
        var d = slant(h, b);
        A.note('β = ' + (b / DEG).toFixed(2) + '°　覆盖直径 2βR ≈ ' + grp(Math.round(2 * b * R / 10) * 10) + ' km<br>斜距 d ≈ ' + grp(Math.round(d / 10) * 10) + ' km　（θ + β = ' + (th + b / DEG).toFixed(2) + '°）');
      }
      var sl = A.slider({ label: '高度 h', min: 500, max: 36000, step: 1, value: h, fmt: function (v) { return grp(v) + ' km'; },
        on: function (v) { if (v !== HGEO && Math.abs(v - HGEO) < 300) { sl.set(HGEO); return; } h = v; draw(); } });
      A.slider({ label: '最低仰角 θ', min: 0, max: 40, step: 1, value: th, unit: '°', fmt: function (v) { return v + '°'; }, on: function (v) { th = v; draw(); } });
      draw();
      return {};
    }
  });

  /* ================= 2.2 parameter table + pass ================= */
  ANIM.reg('C:2.2', {
    title: 'LEO 一闪而过，GEO 一直挂在天上',
    cap: '上：地面用户看到的天空（示意，一个竖直剖面）。LEO 取 1,500 km、只算卫星自己的运动；过顶时 1 秒 = 2 分钟，看不见时快进。下：讲义 p.14 的参数表。',
    h: 300,
    init: function (A) {
      var ux = 200, uy = 136, rd = 110, hL = 1500, TL = period(hL) / 60, b10 = betaR(hL, 10);
      var vis = 2 * b10 / (2 * Math.PI) * TL, tau = 0;
      A.path('M' + (ux - rd) + ' ' + uy + 'A' + rd + ' ' + rd + ' 0 0 1 ' + (ux + rd) + ' ' + uy, 's-line w1 dash');
      A.line(10, uy, 390, uy, 's-good w2');
      var c10 = Math.cos(10 * DEG), s10 = Math.sin(10 * DEG);
      A.line(ux, uy, ux - rd * c10, uy - rd * s10, 's-bad w1 dash'); A.line(ux, uy, ux + rd * c10, uy - rd * s10, 's-bad w1 dash');
      A.text(ux - 30, uy + 13, '红虚线 = 仰角 10°', { cls: 't-s f-bad', anchor: 'end' });
      place(dish(A, null, 'ink', 0.9), ux, uy);
      A.text(ux, uy + 13, '地面用户', { cls: 't-s', anchor: 'middle' });
      var ge = 40 * DEG, G = [ux + rd * Math.cos(ge), uy - rd * Math.sin(ge)];
      A.line(ux, uy - 10, G[0], G[1], 's-acc w1');
      place(sat(A, null, 'acc', 0.75), G[0], G[1]);
      A.text(G[0] + 16, G[1] + 4, 'GEO：不动', { cls: 't-s t-b f-acc' });
      var link = A.line(0, 0, 0, 0, 's-good w2'), ls = sat(A, null, 'good', 0.75), lt = A.text(0, 0, 'LEO', { cls: 't-s t-b f-good', anchor: 'middle' });
      var clk = A.text(8, 16, '', { cls: 't-s t-m' }), ff = A.text(8, 32, '', { cls: 't-s t-b f-gold' });
      var el1 = A.text(392, 16, '', { cls: 't-s t-b f-good', anchor: 'end' });
      A.text(392, 32, '仰角 ≥ 10° 可见 ' + vis.toFixed(1) + ' min/次', { cls: 't-s', anchor: 'end' });
      A.text(392, 48, '周期 ' + TL.toFixed(0) + ' min（开普勒）', { cls: 't-s', anchor: 'end' });
      /* the p.14 table */
      var y0 = 170, cx = [150, 256, 352];
      A.rect(4, y0 - 15, 392, 143, 'f-card s-line w1', null, 6);
      A.rect(6, y0 + 47, 388, 19, 'f-golds s-none', null, 3);
      A.text(10, y0, '参数', { cls: 't-s t-b' });
      ['LEO', 'MEO', 'GEO'].forEach(function (n, i) { A.text(cx[i], y0, n, { cls: 't-b ' + ['f-good', 'f-gold', 'f-acc'][i], anchor: 'middle' }); });
      A.line(8, y0 + 6, 392, y0 + 6, 's-line w1');
      [['轨道周期', '1.5–2 h', '5–10 h', '24 h'],
       ['高度', '500–1,500 km', '8,000–18,000 km', '35,863 km'],
       ['每次可见', '15–20 min', '2–8 h', '永久'],
       ['仰角变化', '快', '慢', '不变'],
       ['往返时延', '几 ms', '几十 ms', '约 250 ms'],
       ['覆盖直径(10°)', '约 6,000 km', '12,000–15,000 km', '16,000 km']].forEach(function (r, j) {
        var y = y0 + 22 + j * 20;
        A.text(10, y, r[0], { cls: 't-s' });
        for (var i = 0; i < 3; i++) A.text(cx[i], y, r[i + 1], { cls: 't-s t-m', anchor: 'middle' });
      });
      var phi0 = -40;
      return function (t, dt) {
        if (t === 0) tau = 0;
        var phi = phi0 + 360 * tau / TL;
        phi = ((phi + 180) % 360 + 360) % 360 - 180;
        var el = elevR(hL, phi * DEG) / DEG, up = el > -1;
        tau += (dt || 0) * (up ? 2 : 24);
        var on = el >= 0, psi = (phi < 0 ? el : 180 - el) * DEG;
        var P = [ux - rd * Math.cos(psi), uy - rd * Math.sin(psi)];
        show(ls, on); show(lt, on);
        if (on) { place(ls, P[0], P[1]); A.set(lt, { x: P[0], y: P[1] - 10 }); }
        show(link, el >= 10);
        A.set(link, { x1: ux, y1: uy - 10, x2: P[0], y2: P[1] });
        A.setText(clk, '经过 ' + tau.toFixed(1) + ' min');
        A.setText(ff, up ? '' : 'LEO 在地平线下：快进中 ▶▶');
        A.setText(el1, on ? 'LEO 仰角 ' + el.toFixed(0) + '°' + (el < 10 ? '（太低）' : '') : 'LEO 看不见');
      };
    }
  });

  /* ================= 3.1 GEO ================= */
  var G60 = elevR(HGEO, 60 * DEG) / DEG, B0 = betaR(HGEO, 0) / DEG, DLY = 2 * HGEO / CL, DLEO = 20 * Math.log10(HGEO / 1000);
  ANIM.reg('C:3.1', {
    title: 'GEO 的优点和三个代价',
    cap: '侧视图，地球和 GEO 距离按比例画（' + (HGEO / R).toFixed(1) + ' 个地球半径）。仰角、可见纬度都是由这个几何算出来的。',
    h: 240, live: true, stepDur: 4.2,
    steps: [
      'GEO 在赤道上空 35,863 km，周期 = 地球自转 24 h，所以相对地面不动。',
      '覆盖广：从卫星向地球作切线，能看到纬度 ±' + B0.toFixed(0) + '° 以内；3 颗相隔 120° 覆盖几乎全球。',
      '好跟踪：地面天线对准一次就不用动；卫星相对静止，多普勒频移很小。',
      '代价①信号弱：走 35,000 多公里，同频同功率比 1,000 km 的 LEO 弱约 ' + DLEO.toFixed(0) + ' dB。',
      '代价②时延：上下各 35,863 km，71,726 km ÷ 3×10⁵ km/s ≈ ' + DLY.toFixed(2) + ' s。',
      '代价③高纬度仰角低：纬度 60° 只有约 ' + G60.toFixed(0) + '°，' + B0.toFixed(0) + '° 以上根本看不到卫星。'
    ],
    init: function (A) {
      var O = [62, 132], re = 40, D = re * (R + HGEO) / R, S = [O[0] + D, O[1]], b0 = B0 * DEG;
      function onE(lat) { return [O[0] + re * Math.cos(lat * DEG), O[1] - re * Math.sin(lat * DEG)]; }
      A.line(O[0] + re, O[1], S[0] - 16, S[1], 's-faint w1 dash');
      var dl = A.text((O[0] + re + S[0]) / 2, O[1] - 8, '35,863 km（' + (HGEO / R).toFixed(1) + ' R）', { cls: 't-s', anchor: 'middle' });
      var g0 = A.g();
      A.text(200, 160, '周期 24 h = 地球自转一圈', { cls: 't-s t-b f-acc', anchor: 'middle' }, g0);
      A.text(200, 177, '→ 从地面看，卫星停在天上不动', { cls: 't-s f-acc', anchor: 'middle' }, g0);
      var gTan = A.g(), T1 = onE(B0), T2 = onE(-B0);
      A.line(S[0], S[1], T1[0], T1[1], 's-gold w1', gTan); A.line(S[0], S[1], T2[0], T2[1], 's-gold w1', gTan);
      A.circle(O[0], O[1], re, 'f-goods s-good w2');
      A.line(O[0] - re, O[1], O[0] + re, O[1], 's-good w1 dot');
      A.path('M' + T2[0].toFixed(1) + ' ' + T2[1].toFixed(1) + 'A' + re + ' ' + re + ' 0 0 0 ' + T1[0].toFixed(1) + ' ' + T1[1].toFixed(1), 's-gold w4', gTan);
      A.text(O[0], O[1] + re + 16, '能看到 ±' + B0.toFixed(1) + '°', { cls: 't-s t-b f-gold', anchor: 'middle' }, gTan);
      place(sat(A, null, 'acc', 1), S[0], S[1]);
      A.text(S[0], S[1] - 12, 'GEO', { cls: 't-s t-b f-acc', anchor: 'middle' });
      /* inset: 3 GEO, top view */
      var gIn = A.g(), ic = [330, 198], ir = 34;
      A.circle(ic[0], ic[1], ir, 'f-none s-acc w1 dash', gIn); A.circle(ic[0], ic[1], ir * R / (R + HGEO), 'f-good s-none', gIn);
      for (var i = 0; i < 3; i++) { var a = (90 + i * 120) * DEG; A.circle(ic[0] + ir * Math.cos(a), ic[1] - ir * Math.sin(a), 4, 'f-acc', gIn); }
      A.text(ic[0], ic[1] - ir - 8, '俯视：3 颗相隔 120°', { cls: 't-s', anchor: 'middle' }, gIn);
      /* tracking */
      var gAnt = A.g(), P0 = onE(1);
      A.line(P0[0], P0[1], S[0] - 14, S[1], 's-acc w2', gAnt); A.circle(P0[0], P0[1], 3.5, 'f-acc', gAnt);
      A.text(150, 160, '天线对准后固定不动', { cls: 't-s t-b f-acc' }, gAnt);
      A.text(150, 176, '多普勒频移很小', { cls: 't-s f-acc' }, gAnt);
      /* weak signal: wavefronts */
      var gW = A.g(), waves = [];
      for (i = 0; i < 4; i++) waves.push(A.path('', 's-acc w2', gW));
      A.text(120, 196, '同频同功率：比 1,000 km 的 LEO 弱 ' + DLEO.toFixed(1) + ' dB', { cls: 't-s t-b f-bad' }, gW);
      A.text(120, 212, '（约 ' + grp(Math.round(Math.pow(10, DLEO / 10) / 100) * 100) + ' 倍）', { cls: 't-s f-bad' }, gW);
      /* delay */
      var gD = A.g(), PA = onE(8), PB = onE(-8), pk = A.circle(0, 0, 4.5, 'f-gold', gD);
      A.circle(PA[0], PA[1], 3, 'f-ink', gD); A.circle(PB[0], PB[1], 3, 'f-ink', gD);
      A.text(PA[0] + 4, PA[1] - 8, 'A', { cls: 't-s t-b' }, gD); A.text(PB[0] + 4, PB[1] + 16, 'B', { cls: 't-s t-b' }, gD);
      var tm = A.text(150, 200, '', { cls: 't-l t-b t-m f-gold' }, gD);
      A.text(150, 218, '（动画慢放 10 倍）', { cls: 't-s' }, gD);
      /* high latitude */
      var gP = A.g(), P6 = onE(60), u6 = [Math.cos(60 * DEG), -Math.sin(60 * DEG)], tg = [-u6[1], u6[0]];
      [1, -1].forEach(function (sg) {
        var a1 = onE(sg * B0), a2 = onE(sg * (180 - B0));
        A.path('M' + a1[0].toFixed(1) + ' ' + a1[1].toFixed(1) + 'A' + re + ' ' + re + ' 0 0 ' + (sg > 0 ? 0 : 1) + ' ' + a2[0].toFixed(1) + ' ' + a2[1].toFixed(1), 's-bad w4', gP);
      });
      A.text(O[0] - 16, O[1] - re - 14, '极区看不到', { cls: 't-s t-b f-bad', anchor: 'middle' }, gP);
      A.line(P6[0] - 30 * tg[0], P6[1] - 30 * tg[1], P6[0] + 40 * tg[0], P6[1] + 40 * tg[1], 's-ink w1', gP);
      A.line(P6[0], P6[1], S[0] - 14, S[1], 's-bad w2', gP);
      var aH = Math.atan2(tg[1], tg[0]), aS = Math.atan2(S[1] - P6[1], S[0] - P6[0]);
      A.path(arcD(A, P6, 26, aH, aS), 's-bad w2', gP);
      A.circle(P6[0], P6[1], 3.5, 'f-bad', gP);
      A.text(P6[0] + 36, P6[1] - 22, '纬度 60°：仰角 ' + G60.toFixed(1) + '°', { cls: 't-s t-b f-bad' }, gP);
      var cur = 0;
      return {
        step: function (k) {
          cur = k;
          show(g0, k === 0); show(gTan, k === 1 || k === 5); show(gIn, k === 1); show(gAnt, k === 2);
          show(gW, k === 3); show(gD, k === 4); show(gP, k === 5); show(dl, k === 0 || k === 4);
        },
        frame: function (ts, dt, k) {
          if (k === 3) waves.forEach(function (w, j) {
            var p = ((ts / 2.4 + j / 4) % 1), r = 12 + p * (D - re - 8);
            A.set(w, { d: arcD(A, S, r, Math.PI - 0.35, Math.PI + 0.35), opacity: (1 - p) * 0.9 + 0.05, 'stroke-width': 3.2 * (1 - p) + 0.6 });
          });
          if (k === 4) {
            var T = DLY * 10, c = ts % (T + 1.2), p = Math.min(c / T, 1);
            mv(pk, p < 0.5 ? along([PA, S], p * 2) : along([S, PB], p * 2 - 1));
            A.setText(tm, '时延 ' + (Math.min(c / 10, DLY)).toFixed(3) + ' s');
          }
        }
      };
    }
  });

  /* ================= 3.2 LEO ================= */
  ANIM.reg('C:3.2', {
    title: 'LEO：一颗接一颗飞过，要不停切换',
    cap: '按比例画：高度 1,000 km，同一轨道面每隔 36° 一颗。服务卫星仰角低于 10°（红虚线）就切换到最高的那颗。多普勒按 2 GHz、视线方向的速度分量算：飞来为正，飞走为负。',
    h: 262,
    init: function (A) {
      var H = 262, hL = 1000, O = [200, 392], Rp = 260, rs = Rp * (R + hL) / R, sp = 36 * DEG, N = 10, U = [200, O[1] - Rp];
      var Ts = period(hL), w = 2 * Math.PI / (Ts / 60), v = 2 * Math.PI * (R + hL) / Ts;
      var orb = [];
      for (var i = -40; i <= 40; i += 2) orb.push([O[0] + rs * Math.sin(i * DEG), O[1] - rs * Math.cos(i * DEG)]);
      A.poly(orb, 's-faint w1 dash');
      A.path(discPath(A, O[0], O[1], Rp, H), 'f-goods s-good w2');
      var t10 = Math.tan(10 * DEG);
      A.line(U[0], U[1], 3, U[1] - 197 * t10, 's-bad w1 dash'); A.line(U[0], U[1], 397, U[1] - 197 * t10, 's-bad w1 dash');
      A.text(8, U[1] - 197 * t10 - 6, '仰角 10°', { cls: 't-s f-bad' });
      var link = A.line(U[0], U[1] - 10, U[0], U[1], 's-acc w2');
      place(dish(A, null, 'ink', 0.9), U[0], U[1]);
      A.text(U[0] + 12, U[1] + 14, '你', { cls: 't-s t-b' });
      var sats = [];
      for (i = 0; i < N; i++) { var g = sat(A, null, 'good', 0.7); A.text(0, -9, '#' + (i + 1), { cls: 't-s t-b f-good', anchor: 'middle' }, g); sats.push(g); }
      var clk = A.text(8, 16, '', { cls: 't-s t-m' });
      var dLEO = 20 * Math.log10(HGEO / hL);
      A.text(8, 32, 'LEO 比 GEO 信号强 ' + dLEO.toFixed(1) + ' dB（约 ' + grp(Math.round(Math.pow(10, dLEO / 10) / 100) * 100) + ' 倍）', { cls: 't-s t-b f-good' });
      var rd1 = A.text(392, 16, '', { cls: 't-s t-b f-acc', anchor: 'end' }), rd2 = A.text(392, 48, '', { cls: 't-s t-m', anchor: 'end' });
      var fl = A.text(200, 64, '', { cls: 't-b f-gold', anchor: 'middle' });
      [['Little LEO（1 GHz 以下）', '带宽 < 5 MHz，最高 10 kbps', '寻呼、跟踪、低速消息'], ['Big LEO（1 GHz 以上）', '速率可达几 Mbps', 'Little LEO 全部业务 + 话音、定位']].forEach(function (c, j) {
        c.forEach(function (s, k) { A.text(16 + j * 196, 222 + k * 16, s, { cls: k ? 't-s' : 't-s t-b' }); });
      });
      var srv = -1, flT = -9, nH = 0, lastT = -1, from = 0;
      return function (t) {
        if (t === 0 || t < lastT) { srv = -1; flT = -9; nH = 0; }
        lastT = t;
        var best = -1, bE = -99, els = [], ang = [];
        for (var i = 0; i < N; i++) {
          var a = 0.3 + w * t - i * sp;
          a = ((a + Math.PI) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI) - Math.PI;
          var e = elevR(hL, a) / DEG;
          ang.push(a); els.push(e);
          if (e > bE) { bE = e; best = i; }
          var vis = Math.abs(a) < 37 * DEG;
          show(sats[i], vis);
          if (vis) place(sats[i], O[0] + rs * Math.sin(a), O[1] - rs * Math.cos(a));
        }
        if (srv < 0) srv = best;
        else if (els[srv] < 10 && best !== srv) { from = srv; srv = best; flT = t; nH++; }
        var a2 = ang[srv];
        A.set(link, { x2: O[0] + rs * Math.sin(a2), y2: O[1] - rs * Math.cos(a2) + 5 });
        var Px = (R + hL) * Math.sin(a2), Py = (R + hL) * Math.cos(a2) - R, Vx = v * Math.cos(a2), Vy = -v * Math.sin(a2);
        var rr = (Px * Vx + Py * Vy) / Math.hypot(Px, Py), fD = -2e9 * rr / CL / 1000;
        A.setText(clk, 't = ' + t.toFixed(1) + ' min（1 秒 = 1 分钟）');
        A.setText(rd1, '服务卫星 #' + (srv + 1) + '　仰角 ' + els[srv].toFixed(0) + '°');
        A.setText(rd2, '多普勒 ' + (fD >= 0 ? '+' : '−') + Math.abs(fD).toFixed(1) + ' kHz');
        A.setText(fl, t - flT < 2.2 ? 'handoff：#' + (from + 1) + ' → #' + (srv + 1) + '（第 ' + nH + ' 次）' : '');
      };
    }
  });

  /* ================= 3.3 MEO ================= */
  ANIM.reg('C:3.3', {
    title: 'MEO：夹在 LEO 和 GEO 中间的折中',
    cap: '拖高度（对数刻度）或点按钮。都按卫星在正下方、同频同功率算：时延 = 2h/c（地面 → 卫星 → 地面），信号差 = 20 log(35,863/h)，周期由开普勒定律，覆盖直径取最低仰角 10°。',
    h: 250,
    init: function (A) {
      var l0 = Math.log10(500), l1 = Math.log10(HGEO), ay = 56, h = 10000;
      function X(hh) { return 30 + (Math.log10(hh) - l0) / (l1 - l0) * 340; }
      A.rect(X(500), ay - 16, X(1500) - X(500), 16, 'f-goods s-good w1', null, 2);
      A.rect(X(8000), ay - 16, X(18000) - X(8000), 16, 'f-golds s-gold w1', null, 2);
      A.line(X(HGEO), ay - 16, X(HGEO), ay, 's-acc w3');
      A.text((X(500) + X(1500)) / 2, ay - 4, 'LEO', { cls: 't-s t-b f-good', anchor: 'middle' });
      A.text((X(8000) + X(18000)) / 2, ay - 4, 'MEO', { cls: 't-s t-b f-gold', anchor: 'middle' });
      A.text(X(HGEO) - 5, ay - 4, 'GEO', { cls: 't-s t-b f-acc', anchor: 'end' });
      A.line(30, ay, 370, ay, 's-soft w1');
      [500, 1000, 5000, 10000, HGEO].forEach(function (v) { A.line(X(v), ay, X(v), ay + 4, 's-soft w1'); A.text(v === 500 ? 12 : X(v), ay + 15, grp(v) + (v === 500 ? ' km' : ''), { cls: 't-s', anchor: v === 500 ? 'start' : 'middle' }); });
      var mk = A.g(); A.line(0, 4, 0, 18, 's-ink w2', mk); A.path('M0 22L-5 14L5 14Z', 'f-ink s-none', mk);
      var rows = [
        { n: '时延 2h/c', f: function (x) { return 2 * x / CL * 1000; }, u: function (x) { return x.toFixed(x < 10 ? 1 : 0) + ' ms'; }, c: 'acc' },
        { n: '比 GEO 信号强', f: function (x) { return 20 * Math.log10(HGEO / x); }, u: function (x) { return x.toFixed(1) + ' dB'; }, c: 'good' },
        { n: '周期 T', f: function (x) { return period(x) / 3600; }, u: function (x) { return (x < 10 ? x.toFixed(2) : x.toFixed(1)) + ' h'; }, c: 'gold' },
        { n: '覆盖直径(10°)', f: function (x) { return 2 * betaR(x, 10) * R; }, u: function (x) { return grp(Math.round(x / 10) * 10) + ' km'; }, c: 'pur' }];
      rows.forEach(function (r, j) {
        var y = 92 + j * 24;
        r.max = Math.max(r.f(500), r.f(HGEO));
        A.text(8, y, r.n, { cls: 't-s' });
        A.rect(110, y - 10, 200, 12, 'f-card s-line w1', null, 3);
        r.bar = A.rect(110, y - 10, 0, 12, 'f-' + r.c + ' s-none', null, 3);
        r.val = A.text(392, y, '', { cls: 't-s t-b t-m', anchor: 'end' });
      });
      var z1 = A.text(8, 200, '', { cls: 't-b' }), z2 = A.text(8, 218, '', { cls: 't-s' }), z3 = A.text(8, 236, '', { cls: 't-s' });
      var Z = {
        LEO: ['区间：LEO', '卫星数：很多　切换：频繁', '典型用途：手持移动通信、成像', 'f-good'],
        MEO: ['区间：MEO（折中）', '卫星数：中　切换：较少（每次可见 2–8 h）', '典型用途：导航（GPS）；拟用于话音、数据', 'f-gold'],
        GEO: ['区间：GEO', '卫星数：3 颗覆盖全球　切换：几乎没有', '典型用途：广播电视、固定业务', 'f-acc'],
        g1: ['介于 LEO 和 MEO 之间', '讲义没有给这一段归类', '', ''], g2: ['介于 MEO 和 GEO 之间', '讲义没有给这一段归类', '', '']
      };
      var presets = [1000, 10000, HGEO], ch;
      function draw() {
        place(mk, X(h), ay - 40);
        rows.forEach(function (r) { var x = r.f(h); A.set(r.bar, { width: 200 * cl(x / r.max, 0, 1) }); A.setText(r.val, r.u(x)); });
        var z = h <= 1500 ? Z.LEO : h < 8000 ? Z.g1 : h <= 18000 ? Z.MEO : h < HGEO ? Z.g2 : Z.GEO;
        A.setText(z1, z[0]); A.set(z1, { cls: 't-b ' + z[3] }); A.setText(z2, z[1]); A.setText(z3, z[2]);
        if (ch) ch.set(presets.indexOf(h), true);
      }
      function hOf(v) { return v >= l1 - 1e-6 ? HGEO : Math.round(Math.pow(10, v)); }
      var sl = A.slider({ label: '高度 h（对数）', min: l0, max: l1, step: 'any', value: Math.log10(h), fmt: function (v) { return grp(hOf(v)) + ' km'; }, on: function (v) { h = hOf(v); draw(); } });
      ch = A.choice({ options: ['LEO 1,000 km', 'MEO 10,000 km', 'GEO 35,863 km'], value: 1, on: function (i) { sl.set(i === 2 ? l1 : Math.log10(presets[i])); } });
      draw();
      return {};
    }
  });

  /* ================= 4.1 link quality ================= */
  ANIM.reg('C:4.1', {
    title: '影响链路质量的三大因素',
    cap: '① 自由空间损耗 L = 32.44 + 20 log f(MHz) + 20 log d(km)，四条线就是讲义 p.22 的 1、4、10、40 GHz。② 覆盖区中心最强、越往外越弱（示意）。③ 仰角越低，信号穿过的大气越厚（平地近似 1/sin θ）。',
    h: 240,
    init: function (A) {
      var view = 0, vw = [A.g(), A.g(), A.g()], F = [[1, 'good'], [4, 'acc'], [10, 'gold'], [40, 'bad']];
      function L(f, d) { return 32.44 + 20 * Math.log10(f * 1000) + 20 * Math.log10(d); }
      /* ① FSPL vs altitude */
      var g = vw[0];
      var ax = A.axes({ parent: g, x: 48, y: 22, w: 290, h: 178, xr: [2, 5], yr: [120, 230], xAxisAt: 'bottom', yAxisAt: 'left', grid: true,
        ticksX: [{ v: 2, l: '100' }, { v: 3, l: '1,000' }, { v: 4, l: '10,000' }, { v: 5, l: '100,000' }], ticksY: [140, 160, 180, 200, 220], yl: 'L (dB)' });
      A.text(193, 232, '轨道高度 d（km，对数刻度）', { cls: 't-s', anchor: 'middle' }, g);
      [[3, 'LEO'], [Math.log10(HGEO), 'GEO']].forEach(function (m) { A.line(ax.X(m[0]), 30, ax.X(m[0]), 200, 's-faint w1 dot', g); A.text(ax.X(m[0]) + 3, 34, m[1], { cls: 't-s' }, g); });
      F.forEach(function (f) {
        A.curve(ax, [[2, L(f[0], 100)], [5, L(f[0], 1e5)]], 's-' + f[1] + ' w2', g);
        A.text(ax.X(5) + 4, ax.Y(L(f[0], 1e5)) + 4, f[0] + ' GHz', { cls: 't-s t-b f-' + f[1] }, g);
      });
      var vl = A.line(0, 22, 0, 200, 's-ink w1', g), dots = F.map(function (f) { return A.circle(0, 0, 3.5, 'f-' + f[1], g); });
      /* ② distance from aim point */
      g = vw[1];
      var S2 = [200, 34], gy = 186;
      [[150, 'op3'], [100, 'op5'], [50, 'op7']].forEach(function (b) { A.poly([[S2[0], S2[1] + 6], [S2[0] - b[0], gy], [S2[0] + b[0], gy]], 'f-accs s-none ' + b[1], g); });
      A.line(20, gy, 380, gy, 's-good w2', g);
      place(sat(A, g, 'ink', 1), S2[0], S2[1]);
      A.path('M200 ' + (gy - 6) + 'L196 ' + (gy + 2) + 'L204 ' + (gy + 2) + 'Z', 'f-bad s-none', g);
      A.text(200, gy + 18, '瞄准点（覆盖区中心）', { cls: 't-s t-b f-bad', anchor: 'middle' }, g);
      var st = dish(A, g, 'gold', 1), pw = A.rect(8, 30, 0, 10, 'f-gold s-none', g, 2);
      A.text(8, 22, '下行接收功率（示意）', { cls: 't-s' }, g); A.rect(8, 30, 110, 10, 'f-none s-line w1', g, 2);
      var pwt = A.text(8, 56, '', { cls: 't-s t-b f-gold' }, g);
      /* ③ atmosphere */
      g = vw[2];
      var P0 = [40, 196], top = 110;
      A.rect(0, top, 400, P0[1] - top, 'f-accs s-none op5', g, 0);
      A.text(392, P0[1] - 6, '大气层（氧气、水汽）', { cls: 't-s', anchor: 'end' }, g);
      [[175, 128, 16], [195, 122, 20], [218, 128, 16]].forEach(function (c) { A.circle(c[0], c[1], c[2], 'f-line s-none', g); });
      for (var i = 0; i < 6; i++) A.line(172 + i * 9, 146, 168 + i * 9, 160, 's-acc w1', g);
      A.text(244, 140, '雨', { cls: 't-s t-b' }, g);
      A.line(0, P0[1], 400, P0[1], 's-good w2', g);
      place(dish(A, g, 'ink', 0.9), P0[0], P0[1]);
      var rayIn = A.line(0, 0, 0, 0, 's-bad w4', g), rayOut = A.line(0, 0, 0, 0, 's-acc w2 dash', g), arc = A.path('', 's-ink w1', g), tl = A.text(0, 0, 'θ', { cls: 't-s t-b' }, g);
      var r1 = A.text(8, 22, '', { cls: 't-b f-bad' }, g);
      A.text(8, 40, '仰角低于 10° 时衰减急剧增大（雨 > 雾）', { cls: 't-s' }, g);
      A.text(8, 216, '雨衰：频率越高越严重（Ku、Ka ≫ C）', { cls: 't-s t-b' }, g);
      A.text(8, 232, '→ Ku/Ka 链路要留较大的雨衰余量', { cls: 't-s' }, g);
      var ld = Math.log10(HGEO), off = 0.5, th = 30;
      function draw() {
        vw.forEach(function (v, j) { show(v, j === view); });
        [s0, s1, s2].forEach(function (s, j) { s.input.parentNode.style.display = j === view ? '' : 'none'; });
        if (view === 0) {
          A.set(vl, { x1: ax.X(ld), x2: ax.X(ld) });
          var d = Math.pow(10, ld);
          dots.forEach(function (c, j) { mv(c, [ax.X(ld), ax.Y(L(F[j][0], d))]); });
          A.note('d = ' + grp(d) + ' km：' + F.map(function (f) { return f[0] + ' GHz ' + L(f[0], d).toFixed(1); }).join(' · ') + ' dB');
        } else A.note('');
        if (view === 1) {
          place(st, 200 + off * 150, gy);
          var p = 1 - 0.75 * off * off;
          A.set(pw, { width: 110 * p });
          A.setText(pwt, off < 0.15 ? '在中心：最强' : off > 0.8 ? '在边缘：最弱' : '离中心越远越弱');
        }
        if (view === 2) {
          var c = Math.cos(th * DEG), s = Math.sin(th * DEG), lin = (P0[1] - top) / s;
          var e1 = [P0[0] + lin * c, top], len = Math.min((396 - P0[0]) / Math.max(c, 1e-3), (P0[1] - 66) / s), e2 = [P0[0] + len * c, P0[1] - len * s];
          if (lin > len) e1 = e2;
          A.set(rayIn, { x1: P0[0], y1: P0[1] - 8, x2: e1[0], y2: e1[1] });
          A.set(rayOut, { x1: e1[0], y1: e1[1], x2: e2[0], y2: e2[1] });
          A.set(arc, { d: arcD(A, [P0[0], P0[1] - 8], 30, 0, -th * DEG) });
          A.set(tl, { x: P0[0] + 34 * Math.cos(th * DEG / 2) + 2, y: P0[1] - 8 - 34 * Math.sin(th * DEG / 2) + 4 });
          A.setText(r1, '穿过的大气 ≈ 正上方的 ' + (1 / s).toFixed(1) + ' 倍');
        }
      }
      A.choice({ options: ['① 距离与频率', '② 离瞄准点', '③ 大气与雨'], value: 0, on: function (i) { view = i; draw(); } });
      var s0 = A.slider({ label: '高度 d', min: 2, max: 5, step: 'any', value: ld, fmt: function (v) { return grp(Math.pow(10, v)) + ' km'; }, on: function (v) { ld = v; draw(); } });
      var s1 = A.slider({ label: '离中心', min: 0, max: 1, step: 0.01, value: off, fmt: function (v) { return Math.round(v * 100) + '% 半径'; }, on: function (v) { off = v; draw(); } });
      var s2 = A.slider({ label: '仰角 θ', min: 5, max: 90, step: 1, value: th, fmt: function (v) { return v + '°'; }, on: function (v) { th = v; draw(); } });
      draw();
      return {};
    }
  });

  /* ================= 4.2 configurations ================= */
  ANIM.reg('C:4.2', {
    title: '三种通信配置',
    cap: '点按钮切换配置，看信号怎么走。双向星形网里远端站（VSAT）之间不直接通，要经 hub 转发：远端站 → 卫星 → hub → 卫星 → 远端站。',
    h: 222,
    init: function (A) {
      var S = [200, 50], gy = 176, mode = 0, xs = [140, 200, 260, 320, 376];
      A.rect(0, gy, 400, 46, 'f-goods s-none', null, 0); A.line(0, gy, 400, gy, 's-good w2');
      place(sat(A, null, 'ink', 1.1), S[0], S[1]);
      var ttl = A.text(200, 18, '', { cls: 't-b', anchor: 'middle' }), sub = A.text(200, 212, '', { cls: 't-s', anchor: 'middle' });
      var L = [A.g(), A.g(), A.g()];
      function stn(g, x, lab, c, s) { place(dish(A, g, c, s), x, gy); A.line(x, gy - 13 * s, S[0], S[1] + 6, 's-faint w1 dash', g); A.text(x, gy + 16, lab, { cls: 't-s t-b', anchor: 'middle' }, g); }
      stn(L[0], 40, '大站 A', 'ink', 1.4); stn(L[0], 360, '大站 B', 'ink', 1.4);
      A.text(200, gy + 16, '～ 大洋 ～', { cls: 't-s f-acc', anchor: 'middle' }, L[0]);
      stn(L[1], 40, '发射站', 'acc', 1.4); xs.forEach(function (x) { stn(L[1], x, '只收', 'soft', 0.8); });
      stn(L[2], 40, 'hub 中心站', 'pur', 1.5); xs.forEach(function (x, i) { stn(L[2], x, 'VSAT' + (i + 1), 'soft', 0.8); });
      var T = ['点对点：卫星连接两个相距很远的地面站', '广播：一个发射站 → 许多只有接收机的站', '双向星形：一个 hub + 许多远端站'];
      var U = ['例：跨洋干线（双向）', '例：卫星电视', '例：VSAT 网（银行网点、加油站）'];
      var pk = [0, 1, 2, 3, 4].map(function () { return A.circle(0, 0, 4.5, 'f-acc'); });
      A.choice({ options: ['点对点', '广播', '星形 VSAT'], value: 0, on: function (i) { mode = i; set(); A.redraw(); } });
      function set() { L.forEach(function (g, j) { show(g, j === mode); }); A.setText(ttl, T[mode]); A.setText(sub, U[mode]); }
      set();
      function top(x, s) { return [x, gy - 13 * s]; }
      return function (t) {
        var c, i;
        pk.forEach(function (p) { show(p, false); });
        if (mode === 0) {
          c = t % 4; var ab = c < 2, p = (c % 2) / 1.6;
          if (p <= 1) { show(pk[0], true); A.set(pk[0], { cls: ab ? 'f-acc' : 'f-gold' }); mv(pk[0], along(ab ? [top(40, 1.4), S, top(360, 1.4)] : [top(360, 1.4), S, top(40, 1.4)], p)); }
        } else if (mode === 1) {
          c = t % 3.2;
          if (c < 1.2) { show(pk[0], true); A.set(pk[0], { cls: 'f-acc' }); mv(pk[0], along([top(40, 1.4), S], c / 1.2)); }
          else if (c < 2.6) for (i = 0; i < 5; i++) { show(pk[i], true); A.set(pk[i], { cls: 'f-gold' }); mv(pk[i], along([S, top(xs[i], 0.8)], (c - 1.2) / 1.4)); }
        } else {
          c = t % 6;
          if (c < 2.4) { show(pk[0], true); A.set(pk[0], { cls: 'f-acc' }); mv(pk[0], along([top(xs[0], 0.8), S, top(40, 1.5)], c / 2.4)); }
          else if (c < 4.8) { show(pk[0], true); A.set(pk[0], { cls: 'f-pur' }); mv(pk[0], along([top(40, 1.5), S, top(xs[3], 0.8)], (c - 2.4) / 2.4)); }
          A.setText(sub, c < 2.4 ? '第 1 跳：VSAT1 → 卫星 → hub' : c < 4.8 ? '第 2 跳：hub 转发 → 卫星 → VSAT4' : U[2]);
        }
      };
    }
  });

  /* ================= 4.3 ground stations ================= */
  ANIM.reg('C:4.3', {
    title: '地面站：天线越大，增益越高',
    cap: '抛物面天线增益 ∝ 口径面积 ∝ D²，所以两副天线的增益差 = 20 log(D₂/D₁) dB：直径加倍 +6 dB；0.6 m → 6 m 多 20 dB。天线画的大小用的是对数比例。',
    h: 222,
    init: function (A) {
      A.text(8, 14, '地面站的组成：', { cls: 't-s' });
      var parts = ['天线', '跟踪系统', '接收机', '发射机', '复用器', '调制解调器', '地面链路'], x = 8;
      parts.forEach(function (p) { var w = p.length * 10.5 + 10; A.rect(x, 20, w, 20, 'f-card s-line w1', null, 4); A.text(x + w / 2, 34, p, { cls: 't-s', anchor: 'middle' }); x += w + 6; });
      var l0 = Math.log10(0.3), l1 = Math.log10(60), D = 6;
      function X(d) { return 30 + (Math.log10(d) - l0) / (l1 - l0) * 340; }
      var cx = 100, gy = 170;
      A.line(10, gy, 190, gy, 's-good w2');
      var bowl = A.path('', 'f-accs s-acc w2'), ped = A.line(0, 0, 0, 0, 's-ink w3'), feed = A.line(0, 0, 0, 0, 's-acc w1'), fd = A.circle(0, 0, 2.5, 'f-acc');
      [[0.3, 0.9, 'good', 'VSAT 0.3–0.9 m'], [1, 10, 'gold', '小型 1–10 m'], [10, 60, 'acc', '大型 10–60 m']].forEach(function (z) {
        A.rect(X(z[0]), 184, X(z[1]) - X(z[0]), 9, 'f-' + z[2] + ' s-none op7', null, 2);
        A.text((X(z[0]) + X(z[1])) / 2, 208, z[3], { cls: 't-s t-b f-' + z[2], anchor: 'middle' });
      });
      var mk = A.path('M0 0L-5 -8L5 -8Z', 'f-ink s-none');
      var tD = A.text(212, 66, '', { cls: 't-l t-b t-m' }), tC = A.text(212, 86, '', { cls: 't-s t-b' });
      A.text(212, 112, '和 0.6 m 的 VSAT 比，增益', { cls: 't-s' });
      var tG = A.text(212, 134, '', { cls: 't-l t-b t-m f-good' });
      A.text(212, 158, '直径加倍 → 增益 ×4 = +' + (20 * Math.log10(2)).toFixed(1) + ' dB', { cls: 't-s' });
      function draw() {
        var r = 10 + 60 * (Math.log10(D) - l0) / (l1 - l0), yr = gy - 0.75 * r - 12, yb = yr + 0.45 * r;
        A.set(bowl, { d: 'M' + (cx - r).toFixed(1) + ' ' + yr.toFixed(1) + 'Q' + cx + ' ' + (yr + 0.9 * r).toFixed(1) + ' ' + (cx + r).toFixed(1) + ' ' + yr.toFixed(1) + 'Z' });
        A.set(ped, { x1: cx, y1: yb, x2: cx, y2: gy }); A.set(feed, { x1: cx, y1: yb, x2: cx, y2: yr - 0.35 * r }); A.set(fd, { cx: cx, cy: yr - 0.35 * r });
        mk.setAttribute('transform', 'translate(' + X(D).toFixed(1) + ',184)');
        A.setText(tD, 'D = ' + (D < 1 ? D.toFixed(2) : D < 10 ? D.toFixed(1) : D.toFixed(0)) + ' m');
        A.setText(tC, D <= 0.9 ? 'VSAT（0.3–0.9 m）' : D < 1 ? '介于 VSAT 和小型之间' : D <= 10 ? '小型地面站（1–10 m）' : '大型地面站（10–60 m）');
        var g = 20 * Math.log10(D / 0.6);
        A.setText(tG, (g >= 0 ? '+' : '−') + Math.abs(g).toFixed(1) + ' dB（×' + A.fmt(Math.pow(10, g / 10), 3) + '）');
      }
      var sl = A.slider({ label: '直径 D（对数）', min: l0, max: l1, step: 'any', value: Math.log10(D), fmt: function (v) { var d = Math.pow(10, v); return (d < 1 ? d.toFixed(2) : d < 10 ? d.toFixed(1) : d.toFixed(0)) + ' m'; }, on: function (v) { D = Math.pow(10, v); draw(); } });
      A.button('0.6 m VSAT', function () { sl.set(Math.log10(0.6)); });
      A.button('6 m', function () { sl.set(Math.log10(6)); });
      A.button('60 m', function () { sl.set(l1); });
      draw();
      return {};
    }
  });

  /* ================= 4.4 frequency bands ================= */
  var BANDS = [['L', 1, 2, '移动卫星业务 MSS'], ['S', 2, 4, 'MSS、NASA、深空研究'], ['C', 4, 8, '固定卫星业务 FSS'], ['X', 8, 12.5, 'FSS 军用、地面探测、气象卫星'],
    ['Ku', 12.5, 18, 'FSS、广播卫星业务 BSS'], ['K', 18, 26.5, 'BSS、FSS'], ['Ka', 26.5, 40, 'FSS']];
  ANIM.reg('C:4.4', {
    title: '卫星频段：越高越宽，也越怕雨',
    cap: '色块宽度就是各频段的总带宽（讲义 p.27 的表）。拖频率看：所在频段、用途、比 4 GHz 多出的自由空间损耗 20 log(f/4)。例：12 GHz 比 4 GHz 多 ' + (20 * Math.log10(3)).toFixed(1) + ' dB。',
    h: 236,
    init: function (A) {
      function X(f) { return 20 + f * 9; }
      var cls = ['good', 'gold', 'acc', 'pur', 'bad', 'gold', 'acc'];
      A.text(8, 18, '规律：频段越高 → 可用带宽越大，但路径损耗和雨衰也越大', { cls: 't-s' });
      BANDS.forEach(function (b, i) {
        var x = X(b[1]), w = X(b[2]) - x;
        A.rect(x, 50, w, 36, 'f-' + cls[i] + 's s-' + cls[i] + ' w1', null, 2);
        A.text(x + w / 2, w > 24 ? 73 : 44, b[0], { cls: 't-b f-' + cls[i], anchor: 'middle' });
      });
      A.line(20, 90, 384, 90, 's-soft w1');
      [0, 10, 20, 30, 40].forEach(function (f) { A.line(X(f), 90, X(f), 94, 's-soft w1'); A.text(X(f), 106, f + (f === 40 ? ' GHz' : ''), { cls: 't-s', anchor: f === 40 ? 'end' : 'middle' }); });
      var mk = A.g(); A.line(0, 46, 0, 90, 's-ink w2', mk); A.path('M0 50L-5 41L5 41Z', 'f-ink s-none', mk);
      var t = [130, 150, 170, 190, 210, 228].map(function (y, i) { return A.text(8, y, '', { cls: i === 0 ? 't-b t-m' : 't-s' }); });
      var f = 14;
      function draw() {
        mk.setAttribute('transform', 'translate(' + X(f).toFixed(1) + ',0)');
        var k = 0; for (var i = 0; i < BANDS.length; i++) if (f >= BANDS[i][1] && (f < BANDS[i][2] || i === BANDS.length - 1)) k = i;
        var b = BANDS[k], lam = CL * 1e5 / (f * 1e9);
        A.setText(t[0], 'f = ' + f.toFixed(1) + ' GHz　波长 λ = c/f = ' + lam.toFixed(2) + ' cm');
        A.setText(t[1], '频段 ' + b[0] + '：' + b[1] + '–' + b[2] + ' GHz，总带宽 ' + (b[2] - b[1]) + ' GHz');
        A.setText(t[2], '主要用途：' + b[3]);
        var dl = 20 * Math.log10(f / 4);
        A.setText(t[3], '比 4 GHz 的自由空间损耗' + (dl >= 0 ? '多 ' : '少 ') + Math.abs(dl).toFixed(1) + ' dB（20 log(f/4)，同距离）');
        A.setText(t[4], k <= 2 ? '雨衰：小（波长比几毫米的雨滴大得多）' : k === 3 ? '雨衰：比 C 大、比 Ku 小' : '雨衰：明显（波长接近雨滴尺寸）→ 留雨衰余量');
        A.set(t[4], { cls: 't-s t-b ' + (k >= 4 ? 'f-bad' : k <= 2 ? 'f-good' : 'f-gold') });
        A.setText(t[5], k <= 1 ? '移动业务用低频段：手持终端天线小，要穿透力强' : '');
      }
      A.slider({ label: '频率 f', min: 1, max: 40, step: 0.1, value: f, fmt: function (v) { return v.toFixed(1) + ' GHz'; }, on: function (v) { f = v; draw(); } });
      draw();
      return {};
    }
  });

  /* ================= 5.1 FDMA of the transponder band ================= */
  var BW = 500, CH = 40, GB = 4, NCH = Math.floor(BW / CH), USE = CH - GB;
  ANIM.reg('C:5.1', {
    title: '先按频率切一刀：C 波段 500 MHz',
    cap: '讲义 p.28 的例子：500 MHz、40 MHz 信道、每信道 4 MHz 保护带、靠频率复用得到 24 个信道。两种极化是常见的复用做法（课外补充）；点波束是另一种。',
    h: 240, tween: 1.2,
    steps: [
      'C 波段卫星总带宽 ' + BW + ' MHz。先用 FDMA 把它切成若干物理信道，信道里面再细分。',
      '每个信道 ' + CH + ' MHz，' + BW + ' MHz 里放得下 ' + NCH + ' 个（共 ' + NCH * CH + ' MHz）。',
      '每个信道含 ' + GB + ' MHz 保护带：真正可用 ' + USE + ' MHz，保护带占 ' + (GB / CH * 100).toFixed(0) + '%。',
      '频率复用：两种正交极化（H/V）各放一遍 → ' + 2 * NCH + ' 个信道，等效 ' + 2 * NCH * CH + ' MHz。',
      '另一种复用：窄的点波束。不相邻的地区重复用同一频率，互不干扰。'
    ],
    init: function (A) {
      var k0 = 0.68;
      function X(m) { return 40 + m * k0; }
      var tot = A.g(), rowH = A.g(), rowV = A.g(), zoom = A.g(), spot = A.g();
      A.rect(X(0), 44, BW * k0, 22, 'f-accs s-acc w1', tot, 2);
      A.text(X(BW / 2), 59, BW + ' MHz', { cls: 't-b f-acc', anchor: 'middle' }, tot);
      A.text(X(0), 34, 'C 波段转发器总带宽', { cls: 't-s' }, tot);
      function row(g, y, c, n0, lab) {
        for (var i = 0; i < NCH; i++) {
          A.rect(X(i * CH), y, USE * k0, 22, 'f-' + c + ' s-none', g, 1);
          A.rect(X(i * CH + USE), y, GB * k0, 22, 'f-bad s-none', g, 0);
          A.text(X(i * CH + USE / 2), y + 15, String(n0 + i), { cls: 't-s t-b f-card', anchor: 'middle' }, g);
        }
        A.rect(X(NCH * CH), y, (BW - NCH * CH) * k0, 22, 'f-line s-none op5', g, 0);
        A.text(8, y + 15, lab, { cls: 't-s t-b f-' + c }, g);
      }
      row(rowH, 44, 'acc', 1, 'H'); row(rowV, 72, 'gold', NCH + 1, 'V');
      A.line(X(0), 99, X(0), 104, 's-soft w1'); A.line(X(BW), 99, X(BW), 104, 's-soft w1');
      var info = A.text(200, 116, '', { cls: 't-s t-b', anchor: 'middle' });
      A.path('M' + X(0) + ' 66L60 130M' + X(CH) + ' 66L340 130', 's-faint w1 dot', zoom);
      A.rect(60, 130, 280 * USE / CH, 32, 'f-accs s-acc w1', zoom, 2);
      A.rect(60 + 280 * USE / CH, 130, 280 * GB / CH, 32, 'f-bads s-bad w1', zoom, 2);
      A.text(60 + 140 * USE / CH, 151, '可用 ' + USE + ' MHz', { cls: 't-b f-acc', anchor: 'middle' }, zoom);
      A.text(340, 178, '↑ 保护带 ' + GB + ' MHz（' + (GB / CH * 100).toFixed(0) + '%）', { cls: 't-s t-b f-bad', anchor: 'end' }, zoom);
      A.text(60, 178, '一个信道 = ' + CH + ' MHz', { cls: 't-s' }, zoom);
      var hc = [250, 194], fr = ['f1', 'f2', 'f3', 'f2', 'f3', 'f2', 'f3'], fc = { f1: 'acc', f2: 'gold', f3: 'good' };
      for (var i = 0; i < 7; i++) {
        var a = (i - 1) * Math.PI / 3, px = i ? hc[0] + 30 * Math.cos(a) : hc[0], py = i ? hc[1] + 30 * Math.sin(a) : hc[1];
        A.circle(px, py, 16, 'f-' + fc[fr[i]] + 's s-' + fc[fr[i]] + ' w2', spot);
        A.text(px, py + 4, fr[i], { cls: 't-s t-b', anchor: 'middle' }, spot);
      }
      ['点波束：', '同色 = 同一频率', '不相邻的区域', '可以重复使用'].forEach(function (s, j) { A.text(16, 166 + j * 17, s, { cls: j ? 't-s' : 't-s t-b' }, spot); });
      var cur = 0;
      return {
        step: function (k) {
          cur = k;
          show(tot, k === 0); show(rowH, k >= 1); show(rowV, k >= 3); show(zoom, k === 2); show(spot, k === 4);
          [tot, rowH, rowV, zoom, spot].forEach(function (g) { op(g, 1); });
          A.setText(info, k === 1 ? NCH + ' × ' + CH + ' = ' + NCH * CH + ' MHz（灰色是剩下的 ' + (BW - NCH * CH) + ' MHz）' : k >= 3 ? 2 * NCH + ' × ' + CH + ' = ' + 2 * NCH * CH + ' MHz 等效带宽，装进 ' + BW + ' MHz' : '');
        },
        frame: function (ts, dt, k) {
          var p = A.prog(ts, 0.9);
          op(k === 0 ? tot : k === 1 ? rowH : k === 2 ? zoom : k === 3 ? rowV : spot, p);
        }
      };
    }
  });

  /* ================= 5.2 FAMA vs DAMA ================= */
  ANIM.reg('C:5.2', {
    title: '固定分配 FAMA vs 按需分配 DAMA',
    cap: '上：8 个子信道怎么分给 4 个站（需求是举例）。下：DAMA-FDMA 的公共信令信道 CSC，一帧 50 个时隙。',
    h: 250, tween: 1.2, live: true,
    steps: [
      '<b>FAMA</b> 固定分配：每站预先固定 2 个子信道。A 要 4 个不够用，C 一个不用却占着。',
      '<b>DAMA</b> 按需分配：子信道组成公共池，按各站当下的需求分；需求变了就重新分。',
      '分配靠公共信令信道 <b>CSC</b>：反复发送一个 TDMA 帧，共 50 个时隙，第 1 个用于同步。',
      '其余 49 个时隙永久分给 49 个地面站。A 要和 B 全双工通话，选好一对子信道 #3、#4。',
      'A 在自己的时隙里广播"我用 #3、#4"；别的站看到后就不再选这两个。',
      '类比：会议室门口的预约白板，每部门固定一格。为了公平，还需要一个集中调度器。'
    ],
    init: function (A) {
      var SC = ['acc', 'gold', 'good', 'pur'], SN = ['A', 'B', 'C', 'D'], need = [4, 2, 0, 1], sx = [95, 175, 255, 335];
      A.text(8, 36, '子信道', { cls: 't-s' });
      var box = [], lines = A.g();
      for (var i = 0; i < 8; i++) { box.push(A.rect(62 + i * 40, 22, 34, 22, 'f-card s-line w1', null, 3)); A.text(79 + i * 40, 37, '#' + (i + 1), { cls: 't-s t-b', anchor: 'middle' }); }
      var stl = [];
      sx.forEach(function (x, j) {
        A.rect(x - 22, 88, 44, 24, 'f-' + SC[j] + 's s-' + SC[j] + ' w1', null, 5);
        A.text(x, 105, '站 ' + SN[j], { cls: 't-s t-b f-' + SC[j], anchor: 'middle' });
        stl.push(A.text(x, 128, '', { cls: 't-s', anchor: 'middle' }));
      });
      var csc = A.g(), slots = [];
      A.text(8, 166, 'CSC：一帧 50 个时隙（反复发送）', { cls: 't-s t-b' }, csc);
      for (i = 0; i < 50; i++) slots.push(A.rect(25 + i * 7, 174, 6, 18, i ? 'f-card s-line w1' : 'f-soft s-none', csc, 1));
      A.text(25, 206, '↑ 时隙 1：同步', { cls: 't-s' }, csc);
      A.text(375, 206, '时隙 2–50：49 个站各一格', { cls: 't-s', anchor: 'end' }, csc);
      var msg = A.text(8, 228, '', { cls: 't-s t-b f-acc' }), msg2 = A.text(8, 245, '', { cls: 't-s' });
      var cur = 0;
      function link(i, j, cls) { A.line(79 + i * 40, 44, sx[j], 88, cls, lines); }
      return {
        step: function (k) {
          cur = k;
          while (lines.firstChild) lines.removeChild(lines.firstChild);
          var own = [];
          if (k === 0) for (i = 0; i < 8; i++) own.push([Math.floor(i / 2), i % 2 < need[Math.floor(i / 2)]]);
          else if (k === 1) { var o = [0, 0, 0, 0, 1, 1, 3, -1]; for (i = 0; i < 8; i++) own.push([o[i], o[i] >= 0]); }
          else for (i = 0; i < 8; i++) own.push(k >= 3 && i === 2 ? [0, true] : k >= 3 && i === 3 ? [1, true] : [-1, false]);
          own.forEach(function (w, i) {
            if (w[0] < 0) { A.set(box[i], { cls: 'f-card s-line w1' }); return; }
            A.set(box[i], { cls: w[1] ? 'f-' + SC[w[0]] + 's s-' + SC[w[0]] + ' w2' : 'f-paper s-faint w1 dash' });
            link(i, w[0], w[1] ? 's-' + SC[w[0]] + ' w2' : 's-faint w1 dash');
          });
          stl.forEach(function (t, j) {
            var txt = '', c = 't-s';
            if (k === 0) { txt = need[j] > 2 ? '需 ' + need[j] + '，缺 ' + (need[j] - 2) : need[j] < 2 ? '需 ' + need[j] + '，闲置 ' + (2 - need[j]) : '需 2，刚好'; c = need[j] > 2 ? 't-s t-b f-bad' : need[j] < 2 ? 't-s f-soft' : 't-s'; }
            else if (k === 1) { txt = '需 ' + need[j] + ' → 给 ' + need[j]; c = 't-s f-good'; }
            else if (k >= 3 && j < 2) { txt = j ? '收 #3 发 #4' : '发 #3 收 #4'; c = 't-s t-b'; }
            A.setText(t, txt); A.set(t, { cls: c });
          });
          show(csc, k >= 2);
          slots.forEach(function (s, i) { if (i) A.set(s, { cls: (k >= 3 && i === 1) ? 'f-acc s-acc w1' : 'f-card s-line w1' }); });
          A.setText(msg, k === 1 ? '#8 空闲，留给下一个请求；不再有"闲着的固定份额"' : k === 3 ? '站 A 的固定时隙是第 2 格（蓝色）' : k === 4 ? '站 A 在第 2 格广播："我用 #3、#4"' : k === 5 ? '白板 = CSC，每部门一格 = 每站一个时隙' : '');
          A.setText(msg2, k === 4 ? '其余 48 个站听到后都不会再选 #3、#4' : k === 5 ? '写上要用的会议室（子信道），别人看到就不会重复预订' : '');
        },
        frame: function (ts) { op(lines, A.prog(ts, 0.8)); if (cur === 4) op(slots[1], 0.4 + 0.6 * Math.abs(Math.cos(ts * 3))); else op(slots[1], 1); }
      };
    }
  });

  /* ================= 5.3 TDMA ================= */
  var TF = 2000, TR = 20, NST = 10, TP = 10, TG = 2, OVH = TR + NST * (TP + TG);
  ANIM.reg('C:5.3', {
    title: 'TDMA：各站轮流用上行',
    cap: '帧结构按讲义 p.32 画（宽度是示意，不按时间比例）。第 5–6 步的数字是页面例题的假设参数：帧 2 ms、参考突发 20 µs、10 个站、前导 10 µs、保护 2 µs。',
    h: 262, tween: 3.6, live: true,
    steps: [
      'TDMA：时间分成重复的帧，每帧分成时隙。10 个站轮流，各自只在自己的时隙里发上行。',
      '帧开头是<b>参考突发</b>（定时恢复、协调数据），后面是各站的数据突发，之间留<b>保护时间</b>。',
      '每个站的突发 = <b>前导</b>（定时恢复、唯一字、站识别码、控制与请求）+ <b>信息</b>。',
      '下行：卫星把整帧广播给所有站，每个站只挑出发给自己的那部分。',
      '举例：开销 = ' + TR + ' + ' + NST + ' × (' + TP + ' + ' + TG + ') = ' + OVH + ' µs，效率 = 1 − ' + OVH + '/' + TF + ' = ' + Math.round((1 - OVH / TF) * 100) + '%。',
      'FDMA 每个 ' + CH + ' MHz 信道留 ' + GB + ' MHz 保护带，效率 ' + USE + '/' + CH + ' = ' + Math.round(USE / CH * 100) + '%。这组数字下 TDMA 更高效。'
    ],
    init: function (A) {
      var S = [200, 28], gy = 104, st = [], ul = [], i;
      place(sat(A, null, 'ink', 1), S[0], S[1]);
      A.line(10, gy, 390, gy, 's-good w2');
      for (i = 0; i < NST; i++) {
        var x = 38 + i * 36;
        ul.push(A.line(x, gy - 12, S[0], S[1] + 6, 's-faint w1', null));
        st.push(dish(A, null, 'soft', 0.8)); place(st[i], x, gy);
        A.text(x, gy + 14, String(i + 1), { cls: 't-s t-b', anchor: 'middle' });
      }
      var pk = [];
      for (i = 0; i < NST; i++) pk.push(A.circle(0, 0, 3.5, 'f-acc'));
      /* frame bar */
      var fy = 132, bx = [], bursts = [];
      var ref = A.rect(14, fy, 28, 24, 'f-pur s-none', null, 2);
      A.text(28, fy + 16, '参考', { cls: 't-s t-b f-card', anchor: 'middle' });
      for (i = 0; i < NST; i++) {
        var x0 = 42 + i * 34 + 4, g = A.g();
        A.rect(x0, fy, 9, 24, 'f-gold s-none', g, 1); A.rect(x0 + 9, fy, 21, 24, 'f-acc s-none', g, 1);
        A.text(x0 + 19.5, fy + 16, String(i + 1), { cls: 't-s t-b f-card', anchor: 'middle' }, g);
        bx.push(x0); bursts.push(g);
      }
      var ann = A.g();
      A.text(14, fy + 38, '↑ 参考突发', { cls: 't-s t-b f-pur' }, ann);
      A.path('M' + (bx[2] - 2) + ' ' + (fy + 26) + 'L' + (bx[2] - 2) + ' ' + (fy + 32), 's-ink w1', ann);
      A.text(bx[2] - 2, fy + 44, '保护时间', { cls: 't-s t-b', anchor: 'middle' }, ann);
      A.text(bx[5] + 4, fy + 38, '↑ 前导', { cls: 't-s t-b f-gold' }, ann);
      A.text(bx[7] + 14, fy + 38, '↑ 信息', { cls: 't-s t-b f-acc' }, ann);
      var zm = A.g(), fl = [['定时恢复', 62], ['唯一字', 50], ['站识别码', 62], ['控制/请求', 64]], zx = 14;
      A.path('M' + bx[0] + ' ' + (fy + 24) + 'L14 196M' + (bx[0] + 30) + ' ' + (fy + 24) + 'L386 196', 's-faint w1 dot', zm);
      fl.forEach(function (f) { A.rect(zx, 196, f[1], 26, 'f-golds s-gold w1', zm, 2); A.text(zx + f[1] / 2, 213, f[0], { cls: 't-s', anchor: 'middle' }, zm); zx += f[1]; });
      A.rect(zx, 196, 386 - zx, 26, 'f-accs s-acc w1', zm, 2); A.text((zx + 386) / 2, 213, '信息', { cls: 't-s t-b', anchor: 'middle' }, zm);
      A.text(14, 240, '前导（每个突发都有）', { cls: 't-s t-b f-gold' }, zm);
      var calc = A.g();
      A.text(14, 204, '开销 = 参考 ' + TR + ' + ' + NST + ' 站 × (前导 ' + TP + ' + 保护 ' + TG + ') = ' + OVH + ' µs', { cls: 't-s' }, calc);
      A.text(14, 226, '效率 = 1 − ' + OVH + ' / ' + TF + ' = ' + Math.round((1 - OVH / TF) * 100) + '%', { cls: 't-l t-b f-acc' }, calc);
      var cmp = A.g();
      [['TDMA', 1 - OVH / TF, 'acc'], ['FDMA', USE / CH, 'gold']].forEach(function (r, j) {
        var y = 196 + j * 24;
        A.text(14, y + 11, r[0], { cls: 't-s t-b f-' + r[2] }, cmp);
        A.rect(60, y, 280, 14, 'f-card s-line w1', cmp, 3); A.rect(60, y, 280 * r[1], 14, 'f-' + r[2] + ' s-none', cmp, 3);
        A.text(392, y + 11, Math.round(r[1] * 100) + '%', { cls: 't-s t-b t-m', anchor: 'end' }, cmp);
      });
      A.text(14, 252, 'TDMA 的保护时间 + 控制比特 < FDMA 的保护带', { cls: 't-s' }, cmp);
      var cur = 0;
      return {
        step: function (k) { cur = k; show(ann, k === 1); show(zm, k === 2); show(calc, k === 4); show(cmp, k === 5); },
        frame: function (ts, dt, k) {
          var ph = (ts / 0.34) % 13, j = Math.floor(ph), f = ph - j;
          for (var i = 0; i < NST; i++) {
            var on = false, cls = 's-faint w1';
            if (k === 0) { on = j === i + 1; op(bursts[i], j > i ? 1 : 0.15); if (on) cls = 's-acc w2'; show(pk[i], on); if (on) mv(pk[i], along([[38 + i * 36, gy - 12], [S[0], S[1] + 6]], f)); }
            else if (k === 3) {
              var pp = (ts / 1.4) % 1, me = Math.floor(ts / 0.5) % NST === i;
              show(pk[i], true); A.set(pk[i], { cls: 'f-gold' }); mv(pk[i], along([[S[0], S[1] + 6], [38 + i * 36, gy - 12]], pp));
              op(bursts[i], me ? 1 : 0.25); cls = me ? 's-gold w2' : 's-gold w1 op5';
            } else { show(pk[i], false); op(bursts[i], 1); }
            if (k !== 3) A.set(pk[i], { cls: 'f-acc' });
            A.set(ul[i], { cls: cls });
          }
          op(ref, k === 0 ? (j >= 0 ? 1 : 0.15) : 1);
        }
      };
    }
  });

  /* ================= 5.4 SS/TDMA ================= */
  function perms(a) { if (a.length < 2) return [a]; var r = []; a.forEach(function (x, i) { perms(a.slice(0, i).concat(a.slice(i + 1))).forEach(function (p) { r.push([x].concat(p)); }); }); return r; }
  function fact(n) { return n < 2 ? 1 : n * fact(n - 1); }
  ANIM.reg('C:5.4', {
    title: 'SS/TDMA：卫星在天上当交换机',
    cap: '左边 3 个区域的上行波束，右边 3 个区域的下行波束。星上开关每个时隙换一种接法（模式）。模式 "BCA" 表示 A→B、B→C、C→A。完全连通要 N! 种模式。',
    h: 250,
    init: function (A) {
      var Z = ['A', 'B', 'C'], ZC = ['acc', 'gold', 'good'], ys = [72, 124, 176], P = perms([0, 1, 2]), slot = 1.8;
      A.text(40, 40, '上行波束', { cls: 't-s t-b', anchor: 'middle' }); A.text(360, 40, '下行波束', { cls: 't-s t-b', anchor: 'middle' });
      A.rect(140, 48, 120, 152, 'f-card s-ink w1', null, 8);
      A.text(200, 64, '星上交换开关', { cls: 't-s t-b', anchor: 'middle' });
      ys.forEach(function (y, i) {
        A.circle(40, y, 17, 'f-' + ZC[i] + 's s-' + ZC[i] + ' w2'); A.text(40, y + 5, Z[i], { cls: 't-b f-' + ZC[i], anchor: 'middle' });
        A.circle(360, y, 17, 'f-paper s-ink w1'); A.text(360, y + 5, Z[i], { cls: 't-b', anchor: 'middle' });
        A.line(57, y, 140, y, 's-' + ZC[i] + ' w2'); A.line(260, y, 343, y, 's-soft w1');
        A.circle(146, y, 3.5, 'f-ink'); A.circle(254, y, 3.5, 'f-ink');
      });
      var sw = ys.map(function (y, i) { return A.line(146, y, 254, y, 's-' + ZC[i] + ' w3'); });
      var pk = ys.map(function (y, i) { return A.circle(0, 0, 5, 'f-' + ZC[i]); });
      var head = A.text(200, 20, '', { cls: 't-b', anchor: 'middle' });
      A.text(8, 236, '模式', { cls: 't-s t-b' });
      var mb = P.map(function (p, j) {
        var g = A.g();
        A.rect(40 + j * 58, 220, 50, 24, 'f-card s-line w1', g, 5);
        A.text(65 + j * 58, 237, p.map(function (q) { return Z[q]; }).join(''), { cls: 't-b t-m', anchor: 'middle' }, g);
        return g;
      });
      A.note('N 个区域要 N! 种模式：N = 3 → ' + fact(3) + ' 种；N = 4 → ' + fact(4) + ' 种；N = 5 → ' + fact(5) + ' 种');
      return function (t) {
        var n = Math.floor(t / slot), m = P[n % P.length], f = (t % slot) / slot;
        ys.forEach(function (y, i) {
          A.set(sw[i], { y2: ys[m[i]] });
          var pp = cl(f / 0.8, 0, 1);
          show(pk[i], f < 0.85);
          mv(pk[i], along([[57, y], [146, y], [254, ys[m[i]]], [343, ys[m[i]]]], pp));
        });
        mb.forEach(function (g, j) { A.set(g.firstChild, { cls: j === n % P.length ? 'f-accs s-acc w2' : 'f-card s-line w1' }); });
        A.setText(head, '时隙 ' + (n + 1) + '：模式 ' + m.map(function (q) { return Z[q]; }).join('') + '　' + m.map(function (q, i) { return Z[i] + '→' + Z[q]; }).join('，'));
      };
    }
  });

  /* ================= 6.1 ISL vs gateways ================= */
  ANIM.reg('C:6.1', {
    title: '星间链路 ISL：在太空里抄近路',
    cap: '按页面例题按比例画：两颗 LEO 高 1,000 km、相距 4,000 km，都按正下方算。无线电速度 3×10⁵ km/s，光纤约 2×10⁵ km/s。动画里 1 ms 放慢成 0.12 s。',
    h: 212,
    init: function (A) {
      var k = 0.05, gy = 112, S1 = [100, gy - 1000 * k], S2 = [100 + 4000 * k, gy - 1000 * k], mode = 0;
      var UA = [86, gy - 9], UB = [314, gy - 9], G1 = [114, gy - 9], G2 = [286, gy - 9], fy = 146;
      A.rect(0, gy, 400, 212 - gy, 'f-goods s-none', null, 0); A.line(0, gy, 400, gy, 's-good w2');
      var isl = A.line(S1[0] + 15, S1[1], S2[0] - 15, S2[1], 's-pur w3');
      var islT = A.text(200, S1[1] - 8, '星间链路 ISL 4,000 km', { cls: 't-s t-b f-pur', anchor: 'middle' });
      var gw = A.g();
      A.path('M' + G1[0] + ' ' + gy + 'L' + G1[0] + ' ' + fy + 'L' + G2[0] + ' ' + fy + 'L' + G2[0] + ' ' + gy, 's-ink w2 dash', gw);
      A.text(200, fy - 6, '地面网络（光纤约 4,000 km）', { cls: 't-s', anchor: 'middle' }, gw);
      place(dish(A, gw, 'pur', 1), G1[0], gy); place(dish(A, gw, 'pur', 1), G2[0], gy);
      A.text(G1[0] + 12, gy + 14, '网关 1', { cls: 't-s t-b f-pur' }, gw); A.text(G2[0] - 12, gy + 14, '网关 2', { cls: 't-s t-b f-pur', anchor: 'end' }, gw);
      place(sat(A, null, 'ink', 0.9), S1[0], S1[1]); place(sat(A, null, 'ink', 0.9), S2[0], S2[1]);
      A.text(S1[0], S1[1] - 10, '卫星 1', { cls: 't-s', anchor: 'middle' }); A.text(S2[0], S2[1] - 10, '卫星 2', { cls: 't-s', anchor: 'middle' });
      A.circle(UA[0], UA[1], 5, 'f-gold'); A.circle(UB[0], UB[1], 5, 'f-gold');
      A.text(UA[0] - 8, UA[1] + 4, '用户 A', { cls: 't-s t-b', anchor: 'end' }); A.text(UB[0] + 8, UB[1] + 4, '用户 B', { cls: 't-s t-b' });
      var hops = A.g(), pk = A.circle(0, 0, 5, 'f-bad');
      var t1 = A.text(8, 18, '', { cls: 't-b' }), tm = A.text(392, 18, '', { cls: 't-b t-m f-bad', anchor: 'end' });
      var r1 = A.text(8, 178, '', { cls: 't-s' }), r2 = A.text(8, 196, '', { cls: 't-s t-b' });
      /* segments: [from, to, km, speed km/s, kind] */
      var PATHS = [
        [[UA, S1, 1000, CL, 'up'], [S1, S2, 4000, CL, 'isl'], [S2, UB, 1000, CL, 'down']],
        [[UA, S1, 1000, CL, 'up'], [S1, G1, 1000, CL, 'down'], [G1, [G1[0], fy], 0, 2e5, 'f'], [[G1[0], fy], [G2[0], fy], 4000, 2e5, 'f'], [[G2[0], fy], G2, 0, 2e5, 'f'], [G2, S2, 1000, CL, 'up'], [S2, UB, 1000, CL, 'down']]];
      function build() {
        while (hops.firstChild) hops.removeChild(hops.firstChild);
        PATHS[mode].forEach(function (s) { if (s[4] !== 'f' && s[4] !== 'isl') A.line(s[0][0], s[0][1], s[1][0], s[1][1], s[4] === 'up' ? 's-acc w2' : 's-gold w2', hops); });
        show(isl, mode === 0); show(islT, mode === 0); op(gw, mode === 0 ? 0.3 : 1);
        var radio = 0, fib = 0, nu = 0, nd = 0;
        PATHS[mode].forEach(function (s) { if (s[4] === 'f') fib += s[2]; else radio += s[2]; if (s[4] === 'up') nu++; if (s[4] === 'down') nd++; });
        var tr = radio / CL * 1000, tf = fib / 2e5 * 1000;
        A.setText(t1, (mode ? '无 ISL：' : '有 ISL：') + nu + ' 条上行（蓝）+ ' + nd + ' 条下行（金）');
        A.setText(r1, '无线 ' + grp(radio) + ' km → ' + tr.toFixed(1) + ' ms' + (fib ? '；光纤 ' + grp(fib) + ' km → ' + tf.toFixed(1) + ' ms' : ''));
        A.setText(r2, '合计约 ' + Math.round(tr + tf) + ' ms；' + (mode ? '要经过 2 个地面网关' : '不经过地面网关'));
      }
      A.choice({ options: ['有星间链路', '没有星间链路'], value: 0, on: function (i) { mode = i; build(); A.redraw(); } });
      build();
      return function (t) {
        var segs = PATHS[mode], tot = 0, i;
        var dur = segs.map(function (s) { return s[2] / s[3] * 1000; });
        dur.forEach(function (d) { tot += d; });
        var ms = (t / 0.12) % (tot + 8), left = Math.min(ms, tot);
        for (i = 0; i < segs.length; i++) { if (left <= dur[i] || i === segs.length - 1) break; left -= dur[i]; }
        var f = dur[i] ? cl(left / dur[i], 0, 1) : 1;
        mv(pk, along([segs[i][0], segs[i][1]], f));
        A.setText(tm, (Math.min(ms, tot)).toFixed(1) + ' ms');
      };
    }
  });

  /* ================= 6.2 four handoffs ================= */
  ANIM.reg('C:6.2', {
    title: '四种切换：看"谁变了"',
    cap: '每一步演示一种切换：红线是你当前的通信链路，紫色虚线是卫星到地面网关的链路。',
    h: 236, tween: 3.6, stepDur: 4.6,
    steps: [
      '<b>星内切换</b> Intra-satellite：还是同一颗卫星，你从它的一个波束（扇区）走进另一个波束。',
      '<b>星间切换</b> Inter-satellite：你站着不动，但卫星飞走了，通话转给下一颗卫星。',
      '<b>网关切换</b> Gateway：卫星飞离了原来连接的地面网关，改连另一个网关。',
      '<b>系统间切换</b> Inter-system：从野外进城，卫星网络转到地面蜂窝（4G），是垂直切换。',
      '关键看"谁变了"：波束变 → 星内；卫星变 → 星间；网关变 → 网关；系统变 → 系统间。'
    ],
    init: function (A) {
      var gy = 186, sy = 52;
      A.rect(0, gy, 400, 236 - gy, 'f-goods s-none', null, 0); A.line(0, gy, 400, gy, 's-good w2');
      var clip = A.el('clipPath', { id: 'anC62clip' }); A.rect(0, 0, 400, 236, 'f-ink', clip, 0);
      var scene = A.g({ 'clip-path': 'url(#anC62clip)' });
      function mkSat(c1, c2, n) {
        var g = A.g({}, scene);
        A.poly([[0, 6], [-80, gy - sy], [0, gy - sy]], 'f-' + c1 + ' s-none', g);
        A.poly([[0, 6], [80, gy - sy], [0, gy - sy]], 'f-' + c2 + ' s-none', g);
        sat(A, g, 'ink', 0.85);
        A.text(0, -10, n, { cls: 't-s t-b', anchor: 'middle' }, g);
        return g;
      }
      var city = A.g();
      [[318, 26], [334, 40], [352, 30], [384, 22]].forEach(function (b) { A.rect(b[0], gy - b[1], 14, b[1], 'f-line s-soft w1', city, 1); });
      A.line(370, gy, 370, gy - 46, 's-ink w2', city); A.path('M362 ' + (gy - 46) + 'L370 ' + (gy - 56) + 'L378 ' + (gy - 46), 's-ink w2', city);
      A.text(392, gy - 60, '4G 基站', { cls: 't-s t-b', anchor: 'end' }, city);
      A.text(340, gy + 16, '城市', { cls: 't-s', anchor: 'middle' }, city);
      var s1 = mkSat('accs', 'golds', '卫星 1'), s2 = mkSat('purs', 'goods', '卫星 2');
      var bt = [A.text(0, 0, '波束 1', { cls: 't-s t-b f-acc', anchor: 'middle' }), A.text(0, 0, '波束 2', { cls: 't-s t-b f-gold', anchor: 'middle' })];
      var GW = [[60, gy], [300, gy]], gws = A.g();
      GW.forEach(function (p, i) { place(dish(A, gws, 'pur', 1), p[0], p[1]); A.text(p[0], gy + 16, '网关 ' + (i + 1), { cls: 't-s t-b f-pur', anchor: 'middle' }, gws); });
      var feed = A.line(0, 0, 0, 0, 's-pur w2 dash'), lk = A.line(0, 0, 0, 0, 's-bad w3');
      var you = A.circle(0, 0, 5.5, 'f-gold'), yt = A.text(0, 0, '你', { cls: 't-s t-b', anchor: 'end' });
      var fl = A.text(200, 18, '', { cls: 't-b f-bad', anchor: 'middle' });
      var sum = A.g();
      A.rect(40, 30, 320, 112, 'f-card s-ink w1', sum, 8);
      ['波束变 → 星内切换 Intra-satellite', '卫星变 → 星间切换 Inter-satellite', '网关变 → 网关切换 Gateway', '系统变 → 系统间切换 Inter-system'].forEach(function (s, j) { A.text(56, 56 + j * 24, s, { cls: 't-b' }, sum); });
      var cur = 0;
      return {
        step: function (k) { cur = k; show(sum, k === 4); show(city, k === 3); show(s2, k === 1); [s1, bt[0], bt[1], feed, lk, you, yt].forEach(function (e) { show(e, k < 4); }); },
        frame: function (ts, dt, k) {
          var p = A.prog(ts, 2.6, 0.4), x1 = 170, x2 = 380, ux = 200, msg = '', sv = 1, beam = 0, g = 0;
          if (k === 0) { ux = A.lerp(110, 230, p); beam = ux < x1 ? 0 : 1; msg = beam ? '星内切换：波束 1 → 波束 2' : ''; }
          else if (k === 1) { x1 = A.lerp(200, 60, p); x2 = x1 + 150; sv = x1 + 80 < ux ? 2 : 1; msg = sv === 2 ? '星间切换：卫星 1 → 卫星 2' : ''; }
          else if (k === 2) { ux = 210; x1 = A.lerp(130, 290, p); g = Math.abs(x1 - GW[0][0]) <= Math.abs(x1 - GW[1][0]) ? 0 : 1; msg = g ? '网关切换：网关 1 → 网关 2' : ''; }
          else if (k === 3) { x1 = 220; ux = A.lerp(190, 360, p); sv = ux > 300 ? 0 : 1; msg = sv ? '' : '系统间切换：卫星 → 4G'; }
          else { x1 = 150; x2 = 300; }
          place(s1, x1, sy); place(s2, x2, sy);
          A.set(bt[0], { x: x1 - 40, y: gy - 40 }); A.set(bt[1], { x: x1 + 40, y: gy - 40 });
          var sx = sv === 2 ? x2 : x1;
          mv(you, [ux, gy - 6]); A.set(yt, { x: ux - 9, y: gy - 4 });
          A.set(lk, sv ? { x1: ux, y1: gy - 10, x2: sx, y2: sy + 6 } : { x1: ux, y1: gy - 10, x2: 370, y2: gy - 52 });
          A.set(feed, { x1: x1, y1: sy + 6, x2: GW[g][0], y2: gy - 12 });
          if (k === 0) { op(s1.childNodes[0], beam ? 0.25 : 0.7); op(s1.childNodes[1], beam ? 0.7 : 0.25); } else { op(s1.childNodes[0], 0.5); op(s1.childNodes[1], 0.5); }
          A.setText(fl, msg);
        }
      };
    }
  });
})();
