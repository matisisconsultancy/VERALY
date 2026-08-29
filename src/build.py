#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador estático del sitio de Veraly Grupo Jurídico.
No hay build en CI: este script se ejecuta localmente y emite HTML final
en las rutas limpias del sitemap (carpeta/index.html). GitHub Pages sirve
esos archivos tal cual. Fuente de verdad del copy: especificación funcional v1.0.

Uso:  python3 src/build.py
"""
import os, json, html, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------------------------------------------------------
# Configuración del sitio
# ----------------------------------------------------------------------------
SITE = {
    "name": "Veraly Grupo Jurídico",
    "claim": "Defensa en fraude financiero",
    # Dominio canónico PENDIENTE (decisión 05). Placeholder para canónicas/OG/sitemap.
    "base_url": "https://veraly.co",
    "locale": "es-CO",
    # Datos de contacto PENDIENTES (decisión 07) — placeholders marcados.
    "email": "contacto@veraly.co",
    "phone_display": "+57 000 000 0000",
    "phone_href": "+570000000000",
    "whatsapp": "",  # wa.me/57XXXXXXXXXX
    "address": "Dirección por definir — Colombia",
    "hours": "Lun a Vie, 8:00–18:00",
    # Agendamiento (Cal.com). Placeholder hasta conectar el calendario de la firma.
    "cal_link": "",  # p.ej. "veraly/consulta"  (TODO: cuenta Cal.com de la firma)
}

# Isotipo "Convergencia" reutilizado del brandbook (cinco V hacia un punto).
LOGO_SVG = ('<svg viewBox="-140 -140 280 280" fill="none" aria-hidden="true" focusable="false">'
    '<g stroke="currentColor" stroke-width="17.6" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M -29.2 -120.8 L 0.0 -39.6 L 39.6 -72.0"/>'
    '<path d="M 105.6 -64.8 L 37.6 -12.0 L 80.4 15.6"/>'
    '<path d="M 94.4 80.4 L 23.2 32.0 L 10.0 81.2"/>'
    '<path d="M -47.2 114.8 L -23.2 32.0 L -74.0 34.8"/>'
    '<path d="M -124.0 -9.6 L -37.6 -12.0 L -56.0 -59.6"/></g>'
    '<circle cx="0" cy="0" r="16.0" fill="currentColor"/></svg>')

ICON_CHEVRON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>'
ICON_CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'

# ----------------------------------------------------------------------------
# Datos: socios (dato cerrado) y artículos de arranque
# Formación/cargos PENDIENTES (decisión 03) — marcados como placeholder.
# ----------------------------------------------------------------------------
SOCIOS = [
    {"slug": "hermes-vergara", "nombre": "Hermes Vergara",
     "practica": "Derecho contractual y constitucional",
     "aporte": "Estructura la lectura constitucional del debido proceso en un trámite de única instancia y el andamiaje contractual de las relaciones anteriores a la toma de posesión."},
    {"slug": "kewin-santiago-canizales", "nombre": "Kewin Santiago Canizales",
     "practica": "Derecho tributario y migratorio",
     "aporte": "Analiza las contingencias tributarias sobre los flujos del esquema y las consecuencias migratorias que alcanzan a vinculados extranjeros."},
    {"slug": "miguel-bayter", "nombre": "Miguel Bayter",
     "practica": "Derecho corporativo y urbano",
     "aporte": "Aborda las controversias societarias sobre actos anteriores a la intervención y la situación de los activos inmobiliarios comprometidos."},
    {"slug": "juan-david-naar", "nombre": "Juan David Naar",
     "practica": "Derecho penal y derecho informático",
     "aporte": "Conduce la defensa penal por los artículos 316 y 316A y la evidencia digital del esquema, desde los actos urgentes hasta el juicio oral."},
    {"slug": "javier-pisciotti", "nombre": "Javier Pisciotti",
     "practica": "Derecho laboral y seguros",
     "aporte": "Resuelve las reclamaciones laborales de la sociedad intervenida y la exposición de las pólizas y garantías vinculadas al recaudo."},
]

ARTICLES = [
    {
        "slug": "diferencia-entre-estafa-y-captacion-masiva",
        "tema": "El fenómeno", "perfil": "A · B", "author": "juan-david-naar",
        "date_iso": "2026-08-12", "date_disp": "12 AGO 2026",
        "title": "Diferencia entre estafa y captación masiva",
        "h1": "¿Qué diferencia hay entre estafa y captación masiva?",
        "desc": "Estafa y captación masiva son delitos distintos: cambian el proceso, la defensa y la vía de recuperación. La captación activa además un trámite administrativo propio.",
        "answer": "La estafa y la captación masiva y habitual son tipos penales distintos. La captación, además del proceso penal del artículo 316, activa un procedimiento administrativo especial ante la Superintendencia de Sociedades, con un mecanismo de devolución que la estafa no tiene. La calificación correcta cambia la estrategia completa.",
        "cta_target": "afectados",
    },
    {
        "slug": "captacion-con-libranzas-y-factoring",
        "tema": "El fenómeno", "perfil": "A · B · C", "author": "miguel-bayter",
        "date_iso": "2026-07-28", "date_disp": "28 JUL 2026",
        "title": "Captación montada sobre contratos legales: libranzas y factoring",
        "h1": "¿Cuándo un esquema de libranzas o factoring se convierte en captación?",
        "desc": "Contratos legales como libranzas y factoring pueden configurar captación cuando superan los umbrales y el rendimiento carece de explicación financiera razonable.",
        "answer": "Un esquema de libranzas o factoring —contratos legales en sí mismos— puede configurar captación masiva cuando el pasivo con el público supera los umbrales del Decreto 1981 de 1988 o cuando el rendimiento ofrecido no tiene explicación financiera razonable, en los términos del artículo 6 del Decreto 4334 de 2008.",
        "cta_target": "cumplimiento",
    },
    {
        "slug": "que-hace-la-superintendencia-de-sociedades",
        "tema": "La intervención", "perfil": "A", "author": "hermes-vergara",
        "date_iso": "2026-07-10", "date_disp": "10 JUL 2026",
        "title": "Qué hace la Superintendencia de Sociedades con una captadora",
        "h1": "¿Qué hace la Superintendencia de Sociedades cuando interviene una captadora?",
        "desc": "La ruta administrativa del Decreto 4334 de 2008: toma de posesión, devolución de recursos y plazos, en paralelo al proceso penal.",
        "answer": "La Superintendencia de Sociedades ordena la toma de posesión de los bienes de la captadora mediante el procedimiento del Decreto 4334 de 2008. Sus decisiones tienen carácter jurisdiccional, efectos de cosa juzgada frente a todos y son de única instancia. A partir de ahí se abre el trámite de devolución de recursos a los afectados.",
        "cta_target": "afectados",
    },
    {
        "slug": "buena-fe-exenta-de-culpa-tercero-proveedor",
        "tema": "La defensa", "perfil": "B", "author": "juan-david-naar",
        "date_iso": "2026-06-24", "date_disp": "24 JUN 2026",
        "title": "Buena fe exenta de culpa: el estándar del tercero proveedor",
        "h1": "¿Qué es la buena fe exenta de culpa en un proceso de captación?",
        "desc": "El estándar que puede excluir de la intervención a proveedores y terceros que actuaron de buena fe: qué exige y cómo se acredita.",
        "answer": "La buena fe exenta de culpa es el estándar que, según la Sentencia C-145 de 2009, puede dejar fuera de la intervención a terceros proveedores que actuaron en el ámbito de sus actividades lícitas ordinarias. No basta la creencia honesta: exige diligencia positiva y comprobable, acreditada con documentos, controles y decisiones registradas.",
        "cta_target": "defensa",
    },
]

# Cinco prácticas (composición de la firma, sin nombres — decisión del cliente).
PRACTICAS = [
    {"rama": "Contractual y constitucional",
     "aporte": "El debido proceso en un trámite de única instancia y el andamiaje contractual anterior a la toma de posesión."},
    {"rama": "Tributaria y migratoria",
     "aporte": "Las contingencias tributarias sobre los flujos del esquema y las consecuencias migratorias de los vinculados."},
    {"rama": "Corporativa y urbana",
     "aporte": "Las controversias societarias sobre actos anteriores a la intervención y los activos inmobiliarios comprometidos."},
    {"rama": "Penal e informática",
     "aporte": "La defensa penal por los artículos 316 y 316A y la evidencia digital, desde los actos urgentes hasta el juicio oral."},
    {"rama": "Laboral y de seguros",
     "aporte": "Las reclamaciones laborales de la sociedad intervenida y la exposición de las pólizas y garantías del recaudo."},
]

TEMAS = ["El fenómeno", "La intervención", "La defensa", "La recuperación", "Prevención empresarial"]


def tres_vias_rows():
    """Las tres vías/responsabilidades como filas alternadas (compartido home + /firma)."""
    vias = [
        ("01", "VÍA ADMINISTRATIVA", "Ante la Superintendencia de Sociedades",
         "Procedimiento del Decreto 4334 de 2008. La toma de posesión tiene efectos de cosa juzgada frente a todos y es de única instancia: no hay segunda oportunidad procesal.", wave_svg()),
        ("02", "VÍA PENAL", "Artículos 316 y 316A del Código Penal",
         "Captación masiva y habitual, con prisión de 120 a 240 meses, y el tipo autónomo de no reintegro. A ellos suelen sumarse estafa agravada, lavado de activos y concierto para delinquir.", globe_svg()),
        ("03", "VÍA CIVIL", "Responsabilidad patrimonial",
         "Persigue el patrimonio personal de administradores, revisores fiscales, contadores y vinculados solventes por el faltante que la masa de la intervención no alcanza a cubrir.", wave_svg()),
    ]
    rows = ""
    for i, (num, eyb, h, d, media) in enumerate(vias):
        media_html = (f'<div class="fr-media"><div class="fr-par">{media}</div>'
                      f'<span class="fr-index" aria-hidden="true">{num}</span></div>')
        text_html = (f'<div class="fr-text">'
                     f'<p class="fr-eyebrow">{eyb}</p><h2>{esc(h)}</h2>'
                     f'<p class="lead" style="margin-top:1rem;color:var(--dim)">{esc(d)}</p></div>')
        inner = (media_html + text_html) if i % 2 == 0 else (text_html + media_html)
        rows += f'<div class="frow">{inner}</div>'
    return rows

def socio_by_slug(slug):
    return next(s for s in SOCIOS if s["slug"] == slug)

def esc(s):
    return html.escape(s, quote=True)

# ----------------------------------------------------------------------------
# Enlaces de navegación
# ----------------------------------------------------------------------------
SITUACIONES = [
    ("/afectados-por-captacion-masiva/", "Perdí dinero en un esquema de captación",
     "Vías administrativa, penal y civil, y los plazos que corren.", "afectado"),
    ("/defensa-en-captacion-masiva/", "Me investigan o me vincularon",
     "Defensa en los tres frentes para investigados y vinculados.", "investigado"),
    ("/cumplimiento-en-recaudo-masivo/", "Mi empresa recauda de muchas personas",
     "Revisión de encuadre frente a los umbrales de captación.", "empresa"),
]

# ----------------------------------------------------------------------------
# Plantillas compartidas
# ----------------------------------------------------------------------------
def brand(link=True, small=True):
    inner = (f'<span class="brand-mark" aria-hidden="true" style="width:30px;height:30px;color:var(--accent);display:inline-block">{LOGO_SVG}</span>'
             f'<span><b>Veraly</b>{" <span>Grupo Jurídico</span>" if small else ""}</span>')
    if link:
        return f'<a class="brand" href="/" aria-label="Veraly Grupo Jurídico — inicio">{inner}</a>'
    return f'<span class="brand">{inner}</span>'

def header_html(active=""):
    def cur(key):
        return ' aria-current="page"' if active == key else ''
    sub = "".join(
        f'<li><a href="{url}" data-situacion="{tag}"{cur(tag)}>{esc(t)}<small>{esc(d)}</small></a></li>'
        for url, t, d, tag in SITUACIONES)
    # enlaces reutilizados (pill de escritorio y menú móvil)
    def links(prefix=""):
        return f'''<a href="/firma/"{cur('firma')}>La firma</a>
        <a href="/equipo/"{cur('equipo')}>El equipo</a>
        <div class="has-sub">
          <button type="button" aria-haspopup="true">Soluciones {ICON_CHEVRON}</button>
          <ul class="submenu">{sub}</ul>
        </div>
        <a href="/analisis/"{cur('analisis')}>Análisis</a>'''
    return f'''<a class="skip-link" href="#main">Saltar al contenido</a>
<header class="site-header floating">
  <div class="container nav">
    {brand()}
    <button class="nav-toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav-menu">{ICON_MENU}</button>
    <div class="nav-cluster">
      <nav class="nav-pill" aria-label="Navegación principal">{links()}</nav>
      <a class="btn btn--primary btn--sm nav-cta-pill" href="/contacto/"{cur('contacto')}>Contacto</a>
    </div>
    <div class="nav-menu-wrap" id="nav-menu">
      <ul class="nav-menu">
        <li><a href="/firma/"{cur('firma')}>La firma</a></li>
        <li><a href="/equipo/"{cur('equipo')}>El equipo</a></li>
        <li class="has-sub">
          <button type="button" aria-haspopup="true">Soluciones {ICON_CHEVRON}</button>
          <ul class="submenu">{sub}</ul>
        </li>
        <li><a href="/analisis/"{cur('analisis')}>Análisis</a></li>
        <li class="nav-cta"><a class="btn btn--primary" href="/contacto/"{cur('contacto')}>Contacto</a></li>
      </ul>
    </div>
  </div>
</header>'''

def footer_html():
    wa = (f'<li><a href="https://wa.me/{SITE["whatsapp"]}" data-whatsapp>WhatsApp</a></li>'
          if SITE["whatsapp"] else '')
    return f'''<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      {brand()}
      <p class="footer-claim">Defensa en fraude financiero por captación masiva y habitual.</p>
      <p class="footer-status"><span class="dot" aria-hidden="true"></span>{esc(SITE["hours"])}</p>
    </div>
    <div class="footer-col">
      <h4>Dirección</h4>
      <address class="footer-plain">{esc(SITE["address"])}</address>
      <h4>Horario</h4>
      <p class="footer-plain">{esc(SITE["hours"])}</p>
    </div>
    <div class="footer-col">
      <h4>Contacto</h4>
      <ul>
        <li><a href="tel:{SITE["phone_href"]}" data-pos="footer">{esc(SITE["phone_display"])}</a></li>
        <li><a href="mailto:{SITE["email"]}">{esc(SITE["email"])}</a></li>
        {wa}
      </ul>
    </div>
    <div class="footer-col">
      <h4>Navegación</h4>
      <ul>
        <li><a href="/firma/">La firma</a></li>
        <li><a href="/equipo/">El equipo</a></li>
        <li><a href="/analisis/">Análisis</a></li>
        <li><a href="/preguntas-frecuentes/">Preguntas frecuentes</a></li>
        <li><a href="/contacto/">Contacto</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-legal">
    <div class="container footer-legal-top">
      <span>© 2026 · {esc(SITE["name"])} · Todos los derechos reservados.</span>
      <span class="footer-legal-links">
        <a href="/aviso-de-privacidad/">Aviso de privacidad</a>
        <a href="/aviso-legal/">Aviso legal</a>
        <a href="/politica-de-cookies/">Política de cookies</a>
      </span>
    </div>
    <div class="container footer-legal-bottom">
      <span class="footer-disclaimer">La información publicada en este sitio tiene carácter informativo y no constituye asesoría jurídica ni genera relación profesional.</span>
    </div>
  </div>
</footer>'''

def mobile_bar_html():
    wa = (f'<a class="btn btn--ghost" href="https://wa.me/{SITE["whatsapp"]}" data-whatsapp data-pos="mobilebar">WhatsApp</a>'
          if SITE["whatsapp"] else
          '<a class="btn btn--ghost" href="/contacto/" data-pos="mobilebar">Escribir</a>')
    return f'''<div class="mobile-bar is-on">
  <a class="btn btn--primary" href="tel:{SITE["phone_href"]}" data-pos="mobilebar">Llamar</a>
  {wa}
</div>'''

def burst_svg():
    import math
    parts = []
    N = 64
    for i in range(N):
        ang = 2 * math.pi * i / N
        r1 = 10
        r2 = 92 + (i % 8) * 12
        x1 = 140 + math.cos(ang) * r1; y1 = 140 + math.sin(ang) * r1
        x2 = 140 + math.cos(ang) * r2; y2 = 140 + math.sin(ang) * r2
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="currentColor" stroke-width="0.7"/>')
        parts.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="1.3" fill="currentColor"/>')
    return ('<svg class="burst" viewBox="0 0 280 280" fill="none" aria-hidden="true" '
            'style="color:var(--accent)">' + "".join(parts) + '</svg>')


def pixels_strip(n=48, on_every=5):
    cells = "".join(
        f'<i class="{"on" if (k % on_every == 0 or k % on_every == 1) else ""}"></i>'
        for k in range(n))
    return f'<div class="pixel-strip"><div class="container"><div class="pixels" aria-hidden="true">{cells}</div></div></div>'


def convergence_svg():
    # Cinco trazos que convergen a un punto (traducción del isotipo a diagrama).
    import math
    parts = []
    cx, cy = 200, 150
    for i in range(5):
        ang = math.radians(-90 + i * 72)
        x = cx + math.cos(ang) * 130
        y = cy + math.sin(ang) * 110
        parts.append(f'<path class="trace-on" d="M {x:.0f} {y:.0f} L {cx} {cy}"/>')
        parts.append(f'<circle class="node" cx="{x:.0f}" cy="{y:.0f}" r="7"/>')
    parts.append(f'<circle class="dot" cx="{cx}" cy="{cy}" r="9"/>')
    return ('<svg class="circuit" viewBox="0 0 400 300" fill="none" aria-hidden="true" '
            'style="max-width:520px;margin-inline:auto">' + "".join(parts) + '</svg>')


def globe_svg():
    import math
    cx, cy, R = 200, 150, 120
    dots = []
    for lat in range(-80, 81, 12):
        ry = math.sin(math.radians(lat))
        rx = math.cos(math.radians(lat))
        for lon in range(0, 360, 10):
            cl = math.cos(math.radians(lon))
            if cl < -0.15:  # solo hemisferio visible
                continue
            x = cx + R * rx * math.sin(math.radians(lon))
            y = cy + R * ry
            op = 0.25 + 0.55 * max(0, cl)
            r = 1.1 + 0.7 * max(0, cl)
            dots.append(f'<circle class="pt" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" opacity="{op:.2f}"/>')
    ring = (f'<ellipse cx="{cx}" cy="{cy}" rx="{R+18}" ry="{(R+18)*0.32:.0f}" fill="none" '
            f'stroke="currentColor" stroke-width="1" opacity="0.25" transform="rotate(-18 {cx} {cy})"/>')
    return ('<svg class="media-svg" viewBox="0 0 400 300" fill="none" aria-hidden="true" '
            'preserveAspectRatio="xMidYMid slice">' + ring + "".join(dots) + '</svg>')


def wave_svg():
    import math
    W, H = 400, 300
    dots = []
    for li in range(9):
        base = 120 + li * 16
        amp = 26 - li * 1.2
        for xi in range(0, 80):
            x = xi / 79 * W
            y = base + amp * math.sin(xi / 79 * math.pi * 2.4 + li * 0.5)
            op = 0.18 + 0.5 * (xi / 79)
            dots.append(f'<circle class="pt" cx="{x:.1f}" cy="{y:.1f}" r="1.3" opacity="{op:.2f}"/>')
    return ('<svg class="media-svg" viewBox="0 0 400 300" fill="none" aria-hidden="true" '
            'preserveAspectRatio="xMidYMid slice">' + "".join(dots) + '</svg>')


def proceso_stepper():
    ov_verificar = ('<div class="sv-overlay"><b>Verificación de conflicto</b>'
                    '<div class="svc-row"><span>Consulta entrante</span><span class="ok">Afectado</span></div>'
                    '<div class="svc-row"><span>Proceso en curso</span><span class="bad">Investigado</span></div>'
                    '<div class="svc-flag">Misma intervención → se declina <span class="ok">✓</span></div></div>')
    ov_hechos = ('<div class="sv-overlay"><b>Expediente</b>'
                 '<div class="svc-line">Transferencias · 12 movimientos</div>'
                 '<div class="svc-line">Fechas · 2023 – 2024</div>'
                 '<div class="svc-line">Trazabilidad · reconstruida</div></div>')
    ov_actores = ('<div class="sv-overlay"><b>Posiciones vinculadas</b>'
                  '<div class="svc-tags"><span class="svc-tag">Administrador</span><span class="svc-tag">Revisor fiscal</span>'
                  '<span class="svc-tag">Contador</span><span class="svc-tag">Proveedor</span><span class="svc-tag">Beneficiario</span></div></div>')
    ov_rutas = ('<div class="sv-overlay"><b>Vías en paralelo</b>'
                '<div class="svc-row"><span>Administrativa</span><span class="ok">10 días</span></div>'
                '<div class="svc-row"><span>Penal</span><span class="ok">art. 316</span></div>'
                '<div class="svc-row"><span>Civil</span><span class="ok">patrimonio</span></div></div>')
    ov_converg = ('<div class="sv-overlay"><b>Cinco prácticas · un expediente</b>'
                  '<div class="svc-line">Contractual · Tributaria · Corporativa</div>'
                  '<div class="svc-line">Penal · Laboral</div>'
                  '<div class="svc-flag">El caso se construye en la <span class="ok">intersección</span></div></div>')
    steps = [
        ("01", "VERIFICAR", "Verificamos el conflicto antes de aceptar",
         "Cada consulta pasa por un protocolo interno: si la firma ya interviene en ese proceso por la orilla contraria, se declina y se explica por qué. Es la primera prueba de integridad.",
         burst_svg(), "Integridad", ov_verificar),
        ("02", "HECHOS", "Reconstruimos los hechos",
         "Qué ocurrió, con qué documentos, en qué fechas y con qué trazabilidad financiera del esquema. El caso se sostiene sobre el expediente, no sobre la versión.",
         wave_svg(), "Trazabilidad", ov_hechos),
        ("03", "ACTORES", "Ubicamos a cada actor",
         "Quién ocupó cada posición —captador, administrador, revisor, contador, proveedor, afectado— y qué consecuencia jurídica arrastra. La defensa empieza por saber si usted debe estar ahí.",
         globe_svg(), "Posiciones", ov_actores),
        ("04", "RUTAS", "Ordenamos las tres vías",
         "Qué vías están abiertas, cuáles ya precluyeron y en qué orden conviene activarlas. Administrativa, penal y civil corren autónomas y concurrentes.",
         wave_svg(), "Estrategia", ov_rutas),
        ("05", "CONVERGENCIA", "Cinco prácticas, un expediente",
         "Los cinco socios trabajan el mismo caso desde sus ramas del derecho. El resultado no se reparte por especialidad: se construye en la intersección.",
         convergence_svg(), "Método", ov_converg),
    ]
    rail = "".join(f'<li class="{"on" if i == 0 else ""}">PASO 0{i + 1}</li>' for i in range(len(steps)))
    steps_html = ""
    for i, (num, chip, h, d, media, tag, overlay) in enumerate(steps):
        active = " active" if i == 0 else ""
        steps_html += f'''<div class="step{active}" data-i="{i}">
  <div class="step-visual">{media}</div>
  <div class="step-body">
    <span class="step-chip">{chip}</span>
    <h2>{esc(h)}</h2>
    <p>{esc(d)}</p>
    <div class="stepper-cta">{agendar_btn("Agendar una consulta")}<a class="btn btn--ghost" href="/firma/">Cómo trabajamos</a></div>
  </div>
</div>'''
    return f'''<section class="stepper" id="metodo">
  <div class="section stepper-intro"><div class="container tc">
    <p class="eyebrow">Por qué esta firma</p>
    <h2 style="max-width:18ch">El método, paso a paso</h2>
    <p class="lead" style="margin-top:1rem;max-width:56ch">No hay atajos ni promesas: hay un método. Así se construye un caso de fraude financiero en Veraly.</p>
  </div></div>
  <div class="stepper-track">
    <div class="stepper-sticky"><div class="stepper-inner">
      {steps_html}
      <ol class="stepper-rail" aria-hidden="true">{rail}</ol>
    </div></div>
  </div>
</section>'''


def marco_reveal():
    phrases = [
        "No perseguimos casos. || Trabajamos figuras jurídicas.",
        "Cada intervención se ordena sobre un marco normativo preciso.",
        "Decreto 4334, artículos 316 y 316A, y la jurisprudencia que los interpreta.",
    ]
    def words(s):
        # "||" fuerza un salto de línea (sin contar como palabra en el reveal).
        return " ".join(
            "<br>" if w == "||" else f'<span class="w">{esc(w)}</span>'
            for w in s.split(" "))
    phr = "".join(
        f'<p class="reveal-phrase{" active" if i == 0 else ""}" data-i="{i}">{words(s)}</p>'
        for i, s in enumerate(phrases))
    # URLs oficiales (TODO: verificar/ajustar por el despacho — decisión pendiente).
    cards = [
        ("Decreto 4334 / 2008", "Intervención", "http://www.secretariasenado.gov.co/senado/basedoc/decreto_4334_2008.html"),
        ("Art. 316 CP", "Captación masiva", "http://www.secretariasenado.gov.co/senado/basedoc/ley_0599_2000_pr012.html"),
        ("Art. 316A CP", "No reintegro", "http://www.secretariasenado.gov.co/senado/basedoc/ley_0599_2000_pr012.html"),
        ("Decreto 1981 / 1988", "Umbrales", "http://www.secretariasenado.gov.co/senado/basedoc/decreto_1981_1988.html"),
        ("Ley 1902 / 2018", "Plan de desmonte", "http://www.secretariasenado.gov.co/senado/basedoc/ley_1902_2018.html"),
        ("Sentencia C‑145 / 2009", "Presunciones", "https://www.corteconstitucional.gov.co/relatoria/2009/C-145-09.htm"),
    ]
    rc = "".join(
        f'<a class="rc" href="{u}" target="_blank" rel="noopener" data-norma="{esc(k)}">'
        f'<span class="t-k">{esc(k)}</span><span class="t-d">{esc(d)}</span>'
        f'<span class="rc-go" aria-hidden="true">Ver norma <i>↗</i></span></a>'
        for k, d, u in cards)
    return f'''<section class="reveal" id="marco">
  <div class="reveal-track">
    <div class="reveal-sticky">
      <p class="eyebrow reveal-eyebrow">El marco que trabajamos</p>
      <div class="reveal-phrases">{phr}</div>
      <div class="reveal-cards" aria-hidden="true">{rc}</div>
    </div>
  </div>
</section>'''


def agendar_btn(label="Agendar una consulta", primary=True):
    cls = "btn btn--primary" if primary else "btn btn--ghost"
    return f'<a class="{cls}" href="#agendar" data-cal data-pos="cta">{esc(label)}</a>'


def assistant_html():
    # Asistente guiado (determinista). El flujo vive en main.js; aquí solo el chasis.
    return '''<div class="asst" id="asst" aria-live="polite">
  <button class="asst-launch" id="asst-launch" aria-expanded="false" aria-controls="asst-panel">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-8.5 8.5 8.5 8.5 0 0 1-3.6-.8L3 21l1.9-5.4A8.5 8.5 0 1 1 21 11.5z"/></svg>
    <span>¿En qué le ayudamos?</span>
  </button>
  <div class="asst-panel" id="asst-panel" role="dialog" aria-label="Asistente de orientación" hidden>
    <div class="asst-head">
      <span class="asst-title">Orientación rápida</span>
      <button class="asst-close" id="asst-close" aria-label="Cerrar">&times;</button>
    </div>
    <div class="asst-body" id="asst-body"></div>
    <p class="asst-legal">Información general, no asesoría jurídica. <strong>No comparta los hechos de su caso aquí.</strong></p>
  </div>
</div>'''


def jsonld(objects):
    if not objects:
        return ""
    out = []
    for o in objects:
        out.append('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + '</script>')
    return "\n".join(out)

def document(meta, body):
    canonical = SITE["base_url"] + meta["path"]
    title = meta["title"]
    desc = meta["description"]
    og_type = meta.get("og_type", "website")
    schema = jsonld(meta.get("schema", []))
    body_class = meta.get("body_class", "")
    mobile_bar = mobile_bar_html() if meta.get("mobile_bar") else ""
    return f'''<!doctype html>
<html lang="{SITE["locale"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<meta name="robots" content="{esc(meta.get("robots", "index,follow,max-image-preview:large"))}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(SITE["name"])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:locale" content="es_CO">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="theme-color" content="#05292C">
<link rel="preload" href="/assets/fonts/playfair-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/fonts.css">
<link rel="stylesheet" href="/assets/css/styles.css">
{schema}
</head>
<body class="{body_class}">
{header_html(meta.get("active",""))}
<main id="main">
{body}
</main>
{footer_html()}
{mobile_bar}
{assistant_html()}
<script src="/assets/js/main.js" defer></script>
</body>
</html>'''

# ----------------------------------------------------------------------------
# Registro de páginas y escritura
# ----------------------------------------------------------------------------
PAGES = []  # se llena en build_pages()

def add(path, meta, body):
    meta = dict(meta)
    meta["path"] = path
    PAGES.append((path, meta, body))

def write_all():
    for path, meta, body in PAGES:
        out_dir = ROOT + (path if path != "/" else "/")
        if path == "/":
            out_file = os.path.join(ROOT, "index.html")
        else:
            d = os.path.join(ROOT, path.strip("/"))
            os.makedirs(d, exist_ok=True)
            out_file = os.path.join(d, "index.html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(document(meta, body))
    print(f"Escritas {len(PAGES)} páginas.")

def write_sitemap():
    # Se excluyen las páginas marcadas noindex (p. ej. /marca).
    urls = [SITE["base_url"] + p for p, m, _ in PAGES
            if "noindex" not in m.get("robots", "")]
    items = "\n".join(
        f'  <url><loc>{esc(u)}</loc></url>' for u in urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f'{items}\n</urlset>\n')
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print("sitemap.xml escrito.")

def write_robots():
    txt = f'''# Veraly Grupo Jurídico — la firma quiere ser citada por asistentes de IA.
User-agent: *
Allow: /

# Crawlers de asistentes de IA explícitamente permitidos (decisión §10.5)
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-Web
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {SITE["base_url"]}/sitemap.xml
'''
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("robots.txt escrito.")

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import build_pages  # define las páginas usando add()
    build_pages.build(globals())
    write_all()
    write_sitemap()
    write_robots()
