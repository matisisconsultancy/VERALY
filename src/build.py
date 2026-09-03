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
    "base_url": "https://veraly.com.co",
    "locale": "es-CO",
    "email": "contacto@veraly.com.co",
    "phone_display": "+57 322 512 6199",
    "phone_href": "+573225126199",
    "whatsapp": "573225126199",  # WhatsApp de la firma (mismo número de contacto)
    "address": "Calle 16 # 4-68, oficina 1204, Bogotá",
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
        f'<li><a href="{url}" data-situacion="{tag}"{cur(tag)}>{esc(t)}</a></li>'
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
      <a class="nav-cta-btn" href="/contacto/"{cur('contacto')}>Contacto<span class="nav-cta-ico" aria-hidden="true"></span></a>
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
    wa = (f'<a class="btn btn--ghost" href="https://wa.me/{SITE["whatsapp"]}" target="_blank" rel="noopener" data-whatsapp data-pos="footer">WhatsApp</a>'
          if SITE["whatsapp"] else '')
    soluciones = "".join(
        f'<a href="{url}">{esc(t)}</a>' for url, t, d, tag in SITUACIONES)
    return f'''<footer class="site-footer">
  <div class="container footer-top">
    <div class="footer-invite">
      <p class="eyebrow">Contacto</p>
      <p class="footer-lede">Hablemos de su caso<br>con la debida reserva.</p>
      <div class="footer-cta">
        {agendar_btn("Agendar una consulta")}
        {wa}
      </div>
    </div>
    <dl class="footer-meta">
      <div class="fm-row"><dt>Correo</dt><dd><a href="mailto:{SITE["email"]}">{esc(SITE["email"])}</a></dd></div>
      <div class="fm-row"><dt>Teléfono</dt><dd><a href="tel:{SITE["phone_href"]}" data-pos="footer">{esc(SITE["phone_display"])}</a></dd></div>
      <div class="fm-row"><dt>Oficina</dt><dd>{esc(SITE["address"])}</dd></div>
      <div class="fm-row"><dt>Horario</dt><dd>{esc(SITE["hours"])}</dd></div>
    </dl>
  </div>

  <div class="container footer-nav">
    <nav class="fn-col" aria-label="Navegación del pie">
      <h4>Navegación</h4>
      <a href="/firma/">La firma</a>
      <a href="/equipo/">El equipo</a>
      <a href="/analisis/">Análisis</a>
      <a href="/preguntas-frecuentes/">Preguntas frecuentes</a>
      <a href="/contacto/">Contacto</a>
    </nav>
    <nav class="fn-col" aria-label="Soluciones">
      <h4>Soluciones</h4>
      {soluciones}
    </nav>
    <nav class="fn-col" aria-label="Legal">
      <h4>Legal</h4>
      <a href="/aviso-de-privacidad/">Aviso de privacidad</a>
      <a href="/aviso-legal/">Aviso legal</a>
      <a href="/politica-de-cookies/">Política de cookies</a>
    </nav>
  </div>

  <div class="footer-wordmark" aria-hidden="true"><span>Veraly<i>.</i></span></div>

  <div class="container footer-baseline">
    <span class="fb-copy">© 2026 · {esc(SITE["name"])}</span>
    <span class="footer-disclaimer">La información publicada en este sitio tiene carácter informativo y no constituye asesoría jurídica ni genera relación profesional.</span>
  </div>
</footer>'''

def mobile_bar_html():
    wa = (f'<a class="btn btn--ghost" href="https://wa.me/{SITE["whatsapp"]}" data-whatsapp data-pos="mobilebar">WhatsApp</a>'
          if SITE["whatsapp"] else
          '<a class="btn btn--ghost" href="/contacto/" data-pos="mobilebar">Escribir</a>')
    return f'''<div class="mobile-bar is-on">
  {agendar_btn("Agendar cita")}
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
    steps = [
        ("01", "Verificar", "Verificamos el conflicto antes de aceptar",
         "Cada consulta pasa por un protocolo interno: si la firma ya interviene en ese proceso por la orilla contraria, se declina y se explica por qué. Es la primera prueba de integridad.",
         burst_svg()),
        ("02", "Hechos", "Reconstruimos los hechos",
         "Qué ocurrió, con qué documentos, en qué fechas y con qué trazabilidad financiera del esquema. El caso se sostiene sobre el expediente, no sobre la versión.",
         wave_svg()),
        ("03", "Actores", "Ubicamos a cada actor",
         "Quién ocupó cada posición, captador, administrador, revisor, contador, proveedor o afectado, y qué consecuencia jurídica arrastra. La defensa empieza por saber si usted debe estar ahí.",
         globe_svg()),
        ("04", "Rutas", "Ordenamos las tres vías",
         "Qué vías están abiertas, cuáles ya precluyeron y en qué orden conviene activarlas. Administrativa, penal y civil corren autónomas y concurrentes.",
         wave_svg()),
        ("05", "Convergencia", "Cinco prácticas, un expediente",
         "Los cinco socios trabajan el mismo caso desde sus ramas del derecho. El resultado no se reparte por especialidad: se construye en la intersección.",
         convergence_svg()),
    ]
    rail = "".join(f'<li class="{"on" if i == 0 else ""}"><span>0{i + 1}</span></li>' for i in range(len(steps)))
    steps_html = ""
    for i, (num, chip, h, d, media) in enumerate(steps):
        active = " active" if i == 0 else ""
        steps_html += f'''<div class="step{active}" data-i="{i}">
  <div class="step-visual">{media}</div>
  <div class="step-body">
    <p class="step-chip"><span class="step-n">{num}</span><span class="step-l">{esc(chip)}</span></p>
    <h2>{esc(h)}</h2>
    <p class="step-d">{esc(d)}</p>
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


def marco_reveal(eyebrow="El marco que trabajamos", phrases=None, cards=None, section_id="marco"):
    if phrases is None:
        phrases = [
            "No perseguimos casos. || Trabajamos figuras jurídicas.",
            "Cada intervención se ordena sobre un marco normativo preciso.",
            "Decreto 4334, artículos 316 y 316A, y la jurisprudencia que los interpreta.",
        ]
    if cards is None:
        # URLs oficiales (TODO: verificar/ajustar por la firma — decisión pendiente).
        cards = [
            ("Decreto 4334 / 2008", "Intervención", "http://www.secretariasenado.gov.co/senado/basedoc/decreto_4334_2008.html"),
            ("Art. 316 CP", "Captación masiva", "http://www.secretariasenado.gov.co/senado/basedoc/ley_0599_2000_pr012.html"),
            ("Art. 316A CP", "No reintegro", "http://www.secretariasenado.gov.co/senado/basedoc/ley_0599_2000_pr012.html"),
            ("Decreto 1981 / 1988", "Umbrales", "http://www.secretariasenado.gov.co/senado/basedoc/decreto_1981_1988.html"),
            ("Ley 1902 / 2018", "Plan de desmonte", "http://www.secretariasenado.gov.co/senado/basedoc/ley_1902_2018.html"),
            ("Sentencia C‑145 / 2009", "Presunciones", "https://www.corteconstitucional.gov.co/relatoria/2009/C-145-09.htm"),
        ]
    def words(s):
        # "||" fuerza un salto de línea (sin contar como palabra en el reveal).
        return " ".join(
            "<br>" if w == "||" else f'<span class="w">{esc(w)}</span>'
            for w in s.split(" "))
    phr = "".join(
        f'<p class="reveal-phrase{" active" if i == 0 else ""}" data-i="{i}">{words(s)}</p>'
        for i, s in enumerate(phrases))
    rc = "".join(
        f'<a class="rc" href="{u}" target="_blank" rel="noopener" data-norma="{esc(k)}">'
        f'<span class="t-k">{esc(k)}</span><span class="t-d">{esc(d)}</span>'
        f'<span class="rc-go" aria-hidden="true">Ver norma <i>↗</i></span></a>'
        for k, d, u in cards)
    cards_html = f'<div class="reveal-cards" aria-hidden="true">{rc}</div>' if cards else ""
    return f'''<section class="reveal" id="{section_id}">
  <div class="reveal-track">
    <div class="reveal-sticky">
      <p class="eyebrow reveal-eyebrow">{esc(eyebrow)}</p>
      <div class="reveal-phrases">{phr}</div>
      {cards_html}
    </div>
  </div>
</section>'''


def agendar_btn(label="Agendar una consulta", primary=True):
    cls = "btn btn--primary" if primary else "btn btn--ghost"
    return f'<a class="{cls}" href="#agendar" data-cal data-pos="cta">{esc(label)}</a>'


def assistant_html():
    # Botón flotante de WhatsApp, en color de marca (menta sobre teal).
    if not SITE["whatsapp"]:
        return ""
    return f'''<a class="wa-fab" href="https://wa.me/{SITE["whatsapp"]}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp" data-whatsapp data-pos="fab">
  <svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 .5C7.4.5.5 7.4.5 16c0 2.8.7 5.4 2 7.7L.5 31.5l8-2.1c2.2 1.2 4.8 1.9 7.5 1.9 8.6 0 15.5-6.9 15.5-15.5S24.6.5 16 .5zm0 28c-2.5 0-4.8-.7-6.8-1.8l-.5-.3-4.7 1.2 1.3-4.6-.3-.5C3.9 20.4 3.2 18.3 3.2 16 3.2 8.9 8.9 3.2 16 3.2S28.8 8.9 28.8 16 23.1 28.5 16 28.5zm7-9.6c-.4-.2-2.3-1.1-2.6-1.3-.4-.1-.6-.2-.9.2-.3.4-1 1.3-1.2 1.5-.2.2-.4.3-.8.1-.4-.2-1.6-.6-3.1-1.9-1.1-1-1.9-2.3-2.1-2.7-.2-.4 0-.6.2-.8.2-.2.4-.4.5-.7.2-.2.2-.4.3-.6.1-.3 0-.5 0-.7 0-.2-.9-2.1-1.2-2.9-.3-.7-.6-.6-.9-.7h-.7c-.2 0-.6.1-1 .5-.3.4-1.3 1.3-1.3 3.1s1.3 3.6 1.5 3.9c.2.3 2.6 4 6.3 5.6.9.4 1.6.6 2.1.8.9.3 1.7.2 2.3.1.7-.1 2.3-.9 2.6-1.8.3-.9.3-1.6.2-1.8-.1-.1-.3-.2-.7-.4z"/></svg>
  <span class="wa-fab-label">WhatsApp</span>
</a>'''


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
