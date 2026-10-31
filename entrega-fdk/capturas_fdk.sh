#!/bin/bash
# Capturas automáticas de FDK EmpowerNet para el anexo de herramientas de la memoria.
# Uso en Mac:  bash capturas_fdk.sh   (requiere Google Chrome en /Applications; no instala nada)

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -x "$CHROME" ]; then echo "No encuentro Google Chrome en /Applications"; exit 1; fi
OUT="capturas_fdk_$(date +%Y-%m-%d)"; mkdir -p "$OUT"

shot () { # nombre url ancho alto espera_ms
  echo "→ $1"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --lang=es-ES \
    --window-size="${3:-1440},${4:-2200}" --virtual-time-budget="${5:-8000}" \
    --screenshot="$PWD/$OUT/$1.png" "$2" >/dev/null 2>&1
}

# PageSpeed Insights (tardan ~45 s cada una)
shot FDK_01_pagespeed_movil      "https://pagespeed.web.dev/analysis?url=https%3A%2F%2Ffdkempowernet.com%2F&form_factor=mobile"  1440 2400 50000
shot FDK_02_pagespeed_escritorio "https://pagespeed.web.dev/analysis?url=https%3A%2F%2Ffdkempowernet.com%2F&form_factor=desktop" 1440 2400 50000

# Web en producción
shot FDK_03_web_home        "https://fdkempowernet.com/" 1440 3200
shot FDK_04_web_home_movil  "https://fdkempowernet.com/" 390 844

# SEO técnico: evidencia del problema de indexación
shot FDK_05_sitemap         "https://fdkempowernet.com/sitemap.xml" 1200 1200
shot FDK_06_robots          "https://fdkempowernet.com/robots.txt"  1200 900
shot FDK_07_rich_results    "https://search.google.com/test/rich-results?url=https%3A%2F%2Ffdkempowernet.com%2F" 1440 1600 30000

echo ""; echo "Listo. Capturas en: $PWD/$OUT"; echo "Súbelas a la carpeta de Drive y avisa a Claude."
open "$OUT"
