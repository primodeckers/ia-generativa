#!/usr/bin/env python3
"""Injeta um painel de passo a passo (texto + destaque no diagrama) em um workflow avulso do Archify.

Uso: add_passo_a_passo.py ENTRADA.html PASSOS.json SAIDA.html
O original nao e alterado. PASSOS.json descreve os passos (ver transformer-llm.passos.json).
"""
import json, sys, re

CSS = r'''
/* ===== Passo a passo (injetado) — explicacao embaixo do fluxo, navegacao pelo proprio diagrama ===== */
.container{max-width:min(1800px,100%)!important}
.walk-shell{display:block;margin-top:.5rem}
.walk-shell>.diagram-container{margin:0;padding:4px 10px 10px!important}
.walk-shell>.diagram-container .diagram-nav{top:4px!important;bottom:auto!important;right:10px!important;transform:scale(.75)!important;transform-origin:top right!important}
.walk-panel{margin-top:.6rem;background:var(--panel);border:1px solid var(--panel-border);border-radius:.75rem;
  padding:.7rem 1.1rem .9rem;color:var(--text);font-size:.92rem;line-height:1.55}
.walk-hint{margin:0;color:var(--text-dim);font-size:.76rem}
.walk-detail{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr) minmax(0,1fr);gap:.6rem 2rem;align-items:start}
.walk-detail h3{font-size:1.2rem;margin:.1rem 0 .25rem;line-height:1.3}
.walk-tag{display:inline-block;font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--text-dim);margin-bottom:.15rem}
.walk-lead{margin:.15rem 0 .5rem}
.walk-io{display:grid;grid-template-columns:auto 1fr;gap:.25rem .7rem;margin:0;padding:.6rem .7rem;border-radius:.55rem;
  background:color-mix(in srgb,var(--text) 4%,transparent);border:1px solid var(--panel-border)}
.walk-io dt{font-weight:700;color:var(--arrow-emphasis);font-size:.78rem;text-transform:uppercase;letter-spacing:.05em;padding-top:.1rem}
.walk-io dd{margin:0;font-size:.86rem}
.walk-ill{font-size:.72rem;color:var(--text-dim)}
.walk-terms-title{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--text-dim);margin:0 0 .3rem}
.walk-terms{margin:0;display:grid;gap:.45rem}
.walk-terms div{border-left:2px solid color-mix(in srgb,var(--arrow-emphasis) 60%,transparent);padding-left:.6rem}
.walk-terms dt{font-weight:700;font-size:.84rem}
.walk-terms dd{margin:0;color:var(--text-muted);font-size:.82rem}
/* sem o painel 'Semantic passport' / zoom automatico ao clicar numa caixa: a explicacao fica embaixo */
.walk-shell .relationship-lens{display:none!important}
/* cartoes 'Em uma frase / De onde vem / Siglas' removidos */
.reader-rail,.rail-reveal,.rail-controls{display:none!important}
/* mini-modal tecnico ao clicar numa caixa */
.walk-shell>.diagram-container{position:relative}
.walk-pop{position:absolute;z-index:30;width:min(300px,calc(100% - 20px));padding:.6rem .75rem .7rem;border-radius:.6rem;
  background:color-mix(in srgb,var(--text) 7%,var(--bg));backdrop-filter:none;border:1px solid var(--arrow-emphasis);box-shadow:0 6px 18px rgba(0,0,0,.5);color:var(--text);font-size:.8rem;line-height:1.45}
.walk-pop[hidden]{display:none}
.walk-pop-k{font-size:.62rem;letter-spacing:.08em;text-transform:uppercase;color:var(--arrow-emphasis)}
.walk-pop strong{display:block;font-size:.9rem;margin:.05rem 1.2rem .25rem 0}
.walk-pop p{margin:0;color:var(--text-muted)}
.walk-pop button{position:absolute;top:.3rem;right:.4rem;width:1.4rem;height:1.4rem;border:0;background:transparent;color:var(--text-muted);font-size:1rem;line-height:1;cursor:pointer}
/* navegacao compacta + numeracao no diagrama */
.walk-nav{position:absolute;left:6px;top:50%;transform:translateY(-50%);z-index:6;display:flex;flex-direction:column;gap:.2rem;align-items:center}
.walk-n{width:1.45rem;height:1.45rem;padding:0;border-radius:.4rem;border:1px solid var(--panel-border);background:transparent;color:var(--text-muted);font:600 .72rem/1 inherit;cursor:pointer}
.walk-n:hover:not(:disabled){border-color:var(--arrow-emphasis);color:var(--text)}
.walk-n.on{background:var(--arrow-emphasis);border-color:var(--arrow-emphasis);color:#04130d}
.walk-n:disabled{opacity:.35;cursor:default}
.walk-badge{pointer-events:none}
.walk-badge circle{fill:var(--bg);stroke:var(--text-dim);stroke-width:1}
.walk-badge text{fill:var(--text-muted);font:700 8px sans-serif}
.walk-badge.on circle{fill:var(--arrow-emphasis);stroke:var(--arrow-emphasis)}
.walk-badge.on text{fill:#04130d}
/* destaque no diagrama */
.walk-on svg [data-node-id]{opacity:.3;transition:opacity .25s,filter .25s}
.walk-on svg [data-edge-id]{opacity:.18;transition:opacity .25s}
.walk-on svg [data-node-id].walk-prev{opacity:.62}
.walk-on svg [data-node-id].walk-current{opacity:1;filter:drop-shadow(0 0 9px var(--arrow-emphasis))}
.walk-on svg [data-edge-id].walk-edge{opacity:1}
.walk-on svg [data-node-id]{cursor:pointer}
@media (max-width:1000px){.walk-detail{grid-template-columns:minmax(0,1fr)}}
'''

JS = r'''
(function(){
 var raw=document.getElementById('walk-data'); if(!raw) return;
 var D=JSON.parse(raw.textContent), S=D.steps, U=Object.assign({
  entra:'Entra',sai:'Sai',exemplo:'Exemplo',ilustrativo:'ilustrativo',termos:'Termos',fontes:'Fontes',de:'de',
  dica:'Clique numa caixa do fluxo (ou use as setas ← →) para trocar a explicação. Ative Live no topo para percorrer o fluxo automaticamente.'},D.ui||{});
 var cont=document.querySelector('.container'), dc=cont&&cont.querySelector('.diagram-container'); if(!dc) return;
 var svg=dc.querySelector('svg'); if(!svg) return;
 function el(t,c,x){var e=document.createElement(t); if(c)e.className=c; if(x!==undefined)e.textContent=x; return e;}
 var shell=el('div','walk-shell'); dc.parentNode.insertBefore(shell,dc);
 var panel=el('aside','walk-panel'); panel.setAttribute('aria-label',D.titulo||'Explicação'); shell.appendChild(dc); shell.appendChild(panel);
 var timer=null, chips=[], nav=el('div','walk-nav'), bPrev=el('button','walk-n','▴'), bNext=el('button','walk-n','▾');
 nav.title=U.dica; bPrev.type=bNext.type='button'; bPrev.title='Passo anterior'; bNext.title='Próximo passo';
 bPrev.addEventListener('click',function(){pauseAll(); closePop(); show(cur-1);}); bNext.addEventListener('click',function(){pauseAll(); closePop(); show(cur+1);});
 nav.appendChild(bPrev);
 S.forEach(function(s,i){var b=el('button','walk-n',String(i+1)); b.type='button'; b.title=s.title; b.addEventListener('click',function(){pauseAll(); closePop(); show(i);}); chips.push(b); nav.appendChild(b);});
 nav.appendChild(bNext); dc.appendChild(nav);
 var detail=el('div','walk-detail'); detail.setAttribute('aria-live','polite'); panel.appendChild(detail);
 var nodes=[].slice.call(svg.querySelectorAll('[data-node-id]')), edges=[].slice.call(svg.querySelectorAll('[data-edge-id]')), byNode={};
 S.forEach(function(s,i){byNode[s.node]=i;});
 var NS='http://www.w3.org/2000/svg', badges=[];
 S.forEach(function(s,i){var n=svg.querySelector('[data-node-id="'+s.node+'"]'); if(!n) return; var bb=n.getBBox(), g=document.createElementNS(NS,'g');
  g.setAttribute('class','walk-badge'); g.setAttribute('transform','translate('+bb.x+' '+bb.y+')');
  var c=document.createElementNS(NS,'circle'); c.setAttribute('r','7'); var t=document.createElementNS(NS,'text'); t.textContent=String(i+1); t.setAttribute('text-anchor','middle'); t.setAttribute('y','3');
  g.appendChild(c); g.appendChild(t); svg.appendChild(g); badges[i]=g;});
 var cur=-1;
 function show(i){
  if(i<0||i>=S.length) return; cur=i; var s=S[i];
  shell.classList.add('walk-on');
  nodes.forEach(function(n){var id=n.getAttribute('data-node-id'); n.classList.toggle('walk-current',id===s.node);
   n.classList.toggle('walk-prev',i>0&&id===S[i-1].node);});
  var es={}; (s.edges||[]).forEach(function(x){es[x]=1;}); edges.forEach(function(e){e.classList.toggle('walk-edge',!!es[e.getAttribute('data-edge-id')]);});
  render(s,i);
  chips.forEach(function(c,k){c.classList.toggle('on',k===i);}); bPrev.disabled=(i===0); bNext.disabled=(i===S.length-1);
  badges.forEach(function(g,k){if(g) g.classList.toggle('on',k===i);});
  try{history.replaceState(null,'','#passo='+(i+1));}catch(e){}
 }
 function render(s,i){
  detail.textContent='';
  var c1=el('div'), c2=el('div'), c3=el('div');
  c1.appendChild(el('div','walk-tag',(s.fase?s.fase+' · ':'')+(i+1)+' '+U.de+' '+S.length));
  c1.appendChild(el('h3','',s.title));
  if(s.resumo) c1.appendChild(el('p','walk-lead',s.resumo));
  (s.notas||[]).forEach(function(n){c1.appendChild(el('p','walk-lead',n));});
  var rows=[[U.entra,s.entra],[U.sai,s.sai],[U.exemplo,s.exemplo]].filter(function(r){return r[1];});
  if(rows.length){var dl=el('dl','walk-io'); rows.forEach(function(r){dl.appendChild(el('dt','',r[0])); var dd=el('dd','',r[1]);
    if(r[0]===U.exemplo&&s.ilustrativo){dd.appendChild(document.createElement('br')); dd.appendChild(el('span','walk-ill','('+U.ilustrativo+')'));} dl.appendChild(dd);}); c2.appendChild(dl);}
  if(s.termos&&s.termos.length){c3.appendChild(el('div','walk-terms-title',U.termos)); var t=el('dl','walk-terms');
   s.termos.forEach(function(k){var d=el('div'); d.appendChild(el('dt','',k[0])); d.appendChild(el('dd','',k[1])); t.appendChild(d);}); c3.appendChild(t);}
  detail.appendChild(c1); detail.appendChild(c2); detail.appendChild(c3);
 }
 var pop=el('div','walk-pop'); pop.hidden=true; pop.setAttribute('role','dialog'); dc.appendChild(pop);
 function closePop(){pop.hidden=true;}
 var html=document.documentElement, btnMotion=document.getElementById('btn-motion'), STEP_MS=6500;
 function isLive(){return html.getAttribute('data-motion')==='live';}
 function stop(){ if(timer){clearInterval(timer); timer=null;} }
 function pauseAll(){ stop(); if(isLive()&&btnMotion) btnMotion.click(); }
 function tick(){ show(cur>=S.length-1?0:cur+1); }
 function play(){ closePop(); if(cur<0||cur>=S.length-1) show(0); stop(); timer=setInterval(tick,STEP_MS); }
 function sync(){ if(isLive()) play(); else stop(); }
 if(btnMotion){ new MutationObserver(sync).observe(html,{attributes:true,attributeFilter:['data-motion']}); }
 function openPop(g,s){
  pop.textContent=''; var x=el('button','','×'); x.type='button'; x.setAttribute('aria-label','Fechar'); x.addEventListener('click',closePop);
  pop.appendChild(el('div','walk-pop-k','Técnico')); pop.appendChild(el('strong','',s.title)); pop.appendChild(el('p','',s.tecnico||'')); pop.appendChild(x);
  pop.hidden=false; var d=dc.getBoundingClientRect(), r=g.getBoundingClientRect(), w=pop.offsetWidth, h=pop.offsetHeight;
  var left=Math.max(10,Math.min(r.left-d.left+r.width/2-w/2,d.width-w-10)), top=r.bottom-d.top+8; if(top+h>d.height-10) top=Math.max(10,r.top-d.top-h-8);
  pop.style.left=left+'px'; pop.style.top=top+'px';}
 function pick(e){var g=e.target.closest&&e.target.closest('[data-node-id]'); if(!g||!svg.contains(g)) return false;
  pauseAll(); e.stopPropagation(); e.preventDefault(); var i=byNode[g.getAttribute('data-node-id')]; if(i!==undefined){show(i); if(S[i].tecnico) openPop(g,S[i]); else closePop();} return true;}
 dc.addEventListener('click',function(e){ if(!pick(e)&&!pop.contains(e.target)) closePop(); },true);
 dc.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' ') pick(e); },true);
 document.addEventListener('keydown',function(e){
  var t=e.target&&e.target.tagName; if(t==='INPUT'||t==='SELECT'||t==='TEXTAREA'||e.metaKey||e.ctrlKey||e.altKey) return;
  if(e.key==='Escape'){closePop(); pauseAll();}
  else if(e.key==='ArrowRight'){pauseAll(); closePop(); e.preventDefault(); show(Math.min(cur+1,S.length-1));}
  else if(e.key==='ArrowLeft'&&cur>0){pauseAll(); closePop(); e.preventDefault(); show(cur-1);}
 });
 var m=/passo=(\d+)/.exec(location.hash);
 setTimeout(function(){ if(isLive()&&btnMotion) btnMotion.click(); },0); show(m?Math.max(0,Math.min(S.length-1,parseInt(m[1],10)-1)):0);
})();
'''

def move_legend_top(html):
    """Move a legenda (interativa, dentro do SVG) para o topo, numa unica linha com o titulo, aproveitando o vazio acima das faixas."""
    m = re.search(r'<svg viewBox="0 0 (\d+) (\d+)"', html)
    g = re.search(r'<g data-legend="" data-legend-bridge="">\s*<text x="\d+" y="(\d+)"', html)
    if not (m and g):
        return html
    w, ly = int(m.group(1)), int(g.group(1))
    html = html.replace(g.group(0), g.group(0).replace('<g data-legend="" data-legend-bridge="">',
        '<g data-legend="" data-legend-bridge="" transform="translate(0 %d)">' % (26 - ly)), 1)
    # itens na mesma linha do titulo "Legend"
    html = re.sub(r'(<g data-legend-semantic-kind="[^"]+" data-legend-kind=)', r'<g transform="translate(0 -17)" data-legend-semantic-kind=" data-legend-kind=', html) if False else \
        html.replace('<g data-legend-semantic-kind=', '<g transform="translate(0 -17)" data-legend-semantic-kind=')
    html = re.sub(r'(<g data-legend="" data-legend-bridge=""[^>]*>\s*)<text [^>]*>Legend</text>', r'\1', html, count=1)
    return html.replace(m.group(0), '<svg viewBox="0 14 %d %d"' % (w, ly - 32), 1)

def main():
    src, steps, out = sys.argv[1:4]
    html = open(src, encoding='utf-8').read()
    data = json.load(open(steps, encoding='utf-8'))
    blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    assert '</head>' in html and '</body>' in html
    html = move_legend_top(html)
    html = html.replace('</head>', '<style id="walk-css">' + CSS + '</style>\n</head>', 1)
    inject = ('<script id="walk-data" type="application/json">' + blob + '</script>\n'
              '<script id="walk-js">' + JS + '</script>\n')
    idx = html.rindex('</body>')
    html = html[:idx] + inject + html[idx:]
    open(out, 'w', encoding='utf-8').write(html)
    print('ok', out)

main()
