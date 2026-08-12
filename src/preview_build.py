# -*- coding: utf-8 -*-
"""Empaqueta el sitio multipágina en un único HTML navegable (vista previa/Artifact).
Router por hash (#!/ruta), fuentes y CSS embebidos, asistente y agendamiento incluidos.
Uso: python3 src/preview_build.py <salida.html>
"""
import base64, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import build, build_pages


def datauri(p):
    return "data:font/woff2;base64," + base64.b64encode(open(os.path.join(ROOT, p), "rb").read()).decode()


def run(out_path):
    build.PAGES.clear()
    build_pages.build(vars(build))
    PAGES = build.PAGES
    fonts_css = f"""
@font-face{{font-family:'Archivo';font-style:normal;font-weight:100 900;font-display:swap;src:url({datauri('assets/fonts/archivo-var.woff2')}) format('woff2')}}
@font-face{{font-family:'Jost';font-style:normal;font-weight:100 900;font-display:swap;src:url({datauri('assets/fonts/jost-var.woff2')}) format('woff2')}}
@font-face{{font-family:'Playfair Display';font-style:normal;font-weight:700;font-display:swap;src:url({datauri('assets/fonts/playfair-700.woff2')}) format('woff2')}}
"""
    styles_css = open(os.path.join(ROOT, "assets/css/styles.css"), encoding="utf-8").read()
    header = build.header_html(""); footer = build.footer_html()
    mobilebar = build.mobile_bar_html(); assistant = build.assistant_html()
    routes = {}
    for path, meta, body in PAGES:
        routes[path] = {"title": meta["title"], "active": meta.get("active", ""),
                        "mobilebar": bool(meta.get("mobile_bar")), "html": body}
    routes["/marca/sistema/"] = {"title": "Brandbook · Veraly", "active": "", "mobilebar": False,
        "html": '<section class="section"><div class="container prose"><p class="eyebrow">Brandbook</p><h1>El brandbook interactivo completo</h1><p>Pieza independiente de gran formato. En esta vista previa se muestra el resumen del sistema de marca; el brandbook completo se sirve en el sitio desplegado, en <code>/marca/sistema/</code>.</p><p><a class="arrowlink" href="#!/marca/">Volver al sistema de marca</a></p></div></section>'}
    templates = "\n".join(
        f'<template data-route="{p}" data-title="{build.esc(r["title"])}" data-active="{r["active"]}" data-mobilebar="{1 if r["mobilebar"] else 0}">{r["html"]}</template>'
        for p, r in routes.items())

    def rw(h):
        return re.sub(r'href="/(?![/])', 'href="#!/', h).replace('href="/"', 'href="#!/"')
    header, footer, mobilebar, templates, assistant = map(rw, (header, footer, mobilebar, templates, assistant))

    JS = r"""
(function(){
  var app=document.getElementById('app'),header=document.querySelector('.site-header'),
      mbar=document.getElementById('mobilebar'),body=document.body;
  document.documentElement.classList.add('js');
  var tpl={};document.querySelectorAll('template[data-route]').forEach(function(t){tpl[t.getAttribute('data-route')]=t;});
  function curRoute(){var h=location.hash;if(h.indexOf('#!')===0){var r=h.slice(2)||'/';if(!r.startsWith('/'))r='/'+r;if(!r.endsWith('/'))r+='/';return r;}return '/';}
  function toast(m){var t=document.createElement('div');t.className='toast';t.textContent=m;document.body.appendChild(t);requestAnimationFrame(function(){t.setAttribute('data-show','true');});setTimeout(function(){t.removeAttribute('data-show');setTimeout(function(){t.remove();},300);},3600);}
  function go(route){location.hash='#!'+route;}
  function openScheduler(){toast('Agendamiento en línea: se activa al conectar el calendario de la firma (Cal.com). En esta vista previa le llevamos al contacto.');go('/contacto/');}
  function bindDynamic(scope){
    scope.querySelectorAll('[data-maxcount]').forEach(function(inp){var max=+inp.getAttribute('data-maxcount');var out=inp.closest('.field').querySelector('.char-count');function u(){if(out)out.textContent=inp.value.length+' / '+max;}inp.addEventListener('input',u);u();});
    scope.querySelectorAll('form[data-veraly-form]').forEach(function(form){form.addEventListener('submit',function(e){e.preventDefault();var ok=true,bad=null;
      form.querySelectorAll('.field').forEach(function(f){var i=f.querySelector('input');if(!i)return;var v=i.value.trim();var b=false;if(i.hasAttribute('required')&&!v)b=true;if(i.dataset.validate==='contact'&&v){var em=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v),ph=/^[+\d][\d\s().-]{6,}$/.test(v);if(!em&&!ph)b=true;}f.setAttribute('data-invalid',b);if(b){ok=false;bad=bad||i;}});
      var ck=form.querySelector('.check input');if(ck&&!ck.checked){ok=false;bad=bad||ck;}var st=form.querySelector('.form-status');
      if(!ok){if(bad)bad.focus();return;}if(st){st.className='form-status ok';st.setAttribute('data-show','true');st.textContent='Recibimos su mensaje. Le respondemos dentro de las próximas 24 horas hábiles. (Vista previa: el envío real se conecta en el sitio desplegado.)';}
      form.reset();form.querySelectorAll('.char-count').forEach(function(c){c.textContent='0 / 200';});});});
  }
  function setActive(route){header.querySelectorAll('[aria-current]').forEach(function(a){a.removeAttribute('aria-current');});header.querySelectorAll('a[href^="#!"]').forEach(function(a){if(a.getAttribute('href')==='#!'+route)a.setAttribute('aria-current','page');});}
  var ICON_MENU='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>';
  var ICON_CLOSE='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  function pinProgress(track){var r=track.getBoundingClientRect();var total=track.offsetHeight-window.innerHeight;return total>0?Math.min(1,Math.max(0,(-r.top)/total)):0;}
  function initStepper(){var track=document.querySelector('.stepper-track');if(!track||track.__i)return;track.__i=1;
    var steps=[].slice.call(track.querySelectorAll('.step')),rail=[].slice.call(track.querySelectorAll('.stepper-rail li')),n=steps.length;if(!n)return;
    function upd(){if(window.innerWidth<=900){steps.forEach(function(s){s.classList.add('active');});return;}
      var idx=Math.min(n-1,Math.floor(pinProgress(track)*n));steps.forEach(function(s,i){s.classList.toggle('active',i===idx);});rail.forEach(function(li,i){li.classList.toggle('on',i===idx);});}
    window.addEventListener('scroll',upd,{passive:true});window.addEventListener('resize',upd);upd();}
  function initReveal(){var track=document.querySelector('.reveal-track');if(!track||track.__i)return;track.__i=1;
    var phrases=[].slice.call(track.querySelectorAll('.reveal-phrase')),cards=[].slice.call(track.querySelectorAll('.reveal-cards .rc')),np=phrases.length;if(!np)return;
    var words=phrases.map(function(p){return [].slice.call(p.querySelectorAll('.w'));});
    function upd(){if(window.innerWidth<=900){phrases.forEach(function(p){p.classList.add('active');});words.forEach(function(ws){ws.forEach(function(w){w.classList.add('lit');});});cards.forEach(function(c){c.classList.add('in');});return;}
      var p=pinProgress(track),idx=Math.min(np-1,Math.floor(p*np)),local=(p*np)-idx;
      phrases.forEach(function(ph,i){ph.classList.toggle('active',i===idx);});
      var lit=Math.min(1,local/0.55);
      words[idx].forEach(function(w,j){w.classList.toggle('lit',(j+0.6)/words[idx].length<=lit);});
      cards.forEach(function(c,k){c.classList.toggle('in',p>=(k+1)/(cards.length+1));});}
    window.addEventListener('scroll',upd,{passive:true});window.addEventListener('resize',upd);upd();}
  var frowIO=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');frowIO.unobserve(e.target);}});},{threshold:0.2,rootMargin:'0px 0px -8% 0px'}):null;
  function frowPar(){var vh=window.innerHeight;[].slice.call(document.querySelectorAll('.fr-par')).forEach(function(par){var m=par.parentNode.getBoundingClientRect();var rel=((m.top+m.height/2)-vh/2)/vh;rel=Math.max(-1,Math.min(1,rel));var t=(1-rel)/2;var scale=(1+0.24*t).toFixed(3);par.style.transform='translate3d(0,'+(rel*-9).toFixed(2)+'%,0) scale('+scale+')';});}
  function initFeatureRows(){var rows=[].slice.call(document.querySelectorAll('.frow'));rows.forEach(function(r){if(r.__f)return;r.__f=1;if(frowIO)frowIO.observe(r);else r.classList.add('in');});if(rows.length&&!window.__frowScroll){window.__frowScroll=1;window.addEventListener('scroll',frowPar,{passive:true});window.addEventListener('resize',frowPar);}frowPar();}
  function render(){var route=curRoute();var t=tpl[route]||tpl['/'];app.innerHTML='';app.appendChild(t.content.cloneNode(true));
    document.title=t.getAttribute('data-title');setActive(t.getAttribute('data-route'));
    var mb=t.getAttribute('data-mobilebar')==='1';mbar.classList.toggle('is-on',mb);body.classList.toggle('has-mobile-bar',mb);
    var mw=document.querySelector('.nav-menu-wrap');if(mw){mw.setAttribute('data-open','false');body.setAttribute('data-nav-open','false');}
    var tg=document.querySelector('.nav-toggle');if(tg){tg.setAttribute('aria-expanded','false');tg.innerHTML=ICON_MENU;}
    window.scrollTo(0,0);bindDynamic(app);initStepper();initReveal();initFeatureRows();}
  document.addEventListener('click',function(e){var el=e.target.closest('[data-cal]');if(el){e.preventDefault();openScheduler();}});
  var tg=document.querySelector('.nav-toggle'),mw=document.querySelector('.nav-menu-wrap');
  if(tg&&mw){tg.addEventListener('click',function(){var o=mw.getAttribute('data-open')==='true';mw.setAttribute('data-open',String(!o));tg.setAttribute('aria-expanded',String(!o));tg.innerHTML=o?ICON_MENU:ICON_CLOSE;body.setAttribute('data-nav-open',String(!o));});}
  document.querySelectorAll('.has-sub').forEach(function(item){var b=item.querySelector('button');if(!b)return;b.setAttribute('aria-expanded','false');function so(v){item.setAttribute('data-open',String(v));b.setAttribute('aria-expanded',String(v));}b.addEventListener('click',function(e){e.stopPropagation();so(item.getAttribute('data-open')!=='true');});item.addEventListener('mouseenter',function(){if(innerWidth>900)so(true);});item.addEventListener('mouseleave',function(){if(innerWidth>900)so(false);});document.addEventListener('click',function(e){if(!item.contains(e.target))so(false);});});
  var FLOW={
   start:{q:'¿Con qué le podemos ayudar?',options:[{label:'Perdí dinero en una captación',to:'A'},{label:'Me investigan o me vincularon',to:'B'},{label:'Mi empresa recauda de muchas personas',to:'C'},{label:'Quiero entender el tema',to:'INFO'}]},
   A:{q:'¿Ya hubo toma de posesión o intervención?',options:[{label:'Sí, ya hay intervención',to:'A1'},{label:'No, o no lo sé',to:'A2'}]},
   A1:{text:'Dentro de la intervención los plazos son cortos: las solicitudes de devolución se presentan en 10 días comunes desde el aviso del interventor. Conviene actuar pronto.',page:['Ver la ruta del afectado','#!/afectados-por-captacion-masiva/'],cta:'agendar'},
   A2:{text:'Existen tres vías —administrativa, penal y civil— y la calificación correcta cambia la estrategia y lo que se recupera por cada una.',page:['Ver la ruta del afectado','#!/afectados-por-captacion-masiva/'],cta:'agendar'},
   B:{q:'¿En qué momento está?',options:[{label:'Requerimientos o visita administrativa',to:'B1'},{label:'Ya hay captura o imputación',to:'B2'},{label:'Soy revisor fiscal, contador o proveedor',to:'B3'}]},
   B1:{text:'Es la fase administrativa previa: todavía se puede sustentar el modelo y, en su caso, evitar la declaratoria y la suspensión.',page:['Ver la ruta de la defensa','#!/defensa-en-captacion-masiva/'],cta:'urgente'},
   B2:{text:'El momento procesal define lo que aún es posible. La defensa se juega desde los actos urgentes y la audiencia de imputación.',page:['Ver la ruta de la defensa','#!/defensa-en-captacion-masiva/'],cta:'urgente'},
   B3:{text:'La vinculación alcanza esas posiciones por el ejercicio del cargo, pero es desvirtuable: la exclusión se construye sobre la buena fe exenta de culpa y el origen lícito.',page:['Ver la ruta de la defensa','#!/defensa-en-captacion-masiva/'],cta:'urgente'},
   C:{q:'¿Qué tipo de modelo?',options:[{label:'Fintech o crowdfunding',to:'C1'},{label:'Libranzas, factoring o multinivel',to:'C1'},{label:'Otro modelo de recaudo',to:'C1'}]},
   C1:{text:'La clave es doble: los umbrales del Decreto 1981 de 1988 y la explicación financiera razonable del rendimiento. Ambas se revisan antes de que las revise una superintendencia.',page:['Ver la ruta preventiva','#!/cumplimiento-en-recaudo-masivo/'],cta:'agendar'},
   INFO:{text:'Publicamos sobre las figuras del fraude financiero: cómo se estructuran, cómo se investigan y qué vías abren. Nunca sobre casos identificables.',page:['Ir a Análisis','#!/analisis/'],cta:'none'}
  };
  var asst=document.getElementById('asst'),aL=document.getElementById('asst-launch'),aP=document.getElementById('asst-panel'),aC=document.getElementById('asst-close'),aB=document.getElementById('asst-body');
  function aRender(k){var n=FLOW[k];if(!n)return;aB.innerHTML='';
    if(n.q){var h=document.createElement('p');h.className='asst-q';h.textContent=n.q;aB.appendChild(h);
      n.options.forEach(function(o){var b=document.createElement('button');b.className='asst-opt';b.textContent=o.label;b.addEventListener('click',function(){aRender(o.to);});aB.appendChild(b);});}
    else{var p=document.createElement('p');p.className='asst-text';p.textContent=n.text;aB.appendChild(p);
      var acts=document.createElement('div');acts.className='asst-actions';
      if(n.cta==='agendar'){var a=document.createElement('a');a.className='btn btn--primary btn--sm';a.href='#';a.textContent='Agendar una consulta';a.addEventListener('click',function(e){e.preventDefault();openScheduler();});acts.appendChild(a);}
      else if(n.cta==='urgente'){var a2=document.createElement('a');a2.className='btn btn--primary btn--sm';a2.href='#!/contacto/';a2.textContent='Escribir ahora';acts.appendChild(a2);}
      if(n.page){var pl=document.createElement('a');pl.className='asst-link';pl.href=n.page[1];pl.textContent=n.page[0]+' →';acts.appendChild(pl);}
      aB.appendChild(acts);
      var bk=document.createElement('button');bk.className='asst-back';bk.textContent='← Empezar de nuevo';bk.addEventListener('click',function(){aRender('start');});aB.appendChild(bk);}}
  function aToggle(o){if(!aP)return;aP.hidden=!o;aL.setAttribute('aria-expanded',String(o));asst.setAttribute('data-open',String(o));if(o&&!aB.hasChildNodes())aRender('start');}
  if(aL){aL.addEventListener('click',function(){aToggle(aP.hidden);});aC.addEventListener('click',function(){aToggle(false);});document.addEventListener('keyup',function(e){if(e.key==='Escape'&&!aP.hidden)aToggle(false);});}
  if(aB){aB.addEventListener('click',function(e){if(e.target.closest('a[href^="#!"]'))aToggle(false);});}
  window.addEventListener('hashchange',function(){if(location.hash.indexOf('#!')===0)render();});
  render();
})();
"""
    mobilebar_global = mobilebar.replace('class="mobile-bar is-on"', 'class="mobile-bar" id="mobilebar"')
    page = f"""<title>Veraly Grupo Jurídico</title>
<style>
{fonts_css}
{styles_css}
.preview-flag{{position:fixed;bottom:12px;left:12px;z-index:60;background:var(--panel-2);border:1px solid var(--line);color:var(--dim);font-family:var(--ui);font-size:12px;padding:6px 12px;border-radius:6px}}
</style>
{header}
<main id="app"></main>
{footer}
{mobilebar_global}
{assistant}
{templates}
<div class="preview-flag">Vista previa navegable · Veraly</div>
<script>{JS}</script>
"""
    open(out_path, "w", encoding="utf-8").write(page)
    print("preview:", out_path, "bytes:", len(page), "routes:", len(routes))


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "veraly-preview.html"))
