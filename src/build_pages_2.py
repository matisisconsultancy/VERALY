# -*- coding: utf-8 -*-
"""Capa 1: /firma, /equipo, /equipo/{socio}, /contacto."""

def build(g):
    add = g["add"]; esc = g["esc"]; SITE = g["SITE"]; SOCIOS = g["SOCIOS"]
    ARTICLES = g["ARTICLES"]; socio_by_slug = g["socio_by_slug"]
    section = g["section"]; crumbs = g["crumbs"]; contact_form = g["contact_form"]
    trust_list = g["trust_list"]; person_schema = g["person_schema"]
    breadcrumb_schema = g["breadcrumb_schema"]; B = g["B"]
    PRACTICAS = g["PRACTICAS"]; agendar = g["agendar_btn"]

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
    # /equipo  (composición por prácticas, sin nombres — decisión del cliente)
    # =====================================================================
    practicas_html = ""
    for pr in PRACTICAS:
        practicas_html += f'''<div class="socio">
  <span class="practica">{esc(pr["rama"])}</span>
  <p style="color:var(--dim);margin:.4rem 0 0;font-size:var(--step-0)">{esc(pr["aporte"])}</p>
</div>'''
    equipo_body = f'''
{section("""
  <p class="eyebrow">El equipo</p>
  <h1>Cinco prácticas, un mismo caso</h1>
  <p class="support" style="max-width:52ch">El método de la firma no es un principio abstracto: es su composición. Cinco socios aportan cinco ramas del derecho al mismo expediente, y el caso se construye en la intersección.</p>
""", cls="hero")}

<section class="section band">
  <div class="container">
    <div class="socios">{practicas_html}</div>
  </div>
</section>

{section(f"""
  <h2>Por qué cinco y no uno</h2>
  <div class="prose" style="margin-top:1.2rem">
    <p>Un proceso por captación produce, en paralelo, una actuación ante la Superintendencia de Sociedades, un proceso penal, demandas civiles de responsabilidad, controversias societarias, contingencias tributarias sobre los flujos y reclamaciones laborales de la intervenida. Ningún abogado cubre eso solo. Esta firma se compuso para cubrirlo.</p>
  </div>
  <div class="cta-row">{agendar("Agendar una consulta")}<a class="btn btn--ghost" href="/firma/">Cómo trabajamos</a></div>
""")}
'''
    add("/equipo/", {
        "title": "El equipo · Veraly Grupo Jurídico",
        "description": "La firma se compone de cinco prácticas del derecho que convergen sobre el mismo expediente de captación masiva.",
        "active": "equipo",
    }, equipo_body)

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
