# -*- coding: utf-8 -*-
"""Capa 1: /firma, /equipo, /equipo/{socio}, /contacto."""

def build(g):
    add = g["add"]; esc = g["esc"]; SITE = g["SITE"]; SOCIOS = g["SOCIOS"]
    ARTICLES = g["ARTICLES"]; socio_by_slug = g["socio_by_slug"]
    section = g["section"]; crumbs = g["crumbs"]; contact_form = g["contact_form"]
    trust_list = g["trust_list"]; person_schema = g["person_schema"]
    breadcrumb_schema = g["breadcrumb_schema"]; B = g["B"]

    # =====================================================================
    # /firma
    # =====================================================================
    firma_body = f'''
{section("""
  <p class="eyebrow">La firma</p>
  <h1>Una firma construida sobre un solo fenómeno jurídico</h1>
  <p class="support" style="max-width:52ch">Veraly Grupo Jurídico entiende el fraude financiero en toda su complejidad. Defendemos a quien lo sufre —sea por haber perdido lo invertido o por estar bajo investigación— con la lectura completa que da un equipo trabajando el problema desde cada una de sus ramas.</p>
""", cls="hero")}

<section class="section band">
  <div class="container prose">
    <h2>Qué es la captación masiva y habitual</h2>
    <p>La captación masiva y habitual no autorizada consiste en recibir dineros del público sin autorización estatal, bajo esquemas —pirámides, tarjetas prepago, venta de servicios y operaciones semejantes— en los que se entregan recursos a cambio de bienes, servicios o rendimientos sin explicación financiera razonable. Así lo define el artículo 6 del Decreto 4334 de 2008.</p>
    <p>Los umbrales objetivos provienen del Decreto 1981 de 1988: en esencia, hay captación cuando el pasivo con el público involucra a más de veinte personas o más de cincuenta obligaciones, o cuando median ofertas masivas.</p>
    <p>Es un fenómeno técnicamente denso y socialmente ruidoso. Esa combinación explica por qué se litiga mal: la cobertura pública lo simplifica y la mayoría de los despachos lo trata como una estafa agravada. No lo es.</p>
  </div>
</section>

{section("""
  <h2>Tres responsabilidades que corren al mismo tiempo</h2>
  <div class="prose" style="margin-top:1.2rem">
    <p>Una misma conducta de captación detona, de forma simultánea e independiente, tres procesos distintos. No son fases: son frentes paralelos, y lo que ocurre en cada uno condiciona a los otros dos.</p>
    <p><strong>Administrativa.</strong> Procedimiento especial del Decreto 4334 de 2008, de competencia privativa de la Superintendencia de Sociedades. Sus decisiones de toma de posesión tienen carácter jurisdiccional, efectos de cosa juzgada frente a todos y única instancia. No hay segunda oportunidad procesal.</p>
    <p><strong>Penal.</strong> Delito de captación masiva y habitual del artículo 316 del Código Penal, con prisión de 120 a 240 meses tras la Ley 1357 de 2009, y tipo autónomo de no reintegro del artículo 316A. A ellos suelen sumarse estafa agravada, lavado de activos, enriquecimiento ilícito de particulares y concierto para delinquir.</p>
    <p><strong>Civil.</strong> Persigue el patrimonio personal de administradores, revisores fiscales, contadores y vinculados solventes por el faltante que la masa de la intervención no alcanza a cubrir.</p>
    <p>Un despacho que atiende solo una de las tres vías está trabajando un tercio del problema.</p>
  </div>
""")}

<section class="section band">
  <div class="container">
    <p class="eyebrow">El método de convergencia</p>
    <h2>Cinco prácticas sobre el mismo expediente</h2>
    <div class="prose" style="margin-top:1.2rem">
      <p>La estructura habitual de un despacho asigna cada caso al socio de la especialidad correspondiente. En captación masiva esa estructura falla, porque el caso no tiene una especialidad: tiene seis a la vez.</p>
      <p>Veraly opera al revés. Los cinco socios trabajan el mismo expediente desde sus ramas —contractual y constitucional, tributaria y migratoria, corporativa y urbana, penal e informática, laboral y de seguros— y el caso se construye en la intersección.</p>
      <h3>En un caso de fraude financiero, identificamos hechos, actores y rutas jurídicas.</h3>
    </div>
    <ul class="method-list">
      <li><strong>Hechos.</strong> Qué ocurrió, con qué documentos, en qué fechas y con qué trazabilidad financiera.</li>
      <li><strong>Actores.</strong> Quién ocupó cada posición —captador, administrador, revisor, contador, proveedor, afectado— y qué consecuencia jurídica arrastra esa posición.</li>
      <li><strong>Rutas.</strong> Qué vías están abiertas, cuáles ya precluyeron y en qué orden conviene activarlas.</li>
    </ul>
    <p class="prose" style="margin-top:1.2rem">Este es el trabajo de las primeras semanas. Todo lo demás depende de él.</p>
  </div>
</section>

{section("""
  <p class="eyebrow">Las dos líneas y la regla</p>
  <h2>Defendemos las dos orillas. Nunca en el mismo proceso.</h2>
  <div class="prose" style="margin-top:1.2rem">
    <p>El despacho atiende dos líneas de trabajo opuestas: la defensa integral del investigado, vinculado o imputado, y la recuperación integral del afectado. Ambas exigen el mismo conocimiento técnico del fenómeno, y por eso ambas viven en la misma firma.</p>
  </div>
  <div class="conflict">
    <p><strong>Y por eso mismo existe una regla que no admite excepción:</strong> las dos líneas jamás se prestan dentro del mismo proceso de intervención. El conflicto de interés sería evidente. El portafolio dual opera sobre casos distintos, y cada consulta entrante pasa por un protocolo interno de verificación de conflicto antes de aceptarse.</p>
  </div>
  <p class="prose" style="margin-top:1.2rem">Si una consulta corresponde a un proceso en el que la firma ya interviene por la orilla contraria, se declina y se explica por qué.</p>
""")}

<section class="section band">
  <div class="container">
    <h2>Lo que no hacemos</h2>
    <ul class="negations">
      <li>No prometemos recuperación ni desenlace judicial. Ningún despacho puede hacerlo, y en esta materia hacerlo es además un problema disciplinario.</li>
      <li>No aceptamos casos de las dos orillas en el mismo proceso.</li>
      <li>No publicamos casos identificables ni cifras de damnificados, aunque sean públicos.</li>
      <li>No trabajamos captación masiva como una especialidad más dentro de un portafolio general.</li>
    </ul>
  </div>
</section>

{section(f"""
  <h2>El equipo</h2>
  <p class="lead" style="margin-top:1rem;max-width:56ch">Cinco socios con prácticas complementarias. Los títulos, las especializaciones y los cargos están publicados.</p>
  <div class="cta-row">
    <a class="btn btn--primary" href="/equipo/">Conocer al equipo</a>
    <a class="btn btn--ghost" href="/contacto/">Solicitar una consulta</a>
  </div>
""", cls="band-2")}
'''
    add("/firma/", {
        "title": "La firma · Veraly Grupo Jurídico",
        "description": "Cómo trabaja Veraly los procesos por captación masiva en sus tres frentes: administrativo, penal y civil.",
        "active": "firma",
    }, firma_body)

    # =====================================================================
    # /equipo
    # =====================================================================
    fichas = ""
    for s in SOCIOS:
        fichas += f'''<a class="socio" href="/equipo/{s["slug"]}/" data-socio="{s["slug"]}">
  <span class="nombre">{esc(s["nombre"])}</span>
  <span class="practica">{esc(s["practica"])}</span>
  <p style="color:var(--dim);margin:.4rem 0 0;font-size:var(--step-0)">{esc(s["aporte"])}</p>
  <span class="arrowlink">Ver ficha completa</span>
</a>'''
    equipo_body = f'''
{section("""
  <p class="eyebrow">El equipo</p>
  <h1>Cinco socios, cinco prácticas, un mismo caso</h1>
  <p class="support" style="max-width:52ch">La convergencia de prácticas que sostiene el método de la firma no es un principio abstracto: es su composición. Cada socio aporta una rama del derecho al mismo expediente.</p>
""", cls="hero")}

<section class="section band">
  <div class="container">
    <div class="socios">{fichas}</div>
  </div>
</section>

{section("""
  <h2>Por qué cinco y no uno</h2>
  <div class="prose" style="margin-top:1.2rem">
    <p>Un proceso por captación masiva produce, en paralelo, una actuación ante la Superintendencia de Sociedades, un proceso penal, demandas civiles de responsabilidad, controversias societarias sobre actos anteriores a la toma de posesión, contingencias tributarias sobre los flujos y reclamaciones laborales de la intervenida. Ningún abogado cubre eso solo. Esta firma se compuso para cubrirlo.</p>
  </div>
  <div class="cta-row"><a class="btn btn--primary" href="/contacto/">Solicitar una consulta</a></div>
""")}
'''
    add("/equipo/", {
        "title": "Socios · Veraly Grupo Jurídico",
        "description": "Formación, especializaciones y práctica de los cinco socios fundadores de Veraly Grupo Jurídico.",
        "active": "equipo",
    }, equipo_body)

    # =====================================================================
    # /equipo/{socio}
    # =====================================================================
    for s in SOCIOS:
        firmados = [a for a in ARTICLES if a["author"] == s["slug"]]
        if firmados:
            lst = "".join(
                f'<a href="/analisis/{a["slug"]}/"><span class="tag">{esc(a["tema"])}</span>'
                f'<span><span class="t">{esc(a["h1"])}</span></span></a>'
                for a in firmados)
            firmados_html = f'<div class="editorial">{lst}</div>'
        else:
            firmados_html = '<p style="color:var(--dim-2)">Sin análisis firmados por el momento.</p>'

        socio_body = f'''
{crumbs([("Inicio", "/"), ("Equipo", "/equipo/"), (s["nombre"], None)])}
{section(f"""
  <h1>{esc(s["nombre"])}</h1>
  <p class="support">{esc(s["practica"])} · Socio fundador, Veraly Grupo Jurídico</p>
""", cls="hero", tight=True)}

<section class="section band">
  <div class="container prose">
    <h2>Formación</h2>
    <p style="color:var(--dim-2)"><em>Títulos, universidades y especializaciones pendientes de aporte del despacho (§17, pendiente 03). No se inventan.</em></p>
    <h2>Su práctica en casos de captación masiva</h2>
    <p>{esc(s["aporte"])}</p>
    <h2>Análisis firmados</h2>
    {firmados_html}
    <div class="cta-row" style="margin-top:2rem">
      <a class="btn btn--primary" href="/contacto/">Solicitar una consulta</a>
      <a class="btn btn--ghost" href="/equipo/">Volver al equipo</a>
    </div>
  </div>
</section>
'''
        add("/equipo/" + s["slug"] + "/", {
            "title": f'{s["nombre"]} · Socio · Veraly Grupo Jurídico',
            "description": f'Práctica de {s["nombre"]} en {s["practica"].lower()} y su función en procesos por captación masiva y habitual.',
            "active": "equipo", "og_type": "profile",
            "schema": [person_schema(s), breadcrumb_schema([
                ("Inicio", "/"), ("Equipo", "/equipo/"), (s["nombre"], "/equipo/" + s["slug"] + "/")])],
        }, socio_body)

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
""", cls="hero", tight=True)}

<section class="section band">
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
