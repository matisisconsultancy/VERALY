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
      if (p < 0.22) {                 // título solo: video oculto
        scale = 0.82; rx = 12; ty = 16; op = 0;
      } else if (p < 0.5) {           // sube y cubre el titular (3D → plano)
        var t = ease((p - 0.22) / 0.28);
        scale = 0.82 + 0.18 * t; rx = (1 - t) * 12; ty = (1 - t) * 16; op = t;
      } else if (p < 0.72) {          // fijo: reproduciéndose
        scale = 1; rx = 0; ty = 0; op = 1;
      } else {                        // sube y revela el resto
        var t2 = ease((p - 0.72) / 0.28);
        scale = 1 - 0.1 * t2; rx = 0; ty = -16 * t2; op = 1 - 0.75 * t2;
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
