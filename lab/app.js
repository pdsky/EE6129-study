/* EE6129 学习工坊 · 应用逻辑 */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var log10 = function (x) { return Math.log(x) / Math.LN10; };
  var num = function (id, d) { var e = $(id); if (!e) return d; var v = parseFloat(e.value); return isNaN(v) ? d : v; };
  function rows(list) {
    return list.map(function (r) {
      return '<div class="r"><span class="k">' + r[0] + '</span><span class="v num">' + r[1] + '</span></div>';
    }).join('');
  }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  /* ================= 导航 ================= */
  var SECTIONS = [];
  document.querySelectorAll('.section').forEach(function (s) { SECTIONS.push(s.id.replace('sec-', '')); });
  var navbtns = document.querySelectorAll('.navbtn');

  function show(id, noScroll) {
    document.querySelectorAll('.section').forEach(function (s) {
      s.classList.toggle('active', s.id === 'sec-' + id);
    });
    navbtns.forEach(function (b) { b.classList.toggle('active', b.dataset.target === id); });
    if (!noScroll) window.scrollTo({ top: 0, behavior: 'instant' });
    if (window.VIZ) window.VIZ.refresh();
    store('ee6129:last', id);
  }
  navbtns.forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.target); }); });

  /* 章节底部：上一节 / 下一节 + 掌握标记 */
  var LESSONS = SECTIONS.filter(function (s) { return ['overview', 'quiz', 'flashcards'].indexOf(s) < 0; });
  function titleOf(id) {
    var b = document.querySelector('.navbtn[data-target="' + id + '"]');
    return b ? b.querySelector('.lbl').textContent : id;
  }
  LESSONS.forEach(function (id, i) {
    var sec = $('sec-' + id); if (!sec) return;
    var foot = document.createElement('div');
    foot.className = 'secfoot';
    var doneKey = 'ee6129:done:' + id;
    var done = store(doneKey) === '1';
    foot.innerHTML =
      '<button class="btn ghost" ' + (i === 0 ? 'disabled' : '') + ' data-go="' + (LESSONS[i - 1] || '') + '">← ' + (i > 0 ? titleOf(LESSONS[i - 1]) : '') + '</button>' +
      '<button class="btn mark' + (done ? ' on' : '') + '" data-mark="' + doneKey + '">' + (done ? '✓ 已掌握' : '标记为已掌握') + '</button>' +
      '<button class="btn ghost" ' + (i === LESSONS.length - 1 ? 'disabled' : '') + ' data-go="' + (LESSONS[i + 1] || '') + '">' + (i < LESSONS.length - 1 ? titleOf(LESSONS[i + 1]) : '') + ' →</button>';
    sec.appendChild(foot);
    foot.querySelectorAll('[data-go]').forEach(function (b) {
      b.addEventListener('click', function () { if (b.dataset.go) show(b.dataset.go); });
    });
    var mk = foot.querySelector('[data-mark]');
    mk.addEventListener('click', function () {
      var on = mk.classList.toggle('on');
      store(doneKey, on ? '1' : '0');
      mk.textContent = on ? '✓ 已掌握' : '标记为已掌握';
      updateProgress();
    });
  });
  function updateProgress() {
    var n = LESSONS.filter(function (id) { return store('ee6129:done:' + id) === '1'; }).length;
    var bar = $('progFill'), txt = $('progTxt');
    if (bar) bar.style.width = (n / LESSONS.length * 100) + '%';
    if (txt) txt.textContent = n + ' / ' + LESSONS.length + ' 节已掌握';
    document.querySelectorAll('.tile[data-go]').forEach(function (t) {
      t.classList.toggle('done', store('ee6129:done:' + t.dataset.go) === '1');
    });
  }

  /* 总览磁贴 */
  document.querySelectorAll('.tile[data-go]').forEach(function (t) {
    t.addEventListener('click', function () { show(t.dataset.go); });
  });

  /* ================= A3 频谱效率 ================= */
  (function () {
    if (!$('sp_bc')) return;
    var mode = 'fdma';
    document.querySelectorAll('#sp_mode .seg').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('#sp_mode .seg').forEach(function (x) { x.classList.remove('active'); });
        b.classList.add('active'); mode = b.dataset.v;
        ['fdma', 'wtdma', 'ntdma'].forEach(function (m) {
          $('sp_fields_' + m).style.display = (m === mode ? 'grid' : 'none');
        });
        calc();
      });
    });
    function calc() {
      var etam = 1 / (num('sp_bc', 0.03) * num('sp_ac', 4) * num('sp_n', 7));
      var etaa, detail;
      if (mode === 'fdma') {
        etaa = num('sp_be', 30) * num('sp_nt', 395) / (num('sp_bw', 12.5) * 1000);
        detail = 'FDMA：η_a = B_e·N_t / B_w';
      } else if (mode === 'wtdma') {
        etaa = num('sp_ts', 5.35) * num('sp_mt', 6) / num('sp_tf', 40);
        detail = '宽带 TDMA：η_a = T_s·M_t / T_f';
      } else {
        etaa = (num('sp_ts2', 5.35) * num('sp_mt2', 6) / num('sp_tf2', 40)) *
          (num('sp_bu', 30) * num('sp_nu', 395) / (num('sp_bw2', 12.5) * 1000));
        detail = '窄带 TDMA：η_a = (T_s·M_t/T_f)·(B_u·N_u/B_w)';
      }
      $('sp_result').innerHTML = rows([
        ['调制效率 η_m', etam.toFixed(4) + ' ch/MHz/km²'],
        [detail, 'η_a = ' + etaa.toFixed(4)],
        ['总频谱效率 η = η_m·η_a', (etam * etaa).toFixed(4) + ' /MHz/km²']
      ]);
    }
    document.querySelectorAll('#calc-spectral input').forEach(function (i) { i.addEventListener('input', calc); });
    calc();
  })();

  /* ================= A4 路径损耗 ================= */
  (function () {
    if (!$('pl_model')) return;
    function calc() {
      var model = $('pl_model').value;
      var f = num('pl_f', 900), d = num('pl_d', 5), ht = num('pl_ht', 30), hr = num('pl_hr', 3);
      var L, warn = '';
      if (model === 'fs') {
        L = 32 + 20 * log10(f) + 20 * log10(d);
      } else {
        var Lu = 69.55 + 26.16 * log10(f) - 13.82 * log10(ht) + (44.9 - 6.55 * log10(ht)) * log10(d), A;
        if (model === 'hata_lgL') A = 8.29 * Math.pow(log10(1.54 * hr), 2) - 1.1;
        else if (model === 'hata_lgH') A = 3.2 * Math.pow(log10(11.75 * hr), 2) - 4.97;
        else A = (1.1 * log10(f) - 0.7) * hr - (1.56 * log10(f) - 0.8);
        Lu -= A;
        if (model === 'hata_sub') L = Lu - 2 * Math.pow(log10(f / 28), 2) - 5.4;
        else if (model === 'hata_open') L = Lu - 4.78 * Math.pow(log10(f), 2) + 18.33 * log10(f) - 40.94;
        else L = Lu;
        if (f < 150 || f > 1500) warn += '⚠ 频率超出有效范围 150–1500MHz。';
        if (ht < 30 || ht > 200) warn += '⚠ 基站高度超出 30–200m。';
        if (d < 1 || d > 20) warn += '⚠ 距离超出 1–20km。';
        if (hr < 1 || hr > 10) warn += '⚠ 终端高度超出 1–10m。';
      }
      var pr = num('pl_pt', 40) + num('pl_gt', 8.14) + num('pl_gr', 2.14) - L;
      $('pl_result').innerHTML = rows([['路径损耗 L', L.toFixed(2) + ' dB'], ['接收功率 P_R', pr.toFixed(2) + ' dBm']]);
      $('pl_warn').textContent = warn;
    }
    document.querySelectorAll('#calc-prop input, #calc-prop select').forEach(function (i) {
      i.addEventListener('input', calc); i.addEventListener('change', calc);
    });
    calc();
  })();

  /* ================= A5 簇尺寸与 SIR ================= */
  (function () {
    if (!$('g_n')) return;
    function calc() {
      var N = num('g_n', 7), n = num('g_pn', 4), Q = Math.sqrt(3 * N);
      var db = function (x) { return (10 * log10(x)).toFixed(2) + ' dB'; };
      $('g_result').innerHTML = rows([
        ['同频复用比 Q = √(3N)', Q.toFixed(3)],
        ['简化近似（6 干扰源等距 D）', db(Math.pow(Q, n) / 6)],
        ['最坏情况 · 一般式', db(1 / (2 * Math.pow(Q - 1, -n) + 2 * Math.pow(Q, -n) + 2 * Math.pow(Q + 1, -n)))],
        ['最坏情况 · 保守式', db(Math.pow(Q - 1, n) / 6)],
        ['3 扇区（120°）最坏情况', db(1 / (Math.pow(Q, -n) + Math.pow(Q + 0.7, -n)))],
        ['6 扇区（60°）最坏情况', db(Math.pow(Q + 0.7, n))]
      ]);
      var ok = false;
      for (var i = 0; i <= 6; i++) for (var j = 0; j <= 6; j++) if (i * i + i * j + j * j === N) ok = true;
      $('g_valid').textContent = ok ? '' : ('⚠ N=' + N + ' 不满足 N=i²+ij+j²，不是有效簇尺寸。');
    }
    document.querySelectorAll('#calc-geom input, #calc-geom select').forEach(function (i) {
      i.addEventListener('input', calc); i.addEventListener('change', calc);
    });
    calc();
  })();

  /* ================= A6 小区分裂 / 扇区 ================= */
  (function () {
    if (!$('cs_pt')) return;
    $('cs_k').addEventListener('change', function () {
      $('cs_kcustom_wrap').style.display = this.value === 'custom' ? 'flex' : 'none'; calcCS();
    });
    function getK() { var v = $('cs_k').value; return v === 'custom' ? num('cs_kcustom', 2) : parseFloat(v); }
    function calcCS() {
      var pt1 = num('cs_pt', 10), k = getK(), n = num('cs_n', 4);
      $('cs_result').innerHTML = rows([
        ['新发射功率 P_t2', (pt1 / Math.pow(k, n)).toFixed(4) + ' W'],
        ['需下降', (10 * n * log10(k)).toFixed(2) + ' dB'],
        ['单位面积小区数变化', '×' + (k * k).toFixed(2)]
      ]);
    }
    ['cs_pt', 'cs_kcustom', 'cs_n'].forEach(function (id) { $(id).addEventListener('input', calcCS); });
    var sectors = 1;
    document.querySelectorAll('#ct_sectors .seg').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('#ct_sectors .seg').forEach(function (x) { x.classList.remove('active'); });
        b.classList.add('active'); sectors = parseFloat(b.dataset.v); calcCT();
      });
    });
    function calcCT() {
      var m = num('ct_m', 57), per = m / sectors;
      var A = 0, gos = 0.01;
      var lo = 0, hi = per * 3;
      for (var it = 0; it < 60; it++) { var mid = (lo + hi) / 2; if (window.erlangB(Math.floor(per), mid) > 0.02) hi = mid; else lo = mid; }
      $('ct_result').innerHTML = rows([
        ['扇区数', sectors],
        ['每扇区信道数', per.toFixed(1)],
        ['每扇区话务量（GoS 2%）', lo.toFixed(1) + ' Er'],
        ['小区总话务量', (lo * sectors).toFixed(1) + ' Er']
      ]);
    }
    $('ct_m').addEventListener('input', calcCT);
    calcCS(); calcCT();
  })();

  /* ================= A7 Erlang ================= */
  (function () {
    if (!$('tr_m')) return;
    function calc() {
      var m = Math.round(num('tr_m', 20)), A = num('tr_a', 13), h = num('tr_h', 100), au = num('tr_au', 0.25);
      if (m < 1 || A <= 0) { $('tr_result').innerHTML = ''; return; }
      var pb = window.erlangB(m, A), pc = window.erlangC(m, A);
      var list = [
        ['Erlang B · 呼损概率 P_B', (pb * 100).toFixed(3) + ' %'],
        ['承载话务 C = A(1−P_B)', (A * (1 - pb)).toFixed(3) + ' Erlang'],
        ['干线效率 C/M', ((A * (1 - pb) / m) * 100).toFixed(1) + ' %']
      ];
      if (A < m) {
        list.push(['Erlang C · 延迟概率', (pc * 100).toFixed(3) + ' %']);
        list.push(['平均等待时间 W', (pc * h / (m - A)).toFixed(3) + ' 秒']);
        list.push(['队列平均等待呼叫数', (pc * A / (m - A)).toFixed(3)]);
      } else list.push(['Erlang C', 'A ≥ M，队列不稳定']);
      if (au > 0) {
        list.push(['支持用户数 A/A_u', (A / au).toFixed(1)]);
        list.push(['干线增益 = 用户数/M', (A / au / m).toFixed(2)]);
      }
      $('tr_result').innerHTML = rows(list);
    }
    ['tr_m', 'tr_a', 'tr_h', 'tr_au'].forEach(function (id) { $(id).addEventListener('input', calc); });
    calc();
    $('tr_findA').addEventListener('click', function () {
      var m = Math.round(num('tr_m', 20)), gos = num('tr_gos', 0.02), lo = 0, hi = Math.max(m * 3, 50);
      for (var i = 0; i < 60; i++) { var mid = (lo + hi) / 2; if (window.erlangB(m, mid) > gos) hi = mid; else lo = mid; }
      $('tr_inv_result').innerHTML = rows([['M=' + m + '，GoS≤' + gos + ' 的最大话务量', lo.toFixed(2) + ' Erlang']]);
    });
    $('tr_findM').addEventListener('click', function () {
      var A = num('tr_a', 13), gos = num('tr_gos', 0.02), m = Math.max(1, Math.floor(A));
      while (window.erlangB(m, A) > gos && m < 5000) m++;
      $('tr_inv_result').innerHTML = rows([['A=' + A + ' Erlang，GoS≤' + gos + ' 的最少信道数', m]]);
    });
  })();

  /* ================= B1 CSMA/CA 开销计算 ================= */
  (function () {
    if (!$('cw_k')) return;
    function calc() {
      var k = Math.round(num('cw_k', 0)), phy = $('cw_phy').value;
      var slot = phy === 'b' ? 20 : 9, sifs = phy === 'b' ? 10 : 16;
      var difs = sifs + 2 * slot;
      var CW = Math.min(32 * Math.pow(2, k), 256);
      var avgSlots = (CW - 1) / 2, avgBo = avgSlots * slot;
      var rate = num('cw_rate', 54), pay = num('cw_pay', 1500);
      var pre = phy === 'b' ? 192 : 20;                       // 前导+PLCP 头（µs）
      var ctrlRate = phy === 'b' ? 1 : 6;                     // 控制帧速率 Mbps
      var tFrame = function (bytes, r) { return pre + bytes * 8 / r; };
      var tRTS = tFrame(20, ctrlRate), tCTS = tFrame(14, ctrlRate), tACK = tFrame(14, ctrlRate);
      var tDATA = tFrame(pay + 34, rate);
      var total = difs + avgBo + tRTS + sifs + tCTS + sifs + tDATA + sifs + tACK;
      var payTime = pay * 8 / rate;
      $('cw_result').innerHTML = rows([
        ['时隙 / SIFS / DIFS', slot + ' / ' + sifs + ' / ' + difs + ' µs'],
        ['第 ' + (k + 1) + ' 次尝试的竞争窗口 CW', CW + '（0～' + (CW - 1) + ' 个时隙）'],
        ['平均退避时隙数', avgSlots.toFixed(1)],
        ['平均退避时间', avgBo.toFixed(1) + ' µs'],
        ['一次 RTS/CTS 完整交互耗时', total.toFixed(1) + ' µs'],
        ['其中纯数据载荷时间', payTime.toFixed(1) + ' µs'],
        ['MAC 效率（载荷/总时长）', (payTime / total * 100).toFixed(1) + ' %'],
        ['有效吞吐量', (pay * 8 / total).toFixed(2) + ' Mbps']
      ]);
    }
    ['cw_k', 'cw_rate', 'cw_pay'].forEach(function (id) { $(id).addEventListener('input', calc); });
    $('cw_phy').addEventListener('change', calc);
    calc();
  })();

  /* ================= B3 LTE 吞吐量 ================= */
  (function () {
    if (!$('lte_bw')) return;
    function calc() {
      var rb = parseInt($('lte_bw').value, 10);
      var bits = parseInt($('lte_mod').value, 10);
      var rate = num('lte_rate', 0.92), layers = parseInt($('lte_mimo').value, 10);
      var re = rb * 12 * 14;                    // 每 1ms 子帧的资源单元
      var raw = re * bits * rate * layers * 1000 / 1e6;
      var net = raw * 0.75;                     // 扣除参考信号/控制信道等开销的粗略估计
      $('lte_result').innerHTML = rows([
        ['资源块数 N_RB', rb],
        ['子载波总数', rb * 12],
        ['每 1ms 子帧资源单元 RE', re.toLocaleString()],
        ['理论峰值速率', raw.toFixed(1) + ' Mbps'],
        ['扣除约 25% 开销后估计', net.toFixed(1) + ' Mbps']
      ]);
    }
    ['lte_bw', 'lte_mod', 'lte_mimo'].forEach(function (id) { $(id).addEventListener('change', calc); });
    $('lte_rate').addEventListener('input', calc);
    calc();
  })();

  /* ================= C2 卫星几何与链路 ================= */
  (function () {
    if (!$('sat_h')) return;
    var RE = 6378, MU = 398600.4418, Cs = 299792.458;
    function calc() {
      var h = num('sat_h', 35863), th = num('sat_el', 10), f = num('sat_f', 6);
      var a = RE + h, thr = th * Math.PI / 180;
      var psi = Math.asin(Math.min(1, RE * Math.cos(thr) / a));
      var gam = Math.PI / 2 - thr - psi;
      var d = a * Math.sin(gam) / Math.cos(thr);
      var cap = 2 * Math.PI * RE * RE * (1 - Math.cos(gam));
      var frac = (1 - Math.cos(gam)) / 2;
      var T = 2 * Math.PI * Math.sqrt(Math.pow(a, 3) / MU);
      var v = Math.sqrt(MU / a);
      var fsl = 92.45 + 20 * log10(f) + 20 * log10(d);
      $('sat_result').innerHTML = rows([
        ['星下点角（nadir）ψ', (psi * 180 / Math.PI).toFixed(2) + ' °'],
        ['中心角 γ', (gam * 180 / Math.PI).toFixed(2) + ' °'],
        ['斜距 d', d.toFixed(0) + ' km'],
        ['单程传播时延 d/c', (d / Cs * 1000).toFixed(2) + ' ms'],
        ['地面→星→地面 时延', (2 * d / Cs * 1000).toFixed(1) + ' ms'],
        ['覆盖面积', (cap / 1e6).toFixed(2) + ' × 10⁶ km²'],
        ['占地球表面比例', (frac * 100).toFixed(1) + ' %'],
        ['全球覆盖所需卫星数（粗估）', Math.ceil(1 / frac)],
        ['轨道周期 T', (T / 3600).toFixed(2) + ' h（' + (T / 60).toFixed(0) + ' min）'],
        ['轨道速度 v', v.toFixed(2) + ' km/s'],
        ['自由空间损耗 @' + f + 'GHz', fsl.toFixed(1) + ' dB']
      ]);
      var note = '';
      if (Math.abs(h - 35863) < 400) note = '≈ GEO 静止轨道：周期与地球自转一致（23.93h），卫星相对地面静止。';
      else if (h >= 8000 && h <= 18000) note = '≈ MEO 中轨：GPS 等导航星座所在区间，切换远少于 LEO。';
      else if (h >= 500 && h <= 1500) note = '≈ LEO 低轨：信号强、时延小，但过顶时间仅几分钟，需要大星座与频繁切换。';
      $('sat_note').textContent = note;
    }
    ['sat_h', 'sat_el', 'sat_f'].forEach(function (id) { $(id).addEventListener('input', calc); });
    document.querySelectorAll('#sat_presets .seg').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('#sat_presets .seg').forEach(function (x) { x.classList.remove('active'); });
        b.classList.add('active');
        $('sat_h').value = b.dataset.h; calc();
        if (window.VIZ) window.VIZ.refresh();
      });
    });
    calc();
  })();

  /* ================= 自测题 ================= */
  (function () {
    var area = $('quizArea'); if (!area) return;
    var filter = 'ALL', order = [], idx = 0, score = 0, wrong = [], answered = false;
    function build() {
      order = [];
      window.QUIZ.forEach(function (q, i) { if (filter === 'ALL' || q[4] === filter) order.push(i); });
      idx = 0; score = 0; wrong = []; render();
    }
    document.querySelectorAll('#quizFilter .seg').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('#quizFilter .seg').forEach(function (x) { x.classList.remove('active'); });
        b.classList.add('active'); filter = b.dataset.v; build();
      });
    });
    $('quizShuffle').addEventListener('click', function () {
      for (var i = order.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = order[i]; order[i] = order[j]; order[j] = t; }
      idx = 0; score = 0; wrong = []; render();
    });
    function render() {
      if (idx >= order.length) return result();
      var q = window.QUIZ[order[idx]];
      answered = false;
      var tag = { A: '蜂窝通信', B: '无线系统', C: '卫星通信' }[q[4]];
      var html = '<div class="quizhead"><span class="scorepill">' + (idx + 1) + ' / ' + order.length + '</span>' +
        '<div class="progressbar"><div style="width:' + (idx / order.length * 100) + '%"></div></div>' +
        '<span class="scorepill">得分 ' + score + '</span></div>' +
        '<div class="qcard"><div class="qn">Part ' + q[4] + ' · ' + tag + '</div>' +
        '<div class="qtext">' + q[0] + '</div><div id="qopts">' +
        q[1].map(function (o, i) { return '<button class="opt" data-i="' + i + '">' + String.fromCharCode(65 + i) + '. ' + o + '</button>'; }).join('') +
        '</div><div class="explain" id="qexplain"></div>' +
        '<div class="quizfoot"><button class="btn" id="qnext" disabled>下一题 →</button></div></div>';
      area.innerHTML = html;
      area.querySelectorAll('#qopts .opt').forEach(function (b) {
        b.addEventListener('click', function () {
          if (answered) return; answered = true;
          var ch = parseInt(b.dataset.i, 10), ok = q[2];
          area.querySelectorAll('#qopts .opt').forEach(function (x) {
            x.setAttribute('disabled', '');
            var xi = parseInt(x.dataset.i, 10);
            if (xi === ok) x.classList.add('correct');
            else if (xi === ch) x.classList.add('incorrect');
          });
          if (ch === ok) score++; else wrong.push(order[idx]);
          var ex = $('qexplain');
          ex.innerHTML = '<b>' + (ch === ok ? '✓ 正确。' : '✗ 正确答案：' + String.fromCharCode(65 + ok) + '。') + '</b> ' + q[3];
          ex.classList.add('show');
          $('qnext').removeAttribute('disabled');
        });
      });
      $('qnext').addEventListener('click', function () { idx++; render(); });
    }
    function result() {
      var pct = Math.round(score / order.length * 100);
      var html = '<div class="qcard quizresult"><div class="eyebrow">测验完成</div>' +
        '<div class="big">' + score + ' / ' + order.length + '</div>' +
        '<p style="color:var(--text-muted)">正确率 ' + pct + '%</p>';
      if (wrong.length) {
        html += '<div class="wronglist"><h4>需要复习的题目</h4>' + wrong.map(function (i) {
          var q = window.QUIZ[i];
          return '<div class="wrongitem"><b>[Part ' + q[4] + ']</b> ' + q[0] + '<br><span>' + q[3] + '</span></div>';
        }).join('') + '</div>';
      }
      html += '<div class="quizfoot" style="justify-content:center"><button class="btn" id="qretry">重新作答</button>' +
        (wrong.length ? '<button class="btn ghost" id="qonlywrong">只重做错题</button>' : '') + '</div></div>';
      area.innerHTML = html;
      $('qretry').addEventListener('click', build);
      if ($('qonlywrong')) $('qonlywrong').addEventListener('click', function () {
        order = wrong.slice(); idx = 0; score = 0; wrong = []; render();
      });
    }
    build();
  })();

  /* ================= 记忆卡片 ================= */
  (function () {
    var cardEl = $('fcCard'); if (!cardEl) return;
    var filter = 'ALL', order = [], pos = 0;
    function build() {
      order = [];
      window.CARDS.forEach(function (c, i) { if (filter === 'ALL' || c[2] === filter) order.push(i); });
      pos = 0; render();
    }
    document.querySelectorAll('#fcFilter .seg').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('#fcFilter .seg').forEach(function (x) { x.classList.remove('active'); });
        b.classList.add('active'); filter = b.dataset.v; build();
      });
    });
    function render() {
      cardEl.classList.remove('flipped');
      var c = window.CARDS[order[pos]];
      $('fc_term').textContent = c[0];
      $('fc_def').innerHTML = c[1];
      $('fc_tag').textContent = 'Part ' + c[2];
      $('fc_progress').textContent = (pos + 1) + ' / ' + order.length;
    }
    cardEl.addEventListener('click', function () { cardEl.classList.toggle('flipped'); });
    $('fc_next').addEventListener('click', function () { pos = (pos + 1) % order.length; render(); });
    $('fc_prev').addEventListener('click', function () { pos = (pos - 1 + order.length) % order.length; render(); });
    $('fc_shuffle').addEventListener('click', function () {
      for (var i = order.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = order[i]; order[i] = order[j]; order[j] = t; }
      pos = 0; render();
    });
    document.addEventListener('keydown', function (e) {
      if (!$('sec-flashcards').classList.contains('active')) return;
      if (e.key === 'ArrowRight') $('fc_next').click();
      else if (e.key === 'ArrowLeft') $('fc_prev').click();
      else if (e.key === ' ') { e.preventDefault(); cardEl.click(); }
    });
    build();
  })();

  /* ================= 启动 ================= */
  updateProgress();
  var last = store('ee6129:last');
  show(last && SECTIONS.indexOf(last) >= 0 ? last : 'overview', true);
  if (window.VIZ) window.VIZ.init();
})();
