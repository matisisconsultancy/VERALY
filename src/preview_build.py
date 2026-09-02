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
                        "mobilebar": bool(meta.get("mobile_bar")),
                        "bodyclass": meta.get("body_class", ""), "html": body}
    routes["/marca/sistema/"] = {"title": "Brandbook · Veraly", "active": "", "mobilebar": False,
        "html": '<section class="section"><div class="container prose"><p class="eyebrow">Brandbook</p><h1>El brandbook interactivo completo</h1><p>Pieza independiente de gran formato. En esta vista previa se muestra el resumen del sistema de marca; el brandbook completo se sirve en el sitio desplegado, en <code>/marca/sistema/</code>.</p><p><a class="arrowlink" href="#!/marca/">Volver al sistema de marca</a></p></div></section>'}
    templates = "\n".join(
        f'<template data-route="{p}" data-title="{build.esc(r["title"])}" data-active="{r["active"]}" data-mobilebar="{1 if r["mobilebar"] else 0}" data-bodyclass="{r.get("bodyclass","")}">{r["html"]}</template>'
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
  function frowPar(){var vh=window.innerHeight;[].slice.call(document.querySelectorAll('.fr-par')).forEach(function(par){var m=par.parentNode.getBoundingClientRect();var rel=((m.top+m.height/2)-vh/2)/vh;rel=Math.max(-1,Math.min(1,rel));var t=(1-rel)/2;var scale=(1+0.24*t).toFixed(3);par.style.transform='translate3d(0,'+(rel*-9).toFixed(2)+'%,0) scale('+scale+')';});
    if(!window.matchMedia||!window.matchMedia('(prefers-reduced-motion:reduce)').matches){[].slice.call(document.querySelectorAll('.pr-parallax')).forEach(function(el){var r=el.getBoundingClientRect();var rel=(r.top+r.height/2)-vh/2;el.style.transform='translateY('+(rel*-0.12).toFixed(1)+'px)';});}}
  function initFeatureRows(){var rows=[].slice.call(document.querySelectorAll('.frow')).concat([].slice.call(document.querySelectorAll('.prac-rows'))).concat([].slice.call(document.querySelectorAll('.pr-timeline'))).concat([].slice.call(document.querySelectorAll('.reveal-up'))).concat([].slice.call(document.querySelectorAll('.plz-sec')));rows.forEach(function(r){if(r.__f)return;r.__f=1;if(frowIO)frowIO.observe(r);else r.classList.add('in');});if(rows.length&&!window.__frowScroll){window.__frowScroll=1;window.addEventListener('scroll',frowPar,{passive:true});window.addEventListener('resize',frowPar);}frowPar();}
  var countIO=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){countIO.unobserve(e.target);if(e.target.__cuRun)e.target.__cuRun();}});},{threshold:0.6}):null;
  function initCountUp(){[].slice.call(document.querySelectorAll('[data-count]')).forEach(function(el){if(el.__cu)return;el.__cu=1;var target=parseFloat(el.getAttribute('data-count'))||0;el.__cuRun=function(){if(scrReduce){el.textContent=String(target);return;}var t0=0;function step(now){if(!t0)t0=now;var p=Math.min(1,(now-t0)/1200),eased=1-Math.pow(1-p,3);el.textContent=String(Math.round(eased*target));if(p<1)requestAnimationFrame(step);}requestAnimationFrame(step);};if(countIO)countIO.observe(el);else el.__cuRun();});}
  function initBlog(){var filters=[].slice.call(document.querySelectorAll('.bfilter')),grid=document.querySelector('[data-blog-grid]');if(filters.length&&grid){var cards=[].slice.call(grid.querySelectorAll('.bcard'));filters.forEach(function(btn){if(btn.__b)return;btn.__b=1;btn.addEventListener('click',function(){var t=btn.getAttribute('data-tema')||'';filters.forEach(function(f){f.classList.toggle('is-active',f===btn);});cards.forEach(function(c){c.hidden=!(t===''||c.getAttribute('data-tema')===t);});});});}[].slice.call(document.querySelectorAll('[data-share-copy]')).forEach(function(btn){if(btn.__b)return;btn.__b=1;btn.addEventListener('click',function(){var url=btn.getAttribute('data-share-copy');var done=function(){var prev=btn.textContent;btn.textContent='✓';btn.classList.add('is-copied');setTimeout(function(){btn.textContent=prev;btn.classList.remove('is-copied');},1600);};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(url).then(done,done);}else{done();}});});}
  function render(){var route=curRoute();var t=tpl[route]||tpl['/'];app.innerHTML='';app.appendChild(t.content.cloneNode(true));
    document.title=t.getAttribute('data-title');setActive(t.getAttribute('data-route'));
    var mb=t.getAttribute('data-mobilebar')==='1';mbar.classList.toggle('is-on',mb);body.classList.toggle('has-mobile-bar',mb);
    body.classList.toggle('theme-light',(t.getAttribute('data-bodyclass')||'').indexOf('theme-light')>=0);
    var mw=document.querySelector('.nav-menu-wrap');if(mw){mw.setAttribute('data-open','false');body.setAttribute('data-nav-open','false');}
    var tg=document.querySelector('.nav-toggle');if(tg){tg.setAttribute('aria-expanded','false');tg.innerHTML=ICON_MENU;}
    window.scrollTo(0,0);bindDynamic(app);initStepper();initReveal();initFeatureRows();initBlog();initScramble();initCountUp();initPlazos();initViaSticky();initPhases();}
  function initViaSticky(){var track=document.querySelector('.via-track');if(!track)return;var slides=[].slice.call(track.querySelectorAll('.via-slide')),bars=[].slice.call(track.querySelectorAll('.via-bars i')),n=slides.length;if(!n)return;function upd(){var h=track.offsetHeight-window.innerHeight;var p=h>0?(-track.getBoundingClientRect().top)/h:0;p=Math.max(0,Math.min(0.999,p));var idx=Math.floor(p*n);slides.forEach(function(s,i){s.classList.toggle('active',i===idx);});bars.forEach(function(b,i){b.classList.toggle('on',i<=idx);});}if(!window.__viaScroll){window.__viaScroll=1;window.addEventListener('scroll',upd,{passive:true});window.addEventListener('resize',upd);}upd();}
  function initPlazos(){var secs=[].slice.call(document.querySelectorAll('.plz-sec'));if(!secs.length)return;function upd(){var vh=window.innerHeight;secs.forEach(function(sec){var track=sec.querySelector('.plz-track');if(!track)return;var steps=[].slice.call(track.querySelectorAll('.plz-step'));var pin=sec.querySelector('.plz-pin-track');var p;if(pin&&getComputedStyle(sec.querySelector('.plz-pin-sticky')).position==='sticky'){var h=pin.offsetHeight-vh;p=h>0?(-pin.getBoundingClientRect().top)/h:0;}else{var r=sec.getBoundingClientRect();p=(vh*0.72-r.top)/Math.max(1,r.height*0.55);}p=Math.max(0,Math.min(1,p));track.style.setProperty('--p',p.toFixed(3));var active=Math.ceil(p*steps.length);steps.forEach(function(s,i){s.classList.toggle('is-on',i<active);});});}if(!window.__plzScroll){window.__plzScroll=1;window.addEventListener('scroll',upd,{passive:true});window.addEventListener('resize',upd);}upd();}
  function initPhases(){[].slice.call(document.querySelectorAll('.phase-tabs')).forEach(function(root){var tabs=[].slice.call(root.querySelectorAll('.ph-tab')),panels=[].slice.call(root.querySelectorAll('.ph-panel'));if(!tabs.length)return;tabs.forEach(function(tab){tab.addEventListener('click',function(){var k=tab.getAttribute('data-ph');tabs.forEach(function(t){t.classList.toggle('is-active',t===tab);});panels.forEach(function(p){p.classList.toggle('is-active',p.getAttribute('data-ph')===k);});});});});}
  var scrReduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var SCR_GLYPHS='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  function scrambleText(el){var node=null;for(var i=el.childNodes.length-1;i>=0;i--){var n=el.childNodes[i];if(n.nodeType===3&&n.nodeValue.replace(/\s/g,'')){node=n;break;}}var text=node?node.nodeValue:el.textContent;var set=node?function(v){node.nodeValue=v;}:function(v){el.textContent=v;};var start=0,dur=Math.min(1100,text.length*55+280);function frame(now){if(!start)start=now;var p=Math.min(1,(now-start)/dur);var reveal=p*text.length,out='';for(var i=0;i<text.length;i++){var c=text.charAt(i);if(c===' '||c==='/'||c==='·'||i<reveal-0.4){out+=c;}else{out+=SCR_GLYPHS.charAt((Math.random()*SCR_GLYPHS.length)|0);}}set(out);if(p<1)requestAnimationFrame(frame);else set(text);}requestAnimationFrame(frame);}
  var scrIO=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){scrIO.unobserve(e.target);scrambleText(e.target);}});},{threshold:0.6}):null;
  function initScramble(){[].slice.call(document.querySelectorAll('.eyebrow, .eyebrow-num, .faq-pill, .bfilter-pill, .article-kicker, .pr-tl-label')).forEach(function(el){if(el.__scr)return;el.__scr=1;if(scrIO)scrIO.observe(el);else scrambleText(el);});}
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
  (function(){var lastY=window.pageYOffset||0,ticking=false;
    function apply(){ticking=false;var y=window.pageYOffset||0;var navOpen=body.getAttribute('data-nav-open')==='true';
      if(y<=90||navOpen){header.classList.remove('nav-hidden');lastY=y;return;}
      var dy=y-lastY;if(dy>6)header.classList.add('nav-hidden');else if(dy<-6)header.classList.remove('nav-hidden');lastY=y;}
    window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(apply);}},{passive:true});})();
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
