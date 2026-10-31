#!/usr/bin/env python3
"""Builds a PDF by mixing original PDF pages (optionally relabelled) with new
HTML pages rendered in the Veraly visual system.

Usage: python3 build.py SPEC.md ORIGINAL.pdf OUTPUT.pdf "Footer doc title"
"""
import sys, os, re, io, html, subprocess, json
import markdown
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'node_modules/@fontsource')
pdfmetrics.registerFont(TTFont('Archivo', os.path.join(HERE, 'Archivo-400.ttf')))
pdfmetrics.registerFont(TTFont('Archivo-I', os.path.join(HERE, 'Archivo-400i.ttf')))
pdfmetrics.registerFont(TTFont('Archivo-SB', os.path.join(HERE, 'Archivo-600.ttf')))

W, H = 960, 540

def ff(fam, file, weight, style='normal'):
    return f"@font-face{{font-family:'{fam}';src:url('file://{FONTS}/{file}') format('woff2');font-weight:{weight};font-style:{style}}}"

CSS = "\n".join([
    ff('Archivo', 'archivo/files/archivo-latin-400-normal.woff2', 400),
    ff('Archivo', 'archivo/files/archivo-latin-400-italic.woff2', 400, 'italic'),
    ff('Archivo', 'archivo/files/archivo-latin-600-normal.woff2', 600),
    ff('Archivo', 'archivo/files/archivo-latin-700-normal.woff2', 700),
    ff('Playfair', 'playfair-display/files/playfair-display-latin-600-normal.woff2', 600),
    ff('Playfair', 'playfair-display/files/playfair-display-latin-700-normal.woff2', 700),
    ff('Playfair', 'playfair-display/files/playfair-display-latin-400-italic.woff2', 400, 'italic'),
]) + """
@page{size:960pt 540pt;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:'Archivo',sans-serif;color:#05292c;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:960pt;height:540pt;position:relative;overflow:hidden;page-break-after:always;background:#fff}
.label{position:absolute;left:50.4pt;top:33.5pt;font-size:7.8pt;font-weight:600;letter-spacing:.06em;color:#1d6f66;text-transform:uppercase}
.title{position:absolute;left:50.4pt;right:50pt;top:46pt;font-family:'Playfair';font-weight:600;font-size:25pt;line-height:1.15;color:#073a3f}
.subtitle{position:absolute;left:50.4pt;right:50pt;font-style:italic;font-size:9.6pt;color:#4e6a68;line-height:1.35}
.body{position:absolute;left:50.4pt;right:50pt;font-size:9.8pt;line-height:1.4}
.source{position:absolute;left:50.4pt;right:50pt;bottom:42pt;font-size:6.6pt;font-style:italic;color:#4e6a68;line-height:1.3}
.foot{position:absolute;left:50.4pt;right:50.4pt;bottom:22pt;font-size:7.2pt;color:#4e6a68;display:flex;justify-content:space-between}
.foot .num{margin-left:42pt}
.body p{margin:0 0 5pt}
.body h3{font-family:'Playfair';font-weight:600;font-size:12pt;color:#073a3f;margin:6pt 0 4pt}
.body h4{font-size:7.6pt;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#1d6f66;margin:5pt 0 3pt}
.body ul,.body ol{margin:0 0 5pt 13pt}
.body li{margin:0 0 2pt}
.body strong{font-weight:700;color:#073a3f}
.body table{width:100%;border-collapse:collapse;margin:2pt 0 6pt;font-size:.88em;line-height:1.3}
.body th{background:#073a3f;color:#fff;text-align:left;font-weight:600;padding:3.6pt 5pt;border:.5pt solid #073a3f;vertical-align:bottom}
.body td{padding:3.2pt 5pt;border:.5pt solid #c9d8d6;vertical-align:top}
.body tr:nth-child(even) td{background:#f2f9f8}
.body td strong{color:#05292c}
.body blockquote{background:#05292c;color:#d9f6ef;padding:8pt 12pt;border-radius:4pt;margin:4pt 0 6pt}
.body blockquote strong{color:#89f5e5}
.body blockquote p:last-child{margin:0}
.body code{font-family:'Archivo';background:#fff3b0;color:#7a4b00;padding:0 2pt;border-radius:2pt;font-size:.95em}
.cols{display:flex;gap:16pt}.cols>div{flex:1;min-width:0}
.cols3{display:flex;gap:12pt}.cols3>div{flex:1;min-width:0}
.card{border:.6pt solid #c9d8d6;border-radius:4pt;padding:7pt 9pt;background:#fff}
.card.dark{background:#05292c;color:#d9f6ef;border-color:#05292c}.card.dark strong{color:#89f5e5}
.card.mint{background:#f2f9f8}
.shot{border:.6pt solid #c9d8d6;border-radius:3pt;display:block;width:100%;object-fit:cover;object-position:top}
.cap{font-size:6.4pt;color:#4e6a68;font-style:italic;margin:2pt 0 4pt}
.kpi{display:flex;gap:10pt;margin:2pt 0 8pt}.kpi>div{flex:1;border-top:2pt solid #89f5e5;padding-top:4pt}
.kpi b{display:block;font-family:'Playfair';font-size:20pt;color:#073a3f;font-weight:700;line-height:1.1}
.kpi span{font-size:7pt;color:#4e6a68}
.tag{display:inline-block;background:#89f5e5;color:#05292c;font-weight:700;font-size:.8em;padding:0 4pt;border-radius:2pt}
.gb{display:block;height:8pt;background:#1d6f66;border-radius:1pt;margin:0 -2pt}
.pend{background:#fff3b0;color:#7a4b00;font-weight:700;padding:0 3pt;border-radius:2pt}
/* separators */
.sep{background:#05292c}
.sep .num{position:absolute;left:50pt;top:118pt;font-family:'Playfair';font-weight:700;font-size:84pt;color:#89f5e5;line-height:1}
.sep .stitle{position:absolute;left:50pt;top:238pt;font-family:'Playfair';font-weight:600;font-size:36pt;color:#d9f6ef}
.sep ul{position:absolute;left:50pt;top:325pt;list-style:none;color:#89f5e5;font-size:11pt;line-height:2.15}
.sep .brand{position:absolute;right:52pt;bottom:42pt;color:#9fb8b5;font-size:7.5pt;letter-spacing:.02em}
/* index */
.idx{width:100%;border-collapse:collapse}
.idx td{padding:5.2pt 6pt;border-bottom:.5pt solid #c9d8d6;vertical-align:top;font-size:8.6pt}
.idx td.n{font-family:'Playfair';font-weight:700;font-size:15pt;color:#1d6f66;width:38pt}
.idx td.t{font-weight:700;color:#073a3f;width:210pt}
.idx td.p{text-align:right;color:#1d6f66;font-weight:700;width:30pt}
"""

FIT_JS = """
() => {
  for (const pg of document.querySelectorAll('.page')) {
    const body = pg.querySelector('.body'); if (!body) continue;
    const limit = pg.getBoundingClientRect().bottom - (pg.querySelector('.source') ? 58 : 40) * 1.3333;
    let fs = parseFloat(getComputedStyle(body).fontSize);
    let guard = 0;
    while (body.getBoundingClientRect().bottom > limit && fs > 9 && guard < 80) {
      fs -= 0.25; body.style.fontSize = fs + 'px'; guard++;
    }
    if (body.getBoundingClientRect().bottom > limit) pg.setAttribute('data-overflow', '1');
  }
  return [...document.querySelectorAll('.page[data-overflow]')].map(p => p.id);
}
"""

def md(text):
    return markdown.markdown(text, extensions=['tables', 'md_in_html', 'sane_lists', 'attr_list'])

def parse_spec(path):
    raw = open(path, encoding='utf-8').read()
    blocks = re.split(r'^=== ', raw, flags=re.M)[1:]
    pages = []
    for b in blocks:
        head, _, rest = b.partition('\n')
        parts = [p.strip() for p in head.split('|')]
        kind = parts[0].split()
        opts = {}
        for p in parts[1:]:
            k, _, v = p.partition('=')
            opts[k.strip()] = v.strip()
        if kind[0] == 'orig':
            pages.append({'kind': 'orig', 'n': int(kind[1]), **opts})
        else:
            meta, sep, body = rest.partition('\n---\n')
            if not sep:
                meta, body = rest, ''
            m = {}
            for line in meta.strip().splitlines():
                if ':' in line:
                    k, _, v = line.partition(':')
                    m[k.strip()] = v.strip()
            pages.append({'kind': kind[0], **m, 'md': body})
    return pages

def render_new(pages, doctitle, out_pdf, imgroot):
    parts = []
    for i, p in enumerate(pages):
        num = p['_num']
        if p['kind'] == 'sep':
            items = ''.join(f'<li>{html.escape(x.strip())}</li>' for x in p.get('items', '').split('|') if x.strip())
            parts.append(f'<div class="page sep" id="p{num}"><div class="num">{p.get("num","")}</div>'
                         f'<div class="stitle">{p.get("title","")}</div><ul>{items}</ul>'
                         f'<div class="brand">VERALY GRUPO JURÍDICO · 2026</div></div>')
        elif p['kind'] == 'raw':
            parts.append(f'<div class="page" id="p{num}">{p["md"]}</div>')
        else:
            top = 92 if p.get('title') else 46
            # subtitle position depends on title lines (approx by length)
            tlines = 2 if len(p.get('title', '')) > 62 else 1
            subtop = 46 + 31 * tlines + 6
            sub = ''
            bodytop = subtop
            if p.get('subtitle'):
                sub = f'<div class="subtitle" style="top:{subtop}pt">{p["subtitle"]}</div>'
                slines = 2 if len(p['subtitle']) > 150 else 1
                bodytop = subtop + 14 * slines + 12
            else:
                bodytop = subtop + 4
            src = f'<div class="source">{p["source"]}</div>' if p.get('source') else ''
            body = md(p['md']).replace('■', '<span class="gb"></span>')
            body = body.replace('src="capturas/', f'src="file://{imgroot}/')
            foot = (f'<div class="foot"><span>{p.get("section","")}</span><span>Veraly Grupo Jurídico · {doctitle}'
                    f'<span class="num">{num:02d}</span></span></div>')
            parts.append(f'<div class="page" id="p{num}"><div class="label">{p.get("label","")}</div>'
                         f'<div class="title">{p.get("title","")}</div>{sub}'
                         f'<div class="body" style="top:{bodytop}pt">{body}</div>{src}{foot}</div>')
    doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(parts)}</body></html>'
    htmlpath = out_pdf.replace('.pdf', '.html')
    open(htmlpath, 'w', encoding='utf-8').write(doc)
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch(); const pg = await b.newPage({{viewport:{{width:1280,height:720}}}});
  await pg.goto('file://{htmlpath}'); await pg.evaluate(() => document.fonts.ready);
  await pg.waitForTimeout(400);
  const over = await pg.evaluate({FIT_JS});
  console.log(JSON.stringify(over));
  await pg.pdf({{path:'{out_pdf}', width:'13.3333in', height:'7.5in', printBackground:true, preferCSSPageSize:true}});
  await b.close();
}})();"""
    jsp = out_pdf.replace('.pdf', '.js')
    open(jsp, 'w').write(js)
    r = subprocess.run(['node', jsp], capture_output=True, text=True, cwd=HERE)
    if r.returncode:
        print(r.stderr); sys.exit(1)
    return json.loads(r.stdout.strip().splitlines()[-1] or '[]')

def overlay(num, label=None, section=None, cover=None, label_box=None, section_box=None):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(W, H))
    c.setFillColorRGB(1, 1, 1)
    if num is not None:
        c.rect(880, H - 521, 40, 15, fill=1, stroke=0)
        c.setFillColor('#4e6a68'); c.setFont('Archivo', 7.2)
        c.drawRightString(909.4, H - 516.4, f"{num:02d}")
    if label:
        c.setFillColorRGB(1, 1, 1); x1 = label_box or 420
        c.rect(48, H - 45, x1 - 46, 14, fill=1, stroke=0)
        c.setFillColor('#1d6f66'); c.setFont('Archivo-SB', 7.8)
        tobj = c.beginText(50.4, H - 41.6); tobj.setCharSpace(0.47); tobj.textLine(label.upper()); c.drawText(tobj)
    if section:
        c.setFillColorRGB(1, 1, 1); x1 = section_box or 300
        c.rect(48, H - 521, x1 - 46, 15, fill=1, stroke=0)
        c.setFillColor('#4e6a68'); c.setFont('Archivo', 7.2)
        c.drawString(50.4, H - 516.4, section)
    if cover:
        # list of (x0,y0top,x1,y1top,text,font,size,color,bg)
        for (x0, y0, x1, y1, text, font, size, color, bg) in cover:
            c.setFillColor(bg); c.rect(x0, H - y1, x1 - x0, y1 - y0, fill=1, stroke=0)
            if text:
                c.setFillColor(color); c.setFont(font, size); c.drawString(x0 + 1, H - y1 + 2.5, text)
    c.save(); buf.seek(0)
    return PdfReader(buf).pages[0]

def word_boxes(pdf, n):
    out = subprocess.run(['pdftotext', '-f', str(n), '-l', str(n), '-bbox', pdf, '-'], capture_output=True, text=True).stdout
    return [(float(a), float(b), float(c), float(d), html.unescape(w)) for a, b, c, d, w in
            re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<', out)]

def main(spec, orig, out, doctitle, imgroot):
    pages = parse_spec(spec)
    keys = {}
    for i, p in enumerate(pages):
        p['_num'] = i + 1
        if p.get('key'): keys[p['key']] = i + 1
    for p in pages:
        if 'md' in p:
            p['md'] = re.sub(r'\{\{(\w+)\}\}', lambda m: str(keys.get(m.group(1), '??')), p['md'])
    news = [p for p in pages if p['kind'] != 'orig']
    tmp = out.replace('.pdf', '_new.pdf')
    over = render_new(news, doctitle, tmp, imgroot) if news else []
    if over:
        print('OVERFLOW pages:', over)
    newr = PdfReader(tmp) if news else None
    origr = PdfReader(orig)
    w = PdfWriter()
    ni = 0
    for p in pages:
        if p['kind'] == 'orig':
            pg = origr.pages[p['n'] - 1]
            boxes = word_boxes(orig, p['n'])
            has_num = any(b[1] > 505 and b[0] > 880 for b in boxes)
            lab_box = max([b[2] for b in boxes if 30 < b[1] < 36 and b[3] < 45] or [0]) + 4
            sec_box = max([b[2] for b in boxes if b[1] > 505 and b[2] < 400] or [0]) + 4
            cover = None
            if p.get('cover'):
                cover = json.loads(p['cover'])
            ov = overlay(p['_num'] if has_num else None, p.get('label'), p.get('section'), cover,
                         lab_box if lab_box > 4 else None, sec_box if sec_box > 4 else None)
            pg.merge_page(ov)
            w.add_page(pg)
        else:
            w.add_page(newr.pages[ni]); ni += 1
    w.add_metadata({'/Title': f'Veraly Grupo Jurídico · {doctitle}', '/Author': '', '/Creator': '', '/Producer': ''})
    with open(out, 'wb') as f:
        w.write(f)
    print('pages', len(pages), '->', out)

if __name__ == '__main__':
    main(*sys.argv[1:6])
