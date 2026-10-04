/* EE6129 学习工坊 · 可视化引擎
   所有动画/图表使用 Canvas 绘制，颜色从 CSS 变量读取以适配明暗主题。 */

window.erlangB = function (m, A) {
  var b = 1;
  for (var k = 1; k <= m; k++) b = (A * b) / (k + A * b);
  return b;
};
window.erlangC = function (m, A) {
  var b = window.erlangB(m, A), rho = A / m;
  if (rho >= 1) return 1;
  return b / (1 - rho * (1 - b));
};

window.VIZ = (function () {
  var items = [];
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 基础工具 ---------- */
  function parseColor(c) {
    c = (c || '').trim();
    if (c.charAt(0) === '#') {
      if (c.length === 4) return [parseInt(c[1] + c[1], 16), parseInt(c[2] + c[2], 16), parseInt(c[3] + c[3], 16)];
      return [parseInt(c.substr(1, 2), 16), parseInt(c.substr(3, 2), 16), parseInt(c.substr(5, 2), 16)];
    }
    var m = c.match(/rgba?\(([^)]+)\)/);
    if (m) { var p = m[1].split(','); return [+p[0], +p[1], +p[2]]; }
    return [128, 128, 128];
  }
  function lum(c) { var r = parseColor(c); return (0.299 * r[0] + 0.587 * r[1] + 0.114 * r[2]) / 255; }
  function alpha(c, a) { var r = parseColor(c); return 'rgba(' + r[0] + ',' + r[1] + ',' + r[2] + ',' + a + ')'; }
  function mix(c1, c2, t) {
    var a = parseColor(c1), b = parseColor(c2);
    return 'rgb(' + Math.round(a[0] + (b[0] - a[0]) * t) + ',' + Math.round(a[1] + (b[1] - a[1]) * t) + ',' + Math.round(a[2] + (b[2] - a[2]) * t) + ')';
  }
  function palette(el) {
    var cs = getComputedStyle(el), g = function (n) { return cs.getPropertyValue(n).trim(); };
    var P = {
      accent: g('--accent'), accentSoft: g('--accent-soft'), accentStrong: g('--accent-strong'),
      text: g('--text'), muted: g('--text-muted'), border: g('--border'),
      surface: g('--surface'), surface2: g('--surface-2'), bg: g('--bg'),
      good: g('--good'), bad: g('--bad'), warn: g('--warn')
    };
    P.dark = lum(P.bg) < 0.45;
    return P;
  }
  function F(px, w) { return (w || 400) + ' ' + px + 'px "IBM Plex Sans", system-ui, sans-serif'; }
  function FM(px, w) { return (w || 400) + ' ' + px + 'px "IBM Plex Mono", monospace'; }

  function el(tag, cls, parent, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    if (parent) parent.appendChild(e);
    return e;
  }
  function segs(host, labels, initial, onPick) {
    var row = el('div', 'vizctrl', host);
    var btns = labels.map(function (l, i) {
      var b = el('button', 'vizbtn' + (i === initial ? ' active' : ''), row, l);
      b.addEventListener('click', function () {
        row.querySelectorAll('.vizbtn').forEach(function (x) { x.classList.remove('active'); });
        b.classList.add('active'); onPick(i);
      });
      return b;
    });
    return { row: row, btns: btns };
  }
  function slider(host, label, min, max, val, step, onInput) {
    var wrap = el('div', 'vizslider', host);
    var lab = el('label', null, wrap, label + ' <b>' + val + '</b>');
    var inp = el('input', null, wrap);
    inp.type = 'range'; inp.min = min; inp.max = max; inp.value = val; inp.step = step || 1;
    inp.addEventListener('input', function () {
      lab.querySelector('b').textContent = inp.value;
      onInput(parseFloat(inp.value));
    });
    return inp;
  }
  function caption(host, txt) { return el('div', 'vizcap', host, txt || ''); }

  function mkCanvas(host, ratio) {
    var cv = el('canvas', 'vizcanvas', host);
    var o = { cv: cv, ctx: cv.getContext('2d'), w: 0, h: 0, P: palette(host), ratio: ratio };
    o.resize = function () {
      var w = host.clientWidth || 600;
      var h = Math.max(160, Math.round(w * o.ratio));
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      cv.style.height = h + 'px';
      o.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      o.w = w; o.h = h; o.P = palette(host);
    };
    o.resize();
    return o;
  }
  function clear(c) { c.ctx.clearRect(0, 0, c.w, c.h); }
  function roundRect(ctx, x, y, w, h, r) {
    r = Math.min(r, Math.abs(w) / 2, Math.abs(h) / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y); ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r); ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h); ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r); ctx.quadraticCurveTo(x, y, x + r, y); ctx.closePath();
  }
  function groupColor(idx, n, P) {
    var hue = (idx * 360 / Math.max(n, 1) + 165) % 360;
    return P.dark ? 'hsl(' + hue + ',38%,30%)' : 'hsl(' + hue + ',48%,84%)';
  }
  function log10(x) { return Math.log(x) / Math.LN10; }

  /* ================= A5 · 频率复用六边形网格 ================= */
  function hexReuse(host) {
    var PAIRS = { 3: [1, 1], 4: [2, 0], 7: [1, 2], 9: [3, 0], 12: [2, 2], 13: [1, 3] };
    var N = 7, showI = true;
    var s = segs(host, ['N=3', 'N=4', 'N=7', 'N=9', 'N=12', 'N=13'], 2, function (i) {
      N = [3, 4, 7, 9, 12, 13][i]; cache = null; setCap();
    });
    var t2 = segs(host, ['显示同频干扰源', '隐藏'], 0, function (i) { showI = (i === 0); setCap(); });
    var c = mkCanvas(host, 0.62);
    var cap = caption(host, '');
    var cache = null;

    function setCap() {
      var Q = Math.sqrt(3 * N);
      cap.innerHTML = '簇尺寸 <b>N = ' + N + '</b>（i,j = ' + PAIRS[N][0] + ',' + PAIRS[N][1] +
        '）　同频复用比 <b>Q = √(3N) = ' + Q.toFixed(2) + '</b>　复用距离 <b>D = ' + Q.toFixed(2) + ' R</b>　' +
        '同色小区使用同一组频率。' + (showI ? '红色箭头标出第一层 6 个同频干扰源。' : '');
    }
    function canon(q, r, i, j) {
      var best = null;
      for (var m = -4; m <= 4; m++) for (var n = -4; n <= 4; n++) {
        var qq = q - (m * i + n * (-j)), rr = r - (m * j + n * (i + j));
        var norm = Math.max(Math.abs(qq), Math.abs(rr), Math.abs(qq + rr));
        if (!best || norm < best.n || (norm === best.n && (qq < best.q || (qq === best.q && rr < best.r))))
          best = { q: qq, r: rr, n: norm };
      }
      return best.q + ',' + best.r;
    }
    function build() {
      var ij = PAIRS[N], map = {}, next = 0, cells = [];
      var span = N >= 12 ? 5 : 4;
      for (var r = -span; r <= span; r++) for (var q = -span; q <= span; q++) {
        if (Math.max(Math.abs(q), Math.abs(r), Math.abs(q + r)) > span) continue;
        var key = canon(q, r, ij[0], ij[1]);
        if (!(key in map)) map[key] = next++;
        cells.push({ q: q, r: r, g: map[key] });
      }
      // 第一层同频小区（与中心同组、距离最近的 6 个）
      var homeG = map[canon(0, 0, ij[0], ij[1])];
      var same = cells.filter(function (c) { return c.g === homeG && !(c.q === 0 && c.r === 0); });
      same.forEach(function (c) { c.d = Math.sqrt(3) * Math.hypot(c.q + c.r / 2, c.r * Math.sqrt(3) / 2); });
      same.sort(function (a, b) { return a.d - b.d; });
      return { cells: cells, home: homeG, tier1: same.slice(0, 6), groups: next };
    }
    function pos(q, r, s) { return [Math.sqrt(3) * s * (q + r / 2), 1.5 * s * r]; }
    function hexPath(ctx, x, y, s) {
      ctx.beginPath();
      for (var i = 0; i < 6; i++) {
        var a = Math.PI / 180 * (60 * i - 90);
        var px = x + s * Math.cos(a), py = y + s * Math.sin(a);
        i ? ctx.lineTo(px, py) : ctx.moveTo(px, py);
      }
      ctx.closePath();
    }
    setCap();
    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        if (!cache || cache.N !== N) { cache = build(); cache.N = N; }
        clear(c); var ctx = c.ctx, P = c.P;
        var span = N >= 12 ? 5 : 4;
        var sz = Math.min(c.w / (Math.sqrt(3) * (2 * span + 1.6)), c.h / (1.5 * (2 * span + 1.4)));
        var cx = c.w / 2, cy = c.h / 2;
        var pulse = 0.5 + 0.5 * Math.sin(t / 620);

        cache.cells.forEach(function (cell) {
          var p = pos(cell.q, cell.r, sz), x = cx + p[0], y = cy + p[1];
          hexPath(ctx, x, y, sz * 0.97);
          var isHome = cell.g === cache.home;
          ctx.fillStyle = isHome ? alpha(P.accent, 0.20 + 0.22 * pulse) : groupColor(cell.g, cache.groups, P);
          ctx.fill();
          ctx.strokeStyle = isHome ? P.accent : alpha(P.border, 0.9);
          ctx.lineWidth = isHome ? 1.8 : 1; ctx.stroke();
          if (sz > 17) {
            ctx.fillStyle = isHome ? P.accentStrong : P.muted;
            ctx.font = FM(Math.max(9, sz * 0.34), isHome ? 600 : 400);
            ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            ctx.fillText('f' + (cell.g + 1), x, y);
          }
        });
        // 中心小区
        var p0 = pos(0, 0, sz);
        hexPath(ctx, cx + p0[0], cy + p0[1], sz * 0.97);
        ctx.fillStyle = alpha(P.accent, 0.55); ctx.fill();
        ctx.strokeStyle = P.accentStrong; ctx.lineWidth = 2.4; ctx.stroke();
        ctx.fillStyle = P.dark ? '#08100e' : '#ffffff';
        ctx.font = FM(Math.max(10, sz * 0.36), 600); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText('f1', cx, cy);

        if (showI && cache.tier1.length) {
          cache.tier1.forEach(function (cell, k) {
            var p = pos(cell.q, cell.r, sz), x = cx + p[0], y = cy + p[1];
            var dx = x - cx, dy = y - cy, L = Math.hypot(dx, dy);
            var ux = dx / L, uy = dy / L;
            ctx.strokeStyle = alpha(P.bad, 0.55 + 0.35 * pulse); ctx.lineWidth = 1.6;
            ctx.setLineDash([5, 4]); ctx.beginPath();
            ctx.moveTo(x - ux * sz * 0.8, y - uy * sz * 0.8);
            ctx.lineTo(cx + ux * sz * 0.85, cy + uy * sz * 0.85);
            ctx.stroke(); ctx.setLineDash([]);
            // 箭头
            var ax = cx + ux * sz * 0.9, ay = cy + uy * sz * 0.9;
            ctx.fillStyle = alpha(P.bad, 0.8); ctx.beginPath();
            ctx.moveTo(ax, ay);
            ctx.lineTo(ax + ux * 9 - uy * 4.5, ay + uy * 9 + ux * 4.5);
            ctx.lineTo(ax + ux * 9 + uy * 4.5, ay + uy * 9 - ux * 4.5);
            ctx.closePath(); ctx.fill();
            if (k === 0) {
              // 标注 D
              ctx.strokeStyle = P.accentStrong; ctx.lineWidth = 2.2;
              ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(x, y); ctx.stroke();
              ctx.fillStyle = P.accentStrong; ctx.font = FM(12, 600);
              ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
              ctx.fillText('D = ' + Math.sqrt(3 * N).toFixed(2) + 'R', (cx + x) / 2, (cy + y) / 2 - 5);
            }
          });
        }
      }
    };
  }

  /* ================= A2 · 多址接入方式对比动画 ================= */
  function accessAnim(host) {
    var mode = 0; // 0 FDMA 1 TDMA 2 CDMA 3 OFDMA
    var names = ['FDMA', 'TDMA', 'CDMA', 'OFDMA'];
    var s = segs(host, names, 0, function (i) { mode = i; setCap(); });
    var c = mkCanvas(host, 0.5);
    var cap = caption(host, '');
    var USERS = 4;
    var ofdmaMap = [];
    for (var i = 0; i < 8; i++) { ofdmaMap[i] = []; for (var j = 0; j < 12; j++) ofdmaMap[i][j] = (i * 3 + j * 5 + (i * j) % 3) % USERS; }
    var texts = [
      'FDMA：每个用户独占一条<b>频率</b>子带，全时间可用。频带之间需要保护频带，用户数受限于带宽/信道间隔。',
      'TDMA：所有用户共用<b>整个频带</b>，按周期轮流占用<b>时隙</b>。上行为突发发送，需要保护时间与同步序列。',
      'CDMA：所有用户<b>同时同频</b>发送，靠近似正交的扩频码区分；接收端用相同 PN 码相关解扩，其它码字结果近似为零。',
      'OFDMA：资源被切成<b>时频二维</b>小块（LTE 的资源块），调度器按信道质量把不同小块分给不同用户。'
    ];
    function setCap() { cap.innerHTML = texts[mode]; }
    setCap();
    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        clear(c); var ctx = c.ctx, P = c.P;
        var L = 52, R = 14, T = 16, B = 34;
        var gw = c.w - L - R, gh = c.h - T - B;
        ctx.strokeStyle = P.border; ctx.lineWidth = 1;
        ctx.strokeRect(L, T, gw, gh);
        ctx.fillStyle = P.muted; ctx.font = F(11);
        ctx.save(); ctx.translate(14, T + gh / 2); ctx.rotate(-Math.PI / 2);
        ctx.textAlign = 'center'; ctx.fillText('频率 →', 0, 0); ctx.restore();
        ctx.textAlign = 'center'; ctx.fillText('时间 →', L + gw / 2, c.h - 10);

        var ucol = function (u) { return P.dark ? 'hsl(' + (160 + u * 52) + ',45%,42%)' : 'hsl(' + (160 + u * 52) + ',55%,62%)'; };
        var cursor = (t / 2600) % 1;

        if (mode === 0) {
          for (var u = 0; u < USERS; u++) {
            var y = T + gh * u / USERS + 3, hh = gh / USERS - 6;
            ctx.fillStyle = ucol(u); ctx.globalAlpha = 0.85;
            roundRect(ctx, L + 2, y, gw - 4, hh, 4); ctx.fill(); ctx.globalAlpha = 1;
            ctx.fillStyle = '#fff'; ctx.font = F(12, 600); ctx.textAlign = 'left';
            ctx.textBaseline = 'middle'; ctx.fillText('用户 ' + (u + 1), L + 12, y + hh / 2);
          }
        } else if (mode === 1) {
          var SLOTS = 12;
          for (var k = 0; k < SLOTS; k++) {
            var u2 = k % USERS, x = L + gw * k / SLOTS + 2, w2 = gw / SLOTS - 4;
            var active = Math.floor(cursor * SLOTS) === k;
            ctx.fillStyle = ucol(u2); ctx.globalAlpha = active ? 1 : 0.45;
            roundRect(ctx, x, T + 4, w2, gh - 8, 3); ctx.fill(); ctx.globalAlpha = 1;
            if (active) { ctx.strokeStyle = P.text; ctx.lineWidth = 2; ctx.stroke(); }
            ctx.fillStyle = '#fff'; ctx.font = FM(10, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            ctx.fillText('U' + (u2 + 1), x + w2 / 2, T + gh / 2);
          }
        } else if (mode === 2) {
          for (var u3 = 0; u3 < USERS; u3++) {
            ctx.save();
            ctx.beginPath(); ctx.rect(L + 2, T + 2, gw - 4, gh - 4); ctx.clip();
            ctx.strokeStyle = ucol(u3); ctx.globalAlpha = 0.55; ctx.lineWidth = 3;
            var off = (t / 40 + u3 * 30) % 40;
            for (var x2 = -gh; x2 < gw + gh; x2 += 40) {
              ctx.beginPath();
              ctx.moveTo(L + x2 + off + (u3 % 2 ? gh : 0), T);
              ctx.lineTo(L + x2 + off + (u3 % 2 ? 0 : gh), T + gh);
              ctx.stroke();
            }
            ctx.restore(); ctx.globalAlpha = 1;
          }
          ctx.fillStyle = P.text; ctx.font = F(13, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText('4 个用户全部占满整个时频平面 · 靠 Walsh / PN 码区分', L + gw / 2, T + gh / 2);
        } else {
          var cols = 12, rows = 8;
          for (var r2 = 0; r2 < rows; r2++) for (var k2 = 0; k2 < cols; k2++) {
            var u4 = ofdmaMap[r2][k2];
            var x3 = L + gw * k2 / cols + 1.5, y3 = T + gh * r2 / rows + 1.5;
            var act = Math.floor(cursor * cols) === k2;
            ctx.fillStyle = ucol(u4); ctx.globalAlpha = act ? 0.98 : 0.55;
            roundRect(ctx, x3, y3, gw / cols - 3, gh / rows - 3, 2); ctx.fill();
            ctx.globalAlpha = 1;
          }
        }
        // 时间游标
        if (mode !== 2) {
          var xc = L + gw * cursor;
          ctx.strokeStyle = alpha(P.text, 0.55); ctx.lineWidth = 1.5;
          ctx.setLineDash([4, 3]); ctx.beginPath();
          ctx.moveTo(xc, T - 4); ctx.lineTo(xc, T + gh + 4); ctx.stroke(); ctx.setLineDash([]);
        }
      }
    };
  }

  /* ================= A8 · 切换过程动画 ================= */
  function handoverAnim(host) {
    var delta = 6, speed = 1;
    slider(host, '切换门限余量 Δ = P_HO − P_min（dB）', 1, 16, 6, 1, function (v) { delta = v; });
    slider(host, '移动速度（相对）', 1, 4, 1, 1, function (v) { speed = v; });
    var c = mkCanvas(host, 0.72);
    var cap = caption(host, '');
    var st = { x: 0.06, dir: 1, serving: 0, ho: 0, drops: 0, hoT: -1, flash: 0, last: 0 };
    var P0 = -35, n = 3.5, Pmin = -95;

    function pw(bsx, x) { var d = Math.max(0.03, Math.abs(x - bsx) * 3); return P0 - 10 * n * log10(d / 0.03) / 1; }
    function power(bs, x) {
      var bx = bs === 0 ? 0.06 : 0.94;
      var d = Math.max(0.02, Math.abs(x - bx)) * 6; // km
      return -32 - 10 * n * log10(Math.max(d, 0.02) / 0.02) - 22;
    }
    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        var dt = st.last ? Math.min(60, t - st.last) : 16; st.last = t;
        clear(c); var ctx = c.ctx, P = c.P;
        var PHO = Pmin + delta;
        // 更新位置
        st.x += st.dir * dt * 0.000045 * speed;
        if (st.x > 0.97) { st.x = 0.97; st.dir = -1; }
        if (st.x < 0.03) { st.x = 0.03; st.dir = 1; }
        var Pa = power(0, st.x), Pb = power(1, st.x);
        var Pserv = st.serving === 0 ? Pa : Pb, Pother = st.serving === 0 ? Pb : Pa;
        if (st.hoT < 0 && Pserv < PHO && Pother > Pserv) { st.hoT = t; }
        if (st.hoT > 0) {
          if (t - st.hoT > 900 / speed) {              // 切换执行需要时间
            if (Pserv < Pmin) { st.drops++; st.flash = t; }
            else { st.ho++; }
            st.serving = 1 - st.serving; st.hoT = -1;
          }
        }
        var topH = c.h * 0.36, chartY = topH + 8, chartH = c.h - topH - 42;
        // ---- 上半：地理场景 ----
        ctx.fillStyle = alpha(P.border, 0.35);
        ctx.fillRect(0, topH - 24, c.w, 22);
        [0, 1].forEach(function (b) {
          var bx = (b === 0 ? 0.06 : 0.94) * c.w;
          var on = st.serving === b;
          ctx.strokeStyle = on ? P.accent : P.muted; ctx.lineWidth = on ? 2.5 : 1.5;
          ctx.beginPath(); ctx.moveTo(bx, topH - 24); ctx.lineTo(bx, topH - 86); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(bx - 12, topH - 24); ctx.lineTo(bx, topH - 86); ctx.lineTo(bx + 12, topH - 24); ctx.stroke();
          for (var k = 1; k <= 3; k++) {
            ctx.globalAlpha = on ? (0.55 - k * 0.12) * (0.6 + 0.4 * Math.sin(t / 300 - k)) + 0.2 : 0.12;
            ctx.strokeStyle = on ? P.accent : P.muted; ctx.lineWidth = 1.6;
            ctx.beginPath(); ctx.arc(bx, topH - 86, 12 + k * 11, -Math.PI * 0.85, -Math.PI * 0.15); ctx.stroke();
          }
          ctx.globalAlpha = 1;
          ctx.fillStyle = on ? P.accentStrong : P.muted; ctx.font = F(12, 600);
          ctx.textAlign = 'center'; ctx.fillText('BS' + (b + 1), bx, topH - 96);
        });
        // 移动台
        var mx = st.x * c.w;
        ctx.fillStyle = st.hoT > 0 ? P.warn || P.accent : P.accentStrong;
        roundRect(ctx, mx - 13, topH - 44, 26, 18, 4); ctx.fill();
        ctx.fillStyle = P.dark ? '#08100e' : '#fff'; ctx.font = FM(9, 600);
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('MS', mx, topH - 35);
        ctx.strokeStyle = alpha(st.serving === 0 ? P.accent : P.accent, 0.75);
        ctx.setLineDash([4, 4]); ctx.lineWidth = 1.5; ctx.beginPath();
        ctx.moveTo(mx, topH - 44); ctx.lineTo((st.serving === 0 ? 0.06 : 0.94) * c.w, topH - 86);
        ctx.stroke(); ctx.setLineDash([]);

        // ---- 下半：接收功率曲线 ----
        var yTop = -30, yBot = -110;
        function py(v) { return chartY + chartH * (1 - (v - yBot) / (yTop - yBot)); }
        ctx.strokeStyle = alpha(P.border, 0.8); ctx.lineWidth = 1;
        ctx.strokeRect(34, chartY, c.w - 46, chartH);
        [Pmin, PHO].forEach(function (v, k) {
          ctx.strokeStyle = k ? P.warn || P.accent : P.bad;
          ctx.setLineDash([6, 4]); ctx.lineWidth = 1.4;
          ctx.beginPath(); ctx.moveTo(34, py(v)); ctx.lineTo(c.w - 12, py(v)); ctx.stroke(); ctx.setLineDash([]);
          ctx.fillStyle = k ? P.warn || P.accent : P.bad; ctx.font = FM(10, 600);
          ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
          ctx.fillText(k ? 'P_HO = ' + PHO + ' dBm' : 'P_min = ' + Pmin + ' dBm', 40, py(v) - 3);
        });
        [0, 1].forEach(function (b) {
          ctx.strokeStyle = st.serving === b ? P.accent : alpha(P.muted, 0.75);
          ctx.lineWidth = st.serving === b ? 2.4 : 1.5;
          ctx.beginPath();
          for (var i = 0; i <= 120; i++) {
            var xx = 0.02 + 0.96 * i / 120;
            var v = power(b, xx);
            var X = 34 + (c.w - 46) * xx, Y = py(Math.max(yBot, v));
            i ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y);
          }
          ctx.stroke();
          var cur = power(b, st.x);
          ctx.fillStyle = st.serving === b ? P.accent : P.muted;
          ctx.beginPath(); ctx.arc(34 + (c.w - 46) * st.x, py(Math.max(yBot, cur)), 4.5, 0, 7); ctx.fill();
        });
        ctx.fillStyle = P.muted; ctx.font = FM(10); ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
        ctx.fillText('dBm', 30, chartY + 8);

        // 状态栏
        var msg = st.hoT > 0 ? '⚡ 切换执行中…（识别新基站、分配新信道）' :
          '服务小区：BS' + (st.serving + 1) + '　接收电平 ' + Pserv.toFixed(1) + ' dBm';
        if (t - st.flash < 1200) msg = '❌ 掉话！信号已跌破 P_min，切换来不及完成 — Δ 太小';
        ctx.fillStyle = (t - st.flash < 1200) ? P.bad : P.text;
        ctx.font = F(12, 600); ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
        ctx.fillText(msg, 4, c.h - 4);
        ctx.fillStyle = P.muted; ctx.font = FM(11); ctx.textAlign = 'right';
        ctx.fillText('成功切换 ' + st.ho + ' 次 · 掉话 ' + st.drops + ' 次', c.w - 4, c.h - 4);
        cap.innerHTML = 'Δ 越大 → 越早触发切换，切换成功率高但<b>切换次数多</b>（可能乒乓切换）；Δ 越小 → 越晚触发，' +
          '信号可能在切换完成前跌破 P_min 而<b>掉话</b>。拖动滑块到 Δ=1~2 并提高速度，观察掉话如何发生。';
      }
    };
  }

  /* ================= A4 · 路径损耗 / 接收功率曲线 ================= */
  function pathLossChart(host) {
    var c = mkCanvas(host, 0.52);
    var cap = caption(host, '三种典型环境下接收功率随距离的变化（标准条件：P_T=10W, f=900MHz, h_T=30m, h_R=3m）。' +
      '直线斜率就是<b>每十倍距离的衰减 dB 数</b>：自由空间 −20dB/decade，平面地球两径模型 −40dB/decade，CCIR 城区 −35.4dB/decade。');
    var MODELS = [
      { name: '自由空间 Free Space', P0: -41, g: -20 },
      { name: '平面地球 Flat Earth', P0: -30.64, g: -40 },
      { name: 'CCIR 城区 (h_T=30m)', P0: -71.04, g: -35.4 }
    ];
    return {
      animated: false, redrawOn: ['pl_d'],
      resize: function () { c.resize(); },
      draw: function () {
        clear(c); var ctx = c.ctx, P = c.P;
        var L = 46, R = 12, T = 12, B = 34, gw = c.w - L - R, gh = c.h - T - B;
        var x0 = -1, x1 = 1.5;   // log10(d/km): 0.1km ~ 31.6km
        var y0 = -140, y1 = -20;
        function X(lx) { return L + gw * (lx - x0) / (x1 - x0); }
        function Y(v) { return T + gh * (1 - (v - y0) / (y1 - y0)); }
        ctx.strokeStyle = alpha(P.border, 0.75); ctx.lineWidth = 1;
        for (var d = -1; d <= 1.5; d += 0.5) {
          ctx.beginPath(); ctx.moveTo(X(d), T); ctx.lineTo(X(d), T + gh); ctx.stroke();
          ctx.fillStyle = P.muted; ctx.font = FM(10); ctx.textAlign = 'center'; ctx.textBaseline = 'top';
          ctx.fillText(Math.pow(10, d) < 1 ? Math.pow(10, d).toFixed(1) : Math.pow(10, d).toFixed(0), X(d), T + gh + 5);
        }
        for (var v = -140; v <= -20; v += 20) {
          ctx.strokeStyle = alpha(P.border, 0.55);
          ctx.beginPath(); ctx.moveTo(L, Y(v)); ctx.lineTo(L + gw, Y(v)); ctx.stroke();
          ctx.fillStyle = P.muted; ctx.font = FM(10); ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
          ctx.fillText(v, L - 6, Y(v));
        }
        ctx.fillStyle = P.muted; ctx.font = F(11); ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
        ctx.fillText('距离 d（km，对数轴）', L + gw / 2, c.h - 2);
        ctx.save(); ctx.translate(12, T + gh / 2); ctx.rotate(-Math.PI / 2);
        ctx.fillText('接收功率 P_R（dBm）', 0, 0); ctx.restore();

        var cols = [P.accent, P.good, P.bad];
        MODELS.forEach(function (m, i) {
          ctx.strokeStyle = cols[i]; ctx.lineWidth = 2.2;
          ctx.beginPath();
          ctx.moveTo(X(x0), Y(m.P0 + m.g * x0));
          ctx.lineTo(X(x1), Y(m.P0 + m.g * x1));
          ctx.stroke();
          ctx.fillStyle = cols[i]; ctx.font = F(11, 600);
          ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
          var ly = Y(Math.max(y0 + 6, m.P0 + m.g * (x1 - 0.42)));
          ctx.fillText(m.name, X(x1 - 0.42) + 4, ly - 10);
        });
        var inp = document.getElementById('pl_d');
        var dv = inp ? parseFloat(inp.value) : 5;
        if (dv > 0) {
          var lx = Math.max(x0, Math.min(x1, log10(dv)));
          ctx.strokeStyle = alpha(P.text, 0.5); ctx.setLineDash([4, 3]); ctx.lineWidth = 1.4;
          ctx.beginPath(); ctx.moveTo(X(lx), T); ctx.lineTo(X(lx), T + gh); ctx.stroke(); ctx.setLineDash([]);
          MODELS.forEach(function (m, i) {
            ctx.fillStyle = cols[i];
            ctx.beginPath(); ctx.arc(X(lx), Y(m.P0 + m.g * lx), 4, 0, 7); ctx.fill();
          });
          ctx.fillStyle = P.text; ctx.font = FM(11, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'top';
          ctx.fillText('d = ' + dv + ' km', X(lx), T + 2);
        }
      }
    };
  }

  /* ================= A5 · SIR vs 簇尺寸曲线 ================= */
  function sirChart(host) {
    var c = mkCanvas(host, 0.5);
    var cap = caption(host, '同频干扰简化式 S/I = (3N)^(n/2)/6。虚线为语音业务常用的 18dB 门槛：' +
      'n 越大（城区遮挡越强）衰减越快，同频干扰反而越小，可选用更小的簇尺寸 N 换取容量。');
    var NS = [1, 3, 4, 7, 9, 12, 13, 16, 19, 21];
    return {
      animated: false, redrawOn: ['g_n', 'g_pn'],
      resize: function () { c.resize(); },
      draw: function () {
        clear(c); var ctx = c.ctx, P = c.P;
        var L = 42, R = 46, T = 14, B = 32, gw = c.w - L - R, gh = c.h - T - B;
        var y0 = 0, y1 = 32;
        function X(i) { return L + gw * i / (NS.length - 1); }
        function Y(v) { return T + gh * (1 - (Math.max(y0, Math.min(y1, v)) - y0) / (y1 - y0)); }
        for (var v = 0; v <= 30; v += 6) {
          ctx.strokeStyle = alpha(P.border, 0.6); ctx.beginPath();
          ctx.moveTo(L, Y(v)); ctx.lineTo(L + gw, Y(v)); ctx.stroke();
          ctx.fillStyle = P.muted; ctx.font = FM(10); ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
          ctx.fillText(v + 'dB', L - 5, Y(v));
        }
        NS.forEach(function (n, i) {
          ctx.fillStyle = P.muted; ctx.font = FM(10); ctx.textAlign = 'center'; ctx.textBaseline = 'top';
          ctx.fillText('N=' + n, X(i), T + gh + 5);
        });
        ctx.strokeStyle = P.bad; ctx.setLineDash([6, 4]); ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.moveTo(L, Y(18)); ctx.lineTo(L + gw, Y(18)); ctx.stroke(); ctx.setLineDash([]);
        ctx.fillStyle = P.bad; ctx.font = FM(10, 600); ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
        ctx.fillText('18dB 语音门槛', L + 4, Y(18) - 3);

        var sel = document.getElementById('g_n'), selN = sel ? parseFloat(sel.value) : 7;
        var selPn = document.getElementById('g_pn'), curN = selPn ? parseFloat(selPn.value) : 4;
        [2, 3, 4, 5].forEach(function (n, k) {
          var isCur = Math.abs(n - curN) < 0.25;
          ctx.strokeStyle = isCur ? P.accent : alpha(P.muted, 0.55);
          ctx.lineWidth = isCur ? 2.6 : 1.4;
          ctx.beginPath();
          NS.forEach(function (N, i) {
            var sir = 10 * log10(Math.pow(3 * N, n / 2) / 6);
            i ? ctx.lineTo(X(i), Y(sir)) : ctx.moveTo(X(i), Y(sir));
          });
          ctx.stroke();
          var last = 10 * log10(Math.pow(3 * NS[NS.length - 1], n / 2) / 6);
          ctx.fillStyle = isCur ? P.accentStrong : P.muted; ctx.font = FM(10, 600);
          ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
          ctx.fillText('n=' + n, L + gw + 5, Y(last));
        });
        var idx = NS.indexOf(selN);
        if (idx >= 0) {
          var sirSel = 10 * log10(Math.pow(3 * selN, curN / 2) / 6);
          ctx.fillStyle = P.accentStrong;
          ctx.beginPath(); ctx.arc(X(idx), Y(sirSel), 5.5, 0, 7); ctx.fill();
          ctx.fillStyle = P.text; ctx.font = FM(11, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
          ctx.fillText(sirSel.toFixed(1) + 'dB', X(idx), Y(sirSel) - 8);
        }
      }
    };
  }

  /* ================= A7 · Erlang B 曲线 ================= */
  function erlangChart(host) {
    var c = mkCanvas(host, 0.52);
    var cap = caption(host, '每条曲线对应一个信道数 M：横轴为提供话务量 A，纵轴为阻塞概率（对数刻度）。' +
      '同样 2% 的 GoS 下，M 越大，<b>每信道能承载的话务越多</b>——这就是干线增益。');
    var MS = [5, 10, 20, 50, 100];
    return {
      animated: false, redrawOn: ['tr_m', 'tr_a'],
      resize: function () { c.resize(); },
      draw: function () {
        clear(c); var ctx = c.ctx, P = c.P;
        var L = 46, R = 40, T = 12, B = 34, gw = c.w - L - R, gh = c.h - T - B;
        var A1 = 120;
        function X(a) { return L + gw * Math.min(a, A1) / A1; }
        function Y(p) { var lp = Math.max(-3, log10(Math.max(p, 1e-3))); return T + gh * (1 - (lp + 3) / 3); }
        [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1].forEach(function (p) {
          var major = (p === 0.01 || p === 0.02);
          ctx.strokeStyle = major ? alpha(P.bad, 0.6) : alpha(P.border, 0.5);
          ctx.setLineDash(major ? [5, 4] : []);
          ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(L, Y(p)); ctx.lineTo(L + gw, Y(p)); ctx.stroke();
          ctx.setLineDash([]);
          if ([0.001, 0.01, 0.02, 0.1, 1].indexOf(p) >= 0) {
            ctx.fillStyle = major ? P.bad : P.muted; ctx.font = FM(10, major ? 600 : 400);
            ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
            ctx.fillText((p * 100).toFixed(p < 0.01 ? 1 : 0) + '%', L - 5, Y(p));
          }
        });
        for (var a = 0; a <= A1; a += 20) {
          ctx.fillStyle = P.muted; ctx.font = FM(10); ctx.textAlign = 'center'; ctx.textBaseline = 'top';
          ctx.fillText(a, X(a), T + gh + 5);
        }
        ctx.fillStyle = P.muted; ctx.font = F(11); ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
        ctx.fillText('提供话务量 A（Erlang）', L + gw / 2, c.h - 2);

        var mi = document.getElementById('tr_m'), curM = mi ? Math.round(parseFloat(mi.value)) : 20;
        var ai = document.getElementById('tr_a'), curA = ai ? parseFloat(ai.value) : 13;
        MS.forEach(function (M) {
          ctx.strokeStyle = alpha(P.muted, 0.6); ctx.lineWidth = 1.5;
          ctx.beginPath();
          for (var a2 = 0.2; a2 <= A1; a2 += 0.6) {
            var p = window.erlangB(M, a2);
            if (p < 1e-3) continue;
            ctx.lineTo(X(a2), Y(p));
          }
          ctx.stroke();
          ctx.fillStyle = P.muted; ctx.font = FM(10, 600);
          ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
          ctx.fillText('M=' + M, X(M) + 3, Y(0.55));
        });
        // 当前 M 曲线高亮
        if (curM >= 1) {
          ctx.strokeStyle = P.accent; ctx.lineWidth = 2.8; ctx.beginPath();
          for (var a3 = 0.2; a3 <= A1; a3 += 0.5) {
            var p3 = window.erlangB(curM, a3);
            if (p3 < 1e-3) continue;
            ctx.lineTo(X(a3), Y(p3));
          }
          ctx.stroke();
          var pc = window.erlangB(curM, curA);
          ctx.fillStyle = P.accentStrong;
          ctx.beginPath(); ctx.arc(X(curA), Y(pc), 5.5, 0, 7); ctx.fill();
          ctx.fillStyle = P.text; ctx.font = FM(11, 600); ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
          ctx.fillText('M=' + curM + ', A=' + curA + ' → ' + (pc * 100).toFixed(2) + '%', X(curA) + 8, Y(pc) - 6);
        }
      }
    };
  }

  /* ================= A6 · 扇区化与干扰源可视化 =================
     N = 7（i = 2, j = 1）时，6 个同频小区相对服务小区的方位角是 19.1° + 60°·k。
     下行视角：每个小区编号相同的扇区（用同一组信道）天线都朝东（0°），
     你在服务小区的这个扇区里。某个同频小区的这个扇区天线正对着你，才构成干扰。 */
  function sectorViz(host) {
    var mode = 0; // 0 全向 1 三扇区 2 六扇区
    segs(host, ['全向天线', '3 扇区 120°', '6 扇区 60°'], 0, function (i) { mode = i; });
    var c = mkCanvas(host, 0.7);
    var cap = caption(host, '');
    var DEG = Math.PI / 180;
    var OFF = Math.atan2(Math.sqrt(3) / 2, 2.5) / DEG;   // i=2, j=1 的偏角 ≈ 19.1°

    function hexPath(ctx, x, y, s) {
      ctx.beginPath();
      for (var i = 0; i < 6; i++) {
        var a = (30 + 60 * i) * DEG;
        var px = x + s * Math.cos(a), py = y - s * Math.sin(a);
        i ? ctx.lineTo(px, py) : ctx.moveTo(px, py);
      }
      ctx.closePath();
    }
    // 按数学角度（逆时针为正、y 轴向上）画扇形
    function wedge(ctx, x, y, r, a0, a1) {
      ctx.beginPath(); ctx.moveTo(x, y);
      ctx.arc(x, y, r, -a1 * DEG, -a0 * DEG);
      ctx.closePath();
    }
    function norm(d) { d = ((d % 360) + 360) % 360; return d > 180 ? d - 360 : d; }
    function arrowHead(ctx, x, y, ang, col) {
      ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(x, y);
      ctx.lineTo(x - 10 * Math.cos(ang - 0.42), y - 10 * Math.sin(ang - 0.42));
      ctx.lineTo(x - 10 * Math.cos(ang + 0.42), y - 10 * Math.sin(ang + 0.42));
      ctx.closePath(); ctx.fill();
    }

    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        clear(c); var ctx = c.ctx, P = c.P;
        var half = mode === 0 ? 180 : (mode === 1 ? 60 : 30);   // 扇区半角
        var nSec = mode === 0 ? 1 : (mode === 1 ? 3 : 6);
        var foot = 28;
        var cx = c.w / 2, cy = (c.h - foot) / 2 + 2;
        var Dp = Math.min(((c.h - foot) / 2 - 18) / 1.24, (c.w / 2 - 10) / 1.4);
        var rc = Dp * 0.24;
        var pulse = 0.5 + 0.5 * Math.sin(t / 450);
        var Q = Math.sqrt(21), n = 4;

        // 6 个同频小区；天线朝东的扇区能照到服务小区 ⇔ 服务小区方向落在 ±half 以内
        var cells = [], hits = [];
        for (var k = 0; k < 6; k++) {
          var a = OFF + 60 * k;
          var hit = mode === 0 || Math.abs(norm(a + 180)) < half;
          cells.push({ name: 'I' + (k + 1), a: a, hit: hit,
            x: cx + Dp * Math.cos(a * DEG), y: cy - Dp * Math.sin(a * DEG) });
          if (hit) hits.push('I' + (k + 1));
        }

        // 干扰路径：从干扰小区流向服务小区的虚线
        cells.forEach(function (cl) {
          if (!cl.hit) return;
          var dx = cx - cl.x, dy = cy - cl.y, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L;
          var x0 = cl.x + ux * rc, y0 = cl.y + uy * rc, x1 = cx - ux * rc * 1.1, y1 = cy - uy * rc * 1.1;
          ctx.strokeStyle = alpha(P.bad, 0.55 + 0.35 * pulse); ctx.lineWidth = 2;
          ctx.setLineDash([7, 6]); ctx.lineDashOffset = -t / 35;
          ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke();
          ctx.setLineDash([]); ctx.lineDashOffset = 0;
          arrowHead(ctx, x1, y1, Math.atan2(uy, ux), alpha(P.bad, 0.9));
        });

        function drawCell(x, y, serve, hit) {
          var col = serve ? P.accent : (hit ? P.bad : P.muted);
          hexPath(ctx, x, y, rc);
          ctx.fillStyle = alpha(col, serve ? 0.12 : 0.06); ctx.fill();
          // 与你同频的那个扇区（全向时是整个小区）
          ctx.save(); hexPath(ctx, x, y, rc); ctx.clip();
          if (mode === 0) hexPath(ctx, x, y, rc); else wedge(ctx, x, y, rc * 1.3, -half, half);
          ctx.fillStyle = serve ? alpha(P.accent, 0.45) : alpha(col, hit ? 0.32 + 0.25 * pulse : 0.2);
          ctx.fill();
          if (mode > 0) {
            ctx.strokeStyle = alpha(P.text, 0.35); ctx.lineWidth = 1; ctx.setLineDash([3, 3]);
            for (var s = 0; s < nSec; s++) {
              var b = (half + s * 2 * half) * DEG;
              ctx.beginPath(); ctx.moveTo(x, y);
              ctx.lineTo(x + rc * 1.3 * Math.cos(b), y - rc * 1.3 * Math.sin(b)); ctx.stroke();
            }
            ctx.setLineDash([]);
          }
          ctx.restore();
          hexPath(ctx, x, y, rc);
          ctx.strokeStyle = col; ctx.lineWidth = (serve || hit) ? 2 : 1.2; ctx.stroke();
          ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, 3, 0, 7); ctx.fill();
        }

        // 同频小区
        cells.forEach(function (cl) {
          drawCell(cl.x, cl.y, false, cl.hit);
          if (mode > 0 && !cl.hit) {   // 天线朝东，背对服务小区
            var ax0 = cl.x + rc * 0.95, ax1 = cl.x + rc * 1.75;
            ctx.strokeStyle = alpha(P.muted, 0.8); ctx.lineWidth = 1.6;
            ctx.beginPath(); ctx.moveTo(ax0, cl.y); ctx.lineTo(ax1, cl.y); ctx.stroke();
            arrowHead(ctx, ax1, cl.y, 0, alpha(P.muted, 0.8));
          }
          ctx.textAlign = 'center';
          ctx.fillStyle = cl.hit ? P.bad : P.muted; ctx.font = FM(12, 700); ctx.textBaseline = 'bottom';
          ctx.fillText(cl.name, cl.x, cl.y - rc - 3);
          ctx.font = F(10, 600); ctx.textBaseline = 'top';
          ctx.fillText(mode === 0 ? '全向，照到你' : (cl.hit ? '天线朝向你' : '天线背对你'), cl.x, cl.y + rc + 3);
        });

        // 服务小区与手机
        drawCell(cx, cy, true, false);
        var mx = cx + rc * 0.55, my = cy - rc * 0.08;
        ctx.fillStyle = P.text; roundRect(ctx, mx - 4, my - 7, 8, 14, 2); ctx.fill();
        ctx.fillStyle = P.accentStrong; ctx.font = F(10, 700); ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
        ctx.fillText('你', mx, my - 9);
        ctx.textBaseline = 'top'; ctx.fillText('服务小区', cx, cy + rc + 3);

        // 底部结论
        var sir = mode === 1 ? 1 / (Math.pow(Q, -n) + Math.pow(Q + 0.7, -n)) : Math.pow(Q + 0.7, n);
        var line = mode === 0
          ? '干扰来自全部 6 个　S/I ≈ ' + (10 * log10(Math.pow(Q, n) / 6)).toFixed(1) + ' dB（简化）／' + (10 * log10(Math.pow(Q - 1, n) / 6)).toFixed(1) + ' dB（最坏）'
          : '干扰来自 ' + hits.join('、') + '，共 ' + hits.length + ' 个　最坏情况 S/I ≈ ' + (10 * log10(sir)).toFixed(1) + ' dB';
        line += '（N=7, n=4）';
        ctx.fillStyle = P.text; ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
        ctx.font = F(12, 600);
        if (ctx.measureText(line).width <= c.w - 10) {
          ctx.fillText(line, 5, c.h - 6);
        } else {                       // 窄屏：在全角空格处拆成两行
          var parts = line.split('　');
          ctx.font = F(10, 600);
          ctx.fillText(parts[0], 5, c.h - 16);
          ctx.fillText(parts.slice(1).join(' '), 5, c.h - 3);
        }

        cap.innerHTML = mode === 0
          ? '全向天线向四面八方发射，第一层 <b>6 个</b>同频小区的信号都能到达你。'
          : (mode === 1
            ? '每个小区分成 3 个扇区，<b>只有编号相同的扇区（图中都朝东、涂色的那一块）用同一组信道</b>，其它扇区用别的信道，不算同频。' +
              '这 6 个同频扇区的天线都朝东：位于你<b>西侧</b>的 ' + hits.join('、') + ' 天线正对着你，形成干扰；其余 4 个背对你，不构成干扰。' +
              '6 个同频小区每隔 60° 一个，120° 的波束范围里恰好落进 <b>2 个</b>。'
            : '6 扇区时每个波束只有 60° 宽。6 个同频小区每隔 60° 一个，60° 的范围里只能落进 <b>1 个</b>：正西方偏 19° 的 ' + hits.join('、') + '。');
      }
    };
  }

  /* ================= A6 · 小区分裂动画 ================= */
  function cellSplit(host) {
    var c = mkCanvas(host, 0.46);
    var cap = caption(host, '小区分裂：半径缩为 1/2 后，同样面积内基站数变为 4 倍，可用信道数也约 4 倍；' +
      '为维持相同的 SIR，微小区发射功率需降为原来的 1/2ⁿ（n=4 时为 1/16，约 −12dB）。');
    function hex(ctx, x, y, s) {
      ctx.beginPath();
      for (var i = 0; i < 6; i++) {
        var a = Math.PI / 180 * (60 * i - 90);
        var px = x + s * Math.cos(a), py = y + s * Math.sin(a);
        i ? ctx.lineTo(px, py) : ctx.moveTo(px, py);
      }
      ctx.closePath();
    }
    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        clear(c); var ctx = c.ctx, P = c.P;
        var phase = (t / 3400) % 1;
        var k = phase < 0.45 ? 0 : (phase < 0.55 ? (phase - 0.45) / 0.1 : 1);
        var cx = c.w / 2, cy = c.h / 2, S = Math.min(c.w / 4.6, c.h / 2.4);
        // 原大小区
        ctx.globalAlpha = 1 - k * 0.72;
        hex(ctx, cx, cy, S);
        ctx.fillStyle = alpha(P.accent, 0.18); ctx.fill();
        ctx.strokeStyle = P.accent; ctx.lineWidth = 2.4; ctx.stroke();
        ctx.globalAlpha = 1;
        if (k < 0.5) {
          ctx.fillStyle = P.accentStrong; ctx.font = F(13, 600);
          ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText('半径 R · 1 个基站 · 60 信道', cx, cy - S - 12);
          ctx.beginPath(); ctx.arc(cx, cy, 6, 0, 7); ctx.fillStyle = P.accentStrong; ctx.fill();
        }
        // 微小区
        if (k > 0) {
          ctx.globalAlpha = k;
          var s2 = S / 2, offs = [[0, 0], [1, 0], [0.5, 1], [-0.5, 1], [-1, 0], [0.5, -1], [-0.5, -1]];
          offs.forEach(function (o, i) {
            var x = cx + o[0] * Math.sqrt(3) * s2, y = cy + o[1] * 1.5 * s2;
            hex(ctx, x, y, s2 * 0.96);
            ctx.fillStyle = alpha(P.good, 0.16 + 0.1 * Math.sin(t / 400 + i)); ctx.fill();
            ctx.strokeStyle = P.good; ctx.lineWidth = 1.6; ctx.stroke();
            ctx.beginPath(); ctx.arc(x, y, 3.4, 0, 7); ctx.fillStyle = P.good; ctx.fill();
          });
          ctx.fillStyle = P.good; ctx.font = F(13, 600);
          ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText('半径 R/2 · 微小区基站 · 功率 −12dB', cx, cy - S - 12);
          ctx.globalAlpha = 1;
        }
      }
    };
  }

  /* ================= B1 · CSMA/CA 时序动画 ================= */
  function csmaAnim(host) {
    var scen = 0, speed = 1;
    segs(host, ['正常 RTS/CTS 交互', '碰撞与二进制指数退避'], 0, function (i) { scen = i; });
    slider(host, '播放速度 ×', 1, 4, 1, 1, function (v) { speed = v; });
    var c = mkCanvas(host, 0.58);
    var cap = caption(host, '');
    var LANES = ['站点 A（发送）', '站点 B（接收/AP）', '站点 C（其它站）'];

    function sched() {
      var b = [], t = 0;
      if (scen === 0) {
        b.push({ l: 0, t: t, d: 50, k: 'ifs', s: 'DIFS', cap: '① A 先侦听信道，确认空闲持续 DIFS（最长的帧间间隔，普通数据帧的最低等待）。' }); t += 50;
        b.push({ l: 0, t: t, d: 60, k: 'bo', s: '退避 3 slots', cap: '② 进入随机退避：在 0~CW−1 个时隙中随机取值并逐隙倒数，信道忙则冻结计数。' }); t += 60;
        b.push({ l: 0, t: t, d: 34, k: 'ctrl', s: 'RTS', cap: '③ A 发送 RTS（请求发送），其中带有本次交互将占用介质的 duration。' }); t += 34;
        b.push({ l: 1, t: t, d: 12, k: 'ifs', s: 'SIFS', cap: '④ B 只等 SIFS（最短间隔，优先级最高）就回应，任何竞争站都抢不到这个空隙。' }); t += 12;
        b.push({ l: 1, t: t, d: 30, k: 'ctrl', s: 'CTS', cap: '⑤ B 回 CTS（允许发送）。关键点：听不到 A 的隐藏节点也能听到这条 CTS。' });
        b.push({ l: 2, t: t, d: 196, k: 'nav', s: 'NAV（推迟发送）', cap: '⑥ C 收到 CTS 后按 duration 设置 NAV 计时器，在整个交互结束前保持静默 —— 虚拟载波侦听。' });
        t += 30;
        b.push({ l: 0, t: t, d: 12, k: 'ifs', s: 'SIFS' }); t += 12;
        b.push({ l: 0, t: t, d: 120, k: 'data', s: 'DATA (MSDU)', cap: '⑦ A 发送数据帧。' }); t += 120;
        b.push({ l: 1, t: t, d: 12, k: 'ifs', s: 'SIFS' }); t += 12;
        b.push({ l: 1, t: t, d: 30, k: 'ack', s: 'ACK', cap: '⑧ B 校验 CRC 通过后回 ACK；A 收不到 ACK 就会重传。这是 802.11 的可靠交付机制。' }); t += 30;
      } else {
        b.push({ l: 0, t: 0, d: 50, k: 'ifs', s: 'DIFS' });
        b.push({ l: 2, t: 0, d: 50, k: 'ifs', s: 'DIFS', cap: '① A 与 C 都在等待 DIFS —— 信道刚空闲，两站同时准备发送。' });
        b.push({ l: 0, t: 50, d: 40, k: 'bo', s: '退避 2', cap: '② 两站各自随机退避，但都抽到了相同的退避值（概率不低，尤其 CW 较小时）。' });
        b.push({ l: 2, t: 50, d: 40, k: 'bo', s: '退避 2' });
        b.push({ l: 0, t: 90, d: 34, k: 'col', s: 'RTS ✗', cap: '③ 退避同时归零，两站同时发送 RTS —— 在 B 处发生碰撞，两帧都被破坏。' });
        b.push({ l: 2, t: 90, d: 34, k: 'col', s: 'RTS ✗' });
        b.push({ l: 1, t: 124, d: 46, k: 'to', s: 'CTS 超时', cap: '④ B 无法正确解码，不会回 CTS；发送方等待超时，判定本次尝试失败。' });
        b.push({ l: 0, t: 170, d: 50, k: 'ifs', s: 'DIFS' });
        b.push({ l: 0, t: 220, d: 110, k: 'bo', s: '退避 0~63（CW 32→64）', cap: '⑤ 二进制指数退避：CW 从 CWmin=32 翻倍到 64，新的退避值从更大的区间中抽取，碰撞概率随之下降（上限 CWmax=256）。' });
        b.push({ l: 2, t: 220, d: 170, k: 'bo', s: '退避 0~63' });
        b.push({ l: 0, t: 330, d: 34, k: 'ctrl', s: 'RTS', cap: '⑥ A 这次先数到 0，抢到信道并成功发出 RTS；C 冻结计数继续等待。' });
        b.push({ l: 1, t: 376, d: 30, k: 'ctrl', s: 'CTS' });
      }
      var end = 0; b.forEach(function (x) { end = Math.max(end, x.t + x.d); });
      return { b: b, end: end + 30 };
    }
    var S = null, curScen = -1;
    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        if (curScen !== scen) { S = sched(); curScen = scen; }
        clear(c); var ctx = c.ctx, P = c.P;
        var L = 96, R = 12, T = 22, laneH = Math.min(44, (c.h - T - 56) / 3), gw = c.w - L - R;
        var play = ((t * speed / 24) % (S.end + 160));
        var COL = {
          ifs: alpha(P.muted, 0.35), bo: alpha(P.warn || P.accent, 0.55), ctrl: P.accent,
          data: P.accentStrong, ack: P.good, nav: alpha(P.muted, 0.3), col: P.bad, to: alpha(P.bad, 0.35)
        };
        ctx.fillStyle = P.muted; ctx.font = F(11, 600); ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
        LANES.forEach(function (n, i) {
          var y = T + i * (laneH + 10);
          ctx.fillStyle = P.muted; ctx.fillText(n, 4, y + laneH / 2);
          ctx.strokeStyle = alpha(P.border, 0.8); ctx.lineWidth = 1;
          ctx.strokeRect(L, y, gw, laneH);
        });
        var curCap = '';
        S.b.forEach(function (x) {
          var y = T + x.l * (laneH + 10);
          var X = L + gw * x.t / S.end, W = gw * x.d / S.end;
          var done = play >= x.t, partial = Math.max(0, Math.min(1, (play - x.t) / x.d));
          ctx.globalAlpha = done ? 1 : 0.16;
          var yy = x.k === 'nav' ? y + laneH * 0.55 : y + 3;
          var hh = x.k === 'nav' ? laneH * 0.4 : laneH - 6;
          ctx.fillStyle = COL[x.k] || P.accent;
          roundRect(ctx, X, yy, Math.max(2, W * (done ? Math.min(1, partial) : 1)), hh, 3);
          ctx.fill();
          if (x.k === 'col' && done) {
            ctx.strokeStyle = P.bad; ctx.lineWidth = 2; ctx.stroke();
          }
          ctx.globalAlpha = done ? 1 : 0.35;
          ctx.fillStyle = (x.k === 'ifs' || x.k === 'nav' || x.k === 'to') ? P.text : (P.dark ? '#07120f' : '#fff');
          ctx.font = FM(Math.max(8, Math.min(10, W / 4.2)), 600);
          ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          if (W > 18) ctx.fillText(x.s, X + W / 2, yy + hh / 2);
          ctx.globalAlpha = 1;
          if (x.cap && play >= x.t && play <= x.t + x.d + 40) curCap = x.cap;
        });
        // 播放头
        var px = L + gw * Math.min(play, S.end) / S.end;
        ctx.strokeStyle = P.text; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(px, T - 8); ctx.lineTo(px, T + 3 * (laneH + 10)); ctx.stroke();
        ctx.fillStyle = P.text; ctx.beginPath();
        ctx.moveTo(px - 5, T - 8); ctx.lineTo(px + 5, T - 8); ctx.lineTo(px, T - 1); ctx.closePath(); ctx.fill();
        // 图例
        var lg = [['DIFS/SIFS', COL.ifs], ['退避', COL.bo], ['控制帧', COL.ctrl], ['数据', COL.data], ['ACK', COL.ack], ['NAV', COL.nav]];
        var lx = L;
        ctx.font = FM(10); ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
        lg.forEach(function (g) {
          ctx.fillStyle = g[1]; roundRect(ctx, lx, c.h - 16, 12, 9, 2); ctx.fill();
          ctx.fillStyle = P.muted; ctx.fillText(g[0], lx + 16, c.h - 11);
          lx += 22 + ctx.measureText(g[0]).width;
        });
        cap.innerHTML = curCap || '时间轴从左向右推进，观察 DIFS → 随机退避 → RTS/CTS → DATA → ACK 的完整流程，以及其它站点如何用 NAV 保持静默。';
      }
    };
  }

  /* ================= B1 · 隐藏节点问题 ================= */
  function hiddenNode(host) {
    var rts = false;
    segs(host, ['不使用 RTS/CTS', '启用 RTS/CTS'], 0, function (i) { rts = (i === 1); t0 = null; });
    var c = mkCanvas(host, 0.55);
    var cap = caption(host, '');
    var t0 = null;
    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        if (t0 === null) t0 = t;
        clear(c); var ctx = c.ctx, P = c.P;
        var cyc = rts ? 6200 : 4200, ph = ((t - t0) % cyc) / cyc;
        var cy = c.h * 0.46, R = Math.min(c.w * 0.24, c.h * 0.42);
        var A = { x: c.w * 0.2, y: cy }, B = { x: c.w * 0.5, y: cy }, C = { x: c.w * 0.8, y: cy };
        // 覆盖圈
        [[A, P.accent], [C, P.warn || P.accent]].forEach(function (p) {
          ctx.strokeStyle = alpha(p[1], 0.5); ctx.setLineDash([5, 5]); ctx.lineWidth = 1.4;
          ctx.beginPath(); ctx.arc(p[0].x, p[0].y, R, 0, 7); ctx.stroke(); ctx.setLineDash([]);
        });
        var msg = '';
        function packet(from, to, prog, col, label) {
          var x = from.x + (to.x - from.x) * prog, y = from.y + (to.y - from.y) * prog;
          ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, 7, 0, 7); ctx.fill();
          ctx.fillStyle = P.text; ctx.font = FM(10, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
          ctx.fillText(label, x, y - 10);
        }
        var collide = false;
        if (!rts) {
          if (ph < 0.3) { packet(A, B, ph / 0.3, P.accent, 'DATA'); msg = '① A 向 B 发送数据。C 在 A 的覆盖范围之外，<b>侦听不到</b> A 的发送。'; }
          else if (ph < 0.6) {
            packet(A, B, 1, P.accent, 'DATA'); packet(C, B, (ph - 0.3) / 0.3, P.warn || P.bad, 'DATA');
            msg = '② C 侦听信道认为空闲，于是也开始向 B 发送。';
          } else {
            collide = true;
            msg = '③ 两个信号在 B 处<b>碰撞</b>，两帧都被破坏 —— 这就是隐藏节点问题，吞吐量因此大幅下降。';
          }
        } else {
          if (ph < 0.2) { packet(A, B, ph / 0.2, P.accent, 'RTS'); msg = '① A 先发 RTS 给 B，请求预约信道（C 仍听不到）。'; }
          else if (ph < 0.42) {
            var pr = (ph - 0.2) / 0.22;
            packet(B, A, pr, P.good, 'CTS'); packet(B, C, pr, P.good, 'CTS');
            msg = '② B 广播 CTS。<b>关键：C 在 B 的覆盖范围内，能收到这条 CTS</b>。';
          } else if (ph < 0.55) { msg = '③ C 依据 CTS 中的 duration 设置 <b>NAV</b>，在整个交互结束前保持静默。'; }
          else if (ph < 0.82) { packet(A, B, (ph - 0.55) / 0.27, P.accent, 'DATA'); msg = '④ A 无碰撞地完成数据发送。'; }
          else { packet(B, A, (ph - 0.82) / 0.18, P.good, 'ACK'); msg = '⑤ B 回 ACK，交互成功完成。'; }
        }
        // 节点
        [[A, 'A', P.accent], [B, 'B', P.good], [C, 'C', P.warn || P.bad]].forEach(function (p) {
          var silent = rts && ph >= 0.42 && p[1] === 'C';
          ctx.beginPath(); ctx.arc(p[0].x, p[0].y, 22, 0, 7);
          ctx.fillStyle = silent ? alpha(P.muted, 0.25) : alpha(p[2], 0.25); ctx.fill();
          ctx.strokeStyle = silent ? P.muted : p[2]; ctx.lineWidth = 2.2; ctx.stroke();
          ctx.fillStyle = P.text; ctx.font = F(14, 700); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText(p[1], p[0].x, p[0].y);
          if (silent) {
            ctx.fillStyle = P.muted; ctx.font = FM(10, 600); ctx.textBaseline = 'top';
            ctx.fillText('NAV 静默', p[0].x, p[0].y + 26);
          }
        });
        if (collide) {
          var pulse = 0.5 + 0.5 * Math.sin(t / 90);
          ctx.strokeStyle = P.bad; ctx.lineWidth = 3;
          ctx.beginPath(); ctx.arc(B.x, B.y, 30 + pulse * 10, 0, 7); ctx.stroke();
          ctx.fillStyle = P.bad; ctx.font = F(13, 700); ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
          ctx.fillText('碰撞！', B.x, B.y - 34);
        }
        ctx.fillStyle = P.muted; ctx.font = FM(10); ctx.textAlign = 'center'; ctx.textBaseline = 'top';
        ctx.fillText('虚线 = 无线覆盖范围：A 与 C 互相听不到，但都能与 B 通信', c.w / 2, c.h - 16);
        cap.innerHTML = msg;
      }
    };
  }

  /* ================= B2 · Ad Hoc 多跳路由 ================= */
  function adhocRoute(host) {
    var c = mkCanvas(host, 0.6);
    var cap = caption(host, '');
    var t0 = null;
    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        if (t0 === null) t0 = t;
        clear(c); var ctx = c.ctx, P = c.P;
        var cyc = 11000, ph = ((t - t0) % cyc) / cyc;
        var W = c.w, H = c.h;
        var drift = ph > 0.55 ? Math.min(1, (ph - 0.55) / 0.2) : 0;
        var N = {
          A: { x: 0.12 * W, y: 0.62 * H }, B: { x: 0.36 * W, y: 0.34 * H },
          C: { x: 0.62 * W, y: 0.60 * H }, D: { x: 0.44 * W + drift * 0.16 * W, y: 0.80 * H + drift * 0.14 * H },
          E: { x: 0.86 * W, y: 0.36 * H }
        };
        var range = Math.min(W, H) * 0.42;
        function near(a, b) { return Math.hypot(N[a].x - N[b].x, N[a].y - N[b].y) < range; }
        var pairs = [['A', 'B'], ['B', 'C'], ['C', 'E'], ['A', 'D'], ['D', 'C'], ['B', 'D'], ['C', 'D']];
        pairs.forEach(function (p) {
          if (!near(p[0], p[1])) return;
          ctx.strokeStyle = alpha(P.border, 1); ctx.lineWidth = 1.2; ctx.setLineDash([4, 4]);
          ctx.beginPath(); ctx.moveTo(N[p[0]].x, N[p[0]].y); ctx.lineTo(N[p[1]].x, N[p[1]].y); ctx.stroke();
          ctx.setLineDash([]);
        });
        var route = ['A', 'B', 'C', 'E'], msg = '';
        if (ph < 0.18) {
          msg = '① <b>信标（beaconing）</b>：各节点广播自身地址与位置，邻居据此建立/更新路由表。';
          ['A', 'B', 'C', 'D', 'E'].forEach(function (k, i) {
            var rr = ((t / 700 + i * 0.2) % 1) * range;
            ctx.strokeStyle = alpha(P.accent, 0.5 * (1 - rr / range)); ctx.lineWidth = 1.6;
            ctx.beginPath(); ctx.arc(N[k].x, N[k].y, rr, 0, 7); ctx.stroke();
          });
        } else if (ph < 0.52) {
          msg = '② A 要发给 E，但两者不在彼此覆盖内 → 通过 <b>B、C 中继多跳转发</b>。Ad Hoc 网络中每个节点都必须能按需充当路由器。';
        } else if (ph < 0.78) {
          msg = '③ 节点移动导致拓扑变化：链路断开，路由失效 —— 这就是需要<b>路由重构（route reconfiguration）</b>的原因。';
        } else {
          msg = '④ 协议重新发现可用路径并恢复通信。若拓扑变化快于路由更新的传播速度，网络将失去<b>组合稳定性</b>。';
        }
        // 路径高亮与数据包
        if (ph >= 0.18 && ph < 0.52) {
          var seg = (ph - 0.18) / 0.34 * (route.length - 1);
          for (var i = 0; i < route.length - 1; i++) {
            ctx.strokeStyle = i < seg ? P.accent : alpha(P.accent, 0.25);
            ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(N[route[i]].x, N[route[i]].y);
            ctx.lineTo(N[route[i + 1]].x, N[route[i + 1]].y); ctx.stroke();
          }
          var si = Math.min(route.length - 2, Math.floor(seg)), fr = seg - si;
          var a = N[route[si]], b = N[route[si + 1]];
          ctx.fillStyle = P.accentStrong;
          ctx.beginPath(); ctx.arc(a.x + (b.x - a.x) * fr, a.y + (b.y - a.y) * fr, 7, 0, 7); ctx.fill();
        }
        if (ph >= 0.78) {
          var r2 = ['A', 'B', 'C', 'E'];
          for (var j = 0; j < r2.length - 1; j++) {
            ctx.strokeStyle = P.good; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(N[r2[j]].x, N[r2[j]].y); ctx.lineTo(N[r2[j + 1]].x, N[r2[j + 1]].y); ctx.stroke();
          }
        }
        Object.keys(N).forEach(function (k) {
          var p = N[k], isEnd = (k === 'A' || k === 'E');
          ctx.beginPath(); ctx.arc(p.x, p.y, 20, 0, 7);
          ctx.fillStyle = isEnd ? alpha(P.accent, 0.3) : alpha(P.muted, 0.18); ctx.fill();
          ctx.strokeStyle = isEnd ? P.accent : P.muted; ctx.lineWidth = 2; ctx.stroke();
          ctx.fillStyle = P.text; ctx.font = F(13, 700); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText(k, p.x, p.y);
        });
        cap.innerHTML = msg;
      }
    };
  }

  /* ================= B1 · 802.11 超帧结构 ================= */
  function superframe(host) {
    var c = mkCanvas(host, 0.4);
    var cap = caption(host, '超帧 = CFP（无竞争期，AP 用 PIFS 轮询各站）+ CP（竞争期，各站用 DCF 竞争）。' +
      '由于 SIFS &lt; PIFS &lt; DIFS，CFP 的优先级高于 CP，竞争期无法打断无竞争期。');
    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        clear(c); var ctx = c.ctx, P = c.P;
        var L = 10, R = 10, T = 26, gw = c.w - L - R, barH = 40;
        var segsArr = [
          { w: 0.05, c: P.accentStrong, s: 'DTIM\nBeacon' },
          { w: 0.38, c: alpha(P.accent, 0.55), s: 'CFP（PCF 轮询）' },
          { w: 0.42, c: alpha(P.muted, 0.35), s: 'CP（DCF 竞争）' },
          { w: 0.05, c: P.accentStrong, s: 'Beacon' },
          { w: 0.10, c: alpha(P.accent, 0.3), s: 'CFP…' }
        ];
        var x = L;
        segsArr.forEach(function (s, i) {
          var w = gw * s.w;
          ctx.fillStyle = s.c; roundRect(ctx, x, T, w - 2, barH, 3); ctx.fill();
          ctx.fillStyle = i === 0 || i === 3 ? (P.dark ? '#08100e' : '#fff') : P.text;
          ctx.font = F(Math.min(11, w / 5), 600); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          s.s.split('\n').forEach(function (line, k, arr) {
            ctx.fillText(line, x + w / 2, T + barH / 2 + (k - (arr.length - 1) / 2) * 12);
          });
          x += w;
        });
        // 轮询箭头动画
        var pp = (t / 2000) % 1;
        var cfpX = L + gw * 0.05, cfpW = gw * 0.38;
        var ax = cfpX + cfpW * pp;
        ctx.strokeStyle = P.accentStrong; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(ax, T - 4); ctx.lineTo(ax, T - 14); ctx.stroke();
        ctx.fillStyle = P.accentStrong; ctx.font = FM(10, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
        ctx.fillText('CF-Poll →', ax, T - 16);
        // 超帧括号
        var sy = T + barH + 12;
        ctx.strokeStyle = P.muted; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(L, sy); ctx.lineTo(L + gw * 0.85, sy); ctx.stroke();
        ctx.fillStyle = P.muted; ctx.font = F(11, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'top';
        ctx.fillText('一个超帧 Superframe = CFP + CP（长度可随话务调整）', L + gw * 0.42, sy + 4);
        // IFS 标尺
        var iy = sy + 28;
        [['SIFS', 0.10, P.good], ['PIFS', 0.17, P.accent], ['DIFS', 0.26, P.bad]].forEach(function (f, i) {
          var w = gw * f[1] * 0.5;
          ctx.fillStyle = alpha(f[2], 0.65);
          roundRect(ctx, L + i * (gw * 0.2), iy, w, 14, 3); ctx.fill();
          ctx.fillStyle = P.text; ctx.font = FM(10, 600); ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
          ctx.fillText(f[0] + (i === 0 ? '（最短→优先级最高）' : (i === 2 ? '（最长→优先级最低）' : '')), L + i * (gw * 0.2) + w + 6, iy + 7);
        });
      }
    };
  }

  /* ================= B3 · LTE 帧结构与资源网格 ================= */
  function lteGrid(host) {
    var BW = [[1.4, 6], [3, 15], [5, 25], [10, 50], [15, 75], [20, 100]];
    var idx = 5;
    segs(host, BW.map(function (b) { return b[0] + 'MHz'; }), 5, function (i) { idx = i; });
    var c = mkCanvas(host, 0.55);
    var cap = caption(host, '');
    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        clear(c); var ctx = c.ctx, P = c.P;
        var nRB = BW[idx][1];
        var L = 8, gw = c.w * 0.52, T = 24;
        // 左：无线帧 → 子帧 → 时隙
        ctx.fillStyle = P.muted; ctx.font = F(11, 600); ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
        ctx.fillText('无线帧 10 ms = 10 个子帧', L, T - 6);
        var sfW = gw / 10, active = Math.floor((t / 400) % 10);
        for (var i = 0; i < 10; i++) {
          ctx.fillStyle = i === active ? P.accent : alpha(P.muted, 0.25);
          roundRect(ctx, L + i * sfW, T, sfW - 3, 26, 3); ctx.fill();
          ctx.fillStyle = i === active ? (P.dark ? '#08100e' : '#fff') : P.muted;
          ctx.font = FM(9, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText('#' + i, L + i * sfW + sfW / 2 - 1.5, T + 13);
        }
        // 放大子帧
        var y2 = T + 46;
        ctx.strokeStyle = alpha(P.accent, 0.5); ctx.setLineDash([3, 3]); ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(L + active * sfW, T + 26); ctx.lineTo(L, y2);
        ctx.moveTo(L + active * sfW + sfW - 3, T + 26); ctx.lineTo(L + gw, y2);
        ctx.stroke(); ctx.setLineDash([]);
        ctx.fillStyle = P.muted; ctx.font = F(11, 600); ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
        ctx.fillText('1 个子帧 1 ms = 2 个时隙 × 0.5 ms', L, y2 - 4);
        [0, 1].forEach(function (k) {
          ctx.fillStyle = alpha(P.accent, k ? 0.35 : 0.6);
          roundRect(ctx, L + k * gw / 2, y2, gw / 2 - 4, 24, 3); ctx.fill();
          ctx.fillStyle = P.text; ctx.font = FM(10, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText('时隙 ' + k + '（0.5ms）', L + k * gw / 2 + gw / 4 - 2, y2 + 12);
        });
        // 右：资源块网格
        var RX = c.w * 0.60, RY = T, RW = c.w - RX - 8, RH = c.h - T - 44;
        ctx.fillStyle = P.muted; ctx.font = F(11, 600); ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
        ctx.fillText('1 个资源块 RB：12 子载波 × 7 符号', RX, RY - 6);
        var cw = RW / 7, ch = RH / 12;
        for (var s = 0; s < 7; s++) for (var f = 0; f < 12; f++) {
          var lit = ((s + f * 2 + Math.floor(t / 160)) % 19) < 3;
          ctx.fillStyle = lit ? alpha(P.accent, 0.75) : alpha(P.muted, 0.18);
          ctx.fillRect(RX + s * cw + 1, RY + f * ch + 1, cw - 2, ch - 2);
        }
        ctx.strokeStyle = P.border; ctx.lineWidth = 1; ctx.strokeRect(RX, RY, RW, RH);
        ctx.fillStyle = P.muted; ctx.font = FM(9); ctx.textAlign = 'center'; ctx.textBaseline = 'top';
        ctx.fillText('7 个 OFDM 符号（常规 CP）→', RX + RW / 2, RY + RH + 4);
        ctx.save(); ctx.translate(RX - 6, RY + RH / 2); ctx.rotate(-Math.PI / 2);
        ctx.textAlign = 'center'; ctx.textBaseline = 'bottom'; ctx.fillText('12 个子载波', 0, 0); ctx.restore();

        var re = nRB * 12 * 14;
        cap.innerHTML = '带宽 <b>' + BW[idx][0] + ' MHz</b> → <b>' + nRB + '</b> 个资源块 → ' +
          '频域共 <b>' + (nRB * 12) + '</b> 个子载波；每 1ms 子帧共 <b>' + re.toLocaleString() + '</b> 个资源单元（RE）可供调度。' +
          '调度器每 1ms 根据信道质量把 RB 分配给不同 UE（OFDMA）。';
      }
    };
  }

  /* ================= B4 · IoT 通信范围谱 ================= */
  function iotRange(host) {
    var c = mkCanvas(host, 0.44);
    var cap = caption(host, '选择 IoT 接入技术的第一考虑是<b>通信范围</b>，其次是单元内对象数量、成本、功耗与可用带宽。');
    var ROWS = [
      { n: 'PAN 个域网', lo: 1, hi: 10, e: 'Bluetooth' },
      { n: 'HAN 家域网', lo: 10, hi: 50, e: 'ZigBee / BLE' },
      { n: 'NAN 邻域网', lo: 50, hi: 500, e: '802.11 mesh' },
      { n: 'FAN 场域网', lo: 100, hi: 1000, e: '802.15.4g' },
      { n: 'LAN 局域网', lo: 10, hi: 100, e: '802.11 / Wi-Fi' },
      { n: 'MAN/WAN', lo: 1000, hi: 50000, e: 'LoRa / NB-IoT / 蜂窝' }
    ];
    return {
      animated: false,
      resize: function () { c.resize(); },
      draw: function () {
        clear(c); var ctx = c.ctx, P = c.P;
        var L = 96, R = 12, T = 14, B = 26, gw = c.w - L - R, gh = c.h - T - B;
        var x0 = 0, x1 = log10(50000);
        function X(m) { return L + gw * (log10(Math.max(1, m)) - x0) / (x1 - x0); }
        [1, 10, 100, 1000, 10000].forEach(function (m) {
          ctx.strokeStyle = alpha(P.border, 0.7); ctx.beginPath();
          ctx.moveTo(X(m), T); ctx.lineTo(X(m), T + gh); ctx.stroke();
          ctx.fillStyle = P.muted; ctx.font = FM(10); ctx.textAlign = 'center'; ctx.textBaseline = 'top';
          ctx.fillText(m >= 1000 ? (m / 1000) + 'km' : m + 'm', X(m), T + gh + 4);
        });
        var rh = gh / ROWS.length;
        ROWS.forEach(function (r, i) {
          var y = T + i * rh + rh * 0.18, h = rh * 0.6;
          ctx.fillStyle = alpha(P.accent, 0.25 + i * 0.09);
          roundRect(ctx, X(r.lo), y, Math.max(6, X(r.hi) - X(r.lo)), h, 4); ctx.fill();
          ctx.strokeStyle = P.accent; ctx.lineWidth = 1.2; ctx.stroke();
          ctx.fillStyle = P.text; ctx.font = F(11, 600); ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
          ctx.fillText(r.n, L - 6, y + h / 2);
          ctx.fillStyle = P.muted; ctx.font = FM(10); ctx.textAlign = 'left';
          ctx.fillText(r.e, X(r.hi) + 6, y + h / 2);
        });
      }
    };
  }

  /* ================= C1 · 卫星轨道动画 ================= */
  function orbitAnim(host) {
    var sel = 2, speedH = 1.5;  // 模拟：每真实秒推进多少小时
    segs(host, ['LEO 800km', 'MEO 20,200km', 'GEO 35,863km', '三者同时'], 2, function (i) { sel = i; });
    slider(host, '时间加速（小时 / 秒）', 0.2, 6, 1.5, 0.2, function (v) { speedH = v; });
    var c = mkCanvas(host, 0.72);
    var cap = caption(host, '');
    var MU = 398600.4418, RE = 6378;
    var SATS = [
      { n: 'LEO', h: 800, col: null }, { n: 'MEO', h: 20200, col: null }, { n: 'GEO', h: 35863, col: null }
    ];
    SATS.forEach(function (s) { s.a = RE + s.h; s.T = 2 * Math.PI * Math.sqrt(Math.pow(s.a, 3) / MU) / 3600; });
    var simH = 0, last = null;
    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        var dt = last === null ? 0 : (t - last) / 1000; last = t;
        simH += dt * speedH;
        clear(c); var ctx = c.ctx, P = c.P;
        var cx = c.w / 2, cy = c.h / 2, rE = Math.min(c.w, c.h) * 0.14;
        var maxR = Math.min(c.w, c.h) * 0.46;
        function rad(h) { return rE + (maxR - rE) * (log10(1 + h / 300) / log10(1 + 35863 / 300)); }
        var cols = [P.good, P.warn || P.accent, P.accent];

        // 地球
        var spin = (simH / 24) * 2 * Math.PI;
        ctx.beginPath(); ctx.arc(cx, cy, rE, 0, 7);
        ctx.fillStyle = P.dark ? '#16343f' : '#cfe6ea'; ctx.fill();
        ctx.strokeStyle = alpha(P.accent, 0.6); ctx.lineWidth = 1.4; ctx.stroke();
        ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, rE, 0, 7); ctx.clip();
        ctx.strokeStyle = alpha(P.accent, 0.35); ctx.lineWidth = 1;
        for (var m = 0; m < 6; m++) {
          var a = spin + m * Math.PI / 3;
          ctx.beginPath();
          ctx.ellipse(cx, cy, Math.abs(rE * Math.cos(a)), rE, 0, 0, 7); ctx.stroke();
        }
        ctx.beginPath(); ctx.moveTo(cx - rE, cy); ctx.lineTo(cx + rE, cy); ctx.stroke();
        ctx.restore();
        // 地面站（随地球自转）
        var gsA = spin;
        var gx = cx + Math.cos(gsA) * rE, gy = cy + Math.sin(gsA) * rE;
        ctx.fillStyle = P.bad; ctx.beginPath(); ctx.arc(gx, gy, 4.5, 0, 7); ctx.fill();
        ctx.fillStyle = P.bad; ctx.font = FM(10, 600);
        ctx.textAlign = Math.cos(gsA) > 0 ? 'left' : 'right'; ctx.textBaseline = 'middle';
        ctx.fillText('地面站', gx + (Math.cos(gsA) > 0 ? 8 : -8), gy);

        var show = sel === 3 ? [0, 1, 2] : [sel];
        SATS.forEach(function (s, i) {
          var r = rad(s.h), on = show.indexOf(i) >= 0;
          ctx.strokeStyle = on ? alpha(cols[i], 0.55) : alpha(P.border, 0.5);
          ctx.setLineDash(on ? [] : [3, 4]); ctx.lineWidth = on ? 1.4 : 1;
          ctx.beginPath(); ctx.arc(cx, cy, r, 0, 7); ctx.stroke(); ctx.setLineDash([]);
          if (!on) return;
          var ang = (simH / s.T) * 2 * Math.PI;
          var sx = cx + Math.cos(ang) * r, sy = cy + Math.sin(ang) * r;
          // 覆盖锥
          var lam = Math.acos(Math.min(1, RE / s.a));
          ctx.fillStyle = alpha(cols[i], 0.13);
          ctx.beginPath(); ctx.moveTo(sx, sy);
          ctx.arc(cx, cy, rE, ang - lam, ang + lam); ctx.closePath(); ctx.fill();
          // 卫星
          ctx.fillStyle = cols[i];
          ctx.beginPath(); ctx.arc(sx, sy, 6, 0, 7); ctx.fill();
          ctx.strokeStyle = cols[i]; ctx.lineWidth = 1.6;
          ctx.beginPath(); ctx.moveTo(sx - 12, sy); ctx.lineTo(sx - 6, sy);
          ctx.moveTo(sx + 6, sy); ctx.lineTo(sx + 12, sy); ctx.stroke();
          ctx.fillStyle = cols[i]; ctx.font = FM(10, 600);
          ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
          ctx.fillText(s.n, sx, sy - 10);
          // 与地面站的连线（可见时）
          var dA = Math.abs(((ang - gsA + Math.PI * 3) % (2 * Math.PI)) - Math.PI);
          if (dA < lam) {
            ctx.strokeStyle = alpha(cols[i], 0.75); ctx.setLineDash([4, 3]); ctx.lineWidth = 1.3;
            ctx.beginPath(); ctx.moveTo(gx, gy); ctx.lineTo(sx, sy); ctx.stroke(); ctx.setLineDash([]);
          }
        });
        ctx.fillStyle = P.muted; ctx.font = FM(11); ctx.textAlign = 'left'; ctx.textBaseline = 'top';
        ctx.fillText('模拟时间 ' + simH.toFixed(1) + ' 小时　（径向距离经对数压缩显示）', 4, 4);
        ctx.textAlign = 'right';
        ctx.fillText('周期：LEO ' + SATS[0].T.toFixed(2) + 'h · MEO ' + SATS[1].T.toFixed(2) + 'h · GEO ' + SATS[2].T.toFixed(2) + 'h', c.w - 4, 4);
        cap.innerHTML = '地球自转周期 24h。<b>GEO 周期恰好等于 23.93h，因此始终停在地面站正上方</b>（连线不断）；' +
          'LEO 约 100 分钟绕一圈，几分钟就掠过地面站 → 必须频繁切换、跟踪天线且多普勒频移大；MEO 介于两者之间。';
      }
    };
  }

  /* ================= C2 · 卫星几何示意图 ================= */
  function satGeometry(host) {
    var c = mkCanvas(host, 0.62);
    var cap = caption(host, '仰角 θ 越低，斜距 d 越大、穿过大气的路径越长；θ = 0° 时覆盖最大但链路最差。' +
      '中心角 γ 决定了单颗卫星的覆盖张角与覆盖面积。');
    return {
      animated: false, redrawOn: ['sat_h', 'sat_el'],
      resize: function () { c.resize(); },
      draw: function () {
        clear(c); var ctx = c.ctx, P = c.P;
        var RE = 6378;
        var hi = document.getElementById('sat_h'), h = hi ? parseFloat(hi.value) : 35863;
        var ei = document.getElementById('sat_el'), th = ei ? parseFloat(ei.value) : 10;
        var thr = th * Math.PI / 180;
        var psi = Math.asin(Math.min(1, RE * Math.cos(thr) / (RE + h)));
        var gam = Math.PI / 2 - thr - psi;

        var cx = c.w * 0.5, cy = c.h * 1.02, rE = Math.min(c.w * 0.42, c.h * 0.78);
        var rS = rE * (1 + Math.min(1.5, (h / RE) * 0.42));
        // 地球
        ctx.beginPath(); ctx.arc(cx, cy, rE, Math.PI, 2 * Math.PI);
        ctx.fillStyle = P.dark ? '#16343f' : '#cfe6ea'; ctx.fill();
        ctx.strokeStyle = alpha(P.accent, 0.7); ctx.lineWidth = 1.4; ctx.stroke();
        // 覆盖弧
        ctx.strokeStyle = P.accent; ctx.lineWidth = 4;
        ctx.beginPath(); ctx.arc(cx, cy, rE, -Math.PI / 2 - gam, -Math.PI / 2 + gam); ctx.stroke();
        // 卫星
        var sx = cx, sy = cy - rS;
        // 地面站位置（中心角 γ）
        var ex = cx + Math.sin(gam) * rE, ey = cy - Math.cos(gam) * rE;
        // 连线
        ctx.strokeStyle = alpha(P.muted, 0.8); ctx.lineWidth = 1.2; ctx.setLineDash([4, 4]);
        ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(sx, sy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(ex, ey); ctx.stroke();
        ctx.setLineDash([]);
        ctx.strokeStyle = P.accentStrong; ctx.lineWidth = 2.2;
        ctx.beginPath(); ctx.moveTo(ex, ey); ctx.lineTo(sx, sy); ctx.stroke();
        // 本地水平线
        var hx = ex - cx, hy = ey - cy, L = Math.hypot(hx, hy);
        var tx = -hy / L, ty = hx / L;
        ctx.strokeStyle = alpha(P.bad, 0.8); ctx.lineWidth = 1.4; ctx.setLineDash([5, 4]);
        ctx.beginPath(); ctx.moveTo(ex - tx * 40, ey - ty * 40); ctx.lineTo(ex + tx * 70, ey + ty * 70); ctx.stroke();
        ctx.setLineDash([]);
        // 角度标注
        function arcLabel(x, y, a0, a1, r, col, txt) {
          ctx.strokeStyle = col; ctx.lineWidth = 1.6;
          ctx.beginPath(); ctx.arc(x, y, r, a0, a1); ctx.stroke();
          var am = (a0 + a1) / 2;
          ctx.fillStyle = col; ctx.font = FM(11, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          ctx.fillText(txt, x + Math.cos(am) * (r + 14), y + Math.sin(am) * (r + 14));
        }
        arcLabel(cx, cy, -Math.PI / 2, -Math.PI / 2 + gam, rE * 0.34, P.accent, 'γ=' + (gam * 180 / Math.PI).toFixed(1) + '°');
        var aE_h = Math.atan2(ty, tx), aE_s = Math.atan2(sy - ey, sx - ex);
        arcLabel(ex, ey, aE_s, aE_h, 30, P.bad, 'θ=' + th + '°');
        var aS_o = Math.atan2(cy - sy, cx - sx), aS_e = Math.atan2(ey - sy, ex - sx);
        arcLabel(sx, sy, aS_o, aS_e, 26, P.muted, 'ψ=' + (psi * 180 / Math.PI).toFixed(1) + '°');
        // 点与文字
        ctx.fillStyle = P.accentStrong; ctx.beginPath(); ctx.arc(sx, sy, 7, 0, 7); ctx.fill();
        ctx.fillStyle = P.text; ctx.font = F(11, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
        ctx.fillText('卫星 (h=' + h.toLocaleString() + 'km)', sx, sy - 12);
        ctx.fillStyle = P.bad; ctx.beginPath(); ctx.arc(ex, ey, 5, 0, 7); ctx.fill();
        ctx.fillStyle = P.text; ctx.textAlign = 'left';
        ctx.fillText('地球站', ex + 8, ey - 6);
        // 斜距标注
        var d = (RE + h) * Math.sin(gam) / Math.cos(thr);
        ctx.fillStyle = P.accentStrong; ctx.font = FM(11, 600);
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText('斜距 d = ' + d.toFixed(0) + ' km', (sx + ex) / 2 + 40, (sy + ey) / 2);
        ctx.fillStyle = P.muted; ctx.font = FM(10); ctx.textAlign = 'left'; ctx.textBaseline = 'top';
        ctx.fillText('O = 地心　红色虚线 = 地球站本地水平面', 4, 4);
      }
    };
  }

  /* ================= C3 · 卫星容量分配 ================= */
  function satAccess(host) {
    var mode = 0;
    segs(host, ['FAMA-FDMA', 'TDMA 帧', 'SS/TDMA 星上交换'], 0, function (i) { mode = i; });
    var c = mkCanvas(host, 0.5);
    var cap = caption(host, '');
    var TXT = [
      'FAMA-FDMA：各地球站<b>预先固定分配</b>频带，互不干扰但需要保护频带；需求波动时容量闲置严重（DAMA 则按需动态分配这些子信道）。',
      'TDMA：各站在<b>同一频带</b>内轮流占用时隙，帧首为参考突发（同步），各业务突发之间只需很短的保护时间 —— 这正是 TDMA 通常比 FDMA 高效的原因。',
      'SS/TDMA：卫星上的开关矩阵按<b>模式</b>把 N 个上行波束路由到 N 个下行波束，每个时隙可切换一次模式；实现全连接需要 N! 种模式，模式序列可由地面指令调整。'
    ];
    return {
      animated: true,
      resize: function () { c.resize(); },
      draw: function (t) {
        clear(c); var ctx = c.ctx, P = c.P; cap.innerHTML = TXT[mode];
        var L = 44, R = 14, T = 18, B = 28, gw = c.w - L - R, gh = c.h - T - B;
        if (mode === 0) {
          var st = ['站 A', '站 B', '站 C', '站 D'];
          st.forEach(function (s, i) {
            var y = T + gh * i / 4 + 4, hh = gh / 4 - 14;
            ctx.fillStyle = alpha(P.accent, 0.35 + i * 0.12);
            roundRect(ctx, L, y, gw, hh, 3); ctx.fill();
            ctx.fillStyle = P.text; ctx.font = F(11, 600); ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
            ctx.fillText(s + ' 的固定频带', L + 10, y + hh / 2);
            ctx.fillStyle = alpha(P.muted, 0.35);
            ctx.fillRect(L, y + hh, gw, 10);
            ctx.fillStyle = P.muted; ctx.font = FM(9); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            ctx.fillText('保护频带 guard band', L + gw / 2, y + hh + 5);
          });
          ctx.save(); ctx.translate(14, T + gh / 2); ctx.rotate(-Math.PI / 2);
          ctx.fillStyle = P.muted; ctx.font = F(11); ctx.textAlign = 'center';
          ctx.fillText('频率 →', 0, 0); ctx.restore();
        } else if (mode === 1) {
          var segsT = [{ w: 0.10, s: '参考突发', c: P.accentStrong }, { w: 0.02, s: '', c: P.muted },
          { w: 0.20, s: '站 A 突发', c: P.accent }, { w: 0.02, s: '', c: P.muted },
          { w: 0.20, s: '站 B 突发', c: P.accent }, { w: 0.02, s: '', c: P.muted },
          { w: 0.20, s: '站 C 突发', c: P.accent }, { w: 0.02, s: '', c: P.muted },
          { w: 0.18, s: '站 D 突发', c: P.accent }];
          var x = L, cur = (t / 3000) % 1;
          segsT.forEach(function (s) {
            var w = gw * s.w, act = (x - L) / gw <= cur && cur < (x - L + w) / gw;
            ctx.fillStyle = s.s ? alpha(s.c, act ? 0.95 : 0.5) : alpha(P.muted, 0.3);
            roundRect(ctx, x, T + 18, w - 1, 46, 3); ctx.fill();
            if (s.s) {
              ctx.fillStyle = P.dark ? '#08100e' : '#fff'; ctx.font = F(Math.min(11, w / 5), 600);
              ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
              ctx.fillText(s.s, x + w / 2, T + 41);
            }
            x += w;
          });
          ctx.fillStyle = P.muted; ctx.font = FM(10); ctx.textAlign = 'center'; ctx.textBaseline = 'top';
          ctx.fillText('一个 TDMA 帧（周期重复）　窄条 = 保护时间 guard time', L + gw / 2, T + 70);
          var pxx = L + gw * cur;
          ctx.strokeStyle = P.text; ctx.lineWidth = 1.6;
          ctx.beginPath(); ctx.moveTo(pxx, T + 10); ctx.lineTo(pxx, T + 68); ctx.stroke();
        } else {
          var N = 3, modeIdx = Math.floor(t / 1400) % 6;
          var perms = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]];
          var pm = perms[modeIdx];
          var lx = L + 30, rx = L + gw - 30, ys = [];
          for (var i = 0; i < N; i++) ys.push(T + 24 + i * (gh - 50) / (N - 1));
          for (var i2 = 0; i2 < N; i2++) {
            ctx.fillStyle = alpha(P.accent, 0.8);
            ctx.beginPath(); ctx.arc(lx, ys[i2], 13, 0, 7); ctx.fill();
            ctx.fillStyle = P.dark ? '#08100e' : '#fff'; ctx.font = FM(11, 600);
            ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('U' + (i2 + 1), lx, ys[i2]);
            ctx.fillStyle = alpha(P.good, 0.8);
            ctx.beginPath(); ctx.arc(rx, ys[i2], 13, 0, 7); ctx.fill();
            ctx.fillStyle = P.dark ? '#08100e' : '#fff';
            ctx.fillText('D' + (i2 + 1), rx, ys[i2]);
            ctx.strokeStyle = alpha(P.accentStrong, 0.85); ctx.lineWidth = 2.4;
            ctx.beginPath(); ctx.moveTo(lx + 14, ys[i2]);
            ctx.bezierCurveTo((lx + rx) / 2, ys[i2], (lx + rx) / 2, ys[pm[i2]], rx - 14, ys[pm[i2]]);
            ctx.stroke();
          }
          ctx.fillStyle = P.muted; ctx.font = F(11, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'top';
          ctx.fillText('上行波束', lx, T + 2); ctx.fillText('下行波束', rx, T + 2);
          ctx.fillStyle = P.text; ctx.font = FM(12, 600); ctx.textBaseline = 'bottom';
          ctx.fillText('星上开关模式 ' + (modeIdx + 1) + ' / 3! = 6', c.w / 2, c.h - 6);
        }
      }
    };
  }

  /* ---------- 注册与主循环 ---------- */
  var builders = {
    hexReuse: hexReuse, accessAnim: accessAnim, handoverAnim: handoverAnim,
    pathLossChart: pathLossChart, sirChart: sirChart, erlangChart: erlangChart,
    sectorViz: sectorViz, cellSplit: cellSplit, csmaAnim: csmaAnim, hiddenNode: hiddenNode,
    adhocRoute: adhocRoute, superframe: superframe, lteGrid: lteGrid, iotRange: iotRange,
    orbitAnim: orbitAnim, satGeometry: satGeometry, satAccess: satAccess
  };

  function visible(host) {
    if (!host.offsetParent) return false;
    var r = host.getBoundingClientRect();
    return r.bottom > -80 && r.top < (window.innerHeight || 800) + 80;
  }

  function loop(t) {
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      if (!visible(it.host)) continue;
      if (it.v.animated && !reduced) it.v.draw(t);
      else if (it.dirty) { it.v.draw(t); it.dirty = false; }
    }
    requestAnimationFrame(loop);
  }

  function init() {
    document.querySelectorAll('[data-viz]').forEach(function (host) {
      var b = builders[host.getAttribute('data-viz')];
      if (!b) return;
      var v = b(host);
      var it = { host: host, v: v, dirty: true };
      items.push(it);
      if (v.redrawOn) v.redrawOn.forEach(function (id) {
        var e = document.getElementById(id);
        if (e) e.addEventListener('input', function () { it.dirty = true; });
        if (e) e.addEventListener('change', function () { it.dirty = true; });
      });
    });
    window.addEventListener('resize', function () {
      items.forEach(function (it) { if (it.v.resize) it.v.resize(); it.dirty = true; });
    });
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    if (mq.addEventListener) mq.addEventListener('change', function () {
      items.forEach(function (it) { if (it.v.resize) it.v.resize(); it.dirty = true; });
    });
    requestAnimationFrame(loop);
  }
  function refresh() { items.forEach(function (it) { if (it.v.resize) it.v.resize(); it.dirty = true; }); }

  return { init: init, refresh: refresh };
})();
