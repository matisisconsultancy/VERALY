# -*- coding: utf-8 -*-
"""Capa 1: /firma, /equipo, /equipo/{socio}, /contacto."""

def build(g):
    add = g["add"]; esc = g["esc"]; SITE = g["SITE"]; SOCIOS = g["SOCIOS"]
    ARTICLES = g["ARTICLES"]; socio_by_slug = g["socio_by_slug"]
    section = g["section"]; crumbs = g["crumbs"]; contact_form = g["contact_form"]
    trust_list = g["trust_list"]; person_schema = g["person_schema"]
    breadcrumb_schema = g["breadcrumb_schema"]; B = g["B"]
    PRACTICAS = g["PRACTICAS"]; agendar = g["agendar_btn"]
    service_schema = g["service_schema"]

    # =====================================================================
    # /firma
    # =====================================================================
    firma_body = f'''
{section("""
  <p class="eyebrow">La firma</p>
  <h1>Una firma construida sobre un solo fenómeno jurídico</h1>
  <p class="support" style="max-width:52ch">Veraly Grupo Jurídico entiende el fraude financiero en toda su complejidad. Defendemos a quien lo sufre —por haber perdido lo invertido o por estar bajo investigación— con la lectura completa que da un equipo trabajando el problema desde cada una de sus ramas.</p>
""", cls="hero")}

<section class="section band">
  <div class="container prose">
    <h2>Qué es la captación masiva y habitual</h2>
    <p>Consiste en recibir dineros del público sin autorización estatal, entregando a cambio bienes, servicios o rendimientos sin explicación financiera razonable (art. 6 del Decreto 4334 de 2008). Hay captación cuando el pasivo con el público supera los umbrales del Decreto 1981 de 1988 —más de veinte personas o más de cincuenta obligaciones, o mediación de ofertas masivas—.</p>
    <p>Es un fenómeno denso y ruidoso, y por eso se litiga mal: la mayoría de los despachos lo trata como una estafa agravada. No lo es.</p>
  </div>
</section>

{section("""
  <h2>Tres responsabilidades que corren al mismo tiempo</h2>
  <div class="prose" style="margin-top:1.2rem">
    <p>Una misma conducta detona, de forma simultánea e independiente, tres procesos. No son fases: son frentes paralelos, y cada uno condiciona a los otros dos.</p>
    <p><strong>Administrativa.</strong> Procedimiento del Decreto 4334 de 2008 ante la Superintendencia de Sociedades. La toma de posesión tiene efectos de cosa juzgada frente a todos y es de única instancia.</p>
    <p><strong>Penal.</strong> Artículo 316 del Código Penal (prisión de 120 a 240 meses) y tipo autónomo de no reintegro del 316A, a los que suelen sumarse estafa agravada, lavado de activos y concierto para delinquir.</p>
    <p><strong>Civil.</strong> Persigue el patrimonio personal de administradores, revisores fiscales, contadores y vinculados solventes por el faltante que la masa no cubre.</p>
    <p>Un despacho que atiende solo una de las tres vías trabaja un tercio del problema.</p>
  </div>
""")}

<section class="section band">
  <div class="container">
    <p class="eyebrow">El método de convergencia</p>
    <h2>Cinco prácticas sobre el mismo expediente</h2>
    <div class="prose" style="margin-top:1.2rem">
      <p>Lo habitual es asignar cada caso al socio de la especialidad correspondiente. En captación esa estructura falla, porque el caso no tiene una especialidad: tiene seis a la vez. Veraly opera al revés: los cinco socios trabajan el mismo expediente desde sus ramas, y el caso se construye en la intersección.</p>
      <h3>Identificamos hechos, actores y rutas jurídicas.</h3>
    </div>
    <ul class="method-list">
      <li><strong>Hechos.</strong> Qué ocurrió, con qué documentos, en qué fechas y con qué trazabilidad financiera.</li>
      <li><strong>Actores.</strong> Quién ocupó cada posición y qué consecuencia jurídica arrastra.</li>
      <li><strong>Rutas.</strong> Qué vías están abiertas, cuáles precluyeron y en qué orden activarlas.</li>
    </ul>
  </div>
</section>

{section("""
  <p class="eyebrow">Las dos líneas y la regla</p>
  <h2>Defendemos las dos orillas. Nunca en el mismo proceso.</h2>
  <div class="conflict" style="margin-top:1.4rem">
    <p><strong>Es una regla que no admite excepción:</strong> la defensa del investigado y la recuperación del afectado jamás se prestan dentro del mismo proceso de intervención. El portafolio opera sobre casos distintos, y cada consulta pasa por verificación previa de conflicto antes de aceptarse. Si la firma ya interviene por la orilla contraria, se declina y se explica por qué.</p>
  </div>
""")}

<section class="section band">
  <div class="container">
    <h2>Lo que no hacemos</h2>
    <ul class="negations">
      <li>No prometemos recuperación ni desenlace judicial.</li>
      <li>No aceptamos casos de las dos orillas en el mismo proceso.</li>
      <li>No publicamos casos identificables ni cifras de damnificados.</li>
      <li>No trabajamos captación masiva como una especialidad más de un portafolio general.</li>
    </ul>
  </div>
</section>

{section(f"""
  <h2>El equipo</h2>
  <p class="lead" style="margin-top:1rem;max-width:56ch">Cinco socios aportan cinco ramas del derecho al mismo expediente.</p>
  <div class="cta-row">
    <a class="btn btn--ghost" href="/equipo/">Por qué cinco prácticas</a>
    {agendar("Agendar una consulta")}
  </div>
""", cls="band-2")}
'''
    add("/firma/", {
        "title": "La firma · Veraly Grupo Jurídico",
        "description": "Cómo trabaja Veraly los procesos por captación masiva en sus tres frentes: administrativo, penal y civil.",
        "active": "firma",
    }, firma_body)

    # =====================================================================
    # /equipo  (hub de las cinco prácticas, sin nombres) + páginas de práctica
    # =====================================================================
    # Desarrollo de cada práctica: función en un caso de captación, a qué
    # situación sirve y qué normas toca. Habla de la disciplina, no de personas.
    PRACTICAS_DEV = [
        {
            "slug": "contractual-y-constitucional",
            "rama": "Contractual y constitucional",
            "card": "El debido proceso en un trámite de única instancia y el andamiaje contractual anterior a la toma de posesión.",
            "lede": "Lee el proceso de captación desde dos planos: las garantías constitucionales del trámite y la arquitectura contractual de todo lo que ocurrió antes de la intervención.",
            "paras": [
                "El procedimiento del Decreto 4334 de 2008 es de única instancia y sus decisiones tienen efectos de cosa juzgada frente a todos. Esa concentración exige una lectura constitucional cuidadosa del debido proceso: cuándo se garantiza la contradicción, cómo se ejerce la defensa material dentro de un trámite tan comprimido y qué actos son susceptibles de control.",
                "En paralelo, el esquema casi siempre se construyó sobre contratos —mandatos, mutuos, cuentas en participación, promesas— firmados antes de la toma de posesión. Entender ese andamiaje contractual permite distinguir lo lícito de lo que sostuvo la captación, y es la base sobre la que se apoyan las demás prácticas.",
            ],
            "normas": ["Decreto 4334 de 2008 — única instancia y efectos de cosa juzgada.",
                       "Debido proceso (art. 29 de la Constitución) en trámites concentrados.",
                       "Régimen general de obligaciones y contratos previos a la intervención."],
            "serves": [("Me investigan o me vincularon", "/defensa-en-captacion-masiva/"),
                       ("Perdí dinero en un esquema", "/afectados-por-captacion-masiva/")],
            "articulo": ("que-hace-la-superintendencia-de-sociedades", "Qué hace la Superintendencia de Sociedades"),
        },
        {
            "slug": "tributaria-y-migratoria",
            "rama": "Tributaria y migratoria",
            "card": "Las contingencias tributarias sobre los flujos del esquema y las consecuencias migratorias de los vinculados.",
            "lede": "Sigue el dinero y sigue a las personas: las contingencias fiscales que dejan los flujos del esquema y las consecuencias migratorias que alcanzan a vinculados extranjeros.",
            "paras": [
                "Todo esquema de captación deja un rastro tributario: retenciones, declaraciones, movimientos que la autoridad fiscal puede leer de forma independiente al proceso por captación. Anticipar esas contingencias evita que una defensa se gane en un frente y se pierda en otro.",
                "Cuando hay vinculados extranjeros o estructuras fuera del país, la dimensión migratoria se vuelve real: visados, permanencia y salidas quedan condicionados por el proceso. Integrar ese análisis desde el inicio impide sorpresas que ninguna de las otras prácticas vería venir.",
            ],
            "normas": ["Estatuto Tributario — obligaciones formales y sustanciales sobre los flujos.",
                       "Régimen migratorio aplicable a vinculados extranjeros.",
                       "Intercambio de información entre autoridades."],
            "serves": [("Me investigan o me vincularon", "/defensa-en-captacion-masiva/"),
                       ("Mi empresa recauda de muchos", "/cumplimiento-en-recaudo-masivo/")],
            "articulo": None,
        },
        {
            "slug": "corporativa-y-urbana",
            "rama": "Corporativa y urbana",
            "card": "Las controversias societarias sobre actos anteriores a la intervención y los activos inmobiliarios comprometidos.",
            "lede": "Trabaja la vida societaria de la captadora y los activos reales que suelen sostener el esquema: qué decisiones son atacables y qué pasa con los inmuebles comprometidos.",
            "paras": [
                "La toma de posesión congela una sociedad que, hasta el día anterior, tomaba decisiones: aumentos de capital, cesiones, garantías, operaciones entre vinculadas. Revisar la validez de esos actos anteriores a la intervención define responsabilidades y, muchas veces, la suerte de administradores y terceros.",
                "Buena parte de los esquemas se apoya en inmuebles —comprados, prometidos o dados en garantía—. La dimensión urbana y registral determina qué activos entran a la masa, cuáles pueden liberarse y cómo se protege a quien contrató de buena fe.",
            ],
            "normas": ["Código de Comercio — validez de actos societarios y responsabilidad de administradores.",
                       "Régimen de propiedad y registro de inmuebles comprometidos.",
                       "Decreto 4334 de 2008 — perímetro de bienes de la intervención."],
            "serves": [("Me investigan o me vincularon", "/defensa-en-captacion-masiva/"),
                       ("Perdí dinero en un esquema", "/afectados-por-captacion-masiva/")],
            "articulo": ("captacion-con-libranzas-y-factoring", "Captación montada sobre contratos legales"),
        },
        {
            "slug": "penal-e-informatica",
            "rama": "Penal e informática",
            "card": "La defensa penal por los artículos 316 y 316A y la evidencia digital, desde los actos urgentes hasta el juicio oral.",
            "lede": "Conduce el frente penal —los artículos 316 y 316A y los delitos que suelen concurrir— y la prueba digital que hoy sostiene o desmonta la acusación.",
            "paras": [
                "El proceso penal por captación masiva y habitual (art. 316) y no reintegro (art. 316A) suele venir acompañado de estafa agravada, lavado de activos y concierto para delinquir. La defensa se juega desde los actos urgentes y la audiencia de imputación: cada decisión temprana condiciona el juicio oral.",
                "Casi toda la prueba es digital: registros de plataformas, comunicaciones, trazas de pagos. Tratar esa evidencia con criterio informático —cadena de custodia, autenticidad, alcance— es lo que permite excluir lo mal recaudado y sostener el origen lícito de lo que sí lo tiene.",
            ],
            "normas": ["Artículos 316 y 316A del Código Penal — captación masiva y no reintegro.",
                       "Delitos concurrentes: estafa agravada, lavado de activos, concierto para delinquir.",
                       "Régimen de evidencia digital y cadena de custodia."],
            "serves": [("Me investigan o me vincularon", "/defensa-en-captacion-masiva/")],
            "articulo": ("diferencia-entre-estafa-y-captacion-masiva", "Diferencia entre estafa y captación masiva"),
        },
        {
            "slug": "laboral-y-de-seguros",
            "rama": "Laboral y de seguros",
            "card": "Las reclamaciones laborales de la sociedad intervenida y la exposición de las pólizas y garantías del recaudo.",
            "lede": "Resuelve dos frentes que suelen quedar huérfanos: las relaciones laborales de la sociedad intervenida y las pólizas o garantías vinculadas al recaudo.",
            "paras": [
                "La captadora tuvo empleados, comisionistas y estructuras de pago que la intervención interrumpe de golpe. Ordenar esas relaciones laborales —qué se debe, a quién y con qué prelación— evita contingencias que crecen en silencio mientras el resto del caso avanza.",
                "Muchos esquemas se aseguraron: pólizas de cumplimiento, de manejo, garantías de terceros. Leer esa exposición determina si hay una fuente adicional de recuperación para el afectado o un frente adicional de reclamación contra el vinculado.",
            ],
            "normas": ["Código Sustantivo del Trabajo — obligaciones y prelación de acreencias laborales.",
                       "Régimen de seguros — pólizas de cumplimiento, manejo y garantías.",
                       "Concurrencia con la masa de la intervención."],
            "serves": [("Perdí dinero en un esquema", "/afectados-por-captacion-masiva/"),
                       ("Me investigan o me vincularon", "/defensa-en-captacion-masiva/")],
            "articulo": None,
        },
    ]

    # --- hub /equipo: tesis "por qué cinco" integrada + tarjetas-enlace ---
    practicas_cards = ""
    for pr in PRACTICAS_DEV:
        practicas_cards += f'''<a class="socio" href="/equipo/{pr["slug"]}/">
  <span class="practica">{esc(pr["rama"])}</span>
  <p style="color:var(--dim);margin:.4rem 0 .2rem;font-size:var(--step-0)">{esc(pr["card"])}</p>
  <span class="arrowlink">Ver la práctica</span>
</a>'''
    equipo_body = f'''
{section("""
  <p class="eyebrow">El equipo</p>
  <h1>Cinco prácticas, un mismo caso</h1>
  <p class="support" style="max-width:52ch">El método de la firma no es un principio abstracto: es su composición. Cinco prácticas del derecho trabajan el mismo expediente, y el caso se construye en la intersección.</p>
""", cls="hero")}

{section("""
  <p class="eyebrow">Por qué cinco y no una</p>
  <h2 style="max-width:22ch">Un caso de captación no tiene una especialidad: tiene seis a la vez</h2>
  <div class="prose" style="margin-top:1.2rem">
    <p>Un proceso por captación produce, en paralelo, una actuación ante la Superintendencia de Sociedades, un proceso penal, demandas civiles de responsabilidad, controversias societarias, contingencias tributarias sobre los flujos y reclamaciones laborales de la intervenida. Ningún abogado cubre eso solo. Lo habitual es asignar el caso a una especialidad y trabajar un tercio del problema; esta firma se compuso para cubrirlo entero.</p>
  </div>
""")}

<section class="section band">
  <div class="container">
    <h2 style="margin-bottom:1.4rem">Las cinco prácticas</h2>
    <div class="socios">{practicas_cards}</div>
    <div class="cta-row" style="margin-top:2rem">{agendar("Agendar una consulta")}<a class="btn btn--ghost" href="/firma/">Cómo trabajamos</a></div>
  </div>
</section>
'''
    add("/equipo/", {
        "title": "El equipo · Las cinco prácticas · Veraly Grupo Jurídico",
        "description": "La firma se compone de cinco prácticas del derecho que convergen sobre el mismo expediente de captación masiva: constitucional, penal, corporativa, tributaria y laboral.",
        "active": "equipo",
        "schema": [breadcrumb_schema([("Inicio", "/"), ("El equipo", "/equipo/")])],
    }, equipo_body)

    # --- navegador lateral: la ruta entre las cinco prácticas, siempre visible ---
    def practica_nav(current):
        items = ""
        for p in PRACTICAS_DEV:
            cur = ' aria-current="page"' if p["slug"] == current else ''
            items += f'<a href="/equipo/{p["slug"]}/"{cur}>{esc(p["rama"])}</a>'
        return (f'<div class="container practica-nav-wrap">'
                f'<nav class="practica-nav" aria-label="Las cinco prácticas">{items}</nav></div>')

    # --- páginas de desarrollo por práctica (simplificadas: un solo bloque) ---
    for pr in PRACTICAS_DEV:
        url = "/equipo/" + pr["slug"] + "/"
        paras = "".join(f"<p>{esc(t)}</p>" for t in pr["paras"])
        normas = "".join(f"<li>{esc(n)}</li>" for n in pr["normas"])
        serves = "".join(
            f'<li><a class="arrowlink" href="{u}">{esc(t)}</a></li>' for t, u in pr["serves"])
        art = ""
        if pr["articulo"]:
            aslug, atitle = pr["articulo"]
            art = f'<a class="arrowlink" href="/analisis/{aslug}/">Análisis · {esc(atitle)}</a>'
        practica_body = f'''
{crumbs([("Inicio", "/"), ("El equipo", "/equipo/"), (pr["rama"], None)])}
{section(f"""
  <p class="eyebrow">Una de las cinco prácticas</p>
  <h1>{esc(pr["rama"])}</h1>
  <p class="support" style="max-width:60ch">{esc(pr["lede"])}</p>
""", cls="hero", tight=True)}

{practica_nav(pr["slug"])}

<section class="section band">
  <div class="container prose">
    <h2>Qué resuelve en un caso de captación</h2>
    {paras}
    <h3 style="margin-top:1.8rem">Normas que toca</h3>
    <ul>{normas}</ul>
    <h3 style="margin-top:1.8rem">A qué situación sirve</h3>
    <ul class="method-list">{serves}</ul>
    {art}
    <div class="cta-row" style="margin-top:1.8rem">{agendar("Agendar una consulta")}<a class="btn btn--ghost" href="/equipo/">← Volver a las cinco prácticas</a></div>
  </div>
</section>
'''
        add(url, {
            "title": f'{pr["rama"]} · Las cinco prácticas · Veraly',
            "description": pr["lede"],
            "active": "equipo",
            "schema": [
                service_schema(
                    pr["rama"] + " en captación masiva", pr["lede"], url, pr["rama"]),
                breadcrumb_schema([("Inicio", "/"), ("El equipo", "/equipo/"),
                                   (pr["rama"], url)]),
            ],
        }, practica_body)

    # =====================================================================
    # /marca  (brandbook — pieza de verificación)
    # =====================================================================
    LOGO = g["LOGO_SVG"]
    marca_body = f'''
{section(f"""
  <p class="eyebrow">El sistema de marca</p>
  <h1>El sistema de marca de Veraly</h1>
  <p class="support" style="max-width:60ch">La identidad de la firma se construyó como se construye un caso: con criterio declarado, decisiones documentadas y límites explícitos. Publicamos el sistema completo porque la disciplina con la que una firma administra su propia marca dice algo sobre la disciplina con la que administra lo demás.</p>
""", cls="hero")}

<section class="section band">
  <div class="container">
    <div class="grid grid-2" style="align-items:center">
      <div class="prose">
        <h2>El nombre</h2>
        <p>Veraly es una palabra construida. La raíz <em>vera-</em> remite a lo verdadero; la terminación le da textura contemporánea y la aleja de las sonoridades tradicionales del sector. Los socios optaron por no cargar el nombre con un significado declarado: el significado lo construyen la comunicación y la práctica.</p>
        <h2>El isotipo: Convergencia</h2>
        <p>Cinco formas en V que convergen en un punto central. Una por socio. Es la traducción gráfica del método: cinco prácticas que se encuentran sobre el mismo caso.</p>
      </div>
      <div style="display:flex;justify-content:center">
        <span aria-hidden="true" style="width:min(260px,60vw);height:min(260px,60vw);color:var(--accent);display:inline-block">{LOGO}</span>
      </div>
    </div>
  </div>
</section>

{section("""
  <h2>El sistema visual</h2>
  <p class="prose" style="margin-top:1rem">Paleta, tipografía y usos se documentan en el brandbook completo. El sitio aplica la paleta teal con acento menta, la tipografía Playfair Display para los títulos y Archivo para el texto.</p>
  <h2 style="margin-top:2.4rem">El sistema verbal</h2>
  <div class="prose" style="margin-top:1rem">
    <p>Claim institucional: <strong>Defensa en fraude financiero.</strong></p>
    <p>Voz sobria pero no rígida, directa, respetuosa y técnica donde corresponde. Sin promesas de resultado: se promete rigor, criterio y trabajo. Vocabulario propio: fraude financiero, captación masiva y habitual, vinculado, afectado, intervención, rutas jurídicas, convergencia, las cinco prácticas, explicación financiera razonable.</p>
  </div>
  <div class="cta-row">
    <a class="btn btn--primary" href="/marca/sistema/" data-marca>Ver el brandbook completo</a>
    <a class="btn btn--ghost" href="/equipo/">Conocer al equipo</a>
  </div>
""", cls="band")}
'''
    add("/marca/", {
        "title": "El sistema de marca · Veraly Grupo Jurídico",
        "description": "El sistema de marca de Veraly Grupo Jurídico: nombre, isotipo Convergencia, sistema visual y verbal.",
        "active": "",
        "robots": "noindex,follow",  # pieza de verificación: no debe competir en búsquedas
    }, marca_body)

    # =====================================================================
    # /contacto
    # =====================================================================
    wa_btn = (f'<a class="btn btn--ghost" href="https://wa.me/{SITE["whatsapp"]}" data-whatsapp data-pos="contacto">Escribir por WhatsApp</a>'
              if SITE["whatsapp"] else "")
    contacto_body = f'''
{section(f"""
  <p class="eyebrow">Contacto</p>
  <h1>Hablar con la firma</h1>
  <p class="support" style="max-width:54ch">Una primera conversación sirve para determinar si hay caso, qué vías están abiertas y qué plazos corren. No requiere aportar documentación ni tomar ninguna decisión.</p>
  <div class="cta-row">{agendar("Agendar una consulta")}<a class="btn btn--ghost" href="#formulario">Escribir el formulario</a></div>
""", cls="hero", tight=True)}

<section class="section band" id="agendar">
  <div class="container">
    <div class="agendar-box">
      <p class="eyebrow">Agendar en línea</p>
      <h2>Elija una franja para la primera conversación</h2>
      <p>Reserve directamente un espacio con la firma. Solo necesitamos su nombre y una vía de contacto; no hace falta describir el caso.</p>
      <div id="cal-inline" data-cal-inline></div>
      <div class="cta-row">{agendar("Agendar una consulta")}</div>
    </div>
  </div>
</section>

<section class="section band" id="formulario">
  <div class="container">
    <div class="contact-grid">
      <div>
        {contact_form("institucional", "Enviar")}
        <div class="cta-row">
          <a class="btn btn--ghost" href="tel:{SITE["phone_href"]}" data-pos="contacto">Llamar</a>
          {wa_btn}
        </div>
      </div>
      <aside>
        {trust_list()}
        <dl class="firm-data">
          <div><dt>Dirección</dt><dd>{esc(SITE["address"])}</dd></div>
          <div><dt>Teléfono</dt><dd><a href="tel:{SITE["phone_href"]}" data-pos="contacto">{esc(SITE["phone_display"])}</a></dd></div>
          <div><dt>Correo</dt><dd><a href="mailto:{SITE["email"]}">{esc(SITE["email"])}</a></dd></div>
          <div><dt>Horario</dt><dd>{esc(SITE["hours"])}</dd></div>
        </dl>
      </aside>
    </div>
  </div>
</section>
'''
    add("/contacto/", {
        "title": "Contacto · Veraly Grupo Jurídico",
        "description": "Solicite una primera conversación con Veraly Grupo Jurídico. Datos mínimos y verificación previa de conflicto de interés.",
        "active": "contacto",
    }, contacto_body)
