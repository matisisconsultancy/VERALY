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
                f'<span class="acard-tag">{esc(pill)}</span>'
                f'<div class="acard-media">{media()}</div></a>')

    def faq_numbered(items):
        rows = ""
        for i, (q, a) in enumerate(items, 1):
            rows += (f'<details class="fq-item"><summary>'
                     f'<span class="fq-n">{i}</span><span class="fq-q">{esc(q)}</span>'
                     f'<span class="fq-ic" aria-hidden="true"></span></summary>'
                     f'<div class="fq-a">{a}</div></details>')
        return f'<div class="fq-list">{rows}</div>'

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
            f'<span class="nh-n">/ {i:02d}</span>'
            f'<span class="nh-ico" aria-hidden="true">{ico}<span class="nh-strike"></span></span>'
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

    # Filas numeradas de las cinco prácticas (mismo diagramado que el hub /equipo)
    _prac_slugs = ["contractual-y-constitucional", "tributaria-y-migratoria",
                   "corporativa-y-urbana", "penal-e-informatica", "laboral-y-de-seguros"]
    firma_prac_rows = "".join(
        f'<a class="prac-row" href="/equipo/{_prac_slugs[i]}/">'
        f'<span class="pr-n">{i+1:02d}</span>'
        f'<span class="pr-t">{esc(pr["rama"])}</span>'
        f'<span class="pr-d">{esc(pr["aporte"])}</span>'
        f'<span class="pr-go" aria-hidden="true">→</span></a>'
        for i, pr in enumerate(PRACTICAS))

    firma_body = f'''
{section("""
  <p class="eyebrow">La firma</p>
  <span class="prac-rule" aria-hidden="true"></span>
  <h1 class="prac-h1" style="max-width:24ch">Una firma construida sobre un solo fenómeno jurídico.</h1>
  <p class="prac-sub">Veraly Grupo Jurídico entiende el fraude financiero en toda su complejidad. Defendemos a quien lo sufre —por haber perdido lo invertido o por estar bajo investigación— con la lectura completa que da un equipo trabajando el problema desde cada una de sus ramas.</p>
""", cls="hero hero--vh")}

<section class="section section-light">
  <div class="container pr-two">
    <div class="pr-two-l">
      <p class="eyebrow-num"><span class="n">§</span>El fenómeno</p>
      <h2 class="pr-big pr-parallax">Qué es la captación <span class="pr-accent">masiva y habitual.</span></h2>
    </div>
    <div class="pr-two-r">
      <p>Consiste en recibir dineros del público sin autorización estatal, entregando a cambio bienes, servicios o rendimientos sin explicación financiera razonable (art. 6 del Decreto 4334 de 2008). Hay captación cuando el pasivo con el público supera los umbrales del Decreto 1981 de 1988 —más de veinte personas o más de cincuenta obligaciones, o mediación de ofertas masivas—.</p>
      <p>Es un fenómeno denso y ruidoso, y por eso se litiga mal: la mayoría de los despachos lo trata como una estafa agravada. No lo es.</p>
    </div>
  </div>
</section>

<section class="section section-light">
  <div class="container">
    <p class="eyebrow">Las tres vías</p>
    <h2 style="max-width:22ch">Tres responsabilidades que corren al mismo tiempo</h2>
    <p class="lead" style="margin-top:1rem;max-width:56ch;color:var(--dim)">Una misma conducta detona, de forma simultánea e independiente, tres procesos. No son fases: son frentes paralelos, y cada uno condiciona a los otros dos. Un despacho que atiende solo una de las tres vías trabaja un tercio del problema.</p>
    <div style="margin-top:1.4rem">{g["tres_vias_rows"]()}</div>
  </div>
</section>

<section class="section section-light prac-rows-sec">
  <div class="container">
    <p class="eyebrow">El método de convergencia</p>
    <span class="prac-rule" aria-hidden="true"></span>
    <h2 class="prac-h1" style="max-width:18ch">Cinco prácticas sobre el mismo expediente.</h2>
    <p class="prac-sub">Lo habitual es asignar cada caso al socio de la especialidad correspondiente. En captación esa estructura falla: el caso no tiene una especialidad, tiene varias a la vez. Veraly opera al revés —los cinco socios trabajan el mismo expediente desde sus ramas y el caso se construye en la intersección.</p>
  </div>
  <div class="prac-rows" style="margin-top:clamp(34px,5vw,66px)">{firma_prac_rows}</div>
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
            "lede": "Lee el proceso de captación desde dos planos: las garantías constitucionales del trámite y la arquitectura contractual de todo lo que ocurrió antes de la intervención.",
            "meta": "La práctica constitucional y contractual en captación masiva: debido proceso en el trámite de única instancia del Decreto 4334 de 2008, control de las decisiones de la Superintendencia de Sociedades y validez de los contratos previos a la toma de posesión.",
            "paras": [
                "El procedimiento de intervención por captación masiva y habitual del Decreto 4334 de 2008 es de única instancia y sus decisiones tienen efectos de cosa juzgada frente a todos. Esa concentración exige una lectura constitucional cuidadosa del debido proceso: cuándo se garantiza la contradicción, cómo se ejerce la defensa material dentro de un trámite tan comprimido y qué actos de la Superintendencia de Sociedades son susceptibles de control.",
                "En paralelo, el esquema casi siempre se construyó sobre contratos —mandatos, mutuos, cuentas en participación, promesas de compraventa— firmados antes de la toma de posesión. Entender ese andamiaje contractual permite distinguir lo lícito de lo que sostuvo la captación, y es la base sobre la que se apoyan las demás prácticas de la firma.",
                "El trabajo constitucional y contractual, entonces, fija el terreno: qué garantías se pueden invocar, qué decisiones administrativas se pueden controlar y qué relaciones jurídicas anteriores conservan validez. Sobre ese terreno se construyen la defensa penal, la responsabilidad civil y la recuperación del afectado.",
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
                       ("Perdí dinero en un esquema", "/afectados-por-captacion-masiva/")],
            "articulo": ("que-hace-la-superintendencia-de-sociedades", "Qué hace la Superintendencia de Sociedades"),
        },
        {
            "slug": "tributaria-y-migratoria",
            "rama": "Tributaria y migratoria",
            "card": "Las contingencias tributarias sobre los flujos del esquema y las consecuencias migratorias de los vinculados.",
            "lede": "Sigue el dinero y sigue a las personas: las contingencias fiscales que dejan los flujos del esquema y las consecuencias migratorias que alcanzan a vinculados extranjeros.",
            "meta": "Contingencias tributarias sobre los flujos de un esquema de captación masiva y consecuencias migratorias de los vinculados: obligaciones del Estatuto Tributario, intercambio de información y permanencia de extranjeros vinculados.",
            "paras": [
                "Todo esquema de captación deja un rastro tributario: retenciones, declaraciones, movimientos que la autoridad fiscal puede leer de forma independiente al proceso por captación masiva. Anticipar esas contingencias tributarias evita que una defensa se gane en el frente penal o administrativo y se pierda en el fiscal.",
                "Cuando hay vinculados extranjeros o estructuras fuera del país, la dimensión migratoria se vuelve real: visados, permanencia y salidas quedan condicionados por el proceso. Integrar el análisis migratorio desde el inicio impide sorpresas que ninguna de las otras prácticas vería venir.",
                "Los mecanismos de intercambio de información entre autoridades hacen que lo tributario y lo penal-administrativo se lean en conjunto. Por eso la estrategia fiscal y migratoria no puede ir por separado: debe ser coherente con la defensa que se construye en los demás frentes.",
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
            "slug": "corporativa-y-urbana",
            "rama": "Corporativa y urbana",
            "card": "Las controversias societarias sobre actos anteriores a la intervención y los activos inmobiliarios comprometidos.",
            "lede": "Trabaja la vida societaria de la captadora y los activos reales que suelen sostener el esquema: qué decisiones son atacables y qué pasa con los inmuebles comprometidos.",
            "meta": "Responsabilidad de administradores y validez de los actos societarios anteriores a la intervención, y suerte de los inmuebles comprometidos en un esquema de captación: Código de Comercio, registro y perímetro de bienes del Decreto 4334 de 2008.",
            "paras": [
                "La toma de posesión congela una sociedad que, hasta el día anterior, tomaba decisiones: aumentos de capital, cesiones, garantías, operaciones entre vinculadas. Revisar la validez de esos actos societarios anteriores a la intervención define la responsabilidad de administradores, revisores fiscales y terceros.",
                "Buena parte de los esquemas se apoya en inmuebles —comprados, prometidos o dados en garantía—. La dimensión urbana y registral determina qué activos inmobiliarios entran a la masa de la intervención, cuáles pueden liberarse y cómo se protege a quien contrató de buena fe.",
                "Leer la sociedad y sus bienes con criterio corporativo y registral define, en la práctica, el tamaño del problema: cuánto patrimonio responde, quién responde por él y qué activos pueden devolverse a los afectados.",
            ],
            "normas": [
                {"ley": "Código de Comercio", "que": "Validez de actos societarios y responsabilidad de administradores.", "url": _U["ccio"]},
                {"ley": "Decreto 4334 de 2008", "que": "Perímetro de bienes que entran a la intervención.", "url": _U["d4334"]},
                {"ley": "Régimen de registro de inmuebles", "que": "Oponibilidad y protección del tercero de buena fe.", "url": None},
            ],
            "faqs": [
                ("¿Responden los administradores por los actos de la sociedad captadora?",
                 '<p>Pueden responder. Se revisa la validez de las decisiones anteriores a la intervención —aumentos de capital, cesiones, garantías, operaciones entre vinculadas— y de allí se define la responsabilidad de administradores, revisores fiscales y terceros.</p>'),
                ("¿Qué pasa con los inmuebles del esquema?",
                 '<p>La dimensión registral determina qué activos inmobiliarios entran a la masa de la intervención, cuáles pueden liberarse y cómo se protege a quien contrató de buena fe.</p>'),
                ("¿Se pueden anular operaciones societarias previas a la toma de posesión?",
                 '<p>Según su validez. El Código de Comercio permite examinar esos actos; el resultado incide en el perímetro de bienes y en las responsabilidades que se atribuyen.</p>'),
            ],
            "serves": [("Me investigan o me vincularon", "/defensa-en-captacion-masiva/"),
                       ("Perdí dinero en un esquema", "/afectados-por-captacion-masiva/")],
            "articulo": ("captacion-con-libranzas-y-factoring", "Captación montada sobre contratos legales"),
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
            "slug": "laboral-y-de-seguros",
            "rama": "Laboral y de seguros",
            "card": "Las reclamaciones laborales de la sociedad intervenida y la exposición de las pólizas y garantías del recaudo.",
            "lede": "Resuelve dos frentes que suelen quedar huérfanos: las relaciones laborales de la sociedad intervenida y las pólizas o garantías vinculadas al recaudo.",
            "meta": "Acreencias laborales de la sociedad intervenida y exposición de pólizas y garantías del recaudo en un esquema de captación: prelación de créditos del Código Sustantivo del Trabajo y régimen de seguros.",
            "paras": [
                "La captadora tuvo empleados, comisionistas y estructuras de pago que la intervención interrumpe de golpe. Ordenar esas relaciones laborales —qué se debe, a quién y con qué prelación de créditos— evita contingencias que crecen en silencio mientras el resto del caso avanza.",
                "Muchos esquemas se aseguraron: pólizas de cumplimiento, de manejo, garantías de terceros. Leer esa exposición determina si hay una fuente adicional de recuperación para el afectado o un frente adicional de reclamación contra el vinculado.",
                "Ninguno de estos dos frentes suele estar en el radar de una defensa penal clásica, y sin embargo pueden mover cifras importantes: las acreencias laborales por su prelación, y las pólizas por su capacidad de responder cuando el patrimonio de la sociedad no alcanza.",
            ],
            "normas": [
                {"ley": "Código Sustantivo del Trabajo", "que": "Obligaciones laborales y prelación de créditos.", "url": _U["cst"]},
                {"ley": "Régimen de seguros", "que": "Pólizas de cumplimiento, de manejo y garantías del recaudo.", "url": None},
                {"ley": "Decreto 4334 de 2008", "que": "Concurrencia de acreencias con la masa de la intervención.", "url": _U["d4334"]},
            ],
            "faqs": [
                ("¿Qué pasa con los empleados de la sociedad intervenida?",
                 '<p>La intervención interrumpe las relaciones laborales; ordenar qué se debe, a quién y con qué prelación de créditos evita contingencias que crecen mientras avanza el resto del caso.</p>'),
                ("¿Las pólizas pueden ser una fuente de recuperación?",
                 '<p>Pueden serlo. Las pólizas de cumplimiento, de manejo y las garantías de terceros se revisan para ver si abren una fuente adicional de recuperación o un frente adicional de reclamación.</p>'),
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
  <span class="pr-go" aria-hidden="true">→</span>
</a>'''
    equipo_body = f'''
{section("""
  <p class="eyebrow">Áreas de práctica</p>
  <span class="prac-rule" aria-hidden="true"></span>
  <h1 class="prac-h1">Cinco prácticas al servicio de su defensa.</h1>
  <p class="prac-sub">Cada proceso por captación abre a la vez frentes administrativos, penales, civiles, societarios, tributarios y laborales. La firma los cubre con cinco prácticas que trabajan el mismo expediente.</p>
""", cls="hero")}

<section class="prac-rows-sec">
  <div class="prac-rows">{prac_rows}</div>
  <div class="container">
    <div class="cta-row" style="margin-top:clamp(40px,6vw,72px)">{agendar("Agendar una consulta")}<a class="btn btn--ghost" href="/firma/">Cómo trabajamos</a></div>
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
    for pr in PRACTICAS_DEV:
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
                          f'<div class="pr-tl-media"><div class="pr-tl-par">{media}</div></div></div>')
        art = ""
        if pr["articulo"]:
            aslug, atitle = pr["articulo"]
            art = f'<p class="pr-more"><a class="arrowlink" href="/analisis/{aslug}/">Análisis · {esc(atitle)}</a></p>'
        situ_cards_html = "".join(situ_card(t, u) for t, u in pr["serves"])
        practica_body = f'''
{crumbs([("Inicio", "/"), ("El equipo", "/equipo/"), (pr["rama"], None)])}
{section(f"""
  <p class="eyebrow">Una de las cinco prácticas</p>
  <span class="prac-rule" aria-hidden="true"></span>
  <h1 class="prac-h1">{esc(pr["rama"])}</h1>
  <p class="prac-sub">{esc(pr["lede"])}</p>
""", cls="hero", tight=True)}

{practica_nav(pr["slug"])}

<section class="section">
  <div class="container pr-two">
    <div class="pr-two-l">
      <p class="eyebrow-num"><span class="n">01</span>Qué resuelve</p>
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
    <p class="eyebrow-num"><span class="n">02</span>A qué situación sirve</p>
    <h2 class="pr-big">Desde dónde entra <span class="pr-accent">su caso.</span></h2>
    <div class="acards">{situ_cards_html}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="eyebrow-num"><span class="n">03</span>Normatividad asociada</p>
    <h2 class="pr-big">El marco que <span class="pr-accent">enmarca esta práctica.</span></h2>
  </div>
  <div class="pr-timeline">{norm_rows}</div>
</section>

<section class="section">
  <div class="container faq-two">
    <div class="faq-two-l">
      <p class="faq-pill"><span class="dot" aria-hidden="true"></span>Preguntas</p>
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
