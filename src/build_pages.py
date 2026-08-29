# -*- coding: utf-8 -*-
"""Definición del contenido de cada página. Copy final de la especificación v1.0."""

def build(g):
    add = g["add"]; esc = g["esc"]; SITE = g["SITE"]
    SOCIOS = g["SOCIOS"]; ARTICLES = g["ARTICLES"]; SITUACIONES = g["SITUACIONES"]
    socio_by_slug = g["socio_by_slug"]; TEMAS = g["TEMAS"]; jsonld = g["jsonld"]
    PRACTICAS = g["PRACTICAS"]; agendar = g["agendar_btn"]
    burst = g["burst_svg"]; pixels = g["pixels_strip"]; convergence = g["convergence_svg"]
    globe = g["globe_svg"]; wave = g["wave_svg"]
    stepper = g["proceso_stepper"]; marco = g["marco_reveal"]
    B = SITE["base_url"]

    # -------- helpers de componentes --------
    def section(inner, cls="", tight=False):
        c = "section" + (" section--tight" if tight else "")
        if cls:
            c += " " + cls
        return f'<section class="{c}"><div class="container">{inner}</div></section>'

    def crumbs(items):
        # items: list of (label, href|None)
        parts = []
        for i, (label, href) in enumerate(items):
            if href:
                parts.append(f'<a href="{href}">{esc(label)}</a>')
            else:
                parts.append(esc(label))
            if i < len(items) - 1:
                parts.append('<span>›</span>')
        return f'<nav class="crumbs container" aria-label="Migas de pan">{"".join(parts)}</nav>'

    def faq_block(items):
        # items: list of (question, answer_html)
        rows = "".join(
            f'<details><summary>{esc(q)}</summary><div class="faq-a">{a}</div></details>'
            for q, a in items)
        return f'<div class="faq">{rows}</div>'

    def faq_schema(items):
        return {
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": re_text(a)}}
                for q, a in items]
        }

    def re_text(htmls):
        import re
        return re.sub(r"<[^>]+>", "", htmls).strip()

    def contact_form(perfil, submit_label="Enviar", compact=False):
        wa = (f'<a class="btn btn--ghost" href="https://wa.me/{SITE["whatsapp"]}" data-whatsapp data-pos="form">Escribir por WhatsApp</a>'
              if SITE["whatsapp"] else
              f'<a class="btn btn--ghost" href="mailto:{SITE["email"]}" data-pos="form">Escribir por correo</a>')
        return f'''<form class="form-wrap" data-veraly-form data-perfil="{perfil}" novalidate>
  <p class="form-note">Pedimos tres datos: su nombre, una vía de contacto y una línea de contexto. <strong>No escriba los hechos de su caso aquí.</strong> Los detalles se conversan; no necesitan quedar por escrito antes de que exista relación profesional.</p>
  <div class="field">
    <label for="{perfil}-nombre">Nombre</label>
    <input type="text" id="{perfil}-nombre" name="nombre" required minlength="2" autocomplete="name">
    <p class="field-error">Indique su nombre (mínimo 2 caracteres).</p>
  </div>
  <div class="field">
    <label for="{perfil}-contacto">Vía de contacto <span class="hint">Correo o teléfono</span></label>
    <input type="text" id="{perfil}-contacto" name="contacto" required data-validate="contact" autocomplete="email">
    <p class="field-error">Indique un correo o teléfono válido.</p>
  </div>
  <div class="field">
    <label for="{perfil}-contexto">Una línea de contexto <span class="hint">Opcional · máx. 200 caracteres</span></label>
    <input type="text" id="{perfil}-contexto" name="contexto" maxlength="200" data-maxcount="200" aria-describedby="{perfil}-count">
    <p class="char-count" id="{perfil}-count">0 / 200</p>
  </div>
  <div class="check">
    <input type="checkbox" id="{perfil}-auth" name="autorizacion" required>
    <label for="{perfil}-auth">Autorizo el tratamiento de mis datos personales conforme a la <a href="/aviso-de-privacidad/">política de tratamiento de datos</a> (Ley 1581 de 2012).</label>
  </div>
  <button type="submit" class="btn btn--primary">{submit_label}</button>
  <div class="form-status" role="status" aria-live="polite"></div>
</form>'''

    def trust_list():
        return '''<ul class="trust-list">
  <li>Respondemos en un plazo máximo de 24 horas hábiles.</li>
  <li>Toda consulta pasa por verificación previa de conflicto de interés antes de aceptarse.</li>
  <li>Sus datos se tratan conforme a la Ley 1581 de 2012. <a class="textlink" href="/aviso-de-privacidad/">Aviso de privacidad</a>.</li>
</ul>'''

    def conflict_block(text):
        return f'<div class="conflict"><p>{text}</p></div>'

    def person_schema(s):
        return {
            "@context": "https://schema.org", "@type": "Person",
            "name": s["nombre"], "jobTitle": "Socio · " + s["practica"],
            "worksFor": {"@type": "LegalService", "name": SITE["name"]},
            "url": B + "/equipo/" + s["slug"] + "/"
        }

    def breadcrumb_schema(items):
        # items: (name, url|None)
        return {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n,
                 **({"item": B + u} if u else {})}
                for i, (n, u) in enumerate(items)]
        }

    def service_schema(name, description, url, service_type, area="Colombia"):
        # Cada landing de situación es un Service prestado por la LegalService.
        return {
            "@context": "https://schema.org", "@type": "Service",
            "name": name, "description": description,
            "serviceType": service_type, "url": B + url,
            "areaServed": {"@type": "Country", "name": area},
            "provider": {"@type": "LegalService", "name": SITE["name"], "url": B + "/"},
        }

    # =====================================================================
    # HOME
    # =====================================================================
    situ_data = [
        ("Perdí dinero en un esquema de captación", "Vías administrativa, penal y civil, y los plazos que corren desde la toma de posesión.",
         "/afectados-por-captacion-masiva/", "afectado", "Afectado", "Recuperación", globe()),
        ("Me investigan o me vincularon", "Defensa en los tres frentes para investigados, administradores, revisores y proveedores.",
         "/defensa-en-captacion-masiva/", "investigado", "Investigado o vinculado", "Defensa", wave()),
        ("Mi empresa recauda de muchas personas", "Revisión de encuadre frente a los umbrales de captación antes de que la revise una superintendencia.",
         "/cumplimiento-en-recaudo-masivo/", "empresa", "Empresa", "Cumplimiento", globe()),
    ]
    situ_cards = ""
    for t, sub, url, tag, label, pill, media in situ_data:
        situ_cards += f'''<a class="acard" href="{url}" data-situacion="{tag}">
  <span class="acard-label">{esc(label)}</span>
  <h3 class="acard-title">{esc(t)}</h3>
  <p class="acard-desc">{esc(sub)}</p>
  <span class="acard-tag">{esc(pill)}</span>
  <div class="acard-media">{media}</div>
</a>'''

    # Tres vías como filas numeradas alternadas
    vias = [
        ("01", "VÍA ADMINISTRATIVA", "Ante la Superintendencia de Sociedades",
         "Procedimiento del Decreto 4334 de 2008. La toma de posesión tiene efectos de cosa juzgada frente a todos y es de única instancia: no hay segunda oportunidad procesal.", wave()),
        ("02", "VÍA PENAL", "Artículos 316 y 316A del Código Penal",
         "Captación masiva y habitual, con prisión de 120 a 240 meses, y el tipo autónomo de no reintegro. A ellos suelen sumarse estafa agravada, lavado de activos y concierto para delinquir.", globe()),
        ("03", "VÍA CIVIL", "Responsabilidad patrimonial",
         "Persigue el patrimonio personal de administradores, revisores fiscales, contadores y vinculados solventes por el faltante que la masa de la intervención no alcanza a cubrir.", wave()),
    ]
    vias_rows = ""
    for i, (num, eyb, h, d, media) in enumerate(vias):
        media_html = (f'<div class="fr-media"><div class="fr-par">{media}</div>'
                      f'<span class="fr-index" aria-hidden="true">{num}</span></div>')
        text_html = (f'<div class="fr-text">'
                     f'<p class="fr-eyebrow">{eyb}</p><h2>{esc(h)}</h2>'
                     f'<p class="lead" style="margin-top:1rem;color:var(--dim)">{esc(d)}</p></div>')
        inner = (media_html + text_html) if i % 2 == 0 else (text_html + media_html)
        vias_rows += f'<div class="frow">{inner}</div>'

    prac_cards = ""
    for pr in PRACTICAS:
        prac_cards += (f'<div class="bigcard"><span class="bc-label">Práctica</span>'
                       f'<h3>{esc(pr["rama"])}</h3><p>{esc(pr["aporte"])}</p></div>')

    conf = [
        ("3", "Vías en paralelo", "Administrativa, penal y civil, trabajadas a la vez sobre el mismo expediente."),
        ("5", "Prácticas del derecho", "Cinco socios aportan cinco ramas al mismo caso; se construye en la intersección."),
        ("24 h", "Tiempo de respuesta", "Respondemos toda consulta en un máximo de 24 horas hábiles, tras verificar el conflicto."),
        ("0", "Promesas de resultado", "No prometemos desenlace judicial. Se promete rigor, criterio y trabajo — con los límites dichos en voz alta."),
    ]
    conf_cards = ""
    for big, label, d in conf:
        conf_cards += (f'<div class="bigcard"><span class="bc-big">{esc(big)}</span>'
                       f'<span class="bc-label">{esc(label)}</span><p>{esc(d)}</p></div>')

    norms = [
        ("Decreto 4334 / 2008", "Intervención"), ("Art. 316 CP", "Captación masiva"),
        ("Art. 316A CP", "No reintegro"), ("Decreto 1981 / 1988", "Umbrales"),
        ("Ley 1902 / 2018", "Plan de desmonte"), ("Sentencia C‑145 / 2009", "Presunciones"),
        ("Supersociedades", "Competencia privativa"), ("Ley 1581 / 2012", "Datos personales"),
    ]
    tiles = "".join(
        f'<div class="tile"><span class="t-k">{esc(k)}</span><span class="t-d">{esc(d)}</span></div>'
        for k, d in norms)

    art_home = ""
    for a in ARTICLES[:3]:
        art_home += f'''<a href="/analisis/{a["slug"]}/">
  <span class="tag">{esc(a["tema"])}</span>
  <span><span class="t">{esc(a["h1"])}</span><span class="d">{esc(a["desc"])}</span></span>
</a>'''

    home_body = f'''
<section class="hero-full">
  <div class="hero-bg" aria-hidden="true"><div class="drape"></div><div class="sphere"></div></div>
  <div class="container hero-inner">
    <div class="hero-left">
      <h1>Defensa en<br>fraude financiero.</h1>
      <p class="hero-kicker">Captación masiva y habitual.</p>
    </div>
    <div class="hero-right">
      <p class="desc">Los procesos por captación avanzan por tres vías —administrativa, penal y civil—, autónomas y concurrentes. Las trabajamos las tres en paralelo, sobre el mismo expediente.</p>
      <div class="cta-row">
        {agendar("Agendar una consulta")}
        <a class="btn btn--ghost" href="#situaciones">Ver mi situación</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="situaciones">
  <div class="container">
    <div class="tc">
      <p class="eyebrow">Encaminar por situación</p>
      <h2 style="max-width:20ch">Tres situaciones distintas, tres rutas distintas</h2>
      <p class="lead" style="margin-top:1rem;max-width:56ch">Un mismo esquema de captación produce problemas jurídicos opuestos según el lugar que se ocupe en él. La ruta empieza por reconocer el suyo.</p>
    </div>
    <div class="acards">{situ_cards}</div>
    <div class="conflict-note">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6l7-3z"/><path d="M9.5 12l1.8 1.8L15 10"/></svg>
      <p>El despacho <strong>no representa simultáneamente</strong> a afectados y a vinculados dentro de un mismo proceso de intervención. Cada consulta pasa por una verificación previa de conflicto antes de aceptarse.</p>
    </div>
  </div>
</section>

<section class="section band">
  <div class="container">
    <p class="eyebrow">Las tres vías</p>
    <h2 style="max-width:22ch">Tres responsabilidades que corren al mismo tiempo</h2>
    <div style="margin-top:1.4rem">{vias_rows}</div>
  </div>
</section>

<section class="section">
  <div class="container stack">
    <div class="stack-head">
      <p class="eyebrow">El equipo</p>
      <h2>Cinco prácticas, un mismo caso</h2>
      <p class="lead" style="margin-top:1rem">La convergencia no es una declaración: es la composición de la firma. Cinco socios aportan cinco ramas del derecho al mismo expediente.</p>
      <div style="margin:1.6rem 0">{convergence()}</div>
      <div class="cta-row"><a class="btn btn--ghost" href="/equipo/">Por qué cinco prácticas</a></div>
    </div>
    <div class="stack-cards">{prac_cards}</div>
  </div>
</section>

{stepper()}

{marco()}

<section class="hero-full" style="min-height:auto;justify-content:center">
  <div class="hero-bg" aria-hidden="true"><div class="drape"></div><div class="sphere"></div></div>
  <div class="container">
    <p class="eyebrow">Contacto</p>
    <h2 style="font-size:clamp(2rem,1.3rem+3vw,3.6rem);max-width:22ch">Cuando un fraude financiero atraviesa una situación, la claridad jurídica es el primer paso.</h2>
    <p class="lead" style="margin-top:1.2rem;max-width:58ch">Una primera conversación sirve para saber si hay caso, qué vías están abiertas y qué plazos corren. No requiere aportar documentos ni tomar ninguna decisión.</p>
    <div class="cta-row">
      {agendar("Agendar una consulta")}
      <a class="btn btn--ghost" href="/contacto/">Escribir</a>
      <a class="btn btn--ghost" href="tel:{SITE["phone_href"]}" data-pos="home">Llamar</a>
    </div>
  </div>
</section>
'''

    home_schema = [
        {
            "@context": "https://schema.org", "@type": "LegalService",
            "name": SITE["name"],
            "description": "Despacho boutique colombiano especializado en captación masiva y habitual: defensa administrativa, penal y civil, y recuperación de afectados.",
            "url": B + "/",
            "areaServed": {"@type": "Country", "name": "Colombia"},
            "knowsAbout": ["Captación masiva y habitual", "Fraude financiero",
                           "Decreto 4334 de 2008", "Artículo 316 del Código Penal",
                           "Superintendencia de Sociedades"],
            "email": SITE["email"],
            "telephone": SITE["phone_display"],
            "address": {"@type": "PostalAddress", "addressCountry": "CO",
                        "streetAddress": SITE["address"]},
        },
        {
            "@context": "https://schema.org", "@type": "WebSite",
            "name": SITE["name"], "url": B + "/",
            "inLanguage": "es-CO",
            "publisher": {"@type": "LegalService", "name": SITE["name"], "url": B + "/"},
        },
    ]
    add("/", {
        "title": "Veraly Grupo Jurídico · Defensa en fraude financiero",
        "description": "Despacho boutique colombiano especializado en captación masiva y habitual. Cinco socios, cinco ramas del derecho, un mismo caso.",
        "active": "", "schema": home_schema,
    }, home_body)

    # las demás páginas se agregan en módulos separados para mantener legible el archivo
    import build_pages_2, build_pages_3
    ctx = dict(g)
    ctx.update({"section": section, "crumbs": crumbs, "faq_block": faq_block,
                "faq_schema": faq_schema, "contact_form": contact_form,
                "trust_list": trust_list, "conflict_block": conflict_block,
                "person_schema": person_schema, "breadcrumb_schema": breadcrumb_schema,
                "service_schema": service_schema, "faq_block": faq_block,
                "re_text": re_text, "B": B})
    build_pages_2.build(ctx)
    build_pages_3.build(ctx)
