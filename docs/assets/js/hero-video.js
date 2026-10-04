/* ============================================================
   Hero video — efecto 3D ligado al scroll.
   La escena se "fija" (sticky): al entrar, el marco baja, crece y se
   endereza (rotateX → 0); mientras se mantiene, se reproduce; al salir,
   sube y se encoge para dejar ver el resto del contenido.
   <video> se reproduce/pausa según visibilidad; un <img> (webp/gif) sólo
   recibe el efecto. prefers-reduced-motion: estático, sin transformar.
   ============================================================ */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  function ease(t) { return t < 0 ? 0 : t > 1 ? 1 : t * t * (3 - 2 * t); }

  function setup(scene) {
    if (scene.__v) return; scene.__v = 1;
    var frame = scene.querySelector('.vs-frame');
    var video = scene.querySelector('video');
    if (!frame) return;

    function onScroll() {
      var r = scene.getBoundingClientRect();
      var vh = window.innerHeight || 1;
      var range = Math.max(1, scene.offsetHeight - vh);
      var p = Math.min(1, Math.max(0, -r.top / range));
      var scale, ty, rx, op;
      if (p < 0.30) {                 // entrada: baja, crece, se endereza
        var t = ease(p / 0.30);
        scale = 0.64 + 0.36 * t; rx = (1 - t) * 13; ty = (1 - t) * 7; op = 0.35 + 0.65 * t;
      } else if (p < 0.72) {          // fijo: a tamaño completo
        scale = 1; rx = 0; ty = 0; op = 1;
      } else {                        // salida: sube y se encoge
        var t2 = ease((p - 0.72) / 0.28);
        scale = 1 - 0.1 * t2; rx = 0; ty = -13 * t2; op = 1 - 0.45 * t2;
      }
      frame.style.transform = 'translateY(' + ty.toFixed(2) + 'vh) rotateX(' + rx.toFixed(2) + 'deg) scale(' + scale.toFixed(3) + ')';
      frame.style.opacity = op.toFixed(3);
    }

    if (reduce) { frame.style.transform = 'none'; }
    else {
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', onScroll);
      onScroll();
    }

    if (video && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) { var pr = video.play && video.play(); if (pr && pr.catch) pr.catch(function () {}); }
          else if (video.pause) { video.pause(); }
        });
      }, { threshold: 0.25 }).observe(scene);
    }
  }

  function init() {
    var list = document.querySelectorAll('[data-video-scene]');
    for (var i = 0; i < list.length; i++) setup(list[i]);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
  window.initHeroVideo = init;
})();
