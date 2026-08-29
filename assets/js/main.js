/* ============================================================
   Veraly — JS del sitio. Vanilla, sin dependencias.
   El contenido esencial NO depende de este archivo (requisito
   de citación por IA). Aquí solo hay progresividad e interacción.
   ============================================================ */
(function () {
  'use strict';

  /* ---- Configuración (placeholders — ver §17 pendientes) ---- */
  var CONFIG = {
    GA_ID: 'G-XXXXXXXXXX',            // TODO: id real de GA4
    FORM_ENDPOINT: '',                // TODO: endpoint de formulario (p.ej. Formspree). Vacío = fallback mailto
    FIRM_EMAIL: 'contacto@veraly.co', // TODO: correo definitivo (pendiente 07)
    WHATSAPP: '',                     // TODO: número wa.me (pendiente 07)
    CAL_LINK: '',                     // TODO: enlace Cal.com de la firma, p.ej. 'veraly/consulta'
  };

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  document.documentElement.classList.add('js');

  /* ---------- Analítica con consentimiento ---------- */
  var consent = localStorage.getItem('veraly-consent');
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  function loadGA() {
    if (!CONFIG.GA_ID || CONFIG.GA_ID.indexOf('XXXX') > -1) return; // sin id real, no carga
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + CONFIG.GA_ID;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', CONFIG.GA_ID, { anonymize_ip: true });
  }

  function track(name, params) {
    if (consent !== 'accepted') return;
    gtag('event', name, params || {});
  }

  if (consent === 'accepted') loadGA();

  /* ---------- Banner de cookies (no bloqueante) ---------- */
  function buildConsent() {
    if (consent) return;
    var bar = document.createElement('div');
    bar.className = 'cookie-bar';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Aviso de cookies');
    bar.innerHTML =
      '<p>Usamos analítica para entender cómo se usa el sitio. Puede aceptarla o continuar sin ella. ' +
      '<a href="/politica-de-cookies/">Más información</a>.</p>' +
      '<div class="cookie-actions">' +
      '<button type="button" class="btn btn--ghost btn--sm" data-consent="declined">Solo esenciales</button>' +
      '<button type="button" class="btn btn--primary btn--sm" data-consent="accepted">Aceptar analítica</button>' +
      '</div>';
    document.body.appendChild(bar);
    $$('[data-consent]', bar).forEach(function (b) {
      b.addEventListener('click', function () {
        consent = b.getAttribute('data-consent');
        localStorage.setItem('veraly-consent', consent);
        if (consent === 'accepted') loadGA();
        bar.remove();
      });
    });
  }
  buildConsent();

  /* ---------- Navegación móvil ---------- */
  var toggle = $('.nav-toggle');
  var menuWrap = $('.nav-menu-wrap');
  var ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>';
  var ICON_CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  if (toggle && menuWrap) {
    toggle.addEventListener('click', function () {
      var open = menuWrap.getAttribute('data-open') === 'true';
      menuWrap.setAttribute('data-open', String(!open));
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? 'Abrir menú' : 'Cerrar menú');
      toggle.innerHTML = open ? ICON_MENU : ICON_CLOSE;
      document.body.setAttribute('data-nav-open', String(!open));
    });
    // cerrar el menú al navegar a un ancla o enlace
    menuWrap.addEventListener('click', function (e) {
      if (e.target.closest('a') && menuWrap.getAttribute('data-open') === 'true') {
        menuWrap.setAttribute('data-open', 'false');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.innerHTML = ICON_MENU;
        document.body.setAttribute('data-nav-open', 'false');
      }
    });
    document.addEventListener('keyup', function (e) {
      if (e.key === 'Escape' && menuWrap.getAttribute('data-open') === 'true') { toggle.click(); }
    });
  }

  /* ---------- Dropdown "Situaciones" (desktop hover + click/teclado) ---------- */
  $$('.has-sub').forEach(function (item) {
    var btn = $('button', item);
    if (!btn) return;
    btn.setAttribute('aria-expanded', 'false');
    function setOpen(v) {
      item.setAttribute('data-open', String(v));
      btn.setAttribute('aria-expanded', String(v));
    }
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      setOpen(item.getAttribute('data-open') !== 'true');
    });
    item.addEventListener('mouseenter', function () { if (window.innerWidth > 900) setOpen(true); });
    item.addEventListener('mouseleave', function () { if (window.innerWidth > 900) setOpen(false); });
    document.addEventListener('click', function (e) { if (!item.contains(e.target)) setOpen(false); });
    item.addEventListener('keyup', function (e) { if (e.key === 'Escape') setOpen(false); });
  });

  /* ---------- Contador de caracteres ---------- */
  $$('[data-maxcount]').forEach(function (input) {
    var max = parseInt(input.getAttribute('data-maxcount'), 10);
    var out = $('#' + input.getAttribute('aria-describedby').split(' ').filter(function (id) { return id.indexOf('count') > -1; })[0]);
    function upd() { if (out) out.textContent = input.value.length + ' / ' + max; }
    input.addEventListener('input', upd); upd();
  });

  /* ---------- Validación y envío del formulario ---------- */
  $$('form[data-veraly-form]').forEach(function (form) {
    var started = false;
    form.addEventListener('focusin', function () {
      if (!started) { started = true; track('form_start', { page_path: location.pathname }); }
    });

    function setInvalid(field, on) { field.setAttribute('data-invalid', String(on)); }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true, firstBad = null;
      $$('.field', form).forEach(function (field) {
        var input = $('input', field);
        if (!input) return;
        var required = input.hasAttribute('required');
        var val = input.value.trim();
        var bad = false;
        if (required && !val) bad = true;
        if (input.dataset.validate === 'contact' && val) {
          var isEmail = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(val);
          var isPhone = /^[+\d][\d\s().-]{6,}$/.test(val);
          if (!isEmail && !isPhone) bad = true;
        }
        setInvalid(field, bad);
        if (bad) { ok = false; firstBad = firstBad || input; }
      });
      var check = $('.check input', form);
      var checkField = check ? check.closest('.check') : null;
      if (check && !check.checked) { ok = false; if (checkField) checkField.style.color = '#FFC7B8'; firstBad = firstBad || check; }
      else if (checkField) checkField.style.color = '';

      var status = $('.form-status', form);
      if (!ok) {
        track('form_error', { page_path: location.pathname, tipo_error: 'validacion' });
        if (firstBad) firstBad.focus();
        return;
      }

      var perfil = form.getAttribute('data-perfil') || 'institucional';
      submit(form, status, perfil);
    });

    function submit(form, status, perfil) {
      var btn = $('button[type=submit]', form);
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = 'Enviando…'; }

      function done(success) {
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; }
        if (status) {
          status.className = 'form-status ' + (success ? 'ok' : 'err');
          status.setAttribute('data-show', 'true');
          status.textContent = success
            ? 'Recibimos su mensaje. Le respondemos dentro de las próximas 24 horas hábiles. Si su situación tiene un término corriendo, puede escribirnos también por WhatsApp o llamarnos.'
            : 'No pudimos enviar el mensaje. Puede intentarlo de nuevo o escribirnos directamente a ' + CONFIG.FIRM_EMAIL + ' o por WhatsApp.';
        }
        if (success) { form.reset(); track('form_submit', { page_path: location.pathname, perfil_inferido: perfil }); }
        else track('form_error', { page_path: location.pathname, tipo_error: 'envio' });
      }

      if (CONFIG.FORM_ENDPOINT) {
        fetch(CONFIG.FORM_ENDPOINT, {
          method: 'POST',
          headers: { 'Accept': 'application/json' },
          body: new FormData(form)
        }).then(function (r) { done(r.ok); }).catch(function () { done(false); });
      } else {
        // Fallback sin backend: abre el cliente de correo con datos mínimos.
        var data = new FormData(form), parts = [];
        data.forEach(function (v, k) { if (k !== 'autorizacion') parts.push(k + ': ' + v); });
        var href = 'mailto:' + CONFIG.FIRM_EMAIL +
          '?subject=' + encodeURIComponent('Consulta desde el sitio (' + perfil + ')') +
          '&body=' + encodeURIComponent(parts.join('\n'));
        window.location.href = href;
        done(true);
      }
    }
  });

  /* ---------- Eventos de conversión y micro ---------- */
  $$('a[href^="tel:"]').forEach(function (a) {
    a.addEventListener('click', function () { track('phone_click', { page_path: location.pathname, posicion: a.dataset.pos || 'body' }); });
  });
  $$('a[href*="wa.me"],a[data-whatsapp]').forEach(function (a) {
    a.addEventListener('click', function () { track('whatsapp_click', { page_path: location.pathname, posicion: a.dataset.pos || 'body' }); });
  });
  $$('a[data-download]').forEach(function (a) {
    a.addEventListener('click', function () { track('download_' + a.dataset.download, { page_path: location.pathname }); });
  });
  $$('a[data-situacion]').forEach(function (a) {
    a.addEventListener('click', function () { track('situacion_click', { situacion: a.dataset.situacion }); });
  });
  $$('a[data-marca]').forEach(function (a) {
    a.addEventListener('click', function () { track('marca_click', { origen: location.pathname }); });
  });
  $$('a[data-socio]').forEach(function (a) {
    a.addEventListener('click', function () { track('socio_view', { socio: a.dataset.socio, origen: location.pathname }); });
  });
  $$('.accordion details').forEach(function (d) {
    d.addEventListener('toggle', function () { if (d.open) track('fase_open', { fase: d.dataset.fase || '', page_path: location.pathname }); });
  });
  $$('.faq details').forEach(function (d) {
    d.addEventListener('toggle', function () { if (d.open) track('faq_open', { pregunta: (d.querySelector('summary') || {}).textContent || '' }); });
  });

  /* ---------- Agendamiento (Cal.com) ---------- */
  function toast(msg) {
    var t = document.createElement('div');
    t.className = 'toast'; t.textContent = msg; document.body.appendChild(t);
    requestAnimationFrame(function () { t.setAttribute('data-show', 'true'); });
    setTimeout(function () { t.removeAttribute('data-show'); setTimeout(function () { t.remove(); }, 300); }, 3600);
  }
  var calReady = false;
  function initCal() {
    if (!CONFIG.CAL_LINK) return;
    /* eslint-disable */
    (function (C, A, L) { var p = function (a, ar) { a.q.push(ar); }; var d = C.document; C.Cal = C.Cal || function () { var cal = C.Cal; var ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { var api = function () { p(api, arguments); }; var namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); } else p(cal, ar); return; } p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "init");
    /* eslint-enable */
    window.Cal("init", { origin: "https://cal.com" });
    window.Cal("ui", { theme: "dark", styles: { branding: { brandColor: "#89F5E5" } } });
    calReady = true;
  }
  initCal();
  function openScheduler() {
    if (calReady && window.Cal) {
      window.Cal("modal", { calLink: CONFIG.CAL_LINK });
    } else {
      // Fallback sin calendario conectado: llevar al formulario/contacto.
      toast('Agendamiento en línea: se activa al conectar el calendario de la firma. Puede escribirnos mientras tanto.');
      if (location.pathname.indexOf('/contacto') === -1) location.href = '/contacto/';
      else { var f = document.querySelector('form[data-veraly-form]'); if (f) f.scrollIntoView({ behavior: 'smooth' }); }
    }
  }
  $$('[data-cal]').forEach(function (el) {
    el.addEventListener('click', function (e) { e.preventDefault(); track('agendar_click', { page_path: location.pathname }); openScheduler(); });
  });
  var calInline = $('#cal-inline');
  if (calInline) {
    if (calReady && window.Cal) {
      window.Cal('inline', { elementOrSelector: '#cal-inline', calLink: CONFIG.CAL_LINK });
    } else {
      calInline.innerHTML = '<p style="color:var(--dim-2);margin:0">El calendario en línea se activa al conectar la cuenta de la firma. Mientras tanto, puede usar el formulario, WhatsApp o el teléfono.</p>';
    }
  }

  /* ---------- Asistente guiado (determinista, sin IA, sin campo libre) ---------- */
  var FLOW = {
    start: { q: '¿Con qué le podemos ayudar?', options: [
      { label: 'Perdí dinero en una captación', to: 'A' },
      { label: 'Me investigan o me vincularon', to: 'B' },
      { label: 'Mi empresa recauda de muchas personas', to: 'C' },
      { label: 'Quiero entender el tema', to: 'INFO' } ] },
    A: { q: '¿Ya hubo toma de posesión o intervención?', options: [
      { label: 'Sí, ya hay intervención', to: 'A1' },
      { label: 'No, o no lo sé', to: 'A2' } ] },
    A1: { text: 'Dentro de la intervención los plazos son cortos: las solicitudes de devolución se presentan en 10 días comunes desde el aviso del interventor. Conviene actuar pronto.',
      page: ['Ver la ruta del afectado', '/afectados-por-captacion-masiva/'], cta: 'agendar' },
    A2: { text: 'Existen tres vías —administrativa, penal y civil— y la calificación correcta cambia la estrategia y lo que se recupera por cada una.',
      page: ['Ver la ruta del afectado', '/afectados-por-captacion-masiva/'], cta: 'agendar' },
    B: { q: '¿En qué momento está?', options: [
      { label: 'Requerimientos o visita administrativa', to: 'B1' },
      { label: 'Ya hay captura o imputación', to: 'B2' },
      { label: 'Soy revisor fiscal, contador o proveedor', to: 'B3' } ] },
    B1: { text: 'Es la fase administrativa previa: todavía se puede sustentar el modelo y, en su caso, evitar la declaratoria y la suspensión.',
      page: ['Ver la ruta de la defensa', '/defensa-en-captacion-masiva/'], cta: 'urgente' },
    B2: { text: 'El momento procesal define lo que aún es posible. La defensa se juega desde los actos urgentes y la audiencia de imputación.',
      page: ['Ver la ruta de la defensa', '/defensa-en-captacion-masiva/'], cta: 'urgente' },
    B3: { text: 'La vinculación alcanza esas posiciones por el ejercicio del cargo, pero es desvirtuable: la exclusión se construye sobre la buena fe exenta de culpa y el origen lícito.',
      page: ['Ver la ruta de la defensa', '/defensa-en-captacion-masiva/'], cta: 'urgente' },
    C: { q: '¿Qué tipo de modelo?', options: [
      { label: 'Fintech o crowdfunding', to: 'C1' },
      { label: 'Libranzas, factoring o multinivel', to: 'C1' },
      { label: 'Otro modelo de recaudo', to: 'C1' } ] },
    C1: { text: 'La clave es doble: los umbrales del Decreto 1981 de 1988 y la explicación financiera razonable del rendimiento. Ambas se revisan antes de que las revise una superintendencia.',
      page: ['Ver la ruta preventiva', '/cumplimiento-en-recaudo-masivo/'], cta: 'agendar' },
    INFO: { text: 'Publicamos sobre las figuras del fraude financiero: cómo se estructuran, cómo se investigan y qué vías abren. Nunca sobre casos identificables.',
      page: ['Ir a Análisis', '/analisis/'], cta: 'none' }
  };
  var asst = $('#asst'), asstLaunch = $('#asst-launch'), asstPanel = $('#asst-panel'),
      asstClose = $('#asst-close'), asstBody = $('#asst-body');
  function asstRender(key) {
    var node = FLOW[key]; if (!node) return;
    asstBody.innerHTML = '';
    if (node.q) {
      var h = document.createElement('p'); h.className = 'asst-q'; h.textContent = node.q; asstBody.appendChild(h);
      node.options.forEach(function (o) {
        var b = document.createElement('button'); b.className = 'asst-opt'; b.textContent = o.label;
        b.addEventListener('click', function () { asstRender(o.to); });
        asstBody.appendChild(b);
      });
    } else {
      var p = document.createElement('p'); p.className = 'asst-text'; p.textContent = node.text; asstBody.appendChild(p);
      var acts = document.createElement('div'); acts.className = 'asst-actions';
      if (node.cta === 'agendar') {
        acts.appendChild(mkA('Agendar una consulta', '#agendar', 'primary', true));
      } else if (node.cta === 'urgente') {
        acts.appendChild(mkA('Escribir ahora', '/contacto/', 'primary', false));
      }
      if (node.page) {
        var pl = document.createElement('a'); pl.className = 'asst-link'; pl.href = node.page[1];
        pl.textContent = node.page[0] + ' →'; acts.appendChild(pl);
      }
      asstBody.appendChild(acts);
      var back = document.createElement('button'); back.className = 'asst-back'; back.textContent = '← Empezar de nuevo';
      back.addEventListener('click', function () { asstRender('start'); }); asstBody.appendChild(back);
    }
  }
  function mkA(label, href, kind, isCal, isTel) {
    var a = document.createElement('a'); a.className = 'btn btn--' + kind + ' btn--sm';
    if (isTel) { a.href = 'tel:'; a.setAttribute('data-pos', 'asistente'); }
    else a.href = href;
    a.textContent = label;
    if (isCal) { a.setAttribute('data-cal', ''); a.addEventListener('click', function (e) { e.preventDefault(); openScheduler(); }); }
    return a;
  }
  function asstToggle(open) {
    if (!asstPanel) return;
    asstPanel.hidden = !open;
    asstLaunch.setAttribute('aria-expanded', String(open));
    asst.setAttribute('data-open', String(open));
    if (open && !asstBody.hasChildNodes()) asstRender('start');
  }
  if (asstLaunch) {
    asstLaunch.addEventListener('click', function () { asstToggle(asstPanel.hidden); track('asistente_open', { page_path: location.pathname }); });
    asstClose.addEventListener('click', function () { asstToggle(false); });
    document.addEventListener('keyup', function (e) { if (e.key === 'Escape' && !asstPanel.hidden) asstToggle(false); });
  }

  /* ---------- Pin scroll helpers (stepper + reveal) ---------- */
  function pinProgress(track) {
    var r = track.getBoundingClientRect();
    var total = track.offsetHeight - window.innerHeight;
    return total > 0 ? Math.min(1, Math.max(0, (-r.top) / total)) : 0;
  }
  function initStepper() {
    var track = $('.stepper-track'); if (!track || track.__i) return; track.__i = 1;
    var steps = $$('.step', track), rail = $$('.stepper-rail li', track), n = steps.length;
    if (!n) return;
    function upd() {
      if (window.innerWidth <= 900) { steps.forEach(function (s) { s.classList.add('active'); }); return; }
      var idx = Math.min(n - 1, Math.floor(pinProgress(track) * n));
      steps.forEach(function (s, i) { s.classList.toggle('active', i === idx); });
      rail.forEach(function (li, i) { li.classList.toggle('on', i === idx); });
    }
    window.addEventListener('scroll', upd, { passive: true });
    window.addEventListener('resize', upd); upd();
  }
  function initReveal() {
    var track = $('.reveal-track'); if (!track || track.__i) return; track.__i = 1;
    var phrases = $$('.reveal-phrase', track), cards = $$('.reveal-cards .rc', track);
    var np = phrases.length; if (!np) return;
    var words = phrases.map(function (p) { return $$('.w', p); });
    function upd() {
      if (window.innerWidth <= 900) {
        phrases.forEach(function (p) { p.classList.add('active'); });
        words.forEach(function (ws) { ws.forEach(function (w) { w.classList.add('lit'); }); });
        cards.forEach(function (c) { c.classList.add('in'); });
        return;
      }
      var p = pinProgress(track);
      var idx = Math.min(np - 1, Math.floor(p * np));
      var local = (p * np) - idx;
      phrases.forEach(function (ph, i) { ph.classList.toggle('active', i === idx); });
      var lit = Math.min(1, local / 0.55); // ilumina en el primer 55% y mantiene
      words[idx].forEach(function (w, j) { w.classList.toggle('lit', (j + 0.6) / words[idx].length <= lit); });
      cards.forEach(function (c, k) { c.classList.toggle('in', p >= (k + 1) / (cards.length + 1)); });
    }
    window.addEventListener('scroll', upd, { passive: true });
    window.addEventListener('resize', upd); upd();
  }
  /* ---------- Las tres vías: entrada + parallax interno ---------- */
  var frowIO = ('IntersectionObserver' in window)
    ? new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); frowIO.unobserve(e.target); } });
      }, { threshold: 0.2, rootMargin: '0px 0px -8% 0px' })
    : null;
  function frowPar() {
    var vh = window.innerHeight;
    $$('.fr-par').forEach(function (par) {
      var m = par.parentNode.getBoundingClientRect();
      var rel = ((m.top + m.height / 2) - vh / 2) / vh;
      rel = Math.max(-1, Math.min(1, rel));
      var t = (1 - rel) / 2;                 // 0 al entrar por abajo, 1 al salir por arriba
      var scale = (1 + 0.24 * t).toFixed(3); // la imagen "crece" con el scroll
      par.style.transform = 'translate3d(0,' + (rel * -9).toFixed(2) + '%,0) scale(' + scale + ')';
    });
    // parallax del título de la sección "Qué resuelve"
    if (!window.matchMedia || !window.matchMedia('(prefers-reduced-motion:reduce)').matches) {
      $$('.pr-parallax').forEach(function (el) {
        var r = el.getBoundingClientRect();
        var rel = (r.top + r.height / 2) - vh / 2;
        el.style.transform = 'translateY(' + (rel * -0.12).toFixed(1) + 'px)';
      });
    }
  }
  function initFeatureRows() {
    var rows = $$('.frow').concat($$('.prac-rows')).concat($$('.pr-timeline')).concat($$('.reveal-up'));
    rows.forEach(function (r) { if (r.__f) return; r.__f = 1; if (frowIO) frowIO.observe(r); else r.classList.add('in'); });
    if (rows.length && !window.__frowScroll) {
      window.__frowScroll = 1;
      window.addEventListener('scroll', frowPar, { passive: true });
      window.addEventListener('resize', frowPar);
    }
    frowPar();
  }
  function initBlog() {
    var filters = $$('.bfilter'), grid = $('[data-blog-grid]');
    if (filters.length && grid) {
      var cards = $$('.bcard', grid);
      filters.forEach(function (btn) {
        if (btn.__b) return; btn.__b = 1;
        btn.addEventListener('click', function () {
          var t = btn.getAttribute('data-tema') || '';
          filters.forEach(function (f) { f.classList.toggle('is-active', f === btn); });
          cards.forEach(function (c) {
            c.hidden = !(t === '' || c.getAttribute('data-tema') === t);
          });
        });
      });
    }
    $$('[data-share-copy]').forEach(function (btn) {
      if (btn.__b) return; btn.__b = 1;
      btn.addEventListener('click', function () {
        var url = btn.getAttribute('data-share-copy');
        var done = function () {
          var prev = btn.textContent; btn.textContent = '✓'; btn.classList.add('is-copied');
          setTimeout(function () { btn.textContent = prev; btn.classList.remove('is-copied'); }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(done, done);
        } else { done(); }
      });
    });
  }
  /* ---------- Títulos de sección: efecto "scramble/decode" ---------- */
  var scrReduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var SCR_GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  function scrambleText(el) {
    // localizar el último nodo de texto (preserva iconos/números anteriores)
    var node = null;
    for (var i = el.childNodes.length - 1; i >= 0; i--) {
      var n = el.childNodes[i];
      if (n.nodeType === 3 && n.nodeValue.replace(/\s/g, '')) { node = n; break; }
    }
    var text = node ? node.nodeValue : el.textContent;
    var set = node ? function (v) { node.nodeValue = v; } : function (v) { el.textContent = v; };
    var start = 0, dur = Math.min(1100, text.length * 55 + 280);
    function frame(now) {
      if (!start) start = now;
      var p = Math.min(1, (now - start) / dur);
      var reveal = p * text.length, out = '';
      for (var i = 0; i < text.length; i++) {
        var c = text.charAt(i);
        if (c === ' ' || c === '/' || c === '·' || i < reveal - 0.4) { out += c; }
        else { out += SCR_GLYPHS.charAt((Math.random() * SCR_GLYPHS.length) | 0); }
      }
      set(out);
      if (p < 1) requestAnimationFrame(frame); else set(text);
    }
    requestAnimationFrame(frame);
  }
  var scrIO = ('IntersectionObserver' in window)
    ? new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { scrIO.unobserve(e.target); scrambleText(e.target); } });
      }, { threshold: 0.6 })
    : null;
  function initScramble() {
    $$('.eyebrow, .eyebrow-num, .faq-pill, .bfilter-pill, .article-kicker, .pr-tl-label').forEach(function (el) {
      if (el.__scr) return; el.__scr = 1;
      if (scrIO) scrIO.observe(el); else scrambleText(el);
    });
  }
  window.__initPins = function () { initStepper(); initReveal(); initFeatureRows(); initBlog(); initScramble(); };
  window.__initPins();

  /* ---------- Profundidad de scroll ---------- */
  var fired = {};
  function onScroll() {
    var h = document.documentElement;
    var pct = (h.scrollTop) / (h.scrollHeight - h.clientHeight) * 100;
    [60, 90].forEach(function (mark) {
      if (pct >= mark && !fired[mark]) { fired[mark] = true; track('scroll_' + mark, { page_path: location.pathname }); }
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Nav que se oculta/muestra con el scroll ---------- */
  (function () {
    var hdr = $('.site-header'); if (!hdr) return;
    var lastY = window.pageYOffset || 0, ticking = false;
    function apply() {
      ticking = false;
      var y = window.pageYOffset || 0;
      var navOpen = document.body.getAttribute('data-nav-open') === 'true';
      if (y <= 90 || navOpen) { hdr.classList.remove('nav-hidden'); lastY = y; return; }
      var dy = y - lastY;
      if (dy > 6) hdr.classList.add('nav-hidden');        // baja → esconde
      else if (dy < -6) hdr.classList.remove('nav-hidden'); // sube → muestra
      lastY = y;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(apply); }
    }, { passive: true });
  })();
})();
