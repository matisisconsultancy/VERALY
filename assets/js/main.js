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
  };

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

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
      '<a href="/aviso-de-privacidad/">Más información</a>.</p>' +
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
})();
