#!/bin/bash
# Capturas automáticas para el análisis de la competencia (Veraly)
# Uso en Mac: abre Terminal, entra en tu carpeta y ejecuta:  bash capturas_automaticas.sh
# Requisito: Google Chrome instalado en /Applications. No instala nada.

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -x "$CHROME" ]; then echo "No encuentro Google Chrome en /Applications"; exit 1; fi

OUT="capturas_$(date +%Y-%m-%d)"
mkdir -p "$OUT"

shot () { # nombre url ancho alto espera_ms
  echo "→ $1"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --lang=es-CO \
    --window-size="${3:-1440},${4:-2200}" --virtual-time-budget="${5:-8000}" \
    --screenshot="$PWD/$OUT/$1.png" "$2" >/dev/null 2>&1
}

# PASO 2 · PageSpeed (tardan: 45 s cada una)
shot 10_EP_pagespeed_movil  "https://pagespeed.web.dev/analysis?url=https%3A%2F%2Festudiopenal.com%2F&form_factor=mobile"  1440 2200 45000
shot 10b_EP_pagespeed_escritorio "https://pagespeed.web.dev/analysis?url=https%3A%2F%2Festudiopenal.com%2F&form_factor=desktop" 1440 2200 45000
shot 11_AF_pagespeed_movil  "https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fwww.affirmalegal.com%2F&form_factor=mobile" 1440 2200 45000
shot 11b_AF_pagespeed_escritorio "https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fwww.affirmalegal.com%2F&form_factor=desktop" 1440 2200 45000
shot 12_CMS_pagespeed_movil "https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fcms.law%2Fes%2Fcol%2F&form_factor=mobile" 1440 2200 45000
shot 12b_CMS_pagespeed_escritorio "https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fcms.law%2Fes%2Fcol%2F&form_factor=desktop" 1440 2200 45000

# PASO 3 · Webs de la competencia
shot 14_EP_home "https://estudiopenal.com/"
shot 15_EP_precios "https://estudiopenal.com/cuanto-cobra-un-abogado-penalista-en-colombia-tarifas-reales-por-etapa-procesal-2026" 1440 4000
shot 16_EP_consulta "https://estudiopenal.com/programa-una-consulta"
shot 17_EP_guia_captacion "https://estudiopenal.com/captacion-masiva-y-habitual-de-dinero-delito-o-inversion-guia-legal-y-defensa-2026" 1440 4000
shot 18_EP_blog "https://estudiopenal.com/nuestro-blog"
shot 19_EP_contacto "https://estudiopenal.com/contactanos"
shot 20_EP_equipo "https://estudiopenal.com/abogados-penalistas-bogota"
shot 21_AF_home "https://www.affirmalegal.com/"
shot 22_AF_abogado_penalista "https://www.affirmalegal.com/abogado-penalista/"
shot 23_AF_pago_servicios "https://www.affirmalegal.com/pago-de-servicios/"
shot 24_AF_testimonios "https://www.affirmalegal.com/testimonios"
shot 25_AF_derecho_penal "https://www.affirmalegal.com/derecho-penal/"
shot 26_AF_blog "https://www.affirmalegal.com/blog/"
shot 27_CMS_home "https://cms.law/es/col/"
shot 28_CMS_penal_corporativo "https://cms.law/es/col/global-reach/americas/colombia/expertise/derecho-penal-corporativo"
shot 29_CMS_insight_hub "https://cms.law/es/col/insight-hub"
shot 30_SI_web "https://sinturaabogados.com/"
shot 31_SI_google "https://www.google.com/search?q=%22Sintura%22+abogados+asociados+Bogot%C3%A1&hl=es"
shot 32_SI_legal500 "https://www.legal500.com/c/colombia/compliance-and-white-collar-crime/"
shot 33_prensa_rocha_asuntoslegales "https://www.asuntoslegales.com.co/actualidad/victimas-de-piramide-ganadera-solicitaron-formalmente-que-se-investigue-a-felipe-rocha-3621706" 1440 3000
shot 34_prensa_rocha_espectador "https://www.elespectador.com/judicial/por-tercera-vez-cambian-al-fiscal-en-el-caso-de-felipe-rocha-y-piramide-ganadera/" 1440 3000
shot 35_prensa_simhon "https://www.asuntoslegales.com.co/consumidor/equipo-de-cms-rodriguez-azuero-lanzo-la-firma-boutique-simhon-vanegas-calle-4398811" 1440 3000
shot 36_prensa_affirma_larepublica "https://www.larepublica.co/especiales/desafios-legales-2024/asi-se-transforma-el-mercado-legal-en-colombia-3807776" 1440 3000

# PASO 4 · SEO técnico y responsive (390x844 = iPhone)
shot 37_EP_robots "https://estudiopenal.com/robots.txt" 1200 900
shot 37b_AF_robots "https://www.affirmalegal.com/robots.txt" 1200 900
shot 37c_CMS_robots "https://cms.law/robots.txt" 1200 900
shot 38_EP_sitemap "https://estudiopenal.com/sitemap.xml" 1200 1400
shot 38b_AF_sitemap "https://www.affirmalegal.com/sitemap.xml" 1200 1400
shot 38c_CMS_sitemap "https://cms.law/sitemap.xml" 1200 1400
shot 40_EP_movil "https://estudiopenal.com/" 390 844
shot 40b_AF_movil "https://www.affirmalegal.com/" 390 844
shot 40c_CMS_movil "https://cms.law/es/col/" 390 844

# PASO 5 · Fichas de Google Maps
shot 41_EP_maps "https://www.google.com/maps/search/Estudio+Penal+Carrera+13+90-17+Bogot%C3%A1?hl=es" 1440 1000 12000
shot 42_AF_maps "https://www.google.com/maps/search/Affirma+Legal+Bogot%C3%A1?hl=es" 1440 1000 12000
shot 43_CMS_maps "https://www.google.com/maps/search/CMS+Rodr%C3%ADguez-Azuero+Bogot%C3%A1?hl=es" 1440 1000 12000
shot 44_SI_maps "https://www.google.com/maps/search/Sintura+Abogados+Bogot%C3%A1?hl=es" 1440 1000 12000
shot 45_VE_maps "https://www.google.com/maps/search/Veraly+Grupo+Jur%C3%ADdico?hl=es" 1440 1000 12000

# PASO 7 · Bibliotecas de anuncios
shot 57_EP_meta_ads "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=CO&q=Estudio%20Penal&search_type=keyword_unordered" 1440 1600 12000
shot 57b_EP_google_ads "https://adstransparency.google.com/?region=CO&domain=estudiopenal.com" 1440 1400 12000
shot 58_AF_meta_ads "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=CO&q=Affirma%20Legal&search_type=keyword_unordered" 1440 1600 12000
shot 58b_AF_google_ads "https://adstransparency.google.com/?region=CO&domain=affirmalegal.com" 1440 1400 12000
shot 59_CMS_meta_ads "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=CO&q=CMS%20Rodr%C3%ADguez-Azuero&search_type=keyword_unordered" 1440 1600 12000
shot 59b_CMS_google_ads "https://adstransparency.google.com/?region=CO&domain=cms.law" 1440 1400 12000
shot 60_SI_meta_ads "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=CO&q=Sintura&search_type=keyword_unordered" 1440 1600 12000

echo ""
echo "Listo. Capturas en: $PWD/$OUT"
echo "Sube esa carpeta a tu Drive (Capturas competencia) y avisa a Claude."
open "$OUT"
