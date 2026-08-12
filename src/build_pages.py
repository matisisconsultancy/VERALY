# -*- coding: utf-8 -*-
"""Definición del contenido de cada página. Copy final de la especificación v1.0."""

def build(g):
    add = g["add"]; esc = g["esc"]; SITE = g["SITE"]
    SOCIOS = g["SOCIOS"]; ARTICLES = g["ARTICLES"]; SITUACIONES = g["SITUACIONES"]
    socio_by_slug = g["socio_by_slug"]; TEMAS = g["TEMAS"]; jsonld = g["jsonld"]
    PRACTICAS = g["PRACTICAS"]; agendar = g["agendar_btn"]
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

    # =====================================================================
    # HOME
    # =====================================================================
    situ_cards = ""
    situ_data = [
        ("Perdí dinero en un esquema de captación",
         "Existen vías administrativas, penales y civiles para reclamar, y cada una tiene términos propios que corren desde la toma de posesión. Saber cuál aplica y en qué plazo es la primera decisión del caso.",
         "Ver la ruta del afectado", "/afectados-por-captacion-masiva/", "afectado"),
        ("Me investigan o me vincularon a una captadora",
         "La vinculación alcanza a administradores, socios, revisores fiscales, contadores y proveedores por el solo ejercicio del cargo durante el periodo de captación. La defensa se construye sobre la exclusión, la contradicción de presunciones y la prueba del origen lícito.",
         "Ver la ruta de la defensa", "/defensa-en-captacion-masiva/", "investigado"),
        ("Mi empresa recauda de muchas personas",
         "Fintech, crowdfunding, libranzas, factoring, multinivel y clubes de inversión operan cerca de los umbrales que configuran captación. Conviene revisar el encuadre antes de que lo revise una superintendencia.",
         "Ver la ruta preventiva", "/cumplimiento-en-recaudo-masivo/", "empresa"),
    ]
    for t, d, cta, url, tag in situ_data:
        situ_cards += f'''<a class="card card--link" href="{url}" data-situacion="{tag}">
  <h3>{esc(t)}</h3>
  <p>{esc(d)}</p>
  <span class="arrowlink">{esc(cta)}</span>
</a>'''

    practicas_home = ""
    for pr in PRACTICAS:
        practicas_home += f'''<div class="socio">
  <span class="practica">{esc(pr["rama"])}</span>
  <p style="color:var(--dim);margin:.3rem 0 0;font-size:var(--step-0)">{esc(pr["aporte"])}</p>
</div>'''

    art_home = ""
    for a in ARTICLES[:3]:
        art_home += f'''<a href="/analisis/{a["slug"]}/">
  <span class="tag">{esc(a["tema"])}</span>
  <span><span class="t">{esc(a["h1"])}</span><span class="d">{esc(a["desc"])}</span></span>
</a>'''

    home_body = f'''
{section(f"""
  <p class="eyebrow">Veraly Grupo Jurídico</p>
  <h1>Defensa en fraude financiero</h1>
  <p class="support">Despacho boutique colombiano especializado en captación masiva y habitual de dineros. Cinco socios, cinco ramas del derecho, un mismo caso.</p>
  <p class="desc">Los procesos por captación no autorizada avanzan al mismo tiempo por tres vías —administrativa, penal y civil— que en Colombia operan de forma autónoma y concurrente. Trabajamos las tres en paralelo, con las cinco prácticas de la firma leyendo el mismo expediente.</p>
  <div class="cta-row">
    {agendar("Agendar una consulta")}
    <a class="btn btn--ghost" href="#situaciones">Ver mi situación</a>
  </div>
""", cls="hero")}

<section class="section band" id="situaciones">
  <div class="container">
    <p class="eyebrow">Encaminar por situación</p>
    <h2>Tres situaciones distintas, tres rutas distintas</h2>
    <p class="lead" style="margin-top:1rem;max-width:60ch">Un mismo esquema de captación produce problemas jurídicos opuestos según el lugar que se ocupe en él. La ruta empieza por identificar cuál es el suyo.</p>
    <div class="doors">{situ_cards}</div>
    {conflict_block('El despacho <strong>no representa simultáneamente</strong> a afectados y a vinculados dentro de un mismo proceso de intervención. Cada consulta pasa por una verificación previa de conflicto antes de aceptarse.')}
  </div>
</section>

{section(f"""
  <p class="eyebrow">El método</p>
  <h2 style="max-width:20ch">Los casos de fraude financiero no necesitan un abogado. Requieren un equipo.</h2>
  <div class="prose" style="margin-top:1.4rem">
    <p>Un proceso por captación no es un problema penal con derivaciones. Es un problema simultáneamente administrativo, penal, civil, societario, tributario y laboral, en el que cada frente condiciona a los demás: lo que se acepta en una audiencia preliminar reaparece en la reclamación, y lo que se declara ante la Superintendencia reaparece en el juicio oral.</p>
    <p>Por eso los cinco socios de Veraly no se reparten los casos por especialidad. Trabajan el mismo expediente desde sus cinco ramas.</p>
  </div>
  <ul class="method-list">
    <li><strong>Hechos.</strong> Reconstrucción documental del esquema, de los flujos y de las fechas.</li>
    <li><strong>Actores.</strong> Identificación de quién ocupó cada posición y con qué consecuencia jurídica.</li>
    <li><strong>Rutas.</strong> Priorización de las vías administrativa, penal y civil según lo que el caso permite y el momento en que llega.</li>
  </ul>
  <div class="cta-row"><a class="arrowlink" href="/firma/">Cómo trabajamos</a></div>
""")}

<section class="section band">
  <div class="container">
    <p class="eyebrow">El equipo</p>
    <h2>Cinco prácticas, un mismo caso</h2>
    <p class="lead" style="margin-top:1rem;max-width:52ch">La convergencia no es una declaración: es la composición de la firma. Cinco socios aportan cinco ramas del derecho al mismo expediente.</p>
    <div class="socios" style="margin-top:1.8rem">{practicas_home}</div>
    <div class="cta-row"><a class="arrowlink" href="/equipo/">Por qué cinco prácticas</a></div>
  </div>
</section>

{section(f"""
  <p class="eyebrow">Análisis</p>
  <h2>Análisis reciente</h2>
  <p class="lead" style="margin-top:1rem;max-width:60ch">Publicamos sobre las figuras jurídicas del fraude financiero: cómo se estructuran, cómo se investigan y qué vías abren. Nunca sobre casos identificables.</p>
  <div class="editorial">{art_home}</div>
  <div class="cta-row"><a class="arrowlink" href="/analisis/">Ver todos los análisis</a></div>
""")}

<section class="section band-2">
  <div class="container">
    <p class="eyebrow">Contacto</p>
    <h2 style="max-width:24ch">Cuando un fraude financiero atraviesa una situación, la claridad jurídica es el primer paso.</h2>
    <p class="lead" style="margin-top:1.2rem;max-width:60ch">Una primera conversación sirve para saber si hay caso, qué vías están abiertas y qué plazos corren. No requiere aportar documentos ni tomar ninguna decisión.</p>
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
        }
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
                "re_text": re_text, "B": B})
    build_pages_2.build(ctx)
    build_pages_3.build(ctx)
