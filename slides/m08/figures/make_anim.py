"""Build the three HTML animations of the m08 deck:  python3 figures/make_anim.py  (from slides/m08).

Output goes to anim/*.html (not committed; the deck embeds them with <iframe>, so they play in the HTML
export and show one still frame in the PDF).  All data are computed here and pasted into the pages:
  skipgram.html     a window slides over text, samples pairs, and the pairs move 2D word vectors (real SGNS run)
  growth.html       popularity-similarity growth: r = ln t, uniform angle, links to the m smallest s * theta_st
  reconstruct.html  the rank-d approximation A_d of the karate club for a chosen d
Each page takes ?still=N and draws that frame without playing (used for screenshots).
"""

import json
import math
import random
import shutil
from pathlib import Path

import networkx as nx
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "anim"
FONTS = Path.home() / ".claude/skills/slide-math/fonts"

BASE_CSS = """
@font-face{font-family:SS3;src:url(fonts/SourceSans3-Regular.otf);font-weight:400}
@font-face{font-family:SS3;src:url(fonts/SourceSans3-Bold.otf);font-weight:700}
@font-face{font-family:SS3;src:url(fonts/SourceSans3-It.otf);font-style:italic}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#FAF9F6;color:#000;font-family:SS3,'Helvetica Neue',Arial,sans-serif;overflow:hidden}
svg{display:block;width:100%;height:auto}
.bar{white-space:nowrap;display:flex;align-items:center;gap:10px;height:40px;padding:0 4px;font-size:22px}
button{font:inherit;font-size:20px;padding:2px 16px;border:2px solid #000;border-radius:6px;background:#fff;cursor:pointer}
button:hover{background:#F4E6FF}
.muted{fill:#969696;color:#969696}
body.still .bar button{visibility:hidden}
"""

CTRL_JS = """
function bindBar(api){
  var q=function(i){return document.getElementById(i)};
  q('play').onclick=function(){api.toggle()};
  q('step').onclick=function(){api.pause();api.step()};
  q('restart').onclick=function(){api.restart()};
}
"""


def page(title, body, script, extra_css=""):
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title>"
            f"<style>{BASE_CSS}{extra_css}</style></head><body>{body}<script>if(/still=/.test(location.search))document.body.className='still';</script><script>{CTRL_JS}{script}</script></body></html>")


BAR = ("<div class='bar'><button id='play'>Pause</button><button id='step'>Step</button>"
       "<button id='restart'>Restart</button><span id='status' style='margin-left:14px;color:#555'></span></div>")


# --------------------------------------------------------------------------------------- skip-gram

def skipgram():
    sents = ["the king wears the royal crown", "the queen wears the royal crown", "the dog chews the old bone",
             "the cat chases the old mouse", "the king and the queen rule", "the dog and the cat sleep"]
    S = [s.split() for s in sents]
    vocab = sorted({w for s in S for w in s})
    ix = {w: i for i, w in enumerate(vocab)}
    lr, epochs, seed, K = 0.6, 6, 59, 2
    rng = np.random.default_rng(seed)
    X = rng.normal(0, 0.3, (len(vocab), 2))          # query vectors u (shown)
    Y = rng.normal(0, 0.3, (len(vocab), 2))          # key vectors v (hidden)
    sig = lambda z: 1 / (1 + np.exp(-z))
    frames, init = [], X.copy()
    for _ in range(epochs):
        for si, s in enumerate(S):
            for c in range(len(s)):
                for d in (-1, 1):
                    j = c + d
                    if not 0 <= j < len(s):
                        continue
                    i, jj = ix[s[c]], ix[s[j]]
                    g = 1 - sig(X[i] @ Y[jj])
                    xi = X[i].copy()
                    X[i] += lr * g * Y[jj]
                    Y[jj] += lr * g * xi
                    negs = []
                    for _ in range(K):
                        neg = int(rng.integers(len(vocab)))
                        while neg in (i, jj):
                            neg = int(rng.integers(len(vocab)))
                        g = -sig(X[i] @ Y[neg])
                        xi = X[i].copy()
                        X[i] += lr * g * Y[neg]
                        Y[neg] += lr * g * xi
                        negs.append(neg)
                    frames.append([si, c, j, negs, [round(float(v), 3) for v in X.ravel()]])
    allp = np.array([f[4] for f in frames[-60:]] + [init.ravel().tolist()]).reshape(-1, len(vocab), 2)
    allp[-1] *= 0.5
    data = {"vocab": vocab, "sents": [[ix[w] for w in s] for s in S], "frames": frames,
            "init": [round(float(v), 3) for v in init.ravel()],
            "bbox": [float(allp[..., 0].min()), float(allp[..., 0].max()), float(allp[..., 1].min()), float(allp[..., 1].max())],
            "perEpoch": len(frames) // epochs}
    body = "<svg id='svg' viewBox='0 0 1170 490'></svg>" + BAR
    js = """
var D=__DATA__, NS='http://www.w3.org/2000/svg', svg=document.getElementById('svg');
var still=(location.search.match(/still=(\\d+)/)||[])[1];
function E(tag,attrs,parent,text){var e=document.createElementNS(NS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(text!=null)e.textContent=text;(parent||svg).appendChild(e);return e}
var INK='#000',HL='#F4E6FF',HLC='#E5FDFF',RED='#D55E00',MUT='#969696';
// panel titles
E('text',{x:0,y:26,'font-size':24,'font-weight':700,fill:INK},0,'1  Window over the text');
E('text',{x:0,y:334,'font-size':24,'font-weight':700,fill:INK},0,'2  Sampled pairs');
E('text',{x:650,y:26,'font-size':24,'font-weight':700,fill:INK},0,'3  Query vectors u in 2D');
// arrows between panels
E('path',{d:'M 598 250 L 634 250',stroke:INK,'stroke-width':3,fill:'none'});
E('path',{d:'M 634 250 l -12 -9 M 634 250 l -12 9',stroke:INK,'stroke-width':3,fill:'none'});
// text panel
var CW=98,CH=38,X0=2,Y0=44,GAP=44,cells=[];
var win=E('rect',{rx:10,ry:10,fill:HL,stroke:INK,'stroke-width':2.5,height:CH+12,width:3*CW,x:X0-6,y:Y0-6,style:'transition:all .35s ease'});
D.sents.forEach(function(s,si){var row=[];s.forEach(function(w,c){
  var g=E('g',{transform:'translate('+(X0+c*CW)+','+(Y0+si*GAP)+')'});
  var r=E('rect',{width:CW-10,height:CH,rx:8,fill:'#fff',stroke:MUT,'stroke-width':1.5},g);
  var t=E('text',{x:(CW-10)/2,y:CH/2+10,'text-anchor':'middle','font-size':28,fill:INK},g,D.vocab[w]);
  row.push({g:g,r:r,t:t})});cells.push(row)});
// pairs panel
E('text',{x:380,y:380,'font-size':24,fill:INK},0,'label 1: pull together');
E('text',{x:380,y:438,'font-size':24,fill:RED},0,'label 0: push apart');
var posT=E('text',{x:0,y:382,'font-size':34,'font-weight':700,fill:INK},0,'');
var negT=[0,1].map(function(i){return E('text',{x:0,y:424+i*40,'font-size':34,fill:RED},0,'')});
// scatter panel
var PX=650,PY=44,PW=520,PH=420;
E('rect',{x:PX,y:PY,width:PW,height:PH,fill:'#fff',stroke:INK,'stroke-width':2,rx:6});
var bb=D.bbox,pad=0.25,sx=(PW-60)/(bb[1]-bb[0]+2*pad),sy=(PH-60)/(bb[3]-bb[2]+2*pad),sc=Math.min(sx,sy);
var cx=PX+PW/2-sc*(bb[0]+bb[1])/2, cy=PY+PH/2+sc*(bb[2]+bb[3])/2;
function map(x,y){return [cx+sc*x, cy-sc*y]}
var ghost=E('circle',{r:9,fill:'none',stroke:MUT,'stroke-width':2.5,'stroke-dasharray':'4 3',opacity:0});
var mv=E('line',{stroke:INK,'stroke-width':3.5,opacity:0});
var pts=D.vocab.map(function(w){var g=E('g',{style:'transition:transform .35s ease'});
  var c=E('circle',{r:9,fill:'#fff',stroke:INK,'stroke-width':2.5},g);
  var t=E('text',{x:14,y:-10,'font-size':27,fill:INK,stroke:'#fff','stroke-width':5,'paint-order':'stroke'},g,w);return {g:g,c:c,t:t}});
var CAND=[[14,-10,'start'],[14,28,'start'],[-14,-10,'end'],[-14,28,'end'],[0,-20,'middle'],[0,42,'middle']],choice=D.vocab.map(function(){return 0});
function place(P){var M=D.vocab.map(function(w,i){return map(P[2*i],P[2*i+1])}),placed=[];
  function rect(i,c){var w=D.vocab[i].length*14+6,x=M[i][0]+CAND[c][0],h=30,y=M[i][1]+CAND[c][1];
    var l=CAND[c][2]=='start'?x:CAND[c][2]=='end'?x-w:x-w/2;return [l,y-24,l+w,y+6]}
  function hit(a,b){return !(a[2]<b[0]||b[2]<a[0]||a[3]<b[1]||b[3]<a[1])}
  function bad(i,c){var r=rect(i,c);for(var q=0;q<M.length;q++){if(q!=i&&hit(r,[M[q][0]-11,M[q][1]-11,M[q][0]+11,M[q][1]+11]))return true}
    for(var q=0;q<placed.length;q++){if(hit(r,placed[q]))return true}return false}
  D.vocab.forEach(function(w,i){var c=choice[i];if(bad(i,c)){for(var t=0;t<CAND.length;t++){if(!bad(i,t)){c=t;break}}}
    choice[i]=c;placed.push(rect(i,c));var t=pts[i].t;t.setAttribute('x',CAND[c][0]);t.setAttribute('y',CAND[c][1]);t.setAttribute('text-anchor',CAND[c][2])})}
var K=-1,playing=!still,timer=null,N=D.frames.length;
function coords(k){return k<0?D.init:D.frames[k][4]}
function show(k){
  K=k;var P=coords(k),fr=k<0?null:D.frames[k];
  var tr=Math.min(380,Math.max(60,dwell(k)*0.8));
  pts.forEach(function(p,i){var m=map(P[2*i],P[2*i+1]);p.g.style.transitionDuration=tr+'ms';p.g.setAttribute('transform','translate('+m[0]+','+m[1]+')');
    p.c.setAttribute('fill','#fff');p.c.setAttribute('stroke-width',2.5);p.t.setAttribute('font-weight',400)});
  place(P);
  cells.forEach(function(row){row.forEach(function(c){c.r.setAttribute('stroke-width',1.5);c.r.setAttribute('stroke',MUT);c.t.setAttribute('font-weight',400)})});
  if(!fr){posT.textContent='';negT.forEach(function(t){t.textContent=''});ghost.setAttribute('opacity',0);mv.setAttribute('opacity',0);
    document.getElementById('status').textContent='initial random vectors';return}
  var si=fr[0],c=fr[1],j=fr[2],ngs=fr[3],s=D.sents[si];
  var lo=Math.max(c-1,0),hi=Math.min(c+1,s.length-1);
  win.setAttribute('x',X0+lo*CW-6);win.setAttribute('y',Y0+si*GAP-6);win.setAttribute('width',(hi-lo+1)*CW-10+12);
  cells[si][c].t.setAttribute('font-weight',700);cells[si][c].r.setAttribute('stroke',INK);cells[si][c].r.setAttribute('stroke-width',3);
  cells[si][j].r.setAttribute('stroke',INK);cells[si][j].r.setAttribute('stroke-width',3);
  var wi=s[c],wj=s[j],W=D.vocab;
  posT.textContent=W[wi]+'  \\u2192  '+W[wj];
  negT.forEach(function(t,q){t.textContent=W[wi]+'  \\u21E2  '+W[ngs[q]]});
  pts[wi].c.setAttribute('fill',HL);pts[wi].t.setAttribute('font-weight',700);
  var q=coords(k-1),a=map(q[2*wi],q[2*wi+1]),b=map(P[2*wi],P[2*wi+1]);
  ghost.setAttribute('cx',a[0]);ghost.setAttribute('cy',a[1]);ghost.setAttribute('opacity',1);
  mv.setAttribute('x1',a[0]);mv.setAttribute('y1',a[1]);mv.setAttribute('x2',b[0]);mv.setAttribute('y2',b[1]);mv.setAttribute('opacity',1);
  document.getElementById('status').textContent='pair '+(k+1)+' of '+N+'   (pass '+(Math.floor(k/D.perEpoch)+1)+' over the text)';
}
function dwell(k){var e=Math.floor(Math.max(k,0)/D.perEpoch);return [700,320,140,70][Math.min(e,3)]}
function tick(){if(!playing)return;if(K+1>=N){playing=false;document.getElementById('play').textContent='Play';timer=setTimeout(function(){api.restart()},4000);return}
  show(K+1);timer=setTimeout(tick,dwell(K))}
var api={toggle:function(){if(playing){api.pause()}else{if(K+1>=N)K=-1;playing=true;document.getElementById('play').textContent='Pause';clearTimeout(timer);tick()}},
  pause:function(){playing=false;clearTimeout(timer);document.getElementById('play').textContent='Play'},
  step:function(){if(K+1<N)show(K+1)},
  restart:function(){clearTimeout(timer);show(-1);playing=true;document.getElementById('play').textContent='Pause';timer=setTimeout(tick,700)}};
bindBar(api);
if(still!=null){show(parseInt(still)-1)}else{show(-1);document.getElementById('play').textContent='Pause';timer=setTimeout(tick,900)}
document.addEventListener('visibilitychange',function(){if(document.hidden)api.pause()});
""".replace("__DATA__", json.dumps(data))
    (OUT / "skipgram.html").write_text(page("skip-gram", body, js))


# ------------------------------------------------------------------------------------------ growth

def growth():
    rnd = random.Random(7)
    N, m = 110, 2
    th = [0.0] + [rnd.uniform(0, 2 * math.pi) for _ in range(N)]
    links = {}
    for t in range(2, N + 1):
        cand = []
        for s in range(1, t):
            d = abs(th[s] - th[t])
            d = min(d, 2 * math.pi - d)
            cand.append((s * d, s))
        links[t] = [s for _, s in sorted(cand)[: min(m, t - 1)]]
    data = {"th": [round(v, 4) for v in th], "links": {str(t): v for t, v in links.items()}, "N": N, "m": m}
    body = "<svg id='svg' viewBox='0 0 570 490'></svg>" + BAR
    js = """
var D=__DATA__, NS='http://www.w3.org/2000/svg', svg=document.getElementById('svg');
var still=(location.search.match(/still=(\\d+)/)||[])[1];
function E(tag,attrs,parent,text){var e=document.createElementNS(NS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(text!=null)e.textContent=text;(parent||svg).appendChild(e);return e}
var INK='#000',HL='#F4E6FF',HLC='#E5FDFF',RED='#D55E00',MUT='#969696';
var CX=285,CY=208,R=198,RL=Math.log(D.N);
var s1=E('text',{x:285,y:446,'font-size':27,'text-anchor':'middle',fill:INK},0,''),s2=E('text',{x:285,y:480,'font-size':25,'text-anchor':'middle',fill:'#555'},0,'');
function rad(t){return R*Math.log(t)/RL}
function pos(t){return t==1?[CX,CY]:[CX+rad(t)*Math.cos(D.th[t]),CY-rad(t)*Math.sin(D.th[t])]}
var gEdges=E('g',{}),gNodes=E('g',{});
var ring=E('circle',{cx:CX,cy:CY,r:0,fill:'none',stroke:INK,'stroke-width':2,'stroke-dasharray':'8 6',opacity:0});
var axis=E('line',{x1:CX,y1:CY,x2:CX+R+14,y2:CY,stroke:MUT,'stroke-width':1.5,'stroke-dasharray':'5 5',opacity:0});
var ray=E('line',{x1:CX,y1:CY,x2:CX,y2:CY,stroke:INK,'stroke-width':2,opacity:0});
var arc=E('path',{d:'',fill:'none',stroke:INK,'stroke-width':2.5,opacity:0});
var tTh=E('text',{x:0,y:0,'font-size':28,'font-style':'italic',fill:INK,opacity:0,stroke:'#FAF9F6','stroke-width':5,'paint-order':'stroke'},0,'\\u03b8');
var tR=E('text',{x:0,y:0,'font-size':28,'font-style':'italic',fill:INK,opacity:0,stroke:'#FAF9F6','stroke-width':5,'paint-order':'stroke'},0,'r');
var nodes=[],edges=[],T=0,playing=!still,timer=null;
function addNode(t,cur){var p=pos(t),c=E('circle',{cx:p[0],cy:p[1],r:cur?9:5.5,fill:cur?HL:'#fff',stroke:INK,'stroke-width':cur?3:1.8},gNodes);nodes[t]=c}
function relink(t){var o=[];D.links[t].forEach(function(s){var a=pos(t),b=pos(s);var l=E('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:RED,'stroke-width':4.5},gEdges);edges.push([t,l])});}
function settle(t){if(nodes[t]){nodes[t].setAttribute('r',5.5);nodes[t].setAttribute('fill','#fff');nodes[t].setAttribute('stroke-width',1.8)}
  edges.forEach(function(e){if(e[0]==t){e[1].setAttribute('stroke',MUT);e[1].setAttribute('stroke-width',1.6)}})}
function info(t){var th=D.th[t]*180/Math.PI;var tgt=D.links[t]||[];
  s1.textContent='t = '+t+'    r = ln t = '+(t==1?'0':Math.log(t).toFixed(2))+'    \\u03b8 = '+(t==1?'\\u2013':th.toFixed(0)+'\\u00b0');
  s2.textContent=tgt.length?'links to nodes '+tgt.join(' and '):'first node'}
function gauge(t){
  if(t==1){ring.setAttribute('opacity',0);ray.setAttribute('opacity',0);arc.setAttribute('opacity',0);tTh.setAttribute('opacity',0);tR.setAttribute('opacity',0);axis.setAttribute('opacity',0);return}
  var r=rad(t),th=D.th[t],p=pos(t);
  axis.setAttribute('opacity',1);ring.setAttribute('r',r);ring.setAttribute('opacity',1);
  ray.setAttribute('x2',p[0]);ray.setAttribute('y2',p[1]);ray.setAttribute('opacity',1);
  var ra=Math.min(46,r*0.45),ax=CX+ra,ay=CY,bx=CX+ra*Math.cos(th),by=CY-ra*Math.sin(th);
  arc.setAttribute('d','M '+ax+' '+ay+' A '+ra+' '+ra+' 0 '+(th>Math.PI?1:0)+' 0 '+bx+' '+by);arc.setAttribute('opacity',1);
  var am=th/2;tTh.setAttribute('x',CX+(ra+22)*Math.cos(am)-8);tTh.setAttribute('y',CY-(ra+22)*Math.sin(am)+8);tTh.setAttribute('opacity',ra>20?1:0);
  tR.setAttribute('x',CX+r*0.5*Math.cos(th)+12*Math.sin(th));tR.setAttribute('y',CY-r*0.5*Math.sin(th)+12*Math.cos(th)+8);tR.setAttribute('opacity',r>26?1:0)}
function build(t){ // instant: nodes 1..t, last one current
  gEdges.innerHTML='';gNodes.innerHTML='';edges=[];nodes=[];
  for(var u=2;u<=t;u++){relink(u);settle(u)}
  for(var u=1;u<=t;u++){addNode(u,u==t&&t>1)}
  edges.forEach(function(e){if(e[0]==t&&t>1){e[1].setAttribute('stroke',RED);e[1].setAttribute('stroke-width',4.5)}});
  gauge(t);info(t);T=t}
function dwell(t){return t<8?1500:t<20?800:t<45?380:110}
function next(){if(T>=D.N){playing=false;document.getElementById('play').textContent='Play';timer=setTimeout(function(){api.restart()},4500);return}
  var t=T+1;settle(T);var prev=T;T=t;gauge(t);addNode(t,true);info(t);
  setTimeout(function(){if(T==t)relink(t)},Math.min(300,dwell(t)*0.4));
  if(playing)timer=setTimeout(next,dwell(t))}
var api={toggle:function(){if(playing)api.pause();else{if(T>=D.N)build(1);playing=true;document.getElementById('play').textContent='Pause';clearTimeout(timer);next()}},
  pause:function(){playing=false;clearTimeout(timer);document.getElementById('play').textContent='Play'},
  step:function(){if(T<D.N){var was=playing;playing=false;next()}},
  restart:function(){clearTimeout(timer);build(1);playing=true;document.getElementById('play').textContent='Pause';timer=setTimeout(next,900)}};
bindBar(api);
if(still!=null){build(parseInt(still))}else{build(1);document.getElementById('play').textContent='Pause';timer=setTimeout(next,900)}
document.addEventListener('visibilitychange',function(){if(document.hidden)api.pause()});
""".replace("__DATA__", json.dumps(data))
    (OUT / "growth.html").write_text(page("growth", body, js))


# ------------------------------------------------------------------------------------- reconstruct

def reconstruct():
    G = nx.karate_club_graph()
    A = nx.to_numpy_array(G, weight=None)
    L = np.diag(A.sum(1)) - A
    _, V = np.linalg.eigh(L)
    order = np.argsort(V[:, 1])
    lam, U = np.linalg.eigh(A)
    idx = np.argsort(-np.abs(lam))
    lam, U = lam[idx], U[:, idx]
    data = {"A": A[np.ix_(order, order)].astype(int).tolist(), "lam": [round(float(v), 4) for v in lam],
            "U": [[round(float(v), 4) for v in row] for row in U[order]]}
    css = ("#c{display:block}.row{display:flex;gap:18px;align-items:flex-start;padding:4px 0}.lab{font-size:26px;text-align:center;margin-top:2px}"
           "input[type=range]{width:360px;height:30px;accent-color:#000}#dv{font-weight:700;font-size:32px;min-width:44px;display:inline-block}"
           "#err{font-size:28px;margin-left:30px;color:#222}")
    body = ("<div class='bar' style='height:48px;font-size:30px;gap:14px'><span>kept terms <i>d</i> =</span>"
            "<input id='sl' type='range' min='0' max='34' value='6'><span id='dv'>6</span><span id='err'></span></div>"
            "<div class='row'><svg id='sp' viewBox='0 0 470 316' style='width:470px;height:316px;flex:none'></svg>"
            "<div><canvas id='a' width='240' height='240'></canvas><div class='lab'><b>A</b></div></div>"
            "<div style='font-size:46px;align-self:center;margin-top:-20px'>→</div>"
            "<div><canvas id='b' width='240' height='240'></canvas><div class='lab'><b>A</b><sub><i>d</i></sub>: orange &gt; 0, <span style='color:#0072B2'>blue</span> &lt; 0</div></div></div>")
    js = """
var D=__DATA__, n=34, NS='http://www.w3.org/2000/svg';
function col(v){v=Math.max(-1,Math.min(1,v));var neg=[0,114,178],pos=[213,94,0],tg=v>=0?pos:neg,t=Math.abs(v);
  return 'rgb('+[0,1,2].map(function(i){return Math.round(255+(tg[i]-255)*t)}).join(',')+')'}
function draw(id,M,bin){var cv=document.getElementById(id),x=cv.getContext('2d'),c=cv.width/n;x.clearRect(0,0,cv.width,cv.height);
  x.fillStyle='#fff';x.fillRect(0,0,cv.width,cv.height);
  for(var i=0;i<n;i++)for(var j=0;j<n;j++){var v=M[i][j];if(bin){if(!v)continue;x.fillStyle='#000'}else{if(Math.abs(v)<0.02)continue;x.fillStyle=col(v)}
    x.fillRect(Math.floor(j*c),Math.floor(i*c),Math.ceil(c),Math.ceil(c))}
  x.strokeStyle='#000';x.lineWidth=2;x.strokeRect(1,1,cv.width-2,cv.height-2)}
function Ad(d){var M=[];for(var i=0;i<n;i++){M.push(new Array(n).fill(0))}
  for(var k=0;k<d;k++)for(var i=0;i<n;i++){var a=D.lam[k]*D.U[i][k];for(var j=0;j<n;j++)M[i][j]+=a*D.U[j][k]}return M}
// spectrum
var sp=document.getElementById('sp');
function E(tag,attrs,text){var e=document.createElementNS(NS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(text!=null)e.textContent=text;sp.appendChild(e);return e}
var X0=48,DX=12.6,YM=[-14,23],PH=256,PY=34;
function yy(v){return PY+(YM[1]-v)/(YM[1]-YM[0])*PH}
E('text',{x:235,y:22,'font-size':26,'text-anchor':'middle'},'eigenvalue \\u03bb\\u2096, ordered by |\\u03bb\\u2096|');
var band=E('rect',{x:X0-6,y:PY,width:0,height:PH,fill:'#F4E6FF'});
E('line',{x1:X0-8,y1:yy(0),x2:466,y2:yy(0),stroke:'#000','stroke-width':1.6});
[-10,0,10,20].forEach(function(v){E('text',{x:X0-14,y:yy(v)+8,'font-size':22,'text-anchor':'end'},String(v));E('line',{x1:X0-8,y1:yy(v),x2:X0-3,y2:yy(v),stroke:'#000'})});
var dots=D.lam.map(function(l,k){return E('circle',{cx:X0+DX*k+4,cy:yy(l),r:4.8,fill:'#fff',stroke:'#000','stroke-width':1.8})});
[1,10,20,30].forEach(function(k){E('text',{x:X0+DX*(k-1)+4,y:yy(0)+(k==1?-0:0)+PH*0+330-yy(0)+yy(0)-yy(0)+0,'font-size':0},'')});
[1,10,20,30].forEach(function(k){E('text',{x:X0+DX*(k-1)+4,y:312,'font-size':22,'text-anchor':'middle'},String(k))});
function upd(d){document.getElementById('dv').textContent=d;var e=0;for(var k=d;k<n;k++)e+=D.lam[k]*D.lam[k];
  document.getElementById('err').innerHTML='error \\u2016A \\u2212 A<sub>d</sub>\\u2016<sub>F</sub><sup>2</sup> = <b>'+e.toFixed(1)+'</b>';
  band.setAttribute('width',d>0?DX*d:0);dots.forEach(function(c,k){c.setAttribute('fill',k<d?'#000':'#fff')});draw('b',Ad(d),false)}
draw('a',D.A,true);
var sl=document.getElementById('sl');var st=(location.search.match(/still=(\\d+)/)||[])[1];if(st!=null)sl.value=st;
sl.oninput=function(){upd(parseInt(sl.value))};upd(parseInt(sl.value));
""".replace("__DATA__", json.dumps(data))
    (OUT / "reconstruct.html").write_text(page("reconstruct", body, js, css))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "fonts").mkdir(exist_ok=True)
    for f in ("SourceSans3-Regular.otf", "SourceSans3-Bold.otf", "SourceSans3-It.otf"):
        shutil.copy(FONTS / f, OUT / "fonts" / f)
    skipgram()
    growth()
    reconstruct()
    print("animations written to", OUT)
