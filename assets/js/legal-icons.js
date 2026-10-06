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
    recuperacion: [   // moneda sólida con flecha al alza (hueco) = recuperar dinero
      { rule: 'evenodd', d: 'M21 48 a27 27 0 1 0 54 0 a27 27 0 1 0 -54 0'
        + 'M48 31 L63 47 L55 47 L55 65 L41 65 L41 47 L33 47 Z' }
    ],
    defensa: [        // escudo sólido con visto (hueco) = defensa
      { rule: 'evenodd', d: 'M48 14 L76 25 V47 C76 65 63 75 48 81 C33 75 20 65 20 47 V25 Z'
        + 'M44 61 L30 47 L36 41 L44 49 L62 31 L68 37 Z' }
    ],
    recaudo: [        // edificio sólido con ventanas y puerta (huecos) = la empresa
      { d: 'M26 36 L48 21 L70 36 Z' },
      { rule: 'evenodd', d: 'M31 36 H65 V80 H31 Z'
        + 'M37 43 H45 V52 H37 Z' + 'M51 43 H59 V52 H51 Z'
        + 'M37 57 H45 V66 H37 Z' + 'M51 57 H59 V66 H51 Z'
        + 'M43 80 V68 H53 V80 Z' }
    ],
    // ---- Las tres vías ----
    'via-admin': [   // pórtico / institución (Superintendencia)
      { d: 'M14 33 L48 15 L82 33 Z' },
      { rect: [17, 35, 62, 8, 2] },
      { rect: [20, 46, 8, 28, 2] }, { rect: [33, 46, 8, 28, 2] },
      { rect: [47, 46, 8, 28, 2] }, { rect: [60, 46, 8, 28, 2] },
      { rect: [14, 76, 68, 8, 2] }
    ],
    'via-penal': [   // libro (código) con lomo y líneas de página (huecos)
      { d: 'M22 24 H30 V72 H22 Z' },
      { rule: 'evenodd', d: 'M30 24 H72 V72 H30 Z'
        + 'M38 33 H64 V36 H38 Z' + 'M38 42 H64 V45 H38 Z'
        + 'M38 51 H64 V54 H38 Z' + 'M38 60 H56 V63 H38 Z' }
    ],
    'via-civil': [   // casa + candado = patrimonio protegido (responsabilidad patrimonial)
      { d: 'M20 50 L48 25 L76 50', stroke: 4.5 },          // techo
      { d: 'M28 50 V82 H68 V50', stroke: 4.5 },            // cuerpo de la casa (contorno)
      { d: 'M42 61 V56 a6 6 0 0 1 12 0 V61', stroke: 3.6 },// arco del candado
      { rule: 'evenodd',
        d: 'M39 61 H57 Q59 61 59 63 V75 Q59 77 57 77 H39 Q37 77 37 75 V63 Q37 61 39 61 Z'
          + 'M48 65 a2.6 2.6 0 1 0 0.1 0 Z' + 'M47 68 H49 V74 H47 Z' }  // candado + ojo de cerradura (huecos)
    ],
    // ---- El método, paso a paso ----
    'metodo-verificar': [   // visto bueno en círculo = verificación
      { d: 'M20 48 a28 28 0 1 0 56 0 a28 28 0 1 0 -56 0', stroke: 4 },
      { d: 'M35 49 L45 59 L63 37', stroke: 5 }
    ],
    'metodo-hechos': [      // documento con esquina doblada + líneas
      { d: 'M30 14 H58 L68 24 V82 H30 Z', stroke: 4 },
      { d: 'M58 14 V24 H68', stroke: 3.4 },
      { d: 'M38 37 H60', stroke: 3 }, { d: 'M38 47 H60', stroke: 3 },
      { d: 'M38 57 H60', stroke: 3 }, { d: 'M38 67 H52', stroke: 3 }
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

  // Isotipo real de Veraly: cinco galones (V) que convergen a un punto central.
  // Geometría del LOGO_SVG (viewBox -140..140) mapeada al espacio 0..96.
  (function () {
    var S = 0.3, O = 48;  // escala y traslación (x' = 48 + x*0.3)
    function m(x, y) { return (O + x * S).toFixed(1) + ' ' + (O + y * S).toFixed(1); }
    var arms = [
      [-29.2, -120.8, 0, -39.6, 39.6, -72.0],
      [105.6, -64.8, 37.6, -12.0, 80.4, 15.6],
      [94.4, 80.4, 23.2, 32.0, 10.0, 81.2],
      [-47.2, 114.8, -23.2, 32.0, -74.0, 34.8],
      [-124.0, -9.6, -37.6, -12.0, -56.0, -59.6]
    ];
    var shp = arms.map(function (a) {
      return { d: 'M' + m(a[0], a[1]) + ' L' + m(a[2], a[3]) + ' L' + m(a[4], a[5]), stroke: 30 * S };
    });
    shp.push({ d: 'M' + (O - 4.8) + ' ' + O + ' a4.8 4.8 0 1 0 9.6 0 a4.8 4.8 0 1 0 -9.6 0' }); // punto central
    ICONS['metodo-convergencia'] = shp;
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

  // Contexto de prueba COMPARTIDO (1×1), solo para pruebas geométricas de punto
  // dentro de figura. No se dibuja ni se leen píxeles: isPointInPath/InStroke son
  // puramente geométricas y no dependen del tamaño del lienzo. Evitamos
  // getImageData por completo (iOS Safari lo "envenena" con su protección
  // antihuella tras unas pocas llamadas, devolviendo datos en blanco → iconos
  // vacíos). Así cada icono se forma igual, sin leer píxeles y con un único
  // lienzo auxiliar en toda la página.
  var _probe = document.createElement('canvas');
  _probe.width = 1; _probe.height = 1;
  var _pctx = _probe.getContext('2d');
  if (_pctx) { _pctx.lineCap = 'round'; _pctx.lineJoin = 'round'; }

  // Muestrea la silueta del icono en una rejilla y devuelve targets normalizados.
  function sampleTargets(shapes) {
    var G = 96, c = _pctx;
    // Prepara los Path2D (con metadatos de relleno/trazo) una sola vez.
    var paths = shapes.map(function (s) {
      var p;
      if (s.rect) {
        p = new Path2D();
        var r = s.rect, x = r[0], y = r[1], w = r[2], h = r[3], rr = r[4];
        p.moveTo(x + rr, y);
        p.arcTo(x + w, y, x + w, y + h, rr);
        p.arcTo(x + w, y + h, x, y + h, rr);
        p.arcTo(x, y + h, x, y, rr);
        p.arcTo(x, y, x + w, y, rr);
        p.closePath();
      } else {
        p = new Path2D(s.d);
      }
      return { p: p, stroke: s.stroke || 0, rule: s.rule || 'nonzero' };
    });
    var pts = [];
    var step = 1.7;
    for (var y = 0; y < G; y += step) {
      for (var x = 0; x < G; x += step) {
        var hit = false;
        for (var k = 0; k < paths.length; k++) {
          var pa = paths[k];
          if (pa.stroke) {
            c.lineWidth = pa.stroke;
            if (c.isPointInStroke(pa.p, x, y)) { hit = true; break; }   // figura de contorno (línea)
          } else if (c.isPointInPath(pa.p, x, y, pa.rule)) { hit = true; break; }
        }
        if (hit) pts.push([x / G, y / G]);
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
    // Sobre fondo claro (.section-light) los puntos van oscuros (contraste).
    var light = !!canvas.closest('.section-light');
    var COL_M = light ? '7,56,61' : MENTA;
    var COL_C = light ? '11,70,76' : CREMA;

    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var W = 0, H = 0, S = 0, OX = 0, OY = 0;
    var MAX = +canvas.getAttribute('data-max') || 560;
    var DOT = +canvas.getAttribute('data-dot') || 1;   // escala del tamaño de punto
    var FIT = +canvas.getAttribute('data-fit') || 1;   // fracción del lado menor que ocupa la figura
    var NET = canvas.hasAttribute('data-net') && name !== 'metodo-convergencia'; // red (no en el logo)
    var GLOW = canvas.hasAttribute('data-glow');       // halo menta de fondo
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

    // Red: para cada punto, sus 2 vecinos más cercanos (en la figura formada).
    var edges = [];
    if (NET) {
      var n = pts.length;
      for (var a = 0; a < n; a++) {
        var b1 = -1, b2 = -1, d1 = 9, d2 = 9;
        for (var b = 0; b < n; b++) {
          if (b === a) continue;
          var ddx = pts[a].tx - pts[b].tx, ddy = pts[a].ty - pts[b].ty, dd = ddx * ddx + ddy * ddy;
          if (dd < d1) { d2 = d1; b2 = b1; d1 = dd; b1 = b; }
          else if (dd < d2) { d2 = dd; b2 = b; }
        }
        if (b1 > a) edges.push(a, b1);
        if (b2 > a) edges.push(a, b2);
      }
    }

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
      // halo menta de fondo (profundidad / impacto)
      if (GLOW && progress > 0.02) {
        var gcx = OX + S * 0.5, gcy = OY + S * 0.5, gr = S * 0.62;
        var g = ctx.createRadialGradient(gcx, gcy, 0, gcx, gcy, gr);
        g.addColorStop(0, 'rgba(' + COL_M + ',' + (0.12 * progress).toFixed(3) + ')');
        g.addColorStop(1, 'rgba(' + COL_M + ',0)');
        ctx.fillStyle = g; ctx.fillRect(OX - S * 0.2, OY - S * 0.2, S * 1.4, S * 1.4);
      }
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
        p._x = OX + x * S; p._y = OY + y * S;
        (p.acc ? cC : mC).push(p._x, p._y, p.sz);
      }
      // red de conexiones (sólo cuando está suficientemente formado y si están cerca)
      if (NET && edges.length && progress > 0.25) {
        var cap = S * 0.16, cap2 = cap * cap;
        ctx.lineWidth = 1;
        ctx.strokeStyle = 'rgba(' + COL_M + ',' + (0.16 * (progress - 0.25) / 0.75).toFixed(3) + ')';
        ctx.beginPath();
        for (var e = 0; e < edges.length; e += 2) {
          var pa = pts[edges[e]], pb = pts[edges[e + 1]];
          var dx = pa._x - pb._x, dy = pa._y - pb._y;
          if (dx * dx + dy * dy < cap2) { ctx.moveTo(pa._x, pa._y); ctx.lineTo(pb._x, pb._y); }
        }
        ctx.stroke();
      }
      drawBatch(mC, COL_M); drawBatch(cC, COL_C);
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

    // Respaldo accesible: el contenedor muestra un SVG SÓLIDO del icono por
    // defecto. Solo "encendemos" el lienzo de partículas (clase .ico-ok en el
    // contenedor) cuando NO hay movimiento reducido y el lienzo puede medirse.
    // Si algo falla, queda el sólido visible — el icono nunca desaparece.
    var host = canvas.parentElement;
    if (reduce) { return; }                         // movimiento reducido → SVG sólido
    if (host) host.classList.add('ico-ok');         // revela el lienzo (el CSS lo tenía oculto)
    resize();
    if (W < 2 || H < 2) {                           // el lienzo no obtuvo tamaño → vuelve al sólido
      if (host) host.classList.remove('ico-ok');
      return;
    }
    window.addEventListener('resize', function () { resize(); });

    var step = canvas.closest('.step');
    if (step) {
      // En el stepper: converge cuando el paso se activa; se re-dispersa después.
      var section = canvas.closest('.stepper') || step;
      var sectionIn = false, stepIn = false;
      function recompute() {
        var staticVisible = (getComputedStyle(step).position !== 'absolute');
        // móvil (apilado): converge al entrar el paso; escritorio: según .active
        target = staticVisible ? (stepIn ? 1 : 0) : (step.classList.contains('active') ? 1 : 0);
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
