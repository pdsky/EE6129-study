/* Reference examples for the animation API (not injected into any page: ids start with "demo:"). */

/* 1) loop mode: init returns a frame(t, dt) function; a slider changes a parameter. */
ANIM.reg('demo:loop', {
  title: '多普勒：手机越快，信道变得越快',
  cap: '蓝线是接收信号包络 |h(t)|。拖动速度滑块：速度越快，深衰落（红点）来得越密。',
  h: 200,
  init: function (A) {
    var ax = A.axes({ x: 40, y: 24, w: 330, h: 140, xr: [0, 1], yr: [0, 2.2], xl: 't', yl: '|h(t)|', ticksY: [{ v: 1, l: '1' }] });
    var curve = A.curve(ax, function () { return 0; }, 's-acc w2');
    var dots = A.g();
    var v = 30;
    var label = A.text(390, 18, '', { cls: 't-s t-m', anchor: 'end' });
    A.slider({ label: '速度 v', min: 5, max: 120, step: 5, value: v, unit: 'km/h', on: function (x) { v = x; A.redraw(); } });
    // fixed random scatterers, so the picture is repeatable
    var N = 12, ph = [], ang = [];
    for (var i = 0; i < N; i++) { ph.push(A.rand() * 2 * Math.PI); ang.push(A.rand() * 2 * Math.PI); }
    function env(t) {
      var fd = v / 6, re = 0, im = 0;
      for (var i = 0; i < N; i++) { var p = ph[i] + 2 * Math.PI * fd * Math.cos(ang[i]) * t; re += Math.cos(p); im += Math.sin(p); }
      return Math.sqrt(re * re + im * im) / Math.sqrt(N);
    }
    return function frame(t) {
      var pts = [];
      for (var k = 0; k <= 200; k++) { var x = k / 200; pts.push([x, Math.min(2.2, env(t * 0.25 + x))]); }
      A.setCurve(curve, ax, pts);
      while (dots.firstChild) dots.removeChild(dots.firstChild);
      for (var j = 1; j < pts.length - 1; j++) if (pts[j][1] < 0.25 && pts[j][1] <= pts[j - 1][1] && pts[j][1] <= pts[j + 1][1]) A.circle(ax.X(pts[j][0]), ax.Y(pts[j][1]), 3.2, 'f-bad', dots);
      A.set(label, { text: 'f_{D} = v/λ ≈ ' + Math.round(v / 6 * 10) / 10 + '（相对值）' });
    };
  }
});

/* 2) steps mode: def.steps = captions; init returns {step(k), frame(ts, dt, k)}; A.prog(ts) eases 0→1 within a step. */
ANIM.reg('demo:steps', {
  title: '长除法求迫零均衡器 C(z) = 1/H(z)',
  cap: '按“下一步”逐项看：每一步商写一项，再从余数里减掉。',
  h: 170,
  steps: [
    'H(z) = 1 + 0.3z^-1，目标：让 H(z)·C(z) = 1。',
    '第一项 c₀ = 1：1 − 1·H(z) = −0.3z^-1。',
    '第二项 c₁ = −0.3：余数变成 +0.09z^-2。',
    '规律：c_k = (−0.3)^k，C(z) = 1 − 0.3z^-1 + 0.09z^-2 − …'
  ],
  init: function (A) {
    var boxes = [];
    var vals = ['1', '−0.3', '+0.09', '−0.027'];
    for (var i = 0; i < 4; i++) {
      var g = A.g({ opacity: 0 });
      A.rect(30 + i * 88, 60, 74, 44, 'f-accs s-acc w1', g, 8);
      A.text(67 + i * 88, 88, vals[i], { cls: 't-l t-b t-m', anchor: 'middle' }, g);
      A.text(67 + i * 88, 124, 'c_{' + i + '}', { cls: 't-s', anchor: 'middle' }, g);
      boxes.push(g);
    }
    A.text(200, 34, 'C(z) 的系数', { cls: 't-b', anchor: 'middle' });
    var cur = 0;
    return {
      step: function (k) { cur = k; },
      frame: function (ts) {
        for (var i = 0; i < 4; i++) {
          var shown = cur === 3 ? 1 : (i < cur ? 1 : i === cur ? A.prog(ts, 0.6) : 0);
          if (cur === 0) shown = i === 0 ? A.prog(ts, 0.6) * 0.35 : 0;
          boxes[i].setAttribute('opacity', shown.toFixed(2));
        }
      }
    };
  }
});
