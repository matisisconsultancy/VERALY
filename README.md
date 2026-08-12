# Veraly Grupo Jurídico — Sitio web

Sitio institucional de Veraly Grupo Jurídico, despacho boutique especializado en
captación masiva y habitual (fraude financiero). Implementa la especificación
funcional v1.0 (Workstream 2, bloques #1 y #3).

## Arquitectura

Sitio **estático** (HTML/CSS/JS sin dependencias) servido por GitHub Pages. Las
páginas se generan con un script Python a partir de plantillas y datos, y el HTML
final se commitea en rutas limpias (`carpeta/index.html`).

Arquitectura de dos capas:

- **Capa 1 · institucional:** `/`, `/firma`, `/equipo` (+ ficha por socio),
  `/marca`, `/contacto`.
- **Capa 2 · intención:** `/afectados-por-captacion-masiva`,
  `/defensa-en-captacion-masiva`, `/cumplimiento-en-recaudo-masivo`,
  `/analisis` (+ artículos).
- **Legales:** `/aviso-de-privacidad`, `/aviso-legal`.

El brandbook interactivo (Workstream 1) vive en `/marca/sistema/`.

## Estructura

```
index.html, <ruta>/index.html   Páginas generadas (NO editar a mano)
assets/css/  assets/js/  assets/fonts/   Sistema de diseño y fuentes autoalojadas
src/build.py                    Generador: configuración, plantillas, sitemap, robots
src/build_pages*.py             Contenido (copy final) de cada página
sitemap.xml, robots.txt         Generados por el build
```

## Regenerar el sitio

```bash
python3 src/build.py
```

## Diseño

Identidad "Convergencia": tema teal (`#05292C`) con acento menta (`#89F5E5`),
tipografías Playfair Display (títulos), Archivo (texto) y Jost (UI). Derivado del
brandbook. Objetivos: WCAG 2.1 AA, JS mínimo, HTML semántico citable por IA.

## Pendientes que condicionan la publicación

Marcados en el código con `TODO` / notas. Ver §17 de la especificación:

- **03** Formación, títulos y cargos de los cinco socios (bloquea `/equipo`).
- **05** Dominio canónico (`veraly.co` vs. dominio de Semrush) — bloquea despliegue.
- **06** Aprobación de aviso de privacidad y aviso legal.
- **07** Dirección física, teléfono y correo definitivos (footer/contacto).
- Config del formulario (endpoint), GA4 (`GA_ID`) y WhatsApp en `assets/js/main.js`.
- Guía de plazos (PDF, Perfil A) y cuestionario de encuadre (PDF, Perfil C).
