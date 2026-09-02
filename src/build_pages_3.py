# -*- coding: utf-8 -*-
"""Capa 2 (intención + editorial) y páginas legales."""

def build(g):
    add = g["add"]; esc = g["esc"]; SITE = g["SITE"]; ARTICLES = g["ARTICLES"]
    socio_by_slug = g["socio_by_slug"]; TEMAS = g["TEMAS"]
    section = g["section"]; crumbs = g["crumbs"]; faq_block = g["faq_block"]
    faq_schema = g["faq_schema"]; contact_form = g["contact_form"]; trust_list = g["trust_list"]
    breadcrumb_schema = g["breadcrumb_schema"]; B = g["B"]; agendar = g["agendar_btn"]
    service_schema = g["service_schema"]; faq_block = g["faq_block"]

    def acc(items):
        # items: (fase_id, titulo, cuerpo_html)
        rows = "".join(
            f'<details data-fase="{fid}"><summary>{esc(t)}</summary><div class="acc-body">{body}</div></details>'
            for fid, t, body in items)
        return f'<div class="accordion">{rows}</div>'

    # --- componentes reutilizables para las páginas de soluciones ---
    globe = g["globe_svg"]; wave = g["wave_svg"]

    def faq_sticky(items, title='Las preguntas que <span class="pr-accent">más nos hacen.</span>',
                   eyebrow="Preguntas frecuentes"):
        rows = "".join(
            f'<details class="faq-acc"><summary><span class="fa-n">{i:02d}</span>'
            f'<span class="fa-q">{esc(q)}</span>'
            f'<span class="fa-box" aria-hidden="true"></span></summary>'
            f'<div class="fa-a">{a}</div></details>'
            for i, (q, a) in enumerate(items, 1))
        return ('<section class="section faq-sticky-sec"><div class="container faq-sticky-grid">'
                '<div class="faq-sticky-l">'
                f'<p class="faq-pill"><span class="dot" aria-hidden="true"></span>{esc(eyebrow)}</p>'
                f'<h2 class="faq-sticky-title">{title}</h2></div>'
                f'<div class="faq-sticky-r">{rows}</div></div></section>')

    def sol_two(eyebrow_label, title_html, body_html, band=False, parallax=True):
        cls = "section band" if band else "section"
        ppx = " pr-parallax" if parallax else ""
        return (f'<section class="{cls}"><div class="container pr-two">'
                f'<div class="pr-two-l"><p class="eyebrow-num"><span class="n">§</span>{esc(eyebrow_label)}</p>'
                f'<h2 class="pr-big{ppx}">{title_html}</h2></div>'
                f'<div class="pr-two-r">{body_html}</div></div></section>')

    def sol_timeline(rows):
        media = [globe, wave]
        r = "".join(
            f'<div class="pr-tl-row"><span class="pr-tl-label">{esc(lbl)}</span>'
            f'<div class="pr-tl-body"><p class="pr-tl-desc">{esc(d)}</p></div>'
            f'<div class="pr-tl-media"><div class="pr-tl-par">{media[i % 2]()}</div></div></div>'
            for i, (lbl, d) in enumerate(rows))
        return f'<div class="pr-timeline">{r}</div>'

    def via_card(tag, title, desc, recup, scope):
        segs = "".join(f'<i class="{"on" if k < scope else ""}"></i>' for k in range(3))
        return (f'<div class="via-card reveal-up"><span class="via-tag">{esc(tag)}</span>'
                f'<h3>{esc(title)}</h3><p>{esc(desc)}</p>'
                f'<div class="via-recup"><span class="k">Qué recupera</span>'
                f'<span class="v">{esc(recup)}</span>'
                f'<div class="via-scope" aria-hidden="true">{segs}</div></div></div>')

    def plz_step(idx, num, unit, label, detail):
        return (f'<div class="plz-step"><span class="plz-ord">{idx:02d}</span>'
                f'<span class="plz-num"><span data-count="{num}">0</span>'
                f'<span class="u">{esc(unit)}</span></span>'
                f'<p class="plz-label">{esc(label)}</p><p class="plz-detail">{esc(detail)}</p></div>')

    def phase_tabs(items):
        # items: (etiqueta corta, título, cuerpo_html)
        tabs = "".join(
            f'<button type="button" class="ph-tab{" is-active" if i == 0 else ""}" data-ph="{i}">'
            f'<span class="ph-n">{i+1:02d}</span><span class="ph-l">{esc(lbl)}</span>'
            f'<span class="ph-go" aria-hidden="true">→</span></button>'
            for i, (lbl, title, body) in enumerate(items))
        panels = "".join(
            f'<div class="ph-panel{" is-active" if i == 0 else ""}" data-ph="{i}">'
            f'<h3 class="ph-title">{esc(title)}</h3>{body}</div>'
            for i, (lbl, title, body) in enumerate(items))
        return f'<div class="phase-tabs"><div class="ph-nav">{tabs}</div><div class="ph-panels">{panels}</div></div>'

    # =====================================================================
    # /afectados-por-captacion-masiva  (Perfil A)
    # =====================================================================
    afectados_faq = [
        ("¿Cuánto tiempo tengo para reclamar?",
         "<p>Dentro de la intervención administrativa, diez días comunes contados desde el aviso que el interventor publica en los dos días siguientes a la toma de posesión. Fuera de ese trámite, los términos dependen de la vía: la penal y la civil tienen sus propios plazos de prescripción.</p>"),
        ("¿Puedo recuperar los intereses que me prometieron?",
         "<p>Por la vía administrativa, no: la devolución tiene techo en el capital entregado. Los rendimientos y perjuicios solo se persiguen por la vía penal, en el incidente de reparación integral, o por la vía civil.</p>"),
        ("¿Y si entregué el dinero en efectivo y no tengo comprobante?",
         "<p>Dificulta la reclamación pero no la cierra automáticamente. La trazabilidad se puede reconstruir con otros elementos —transferencias parciales, comunicaciones, registros del propio esquema, declaraciones de terceros—. Es trabajo probatorio, y conviene empezarlo antes de que corra el término.</p>"),
        ("¿Qué diferencia hay entre estafa y captación masiva?",
         "<p>Son tipos penales distintos. La captación masiva, además, activa un procedimiento administrativo especial ante la Superintendencia de Sociedades con un mecanismo de devolución propio que la estafa no tiene. La calificación correcta cambia la estrategia completa.</p>"),
        ("¿Qué es un plan de desmonte y me conviene votarlo?",
         "<p>Es una propuesta de devolución voluntaria y ordenada conforme a un cronograma. Bajo la Ley 1902 de 2018 requiere aval de la Superintendencia y respaldo del 75 % de los afectados. Conviene o no según lo que ofrezca frente a lo que la prorrata alcanzaría, y según los plazos: hay planes que protegen la igualdad entre afectados y otros que la sacrifican.</p>"),
        ("¿Qué pasa si el dinero ya no existe?",
         "<p>Es la pregunta correcta y no siempre tiene respuesta inmediata. Cuando la masa no alcanza, la vía civil persigue el patrimonio personal de administradores y vinculados solventes, y las acciones de simulación y pauliana permiten reintegrar bienes distraídos antes de la intervención. Si hay algo que perseguir, se persigue; si no lo hay, se dice.</p>"),
        ("¿Cuánto cuesta consultar?",
         "<p>La primera conversación sirve para determinar si hay caso y qué vías están abiertas. Las condiciones del encargo se definen después y por escrito.</p>"),
    ]
    afectados_acc = phase_tabs([
        ("Antes de la intervención", "Antes de que se abra la intervención",
         "<ul><li>Denuncia administrativa y solicitud de intervención por hechos objetivos o notorios.</li>"
         "<li>Organización probatoria individual o del grupo: reconstrucción de entregas, trazabilidad y armado del expediente reclamable.</li>"
         "<li>Denuncia penal estructurada y acreditación como víctima.</li>"
         "<li>Solicitud de medidas cautelares penales sobre bienes, para evitar el vaciamiento patrimonial antes de la sentencia.</li>"
         "<li>Aseguramiento civil temprano frente a codeudores, avalistas y garantes no intervenidos, que no quedan cubiertos por la suspensión de ejecuciones.</li></ul>"),
        ("Durante la intervención", "Durante la intervención",
         "<ul><li>Reclamación de devolución dentro del término, con la formalidad que exige el trámite.</li>"
         "<li>Impugnación del reconocimiento cuando se rechaza o se acepta por menor valor.</li>"
         "<li>Exclusión de bienes propios aprehendidos por error en el inventario.</li>"
         "<li>Gestión de títulos valores y libranzas para acreditar tenencia legítima y prelación sobre los flujos.</li>"
         "<li>Evaluación y voto de planes de desmonte, que bajo la Ley 1902 de 2018 requieren el respaldo del 75 % de los afectados.</li>"
         "<li>Vigilancia activa de la intervención: prorrateos incompletos, recursos nuevos sin distribuir, gestión opaca del interventor.</li></ul>"),
        ("Después del fallo", "Después del fallo",
         "<ul><li>Representación de víctimas en el proceso penal, incluidas las salidas negociadas.</li>"
         "<li>Incidente de reparación integral: daño emergente, lucro cesante y perjuicio moral.</li>"
         "<li>Responsabilidad civil contra administradores, revisores fiscales, contadores y vinculados solventes.</li>"
         "<li>Reconstrucción de la prenda general por simulación, acción pauliana y revocatoria concursal.</li></ul>"),
    ])
    wa_a = (f'<a class="btn btn--ghost" href="https://wa.me/{SITE["whatsapp"]}" data-whatsapp data-pos="afectados">Escribir por WhatsApp</a>' if SITE["whatsapp"] else "")
    af_hero = (
        '<section class="sol-hero"><div class="container sol-hero-grid">'
        '<div class="sol-hero-main">'
        '<p class="eyebrow">Para el afectado</p>'
        '<h1 class="sol-h1">Recuperar lo que entregó <span class="pr-accent">tiene vías —y un reloj.</span></h1>'
        '<p class="sol-lede">Perder dinero en una pirámide o en un esquema de rendimientos no autorizado abre tres vías de recuperación, todas con plazos que empiezan a correr desde la toma de posesión.</p>'
        '<div class="cta-row">' + agendar("Agendar una consulta")
        + '<a class="btn btn--ghost" href="#formulario">Escribir a la firma</a></div>'
        '</div>'
        '<aside class="sol-hero-aside"><div class="sol-facts">'
        '<div class="sol-fact"><b>3</b><span>vías de recuperación: administrativa, penal y civil</span></div>'
        '<div class="sol-fact"><b>10<span class="u">días</span></b><span>para reclamar dentro de la intervención</span></div>'
        '<div class="sol-fact"><b>316<span class="u">CP</span></b><span>captación masiva y habitual, y no reintegro</span></div>'
        '</div></aside>'
        '</div></section>')
    af_stmt = (
        '<section class="section sol-stmt-sec"><div class="container sol-stmt-grid">'
        '<div><p class="eyebrow-num"><span class="n">§</span>El fenómeno</p>'
        '<h2 class="sol-stmt pr-parallax">Probablemente no fue una estafa. <span class="pr-accent">Fue captación masiva.</span></h2></div>'
        '<div class="sol-stmt-body">'
        '<p>La diferencia no es semántica. La estafa y la captación masiva son delitos distintos, con procesos distintos y con vías de recuperación distintas —y se usan como sinónimos incluso en la prensa.</p>'
        '<p>Hay <strong>captación masiva y habitual no autorizada</strong> cuando se reciben dineros del público sin autorización estatal, entregando a cambio bienes, servicios o rendimientos sin explicación financiera razonable: más de veinte personas, o más de cincuenta obligaciones, o mediación de ofertas masivas.</p>'
        '<p>Que su caso encuadre en esta figura lo cambia todo: activa un procedimiento administrativo especial ante la Superintendencia de Sociedades que no existe en la estafa común, y con él un mecanismo de devolución al que usted puede acceder.</p>'
        '</div></div></section>')
    _via_data = [
        ("Vía administrativa", "La reclamación dentro de la intervención",
         "Cuando la Superintendencia ordena la toma de posesión para devolver, se abre un trámite de reclamación a prorrata entre los afectados. Es la vía más rápida.",
         "El capital entregado"),
        ("Vía civil", "La responsabilidad de los solventes",
         "Cuando la masa no cubre el faltante, persigue el patrimonio de administradores, revisores, contadores y vinculados solventes; y reconstruye la prenda general.",
         "El patrimonio de los responsables"),
        ("Vía penal", "El incidente de reparación integral",
         "Tras la sentencia condenatoria se reclaman daño emergente, lucro cesante y perjuicios morales. Es la vía de mayor alcance: llega a lo que las demás dejan fuera."),
    ]
    _via_recup = ["El capital entregado", "El patrimonio de los responsables", "Capital, rendimientos y perjuicios"]
    _via_slides = "".join(
        f'<div class="via-slide{" active" if i == 0 else ""}" data-i="{i}">'
        f'<span class="via-idx">{i+1:02d} / 03</span>'
        f'<span class="via-tag">{esc(v[0])}</span>'
        f'<h3 class="via-h">{esc(v[1])}</h3>'
        f'<p class="via-d">{esc(v[2])}</p>'
        f'<div class="via-recup"><span class="k">Qué recupera</span><span class="v">{esc(_via_recup[i])}</span></div>'
        f'</div>'
        for i, v in enumerate(_via_data))
    _via_bars = "".join('<i></i>' for _ in range(3))
    af_vias_grid = (
        '<section class="via-sticky-sec"><div class="container">'
        '<p class="eyebrow-num"><span class="n">§</span>Las tres vías</p>'
        '<h2 class="pr-big">Tres vías, tres cosas distintas <span class="pr-accent">que se recuperan.</span></h2>'
        '</div>'
        '<div class="via-track"><div class="via-sticky"><div class="container via-stage">'
        f'<div class="via-slides">{_via_slides}</div>'
        '<div class="via-scopewrap" aria-hidden="true">'
        '<span class="via-scope-k">Alcance de la recuperación</span>'
        f'<div class="via-bars">{_via_bars}</div>'
        '<span class="via-scope-hint">Cada vía llega más lejos que la anterior.</span>'
        '</div>'
        '</div></div></div>'
        '<div class="container"><p class="lead" style="max-width:66ch;color:var(--dim)">La devolución administrativa tiene <strong>techo en el capital</strong>: los intereses y los perjuicios solo se recuperan por la vía civil o la penal. Las tres corren de forma autónoma —no hay que elegir una, hay que ordenarlas.</p></div>'
        '</section>')
    af_plazos = (
        '<section class="plz-sec plz-pin"><div class="plz-pin-track">'
        '<div class="plz-pin-sticky"><div class="container">'
        '<p class="eyebrow-num"><span class="n">§</span>El calendario</p>'
        '<div class="plz-head"><h2 class="plz-title">Los términos corren, <span class="pr-accent">y son cortos.</span></h2></div>'
        '<p class="plz-sub">Dentro de la intervención administrativa el calendario es estricto y se cuenta en días comunes desde la toma de posesión.</p>'
        '<div class="plz-track">'
        + plz_step(1, "2", "días", "El aviso", "El interventor publica el aviso dentro de los dos días siguientes a la toma de posesión.")
        + plz_step(2, "10", "días", "La reclamación", "Las solicitudes de devolución se presentan por escrito, con presentación personal y original del comprobante.")
        + plz_step(3, "20", "días", "La decisión", "La providencia que acepta o rechaza se profiere dentro de los veinte días siguientes.")
        + plz_step(4, "3", "días", "El recurso", "El recurso de reposición contra esa decisión se interpone dentro de los tres días siguientes.")
        + '</div>'
        '<p class="plz-note">La causa más frecuente de rechazo no es la falta de derecho: es <strong>la forma</strong> —comprobantes informales, copias sin original, entregas en efectivo sin rastro, o la simple pérdida del término.</p>'
        '</div></div></div></section>')
    af_grupo = sol_two(
        "Casos colectivos",
        'Cuando el grupo <span class="pr-accent">ya existe.</span>',
        "<p>Trabajar el caso de forma colectiva tiene ventajas concretas: la prueba se vuelve más sólida, un plan de desmonte se sostiene con peso real y el seguimiento de la intervención no depende de una sola persona. Si forma parte de un grupo, la primera conversación conviene tenerla con quien lo represente.</p>"
        '<p style="margin-top:1.2rem"><a class="arrowlink" href="/contacto/">Escribir en nombre de un grupo</a></p>',
        band=True, parallax=False)
    af_faq = faq_sticky(afectados_faq, title='Preguntas del <span class="pr-accent">afectado.</span>')
    afectados_body = f'''
{af_hero}

{af_stmt}

{af_vias_grid}

{af_plazos}

<section class="section">
  <div class="container">
    <p class="eyebrow-num"><span class="n">§</span>El acompañamiento</p>
    <h2 class="pr-big">El trabajo, <span class="pr-accent">por momento del proceso.</span></h2>
    <div style="margin-top:clamp(28px,3.4vw,48px)">{afectados_acc}</div>
  </div>
</section>

{af_grupo}

{af_faq}

<section class="section band-2" id="formulario">
  <div class="container">
    <h2>Una primera conversación</h2>
    <p class="lead" style="margin-top:1rem;max-width:56ch">No necesita traer documentos ni haber decidido nada. Sirve para saber si hay caso, qué vías siguen abiertas y qué plazos corren.</p>
    <div class="contact-grid" style="margin-top:1.6rem">
      <div>{contact_form("afectados", "Enviar")}
        <div class="cta-row">{agendar("Agendar una consulta")}<a class="btn btn--ghost" href="tel:{SITE["phone_href"]}" data-pos="afectados">Llamar</a>{wa_a}</div>
      </div>
      <aside>{trust_list()}
        <p style="margin-top:1.4rem"><a class="arrowlink" href="/firma/">Conocer cómo trabaja la firma</a></p>
        <p><a class="arrowlink" href="/equipo/">Conocer al equipo</a></p>
      </aside>
    </div>
  </div>
</section>
'''
    add("/afectados-por-captacion-masiva/", {
        "title": "Afectados por captación masiva: vías y plazos",
        "description": "Vías administrativa, penal y civil para reclamar tras una captación no autorizada, con los términos que corren desde la toma de posesión.",
        "active": "afectado", "og_type": "article", "body_class": "theme-light",
        "schema": [
            service_schema(
                "Recuperación para afectados por captación masiva",
                "Acompañamiento a afectados para reclamar por las vías administrativa, penal y civil tras una captación no autorizada.",
                "/afectados-por-captacion-masiva/", "Recuperación de recursos"),
            faq_schema(afectados_faq),
            breadcrumb_schema([("Inicio", "/"),
                ("Perdí dinero en un esquema", "/afectados-por-captacion-masiva/")]),
        ],
    }, afectados_body)

    # =====================================================================
    # /defensa-en-captacion-masiva  (Perfil B) — barra móvil fija
    # =====================================================================
    defensa_faq = [
        ("¿Me pueden vincular solo por haber sido revisor fiscal o contador?",
         "<p>El perímetro del artículo 5 alcanza esas posiciones, y existe además una presunción de participación por el ejercicio del cargo durante el periodo de captación. Es desvirtuable, y la solicitud de exclusión es precisamente la vía para hacerlo.</p>"),
        ("¿Qué diferencia hay entre el artículo 316 y el 316A?",
         "<p>El 316 tipifica la captación masiva y habitual, con prisión de 120 a 240 meses tras la Ley 1357 de 2009. El 316A es un tipo autónomo que sanciona el no reintegro, con pena de 96 a 180 meses. Son imputaciones distintas y admiten defensas distintas.</p>"),
        ("¿Se puede recurrir la decisión de toma de posesión?",
         "<p>El procedimiento del Decreto 4334 es de única instancia y sus decisiones tienen efectos de cosa juzgada frente a todos. Eso no significa que no haya control: existen recursos dentro del trámite, control judicial de las sanciones y, frente a vías de hecho, la acción de tutela.</p>"),
        ("¿La devolución voluntaria reduce la exposición penal?",
         "<p>La reparación y el reintegro tienen efecto en la justicia penal negociada. Cuánto, depende del momento procesal y de la estructura del acuerdo. Es una decisión que no debería tomarse mirando solo el frente penal.</p>"),
        ("¿Pueden alcanzar bienes de mi cónyuge o de mis sociedades?",
         "<p>Es habitual que se intenten, por la vía de la simulación y de la acción pauliana. La defensa se construye acreditando origen lícito y separación real de patrimonios, y es un trabajo probatorio que conviene empezar antes de que la demanda llegue.</p>"),
    ]
    defensa_acc = acc([
        ("previa", "Fase administrativa previa — antes de la declaratoria",
         "<p>Requerimientos, visitas y actuaciones de las Superintendencias que anteceden a la declaratoria de captación. Aquí se sustenta técnicamente el modelo de negocio y se acredita la explicación financiera razonable. Es la fase en la que todavía se puede evitar la declaratoria y la suspensión.</p>"
         "<ul><li>Defensa en la actuación administrativa previa y sustentación técnica del modelo.</li>"
         "<li>Recursos contra la orden de suspensión y las multas, y control judicial de la sanción.</li>"
         "<li>Plan de desmonte voluntario preintervención, cuando la toma de posesión es inminente.</li></ul>"),
        ("intervencion", "Fase de intervención — después de la toma de posesión",
         "<p>La toma de posesión trae nombramiento de agente interventor, remoción de administradores, congelación de activos, exigibilidad inmediata de créditos, suspensión de ejecutivos en curso y prohibición de iniciar nuevos.</p>"
         "<ul><li>Solicitud de exclusión y desintervención.</li>"
         "<li>Contradicción de las presunciones sobre recursos y sobre participación.</li>"
         "<li>Auditoría de trazabilidad y origen lícito de activos, con separación de patrimonios legítimos.</li>"
         "<li>Objeción al inventario valorado y controversia de avalúos.</li>"
         "<li>Suspensión de ejecuciones y cobros coactivos paralelos.</li>"
         "<li>Defensa frente a revocatorias e ineficacias promovidas por el interventor.</li>"
         "<li>Representación en audiencias y recursos de reposición, aclaración y adición.</li>"
         "<li>Acciones constitucionales frente a vías de hecho, en un trámite que es de única instancia.</li></ul>"),
        ("penal", "Fase penal",
         "<ul><li>Defensa en indagación e investigación: interrogatorios, allanamientos, capturas y actos urgentes.</li>"
         "<li>Audiencias preliminares: imputación, medida de aseguramiento y cautelares reales sobre bienes.</li>"
         "<li>Defensa técnica en juicio oral frente a acusaciones por captación, no reintegro, estafa o lavado.</li>"
         "<li>Ejecución penal: subrogados, prisión domiciliaria, libertad condicional y redenciones.</li></ul>"),
        ("civil", "Fase civil y patrimonial",
         "<ul><li>Defensa frente a demandas de afectados por el faltante.</li>"
         "<li>Responsabilidad de administradores, simulaciones y acciones paulianas contra el patrimonio del cónyuge, la familia o sociedades relacionadas.</li>"
         "<li>Conciliación y acuerdos de pago con afectados.</li></ul>"),
    ])
    wa_b = (f'<a class="btn btn--ghost" href="https://wa.me/{SITE["whatsapp"]}" data-whatsapp data-pos="defensa">Escribir por WhatsApp</a>' if SITE["whatsapp"] else "")
    defensa_body = f'''
{section(f"""
  <p class="eyebrow">Para el investigado o vinculado</p>
  <h1>Defensa en procesos por captación masiva y habitual</h1>
  <p class="support" style="max-width:56ch">Actuaciones administrativas ante la Superintendencia de Sociedades, defensa penal por los artículos 316 y 316A del Código Penal, y defensa patrimonial civil. Los tres frentes, en paralelo.</p>
  <p class="desc" style="max-width:58ch">Si hay requerimientos, visita administrativa, orden de suspensión, actos urgentes, captura o audiencia de imputación, el momento procesal define lo que todavía es posible.</p>
  <div class="cta-row">
    <a class="btn btn--primary" href="/contacto/">Escribir ahora</a>
    <a class="btn btn--ghost" href="tel:{SITE["phone_href"]}" data-pos="defensa-hero">Llamar</a>
  </div>
""", cls="hero")}

<section class="section band">
  <div class="container prose">
    <h2>La vinculación no se limita al captador</h2>
    <p>El artículo 5 del Decreto 4334 de 2008 alcanza a captadores, administradores —representantes legales y miembros de junta directiva—, socios, revisores fiscales, contadores, beneficiarios y demás personas vinculadas directa o indirectamente a la operación.</p>
    <p>En la práctica, esto significa que profesionales que prestaron un servicio puntual y correcto quedan dentro del perímetro de la intervención por el solo ejercicio del cargo durante el periodo de captación. Y también proveedores que contrataron de buena fe con la intervenida.</p>
    <p>Si usted está en ese perímetro, su defensa no empieza discutiendo los hechos del esquema: empieza discutiendo si debe estar ahí.</p>
  </div>
</section>

{section("""
  <h2>Dos presunciones que hay que desvirtuar</h2>
  <div class="prose" style="margin-top:1.2rem">
    <p><strong>Sobre los recursos.</strong> Dentro de la intervención se presume que todos los recursos aprehendidos provienen de la actividad ilícita. Es una presunción legal y, por tanto, desvirtuable —así lo precisó la Sentencia C-145 de 2009—, pero mientras no se desvirtúe opera contra el patrimonio del vinculado.</p>
    <p><strong>Sobre la participación.</strong> El régimen posterior hace recaer sobre administradores y vinculados una presunción de participación por el solo ejercicio del cargo durante el periodo de captación.</p>
    <p>Desvirtuarlas exige prueba positiva: trazabilidad y origen lícito de los activos, y acreditación de gestión diligente. No basta con negar.</p>
  </div>
""")}

<section class="section band">
  <div class="container">
    <h2>Dónde está su caso</h2>
    <p class="acc-note">Abra la fase en la que se encuentra. No necesita leer las demás.</p>
    {defensa_acc}
  </div>
</section>

{section("""
  <h2>El estándar que decide muchas exclusiones</h2>
  <div class="prose" style="margin-top:1.2rem">
    <p>El artículo 7, literal c, del Decreto 4334 permite devolver bienes de personas no vinculadas a la actividad. Y la Sentencia C-145 de 2009 condicionó el artículo 5 para que la intervención no alcance a terceros proveedores que hayan procedido de <strong>buena fe exenta de culpa</strong> en el ámbito de sus actividades lícitas ordinarias.</p>
    <p>El estándar es exigente: no basta la creencia honesta. Exige diligencia positiva y comprobable. Acreditarla es un trabajo documental que se construye hacia atrás —contratos, controles, comunicaciones, decisiones registradas— y es, con frecuencia, la diferencia entre quedar dentro o fuera del perímetro de la intervención.</p>
  </div>
""")}

<section class="section band">
  <div class="container prose">
    <h2>Cuando la salida es negociada</h2>
    <p><strong>Plan de desmonte en intervención.</strong> Propuesta de devolución voluntaria conforme a cronograma que, bajo la Ley 1902 de 2018, exige aval de la Superintendencia y respaldo del 75 % de los afectados. Su cumplimiento conduce a la desintervención; su incumplimiento reactiva las medidas.</p>
    <p><strong>Justicia penal negociada.</strong> Preacuerdos, allanamiento y principio de oportunidad. La reparación y el reintegro tienen efecto directo sobre la exposición punitiva, y la coordinación entre la conciliación civil, la devolución administrativa y la negociación penal es donde se juega el resultado. Trabajarlas por separado, con abogados distintos que no se hablan, es la forma más frecuente de perder la ventaja.</p>
  </div>
</section>

{section(f"""
  <h2>Antes de escribir</h2>
  <div class="conflict" style="margin-top:1.2rem">
    <p>El formulario pide tres datos: nombre, una vía de contacto y una línea de contexto. <strong>No escriba los hechos de su caso en el formulario.</strong> No lo necesitamos para agendar y usted no necesita dejarlo por escrito antes de que exista relación profesional.</p>
  </div>
  <p class="prose" style="margin-top:1.2rem">Veraly también representa a afectados en procesos de captación, en casos distintos. Antes de aceptar cualquier consulta verificamos si la firma ya interviene en ese proceso por la orilla contraria. Si es así, declinamos.</p>
""")}

{section(f"""
  <h2>Preguntas frecuentes</h2>
  {faq_block(defensa_faq)}
""", cls="band")}

<section class="section band-2">
  <div class="container">
    <h2>Hablar hoy</h2>
    <div class="contact-grid" style="margin-top:1.4rem">
      <div>{contact_form("defensa", "Enviar el formulario")}
        <div class="cta-row"><a class="btn btn--ghost" href="tel:{SITE["phone_href"]}" data-pos="defensa">Llamar</a>{wa_b}{agendar("Agendar", primary=False)}</div>
      </div>
      <aside>{trust_list()}
        <p style="margin-top:1.4rem"><a class="arrowlink" href="/equipo/">Ver al equipo</a></p>
      </aside>
    </div>
  </div>
</section>
'''
    add("/defensa-en-captacion-masiva/", {
        "title": "Defensa en captación masiva · Arts. 316 y 316A",
        "description": "Defensa administrativa ante la Superintendencia de Sociedades, penal por los arts. 316 y 316A, y civil patrimonial.",
        "active": "investigado", "og_type": "article", "mobile_bar": True,
        "body_class": "has-mobile-bar",
        "schema": [
            service_schema(
                "Defensa en captación masiva y habitual",
                "Defensa de investigados y vinculados en los tres frentes: administrativo ante la Superintendencia de Sociedades, penal por los arts. 316 y 316A, y civil patrimonial.",
                "/defensa-en-captacion-masiva/", "Defensa penal y administrativa"),
            faq_schema(defensa_faq),
            breadcrumb_schema([("Inicio", "/"),
                ("Me investigan o me vincularon", "/defensa-en-captacion-masiva/")]),
        ],
    }, defensa_body)

    # =====================================================================
    # /cumplimiento-en-recaudo-masivo  (Perfil C)
    # =====================================================================
    cumplimiento_faq = [
        ("¿Mi modelo de crowdfunding puede considerarse captación?",
         "<p>Depende de dos cosas: si supera los umbrales del Decreto 1981 de 1988 y si el rendimiento que ofrece tiene explicación financiera razonable acreditable. Las dos se pueden revisar antes de que alguien más las revise.</p>"),
        ("¿Qué pasa si recibimos un requerimiento?",
         "<p>El requerimiento pertenece a la fase administrativa previa, anterior a cualquier declaratoria. Es el momento en que se sustenta técnicamente el modelo, y la calidad de esa sustentación condiciona todo lo que venga después.</p>"),
        ("¿La auditoría periódica es un servicio recurrente?",
         "<p>Sí. Los modelos derivan cuando crecen: cambian los volúmenes, los productos y las contrapartes. La revisión periódica existe para detectar esa deriva antes de que sea material.</p>"),
    ]
    cumplimiento_body = f'''
{section("""
  <p class="eyebrow">Para la empresa preventiva</p>
  <h1>Cumplimiento normativo para modelos de recaudo masivo</h1>
  <p class="support" style="max-width:58ch">Fintech, crowdfunding, libranzas, factoring, multinivel y clubes de inversión operan cerca de los umbrales que configuran captación. La distancia a esos umbrales se puede medir.</p>
  <p class="desc" style="max-width:58ch">Revisamos el encuadre del modelo, fijamos los límites operativos y documentamos los protocolos que sostienen la posición si una superintendencia pregunta.</p>
  <div class="cta-row">
    {agendar("Solicitar una revisión de encuadre")}
    <a class="btn btn--ghost" href="#" data-download="cuestionario">Descargar el cuestionario</a>
  </div>
""", cls="hero")}

<section class="section band">
  <div class="container prose">
    <h2>Dónde está la línea</h2>
    <p>El Decreto 1981 de 1988 fija umbrales objetivos: en esencia, hay captación cuando el pasivo con el público involucra a más de veinte personas o más de cincuenta obligaciones, o cuando median ofertas masivas. El artículo 6 del Decreto 4334 de 2008 añade el criterio material: recursos entregados a cambio de bienes, servicios o rendimientos <strong>sin explicación financiera razonable</strong>.</p>
    <p>El segundo criterio es el que sorprende a los modelos legítimos. Un negocio puede estar por debajo de los umbrales numéricos y aun así quedar señalado si no puede sustentar de dónde sale el rendimiento que ofrece. La defensa de un modelo empieza mucho antes de que haya una investigación: empieza el día en que el modelo se documenta.</p>
  </div>
</section>

{section("""
  <h2>La revisión de encuadre</h2>
  <ul class="method-list">
    <li><strong>Diagnóstico de encuadre y hoja de ruta.</strong> Dictamen de riesgo sobre el modelo actual, con identificación de los puntos en que se aproxima a los supuestos del artículo 6.</li>
    <li><strong>Blindaje preventivo y estructura.</strong> Definición de límites operativos, arquitectura contractual y protocolos documentados, con especial atención a la sustentación de la explicación financiera del rendimiento ofrecido.</li>
    <li><strong>Auditoría periódica de cumplimiento.</strong> Revisión recurrente que detecta la deriva del modelo cuando el negocio crece y las condiciones cambian. Incluye alertas tempranas.</li>
  </ul>
  <p class="prose" style="margin-top:1.2rem">El objeto de la revisión no es un concepto general sobre la normativa: es una posición defendible sobre <strong>su</strong> modelo, escrita para ser leída por un tercero que la cuestione.</p>
""")}

<section class="section band">
  <div class="container prose">
    <h2>Estructuramos con la información que da litigar</h2>
    <p>Veraly defiende procesos de captación en sus tres frentes. Eso significa que conoce el fenómeno por el lado en que se rompe: qué hallazgos activan un requerimiento, qué documentos pide la Superintendencia, qué elementos sostienen la explicación financiera razonable cuando se cuestiona y cuáles no resisten.</p>
    <p>Un modelo se puede estructurar sin esa información. Se estructura mejor con ella.</p>
  </div>
</section>

{section("""
  <h2>Diez preguntas para medir su distancia a los umbrales</h2>
  <p class="lead" style="margin-top:1rem;max-width:60ch">Un cuestionario breve para revisar internamente antes de decidir si conviene una revisión formal. No sustituye un concepto jurídico y no genera relación profesional.</p>
  <div class="cta-row"><a class="btn btn--primary" href="#" data-download="cuestionario">Descargar el cuestionario (PDF)</a></div>
""")}

{section(f"""
  <h2>Preguntas frecuentes</h2>
  {faq_block(cumplimiento_faq)}
""", cls="band")}

<section class="section band-2">
  <div class="container">
    <h2>Revisar el encuadre</h2>
    <div class="contact-grid" style="margin-top:1.4rem">
      <div>{contact_form("cumplimiento", "Solicitar una revisión")}
        <div class="cta-row">{agendar("Agendar una revisión")}</div>
      </div>
      <aside>{trust_list()}</aside>
    </div>
  </div>
</section>
'''
    add("/cumplimiento-en-recaudo-masivo/", {
        "title": "Cumplimiento en recaudo masivo · Captación",
        "description": "Revisión de encuadre para fintech, crowdfunding, libranzas y multinivel frente a los umbrales de captación.",
        "active": "empresa", "og_type": "article",
        "schema": [
            service_schema(
                "Revisión de encuadre en recaudo masivo",
                "Revisión preventiva para fintech, crowdfunding, libranzas, factoring y multinivel frente a los umbrales de captación del Decreto 1981 de 1988.",
                "/cumplimiento-en-recaudo-masivo/", "Cumplimiento normativo"),
            faq_schema(cumplimiento_faq),
            breadcrumb_schema([("Inicio", "/"),
                ("Mi empresa recauda de muchos", "/cumplimiento-en-recaudo-masivo/")]),
        ],
    }, cumplimiento_body)

    # =====================================================================
    # Blog / Análisis  (referente Orionix: fondo claro, serif editorial,
    # tarjeta destacada dividida, filtros y grid de tarjetas)
    # =====================================================================
    LOGO_SVG = g["LOGO_SVG"]
    _GRAPHICS = [g["globe_svg"], g["wave_svg"], g["burst_svg"], g["convergence_svg"]]

    def art_media(i):
        return _GRAPHICS[i % len(_GRAPHICS)]()

    def read_min(html):
        import re as _re
        n = len(_re.sub(r"<[^>]+>", " ", html).split())
        return max(2, round(n / 170))

    def bcard(a, ridx):
        return (
            f'<a class="bcard reveal-up" href="/analisis/{a["slug"]}/" data-tema="{esc(a["tema"])}">'
            f'<div class="bcard-head">'
            f'<span class="bcard-date">{esc(a["date_disp"])}</span>'
            f'<h3 class="bcard-title">{esc(a["title"])}</h3>'
            f'<p class="bcard-desc">{esc(a["desc"])}</p>'
            f'</div>'
            f'<span class="tag bcard-tag">{esc(a["tema"])}</span>'
            f'<div class="bcard-media">{art_media(ridx)}</div>'
            f'</a>')

    # ---- Cuerpos de los artículos (necesarios para calcular el tiempo de lectura)
    ARTICLE_BODIES = {
        "diferencia-entre-estafa-y-captacion-masiva": """
    <h2>Por qué no son el mismo delito</h2>
    <p>La estafa (artículo 246 del Código Penal) exige un artificio o engaño que induce a error a una víctima determinada y le produce un perjuicio. La captación masiva y habitual (artículo 316) sanciona una conducta distinta: recibir dineros del público, de forma masiva y habitual, sin autorización estatal. No requiere probar el engaño individual: lo que se reprocha es la captación no autorizada en sí misma.</p>
    <h2>Qué cambia en la práctica</h2>
    <p>La calificación como captación activa el procedimiento administrativo especial del Decreto 4334 de 2008 ante la Superintendencia de Sociedades, con toma de posesión y un mecanismo de devolución que la estafa común no tiene. Para el afectado, eso abre una vía de recuperación adicional. Para el investigado, cambia por completo el mapa de frentes: a lo penal se suma lo administrativo y lo civil.</p>
    <h2>Por qué se confunden</h2>
    <p>La cobertura pública trata ambos fenómenos como sinónimos, y muchos despachos litigan la captación como si fuera una estafa agravada. No lo es, y trabajarla así deja fuera la vía administrativa —que suele ser la más rápida para el afectado y la más determinante para el vinculado.</p>
""",
        "captacion-con-libranzas-y-factoring": """
    <h2>Contratos legales, uso que puede no serlo</h2>
    <p>La libranza y el factoring son figuras contractuales lícitas. El problema no está en el contrato, sino en el esquema que se construye sobre él: cuando se usan para recibir dineros del público de forma masiva y habitual prometiendo un rendimiento, pueden configurar captación masiva y habitual no autorizada.</p>
    <h2>Los dos criterios que hay que revisar</h2>
    <p>El primero es objetivo: los umbrales del Decreto 1981 de 1988 —más de veinte personas o más de cincuenta obligaciones, o mediación de ofertas masivas—. El segundo es material: el artículo 6 del Decreto 4334 de 2008 exige que exista una explicación financiera razonable del rendimiento ofrecido. Un modelo puede estar por debajo de los umbrales numéricos y aun así quedar señalado si no puede sustentar de dónde sale ese rendimiento.</p>
    <h2>Por qué es terreno defendible</h2>
    <p>Cuando el esquema se apoya en contratos legales y en activos reales, la frontera entre el modelo lícito y la captación se vuelve fina, y se juega en la documentación. Es exactamente el tipo de análisis que exige leer el fenómeno desde varias ramas del derecho a la vez.</p>
""",
        "que-hace-la-superintendencia-de-sociedades": """
    <h2>La toma de posesión</h2>
    <p>Ante indicios de captación no autorizada, la Superintendencia de Sociedades puede ordenar la toma de posesión de los bienes, haberes y negocios de la persona o entidad. La medida trae nombramiento de agente interventor, remoción de administradores, congelación de activos y suspensión de las ejecuciones en curso.</p>
    <h2>Una vía paralela a la penal</h2>
    <p>El procedimiento del Decreto 4334 de 2008 corre de forma autónoma respecto del proceso penal. Sus decisiones tienen carácter jurisdiccional, efectos de cosa juzgada frente a todos y son de única instancia. Para el afectado, esta vía suele ser la más rápida para intentar recuperar el capital.</p>
    <h2>La devolución de recursos</h2>
    <p>Dentro de la intervención se abre un trámite de reclamación con términos cortos, contados en días comunes desde el aviso del interventor. La devolución tiene techo en el capital entregado y opera a prorrata entre los afectados; los rendimientos prometidos no se recuperan por esta vía.</p>
""",
        "buena-fe-exenta-de-culpa-tercero-proveedor": """
    <h2>De dónde viene el estándar</h2>
    <p>El artículo 5 del Decreto 4334 de 2008 extiende la intervención a un perímetro amplio de vinculados. La Sentencia C-145 de 2009 lo condicionó: la intervención no puede alcanzar a terceros proveedores que hayan procedido de buena fe exenta de culpa en el ámbito de sus actividades lícitas ordinarias.</p>
    <h2>Qué exige, exactamente</h2>
    <p>No basta la creencia honesta de estar actuando bien. La buena fe exenta de culpa exige diligencia positiva y comprobable: haber tomado las precauciones que un profesional razonable habría tomado, y poder demostrarlo. Es un estándar más alto que la simple buena fe.</p>
    <h2>Cómo se acredita</h2>
    <p>Se construye hacia atrás, con documentos: contratos, controles internos, comunicaciones, decisiones registradas en su momento. Acreditar ese estándar es, con frecuencia, la diferencia entre quedar dentro o fuera del perímetro de la intervención, y es un trabajo que conviene empezar antes de que la vinculación se formalice.</p>
""",
    }
    READ_MIN = {a["slug"]: read_min(ARTICLE_BODIES[a["slug"]]) for a in ARTICLES}

    # ---- Índice /analisis/ -------------------------------------------------
    feat = ARTICLES[0]
    featured = (
        f'<a class="blog-feature reveal-up" href="/analisis/{feat["slug"]}/">'
        f'<div class="bf-body">'
        f'<span class="bcard-date">{esc(feat["date_disp"])}</span>'
        f'<h2 class="bf-title">{esc(feat["title"])}</h2>'
        f'<p class="bf-desc">{esc(feat["desc"])}</p>'
        f'<span class="tag">{esc(feat["tema"])}</span>'
        f'<div class="bf-foot"><span class="bf-by">Equipo editorial · Veraly</span>'
        f'<span class="bf-read">{READ_MIN[feat["slug"]]} min de lectura</span></div>'
        f'</div>'
        f'<div class="bf-media">{art_media(0)}</div>'
        f'</a>')

    temas_present = [t for t in TEMAS if any(a["tema"] == t for a in ARTICLES)]
    filtros = ('<button type="button" class="bfilter is-active" data-tema="">Todos</button>'
               + "".join(f'<button type="button" class="bfilter" data-tema="{esc(t)}">{esc(t)}</button>'
                         for t in temas_present))
    grid_cards = "".join(bcard(a, i) for i, a in enumerate(ARTICLES[1:]))

    analisis_body = f'''
<section class="section section--tight blog-hero">
  <div class="container">
    <p class="eyebrow">Análisis</p>
    <h1 class="blog-h1">Análisis, criterio<br>y perspectiva jurídica</h1>
    <p class="blog-sub">Sobre las figuras del fraude financiero: cómo se estructuran los esquemas, qué presunciones activan y qué vías abren. Escribimos sobre la figura, nunca sobre casos identificables.</p>
  </div>
</section>

<section class="section section--tight">
  <div class="container">
    {featured}
    <div class="blog-filters" role="group" aria-label="Filtrar por tema">{filtros}</div>
    <div class="blog-grid" data-blog-grid>{grid_cards}</div>
  </div>
</section>
'''
    add("/analisis/", {
        "title": "Análisis · Veraly Grupo Jurídico",
        "description": "Publicaciones sobre las figuras jurídicas del fraude financiero: estructura de los esquemas, presunciones y vías procesales.",
        "active": "analisis", "body_class": "theme-light",
    }, analisis_body)

    # ---- Artículos /analisis/{slug} ---------------------------------------
    cta_labels = {
        "afectados": ("/afectados-por-captacion-masiva/", "Ver la ruta del afectado"),
        "defensa": ("/defensa-en-captacion-masiva/", "Ver la ruta de la defensa"),
        "cumplimiento": ("/cumplimiento-en-recaudo-masivo/", "Ver la ruta preventiva"),
    }
    import urllib.parse as _url
    for a in ARTICLES:
        cta_url, cta_txt = cta_labels[a["cta_target"]]
        body_html = ARTICLE_BODIES[a["slug"]]
        art_url = B + "/analisis/" + a["slug"] + "/"
        share_ln = "https://www.linkedin.com/sharing/share-offsite/?url=" + _url.quote(art_url, safe="")
        share_x = ("https://twitter.com/intent/tweet?text="
                   + _url.quote(a["title"] + " — Veraly Grupo Jurídico", safe="")
                   + "&url=" + _url.quote(art_url, safe=""))
        related = [x for x in ARTICLES if x["slug"] != a["slug"]][:3]
        rel_cards = "".join(bcard(x, i) for i, x in enumerate(related))
        ai = ARTICLES.index(a)
        NORMAS = [
            ("Decreto 4334 de 2008", "Procedimiento de intervención por captación no autorizada."),
            ("Decreto 1981 de 1988", "Umbrales objetivos de captación."),
            ("Artículos 316 y 316A · Código Penal", "Captación masiva y habitual, y no reintegro."),
            ("Sentencia C-145 de 2009", "Presunciones y buena fe exenta de culpa."),
        ]
        norm_rows = "".join(
            f'<div class="norm-row"><span class="norm-k">{esc(k)}</span>'
            f'<p class="norm-d">{esc(d)}</p></div>' for k, d in NORMAS)
        art_body = f'''
{crumbs([("Inicio", "/"), ("Análisis", "/analisis/"), (a["title"], None)])}
<article class="blog-article">
  <header class="container article-head">
    <p class="article-kicker"><span class="dot" aria-hidden="true"></span>{esc(a["tema"])}</p>
    <div class="article-head-row">
      <h1 class="article-h1">{esc(a["h1"])}</h1>
      <p class="article-lede">{esc(a["desc"])}</p>
    </div>
    <div class="article-byline">
      <span class="brand-mark" aria-hidden="true">{LOGO_SVG}</span>
      <span class="ab-name">Equipo editorial · Veraly Grupo Jurídico</span>
      <span class="ab-sep" aria-hidden="true">·</span>
      <time datetime="{a["date_iso"]}">{esc(a["date_disp"])}</time>
      <span class="ab-sep" aria-hidden="true">·</span>
      <span>{READ_MIN[a["slug"]]} min de lectura</span>
    </div>
  </header>
  <div class="article-hero-media"><div class="ahm-inner">{art_media(ai)}</div></div>
  <div class="container prose prose-article article-col">
    <p class="article-intro">{esc(a["answer"])}</p>
    {body_html}
  </div>
  <section class="section norm-two-sec">
    <div class="container pr-two">
      <div class="pr-two-l">
        <p class="eyebrow-num"><span class="n">§</span> Fundamento normativo</p>
        <h2 class="pr-big pr-parallax">El marco que <span class="pr-accent">sostiene el análisis.</span></h2>
      </div>
      <div class="pr-two-r norm-flow">{norm_rows}</div>
    </div>
  </section>
  <div class="container article-col">
    <div class="article-end">
      <div class="article-byline-card">
        <span class="brand-mark" aria-hidden="true">{LOGO_SVG}</span>
        <div>
          <p class="abc-role">Preparado y revisado por la firma</p>
          <p class="abc-text">Las <a class="textlink" href="/equipo/">cinco prácticas del derecho</a> —constitucional, penal, corporativa, tributaria y laboral— especializadas en captación masiva y habitual. Contenido informativo con fundamento normativo verificable. Más respuestas en las <a class="textlink" href="/preguntas-frecuentes/">preguntas frecuentes</a>.</p>
        </div>
      </div>
      <div class="share-row">
        <span class="share-lead">¿Le resultó útil? Compártalo.</span>
        <div class="share-links">
          <a class="share-btn" href="{share_ln}" target="_blank" rel="noopener" aria-label="Compartir en LinkedIn">in</a>
          <a class="share-btn" href="{share_x}" target="_blank" rel="noopener" aria-label="Compartir en X">X</a>
          <button type="button" class="share-btn" data-share-copy="{esc(art_url)}" aria-label="Copiar enlace">↗</button>
        </div>
      </div>
    </div>
  </div>
  <section class="blog-related">
    <div class="container">
      <div class="related-head">
        <p class="bfilter-pill"><span class="dot" aria-hidden="true"></span>Análisis recientes</p>
        <a class="btn btn--ghost" href="/analisis/">Ver todos</a>
      </div>
      <h2 class="related-h2">También puede interesarle</h2>
      <div class="blog-grid">{rel_cards}</div>
    </div>
  </section>
</article>
'''
        article_schema = {
            "@context": "https://schema.org", "@type": "Article",
            "headline": a["h1"],
            "description": a["desc"],
            "datePublished": a["date_iso"], "dateModified": a["date_iso"],
            "author": {"@type": "Organization", "name": "Equipo editorial · " + SITE["name"],
                       "url": B + "/equipo/",
                       "knowsAbout": ["Captación masiva y habitual", "Decreto 4334 de 2008",
                                      "Artículos 316 y 316A del Código Penal",
                                      "Superintendencia de Sociedades", "Fraude financiero"]},
            "publisher": {"@type": "LegalService", "name": SITE["name"], "url": B + "/"},
            "about": {"@type": "Thing", "name": "Captación masiva y habitual"},
            "isPartOf": {"@type": "WebSite", "name": SITE["name"], "url": B + "/"},
            "mainEntityOfPage": B + "/analisis/" + a["slug"] + "/",
            "inLanguage": "es-CO",
        }
        add("/analisis/" + a["slug"] + "/", {
            "title": f'{a["title"]} · Veraly',
            "description": a["desc"],
            "active": "analisis", "og_type": "article", "body_class": "theme-light",
            "schema": [article_schema, breadcrumb_schema([
                ("Inicio", "/"), ("Análisis", "/analisis/"),
                (a["title"], "/analisis/" + a["slug"] + "/")])],
        }, art_body)

    # =====================================================================
    # /preguntas-frecuentes  (FAQ central — autoridad + featured snippets)
    # =====================================================================
    faq_central = [
        ("¿Qué es la captación masiva y habitual?",
         '<p>Es recibir dineros del público sin autorización estatal, entregando a cambio bienes, servicios o rendimientos sin explicación financiera razonable (art. 6 del Decreto 4334 de 2008). Hay captación cuando el pasivo con el público supera los umbrales del Decreto 1981 de 1988: más de veinte personas o más de cincuenta obligaciones, o mediación de ofertas masivas.</p>'),
        ("¿En qué se diferencia la captación de una estafa?",
         '<p>Son delitos distintos. La estafa (art. 246) exige un engaño que induce a error a una víctima determinada; la captación (art. 316) sanciona recibir dineros del público sin autorización, sin necesidad de probar el engaño individual. La captación, además, activa un trámite administrativo propio ante la Superintendencia de Sociedades. <a class="textlink" href="/analisis/diferencia-entre-estafa-y-captacion-masiva/">Ver el análisis completo</a>.</p>'),
        ("¿Qué es la toma de posesión y qué efectos tiene?",
         '<p>Es la medida con la que la Superintendencia de Sociedades interviene los bienes de la captadora bajo el Decreto 4334 de 2008. Tiene carácter jurisdiccional, efectos de cosa juzgada frente a todos y es de única instancia. <a class="textlink" href="/analisis/que-hace-la-superintendencia-de-sociedades/">Cómo funciona la intervención</a>.</p>'),
        ("Perdí dinero en un esquema, ¿por dónde empiezo?",
         '<p>Existen tres vías —administrativa, penal y civil— y cada una tiene términos propios que corren desde la toma de posesión. Identificar cuál aplica y en qué plazo es la primera decisión. No prometemos recuperación: el desenlace depende de la masa de la intervención y de cada caso. <a class="textlink" href="/afectados-por-captacion-masiva/">Ver las vías y los plazos</a>.</p>'),
        ("¿Qué es el no reintegro del artículo 316A?",
         '<p>Es un tipo penal autónomo que sanciona no devolver los recursos captados. Puede concurrir con el art. 316 y con otros delitos como estafa agravada, lavado de activos o concierto para delinquir.</p>'),
        ("Tengo una empresa que recauda de muchas personas, ¿cuándo se configura captación?",
         '<p>Se revisa un criterio objetivo —los umbrales del Decreto 1981 de 1988— y uno material —que exista explicación financiera razonable del rendimiento (art. 6 del Decreto 4334 de 2008)—. Un modelo puede estar bajo los umbrales y aun así quedar señalado si no sustenta de dónde sale el rendimiento. <a class="textlink" href="/cumplimiento-en-recaudo-masivo/">Revisión de encuadre</a>.</p>'),
        ("¿Qué es la “explicación financiera razonable”?",
         '<p>Es la justificación económica verificable del rendimiento ofrecido: de dónde sale y por qué es sostenible. Su ausencia es uno de los indicios centrales de captación, incluso cuando el esquema se apoya en contratos legales como libranzas o factoring. <a class="textlink" href="/analisis/captacion-con-libranzas-y-factoring/">Cuándo un contrato legal configura captación</a>.</p>'),
        ("Me vincularon a un proceso por captación, ¿qué significa?",
         '<p>La vinculación alcanza a administradores, socios, revisores fiscales, contadores y proveedores por el ejercicio del cargo durante el período de captación. Es desvirtuable: la defensa se construye sobre la exclusión y la prueba del origen lícito. <a class="textlink" href="/defensa-en-captacion-masiva/">Ver la ruta de la defensa</a>.</p>'),
        ("¿Qué es la buena fe exenta de culpa?",
         '<p>Es el estándar que, según la Sentencia C-145 de 2009, puede dejar fuera de la intervención a terceros proveedores que actuaron diligentemente en sus actividades lícitas ordinarias. No basta la creencia honesta: exige diligencia comprobable con documentos. <a class="textlink" href="/analisis/buena-fe-exenta-de-culpa-tercero-proveedor/">Cómo se acredita</a>.</p>'),
        ("¿La firma garantiza recuperar el dinero o un resultado?",
         '<p>No. No prometemos recuperación ni desenlace judicial. Lo que se promete es rigor, criterio y trabajo sobre las tres vías, con los límites dichos en voz alta.</p>'),
        ("¿Qué datos piden para una primera consulta?",
         '<p>Solo su nombre, una vía de contacto y una línea de contexto. No pedimos los hechos del caso por escrito: se conversan. Los datos se tratan conforme a la Ley 1581 de 2012. <a class="textlink" href="/contacto/">Agendar una consulta</a>.</p>'),
        ("¿Atienden al afectado y al investigado en el mismo caso?",
         '<p>No. La defensa del investigado y la recuperación del afectado nunca se prestan dentro del mismo proceso de intervención. Cada consulta pasa por verificación previa de conflicto de interés antes de aceptarse.</p>'),
        ("¿Cuál es la diferencia entre la Superintendencia de Sociedades y la Superintendencia Financiera en estos casos?",
         '<p>La Superintendencia Financiera supervisa a las entidades autorizadas para captar y persigue el ejercicio ilegal de la actividad financiera. La captación no autorizada, en cambio, se interviene por la Superintendencia de Sociedades bajo el Decreto 4334 de 2008, que es la que ordena la toma de posesión y adelanta la devolución de recursos.</p>'),
        ("En la devolución, ¿se recupera el capital o también los rendimientos prometidos?",
         '<p>La devolución opera sobre el capital efectivamente entregado, con techo en ese monto y a prorrata entre los afectados según la masa disponible. Los rendimientos prometidos no se reconocen por esa vía. No prometemos recuperación: el desenlace depende de la masa de la intervención. <a class="textlink" href="/analisis/que-hace-la-superintendencia-de-sociedades/">Cómo funciona la devolución</a>.</p>'),
        ("¿Cuánto tiempo hay para presentar la reclamación de devolución?",
         '<p>Los términos son cortos y se cuentan en días comunes desde el aviso del agente interventor. Por eso, ante una toma de posesión, conviene actuar pronto para no perder la oportunidad de reclamar. <a class="textlink" href="/afectados-por-captacion-masiva/">Ver las vías y los plazos</a>.</p>'),
        ("¿Una pirámide o un esquema Ponzi es lo mismo que la captación masiva?",
         '<p>En el lenguaje corriente se usan como sinónimos, pero “pirámide” y “Ponzi” describen el modelo económico. La figura jurídica que activa la intervención administrativa y el tipo penal es la captación masiva y habitual (artículos 316 y 316A del Código Penal y Decreto 4334 de 2008).</p>'),
        ("¿El mercadeo multinivel o en red configura captación?",
         '<p>No por sí mismo. Puede configurarla cuando, más allá de la venta real de bienes o servicios, el modelo recibe dineros del público de forma masiva y habitual prometiendo rendimientos sin explicación financiera razonable y supera los umbrales del Decreto 1981 de 1988. <a class="textlink" href="/cumplimiento-en-recaudo-masivo/">Revisión de encuadre</a>.</p>'),
        ("¿La captación con criptoactivos o a través de una fintech también está cubierta?",
         '<p>El medio tecnológico no cambia la sustancia. Si hay recaudo masivo y habitual del público, sin autorización y sin explicación financiera razonable del rendimiento, puede configurar captación aunque se instrumente con criptoactivos o una plataforma digital. <a class="textlink" href="/analisis/captacion-con-libranzas-y-factoring/">Cuándo un contrato legal configura captación</a>.</p>'),
        ("¿Qué es el agente interventor y qué funciones tiene?",
         '<p>Es la persona designada en la toma de posesión para administrar los bienes intervenidos: remover administradores, congelar y ubicar activos, suspender ejecuciones y adelantar el trámite de devolución de recursos a los afectados. <a class="textlink" href="/analisis/que-hace-la-superintendencia-de-sociedades/">Cómo opera la intervención</a>.</p>'),
        ("Durante la toma de posesión, ¿qué ocurre con los bienes, contratos y procesos en curso?",
         '<p>Los bienes quedan bajo administración del interventor y se congelan; las ejecuciones y procesos sobre ellos se suspenden, y los actos de disposición anteriores pueden revisarse. Leer esa exposición con criterio societario y registral define cuánto patrimonio responde y qué puede devolverse.</p>'),
        ("¿La acción penal por captación prescribe?",
         '<p>Sí, conforme a las reglas generales del Código Penal, cuyos términos dependen de la pena de cada tipo. Por la gravedad de los artículos 316 y 316A y de los delitos que suelen concurrir, esos términos son extensos; el momento procesal, más que la prescripción, suele ser lo determinante.</p>'),
        ("¿Qué otros delitos suelen concurrir con la captación masiva?",
         '<p>Junto al no reintegro del artículo 316A, es frecuente que concurran estafa agravada, lavado de activos y concierto para delinquir. La calificación conjunta define el número de frentes y la estrategia de defensa. <a class="textlink" href="/defensa-en-captacion-masiva/">Ver la ruta de la defensa</a>.</p>'),
    ]
    faq_central_body = f'''
{section("""
  <p class="eyebrow">Preguntas frecuentes</p>
  <span class="prac-rule" aria-hidden="true"></span>
  <h1 class="prac-h1">Preguntas frecuentes sobre captación masiva.</h1>
  <p class="prac-sub">Las dudas más frecuentes sobre el fraude financiero por captación —qué es, cómo se investiga, qué vías abre y qué se puede hacer—. Respuestas sobre la figura jurídica, nunca sobre casos identificables.</p>
""", cls="hero")}

{faq_sticky(faq_central)}

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="cta-row">{agendar("Agendar una consulta")}<a class="btn btn--ghost" href="/analisis/">Leer los análisis</a></div>
  </div>
</section>
'''
    add("/preguntas-frecuentes/", {
        "title": "Preguntas frecuentes sobre captación masiva · Veraly",
        "description": "Respuestas claras sobre captación masiva y habitual: diferencia con la estafa, toma de posesión, vías de recuperación, vinculación y umbrales.",
        "active": "", "body_class": "theme-light",
        "schema": [faq_schema(faq_central), breadcrumb_schema([
            ("Inicio", "/"), ("Preguntas frecuentes", "/preguntas-frecuentes/")])],
    }, faq_central_body)

    # =====================================================================
    # /politica-de-cookies
    # =====================================================================
    cookies_body = f'''
{section("""
  <p class="eyebrow">Legal</p>
  <h1>Política de cookies</h1>
""", cls="hero", tight=True)}
<section class="section band">
  <div class="container prose">
    <p style="color:var(--dim-2)"><em>Borrador. Requiere revisión y aprobación de los socios antes de publicar (§17, pendiente 06).</em></p>
    <h2>Qué son las cookies</h2>
    <p>Las cookies son pequeños archivos que un sitio guarda en su navegador para recordar preferencias y entender cómo se usa el sitio. Este sitio funciona sin necesidad de aceptarlas.</p>
    <h2>Qué cookies usamos</h2>
    <p>Usamos dos categorías. Las <strong>esenciales</strong> permiten recordar su preferencia sobre las cookies y no requieren consentimiento. Las <strong>analíticas</strong> —opcionales— nos ayudan a entender de forma agregada cómo se navega el sitio; solo se activan si usted las acepta en el aviso inicial.</p>
    <h2>Cómo gestionar su preferencia</h2>
    <p>Puede aceptar o continuar sin las cookies analíticas desde el aviso que aparece al entrar. También puede borrar o bloquear las cookies desde la configuración de su navegador en cualquier momento.</p>
    <h2>Datos personales</h2>
    <p>El tratamiento de datos personales se rige por nuestro <a class="textlink" href="/aviso-de-privacidad/">aviso de privacidad</a>, conforme a la Ley 1581 de 2012.</p>
  </div>
</section>
'''
    add("/politica-de-cookies/", {
        "title": "Política de cookies · Veraly Grupo Jurídico",
        "description": "Cómo usa Veraly Grupo Jurídico las cookies esenciales y analíticas, y cómo gestionar su preferencia.",
        "active": "",
    }, cookies_body)

    # =====================================================================
    # Páginas legales
    # =====================================================================
    privacidad_body = f'''
{section("""
  <p class="eyebrow">Legal</p>
  <h1>Aviso de privacidad y política de tratamiento de datos</h1>
""", cls="hero", tight=True)}
<section class="section band">
  <div class="container prose">
    <p style="color:var(--dim-2)"><em>Borrador. Requiere revisión y aprobación de los socios antes de publicar (§17, pendiente 06).</em></p>
    <h2>Responsable del tratamiento</h2>
    <p>{esc(SITE["name"])}, con domicilio en {esc(SITE["address"])}, correo {esc(SITE["email"])} y teléfono {esc(SITE["phone_display"])}, es responsable del tratamiento de los datos personales recogidos a través de este sitio.</p>
    <h2>Finalidades</h2>
    <p>Los datos que usted proporciona a través del formulario de contacto —nombre, una vía de contacto y una línea de contexto opcional— se tratan con la única finalidad de atender su solicitud de contacto y realizar la verificación previa de conflicto de interés. No se solicitan los hechos del caso ni datos sensibles a través del sitio.</p>
    <h2>Derechos del titular</h2>
    <p>Conforme a la Ley 1581 de 2012 y al Decreto 1074 de 2015, usted puede conocer, actualizar, rectificar y suprimir sus datos, así como revocar la autorización otorgada. Para ejercer estos derechos puede escribir a {esc(SITE["email"])}.</p>
    <h2>Término de conservación</h2>
    <p>Los datos se conservan durante el tiempo necesario para atender la solicitud y cumplir las obligaciones legales aplicables. [Definir término definitivo.]</p>
    <h2>Autorización</h2>
    <p>El envío del formulario, con la casilla de autorización marcada, constituye la autorización informada para el tratamiento de datos conforme a esta política.</p>
  </div>
</section>
'''
    add("/aviso-de-privacidad/", {
        "title": "Aviso de privacidad · Veraly Grupo Jurídico",
        "description": "Política de tratamiento de datos personales de Veraly Grupo Jurídico conforme a la Ley 1581 de 2012.",
        "active": "",
    }, privacidad_body)

    legal_body = f'''
{section("""
  <p class="eyebrow">Legal</p>
  <h1>Aviso legal</h1>
""", cls="hero", tight=True)}
<section class="section band">
  <div class="container prose">
    <p style="color:var(--dim-2)"><em>Borrador. Requiere revisión y aprobación de los socios antes de publicar (§17, pendiente 06).</em></p>
    <h2>Titularidad del sitio</h2>
    <p>Este sitio es titularidad de {esc(SITE["name"])}. Los contenidos, textos y elementos de identidad son propiedad de la firma o se utilizan con autorización.</p>
    <h2>Alcance de la información</h2>
    <p>La información publicada en este sitio tiene carácter general e informativo sobre figuras jurídicas del fraude financiero y la práctica de la firma. No se refiere a casos identificables ni a personas determinadas.</p>
    <h2>No constituye asesoría</h2>
    <p>El contenido de este sitio <strong>no constituye asesoría jurídica ni genera relación profesional</strong>. Ninguna relación abogado-cliente se establece por la consulta del sitio ni por el envío del formulario de contacto; esa relación, cuando corresponde, se formaliza por escrito y tras la verificación previa de conflicto de interés.</p>
  </div>
</section>
'''
    add("/aviso-legal/", {
        "title": "Aviso legal · Veraly Grupo Jurídico",
        "description": "Titularidad del sitio, alcance de la información publicada y nota de que el contenido es informativo y no constituye asesoría jurídica.",
        "active": "",
    }, legal_body)
