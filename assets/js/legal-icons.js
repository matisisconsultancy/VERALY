/* ============================================================
   LegalIcons — iconos que se ENSAMBLAN a partir de puntos que
   convergen (Canvas 2D, vanilla). Hermano pequeño de LegalMotion.
   Concepto de marca: el isotipo es una estrella de trazos que
   convergen a un punto (un equipo que se une). Aquí cada icono se
   forma igual: un enjambre de puntos converge hasta dibujar la figura.

   - La silueta se obtiene rasterizando las mismas formas sólidas del
     icono y muestreando sus píxeles (nube de puntos = figura).
   - Al entrar en viewport, los puntos convergen (progreso 0→1).
   - Deriva mínima una vez formado; realce muy sutil al pasar el cursor.
   - prefers-reduced-motion: no corre (se muestra el SVG sólido estático).
   ============================================================ */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var MENTA = '137,245,229';   // acento
  var CREMA = '217,246,239';   // texto (una fracción, para textura)

  // Definición de cada icono en el espacio del viewBox 96×96 (mismas formas
  // que los SVG sólidos de build.py). 'd' = path; 'rect' = [x,y,w,h,r].
  var ICONS = {
    recuperacion: [
      { d: 'M48 19 L74 45 L65 54 L48 37 L31 54 L22 45 Z' },
      { rect: [25, 59, 46, 15, 5] }
    ],
    defensa: [
      { d: 'M45.5 15 L23 24 V47 C23 63 34 72.5 45.5 78 Z' },
      { d: 'M50.5 15 L73 24 V47 C73 63 62 72.5 50.5 78 Z' }
    ],
    recaudo: [
      { d: 'M34 16 H62 L48 39 Z' },
      { d: 'M34 80 H62 L48 57 Z' },
      { d: 'M16 34 V62 L39 48 Z' },
      { d: 'M80 34 V62 L57 48 Z' }
    ],
    // ---- Las tres vías ----
    'via-admin': [   // pórtico / institución (Superintendencia)
      { d: 'M14 33 L48 15 L82 33 Z' },
      { rect: [17, 35, 62, 8, 2] },
      { rect: [20, 46, 8, 28, 2] }, { rect: [33, 46, 8, 28, 2] },
      { rect: [47, 46, 8, 28, 2] }, { rect: [60, 46, 8, 28, 2] },
      { rect: [14, 76, 68, 8, 2] }
    ],
    'via-penal': [   // libro abierto = código
      { d: 'M48 30 L22 24 V60 L48 66 Z' },
      { d: 'M48 30 L74 24 V60 L48 66 Z' }
    ],
    'via-civil': [   // monedas apiladas = patrimonio
      { rect: [28, 26, 44, 12, 6] },
      { rect: [24, 41, 44, 12, 6] },
      { rect: [29, 56, 44, 12, 6] }
    ],
    // ---- El método, paso a paso ----
    'metodo-verificar': [   // visto bueno = verificación
      { d: 'M40 73 L19 52 L28 43 L40 55 L71 24 L80 33 Z' }
    ],
    'metodo-hechos': [      // documento (marco de página + líneas de texto)
      { rect: [27, 14, 42, 4, 2] }, { rect: [27, 76, 42, 4, 2] },
      { rect: [27, 14, 4, 66, 2] }, { rect: [65, 14, 4, 66, 2] },
      { rect: [37, 32, 22, 3.4, 1.7] }, { rect: [37, 42, 22, 3.4, 1.7] },
      { rect: [37, 52, 22, 3.4, 1.7] }, { rect: [37, 62, 13, 3.4, 1.7] }
    ],
    'metodo-actores': [     // tres personas = actores
      { d: 'M48 20 a10 10 0 1 0 0.1 0 Z' },
      { d: 'M30 72 C30 56 66 56 66 72 L66 78 L30 78 Z' },
      { d: 'M21 34 a7 7 0 1 0 0.1 0 Z' },
      { d: 'M9 70 C9 58 33 58 33 70 L33 78 L9 78 Z' },
      { d: 'M75 34 a7 7 0 1 0 0.1 0 Z' },
      { d: 'M63 70 C63 58 87 58 87 70 L87 78 L63 78 Z' }
    ],
    'metodo-rutas': [       // tres flechas = tres vías/rutas
      { rect: [16, 24, 34, 6, 3] }, { d: 'M50 18 L68 27 L50 36 Z' },
      { rect: [16, 45, 34, 6, 3] }, { d: 'M50 39 L68 48 L50 57 Z' },
      { rect: [16, 66, 34, 6, 3] }, { d: 'M50 60 L68 69 L50 78 Z' }
    ]
    // 'metodo-convergencia' se genera abajo (estrella del isotipo).
  };

  // Estrella de convergencia (isotipo): cinco radios que convergen a un punto.
  (function () {
    var cx = 48, cy = 48, spk = [];
    for (var k = 0; k < 5; k++) {
      var a = -Math.PI / 2 + k * 2 * Math.PI / 5;
      var nx = Math.cos(a), ny = Math.sin(a), px = -ny, py = nx;
      var r0 = 12, r1 = 42, w = 3.6;
      var ax = cx + nx * r0, ay = cy + ny * r0, bx = cx + nx * r1, by = cy + ny * r1;
      spk.push({ d: 'M' + (ax + px * w) + ' ' + (ay + py * w) + ' L' + (bx + px * w) + ' ' + (by + py * w)
        + ' L' + (bx - px * w) + ' ' + (by - py * w) + ' L' + (ax - px * w) + ' ' + (ay - py * w) + ' Z' });
    }
    spk.push({ rect: [cx - 8, cy - 8, 16, 16, 8] });
    ICONS['metodo-convergencia'] = spk;
  })();

  function rnd(seed) {
    return function () { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; };
  }

  function roundRectPath(p, x, y, w, h, r) {
    p.moveTo(x + r, y);
    p.arcTo(x + w, y, x + w, y + h, r);
    p.arcTo(x + w, y + h, x, y + h, r);
    p.arcTo(x, y + h, x, y, r);
    p.arcTo(x, y, x + w, y, r);
    p.closeType = 1;
  }

  // Muestrea la silueta del icono en una rejilla y devuelve targets normalizados.
  function sampleTargets(shapes) {
    var G = 96;
    var off = document.createElement('canvas');
    off.width = G; off.height = G;
    var c = off.getContext('2d');
    c.fillStyle = '#fff';
    shapes.forEach(function (s) {
      var p = new Path2D();
      if (s.rect) {
        var r = s.rect;
        // rect redondeado
        var x = r[0], y = r[1], w = r[2], h = r[3], rr = r[4];
        p.moveTo(x + rr, y);
        p.arcTo(x + w, y, x + w, y + h, rr);
        p.arcTo(x + w, y + h, x, y + h, rr);
        p.arcTo(x, y + h, x, y, rr);
        p.arcTo(x, y, x + w, y, rr);
        p.closePath();
      } else {
        p = new Path2D(s.d);
      }
      c.fill(p);
    });
    var data = c.getImageData(0, 0, G, G).data;
    var pts = [];
    var step = 1.7;
    for (var y = 0; y < G; y += step) {
      for (var x = 0; x < G; x += step) {
        var ix = (Math.floor(y) * G + Math.floor(x)) * 4;
        if (data[ix + 3] > 130) {
          pts.push([x / G, y / G]);
        }
      }
    }
    return pts;
  }

  function IconField(canvas) {
    var ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;
    var name = canvas.getAttribute('data-icon');
    var shapes = ICONS[name];
    if (!shapes) return;

    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var W = 0, H = 0, S = 0, OX = 0, OY = 0;
    var MAX = +canvas.getAttribute('data-max') || 560;
    var DOT = +canvas.getAttribute('data-dot') || 1;   // escala del tamaño de punto
    var FIT = +canvas.getAttribute('data-fit') || 1;   // fracción del lado menor que ocupa la figura
    var targets = sampleTargets(shapes);
    var r = rnd(90210 + name.length * 7);
    // submuestreo para acotar el número de puntos
    if (targets.length > MAX) {
      for (var i = targets.length - 1; i > 0; i--) { var j = (r() * (i + 1)) | 0; var t = targets[i]; targets[i] = targets[j]; targets[j] = t; }
      targets = targets.slice(0, MAX);
    }
    var pts = targets.map(function (tg) {
      var ang = r() * Math.PI * 2, rad = 0.45 + r() * 0.55;   // origen disperso alrededor
      return {
        tx: tg[0], ty: tg[1],
        sx: tg[0] + Math.cos(ang) * rad, sy: tg[1] + Math.sin(ang) * rad,
        ph: r() * Math.PI * 2, sp: 0.6 + r() * 0.9,
        dl: r() * 0.28,                    // retardo individual (ensamblado orgánico)
        acc: r() < 0.14,                   // fracción en crema
        sz: (r() < 0.3 ? 1.6 : 1.2) * DOT
      };
    });

    var progress = 0, target = 0, hover = 0, hoverT = 0;
    var raf = null, inView = true;

    function resize() {
      var rect = canvas.getBoundingClientRect();
      W = Math.max(1, rect.width); H = Math.max(1, rect.height);
      S = Math.min(W, H) * FIT; OX = (W - S) / 2; OY = (H - S) / 2;  // cuadra la figura (respeta aspecto)
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function ease(t) { return t < 0 ? 0 : t > 1 ? 1 : t * t * (3 - 2 * t); }

    function render(time) {
      ctx.clearRect(0, 0, W, H);
      var tt = (time || 0) * 0.001;
      var mC = [], cC = [];
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];
        var pp = ease((progress - p.dl) / (1 - p.dl));       // progreso con retardo
        var x = p.sx + (p.tx - p.sx) * pp;
        var y = p.sy + (p.ty - p.sy) * pp;
        // deriva mínima sólo cuando está formado
        var amp = (0.004 + hover * 0.01) * pp;
        x += amp * Math.sin(tt * p.sp + p.ph);
        y += amp * Math.cos(tt * p.sp * 0.9 + p.ph);
        var px = OX + x * S, py = OY + y * S;
        (p.acc ? cC : mC).push(px, py, p.sz);
      }
      drawBatch(mC, MENTA); drawBatch(cC, CREMA);
    }
    function drawBatch(arr, col) {
      if (!arr.length) return;
      ctx.fillStyle = 'rgba(' + col + ',0.92)';
      for (var i = 0; i < arr.length; i += 3) ctx.fillRect(arr[i], arr[i + 1], arr[i + 2], arr[i + 2]);
    }

    function frame(time) {
      progress += (target - progress) * 0.055;
      hover += (hoverT - hover) * 0.08;
      render(time);
      // deja de pintar cuando ya está totalmente disperso (ahorra CPU)
      var settled = (target === 0 && progress < 0.004);
      raf = (inView && !settled) ? requestAnimationFrame(frame) : null;
    }
    function start() { if (!raf) raf = requestAnimationFrame(frame); }
    function stop() { if (raf) { cancelAnimationFrame(raf); raf = null; } }

    resize();
    window.addEventListener('resize', function () { resize(); });

    if (reduce) { progress = 1; target = 1; render(0); return; }

    var step = canvas.closest('.step');
    if (step) {
      // En el stepper: converge cuando el paso se activa; se re-dispersa después.
      var section = canvas.closest('.stepper') || step;
      var sectionIn = false, stepIn = false;
      function recompute() {
        var staticVisible = (getComputedStyle(step).position !== 'absolute');
        target = (step.classList.contains('active') || (staticVisible && stepIn)) ? 1 : 0;
      }
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (es) {
          es.forEach(function (e) { sectionIn = e.isIntersecting; inView = sectionIn; if (inView) { recompute(); start(); } else stop(); });
        }, { threshold: 0 }).observe(section);
        new IntersectionObserver(function (es) {
          es.forEach(function (e) { stepIn = e.isIntersecting; recompute(); if (inView) start(); });
        }, { threshold: 0.3 }).observe(step);
      } else { inView = true; target = 1; }
      new MutationObserver(function () { recompute(); if (inView) start(); })
        .observe(step, { attributes: true, attributeFilter: ['class'] });
      window.addEventListener('resize', recompute);
      recompute(); start();
      return;
    }

    var card = canvas.closest('.fcard') || canvas;
    if (canvas.closest('.fcard')) {
      card.addEventListener('pointerenter', function () { hoverT = 1; });
      card.addEventListener('pointerleave', function () { hoverT = 0; });
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) { target = 1; inView = true; start(); }
          else { inView = false; stop(); }
        });
      }, { threshold: 0.25, rootMargin: '0px 0px -8% 0px' }).observe(card);
    } else { target = 1; }
    start();
  }

  function init() {
    var list = document.querySelectorAll('canvas[data-icon]');
    for (var i = 0; i < list.length; i++) { if (list[i].__li) continue; list[i].__li = 1; IconField(list[i]); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
  window.initLegalIcons = init;
})();
