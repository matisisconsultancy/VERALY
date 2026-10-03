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
    ]
  };

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
    var step = 2.05;
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
    var W = 0, H = 0;
    var targets = sampleTargets(shapes);
    var r = rnd(90210 + name.length * 7);
    // submuestreo para acotar el número de puntos
    var MAX = 560;
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
        sz: r() < 0.3 ? 1.6 : 1.2
      };
    });

    var progress = 0, target = 0, hover = 0, hoverT = 0;
    var raf = null, inView = true;

    function resize() {
      var rect = canvas.getBoundingClientRect();
      W = Math.max(1, rect.width); H = Math.max(1, rect.height);
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
        var px = x * W, py = y * H;
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
      raf = inView ? requestAnimationFrame(frame) : null;
    }
    function start() { if (!raf) raf = requestAnimationFrame(frame); }
    function stop() { if (raf) { cancelAnimationFrame(raf); raf = null; } }

    resize();
    window.addEventListener('resize', function () { resize(); });

    if (reduce) { progress = 1; target = 1; render(0); return; }

    var card = canvas.closest('.fcard') || canvas;
    card.addEventListener('pointerenter', function () { hoverT = 1; });
    card.addEventListener('pointerleave', function () { hoverT = 0; });

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
    var list = document.querySelectorAll('canvas.fic-canvas[data-icon]');
    for (var i = 0; i < list.length; i++) { if (list[i].__li) continue; list[i].__li = 1; IconField(list[i]); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
  window.initLegalIcons = init;
})();
