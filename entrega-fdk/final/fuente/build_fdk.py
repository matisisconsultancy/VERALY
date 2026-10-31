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
pdfmetrics.registerFont(TTFont('Arimo-R', os.path.join(HERE, 'Arimo-400.ttf')))
pdfmetrics.registerFont(TTFont('Arimo-B', os.path.join(HERE, 'Arimo-700.ttf')))
pdfmetrics.registerFont(TTFont('Archivo-I', os.path.join(HERE, 'Archivo-400i.ttf')))
pdfmetrics.registerFont(TTFont('Archivo-SB', os.path.join(HERE, 'Archivo-600.ttf')))

W, H = 960, 540

def ff(fam, file, weight, style='normal'):
    return f"@font-face{{font-family:'{fam}';src:url('file://{FONTS}/{file}') format('woff2');font-weight:{weight};font-style:{style}}}"

CSS = "\n".join([
    ff('Arimo', 'arimo/files/arimo-latin-400-normal.woff2', 400),
    ff('Arimo', 'arimo/files/arimo-latin-400-italic.woff2', 400, 'italic'),
    ff('Arimo', 'arimo/files/arimo-latin-700-normal.woff2', 700),
    ff('Arimo', 'arimo/files/arimo-latin-700-normal.woff2', 600),
]) + """
@page{size:960pt 540pt;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:'Arimo',sans-serif;color:#0e0d51;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:960pt;height:540pt;position:relative;overflow:hidden;page-break-after:always;background:#f5f7fb}
.label{position:absolute;left:49pt;top:44pt;font-size:8.6pt;font-weight:700;letter-spacing:.03em;color:#009aaf;text-transform:uppercase}
.title{position:absolute;left:49pt;right:50pt;top:62pt;font-family:'Arimo';font-weight:700;font-size:21pt;line-height:1.15;color:#0e0d51}
.subtitle{position:absolute;left:50.4pt;right:50pt;font-size:9.6pt;color:#4a4a7a;line-height:1.35}
.body{position:absolute;left:49pt;right:49pt;font-size:11pt;line-height:1.38}
.source{position:absolute;left:50.4pt;right:50pt;bottom:42pt;font-size:6.6pt;font-style:italic;color:#5a5a85;line-height:1.3}
.foot{position:absolute;left:50.4pt;right:50.4pt;bottom:22pt;font-size:7.2pt;color:#5a5a85;display:flex;justify-content:space-between}
.foot .num{margin-left:42pt}
.body p{margin:0 0 5pt}
.body h3{font-family:'Arimo';font-weight:600;font-size:12pt;color:#0e0d51;margin:6pt 0 4pt}
.body h4{font-size:7.6pt;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#009aaf;margin:5pt 0 3pt}
.body ul,.body ol{margin:0 0 5pt 13pt}
.body li{margin:0 0 2pt}
.body strong{font-weight:700;color:#0e0d51}
.body table{width:100%;border-collapse:collapse;margin:2pt 0 6pt;font-size:.88em;line-height:1.3}
.body th{background:#0e0d51;color:#fff;text-align:left;font-weight:600;padding:3.6pt 5pt;border:.5pt solid #0e0d51;vertical-align:bottom}
.body td{background:#fff;padding:3.2pt 5pt;border:.5pt solid #dfe0eb;vertical-align:top}
.body tr:nth-child(even) td{background:#fafbfd}
.body td strong{color:#0e0d51}
.body blockquote{background:#0e0d51;color:#ffffff;padding:8pt 12pt;border-radius:4pt;margin:4pt 0 6pt}
.body blockquote strong{color:#2fd483}
.body blockquote p:last-child{margin:0}
.body code{font-family:'Archivo';background:#fff3b0;color:#7a4b00;padding:0 2pt;border-radius:2pt;font-size:.95em}
.cols{display:flex;gap:16pt}.cols>div{flex:1;min-width:0}
.cols3{display:flex;gap:12pt}.cols3>div{flex:1;min-width:0}
.card{border:.6pt solid #dfe0eb;border-radius:4pt;padding:7pt 9pt;background:#fff}
.card.dark{background:#0e0d51;color:#ffffff;border-color:#0e0d51}.card.dark strong{color:#2fd483}
.card.mint{background:#fafbfd}
.shot{border:.6pt solid #dfe0eb;border-radius:3pt;display:block;width:100%;object-fit:cover;object-position:top}
.cap{font-size:6.4pt;color:#5a5a85;font-style:italic;margin:2pt 0 4pt}
.kpi{display:flex;gap:10pt;margin:2pt 0 8pt}.kpi>div{flex:1;border-top:2pt solid #2fd483;padding-top:4pt}
.kpi b{display:block;font-family:'Arimo';font-size:20pt;color:#0e0d51;font-weight:700;line-height:1.1}
.kpi span{font-size:7pt;color:#5a5a85}
.tag{display:inline-block;background:#2fd483;color:#0e0d51;font-weight:700;font-size:.8em;padding:0 4pt;border-radius:2pt}
.gb{display:block;height:8pt;background:#009aaf;border-radius:1pt;margin:0 -2pt}
.pend{background:#fff3b0;color:#7a4b00;font-weight:700;padding:0 3pt;border-radius:2pt}
/* separators */
.sep{background:#0e0d51}
.sep .num{position:absolute;left:50pt;top:118pt;font-family:'Arimo';font-weight:700;font-size:84pt;color:#2fd483;line-height:1}
.sep .stitle{position:absolute;left:50pt;top:238pt;font-family:'Arimo';font-weight:600;font-size:36pt;color:#ffffff}
.sep ul{position:absolute;left:50pt;top:325pt;list-style:none;color:#2fd483;font-size:11pt;line-height:2.15}
.sep .brand{position:absolute;right:52pt;bottom:42pt;color:#9a9ac4;font-size:7.5pt;letter-spacing:.02em}
/* index */
.idx{width:100%;border-collapse:collapse}
.idx td{padding:5.2pt 6pt;border-bottom:.5pt solid #dfe0eb;vertical-align:top;font-size:8.6pt}
.idx td.n{font-family:'Arimo';font-weight:700;font-size:15pt;color:#009aaf;width:38pt}
.idx td.t{font-weight:700;color:#0e0d51;width:210pt}
.idx td.p{text-align:right;color:#009aaf;font-weight:700;width:30pt}
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
                         f'<div class="brand">fdkEmpowerNet · 2026</div></div>')
        elif p['kind'] == 'raw':
            parts.append(f'<div class="page" id="p{num}" style="background:{p.get("bg","#f5f7fb")}">{p["md"]}</div>')
        else:
            top = 92
            # subtitle position depends on title lines (approx by length)
            tlines = 2 if len(p.get("title", "")) > 80 else 1
            subtop = 62 + 26 * tlines + 6
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
            foot = ''
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
        c.setFillColor('#009aaf'); c.setFont('Archivo-SB', 7.8)
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
            if p.get('cover'):
                pw, ph = float(pg.mediabox.width), float(pg.mediabox.height)
                buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(pw, ph))
                for (x0, y0, x1, y1, text, font, size, color, bg) in json.loads(p['cover']):
                    c.setFillColor(bg); c.rect(x0, ph - y1, x1 - x0, y1 - y0, fill=1, stroke=0)
                    if text:
                        c.setFillColor(color); c.setFont(font, size); c.drawString(x0 + 2.5, ph - y1 + 5.5, text)
                c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0])
            w.add_page(pg)
        else:
            np_ = newr.pages[ni]; np_.scale_by(1.5); w.add_page(np_); ni += 1
    w.add_metadata({'/Title': f'FDK EmpowerNet · {doctitle}', '/Author': '', '/Creator': '', '/Producer': ''})
    with open(out, 'wb') as f:
        w.write(f)
    print('pages', len(pages), '->', out)

if __name__ == '__main__':
    main(*sys.argv[1:6])
