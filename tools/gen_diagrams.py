# Generates animated SVG versions of every diagram. Run from repo root: python3 tools/gen_diagrams.py
import math, datetime as dt
P=dict(v='#a78bfa',i='#818cf8',s='#38bdf8',c='#22d3ee',g='#34d399',p='#f472b6',a='#fbbf24',o='#fb923c')
FONT='font-family="Segoe UI,Arial,sans-serif"'
def esc(t): return t.replace('&','&amp;').replace('<','&lt;')
def wr(fn,W,H,body,defs=''):
    open('assets/'+fn,'w').write(f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg"><defs>{defs}'
    '<linearGradient id="card" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f172a"/><stop offset="1" stop-color="#1e1b4b"/></linearGradient>'
    '<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#a78bfa"/><stop offset="1" stop-color="#22d3ee"/></linearGradient>'
    '<filter id="f" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    '<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#94a3b8"/></marker></defs>'
    f'<rect width="{W}" height="{H}" rx="16" fill="url(#card)" stroke="#4c1d95"/>{body}</svg>')
def N(id,x,y,t,c,**k): return dict(id=id,x=x,y=y,t=t,c=c,**k)
def meas(n):
    L=n['t'].split('\n')
    if n.get('box'): return max(len(l) for l in L)*7.6+34, 28+len(L)*18
    return max(len(l) for l in L)*8.6+36, 22+len(L)*19
def clip(cx,cy,w,h,tx,ty):
    dx,dy=tx-cx,ty-cy
    s=min((w/2)/abs(dx) if dx else 1e9,(h/2)/abs(dy) if dy else 1e9)
    return cx+dx*s,cy+dy*s
def graph(fn,W,H,nodes,edges,groups=()):
    M={}
    for n in nodes:
        w,h=meas(n);x=n['x']
        if n.get('anchor')=='r':x-=w/2
        if n.get('anchor')=='l':x+=w/2
        M[n['id']]=(x,n['y'],w,h,n)
    b=''
    for gx,gy,gw,gh,gl,gc in groups:
        b+=f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="18" fill="{gc}" fill-opacity=".06" stroke="{gc}" stroke-opacity=".6" stroke-dasharray="8 6"><animate attributeName="stroke-dashoffset" from="28" to="0" dur="3s" repeatCount="indefinite"/></rect><text x="{gx+16}" y="{gy+24}" {FONT} font-size="14" font-weight="700" fill="{gc}">{esc(gl)}</text>'
    for k,e in enumerate(edges):
        a,c2,bend,lab=(list(e)+[0,None])[:4] if len(e)<4 else e[:4]
        ax,ay,aw,ah,an=M[a];bx,by,bw,bh,bn=M[c2];col=an['c']
        mx,my=(ax+bx)/2,(ay+by)/2
        if bend:
            dx,dy=bx-ax,by-ay;l=math.hypot(dx,dy) or 1;cx,cy=mx-dy/l*bend,my+dx/l*bend
            p0=clip(ax,ay,aw,ah,cx,cy);p2=clip(bx,by,bw,bh,cx,cy)
            d=f'M{p0[0]:.1f} {p0[1]:.1f} Q{cx:.1f} {cy:.1f} {p2[0]:.1f} {p2[1]:.1f}';lx,ly=.25*p0[0]+.5*cx+.25*p2[0],.25*p0[1]+.5*cy+.25*p2[1]
        else:
            p0=clip(ax,ay,aw,ah,bx,by);p2=clip(bx,by,bw,bh,ax,ay)
            d=f'M{p0[0]:.1f} {p0[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f}';lx,ly=mx,my
        b+=f'<path d="{d}" fill="none" stroke="#475569" stroke-width="2" marker-end="url(#ar)"/>'
        b+=f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2.6" stroke-dasharray="5 17" stroke-linecap="round" filter="url(#f)"><animate attributeName="stroke-dashoffset" from="22" to="0" dur="1.3s" repeatCount="indefinite"/></path>'
        b+=f'<circle r="4.5" fill="#fff" filter="url(#f)"><animateMotion path="{d}" dur="{2.2+k%3*.4}s" begin="{k*.25%2}s" repeatCount="indefinite"/></circle>'
        if lab: b+=f'<text x="{lx:.0f}" y="{ly-6:.0f}" text-anchor="middle" {FONT} font-size="12" fill="#e2e8f0" stroke="#0b1020" stroke-width="4" paint-order="stroke">{esc(lab)}</text>'
    for i,(x,y,w,h,n) in enumerate(M.values()):
        c=n['c'];L=n['t'].split('\n');rx=x-w/2;ry=y-h/2
        b+=f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="#0b1020" stroke="{c}" stroke-width="2"/>'
        b+=f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="none" stroke="{c}" stroke-width="3" filter="url(#f)"><animate attributeName="opacity" values=".9;.1;.9" dur="3s" begin="{i*.27%3:.2f}s" repeatCount="indefinite"/></rect>'
        if n.get('box'):
            b+=f'<text x="{x:.1f}" y="{ry+22:.1f}" text-anchor="middle" {FONT} font-size="14" font-weight="800" fill="{c}">{esc(L[0])}</text><line x1="{rx+8:.1f}" x2="{rx+w-8:.1f}" y1="{ry+30:.1f}" y2="{ry+30:.1f}" stroke="{c}" stroke-opacity=".5"/>'
            for j,l in enumerate(L[1:]): b+=f'<text x="{rx+16:.1f}" y="{ry+48+j*18:.1f}" font-family="Consolas,monospace" font-size="12" fill="#cbd5e1">{esc(l)}</text>'
        else:
            for j,l in enumerate(L): b+=f'<text x="{x:.1f}" y="{y-(len(L)-1)*9.5+j*19+5:.1f}" text-anchor="middle" {FONT} font-size="14" font-weight="600" fill="#e0e7ff">{esc(l)}</text>'
    wr(fn,W,H,b)
def keys(s,e): return f'keyTimes="0;{s:.3f};{e:.3f};1"'
# ---------- graph diagrams ----------
def vision():
    n=[N('A',285,50,'🧠 AI & Intelligence Systems',P['v']),N('D',830,50,'💻 Full-Stack Architecture',P['s']),
       N('B',95,190,'👁️ Computer Vision\n& ML/DL',P['v']),N('C',285,190,'⚡ Expert Systems\n& Agents',P['v']),N('H',440,190,'💬 NLP &\nGenerative AI',P['v']),
       N('E',660,190,'🎨 Modern Frontend\nSystems',P['s']),N('F',830,190,'⚙️ Backend &\nDatabases',P['s']),N('I',1000,190,'🐳 DevOps &\nCloud Delivery',P['s']),
       N('G',550,335,'🚀 End-to-End Enterprise Solutions',P['g'])]
    e=[('A','B'),('A','C'),('A','H'),('D','E'),('D','F'),('D','I')]+[(x,'G') for x in 'BCHEFI']
    graph('vision.svg',1100,390,n,e)
def mindmap():
    n=[N('r',580,265,'🌌 Nibras & Dana',P['v'])];e=[]
    br=[('ai',370,130,'🧠 AI & Data Science',P['v'],'r',['Computer Vision','Deep Learning','Machine Learning','Multi-Agent Systems','Expert Systems']),
        ('fs',370,400,'💻 Full-Stack',P['s'],'r',['Responsive UI','Flutter','State Management','FastAPI','Laravel','Microservices']),
        ('db',790,130,'🗄️ Databases',P['g'],'l',['Oracle 12c PL/SQL','EER Modeling','Normalization 1NF-BCNF','Query Optimization']),
        ('do',790,400,'🐳 DevOps',P['o'],'l',['Git & GitHub Actions','Docker','Linux & Bash'])]
    for id,x,y,t,c,side,ls in br:
        n.append(N(id,x,y,t,c));e.append(('r',id))
        for j,l in enumerate(ls):
            yy=y+(j-(len(ls)-1)/2)*46;n.append(N(f'{id}{j}',230 if side=='r' else 900,yy,l,c,anchor=side));e.append((id,f'{id}{j}'))
    graph('mindmap.svg',1160,560,n,e)
def mllife():
    t=['📥 Data Collection','🧹 Cleaning & EDA','🧪 Feature Engineering','🏋️ Model Training','📊 Evaluation & Tuning','📦 Deployment API','📡 Monitoring'];pos=[(110,70),(330,70),(570,70),(800,70),(800,230),(570,230),(330,230)]
    cs=[P['i'],P['i'],P['v'],P['v'],P['a'],P['g'],P['c']]
    n=[N(str(i),x,y,t[i].replace(' ','\n',1) if len(t[i])>16 else t[i],cs[i]) for i,(x,y) in enumerate(pos)]
    e=[('0','1'),('1','2'),('2','3'),('3','4'),('4','3',70,'Underfit / Overfit'),('4','5'),('5','6'),('6','0',0,'Data Drift')]
    graph('ml-lifecycle.svg',920,300,n,e)
def agents():
    n=[N('U',450,40,'👤 User Request',P['v']),N('O',450,125,'🎯 Orchestrator Agent',P['v']),N('R',170,235,'🔎 Research Agent',P['s']),N('P',450,235,'🧩 Planner Agent',P['s']),N('C',730,235,'💻 Coder Agent',P['s']),
       N('M',450,330,'🧠 Shared Memory / Vector DB',P['c']),N('V',450,415,'✅ Validator Agent',P['a']),N('X',740,415,'📤 Final Response',P['g'])]
    e=[('U','O'),('O','R'),('O','P'),('O','C'),('R','M'),('P','M'),('C','M'),('M','V'),('V','O',-700,'Rejected'),('V','X',0,'Approved')]
    graph('multi-agent.svg',900,470,n,e)
def arch():
    n=[N('W',110,130,'🌐 Web SPA',P['v']),N('M',110,300,'📱 Flutter App',P['v']),N('G',330,215,'🚪 API Gateway\nJWT / OAuth',P['s']),N('S1',560,130,'FastAPI Service',P['s']),N('S2',560,300,'Laravel Service',P['s']),
       N('ML',845,120,'Inference Server',P['p']),N('VD',845,195,'Vector Store',P['p']),N('OR',845,320,'Oracle 12c',P['g']),N('CA',845,385,'Cache',P['g'])]
    e=[('W','G'),('M','G'),('G','S1'),('G','S2'),('S1','ML'),('ML','VD'),('S1','OR'),('S2','OR'),('S2','CA')]
    gr=[(20,60,200,300,'🎨 Client Layer',P['v']),(250,60,430,310,'⚙️ Backend Layer',P['s']),(720,50,260,210,'🧠 AI Layer',P['p']),(720,270,260,150,'🗄️ Data Layer',P['g'])]
    graph('architecture.svg',1000,440,n,e,gr)
def er():
    n=[N('U',110,140,'USER\nint id PK\nstring name\nstring email',P['v'],box=1),N('P',390,140,'PROJECT\nint id PK\nint user_id FK\nstring title',P['s'],box=1),
       N('T',690,70,'TASK\nint id PK\nint project_id FK\nstring status',P['g'],box=1),N('R',690,260,'MODEL_RUN\nint id PK\nint project_id FK\nstring algorithm\ndate trained_at',P['p'],box=1),
       N('Me',920,260,'METRIC\nint id PK\nint run_id FK\nstring name\nfloat value',P['a'],box=1)]
    e=[('U','P',0,'owns'),('P','T',0,'contains'),('P','R',0,'trains'),('R','Me',0,'records')]
    graph('er.svg',1040,360,n,e)
def state():
    n=[N('A',120,180,'👤 Anonymous',P['v']),N('B',390,180,'🔑 Authenticating',P['s']),N('C',660,180,'✅ Authenticated',P['g']),N('D',660,340,'🔄 Refreshing',P['a'])]
    e=[('A','B',0,'Login'),('B','C',0,'Valid JWT'),('B','A',55,'Invalid Credentials'),('C','D',0,'Token Expired'),('D','C',160,'Refresh OK'),('D','A',-95,'Refresh Failed'),('C','A',-150,'Logout')]
    graph('auth-state.svg',860,420,n,e)
def cicd():
    t=['💾 Git Push','🧪 Lint & Tests','🐳 Docker Build','🔒 Security Scan','🚢 Deploy Staging','✅ Approved?','🚀 Production'];pos=[(100,80),(300,80),(500,80),(700,80),(700,230),(500,230),(300,230)]
    cs=[P['i'],P['s'],P['s'],P['p'],P['a'],P['o'],P['g']]
    n=[N(str(i),x,y,t[i],cs[i]) for i,(x,y) in enumerate(pos)]
    e=[('0','1'),('1','2'),('2','3'),('3','4'),('4','5'),('5','6',0,'Yes'),('5','0',0,'No')]
    graph('cicd.svg',820,320,n,e)
# ---------- custom diagrams ----------
def seq():
    W,H=1000,540;A=[('👤 Client / UI',110,P['v']),('🎨 Frontend',300,P['i']),('⚙️ API Gateway',500,P['s']),('🧠 AI / ML Model',700,P['p']),('🗄️ DB Cluster',890,P['g'])]
    M=[(0,1,'Interacts with UI'),(1,2,'REST / GraphQL request'),(2,3,'Inference call'),(3,2,'Predictions'),(2,4,'Query / persist'),(4,2,'ACID response'),(2,1,'JSON / WebSocket'),(1,0,'UI update')]
    b=''
    for t,x,c in A: b+=f'<line x1="{x}" y1="72" x2="{x}" y2="{H-20}" stroke="{c}" stroke-opacity=".5" stroke-dasharray="5 7"/><rect x="{x-72}" y="24" width="144" height="42" rx="12" fill="#0b1020" stroke="{c}" stroke-width="2" filter="url(#f)"/><text x="{x}" y="51" text-anchor="middle" {FONT} font-size="14" font-weight="700" fill="#e0e7ff">{t}</text>'
    n=len(M)
    for i,(a,c2,l) in enumerate(M):
        y=120+i*48;x1,x2=A[a][1],A[c2][1];col=A[a][2];s=.05+i/(n+.5);e=s+.7/(n+.5);d=f'M{x1} {y} L{x2} {y}'
        b+=f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#475569" stroke-width="2" marker-end="url(#ar)"{" stroke-dasharray=\"6 5\"" if i in (3,5,6,7) else ""}/>'
        b+=f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="3.5" filter="url(#f)" opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{s:.3f};{e:.3f};{e+.04:.3f};1" dur="12s" repeatCount="indefinite"/></line>'
        b+=f'<circle r="6" fill="#fff" filter="url(#f)" opacity="0"><animateMotion path="{d}" dur="12s" repeatCount="indefinite" calcMode="linear" keyPoints="0;0;1;1" {keys(s,e)}/><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{s:.3f};{e:.3f};{e+.01:.3f};1" dur="12s" repeatCount="indefinite"/></circle>'
        b+=f'<text x="{(x1+x2)/2}" y="{y-9}" text-anchor="middle" {FONT} font-size="13" fill="#e2e8f0">{i+1}. {esc(l)}</text>'
    wr('sequence.svg',W,H,b)
def pie():
    D=[('Deep Learning & Computer Vision',30,P['v']),('Backend & APIs',25,P['s']),('Databases & SQL',20,P['g']),('Frontend & Mobile',15,P['p']),('DevOps & Tooling',10,P['a'])]
    r=90;C=2*math.pi*r;b='';st=0
    for i,(l,v,c) in enumerate(D):
        ln=C*v/100;s=.03+i*.09;e=s+.14
        b+=f'<circle cx="220" cy="160" r="{r}" fill="none" stroke="{c}" stroke-width="46" stroke-dasharray="{ln-3:.1f} {C-ln+3:.1f}" stroke-dashoffset="{-st:.1f}" transform="rotate(-90 220 160)" filter="url(#f)"><animate attributeName="stroke-dasharray" values="0 {C:.1f};0 {C:.1f};{ln-3:.1f} {C-ln+3:.1f};{ln-3:.1f} {C-ln+3:.1f};0 {C:.1f}" keyTimes="0;{s:.2f};{e:.2f};.92;1" dur="9s" repeatCount="indefinite"/></circle>'
        b+=f'<circle cx="470" cy="{90+i*36}" r="8" fill="{c}"><animate attributeName="r" values="7;10;7" dur="3s" begin="{i*.4}s" repeatCount="indefinite"/></circle><text x="494" y="{95+i*36}" {FONT} font-size="15" fill="#e2e8f0">{esc(l)}</text><text x="760" y="{95+i*36}" text-anchor="end" {FONT} font-size="16" font-weight="800" fill="{c}">{v}%</text>'
        st+=ln
    b+=f'<text x="220" y="156" text-anchor="middle" {FONT} font-size="15" fill="#94a3b8">Technical</text><text x="220" y="178" text-anchor="middle" {FONT} font-size="20" font-weight="800" fill="url(#g)">Focus</text>'
    wr('focus-pie.svg',800,320,b)
def skillbars():
    D=[('Python',92),('DeepLearning',88),('FastAPI',90),('Laravel',82),('Flutter',80),('Oracle',88),('Docker',78),('Git',90)];W,H=900,340;base=270;top=50;b=''
    for k in range(5):
        y=base-k*(base-top)/4;b+=f'<line x1="60" x2="870" y1="{y}" y2="{y}" stroke="#334155" stroke-dasharray="3 6"/><text x="48" y="{y+4}" text-anchor="end" {FONT} font-size="11" fill="#64748b">{k*25}</text>'
    for i,(l,v) in enumerate(D):
        x=95+i*98;h=(base-top)*v/100;y=base-h;c=list(P.values())[i%8];bg=i*.15
        b+=f'<rect x="{x}" width="58" rx="8" fill="{c}" filter="url(#f)" y="{base}" height="0"><animate attributeName="y" values="{base};{y};{y};{base}" keyTimes="0;.25;.9;1" dur="8s" begin="{bg}s" repeatCount="indefinite"/><animate attributeName="height" values="0;{h};{h};0" keyTimes="0;.25;.9;1" dur="8s" begin="{bg}s" repeatCount="indefinite"/></rect>'
        b+=f'<text x="{x+29}" y="{y-8}" text-anchor="middle" {FONT} font-size="14" font-weight="800" fill="{c}" opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.2;.3;.9;1" dur="8s" begin="{bg}s" repeatCount="indefinite"/>{v}%</text><text x="{x+29}" y="{base+24}" text-anchor="middle" {FONT} font-size="13" fill="#cbd5e1">{l}</text>'
    wr('skills-bar.svg',W,H,b)
def gitgraph():
    W,H=1000,370;L={'main':(70,P['v']),'dev':(150,P['s']),'ai':(230,P['p']),'ui':(310,P['g'])}
    C=[('init','main',80),('setup','dev',200),('train','ai',300),('optimize','ai',400),('merge','dev',520),('dashboard','ui',620),('merge','dev',740),('v1.0','main',890)]
    S=[(0,1),(1,2),(2,3),(3,4),(1,4),(4,5),(5,6),(4,6),(0,7),(6,7)];b=''
    for k,(y,c) in L.items(): b+=f'<line x1="30" x2="990" y1="{y}" y2="{y}" stroke="{c}" stroke-opacity=".18" stroke-dasharray="4 8"/><text x="990" y="{y-10}" text-anchor="end" {FONT} font-size="12" fill="{c}">{ {"main":"main","dev":"develop","ai":"feature/ai-model","ui":"feature/ui"}[k] }</text>'
    for i,(a,c2) in enumerate(S):
        (_,la,xa),(_,lb,xb)=C[a],C[c2];ya,yb=L[la][0],L[lb][0];col=L[max((la,lb),key=lambda q:L[q][0])][1];xm=(xa+xb)/2
        d=f'M{xa} {ya} L{xb} {yb}' if ya==yb else f'M{xa} {ya} C{xm} {ya} {xm} {yb} {xb} {yb}'
        b+=f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-opacity=".4"/><path d="{d}" fill="none" stroke="{col}" stroke-width="3" stroke-dasharray="5 16" stroke-linecap="round" filter="url(#f)"><animate attributeName="stroke-dashoffset" from="21" to="0" dur="1.2s" repeatCount="indefinite"/></path><circle r="5" fill="#fff" filter="url(#f)"><animateMotion path="{d}" dur="3s" begin="{i*.35}s" repeatCount="indefinite"/></circle>'
    for i,(t,l,x) in enumerate(C):
        y,c=L[l];b+=f'<circle cx="{x}" cy="{y}" r="10" fill="#0b1020" stroke="{c}" stroke-width="3" filter="url(#f)"><animate attributeName="r" values="9;13;9" dur="2.5s" begin="{i*.3}s" repeatCount="indefinite"/></circle><text x="{x}" y="{y+30}" text-anchor="middle" {FONT} font-size="12" fill="#cbd5e1">{t}</text>'
    b+=f'<rect x="{890-26}" y="20" width="52" height="24" rx="12" fill="{P["a"]}" fill-opacity=".2" stroke="{P["a"]}"><animate attributeName="fill-opacity" values=".1;.5;.1" dur="2s" repeatCount="indefinite"/></rect><text x="890" y="37" text-anchor="middle" {FONT} font-size="13" font-weight="800" fill="{P["a"]}">v1.0</text>'
    wr('git-graph.svg',W,H,b)
def gantt():
    T=[('Deep Learning Models','AI',dt.date(2025,1,1),120,'done',P['g']),('Multi-Agent Systems','AI',dt.date(2025,6,1),150,'active',P['v']),('Microservices Platform','Full-Stack',dt.date(2025,5,1),140,'active',P['s']),('Cloud Deployment','Full-Stack',dt.date(2025,10,1),90,'planned',P['o'])]
    s0=dt.date(2025,1,1);X0,X1=250,960;ppd=(X1-X0)/365;W,H=1000,330;b=''
    for m in range(12):
        x=X0+(dt.date(2025,m+1,1)-s0).days*ppd;b+=f'<line x1="{x:.0f}" x2="{x:.0f}" y1="60" y2="{H-30}" stroke="#334155" stroke-dasharray="3 6"/><text x="{x+4:.0f}" y="50" {FONT} font-size="12" fill="#94a3b8">{dt.date(2025,m+1,1):%b}</text>'
    for i,(l,sec,st,ln,stt,c) in enumerate(T):
        y=80+i*55;x=X0+(st-s0).days*ppd;w=ln*ppd
        b+=f'<text x="24" y="{y+22}" {FONT} font-size="14" fill="#e2e8f0">{l}</text><text x="24" y="{y+38}" {FONT} font-size="11" fill="{c}">{sec} · {stt}</text>'
        b+=f'<rect x="{x:.0f}" y="{y}" height="30" rx="9" fill="{c}" fill-opacity="{.35 if stt=="planned" else .9}" stroke="{c}" {"stroke-dasharray=\"6 4\"" if stt=="planned" else ""} filter="url(#f)" width="0"><animate attributeName="width" values="0;{w:.0f};{w:.0f};0" keyTimes="0;.3;.9;1" dur="9s" begin="{i*.4}s" repeatCount="indefinite"/></rect>'
        if stt=='active': b+=f'<rect x="{x:.0f}" y="{y}" width="40" height="30" rx="9" fill="#fff" fill-opacity=".25"><animate attributeName="x" values="{x:.0f};{x+w-40:.0f};{x:.0f}" dur="3s" repeatCount="indefinite"/></rect>'
    wr('roadmap.svg',W,H,b)
for f in (vision,mindmap,mllife,agents,arch,er,state,cicd,seq,pie,skillbars,gitgraph,gantt): f()
print('diagrams ok')
