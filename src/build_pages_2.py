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
    faq_block = g["faq_block"]; faq_schema = g["faq_schema"]
    globe = g["globe_svg"]; wave = g["wave_svg"]

    # Info de cada situación para las tarjetas dentro de las páginas de práctica
    SITU_INFO = {
        "/afectados-por-captacion-masiva/": ("Afectado", "Recuperación",
            "Vías administrativa, penal y civil, y los plazos que corren desde la toma de posesión.", globe),
        "/defensa-en-captacion-masiva/": ("Investigado o vinculado", "Defensa",
            "Defensa en los tres frentes para investigados, administradores, revisores y proveedores.", wave),
        "/cumplimiento-en-recaudo-masivo/": ("Empresa", "Cumplimiento",
            "Revisión de encuadre frente a los umbrales de captación antes de que la revise una superintendencia.", globe),
    }
    def situ_card(title, url):
        label, pill, desc, media = SITU_INFO[url]
        return (f'<a class="acard" href="{url}">'
                f'<span class="acard-label">{esc(label)}</span>'
                f'<h3 class="acard-title">{esc(title)}</h3>'
                f'<p class="acard-desc">{esc(desc)}</p>'
                f'<span class="acard-tag">{esc(pill)}</span></a>')

    def faq_numbered(items, open_all=False):
        rows = ""
        op = " open" if open_all else ""
        for i, (q, a) in enumerate(items, 1):
            rows += (f'<details class="qa"{op}><summary>'
                     f'<span class="qa-n">{i:02d}</span><span class="qa-q">{esc(q)}</span>'
                     f'<span class="qa-ic" aria-hidden="true"></span></summary>'
                     f'<div class="qa-a">{a}</div></details>')
        return f'<div class="qa-list">{rows}</div>'

    # =====================================================================
    # /firma
    # =====================================================================
    def no_hacemos_section():
        I = {
            "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="8.2"/><circle cx="12" cy="12" r="3.4"/></svg>',
            "merge": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="8.5" cy="12" r="5"/><circle cx="15.5" cy="12" r="5"/></svg>',
            "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 12S6 5.8 12 5.8 21.5 12 21.5 12 18 18.2 12 18.2 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="2.6"/></svg>',
            "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="M3 13.5l9 5 9-5"/></svg>',
            "scales": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v16M6 20h12M5 8h14"/><path d="M5 8 2.6 13a2.9 2.9 0 0 0 4.8 0Z"/><path d="M19 8l-2.4 5a2.9 2.9 0 0 0 4.8 0Z"/></svg>',
            "form": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="5.5" y="3.5" width="13" height="17" rx="2.2"/><path d="M9 8.5h6M9 12h6M9 15.5h3.5"/></svg>',
        }
        items = [
            (I["target"], "No prometemos resultados.",
             "No prometemos recuperación ni desenlace judicial: se promete rigor, criterio y trabajo, con los límites dichos en voz alta."),
            (I["merge"], "No mezclamos las dos orillas.",
             "La defensa del investigado y la recuperación del afectado nunca se prestan dentro del mismo proceso de intervención."),
            (I["eye"], "No exponemos casos.",
             "No publicamos casos identificables, testimonios ni cifras de damnificados. Escribimos sobre la figura, nunca sobre personas."),
            (I["layers"], "No somos un portafolio general.",
             "No tratamos la captación masiva como una especialidad más entre muchas: es el único fenómeno sobre el que trabaja la firma."),
            (I["scales"], "No la litigamos como una estafa.",
             "No trabajamos la captación como si fuera una estafa agravada. Es una figura jurídica distinta, con vías y plazos propios."),
            (I["form"], "No capturamos su caso en un formulario.",
             "El primer contacto no pide los hechos por escrito: se conversan. Los datos se tratan conforme a la Ley 1581 de 2012."),
        ]
        cards = "".join(
            f'<div class="nh-card reveal-up">'
            f'<span class="nh-n">{i:02d}</span>'
            f'<h3 class="nh-t">{esc(t)}</h3><p class="nh-d">{esc(d)}</p></div>'
            for i, (ico, t, d) in enumerate(items, 1))
        return (
            '<section class="section band nh-sec">'
            '<div class="container">'
            '<div class="nh-head">'
            '<p class="eyebrow nh-eyebrow">Nuestros límites</p>'
            '<h2 class="nh-title">Lo que <span class="pr-accent">no hacemos.</span></h2>'
            '</div>'
            f'<div class="nh-grid">{cards}</div>'
            '</div></section>')

    # Método (hechos, actores, rutas) con el diagramado del timeline "El marco"
    _metodo = [
        ("Hechos", "Qué ocurrió, con qué documentos, en qué fechas y con qué trazabilidad financiera."),
        ("Actores", "Quién ocupó cada posición y qué consecuencia jurídica arrastra."),
        ("Rutas", "Qué vías están abiertas, cuáles precluyeron y en qué orden activarlas."),
    ]
    tl_video_media = g["tl_video_media"]
    hero_media = g["hero_media"]
    metodo_rows = "".join(
        f'<div class="pr-tl-row"><span class="pr-tl-label">{esc(t)}</span>'
        f'<div class="pr-tl-body"><p class="pr-tl-desc">{esc(d)}</p></div>'
        f'{tl_video_media()}</div>'
        for i, (t, d) in enumerate(_metodo))

    firma_body = f'''
{section("""
  <p class="eyebrow">La firma</p>
  <span class="prac-rule" aria-hidden="true"></span>
  <h1 class="prac-h1" style="max-width:24ch">Una firma construida sobre un solo fenómeno jurídico.</h1>
  <p class="prac-sub">Veraly Grupo Jurídico entiende el fraude financiero en toda su complejidad y defiende a quien lo enfrenta, haya perdido lo que invirtió o se encuentre bajo investigación, con la lectura completa de un equipo que trabaja el caso desde cada una de las ramas del derecho que lo atraviesan.</p>
""", cls="hero hero--vh")}

<section class="section section-light">
  <div class="container pr-two">
    <div class="pr-two-l">
      <p class="eyebrow-num">El fenómeno</p>
      <h2 class="pr-big pr-parallax">Qué es la captación <span class="pr-accent">masiva y habitual.</span></h2>
    </div>
    <div class="pr-two-r">
      <p>Hay captación masiva y habitual cuando el pasivo para con el público está compuesto por obligaciones con más de veinte (20) personas o por más de cincuenta (50) obligaciones y, además, concurre una de dos condiciones: que lo recibido supere el cincuenta por ciento (50 %) del patrimonio líquido, o que las operaciones provengan de ofertas públicas o privadas a personas innominadas (artículo 2.18.2.1 del Decreto 1068 de 2015). A ello se suma el criterio material del artículo 6 del Decreto 4334 de 2008: recibir dineros del público entregando a cambio rendimientos sin explicación financiera razonable.</p>
      <p>Es un fenómeno denso y ruidoso, y por eso se litiga mal: la mayoría de las firmas lo trata como una estafa agravada. No lo es.</p>
    </div>
  </div>
</section>

<section class="section section-light">
  <div class="container">
    <p class="eyebrow">Las tres vías</p>
    <h2 style="max-width:22ch">Tres responsabilidades que corren al mismo tiempo</h2>
    <p class="lead" style="margin-top:1rem;max-width:62ch;color:var(--dim)">Una misma conducta puede abrir tres procesos: administrativo, civil y penal. Están disponibles y pueden complementarse, pero no siempre conviene activarlos al mismo tiempo ni de la misma manera para todos los afectados. La estrategia está en definir cuál activar, cuándo y contra quién. Una firma que atiende solo una de las tres vías trabaja un tercio del problema.</p>
    <div style="margin-top:1.4rem">{g["tres_vias_rows"]()}</div>
  </div>
</section>

<section class="section section-light">
  <div class="container">
    <p class="eyebrow-num">El método de convergencia</p>
    <h2 class="pr-big">Leemos cada expediente en <span class="pr-accent">hechos, actores y rutas.</span></h2>
    <p class="prac-sub">Lo habitual es asignar el caso al socio de la especialidad correspondiente. En captación esa estructura falla: el caso no tiene una especialidad, tiene varias a la vez. Por eso las cinco prácticas trabajan el mismo expediente y el caso se construye en la intersección —a partir de tres lecturas.</p>
    <div class="pr-timeline">{metodo_rows}</div>
  </div>
</section>

{g["marco_reveal"](
    eyebrow="Las dos líneas y la regla",
    phrases=[
        "Defendemos las dos orillas. || Nunca en el mismo proceso.",
        "La defensa y la recuperación || no caben en una misma intervención.",
        "Cada consulta pasa por || verificación previa de conflicto.",
    ],
    cards=[],
    section_id="dos-lineas",
)}

{no_hacemos_section()}

{section(f"""
  <h2>El equipo</h2>
  <p class="lead" style="margin-top:1rem;max-width:56ch">Cinco prácticas aportan cinco ramas del derecho al mismo expediente.</p>
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
    # Fuentes oficiales (best-effort — la firma debe verificar cada enlace).
    _U = {
        "d4334": "http://www.secretariasenado.gov.co/senado/basedoc/decreto_4334_2008.html",
        "cp": "http://www.secretariasenado.gov.co/senado/basedoc/ley_0599_2000_pr012.html",
        "d1981": "http://www.secretariasenado.gov.co/senado/basedoc/decreto_1981_1988.html",
        "const": "http://www.secretariasenado.gov.co/senado/basedoc/constitucion_politica_1991.html",
        "ccio": "http://www.secretariasenado.gov.co/senado/basedoc/codigo_comercio.html",
        "et": "http://www.secretariasenado.gov.co/senado/basedoc/estatuto_tributario.html",
        "cst": "http://www.secretariasenado.gov.co/senado/basedoc/codigo_sustantivo_trabajo.html",
        "l906": "http://www.secretariasenado.gov.co/senado/basedoc/ley_0906_2004.html",
    }
    PRACTICAS_DEV = [
        {
            "slug": "contractual-y-constitucional",
            "rama": "Contractual y constitucional",
            "card": "El debido proceso en un trámite de única instancia y el andamiaje contractual anterior a la toma de posesión.",
            "lede": "Sus contratos y sus garantías, leídos antes de que los lea la Superintendencia de Sociedades. Revisamos cómo la autoridad va a interpretar cada acuerdo que sostuvo el negocio y defendemos el debido proceso en un trámite que no tiene segunda instancia.",
            "meta": "Contratos en procesos de captación y debido proceso ante la Superintendencia de Sociedades: lectura de mandatos, mutuos, compraventas de cartera y promesas antes de que los recalifique la autoridad, en un trámite de única instancia del Decreto 4334 de 2008.",
            "paras": [
                "En los procesos de captación masiva y habitual casi todos cometen el mismo error: esperan una segunda oportunidad que no existe, porque la intervención de la Superintendencia de Sociedades no tiene apelación, lo que allí se decide vale frente a todos y ningún juez administrativo lo revisa después, así que el debido proceso se ejerce dentro del trámite o no se ejerce.",
                "Mientras tanto, los contratos que sostenían el negocio se leen de otra manera, porque la autoridad no mira el nombre que usted les puso sino lo que en realidad fueron, y un mandato, un mutuo, una compraventa de cartera o una promesa sobre planos pueden terminar recalificados sin que nadie le pregunte. De esa lectura depende la posición de cada quien en el proceso.",
                "Por eso nuestro trabajo empieza por dos frentes al mismo tiempo: defendemos sus garantías constitucionales mientras todavía sirven y revisamos sus contratos como los va a revisar la autoridad, antes de que lo haga. A quien ya enfrenta la intervención, eso le permite saber qué resiste y qué camino le queda; a la empresa que quiere prevenirla, le da el blindaje contractual que evita que un negocio legítimo sea confundido con uno de captación.",
            ],
            "normas": [
                {"ley": "Decreto 4334 de 2008", "que": "Procedimiento de intervención de única instancia y con efectos de cosa juzgada.", "url": _U["d4334"]},
                {"ley": "Constitución Política, art. 29", "que": "Debido proceso y derecho de defensa en trámites administrativos concentrados.", "url": _U["const"]},
                {"ley": "Código de Comercio", "que": "Validez de los contratos y actos jurídicos previos a la intervención.", "url": _U["ccio"]},
            ],
            "faqs": [
                ("¿El trámite de intervención por captación tiene segunda instancia?",
                 '<p>No. El procedimiento del Decreto 4334 de 2008 es de <strong>única instancia</strong> y sus decisiones tienen efectos de cosa juzgada frente a todos. Por eso el debido proceso se ejerce dentro del mismo trámite y en los escenarios de control de legalidad disponibles, y actuar temprano es decisivo.</p>'),
                ("¿Se pueden atacar los contratos firmados antes de la toma de posesión?",
                 '<p>Según su validez. Los mandatos, mutuos, cuentas en participación o promesas anteriores a la intervención se revisan para distinguir lo lícito de lo que sostuvo la captación; de esa lectura dependen responsabilidades posteriores y el perímetro de bienes.</p>'),
                ("¿Qué garantías constitucionales aplican en un trámite tan concentrado?",
                 '<p>El debido proceso del artículo 29 de la Constitución: derecho de defensa, contradicción y control de legalidad, adaptados a un procedimiento de única instancia. Su ejercicio temprano condiciona todo el caso.</p>'),
            ],
            "serves": [("Me investigan o me vincularon", "/defensa-en-captacion-masiva/"),
                       ("Perdí dinero en un esquema", "/afectados-por-captacion-masiva/"),
                       ("Mi empresa recauda de muchas personas", "/cumplimiento-en-recaudo-masivo/")],
            "articulo": ("captacion-con-libranzas-y-factoring", "Captación montada sobre contratos legales"),
        },
        {
            "slug": "tributaria-y-migratoria",
            "rama": "Tributaria y migratoria",
            "card": "Las contingencias tributarias sobre los flujos del esquema y las consecuencias migratorias de los vinculados.",
            "lede": "Analizamos las obligaciones tributarias y la situación migratoria de personas y empresas, y en un caso de captación lo hacemos para identificar contingencias, ordenar la información relevante y orientar una estrategia coherente con los demás frentes jurídicos.",
            "meta": "Obligaciones tributarias y situación migratoria de personas y empresas en un caso de captación masiva: movimientos de dinero y declaraciones, residencia fiscal de vinculados extranjeros y contingencias ante Migración Colombia.",
            "paras": [
                "Revisamos los movimientos de dinero, las declaraciones y las obligaciones tributarias de la empresa y de las personas involucradas. Examinamos cómo están organizados sus asuntos tributarios y contables y, cuando no existe una estructura clara, ayudamos a definir una que permita identificar obligaciones, sustentar operaciones y atender los requerimientos que puedan surgir.",
                "Cuando hay personas extranjeras vinculadas al caso, evaluamos su situación migratoria, el cumplimiento de los requisitos aplicables y las posibles contingencias ante Migración Colombia. También analizamos si, según sus circunstancias, pueden tener obligaciones tributarias en Colombia, incluida la necesidad de determinar su residencia fiscal.",
                "Integramos estos análisis con las demás prácticas de la firma para que las decisiones sobre la empresa, sus recursos y las personas vinculadas al proceso tengan en cuenta sus efectos tributarios y migratorios.",
            ],
            "normas": [
                {"ley": "Estatuto Tributario", "que": "Obligaciones formales y sustanciales sobre los flujos del esquema.", "url": _U["et"]},
                {"ley": "Régimen migratorio (Decreto 1067 de 2015)", "que": "Permanencia, visados y salidas de vinculados extranjeros.", "url": None},
                {"ley": "Mecanismos de intercambio de información", "que": "Cruce de datos entre autoridades tributarias y de investigación.", "url": None},
            ],
            "faqs": [
                ("¿Un proceso por captación tiene consecuencias tributarias?",
                 '<p>Sí. Los flujos del esquema dejan obligaciones formales y sustanciales que la autoridad fiscal puede revisar de forma independiente al proceso por captación; anticiparlas evita perder en un frente lo ganado en otro.</p>'),
                ("¿La captación puede afectar la situación migratoria de un vinculado extranjero?",
                 '<p>Puede. Cuando hay vinculados extranjeros, los visados, la permanencia y las salidas del país quedan condicionados por el proceso; conviene integrar el análisis migratorio desde el inicio.</p>'),
                ("¿La información tributaria se cruza con la investigación penal?",
                 '<p>Los mecanismos de intercambio de información permiten que lo tributario y lo penal-administrativo se lean en conjunto, por lo que la estrategia debe ser coherente entre todos los frentes.</p>'),
            ],
            "serves": [("Me investigan o me vincularon", "/defensa-en-captacion-masiva/"),
                       ("Mi empresa recauda de muchos", "/cumplimiento-en-recaudo-masivo/")],
            "articulo": None,
        },
        {
            "slug": "corporativa",
            "rama": "Corporativa",
            "card": "Las controversias societarias sobre los actos anteriores a la intervención y la responsabilidad de administradores, revisores fiscales y terceros.",
            "lede": "Trabaja la vida societaria de la captadora: qué decisiones anteriores a la intervención son atacables y cómo se define la responsabilidad de administradores, revisores fiscales y terceros.",
            "meta": "Responsabilidad de administradores y validez de los actos societarios anteriores a la intervención en un esquema de captación: Código de Comercio y perímetro de la intervención del Decreto 4334 de 2008.",
            "paras": [
                "La toma de posesión congela una sociedad que, hasta el día anterior, tomaba decisiones: aumentos de capital, cesiones, garantías, operaciones entre vinculadas. Revisar la validez de esos actos societarios anteriores a la intervención define la responsabilidad de administradores, revisores fiscales y terceros.",
                "Leer la sociedad con criterio corporativo define, en la práctica, el tamaño del problema: cuánto patrimonio responde, quién responde por él y qué relaciones jurídicas conservan validez frente a la intervención.",
            ],
            "normas": [
                {"ley": "Código de Comercio", "que": "Validez de actos societarios y responsabilidad de administradores.", "url": _U["ccio"]},
                {"ley": "Decreto 4334 de 2008", "que": "Perímetro de la intervención y de los bienes que entran a la masa.", "url": _U["d4334"]},
            ],
            "faqs": [
                ("¿Responden los administradores por los actos de la sociedad captadora?",
                 '<p>Pueden responder. Se revisa la validez de las decisiones anteriores a la intervención —aumentos de capital, cesiones, garantías, operaciones entre vinculadas— y de allí se define la responsabilidad de administradores, revisores fiscales y terceros.</p>'),
                ("¿Se pueden anular operaciones societarias previas a la toma de posesión?",
                 '<p>Según su validez. El Código de Comercio permite examinar esos actos; el resultado incide en el perímetro de la intervención y en las responsabilidades que se atribuyen.</p>'),
            ],
            "serves": [("Me investigan o me vincularon", "/defensa-en-captacion-masiva/"),
                       ("Perdí dinero en un esquema", "/afectados-por-captacion-masiva/")],
            "articulo": ("que-hace-la-superintendencia-de-sociedades", "Qué hace la Superintendencia de Sociedades"),
        },
        {
            "slug": "penal-e-informatica",
            "rama": "Penal e informática",
            "card": "La defensa penal por los artículos 316 y 316A y la evidencia digital, desde los actos urgentes hasta el juicio oral.",
            "lede": "Conduce el frente penal —los artículos 316 y 316A y los delitos que suelen concurrir— y la prueba digital que hoy sostiene o desmonta la acusación.",
            "meta": "Defensa penal por captación masiva y habitual (art. 316) y no reintegro (art. 316A), delitos concurrentes y tratamiento de la evidencia digital: de los actos urgentes y la imputación al juicio oral.",
            "paras": [
                "El proceso penal por captación masiva y habitual (artículo 316 del Código Penal) y no reintegro (artículo 316A) suele venir acompañado de estafa agravada, lavado de activos y concierto para delinquir. La defensa penal se juega desde los actos urgentes y la audiencia de imputación: cada decisión temprana condiciona el juicio oral.",
                "Casi toda la prueba es digital: registros de plataformas, comunicaciones, trazas de pagos, billeteras. Tratar esa evidencia digital con criterio informático —cadena de custodia, autenticidad, alcance— es lo que permite excluir lo mal recaudado y sostener el origen lícito de lo que sí lo tiene.",
                "La combinación de derecho penal y competencia informática es la que permite discutir, a la vez, la calificación del delito y la validez de la prueba que lo sostiene. Ese doble frente es difícil de cubrir cuando la defensa se apoya en una sola especialidad.",
            ],
            "normas": [
                {"ley": "Código Penal, arts. 316 y 316A", "que": "Captación masiva y habitual (prisión de 120 a 240 meses) y no reintegro.", "url": _U["cp"]},
                {"ley": "Delitos concurrentes", "que": "Estafa agravada, lavado de activos y concierto para delinquir.", "url": _U["cp"]},
                {"ley": "Ley 906 de 2004", "que": "Régimen de la prueba, evidencia digital y cadena de custodia.", "url": _U["l906"]},
            ],
            "faqs": [
                ("¿Qué pena tiene la captación masiva y habitual?",
                 '<p>El artículo 316 del Código Penal contempla prisión de 120 a 240 meses. Suele concurrir con estafa agravada, lavado de activos y concierto para delinquir, y con el tipo autónomo de no reintegro del artículo 316A.</p>'),
                ("¿Qué es el no reintegro del artículo 316A?",
                 '<p>Es un tipo penal autónomo que sanciona no devolver los recursos captados, y puede concurrir con el artículo 316.</p>'),
                ("¿La evidencia digital se puede excluir del proceso?",
                 '<p>Sí, cuando fue mal recaudada. El tratamiento con criterio informático —cadena de custodia, autenticidad y alcance— permite excluir lo indebido y sostener el origen lícito de lo demás.</p>'),
            ],
            "serves": [("Me investigan o me vincularon", "/defensa-en-captacion-masiva/")],
            "articulo": ("diferencia-entre-estafa-y-captacion-masiva", "Diferencia entre estafa y captación masiva"),
        },
        {
            "slug": "empresarial-y-laboral",
            "rama": "Empresarial y laboral",
            "card": "El análisis de la operación de la empresa y sus relaciones laborales para identificar obligaciones y anticipar contingencias en un caso de captación.",
            "lede": "Analizamos la operación de la empresa y sus relaciones laborales para identificar obligaciones, anticipar contingencias y orientar la estrategia jurídica en casos de captación.",
            "meta": "Operación de la empresa y relaciones laborales en un caso de captación: estructura societaria, contratos y vínculos con trabajadores, comisionistas y colaboradores dentro del proceso de intervención.",
            "paras": [
                "Comprender cómo operaba la empresa es fundamental para analizar el caso. Revisamos su estructura, sus contratos y las relaciones entre socios, administradores y terceros para identificar los compromisos asumidos y las posibles responsabilidades.",
                "En el ámbito laboral, examinamos los vínculos con trabajadores, comisionistas y colaboradores para determinar su naturaleza, las obligaciones pendientes y su tratamiento dentro del proceso de intervención.",
                "Integramos ambos frentes para evaluar cómo las decisiones empresariales y las obligaciones laborales inciden en la situación de la sociedad y de las personas vinculadas al caso.",
            ],
            "normas": [
                {"ley": "Código de Comercio", "que": "Estructura de la empresa, contratos y responsabilidad de administradores.", "url": _U["ccio"]},
                {"ley": "Código Sustantivo del Trabajo", "que": "Vínculos laborales, obligaciones pendientes y prelación de créditos.", "url": _U["cst"]},
                {"ley": "Decreto 4334 de 2008", "que": "Concurrencia de acreencias con la masa de la intervención.", "url": _U["d4334"]},
            ],
            "faqs": [
                ("¿Por qué revisar la operación de la empresa en un caso de captación?",
                 '<p>Comprender cómo operaba la empresa —su estructura, sus contratos y las relaciones entre socios, administradores y terceros— permite identificar los compromisos asumidos y las posibles responsabilidades dentro del proceso.</p>'),
                ("¿Qué pasa con los empleados de la sociedad intervenida?",
                 '<p>La intervención interrumpe las relaciones laborales; examinar los vínculos con trabajadores, comisionistas y colaboradores permite determinar su naturaleza, las obligaciones pendientes y su tratamiento dentro del proceso.</p>'),
                ("¿Cómo se ubican las acreencias laborales frente a los afectados?",
                 '<p>El Código Sustantivo del Trabajo establece una prelación de créditos laborales que debe leerse junto con la masa de la intervención y las demás acreencias.</p>'),
            ],
            "serves": [("Perdí dinero en un esquema", "/afectados-por-captacion-masiva/"),
                       ("Me investigan o me vincularon", "/defensa-en-captacion-masiva/")],
            "articulo": None,
        },
    ]

    # --- hub /equipo: titular grande + filas numeradas (referente Expertise) ---
    prac_rows = ""
    for i, pr in enumerate(PRACTICAS_DEV, 1):
        prac_rows += f'''<a class="prac-row" href="/equipo/{pr["slug"]}/">
  <span class="pr-n">{i:02d}</span>
  <span class="pr-t">{esc(pr["rama"])}</span>
  <span class="pr-d">{esc(pr["card"])}</span>
  <span class="pr-go" aria-hidden="true"></span>
</a>'''
    equipo_body = f'''
{section("""
  <p class="eyebrow">Áreas de práctica</p>
  <span class="prac-rule" aria-hidden="true"></span>
  <h1 class="prac-h1">Cinco prácticas al servicio de su defensa.</h1>
  <p class="prac-sub">Cada proceso por captación abre a la vez frentes administrativos, penales, civiles, societarios, tributarios y laborales. La firma los cubre con cinco prácticas que trabajan el mismo expediente.</p>
""", cls="hero", hero_v=2)}

<section class="prac-rows-sec">
  <div class="prac-rows">{prac_rows}</div>
  <div class="container">
    <div class="equipo-cta">
      <div>
        <p class="eyebrow">Las personas</p>
        <h2 class="pr-big">Detrás de las cinco prácticas, <span class="pr-accent">un equipo.</span></h2>
      </div>
      <a class="btn btn--primary" href="/equipo/socios/">Equipo</a>
    </div>
  </div>
</section>
'''
    add("/equipo/", {
        "title": "El equipo · Las cinco prácticas · Veraly Grupo Jurídico",
        "description": "La firma se compone de cinco prácticas del derecho que convergen sobre el mismo expediente de captación masiva: constitucional, penal, corporativa, tributaria y laboral.",
        "active": "equipo", "body_class": "theme-light",
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

    # --- páginas de desarrollo por práctica: contenido + normatividad + FAQ ---
    for _pi, pr in enumerate(PRACTICAS_DEV):
        url = "/equipo/" + pr["slug"] + "/"
        paras = "".join(f"<p>{esc(t)}</p>" for t in pr["paras"])
        # timeline de normatividad (etiqueta · descripción+enlace · imagen)
        norm_rows = ""
        _media_cycle = [globe, wave]
        for i, n in enumerate(pr["normas"]):
            go = (f'<a class="pr-tl-go" href="{n["url"]}" target="_blank" rel="noopener">Ver norma <i>↗</i></a>'
                  if n.get("url") else '')
            media = _media_cycle[i % 2]()
            norm_rows += (f'<div class="pr-tl-row"><span class="pr-tl-label">{esc(n["ley"])}</span>'
                          f'<div class="pr-tl-body"><p class="pr-tl-desc">{esc(n["que"])}</p>{go}</div>'
                          f'{tl_video_media()}</div>')
        art = ""
        if pr["articulo"]:
            aslug, atitle = pr["articulo"]
            art = f'<p class="pr-more"><a class="arrowlink" href="/analisis/{aslug}/">Análisis · {esc(atitle)}</a></p>'
        situ_cards_html = "".join(situ_card(t, u) for t, u in pr["serves"])
        practica_body = f'''
{section(crumbs([("Inicio", "/"), ("El equipo", "/equipo/"), (pr["rama"], None)], inline=True) + f"""
  <p class="eyebrow">Una de las cinco prácticas</p>
  <span class="prac-rule" aria-hidden="true"></span>
  <h1 class="prac-h1">{esc(pr["rama"])}</h1>
  <p class="prac-sub">{esc(pr["lede"])}</p>
""", cls="hero", tight=True, hero_v=(_pi % 4) + 1)}

{practica_nav(pr["slug"])}

<section class="section">
  <div class="container pr-two">
    <div class="pr-two-l">
      <p class="eyebrow-num">Qué resuelve</p>
      <h2 class="pr-big pr-parallax">Qué resuelve esta práctica <span class="pr-accent">en un caso de captación.</span></h2>
    </div>
    <div class="pr-two-r">
      {paras}
      {art}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="eyebrow-num">A qué situación sirve</p>
    <h2 class="pr-big">Desde dónde entra <span class="pr-accent">su caso.</span></h2>
    <div class="acards">{situ_cards_html}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="eyebrow-num">Las normas de esta práctica</p>
    <h2 class="pr-big">El marco que <span class="pr-accent">enmarca esta práctica.</span></h2>
    <div class="pr-timeline">{norm_rows}</div>
  </div>
</section>

<section class="section">
  <div class="container faq-two">
    <div class="faq-two-l">
      <p class="faq-pill"><span class="dot" aria-hidden="true"></span>Preguntas sobre esta práctica</p>
      <h2 class="pr-big">¿Dudas? <span class="pr-accent">Estamos para ayudar.</span></h2>
    </div>
    <div class="faq-two-r">{faq_numbered(pr["faqs"])}</div>
  </div>
</section>
'''
        add(url, {
            "title": f'{pr["rama"]} en captación masiva · Veraly Grupo Jurídico',
            "description": pr["meta"],
            "active": "equipo", "body_class": "theme-light",
            "schema": [
                service_schema(
                    pr["rama"] + " en captación masiva", pr["meta"], url, pr["rama"]),
                faq_schema(pr["faqs"]),
                breadcrumb_schema([("Inicio", "/"), ("El equipo", "/equipo/"),
                                   (pr["rama"], url)]),
            ],
        }, practica_body)

    # =====================================================================
    # /equipo/socios  — el equipo (personas); se llega con el botón "Equipo"
    # Retratos generativos como placeholder (hover: escala de grises -> color
    # + acercamiento); se reemplazan por fotografías reales cuando estén.
    # =====================================================================
    def socio_portrait(s):
        p = s["nombre"].split()
        ini = (p[0][0] + (p[-1][0] if len(p) > 1 else "")).upper()
        sid = s["slug"]
        return (
            f'<svg class="socio-ph" viewBox="0 0 320 400" preserveAspectRatio="xMidYMid slice" '
            f'role="img" aria-label="Retrato de {esc(s["nombre"])}">'
            f'<defs><linearGradient id="g-{sid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="#0A4A50"/><stop offset="1" stop-color="#03191B"/></linearGradient>'
            f'<radialGradient id="r-{sid}" cx="0.5" cy="0.34" r="0.75">'
            f'<stop offset="0" stop-color="#89F5E5" stop-opacity="0.30"/>'
            f'<stop offset="1" stop-color="#89F5E5" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="320" height="400" fill="url(#g-{sid})"/>'
            f'<rect width="320" height="400" fill="url(#r-{sid})"/>'
            f'<text x="160" y="230" text-anchor="middle" font-family="Archivo,sans-serif" '
            f'font-weight="300" font-size="128" letter-spacing="2" fill="#D9F6EF" fill-opacity="0.92">{esc(ini)}</text>'
            f'</svg>')
    socio_cards = ""
    for s in SOCIOS:
        socio_cards += (
            f'<a class="socio-card" href="/equipo/socios/{s["slug"]}/">'
            f'<span class="socio-photo">{socio_portrait(s)}</span>'
            f'<span class="socio-meta"><span class="socio-name">{esc(s["nombre"])}</span>'
            f'<span class="socio-rama">{esc(s["practica"])}</span></span></a>')
    equipo_socios_body = f'''
{section("""
  <p class="eyebrow">El equipo</p>
  <span class="prac-rule" aria-hidden="true"></span>
  <h1 class="prac-h1">El equipo detrás <span class="pr-accent">de cada expediente.</span></h1>
  <p class="prac-sub">Las personas que trabajan cada práctica del derecho sobre el mismo expediente de captación masiva. Conozca a quienes construyen la defensa.</p>
""", cls="hero", tight=True)}

<section class="socios-grid-sec">
  <div class="socios-grid">{socio_cards}</div>
  <div class="container">
    <div class="cta-row" style="margin-top:clamp(40px,6vw,72px)"><a class="btn btn--ghost" href="/equipo/">Volver a las prácticas</a>{agendar("Agendar una consulta")}</div>
  </div>
</section>
'''
    add("/equipo/socios/", {
        "title": "El equipo · Los socios · Veraly Grupo Jurídico",
        "description": "El equipo de Veraly Grupo Jurídico y la práctica del derecho que cada integrante aplica a la defensa en captación masiva.",
        "active": "equipo", "body_class": "theme-light",
        "schema": [breadcrumb_schema([("Inicio", "/"), ("El equipo", "/equipo/"), ("Los socios", "/equipo/socios/")])],
    }, equipo_socios_body)

    for i, s in enumerate(SOCIOS):
        nxt = SOCIOS[(i + 1) % len(SOCIOS)]
        url = "/equipo/socios/" + s["slug"] + "/"
        practica_lc = s["practica"][0].lower() + s["practica"][1:]
        socio_body = f'''
<section class="section socio-detail">
  <div class="container">
    <p class="backlink"><a href="/equipo/socios/"><span class="ico-ar ico-ar--l" aria-hidden="true"></span> Volver al equipo</a></p>
    <div class="socio-hero">
      <div class="socio-hero-photo"><span class="socio-photo socio-photo--lg">{socio_portrait(s)}</span></div>
      <div class="socio-hero-txt">
        <p class="eyebrow-num">Socio</p>
        <h1 class="socio-h1">{esc(s["nombre"])}</h1>
        <p class="socio-role">Socio · {esc(s["practica"])}</p>
        <div class="socio-bio">
          <p>{esc(s["nombre"])} integra en la firma la práctica de {esc(practica_lc)}.</p>
          <p>{esc(s["aporte"])}</p>
          <p>Su trabajo se articula con las demás prácticas sobre el mismo expediente: en un proceso por captación masiva, ninguna defensa se sostiene desde un solo frente.</p>
        </div>
        <div class="socio-contact">
          <span class="ci-k">Contacto</span>
          <p class="ci-v"><a href="mailto:{SITE["email"]}">{esc(SITE["email"])}</a></p>
        </div>
      </div>
    </div>
  </div>
  <a class="socio-next" href="/equipo/socios/{nxt["slug"]}/">
    <span class="sn-k">Siguiente miembro</span>
    <span class="sn-name">{esc(nxt["nombre"])} <span class="ico-ar" aria-hidden="true"></span></span>
  </a>
</section>
'''
        add(url, {
            "title": f'{s["nombre"]} · Socio · Veraly Grupo Jurídico',
            "description": f'{s["nombre"]}, socio de Veraly Grupo Jurídico en {practica_lc}, aplicada a la defensa en captación masiva.',
            "active": "equipo", "body_class": "theme-light",
            "schema": [
                person_schema(s),
                breadcrumb_schema([("Inicio", "/"), ("El equipo", "/equipo/"),
                                   ("Los socios", "/equipo/socios/"), (s["nombre"], url)]),
            ],
        }, socio_body)

    # =====================================================================
    # /marca  (brandbook — pieza de verificación)
    # =====================================================================
    # (Las páginas /marca/ y /marca/sistema/ se retiraron del sitio público:
    #  el manual de marca es un documento de trabajo interno de la firma.)

    # =====================================================================
    # /contacto
    # =====================================================================
    maps_q = "https://www.google.com/maps/search/?api=1&query=Calle+16+%234-68+oficina+1204+Bogot%C3%A1"
    wa_contact = (f'<a class="btn btn--ghost" href="https://wa.me/{SITE["whatsapp"]}" target="_blank" rel="noopener" data-whatsapp data-pos="contacto">WhatsApp</a>'
                  if SITE["whatsapp"] else '')
    contacto_body = f'''
<section class="contact-hero">
  {hero_media(3)}
  <div class="contact-hero-bg" aria-hidden="true">{g["wave_svg"]()}</div>
  <div class="container contact-hero-in">
    <p class="eyebrow">Contacto</p>
    <h1 class="contact-hero-h1">No dude en <span class="pr-accent">contactarnos.</span></h1>
    <p class="contact-hero-sub">Para cualquier solicitud de información o para agendar una primera conversación, la firma queda a su disposición.</p>
  </div>
</section>

<section class="section">
  <div class="container contact-cols">
    <aside class="contact-info">
      <div class="ci-block">
        <span class="ci-k">Dirección</span>
        <p class="ci-v">Calle 16 # 4-68<br>Oficina 1204<br>Bogotá, Colombia</p>
        <a class="arrowlink" href="{maps_q}" target="_blank" rel="noopener">Cómo llegar</a>
      </div>
      <div class="ci-block">
        <span class="ci-k">Teléfono</span>
        <p class="ci-v"><a href="tel:{SITE["phone_href"]}" data-pos="contacto">{esc(SITE["phone_display"])}</a></p>
      </div>
      <div class="ci-block">
        <span class="ci-k">Correo</span>
        <p class="ci-v"><a href="mailto:{SITE["email"]}">{esc(SITE["email"])}</a></p>
      </div>
      <div class="ci-block">
        <span class="ci-k">Horario</span>
        <p class="ci-v">Lunes a viernes · 8:00 – 18:00</p>
      </div>
    </aside>
    <div class="contact-main">
      <div class="contact-block">
        <span class="ci-k">Escríbanos</span>
        <p class="contact-lead">Cuéntenos en una línea su situación y cómo contactarlo. Respondemos dentro de 24 horas hábiles, tras verificar el conflicto de interés.</p>
        {contact_form("contacto", "Enviar mensaje")}
      </div>
      <div class="contact-block contact-agenda">
        <span class="ci-k">Agendar una cita</span>
        <p class="contact-lead">O reserve directamente una primera conversación en el calendario de la firma.</p>
        <div class="cta-row">{agendar("Agendar una cita")}{wa_contact}</div>
        <div id="cal-inline" class="cal-inline" aria-live="polite"></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight contact-trust-sec">
  <div class="container">
    <ul class="trust-row">
      <li><span class="tr-k">24 h</span><p class="tr-d">Respondemos toda consulta dentro de las 24 horas hábiles siguientes.</p></li>
      <li><span class="tr-k">Conflicto</span><p class="tr-d">Verificamos el conflicto de interés antes de aceptar cualquier caso.</p></li>
      <li><span class="tr-k">Ley 1581</span><p class="tr-d">Sus datos se tratan conforme a la ley de protección de datos personales.</p></li>
    </ul>
  </div>
</section>

<section class="contact-map-sec" aria-label="Ubicación de la oficina">
  <div class="container">
    <div class="map-frame">
      <iframe title="Mapa de la oficina de Veraly Grupo Jurídico en Bogotá" loading="lazy"
        referrerpolicy="no-referrer-when-downgrade" allowfullscreen
        src="https://maps.google.com/maps?q=Calle%2016%20%234-68%2C%20Bogot%C3%A1%2C%20Colombia&z=16&output=embed"></iframe>
    </div>
    <p class="map-note">Calle 16 # 4-68, oficina 1204 · Bogotá, Colombia · <a class="textlink" href="{maps_q}" target="_blank" rel="noopener">Cómo llegar</a></p>
  </div>
</section>
'''
    add("/contacto/", {
        "title": "Contacto · Veraly Grupo Jurídico",
        "description": "Reserve una primera conversación con Veraly Grupo Jurídico en Bogotá. Verificación previa de conflicto de interés.",
        "active": "contacto",
    }, contacto_body)
