#!/usr/bin/env python3
"""Genera una copia lista para GitHub Pages en docs/ con las rutas
raíz-absolutas reescritas al subpath del proyecto (p. ej. /VERALY/).

Uso:  python3 src/deploy_pages.py [BASE]
BASE por defecto: /VERALY  (nombre del repositorio en la URL de Pages)
"""
import os, re, sys, shutil, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
BASE = (sys.argv[1] if len(sys.argv) > 1 else "/VERALY").rstrip("/")

def _asset_version():
    """Hash corto del contenido de los assets versionables (css/js). Cambia
    solo cuando cambian los archivos, de modo que el navegador y el CDN de
    GitHub Pages descargan la versión nueva en cada despliegue real."""
    h = hashlib.sha1()
    files = [
        "assets/css/fonts.css", "assets/css/styles.css",
        "assets/js/main.js", "assets/js/legal-motion.js",
        "assets/js/legal-icons.js", "assets/js/hero-video.js",
    ]
    for rel in files:
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            h.update(rel.encode("utf-8"))
            h.update(open(p, "rb").read())
    return h.hexdigest()[:10]

VER = _asset_version()

# Carpetas/archivos de la salida estática que se copian a docs/
PAGE_DIRS = [
    "afectados-por-captacion-masiva", "analisis", "aviso-de-privacidad",
    "aviso-legal", "contacto", "cumplimiento-en-recaudo-masivo",
    "defensa-en-captacion-masiva", "equipo", "firma", "marca",
    "politica-de-cookies", "preguntas-frecuentes",
]
TOP_FILES = ["index.html", "404.html", "robots.txt", "sitemap.xml",
             "favicon.ico", "favicon.svg", "site.webmanifest"]
ASSET_DIR = "assets"

# Primeros segmentos de ruta interna válidos (para reescribir strings en JS)
KNOWN = PAGE_DIRS + [ASSET_DIR]

def clean_out():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

def copy_all():
    for f in TOP_FILES:
        src = os.path.join(ROOT, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(OUT, f))
    for d in PAGE_DIRS + [ASSET_DIR]:
        src = os.path.join(ROOT, d)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(OUT, d))

def rewrite_html(text):
    # href/src/poster="/..." (comillas dobles o simples), sin tocar "//"
    text = re.sub(r'(\b(?:href|src|poster)=")/(?!/)', r'\1' + BASE + '/', text)
    text = re.sub(r"(\b(?:href|src|poster)=')/(?!/)", r'\1' + BASE + '/', text)
    # Cache-busting: añade ?v=<hash> a los assets css/js para forzar que el
    # navegador y el CDN descarguen la versión nueva en cada despliegue real.
    text = re.sub(
        r'((?:href|src)=["\'][^"\']+/assets/(?:css|js)/[^"\']+?\.(?:css|js))(["\'])',
        r'\1?v=' + VER + r'\2', text)
    return text

def rewrite_css(text):
    return re.sub(r'url\(\s*/(?!/)', 'url(' + BASE + '/', text)

def rewrite_js(text):
    # Reescribe literales de ruta '/<seg>...' y "/<seg>..." para segmentos conocidos
    for seg in KNOWN:
        text = text.replace("'/" + seg, "'" + BASE + "/" + seg)
        text = text.replace('"/' + seg, '"' + BASE + "/" + seg)
    return text

def rewrite_manifest(text):
    # Prefija las rutas raíz-absolutas del manifest ("/..." -> "/BASE/...")
    return re.sub(r'"/(?!/)', '"' + BASE + '/', text)

def process():
    for dirpath, _dirs, files in os.walk(OUT):
        for name in files:
            p = os.path.join(dirpath, name)
            if name.endswith(".html"):
                t = open(p, encoding="utf-8").read()
                open(p, "w", encoding="utf-8").write(rewrite_html(t))
            elif name.endswith(".webmanifest"):
                t = open(p, encoding="utf-8").read()
                open(p, "w", encoding="utf-8").write(rewrite_manifest(t))
            elif name.endswith(".css"):
                t = open(p, encoding="utf-8").read()
                open(p, "w", encoding="utf-8").write(rewrite_css(t))
            elif name.endswith(".js"):
                t = open(p, encoding="utf-8").read()
                open(p, "w", encoding="utf-8").write(rewrite_js(t))

def extras():
    # Jekyll off (por si hay nombres con guion bajo) y 404 amable
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    idx = os.path.join(OUT, "index.html")
    if os.path.exists(idx):
        shutil.copy2(idx, os.path.join(OUT, "404.html"))

if __name__ == "__main__":
    clean_out()
    copy_all()
    process()
    extras()
    n = sum(len(f) for _r, _d, f in os.walk(OUT))
    print(f"docs/ generado con BASE={BASE} · {n} archivos")
