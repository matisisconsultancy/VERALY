/* ============================================================
   LegalMotion — campo de partículas (Canvas 2D), vanilla.
   Inspiración: visualizaciones de partículas en flujo (ref. gris).
   Traducción al concepto "Convergencia" de la firma: miles de puntos
   dispersos que fluyen y CONVERGEN hacia un núcleo con el scroll
   (información dispersa -> prácticas/vías que confluyen).

   - Sin líneas (densidad de puntos = forma), como el referente.
   - Estados paramétricos con morphing suave ligado al scroll.
   - Deriva ambiental lenta; reacción muy sutil al cursor.
   - prefers-reduced-motion: una composición estática.
   - Rendimiento: 1px, sin O(n^2), cap de DPR, pausa fuera de viewport,
     menos partículas en móvil.
   Uso: <canvas data-motion> dentro de un contenedor posicionado.
   ============================================================ */
(function () {
  'use strict';
  var TAU = Math.PI * 2;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;

  function rnd(seed) { // PRNG determinista (composición estable entre recargas)
    return function () { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; };
  }

  function LegalMotion(canvas, opts) {
    opts = opts || {};
    var ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;
    var host = canvas.parentElement || canvas;
    var mobile = window.matchMedia && window.matchMedia('(max-width:820px)').matches;

    var DIM = opts.dim || '217,246,239';     // crema (texto) en rgb
    var ACC = opts.accent || '137,245,229';  // menta
    var COUNT = opts.count || (mobile ? 900 : 2300);
    var FOCAL = opts.focal || { x: 0.80, y: 0.36 };   // núcleo de convergencia (estado A)
    var FOCAL_B = opts.focalB || { x: 0.60, y: 0.46 };

    var dpr = Math.min(window.devicePixelRatio || 1, 1.75);
    var W = 0, H = 0, S = 0;
    var pts = [];
    var mouse = { x: -1, y: -1, on: false };
    var progress = 0, target = 0;
    var raf = null, inView = true;

    function seed() {
      var r = rnd(20260402);
      pts = [];
      for (var i = 0; i < COUNT; i++) {
        var u = r();                     // posición a lo largo del flujo (0..1)
        var g = (r() + r() + r() - 1.5); // ~gaussiana [-1.5,1.5] para el ancho
        var tier = r();                  // profundidad (alpha/tamaño)
        pts.push({
          u: u, g: g,
          ph: r() * TAU, sp: 0.4 + r() * 0.9,
          sp2: u * TAU * 3.2 + r() * TAU,   // ángulo para el estado convergido
          rad: 0.03 + r() * r() * 0.20,     // radio en el nudo convergido
          acc: r() < 0.09,                  // ~9% en menta, el resto crema
          z: tier,
          t: tier < 0.5 ? 0 : (tier < 0.82 ? 1 : 2)  // nivel de alpha
        });
      }
    }

    // Estado A: nube ancha a la izquierda que se estrecha en un flujo hacia el núcleo.
    function stateA(p) {
      var x = (0.0 + (FOCAL.x - 0.0) * Math.pow(p.u, 0.78));
      var spread = Math.pow(1 - p.u, 1.25) * 0.46;
      var y = FOCAL.y + p.g * spread * 0.5;
      return { x: x, y: y };
    }
    // Estado B: convergencia — los puntos se recogen en un nudo en espiral.
    function stateB(p) {
      var rad = p.rad * (0.5 + 0.5 * p.u);
      var ang = p.sp2;
      return { x: FOCAL_B.x + Math.cos(ang) * rad, y: FOCAL_B.y + Math.sin(ang) * rad * (W / Math.max(1, H)) };
    }

    function resize() {
      var rect = host.getBoundingClientRect();
      W = Math.max(1, rect.width); H = Math.max(1, rect.height); S = Math.min(W, H);
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function render(time) {
      ctx.clearRect(0, 0, W, H);
      var tt = (time || 0) * 0.00016;
      var drift = reduce ? 0 : 1;
      // dibujar por niveles de alpha (3 fillStyle por color/nivel, barato)
      var ALPH = [0.14, 0.3, 0.55];
      var buckets = [[], [], [], [], [], []]; // 0-2 crema, 3-5 menta
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];
        var A = stateA(p), B = stateB(p);
        var nx = A.x + (B.x - A.x) * progress;
        var ny = A.y + (B.y - A.y) * progress;
        // deriva ambiental (flujo)
        nx += drift * 0.006 * Math.sin(tt * p.sp + p.ph);
        ny += drift * 0.006 * Math.cos(tt * p.sp * 0.8 + p.ph);
        var x = nx * W, y = ny * H;
        // reacción sutil al cursor
        if (mouse.on && !reduce) {
          var dx = x - mouse.x, dy = y - mouse.y, d2 = dx * dx + dy * dy, R = S * 0.26;
          if (d2 < R * R && d2 > 1) { var f = (1 - Math.sqrt(d2) / R) * 0.18; x += dx * f; y += dy * f; }
        }
        p._x = x; p._y = y;
        buckets[(p.acc ? 3 : 0) + p.t].push(p);
      }
      for (var b = 0; b < 6; b++) {
        var arr = buckets[b]; if (!arr.length) continue;
        var col = b < 3 ? DIM : ACC;
        ctx.fillStyle = 'rgba(' + col + ',' + ALPH[b % 3] + ')';
        for (var k = 0; k < arr.length; k++) {
          var q = arr[k], sz = q.z > 0.82 ? 1.5 : 1;
          ctx.fillRect(q._x, q._y, sz, sz);
        }
      }
      // núcleo menta (punto de convergencia), más visible al converger
      var cx = (FOCAL.x + (FOCAL_B.x - FOCAL.x) * progress) * W;
      var cy = (FOCAL.y + (FOCAL_B.y - FOCAL.y) * progress) * H;
      var gl = ctx.createRadialGradient(cx, cy, 0, cx, cy, S * 0.14);
      gl.addColorStop(0, 'rgba(' + ACC + ',' + (0.14 + 0.18 * progress) + ')');
      gl.addColorStop(1, 'rgba(' + ACC + ',0)');
      ctx.fillStyle = gl; ctx.beginPath(); ctx.arc(cx, cy, S * 0.14, 0, TAU); ctx.fill();
    }

    var scene = host.closest('.hero-scene') || host.closest('.hero-full') || host;
    var lastP = -1;
    function syncVar() {
      // Exponer el progreso a CSS (el contenido se desvanece al converger).
      if (Math.abs(progress - lastP) > 0.004) {
        lastP = progress;
        scene.style.setProperty('--p', progress.toFixed(3));
      }
    }
    function frame(time) {
      progress += (target - progress) * 0.06;
      render(time);
      syncVar();
      raf = inView ? requestAnimationFrame(frame) : null;
    }
    function onScroll() {
      var r = scene.getBoundingClientRect();
      var vh = window.innerHeight || H;
      // El morph se completa a lo largo del tramo "fijado" (sticky) de la escena.
      var range = Math.max(1, r.height - vh);
      target = Math.max(0, Math.min(1, -r.top / range));
    }
    function start() { if (!raf) raf = requestAnimationFrame(frame); }
    function stop() { if (raf) { cancelAnimationFrame(raf); raf = null; } }

    seed(); resize();
    if (reduce) {
      progress = 0.2; scene.style.setProperty('--p', '0'); render(0);
      window.addEventListener('resize', function () { resize(); render(0); });
      return;
    }
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { resize(); });
    window.addEventListener('pointermove', function (e) {
      var rect = canvas.getBoundingClientRect();
      var x = e.clientX - rect.left, y = e.clientY - rect.top, m = S * 0.3;
      mouse.on = x > -m && y > -m && x < rect.width + m && y < rect.height + m;
      mouse.x = x; mouse.y = y;
    }, { passive: true });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { inView = e.isIntersecting; if (inView) start(); else stop(); });
      }, { threshold: 0 }).observe(host);
    }
    start();
  }

  function init() {
    var list = document.querySelectorAll('canvas[data-motion]');
    for (var i = 0; i < list.length; i++) { if (list[i].__lm) continue; list[i].__lm = 1; new LegalMotion(list[i], {}); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
  window.LegalMotion = LegalMotion;
  // Re-escaneo para vistas que inyectan el DOM después de cargar (preview SPA).
  window.initLegalMotion = init;
})();
